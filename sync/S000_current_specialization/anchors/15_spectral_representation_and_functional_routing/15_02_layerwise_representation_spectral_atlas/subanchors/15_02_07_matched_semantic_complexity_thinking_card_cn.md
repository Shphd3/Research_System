---
thinking_card_id: 15_02_07_matched_semantic_complexity
status: researcher_direction_confirmed_anchor_draft_requested
human_language: zh
formalization_authorized: draft_for_review
execution_authorized: false
---

# Thinking Card：匹配语义复杂度在逐层 MLP 参数谱中的位置

> 本卡整理研究者 2026-08-08 在会议总结、后续讨论和 H1 图片中明确表达的判断。研究者已要求写出完整 Anchor 与数据构造图供下一轮审核；尚未批准 Protocol、实现或执行。

## 我的判断

- **具体现象：**越深层的 attention 写入可能越能区分更细或更组合的目标。初步实验应逐层画出各本地 MLP 参数方向上的语义类别间方差曲线，纵轴使用 `log10` scale，横轴按每层自身参数增益从大到小排列。每层的方向不同，只比较本地 rank 次序，不把相同 rank 当作同一向量。
- **机制猜想：**此前 residual 已携带较简单或共同的信息；本层 attention 写入可能增加更细或更组合目标的可访问性。如果这种新增区别在深层相对分配到更后的本地 MLP 参数秩，那么复杂目标相对简单目标的归一化谱秩重心应随深度增加。该位置变化应与 H2 的“本层写入确实增加复杂目标可分性”并行检验。
- **最强替代解释：**所有语义对象都随层深共同右移，观察结果来自层级整体尺度、RMSNorm/参数增益或本地坐标变化，而不是复杂目标特异的新增信息。旧粗/细 taxonomy 的类别层级、类中心数量、每中心样本量和 within-class 定义不同，也可能机械制造差异；简单目标若在写入前已接近读满，其较小 `Disc` 增量还可能只是天花板效应。
- **最不确定的一环：**如何构造在类别数、熵、样本数、中心估计精度、文本分布、query 目标角色和读出位置上公平可比的简单/复杂对象；以及 `Disc` 应如何定义，才能区分“几何位置改变”与“本层新增可访问性”。
- **什么证据会改变判断：**若在匹配数据上，复杂相对简单的本地参数秩重心没有正的晚层增量，或本层 attention 写入没有带来复杂目标相对简单目标的 held-out `Disc` 增量，则当前联合机制不成立。若只有谱右移而没有 `Disc` 增量，只保留几何重分配；若只有 `Disc` 增量而没有右移，则放弃简单的参数谱后移解释。
- **当前唯一决策：**审核一个完整 Anchor：把 conditional-fine taxonomy 与真正的单一 composition 作为两个独立数据分支，冻结参数谱、逐方向方差曲线、rank-shift 主统计量和 H2 `Disc` 定义，再决定是否进入 Protocol。

## AI 审核

- **唯一未定义对象或隐藏假设：**“细粒度”与“组合关系”不是同一语义对象，不能合并统计。一大类与唯一小类一一对应时两个标签完全混淆，不能估计层级效应。raw post-`o_proj` 写入位于 residual 坐标，而 MLP 参数谱位于 RMSNorm 后的输入坐标；主判断应使用 attention 引起的实际 MLP 输入增量，raw 写入只作坐标匹配后的辅助图。
- **最小反例或区分实验：**在同一批匹配样本上分别构造简单和复杂标签，计算复杂减简单的逐层本地参数秩重心差；同时用同一固定容量读出比较 attention 写入前后的 held-out 交叉熵改善，并按写入前剩余交叉熵做天花板敏感性检查。共享右移会被复杂减简单抵消，纯几何变化会被 H2 `Disc` 门识别，简单任务提前饱和则不能伪装成复杂特异增量。
- **AI 建议：**pursue design review。先审核两个数据分支与指标，不直接复用旧粗/细 estimator，也不启动 Router 或训练实验。

## 我的确认

- **保留或修改后的判断：**保留 H1“深度—语义精细化”，并把它拆为参数谱位置 H1 与新增可访问性 H2；conditional-fine 与真正 composition 分开裁定。
- **是否允许写入正式 anchor：**允许写出完整 draft 供审核；不批准 Protocol、implementation、smoke 或 full run。
