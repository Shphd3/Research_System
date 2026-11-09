# 05_03 Experiment Protocols: Uniform Collapse / Common Offset / Anti-Lockin

## Protocol Role Map

Conclusion:

```text
The three main experiments for the current research question are P1, P2, and P3.
P0 is the precondition audit.
P4 and P5 are support / extension protocols.
P6 and P7 are later-stage protocols: run them only after P1/P2/P3 finish and
their results have been audited.
```

Current execution order:

| Order | Protocol | Role | Run Now? | Decision It Answers |
|---:|---|---|---|---|
| 0 | P0 Audit Closure / Baseline Freezing | precondition audit | yes, first | Can we treat data/init/code as audited enough to run mechanism tests? |
| 1 | P1 Common Source Perturbation | main experiment 1 | yes | Does changing the suspected source weaken \(c\) and early collapse? |
| 2 | P2 Multi-Seed Common-Score Audit | main experiment 2 | yes | Does \(w_e^\top c\) predict the dominant expert across seeds? |
| 3 | P3 Common-Offset Cancellation Before Routing | main experiment 3 | yes | Does removing the common offset reduce collapse while preserving target learning? |
| support | P4 Common-Aware Router Initialization | support / extension | after P1/P2/P3 audit if needed | Can initialization equalize common scores and reduce collapse? |
| support | P5 Stable Common Subtraction Methods | support / extension | after P1/P2/P3 audit if needed | Which subtraction estimator is stable enough after P3 clarifies mechanism? |
| later | P6 Anti-Lockin Warmup / Load-Balance Variants | later-stage protocol | after P1/P2/P3 audit | Test anti-lockin only if common-offset control is insufficient or incomplete. |
| later | P7 Forced-Routing Utility Diagnostic | later-stage protocol | after P1/P2/P3 audit | Test utility dominance only if main experiments leave this rival explanation open. |

Instruction to execution AI:

```text
First execute P0, then run the three main experiments P1, P2, and P3 in order.
After P1/P2/P3 finish, audit whether the actual runs matched the protocols,
whether the primary metrics exist, and whether the result supports, weakens, or redirects the hypothesis.
Only after that audit should AI consider P4/P5 as support or extension.
Only after that audit should AI consider P6/P7.
Do not turn P4/P5/P6/P7 into broad sweeps.
```

## Global Rules

Use the original uniform feature setting unless the protocol explicitly tests data/common-source perturbation.

Keep fixed:

```text
data rule
target rule
seeds
optimizer / training length
expert input = full hidden state
```

Change one variable per protocol.

Primary metrics across all protocols:

```text
1. step0 / step10 / step20 / step50 max_load
2. load_entropy
3. dominant_expert_persistence
4. top1_margin
5. final collapse rate across seeds
6. target accuracy / loss
7. common_score = w_e^T c for each expert
8. agreement(argmax_e common_score, dominant expert)
```

Collapse is not considered fixed unless routing improves **and** target accuracy is preserved.

Slot-code patterns:

```text
S0 repeated slot code: [A,A,A,A,A]-style repeated cue token.
S1 distributed / complex slot code: [p,q,r,t,u]-style non-repeated pattern,
    analogous to the abcdef-like construction used in earlier slot-context experiments.
```

The complex slot-code condition is a controlled construction factor. It tests
whether the common-offset mechanism depends on repeated slot tokens; it does not
by itself prove feature-level specialization.

---

## P0: Audit Closure / Baseline Freezing

Role:

```text
Precondition audit. This is not one of the three main experiments.
```

### Decision question

Can we treat code/data/init as sufficiently audited and move to causal intervention?

### Inputs

```text
audit_report outputs
original uniform runs
same seeds used in previous meeting brief
```

### Checks

Confirm these artifacts exist and are reproducible enough for the next iteration:

```text
data_uniformity_counts.csv
batch_order_entropy.csv
initialization_parameter_stats.csv
step0_hidden_common_geometry.csv
common_direction_source_alignment.csv
router_score_decomposition.csv
random_geometry_baseline.csv
early_gradient_self_reinforcement.csv
```

