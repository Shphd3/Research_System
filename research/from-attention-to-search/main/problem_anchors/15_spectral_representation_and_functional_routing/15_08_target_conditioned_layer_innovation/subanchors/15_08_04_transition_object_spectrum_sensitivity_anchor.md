---
anchor_id: 15_08_04_transition_object_spectrum_sensitivity
status: EXECUTED_AWAITING_HUMAN_JUDGMENT
canonical_language: en
chinese_companion: 15_08_04_transition_object_spectrum_sensitivity_anchor_cn.md
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor.md
depends_on: 15_08_03_function_admitted_update_representation_rank_anchor.md
parent_line: 15_spectral_representation_and_functional_routing
execution_authority: APPROVED_IMPLEMENTATION_SMOKE_FULL_RUN_2026-08-17
created: 2026-08-17
updated: 2026-08-17
---

# A15_08_04 Transition-Object And RMSNorm Spectrum Sensitivity

Parent definition: [A15_08 Target-Conditioned Layer Innovation](../15_08_target_conditioned_layer_innovation_anchor.md). Chinese companion: [Anchor](15_08_04_transition_object_spectrum_sensitivity_anchor_cn.md).

## 1. Problem Definition

This child Anchor asks one descriptive decision question:

> On the same frozen model and the same 2,048 DCLM token positions, does the centered covariance spectrum change materially when the measured object is an adjacent Attention-write difference, one of four raw/normalized MLP-site differences, the same-layer normalized update \(U=Z-X\), or the residual/normalized state received at the MLP site?

The blocking uncertainty is object identity. Earlier adjacent-layer, MLP-input, and same-layer-update spectra cannot be interpreted as one rank statement unless hook site and RMSNorm placement are held explicit. This is the smallest guard needed before comparing those results. The audit is unlabeled representation geometry; function, semantics, causality, intrinsic population rank, and Router utility are out of scope.

## 2. Physical Priors

**Prior:** covariance rank is a property of a named random vector, not of an abstract layer. Residual accumulation, Attention-only writes, adjacent-layer differencing, and RMSNorm are different transformations of the token cloud and may change its spectrum. The prior is weakened if all registered raw/normalized matched contrasts yield nearly identical normalized spectra and \(r_{80}\) profiles.

## 3. Falsifiable Hypotheses

**H-SENS — definition-sensitive spectrum.** At least one registered matched raw-versus-RMSNorm contrast changes the layerwise \(r_{80}\) fraction by a median of at least 0.05 of the identifiable rank and has the same direction in at least 70% of matched layers.

**Strongest rival R-ROBUST — object-robust spectrum.** Under identical tokens, centering, rank cap, and plot axes, all registered matched contrasts have median absolute \(r_{80}\)-fraction differences below 0.02 and no contrast reaches 70% directional consistency.

An intermediate effect, identity-guard failure, non-finite spectrum, incomplete layer coverage, or covariance trace below \(10^{-12}\) is `INSUFFICIENT`. These operational thresholds classify sensitivity only; they do not define scientific low rank.

## 4. Mathematical Model

For block \(\ell\), define the raw pre-Attention residual \(h_\ell\), raw Attention write \(a_\ell\), raw post-Attention residual \(r_\ell=h_\ell+a_\ell\), normalized old state \(X_\ell=N_\ell(h_\ell)\), actual normalized MLP input \(Z_\ell=N_\ell(r_\ell)\), and same-layer update \(U_\ell=Z_\ell-X_\ell\).

For every registered object matrix \(M_{c,\ell}\in\mathbb R^{2048\times4096}\), center over token rows and form the sample-space covariance Gram matrix

\[
G_{c,\ell}=\frac{1}{2047}\widetilde M_{c,\ell}\widetilde M_{c,\ell}^{\top}.
\]

Let descending nonnegative eigenvalues be \(\lambda_j\) and \(p_j=\lambda_j/\sum_k\lambda_k\). The primary compactness coordinate is

