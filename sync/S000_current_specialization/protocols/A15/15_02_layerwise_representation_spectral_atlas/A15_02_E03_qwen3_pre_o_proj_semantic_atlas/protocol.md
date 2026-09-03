# A15_02_E03: Full Pre-o_proj Attention-Output Semantic Variance Atlas

Status: **COMPLETED**; typed verdict `depth_pass_spectral_fail`.

Approval source: the user explicitly requested on 2026-08-05 that the completed semantic-granularity experiment be repeated on the attention output, reusing the same data, and delivered as a self-contained report with a comparison to the prior post-block residual result.

Canonical result records: [summary.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_E03_qwen3_pre_o_proj_semantic_atlas/summary.md) and [detailed.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_E03_qwen3_pre_o_proj_semantic_atlas/detailed.md).

## 0. Advancement Point

E01 established that conditional-fine classes become relatively more discriminable late in the 4096-dimensional decoder-block residual state. E02 localized that depth effect to the 32 pre-`o_proj` attention heads and audited each 128-dimensional head separately, but its covariance moments omitted cross-head covariance. E03 supplies the missing like-for-like full-width spectral atlas: the same 512 semantic texts and 65,536 calibration tokens are analyzed in the concatenated 4096-dimensional pre-`o_proj` attention-output space.

## 1. Question And Boundary

**Decision question:** In frozen Qwen3-8B, does the concatenated attention output before `o_proj` already show (a) a late-layer increase in conditional-fine versus coarse semantic discriminability and (b) a stable covariance-rank location for that advantage, when measured with the same definitions used for the prior full residual state?

This experiment is a frozen representation audit. It does not test attention necessity, module-wise causal contribution, Router suitability, expert compatibility, or training benefit.

## 2. Hypotheses And Rivals

- **H-depth:** late pre-`o_proj` attention outputs have larger $R_\ell=\log(D_{fine}/D_{coarse})$ than early outputs.
- **H-head:** actual coarse and fine between-class variance is largest in F1 for most contextual blocks.
- **H-nonhead:** the late conditional-fine advantage is specifically enriched in fixed middle/tail covariance bands beyond equal-dimensional random orientations.
- **R1:** the late residual effect is written only after attention, by `o_proj`, residual accumulation, normalization, or MLP computation.
- **R2:** full-width attention results are an artifact of averaging separately normalized heads; cross-head covariance changes the spectral conclusion.
- **R3:** any apparent non-head concentration is reproduced by arbitrary equal-dimensional subspaces or unstable calibration bases.

## 3. Frozen Model And Exact Representation

- model: local `/data/share/Qwen3-8B`, frozen;
- 36 decoder blocks, hidden width 4096, 32 query heads × 128 dimensions;
- bfloat16 forward, SDPA, `use_cache=False`;
- capture the tensor entering each block's `self_attn.o_proj`;
- concatenate all 32 native heads in their architectural order, yielding one 4096-dimensional vector per token and block;
- this tensor is after attention-weighted value aggregation and before learned `o_proj` cross-head mixing, residual addition, post-attention normalization, and MLP computation.

The external comparison is E01's raw decoder-block residual output. E01 is not a strict post-attention MLP-input measurement and must not be described as one.

## 4. Reused Data And Split

Reuse without alteration:

- semantic data: 8 parent domains × 8 conditional-fine classes × 4 templates × 2 disjoint fact bundles = 512 label-free English descriptions;
- design templates: T1/T2; sealed confirmation templates: T3/T4;
- common readout: final `Classification:` colon at the same absolute position;
- calibration: 128 independent DCLM documents × 512 tokens = 65,536 tokens;
- exact semantic, token, calibration, tokenizer, and model hashes from E01/E02.

No concept, text, token position, split, calibration document, layer, or band may be selected after seeing E03 results.

## 5. Covariance And Metrics

For block $\ell$, fit from calibration only:

$$
\Sigma_\ell=U_\ell\Lambda_\ell U_\ell^\top.
$$

