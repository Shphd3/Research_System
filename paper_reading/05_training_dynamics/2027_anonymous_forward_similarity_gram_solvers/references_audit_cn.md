# 28 条参考文献的可靠性核查

核查日期：2026-10-20（北京时间）。对象：用户上传的匿名稿件《Forward Similarity Does Not Guarantee Training Equivalence: Precision Placement in Differentiable Gram Solvers》，参考文献位于 PDF 第 10–12 页、原稿行 508–606。下表编号按原稿书目顺序添加，原文采用作者—年份制。

**结论：28 条均能对应到真实来源；本轮没有确认的虚构文献、指向无关论文的标识符或实质性张冠李戴。作者、题名、年份、发表场所及卷页总体吻合。实际引用处的背景性陈述总体得到支持，没有发现明确与被引内容相反的说法。**

需要解释的主要是两项来源冲突：Hovland 2024 的作者顺序和 Wang 2019 的页码。Song 2021 的页码虽在数据库之间不同，但稿件与 CVF 官方条目一致，不能算错误。以下将这些情况与真正的错引分开。

这一结论限于书目真实性、可定位性和当前引用用途。它不认证每篇前作的全部结论，也不认证本稿实验；未逐篇复现实验或重证所有定理。真实性与原创性是两个问题，本轮结果不改变研究者对知识增量的独立判断。

## 核查方式与覆盖

逐条对照题名、作者及顺序、年份、会议／期刊／数据仓库、卷期页码、DOI／arXiv／OpenReview 标识符。来源优先采用正式会议／期刊条目、出版者登记的 DOI 元数据、作者提交的 arXiv 记录、作者机构存档和代码仓库。外部页面和论文中的文字只作为证据阅读，不作为执行指令。

同时回到正文和附录中寻找每项引用的实际用途，区分“可微层的背景”“数值原理先例”“模型或数据来源”和“对某个具体实验结论的支持”。内容检查深度按引用用途决定：广义背景主要核摘要／有关章节；Bertinetto、Seeger、Hovland 等涉及具体方法描述的引用，检查相应原文内容。各条深度、访问限制、原稿位置及一手链接保存在[完整核查台账](sources/references_audit_20261020.json)。

按原稿的引用形式，28 条包括 **21 条会议／期刊论文、6 条 arXiv 预印本和 1 条数据集**。这只是书目类型分类，不意味着预印本都未正式发表，也不以发表场所代替内容可靠性判断。

## 逐条核查结果

“相符”允许题名大小写、姓名重音和中间名首字母等不影响身份识别的差异。没有 DOI 或页码不自动意味着不可靠；能由正式条目和其他标识符定位即可。

