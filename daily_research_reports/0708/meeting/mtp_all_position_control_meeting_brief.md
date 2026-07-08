# 会议简报：MTP 对长程语义学习的理论优势

## 0. 执行摘要

**研究问题：** 多个未来 token 预测（MTP）相比只预测下一个 token（NTP），到底在什么意义上更有利于长程语义学习。

**机制解释：** 长程语义指“早期信息暂时不影响下一个 token，但会影响更远的输出”；在这种情况下，MTP 如果预测到那个更远位置，就会直接要求当前状态保留早期信息，而 NTP 在同一位置没有这个要求。

**主要结果：** 理论上可以证明：MTP 有“表示监督优势”，即它能把远处语义目标变成当前状态必须保存的信息；但这不是“训练一定更快”或“真实任务一定更好”的定理。

**证据说明：** 数学证明的核心是：若第 $\tau$ 个未来 token 第一次携带早期语义变量 $Z$ 的信息，则 $K<\tau$ 时模型可以不记 $Z$，而 $K\ge\tau$ 且该未来 token 能识别 $Z$ 时，低 MTP 损失推出当前状态 $h_T$ 必须包含 $Z$。

1. 当前理论把“MTP 是否更好”从泛泛的性能问题，缩小成一个可证明问题：MTP 是否对当前状态施加了更强的长程语义表示要求。
2. 理论证明给出的肯定结论是：只要 MTP 的预测范围覆盖了第一个携带长程信息的未来 token，它就比 NTP 多一个直接语义监督项。
3. 实验的作用是检查这个理论对象是否可观察：单前缀实验支持该机制，全位置训练则提示真实训练还存在间接学习路径。

**结论边界：** 当前理论不能推出“MTP 总是更快、更省样本、自然语言上必然更好”；它只证明在明确的长程语义结构下，MTP 对当前状态有 NTP 没有的直接表示约束。

**执行动作：** 下一步应围绕“效率优势”继续：在全位置训练下测试这种直接表示约束是否让模型更早、更稳定地学到长程语义，同时不破坏下一个 token 的预测。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 单位或公式 | 为什么影响当前判断 | 不能证明什么 |
|---|---|---|---|---|---|
| 只预测下一个 token（NTP） | 模型只被要求预测紧接着出现的 token | 当前状态 $h_T$ 只预测 $Y_1$ | $L_1=\operatorname{CE}(q_1,Y_1)$ | 作为对照基线 | 不代表模型永远学不到长程信息 |
| 多个未来 token 预测（MTP） | 模型同时预测后面多个 token | 当前状态 $h_T$ 预测 $Y_1,\ldots,Y_K$ | $L_K=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j,Y_j)$ | 可能把远处信息提前监督到当前状态 | 不代表预测越多一定越好 |
| 当前状态 | 模型读完当前前缀后形成的内部表示 | $h_T=f_\theta(X_{\le T})$ | 向量 | 判断模型此刻是否已经保留早期信息 | 不等于模型所有层、所有位置的信息 |
| 长程语义变量 | 早期出现、后来才影响输出的信息 | 记作 $Z$；可类比早期指令、人物身份、程序变量、前提条件 | 随机变量 | 表示“长程关系”中被延迟使用的信息 | 不覆盖自然语言中的所有语义 |
| 第一个含信息位置 | 第一个真正需要 $Z$ 的未来 token 位置 | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | 未来 token 编号 | 决定 MTP 是否预测到了关键语义位置 | 自然语料中未必固定或唯一 |
| 表示监督优势 | 目标函数迫使当前状态保存更多语义信息 | 低未来预测损失推出 $I(h_T;Z)$ 较高 | 信息量下界 | 这是当前理论已经证明的优势 | 不等于优化速度优势 |
| 效率优势 | 更快或更稳地学到长程语义 | 达到语义恢复阈值的训练步数或早期曲线面积 | $T_\theta=\inf\{t:Q(t)\ge\theta\}$ | 这是下一步要检验的优势 | 目前还不是理论定理 |

## 2. 机制解释与建模

