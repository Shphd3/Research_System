派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/corrections_cn.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/corrections_cn.md)；研究修改仍回到原件。

---

# D1已生效的修正与重算

每项修正已进入受影响假设，旧结果均保留。下表英文为机器台账原文；[总认识](summary_cn.md)解释其影响。[当前机器台账](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/correction_ledger.json)；初稿另存执行侧inputs，不覆盖历史。

| id   | H           | problem                                                                          | actual                                                                                                                                                                                                                                                | recalculated                                                                                                                        |
|:-----|:------------|:---------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|
| T1   | H1,H2,H3,H4 | answer-present and absent also changed matrix/array frame, n binding and wording | same object/certificate/frame; only cue versus neutral sentence in corrected old and locked fresh; appendices isolate array and negation                                                                                                              | bothSAEs all4 and affectedCC all4; oldreference preserved                                                                           |
| S1   | H1,H2,H3,H4 | jointCC response is not an independent native SAE or either requested hook       | native A17attention o_proj and E16MLPinput; own decoder/activation/frequency/candidates                                                                                                                                                               | 8SAE hypothesis cells and direct between-site effects                                                                               |
| P1   | H1,H2,H3,H4 | BF16 fixed-shape replay does not prove FP32 equivalence                          | FP32 primary fixed in advance;24old paired precision diagnostic retainsBF16reference                                                                                                                                                                  | all corrected old/new and natural native SAE; affectedCC separately                                                                 |
| R1   | H1,H2,H3,H4 | mixed development selection may favor explicit cues and confidence               | Original mixed/mixed first localized old errors; before fresh, all corrected H1-H4 primary fits use mixed old discovery with description-only old development C selection; all3 schemes retained on core continuous/binary/high16; no fresh selection | all3spaces H1-H4 primary; same-C-grid eacharm; serialized models/predictions/figures/reports regenerated                            |
| L1   | H4          | H4 rule recall and target coverage unknown                                       | v1→v2/v3/v4 text-only rule repair; 20 known controls 9→20 correct; old49 + newSAE6/40 agent text reviews; all7 result roots relabeled; full source600 exact SHA; bounded48doc enrichment; unknown excluded from determinate semantic pairs            | H4 semantic labels/prevalence/correspondence and enrichment sensitivity only; not frozen frequencies/thresholds or H1-H3 probe fits |

T1控制文本，S1核准两个SAE位置和独立字典，P1统一FP32，R1修正读出选择，四项均重算两位置H1-H4和受影响CC；L1只影响H4标签和内容解释，不用重跑H1-H3或改频率边界。

**R1口径修正**：初稿台账曾写混合开发集作主方案；实际在新响应前追加协议：先用原混合方案定位，再让全部修正H1-H4用混合旧发现集训练、无答案旧开发集选C。02:27:16UTC候选与分支冻结在首次新响应之前，不能混用初稿与最终方案。三种核心方案均保留。

**L1标注修正**：v1→v2/v3/v4修复等行列array、matrices复数、nominal提及和多对象范围问题；20控制9→20正确。此规则经有限自然文本审核校准，不是独立人工标注，也不是自然总体召回。每个结果目录保留pre_v4_semantic_snapshot，新表后缀v4。未知／粗未知不作语义阴性。富集只改变两个标签元数据字段；原v3文件可精确重构且SHA与编码时一致，token逐项相同，故不必重跑前向。频率、配置和阈值不因新标签重选。

**实现修复**：源行号从错误1基改成原0基后600/600源文档SHA一致；Unicode分隔符不再切开JSON文本；并行decoder写入改PID临时名；系数重放恢复原StandardScaler的浮点算术。CSV近1概率的十进制舍入会放大logloss差，独立CSV损失复算容差1e-6，系数概率重放仍为1e-8，不混为一个阈值。首次失败日志与旧文件保留。

n修订实际分解：旧0.3843765→旧系数换正确输入0.4202054→固定成员重拟合0.4132191→重选成员重拟合0.6355330。成员重选放大变化，不能把总差归因n的一句补充。该分解依赖路径，不能当唯一因果分配。

[代码清单](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/code_manifest.json)记录实际执行源码SHA；五图均从当前D1表生成，原R17图与结论仍保留。没有把修正改成支持假设的优化目标。