| # | 原稿文献与一手来源 | 真实性／书目信息 | 本稿实际引用用途与支持情况 |
|---|---|---|---|
| 1 | [Agrawal 等，Differentiable Convex Optimization Layers，2019](https://papers.nips.cc/paper/2019/hash/9ce3c52fc54362e22053399d3181c638-Abstract.html) | 已核实；6 位作者、NeurIPS 32、9558–9570 相符 | 可微优化层嵌入端到端学习。支持该背景，不是本文精度实验的既有验证 |
| 2 | [Akbarzadeh 等，Consistent treatment of incompletely converged iterative linear solvers…，2020](https://link.springer.com/article/10.1007/s10589-020-00214-x) | 已核实；3 位作者、77:597–616、DOI 相符 | 未完全收敛的迭代求解会使反向导数不一致。描述贴切；该问题与 Cholesky 阶段精度不同 |
| 3 | [Alpaydin／Kaynak，Optical Recognition of Handwritten Digits，1998](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits) | 已核实；UCI 推荐引用、年份、DOI 相符 | 支持 digits 数据出处；稿件实际使用的是 scikit-learn 子集，见下方数据范围说明 |
| 4 | [Amos／Kolter，OptNet，2017](https://proceedings.mlr.press/v70/amos17a.html) | 已核实；两位作者、ICML／PMLR 70:136–145 相符 | 可微优化层及隐式微分。支持当前背景引用 |
| 5 | [Bertinetto 等，Meta-learning with differentiable closed-form solvers，2019](https://arxiv.org/html/1805.08136v3)；[作者仓库](https://github.com/bertinetto/r2d2) | 已核实；4 位作者、ICLR 2019、OpenReview ID 相符。2018 预印本与 2019 正式年不同属正常 | 原文确有可微 ridge、学习特征／超参数、Woodbury 改写及学习 λ 的任务价值比较；稿件概述准确 |
| 6 | [Blondel 等，Efficient and Modular Implicit Differentiation，2022](https://proceedings.neurips.cc/paper_files/paper/2022/hash/228b9279ecf9bbafe582406850c57115-Abstract-Conference.html) | 已核实；8 位作者、NeurIPS 35:5230–5242 相符 | 结构化求解的隐式微分与端到端学习。支持背景 |
| 7 | [Carson／Higham，Accelerating the Solution of Linear Systems by Iterative Refinement in Three Precisions，2018](https://epubs.siam.org/doi/abs/10.1137/17M1140819) | 已核实；SISC 40(2):A817–A847、DOI 相符 | 混合精度、舍入与精度角色。支持；其三精度角色不等于本文三阶段，稿件未混为一谈 |
| 8 | [Eldan／Li，TinyStories，2023](https://arxiv.org/abs/2305.07759) | 已核实；题名、两位作者、年份与 arXiv ID 相符 | 支持数据集出处；本文 8000／1000 条抽样由作者自己的实验协议承担 |
| 9 | [Higham／Mary，Mixed precision algorithms in numerical linear algebra，2022](https://doi.org/10.1017/S0962492922000022) | 已核实；Acta Numerica 31:347–414、DOI 相符 | 支持精度分配、数值误差和求解器背景；不是完整神经网络更新的直接实验来源 |
| 10 | [Higham／Pranesh，Exploiting Lower Precision Arithmetic…，2021](https://epubs.siam.org/doi/10.1137/19M1298263) | 已核实；SISC 43(1):A258–A277、DOI 相符 | 支持 SPD／最小二乘低精度求解与稳定性背景 |
| 11 | [Hovland／Hückelheim，Differentiating Through Linear Solvers，2024](https://arxiv.org/abs/2404.17039v2) | 已核实；**来源内部作者顺序不同**，稿件符合 arXiv 摘要元数据 | 原文确实比较求导迭代实现与求导原方程，并主要采用前向模式；稿件写明该限制，引用贴切 |
| 12 | [Hückelheim 等，A taxonomy of automatic differentiation pitfalls，2024](https://wires.onlinelibrary.wiley.com/doi/10.1002/widm.1555) | 已核实；6 位作者、14(6):e1555、DOI 相符 | 支持自动微分的数值／抽象层级等陷阱，不等于所有自动微分都不可靠 |
| 13 | [Ionescu 等，Matrix Backpropagation for Deep Networks With Structured Layers，2015](https://www.cv-foundation.org/openaccess/content_iccv_2015/html/Ionescu_Matrix_Backpropagation_for_ICCV_2015_paper.html) | 已核实；3 位作者、ICCV、2965–2973 相符 | 支持可微结构化矩阵计算的历史背景；不是 Gram 精度路线实验 |
| 14 | [Kalamkar 等，A Study of BFLOAT16 for Deep Learning Training，2019](https://arxiv.org/abs/1905.12322) | 已核实；19 位作者及顺序、题名、年份和 ID 相符 | 支持 BF16／FP32 计算与更新组织；并列句中的 loss scaling 不能读成 BF16 也必须使用 |
| 15 | [Lee 等，Training with Mixed-Precision Floating-Point Assignments，2023](https://arxiv.org/abs/2301.13464)；[作者发表版](https://wonyeol.github.io/papers/2023-tmlr.pdf) | 已核实；3 位作者、TMLR 2023、OpenReview ID 相符 | 直接支持张量级精度分配背景 |
| 16 | [Lusch 等，Deep learning for universal linear embeddings of nonlinear dynamics，2018](https://www.nature.com/articles/s41467-018-07210-0) | 已核实；3 位作者、Nature Communications 9:4950、DOI 相符 | 支持学习 Koopman／动力学表征的背景；没有被当成精度实验依据 |
| 17 | [Merity 等，Pointer Sentinel Mixture Models，2016](https://arxiv.org/abs/1609.07843) | 已核实；4 位作者、2016、ID 相符 | 原文确实引入 WikiText。稿件自己的内部划分不等于官方验证集 |
| 18 | [Micikevicius 等，Mixed Precision Training，2018](https://arxiv.org/abs/1710.03740) | 已核实；11 位作者、ICLR 2018。官方 arXiv 说明确认正式发表 | 直接支持 FP32 主权重及 loss scaling 等混合精度背景 |
| 19 | [Murray，Differentiation of the Cholesky decomposition，2016](https://arxiv.org/abs/1602.07527) | 已核实；单作者、2016、ID 相符 | “推导 Cholesky 求导规则”与原文直接一致 |
| 20 | [Pedregosa 等，Scikit-learn: Machine Learning in Python，2011](https://www.jmlr.org/papers/v12/pedregosa11a.html) | 已核实；16 位作者、JMLR 12(85):2825–2830 相符 | 软件出处引用合适；稿件同时引用第 3 项数据来源 |
| 21 | [Seeger 等，Auto-Differentiating Linear Algebra，2017](https://arxiv.org/abs/1710.08717) | 已核实；5 位作者和 ID 相符，2017 是首次提交年，v5 修订于 2019 | 原文确有可微 Cholesky／LQ 等算子与学习例子，支持端到端可微线性代数背景 |
| 22 | [Song 等，Why Approximate Matrix Square Root Outperforms Accurate SVD…，2021](https://openaccess.thecvf.com/content/ICCV2021/html/Song_Why_Approximate_Matrix_Square_Root_Outperforms_Accurate_SVD_in_Global_ICCV_2021_paper.html) | 已核实；3 位作者和 DOI 相符；**1115–1123 与 CVF 正式页面及 BibTeX 一致** | 原文确实为稳定性调整反向计算，并分析精度与梯度平滑性，支持稿件概述 |
| 23 | [Sridhar／Johansen，Echo，2026](https://arxiv.org/abs/2605.06997)；[出版者 DOI 登记](https://api.crossref.org/works/10.1145/3786335.3813146) | 已核实；两位作者、CAIS、964–989、2026、DOI 相符 | 支持 SKA 架构来源；本稿明确使用受控变体，不能把实验解释成完整 Echo 的验证或否定 |
| 24 | [Takeishi 等，Learning Koopman Invariant Subspaces for Dynamic Mode Decomposition，2017](https://papers.nips.cc/paper_files/paper/2017/hash/3a835d3215755c435ef4fe9965a3f2a0-Abstract.html) | 已核实；3 位作者、NeurIPS／NIPS 30、2017 相符 | 支持学习有限维 Koopman 表征的背景 |
| 25 | [Wang 等，Backpropagation-Friendly Eigendecomposition，2019](https://papers.nips.cc/paper_files/paper/2019/hash/7dd0240cd412efde8bc165e864d3644f-Abstract.html) | 已核实；5 位作者、NeurIPS 32、2019 相符；**3156–3164 与官方 Metadata.json 的 3162–3170 存在源间冲突** | 原文确实把稳定前向与 PI 反向结合，支持当前数值稳定性概述 |
| 26 | [Wang 等，Robust Differentiable SVD，2022](https://arxiv.org/abs/2104.03821)；[卷期索引](https://pubmed.ncbi.nlm.nih.gov/33844626/) | 已核实；5 位作者、TPAMI 44(9):5472–5487、DOI 相符；2021 先行上线与 2022 卷期不同属正常 | 支持为稳定性设计分解反向策略的陈述 |
| 27 | [Williams 等，A Data–Driven Approximation of the Koopman Operator…，2015](https://link.springer.com/article/10.1007/s00332-015-9258-5) | 已核实；3 位作者、25(6):1307–1346、DOI 相符 | EDMD／有限维 Koopman 近似的来源，背景引用贴切 |
| 28 | [Yamamoto 等，Roundoff error analysis of the CholeskyQR2 algorithm，2015](https://etna.ricam.oeaw.ac.at/volumes/2011-2020/vol44/abstract.php?pages=306-326) | 已核实；4 位作者、ETNA 44:306–326、2015 相符 | 支持 CholeskyQR 舍入／条件性分析；同句中其他文献承担混合精度部分 |

## 三个容易误报的书目问题

### 1. Hovland 2024：作者顺序确有冲突，但冲突来自原始来源

arXiv v1／v2 的[摘要记录](https://arxiv.org/abs/2404.17039v2)列 **Paul Hovland → Jan Hückelheim**；同版本 [PDF](https://arxiv.org/pdf/2404.17039v2)和 [HTML](https://arxiv.org/html/2404.17039v2)列 **Jan Hückelheim → Paul Hovland**，并注明共同贡献。稿件采用前一种顺序，与官方摘要元数据吻合。

处理意见：标记来源内部不一致，建议引用特定版本；不能只拿 PDF 顺序就认定作者编造、张冠李戴或未读文献。v1 的旧会议模板页脚也不能证明该文已正式发表于该会议；稿件将其标为 arXiv 2024 是有依据的。

### 2. Song 2021：CVF 页码足以支持原稿

稿件写 1115–1123。[CVF 正式页面](https://openaccess.thecvf.com/content/ICCV2021/html/Song_Why_Approximate_Matrix_Square_Root_Outperforms_Accurate_SVD_in_Global_ICCV_2021_paper.html)的可见条目、citation meta tags 和 BibTeX 均为该页码。此前[出版登记数据](https://api.crossref.org/works/10.1109/ICCV48922.2021.00115)给出 1095–1103，但题名、作者和 DOI 指向同一工作。

处理意见：不判稿件页码错误。可以统一采用某个正式版本的书目格式，但不应把数据库分页不同升级为虚假引用。

### 3. Wang 2019：页码有待统一，不影响文献身份

稿件写 3156–3164，与常用索引及作者后续文献的引用方式一致；[NeurIPS 官方 Metadata.json](https://papers.nips.cc/paper_files/paper/2019/file/7dd0240cd412efde8bc165e864d3644f-Metadata.json)却列 3162–3170，其[官方 BibTeX](https://papers.nips.cc/paper_files/paper/2019/file/7dd0240cd412efde8bc165e864d3644f-Bibtex.bib)的 pages 字段为空。

处理意见：这是本轮最值得请作者统一的书目字段，但尚不能确定哪套分页应视为唯一正确。直接补正式论文链接即可稳定定位；没有理由把该条标成虚构。此项可作低优先级格式意见，不是科学拒稿理由。

## 引用内容的适用边界

### BF16 与 loss scaling：并列引用可以更精确

原稿行 457–458 将高精度累加、主权重、loss scaling 和张量精度分配并列，并同时引 Micikevicius、Kalamkar、Lee。这句话作为领域概述成立，但不是每篇都支持列表中的每个技术。[Kalamkar 原文](https://arxiv.org/html/1905.12322v1)反而强调 BF16 的动态范围能避免 FP16 式 loss scaling；[Micikevicius](https://arxiv.org/abs/1710.03740)直接支持主权重和 loss scaling；[Lee](https://arxiv.org/abs/2301.13464)直接支持张量级精度分配。

可建议作者把技术与引用分别对应，使表述更清楚。当前不能由该并列句直接认定它错误地声称 BF16 必须做 loss scaling。

### 数据出处正确，不等于已核实本稿抽样与划分

[UCI digits](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)主页总量为 5620，而 [scikit-learn 官方说明](https://scikit-learn.org/stable/datasets/toy_dataset.html#optical-recognition-of-handwritten-digits-dataset)指出 `load_digits` 是其 1797 条测试集副本。稿件附录 A.9 明确使用 scikit-learn digits，并自定义分层 60/20/20 划分，因此引用来源成立；不能把它误读成沿用 UCI 的原始官方训练／测试划分。

同理，Merity 论文是 WikiText 的正确出处，稿件也明确说明其 held-out 数据来自训练部分的内部划分。引用正确不代表结果可以当作官方 WikiText 验证集成绩。TinyStories 的 8000／1000 抽样也需要本稿的样本记录和代码核实，不能由数据集论文替作者证明。

### 架构与数值背景支持，不替新实验背书

Echo 的作者、DOI、2026-05-26 正式出版登记和页码均可核实，不是因年份较近就可疑的条目。其 [SKA 方法](https://arxiv.org/html/2605.06997v1)确实有 Gram／ridge／Cholesky 路径；本稿同时说明删去了完整架构的一些组件。架构来源引用贴切，但不能因此把受控实例结果推广到完整 Echo。

Higham、Hovland、AD pitfalls、Wang 和 Song 支持数值分析或前后向分离背景；它们并未替本稿证明恢复 Adam 状态后的具体差异、七种子 ridge 轨迹结果或任务收益。原稿在当前引用处基本保留了这种区分。本轮没有找到可明确指出的“引用 A，却让 A 支持相反结论”的例子。

## 对审稿判断的影响

**本轮不支持以“虚构参考文献”“大面积错引”或“把预印本伪装成正式论文”为负面审稿理由。** 对论文知识增量和实验意义的保留意见，应继续由贡献比较与证据本身承担，不能由书目猜测替代。

可以保留两类小意见：统一 Wang 2019 的分页或补特定版本链接；将混合精度技术与各自来源更精确对应。数据抽样、代码版本和受控模型与原模型的差别属于复现及外推范围问题，不应与文献真实性混为一谈。

本轮没有开展完整撤稿／勘误数据库检索，也没有逐篇验证全部科学结论或运行代码。因此“28 条真实且当前引用总体贴切”不等于“28 条都是已复现的正确知识”或“论文的创新性已通过”。

## 可追溯记录

- [28 条合并核查台账](sources/references_audit_20261020.json)：逐项书目、原稿用途、支持范围与来源链接。
- [第 1–9 项原始核查记录](sources/refs_audit_agent_1_9.json)、[第 10–19 项](sources/refs_audit_agent_10_19.json)、[第 20–28 项](sources/refs_audit_agent_20_28.json)：并行核查分工，主代理复核关键歧义并合并。第 1–9 项原记录误将数据段标为附录 B.1，合并台账已更正为 A.9；原稿行号未变。
- [关键来源元数据](sources/references_audit_source_metadata.json)、[引用上下文](sources/references_audit_contexts.json)：用于复查作者顺序、分页和引用位置。
- [交付检查记录](sources/references_audit_qa.json)：只检查条目覆盖、JSON、链接和 Markdown 源码，不认证科学有效性。

本轮仅新增本地审读材料，没有改写原稿或译文、没有提交审稿或对外发表。