Split the 4096 ordered directions into 16 equal 256-dimensional bands. F1 is head, F2--F8 middle, and F9--F16 tail.

For semantic level $g\in\{coarse,fine\}$:

$$
D_{\ell,g}=\frac{\operatorname{tr}(B_{\ell,g})}{\operatorname{tr}(W_{\ell,g})+\epsilon},
\qquad
R_\ell=\log\frac{D_{\ell,fine}}{D_{\ell,coarse}}.
$$

Here $B$ is variance between category centers and $W$ is within-category variation across wording/facts. $R>0$ means fine classes are more separated relative to their internal variation; it is not accuracy, activation magnitude, or causal computation.

For each band report:

- $b$: actual between-class variance per direction, activation$^2$/direction;
- $q$: $b$ divided direction-wise by calibration eigenvalues, dimensionless background-normalized semantic variance;
- $j=B/W$: band discriminability, dimensionless;
- $e$: $b$ relative to the representation-wide per-direction mean.

## 6. Primary Comparisons And Rules

- early blocks: 1--12;
- late blocks: 25--35;
- block 36 reported separately;
- primary depth statistic: $T_{attn}=\operatorname{median}_{25:35}R-\operatorname{median}_{1:12}R$;
- paired nested bootstrap: parent, child within parent, and replicate/template within child, 2,000 draws;
- require all four template contrasts and all eight leave-one-parent-out contrasts to share the depth direction;
- spectral specificity must exceed equal-dimensional random orientation controls and survive design/confirmation, calibration-half, nuisance residualization, and eigenvalue-floor checks;
- no practical effect-size threshold is imposed.

Typed verdicts:

- `depth_pass_spectral_pass`;
- `depth_pass_spectral_fail`;
- `depth_fail_spectral_pass`;
- `joint_fail`;
- `insufficient_<guard>`.

## 7. Mandatory Validity Gates

1. Model and reused-data hashes match E01/E02 exactly.
2. All 36 pre-`o_proj` hooks have shape `[batch, seq, 4096]` and exact replay.
3. Concatenated heads reconstruct the native `o_proj` input exactly; per-head projections reconstruct native `o_proj` output within $10^{-5}$ relative error.
4. Cross-head 4096-dimensional moments use all 65,536 calibration tokens and two fixed 64-document halves.
5. Covariance reconstruction, trace, orthogonality, and semantic projection-energy errors remain below registered numerical tolerances.
6. Head/middle/tail split-half projectors are stable in all but at most two blocks, and blocks 35/36 must pass.
7. All 512 semantic records are present once and retain the original hierarchy and split.
8. Raw results, whitened results, block 35, and block 36 are all reported regardless of direction.

## 8. Execution Contract

1. Reuse E02 semantic activations and provenance after exact hash/index verification.
2. Re-run only the missing cross-head calibration moment extraction.
3. Run a reduced smoke on representative early/middle/late blocks before full extraction.
4. Fit full and half-split bases, run the full semantic analysis, bootstrap, random-orientation controls, and sensitivity checks.
5. Open and audit every decisive figure.
6. Write `summary.md`, `summary_cn.md`, `detailed.md`, update the owning anchor, and create a self-contained Chinese report under `daily_research_reports/backup/2026/08/0805/`.

## 9. Required Outputs

- full-width attention covariance spectrum;
- layer × 16-band coarse/fine $b/q/j$ heatmaps;
- depth discriminability trajectory;
- decisive layer × band $\log(j_{fine}/j_{coarse})$ heatmap;
- explicit comparison with E01 residual results;
- complete compact CSV tables and provenance manifests.

## 10. Claim Boundary

The allowed result is a Qwen3-8B-specific association in one balanced English taxonomy. A stronger attention signal than residual does not mean attention alone created the information; a weaker signal does not mean attention is unimportant. Neither representation is a Router input in this dense Qwen model. No result may be upgraded to composition, causality, universal spectral semantics, expert compatibility, or training benefit.
