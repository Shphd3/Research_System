派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/CC_CORRECTED/H4/conclusion_update_cn.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/CC_CORRECTED/H4/conclusion_update_cn.md)；研究修改仍回到原件。

---

# CC_CORRECTED / H4：结论更新

## 目的

检验原H4，保留正命题，不将失败诊断改写成已被支持的新假设。此处是AI证据判断；研究者的科学接受和下一决策仍为Unknown。

## 假设

常见成员的低频状态搭配确实可被有限搜索找到；本轮尚不能把这些搭配命名为少见细分概念。 原假设和数学定义见[本路线协议](protocol_cn.md)及总[协议](../../protocol_cn.md)。C为最多8个共同候选；F为最多8个细类候选；A=F减C。这里的“成员”是当前字典的候选坐标，不保证是唯一真实语义原子。各位置独立编号。

## 实验

使用自身编码和自然频率，发现选择、旧开发集选正则。下面列出修正前旧48、修正后同旧48和锁定新面板。修正前也是D1中固定新候选的输入诊断，不冒充原R17未修改结果；不可把不同样本上的差简单归因某项修正。新面板含24家族、12定理组、2改写、答案有／无；每种答案条件96细标签。

| arm                           | version                                       | cue         |   N |       LL |   correct |
|:------------------------------|:----------------------------------------------|:------------|----:|---------:|----------:|
| 3604_2__15445_1_additive      | Original inputs / mixed selection / old48     | explicit    |  24 | 0.285972 |        22 |
| 3604_2__15445_1_additive      | Original inputs / mixed selection / old48     | description |  24 | 0.857780 |        12 |
| 3604_2__15445_1_additive      | Corrected inputs / repaired selection / old48 | explicit    |  24 | 0.510673 |        24 |
| 3604_2__15445_1_additive      | Corrected inputs / repaired selection / old48 | description |  24 | 0.681776 |        12 |
| 3604_2__15445_1_additive      | Locked fresh /192 total,96 per cue condition  | explicit    |  96 | 0.540436 |        95 |
| 3604_2__15445_1_additive      | Locked fresh /192 total,96 per cue condition  | description |  96 | 0.692462 |        48 |
| 3604_2__15445_1_configuration | Original inputs / mixed selection / old48     | explicit    |  24 | 0.286195 |        22 |
| 3604_2__15445_1_configuration | Original inputs / mixed selection / old48     | description |  24 | 0.857934 |        12 |
| 3604_2__15445_1_configuration | Corrected inputs / repaired selection / old48 | explicit    |  24 | 0.470215 |        24 |
| 3604_2__15445_1_configuration | Corrected inputs / repaired selection / old48 | description |  24 | 0.685767 |        12 |
| 3604_2__15445_1_configuration | Locked fresh /192 total,96 per cue condition  | explicit    |  96 | 0.514118 |        95 |
| 3604_2__15445_1_configuration | Locked fresh /192 total,96 per cue condition  | description |  96 | 0.695398 |        48 |

## 分析

无答案条件的损失收益（正数有利于较完整模型；区间为2000次定理组重采样、协议比较组内Bonferroni95%）：

- additive_minus_configuration: -0.002936 [-0.004033, -0.001827]
- matched_minus_configuration: -0.001466 [-0.001844, -0.001112]


自然验证：19200位置、150文档。

| config           |   joint_count |   joint_documents |   joint_frequency |   simultaneous_upper |   joint_to_product | formal_rarity_supported   |
|:-----------------|--------------:|------------------:|------------------:|---------------------:|-------------------:|:--------------------------|
| 3604_2__15445_1  |            58 |                37 |          0.003021 |             0.004375 |           1.107662 | True                      |
| 3604_2__11090_1  |            26 |                21 |          0.001354 |             0.002135 |           2.163399 | False                     |
| 3604_2__5308_1   |            35 |                26 |          0.001823 |             0.002761 |           1.739572 | True                      |
| 11090_1__5308_1  |            79 |                45 |          0.004115 |             0.005990 |           1.401610 | False                     |
| 3604_2__14796_1  |            35 |                21 |          0.001823 |             0.003073 |           1.139398 | True                      |
| 15445_1__11090_2 |            47 |                31 |          0.002448 |             0.004010 |           0.975787 | True                      |
| 3604_2__5308_2   |            24 |                19 |          0.001250 |             0.002188 |           3.954618 | False                     |
| 15445_1__5308_2  |            84 |                51 |          0.004375 |             0.006042 |           1.134003 | False                     |
| 11090_1__5308_2  |            24 |                18 |          0.001250 |             0.002083 |           1.411661 | False                     |
| 3604_2__11090_2  |            11 |                10 |          0.000573 |             0.001042 |           2.787456 | False                     |

