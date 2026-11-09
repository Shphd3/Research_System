# Reproduction and scope

Exact inputs/hashes are in evidence/input_manifest.json; source model weights are unnecessary. Python numpy/scipy/pandas/matplotlib are used. Full analysis needs original S11/S13 saved primary/reference assets. A compact packet supplies decisive original CSR/weights/counts and main-table slices; large all-pair tables stay outside with size/hash index.

```bash
OPENBLAS_NUM_THREADS=1 python code/analyze.py
OPENBLAS_NUM_THREADS=1 python code/finish_audit.py
```

The original verification failure is preserved in versions/finish_audit_initial.py and evidence/verification_attempt1.json. The current finish_audit.py correctly keeps jointly undefined empty-subset arms as missing. resume_verification.py records the actual successful continuation; it is optional for an interrupted review and does not repeat analysis.

```bash
OPENBLAS_NUM_THREADS=1 python code/figures.py
OPENBLAS_NUM_THREADS=1 python code/write_reports.py
```

Do not rerun original S11 lock_development/analyze_results or any producer. All new statistics are exploratory on previously exposed splits. New confirmation_protocol.md is NOT RUN; no forward command is provided for uncreated texts. The packet's portable_replay.py only audits included data and never loads neural weights.
