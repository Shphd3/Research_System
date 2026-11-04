派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_28_sentence_feature_continuation/15_28_sentence_feature_continuation_anchor_cn.md`。
[精确原始文件](../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_28_sentence_feature_continuation/15_28_sentence_feature_continuation_anchor_cn.md)；研究修改仍回到原件。

---

# A15_28：句内 feature 延续与旧图关联

## 1. 问题定义

在同一句数学或生物文本中，前面 token 的 feature，后面是否仍然激活，或通过
旧图与不同的后续活跃 feature 相连，并且超过可比的无关位置？研究者于
2026-10-28 固定了这个问题。[Focus](../../../focus/focus_sentence_feature_continuation_cn.md)
持有本轮问题；[Protocol](../../../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/protocol_cn.md)
给出具体分析规则的草案。

这是 A15 下独立的跨 token 坐标延续问题。A15_27 研究的是改变前缀后，固定目标
位置如何响应，原问题、证据和状态保留。复用其文本，不代表旧领域读出、Attention
关联或语义响应结果已经回答了本轮问题。当前要分清：看似延续的现象，是否仅由
高频、词面重复、领域背景和活跃集合大小造成。

超过对照支持有界的序列关联，值得继续检查；非正差异削弱当前测量下的延续主张；
匹配不足或区间过宽仍是未决。之后由研究者决定是否对某个模式做上下文干预。
本轮使用已有缓存，不训练、不聚类，不新增大规模前向或干预。

## 2. 物理先验

1. **研究者假设：** feature 可能沿句子继续出现，也可能变化。不要求后面 token
   包含前面所有 feature。
2. **测量假设：** 某字典在其原生接口上的正激活定义活跃坐标。某个坐标不激活，
   不等于完整模型表征里已无相关信息。
3. **比较假设：** 同领域、不同文档中匹配 token ID、位置和活跃数量的位置可作为
   背景，但不能保证句法、主题和语义角色可交换；这些残余混杂仍需保留。

## 3. 可证伪假设

**H1：** 前位置活跃集合在同句后位置仍然活跃的比例，高于匹配的无关位置对照。

**H2：** 当前位置的某个 feature 到后面不再激活时，它仍通过旧图非自环边连接到
后位置活跃 feature 的比例，高于对照。正向、反向分别计算。用“已经消失的前位置
feature”作为替换读数的分母，是对研究者“即便相同 feature 不再出现”条款的
**AI 建议形式化**；同时保留全部前位置 feature 的非自环关联覆盖。

最强竞争解释是高频 feature 普遍出现、token ID 重复、同领域／主题共同激活、
每位置活跃数量不同，以及少数高连接度节点造成覆盖。只在高频或同 ID 条件成立时，
优先采用这些较窄的解释。同坐标延续和图关联可以同时存在，均不自动说明因果传递。

## 4. 数学模型

先固定一套字典，其坐标全集记为 \(\mathcal F\)。位置 \(i\) 上 feature \(f\) 的原生激活为 \(z_{if}\)，
活跃集合为 \(A_i=\{f:z_{if}>0\}\)。同一完整句子里，前后位置满足
\(i<j\)，距离为 \(d=j-i\)；\(E\) 是旧图的有向、非自环边集。

统一读数是：指定的前位置集合中，有多少成员通过指定关系在后位置找到对应成员。

\[
C_R(B,A_j)=\frac{1}{|B|}\sum_{f\in B}
\mathbf{1}\{\exists g\in A_j:(f,g)\in R\}.
\]

每个位置对得到一个 0 到 1 的比例。H1 令 \(B=A_i\)，关系 \(R=\{(f,f):f\in\mathcal F\}\) 只允许
相同编号，得到 \(S_{ij}=|A_i\cap A_j|/|A_i|\)。H2 的替换读数建议令
\(B=A_i\setminus A_j\)，关系使用 \(E\) 或全部反向边。另报
\(C_E(A_i,A_j)\) 及反向的全部前集合关联；它们允许与延续重叠。
分母为空记 NA，不记零。频率分组先限制前集合 \(B\)，再计算各组比例；
不把所有更早位置不断取并集。

每个领域、字典、频率组、距离和 token ID 状态下，关键量是按文档汇总后的
真实值减匹配对照值 \(\Delta_R\)。具体权重、匹配覆盖率和文档间依赖处理先在
Protocol 固定。每个比较同时报告 \(|A_i|\)、\(|A_j|\)、已消失前成员数和
未匹配数量。公式定义的是描述性观察量，不是信息传输模型。

旧 CrossCoder 箭头的观察单位不同：**同一 token** 上，\(A\to B\) 通过
计数支持和非对称条件共现门槛。原规则要求 \(P(B\mid A)\ge0.8\)、
\(P(A\mid B)\le0.5\)、\(n_B\ge2n_A\)。旧输出保存了基频校正诊断量，
但校正量不参与边准入。本轮将旧边用于跨 token 覆盖，是新观察量；不能把原条件
概率读成跨位置转移概率。

## 5. 计算实现

| 目标 | 怎么做 | 为什么 |
|---|---|---|
| 保持坐标身份 | 分别使用 E16 的 block-27 MLP 输入 SAE，以及 A22 在 14 个 residual-post 接口联合编码的原生共享 z | 两字典相同编号不是同一对象；共享 z 不是每层独立激活 |
| 确定真实句内位置对 | 复用 120 篇数学／生物前缀缓存，先根据文本标注并冻结完整句界 | 同文档或 Attention 两端不必处于同一句 |
| 分开延续和关联 | 计算相同坐标比例、已消失前成员的图覆盖、全部前成员的图覆盖，保留完整分母 | 自环或重复坐标不能充当替换证据 |
| 区分竞争解释 | 匹配同领域不同文档位置；拆分同／异 ID、空白标点；沿用 DCLM 频率组，采用保激活边际和保图度数的随机基线 | 高频坐标、后集合稠密和图中的高连接度节点都能制造高覆盖 |
| 理解实际句子 | 展示所有 token，固定 feature 展示规则，报告未展示数量，并给两个真实例子和一个反例 | 少数好看的热图不能证明总体假设 |

当前核查确认了两字典 H1 与 CrossCoder 旧图 H2 的输入可行性。SAE H2 状态是
`INCOMPATIBLE_INTERFACE_UNQUALIFIED`：旧图使用另一套精度／过滤与所选索引计数
接口，本缓存使用 FP32 原生正激活。不能套用 CrossCoder 图，也不临时重建 SAE
图作为替代。身份与证据见[准备记录](../../../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/preflight_cn.md)。

*Towards Monosemanticity* 的[有限状态自动机讨论](https://transformer-circuits.pub/2023/monosemantic-features/index.html#phenomenology-fsa)
提供序列层面的启发：同一 feature 可以持续出现，不同 feature 也可以交替。
**本轮改编：** 沿完整句子检查延续与变化。**证据边界：** 原文关于 feature
影响输出、输出 token 再触发后续 feature 的功能链，没有被我们的缓存共现测量检验。
论文里随字典规模变化的 feature splitting 也不定义句内语义升级。
[方法阅读说明](../../../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/literature_methods_cn.md)
区分原论文证据与本轮建议。

## 6. 最小证伪检查

一个缓存实验检验两种联系。H1 比较同坐标延续与匹配无关位置。H2 把仍保留的前成员
从替换分母中去掉，分别比较正、反向非自环覆盖。保边际随机化和图度数随机基线检验
频率、活跃数量与连接度是否足以解释观察。

**AI 建议判定：** 在登记的多重比较处理之后，真实减对照的区间严格高于零，且
相应随机基线诊断合格，才支持该合格分层中的额外联系。区间全部不大于零不支持
正向超额；跨零、匹配失败、随机化混合不足或图不可用均记证据不足。
零只是方向性零假设，不是由统计功效推导的实用阈值。目前未指定最小有意义效应，
因此统计可区分本身不决定科学或功能价值。具体参数与审阅台账由仍为草案的 Protocol 持有。

## 7. 当前证据

以下为初始设计核查快照；本节末尾链接当前执行结果。

已读两条指定对话及当前 owner。其来源与先前范围见[来源核查](../../../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/provenance/conversation_sources.md)，
它们还没有回答新的 H1/H2。

当前资产核查得到 120 篇文档，每篇缓存 192 个 token，共 23,040 个位置，两字典均有
原生稀疏激活。SAE 每位置活跃 32 个坐标；CrossCoder 为 29–637 个。独立 DCLM
频率参考含 65,536 个位置、254 个文档组。CrossCoder 旧图验证通过的原始边共有
206,136 条，最大入度为 15,439，因此高连接度控制是必要环节。旧图无环是频率倍增
准入规则的结果，并不建立独立的语义层级。

句子 ID 尚未标注。文本已被旧轮分析读取，不能称作新鲜确认集。
**本轮 H1/H2、三类结果图和新的“两例一反例”选择均为 NOT RUN。** 当前终点是
按请求完成设计和可行性核查。

**执行状态更新（2026-10-28）：** 上述 NOT RUN 为设计阶段快照，现仅就执行状态被本条取代。已完成两字典 H1、CC H2、冻结对照、随机基线及三类图；SAE H2 仍单独受阻。结果事实与有界 AI 解读由 [Summary](../../../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/summary_cn.md) 和 [Detailed](../../../experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/detailed_cn.md) 持有；不以运行完成替代研究者机制接受或问题关闭。

## 8. 边界与下一决定

同坐标超额支持句内坐标延续；没有同坐标延续但旧边覆盖超额，与关联坐标替换相容。
只在高频或重复词面条件成立，优先解释为公共模式或词面延续。背景校正后消失，
不支持当前测量下的额外联系，但不能据此断言遗忘。部分句子的结果只适用于相应条件。

本轮不能证明前文信息完整保留、因果传递、语义层级、簇形成原因或专家效用。
机制接受与问题关闭仍为 `Unknown`。

**唯一下一决定：** 三类图、真实案例、完整覆盖率表和区间交付后，由研究者判断
某个具体模式是否值得后续上下文替换干预。恢复时先审阅精确 Protocol，冻结只看
文本的句界，再开展已限定范围的缓存分析。A15_27 原有记录保持原义。
