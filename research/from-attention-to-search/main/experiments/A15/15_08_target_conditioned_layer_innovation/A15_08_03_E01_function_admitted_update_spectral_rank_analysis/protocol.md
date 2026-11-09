---
experiment_id: A15_08_03_E01_function_admitted_update_spectral_rank_analysis
status: COMPLETED_2026-08-16
anchor: ../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_03_function_admitted_update_representation_rank_anchor.md
depends_on: ../A15_08_02_E01_layerwise_conditional_fine_added_accessibility
created: 2026-08-16
approved: 2026-08-16
execution_authority: FULL_LOCAL_EXECUTION_APPROVED_2026-08-16
---

# Protocol: A15_08_03_E01 Cross-Layer Update Spectrum, Rank, And Token Geometry

## 0. Approval And Scope

The researcher authorized experiment two in the same 2026-08-16 turn as the complete experiment-one run. This Protocol executes even when experiment one has negative, unresolved, or mixed layer outcomes. Geometry is computed for every extraction-eligible block; task-related language is restricted to experiment-one function-admitted layers.

One decision question:

> Across eligible Qwen3-8B blocks, how do the same-token residual updates differ in local-MLP parameter-spectrum activation, frozen common-parameter-spectrum location, token-cloud representation rank, cross-layer token geometry, and low-dimensional functional retention?

No Router, expert, model training, checkpoint change, commit, push, or external publication is authorized.

## 1. Frozen Input And Object

Reuse experiment one's exact model, record order, splits, token site, extraction arrays, TRAIN residualizers, base logits, folds, mismatch maps, and confirmation opening. For sample \(i\) at block \(\ell\),

\[
R_{U,\ell,i}=U_{\ell,i}-\widehat m^U_\ell(X_{\ell,i}).
\]

Remove only the TRAIN parent mean:

\[
\widetilde R_{\ell,i}=R_{U,\ell,i}-\mu^{tr}_{\ell,p(i)}.
\]

Do not subtract child means. Blocks with invalid extraction or undefined residualization stay visibly ineligible; no replacement layer is selected.

## 2. Three Analysis Coordinates

### 2.1 Layer-local MLP parameter spectrum

For every block, construct in float32 and eigendecompose in descending order

\[
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}
+W_{up,\ell}^{\top}W_{up,\ell}
=B_\ell\Gamma_\ell B_\ell^\top.
\]

Split the 4,096 directions into sixteen fixed bands of 256 ranks, F1 through F16. For split \(s\),

\[
e^{local,s}_{\ell,j}
=\operatorname{Var}_{i\in s}
\left(b_{\ell,j}^{\top}\widetilde R_{\ell,i}\right),
\qquad
E^{local,s}_{\ell,b}=\sum_{j\in b}e^{local,s}_{\ell,j}.
\]

Report raw total energy, normalized band shares, the dominant band \(\arg\max_bE_{\ell,b}\), and the full-spectrum rank centroid. Dominant band is descriptive; local equal rank is not cross-layer direction identity.

### 2.2 Frozen common parameter spectra

Reuse without refitting:

`/data/250010109/MoE_Router/experiments/20260811_a15_02_06_shared_parameter_basis_attention_projection/runs/a15-02-06-e02-20260811-shared-basis/arrays/shared_bases.pt`

Frozen SHA-256:

`11eb40144cafbc12c77c9043efd982d1da9018fe876a063fbb7250914480f532`

The primary common coordinate is `mean_response`, obtained from the equal-layer average of trace-normalized \(K_\ell\). `rank_consensus`, obtained from a rank-weighted average of local-band projectors, is the mandatory basis-sensitivity control.

For basis \(v\in\{MR,RC\}\), normalize direction energy within each layer and split:

\[
p^v_{\ell,j}=e^v_{\ell,j}/\sum_ke^v_{\ell,k},
\qquad
C^v_\ell=\sum_jp^v_{\ell,j}\frac{j-1/2}{4096}.
\]

