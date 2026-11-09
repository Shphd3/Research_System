# Implementation correction ledger

2026-11-03 UTC: select.py completed and saved selection.json and candidates_frozen.json before its final console summary failed to JSON-serialize numpy int64. Convert console-only summary IDs to Python int. Selection and gate hashes unchanged; no reselection or replay. No heldout responses were available when this occurred. Scientific protocol, thresholds and sample identities unchanged. Exact UTC in candidates_frozen.json.

2026-11-03T17:12:09.898843+00:00 — Engineering-only NPZ loading repair: old code decompressed a whole compressed matrix once per row; load each field once before row scatter. Interrupted only this task-owned CPU analysis process after exact command identity check. No scientific output tables had been written; raw responses, selection and protocol unchanged. Partial sparse export recomputes identical values. No metric/threshold change.
