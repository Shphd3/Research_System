# SAE 表征几何、稀疏预算与语义对应：文献调研

日期：2026-09-18  
性质：文献调研与研究判断备忘；不是已批准的实验协议，也不记录新实验结果。  
配套文档：`02_冻结检查点表征审计_实验规划_cn.md`

## 摘要

本轮应把“SAE旁支没有训崩”保留为可行性结论，而不要提升为方法有效。接下来需要回答三个相互独立的问题：主干原始表示的语义组织是否改变；SAE的字典与编码是否忠实、容易读取地描述这种组织；固定的每词元稀疏预算是否丢失任务相关因素。

最重要的概念澄清是：每个词元至多32个激活，不意味着所有语义共同位于一个32维子空间。固定激活集合时，线性解码输出至多位于一个32维仿射子空间；不同输入选择不同集合，整体是许多子空间的并集。但这也不意味着它能无损表达任意高维连续结构。原始主干没有经过硬瓶颈，而且还保留重构误差，因此必须把原始表示、稀疏系数、重构及误差分开分析。

文献中适合本项目的主要工具不是另一项“总分”，而是：跨条件语义读出、语义与词汇/模板的关系矩阵、类条件几何与维度、单特征及多特征的概念检测、经机会校正的聚类对应、重构后的语义保留，以及特征组的选择性干预。其中，2026年的SAE评测审计提示：不要直接把默认TPP/SCR或自动解释分数当成方法有效性的可靠终点。

**建议本轮先冻结现有Dense与SALL检查点，开展三项审计，而不启动新一轮主模型预训练：语义组织、特征对应、稀疏预算。**它们分别判断应继续主干正则、把SAE改作读取工具，还是修改固定稀疏假设。

## 1. 材料与结论边界

### 1.1 项目已有信息

依据本轮用户报告：组会认同旁支训练可继续研究，但语义对应性、稀疏预算合理性和表征改善均未确立。此前展示的P/N面板、Dense/S7/S37/SALL和10B检查点仅作为拟议审计入口；本轮没有读取原始张量、复核指标数值或运行新实验。

旧会议稿已经要求将“原始表征”和“SAE激活/重构”分开评测。本轮沿用这一问题划分，不沿用旧摘要中“Fisher上升即证明更可分”的强解释。

### 1.2 文献能支持什么

本调研以论文原文、官方论文集和作者公开预印本为依据。经典研究的实验对象包括神经记录、视觉网络和语言模型；从前两者迁移到当前8层模型的部分，均属于AI实验建议。来源的正式发表状态与预印本状态分开列出。

论文中的“特征质量”“流形容量”“语义对应”和本项目的“模型有效容量”不等同。调研不把论文的单项指标正结果，转换成当前主干已改善的证据。

## 2. Top-K=32究竟限制什么？

### 2.1 四种量必须区分

| 量 | 含义 | 是否由Top-K=32确定？ |
|---|---|---|
| 主干宽度d | 每个表示有多少坐标 | 否 |
| 字典宽度M | 可供使用的字典原子总数 | 否 |
| 激活预算K | 单个输入允许使用多少个原子 | 在每词元Top-K实现中，是 |
| 语义结构的维度 | 指定语义及变化范围所需的连续自由度，或某个操作性维度指标 | 否 |

首先核实实现：每词元Top-K限制每个输入的激活数；BatchTopK主要控制批内平均预算，不保证每个输入都是32。词元激活取句均值后，也可能不再稀疏。不能把这三种对象用同一条维度上限解释。[R01–R02]

### 2.2 数学图像：许多小平面的并集，不是一张共同的小平面

假设解码器是固定线性的：

$$\hat h=b+Dz,\qquad D\in\mathbb R^{d\times M},\quad \|z\|_0\le K.$$

固定激活位置集合S后：

$$\hat h\in b+\operatorname{span}(D_S),\qquad \operatorname{rank}(D_S)\le K.$$

允许集合随输入变化，得到：

$$\hat h\in\bigcup_{|S|\le K}\left(b+\operatorname{span}(D_S)\right).$$

这是从模型定义直接得到的结论。即使K=1，输入也可以分别位于很多不同坐标轴上，整体线性张成空间远大于1维。因此“总体协方差有160个方向”不必与“每次只用32个原子”矛盾。

但不要过度纠正：有限字典所形成的有限个至多32维子空间，不能无损覆盖一个真正具有160个连续自由度的开放区域。对于固定支持、没有其他数据相关旁路的线性解码器，其局部连续变化也不能突破该支持的秩。支撑集合的组合选择提供离散表达能力，不等于无限的连续维度。

