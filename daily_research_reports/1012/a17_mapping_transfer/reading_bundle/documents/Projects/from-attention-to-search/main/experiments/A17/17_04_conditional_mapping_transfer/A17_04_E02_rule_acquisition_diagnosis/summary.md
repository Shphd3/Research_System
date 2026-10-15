派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/summary.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/summary.md)；研究修改仍回到原件。

---

# A17_04_E02: Diagnose conditional-rule acquisition

[Subanchor](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor.md) · [Protocol](protocol.md) · [Detailed](detailed.md) · [Manifest](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/artifact_manifest.json)

All five bounded training arms and factual analysis completed. Evidence scope: `DEV_DIAGNOSTIC_ONLY`, one new training-order seed. Researcher scientific mechanism judgment and question closure remain `Unknown`.

## Purpose

Determine why the previous old conditional rule was not acquired, and identify a feasible adjustment before interpreting shared learning's effects on an acquired rule.

## Model

The carrier is registered Qwen3-0.6B Base. Mode one contains a neutral command and a three-word list: 甲 selects the first word and 乙 the last. For `红 蓝 绿`, their targets are 红 and 绿. Every target is one token; loss is computed only after the answer prefix. Accuracy uses the complete vocabulary.

Five conditions start independently from the same Base with training-order seed 29. A trains only the last attention output projection with the previous SGD configuration. B uses AdamW on that same 2,097,152-parameter matrix. C uses the same AdamW but trains q/k/v/o weights in the last four attention layers: 16 tensors, 25,165,824 parameters. D uses B's parameters/optimizer with explicit first/last instruction wording. E uses B's parameters/optimizer with neutral commands and a normalized list separator `、`, whose input-candidate token IDs passed the CPU target-ID guard.

Each arm separately performs 160 microfit updates on 64 fixed training targets, then restarts Base and optimizer for 1,200 full updates on 2,400 records. Each update contains 20 answers, so each full arm sees 24,000 answers. Original lists, labels and exposure match across arms; input token counts, trainable computation, actual update sizes and FLOPs need not match. A fixed 400-target training panel and two 400-target DEV panels measure seen-list fitting, unseen order and unseen combinations. No original TEST enters the formal generator, trainer or analysis. Qualification requires at least 80% accuracy separately for each command in each DEV panel; the combined mean alone cannot qualify an arm.

## Hypothesis

AI candidate hypothesis: the original acquisition failure can be repaired by bounded optimization, trainable-scope or presentation changes. The strongest alternatives are inadequate exposure, failure to generalize despite fitting seen examples, or candidate-word adaptation without command-controlled selection. A/B, B/C, B/D and B/E separate the practical repair routes; they do not identify pure parameter count, optimizer geometry or tokenization as unique causes.

## Conclusion

1. **The earlier failure was not only an unseen-data generalization problem.** Three existing old endpoints averaged 44.833% on the fixed training panel and 44.542% on DEV. DEV assigned 87.882% probability to the three candidates on average, yet only 7.417% of paired lists answered both commands correctly; 83.667% gave the same argmax for both commands. The old states had not reliably fitted command selection even on the inspected training subset.
2. **The original neutral task is learnable in this Base carrier when the trainable attention scope is expanded.** C reached 100% on every command/DEV-panel cell at the first qualified saved milestone, 240 updates / 4,800 answers, and retained 100% at 1,200 updates. The original data do not need relabeling to admit this observed solution. This supports expanded trainable computation as a feasible repair; it does not isolate parameter quantity from attention retrieval or optimization geometry.
3. **Increasing parameter count is not necessary for every presentation of this task, and token-ID normalization alone did not repair it.** D retained the original projection parameter count and reached 86.750% combined DEV accuracy, with its weakest cell at 82%; it first qualified at the saved 600-update milestone. Its Base baseline was 58.125%, unqualified, so this is a presentation-plus-training repair. B and E improved but did not qualify; E's matched candidate/target token IDs were not sufficient under the tested setting.

The decisive values and eligibility below come from [native analysis results](../../../../../../../../UNAVAILABLE.md), with [cellwise trajectories](../../../../../../../../UNAVAILABLE.md). These are bounded diagnostic interpretations, not researcher-approved mechanism closure.

## Analysis

The table compares all arms at the same fixed 1,200-update endpoint. TRAIN is the fixed 400-target panel, not the entire training corpus. Each DEV type has 400 answers; combined DEV weights them equally. “Weakest cell” is the minimum over the four command/panel accuracies, the qualification reader. Values are percentages.

