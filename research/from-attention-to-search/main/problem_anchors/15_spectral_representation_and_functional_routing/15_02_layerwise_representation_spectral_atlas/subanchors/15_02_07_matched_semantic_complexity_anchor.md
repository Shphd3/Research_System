---
anchor_id: 15_02_07_matched_semantic_complexity
status: closed_insufficient_complex_specific_effect
canonical_language: en
companion_language: zh
parent_anchor: 15_02_layerwise_representation_spectral_atlas
updated: 2026-08-09
---

# A15_02_07 Matched Semantic Complexity In The Layerwise MLP Parameter Spectrum


## 1. Problem Definition

**Decision question:**

> In frozen Qwen3-8B, under separately matched taxonomy and controlled-composition tasks, does the attention-induced actual MLP-input increment make a complex target increasingly occupy later ranks of each layer's local MLP parameter spectrum and provide conditionally new linear information with depth?

The actual MLP-input increment is \(\Delta n_\ell=RMSNorm_\ell(x_\ell+a_\ell)-RMSNorm_\ell(x_\ell)\). Each layer's input-side MLP parameter operator is \(K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell}\), ordered from high to low parameter gain. Equal rank across layers is not vector identity.

The two semantic objects are adjudicated separately:

- **TAX:** matched eight-way simple between-parent tasks versus eight-way conditional-fine within-parent tasks.
- **COMP:** one-edge retrieval \(V\to C\) versus two-edge composition \(U\to V\to C\), with the same context and terminal code.

The question has two clauses: H1 asks where complex-relative between-class variance lies; H2 asks whether \(\Delta n_\ell\) supplies linear information beyond the old MLP input. Neither clause can rescue the other.

## 2. Physical Priors

1. If deeper attention writes add a complex distinction, a frozen readout that already sees the old MLP input should improve when given a correction from \(\Delta n_\ell\).
2. If that distinction is increasingly assigned to lower-gain local MLP directions, the complex-minus-simple normalized rank centroid should increase from early to late layers.
3. A target-common change in scale, normalization geometry, or local-rank occupancy predicts that simple and complex curves move together while their difference remains small.

These are frozen-model representation hypotheses. They do not imply information creation, native MLP use, or Router utility.

## 3. Falsifiable Hypotheses

**H1 — complex-specific local-rank relocation.** Within each branch, the complex-minus-simple normalized local-rank centroid increases from sampled early layers to sampled late layers.

**H2 — conditionally new linear information.** After a linear readout on the old MLP input is fitted and frozen, a fitted correction from \(\Delta n_\ell\) improves untouched confirmation loss more for the complex target than for the simple target, with a larger complex-minus-simple gain late than early.

**Strongest rival.** Matching removes covariance-cardinality and capability confounds, but depth still produces only a target-common geometric movement or linearly redundant information. It predicts H1 and H2 effects centered near zero, even when update-only readability is high.

TAX and COMP require separate verdicts. `Disc(\Delta n)`—a readout from the update alone—is supporting evidence and cannot establish H2.

## 4. Mathematical Model

For branch \(d\) and condition \(q\in\{simple,complex\}\), let \(B_{\ell,d,q}\) be the balanced between-class covariance of \(\Delta n_\ell\). In the local eigenbasis \(K_\ell=V_\ell\Gamma_\ell V_\ell^{\top}\), normalize the directional masses and compute the rank centroid \(m_{\ell,d,q}\). Define

\[
R_{\ell,d}=m_{\ell,d,complex}-m_{\ell,d,simple},
\]

and the H1 statistic

\[
T_{rank,d}=\operatorname{median}_{\ell\in\{25,29,33\}}R_{\ell,d}
-\operatorname{median}_{\ell\in\{1,5,9\}}R_{\ell,d}.
\]

For H2, fit a regularized linear readout on \(n_\ell^{old}\), freeze it, then fit only a \(\Delta n_\ell\) logit correction. Conditional information gain is

\[
CIG_{\ell,d,q}=CE^{conf}_{base}-CE^{conf}_{base+\Delta n}.
\]

