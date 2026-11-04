派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/preflight_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/preflight_cn.md)；研究修改仍回到原件。

---

# R01 准备记录：来源、原生缓存与旧图资格

本记录确认新设计的可行性，不包含新的 H1/H2 估计。按 2026-10-28 请求中
“先构建 Anchor Protocol，然后分析”的顺序，本次交付完成第一阶段；后续三类图
与句子案例尚未产生。

## 已核查什么

已定位两条指定对话，读取影响本轮决定的内容，并与当前科研 owner 对照。
[来源核查](provenance/conversation_sources.md)说明实际阅读范围。新问题把观察单位
从固定目标位置的响应，换成一句话中的两个位置，因此独立归属 A15_28；A15_27 不改写。

本次八个所需登记资产的严格访问检查全部通过。[回执](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/provenance/input_access_20261028.json)
证明所选文件可读；[资产审计](provenance/asset_sources.md)另记录生产者身份绑定、
实际稀疏缓存核查与小文件 hash。没有声称重新哈希大模型权重或执行新的模型前向。

| 对象 | 当前核实事实 | 对本轮的作用 |
|---|---|---|
| 已有数学／生物文本 | 各 60 篇，共 120 个 canonical URL 文档组，每篇 192 token | 可复用 23,040 个缓存位置；完整句资格会减少实际分析量 |
| 原生 SAE | E16，block27 MLP 输入，30,000 坐标；FP32 Top32 正激活；120 份逐 token 缓存可读 | H1 可做；不能套用 CrossCoder 编号 |
| 原生 CrossCoder | A22，16,384 坐标；14 层 residual-post 联合共享 z，使用已保存归一化与门槛 | H1 及兼容旧图 H2 可做；不是 14 次独立层激活 |
| 活跃数量 | SAE 恒 32；CC 为 29–637，均值 295.4366 | 必须匹配数量，并报告后位置实际活跃数 |
| 独立频率参考 | DCLM 256 窗、65,536 位置、254 文档组；与研究文本 URL/WARC/全文 hash 交集均为 0 | 复用 R05 频率组；尚不能排除所有未知近重复 |
| 句界 | 没有保存句子 ID | 成对结果揭示前，先只看文本冻结完整句标注 |
| 先前暴露 | 每领域 30 discovery、10 development、20 heldout 文档均已经旧轮分析 | 不能称为新的未触碰确认集 |

R05 的频率组沿用“至少 20 次 DCLM 激活，再按频率三分位划分，并列不拆开”；
不足 20 次另列低支持组。它是已用的操作定义，不是本轮由统计功效推导的新阈值。
准确切点和代码在资产审计中，不能从数学／生物面板重估频率组。

## 旧图究竟表示什么

兼容的 CrossCoder 图使用完整 16,384 坐标空间。建议主图固定为 `raw_edges.npz`
的 `A -> u`，只保留 `passV=True`，共 206,136 条边。孤立节点仍属于图的坐标空间；
没有准入边与编号根本不在图中是两种情况。

旧准入规则在**同一 token**上统计：前后节点各至少 200 次，联合至少 20 次；
P(目标|源) 至少 0.8，P(源|目标) 至多 0.5，目标频率至少是源的两倍。
DeltaP 和 lift 虽被保存，却不参与准入。所以高频目标自身的基频就可能产生较大条件概率。

图中自环和双向边均为零。每条边都使正频率至少翻倍，数学上已排除有向环；
本次审计没有删环。没有独立定义的语义层级。旧约简图中的最长路径深度只是图统计，
不是语义高度。约简图与原始图的一跳覆盖不同，不能看结果后切换。

最大入度 15,439，最大出度 91。因此 Protocol 纳入保入度／出度的随机基线；
随机图只称随机基线，不替代旧图。同 token 的条件概率也不能称跨 token 传递概率。

## 分支阻塞与剩余准备

旧 E17 SAE 图采用 BF16 编码、FP16 保存、norm 异常过滤，并按所选索引计数，
不一定等于正值次数。它与 R04 原生 FP32 正激活接口的等价性尚未合格，历史父模型
与来源绑定也有缺口。**SAE H2 为 `INCOMPATIBLE_INTERFACE_UNQUALIFIED`。**
SAE H1 与 CrossCoder 两项读数可继续。不重建替代图。

后续先切句，再在固定规则下做不读取成对结果的匹配覆盖率审计。必须区分真正缺少
同 ID 伙伴，与文档配对、位置分箱、活跃数范围造成的损失。不能把便利阈值称为统计
功效依据，也不能看到结果后放松匹配。

## 执行与交付状态

新增模型前向 0；训练 0；聚类 0；重建替代旧图 0；新 H1/H2 成对估计 NOT RUN。
[机器可读审计](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/provenance/asset_preflight.json)保留本次核实事实。完整统计脚本、
输出表、三类图和真实案例属于之后的分析阶段，本记录没有把它们写成已完成结果。

[一页入口](one_page_cn.md) · [Protocol](protocol_cn.md) · [论文方法说明](literature_methods_cn.md)。
