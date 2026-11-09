# A06 Router 训练动力学相关论文阅读报告

文档状态：
- 类型：论文阅读入口报告
- 研究线：`06_geometry_proxy_preservation`
- 语言：中文
- 目的：为逐篇阅读 soft / sparse MoE routing 动力学文献提供问题、物理先验、分析故事线和 A06 连接
- 版权说明：本报告不逐句复制或整段翻译论文摘要/引言；“摘要转述”和“引言转述”是基于公开论文页面和论文内容的中文概括，供研究阅读导航使用。

## 0. 总结

这些论文不是同一类工作。它们分别回答四个层次的问题：

1. 经典 soft mixture：gate 如何根据 expert 对样本的解释能力分配 responsibility。
2. 现代 sparse MoE：如何让 conditional computation 在大模型里可训练。
3. 理论 MoE：在什么数据结构下，router 可以学到 cluster / region / gate 参数。
4. collapse / competition：softmax 或 sparse routing 为什么可能产生竞争、区域切分、表示坍塌或样本效率问题。

对 A06 最重要的启发是：

> router 更新不应被抽象地说成“学习 feature”。更具体地，它是在每个样本上根据 expert 的相对损失优势移动 row；soft router 提供连续责任分配，top-1 sparse router 则把这种连续比较破坏成选中 expert 的离散反馈。

因此下一步 `06_30` 应先验证 soft-router 的一步梯度：

\[
\Delta w_e=\eta\frac{p_e}{\tau}A_eh,
\]

再把 top-1 sparse router 看成一个低温 / 离散 / selected-expert feedback 的边界情况。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象 | 为什么重要 | 不能证明什么 |
|---|---|---|---|---|
| 责任分配 | 某个样本应由哪个 expert 解释 | soft gate probability 或 EM posterior | 是 soft MoE 训练动力学的核心语言 | feature 语义 |
| expert advantage | 某 expert 相比当前 mixture 是否更能降低 loss | \(A_e=-\langle\nabla_{\hat y}\ell,E_e(h)-\hat y\rangle\) | 直接决定 router row 更新方向 | 真实 utility |
| softmax competition | expert 概率共享一个归一化分母导致相互竞争 | \(p_e=\exp s_e/\sum_j\exp s_j\) | 解释 softmax gate 的耦合和可能 collapse | top-1 具体实现行为 |
| top-k 区域切分 | top-k gate 把输入空间分成不同激活区域 | 不同 region 有不同被选 expert 集合 | 对应 A06 的 boundary / margin 视角 | 训练一定能学到正确 region |
| 表示坍塌 | token hidden states 被 routing 拉向少数 expert centroid | token-expert score 诱导 hidden clustering | 说明 router 和 representation 会互相塑形 | A06 的 margin collapse 已被完全解释 |

## 2. 建议阅读顺序

1. Jacobs et al. 1991：先理解 soft gate 的责任分配。
2. Jordan & Jacobs 1994：把责任分配写成最大似然和 EM。
3. Shazeer et al. 2017：看现代 sparse top-k MoE 的工程目标和 discontinuity。
4. Chen et al. 2022：看 cluster structure 下 router 学 cluster-center features 的理论故事。
5. Nguyen et al. 2023 softmax Gaussian MoE：看 softmax gate 的 identifiability 和 gate-expert coupling。
6. Nguyen et al. 2023/2024 top-k sparse softmax：看 sparse gate 如何切分输入区域。
7. Nguyen et al. 2024 sigmoid vs softmax：看 softmax competition 为什么可能降低样本效率。
8. Chi et al. 2022：看 sparse routing 如何反向塑形 hidden representation 并导致 collapse。

## 3. 论文 1：Adaptive Mixtures of Local Experts

Source:
- Robert A. Jacobs, Michael I. Jordan, Steven J. Nowlan, Geoffrey E. Hinton, 1991.
- PubMed / Neural Computation: https://pubmed.ncbi.nlm.nih.gov/31141872/
- Author PDF: https://www.cs.toronto.edu/~fritz/absps/jjnh91.pdf

