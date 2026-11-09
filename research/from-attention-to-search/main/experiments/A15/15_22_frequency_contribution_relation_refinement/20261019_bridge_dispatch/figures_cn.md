# 图怎么读：每张图只回答一个问题

所有图描述冻结字典的统计或固定分发。Expert ID只是接收槽位，不是已学到的功能编号。Feature band按TRAIN频率从1到4增加，不是模型层号。R是跨feature幅度份额，不是频率p；φ是二元激活相关，不是因果关系。所有EVAL解释都限探索。

| 图 | 看什么 | 可得认识 | 不能推出 |
|---|---|---|---|
| 1a/1b | 复用既有DCLM/SFT排名与共箱直方图，零频另列 | 字典使用不均且数据迁移存在 | Zipf、知识难度、容量 |
| 2 | 四段R、词频档、固定词片内中位数/IQR；灰格是空档、灰点为低支持 | 有词频联系，部分上下文变化 | 残差都是语义，每个词片都变化 |
| 3 | φ相对20随机均值的差，及两子组真实人数 | 部分段保留额外共现，且部分切分极不平衡 | 天然语义群、学习相容 |
| 4 | 左侧输入位置负载；右侧逐feature平均接收率 | 评分改变频率段机会，关系细分增量较小 | 72%输入为低频、低频已学好 |
| 5 | 所选段组成余弦；完整输入平均激活数 | 组织略有变化，仍携带高频信息 | 不同评分的绝对余弦可比为学习收益、高频造成梯度损害 |

图3灰色范围是20个随机分组的最小/最大值，不是置信区间。图5余弦使用TRAIN中心，EVAL每专家至多2000个固定样本；实际输入计数用完整EVAL。图中NA不当作0。

## figure1a_existing_frequency_rank

![figure1a_existing_frequency_rank](figures/figure1a_existing_frequency_rank.png)

[SVG](figures/figure1a_existing_frequency_rank.svg) · [PDF](figures/figure1a_existing_frequency_rank.pdf)。来源详见artifact_manifest及执行侧provenance/figures.json。

## figure1b_existing_frequency_histogram

![figure1b_existing_frequency_histogram](figures/figure1b_existing_frequency_histogram.png)

[SVG](figures/figure1b_existing_frequency_histogram.svg) · [PDF](figures/figure1b_existing_frequency_histogram.pdf)。来源详见artifact_manifest及执行侧provenance/figures.json。

## figure2_token_frequency_bridge

![figure2_token_frequency_bridge](figures/figure2_token_frequency_bridge.png)

[SVG](figures/figure2_token_frequency_bridge.svg) · [PDF](figures/figure2_token_frequency_bridge.pdf)。来源详见artifact_manifest及执行侧provenance/figures.json。

## figure3_relation_review

![figure3_relation_review](figures/figure3_relation_review.png)

[SVG](figures/figure3_relation_review.svg) · [PDF](figures/figure3_relation_review.pdf)。来源详见artifact_manifest及执行侧provenance/figures.json。

## figure4_actual_dispatch

![figure4_actual_dispatch](figures/figure4_actual_dispatch.png)

[SVG](figures/figure4_actual_dispatch.svg) · [PDF](figures/figure4_actual_dispatch.pdf)。来源详见artifact_manifest及执行侧provenance/figures.json。

## figure5_input_composition

![figure5_input_composition](figures/figure5_input_composition.png)

[SVG](figures/figure5_input_composition.svg) · [PDF](figures/figure5_input_composition.pdf)。来源详见artifact_manifest及执行侧provenance/figures.json。

