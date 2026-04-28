#!/usr/bin/env python3
"""Sync accepted LeetCode submissions into the repository.

Default behavior:
  - Pulls submissions newer than the last sync (incremental).
  - Keeps only ACCEPTED submissions.
  - Writes the LATEST accepted submission per (problem, language) as the
    canonical solution file (older code attempts are not stored, but their
    metadata is kept in the per-problem submission history).
  - Refreshes problem metadata (title, difficulty, tags, stats) via GraphQL.
  - Regenerates per-problem READMEs and the main solutions table.

Use --full to ignore the incremental marker and rebuild from scratch.
"""

import argparse
import json
import logging
import os
import sys
from collections import defaultdict
from typing import Dict, List, Optional

# Allow running as `python scripts/sync_submissions.py` from the repo root
# OR from inside the scripts folder.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from leetcode_api import LeetCodeClient, lang_to_ext, load_cookies
from repo_io import (
    PROBLEMS_DIR,
    collect_all_rows,
    detect_languages,
    find_existing_problem_folder,
    load_problem_history,
    load_problem_metadata,
    merge_submission_history,
    problem_folder_name,
    save_problem_history,
    save_problem_metadata,
    slugify_safe,
    update_main_readme,
    write_problem_readme,
)


MANIFEST_FILE = ".leetcode_sync.json"


def load_manifest() -> Dict:
    if not os.path.exists(MANIFEST_FILE):
        return {"last_submission_timestamp": None, "last_sync": None}
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_manifest(manifest: Dict) -> None:
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")


def configure_logging(verbose: int) -> None:
    level = logging.WARNING
    if verbose == 1:
        level = logging.INFO
    elif verbose >= 2:
        level = logging.DEBUG
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=level,
    )


def parse_args():
    p = argparse.ArgumentParser(
        description="Sync accepted LeetCode submissions into this repo."
    )
    p.add_argument("--cookies", help="Cookie header string from leetcode.com")
    p.add_argument(
        "--full",
        action="store_true",
        help="Ignore the incremental marker and re-scan all submissions.",
    )
    p.add_argument(
        "--language",
        help="Comma-separated language filter (e.g. python3,cpp). Default: all.",
    )
    p.add_argument(
        "--no-readme",
        action="store_true",
        help="Skip rewriting the main README table.",
    )
    p.add_argument(
        "--refresh-metadata",
        action="store_true",
        help="Re-fetch problem metadata for every touched problem (slower).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without writing any files.",
    )
    p.add_argument("-v", "--verbose", action="count", default=0)
    return p.parse_args()


def fetch_new_submissions(
    client: LeetCodeClient,
    stop_at_timestamp: Optional[int],
    language_filter: Optional[set],
) -> List[Dict]:
    new_subs: List[Dict] = []
    for sub in client.iter_submissions(stop_at_timestamp=stop_at_timestamp):
        if sub.get("status_display") != "Accepted":
            continue
        if language_filter and sub.get("lang") not in language_filter:
            continue
        new_subs.append(sub)
        if len(new_subs) % 20 == 0:
            print(f"  fetched {len(new_subs)} accepted submissions so far...")
    return new_subs


def group_latest_by_lang(subs: List[Dict]) -> Dict[str, Dict[str, Dict]]:
    """Return slug -> lang -> latest submission (by timestamp)."""
    out: Dict[str, Dict[str, Dict]] = defaultdict(dict)
    for s in subs:
        slug = s["title_slug"]
        lang = s["lang"]
        cur = out[slug].get(lang)
        if cur is None or s["timestamp"] > cur["timestamp"]:
            out[slug][lang] = s
    return out


def write_solution_file(folder: str, slug: str, sub: Dict) -> str:
    ext = sub["extension"] or lang_to_ext(sub["lang"])
    filename = f"{slugify_safe(slug)}.{ext}"
    path = os.path.join(folder, filename)
    code = sub.get("code", "")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(code)
        if not code.endswith("\n"):
            f.write("\n")
    return path


def main():
    args = parse_args()
    configure_logging(args.verbose)

    if not os.path.exists("README.md") or not os.path.isdir("scripts"):
        print(
            "ERROR: Run this script from the repo root "
            "(where README.md and scripts/ live).",
            file=sys.stderr,
        )
        sys.exit(1)

    language_filter = None
    if args.language:
        language_filter = {l.strip() for l in args.language.split(",") if l.strip()}

    cookies = load_cookies(args.cookies)
    print("Authenticating with LeetCode...")
    client = LeetCodeClient(cookies)

    manifest = load_manifest()
    stop_at = None if args.full else manifest.get("last_submission_timestamp")
    if stop_at:
        print(f"Incremental sync: fetching submissions newer than {stop_at}.")
    else:
        print("Full sync: fetching all submissions (this may take a while).")

    new_subs = fetch_new_submissions(client, stop_at, language_filter)
    print(f"Found {len(new_subs)} accepted submissions to process.")

    if not new_subs and not args.full and not args.refresh_metadata:
        print("Nothing new. Re-rendering main README from existing data...")
        if not args.no_readme and not args.dry_run:
            update_main_readme(collect_all_rows())
        print("Done.")
        return

    grouped = group_latest_by_lang(new_subs)
    os.makedirs(PROBLEMS_DIR, exist_ok=True)

    written_files = 0
    touched_folders: List[str] = []

    for slug, by_lang in grouped.items():
        # Find existing folder or compute a new one.
        folder = find_existing_problem_folder(slug)
        metadata = load_problem_metadata(folder) if folder else None
        need_metadata_fetch = (
            metadata is None
            or args.refresh_metadata
            or "questionFrontendId" not in metadata
        )

        if need_metadata_fetch:
            print(f"  fetching metadata for {slug}...")
            metadata = client.get_problem_metadata(slug)
            if not metadata:
                logging.warning("Skipping %s: no metadata available.", slug)
                continue

        if folder is None:
            folder_name = problem_folder_name(
                str(metadata.get("questionFrontendId", "0")), slug
            )
            folder = os.path.join(PROBLEMS_DIR, folder_name)
            if not args.dry_run:
                os.makedirs(folder, exist_ok=True)

        if args.dry_run:
            print(f"[dry-run] would write {len(by_lang)} solution(s) for {slug} into {folder}")
            continue

        save_problem_metadata(folder, metadata)

        history = load_problem_history(folder)
        history["slug"] = slug
        history = merge_submission_history(history, list(by_lang.values()))
        save_problem_history(folder, history)

        for lang, sub in by_lang.items():
            write_solution_file(folder, slug, sub)
            written_files += 1

        languages = detect_languages(folder)
        write_problem_readme(folder, metadata, history, languages)
        touched_folders.append(folder)

    print(f"Wrote {written_files} solution file(s) across {len(touched_folders)} problem(s).")

    if args.dry_run:
        print("Dry run: no manifest or README updates persisted.")
        return

    if not args.no_readme:
        print("Refreshing main README solutions table...")
        update_main_readme(collect_all_rows())

    if new_subs:
        max_ts = max(s["timestamp"] for s in new_subs)
        prev = manifest.get("last_submission_timestamp") or 0
        manifest["last_submission_timestamp"] = max(prev, max_ts)
    import datetime
    manifest["last_sync"] = datetime.datetime.now().isoformat(timespec="seconds")
    save_manifest(manifest)

    print("Sync complete. Don't forget to:")
    print("  git add problems/ README.md")
    print("  git commit -m \"Sync LeetCode solutions\"")


if __name__ == "__main__":
    main()
