---
thinking_card_id: 15_02_05_balanced_taxonomy_attention_write_atlas
status: researcher_statements_compiled_ai_proposals_pending_confirmation
human_language: zh
formalization_authorized: draft_only
execution_authorized: false
---

# Thinking Card：平衡三级 taxonomy 在 attention write 中的层深与谱位置

> 本卡整理研究者截至 2026-08-07 已明确表达的判断。凡标注“AI 提案”的内容都等待研究者确认，不能作为已批准结论或执行授权。

## 我的判断（研究者原意整理）

- **具体现象：**当前先搁置组合关系长短程问题，回到粗粒度、细粒度和更细粒度的 taxonomy 区分；使用冻结 Qwen3-8B，比较各层 `o_proj` 前的 32 头拼接 attention 输出与 `o_proj` 后、残差相加前的 isolated attention write。
- **机制猜想：**更深层可能更能刻画更细、更复杂的语义区分；如果更细语义是较条件化的变化，其语义方差相对位置可能在晚层落到本层 DCLM activation-covariance 谱的更大 rank，而不要求绝对方差峰离开 head。
- **最强替代解释：**粗、细、更细层级的类别数、每类样本数、类中心估计精度、协方差最大秩、词频、模板和语义距离不同，足以产生表面层深或谱位置差异；晚层也可能只是普遍提高可读性而没有发生谱秩重分配。
- **最不确定的一环：**如何让三级语义方差在同一个估计尺度上可比，以及如何把“数据谱位置”与 `o_proj` 参数矩阵方向的确定性重标度分开。
- **什么证据会改变判断：**尚待研究者确认。**AI 提案：**若同一批 hidden states 在平衡三级树、等数量二元对比、等类中心样本数、跨模板可靠性和独立 DCLM basis 守卫下，post-`o_proj` 的更细相对粗层级仍没有正的晚层谱秩重心增量，则当前“更细语义在晚层相对右移”命题失败；若只有强度上升而谱位置不变，则只保留“晚层更可读”。
- **当前唯一决策：**审核并修正本卡、正式 Anchor 与 `DRAFT_NOT_EXECUTABLE` Protocol；在 A--G 区块和跨区块一致性全部确认前不实现、不运行。

## AI 审核提案

- **保留的核心判断：**研究对象是每层本地 activation data spectrum；跨层比较的是归一化 rank percentile，不是追踪同一 eigenvector。
- **统计修正：**所有层级复用完全相同的 512 条文本状态；每个层级以父节点内二元兄弟对比为基本单位。主分析每级都使用 8 个对比、每个子节点都使用相同数量的样本；全节点估计只作次要结果。
- **尺度修正：**语义强度使用跨模板可复现的二元对比方差，并统一除以同一 leaf 内表达噪声；谱位置先归一化为层内 rank 分布，再计算 rank centroid。强度未过门时不解释位置。
- **参数方向图：**对每层 `o_proj` 做 SVD，分别画 pre 激活在右奇异方向、post 激活在对应左奇异方向上的方差。该图回答 `o_proj` 怎样重标度已有能量；它不替代 DCLM data-covariance 谱，也不能证明 `o_proj` 创造语义。
- **AI 建议：**pursue design review；暂不执行。

## 我的确认（待填写）

- 保留或修改后的判断：
- 是否确认“更细相对粗的晚层本地谱秩重分配”为唯一主命题：
- 是否确认 8 个平衡 taxonomy root family、每条路径二叉分支的数据骨架：
  确定
- 是否确认主表征为 full pre-`o_proj` concat 与 isolated post-`o_proj` write：
  确定
- 是否允许将 Anchor 从 draft 提升为 confirmed：
  暂不确定
- 是否批准 implementation / smoke / full run（可分开）：

