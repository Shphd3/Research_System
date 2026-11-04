# 10月20日讨论：高频成分在场，是否就该固定调用高频专家？

**本轮没有得到这个学习收益。** 表征分析和四条件×两种子的学习验证全部完成。主问题未关闭，机制判断待讨论。[一页项目结论](../../../Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/20261020_20261019T164834Z/one_page_cn.md) · [完整Summary](../../../Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/20261020_20261019T164834Z/summary_cn.md) · [Detailed与全部源表](../../../Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/20261020_20261019T164834Z/detailed_cn.md)。

## 两分钟汇报

我们的总目标是让低频feature相关输入学得更好。导师提出的关键直觉是：一个输入可能同时需要共同成分和特有成分，互斥分发可能不合适。我们先检查表征，再把“高频名单可代表共同计算”变成有限学习假设。

模型是冻结Qwen3-0.6B Base，在第28层输出、最终归一化之前增加8个FFN专家，每次调用2个，输出各乘1/2。T按TRAIN feature频率组织名单，R随机重排但严格匹配人数；F动态选择两个组对，H固定第4组对再选一个。只有T的第4组对是高频。各臂同85,548答案目标、168更新、配对初始化和数据顺序。Base原计算及完整输入均保留。

**三条证据：**

1. 低频输入确实混合高频成分；真实hidden首主方向只覆盖11.61%总方差，DEV中高频向量对该方向的有符号对齐为90.13%。这是几何关系，不是共同功能或90%全部信息。
2. 固定调用高频组对后，低频feature到所属专家的平均接收率从72.76%降至66.75%。这说明调用机会改变，不是输入被删除，也不能直接判学习差。
3. 统一DEV上T_H−T_F低频feature宏NLL差+0.00099；相对随机组织的额外差+0.00246。两者未满足预定改善方向，原重采样范围跨0，两seed方向不一致。本轮不支持“应固定高频路径”的结论，但不足以宣判common无用。

![同预算终点比较](../figures/figure5_terminal_dev.png)

左图是四臂两种子，越低越好；右图是配对差，负数才支持改善，横线跨过0。DEV128对话/10,340位置，最低频池1,694项中838可估、856NA，支持≥20为0。重采样中可估项会变化，图中范围不能当作固定838项的合格置信覆盖保证。

## 我们现在怎样理解“按频率分发”

先用固定TRAIN统计每个feature出现频率，再把feature放入名单；当前输入携带多种feature，用同一幅度评分决定调用谁。它不是按当前token是否罕见直接分发，也不是让专家只看自己频段的信息。所有专家输入仍是完整hidden。

当前token身份对DEV低频幅度份额的全部位置R²约0.434，已见ID子集较高，但有15.82%位置的ID未见。固定16feature的50个可用文本展示槽保留随机、高激活及同ID未激活例；最低段四项DEV命中仅1/0/1/1，不能稳定命名。探索性高低频伴随超出匹配背景，也尚未证明功能依赖。

![接收和调用分开](../figures/figure3_static_routing.png)

图中总负载为200%，因为每位置调用两个专家。名单接收更高并没有在本轮显示出相应低频学习优势。因此我们暂不把接收率、高频共现或PCA对齐当作设计成功指标。

## 认识变化与下一决策

昨天原以为：混合输入需要common，可以给高频组固定一个槽。今天证据：混合与高频几何结构成立，固定调用却未显示预定学习收益。保留混合表征；缩小“高频=有用共同计算”的代理推断。未答的是：高频名单专家是否真的执行了这批输入需要的功能。

**AI建议的唯一下一问题：固定已训模型内，高频名单专家是否有可替换验证的任务收益？** 若继续，先在同两专家预算下做固定权重调用替换，分开功能与名单；本轮未自动执行。尚存竞争解释包括Base已提供共同能力、高频标签不对应有用更新、固定槽挤占，以及有限预算与极低支持。

## 讨论自检

- 为什么不能用“高频在场”直接推出固定高频专家有用？——输入成分、调用参数和loss收益是三个对象。
- 为什么必须有随机名单上的F/H？——它帮助区分频率组织特定增量与一般固定一个组对的影响。
- 为什么宏NLL改善而含低频位置NLL可略差？——前者让每个feature等权，同一位置可重复；后者每个位置只算一次。
- 为什么仍不能说高频路径无效？——差值很小、seed不一致、区间支持有限；当前代理也没有认证共同功能。
- 如果只做一个后续，测什么？——测固定权重下调用替换的任务代价，不先继续调频率评分。

[导师18项直觉及检查](../../../Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/20261020_20261019T164834Z/mentor_intuitions_audit_cn.md) · [Anchor](../../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/15_24_frequency_composition_common_path_anchor_cn.md) · [Protocol](../../../Projects/from-attention-to-search/main/experiments/A15/15_24_frequency_composition_common_path/20261020_20261019T164834Z/protocol_cn.md)。

## 完成与停止

恢复任务pt-4kefocs4已SUCCEEDED；原文件锁失败pt-gzle2ypd保留，未重训已完成两模型。8/8模型、五图、源表、文本与10项输出资产登记已完成；累计主动远程计算约3.82分钟。未commit/push、未改Focus科学状态、未启动新参数扫描或下一训练。
