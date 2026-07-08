# MTP 的长程语义表示边界与学习效率证据

## 0. 执行摘要

**研究问题：**

MTP在长程语义学习上是否比NTP更好；这次研究的是更具体的问题，它是否能更高效地让当前隐藏状态 $h_T$ 学到早期语义变量 $Z$？

**机制解释：**

把输入序列建模成：

$$
X=(\operatorname{BR}_Z,F_1,\ldots,F_L,U,A,S_Z).
$$

模型先读到决策前缀 $(\operatorname{BR}_Z,F_1,\ldots,F_L,U)$，形成当前隐藏状态：

$$
h_T=f_\theta(\operatorname{BR}_Z,F_1,\ldots,F_L,U).
$$

之后它要预测未来词元：

$$
Y_1=A,\qquad Y_2=S_Z.
$$

这里 $Z$ 是早期分支语义，$A$ 是所有分支共享的下一词元，$S_Z$ 是由 $Z$ 决定的第二个未来词元。

1. K=2 是最小证明对象。NTP 只需预测 $A$，所以不要求 $h_T$ 区分 $Z$；预测接下来两个词元时还要预测 $S_Z$。

$$
\mathbb E[-\log q_2(S_Z\mid h_T)]\le\varepsilon
\Rightarrow
I(h_T;Z)\ge H(Z)-\varepsilon.
$$

2. 一般 K 个未来词元预测只把第 2 个未来位置换成第一个有信息未来位置 $\tau$。

$$
\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}.
$$

如果 $K\ge\tau$ 且 $Y_\tau=S_Z$，则低第 $\tau$ 个未来位置损失推出：

$$
I(h_T;Z)\ge H(Z)-\varepsilon.
$$

3. 学习效率不是这个表示定理自动推出的；它还需要额外优化假设和学习曲线证据。

**主要结果：**

1. K=2 给出最小表示保证，K 个未来词元预测给出一般覆盖原则：**当预测范围覆盖第一个含 $Z$ 的未来位置 $\tau$，低于一个特定的损失阈值会迫使 $h_T$ 含有可线性读出的 $Z$ 的信息**。K=2 实验支持目标函数分离：只预测下一词元时 $Y_2$ 准确率为 `0.000`，预测接下来两个词元时 $Y_2$、分支替换、分支读出可达 `1.000`

2. 学习效率还没有无条件证明；现有证据只支持受控版本。K=2/A11_02 中存在NTP 和 MTO共享梯度冲突但没有观察到 $Y_1$ 性能受损；K=3 只是进一步验证“覆盖第一个有信息未来位置”后，在干净、只在决策位置训练中会更早恢复 $Z$。

**结论边界：** 当前不能证明 MTP 相对下一词元预测（NTP）在自然语言中更高效，也不能证明任意更大 K 都更好；能证明的是，在指定信息结构和低“有信息未来位置损失”条件下，$h_T$ 必须含有对应的长程语义信息。

**执行动作：** 下一步只需要补清楚效率桥梁：在什么梯度投影、步长和平滑性假设下，覆盖 $\tau$ 会减少达到 $Q\ge\theta$ 的训练时间；完成判据是命题可证明或对应实验可证伪。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 单位或公式 | 为什么影响当前判断 | 不能证明什么 |
|---|---|---|---|---|---|
| 多未来词元预测（MTP） | 用同一个当前状态预测多个未来词元 | K=2 预测 $Y_1,Y_2$，K=3 预测 $Y_1,Y_2,Y_3$ | 预测范围 K | 决定目标函数是否包含长程语义目标 | 普遍优于 NTP |
| 下一词元预测（NTP） | 只预测紧接着的未来词元 | 本线中对应 K=1，只预测 $Y_1$ | K=1 | 基线条件 | 不能学习长程信息 |
| 早期语义变量 $Z$ | 前缀中已经出现、但未来才需要的信息 | 受控分支身份 | 离散变量 | 被要求保留在 $h_T$ 中的对象 | 自然语言语义全部情况 |
| 当前隐藏状态 $h_T$ | 模型读完决策前缀后的表示 | 决策位置的 Transformer 隐藏向量 | 向量 | 表示定理和实验评估都作用在这里 | 后续所有位置的信息 |
| 第一个有信息的未来位置 $\tau$ | 第一个未来词元开始依赖 $Z$ 的位置 | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | 未来词元偏移 | 决定 K 是否覆盖有效监督 | 真实文本中固定唯一位置 |
| 有信息未来位置损失 | 预测第 $\tau$ 个语义词元的交叉熵 | $\operatorname{CE}(q_\tau(\cdot\mid h_T),S_Z)$ | CE | 低这个损失才能推出 $h_T$ 含 $Z$ | 任意总损失下降 |
| 语义恢复分数 $Q$ | 保守判断 $h_T$ 是否恢复 $Z$ | $Q=\min\{A,P,S\}$ | 0 到 1 | 防止只靠冻结读出得出假阳性 | 精确因果路径 |
| 到阈值时间 $T_\theta$ | 可靠达到语义恢复阈值的训练步数 | $T_\theta=\inf\{t:Q(t)\ge0.9\text{ 连续 }2\text{ 次评估}\}$ | 步 | 判断是否更早学到 $Z$ | 最终上限 |
| 早期曲线面积（early AUC） | 早期语义恢复曲线面积 | 0 到 3000 步的 $Q(t)$ 平均面积 | 分数面积 | 判断早期学习是否更稳定 | 梯度因果解释 |
| 全位置训练（all-position） | 每个有效位置都计算预测损失 | $\sum_t\sum_j\operatorname{CE}(q_j(h_t),X_{t+j})$ | CE | 检查更接近语言模型训练的边界 | 纯直接监督机制 |
| 只在决策位置训练（decision-only） | 只在当前决策前缀计算预测损失 | $L_K(h_T)$ | CE | 最干净地检验 $h_T$ 是否被目标直接监督 | 完整语言模型训练 |
| 共享梯度冲突 | 两个损失在共享参数上的更新方向相反 | $c=\langle g_1,g_j\rangle/(\|g_1\|\|g_j\|)$ | -1 到 1 | 说明目标可能拉扯同一参数 | 单独证明性能损害 |