Raw trace is reported separately. A later centroid is a relative spectral relocation, not more new information.

### 2.3 Token covariance space

Stack TRAIN rows as \(M^{tr}_\ell\) and compute its thin SVD. Equivalently,

\[
C^{tr}_\ell=(M^{tr}_\ell)^\top M^{tr}_\ell/(n-P).
\]

Report normalized effective rank, stable rank, and

\[
r^{rep}_{80,\ell}=\min\left\{r:\sum_{j\le r}\lambda_{\ell,j}/\sum_k\lambda_{\ell,k}\ge0.8\right\}.
\]

The identifiable cap is \(n-P\), not hidden width. Freeze TRAIN projectors and apply them unchanged to DEVELOPMENT and CONFIRMATION.

## 3. Primary Hypotheses And Typed Outcomes

Freeze early blocks \(\mathcal E=\{2,\ldots,12\}\) and deep blocks \(\mathcal D=\{25,\ldots,35\}\). Block 36 is displayed as a terminal boundary but excluded from the trajectory contrast.

\[
\Delta_T=\operatorname{median}_{\ell\in\mathcal D}T_\ell-
\operatorname{median}_{\ell\in\mathcal E}T_\ell,
\]

\[
\Delta_C^{MR}=\operatorname{median}_{\ell\in\mathcal D}C^{MR}_\ell-
\operatorname{median}_{\ell\in\mathcal E}C^{MR}_\ell.
\]

Use the same 2,000 paired parent/semantic-family bootstrap draws as experiment one and max-statistic simultaneous intervals.

- `BOTH`: both simultaneous 95% lower bounds exceed zero.
- `FUNCTION_ONLY`: only \(\Delta_T\) passes.
- `SPECTRAL_SHIFT_ONLY`: only \(\Delta_C^{MR}\) passes.
- `NEITHER`: both simultaneous 95% upper bounds are at most zero.
- `INSUFFICIENT`: any decisive interval crosses zero or a mandatory guard fails.

If Mean Response passes but Rank Consensus does not pass the same positive criterion, append `BASIS_SENSITIVE`. The local dominant band cannot create a Pass.

## 4. Representation-Low-Rank Test

For each eligible block:

1. require \(r_{80}^{rep}/(n-P)\le0.10\);
2. require real \(r_{80}^{rep}\) below q05 of 512 coordinate-independent TRAIN row-shuffle nulls;
3. require the TRAIN \(r_{80}^{rep}\) projector to retain at least 75% of total centered variance on both DEVELOPMENT and CONFIRMATION;
4. report all components separately, so a failed conjunction names its failed guard.

The null preserves each coordinate's marginal values and independently permutes its token rows. Null seeds and all permutations freeze before reading confirmation geometry.

## 5. Cross-Layer Token Geometry

For the same ordered, parent-centered records, use token Gram matrices

\[
G_\ell=M_\ell M_\ell^\top
\]

and linear centered-kernel alignment

\[
CKA(\ell,m)=
\frac{\langle HG_\ell H,HG_mH\rangle_F}
{\|HG_\ell H\|_F\|HG_mH\|_F}.
\]

Compute complete 35-by-35 TRAIN, DEVELOPMENT, and CONFIRMATION matrices, adjacent-layer curves, and paired bootstrap intervals. CKA measures token-relation similarity, not rank or function.

## 6. Low-Dimensional Functional Retention

Candidate ranks are

\[
r\in\{1,2,4,8,16,32,64,128,256,512\}
\]

up to the identifiable cap. For every eligible block and rank, project \(R_U\) through the TRAIN PCA projector, preserve experiment one's bit-identical frozen base logits, fit the same parent-specific centered-one-hot ridge correction, and select its penalty only on DEVELOPMENT.

For full-update gain \(G_{\ell,full}\) and projected gain \(G^{PCA}_{\ell,r}\),

\[
D^{func}_{\ell,r}=G^{PCA}_{\ell,r}-0.8G_{\ell,full}.
\]

