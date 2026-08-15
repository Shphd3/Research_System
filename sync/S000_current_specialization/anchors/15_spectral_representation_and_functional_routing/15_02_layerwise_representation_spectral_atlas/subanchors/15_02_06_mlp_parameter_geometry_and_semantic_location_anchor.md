---
anchor_id: 15_02_06_mlp_parameter_geometry_and_semantic_location
status: completed_location_without_commonality
canonical_language: en
companion_language: zh
thinking_card: 15_02_06_mlp_parameter_geometry_and_semantic_location_thinking_card_cn.md
parent_anchor: 15_02_layerwise_representation_spectral_atlas
updated: 2026-08-07
---

# A15_02_06 MLP Parameter Commonality And Attention-Write Semantic Location

Researcher judgment: [Chinese Thinking Card](15_02_06_mlp_parameter_geometry_and_semantic_location_thinking_card_cn.md). Protocol: [A15_02_06_E01](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E01_mlp_parameter_geometry_and_semantic_location/protocol.md).

## 1. Problem Definition

In frozen Qwen3-8B, is the high-gain input subspace of the MLP more shared across layers than its middle and tail subspaces, and does fine-relative-to-coarse semantic variance in each layer's isolated attention write move toward lower-gain local parameter ranks with depth in a way that survives RMSNorm, parameter gain, and the nonlinear MLP response?

This is a static parameter/representation audit. It does not test frequency, compositional depth, knowledge acquisition, causal necessity, Router utility, or training benefit.

## 2. Physical Priors

1. The isolated attention write $a_\ell$ is the direct output of `o_proj` before residual addition. It is newly written by layer $\ell$, but it is conditioned on the accumulated residual and is not information-theoretically pure new information.
2. The MLP receives $n_\ell=\operatorname{RMSNorm}_\ell(x_\ell+a_\ell)$, not $a_\ell$ alone. Its attention-induced input increment is $\Delta n_\ell=n_\ell-\operatorname{RMSNorm}_\ell(x_\ell)$.
3. Repeated common processing could make high-gain MLP input subspaces more aligned across layers, while lower-gain subspaces remain more layer-specific.
4. Raw variance occupancy can differ from effective response: small raw tail variance may be amplified, or raw tail enrichment may be suppressed by parameter gain and MLP nonlinearity.

## 3. Falsifiable Hypotheses

**H1, parameter commonality guard.** The equal-rank head input projector is more aligned across layer pairs than matched middle/tail projectors and a Haar-random equal-rank baseline. The conclusion must be stable for ranks 128, 256, and 512 and after folding the layer's post-attention RMSNorm scale into the effective parameter operator.

**H2, semantic location.** The fine-minus-coarse local parameter-rank centroid increases from blocks 1--12 to blocks 25--35 for the isolated post-`o_proj` write. Each layer has its own sorted parameter basis; this is a percentile redistribution, not a shared-vector trajectory.

**H3, effective-use guard.** The H2 direction survives (i) parameter-gain weighting, (ii) the actual MLP input increment $\Delta n_\ell$ in the native parameter basis, and (iii) broad-band nonlinear MLP response interventions.

**Strongest rival.** Apparent head commonality is scale or normalization geometry, while apparent semantic tail enrichment is a normalized low-energy residue that the MLP does not effectively transmit.

## 4. Mathematical Model

For MLP gate and up projections, define the native input Gram operator

$$
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell}
=V_\ell\Gamma_\ell V_\ell^{\top}.
$$

For an equal-rank band $k$ with projector $P_{\ell,k}$ and rank $r$, cross-layer overlap is

$$
O_{\ell m k}=\frac{\operatorname{tr}(P_{\ell,k}P_{m,k})}{r},
$$

whose Haar expectation is $r/4096$. Individual singular vectors are not compared. A normalization-folded control uses $K_\ell^{eff}=D_\ell K_\ell D_\ell$, where $D_\ell$ is the diagonal post-attention RMSNorm weight.

For semantic role $g\in\{coarse,fine\}$ with between-class covariance $B_{\ell,g}$, raw and gain-weighted band variance are

$$
E^{raw}_{\ell g k}=\frac{\operatorname{tr}(P_{\ell,k}B_{\ell,g})}{r},\qquad
E^{gain}_{\ell g k}=\frac{\operatorname{tr}(V_{\ell,k}\Gamma_{\ell,k}V_{\ell,k}^{\top}B_{\ell,g})}{r}.
$$

Normalize within role, $p_{\ell g k}=E_{\ell g k}/\sum_jE_{\ell g j}$, and define the local-rank centroid $C_{\ell g}=\sum_kp_{\ell g k}c_k$, where $c_k$ is the band's rank-percentile center. The primary metric is

$$
T_{eff}=\operatorname{median}_{\ell=25:35}(C^{gain}_{\ell,fine}-C^{gain}_{\ell,coarse})
-\operatorname{median}_{\ell=1:12}(C^{gain}_{\ell,fine}-C^{gain}_{\ell,coarse}),
$$

evaluated on the actual MLP input increment. H1 is a mandatory mechanism guard; raw-write and nonlinear-response versions are registered supporting tests.

## 5. Computational Realization

Freeze local Qwen3-8B: 36 blocks, hidden size 4096, MLP width 12,288. Divide each local parameter spectrum into 16 equal-rank bands of 256 directions: F1=head, F2--F8=middle, F9--F16=tail. Report rank-128/512 sensitivity and broad H/M/T aggregates.

