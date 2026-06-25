---
anchor_id: 00_feature_level_expert_specialization_mainline
parent_node: rq.expert_specialization
status: active
updated: 2026-06-25
canonical_language: en
---

# Feature-Level Expert Specialization Mainline Anchor

## 0. Thinking Card

**Phenomenon:** 普通 top-1 MoE 不会自然形成稳定、可解释、可复用的 feature-level expert partition；即使 feature 均匀出现，也可能进入 expert underuse、feature merge 或训练早期覆盖。

**Mechanism guess:** hidden state 同时包含 common component、route-relevant feature residual 和非路由状态；随机门控或 all-position 聚类会对准错误对象，训练反馈会放大早期偏置。

**Key variables:** common component $c$、route-position feature residual $r_f$、非路由状态集合 $N$、gate row $w_e$、route distribution $q_{f,e}$、common/rare gradient conflict $\mathcal{C}_{C,R}$。

**Causal relation:** wrong geometric object or early feedback changes $q_{f,e}$, causing feature merge or route concentration; useful specialization further requires lower feature interference, not only balanced load.

**Observable metric:** route-position `feature_NMI`, `max_load`, step-5/10 proxy-route NMI, all-position vs route-position clustering gap, and routing-weighted common/rare gradient conflict.

**Alternative explanation:** feature geometry may be absent, the chosen proxy may not match semantic feature, or dense/shared training may solve rare features better than MoE.

**Decision:** pursue real-text early-preservation only if step-0 proxy partition can be kept through early training without loss regression; revise if preservation fails; park functional claims until preservation and utility evidence both pass.

## 1. Problem Definition

Parent problem:
Can gating make MoE experts form stable, interpretable, reusable feature-level specialization?

Sharper subproblem:
After A05/A06/A07, the main uncertainty is no longer whether a controlled feature partition can be constructed. The sharper question is whether the right route-relevant hidden-state population can be selected and preserved through early real-text training, and whether the preserved partition has functional value.

Decision question:
Can a real-text proxy partition that is linearly routable at step 0 be preserved through the step-5/10 training window while keeping language-model loss acceptable?

Not in scope:
This anchor does not claim real semantic experts, a deployable routing method, dense-beating MoE value, or reverse-KV retrieval benefit.

## 2. Physical Priors

P1:
Router inputs contain common and feature-specific components.
Meaning:
A hidden state can be decomposed into a shared component plus a feature residual; top-1 routing can amplify the shared part even when feature frequencies are uniform.
Could be wrong if:
Centering or common-channel audits do not change route concentration, or early-training concentration is explained by another stage.

P2:
Feature geometry is only useful if it is measured on route-relevant hidden states.
Meaning:
Route-position states can contain clean feature centers, while all-position clustering mixes route states with neutral, nuisance, and role states.
Could be wrong if:
Route-only and all-position clustering fail in the same way despite strong oracle separability.

P3:
Expert specialization must have functional value, not only route purity.
Meaning:
Balanced load or high route-feature NMI is a guard; the stronger claim requires lower feature interference or higher expert utility for the routed feature.
Could be wrong if:
Conflict metrics move without rare-loss or utility improvement, or dense/shared baselines remain stronger.

## 3. Falsifiable Hypotheses

H1:
Ordinary random or early-trained top-1 routing fails because the gate first sees a common or wrong-population geometric object.
Supported if:
A05 common-logit and A06 all-position audits show concentration or merge that improves when the object is centered or restricted to route-relevant states.
Weakened if:
Wrong-object corrections do not change load, route NMI, or merge patterns.

H2:
Route-position feature geometry is reachable but not automatically preserved in real training.
Supported if:
A06 route-position proxy centers produce step-0 routing and controlled preservation, while ordinary DCLM training destroys proxy-route NMI by step 5/10.
Weakened if:
Step-0 proxy routing is unstable or preservation fails even in controlled bridge runs.

H3:
Functional specialization requires reducing feature interference after preservation.
Supported if:
A07-style common/rare conflict reduction improves rare loss or expert utility under matched load and objective guards.
Weakened if:
Conflict reduction is small, noisy, or worse than dense/shared training.

## 4. Mathematical Model

Objects:

- $h_f$: hidden state used by the router for feature $f$.
- $c$: shared common component.
- $r_f$: route-relevant feature residual.
- $n$: non-route or nuisance state contribution.
- $w_e$: gate row for expert $e$.
- $q_{f,e}=P(E=e\mid F=f)$: route distribution.
- $g_{f,e}$: per-feature, per-expert gradient.

Core decomposition:
$$
h_f = c + r_f + n,\qquad z_{f,e}=w_e^\top h_f.
$$

Mechanism relation:
$$
z_{f,e}=w_e^\top c+w_e^\top r_f+w_e^\top n.
$$

Specialization is only meaningful if routing emphasizes $r_f$, suppresses common or non-route dominance, and preserves the partition during training.

Functional value metric:
$$
\mathcal{C}_{C,R}=\sum_e q_{C,e}q_{R,e}[-\cos(g_{C,e},g_{R,e})]_+.
$$

Observable metrics:
`feature_NMI`, `max_load`, `active_experts`, proxy-route NMI across checkpoints, all-position route-evaluation NMI, $\mathcal{C}_{C,R}$, rare loss, and expert utility guards.

