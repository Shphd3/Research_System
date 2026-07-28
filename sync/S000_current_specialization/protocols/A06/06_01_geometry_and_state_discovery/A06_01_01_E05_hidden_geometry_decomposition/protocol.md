# Protocol: A06_01_01_E05 Synthetic Hidden-State Gate Geometry Decomposition

## 0. Approval Snapshot

Approval status:
Approved for implementation and run.

Purpose:
Diagnose which initialized gate/hidden geometry term explains step-0 top-1 load imbalance after uniformly sampled synthetic `(slot,target)` pairs are mapped into model hidden states.

Primary anchor:
`Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/subanchors/06_01_01_common_geometry_nuisance_controls_anchor.md`

Anchor decision question:
Under a uniform synthetic `(slot,target)` distribution, does initialized step-0 top-1 load imbalance come mainly from expert-center norm variation, hidden common component, their interaction, or neither?

Anchor physical prior tested:
Uniform symbolic pairs can still become non-uniform hidden-state geometry; dot-product routing scores follow $z_{i,e}=w_e^\top h_i=\rho_e u_e^\top(c+r_i)$.

Anchor core model term tested:
$\rho_e$, $c$, and their top-1 interaction.

Anchor falsifier:
All replay controls leave $L$ close to the raw condition under balanced pairs, randomized positions, random background tokens, and guard sweeps.

Experiment role:
Root-cause audit on synthetic hidden states. This is not method construction and not a real-text audit.

Primary metric from anchor:
Load imbalance $L=m\max_e |p_e-1/m|$.

Claim boundary from anchor:
Initialized hidden-state routing geometry for a uniform synthetic `(slot,target)` task only.

Minimal setup:
No training. Replay four scoring conditions on the same extracted hidden states and final-router rows.

Basic configuration:
`seq_len=32`, 4 `(slot,target)` pairs, 4 experts, random pair position, random background tokens, route at the last slot position.

Conditions to run:
`RR`, `NR`, `RC`, `NC` crossed with `num_layers=1,2,4` and `router_input_norm=post_ln,pre_ln_replay`.

Pass:
One named factor gives the clearest paired reduction in $L$ without reversing under guard sweeps.

Fail:
No replay control reduces $L$ relative to `RR`.

Insufficient:
The 4 pairs are not uniform, pair positions are not randomized, background tokens are pair-correlated, final-block states are not exposed, or LayerNorm/readout conditions are not comparable.

Cannot claim:
Uniform-sphere gate-only behavior, real-text behavior, training collapse, semantic specialization, expert utility, or final router design.

Approval decision:
Approved by user response on 2026-06-21. The user resolved the data,
position, LayerNorm-sweep, and claim-boundary review points.

## 1. Anchor Alignment

Decision question:
Which replay control most reduces initialized step-0 load imbalance on the same synthetic hidden states: norm control, common-centering, both, or neither?

Physical prior tested:
Uniform symbolic data may still produce non-uniform router-input hidden-state geometry.

Core model term tested:
The four-condition replay of $w_e=\rho_e u_e$ and $h_i=c+r_i$.

Falsifier:
`NR`, `RC`, and `NC` have load imbalance close to `RR`.

Claim boundary:
Synthetic initialized hidden states only. No training, real-text, or method claim.

## 2. Tested Hypothesis

H1:
If expert-center norm variation matters, `NR` lowers $L$ relative to `RR`.

H2:
If hidden common component matters, `RC` lowers $L$ relative to `RR`.

H3:
If the two factors interact, `NC` is the lowest condition or the joint effect differs from the sum of the two single-control effects.

H4:
If none of these terms matter, all four conditions have similar $L$.

## 3. Rival Explanations

R1:
The old fixed `B_CONST` structure created a misleading common-logit read.

Separated by:
Remove B tokens entirely. Use only `(slot,target)` pairs and route at the slot's last position.

R2:
Random background tokens or pair positions create a shortcut rather than a uniform feature distribution.

Separated by:
Audit uniform pair counts, uniform pair-position counts, and background-token independence from pair id.

R3:
Residual router-direction geometry or hidden anisotropy causes the imbalance.

Separated by:
`NC` still remains imbalanced.

