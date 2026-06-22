---
anchor_id: A06_08_label_free_feature_discovery_initialization
parent_node: rq.feature_specialization.initialization_method
status: active_draft
created: 2026-06-22
canonical_language: en
---

# A06_08 Label-Free Feature Discovery Initialization Anchor Draft

## 0. Tiny Summary

父问题：uniform feature distribution 下，random-init dot-product top-1 MoE 为什么不能自然形成 feature-level specialization。

当前子问题：A06_06 已证明 oracle feature-centroid initialization 能在 synthetic initialized hidden states 中达到 perfect feature routing；A06_07 已证明 simple global common-centering / projection / whitening 只能改善 load，不能恢复 feature_NMI。本轮测试 label-free feature discovery 是否能找到 pseudo-feature centers，并近似 oracle partition。

当前判断：这是 feature discovery diagnostic，不是 final router method。目标不是继续调 global control，而是判断 residual hidden state 中是否存在可无监督恢复的 feature-cluster / sparse-atom structure。

最危险边界：feature label 只能用于 evaluation，不能用于 discovery、center selection 或 router construction。聚类范围必须分清：`routed-position hidden states only` 与 `all hidden states` 是两个不同问题。

下一步决策：如果 pseudo centers 能显著提高 held-out feature_NMI 并接近 oracle upper bound，则进入 A06_09 training basin preservation；如果只改善 load 或学到 position/context clusters，则 feature-discovery initialization 被削弱。

Question:
Can label-free feature discovery on initialized hidden states recover pseudo-feature centers that approximate the A06_06 oracle feature partition?

Physical prior:
A06_06 shows that feature-level routing is geometrically reachable under oracle feature centers. A06_07 shows that global common/residual controls do not discover feature-aligned directions. Therefore the missing step may be multi-center latent feature discovery in the residual hidden space.

Core model:
For routed-position hidden states, write `h_i = c + r_i`, and model residuals as `r_i = mu_{f_i} + eps_i` or more generally `r_i = D a_i + eps_i`. Label-free discovery estimates pseudo centers / atoms `{nu_k}` from calibration hidden states, then initializes equal-norm router rows from these directions.

Model term being tested:
Recoverability of latent feature centers / atoms from hidden-state geometry without using labels.

Primary metric:
Held-out `feature_NMI`, read jointly with load imbalance `L`, margin, cluster stability, and position/context leakage guards.

Falsifier:
If pseudo centers improve load but not held-out feature_NMI, or if discovered clusters align more with position/context/token identity than feature identity, then label-free feature discovery does not approximate the oracle partition in this setting.

Can claim:
Only whether the tested label-free discovery families recover pseudo-feature centers in synthetic initialized hidden states.

Cannot claim:
Final MoE method, training stability, expert causal utility, real-text transfer, or that dictionary learning is generally sufficient.

Next decision:
Choose whether to proceed to A06_09 with the best pseudo-center initialization, or return to representation audit if no label-free discovery family recovers feature structure.

---

## 1. Problem Definition

Parent problem:
Uniform feature frequency does not guarantee feature-level expert specialization under random dot-product top-1 routing.

Immediate prior results:

- A06_06: oracle feature-centroid initialization reaches feature-level routing at step 0.
- A06_07: simple label-free global common/residual controls reduce load but do not improve feature_NMI.

Decision question:
Can label-free feature discovery from initialized hidden states produce pseudo centers that, when used as equal-norm router centers, yield held-out feature-level specialization above random/global-control baselines and toward the oracle upper bound?

Why this matters:
If this succeeds, the next method target is pseudo-center initialization plus training-basin preservation. If it fails, the gap between oracle reachability and label-free construction remains unresolved, and real-data experiments are premature.

Not in scope:
Training, final collapse, real text, expert utility, route-utility binding, or production router design.

---

## 2. Physical Priors

P1: Feature structure may exist as latent multi-center residual geometry.

Meaning:
After removing a global common component, routed hidden states may contain feature-aligned clusters or sparse latent atoms, even if global centering alone cannot reveal them.

Could be wrong if:
Residual hidden variation is dominated by context/position/noise rather than feature identity.

P2: Global common/residual control is too low-rank to recover a feature partition.

Meaning:
A single mean, top-PC removal, or whitening can improve load balance but does not construct one center per feature.

Could be wrong if:
A stronger global transformation plus random centers already achieves high held-out feature_NMI.

P3: Discovery scope changes the meaning of the learned structure.

Meaning:
Clustering only routed-position hidden states directly targets router input. Clustering all hidden states has more data but may learn token-type, position, background, or syntactic structure rather than routed feature structure.

Could be wrong if:
All-hidden discovery transfers cleanly to routed-position feature routing and passes leakage guards.

P4: Different discovery families test different latent assumptions.

