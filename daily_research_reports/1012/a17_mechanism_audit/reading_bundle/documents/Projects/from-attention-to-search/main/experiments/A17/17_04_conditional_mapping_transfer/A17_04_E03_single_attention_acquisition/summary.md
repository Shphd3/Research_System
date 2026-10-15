派生阅读副本；科学含义及 Unknown 状态不变。
原件：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E03_single_attention_acquisition/summary.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E03_single_attention_acquisition/summary.md)；仅引用目标改为包内读本或固定项目版本。

---

# Summary: A17_04_E03 single-attention acquisition

[中文](summary_cn.md) · [Anchor](../../../../../../../../UNAVAILABLE.md) · [Frozen Protocol](../../../../../../../../UNAVAILABLE.md) · [Detailed](../../../../../../../../UNAVAILABLE.md) · [Manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E03_single_attention_acquisition/artifact_manifest.json)

Protocol revision: a17_04_e03_single_attention_acquisition_v1, with append-only arithmetic erratum A01. Two bounded training arms and native analysis completed; registered engineering checks passed. Evidence is eligible for the specified acquisition diagnosis, with scope DEV_DIAGNOSTIC_ONLY and one training-order seed. Researcher mechanism judgment, adoption and parent question closure remain Unknown.

## 1. Purpose

Determine whether training only the final attention layer's four projection weights can establish the old neutral-command rule, and whether success depends on the two tested optimization packages. This narrows the acquisition prerequisite for later shared-learning experiments; it does not test new-task transfer.

## 2. Model

The carrier is the registered Qwen3-0.6B Base. Its input contains mode one, command甲 or乙, and a spaced list of three distinct words. 甲 selects the first word and乙 the last. For the same list 红 蓝 绿, their targets are红 and绿. Every answer is one target token; only that answer's next-token CE is trained.

Both arms train only layer 27's q/k/v/o weight matrices: four tensors and 6,291,456 parameters. Every other parameter, including attention normalization, stays frozen. This permits changes in attention retrieval and output projection without enlarging the model itself. It is neither Q/K/V-only training nor training every parameter in the attention module.

SGD uses learning rate 0.01 without momentum/decay. AdamW uses rate 0.0001, betas (0.9,0.999), epsilon 1e-8 and decay 0. Both apply global gradient-norm clipping at 1 across the four tensors. Both use seed 29, identical neutral lists/labels/batch order, 20 valid answers/update and the same FP32 native forward. Each separately trains 64 tiny-set targets for 160 updates, then restarts Base and optimizer for 1,200 Main updates on 2,400 records. Main therefore exposes 24,000 answers per arm; tiny weights never initialize Main.

Qualification requires at least 80% full-vocabulary accuracy in every command×DEV-panel cell, each with 200 answers. The two panels distinguish unseen order of a familiar triple from an unseen triple. Their combined mean weights them equally. A list-pair succeeds only if both command answers are correct; that reader distinguishes command-controlled selection from simply concentrating probability on candidate words.

## 3. Hypothesis

Candidate H: the final layer's four projection weights are sufficient for acquisition under at least one frozen optimization package within the bounded budget. The strongest alternatives are that earlier attention layers are needed here, that this package cannot optimize the smaller scope, or that observed CE improvement only reflects candidate-word adaptation. Fixed DEV cells and paired-command success distinguish acquisition from the latter alternative. Comparing the two arms preserves learning-rate, preconditioning and actual-step-size confounds.

## 4. Conclusion

1. **One final attention layer is a feasible acquisition route with the tested AdamW package.** At the fixed1,200-update endpoint, both unseen panels, all four command/panel cells and all 400 paired lists scored 100%. The first qualifying saved point was 240 updates/4,800 answers: combined accuracy 99.375%, weakest cell 98.5%. Thus the successful route does not require opening four layers for this task, seed and budget. This does not prove the globally smallest necessary scope.
2. **The same single-layer scope did not qualify with the tested SGD package.** Final unseen-order accuracy was 52%, unseen-combination 53.5%, combined 52.75%, and weakest cell 46.5%. Only 16.75% of paired lists answered both commands correctly; 76.25% produced the same answer for both commands. Failure is bounded to this SGD rate/clipping/budget, not every possible SGD or one-layer solution.
3. **The acquisition barrier has been narrowed, rather than the transfer question answered.** Original neutral data can be learned with one trainable attention layer and AdamW. This run supplies a smaller feasible old-rule starting configuration. No consistent/reversed new-mode learning, parameter-mechanism analysis or sharing/separation comparison was executed.

