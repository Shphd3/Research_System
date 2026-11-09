# A06_02_04_E02 Detailed Record: Optimizer-Preconditioned Router Boundary Pressure

## 1. Decision And Outcome

**Decision question:** Is AdamW's coordinate-wise second-moment normalization of router gradients necessary for early matched-margin crossing, or can the current raw-gradient direction reproduce crossing when its actual update norm is matched to full AdamW?

**Outcome:** Coordinate-wise second-moment anisotropy is not necessary. A scalar second moment reproduces 96.15% of full-AdamW events and creates more crossings. Current raw-gradient direction at the full-update norm reproduces 88.46% with a similar overall rate. Nominal SGD, whose first-50-step router-update norm is about 9.7 times smaller, reproduces none. Actual update scale is therefore the next causal variable; direction controls excursion depth and recovery speed.

## 2. Mathematical Intervention

The full router update is

\[
\Delta W_t^{full}
=-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}
-\eta\lambda W_t.
\]

The scalar-second-moment candidate is

\[
\tilde U_t^{iso}
=-\eta\frac{\hat m_t}{\sqrt{\operatorname{mean}(\hat v_t)}+\epsilon}
-\eta\lambda W_t,
\]

\[
\Delta W_t^{iso}
=\frac{\|\Delta W_t^{full}\|_2}{\|\tilde U_t^{iso}\|_2}
\tilde U_t^{iso}.
\]

The raw-gradient candidate is

\[
\Delta W_t^{raw}
=-\|\Delta W_t^{full}\|_2\frac{g_t}{\|g_t\|_2}.
\]

The nominal-SGD reference is

\[
\Delta W_t^{sgd}=-0.002g_t.
\]

All conditions train the representation with the same standard AdamW rule. Each condition maintains its own model and moment state.

## 3. Decision Metrics

For early crossing by step 50,

\[
R_q=\Pr(C^q=1\mid C^{full}=1),
\qquad
N_q=1-R_q.
\]

The boundary projection of the actual router update is

\[
b_{f,a,b}(t)
=\langle\Delta w_a(t)-\Delta w_b(t),\mu_f(t)\rangle,
\]

and cumulative negative pressure through step 50 is

\[
B_i(50)=\sum_{t=1}^{50}[-b_i(t)]_+.
\]

These metrics identify event reproduction and router-side pressure. They do not include the representation term in the exact margin decomposition.

## 4. Exact Setup

### Data And Model

- Four uniform features and four fixed function-matched experts.
- Each batch has 32 complete repeated-token sequences and 32 next-token losses per sequence.
- Critical regimes: 8/32 and 4/32 feature sequences; remaining sequences are class-0 background.
- Guards: 32/32 feature sequences and 4/32 feature plus solved router-orthogonal background.
- No positional embedding.
- One causal attention layer, residual, layer normalization, weighted top-1 routing, fixed readout.
- Initial matched-margin p05: 0.5.

### Optimization

| Component | Rule |
| --- | --- |
| Representation | AdamW, learning rate 0.002, \(\beta_1=0.9\), \(\beta_2=0.999\), \(\epsilon=10^{-8}\), weight decay \(10^{-4}\) |
| Router full reference | same standard AdamW |
| Router scalar-\(v\) | scalar second moment, full-update norm matched |
| Router raw norm | current raw-gradient direction, full-update norm matched |
| Router nominal SGD | learning rate 0.002, no momentum or decay |

### Run

- Seeds: 0--31.
- Updates: 1,000.
- Early horizon: 50.
- Hardware: four N6lS 80 GB GPUs.
- ACP job: `pt-fqs0n40o`.
- Run: `a06_35_full_4gpu_20260710_01`.
- Job state: succeeded on 2026-07-10.

## 5. Pre-Full Validation And Protocol Refinement

1. A deterministic 10-step parity test compared the manual full-router AdamW update with PyTorch AdamW. The maximum parameter error was \(9.54\times10^{-7}\), below the registered \(10^{-6}\) tolerance.
2. One-seed smoke completed all 16 condition/regime cells and kept scalar/raw norm-match error below \(1.9\times10^{-7}\).
3. Before the full run, the raw-gradient decision rule was clarified: extra raw-gradient crossings do not falsify reference-event reproduction. The registered condition therefore checks whether the raw-norm event rate falls more than 0.10 below full AdamW, not whether the absolute rate gap is small.

No data, model, early horizon, seed count, update rule, or primary reproduction metric changed after the full run began.

## 6. Completion And Validity

