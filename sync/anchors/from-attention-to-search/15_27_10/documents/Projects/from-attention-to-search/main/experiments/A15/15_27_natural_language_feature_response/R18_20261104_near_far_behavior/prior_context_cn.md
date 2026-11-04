派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior/prior_context_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R18_20261104_near_far_behavior/prior_context_cn.md)；研究修改仍回到原件。

---

# 前置来源与复用审计

已通过read_thread读取三个用户指定livechat，另读相关对话记忆、项目规则／路线、15_27主Anchor、R09与距离分支、R17_D1及S06／S07／S09结果。所有科学结论由原owner持有。

学长《1027-交流》原文现已完整核实：固定同一token，比较不同语境的feature变化，变化大称“长程”、变化小称“短程”，再建议对token做某种汇总。没有给出变化的精确统计、实际token距离或答题标准。因此它是上下文敏感性的定义，本轮是另一种实际距离下的行为验证。两个附件副本SHA一致，原文和恢复收据在执行侧evidence。具体原文在评分开始后找到；当时已按项目定义冻结相同区分，没有修改任何文本、划分、分数、阈值或实验范围。《1026长短程修订转写》还明确保留了操作定义待明确，不能代填。

R09实际240token、目标239、核心末端与目标的索引差16/32/64/96/144，测feature响应而非答案。原36复现成员中只有9个在新近距两结尾保留原方向，不能把全部失配称距离衰减。旧距离是索引差，本轮排除两端，所以相同端点的数字相差1。

近期R17_D1无答案完整序列原生续写73/96、问答50/96；问答含两个选项词，且语境和观测位置一起改变。S06属性猫3/8、狗8/8，说明表征差不能代替任务成功。S07有小的分数效应但候选判断仍16/16不变；强制候选词也不是全词表首选，区分候选评分与自由生成。S09发现边际参照解释大量重叠差，另有独立联合统计；都不证明本轮事实利用。原科学接受／下一步Unknown均保留。

复用官方Base权重／tokenizer与已检查S06CPU前向和完整序列评分。改编固定320前缀、2×328形状、物品完整词偏移和两候选行为；不复用SAE hook、probe、训练、Dense或干预代码。现有HF依赖4.53.3和Torch2.3.0a0可用，无下载。完整源路径、哈希、检索时间、入口检查与旧问题边界见[英文审计](prior_context.md)和evidence/referenced_chats_read.json、source_recovery.json。
