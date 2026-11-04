派生阅读副本；原件位置：`Projects/from-attention-to-search/main/focus/focus_crosscoder_context_computation_dependency_cn.md`。
[精确原始文件](../../../../../sources/Projects/from-attention-to-search/main/focus/focus_crosscoder_context_computation_dependency_cn.md)；研究修改仍回到原件。

---

# CrossCoder同token上下文计算依赖

problem_key: 同一token不同上下文的C到R功能依赖
question_state: 主问题仍未回答
task_state: 已在预定数据门槛处完成本次执行
design_state: 本轮明确继续执行指令已接受原协议
result_state: 数据支持不足，功能检验NOT_RUN

唯一问题：同token不同上下文中，第14层共同激活候选C的削弱，是否相对匹配干预影响第28层上下文方向R及预测？本问题一个核心实验：先确认候选和局部测量资格，再冻结对象作配对干预；最多2token，不训练、不新增资源。

用户已明确授权执行原协议。其第一道数据门槛未通过：每类需64个独立文档，实际较少一类最多43；分层匹配最多23／类。没有合格token进入C/R发现、局部读数资格或干预；前向0，EVAL／TEST未读。H1／H2／H3尚未检验，不能写成阴性。当前授权执行按预定停止分支完成，不关闭科学问题。

证据依赖顺序是：足够上下文对象→可信层局部读数→R及预测相对两类对照的配对效应；联合z几何不能替代后两项。下一项研究者决定只是未来是否修订数据构造；本轮没有启动修订、转用数据或降低门槛。

[当前结果](../experiments/A15/15_25_03_context_computation_dependency/R01_bounded_execution_20261026/summary_cn.md) · [冻结协议](../experiments/A15/15_25_03_context_computation_dependency/R00_readonly_design_20261026/protocol_cn.md)。准备阶段Focus原始字节保存在本轮provenance；原Anchor／Protocol科学体不变。
