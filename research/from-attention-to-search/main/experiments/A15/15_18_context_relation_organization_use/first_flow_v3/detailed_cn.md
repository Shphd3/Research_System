# Detailed：这轮关系分析怎样做、数值怎样追溯

[先读Summary](summary_cn.md) · [逐项解释附录](explanation_appendix_cn.md) · [English](detailed.md) · [冻结Protocol](protocol.md)

**本轮回答的是固定模型对关系题的行为、表示和替换响应。** 640道测试题答对329道，四格主交互为+0.024219 nat［−0.011719, 0.060937］。以下依次解释题目、评分、内部工具、有效性修复和证据路径；机制判断保持PENDING_RESEARCHER_REVIEW。本文件拥有方法与证据链，[附录](explanation_appendix_cn.md)保存E00–E10逐项A–F、全层长表、八个完整输入和两个贯穿案例。

## 1. 题目为什么是四格，而不是八格

把“甲在乙左边”画成甲指向乙的一条边，就得到一个可以由程序求解的关系图。每题有13个实体和12条事实，答案只有在查询方向或反方向可达时才被标注；不能确定时不强行标No。生成器逐条删去必要路径上的边，确认少一条便不能确定答案。

**C是必须用几条关系。** C=1时有直接证据；C=3时需要三条边连起来。例如真实题1416的必要事实是“Carol在Sam右边”“Carol在Mary左边”“Bob在Mary右边”，共同给出Sam→Carol→Mary→Bob，故问Sam是否在Bob左边，答案Yes。它们以原英文事实出现在12事实输入里；完整文本在[附录](explanation_appendix_cn.md)。C=1/3保持总事实数、实体出现次数和近似长度，仍会改变任务相关关系与干扰事实的构成。

**D是必要证据离答案前位置有多远。** 近远版重排同一事实集合，把包含查询端点相邻关系的固定五事实邻域移到前部或后部。以题1408/1410为例，事实和答案相同，必要事实末尾距查询由33变为103个token。全测试集C1近/远平均35.531250/106.193750，C3为33.327083/103.989583个token；长度155–161。重排还改变顺序，这是距离比较保留的混杂。

**F是训练暴露次数。** 既没有可追溯的关系曝光估计，也未实施受控训练，所以实际只形成C×D四格。附录八个输入中的高/低F是请求槽位，实际值全未知；词频和字典激活率不补这两个格。

每族有2C×2D×2关系方向×2表达，共16变体。128族共2048题，TRAIN/DEV/TEST为64/24/40族、1024/384/640题，模板集合分别0–3/4–5/6–7。族间重新抽实体及渲染分配，共用13节点链形；这是跨实体/模板留出，不是跨图形结构泛化。只看词袋的基线测试50.00%，首末事实实体角色/度数基线53.75%；这些对照检查指定捷径，不能穷尽所有策略。

数据来源和逐边证明见[数据与平衡](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/data/data_audit.json) · [完整题目](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/data/dataset.jsonl)；实际token位置见[token位置表](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E01/token_metadata.json)。所有合法困难题与错误预测均保留。

## 2. 从Yes/No概率到四格比较

在相同前缀后，分别读取单token候选` No`和` Yes`的条件对数概率，token ID为2308/7414。这里的概率来自完整词表，两个候选没有重新归一成总和为1。

**单题正确优势** = log p(正确候选) − log p(错误候选)。例如题1408真值Yes，两个原值No=−0.685887814、Yes=−1.310887814，优势−0.625；反转题1412真值No，No=−0.650239527、Yes=−1.400239468，优势+0.749999940。两题都选No，因此一对只有一题对。正负相抵会使条件平均优势靠近0，并不意味着单题两候选普遍同分。

**候选准确率**只看较大候选是否正确，同分按预定No优先；**反转成对正确率**要求同族同C/D/表达的一正一反都答对。真值各320个，实际611次No含40同分，整体329/640正确。四格成对正确率为7.50%、8.75%、2.50%、1.25%，分母与普通准确率不同。

**正确答案负对数似然（NLL）** = −log p(正确候选)。替换后减原生的NLL差为正，表示正确候选概率变小。由于完整词表中其他token也占概率，Yes和No可同时上升而彼此优势近乎不变；所以干预表同时报告margin与NLL。

先在同族各变体内平均，再对40个测试族等权。主比较为：

\[
I=(M_{3,far}-M_{3,near})-(M_{1,far}-M_{1,near}).
\]

