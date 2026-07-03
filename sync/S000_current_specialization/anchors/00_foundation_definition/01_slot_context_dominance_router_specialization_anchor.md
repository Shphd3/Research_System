---
parent_node: problem.moe_expert_specialization
---

# Slot-Context Signal And Operational Feature Audit

## 0. Thinking Card
我们的父问题不变：如何让 MoE gating 形成稳定、可解释、可复用的 feature-level expert specialization。

0603 组会和 A05_01_feature_key_routing_stability_center_only 之后，当前主线需要往前收一步：

> **在 route-utility binding 之前，先定义 operational feature，并检查 router 实际绑定的是 slot、$B_i$，还是原子组合 $(slot,B_i)$。**

当前认知：

- advisor 的 weak toy claim 可以接受：在一个 operational feature key 下，同一个 feature 可以稳定 route 到一个 expert；
- A05_01_feature_key_routing_stability_center_only 支持这个弱 claim：FeatureKeyConsistency 在各条件中都接近 0.99；
- 但 FeatureKeyConsistency 不能区分 specialization 和 collapse；
- center separation 在 A05_01_feature_key_routing_stability_center_only 中没有独立增益，因为 `S0 ~= S1` 且 `S0-cos ~= S1-cos`；
- cosine router + slot init 给出最好的非坍缩 slot-aligned routing，但这还不是 functional specialization。

当前路线：

```text
define feature-level expert specialization
-> answer the advisor's weak toy question: same-feature route consistency
-> audit operational feature identity: slot vs B_i vs (slot, B_i)
-> audit non-collapse and expert composition under the chosen feature definition
-> only then test route-utility binding
-> only then test Zipfian / real-corpus robustness
```

下一步：

在已有 A05_01_feature_key_routing_stability_center_only route logs/checkpoints 上做 feature key audit：

```text
feature labels: slot, B_i, slot+B_i
metrics: mean_f max_e P(route=e | feature=f), NMI(route; slot),
NMI(route; B_i), NMI(route; slot+B_i), load entropy / max load,
per-expert composition table
```

Meeting-facing phrasing:

> Last time I mixed two levels. Under the advisor's weak toy definition, same-feature consistency is basically true, and A05_01_feature_key_routing_stability_center_only supports it. But this metric does not distinguish specialization from collapse. Therefore I will not yet claim functional specialization. The next step is to audit what the router treats as the feature: slot, $B_i$, or slot+$B_i$.

## Question

Broader question:

```text
Why does ordinary top-1 MoE gating fail to produce stable, interpretable feature-level expert specialization?
```

Sharper question:

```text
Before route-utility binding, what operational feature does the router bind to:
slot, B_i, or the atomic pair (slot, B_i)?
```

This anchor is a diagnostic child of the specialization mainline. It first tested the weak-context explanation for prior routing failure. After A05_01_feature_key_routing_stability_center_only, its current role is earlier: define the operational feature axis and distinguish weak same-feature consistency from non-collapsed feature specialization.

It does not test real-corpus specialization, Zipfian robustness, KV-cache reverse indexing, or a new MoE architecture. It also does not yet test route-utility binding; that is downstream of feature-axis audit.

## 2. Physical Priors
In language, the same surface token can require different continuations in different contexts. Therefore the relevant feature is not token identity alone, but a context-dependent predictive state.

For a B token under slot $s$, the router input can be decomposed as:

$$
h_{i,s}^{(m)} = c_i + \beta_m u_s + \epsilon
$$

where $c_i$ is B-token identity, $u_s$ is slot/context information, and $\beta_m$ is the strength of that context at the B position.

A linear router can route by slot only if $u_s$ is visible in $h_{i,s}^{(m)}$ and useful for reducing NTP loss. But routing alignment alone is not specialization. A slot-specialized route must also select the expert that has causal utility for that slot.

## Hypothesis / Mechanism

Previous short-slot experiments showed:

```text
semantic / context initialization can create early routing alignment;
NTP training can wash that alignment out;
hidden states may still contain recoverable slot boundaries.
```

This leaves two rival explanations:

```text
A. slot signal at B was too weak, so B identity dominated routing;
B. slot is visible and useful, but top-1 NTP does not bind route assignment to expert utility.
```

The experiment separates them by first removing B-identity variation, then adding it back.

## 4. Mathematical Model
Use four slots and four experts:

$$
s\in\{0,1,2,3\}, \qquad e\in\{0,1,2,3\}.
$$

Each sample has:

$$
x_{i,s}=(C_s^{(m)}, B_i), \qquad y_{i,s}=\pi_s(B_i).
$$

For the same $B_i$, the four slots produce distinct targets. Thus $B_i$ alone cannot determine the next token; slot context must disambiguate prediction.

The top-1 selected-gate router is:

$$
p=\operatorname{softmax}(Wh_{i,s}), \qquad r_{i,s}=\arg\max_e p_e.
$$

Slot-conditioned expert utility is measured by ablation:

$$
\Delta CE(s,e)=CE_s(\operatorname{ablate}(e))-CE_s(\operatorname{full}).
$$

The core judgment is not one metric but the bundle:

```text
route-slot NMI / route heatmap / forced expert loss / assignment-utility agreement
```

A result supports functional specialization only if final route assignment is slot-aligned and the assigned expert is also utility-best for that slot.

After A05_01_feature_key_routing_stability_center_only, add a prior feature-axis audit before this utility judgment:

```text
feature labels: slot, B_i, slot+B_i
route consistency: mean_f max_e P(route=e | feature=f)
route-feature NMI: NMI(route; slot), NMI(route; B_i), NMI(route; slot+B_i)
collapse guard: load entropy / max load
composition: per-expert distribution over slot, B_i, and slot+B_i
```

