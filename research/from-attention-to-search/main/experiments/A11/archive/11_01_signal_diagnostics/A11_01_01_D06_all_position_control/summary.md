# Summary: A11_04_02 K=3 All-Position Control

Status: completed on 2026-07-08 with reserved 4-GPU remote job `pt-f5hhx4a6`.

## What We Established

All-position training changes the mechanism object. In the original decision-only setup, K=1/K=2 had no active branch-specific target at the decision prefix, so K=3 was the first condition that recovered $Z$. Under all-position LM-style loss, K=1 and K=2 also become branch-readable at the decision prefix, even in clean $\tau=3$ where their active decision-prefix targets are not branch-informative.

Therefore the all-position control weakens the strong claim "only covering $\tau$ can recover $Z$." The supported refined claim is: K=3 remains the cleanest and strongest direct-supervision condition, but all-position background losses and shared parameters can transmit branch information into $h_T$ even for non-covering conditions.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| all-position LM-style loss | Train offset heads at every valid sequence position | for horizon $j$, predict $X_{t+j}$ from all valid $t$ | tests robustness beyond decision-only | natural-language transfer |
| decision prefix $h_T$ | hidden state before `A_SHARED C_SHARED S_z` | same evaluation point as A11_04 | keeps metric comparable | all hidden-state behavior |
| guarded score $Q$ | conservative branch-recovery score | $\min\{\text{suffix decoder},\text{branch probe},\text{branch swap}\}$ | primary recovery metric | full causal proof |
| coverage gap | K=3 advantage over K=1/K=2 | $\operatorname{AUC}_Q(3)-\max\{\operatorname{AUC}_Q(1),\operatorname{AUC}_Q(2)\}$ | tests coverage mechanism | larger K always helps |
| clean $\tau=3$ | first branch-informative target is horizon 3 | $Y_1=A,\;Y_2=C,\;Y_3=S_Z$ | main test | real semantics |
| noisy control | horizon-3 target is branch-independent | $Y_3\perp Z$ | false-positive guard | all noise behavior |

## Setup

Same matrix as A11_04 decision-only:

- conditions: `K1_fixed_3head`, `K2_active`, `K3_active`;
- regimes: `clean_tau3`, `noisy_h3`, `redundant_h3`;
- init modes: `identical_branch`, `random`;
- seeds: `971,972,973,974,975`;
- model: one-layer one-head Transformer, `d_model=64`;
- training: `15000` steps, eval every `500` steps.

Only training scope changes:

$$
\texttt{decision\_only}\rightarrow\texttt{all\_positions\_lm\_control}.
$$

Evaluation remains at the same decision prefix $h_T$.

## Main Result

Clean $\tau=3$ condition means:

| Init | Condition | AUC $Q$ | Final $Q$ | Reach rate | Final $Y_1$ acc | Final $Y_2$ acc | Native $Y_3$ acc |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| identical | K=1 | 0.823 | 0.700 | 0.60 | 1.00 | 0.00 | NA |
| identical | K=2 | 0.715 | 0.700 | 0.40 | 1.00 | 1.00 | NA |
| identical | K=3 | 0.976 | 1.000 | 1.00 | 1.00 | 1.00 | 1.00 |
| random | K=1 | 0.942 | 0.950 | 0.80 | 1.00 | 0.00 | NA |
| random | K=2 | 0.942 | 1.000 | 0.80 | 1.00 | 1.00 | NA |
| random | K=3 | 1.000 | 1.000 | 1.00 | 1.00 | 1.00 | 1.00 |

Coverage contrast:

| Init | AUC coverage gap | Final $Q$ gap | Interpretation |
| --- | ---: | ---: | --- |
| identical | +0.153 | +0.300 | K=3 remains strongest |
| random | +0.058 | +0.000 | K=1/K=2 nearly match K=3 |

## Control Result

Noisy controls are high under all-position training:

| Init | Noisy K=1 AUC $Q$ | Noisy K=2 AUC $Q$ | Noisy K=3 AUC $Q$ | Main implication |
| --- | ---: | ---: | ---: | --- |
| identical | 0.500 | 0.552 | 0.489 | moderate false-positive branch readability |
| random | 0.798 | 0.932 | 0.913 | strong random-init / background-loss leakage |

This means all-position recovery cannot be interpreted as direct evidence that the active horizon covered the first informative future token. The target-information guard is weaker under all-position training because other positions and shared parameters can create branch-readable states.

## Interpretation

Decision-only asks a clean theoretical question: does the loss at $h_T$ include a branch-specific target? There, K=3 is decisive in $\tau=3$.

All-position asks a different question: after training the whole sequence with LM-style losses, is $Z$ recoverable from $h_T$? In this setting, even K=1 can become branch-readable because the same model parameters are trained on later branch-revealing contexts. This is not a bug; it shows that all-position LM training supplies indirect branch supervision outside the decision prefix.

## Hypothesis Status

| Hypothesis | Status | Reason |
| --- | --- | --- |
| K=3 remains strongest in clean $\tau=3$ | supported | K=3 AUC $Q$ is `0.976/1.000`, reach rate `1.00` |
| K=1/K=2 remain low under all-position | falsified | clean K=1/K=2 AUC $Q$ is high, especially under random init |
| noisy controls remain negative | falsified / weakened | noisy all-position random AUC is high for K=1/K=2/K=3 |
| local targets preserved | supported | clean $Y_1,Y_2$ accuracies are preserved where active |

## Claim Boundary

Can claim:

- decision-only supports the direct first-informative-horizon mechanism;
- all-position K=3 is still the strongest and cleanest covering condition;
- all-position training introduces indirect branch supervision that can make non-covering conditions branch-readable.

Cannot claim:

- only K=3 can recover $Z$ under all-position training;
- high all-position $Q$ alone proves active-horizon coverage;
- all-position results prove natural-language MTP superiority;
- noisy controls are clean under all-position training.

## Next Decision

The next theoretical statement should separate two mechanisms:

1. direct single-prefix supervision: $K\ge\tau$ creates a direct loss term at $h_T$;
2. indirect all-position transfer: background losses at later positions can move shared parameters so that $h_T$ also exposes $Z$.

The next experiment should only proceed after this distinction is written into the theory story.

## Source Artifacts

- Protocol: `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/protocol.md`
- Detailed record: `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/detailed.md`
- Runner: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py`
- Config: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_04_k3_first_informative_horizon_all_positions.json`
- Result dir: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_04_k3_first_informative_horizon_all_positions/a11_04_02_k3_all_positions_4gpu_20260708_0015`
- Remote job: `pt-f5hhx4a6`
