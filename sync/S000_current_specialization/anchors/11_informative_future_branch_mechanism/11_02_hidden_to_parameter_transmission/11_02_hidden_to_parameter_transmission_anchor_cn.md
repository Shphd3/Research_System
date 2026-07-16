# 隐藏状态到参数传递 Anchor

状态：已完成；在受控 Transformer 设置中得到条件性支持。

Thinking Card source: [11_02_hidden_to_parameter_transmission_thinking_card_cn.md](11_02_hidden_to_parameter_transmission_thinking_card_cn.md)

## 1. 问题定义

### 术语解释

| 术语 | 通俗含义 | 具体对象 | 为什么重要 | 不能证明 |
|---|---|---|---|---|
| 隐藏到参数传递 | 共享参数能否沿有用方向改变隐藏状态 | $J^Tv$ | 把表征理论连接到实际训练 | 自然语言收益 |
| 参数语义速度 | 参数一步更新造成的任务 margin 一阶变化 | $-\langle\nabla_\theta M,\nabla_\theta L\rangle$ | 主指标 | 长期收敛 |
| 直接路径 | MTP 从较早决策状态预测信息目标的损失 | $L_D$ | MTP 特有增量 | 净更新一定为正 |
| 背景项 | 同一参数上其余位置和目标的损失 | 各分量的带符号速度 | 显示干扰 | 唯一普适原因 |

**唯一决策问题：** 加入普通的全位置损失后，直接隐藏状态信号还能否通过共享 Transformer 参数传递？

## 2. 物理先验

1. 只有编码器参数能沿任务方向改变状态，隐藏状态理论才对训练有意义。
2. 全位置 NTP 会在更晚位置看到同一答案；MTP 增加的是更早路径，不是独占信息。
3. 净更新是直接、晚到语义、局部以及其余背景分量的带符号和。

## 3. 可证伪假设

在同一检查点，直接分量为正并能预测真实小步更新；完整净分量可能因为背景干扰而在个别种子中为负。

若直接参数速度为零，或有限步变化不服从局部预测，则解释被推翻。

## 4. 数学模型

令 $M$ 为任务 margin，把全位置损失分为

$$
L^{all}=L_D+L_I+L_S+L_R.
$$

每个分量的作用为

$$
G_c=-\langle\nabla_\theta M,\nabla_\theta L_c\rangle,
\qquad
G_{total}=G_D+G_I+G_S+G_R.
$$

$G_D$ 是较早的 MTP 路径，$G_I$ 是较晚的标准 NTP 路径。

## 5. 计算实现

使用一层因果 Transformer，冻结词嵌入和输出头，只训练共享编码器。先验证决策位置的参数传递，再在同一检查点把所有合法的全位置损失逐项分解。

## 6. 最小证伪测试

1. 检查 $G_D>0$ 且参数可达性非零。
2. 比较预测与真实一步 margin 变化。
3. 报告 $G_D,G_I,G_S,G_R$ 及净符号，不隐藏不利种子。

## 7. 当前证据

决策位置实验中直接传递在 5/5 种子为正，且准确预测有限步变化。全位置实验中，$G_D$ 在 5/5 种子为正并大于 $G_I$，但其余损失在一个种子中使净速度反转。见[决策位置传递](/Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E01_semantic_tangent_transmission/summary.md)、[全位置分解](/Projects/from-attention-to-search/main/experiments/A11/11_02_hidden_to_parameter_transmission/A11_02_01_E02_all_position_path_decomposition/summary.md)与[子锚点 11_02_01](subanchors/11_02_01_reachability_and_background_sign_anchor.md)。

## 8. 结论边界与下一决策

可支持：受控模型中，较早的信息性 MTP 路径能通过共享参数实现，并可与 NTP 的较晚路径分离；背景项有正有负，因此直接帮助不等于净训练一定受益。

不可支持：自然语言效率、净梯度普遍为正或下游使用。

**唯一下一决策：** 检查形成的方向经过状态转移到标准答案位置后是否仍然有用。
