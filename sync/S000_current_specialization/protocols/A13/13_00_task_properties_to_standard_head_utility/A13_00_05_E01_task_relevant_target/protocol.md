# Protocol: A13_00_05_E01 Task-Relevant Relay Target

## 0. Approval Snapshot

Approval status: approved under standing autonomous authorization.

Purpose: distinguish downstream task relevance from generic variable-target
supervision at the already localized relay position.

## 1. Terminology / Definitions

`Answer-aux` predicts $A$ at the relay; `nuisance-aux` predicts independent
value $B$. Both use the same value vocabulary and position.

## 2. Anchor Alignment

Primary anchor:
[13_00_05](/Projects/from-attention-to-search/main/problem_anchors/13_mtp_task_property_decomposition/13_00_task_properties_to_standard_head_utility/subanchors/13_00_05_task_relevant_relay_target_anchor.md)

## 3. Tested Hypothesis

Answer-aligned relay supervision has positive ordinary-head utility relative
to nuisance-matched relay supervision, and the utility is larger when relay
transport is required.

## 4. Rival Explanations

The earlier localization was caused by target variability, token frequency,
conditional entropy, auxiliary-head scale, other Next-2 positions, or direct
path regularization rather than downstream relevance.

## 5. Data / Model / Algorithm / Objective

Use the frozen `copy_matched` carrier and full A13_00_04 contract. The two
auxiliary target arrays differ only in their last element:

```text
nuisance control: [x2 x3 x4 x5 B]
answer-aligned:   [x2 x3 x4 x5 A]
```

$A$ and $B$ are iid uniform in the full generator and both are visible to the
relay. Their per-token marginal counts match exactly inside both realized
splits. The combination split induces within-split association, so nuisance
means structurally non-causal under the answer rule, not statistically
independent in the evaluation subset.

## 6. Conditions, Seeds, And Checkpoints

Paths: relay and bypass. Objectives: nuisance-aux and answer-aux. Fresh paired
seeds: 1701--1708. Train 3,000 steps; primary AULC remains 0--1,000.

## 7. Primary Metric

$$
R_r=\operatorname{AULC}_{B,r}-\operatorname{AULC}_{A,r},
\qquad
\Delta_R=R_{\mathrm{relay}}-R_{\mathrm{bypass}}.
$$

Pass requires positive bootstrap lower bounds, means at least 0.02 nats, and
at least seven of eight positive seeds for both quantities.

## 8. Guard Logic

The NTP carrier is a pre-treatment validated fact. Arm capability is an
outcome. Causal donor use is reported among capability-eligible models and does
not select paired performance observations.

## 9. Secondary Metrics

Final capability, relay auxiliary accuracy, donor follow, initial gradient
norm/cosine, first step to 90% answer accuracy, and comparison with fixed-marker
localization.

## 10. Known Good / Known Bad / Known Confusing Cases

Known good: full answer-aux reached final 1.0 accuracy in all 24 seeds across
A13_00_03 E01/E02 and A13_00_04.

Known confusing: $B$ is a past token rather than a literal future target. It
is a causal content control, not a deployable MTP objective.

Known confusing: the held-out-pair split associates $A$ and $B$ within each
subset. The registered counterfactual object is
$Y(A=a,B=b)=a$ for every $b$, not zero subset mutual information.

## 11. Algorithm Specification

Replay paired initializations and mini-batches. Change only the registered
relay auxiliary label.

## 12. Success / Failure / Insufficient Evidence

Pass/fail follows the registered effect criteria. A failed arm-use diagnostic
limits interface claims but does not erase a randomized objective effect.

## 13. What This Cannot Claim

The nuisance control isolates relevance in this synthetic carrier; it does not
show that standard future text naturally supplies such a control or that the
effect transfers to a real workload. It does not remove observational
association created by the split.

## 14. Review Notes And Protocol Changes

Relative to A13_00_04, only the reference relay label changes from a fixed
marker to same-distribution nuisance $B$; all thresholds and other objects are
unchanged.
