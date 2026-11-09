# Summary: A12_02 One-Step Standard-NTP Interference

Primary anchor: `../../../problem_anchors/12_structured_compositional_mtp_workload/12_02_one_step_ntp_interference_anchor.md`
Protocol: `protocol.md`

## Result Snapshot

**Verdict:** insufficient evidence for the task-conditioned mechanism; the local first-order identity itself is numerically supported.

**What we established:** At relative parameter-step norm $10^{-5}$, the first-order prediction matches the paired finite difference with slope `1.0174`, Pearson correlation `0.9990`, sign agreement `1.0000`, and median normalized residual `0.1012`.

**What the experiment shows:** First-order gradient geometry accurately predicts the local one-step standard-loss difference at a small step. However, all five burn-in checkpoints remain at answer chance accuracy `0.125`, so the audit does not show interference after learning the composition task.

**What we do next:** repair the task/model calibration with one minimal known-good composition learner before opening capacity or curriculum anchors.

## Purpose

Test whether the extra standard-loss change caused by a direct second-future-token target is quantitatively predicted by $-\eta\langle g_N,g_A\rangle$.

## Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Controlled standard objective $L_N$ | two-position autoregressive objective shared by NTP and Next-2 | format CE plus next-state answer CE | nats | fair comparison | all-token LM quality |
| Auxiliary objective $L_A$ | direct future-answer objective | answer CE at the decision state | nats | added Next-2 signal | later usefulness |
| Prediction fidelity | agreement between local theory and intervention | slope, correlation, sign, normalized residual | dimensionless | tests the mechanism equation | full training |
| Calibration guard | evidence that the model has learned the controlled task | held-out next-state answer accuracy | probability | prevents interpreting random-task gradients | capacity cause |

## Exact Setup

**Research question:** Does the first-order gradient inner product predict the observed paired one-step standard-loss difference?
**Data / model / objective:** Exact $M=8$ two-permutation composition sequences; 8192 NTP burn-in examples and 1024 audit examples; one-layer causal Transformer with hidden width 64; $L_N=L_{format}+L_{answer}$ and $L_A=L_{answer}^{direct}$.
**Conditions:** cloned NTP-only and joint updates from the same checkpoint and batch.
**Changed variables:** inclusion of $g_A$ and relative step norm.
**Held fixed:** checkpoint, batch, targets, standard objective, and parameter set.
**Seeds / checkpoints:** seeds `971--975`; all reached step 600 because the `0.70` answer-accuracy guard was not met.
**Paths:** runner `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a12_02_one_step_ntp_interference.py`; raw result directory recorded in `detailed.md`.
**Known limitation:** the one-layer learner did not learn the two-hop composition, and the actual auxiliary loss reused the tied standard unembedding rather than a separately frozen auxiliary head.

## Primary Metric

**Definition:** origin-constrained slope of observed on predicted one-step differences at the two smallest step sizes.
**Unit:** dimensionless.
**Why it decides:** a quantitative mechanism should predict magnitude, not only gradient sign.
**False-positive cost:** opening capacity/curriculum work when the local equation is invalid. The calibration guard prevents this promotion here.

## Result

At $10^{-5}$ relative step norm, the equation passes every numerical fidelity threshold. Pooled over $10^{-5}$ and $3\times10^{-5}$, slope is `1.0530`, correlation `0.9741`, sign agreement `1.0000`, and median normalized residual `0.1102`. Error grows with step size: normalized residual is `0.1012`, `0.3046`, and `1.0676` from smallest to largest, consistent with increasing curvature.

The formal verdict remains insufficient because validation answer accuracy is exactly `0.125` in all five seeds. In addition, the actual auxiliary loss reused the tied standard unembedding and the preregistered shuffled-gradient negative control was not executed. The experiment validates the local Taylor calculation but not the intended learned-composition interference claim.

## Key Evidence

- Numerical law: smallest-step slope `1.0174`, correlation `0.9990`, sign agreement `1.0000`.
- Curvature guard: residual increases monotonically with step size.
- Calibration failure: five of five validation answer accuracies equal chance `0.125` at step 600.
- Sign heterogeneity: auxiliary gradients harm the standard objective in four seeds and help in one; the mean gradient cosine is `-0.0135`. Therefore conflict is not universal.

## Key Figures

### Figure: Predicted versus observed one-step standard-loss difference

![Predicted versus observed one-step standard-loss difference](figures/prediction_fidelity.png)

**What this tests:** whether the first-order prediction matches the paired intervention and whether error grows with update size.
**Anchor question:** the A12_02 local interference law.
**Protocol question:** prediction fidelity under three relative step norms.
**Metric shown:** predicted and observed loss difference; median normalized residual.
**Metric definition:** $\Delta_{pred}=-\eta\langle g_N,g_A\rangle$ and $\Delta_{obs}=L_N(\theta_M')-L_N(\theta_N')$.
**Metric unit:** nats for the left panel; dimensionless residual for the right.
**Data source:** 5 seeds × 32 audit batches × 3 step sizes.
**Aggregation level:** points are seed-batch observations; residual is pooled by step size.
**How to read:** points on the dashed identity line support the first-order equation; a rising right curve indicates increasing finite-step curvature.
**Expected if supported:** small-step points lie near identity and residual grows with step size.
**Expected if weakened or incomplete:** small-step sign/magnitude mismatch or no step-size dependence.
**What this figure decides:** the numerical local-law component passes.
**Observed result:** strong small-step agreement and increasing large-step residual.
**Allowed claim:** local first-order finite-difference fidelity at an uncalibrated task checkpoint.
**What this does not prove:** interference after task learning or long-run MTP harm.
**Anchor update implication:** keep the mathematical relation; do not open capacity/curriculum until calibration is repaired.

## Claim Boundary

**Can claim:** the local first-order equation is numerically faithful at sufficiently small paired updates in this implementation.
**Cannot claim:** Next-2 harms a model that learned composition, capacity explains small/large-model differences, curriculum repairs harm, or MTP improves real workloads.

## Next Decision

Use one minimal known-good architecture or symbolic composition module to make held-out answer accuracy exceed `0.70`, while preserving the same data, objectives, and finite-difference protocol. Only then rerun A12_02 and decide whether A12_03 capacity should open.
