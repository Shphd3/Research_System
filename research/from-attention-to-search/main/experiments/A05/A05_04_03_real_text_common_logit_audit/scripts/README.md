# Scripts For Real-Text Common-Logit Audit

These scripts support the DCLM real-text random-init MoE common-logit audit
drafted on 2026-06-11.

## `real_text_common_logit_preflight.py`

Purpose: check data/source/model/manifest assumptions before a full run.

Example:

```bash
python scripts/real_text_common_logit_preflight.py --write-snapshot
```

This script does not train or run the full audit. It writes a lightweight
preflight snapshot under:

```text
source_list/real_text_common_logit_audit_v5_preflight/
```

Use it again after the unresolved protocol questions are fixed.