### 2.3 为什么这还不能直接判定当前正则太强？

当前约束在旁支，主网络使用的是h，而不是强制替换为hat h。写成：

$$h=\hat h+e.$$

重构误差e可以保留其他信息；有限权重的正则也不要求误差严格为零。因此，真正需要问的是：**哪些信息被重构了，哪些留在误差里，它们是否影响任务？**

即使某个语义类别内有160个显著协方差方向，也可能包括模板、实体、位置、幅度和噪声；反之，30维的连续结构也不保证当前字典用30个非负原子就能准确表示。不能用一个估计维度直接设定K。

### 2.4 更可检验的替代问题

不要先追问“语义真实维度到底是32还是160”，先测：

$$K\longmapsto\{\text{重构失真、语义保留、误差中的可读信息、任务影响}\}.$$

分别训练K=16、32、64、128的离线观察器。Gao等人的研究指出，对只在一个K上训练的SAE直接改变推理K，甚至可能使重构误差非单调变化。因此仅修改已有SAE的Top-K开关，不能作为预算充分性的决定性检验。[R01]

## 3. 不应默认语义形成一个个互不重叠的“小球”

“小球”包含至少三个未经验证的前提：每个语义只对应一个连通区域；区域在所选距离下近似各向同性；一个样本只属于一个语义。

自然语言里，一个样本可以同时涉及物理、数值计算、因果关系与时间顺序。不同概念可能共享因素；一个概念也可以在不同上下文中形成多个区域。因此，除了球状簇，还需要允许细长子空间、弯曲结构、多个子簇和共享方向。

Engels等人在语言模型中分析了多维特征组及周期性概念；其方法包含对SAE字典方向分组、分析组内部分重构和结构干预。它为“不把所有概念强制解释成一个字典原子”提供了直接案例，但没有证明每个语义都应是流形或每个聚类都是真实概念。[R03]

对本项目，最稳妥的目标是：**与语义无关的变化不应轻易破坏读出，相关语义的差异应可以在所需预算下被识别。**不要求所有概念全局正交，更不预设每个domain都必须对应一个专家。

## 4. 表征分析的方法地图

下表中的“迁移到本项目”是AI建议，不是原论文已在本项目上验证的结论。

| 要回答的问题 | 文献与方法 | 迁移到本项目 | 不能声称 |
|---|---|---|---|
| 表示发生了什么变化？ | CKA，Kornblith等，ICML2019 [R14] | 相同样本比较层/检查点的关系结构，定位变化 | CKA变小就是变好，或CKA高意味着功能相同 |
| 距离主要对应语义还是词汇？ | RSA，Kriegeskorte等，2008 [R15] | 表征距离与语义、模板、词汇距离模型分别比较 | 距离相关就是因果机制 |
| 类别差异是否被各向异性噪声掩盖？ | 交叉验证Mahalanobis距离，Walther等，2016 [R16] | 用训练数据估计收缩协方差，在独立样本间测类均值差异 | 它优于所有语言模型指标，或无条件无偏 |
| 相同语义跨上下文是否仍能读出？ | CCGP，Bernardi等，Cell2020 [R11] | 在部分词汇/领域/表述中训练，在新条件中测试 | 新测试只是原始随机划分的另一次准确率 |
| 类簇为何容易或难以线性分离？ | 流形半径、维度、相关性，Chung等PRX2018，Mamou等ICML2020 [R12–R13] | 在控制语义后的样本集合上区分类内变化、方向数和类间相关 | 流形分类容量等于语言模型知识容量 |
| 有效维度多大？ | PR、TwoNN、有限样本校正 [R17–R18] | 全局与类条件、局部尺度、样本量敏感性分开报告 | 一个数字就是语义真实维度 |
| 现有准确率是否已饱和？ | 控制任务、低样本Probe、MDL [R20–R21] | 测少量标注和未见模板下的学习曲线 | 更复杂读出有收益等于线性可分性改善 |
| SAE系数能识别什么概念？ | SAEBench的稀疏Probe [R04] | 单特征和固定少量特征预测独立语义标签 | 字典原子就是唯一语义单位 |
| 簇是否与标签一致？ | NMI/AMI机会校正 [R19] | 固定聚类流程，保留NMI并以AMI及随机参照补充 | NMI高就说明因果性、完整语义或专家价值 |
| 特征解释是否可靠？ | 随机模型解释对照、字典非规范性 [R08–R09] | 未训练检查点、随机投影、留出解释预测、跨种子匹配 | 几个高激活例子足以给特征命名 |
| 特征是否对指定输出有选择性作用？ | RAVEL，ACL2024 [R22] | 改一个属性，观察其他属性保持；只测底座原本会的任务 | 任意消融造成损失就证明语义对应 |

