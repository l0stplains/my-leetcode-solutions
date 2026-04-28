#!/bin/bash

# Change to repository root directory
cd "$(dirname "$0")/.."

if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    python3 scripts/sync_submissions.py --help
    exit 0
fi

python3 scripts/sync_submissions.py "$@"
