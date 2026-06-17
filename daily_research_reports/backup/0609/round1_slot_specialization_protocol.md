# Round-1 Protocol: Minimal Slot-Block Collapse Audit for Sparse Top-1 MoE

## 0. Execution Status

This is the **Round-1 source-of-truth protocol**.

Run only:

```text
P0 Dataset Audit
P1 Clean Baseline Re-Collapse
P2 Slot Signal Probe
P3 Logit Trajectory Decomposition
P5 Slot-Initialized Positive Control
```

Do **not** run in Round 1:

```text
P4 forced-routing utility audit
P6 anti-lockin intervention
P7 slot-order diagnostic
```

Reason:

```text
Round 1 must first establish whether the clean minimal setting still collapses,
whether slot information exists in the routed hidden state,
which logit component drives route changes,
and whether slot specialization is reachable under favorable initialization.
```

---

## 1. Scientific Question

### Parent Problem

Why does ordinary sparse top-1 MoE gating fail to stably form feature-to-expert specialization?

### Current Subproblem

After removing explicit positional encoding and moving the slot block across sequence positions, why does routing still collapse during training?

### Round-1 Decision Question

In the minimal uniform slot task, does collapse come from:

```text
A. missing slot signal in the routed hidden state;
B. non-slot logit dominance from common / prefix-position components;
C. early sparse top-1 lock-in from random initialization;
D. or insufficient evidence?
```

---

## 2. Non-Negotiable Scope

### 2.1 Router Type

Study only:

```text
sparse top-1 differentiable MoE
```

Meaning:

```text
For each routed token, the forward pass selects exactly one expert:
    e_i = argmax_e z_{i,e}
```

Not studied:

```text
soft routing;
probability-weighted multi-expert mixture;
soft-to-hard routing schedule;
top-k routing with k > 1.
```

### 2.2 Position Encoding

Round 1 uses:

```text
no positional encoding throughout training and evaluation
```

Implementation requirement:

```text
Position embeddings must be removed, zeroed, or disabled from initialization.
Do not merely freeze a trained position embedding.
```

### 2.3 B Token

Round 1 uses:

```text
one fixed B token: B_CONST
```

Do not vary B in Round 1.

Reason:

```text
Round 1 tests whether slot-specialization is possible in the cleanest setting.
B variation would introduce an additional nuisance component and should be saved for Round 2.
```

---

## 3. Minimal Data Construction

### 3.1 Dataset Name

```text
D_min_block_shift
```

### 3.2 Vocabulary

Default:

```text
num_slots S = 4
num_experts E = 4
sequence_length L = 12
slot tokens = SLOT_0, SLOT_1, SLOT_2, SLOT_3
fixed B token = B_CONST
target tokens = Y_0, Y_1, Y_2, Y_3
filler token = FILL
```

The target rule is deterministic:

```text
SLOT_s -> Y_s
```

### 3.3 Sequence Form

Each sequence contains a contiguous causal block:

```text
FILL ... FILL SLOT_s B_CONST Y_s FILL ... FILL
```

Equivalently:

```text
prefix filler + SLOT_s B_CONST Y_s + suffix filler
```

Important:

```text
There must be no filler between SLOT_s and B_CONST.
There must be no filler between B_CONST and Y_s.
The whole SLOT_s B_CONST Y_s block moves across the sequence.
```

### 3.4 Sampling Rule

For each example:

```text
s ~ Uniform({0, 1, 2, 3})
p ~ Uniform(valid block start positions)
sequence[p]     = SLOT_s
sequence[p + 1] = B_CONST
sequence[p + 2] = Y_s
all other positions = FILL
```

Valid block starts:

```text
p in {0, 1, ..., L - 3}
```

### 3.5 Balanced Epoch Construction

Do not rely on iid random sampling alone.

Construct each epoch by enumerating:

```text
all pairs (slot s, block_start p)
```

Then repeat each pair equally often and shuffle.

Required checks:

```text
count(slot=s) equal for all s
count(block_start=p) equal for all p
count(slot=s, block_start=p) equal for all valid pairs
```

### 3.6 Loss and Routing Position

Training loss:

```text
Compute next-token prediction loss only at the B_CONST position.
```

For each sequence:

```text
routed position = p + 1
input hidden state = h_B = hidden state at B_CONST
target = Y_s
```

Route statistics:

