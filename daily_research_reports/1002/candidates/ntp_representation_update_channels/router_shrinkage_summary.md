# Router-score shrinkage reduces the original policy's loss without beating fixed common

2026-10-04. [中文](router_shrinkage_summary_cn.md) · [Detailed record](router_shrinkage_detailed.md). Design source: [Anchor](anchor.md). Execution contract: [Protocol addendum dated 2026-10-04 16:20 UTC](protocol.md). Execution is complete. Evidence applies only to a post-hoc diagnostic on previously exposed DEV; researcher scientific judgment and the next decision remain `Unknown`.

## 1. Purpose

Candidates remain five normalized matrix increments with measured consequences; common pools four raw domain mean gradients before scaling. This set has no zero update and never learns further. FIT-fixed selection uses its chosen common increment everywhere; the input-dependent selector predicts candidate losses before choosing. This note shrinks the input-varying part of predictions, not the physical update, distinguishing better selection from simple reversion to fixed.

Test whether choosing the strength of input-dependent predictions using FIT alone reduces the current fixed-action selector's loss while retaining utility beyond a strong fixed common action.

## 2. Hypothesis

Shrinking predictions toward FIT action means may improve the current rule. The rival is that improvement mainly comes from reverting to common, so reducing the original rule's loss does not establish useful adaptive selection. This diagnostic does not isolate estimation error, function-class limitations, record-composition differences or irreducible target uncertainty.

## 3. Analysis Method

This diagnostic changes prediction scores used to rank candidates, not parameter-increment magnitude. Four domain-gradient directions and one pooled raw-gradient direction retain their original separate normalization and remain frozen; this candidate set has no zero update. For each candidate, combine its training-fold mean finite loss change \(\mu\) and input prediction \(q\) as \(\mu+\alpha(q-\mu)\). Alpha 0 selects by candidate means alone; alpha 1 uses the original input prediction. Shrinkage may reduce selection error, or merely revert to strong fixed selection, so both the original rule and the fixed rule are necessary comparators.

FIT fits the predictor and chooses alpha; DEV scores the selected rule. A/B remain candidate-construction source banks, not a train/test split. Out-of-fold (OOF) predictions hold out entire records, keeping their 16 positions together. The LM, SAE and experts are not trained further.

- Freeze Dense, fresh S7 and SALL checkpoints at 33 billion cumulative training tokens and their original measured A/B action tables. Retain only base389 and base+full-(c,x)3461, with five nonzero actions including common and no rejection action. No language-model forward or training occurs; the ridge selectors below are refitted by fold.
- Cross-fit within 512 FIT records, keeping each record's 16 positions together. Each of four folds re-estimates scaling and fits the original λ=10 ridge on 384 training records. Select α from {0,0.1,0.25,0.5,1} by pooled out-of-fold measured finite delta CE. Within each fold, alpha 0 selects by training-fold means and alpha 1 uses that fold prediction. Final DEV uses the original all-FIT predictions and means: alpha 0 reproduces fixed common and alpha 1 the original selector. Freeze all 12 selections and every candidate's final choices before DEV scoring.
- On the original 1,024 DEV records, compare selected rules with the original rule and FIT-fixed common. Retain 24 pooled conditions and 120 pooled/domain rows. Gain is comparator CE minus policy CE; positive favors the policy, in micro-nats per prediction event. Reuse the original 2,000 category-stratified paired whole-record bootstrap draws, without refitting or reselecting alpha; 95% intervals are conditional and uncorrected for multiplicity.

## 4. Conclusion

1. **The original selector's loss can be reduced, mainly by ceasing to use its input-dependent prediction.** Eleven of 12 FIT cross-fitted selections choose alpha0; only SALL/base/A chooses alpha0.1. Selected policies improve over original alpha1 by +265.74 to +707.13 micro-nats across the 24 pooled conditions, with every corresponding conditional interval positive. In 22 conditions, selected choices are exactly fixed common. Their improvement does not establish adaptive utility over common. [All selected results](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/evaluation_selected_alpha.csv)

2. **The only rule retaining input-dependent switching also yields no pooled gain over common.** SALL/base/A switches on 2.5269% of DEV events. A→A uses the same source action bank for prediction and evaluation, still on DEV; A→B preserves the choice and scores B's corresponding action.

   | Evaluation | Gain over fixed common | Conditional 95% interval |
   |---|---:|---:|
   | A→A | −6.23 | [−20.88, +9.06] |
   | A→B | −19.72 | [−35.49, −3.45] |

   The same-source interval includes zero; the cross-source interval is negative. The former is not described as strict harm. Mean extra cost within switched events is 246.44 and 780.48 micro-nats respectively; multiplying by the switching rate exactly recovers pooled extra cost. [Condition-level results and decomposition](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/evaluation_all_alpha.csv)

3. **AI interpretation: current in-sample FIT gains do not justify adopting the input-dependent rule; a strong fixed baseline remains necessary.** Cross-fitting usually reverted to fixed before DEV was read. This narrows the current fitted predictors' use without proving that all routing information is absent or uniquely identifying overfitting. The full-input predictor's reversion does not establish insufficient input information.

All five candidate alphas are retained; no new winner was chosen from DEV. The selected OOF minimum is not an unbiased performance estimate. Smaller training folds with fixed λ=10 also change relative regularization. DEV was exposed before this recipe was proposed, and correlated conditions are not independent replications. These results do not test whether joint training creates useful expert differences, long-term acquisition/retention, or MoE architecture benefits. [Complete boundaries and lineage](router_shrinkage_detailed.md)
