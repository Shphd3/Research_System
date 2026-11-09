# Protocol: A07_01 Nested Common Backbone Reproduction

## 0. Approval Snapshot

Approval status: user requested immediate sequential protocols and experiments on 2026-06-28.

Purpose: test whether a nested-prefix synthetic benchmark can reproduce the mentor mechanism: frequent parent features form a stable common singular subspace, and singular gain continues to grow after that subspace stabilizes.

Primary anchor: `../../../problem_anchors/07_features_overlap/07_01_common_rare_conflict_metric_audit_anchor.md`

Anchor decision question: does standard CE/AdamW on nested-prefix data produce a stable common singular subspace whose gain continues to grow after common-feature accuracy saturates?

Anchor physical prior tested: high-frequency parent feature \(A\) is learned before rare child features and creates the first high-gain backbone.

Anchor core model term tested: \(P_C(t)\) and \(S_C(t)\).

Anchor falsifier: common accuracy does not precede tail accuracy, \(P_C\) is not stable, or \(S_C\) does not grow after warmup.

Experiment role: root-cause / mechanism reproduction audit.

Primary metric from anchor: stable-late-gain signature: low post-\(T_0\) \(\delta_C(t)\) with positive \(S_C(T)-S_C(T_0)\).

Claim boundary from anchor: passing only supports a controlled nested mechanism surface, not C3S, MoE utility, or real-language semantics.

Minimal setup: train a small nested-prefix classifier with levels \(A\), \(AB\), \(ABC\), and \(ABCD\) under frequency imbalance; save checkpoints; compute the top common singular subspace of the output matrix.

Basic configuration: 8 seeds, CE/AdamW baseline, nested level frequencies decreasing from parent to child, balanced evaluation by level.

Conditions to run: `nested_ce_adamw`, `marker_shortcut_guard`, and `balanced_frequency_guard`.

Pass: \(A\) accuracy saturates before \(ABCD\), post-warmup projector drift is low, common singular energy continues to grow, and shortcut guards do not solve the child task.

Fail: no learning-order separation, no stable common subspace, no late singular-gain growth, or shortcut guards explain the task.

Insufficient: checkpoint spectra are missing, \(P_C\) cannot be estimated, or the data construction does not enforce nested dependence.

Cannot claim: tail interference, C3S benefit, MoE utility, real-DCLM transfer, or semantic experts.

Approval decision: proceed as the first gate because later A07 tests depend on this surface.

## 1. Anchor Alignment

Decision question: can our benchmark reproduce the common-backbone geometry described in the mentor notes?

Physical prior tested: frequency and nesting create a temporal order in which \(A\) stabilizes before tail levels.

Core model term tested: common projector \(P_C\) and common singular energy \(S_C\).

Falsifier: stable-late-gain signature absent.

Claim boundary: controlled synthetic mechanism reproduction only.

## 2. Tested Hypothesis

Standard CE/AdamW will first learn the common parent feature \(A\) and then keep increasing singular gain in the common subspace after \(P_C\) has stabilized.

## 3. Rival Explanations

1. The task is solved by an independent level marker rather than parent reuse.
2. Tail failure is only caused by frequency imbalance or capacity.
3. The top singular subspace reflects label frequency only, not nested structure.
4. Common and tail learn together, so the proposed temporal mechanism is absent.

## 4. Data / Model / Algorithm / Objective

Data: controlled nested-prefix vectors with cumulative parent-child structure. A sample at level \(ABC\) contains the parent component \(A\), the child component \(B\), and the child component \(C\).

Model: small MLP classifier trained with CE/AdamW. The output matrix is the selected block for singular analysis.

Objective: cross-entropy over nested targets. Labels are used for training and audit; level labels are used only for evaluation and grouping.

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nested CE/AdamW | common backbone reproduction | \(P_C\), \(S_C\) | primary mechanism surface | primary | stable-late-gain appears | no signature | spectra missing | `figures/a07_01_backbone_curves.png` |
| Marker shortcut guard | nested validity | independent rare marker rival | protects data interpretation | guard | shortcut probe weak | shortcut solves child | missing probe | `tables/a07_01_summary.csv` |
| Balanced frequency guard | frequency-only rival | frequency imbalance | checks whether the phenomenon needs frequency skew | secondary | skew stronger than balanced | balanced same pattern | missing guard | `tables/a07_01_summary.csv` |

Seeds: `20260628-20260635`.

Checkpoints: fixed interval from step 0 to final, including estimated warmup \(T_0\).

## 6. Primary Metric

Primary metric:

\[
\text{stable-late-gain} =
\mathbf{1}[\delta_C^{\mathrm{post}} \text{ is low}]
\land
\mathbf{1}[S_C(T)-S_C(T_0)>0].
\]

This decides whether the mentor mechanism exists on the synthetic surface before any method or MoE test.

## 7. Secondary Metrics

Secondary metrics: per-level loss/accuracy, \(A\)-before-\(ABCD\) learning gap, top singular energy, top singular vector alignment with known \(A\) direction, shortcut probe accuracy, and balanced-frequency guard metrics.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good: \(A\) should learn earlier than \(ABCD\) on the skewed nested distribution.

Known bad: a marker-only task that solves tail with a child marker should not be treated as nested evidence.

Known confusing: \(P_C\) stable and gain grows, but tail accuracy is already perfect. This reproduces gain growth but does not establish interference.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Data audit | is the task nested? | level probes | shortcut fails | `tables/a07_01_summary.csv` | detailed |
| Training audit | does \(A\) learn first? | per-level curves | \(A\) saturates earlier | `figures/a07_01_backbone_curves.png` | summary |
| SVD audit | does \(P_C\) stabilize and gain grow? | checkpoint matrices | primary metric | `tables/a07_01_checkpoint_trace.csv` | summary |

## 10. Algorithm Specification, If Nontrivial

input: config, seeds, nested data generator, MLP model, checkpoint schedule.

parameters: feature dimension, level frequencies, model width, learning rate, checkpoint interval, top-\(k\) rank.

steps: generate nested data; train baseline; save output matrices; estimate \(P_C\) at warmup; compute projector drift and singular energy; aggregate seed metrics; write figures and tables.

outputs: `summary.md`, `detailed.md`, tables, and figures.

## 11. Success / Failure / Insufficient Evidence

Success: stable-late-gain appears with valid nested guards.

Failure: common-backbone geometry does not appear.

Insufficient evidence: data or checkpoint audit fails.

## 12. What This Cannot Claim

This cannot claim that common-subspace reuse is harmful, that C3S works, that MoE experts specialize, or that real language behaves the same way.

## 13. Review Notes And Protocol Changes

This protocol supersedes the old D07 metric-audit role for A07_01. Old D07 remains legacy controlled evidence only.
