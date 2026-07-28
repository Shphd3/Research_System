# Protocol: A06_01_05_E01_warmup_spectral_reinit

## 0. Approval Snapshot

Approval status: user requested full local 2-GPU execution after discussing the
three linked experiments.

Purpose: Test whether a short warmup makes all-position hidden-state clustering
or expert top singular directions usable for router reinitialization on the
uniform no-position slot dataset.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/subanchors/06_01_05_warmup_spectral_gradient_selector_audit_anchor.md`

Anchor decision question: After a short warmup, do all-position hidden-state
clustering or expert top singular directions become feature-aware enough to
initialize router rows for uniform feature distribution?

Anchor physical prior tested: step-0 geometry may be too unformed, but warmup
geometry must still be route-relevant and feature-aware to initialize a router.

Anchor core model term tested: feature-center margin induced by candidate rows
from hidden-state centers or expert singular directions.

Anchor falsifier: warmup all-position or warmup expert SVD reaches
route-position feature NMI and positive margin while slot-start NMI remains low.

Experiment role: root-cause audit and method-readiness gate.

Primary metric from anchor: feature NMI on balanced route-position evaluation.

Claim boundary from anchor: uniform no-position synthetic slot dataset only.

Minimal setup: one-layer causal Transformer, one weighted top-1 MoE layer, no
position embeddings, four uniformly sampled features, repeated feature slots,
neutral background, feature-specific targets, local two-GPU full run.

Basic configuration: seeds 0--7, slot lengths 1/2/4/8, warmup steps 0/10/40,
post-reinit train checkpoints 0/10/40/80/160.

Conditions to run: no-reinit controls, all-position centered k-means,
route-position centered k-means, oracle centered feature centers, raw expert
SVD rows, common-projected expert SVD rows, and orthogonalized expert SVD rows.

Pass: a warmup all-position or expert SVD condition approaches route-position
clustering on feature NMI and margin p05 without slot-start leakage or target
loss failure.

Fail: warmup all-position and expert SVD remain far below route-position /
oracle controls, or gains are explained by slot-start routing.

Insufficient: route-position or oracle controls fail, target accuracy fails,
the full run does not complete seed/slot coverage, or slot-start NMI is high.

Cannot claim: real-DCLM transfer, semantic experts, deployable MPI router, or
spectral routing impossibility.

Approval decision: execute full local 2-GPU run.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Uniform feature | Four features sampled equally | Feature ids 0--3, each probability 0.25 | Probability | Tests geometry, not frequency skew | Real language semantics |
| Route position | Task-relevant token | Last token of repeated slot | Sequence index | Routing metric is tied to target prediction | Real route selection |
| Warmup | Training before router reset | 0, 10, or 40 optimization steps | Steps | Tests whether geometry appears after early learning | Long-run method validity |
| All-position centered k-means | Cluster all token hidden states after mean subtraction | k-means on $h-c_{\mathrm{all}}$ | Condition | Tests global hidden geometry | Route relevance |
| Route-position centered k-means | Cluster route-position hidden states after mean subtraction | k-means on route $h-c_{\mathrm{route}}$ | Positive control | Shows available route geometry | Real labels |
| Expert SVD row | Router row from expert top input singular vector | Top right singular vector of expert first linear layer | Unit vector | Tests expert parameter spectral geometry | Expert utility |
| Feature NMI | Feature/expert agreement | NMI(feature id, route) | 0--1 | Primary separation metric | Utility |
| Matched preserve fraction | Fixed feature-to-expert assignment survival | assign equals step-0 mapping(feature) | 0--1 | Detects identity loss | Semantics |
| Margin p05 | Lower-tail route safety distance | 5th percentile matched score gap | Logit difference | Tests basin thickness | Loss optimality |
| Slot-start NMI | Position nuisance agreement | NMI(slot_start, route) | 0--1 | Position shortcut guard | No context effect |

## 2. Anchor Alignment

Decision question: Does warmup make all-position hidden geometry or expert
spectral geometry usable for router reinitialization?

Physical prior tested: warmup can form geometry, but only route-relevant,
feature-aware geometry should improve routing.

Core model term tested: $\gamma_f=w_{m(f)}^\top\mu_f-\max_{e\ne m(f)}w_e^\top\mu_f$.

Falsifier: warmup all-position or expert SVD matches route-position / oracle on
feature NMI and margin with low slot-start NMI.

Claim boundary: no-position uniform synthetic slot dataset.

## 3. Tested Hypothesis

The primary hypothesis is that delayed reinitialization only works when the
candidate geometry is feature-aware. Warmup may improve hidden or expert
geometry, but all-position pooling and expert top singular vectors can still be
wrong sources if they are common-aligned, near-parallel, or locked to current
routing feedback.

## 4. Rival Explanations

- Unformed representation: step-0 all-position fails but warmup all-position
  succeeds.
- Wrong population: warmup all-position remains worse than route-position.
- Row similarity: expert SVD rows are too close to separate features.
- Common alignment: expert SVD rows align with the mean/common direction.
- Feature-unaware spectrum: expert SVD rows are distinct but do not give
  positive feature-center margins.
- Shortcut: apparent improvement tracks slot start rather than feature id.

## 5. Data / Model / Algorithm / Objective

Data: sequences contain neutral background tokens, one repeated feature slot,
and a feature-specific target token after the slot. Features 0--3 are uniformly
sampled for calibration, warmup, training, and evaluation. Slot starts are
balanced.

Model: one-layer causal self-attention, one weighted top-1 MoE layer, no
explicit position embeddings, and one LM head.

Objective: cross-entropy at the route position predicting the feature-specific
target token.

Algorithm: warm up, extract geometry, reset router rows, evaluate immediate
routing, train after reinit, evaluate trajectories and spectral diagnostics.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `allpos_centered` at warmup 0/10/40 | H1 | unformed representation vs wrong population | Tests all-position delayed clustering | feature NMI, margin | approaches route | remains weak | high slot NMI | `condition_aggregate_reinit.csv` |
| `route_centered` at warmup 0/10/40 | positive control | route-relevant geometry | Shows hidden feature geometry exists | feature NMI, margin | high | fails | data invalid | `condition_aggregate_reinit.csv` |
| `oracle_centered` at warmup 0/10/40 | upper bound | label-known center | Validates reachability | feature NMI, margin | high | fails | data/model invalid | `condition_aggregate_final.csv` |
| `expert_svd` at warmup 0/10/40 | H2/H3 | raw expert spectral source | Tests naive SVD init | feature NMI, diagnostics | improves | weak | target fails | `spectral_diagnostics.csv` |
| `expert_svd_decommon` | H2 | common alignment | Tests whether removing common helps | feature NMI, common alignment | improves | weak | bad common estimate | `spectral_diagnostics.csv` |
| `expert_svd_orth` | H2 | row similarity | Tests whether orthogonalization helps | feature NMI, pairwise cosine | improves | weak | numerical failure | `spectral_diagnostics.csv` |
| `no_reinit` at warmup 10/40 | guard | warmup alone | Checks whether gains come from reinit | feature NMI | lower than good reinit | matches all | target fails | `training_trajectory.csv` |

Seeds: 0--7. Slot lengths: 1, 2, 4, 8. Warmup: 0, 10, 40. Post-reinit checkpoints: 0, 10, 40, 80, 160.

## 7. Primary Metric

Feature NMI is the primary metric because the current question is uniform
feature-to-expert assignment. The main false positive is promoting a spectral
or all-position source that improves load or target accuracy without actually
separating features.

## 8. Secondary Metrics

Matched preserve fraction, margin mean, margin p05, sign-flip rate, max load,
effective experts, target accuracy, loss, slot-start NMI, row pairwise cosine,
common alignment, feature-center alignment, and current-router alignment.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: route-position and oracle centered rows should score high.

Known bad: no-reinit random routing should not be treated as a successful
feature router even if target accuracy rises.

Known confusing: expert SVD may improve load or target loss while remaining
feature-unaware.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Data audit | Is the dataset uniform and slot-balanced? | feature and slot counts | pass if balanced | `data_audit.csv` | detailed |
| Warmup audit | Did warmup train without target failure? | loss/accuracy | pass if target learns enough | warmup rows | detailed |
| Reinit audit | Which geometry gives immediate feature routing? | reinit table | compare against route/oracle | `reinit_metrics.csv` | summary |
| Training audit | Does routing survive post-reinit training? | trajectories | final NMI/margin | trajectory figures | summary |
| Spectral audit | Why does expert SVD fail or pass? | cosine diagnostics | row similarity/common/feature alignment | `spectral_diagnostics.csv` | detailed |

## 11. Algorithm Specification, If Nontrivial

input: seed, slot length, warmup step, method list, train steps, and checkpoint list.

parameters: full run uses eight seeds, four slot lengths, warmup steps 0/10/40,
hidden size 64, four experts, and 160 post-reinit training steps.

intermediate variables: warmup model state, all-position hidden states,
route-position hidden states, centers, expert top singular vectors, router rows,
assignments, margins, and diagnostics.

steps:

1. Generate balanced calibration and evaluation data.
2. Warm up one base model for 0/10/40 steps.
3. Extract hidden states and expert top singular directions.
4. Build router rows for each method.
5. Reset only the router rows on the warmed model.
6. Evaluate immediate routing.
7. Continue post-reinit training and evaluate checkpoints.
8. Aggregate tables and figures.

outputs: CSV tables, PNG figures, JSON summary, and local log.

pass conditions: route/oracle controls pass; one warmup all-position or spectral
source closes the gap without slot leakage.

fail conditions: all-position and SVD sources stay weak while route/oracle pass.

failure reasons: unformed representation not enough, wrong hidden pool,
feature-unaware expert spectrum, row similarity, common alignment, or shortcut.

## 12. Success / Failure / Insufficient Evidence

Success for warmup method candidacy: warmup all-position or warmup expert SVD
approaches route-position feature NMI, has positive margin p05, low slot-start
NMI, and no target failure.

Failure: warmup all-position and expert SVD remain far below route-position and
oracle controls.

Insufficient: controls fail, slot-start NMI is high, target accuracy fails, or
the run misses full seed/slot coverage.

## 13. What This Cannot Claim

This cannot claim real-DCLM transfer, semantic expert specialization, expert
utility, a deployable MPI router, or impossibility of spectral routing.

## 14. Review Notes And Protocol Changes

This protocol intentionally uses the uniform no-position slot dataset, not the
A06_02_02_E03 common/rare skewed dataset, because the meeting question is uniform
feature distribution.
