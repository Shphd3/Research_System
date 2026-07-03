# A06 Geometry Proxy Preservation Closure Report

## Subtitle

From feature-center discovery to margin-budget preservation.

Canonical map: [`research_map.md`](../research_map.md)  
Scope: A06 controlled geometry, real-DCLM proxy initialization, and preservation mechanism through A06_21.

## Abstract

Current verdict:

```text
Feature/proxy structure can be discovered in router-input hidden states and
can initialize a top-1 MoE router.
In the corrected controlled bridge, center initialization is preserved because
the initialized router creates positive route margins around feature centers.
The router does not need to actively follow drifting feature centers.
In real-DCLM next-token training, the same proxy routing is erased by step 5/10.
The next question is which margin-budget term fails in real-DCLM training.
```

What this closure establishes:

- A06 has moved from "can feature-to-expert specialization form?" to "what
  geometric condition makes it preserve?"
- The controlled answer is a positive-margin basin around route-relevant
  feature/proxy centers.
- The real-DCLM bottleneck is not step-0 linear routing. The bottleneck is
  preservation under ordinary training.

What remains open:

- Whether real-DCLM proxy clusters are semantic features.
- Whether high route agreement implies expert utility.
- Whether real-DCLM failure is caused by common overwrite, representation
  drift, router drift, token spread, or their interaction.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Why it matters | Cannot prove |
|---|---|---|---|---|
| Feature | The route-relevant label in controlled synthetic data. | The synthetic label used to define the prediction target and expected routing partition. | It is the clean target for controlled mechanism tests. | Real language semantics. |
| Proxy | A reproducible hidden-state cluster in real DCLM. | Cluster assignment learned from real-DCLM hidden states and evaluated by held-out stability. | It gives a label-free operational target for real-data routing. | That the cluster is a semantic feature. |
| Route-position hidden state | The hidden state actually fed to the router for the decision. | In the corrected controlled bridge, the last token of the feature slot. | It is the correct population for router initialization. | That all hidden states carry the same route information. |
| All-position pool | Hidden states from route and non-route positions mixed together. | K-means or representation learning over all token positions. | It tests whether route-relevant states can be found without position labels. | A valid route initializer by itself. |
| Top-1 router | Sparse router that sends each token to the highest-scoring expert. | Scores $s_e(h)=w_e^\top h$, assignment $\arg\max_e s_e(h)$. | It defines expert regions as linear cones in hidden-state space. | Expert utility or semantic specialization. |
| Feature NMI | Partition agreement between feature/proxy labels and expert assignments. | Normalized mutual information between labels and top-1 expert ids. | It says whether routing separates the target partition. | Preservation of the original feature-expert matching. |
| Matched preserve fraction | Whether the original step-0 feature-expert mapping survives. | Fraction of examples still routed to the matched initial expert region. | It catches feature-expert swaps and partial merges hidden by NMI. | Expert utility. |
| Route margin | Distance-like score gap from intended expert to nearest competitor. | $m_f=\min_{e\ne a(f)}(w_{a(f)}-w_e)^\top\mu_f$. | It is the core preservation condition. | That tokens away from the center are safe. |
| Cluster-aware margin | Route margin after accounting for within-cluster spread. | Center margin minus a token-spread allowance. | It tests whether the cluster, not just the center, stays inside the region. | Exact behavior of every tail token unless tails are audited. |
| Common component | A hidden-state direction shared across many tokens. | A mean, principal direction, or routing-aware direction used for common/residual audits. | It can create load bias or hide residual feature geometry. | A universal correction method. |
| Margin budget | The decomposition of margin gain/loss over training. | Router drift term, feature-center drift term, and interaction term. | It localizes why preservation succeeds or fails. | Real-DCLM failure before the real audit is run. |
| DCLM | The real language-data training surface used in this line. | Packed DCLM token stream and its router-input hidden states. | It is the bridge from controlled features to real-data proxy routing. | That a proxy cluster is semantically meaningful. |
| MoE | Mixture of Experts, a model block with multiple experts and a router. | Top-1 MoE sends each routed token to one selected expert. | It is the mechanism whose specialization is being tested. | That selected experts learn useful roles. |
| SAE / autoencoder | A representation-learning method that reconstructs hidden states through a constrained code. | Sparse autoencoder or bottleneck autoencoder fitted to hidden states. | It tests whether generic representation learning discovers route-relevant states. | Route relevance when the objective is only reconstruction. |
| Raw center / residual center | Two ways to turn cluster centers into router rows. | Raw center uses the original hidden-state mean; residual center subtracts an estimated common component first. | A06_11 shows raw centers work better for actual raw-input routing. | That residual geometry is useless; it may work under centered-input diagnostics. |
| C0-C4 bridge cells | Controlled data cells with increasing nuisance and population difficulty. | C0-C3 test route-position discovery/preservation; C4 tests all-position clustering. | They isolate whether failure comes from feature strength, nuisance, or wrong state population. | Real-DCLM behavior. |
| Rho | Perturbation strength for moving initialized router rows away from pseudo centers. | A scalar sweep in A06_17_05; rho 0 is exact pseudo-center, rho 1 is random-direction scale. | It tests whether exact centers are required or whether a positive-margin basin exists. | The exact tolerance in real-DCLM. |