\[
r_{80}(c,\ell)=\min\left\{r:\sum_{j\le r}p_j\ge0.8\right\},
\]

reported as \(r_{80}/2047\). Effective rank and covariance trace are secondary. The spectrum describes token variation in one named object; it cannot identify target information.

## 5. Computational Realization

1. Load Qwen3-8B locally and run one deterministic length-2,048 DCLM sequence without training.
2. Capture every token position at each of 36 block inputs and each raw Attention `o_proj` output. Recompute \(r\), \(X\), \(Z\), and \(U\) with the block's own post-Attention RMSNorm; verify native MLP input equals \(Z\).
3. Construct eight conditions: \(\Delta a\), \(\Delta h\), \(\Delta X\), \(\Delta r\), \(\Delta Z\), \(U\), \(r\), and \(Z\). Adjacent conditions have transitions 1→2 through 35→36; state/update conditions have layers 1 through 36.
4. Compute every centered Gram spectrum in float32, clip only negative roundoff, normalize by trace, and preserve the same 2,048-rank x-axis. The final centered eigenvalue is structurally zero and is floored only for log display.
5. Render one full-layer figure per condition, one 2×4 common-axis grid, one layer-median overlay, and numerical tables for trace, \(r_{80}\), and effective rank.

## 6. Minimal Falsification Tests

The primary matched contrasts are pre-Attention RMSNorm effect \((\Delta X,\Delta h)\), post-Attention MLP-site RMSNorm effect \((\Delta Z,\Delta r)\), and state-site RMSNorm effect \((Z,r)\). For each contrast compute the median absolute paired difference in \(r_{80}/2047\) and the larger directional fraction across layers.

- **Pass — `DEFINITION_SENSITIVE`:** any registered contrast has median absolute difference at least 0.05 and directional consistency at least 0.70.
- **Fail — `DEFINITION_ROBUST_WITHIN_TOLERANCE`:** every contrast has median absolute difference below 0.02 and directional consistency below 0.70.
- **Insufficient:** all other numerical outcomes or any validity-guard failure.

The other objects and all spectral curves are descriptive comparisons and cannot rescue or overturn the matched-contrast verdict.

## 7. Current Evidence

The eligible full run covers the frozen 2,048-token DCLM slice, all 36 blocks, and all 283 registered curves, with zero identity and replay errors. The registered verdict is `DEFINITION_SENSITIVE`: the state contrast \((Z,r)\) has median absolute \(r_{80}/2047\) difference 0.194675 and directional consistency 0.8056. In contrast, the adjacent differences \((\Delta X,\Delta h)\) and \((\Delta Z,\Delta r)\) are only 0.013679/0.6286 and 0.011724/0.5714 and do not reach the sensitivity threshold.

A post-hoc scale audit found that raw \(r_l\) is dominated from block 8 onward by the first sequence token: at block 8 its norm is 12,414 versus a token median of 46.7, a 266-fold ratio. The Pass therefore means that whole-state spectra depend on RMSNorm and raw-state scale; it does not show that the rank of cross-layer added information is highly RMSNorm-sensitive. See the [canonical Summary](../../../../experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_04_E01_dclm_transition_object_spectrum_comparison/summary.md). Interpretation remains `AI_DRAFT_AWAITING_HUMAN_JUDGMENT`.

## 8. Claim Boundary And Next Decision

The current result establishes only that apparent spectral compactness in this frozen Qwen3-8B DCLM slice depends materially on the named object and RMSNorm, with sensitivity dominated by whole states rather than adjacent differences. It cannot identify new information, semantic content, model-native features, population-intrinsic rank, or routing utility, and the raw-state rank-one appearance cannot be called semantic low rank.

**Exactly one next decision:** the researcher decides whether to freeze \(U_l=Z_l-X_l\) as the primary object for subsequent token-subspace analysis and restrict raw \(r_l\) to scale diagnostics. Completion requires an explicit accept/reject judgment on that boundary. Resume from the canonical Summary, then register a separate function-conditioned subspace experiment if accepted.