| Check | Result | Criterion | Status |
| --- | ---: | ---: | --- |
| Completed seeds | 32 / 32 | 32 | pass |
| Event rows | 2,048 | complete matrix | pass |
| Trajectory rows | 28,672 | complete checkpoints | pass |
| Update-pressure rows | 114,688 | complete first-50 and checkpoints | pass |
| Manual AdamW parity error | \(9.54\times10^{-7}\) | \(<10^{-6}\) | pass |
| Maximum norm-match error | \(2.30\times10^{-7}\) | \(<10^{-5}\) | pass |
| Maximum guard early-cross rate | 11.46% | \(<25\%\) | pass |

## 7. Event Results

### 7.1 Combined Critical Population

| Condition | Early events | Rate | Full events reproduced | \(R_q\) | \(N_q\) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Full AdamW | 78 / 192 | 40.625% | 78 | 1.0000 | 0.0000 |
| Scalar second moment | 100 / 192 | 52.08% | 75 | 0.9615 | 0.0385 |
| Raw gradient, norm matched | 84 / 192 | 43.75% | 69 | 0.8846 | 0.1154 |
| Nominal SGD | 0 / 192 | 0% | 0 | 0.0000 | 1.0000 |

The registered 0.75 necessity threshold is not reached for removing coordinate-wise second moments or full AdamW direction. Both hypotheses are rejected.

### 7.2 Regime Robustness

| Regime | Full AdamW | Scalar second moment | Raw norm match | Nominal SGD |
| --- | ---: | ---: | ---: | ---: |
| 8/32 signal | 39.58% | 51.04% | 41.67% | 0% |
| 4/32 signal | 41.67% | 53.13% | 45.83% | 0% |

The classification is consistent across both signal/background ratios.

### 7.3 Recovery And Final State

| Condition | Median cross | Median re-entry | Re-entry given cross | Final margin p05 | Final route NMI |
| --- | ---: | ---: | ---: | ---: | ---: |
| Full AdamW | 7 | 16.5--19.5 | 100% | 0.136--0.138 | 1.0 |
| Scalar second moment | 5 | 22 | 100% | 0.075--0.078 | 1.0 |
| Raw norm match | 5 | 6--7 | 100% | 0.298--0.327 | 1.0 |
| Nominal SGD | -- | -- | -- | 0.372--0.374 | 1.0 |

Same-norm directions change how deeply and how long the binding becomes negative. The raw current-gradient direction corrects fastest; first-moment accumulation under scalar \(v\) creates the longest excursion.

## 8. Actual Router Update Scale

| Horizon | Condition | Mean actual norm | Ratio to nominal SGD |
| --- | --- | ---: | ---: |
| 1--10 | Full AdamW | 0.014196 | 6.65x |
| 1--10 | Scalar second moment | 0.014187 | 6.65x |
| 1--10 | Raw norm match | 0.014105 | 6.61x |
| 1--10 | Nominal SGD | 0.002134 | 1.00x |
| 1--50 | Full AdamW | 0.004164 | 9.73x |
| 1--50 | Scalar second moment | 0.004203 | 9.83x |
| 1--50 | Raw norm match | 0.004054 | 9.48x |
| 1--50 | Nominal SGD | 0.000428 | 1.00x |

The mean is computed once per router update over both critical regimes and 32 seeds. This contrast motivates a norm-threshold experiment but does not yet identify the threshold.

## 9. Boundary Pressure

On the 78 full-AdamW-crossed cells:

| Condition | Mean \(B(50)\) | Change from full | Reference reproduction |
| --- | ---: | ---: | ---: |
| Full AdamW | 0.5283 | reference | 100% |
| Scalar second moment | 0.7233 | +36.92% | 96.15% |
| Raw norm match | 0.3926 | -25.68% | 88.46% |
| Nominal SGD | 0.0703 | -86.69% | 0% |

The safe nominal scale strongly reduces router-side negative pressure. The scalar/raw comparison shows that \(B(50)\) is not a complete recovery model: it sums after crossing and uses the current nearest competitor, while the representation and competitor identity evolve.

## 10. Guard Results

| Guard | Full AdamW | Scalar second moment | Raw norm match | Nominal SGD |
| --- | ---: | ---: | ---: | ---: |
| Signal-only early crossing | 7.29% | 11.46% | 1.04% | 0% |
| Solved orthogonal background early crossing | 7.29% | 9.38% | 1.04% | 0% |

Every guard event re-entered, every final margin was positive, and final route NMI was 1.0. The interventions therefore do not create widespread generic instability.