These answers come from the registered [native results](../../../../../../../../UNAVAILABLE.md) and [cellwise trajectories](../../../../../../../../UNAVAILABLE.md). Scientific mechanism acceptance remains Unknown.

## 5. Analysis

The endpoint table uses the same 1,200 Main updates/24,000 answers per arm. Each DEV panel has 400 answers; the minimum is over four 200-answer command/panel cells. “Both commands correct” is the fraction of 400 paired lists, not answer-level accuracy. All entries are percentages.

| Final-layer setting | Unseen order | Unseen combination | Combined DEV | Weakest cell | Both commands correct |
|---|---:|---:|---:|---:|---:|
| Four projections + SGD | 52.00 | 53.50 | 52.75 | 46.50 | 16.75 |
| Four projections + AdamW | 100.00 | 100.00 | 100.00 | 100.00 | 100.00 |

The fixed seen-TRAIN panel scored 61.5% for SGD and 100% for AdamW. SGD therefore has an incomplete fitting/selection problem as well as a TRAIN/DEV gap; it is not only a failure on unseen lists. AdamW's Main Base baseline was 33.25% combined DEV, its 240-update result 99.375%, and its 600/1200 saved results 100%. SGD did not qualify at any saved point. Earlier than 240 acquisition time is unmeasured because the saved reader schedule does not localize it. [Native trajectories](../../../../../../../../UNAVAILABLE.md) preserve these points.

At SGD's final endpoint, 98.2288% of probability mass was assigned to the three list words, but command selection remained weak. Its mean CE 0.941982 nat decomposes into candidate-access loss 0.018152 plus conditional-selection loss 0.923831. AdamW's mean CE was 0.000691 nat, with conditional-selection loss 0.000685, paired success 100% and same-answer fraction 0%. These are exact output-accounting and observed prediction results; they establish rule-consistent behavior on this DEV set, not a unique internal circuit. The [paired trajectories](../../../../../../../../UNAVAILABLE.md) retain command switching.

Small-set fitting must remain separate. AdamW fit all 64 tiny answers, yet after tiny training its combined DEV accuracy was only 65.375%. SGD tiny accuracy was 59.375%, with 46.25% DEV. Main then restarted, so its success is not inherited memorization of the tiny set.

For historical context, E02's neutral projection AdamW scored 68.5% combined DEV and its final-four-layer AdamW 100% at the same final target budget; both used the same neutral release and optimization settings. This new one-layer result retains the successful 100% while reducing trainable weights from 25,165,824 to 6,291,456. The [E02 Summary](../../../../../../../../UNAVAILABLE.md) owns those historical values. This shows a feasible smaller scope, not that Q/K/V individually are necessary or that parameter count alone caused the difference.

The new arms' actual updates also differ. Mean Main displacement norm across all four weights was 0.010000 for SGD and 0.015209 for AdamW; AdamW's maximum step norm was 0.249701. Its average and early-step dynamics are not matched to SGD. Therefore “AdamW works here” cannot be rewritten as a pure preconditioning mechanism or proof that every SGD fails. The source-bound [exposure/update-scale table](../../../../../../../../UNAVAILABLE.md) records this confound.

Both finite arms completed with 54,400 fitting answers total, plus 240 Smoke and 80 external-replay answers, separately counted. A01 corrects the Protocol's original aggregate Smoke arithmetic without changing its three-update paths or configuration. Native analysis checked 16 Main/tiny saved states and 34 prediction files containing 17,184 record occurrences; maximum loss-identity error was 1.6231×10⁻⁶ nat. External resume, frozen-parameter and telemetry guards passed; post-execution freeze verification passed all 36 frozen files. The [registration receipt](../../../../../../../../UNAVAILABLE.md) and [current output access](../../../../../../../../sources/assets/checks/2026-10-11_a17_single_attention_20261011t145214z_full_outputs.json) bind actual saves; Detailed owns complete provenance.

The single training-order seed and already exposed DEV panels support bounded diagnosis, not independent confirmation or generalization to arbitrary tasks. The next decision is Unknown: whether the researcher authorizes a new transfer comparison from this feasible one-layer AdamW configuration. The requested small test is complete; no subsequent experiment is launched.