```text
Compute routing metrics only at the B_CONST position.
Ignore routing behavior at filler / slot / target positions.
```

---

## 4. Model and Training Requirements

### 4.1 Architecture

Use the existing small causal Transformer + MoE setup, with these constraints:

```text
MoE layer contains E = 4 experts.
Router is bias-free unless the existing baseline requires otherwise.
Router forward is sparse top-1.
Position encoding is disabled.
Auxiliary load-balance loss is disabled in Round 1 baseline.
```

### 4.2 Seeds

Minimum:

```text
8 random seeds
```

Preferred:

```text
16 random seeds
```

Use the same seed list for all variants.

### 4.3 Checkpoints

Save dense early checkpoints:

```text
step 0
steps 1, 2, 5, 10, 20, 50, 100, 200, 500
then every fixed interval until final
```

If training is short, use:

```text
save every 5-10 steps for the first 300 steps
save every 50-100 steps afterwards
```

Must save:

```text
model weights
router weights
route assignments at B position
router logits at B position
hidden states at B position
training loss and target accuracy
```

---

## 5. Shared Metrics

### 5.1 Task Learning

```text
target_accuracy
cross_entropy_loss
accuracy_by_slot
accuracy_by_block_start
```

Interpretation:

```text
High accuracy + low slot specialization means the task was learned but routing did not specialize by slot.
Low accuracy means routing evidence is not cleanly interpretable.
```

### 5.2 Slot Specialization

Compute only on B_CONST positions.

```text
slot_to_expert_NMI = normalized mutual information between slot_id and routed_expert
per_slot_route_purity = mean_s max_e P(e | s)
slot_expert_confusion = matrix P(e | s)
```

Interpretation:

```text
High NMI + high per-slot purity = slot-consistent routing.
Balanced load alone is not slot-specialization.
```

### 5.3 Collapse

```text
expert_load = P(e)
max_load = max_e P(e)
load_entropy = entropy(P(e))
dominant_expert_persistence = fraction of checkpoints with the same dominant expert
collapse_rate = fraction of seeds with final max_load above threshold
```

Default thresholds for E = 4:

```text
hard collapse: final max_load >= 0.70
partial collapse: final max_load >= 0.50 and slot_to_expert_NMI < 0.50
```

### 5.4 Trajectory

```text
top1_expert_by_slot_over_time
top2_logit_margin_by_slot_over_time
route_switch_step_by_slot
stable_lock_step_by_slot
component_contribution_to_logit_margin
```

Definitions:

```text
route_switch_step:
    first checkpoint where the dominant routed expert for a slot changes.

stable_lock_step:
    earliest checkpoint after which the dominant routed expert for a slot no longer changes.
```

---

## 6. P0: Dataset Audit

### Question

Is the Round-1 dataset truly balanced and free from slot-position shortcuts?

### Run

Before any model training, compute:

```text
count(slot)
count(block_start)
count(slot, block_start)
count(target | slot)
count(target | block_start)
loss_mask_position distribution
route_position distribution
```

### Required Checks

```text
P(slot) uniform
P(block_start) uniform
P(slot, block_start) uniform
Y_s deterministic from slot
Y_s not predictable from block_start alone
loss mask always at B_CONST position
route stats always collected at B_CONST position
```

### Pass Criteria

```text
all slot counts equal or within pre-fixed tolerance
all block_start counts equal or within pre-fixed tolerance
all slot × block_start counts equal or within pre-fixed tolerance
target = Y_s for every example
```

### If P0 Fails

Stop. Fix data generation before running any model experiment.

### Deliverables

```text
p0_dataset_audit.json
p0_dataset_audit.md
```

---

## 7. P1: Clean Baseline Re-Collapse

### Question

In the minimal clean setting, does ordinary sparse top-1 MoE still collapse during training?

### Dataset

```text
D_min_block_shift
```

### Model Variant

```text
ordinary sparse top-1 MoE
random router initialization
no position encoding
B fixed
no auxiliary load-balance loss
```

### Run

Train for all seeds using the same dataset and checkpoint schedule.

For each checkpoint, collect:

```text
route assignment at B_CONST position
router logits at B_CONST position
hidden state h_B
target accuracy
loss
```

### Primary Metrics

```text
final max_load
final slot_to_expert_NMI
final per_slot_route_purity
target_accuracy
collapse_rate across seeds
max_load trajectory
slot_NMI trajectory
```

