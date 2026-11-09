## 0. Quick Recap

Purpose:

Run the Round-1 minimal slot-block collapse audit for sparse top-1 MoE, exactly covering P0, P1, P2, P3, and P5 from `daily_research_reports/0609/round1_slot_specialization_protocol.md`.

Hypothesis:

If slot information is visible in the routed hidden state but vanilla top-1 routing still collapses, then the failure is a router/gating-dynamics problem rather than a representation-absence problem. If slot-aware initialization preserves slot routing, then slot specialization is reachable under favorable initialization.

Experiment logic:

Use a balanced moving-block dataset `D_min_block_shift`: each sequence contains `SLOT_s B_CONST Y_s`, the block start is uniformly sampled over valid positions, position embeddings are zeroed and frozen, loss and routing metrics are computed only at the `B_CONST` position, and the router is sparse top-1.

Conclusion:

The clean minimal setting still collapses under vanilla sparse top-1 routing. Slot signal is perfectly decodable from `h_B`, and slot-aware initialization makes slot specialization mostly stable. The strongest Round-1 interpretation is: collapse is not caused by missing slot information; it is caused by ordinary router entry/lock-in dynamics, with P3 pointing to common-component logit dominance.

Evidence:

P1 reaches target accuracy 1.0 in all 8 seeds but has mean `max_load=0.969` and mean `slot_to_expert_NMI=0.080`. P2 final held-out-position slot probe accuracy is 1.0 in all seeds. P5 reaches mean `slot_to_expert_NMI=0.980`, mean `max_load=0.278`, and accuracy 1.0.

---

## 1. Source Protocol And Scope

Source protocol:

`daily_research_reports/0609/round1_slot_specialization_protocol.md`

Primary anchor:

`Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_01_uniform_feature_specialization_after_position_removal_anchor.md`

Anchor decision question:

After position signals are removed, does collapse come from missing slot signal, residual non-slot logit bias, or sparse top-1 training lock-in?

Experiment role:

This is a staged audit under the `05_04` anchor. The experiment folder now follows the `A05_04_*` naming rule. The execution date is preserved in the run name, result folders, logs, and daily report path.

Stage mapping:

- P0 Dataset Audit -> validates the data and routing/loss positions before interpreting collapse.
- P1 Clean Baseline Re-Collapse -> tests whether vanilla sparse top-1 still collapses after position control.
- P2 Slot Signal Probe -> audits whether missing slot signal explains P1 collapse.
- P3 Logit Trajectory Decomposition -> audits whether router logits are driven by slot, common, block-position, or residual components.
- P4 Forced-Routing Utility Audit -> not run; therefore expert causal utility is not audited in Round 1.
- P5 Slot-Initialized Positive Control -> tests whether the intended slot partition is reachable and stable under favorable initialization.

Run name:

`round1_slot_specialization_4gpu_20260609`

Executed protocols:

1. P0 Dataset Audit
2. P1 Clean Baseline Re-Collapse
3. P2 Slot Signal Probe
4. P3 Logit Trajectory Decomposition
5. P5 Slot-Initialized Positive Control

Explicitly not run:

- P4 forced-routing utility audit
- P6 anti-lockin intervention
- P7 slot-order diagnostic

Reason:

Round 1 isolates whether the minimal clean setting collapses, whether slot information exists in `h_B`, which logit component dominates routing, and whether slot specialization is reachable under favorable initialization.

---

## 2. Execution Record

Code workspace:

`/data/250010109/Research_System`

Experiment directory:

`Projects/from-attention-to-search/main/experiments/A05/A05_04_01_round1_slot_specialization_protocol/`

Runner:

`scripts/run_round1_slot_specialization_protocol.py`

Submission script:

`scripts/submit_round1_slot_specialization_4gpu_acp.sh`

ACP job:

`pt-hkkon9oy`

ACP display name:

`ats-round1-slot-spec-4gpu`

ACP status:

`SUCCEEDED`

ACP worker:

`n6ls.iu.i40.4`, 4 H100-class GPUs, one worker node.

Runtime log:

`logs/acp/round1_slot_specialization_4gpu_20260609_runtime_20260609_101810.log`

Submit log:

`logs/acp/round1_slot_specialization_4gpu_20260609_submit_20260609_101751.log`

Full command:

