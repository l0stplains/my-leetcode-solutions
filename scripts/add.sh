#!/bin/bash

# Change to repository root directory
cd "$(dirname "$0")/.."

if [ "$1" = "-h" ] || [ "$1" = "--help" ] || [ $# -lt 2 ]; then
    echo "Usage: ./add <filename> <slug>"
    echo "  <filename>   - File in the workspace/ directory (e.g. solution.py)"
    echo "  <slug>       - LeetCode problem slug from the URL (e.g. two-sum)"
    echo ""
    echo "Optional flags (passed through to scripts/add_solution.py):"
    echo "  --no-network         Skip metadata fetch (use cached if available)"
    echo "  --cookies COOKIES    Override cookie source"
    echo "  --lang LANG          Override language detection"
    echo ""
    echo "Other commands:"
    echo "  ./sync               Pull all accepted submissions from LeetCode"
    echo "  ./list               List all solved problems"
    echo "  ./stats              Show statistics about solved problems"
    echo "  ./open <slug>        Open problem in browser"
    exit 0
fi

python3 scripts/add_solution.py "$@"
