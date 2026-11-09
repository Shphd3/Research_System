# A06_02_04_E01 Detailed Record: Representation-Router-Optimizer Co-Dynamics

## 1. Decision And Outcome

**Decision question:** Under trainable full-sequence LM dynamics, which path is necessary for first matched-margin crossing and later positive re-entry: router-row motion, representation motion, their coupling, or optimizer-conditioned transmission?

**Outcome:** The answer is optimizer-conditioned. Under AdamW, router-row motion is necessary for crossing; representation motion is not necessary for crossing but is required to reproduce most joint re-entry events. Under SGD, the joint model does not enter a sufficiently frequent crossing regime for the registered path classifier. AdamW produces a large and much earlier transient-crossing regime despite nearly identical final specialization.

## 2. Terminology / Definitions

| Term | Concrete meaning | Formula / unit | Role | Limitation |
| --- | --- | --- | --- | --- |
| Feature center | Mean router input for feature \(f\) on the fixed evaluation set | \(\mu_f\) | Represents feature geometry | Not a natural-language semantic center |
| Router-row gap | Difference between the intended and competing gate rows | \(v_{a,b}=w_a-w_b\) | Represents one decision boundary | Does not include expert utility |
| Matched margin | Intended expert's router-logit lead | \(m_{f,a,b}=v_{a,b}^\top\mu_f\) | Primary state variable | Positive margin does not prove useful expert computation |
| First crossing | First nonpositive matched margin | update step | Failure event | Can be transient |
| Positive re-entry | First later positive matched margin | update step | Correction event | Requires a previous crossing |
| Freeze-necessity fraction | Joint events removed by a paired path freeze | fraction in \([0,1]\) | Primary causal statistic | Does not prove sufficiency |
| Non-common feature | Features 1--3, which are opposed by class-0 background pressure | feature-seed cell | Primary decision population | Excludes feature 0 |

## 3. Mathematical Audit Model

For intended expert \(a=f\) and competitor \(b\),

\[
m_{f,a,b}(t)=(w_a(t)-w_b(t))^\top\mu_f(t).
\]

The exact one-step change is

\[
\Delta m
=(\Delta w_a-\Delta w_b)^\top\mu_f
+(w_a-w_b)^\top\Delta\mu_f
+(\Delta w_a-\Delta w_b)^\top\Delta\mu_f.
\]

This identity validates the implementation but does not assign causality. Causality is tested by freezing router rows or representation parameters under matched initial states and seeds.

For event \(E\) and path \(k\),

\[
N_k(E)=
\frac{\sum_i\mathbf 1[E_i^{joint}=1\land E_i^{freeze(k)}=0]}
{\sum_i\mathbf 1[E_i^{joint}=1]}.
\]

An event-bearing optimizer regime requires joint event rate at least 0.25. A path is called necessary when \(N_k(E)\ge0.75\).

AdamW transmits the raw gradient through history-dependent first and second moments:

\[
\Delta\theta_t=-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}-\eta\lambda\theta_t.
\]

This experiment tests whether AdamW changes the trajectory regime. It does not yet isolate which term in this update causes the change.

## 4. Exact Experimental Setup

### Data

Each batch contains 32 independent complete sequences. Each sequence has 33 repeated tokens and 32 supervised next-token positions. No positional embedding is used.

| Regime | Signal sequences | Background sequences | Purpose |
| --- | ---: | ---: | --- |
| `biased_s8` | 8, two per feature | 24 repeated class-0 common sequences | Critical biased-background condition |
| `biased_s4` | 4, one per feature | 28 repeated class-0 common sequences | Stronger biased-background condition |
| `signal_only_s32` | 32, eight per feature | 0 | Generic-instability guard |
| `solved_orthogonal_s4` | 4, one per feature | 28 solved neutral sequences | Background-count guard without route pressure |

The loss is mean cross-entropy over every next-token position. The construction does not reveal a route position or mask background losses.

