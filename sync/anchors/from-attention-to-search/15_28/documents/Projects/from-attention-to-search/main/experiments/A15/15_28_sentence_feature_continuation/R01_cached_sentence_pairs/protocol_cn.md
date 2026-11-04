派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/protocol_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/protocol_cn.md)；研究修改仍回到原件。

---

# Protocol：A15_28 R01 缓存句内位置对

## 0. 审批快照

- 文档状态：统计实现方案为 `APPROVED_FOR_BOUNDED_CACHE_ANALYSIS`；新 H1/H2 测量为 `NOT RUN`。
- 研究者已固定目的：“一句话中，前面 token 激活的 feature，到后面是继续出现、换成关联 feature，还是不再出现？”
- 已授权范围：核对既有对话、研究记录、文本、原生活跃缓存和旧图；构建新的 Anchor/Protocol；在缓存范围内分析，不训练、不重新聚类、不新增大规模前向、不做功能干预。本次按“先构建设计，然后分析”交付设计与可行性，不重复请求总体缓存分析授权。
- 待方法审阅：下文的丢失源 feature 分母、切句与位置对资格、匹配、加权、随机基线、区间与判定参数标为 `AI_PROPOSAL`（AI 建议），不冒充研究者已确认的精确方法。后续分析前需解决影响解释的方法选择并冻结实现；工程 seed 本身不构成新的科学批准门槛。
- [Focus](../../../../focus/focus_sentence_feature_continuation_cn.md)；[Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_28_sentence_feature_continuation/15_28_sentence_feature_continuation_anchor_cn.md)；[English](protocol.md)。
- 实验角色：坐标延续与旧图关联的操作化／代理量检验。一个实验含三步：核对句子与缓存坐标；比较相同 feature 延续；比较旧图关联并阅读具体例子。
- 最小配置：既有 120 篇数学／生物文档前缀、原生 E16 SAE 与 A22 CrossCoder 缓存、固定 DCLM 频率参考、旧 A22 复核通过的原始边图。SAE 的 H2 因旧图接口未兼容而单独受阻。
- 改变项：后位置来自同一句，还是配对的同领域无关文档。固定项：前位置激活、字典、领域、匹配后的后 token ID／类别、位置分层与后位置活跃数范围。这是观察性匹配，不是随机上下文干预。
- 支持：合格真实减对照差值的同时区间高于零，且背景／连接度随机基线诊断相容。不支持：区间整体不高于零。不足：区间跨零、匹配／分母／区间无法估计、必要随机基线未合格，或图身份不合格。
- 不可声称：前文信息完整保留、因果传递、语义层级、簇形成原因或功能收益。尚未指定最小有用效应，统计分离不自动等于有用。

## 1. 术语与定义

**token 位置**是一个已缓存 192-token 前缀中的偏移。**完整句子**是经文本审核、起止都能在前缀中确定的跨度；文档或前缀不自动是一句。**feature**是某套固定字典和激活接口的一个坐标；两套字典的相同编号不代表同一个 feature。

固定字典后，原生活跃值记为 \(z_{if}\)，活跃集合为 \(A_i=\{f:z_{if}>0\}\)。同一完整句中前后位置满足 \(i<j\)，距离 \(d=j-i\)。固定 DCLM 频率组为 \(F_b\)，源组 \(B_i=A_i\cap F_b\)。源组为空时记 NA，不记零。每位置 L0 指非零活跃坐标数，即 L0(i)=|A_i|；它是成员数量，不是激活强度。

旧图 \(E\) 是有向非自环边集。A22 图的节点全集为全部 16,384 个编号，包括孤立节点。源 feature 在某方向没有边，应得到真实的零覆盖；这与“该 feature 不在图声明的节点全集中”不同，后者意味着图测量不合格。

**T1**：跨配对文档、后 token ID 精确匹配。**T2**：仅匹配词面类别及前后 token ID 相等状态的后备分层，不控制确切后词面。**文档块**：固定配对的两个不同 canonical 文档。**随机基线**：保留指定边际量的随机参照，不是替换科学图或新字典。

## 2. 与 Anchor 对齐

