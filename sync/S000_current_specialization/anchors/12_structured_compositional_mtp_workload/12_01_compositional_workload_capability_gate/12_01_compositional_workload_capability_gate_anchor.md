# Compositional Workload And Capability-Gate Anchor

Status: workload model supported; current from-scratch small-Transformer capability gate failed and is closed.

## 0. Thinking Card

**Phenomenon:** A long context is not necessarily a long-range reasoning task. The relevant case requires remote evidence that remains necessary after local context is known and must be combined through an intermediate state.

**Mechanism guess:** A two-table composition task isolates this computational skeleton while removing lexical shortcuts. It is useful only if the tested model can first learn the task.

**Observable metric:** full-context held-out answer accuracy, guarded by single-table and evidence-intervention controls.

**Decision:** accept the workload construction, reject further tuning of the current from-scratch learner, and require a capable shared checkpoint before objective comparison.

## 1. Problem Definition

### Terminology / Definitions

| Term | Plain meaning | Concrete object | Why it matters | Cannot prove |
|---|---|---|---|---|
| long-range compositional semantics | remote facts remain necessary and must be combined in order | $a\rightarrow b\rightarrow y$ | matches the target capability | all natural-language semantics |
| permutation table | a random one-to-one mapping over all entities | $\pi:\mathcal V\to\mathcal V$ | removes frequency and duplicate-output shortcuts | natural-language understanding |
| capability gate | proof that the shared model can solve the task before NTP/MTP comparison | held-out full-context accuracy | prevents interpreting random-task gradients | why the model learned it |

**Single decision question:** Is the workload a valid minimal model of distributed evidence composition, and is the current small learner eligible for mechanism comparison?

## 2. Physical Priors

1. Distance alone is insufficient; remote evidence must be non-substitutable.
2. No single evidence block should determine the answer.
3. The model must form an intermediate entity before selecting the correct row in the second table.
4. Objective comparisons are invalid when the model remains at chance.

## 3. Falsifiable Hypotheses

The data model predicts chance answer uncertainty from either table alone and complete determination from both tables. The learner gate predicts held-out accuracy above 0.70 with full context while single-table controls remain near chance.

## 4. Mathematical Model

Sample two independent random permutations over $M$ entities and a query entity $A$:

$$
B=\pi_1(A),
\qquad
Y=\pi_2(B).
$$

For uniform independent permutations,

$$
I(Y;\pi_1\mid A)=I(Y;\pi_2\mid A)=0,
$$

while

$$
I(Y;\pi_1,\pi_2\mid A)=H(Y\mid A)=\log M.
$$

The first table determines which row to query; the second determines the answer in that row.

## 5. Computational Realization

For $M=8$, serialize two complete tables, place controlled distractors between them, ask for a start entity, and emit three atomic tokens: a decision marker, a shared format token, and an answer entity. The standard next-token head predicts the answer after consuming the format token; Next-2 additionally predicts that answer directly from the decision state.

This is the computational skeleton of multi-document question answering, relation-chain knowledge reasoning, and cross-file code tracing. It does not include natural-language relation extraction, entity ambiguity, or open-ended generation.

It is also only a depth-two serial path through the A12 computation-tree
model. It tests intermediate-state binding and ordered composition, not
multi-branch aggregation.

## 6. Minimal Falsification Tests

1. Audit the exact data distribution and single-table information controls.
2. Require full-context held-out answer accuracy above 0.70.
3. Require single-table/local controls near chance and correct answer changes under evidence replacement.

## 7. Current Evidence

The data construction satisfies the intended joint-necessity property. The tested from-scratch Transformers did not learn it: depth, width, longer training, and atomic row-binding tokens all remained near chance, with format accuracy at 1.0. See [capacity ladder](../../../../../Projects/from-attention-to-search/main/experiments/A12/12_01_compositional_workload_capability_gate/A12_01_01_E01_composition_calibration/summary.md), [explicit-binding repair](../../../../../Projects/from-attention-to-search/main/experiments/A12/12_01_compositional_workload_capability_gate/A12_01_01_E02_explicit_binding_calibration/summary.md), and [subanchor 12_01_01](subanchors/12_01_01_workload_validity_and_learner_guard_anchor.md).

## 8. Claim Boundary And Next Decision

Supported claim: the task is a valid minimal workload for ordered two-evidence composition. The current negative result concerns the tested from-scratch sequence learners, not Transformers in general.

Not supported: MTP benefit on this task, small-versus-large scaling, a general
branching-tree mechanism, or transfer to real benchmarks.

**Exactly one next decision:** obtain one shared pretrained or explicitly structured checkpoint that passes the capability gate before any NTP/MTP comparison.