Freeze 64 equal-rank Haar subspaces per block/rank. A function-admitted layer has low-dimensional functional retention only if some registered rank has a simultaneous 95% lower bound for \(D^{func}_{\ell,r}\) above zero and its projected gain exceeds the q95 equal-rank Haar gain. All-layer rank-gain curves are computed regardless of experiment-one outcome; only \(\mathcal L^+\) receives task-related interpretation.

## 7. Token Clustering

At each layer's TRAIN \(r_{80}^{rep}\) coordinates, fit parent-specific \(k=8\) k-means with a frozen seed and transfer centers unchanged to DEVELOPMENT and CONFIRMATION. Report adjusted Rand index (ARI), normalized mutual information (NMI), resampling stability, 64 label permutations, and 64 equal-rank Haar controls. Clustering is secondary and cannot alter either primary verdict.

## 8. Guards And Execution

Mandatory guards:

- exact experiment-one record order, split, tensor, residualizer, and base-logit hashes;
- orthogonality and descending-order checks for every local/common basis;
- projection energy conservation within relative error \(5\times10^{-4}\);
- TRAIN-only means, PCA directions, k-means centers, ridge selection, nulls, and Haar draws;
- no post-confirmation layer/rank/band selection;
- finite covariance trace and at least two eligible layers in each depth window.

Resource ceiling: one local NVIDIA H100 MIG 3g.40GB, at most 32 CPU workers, 256 GiB RAM, 30 GiB new storage, and 12 wall-clock hours. Reuse experiment one's model forward; parameter eigendecomposition may reload frozen weights but performs no language-model inference.

## 9. Required Outputs

- `tables/local_parameter_spectrum.csv`;
- `tables/common_parameter_spectrum.csv`;
- `tables/representation_rank.csv`;
- `tables/functional_retention.csv` and `tables/haar_controls.csv`;
- `tables/clustering.csv`;
- `arrays/spectral_profiles.npz`, `arrays/pca_metrics.npz`, and `arrays/cka_matrices.npz`;
- all-layer local/common spectral atlas and centroid trajectories;
- function-versus-common-spectrum joint figure;
- representation-rank/held-out-retention curves;
- TRAIN/DEVELOPMENT/CONFIRMATION CKA heatmaps;
- rank-versus-functional-retention curves;
- clustering diagnostics;
- `summary.md`, `detailed.md`, and a complete artifact manifest.

## 10. Claim Boundary

Parameter-spectrum relocation, low covariance rank, high CKA, or stable clusters cannot independently establish new information. Only experiment one's same-\(X\) matched excess defines added accessibility. A joint result remains specific to this model, token site, taxonomy, linear residualizer/readout, parameter bases, and data population; it does not establish native MLP use, expert identity, Router utility, or cross-model generality.

## 11. Executed Result

- Experiment-one function-admitted layers: \(\{24,28\}\).
- Cross-depth typed outcome: `INSUFFICIENT_BASIS_SENSITIVE`.
- \(\Delta_T=-0.0046\), simultaneous 95% CI \([-0.0260,0.0169]\).
- Mean Response \(\Delta_C=0.0285\), simultaneous 95% CI \([0.0218,0.0352]\); Rank Consensus \(\Delta_C=-0.0397\), simultaneous 95% CI \([-0.0471,-0.0322]\).
- Strict representation-low-rank conjunction: no layer passes.
- Low-dimensional functional retention: blocks 24 and 28 pass first at registered rank 256; ranks 1--128 do not pass.
- CKA calibration note: paired with-replacement resampling duplicates token rows and raises high-dimensional Gram similarity; the full point matrices remain descriptive, but percentile intervals are not used to infer layer breakpoints.
- Raw run root: `/data/250010109/MoE_Router/experiments/20260816_a15_08_03_e01_function_admitted_update_spectral_rank_analysis/runs/a15-08-03-e01-20260816-full`.