```bash
python "${EXP_DIR}/scripts/run_round1_slot_specialization_protocol.py" \
  --output-dir "${EXP_DIR}" \
  --run-name "round1_slot_specialization_4gpu_20260609" \
  --run-stage full \
  --variants "P1_clean_baseline,P5_slot_centroid_init" \
  --router-metrics "cosine" \
  --seeds "20260521,20260522,20260523,20260524,20260525,20260526,20260527,20260528" \
  --train-steps "1600" \
  --train-repeats-per-pair "500" \
  --eval-repeats-per-pair "32" \
  --calibration-repeats-per-pair "32" \
  --batch-size "384" \
  --eval-batch-size "512" \
  --parallel \
  --max-parallel "4"
```

Smoke check:

Before ACP submission, a local smoke run completed with one seed and 10 steps. It verified that P0 passes, P1 collapses in the toy smoke setting, P5 step-0 initialization reaches `slot_to_expert_NMI=1.0`, and all required tables/figures can be generated.

---

## 3. Dataset And Model Setup

Dataset:

`D_min_block_shift`

Vocabulary and sequence:

- `S=4` slots: `SLOT_0` to `SLOT_3`
- `E=4` experts
- sequence length `L=12`
- one fixed `B_CONST`
- deterministic target rule: `SLOT_s -> Y_s`
- each sequence contains a contiguous block: `SLOT_s B_CONST Y_s`
- valid block starts: `0..9`

Sampling:

Each epoch enumerates all `(slot, block_start)` pairs, repeats each pair equally, and shuffles. The full run used `train_repeats_per_pair=500`, so each full training dataset has `4 * 10 * 500 = 20000` examples.

Loss and routing:

- training loss is next-token prediction loss only at the `B_CONST` position;
- routed hidden state is `h_B`, the hidden state at `B_CONST`;
- route statistics are collected only at the `B_CONST` position.

Model:

- small causal Transformer + MoE
- sparse top-1 selected-gate router
- `num_experts=4`
- router metric: cosine
- position embeddings zeroed and frozen from initialization
- auxiliary load-balance loss disabled

Evaluation schedule:

Checkpoints were collected at `0, 1, 2, 5, 10, 20, 50, 100, 200, 500`, then every 100 steps through 1600.

---

## 4. P0 Dataset Audit

Question:

Is the Round-1 dataset truly balanced and free from slot-position shortcuts?

Setup:

P0 enumerated slot counts, block-start counts, slot-block counts, target mapping, route position, and loss-mask position.

Observation:

All P0 checks passed.

Key audit values:

- each slot count: 320 in the audit set;
- each block-start count: 128 in the audit set;
- each route position count: 128 for positions 1 through 10;
- `target_given_slot_unique`: each slot maps to exactly one target;
- `target_given_block_start_unique`: each block start contains all four targets.

Interpretation:

The dataset is balanced with respect to slot and block start. The target is deterministic from slot and not uniquely determined by block start.

Supported:

P0 supports using this dataset for P1/P2/P3/P5.

Weakened:

Simple data imbalance or fixed-position shortcut is weakened as an explanation.

Insufficient evidence:

P0 does not test real representations or multi-B settings.

Cannot claim:

P0 does not prove the router will or should specialize; it only validates the dataset construction.

Deliverables:

- `results/round1_slot_specialization_4gpu_20260609/p0_dataset_audit.json`
- `results/round1_slot_specialization_4gpu_20260609/p0_dataset_audit.md`
- `results/round1_slot_specialization_4gpu_20260609/p0_dataset_audit_counts.csv`

---

## 5. P1 Clean Baseline Re-Collapse

Question:

In the minimal clean setting, does ordinary sparse top-1 MoE still collapse during training?

Setup:

Variant `P1_clean_baseline` uses random router initialization, no position encoding, fixed `B_CONST`, no auxiliary load-balance loss, and ordinary sparse top-1 routing.

Primary metric:

`max_load` is the decisive collapse metric because it measures whether traffic concentrates on a small subset of experts. `slot_to_expert_NMI` is the decisive specialization metric because it measures whether routed expert identity aligns with slot identity.

Observation:

| Metric | Mean | Min | Max |
|---|---:|---:|---:|
| `target_accuracy` | 1.000 | 1.000 | 1.000 |
| `max_load` | 0.969 | 0.750 | 1.000 |
| `slot_to_expert_NMI` | 0.080 | 0.000 | 0.637 |
| `active_experts` | 1.125 | 1.000 | 2.000 |
| `per_slot_route_purity` | 1.000 | 1.000 | 1.000 |

