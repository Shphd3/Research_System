派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/new_learning_speed_audit_20261026/summary.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/new_learning_speed_audit_20261026/summary.md)；研究修改仍回到原件。

---

# R05 Top-16 protection: new learning outcome and speed audit

**New-task learning succeeds, but reliable acceleration is not established.** This audit recalculates all original168DEVreadings from per-item records, retains1200asprimaryendpoint, and never trains or readsTEST. ExistingA-stageaudit already covered newendpoints and firstfour-cell95qualification; addedthresholds are descriptive, posthoc sensitivity only.

Actual intervention attenuates16pairedinitialfull-Wrank-onecoefficients perQ/K/V/Omatrix (64total); complementarydisplacement keeps ordinaryscale. TC uses0.1constant; TS usesR05cosine0.1to0.01over1200steps. They filter actualAdamdisplacement without separateoptimizers or establishedsharedfunction. Eachseed sharesoneoldmodel and exactlymatched20newanswers/update,24000atendpoint.

| arm | new_accuracy_mean_pct | new_CE_mean_nats | old_accuracy_mean_pct | qualified_orders | original_qualified_first_steps_29_43_71 |
| --- | --- | --- | --- | --- | --- |
| U | 99.541667 | 0.018265 | 0.291667 | 3 | 120 / 240 / 1200 |
| UL | 98.708333 | 0.036421 | 0.333333 | 2 | 600 / 1200 / NOT_REACHED |
| US | 96.583333 | 0.102106 | 2.291667 | 2 | 1200 / 1200 / NOT_REACHED |
| TC | 99.500000 | 0.017292 | 0.041667 | 3 | 120 / 240 / 1200 |
| TS | 99.500000 | 0.013446 | 0.166667 | 3 | 120 / 240 / 1200 |
| RS | 99.375000 | 0.016833 | 0.375000 | 2 | 120 / 240 / 600 |
| LS | 99.500000 | 0.021953 | 0.791667 | 3 | 120 / 240 / 1200 |

| seed | arm | new_accuracy_pct | new_ce_nats | first_original_qualified_step | first_original_qualified_new_targets | second_original_qualified_step |
| --- | --- | --- | --- | --- | --- | --- |
| 29 | U | 100.000000 | 0.000192 | 120 | 2400 | 240 |
| 29 | TC | 100.000000 | 0.000218 | 120 | 2400 | 240 |
| 29 | TS | 100.000000 | 0.000190 | 120 | 2400 | 240 |
| 43 | U | 100.000000 | 0.000382 | 240 | 4800 | 600 |
| 43 | TC | 99.875000 | 0.001902 | 240 | 4800 | 600 |
| 43 | TS | 99.875000 | 0.001676 | 240 | 4800 | 600 |
| 71 | U | 98.625000 | 0.054221 | 1200 | 24000 | NOT_REACHED |
| 71 | TC | 98.625000 | 0.049758 | 1200 | 24000 | NOT_REACHED |
| 71 | TS | 98.625000 | 0.038472 | 1200 | 24000 | NOT_REACHED |

Underoriginalall4newcells>=95%, U/TC/TSfirstsavedhits are120/240/1200fororders29/43/71, with2400/4800/24000newtargets. Sameobservedfirsthitdoesnotproveexactcrossingtimesequalbetweencheckpoints. SomehigherthresholdcasesfavorTC, othersfavorUorTS; all are retained inCSV and cannotreplaceoriginalcriterion. Recordedcomputetimingsarejob-loadconfounded andnotaconfirmedwallclockspeedupbenchmark. R06U/Sisreportedseparatelybecausebatch/denominator/probes/budgetdiffer.

[Chinese](summary_cn.md) · [Allthresholds](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/new_learning_speed_audit_20261026/R05_thresholds_all_105.csv) · [R06separatecheck](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/new_learning_speed_audit_20261026/R06_separate_U_S_18.csv) · [Verification](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/new_learning_speed_audit_20261026/verification.json).

Threshold sensitivity detail: mean90/95hits are identical within eachorder. Atmean99%, TC/TSorder43hit240versusU600; order29all600; order71allNOT_REACHED. Atmean99.5%, TSorder29hits1200versusU/TC600; order43all600; order71allNOT_REACHED. These posthoc details preserve exceptions rather than a universal no-difference claim.
