---
anchor_id: 15_02_03_architectural_head_channel_concentration
status: completed_attention_sparse_pass_mlp_and_band_fail
canonical_language: en
companion_language: zh
parent_anchor: 15_02_layerwise_representation_spectral_atlas
updated: 2026-08-05
---

# A15_02_03 Semantic Concentration in Fixed MLP-Input Groups versus True Attention Heads


## 1. Problem Definition

The decision question is:

> In frozen Qwen3-8B, is coarse- or fine-grained semantic discriminability more concentrated in true pre-`o_proj` attention heads than in fixed 128-dimensional channel groups of the post-attention MLP input, and does either site exceed its own shape-matched random channel-partition null?

Let $m_\ell\in\mathbb R^{4096}$ be the output of the block's post-attention RMSNorm and the exact input to its MLP. Native channel order is partitioned once into 32 contiguous groups $G_1,\ldots,G_{32}$ of 128 dimensions. These groups are analysis coordinates, not attention heads or architectural modules.

The anchor separates three observables: actual between-class variance, semantic discriminability relative to within-class wording variation, and within-group covariance-rank localization. It does not test causal computation, Router utility, or training benefit.

## 2. Physical Priors

1. Learned representations can be anisotropic across native channels after attention mixing, residual addition, and RMSNorm, so semantic signal and nuisance variation need not be uniformly distributed.
2. Removing nuisance-heavy channels can raise a group's between/within ratio even when the group contains less total semantic energy than the full state.
3. Contiguous channel indices have no guaranteed modular identity; a real concentration claim therefore requires fixed groups to beat random channel repartitions of identical size.

## 3. Falsifiable Hypotheses

**Primary hypothesis, channel-group concentration.** On untouched semantic evidence, fixed 128-dimensional groups show a coarse and/or fine discriminability-concentration profile that exceeds equally shaped random channel partitions. Report separately whether the effect is typical across groups or confined to a selection-corrected best group.

**Spectral localization clause.** Inside a concentration-qualified group, the coarse/fine signal has a reproducible eight-band covariance profile that exceeds equal-dimensional random orientations within that group.

**Strongest rival.** Any 4096-dimensional representation split into 32 groups produces a best group above the full-state ratio because the full ratio is a weighted average; the observed maximum and band pattern are therefore partition and selection artifacts.

**Pass.** Fixed grouping exceeds the random-partition null on independent confirmation data for at least one registered semantic granularity, with valid capability, uncertainty, multiplicity, and stability guards. Typical and sparse-best clauses are typed separately.

**Fail.** All validity gates pass, but fixed grouping is indistinguishable from random partitions for both granularities; or no within-group band exceeds its random-orientation control.

**Insufficient.** The MLP-input hook, semantic capability, confirmation boundary, covariance reconstruction, numerical floor, random null, or basis-stability gate fails.

## 4. Mathematical Model

For semantic granularity $g\in\{c,f\}$ (coarse or conditional fine), let $B_\ell^g$ and $W_\ell^g$ be full-state between-class and within-class covariance at layer $\ell$. Let $S_h$ select the 128 coordinates of group $G_h$:

$$
x_{\ell h}=S_hm_\ell,
\qquad
B_{\ell h}^g=S_hB_\ell^gS_h^\top,
\qquad
W_{\ell h}^g=S_hW_\ell^gS_h^\top.
$$

Actual between-class variance per direction and energy share are

$$
v_{\ell h}^g=\frac{\operatorname{tr}(B_{\ell h}^g)}{128},
\qquad
s_{\ell h}^g=\frac{\operatorname{tr}(B_{\ell h}^g)}{\operatorname{tr}(B_\ell^g)}.
$$

They obey $\sum_hs_{\ell h}^g=1$ and $\frac1{32}\sum_hv_{\ell h}^g=\operatorname{tr}(B_\ell^g)/4096$. Thus mean raw variance is an energy-conservation diagnostic; concentration is expressed by the distribution and maximum of $s$ or $v$, not by claiming the mean exceeds the full state.

Discriminability is

$$
D_{\ell h}^g=
\frac{\operatorname{tr}(B_{\ell h}^g)}
{\operatorname{tr}(W_{\ell h}^g)+\epsilon},
\qquad
D_{\ell,\mathrm{full}}^g=
\frac{\operatorname{tr}(B_\ell^g)}
{\operatorname{tr}(W_\ell^g)+\epsilon}.
$$

Ignoring the numerical ridge, $D_{\ell,\mathrm{full}}^g$ is the within-variance-weighted mean of the group $D_{\ell h}^g$, so $\max_hD_{\ell h}^g\ge D_{\ell,\mathrm{full}}^g$ is algebraically expected. The decision metric is therefore the group-advantage profile relative to random partitions:

