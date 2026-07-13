# Does Local MTP Gradient Interaction Explain Standard-NTP Degradation?

## 0. Executive Summary

**Research question:** Does first-order gradient interference explain local standard-loss harm from an informative second-future-token objective well enough to open capacity and curriculum studies?

**Mechanism:** The equation compares a joint update with an NTP-only update from the same checkpoint; it does not imply an absolute loss increase from the pre-update state.

$$
\Delta_{obs}=-\eta\lambda\langle g_N,g_A\rangle+O(\eta^2).
$$

**Main results:**

1. The local equation is numerically faithful at relative step norm $10^{-5}$: slope `1.0174`, Pearson `0.9990`, sign agreement `1.0000`.
2. The one-layer learner did not learn the two-hop answer: validation answer accuracy is chance `0.125` in all five seeds.
3. Capacity, curriculum, and scale anchors remain gated; the only next action is a known-good composition calibration followed by the identical audit.

**Claim boundary:** This supports local differential geometry, not learned-task interference or general MTP behavior.

## 1. Terminology / Definitions

| Term | Plain meaning | Computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Controlled standard objective $L_N$ | two-position objective shared by NTP and Next-2 | format CE plus next-state answer CE | fair comparison | all-token LM quality |
| Auxiliary objective $L_A$ | direct future-answer loss using the tied standard unembedding | answer CE at the decision state | added gradient | a separate MTP head or later use |
| Fidelity slope | magnitude agreement | origin-constrained regression | primary decision | task calibration |
| Calibration guard | task learned before mechanism interpretation | held-out answer accuracy $\ge0.70$ | prevents random-checkpoint claims | why learning failed |

## 2. Mechanism Model

$$
g_N=\nabla L_N,\quad g_A=\nabla L_A,\quad
\theta_N'=\theta-\eta g_N,\quad
\theta_M'=\theta-\eta(g_N+\lambda g_A).
$$

The two-permutation task is $B=\pi_1(A)$ and $Y=\pi_2(B)$.

If $L_N$ is twice differentiable, the explicit second-order correction is

$$
\Delta_{obs}
=-\eta\lambda g_N^\top g_A
+\eta^2\lambda g_N^\top H_Ng_A
+\frac{\eta^2\lambda^2}{2}g_A^\top H_Ng_A
+O(\eta^3).
$$

## 3. Main Results

![Prediction fidelity](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_22_one_step_ntp_interference/figures/prediction_fidelity.png)

The smallest step passes the numerical-law thresholds, while residual grows with step size. The hard calibration guard fails in five of five seeds, so the formal verdict is insufficient evidence for learned-task interference. A11_01--A11_20 have complete protocol/summary/detailed records; A11_21 is explicitly parked; A11_22 is closed with this insufficient verdict; A11_23--A11_26 are not open.

## 4. Execution Action

Use one minimally deeper or explicitly compositional architecture while holding data, objectives, seeds, and audit fixed. Complete when all five validation answer accuracies exceed `0.70`, the same finite-difference thresholds pass, and the preregistered shuffled-gradient negative control is present.

## 5. Evidence Index

See the canonical [anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_22_one_step_ntp_interference_anchor.md), [protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_22_one_step_ntp_interference/protocol.md), [summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_22_one_step_ntp_interference/summary.md), and [detailed record](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_22_one_step_ntp_interference/detailed.md).

## 6. Source Index

All included sources are listed above; no capacity or curriculum result is included because those anchors were not opened.

## 7. Supplement

The Chinese companion contains the complete advisor-facing question-by-question table and 30-second script.
