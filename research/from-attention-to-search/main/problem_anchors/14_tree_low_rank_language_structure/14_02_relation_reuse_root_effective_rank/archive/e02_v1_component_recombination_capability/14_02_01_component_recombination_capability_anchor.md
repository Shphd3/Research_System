---
anchor_id: 14_02_01_component_recombination_capability
status: closed_falsified
canonical_language: en
companion_language: zh
parent_anchor: 14_02_relation_reuse_root_effective_rank
---

# A14_02_01 Component-Recombination Capability Under NTP

researcher judgment record source:
14_02 relation reuse and ROOT functional rank

## 1. Problem Definition

The parent A14_02 question asks whether a reusable compositional rule requires
fewer task-functional ROOT directions than a matched independent lookup. That
rank comparison is not interpretable until the shared condition has actually
learned a reusable computation.

**Decision question:**

> Under next-token prediction, can the registered shared-rule task solve a
> held-out pairing of two components when every component was observed in
> training with other partners?

An **unseen component pair** is an ordered pair $(\alpha,\beta)$ absent from
training although $\alpha$ and $\beta$ each occur in other training pairs.
Recombination accuracy is exact answer-token accuracy on all entities and new
nuisance contexts for those held-out pairs. It is a capability test, not a
rank measure.

## 2. Physical Priors

1. A reusable two-stage computation should be callable after its components
   were learned in different pairings.
2. Repeating the same complete input-output table is not evidence of component
   reuse.
3. New-context invariance is a prerequisite: a model that cannot solve seen
   mappings in unseen nuisance contexts has not reached the capability surface.

The main prior is falsified on this registered task if seen-pair capability
passes but shared-rule recombination remains near chance.

## 3. Falsifiable Hypotheses

**Primary hypothesis.** The shared generator supports unseen-pair
recombination after diverse-context NTP training.

**Strongest rival.** The Transformer learns complete
$(\alpha,\beta,a)\mapsto y$ tables rather than reusable components; therefore
it solves seen pairs but not held-out pairs.

Predictions:

- hypothesis: seen-pair new-context capability passes and shared held-out-pair
  accuracy is at least $0.80$ in at least four of five seeds;
- rival: both conditions solve seen pairs, while shared held-out-pair accuracy
  remains near the $1/17$ answer chance rate;
- insufficient: either condition fails the seen-pair gate, the result is
  unstable across seeds, or a generator/leakage guard fails.

## 4. Mathematical Model

Entities are $a\in\mathbb Z_{17}$. The two component families are
$\alpha\in\{0,1,2,3\}$ and
$\beta\in\{1,2,4,8\}$. The shared task is

$$
u=a+\alpha\pmod {17},
\qquad
y=\beta u\pmod {17}.
$$

Four component pairs form a fixed perfect matching and are removed from
training. The remaining twelve pairs contain every $\alpha$ and every $\beta$
three times, so success cannot be explained by seeing a new primitive token at
test time.

The lookup control replaces each complete pair with an independent random
permutation of $\mathbb Z_{17}$. It shares the same prefixes, split, answer
marginals, exposure, model, and objective. It should solve seen pairs in new
contexts but has no rule for an unobserved random table.

## 5. Computational Realization

Each sequence is

```text
[alpha] [entity] [nuisance-context] [beta] [ROOT] [ANSWER]
```

A two-layer, one-head, width-64 causal Transformer is trained with
full-position NTP cross-entropy. Each seen relation receives eight distinct
training contexts. Calibration and test use disjoint contexts. Checkpoint
selection uses seen-pair calibration only; held-out-pair results never select a
checkpoint or hyperparameter.

## 6. Minimal Falsification Tests

The decisive test is
[historical A14_02_E02 protocol](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/protocol.md).

Required guards:

- exact prefix, sample-count, and answer-marginal matching;
- all primitive components occur in training;
- train, calibration, and test contexts are disjoint per relation;
- both shared and lookup pass seen-pair new-context capability;
- lookup held-out-pair performance remains below the leakage threshold.

No ROOT rank, parameter rank, Jacobian, or Router metric is part of this test.

## 7. Current Evidence

The parent
[A14_02_E01 result](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/summary.md)
was insufficient for the shared-versus-lookup rank decision. It established
that duplicate exposure did not create new-context invariance, but its shared
condition never passed the registered composition gate.

The separate
[historical A14_02_E02 full run](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/summary.md)
completed all 10 jobs and passed every generator guard. Both conditions passed
seen-pair new-context capability in 5/5 seeds, with mean accuracies 0.9990
(shared) and 0.9949 (lookup). The decisive shared unseen-pair test passed in
0/5 seeds: mean accuracy was 0.2125 against the 0.80 gate, and all four
held-out-pair means were below 0.70. Lookup averaged 0.0640, near $1/17$
chance, with no leakage failure.

Shared performance exceeded lookup descriptively in every paired seed, but it
ranged from 0.088 to 0.515 and never reached the operational capability gate.
This is compatible with weak partial structure use, not a learned reusable
algorithm.

## 8. Claim Boundary And Next Decision

The registered capability hypothesis is falsified on this controlled surface:
learning seen mappings under new contexts did not yield reliable held-out
component-pair recombination. Therefore this surface is not eligible for the
proposed shared-versus-lookup ROOT functional-rank comparison.

This does not show that NTP cannot learn composition in general, that the
network used only lookup memorization, that the controlled conditional-rank
theorem is false, that natural language is not hierarchical, or that any
Router is useful.

**Exactly one next decision:** decide whether to park the current A14_02
synthetic surface rather than launch a ROOT rank experiment on a task that
failed its composition-capability gate.