### 4.1 优先采用跨条件语义读出，而非继续只测IID domain分类

直觉：能用“integral”判断文本属于数学，不代表识别了与表述无关的关系。更强的测试是：在一种表述/词汇条件中学会读出关系，到了新的条件仍能读出。

以因果方向为例：

- “A causes B.”
- “B is caused by A.”
- “B causes A.”

前两句的关系相同但形式不同；第一、三句词汇接近但方向相反。实际数据需平衡主动被动、实体顺序、长度和关系词，防止新测试又退化成语法模板检测。

CCGP源自对跨实验条件抽象表示的研究。[R11] 在本项目的具体迁移，是把“条件”定义为语境、模板或实体词汇，预先留出条件，而不是随机留出一些同模板句子。

### 4.2 RSA把“更分开”改成“按照什么分开”

对相同样本得到表征距离矩阵：

$$D^h_{ij}=1-\cos(h_i,h_j).$$

另外构造语义关系、模板、词汇重合、长度等候选距离矩阵。比较这些矩阵与表征距离的对应，观察语义是否解释了不同于模板的部分。[R15]

建议先做匹配语义三元组的距离差，再把多因素RSA作为补充。不能把n条样本产生的n(n−1)/2对距离当成独立样本；置换或自助法必须以样本家族/文档为单位。若语义标签与模板高度共线，统计控制不能凭空识别语义，必须先改数据设计。

### 4.3 维度需要分尺度、分来源

全局参与比定义为：

$$d_{\rm PR}=\frac{(\sum_i\lambda_i)^2}{\sum_i\lambda_i^2},$$

其中lambda是中心化协方差特征值。它度量方差分散在多少方向，不直接度量拓扑维度或语义数量。类内PR、总体PR和局部PR应分开；如果只看类均值的协方差，C个类别本来就至多有C−1个独立均值差方向。

TwoNN用最近与次近邻距离比例估计局部内在维度，需要相应的采样与局部密度假设。[R17] ICLR2026的有限样本维度研究专门讨论PR估计的样本偏差，并给出校正方法。[R18]

你们的360/1,200个样本适合做受控的比较性诊断，但不能默认足以精确辨别30维和160维。尤其一个只有64个点的局部协方差，中心化后秩最多63；这种程序上限绝不是测得语义最多63维的证据。

### 4.4 类条件几何比总体Fisher更有解释力

在当前B/W之外，逐类看类均值距离、类内主要方向、方向是否共享、跨条件的类中心漂移。Mamou等把流形分析用于BERT、RoBERTa和GPT的语言表示，报告分离性与流形半径、维度及相关性共同变化。[R13]

不要把类内方差全部叫噪声：例如同一domain内的算法差异正可能是未来专家需要处理的因素。半径下降可能是消除模板干扰，也可能是损失细语义；必须结合细标签或语义对照。

## 5. “聚类＋NMI”怎样变成可靠实验？

### 5.1 先分清聚的是谁

激活矩阵Z的行是样本，列是SAE特征。

**聚样本行：**每条文本获得一个簇标签，可以与同一条文本的domain标签计算NMI/AMI。

**聚特征列：**每个特征获得一个组编号，但没有天然的一一对应domain真值。此时不能拿“特征组编号”和“文本domain标签”直接算NMI，因为对象数量和含义不一致。应该测试特征组的响应是否能预测语义、是否共享功能，或再把样本映射成组激活后进行另一次明确的样本聚类。

SAE本身只产生稀疏编码，并没有自动决定样本的唯一类别。

### 5.2 NMI保留，AMI作为主补充

NMI对聚类数量与偶然匹配敏感，因此跨方法要固定聚类数量，并报告机会校正后的AMI、ARI、簇大小，以及同样类别比例下的随机标签参照。[R19]

P面板可预先探索簇数Q∈{4,8,16}；N面板Q∈{8,16,32}。这里Q是簇数，与SAE的激活预算K不同。按每个Q完整报告，不能在报告集选出最佳Q当作最终结果。当前已经看过的报告集只承担探索用途。

