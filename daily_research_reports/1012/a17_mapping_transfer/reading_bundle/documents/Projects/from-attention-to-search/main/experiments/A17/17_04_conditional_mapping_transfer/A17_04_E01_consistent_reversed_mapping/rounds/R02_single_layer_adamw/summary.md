派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/summary.md)；研究修改仍回到原件。

---

# Summary: A17_04_E01 R02 single-layer AdamW mapping transfer

[中文](summary_cn.md) · [Anchor](../../../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor.md) · [Protocol](protocol.md) · [Detailed](detailed.md) · [Manifest](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/rounds/R02_single_layer_adamw/artifact_manifest.json)

The nine bounded continuation branches and 34-condition local optimizer probe completed. Smoke and Full engineering checks passed; actual saves and readouts are registered. Results are eligible for the registered, exposed-DEV diagnosis, conditional on one trained old endpoint. Researcher mechanism judgment, architecture adoption and question closure remain Unknown.

## 1. Purpose

Determine whether changing a new visible mode's command-to-position relation changes the cost of shared-parameter learning to an already acquired old rule. Separately, test whether a small optimizer intervention can distinguish immediate step-size, direction and moment-history effects without claiming a long-term mechanism.

## 2. Model

The carrier is Qwen3-0.6B Base with only the final attention layer's q/k/v/o weights trainable: four tensors, 6,291,456 parameters. All other parameters freeze. Mode one maps甲 to the first word and乙 to the last. Mode two either keeps this mapping (consistent) or swaps it (reversed). The two new-world inputs and paired answer marginals are identical; target assignment changes. Answers are one token and only answer CE is trained.

All branches start from the same actual E03 AdamW1200 old endpoint, with old DEV accuracy 100%. Three continuation-order seeds 29/43/71 each run consistent, reversed and joint_reversed. They are three orders from one learned old model, not three independent old-training replications. Every branch resets AdamW moments, uses rate 1e-4/betas(.9,.999)/epsilon1e-8/decay0 and global four-tensor clipping 1, and trains 1200updates×20answers. Primary branches receive 24000 new answers. Joint has 10 old + 10 new per update, hence 12000 of each; it supplies old-label rehearsal and is only a feasibility control.

Measure full-vocabulary accuracy, answer CE and correct-versus-opposite endpoint margin. For fixed old DEV mean margin \(M_A\), the primary effect is

\[
E_s=\Delta M^{\mathrm{reversed}}_{A,s}-\Delta M^{\mathrm{consistent}}_{A,s},
\]

where both changes use the common old endpoint and units are nat/answer. Negative \(E_s\) means a relative reversal cost; absolute old deterioration is assessed separately. Each world has 400 answers per unseen-order/unseen-combination panel; the combined reader weights panels equally. Old/new qualification requires every command/panel cell ≥80%.

The local probe separately restores Base, E03 SGD240 or AdamW240 for each intervention. It uses two fixed old TRAIN batches and 80 old DEV records. Native SGD/AdamFresh steps, cross-norm rescalings and AdamCarry at the actual240-step history give 34 conditions. Actual displacement \(\delta=\theta_{\mathrm{after}}-\theta_{\mathrm{before}}\) is distinguished from source gradient; recipient first-order prediction is \(g_R^\top\delta\), with measured remainder \(\Delta L_R-g_R^\top\delta\).

## 3. Hypothesis

Candidate H: after matched new-answer exposure, reversal reduces old answer advantage relative to consistency. Old acquisition, learned reversed targets and absolute harm must be verified rather than assumed. Difficulty, initial new competence, optimization path and general candidate-word adaptation are the strongest alternatives. Joint learning tests feasibility, not the utility of separating modules. The small probe constrains local update explanations only.

## 4. Conclusion