两SAE匹配配置池均未产生可接受对照：各20/20次失败，实际检查后按门槛停止；加性／配置主比较均已执行。旧CC原10配置、208匹配对不变，v4重标在D1参照目录；FP32 CC另有自己的10配置、228匹配对。自然盲前缀均无可明确细标签；富集48文档仍仅2可逆、0奇异，未满足每类10文档。未知不并入语义阴性。

- 已处理的竞争解释：n未绑定、答案有无与矩阵／array框架混杂、把CC误当单位置SAE、两字典共用频率、dtype混用、只给分类率不比较预算。它们的修复均进入本路线重算；[修正台账](../../corrections_cn.md)给出范围。
- 保留的解释：旧候选选择偏向答案词；生成证书与改写的迁移；线性模型和正则的校准；字典重建对该任务的保留；有限独立家族与定理。控制成员身份／总幅值采用协变量与同支持子集，不是把这些量作精确实验操纵。
- 具体文本、token、逐成员响应、预测及反例见[案例](../../casebook_cn.md)。逐改写、同支持子集、定理暴露和跨位置差值见[Detailed](../../detailed_cn.md)。没有根据新测试挑原子或改判据。

## 结论

**证据不足：验证支持／稀有置信界、目标覆盖与匹配配置分别存在实测限制。** 常见成员的低频状态搭配确实可被有限搜索找到；本轮尚不能把这些搭配命名为少见细分概念。 这是当前模型、字典、文本和线性读出范围内的判断，不能推广成不存在语义或不存在非线性组合。H4还单列真实支持／覆盖门槛；不能由无阳性判语义不存在。

认识更新：常见成员的低频状态搭配确实可被有限搜索找到；本轮尚不能把这些搭配命名为少见细分概念。

AI假设修正倾向：保留粗类别共同响应，把“稳定细化”改成须跨答案提示、改写和定理迁移同时成立的条件命题；H3须保持双等预算优势，H4须先建立足够的可见目标内容与稀有支持。AI建议的唯一下一决策是：研究者是否优先把“无答案、问答前缀原表示可读，而当前字典／小集合弱”的断点作为下一问题；本建议不启动新实验。

[原始结果目录](../../../../../../../../../../../../UNAVAILABLE.md) · [逐例预测](../../../../../../../../../../../../UNAVAILABLE.md) · [系数与scaler](../../../../../../../../../../../../UNAVAILABLE.md)

## Fixed text and route predictions

Old original (same old ID before and after repair):

```text
Let A be a real array with 22 rows and 22 columns. For this array, zero is not an eigenvalue.
Summarize the mathematical object and its stated properties.
Summary:
```

Corrected old:

```text
Consider a real square matrix A with n = 22. It satisfies the following condition: zero is not an eigenvalue. This is the full description for this exercise.
Summarize the mathematical object and its stated properties.
Summary:
```

Locked fresh instance (related spectral certificate, different n and expression, not an old/new identical-input contrast):

```text
Consider a real square matrix A with n = 62. It satisfies the following condition: det(t I - A) evaluated at t = 0 is nonzero. This is the full description for this exercise.
Summarize the mathematical object and its stated properties.
Summary:
```

| id                                      | arm                           |   p_invertible |     loss |   correct |
|:----------------------------------------|:------------------------------|---------------:|---------:|----------:|
| M05_0_invertible_description            | 3604_2__15445_1_additive      |       0.518746 | 0.656340 |         1 |
| D1_M05_0_invertible_description_p0_main | 3604_2__15445_1_additive      |       0.602531 | 0.506616 |         1 |
| M05_0_invertible_description            | 3604_2__15445_1_configuration |       0.533952 | 0.627450 |         1 |
| D1_M05_0_invertible_description_p0_main | 3604_2__15445_1_configuration |       0.611129 | 0.492447 |         1 |

Own primary configuration: `{"config": "3604_2__15445_1", "atom_a": 3604, "state_a": 2, "atom_b": 15445, "state_b": 1, "discovery_positions": 145, "discovery_documents": 81, "discovery_frequency": 0.0037760416666666667, "state_a_frequency": 0.017213541666666665, "state_b_frequency": 0.18263020833333332, "panel_discovery_difference": -0.4375, "panel_discovery_hits": 21, "target": "singular", "eligible": true, "reasons": ""}`. State cuts remain frozen. Raw member values and enriched event flags are in results/H4_enrichment_sensitivity.csv, not inferred from these predictions.

## Final localization receipt

[Current read-only failure localization](../../summary_cn.md): actual H4event counts, admissible matching attempts, and Kconditional uncertainty are stated separately. In particular MLPIN H4event is identically0 on all fine rows; ATTN K64 has0/20successful matched sets. No parameter or candidate was changed.