Seven of eight seeds route all slots to a single expert at the final checkpoint. One seed uses two experts but still has `max_load=0.75`, so it remains hard-collapsed under the protocol threshold.

Important interpretation of purity:

`per_slot_route_purity=1.0` is not evidence for useful slot specialization here. It only means each slot has a stable route. In collapsed seeds, every slot can be stably routed to the same expert, so purity is high while `slot_to_expert_NMI` is near zero.

Central figure:

![P1 route heatmaps](figures/round1_slot_specialization_4gpu_20260609/p1_route_heatmaps.png)

Interpretation:

The task is learned perfectly, but vanilla sparse top-1 routing does not form a non-collapsed slot-to-expert partition.

Supported:

P1 supports the claim that the clean minimal setting still collapses.

Weakened:

The idea that position encoding alone explains collapse is weakened.

Insufficient evidence:

P1 alone does not decide whether collapse is due to missing slot representation, common-logit dominance, early lock-in, or expert utility.

Cannot claim:

P1 does not prove that all sparse top-1 MoE settings collapse, and it does not test any intervention.

Deliverables:

- `p1_metrics_by_seed.csv`
- `p1_route_confusion_by_seed.csv`
- `p1_route_heatmaps.png`
- `p1_max_load_trajectory.png`
- `p1_slot_nmi_trajectory.png`
- `p1_accuracy_trajectory.png`
- `p1_summary.md`

---

## 6. P2 Slot Signal Probe

Question:

Does the routed hidden state at `B_CONST` contain decodable slot information?

Setup:

P2 trains linear probes from `h_B` to slot id and block-start id. It uses both a random split and a held-out block-start split. The held-out split tests whether slot information generalizes across block positions.

Observation:

Final P1 probe metrics:

| Metric | Mean | Min | Max |
|---|---:|---:|---:|
| `slot_probe_accuracy_random_split` | 1.000 | 1.000 | 1.000 |
| `slot_probe_accuracy_heldout_position` | 1.000 | 1.000 | 1.000 |
| `position_probe_accuracy` | 0.196 | 0.055 | 0.333 |
| `slot_component_variance_ratio` | 0.999 | 0.995 | 1.000 |
| `position_component_variance_ratio` | 0.00037 | 0.0000005 | 0.00239 |

Central figure:

![P2 probe trajectory](figures/round1_slot_specialization_4gpu_20260609/p2_probe_accuracy_trajectory.png)

Interpretation:

Slot information is present and linearly decodable from `h_B`, including across held-out block positions. Missing slot representation is therefore not the main Round-1 explanation for collapse.

Supported:

P2 supports the router/gating-dynamics hypothesis: the representation contains slot information, but P1 routing fails to use it as a balanced slot-to-expert partition.

Weakened:

Representation-side absence of slot signal is strongly weakened for this minimal task.

Insufficient evidence:

P2 does not prove slot-to-expert routing has causal expert utility; that is P4-like evidence and was not run in Round 1.

Cannot claim:

P2 does not establish that the same slot information will remain clean in multi-B or real-language settings.

Deliverables:

- `p2_probe_metrics_by_checkpoint.csv`
- `p2_probe_accuracy_trajectory.png`
- `p2_component_variance.csv`
- `p2_summary.md`

---

## 7. P3 Logit Trajectory Decomposition

Question:

When routing changes or locks in, is the top-1 decision driven by the slot component or by non-slot common / block-position components?

Setup:

P3 decomposes the hidden state as:

\[
h(s,p) = c + r_s + u_p + residual
\]

where `c` is the global common component, `r_s` is the slot component, and `u_p` is the block-start component.

For the current top-1 expert and runner-up expert, P3 decomposes the top-2 margin into common, slot, position, and residual terms.

Concrete decomposition algorithm:

1. Collect the routed hidden state `h_B` at the `B_CONST` position for every evaluation example.
2. Group `h_B` by slot `s` and block start `p`, then compute the cell mean:

\[
m_{s,p} = mean(h_B \mid slot=s, block\_start=p)
\]

3. Compute the global common component as the mean over all slot-position cells:

\[
c = mean_{s,p}(m_{s,p})
\]