### Model

- trainable token embedding, one causal multi-head self-attention layer, residual addition, and layer normalization;
- hidden size 64 and four attention heads;
- four-row linear router with weighted top-1 dispatch;
- four fixed function-matched affine expert vectors with strength 4;
- fixed class/type readout;
- trainable groups selected as router-only, representation-only, or joint.

### Initialization

All conditions for one seed clone the same base model. Router rows are initialized from signal feature centers and rescaled so the step-0 low-tail matched margin is 0.5. Every feature initially selects its identity-matched expert, and forced-expert loss verifies that expert \(f\) is useful for target \(f\).

### Optimization And Run Size

| Item | Value |
| --- | --- |
| Seeds | 0--31 |
| Updates | 1,000 |
| SGD | learning rate 0.002, no momentum, no weight decay |
| AdamW | learning rate 0.002, \(\beta_1=0.9\), \(\beta_2=0.999\), \(\epsilon=10^{-8}\), weight decay \(10^{-4}\) |
| Full-run hardware | 4 x N6LS 80 GB GPU |
| ACP job | `pt-aoko7u4m` |
| Run name | `a06_34_full_4gpu_20260710_01` |

Event status is checked every update. Full diagnostics are recorded at steps 0, 1, 2, 5, 10, 20, 40, 80, 160, 320, 500, 750, and 1000.

## 5. Protocol Corrections Before The Full Run

1. The original within-sequence signal/background construction allowed causal attention to carry feature-prefix information into nominal background positions. Signal and background were moved into separate complete sequences mixed within the same batch.
2. AdamW at learning rate 0.01 created excessive signal-only transients. The common nominal learning rate was fixed at 0.002 for both optimizers before the full run.
3. Balanced labels on identical common inputs created an irreducible prediction conflict in the trainable bridge. The count control was replaced by a step-0-solved router-orthogonal background.
4. Router-only and representation-only AdamW conditions were added before the full run after the pilot revealed an optimizer-conditioned event regime.

These changes preserve the anchor question and primary freeze-necessity metric.

## 6. Run Completion And Validity

| Check | Result | Criterion | Status |
| --- | ---: | ---: | --- |
| Completed seeds | 32 / 32 | 32 | pass |
| Event rows | 2,048 | complete condition matrix | pass |
| Trajectory rows | 26,624 | complete checkpoints | pass |
| Maximum finite-step margin closure error | \(8.32\times10^{-7}\) | \(<10^{-5}\) | pass |
| Maximum raw-gradient source closure error | \(4.77\times10^{-7}\) | \(<10^{-5}\) | pass |
| Maximum guard crossing rate | 7.29% | \(<25\%\) | pass |

The ACP job completed successfully on 2026-07-10.

## 7. Full Results

### 7.1 Critical Joint Conditions

The primary population is features 1--3.

| Regime | Optimizer | Crossing rate | Median cross | Re-entry given cross | Median re-entry | Final positive rate | Final margin p05 | Final route NMI |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| biased_s8 | SGD | 1.04% | 620 | 100% of one event | 622 | 100% | 0.0856 | 1.0000 |
| biased_s4 | SGD | 1.04% | 412 | 0% of one event | -- | 98.96% | 0.0723 | 0.9958 |
| biased_s8 | AdamW | 39.58% | 7 | 100% | 16.5 | 100% | 0.1360 | 1.0000 |
| biased_s4 | AdamW | 41.67% | 7 | 100% | 19.5 | 100% | 0.1377 | 1.0000 |

Final specialization alone would miss the central phenomenon: AdamW jointly trained models undergo frequent early boundary crossing and later recover.

### 7.2 Single-Path Interventions