### 摘要转述

论文提出一种监督学习过程：系统由多个 expert network 构成，每个 expert 学习处理训练样本的一个子集。这个机制既可以看成模块化的多层监督网络，也可以看成带关联结构的竞争学习。实验上，模型能把元音分类任务分解成适合简单 expert 处理的子任务。

### 引言转述

引言的核心动机是：单个大网络在面对由多个局部规律组成的问题时，容易把所有模式揉在一起学；更自然的做法是让多个 local experts 分别拟合不同区域，再由 gate 决定每个样本交给谁。关键不是手工指定样本属于哪个 expert，而是让 gate 和 experts 一起适应训练数据。

### 要解决的问题

如何让多个简单 expert 自动分工，而不是把全部训练样本都压给同一个全局模型。

### 物理先验

数据可能由多个局部规律组成。每个 expert 只需要学局部子任务，因此比单一模型更容易拟合。

### 分析故事线

1. 每个样本经过 gate 得到 expert 权重。
2. expert 输出按权重组合。
3. 训练误差反过来改变 gate，使表现更好的 expert 在类似样本上权重更高。
4. 由此形成 soft competition 和 specialization。

### 对 A06 的启发

这篇是 A06 soft-router 梯度分析的源头语言。它支持把 router 更新写成：

\[
\Delta w_e\propto p_eA_eh.
\]

对 A06 来说，关键不是“router 是否能分工”，而是每个 feature 样本是否给目标 expert 一个正的 advantage。如果没有这个 advantage，feature center 初始化只能靠初始 margin 暂时保持。

### 对未来分析的指导

读这篇时重点看：gate 的训练信号到底来自 expert output 的什么差异。对应 `A06_02_03_E01`，应测 \(A_e\)、\(p_eA_e\)、\(\Delta w_e\)。

## 4. 论文 2：Hierarchical Mixtures of Experts and the EM Algorithm

Source:
- Michael I. Jordan, Robert A. Jacobs, 1994 / related 1993 IJCNN PDF.
- Author PDF: https://www.cs.toronto.edu/~hinton/absps/hme.pdf
- MIT Press page: https://direct.mit.edu/neco/article/6/2/181/5779/Hierarchical-Mixtures-of-Experts-and-the-EM

### 摘要转述

论文提出树状 supervised learning 架构。底层是 generalized linear experts，内部节点是 gating networks。模型被解释为层级 mixture model，学习被写成最大似然问题，并用期望最大化算法进行参数更新；同时也给出在线增量更新形式。

### 引言转述

引言把 HME 放在 divide-and-conquer 学习传统中：CART、MARS、ID3 等方法通过划分输入空间并在局部区域拟合简单函数来解决复杂问题。HME 的目标是把这种区域划分变成 soft boundary 和可训练 neural architecture。也就是说，gate 不只是分类器，而是在学习输入空间的可微软划分。

### 要解决的问题

如何把复杂监督学习问题拆成嵌套区域，让不同 expert 在不同区域拟合简单规律，同时用概率模型给训练提供清晰目标。

### 物理先验

复杂函数可以分解为多个局部简单函数；输入空间存在层级区域结构。

### 分析故事线

1. gate 给每个输入分配 prior probability。
2. 观察输出后，用 Bayes rule 计算 posterior responsibility。
3. EM 的 E step 估计“哪个 expert 生成了这个样本”。
4. M step 用责任权重分别更新 expert 和 gate。

### 对 A06 的启发

这篇给 A06 一个很干净的概念区分：

- prior routing：只看 hidden state 的路由概率；
- posterior responsibility：看完 label / loss 后，哪个 expert 更该解释这个样本。

A06 当前的 top-1 router 问题可以说成：训练时 router 是否能从 task loss 形成足够清楚的 posterior-like correction。如果 top-1 只更新被选 expert，而不评估未选 expert，就缺少 HME 式的完整责任重分配。