这里M是正确优势的题族等权均值，I仍用nat。浅条件远减近−0.005469，深条件+0.018750，得到I=+0.024219、95%题族区间［−0.011719,0.060937］。2000次重采样抽整族、共同保持配对；不是抽640道独立题，也不是多个训练种子。没有预定实际意义门槛，这些为探索性估计。[逐题评分](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/per_row.jsonl) · [四格与配对统计](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/results.json) · [同分计数](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/tie_guard.json)

## 3. 具体保存了哪一列内部数字

模型在每个token、每层都有1024个数。**完整状态**在本轮专指某层结束时、某个位置的1024维输出；**层增量**是该位置输出减同层输入，以FP32相减。完整状态累积先前内容，增量记录这层数值改动。它们是两个不同的矩阵对象。

主要读取答案开始前末尾位置；另保存每条必要事实的末尾。题1408有155个token，查询索引154、必要证据末尾121。本轮不缓存155个位置全体，只存预定行；统一数组有4槽，C1的重复填充槽不重复计数。实际保存2048个查询位置、4096个证据末尾、全部28层。层号均从0计，15/27对应第16/28个block。另一个SAE接口读取末层归一化MLP输入，未与block输出混用。

完整状态回答“目前留下什么数值”，增量回答“这一层改了多少”；后续工具分别分析它们。[张量接口](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E00/interfaces.json) · [全部证据位置](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E03/all_evidence_norms.jsonl)

## 4. 几何工具各自量什么（E03、E04、E06）

### 配对距离：关系反转怎样改变状态

E03把同层同位置的两条向量逐项相减，计算平方和再开方的**欧氏距离**；单个向量的同样计算是**范数**，表示整体幅度。另将每条向量除以自身范数后重算距离/余弦，以检查差别是否仅是整体放大。

例如C1近条件在层0/13/27，完整状态平均范数为6.702474/38.302616/583.017944；反转距离为0.048744/1.611201/43.490314，单位范数后为0.007217/0.041760/0.074064。原始距离随幅度增长，归一化读数给出另一个参照。距离描述数值变化，不能把43.49解释成多少“语义差距”。全层与所有实际证据位置在[全层统计](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E03/layer_statistics.json)。

### PCA与SVD：很多题是否共享一些变化方向

E04把同hook、同查询位置的每题向量排成一行。**主成分分析（PCA）**在TRAIN上减平均状态，再寻找变化最大的正交方向；**奇异值分解（SVD）**提供这些方向及其强度。谱是平方奇异值按大小排列，能量是中心化数值平方和。测试题只投到已冻结方向上，不重新找方向。

各C/D训练矩阵均256行，合并矩阵1024行；完整状态和增量、原始与中心化谱分开保存。**熵有效秩**是把能量比例的熵取指数，量化等效方向数，受样本数限制，并非整数矩阵秩。层0/27完整状态有效秩5.803002/33.863758；同层前64 TRAIN方向保留TEST能量0.717169/0.718719。层27前16只保留0.478150，增量的相应值为0.475185。

训练方向能保留新题多少能量，比给每题单独取其自身方向更能回答“共享”；后者非零向量用1维即可保留100%，是代数构造。去均值或去第一方向只定义数值诊断。[谱和保留量](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E04/spectra.json) · [四格留出保留](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E04/condition_heldout_retention.json)

### CKA与子空间：不同层怎样排列同一批题

E06先在一层把同批题两两内积，形成样本×样本关系表，再用**中心化核对齐（CKA）**比较两层关系表：两表中心化后的内积除以各自长度。这样比较相同题之间的相对几何，不要求坐标一一对应。CKA中心化用于定义该统计，不用于拟合预测器或选层。

真实案例所在C1近条件的层13/14 CKA为0.995679；这个数属于整批160行，不是单题CKA。全层、四格、完整状态/增量及反转差向量共16张28×28矩阵均保留。另以TRAIN估计固定16维空间，报告投影重合、TEST保留与10次随机参考。等维控制排除“维数更大所以更相似”，但高CKA也不等于层功能相同或可删去。[全部CKA及子空间](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E06/results.json) · [四格子空间](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E06/condition_subspaces.json)

## 5. 线性读出：训练拟合与测试泛化一起看（E05）

读出器是从查询状态的1024个数预测Yes/No的小分类器；每层各拟合一套真实训练标签和一套打乱训练标签。先一起读训练、验证和测试，下面固定展示层0/13/27；全28层和区间在[附录](explanation_appendix_cn.md)。

| 层 | 训练交叉熵 | 验证交叉熵 | 真实标签测试准确率，% | 乱标签测试准确率，% |
|---|---|---|---|---|
| 0 | 0.122844 | 14.719437 | 48.750 | 49.219 |
| 13 | 0.109730 | 3.497388 | 51.406 | 48.906 |
| 27 | 0.132951 | 4.312807 | 51.719 | 49.531 |

