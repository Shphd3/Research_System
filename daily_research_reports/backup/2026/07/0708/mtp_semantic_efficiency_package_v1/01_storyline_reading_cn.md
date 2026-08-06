# MTP 长程语义学习效率故事线：中文阅读版

Status: reading version for advisor-facing discussion
Source package: `daily_research_reports/0708/mtp_semantic_efficiency_package_v1.zip`
Scope: controlled theory, existing evidence boundary, and next decision

## 0. 一句话回答

我们已经回答到的程度是：**在受控构造中，当 MTP 的预测范围覆盖第一个包含早期语义变量 $Z$ 的未来 token 时，它会给当前隐藏状态 $h_T$ 一个 NTP 没有的直接语义监督；clean decision-only 实验证明这种直接监督能更早恢复 $Z$，但 all-position 中 NTP / non-covering K 也能通过间接路径恢复 $Z$，所以还没有证明自然语言或所有 LM-style 训练中 MTP 都更好。**

下一步最小决策是：**在固定 $\tau=3$ 的最小设置中，分解 MTP 的效率优势到底来自直接监督强度、较短 credit-assignment path、all-position 间接迁移，还是梯度 routing / interference；不要先扩大到更大的 K。**

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算 | 单位 / 公式 | 为什么影响当前判断 | 不能证明什么 |
|---|---|---|---|---|---|
| 下一词元预测，NTP | 每个位置只预测下一个 token 的训练目标 | 从 $h_T$ 预测 $Y_1$ | $L_1(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),Y_1)$ | 导师问题中的 baseline | NTP 永远学不到长程信息 |
| 多词元预测，MTP | 同一个当前状态预测多个未来 token | 从 $h_T$ 同时预测 $Y_1,\ldots,Y_K$ | $L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j)$ | 决定是否有远处监督直接作用到 $h_T$ | MTP 一定更好 |
| 预测范围，K | MTP 一次预测几个未来 token | K=1 是 NTP；K=2 是 next-two；K=3 是 next-three | token offset count | 判断目标是否覆盖第一个有信息位置 | K 越大越好 |
| 早期语义变量，$Z$ | 前缀中已经出现、未来才需要的信息 | 受控实验中是 branch key $B$ | 离散变量 | 被长程恢复的核心对象 | 自然语言全部语义 |
| 当前隐藏状态，$h_T$ | 模型读完当前 prefix 后的表示 | decision prefix 的 Transformer hidden state | 向量 | 我们问 $Z$ 是否已写入当前状态 | 后面所有状态的信息 |
| 第一个语义显现位置，$\tau$ | 第一个 future token 开始提供关于 $Z$ 的新信息 | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | token offset | 判断 K 是否覆盖有效监督 | 真实语言中固定唯一 horizon |
| 覆盖条件 | MTP 预测范围到达第一个有信息位置 | $K\ge\tau$ | 布尔条件 | 有直接 $Z$ 监督的必要结构 | 优化一定成功 |
| 非覆盖条件 | MTP 预测范围停在有信息位置之前 | $K<\tau$ | 布尔条件 | 没有直接 $Z$ 监督 | 在 all-position 中完全不能学 |
| 语义恢复分数，$Q_K(t)$ | 保守判断 $h_T$ 是否恢复 $Z$ | informative-horizon accuracy、probe、swap 的最小值 | $Q_K(t)=\min\{A_K(t),P_K(t),S_K(t)\}$ | 主效率指标的基础 | 完整因果机制 |
| 到阈值时间，$T_\theta$ | 多快稳定恢复 $Z$ | 第一次连续若干 checkpoint 满足 $Q_K(t)\ge\theta$ | training steps | 判断“更早学到” | 最终上限 |
| 早期曲线面积，AUC | 训练早期平均恢复程度 | 对 $Q_K(t)$ 在早期窗口求平均或积分 | score area | 判断“更稳、更持续地学到” | 梯度原因 |
| 本地学习保护，local guard | 额外 future loss 是否损害原 next-token 学习 | $Y_1/Y_2$ accuracy 和 cross entropy | accuracy / CE | 回答“是否不严重损害原 NTP 效率” | 全部语言建模能力不受损 |
| 梯度有用性，gradient usefulness | informative future loss 的梯度是否降低语义恢复损失 | $U_\tau=\langle\nabla_\theta R_\phi,g_\tau\rangle$ | signed inner product | 从表示约束推进到优化效率的桥梁 | 单独证明因果 |
| 语义恢复损失，$R_\phi$ | 从 $h_T$ 读出 $Z$ 有多难 | $R_\phi(\theta)=\operatorname{CE}(s_\phi(h_T(\theta)),Z)$ | CE | 用来定义 future gradient 是否有助于恢复 $Z$ | 下游真实任务收益 |
| 可用表征 | $Z$ 不只是能被 probe 读出，还能被输出头或 gate 使用 | output margin、branch-output alignment、route NMI 等 | 多个指标 | 连接到“学到的信息是否有用” | 真实 MoE expert utility |

