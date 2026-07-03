# 06_04 Synthetic Hidden-State Gate Geometry Decomposition Anchor

## 0. Thinking Card
父问题：在 feature distribution 均匀时，初始化 dot-product top-1 gate 是否仍会因为 hidden-state geometry 而产生 step-0 load imbalance？
当前子问题：在 `seq_len=32` 的 synthetic `(slot,target)` task 上，用 4 个均匀 `(slot,target)` pairs 和 4 个 experts，诊断 expert center norm、hidden common component、以及二者交互。
当前判断：A06_04 支持 hidden common component 是本 synthetic hidden-state setting 中的主导 tested source；row norm 不是主因，interaction 不稳定。
关键证据：primary readout 中 $L$ 从 `RR=0.5578` 降到 `RC=0.2578` / `NC=0.2407`，但 `NR=0.5577` 基本不变；layer 和 LayerNorm guard sweep 保持同一主判断。
最危险边界：只能 claim 均匀合成任务上的 initialized hidden-state step-0 routing geometry，不能 claim real text、training collapse、semantic specialization 或 final router method。
下一步决策：在 common-centering 后的 residual load 上继续拆 hidden anisotropy、router-direction cell geometry、random context / position effects。

Question:
Under a uniform synthetic `(slot,target)` distribution, does initialized step-0 top-1 load imbalance come mainly from expert-center norm variation, hidden common component, their interaction, or neither?
Physical prior:
Even when symbolic feature pairs are uniformly sampled, the initialized model maps them to hidden states with geometry $h_i=c+r_i$, and dot-product routing scores $z_{i,e}=w_e^\top h_i=\rho_e u_e^\top(c+r_i)$ can be imbalanced.
Core model:
Four-condition score replay on the same hidden states: raw/normalized expert centers crossed with raw/common-centered hidden states.
Model term being tested:
The norm scale $\rho_e$, the common component $c$, and their top-1 interaction.
Primary metric:
Load imbalance $L=m\max_e |p_e-1/m|$.
Falsifier:
Not observed. `RC` and `NC` reduce $L$ under balanced `(slot,target)` pairs and guard sweeps, while `NR` remains close to `RR`.
Can claim:
Mechanism evidence that the hidden common component is the dominant tested source of initialized synthetic hidden-state step-0 routing imbalance.
Cannot claim:
Uniform-sphere gate-only behavior, real-text routing, training collapse, semantic specialization, expert utility, or a deployable router.
Next decision:
Diagnose the residual load after common-centering: hidden anisotropy, router-direction cell geometry, random-context structure, position effects, or finite-sample effects.

## 1. Problem Definition

Parent problem:
Can a uniform feature distribution still produce non-uniform initialized expert loads after the data are embedded and transformed into router-input hidden states?

Sharper subproblem:
Separate two named gate/hidden geometry terms on the same initialized hidden states:

- expert-center norm variation in router rows;
- hidden common component through $w_e^\top c$.

Decision question:
Which replay control most reduces step-0 load imbalance on the same initialized hidden states: expert-center norm normalization, hidden common-centering, both together, or neither?

Not in scope:
Training dynamics, final collapse explanation, real-text claim, semantic specialization, expert utility claim, or method design.

## 2. Physical Priors

P1:
Uniform symbolic data does not imply uniform hidden-state geometry.

Could be wrong if:
Balanced `(slot,target)` pairs with random context produce no fixed hidden-state load imbalance beyond sampling noise.

P2:
Router rows act as expert centers. If $w_e=\rho_e u_e$, larger $\rho_e$ can increase expert $e$'s top-1 winning probability.

Could be wrong if:
Normalizing $\rho_e$ does not reduce load imbalance on matched hidden states.

P3:
Hidden states may contain a shared component. If $h_i=c+r_i$, then $w_e^\top c$ is an expert-specific effective bias.

Could be wrong if:
Routing $h_i-c$ does not reduce load imbalance.

## 3. Falsifiable Hypotheses

H1:
Expert-center norm variation contributes if `normalized_center_raw_hidden` has lower $L$ than `raw_center_raw_hidden`.

H2:
Hidden common component contributes if `raw_center_centered_hidden` has lower $L$ than `raw_center_raw_hidden`.

H3:
Interaction contributes if `normalized_center_centered_hidden` is lower than both single controls, or the joint readout differs from the sum of the single-control reads.

H4:
Neither tested term is sufficient if all controls have $L$ close to the raw condition.

## 4. Mathematical Model

Objects:
There are 4 uniformly sampled `(slot,target)` pairs and 4 experts. For sample $i$ and expert $e$, let $h_i$ be the final router-input hidden state at the last slot position, $w_e$ the router row, $\rho_e=\|w_e\|$, $u_e=w_e/\rho_e$, $c=\frac{1}{N}\sum_i h_i$, and $r_i=h_i-c$.

Core decomposition:
$$
w_e=\rho_e u_e,\quad h_i=c+r_i
$$

Scoring conditions:
$$
z^{RR}_{i,e}=w_e^\top h_i,\quad
z^{NR}_{i,e}=\bar{\rho}u_e^\top h_i
$$

