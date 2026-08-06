我们现在开始下一轮实验执行。请不要把这轮任务理解成一次普通的“跑实验”，而要把它理解成：基于当前 checkpoint 的主线建模，完成一个最小、封闭、可判别的 mechanism audit。

请先完整接受下面这些背景，不要擅自改写问题。

一、项目主线

- 项目主题是 `MoE Router for Continual Learning`
- 我们当前不是在泛泛比较 router，而是在判断：
  1. `quadratic_nosvd_debias` 是否真的 learned variance routing
  2. 如果没有，就不应直接进入 CL necessity 判决
  3. 如果有，再考虑最小 forgetting test

当前主线建模已经固定为：

`Architecture -> Mechanism -> Assignment -> Geometry -> CL Outcome`

对应关系：
- Architecture: `quadratic_nosvd_debias`
- Mechanism: `variance routing`
- Assignment: `specialization`
- Geometry: `low-rankness / low overlap / low SI`
- CL Outcome: `lower forgetting`

二、当前稳定定义

1. `Variance Routing`
- 不是“架构里有 x*x 项”就算 variance routing
- 只有当 quadratic 的二阶项在分域判别中主导了 logit margin，才算真的在按方差分发

2. `Expert Specialization`
- 不是高 margin，也不是低 rank
- 它首先是 assignment phenomenon
- 推荐主指标：`NMI(E,C)` 或 `MI(E;C)`，并同时检查 `load balance`

3. `Expert Low-rankness`
- 不是架构属性
- 是 routed feature covariance 在 expert 内部占据低维子空间的几何状态
- 推荐主指标：`r_{0.9}`
- `ED_comp` 不再作为主指标

三、本轮真正要回答的问题

本轮只回答一句话：

`quadratic_nosvd_debias @ ckpt40000` 到底有没有 learned variance routing？

如果这个问题没回答清楚，我们就不应该直接把它拿去做 CL forgetting verdict。

四、固定比较模型

- `linear_running_center`
- `acp_lite`
- `quadratic_nosvd_debias`

五、本轮 Experiment Type

`static_proxy_audit`

更准确地说，是：

`mechanism_audit_before_cl`

六、本轮必须输出的三个核心量

1. `rho`
- quadratic 的一阶/二阶 attribution ratio
- 目标：判断二阶项是否主导分域 margin

2. `NMI(E,C)`
- 目标：判断 assignment-level specialization

3. `r_{0.9}`
- 目标：判断 expert 内部 low-rank geometric state

七、本轮不要做的事

- 不要训练新 router
- 不要扩展到 TRACE benchmark
- 不要直接做 two-task forgetting test
- 不要新增一堆模型
- 不要再回到 `acp_on`

八、你现在的任务

请严格按以下结构输出：

1. Task Restatement
- 用一句话准确重述本轮唯一问题

2. Metric Operationalization
- 明确写出：
  - `rho` 怎么定义、怎么计算
  - `NMI(E,C)` 怎么定义、数据从哪里来
  - `r_{0.9}` 怎么定义、对哪个 covariance 计算

3. Implementation Plan
- 说明你准备复用哪些已有脚本或结果
- 说明需要新增哪些脚本
- 说明输入输出路径

4. Output Contract
- 列出最终必须产出的文件：
  - per-model metrics
  - aggregated summary
  - markdown report
  - result card

5. Decision Rule
- 明确写出：
  - 如果 `rho <= 1` 或不稳定，意味着什么
  - 如果 `rho > 1` 且 NMI / geometry 也支持，意味着什么
  - 什么时候才允许进入下一步 two-task forgetting test

6. Immediate Execution
- 如果没有阻塞，就直接开始实现
- 如果有阻塞，只允许提出最小必要的 1-3 个问题

九、最终必须额外输出

请在结果末尾额外输出：

`Experiment -> Theory Result Card`

必须包含：
- Scope
- Positive Evidence
- Negative / Null Evidence
- Reliability Grade
- Theory Result
- Recommended Next Action

十、你必须记住的总原则

你这轮不是在证明 quadratic 强，而是在检查：

`quadratic_debias` 是否真的在按方差分发。

只有这个问题回答为“是”，下一轮我们才进入最小 Continual Learning forgetting test。
