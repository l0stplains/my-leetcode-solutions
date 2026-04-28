#!/usr/bin/env python3
"""Manually add a solution from the workspace folder.

Use this when you want to add a polished solution outside the sync flow,
e.g., a hand-cleaned version of your accepted submission, or a solution for
a problem you solved offline.

Usage:
    python add_solution.py <filename> <slug> [--no-network]

  <filename>: file inside workspace/, e.g., my-solution.py
  <slug>:     LeetCode problem slug from the URL, e.g., two-sum

The script will:
  1. Copy workspace/<filename> into problems/<id>-<slug>/<slug>.<ext>
  2. Fetch problem metadata via the LeetCode GraphQL API (unless --no-network)
  3. Update the per-problem README and main solutions table
"""

import argparse
import datetime
import os
import shutil
import sys

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


EXT_TO_LANG = {
    "py": "python3",
    "c": "c",
    "cpp": "cpp",
    "cc": "cpp",
    "cxx": "cpp",
    "cs": "csharp",
    "java": "java",
    "kt": "kotlin",
    "js": "javascript",
    "ts": "typescript",
    "go": "golang",
    "rb": "ruby",
    "php": "php",
    "rs": "rust",
    "swift": "swift",
    "scala": "scala",
    "sh": "bash",
    "sql": "mysql",
    "ex": "elixir",
    "erl": "erlang",
    "rkt": "racket",
    "dart": "dart",
}


def parse_args():
    p = argparse.ArgumentParser(description="Add a LeetCode solution from workspace/.")
    p.add_argument("filename", help="File inside workspace/")
    p.add_argument("slug", help="LeetCode problem slug (from the URL)")
    p.add_argument(
        "--no-network",
        action="store_true",
        help="Skip metadata fetch (uses cached .meta.json if present)",
    )
    p.add_argument(
        "--cookies",
        help="LeetCode cookies (only needed when fetching metadata for a new problem)",
    )
    p.add_argument(
        "--lang",
        help="Override language detection (e.g. python3, cpp).",
    )
    return p.parse_args()


def main():
    args = parse_args()

    if not os.path.exists("README.md") or not os.path.isdir("scripts"):
        print(
            "ERROR: Run from the repo root (where README.md and scripts/ live).",
            file=sys.stderr,
        )
        sys.exit(1)

    src = os.path.join("workspace", args.filename)
    if not os.path.isfile(src):
        print(f"ERROR: workspace/{args.filename} not found.", file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(args.filename)[1].lstrip(".").lower()
    lang = args.lang or EXT_TO_LANG.get(ext)
    if not lang:
        print(
            f"ERROR: Could not infer LeetCode language from .{ext}. "
            "Pass --lang to override.",
            file=sys.stderr,
        )
        sys.exit(1)

    folder = find_existing_problem_folder(args.slug)
    metadata = load_problem_metadata(folder) if folder else None

    if metadata is None and not args.no_network:
        cookies = load_cookies(args.cookies)
        print(f"Fetching metadata for {args.slug}...")
        client = LeetCodeClient(cookies)
        metadata = client.get_problem_metadata(args.slug)
        if not metadata:
            print(f"ERROR: Could not fetch metadata for {args.slug}.", file=sys.stderr)
            sys.exit(1)

    if metadata is None:
        # --no-network and no cached metadata: use a bare-bones placeholder.
        metadata = {
            "questionFrontendId": "0",
            "title": args.slug.replace("-", " ").title(),
            "titleSlug": args.slug,
            "difficulty": "Unknown",
            "topicTags": [],
            "stats_parsed": {},
            "similar_parsed": [],
        }

    if folder is None:
        folder = os.path.join(
            PROBLEMS_DIR,
            problem_folder_name(str(metadata.get("questionFrontendId", "0")), args.slug),
        )
        os.makedirs(folder, exist_ok=True)

    save_problem_metadata(folder, metadata)

    file_ext = lang_to_ext(lang)
    dest = os.path.join(folder, f"{slugify_safe(args.slug)}.{file_ext}")
    shutil.copy2(src, dest)
    print(f"Copied workspace/{args.filename} -> {dest}")

    history = load_problem_history(folder)
    history["slug"] = args.slug
    history = merge_submission_history(history, [{
        "id": int(datetime.datetime.now().timestamp() * 1000),  # synthetic id
        "lang": lang,
        "timestamp": int(datetime.datetime.now().timestamp()),
        "date_formatted": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status_display": "Accepted",
        "runtime": "manual",
        "memory": "manual",
    }])
    save_problem_history(folder, history)

    write_problem_readme(folder, metadata, history, detect_languages(folder))
    update_main_readme(collect_all_rows())

    print(f"Updated README and main solutions table for {args.slug}.")
    print("Don't forget to commit:")
    print(f"  git add {folder} README.md")
    print(f"  git commit -m \"Add solution for {args.slug}\"")


if __name__ == "__main__":
    main()
