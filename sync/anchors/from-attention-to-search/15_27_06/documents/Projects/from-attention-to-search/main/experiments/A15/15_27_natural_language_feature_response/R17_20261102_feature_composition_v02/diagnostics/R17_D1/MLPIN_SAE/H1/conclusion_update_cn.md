派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/MLPIN_SAE/H1/conclusion_update_cn.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/MLPIN_SAE/H1/conclusion_update_cn.md)；研究修改仍回到原件。

---

# MLPIN_SAE / H1：结论更新

## 目的

检验原H1，保留正命题，不将失败诊断改写成已被支持的新假设。此处是AI证据判断；研究者的科学接受和下一决策仍为Unknown。

## 假设

粗类别候选响应可复用，细化同时包含开关变化和强度重分配；无答案时尚未证明新增成员优于共同集合和匹配随机集合两者。 原假设和数学定义见[本路线协议](protocol_cn.md)及总[协议](../../protocol_cn.md)。C为最多8个共同候选；F为最多8个细类候选；A=F减C。这里的“成员”是当前字典的候选坐标，不保证是唯一真实语义原子。各位置独立编号。

## 实验

使用自身编码和自然频率，发现选择、旧开发集选正则。下面列出修正前旧48、修正后同旧48和锁定新面板。修正前也是D1中固定新候选的输入诊断，不冒充原R17未修改结果；不可把不同样本上的差简单归因某项修正。新面板含24家族、12定理组、2改写、答案有／无；每种答案条件96细标签。

| arm          | version                                       | cue         |   N |       LL |   correct |
|:-------------|:----------------------------------------------|:------------|----:|---------:|----------:|
| C            | Original inputs / mixed selection / old48     | explicit    |  24 | 0.617572 |        17 |
| C            | Original inputs / mixed selection / old48     | description |  24 | 0.670864 |        15 |
| C            | Corrected inputs / repaired selection / old48 | explicit    |  24 | 0.655276 |        20 |
| C            | Corrected inputs / repaired selection / old48 | description |  24 | 0.691071 |        13 |
| C            | Locked fresh /192 total,96 per cue condition  | explicit    |  96 | 0.659925 |        66 |
| C            | Locked fresh /192 total,96 per cue condition  | description |  96 | 0.695204 |        50 |
| C_union_F    | Original inputs / mixed selection / old48     | explicit    |  24 | 0.424272 |        21 |
| C_union_F    | Original inputs / mixed selection / old48     | description |  24 | 0.639766 |        15 |
| C_union_F    | Corrected inputs / repaired selection / old48 | explicit    |  24 | 0.247235 |        23 |
| C_union_F    | Corrected inputs / repaired selection / old48 | description |  24 | 0.691742 |        13 |
| C_union_F    | Locked fresh /192 total,96 per cue condition  | explicit    |  96 | 0.370851 |        83 |
| C_union_F    | Locked fresh /192 total,96 per cue condition  | description |  96 | 0.703452 |        56 |
| binary_union | Original inputs / mixed selection / old48     | explicit    |  24 | 0.501887 |        16 |
| binary_union | Original inputs / mixed selection / old48     | description |  24 | 0.699547 |        10 |
| binary_union | Corrected inputs / repaired selection / old48 | explicit    |  24 | 0.362241 |        21 |
| binary_union | Corrected inputs / repaired selection / old48 | description |  24 | 0.895187 |        11 |
| binary_union | Locked fresh /192 total,96 per cue condition  | explicit    |  96 | 0.471391 |        65 |
| binary_union | Locked fresh /192 total,96 per cue condition  | description |  96 | 0.863617 |        52 |
| best_single  | Original inputs / mixed selection / old48     | explicit    |  24 | 0.515123 |        18 |
| best_single  | Original inputs / mixed selection / old48     | description |  24 | 0.720102 |        12 |
| best_single  | Corrected inputs / repaired selection / old48 | explicit    |  24 | 0.640490 |        21 |
| best_single  | Corrected inputs / repaired selection / old48 | description |  24 | 0.706579 |        10 |
| best_single  | Locked fresh /192 total,96 per cue condition  | explicit    |  96 | 0.644452 |        80 |
| best_single  | Locked fresh /192 total,96 per cue condition  | description |  96 | 0.694476 |        48 |

## 分析

无答案条件的损失收益（正数有利于较完整模型；区间为2000次定理组重采样、协议比较组内Bonferroni95%）：

- C_minus_union: -0.008247 [-0.075000, 0.043030]
- random_minus_union: 0.074507 [0.025371, 0.120956]


- 已处理的竞争解释：n未绑定、答案有无与矩阵／array框架混杂、把CC误当单位置SAE、两字典共用频率、dtype混用、只给分类率不比较预算。它们的修复均进入本路线重算；[修正台账](../../corrections_cn.md)给出范围。
- 保留的解释：旧候选选择偏向答案词；生成证书与改写的迁移；线性模型和正则的校准；字典重建对该任务的保留；有限独立家族与定理。控制成员身份／总幅值采用协变量与同支持子集，不是把这些量作精确实验操纵。
- 具体文本、token、逐成员响应、预测及反例见[案例](../../../../../../../../../../../../UNAVAILABLE.md)。逐改写、同支持子集、定理暴露和跨位置差值见[Detailed](../../detailed_cn.md)。没有根据新测试挑原子或改判据。

## 结论

**证据不足；保留共同响应和实际成员变化。** 粗类别候选响应可复用，细化同时包含开关变化和强度重分配；无答案时尚未证明新增成员优于共同集合和匹配随机集合两者。 这是当前模型、字典、文本和线性读出范围内的判断，不能推广成不存在语义或不存在非线性组合。H4还单列真实支持／覆盖门槛；不能由无阳性判语义不存在。

认识更新：粗类别候选响应可复用，细化同时包含开关变化和强度重分配；无答案时尚未证明新增成员优于共同集合和匹配随机集合两者。

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

| id                                      | arm          |   p_invertible |     loss |   correct |
|:----------------------------------------|:-------------|---------------:|---------:|----------:|
| M05_0_invertible_description            | C            |       0.454768 | 0.787967 |         0 |
| D1_M05_0_invertible_description_p0_main | C            |       0.453777 | 0.790149 |         0 |
| M05_0_invertible_description            | C_union_F    |       0.305977 | 1.184244 |         0 |
| D1_M05_0_invertible_description_p0_main | C_union_F    |       0.209771 | 1.561738 |         0 |
| M05_0_invertible_description            | binary_union |       0.397843 | 0.921698 |         0 |
| D1_M05_0_invertible_description_p0_main | binary_union |       0.315053 | 1.155016 |         0 |

## Final localization receipt

[Current read-only failure localization](../../summary_cn.md): actual H4event counts, admissible matching attempts, and Kconditional uncertainty are stated separately. In particular MLPIN H4event is identically0 on all fine rows; ATTN K64 has0/20successful matched sets. No parameter or candidate was changed.
