# 会议简报：多词元预测如何帮助长程关系学习

## 0. 执行摘要

**研究问题：** 当前需要判断的是：多词元预测（MTP）是否在学习长程关系上比下一词元预测（NTP）更有利；这里的“更有利”严格定义为同一个前缀状态 $h_T$ 更早或更稳定地暴露早期变量 $Z$。

**机制解释：** 最小机制是“第一个含信息位置覆盖”：若 $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$，则只有当 $K\ge\tau$ 时，目标 $L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j)$ 才直接包含长程变量监督。

**主要结果：** 当前受控的单预测点证据支持：MTP 在覆盖第一个含长程信息的未来 token 时，比 NTP/非覆盖 MTP 更能让 $h_T$ 恢复 $Z$；但这不是普遍语言建模优势，也不是优化必然成功。

**证据说明：** 决定性指标是 guarded recovery score，即 $Q_K(t)=\min\{A_K(t),P_K(t),S_K(t)\}$；它同时要求可预测、可线性读出、并对分支替换敏感。

1. K=2 clean 实验显示，当 $Y_1=A$ 共享而 $Y_2=S_Z$ 含分支信息时，next-two 相比匹配的 next-one 明显提高 AUC $Q$、final $Q$ 和阈值到达率。
2. K=3 clean 实验显示，当第一个含分支信息的 token 被移到 $\tau=3$ 时，K=1/K=2 都保持 chance，而 K=3 获得正的 coverage gap。
3. noisy 和 redundant 控制显示：未来 token 必须含有新的分支信息才支持长程结论；噪声目标的短暂假阳性说明不能只看阈值命中。

**结论边界：** 当前只证明受控分支延迟、单预测点、同一前缀状态可恢复性意义下的 MTP 优势，不能推出自然语言中 MTP 普遍优于 NTP。

**执行动作：** 下一步最小动作是做 $\tau=3$ 的 all-position language-model control，完成判据是 clean K=3 的 coverage gap 仍保留、K=1/K=2 仍低、noisy final $Q$ 仍低，并且 $Y_1,Y_2$ 本地学习不受损。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 单位或公式 | 为什么影响当前判断 | 不能证明什么 |
|---|---|---|---|---|---|
| 多词元预测（MTP） | 一个前缀状态同时预测多个未来 token | $h_T\to Y_1,\ldots,Y_K$ | $L_K=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j,Y_j)$ | 研究对象 | 普遍优于 NTP |
| 下一词元预测（NTP） | 一个前缀状态只预测紧邻的下一个 token | $h_T\to Y_1$ | $L_1=\operatorname{CE}(q_1,Y_1)$ | 对照目标 | 无法学习长程关系 |
| 长程变量 $Z$ | 早期出现、晚些时候才影响目标的变量 | branch token `BR_z` 对应的分支编号 | categorical | 受控长程因果因素 | 自然语言语义 |
| 前缀状态 $h_T$ | 模型读完 prefix 后的隐藏状态 | $h_T=f_\theta(X_{\le T})$ | vector | 检查长程信息是否已被表示 | 后续状态不能重算 |
| 第一个含信息的未来位置 $\tau$ | 第一个让未来目标新增 $Z$ 信息的位置 | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | token offset | 决定哪个 K 应该有效 | 真实语料中 $\tau$ 的分布 |
| 覆盖条件 | MTP 的预测范围包含 $\tau$ | $K\ge\tau$ | Boolean | 应该有直接长程监督 | 优化一定成功 |
| 非覆盖条件 | 预测范围未包含 $\tau$ | $K<\tau$ | Boolean | 不应有直接长程监督 | 永远不会偶然编码 $Z$ |
| guarded recovery score | 保守的分支恢复分数 | $Q=\min\{A,P,S\}$ | 0 到 1 | 防止只靠 probe 假阳性 | 完整因果证明 |
| AUC $Q$ | 训练过程中 $Q$ 的平均水平 | checkpoints 上 $Q$ 的均值 | score | 衡量学习效率 | 最终能力上界 |
| coverage gap | 覆盖条件相对非覆盖条件的优势 | $\operatorname{AUC}_Q(K=\tau)-\max_{K<\tau}\operatorname{AUC}_Q(K)$ | score gap | 判断第一个含信息位置覆盖机制 | 更大 K 总是更好 |
| clean 条件 | 未来目标真实包含分支信息 | K=2 中 $Y_2=S_Z$；K=3 中 $Y_3=S_Z$ | data regime | 主实验条件 | 自然语言语义 |
| noisy 条件 | 未来目标是分支无关噪声 | $Y_j\perp Z$ | data regime | 排除任意辅助 loss 都有用 | 所有噪声情形 |
| redundant 条件 | 更早目标已经暴露分支 | 例如 $Y_2=S_Z$ 后 $Y_3=T_Z$ | data regime | 排除“只是本地已知信息” | 新的长程信息 |
| decision-only | 只在选定预测点计算 loss | 只优化 $h_T\to Y_j$ | training scope | 对齐理论对象 | 标准 LM 训练 |
| all-position control | 所有合法位置都计算 LM loss | 全序列 offset losses | training scope | 检查结果是否接近真实 LM 训练 | 自然语言迁移 |