$$
C_{\ell h}^g=\log\frac{D_{\ell h}^g}{D_{\ell,\mathrm{full}}^g},
\quad
C_{\ell}^{\mathrm{typ},g}=\operatorname{median}_hC_{\ell h}^g,
\quad
C_{\ell}^{\max,g}=\max_hC_{\ell h}^g.
$$

The mean across groups is reported descriptively. Fine-relative concentration is

$$
R_{\ell h}=\log\frac{D_{\ell h}^f}{D_{\ell h}^c},
\qquad
C_{\ell h}^{\mathrm{rel}}=R_{\ell h}-R_{\ell,\mathrm{full}}.
$$

Independent natural text defines each group's background covariance $\Sigma_{\ell h}^{\mathrm{bg}}=U_{\ell h}\Lambda_{\ell h}U_{\ell h}^\top$. Each 128-dimensional group is split into eight consecutive 16-dimensional bands: F1=head, F2--F5=middle, F6--F8=tail. For band $k$, report per-direction actual semantic variance $b$, background-whitened variance $q$, and discriminability $j=B/W$.

## 5. Computational Realization

Freeze `/data/share/Qwen3-8B` (36 blocks, hidden size 4096, bfloat16 forward). Register a pre-hook on each block MLP and read the exact post-attention RMSNorm output at the common final `Classification:` colon token. Split only the last dimension in native order into `G1--G32`; reconstructing the full tensor by concatenation must be exact.

Reuse exactly the audited 8-parent × 8-child × 8-description semantic cube and the independent 128-document, 65,536-token DCLM calibration corpus. Within this taxonomy, templates 1--2 are design evidence and templates 3--4 are sealed confirmation evidence. This adjudicates the current site comparison but not cross-taxonomy generality. Qwen receives no gradients.

Random-partition controls permute the 4096 native channels and repartition them into 32 groups of 128. Equal-dimensional Haar subspaces are a secondary orientation control. All random seeds, partition counts, thresholds, and the confirmation manifest are frozen before confirmation is opened.

## 6. Minimal Falsification Tests

1. MLP pre-hook replay, shape, exact group concatenation, and layer identity pass for all 36 blocks.
2. Both coarse and conditional-fine variables are readable from the full MLP input above hierarchical label-permutation q95.
3. Raw semantic energy reconstructs exactly across 32 groups; group and full $B/W$ traces agree with direct full-state computation.
4. Fixed grouping's typical and maximum $C$ are compared with the corresponding statistics from random 32×128 channel partitions; the maximum null covers all registered layers and groups.
5. Templates 1--2 may rank groups, while templates 3--4 adjudicate the current same-taxonomy site comparison; cross-taxonomy generality still requires independent replication.
6. Within-group spectral claims require calibration half-split stability, three eigenvalue floors, and same-group random 16-dimensional orientation controls.
7. Parent-to-child-to-template nested bootstrap, four template directions, and leave-one-parent-out analysis protect the semantic unit; sentences are not treated as independent classes.

## 7. Current Evidence

A15_02_03_E01 is complete. All hook, replay, capability, calibration, label-permutation, and numerical guards passed.

- Maximum true-attention-head $C$ values are 3.221, 1.045, and 2.544 for coarse, fine, and fine-relative discriminability. Each exceeds the corresponding global random-partition maximum q95 and bootstrap lower-bound rule: sparse maximum Pass.
- Attention median $C$ values are -0.022, -0.067, and -0.026: typical-head Pass fails.
- Fixed MLP-group maximum $C$ values are 0.877, 0.624, and 0.945, all below their random maximum q95: fixed-group concentration Fail.
- After site-specific null calibration, attention-minus-MLP maximum differences are positive with paired intervals above zero for all three metrics; medians do not support broad attention superiority.
- No fixed F1--F8 band in a concentration-qualified attention candidate exceeds the maximum over eight random 16-d subspaces: within-unit eight-band specificity Fail.

Results: [summary](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_03_E01_architectural_head_channel_concentration/summary.md) and [evidence ledger](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_03_E01_architectural_head_channel_concentration/detailed.md).

## 8. Claim Boundary And Next Decision

This anchor establishes sparse, non-random semantic concentration in true pre-`o_proj` attention heads for the current taxonomy, while fixed MLP-input groups and fixed within-head eight-band coordinates do not pass specificity controls. It cannot upgrade this association into a causal semantic circuit, cross-taxonomy/model head identity, Router suitability, or training benefit.

**One next decision:** replicate the selection-corrected attention maximum on an independent balanced, label-free taxonomy and test whether the qualified layer/head identity is stable across taxonomies. Only replication qualifies the coordinates for expert-counterfactual or Router-training tests.
