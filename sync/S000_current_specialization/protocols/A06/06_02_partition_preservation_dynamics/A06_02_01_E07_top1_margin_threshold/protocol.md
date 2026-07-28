# Protocol: A06_02_01_E07 Top-1 Lock-In Margin Threshold

## 0. Approval Snapshot

**Approval status:** approved by user request on 2026-07-01.

**Purpose:** test whether positive top-1 margin creates a lock-in basin, or
whether preservation degrades smoothly as initial margin is made thin.

**Primary anchor:** `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/subanchors/06_02_01_finite_margin_basin_anchor.md`

**Anchor decision question:** If step-0 assignment is correct but the positive
margin is made very small, does training preserve the original
feature-to-expert identity?

**Anchor physical prior tested:** top-1 routing has path dependence once
feature assignment is stable.

**Anchor core model term tested:** row-gap scale $q$ and pairwise route margin
$\gamma_{f,e}$.

**Anchor falsifier:** $q>0$ fails to preserve step-0 assignment or fails to
scale margin; or thin positive margins collapse smoothly with q.

**Experiment role:** root-cause audit and mechanism threshold test.

**Primary metric from anchor:** matched preserve fraction at steps 5, 10, and
1600.

**Claim boundary from anchor:** controlled no-position bridge only.

**Minimal setup:** A06 controlled no-position bridge; one-layer Transformer +
top-1 MoE; 4 experts; slot length 4; route on the last slot token; no learned
absolute positional embedding; no B token.

**Basic configuration:** C0-C3 cells, 8 seeds, 1600 steps, checkpointed
margin-budget audit.

**Conditions to run:** `gap_q1p0`, `gap_q0p5`, `gap_q0p25`, `gap_q0p1`,
`gap_q0p05`, `gap_q0p02`, `gap_q0p0_guard`, `cross_alpha1p25_guard`.

**Pass for lock-in:** all positive-q conditions keep high matched preserve
fraction, near-zero sign flips, and high feature NMI.

**Pass for passive budget:** small positive-q conditions show early sign flips,
negative margins, and reduced matched preserve fraction.

**Insufficient:** q-scaling does not reduce step-0 margin as intended, q>0
changes step-0 assignment, or training/loss fails generically.

**Cannot claim:** real-DCLM behavior, semantic experts, expert utility, or
that lock-in solves preservation.

**Approval decision:** implement and run.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| Row-gap scale | Shrinks router rows toward their mean. | $w'_e=\bar w+q(w_e-\bar w)$ | scalar q | Controls initial margin without changing signs for q>0. | Real-data behavior. |
| Matched preserve fraction | Original feature-expert identity preservation. | Fraction routed to step-0 matched expert. | fraction | Primary lock-in metric. | Utility. |
| Sign flip | Pairwise margin crosses zero. | $\gamma_{f,e}(t)\le 0$. | rate | Detects boundary crossing. | Semantic meaning. |
| Crossed guard | Deliberately crossed initialization. | $w'_a=(1-\alpha)w_a+\alpha w_j$, $\alpha=1.25$. | scalar alpha | Checks whether training recovers a broken original identity. | Natural training crossing. |

## 2. Anchor Alignment

**Decision question:** positive thin margin lock-in versus passive margin
budget.

**Physical prior tested:** top-1 routing can create path-dependent assignment
basins.

**Core model term tested:** pairwise margin scale and sign.

**Falsifier:** q>0 preserves step-0 assignment but small-q conditions lose
matched preserve smoothly with q.

**Claim boundary:** controlled bridge only.

## 3. Tested Hypothesis

H1 lock-in: every positive-q condition with valid step-0 assignment preserves
the original feature-to-expert identity.

H2 passive budget: lower q makes margin easier to consume and causes earlier
sign flips and lower matched preserve.

## 4. Rival Explanations

- q did not actually shrink margin.
- q changed step-0 assignment, invalidating the lock-in test.
- feature NMI remains high after expert identity swaps.
- crossed guard recovers due to training rather than initialization.
- task accuracy hides routing failure.

## 5. Data / Model / Algorithm / Objective

Data/model match A06_02_01_E06:

- controlled A06 no-position bridge;
- one-layer Transformer + top-1 MoE, 4 experts, `d_model=128`;
- 4 feature ids, 4 nuisance ids, slot length 4;
- slot starts `[2, 10, 18]`;
- route position is the last token of the feature slot;
- no learned absolute positional embedding and no B token;
- target depends only on feature identity;
- objective is slot-end target cross-entropy.

Algorithm:

1. Discover pseudo centers from route-position hidden states.
2. Initialize router rows from pseudo centers.
3. Apply row-gap scaling or crossed guard.
4. Verify step-0 assignment and margin scaling.
5. Train and compute A06_02_01_E06 margin-budget metrics.

## 6. Conditions, Seeds, And Checkpoints

Seeds: `20260623` through `20260630`.

Cells: `C0_clean`, `C1_mild_nuisance`, `C2_moderate_nuisance`,
`C3_weak_feature_nuisance`.

Checkpoints: `0, 1, 2, 5, 10, 20, 50, 100, 200, 400, 800, 1600`.

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
|---|---|---|---|---|---|---|---|---|
| q sweep | H1/H2 | row-gap margin scale | separates lock-in from passive budget | primary | positive q preserves | smooth q collapse | q invalid | threshold table |
| q=0 guard | H1 | no positive margin | positive-margin necessity guard | secondary | identity fails | identity preserves | tie untracked | guard row |
| crossed guard | H3 | crossed boundary | checks recovery from broken identity | secondary | low preserve | recovery | step-0 unclear | guard row |

## 7. Primary Metric

Primary metric: matched preserve fraction at steps 5, 10, and 1600.

Why it decides: lock-in is a claim about preserving the original
feature-to-expert identity. Feature NMI alone can stay high after expert
identity swaps.

## 8. Secondary Metrics

- feature NMI;
- current margin;
- sign flip rate;
- cluster-aware margin;
- target accuracy and loss;
- max load;
- step-0 margin scale ratio.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: pseudo-center initialization from A06_02_01_E06 preserves perfectly.

Known bad: crossed post-hoc intervention in A06_02_01_E04 destroys matched
preserve fraction.

Known confusing: q=0 has exact tied rows and may depend on deterministic
tie-breaking; it is a no-margin guard, not a positive-margin condition.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
|---|---|---|---|---|---|
| Step-0 intervention audit | Did q shrink margin while preserving assignment? | step-0 NMI, preserve, margin ratio | q>0 must preserve; margin ratio must track q | intervention audit table | summary |
| Training audit | Does thin margin preserve? | step 5/10/final preserve | compare positive q conditions | threshold table | summary |
| Guard audit | Do no-margin/crossed guards fail identity? | q=0/crossed preserve | expected low preserve | guard table | detailed |

## 11. Algorithm Specification

Input: pseudo-center initialized router rows, audit hidden states, feature
labels, and controlled bridge training batches.

Parameters: q values `[1.0, 0.5, 0.25, 0.1, 0.05, 0.02, 0.0]`; crossed alpha
`1.25`; 8 seeds; C0-C3; checkpoints through 1600.

Steps:

1. Initialize pseudo-center router rows.
2. For q condition, replace rows by $\bar w+q(w_e-\bar w)$.
3. For crossed guard, move each matched row toward its nearest competitor with
   alpha 1.25.
4. Save step-0 intervention audit.
5. Train with the A06_02_01_E06 loop.
6. Aggregate matched preserve, NMI, margin, sign flip, and loss.

Outputs: `summary.md`, `detailed.md`, tables, figures, anchor update.

## 12. Success / Failure / Insufficient Evidence

Support lock-in: all positive q conditions preserve high matched identity and
show near-zero sign flips.

Support passive budget: smaller positive q conditions show early sign flips
and lower matched preserve.

Insufficient: intervention invalid, loss failure, or q=0 tie behavior cannot
be separated from implementation artifacts.

## 13. What This Cannot Claim

This cannot claim real-DCLM preservation, semantic experts, expert utility, or
that lock-in is enough to solve preservation.

## 14. Review Notes And Protocol Changes

Created after user approved row-gap scaling as the clean intervention.
