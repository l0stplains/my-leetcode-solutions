"""Shared helpers for reading/writing the repo state.

Both sync_submissions.py and add_solution.py import from here so the on-disk
format stays consistent.
"""

import datetime
import json
import os
import re
from typing import Dict, List, Optional

from leetcode_api import LANG_DISPLAY_NAME, lang_display, lang_to_ext, PROBLEM_URL


PROBLEMS_DIR = "problems"
MAIN_README = "README.md"
TABLE_START = "<!-- SOLUTIONS_TABLE_START -->"
TABLE_END = "<!-- SOLUTIONS_TABLE_END -->"

# Difficulty sort order for tables/stats.
DIFFICULTY_RANK = {"Easy": 1, "Medium": 2, "Hard": 3}


def slugify_safe(slug: str) -> str:
    """LeetCode slugs are already filesystem-safe but be defensive anyway."""
    return re.sub(r"[^a-zA-Z0-9._-]", "-", slug)


def problem_folder_name(question_frontend_id: str, slug: str) -> str:
    return f"{question_frontend_id}-{slugify_safe(slug)}"


def find_existing_problem_folder(slug: str) -> Optional[str]:
    """Look up an existing folder for this slug (slug is the stable key)."""
    if not os.path.isdir(PROBLEMS_DIR):
        return None
    safe = slugify_safe(slug)
    suffix = f"-{safe}"
    for entry in os.listdir(PROBLEMS_DIR):
        full = os.path.join(PROBLEMS_DIR, entry)
        if os.path.isdir(full) and entry.endswith(suffix):
            return full
    return None


