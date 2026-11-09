---
anchor_id: 15_02_02_natural_hierarchy_role_localization
parent_anchor: 15_02_layerwise_representation_spectral_atlas
status: completed_e02_pass_layer_specific_role_selectivity
---

# A15_02_02 Natural Hierarchy Token Spectral Localization


## 1. Problem Definition

Current decision question: in frozen Qwen3-8B, with each layer's covariance basis fitted on independent natural text, does the same intermediate concept occupy reproducibly different covariance-rank locations when it acts as a parent versus a child? The experiment distinguishes actual projected energy from directional selectivity after dividing out each direction's background variance.

Covariance head, middle, and tail mean high-, intermediate-, and low-background-variance rank intervals within one layer. Equal rank names across layers do not imply equal semantic content.

## 2. Physical Priors

Background variance mechanically raises raw projection energy in head directions. A semantic-role-specific direction should therefore survive per-direction variance normalization, exact lexical and token-position pairing, template changes, chain resampling, and calibration half splits. A lexical, positional, or background-scale artifact predicts that raw differences disappear after whitening or change with templates.

## 3. Falsifiable Hypotheses

H1 predicts a stable parent-minus-child contrast in at least one coarse or fine rank band after background-variance normalization. The strongest rival predicts raw head differences without a stable whitened contrast. A second rival predicts isolated layer/template effects rather than a depth-stable mapping.

Pass requires a valid independent basis and a band effect that survives chain bootstrap, chain-label permutation, multiple templates, tail-floor sensitivity, and adjacent-layer or preregistered terminal-layer replication. Valid data with no such stable effect is Fail. Failed token pairing, basis stability, reconstruction, or tail sensitivity is Insufficient.

## 4. Mathematical Model

For layer \(\ell\), independent natural calibration states define

\[
\Sigma_\ell=U_\ell\Lambda_\ell U_\ell^\top.
\]

For centered target state \(x=h-\mu_\ell\), coefficient \(a_i=u_i^\top x\) has raw energy \(a_i^2\) and variance-normalized energy

\[
q_i=\frac{a_i^2}{\lambda_i+\epsilon}.
\]

For equal-rank band \(B\), both quantities are averaged per direction. The paired role effects are parent minus child, with 32 semantic chains as the inference unit. Raw effects measure actual activation energy; normalized effects measure selectivity beyond background variance. Neither is an expert-utility metric.

## 5. Computational Realization

The frozen local `/data/share/Qwen3-8B` model contributes the embedding output and every decoder-block output residual state. A fixed 128-document DCLM holdout slice supplies 65,536 independent calibration tokens. The existing 32 disciplinary chains are rendered into four same-target, same-token-position, equal-length parent/child template pairs. Covariance decomposition is offline and never enters model inference.

## 6. Minimal Falsification Tests

The decisive evidence is the layer-by-band same-concept parent-minus-child raw and normalized atlas. Guards include exact token/span/position matching, relation-before-target visibility, covariance reconstruction and energy conservation, calibration split-half overlap, paired label permutation, template consistency, eigenvalue-floor sensitivity, and chain-level support for any final-layer reversal.

## 7. Current Evidence

E01 used 32 disciplinary chains with a templated calibration corpus, nine Qwen depths, and a band-enrichment metric. It found no strict Qwen same-lexeme parent/child cell and rejected a universal cross-model rank mapping. See [E01 summary](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_02_E01_natural_hierarchy_role_localization/summary.md).

E02 fitted all 37 Qwen3-8B representation-site bases on 128 independent DCLM documents (65,536 tokens) and evaluated 128 exact-position parent/child pairs from the inherited 32 chains. All pair, replay, numerical, split-half, template, chain, permutation, and eigenvalue-floor guards passed.

The result is **Pass for layer-specific whitened role selectivity** and **Fail for a uniform parent=head rule**. Whitened head selectivity is child-greater-than-parent in ten blocks between 5 and 19, then parent-greater-than-child in every block 25--32. Representative paired parent/child ratios are 0.961 at block 10, 1.080 at block 29, and 0.915 at block 36. No raw or whitened H/M/T contrast passes the preregistered final-layer-only reversal rule. See [E02 summary](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_02_E02_qwen3_independent_role_atlas/summary.md).

## 8. Claim Boundary And Next Decision

E02 establishes only a Qwen3-8B-specific, layer-specific representation association. It does not establish that covariance rank causes semantics, that deeper layers perform composition, that a band should guide a Router, or that a band improves expert training. It also does not establish a universal hierarchy-to-rank map across models, languages, calibration corpora, or ontologies.

The sole next decision is whether to reproduce the early/intermediate child-head and late parent-head phases with an independent model or independently sampled natural-corpus basis. Only an externally reproduced layer-band coordinate may enter a separately approved functional-utility test.