## 1. Motivation

The original A06 question was broad:

```text
Can hidden-state geometry support label-free feature/proxy-level top-1 MoE
router initialization, and can that routing survive training?
```

The useful version is narrower:

```text
If a feature/proxy center is found, does the router create a positive decision
margin around it, and does training keep that margin positive?
```

This shift matters because clustering alone is not enough. A center can be
found but fail to route. A router can route at step 0 but fail during training.
NMI can be high but hide the loss of the original feature-to-expert mapping.
A06 therefore became a margin-budget line.

## 2. What Must Be Distinguished

The closure depends on five distinctions:

| Confused concepts | Correct distinction |
|---|---|
| Feature versus proxy | Controlled features are ground-truth synthetic labels; real-DCLM proxies are stable clusters only. |
| Discovery versus preservation | Discovery asks whether centers can be found; preservation asks whether the initialized expert regions survive training. |
| Route-position versus all-position states | The router only sees one decision state; mixing every position can merge role-specific geometry. |
| NMI versus matched preservation | NMI measures partition similarity; matched preservation measures whether the initial assignment survived. |
| Load balance versus specialization | Balanced load can occur without feature routing; feature routing can fail even if load looks reasonable. |

## 3. Clean Baseline / No-Effect Case

Two negative or no-effect results define the baseline:

1. In real-DCLM training, raw proxy-center routing is strong at step 0 but is
   erased quickly. A06_12 raw-center NMI drops from 0.7549 at step 0 to 0.0410
   at step 5 and 0.0131 at step 10.
2. In the controlled bridge, all-position clustering is not a reliable proxy
   for route-position clustering. A06_17 route-only feature NMI is 1.000, while
   all-position mean NMI is 0.797.

These results rule out a simple story where "finding any cluster" or "getting
balanced load" is enough.

## 4. Mechanism Model

For feature/proxy $f$, let $\mu_f(t)$ be its route-position center and let
$w_e(t)$ be router row $e$. At step 0, the matched expert is

$$
a(f)=\arg\max_e w_e(0)^\top \mu_f(0).
$$

For every competing expert $e\ne a(f)$, define the pairwise route margin:

$$
g_{f,e}(t)=(w_{a(f)}(t)-w_e(t))^\top\mu_f(t).
$$

The center is preserved if

$$
\min_{e\ne a(f)} g_{f,e}(t)>0.
$$

The margin change decomposes as

$$
\Delta g_{f,e}
=\Delta w_{a,e}^\top\mu_f(0)
+w_{a,e}(0)^\top\Delta\mu_f
+\Delta w_{a,e}^\top\Delta\mu_f,
$$

where $w_{a,e}=w_{a(f)}-w_e$.

Interpretation:

| Model term | Meaning | Mechanism tested |
|---|---|---|
| $\Delta w_{a,e}^\top\mu_f(0)$ | Router-row movement under old feature center. | Does router drift destroy the old partition? |
| $w_{a,e}(0)^\top\Delta\mu_f$ | Feature-center movement under old router boundary. | Does representation drift cross the old boundary? |
| $\Delta w_{a,e}^\top\Delta\mu_f$ | Coupled router-center movement. | Does training feedback jointly move both objects into failure? |

With $h=c+r$, the score gap also decomposes as

