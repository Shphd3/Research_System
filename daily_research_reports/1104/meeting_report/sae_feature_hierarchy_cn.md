# 1104组会：SAE特征组合与语义层级

目的：看成员如何换入换出，以及共同成员怎样搭配强弱，把几何坐标带回具体文本。预期H1为可复现成员关系，H2为可复现共同强弱；实际按类别／字典／措辞分别判定。

| SAE | 大类 | H | 显式条件 | 跨措辞 |
| --- | --- | --- | --- | --- |
| ATTN_SAE | animal | H1 | LOCAL_SUPPORT | INSUFFICIENT |
| ATTN_SAE | animal | H2 | LOCAL_SUPPORT | INSUFFICIENT |
| ATTN_SAE | vehicle | H1 | LOCAL_SUPPORT | SUPPORT_IN_THIS_PANEL |
| ATTN_SAE | vehicle | H2 | LOCAL_SUPPORT | NOT_SUPPORTED |
| MLPIN_SAE | animal | H1 | LOCAL_SUPPORT | INSUFFICIENT |
| MLPIN_SAE | animal | H2 | LOCAL_SUPPORT | INSUFFICIENT |
| MLPIN_SAE | vehicle | H1 | LOCAL_SUPPORT | SUPPORT_IN_THIS_PANEL |
| MLPIN_SAE | vehicle | H2 | INSUFFICIENT | INSUFFICIENT |

## 认识更新与紧接的原始数据

本轮多确定了三件事。第一，细类不是把父类32个成员全部保留后再往上添加：它在同一32成员预算内保留部分并更替部分。具体候选有复现也有失败，例如MLP输入猫换入候选#22958为8/8，#11234为0/8；自行车#16830为8/8。因而可重复的是部分组合事件，而不是整份列表稳定不变。

第二，成员重叠与共同成员的强弱复现是两个问题。显式留出中，同域相对跨域的Jaccard差为Attention动物0.2212、交通0.1341，MLP输入0.1884、0.1595；但交通工具H2在MLP输入只有5/8组固定成员资格。不能把更高类内重叠直接改写为稳定强弱规律。Attention交通工具H2在显式词下局部通过，属性改写后联合投影95%区间跨零，跨措辞稳定性未支持。

第三，语义推广首先受原模型行为约束。动物属性文本猫3/8、狗8/8，不能把这些表征差直接当成模型成功完成了隐含猫狗识别。交通工具两子类属性均8/8；H1重叠子预测跨措辞保持，但仍有词面/属性线索和位置差异。所有共同列表的严格频率匹配完整随机名单均0/256，因此这些名单的特异优势还没有匹配参照，不能声称优于任意同频共同成员。

组合模式需要给出适用语境。换一句表达后，原方向可以保留、改变，或因成员不再共同激活而无法检验；这三者对应不同认识。两个大类和两套SAE分开看，不拼成统一层级规律。

| SAE | 大类 | 措辞 | H1关系重叠差[区间] | H2联合强弱投影[区间] | H2可用/8 |
| --- | --- | --- | --- | --- | --- |
| ATTN_SAE | animal | explicit | 0.2212 [0.1868, 0.2500] | 0.0401 [0.0186, 0.0572] | 8 |
| ATTN_SAE | animal | synonym | 0.2031 [0.1790, 0.2294] | 0.0209 [0.0142, 0.0273] | 8 |
| ATTN_SAE | animal | property | 0.1362 [0.0947, 0.1730] | 0.0052 [-0.0158, 0.0239] | 8 |
| ATTN_SAE | vehicle | explicit | 0.1341 [0.0966, 0.1740] | 0.0275 [0.0136, 0.0444] | 8 |
| ATTN_SAE | vehicle | synonym | 0.0388 [0.0201, 0.0566] | 0.0221 [0.0148, 0.0317] | 7 |
| ATTN_SAE | vehicle | property | 0.1340 [0.0924, 0.1769] | 0.0057 [-0.0040, 0.0161] | 7 |
| MLPIN_SAE | animal | explicit | 0.1884 [0.1508, 0.2254] | 0.0048 [0.0031, 0.0065] | 7 |
| MLPIN_SAE | animal | synonym | 0.1975 [0.1762, 0.2205] | 0.0101 [0.0071, 0.0131] | 7 |
| MLPIN_SAE | animal | property | 0.1469 [0.1178, 0.1773] | -0.0062 [-0.0093, -0.0031] | 8 |
| MLPIN_SAE | vehicle | explicit | 0.1595 [0.0884, 0.2416] | 0.0530 [0.0350, 0.0711] | 5 |
| MLPIN_SAE | vehicle | synonym | 0.0546 [0.0222, 0.0888] | 0.0464 [0.0251, 0.0677] | 5 |
| MLPIN_SAE | vehicle | property | 0.1824 [0.1545, 0.2084] | 0.0626 [0.0522, 0.0730] | 8 |

