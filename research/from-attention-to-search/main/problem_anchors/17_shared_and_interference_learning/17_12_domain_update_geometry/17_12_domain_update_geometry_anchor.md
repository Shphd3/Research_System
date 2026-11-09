# Anchor: common and domain-specific update geometry

Status: **AUTHORIZED_ANALYSIS_DESIGN; results NOT RUN**. Problem key `domain_update_geometry`. [Focus](../../../focus/focus_domain_update_geometry.md) · [Protocol](../../../experiments/A17/17_12_domain_update_geometry/20260930/protocol.md) · [中文](17_12_domain_update_geometry_anchor_cn.md). The researcher accepted the domain-first question and delegated its complete SVD/SAE analysis and necessary four-H100 Reserved execution on 2026-09-29. Numerical choices are AI operationalizations within that authorization; no future scientific verdict is implied.

## 1. Problem Definition

**At fixed S7, can predefined academic-text domains predict reproducible differences in local update demand beyond a pooled mean, and how are those differences represented in spectral structure and trained SAE activation patterns?** The long-term problem is evidence for sharing parameters. A preceding natural-NTP pair predictor did not generalize; this neither establishes an unstructured target nor proves absent representation information. The present uncertainty is whether the update target has repeatable domain-associated structure worth subsequently predicting.

One observational experiment examines the final attention output matrix at the exact 33B-training-token checkpoint, four academic domains and their historical fit/readout text panel. Single-target gradients are primary; a fixed 16-target mean diagnoses aggregation. A domain prototype that improves heldout gradient prediction supports a bounded domain association; qualified non-improvement weakens this grouping; failed measurement or unresolved precision leaves the question open. Every SVD and SAE diagnostic remains required regardless of the primary outcome. Finite-step loss, causally isolated semantics, router construction and long-term shared/separate training are outside scope.

## 2. Physical Priors

**Accepted research hypothesis, not an established fact:** the common natural-NTP objective may induce a pooled update component, while domain-conditioned contexts and targets may induce repeatable deviations. Domain labels are explanatory variables fixed independently of gradients. Neither equal domain nor common activation guarantees aligned learning. Failure of domain deviations to reproduce on other records would weaken this grouping without denying all language structure.

## 3. Falsifiable Hypotheses

**Primary H1:** a fit-domain mean gradient predicts readout gradients more accurately than the fit-pooled mean. The strongest rival is that domain appearance/activation differs but repeatable updates are adequately described by the pooled mean; apparent differences are finite-record fluctuations or magnitude effects.

Dependent diagnostics: H2 asks whether common, between-domain and within-domain update geometry has reproducible spectral concentration beyond a common mean or large norms. H3 asks whether common/specific activation patterns replicate and whether fit-selected SAE decoder spans capture relevant update components beyond equal-rank random directions. H4 asks whether fixed within-record aggregation improves domain association more than matched random grouping. These can fail independently. Low effective rank is not necessary for a domain association; SAE activity is not itself gradient attribution.

## 4. Mathematical Model

For record i and causal output position t, c is the input to W, a=Wc its output, e is the pure full-vocabulary NTP derivative with respect to a, and the residual stream remains record-specific. With only this final-block matrix observed, each target contributes G_it=e_it c_it^T. Use the last target G_i and the mean of 16 preselected target gradients G_i^(16); never form a gradient from separately averaged c and e. Flatten a gradient as g. The sample Gram matrix is

\[
K_{ij}=\langle G_i,G_j\rangle_F,\qquad
K=\mathcal G\mathcal G^\top=(CC^\top)\odot(EE^\top)
\]

for the single-target factorization. The aggregated Gram uses the actual summed outer products. K is positive semidefinite; its entries can be negative. Its singular-value geometry describes gradients, not the same object as representation geometry. Ordinary common-step SGD has first-order cross effect −ηK; actual finite loss is not measured here.

Fit records define a pooled mean μ, domain means μ_s and deviations δ_s=μ_s−μ. This separates a common vector, domain differences and within-domain residuals. The primary dimensionless heldout score is

\[
Q_D=1-\frac{\sum_{j\in R}\|g_j-\mu_{s_j}\|^2}
{\sum_{j\in R}\|g_j-\mu\|^2}.
\]

It can be computed from K without materializing all single-target gradients. Raw/centered/unit-gradient spectra have different meanings. Gram eigenvalues equal squared singular values; coordinates are Z=UΛ^(1/2). Fit bases are transferred to readout records rather than comparing independently fitted axes. With four domain means, between-domain rank is at most three by construction, not a low-rank discovery.

The frozen SAE encodes native a: z=E_SAE(a), reconstruction D z+b. Common atoms must fire in every domain with similar frequencies and positive amplitudes; specificity means enrichment, not exclusivity. Fit-selected decoder columns yield an orthogonal output-space projector P. Then G_P=P G and

