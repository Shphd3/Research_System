# Continuation Brief: T plus AuxK after engineering Smoke

```text
Workstream:     SAE auxiliary-backbone pilot    Problem key: none confirmed
Role:           PRIMARY
Record:         .research/memory/conversations/0914-training-excution/
Continues from: none
Supersedes:     none
Updated at:     2026-09-14T13:26:49Z             Status: CURRENT
Non-canonical:  points at canonical sources; owns no claim, approval, verdict,
                or next decision.
```

## A. Environment roots

| Root | Path | Readable here? |
| --- | --- | --- |
| Repository root | `/data/250010109/Research_System` | yes |
| Execution workspace | `/data/250010109/MoE_Router` | yes |
| Smoke evidence | `/data/250010109/MoE_Router/experiments/20260914_sae_aux_backbone_t_auxk` | yes |

## B. Read list — in order

| # | Path | Answers which question | Required? |
| --- | --- | --- | --- |
| 1 | `daily_research_reports/0914/sae_aux_backbone_pilot_decision/protocol.md` | What remains draft and scientifically unresolved? | yes |
| 2 | `/data/250010109/MoE_Router/experiments/20260914_sae_aux_backbone_t_auxk/README.md` | What was implemented and what is the comparison boundary? | yes |
| 3 | sibling `audit/source_identity.json` and `audit/config_diff.json` | Which frozen 0912 source and fields changed? | yes |
| 4 | run `smoke_receipt.json`, `terminal_receipt.json`, `resolved_config.json` | Did the authorized Smoke pass under the resolved contract? | yes |
| 5 | run `checks/gradient_contract.json` and `resume_check.json` | Are gradient ownership and replay qualified? | yes |
| 6 | current Focus and Anchor | Which question owns a full run? They do not yet exist for this design; stop before scientific execution. | yes for any development/full run |

## C. Authority and boundaries

- Approved scope and its owner: the researcher's 2026-09-14 instruction authorized the completed four-H100 engineering Smoke; the run-local scope and receipts record it.
- NOT approved — do not start: development/full T training, a new C, three seeds, new data acquisition, or any scientific state transition.
- May not claim: AuxK revived features; the sampled-input gradient improved representations; old C is a strict single-variable control; or the scientific hypothesis is supported.
- Human-owned decisions still open: stable problem key/owner, combined-intervention versus AuxK-matched comparison, natural panel freeze, acceptable LM cost, and next budget.

## E. Action list

| # | Action (one verb) | Verify | If pass | If fail |
| --- | --- | --- | --- | --- |
| 1 | Inspect | terminal receipt exit 0, Smoke receipt PASS, 100 metrics rows, no failure artifact | Treat engineering Smoke as complete | Report the exact failed gate; do not resubmit |
| 2 | Ask | researcher chooses estimand and confirms canonical owner/key/budget | Revise one Protocol before any full run | Keep execution blocked |
| 3 | Freeze | panel, loss schedule, coefficients and approved training ceiling in the owning Protocol | Prepare a new explicit full launcher | Stop on any unresolved field |

`STARTING`, a job ID, or a checkpoint file alone is not a completion signal;
the terminal and Smoke receipts are.

## F. Current state

- Done: isolated implementation, source/config audit, CPU checks, four-H100 Smoke job `pt-k27u0fea`, checkpoint replay, TensorBoard and terminal receipts.
- Pending: scientific ownership/design and any training beyond Smoke.
- Material boundary: AuxK was force-exercised but not naturally eligible within 3.2768M sampled positions; existing C has no AuxK.
- Already rejected: reusing the old 50B launcher, changing old C artifacts, treating the old C as a strict detach-only control, or interpreting engineering PASS scientifically.
- Live concurrency risk: none in this run root; the job is terminal `SUCCEEDED`.

## G. Completion contract

- Deliverables: one researcher-approved canonical Protocol and panel manifest before training.
- Done when: owner/key, estimand, data, budget and execution scope are explicit and internally consistent.
- Stop and ask the researcher when: choosing combined intervention versus a fresh matched control, or setting the next compute budget.

## H. Reusable assets — reuse before rewriting

| Asset | Path | Reuse for | Verified? |
| --- | --- | --- | --- |
| T + AuxK code and Smoke runner | `/data/250010109/MoE_Router/experiments/20260914_sae_aux_backbone_t_auxk` | Any approved continuation after requalification | yes, Smoke source hashes are run-local |
| Exact 0912 submitted source | `/data/250010109/MoE_Router/experiments/20260912_dense_sae_pretraining/continuation_sources/formal50b_submitted_20260912T1130Z` | Baseline identity and unchanged infrastructure | yes |
| Frozen DCLM view | `/data/250010109/training_data_views/dclm_pair_v1/manifest.json` | Matched training input | yes, hash in resolved config |
| Gradient/replay checks | new workspace `checks/` and run-local `checks/` | Re-run before any changed source | yes |
| Execution templates | `docs/execution_envelope.md`, `templates/execution/acp_submit_template.sh` | Resolve future approved jobs | yes |