$$
(w_a-w_e)^\top h=(w_a-w_e)^\top c+(w_a-w_e)^\top r.
$$

This is the common/residual audit. It asks whether a shared direction $c$
dominates routing or whether residual feature geometry $r$ carries the
specialization.

## 5. Propositions And Proofs

**Proposition 1: Positive center margin is sufficient for center preservation.**

If $g_{f,e}(t)>0$ for every $e\ne a(f)$, then the top-1 router assigns
$\mu_f(t)$ to $a(f)$.

Proof: for every competitor $e$,

$$
w_{a(f)}(t)^\top\mu_f(t)-w_e(t)^\top\mu_f(t)=g_{f,e}(t)>0.
$$

Therefore the intended expert has the highest score.

**Proposition 2: Positive cluster-aware margin is sufficient for local token
preservation.**

If tokens in cluster $f$ satisfy $h=\mu_f+\epsilon$ and

$$
g_{f,e}(t)>\|(w_{a(f)}(t)-w_e(t))\|\cdot\|\epsilon\|
$$

for every competitor, then those tokens stay in the intended expert region.

Proof: Cauchy-Schwarz bounds the maximum margin loss from $\epsilon$. The
remaining score gap is still positive.

**Proposition 3: Margin-budget decomposition is exact.**

The decomposition in Section 4 is an algebraic identity. A06_21 measured a
maximum implementation error of $1.37\times10^{-6}$.

**Metric proposition: NMI alone cannot prove preservation.**

NMI can stay high after expert permutation or partial feature merge. Therefore
preservation requires NMI plus matched preserve fraction, margin sign, and
sign-flip rate.

## 6. Controlled Evidence

The controlled bridge isolates the geometry under a one-layer Transformer +
top-1 MoE, no learned absolute positional embedding, slot length 4, and routing
on the last slot token.

Main controlled updates:

| Experiment | Observation | Interpretation |
|---|---|---|
| A06_16 | C0-C3 step-0 pseudo NMI and final feature NMI are 1.000. | Route-position feature centers can initialize and preserve routing in the corrected bridge. |
| A06_17 | Route-only and route-offset NMI are 1.000; all-position mean NMI is 0.797. | The correct hidden-state population is route-relevant states, not every token. |
| A06_17_02 | Center-init final NMI is 1.000, but movement alignment is negative. | Preservation is not active router-center tracking. |
| A06_17_03 | Max boundary consumption mean is 0.530; dynamic switch rate is 0.000. | Drift consumes only part of the initial margin buffer. |
| A06_17_04 | Forced row crossing breaks the original feature-to-expert region. | Margin is a valid geometric switch ruler. |
| A06_17_05 | Perturbations through rho 0.7 preserve; rho 1.0 has negative margin and poor preserve fraction. | Exact centers are not necessary; a positive-margin basin is necessary. |
| A06_21 | Pseudo/oracle center-init keeps NMI 1.000, preserve 1.000, positive margins, and zero sign flips; random/shuffled guards do not. | The controlled preservation mechanism is positive current and cluster-aware margin. |

Controlled conclusion:

```text
In the corrected bridge, feature-to-expert specialization is preserved when
the initialized router creates a positive margin buffer around route-relevant
feature centers.
```

## 7. Real Evidence / Negative Result

The real-DCLM experiments answer a different question: whether the same proxy
idea survives ordinary next-token training.

| Experiment | Observation | Interpretation |
|---|---|---|
| A06_10 | Step-10 residual proxy stability NMI is 0.5211; layer-5 stability is 0.6501; frequency and position NMI are much lower. | Real-DCLM hidden states contain stable proxy clusters. |
| A06_11 | Step-10 raw-center equal-norm routing reaches proxy-route NMI 0.8811 versus random 0.0417. | Proxy centers are linearly routable at step 0. |
| A06_12 | Raw-center NMI falls from 0.7549 to 0.0410 by step 5 and 0.0131 by step 10; loss is comparable across variants. | Ordinary DCLM training erases proxy routing without an obvious loss crash. |

Real-data conclusion:

```text
The real-DCLM bottleneck is not the existence of proxy geometry and not the
step-0 linear router bridge. The bottleneck is early training preservation.
```

## 8. Reconciliation And Refined Theory

The controlled and real results do not conflict. They answer different parts of
the same mechanism.