聚类中心、预处理、活跃特征筛选和尺度缩放均只能用拟合集学习；在新数据上固定后分配簇。至少使用10个聚类随机种子区分算法随机性，另用结构保持的标签置换确定机会参照。

### 5.3 必须同时比较替代解释

比较原始h、SAE系数z、重构hat h及PCA表示的样本聚类。对相同聚类分别检查domain、模板/来源、长度等标签的对应。不同标签熵和粒度不同，AMI也不宜简单相减解释成“净语义分”。

若原始h和z都主要按模板聚类，换一个漂亮布局不能解决问题。若z只是在全连接非线性变换后让分类更容易，要把它归入读法改善，不自动归入主干改善。

## 6. “高激活词看起来有意义”怎样升级为语义对应？

### 6.1 从举例到预测

在探索集看高激活的完整上下文，写出可被反例推翻的描述；冻结描述后，预测该特征在未看过文本上会不会激活。检验集必须包含：同义而低词汇重合的正例、关键词相同但语义相反的负例、弱激活和不激活样本。

只看Top-20例子很容易忽略召回率。一项特征可能只抓住“带某关键词的物理文本”，遗漏大多数不带该词的物理文本。对极稀有特征，随机负例下高准确率也可能只来自多数类。因此报告精确率—召回率曲线、AP、正例基率、覆盖率和失败例。

自动解释模型给出的文字只用来生成候选解释，不作为标签真值。2026更新的随机Transformer对照研究表明，一些自动解释指标不能可靠地区分训练与随机模型，这要求加入随机/未训练对照。[R09]

### 6.2 单特征不好，不代表整个分组没有语义

对每个预定义语义分别比较1、4、16、64个特征的受限读出。这里q是探针允许使用的坐标数，不是每词元激活数K。特征筛选与正则强度选择必须限制在拟合和开发数据上。[R04]

若单特征差、少量特征组合好，允许结论是“分布式的可读语义”，不是单原子语义。若同一概念在不同随机种子下分裂成不同数量的特征，不应强迫一对一ID匹配。SAE特征不是已经确立的唯一规范分解。[R08]

### 6.3 特征组的几何分析

先用字典方向相似性或响应关系提出分组，再分析组的部分重构：

$$h_G=D_Gz_G.$$

检查其方向、有效维度、与独立语义变量的关系，并与同样组大小、活跃频率、贡献范数的随机分组比较。Engels等的工作提供了字典分组—部分重构—多维结构分析的范例。[R03]

注意：Top-K竞争会使相关特征不总是共激活；共激活不强不能排除共同概念。不同主干的解码向量也未必共享坐标意义；跨主干对应优先看同一文本上的响应关系，而非直接比较列编号。

## 7. 评测本身也需要校准

SAEBench提供了覆盖多个方面的评估框架，是本项目选题和组织实验的良好起点。[R04] 但2026年的《Are Sparse Autoencoder Benchmarks Reliable?》通过固定SAE重复评估、合成真值和训练轨迹审计，发现默认TPP/SCR存在可靠性或有效性问题；其他指标也可能难以区分小变体。[R05]

这篇预印本不能被解释成“所有SAE指标无效”。其合成生成假设、模型范围和把训练进展作为质量参照的部分，也有边界。对本项目更实用的结论是：

**先检验一把尺子能否区分已知真值、纯噪声和同模型重复，再让它裁定SAE方法。**

本轮不把默认TPP/SCR设成主要终点；稀疏Probe也不享有豁免，仍要比较原始表示上的强基线。Kantamneni等对数据稀缺、类别不均衡、标签噪声和分布变化进行了专门检验，未得到SAE相对强基线的稳定整体收益。[R10]

## 8. 方法修改应从什么结果出发？

| 观察到的失效 | 对应的候选改进 | 必须先排除 |
|---|---|---|
| K=32只对复杂样本损失大量可用信息 | 可变预算：BatchTopK或阈值式稀疏；先等平均L0比较 | 更大字典、编码器拟合不足、幅度差异 |
| 单原子不稳定，但小组包含稳定语义 | 多维特征组读出、分组路由 | 单纯增加分类器复杂度造成的收益 |
| 粗概念被细概念吞并 | Matryoshka的嵌套重构思路 [R06] | 真实标签层级与字典容量层级混淆 |
| 读出明显依赖先解释什么、再解释什么 | MP-SAE的条件性残差读取 [R07] | 普通非线性读出已同样有效 |
| 几何主要对应高方差模板因素 | 先改数据设计；必要时试尺度平衡/白化 [R24] | 白化放大噪声、改变损失权重而非语义 |
| 只改读法有益，主干没有稳定收益 | SAE保留为观察器/路由表示，不再默认正则主干 | 观察器训练预算是否公平 |
| 原始语义在跨条件测试中确实改善 | 再测选择性功能与持续学习 | 不把可读性直接当作模型实际使用 |

