# Protocol: A06_02_04_E02 Optimizer-Preconditioned Router Boundary Pressure

## 0. Approval Snapshot

**Approval status:** approved by the user's standing instruction to continue the specialization line with one definite anchor per experiment iteration and execute full runs on four remote GPUs.

**Purpose:** isolate whether AdamW's coordinate-wise router second moment, first-moment direction, or total actual update norm causes the early crossing regime found in A06_02_04_E01.

**Primary anchor:** `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

**Decision question:** Is coordinate-wise second-moment normalization necessary for early matched-margin crossing, or is router-update magnitude sufficient?

**Primary metric:** paired reproduction/removal of full-AdamW early-cross events by step 50.

**Minimal setup:** exact A06_02_04_E01 data/model/initialization; representation always uses AdamW; only router update transmission changes.

**Basic configuration:** 32 seeds, 1,000 updates, four GPU shards, two biased-background regimes, two guards, four router-update rules.

**Pass:** full AdamW reproduces at least 0.25 early-cross rate and one registered mechanism classification is reached with norm-match and guard checks passing.

**Fail:** the named component is removed but at least 75% of full-AdamW events reproduce, or the raw norm-matched condition reproduces events and magnitude is sufficient.

**Insufficient:** fewer than 32 seeds, full AdamW early-cross rate below 0.25, norm-match relative error above \(10^{-5}\), manual AdamW parity failure, or guard crossing rate at least 0.25.

**Cannot claim:** a final Router, real-text specialization, learned-expert utility, MTP benefit, or downstream interference reduction.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| `full_adamw` | Standard AdamW on representation and router | PyTorch-equivalent update | condition | Reference event regime | General superiority |
| `scalar_v_norm` | Standard AdamW representation; router uses first moment with scalar second moment and full-update norm | formula in anchor | condition | Removes coordinate-wise \(v\) | Removes first-moment history |
| `raw_norm` | Standard AdamW representation; router uses current raw-gradient direction at full-update norm | formula in anchor | condition | Tests magnitude sufficiency | Same future state |
| `sgd_nominal` | Standard AdamW representation; router uses plain SGD at learning rate 0.002 | \(-\eta g\) | condition | Declared-LR reference | Moment causality |
| Early-cross rate | Fraction crossing by step 50 | mean of \(C_i\) | fraction | Primary event | Long-run failure |
| Reproduction fraction | Full-reference events also present under intervention | \(R_q\) | fraction | Tests necessity | Sufficiency outside tested surface |
| Norm-match error | Relative difference between intervention and full candidate update norms | \(|\|\Delta W^q\|-\|\Delta W^{full}\||/(\|\Delta W^{full}\|+\epsilon)\) | relative error | Validates direction-only intervention | Boundary equivalence |

## 2. Anchor Alignment

The protocol keeps representation dynamics, fixed expert utility, data, loss, initialization, seed, and training horizon unchanged. It intervenes only on router optimizer transmission, the unresolved term from A06_02_04_E01.

## 3. Hypotheses And Decision Rules

For each non-common feature-seed-regime cell:

\[
C_i^{q}=\mathbf1[T_{cross,i}^{q}\le50].
\]

For intervention \(q\) relative to `full_adamw`:

\[
R_q=\frac{\sum_i C_i^{full}C_i^q}{\sum_i C_i^{full}},
\qquad
N_q=1-R_q.
\]

- Coordinate-wise second moment necessary: \(N_{scalar\_v\_norm}\ge0.75\).
- AdamW-specific directional history unnecessary: \(R_{raw\_norm}\ge0.75\) and the raw-norm early-cross rate is no more than 0.10 below full AdamW.
- First-moment direction sufficient: \(R_{scalar\_v\_norm}\ge0.75\) and \(R_{raw\_norm}<0.25\).
- Multiple mechanisms / unresolved: no rule above holds.

All rules require full-reference event rate at least 0.25, norm-match error below \(10^{-5}\), guards below 0.25, and 32 complete seeds.

## 4. Data, Model, Objective, And Initialization

Reuse the A06_02_04_E01 contract exactly:

- 32 complete sequences per batch, 33 repeated tokens each, 32 next-token losses;
- `biased_s8`, `biased_s4`, `signal_only_s32`, and `solved_orthogonal_s4`;
- no positional embedding;
- one causal attention layer, residual, layer normalization, weighted top-1 router;
- four fixed function-matched affine experts and fixed readout;
- step-0 identity binding with matched-margin p05 0.5;
- full-position cross-entropy.

Any data/model/init difference from the A06_02_04_E01 config invalidates the comparison.

## 5. Router Update Algorithms

Representation parameters use a separate standard AdamW optimizer in all conditions.

At each router step, update common internal moments:

\[
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,
\qquad
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2.
\]

Compute the full candidate:

\[
U_t^{full}=-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}-\eta\lambda W_t.
\]

Then apply one rule:

1. `full_adamw`: \(\Delta W=U_t^{full}\).
2. `scalar_v_norm`: replace \(\hat v_t\) by its router-wide mean, include the same decay term, then rescale to \(\|U_t^{full}\|_2\).
3. `raw_norm`: use \(-g_t/\|g_t\|_2\) and rescale to \(\|U_t^{full}\|_2\).
4. `sgd_nominal`: use \(-0.002g_t\) without momentum or decay.

The moments are still updated in every condition so counterfactual full/scalar/raw candidates can be logged at each condition's current state.

## 6. Conditions, Seeds, And Checkpoints

| Regime | Conditions | Role |
| --- | --- | --- |
| `biased_s8` | all four router rules | primary |
| `biased_s4` | all four router rules | primary robustness |
| `signal_only_s32` | all four router rules | generic-transient guard |
| `solved_orthogonal_s4` | all four router rules | background-count guard |

- Seeds: 0--31.
- Updates: 1,000.
- Four shards: eight seeds per GPU.
- Event logging: every step.
- Boundary/update logging: steps 1--50 and diagnostic checkpoints 80, 160, 320, 500, 750, 1000.

## 7. Primary And Secondary Metrics

**Primary:** combined-critical \(R_q\), \(N_q\), and early-cross-rate gap for features 1--3.

**Mechanism metric:** cumulative negative router boundary pressure through step 50:

\[
B_i^q(50)=\sum_{t=1}^{50}[-b_i^q(t)]_+.
\]

**Validity:** norm-match maximum error, manual-versus-PyTorch AdamW parity, step-0 binding/utility, finite values, complete seeds.

**Guards:** final margin p05, final positive-margin rate, route NMI, LM loss, signal/background accuracy, and guard early-cross rate.

## 8. Stage Plan

| Stage | Question | Pass | Stop condition |
| --- | --- | --- | --- |
| parity unit test | Does manual `full_adamw` equal PyTorch AdamW? | max parameter error \(<10^{-6}\) for 10 deterministic steps | any larger error |
| smoke | Are all update rules finite and norm matched? | one seed, 50 steps, error \(<10^{-5}\) | invalid update or guard explosion |
| pilot | Does full AdamW reproduce early crossing? | one seed trend consistent with A06_02_04_E01 | pilot only; never evidence |
| full | Do 32 seeds classify the mechanism? | complete matrix and valid guards | missing shard or invalid comparison |
| visualization | Can the decision be read directly? | event, pressure, and trajectory plots | unclear or post-hoc metric |

## 9. Output Contract

- `events.csv`: first crossing, early crossing, re-entry, final margin/route.
- `update_pressure.csv`: actual and counterfactual update norms, norm-match errors, and boundary projections.
- `condition_summary.csv`: early/ever crossing, final guards.
- `paired_reproduction.csv`: \(R_q\), \(N_q\), and rate gaps.
- `pressure_summary.csv`: cumulative negative pressure through step 50.
- central figures: early crossing, boundary pressure, margin trajectories.
- canonical `summary.md`, `detailed.md`, and anchor verdict after full completion.

## 10. Claim Boundary And Next Decision

The experiment classifies only optimizer components on the controlled A06 neural bridge. If coordinate-wise \(v\) is necessary, the next anchor tests an optimizer-aware router update. If raw-gradient direction at the full norm is sufficient, the next anchor tests adaptive router step control. If neither is sufficient, the next anchor decomposes first-moment and signal/background gradient accumulation.
