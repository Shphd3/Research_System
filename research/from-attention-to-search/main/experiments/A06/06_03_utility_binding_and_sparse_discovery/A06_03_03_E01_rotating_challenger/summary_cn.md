# A06_03_03_E01 有限 Challenger Router：结论摘要

## 确定结论

在不知道任务标签、有用专家编号和目标身份的情况下，每步只额外计算一个轮换
challenger，已经足以逃离错误路由盆地。

- 有用专家初始第 2 名：full-pair `128/128` 纠正。
- 有用专家初始第 4 名：full-pair `125/128`（`97.6563%`）纠正。
- task-pair 在两个排名均为 `128/128`。
- full top-1 在两个排名均为 `0/128`。
- generalist 控制的任意目标绑定为 `0/128`。

因此，**有限候选效用覆盖足以发现有用专家；oracle 任务位置 mask 不是最终纠正的
必要条件。** 任务位置信用仍能提高效率：rank 4 的中位纠正时间从 full-pair 的
`192.5` 步降到 task-pair 的 `118.5` 步；中位累计遗憾从 `0.6810` 降到
`0.4582`。

![纠正率二因子结果](figures/factorial_correction_rates.png)

pair coverage 是决定性因素。rank-4 的信用来源与 coverage 交互仅为 `0.0234`，
95% 置信区间 `[0,0.0547]`，不支持“二者必须联合才有效”。

![rank-4 发现轨迹](figures/rank4_discovery_trajectory.png)

full-pair 和 task-pair 都持续提高有用专家概率，top-1 两个分支保持停滞；任务
位置加权更快，全 soft 最快。

## 假设更新

- 联合方法充分，但联合必要性不成立。
- 只有信用不足：rank-4 task-top1 为 `0/128`。
- 只有有限 coverage：支持。
- 两专家 coverage 不足：证伪。

## 下一决策

下一步不应先设计更复杂的语义 Router，而应测最小 audition 频率：challenger
可以多稀疏地出现，仍保持 rank-4 纠正与低遗憾。MTP 语义信用现在是用于选择
“何时 audition”的效率增强器，不再是身份发现的必要前提。

边界：当前没有证明预训练 LLM specialization、自然语义专家、端到端计算收益或
最优探索排程。