4. Compute the slot component by averaging over block starts for each slot, then subtracting the common component:

\[
r_s = mean_p(m_{s,p}) - c
\]

This is the part of `h_B` that changes with slot identity after averaging out block position.

5. Compute the block-position component by averaging over slots for each block start, then subtracting the common component:

\[
u_p = mean_s(m_{s,p}) - c
\]

This is the part of `h_B` that changes with the moving block position after averaging out slot identity. Since position embeddings are zeroed and frozen, `u_p` is not a learned position embedding; it is any residual position/template effect still present in the hidden state.

6. Compute the residual for each slot-position cell:

\[
residual_{s,p} = m_{s,p} - c - r_s - u_p
\]

The residual is the remaining interaction/noise term not explained by the additive common + slot + block-position decomposition.

7. For each `(slot, block_start)` cell, compute router logits on the cell mean, identify the top-1 expert `e_1` and runner-up expert `e_2`, and define:

\[
\Delta w = w_{e_1} - w_{e_2}
\]

8. Decompose the top-2 router margin:

\[
margin = \Delta w^T m_{s,p}
\]

into:

\[
common\_margin = \Delta w^T c
\]

\[
slot\_margin = \Delta w^T r_s
\]

\[
position\_margin = \Delta w^T u_p
\]

\[
residual\_margin = \Delta w^T residual_{s,p}
\]

9. Mark the dominant component as the component with the largest absolute margin contribution. The absolute contribution is used because a component can either increase or oppose the final margin.

Metrics:

- `dominant_component`: which component has the largest absolute contribution to the top-2 router margin.
- `common_margin_abs_frac`, `slot_margin_abs_frac`, `position_margin_abs_frac`, `residual_margin_abs_frac`: component absolute contribution divided by the absolute total margin.
- `route_switch_step`: first checkpoint where a slot's dominant expert changes.
- `stable_lock_step`: earliest checkpoint after which a slot's dominant expert no longer changes.

Result A meaning:

If slot margin dominates before and after lock-in, then the router is using the intended slot axis; collapse would need another explanation, such as expert utility or load dynamics.

Result B meaning:

If common, block-position, or residual margin dominates while slot signal is decodable, then collapse is more likely a router-logit selection problem: the router sees slot information but the top-1 decision is controlled by a non-slot direction.

Observation:

In the P1 baseline, the common component dominates the top-2 margin in most `(seed, slot, block_start)` rows.

| Step | Rows | Common dominant | Slot dominant | Position dominant | Residual dominant |
|---:|---:|---:|---:|---:|---:|
| 0 | 320 | 286 | 18 | 15 | 1 |
| 1 | 320 | 263 | 44 | 11 | 2 |
| 2 | 320 | 247 | 49 | 23 | 1 |
| 5 | 320 | 281 | 36 | 3 | 0 |
| 10 | 320 | 298 | 19 | 3 | 0 |
| 20 | 320 | 280 | 40 | 0 | 0 |
| 50 | 320 | 290 | 30 | 0 | 0 |
| 1600 | 320 | 290 | 30 | 0 | 0 |

Route lock-in:

- P1 has 32 slot-level rows across 8 seeds and 4 slots.
- All 32 rows have `stable_lock_step <= 10`.
- Only 4 rows ever switch dominant expert.

Central figure:

![P3 margin decomposition](figures/round1_slot_specialization_4gpu_20260609/p3_margin_decomposition_plots.png)

Interpretation:

P3 supports non-slot logit dominance, mainly common-component dominance rather than block-position dominance. The position component is visible early but becomes small by the final checkpoint. The common component can dominate router logits even when the hidden representation itself becomes almost entirely slot-decodable.

Supported:

P3 supports common-logit dominance as a mechanism for early and persistent route collapse.

Weakened:

The idea that final collapse is driven primarily by block-start position is weakened in this minimal no-position setting.

Insufficient evidence:

P3 does not by itself distinguish common-logit dominance from expert utility co-adaptation after routing. It only analyzes router logit components.

Cannot claim:

P3 does not prove that common-logit cancellation will solve the problem; that requires a Round-2 intervention.

Deliverables:

- `p3_margin_decomposition_by_checkpoint.csv`
- `p3_route_switch_table.csv`
- `p3_margin_decomposition_plots.png`
- `p3_route_switch_event_table.md`
- `p3_summary.md`

---