### Supports Collapse Study If

```text
target_accuracy is high;
final max_load is high;
slot_to_expert_NMI and per-slot purity are low or unstable across seeds.
```

### Weakens Current Anchor If

```text
D_min_block_shift does not collapse;
or the model fails to learn the target mapping.
```

### Interpretation

If P1 shows high accuracy but poor slot routing:

```text
The task is learnable, but ordinary sparse top-1 routing does not naturally form slot-specialization in this clean setting.
```

### Deliverables

```text
p1_metrics_by_seed.csv
p1_route_confusion_by_seed.csv
p1_route_heatmaps.png
p1_max_load_trajectory.png
p1_slot_nmi_trajectory.png
p1_accuracy_trajectory.png
p1_summary.md
```

---

## 8. P2: Slot Signal Probe

### Question

Does the routed hidden state at B_CONST contain decodable slot information?

### Dataset and Checkpoints

Use P1 checkpoints on `D_min_block_shift`.

### Hidden State

For each example:

```text
h_B = hidden state at B_CONST position
label = slot_id s
nuisance = block_start p
```

### Probe Tasks

Train linear probes:

```text
probe_slot: h_B -> slot_id
probe_position: h_B -> block_start
```

Use at least two splits:

```text
random split
held-out block_start split
```

The held-out block_start split tests whether slot information generalizes across block positions.

### Primary Metrics

```text
slot_probe_accuracy_random_split
slot_probe_accuracy_heldout_position
position_probe_accuracy
slot_component_variance_ratio
```

### Component Variance Ratio

Estimate:

```text
c = mean_{s,p} h(s,p)
r_s = mean_p h(s,p) - c
u_p = mean_s h(s,p) - c
```

Report:

```text
||r_s||^2 contribution relative to total hidden variance
||u_p||^2 contribution relative to total hidden variance
```

### Supports Gating-Dynamics Hypothesis If

```text
slot is linearly decodable from h_B,
especially on held-out block_start positions,
but P1 routing is not slot-specialized.
```

### Weakens Gating-Dynamics Hypothesis If

```text
slot is not decodable from h_B.
```

### Interpretation

```text
slot decodable + routing not slot-specialized:
    router/gating dynamics problem.

slot not decodable:
    representation problem; do not blame router specialization yet.
```

### Deliverables

```text
p2_probe_metrics_by_checkpoint.csv
p2_probe_accuracy_trajectory.png
p2_component_variance.csv
p2_summary.md
```

---

## 9. P3: Logit Trajectory Decomposition

### Question

When routing changes, is the top-1 decision driven by the slot component or by non-slot common / block-position components?

### Dataset and Checkpoints

Use P1 checkpoints on `D_min_block_shift`.

### Round-1 Hidden Decomposition

Since B is fixed and template is fixed, use only:

```text
h(s,p) = c + r_s + u_p + residual
```

where:

```text
c: global common component
r_s: slot-specific component
u_p: block-start / prefix-position component
residual: unexplained term
```

Estimate:

```text
c = mean_{s,p} h(s,p)
r_s = mean_p h(s,p) - c
u_p = mean_s h(s,p) - c
residual(s,p) = h(s,p) - c - r_s - u_p
```

If the additive decomposition is numerically unstable, use least-squares ANOVA with sum-to-zero constraints.

### Router Logit

For expert e:

```text
z_e(s,p) = w_e^T h(s,p)
```

For current top-1 expert e* and runner-up expert e':

```text
margin(s,p) = z_{e*}(s,p) - z_{e'}(s,p)
```

Decompose margin:

```text
common_margin      = (w_{e*} - w_{e'})^T c
slot_margin        = (w_{e*} - w_{e'})^T r_s
position_margin    = (w_{e*} - w_{e'})^T u_p
residual_margin    = (w_{e*} - w_{e'})^T residual(s,p)
```

### Primary Metrics

```text
component contribution to top-2 margin
slot_margin / total_margin
common_margin / total_margin
position_margin / total_margin
component that predicts final dominant expert earliest
route_switch_step by slot
stable_lock_step by slot
```

### Supports Non-Slot Logit Dominance If

```text
before route lock-in, common_margin or position_margin predicts the final dominant expert better than slot_margin.
```

