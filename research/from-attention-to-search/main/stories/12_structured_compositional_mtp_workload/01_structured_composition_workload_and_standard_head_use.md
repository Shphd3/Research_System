# Structured Composition Workload And Standard-Head Use

## Abstract

A12 asks whether the earlier future signal isolated by A11 becomes functional
on the kind of task raised in advisor discussions: many locally simple facts
are dispersed across a context, coupled through intermediate variables, and
must be combined in the correct order before a decision can be made. The core
model is a computation tree. The current synthetic task is only its smallest
serial instance, a depth-two path through two random one-to-one tables. This
construction validly removes single-evidence shortcuts, but the tested
from-scratch small Transformers remain near chance on unseen compositions. A
fixed-table control is exactly learnable, but its positive interaction appears
only at exact accuracy `1.0`. E03 then fails as an operationalization because
its task depths have asymmetric query-relevant structure. E04 replaces both
with a per-sample balanced dual-map carrier whose paired tasks share the query,
maps, serialization, and answer position; calibration and sealed confirmation
sets are base-instance disjoint. E04 Stage A completed all 12 approved NTP
trajectories, but neither scale learned both task depths across all three seeds,
no mastery threshold was frozen, and the row-removal necessity guard proved
invalid because bijection completion recovers the missing value. A separate
oracle-factor linear model shows that insufficient representation rank is a
sufficient cause of an NTP/MTP tradeoff and that curriculum cannot create a
missing dimension. The immediate decision is whether to close E04 or redesign
the carrier/capability test under a new Protocol; every MTP run and the
intermediate-state causal-use question remain blocked.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object or computation | Why it matters | Cannot prove |
|---|---|---|---|---|
| computation tree | evidence is combined in stages through intermediate states | \(Z_v=g_v(Z_{c_1},\ldots,Z_{c_k})\) and root \(Y\) | captures coupling, order, and staged aggregation | that the network internally uses the same tree |
| long-range task dependence | remote evidence remains necessary after the local question region is known | local-only and evidence-removal controls fail while full context succeeds | separates dependency from token distance | natural-language semantics in general |
| joint evidence necessity | no intended proper evidence subset determines the answer, but the full set does | partial-evidence accuracy near chance; full evidence determines \(Y\) | blocks single-evidence shortcuts | internal composition by itself |
| intermediate state | the result of one stage that must be used by the next stage | \(B=\pi_1(A)\) in the base task | makes composition testable | linear decodability in every model |
| task capability gate | the shared checkpoint can solve unseen full-context examples and passes shortcut controls | accuracy and intervention thresholds | makes objective comparison eligible | the learning mechanism |
| causal use | changing a task-specific component changes the standard-head answer according to the data-generating rule | cross-fitted hidden-state intervention | distinguishes stored information from function | real-benchmark transfer |

## 2. Mapping The Advisor's Difficult Task To The Model

| Advisor-side description | Model object | Operational test |
|---|---|---|
| many local factors | evidence leaves \(E_1,\ldots,E_m\) | vary the number of required leaves |
| each local step is easy | simple lookup or elementary operator \(g_v\) | oracle one-step accuracy is near perfect |
| factors are coupled | a parent node consumes child states | replacing one child changes the parent result |
| order matters | noncommutative composition | reverse the operator order and recompute the answer |
| causal relations matter | evidence intervention predicts an answer change | counterfactual evidence swap |
| gradual aggregation | intermediate nodes \(Z_v\) | probe or intervene at the corresponding stage |
| information is dispersed | evidence is rendered in separated context regions with distractors | vary positions without changing latent facts |
| final decision is difficult | root answer requires the complete path or tree | full-context versus partial-evidence gap |

The model is useful because each phrase becomes a controlled variable rather
than a metaphor.

## 3. Core Mathematical Model

For a rooted computation tree, evidence values occupy the leaves. Every
internal node applies a specified operator to its children:

