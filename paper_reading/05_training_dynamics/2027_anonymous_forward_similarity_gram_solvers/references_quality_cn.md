# 参考文献质量、发表渠道与公开争议核查

核查日期：2026-10-21（北京时间）。按匿名稿件第 10–12 页书目原顺序覆盖全部 28 条。本文是 AI 辅助审读；不代表正式期刊认证、完整科学复现或研究者的最终审稿意见。文献真实性与引用是否贴切，另见[上一轮报告](references_audit_cn.md)。

**结论：大部分来源属于成熟主流会议或正规专业期刊，没有发现需要按“可疑出版渠道”整体剔除的一组文献。本轮未检出针对这 28 条的正式撤稿或已核实的核心证伪记录，但确实找到独立复现中的批评、数据质量报告，以及 Echo 所查版本中的内部理论表述不一致。**

最值得单列的不是“所有预印本都不可信”，而是：**#23 Echo 的特定梯度保证不宜无条件采用；#8 TinyStories 的数据版本与清理需核实；#11、#14、#19、#21 的完整版本缺少本轮能确认的正式主会／期刊评审保障。** #5 和 #25 有实际公开技术质疑，但现有证据不足以将整篇剔除。

## 1. 如何理解“权威认证”

学术文献没有一个全球统一、能保证论文正确的认证。这里分别检查：发表渠道是否真实且有学术组织／编辑部与明确审查流程；文章是否属于正式研究轨道，还是预印本、非归档 workshop 或数据记录；具体主张是否有推导、代码、独立复现及公开问题记录。

