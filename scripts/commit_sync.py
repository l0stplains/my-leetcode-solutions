#!/usr/bin/env python3
"""Commit exactly the paths recorded by the latest LeetCode sync."""

import argparse
import os
import subprocess
import sys
from typing import Iterable, List


MESSAGE_FILE = ".leetcode_commit_message"
PATHS_FILE = ".leetcode_sync_paths"


def validate_sync_path(path: str) -> str:
    normalized = os.path.normpath(path)
    if (
        os.path.isabs(path)
        or normalized != path
        or normalized == ".."
        or normalized.startswith(f"..{os.sep}")
    ):
        raise ValueError(f"Unsafe sync path: {path}")
    if normalized != "README.md" and not normalized.startswith(f"problems{os.sep}"):
        raise ValueError(f"Path is outside the sync scope: {path}")
    return normalized


def write_sync_paths(paths: Iterable[str], output_path: str = PATHS_FILE) -> str:
    validated = {validate_sync_path(path) for path in paths}
    ordered = sorted(validated, key=lambda path: (path != "README.md", path))
    with open(output_path, "w", encoding="utf-8", newline="\n") as file:
        for path in ordered:
            file.write(f"{path}\n")
    return output_path


def load_sync_paths(input_path: str = PATHS_FILE) -> List[str]:
    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            f"{input_path} was not found. Run the sync command first."
        )
    with open(input_path, "r", encoding="utf-8") as file:
        paths = [line.strip() for line in file if line.strip()]
    if not paths:
        raise ValueError(f"{input_path} does not contain any paths.")
    return [validate_sync_path(path) for path in paths]


def is_in_scope(path: str, scopes: Iterable[str]) -> bool:
    return any(path == scope or path.startswith(f"{scope}{os.sep}") for scope in scopes)


def run(*args: str, capture_output: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        list(args),
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture_output else None,
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Stage and commit exactly the files recorded by the latest sync."
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push the commit using the branch's configured upstream.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        paths = load_sync_paths()
        if not os.path.isfile(MESSAGE_FILE):
            raise FileNotFoundError(
                f"{MESSAGE_FILE} was not found. Run the sync command first."
            )

        run("git", "add", "--", *paths)

        staged_output = run(
            "git", "diff", "--cached", "--name-only", capture_output=True
        ).stdout
        staged_paths = [path for path in staged_output.splitlines() if path]
        unrelated = [
            path for path in staged_paths if not is_in_scope(path, paths)
        ]
        if unrelated:
            print(
                "ERROR: Refusing to commit because unrelated files were already staged:",
                file=sys.stderr,
            )
            for path in unrelated:
                print(f"  {path}", file=sys.stderr)
            print("Unstage them, then run this command again.", file=sys.stderr)
            sys.exit(1)
        if not staged_paths:
            print("No synced changes to commit.")
            return

        run("git", "commit", "-F", MESSAGE_FILE)
        if args.push:
            run("git", "push")
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
