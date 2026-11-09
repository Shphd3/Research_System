# Git payload cleanup, 2026-09-24

The researcher requested faster routine Git commits and a source-and-record-only from-attention project. The exact path and byte inventory of this root cleanup is in [`git_payload_cleanup_20260924.txt`](archive/process_records/git_payload_cleanup_20260924.txt). The matching project inventory is in `Projects/from-attention-to-search/docs/git_payload_cleanup_20260924.txt`.

| Repository | Generated files removed from the Git index | Bytes removed from future snapshots | Kept locally |
|---|---:|---:|---|
| Research_System | 1,236 | 230,440,986 (219.77 MiB) | Yes |
| from-attention-to-search | 3,954 | 525,443,872 (501.10 MiB) | Yes |

These are index removals; the files are still available in this checkout. The four previously approved duplicate CSV copies were physically deleted separately and documented in [`storage_cleanup_20260924.md`](archive/process_records/storage_cleanup_20260924.md). The generated root `sync/S000_current_specialization` publication was also retired to four navigation files; canonical project records remain in the independent project repository.

The root repository now tracks Markdown, scripts, configs, and process records while excluding generated daily-report tables, figures, result JSON, logs, and fonts. The project repository tracks scripts, configs, Anchors, Protocols, Summaries, and Detailed records while excluding generated tables, figures, result JSON, logs, caches, and run notes. `.gitignore` prevents ordinary future adds; `python tools/check_git_payload.py` and the project `scripts/check_git_payload.py` detect force-added payloads. Neither checker judges scientific validity.

**Portability boundary:** a fresh clone will not contain the removed generated figures and tables. The owning Detailed record must identify the execution location and digest for decision-bearing outputs; explicitly requested reading packages can copy selected artifacts. Existing Git history still contains older payloads; ordinary commits do not erase historical packfiles. A history rewrite would change commit identities and is outside this cleanup.

The first commit that records thousands of index removals is a one-time large deletion. Routine later commits benefit from the smaller tracked set. The two repositories are committed separately so the project retains its independent history.
