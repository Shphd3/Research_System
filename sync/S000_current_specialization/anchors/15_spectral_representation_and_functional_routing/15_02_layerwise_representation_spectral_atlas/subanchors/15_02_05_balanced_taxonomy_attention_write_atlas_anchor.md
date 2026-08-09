---
anchor_id: 15_02_05_balanced_taxonomy_attention_write_atlas
status: draft_pending_researcher_confirmation
canonical_language: en
thinking_card: 15_02_05_balanced_taxonomy_attention_write_atlas_thinking_card_cn.md
parent_anchor: 15_02_layerwise_representation_spectral_atlas
updated: 2026-08-07
---

# A15_02_05 Balanced Three-Level Taxonomy Attention-Write Atlas

Thinking Card source: [researcher statements and pending AI proposals](15_02_05_balanced_taxonomy_attention_write_atlas_thinking_card_cn.md).

## 1. Problem Definition

The single decision question is:

> In frozen Qwen3-8B, after class count, node sample count, prompt distribution, and covariance reliability are controlled, does a finer taxonomic distinction relative to a coarser distinction show a larger late-versus-early shift toward higher within-layer DCLM activation-covariance rank at isolated post-`o_proj` attention writes?

Three semantic granularities are analyzed on the same hidden states. `G0` is a broad binary distinction inside a root family, `G1` is a binary distinction inside a `G0` node, and `G2` is a binary distinction between leaves inside a `G1` node. Granularity is not relation-hop depth or composition length.

The primary representation is the isolated post-`o_proj` attention write before residual addition. The full 32-head concatenated pre-`o_proj` attention output is a registered secondary boundary. Each layer and representation site receives its own DCLM activation-covariance basis. A larger local rank means lower background variance relative to other directions at the same layer and site; it does not identify the same direction across layers.

The primary metric is the post-`o_proj` late-minus-early change in the `G2-G0` normalized rank-centroid gap. Semantic strength and `G1` ordering are mandatory interpretation guards, not competing primary questions.

## 2. Physical Priors

1. Re-labeling the same balanced leaf-description states at all three taxonomy levels removes prompt frequency, token length, and input sampling as across-level differences. It does not remove semantic-distance or taxonomy-choice dependence.
2. Averaging equally normalized binary sibling contrasts estimates variance per taxonomic split; it prevents more classes from mechanically increasing total variance. The number of contrasts still changes estimator precision and rank capacity, so the primary analysis must match contrast count and node sample count across levels.
3. Finer conditional distinctions may become relatively more represented at later layers and larger local covariance ranks, but this is an empirical proposition. Deeper processing does not logically imply a rightward spectral shift.

## 3. Falsifiable Hypotheses

**Primary hypothesis.** After all matching and reliability gates pass, the post-`o_proj` statistic

$$
T_{\rho,\mathrm{post}}
=\operatorname{median}_{\ell=25:35}(\rho_{\ell,\mathrm{post},G2}-\rho_{\ell,\mathrm{post},G0})
-\operatorname{median}_{\ell=1:12}(\rho_{\ell,\mathrm{post},G2}-\rho_{\ell,\mathrm{post},G0})
$$

is positive and exceeds a balanced taxonomy-rerandomization null. `G1` must not show a statistically negative intermediate ordering if the result is called a monotone three-level trend.

**Strongest rival.** Later layers increase stable semantic strength broadly across all local covariance ranks, while normalized spectral location remains unchanged. A second rival is that unequal class count, center sample count, or contrast rank capacity produces the apparent shift.

**Main falsifier.** Reliable `G2` strength increases late relative to `G0`, but $T_{\rho,\mathrm{post}}$ is null or negative under matched contrast and sample counts.

**Pass.** All gates pass; the bootstrap lower bound of $T_{\rho,\mathrm{post}}$ is above zero; the statistic exceeds the registered balanced-tree null q95; and its sign replicates across template and DCLM calibration halves. A monotone three-level claim additionally requires coherent `G1` ordering.