## 9. 推荐最小阅读顺序

1. R01：明确Top-K目标与推理时修改K的局限。阅读输出：用一句话区分“固定支持的秩”与“全局表示维度”。
2. R03：理解多维特征组。阅读输出：画出“一个概念用几个相关原子表达”的示意，不要求实现算法。
3. R04与R05配对：理解SAE评测种类及可靠性边界。阅读输出：为本项目选一个主要语义终点、一个竞争解释和一个随机对照。
4. R13与R11：把距离统计改成跨条件语义组织。阅读输出：写出一个同语义异表述正例和同词汇异语义负例。
5. 执行需要时再看R19（AMI）、R18（有限样本维度）、R21（MDL），不在第一天把全部指标都实现。

## 10. 文献索引与核验范围

以下编号对应正文。正式论文集页面核验用于发表信息；HTML正文用于相应方法描述。只依据摘要的前沿条目明确标出，没有据此复述具体实验数值。

### 稀疏编码与SAE评估

- **[R01] Gao et al. Scaling and evaluating sparse autoencoders. 2024预印本。** 核对HTML方法及修改推理K的讨论。用途：Top-K定义、稀疏—重构权衡、编码近似误差。不是当前主干正则有效性的证据。https://arxiv.org/html/2406.04093v1
- **[R02] Bussmann, Leask, Nanda. BatchTopK Sparse Autoencoders. 2024预印本。** 核对摘要和方法定位；可变单样本预算的候选。https://arxiv.org/abs/2412.06410
- **[R03] Engels et al. Not All Language Model Features Are One-Dimensionally Linear. ICLR2025。** 核对正文的特征分组、多维表示和干预方法；不能把少数已知周期概念推广成所有语义。https://arxiv.org/html/2405.14860v3
- **[R04] Karvonen et al. SAEBench: A Comprehensive Benchmark for Sparse Autoencoders in Language Model Interpretability. ICML2025。** 官方出版页与HTML评测定义；用于评测维度划分，不直接照搬所有默认指标。https://proceedings.mlr.press/v267/karvonen25a.html
- **[R05] Chanin. Are Sparse Autoencoder Benchmarks Reliable? 2026-05预印本。** 核对评测噪声、合成真值及训练轨迹分析与局限。https://arxiv.org/html/2605.18229v1
- **[R06] Bussmann et al. Learning Multi-Level Features with Matryoshka Sparse Autoencoders. ICML2025。** 官方出版信息、嵌套字典与吸收问题；不采用单项概念擦除分数证明当前LM改善。https://proceedings.mlr.press/v267/bussmann25a.html
- **[R07] Costa et al. From Flat to Hierarchical: Extracting Sparse Representations with Matching Pursuit. NeurIPS2025主会。** 核对官方摘要及方法定位：条件性、层级、非线性可访问特征。https://proceedings.neurips.cc/paper_files/paper/2025/hash/311bd32bcd952f93cf820bacd6955f0a-Abstract-Conference.html
- **[R08] Leask et al. Sparse Autoencoders Do Not Find Canonical Units of Analysis. ICLR2025。** 核对正式归属与摘要中的字典不完整、非原子性；不宣称它证明语义永远不可识别。https://arxiv.org/abs/2502.04878
- **[R09] Heap et al. Automated Interpretability Metrics Do Not Distinguish Trained and Random Transformers. arXiv v2，2026-01。** 核对当前版本题名和随机对照结论；与2025旧版题名区分。https://arxiv.org/abs/2501.17727v2
- **[R10] Kantamneni et al. Are Sparse Autoencoders Useful? A Case Study in Sparse Probing. 2025预印本。** 核对摘要中四种泛化困难设置及强基线结果；本调研不据此否定所有SAE用途。https://arxiv.org/abs/2502.16681

### 表征几何、维度与泛化