**核心模型：**

$$
Z\rightarrow X_{\le T}\rightarrow h_T,\qquad Y_j=X_{T+j}.
$$

**符号含义：**

- $Z$：早期语义变量，例如早期指令、故事前提、程序变量或分支身份。
- $X_{\le T}$：当前已经读到的前缀。
- $h_T$：模型读完当前前缀后的内部状态。
- $Y_j$：当前之后第 $j$ 个未来 token。
- $\tau$：第一个携带 $Z$ 信息的未来位置。

**最小长程语义结构：**

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_\tau\mid Y_{<\tau})>0.
$$

直观意思是：下一个 token 可以完全由局部上下文决定，但更远处的 token 才需要早期信息 $Z$。

**理论命题：**

若 $K<\tau$，被监督的未来 token 还没有包含 $Z$ 的信息，则一个不保存 $Z$ 的当前状态也可以完成这些预测：

$$
K<\tau \quad\Rightarrow\quad h_T \text{ 不必包含 } Z.
$$

若 $K\ge\tau$，并且第 $\tau$ 个未来 token 能识别 $Z$，那么低 MTP 损失会推出当前状态必须含有 $Z$ 的信息：

$$
\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le \varepsilon
\quad\Rightarrow\quad
I(h_T;Z)\ge H(Z)-\varepsilon.
$$

**机制链条：**

1. NTP 只训练 $h_T\to Y_1$；如果 $Y_1$ 不需要 $Z$，NTP 在这个位置没有理由强迫 $h_T$ 保存 $Z$。
2. MTP 训练 $h_T\to Y_{1:K}$；如果 $Y_{1:K}$ 中包含第一个需要 $Z$ 的未来 token，当前状态就必须为这个远处目标保存 $Z$。
3. 因此，MTP 的理论优势不是“多预测几个 token”，而是“预测范围覆盖了真正新增长程信息的位置”。

**当前问题分解：**

- 已证明：MTP 在目标函数层面有直接表示监督优势。
- 未证明：这种优势一定转化为更快优化、更好泛化或自然语言提升。
- 需要实验判断：表示监督优势是否在训练过程中表现为更早、更稳的长程语义恢复。

## 3. 主要结果

**一句话总结：** 当前理论证明的是：在长程语义信息被延迟使用的设定下，MTP 比 NTP 对当前状态提出了更强的语义表示要求。

### 结果 1：理论先把“长程语义”定义成可证明对象

**机制对应：** 长程语义不是泛指“很长上下文”，而是一个早期变量 $Z$ 对远处 token 有预测价值、但对近处 token 没有预测价值。

**指标或条件定义：** 第一个含信息位置 $\tau$ 是判断点；如果 $K$ 没有覆盖 $\tau$，MTP 也没有保证优势。

**证据：** 文档定义 $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$，并说明优势只在新增未来 token 含有 $Z$ 信息时出现。

**解释：** 这一步很重要，因为它避免把“MTP 更好”说成空泛性能判断，而是变成“是否多监督了真正含长程信息的位置”。

**边界：** 这只是一个理论框架，不声称自然语言里的 $\tau$ 已经被识别出来。

**来源：** `daily_research_reports/0708/mtp_story_package/01_long_horizon_mtp_self_contained_story_v0.md`。

### 结果 2：理论证明 MTP 有 NTP 没有的直接表示约束

**机制对应：** 当 $K\ge\tau$ 且未来目标 $Y_\tau$ 能识别 $Z$，MTP 的第 $\tau$ 个预测损失直接作用在当前状态 $h_T$ 上。

**指标或条件定义：** 表示约束用互信息表述：$I(h_T;Z)$ 越高，说明当前状态越包含早期语义变量。

**证据：** 理论证明给出：

$$
\mathbb E[-\log q_\tau(S_Z\mid h_T)]\le \varepsilon
\Rightarrow
I(h_T;Z)\ge H(Z)-\varepsilon.
$$