### 对未来分析的指导

06_30 可以先在 soft router 中构造 posterior-like quantity：

\[
\rho_e \propto p_e\exp(-\ell_e),
\]

再比较它和 gradient-defined \(p_eA_e\) 是否给出一致的 row movement 方向。

## 5. 论文 3：Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer

Source:
- Noam Shazeer et al., 2017.
- arXiv: https://arxiv.org/abs/1701.06538
- OpenReview: https://openreview.net/forum?id=B1ckMDqlg

### 摘要转述

论文关注 conditional computation：通过每个样本只激活部分网络，显著增加参数容量而不等比例增加计算。作者提出 sparsely-gated MoE layer，由大量 feed-forward experts 和一个 trainable gating network 组成。该模型用于语言模型和机器翻译，在较低计算代价下提升性能。

### 引言转述

引言的重点是容量与计算的矛盾：模型容量受参数量限制，但每个 token 都使用全部参数会过于昂贵。conditional computation 理论上可以解决这个问题，但实践中存在训练不稳定、负载不均衡、并行效率等困难。论文的贡献是把稀疏 MoE 做成可实际训练的大规模模块。

### 要解决的问题

如何在不显著增加每样本计算的情况下，大幅增加模型参数容量。

### 物理先验

不同样本不需要调用同一组参数；样本级稀疏激活可以把容量和计算解耦。

### 分析故事线

1. gate 对每个样本产生 expert 分数。
2. 加入噪声并保留 top-k experts。
3. 只计算被选 experts。
4. 用 auxiliary losses 控制 load balance。
5. 通过大规模并行实现容量扩展。

### 对 A06 的启发

这篇主要不是理论分析，但它定义了现代 sparse MoE 的工程表面。它明确提示：top-k sparsity 会带来理论上可怕的 discontinuity，但工程上通过 noise、load loss 和大 batch 稳住。

对 A06 来说，这正好提出一个反问题：

> 工程上可训练不等于 feature binding 可保持。

`A06_02_03_E01/E02` 应该把 top-1 的 discontinuity 具体化为：选中 expert 的梯度、未选 expert 的梯度、以及 margin crossing。

### 对未来分析的指导

读这篇重点看 noisy top-k gating 和 load balancing。不要把 load balance 当 specialization；A06 必须继续用 feature NMI、matched preserve、margin p05 做主指标。

## 6. 论文 4：Towards Understanding Mixture of Experts in Deep Learning

Source:
- Zixiang Chen, Yihe Deng, Yue Wu, Quanquan Gu, Yuanzhi Li, 2022.
- arXiv: https://arxiv.org/abs/2208.02813
- NeurIPS abstract: https://proceedings.neurips.cc/paper_files/paper/2022/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html

### 摘要转述

论文试图形式化解释 MoE layer 为什么能提升深度学习，以及 mixture 为什么不会坍缩成单模型。作者认为 underlying problem 的 cluster structure 和 expert 的非线性是 MoE 成功的关键。在一个带内在 cluster 结构的分类问题中，单 expert 很难学习，而 MoE 可以由 router 学到 cluster-center features，把复杂问题拆成更简单的线性分类子问题。

### 引言转述

引言的问题意识是：MoE 在实践中很成功，但为什么不 collapse、为什么 router 能分出有用 expert，理论上还不清楚。作者先用经验观察提出 cluster structure 和 nonlinear expert 的重要性，再构造一个可证明的分布，让 MoE 的优势可以被数学刻画。

### 要解决的问题

在什么结构化数据分布下，MoE 的 router 可以学到有意义的分区，并使 experts 分别解决更简单的问题。

### 物理先验

数据有 cluster 结构；router 学 cluster-center features 后，expert 可以在各自 cluster 上解决低复杂度子问题。

### 分析故事线