\[
Z_v=g_v(Z_{c_1(v)},\ldots,Z_{c_k(v)}),
\qquad
Y=Z_{root}.
\]

The rendered sequence contains the evidence, operator specification, query,
and distractors. Changing wording, row order, or evidence position should not
change the latent tree result. Changing a required leaf or operator should
change the result according to the same computation graph.

This is the A12 target model. The current experiment instantiates only a
depth-two serial path, not a branching tree. The serial base case must be
understood before adding branch aggregation because failure on the base case
cannot be repaired by making the tree deeper.

## 4. Exact Current Synthetic Data

Let the entity set be

\[
\mathcal V=\{v_0,\ldots,v_7\}.
\]

For every example, sample two independent random permutations, meaning two
complete one-to-one mappings

\[
\pi_1,\pi_2:\mathcal V\rightarrow\mathcal V,
\]

and a start entity \(A\). Define

\[
B=\pi_1(A),
\qquad
Y=\pi_2(B).
\]

Example:

```text
TABLE_1: v0->v2  v1->v0  v2->v3  v3->v1  ...
TABLE_2: v0->v1  v1->v3  v2->v0  v3->v2  ...
QUERY: start=v1; apply TABLE_1, then TABLE_2
<DECIDE> <FMT_0> <ANS_v1>
```

The required computation is

```text
v1 --TABLE_1--> v0 --TABLE_2--> v1.
```

The full tables are necessary. If only the answer-path rows were shown, a
model could succeed through local entity matching in a context with no
competing rows. In a complete permutation table, every candidate answer
appears once. TABLE_1 is needed to determine which row of TABLE_2 should be
used, and TABLE_2 is needed to determine the output of that row.

Conditioned on the query, either independently sampled table alone leaves \(Y\)
uniform, while the two tables together determine it:

\[
I(Y;\pi_1\mid A)=0,
\qquad
I(Y;\pi_2\mid A)=0,
\]

\[
H(Y\mid A,\pi_1,\pi_2)=0.
\]

This establishes the data distribution's joint-necessity property. It does
not by itself show that a trained network forms the explicit state \(B\).

## 5. Why The Output Layout Identifies The Objective Difference

`<DECIDE>`, `<FMT_0>`, and each answer symbol are registered as atomic tokens.
At the decision state \(h_T\):

- the next token `<FMT_0>` is shared and locally determined;
- the second future token `<ANS_Y>` requires the two-table result.

NTP and informative Next-2 use the same standard next-token loss. Informative
Next-2 adds a direct answer loss at \(h_T\):

\[
L_{NTP}=L_N,
\]

\[
L_{MTP-info}=L_N+\lambda L_A.
\]

Final evaluation always uses the same standard head after `<FMT_0>`. Auxiliary
head accuracy is explanatory evidence, not the final outcome.

## 6. Relation To Real Workloads

The synthetic task represents the computational skeleton of cases such as:

- multi-document question answering: organization \(\rightarrow\) founder
  \(\rightarrow\) birthplace;
- repository reasoning: configuration key \(\rightarrow\) invoked module
  \(\rightarrow\) effective parameter;
- rule-based audit: subject attribute \(\rightarrow\) applicable rule
  \(\rightarrow\) decision.

The synthetic data removes natural-language parsing, retrieval ambiguity,
entity resolution, and answer generation. Success would therefore establish
only the ordered-composition mechanism. Transfer requires a later paired test
on a real workload with the same evidence-removal and causal controls.

## 7. Current Evidence

### 7.1 Workload validity is supported

Analytically and empirically, one table is insufficient and the two tables
jointly determine the answer. Row order, distractors, and evidence swaps can be
controlled independently. The data model therefore answers the workload
definition question.

### 7.2 The tested neural learner did not pass the capability gate

Across the bounded depth, width, training-length, and explicit row-binding
repairs, answer accuracy remained near the \(1/8=0.125\) chance level while
format accuracy reached 1.0. This localizes the failure: the model learned the
output interface but not held-out two-step composition.