**Fail.** All gates pass, but the post-`o_proj` primary statistic does not pass. A positive strength result with no location shift is a typed `strength_pass_rank_shift_fail` result.

**Insufficient.** Taxonomy validity, exact balance, hook reconstruction, semantic reliability, matched-count, or covariance-basis stability fails. A normalized location effect at negligible reliable strength is insufficient.

## 4. Mathematical Model

Let $h_{\ell,s,r,a,b,c,t,f}$ be the readout activation at layer $\ell$, site $s\in\{\mathrm{pre},\mathrm{post}\}$, root family $r\in\{1,\ldots,8\}$, binary taxonomy path $(a,b,c)\in\{0,1\}^3$, template $t$, and fact bundle $f$. There are $64$ leaves and the same activation belongs to one `G0`, one `G1`, and one `G2` label.

For granularity $g$ and one immediate parent $p$, let $\mu_{g,p,0}$ and $\mu_{g,p,1}$ be balanced child means and define the normalized sibling contrast

$$
\delta_{\ell,s,g,p}=\frac{\mu_{\ell,s,g,p,1}-\mu_{\ell,s,g,p,0}}{\sqrt 2}.
$$

Every primary schedule uses exactly $P=8$ parent contrasts at every granularity:

$$
B_{\ell,s,g}=\frac1P\sum_{p=1}^{P}\delta_{\ell,s,g,p}\delta_{\ell,s,g,p}^{\top}.
$$

Thus $\operatorname{tr}(B)$ is mean squared activation contrast per binary semantic split, not a sum over the number of classes. Two disjoint template halves $A,B$ define the cross-template reliable estimator

$$
B^{\times}_{\ell,s,g}
=\frac{1}{2P}\sum_p
\left(\delta^A_p\delta^{B\top}_p+\delta^B_p\delta^{A\top}_p\right).
$$

The common expression-noise covariance is variation across templates and fact bundles within the same leaf:

$$
W^{\mathrm{expr}}_{\ell,s}
=\mathbb E_{r,a,b,c}\operatorname{Cov}_{t,f}(h_{\ell,s,r,a,b,c,t,f}).
$$

Reliable semantic strength is

$$
S_{\ell,s,g}
=\frac{\operatorname{tr}(B^{\times}_{\ell,s,g})}
{\operatorname{tr}(W^{\mathrm{expr}}_{\ell,s})+\epsilon}.
$$

It is dimensionless and uses the same denominator for `G0/G1/G2`. It measures stable contrast magnitude relative to wording variation; it does not measure model use or causality.

Let $\Sigma^{\mathrm{bg}}_{\ell,s}=U_{\ell,s}\Lambda_{\ell,s}U_{\ell,s}^{\top}$ be the independent DCLM activation covariance, and let $P_{\ell,s,k}$ project onto equal-rank band $k$. Within each template half, the nonnegative spectral allocation and normalized rank centroid are

$$
p_{\ell,s,g,k}
=\frac{\operatorname{tr}(P_{\ell,s,k}B_{\ell,s,g})}
{\operatorname{tr}(B_{\ell,s,g})+\epsilon},
\qquad
\rho_{\ell,s,g}=\sum_{k=1}^{16}\frac{k-\tfrac12}{16}p_{\ell,s,g,k}.
$$

The two template-half centroids are averaged only after their effect signs are audited separately. $\rho$ is a within-layer rank location, not a transported direction and not raw semantic strength.

For the requested parameter-direction diagnostic, decompose the frozen output projection as

$$
W^O_\ell=U^O_\ell\operatorname{diag}(\sigma_{\ell,j})V^{O\top}_\ell.
$$

For centered pre-`o_proj` attention $a_\ell$ and post write $y_\ell=W^O_\ell a_\ell$,

$$
A^{\mathrm{pre}}_{\ell,j}=\operatorname{Var}(v^{O\top}_{\ell,j}a_\ell),
\qquad
A^{\mathrm{post}}_{\ell,j}=\operatorname{Var}(u^{O\top}_{\ell,j}y_\ell)
=\sigma_{\ell,j}^2A^{\mathrm{pre}}_{\ell,j}.
$$

