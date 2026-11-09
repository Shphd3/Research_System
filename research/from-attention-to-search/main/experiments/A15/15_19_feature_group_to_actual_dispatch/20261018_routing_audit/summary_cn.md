# 低频 feature 出现后，为何没有到达负责专家？

[完整分析](detailed_cn.md) · [用户 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_19_feature_group_to_actual_dispatch/15_19_feature_group_to_actual_dispatch_anchor_cn.md) · [用户 Protocol](protocol_cn.md) · [四图读法](figures_cn.md) · [12张文本卡](text_cases_cn.md) · [唯一下一决策](next_decision_cn.md)

**本轮证据更支持先明确并校准评分，而非先认定必须重分组。** 原评分为什么压过低频组已定位；有限共现约束不能迫使当前零接收。但没有证明全局分组可行，也没有验证新评分或学习收益。这是 AI 的有界建议，研究者判断待定。

## 目的与比较对象

只回答“低频 feature 已激活，为何完整输入没有进入名单指定的专家”。负责专家是名单安排，不代表它已学会该内容。固定 top-1 每个位置只送一个专家，不能将同一输入的各 feature 分拆。

复用冻结 Qwen3-0.6B Base／最终14选定层 CrossCoder 的既有缓存。A为原始概率等宽八段；B1/B2是保持八组人数的原随机名单，各用自己的去向。TRAIN 130,712位置，EVAL 65,402位置；可靠池9,615项，原低频964项。EVAL只是已观察过的留出位置复核，文档独立性未知。

## 三条实测证据

**1．名单分组没有落实成逐 feature 接收。** A的964个低频 feature 在两侧负责专家接收率全部为0。EVAL中B1/B2的等权平均接收率分别为4.44%／10.30%，仍有122／48项零接收；有正接收不等于学得更好。A0完全无输入，所以它的专家内频率 q 是NA，不能记成0。

![图1：实际接收与零接收目标](figures/figure1_actual_reception.png)

[源表：各专家接收与组内目标](tables/expert_summary.csv)；[按 feature 等权和按事件加权汇总](tables/group_summary.csv)。图1上排是输入位置比例，下排是各名单组内零接收 feature 比例。

**2．低频命中没有赢得评分竞争。** 原评分为组内所有成员的 decoder 范数加权激活均值。TRAIN含低频 feature 的95,544个位置，赢家减低频所在A0的平均分差为0.567492；其中原高频名单C的分差为+0.569428，非C为−0.001935。低频组有响应，但原始幅度、频率和名单构成共同作用，仍被压过；本轮没有拆出它们各自的独立因果效应。

仅将C的评分项置零，会把全部位置送进A0。这不是可用改法：A的组1–7全部由C构成，删项使七组机械归零，原来有正接收的另25项反而失去负责专家接收。不能把高频项当噪声删除。详见[评分分解](tables/winner_vs_A0_margin_components.csv)与[代价](tables/frequency_band_costs.csv)。

**3．已查到的共现取舍不能解释“必须为零”。** 从TRAIN选3个固定案例，每条规则最多选9对跨负责专家的高重叠伙伴，再读EVAL：共27个固定对。A配对允许的共同接收率上界在TRAIN为99.18%–99.61%，EVAL为98.84%–99.72%。这些界只排除极高的同时覆盖要求，不能迫使低频接收为0；有限配对也不证明全体可行。

![图4：固定随机文本位置与原始评分](figures/figure4_text_and_score.png)

三个案例9297、1133、2704各有3随机＋1高激活文本；12个A位置都进入专家7。图4使用各ID的第一个冻结随机样本。当前token与下一token标签分开，完整前文和36组评分敏感性记录见[文本卡](text_cases_cn.md)。

## 认识更新与下一步

过去只知道“专家负载失衡”；现在明确了“逐 feature 零接收 → 原组均分竞争 → 高频名单项的胜出差额”这条计算路径。**AI建议只推进一个问题：保持名单和top-1，先定义评分应比较什么，再登记一次有代价约束的评分校准比较。** 需要先决定逐 feature 接收要求，以及允许其他组损失多少接收。没有运行校准、重分组或学习训练。

核心计数、200次上下文块描述性重采样、全部低频×C伴随表、评分虚拟诊断、12张文本卡和有限冲突检查均已完成。完整机器表与回执在[执行目录](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/routing_audit_20261018T143950Z)。本轮使用CPU，未新增GPU／模型前向／训练。执行细节、已完成与未执行清单、实际资源见[Detailed](detailed_cn.md)。
