# Execution record: NTP statistics and local update structure

Owner: [Protocol](protocol.md). Run approval: researcher2026-09-30 requested initial implementation, Smoke and complete gated Full. Full SUCCEEDED. Scientific judgment: Unknown. Model/SAE updates:0.

## Resolved execution tuple

Default `h100-4-reserved`; ACP; `share-space` / `share-cluster`; one `n6ls.iu.i40.4` node,4 workers,4 H10080GB; Reserved/Normal; image `shphd-lite-0911`, expanded `registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423`; AFS01995892-d478-76d8-aec7-13fd8284477e mounted `/data`; GPU used true. Runtime [/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runtime.sh](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runtime.sh) activates the audited frozen-core dependency layer. Training comparison: NOT_APPLICABLE.

## Attempts and gates

| Stage | Job | Run root | Factual result | Eligibility |
| --- | --- | --- | --- | --- |
| Strict Smoke1 | pt-wd184bbc | smoke_initial | Failed VJP recombination precision | Failed-gate evidence only |
| Strict Smoke2 | pt-gqxil5g2 | smoke_precision | Failed stable versus native VJP precision | Failed-gate evidence only |
| Instrumented diagnosis | pt-xm7fqnf3 | smoke_diagnostic | Runner PASS with diagnostic assertions removed | DEBUG_ONLY, cannot gate Full |
| Qualified strict Smoke | pt-k68kogs3 | smoke_qualified | PASS16 records,256 targets,48 SAE/PCA/random KL direction checks; unchanged state | Eligible numerical qualification |
| Full | pt-z162gb1w | full_initial | COMPLETE; 2048records/32768targets,4096functionalcontexts; primaryINSUFFICIENT | Bounded descriptive/primary evidence |

The qualified Smoke restored all original thresholds. Maximum VJP relative error 3.35012007e-07, below2e-5. Independent nonlinear CPU tests verify unchanged native forward bits; primary CPU tests verify shared-target cancellation and recurring/reversed known contrasts. Calibration:28 cases×5,000 repetitions PASS. Smoke measured conservative Full estimate 927.2s. Full deadline6,600s, within the existing combined retry/Full resource ceiling. No scientific selection changed after Smoke; precision engineering amendment is appended to Protocol before R unsealing.

## Exact entry and scope

Submitted through [repository ACP template](/data/250010109/Research_System/templates/execution/acp_submit_template.sh), which calls the audited `sco_acp_compat.sh`. All submission gates true, including SMOKE_GATE_PASSED=1 for Full. Activation and program:

```bash
source runtime.sh
python scripts/stage.py --mode full --out runs/full_initial --smoke-root runs/smoke_qualified
```

Code root [/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/scripts](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/scripts); [data manifest](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/data/data_manifest.json); [calibration](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/data/calibration.json); [qualified Smoke receipt](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/smoke_qualified/smoke_receipt.json); [ACP receipts](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/acp_receipts); [pod logs](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/acp_receipts/pod); [Full root](/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial). Full registration freezes code/config/source identities and copies the owning Protocol/Anchor. The source exposure audit marks the reused N8 source as historically exposed; this is a descriptive new33B measurement, not untouched prospective confirmation.

## Monitoring and completion

Monitor owner: current Codex chat, primary agent. Verify scheduling/startup, collection receipts, fit-only freeze before R, complete registered analysis, state/checkpoint identities and terminal job status. A success status without complete artifacts is insufficient. Full targets2,048 records/32,768 positions; functional subset256 records/4,096 contexts/32,768 VJPs. TensorBoard NOT_APPLICABLE. No training/checkpoint update, routing experiment, finite-W outcome or long-term sharing comparison.

Terminal verification: ACP pt-z162gb1w SUCCEEDED, start2026-09-30T05:32:22Z / complete05:36:14Z; completion receipt223.0s. [Summary](summary.md), [Detailed](detailed.md), and postrun audit certify required artifacts and explicit insufficient branches. Original code snapshots remain immutable; later domain-ID output repair and figure layout changes are factual amendments. All figures visually inspected.