$$
z^{RC}_{i,e}=w_e^\top(h_i-c),\quad
z^{NC}_{i,e}=\bar{\rho}u_e^\top(h_i-c)
$$

where `RR` is raw center/raw hidden, `NR` is normalized center/raw hidden, `RC` is raw center/centered hidden, and `NC` is normalized center/centered hidden.

Primary metric:
$$
a_i=\arg\max_e z_{i,e},\quad
p_e=\frac{1}{N}\sum_i \mathbf{1}[a_i=e],\quad
L=m\max_e\left|p_e-\frac{1}{m}\right|
$$

Diagnostic effects:
$$
E_{norm}=L^{RR}-L^{NR},\quad
E_{common}=L^{RR}-L^{RC},\quad
E_{joint}=L^{RR}-L^{NC}
$$

$$
E_{interaction}=E_{joint}-E_{norm}-E_{common}
$$

The effect terms are secondary diagnostics. The primary judgment remains the condition-wise $L$ comparison.

## 5. Computational Realization

Input objects:
Initialized dot-product top-1 synthetic MoE, `seq_len=32`, four uniformly sampled `(slot,target)` pairs, random pair position, random background tokens, final hidden states at the last slot position, and final-router rows.

Minimal setup constraints:

- 4 `(slot,target)` pairs and 4 experts;
- each pair is sampled uniformly;
- the pair appears at random valid positions in the sequence;
- all non-pair positions are filled with random background tokens independent of pair id and position;
- route at the last slot position; for a one-token slot this is the slot token position;
- `num_layers` guard sweep is `1, 2, 4`;
- for `num_layers > 1`, read only the final TransformerMoEBlock distribution;
- LayerNorm guard sweep compares final-router `post_ln` input with `pre_ln_replay` input;
- no training and no architecture/method conclusion.

Expected artifacts:
`protocol.md`, result tables, central load-imbalance figures, `summary.md`, and `detailed.md`.

## 6. Minimal Falsification Tests

Test 1:
Four-condition score replay on identical hidden states.

Primary metric:
$L=m\max_e |p_e-1/m|$.

Supports:
Norm, common, or interaction according to which control lowers $L$ on matched samples.

Weakens:
All tested terms are weakened if `NR`, `RC`, and `NC` stay close to `RR`.

Insufficient evidence:
The 4 pairs are not uniform, pair positions are not randomized, random background tokens are pair-correlated, hidden states are extracted from the wrong slot position/block, or the replay changes model state instead of only scores.

Test 2:
Configuration guard sweep.

Comparison:
Repeat Test 1 for `num_layers=1,2,4` and `router_input_norm=post_ln,pre_ln_replay`.

Role:
This sweep qualifies the claim boundary. It does not change the decision question or introduce a method.

## 7. Current Evidence

Observation:
06_03 supports row-norm variation as a causal contributor to fixed gate-only top-1 imbalance.

Boundary:
That evidence is pure gate-only with uniform high-dimensional inputs. It does not include model-generated hidden states.

Evidence links:
`Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_03_high_dimensional_gaussian_gate_norm_variation_anchor.md`
`Projects/from-attention-to-search/main/experiments/A06/A06_03_high_dimensional_gaussian_gate_norm_variation/summary.md`

Observation:
0610 dot-product slot-specialization work supports common-logit as a plausible early routing driver, but its main setting used fixed `B_CONST`.

Boundary:
That evidence motivates this synthetic hidden-state audit but does not decide it.

Evidence links:
`daily_research_reports/backup/0610/meeting_brief.md`
`Projects/from-attention-to-search/main/experiments/A05/A05_04_01_round1_slot_specialization_protocol_dot_product/summary.md`

Observation:
A06_04 completed the planned synthetic hidden-state replay audit. In the primary readout, mean $L$ is `RR=0.5578`, `NR=0.5577`, `RC=0.2578`, and `NC=0.2407`. The common effect is positive in all 8 primary seeds; the norm effect is near zero and changes sign. The layer and LayerNorm guard sweeps keep the same main ordering.

Boundary:
This supports hidden common component as the dominant tested source in initialized synthetic hidden states. It weakens row norm as the main explanation in this setting, but does not erase the earlier gate-only 06_03 result. Residual load after common-centering remains.

Evidence links:
`Projects/from-attention-to-search/main/experiments/A06/A06_04_real_hidden_state_gate_geometry_decomposition/summary.md`
`Projects/from-attention-to-search/main/experiments/A06/A06_04_real_hidden_state_gate_geometry_decomposition/detailed.md`

## 8. Claim Boundary And Next Decision

Can claim:
For the completed synthetic initialized hidden-state audit, the hidden common component is the strongest tested explanation of step-0 top-1 load imbalance under uniform `(slot,target)` sampling.

Also can claim:
Expert-center norm variation is weakened as the main explanation for this hidden-state setting, and the tested interaction is not stable enough to be the main claim.

Cannot claim:
Uniform-sphere gate-only behavior, real-text behavior, final trained collapse, semantic specialization, expert utility, or a final router method.

Next decision:
Use common-centering as the baseline control and run the next residual diagnostic: hidden anisotropy, router-direction cell geometry, random-context / position structure, or finite-sample effects.