## 8. P4 Forced-Routing Utility Audit (Not Run)

Purpose:

P4 would test whether slot-specific experts have causal utility for prediction. This matters because routing alignment alone is not the same as useful expert specialization.

Planned question:

If examples from slot `s` are forced through expert `e`, does the slot-matched route have lower loss than mismatched routes?

What it would do:

P4 would take trained or controlled models, override the selected expert at the `B_CONST` position, and measure target loss under each forced `(slot, expert)` pair.

Primary metric:

Forced-route loss matrix by slot and expert. A useful slot-expert partition should show a diagonal or slot-consistent low-loss structure, not just balanced assignment.

Result A meaning:

If the forced-route loss matrix has a clear slot-aligned low-loss diagonal, then routed experts have causal utility for slots.

Result B meaning:

If forced losses are similar across experts, or if the best expert is common for all slots, then route-slot NMI alone would not prove useful specialization.

Round-1 status:

P4 was explicitly not run. Therefore this detailed record cannot claim that router-selected experts have causal slot utility. It can only claim collapse, slot-signal visibility, router-logit dominance, and reachability under positive control.

---

## 9. P5 Slot-Initialized Positive Control

Question:

If early random lock-in is removed, is slot-to-expert specialization reachable and stable?

Setup:

P5 uses the same dataset and model constraints as P1. At step 0, it collects `h_B`, estimates slot centroids, initializes the router with slot directions, and then calibrates the bias-free linear router on `h_B -> slot_id`. The calibration updates only the router weights and is used as a favorable initialization positive control.

How it was done:

1. Build a balanced calibration set with the same `D_min_block_shift` construction.
2. Run the randomly initialized model before training and collect `h_B` at `B_CONST`.
3. Compute one centroid per slot:

\[
\mu_s = mean(h_B \mid slot=s)
\]

4. Center the slot centroids by subtracting the mean centroid and optionally whiten the directions using the empirical covariance of `h_B`.
5. Normalize the four slot directions and copy them into the four router weight rows.
6. Calibrate only the router weights as a bias-free linear classifier from `h_B` to `slot_id` for 400 steps.
7. Require step-0 slot-to-expert NMI to exceed 0.90 before continuing.
8. Train normally for 1600 steps with the same loss, optimizer, data, and sparse top-1 routing as P1.

Metrics:

- `slot_to_expert_NMI`: decides whether routed expert identity aligns with slot identity.
- `max_load`: decides whether the route partition is collapsed or balanced.
- `active_experts`: checks whether all experts are used.
- `target_accuracy`: checks whether preserving slot routing still solves the task.
- `p5_route_switch_after_release.csv`: checks whether the initialized slot partition erodes during training.

Result A meaning:

If P5 preserves high NMI, low max load, all four active experts, and high accuracy, then the slot partition is reachable and mostly stable once the router starts in the intended partition.

Result B meaning:

If P5 collapses despite favorable initialization, then the task/objective/expert capacity may make slot specialization unstable even when the correct partition is provided.

Boundary of P5:

P5 is not evidence that vanilla random-initialized sparse top-1 MoE naturally discovers slot specialization. It only tests reachability and stability once the router starts in the intended partition.

Observation:

| Metric | Mean | Min | Max |
|---|---:|---:|---:|
| `target_accuracy` | 1.000 | 1.000 | 1.000 |
| `slot_to_expert_NMI` | 0.980 | 0.842 | 1.000 |
| `per_slot_route_purity` | 0.997 | 0.975 | 1.000 |
| `max_load` | 0.278 | 0.250 | 0.475 |
| `active_experts` | 4.000 | 4.000 | 4.000 |

Seven of eight seeds preserve perfect slot-to-expert routing at the final checkpoint. Seed `20260524` shows mild erosion with `slot_to_expert_NMI=0.842` and `max_load=0.475`, but it still uses all four experts and does not meet the protocol collapse threshold.

Central figure:

![P5 baseline vs positive control](figures/round1_slot_specialization_4gpu_20260609/p5_baseline_vs_positive_control.png)

Interpretation:

Slot specialization is reachable and mostly stable under favorable initialization. Therefore the P1 failure is not because slot specialization is impossible under the task, model capacity, or objective.

Supported:

P5 supports the reachability interpretation: a slot partition can be maintained while preserving perfect target accuracy.

Weakened:

The claim that correct slot specialization is inherently unstable in this minimal task is weakened.

Insufficient evidence:

P5 does not show that an unsupervised router can enter the correct partition without labels or calibration.

Cannot claim:

P5 does not solve anti-lock-in and does not prove a deployable method.

Deliverables:

- `p5_metrics_by_seed.csv`
- `p5_route_confusion_by_seed.csv`
- `p5_baseline_vs_positive_control.png`
- `p5_route_switch_after_release.csv`
- `p5_summary.md`

---

## 10. Required Final Questions

### 1. Did the clean minimal dataset reproduce collapse?

Yes. P1 reaches accuracy 1.0 in every seed, while final mean `max_load=0.969`, mean `slot_to_expert_NMI=0.080`, and hard collapse rate is 1.0 under the protocol threshold `max_load >= 0.70`.

### 2. Was slot information decodable from the routed hidden state?

Yes. P2 final slot probe accuracy is 1.0 on both random split and held-out block-start split for all P1 seeds.

### 3. Which logit component drove route changes?

The common component dominates the P1 top-2 margin in most rows: 286 / 320 at step 0 and 290 / 320 at final step 1600. Position contribution is not the main final driver in this no-position setting.

### 4. Was slot specialization reachable under positive control?

Yes. P5 reaches mean final `slot_to_expert_NMI=0.980`, mean `max_load=0.278`, and accuracy 1.0. Seven of eight seeds are perfectly balanced with `max_load=0.25`; one seed has mild erosion but no collapse.

### 5. What is the next scientific decision?

Round 2 should test whether a trainable router can enter or preserve the reachable slot/exact-feature partition without oracle labels, using targeted interventions such as common-logit cancellation, feature-aware initialization, or anti-lock-in.

---

## 11. Result Files

Result directory:

`results/round1_slot_specialization_4gpu_20260609/`

Figure directory:

`figures/round1_slot_specialization_4gpu_20260609/`

Core tables:

- `summary_by_variant.csv`
- `final_metrics_by_seed.csv`
- `metrics_by_step.csv`
- `route_confusion_by_step.csv`
- `accuracy_by_slot.csv`
- `accuracy_by_block_start.csv`
- `p2_probe_metrics_by_checkpoint.csv`
- `p3_margin_decomposition_by_checkpoint.csv`
- `p3_route_switch_table.csv`

Core figures:

- `p1_route_heatmaps.png`
- `p1_max_load_trajectory.png`
- `p1_slot_nmi_trajectory.png`
- `p1_accuracy_trajectory.png`
- `p2_probe_accuracy_trajectory.png`
- `p3_margin_decomposition_plots.png`
- `p5_baseline_vs_positive_control.png`

Checkpoint artifacts:

Each per-seed run stores checkpoint artifacts under:

`results/round1_slot_specialization_4gpu_20260609/cosine/<variant>/seed_<seed>/checkpoint_artifacts/`

Each checkpoint artifact contains:

- model state;
- router weight;
- slot labels;
- block-start labels;
- route positions;
- targets;
- predictions;
- route assignments;
- router logits at `B_CONST`;
- hidden states at `B_CONST`.

These checkpoint artifacts are audit material and should not be committed as curated Git artifacts.

---

## 12. Claim Boundary

Can claim:

1. In `D_min_block_shift`, vanilla sparse top-1 routing collapses despite perfect task learning.
2. Slot information is linearly decodable from `h_B`, including across held-out block positions.
3. Common-component logit dominance is the strongest Round-1 logit-level explanation.
4. Slot specialization is reachable and mostly stable under favorable router initialization.

Cannot claim:

1. The same result holds for multi-B exact-feature routing.
2. The same mechanism holds in full language modeling or real representations.
3. P5 is a deployable method or proof that vanilla training can discover the partition.
4. Anti-lock-in or inhibition solves the problem, because P6 was not run.
5. Router-selected experts have causal utility for each slot, because P4 was not run.

Insufficient evidence:

The current result does not decide whether common-logit cancellation alone is enough, whether expert utility co-adaptation contributes after lock-in, or whether a label-free feature-aware router can enter the correct partition.

---

## 13. Next Step

Run a Round-2 intervention test. The smallest next decision is:

Does targeted common-logit cancellation or feature-aware anti-lock-in make the trainable sparse top-1 router enter the reachable slot/exact-feature partition without oracle labels?