1. **The acquired old rule is strongly harmed by reversed-only continuation in this setting.** All three orders end at 0% old accuracy, while new reversed accuracy is 100%, 100% and 97.75%. Consistent continuation retains 100% old accuracy. The primary combined effects are −38.3854,−41.2847 and−37.1470nat, mean −38.9391, sampleSD2.1237. They satisfy the registered descriptive direction/size convention. This is actual old harm, not merely less improvement: mean old CE rises from 0.000691 to 15.819206 and margin falls from 17.524653 to −15.793102.
2. **The harm concerns conditional answer selection, and joint supervision can preserve both mappings.** A post-hoc count finds that 100%, 100% and 97.5% of old predictions after reversal choose the opposite endpoint—the answer required by the new mapping. Joint old/new training reaches mean 99.833% old and 99.667% new accuracy, with all eight command/mode/panel cells qualified in every order. This supplies a feasible shared-parameter solution under mixed supervision, not evidence that separate experts are necessary or that rehearsal wins under equal supervision.
3. **The optimizer probe rejects a simple “larger SGD steps solve learning” account.** At Base, enlarging SGD to Adam's norm lowers CE mainly through candidate access while conditional choice worsens. At SGD240, the same intervention raises CE by 0.97545/1.53274nat. Direction, state and moment history affect local results; these finite interventions do not establish why the full SGD/Adam acquisition trajectories differed.

The first two answers use [registered native transfer results](../../../../../../../../../../UNAVAILABLE.md), [endpoint tables](../../../../../../../../../../UNAVAILABLE.md) and the explicitly [post-hoc rule-choice count](../../../../../../../../../../UNAVAILABLE.md). The third uses the [local probe results](../../../../../../../../../../UNAVAILABLE.md). Mechanism acceptance remains Unknown.

## 5. Analysis

The endpoint table reports accuracy percentages, averaging the three continuation orders equally. Each order is evaluated on the same 400 answers per panel/world. Joint uses half the new exposure and additional old labels; its row is a feasibility witness rather than a matched primary competitor.

| Continuation | Evaluated rule | Unseen order | Unseen combination | Combined |
|---|---|---:|---:|---:|
| Consistent-only | Old | 100.000 | 100.000 | 100.000 |
| Consistent-only | New consistent | 100.000 | 100.000 | 100.000 |
| Reversed-only | Old | 0.000 | 0.000 | 0.000 |
| Reversed-only | New reversed | 99.000 | 99.500 | 99.250 |
| Joint old/reversed-new | Old | 99.833 | 99.833 | 99.833 |
| Joint old/reversed-new | New reversed | 99.667 | 99.667 | 99.667 |

The combined endpoint below reports all three requested quantities, averaging the three continuation orders equally and weighting the two DEV panels equally. CE and rule margin use nat/answer; accuracy is a percentage. Lower CE is better, while higher correct-versus-opposite margin is better. These are absolute endpoint values, not changes from the old start.

| Continuation | Evaluated rule | CE | Accuracy (%) | Rule margin |
|---|---|---:|---:|---:|
| Consistent-only | Old | 0.000040806 | 100.000 | 23.145962 |
| Consistent-only | New consistent | 0.000040982 | 100.000 | 22.851338 |
| Reversed-only | Old | 15.819206 | 0.000 | −15.793102 |
| Reversed-only | New reversed | 0.031350 | 99.250 | 16.189830 |
| Joint old/reversed-new | Old | 0.004841 | 99.833 | 18.106281 |
| Joint old/reversed-new | New reversed | 0.009108 | 99.667 | 15.650192 |

[Native combined means](../../../../../../../../../../UNAVAILABLE.md) retain exact values and each continuation order. The old starting point is CE0.000691, accuracy100%, margin17.524653; under reversed-only continuation, its loss and answer advantage both deteriorate while the new rule is learned.

The relative old-margin effect is negative on both unseen types: mean −39.5665nat for order and−38.3117 for combination, with respective sampleSD2.3223/1.9418. The combined mean is their equal-weight average, not an independent third panel. Under consistency, old margin increases by mean 5.6213nat while accuracy stays at its 100% ceiling. Old CE decreases by only 0.000650nat, below the inherited 0.005nat material-loss convention; do not call this a large CE improvement. Reversal's large CE/accuracy/margin deterioration supplies the net-harm evidence separately from the relative contrast. [Native results](../../../../../../../../../../UNAVAILABLE.md) retain each order and panel.

