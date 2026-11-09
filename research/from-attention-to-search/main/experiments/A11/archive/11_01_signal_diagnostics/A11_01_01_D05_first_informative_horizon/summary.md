# Summary: A11_04 K=3 First-Informative-Horizon

Status: completed and merged. This folder is the canonical experiment record for both the decision-only run (`pt-a140a1iu`, 2026-07-07) and the all-position control run (`pt-f5hhx4a6`, 2026-07-08).

## What We Established

A11_04 is one experiment with two training scopes. The shared question is whether MTP helps because its prediction horizon covers the first future token that contains new information about an early variable.

The clean theoretical result is supported in the decision-only scope: when the first informative future token is at $\tau=3$, K=1 and K=2 stay branch-blind, while K=3 recovers the early variable from the same prefix state.

The all-position scope refines the boundary: K=3 remains strongest, but K=1/K=2 can also recover the early variable through indirect training at other positions. Therefore the supported claim is direct single-prefix supervision, not exclusive recoverability under full LM-style training.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Why it matters | What it cannot prove |
| --- | --- | --- | --- | --- |
| early variable $Z$ | information present in the prefix and needed later | branch identity in `BR_z` | controlled long-horizon semantic factor | natural-language semantics |
| first informative horizon $\tau$ | first future offset that adds new information about $Z$ | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | core theory variable | fixed horizon in real text |
| covering condition | active objective includes $\tau$ | K=3 in clean $\tau=3$ | receives direct supervision from $S_Z$ | guaranteed optimization speed |
| non-covering condition | active objective stops before $\tau$ | K=1/K=2 in clean $\tau=3$ | lacks direct $S_Z$ target at $h_T$ | no indirect learning |
| decision-only scope | loss is applied only at the decision prefix | $L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j,Y_j)$ | isolates the theorem object | full language-model training |
| all-position scope | loss is applied at every valid sequence position | $\sum_t\sum_j\lambda_j\operatorname{CE}(q_j(h_t),X_{t+j})$ | checks LM-style boundary | direct supervision source |
| guarded score $Q_K$ | conservative branch-recovery score | $\min\{A_K,P_K,S_K\}$ | primary evidence for $Z$ in $h_T$ | full causal proof |

## Setup

Clean $\tau=3$ data:

```text
BR_z F_00 ... F_15 U_00 ... U_03 A_SHARED C_SHARED S_z
```

Targets:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

Information structure:

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)>0.
$$

Shared configuration: one-layer one-head Transformer, `d_model=64`, `num_branches=4`, `filler_length=16`, `shared_context_length=4`, seeds `971-975`, conditions K=1/K=2/K=3, regimes clean/noisy/redundant, and both `identical_branch` and `random` initialization.

The only intended difference between the two scopes is training scope:

$$
\text{decision-only}\quad \text{vs.}\quad \text{all-position}.
$$

Evaluation remains at the same decision prefix $h_T$.

## Main Results

### Scope A: decision-only

Clean $\tau=3$ decision-only means:

| Init | K | Covers $\tau=3$? | AUC $Q$ | Final $Q$ | Reach rate | Local $Y_1,Y_2$ guard |
| --- | --- | --- | ---: | ---: | ---: | --- |
| identical | 1 | no | 0.250 | 0.250 | 0.00 | $Y_1=1.00$ |
| identical | 2 | no | 0.250 | 0.250 | 0.00 | $Y_1=1.00,Y_2=1.00$ |
| identical | 3 | yes | 0.665 | 0.800 | 0.60 | $Y_1=1.00,Y_2=1.00$ |
| random | 1 | no | 0.266 | 0.250 | 0.00 | $Y_1=1.00$ |
| random | 2 | no | 0.271 | 0.250 | 0.00 | $Y_1=1.00,Y_2=1.00$ |
| random | 3 | yes | 0.735 | 0.750 | 0.40 | $Y_1=1.00,Y_2=1.00$ |

Decision-only interpretation: K=2 can learn the shared second token $C$, but it does not recover $Z$ because $C$ carries no information about $Z$. K=3 is the first condition with a direct $S_Z$ target at $h_T$, and it recovers $Z$.

### Scope B: all-position control

Clean $\tau=3$ all-position means:

| Init | K | Covers decision-prefix $\tau=3$? | AUC $Q$ | Final $Q$ | Reach rate | Local $Y_1,Y_2$ guard |
| --- | --- | --- | ---: | ---: | ---: | --- |
| identical | 1 | no | 0.823 | 0.700 | 0.60 | $Y_1=1.00$ |
| identical | 2 | no | 0.715 | 0.700 | 0.40 | $Y_1=1.00,Y_2=1.00$ |
| identical | 3 | yes | 0.976 | 1.000 | 1.00 | $Y_1=1.00,Y_2=1.00$ |
| random | 1 | no | 0.942 | 0.950 | 0.80 | $Y_1=1.00$ |
| random | 2 | no | 0.942 | 1.000 | 0.80 | $Y_1=1.00,Y_2=1.00$ |
| random | 3 | yes | 1.000 | 1.000 | 1.00 | $Y_1=1.00,Y_2=1.00$ |

All-position interpretation: K=3 remains strongest, but K=1/K=2 no longer stay low. This means all-position background losses can transmit $Z$ through shared parameters, so high $Q(h_T)$ is not by itself evidence that the decision-prefix active horizon covered $\tau$.

## Combined Judgment

| Claim | Status | Reason |
| --- | --- | --- |
| Direct first-informative-horizon supervision | supported | decision-only K=3 beats K=1/K=2 when $\tau=3$ |
| "Larger K always helps" | not supported | advantage appears when added horizons contain information about $Z$ |
| "Only K=3 can recover $Z$" under all-position training | falsified | all-position K=1/K=2 can also become branch-readable |
| MTP efficiency advantage | open | current evidence shows direct supervision and boundary, not faster optimization |

## Claim Boundary

Can claim:

- In a controlled single-prefix objective, MTP has an advantage when its active horizon covers the first future token that contains information about the early variable.
- This advantage is a direct representation-supervision claim: low loss on the informative future token requires $h_T$ to contain $Z$.
- In all-position training, K=3 remains the cleanest direct-supervision condition, but non-covering K=1/K=2 can recover $Z$ indirectly.

Cannot claim:

- MTP is always better than NTP.
- Larger K always helps.
- MTP has already been shown to be faster or more sample-efficient.
- The synthetic mechanism directly transfers to natural language.
- Non-covering horizons can never encode $Z$ under all-position training.

## Next Decision

The next research question should be efficiency, not existence:

> Given that MTP provides direct representation supervision when it covers the informative future token, does this direct supervision make long-horizon semantic information appear earlier or more robustly during LM-style training than NTP?

The primary future metrics should be time-to-threshold $T_\theta$, early AUC of $Q_K(t)$, and local next-token loss guard.

## Source Artifacts

- Protocol: `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/protocol.md`
- Detailed record: `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/detailed.md`
- Original all-position record: `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/`
- Decision-only result dir: `active/synthetic_data_understanding/results/a11_04_k3_first_informative_horizon/a11_04_k3_first_informative_decision_only_4gpu_20260707_1718`
- All-position result dir: `active/synthetic_data_understanding/results/a11_04_k3_first_informative_horizon_all_positions/a11_04_02_k3_all_positions_4gpu_20260708_0015`
- Decision-only job: `pt-a140a1iu`
- All-position job: `pt-f5hhx4a6`
