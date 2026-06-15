# Literature Integration: MoE Routing Geometry

Date: 2026-06-15

Purpose: integrate two 2026 MoE routing-geometry papers into the Project 2 presentation and our current common-logit / gating-initialization research framing.

## Reading Card 1

Paper title:
Routers Learn the Geometry of Their Experts: Geometric Coupling in Sparse Mixture-of-Experts

Source:
https://arxiv.org/abs/2605.12476

Why I read it:
It directly addresses whether routers are external assignment modules or whether they co-evolve geometrically with the experts they select.

Core question:
How are routing decisions formed mechanistically in sparse MoE training?

Authors' method:
The paper derives a gradient-level coupling: for a routed token, the selected expert's router weight vector and the expert's input-side weights receive updates along the same hidden-state direction, up to scalar coefficients. It then tests whether router scores predict selected-expert activations, analyzes auxiliary load balancing, and builds an online K-Means centroid router as a constructive test.

Key result:
Matched router-expert pairs accumulate a shared routed-token history. Router scores are reflected in expert activations. Auxiliary load-balancing gradients can weaken this expert-specific geometry by spreading input-directed gradients across router rows. A centroid-style router recovers a substantial part of learned routing behavior.

Authors' interpretation:
Effective routing is partly a geometric coupling between router directions and expert input geometry. Future routers should preserve useful router-expert geometry instead of only enforcing utilization.

My judgment:
This is highly relevant to our current next-mechanism direction. It supports treating routing as a geometry-preserving construction rather than a pure load-balancing problem. However, it does not by itself prove functional domain specialization, and its K-Means router is a constructive test rather than a final deployment method.

Relation to our research:
Our A06_02 results show that gate-only updates are insufficient to explain the step-10 common-margin spike; hidden-producing path and gate-hidden interaction matter. This paper provides an external theoretical reason: router and expert geometry are coupled through selected-token histories. Our common-filtered expert-spectrum initialization should therefore be framed as preserving useful router-expert coupling after removing shared/common directions.

Need to read deeply later:
Yes. Especially the gradient derivation, auxiliary-loss effect, and centroid-router design.

Mainline update check:

- Hypothesis: strengthen the idea that routing initialization should respect expert geometry, not just hidden-state clusters.
- Modeling: add router-expert coupling as a second geometric channel beside common-logit bias.
- Experiment: add a future diagnostic measuring router-expert alignment or centroid agreement under random, common-filtered, and spectrum-based initialization.
- Interpretation: common-aware routing should not erase all common structure blindly; it should prevent common directions from dominating top-1 while preserving useful residual coupling.
- Next decision: compare common-filtered expert-spectrum initialization with centroid-style residual routing or router-expert alignment metrics.

## Reading Card 2

Paper title:
The Myth of Expert Specialization in MoEs: Why Routing Reflects Geometry, Not Necessarily Domain Expertise

Source:
https://arxiv.org/abs/2604.09780

Why I read it:
It directly challenges the assumption that observed MoE expert usage patterns imply interpretable domain expertise.

Core question:
What produces apparent expert specialization, and how interpretable are the resulting expert activation patterns?

Authors' method:
The paper uses the fact that MoE routers are linear maps from hidden states to expert logits. It proves and empirically checks that hidden-state similarity is enough to explain expert-usage similarity across pretrained MoEs. It also analyzes the role of load-balancing loss in suppressing shared hidden directions.

Key result:
Expert usage similarity largely follows hidden-state geometry. Load balancing can suppress shared directions to preserve routing diversity. But expert specialization patterns are often hard to interpret: similar tasks across models do not necessarily use the same experts, prompt-level routing may not predict rollout routing, and deeper layers can show similar activations across semantically unrelated inputs.

Authors' interpretation:
MoE specialization should be understood as a property of representation geometry, not as standalone evidence of human-interpretable domain expertise.

My judgment:
This is a strong claim-boundary paper for us. It supports our decision not to claim "domain expertise" or "functional expert specialization" from routing heatmaps, NMI, or load balance alone. It also supports our focus on hidden-state decomposition, common directions, residual directions, and early-training geometry.

Relation to our research:
Our current story is aligned with this paper: route consistency and slot heatmaps are not enough; we need causal interventions and mechanism metrics. The paper reframes our common-logit result as a concrete case of hidden-state geometry controlling router output. It also suggests that our target should be "feature/residual-aligned routing under controlled definitions", not broad "semantic expert specialization".

Need to read deeply later:
Yes. Especially the load-balancing/shared-direction argument and metrics for hidden-state geometry vs expert usage.

Mainline update check:

- Hypothesis: route specialization claims must be weakened unless functional utility is tested.
- Modeling: keep $h=c+r$ as the central decomposition, but state that $r$ is an operational residual feature, not necessarily semantic domain.
- Experiment: use hidden-state geometry metrics together with routing metrics; do not treat domain labels as sufficient ground truth.
- Interpretation: our contribution is a mechanism audit of routing geometry, not a proof that experts learn interpretable domains.
- Next decision: add claim-boundary language to slides and later paper intro.

## Integrated Research Position

The two papers should change our front-stage framing from:

```text
Why does MoE fail to form expert specialization?
```

to:

```text
Which hidden-state geometry does the router amplify, and how can initialization make routing follow residual feature geometry instead of common directions?
```

This supports the current Project 2 story:

1. Apparent expert specialization is a geometry question, not automatically a semantic or domain-expertise question.
2. Our common-logit model identifies one harmful geometry: a shared direction $c$ becomes expert-specific bias $w_e^T c$.
3. Our early-training results show that this geometry is not static; hidden-state drift and gate-hidden interaction amplify it.
4. The next method should be common-filtered and expert-geometry-aware: remove or isolate common directions, then preserve useful router-expert coupling on residual structure.

## Slide-Level Integration

- Slide 02: add literature framing: recent work argues router usage reflects hidden-state geometry.
- Slide 03: sharpen thesis: the project audits which geometry is amplified before useful specialization can form.
- Slide 06: cite "The Myth" as support for the linear-router geometry view.
- Slide 11: cite "Routers Learn" as support for selected-path router-expert coupling.
- Slide 12: state next mechanism as "common-filtered, coupling-preserving initialization", not merely load balance.

## Claim Boundary

Do not claim:

- routing patterns equal human-interpretable domain expertise;
- common-filtered routing solves expert specialization;
- load balancing is wrong or unnecessary;
- router-expert coupling alone explains all early route concentration;
- our current DCLM results transfer to pretrained large-scale MoEs.

Can claim:

- recent literature supports a geometry-first view of MoE routing;
- our experiments identify a specific geometry failure mode: common directions become expert-specific top-1 bias and are amplified early;
- this motivates initialization and routing mechanisms that handle common directions while preserving useful router-expert geometric coupling.