Reuse the audited A15_02 semantic cube: 8 parents, 8 children per parent, 4 templates, and 2 fact bundles, totaling 512 balanced records with dataset identifier `cb440b98d81bac3f9813344f85e6efdbd994b7b988d8009ba64e207e64a11859`. Reuse cached post-`o_proj` states. Rerun only the identical records needed to capture $x_\ell$, $a_\ell$, $\Delta n_\ell$, and MLP responses.

For broad band $k\in\{H,M,T\}$, measure

$$
\Delta m_{\ell,k}=MLP_\ell(n_{old,\ell}+P_{\ell,k}\Delta n_\ell)-MLP_\ell(n_{old,\ell}),
$$

along with full $MLP(n_{old}+\Delta n)-MLP(n_{old})$ and the non-additivity residual.

## 6. Minimal Falsification Tests

1. Verify parameter shape, eigendecomposition residual, orthogonality, band energy conservation, and deterministic replay.
2. Compare projector overlap with equal-rank Haar expectation and wrong-band cross-layer controls; report adjacent and all-pair summaries separately.
3. Use the same balanced 512 records and population-weighted class covariance for coarse and conditional fine roles. Use one common within-child expression-noise covariance only as a reliability guard.
4. Keep raw occupancy, gain-weighted response, RMSNorm-folded coordinate control, actual $\Delta n$, and nonlinear $\Delta m$ separate.
5. Require paired hierarchical bootstrap over parent, child, and expression; block 36 is displayed but excluded from early/late primary contrasts.
6. Fail closed if post-`o_proj` replay does not match the frozen cache, if semantic energy is not conserved over 16 bands, or if the primary direction changes under the registered rank sensitivities without a stable broad-band interpretation.

## 7. Current Evidence

A15_02_E04 established that post-`o_proj` coarse and fine actual semantic variance is head-dominant in every block, while late fine-relative-to-coarse middle enrichment is modest and tail enrichment is not stable across calibration halves. That basis was each layer's natural-data covariance basis, not a parameter basis.

The senior parameter-spectrum report used $W_{gate}^{\top}W_{gate}+W_{up}^{\top}W_{up}$ and found broadly similar leaf/composite variance shapes. It did not test cross-layer projector commonality, coordinate-matched attention-induced MLP input increments, or balanced coarse/fine semantic location. Therefore it cannot answer H1--H3.

A15_02_06_E01 completed all registered jobs and guards. Native head/middle/tail-256 projector overlap is 2.20/1.04/3.26 times the equal-rank Haar expectation; RMSNorm-folded values are 2.05/1.13/7.04. H1 therefore fails: head exceeds middle, but tail exceeds head at ranks 128, 256, and 512.

Both semantic roles show a large descriptive right shift in local parameter rank. Raw-write coarse/fine centroids move from 0.342/0.353 in blocks 1--12 to 0.479/0.470 in blocks 25--35. After removing this common layer effect, raw-write fine-specific shift fails: $T=-0.0107$ with interval $[-0.0178,0.00447]$. The registered gain-weighted actual-input statistic passes at $T_{eff}=+0.01630$ with interval $[0.00599,0.02833]$, both template splits, 8/8 leave-one-parent contrasts, and all rank widths positive. The nonlinear H/M/T MLP response remains insufficient for effective use: $T=+0.00514$ with interval $[-0.00298,0.01620]$. The typed outcome is `location_without_commonality`; see the [summary](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E01_mlp_parameter_geometry_and_semantic_location/summary.md).

The shared-coordinate continuation separated three further questions. E02 found a positive early-to-late fine-only shift in the Mean Response basis ($+0.03171$) but not in the Rank Consensus basis ($-0.00755$, interval crossing zero), so the depth claim is `basis_sensitive_shift`. E03 then froze Mean Response and found an ordered trajectory-level coarse < medium < fine centroid; fine-minus-coarse is $+0.008175$ with interval $[+0.001964,+0.012620]$. Its post-hoc shape audit shows mostly overlapping coarse/fine curves: the average shift is a reduction at the spectrum head plus small distributed increases at later ranks, not one continuous semantic band. E04 rejects aligned later-spectrum growth for block 8→9, and E05 finds 16 positive, 11 negative, and 8 unresolved adjacent transitions under simultaneous correction. The all-depth outcome is `stage_dependent_nonmonotonic`.

Direct records: [E02](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E02_shared_parameter_basis_attention_projection/summary.md), [E03](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E03_shared_basis_semantic_granularity/summary.md), [E04](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E04_layer8_to9_shared_basis_growth/summary.md), and [E05](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/summary.md).

## 8. Claim Boundary And Next Decision

The completed sequence does not support the joint mechanism. H1 is refuted by stronger tail than head commonality; raw fine-specific location is absent; the gain-weighted actual-input metric passes; nonlinear effective use remains unconfirmed; and the shared-coordinate depth trajectory is basis-sensitive and non-monotonic. The retained statement is narrower: Mean Response is a valid descriptive parameter-response ruler on which semantic granularity is ordered in aggregate, but it does not identify one band or layer-added information.

Even a Pass supports only a frozen-model local-rank organization statement. It cannot identify token frequency, rare knowledge, knowledge-learning sites, causal necessity, a universal shared spectral identity, or a useful Router coordinate.

**One next decision:** close normalized Attention-write variance redistribution as the candidate definition of layer-added information and hand the question to A15_08's residual-relative held-out accessibility test. Completion requires one fixed old state, one named update, one frozen target, and matched held-out gain beyond old-state and target-independent controls; no Router experiment starts from this Anchor.