def load_problem_history(folder: str) -> Dict:
    path = os.path.join(folder, ".submissions.json")
    if not os.path.exists(path):
        return {"slug": "", "submissions": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_problem_history(folder: str, record: Dict) -> None:
    path = os.path.join(folder, ".submissions.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, sort_keys=True)
        f.write("\n")


def merge_submission_history(record: Dict, new_subs: List[Dict]) -> Dict:
    """Merge newly seen submissions into the per-problem history.

    Only metadata is kept (no code). Deduplicated by submission id.
    """
    existing = {s["id"]: s for s in record.get("submissions", [])}
    for sub in new_subs:
        existing[sub["id"]] = {
            "id": sub["id"],
            "lang": sub["lang"],
            "timestamp": sub["timestamp"],
            "date_formatted": sub["date_formatted"],
            "status_display": sub["status_display"],
            "runtime": sub["runtime"],
            "memory": sub["memory"],
        }
    record["submissions"] = sorted(
        existing.values(), key=lambda s: s["timestamp"], reverse=True
    )
    return record


def detect_languages(folder: str) -> List[str]:
    """Scan the folder for solution files and infer languages by extension."""
    langs = set()
    ext_to_lang = {}
    for lang, ext in {l: lang_to_ext(l) for l in LANG_DISPLAY_NAME}.items():
        ext_to_lang.setdefault(ext, lang)
    if not os.path.isdir(folder):
        return []
    for name in os.listdir(folder):
        if name.startswith(".") or name == "README.md":
            continue
        full = os.path.join(folder, name)
        if not os.path.isfile(full):
            continue
        _, ext = os.path.splitext(name)
        ext = ext.lstrip(".").lower()
        lang = ext_to_lang.get(ext)
        if lang:
            langs.add(lang)
    return sorted(langs, key=lambda l: lang_display(l).lower())


def write_problem_readme(
    folder: str,
    metadata: Dict,
    history: Dict,
    languages: List[str],
) -> None:
    """Render the per-problem README from metadata + accepted history."""
    readme_path = os.path.join(folder, "README.md")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    title = metadata.get("title", history.get("slug", "Unknown"))
    slug = metadata.get("titleSlug", history.get("slug", ""))
    qid = metadata.get("questionFrontendId", "?")
    difficulty = metadata.get("difficulty", "Unknown")
    is_paid = metadata.get("isPaidOnly", False)
    likes = metadata.get("likes")
    dislikes = metadata.get("dislikes")
    tags = [t.get("name", "") for t in metadata.get("topicTags", []) or []]
    stats = metadata.get("stats_parsed") or {}
    url = PROBLEM_URL.format(slug)

    lines = []
    lines.append(f"# {qid}. {title}")
    lines.append("")
    lines.append(f"**Problem:** [{slug}]({url})")
    lines.append("")

    info_bits = [f"**Difficulty:** {difficulty}"]
    if is_paid:
        info_bits.append("**Premium:** Yes")
    if likes is not None and dislikes is not None:
        info_bits.append(f"**Likes / Dislikes:** {likes} / {dislikes}")
    lines.append("  \n".join(info_bits))
    lines.append("")

    if tags:
        tag_str = ", ".join(f"`{t}`" for t in tags)
        lines.append(f"**Tags:** {tag_str}")
        lines.append("")

    if stats:
        lines.append("## Statistics")
        lines.append("")
        if "acRate" in stats:
            lines.append(f"- **Acceptance Rate:** {stats['acRate']}")
        if "totalAccepted" in stats:
            lines.append(f"- **Total Accepted:** {stats['totalAccepted']}")
        if "totalSubmission" in stats:
            lines.append(f"- **Total Submissions:** {stats['totalSubmission']}")
        lines.append("")
        lines.append(f"> *Last updated: {now}*")
        lines.append("")

    lines.append("## Solutions")
    lines.append("")
    if not languages:
        lines.append("_No solution files found._")
        lines.append("")
    else:
        for lang in languages:
            ext = lang_to_ext(lang)
            filename = f"{slugify_safe(slug)}.{ext}"
            if not os.path.exists(os.path.join(folder, filename)):
                for n in os.listdir(folder):
                    if n.endswith(f".{ext}") and not n.startswith("."):
                        filename = n
                        break
            lines.append(f"- **{lang_display(lang)}**: [{filename}](./{filename})")
        lines.append("")

    accepted = [
        s for s in history.get("submissions", []) if s.get("status_display") == "Accepted"
    ]
    if accepted:
        lines.append("## Accepted Submission History")
        lines.append("")
        lines.append("| Date | Language | Runtime | Memory |")
        lines.append("| ---- | -------- | ------- | ------ |")
        for s in accepted:
            lines.append(
                f"| {s['date_formatted']} | {lang_display(s['lang'])} | "
                f"{s.get('runtime', '')} | {s.get('memory', '')} |"
            )
        lines.append("")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def update_main_readme(rows: List[Dict]) -> None:
    """Rewrite the solutions table in the main README.

    Each row: {qid, title, slug, folder, difficulty, tags, languages}.
    Sorted by numeric qid.
    """
    if not os.path.exists(MAIN_README):
        raise FileNotFoundError("Main README.md not found in current directory.")

    with open(MAIN_README, "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find(TABLE_START)
    end = content.find(TABLE_END)
    if start == -1 or end == -1:
        raise ValueError("README.md is missing the SOLUTIONS_TABLE markers.")

    def sort_key(r):
        try:
            return (0, int(r["qid"]))
        except (ValueError, TypeError):
            return (1, str(r["qid"]))

    sorted_rows = sorted(rows, key=sort_key)

    table_lines = [
        "| # | Title | Difficulty | Tags | Languages |",
        "| - | ----- | ---------- | ---- | --------- |",
    ]
    for r in sorted_rows:
        title_link = f"[{r['title']}]({r['folder'].replace(os.sep, '/')})"
        tag_str = ", ".join(r["tags"][:5]) if r["tags"] else ""
        if r["tags"] and len(r["tags"]) > 5:
            tag_str += f", +{len(r['tags']) - 5}"
        lang_str = ", ".join(lang_display(l) for l in r["languages"])
        table_lines.append(
            f"| {r['qid']} | {title_link} | {r['difficulty']} | {tag_str} | {lang_str} |"
        )

    new_table = TABLE_START + "\n" + "\n".join(table_lines) + "\n" + TABLE_END
    new_content = content[:start] + new_table + content[end + len(TABLE_END):]

    with open(MAIN_README, "w", encoding="utf-8") as f:
        f.write(new_content)


def collect_all_rows() -> List[Dict]:
    """Walk problems/ and build the row list for the main README table."""
    rows = []
    if not os.path.isdir(PROBLEMS_DIR):
        return rows
    for entry in sorted(os.listdir(PROBLEMS_DIR)):
        folder = os.path.join(PROBLEMS_DIR, entry)
        if not os.path.isdir(folder):
            continue
        meta_path = os.path.join(folder, ".meta.json")
        if not os.path.exists(meta_path):
            continue
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        rows.append({
            "qid": meta.get("questionFrontendId", "?"),
            "title": meta.get("title", entry),
            "slug": meta.get("titleSlug", entry),
            "folder": folder,
            "difficulty": meta.get("difficulty", "Unknown"),
            "tags": [t.get("name", "") for t in meta.get("topicTags", []) or []],
            "languages": detect_languages(folder),
        })
    return rows


def save_problem_metadata(folder: str, metadata: Dict) -> None:
    path = os.path.join(folder, ".meta.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, sort_keys=True)
        f.write("\n")


def load_problem_metadata(folder: str) -> Optional[Dict]:
    path = os.path.join(folder, ".meta.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
