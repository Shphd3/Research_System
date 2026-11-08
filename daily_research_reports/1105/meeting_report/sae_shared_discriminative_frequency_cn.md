# 2026-11-05组会：粗细类别的共同与区分feature频率

## 目的

检验导师的方向性直觉：共有和区分的feature是否随粗细粒度落入不同频率范围。频率从独立自然题干估计，不能由本次共现次数自己定义。

## 结论

**共有相对偏高频，但还不能概括为“共有高频、区别低频”。** 新16家族中，跨大类共有成员的高频占比Attention43.1%、MLP67.2%；猫狗35.6%/60.1%、汽车自行车41.8%/61.0%。四个主要差值3个通过家族检验，Attention交通差未分辨；常见成员机会和家族背景仍可解释一部分。

**细类区别没有稳定地转向中低频。** 猫狗只锁出2/1个出现率候选，频率梯度不足；车辆各9个，只有3/4个在参考中支持充分。反例MLP24399：参考10/384、低频，却在新动物16/16、交通工具0/16激活，同义/属性也复现。高频8048也有汽车–自行车区别，但属性措辞减弱。

**区别不只来自换成员。** 同一共同名单的相对强度3/4显式主条件复现；另1个11/16不足。新改写猫狗两SAE方向反转；保边际联合结构4个主区间均跨0。不能用这批数据推出普遍语义组合或真实路由机制。

![共有与区分的频率](sae_frequency_assets/main_frequency_shared_discriminative.png)

读图：每行合计100%；左是真实交集组成，右是发现侧固定候选，含未复现成员。深蓝高频、浅蓝中低频；橙灰不能叫低频。右侧猫狗候选太少，不能下频率分工结论。

## 机制直觉与假设

频繁坐标提供共享底座是可解释的描述；不过它们也能通过强弱区别文本，较低频坐标也能区分粗类。因此频率不必与“共有/区分”一一对应。H1局部支持，H2未支持跨措辞一致方向且猫狗不足，H3局部支持成员/强度描述，超边际联合证据不足。这是AI操作判定，科研接受Unknown。

## 实验分析与边界

复用S06原384行/两SAE缓存，原留出新统计是探索。先锁定新规则/名单，再前向新16家族×6类×4措辞384条。频率用S09固定384独立题干在同一Description冒号处提取；>=8次支持后分三分位，其余单列。每feature全部原始值与逐familyCSV保存；以家族bootstrap/置换，单feature另BH。4链exactrow32/列次数零模型、幅值/总量、措辞和最简词组控制均执行。无训练/功能干预。

频率高度依赖取样位置：同MLP24399在正文参照是高频，末冒号是低频。新改写猫狗行为弱，参考只三种题干；词面、格式和模型能力没有排除。两份指定最新会议原文未取得，方向按当前用户转述记录。完整报告、全部数据与可编辑图由执行S10报告拥有。

## 一句话讲法

“共有相对偏高频，但粗细区别没有稳定的高低频分工；同一成员的强弱也能区分文本，不过换措辞会改变方向，所以还不能据此设计专家分发。”

**AI建议唯一下一问题：在覆盖更充分且位置匹配的独立参照中，粗细区分成员的频率分布能否在行为可靠的新措辞上保持？**

[完整中文报告](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/summary_cn.md) · [案例册](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/casebook_cn.md) · [原始表与配置](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105)。