| Apparent conflict | Reconciliation |
|---|---|
| Controlled center-init preserves, but real-DCLM center-init collapses. | Controlled runs show preservation is possible under positive margin. Real runs have not yet been audited for whether that margin exists or is consumed. |
| Clustering can find centers, but all-position clustering fails. | Route-position clustering and all-position clustering are different operationalizations. The latter mixes role-specific states. |
| Good initialization matters, but router rows do not track centers. | Initialization matters because it creates a margin buffer, not because it guarantees future co-movement. |
| Common subtraction sometimes helps, but route-logit common estimation failed. | Common/residual decomposition is a diagnostic. The tested estimator did not isolate route-relevant residual feature structure. |

Refined working theory:

```text
Feature/proxy specialization is a margin-preservation problem in router-input
hidden-state space. Center discovery is only useful if the resulting router rows
create a positive, cluster-aware margin that survives early training.
```

## 9. Next Experiment

Next decision:

```text
Run a real-DCLM margin-budget audit on A06_12-style proxy-init training.
```

Minimal design:

1. Reuse the A06_12 real-DCLM proxy-init setup.
2. Save router rows, route-input hidden states, proxy centers, proxy labels,
   and expert assignments at steps 0, 1, 2, 3, 5, and 10.
3. Compute proxy-route NMI, matched preserve fraction, current margin,
   cluster-aware margin, sign-flip rate, common/residual margin terms, max
   load, and language-model loss.

Decision table:

| Outcome | Mechanism update | Next action |
|---|---|---|
| Step-0 margin is weak or negative. | Real proxy-center initialization is not geometrically safe enough. | Improve proxy selection or center normalization before training. |
| Step-0 margin is positive but disappears by step 5. | Real failure is margin-budget collapse. | Decompose router drift, center drift, common overwrite, token spread, and interaction. |
| Common term dominates the loss of margin. | Failure is common-direction overwrite. | Test common-invariant or common-guarded routing. |
| Feature-center drift dominates. | Representation motion crosses the old router boundary. | Study representation-router co-movement and early stabilization. |
| Margins remain positive but NMI collapses. | Center-level audit is insufficient. | Move to token-level tail-risk and cluster-aware diagnostics. |
| Preservation succeeds in the rerun. | A06_12 and the rerun disagree. | Reconcile implementation and snapshot differences before utility tests. |

## 10. Source Map And Audit Tables

### 10.1 Experiment Logic Chain

| Step | Question | Result | Knowledge update |
|---|---|---|---|
| A06_03-A06_05 | Can common directions and residual geometry explain early routing behavior? | Common components can dominate load; residual geometry remains after centering. | Load imbalance alone is not specialization. |
| A06_06-A06_09 | Is synthetic feature routing reachable and preservable? | Oracle and label-free route-position discovery can initialize feature routing. | Feature routing is geometrically reachable under controlled data. |
| A06_10-A06_12 | Does real-DCLM proxy geometry route and preserve? | Proxy exists and routes at step 0, but training erases it by step 5/10. | The real bottleneck is preservation. |
| A06_16-A06_17 | What caused the earlier controlled discovery failure? | No-position route-position discovery passes; all-position remains unreliable. | State population matters. |
| A06_17_02-A06_17_05 | Why does controlled center-init preserve? | Positive margins, not active tracking or exact center equality. | Preservation is a margin-basin phenomenon. |
| A06_18-A06_20 | Can minimal-prior selectors or common estimators recover centers from all positions? | Tested selectors and route-logit common estimator fail to solve recovery. | Route relevance remains unsolved under minimal priors. |
| A06_21 | Which metric explains controlled preservation? | Current and cluster-aware margins stay positive; sign flips stay zero. | Margin-budget audit is the right next diagnostic for real DCLM. |

### 10.2 Measured Results

