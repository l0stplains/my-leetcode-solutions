#!/usr/bin/env python3
"""Generate a useful commit message for synced LeetCode changes."""

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple

# Allow running as `python3 scripts/generate_commit_message.py` from the repo root.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from leetcode_api import LANG_DISPLAY_NAME, lang_display, lang_to_ext


DEFAULT_OUTPUT = ".leetcode_commit_message"
IGNORED_PROBLEM_FILES = {"README.md", ".meta.json"}


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout


def parse_status() -> List[Tuple[str, str]]:
    """Return (status, path) entries from the working tree."""
    entries = []
    output = run_git("status", "--porcelain=v1", "--untracked-files=all")
    for line in output.splitlines():
        if len(line) < 4:
            continue
        status = line[:2]
        path = line[3:]
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1]
        entries.append((status, path.strip('"')))
    return entries


def tracked_problem_folders() -> Set[str]:
    folders = set()
    for path in run_git("ls-files", "--", "problems").splitlines():
        parts = path.split("/", 2)
        if len(parts) >= 2:
            folders.add(parts[1])
    return folders


def language_for_path(path: str) -> Optional[str]:
    extension = os.path.splitext(path)[1].lstrip(".").lower()
    if not extension:
        return None
    for language in LANG_DISPLAY_NAME:
        if lang_to_ext(language) == extension:
            return lang_display(language)
    return None


def load_problem(folder_name: str) -> Dict:
    metadata_path = os.path.join("problems", folder_name, ".meta.json")
    metadata: Dict = {}
    if os.path.isfile(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as file:
            metadata = json.load(file)

    fallback_id, _, fallback_slug = folder_name.partition("-")
    return {
        "id": str(metadata.get("questionFrontendId") or fallback_id),
        "title": metadata.get("title") or fallback_slug.replace("-", " ").title(),
    }


def problem_sort_key(problem: Dict) -> Tuple[int, object]:
    try:
        return (0, int(problem["id"]))
    except (TypeError, ValueError):
        return (1, problem["id"])


def pluralize(count: int, singular: str, plural: Optional[str] = None) -> str:
    return singular if count == 1 else (plural or f"{singular}s")


def generate_commit_message() -> Optional[str]:
    """Build a Conventional Commit message from current solution changes."""
    status_entries = parse_status()
    tracked_folders = tracked_problem_folders()
    changed_by_folder: Dict[str, List[str]] = defaultdict(list)
    docs_changed = False

    for _, path in status_entries:
        if path == "README.md":
            docs_changed = True
            continue

        parts = path.split("/", 2)
        if len(parts) < 3 or parts[0] != "problems":
            continue

        folder_name, filename = parts[1], parts[2]
        changed_by_folder[folder_name].append(filename)
        if os.path.basename(filename) in IGNORED_PROBLEM_FILES:
            docs_changed = True

    problems = []
    for folder_name, filenames in changed_by_folder.items():
        is_new = folder_name not in tracked_folders
        meaningful_files = [
            name
            for name in filenames
            if os.path.basename(name) not in IGNORED_PROBLEM_FILES
        ]
        if not is_new and not meaningful_files:
            continue

        problem = load_problem(folder_name)
        problem["action"] = "Add" if is_new else "Update"
        problem["languages"] = sorted(
            {
                language
                for name in meaningful_files
                if (language := language_for_path(name))
            }
        )
        problems.append(problem)

    problems.sort(key=problem_sort_key)
    added = sum(problem["action"] == "Add" for problem in problems)
    updated = len(problems) - added

    if added and updated:
        title = (
            f"feat(solutions): sync {len(problems)} LeetCode "
            f"{pluralize(len(problems), 'solution')}"
        )
    elif added:
        title = (
            f"feat(solutions): add {added} LeetCode "
            f"{pluralize(added, 'solution')}"
        )
    elif updated:
        title = (
            f"chore(solutions): update {updated} LeetCode "
            f"{pluralize(updated, 'solution')}"
        )
    elif docs_changed:
        return "docs(solutions): refresh generated solution metadata\n"
    else:
        return None

    body = []
    for problem in problems:
        languages = ""
        if problem["languages"]:
            languages = f" ({', '.join(problem['languages'])})"
        body.append(
            f"- {problem['action']} #{problem['id']} {problem['title']}{languages}"
        )

    if docs_changed:
        body.append("- Refresh generated problem documentation and solution index")

    return f"{title}\n\n" + "\n".join(body) + "\n"


def write_commit_message(
    message: Optional[str] = None, output_path: str = DEFAULT_OUTPUT
) -> Optional[str]:
    message = message if message is not None else generate_commit_message()
    if not message:
        return None
    with open(output_path, "w", encoding="utf-8", newline="\n") as file:
        file.write(message)
    return output_path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a commit message from synced LeetCode changes."
    )
    parser.add_argument(
        "--write",
        nargs="?",
        const=DEFAULT_OUTPUT,
        metavar="PATH",
        help=f"Write the message to PATH (default: {DEFAULT_OUTPUT}).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        message = generate_commit_message()
    except subprocess.CalledProcessError as error:
        detail = error.stderr.strip() or str(error)
        print(f"ERROR: Could not inspect git changes: {detail}", file=sys.stderr)
        sys.exit(1)

    if not message:
        print("No LeetCode solution changes found.", file=sys.stderr)
        sys.exit(1)

    if args.write:
        write_commit_message(message, args.write)
        print(f"Commit message written to {args.write}")
    else:
        print(message, end="")


if __name__ == "__main__":
    main()