Let \(G_{\ell,d}=CIG_{\ell,d,complex}-CIG_{\ell,d,simple}\) and apply the same sampled late-minus-early contrast to obtain \(T_{CIG,d}\). Both metrics are branch-internal difference-in-differences. H1 cannot prove accessibility; H2 cannot locate information in the parameter spectrum.

## 5. Computational Realization

- **Frozen model and layers:** Qwen3-8B at layers 1/5/9/13/17/21/25/29/33/36.
- **TAX:** 1,920 texts; eight paired eight-way tasks; 10 TRAIN, 10 DEVELOPMENT, and 10 CONFIRMATION expressions per leaf. Both conditions use eight labels and identical center counts.
- **COMP:** 3,072 records; 64 independent map episodes, eight terminal codes, two conditions, and three splits. The amended task passed restricted-choice capability at 0.9902 simple and 0.7578 complex.
- **Information roles:** TRAIN fits readouts, DEVELOPMENT selects regularization, and untouched CONFIRMATION supplies H1/H2. TAX tasks and COMP episode groups are the paired resampling units; layers and directions are not independent replicates.
- **Figures:** the required curves display raw and normalized directional variance for all ten layers, with smoothing used only for display. Verdicts use unsmoothed values.

TAX and COMP are never pooled. Complete data identities, Protocol amendments, hashes, and artifact lineage remain in their detailed records.

## 6. Minimal Falsification Tests

For each branch:

- **H1 Pass:** confirmation \(T_{rank}>0\), its paired-bootstrap 95% lower bound \(>0\), and DEVELOPMENT \(T_{rank}>0\).
- **H2 Pass:** confirmation \(T_{CIG}>0\) and its paired-bootstrap 95% lower bound \(>0\).
- **Fail:** the corresponding 95% upper bound is below zero under valid guards.
- **Insufficient:** the interval crosses zero, DEVELOPMENT reverses the required H1 direction, or a data/capability/reliability guard fails.

The joint semantic-refinement mechanism requires H1 and H2 Pass in the same branch. A shared simple/complex shift, update-only readability, or a visually ordered smoothed curve cannot substitute for either registered result.

## 7. Current Evidence

Both approved full runs completed and passed their validity guards, but neither branch supports the joint mechanism.

| Branch | H1: complex-specific rank shift | H2: conditionally new linear information | Verdict |
|---|---|---|---|
| TAX | \(-0.004690\), interval \([-0.012182,0.009295]\) | \(-1.09\times10^{-7}\) nats/example, interval \([-4.30\times10^{-7},5.92\times10^{-7}]\) | both insufficient |
| COMP | \(+0.002114\), interval \([-0.002384,0.005226]\); DEVELOPMENT \(-0.003608\) | \(+0.018523\) nats/example, interval \([-0.050412,0.081052]\) | both insufficient |

The [TAX result](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_07_E01_matched_taxonomy_full/summary.md) shows no stable fine-specific effect after matching class count and center precision. The [COMP result](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_07_E02_controlled_composition_full/summary.md) shows late update-only readability, but neither stable complex-specific relocation nor information linearly new beyond the old state.

The retained observation is target-common: simple and complex centroids both move substantially toward later local ranks, while their difference is small and non-monotonic.

## 8. Claim Boundary And Next Decision

- **Question:** Under separately matched TAX and COMP data, does a complex target increasingly occupy later local MLP-parameter ranks and gain conditionally new linear accessibility with depth?
- **Direct result:** No registered branch supports the joint claim. All H1/H2 intervals cross zero, and COMP H1 reverses between DEVELOPMENT and CONFIRMATION.
- **Updated judgment:** Complexity-specific semantic refinement is not supported as a stable parameter-rank shift or linearly new information. The retained object is target-common depthwise relocation and spectral-shape change.
- **Cannot claim:** These runs cannot establish absence of nonlinear information, functional tail use, native MLP use, shared semantic vectors, or nonlinear Router benefit. Lower fine readability alone does not imply nonlinear coding.
- **Exactly one next decision:** make A15_04 the close-out gate and permit only one geometry reanalysis on the existing fixed sample set: test whether target-common relocation aligns with a cross-layer shared parameter tail beyond equal-rank random, head, and middle spaces. Pass permits a separate function test; Fail closes the tail-functional interpretation. No new data, replication, intervention, or Router experiment is authorized here.
