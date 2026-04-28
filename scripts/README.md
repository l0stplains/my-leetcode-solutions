# LeetCode Solutions Repository Scripts

This folder contains the scripts that power the LeetCode solutions repository. There are two main flows:

1. **Automated sync** (`./sync`): pull every accepted submission from your LeetCode account.
2. **Manual add** (`./add`): drop a polished solution from `workspace/` into the repo.

## Setup

1. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make scripts executable and create the `./sync`, `./add`, etc. command shortcuts:
   ```bash
   ./setup.sh
   ```

   **Note:** `setup.sh` only works in environments that support symlinks via `ln -sf` (Linux, macOS, Git Bash with Developer Mode, WSL). On Windows it usually fails silently. If it does, just call the scripts directly. See "Running on Windows" below.

3. **Provide LeetCode cookies** so the sync script can authenticate. Pick one:
   - Create a file `.leetcode_cookies` in the repo root containing the cookie header. (Recommended; gitignored.)
   - Set the environment variable: `export LEETCODE_COOKIES="csrftoken=...; LEETCODE_SESSION=..."`
   - Pass `--cookies "..."` directly to `./sync`.
   - If none is set, you'll be prompted interactively.

   **How to get cookies:**
   1. Log in to [leetcode.com](https://leetcode.com/) in your browser.
   2. Open DevTools and go to the Network tab.
   3. Click any request to `leetcode.com`.
   4. In *Request Headers*, copy the entire `cookie` header value.
   5. Paste it into `.leetcode_cookies`.

## Running on Windows

`setup.sh` uses `ln -sf` which is unreliable on Windows. If the `./sync`, `./add`, etc. shortcuts don't get created, run the scripts directly from the repo root:

```bash
python scripts/sync_submissions.py
python scripts/add_solution.py <filename> <slug>
python scripts/list_problems.py
python scripts/generate_stats.py
bash   scripts/open.sh <slug>
```

The `.sh` wrappers in `scripts/` only forward arguments to the corresponding Python file, so calling Python directly is equivalent.

## Commands

### Sync: `./sync`

The main command. Pulls accepted submissions from LeetCode and writes them into `problems/`.

```bash
./sync                           # Incremental: only fetch submissions newer than last sync
./sync --full                    # Re-scan all submissions
./sync --refresh-metadata        # Re-fetch problem metadata for every touched problem
./sync --language python3,cpp    # Only sync these languages
./sync --dry-run                 # Preview without writing files
./sync -v                        # Verbose logging
```

**What it does:**
1. Walks your LeetCode submissions in reverse chronological order.
2. Stops when it hits a submission older than the last sync (incremental mode).
3. Keeps only `Accepted` submissions.
4. Groups by `(problem, language)` and keeps the **latest** accepted attempt per group.
5. Writes the latest code as the canonical solution file (`problems/<id>-<slug>/<slug>.<ext>`).
6. Logs every accepted attempt's metadata (date, runtime, memory) into the per-problem `.submissions.json` and the README's *Accepted Submission History* table.
7. Fetches problem metadata via GraphQL (title, difficulty, tags, stats; **never the problem statement**).
8. Regenerates per-problem READMEs and the main solutions table.
9. Updates `.leetcode_sync.json` so the next run is incremental.

### Add: `./add <filename> <slug>`

Manually copy a solution from the `workspace/` folder into the repo. Useful when:
- You want to commit a hand-cleaned version of a solution.
- You solved the problem somewhere else and want it documented.
- The sync API is being flaky.

```bash
./add solution.py two-sum
./add solution.cpp two-sum --no-network    # Skip metadata fetch
./add solution.kt two-sum --lang kotlin    # Override language
```

### List: `./list`

Print a table of every solved problem (sorted by difficulty then problem #).

### Stats: `./stats`

Show counts by difficulty, language, and tag.

### Open: `./open <slug>`

Open the LeetCode problem page in your default browser.
```bash
./open two-sum
```

## Workflow

**Typical workflow (sync-first):**
1. Solve and submit problems on LeetCode as usual.
2. Periodically run `./sync` to mirror your accepted submissions.
3. Commit the changes:
   ```bash
   git add problems/ README.md
   git commit -m "Sync LeetCode solutions"
   git push
   ```

**Manual workflow:**
1. Write a solution in `workspace/`.
2. Run `./add filename.py problem-slug`.
3. Commit.

## Repository layout

```
my-leetcode-solutions/
  README.md                    Auto-generated solutions table (between markers)
  requirements.txt             Python deps (requests, tabulate)
  setup.sh                     Creates ./sync, ./add, ./list, ./open, ./stats (Unix-like only)
  .gitignore
  .leetcode_cookies            YOUR cookies (gitignored, you create this)
  .leetcode_sync.json          Incremental sync marker (gitignored)
  problems/
    <id>-<slug>/
      README.md                Per-problem (regenerated on sync)
      .meta.json               Cached LeetCode metadata
      .submissions.json        Accepted submission history (committed)
      <slug>.<ext>             Latest accepted solution per language
  scripts/
    README.md                  This file
    leetcode_api.py            Shared LeetCode REST + GraphQL client
    repo_io.py                 Shared on-disk read/write helpers
    sync_submissions.py
    sync.sh
    add_solution.py
    add.sh
    list_problems.py
    list.sh
    generate_stats.py
    stats.sh
    open.sh
  workspace/
    README.md
```

## Why we don't store problem statements

LeetCode problem statements are copyrighted by LeetCode LLC. Per the [leetcode-export project's disclaimer](../../leetcode-export/README.md#disclaimer), uploading them to GitHub can result in a DMCA takedown. We deliberately **omit problem `content`** from the GraphQL query and only store:

- Problem ID, title, slug
- Difficulty, tags
- Public stats (acceptance rate, totals)
- A link to the original problem
- Your own solution code

If you want a fully local archive that includes problem statements (kept off GitHub), use the [leetcode-export](../../leetcode-export) tool directly.

## Design notes

### Latest vs. all submissions

The sync stores **only the latest accepted submission per language** as the canonical solution file, but **logs every accepted attempt's metadata** in the per-problem README and `.submissions.json`. This keeps the repo readable while preserving a sense of progress (e.g., went from 200ms to 60ms over five attempts).

If you'd rather keep every accepted code blob, the trade-off is noise: it's common to submit the same solution many times for testing, or with one-line tweaks. You can adapt `sync_submissions.py` (`group_latest_by_lang`) to write all of them if you want.

### Metadata caching

`.meta.json` per problem caches the GraphQL response so re-syncs don't re-hit the API for already-known problems. Use `./sync --refresh-metadata` to force a refresh.

## Troubleshooting

**"Cookies are not valid or expired"**: cookies typically last about 30 days. Get a fresh `cookie` header from your browser's Network tab and update `.leetcode_cookies`.

**Sync is slow**: that's intentional. There's a built-in 2s delay between paginated requests to be polite to the LeetCode API. The first full sync of a large account can take several minutes.

**`tabulate` not found**: `pip install -r requirements.txt`. Sync and add do not require `tabulate`; only list and stats do.

**Windows symlinks**: `setup.sh` uses `ln -sf`, which is unreliable on Windows. Skip it and call `python scripts/sync_submissions.py` (etc.) directly.
