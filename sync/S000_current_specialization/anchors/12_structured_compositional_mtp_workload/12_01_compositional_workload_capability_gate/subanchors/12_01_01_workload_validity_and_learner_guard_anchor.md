# Workload Validity And Learner-Eligibility Guard


## 1. Problem Definition

**Parent problem:** [12_01 compositional workload capability gate](../12_01_compositional_workload_capability_gate_anchor.md).
**Decision question:** Is the two-table task valid, and is the tested checkpoint eligible for NTP/MTP comparison?
**Not in scope:** explaining all Transformer task-learning failures.

The **capability gate** requires the same checkpoint to solve unseen full-context examples, remain near chance with either table removed, and change answers correctly after evidence replacement. It prevents objective claims on an unlearned task.

## 2. Physical Priors

**P1:** Independent complete permutations make either table alone uninformative about the answer.
**P2:** A checkpoint at chance cannot identify objective-level composition mechanisms.

## 3. Falsifiable Hypotheses

The data hypothesis is supported if partial evidence remains at chance and both tables determine the answer. Learner eligibility is supported only if full-context held-out accuracy exceeds the registered threshold and intervention guards pass.

## 4. Mathematical Model

$$
B=\pi_1(A),\qquad Y=\pi_2(B).
$$

For independent uniform permutations, either table alone leaves $Y$ uniform, while both tables determine it. The learner falsifier is near-chance full-context accuracy despite a correct output interface.

## 5. Computational Realization

Serialize two complete $M=8$ tables using atomic task tokens; train on fresh permutations; evaluate unseen permutations, single-table controls, and evidence swaps.

## 6. Minimal Falsification Tests

1. Verify the analytical and empirical single-table guards.
2. Require full-context held-out answer accuracy above 0.70 and format accuracy above 0.99.
3. Require correct counterfactual answers after table-row replacement.

## 7. Current Evidence

The distribution passes the joint-evidence audit. The [capacity ladder](/Projects/from-attention-to-search/main/experiments/A12/12_01_compositional_workload_capability_gate/A12_01_01_E01_composition_calibration/summary.md) and [explicit-binding repair](/Projects/from-attention-to-search/main/experiments/A12/12_01_compositional_workload_capability_gate/A12_01_01_E02_explicit_binding_calibration/summary.md) remain near $1/8$ answer chance while format accuracy reaches 1.0.

## 8. Claim Boundary And Next Decision

**Can claim:** the task construction is valid; the tested learner branch is ineligible.
**Cannot claim:** MTP failure or Transformer impossibility.
**Next decision:** evaluate one pretrained or explicitly structured shared checkpoint against the same gate before any objective comparison.