1. 构造单 expert 难以学习的 cluster classification。
2. 使用非线性 experts 和 router。
3. 证明 router 可以学习 cluster-center features。
4. 解释 MoE 如何把复杂问题拆成局部简单问题。

### 对 A06 的启发

这篇是最接近我们“feature center”语言的理论工作。但它和 A06 的关键差别是：

- 它关心 MoE 为什么能在特定 cluster 分布上成功学习；
- A06 现在关心在已知 center 附近初始化后，router margin 为什么被训练信号保持或吃掉。

也就是说，它支持“cluster-center feature 可以成为 router 学习对象”，但不能替代 A06 的 preservation dynamics。

### 对未来分析的指导

读这篇重点抽取：router 学 cluster center 的梯度条件。然后问：它的条件在我们的 synthetic full-LM setting 中是否成立？如果不成立，失败项是 expert advantage 不够，还是 top-1 feedback 不够？

## 7. 论文 5：Demystifying Softmax Gating Function in Gaussian Mixture of Experts

Source:
- Huy Nguyen, TrungTin Nguyen, Nhat Ho, 2023.
- arXiv: https://arxiv.org/abs/2305.03288
- NeurIPS paper PDF: https://papers.neurips.cc/paper_files/paper/2023/file/0ef6ffcb85a2d238fc4761860c31ded4-Paper-Conference.pdf

### 摘要转述

论文研究 softmax-gated Gaussian MoE 的参数估计。难点来自 softmax gate 的三个理论问题：参数只在平移等价下可识别，softmax gate 和 expert functions 之间有内在耦合，条件密度中分子和分母依赖复杂。作者提出 Voronoi-type loss 来刻画参数距离，并建立最大似然估计的收敛率。

### 引言转述

引言强调：MoE 统计模型中，expert 参数承担刻画数据异质性的任务，因此需要理解这些参数是否能被估计、估计速度多快。softmax gate 虽然常用，但归一化分母让不同 experts 的 gate 参数强耦合，导致传统 mixture 分析不够用。

### 要解决的问题

softmax gating Gaussian MoE 中，参数如何识别，最大似然估计以什么速率收敛。

### 物理先验

softmax gate 的归一化竞争会让 expert 与 gate 参数耦合；必须用几何化的参数距离来描述估计误差。

### 分析故事线

1. 明确 softmax gate 的平移不变性。
2. 用 Voronoi loss 捕捉参数之间的区域归属和距离。
3. 分析正确指定和过度指定 expert 数量下的收敛率。
4. 将速率退化和 polynomial equation solvability 联系起来。

### 对 A06 的启发

这篇提醒我们：softmax router row 不是彼此独立地学习 feature。因为 softmax 分母存在，某个 expert 的 row 更新会影响其他 expert 的概率。

这直接对应 A06 的量：

\[
p_aA_a-p_bA_b.
\]

也就是说，margin 变化是相对竞争项，不是单个目标 expert 的绝对优势。

### 对未来分析的指导

读这篇时重点看 identifiability 和 softmax coupling。`A06_02_03_E01` 应显式测竞争 expert 项，而不是只看 matched expert 的梯度 norm。

## 8. 论文 6：Statistical Perspective of Top-K Sparse Softmax Gating Mixture of Experts

Source:
- Huy Nguyen, Pedram Akbarian, Fanqi Yan, Nhat Ho, 2023/2024.
- arXiv: https://arxiv.org/abs/2309.13850
- ICLR paper: https://proceedings.iclr.cc/paper_files/paper/2024/hash/0fd489e5e393f61b355be86ed4c24a54-Abstract-Conference.html

### 摘要转述

论文从 Gaussian MoE 出发，分析 top-k sparse softmax gate 对密度估计和参数估计的影响。核心难点是 top-k sparse softmax 会把输入空间分割成多个行为不同的区域。作者提出新的参数 loss 来捕捉不同区域中的行为，并分析已知真实 expert 数和过度指定 expert 数时的收敛性质。

### 引言转述

