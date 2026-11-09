# Detailed Record: A06_03_01_E02 Specialist-Generalist Router Release

## 0. Decision Recap

**Question:** When representation and router start identically, does replacing
load-matched generalists with learned specialists cause larger native
weighted-top-1 margin growth while preserving lower task loss?

**Formal result:** Specialists preserve lower task loss, but their margin grows
less. Router-only SGD gives \(D_m(50)=-0.00324\) with seed-clustered 95% CI
\([-0.00413,-0.00245]\). The generalist-minus-specialist task-loss difference is
0.9125 nats/task-token with 95% CI \([0.8905,0.9438]\).

**Refined interpretation:** The registered operational mismatch is real, but it
does not establish failed route correction. The useful expert is already top-1.
Counterfactual utility compares expert identity, whereas margin growth changes
the probability of the selected identity. The experiment therefore closes the
correct-route confidence audit and motivates a wrong-rank correction test.

## 1. Definitions

| Object | Definition | Unit | Decision role | Limitation |
| --- | --- | --- | --- | --- |
| \(G_f^{cf}\) | \(\min_{b\ne f}(L_{f,b}^{cf}-L_{f,f}^{cf})\) | nats/task-token | expert-identity utility | not confidence sensitivity |
| \(m_f(t)\) | assigned score minus closest competitor score | logit margin | route confidence | center statistic |
| \(D_m(T)\) | median paired specialist-minus-generalist margin growth | logit margin | registered primary metric | correct-route start only |
| \(E_f(t)\) | \(L_f^{native}(t)-L_{f,f}^{cf}(t)\) | nats/task-token | routing excess | can be negative numerically near zero |
| \(R_f(t)\) | \(E_f(t)/E_f(0)\) | ratio | relative routing efficiency | not wall-clock efficiency |
| Route NMI | normalized mutual information between task and selected expert | ratio | identity preservation guard | no functional value |

## 2. Data Construction

The vocabulary has four instruction tokens, four content tokens, and four
output tokens. Task \(f\in\{0,1,2,3\}\) defines

\[
y=(c+f)\bmod4.
\]

Each length-33 sequence is

```text
[instruction, content_1, output_1, ..., content_16, output_16]
```

All 32 autoregressive targets enter training. The sixteen content predictors
are task-dependent positions. Each seed contains 32 training and 32 disjoint
held-out sequences, balanced across tasks.

## 3. Model And Training

The model is the A06_03_01_E01 known-good context bridge:

- hidden dimension 64 and four attention heads;
- one causal attention layer initialized as causal averaging;
- a fixed instruction-state visibility control;
- residual plus LayerNorm and no learned positional embedding;
- four MLP experts of hidden width 128;
- fixed readout;
- weighted top-1 routing with softmax probability multiplying the selected
  expert output.

### 3.1 Exposure reconstruction

A06_03_01_E01 did not save checkpoints, so each seed deterministically rebuilds them
from its original initialization.

| Start | Assignment during 200 updates | Trainable block | Expected function |
| --- | --- | --- | --- |
| Specialist | task \(f\) always forced to expert \(f\) | experts only | one useful expert per task |
| Generalist | cyclic balanced task-expert shuffle | experts only | interchangeable experts |

Both use full-sequence loss and expert AdamW at 0.001. The router and
representation remain unchanged. Each expert receives equal total updates, and
every task-expert pair in the generalist condition receives equal updates.

### 3.2 Router release

After exposure, the forced assignment is removed. Every release optimizer
starts with empty state; exposure AdamW moments are not transferred.

| Mode | Trainable blocks | Learning rates | Role |
| --- | --- | --- | --- |
| Router-only SGD | router | \(10^{-4}\) | primary local causal surface |
| Router-only AdamW | router | 0.001 | optimizer transfer |
| Joint AdamW | router, experts, representation | 0.001, 0.001, 0.0005 | secondary native-training bridge |

Release lasts 50 updates. Checkpoints are 0, 1, 2, 5, 10, 20, and 50.

## 4. Exact Mechanism Measurements

For the currently closest competitor \(b\), pair margin is

\[
m_{f,b}(t)=(w_f(t)-w_b(t))^\top\mu_f(t).
\]

The finite-step identity is evaluated in float64:

\[
\Delta m
=(\Delta w_f-\Delta w_b)^\top\mu_f
+(w_f-w_b)^\top\Delta\mu_f
+(\Delta w_f-\Delta w_b)^\top\Delta\mu_f.
\]

Maximum closure error is \(7.02\times10^{-8}\). This validates measurement, not
causal attribution. The frozen router-only intervention supplies the causal
comparison.

At release start, the task-specific margin pressure is