This exact paired-direction identity diagnoses deterministic `o_proj` energy reweighting. It is not the DCLM data spectrum and cannot independently establish semantic redistribution.

## 5. Computational Realization

Freeze local Qwen3-8B. At the common final `Classification:` colon token, capture for every decoder block:

1. the $4096$-dimensional concatenation of all 32 pre-`o_proj` head outputs;
2. the $4096$-dimensional isolated `o_proj` output before residual addition.

Construct eight manually audited binary taxonomy root families. Every root has two `G0` children, every `G0` node has two `G1` children, and every `G1` node has two `G2` leaves, yielding $8\times2\times2\times2=64$ leaves. Each leaf has four shared templates and two disjoint label-free fact bundles, yielding $512$ texts. Canonical leaf and ancestor labels are forbidden from the description body.

The primary matched estimator uses eight parent contrasts and equal child-center sample counts at every level. Four frozen rotation schedules cover all 16 `G1` and 32 `G2` parent contrasts without raising the per-schedule rank cap above eight. The all-parent estimate is secondary. The same independent 65,536-token DCLM manifest supplies separate pre/post covariance bases and calibration halves.

No model training, SAE, residual state, MLP state, Router, parameter update, or expert-utility test enters this Anchor.

## 6. Minimal Falsification Tests

1. Audit every taxonomy edge as `is-a`, remove label leakage, and enforce exact $64\times4\times2$ balance. The same 512 states must be used for every granularity.
2. Match eight binary parent contrasts and equal child-center sample counts per granularity; require the full-parent and matched estimators to preserve the primary effect direction.
3. Require positive cross-template reliable strength for `G0/G1/G2` in registered early and late windows before interpreting $\rho$.
4. Test $T_{\rho,\mathrm{post}}$ with root-family bootstrap, balanced-tree leaf rerandomization, template halves, DCLM calibration halves, and leave-one-root-family-out analysis. Report block 36 separately.
5. Reconstruct pre/post hooks and verify the parameter-direction identity $A^{\mathrm{post}}=\sigma^2A^{\mathrm{pre}}$ numerically. This diagnostic cannot rescue a failed data-spectrum result.

## 7. Current Evidence

[A15_02](../15_02_layerwise_representation_spectral_atlas_anchor.md) found that fine classes become relatively more discriminable late at residual, pre-`o_proj`, post-`o_proj`, and MLP-input sites. However, its coarse and fine within-class denominators have different meanings, and it did not estimate a normalized spectral rank centroid under matched hierarchical contrast counts.

[A15_02_04](15_02_04_compositional_attention_write_atlas_anchor.md) correctly separated semantic strength from normalized rank location and used local DCLM bases, but its spatial-relation interface failed capability and reliability gates. Its later `is-a` smoke showed that Qwen3-8B can follow explicit one-, two-, and four-hop alias chains, while leaving natural distractor validity unresolved. Relation-hop depth remains parked and is not reused as taxonomy granularity here.

No current evidence adjudicates the present three-level, same-state, matched-count post-`o_proj` rank-redistribution question. The Anchor is a draft and does not authorize execution.

The complete candidate is recorded in the [`DRAFT_NOT_EXECUTABLE` Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/protocol.md). No `summary.md` or `detailed.md` result record exists before execution.

## 8. Claim Boundary And Next Decision

This Anchor can establish only a Qwen3-8B-specific association between taxonomy granularity, model layer, and local DCLM covariance-rank location at two attention boundaries under one balanced English taxonomy. It cannot establish composition, relation inference, literal cross-layer direction transport, attention necessity, `o_proj` semantic creation, universal middle/tail meaning, SAE correspondence, Router utility, or training benefit.

**Exactly one next decision:** confirm or correct the Thinking Card and Protocol blocks A--G, especially the taxonomy bank, matched-count estimator, primary post-`o_proj` statistic, and pass/fail/insufficient rules. Completion means every block is explicitly confirmed and cross-block consistency passes; only then may the same Protocol be promoted, after which execution scope is decided separately.
