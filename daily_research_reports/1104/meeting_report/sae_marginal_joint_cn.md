# 1104组会：单成员频率与联合结构的区分

**问题。** S08同域Top32重叠更高，是否主要来自单feature频率？控制这些频率后，是否仍有留出复现、随源不同的共现结构？

**观察与对照。** 固定留出每feature次数和每行32的零模型，复制原式差值的82.9%–97.0%；5/6个剩余差区间跨0。发现集频率预测也复制99.4%–127.7%，但它不固定行32且有频率估计偏差。平均Jaccard主要是边际现象，不能作为联合结构的充分证据。两类比值都是数值复制比例，不是因果解释率。

| SAE | pair | real_gap | discovery_frequency_gap | fixed32_margin_gap | fixed32_ratio | remaining_gap_CI |
|---|---|---|---|---|---|---|
| ATTN_SAE | Magicoder/GSM8K | 0.014126 | 0.017108 | 0.013297 | 94.1% | [-0.000572,0.002301] |
| ATTN_SAE | Magicoder/MMLU | 0.010565 | 0.011846 | 0.008760 | 82.9% | [0.000136,0.004108] |
| ATTN_SAE | GSM8K/MMLU | 0.009900 | 0.012646 | 0.008845 | 89.3% | [-0.000719,0.003353] |
| MLPIN_SAE | Magicoder/GSM8K | 0.046637 | 0.046341 | 0.045240 | 97.0% | [-0.001008,0.003852] |
| MLPIN_SAE | Magicoder/MMLU | 0.029533 | 0.029801 | 0.027332 | 92.5% | [-0.000206,0.005047] |
| MLPIN_SAE | GSM8K/MMLU | 0.026308 | 0.029499 | 0.025209 | 95.8% | [-0.001765,0.004574] |


**联合统计结果。** 发现集按频率固定每字典24成员、全部276对；本源残差方向和源间差方向只在发现集拟合。留出本源6/6、源间差6/6通过冻结的正向/区间/混合/null判据；分别Holm6校正，p=.023346。支持本轮可测的条件共同出现结构及其跨源差异；不支持将其命名为语义或router机制。

**结论下原始数据。** Attention-GSM8K #17625/#14773，留出221/1032位置共同出现（94/129文档），固定次数零模型0.115708，真实0.214147。GSM8K原文“On a moonless night, three fireflies danced in the evening breeze...”在token ` by`的激活9.756166/12.859011。反例：MLP #20989/#24338，GSM8K发现低于null，留出高于null（2/1024→12/1032）；整体向量复现不代表每对同向。

**做法。** 原771篇与8位置不变，各源128发现/129留出；4链×64严格边际零模型，burn100/thin10。所有列次数误差0；Rhat≤1.0276、ESS≥129.9；文档bootstrap999，不能把null或token当独立文档。无新前向、训练、分类或干预，S08原文件保持。

**边界与审阅。** S08只是格式描述，没有独立格式匹配；本轮也未做。额外token分层仍为正，但52/89层<8行。位置、长度、代码格式、来源/主题、近重复、发现概率估计与条件CI范围仍限制解释。Numina缺失。科学接受/关闭Unknown；本轮结束，等待审阅。

[完整Summary](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S09_marginal_vs_joint_1104/summary_cn.md) · [两张主图](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S09_marginal_vs_joint_1104/figures/01_overlap_vs_frequency.png) / [联合检验](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S09_marginal_vs_joint_1104/figures/02_joint_null_and_holdout.png) · [Detailed](/data/250010109/Research_System/research/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S09_marginal_vs_joint_1104/detailed_cn.md)
