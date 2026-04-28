#!/usr/bin/env python3
"""Print statistics about solved LeetCode problems."""

import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from leetcode_api import lang_display
from repo_io import collect_all_rows


def main():
    rows = collect_all_rows()
    if not rows:
        print("No problems found. Run ./sync to import your LeetCode submissions.")
        return

    print("\n=== LeetCode Solutions Statistics ===\n")
    print(f"Total problems solved: {len(rows)}")

    # By difficulty
    diff_counter = Counter(r["difficulty"] for r in rows)
    print("\nBy Difficulty:")
    for diff in ("Easy", "Medium", "Hard", "Unknown"):
        count = diff_counter.get(diff, 0)
        if count:
            print(f"  {diff}: {count} ({count / len(rows) * 100:.1f}%)")

    # By language
    lang_counter = Counter()
    for r in rows:
        for lang in r["languages"]:
            lang_counter[lang] += 1
    print("\nBy Language:")
    for lang, count in sorted(lang_counter.items(), key=lambda x: x[1], reverse=True):
        print(f"  {lang_display(lang)}: {count}")

    # By tag (top 15)
    tag_counter = Counter()
    for r in rows:
        for tag in r["tags"]:
            tag_counter[tag] += 1
    if tag_counter:
        print("\nTop Tags:")
        for tag, count in tag_counter.most_common(15):
            print(f"  {tag}: {count}")

    # Multi-language problems
    multi = [r for r in rows if len(r["languages"]) > 1]
    if multi:
        print(f"\nProblems solved in multiple languages: {len(multi)}")


if __name__ == "__main__":
    main()
