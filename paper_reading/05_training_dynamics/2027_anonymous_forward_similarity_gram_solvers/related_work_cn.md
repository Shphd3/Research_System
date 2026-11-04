# 相关工作核查：原创性究竟可能在哪里

核查日期：2026-10-19。对象仅为研究者上传的匿名稿件。以下是有针对性的近邻核查，不是穷尽检索，也不保证“历史上首次”。检索使用原理与主题词，并未检索匿名作者身份。文献事实优先来自论文原文、作者预印本及正式会议／期刊页面；评述栏是 AI 比较判断。

## 与接收判断关系最大的既有工作

| 工作及一手来源 | 已有内容及本次核查深度 | 与本文的重合与差别 | 稿件是否已引用 |
|---|---|---|---|
| [Seeger et al., Auto-Differentiating Linear Algebra](https://arxiv.org/html/1710.08717v5)，2017；所查修订版为 2019 | 核查全文中可微分解及 §3.3：学习特征和超参数的线性模型可用可微 LQ；不先构造 Gram 有数值优势，算子支持 FP32 / FP64。2026-10-19 第二轮复核收紧原先“单精度训练也更稳健”的表述；未确认该文提供此类训练对照 | 直接限制“稳定前向／反向计算和等价代数改写”作为全新原则的原创性。本文的新增候选是匹配状态与实际优化器更新审计，而不是首次指出应采用稳定形式 | 是 |
| [Hovland / Hückelheim, Differentiating Through Linear Solvers](https://arxiv.org/html/2404.17039v2)，2024 | 核查全文：比较底层迭代实现求导和高层方程求导，主要为前向模式；解和导数的可靠性依赖求解器。v2 页显示作者顺序为 Hückelheim、Hovland，稿件书目采用另一顺序，不据此作实质判断 | 与“求解器结果可信不等于导数可信”直接接近。但不是本文的 Cholesky 阶段 FP32/FP64、反向模式全模型更新及训练后正则化干预 | 是 |
| [Wang et al., Backpropagation-Friendly Eigendecomposition](https://papers.nips.cc/paper_files/paper/2019/hash/7dd0240cd412efde8bc165e864d3644f-Abstract.html)，NeurIPS 2019 | 核查正式摘要：特征向量反向传播可能不稳，设计更稳定的可微计算 | “矩阵层需要专门检查反向”以及前后向采用不同策略已属已知方向；不能据此把本文自定义 VJP 本身当作新范式 | 是 |
| [Wang et al., Robust Differentiable SVD](https://arxiv.org/abs/2104.03821)，TPAMI，卷期 2022 | 核查摘要和作者机构全文：前向使用 SVD，反向用泰勒展开以避免迭代误差；讨论近重根下梯度不稳 | 说明更准的前向分解并不自动提供合适的反向。本文研究 Gram 求解的精度位置和实际更新，算子与实验目的不同 | 是 |
| [Song et al., Why Approximate Matrix Square Root Outperforms Accurate SVD in Global Covariance Pooling?](https://openaccess.thecvf.com/content/ICCV2021/html/Song_Why_Approximate_Matrix_Square_Root_Outperforms_Accurate_SVD_in_Global_ICCV_2021_paper.html)，ICCV 2021 | 核查正式摘要及论文相关段落：联合分析数据精度、梯度平滑性和条件数；前向 SVD、反向 Padé 近似 | 很强的“数值准确性、训练行为和任务表现要分开”的先例，且涉及真实任务。本文的新意必须具体落在求解阶段、优化器匹配和岭参数干预上 | 是 |
| [Higham & Mary, Mixed Precision Algorithms in Numerical Linear Algebra](https://doi.org/10.1017/S0962492922000022)，Acta Numerica 2022 | 核查正式摘要及作者公开稿入口：混合精度线性代数、稳定性和精度分配 | 分阶段配置精度、Gram 构造误差无法由后续高精度完全修复，不是全新数值原理；本文把这些问题接到端到端学习的实际更新 | 是 |
| [Bertinetto et al., Meta-learning with Differentiable Closed-form Solvers](https://openreview.net/forum?id=HyxnZh0ct7)，ICLR 2019；[作者预印本](https://arxiv.org/abs/1805.08136) | 正式检索记录确认可微闭式求解元学习；OpenReview 详情／PDF直接访问遇到验证。本次另核作者预印本，用于确认岭回归、学习超参数及 Woodbury 改写 | 本文独立分类器的方法基础，不是新分类器；对偶形式也是标准既有基线。数值审计结果可以是新实证，代数恒等式不能当新定理 | 是 |
| [Amos & Kolter, OptNet](https://proceedings.mlr.press/v70/amos17a.html)，ICML 2017；[Blondel et al., Efficient and Modular Implicit Differentiation](https://proceedings.neurips.cc/paper_files/paper/2022/hash/228b9279ecf9bbafe582406850c57115-Abstract-Conference.html)，NeurIPS 2022 | 核查正式论文摘要：优化问题作为可微层、通过最优性条件进行隐式微分 | 确立大背景；不能从“可微求解器本身”获得原创性。但这些论文不自动覆盖本文匹配 Adam 更新的所有具体实验 | 两者均是 |
| [Micikevicius et al., Mixed Precision Training](https://arxiv.org/abs/1710.03740)，ICLR 2018；[Lee et al., Training with Mixed-Precision Floating-Point Assignments](https://arxiv.org/abs/2301.13464)，TMLR 2023 | 核查作者预印本摘要与官方实现文档：混合精度训练和张量精度分配，不只关注推理输出 | 精度影响梯度与权重更新并不陌生；本文更窄地讨论 Gram 求解阶段，不能被通用 AMP 文献完全代替 | 两者均是 |
| [Sridhar & Johansen, Echo](https://arxiv.org/abs/2605.06997)，2026 | 核查作者预印本摘要：SKA、谱 Koopman 算子、核岭回归与流式状态 | 本文的 SKA 来源。受控字符模型删去了完整 Echo 中的若干结构，不能直接把结果推广为整个 Echo 或所有高效注意力模型的结论 | 是 |

这些最接近的经典工作在稿件中基本都已引用。严肃审稿应评估作者对差别是否交代充分，而不是错误指责作者“漏引”这些文献。

## 额外发现的近年工作

[**Mixed Precision Training of Neural ODEs**](https://arxiv.org/html/2510.23498v2)，Celledoni et al.，最初发表于 arXiv 2025-10，所查版本 2026-04。它联合配置低精度前向、状态存储与更高精度的累加／伴随计算，并报告内存与速度结果。这里核查了作者摘要及全文结构。它不是 Gram 求解的重复工作，但进一步说明“求解器前向与反向精度要分别设计”在近期学习社区也已有实践。稿件未引用。**本次未确认其正式同行评议发表情况，因此不把缺少比较作为拒稿依据。**

[**Mosaic: A Benchmark Suite for Differentiable Physics Solvers**](https://arxiv.org/abs/2606.27895)，Rehmann et al.，arXiv 2026-06。作者摘要报告：可微物理求解器在代价、雅可比条件数和兼容性上差别显著，但能够提供梯度的求解器可能达到相近最优点。本次仅核查摘要。它是“梯度／数值差异不自动等于最终效用差异”的近邻背景，系统类型不同，不能据此宣称本文被抢先完成。稿件未引用；**未核实同行评议状态，不作为强制补引或拒稿依据。**

ICLR 2027 官方指南明确区分应比较的已发表前作、同期工作及仅在 arXiv 的工作。这里的近年发现用于帮助定位，而不是扩大作者必须完成的实验清单。[官方指南](https://iclr.cc/Conferences/2027/ReviewerGuidelines)

## 本文可能真正新增的内容

1. 在相同参数、输入和优化器状态下，把求解器阶段精度一直追踪到全模型梯度及**实际 Adam／AdamW 参数变化**，而不止解向量或方向导数。这是具体审计证据的候选增量。
2. 把固定状态的前向／反向诊断、统一评估器下的独立训练终点以及训练期岭参数干预分开，从而限制因果解释。跨种子确认和 CPU/A100 单状态控制加强了其可信度，但并不等于大范围训练复现。
3. 分类器中，共享参考岭参数轨迹后，条件数的绝对路径离散程度降低 97.4%。这不是整段表示被解释的比例，却是可检验的训练干预事实。它是否提供超出已有原理的重要知识，仍需结合适用范围、实际决策价值和补充材料判断。

没有证据支持把本文定位为新的求导恒等式、新的岭回归算法、新的 SKA 架构或普适混合精度训练理论。也没有检索证据足以宣称整套匹配审计与岭干预已经被某一前作完整重复。较公平的定位是：**已有数值原理下，一项有具体增量但外推范围有限的训练实证审计。**
