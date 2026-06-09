# Audit Prompt: Uniform Feature-to-Expert Specialization Collapse

## Goal

Audit the current code, data generation, logging, and result interpretation for the uniform synthetic MoE experiments.

The scientific question is:

```text
In a uniform feature distribution, after removing or randomizing fixed position signals, why does a top-1 MoE router still fail to form stable feature-to-expert specialization and instead collapse during training?
```

The audit should not propose a new architecture first. Its job is to determine whether the observed collapse is caused by implementation/data/metric artifacts, by remaining common/nuisance signals, or by training dynamics such as top-1 lock-in and route/expert co-adaptation.

## Current Known State To Respect

- Previous audit found no first-order data/init/router bug in the original uniform setting.
- Original baseline had a hidden common component `c` at routed positions.
- For a bias-free linear router, `z_{f,e} = w_e^T h_f = w_e^T c + w_e^T r_f`; therefore `w_e^T c` acts as an expert-specific effective common bias.
- `w_e^T c` strongly predicted step-0 dominant expert in the original setting.
- Logit-level common-offset cancellation reduced step-0 imbalance and hard collapse, but did not fully solve final collapse.
- In the most recent no-position meeting observation, removing position embedding reportedly made step-0 less/no collapsed, but training still collapsed later, less severely, often toward two experts.

Do not treat “position embedding causes collapse” as proven. The safer claim is:

```text
Position/common-offset may explain the original step-0 seed, but final collapse still requires a training-dynamics or utility-alignment explanation.
```

## Files / Code Areas To Inspect

Please inspect the relevant repo files for:

1. data generation;
2. sequence construction and slot/feature placement;
3. model definition;
4. positional encoding removal or randomization;
5. router implementation and initialization;
6. top-1 routing / capacity / tie-breaking;
7. auxiliary losses or regularizers;
8. training loop;
9. logging and checkpoint evaluation;
10. metric scripts and plotting scripts.

Report exact file paths, function names, and line ranges where possible.

## A. Experiment Reconstruction

Reconstruct the exact experiment matrix from config files, scripts, logs, and output directories.

For each run, record:

```text
run_name
seed
model_size
num_experts
top_k
router type
router bias yes/no
router initialization distribution
position encoding setting
feature position setting
feature distribution
slot distribution
B/context distribution
target distribution
batch size
optimizer
learning rate schedule
number of steps
auxiliary losses
load-balance regularization
capacity factor / token dropping behavior
checkpoint/eval cadence
```

Flag any mismatch between the intended experiment and the actual config.

## B. Data And Feature Definition Audit

### B1. Distribution checks

Verify with direct counts, not assumptions:

```text
count(feature_key)
count(slot)
count(B/context)
count(target_label)
count(slot, B)
count(feature_key, target_label)
count(feature_key, position)
count(B/context, position)
```

Expected for the uniform setting:

- feature counts should be uniform within statistical tolerance;
- slot counts should be uniform if slots are supposed to be balanced;
- B/context counts should be uniform if B is part of the design;
- target labels should not accidentally create a dominant class unless this is intended;
- if feature position is randomized, `position` should be independent of `feature_key`.

### B2. Feature key clarity

Do not let the code silently define “feature” as only a target label if the experiment intended a more precise factor.

Audit whether the intended feature is one of:

```text
slot_id
B/context id
target id
(slot_id, B/context id)
(slot_id, target id)
logical rule id
```

For each reported metric such as NMI or purity, state exactly which `feature_key` was used.

### B3. Train/eval consistency

Check whether train and eval use the same feature support and the same uniformity constraints. Confirm that evaluation is not accidentally easier, smaller, sorted, or non-randomized.

## C. Position-Removal / Position-Randomization Audit

The recent meeting observation depends critically on whether position was really removed.

Verify all possible position sources:

```text
learned absolute positional embedding
sinusoidal positional embedding
RoPE / ALiBi / relative position bias
position ids passed into the model
segment / token-type embeddings
fixed template tokens around the routed slot
causal mask pattern that exposes absolute location
routing index tied to an absolute position
special tokens at fixed positions
sequence length artifacts
```

Required checks:

1. Confirm that position parameters are absent, zeroed, or unused in forward pass.
2. Confirm that no position parameters receive gradients when the no-position setting is active.
3. If the routed logical slot is moved, confirm the router reads the logical slot token, not a fixed absolute index.
4. If feature position is randomized, verify `count(position | feature_key)` is approximately uniform.
5. Run a shift/permutation invariance sanity check if compatible with the task.

Report whether “no position” means:

```text
no learned position embedding only
no explicit position signal but fixed template remains
logical slot randomized over positions
fully position-invariant input construction
```

## D. Router / Initialization Audit

Check:

```text
router weight shape
router bias flag
router initialization distribution and scale
whether weights are reinitialized between seeds
whether expert and router seeds are accidentally tied
whether router rows are independent
whether there is any hidden bias term after layernorm or projection
tie-breaking behavior in top-1 argmax
whether capacity constraints/drop tokens induce apparent collapse
whether S* / centroid-overwrite routers are mistakenly counted as random init evidence
```

For each seed, compute at step 0:

```text
router row norms
pairwise cosine between router rows
logit mean/std by expert
fraction of exact or near ties
step0 max_load, entropy, Gini
matched random-assignment baseline
matched balanced/oracle baseline if available
```

## E. Hidden Geometry Audit

For each relevant checkpoint, especially step 0 and early checkpoints:

Define feature centroids:

```text
h_f = E[h(x) | feature_key = f]
c = E_f[h_f]
r_f = h_f - c
```

Compute:

```text
common_ratio = ||c||^2 / mean_f ||h_f||^2
feature_residual_ratio = mean_f ||r_f||^2 / mean_f ||h_f||^2
within_feature_variance
between_feature_variance
linear-probe accuracy for feature_key from h
linear-probe accuracy for target_label from h
linear-probe accuracy for position from h
cos(c, position_embedding_at_routed_position) if applicable
```

For the router logits:

```text
z_{f,e} = w_e^T h_f
common_logit a_e = w_e^T c
feature_logit q_{f,e} = w_e^T r_f
rank of dominant expert by a_e
agreement between argmax_e a_e and step0 dominant expert
step0 max_load before cancellation
step0 max_load after z'_{f,e} = z_{f,e} - a_e
```

Interpretation boundary:

- If common cancellation fixes step-0 routing, this supports common-offset as an early mechanism.
- It does not by itself explain final collapse.
- If no-position step-0 is balanced but final collapses, the audit must pivot to training dynamics.

## F. Training-Dynamics Audit

Track these quantities at dense early checkpoints and then throughout training:

```text
max_load trajectory
load entropy trajectory
route-feature NMI trajectory
route purity trajectory
per-feature route entropy trajectory
accuracy / loss trajectory
per-expert token counts
per-expert gradient norm
router gradient norm
expert parameter norm
route flip rate per checkpoint
winner persistence: whether early top expert predicts final top expert
```

Decompose router logits over time:

```text
z_{f,e}(t) = w_e(t)^T c(t) + w_e(t)^T r_f(t)
```

Log:

```text
common_logit range across experts
feature_logit range across features and experts
margin between chosen and second expert
gradient component along c
gradient component along r_f
traffic-weighted feature distribution per expert
```

Key question:

```text
When step-0 is balanced, what changes first: router logits, expert utility, load, or feature separability?
```

## G. Expert Utility / Co-adaptation Audit

At selected checkpoints, estimate a feature-by-expert utility matrix.

For each feature `f` and expert `e`, measure:

```text
loss if examples with feature f are routed to expert e
accuracy if feature f is routed to expert e
utility U[e,f] relative to average or oracle expert
```

Then compute:

```text
route-utility match
utility diagonal dominance under the claimed feature-to-expert map
best expert per feature
best feature per expert
utility entropy per feature
```

Interpretation:

- If final route-utility match is high, do not say “router picked the wrong expert.”
- Safer claim: route and expert utility co-adapted under top-1 training.
- If utility is not feature-diagonal, high route consistency does not imply feature-level specialization.

## H. Forced Feature-to-Expert Initialization Audit

For experiments initialized with a feature/expert one-to-one map:

Verify:

```text
exact initial assignment map feature -> expert
initial route heatmap
initial route-feature NMI / purity
initial per-feature route entropy
initial load balance
initial logit margin supporting the assigned expert
whether the gate is trainable or frozen
whether expert parameters are identical, random, or feature-pretrained
whether learning rates differ for router and experts
```

Track:

```text
time-to-first route flip
time-to-NMI-drop
feature assignment survival rate
logit margin trajectory for assigned expert
router gradient along assigned feature direction
expert utility matrix trajectory
accuracy/loss relative to oracle/frozen routers
```

Required controls:

1. `oracle_feature_router_frozen`: feature-to-expert routing fixed throughout training.
2. `feature_init_trainable_router`: same initialization but router trainable.
3. `random_balanced_init_trainable_router`: balanced but not feature-aligned.
4. `vanilla_random_router`.
5. Optional: `feature_init_with_inhibition_or_anti_lockin`.

Interpretation:

- If frozen oracle helps but trainable feature init collapses, the issue is optimization/gating stability.
- If frozen oracle does not help, the proposed feature partition may not be causally useful.
- If feature init survives only with inhibition, inhibition is a stabilizer, not yet evidence that vanilla MoE would naturally discover feature specialization.

## I. Alternative Explanations To Explicitly Test Or Rule Out

Check and report evidence for or against:

```text
data imbalance
target-label imbalance
target difficulty imbalance
position/template leakage
layernorm/residual common shift
finite random init geometry
top-1 rich-get-richer amplification
expert parameter co-adaptation
lack of capacity/interference pressure
router learning rate too high/low
expert learning rate too high/low
auxiliary load-balancing side effects
capacity factor or token dropping artifacts
argmax tie-breaking
batch-order stochasticity
metric definition mismatch
```

## J. Required Output Format

Please produce an audit report with the following sections:

```markdown
# Audit Report: Uniform Feature-to-Expert Collapse

## 1. Executive Verdict
- PASS / FAIL / UNCLEAR for each audit area.
- One-sentence safest conclusion.

## 2. Experiment Matrix Reconstructed
Table of actual runs and configs.

## 3. Code / Data / Init Findings
For every finding, include file path, function, and evidence.

## 4. Metric Validity
Which metrics answer the decision question, which are secondary, and which are misleading.

## 5. Step-0 Geometry Verdict
Does common-offset explain step-0? Under which position setting?

## 6. Training-Dynamics Verdict
Does collapse reappear after balanced step-0? What dynamics precede it?

## 7. Forced Feature-Init Verdict
Does a feature-to-expert prior survive? If not, when and why does it break?

## 8. Remaining Rival Explanations
Ranked by plausibility and missing evidence.

## 9. Claim Boundary
Can claim / cannot claim.

## 10. Minimal Next Experiments
No more than three decisive next experiments.
```

Also save or report paths for:

```text
csv tables for all metrics
route heatmaps by seed/checkpoint
max_load / entropy / NMI / accuracy trajectories
logit decomposition trajectories
gradient decomposition trajectories
utility matrix heatmaps
```
