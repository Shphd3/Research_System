# A06_03_04_E01 稀疏 Audition 占空比：结论摘要

## 确定结论

固定低频 audition 不能可靠地从 rank 4 发现有用专家：

- \(\rho\le1/4\)：全部 `0/128`；
- \(\rho=1/2\)：`79/128`，即 `61.7188%`，95% CI
  `[53.9063%,69.5313%]`；
- \(\rho=1\)：`128/128`。

但 audition 不需要永久保持。\(\rho=1/2\) 和 \(\rho=1\) 中所有已纠正单元，在关闭
audition、继续 200 步普通 top-1 后均保持，保持率 `100%`。

因此支持的是**先发现、后利用**的相变：错误身份阶段需要连续反事实 expert utility；
一旦有用专家越界成为 top-1，普通 top-1 会继续加固，而不是破坏它。

![占空比前沿](figures/duty_cycle_frontier.png)

当前测试中，平均激活专家数低于 2 的固定策略都未达到 `90%` 可靠纠正门槛。

![Margin 动力学与保持](figures/margin_dynamics_and_retention.png)

\(\rho\le1/4\) 的 margin 始终为负；\(\rho=1/2\) 与 1 越过零点后，关闭 audition
反而继续增厚 margin。这说明 top-1 的作用依赖当前位于哪个身份盆地。

## 理论更新

初始中位 selected-only pressure 为 `-2.6052`，audition pressure 为
`+12.1621`，局部公式预测 \(\rho_c=0.1802\)。实际直到 \(\rho=1/2\) 才出现部分
纠正，且仍未达到可靠门槛。单个 step-0 平均压力不能预测有限时域 discovery；
梯度场随 route identity、候选概率和累计 margin 改变。

## 下一决策

不再继续测试全程固定低频 audition。下一 Router 应在发现阶段连续 audition，
然后依据**无标签功能优势证书**停止。需要检验该证书能否接近 oracle crossing
时刻停止，同时避免错误专家上的 premature stop。

边界：没有证明所有更长 horizon 的低占空比都失败，也没有证明预训练 LLM 必须
连续 audition，或现有无标签停止规则已经有效。
