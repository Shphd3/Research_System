# Protocol: A06_01_03_E03 Synthetic-To-Realistic Proxy Bridge

## 0. Approval Snapshot

Approval status: Draft for user review. Do not run until approved.

Purpose: locate the first failed contract when moving from clean synthetic input cues toward weaker realistic proxy conditions.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/subanchors/06_01_03_label_free_route_state_selection_anchor.md`

Anchor decision question: when input sequences are made progressively less clean, does the first failed contract occur in label-free proxy discovery or in training-time preservation?

Anchor physical prior tested: stable input feature cues can create measurable residual feature centers after attention, but nuisance cues can compete with those centers and training can erase their routing margin.

Anchor core model term tested: the input-to-hidden measured ratio $\beta_{\mathrm{eff}}/\lambda_{\mathrm{eff}}$, not directly assigned $\beta/\lambda$.

Anchor falsifier: oracle reachability fails in the bridge cells, or measured $\beta_{\mathrm{eff}}/\lambda_{\mathrm{eff}}$ does not move with the input knobs, so the bridge cannot test the intended mechanism.

Experiment role: root-cause audit / mechanism bridge, not method construction.

Primary metric from anchor: `first_failed_stage`.

Claim boundary from anchor: this can choose the next mechanism class; it cannot prove real-DCLM semantic specialization, expert utility, or a deployable router method.

Minimal setup: start from the A06_01_03_E02/A06_02_01_E01 one-layer Transformer + top-1 MoE route-position task, fix slot length at 4, route at the last token of the feature slot, add controlled input feature/nuisance cues, measure post-attention hidden geometry, then test discovery and preservation.

Basic configuration: 4 operational features, 4 experts, top-1 router, equal-norm router rows, movable slot start, routed position equal to `slot_start + slot_token_len - 1`, slot token length 4, calibration/evaluation split, train only cells whose step-0 discovery passes.

Conditions to run: clean feature-only input, mild nuisance input, moderate nuisance input, weak feature plus nuisance input, route-position clustering, all-position clustering, oracle controls, random/equal-norm random, and label-shuffled guard.

Pass: a valid cell identifies geometry failure, discovery failure, preservation failure, or pass with oracle/random/shuffled guards.

Fail: all cells are ambiguous, oracle fails before pseudo can be judged, or input knobs do not measurably change hidden-state feature/nuisance geometry.

Insufficient: missing held-out split, label leakage, no oracle upper bound, no measured $\beta_{\mathrm{eff}}/\lambda_{\mathrm{eff}}$, no nuisance guard, or no checkpointed trajectory for preservation cells.

Cannot claim: direct hidden-state control, real-language feature discovery, DCLM preservation, expert utility, or final anti-collapse method.

Approval decision: approve only if the user accepts that the direct experimental knobs are input-sequence knobs and that $\beta_{\mathrm{eff}}/\lambda_{\mathrm{eff}}$ are measured hidden-state quantities.

## 1. Anchor Alignment

Decision question: which stage first breaks when clean synthetic input feature cues are weakened toward realistic proxy mixtures?

Physical prior tested: post-attention hidden states may contain recoverable feature residual centers, but nuisance cues and training dynamics can destroy their usefulness for routing.

Core model term tested: measured feature-to-nuisance strength in hidden space, $\beta_{\mathrm{eff}}/\lambda_{\mathrm{eff}}$, plus route-position versus all-position clustering scope.

Falsifier: the intended sequence knobs do not create measurable hidden-state geometry changes, or oracle controls fail in all bridge cells.

Claim boundary: the experiment chooses the next anchor direction; it does not validate a real DCLM method.

## 2. Tested Hypothesis

H1: Discovery is the first bottleneck if oracle centroids still route the feature but label-free pseudo centers fail step-0 feature NMI or align with nuisance after input cues become less clean.

H2: Preservation is the first bottleneck if pseudo centers pass step-0 feature NMI but training causes large NMI drop while target accuracy remains acceptable.

H3: Route-position specificity is an active boundary if route-position clustering succeeds but all-position clustering fails or becomes nuisance-aligned.

H4: The bridge itself is invalid if input knobs do not change measured $\beta_{\mathrm{eff}}/\lambda_{\mathrm{eff}}$ in the intended direction.

## 3. Rival Explanations

R1: The bridge is too hard because the operational feature is absent. Guard: oracle centroid must remain high; otherwise mark the cell insufficient.

R2: The sequence knobs do not affect hidden geometry after attention. Guard: measure $\beta_{\mathrm{eff}}$, $\lambda_{\mathrm{eff}}$, feature separability, and nuisance separability before interpreting discovery.

R3: Pseudo discovery only improves load, not feature routing. Guard: require `feature_NMI` and nuisance NMI, not load alone.

R4: All-position clustering fails because of occupancy or implementation details rather than mixed factors. Guard: compare occupancy, nuisance NMI, and held-out route-position evaluation.

R5: Training failure is actually target-learning failure. Guard: require target accuracy / loss to remain acceptable before calling it preservation failure.

R6: Training failure can come from router row drift or hidden-state drift. Guard: for preservation-fail cells, replay `W0 on Ht`, `Wt on H0`, and `Wt on Ht`.

## 4. Data / Model / Algorithm / Objective

Data family: synthetic sequence task inherited from A06_01_03_E02/A06_02_01_E01, with evaluation-only feature label $f_i$, nuisance label $z_i$, and slot start $s_i$.

Model: one-layer Transformer feeding a top-1 MoE router with 4 experts. Slot token length is fixed at 4. The routed/evaluated position is the last token of the slot, not the penultimate token and not a fixed final `QUERY` token:

$$
p_i^\star=s_i+\texttt{slot\_token\_len}-1=s_i+3.
$$

Direct input knobs:

- `slot_start`: where the length-4 feature slot appears in the sequence.
- `slot_pattern_mode`: whether the slot uses repeated feature tokens or heterogeneous feature-specific token patterns.
- `feature_cue_strength`: operationalized by how many slot tokens carry feature information, slot-template consistency, or cue-token dropout.
- `nuisance_type`: decoy token, irrelevant context token, or position/context pattern independent of the feature.
- `nuisance_strength`: operationalized by nuisance token count, nuisance consistency, or nuisance-token salience.
- `clustering_scope`: route-position hidden states versus all-position hidden states.

Hidden-state audit:

$$
h_i=T_\theta(x_i,p^\star),\qquad r_i=h_i-\bar h.
$$

Estimate feature center:

$$
\hat\mu_f=\mathbb{E}[r_i\mid f_i=f].
$$

Estimate nuisance center after feature removal:

$$
\hat n_z=\mathbb{E}[r_i-\hat\mu_{f_i}\mid z_i=z].
$$

Compute:

$$
\beta_{\mathrm{eff}}=\operatorname{mean}_f\|\hat\mu_f\|,\qquad
\lambda_{\mathrm{eff}}=\operatorname{mean}_z\|\hat n_z\|,\qquad
\rho_{\mathrm{eff}}=\beta_{\mathrm{eff}}/(\lambda_{\mathrm{eff}}+\delta).
$$

Discovery algorithm: compute calibration common mean $\bar h$, form residuals $r_i=h_i-\bar h$, fit k-means centers without feature labels, normalize centers into equal-norm router rows, evaluate held-out route-position assignments.

Training objective: same route-position target prediction objective as A06_02_01_E01 for the first approved run. This keeps the bridge tied to the synthetic success case before adding DCLM complexity.

Stage order:
1. Input-to-hidden geometry audit.
2. Oracle reachability.
3. Label-free discovery.
4. Training preservation only if discovery passes.
5. Replay decomposition only if preservation fails.

## 5. Concrete Experimental Design

Main experiment: a small controlled sequence ladder, not a broad sweep. The core data unit is a length-4 feature slot placed at a variable start position. Routing happens at the fourth token of that slot.

Example with `seq_len=16`, `slot_token_len=4`, `slot_start=5`, `feature_id=2`, `nuisance_id=1`:

```text
[N, D1, N, N, N, F2a, F2b, F2c, F2d, N, N, D1, N, N, N, N]
                         ^
                    route at F2d