## 2. 机制解释与建模

**核心模型：**

先把受控文本写成一个序列。早期变量 $Z$ 出现在前缀分支标记 $\operatorname{BR}_Z$ 中，中间填充词元 $F_1,\ldots,F_L$ 和决策词元 $U$ 本身不揭示最终语义答案；真正依赖 $Z$ 的语义词元被延迟到未来位置。

K=2 最小构造：

$$
X=(\operatorname{BR}_Z,F_1,\ldots,F_L,U,A,S_Z),
$$

$$
h_T=f_\theta(\operatorname{BR}_Z,F_1,\ldots,F_L,U),
$$

$$
Y_1=A,\qquad Y_2=S_Z.
$$

其中 $A$ 对所有分支相同，$S_Z$ 由早期变量 $Z$ 决定，且 $Z\mapsto S_Z$ 一一对应。因此：

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=H(Z).
$$

K=2 目标函数：

$$
L_2(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),A)+\lambda_2\operatorname{CE}(q_2(\cdot\mid h_T),S_Z).
$$

K=2 表示保证：

$$
\mathbb E[-\log q_2(S_Z\mid h_T)]\le\varepsilon
\Rightarrow I(h_T;Z)\ge H(Z)-\varepsilon.
$$

一般 K 个未来词元预测推广：

$$
L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
$$

定义第一个有信息未来位置：

$$
\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}.
$$

若 $Y_\tau=S_Z$ 且 $Z\mapsto S_Z$ 一一对应，则：

$$
K\ge\tau,\quad Y_\tau=S_Z,\quad \mathbb E[-\log q_\tau(S_Z\mid h_T)]\le\varepsilon
\Rightarrow I(h_T;Z)\ge H(Z)-\varepsilon.
$$

当前 K=3 实验只是该推广的一个实例：

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z,\qquad \tau=3.
$$

学习效率桥梁目前只是条件命题，不是已完成的无条件证明。定义语义恢复损失：

$$
R_\phi(\theta)=\operatorname{CE}(s_\phi(h_T(\theta)),Z).
$$

若额外未来位置梯度 $g_\tau=\nabla_\theta L_\tau$ 满足：

$$
\langle\nabla_\theta R_\phi,g_\tau\rangle\ge\gamma>0,
$$

则在小步长的一阶近似下，MTP 比 NTP 多降低约：

$$
\eta\lambda_\tau\gamma
$$

的语义恢复损失。这个桥梁还需要实验证明其假设成立。

**符号含义：**

- $Z$：早期语义变量，本实验中是受控分支身份。
- $h_T$：当前决策前缀的隐藏状态。
- $Y_j$：从当前前缀往后第 $j$ 个词元。
- $S_Z$：由 $Z$ 决定的未来语义词元。
- $\tau$：第一个让未来目标开始依赖 $Z$ 的位置。
- $q_j(\cdot\mid h_T)$：用 $h_T$ 预测第 $j$ 个未来词元的预测分布。
- $R_\phi$：从 $h_T$ 中恢复 $Z$ 的评估损失，用来定义学习效率桥梁。

**机制链条：**