## 2. 导师问题与我们的精确问题

导师问题是：

> MTP 在长程语义学习上是否比 NTP 更好？如果更好，好在哪里？是否更高效？是否不会严重损害原来的 next-token 学习？

这个问题不能直接回答成“MTP 好”或“MTP 不好”，因为“好”至少有三层含义：

| 层次 | 要回答的问题 | 当前状态 |
|---|---|---|
| 表示要求 | MTP 是否要求 $h_T$ 含有远处才需要的 $Z$？ | 已有定理层回答 |
| 学习效率 | MTP 是否更早、更稳地把 $Z$ 学进 $h_T$？ | clean decision-only 有支持；all-position 是相对优势而非排他优势 |
| 不损害本地学习 | MTP 学 $Z$ 是否以牺牲 $Y_1/Y_2$ 为代价？ | 当前受控实验 local guard 通过 |
| 表征可用性 | 学到的 $Z$ 是否更 output-facing / gateable？ | 仍是下一步问题 |
| 自然语言迁移 | 受控机制是否迁移到真实 LM / 自然语言？ | 未证明 |

所以我们对导师问题的准确回答是：

> MTP 的确定优势不是“唯一能学长程语义”，而是当它覆盖第一个语义显现位置时，会把远处才出现的语义相关性提前变成当前 $h_T$ 的直接监督。这个直接监督在 clean decision-only 中表现为更早恢复 $Z$；在 all-position 中 K=3 仍更强，但 NTP / K=1、K=2 也能通过共享参数间接恢复 $Z$，所以目前支持的是受控、带边界的效率优势，不是普遍优势。

## 3. 核心物理直觉

长程语义学习的困难不是“未来 token 远”本身，而是：

1. 早期变量 $Z$ 已经在 prefix 中出现；
2. 下一个 token $Y_1$ 不需要 $Z$；
3. 更远的某个未来 token $Y_\tau$ 才第一次需要 $Z$；
4. 如果训练目标只看 $Y_1$，模型可以把不同 $Z$ 的 prefix 压成相同或近似相同的 $h_T$，仍然把 $Y_1$ 预测对；
5. 如果 MTP 直接预测到 $Y_\tau=S_Z$，那么 branch-blind 的 $h_T$ 会被 loss 惩罚。

直观例子：故事开头给出凶手身份，中间几句话都可以局部预测，最后某句话才需要凶手身份。NTP 只问“下一句话是什么”，可能暂时不需要记住凶手；MTP 如果在当前状态就预测到首次需要凶手身份的未来 token，就会直接要求当前状态保留这个信息。

## 4. 最小数学模型

设早期变量：

$$
Z\sim\operatorname{Unif}\{1,\ldots,m\}.
$$

当前 prefix state：

$$
h_T=f_\theta(X_{\le T}).
$$

未来 token：

$$
Y_j=X_{T+j}.
$$

第一个语义显现位置：

$$
\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}.
$$

MTP objective：

$$
L_K(h_T)=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
$$

干净确定性情形：

$$
Y_\tau=S_Z,
$$

且 $Z\mapsto S_Z$ 一一对应。

### 4.1 表示要求定理

如果 $K\ge\tau$ 且：

$$
\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le\varepsilon,
$$

那么：

$$
I(h_T;Z)\ge H(Z)-\varepsilon.
$$

意思是：**如果 MTP 覆盖第一个含 $Z$ 信息的 future token，并把它预测好，那么当前隐藏状态 $h_T$ 必须含有 $Z$。**

### 4.2 非覆盖条件

如果：

$$
I(Z;Y_{1:K})=0,
$$

那么 $Z$-blind 的 $h_T$ 也可以是这些 active targets 的最优表示。意思是：**如果被监督的 token 都不需要 $Z$，目标函数没有直接理由强迫 $h_T$ 保存 $Z$。**

## 5. K=2 与 K=3 的故事位置

### 5.1 K=2 最小机制

构造：