The initial new rules are not equally difficult. Before new training, consistent mode-two accuracy is already 99.875%, whereas reversed accuracy is 0%; their target margins are 16.0350 and −16.0350nat. The old mapping therefore already generalizes almost perfectly to the new visible mode when the command relation is preserved. This experiment estimates the total consequence of changing that relation under the frozen training procedure; it does not isolate compatibility from the effort of relearning an initially reversed relation. First saved new qualification occurs at step 0 for every consistent branch and 120/120/240 for reversed branches. At those reversed crossings, old accuracy is already only 2.875%, 2.5% and 2.75%. The secondary reader demonstrates early harm after useful new learning, but does not equalize attained skill or training paths. [Comparable-level readouts](../../../../../../../../../../UNAVAILABLE.md) preserve this limitation.

Candidate adaptation cannot explain the old failure by itself. After reversal, mean old candidate mass remains 99.6211%, while conditional-choice loss is 15.810429 of the 15.819206nat answer CE. The post-hoc argmax count shows opposite-endpoint choice in both panels for all seed 29/43 records; seed 71 gives 96.5% on unseen order and 98.5% on unseen combination. This is predominantly a reversal of selected endpoint, rather than inability to output a list word. It is an output observation; it does not prove that the model internally ignored mode or identify which attention component caused the change.

An illustrative seed 29 list is 红 黄 猫. In old mode,甲 should output红 and乙猫. At the start both are correct; after reversed-only continuation they become猫/红 even under old mode, while those predictions are correct in the reversed new mode. Joint continuation outputs红/猫 in old mode and猫/红 in new mode. This sample was selected after seeing outcomes and illustrates the aggregate result; it is not extra confirmation. The [sample probabilities](../../../../../../../../../../UNAVAILABLE.md) make the two conditions explicit. The [trajectory figure](../../../../../../../../../../UNAVAILABLE.md) plots saved learning progress; it does not establish events between saved checkpoints.

All three joint runs qualify both modes, with weakest old/new cells at least 99.5%/98.5%. Thus the one-layer shared carrier has an observed way to express both visible mappings when both receive supervision. This weakens an unavoidable representational-incompatibility explanation. The old-label mixture, lower new exposure and different trajectory prevent attributing its preservation solely to any one factor. No parameter split or expert comparison was run.

The small optimizer probe adds a different, bounded insight. At Base/batch 1, SGD enlarged from norm 0.01 to 0.249701 changes CE by −0.650492nat, access loss by −0.903941 and conditional-choice loss by +0.253449. Its larger CE gain does not mean better candidate selection. At SGD240/batch 1, enlargement predicts a first-order CE change of −0.429824, but actual change is +0.975447; the finite remainder is +1.405271. The actual finite result, not the gradient dot product alone, determines harm at that step.

SGD and fresh Adam directions have cosine 0.192–0.306 across probe states/batches. At Adam240, fresh-versus-carried Adam cosines are 0.0862/0.2104, showing that actual saved moments change local direction. These findings do not rank one optimizer universally or identify the cause of1200-step success. Probe CE uses FP64 log-softmax over native FP32 logits, with native FP32 CE gradients; the reported remainder includes nonlinear finite-step effects and residual precision differences. The [independent probe audit](../../../../../../../../../../UNAVAILABLE.md) preserves all 34 conditions, actual tensors, remainders and numerical bounds.

Engineering completion is separate from scientific interpretation. Full job pt-x0czuelx succeeded; all nine branches reached 1200updates and 216000 training answers. Native analysis verified 72 saved states, 72 readout files/115200 record occurrences and the seven required TensorBoard tags. All 42 frozen files remained unchanged. Smoke/replay and local probe guards passed; the latter's independent maximum norm-match relative error is 2.1306×10⁻⁵, below 1%. The [actual output registration](../../../../../../../../../../UNAVAILABLE.md) binds eleven saved checkpoint/probe/analysis families and current strict access. Detailed owns the complete lineage and deviations.

The bounded update is that preserved versus reversed conditional relations lead to sharply different retention under new-only shared learning, while mixed old/new supervision demonstrates feasible coexistence. Internal mediation, difficulty/path separation, fresh confirmation and the utility of parameter separation remain unresolved. Exactly one next researcher decision is whether these conditional costs justify a separately contracted sharing-versus-separation comparison. This result does not itself authorize that experiment.