- **[R11] Bernardi et al. The Geometry of Abstraction in the Hippocampus and Prefrontal Cortex. Cell2020。** 核对摘要及CCGP的研究定位；迁移到文本的数据设计为AI建议。https://research.ibm.com/publications/the-geometry-of-abstraction-in-the-hippocampus-and-prefrontal-cortex
- **[R12] Chung, Lee, Sompolinsky. Classification and Geometry of General Perceptual Manifolds. Physical Review X，2018。** 核对理论摘要；“容量”是该设置中的流形分类容量。https://journals.aps.org/prx/abstract/10.1103/PhysRevX.8.031003
- **[R13] Mamou et al. Emergence of Separable Manifolds in Deep Language Representations. ICML2020。** 核对官方摘要；语言模型中的半径、维度、流形相关性分析。https://proceedings.mlr.press/v119/mamou20a.html
- **[R14] Kornblith et al. Similarity of Neural Network Representations Revisited. ICML2019。** CKA作为跨表示的相似性度量，而非好坏度量。https://proceedings.mlr.press/v97/kornblith19a.html
- **[R15] Kriegeskorte, Mur, Bandettini. Representational similarity analysis—connecting the branches of systems neuroscience. Frontiers2008。** 核对RSA的距离关系模型框架；文本语义/模板模型为迁移设计。https://doi.org/10.3389/neuro.06.004.2008
- **[R16] Walther et al. Reliability of dissimilarity measures for multi-voxel pattern analysis. NeuroImage2016。** 核对原论文摘要与结论；连续距离、噪声归一化及交叉验证距离。原实证场景是fMRI，不是当前语言模型。https://pubmed.ncbi.nlm.nih.gov/26707889/
- **[R17] Facco et al. Estimating the intrinsic dimension of datasets by a minimal neighborhood information. Scientific Reports2017。** TwoNN；估计依赖采样和尺度，不能按数字直接设置K。https://www.nature.com/articles/s41598-017-11873-y
- **[R18] Chun et al. Estimating Dimensionality of Neural Representations from Finite Samples. ICLR2026。** 核对正式归属及有限样本PR偏差校正；实现前需读终版估计器细节。https://proceedings.iclr.cc/paper_files/paper/2026/hash/9768645621c2cd6c5b851a06205b92cf-Abstract-Conference.html

### 聚类、读出和功能验证

- **[R19] Vinh, Epps, Bailey. Information Theoretic Measures for Clusterings Comparison: Variants, Properties, Normalization and Correction for Chance. JMLR2010。** 核对机会校正问题；本方案以AMI为主补充是具体方法选择。https://www.jmlr.org/beta/papers/v11/vinh10a.html
- **[R20] Hewitt, Liang. Designing and Interpreting Probes with Control Tasks. EMNLP2019。** 核对控制任务与选择性思想；本文的简单随机标签置换不是其全部控制任务设计。https://aclanthology.org/D19-1275/
- **[R21] Voita, Titov. Information-Theoretic Probing with Minimum Description Length. EMNLP2020。** MDL兼顾学习数据量与模型编码开销；不是直接估计表示的真实互信息。https://aclanthology.org/2020.emnlp-main.14/
- **[R22] Huang et al. RAVEL: Evaluating Interpretability Methods on Disentangling Language Model Representations. ACL2024。** 核对选择性改变属性并保持其他属性的任务框架；需要底座能回答相应问题。https://aclanthology.org/2024.acl-long.470/

### 可追踪，但不作为本轮主判断依据

- **[R23] Zaher et al. The Geometric Wall: Manifold Structure Predicts Layerwise Sparse Autoencoder Scaling Laws. 2026-05预印本。** 核对其几何量预测特定SAE尺度关系的定位。有限范围预测关联，不是不可逾越的几何上限证明。https://arxiv.org/abs/2605.09887
- **[R24] Saraswatula, Klindt. Data Whitening Improves Sparse Autoencoder Learning. 2025公开稿；arXiv页面注明AAAI2026 XAI4Science Workshop接收，非AAAI主会。** 依据摘要，作为尺度失配时的候选；不能默认白化保留所有任务信息或优于其他方式。https://arxiv.org/abs/2511.13981

## 11. 本轮允许的总判断

SAE旁支可以继续研究，但需要从“它没有破坏训练”转向“它究竟改变哪类结构，并让哪些语义更容易保留和读取”。这项判断应由新、独立的语义条件检验与稀疏预算曲线决定，而不是由更多候选指标中最漂亮的一项决定。

本轮文献研究完成；配套实验均未运行，也未修改仓库的正式Anchor或Protocol。
