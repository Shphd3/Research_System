---
anchor_id: 15_03_middle_band_information
legacy_anchor_id: 15_01_12_middle_band_stability_decomposition
status: draft_metric_and_threshold_pending_review
canonical_language: en
thinking_card: 15_03_middle_band_information_thinking_card_cn.md
parent_line: 15_spectral_representation_and_functional_routing
updated: 2026-08-09
---

# A15_03 Is Apparent Middle-Band Stability Real Or An Averaging Artifact?

Researcher judgment: [Chinese Thinking Card](15_03_middle_band_information_thinking_card_cn.md). Candidate experiment: [A15_03_E01 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_03_middle_band_information/A15_03_E01_middle_band_stability_decomposition/protocol.md).

## 1. Problem Definition

A15_02_06 and A15_02_07 retain a target-common observation: semantic variance in the attention-induced actual MLP-input increment changes its local parameter-rank profile with depth even though the registered complex-minus-simple effects are not stable. In the existing plots, the normalized middle part appears to change less than the head and tail. That visual statement does not identify why.

Freeze each layer's native MLP input operator

$$
K_\ell=W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell}
=V_\ell\Gamma_\ell V_\ell^{\top}
$$

and divide its descending local rank into sixteen 256-direction bands. F1 is the head, F2--F8 are the **middle band** with total rank 1,792, and F9--F16 are the tail. Equal local rank across layers is not direction identity.

The representation is the actual attention-induced MLP-input increment

$$
\Delta n_\ell=RMSNorm_\ell(x_\ell+a_\ell)-RMSNorm_\ell(x_\ell).
$$

The fixed data are exactly A15_02_06's balanced 512 English records. `AI_PROPOSAL`: conditional-fine within-parent between-class covariance is the primary semantic object because it is the finest balanced object on this bank; coarse covariance is a registered replication control and cannot rescue the primary verdict.

**Exactly one decision question:**

> On the fixed 512-record bank and actual $\Delta n_\ell$, does the apparently depth-stable normalized F2--F8 curve remain stable in absolute per-direction variance, within-middle rank shape, and cross-layer direction identity, or is the appearance caused by total-variance normalization, canceling movement inside F2--F8, or layer-specific directions erased by local-rank averaging?

This is the smallest decision needed before asking what information middle carries or whether selecting it can improve spatial differentiation. It is a geometry and metric-identifiability audit. It does not test MLP use, task loss, expert utility, or Router gain.

A15_04 remains a separate broad shared-tail experiment with its own metric, verdict, approval, and output root. No middle analysis may be added to that Protocol or executed under its future authorization.

## 2. Physical Priors

1. **Normalization can hide scale.** A full-spectrum normalized share can remain constant while every absolute middle-direction variance grows in proportion to total semantic variance. Absolute per-direction variance and normalized share must therefore be reported together.
2. **A broad sum can hide transport.** The total F2--F8 share can remain constant while mass moves from the high-gain side F2 toward the low-gain side F8, or while opposite sub-band changes cancel. The seven registered bands must remain separate.
3. **Rank stability is not orientation stability.** Two layers can have identical variance-versus-rank curves while their occupied directions are unrelated. A cross-fitted shared-middle space must therefore beat a dimension-matched Haar space; local-rank averaging alone cannot establish a persistent coordinate.

These three risks are `HUMAN_CONFIRMED`. The metric and equivalence margin below are `AI_PROPOSAL` until reviewed.

## 3. Falsifiable Hypotheses

**H1 -- true middle stability.** The early-to-late absolute F2--F8 per-direction curve is practically equivalent, its seven-band internal shape does not move, and a middle space constructed only from other layers captures conditional-fine variance above a matched Haar partition in both early and late layers.

**H2 -- aggregation artifact.** The broad normalized middle share appears flat, but either the absolute F2--F8 curve changes with the total variance scale or the seven sub-bands redistribute internally. These are two measurable subtypes of one aggregation explanation and may coexist.

**H3 -- rank-averaging artifact.** Absolute and normalized rank curves can remain similar, and each layer's local middle can capture semantic variance, while the cross-fitted shared middle fails to beat Haar. The apparent stability then belongs to a rank interval, not to stable cross-layer directions.

H2 and H3 may both hold; the Protocol must return a typed mixed outcome rather than selecting the more convenient explanation. No hypothesis assigns a function to middle.

## 4. Mathematical Model

Let $B_{\ell,F}$ be the balanced conditional-fine between-class covariance of $\Delta n_\ell$. For local direction $v_{\ell i}$, absolute semantic variance per direction is

$$
b_{\ell i}=v_{\ell i}^{\top}B_{\ell,F}v_{\ell i}.
$$

For 256-direction band $k$, define absolute per-direction variance and full-spectrum normalized share

$$
A_{\ell k}=\frac{\operatorname{tr}(P_{\ell k}B_{\ell,F})}{256},
\qquad
p_{\ell k}=\frac{\operatorname{tr}(P_{\ell k}B_{\ell,F})}
{\operatorname{tr}(B_{\ell,F})}.
$$

