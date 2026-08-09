---
anchor_id: 15_02_layerwise_representation_spectral_atlas
legacy_anchor_id: 15_01_05_coarse_fine_semantic_variance_atlas
status: e01_e02_e03_e04_completed_depth_pass_spectral_fail
canonical_language: en
companion_language: zh
thinking_card: 15_02_layerwise_representation_spectral_atlas_thinking_card.md
parent_line: 15_spectral_representation_and_functional_routing
updated: 2026-08-06
---

# A15_02 Layerwise Representation Spectral Atlas

Thinking Card: [researcher-approved version](15_02_layerwise_representation_spectral_atlas_thinking_card.md). Chinese companion: [anchor_cn](15_02_layerwise_representation_spectral_atlas_anchor_cn.md).

## 1. Problem Definition

In frozen Qwen3-8B, are broad categories already discriminable in shallow layers while fine categories within the same parent gain more relative discriminability with depth, and which bands of each layer's natural-background covariance carry the corresponding between-class semantic variance?

The semantic hierarchy has two levels only: parent and child. Composition length, long-range dependencies, Router utility, and training benefit are outside this anchor.

## 2. Physical Priors

1. Cross-domain distinctions may form early, while within-domain distinctions may require deeper representational transformations.
2. Large background variance mechanically raises actual energy in covariance-head directions, so both granularities may appear head-dominant.
3. Fine semantics can remain absolutely head-dominant while allocating a larger relative share than coarse semantics to middle and tail bands.
4. Total variance alone is not discriminability; between-class variation must be interpreted relative to within-class wording and template variation.

## 3. Falsifiable Hypotheses

**H1, depth-relative gain:** Fine discriminability relative to coarse discriminability increases with depth. The primary contrast compares blocks 25--35 with blocks 1--12; block 36 is reported separately.

**H2, spectral atlas:** The first equal-rank band has the largest per-direction actual semantic variance for both coarse and fine variables, while fine semantics have greater relative enrichment than coarse semantics in bands 2--8 and 9--16. Fine absolute energy need not exceed coarse energy.

**Strongest rival:** Label entropy, sample count, lexical identity, prompt template, position, residual scale, tiny eigenvalues, or arbitrary equal-dimensional orientations reproduce the pattern.

**Pass:** Data and representation capability gates pass; H1 and H2 replicate on sealed templates, leave-one-parent-out analysis, nested bootstrap, label permutations, calibration half splits, and equal-dimensional random controls.

**Fail:** Validity gates pass, but the corresponding depth or spectral clause does not hold. The two clauses are adjudicated separately.

**Insufficient:** Natural semantic variables are not stably readable, or any mandatory data-balance, token, basis, numerical-stability, or sealed-confirmation guard fails.

## 4. Mathematical Model

Let $h_{\ell,p,c,t}$ be the shared readout representation at layer $\ell$, parent $p$, child $c$ within $p$, and description template $t$. Define

$$
B_\ell^{\mathrm{coarse}}
=\operatorname{Cov}_{p}\!\left(\mathbb E_{c,t}h_{\ell,p,c,t}\right),
$$

$$
B_\ell^{\mathrm{fine}}
=\mathbb E_p\operatorname{Cov}_{c\mid p}\!\left(\mathbb E_t h_{\ell,p,c,t}\right).
$$

$W_\ell^{\mathrm{coarse}}$ contains child and template variation within a parent; $W_\ell^{\mathrm{fine}}$ contains template variation within a child. Define discriminability and its relative contrast as

$$
D_{\ell,g}=\frac{\operatorname{tr}(B_\ell^g)}{\operatorname{tr}(W_\ell^g)+\epsilon},
\qquad
R_\ell=\log\frac{D_{\ell,\mathrm{fine}}}{D_{\ell,\mathrm{coarse}}}.
$$

Independent natural text defines $\Sigma_\ell^{\mathrm{bg}}=U_\ell\Lambda_\ell U_\ell^\top$. The 4096 hidden dimensions are divided into 16 consecutive equal-rank bands of 256 dimensions: F1 is head, F2--F8 are middle, and F9--F16 are tail. Per-direction actual semantic variance in band $k$ is

$$
b_{\ell,g,k}
=\frac{\operatorname{tr}(U_{\ell,k}^\top B_\ell^gU_{\ell,k})}{256}.
$$

The audit also reports $q_{\ell,g,k}$ normalized by background variance, $j_{\ell,g,k}$ normalized by within-class noise, and enrichment $e_{\ell,g,k}$ normalized by the full-spectrum per-direction semantic mean.

## 5. Computational Realization

Freeze `/data/share/Qwen3-8B` with 36 decoder blocks and hidden size 4096. Use bfloat16 forward passes and FP64 statistics. Read the embedding output and every raw decoder-block residual output, for 37 sites, at the shared final `Classification:` colon token. Do not read concept-name tokens.

Reuse the audited 128-document, 65,536-token independent DCLM covariance corpus from A15_02_02_E02. The semantic dataset is 8 parents by 8 children per parent by 8 label-free natural descriptions per child, totaling 512 texts. A low-capacity ridge probe is a held-out capability gate only and cannot update Qwen.

## 6. Minimal Falsification Tests

