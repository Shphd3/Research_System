派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/protocol_cn.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R16_20261102_layerwise_head64_intervention/supplements/20261104_equal64_bands_mean_control/protocol_cn.md)；研究修改仍回到原件。

---

# 等维谱段与均值对照：冻结协议

已获当前请求直接运行授权。沿用原R16全部模型、文本、28层PCA和两个干预范围。16段：1—64、65—128，依次至961—1024，每段64维。

逐层比较：①训练均值+(中心化表征在该段上的投影)；②仅中心化投影、不加均值。另测零向量和全维减均值；复用原均值与随机64维参照。全维减均值不是身份对照。

原首选保持率为主指标；真实后继损失、与原分布KL、候选ID/概率、保留能量及扰动为辅助。175篇700位置主面板与37篇the面板分开。先文档内平均再文档等权，2000次文档重采样，区间为逐点探索性区间。

先完成身份重建、旧头64重放、真实hook与后续网络一致、因果mask检查，再执行全矩阵。最多两张已授权5090spot，无训练、无新PCA、不动H100。固定旧9例展示，不能根据漂亮输出改谱段或标签。

等维仍不等能量。不加均值同时改变共同偏置和网络工作点；结果不直接证明常见/细语义排序或后续补偿。完整精确协议见protocol.md，来源与索引见manifest.json。

实现修订E1：首次检查把批量1的真实前向与批量5的续算相比，出现0.082834nat差异，原失败保留。改为同形状核查，再单独评估批处理数值差异；超过原容差或改变首选则全条件退回逐条件计算。未扩大容差，无评估结果被挑选。

E2数值修订：5篇只属于the面板的单位置文档，其原批量形状不同；按原批量重算全部条件、保留原版，现737对照均精确一致，主面板保持率与区间完全不变。详见amendments.md。
