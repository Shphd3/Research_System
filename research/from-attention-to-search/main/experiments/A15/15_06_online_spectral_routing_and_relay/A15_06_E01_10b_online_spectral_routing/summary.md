---
experiment_id: A15_06_E01_10b_online_spectral_routing
legacy_experiment_id: A15_00_E01_10b_five_arm_training
status: complete
scientific_verdict: does_not_support_relay_hmt
last_updated: 2026-08-03
---

# Final Result Summary

## Direct answer

The registered experiment does **not** support Relay-HMT.  At 10B tokens,
Relay-HMT was decisively worse than both Local-HMT and Centered-Full in each
seed, and it did not reproducibly beat the matched Relay-Random control.

Local-HMT had the lowest endpoint point estimate in both seeds, but its paired
advantage over Centered-Full was decisive only in seed 17.  The strict
two-seed criterion therefore does not establish Local-HMT either.  Centering
was the only large, reproducible improvement: Centered-Full beat Vanilla-Full
by 0.113 and 0.128 nat/token.

## Registered endpoint evidence

| Arm | Seed 17 NLL | Seed 29 NLL |
|---|---:|---:|
| Local-HMT | **3.59874** | **3.60203** |
| Centered-Full | 3.60384 | 3.60259 |
| Relay-HMT | 3.61309 | 3.60892 |
| Relay-Random | 3.61576 | 3.60866 |
| Vanilla-Full | 3.71639 | 3.73053 |

Paired differences are \(L_A-L_B\) in nat/token; negative favors A.

| Comparison | Seed 17, 95% paired CI | Seed 29, 95% paired CI | Verdict |
|---|---:|---:|---|
| Centered − Vanilla | −0.11254 [−0.11445, −0.11074] | −0.12795 [−0.13003, −0.12596] | centering pass |
| Local − Centered | −0.00510 [−0.00654, −0.00371] | −0.00056 [−0.00211, +0.00098] | not supported across seeds |
| Relay-HMT − Local | +0.01436 [+0.01280, +0.01590] | +0.00689 [+0.00535, +0.00846] | H2 fail |
| Relay-HMT − Centered | +0.00925 [+0.00769, +0.01080] | +0.00633 [+0.00476, +0.00791] | Relay architecture fail |
| Relay-HMT − Relay-Random | −0.00266 [−0.00420, −0.00115] | +0.00026 [−0.00123, +0.00175] | H3 fail |

![Five-arm NLL trajectory](figures/figure1_five_arm_nll_trajectory.png)

![Registered endpoint contrasts](figures/figure2_endpoint_paired_delta_nll.png)

## Online updater result

The online updater had a distinct engineering success and scientific failure:

- At 10B, HMT deployed/target overlap was about 0.756--0.762 for \(U_{64}\)
  and 0.854--0.866 for \(U_{320}\), versus 0.157--0.189 and 0.547--0.591 if
  the step-0 subspace was never updated.
- The remaining RMS principal-angle lag was about 30--31 degrees for \(U_{64}\)
  and 23--24 degrees for \(U_{320}\), so tracking was useful but not exact.
- Across all registered refresh events, the actual maximum high-confidence
  route flip was zero, all accepted updates had nonzero gamma, and all
  continuity guards passed.
- Hard replacement at the 10B checkpoint would flip roughly 25--38% of
  high-confidence tokens for Local/Relay-HMT, demonstrating that smoothing
  prevented a large discontinuity.
- Refresh-event loss changes were mixed around zero and did not support a
  systematic NLL jump at statistics updates.

Thus H4 passes: EMA plus Grassmann backtracking solved the continuity problem.
This did not make Relay-HMT a better language model.

![Online tracking and continuity](figures/figure6_online_tracking_accuracy_continuity.png)

## Mechanism reading

- Vanilla-Full developed severe deep-layer routing collapse and was worst in
  NLL. Centering prevented collapse and produced the largest quality gain.
- Local-HMT used experts most broadly and had somewhat lower norm-weighted
  within-expert negative-gradient-pair fractions than the Relay arms.
- Local-HMT did not reproducibly improve forced-expert choice regret over
  Centered-Full, so the expert-compatibility mechanism is not closed.
- Relay-HMT and Relay-Random had higher choice regret and output redundancy,
  consistent with their lack of endpoint benefit but not a unique causal
  explanation.

## Evidence completeness and boundary

All 10 jobs reached 10B with zero retries.  The record contains 110/110 routing
snapshots, 40/40 expert-function snapshots, 192 refresh events, all terminal
per-document NLL arrays, and complete TensorBoard/JSONL telemetry.  The result
is therefore a valid negative verdict, not insufficient evidence.

The experiment cannot establish universal H/M/T semantics, transfer to larger
models, or covariance identity as the cause of Local-HMT's weak point-estimate
advantage.  There was no Local-Random arm, and the Relay-Random target was more
difficult to track because it mixed the full, tail-sensitive eigenbasis.

## One next decision

Before scaling or extending Relay-HMT, decide whether to run a
target-motion-and-tracking-matched Local-Random control against Local-HMT and
Centered-Full.  That is the minimal test of whether the remaining Local-HMT
signal is covariance-specific or merely a dynamic low-dimensional
regularization effect.

Full Chinese reading surface:
[2026-08-03 training report](../../../../../../../daily_research_reports/backup/2026/08/0803/online_spectral_router_10b_training_report/report.md).

Complete evidence and worker artifact map: [detailed.md](detailed.md).