引言的动机是：top-k sparse softmax 在大规模模型中常用，但它不像普通 softmax 那样处处平滑；top-k 选择会让输入空间出现不同 active expert set，从而改变统计估计问题。这种区域化行为需要新的理论工具。

### 要解决的问题

top-k sparse gate 如何改变 MoE 的输入空间划分、密度估计和参数估计速度。

### 物理先验

top-k 不是简单的 softmax 稀疏化；它改变了输入空间的区域结构。不同区域内的参数可识别性和收敛行为不同。

### 分析故事线

1. 定义 top-k sparse softmax gate。
2. 观察它诱导多个输入 regions。
3. 为不同 regions 定义合适的 parameter loss。
4. 分析 true expert 数已知和 over-specified 两种情况。

### 对 A06 的启发

这篇和 A06 的 route margin / boundary 语言非常接近。A06 的 top-1 router 本质上就是把 hidden space 切成 regions：

\[
R_e=\{h:w_e^\top h\ge w_j^\top h,\forall j\}.
\]

margin crossing 就是样本从一个 region 进入另一个 region。该论文提醒我们，top-k sparse gate 的理论对象应是 region，而不只是 continuous probability。

### 对未来分析的指导

读这篇时重点看：top-k 如何定义 region-specific behavior。`A06_02_03_E02` 应把每一步更新标到 region：当前 sample 是否留在原 matched region，是否进入 competitor region，是否发生 sign flip。

## 9. 论文 7：Sigmoid Gating is More Sample Efficient than Softmax Gating in Mixture of Experts

Source:
- Huy Nguyen, Nhat Ho, Alessandro Rinaldo, 2024.
- arXiv: https://arxiv.org/abs/2405.13997
- NeurIPS 2024 paper: https://proceedings.neurips.cc/paper_files/paper/2024/file/d65befe6b80ecf7f180b4def503d7776-Paper-Conference.pdf

### 摘要转述

论文研究 sigmoid gating 相比 softmax gating 的样本效率。softmax gate 很常用，但它可能引入不必要的 expert competition，并导致 representation collapse。作者在回归框架中分析 over-specified MoE 的 least-squares estimator，证明在若干 expert function 设置下，sigmoid gating 比 softmax gating 有更快收敛率，因此达到同样估计误差需要更少样本。

### 引言转述

引言的问题是：softmax gating 因归一化竞争而广泛使用，但这种竞争未必总是必要。近年经验工作发现 sigmoid gating 可能更好，但缺少理论解释。论文目标是从 expert estimation 的角度证明 sigmoid gate 的样本效率优势。

### 要解决的问题

softmax competition 是否会降低 expert estimation 的样本效率；sigmoid gate 是否能缓解这种竞争。

### 物理先验

softmax 强制 experts 在一个 simplex 上竞争；sigmoid 允许更独立的 expert activation，因此可能减少不必要竞争。

### 分析故事线

1. 建立 over-specified regression MoE。
2. 比较 sigmoid 和 softmax gating。
3. 证明两种 gating regime 下的 identifiability 条件和收敛率。
4. 显示常见 feed-forward expert 下 sigmoid 更 sample efficient。

### 对 A06 的启发

A06 目前不是要换 sigmoid gate，但这篇非常重要，因为它把“softmax competition 可能是问题”从直觉变成可分析对象。

对 A06 的具体启发是：不能只看目标 expert 是否有正梯度，还要看 softmax denominator 是否把 competitors 推成错误方向。也就是要测：

\[
p_aA_a,\quad p_bA_b,\quad p_aA_a-p_bA_b.
\]

### 对未来分析的指导

如果 `A06_02_03_E01` 发现 softmax competition 项消耗 margin，即 \(p_bA_b\) 经常抵消 \(p_aA_a\)，那么后续可以考虑 sigmoid-like independent gating 作为 method candidate。但在该局部机制裁定前，换 gate 是过早的。

## 10. 论文 8：On the Representation Collapse of Sparse Mixture of Experts

