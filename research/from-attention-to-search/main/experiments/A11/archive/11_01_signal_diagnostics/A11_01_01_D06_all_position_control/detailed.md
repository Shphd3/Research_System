# Detailed: A11_04_02 K=3 All-Position Control

Status: completed on 2026-07-08.

## Decision

The all-position control is a negative/refining result for the strong coverage claim. K=3 remains strongest in clean $\tau=3$, but K=1 and K=2 no longer remain branch-blind. Therefore all-position training does not preserve the clean decision-only separation.

## Terminology / Definitions

| Term | Plain meaning | Concrete object or computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| all-position LM-style loss | Offset loss applied at every valid sequence position | for active horizon $j$, predict $X_{t+j}$ at each valid $t$ | CE | tests robustness to LM-style training | natural-language transfer |
| decision prefix $h_T$ | prefix hidden state before target suffix | state after `BR_z F... U...` | vector | same evaluation point as decision-only | all states |
| coverage gap | K=3 advantage over K=1/K=2 | $\operatorname{AUC}_Q(3)-\max\{\operatorname{AUC}_Q(1),\operatorname{AUC}_Q(2)\}$ | score | primary metric | universal K scaling |
| guarded score $Q$ | conservative branch recovery | $\min\{A,P,S\}$ | 0 to 1 | avoids probe-only evidence | full causality |
| indirect transfer | shared-parameter effect from losses at other positions | background losses make $h_T$ branch-readable | qualitative mechanism | explains non-covering recovery | direct supervision at $h_T$ |

## Protocol Compliance

| Item | Required | Observed |
| --- | --- | --- |
| Job id | reserved 4-GPU full run | `pt-f5hhx4a6`, `RESERVED`, `SUCCEEDED` |
| Seeds | `971-975` | complete |
| Regimes | `clean_tau3`, `noisy_h3`, `redundant_h3` | complete |
| Conditions | K=1, K=2, K=3 | complete |
| Init modes | `identical_branch`, `random` | complete |
| Seed-condition rows | 90 | 90 |
| Summary rows | 18 | 18 |
| Checkpoint rows | 2790 | 2790 |

## Theory Clause Tested

Decision-only mechanism:

$$
\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\},
\qquad
L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
$$

In clean $\tau=3$:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

The decision-only claim is direct: K=1/K=2 do not contain $\operatorname{CE}(q_3,S_Z)$ at $h_T$, while K=3 does.

All-position changes the training object:

$$
L_K^{\mathrm{all}}=\sum_{t}\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_t),X_{t+j}).
$$

This includes losses at later positions, so branch information can affect shared parameters even if the decision-prefix active targets are non-informative.

## Main Tables

Full condition means:

| Regime | Condition | Init | n | Mean reached step | Reach rate | AUC $Q$ | Final $Q$ | Eval suffix | Probe | Swap | $Y_1$ acc | $Y_2$ acc | Native info acc |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| clean | K=1 | identical | 5 | 1833 | 0.60 | 0.823 | 0.700 | 0.850 | 0.800 | 0.850 | 1.000 | 0.000 | NA |
| clean | K=1 | random | 5 | 1000 | 0.80 | 0.942 | 0.950 | 1.000 | 0.950 | 1.000 | 1.000 | 0.000 | NA |
| clean | K=2 | identical | 5 | 1500 | 0.40 | 0.715 | 0.700 | 0.700 | 0.800 | 0.700 | 1.000 | 1.000 | NA |
| clean | K=2 | random | 5 | 1000 | 0.80 | 0.942 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | NA |
| clean | K=3 | identical | 5 | 1500 | 1.00 | 0.976 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| clean | K=3 | random | 5 | 1000 | 1.00 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| noisy | K=1 | identical | 5 | 10167 | 0.60 | 0.500 | 0.600 | 0.600 | 0.600 | 0.600 | 1.000 | 0.000 | NA |
| noisy | K=1 | random | 5 | 1600 | 1.00 | 0.798 | 0.400 | 0.550 | 0.450 | 0.550 | 1.000 | 0.000 | NA |
| noisy | K=2 | identical | 5 | 9750 | 0.40 | 0.552 | 0.700 | 0.750 | 0.700 | 0.750 | 1.000 | 1.000 | NA |
| noisy | K=2 | random | 5 | 1600 | 1.00 | 0.932 | 0.800 | 0.800 | 0.800 | 0.800 | 1.000 | 1.000 | NA |
| noisy | K=3 | identical | 5 | NA | 0.00 | 0.489 | 0.550 | 0.600 | 0.600 | 0.600 | 1.000 | 1.000 | NA |
| noisy | K=3 | random | 5 | 1600 | 1.00 | 0.913 | 0.750 | 0.800 | 0.750 | 0.800 | 1.000 | 1.000 | NA |
| redundant | K=1 | identical | 5 | 4667 | 0.60 | 0.813 | 0.800 | 0.850 | 0.800 | 0.850 | 1.000 | 0.000 | NA |
| redundant | K=1 | random | 5 | 1000 | 0.80 | 0.950 | 0.950 | 0.950 | 0.950 | 0.950 | 1.000 | 0.000 | NA |
| redundant | K=2 | identical | 5 | 1500 | 1.00 | 0.976 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | NA |
| redundant | K=2 | random | 5 | 1000 | 1.00 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | NA |
| redundant | K=3 | identical | 5 | 1500 | 1.00 | 0.976 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| redundant | K=3 | random | 5 | 1000 | 1.00 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Clean coverage contrast:

| Init | AUC coverage gap | Final $Q$ gap | K=1 AUC | K=2 AUC | K=3 AUC |
| --- | ---: | ---: | ---: | ---: | ---: |
| identical | +0.153 | +0.300 | 0.823 | 0.715 | 0.976 |
| random | +0.058 | +0.000 | 0.942 | 0.942 | 1.000 |

## Interpretation

Observation: K=3 is strongest in clean $\tau=3$, but K=1 and K=2 are already high under all-position training.

Interpretation: all-position losses at later sequence positions provide indirect branch supervision through shared parameters. Thus high $Q(h_T)$ is not sufficient evidence that the active decision-prefix horizon covered $\tau$.

Decision: keep the direct first-informative-horizon theorem as a decision-only/single-prefix statement. For LM-style training, add a second mechanism: indirect all-position transfer.

## Visualization Results

No central figure is promoted. The decision is table-based: the full condition table and coverage-contrast table directly show that non-covering conditions become high under all-position training. These tables do not prove natural-language transfer.

## Artifact Map

| Artifact | Path |
| --- | --- |
| Protocol | `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/protocol.md` |
| Summary | `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/summary.md` |
| Runner | `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py` |
| Config | `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_04_k3_first_informative_horizon_all_positions.json` |
| Result dir | `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_04_k3_first_informative_horizon_all_positions/a11_04_02_k3_all_positions_4gpu_20260708_0015` |
| Curated local tables | `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/tables/` |
| Remote job | `pt-f5hhx4a6` |
