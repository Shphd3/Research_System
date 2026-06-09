# Protocols: Slot-Specialization Failure and Collapse in Sparse Top-1 MoE

## 0. Protocol Goal

We study why a sparse top-1 MoE router fails to form stable slot-to-expert specialization in a uniform synthetic task after explicit position-common signals are controlled.

Core decision question:

```text
In a uniform slot-feature task, does post-position-control collapse come from:
1. missing slot signal in the routed hidden state;
2. residual non-slot logit bias from common / B / template components;
3. sparse top-1 training lock-in;
4. or insufficient evidence?
```

Scope:

```text
Studied: sparse top-1 differentiable MoE.
Not studied: soft routing, probability-weighted multi-expert routing, real-LM transfer.
```

Sparse top-1 definition:

```text
For each routed token, the router selects exactly one expert:
    e_i = argmax_e z_{i,e}

Training uses the implementation's differentiable top-1 estimator or selected-path gradient.
No experiment replaces the forward pass with a soft mixture of experts.
Forced routing is allowed only as an evaluation diagnostic or as an explicit positive-control intervention.
```

---

## 1. Synthetic Data Design

### 1.1 Why we need a new dataset

Previous data may mix three factors:

```text
slot identity;
absolute position / fixed template;
local B-token identity.
```

This protocol needs a dataset where slot identity is the only causal target factor, while B-token, position, and template are nuisance variables. Otherwise, final routing cannot distinguish slot-specialization from shortcut-driven collapse.

---

### 1.2 Main dataset: `D_clean_slot_B_target`

Each sequence contains one causal slot token, one routed B-token, and one target token.

Default values:

```text
num_slots S = 4
num_experts E = 4
num_B_tokens B = 16
num_template_variants T = 16
sequence_length L = 12
slot tokens: SLOT_0 ... SLOT_3
B tokens: B_0 ... B_15
target tokens: Y_0 ... Y_3
```

Generative rule:

```text
s ~ Uniform({0, ..., S-1})
b ~ Uniform({0, ..., B-1})
template_id ~ Uniform({0, ..., T-1})
p_slot ~ Uniform(valid slot positions)
gap ~ Uniform({1, 2, 3})
p_route = p_slot + gap
p_target = p_route + 1
y = Y_s
```

Sequence form:

```text
[ filler / template tokens ... SLOT_s ... filler ... B_b Y_s ... filler ]
```

Training objective:

```text
Only the B_b position is loss-masked for next-token prediction:
    h_i = hidden state at B_b
    target = Y_s
```

Routed hidden state:

```text
h_i = hidden(B_b)
```

Why route at `B_b`:

```text
B_b is a strong local nuisance token.
The target depends only on the earlier slot.
Therefore this setting tests whether the router uses slot information rather than local B/template information.
```

Hard constraints:

```text
P(s) is uniform.
P(b) is uniform.
P(p_slot | s) is uniform.
P(p_route | s) is uniform up to valid-position constraints.
B-token identity is independent of slot identity.
Template identity is independent of slot identity.
Target Y_s never appears in the input context before the target position.
```

Balanced epoch construction:

```text
Build each epoch by enumerating the full Cartesian product:
    slot s × B-token b × valid position pattern p × template_id t

Then shuffle according to the selected schedule.
This avoids finite-sample slot / B / position imbalance.
```

---

### 1.3 Dataset variants

#### D0: `fixed_position_oldstyle`

Purpose:

```text
Replicate old-style collapse and preserve continuity with previous runs.
```

Construction:

```text
slot position fixed;
B position fixed;
template mostly fixed;
position embeddings enabled.
```

Use:

```text
Sanity baseline only. Not the main evidence source.
```

---

#### D1: `no_pos_random_position_main`

Purpose:

```text
Main dataset for post-position-control collapse.
```

Construction:

```text
position embeddings disabled or zeroed throughout training;
slot position randomized;
B position randomized after slot;
template randomized;
fully balanced epoch.
```

Use:

```text
Primary dataset for P1-P6.
```

---

#### D2: `pos_enabled_random_position`

Purpose:

```text
Check whether randomizing slot/B positions is enough even when position embeddings exist.
```

Construction:

```text
same as D1, but position embeddings enabled.
```

Use:

```text
Secondary position/template ablation.
```

---

#### D3: `no_pos_fixed_template`

Purpose:

```text
Separate position effects from fixed-template effects.
```

