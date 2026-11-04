派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/frequency_effect_association_20261024/summary.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/frequency_effect_association_20261024/summary.md)；研究修改仍回到原件。

---

# Does parameter-intervention impact relate to feature frequency?

**A15_24_03 is complete:40 forward readouts and numerical audits pass, but a stable frequency association is not established.** Strict matching retains11pairs/9dialogues with remaining imbalance. The two model contrasts have opposite signs and both intervals cross zero. This is insufficient evidence, not evidence of no frequency effect.

Read three analysis paths:

1. **Behavior and factor controls:** predictive loss under the same rollback and eight matched random controls.
2. **Representations and organization:** reuse fixed frequency bands, input PCA and activations; no new dictionary/model fitting.
3. **Functional interventions and quality:** comparable positions, random controls, freeze/no-op/replay, separating finite effects from frequency interpretation.

[Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_03_frequency_effect_association_anchor.md) · [Frozen Protocol](protocol.md) · [Detailed](detailed.md) · [中文](summary_cn.md)

## Operation and comparison

Use two original trained frequency-routing models. Only expertE0 up is temporarily edited; full inputs, routing and all other parameters stay fixed. Roll back25%/50% of initial-to-step168 displacement along16 existing input PCs. Eight random same-rank directions match parameter-edit norm; restore after every readout.

B1/B4 label original TRAIN feature activation frequencies. A position commonly contains both bands, so duplicating its loss is not two independent task outcomes. Match different positions within dialogue/current-token/other-expert, balancing activation contribution, decoder norm,hidden RMS,baseline NLL and relative position. This is similar, not identical complete context, and does not isolate individual feature contributions.

## Primary observations

For each position, subtract the mean eight-random loss change from PCA rollback loss change. T is mean matched low-minus-high excess impact. Positive means greater low-side excess harm; negative means greater high-side harm. Unit nat; loss lower is better.50% is primary,25% secondary.

| Seed | Rollback | PCA low−high | Mean random low−high | Excess T | Conditional95% interval |
|---|---:|---:|---:|---:|---|
| 11 | 0.25 | -0.000482746 | +0.000015154 | -0.000497900 | [-0.002294919, +0.001350924] |
| 11 | 0.5 | -0.000960490 | +0.000034976 | -0.000995466 | [-0.004580875, +0.002690475] |
| 22 | 0.25 | +0.001991024 | +0.000045373 | +0.001945651 | [-0.005056263, +0.008899924] |
| 22 | 0.5 | +0.004019452 | +0.000088292 | +0.003931161 | [-0.010033855, +0.017777335] |


Primary50% T is **−0.000995 / +0.003931 nat**: opposite signs with both intervals crossing zero. Leave-one-random-out signs persist within each model, but between-model disagreement remains. [Matched raw/random/excess values](detailed.md#matched-and-band-results)

Qualification requires20pairs/10dialogues and all absolute SMD<=.1. Actual11pairs/9dialogues; decoder-norm SMD−.107 and relative-position SMD+.151 exceed the line. This was known in covariate-only preflight. No matching relaxation was made; independent finite effects and random controls still completed. Intervals are conditional on fixed matches/directions and do not repair qualification.

## Credibility and limits

All40 arms retain position NLL. Both inherited baseline replay errors are0, no-op is exact, other tensors/head remain frozen and original models are restored. Maximum random norm mismatch is below8.4×10⁻⁹. Independent CPU verification recomputes all paired effects, intervals and44,332 feature rows with maximum discrepancy0.

All four-band unadjusted descriptions remain, but overlap, support and weighting differ. At50%, low-feature macro loss increases are.000570/.001918, high-feature increases.000904/.000449, with ordering changing across models. They cannot replace matching. [All bands and40 readouts](detailed.md#all40-readouts)

Scope remains one matrix,one expert,two inherited models and exposed DEV. All693 affected positions contain both low/high features. Training frequency was not manipulated; no frequency causation, independent modules or long-training benefit is established. Scientific judgment and any next experiment await researcher implementation/evidence review.

| Work | Completion/eligibility |
|---|---|
| Bilingual Anchor/frozen Protocol | Complete; frozen bytes/hashes retained |
|2seeds×20forward readouts |DONE_VALID; no missing/failed arms |
|Frequency events,matching,multiple random controls |Complete; primary association INSUFFICIENT |
|Replay,freeze,norms,independent aggregation |PASS |
|Training/new model/publication |Zero training; no new model; local only |
