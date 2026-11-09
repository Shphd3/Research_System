---
anchor_id: 15_02_05_balanced_taxonomy_attention_write_atlas
status: completed_nonpositive_location_fail_pending_human_judgment
canonical_language: en
companion_language: zh
chinese_companion: 15_02_05_balanced_taxonomy_attention_write_atlas_anchor_cn.md
parent_anchor: 15_02_layerwise_representation_spectral_atlas
updated: 2026-08-09
execution_authorized: false
---

# A15_02_05 Coarse--Fine Semantic Layerwise Spectral Localization


## 1. Problem Definition

**Decision question:**

> In frozen Qwen3-8B, does a child concept's sibling-relative semantic residual acquire a reproducible depth-dependent spectral location, beyond the location of coarse parent distinctions, when both absolute strength and normalized allocation are audited; and is the aggregate result visible in preregistered child cases rather than created by averaging?

This is a representation-knowledge experiment. It does not implement or evaluate a Router, expert assignment, causal use, or training gain. It inherits only the A15_02 question of what layerwise semantic objects are present and where they lie in a named local spectrum.

The experiment must partially answer three linked questions:

1. **Aggregate location:** how do coarse and conditional-fine semantic contrast strength, normalized F1--F16 allocation, and their difference change with layer?
2. **Difference defects:** can an apparent fine-minus-coarse curve be explained by total-scale growth, normalization, unequal contrast counts, self-inclusion in the parent mean, expression noise, local-basis instability, or cancellation across children?
3. **Named semantic cases:** do `combinatorics - mathematics` and `linear algebra - mathematics` have reliable layerwise residuals, stable cross-layer correlation structure, and similar or distinct fine-semantic trajectories?

Here, a **coarse residual** is one academic-domain center relative to the other domain centers. A **conditional-fine residual** is one child-subfield center relative to the other child centers within the same domain. The latter is an operational sibling contrast, not a purified or causally isolated “fine feature.” The labels `child - parent` in figures are shorthand for this leave-one-child-out residual because the fixed bank contains child descriptions, not an independent set of parent-only descriptions.

The primary representation is the actual attention-induced change in the current block's MLP input,
\(\Delta n_\ell=\operatorname{RMSNorm}_\ell(h_\ell+a_\ell)-\operatorname{RMSNorm}_\ell(h_\ell)\), where \(a_\ell\) is the isolated post-`o_proj` attention write. This same-layer counterfactual subtraction is defined; subtraction of covariance matrices, RMS values, or eigenvectors from different layers is forbidden. The isolated write \(a_\ell\) is a source-boundary control only.

Each layer has its own DCLM activation-covariance eigenbasis, divided into 16 equal-rank bands. F1 is the highest-background-variance band, F2--F8 are middle, and F9--F16 are tail. Equal local ranks across layers are comparable percentiles, not the same direction.

The approved and frozen data bank has exactly 512 label-free descriptions: 8 parent domains, 8 child fields per parent, and 8 expressions per child. To include both requested mathematics cases while retaining 512 records, the approved new manifest replaces the old `algebra` child with `linear algebra`. This is not literal record-for-record reuse of the earlier 512-record bank. Treating `linear algebra` and `combinatorics` as same-level children is an operational grouping, not evidence that they have equal taxonomy depth or semantic distance.

Pass supports only a bounded statement about layerwise spectral localization in this model and bank. Fail weakens a fine-specific relocation claim. Insufficient leaves the question open. No outcome authorizes a Router experiment automatically.

## 2. Physical Priors

1. **Granularity-location prior.** If deeper layers organize within-domain distinctions differently from between-domain distinctions, conditional-fine residuals should change their normalized local spectral location relative to coarse residuals. The exposing variable is the layerwise fine-minus-coarse F1--F16 allocation; a shared trajectory falsifies fine specificity.
2. **Absolute-and-relative prior.** A normalized shift has semantic-strength meaning only when the underlying contrast is reproducible across independent expression halves. Absolute per-direction cross-expression energy exposes this requirement. A normalized shift at the absolute reliability floor is an artifact or insufficient evidence, not “more fine information.”
3. **Aggregate-to-case prior.** A general fine-semantic trajectory should not be carried by one parent or disappear in preregistered child cases. Leave-one-parent-out results and named-case split-half correlations expose this prior. Failure yields an aggregate-heterogeneity conclusion, not a universal fine coordinate.

## 3. Falsifiable Hypotheses

The following operational definitions and verdict rules were confirmed and frozen in Protocol revision `A15_02_05_E01_r1` before execution.