## Minimal Computational Test

Two modes:

```text
single_b_sanity: one shared B token; tests whether slot context can control routing when B identity is removed.
multi_b_primary: 256 B identities; tests whether slot routing survives B-identity variation.
```

Conditions:

```text
C0_short_slot_init: one-token slot cue baseline
A_long_repeated_slot_init: 5-token repeated slot cue
B_long_distributed_slot_init: 5-token distributed slot code
Oracle_slot_router / Oracle_b_position_only: slot-utility upper bound
A_long_random_init / B_long_random_init: natural-discovery controls
```

The repeated cue is the strongest context signal. The distributed code is cleaner because no single prefix token uniquely identifies the slot.

## Current Evidence

Supported weak result:

```text
Stronger context plus slot-centroid init can control routing in fixed-B diagnostics.
```

Evidence:

```text
single-B A_long_repeated: route NMI = 1.000, Assign-Utility = 1.000
single-B B_long_distributed: route NMI = 0.893, Assign-Utility = 1.000
bridge fixed-B long semantic: final NMI = 1.000 across seeds
```

Weakened strong result:

```text
slot visibility plus slot-centroid init is not sufficient for robust multi-B functional specialization.
```

Evidence:

```text
multi-B h_B -> slot probe = 1.000 and target accuracy = 1.000;
multi-B Oracle = 1.000, so slot-specific utility is available;
multi-B A_long_repeated improves but remains imperfect: route NMI 0.243 -> 0.591, Assign-Utility 0.565 -> 0.925;
multi-B B_long_distributed remains weak: route NMI 0.078 -> 0.313, Assign-Utility 0.326 -> 0.747.
```

Metric caveat:

```text
multi-B B_long_random_init reaches Assign-Utility = 0.998 while route NMI = 0.010.
```

Therefore Assign-Utility alone can be high under utility collapse. It must be read together with route-slot alignment and forced expert loss.

A05_01_feature_key_routing_stability_center_only feature-key diagnostic:

```text
Advisor weak toy claim accepted: under an operational feature key, the same
feature can be stably routed to one expert.
```

Evidence:

```text
FeatureKeyConsistency is near 0.99 across random init, slot init, and
center-separation-only conditions.
```

But this is a weak result:

```text
FeatureKeyConsistency alone does not distinguish specialization from collapse.
Single-expert or near-single-expert seeds can score near 1.0.
```

Mechanism update:

```text
Center separation shows no independent gain in A05_01_feature_key_routing_stability_center_only because S0 ~= S1 and
S0-cos ~= S1-cos. Cosine router + slot init gives the best non-collapsed
slot-aligned routing, but this does not establish functional specialization.
```

Mainline impact:

```text
The immediate uncertainty is no longer "how do we bind route to utility?"
The immediate uncertainty is "what is the feature that routing is already
binding to: slot, B_i, or atomic (slot, B_i)?"
```

## Claim Boundary

What can be claimed:

```text
Context strength matters. Long slot context and semantic centroid initialization make B-position routing more slot-aligned, especially when B identity is fixed.
Under a weak operational feature-key definition, same-feature route consistency is basically true in A05_01_feature_key_routing_stability_center_only.
```

What cannot be claimed:

```text
ordinary top-1 NTP naturally forms robust slot-functional experts;
init-final diagonal improvement alone proves specialization;
route heatmap diagonalization alone proves expert utility;
high FeatureKeyConsistency alone proves specialization;
center separation has independent feature-key benefit in A05_01_feature_key_routing_stability_center_only;
this transfers to Zipfian or real-corpus data.
```

The current failure is more specific than weak representation:

```text
slot information is visible and useful, but learned routing does not reliably bind the slot axis to utility-best experts under many B identities.
```

Additional 2x2 mechanism audit:

```text
In a minimal 2-feature / 2-expert NTP-style top-1 proxy, failed seeds are
already collapsed at step 0, not after late optimization drift.

Success seeds start with A/B split across experts and keep that split through
training while forming counterfactual CE advantage.

Removing router bias improves random-router initial split from 3/10 to 6/10,
but does not guarantee route-pattern separation.
```

Evidence:

```text
Projects/from-attention-to-search/main/experiments/A02/A02_top1_router_lockin_2x2/summary.md
Projects/from-attention-to-search/main/experiments/A02/A02_top1_router_lockin_2x2/detailed.md
Projects/from-attention-to-search/main/experiments/A02/A02_top1_router_lockin_2x2/report_card.md
```

## Next Decision

Do not move directly to route-utility binding.

```text
First define the operational feature and audit what the router already binds to:
slot, B_i, or atomic (slot, B_i).
```

Next immediate diagnostic:

```text
Use existing A05_01_feature_key_routing_stability_center_only route logs/checkpoints.

Feature labels:
1. slot;
2. B_i;
3. slot+B_i.

Metrics:
1. mean_f max_e P(route=e | feature=f);
2. NMI(route; slot);
3. NMI(route; B_i);
4. NMI(route; slot+B_i);
5. load entropy / max load;
6. per-expert composition table.
```

Decision logic:

```text
If route aligns mostly with slot:
  slot is a valid operational feature for the next stage.

If route aligns mostly with B_i:
  previous slot-specialization claim is too strong.

If route aligns mostly with slot+B_i:
  the actual routed feature is atomic predictive state, not slot alone.

If consistency is high but load entropy is low:
  this is weak lock-in / collapse, not specialization.

If non-collapsed slot or slot+B_i structure exists:
  then proceed to utility-binding diagnostic.

If frequency is later varied:
  do it only after the feature axis is fixed.
```

Route-utility binding remains the next major mechanism question, but only after the feature-composition audit decides what object the router is routing.