1. K=2 中，NTP 只需预测共享的 $A$，所以不要求 $h_T$ 区分 $Z$；预测接下来两个词元时还要预测 $S_Z$，所以低第二位置损失会排除不区分分支的 $h_T$。
2. 一般 K 个未来词元预测中，同样逻辑只在 $K\ge\tau$ 时成立；如果 $K<\tau$，被监督的未来词元不含 $Z$，目标函数没有直接语义要求。
3. 学习效率需要额外优化假设：$g_\tau$ 必须实际降低 $R_\phi$，且不能明显破坏本地下一词元学习。

**当前问题分解：**

- 已关闭的问题：K=2 和 K 个未来词元覆盖条件下，低有信息未来位置损失是否迫使 $h_T$ 含有 $Z$。
- 部分支持的问题：覆盖 $\tau$ 是否在干净、只在决策位置训练中更早恢复 $Z$。
- 尚未关闭的问题：效率桥梁中的梯度投影假设是否真实成立。
- 最危险的替代解释：全位置训练中，K=1/K=2 可通过其他位置损失和共享参数间接恢复 $Z$，所以高 $Q$ 不等于直接监督。

## 3. 主要结果

**一句话总结：** 当前组会只讲两点：第一，K=2 到一般 K 个未来词元预测的表示保证；第二，学习效率只有受控证据和待证明的优化桥梁。

### 结果 1：在受控 K=2 / K 个未来词元构造中，低有信息未来位置损失可以保证 $h_T$ 含有长程语义变量 $Z$。

**机制对应：** 对应第 2 节的表示定理。K=2 是最小构造：$Y_1=A$ 不含 $Z$，$Y_2=S_Z$ 第一次含 $Z$；一般 K 个未来词元预测只是把这个位置从 2 推广到 $\tau$。

**指标或条件定义：** 有信息未来位置损失是第 $\tau$ 个未来目标的交叉熵，不是任意总损失。K=2 中 $\tau=2$，目标是 $Y_2=S_Z$；K=3 中 $\tau=3$，目标是 $Y_3=S_Z$。

**证据：** 理论上，K=2 若 $\mathbb E[-\log q_2(S_Z\mid h_T)]\le\varepsilon$，则 $I(h_T;Z)\ge H(Z)-\varepsilon$；K 个未来词元预测若 $\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le\varepsilon$，则同样有 $I(h_T;Z)\ge H(Z)-\varepsilon$。实验上，A11_01 中只预测下一词元的模型 $Y_2$ 准确率为 `0.000`，预测接下来两个词元的模型 $Y_2$ 准确率为 `1.000`；A11_02 中 K=2 干净、全位置训练的第二预测头、分支替换、分支读出都达到 `1.000`，噪声目标保持接近机会水平。

**解释：** $S_Z$ 与 $Z$ 一一对应；如果 $h_T$ 不含 $Z$，预测 $S_Z$ 的最优交叉熵不能低于分支不确定性。反过来，低 $S_Z$ 预测损失意味着 $h_T$ 必须保留足够多的 $Z$ 信息。

**边界：** 该定理不是自然语言结论，也不是优化速度定理；它只在数据构造和有信息未来位置损失条件满足时成立。

**来源：** `../../../problem_anchors/11_long_horizon_mtp_objective/11_04_k3_first_informative_horizon_anchor.md`; `../A11_01_k2_branch_delayed_next_two/summary.md`; `../A11_02_two_token_shared_trunk_signal_interference/summary.md`; `summary.md`; `detailed.md`。

### 结果 2：学习效率还没有无条件证明；现有指标只支持受控、带边界的效率证据。

**机制对应：** 表示定理只说明“学好有信息未来位置后 $h_T$ 必须含 $Z$”。要推出“更快学到 $Z$”，还需要第 2 节的优化桥梁：额外未来位置梯度 $g_\tau$ 要实际降低语义恢复损失 $R_\phi$，并且不能破坏本地下一词元学习。

**指标或条件定义：** 效率指标是 $T_\theta$ 和早期曲线面积。$T_\theta$ 是 $Q\ge0.9$ 连续两次成立的最早训练步；早期曲线面积是 0 到 3000 步内的 $Q(t)$ 平均面积。本地保护指标是 $Y_1/Y_2$ 损失和准确率。梯度指标是 $c=\langle g_1,g_\tau\rangle/(\|g_1\|\|g_\tau\|)$ 以及它和未来 $\Delta Q$ 的关系。

**证据：** K=2 中，A11_02 观察到 $L_1/L_2$ 共享梯度冲突，词嵌入和注意力参数的余弦约为 `-0.94`，但 $Y_1$ 准确率仍为 `1.00`；这说明冲突存在，但不能判定为有害。K=3 中，干净、只在决策位置训练下，K=1/K=2 达到率都是 `0.00`，K=3 为 `0.60/0.40`；K=3 早期曲线面积是 `0.537/0.644`，K=1/K=2 最好只有 `0.250/0.281`。干净、全位置训练下，K=3 仍最强，但 K=1/K=2 也能通过间接路径恢复 $Z$。

