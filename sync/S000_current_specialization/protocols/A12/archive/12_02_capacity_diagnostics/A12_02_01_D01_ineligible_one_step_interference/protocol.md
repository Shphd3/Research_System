# Protocol: A12_02 One-Step Standard-NTP Interference

## 0. Approval Snapshot

**Approval status:** approved by the user's explicit 2026-07-12 instruction to execute the first experiment.
**Purpose:** decide whether first-order gradient interference quantitatively explains the local standard-loss penalty of Next-2.
**Primary anchor:** `../../../problem_anchors/12_structured_compositional_mtp_workload/12_02_one_step_ntp_interference_anchor.md`.
**Anchor decision question:** does $-\eta\lambda\langle g_N,g_A\rangle$ predict the paired one-step standard-loss difference?
**Anchor physical prior tested:** sufficiently small paired updates are controlled by local first-order loss geometry.
**Anchor core model term tested:** $-\eta\lambda\langle g_N,g_A\rangle$.
**Anchor falsifier:** resolved small-step measurements disagree in sign or batchwise variation.
**Experiment role:** root-cause audit.
**Primary metric from anchor:** origin-constrained regression slope of $\Delta_{obs}$ on $\Delta_{pred}$, pooled over the two smallest valid relative step sizes.
**Claim boundary from anchor:** local controlled one-step mechanism only.
**Minimal setup:** exact $M=8$ permutation-composition data; one-layer causal Transformer; NTP burn-in; paired cloned updates.
**Basic configuration:** five seeds; 32 fixed audit batches per seed; relative parameter-step norms $10^{-5},3\times10^{-5},10^{-4}$; float64 audit.
**Conditions to run:** NTP-only update and NTP-plus-auxiliary update from an identical checkpoint and batch.
**Pass:** pooled small-step slope in $[0.8,1.2]$, Pearson correlation at least $0.95$, sign agreement at least $0.90$, and median normalized residual at most $0.20$; all guards pass.
**Fail:** correlation below $0.5$ or sign agreement below $0.70$ at resolved small steps, with all guards valid.
**Insufficient:** metrics fall between thresholds, fewer than 80% of rows are numerically resolved, or any pairing/data/restore guard fails.
**Cannot claim:** full-training causality, capacity scaling, curriculum benefit, natural-language transfer, or general MTP superiority.
**Approval decision:** run only this root-cause audit; later anchors remain gated by its result.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| $L_N$ | shared standard autoregressive objective | decision-format CE plus next-state answer CE | nats | fair NTP target | final task quality |
| $L_A$ | Next-2-only future answer objective | answer CE read directly at decision state | nats | added supervision | downstream use |
| relative step norm | update size normalized by parameter norm | $\|\delta\theta\|/\|\theta\|$ | dimensionless | compares stable local scales | optimizer training dynamics |
| $\Delta_{pred}$ | first-order predicted standard-loss difference | $-\eta\lambda\langle g_N,g_A\rangle$ | nats | mechanism prediction | curvature |
| $\Delta_{obs}$ | measured paired one-step difference | $L_N(\theta_M')-L_N(\theta_N')$ | nats | causal local observation | long-run convergence |

## 2. Anchor Alignment

**Decision question:** the exact A12_02 question.
**Physical prior tested:** first-order local geometry.
**Core model term tested:** gradient inner product scaled by the actual step.
**Falsifier:** valid small-step finite differences do not track the prediction.
**Claim boundary:** controlled local one-step mechanism.

## 3. Tested Hypothesis

At the two smallest resolved update scales, $\Delta_{obs}=\Delta_{pred}+O(\eta^2)$ across batches and seeds.

## 4. Rival Explanations

1. Curvature dominates at the chosen step size.
2. Standard supervision differs between conditions.
3. Audit batches or parameter states are not paired.
4. The auxiliary head is random and produces arbitrary gradients.
5. Float precision hides the finite difference.

## 5. Data / Model / Algorithm / Objective