Meaning:
K-means / vMF / GMM test one-center-per-sample mixture structure. Spectral clustering tests nonlinear manifold structure. Dictionary learning tests sparse compositional structure.

Could be wrong if:
All methods fail similarly, implying the hidden geometry does not contain recoverable label-free feature structure under the tested setup.

P5: Load balance is not specialization.

Meaning:
A method must improve feature_NMI or feature purity, not only lower max-load.

Could be wrong only if:
A later expert-utility audit proves load balance alone gives functional specialization; that is outside this anchor.

---

## 3. Falsifiable Hypotheses

H1: Routed-position discovery can approximate oracle feature centers.

Supported if:
Pseudo centers learned only from routed-position calibration hidden states raise held-out feature_NMI far above random/global-control baselines while maintaining balanced load and positive margin.

Weakened if:
They only improve load or produce many-to-one feature merging.

H2: All-hidden discovery is either beneficial or confounded.

Supported if:
All-hidden pseudo centers transfer to routed-position held-out routing and improve feature_NMI without aligning to position/context labels.

Weakened if:
All-hidden clusters mainly encode position, token type, or background structure and do not improve routed-position feature_NMI.

H3: Mixture-style discovery should work before dictionary learning in the current synthetic one-feature setting.

Supported if:
Spherical k-means, vMF mixture, or GMM recover feature-aligned pseudo centers close to oracle.

Weakened if:
Only sparse dictionary atoms work, suggesting the hidden representation is compositional rather than one-cluster-per-feature.

H4: Dictionary learning is useful only if residual states are sparse-compositional.

Supported if:
Sparse atoms yield higher held-out feature_NMI or more stable pseudo centers than mixture/clustering methods.

Weakened if:
Dictionary atoms align with nuisance variation or do not improve routing over clustering.

H5: Pseudo-center initialization must beat load-only controls.

Supported if:
Feature_NMI improves together with acceptable load and margin.

Weakened if:
Load improves but feature_NMI remains near A06_07 baseline.

---

## 4. Mathematical Model

Objects:
For sequence `s`, position `p`, feature `f`, hidden state `h_{s,p}`, routed-position hidden state `h_i^{route}`, common component `c`, residual `r_i=h_i^{route}-c`, and expert assignment `a_i`.

Routed-position residual mixture model:

```math
h_i^{route}=c+r_i, \qquad r_i = \mu_{f_i}+\epsilon_i.
```

General sparse dictionary model:

```math
r_i = D a_i + \epsilon_i,
```

where `D=[d_1,...,d_K]` are label-free atoms and `a_i` is a sparse code.

All-hidden decomposition:

```math
h_{s,p}=c + q_{pos(p)} + t_{token(s,p)} + b_{context(s,p)} + g_{feature(s)} + \epsilon_{s,p}.
```

This explains why all-hidden discovery can be useful but also confounded.

Pseudo-center router construction:

```math
w_e = \alpha \cdot \frac{\nu_{\pi(e)}}{\|\nu_{\pi(e)}\|},
```

where `nu_k` is a discovered center / atom, `alpha` is an equal norm scale, and `pi` is a label-free center-to-expert assignment. If `K>m`, select centers by routed-position activation mass / cluster occupancy / stability, not by feature labels.

Routing score:

```math
z_{i,e}=w_e^T \phi(h_i^{route}),
```

where `phi` is a fixed preprocessing function, such as raw, common-centered, or common-centered normalized hidden state. Labels cannot be used in `phi`.

Metrics:

```math
feature\_NMI=NMI(f_i,a_i), \qquad
L=m\max_e |p_e-1/m|,
```

```math
margin_i=z_{i,a_i}-\max_{e\ne a_i}z_{i,e}.
```

---

## 5. Computational Realization

Fixed data/model surface:
Use the same synthetic initialized hidden-state setting as A06_06/A06_07 unless explicitly stated. Use calibration/evaluation split. Feature labels are forbidden for discovery and router construction, and allowed only for evaluation.

Discovery scopes:

1. `route_only_scope`:
   - use only hidden states at the routed position;
   - this directly targets router input;
   - primary scope.

2. `all_hidden_scope`:
   - use hidden states from all positions;
   - more data but stronger nuisance-risk;
   - must report position/context/token leakage guards.

Preprocessing variants:

1. raw hidden;
2. common-centered hidden;
3. common-centered + unit-normalized hidden;
4. optional covariance-whitened hidden as diagnostic, not as final claim.

Discovery method families:

1. Euclidean k-means.
2. Spherical k-means.
3. Gaussian mixture model.
4. von Mises-Fisher / spherical mixture model, if implementation is available.
5. Spectral clustering on a kNN graph.
6. PCA / ICA direction discovery followed by center construction.
7. Dictionary learning / sparse coding with `K=m` and `K>m` guards.

