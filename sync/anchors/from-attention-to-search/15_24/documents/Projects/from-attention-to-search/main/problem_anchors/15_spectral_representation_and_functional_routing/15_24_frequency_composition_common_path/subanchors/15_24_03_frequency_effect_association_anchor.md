派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_03_frequency_effect_association_anchor.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_03_frequency_effect_association_anchor.md)；研究修改仍回到原件。

---

# Anchor A15_24_03：Does direction-intervention impact relate to feature frequency?

## 1. Problem Definition

Does the predictive effect of the same parameter intervention relate to feature activation frequency on TRAIN? This child inherits A15_24 frequency dispatch, and extends the local effects recorded by A15_24_02. It tests conditional association, not general forgetting, and creates no independent Focus. The researcher explicitly authorizes design and autonomous bounded verification; numerical choices are AI operationalization and scientific judgment awaits review. A feature is a fixed CrossCoder activation coordinate. Frequency is the original TRAIN positive-activation rate, not token/combination frequency or difficulty. The primary contrast is B1 versus B4; middle bands are descriptive, not a test of universal monotonicity.

## 2. Physical Priors

The sole working premise is that a frequency association may survive adjustment for measured covariates. Context, activation amplitude, decoder norm, routing exposure and generic perturbation are credible rivals. A position can contain both bands, so copying its loss into two event groups does not create independent task outcomes. Match different positions and retain the same-position identity diagnostic. Observational matching does not randomize frequency.

## 3. Falsifiable Hypotheses

Within the same dialogue, current token and other routed expert, after matching activation contribution, decoder norm, hidden RMS, baseline loss and relative position, PCA rollback minus matched random rollback has a reproducible nonzero low/high event contrast. Direction is unspecified. A qualified pattern requires consistent seed signs, conditional intervals excluding zero and support/balance gates. Sparse or unbalanced matches and wide intervals are insufficient, not evidence of no association. Any association does not establish frequency causation or useful continued training.

## 4. Mathematical Model

Use original T_F step168 seeds11/22, eight experts, two selected per position with weight0.5, full cached input. Only E0 up changes temporarily. Let saved \(W_*\), initialization \(W_0\), net displacement \(D=W_*-W_0\), existing16-column TRAIN PCA basis \(V\), and \(P=VV^\top\). Roll back to \(W_*-aDP\), primary \(a=0.5\), secondary0.25. Eight fixed random orthonormal bases \(Q_r\) supply \(DQ_rQ_r^\top\), rescaled to the same parameter-edit norm and shared across seeds. PCA is not qualified as a high-frequency function.

Position loss is next-token NLL in nat, lower is better. Let \(\delta_i^P\) and \(\delta_i^{R_r}\) be PCA and random condition minus baseline loss. Define

\[
y_i=\delta_i^P-\frac18\sum_{r=1}^8\delta_i^{R_r},\qquad T=\frac1M\sum_{m=1}^M(y_{l_m}-y_{h_m}).
\]

Each pair contains a B1 activation event and a B4 activation event at different positions; no position is reused. Original \(p_f=N_{TRAIN}^{-1}\sum_i1[z_{if}>0]\) is rechecked. Features label observations rather than components manipulated in isolation. Positive T means greater low-side excess damage in matched events; negative means greater high-side excess damage. This is a conditional subset contrast, not a causal population average. Report original, random and excess effects together.

## 5. Computational Realization

Reuse verified caches, original model loading, fixed head and the A15_24_02 FP32 forward; adapt random bases, matching and position-level aggregation. No backward, optimizer or training. Events retain position, feature, band, frequency and covariates. Primary exact matching uses dialogue/current-token/other-expert identity. Continuous covariates are log(z×decoder norm), log decoder norm, log hidden RMS, mean inherited two-seed baseline NLL and relative context position. Covariate-only SD standardization, per-coordinate caliper0.5, global greedy squared distance and deterministic ties; exclude same positions and never reuse a position. This is not identical full context. Prespecified cross-dialogue same-source/token/route matching is diagnostic only. Four-band/feature tables remain descriptive and do not create independent replicates.

## 6. Minimal Falsification Tests

Primary is the50% T in both seeds, with5000 dialogue-bootstrap draws and conditional95% intervals. Require at least20 pairs/10 dialogues and absolute standardized mean difference<=0.1 on all five covariates before interpreting signs as qualified association evidence. These AI operational thresholds do not guarantee power. Retain all random draws and leave-one-random-out contrasts. Secondary dose and cross-dialogue analysis cannot rescue failed primary qualification. Exact no-op, matching identity, finiteness, frozen tensors/input files, actual parameter norm matching and complete coverage are required. Same-position low/high copies necessarily share loss and yield zero; that identity is not a frequency null result.

## 7. Current Evidence

Functional outcomes are NOT RUN at freeze. Covariate-only preflight gives693 E0 positions and11 within-dialogue pairs across9 dialogues, maximum absolute SMD0.1513. Primary support/balance is already insufficient before outcomes; the cross-dialogue diagnostic has one pair. Further computation cannot repair this qualification gap, but finite interventions remain independently measurable. Earlier A15_24_02 results retain their own identity and are not new confirmation.

**2026-10-24 execution facts.**All40readouts complete;no-op/freeze/norm/independent aggregation pass.Primary50% T=−.000995/+.003931nat with both intervals crossing zero;11pairs/9dialogues and imbalance retain INSUFFICIENT.Scientific judgment Unknown.[Summary](../../../../experiments/A15/15_24_frequency_composition_common_path/frequency_effect_association_20261024/summary.md).

## 8. Claim Boundary And Next Decision

Scope is fixed models, one matrix, specified rollback and matched subset. All693 affected positions contain both high and low features. Seeds share previously exposed DEV and near-duplicate independence is unknown. No frequency causation, independent modules, long-training gain, general forgetting or fresh confirmation is established. Completion does not update researcher understanding. The sole decision after implementation/support/result review is whether frequency-association evidence is sufficient; otherwise retain uncertainty without relaxing matching, selecting endpoints or training for a favorable result.

[Protocol](../../../../../../../../UNAVAILABLE.md)