\[
P_{f,b}=-\langle g_f-g_b,\mu_f\rangle.
\]

For weighted top-1 selected expert \(r\),

\[
\Delta w_j
=\frac{\eta}{\tau}p_r(\mathbf1[j=r]-p_j)B_rh,
\qquad
B_r=-\langle\nabla_{\hat y}\ell,E_r(h)\rangle.
\]

This update depends on the selected expert and residual task gradient. It does
not contain the unselected expert's own counterfactual loss.

## 5. Protocol Compliance

| Guard | Formal result | Status |
| --- | ---: | --- |
| Completed seeds | 32 | pass |
| Primary paired cells | 128 | pass |
| Specialist median utility gap | 8.8947 | pass, threshold 5 |
| Generalist median utility gap | -0.0042 | pass, absolute threshold 0.5 |
| Max non-expert state error | 0 | pass |
| Max router state error | 0 | pass |
| Max representation state error | 0 | pass |
| Max initial paired route-state spread | 0 | pass |
| Minimum initial route NMI | 0.999999999994 | pass |
| Generalist task-expert count spread | 0 | pass |
| Max finite-step closure error | \(7.02\times10^{-8}\) | pass |
| Finite trajectory | complete | pass |

The formal run is valid. The first local smoke was excluded because float32
subtraction produced a closure diagnostic of \(2.51\times10^{-4}\). Recomputing
the same identity from the same tensors in float64 reduced the error without
changing training. Smoke run 02 passed. A one-seed full-horizon audit passed all
guards except the intentionally unmet 32-seed coverage requirement.

## 6. Primary Results

### 6.1 Router-only SGD

| Checkpoint | Specialist margin growth | Generalist margin growth | Contrast | Specialist loss | Generalist loss | Specialist \(R_f\) | Generalist \(R_f\) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0.8404 | 1.8105 | 1.0000 | 1.0000 |
| 10 | 0.02108 | 0.02156 | -0.00047 | 0.7943 | 1.7530 | 0.9461 | 0.9681 |
| 20 | 0.04159 | 0.04266 | -0.00105 | 0.7512 | 1.7012 | 0.8954 | 0.9373 |
| 50 | 0.10031 | 0.10337 | -0.00324 | 0.6441 | 1.5576 | 0.7612 | 0.8513 |

The margin contrast becomes steadily negative, but both margins increase and
route NMI remains 1. The specialist has lower absolute loss at every checkpoint
and a smaller normalized routing excess at update 50.

The horizon-normalized trapezoidal area under \(R_f(t)\) is 0.8757 for specialists
and 0.9239 for generalists; lower is faster. Neither reaches \(R_f\le0.1\) under
the deliberately small SGD step within 50 updates.

### 6.2 Router-only AdamW

At update 50:

- specialist margin growth: 1.1752;
- generalist margin growth: 1.2253;
- paired contrast: -0.04668, 95% CI \([-0.05474,-0.03562]\);
- specialist task loss: 0.0302;
- generalist task loss: 0.2911;
- normalized routing excess: 0.0334 versus 0.1202.

AdamW preserves the negative contrast sign and amplifies its scale. Specialists
reach \(R_f\le0.1\) at checkpoint 50; generalists do not. This shows optimizer
scale changes trajectory speed but not the identity-utility/confidence-growth
separation on the frozen path.

### 6.3 Joint AdamW

At update 50, specialist and generalist losses are 0.000467 and 0.001763. Margin
growth is 0.7760 and 0.7722. The paired contrast is 0.00013 with 95% CI
\([-0.00465,0.00770]\) and is unresolved. Specialists reach \(R_f\le0.1\) at
checkpoint 10 and generalists at checkpoint 20.

Because expert and representation functions change, this condition cannot
identify a router-only transmission law. It only shows that joint optimization
can solve both starts on the controlled task.

## 7. Pressure And Movement

| Quantity | Specialist | Generalist |
| --- | ---: | ---: |
| Pre-release task-gradient pressure, median | 121.9420 | 146.9933 |
| First SGD step pair-margin movement, median | 0.0021479 | 0.0021751 |

The ordering from A06_03_01_E01 survives in realized movement but with much smaller
absolute separation. The plausible explanation is residual-error scaling:
generalists begin with higher loss and receive larger selected-expert pressure.
This is consistent with the formula but is not a complete mediation proof.

## 8. Visualization Results

### Figure 1: Margin-Growth Contrast

![Margin-growth contrast](figures/margin_growth_contrast.png)

- **Plot contract:** paired seed-task contrast, seed-clustered bootstrap bands,
  logit-margin units, checkpoints aggregated by median.