| 分析步骤 | 对应对象／竞争解释 | 如何计算及目的 | 证据角色 |
| --- | --- | --- | --- |
| 核对文本与坐标 | 原生活跃、完整句子、文档单位 | 绑定身份；逐句做文本盲审；冻结频组和文档配对 | 缺项只停止依赖该项的测量 |
| 相同坐标延续 | H1；频率、词面、领域、活跃数 | 计算源归一化交集，对比 T1/T2 和保边际随机基线 | 只支持相应条件下句内坐标重复 |
| 旧图关联与例子 | H2；图 hub、丢失分母选择 | 正／反向丢失源覆盖、全源诊断、连接度随机基线和三类图 | 与关联坐标替换相容，不等于语义抽象 |

不改变 A15_27 结果或 A15_25 图定义。已有响应、分类和 Attention 结果不代替新估计量。

## 3. 待检验假设

H1：同句前后位置的相同 feature 延续比例高于可比无关位置。H2：即便前 feature 不再激活，后活跃集合仍比对照更多地沿旧图与它相连。正反方向分开。两者都不预设后 token 包含全部前文。

H2 的精确“丢失源 feature”分母是对“即便相同 feature 不再出现”的 `AI_PROPOSAL` 形式化；全源非自环覆盖另作次要量。H1 与 H2 可以同时成立。

## 4. 竞争解释

| 竞争解释 | 对照／诊断 | 仍存边界 |
| --- | --- | --- |
| 高频 feature 到处出现 | 独立 DCLM 固定频组；保每 feature 次数和每位置活跃数的随机基线 | 有限参考频率不是普遍真频率 |
| 重复词面 | 同／不同 ID 分开；T1 精确匹配后 ID | ID 不匹配句法、词义或多 token 短语 |
| 同领域话题／文风 | 同领域不同文档；报告 genre／host 构成 | 话题、来源和话语角色仍可能不同 |
| 活跃集合大小不同 | 源位置固定；后 L0 范围；更窄敏感性；报告两端 L0 | 条件化 L0 会限制可解释人群 |
| 高连接度节点 | 全节点度表；保入度／出度的有向图随机基线 | 保留节点级度—频率关系，但不保留全部图模体或边端点频率配对 |
| 丢失源集合随后位置改变 | 两侧丢失比例／分母；共同丢失集合诊断 | 主 H2 是条件关联，不是因果替换效应 |
| 匹配筛选损失 | 全部合格真实对与匹配对分别报告；排除原因完整 | 匹配结果仅适用于有支持的部分 |

## 5. 数据构建与来源

**已核实来源。** 复用 `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/`（下称 R04 根目录）。`data/documents.jsonl` 有数学、生物各 60 篇，每篇一个 192-token 前缀。每领域原 split 为 discovery 30、development 10、heldout 20；三者均已暴露，保留标签但不称新鲜确认集。本轮描述性分析使用全部 120 篇，不新增任务人群。数据含 URL／文档组、WARC ID、来源行／全文 hash、源字符范围、原文、token IDs、领域及 split。

输入资产 ID：

1. `model_qwen3_0p6b_base`、`model_qwen3_0p6b_base_official_a5`（父模型身份）。
2. `tokenizer_qwen3_0p6b_base_official_a5`。
3. `sae_qwen3_0p6b_e16_layer27_final_1b`。
4. `crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013`。
5. `data_a15_27_r04_domain_native_dual_20261027`。
6. `analysis_a15_27_r04_native_sae_joint_cc_domain_20261027`。
7. `analysis_crosscoder_feature_relation_phase1_20261013t173130z`。

第一项含两个 ID，合计八个。当前严格访问与字段检查见 [preflight](preflight_cn.md)。访问通过不是新批准或本轮重新计算权重 hash。逐 token 文件为 `forward/documents/<seq_id>.npz`，字段为 `token_ids` 及各字典 `ptr/ids/z`。`documents_SAE.npz`／`documents_CC.npz` 的聚合只覆盖位置 32:192，不能替代完整 token 缓存。