### Success

```text
1. Slot-level train/eval uniformity passes.
2. Training order / batch entropy passes.
3. R* router init is random, bias-free, and seed-controlled.
4. Step-0 hidden common component is observed.
5. Residual routing diagnostic reduces step-0 concentration.
```

### Failure / redirect

```text
Any code/data/init check fails -> stop mechanism claims and repair code first.
```

### Claim after success

```text
We can move from bug audit to mechanism intervention, with the boundary that exact byte-identical rerun and utility-best expert remain unchecked.
```

---

## P1: Common Source Perturbation

Role:

```text
Main experiment 1. It tests whether the measured common direction has the proposed
construction source.
```

### Decision question

Does the measured common direction come from a specific construction source such as fixed routed position / template component?

### Hypothesis

```text
The common direction is not caused by feature frequency. It is mainly induced by fixed routed-position / template structure in the hidden representation.
```

### Conditions

Run step-0 diagnostics first. Only train the most informative variant.

```text
C0: original data construction.
C1: randomize routed/B position while preserving target rule and balanced feature grid.
C2: keep position fixed but remove or zero the routed-position embedding for router input only, if implementation permits.
C3: keep B position fixed but vary template/special tokens while preserving feature and target rule.
C4: route on hidden after subtracting known position/template source vector, without changing expert input.
C5: replace repeated slot code with distributed / complex slot code while keeping feature frequency, target rule, B position, and router unchanged.
```

Do not combine multiple changes in the same condition.

### Metrics

```text
common_ratio
cos(c, position_embedding)
cos(c, raw_input_at_B_position)
cos(c, mean_B_embedding)
cos(c, mean_slot_embedding)
full_hidden_max_load
residual_max_load
argmax_e w_e^T c
```

### Supported if

```text
Weakening or removing the suspected source reduces common_ratio and step-0 max_load, and changes common-source alignment accordingly.
The distributed / complex slot-code control shows whether the same effect persists without repeated slot tokens.
```

### Weakened if

```text
Common direction and step-0 concentration remain unchanged after removing the suspected source.
```

### Insufficient evidence if

```text
The variant changes task difficulty or target accuracy so much that routing cannot be compared.
```

---

## P2: Multi-Seed Common-Score Audit

Role:

```text
Main experiment 2. This tests whether the proposed common offset predicts the
dominant expert across seeds without changing data, training, or router behavior.
```

### Decision question

Does `w_e^T c` predict which expert becomes dominant?

### Hypothesis

```text
Random bias-free router rows produce unequal common scores. The expert with the largest common score receives the most load at step 0 and often becomes the final collapse expert.
```

### Procedure

For each seed and condition:

```text
1. Compute feature centroids h_f at step 0.
2. Compute c = mean_f h_f.
3. Compute common_score[e] = w_e^T c.
4. Record step0 dominant expert.
5. Train or load checkpoints.
6. Record final dominant expert and collapse status.
```

Run the audit separately for:

```text
S0 repeated slot code
S1 distributed / complex slot code
```

### Primary figures

```text
1. common_score bar plot per seed.
2. heatmap: seed x expert for common_score and load.
3. scatter: common_score margin vs step0 max_load.
4. table: argmax common_score == step0 dominant / final dominant.
```

### Supported if

```text
argmax_e w_e^T c predicts step0 dominant expert substantially above random chance, and common_score margin correlates with early max_load / top1_margin.
```

For 4 experts, random chance is approximately 25%; use exact permutation / binomial test across seeds.

### Weakened if

```text
common_score has weak or no relation to early/final dominant expert.
```

### Redirected if

```text
common_score predicts step0 but not final, suggesting recovery / training dynamics are the main unresolved mechanism.
```

---

## P3: Common-Offset Cancellation Before Routing

Role:

```text
Main experiment 3. This is the first causal intervention because it removes the
hypothesized common offset at the logit level while keeping expert input unchanged.
```

