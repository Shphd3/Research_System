# Protocol Card: A06_route_relevant_state_selector

Draft status: pending user / experiment-AI approval. Do not run before approval.

## 0. Approval Snapshot

**Approval status:** Draft / not approved.

**Purpose:** Test whether a label-free selector can choose the controlled
hidden-state pool that should be clustered for route initialization, then run a
small real-DCLM compatibility read if the controlled test passes.

**Primary anchor:** `A06_route_relevant_proxy_extraction_anchor.md`

**Anchor decision question:** Can a label-free selector choose a hidden-state
pool whose centers recover held-out route-position features better than
all-position clustering?

**Anchor physical prior tested:** Route-relevant geometry is
population-dependent.

**Anchor core model term tested:** selector $s(h)$ and selected pool $\hat R$.

**Anchor falsifier:** no selector beats all-position while the route-only
positive control remains high.

**Experiment role:** operationalization / proxy test.

**Primary metric from anchor:** held-out route-position `feature_NMI`.

**Claim boundary from anchor:** Passing supports controlled route-relevant state
selection. A compatible real-DCLM read only justifies the next real proxy
anchor; it does not prove preservation.

**Minimal setup:** Reuse A06_17 controlled bridge hidden states and labels;
optionally reuse A06_10/A06_11 real-DCLM hidden states after controlled pass.

**Basic configuration:** K=4 clustering, held-out route-position evaluation,
labels used only for evaluation, and no model training.

**Conditions to run:** all-position baseline, route-only positive control,
cheap label-free selector, optional SAE/code selector if already available,
and a gated real-DCLM compatibility read only after controlled pass.

**Pass:** a label-free selector improves over all-position and approaches the
route-only positive control under load/nuisance guards. The real-DCLM read is
compatible if it is stable above nuisance controls and non-collapsed at step 0.

**Fail:** selector matches all-position failure or improves only load /
visualization.

**Insufficient:** missing held-out route states, feature labels, nuisance
metadata, or real-DCLM proxy metadata for the gated read.

**Cannot claim:** real-DCLM semantics, training preservation, expert utility,
or that SAE is required.

**Approval decision:** approve exact selector list, whether SAE is included, and
whether the gated real-DCLM touchpoint is included in this run.

## 1. Anchor Alignment

**Decision question:** same as approval snapshot.

**Physical prior tested:** only the correct hidden-state population should
define route centers.

**Core model term tested:** $\hat R=\{h:s(h)=1\}$.

**Falsifier:** selected pool does not improve route readout over all-position.

**Claim boundary:** controlled selector validity only; real-DCLM compatibility
is a bridge to the next anchor, not this anchor's primary claim.

## 2. Tested Hypothesis

A label-free selector can pick a more route-relevant clustering pool than
all-position hidden states.

## 3. Rival Explanations

1. Route feature geometry is absent.
2. Selector encodes slot position or nuisance, not route relevance.
3. Improvement is only load balance or visualization.
4. SAE/code features add complexity without improving `feature_NMI`.

## 4. Data / Model / Algorithm / Objective

**Data:** A06_17 controlled no-position bridge hidden states with held-out
route-position feature labels. Optional gated input: A06_10/A06_11-style
real-DCLM hidden states and proxy metadata.

**Algorithm:** compute selector scores, choose candidate pool, fit K=4 centers,
evaluate centers on held-out route-position states. If the controlled selector
passes, apply the same selected-pool/readout idea to the real-DCLM proxy
surface as a compatibility read.

**Objective:** no model training; this is a clustering/selector audit.

## 5. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
|---|---|---|---|---|---|---|---|---|
| All-position baseline | all-position is the failed pool | sample-pool mismatch | anchors the known failure | primary baseline | below selector | matches selector | missing states | selector table |
| Route-only positive control | route geometry exists | absent-geometry rival | checks that the task is learnable | guard / upper bound | high `feature_NMI` | low `feature_NMI` | missing route labels | selector table |
| Cheap label-free selector | selector can recover route-relevant pool | $s(h)$ and $\hat R$ | primary operationalization | primary evidence | beats all-position, near route-only | all-position-like or only load gain | metadata missing | heatmap + selector table |
| Optional SAE/code selector | representation may help selection | complexity vs cheap selector | tests whether extra representation is needed | secondary evidence | beats cheap selector | no gain over cheap selector | unavailable implementation | selector table |
| Gated real-DCLM compatibility read | selected object should be worth real proxy follow-up | transfer from controlled to real-DCLM state object | prevents a controlled-only method claim | secondary bridge | stable above nuisance and non-collapsed at step 0 | unstable, nuisance-driven, or collapsed | missing proxy metadata | compatibility table |

Use the A06_17 seed set unless implementation constraints force a smoke subset.

## 6. Primary Metric

`feature_NMI` on held-out route-position states decides the test because the
selector is useful only if its centers recover the routed feature partition.

## 7. Secondary Metrics

Max load, active experts, nuisance/slot-position NMI, selected-pool
composition, real-DCLM split stability, and optional step-0 `proxy_route_NMI`.

## 8. Known Good / Known Bad / Known Confusing Cases

**Known good:** route-only pool.

**Known bad:** all-position pool from A06_17.

**Known confusing:** a selector that balances load but still merges whole
features; a selector that passes the controlled task but is nuisance-driven on
real-DCLM states.

## 9. Stage-Level Profiling Plan

| Stage | Local question | Debug artifact |
|---|---|---|
| Selector audit | which states are selected? | selected-pool composition |
| Cluster audit | do centers recover features? | feature-to-expert heatmap |
| Guard audit | is improvement a nuisance/load artifact? | load and nuisance table |
| Real-DCLM bridge | does the selected object stay stable off the toy surface? | compatibility table |

## 10. Algorithm Specification, If Nontrivial

**input:** controlled hidden states, position metadata, held-out route labels,
and optional real-DCLM hidden states / proxy metadata.

**parameters:** selector rule, K=4 centers, held-out split.

**steps:** score states; select pool; fit centers; assign held-out route states;
compute metrics and guards; if controlled pass holds, run the real-DCLM
compatibility read and report it separately from the primary metric.

**outputs:** selector comparison table, route-feature heatmap, and optional
real-DCLM compatibility table.

**failure reasons:** wrong selector, missing route geometry, nuisance shortcut,
or insufficient metadata.

## 11. Success / Failure / Insufficient Evidence

**Success:** selector beats all-position and is close to route-only. The
real-DCLM bridge is compatible if stable above nuisance controls and
non-collapsed at step 0.

**Failure:** selector does not improve the route readout.

**Insufficient:** required labels or metadata are missing, or the real-DCLM
bridge lacks proxy metadata.

## 12. What This Cannot Claim

This protocol cannot claim real-DCLM proxy validity, preservation, utility, or
SAE necessity. The real-DCLM bridge can only decide whether the next real proxy
anchor is worth writing.

## 13. Review Notes And Protocol Changes

After controlled pass plus compatible real-DCLM bridge, write a separate
real-DCLM proxy extraction / step-0 initialization anchor. If the bridge fails,
revise the real-DCLM state object before preservation work.