$$
Y_1=A,\qquad Y_2=S_Z.
$$

$A$ 是共享 token，不含 $Z$；$S_Z$ 是由 $Z$ 决定的 branch-specific token。

NTP 只需要预测：

$$
h_T\to A.
$$

它可以不让 $h_T$ 记住 $Z$。

K=2 MTP 还需要预测：

$$
h_T\to S_Z.
$$

因此低 second-token loss 会迫使 $h_T$ 含有 $Z$。

### 5.2 K=3 first-informative-horizon

构造：

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

这里：

$$
I(Z;Y_1)=0,
$$

$$
I(Z;Y_2\mid Y_1)=0,
$$

$$
I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

因此 $\tau=3$。K=1/K=2 不覆盖 $\tau$，K=3 覆盖 $\tau$。

这个实验回答的是：**MTP 的优势是否由“覆盖第一个有信息 future token”决定，而不是由“多预测几个 token”本身决定。**

## 6. 从表示要求到学习效率

表示定理只说明：

> 如果 MTP 把 $S_Z$ 预测好，那么 $h_T$ 必须含有 $Z$。

它不自动说明：

> MTP 一定更快学到 $Z$。

要说“更高效”，需要一个优化桥梁。定义语义恢复损失：

$$
R_\phi(\theta)=\operatorname{CE}(s_\phi(h_T(\theta)),Z).
$$

设：

$$
g_1=\nabla_\theta L_1,\qquad g_\tau=\nabla_\theta L_\tau.
$$

NTP 更新：

$$
\theta_N^+=\theta-\eta g_1.
$$

MTP 更新：

$$
\theta_M^+=\theta-\eta(g_1+\lambda_\tau g_\tau).
$$

如果：

$$
\langle\nabla_\theta R_\phi,g_\tau\rangle>0,
$$

那么沿 $-g_\tau$ 更新会降低语义恢复损失；MTP 相比 NTP 多一个一阶下降项：

$$
\eta\lambda_\tau\langle\nabla_\theta R_\phi,g_\tau\rangle.
$$

但还需要 local guard：如果 $g_\tau$ 与 $g_1$ 强烈冲突，MTP 可能提升 $Z$ 恢复，却损害本地 next-token 学习。因此效率 claim 必须同时满足：

1. $Q_K(t)$ 更早或更稳上升；
2. $Y_1/Y_2$ local loss 不恶化；
3. 梯度有用性最好能解释一部分恢复，但不能只靠 cosine 正负判断。

## 7. 现有证据如何回答导师问题

### 7.1 已经回答的部分

1. **直接表示监督已经回答。**
   在 K=2 与 K=3 的受控构造中，只要 MTP 覆盖第一个含 $Z$ 信息的 token，低 loss 会数学上要求 $h_T$ 含有 $Z$。

2. **clean decision-only 的效率优势已有支持。**
   在 $\tau=3$ clean decision-only 中，K=1/K=2 不覆盖 $\tau$，从未可靠达到高 $Q$；K=3 覆盖 $\tau$，更早恢复 $Z$，且 local $Y_1/Y_2$ 学习不受损。

3. **all-position 的边界已经观察到。**
   在更接近 LM-style 的 all-position training 中，K=3 仍最强，但 K=1/K=2 也能通过其他位置的 loss 和共享参数间接恢复 $Z$。

4. **“不严重损害原来 NTP 效率”在受控实验中有支持。**
   当前 clean 受控实验中，K=3 的 $Y_1/Y_2$ accuracy 保持高、loss 接近 0；因此长程恢复不是靠牺牲本地 token 学习换来的。

### 7.2 尚未回答的部分

1. **没有证明自然语言中 MTP 一定更好。**
2. **没有证明 K 越大越好。**
3. **没有证明 NTP 学不到长程信息。**
4. **没有证明 all-position 中高 $Q$ 一定来自 direct supervision。**
5. **没有用梯度干预证明 extra-horizon gradient 是效率优势的因果原因。**
6. **还没有证明 MTP 学到的 $Z$ 更 output-facing、更 gateable，或能带来真实 MoE expert utility。**

## 8. 和导师问题的关系解析

导师问的“更好”可以拆成三个可判定问题：

### 8.1 是否学得到长程语义？

回答：**在受控构造中，MTP 覆盖 $\tau$ 时有确定的表示要求；NTP 在同一 decision-prefix objective 下可以不要求 $Z$。**

边界：all-position 中 NTP 也可能通过间接路径学到 $Z$。

