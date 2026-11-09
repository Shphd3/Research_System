# Protocol: A15_17_E04 Layer-8 Attention-Sidecar Representation Trajectory

Primary Anchor: [A15_17](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md)

Protocol status: `RECOVERED_FROZEN_CONTRACT`

Execution approval: human-confirmed in the controlling conversation before eligible computation; one single-node four-RTX5090 Spot Smoke and, after Smoke PASS, one full read-only analysis run.

Freeze note: this is a collision-safe relocation of the S7-only contract that was recorded before eligible computation in the former E03 Appendix A01/A02. A concurrent workflow later reused E03 for a different multi-model matrix. E04 preserves the earlier S7 contract and evidence without overwriting that workflow. No condition, checkpoint, metric, or interpretation was selected from the result when creating this file.

## 1. Purpose

Determine how the newly trained language model with one width-30,000, Top-32 sparse-autoencoder sidecar on the eighth transformer's raw Attention output evolves from 0 to 10B valid prediction tokens, and whether any apparent domain organization survives removal of the dominant fit-only representation direction.

## 2. Hypothesis

If the layer-8 sidecar changes residual domain organization rather than only a dominant common direction, the sidecar model will show a coherent Dense-relative trajectory in paired Fisher geometry or frozen linear-readout accuracy on both the controlled synthetic panel and the natural academic panel, and at least part of that difference will survive the fit-only centered first-direction removal.

The strongest rival is that visible differences come from one high-variance common direction, template-specific structure, training-trajectory noise, or a local reconstruction objective that changes geometry without improving accessible semantic organization.

## 3. Analysis Method

1. Compare the Dense control `M0` with the layer-8 sidecar model `S7` at exactly 0, 0.5, 1, 3, 5, and 10B cumulative valid prediction tokens. Use the same frozen P and N rows, row identities, fit/tune/report partitions, tokenizer, and anatomical final representation.
2. Report raw coordinates, fit-only centering, removal of the uncentered fit-matrix first singular direction, and `B3`: fit-only centering followed by removal of the centered fit-matrix first singular direction. Select each linear probe's regularization strength on the raw fit/tune coordinates and reuse it unchanged for all transformed coordinates.
3. Keep representation accessibility, covariance geometry, sparse contribution shares, reconstruction quality, local objective gradients, and token-aligned training loss as separate evidence surfaces. Use paired, stratum-preserving report-row bootstrap intervals for Dense-relative coarse Fisher and probe differences.

## 4. Registered Outcome Reading

- `difference observed`: a numerical paired difference is present, with its interval and panel/checkpoint scope stated.
- `no eligible difference detected`: the paired interval includes zero or the pattern is not coherent across the registered panels/checkpoints.
- `insufficient`: any checkpoint identity, row alignment, hook, immutability, finite-value, structural-gradient-zero, or artifact-completeness guard fails.

This is an estimation audit, not a thresholded model-selection trial. A readable sparse code, lower reconstruction error, or visually separated embedding cannot by itself establish functional use, semantic feature identity, language-model benefit, or causal specialization.

## 5. Frozen Objects

- Treatment: `S7`, one sidecar at zero-indexed block 7, after `W_O` and before residual addition.
- Control: qualified Dense `M0` caches on the same rows and token coordinates.
- Checkpoints: 0, 0.5, 1, 3, 5, and 10B valid prediction tokens.
- P panel: 360 controlled rows; family-disjoint 120/60/180 fit/tune/report; last valid token.
- N panel: 1,200 M2D2 academic rows; 600/200/400 fit/tune/report; mean over positions 0--255.
- Gradient unit: four frozen class-balanced fit batches; full node and deterministic 32-position support reported separately.
- Uncertainty unit: one report row, paired between `M0` and `S7`; checkpoints are not independent replications.
- Execution: analysis only, zero optimizer updates, no checkpoint mutation.

## 6. Required Artifacts

The required output is PNG and SVG for topology, readability, paired differences, fixed-atom contribution trajectories including 0B, variance distributions, full/support gradient geometry, raw/B3 Fisher trajectories, reconstruction health, token-aligned training losses, joint PCA/UMAP/t-SNE views, endpoint spectrum, and sidecar-internal variance. Every quantitative figure must have a local source table or an explicit raw-cache lineage.

## 7. Claim Boundary

Eligible claims are limited to representation accessibility, covariance organization, reconstruction behavior, and local objective-gradient geometry for this seed and these panels through 10B tokens. The experiment cannot establish native use of sparse features, causal language-model improvement or harm, stable atom semantics, expert specialization, or generality across seeds or model scales.

## 8. Execution And Analysis Amendments

### A01 — Offline tokenizer runtime repair before evidence

Smoke job `pt-aafi4o85` stopped after hardware preflight because the base image did not expose the frozen tokenizer dependency. It produced no cache, gradient record, or scientific metric. The next Smoke sourced the already qualified mounted Transformers 4.53.3 runtime while retaining the registered PyTorch 2.8/CUDA 12.8 layer. Scientific scope and computation were unchanged.

### A02 — Probe comparability repair after collection

The first synthesis implementation reselected linear-probe regularization independently after each coordinate transform. The established analysis flow requires selecting it on raw coordinates and reusing it for B1/B2/B3. The final `analysis_v2` restores that rule from the same immutable caches and row splits. No condition, feature, checkpoint, label, or metric was added or removed; all non-probe tables and figures are byte-for-byte inherited from the successful full run. This is an eligibility repair, not a result-selected analysis.

### A03 — Collision-safe result placement

The shared E03 path contains a separate concurrent multi-model result. The S7-only result is therefore recorded as E04. The raw execution workspace, job IDs, source hashes, and output hashes remain unchanged and are recorded in `execution_receipt.md` and `detailed.md`.