## 从完整文本看组合

```text
Asked what the survey was about, the researcher replied that it concerned an animal. The interview then ended.
Description:
```

```text
Asked what the survey was about, the researcher replied that it concerned a cat. The interview then ended.
Description:
```

```text
Asked what the survey was about, the researcher replied that it concerned a dog. The interview then ended.
Description:
```

ATTN_SAE，固定ID `[23899, 18691, 9522]`，依次父／子1／子2原始z `[[29.915199279785156, 1.8149000406265259, 2.1656999588012695], [29.234399795532227, 1.8162000179290771, 2.7362000942230225], [29.653900146484375, 3.1851000785827637, 2.513400077819824]]`。

MLPIN_SAE，固定ID `[14481, 29342, 29506, 17390, 11190, 21902]`，依次父／子1／子2原始z `[[92.14019775390625, 56.114200592041016, 29.172000885009766, 10.6697998046875, 8.385499954223633, 10.570899963378906], [89.72429656982422, 55.3473014831543, 29.16510009765625, 9.631999969482422, 8.803999900817871, 10.571800231933594], [90.90249633789062, 56.3484992980957, 29.34749984741211, 9.717100143432617, 8.71500015258789, 10.695799827575684]]`。

```text
Asked what the survey was about, the researcher replied that it concerned a vehicle. The interview then ended.
Description:
```

```text
Asked what the survey was about, the researcher replied that it concerned a car. The interview then ended.
Description:
```

```text
Asked what the survey was about, the researcher replied that it concerned a bicycle. The interview then ended.
Description:
```

ATTN_SAE，固定ID `[23899, 9522]`，依次父／子1／子2原始z `[[30.53019905090332, 1.6159000396728516], [31.085800170898438, 2.0899999141693115], [30.924100875854492, 2.578200101852417]]`。

MLPIN_SAE，固定ID `[14481, 29342, 29506, 16240, 20696, 11190, 21902]`，依次父／子1／子2原始z `[[91.1134033203125, 55.66709899902344, 29.452899932861328, 9.37969970703125, 7.4430999755859375, 8.42389965057373, 10.911600112915039], [91.04720306396484, 56.153099060058594, 28.663299560546875, 7.729000091552734, 5.15749979019165, 8.42959976196289, 10.369600296020508], [90.38490295410156, 55.6963005065918, 29.70549964904785, 7.340700149536133, 2.608799934387207, 8.265399932861328, 10.812399864196777]]`。

## 实验分析与机制直觉

每大类16家族、8发现／8留出；统一Description:冒号取样。显式词、同义词、属性描述和两负类都保留。H1算逐对支持交并、三方共同、换入／换出和同模板跨大类；H2用发现固定共同列表L2归一化，联合方向只在发现拟合，留出不重选。原模型先检查完整二选一／四选一，不删错误。随机支持／频率匹配、家族内标签打乱、同义／属性和共享父结构参照分别检查竞争解释。

AI机制直觉：固定Top32会使排序竞争与强弱再分配同时出现。它是下一步可检验的解释，不是本轮确认的语义计算机制。

边界：显式词复述、属性词线索、改写长度／位置、重构限制和小样本仍在。组合可区分不等于router已学会分发。H3/H4和router本轮未运行。科研接受和下一决策由研究者保留。

[完整中文Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/summary_cn.md) · [详细报告](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/detailed_cn.md) · [具体反例](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/casebook_cn.md) · [图](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/figures)