target = Y2
```

Here the slot is `[F2a, F2b, F2c, F2d]`. Its tokens need not be identical. The prediction target depends only on `feature_id=2`, not on `nuisance_id=1`, `slot_start=5`, or filler tokens.

| Cell | Input construction | Intended role | Direct knobs | Expected hidden effect |
| --- | --- | --- | --- | --- |
| C0 clean feature | movable heterogeneous feature slot; no decoy/context nuisance | known-good bridge start | high feature cue, no nuisance | high $\beta_{\mathrm{eff}}$, low $\lambda_{\mathrm{eff}}$ |
| C1 mild nuisance | C0 plus one nuisance cue independent of feature and slot start | test mild realistic mixture | high feature cue, low nuisance | high $\beta_{\mathrm{eff}}$, small $\lambda_{\mathrm{eff}}$ |
| C2 moderate nuisance | C0 plus stronger or repeated nuisance cue | find discovery boundary | high feature cue, medium nuisance | lower $\rho_{\mathrm{eff}}$ |
| C3 weak feature + nuisance | only part of the slot carries feature-specific tokens; nuisance kept | test weak proxy condition | lower feature cue, medium nuisance | lowest $\rho_{\mathrm{eff}}$ among valid cells |
| C4 all-position clustering | same data as C1/C2, but cluster all hidden states | test route-position boundary | clustering scope changed | possible nuisance or position alignment |

Operational examples:

- Feature slot: each feature has a length-4 slot pattern, for example `F2a F2b F2c F2d`; slot tokens are allowed to differ.
- Main template: the final slot token is feature-specific for this bridge run, so oracle reachability remains valid at step 0.
- Clean feature: all four slot positions carry feature-specific tokens.
- Weak feature: only two or three slot positions carry feature-specific tokens; the remaining slot positions are neutral, while the target label is still the slot's feature id.
- Route position: always the fourth token of the slot, for example `F2d` in `F2a F2b F2c F2d`.
- Nuisance cue: token family `D0/D1/D2/D3` sampled independently from feature id and slot start, placed outside the feature slot.
- Stronger nuisance: repeat `D_z`, place it closer to the routed position, or make its position pattern more consistent.
- Filler: neutral token family `N` fills positions outside the feature slot and nuisance positions.
- Independence guard: feature id, nuisance id, and slot start must be independently and uniformly sampled.
- Last-token shortcut guard: because the main run uses a feature-specific slot-end token, it cannot prove whole-slot composition. A later stronger bridge may use shared or partially shared slot-end tokens after oracle reachability is restored.

Important implementation constraint: if the current A06_01_03_E02/A06_02_01_E01 code cannot directly scale embeddings, do not edit embeddings for the main protocol. Use only sequence-level controls first. Embedding-scale variants may be a later diagnostic, not the primary evidence.

## 6. Conditions, Seeds, And Checkpoints

Default smoke run:

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C0 clean route-position pseudo | known-good bridge start | high $\rho_{\mathrm{eff}}$ | reproduces A06_01_03_E02/A06_02_01_E01 style success | primary sanity | pseudo NMI high and preserved | clean case fails | oracle fails | stage table, NMI trajectory |
| C1 mild nuisance route-position | discovery robustness | mild nuisance cue | tests whether small nuisance breaks pseudo centers | primary | pseudo near oracle | oracle high but pseudo low | hidden geometry unchanged | geometry table, first-failed-stage plot |
| C2 moderate nuisance route-position | discovery robustness | stronger nuisance cue | locates break point if mild passes | primary | pseudo near oracle or clear fail | oracle high but pseudo low | oracle low | first-failed-stage plot |
| C3 weak feature plus nuisance | feature-to-nuisance stress | weaker feature cue | tests lower measured feature margin | primary | pseudo discovers or preservation fails | discovery/preservation fail localized | oracle low or geometry unchanged | stage table |
| C4 all-position clustering | route-position boundary | clustering scope | tests whether discovery depends on known routed position | secondary but decision-relevant | all-position near route-position | all-position nuisance-aligned | occupancy degenerate | nuisance NMI table |
| Oracle centroid | upper bound | feature present? | prevents false method failure | guard | oracle NMI high | none | oracle low marks cell invalid | oracle gap table |
| Random / equal-norm random | lower bound | row-norm/load artifact | prevents load-only false positive | guard | low NMI baseline | random high ambiguous | no baseline | baseline table |
| Label-shuffled pseudo | leakage guard | label leakage | ensures discovery is label-free | guard | shuffled near random | shuffled high | no shuffled labels | leakage table |

Seeds: smoke `0, 1, 2`; full run only after smoke passes may use `0..7`.

Checkpoints: `0, 1, 2, 3, 5, 10, 20, 50, final` using the A06_02_01_E01 step schedule. If runtime is limited, `0, 5, 10, final` is the minimum preservation audit.

## 7. Primary Metric

Primary metric: `first_failed_stage`.

Definition:

```text
bridge_invalid:
  measured rho_eff in harder C2/C3 cells is not lower than clean C0
  or feature/nuisance labels are not independent
  or feature/slot-start/nuisance balance is violated
  or oracle step0 feature_NMI < 0.90 in all non-clean cells