\[
K_{ij}=\langle PG_i,PG_j\rangle_F+
\langle(I-P)G_i,(I-P)G_j\rangle_F.
\]

This is an exact gradient-row-space decomposition, not a causal SAE intervention or proof that a feature drove an update. Spans from different atom sets can overlap and are not additive across sets. Native/SAE reconstruction error and residual sensitivity are recorded.

## 5. Computational Realization

Use the verified fresh S7 reconstruction-coefficient 0.1 checkpoint, 281,431,040 backbone parameters, exact 33B training tokens; W=`model.blocks[7].attn.o.weight`, shape 1024×2048. The trained sidecar has 30,000 atoms and TopK32, observes the native 1024-dimensional attention output, and does not replace the forward path. Measure pure NTP only; no SAE auxiliary loss, optimizer update or retraining.

Reuse the 1,024-record [historical domain panel](/data/250010109/MoE_Router/experiments/20260925_sae_domain_activation/selected.jsonl): computer science, mathematics, physics and biology; two source subfields per domain, 64 records/subfield/split. This panel is already exposed and lacks paper IDs. New 33B measurements have a fit/readout separation but are **bounded descriptive replication**, not untouched confirmation or universal semantic evidence. Old 21B activations and old MLP-gradient results cannot serve as current measurements.

Three stages implement the Focus: capture same-record activations/gradients; quantify pooled/domain/within geometry and aggregation controls; audit all atoms and their update-space correspondence. SVD uses the pooled fit coordinate system; all-atom tables precede any illustrative selection. Activation analysis covers positive frequency, unconditional/conditional amplitude, spread/quantiles, positional profiles, persistence, coactivation, full-pattern similarity and reconstruction quality. Common/specific sets are selected using fit activation alone, before readout gradient interpretation, and measured regardless of primary Q_D.

Reuse the inspected 0930 S7 loader/capture/full-vocabulary tail, adapting positions and batched targets. Reuse domain metadata and trained decoder identity. Reject the old 21B caches, binary vocabulary tail, fixed background residual and atom selection using outcome gradients. Exact algorithms, thresholds, source hashes, outputs and budget belong to the Protocol.

## 6. Minimal Falsification Tests

Primary comparison: fit-domain versus fit-pooled gradient prototypes on the 512 readout records, single target. Bootstrap both fit and readout records within eight source subfields; use a balanced fit-label permutation control. **Support** requires the 95% interval lower bound for Q_D>0 and permutation p≤0.05; **non-support** requires a qualified interval upper bound≤0; otherwise **insufficient** for the directional primary claim. This zero threshold tests reproducible association, not a practical router-benefit threshold. Historical exposure and record-only independence bound every branch.

Unit-gradient prototypes distinguish direction from magnitude. Two source-subfield transfer comparisons and target/loss/norm diagnostics delimit lexical/source alternatives. Fixed-16-target and matched random grouping investigate scale. Spectral transfer and equal-rank random projector controls distinguish static concentration from reproducible update coverage. SAE activation equivalence and enrichment are tested separately from projected gradient capture; an empty set is a valid result, not permission to loosen thresholds. Secondary findings cannot overturn the primary outcome.

## 7. Current Evidence

[Natural-NTP prediction](../../../experiments/A17/17_11_natural_ntp_representation_compatibility/20260930/summary_cn.md): full-c Q=−0.000138, conditional 95% interval [−0.002768,0.002294]; the registered 5% predictive-gain claim was not supported. That fixed predictor result is preserved.

[Earlier domain activation](../../../experiments/A17/17_12_domain_update_geometry/historical_support/sae_domain_activation/20260925/summary_cn.md) demonstrated domain-associated activity on this panel at 21B, but not semantic purity or update prediction. [Same-panel 21B MLP update](../../../experiments/A17/17_12_domain_update_geometry/historical_support/structure_update/20260926/summary_cn.md) found all 12 cross-domain average directions helpful; that different checkpoint/matrix does not answer the current question. Large raw representation energy previously came mostly from a mean vector, motivating the centered/raw distinction.

Current 33B domain K, its spectra, current SAE activation patterns and atom-gradient span comparisons are **NOT RUN**. File availability and algebra are not empirical findings.

## 8. Claim Boundary And Next Decision

At most this analysis supports or weakens reproducible domain-associated local update structure in the specified historically exposed panel, with descriptive spectral and SAE correspondences. It cannot identify semantic causation, prove irreducible information limits, call every leading direction common, infer SAE feature causal use, or justify expert separation. The source/paper and lexical confounds remain explicit.

One next decision, owned by the researcher after all required outputs: whether a reproducible domain/activation update structure merits a new prospective representation readout, or whether grouping/scale should change. Completion requires the primary comparison plus every mandatory diagnostic with provenance and named failures. Resume from the Protocol and execution receipt; no old frozen judgment is rewritten.
