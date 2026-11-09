# Detailed: A11_04 K=3 First-Informative-Horizon

Status: completed and merged. A11_04 now owns both the decision-only mechanism run and the all-position LM-style control. The old `A11_04_02_k3_all_position_control` folder is retained as an original run archive, not as a separate research question.

## Decision

A11_04 supports the first-informative-horizon mechanism as a direct single-prefix statement. In clean $\tau=3$, the decision-only objective shows the intended separation: K=1/K=2 remain at chance-level guarded recovery, while K=3 recovers the early variable $Z$ because it is the first condition whose active target includes $Y_3=S_Z$.

The all-position control refines the boundary. K=3 remains strongest, but K=1/K=2 also become branch-readable because losses at other sequence positions can update shared parameters. Therefore the combined result supports direct representation supervision, not the stronger claim that non-covering horizons cannot recover $Z$ in LM-style training.

## Terminology / Definitions

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | What it cannot prove |
| --- | --- | --- | --- | --- | --- |
| $Z$ | early branch variable | branch index in `BR_z` | categorical | delayed cause | natural-language semantics |
| $\tau$ | first informative horizon | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | future token offset | core mechanism variable | fixed horizon in real text |
| covering condition | objective includes $\tau$ | K=3 in clean $\tau=3$ | Boolean | receives direct branch-specific target | optimization guarantee |
| non-covering condition | objective stops before $\tau$ | K=1/K=2 in clean $\tau=3$ | Boolean | lacks direct $S_Z$ target at $h_T$ | no indirect transfer |
| decision-only scope | loss only at the target decision prefix | $L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j,Y_j)$ | CE | isolates theorem object | LM-style training behavior |
| all-position scope | loss at every valid sequence position | $\sum_t\sum_j\lambda_j\operatorname{CE}(q_j(h_t),X_{t+j})$ | CE | tests robustness boundary | direct cause of $h_T$ information |
| $Q_K$ | guarded branch-recovery score | $\min\{A_K,P_K,S_K\}$ | 0 to 1 | primary recovery evidence | full causal proof |
| coverage gap | K=3 recovery gap over K=1/K=2 | $\operatorname{AUC}_Q(3)-\max\{\operatorname{AUC}_Q(1),\operatorname{AUC}_Q(2)\}$ | score | primary pass/fail metric | universal scaling |

## Theory Clause Tested

The clean construction is:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

The information relation is:

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

Thus:

$$
\tau=3.
$$

Decision-only objective:

$$
L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
$$

For $K<3$, the active targets contain no branch-specific loss at $h_T$. For $K=3$, the term

$$
\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)
$$

directly penalizes a $Z$-blind $h_T$.

All-position objective:

$$
L_K^{\mathrm{all}}=\sum_t\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_t),X_{t+j}).
$$

This changes the mechanism object because later sequence positions can carry branch information and update shared parameters.

## Data Audit

Representative generated rows:

| Regime | Branch | Prefix | Targets |
| --- | ---: | --- | --- |
| clean $\tau=3$ | 0 | `BR_0 F_00 ... F_15 U_00 U_01 U_02 U_03` | `A_SHARED C_SHARED S_0` |
| clean $\tau=3$ | 1 | `BR_1 F_00 ... F_15 U_00 U_01 U_02 U_03` | `A_SHARED C_SHARED S_1` |
| noisy horizon-3 | 0 | `BR_0 F_00 ... F_15 U_00 U_01 U_02 U_03` | `A_SHARED C_SHARED NOISE_12` |
| redundant horizon-3 | 0 | `BR_0 F_00 ... F_15 U_00 U_01 U_02 U_03` | `A_SHARED S_0 T_0` |

## Shared Experimental Setup