Construction:

```text
position embeddings disabled;
slot/B positions fixed;
template fixed or low-diversity.
```

Use:

```text
If collapse persists in D1, D3 helps determine whether random template diversity matters.
```

---

## 2. Model and Training Setting

Default architecture:

```text
small causal transformer;
MoE FFN layer with E = S experts;
sparse top-1 router;
router weight matrix W_r has no explicit bias;
experts receive the full hidden state h_i;
route statistics are computed only on routed B-token positions.
```

Default training:

```text
loss = cross_entropy(next_token = Y_s at B_b position)
optimizer and learning rate: keep identical across variants
number of seeds: at least 8; preferably 16
checkpoint cadence: dense early checkpoints, sparse late checkpoints
```

Suggested checkpoint cadence:

```text
save every 5-10 steps for first 300 steps;
save every 50-100 steps afterwards;
always save step 0, first route-switch checkpoint, final checkpoint.
```

Do not change during the main comparison:

```text
number of slots;
number of experts;
expert hidden size;
training tokens;
optimizer;
loss mask;
random seed list.
```

---

## 3. Shared Metrics

### 3.1 Specialization metrics

```text
slot_to_expert_NMI = NMI(slot_id, routed_expert)
per_slot_route_purity = mean_s max_e P(e | s)
slot_split_count = number of experts used per slot across examples
```

Interpretation:

```text
High NMI + high per-slot purity = slot-consistent routing.
High load balance alone is not specialization.
```

---

### 3.2 Collapse metrics

```text
max_load = max_e P(e)
load_entropy = entropy(P(e))
dominant_expert_persistence = fraction of checkpoints with same dominant expert
collapse_rate = fraction of seeds whose final max_load exceeds the fixed threshold
```

Recommended initial threshold for E = 4:

```text
hard collapse: final max_load >= 0.70 over the final 20% of checkpoints
partial collapse: final max_load >= 0.50 and slot_NMI < 0.5
```

Thresholds may be adjusted, but must be fixed before reading results.

---

### 3.3 Task metrics

```text
target_accuracy
cross_entropy_loss
accuracy_by_slot
accuracy_by_B_token
accuracy_by_position
```

Interpretation:

```text
High target accuracy with low slot_NMI means the model learned the task but the router did not specialize by slot.
Low target accuracy means routing evidence is not interpretable as specialization failure.
```

---

### 3.4 Trajectory metrics

```text
top1_expert over time
top2_logit_margin over time
route_switch_step
stable_lock_step
component contribution to logit margin
router update effect on future logits
forced-route expert utility
route_utility_match
```

Definitions:

```text
route_switch_step: first checkpoint where the top-1 expert changes for a slot group.
stable_lock_step: earliest checkpoint after which the slot group's dominant expert no longer changes.
route_utility_match: chosen expert equals the best expert under forced-routing evaluation.
```

---

## 4. Hidden-State and Logit Decomposition

Use routed hidden states at the B-token position.

For checkpoint t:

```math
h_i = c + r_{s_i} + q_{b_i} + u_{p_i} + m_{	au_i} + \epsilon_i
```

where:

```text
c: global common component
r_s: slot-specific component
q_b: B-token component
u_p: routed-position component
m_tau: template component
epsilon: residual
```

Estimate with balanced means and sum-to-zero constraints:

```text
c = mean_i h_i
r_s = mean(h_i | slot=s) - c
q_b = mean(h_i | B=b) - c
u_p = mean(h_i | route_position=p) - c
m_tau = mean(h_i | template=tau) - c
```

If components are not additive enough, use least-squares ANOVA decomposition with sum-to-zero constraints.

Router logit:

```math
z_{i,e} = w_e^T h_i
```

Top-2 margin decomposition:

```math
\Delta z_i = (w_{e^*} - w_{e'})^T h_i
```

```text
e*: current top-1 expert
e': runner-up expert
```

Component contributions:

```math
\Delta z_i = \Delta z_c + \Delta z_{slot} + \Delta z_B + \Delta z_{pos} + \Delta z_{template} + \Delta z_{residual}
```

Primary trajectory question:

```text
At the route-switch or lock-in step, which component caused the top-1 margin to cross zero?
```

---

## 5. Protocol P0: Dataset Audit

### Question

Did the dataset actually remove non-slot shortcuts and sampling imbalance?

### Run

For every dataset variant, compute before training:

```text
count(slot)
count(B)
count(slot, B)
count(slot, position)
count(B, position)
count(slot, template)
count(target | slot)
count(target | B)
count(target | position)
```

### Primary metrics

```text
max deviation from uniform count
mutual_information(slot, B)
mutual_information(slot, position)
mutual_information(slot, template)
mutual_information(target, B)
mutual_information(target, position)
```

### Supports

```text
All nuisance correlations are near zero.
Target is deterministic from slot and not predictable from B or position.
```

### Weakens

```text
Any nuisance variable predicts target or slot above the pre-fixed tolerance.
```

### New knowledge

```text
This closes the data-shortcut explanation before mechanism experiments.
```

---

## 6. Protocol P1: Clean Baseline Re-Collapse

### Question

Does sparse top-1 MoE still collapse in the clean no-position randomized-slot dataset?

### Dataset

```text
Primary: D1 no_pos_random_position_main
Secondary: D0 fixed_position_oldstyle, D2 pos_enabled_random_position
```

### Intervention

```text
No intervention.
Train the ordinary sparse top-1 MoE baseline.
```

### Primary metrics

```text
final max_load
collapse_rate across seeds
slot_to_expert_NMI
per_slot_route_purity
target_accuracy
dominant_expert_persistence
```

### Supports collapse mechanism study

```text
Accuracy is high, but final max_load is high and slot_NMI / purity are low.
```

### Weakens current direction

```text
D1 does not collapse, or accuracy is too low to interpret routing.
```

### New knowledge

```text
This establishes whether the new clean dataset reproduces the phenomenon that needs explanation.
```

---

## 7. Protocol P2: Slot Signal Probe

### Question

Is slot identity linearly decodable from the routed hidden state after position-common control?

### Dataset

```text
Use checkpoints from P1 on D1.
```

### Run

For each checkpoint:

```text
collect h_i at routed B-token positions;
train linear probe: h_i -> slot_id;
train nuisance probes: h_i -> B_id, route_position, template_id;
report train/test split by held-out B and held-out position.
```

Probe splits:

```text
in-distribution split: random examples;
held-out-B split: train on subset of B tokens, test on unseen B tokens;
held-out-position split: train on subset of route positions, test on unseen positions.
```

### Primary metrics

```text
slot_probe_accuracy
slot_probe_accuracy_heldout_B
slot_probe_accuracy_heldout_position
B_probe_accuracy
position_probe_accuracy
variance ratio of slot component ||r_s||^2 / E||h||^2
```

### Supports gating-dynamics hypothesis

```text
Slot is decodable from h_i, including held-out B and held-out positions, but routing is not slot-specialized.
```

### Weakens gating-dynamics hypothesis

```text
Slot is not decodable from h_i.
```

### New knowledge

```text
This separates representation failure from router failure.
```

---

## 8. Protocol P3: Logit Trajectory Decomposition

### Question

When routing changes, is the top-1 decision driven by slot component or non-slot component?

### Dataset

```text
Use P1 checkpoints on D1.
```

### Run

For each checkpoint:

```text
1. collect h_i, slot_id, B_id, route_position, template_id, routed_expert;
2. decompose h_i into c, r_s, q_b, u_p, m_tau, residual;
3. compute router logits z_{i,e};
4. compute top-2 margin contribution from each component;
5. identify route switch and stable lock steps per slot.
```

### Primary metrics

```text
component contribution to top-2 margin
fraction of route switches caused by each component
first component whose margin predicts final dominant expert
slot_margin / total_margin ratio over time
non_slot_margin / total_margin ratio over time
```

### Supports residual non-slot logit bias

```text
Before lock-in, common / B / position / template margin predicts the final dominant expert better than slot margin.
```

### Weakens residual non-slot logit bias

```text
Slot margin dominates from early checkpoints, but routing still collapses.
```

### New knowledge

```text
This identifies when distribution changes and which logit term caused it.
```

---

## 9. Protocol P4: Router Update and Forced-Utility Trajectory

### Question

Do sparse top-1 router updates align with slot identity or with early expert advantage?

### Dataset

```text
Use P1 training runs on D1.
```

### Run

At each selected checkpoint:

```text
1. record actual sparse top-1 router gradients from the implementation;
2. compute update effect on logits:
       delta_z_{i,e} = -eta * <grad(w_e), h_i>
3. decompose delta_z into common / slot / B / position / template contributions;
4. force each routed token through each expert for evaluation only;
5. compute forced-route utility U_{i,e} = -CE(y_i | force expert e);
6. compare chosen expert with best-utility expert.
```

