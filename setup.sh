#!/bin/bash

# Create symlinks in the root directory for easy access.
#
# NOTE: This script does NOT work on Windows (cmd.exe / native PowerShell).
# Symlinks via `ln -sf` only work in Git Bash / WSL, and even then they often
# need Administrator rights or Developer Mode enabled. If setup.sh fails for
# you, just skip it and run the scripts directly:
#
#   python scripts/sync_submissions.py
#   python scripts/add_solution.py <filename> <slug>
#   python scripts/list_problems.py
#   python scripts/generate_stats.py
#   bash   scripts/open.sh <slug>
#
# Or call them via bash:
#
#   bash scripts/sync.sh
#   bash scripts/add.sh <filename> <slug>
#   bash scripts/list.sh
#   bash scripts/stats.sh

cd "$(dirname "$0")"

# Make scripts executable
chmod +x scripts/*.py
chmod +x scripts/*.sh

# Create symlinks for main commands
ln -sf scripts/sync.sh sync
ln -sf scripts/add.sh add
ln -sf scripts/list.sh list
ln -sf scripts/stats.sh stats
ln -sf scripts/open.sh open

echo "Setup complete. You can now use the following commands:"
echo "  ./sync                       Pull and document accepted submissions from LeetCode"
echo "  ./add <filename> <slug>      Manually add a solution from the workspace folder"
echo "  ./list                       List all solved problems"
echo "  ./stats                      Show statistics about solved problems"
echo "  ./open <slug>                Open a problem in the browser"
echo ""
echo "If symlinks were not created (common on Windows), run the scripts directly:"
echo "  python scripts/sync_submissions.py"
echo "  python scripts/add_solution.py <filename> <slug>"
echo "  python scripts/list_problems.py"
echo "  python scripts/generate_stats.py"
echo "  bash   scripts/open.sh <slug>"
