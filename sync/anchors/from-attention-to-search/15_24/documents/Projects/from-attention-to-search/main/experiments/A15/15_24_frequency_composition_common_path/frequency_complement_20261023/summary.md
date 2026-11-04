派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/frequency_complement_20261023/summary.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/frequency_complement_20261023/summary.md)；研究修改仍回到原件。

---

# Summary A15_24_02: local complement-restriction results

Read this round through three analysis paths:

1. **Behavior and factor controls:** fixed routing, model start and optimizer history; compare local predictive changes.
2. **Representations and layerwise organization:** reuse the existing input PCA; no new basis fit or layer sweep.
3. **Functional interventions and quality:** compare partial rollback and a scratch displacement, auditing preservation, support and coverage.

**All tests are complete; scientific judgment awaits researcher reading, explanation and discussion.** In both seeds, norm-matched PCA-complement primary loss is lower than the full-update and random-complement losses, but slightly above the original model. All four PCA rollback measurements also exceed their original baselines. These are comparisons, not a mechanism verdict or a decision to continue training.

[Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_02_frequency_complement_anchor.md) · [Frozen Protocol](../../../../../../../../UNAVAILABLE.md) · [Detailed evidence](../../../../../../../../UNAVAILABLE.md) · [中文](summary_cn.md)

## Question and necessary model

Separate retaining current responses from restricting future changes along the same directions. Original frequency dispatch selects two of eight experts; each sees the complete hidden input. Only low-list expert E0's up matrix changes temporarily; other weights, inputs and routing are fixed.

Let \(V\) contain the first 16 unit directions of the existing centered TRAIN input PCA, with \(P=VV^\top\). High input variation does not qualify these directions as belonging to an independent task. For complete AdamW displacement \(U\), applying \(U(I-P)\) preserves this matrix's response to \(V\) in exact arithmetic, retaining its existing forward contribution. Mixed inputs can still change predictions.

The candidate hypothesis predicts lower low-feature loss than both the full update and a random complement at matched displacement norm. Random restriction and norm matching address direction choice and generic step-size effects. Separate rollback removes part of the historical net displacement to test its current predictive role; it is not the same estimand as a prospective update.

## Primary predictive measurements

For each original low-frequency feature, average next-token negative log probability over DEV positions where it is active and E0 is routed, then average equally over supported features. Unit: nat, lower is better. Each delta below is relative to the same seed's original model; positive means increased loss. It is not a fraction of features improved.

| Condition | seed 11 NLL | Δ 11 (nat) | seed 22 NLL | Δ 22 (nat) |
|---|---:|---:|---:|---:|
| Saved model | 1.007749989 | +0.000000000 | 1.004129048 | +0.000000000 |
| Full AdamW displacement | 1.007756083 | +0.000006095 | 1.004151317 | +0.000022269 |
| PCA complement, full-matched norm | 1.007751599 | +0.000001610 | 1.004136524 | +0.000007476 |
| Random complement, full-matched norm | 1.007756830 | +0.000006841 | 1.004150878 | +0.000021830 |


Norm-matched PCA complement minus full update is **−0.000004485 / −0.000014793 nat**; minus matched random complement is **−0.000005231 / −0.000014354 nat**. All four contrasts are below the prespecified descriptive floor of −0.000001 nat. The same condition minus original model is **+0.000001610 / +0.000007476 nat**. Both references must remain visible because they answer different questions. [Full readouts and contrasts](../../../../../../../../UNAVAILABLE.md)

Effects are small. The floor is not estimated error, statistical significance or practical value; cross-environment numerical stability is not established. High-feature and overall readouts are reported [separately](../../../../../../../../UNAVAILABLE.md).

## Partial rollback of accumulated displacement

25% / 50% is the fraction of previously accumulated displacement removed along the candidate basis. Same-rank random rollback is norm-matched so generic perturbation damage is not automatically attributed to PCA specificity. The metric and baseline delta retain the definitions above.

| Condition | seed 11 NLL | Δ 11 (nat) | seed 22 NLL | Δ 22 (nat) |
|---|---:|---:|---:|---:|
| 25% PCA net-displacement rollback | 1.007965317 | +0.000215328 | 1.004978932 | +0.000849884 |
| Random rollback matched to 25% edit | 1.007971889 | +0.000221900 | 1.004261486 | +0.000132439 |
| 50% PCA net-displacement rollback | 1.008319567 | +0.000569578 | 1.006046609 | +0.001917561 |
| Random rollback matched to 50% edit | 1.008195751 | +0.000445762 | 1.004395395 | +0.000266347 |


All four PCA rollback values exceed their original baselines. PCA versus random ordering is not uniform: seed 11 has a slightly smaller increase for PCA at 25%, but a larger one at 50%. A rollback contrast is not extrapolated to a long-training policy. [Full norms and measurements](../../../../../../../../UNAVAILABLE.md)

## Was the intended constraint implemented?

Exact preservation of \(WV\) is equivalent to \(UV=0\). After projection of the complete displacement, actual FP32 response residual divided by original matrix norm is about **3.14×10⁻⁹**, within the prespecified 5×10⁻⁷ guard. All non-target matrices remain unchanged.

Projecting the raw gradient before AdamW leaves **19.23% / 21.67%** of the eventual displacement's norm along \(V\). This is \(\lVert UV\rVert_F/\lVert U\rVert_F\), not squared energy. That operation does not implement the specified response-preservation condition. Algebra, implementation and predictive utility are separate readings. [Numerical evidence](../../../../../../../../UNAVAILABLE.md)

## Scope and reading order

Of 1,694 original low features, 417 have support in the E0-hit subset and 1,277 are NA. Supported features have median 1 and maximum 16 positions. There are 693 affected positions across 109 dialogues; **all 693 also have high-frequency features**, so the readouts are not independent tasks. DEV has been exposed before; two inherited model seeds are not population replication. Support does not establish robust general or practical benefit.

Coverage is 12 conditions per seed, 24 total: baseline, no-op, four rollbacks and six updates. Four independent scratch AdamW proposals were constructed; accepted continuation steps are zero and no new trained checkpoint exists. Read the Anchor and Protocol before interpreting the result, and use Detailed for verification. Scientific conclusion and next decision remain Unknown pending explanation and discussion.

| Work | Coverage | Evidence type |
|---|---|---|
| Preservation and calibration | DONE_VALID | Algebra and numerical checks |
| 4 rollbacks × 2 seeds | DONE_EXPLORATORY | Finite interventions on exposed DEV |
| 6 updates × 2 seeds | DONE_EXPLORATORY | Single-batch, nonaccumulating comparisons |
| No-op, freeze, norms and independent aggregation | DONE_VALID | All 24 conditions accounted for; no failures |
| Mechanism judgment and understanding update | Pending researcher review | Not supplied by execution completion |
