# Protocol: A07_02 Nested Tail Common-Subspace Control

## 0. Approval Snapshot

Approval status: user requested immediate sequential protocols and experiments on 2026-06-28.

Purpose: conditional on A07_01, test whether suppressing the common-subspace component of active updates reduces rare nested tail loss.

Primary anchor: `../../../problem_anchors/07_features_overlap/07_02_common_controlled_rare_interference_anchor.md`

Anchor decision question: conditional on A07_01 passing, does common-subspace update control reduce nested tail loss while preserving common accuracy?

Anchor physical prior tested: harmful tail interference is update-space concentration inside the frozen common projector \(P_C\).

Anchor core model term tested: \(\alpha_{\mathrm{tail}}\) and \(\Delta L_{\mathrm{tail}}\).

Anchor falsifier: no tail loss improvement, common loss regression, or no reduction in \(\alpha_{\mathrm{tail}}\).

Experiment role: mechanism-aware method test after a reproduction gate.

Primary metric from anchor: \(\Delta L_{\mathrm{tail}}=L_{\mathrm{tail}}(\mathrm{CE})-L_{\mathrm{tail}}(\mathrm{control})\).

Claim boundary from anchor: controlled nested surface only; not full C3S validity or MoE specialization.

Minimal setup: reuse the nested benchmark and frozen \(P_C\) from A07_01; compare CE baseline, confidence-gate-only, subspace-suppression-only, and combined control.

Basic configuration: 8 seeds, matched training budget, same initialization family, same data distribution.

Conditions to run: `ce_adamw`, `confidence_gate_only`, `subspace_suppression_only`, `combined_gate_and_suppression`.

Pass: combined control improves tail loss, preserves common loss, and lowers \(\alpha_{\mathrm{tail}}\) beyond confidence-gate-only.

Fail: tail loss does not improve, common loss regresses, or \(\alpha_{\mathrm{tail}}\) does not decrease.

Insufficient: A07_01 gate fails, frozen \(P_C\) is unstable, or control conditions are not matched.

Cannot claim: full C3S-AdamW, deployable optimizer, real-DCLM transfer, or expert utility.

Approval decision: run only after A07_01 reports a usable common projector; if A07_01 is weak, record A07_02 as conditional/diagnostic.

## 1. Anchor Alignment

Decision question: does controlling actual updates away from \(P_C\) help tail learning?

Physical prior tested: frequent common backbone can monopolize tail updates.

Core model term tested: \(\alpha_{\mathrm{tail}}=\|P_Cu_{\mathrm{tail}}\|^2/(\|u_{\mathrm{tail}}\|^2+\epsilon)\).

Falsifier: loss or update projection does not move as predicted.

Claim boundary: controlled optimizer-geometry evidence only.

## 2. Tested Hypothesis

If tail learning is harmed by update concentration in \(P_C\), then update suppression should reduce \(\alpha_{\mathrm{tail}}\) and improve tail loss without erasing the common parent.

## 3. Rival Explanations

1. Confidence capping alone explains improvement.
2. Suppression only regularizes update norm, not common-subspace interference.
3. Tail loss is limited by data or capacity, not common-subspace absorption.
4. Common loss improves or worsens for unrelated optimization reasons.

## 4. Data / Model / Algorithm / Objective

Data/model: same nested benchmark and MLP as A07_01.

Algorithm: train to warmup, freeze \(P_C\), continue with matched variants. Suppression is applied to the selected output matrix gradient/update along the input-side common projector.

Objective: CE with optional confidence gate for solved common examples.

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CE/AdamW | baseline | standard training | primary comparison | baseline | control beats it | control fails | missing | `tables/a07_02_summary.csv` |
| Confidence gate only | capping rival | common gradient reduction | separates capping from projection | guard | combined adds beyond it | same as combined | unmatched | `figures/a07_02_control_results.png` |
| Suppression only | subspace target | \(\alpha_{\mathrm{tail}}\) | isolates projection effect | secondary | lowers \(\alpha\) | no movement | bad \(P_C\) | `tables/a07_02_summary.csv` |
| Combined control | full control | \(\Delta L_{\mathrm{tail}}\) | primary method | primary | tail loss improves and common stable | loss guard fails | A07_01 failed | `figures/a07_02_control_results.png` |

Seeds: `20260628-20260635`.

Checkpoints: warmup and final, with update projection sampled during post-warmup training.

## 6. Primary Metric

\[
\Delta L_{\mathrm{tail}}=
L_{\mathrm{tail}}(\mathrm{CE})-
L_{\mathrm{tail}}(\mathrm{combined}).
\]

This metric decides whether the control improves the nested child objective. It must be interpreted with the \(\alpha_{\mathrm{tail}}\) mechanism guard.

## 7. Secondary Metrics

Common loss regression, per-level accuracy, \(\alpha_{\mathrm{tail}}\), update norm, confidence-gate-only tail loss, suppression-only tail loss, and effective rank.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: suppression should lower measured \(\alpha_{\mathrm{tail}}\) if implementation is correct.

Known bad: lowering \(\alpha_{\mathrm{tail}}\) while hurting tail loss means the projected direction was useful reuse, not harmful interference.

Known confusing: tail loss improves but rare accuracy does not, as in A07_06; this supports a loss effect but not clean tail recovery.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Gate import | did A07_01 pass? | A07_01 summary | usable \(P_C\) | `tables/a07_01_summary.csv` | detailed |
| Control implementation | does suppression reduce \(\alpha\)? | update projection | suppression lowers \(\alpha\) | `tables/a07_02_summary.csv` | summary |
| Functional guard | does tail improve without common damage? | loss table | primary pass | `figures/a07_02_control_results.png` | summary |

## 10. Algorithm Specification, If Nontrivial

input: warmup checkpoint, frozen \(P_C\), matched condition config.

parameters: suppression strength \(\rho\), confidence threshold, learning rate, seeds.

steps: train warmup; freeze \(P_C\); continue each condition; project selected update component; record update projection and losses; aggregate.

outputs: `summary.md`, `detailed.md`, tables, and figures.

## 11. Success / Failure / Insufficient Evidence

Success: tail loss improves, common loss is stable, and \(\alpha_{\mathrm{tail}}\) decreases.

Failure: functional or mechanism guard fails.

Insufficient evidence: A07_01 does not establish the projector.

## 12. What This Cannot Claim

This cannot claim real-language transfer, full C3S optimizer validity, or expert specialization.

## 13. Review Notes And Protocol Changes

A07_06 motivates this separation: rare loss can improve while route-level conflict barely moves, so A07_02 must require a mechanism guard.
