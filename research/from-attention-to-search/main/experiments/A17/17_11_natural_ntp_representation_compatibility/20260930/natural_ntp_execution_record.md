# Natural NTP compatibility: execution record

Protocol: [registered design](protocol.md) · [中文](natural_ntp_execution_record_cn.md)

Status at 2026-09-29 18:00 UTC: engineering Smoke passed; Full job submitted and observed running. Scientific result and Focus judgment remain **Unknown**.

| Attempt | Job ID | Factual state | Durable evidence |
|---|---|---|---|
| Smoke 1 | `pt-5k6mv35t` | Failed after four measurement workers passed: CPU RNG state was loaded onto CUDA in predictor resume check. No confirmation data opened. | `/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/smoke_20260929T173730Z/result/failure.json` |
| Smoke 2 | `pt-1lqply7o` | Succeeded; 64 OPS events, 32 pairs, numerical gradient and temporary-update checks, and next-step predictor resume checks passed. | `/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/smoke_20260929T174308Z/result/smoke_receipt.json` |
| Full | `pt-dgpld36j` | Submitted 2026-09-29 17:59:39 UTC, observed `RUNNING` at 18:00:04 UTC; no scientific result yet. | `/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/submit/` and `pod` |

All three submissions used the envelope's `h100-4-reserved` profile and `shphd-lite-0911` image. Smoke 2 measured 50.57 seconds of run time and estimated 0.53 GPU hours for the full event-collection component with a 1.5 factor. This is an engineering estimate, not an observed Full completion time. Full retains the Protocol's 24 GPU-hour aggregate and 50 GiB artifact ceilings; it has a bounded runtime command and stops on failed gates.

The data preparation checked the selected shard and tokenizer hashes, parsed 59,812 source rows, found 47,760 eligible records, and obtained 19,997 duplicate groups from the 20,000 hash-ranked candidate pool. The four prescribed splits were allocated without outcome-based filtering. The data manifest is `/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/data_v1/data_manifest.json`.

The Full job must leave collection, fit, registration, sealed prediction, analysis and verification receipts under `/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/`. A submitted job and a platform `SUCCEEDED` state alone do not establish a scientific result; the durable outputs and Protocol gates determine eligibility. No commit, push or scientific verdict was made in this record.

Startup check at 2026-09-29 18:01 UTC: all 7,232 prescribed events were collected, the OPS numerical-resolution stage reported PASS (`delta_l=6.69e-6`, `delta_k=1.82e-6`), and predictor fitting reached epoch 10 in several geometry runs. Platform state remained `RUNNING`. These are stage progress checks, not a confirmation result; Full completion time is not yet established from the early geometry fits.

## Terminal update — 2026-09-29

The earlier `RUNNING` statements above are time-stamped history. ACP job `pt-dgpld36j` subsequently reached `SUCCEEDED`; its durable pod log and [Full verification receipt](/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/runs/full_20260929T175901Z/result/verification.json) show `COMPLETE_OPERATIONAL` after 210.54 seconds, 4,699,652,035 bytes of output, and the source checkpoint unchanged. All 7,232 events, 34,336 pairs across four splits, and 24 predictor fits completed. The sealed main CONFIRM result is **eligible `NON_SUPPORT`**, not `Unknown`: selected full-reader \(Q=-0.000138\), 95% CI \([-0.002768,0.002294]\), against a registered 0.05 support threshold. The finite-step confirmation is `NOT_RUN_BY_BRIDGE` after DEV calibration failed the resolved-effect guard; all 14 structural readers are `NOT_RUN_BY_GATE`. Researcher interpretation and Focus transition remain `Unknown`.

Read [Summary](summary.md) / [中文摘要](summary_cn.md) first, then [Detailed](detailed.md) / [中文证据记录](detailed_cn.md). [Theoretical-audit handoff](../../../../research_notes/shared_updates/20260930/reviews/natural_ntp_audit_handoff.md) indexes every result and its evidence priority. This terminal update does not revise the frozen Protocol or authorize a follow-on run.