### Weakens Non-Slot Logit Dominance If

```text
slot_margin dominates from early training, but routing still collapses.
```

### Interpretation

```text
If non-slot margin drives switch:
    collapse is logit-level non-slot dominance.

If slot margin drives switch but final routing still collapses:
    logit decomposition is insufficient; later experiments must inspect top-1 training dynamics or expert utility.
```

### Deliverables

```text
p3_margin_decomposition_by_checkpoint.csv
p3_route_switch_table.csv
p3_margin_decomposition_plots.png
p3_route_switch_event_table.md
p3_summary.md
```

---

## 10. P5: Slot-Initialized Positive Control

### Question

If early random lock-in is removed, is slot-to-expert specialization reachable and stable?

### Why P5 Exists

P5 is a positive control, not the main causal explanation.

It tests:

```text
Can the model maintain slot-specialization under favorable initialization?
```

It does not prove:

```text
ordinary random-initialized sparse top-1 MoE naturally learns slot-specialization.
```

### Dataset

Use exactly the same dataset:

```text
D_min_block_shift
```

Keep:

```text
no position encoding
B fixed
loss only at B_CONST position
route stats only at B_CONST position
```

### P5A: Slot-Centroid Router Initialization

Required variant.

Procedure:

```text
1. At step 0, collect h_B for all slots and block positions.
2. Estimate slot centroids mu_s = mean_p h(s,p).
3. Initialize router rows so that SLOT_s is routed to expert e_s.
4. Use mapping:
       SLOT_0 -> expert 0
       SLOT_1 -> expert 1
       SLOT_2 -> expert 2
       SLOT_3 -> expert 3
5. Train with ordinary sparse top-1 routing after initialization.
```

Allowed implementation choices:

```text
nearest-centroid linear classifier initialization;
least-squares classifier from h_B to slot_id;
manually set w_e to slot residual directions r_s if numerically stable.
```

Required check at step 0:

```text
slot_to_expert_NMI should be high;
per-slot purity should be high;
all experts should receive at least one slot.
```

If this check fails, fix initialization before training.

### P5B: Forced-Slot Warmup Then Release

Optional Round-1 variant. Run only if P5A is ambiguous or fails unexpectedly.

Procedure:

```text
1. For K warmup steps, override top-1 assignment:
       SLOT_s -> expert e_s
2. Train experts under this forced sparse assignment.
3. Release to ordinary sparse top-1 router.
4. Continue training and track whether slot routing persists or collapses.
```

Important:

```text
This is not soft routing.
Each example still uses exactly one expert.
This is an oracle positive control and cannot be used as random-init evidence.
```

### Primary Metrics

```text
slot_to_expert_NMI
per_slot_route_purity
max_load
target_accuracy
route_switch_count_after_release
time_to_collapse_after_release
```

### Supports Reachability If

```text
P5 maintains high slot_NMI and purity across seeds while preserving high target accuracy.
```

### Weakens Reachability If

```text
P5 collapses into shared experts despite favorable initialization or warmup.
```

### Interpretation

If P5 succeeds and P1 fails:

```text
slot-specialization is reachable;
baseline failure is likely caused by early random lock-in or non-slot logit dominance.
```

If P5 fails:

```text
failure is not merely early random lock-in;
inspect representation quality, expert capacity, objective geometry, or whether slot-specialization is unstable under this task.
```

### Deliverables

```text
p5_metrics_by_seed.csv
p5_route_confusion_by_seed.csv
p5_baseline_vs_positive_control.png
p5_route_switch_after_release.csv
p5_summary.md
```

---

## 11. Minimal Run Order

Run exactly in this order:

```text
1. P0 dataset audit
2. P1 clean baseline re-collapse
3. P2 slot signal probe
4. P3 logit trajectory decomposition
5. P5 slot-initialized positive control
```

Stop rules:

```text
If P0 fails:
    stop and fix data.

If P1 does not collapse and learns well:
    current collapse anchor may not apply to this minimal setting.

If P1 does not learn:
    fix task/model before interpreting routing.

If P2 shows no slot signal:
    stop gating-dynamics story and study representation formation.

If P2 shows slot signal and P3 shows non-slot margin dominance:
    proceed to P5 to test reachability.

If P5 succeeds:
    next round should study anti-lockin / feature-aware router intervention.

If P5 fails:
    next round should audit expert capacity and objective stability.
```