**解释：** 当前效率证据支持“覆盖 $\tau$ 的直接监督在受控、只在决策位置训练条件下更早恢复 $Z$”。但梯度冲突没有导致 $Y_1$ 下降，且全位置训练有间接迁移，所以还不能证明 MTP 相对 NTP 有无条件效率优势。

**边界：** 不能说 MTP 梯度已经被证明更有用，不能说梯度冲突一定伤害 NTP，也不能说全位置训练中 K=1/K=2 学不到；当前只能说效率桥梁有明确指标和部分受控证据，证明尚未完成。

**来源：** `../A11_02_two_token_shared_trunk_signal_interference/summary.md`; `../A11_02_two_token_shared_trunk_signal_interference/detailed.md`; `summary.md`; `detailed.md`; `figures/clean_q_curves.png`; `figures/gradient_usefulness_clean_h3.png`。

![干净条件 Q 曲线](figures/clean_q_curves.png)

![梯度有用性审计](figures/gradient_usefulness_clean_h3.png)

## 4. 执行动作

**下一步动作：** 写出并审查一个最小优化效率命题：当 $K\ge\tau$ 时，什么额外优化假设能推出更小的 $T_\theta$ 或更高早期曲线面积。

**目的：** 把“低有信息未来位置损失迫使 $h_T$ 含 $Z$”推进到“为什么训练过程更快学到 $Z$”，并区分直接监督强度、信用分配距离、全位置间接迁移和共享梯度冲突。

**完成判据：** 形成一个可证明或可证伪的命题，并给出最小实验判据：如果 K=3 的 $T_\theta$/早期曲线面积优势在控制间接迁移后仍存在，才支持效率机制；否则结论收缩为表示约束优势。

## 5. 证据索引

| 结果 | 证据 | 主要指标或图 | 支持什么 | 不能证明什么 | 来源 |
|---|---|---|---|---|---|
| 结果 1 | K=2 与 K 个未来词元表示定理；A11_01/A11_02/A11_04 支持目标函数分离 | $I(h_T;Z)\ge H(Z)-\varepsilon$；只在决策位置训练的 $Q$ | 覆盖含 $Z$ 的未来位置会产生表示保证 | 优化必然更快 | anchor; A11_01 summary; A11_02 summary; A11_04_03 summary |
| 结果 2 | 干净 $\tau=3$ K=1/K=2/K=3 对比 | $T_\theta$、早期曲线面积、最终 $Q$、干净条件 Q 曲线 | K=3 在受控设置下更早/更稳恢复 $Z$ | 全位置排他性、自然语言优势 | `summary.md`; `detailed.md`; `figures/clean_q_curves.png` |
| 结果 3 | A11_02 共享梯度冲突与 A11_04_03 梯度有用性 | $c\approx-0.94$；梯度有用性散点图 | 梯度冲突存在但未证明有害 | MTP 梯度一定更有用或更坏 | A11_02 summary/detailed; A11_04_03 summary/detailed |

## 6. 来源索引

**Anchor：**

- `../../../problem_anchors/11_long_horizon_mtp_objective/11_04_k3_first_informative_horizon_anchor.md`

**Protocol：**

- `protocol.md`
- `../A11_02_two_token_shared_trunk_signal_interference/protocol.md`

**Summary：**

- `summary.md`
- `../A11_01_k2_branch_delayed_next_two/summary.md`
- `../A11_02_two_token_shared_trunk_signal_interference/summary.md`

**Detailed：**

- `detailed.md`
- `../A11_02_two_token_shared_trunk_signal_interference/detailed.md`

**Figures：**

- `figures/clean_q_curves.png`
- `figures/gradient_usefulness_clean_h3.png`
- `figures/local_loss_guard_y1.png`

## 7. 补充材料

本地损失保护通过：K=3 在干净、只在决策位置训练和全位置训练中保持有效 $Y_1/Y_2$ 准确率为 `1.00`，说明长程恢复不是通过牺牲局部预测得到的。

![本地损失保护](figures/local_loss_guard_y1.png)

噪声全位置控制是当前最重要的警告：当 $Y_3\perp Z$ 时，随机初始化下 K=1/K=2/K=3 的早期曲线面积仍可达到 `0.958/0.946/0.985`，说明全位置训练的高 $Q$ 不能单独作为直接监督证据。

![噪声全位置 Q 曲线](figures/noisy_all_position_q_curves.png)