交叉熵是按真实标签计算的平均负对数概率，越小表示读出器给真值的概率越高。训练列说明拟合已见题怎样，验证列用于选择正则强度；测试列才说明新题族、新模板上答对多少。乱标签列先打乱训练目标，测试仍对真值，用来参照同容量分类器的偶然表现。本轮训练损失低而验证损失高，真实与乱标签测试范围都约48%–52%。实例族与模板同时留出，当前对比不能单独定位是哪一种迁移造成。

具体计算是对1024维加权求和并加偏置，经sigmoid转成Yes概率；每头1025参数。这个概率属于外部分类器。输入标准化只用TRAIN，L2权重惩罚的0.001/0.01/0.1只由DEV交叉熵选择。所有候选最终在同一“二分类交叉熵＋λ×权重平方均值”目标上达到预定数值精度；这项合格与表中的测试泛化分别判断。求解器和梯度细节放在[第9节](#9-哪些有效性问题修复了哪些结果不再使用e00e10)。

最初测试值已经暴露，求解修复后仍按探索性报告。[全部拟合](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/probes.json) · [优化诊断](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/optimization_diagnostic.json) · [逐题读出](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/test_predictions.npz)

候选中间有向关系标签与最终反转标签重复，未另拟一个伪独立目标。E09只由最终DEV准确率选15/27层（两者0.513021，平分取早），不按TEST替换效果选层；它只规定后续观察位置。

## 6. 字典先重构，再看特征（E07）

**CrossCoder**用同一组稀疏代码重构多个指定层；A22有16384特征，联合读取从0计数的1/3/…/27共14层。加载其原TRAIN中心/尺度及已保存门阈值，不在这批题上重新调阈值。它是跨层联合编码，不能直接当成某一早层在线可用的局部特征。

重构解释方差比例**FVE**=1−重构平方误差/均值基准平方误差。A22相对其保存的TRAIN均值总体0.767563，之后统计12个split/C/D组的激活概率、幅度和真实高/低激活文本。激活概率是这些测量位置中代码大于0的比例，不是模型训练曝光。特征ID只在本字典内定位，未按编号命名common或关系机制。

**SAE稀疏自编码器**是另一份末层归一化MLP输入字典。它与模型父本匹配，但本任务相对任务TRAIN均值的FVE=−4.270350，说明其重构比该均值基准更差，特征解释标INVALID。两个FVE的基准不同，不能当成同对象排行榜。

字典替换对行为另用同组批16个DEV诊断输入逐层报告。没有独立合格的关系特征，所以特征级干预仍BLOCKED，未为补清单重训字典。[A22重构/行为](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E07/crosscoder_calibration.json) · [SAE资格](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E07/sae_calibration.json) · [真实特征例](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E07/crosscoder/representative_features.json)

## 7. 保留或移除方向后，模型怎样继续算（E08）

先在TRAIN估计均值μ与方向V，测试状态h替换为μ+VVᵀ(h−μ)，再让余下模型计算。均值恢复把平均偏置与变化方向分开。等秩随机方向检查任何同维压缩是否有相似后果；移除第一主方向检查单个最大方向。小幅版本为h+α(替换值−h)，α=0.1/0.5/1全部报告。

层0/7/13/20/27、保留1/16/64及去PC1，共105条件。受体是固定前10 TEST族、表达0、两C/D/反转的80题。下表完整列预定五层的rank16、幅度1例子；其他秩与幅度在逐项附录和原表，不是择优结果。

| 层 / 保留方向 | 状态相对误差 | 正确优势变化，nat（95%区间） | 正确答案NLL变化，nat（95%区间） |
|---|---|---|---|
| 0 / 主方向16 | 0.496554 | -0.012500 [-0.028125, 0.003125] | 0.005838 [-0.002286, 0.012744] |
| 0 / 随机16 | 0.979840 | 0.001563 [-0.015625, 0.020312] | -0.003124 [-0.013924, 0.005484] |
| 7 / 主方向16 | 0.655748 | 0.000000 [-0.015625, 0.017188] | -0.017109 [-0.025616, -0.008925] |
| 7 / 随机16 | 0.981591 | -0.001563 [-0.017188, 0.012500] | -0.008550 [-0.016621, -0.000975] |
| 13 / 主方向16 | 0.633884 | -0.010938 [-0.025000, 0.004687] | -0.002716 [-0.010596, 0.004785] |
| 13 / 随机16 | 0.990120 | -0.015625 [-0.031250, 0.000000] | 0.033574 [0.025914, 0.040972] |
| 20 / 主方向16 | 0.527372 | -0.003125 [-0.017227, 0.010938] | 0.007699 [-0.001692, 0.015920] |
| 20 / 随机16 | 0.988487 | -0.006250 [-0.029688, 0.017188] | -0.009713 [-0.032212, 0.011211] |
| 27 / 主方向16 | 0.637550 | ≈0 [-0.025000, 0.025000] | -0.048345 [-0.073902, -0.023194] |
| 27 / 随机16 | 0.984532 | -0.007812 [-0.034375, 0.018750] | -0.061420 [-0.097792, -0.028371] |

每行误差是条件内“替换差平方总和/原生中心化平方总和”，不是每题同一个真实误差。逐题文件另记录要求写入、实际BF16写入和舍入偏差。NLL差与margin差采用同一组批新取的原生参考；区间抽10个题族。高能量保留与答案变化分开报告，投影可能引入分布偏移。这里NLL只测正确答案，不是整段上下文的LM损失。[105条件](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E08/results.json) · [逐题状态误差](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E08/per_row_with_state_errors.jsonl) · [420行C/D结果](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E08/stratified_CD_results.json)

## 8. 用另一道题的状态替换（E09）

固定DEV选出的15/27层，分别替换答案前位置和第一条必要证据末尾。**供体**是提供状态的题，**受体**是继续被评分的题。self原值写回查操作本身；同关系改写查一般表达变化；相反关系供体查受体答案偏好是否向供体方向移动。双向是两种关系互换，不是训练重复。

相反供体保持实体、C/D、模板及长度/位置，160个配对位置全部严格匹配。80受体中原生正确40、错误40，均报告；以下是全部相反供体条件。

| 层 / 替换位置 | 正确优势变化，nat（95%区间） | 正确答案NLL变化，nat（95%区间） |
|---|---|---|
| 15 / 答案前 | -0.014063 [-0.032813, 0.007812] | 0.005648 [-0.007100, 0.015840] |
| 15 / 首条必要证据末尾 | -0.009375 [-0.031250, 0.010938] | 0.006041 [-0.003056, 0.015701] |
| 27 / 答案前 | -0.006250 [-0.050000, 0.034375] | 0.003125 [-0.017187, 0.025000] |
| 27 / 首条必要证据末尾 | 0.000000 [0.000000, 0.000000] | 0.000000 [0.000000, 0.000000] |

负正确优势变化表示向相反供体的答案偏好移动。层27证据末尾的0还受干预时点约束：替换的是最后block输出，后续只在各位置独立归一化/打分，没有下一层注意力把证据位置重新混入查询，因此该条件不构成“模型未使用证据”的检验。

原同关系跨模板供体只有4/160严格长度/位置匹配，保留为有混杂的探索记录。新增控制仅交换两条无关事实，按前向前第一个合格交换确定；80题均严格对齐。它保持关系但不是同幅度扰动，也不是词句改写。其查询位置平均正确优势变化在15/27层约0/+0.001562 nat。

完整状态可同时携带答案、实体和上下文；操作效应本身不定位是哪一种内容。正确/错误分组避免把修正一个错误预测包装为正确推理路径。[供体原表](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/results.json) · [原始对齐](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/donor_alignment.json) · [严格供体文本](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/strict_same_relation_donors.jsonl) · [严格逐题控制](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/strict_same_relation_per_row.jsonl) · [64行分层](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/stratified_CD_results.json)

## 9. 哪些有效性问题修复了，哪些结果不再使用（E00、E10）

| 问题 | 实际修复与保留 | 对读数的影响 |
|---|---|---|
| 平台新增字段无法解析 | 本轮目录内兼容代理过滤未知元数据；首次失败在创建作业前 | 环境、镜像、Reserved规格不变，失败收据保留 |
| NumPy整数无法写JSON | 转内置整数，保留失败源码/状态 | 首批算过但未成功落盘的值不补造 |
| 跨组批缓存原值重放差0.25 nat | 相关E08/E09及字典行为批次INVALID，改用完全相同组批的新原生状态/分数 | 最终所有选用no-op差0；原0.005nat分数/0.01nat优势容差未放宽 |
| AdamW波动、L-BFGS迭代上限 | 保存两份INVALID，固定目标与容量改Newton | 全候选数值合格；仍保留已看TEST的探索边界 |
| 读出修复改变DEV选层 | 24/2改为15/27，只重跑依赖的E09 | 旧层输出保留，不混入最终平均 |
| 原同关系供体位置混杂 | 原结果保留，另加严格事实顺序控制 | 新控制限于其实际改写方式，未冒称完全排除内容替代解释 |
| FP32/FP64减法要求过严 | 保存失败，按操作数和机器精度推导复核界 | 主对比独立重算差7.45e-10，未更改模型容差 |

读出求解保留完整修复链：原AdamW波动、首个有界L-BFGS达到迭代上限，两次结果均INVALID。最终双精度Newton使用目标的曲率矩阵求下降方向，再通过线搜索选择降低目标的步长。168候选和56所选头全部达到未变的“梯度最大分量≤1e-5”，所选最大8.67e-7；它检验拟合目标的数值精度，不是泛化证据。

原生参考必须与当前操作属于同一组批。例如题1408的E02初始优势为−0.625000，功能阶段重新取得的同组批原生优势约−0.750000；E08/E09只对各自当次参考求差，两个绝对值不能互换。

最初原生/只读误差0，阈值0.02nat；初始及最终同组批原值写回均0。主模型实际可训练参数0，完整前后参数哈希相同。独立256×1024双精度谱能量核对相对差1.17e-16。[追加修订](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/amendments.jsonl) · [最终无操作](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E00/functional_noop_replay.json) · [独立复算](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E10/independent_arithmetic.json)

## 10. 运行边界、完整覆盖和未运行训练

这是一个实验内的E00–E10清单，不是十一条新研究线。E00/E01/E10为DONE_VALID，E02–E09为DONE_EXPLORATORY；[覆盖账本](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/coverage.json)逐项保留证据、计数和缺口。F BLOCKED、SAE INVALID、中间目标重复、未合格特征干预均没有补成“完成”。正确/错误题、所有预定层和全部干预幅度保留。

实际拟合只有T1读出和T2统计；T3新字典、T4受控暴露训练、T5 common/remaining更新均未运行。后两项只做设计审计：T4的反向4:1三原子组合分配可匹配原子边际，但C1组合本身即原子，不能同时改其组合暴露又固定该原子暴露；T5尚缺操作定义。T1–T5各三轮审计，加两次数值修订，共21记录。

批准上限为两逻辑单H100 Reserved worker，各2小时、合计4 GPU小时、总墙钟3小时，20GiB产物上限。5个平台分配服务这两worker，最多并行2卡，运行时间合计0.2989GPU小时；含排队的保守分配上界0.6342，各worker均小于2小时，所有作业已结束。该值不是账单。CPU补充未用本地GPU。[完整作业证书](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/execution_certificate.json) · [21份拟合审计](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/protocols)

## 11. 从一句观察追到原始文件

| 观察/对象 | 原始记录与变换 | 如何核对 |
|---|---|---|
| 329/640、611次No、四格及主交互 | [原始logp](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/per_row.jsonl) → [题族统计](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/results.json) | row_id联接真值与两个logp，先族内平均，再复算四格差 |
| 全层距离、谱、CKA | [128个原始capture与日志](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/runs) → [距离](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E03/layer_statistics.json) / [谱](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E04/spectra.json) / [CKA](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E06/results.json) | 按同层/同位置/同row_id取向量，TRAIN拟合方向，TEST投影 |
| 所有线性读出与泛化 | [拟合状态](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/probe_states.pt) / [预测](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/test_predictions.npz) / [全部候选](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/optimization_all_candidates.json) | 1025参数头、TRAIN变换、DEV选择、TEST逐题预测与接受更新日志 |
| 105投影与12供体条件、严格控制 | [E08逐题](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E08/per_row.jsonl) / [E09逐题](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/per_row.jsonl) / [案例联接](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/case_traces.json) | 各阶段自己的同组批参考，不能拿旧缓存margin替换；保留C/D和正确/错误分组 |
| 资产、产物、全部修订 | [初始冻结](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/run_manifest.json) / [产物身份](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/artifact_manifest.json) / [修订](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/amendments.jsonl) | 源码/数据/拟合状态有身份哈希，大数组部分仅记录路径/大小，不声称全字节重验 |

输出资产族为`representation_context_relation_audit_v3_qwen06b_20261022`；实际参数、tokenizer及字典身份由[输入身份](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E00/resolved_input_identity.json) · [输出资产](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/output_asset_manifest.json)记录。原始数组、拟合头、TensorBoard、运行日志和图片留执行侧；本记录通过清单定位它们，不复制进Git。

本次可读性修订把旧Summary完整留作同记录附录，旧四文件的逐字节备份和SHA256保存在[排版前备份清单](/data/250010109/MoE_Router/research_record_archives/20261022_readability/A15_18_pre_readability_manifest.json)。未改变Protocol、数据、模型、阈值或任何科学状态。理解本文后，再按需要核对附录；研究者先陈述观察，AI机制判断随后。
