# Workspace

Temporary work area for solutions you want to add manually (the contents of this folder are gitignored except this README).

## Two workflows

### 1. Sync from LeetCode (recommended)

Most of the time you don't need this folder. Just solve problems on LeetCode and run:

```bash
./sync
```

That pulls every accepted submission into `problems/` automatically.

### 2. Manual add

When you want to commit a hand-cleaned or offline solution:

1. Drop the file in `workspace/`, e.g., `workspace/two-sum.py`.
2. Run:
   ```bash
   ./add two-sum.py two-sum
   ```
   - First arg: filename inside `workspace/`.
   - Second arg: the LeetCode problem slug (from the URL: `leetcode.com/problems/<slug>/`).
3. The script copies the file into `problems/<id>-<slug>/<slug>.<ext>`, fetches metadata, and updates the main README.

### Optional flags

```bash
./add solution.cpp two-sum --no-network    # Don't fetch metadata (use cached)
./add solution.kt two-sum --lang kotlin    # Force a specific language
./add solution.py two-sum --cookies "..."  # Override cookie source
```

## Other commands

```bash
./sync                  # Pull all accepted submissions from LeetCode
./list                  # Tabular list of solved problems
./stats                 # Difficulty / language / tag breakdown
./open <slug>           # Open the problem page in your browser
```

## Notes

- The workspace folder is gitignored except for this README.
- Files added through `./add` are renamed to `<slug>.<ext>` for consistency.
- See [scripts/README.md](../scripts/README.md) for full documentation.
