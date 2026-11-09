# A06_02_04_E03 Detailed Record: Router Update Norm And Margin Budget

## 1. Decision And Outcome

**Decision question:** With raw-gradient direction fixed, does a reproducible router-update norm threshold exhaust initial margin before representation correction, and does a router-only pressure ratio predict held-out crossing?

**Outcome:** The causal scale transition is supported, but the router-only physical threshold and the relative terminal-loss guard fail. Crossing falls from 41.67--45.83% at full norm to 3.13--4.17% at half norm and zero at quarter/eighth norm. The router-only score has AUC 0.978 but only 20% recall at the untuned threshold 1 because direct representation motion contributes roughly 0.29 initial margins at crossing.

## 2. Mathematical Model

The applied router update is

\[
\Delta W_t^{(\alpha)}
=-\alpha\|\Delta W_t^{full}\|_F
\frac{g_t}{\|g_t\|_F}.
\]

For each pair \((f,b)\),

\[
\Delta m_{f,b}(t)
=r_{f,b}(t)+c_{f,b}(t),
\]

\[
r_{f,b}(t)
=(\Delta w_f-\Delta w_b)^\top\mu_f,
\]

\[
c_{f,b}(t)
=(w_f-w_b)^\top\Delta\mu_f
+(\Delta w_f-\Delta w_b)^\top\Delta\mu_f.
\]

The pre-registered router-only predictor is

\[
\rho_f^{router}(50)
=\max_{t\le50,b\ne f}
\frac{-\sum_{s=1}^{t}r_{f,b}(s)}{m_{f,b}(0)}.
\]

The threshold is fixed at 1 on held-out seeds 16--31.

## 3. Exact Setup

- Four uniform features; four fixed function-matched experts.
- 32 complete repeated-token sequences and 32 full next-token losses per sequence.
- Critical regimes: 8/32 and 4/32 signal sequences; remaining sequences are class-0 background.
- Guards: all signal; signal plus solved router-orthogonal background.
- One causal attention layer, residual, layer normalization, no positional embedding.
- Representation always uses standard AdamW at learning rate 0.002.
- Router always uses current raw-gradient direction.
- Norm multipliers: 1, 0.5, 0.25, 0.125.
- Initial margin p05: 0.5.
- 32 seeds, 1,000 updates, four GPUs.
- ACP job: `pt-114g2p4y`; run `a06_36_full_4gpu_20260710_01`; state succeeded.

## 4. Completion And Validity

| Check | Result | Criterion | Status |
| --- | ---: | ---: | --- |
| Completed seeds | 32 / 32 | 32 | pass |
| Event rows | 2,048 | complete | pass |
| Trajectory rows | 28,672 | complete | pass |
| Pairwise budget rows | 307,200 | complete first 50 steps | pass |
| Norm-scale error | \(2.15\times10^{-7}\) | \(<10^{-5}\) | pass |
| Budget closure error | \(6.70\times10^{-7}\) | \(<10^{-5}\) | pass |
| Manual AdamW parity | \(9.54\times10^{-7}\) | \(<10^{-6}\) | pass |
| Guard early-cross rate | 4.17% | \(<25\%\) | pass |

## 5. Scale Intervention Results

### 5.1 Event Rates

| \(\alpha\) | biased 8/32 | biased 4/32 | Median cross | Re-entry given cross |
| ---: | ---: | ---: | ---: | ---: |
| 1.0 | 41.67% | 45.83% | 5 | 100% |
| 0.5 | 3.13% | 4.17% | 8--9 | 100% |
| 0.25 | 0% | 0% | -- | -- |
| 0.125 | 0% | 0% | -- | -- |

H1 monotonicity and H2 critical interval both pass. The registered adjacent interval is \(1.0\rightarrow0.5\).

### 5.2 Final Routing

Every condition in both critical regimes ends with route NMI 1.0 and positive-margin rate 1.0. Final margin p05 is larger at half and quarter norm than at full norm.

## 6. Held-Out Budget Prediction

The primary held-out population contains 384 feature-regime-condition cells from seeds 16--31, with 11.72% event prevalence.

| Count / metric | Value |
| --- | ---: |
| True positive | 9 |
| False negative | 36 |
| True negative | 338 |
| False positive | 1 |
| True-positive rate | 0.200 |
| False-positive rate | 0.003 |
| Precision | 0.900 |
| Balanced accuracy | 0.599 |
| Ranking AUC | 0.978 |

The score is highly discriminative but the physical threshold 1 is miscalibrated. Post-hoc threshold tuning is not used to alter the registered H3 verdict.

## 7. Exact Event Budget

### 7.1 Full-Norm Crossed Cells

For the 84 full-norm cells crossing by step 50:

| Event time | Router | Representation | Interaction | Total |
| --- | ---: | ---: | ---: | ---: |
| crossing | 0.7477 | 0.2899 | 0.0072 | 1.0448 |
| re-entry | 0.5913 | 0.3018 | 0.0073 | 0.9005 |

Each value is normalized margin consumption relative to the initial pairwise margin. At crossing, the direct representation term supplies 27.7% of total consumption. Between crossing and re-entry, router consumption decreases by 0.1564; representation consumption increases by 0.0119. Direct center motion therefore does not produce the observed re-entry.

### 7.2 Half-Norm Crossed Cells

For the seven half-norm crossed cells:

| Event time | Router | Representation | Interaction | Total |
| --- | ---: | ---: | ---: | ---: |
| crossing | 0.6423 | 0.3806 | 0.0067 | 1.0296 |
| re-entry | 0.5876 | 0.3853 | 0.0066 | 0.9796 |

The same qualitative decomposition holds, though the event count is small.

## 8. Reconciliation With A06_02_04_E01

A06_02_04_E01 shows that allowing representation training is causally necessary to reproduce most joint recovery events compared with router-only training. A06_02_04_E03 shows that the direct center-motion term remains margin-consuming through re-entry under the raw-gradient update.

These statements are compatible. Representation learning can alter later hidden states, losses, expert-weighted outputs, and therefore future router gradients. Its total causal effect can be protective even when its direct algebraic center-motion term is harmful. The next anchor must separate this indirect gradient-shaping path from direct geometry.

## 9. Learning Guard Audit

The largest safe multiplier is 0.5.

| Quantity | Full norm | Half norm | Difference |
| --- | ---: | ---: | ---: |
| Mean final loss | \(4.19\times10^{-6}\) | \(4.50\times10^{-6}\) | +7.42% relative |
| Final accuracy | 1.0 | 1.0 | none |
| Final route NMI | 1.0 | 1.0 | none |
| Final positive-margin rate | 1.0 | 1.0 | none |

H4 formally fails because the protocol uses a 5% relative final-loss threshold. This metric is ill-conditioned near zero. Losses at steps 10, 20, and 50 are comparable and do not show consistent slower learning under half norm. Therefore the run cannot claim a meaningful learning-efficiency penalty or a clean learning-preservation pass.

## 10. Visualization Results

### Figure A: Scale Transition

![Scale transition](figures/scale_transition.png)

- **Question:** does event rate respond monotonically to a direction-fixed norm intervention?
- **Observed:** a sharp and replicated transition occurs between full and half norm.
- **Allowed conclusion:** router-update scale is causal.
- **Limitation:** critical value is interval-valued.

### Figure B: Held-Out Router Pressure

![Budget prediction](figures/budget_prediction.png)

- **Question:** does \(\rho^{router}\ge1\) predict held-out events?
- **Observed:** risk distributions separate, but most crossed cells remain below 1.
- **Allowed conclusion:** the statistic ranks risk but is not physically calibrated without representation terms.
- **Limitation:** boxplots do not define a transferable threshold.

### Figure C: Margin Trajectories

![Margin trajectories](figures/margin_trajectories.png)

- **Question:** how does the low-tail margin evolve under each norm scale?
- **Observed:** full norm briefly becomes negative; half and lower norms remain positive in the aggregate and end with larger margins.
- **Allowed conclusion:** scale reduction protects the controlled margin.
- **Limitation:** aggregate p05 hides the seven half-norm crossing cells.

## 11. Hypothesis Adjudication

| Hypothesis | Verdict | Reason |
| --- | --- | --- |
| H1 scale monotonicity | supported | both regimes satisfy endpoints and monotonic tolerance |
| H2 adjacent critical interval | supported | \(1.0\rightarrow0.5\) in both regimes |
| H3 held-out router-only threshold | rejected | balanced accuracy 0.599 and recall 0.200 |
| H4 relative terminal-loss guard | formally rejected | +7.42%, with near-zero metric caveat |

**Overall verdict:** scale transition supported; router-only controller not supported. The full conjunction required to authorize a method is not met.

## 12. Updated Mechanism

The early crossing mechanism is

\[
\text{large router update scale}
+\text{direct early representation consumption}
\rightarrow
\text{margin exhaustion}.
\]

Recovery in the raw-gradient surface is

\[
\text{future router correction}
\rightarrow
\text{re-entry},
\]

while representation learning may enable that correction indirectly by changing future router gradients.

## 13. Claim Boundary

**Established:** a direction-fixed causal scale transition; a strong but miscalibrated router-only risk ranking; direct representation contribution to early crossing; router-term correction at re-entry.

**Not established:** a usable threshold, meaningful LM-efficiency tradeoff, indirect recovery mechanism, native real-LLM controller, learned-expert utility, MTP benefit, or downstream value.

## 14. Next Decision

Use event-triggered branches cloned at the first crossing:

1. continue joint training;
2. freeze representation after crossing and continue router updates;
3. freeze router after crossing and continue representation updates;
4. record future router-gradient changes and exact direct margin terms.

This decides whether representation learning enables recovery indirectly through router-gradient shaping. A native-margin controller should not be designed until that missing budget is localized.

## 15. Artifact Map

- Anchor: `main/problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`
- Protocol: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E03_router_update_norm/protocol.md`
- Summary: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E03_router_update_norm/summary.md`
- Tables: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E03_router_update_norm/tables/`
- Figures: `main/experiments/A06/06_02_partition_preservation_dynamics/A06_02_04_E03_router_update_norm/figures/`
- Runner: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_36_router_update_norm_margin_budget.py`
- Config: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_36_router_update_norm_margin_budget.json`
- Submission: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_a06_36_router_update_norm_margin_budget_4gpu_acp.sh`
- Raw results: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_36_router_update_norm_margin_budget/a06_36_full_4gpu_20260710_01/`
- ACP job: `pt-114g2p4y`

```bash
A0636_ALLOW_REAL_SUBMIT=1 RUN_NAME=a06_36_full_4gpu_20260710_01 bash scripts/submit_a06_36_router_update_norm_margin_budget_4gpu_acp.sh
```
