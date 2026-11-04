# 一句话前面的 feature，到后面是延续、关联出现，还是不再出现？

problem_key: `sentence_feature_continuation`
anchor_id: `15_28`
question_state: `USER_ACTIVATED`
design_state: `EXACT_PROTOCOL_CONFIRMED_FOR_BOUNDED_CACHE_ANALYSIS`
task_state: `CACHE_ANALYSIS_AND_LOCAL_DELIVERY_COMPLETE`
result_state: `EXPLORATORY_RESULTS_AVAILABLE_SAE_H2_BLOCKED`
human_result_judgment: `Unknown`
question_closure: `Unknown`

## 问题、假设与边界

研究者于 2026-10-28 激活这个独立问题：一句话中，前面 token 激活的
feature，后面是否仍以相同坐标出现，或与后面活跃坐标通过旧图相连？
这种联系能否超出高频、重复词面、同领域背景和活跃数量差异的解释？

H1 问同一坐标是否延续。H2 问不同坐标是否沿旧图相连，特别是原坐标已经
不激活时。位置靠后、箭头朝向都不定义语义层级。SAE 与 CrossCoder 分别使用
各自的原生坐标。A15_27 原来关于固定目标词含义响应的问题与结果保留。

## 必要比较与已有证据

一个缓存分析包含三个步骤：

1. 核对文本、token 位置、原生字典、DCLM 频率组和旧图；先固定句界与匹配规则。
2. 比较句内延续和正反向关联覆盖，与同领域、不同文档对照及保边际随机基线比较。
3. 结合三类图、两个真实例子、一个反例，说明匹配覆盖率、文档级区间与缺项。

当前核查找到 120 篇数学／生物文档的完整逐 token 缓存。两字典都能做 H1；
CrossCoder 旧图兼容。SAE 旧图的激活接口未完成等价资格核查，单独阻塞其 H2。
以上是初始资产核查。现已完成本轮缓存统计，结果由下方 Summary／Detailed 持有。文本已经用于旧轮分析，本轮属于探索性复用。

后续分析完成标准是一页事实结论、三类图或对应分支的明确缺项、真实文本例子、
数据表、脚本、来源与边界。超过对照支持有界坐标延续或旧图关联；只在高频／重复词面
成立时优先采用这些解释；校正后消失则削弱当前测量下的额外句内联系。
缺少匹配、区间过宽或图不兼容意味着证据不足，不能解释成模型遗忘。

## 研究者判断与唯一下一决定

目的、假设、竞争解释、三类图和缓存范围来自研究者。研究者随后明确要求按已讨论思路执行缓存分析；对应 Protocol 记录了执行确认。统计、随机基线和三类图已交付，缺项与低覆盖保留。Summary 中的解释是有界 AI 解读，不代替研究者机制判断。

**唯一下一决定：** 看完有界缓存结果后，研究者决定某个仍成立的模式是否值得做后续
上下文替换干预。本轮不执行、也不预先批准该干预。继续讨论的入口是结果 Summary；不自动进入新干预。

## 来源

[Anchor](../problem_anchors/15_spectral_representation_and_functional_routing/15_28_sentence_feature_continuation/15_28_sentence_feature_continuation_anchor_cn.md)
· [Protocol](../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/protocol_cn.md)
· [准备记录](../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/preflight_cn.md)
· [一页入口](../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/one_page_cn.md)。
[本轮 Summary](../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/summary_cn.md) · [完整事实与证据](../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/detailed_cn.md)。科学判断与关闭保持 Unknown。