| Item | Value |
| --- | --- |
| Model | one-layer one-head Transformer |
| Hidden size | `d_model=64` |
| Branches | `4` |
| Filler length | `16` |
| Shared context length | `4` |
| Max horizon | `3` |
| Seeds | `971,972,973,974,975` |
| Initializations | `identical_branch`, `random` |
| Conditions | `K1_fixed_3head`, `K2_active`, `K3_active` |
| Regimes | `clean_tau3`, `noisy_h3`, `redundant_h3` |
| Training steps | `15000` |
| Eval interval | `500` |
| Decision-only job | `pt-a140a1iu` |
| All-position job | `pt-f5hhx4a6` |

## Main Tables

### Decision-only clean $\tau=3$

| Init | K | n | Mean reached step | Reach rate | AUC $Q$ | Final $Q$ | Eval suffix | Probe | Swap | $Y_1$ acc | $Y_2$ acc | Native informative acc |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| identical | 1 | 5 | NA | 0.00 | 0.250 | 0.250 | 0.250 | 0.250 | 0.250 | 1.000 | 0.000 | NA |
| identical | 2 | 5 | NA | 0.00 | 0.250 | 0.250 | 0.250 | 0.250 | 0.250 | 1.000 | 1.000 | NA |
| identical | 3 | 5 | 3333 | 0.60 | 0.665 | 0.800 | 0.800 | 0.800 | 0.800 | 1.000 | 1.000 | 0.800 |
| random | 1 | 5 | NA | 0.00 | 0.266 | 0.250 | 0.250 | 0.250 | 0.250 | 1.000 | 0.000 | NA |
| random | 2 | 5 | NA | 0.00 | 0.271 | 0.250 | 0.250 | 0.250 | 0.250 | 1.000 | 1.000 | NA |
| random | 3 | 5 | 1000 | 0.40 | 0.735 | 0.750 | 0.750 | 0.750 | 0.750 | 1.000 | 1.000 | 0.750 |

Decision-only coverage contrasts:

| Init | Coverage gap AUC $Q$ | Coverage gap final $Q$ | K=1 AUC | K=2 AUC | K=3 AUC |
| --- | ---: | ---: | ---: | ---: | ---: |
| identical | +0.415 | +0.550 | 0.250 | 0.250 | 0.665 |
| random | +0.465 | +0.500 | 0.266 | 0.271 | 0.735 |

### All-position clean $\tau=3$

| Init | K | n | Mean reached step | Reach rate | AUC $Q$ | Final $Q$ | Eval suffix | Probe | Swap | $Y_1$ acc | $Y_2$ acc | Native informative acc |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| identical | 1 | 5 | 1833 | 0.60 | 0.823 | 0.700 | 0.850 | 0.800 | 0.850 | 1.000 | 0.000 | NA |
| identical | 2 | 5 | 1500 | 0.40 | 0.715 | 0.700 | 0.700 | 0.800 | 0.700 | 1.000 | 1.000 | NA |
| identical | 3 | 5 | 1500 | 1.00 | 0.976 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| random | 1 | 5 | 1000 | 0.80 | 0.942 | 0.950 | 1.000 | 0.950 | 1.000 | 1.000 | 0.000 | NA |
| random | 2 | 5 | 1000 | 0.80 | 0.942 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | NA |
| random | 3 | 5 | 1000 | 1.00 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

All-position coverage contrasts:

| Init | Coverage gap AUC $Q$ | Final $Q$ gap | K=1 AUC | K=2 AUC | K=3 AUC |
| --- | ---: | ---: | ---: | ---: | ---: |
| identical | +0.153 | +0.300 | 0.823 | 0.715 | 0.976 |
| random | +0.058 | +0.000 | 0.942 | 0.942 | 1.000 |

## Control Results

Decision-only controls:

| Regime | Observation | Interpretation |
| --- | --- | --- |
| clean $\tau=3$ | K=3 beats K=1/K=2; K=1/K=2 stay at chance | supports direct first-informative-horizon coverage |
| noisy horizon-3 | K=3 shows weak transient threshold hits but final $Q$ remains low | threshold reach alone is unsafe |
| redundant horizon-3 | K=2 improves when $Y_2=S_Z$ | earlier branch-revealing targets explain recovery |