Falsifier:
If route-relevant geometry cannot be found, cannot be preserved, or has no functional utility after preservation, then current evidence does not support feature-level expert specialization as a mainline claim.

## 5. Computational Realization

Input objects:
A05 common-logit and common-bias audits; A06 route-position, all-position, and real-DCLM proxy audits; A07 common/rare conflict audits.

Computed variables:
Common-centered route metrics, route-position cluster centers, proxy labels, checkpoint proxy-route NMI, all-position merge metrics, and common/rare conflict metrics.

Algorithm stages:

- audit why ordinary top-1 routing fails;
- construct route-position feature centers;
- test whether the partition survives early training;
- only after preservation, test functional utility or common/rare conflict reduction.

Stage-local evidence:
A05 supports wrong-object / early-feedback risk; A06 supports reachable route-position geometry and exposes preservation failure; A07 gives a functional metric but currently only weak neural evidence.

Expected artifacts:
One next `Thinking Card`, then one approved `protocol.md`, followed by `summary.md`, `detailed.md`, and an anchor update.

## 6. Minimal Falsification Tests

Test:
Real-text early-preservation audit.
Question:
Can step-0 DCLM proxy routing survive step 5/10?
Intervention / comparison:
Compare ordinary training with router freeze, delayed router update, low router learning rate, common/load anti-collapse control, or proxy-preservation auxiliary loss.
Primary metric:
Step-5/10 proxy-route NMI under fixed step-0 proxy labels, with LM loss guard.
Supports:
At least one preservation mechanism keeps proxy-route NMI clearly above ordinary training without unacceptable loss regression.
Weakens:
All mechanisms collapse to ordinary-training NMI or damage LM loss.
Insufficient evidence:
Proxy labels, checkpoints, loss guard, or exact route object are missing.

Test:
Label-free route-relevant state selector.
Question:
Can the system identify the hidden-state pool that should define the route partition without labels?
Intervention / comparison:
Compare route-only upper bound, all-position baseline, role-balanced pool, and label-free route selector.
Primary metric:
Held-out route-position `feature_NMI`.
Supports:
Label-free selector approaches route-only performance and beats all-position.
Weakens:
Selector behaves like all-position or needs feature labels.
Insufficient evidence:
The selector is evaluated only on the fitting pool.

Test:
Functional utility after preservation.
Question:
Does the preserved partition reduce feature interference or improve expert utility?
Intervention / comparison:
Preserved routing versus dense/shared and random top-1 baselines.
Primary metric:
Routing-weighted common/rare conflict with rare-loss or expert-utility guard.
Supports:
Conflict reduction is positive and rare loss or expert utility improves.
Weakens:
Conflict improves without utility, or dense/shared remains better.
Insufficient evidence:
Load, capacity, or objective is unmatched.

## 7. Current Evidence

Observation:
A05 shows ordinary random or early-trained top-1 routing can fail because the gate sees common or wrong geometric objects. Toy dot-product evidence supports common-logit causality; real DCLM weakens pure step-0 common dominance but shows centering reduces max load and step-10 common channel amplification.

Interpretation:
The main failure mechanism is not simply "uniform features are hard." The sharper risk is wrong-object routing plus early-training feedback.

Evidence links:

- `Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_03_real_text_common_logit_initialization_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A05/A05_04_02_round2_dotproduct_common_logit/summary.md`
- `Projects/from-attention-to-search/main/experiments/A05/A05_04_03_real_text_common_logit_audit/summary.md`

Observation:
A06 shows route-position feature centers are reachable and can be preserved in controlled synthetic-to-realistic bridges, but all-position clustering fails because it mixes route and non-route states. Real DCLM proxy routing is available at step 0 but ordinary training destroys it by step 5/10.

Interpretation:
The next problem is route-relevant state selection and early-training preservation, not proving feature geometry exists again.

Evidence links:

- `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_17_all_position_route_relevant_feature_discovery_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_10_real_dclm_proxy_feature_operationalization/summary.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md`
- `Projects/from-attention-to-search/main/experiments/A06/A06_17_all_position_route_relevant_feature_discovery/summary.md`

Observation:
A07 reframes value around common/rare functional interference. A07_01 to A07_03 validate the controlled audit machinery, while A07_04 neural proxy measures conflict but gives only weak centered-split improvement and does not beat the dense rare-loss boundary.

Interpretation:
Functional specialization remains unclaimed. A07 should be resumed only after preservation and proxy/router correction.

Evidence links:

- `Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_04_common_rare_gradient_conflict_splitting_anchor.md`
- `Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md`

## 8. Claim Boundary And Next Decision

Can claim:
Feature-level partition is reachable in controlled route-position geometry, ordinary top-1 does not naturally discover or preserve it, and all-position or raw random routing can fail because they optimize the wrong object.

Cannot claim:
Real semantic experts, deployable MoE gating, dense-beating functional value, true natural-language specialization, or KV-cache retrieval benefit.

Next decision:
Write and approve one real-text early-preservation protocol. The test should decide whether a step-0 DCLM proxy partition can survive the step-5/10 training window before any stronger A07 utility or real-semantic claim is promoted.