## 2. 机制解释与建模

**核心模型：**

$$
\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\},\qquad
L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
$$

若 $K<\tau$，active loss 中没有直接依赖 $Z$ 的未来目标；若 $K\ge\tau$ 且 $Y_\tau=S_Z$，则 $\operatorname{CE}(q_\tau,S_Z)$ 会直接惩罚 branch-blind 的 $h_T$。

**符号含义：**

- $Z$：早期分支变量，是受控长程信息。
- $h_T$：预测点前缀状态，是要检查的信息载体。
- $Y_j$：从 $h_T$ 向后第 $j$ 个未来 token。
- $K$：MTP 同时预测的未来 token 数。
- $\tau$：第一个未来目标真正新增 $Z$ 信息的位置。

**机制链条：**

1. 若 $Y_1$ 与 $Z$ 无关，NTP 可以只学 shared next token，而不要求 $h_T$ 暴露 $Z$。
2. 若某个未来目标 $Y_\tau=S_Z$ 与 $Z$ 一一对应，则覆盖该位置的 MTP loss 直接要求 $h_T$ 支持 $S_Z$ 预测。
3. 在 clean 构造中，若 $\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le\varepsilon$，则 $H(S_Z\mid h_T)\le\varepsilon$，又因 $S_Z$ 与 $Z$ 一一对应，所以 $I(h_T;Z)\ge H(Z)-\varepsilon$。

**当前问题分解：**

- 理论层：证明 MTP 的未来目标能给 $h_T$ 加上 NTP 没有的表示要求。
- 效率层：检查这个表示要求是否让训练中更早恢复 $Z$。
- 覆盖层：检查 K=2 结果是否只是 next-two 特例，还是“第一个含信息位置覆盖”的特例。
- 最危险替代解释：随机初始化泄漏、probe 假阳性、噪声 auxiliary loss、redundant local target、以及 decision-only 与真实 LM 训练不一致。

## 3. 主要结果

**一句话总结：** 当前证据支持的精确说法是：在受控长程构造中，MTP 比 NTP 更好地学习长程关系，是指当 MTP 覆盖第一个含长程信息的未来 token 时，它能让同一个前缀状态 $h_T$ 更可恢复早期变量 $Z$。

### 结果 1：K=2 clean 中，next-two 比匹配的 next-one 更有效地让 $h_T$ 恢复早期变量

**机制对应：** 该结果对应第 2 节中的 $\tau=2$ 特例：$Y_1=A$ 不含 $Z$，$Y_2=S_Z$ 含 $Z$。

**指标或条件定义：** 匹配的 next-one 只优化 $L_1$，next-two 优化 $L_1+\lambda L_2$；$Q$ 是可预测、可读出、可分支替换的最小值。

**证据：** clean K=2 中，fixed next-one 的 AUC $Q$ 为 `0.250/0.288`，final $Q$ 为 `0.250`，阈值到达率 `0.00`；next-two 的 AUC $Q$ 为 `0.536/0.895`，final $Q$ 为 `0.550/0.900`，阈值到达率 `0.40/0.80`。两种初始化下 $Y_1$ accuracy 都保持 `1.00`。

**解释：** fixed next-one 能预测 shared $A$，但这不要求 $h_T$ 区分分支；next-two 必须预测 $S_Z$，因此给 $h_T$ 提供直接分支监督。

**边界：** identical 初始化下 next-two 只有 2/5 seeds 到达阈值，说明这是“有用但不保证优化成功”的信号；随机初始化结果还要受 noisy 控制约束。

**来源：** `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/summary.md`。

### 结果 2：K=3 clean 中，只有覆盖 $\tau=3$ 的 K=3 条件显著优于 K=1/K=2

**机制对应：** 该结果检验“第一个含信息位置覆盖”：$Y_1=A$、$Y_2=C$ 都不含 $Z$，只有 $Y_3=S_Z$ 含 $Z$。

**指标或条件定义：** coverage gap 是 K=3 的 AUC $Q$ 减去 K=1/K=2 中最好的 AUC $Q$。

**证据：** clean $\tau=3$ 中，K=1/K=2 的 final $Q$ 都是 `0.250`，阈值到达率 `0.00`；K=3 的 final $Q$ 为 `0.800/0.750`，AUC $Q$ 为 `0.665/0.735`。coverage gap 为 `+0.415`（identical）和 `+0.465`（random）。

