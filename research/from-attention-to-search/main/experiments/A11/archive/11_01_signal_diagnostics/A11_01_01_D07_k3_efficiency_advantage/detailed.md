# Detailed Record: A11_04_03 K=3 Efficiency Advantage

## 1. Decision Record

This experiment was run to test whether the theory-proven direct representation-supervision advantage becomes a learning-efficiency advantage. The result is a qualified positive:

- decision-only clean $\tau=3$: supported;
- all-position clean $\tau=3$: K=3 remains strongest, but K=1/K=2 also recover through indirect paths;
- noisy all-position control: false-positive recovery exists, so all-position evidence must be interpreted cautiously;
- gradient usefulness: insufficient as a causal explanation.

Strict protocol result: partial pass, not full pass.

## 2. Terminology / Definitions

| Term | Plain meaning | Computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| $Z$ | early semantic variable | branch identity in the prefix | discrete branch label | target of long-horizon learning | natural-language meaning |
| $\tau$ | first informative horizon | first future offset where target depends on $Z$ | $\tau=3$ in clean data | determines whether K covers useful target | universal MTP rule |
| K | prediction horizon | active future offsets in the loss | K=1,2,3 | intervention variable | model capacity alone |
| $h_T$ | decision hidden state | transformer hidden state at decision prefix | vector | representation being audited | full sequence behavior |
| $Q$ | guarded semantic recovery | min of suffix accuracy, branch probe, branch swap consistency | score in $[0,1]$ | main recovery metric | strict causality |
| $T_\theta$ | reliable time-to-threshold | first time $Q\ge0.9$ for 2 evals | training steps | main efficiency metric | final convergence |
| early AUC | early trajectory area | normalized AUC over steps 0-3000 | score area | speed and stability | causal gradient |
| local-loss guard | local target protection | $Y_1/Y_2$ loss and accuracy | CE / accuracy | rules out local tradeoff | semantic mechanism |
| gradient usefulness | forward-looking gradient audit | compare $c,r,\rho$ with future $\Delta Q$ | correlation / score delta | tests optimization explanation | proof by itself |

## 3. Theoretical Context

The clean construction is:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

The information structure is:

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)>0.
$$

Thus the first future target that reveals $Z$ is $\tau=3$. K=1 and K=2 do not include this target at the decision prefix. K=3 includes:

$$
\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z).
$$

The previous theory proves a representational requirement: if K covers $\tau$ and the offset-$\tau$ loss is low, then $h_T$ must contain information about $Z$. This experiment asks whether that requirement also makes learning faster.

## 4. Implementation Contract

Experiment code:

`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py`

Config:

`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_04_03_k3_efficiency_advantage.json`

Run name:

`a11_04_03_k3_efficiency_advantage_4gpu_20260708_0110`

Remote job:

`pt-q3l79ir6`

Resource:

reserved 4-GPU worker, `n6ls.iu.i40.4`.

Raw result directory:

`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_04_03_k3_efficiency_advantage/a11_04_03_k3_efficiency_advantage_4gpu_20260708_0110`

Curated result directory:

`/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_04_03_k3_efficiency_advantage`

## 5. Experimental Matrix

Seeds: `971, 972, 973, 974, 975`.

Objectives:

- decision-only;
- all-position LM-style control.

Data regimes:

- clean $\tau=3$: $Y_1=A$, $Y_2=C$, $Y_3=S_Z$;
- noisy horizon-3: $Y_3\perp Z$;
- redundant horizon-3: $Y_2=S_Z$.

Conditions:

- K=1: active $Y_1$;
- K=2: active $Y_1,Y_2$;
- K=3: active $Y_1,Y_2,Y_3$.

Initializations:

- `identical_branch`;
- `random`.

Completeness audit:

| Expected | Observed | Status |
| --- | ---: | --- |
| 180 training runs | 180 unique runs | pass |
| 10980 evaluation rows | 10980 rows | pass |
| 27720 gradient profile rows | 27720 rows | pass |
| 36 condition summaries | 36 rows | pass |
| 1512 gradient usefulness summaries | 1512 rows | pass |