This is not evidence that MTP fails. It means the checkpoint is ineligible for
an NTP/MTP mechanism comparison. Comparing objectives before task capability
would mix objective effects with a more basic task-learning failure.

### 7.3 The in-support short-range carrier passes capability

The fixed-length rule-token control first failed when evaluation held out
ordered rule pairs. After changing only the support contract so that all 64
ordered pairs appear in training and complete-support evaluation, all 24
conditions reached exact standard-head accuracy `1.0`. The 2- and 4-layer
formal scales remained exact throughout steps 19,000--20,000 under both tasks,
both objectives, and both calibration seeds.

This establishes a learnable finite comparison surface and localizes the
earlier failure mainly to unseen-pair composition. It does not establish a
compositional algorithm: even the one-layer diagnostic fits exactly. The speed
interaction is also threshold-sensitive. It is near zero, negative, or
seed-inconsistent through threshold `0.99`, and positive for both formal
scales and both seeds only at exact `1.0`. The eligible candidate is therefore
the last stage of eliminating every supported error, not broad convergence.

### 7.4 E03 fails, and E04 defines the current carrier

E03 attempted per-sample regeneration, but the one-step direct-edge task and
the two-step unique-chain task had asymmetric query-relevant structure. A
query-free topology predictor and node-repetition statistics could therefore
distinguish the task depths for reasons unrelated to ordered composition.

E04 replaces that carrier with two per-sample five-row bijections. Paired task
depths share the query, both maps, token sequence, and answer position; only
the depth marker and correct answer differ. NTP-only Stage A used a calibration
set disjoint from a sealed future confirmation set and completed all 12
approved trajectories. No scale qualified: 2-layer two-step runs ended near
`0.250`, 4-layer two-step runs near `0.329`, and one 4-layer one-step seed
remained at `0.838`. The proposed row-removal necessity guard also failed
logically because the fifth value of a bijection is recoverable from the other
four rows. E04 therefore provides descriptive capability-floor evidence, not
an eligible MTP comparison or a valid evidence-necessity carrier.

### 7.5 Missing rank is a sufficient tradeoff mechanism in a linear model

An oracle-factor model supplies the local factor and future factor directly,
then limits the shared representation rank. At rank one, MTP improves the
future factor but raises the standard loss by 0.9084--1.0218 across the five
reported seeds. At rank two, the standard-loss gap falls to numerical zero.

This supports a bounded causal statement: when two independent task directions
must share one representational dimension, learning the auxiliary future
factor can displace the standard factor. It does not show that parameter count
or neural model scale follows the same law.

### 7.6 Curriculum cannot create missing rank

A dose-matched curriculum changes when the auxiliary objective is introduced
without changing total auxiliary weight. It passes the rank-one Pareto repair
criterion in 0/5 seeds, while rank two solves both objectives. Therefore
curriculum does not repair structural missing dimension in this model. It may
still help a capacity-sufficient nonlinear model with path-dependent
optimization conflict.

## 8. The Active Causal-Use Question

The phrase representation use must be split into three claims:

1. **presence:** a held-out decoder can recover a task variable;
2. **causal control:** changing only that component changes the standard-head
   answer as predicted;
3. **task benefit:** removing that component harms clean standard-head
   performance more than a matched random removal.

The base task contains two different variables:

\[
B=\pi_1(A)
\quad\text{and}\quad
Y=\pi_2(B).
\]

Patching an early \(Y\) direction tests whether the model stores an answer code
early. It does not prove that the model uses the intermediate composition
state \(B\). The stronger A12 claim therefore uses \(B\) as the primary
intervention target and \(Y\) as a secondary diagnostic.

For a recipient and donor sharing TABLE_2 but having different TABLE_1 outputs,
the predicted counterfactual is

\[
Y'=\pi_2(B_{donor}).
\]

