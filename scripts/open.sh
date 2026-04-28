#!/bin/bash

cd "$(dirname "$0")/.."

if [ $# -lt 1 ]; then
    echo "Usage: ./open <slug>"
    echo "Example: ./open two-sum"
    exit 1
fi

slug="$1"
url="https://leetcode.com/problems/$slug/"

if command -v xdg-open &> /dev/null; then
    xdg-open "$url"     # Linux
elif command -v open &> /dev/null; then
    open "$url"         # macOS
elif command -v start &> /dev/null; then
    start "$url"        # Windows (Git Bash)
else
    echo "Could not open browser. Visit: $url"
fi
