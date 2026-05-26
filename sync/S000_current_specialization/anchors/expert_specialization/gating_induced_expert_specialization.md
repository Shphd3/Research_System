---
parent_node: rq.specialization
---

# Gating-Induced Expert Specialization

## 1. Problem Definition

1. broader question
   $$\downarrow$$
2. sharper question

Broader question:

```text
How can MoE gating make experts form stable, interpretable, reusable
feature-level specialization?
```

Sharper question:

```text
When token identity, slot/context feature, target behavior, and frequency can
disagree, can the gate assign tokens to experts according to the feature whose
expert has causal utility for the prediction?
```

This anchor belongs to the expert-specialization mainline. Reverse KV retrieval
is outside the current success criterion; it is a downstream effect to revisit
only after feature-level expert specialization is established.

## 2. Physical Priors

- Feature
  - A feature is a reusable downstream-behavior structure, not merely a token
    id.
  - It should remain meaningful when the same token appears in different
    slots or contexts.
  - It can be refuted if token identity explains routing and utility better
    than the proposed feature.
  - It should guide both the mathematical object and the synthetic data
    construction.

- Expert specialization
  - Specialization requires both assignment and causal utility.
  - A route is not specialized just because its normalized mutual information
    with a label is high.
  - An expert is specialized only if ablating it harms the corresponding
    feature behavior more than rival feature behaviors.
  - This can be refuted if assignment aligns with a feature label but expert
    utility does not.

- Gating factor visibility
  - The gate can only route by factors visible or learnable from its input.
  - Residual state, key/query/value projections, and head-level slices may
    expose different factors.
  - This can be refuted if changing the visible factor does not change route
    assignment or expert utility.

- Shortcut pressure
  - Token identity, target token, and frequency are easier shortcuts than
    feature-level structure.
  - A valid test must make these shortcuts compete with the intended feature.
  - This can be refuted if no shortcut dominates even in a deliberately
    conflicting setup.

## 3. Mechanistic Motivation

MoE training couples three objects that are often conflated:

```text
route assignment
expert computation
next-token loss
```

The gate may learn a stable partition that lowers loss without matching the
researcher's intended feature. For example, it may route by token id or target
token because those factors are easier and more immediately predictive than
slot/context feature.

Therefore, the key mechanism is not "make routing look semantic." The key
mechanism is:

```text
the assigned expert should be the expert whose computation has causal utility
for the same feature that defines the route.
```

This is why the anchor must measure assignment and expert utility together.

## 4. Mathematical Modeling

physical prior -> objects -> variables -> mapping/operator -> observable metric

Objects:

```text
token position
latent feature
router input
route assignment
expert output
feature-conditioned loss
```

Variables:

$$
z_t = (z_t^{token}, z_t^{slot}, z_t^{context}, z_t^{target}, z_t^{freq})
$$

where $z_t^{feature}$ is the intended slot/context or downstream-behavior
feature.

Router input:

$$
g_t = \phi(h_t)
$$

where $\phi$ is the chosen gate-visible representation.

Route assignment:

$$
r_t = G_\theta(g_t), \qquad e_t = \arg\max_e r_{t,e}
$$

Expert utility for feature class $c$:

$$
\Delta CE(c,e) =
CE(c; \operatorname{ablate}(e)) - CE(c; \operatorname{full})
$$

Utility-best expert:

$$
e_c^\* = \arg\max_e \Delta CE(c,e)
$$

Observable metric:

$$
A_{\mathrm{assign\text{-}utility}}
= P(e_t = e_{z_t^{feature}}^\* \mid z_t^{feature})
$$

Primary judgment:

```text
assignment-utility agreement
```

Supporting diagnostics:

```text
I(e_t; z_t^{feature})
I(e_t; z_t^{token})
I(e_t; z_t^{target})
I(e_t; z_t^{freq})
```

The intended result is not simply high feature alignment. The intended result
is that the assigned expert is also the expert with causal utility for that
feature.

## 5. Computational Realization

### 5.1 Workflow Interface

If the hypothesis holds, then the system should look like:

```text
input token sequence with controlled conflicting factors
-> model produces hidden states
-> gate observes a chosen representation phi(h)
-> router assigns each token to an expert
-> experts produce prediction behavior
-> ablation measures which expert causally supports which feature
-> assignment-utility agreement decides whether specialization exists
```

Input:

```text
synthetic sequences where the same token can appear in different
slot/context roles, and different tokens can share the same feature role
```

Computation:

```text
train a small top-1 MoE under matched budget, then record route assignment and
feature-conditioned expert ablation utility
```

Output:

