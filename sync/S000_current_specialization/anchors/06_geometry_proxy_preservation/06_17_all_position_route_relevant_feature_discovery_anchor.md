---
anchor_id: A06_17_all_position_route_relevant_feature_discovery
parent_node: rq.feature_specialization.initialization_geometry
status: result_updated
created: 2026-06-23
canonical_language: en
---

# A06_17 All-Position Route-Relevant Feature Discovery Anchor

## 0. Thinking Card

**Phenomenon:** A06_16 showed that route-position discovery and preservation can
work in the corrected no-position bridge, but clustering all hidden states still
sometimes merges whole feature classes.

**Mechanism guess:** The failure is a sample-pool mismatch. All-position
clustering mixes route-relevant states with non-route, neutral, and slot-role
states, so centers are not optimized for the route readout.

**Key variables:** fit pool, route-position held-out states, slot role,
non-route states, cluster centers, held-out route-position `feature_NMI`.

**Causal relation:** If the fit pool is the problem, route-only or route-like
pools should recover the feature partition, while all-position or mixed-role
pools should merge features even when route geometry is clean.

**Observable metric:** held-out route-position `feature_NMI`.

**Alternative explanation:** The route feature geometry itself may be weak, or
merged features may simply be nearest neighbors in route-hidden space.

**Decision:** Supported. Build a label-free route-relevant state selector before
returning to real proxy initialization.

**Addendum question:** For all-position failure seeds, can training-time common
subtraction rescue the failed all-position initialization into a
feature-specialized route partition?

## 1. Problem Definition

**Parent problem:** real-data proxy initialization needs a way to choose which
hidden states should define routing without knowing feature labels.

**Sharper subproblem:** A06_17 decides whether all-position clustering fails
because it fits the wrong hidden-state population.

**Decision question:** Is C4 all-position failure caused by clustering the wrong
hidden-state population rather than by missing route-position feature geometry?

**Not in scope:** real-DCLM semantic feature discovery, RoPE behavior,
whole-slot compositional routing, anti-collapse training, or a deployable
selector.

## 2. Physical Priors

**P1: Route-relevant states can contain clean feature centers.**  
If the route position is the true routing readout, route-only clustering should
recover feature classes.

**P2: Non-route states can distort all-position clustering.**  
All-position k-means sees many states that do not need to define the route
partition; these states can consume center capacity or introduce role geometry.

## 3. Falsifiable Hypotheses

**H1: All-position failure is sample-pool mismatch.**  
Supported: route-only and slot offset 3 pass perfectly, while all-position
fails in 7/8 strict seeds and often uses too few experts.  
Weakened if: every candidate pool had failed despite a strong route-only upper
bound.

**H2: Route feature geometry weakness is not the main cause.**  
Supported: oracle route and route-only pseudo are perfect, and merged feature
pairs are not consistently the nearest route centroids.

**H3: Common bias is not sufficient to explain all-position failure.**  
Supported if: fixed or dynamic common subtraction improves load but does not
turn failed all-position initialization into high route-position `feature_NMI`.
Weakened if: dynamic common subtraction converts failed all-position seeds into
stable feature-specialized routing during training.

## 4. Mathematical Model

**Objects:** $R$ is the route-position pool, $A$ is the all-position pool,
$S_j$ is slot-role pool $j$, and $N$ is non-route states.

**Core model:**

$$
A = R \cup S_0 \cup S_1 \cup S_2 \cup N.
$$

**Mechanism relation:**

$$
\operatorname{Cluster}(R)\rightarrow \text{route feature partition},
\qquad
\operatorname{Cluster}(A)\not\Rightarrow \text{route feature partition}.
$$

**Observable metric:** held-out route-position `feature_NMI`, with feature-merge
heatmaps and merged-pair distance ranks as guards.

**Falsifier:** no candidate pool improves over all-position while oracle and
route-only route-position clustering remain high.

## 5. Computational Realization

**Input objects:** A06_16 no-position C4 controlled data and hidden states.

