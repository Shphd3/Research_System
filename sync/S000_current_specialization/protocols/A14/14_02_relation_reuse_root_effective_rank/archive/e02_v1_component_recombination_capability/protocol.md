---
experiment_id: A14_02_E02_component_recombination_capability
status: completed_fail
run_authorized: true
approval_date: 2026-07-23
run_id: a14_02_e02_component_recombination_capability_4gpu_20260723_full_v1
job_id: pt-zecsxjd8
primary_anchor: /Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/14_02_01_component_recombination_capability_anchor.md
---

# Protocol: A14_02_E02 Component-Recombination Capability

## 0. Approval Snapshot

**Approval status:** The user explicitly authorized a separate small anchor,
implementation, and reserved-resource full run without another approval round.
**Purpose:** Determine whether the shared NTP task supports genuine
seen-component/unseen-pair recombination.
**Primary anchor:** [historical A14_02_01](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/14_02_01_component_recombination_capability_anchor.md).
**Anchor decision question:** Can a held-out pair of individually observed
components be recombined under NTP?
**Physical prior tested:** Reusable components should transfer to a new pairing.
**Core model term tested:** Held-out component-pair answer accuracy.
**Anchor falsifier:** Seen-pair capability passes, but shared recombination
stays near answer chance.
**Experiment role:** Capability operationalization and falsification test.
**Primary metric:** Shared unseen-pair exact answer accuracy.
**Claim boundary:** Controlled synthetic NTP only; no rank or Router claim.
**Minimal setup:** Shared composition versus independent lookup, 5 paired seeds.
**Basic configuration:** 2-layer, 1-head, width-64 causal Transformer;
full-position NTP; 8 diverse training contexts per seen relation.
**Conditions to run:** `shared_components`, `lookup_tables`.
**Pass:** At least 4/5 seeds pass both seen-pair capability and shared
recombination accuracy $\ge0.80$ with consistency $\ge0.95$.
**Fail:** At least 4/5 seeds in both conditions pass seen-pair capability, but
at most 1/5 shared seeds pass recombination.
**Insufficient:** Capability mismatch, 2--3 recombination passes, leakage, or a
generator/implementation guard failure.
**Cannot claim:** Low rank, natural-language hierarchy, Transformer-wide
mechanism, or Router utility.
**Approval decision:** Approved and full-run authorized by the user.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| component | One reusable rule part | $\alpha$ or $\beta$ token | category | Defines recombination | Semantic atom |
| seen pair | A component pair present in training | $(\alpha,\beta)$ among 12 train pairs | pair | Capability guard | Component reuse |
| unseen pair | Both components seen, pair absent | One of 4 fixed matching pairs | pair | Decisive intervention | Natural-language composition |
| seen-pair new-context accuracy | Solve trained mappings under new nuisance contexts | exact answer accuracy on test contexts | proportion | Ensures the base task is learned | Algorithmic composition |
| recombination accuracy | Solve held-out pairs | exact answer accuracy over held-out pairs, entities, and test contexts | proportion | Primary metric | Low representation rank |
| semantic consistency | Equivalent contexts yield the same predicted answer | mean modal-prediction fraction per relation | proportion | Excludes unstable guessing | Correctness |

## 2. Anchor Alignment

The parent rank question remains untouched. This experiment resolves only the
capability clause that blocked A14_02_E01.

Decision question: Can NTP learn the registered reusable component
operationalization?

Falsifier: Both tasks solve seen pairs, while shared held-out-pair accuracy is
near $1/17$.

## 3. Tested Hypothesis

For shared-rule seed $j$, define $A_j^{\mathrm{recomb}}$ as exact accuracy on
the four held-out component pairs. The registered support pattern is

$$
\#\{j:A_j^{\mathrm{recomb}}\ge0.80
\ \text{and}\ C_j^{\mathrm{recomb}}\ge0.95\}\ge4.
$$

This test is evaluated only after the seen-pair capability gate.

## 4. Rival Explanations

1. Complete-table memorization rather than component reuse.
2. New-context failure rather than composition failure.
3. A primitive component absent from training.
4. Output-class imbalance or answer bottleneck.
5. Test leakage through checkpoint selection.
6. Accidental structure in the lookup control.
7. One easy held-out pair driving the macro average.

## 5. Data / Model / Algorithm / Objective

Shared rule:

$$
y=\beta(a+\alpha)\pmod {17},
$$

with four $\alpha$ values and four nonzero $\beta$ multipliers. The fixed
held-out perfect matching is

```text
(alpha 0, beta-index 1)
(alpha 1, beta-index 3)
(alpha 2, beta-index 0)
(alpha 3, beta-index 2)
```

Every component appears in three training pairs. Every seen pair contains all
17 entities and eight distinct training contexts. Calibration and test use
four disjoint contexts each.

