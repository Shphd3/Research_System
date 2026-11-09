# 33B S7 Four-H100 Engineering Smoke — Execution Record

Owner: [Protocol](protocol.md). Scope: four-card H100 reserved engineering smoke on development families 11001–11004 only. Scientific result: `NOT_EVALUATED`.

## Resolved execution tuple

| Field | Value |
|---|---|
| Resource / surface | `h100-4-reserved` / ACP, one node, four independent GPU processes |
| Workspace / cluster / spec | `share-space` / `share-cluster` / `n6ls.iu.i40.4` |
| Quota / priority | reserved / normal |
| Image | `shphd-lite-0911`; expanded URL in each submission receipt |
| Runtime | image Python 3.10, Torch 2.3, CUDA 12.4; no extra activation layer used |
| Mount | envelope default `/data` |
| Fixed model | fresh S7, λ_rec=0.1, exact 33B state SHA256 `c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803` |
| Command | `bash /data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/scripts/run_smoke.sh <run_root>` |
| Training comparison contract | NOT_APPLICABLE: no optimizer step or persistent model update |

## Attempt 1 — preserved engineering failure

- Job `pt-ly724mym`, submitted 2026-09-27 15:23:54 UTC, ACP terminal state `FAILED` by 15:24:37 UTC.
- Run root: `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/smoke_h100_20260927T1524Z`.
- Four GPU workers ran the exact 33B checkpoint and smoke-only calibration. Rank 1 and 2 passed; rank 0 and 3 stopped on the keep/flip logit identity check. The right side had been formed by subtracting FP32 logits before comparison with FP64 cross-entropy differences; the absolute residuals were `1.66893e-6` and `2.86102e-6`, slightly over the mixed absolute/relative gate. This is a numerical implementation error in the smoke check, not a task-interference result.
- Preserved evidence: `registration.json`, four worker logs and receipts/failures, `failed.json`, ACP submission receipt and mounted pod log. No confirmation family was read.

## Attempt 2 — preserved engineering failure

- Job `pt-04q79dqa`, submitted 2026-09-27 15:25:27 UTC, with the same resource, checkpoint and scope. The only code correction converts each FP32 logit to FP64 **before** the analytic margin subtraction, matching the FP64 conditional CE computation. The new source hashes are in its `registration.json`.
- Run root: `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/smoke_h100_20260927T1525Z`.
- Later terminal state: `FAILED`, again 2/4 ranks. FP64 CE used logits from 32-row microbatches, while the identity's right side was recomputed with a full-batch FP32 GEMM. Batch-shape-dependent rounding still exceeded the strict per-row tolerance. This was an audit-path mismatch, not a scientific outcome. Preserved logs and failed receipts remain in the run root.

## Attempt 3 — audited PASS

- Job `pt-jtp7to06`, run root `/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/smoke_h100_20260927T162026Z`.
- Corrected the audit to use the exact two FP32 logits that produced each FP64 cross-entropy value. `complete.json` records `PASS_ENGINEERING_SMOKE`, four workers passed, exact 33B state SHA256 matched, and no confirmation family was read.
- Maximum worker elapsed time was 25.25 s; maximum peak GPU allocation was 1.59 GB. These values qualify the small engineering inputs only, not the 256-context calibration or full-size source/target throughput.
- The common similarity threshold used in Smoke remains a proposed scientific cut-off; Smoke success does not approve it for confirmation-family analysis.

## Smoke contract and boundary

Each rank captures native `c`, attention output `a` and block input `x`; checks the FP32 tail against native logits before and after a reversible W change; contributes four selected natural contexts to a smoke-only basis; then exercises one development family, the revised common-atom distribution rule, source gradient, both step sizes and both B rules. The job checks frozen W restoration and SAE activity buffers. The 16-context basis and small source/target readouts are engineering inputs and cannot be used for the 12-family scientific verdict or a throughput estimate for the formal run.