Let $A_{E,k}$ and $A_{L,k}$ be medians over blocks 1--12 and 25--35. For $k=2,\ldots,8$, define $u_k=\log(A_{L,k}/A_{E,k})$. A nonpositive band value is a numerical or semantic-reliability failure rather than a value to floor after inspection.

The **one primary metric** is the absolute middle-curve drift

$$
D_M=\sqrt{\frac{1}{7}\sum_{k=2}^{8}u_k^2}.
$$

$D_M$ is in natural-log fold-change units; $\exp(D_M)-1$ is the typical multiplicative change represented by the seven-band curve. It detects both uniform absolute growth and internal redistribution. Its exact decomposition is

$$
g_M=\frac{1}{7}\sum_{k=2}^{8}u_k,
\qquad
D_{shape}=\sqrt{\frac{1}{7}\sum_{k=2}^{8}(u_k-g_M)^2},
\qquad
D_M^2=g_M^2+D_{shape}^2.
$$

$g_M$ exposes common scale growth; $D_{shape}$ exposes nonuniform F2--F8 change. The normalized broad share $p_{\ell,M}=\sum_{k=2}^{8}p_{\ell k}$ and within-middle distribution $q_{\ell k}=p_{\ell k}/p_{\ell,M}$ show whether total normalization or left/right transport makes the broad curve look flat. A registered one-dimensional Wasserstein distance over $q_{2:8}$ reports the amount of internal rank transport but does not replace $D_M$.

`AI_PROPOSAL`: practical equivalence is $D_M\le\delta_M$ with $\delta_M=\log(1.25)$, meaning no more than 25% typical absolute drift. No true-stability claim may be promoted until the researcher confirms or replaces this margin before execution.

For direction identity, define the local middle projector $P_{\ell,M}=\sum_{k=2}^{8}P_{\ell k}$ of rank $r_M=1792$. Split blocks 1--35 into odd and even groups and construct the evaluated layer's shared middle from only the opposite group:

$$
Q_M^{(-f)}=\operatorname{TopEig}_{1792}
\left(\frac{1}{|-f|}\sum_{j\in-f}P_{j,M}\right).
$$

Parameter-space stability is measured separately from semantic capture:

$$
O_{\ell m,M}=\frac{\operatorname{tr}(P_{\ell,M}P_{m,M})}{1792},
\qquad
O_{shared,M}=\frac{\operatorname{tr}(Q_M^{(A)}Q_M^{(B)})}{1792}.
$$

For independent Haar rank-1,792 subspaces in 4,096 dimensions, the expected overlap is $1792/4096=7/16$. Local-pair and odd/even-consensus overlap must be compared with matched Haar distributions; a rank label alone is not evidence of a stable parameter space.

The registered local summary is the median $O_{\ell m,M}$ over all block pairs among 1--35. Adjacent and layer-gap-at-least-18 summaries are diagnostics and cannot rescue that all-pair guard.

For $Q\in\{P_{\ell,M},Q_M^{(-f)}\}$, dimension-normalized capture is

$$
e_{\ell,Q}=
\frac{\operatorname{tr}(QB_{\ell,F})/\operatorname{tr}(B_{\ell,F})}
{1792/4096}.
$$

$e=1$ is the Haar expectation. This is a mandatory direction-identity guard, not a second primary metric. It cannot show what information the space contains or whether the MLP uses it.

## 5. Computational Realization

1. Freeze `/data/share/Qwen3-8B`, all 36 native $K_\ell$ bases, the 512-record A15_02_06 bank, record order, tokenization, readout position, and actual raw $\Delta n_\ell$.
2. The old A15_02_06 response files retain layer-local projection coordinates rather than a verified common raw vector. A cross-layer middle test therefore needs an independently approved deterministic raw-$\Delta n$ materialization or an immutable raw bank with equivalent provenance. A15_02_07 showed that cross-hardware comparison with the older cache is not a valid exact oracle; same-run replay and hook-identity guards must be used instead.
3. Retain all 4,096 exact $b_{\ell i}$ values for audit. The registered decision curve is the unsmoothed seven-point F2--F8 vector $A_{\ell,2:8}$; smoothing is display-only and cannot select a result.
4. Use blocks 1--12 as early, 13--24 as descriptive middle depth, 25--35 as late, and block 36 as a displayed terminal boundary excluded from construction and verdicts.
5. Use odd/even blocks among 1--35 as mutually exclusive shared-space construction and evaluation groups. Construct both the rank-1,792 broad middle and the seven rank-256 shared F2--F8 projectors. Report local-pair overlap and odd-built versus even-built consensus overlap before interpreting semantic capture.
6. Use matched random orthogonal 16-band partitions. Each draw's F2--F8 union is the rank-1,792 Haar control, and the same draw is applied to every layer. Independent Haar pairs additionally define the projector-overlap null. This preserves the distinction between a globally shared random orientation and layer-wise random redraws.
7. Report the full bank and the two fixed template halves separately. They are reliability strata on already inspected data, not untouched population confirmation. Parents and template clusters, not directions or layers, are the uncertainty units.