R4:
The readout is an artifact of one-layer architecture or LayerNorm placement.

Separated by:
Run `num_layers=1,2,4` and `post_ln` vs `pre_ln_replay` guard sweeps.

## 4. Data / Model / Algorithm / Objective

Data:

| Field | Value |
| --- | --- |
| sequence length | 32 |
| number of pairs | 4 |
| number of experts | 4 |
| slot tokens | `SLOT_0..SLOT_3` |
| target tokens | `TARGET_0..TARGET_3` |
| pair form | `(SLOT_s, TARGET_s)` |
| valid pair starts | `0..30` |
| route position | last slot position; for one-token slots this is `pair_start` |
| target position | `pair_start + 1` |
| pair distribution | uniform over the 4 pairs |
| position distribution | pair start sampled uniformly over valid starts |
| background tokens | random tokens in all non-pair positions, sampled independently of pair id and position |
| background-token guard | prefer a disjoint background-token set so accidental slot/target repeats do not create a second feature source |

This is uniform in the symbolic synthetic task distribution. It is not uniform over hidden-state geometry.

Model:
Initialized dot-product top-1 synthetic MoE. No training is run.

Layer sweep:
Run `num_layers=1,2,4`. For depth greater than one, extract only the final TransformerMoEBlock router distribution and final-router rows.

LayerNorm sweep:

- `post_ln`: the actual final-router input after the block's LayerNorm.
- `pre_ln_replay`: the corresponding final pre-router residual stream before that LayerNorm, scored by the same final-router rows.

This is a readout sweep, not a proposed architecture.

Reference code:

- Old 0610 extraction reference: `Projects/from-attention-to-search/main/experiments/A05/A05_04_01_round1_slot_specialization_protocol_dot_product/scripts/run_round1_slot_specialization_protocol_dot_product.py`
- Current one-layer model reference: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/src/synthetic_data_understanding/tiny_moe.py`
- A06_01_01_E05 runner: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_04_real_hidden_state_gate_geometry_decomposition.py`
- A06_01_01_E05 config: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_04_real_hidden_state_gate_geometry_decomposition.json`
- A06_01_01_E05 4GPU ACP submit script: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_acp.sh`

Implementation note:
The 0610 runner is a reference for hidden-state extraction and position audits only. Its `SLOT_s B_CONST Y_s` data format must not be reused for this protocol.

Objective:
No optimization objective is used because this is a replay diagnostic before training.

## 5. Conditions, Seeds, And Checkpoints

Primary readout:
`num_layers=1`, `router_input_norm=post_ln`.

Guard sweeps:
`num_layers=1,2,4` crossed with `router_input_norm=post_ln,pre_ln_replay`.

Seeds:
Use the 0610 seed set unless implementation smoke tests require a smaller dry run first:
`20260521, 20260522, 20260523, 20260524, 20260525, 20260526, 20260527, 20260528`.

