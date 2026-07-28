# A06_03_04_E01 稀疏 Audition 占空比：实验协议

**唯一问题：** 在 full-LM 训练下，challenger 可以多稀疏地执行，仍可靠地从
rank 4 找回有用专家？

## 固定设置

- 复用 A06_03_03_E01 learned specialists 与 rank-4 Router。
- 冻结表示和专家；Router-only SGD `0.001`。
- discovery 600 步；随后关闭 audition，用 top-1 再训练 200 步检查保持。
- 32 seeds、四任务。

占空比为 $\rho\in\{0,1/16,1/8,1/4,1/2,1\}$。audition update 计算当前
top-1 和一个轮换 challenger；其他 update 使用普通 weighted top-1。确定性累加器
均匀安排 audition，challenger phase 只在 audition 时推进，不读取任务、target 或
有用专家编号。平均激活专家数为 $1+\rho$。

初始状态测普通 top-1 pressure $P_S$ 与三种 challenger phase 的平均 audition
pressure $P_A$，预测：

$$
\rho_c=\frac{-P_S}{P_A-P_S}.
$$

该式只作局部预测，不用于修改实验网格。

## 主判据

最小可行 $\rho$ 必须同时满足：纠正率至少 `90%`；seed-clustered 95% 置信区间
下界至少 `85%`；停止 audition 后至少 `90%` 的已纠正单元保持；generalist 任意
绑定低于 `10%`。

- 若某个 $\rho<1$ 可行，且经验转折与预测 $\rho_c$ 相差不超过一个相邻网格，
  支持临界占空比模型。
- 若只有 $\rho=1$ 可行，说明必须持续 audition。
- 若 $\rho\le1/8$ 可行，平均激活专家数不超过 `1.125`。
- 若低占空比有效但局部压力预测偏离超过一个网格，必须改成状态依赖模型。

边界：不能据此证明真实 LLM wall-clock、many-expert 通信成本、MTP adaptive
trigger 或自然语言下游 specialization。