Source:
- Zewen Chi et al., 2022.
- arXiv: https://arxiv.org/abs/2204.09179
- NeurIPS / OpenReview PDF: https://openreview.net/pdf?id=mWaYC6CZf5

### 摘要转述

论文指出 sparse MoE 通过 hidden representation 将 token 路由到最匹配的 experts，但学习这种 routing 会鼓励 token 围绕 expert centroids 聚集，产生 representation collapse。作者提出在低维超球面上估计 token-expert routing scores，并在跨语言预训练和下游任务上显示这种方法缓解 collapse、提升路由一致性和任务表现。

### 引言转述

引言的动机是：sparse MoE 提供更大容量和固定计算开销，但训练 routing 时，token representations 和 expert centroids 互相吸引，可能导致表征空间塌缩到少数模式。问题不只是 router assignment，也包括 hidden representation 被 router 反馈塑形。

### 要解决的问题

sparse MoE 中，routing 训练为什么会导致 representation collapse，以及如何通过改变 routing score 的几何空间缓解。

### 物理先验

router 不只是读 hidden state；router 的训练会反向塑造 hidden state。token hidden states 可能被拉向 expert centroids，减少表征多样性。

### 分析故事线

1. sparse routing 根据 token hidden 和 expert centroid 计算 score。
2. 训练鼓励 token 聚向被选 expert centroid。
3. 这种吸引可能造成 hidden representation collapse。
4. 把 routing score 放到低维 hypersphere 上，缓解 collapse。

### 对 A06 的启发

A06 之前主要分析 row drift 和 center drift；这篇强调二者不是独立的。router 更新会影响 representation，representation drift 又反过来改变 margin：

\[
\Delta m_f
=
(\Delta w_a-\Delta w_b)^\top\mu_f
+
(w_a-w_b)^\top\Delta\mu_f
+ \cdots
\]

因此 `A06_02_03_E01` 先 freeze hidden 是必要的；之后必须进入 `A06_02_04`，把 hidden drift 放回 margin budget。

### 对未来分析的指导

读这篇时重点看：routing score geometry 如何改变 representation dynamics。它可能启发我们之后把 row projection / hypersphere normalization 看成 preservation constraint，而不是简单 common subtraction。

## 11. 横向对照：它们分别帮助 A06 的哪一块

| A06 缺口 | 最相关论文 | 借鉴对象 | 不能直接拿来的地方 |
|---|---|---|---|
| soft router 一步更新 | Jacobs 1991; Jordan & Jacobs 1994 | responsibility / posterior correction | 它们不是 top-1 sparse Transformer MoE |
| sparse top-k 工程表面 | Shazeer 2017 | noisy top-k, load balance, discontinuity | load balance 不等于 specialization |
| cluster-center learning | Chen et al. 2022 | router 学 cluster-center features | 它分析成功条件，不分析我们 full-LM margin erosion |
| softmax gate 耦合 | Nguyen et al. 2023 softmax Gaussian MoE | identifiability, gate-expert coupling | 统计 Gaussian MoE 与 Transformer MoE 不同 |
| top-k 区域边界 | Nguyen et al. 2023/2024 top-k | region-specific behavior | 它不直接给训练中 sign flip 的实验指标 |
| softmax competition | Nguyen et al. 2024 sigmoid | competition 降低样本效率 | 不等于应立刻换 sigmoid gate |
| representation collapse | Chi et al. 2022 | router 和 hidden state 互相塑形 | 它的 method 不直接解决 A06 synthetic margin |

## 12. 对 A06 story 的更新

读完这些论文后，A06 的理论推进应变得更具体：

### 12.1 最小动力学对象

不要先问“router 是否学 feature”。应问：

\[
\mathbb E[p_aA_a-p_bA_b\mid f]
\]

是否为正。

如果这个量为正，feature margin 有增长压力。  
如果这个量为零，router 没有 modification 机制，只能靠初始化。  
如果这个量为负，训练会主动破坏 feature binding。