### Decision question

If we remove only the router's common offset, does collapse reduce while target learning remains intact?

### Main intervention

Estimate `c` on a balanced calibration grid. Use one of the following router-only transformations:

```text
A. logit correction:
   z'_e = w_e^T h - w_e^T c

B. residual routing:
   h_route = h - proj_c(h)
   z'_e = w_e^T h_route

C. low-rank residual routing:
   h_route = h - U_k U_k^T h
   z'_e = w_e^T h_route
```

Experts still receive full hidden state `h`.

Run the first implementation for both:

```text
S0 repeated slot code
S1 distributed / complex slot code
```

### Recommended first implementation

Use **A. logit correction** first.

Reason:

```text
It directly removes the measured expert-specific common offset w_e^T c without changing the hidden vector consumed by experts.
```

### Estimator variants

```text
E0: c estimated once from step-0 balanced calibration grid, frozen.
E1: c estimated from current checkpoint on the same fixed calibration grid, updated only at logging/checkpoint boundaries.
E2: EMA c_t with stop-gradient and high momentum; no per-batch exact centering.
```

Avoid using raw per-batch mean as the first decisive intervention.

### Metrics

```text
step0-50 max_load
load_entropy
dominant_expert_persistence
collapse_rate across seeds
target accuracy / loss
same-feature consistency only after excluding collapse
feature-to-expert heatmap
common_score after correction
```

### Supported if

```text
1. early max_load decreases;
2. final collapse rate decreases;
3. target accuracy remains near baseline;
4. non-collapsed seeds keep or improve feature-level routing structure.
```

### Weakened if

```text
common correction does not change early/final load.
```

### Redirected if

```text
routing balances but target accuracy drops, meaning the removed component carries task signal or the estimator is too aggressive.
```

---

## P4: Common-Aware Router Initialization

Role:

```text
Support / extension protocol. Run after P1/P2/P3 result audit if initialization
is the next unresolved mechanism.
```

### Decision question

Can we make random initialization more stable by equalizing router rows on the measured common direction?

### Hypothesis

```text
Default random init is not a bug, but it creates unequal w_e^T c. Equalizing this quantity should reduce early load concentration.
```

### Conditions

```text
I0: default PyTorch random Linear(..., bias=False).
I1: reduced-scale router init.
I2: common-orthogonal row init: w_e <- w_e - proj_c(w_e), then rescale row norm.
I3: common-score matched init: adjust rows so w_e^T c is identical across experts.
I4: residual-subspace orthogonal rows: orthogonalize router rows within c^perp.
```

Keep experts and all non-router weights identical where possible.

### Important caveat

Reduced scale alone may reduce softmax confidence but does not necessarily change hard top-1 argmax ordering at step 0. The more direct anti-collapse initialization is common-score matching or common-orthogonalization.

### Metrics

```text
step0 max_load
common_score variance across experts
top1_margin
final collapse rate
target accuracy
router row norm and pairwise cosine
```

### Supported if

```text
Common-aware init reduces common_score variance, early max_load, and final collapse without hurting target accuracy.
```

### Weakened if

```text
Common-aware init equalizes common_score but collapse remains unchanged.
```

---

## P5: Stable Common Subtraction Methods

Role:

```text
Support / extension protocol. Use it to refine the estimator after P3, not as the
first decisive experiment.
```

This protocol answers the engineering question: how to subtract common components more stably than per-batch mean or broad SVD removal?

### Candidate A: Frozen calibration mean

```text
c = mean hidden state on a fixed balanced calibration grid.
h_route = h - beta * c
```

Use `beta in {0.25, 0.5, 1.0}` only if needed. First run beta=1 for mechanism test.

Pros:

```text
stable, deterministic, easy to interpret.
```

Cons:

```text
may not track learned common drift.
```

### Candidate B: Logit-level common offset cancellation

```text
a_e = w_e^T c
z'_e = z_e - a_e
```