The lookup condition uses one independent random permutation per complete
component pair. Its prefixes and per-split answer marginals exactly match the
shared condition.

Input:

```text
[alpha] [entity] [context] [beta] [ROOT] [ANSWER]
```

Model: the same `RootTaskLM` family used by A14_02_E01. Objective:
full-position next-token cross-entropy. Checkpoint selection uses only
seen-pair calibration accuracy and CE.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause / rival | Why needed | Evidence role | Pass | Fail | Insufficient | Artifact |
| --- | --- | --- | --- | --- | --- | --- | --- |
| shared components | reusable recombination | Primary test | Primary | 4/5 recombination passes | at most 1/5 after capability | 2--3/5 or capability failure | capability table |
| lookup tables | table-memorization control | Verifies base surface and leakage | Hard guard | 4/5 seen-pair passes; unseen-pair $\le0.20$ | — | seen failure or leakage | capability table |
| generator audit | split and marginal validity | Excludes construction artifacts | Hard gate | all exact checks pass | — | any failure | generator audit |
| held-out-pair breakdown | one easy pair | Requires broad recombination | Secondary guard | every pair mean $\ge0.70$ | one-pair collapse | unstable | pair table |

Seeds: `[0, 1, 2, 3, 4]`, paired across conditions.

Checkpoint: first checkpoint with calibration answer accuracy $\ge0.95$ and
answer CE $\le0.10$ for three consecutive evaluations. Maximum 6000 update
steps; no condition-specific extension.

## 7. Primary Metric

**Metric:** shared unseen-pair exact answer accuracy.

**Computation:** number of correct answer tokens divided by all held-out-pair,
entity, and test-context examples.

**Decision role:** It directly distinguishes component reuse from memorizing
the 12 observed complete pair tables.

**False-positive cost:** Passing a leaky or answer-imbalanced surface would
incorrectly authorize a rank comparison. Therefore generator, component
coverage, lookup, and checkpoint-selection guards are hard.

## 8. Secondary Metrics

- seen-pair calibration and test answer CE/accuracy;
- recombination semantic consistency;
- accuracy for each of the four held-out pairs;
- training step at capability;
- lookup unseen-pair accuracy as a leakage diagnostic.

## 9. Known Good / Known Bad / Known Confusing Cases

- Known good: every shared and lookup mapping is a permutation, so answers are
  balanced.
- Known bad: unseen lookup tables should stay near $1/17$ accuracy.
- Known confusing: training fit without seen-pair new-context capability is
  memorization and yields `insufficient`.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| generator | Is the split valid and matched? | manifests | all checks pass | `generator_audit.json` | train |
| train | Is the base task learned? | calibration trajectory | capability gate | per-job JSON | test |
| seen test | Does capability transfer to new contexts? | seen-pair test | threshold | result table | recombination |
| recombination | Are unseen pairs solved? | held-out test | pass/fail rule | pair table | decision |
| merge | Is the result stable? | 10 jobs | 5-seed rule | decision JSON / figure | result record |

## 11. Algorithm Specification

Input: fixed manifests, condition, model seed.

Steps:

1. Audit component coverage, pair holdout, contexts, prefixes, and marginals.
2. Train with a condition-independent optimizer and budget.
3. Select a checkpoint using seen-pair calibration only.
4. Evaluate seen-pair new-context and unseen-pair recombination.
5. Aggregate paired five-seed results without post-hoc threshold changes.

Outputs: per-job JSON, merged CSV tables, `decision.json`, central figure,
checkpoints, and runtime logs.

## 12. Success / Failure / Insufficient Evidence

The first-page definitions are binding. Scientific pass additionally requires
all four held-out pairs to have mean accuracy at least $0.70$. A lookup
unseen-pair accuracy above $0.20$ in any capability-passing seed triggers
`insufficient`, not support.

## 13. What This Cannot Claim

This experiment does not measure functional rank. It cannot establish the
A14 conditional-rank theorem in Transformers, natural-language hierarchy,
parameter compression, or expert specialization.

## 14. Review Notes And Protocol Changes

2026-07-23: Created as a separate capability anchor after the user explicitly
required preservation of A14_02_E01 and authorized immediate full execution.
No E01 condition, threshold, result, or file was changed.

2026-07-23: Submitted the frozen 10-unit full run as ACP job `pt-zecsxjd8`
on one reserved `n6ls.iu.i40.4` worker (4 GPUs). Run ID:
`a14_02_e02_component_recombination_capability_4gpu_20260723_full_v1`.

2026-07-23: The job completed `SUCCEEDED`; the scientific verdict is `fail`.
See [summary.md](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/summary.md) and [detailed.md](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/detailed.md). No threshold,
condition, or E01 artifact was changed after observing the result.
