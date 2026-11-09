# H0522 Router Factor Audit Seq32

Linked hypothesis:

The legacy purpose card was removed; this experiment record is the surviving
source.

Status:

```text
completed on ACP 4-card job pt-xceqs84c
```

This experiment executes Stage 1-5 of the `seq_len=32` router factor audit.

Main result:

```text
Stage 1/2: source-position and token-id explain the existing H0521b router
better than rule/class.

Stage 5: in the disentangled synthetic task, rule/function does not stably beat
identity; target/second-token shortcut dominates routing.
```

Archived implementation:

```text
scripts/run_h0522_router_factor_audit_seq32.py
config/h0522_router_factor_audit_seq32.json
```