1. Coarse and conditional-fine tasks are both eight-way and use the same representation states.
2. Correct parent and child label strings are absent from the descriptions; tokenization, readout position, length distribution, and sample counts are matched.
3. Both full-state variables must exceed hierarchical label-permutation q95 before internal variance is interpreted.
4. Covariance reconstruction, energy conservation, 16-band half-split stability, and eigenvalue-floor sensitivity must pass.
5. Band claims must exceed equal-dimensional Haar-random orientations. If the full state is readable but true bands do not exceed random controls, covariance rank is not specific.
6. Primary uncertainty uses parent-to-child-to-template nested bootstrap, leave-one-parent-out analysis, and sealed templates; the 512 sentences are not treated as independent semantic units.
7. Block 36 is reported separately from the early/late primary contrast.

## 7. Current Evidence

A15_02_01 established that a compositional target becomes more readable in full deep representations in a capability-valid four-layer task, but no fixed H/M/T or fine band consistently beat equal-dimensional random directions. A15_02_02 established layer-specific same-token parent/child-role selectivity in frozen Qwen3-8B while rejecting a universal parent-equals-head mapping.

Neither experiment estimated between-parent coarse covariance and within-parent between-child fine covariance. The prior 32 chains contain one child per parent and cannot define $\operatorname{Cov}_{c\mid p}$, so they remain a secondary descriptive control only.

A15_02_E01 completed with a clause-specific result. The early-to-late fine/coarse discriminability contrast was $T_{depth}=0.4514$ with paired basic-bootstrap 95% interval $[0.3327,1.1891]$; all four template contrasts and all eight leave-one-parent-out contrasts were positive, so the Depth clause passed. Blocks 35/36 had fine/coarse discriminability ratios of 1.82/1.84, with no final-block reversal.

F1 was the largest actual between-class variance band in every block 1--35 for both semantic granularities, so actual-variance head dominance passed. Late fine middle/tail relative shares were only about 3.5%/3.7% higher; their intervals crossed zero and they did not exceed the equal-dimensional random-orientation q95. The late fine discriminability gain was broad across nearly all 16 bands. Fine middle/tail specificity therefore failed, giving typed verdict `depth_pass_spectral_fail`. See the [canonical result](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_E01_qwen3_residual_semantic_variance_atlas/summary.md).

A15_02_E02 localized the depth effect to individual attention-head outputs before `o_proj`. A 2026-08-05 axis-order audit corrected the old template split. The corrected pooled contrast is $T_{attention}=0.6106$ with interval $[0.6039,1.2096]$; all four template and all eight leave-parent contrasts remain positive. Nine, rather than fourteen, cells survive the global maximum over 352 late layer-head cells. No 8-dimensional band inside a qualified head exceeds all orientation and stability guards; the old `L32H27-F1` narrow claim is withdrawn. See the [corrected E02 result](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_E02_qwen3_attention_head_semantic_atlas/summary.md).

A15_02_E03 added full 4096-dimensional pre-`o_proj` covariance, including cross-head terms absent from E02's per-head block-diagonal moments. With the same 512 semantic records and 65,536 calibration tokens, early/late median $R$ is 0.153/0.764 and $T_{attention}=0.6106$ with basic-bootstrap interval $[0.6238,1.1562]$. Blocks 35/36 have fine/coarse ratios 1.99/2.21. Actual between-class variance is maximal in F1 for both semantic roles in every block 1--35. A descriptive late tail enrichment of +0.162 exceeds equal-dimensional random q95=0.059 but fails the per-late-layer calibration-half direction guard; middle also fails. The typed verdict is `depth_pass_spectral_fail`. See the [E03 result](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_E03_qwen3_pre_o_proj_semantic_atlas/summary.md).

A15_02_E04 added the full post-`o_proj` attention branch after cross-head mixing and before residual addition. With the identical model, 512 semantic records, and 65,536 calibration tokens, early/late median $R$ is 0.131/0.762 and $T_{post}=0.6311$ with hierarchical-bootstrap interval $[0.5529,1.1477]$. Blocks 35/36 have fine/coarse ratios 2.13/2.36, so the last block does not reverse. Actual between-class variance remains F1-maximal for both roles in every block 1--35. Late head/middle/tail relative-enrichment log ratios are -0.106/+0.063/+0.159. Middle narrowly exceeds equal-dimensional random q95=0.059 and passes both calibration halves and local guards; tail fails the independent-half per-late-layer direction guard. The joint typed verdict remains `depth_pass_spectral_fail`. See the [E04 result](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_E04_qwen3_post_o_proj_semantic_atlas/summary.md).

## 8. Claim Boundary And Next Decision

This anchor now establishes that fine classes become relatively more discriminable late in whole residual states, pre-`o_proj` attention, post-`o_proj` attention, and MLP input; the signal crosses `o_proj` and does not reverse at the final block. Actual semantic variance remains F1-dominant. Post-`o_proj` middle has a modest locally qualified relative-share enrichment, but tail instability prevents a joint fixed-rank non-head coordinate. The evidence cannot prove that deeper layers perform composition, attention or `o_proj` is necessary, covariance rank causes semantics, a band should guide a Router, or expert training would benefit.

**One next decision:** Decide whether an independent balanced, label-free taxonomy reproduces both positive post-`o_proj` depth contrast and the modest late middle relative enrichment. Only joint replication qualifies middle for expert-utility or compatibility admission; no Router training starts before replication.