**AI 建议切句规则。** 用登记 tokenizer 编码原样前缀，要求 token IDs 完全一致，获得字符偏移。初始句末为 `. ? !` 后接闭引号／括号及空白或文本末尾；保护小数点、姓名首字母以及固定缩写表 `e.g., i.e., etc., vs., Dr., Mr., Mrs., Prof., Fig., Eq., No., U.S., U.K.`。段落、标题和公式块触发审核，不自动成为句子。文本审核者在不看活跃和成对结果的条件下审核全部候选，记录合并／拆分理由及 complete／fragment／ambiguous。统计前冻结 manifest、hash 和 token-to-sentence 表。模糊跨度按文本排除，不能按激活挑选。首末截断片段排除；位于前缀边缘但完整的句子，仅在源字符边界或既有来源上下文能证明完整时收入。来源边界不可读则记 Unknown 并排除该片段。完整保留文本和排除数。

合格对为同一完整句内全部 \(i<j\)。不累积所有前位置的并集。距离组（AI 建议）：1；2–3；4–7；8–15；16–31；32–63；64+，只使用真实句内距离。

按解码词面给 token 分类：special ID；纯空白；含 Unicode 字母或数字（lexical）；去空白后纯标点；other。词前空格不使 lexical token 变为纯空白。位置对按优先顺序分 any-special、any-whitespace、any-punctuation、any-other、both-lexical。special 对不进入主统计但计数；其他非 lexical 条件单列。在每类内区分前后相同／不同 token ID。含数字 lexical token 保留并另报数量，不从编号推断语义。

**沿用频组。** 复用 R05 `analyze_A.py:60–62` 的 `groups(k)` 和 R04 `forward/reference_{SAE,CC}.npz`：hits 为各窗口次数和，rate=hits/65,536。hits≥20 的 feature 按 rate 的 1/3、2/3 分位数分组，ties 不拆开（≤下界为低、≤上界为中，其余高）；低于 20 单列 `low_support`。20 次是继承的参考支持规则，不是新功效阈值。256 个参考窗口对应 254 个 canonical URL 组，与 120 文档的 URL／WARC／源全文 hash 无已观察交集；不能排除全部未知近重复。

## 6. 学习任务与允许的信息

不引入训练任务、拟合目标、优化器、字典训练或聚类。输入是已有文本元数据、原生正激活、固定参考计数和旧边；输出是确定的位置对测量、对照分配、条件区间及说明图。

切句盲审与领域标签是标注，不是机制真值。结果不得影响切句资格、匹配门槛、图选择、频率切点或主检验族。不读封存 TEST，不采集新语料，不前向，不做上下文替换；如实记录既有暴露。

## 7. 模型、架构与固定版本

SAE：E16、F30000、零起始 block27 MLP 输入、原生 FP32 ReLU Top32。CrossCoder：final A22、F16384、blocks1,3,…,27 residual-post 的联合共享 z，原生 BF16 GEMM、保存的 TRAIN 中心／向量 RMS 和 score 阈值 0.051281172782182693。不切分 encoder 分支。共享 z 不等于各层独立激活。热图可显示 z 或原生 decoder 贡献，但须注明；统计仅用二值 z>0。