| Experiment | Primary evidence | Decision |
|---|---|---|
| [A06_10](../../../experiments/A06/A06_10_real_dclm_proxy_feature_operationalization/summary.md) | Step-10 residual stability NMI 0.5211; layer-5 stability 0.6501. | Real-DCLM proxy exists with non-semantic boundary. |
| [A06_11](../../../experiments/A06/A06_11_real_dclm_proxy_center_router_initialization/summary.md) | Step-10 raw-center equal-norm proxy-route NMI 0.8811 versus random 0.0417. | Proxy centers are linearly routable at step 0. |
| [A06_12](../../../experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md) | Raw-center NMI 0.7549 -> 0.0410 by step 5 -> 0.0131 by step 10. | Ordinary DCLM training erases proxy routing. |
| [A06_16](../../../experiments/A06/A06_16_synthetic_to_realistic_proxy_bridge/summary.md) | C0-C3 step-0 pseudo NMI and final feature NMI are 1.000. | Corrected no-position route-position bridge passes. |
| [A06_17](../../../experiments/A06/A06_17_all_position_route_relevant_feature_discovery/summary.md) | Route-only NMI 1.000; all-position mean NMI 0.797. | Route-relevant state selection is required. |
| [A06_17_02](../../../experiments/A06/A06_17_02_router_center_tracking_preservation/summary.md) | Center-init final NMI 1.000; movement alignment about -0.4. | Active tracking is not the mechanism. |
| [A06_17_03](../../../experiments/A06/A06_17_03_feature_drift_margin_boundary/summary.md) | Pseudo max boundary consumption mean 0.530; switch rate 0.000. | Drift stays inside the margin buffer. |
| [A06_17_04](../../../experiments/A06/A06_17_04_margin_crossing_causal_stress/summary.md) | Forced crossing makes margin negative and preserve fraction collapse. | Margin is a valid geometric switch ruler. |
| [A06_17_05](../../../experiments/A06/A06_17_05_margin_basin_robust_initialization/summary.md) | Rho 0.7 preserves; rho 1.0 has negative margin and preserve 0.219. | Positive-margin basin, not exact center equality. |
| [A06_18](../../../experiments/A06/A06_18_label_free_route_relevant_state_selector/summary.md) | Route-only 1.000; PCA q=4 0.871; SAE L1 8x 0.729. | Generic representation learning does not define route relevance. |
| [A06_19](../../../experiments/A06/A06_19_minimal_prior_margin_aware_center_search/summary.md) | Raw all-token 0.863; M1 0.843; M2 continuous 0.784. | Tested minimal-prior margin signals do not solve selection. |
| [A06_20](../../../experiments/A06/A06_20_route_logit_common_estimator_random_init_feature_recovery/summary.md) | Route-logit subtraction 0.815 versus raw all-position 0.829. | Tested route-logit common estimator is not the solution. |
| [A06_21](../../../experiments/A06/A06_21_margin_budget_preservation_audit/summary.md) | Step-10 pseudo/oracle NMI 1.000, preserve 1.000, positive margins, zero sign flips. | Margin budget explains controlled preservation. |

### 10.3 Proved / Assumed / Empirical

| Type | Statement | Status |
|---|---|---|
| Proved from model | Positive center margin preserves the center assignment. | Mathematical statement. |
| Proved from model | Positive cluster-aware margin preserves local tokens within the stated spread bound. | Mathematical statement. |
| Proved from algebra | Margin-budget decomposition is exact. | Implementation verified in A06_21. |
| Empirical | Controlled bridge center-init preserves because margins remain positive. | Supported by A06_17_02-A06_21. |
| Empirical | Real-DCLM proxy clusters exist and route at step 0. | Supported by A06_10-A06_11. |
| Empirical negative | Ordinary real-DCLM training erases proxy routing. | Supported by A06_12. |
| Assumption | Real-DCLM proxy clusters are useful targets for specialization. | Operational assumption, not semantic proof. |
| Open empirical proposition | Real-DCLM failure is margin-budget collapse. | Next experiment decides. |

## 11. Claim Boundary

Can claim:

- route-position feature/proxy geometry can support top-1 router
  specialization;
- raw proxy centers can initialize a strong real-DCLM proxy router at step 0;
- ordinary real-DCLM next-token training erases that proxy routing quickly in
  the tested setup;
- controlled no-position preservation is explained by positive current and
  cluster-aware route margins;
- exact center equality is not required when the initialization lies inside a
  positive-margin basin;
- all-position hidden-state clustering is not a reliable substitute for
  route-relevant state selection.

Cannot claim:

- real-DCLM proxy clusters are semantic language features;
- high route NMI implies expert utility;
- load balance implies specialization;
- common subtraction is a general fix;
- SAE or generic representation learning can or cannot ever solve route
  relevance beyond the tested settings;