- Data: `D_model8` from `daily_research_reports/0712/docs/mtp_math_foundations_and_synthetic_data_audit_cn.md`; six length-matched permutation tables, input length 155, target `<FMT_u> <E_y>`.
- Train split: 8192 examples; audit split: 1024 examples in 32 fixed batches.
- Model: one-layer causal Transformer, $d=64$, four heads, MLP width 256, atomic vocabulary.
- Standard loss: $L_N=L_{format}(h_T)+L_{answer}(h_{T+1})$.
- Intended auxiliary loss: $L_A=L_{answer}^{direct}(h_T)$ using the standard answer unembedding rows at the decision state.
- Burn-in: NTP-only AdamW until the frozen validation rule or the preregistered step budget is reached.
- Audit: float64 gradients and direct cloned SGD perturbations; no optimizer state is applied.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| paired NTP vs joint update | first-order law | $\langle g_N,g_A\rangle$ | decisive comparison | primary | protocol thresholds | fail thresholds | middle range | `finite_difference.csv`, main figure |
| three relative step sizes | curvature guard | $O(\eta^2)$ | residual should shrink | secondary | monotone/compatible | contrary pattern | noisy | `step_size_summary.csv` |
| format-flip paired batch | local/answer direction guard | head calibration | verifies objective separation | guard | target-selective gradients | no separation | noisy | `guard_metrics.csv` |
| data and restore hashes | pairing guard | implementation | excludes state mismatch | guard | exact | mismatch | missing | `guard_metrics.csv` |

Seeds are `971,972,973,974,975`. The single selected checkpoint per seed is the first validation checkpoint with answer accuracy at least `0.70`; if none reaches it by 600 steps, use step 600 and mark the calibration guard failed.

## 7. Primary Metric

For resolved rows at relative step norms $10^{-5}$ and $3\times10^{-5}$, fit the origin-constrained slope

$$
\widehat\beta=\frac{\sum_i\Delta_{pred,i}\Delta_{obs,i}}{\sum_i\Delta_{pred,i}^2}.
$$

It decides whether the theory predicts magnitude, not only sign. A false positive would open an unsupported capacity explanation; therefore slope, correlation, sign, residual, and guards must all pass.

## 8. Secondary Metrics

- Pearson correlation and sign agreement;
- median $|\Delta_{obs}-\Delta_{pred}|/(|\Delta_{pred}|+\epsilon)$;
- gradient cosine;
- residual divided by squared relative step norm;
- validation format and answer accuracy;
- format-flip gradient selectivity.

## 9. Known Good / Known Bad / Known Confusing Cases

- Known good: replace $g_A$ by $g_N$; the prediction is positive and finite difference should match.
- Known bad: independently shuffle audit gradients across batches; correlation should collapse.
- Known confusing: near-zero $\Delta_{pred}$ rows; exclude only when below the preregistered float64 resolution floor and report their fraction.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| data | are splits and labels exact? | manifests and balance counts | exact or stop | `data_manifest.json` | detailed |
| burn-in | is the answer head non-random? | validation curves | answer accuracy $\ge0.70$ | `training_curves.csv` | detailed |
| gradient | are paired gradients finite? | norms and hashes | finite and exact | `guard_metrics.csv` | detailed |
| finite step | does theory predict observation? | per-row table | protocol thresholds | main figure | summary |

## 11. Algorithm Specification

**input:** fixed checkpoint and audit batch.
**parameters:** $\lambda=1$ and three relative step norms.
**intermediate variables:** $g_N,g_A$, actual scalar $\eta$ selected so $\|\eta g_N\|/\|\theta\|$ equals the requested relative norm.
**steps:** compute both gradients; clone parameters; apply NTP and joint SGD updates; evaluate the same $L_N$ batch; restore; record prediction and observation.
**outputs:** tables, guards, decision, and figure.
**pass/fail:** section 0 thresholds.
**failure reasons:** curvature, unresolved signal, checkpoint failure, or implementation mismatch.

## 12. Success / Failure / Insufficient Evidence

Apply section 0 without post-hoc threshold changes. Passing only gradient cosine is not success.

## 13. What This Cannot Claim

The run cannot decide low-rank competition, scale dependence, curriculum learning, cross-position preservation, natural-language transfer, or final MTP performance.

## 14. Review Notes And Protocol Changes

The standard objective was corrected before execution to include both format and next-position answer losses. This prevents the unfair earlier draft in which NTP received no answer supervision. The actual runner reused the tied standard unembedding directly rather than instantiating a separately copied and frozen auxiliary head. This post-run compliance note narrows the result to a shared-readout auxiliary objective; it does not change the insufficient-evidence verdict. No thresholds were changed after results appeared.