oracle_fail:
  oracle step0 feature_NMI < 0.90 for a specific cell

discovery_fail:
  oracle step0 feature_NMI >= 0.90
  and (
    pseudo step0 feature_NMI < 0.80
    or oracle-pseudo NMI gap >= 0.30
    or pseudo nuisance_NMI >= pseudo feature_NMI - 0.10
  )

preservation_fail:
  pseudo step0 feature_NMI >= 0.80
  and (
    final feature_NMI < 0.60
    or NMI_drop >= 0.40
  )
  while target_accuracy >= 0.95

pass_bridge_cell:
  oracle step0 feature_NMI >= 0.90
  pseudo step0 feature_NMI >= 0.80
  final feature_NMI >= 0.80
  NMI_drop <= 0.20
  target_accuracy >= 0.95
```

Why it decides the judgment: the anchor is not asking for the best score. It asks which contract fails first: bridge validity, oracle reachability, discovery, or preservation.

False-positive cost: calling preservation failure when the input bridge did not create the intended hidden geometry would send the next anchor toward anti-feedback prematurely.

False-negative cost: calling discovery success when clusters are nuisance-aligned would send a bad proxy into training and hide the real bottleneck.

## 8. Secondary Metrics

- $\beta_{\mathrm{eff}}$: average norm of feature-conditioned residual centers.
- $\lambda_{\mathrm{eff}}$: average norm of nuisance-conditioned residual centers after removing feature center.
- $\rho_{\mathrm{eff}}$: $\beta_{\mathrm{eff}}/(\lambda_{\mathrm{eff}}+\delta)$.
- `feature_NMI`: agreement between evaluation-only feature label and routed expert.
- `nuisance_NMI`: agreement between route/cluster and nuisance id.
- Load $L=m\max_e|p_e-1/m|$: detects collapse or empty experts.
- Margin p05: 5th percentile of top-1 versus runner-up router logit gap.
- Target accuracy / loss: guard that the model learned the prediction task.
- Oracle-pseudo gap: difference between oracle centroid NMI and pseudo-center NMI.
- Replay decomposition if preservation fails:
  - `W0 on Ht`: hidden drift under fixed initial router.
  - `Wt on H0`: router row drift under fixed initial hidden states.
  - `Wt on Ht`: actual trained trajectory.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good:

- C0 clean route-position pseudo should reproduce A06_01_03_E02/A06_02_01_E01: high step-0 NMI and preserved training NMI.
- Oracle centroid should be high in every valid bridge cell.

Known bad:

- Random and label-shuffled pseudo should not reach high feature_NMI.
- Load balance without high feature_NMI is not discovery.

Known confusing:

- Input knob changes but $\rho_{\mathrm{eff}}$ does not move: bridge invalid, not evidence against discovery or preservation.
- Oracle fails: the cell does not contain a recoverable feature partition; do not blame pseudo discovery.
- High load balance with low NMI: load-only false positive.
- High step-0 NMI but low target accuracy: not valid preservation failure.
- All-position clusters may be balanced but nuisance-aligned; read nuisance NMI before judging discovery.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Input-to-hidden geometry | did the sequence knobs create the intended hidden geometry? | hidden states, feature/nuisance labels | $\rho_{\mathrm{eff}}$ decreases from clean to harder cells; otherwise bridge invalid | effective geometry table, center cosine matrix | valid cells only |
| Oracle reachability | does the feature exist in the cell? | hidden states, feature labels for evaluation | oracle NMI >= 0.90 pass; otherwise cell insufficient | oracle route heatmap | valid cells only |
| Discovery | can pseudo centers recover feature without labels? | calibration residuals, held-out residuals | pseudo NMI >= 0.80 and nuisance guard pass | cluster occupancy, feature/nuisance NMI table | train only pass cells |
| Preservation | does training keep routing? | initialized model, checkpoints | final NMI >= 0.80 and drop <= 0.20 pass | NMI/load/margin trajectory | if fail, run replay split |
| Replay split | what moved, router or hidden states? | W0, Wt, H0, Ht | W0/Ht fail = hidden drift; Wt/H0 fail = router drift; both = coupled feedback | replay table | next anchor target |

## 11. Algorithm Specification

input:

- Synthetic sequences with feature label $f_i$ used only for evaluation.
- Nuisance label $z_i$ sampled independently from $f_i$.
- Slot start $s_i$ sampled independently from both $f_i$ and $z_i$.
- Hidden states at route position and optional all positions.
- Train / calibration / held-out split.

parameters:

| Parameter | Value | Meaning | Why this value | If too small | If too large |
| --- | --- | --- | --- | --- | --- |
| `K` | 4 | number of clusters / features / experts | matches A06_01_03_E02/A06_02_01_E01 feature count | merges features | creates unused experts |
| `num_experts` | 4 | MoE experts | one expert per feature in positive control | cannot represent all features | makes NMI harder to interpret |
| `slot_token_len` | 4 | slot cue length | matches robust A06_01_03_E02/A06_02_01_E01 setting | feature signal may be too weak | too clean / unrealistic |
| `slot_start_set` | early/middle/late valid starts | allowed feature-slot starts | tests position variation without changing route rule | fixed-position shortcut remains | may collide with nuisance/filler constraints |
| `route_position` | `slot_start + 3` | routed/evaluated token | tests slot-end routing geometry | if earlier, route may miss full slot | if final query, mixes retrieval with routing |
| `feature_cue_strength` | clean/high/weak | direct sequence-level feature visibility | replaces invalid direct beta control | no bridge if unchanged | may stay too clean |
| `nuisance_strength` | none/mild/moderate | direct sequence-level nuisance visibility | replaces invalid direct lambda control | no stress if too low | oracle may fail if too high |
| `clustering_scope` | route-position, all-position | hidden states used for clustering | tests route-position boundary | misses generalization if only route | may mix too many factors |
| `calibration_fraction` | 0.5 | data for fitting centers | matches held-out audit logic | unstable centers | small held-out set |
| `seeds` | `0,1,2` smoke | randomness | enough to catch obvious seed fragility | no robustness read | slow before operationalization passes |
| `train_checkpoints` | `0,1,2,3,5,10,20,50,final` | preservation trajectory | catches early collapse | misses timing | unnecessary for smoke if too dense |
| `nmi_pass` | 0.80 | step-0 pseudo pass threshold | separates useful from weak routing | accepts weak proxy | may reject partial but useful signal |
| `oracle_pass` | 0.90 | valid-cell threshold | ensures feature is present | invalid cells enter | too few cells remain |
| `target_acc_pass` | 0.95 | learning guard | prevents task-failure confusion | calls bad learners valid | may reject hard but informative cells |

intermediate variables:

- calibration mean $\bar h$;
- residual $r_i=h_i-\bar h$;
- feature centers $\hat\mu_f$;
- nuisance centers $\hat n_z$;
- $\beta_{\mathrm{eff}}$, $\lambda_{\mathrm{eff}}$, and $\rho_{\mathrm{eff}}$;
- discovered centers $\hat c_k$;
- oracle centers;
- router rows $w_e$;
- route assignment $a_i(t)$;
- `feature_NMI`, `nuisance_NMI`, load $L$, margin p05, target accuracy.

steps:

1. Generate sequence cells C0-C4 from the balanced Cartesian product of feature id, nuisance id, and slot start.
2. Train or instantiate the same one-layer Transformer + top-1 MoE setup used by A06_02_01_E01 for the clean route-position task.
3. Split examples into calibration and held-out sets.
4. Extract post-attention hidden states at `route_position = slot_start + 3`; for C4 also collect all-position hidden states for clustering.
5. Compute calibration mean and residual hidden states.
6. Estimate $\beta_{\mathrm{eff}}$, $\lambda_{\mathrm{eff}}$, and $\rho_{\mathrm{eff}}$ on calibration and held-out splits.
7. Fit pseudo centers using k-means without labels.
8. Build equal-norm router rows from pseudo centers.
9. Build oracle centroid rows using labels for upper-bound evaluation only.
10. Evaluate step-0 held-out routing for random, pseudo, oracle, and shuffled guards.
11. Mark each cell as bridge invalid, oracle fail, discovery fail, discovery pass, or insufficient.
12. Train only discovery-pass cells.
13. Evaluate checkpoint trajectories.
14. For preservation-fail cells, run `W0 on Ht`, `Wt on H0`, and `Wt on Ht` replay.
15. Save stage contract table, effective geometry table, and figures.

outputs:

- `tables/effective_geometry_table.csv`;
- `tables/stage_contract_table.csv`;
- `tables/bridge_metrics_by_cell.csv`;
- `tables/replay_decomposition.csv`;
- `figures/effective_geometry_by_cell.png`;
- `figures/bridge_first_failed_stage.png`;
- `figures/nmi_trajectory_by_bridge_cell.png`;
- `figures/nuisance_alignment_by_scope.png`.

debug artifacts:

- cluster occupancy by cell;
- route heatmap by condition;
- representative pass/fail examples per failed stage;
- center cosine matrix;
- margin histogram;
- feature/nuisance independence check.
- feature/nuisance/slot-start balance check.

pass conditions:

- input knobs make hard cells C2/C3 lower in measured rho_eff than clean C0;
- feature id, nuisance id, and slot start are strictly balanced and mutually independent;
- each valid cell maps to a clear `first_failed_stage`;
- at least one clean known-good cell passes;
- random and shuffled guards remain low;
- oracle upper bound marks valid cells.

fail conditions:

- no cell separates geometry validity, discovery, and preservation;
- label leakage guard is high;
- oracle is low in all bridge cells;
- target learning fails in all training cells;
- measured hidden geometry does not change with the sequence knobs.

failure reasons:

- `bridge_invalid_geometry_not_moved`;
- `bridge_invalid_unbalanced_slot_feature_nuisance`;
- `oracle_feature_absent`;
- `pseudo_discovery_failed`;
- `nuisance_aligned_clusters`;
- `training_preservation_failed`;
- `target_learning_failed`;
- `router_drift`;
- `hidden_drift`;
- `coupled_feedback_drift`;

## 12. Success / Failure / Insufficient Evidence

Support discovery bottleneck: oracle and hidden geometry are valid, but pseudo step-0 feature NMI fails or becomes nuisance-aligned.

Support preservation bottleneck: pseudo step-0 feature NMI passes, but final feature NMI collapses while target accuracy passes.

Support route-position boundary: route-position clustering passes while all-position clustering fails or becomes nuisance-aligned.

Insufficient evidence: the bridge is invalid, oracle fails before pseudo can be judged, label leakage guard is high, or hidden geometry is not measured.

## 13. What This Cannot Claim

This protocol cannot claim direct control of attention hidden states.

It cannot claim real-language semantic feature discovery.

It cannot claim real DCLM preservation or expert utility.

It cannot claim that a preservation intervention works.

It only decides which mechanism class should be tested next.

## 14. Review Notes And Protocol Changes

2026-06-23: revised protocol after user audit. The old wording treated $\beta$ and $\lambda$ as directly controllable hidden-state knobs. The protocol now treats input-sequence construction as the direct control and $\beta_{\mathrm{eff}}/\lambda_{\mathrm{eff}}$ as measured hidden-state quantities.

2026-06-23: superseded execution note. The first completed reduced-full run used 4-GPU ACP job `pt-an9ktx73`: 8 seeds, C0-C4 cells, 128 train samples per `(feature, nuisance, slot_start)` combination, 96 calibration/eval samples per combination, and 400 training steps. This run is retained as the pos-on diagnostic, not as the current A06_01_03_E03 conclusion. The larger first submission `pt-i2mx9s6u` was stopped because it was too slow for same-day mechanism closure.

2026-06-23: superseded post-result correction. A local root-cause diagnostic showed that the `pt-an9ktx73` C0 discovery failure was driven by learned absolute positional embeddings interacting with discrete slot starts `{2,10,18}`. Per user decision, A06_01_03_E03 was rerun with learned absolute `pos_emb` zeroed and frozen; RoPE is not tested in this anchor. The intermediate corrected run was `pt-x1txvi33`, `a06_16_proxy_bridge_no_pos_c0_c3_reduced_full_20260623_1`, covering C0-C3 over 8 seeds. C4 all-position k-means was then still unresolved because sklearn/CPU attempts in `pt-m99g4msb` and `pt-68d6f8x6` were stopped as runtime-invalid. This note is superseded by the full-run update below.

2026-06-23: full-run update. A06_01_03_E03 added a torch/GPU k-means backend and reran the corrected no-pos bridge as `pt-7oabnyza`, `a06_16_proxy_bridge_no_pos_full_gpu_kmeans_20260623_1`: 8 seeds, C0-C4, full 1600-step training for C0-C3, and all-position C4 discovery. This supersedes the reduced C0-C3 run for the canonical result. C4 is now adjudicated as mostly passing in the no-pos setting, 7/8 seeds.

2026-06-23: preservation audit correction. A post-run audit found that the full-run preservation stage discovered pseudo centers in one random model but trained a freshly initialized random model. This makes the preservation trajectory a cross-model center-transfer diagnostic, not a same-model training-preservation result. The runner is updated so preservation defaults to `reuse_discovery_model_state=true`; smoke verification showed C0 same-model training step 0 returns `feature_NMI=1.0`.

2026-06-23: audit artifact expansion. Future A06_01_03_E03 reruns save `discovery_heatmap.csv`, `training_heatmap.csv`, `*_mapping_audit.csv`, `training_mapping_change.csv`, feature centroid distance/PCA tables, router-feature alignment tables, and router row geometry tables. These tables are required to distinguish label swap, feature merge, router-row drift, and hidden-state drift.

2026-06-23: canonical rerun. Per user instruction, old problematic A06_01_03_E03 raw result and figure directories were deleted, along with project-local copied tables/figures. The same-model audit full run was submitted as ACP job `pt-vcl6tl57`, run name `a06_16_proxy_bridge_no_pos_same_model_audit_full_20260623_1`. This run is now canonical for A06_01_03_E03. It shows C0-C3 pass discovery and same-model preservation across 8/8 seeds; C4 all-position discovery remains mostly passing with 7/8 pass and one route-position boundary failure.