Important restriction:

```text
Forced routing is diagnostic only.
It is not soft routing and does not train with expert mixtures.
```

### Primary metrics

```text
update_slot_alignment
update_non_slot_alignment
update_effect_on_top1_margin
best_utility_expert_by_slot
route_utility_match
utility_gap = U_best - U_second_best
shared_best_expert_rate across slots
```

### Supports top-1 training lock-in

```text
Early updates push multiple slots toward the same expert, and that expert later becomes the dominant routed expert.
Forced utility shows expert/router co-adaptation after assignment.
```

### Weakens top-1 training lock-in

```text
Updates are slot-aligned from early training, but final routing still collapses.
```

### New knowledge

```text
This tests whether the router is learning slot identity or route-utility binding under sparse top-1 training.
```

---

## 10. Protocol P5: Slot-Initialized Positive Control

### Question

Is slot-to-expert specialization reachable when early random lock-in is removed?

### Dataset

```text
Primary: D1 no_pos_random_position_main
```

### Variants

#### P5A: centroid-router initialization

```text
1. collect step-0 or early h_i centroids by slot;
2. initialize router rows to classify slot centroids into a fixed slot-to-expert mapping;
3. train with ordinary sparse top-1 routing.
```

Boundary:

```text
This is not random-init evidence. It is a positive control.
```

#### P5B: forced-slot warmup then release

```text
1. for K warmup steps, force slot s -> expert e_s;
2. train experts under this forced assignment;
3. release to ordinary sparse top-1 routing;
4. track whether specialization persists.
```

Boundary:

```text
This tests reachability and stability, not natural emergence.
```

### Primary metrics

```text
slot_to_expert_NMI
per_slot_route_purity
accuracy
route switch count after release
time_to_collapse_after_release
expert causal utility by slot
```

### Supports positive-control hypothesis

```text
Slot specialization is stable across seeds after slot-aware initialization or warmup.
```

### Weakens positive-control hypothesis

```text
Even slot-initialized / forced-warmup runs collapse into the same shared experts.
```

### New knowledge

```text
This tells us whether the target specialization is reachable under favorable conditions.
If reachable, baseline failure is more likely a training-dynamics problem.
If unreachable, the issue is deeper: representation, capacity, or objective geometry.
```

---

## 11. Protocol P6: Early vs Late Anti-Lockin Intervention

### Question

Is there an early time window where changing router geometry prevents collapse?

### Dataset

```text
Primary: D1 no_pos_random_position_main
```

### Variants

```text
baseline: ordinary sparse top-1
common_logit_cancel_early: subtract w_e^T c from router logits during early window only
common_logit_cancel_late: same intervention after lock-in window
load_balance_warmup_early: top-1 sparse routing with auxiliary load-balance loss during early window
slot_inhibition_after_P5: slot-aware inhibition only after positive control is shown to work
```

Not allowed:

```text
No soft routing schedule.
No multi-expert probability-weighted forward pass.
```

### Primary metrics

```text
slot_to_expert_NMI
per_slot_route_purity
max_load
target_accuracy
route_switch_count
time_to_lock
component margin at lock step
```

### Supports early lock-in

```text
Early intervention prevents or delays collapse; late intervention does not.
```

### Weakens early lock-in

```text
Early and late interventions have the same effect, or neither changes trajectory.
```

### New knowledge

```text
This converts the lock-in story into a causal timing claim.
```

---

## 12. Protocol P7: Slot Order / Update Overlap Diagnostic

### Question

Does the order in which slots appear create gradient overlap that changes final routing?

### When to run

```text
Run only if P3/P4 show that most route switches occur in a narrow early window.
```

### Dataset

```text
Same D1 examples, different presentation orders.
```

### Schedules

```text
iid_shuffle: fully shuffled balanced epoch
cyclic_balanced: each micro-cycle contains every slot equally often
blocked_by_slot: long contiguous blocks of one slot
anti_blocked: alternates slots to minimize same-slot streaks
```

### Primary metrics

```text
route_switch_step
stable_lock_step
gradient covariance between slots
final slot_NMI
final max_load
accuracy
```

### Supports order-overlap mechanism

```text
Changing only order changes route-switch timing and final specialization, with matched data counts.
```