## 11. Visualization Results

### Figure A: Early Crossing Rates

![Early crossing rates](figures/early_cross_rates.png)

- **Question:** which optimizer components are needed for early crossing?
- **Metric:** feature-seed fraction crossing by step 50.
- **Observed:** scalar-\(v\) and raw norm match remain above the event threshold; nominal SGD is zero.
- **Allowed conclusion:** coordinate-wise \(v\) and AdamW-specific direction are unnecessary on this surface.
- **Limitation:** does not identify the critical actual norm.

### Figure B: Margin Trajectories

![Margin trajectories](figures/margin_trajectories.png)

- **Question:** how does update direction alter the transient after scale is held near the full reference?
- **Metric:** non-common-feature matched-margin p05.
- **Observed:** scalar \(v\) has the deepest/longest negative interval; raw-gradient direction rapidly re-enters; nominal SGD remains positive.
- **Allowed conclusion:** direction affects severity and recovery.
- **Limitation:** later states are not matched across interventions.

### Figure C: Negative Router Pressure

![Boundary pressure](figures/boundary_pressure.png)

- **Question:** does the safe scale reference remove router-side margin consumption?
- **Metric:** cumulative negative actual router projection through step 50 on full-reference crossed cells.
- **Observed:** nominal SGD reduces pressure 86.69%; scalar \(v\) increases it; raw norm match remains event-bearing.
- **Allowed conclusion:** router scale is a plausible causal control variable.
- **Limitation:** \(B(50)\) includes post-cross correction and excludes representation terms.

## 12. Hypothesis Adjudication

| Hypothesis | Verdict | Reason |
| --- | --- | --- |
| H1: coordinate-wise second moment necessary | rejected | \(N_{iso}=0.0385\), far below 0.75 |
| H2: AdamW-specific direction unnecessary | supported | raw norm match \(R=0.8846\) and event rate is not below full |
| H3: first-moment direction sufficient but raw direction insufficient | rejected | raw reproduction is 88.46% |
| H4: negative pressure mediates crossing | supported for the scale contrast; incomplete for recovery | nominal SGD reduces pressure 86.69% and removes crossing; same-norm directions differ in recovery |

## 13. Updated Mechanism

The supported mechanism is now:

\[
\text{large early actual router-update norm}
\times
\text{task/background gradient direction}
\rightarrow
\text{matched-boundary crossing},
\]

with optimizer history shaping the transient rather than being required to create it:

\[
\text{first/second-moment direction}
\rightarrow
\text{crossing depth and recovery time}.
\]

Representation learning remains the correction path identified in A06_02_04_E01.

## 14. Claim Boundary

**Established:** coordinate-wise AdamW second moments are not necessary; current raw-gradient direction at full-AdamW norm reproduces most early events; nominal SGD scale is safe and has much lower pressure.

**Not established:** update norm alone is sufficient, the exact stability threshold, a label-free real-model margin controller, learned-expert behavior, downstream utility, or MTP benefit.

## 15. Next Decision

The next anchor should test a small controlled norm multiplier set while fixing router direction to the current raw gradient and keeping representation AdamW unchanged. It should determine whether the dimensionless router pressure budget

\[
\rho_i(T)=\frac{B_i(T)}{m_i(0)}
\]

predicts crossing before representation correction. An adaptive router-step method is justified only if a reproducible threshold exists and LM progress remains comparable.

## 16. Artifact Map

**Canonical artifacts**

- Anchor: `main/problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`
- Protocol: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E02_optimizer_boundary_pressure/protocol.md`
- Summary: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E02_optimizer_boundary_pressure/summary.md`
- Tables: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E02_optimizer_boundary_pressure/tables/`
- Figures: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E02_optimizer_boundary_pressure/figures/`

**Experiment workspace**

- Runner: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_35_optimizer_preconditioned_router_boundary_pressure.py`
- Config: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_35_optimizer_preconditioned_router_boundary_pressure.json`
- Submission: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_a06_35_optimizer_preconditioned_router_boundary_pressure_4gpu_acp.sh`
- Raw results: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_35_optimizer_preconditioned_router_boundary_pressure/a06_35_full_4gpu_20260710_01/`
- ACP job: `pt-fqs0n40o`

**Reproduction**

```bash
A0635_ALLOW_REAL_SUBMIT=1 RUN_NAME=a06_35_full_4gpu_20260710_01 bash scripts/submit_a06_35_optimizer_preconditioned_router_boundary_pressure_4gpu_acp.sh
```