Checkpoints:
Only initialization / step 0.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RR` raw center/raw hidden | baseline | raw $w_e^\top h_i$ | defines uncontrolled load | primary | baseline exists | missing baseline | wrong state/position | `tables/results.csv` |
| `NR` normalized center/raw hidden | H1 | $\rho_e$ | tests expert-center norm | primary | lower $L$ than `RR` | similar $L$ | row directions not matched | `figures/load_imbalance_by_condition.png` |
| `RC` raw center/centered hidden | H2 | $c$ | tests common component | primary | lower $L$ than `RR` | similar $L$ | $c$ from wrong population | `figures/load_imbalance_by_condition.png` |
| `NC` normalized center/centered hidden | H3/R3 | joint / residual | tests interaction and residual geometry | primary | lowest or distinct joint effect | similar to `RR` | changes hidden states | `tables/paired_effects.csv` |
| layer sweep | R4 | depth sensitivity | checks final-block stability | secondary | ordering stable | ordering reverses | wrong block read | `figures/load_imbalance_by_layer.png` |
| LayerNorm sweep | R4 | normalization sensitivity | checks readout dependence on LayerNorm | secondary | boundary clear | readout reverses | states not comparable | `figures/load_imbalance_by_layernorm.png` |

## 6. Primary Metric

Primary metric:
$L=m\max_e |p_e-1/m|$.

Why it decides:
The current question is whether initialized top-1 routing distributes a uniform synthetic pair distribution unevenly across experts after model hidden-state formation. $L$ directly measures worst-expert deviation from uniform load.

No fixed reduction threshold:
This protocol does not use a hard percentage threshold such as "20% lower
$L$." The first diagnostic reads paired ordering and effect sign across
matched seeds and guard sweeps.

Interpretation rule:
A condition is treated as mechanism-supporting only if it lowers $L$ relative
to `RR` in the matched primary readout and does not reverse under the planned
guard sweeps. Small or seed-unstable reductions are recorded as suggestive or
insufficient rather than promoted to a mechanism claim.

## 7. Secondary Metrics

Secondary diagnostics:

- `max_load`;
- `active_experts`;
- load entropy;
- `row_norm_cv`;
- common-score spread $\max_e w_e^\top c-\min_e w_e^\top c$;
- route agreement between conditions;
- $E_{norm}$, $E_{common}$, $E_{joint}$, and $E_{interaction}$.

Secondary metrics cannot override the primary metric. They explain why $L$ changed or did not change.

## 8. Known Good / Known Bad / Known Confusing Cases

Known good:
06_03 gate-only norm-control result: norm control reduces fixed imbalance when row norm is causal.

Known bad:
A run that keeps `SLOT_s B_CONST Y_s` is invalid for this protocol because it repeats the old fixed-B confound.

Known confusing:
Random context can create hidden common components even when pair labels are uniform. That is not a data-uniformity failure by itself; it is part of the synthetic hidden-state audit.

Known confusing:
`pre_ln_replay` may change hidden norm scale strongly. If its load changes but `post_ln` does not, the result is a LayerNorm boundary, not a method conclusion.

Pre-run prediction:
Because 06_03 already showed that router-row norm can create fixed gate-only
imbalance, `NR` should reduce some part of $L$ if the initialized hidden states
still expose that scale effect. Because earlier common-logit audits showed
that hidden common components can behave like expert-specific bias, `RC` may
also reduce $L$. The most likely informative outcome is partial reduction by
one or both controls rather than perfect balance. If `NC` remains clearly
imbalanced, the next diagnostic should treat residual hidden anisotropy or
router-direction cell geometry as the leading explanation.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| pair audit | Are the 4 `(slot,target)` pairs uniform? | counts table | all pairs equal | `tables/pair_audit.csv` | detailed |
| position audit | Are pair starts uniform? | counts table | starts balanced or sampled uniformly with recorded counts | `tables/position_audit.csv` | detailed |
| background audit | Are random tokens independent of pair id? | token-by-pair table | no pair-correlated background token pattern | `tables/background_audit.csv` | detailed |
| state extraction | Are final-block `post_ln` and `pre_ln_replay` available at slot-last position? | tensor shapes and sample count | both present for every seed/depth | `tables/state_audit.csv` | detailed |
| router audit | Are final-router rows matched to extracted states? | layer id and weight shape | final block only | `tables/router_audit.csv` | detailed |
| score replay | Are only scores changed? | condition config | hidden states unchanged | `tables/replay_audit.csv` | detailed |
| metric read | Which condition lowers $L$? | condition table | paired readout exists | `tables/paired_effects.csv` | summary |

## 10. Algorithm Specification

input:
Balanced `seq_len=32` synthetic batches, initialized model, target layer depth, router input norm mode, final-router weights.

parameters:
`num_pairs=4`, `num_experts=4`, `num_layers in {1,2,4}`, `router_input_norm in {post_ln,pre_ln_replay}`, `score_condition in {RR,NR,RC,NC}`.

intermediate variables:
$h_i$, $c$, $w_e$, $\rho_e$, $u_e$, scores $z_{i,e}$, assignments $a_i$, load probabilities $p_e$.

steps:
1. Build sequences with one uniformly sampled `(slot,target)` pair at a uniformly sampled valid pair start.
2. Fill every non-pair position with random background tokens independent of pair id.
3. Initialize the model for one seed.
4. Extract final-block hidden states at the last slot position for `post_ln` and `pre_ln_replay`.
5. Extract final-router rows from the same block.
6. Compute `RR`, `NR`, `RC`, and `NC` scores without changing model state.
7. Compute top-1 assignments and $L$ for each condition.
8. Aggregate by seed, layer depth, and LayerNorm readout.
9. Write tables and figures.

outputs:
`results.csv`, `aggregate_by_condition.csv`, `paired_effects.csv`, central figures, `summary.md`, and `detailed.md`.

debug artifacts:
Pair audit, position audit, background audit, state audit, router audit, replay audit.

pass conditions:
The primary metric exists for every planned condition and the matched-condition comparison is valid.

fail conditions:
Pair distribution is not uniform, random background is pair-correlated, state extraction is wrong, final-router weights are mismatched, or score replay changes hidden states.

failure reasons:
Implementation drift, wrong block, wrong routed position, background-token confound, missing LayerNorm state, or fixed-B contamination from old code.

## 11. Success / Failure / Insufficient Evidence

Support norm mechanism:
`NR` is lower than `RR` in the primary readout and does not reverse under guard sweeps.

Support common mechanism:
`RC` is lower than `RR` in the primary readout and does not reverse under guard sweeps.

Support interaction:
`NC` is the clearest lowest condition, or $E_{interaction}$ shows that the joint intervention behaves differently from the two single controls.

Weaken tested mechanisms:
`NR`, `RC`, and `NC` all stay close to `RR`.

Insufficient evidence:
Any data audit or extraction audit fails, or the primary readout and guard sweeps conflict so strongly that no claim boundary can be stated.

## 12. What This Cannot Claim

This protocol cannot claim:

- uniform-sphere gate-only behavior;
- real-text behavior;
- trained MoE collapse mechanism;
- semantic or causal expert specialization;
- expert utility alignment;
- a final router method;
- that LayerNorm should be removed or added as an architecture decision.

## 13. Review Notes And Protocol Changes

User review resolved on 2026-06-21:

- The data object is exactly 4 `(slot,target)` pairs and 4 experts.
- The 4 pairs are strictly uniform.
- Pair positions are randomized.
- Background tokens are independent of pair id; implementation should follow
  the listed reference code style for synthetic construction and audits.
- The old `SLOT_s B_CONST Y_s` format must not be reused.
- Slot token length is fixed, and routing uses the last slot position.
- Final-block router extraction should follow the same reference convention as
  other blocks that expose router inputs.
- The LayerNorm comparison is only a sweep / side conclusion and must not be
  written as the mainline result.
- No fixed reduction threshold is used; paired ordering, sign, and guard-sweep
  stability decide the first diagnostic.
- Reports and replies should include the pre-run prediction above, while
  keeping it separate from post-result conclusions.
- Claim boundary remains initialized synthetic hidden-state routing geometry
  only.

## 14. Approval Status

status: approved_for_run
approved_to_run: yes
approval_source: user response on 2026-06-21
execution_status: completed
job_id: pt-sqq2jr6d
run_name: a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_20260621
submit_log: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_20260621_submit_20260621_124911.log`
runtime_log: `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_20260621_runtime_20260621_124953.log`
smoke_status: passed on CPU with run `a06_04_smoke_20260621_1249`
result_summary: `summary.md`
detailed_record: `detailed.md`

## 15. Submission Record

Submitted on 2026-06-21:

- ACP job id: `pt-sqq2jr6d`
- final ACP state: `SUCCEEDED`
- command surface: `submit_a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_acp.sh`
- runner: `run_a06_04_real_hidden_state_gate_geometry_decomposition.py`
- config: `configs/a06_04_real_hidden_state_gate_geometry_decomposition.json`
- seeds: `20260521,20260522,20260523,20260524,20260525,20260526,20260527,20260528`
- guard sweep: `num_layers=1,2,4` crossed with `router_input_norm=post_ln,pre_ln_replay`
- score replay conditions: `RR,NR,RC,NC`
- expected result dir: `active/synthetic_data_understanding/results/a06_04_real_hidden_state_gate_geometry_decomposition/a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_20260621`
- expected figure dir: `active/synthetic_data_understanding/figures/a06_04_real_hidden_state_gate_geometry_decomposition/a06_04_real_hidden_state_gate_geometry_decomposition_4gpu_20260621`