```text
one table comparing assignment alignment, shortcut alignment, and
assignment-utility agreement across seeds
```

### 5.2 Minimal Computational Test

Use the smallest controlled reused-token setup where task factors are known and
expert causal utility can be measured.

Required factors:

```text
token id
slot/context feature
target token
token frequency
selected expert
feature-conditioned ablation utility
```

Required contrast:

```text
same token, different feature
different token, same feature
```

The test should not begin as a broad architecture sweep. It should first answer
whether the current or simplest gating condition routes by feature utility or
by shortcuts.

## 6. Minimal Falsifiable Test

mathematical object -> implementation object -> metric

Mathematical object:

```text
feature-conditioned assignment-utility agreement
```

Implementation object:

```text
reused-token synthetic MoE diagnostic with expert ablation by feature class
```

Metric:

```text
assignment-utility agreement
```

Decision rule:

```text
The hypothesis is supported only if route assignment aligns with the
feature-utility-best expert more strongly than with token id, target token, or
frequency shortcuts, and the pattern is stable across seeds.
```

## 7. Falsifiable Outcomes

Supported if:

- same-feature examples route to the same utility-best expert even when token
  identity differs;
- same-token examples route differently when their slot/context feature and
  utility-best expert differ;
- feature-conditioned expert ablation shows that the assigned expert causally
  supports that feature;
- the result is stable across seeds under the minimal setup.

Weakened if:

- route assignment aligns with token id, target token, or frequency more than
  with feature;
- route assignment aligns with feature but ablation utility does not;
- expert utility exists but the learned gate does not assign tokens to the
  utility-best expert;
- the pattern appears only in one seed or only under labels unavailable to the
  model at inference time.

Still not proven:

- the mechanism transfers to real corpora;
- the expert buckets can serve reverse KV retrieval;
- the same behavior holds at large model scale;
- a particular architecture is generally better than alternatives.

## 8. Current Evidence

Current evidence is mainly negative or boundary-setting.

What it supports:

- baseline top-1 MoE can learn the task without stable feature-level functional
  specialization;
- semantic or context initialization can create early semantic routing, but
  the route can decay during training;
- recoverable semantic boundaries in hidden states are not sufficient for
  functional expert specialization;
- Zipfian frequency changes load structure, but current evidence does not show
  that frequency alone explains tail specialization failure;
- minimal hierarchy can increase routing association diagnostics without
  improving functional specialization.

What it does not support yet:

- a gating mechanism that reliably induces expert specialization;
- a positive assignment-utility agreement result;
- transfer to real-data features;
- reverse KV retrieval utility.

Evidence document links:

- H0526 top-1 sparse router failure mode:
  `../experiments/H0521_router_feature_specialization/H0526_top1_sparse_router_failure_mode/summary.md`
  and
  `../experiments/H0521_router_feature_specialization/H0526_top1_sparse_router_failure_mode/detailed.md`.
- H0528a router prior decay:
  `../experiments/H0521_router_feature_specialization/H0528a_router_prior_decay_audit/summary.md`
  and
  `../experiments/H0521_router_feature_specialization/H0528a_router_prior_decay_audit/detailed.md`.
- H0528a route swap and frozen semantic router:
  `../experiments/H0521_router_feature_specialization/H0528a_route_swap_and_frozen_semantic_router/summary.md`
  and
  `../experiments/H0521_router_feature_specialization/H0528a_route_swap_and_frozen_semantic_router/detailed.md`.
- H0528a semantic refresh continuation:
  `../experiments/H0521_router_feature_specialization/H0528a_semantic_router_refresh_continuation/summary.md`
  and
  `../experiments/H0521_router_feature_specialization/H0528a_semantic_router_refresh_continuation/detailed.md`.
- H0529a Zipfian frequency shortcut:
  `../experiments/H0529a_zipfian_frequency_shortcut/summary.md`
  and `../experiments/H0529a_zipfian_frequency_shortcut/detailed.md`.
- H0530a hierarchical common/sense MoE:
  `../experiments/H0530a_hierarchical_common_sense_moe/summary.md`
  and `../experiments/H0530a_hierarchical_common_sense_moe/detailed.md`.

## 9. Claim Boundary And Next Decision

Claim boundary:

```text
Current evidence weakens the naive claim that ordinary MoE gating naturally
forms feature-level expert specialization. It does not yet provide a positive
mechanism for inducing specialization.
```

Next decision:

```text
Design the reused-token diagnostic and use assignment-utility agreement as the
primary metric.
```

Next sync topic:

```text
Reused-token diagnostic for gating-induced expert specialization.
```