### 12.2 soft router 到 top-1 router 的桥

soft router：

\[
\Delta w_e=\eta\frac{p_e}{\tau}A_eh.
\]

top-1 router：

\[
\Delta w_j
=
\eta\frac{p_r}{\tau}(1_{j=r}-p_j)B_rh.
\]

区别是：soft router 比较所有 expert 的 advantage；top-1 主要看 selected expert 的 benefit。这个差异可能是 early lock-in 和 wrong assignment 不易纠正的根因。

### 12.3 margin-budget 的新拆分

之前 A06 已有：

\[
\Delta m_f
=
(\Delta w_a-\Delta w_b)^\top\mu_f
+
(w_a-w_b)^\top\Delta\mu_f
+\cdots
\]

现在第一项可以继续拆：

\[
(\Delta w_a-\Delta w_b)^\top\mu_f
\approx
\eta\frac{1}{\tau}
[p_aA_a-p_bA_b]h^\top\mu_f.
\]

这就是从“margin 发生变化”推进到“为什么 margin 发生变化”。

## 13. 下一步阅读时的问题清单

逐篇读时，不需要平均用力。每篇只带一个问题：

1. Jacobs 1991：expert advantage 如何反馈到 gate？
2. Jordan & Jacobs 1994：posterior responsibility 和 gradient advantage 是什么关系？
3. Shazeer 2017：top-k sparse gate 的工程 trick 是否掩盖了理论 discontinuity？
4. Chen et al. 2022：router 学 cluster center 需要什么数据和 expert 条件？
5. Nguyen et al. 2023 softmax：softmax denominator 如何让 row 更新强耦合？
6. Nguyen et al. 2023/2024 top-k：top-k region 如何定义边界和区域行为？
7. Nguyen et al. 2024 sigmoid：softmax competition 如何降低样本效率？
8. Chi et al. 2022：router 如何反向改变 hidden representation？

## 14. 对 06_30 Anchor 的直接指导

`06_02_03_utility_signed_local_dynamics_anchor.md` 只回答一个局部问题：

> frozen hidden 的 soft router 中，实际 router row 更新是否由 \(p_eA_eh\) 解释？

最小 protocol 应包含三类 batch：

1. 正确 feature batch：目标 expert 确实更适合 feature。
2. 噪声 batch：target 与 feature 无关。
3. common/background batch：高频共享模式产生 loss signal。

主指标：

\[
\operatorname{corr}(\Delta m^{\mathrm{pred}},\Delta m^{\mathrm{actual}}),
\qquad
\mathbb E[p_aA_a-p_bA_b\mid f].
\]

判定：

- 若预测和实际一致，soft-router 动力学模型成立。
- 若正确 feature batch 的 advantage gap 为正，说明有 modification 机制。
- 若噪声/common batch 的累计 margin 消耗更大，说明 preservation 失败是 signal-noise budget 问题。
- 若模型不一致，先修正理论或实现，不进入 top-1 和 MTP。

## 15. Source Map

- A06 story: `01_functional_specialization_and_utility_routing_cn.md`
- A06 story canonical: `01_functional_specialization_and_utility_routing.md`
- Jacobs et al. 1991: https://pubmed.ncbi.nlm.nih.gov/31141872/
- Jordan & Jacobs HME PDF: https://www.cs.toronto.edu/~hinton/absps/hme.pdf
- Shazeer et al. 2017: https://arxiv.org/abs/1701.06538
- Chen et al. 2022: https://arxiv.org/abs/2208.02813
- Nguyen et al. 2023 softmax Gaussian MoE: https://arxiv.org/abs/2305.03288
- Nguyen et al. 2023/2024 top-k sparse softmax: https://arxiv.org/abs/2309.13850
- Nguyen et al. 2024 sigmoid gating: https://arxiv.org/abs/2405.13997
- Chi et al. 2022 representation collapse: https://arxiv.org/abs/2204.09179