### Weakens order-overlap mechanism

```text
Order changes do not affect trajectory across seeds.
```

### New knowledge

```text
This determines whether slot order belongs in the main mechanism or should be parked.
```

---

## 13. Minimal Run Order

Run in this order:

```text
Stage 1 validity:
  P0 dataset audit
  P1 clean baseline re-collapse
  P2 slot signal probe

Stage 2 mechanism:
  P3 logit trajectory decomposition
  P4 router update / forced-utility trajectory

Stage 3 causal / positive control:
  P5 slot-initialized positive control
  P6 early vs late anti-lockin

Stage 4 secondary diagnostic:
  P7 slot order / update overlap, only if needed
```

Stop conditions:

```text
If P0 fails: fix data before any model interpretation.
If P1 does not reproduce collapse: current anchor is not the right next experiment.
If P2 shows no slot signal: stop gating-dynamics story; study representation formation.
If P3/P4 identify non-slot or utility-driven lock-in: proceed to P5/P6.
If P5 fails: specialization may not be reachable under this model/objective.
```

---

## 14. Expected Decision Outcomes

### Outcome A: slot signal exists, but baseline collapses

Required evidence:

```text
P2 slot probe high;
P1 low slot_NMI / high max_load;
P3 non-slot margin predicts route lock;
P4 updates or utilities show shared expert advantage.
```

Claim:

```text
In this clean uniform setting, collapse is not caused by missing slot information alone.
Sparse top-1 routing fails because router decisions are dominated by non-slot logits or early expert-utility lock-in.
```

---

### Outcome B: slot signal absent

Required evidence:

```text
P2 slot probe fails, especially on held-out B / position splits.
```

Claim:

```text
The failure is primarily representation-side: the routed hidden state does not expose usable slot information.
```

Next decision:

```text
Change representation construction before studying router specialization.
```

---

### Outcome C: positive control succeeds, baseline fails

Required evidence:

```text
P5 high slot_NMI / purity and stable post-release routing;
P1 baseline low slot_NMI / purity.
```

Claim:

```text
Slot specialization is reachable, but ordinary sparse top-1 training does not reliably discover it from random initialization.
```

Next decision:

```text
Design feature-aware anti-lockin or common-controlled router initialization.
```

---

### Outcome D: positive control also fails

Required evidence:

```text
P5 collapses despite forced-slot or centroid initialization.
```

Claim:

```text
The failure is not merely early random lock-in. The target specialization may be unstable under the current objective, expert capacity, or representation.
```

Next decision:

```text
Audit expert capacity, target construction, and whether experts have causal slot utility.
```

---

### Outcome E: load balance improves but NMI does not

Required evidence:

```text
P6 max_load decreases;
slot_NMI / purity remains low.
```

Claim:

```text
Load balancing reduced collapse but did not create feature-level specialization.
```

Next decision:

```text
Do not treat load-balance warmup as a solution. Study feature-aware intervention.
```

---

## 15. Required Figures and Tables

### Figure 1: dataset audit table

```text
slot counts;
B counts;
slot-position counts;
slot-B mutual information;
target-B mutual information.
```

### Figure 2: seed-level route heatmaps

```text
rows = seeds;
columns = checkpoints or methods;
cell = P(expert | slot).
```

### Figure 3: route/load trajectory

```text
max_load over time;
slot_NMI over time;
accuracy over time.
```

### Figure 4: logit margin decomposition

```text
for each slot:
  total top-2 margin;
  common contribution;
  slot contribution;
  B contribution;
  position/template contribution.
```

### Figure 5: route-switch event table

Columns:

```text
seed;
slot;
first_switch_step;
stable_lock_step;
final_expert;
margin_source_at_switch;
best_forced_utility_expert;
interpretation.
```

### Figure 6: positive-control comparison

```text
baseline vs centroid-init vs forced-slot-warmup;
slot_NMI;
purity;
max_load;
accuracy;
time_to_collapse_after_release.
```

---

## 16. Reporting Rules

Every protocol result must be written as:

```text
Observation:
Interpretation:
Supported:
Weakened:
Insufficient evidence:
Cannot claim:
Next decision:
```

Forbidden claims unless directly supported:

```text
position embedding is the only cause;
common offset fully explains final collapse;
load balance equals slot specialization;
positive control proves natural emergence;
forced routing is the same as ordinary sparse top-1 learning;
results transfer to real language models.
```
