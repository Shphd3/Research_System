派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_25_03_context_computation_dependency/R01_bounded_execution_20261026/summary_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_03_context_computation_dependency/R01_bounded_execution_20261026/summary_cn.md)；研究修改仍回到原件。

---

# 执行结果：当前数据未通过候选支持门槛

**结论：本轮停在数据资格阶段，尚未检验C→R功能依赖。** 这是按冻结规则执行后的“证据不足”，不是H1被否定，也不是H2／H3成立。

目标是在同一token不同上下文中，比较第14层C削弱对第28层R及预测的特异作用。用户已明确授权执行原协议；本轮没有降低其样本门槛或更换数据。

| 数据资格 | 协议要求 | 实际结果 |
|---|---|---|
| 同一token对应两种不同续词，每类来自独立对话 | 每类至少64文档；每token每文档只留一处 | 没有合格token；较少一类的支持最多43文档 |
| 再按来源、答案位置与前缀长度匹配 | 两类同分层、同权重 | 最多各23文档；不补样、不换token |
| 合格对象进入C/R与测量资格 | 先有合格上下文对象 | 未进入；局部R测量可靠性仍未知 |

实际读取原TRAIN1024对话／85548答案位置，按特殊token、词片和16个后续答案目标筛选，留下53390位置；每token每文档固定取一处后有35546个上下文。4024个token类型仍有至少两种续词，但没有达到上述门槛。EVAL与TEST本轮均未读。

支持最多的匹配对象是词片` in`，两类续词为` the`与` a`：按固定去重规则分别91／43文档，分层平衡后各23文档。它只是事后说明数据缺口的实例，不是合格C／R候选。[真实文本示例](examples_cn.md)仅说明该数据构造，没有feature激活或干预结论。

**没有执行的部分：** C/R特征选择、源／后层真实激活前向、层局部测量资格、C削弱及匹配对照。所有功能指标与不确定性均为NOT RUN，不填0、不画效果图。没有依据为“共同计算是否支持上下文计算”作正负裁决。

资源与资产：模型前向0／12000，训练0，新资源0；未加载模型或CrossCoder张量，未改权重。原TRAIN、tokenizer身份与冻结协议／源码哈希核对通过。原协议门槛保留，未转用DCLM、增加数据或改变分层。

本轮已按既定停止分支收束。当前不足仅针对这份Tulu数据在冻结筛选规则下的可检验性；不说明所有现有文本或CrossCoder都不能用于此问题。

[逐项记录](detailed_cn.md) · [前10项支持表](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_03_context_computation_dependency/R01_bounded_execution_20261026/tables/token_support_top10.csv) · [完整4024项原表](../../../../../../../../UNAVAILABLE.md) · [原始停止回执](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_03_context_computation_dependency/R01_bounded_execution_20261026/provenance/support_receipt.json) · [冻结协议](../R00_readonly_design_20261026/protocol_cn.md)。
