#!/usr/bin/env python3
"""List all solved LeetCode problems in a tabular format."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from tabulate import tabulate
except ImportError:
    print(
        "ERROR: 'tabulate' is not installed. Run: pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)

from leetcode_api import lang_display
from repo_io import DIFFICULTY_RANK, collect_all_rows


def main():
    rows = collect_all_rows()
    if not rows:
        print("No problems found. Run ./sync to import your LeetCode submissions.")
        return

    rows.sort(key=lambda r: (
        DIFFICULTY_RANK.get(r["difficulty"], 99),
        int(r["qid"]) if str(r["qid"]).isdigit() else float("inf"),
    ))

    table = [
        [
            r["qid"],
            r["title"],
            r["difficulty"],
            ", ".join(r["tags"][:3]) + ("..." if len(r["tags"]) > 3 else ""),
            ", ".join(lang_display(l) for l in r["languages"]),
        ]
        for r in rows
    ]
    headers = ["#", "Title", "Difficulty", "Tags", "Languages"]
    print(tabulate(table, headers=headers, tablefmt="grid"))
    print(f"\nTotal problems solved: {len(rows)}")


if __name__ == "__main__":
    main()
