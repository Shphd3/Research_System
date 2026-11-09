# Protocol: A06_02_04_E03 Router Update Norm And Margin Budget

## 0. Approval Snapshot

**Approval status:** approved by the user's standing instruction to continue the specialization line with a definite anchor and execute each full iteration on four remote GPUs.

**Purpose:** estimate a direction-fixed router-update norm transition and test whether a pre-registered router-only pressure ratio predicts early crossing on held-out seeds.

**Primary anchor:** `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

**Decision question:** Does a reproducible norm threshold exhaust initial margin before representation correction?

**Primary metrics:** early-cross rate by norm multiplier and held-out balanced accuracy of \(\rho^{router}\ge1\).

**Run:** 32 seeds, 1,000 steps, four GPUs, four multipliers, two critical regimes, two guards.

**Pass:** H1 scale monotonicity, H2 critical interval, H3 held-out prediction, and H4 learning guard all pass.

**Fail:** any named hypothesis fails with valid complete data.

**Insufficient:** reference event regime, norm scaling, guard, or completion contract fails.

**Cannot claim:** an adaptive Router method before this protocol is adjudicated.

## 1. Exact Reuse Contract

Reuse A06_02_04_E02 exactly:

- four features, four fixed function-matched experts;
- 32 complete repeated-token sequences and full 32-position LM loss;
- `biased_s8`, `biased_s4`, signal-only, and solved orthogonal background;
- no positional embedding;
- one causal attention layer, residual, layer normalization, weighted top-1 routing;
- initial margin p05 0.5;
- representation AdamW at learning rate 0.002;
- 32 seeds and 1,000 updates.

Only the applied raw-gradient router-update norm multiplier changes.

## 2. Conditions

At every step, maintain Adam moments to compute the current full-AdamW router candidate norm. Apply

\[
\Delta W_t^{(\alpha)}
=-\alpha\|\Delta W_t^{full}\|_F
\frac{g_t}{\|g_t\|_F}.
\]

Conditions:

| Name | \(\alpha\) | Role |
| --- | ---: | --- |
| `raw_a1` | 1.0 | event reference |
| `raw_a0p5` | 0.5 | upper intermediate scale |
| `raw_a0p25` | 0.25 | lower intermediate scale |
| `raw_a0p125` | 0.125 | near nominal-SGD scale |

All four conditions run on all four data regimes.

## 3. Pairwise Budget Logging

For every feature \(f\), competitor \(b\ne f\), and step 1--50, record:

\[
m_{f,b}(0),\quad
r_{f,b}(t),\quad
c_{f,b}(t),\quad
\Delta m_{f,b}(t),
\]

with closure

\[
\left|\Delta m-r-c\right|<10^{-5}.
\]

The router-only predictor is

\[
\rho_f^{router}(50)
=\max_{t\le50,b\ne f}
\frac{-\sum_{s=1}^{t}r_{f,b}(s)}{m_{f,b}(0)}.
\]

Do not tune the threshold. Use \(\rho\ge1\) on seeds 16--31.

## 4. Decision Rules

### H1 Scale Monotonicity

For each of `biased_s8` and `biased_s4`:

- rate(\(1\)) \(\ge\) rate(\(0.5\)) \(-0.05\);
- rate(\(0.5\)) \(\ge\) rate(\(0.25\)) \(-0.05\);
- rate(\(0.25\)) \(\ge\) rate(\(0.125\)) \(-0.05\);
- rate(\(1\)) \(\ge0.25\) and rate(\(0.125\)) \(\le0.10\).

### H2 Critical Interval

At least one adjacent pair \((1,0.5)\), \((0.5,0.25)\), or \((0.25,0.125)\) must satisfy in both critical regimes:

- higher-scale rate \(\ge0.25\);
- lower-scale rate \(\le0.10\).

### H3 Held-Out Prediction

On seeds 16--31, combined critical features 1--3:

- balanced accuracy \(\ge0.80\);
- false-positive rate \(\le0.25\);
- report TPR, TNR, precision, and event prevalence.

### H4 Learning Guard

Select the largest multiplier whose early-cross rate is at most 0.10 in both critical regimes. Relative to `raw_a1`:

- final LM loss increase \(\le5\%\);
- final route NMI \(\ge0.95\);
- final positive-margin rate \(\ge0.95\).

If no multiplier is safe, H4 fails.

## 5. Seeds, Checkpoints, And Execution

- Full seeds: 0--31.
- Held-out prediction seeds: 16--31.
- Four shards: eight seeds per GPU.
- Updates: 1,000.
- Events: every step.
- Pairwise budgets: every step 1--50.
- Trajectory checkpoints: 0, 1, 2, 5, 10, 20, 40, 50, 80, 160, 320, 500, 750, 1000.

## 6. Validity And Guards

- maximum norm-scale relative error \(<10^{-5}\);
- maximum pairwise budget closure error \(<10^{-5}\);
- all 32 seeds and 2,048 event rows complete;
- signal-only and solved-orthogonal-background maximum early-cross rate \(<0.25\);
- finite loss and parameters throughout.

## 7. Output Contract

- `events.csv` and `condition_summary.csv`;
- `pairwise_budget.csv` and `budget_cell_summary.csv`;
- `scale_transition.csv`;
- `heldout_budget_prediction.csv` and confusion metrics;
- `trajectory_summary.csv`;
- central figures for scale transition, pressure prediction, and margin trajectories;
- canonical `summary.md`, `detailed.md`, and anchor verdict.

## 8. Claim Boundary And Next Decision

The run tests a scale law only on the fixed-utility synthetic bridge. A method anchor follows only if scale monotonicity, a critical interval, held-out prediction, and learning preservation all pass.

