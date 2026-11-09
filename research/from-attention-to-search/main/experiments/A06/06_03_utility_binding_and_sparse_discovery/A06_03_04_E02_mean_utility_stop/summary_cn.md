# A06_03_04_E02 Utility-Certified Audition Stop：结论摘要

## 确定结论

all-position **均值 utility certificate** 很省计算，但还不是安全停止证书：

- 中位第 `220.5` 步触发；
- 相对固定 600 步节省 `63.25%` auditions；
- 最终纠正 `127/128`，已纠正保持率 `100%`；
- 但 `24/128 = 18.75%` 在持续 route correction 前提前停止，超过预注册 `5%`。

task-position oracle utility 几乎相同：premature stop `17.19%`，纠正
`127/128`，节省 `62.83%`。因此失败不是背景位置造成的。score-only 从不触发；
generalist 也从不误触发。

结论是：**均值 utility 能检测整体 phase transition，但不能保护 routed
population 的错误尾部。** 已正确的大多数样本可以主导 incumbent 的平均 utility，
掩盖仍路由错误的少数样本。

![停止规则权衡](figures/stopping_rule_tradeoff.png)

utility rule 同时具有接近完整的最终纠正和明显计算节省，但 premature-stop 安全
约束没有通过，不能因最终分数高而忽略。

![停止后的 margin 轨迹](figures/certified_stop_margin_trajectories.png)

均值轨迹与 oracle 很接近，但聚合中位数看不到产生 premature stop 的少数 task
单元；下一步必须直接约束尾部。

## 下一决策

将均值证书改为分布鲁棒证书：比较 lower-tail quantile 或条件风险价值
（conditional value at risk，CVaR），要求 premature stop 降到 `5%` 以下，同时
保持至少 `30%` audition saving。当前问题是 route-population heterogeneity，
不是 MTP semantic-credit source。

边界：当前规则是强 predictor 和工程候选，不是安全证书；尚未证明 joint training、
预训练 LLM、可扩展统计状态或系统吞吐。