## 6. Main Tables

Curated tables:

- `tables/condition_summary.csv`
- `tables/decision_contrasts.csv`
- `tables/efficiency_summary.csv`
- `tables/local_loss_guard_summary.csv`
- `tables/gradient_profile_summary.csv`
- `tables/gradient_usefulness_summary.csv`
- `tables/sample_table.csv`

## 7. Efficiency Results

### 7.1 Decision-Only Clean $\tau=3$

| init | K | reach rate | mean $T_\theta$ reached-only | early AUC | full AUC | final $Q$ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| identical | K=1 | 0.00 | NA | 0.250 | 0.250 | 0.250 |
| identical | K=2 | 0.00 | NA | 0.250 | 0.250 | 0.250 |
| identical | K=3 | 0.60 | 2167 | 0.537 | 0.671 | 0.800 |
| random | K=1 | 0.00 | NA | 0.277 | 0.255 | 0.250 |
| random | K=2 | 0.00 | NA | 0.281 | 0.255 | 0.250 |
| random | K=3 | 0.40 | 0 | 0.644 | 0.728 | 0.750 |

Interpretation: K=3 is the only condition that reliably moves beyond chance-level guarded recovery. This supports direct-supervision efficiency at the decision prefix.

### 7.2 All-Position Clean $\tau=3$

| init | K | reach rate | mean $T_\theta$ reached-only | early AUC | full AUC | final $Q$ |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| identical | K=1 | 0.80 | 375 | 0.838 | 0.834 | 0.850 |
| identical | K=2 | 0.60 | 333 | 0.771 | 0.731 | 0.850 |
| identical | K=3 | 1.00 | 300 | 0.965 | 0.993 | 1.000 |
| random | K=1 | 1.00 | 1000 | 0.956 | 0.935 | 0.950 |
| random | K=2 | 0.80 | 0 | 0.952 | 0.929 | 0.950 |
| random | K=3 | 1.00 | 0 | 1.000 | 1.000 | 1.000 |

Interpretation: K=3 remains strongest. However, all-position losses provide indirect paths for K=1/K=2, so the all-position result cannot support an exclusivity claim.

## 8. Controls

### 8.1 Noisy Control

Decision-only noisy control protects the core mechanism: K=3 does not reproduce clean recovery. Final $Q$ is 0.25 under identical initialization and 0.30 under random initialization.

All-position noisy control weakens the strict protocol because false-positive recovery appears. Under random initialization, noisy all-position early AUC is high for all K: K=1/K=2/K=3 = 0.958/0.946/0.985.

Interpretation: all-position $Q$ can reflect indirect transfer or initialization-dependent recovery even when the horizon-3 target is not informative. This is a boundary condition, not a rejection of the decision-only mechanism.

### 8.2 Redundant Control

Redundant all-position results behave as expected. When $Z$ appears earlier through $Y_2=S_Z$, K=2 and K=3 both reach near-perfect recovery. This supports the information-structure story: the useful variable is where target information enters, not the label K=3 by itself.

## 9. Local-Loss Guard

K=3 preserves the active local targets. In clean decision-only and all-position, K=3 has final $Y_1$ and $Y_2$ accuracy equal to 1.00 with near-zero loss.

K=1 has inactive $Y_2$, so K=1's $Y_2$ loss is not evidence of local-target failure. The meaningful local guard compares active targets, especially K=2 vs K=3.

## 10. Gradient Diagnostics

At profiling steps, the audit computes:

$$
g_1=\nabla_\theta L_1,\qquad g_\tau=\nabla_\theta L_\tau.
$$

and logs:

$$
c=\frac{\langle g_1,g_\tau\rangle}{\|g_1\|\|g_\tau\|},
$$

$$
r=\frac{\|g_\tau\|}{\|g_1\|},
$$

$$
\rho=\frac{\langle g_1+\lambda g_\tau,g_1\rangle}{\|g_1\|^2}.
$$

