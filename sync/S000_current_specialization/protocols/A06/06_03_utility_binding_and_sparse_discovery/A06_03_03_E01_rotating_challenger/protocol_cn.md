# A06_03_03_E01 有限 Challenger 与语义信用联合 Router：实验协议

目的：检验“正确位置的路由信用”和“有限的未选专家效用覆盖”是否共同足以纠正
错误路由。

完全复用 A06_03_02_E02：learned specialists、rank 2/4、冻结表示与专家、Router-only
SGD `0.001`、300 步、32 seeds、四任务。

每个排名从完全相同参数运行五个条件：`full_top1`、`task_top1`、`full_pair`、
`task_pair`、`task_soft`。

pair 条件只计算当前 top-1 和一个 challenger。challenger 按 seed-specific 随机
排列在另外三个 expert ID 中轮换；不读取任务、target 或有用专家编号。训练时在
两个候选内重新归一化概率，评估始终读取普通 top-1 identity。

主判据：task-pair 在 rank 2/4 均至少纠正 `90%`；rank 4 比 full-pair 和
task-top1 各高至少 50 个百分点；二因子交互的 seed-clustered 95% 置信区间下界
大于 0。task-soft 阳性对照必须至少 `90%`。

有效性守卫：静态排程对每个 selected expert 的三个非选 expert 严格每三步各出现
一次；纠正后 wrong-state 被截断，因此实际条件包含率只作描述；pair 每步最多两个专家
前向；继承 A06_03_02_E02 的专家效用、排名、间隔、负载、状态配对和有限值守卫；一般
专家不得形成任意目标绑定。

边界：通过只能证明受控联合充分性，不能证明 MTP estimator、自然语言
specialization 或部署效率。