**解释：** K=2 可以完美学会 shared $Y_2=C$，但因为 $C$ 不含 $Z$，它仍然不能让 $h_T$ 恢复分支；K=3 第一次包含 $S_Z$，所以产生直接长程监督。

**边界：** K=3 也不是每个 seed 都完全成功；当前结论是 controlled coverage support，不是“更大 K 总是更好”。

**来源：** `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/summary.md`。

### 结果 3：控制实验说明“未来 token 是否含新分支信息”比“多预测一个 token”更关键

**机制对应：** 该结果检验条件信息项 $I(Z;Y_j\mid Y_{<j})$，即未来目标是否真的带来新的长程信息。

**指标或条件定义：** noisy control 令未来目标与 $Z$ 无关；redundant control 令更早目标已经暴露 $Z$。

**证据：** K=2 noisy identical-init 保持 chance，K=2 noisy random-init 有弱假阳性；K=3 noisy final $Q$ 低（`0.25/0.30`），但有 `0.20` 的 transient threshold hit。K=3 redundant 中 K=2/K=3 都可恢复分支，因为 $Y_2=S_Z$ 已经暴露分支。

**解释：** noisy 结果说明不能把任何 auxiliary future loss 都解释成长程监督；redundant 结果说明如果更早 token 已经给出 $Z$，高恢复分数不是 horizon-3 的新证据。

**边界：** noisy transient false positives 说明 threshold reach 不能单独作为判断标准；必须同时看 AUC、final $Q$、目标信息结构和本地学习 guard。

**来源：** `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/detailed.md`；`Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/detailed.md`。

## 4. 执行动作

**下一步动作：** 执行 $\tau=3$ 的 all-position language-model control。

**目的：** 当前证据只在 decision-only 下成立；all-position control 用更接近真实语言模型的训练方式检查 coverage 机制是否仍保留。

**完成判据：** clean $\tau=3$ 中 K=3 仍有正 coverage gap，K=1/K=2 不出现同等恢复；noisy final $Q$ 保持低；K=3 不损害 $Y_1,Y_2$ 本地预测。

## 5. 证据索引

| 结果 | 证据 | 主要指标或图 | 支持什么 | 不能证明什么 | 来源 |
|---|---|---|---|---|---|
| 结果 1 | K=2 clean next-two vs fixed next-one | AUC $Q$、final $Q$、阈值到达率、$Y_1$ accuracy | next-two 在 $\tau=2$ 中提高 $h_T$ 的分支恢复 | MTP 普遍更优 | `A11_03/summary.md` |
| 结果 2 | K=3 clean K=1/K=2/K=3 比较 | coverage gap、final $Q$、native $Y_3$ accuracy | 第一个含信息位置覆盖 | 更大 K 总是更好 | `A11_04/summary.md` |
| 结果 3 | noisy/redundant controls | noisy final $Q$、redundant K=2/K=3 recovery | 必须区分新长程信息、噪声和冗余 | noisy 完全无假阳性 | `A11_03/detailed.md`; `A11_04/detailed.md` |

## 6. 来源索引

**Anchor：**

- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_03_k2_semantic_efficiency_anchor.md`
- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_04_k3_first_informative_horizon_anchor.md`

**Protocol：**

- `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/protocol.md`

**Summary：**

- `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_02_two_token_shared_trunk_signal_interference/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/summary.md`

**Detailed：**

- `Projects/from-attention-to-search/main/experiments/A11/A11_03_k2_semantic_efficiency/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/detailed.md`

**Figures：**

- 当前 brief 不使用中心图；主要证据是 `summary.md` 和 `detailed.md` 中的决策表格。

## 7. 补充材料

**理论证明到底证明了什么：** K=2 理论证明的是 objective-level representation requirement。若 $Y_1$ 共享而 $Y_2=S_Z$，branch-blind 的 $h_T$ 可以解决 $Y_1$，但解决不了 $Y_2$；若第二目标交叉熵足够低，则 $h_T$ 必须含有 $Z$ 的信息。

**实验到底验证了什么：** A11_03 验证这个表示要求可以变成训练效率优势；A11_04 验证优势更准确地来自覆盖第一个含信息的未来目标 $\tau$，而不是来自“多预测一个 token”本身。

**当前最准确的一句话：** MTP 比 NTP 更好，不是在所有意义上更好，而是在受控长程、同一前缀状态预测的设定中，当 MTP 的预测范围覆盖第一个含早期变量信息的未来 token 时，它对 $h_T$ 施加了 NTP 没有的直接长程监督，并在实验中提高了 $Z$ 的保守恢复分数。