The forward-looking audit compares these values with:

$$
\Delta Q_\Delta(t)=Q(t+\Delta)-Q(t),\qquad \Delta\in\{500,1000,2000\}.
$$

Main observation: the gradient audit does not yet give a stable causal explanation. Clean K=3 all-position identical-branch has supportive signals in all-parameters and shared-MLP groups, but shared attention is mixed and random initialization is often already saturated. Decision-only gradients are also mixed.

Therefore the correct claim is: the extra horizon gives a direct supervised target; whether its gradient is predictively useful in a simple universal way remains unproven.

## 11. Visualization Results

### Clean Q Curves

![Clean Q curves](figures/clean_q_curves.png)

Question answered: Does K=3 recover $Z$ earlier than K=1/K=2 in clean $\tau=3$?

How to read: Each panel averages $Q(t)$ over 5 seeds. The dashed line is the threshold $Q=0.9$.

Observed result: In decision-only, K=1/K=2 stay near chance while K=3 rises. In all-position, all conditions can rise, but K=3 is highest and most stable.

Take-home: Direct-supervision efficiency is clear in decision-only and visible but not exclusive in all-position.

Limitation: This figure does not prove the gradient cause of the improvement.

### Noisy All-Position Curves

![Noisy all-position Q curves](figures/noisy_all_position_q_curves.png)

Question answered: Does all-position training produce false-positive semantic recovery when horizon 3 is not informative?

Observed result: Yes, especially under random initialization.

Take-home: all-position recovery must be interpreted with controls; final or early $Q$ alone is not enough.

Limitation: This does not invalidate the clean decision-only construction.

### Local-Loss Guard

![Local loss guard](figures/local_loss_guard_y1.png)

Question answered: Does K=3 hurt the local shared next-token target?

Observed result: No. K=3 keeps $Y_1$ loss near zero.

Take-home: K=3's semantic gain is not explained by sacrificing local $Y_1$ learning.

Limitation: This plot focuses on $Y_1$ because K=1 does not actively train $Y_2$.

### Gradient Usefulness

![Gradient usefulness audit](figures/gradient_usefulness_clean_h3.png)

Question answered: Does gradient ratio $r$ alone explain future $\Delta Q$?

Observed result: No. The relation is mixed across scopes, groups, and initializations.

Take-home: gradient usefulness needs a sharper mechanistic statistic before it can support a strong optimization claim.

Limitation: Scatter is descriptive; it is not an intervention on the gradient.

## 12. Hypothesis Table

| Hypothesis | Verdict | Evidence | Boundary |
| --- | --- | --- | --- |
| H1: K=3 is earlier in decision-only clean $\tau=3$ | supported | K=1/K=2 reach rate 0; K=3 reach rate 0.40-0.60 and higher early AUC | seed count is 5 |
| H2: K=3 preserves local targets | supported | active $Y_1/Y_2$ accuracy 1.00 | K=1 inactive $Y_2$ is not comparable |
| H3: all-position K=3 is earlier/stronger | partial | K=3 has best clean AUC/final $Q$ | noisy all-position false positives weaken specificity |
| H4: extra-horizon gradient explains later $Q$ | insufficient | mixed correlations and group patterns | needs sharper gradient intervention or statistic |

## 13. Claim Boundary

Supported claim:

In a controlled first-informative-horizon construction, MTP with K covering $\tau$ can be more learning-efficient than non-covering K because it directly supervises the current hidden state with the first future token that contains $Z$.

Weakened or unsupported claims:

- MTP is already proven better for natural language;
- K=3 is always better than K=1/K=2;
- all-position non-covering objectives cannot recover $Z$;
- gradient cosine or gradient norm ratio alone proves useful optimization direction.

## 14. Next Decision

The next theory question should be:

Under what optimization assumptions does direct horizon coverage reduce learning time or sample complexity?

The next experiment should not simply increase K. It should first isolate whether the efficiency comes from direct supervised signal strength, reduced credit-assignment distance, or gradient routing through shared parameters.