After fitting an intermediate-state subspace on separate data, patch only that
component at \(h_T\), pass through the same format-token transition, and score
whether the common standard head moves to \(Y'\). Subtract an equal-rank random
patch effect and compare informative Next-2 with NTP from the same capable
checkpoint.

## 9. Current Decision And Stop Rule

The immediate decision is not a broader architecture sweep, a full tree, or an
MTP comparison. E04 NTP Stage A is complete and failed both the shared
capability gate and the row-removal validity guard. Decide whether to close E04
under its frozen 2/4-layer, 20,000-step contract or reopen carrier/capability
design under a new Protocol. No threshold can be frozen. The sealed
confirmation comparison, Stage B, and every MTP trajectory remain blocked.

The `12_03` causal-use protocol remains downstream. Its capability and
intervention guards are not replaced by `12_0`: exact behavior and readable
probes still cannot show that the common standard head causally relies on \(B\).

Only after the depth-two causal-use question passes should A12 expand to a true
branching tree, for example two independently computed child states combined
by a root operator. That later expansion is a new anchor, not part of the
current experiment.

## 10. Claim Boundary

A12 currently establishes a valid depth-two joint-evidence workload, a failed
unseen-composition small-model branch, a memorization-prone exactly learnable
fixed-table surface, an E03 rejection for asymmetric query-relevant structure,
a sufficient linear missing-rank mechanism, and an E04 NTP capability failure
with an invalid row-removal guard. E04 does not provide an eligible comparison
surface. A12 does not establish neural causal use, general MTP superiority,
unseen-pair generalization, a scale law, general tree reasoning,
natural-language transfer, or Router/MoE value.

## 11. Anchor Chain And Source Map

1. [Short-range one-step versus two-step composition](../../problem_anchors/12_structured_compositional_mtp_workload/12_00_short_range_single_vs_two_step_composition/12_00_short_range_single_vs_two_step_composition_anchor.md) — [fixed-table audit](../../experiments/A12/12_00_short_range_single_vs_two_step_composition/A12_0_E02_in_support_capability_calibration/summary.md), [E04 Stage A summary](../../experiments/A12/12_00_short_range_single_vs_two_step_composition/A12_0_E04_balanced_per_sample_dual_map/summary.md), and [detailed record](../../experiments/A12/12_00_short_range_single_vs_two_step_composition/A12_0_E04_balanced_per_sample_dual_map/detailed.md).
2. [Compositional workload and capability gate](../../problem_anchors/12_structured_compositional_mtp_workload/12_01_compositional_workload_capability_gate/12_01_compositional_workload_capability_gate_anchor.md) — [capacity ladder](../../experiments/A12/12_01_compositional_workload_capability_gate/A12_01_01_E01_composition_calibration/summary.md) and [explicit-binding guard](../../experiments/A12/12_01_compositional_workload_capability_gate/A12_01_01_E02_explicit_binding_calibration/summary.md).
3. [Interference, capacity, and curriculum boundary](../../problem_anchors/12_structured_compositional_mtp_workload/12_02_interference_capacity_curriculum_boundary/12_02_interference_capacity_curriculum_boundary_anchor.md) — [rank intervention](../../experiments/A12/12_02_interference_capacity_curriculum_boundary/A12_02_01_E01_task_rank_competition/summary.md) and [dose-matched curriculum](../../experiments/A12/12_02_interference_capacity_curriculum_boundary/A12_02_01_E02_curriculum_rank_boundary/summary.md).
4. [Standard-head causal use](../../problem_anchors/12_structured_compositional_mtp_workload/12_03_standard_head_causal_use/12_03_standard_head_causal_use_anchor.md) — downstream [capability-gated protocol](../../experiments/A12/12_03_standard_head_causal_use/A12_03_E01_standard_head_causal_use/protocol.md).

The ineligible one-step neural audit is retained only in the [A12 experiment archive](../../experiments/A12/archive/README.md). Repository-code transfer, deeper trees, neural scale effects, and capacity-sufficient curriculum remain parked rather than separate active anchors.