All-position controls:

| Regime | Observation | Interpretation |
| --- | --- | --- |
| clean $\tau=3$ | K=3 strongest, but K=1/K=2 high | indirect shared-parameter transfer exists |
| noisy horizon-3 | noisy random K=1/K=2/K=3 AUC $Q=0.798/0.932/0.913$ | high all-position $Q$ can be a false positive for active-horizon coverage |
| redundant horizon-3 | K=2 and K=3 both high | redundant earlier information explains recovery |

## Hypothesis Audit

| Hypothesis | Decision-only judgment | All-position judgment | Combined status |
| --- | --- | --- | --- |
| K=3 helps when it covers $\tau$ | supported | K=3 remains strongest | supported for direct supervision |
| K=1/K=2 remain low when $K<\tau$ | supported | falsified | true only in isolated decision-prefix scope |
| local targets are preserved | supported | supported | supported |
| high $Q$ implies active-horizon coverage | guarded | falsified | not valid under all-position |

## Visualization Results

No standalone figure is promoted. The central evidence is the pair of clean result tables and the two coverage-contrast tables. They answer two linked questions:

1. Decision-only: does covering $\tau$ create the expected direct branch recovery? Yes.
2. All-position: does this clean separation survive LM-style training? No; K=1/K=2 can recover $Z$ indirectly.

These tables do not prove natural-language transfer, broad next-K scaling, or learning-efficiency advantage.

## Interpretation

A11_04 should be read as one experiment with two scopes:

1. Scope A isolates the theorem object. It shows that when $Y_1,Y_2$ are shared and $Y_3=S_Z$, K=3 is the first objective that directly forces $h_T$ to carry $Z$.
2. Scope B tests the boundary under a more language-model-like objective. It shows that all-position training can create a separate path for $Z$ to enter $h_T$, even when the decision-prefix active horizon does not cover $\tau$.

The right story is therefore not "only MTP can learn long-horizon semantics." The right story is: MTP has a provable direct representation-supervision advantage when it covers future tokens containing new information about an early variable. Whether that direct supervision yields faster or more robust learning remains the next empirical question.

## Claim Boundary

Can claim:

- controlled first-informative-horizon coverage is supported in decision-only K=3;
- K=3 improves recoverability of $Z$ when $Y_3$ is the first branch-informative target;
- all-position K=3 remains strongest in the clean condition;
- all-position K=1/K=2 recovery shows indirect transfer, not failure of the theorem.

Cannot claim:

- broad next-K scaling;
- curriculum advantage;
- natural-language long-horizon improvement;
- that non-covering horizons can never recover $Z$ under all-position training;
- that efficiency advantage is already established.

## Artifact Map

| Artifact | Path |
| --- | --- |
| Primary protocol | `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/protocol.md` |
| Primary summary | `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/summary.md` |
| Primary detailed | `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/detailed.md` |
| Original all-position archive | `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/` |
| Runner | `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py` |
| Decision-only config | `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_04_k3_first_informative_horizon.json` |
| All-position config | `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_04_k3_first_informative_horizon_all_positions.json` |
| Decision-only result dir | `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_04_k3_first_informative_horizon/a11_04_k3_first_informative_decision_only_4gpu_20260707_1718` |
| All-position result dir | `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_04_k3_first_informative_horizon_all_positions/a11_04_02_k3_all_positions_4gpu_20260708_0015` |
| Decision-only tables | `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/tables/condition_summary.csv` |
| All-position tables | `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/tables/all_position_condition_summary.csv` |
| Decision-only remote job | `pt-a140a1iu` |
| All-position remote job | `pt-f5hhx4a6` |

## Next Decision

The next experiment should test efficiency under LM-style training. The minimal decision-bearing comparison is whether covering the first informative future token reduces time-to-threshold $T_\theta$ or improves early AUC of $Q_K(t)$ while preserving next-token loss.