---

## 12. Expected Decision Outcomes

### Outcome A: Clean Baseline Collapses, Slot Signal Exists

Required evidence:

```text
P1: high accuracy, low slot_NMI, high max_load
P2: high slot probe accuracy, including held-out positions
```

Conclusion:

```text
The routed hidden state contains slot information, but ordinary sparse top-1 routing does not use it to specialize.
```

Next:

```text
Use P3 to identify whether common / position component dominates logits.
```

---

### Outcome B: Slot Signal Missing

Required evidence:

```text
P2 slot probe accuracy is low or does not generalize across block positions.
```

Conclusion:

```text
The failure is representation-side, not primarily router-side.
```

Next:

```text
Redesign representation / data before studying gating specialization.
```

---

### Outcome C: Non-Slot Logit Dominance

Required evidence:

```text
P3: common_margin or position_margin predicts route switch / final dominant expert better than slot_margin.
```

Conclusion:

```text
Collapse is driven by non-slot logit dominance in the router decision.
```

Next:

```text
Round 2 should test common-logit cancellation or feature-aware anti-lockin.
```

---

### Outcome D: P5 Succeeds, P1 Fails

Required evidence:

```text
P1: baseline low slot_NMI or collapse
P5: high slot_NMI, high purity, high accuracy across seeds
```

Conclusion:

```text
Slot-specialization is reachable, but ordinary random-initialized sparse top-1 training does not reliably discover it.
```

Next:

```text
Study early lock-in and design initialization / anti-lockin mechanism.
```

---

### Outcome E: P5 Also Fails

Required evidence:

```text
P5 collapses or loses accuracy despite slot-aware initialization/warmup.
```

Conclusion:

```text
The target slot-specialization may be unstable under the current objective, expert capacity, or representation.
```

Next:

```text
Audit expert capacity, objective, and hidden-state slot separability.
```

---

## 13. Required Final Report Format

For each protocol, report:

```text
Question:
Setup:
Observation:
Interpretation:
Supported:
Weakened:
Insufficient evidence:
Cannot claim:
Next decision:
```

Final summary must answer:

```text
1. Did the clean minimal dataset reproduce collapse?
2. Was slot information decodable from the routed hidden state?
3. Which logit component drove route changes?
4. Was slot-specialization reachable under positive control?
5. What is the next scientific decision?
```

---

## 14. Required Output Directory Structure

Use this structure:

```text
round1_slot_specialization/
  config/
    dataset_config.yaml
    model_config.yaml
    training_config.yaml
    seed_list.txt
  p0_dataset_audit/
    p0_dataset_audit.json
    p0_dataset_audit.md
  p1_clean_baseline/
    p1_metrics_by_seed.csv
    p1_route_confusion_by_seed.csv
    p1_route_heatmaps.png
    p1_max_load_trajectory.png
    p1_slot_nmi_trajectory.png
    p1_accuracy_trajectory.png
    p1_summary.md
  p2_slot_signal_probe/
    p2_probe_metrics_by_checkpoint.csv
    p2_probe_accuracy_trajectory.png
    p2_component_variance.csv
    p2_summary.md
  p3_logit_trajectory/
    p3_margin_decomposition_by_checkpoint.csv
    p3_route_switch_table.csv
    p3_margin_decomposition_plots.png
    p3_route_switch_event_table.md
    p3_summary.md
  p5_positive_control/
    p5_metrics_by_seed.csv
    p5_route_confusion_by_seed.csv
    p5_baseline_vs_positive_control.png
    p5_route_switch_after_release.csv
    p5_summary.md
  final_report/
    round1_summary.md
    round1_detailed.md
```

---

## 15. Forbidden Claims

Do not claim:

```text
position embedding is the only cause;
common component fully explains final collapse;
load balance equals slot-specialization;
positive control proves natural emergence;
forced warmup is ordinary training;
this result transfers to real language models;
soft routing was studied.
```

Allowed claim only if supported:

```text
In the minimal no-position slot-block setting, ordinary sparse top-1 MoE either does or does not form stable slot-to-expert specialization.
If slot signal is decodable but routing collapses, the failure is not due to missing slot information alone.
If P5 succeeds while P1 fails, slot-specialization is reachable but not reliably discovered by ordinary random-initialized sparse top-1 training.
```