### 8.2 是否更高效？

回答：**clean decision-only 中有支持：覆盖 $\tau$ 的 K=3 比 K=1/K=2 更早、更稳恢复 $Z$。all-position 中 K=3 仍更强，但 K=1/K=2 也能恢复，所以只支持相对效率/稳定性优势，不支持排他优势。**

边界：还需要把直接监督强度、credit-assignment distance、all-position indirect transfer、gradient routing 分开。

### 8.3 是否不严重损害原 NTP 效率？

回答：**当前受控实验 local guard 通过：K=2/K=3 的额外 future-token supervision 没有观察到损害 $Y_1/Y_2$ local prediction。**

边界：这不等于所有任务、所有架构、所有自然语言数据上都不会损害 next-token optimization。

## 9. 当前最稳妥 claim

可以说：

> 在受控 first-informative-horizon 构造中，当 MTP 的预测范围覆盖第一个包含早期语义变量 $Z$ 的未来 token 时，它会给当前 $h_T$ 一个 NTP / non-covering K 没有的直接语义监督；在 clean decision-only 中，这种直接监督表现为更早恢复 $Z$，且没有观察到本地 $Y_1/Y_2$ 学习损伤。

更谨慎地补充：

> 在 all-position LM-style training 中，K=3 仍更强，但 K=1/K=2 也能通过间接路径恢复 $Z$，因此 all-position 证据不能解释成“只有 MTP 能学长程语义”。

## 10. 当前最危险 overclaim

不要说：

1. MTP 一定比 NTP 好。
2. NTP 学不到长程语义。
3. K 越大越好。
4. all-position 中 K=1/K=2 不能恢复 $Z$。
5. gradient cosine 的正负能直接说明梯度好坏。
6. 当前受控实验已经证明自然语言里的 MTP 优势。
7. gateability 代理指标如果变好，就说明真实 MoE expert utility 已经成立。

## 11. Next Decision

下一步不要先扩 K，也不要直接跳自然语言。最小 decision 是：

> 在固定 $\tau=3$ 的受控设置中，MTP 的效率优势究竟来自哪条机制：直接监督强度、较短 credit-assignment path、all-position indirect transfer，还是梯度 routing / interference？

建议的最小实验分解：

1. **直接监督强度**：固定 clean $\tau=3$，只改变 $\lambda_3$，看 $T_\theta$、AUC、local guard 是否随 direct signal strength 改变。
2. **credit-assignment distance**：比较同等 $S_Z$ 监督量下，直接从 $h_T$ 预测 $S_Z$ 与只在后面位置间接预测 $S_Z$ 的差异。
3. **all-position indirect transfer**：mask 掉 decision-prefix 的 horizon-3 loss，检查 K=3 优势还剩多少。
4. **gradient routing / interference**：做 one-step counterfactual update，分别用 $g_1$、$g_\tau$、$g_1+\lambda g_\tau$ 更新，直接测 $\Delta R_\phi$、$\Delta Q$ 和 $\Delta L_{local}$。

通过标准：

> 覆盖 $\tau$ 的 K=3 在 $T_\theta$ 或 early AUC 上稳定优于 K=1/K=2，local guard 通过，noisy / redundant controls 不给出错误解释，并且至少有一个梯度或干预指标支持 direct horizon supervision 的效率作用。

若不通过：

> 结论收缩为：MTP 有直接表示约束优势，但在该训练条件下，NTP / non-covering K 的间接路径足够强，效率优势没有成立。

## 12. Source Map

- Original package: `daily_research_reports/0708/mtp_semantic_efficiency_package_v1.zip`
- Whole story draft: `daily_research_reports/0708/mtp_semantic_efficiency_package_v1/01_whole_story_line_mtp_long_horizon_semantic_efficiency_cn.md`
- Meeting brief: `daily_research_reports/0708/mtp_semantic_efficiency_package_v1/02_meeting_brief_mtp_semantic_efficiency_cn.md`
- Next-decision anchor draft: `daily_research_reports/0708/mtp_semantic_efficiency_package_v1/03_next_decision_anchor_semantic_efficiency_bridge_cn.md`
- Protocol A draft: `daily_research_reports/0708/mtp_semantic_efficiency_package_v1/04_protocol_A_semantic_efficiency_all_position_cn.md`
- Protocol B draft: `daily_research_reports/0708/mtp_semantic_efficiency_package_v1/05_protocol_B_representation_form_gradient_gateability_cn.md`