**Computed variables:** centers fit on route-only, slot-offset, all-position,
role-balanced, and non-slot pools; held-out route-position assignments;
feature-merge diagnostics.

**Algorithm stages:** fit centers without feature labels; evaluate every center
set on held-out route-position states; use labels only for post-fit audit.

**Stage-local evidence:** route `feature_NMI`, active experts, feature-to-expert
heatmap, cluster role composition, and merged-pair distance ranks.

**Expected artifacts:** `summary.md`, `detailed.md`,
`tables/pool_comparison_aggregate.csv`, and `tables/merge_audit.csv`.

## 6. Minimal Falsification Test

| Test | Comparison | Primary metric | Pass / fail / insufficient | Failure means |
|---|---|---|---|---|
| Pool mismatch audit | route-only positive control, slot-offset pools, all-position baseline, role-balanced all-position, non-slot negative control | held-out route-position `feature_NMI` | Pass if route-like pools recover features while all-position merges; fail if all pools merge despite route-only upper bound; insufficient if held-out route states or feature labels are missing | either sample-pool mismatch is supported, or the failure returns to route geometry / position encoding |

## 7. Current Evidence

**Observation:** A06_17 full run `pt-9mt77o49` found oracle route, route-only
pseudo, and slot offset 3 all reach `feature_NMI=1.0` across 8/8 seeds.
All-position has mean `feature_NMI=0.797`, minimum 0.637, and only 1/8 perfect
seeds. Role-balanced all-position also has only 1/8 perfect seeds.

**Interpretation:** route-position feature geometry exists and is discoverable
without labels when the correct state pool is known. The failure comes from
clustering the wrong population.

**Boundary:** count imbalance matters, but role-geometry mixing also matters;
route-like selection is stricter than simple balancing.

**Addendum intervention to run:** take the lowest all-position failure seeds
(`20260623`, `20260625`, `20260626`), initialize the router from all-position
residual k-means, then train with raw router input, fixed step-0 all-position
common subtraction, or batch-dynamic all-position common subtraction. Primary
metric remains held-out route-position `feature_NMI`; load is only a guard.

**Addendum result:** completed. All three failed seeds remain at
`feature_NMI=0.6369`, max load `0.75`, and two active route experts through
step 800 under raw, fixed-common, and dynamic-common training. Target accuracy
reaches `1.0`, so the model learns the task while preserving the merged route
partition. Training-time common subtraction does not rescue the failed
all-position basin.

**Evidence links:**

- `../../experiments/A06/A06_16_synthetic_to_realistic_proxy_bridge/summary.md`
- `../../experiments/A06/A06_16_synthetic_to_realistic_proxy_bridge/detailed.md`
- `../../experiments/A06/A06_17_all_position_route_relevant_feature_discovery/summary.md`
- `../../experiments/A06/A06_17_all_position_route_relevant_feature_discovery/detailed.md`
- `../../experiments/A06/A06_17_all_position_route_relevant_feature_discovery/tables/pool_comparison_aggregate.csv`
- `../../experiments/A06/A06_17_all_position_route_relevant_feature_discovery/addendum_common_subtraction_rescue/summary.md`

## 8. Claim Boundary And Next Decision

**Can claim:** in the controlled no-position bridge, all-position hidden-state
clustering is not a reliable proxy population for route-relevant feature
initialization.

**Cannot claim:** real-language semantic features, RoPE behavior, whole-slot
compositional routing, or a final DCLM initialization method.

**Next decision:** construct a label-free route-relevant state selector before
returning to real feature initialization.

**Addendum decision rule:** if dynamic common subtraction rescues the failed
seeds, common bias becomes an active intervention target. If it only improves
load or does not improve `feature_NMI`, keep the main conclusion: the fit
population is wrong, and route-relevant state selection is still the next step.

**Addendum decision:** dynamic common subtraction did not rescue feature NMI or
load. Keep route-relevant state selection as the next step.