- real-DCLM preservation is impossible;
- the real-DCLM failure is already explained by the controlled margin model.

## Appendix. Data / Model / Parameters / Scripts

| Experiment | Data / model / parameters | Seeds / checkpoints | Script / config / result path | Primary metric |
|---|---|---|---|---|
| A06_10 | Packed DCLM stream; Qwen-style top-1 MoE; 6 layers, hidden 512, 8 experts; layers 0/3/4/5. | Seeds 0-2; checkpoints 0/10. | `scripts/run_real_dclm_proxy_feature_operationalization.py`; result `runs/real_dclm_proxy_feature_operationalization/.../proxy_cluster_summary.csv`; records [summary](../../../experiments/A06/A06_10_real_dclm_proxy_feature_operationalization/summary.md), [detailed](../../../experiments/A06/A06_10_real_dclm_proxy_feature_operationalization/detailed.md). | Held-out proxy assignment stability NMI. |
| A06_11 | Same real-DCLM hidden states; router rows from raw/residual proxy centers; equal-norm guard. | Seeds 0-2; source steps 0/10; layers 0/3/4/5. | `scripts/run_real_dclm_proxy_center_router_initialization.py`; result `runs/real_dclm_proxy_center_router_initialization/.../router_initialization_summary.csv`; records [summary](../../../experiments/A06/A06_11_real_dclm_proxy_center_router_initialization/summary.md), [detailed](../../../experiments/A06/A06_11_real_dclm_proxy_center_router_initialization/detailed.md). | Proxy-route NMI on raw router input. |
| A06_12 | Real-DCLM next-token training; random, equal-norm random, raw-center, residual-center variants. | Seeds 0-2; steps 0/1/2/3/5/10/20/50. | `scripts/run_real_dclm_proxy_init_training_preservation.py`; result `runs/real_dclm_proxy_init_training_preservation/.../training_preservation_summary.csv`; records [summary](../../../experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/summary.md), [detailed](../../../experiments/A06/A06_12_real_dclm_proxy_init_training_preservation/detailed.md). | Proxy-route NMI over training. |
| A06_16 | Controlled one-layer Transformer + top-1 MoE; 4 experts; no learned absolute positional embedding; slot length 4; route on last slot token. | C0-C4 cells; 8 seeds where applicable. | `scripts/run_a06_16_synthetic_to_realistic_proxy_bridge.py`; config `configs/a06_16_synthetic_to_realistic_proxy_bridge_no_pos_full.json`; result `results/a06_16_synthetic_to_realistic_proxy_bridge/a06_16_proxy_bridge_no_pos_same_model_audit_full_20260623_1`; records [summary](../../../experiments/A06/A06_16_synthetic_to_realistic_proxy_bridge/summary.md), [detailed](../../../experiments/A06/A06_16_synthetic_to_realistic_proxy_bridge/detailed.md). | First failed stage; feature NMI. |
| A06_17 | Same controlled bridge; fit pools: route-only, slot offset, all-position, slot-mixed, role-balanced, non-slot. | 8 seeds. | `scripts/run_a06_17_all_position_route_relevant_feature_discovery.py`; config `configs/a06_17_all_position_route_relevant_feature_discovery.json`; result `results/a06_17_all_position_route_relevant_feature_discovery/a06_17_route_relevant_pool_audit_full_20260623_1`; records [summary](../../../experiments/A06/A06_17_all_position_route_relevant_feature_discovery/summary.md), [detailed](../../../experiments/A06/A06_17_all_position_route_relevant_feature_discovery/detailed.md). | Held-out route-position feature NMI. |
| A06_17_02 | Same bridge; pseudo-center, oracle-center, random, equal-norm random, label-shuffled center. | 8 seeds; snapshots through 1600 steps. | `scripts/run_a06_17_02_router_center_tracking_preservation.py`; config `configs/a06_17_02_router_center_tracking_preservation.json`; result `results/a06_17_02_router_center_tracking_preservation/a06_17_02_router_center_tracking_full_20260626_024804`; records [summary](../../../experiments/A06/A06_17_02_router_center_tracking_preservation/summary.md), [detailed](../../../experiments/A06/A06_17_02_router_center_tracking_preservation/detailed.md). | Movement alignment, feature NMI, route margin. |
| A06_17_03 | Same bridge; boundary-consumption audit. | 8 seeds; snapshots through 1600 steps. | `scripts/run_a06_17_03_feature_drift_margin_boundary.py`; config `configs/a06_17_02_router_center_tracking_preservation.json`; records [summary](../../../experiments/A06/A06_17_03_feature_drift_margin_boundary/summary.md), [detailed](../../../experiments/A06/A06_17_03_feature_drift_margin_boundary/detailed.md). | Boundary consumption and dynamic margin. |
| A06_17_04 | Same bridge; margin stress and forced row crossing. | C0-C3, 4 seeds. | `scripts/run_a06_17_04_margin_crossing_causal_stress.py`; config `configs/a06_17_04_margin_crossing_causal_stress.json`; result `results/a06_17_04_margin_crossing_causal_stress/a06_17_04_margin_crossing_full_20260629_1`; records [summary](../../../experiments/A06/A06_17_04_margin_crossing_causal_stress/summary.md), [detailed](../../../experiments/A06/A06_17_04_margin_crossing_causal_stress/detailed.md). | Static crossing ratio and preserve fraction. |
| A06_17_05 | Same bridge; pseudo-center row perturbation. | C0-C3, 4 seeds; rho sweep. | `scripts/run_a06_17_05_margin_basin_robust_initialization.py`; result `results/a06_17_05_margin_basin_robust_initialization/a06_17_05_margin_basin_full_20260629_1`; records [summary](../../../experiments/A06/A06_17_05_margin_basin_robust_initialization/summary.md), [detailed](../../../experiments/A06/A06_17_05_margin_basin_robust_initialization/detailed.md). | Final matched preserve fraction. |
| A06_18 | Controlled all-position selection; PCA, bottleneck AE, SAE, split-stability selectors. | 8 seeds. | `scripts/run_a06_18_label_free_route_relevant_state_selector.py`; config `configs/a06_18_label_free_route_relevant_state_selector.json`; run `a06_18_revision_full_local_2gpu_20260625`; records [summary](../../../experiments/A06/A06_18_label_free_route_relevant_state_selector/summary.md), [detailed](../../../experiments/A06/A06_18_label_free_route_relevant_state_selector/detailed.md). | Held-out route-position feature NMI. |
| A06_19 | Minimal-prior M1/M2 center search on all-position pool. | 8 seeds. | `scripts/run_a06_19_minimal_prior_margin_aware_center_search.py`; config `configs/a06_19_minimal_prior_margin_aware_center_search_full.json`; result `results/a06_19_minimal_prior_margin_aware_center_search/full_m1_m2_8seed_20260626`; records [summary](../../../experiments/A06/A06_19_minimal_prior_margin_aware_center_search/summary.md), [detailed](../../../experiments/A06/A06_19_minimal_prior_margin_aware_center_search/detailed.md). | Held-out route-position feature NMI. |
| A06_20 | Equal-norm random router training with common-direction estimators. | 8 seeds; steps 0/5/10/100/1600. | `scripts/run_a06_20_route_logit_common_estimator_random_init_feature_recovery.py`; config `configs/a06_20_route_logit_common_estimator_random_init_feature_recovery.json`; run `a06_20_route_logit_common_estimator_full_20260629_010533`; records [summary](../../../experiments/A06/A06_20_route_logit_common_estimator_random_init_feature_recovery/summary.md), [detailed](../../../experiments/A06/A06_20_route_logit_common_estimator_random_init_feature_recovery/detailed.md). | Delta feature NMI and delta margin versus raw all-position. |
| A06_21 | Controlled bridge margin-budget audit; pseudo/oracle/random/equal-norm/shuffled rows. | 8 seeds x C0-C3 x 5 conditions x 12 snapshots. | `scripts/run_a06_21_margin_budget_preservation_audit.py`; config `configs/a06_21_margin_budget_preservation_audit.json`; result `results/a06_21_margin_budget_preservation_audit/a06_21_margin_budget_full_20260629_1`; records [summary](../../../experiments/A06/A06_21_margin_budget_preservation_audit/summary.md), [detailed](../../../experiments/A06/A06_21_margin_budget_preservation_audit/detailed.md). | Feature NMI, preserve fraction, margin, sign flip, cluster-aware margin. |