Baselines / upper bounds:

1. random Gaussian router;
2. equal-norm random direction router;
3. A06_07 global common/residual control baselines;
4. oracle feature-centroid initialization from A06_06;
5. label-shuffled pseudo-center guard.

Expected artifacts:

- `tables/discovery_summary.csv`
- `tables/scope_comparison.csv`
- `tables/method_family_summary.csv`
- `tables/leakage_guard_summary.csv`
- `figures/route_heatmap_by_method.png`
- `figures/feature_vs_cluster_assignment.png`
- `summary.md`
- `detailed.md`

---

## 6. Minimal Falsification Tests

### Test 1: Routed-position pseudo-center discovery

Question:
Can label-free discovery on routed-position hidden states recover pseudo centers that improve held-out feature routing?

Primary metric:
Held-out `feature_NMI`, read with `L` and margin.

Supports:
Pseudo-center routing has high feature_NMI, balanced load, positive margin, and beats A06_07 global controls.

Weakens:
NMI remains near random/global-control baseline, or routing merges multiple features into one expert.

Insufficient evidence:
No calibration/evaluation split, feature labels leak into discovery, or only load is reported.

### Test 2: All-hidden discovery transfer and leakage guard

Question:
Does discovery from all hidden states produce route-relevant feature centers, or mainly nuisance centers?

Primary metric:
Held-out routed-position feature_NMI, plus position/context/token NMI guards.

Supports:
All-hidden centers improve routed-position feature_NMI and do not primarily align with position/context/token nuisance labels.

Weakens:
Centers are stable but align with nuisance variables rather than feature identity.

Insufficient evidence:
All-hidden clusters are evaluated only by load or qualitative plots.

### Test 3: Method-family comparison

Question:
Which latent assumption best matches the hidden geometry: mixture clusters, spherical clusters, nonlinear graph structure, or sparse dictionary atoms?

Primary metric:
Held-out feature_NMI and stability across seeds.

Supports:
A method family consistently improves feature_NMI across seeds and scopes.

Weakens:
All method families produce load-only improvement.

Insufficient evidence:
Hyperparameter sweep is too broad without a fixed primary readout.

### Test 4: Oracle gap analysis

Question:
How much of the A06_06 oracle feature partition can the best label-free discovery method recover?

Primary metric:
Gap to oracle in feature_NMI, load, and margin.

Supports:
Best pseudo-center method approaches oracle upper bound.

Weakens:
Large persistent NMI gap despite acceptable load.

Insufficient evidence:
Oracle and pseudo methods are evaluated on different hidden-state samples.

---

## 7. Current Evidence

Observation:
A06_05 supports residual covariance / structured residual geometry as a source of common-centered residual load, and weakens finite-sample noise as the main explanation.

Interpretation:
Residual hidden states contain non-isotropic structure, so feature discovery is plausible but not guaranteed.

Boundary:
A06_05 does not identify whether the structure is feature-aligned, position/context-aligned, or generic covariance anisotropy.

Evidence links:
`../experiments/A06_05_common_centered_residual_geometry_diagnostic/summary.md`
`../experiments/A06_05_common_centered_residual_geometry_diagnostic/detailed.md`

Observation:
A06_06 shows oracle feature-centroid initialization reaches perfect held-out feature routing in the synthetic hidden-state setting.

Interpretation:
The desired feature partition exists in the hidden geometry under oracle access.

Boundary:
This is not label-free and does not prove training stability.

Evidence links:
`../experiments/A06_06_feature_level_initialization_positive_control/summary.md`
`../experiments/A06_06_feature_level_initialization_positive_control/detailed.md`

Observation:
A06_07 shows that simple label-free global common/residual controls improve load but do not improve feature_NMI; whitening can even reduce NMI.

Interpretation:
Load balance is insufficient, and the missing operation is likely feature-aligned multi-center discovery rather than another global control.

Boundary:
This does not rule out clustering, dictionary learning, contrastive discovery, or other label-free feature discovery methods.

Evidence links:
`../experiments/A06_07_label_free_common_residual_control_router/summary.md`
`../experiments/A06_07_label_free_common_residual_control_router/detailed.md`

---

## 8. Claim Boundary And Next Decision

Can claim after this test:
Whether the tested label-free discovery methods can recover pseudo-feature centers in synthetic initialized hidden states and approximate the oracle initialization partition.

Cannot claim:
Final trained stability, real-text transfer, expert functional specialization, or a deployable MoE router.

Next decision:
If one method family recovers feature_NMI with acceptable load and margin, pass its pseudo-center initialization to A06_09 training basin preservation. If all fail, do not proceed to method training; instead audit whether feature signal is unrecoverable without labels or whether nuisance variation dominates the hidden space.
