# Protocol: A06_01_05_E03 Gradient/Fisher Route-State Selector

## 0. Approval Snapshot

Approval status: user requested protocol plus full run after reviewing the
minimal anchor in conversation.

Purpose: Test whether label-free gradient or Fisher signals can select
route-relevant hidden states from the all-position pool and initialize router
rows for uniform feature distribution.

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Anchor decision question: Can gradient/Fisher signals beat all-position
clustering and approach route-position control on feature separation and
positive margin?

Anchor physical prior tested: hidden states that affect the supervised
prediction should carry stronger or more structured gradient signals.

Anchor core model term tested: feature-center margin induced by rows built from
gradient-selected or Fisher-weighted hidden states.

Anchor falsifier: gradient/Fisher conditions fail to improve over
all-position clustering or improve NMI without positive margin.

Experiment role: operationalization / proxy test and method-readiness gate.

Primary metric from anchor: immediate feature NMI after router reinitialization.

Claim boundary from anchor: uniform no-position synthetic slot dataset only.

Minimal setup: one-layer causal Transformer, one weighted top-1 MoE layer, no
position embeddings, four uniformly sampled features, repeated feature slots,
neutral background, feature-specific target, and balanced evaluation.

Basic configuration: seeds 0--7, slot lengths 1/2/4/8, warmup steps 0/10/40,
post-reinit train checkpoints 0/10/40/80/160.

Conditions to run: all-position centered clustering, route-position centered
clustering, oracle centers, post-hidden gradient magnitude, post-hidden
gradient weighting, post-hidden gradient direction, post-hidden Fisher
subspace, embedding-gradient magnitude, embedding-gradient weighting,
embedding-gradient direction, and embedding-gradient Fisher subspace.

Pass: at least one gradient/Fisher condition beats all-position clustering,
approaches route-position control, has positive margin p05, preserves after
training, and has low slot-start NMI.

Fail: no gradient/Fisher condition improves over all-position, or gains are
NMI-only with negative margin p05.

Insufficient: route-position or oracle controls fail, target accuracy fails,
full seed/slot coverage is incomplete, or selector diagnostics are missing.

Cannot claim: real-DCLM transfer, semantic experts, common/rare routing, expert
utility, or optimality of the gradient/Fisher rule.

Approval decision: execute full local GPU run.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Post-hidden gradient | Loss sensitivity at router input states | \(\nabla_{h_{i,p}}\mathcal L_i\) after attention and layer norm | Vector | Tests the direct MoE-router state | Real feature semantics |
| Embedding gradient | Loss sensitivity at token embeddings | Gradient at embedding output before attention | Vector | Tests whether earlier causal context positions are visible | Router-ready state quality |
| Gradient magnitude selector | Choose positions by gradient energy | top-1 per sample by \(\|g_{i,p}\|_2^2\) | Position set | Tests task-position localization | Feature separation |
| Gradient-weighted clustering | Let all positions contribute with gradient weights | weighted k-means on centered hidden states | Cluster centers | Tests soft route-state selection | True causal importance |
| Gradient-direction clustering | Cluster selected gradient directions, then average hidden states | k-means on normalized gradients | Router rows | Tests whether direction carries class/feature information | Stable margin |
| Fisher-subspace clustering | Cluster hidden states after projecting onto gradient covariance directions | top eigenspace of \(\mathbb E[gg^\top]\) | Router rows | Tests loss-sensitive geometry | Full Fisher optimality |
| Feature NMI | Agreement between feature id and selected expert | NMI(feature, route) | 0--1 | Primary separation metric | Utility |
| Margin p05 | Lower-tail matched route safety | 5th percentile matched score gap | Logit difference | Preservation guard | Loss optimality |
| Slot-start NMI | Position shortcut guard | NMI(slot_start, route) | 0--1 | Detects positional leakage | All nuisance absence |

## 2. Anchor Alignment

Decision question: Can gradient/Fisher signals find a better route-state pool
than all-position clustering without feature labels?

Physical prior tested: task loss should expose route-relevant hidden states.

Core model term tested: router rows built from selected states should increase
feature-center margin.

Falsifier: the selector does not beat all-position or only improves NMI while
leaving margin p05 negative.

Claim boundary: synthetic uniform no-position bridge.

## 3. Tested Hypothesis

Gradient magnitude should identify positions that affect target prediction.
Gradient direction or Fisher-weighted distance should then help separate
features inside those task-relevant states.

## 4. Rival Explanations

- Loss-locality shortcut: post-hidden gradient only marks the supervised
  position.
- Direction-only class signal: gradient direction separates labels but does
  not produce stable hidden-space router rows.
- Nuisance-pool failure: Fisher projection still clusters background or slot
  position rather than feature.
- Margin failure: feature NMI improves but lower-tail margin stays negative.

