# A06: Label-Free Route-Relevant State Selection

Document status: compressed draft anchor for review. This is not an approved
protocol.

## 0. researcher judgment record

**Phenomenon:** A06_17 shows a sharp mismatch: route-position hidden states
recover the feature partition perfectly, but all-position clustering often
merges whole features.

**Mechanism guess:** The failed object is the clustering population. All-position
k-means mixes route-relevant states with non-route, neutral, or role-specific
states, so centers are spent on the wrong geometry.

**Key variables:** hidden-state pool, label-free route-state selector, selected
pool purity, cluster centers, held-out route-position assignment.

**Causal relation:** If the selector keeps route-relevant states and rejects
non-route states, clustering the selected pool should recover the held-out
route-position feature partition better than all-position clustering.

**Observable metric:** held-out route-position `feature_NMI`. Load, active
experts, nuisance NMI, and a gated real-DCLM compatibility read are guards, not
the main claim.

**Alternative explanation:** Route feature geometry may be absent, or the
selector may simply encode slot position, nuisance, or a handcrafted route mask.

**Decision:** Pursue real proxy extraction only if a label-free selector beats
all-position clustering and approaches the route-only positive control. After
that controlled pass, run a small real-DCLM compatibility read before promoting
the next anchor. Revise if the gain is only load/visualization. Park if it
cannot beat cheap selector baselines.

## 1. Problem Definition

**Parent problem:** A06 asks whether hidden-state geometry can support
label-free proxy-level gate initialization.

**Sharper subproblem:** Before real-DCLM proxy extraction, decide whether we can
identify which controlled hidden states should be clustered for routing.

**Decision question:** Can a label-free selector choose a hidden-state pool whose
cluster centers recover the held-out route-position feature partition better
than all-position clustering?

**Not in scope:** real-DCLM semantics, SAE as a method claim, training
preservation, expert utility, or scaling. The real-DCLM touchpoint is a
compatibility guard, not a primary method claim.

## 2. Physical Prior

**P1: Route-relevant geometry is population-dependent.**  
The route position can contain clean feature geometry even when all hidden
states do not share one clusterable feature geometry. This prior is wrong if
all candidate pools fail in the same way despite a strong route-only control.

**P2: A selector must improve the routed readout, not just cluster appearance.**  
A good selector is defined by held-out route-position `feature_NMI`, not by
silhouette, sparse-looking features, or balanced load.

## 3. Falsifiable Hypothesis

**H1: Sample-pool mismatch is the active bottleneck.**  
Supported if a label-free selected pool gives higher held-out route-position
`feature_NMI` than all-position clustering and is close to the route-only
positive control. Weakened if the selected pool matches all-position failure or
only improves nuisance/load metrics.

## 4. Mathematical Model

**Objects:** $A$ is the all-position hidden-state pool, $R$ is the unknown
route-relevant pool, $N$ is non-route states, $s(h_i)$ is the label-free
selector, and $\hat R$ is the selected pool.

**Core model:** Hidden states are split into route-relevant and non-route
populations:

$$
A = R \cup N,\qquad h_i \in A.
$$

The selector proposes:

$$
\hat R=\{h_i:s(h_i)=1\}.
$$

**Mechanism relation:** Clustering succeeds only if $\hat R$ preserves the
feature residual used at the route position:

$$
\operatorname{Cluster}(\hat R) \rightarrow
\text{high held-out route-position feature_NMI}.
$$

**Observable metric:** held-out route-position `feature_NMI`, with max load,
active experts, and nuisance NMI as guards.

**Falsifier:** no label-free selector improves held-out route-position
`feature_NMI` over all-position clustering while the route-only positive
control remains high.

## 5. Computational Realization

**Input objects:** A06_17 controlled bridge hidden states and route-position
held-out labels; optional A06_10/A06_11-style real-DCLM hidden states for a
gated compatibility read.

**Computed variables:** selected pool $\hat R$, cluster centers, held-out
route-position assignments, `feature_NMI`, load, and nuisance NMI.

**Algorithm stages:** fit centers on candidate pools without feature labels;
evaluate every center set on held-out route-position states; use labels only
for evaluation and failure interpretation.

**Stage-local evidence:** selected-pool composition, route-feature heatmap,
load/nuisance guard table, and optional real-DCLM stability/readout table.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`,
`tables/selector_comparison.csv`, optional
`tables/real_dclm_compatibility.csv`, and one route-feature heatmap.

## 6. Minimal Falsification Test

| Test | Comparison | Primary metric | Pass / fail / insufficient | Failure means |
|---|---|---|---|---|
| Controlled selector audit | all-position baseline, route-only positive control, cheap label-free selector, optional SAE/code selector | held-out route-position `feature_NMI` | Pass if selector beats all-position and approaches route-only; fail if it matches all-position or improves only load/visualization; insufficient if route labels or held-out route states are missing | selector operationalization failed; not proof that feature geometry is absent |
| Gated real-DCLM touchpoint | selected real-DCLM pool/readout vs raw all-position or prior proxy-center baseline | split stability, nuisance guards, optional step-0 `proxy_route_NMI` | Compatible if the selected readout is stable above nuisance controls and does not collapse at step 0; incompatible if it is unstable or nuisance-driven; insufficient if metadata/proxy labels are missing | controlled selector may not transfer, or the real-DCLM state object is still misdefined |

Guards: active experts, max load, nuisance/slot-position NMI, a small
cluster-composition table, and the real-DCLM touchpoint only after the
controlled selector passes.

## 7. Current Evidence

**Observation:** A06_17 found route-only and slot offset 3 clustering reach
`feature_NMI=1.0` across 8/8 seeds, while all-position has mean 0.797 and only
1/8 perfect seeds.

**Observation:** A06_10/A06_11 show real-DCLM proxy clusters can be read out
and converted to step-0 router rows, while A06_12 shows ordinary early training
does not preserve that partition.

**Interpretation:** feature geometry exists at the route position. The next
uncertainty is whether the route-relevant state pool can be selected without
feature labels and whether the selected object is compatible with the existing
real-DCLM proxy surface.

**Boundary:** this evidence is controlled-bridge evidence. It does not prove
real-DCLM semantic proxy extraction or preservation.

**Evidence links:**

- `Projects/from-attention-to-search/main/experiments/A06/A06_17_all_position_route_relevant_feature_discovery/summary.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_17_all_position_route_relevant_feature_discovery/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_10_real_dclm_proxy_feature_operationalization/summary.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_11_real_dclm_proxy_center_router_initialization/summary.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md`

## 8. Claim Boundary And Next Decision

**Can claim if passed:** a label-free selector can identify a better clustering
population than all-position hidden states on the controlled A06 bridge. If the
gated real-DCLM touchpoint is compatible, the selected object is worth testing
as a real proxy extraction / initialization surface.

**Cannot claim:** real-DCLM semantic proxies, training preservation, utility, or
that SAE is needed.

**Next decision:** If the controlled selector passes and the real-DCLM
touchpoint is compatible, write a separate real-DCLM proxy extraction / step-0
initialization anchor. If the selector fails, revise the selector definition.
If the controlled selector passes but the real-DCLM touchpoint fails, revise
the real-DCLM state object before returning to preservation.