| Regime | Condition | Crossing rate | Re-entry given cross | Final positive rate | Final margin p05 |
| --- | --- | ---: | ---: | ---: | ---: |
| biased_s8 | router SGD | 100% | 1.04% | 1.04% | -1.5433 |
| biased_s4 | router SGD | 100% | 0% | 0% | -1.6421 |
| biased_s8 | representation SGD | 0% | -- | 100% | 0.3714 |
| biased_s4 | representation SGD | 0% | -- | 100% | 0.3683 |
| biased_s8 | router AdamW | 100% | 40.63% | 38.54% | -1.3014 |
| biased_s4 | router AdamW | 100% | 19.79% | 16.67% | -1.5773 |
| biased_s8 | representation AdamW | 0% | -- | 100% | 0.3871 |
| biased_s4 | representation AdamW | 0% | -- | 100% | 0.3858 |

Router-only motion destroys every non-common binding under both optimizers. Representation-only motion never crosses and keeps substantial positive margin. Joint representation learning therefore counteracts router damage rather than causing it on this surface.

### 7.3 Paired Causal Classification

Across both biased regimes, joint AdamW has 78 crossing and re-entry events among 192 cells.

| Event | \(N_{representation}\) | \(N_{router}\) | \(N_{coupling}\) | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Crossing | 0.0000 | 1.0000 | 0.0000 | Router motion is necessary; representation motion is not necessary |
| Re-entry | 0.7949 | 1.0000 | 0.7949 | Joint co-training reproduces recovery that router-only misses in 62/78 cells |

The re-entry \(N_{router}\) value includes a structural prerequisite: representation-only conditions never cross. It cannot by itself show that router motion is a distinct correction mechanism after a matched crossing. The defensible recovery claim comes from the joint versus router-only contrast.

Joint SGD crosses in only 2 of 192 cells. Its apparent necessity fractions are not decision-bearing because the registered event-rate prerequisite is not met.

### 7.4 Optimizer Regime Effect

| Event | Joint SGD rate | Joint AdamW rate | Rate gap | Median SGD step | Median AdamW step | Time ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Crossing | 1.04% | 40.625% | +39.58 points | 516 | 7 | 73.71 |
| Re-entry | 0.52% | 40.625% | +40.10 points | 622 | 18 | 34.56 |

The optimizer-effect hypothesis is supported by both registered criteria: the event-rate gap exceeds 25 points and the median event-time ratio exceeds 2.

### 7.5 Guard Conditions

| Guard | Optimizer | Crossing rate | Re-entry given cross | Final margin p05 | Final route NMI |
| --- | --- | ---: | ---: | ---: | ---: |
| Signal only | SGD | 0% | -- | 0.4708 | 1.0000 |
| Signal only | AdamW | 7.29% | 100% | 1.8652 | 1.0000 |
| Solved orthogonal background | SGD | 0% | -- | 0.4882 | 1.0000 |
| Solved orthogonal background | AdamW | 7.29% | 100% | 1.7588 | 1.0000 |

AdamW can create low-rate early transients without biased background. The biased regimes nevertheless have a much larger 39.58--41.67% rate and a far smaller final low-tail margin. Thus background bias amplifies a generic AdamW transient but is not proven to be its sole origin.

## 8. Visualization Results

### Figure A: Margin Trajectories

![Margin trajectories](figures/margin_trajectories.png)

- **Question:** which trainable path changes the sign and long-run level of the matched margin?
- **Metric:** p05 matched margin over non-common feature-seed cells.
- **Axes:** training step versus router-logit margin; zero is the decision boundary.
- **Observed:** router-only curves become strongly negative; representation-only curves remain positive; joint AdamW crosses and recovers; joint SGD remains mostly positive.
- **Allowed conclusion:** representation co-training protects against router-only degradation.
- **Limitation:** the plot does not isolate AdamW's first moment, second moment, decay, or step magnitude.

### Figure B: Event Rates

![Event rates](figures/event_rates.png)