CCF 推荐目录可作为渠道声誉的参考，但 CCF 自己明确反对将目录直接当作单篇论文质量的判据；其适用范围也不能完整代表数值数学。本轮不为每个刊物虚构 CCF 等级、SCI 分区或“国际认证”。[CCF 官方说明](https://www.ccf.org.cn/Academic_Evaluation/By_category/)

需要保留的区别：

- NeurIPS、ICML、ICLR、ICCV 以及 JMLR、TPAMI 等可归为成熟主流学术渠道；这是渠道层面的评价。
- SISC、Acta Numerica、Computational Optimization and Applications、Journal of Nonlinear Science、ETNA 等应按数值分析／优化领域判断，不能因不是 ML 顶会而降低为可疑来源。
- TMLR、WIREs 和 Nature Communications 有正式编辑与评审流程；品牌不替代对具体内容的检查。
- ACM CAIS 2026 是正式、有研究论文双盲评审的新会议，首届尚无长期质量记录；ACM 出版不自动使它成为公认顶会。
- arXiv 是存档平台，内容筛查不是同行评审；但一篇文章放在 arXiv 上，也不说明它没有正式发表。[arXiv 官方政策](https://info.arxiv.org/help/moderation/index.html)

按实际已核状态，本组有 **22 条正式会议／期刊来源（包含 1 条邀请综述）、4 条尚未确认正式版的预印本、1 条有非归档 workshop 早期展示而完整版评审未确认的来源，以及 1 条数据记录**。这与上一轮“按原稿引用形式”统计不同：#17 虽在稿中引 2016 arXiv，实际已在 ICLR 2017 正式发表。

## 2. 争议检索的覆盖与边界

对每条题名结合 retraction、erratum、correction、criticism、reproducibility 等词查询，查看相应出版／作者页面、能访问的公开评审、独立复现和官方项目问题记录。对部分条目另做 PubPeer 域限定检索。搜索引擎索引不是 PubPeer 全库，也不能覆盖未公开或未被索引的质疑。

另从 Crossref 官方指定 GitLab 下载 Retraction Watch CSV 快照，扫描 **73,315 条记录**，比对全部 **28 个标准化题名和 13 个明确 DOI**，没有匹配。下载文件 67,642,568 字节，SHA-256 及匹配规则保存在[数据库核查记录](sources/quality_retraction_watch_check.json)。原文件有编码异常，两种解码方式均得到同样的零匹配结果。下载日期是本轮访问日期；GitLab 版本 API 超时，未确认快照最新提交时间。

该数据库对撤稿的收集较全面，但对更正、关注声明的覆盖较弱；零匹配不能当作“绝无争议”或质量认证。13 次 Crossref 单条更新 API 请求本轮因 TLS 连接错误未成功，已记录为未完成，未当作无更新的证据。[Crossref 数据说明](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/)

以下证据严格分开：正式撤稿／更正、独立复现结果、公开审稿中的质疑、用户未独立验证的问题报告、作者自述局限，以及本轮直接读原文得到的判断。公开有人质疑，并不等于质疑已成立；没有搜索结果，也不等于文章经过了充分外部复核。

## 3. 按书目顺序逐项评估

下表中的“未检出重大不利记录”仅指上述渠道和查询范围；各条检索词、政策及证据链接保存在[合并台账](sources/reference_quality_20261021.json)。简写题名用于对照，完整书目保持在原稿和上一轮报告中。

| # | 文献／当前已核渠道 | 渠道与审查判断 | 公开问题、可靠性及本稿处理 |
|---|---|---|---|
| 1 | [Agrawal 2019，Differentiable Convex Optimization Layers](https://papers.nips.cc/paper/2019/hash/9ce3c52fc54362e22053399d3181c638-Abstract.html)，NeurIPS 主会 | 成熟正式同行评审会议 | 公开评审质疑不可微点、“exact”措辞与示例代码条件；作者回应，最终接受。可作可微优化层先例，不能推出所有优化问题处处精确可微 |
| 2 | [Akbarzadeh 2020，Consistent treatment…](https://link.springer.com/article/10.1007/s10589-020-00214-x)，Computational Optimization and Applications | Springer 正规专业同行评审期刊 | 未检出重大不利记录。其截断迭代与伴随一致性问题有具体条件；可保留，不等于本文 Cholesky 精度比较已被验证 |
| 3 | [Alpaydin／Kaynak 1998，Optical Recognition…](https://archive.ics.uci.edu/dataset/80/optical+recognition+of+handwritten+digits)，UCI | 权威数据仓库记录，**不是期刊论文** | 支持出处；scikit-learn 子集与原数据划分需区分。不能要求数据 DOI 承担算法同行评审功能 |
| 4 | [Amos／Kolter 2017，OptNet](https://proceedings.mlr.press/v70/amos17a.html)，ICML 主会 | 成熟正式同行评审会议 | 作者 qpth 页面承认可行性与数值精度限制，double 可改善 float 不稳。是明确适用边界，可保留 |
| 5 | [Bertinetto 2019，Differentiable Closed-form Solvers](https://arxiv.org/html/1805.08136v3)，ICLR 主会 | 成熟正式同行评审会议；另有独立 ReScience 复现 | 主要结果在若干设置复现成功，但比较容量、训练策略、早期实现细节受到批评。**有条件保留**；不能把 benchmark 优势全部归于求解器 |
| 6 | [Blondel 2022，Efficient and Modular Implicit Differentiation](https://proceedings.neurips.cc/paper_files/paper/2022/hash/228b9279ecf9bbafe582406850c57115-Abstract-Conference.html)，NeurIPS 主会 | 成熟正式同行评审会议 | 未检出核心证伪。JAXopt 维护状态是软件生命周期问题，不是隐式微分理论被推翻；保留背景用途 |
| 7 | [Carson／Higham 2018，Three Precisions](https://epubs.siam.org/doi/abs/10.1137/17M1140819)，SISC | SIAM 专业学会正规同行评审期刊 | 未检出重大不利记录；收敛与误差界有条件。可保留，不能将条件界泛化为任意病态系统保证 |
| 8 | [Eldan／Li 2023，TinyStories](https://arxiv.org/abs/2305.07759)，已核为 arXiv | 本轮未确认同题正式会议／期刊版 | 官方数据仓库有重复、破损故事和空样本用户报告。**单列数据质量核查**；未证明本稿所选子集受影响 |
| 9 | [Higham／Mary 2022，Mixed Precision Algorithms…](https://doi.org/10.1017/S0962492922000022)，Acta Numerica | 成熟专业邀请综述；编委邀请、具名编辑合作及主编接受，**不能称普通双盲外审** | 未检出重大不利记录；作者明确最坏情形误差界可能保守。专业背景价值高，不替本稿实验背书 |
| 10 | [Higham／Pranesh 2021，Exploiting Lower Precision…](https://epubs.siam.org/doi/10.1137/19M1298263)，SISC | SIAM 正规专业同行评审期刊 | 未检出重大不利记录；算法依赖缩放、移位、预条件和迭代改进条件，保留这些条件即可 |
| 11 | [Hovland／Hückelheim 2024，Differentiating Through Linear Solvers](https://arxiv.org/abs/2404.17039)，arXiv | **尚未确认正式主会／期刊版**；模板页脚不是发表证明 | 未检出可靠核心反驳，但独立复核与正式评审保障有限。**作为辅助实证引用**，不承担关键结论的唯一证据 |
| 12 | [Hückelheim 2024，AD Pitfalls](https://wires.onlinelibrary.wiley.com/doi/10.1002/widm.1555)，WIREs | Wiley 正规综述期刊，有正式同行评审流程 | 未检出重大不利记录；适合概念分类与反例，不应被引成 AD 普遍无效的定理 |
| 13 | [Ionescu 2015，Matrix Backpropagation](https://www.cv-foundation.org/openaccess/content_iccv_2015/html/Ionescu_Matrix_Backpropagation_for_ICCV_2015_paper.html)，ICCV 主会 | CVF／IEEE 成熟正式同行评审会议 | 原文及后续研究指出近重特征值时某些反向实现不稳；是已知技术边界，可保留框架来源 |
| 14 | [Kalamkar 2019，BFLOAT16](https://arxiv.org/abs/1905.12322)，arXiv | **尚未确认同题正式评审版**；不能与另篇 ARITH 的 bfloat16 论文混淆 | 多工作负载的工业实证可作历史背景，但不构成所有模型／硬件均无需调整的保证。**条件使用** |
| 15 | [Lee 2023，Mixed-Precision Floating-Point Assignments](https://arxiv.org/abs/2301.13464)，TMLR | 正规机器学习期刊，官方双匿名、公开评审政策 | 未检出重大不利记录；代码可查。OpenReview 评审线程本轮未能读取，不声称所有评审无异议；保留 CNN 精度分配用途 |
| 16 | [Lusch 2018，Universal Linear Embeddings](https://www.nature.com/articles/s41467-018-07210-0)，Nature Communications | 正规综合同行评审期刊 | 未检出核心证伪；有公开实现。有限维、训练覆盖和外推条件重要，标题 universal 不等于所有非线性系统无条件可线性化 |
| 17 | [Merity，Pointer Sentinel Mixture Models](https://openreview.net/pdf?id=Byj72udxe)，**ICLR 2017 主会** | 已核正式同行评审；原稿引的是 2016 arXiv | 不应放入“未经评审”组。作为 WikiText 出处可保留，不能让本稿内部 holdout 冒充官方验证集 |
| 18 | [Micikevicius 2018，Mixed Precision Training](https://arxiv.org/abs/1710.03740)，ICLR 主会 | 成熟正式同行评审会议 | 未检出核心证伪。实现用户的微小非确定性报告不能推翻其“任务效果相当”的主张；任务相当也不保证逐步更新相同 |
| 19 | [Murray 2016，Cholesky Differentiation](https://arxiv.org/abs/1602.07527)，技术预印本 | **未确认正式期刊／主会版** | 作者伴随代码承认测试不足；但公式有可检查推导，并被 Theano 源码采用。**保留公式出处，勿给软件全面稳定性背书** |
| 20 | [Pedregosa 2011，Scikit-learn](https://www.jmlr.org/papers/v12/pedregosa11a.html)，JMLR | 成熟机器学习专业同行评审期刊 | 未检出重大不利记录；软件来源合适。软件功能、具体数据和版本仍分别核验 |
| 21 | [Seeger 2017／2019，Auto-Differentiating Linear Algebra](https://arxiv.org/abs/1710.08717) | 早期短版为 **NIPS 2017 非归档 Autodiff workshop poster**；未确认五作者完整 v5 的正式期刊／主会评审 | 推导与实现可核查，未检出具体证伪；**辅助来源**。不得称 NeurIPS 主会长文，也不应忽略其实现价值 |
| 22 | [Song 2021，Approximate Matrix Square Root…](https://openaccess.thecvf.com/content/ICCV2021/html/Song_Why_Approximate_Matrix_Square_Root_Outperforms_Accurate_SVD_in_Global_ICCV_2021_paper.html)，ICCV 主会 | 成熟正式同行评审会议 | 未检出重大不利记录；本身比较精度／梯度／条件数／任务，可保留。不同算法与任务结果不能直接移植到 Gram 求解器 |
| 23 | [Sridhar／Johansen 2026，Echo](https://arxiv.org/pdf/2605.06997)，ACM CAIS 首届 | 正式新专业会议，官网有双盲及独立 artifact 流程；**尚无长期声誉记录** | **重点复核**：所查 arXiv v1 正文的无条件梯度满秩／正交保证与附录条件冲突。架构出处可引，强理论保证不宜无条件采信 |
| 24 | [Takeishi 2017，Koopman Invariant Subspaces](https://papers.nips.cc/paper_files/paper/2017/hash/3a835d3215755c435ef4fe9965a3f2a0-Abstract.html)，NeurIPS／NIPS 主会 | 成熟正式同行评审会议 | 未检出重大不利记录；可保留学习 Koopman 子空间背景，不提供任意系统全局精确表示保证 |
| 25 | [Wang 2019，Backpropagation-Friendly Eigendecomposition](https://papers.nips.cc/paper/2019/file/7dd0240cd412efde8bc165e864d3644f-Reviews.html)，NeurIPS 主会 | 成熟正式同行评审；公开评审有真实技术争论 | 对称矩阵范围、epsilon 正则与比较公平性、近不可微处反向近似价值受质疑。最终接受，后续改进明确局限；**有条件保留先例用途** |
| 26 | [Wang 2022，Robust Differentiable SVD](https://arxiv.org/abs/2104.03821)，IEEE TPAMI | 成熟专业同行评审期刊 | 未检出重大不利记录；它改进早期 PI 的误差／成本。仓库问题中的澄清不能当作已证实错误，可保留 |
| 27 | [Williams 2015，EDMD](https://link.springer.com/article/10.1007/s00332-015-9258-5)，Journal of Nonlinear Science | Springer 正规动力系统专业同行评审期刊 | 未检出重大不利记录；有限字典／采样的近似受条件限制，不是精度训练结论来源 |
| 28 | [Yamamoto 2015，CholeskyQR2 Roundoff Analysis](https://etna.ricam.oeaw.ac.at/volumes/2011-2020/vol44/abstract.php?pages=306-326)，ETNA | 正规数值分析专业同行评审期刊；官方投稿说明明确外审 | 未检出重大不利记录；稳定性受满列秩和条件数等假设限制。可保留，不改写为任意病态矩阵无条件稳定 |

## 4. 摘出的重点条目：哪些部分不宜直接依赖

### 第一优先级：#23 Echo 的特定理论保证

**这是本轮最明确的内容层面警报，不是单凭新会议身份作出的判断。** [CAIS 官网](https://www.caisconf.org/)确认首届，[CFP](https://www.caisconf.org/pages/cfp/)明确研究论文双盲审稿。没有找到可核实的掠夺性出版证据；会议提供 artifact 流程不等于 Echo 本身获独立复现认证。

本轮核查 [arXiv v1 的 PDF](https://arxiv.org/pdf/2605.06997)第 4 页与第 22–23 页：正文称 SKA 的满秩由构造保证，附录则要求值映射满秩和转移算子可逆，并明确无条件说法一般不成立。正文另称 MLP 谱核正交且奇异值均为 1，附录却给出一般的缩放旋转形式。

这是可直接检查的数学区别。令单个谱块

\[
R_i=\begin{pmatrix}\gamma_i&\omega_i\\-\omega_i&\gamma_i\end{pmatrix},\qquad
\rho_i=\sqrt{\gamma_i^2+\omega_i^2}.
\]

由乘法可得 \(R_i^\top R_i=\rho_i^2 I\)。把 \(\rho_i\) 限制在不大于 1，只保证非扩张；只有 \(\rho_i=1\) 才是正交等距。允许的 \(\gamma_i=1/2,\omega_i=0\) 就给出缩小一半的块。类似地，ridge 使 Gram 可逆，不会使数据产生的所有交叉统计也满秩；值映射为零时，query 到输出的雅可比仍可为零。

**处理：** 不把该版本正文的无条件梯度保证当既定事实；应采用附录的有条件陈述或独立推导。这个问题由本轮直接审读提出，不是已发表的外部证伪；没有据此认定其数据造假。尚未完整比对 ACM 最终版是否保留同样表述。当前被审稿只用它交代 SKA 来源，未发现直接依赖上述保证；不应因前作的这处问题自动否定本稿独立数值测量。

### 第二优先级：#8 TinyStories 的数据质量与未确认评审状态

作者机构页面及 arXiv 当前可核记录仍为预印本。作者数据仓库的用户报告包括[训练内重复及文件版本差别](https://huggingface.co/datasets/roneneldan/TinyStories/discussions/12)、[故事清理报告](https://huggingface.co/datasets/roneneldan/TinyStories/discussions/15)和[带索引的空样本报告](https://huggingface.co/datasets/roneneldan/TinyStories/discussions/23)。这些是具体原始问题报告，不是本轮独立重算，也不是正式证伪；训练内重复不等于训练／验证泄漏。

**处理：** 本稿应交代具体数据文件／版本、去空与去重规则，以及所选 8000／1000 条记录的跨划分重叠检查。当前没有证据证明本稿子集一定含这些问题。同一输入下的数值精度对照不会仅因故事质量自动失效，但任务损失和泛化解释需要数据质量支持。

### 审查保障较弱，需用其他证据支撑：#11、#14、#19、#21

- **#11 Hovland／Hückelheim：** 本轮未确认正式发表和独立复现。可支持一个探索性数值例子，关键结论宜同时由正式 AD 文献和本稿实验支撑。arXiv 作者顺序冲突不构成技术不可靠证据。
- **#14 Kalamkar BF16：** 可引用工业经验与张量计算组织，不能把特定模拟实验扩为全部模型、全部硬件的保证。未找到正式评审记录，不等于已有反驳。
- **#19 Murray：** 作为可检查的公式出处有实质支持，[Theano 源码](https://github.com/Theano/Theano/blob/master/theano/tensor/slinalg.py)采用其推导；[作者示例代码](https://github.com/imurray/chol-rev)测试不充分则限制直接复用软件的信心。公式、代码成熟度和性能结论应分别评价。
- **#21 Seeger：** [官方 workshop 页面](https://autodiff-workshop.github.io/)确认早期展示及非归档性质，不能冒充 NeurIPS 主会评审。完整版本的具体关键推导仍需检查；既有开源实现是正面线索，非全部实验已独立复现的证明。

这组是“证据保障需补足”，不是判定整篇低质或建议一概删除。

## 5. 确有批评，但不宜列成“不可靠文章”

**#5 Bertinetto。** [独立 ReScience 复现](https://zenodo.org/records/3160540)和 [EPFL 原始存档](https://infoscience.epfl.ch/record/265667)同时报告了主要结果的成功复现，以及早期实现说明、特征容量和训练策略比较的问题。作者据反馈更新并发布代码。应限制“求解器单独造成全部 benchmark 优势”的归因，但这没有推翻 ridge／Woodbury 作为模型组件的事实；对当前引用用途，复现支持总体是正面证据。

**#25 Wang 2019。** [正式公开评审](https://papers.nips.cc/paper/2019/file/7dd0240cd412efde8bc165e864d3644f-Reviews.html)中，一位评审质疑对称矩阵适用范围、正则化和实用技巧使比较不公平；另一位保留了近不可微处近似导数的意义及任务收益疑问。也有评审认可稳定性实验。[作者回应](https://papers.neurips.cc/paper_files/paper/2019/file/7dd0240cd412efde8bc165e864d3644f-AuthorFeedback.pdf)说明各方法采用相同 epsilon，补充匹配截断技巧的对照，承诺明确对称矩阵范围，并强调稳定性而非最高任务准确率。不能把投稿时意见全部当最终稿已确认的缺陷，更不能隐去回应、正面意见与最终接受。该文及其后续 TPAMI 改进仍可作为前后向分开设计的先例。

同理，#1 的普通同行评审质疑、#4 的作者自述数值限制、#6 的项目维护状态、#13 的近重根边界，不足以构成“文章整体不可靠”的认定。软件问题、适用条件和理论错误是不同证据。

## 6. 对当前匿名稿的实际影响

1. **不宜声称“参考文献主要来自不权威渠道”。** 核心数值背景有正式专业期刊与成熟会议支持；没有必要靠几篇预印本独力建立全部前提。
2. **最强的新增质询是具体的。** 作者是否依赖 Echo 的无条件梯度保证；TinyStories 实际子集是否做了必要清理和重叠检查。前者涉及机制前提，后者涉及任务测量，两者都比泛称来源不权威更可审查。
3. **预印本／workshop 身份影响证据权重，不自动决定科学价值。** 需看实际被借用的是可核对公式、模型出处，还是未经独立确认的强经验断言。
4. **现有公开问题尚不足以直接否定本稿全部实验。** 当前稿对精度路线的本地测量需要由自己的代码、状态恢复和数据证据支撑；对创新性和意义的质疑仍需独立论证。

因此，本轮可以摘出需要限制的文献和主张，但不能形成“这些文章已被证伪，故引用它们的稿件应拒绝”的结论。

## 7. 记录与未完成的覆盖

[完整台账](sources/reference_quality_20261021.json)含全部 28 项和分层判断；[第 1–9 项](sources/quality_refs_1_9.json)、[第 10–19 项](sources/quality_refs_10_19.json)、[第 20–28 项](sources/quality_refs_20_28.json)保留查询词、原始来源与访问限制。[Retraction Watch 检查](sources/quality_retraction_watch_check.json)、[版本查询限制](sources/quality_retraction_watch_version.json)、[Crossref 请求失败记录](sources/quality_crossref_current_updates.json)、[Echo 原文对照](sources/quality_echo_internal_check.json)及 [CAIS 政策核查](sources/quality_cais_policy_check.json)供复查。

没有运行 28 篇论文的全部实验、审计所有实现或读取所有私有／不可访问评审。部分 OpenReview 和 Nature 评审文件遇访问限制；CCF 页面直接请求受防护，故未声称逐刊逐会核完当前等级。未采用 AI 摘要聚合站替代独立科学评论。数据库负结果和公开检索均不能排除未报告问题。

本轮仅新增本地审读材料；没有提交审稿、联系作者、推送或对外发表。