- **Allowed conclusion:** the specialist/generalist confidence-growth ordering.
- **Observed:** frozen-router paths are negative; joint path is transiently
  positive and unresolved by update 50.
- **Not allowed:** route collapse or wrong-route correction.

### Figure 2: Native Task Value And Normalized Routing Excess

![Task value and routing efficiency](figures/task_loss_and_routing_efficiency.png)

- **Plot contract:** primary SGD condition only; loss is nats/task-token;
  normalized excess uses each condition's forced floor.
- **Observed:** specialists remain lower-loss and close more proportional excess.
- **Not allowed:** throughput or activated-compute advantage.

### Figure 3: Pressure And First-Step Movement

![Pressure and movement](figures/pressure_actual_movement.png)

- **Plot contract:** one point per task-seed cell at release start; x is held-out
  task-specific raw pressure; y is actual first-step pair-margin change under
  the full training batch.
- **Observed:** generalists have larger pressure and slightly larger movement.
- **Not allowed:** exact mediation or identification of an unselected expert.

## 9. Hypothesis Adjudication

| Hypothesis | Verdict | Direct basis | Refined boundary |
| --- | --- | --- | --- |
| H1 specialists retain task value | supported | task-loss CI lower bound \(>0\) | controlled task |
| H2 specialists receive larger route growth | rejected | \(D_m\) CI upper bound \(<0\) | correct top-1 start |
| H3 operational transmission mismatch | supported | H1 passes and H2 reverses | confidence calibration, not correction failure |
| H4 AdamW preserves the sign | supported | AdamW contrast CI below zero | empty AdamW state at release |
| H5 joint transfer preserves sign | not supported | joint CI crosses zero | all blocks trainable |

## 10. Updated Theory

The previous story merged two different router contracts:

1. **Correct-identity confidence calibration:** given selected useful expert
   \(r=f\), how much should \(p_f\) increase?
2. **Useful-identity discovery:** given useful expert \(f\) is unselected, how does
   the router learn that \(f\) is better than the selected expert?

A06_03_01_E02 closes the first contract on the controlled task. Ordinary weighted
top-1 preserves the correct identity and decreases task loss. Its confidence
growth follows the selected path's residual pressure, not the full
counterfactual identity gap. This is not itself defective because a solved
specialist may require less absolute confidence movement.

The architectural information gap remains in the second contract. In the
active top-1 region, an unselected expert's own output does not enter the
forward loss, so its utility is not directly compared. A06_02_03_E02 showed
rank-mediated correction with fixed oracle experts; the next experiment must
test the same mechanism with learned specialists, full-sequence LM loss, and
context-defined tasks.

## 11. Claim Boundary

**Established:** specialists and generalists can be compared from exactly the
same non-expert state; specialists preserve task value; confidence growth is
not monotonic in expert-identity utility; no route collapse occurs over 50
updates; optimizer choice changes scale; joint training erases the contrast.

**Not established:** wrong-route correction, label-free feature discovery,
natural-language semantic routing, sparse-compute system gain, downstream
generalization, or an optimal new gating rule.

## 12. Next Decision

Use the same learned specialist checkpoints but initialize the function-matched
expert at controlled score rank 1, 2, or 4. Freeze experts and representation,
train the router with native full-sequence loss, and measure:

- first sustained recovery of the function-matched expert;
- cumulative native task regret above its forced floor;
- number of score-boundary changes;
- useful-expert probability before and after first selection;
- soft-mixture control in which all experts receive utility-bearing forward
  weight.

The decision is whether learned-specialist correction is rank-mediated under
weighted top-1. A new utility-aware gate is justified only if native top-1 is
slow or fails while the all-expert utility-bearing control corrects reliably.

## 13. Artifact Map

| Artifact | Location |
| --- | --- |
| Anchor | `../../../../problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md` |
| Protocol | `protocol.md` |
| Formal run | `a06_39_full_4gpu_20260710_01` |
| ACP job | `pt-kwdo6x9l` (`SUCCEEDED`) |
| Runner | `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_39_specialist_generalist_router_release.py` |
| Config | `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_39_specialist_generalist_router_release.json` |
| Submitter | `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_a06_39_specialist_generalist_router_release_4gpu_acp.sh` |
| Raw result root | `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_39_specialist_generalist_router_release/a06_39_full_4gpu_20260710_01/` |
| Curated table | `tables/paired_summary.csv` |
| Decision record | `tables/decision_summary.json` |
| Curated figures | `figures/` |

Formal shards covered seeds 0--31 across four H100 GPUs. The formal run
reconstructed exposure, released all six conditions, wrote all four partial
table families, aggregated them, and passed every registered guard.