同时，当 $K<\tau$ 且 $Y_{1:K}$ 不含 $Z$ 信息时，不保存 $Z$ 的 $h_T$ 也可以完成监督目标。

**解释：** 这就是 MTP 比 NTP 更优的严格含义：MTP 可以把远处语义依赖提前压到当前表示里，NTP 在同一前缀位置没有这个数学要求。

**边界：** 这不是训练速度证明；它只证明“如果 MTP 把相关未来 token 预测好，那么当前状态必须含有相关语义信息”。

**来源：** `daily_research_reports/0708/mtp_story_package/01_long_horizon_mtp_self_contained_story_v0.md`。

### 结果 3：实验只作为理论边界检查，而不是主结论本身

**机制对应：** 实验检查理论里的“覆盖第一个含信息位置”是否能在模型训练中被观察到。

**指标或条件定义：** 单前缀实验只看当前状态是否收到直接监督；全位置训练更接近真实语言模型，但会引入其他位置的间接学习。

**证据：** 当信息首次出现在第 3 个未来 token 时，单前缀实验中 K=1/K=2 接近随机水平，K=3 明显更高；全位置训练中 K=3 仍最强，但 K=1/K=2 也能通过其他位置间接恢复信息。

**解释：** 实验支持理论机制，但也提醒汇报时不能说“只有 MTP 能学到长程语义”。更准确的说法是：MTP 提供更直接的监督路径，真实训练中还可能存在间接路径。

**边界：** 实验目前还没有关闭“效率优势”：是否更快、更省样本、更稳，需要下一轮专门测试。

**来源：** `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/summary.md`；`Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/summary.md`。

## 4. 执行动作

**下一步动作：** 做效率判定实验：在全位置训练中比较覆盖条件与非覆盖条件达到同一长程语义恢复阈值所需的训练步数。

**目的：** 判断理论上的直接表示监督是否转化为训练过程中的更快、更稳学习。

**完成判据：** 若覆盖条件达到阈值的时间 $T_\theta$ 更小、早期恢复曲线更高，并且下一个 token 损失不变差，则可以进一步支持“MTP 对长程语义学习更高效”；否则结论保持为“MTP 有直接表示监督优势，但效率优势未被支持”。

## 5. 证据索引

| 结果 | 证据 | 主要指标或公式 | 支持什么 | 不能证明什么 | 来源 |
|---|---|---|---|---|---|
| 结果 1 | 长程语义定义 | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | 问题被转成可证明对象 | 自然语言 $\tau$ 已知 | 01 理论文稿 |
| 结果 2 | 表示约束定理 | $I(h_T;Z)\ge H(Z)-\varepsilon$ | MTP 有直接表示监督优势 | 训练速度和自然语言收益 | 01 理论文稿 |
| 结果 3 | K=3 与全位置对照实验 | 语义恢复分数 $Q$ | 理论机制可观察，真实训练有间接路径 | 效率优势已经成立 | A11_04 / A11_04_02 |

## 6. 来源索引

**Theory：**

- `daily_research_reports/0708/mtp_story_package/01_long_horizon_mtp_self_contained_story_v0.md`

**Anchor：**

- `Projects/from-attention-to-search/main/problem_anchors/11_long_horizon_mtp_objective/11_04_k3_first_informative_horizon_anchor.md`

**Protocol：**

- `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/protocol.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/protocol.md`

**Summary：**

- `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/summary.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/summary.md`

**Detailed：**

- `Projects/from-attention-to-search/main/experiments/A11/A11_04_k3_first_informative_horizon/detailed.md`
- `Projects/from-attention-to-search/main/experiments/A11/A11_04_02_k3_all_position_control/detailed.md`

**Figures：**

- 当前 brief 不使用中心图；理论结论由公式和实验表格支持。

## 7. 补充材料

导师可听懂的一句话版本：MTP 的理论优势不是“多预测就一定更好”，而是当远处 token 才第一次需要早期语义信息时，MTP 会把这个远处目标直接变成当前状态必须记住的信息；NTP 在同一位置没有这个要求，至于是否更快学会，需要下一步效率实验验证。