**H1 — Fine-specific depth localization.** After matched contrast counts and reliability guards, the conditional-fine minus coarse local-rank centroid becomes more rightward from early to late layers in \(\Delta n\).

**H2 — Non-artifactual difference.** Any H1 effect survives parent-preserving child-label permutation, expression-half and calibration-half replication, and leave-one-parent-out analysis; full absolute and normalized F1--F16 curves identify whether it is absolute growth, relative reallocation, or internal cancellation.

**H3 — Named-case structure.** `combinatorics - mathematics` and `linear algebra - mathematics` each have positive split-half reliability in eligible layers. Their cross-layer direction and 16-band-profile correlation maps determine whether the aggregate trajectory is case-concordant, child-specific, or average-only. H3 is a typed diagnostic and cannot rescue failed H1.

**Strongest rival — common amplification plus heterogeneous averaging.** Depth amplifies or reorients all academic semantics together; normalization and averaging across unlike children create a smooth fine-minus-coarse curve. This rival predicts weak or null H1 after controls, or an aggregate effect that is absent or contradictory in named cases.

**Pass:** H1 and all H2 validity guards pass. The result is typed `case_concordant` or `aggregate_heterogeneous` from H3 rather than forcing one pairwise story. **Fail:** reliable evidence gives a nonpositive fine-specific depth interaction, or the observed interaction does not exceed the registered taxonomy/null controls. **Insufficient:** data identity, absolute semantic reliability, basis replication, numerical reconstruction, or precision fails. An interval that crosses zero is insufficient, not a negative claim.

## 4. Mathematical Model

Let \(y_{\ell i}\) be record \(i\)'s primary \(\Delta n_\ell\) representation; replay the same analysis on \(a_\ell\) only as a source-boundary control. For expression half \(s\), parent \(p\), and child \(c\), the coarse contrast is \(u^s_{\ell p}=\mu^s_{\ell p}-\mu^s_{\ell,-p}\) and the conditional-fine residual is \(r^s_{\ell pc}=\mu^s_{\ell pc}-\mu^s_{\ell p,-c}\). Because sibling residuals share a reference and sum to zero up to weighting, their mutual cosine must be compared with matched within-parent child pairs rather than zero.

Let \(P_{\ell k}\) be the 256-direction projector for F\(k\). Absolute cross-expression energy \(A^\times_{\ell gk}\) is the mean of \(v^{A\top}P_{\ell k}v^B\) divided by 256; its unit is activation squared per direction, and it measures reproducible contrast strength rather than causal use. Normalized allocation \(q_{\ell gk}\) averages squared projected energy from both expression halves and divides by all-band energy; it sums to one and cannot establish absolute growth. With band midpoint \(m_k=(k-0.5)/16\), define \(\rho_{\ell g}=\sum_km_kq_{\ell gk}\). The one primary metric is

\[
T_{\rho}
=\operatorname{median}_{\ell\in L_{late}}(\rho_{\ell F}-\rho_{\ell C})
-\operatorname{median}_{\ell\in L_{early}}(\rho_{\ell F}-\rho_{\ell C}),
\]

where \(L_{early}=\{1,\ldots,12\}\) and \(L_{late}=\{25,\ldots,35\}\); block 36 is reported separately. \(T_\rho\) is a normalized local-rank-percentile interaction. It cannot identify a shared vector or distinguish strength growth from redistribution without \(A^\times\). Named-child stability is the average cross-expression cosine across two layers; same-layer child-pair cosine is compared with all mathematics child pairs, and a separate matrix correlates their 16-band profiles. These describe case stability and similarity, not population generality.

## 5. Computational Realization

Freeze Qwen3-8B (36 blocks, width 4096). At each common readout position, capture \(h_\ell\), isolated \(a_\ell\), and actual normalized MLP input, then replay \(\Delta n_\ell\). Fit no model, probe, Router, or expert parameter.

The frozen 512-record bank has eight academic domains, eight children per domain, four templates, and two disjoint fact bundles. The same states receive coarse and conditional-fine metadata offline. Mathematics includes both requested cases, with `linear algebra` replacing `algebra` under the approved new-manifest option. Every description omits parent and child labels.

To prevent a 64-versus-8 contrast-count artifact, eight frozen rotations each select one child per parent, covering all 64 children once; every fine estimate is compared with eight coarse parent contrasts under the same aggregation. Root families, not prompts or layers, are the unit of semantic independence.