- **Question:** how often does each path cross and, after crossing, recover?
- **Metric:** fraction of feature-seed cells and conditional re-entry rate.
- **Observed:** all router-only cells cross; no representation-only cells cross; joint AdamW has frequent but fully recovered transients.
- **Allowed conclusion:** the event path differs from the final-state classification.
- **Limitation:** re-entry is undefined without crossing.

### Figure C: AdamW Freeze Necessity

![Freeze necessity](figures/paired_freeze_necessity.png)

- **Question:** which path removal eliminates joint AdamW events?
- **Metric:** paired freeze-necessity fraction; dashed line is the 0.75 criterion.
- **Observed:** freezing router eliminates all crossings; freezing representation eliminates 79.49% of re-entry events but no crossing events.
- **Allowed conclusion:** router motion initiates damage, while representation motion supplies most correction.
- **Limitation:** correction may be a coupled effect rather than representation motion alone.

## 9. Hypothesis Adjudication

| Hypothesis | Verdict | Reason |
| --- | --- | --- |
| H1: localize first crossing | supported under AdamW; insufficient under SGD | AdamW \(N_{router}=1\) with 40.625% joint event rate; SGD has only 1.04% joint events |
| H2: recovery can use a different path | supported with boundary | router-only reproduces all crossings but misses 79.49% of joint re-entry events |
| H3: optimizer changes the regime | supported | 39.58-point crossing gap and 73.71x median-time ratio |

## 10. Updated Mechanism

The data reject a representation-drift-first explanation for this surface. A more accurate mechanism is:

\[
\text{biased full-LM loss}
\rightarrow \text{optimizer-transmitted router-row motion}
\rightarrow \text{early boundary crossing},
\]

while the trainable representation provides a compensating path:

\[
\text{joint representation adaptation}
\rightarrow \text{feature-center correction relative to the moving boundary}
\rightarrow \text{positive-margin re-entry}.
\]

The optimizer determines whether the transient is common and early. The current evidence does not identify whether AdamW's effect comes from coordinate-wise second-moment normalization, first-moment accumulation, weight decay, or simply a larger effective router step.

## 11. Claim Boundary

**Established:** causal path classification for matched-margin crossing under AdamW on this synthetic fixed-utility neural bridge; representation-supported recovery; optimizer-conditioned event timing and frequency.

**Not established:** natural-language feature semantics, learned expert specialization, downstream utility, general optimizer rankings, MTP-to-MoE benefit, or a deployable routing algorithm.

## 12. Next Decision

The next anchor should ask:

> Is AdamW's coordinate-wise second-moment normalization of router gradients necessary for early matched-margin crossing, or can crossing be explained by total router-update magnitude alone?

The minimum causal controls are:

1. joint AdamW baseline;
2. AdamW representation plus norm-matched SGD router updates;
3. AdamW with the router second moment isotropized to one scalar per row or parameter group;
4. matched one-step boundary projections at shared checkpoints.

This decision precedes an MTP bridge. The present representation dynamics are protective, so adding a longer-horizon objective before localizing optimizer transmission would mix a new objective into an unresolved router-update mechanism.

## 13. Artifact Map

**Canonical research artifacts**

- Anchor: `main/problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`
- Protocol: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E01_representation_router_optimizer/protocol.md`
- Summary: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E01_representation_router_optimizer/summary.md`
- Curated tables: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E01_representation_router_optimizer/tables/`
- Curated figures: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E01_representation_router_optimizer/figures/`

**Experiment workspace**

- Runner: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_34_representation_router_optimizer_codynamics.py`
- Config: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_34_representation_router_optimizer_codynamics.json`
- Submission script: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_a06_34_representation_router_optimizer_codynamics_4gpu_acp.sh`
- Raw result directory: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_34_representation_router_optimizer_codynamics/a06_34_full_4gpu_20260710_01/`
- ACP job: `pt-aoko7u4m`

**Reproduction command**

```bash
bash scripts/submit_a06_34_representation_router_optimizer_codynamics_4gpu_acp.sh a06_34_full_4gpu_20260710_01
```