A22 旧图：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/graphs/raw_edges.npz`。固定 `A[passV] -> u[passV]`，共 206,136 条复核通过原始边、全部 16,384 个节点。`passV` 区分大小写。无自环；保存原 hash 与方向，不看覆盖结果再选择 reduced 图。

旧 A→B 在**同 token**上要求 nA,nB≥200、nAB≥20、P(B|A)≥0.8、P(A|B)≤0.5、nB≥2nA。DeltaP／lift 仅是诊断，不参与准入。每条箭头使频率至少加倍，所以无环和无双向边来自建图规则。旧 reduced 图删去可经更长路径到达的直接边；它保可达性，但改变“一条边”覆盖。本轮不用它作主图。深度和度不是语义层级，不画语义层级图。

SAE H2 为 `INCOMPATIBLE_INTERFACE_UNQUALIFIED`：历史 E17 是 BF16 编码、FP16 导出、norm 过滤及被选索引计数；R04 是 FP32 正激活。不得借用 CC 编号或重建 SAE 图替代，只停止 SAE 图分支。

## 8. 训练目标与优化

不适用：训练步数零，无拟合参数、优化器状态。观测量是源归一化比例及观察性匹配差值。切句规则、随机化配置是分析参数，不是学习出的模型参数。

## 9. 条件、随机种子与 checkpoint

本节及第 10–15 节新增数字选择均为待方法审阅的 `AI_PROPOSAL`。建议基础 seed=20261028；文档配对、匹配 tie、block bootstrap、incidence null、graph null 分别用偏移 +0、+1、+2、+3、+4，记录生成器名称／版本与实际 seed；不得用进程相关 Python hash。

条件：真实句内对、T1 精确 ID 对照、T2 后备对照、更窄 L0 的 T1 子集、保边际 incidence null、CC 保有向度 graph null。同一字典各指标尽量共享冻结位置对与匹配，空分母另处理。checkpoint 仅供身份绑定，不需加载权重。

**固定文档块。** 在各领域内先按全文 hash、再按 seq_id 排序，用冻结 seed 打乱，邻接两篇组成一块。每领域 60 篇得到 30 块。每篇均可作源，只能用其配对文档供给无关后位置。不用同文档后备，不跨块借 donor。完整报告这种限制造成的支持损失；这不等于整个语料没有同 ID。

**后位置匹配。** 对真实 `(i,j)` 固定 i，在配对文档的完整句合格位置 j' 中搜索。T1 要求 ID(j')=ID(j)，句内相对位置十分位相同 `min(9,floor(10*r/L))`（r 句内零起始，L 为句长），前缀位置四分位相同 `floor(position/48)`，后 L0 比在 [0.8,1.25]。若真实后 L0=0，只匹配 0。按 L0 绝对差、句内相对位置绝对差、前缀位置绝对差、dictionary/source-seq/i/j/donor-seq/j'/seed 的 SHA256 依次排序取一个。块内可重复使用 donor 位置，必须计数并在块推断中保留依赖。

无 T1 才进入 T2：保留位置／L0 规则，以相同 token 词面类别和 `ID(i)==ID(j')` 与 `ID(i)==ID(j)` 状态一致替代精确后 ID。只报告 T1 未匹配人群中的 T2，不把二者合并为已排除词面的证据。相同 ID 条件中 equality 本身已固定后 ID，T2 可能不增加支持。不按结果放宽规则。更窄敏感性仅保留已选 T1 匹配中 L0 比在 [0.9,1.1] 的对，不重新匹配以追回结果。

## 10. 主指标与冻结分析

对源频组 \(B_i=A_i\cap F_b\)，相同 feature 延续为

\[
S_{ij,b}=\frac{|B_i\cap A_j|}{|B_i|}.
\]

丢失源集合为 \(D_{ij,b}=B_i\setminus A_j\)，替换覆盖为

\[
G^{\to}_{ij,b}=\frac{\sum_{f\in D_{ij,b}}\mathbf1\{\exists g\in A_j:g\ne f,(f,g)\in E\}}{|D_{ij,b}|},\qquad
G^{\leftarrow}_{ij,b}=\frac{\sum_{f\in D_{ij,b}}\mathbf1\{\exists g\in A_j:g\ne f,(g,f)\in E\}}{|D_{ij,b}|}.
\]

每个源 feature 最多计一次，不按可达后 feature 数累加。空分母为 NA。对 j' 同样计算。H2 的真实和对照各用自身丢失集合，两侧非空才组成配对差值。两边丢失成员可能不同，因此这是条件覆盖比较；必须报告两边丢失数／比例及第 11 节共同丢失诊断，不声称逐坐标因果替换。

对任一 M，在相同有效匹配对 mask 上计算 \(M_{ij,b}-M_{ij',b}\)。依次聚合：句内同 cell 的位置对等权；源文档内句子等权；固定双文档块内有贡献的文档等权；同领域 cell 内文档块等权。报告每块由一篇还是两篇贡献。全部真实对的均值只作描述，不进入匹配差值；按源 feature 数加权的比例仅次要。

主 cell：T1、both-lexical；数学／生物分开；H1 分 SAE／CC，H2 只 CC 且正反方向分开；低中高源频率；7 距离组；同／不同 ID。完整登记 336 个可能 cell，不可删掉不可用 cell 以改善多重比较。`low_support`、全部频率、标点／空白／other、T2、更窄 caliper 皆为诊断，不挽救主结果；每个分层保留自身分母。

**AI 建议区间。** 在各领域内重采样整个双文档块，5000 次；字典、指标和 cell 共用同批抽到的 block 索引，匹配及块内依赖不变。对每个可估 cell，用 block 均值的样本标准误 SE，以及 bootstrap 的 `(重采样均值-原均值)/原SE`；每次对预登记可估主 cell 取绝对值最大值，其 95% 分位 q 给同时双侧区间 `均值±q*SE`。这是条件于现有支持的近似 block-bootstrap 带，不是精确随机实验区间或新鲜确认。至少两块、有限正 SE 是此形式的数学要求，不是功效资格。若某 cell 的任一次重采样没有有效贡献，区间标不可用，不丢掉坏 draw 或重跑直到成功；报告块数、缺失 draw 与稳定性。小值／零值不证明有用等价。次要曲线用明确标注的逐点 95% block-bootstrap 区间，不作确认判定。

结果解封后，不可静默改变估计量、mask、频组、图、聚合、主 family 或区间算法。变更需带日期 amendment，并将受影响证据标为新的探索性分析。

## 11. 次指标与有效性检查

另报以 \(|B_i|\) 为分母的全源非自环覆盖，正反分开，不与丢失源量混淆。报告两端 L0、丢失数、拥有边的源 feature 支持、孤立节点、空分母及含数字 token 构成。A22 节点全集覆盖为 100%；“源是否有边”的覆盖是另一数量，不能偷换主分母。

共同丢失敏感性在两条件均使用 \(B_i\setminus(A_j\cup A_{j'})\)，为空则 NA。它暴露条件各自丢失集合造成的差异，不能替换主量。若主量与共同丢失诊断方向相反，或后者没有支持，必须保留丢失集合组成变化这个未解决解释；主量为正不能单独叫稳定替换，共同丢失量为正也不能救失败的主量。更窄 L0 子集同样只是诊断。

**保边际 incidence 基线（AI 建议）。** 对每字典／领域，在全部被接受句子的 token 上形成位置×feature 二值矩阵。均匀抽两条既存 incidence `(r,f),(s,g)`；r≠s、f≠g 且交叉 incidence `(r,g),(s,f)` 不存在时，用交叉边替换，否则保留状态。这是 checkerboard switch，精确保每行 L0 和每 feature 总次数，词面、句子结构和匹配位置不变。不重阈值或重新采激活。建议两个独立 seeded chain，各自 burn-in=5×nnz 次尝试，此后间隔 ceil(nnz/10) 次尝试，每链保存 199 个 draw，合计 398；每次验证边际。记录接受率、原边 overlap、预先固定整体 overlap／coverage 探针的自相关及链间差异。尝试数不能保证充分混合。建议诊断：接受率<0.001、burn-in 原边 overlap 不下降，或任一固定探针的两链均值差大于合并 draw 标准差的 2 倍，标 `MIXING_UNQUALIFIED`。报告有限 draw 包络，不称精确置换 p 值。此基线破坏词面／序列组织，仅检验边际背景，不能代替 T1。

**连接度基线（AI 建议，仅 CC）。** 固定全部 16,384 节点及活跃矩阵，均匀选有向边 `(a,b),(c,d)`，仅当 a≠c、b≠d，且两条新增 `(a,d),(c,b)` 互异、非自环、不同于原边且当前图中不存在时替换，否则保留状态。精确保每节点入度／出度和总边数，每个 draw 验证。两个 chain，各 199 draw、合计 398，每链 burn-in=5×边数，间隔 ceil(边数/10) 次尝试，记录同样的接受率／原边 overlap／链间诊断。随机图允许有环；要求原 DAG 会改变这个度条件 null。它们仅是人工度参照，不是“新建旧图”；真实旧图字节不改。节点身份／频率与每节点入出度固定，所以该 null 完整保留节点级度—频率关系；它不保留同一条边两端的频率配对、频率倍增／DAG 条件、条件共激活规则或全部图模体。

每个 null draw 使用冻结位置对／匹配和相同句子→文档→块权重重新计算真实量、对照量与差值，不重选匹配。每个 cell／指标先固定真实观察的合格匹配对 mask，incidence H2 每 draw／条件只在该 mask 上重算丢失集合。若任一必要位置对分母变空，或必要 cell／block 值无法定义，则该 cell-null 的包络推断记 `UNAVAILABLE`，完整记录 draw／pair／block 数；不静默删 pair、不把 NA 变零、不只合并有效 draw、不重新匹配。可另存明确标注“支持发生改变”的纯描述性诊断，但不能用于更强解释。完全可定义且两个 chain 诊断均合格的 cell-null，才合并每链 199、共 398 个 draw 形成包络。包络本身不构成有效假设检验 p 值。要进一步声称超出频率／活跃数和图度背景，观测真实减 T1 差值需高于相应固定 null 差值的 97.5% 分位且诊断合格；仍保留这些诊断包络在多个 cell 上的限制。null 失败只阻止更强解释，不阻止报告匹配事实。

## 12. 已知正例、反例与易混淆例

真实 pair 测量前仅用手造小数组检验实现：Ai={1,2}、Aj={2,3}，延续=1/2；空源 NA。E={(1,3)} 时丢失集合{1}的正向覆盖=1、反向=0；自环不能贡献。孤立丢失节点覆盖=0，不是 NA。没有丢失成员时，即使延续=1，丢失覆盖也为 NA。源频率组先限定分母。

测试完整重复 token 句、不同 ID 等支持行、缩写／小数片段、单 token 句、hub 目标、图方向交换、全零行。所有随机交换须精确保边际／度，非法提案不改变状态。用不等位置对／句子数、重复 donor 和只有一篇贡献的块检查聚合。这些是实现检查，不是新科学发现。

## 13. 科学流程与阶段合同

| 阶段 | 目标／输入 | 如何做、为何做 | 输出／失败处理 |
| --- | --- | --- | --- |
| 1 身份与文本冻结 | 原生缓存、原文、旧图 | 刷新资产访问；token 对齐；全部切句文本盲审；在结果前冻结频组、配对、规则和 hash | 句子 manifest／来源回执／不可变 config；身份缺失只停对应分支，模糊句记原因排除 |
| 2 实现与匹配 | 已冻结文本／坐标 | 先做第 12 节小例；在不读延续／覆盖结果前构建 T1/T2／窄 L0 mask，统计支持损失 | 匹配表、校准回执；无匹配只使对应 cell 不足，不设任意全局样本门槛 |
| 3 统计与交付 | 固定 pair／match | H1、兼容 H2、block 区间及固定 null；三类图与例子 | 完整可用／不可用 cell、一页总结与证据；null 混合失败限制解释，不增前向或重建图 |

Preflight 只做设计与来源资格，不是 H1/H2 观察。本轮完成 draft 和可行性。后续方法审阅可在已授权缓存范围内接受／修正具体选择，不产生训练或新远程运行权限。

## 14. 算法、输出与来源合同

后续实现放在执行侧 `/data/250010109/MoE_Router/experiments/20261028_sentence_feature_continuation/R01_cached_sentence_pairs/`。拟议脚本：`prepare_sentence_pairs.py`（文本／缓存／匹配）、`analyze_cached_pairs.py`（统计／null／区间）、`render_figures.py`、`audit_results.py`。这是计划名称，不表示已有脚本或结果。小源码／config／来源随本 Protocol 保存。

冻结资产 IDs、实际输入／digest、原 producer 证据、Protocol／Anchor hash、scientific config、代码 revision／dirty 文件、Python／包版本和随机流。保存全部拒绝原因、交换尝试／接受数、match 重用、分母和核查。身份不一致具名停止相关计算，不重新生成缺失激活。

AI 建议工程上限：本地 CPU、最多 4 worker threads、峰值 16GiB RAM、4h 墙钟、5GiB 新输出。这不是已测 ETA。到上限保存部分回执，未完成 null／cell 记 NOT RUN，不加资源或静默减少随机化。实际统计前需用合成实现检查支持在该上限内完成的可信估计。

完整输出：来源／冻结 manifest；全部句子／token 表；全部 pair／match／排除；pair／句子／文档／块级指标；完整主／次表；null 摘要与诊断；图和准确绘图数据；完整脚本／config；audit；双语 Summary、Detailed，缺项明确。原始数组留执行侧，进入研究 Git 的小证据须 payload manifest；只登记实际生成的可复用资产。

仅三类图：

1. **句内热图**：显示所有 token，默认颜色是二值活跃；若显示贡献则注明原生缩放，不跨字典直接比较未标准化幅值。每字典最多 24 个 feature，按句内活跃位置数降序、原生 z 和降序、ID 升序选取。注明全部活跃并集数、未显示 feature 数及每 token 未显示活跃数。长句连续分面，不能丢 token。作为上下文展示的片段单独阴影且不进入统计。
2. **延续—距离图**：真实与 T1 两条线，频组分面；旁列源／后支持、区间与匹配率。同／不同 ID 及非 lexical 条件分开；逐点曲线区间与同时差值判定区分标注。
3. **旧边覆盖—距离图**：CC 丢失源覆盖真实与 T1，正反分开；全源／null 作为附表或插图，不偷换主量。附真实句子的旧边连线图，解释旧箭头的同 token 含义。SAE 图分支注明 unavailable。

**固定例子规则（AI 建议）。** 在至少有一个 both-lexical、不同 ID 的 T1 匹配对的句子中，数学选择全频率 SAE identity 差值最大的一句；生物选择全频率 CC 正向丢失源差值最大的一句。按句内位置对等权均值排序，tie 用全文 hash、句起点。这是有意选取的说明例，不是代表性或独立证据。反例从另一个文档、identity／正向／反向 CC 均可估的句子中，最小化这三种差值的最大值；最大值≤0 才称测得的“额外关联非正”反例；这是对超出对照联系的反例，不等于原始延续为零。必须同时报告 raw S，仅在 raw S 确为零时才能称完全无延续。若没有符合者，明确未找到并展示最弱例，不能编造反例。两条正例规则若选出的量也非正，称最大观测／弱例，不称支持例。尽量同文显示两套字典，附完整真实文本／token 边界，用文字说明延续、变化和缺失。连线图只画被显示 feature 的旧边，同时报被省略的合格源／端点数。保存全部候选分数及选择记录。

## 15. 支持、不支持与证据不足

| 结果 | 认识更新 | 边界 |
| --- | --- | --- |
| H1 同时区间下界>0，对照／null 合格 | 相应条件下句内坐标延续 | 非完整信息保留或因果传递 |
| H1 弱／未定，H2 下界>0，图与度控制合格 | 与关联坐标替换相容 | 非抽象、语义升级或已证状态机 |
| 仅高频／同 ID 成立 | 优先公共模式／词面延续解释 | 不推广到低频或非重复词 |
| 同时区间上界≤0 | 当前测量／人群不支持正额外联系 | 不代表忘记前文或其他表征无效应 |
| 区间跨零，分母／匹配／区间不足，或 null 不合格 | 报告不足和未排除解释 | 非负机制结论 |
| 仅部分领域／距离／句子成立 | 报告条件和例外 | 非所有后 token 包含前 token |

零是方向性 null，不是有功效依据的有用效应阈值。不加“每类 64 文档”等任意资格门槛，不逐结果调门槛。每领域最多 30 双文档块，实际支持可更少。分别报告真实样本稀少与 paired donor、位置分层、ID、L0、指标分母造成的规则性损失。

## 16. 不能得出的结论

本轮不能证明前文信息完整保留、因果信息传递、语义父子关系、随 token 位置提升的语义层级、CrossCoder 各层独立激活、簇形成、专家学习收益或功能重要性。匹配不能除尽上下文混杂。已暴露文档支持条件描述，不是新的独立确认。某 SAE／CC 坐标不再出现不等于模型忘记前文。

## 17. 分块确认、冻结与变更记录

| 块 | 状态 | 来源／待解决项 |
| --- | --- | --- |
| A 问题和边界 | CONFIRMED | 本次 prompt 固定目的、H1/H2、竞争解释与边界 |
| B 数据和来源 | PROPOSED | 复用范围已确认；精确切句、全部 120 暴露人群和文档配对待方法审阅 |
| C 任务与监督 | CONFIRMED | 缓存统计；不训练、聚类、新增大规模前向或干预 |
| D 模型和架构 | PROPOSED | VERIFIED_SOURCE：producer 原生身份已核实；CC V-passed raw 主图与 SAE H2 受阻已具体验明供审阅 |
| E 优化 | CONFIRMED | NOT_APPLICABLE：无优化器或模型拟合 |
| F 比较与判定 | PROPOSED | 丢失源估计量、匹配、权重、同时区间、null 诊断与阈值 |
| G 复现与范围 | PROPOSED | 缓存范围已授权；具体工程配置与后续代码／冻结待完成 |

跨块一致性：完成 draft 自审与独立冷读，已修正 null 支持变化、图度不变量和例子选择，未提升状态；研究者尚未逐项确认 AI 新增统计参数。科学验收／关闭为 Unknown。`design_frozen_at`、实现／config hash 待记录；本 Protocol 作者未打开新 H1/H2 结果。

后续执行前解决影响解释的方法选择、确认适用块、通过精确实现合成检查，并冻结文本／配置／代码／来源。沿用既有缓存范围授权，不借流程发明新的缺失批准。是否进行上下文替换由研究者之后单独决定。

首次授权成对统计后保留本文科学正文。实质变更仅追加 amendment：前值／后值、理由、已可见结果、受影响 cell／块、授权和证据资格影响。可以追加执行回执／结果链接，不重写规则。本文不授权 commit、push 或对外发布。


### Execution activation 2026-10-28 / 本轮执行确认

The researcher explicitly instructed execution of the explained cached analysis, the three figure types and real math/biology examples, with real-minus-control distance contrasts and unchanged matching thresholds. This instruction confirms the applicable A–G choices for this bounded run; the original proposal labels above remain historical provenance, not a pending repeat approval. No new forward, training, clustering, intervention, or publication is authorized. Synthetic implementation checks and text-only sentence review remain required before scientific outcomes. Report order: question and feature organization, bounded conclusion/recognition update, then result analysis. Scientific mechanism acceptance and closure remain Unknown.

确认时间 UTC: 2026-10-28T07:28:16.344858+00:00。本次用户指令为“就按照这个思路开始做缓存分析……匹配不足的地方如实报告，不要为了得到结论调整门槛”。A–G 适用选择由本次执行确认承接；后续实施细化和冻结见执行侧 config/manifest。原草案表中的 PROPOSED 为修订前历史，不是再次索要许可。


### Execution completion and numerical audit / 执行完成与数值核对 — 2026-10-28T08:25:19.210589+00:00

The bounded cached analysis is complete. Its original scientific body and proposal history above are preserved as the pre-execution contract; the NOT RUN snapshot is superseded for execution status only. Two native H1 branches and CC H2 were measured; SAE H2 remains interface-blocked. Five null jobs completed 398 draws each. See [Summary](summary.md), [中文结果](summary_cn.md), and [Detailed](detailed.md). Human mechanism acceptance and question closure remain Unknown.

Postprocessing correction: observed and null contrasts now use the same frozen sparse weighting operator for the registered strict-envelope comparison. Different floating-point reductions previously produced false H2 excesses of about 10^-18; the two affected comparisons are exactly equal to the graph-null 97.5% envelope under the identical operator. No thresholds, masks, bins, graph, weights, seeds or draw counts changed. The pre-correction provisional verdicts are INELIGIBLE and retained execution-side. [Audit trace](provenance/aggregation_consistency_fix.md).

本次完成缓存统计与三类图，研究者判断仍待确认。共同消失集合诊断、低覆盖及随机空分母均保留；无新训练、前向、聚类、干预或发布。原冻结 Protocol 的字节副本及 hash 保存在执行侧 provenance/frozen_protocol.md。