## 5. Data / Model / Algorithm / Objective

Data: same uniform no-position slot bridge as A06_01_05_E01/A06_01_05_E02. Features 0--3 are
balanced. Slot starts are balanced. The audited route position is the final
token of the repeated feature slot. The objective is cross-entropy at that
route position for the feature-specific target token.

Model: one-layer causal self-attention, one weighted top-1 MoE layer, no
explicit position embeddings, and one LM head.

Algorithm: warm up, collect hidden states and gradients on calibration data,
build candidate router rows, reset router rows, evaluate immediate routing,
continue training, and evaluate preservation.

## 6. Conditions, Seeds, And Checkpoints

| Item | Role | Primary evidence | Guard |
| --- | --- | --- | --- |
| `allpos_centered` | Failure baseline | feature NMI, margin p05 | slot-start NMI |
| `route_centered` | Positive control | feature NMI, margin p05 | target accuracy |
| `oracle_centered` | Upper bound | feature NMI, margin p05 | target accuracy |
| `grad_h_topk_centered` | post-hidden hard selector | feature NMI, margin p05 | selected route fraction |
| `grad_h_weighted_centered` | post-hidden soft selector | feature NMI, margin p05 | gradient mass distribution |
| `grad_h_direction_centered` | post-hidden direction classifier | feature NMI, margin p05 | selected route fraction |
| `fisher_h_topdim_centered` | post-hidden Fisher geometry | feature NMI, margin p05 | Fisher shortcut diagnostics |
| `grad_emb_topk_centered` | embedding hard selector | feature NMI, margin p05 | selected slot/route fraction |
| `grad_emb_weighted_centered` | embedding soft selector | feature NMI, margin p05 | gradient mass distribution |
| `grad_emb_direction_centered` | embedding direction classifier | feature NMI, margin p05 | selected slot/route fraction |
| `fisher_emb_topdim_centered` | embedding-gradient Fisher geometry | feature NMI, margin p05 | coordinate-boundary note |

Seeds: 0--7. Slot lengths: 1, 2, 4, 8. Warmup steps: 0, 10, 40.
Checkpoints after router reset: 0, 10, 40, 80, 160.

## 7. Primary Metric

Immediate feature NMI decides whether the selector separates uniform features
at router initialization. Margin p05 is the required guard because high NMI
without positive lower-tail margin is not a stable routing basin.

## 8. Secondary Metrics

Matched preserve fraction, final feature NMI, positive margin fraction,
sign-flip rate, max load, effective experts, target accuracy, slot-start NMI,
selected route fraction, selected slot fraction, selected target fraction, and
gradient score mass by position role.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: route-position and oracle centered rows should score high.

Known bad: all-position centered clustering is the baseline to beat.

Known confusing: post-hidden gradient can trivially mark the supervised route
position because the loss is evaluated at that position. This is useful for
state selection but cannot by itself prove feature understanding.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Pass / fail / unclear rule | Debug artifact |
| --- | --- | --- | --- |
| Data audit | Are features and slot starts balanced? | pass if balanced | `tables/data_audit.csv` |
| Signal audit | Where does gradient mass go? | route/slot/target fractions interpretable | `tables/selector_diagnostics.csv` |
| Reinit audit | Which rows separate features immediately? | feature NMI plus margin p05 | `tables/condition_aggregate_reinit.csv` |
| Training audit | Does the partition survive? | final NMI and preserve fraction | `tables/condition_aggregate_final.csv` |
| Failure audit | Which signal form fails? | compare magnitude, direction, Fisher | summary/detailed |

## 11. Algorithm Specification

Input: warmed model, calibration data, evaluation data, method list.

Parameters: selector top-k = 1 per sample; Fisher dimension = 8; k-means
clusters = 4; router row scale = 1.5.

Steps:

1. Generate balanced calibration and evaluation data.
2. Warm up one base model for each requested warmup step.
3. Collect all-position hidden states and gradients.
4. Build router rows from baseline and gradient/Fisher methods.
5. Reset only router rows on the warmed model.
6. Evaluate immediate route assignments and margins.
7. Continue training and evaluate checkpoints.
8. Aggregate tables, figures, and result records.

## 12. Success / Failure / Insufficient Evidence

Success: a gradient/Fisher method reaches route-position-like feature NMI and
positive margin p05 while keeping slot-start NMI low.

Failure: all gradient/Fisher methods fail to beat all-position, or their gains
come without positive margin.

Insufficient: controls fail, full coverage is missing, or selector diagnostics
are not available.

## 13. What This Cannot Claim

This cannot claim real-DCLM transfer, semantic experts, common/rare routing,
expert utility, or an optimal route-state selection algorithm.

## 14. Review Notes And Protocol Changes

Created before execution on 2026-07-05.