Pros:

```text
most targeted; does not alter expert input; avoids unstable hidden transformations.
```

Cons:

```text
depends on quality of c estimator.
```

### Candidate C: Router-row common orthogonalization

After optimizer step:

```text
w_e <- w_e - proj_c(w_e)
rescale ||w_e|| to original row norm
```

or use regularizer:

```text
L_common = Var_e(w_e^T c)
```

Pros:

```text
prevents re-acquiring common offset.
```

Cons:

```text
can remove useful signal if c overlaps with task-relevant information.
```

### Candidate D: EMA mean with stop-gradient

```text
mu_t = momentum * mu_{t-1} + (1 - momentum) * batch_mean_stopgrad
h_route = h - beta * debiased(mu_t)
```

Use high momentum, e.g. 0.99 or 0.999. Do not use exact current-batch centering as decisive evidence.

Pros:

```text
tracks drift.
```

Cons:

```text
can inject training-time noise and batch-size dependence.
```

### Candidate E: Regularized low-rank nuisance subspace

Estimate `U_k` on a fixed balanced calibration grid.

```text
h_route = h - beta * U_k U_k^T h
```

Choose `k` by:

```text
explained variance
source alignment with position/template
stability across calibration subsets
```

Do not choose k only because route heatmaps look cleaner.

### Recommended order

```text
1. Logit-level common offset cancellation.
2. Frozen calibration mean residual routing.
3. Common-aware initialization.
4. EMA / low-rank only after 1-3 clarify mechanism.
```

---

## P6: Anti-Lockin Warmup / Load-Balance Variants

Role:

```text
Later-stage protocol. Run only after P1/P2/P3 finish and the result audit shows
that common-offset control is insufficient or incomplete.
```

Run this only after common-offset intervention has been evaluated.

### Decision question

If common control is insufficient, can early anti-lockin pressure prevent top-1 amplification?

### Conditions

```text
A0: baseline hard top-1.
A1: first K steps use load-balancing auxiliary loss, then anneal down.
A2: first K steps use soft routing / top-k, then hard top-1.
A3: first K steps add router noise / temperature, anneal to baseline.
A4: delayed inhibition / selected-expert reinforcement.
A5: auxiliary-loss-free dynamic expert bias for load balancing.
```

### Metrics

```text
max_load trajectory
load_entropy
margin growth rate
final collapse rate
target accuracy
whether feature-level structure survives after anti-lockin removal
```

### Supported if

```text
Early anti-lockin reduces dominant persistence and final collapse, while feature-level routing remains non-arbitrary after warmup.
```

### Weakened if

```text
It only forces uniform load during warmup but collapse returns after hard top-1.
```

---

## P7: Forced-Routing Utility Diagnostic

Role:

```text
Later-stage protocol. Run only after P1/P2/P3 finish and the result audit shows
that utility dominance remains an open rival explanation.
```

Run as diagnostic, not as the main intervention.

### Decision question

Is the dominant expert actually utility-best for most features?

### Procedure

For each feature centroid / token group:

```text
force route to each expert e
measure loss / accuracy / correct-token probability
build utility matrix U[f,e]
compare router-chosen expert to argmax_e U[f,e]
```

### Metrics

```text
route_utility_match_rate
best_expert_load_distribution
utility_gap
collapse expert utility advantage
```

### Interpretation

```text
If one expert is utility-best for most features, collapse may reflect expert utility dominance.
If utilities are diverse but router collapses, routing shortcut / lock-in is more plausible.
```

---

## Minimal Execution Order

Use this order for the next iteration:

```text
0. P0: freeze audit conclusion.
1. P1: common-source perturbation.
2. P2: multi-seed common-score audit.
3. P3A: logit-level common-offset cancellation.
4. Audit P1/P2/P3 actual runs against the protocols and primary metrics.
5. P4/P5: support or extension after the audit if needed.
6. P6/P7: run only after the audit if the previous experiments leave anti-lockin or utility dominance unresolved.
```