Independent DCLM activations define one full and two calibration-half bases per layer/site; F1--F16 are frozen before semantic projection. Parent-preserving child-label permutations and same-dimensional Haar partitions control semantic grouping and rank partition. Statistics use unsmoothed directions. Required evidence is the absolute/normalized layerwise atlas, full-band and per-direction cancellation views, named-case direction/profile correlations against the mathematics-pair envelope, and one defect table.

The named-case figures can answer whether the operational residual is stable and whether cases agree. They cannot answer whether an independent `mathematics` concept vector was subtracted, because no parent-only state exists in this bank.

## 6. Minimal Falsification Tests

The decisive comparison is the \(\Delta n\) fine-minus-coarse depth interaction \(T_\rho\) under matched contrast counts.

1. **Data and numerical gate:** exactly 512 balanced, label-free records; frozen manifest; exact site identity; \(\Delta n\) replay and projection-energy reconstruction within the Protocol tolerances.
2. **Absolute reliability gate:** coarse and fine \(A^\times\) are positive with a root-bootstrap lower bound above zero in both early and late windows. A normalized curve without this gate is Insufficient.
3. **H1 primary test:** the 95% hierarchical-bootstrap lower bound of \(T_\rho\) is above zero, the point estimate exceeds parent-preserving permutation q95, both expression halves and both calibration-half bases are positive, and no leave-one-parent-out estimate reverses sign.
4. **H2 defect audit:** the complete absolute and normalized F1--F16 curves, matched rotations, Haar partitions, and per-direction views must be reported. A positive \(T_\rho\) with no absolute increase is typed `relative_reallocation_only`; a null centroid with stable opposing band changes is typed `redistribution_without_centroid_shift` and does not pass H1.
5. **H3 named cases:** both requested mathematics cases require positive same-layer split-half reliability before their cross-layer cells are unmasked. Agreement with H1 yields `case_concordant`; disagreement yields `aggregate_heterogeneous`. Neither changes the H1 verdict.

The main falsifier is reliable absolute coarse and fine structure with a nonpositive or null-controlled \(T_\rho\). The minimum counterexample to an apparently smooth aggregate curve is an aggregate Pass whose two preregistered cases are unreliable or trend in opposite directions.

## 7. Current Evidence

Earlier post-`o_proj`, parameter-rank, and natural-hierarchy atlases motivated a balanced sibling-relative activation test but did not establish fine-specific localization. A15_02_05_E01 has now completed the frozen `A15_02_05_E01_r1` Protocol with eligible data, tensor, basis, reliability, resampling, numerical, and visual evidence.

The registered result is `nonpositive_location_fail`. In actual \(\Delta n\), the paired fine-minus-coarse centroid changes from +0.009334 in blocks 1--12 to -0.000239 in blocks 25--35, so \(T_\rho=-0.009573\) with registered one-sided 95% lower/upper bounds [-0.011199, -0.004492]. Both expression halves, both calibration-half bases, and all eight leave-one-parent-out estimates are negative. Absolute coarse and fine contrasts are nevertheless reliable in both windows, so the Fail is not absence of a measurable semantic residual.

The isolated attention write has descriptive \(T_\rho=+0.011327\), which shows that the relocation sign is representation-site dependent and cannot be promoted from post-`o_proj` output to the actual MLP-input increment. The two named mathematics residuals are reliable and individually move rightward, but their 16-band profiles remain highly similar while their same-layer and cross-layer directions are weak or unstable. This types the named-case evidence as `aggregate_heterogeneous`; it does not rescue H1. See the [result summary](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/summary.md) and [complete evidence record](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/detailed.md).

## 8. Claim Boundary And Next Decision

This Anchor now rejects the claim that conditional-fine residuals receive an extra depth-dependent rightward local-rank relocation beyond coarse parent residuals at the actual \(\Delta n\) site in this model and bank. It retains three narrower facts: coarse and fine residuals are reproducibly present and strengthen with depth; the sign changes at the isolated-write boundary; and stable-looking band profiles do not imply stable semantic directions.

The result does not establish information creation, general semantic complexity, a pure child-minus-parent feature, attention or MLP causal use, cross-layer eigenvector identity, a universal middle/tail meaning, Router compatibility, expert utility, or training benefit. It does not rule out other layerwise semantic organizations or a separately defined middle object.

**One next decision:** stop treating any fixed band or normalized rank shift as conditional novelty and pass the named update to A15_08's residual-relative held-out accessibility gate. Completion requires fresh held-out target gain beyond the old-state readout and matched target-independent controls; do not start a Router experiment from this atlas.
