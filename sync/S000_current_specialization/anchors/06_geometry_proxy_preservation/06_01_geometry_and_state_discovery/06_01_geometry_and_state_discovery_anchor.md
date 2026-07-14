# A06_01 Geometry And Route-Relevant State Discovery

Status: completed parent anchor with a negative label-free boundary.

## 0. Thinking Card

**Phenomenon:** The intended feature partition is linearly reachable when the
correct route-position states are known. Clustering all positions, waiting for
warmup, or extracting stronger spectral directions does not reliably identify
the same population. Real-text proxies can initialize a Router but are rapidly
overwritten by ordinary training.

**Physical judgment:** The initialization problem has three contracts:
route-relevant information must exist, the correct state population must be
selected without privileged labels, and the resulting rows must enter a
trainable basin. Existing evidence passes the first contract, partially passes
the second only with controlled supervision, and fails the third on real proxy
training.

## 1. Complete Problem

**Decision question:** Can unlabeled hidden-state structure provide a stable,
trainable initial feature partition for a top-1 Router?

### Terminology / Definitions

| Term | Plain meaning | Decision role | Cannot prove |
|---|---|---|---|
| Route-relevant state | A state carrying the condition at the actual routing decision | Defines the legitimate clustering population | Expert utility |
| State selector | A label-free score choosing which positions enter center fitting | Tests whether route relevance is discoverable | Long-run preservation |
| Proxy | A split-stable real-text partition without semantic status | Real-data bridge | A useful expert identity |
| Low-tail margin | Weak examples' score lead for the assigned expert | Guards initialization robustness | Training safety by itself |

## 2. Physical Priors

1. A linear Router can use a feature only if it is readable at the routed
   state.
2. Common components and Router-row norms can change load without changing
   feature identity.
3. Sequence positions encode different computational roles; mixing them can
   merge otherwise separable conditions.
4. A stronger cluster signal is irrelevant if it comes from the wrong state
   population.

## 3. Falsifiable Hypotheses

**H1: geometric reachability.** Oracle route-position centers cannot produce a
balanced positive-margin partition. Rejected by the controlled positive
control.

**H2: all-position equivalence.** All hidden states are an adequate substitute
for route-position states. Rejected by route-only versus all-position feature
merges.

**H3: generic selector sufficiency.** Warmup, stability, spectral, or raw
full-language-model gradient scores identify the useful state population and
retain positive margin. Rejected for the tested families.

**H4: real-proxy preservation.** A split-stable and linearly routable real
proxy survives ordinary language-model training. Rejected on the tested DCLM
bridge.

## 4. Core Mathematical Model

For selected state pool

$$
\mathcal H_{sel}=\{h_{i,p}:p\in\operatorname{TopK}(S_{i,p})\},
$$

fit condition centers $\mu_k$ and initialize equal-norm rows $w_k\propto
\mu_k$. The selector passes only when held-out routed states have both high
partition agreement and positive low-tail margin:

$$
m_k^{tail}
=\operatorname{p05}_{h\mid k}
\left[w_k^\top h-\max_{b\ne k}w_b^\top h\right]>0.
$$

For a real proxy, its definition must be fixed on calibration data and repeated
on held-out data before Router initialization.

## 5. Evidence Chain

1. Row-norm and common-component controls explain load artifacts but do not
   recover feature identity.
2. Oracle route-position centers reach feature NMI 1.0, balanced load, and
   positive margin; slot-length replay rejects a one-token artifact.
3. Route-position clustering reaches NMI 1.0 while mixed all-position pools
   merge features; generic stability and common-logit selectors do not close
   the gap.
4. Warmup increases feature-center distance, but does not clean the state
   population. Expert singular directions, manifold power iteration, and
   gradient selectors improve selected metrics without establishing a safe
   full-LM initializer.
5. Real DCLM proxies are reproducible and linearly routable, but their held-out
   route NMI falls from 0.7549 at initialization to 0.0410 at step 5 and 0.0131
   at step 10.

### Subanchor Registry

| Subanchor | Local decision | Experiment group |
|---|---|---|
| [`A06_01_01`](subanchors/06_01_01_common_geometry_nuisance_controls_anchor.md) | Common directions and row norms are nuisance controls, not feature discovery. | [`E01`--`E06`](../../../../../Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery) |
| [`A06_01_02`](subanchors/06_01_02_oracle_partition_reachability_anchor.md) | The intended partition is linearly reachable when routed states are known. | [`E01`--`E02`](../../../../../Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery) |
| [`A06_01_03`](subanchors/06_01_03_label_free_route_state_selection_anchor.md) | Tested label-free selectors do not recover the oracle state population safely. | [`E01`--`E07`](../../../../../Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery) |
| [`A06_01_04`](subanchors/06_01_04_real_proxy_initialization_overwrite_anchor.md) | A real proxy can initialize routing but ordinary training rapidly overwrites it. | [`E01`--`E04`](../../../../../Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery) |
| [`A06_01_05`](subanchors/06_01_05_warmup_spectral_gradient_selector_audit_anchor.md) | Warmup, spectral, and gradient scores fail the joint state-selection and margin contract. | [`E01`--`E05`](../../../../../Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery) |
| [`A06_01_06`](subanchors/06_01_06_spectral_reservoir_method_audit_anchor.md) | Iterative expert-direction extraction remains a diagnostic, not a feature-aware Router. | [`E01`--`E04`](../../../../../Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery) |
| [`A06_01_07`](subanchors/06_01_07_static_expert_geometry_side_theory_anchor.md) | Static expert geometry is secondary evidence outside the active training-dynamics chain. | [`E01`--`E04`](../../../../../Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery) |

## 6. Minimal Adjudication Contract

A label-free initializer must beat all-position clustering, approach the
route-position positive control, pass nuisance-label and equal-norm guards, and
retain positive low-tail margin under the registered full-sequence objective.
High NMI with negative low-tail margin is insufficient.

## 7. Current Verdict

**Supported:** route-relevant geometry exists and can initialize a controlled
partition. Stable real-text proxies can also seed nontrivial routing.

**Weakened:** no tested fully label-free selector identifies the correct state
population and remains safe under full-LM training.

**Rejected as mainline methods:** repeated common subtraction, all-position
warmup, static expert SVD, manifold power iteration, and the tested raw or
denoised gradient selectors.

## 8. Claim Boundary And Next Decision

**Cannot claim:** unsupervised semantic feature discovery, preserved real-text
routing, or expert utility.

**Next decision:** given a supplied partition, determine the signed training
dynamics that spend or restore its route-margin budget (`A06_02`).