| Setting | TRAIN | Unseen order | Unseen combination | Combined DEV | Weakest cell |
|---|---:|---:|---:|---:|---:|
| A: original projection SGD | 51.750 | 47.750 | 51.500 | 49.625 | 43.0 |
| B: projection AdamW | 82.250 | 64.250 | 72.750 | 68.500 | 58.0 |
| C: final-four-layer attention AdamW | 100.000 | 100.000 | 100.000 | 100.000 | 100.0 |
| D: explicit-instruction projection AdamW | 97.250 | 84.750 | 88.750 | 86.750 | 82.0 |
| E: normalized-list projection AdamW | 81.000 | 58.250 | 72.750 | 65.500 | 46.0 |

Only C and D meet the registered acquisition reader. C qualifies at the original 4,800-answer budget while projection B at that same exposure remains unqualified. Since B/C hold the optimizer, labels, list order and exposure fixed, expanding trainable attention is the effective intervention in this diagnostic. That intervention changes computation location, parameter count and resulting update dynamics together. It cannot establish a pure capacity mechanism or require every future experiment to use all16 tensors.

A remains unqualified after ten dataset passes, so simply extending this SGD setting from two passes to ten did not repair it. B's improvement over A makes a practical optimizer adjustment useful but insufficient. The actual mean full-training step norm is 0.009976 for A versus 0.033880 for B: the comparison changes numerical update size as well as preconditioning. B's 82.250% training-panel accuracy versus 68.500% DEV also reveals a fitting/generalization gap in the adjusted setting. The diagnosis therefore changes with the intervention; the original low TRAIN/DEV result should not be confused with B's later gap.

Microfit accuracies on the 64 trained targets were 51.5625%,85.9375%,100%,100% and81.25% for A–E. Small-set success in B/D/E cannot substitute for DEV qualification. Full starts did not inherit any microfit weights. C and D were not already qualified at Base: neutral C began at 33.25% combined DEV, while explicit D began at 58.125% with a 50.5% weakest cell. D's success therefore shows a feasible smaller-scope route with easier presentation, not unchanged Base mastery.

Candidate concentration and rule selection remain separate. At the previous old endpoints, mean DEV CE was 1.171015 = 0.132331 list-access loss + 1.038685 conditional-selection loss. After long projection SGD, DEV CE was 1.031958 = 0.021794 + 1.010164: list probability concentrated to 97.898%, but both-command success was only 11%. Under C, both-command DEV success was 100% and conditional-selection loss was approximately zero. Under D it was 73.75%, showing why the80%-per-cell convention does not mean every paired list is mastered. [Paired trajectories](../../../../../../../../UNAVAILABLE.md) preserve these distinct readers. The CE decomposition is exact output accounting, not identification of internal shared/differential modules.

E's token-ID preflight passed, but final 65.5% DEV remained below B's 68.5%, and one command/panel cell was 46%. Normalizing input/target IDs alone is therefore not a sufficient acquisition repair here. This does not prove the original encoding was irrelevant: E jointly changes punctuation, prefix length and contextual encoding. Likewise D can draw on pretrained instruction semantics; its gain cannot be assigned solely to learning a new neutral symbol mapping.

The finite five-arm run processed 120,000 full-training answers and 16,000 microfit answers; Smoke/replay counts are separate. Independent source analysis checked 91 readout files containing 46,560 record occurrences and 40 saved-state hashes/manifests; maximum loss-identity error was 9.997×10⁻⁷ nat. A separate CPU tensor audit checked all ten stage endpoints, including optimizer/counters, and confirmed that A's 240-update weight is byte-identical to the original seed 29 endpoint. All 45 frozen source/input/contract files remained unchanged. Near-zero mixed-precision CE decomposition can leave mean selection rounding residues around −3×10⁻⁸; direct double log-probability recomputation is nonnegative. Report these as approximately zero, not negative selection loss. [Detailed](detailed.md) owns full eligibility, exact resume evidence, asset receipts and the disclosed early audit's deserialization of mixed DEV/TEST JSON; no TEST model result selected this run's settings.

The parent inference can now advance from “no qualified old starting point” to “a feasible neutral-rule acquisition setting exists.” **AI suggestion:** retain the neutral task and use the expanded-attention setting as the candidate starting point for a newly contracted transfer comparison. No such transfer run has been executed here; independent confirmation requires newly frozen heldout data. The remaining question is whether a learned conditional mapping changes shared-update transfer, not whether low answer CE alone indicates rule learning.