## 6. Minimal Falsification Tests

| Outcome | Inspectable rule | Route implication |
| --- | --- | --- |
| Pass: `true_middle_stability` | all provenance guards pass; the apparent low normalized-middle drift reproduces in both template halves; the 95% upper bound of $D_M$ is at most confirmed $\delta_M$; both half point estimates are within the margin; local-pair and odd/even-consensus parameter overlap beat matched Haar; local and cross-fitted shared middle semantic capture beat matched Haar q95 in both early and late blocks; fold and half directions do not reverse | retain a stable middle geometry as a candidate for a later information-identity test, not a function claim |
| Fail: `aggregation_artifact` | the normalized broad middle remains comparatively flat, but the 95% lower bound of $D_M$ exceeds $\delta_M$ | reject true stability; use $g_M$ versus $D_{shape}$ only to report scale-dominant, shape-dominant, or mixed aggregation |
| Fail: `rank_averaged_direction_instability` | $D_M$ is equivalent, but local/consensus parameter overlap or shared semantic capture does not beat Haar while the corresponding local middle evidence does; if neither local nor shared evidence beats Haar, use the bounded subtype `haar_like_middle` | reject persistent middle direction identity |
| Fail: `mixed_artifact` | absolute/internal drift exceeds the margin and shared middle also fails its Haar control | retain both explanations; neither may be erased by the other |
| Insufficient | the visual premise does not reproduce, the equivalence interval overlaps the margin, raw-$\Delta n$ or covariance reliability fails, or local/shared/Haar comparisons are unresolved | repair only provenance, precision, or the pre-run metric definition |

**Minimal counterexample:** keep every early and late F2--F8 absolute and normalized band value identical, but rotate the semantic directions independently inside each layer so that local middle exceeds Haar and cross-fitted shared middle remains inside the Haar interval. Then $D_M=0$ and every rank curve looks stable, yet the same middle directions are not stable across layers. This single construction falsifies the inference from curve stability to stable information identity.

## 7. Current Evidence

1. A15_02_06 used the required 512-record bank and actual $\Delta n_\ell$. Its raw conditional-fine local-rank centroid moved from 0.370 early to 0.471 late, while the broad target-common redistribution survived and fine-specific nonlinear use did not. The completed record did not register $D_M$ or a broad F2--F8 shared-middle test. [Summary](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E01_mlp_parameter_geometry_and_semantic_location/summary.md) and [Detailed](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E01_mlp_parameter_geometry_and_semantic_location/detailed.md).
2. A15_02_06's rank-256 parameter-only commonality was about 1.04 times Haar in the middle, versus 2.20 in head and 3.26 in tail. That makes H3 plausible but does not adjudicate the rank-1,792 F2--F8 union or semantic capture.
3. A15_02_07's matched [TAX](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_07_E01_matched_taxonomy_full/summary.md) and [COMP](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_07_E02_controlled_composition_full/summary.md) results found target-common spectral change but no stable complex-specific relocation or conditionally new linear information. They do not distinguish absolute-scale, internal-cancellation, or direction-rotation explanations for middle.
4. A15_04 is an unexecuted broad shared-tail design. Its middle space is only a control and its verdict is tail-specific. This Anchor neither amends nor borrows that verdict. [Anchor](../15_04_tail_band_information/15_04_tail_band_information_anchor.md) and [Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_04_tail_band_information/A15_04_E01_shared_tail_geometry/protocol.md).
5. Earlier A15_05 compatibility and A15_05_05 matched-training results did not admit fixed covariance bands as functional routing coordinates. Therefore even a true-stability Pass here would remain geometry-only.

The A15_03 decomposition has not been implemented or run. $D_M$, $g_M$, $D_{shape}$, within-middle transport, and shared-middle semantic capture are `NOT RUN`.

## 8. Claim Boundary And Next Decision

This Anchor may distinguish a stable absolute rank curve with shared orientation from normalization, internal aggregation, and direction-rotation artifacts on one fixed English bank. It cannot identify the semantic content carried by middle, prove linear or nonlinear accessibility beyond the old state, show native MLP use, establish expert compatibility, or justify a Router intervention.

Even `true_middle_stability` only preserves a later question: whether a function-aligned selection inside the stable middle predicts held-out expert-update or task utility beyond native and random controls. It does not reopen the failed fixed-band dispatch route and does not establish that middle is useful.

**Exactly one next decision:** approve or correct the candidate [Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_03_middle_band_information/A15_03_E01_middle_band_stability_decomposition/protocol.md). **Completion criterion:** the researcher explicitly decides the primary semantic object, $D_M$, the proposed $\delta_M=\log(1.25)$ margin, raw-$\Delta n$ provenance, Haar construction, and typed verdict rules while preserving separation from A15_04. **Resume action:** only after all Protocol blocks are confirmed, request implementation or smoke permission as a separate scope; no execution is authorized now.
