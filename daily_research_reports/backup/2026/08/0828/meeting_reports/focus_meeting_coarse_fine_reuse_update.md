# 从粗—细方向关系到父类条件化架构：0826 组会认识更新

```text
type: meeting_knowledge_update
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
scope: one_problem
cycle_source: 2026-08-26 group meeting
evidence_completed: 2026-08-28
```

**来源：**[0826 会议记录](../../0826/docs/0826会议记录.md)、
[A15_09 粗—细几何 Summary](../../../Projects/from-attention-to-search/main/experiments/A15/15_09_layerwise_coarse_fine_reuse_geometry/A15_09_E01_qwen3_30b_cross_depth_coarse_fine_reuse/summary.md)、
[A15_10 跨父类功能 Summary](../../../Projects/from-attention-to-search/main/experiments/A15/15_10_cross_parent_fine_function_transfer/A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer/summary.md)。

## 1. 会议主题与一个核心问题

0826 组会真正要回答的是：**真实世界的粗—细语义层级，是否在模型表征中形成
一套可以从父类逐级复用到子类的方向结构，从而支持树状 MoE？**

当前最稳妥的认识是：在 C4/C5、mathematics/physics 和六个固定层上，层级语义
并没有表现为“一组公共坐标从粗到细逐级复用”。父类条件细类空间与共同粗类
空间几何上基本分离；mathematics 与 physics 的细类空间也没有表现为可复现的
功能互换。与此同时，细类标签从共同粗类空间和置换得到的七维空间中仍然常常
可读，说明原生完整表征存在强冗余：**能读出来，不等于该空间是任务真正选择的
方向，更不等于 Router 应该共享它。**

这使架构判断从“按 PCA 或公共粗方向切空间”推进为一个更具体的候选：保留原生
完整表征，用正确父类条件调用局部 fine Router。但这仍只是最相容的候选，不是
已验证的架构结论。

## 2. 递进问题链

### 问题一：粗类信息是否就是 PCA 的大方差方向？

**直接回答：不是。**组会前实验已经显示，区分 mathematics 与 physics 的方向
主要在谱的中后部，PCA 头部更多承载公共、句法或表面变化。

**证据边界：**这否定了“最大方差等于粗语义”的简单对应，但谱位置相近并不表示
粗类与细类使用同一方向。因此必须直接比较判别空间，而不能继续用 PCA 序号代理
语义层级。

### 问题二：父类条件细类空间是否大量复用共同粗类空间？

**直接回答：没有观察到正向超出 null 的复用。**A15_09 的 24/24 个空间都能在
独立切分中稳定复现，但实际粗—细重合全部低于匹配标签置换的中位数；经验稳定性
校正量只有 0.0596--0.1445。

**能到达的结论：**fine 不是 shared coarse 的简单弱版本，`shared coarse space`
不能作为细粒度 Router 的默认几何前提。

**不能到达：**低重合不证明 coarse 补空间足够，也不证明删除 coarse 无害。组会
中“删界后 loss 变差”的失败仍然有效，所以不能把低重合重新解释成删方向方案。

![粗类与条件细类空间的直接比较](../../../Projects/from-attention-to-search/main/experiments/A15/15_09_layerwise_coarse_fine_reuse_geometry/A15_09_E01_qwen3_30b_cross_depth_coarse_fine_reuse/figures/figure1_raw_overlap_with_baselines.png)

### 问题三：即便几何不同，不同父类的 fine 空间是否仍能互换功能？

**直接回答：没有建立可复现互换。**在严格匹配目标训练数据、目标标签、七维输入、
分类头、正则化选择和测试流程后，18 个合格方向的相对功能保留量 RR 为
0.0339--0.1810，中位数 0.0743。24 个方向中只有 C5 Block 36 的
mathematics→physics 超过完整流程置换 null；它没有在 C4 复现，同层反向又不
合格。因此六层没有一层满足“双方向、双面板”规则。

**能到达的结论：**mathematics 与 physics 的 named fine Fisher spaces 不是一组
稳定可互换的公共 fine 坐标；强 `shared fine space` 假设不受支持。

**不能到达：**Cross、共同粗类和置换空间的细类准确率本身都很高，所以不能说
细类信息只存在于父类自己的七维空间。当前结果是“目标自己的方向更有效率，而
其他指定方向没有超过匹配冗余基线”，不是“其他方向没有信息”。

![跨父类细类功能的匹配比较](../../../Projects/from-attention-to-search/main/experiments/A15/15_10_cross_parent_fine_function_transfer/A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer/figures/figure1_functional_transfer_ladder.png)

### 问题四：这些结果怎样改变架构选择？

现在不应再从 PCA 方差、几何重合或高线性准确率直接指定 Router。已有证据连续
排除了两个强默认前提：fine 既不是 shared coarse 的弱版本，也没有显示为跨父类
稳定共享的一套 fine 坐标。与组会“先有父类条件，再做父类内细分”最相容的候选
是父类条件化的局部 fine Router；但其训练可学性和语言模型收益尚未验证。

## 3. 结论边界

- **直接结果：**粗—细原始重合在 24/24 个比较中低于匹配标签置换中位数；跨父类 fine
  功能在 0/6 层满足注册复现规则。
- **最可靠认识：**谱位置、方向重合、线性可读性和 Router 功能是四个不同对象。
  当前完整表征中的细类信息具有冗余，但最有效的细类判别坐标具有父类条件性。
- **不能推出：**严格正交、严格父类局部、原生 Router 已使用这些方向、某层是
  最佳层、树状 Router 必然改善语言模型 loss，或结果可外推到任意自然语料。
- **对导师 intuition 的更新：**“粗细都在尾部”可以保留为谱位置观察；“因此
  两者共用同一子空间”不受支持；“正确父类条件可能帮助细分”成为下一项应直接
  用架构和 end-task loss 检验的假设。

## 4. 唯一下一决策

**唯一问题（AI 提案，待研究者确认）：**

> 在数据、容量、优化和监督完全匹配时，正确父类条件下的局部 fine Router，是否
> 比一个全局共享 fine Router 更容易学会稳定细分，并同时改善样本外 routing
> 质量和语言模型 NLL？

这是目前最值得检验的问题，因为它直接检验 0826 组会提出的架构机制，也不会
继续在被动子空间指标上钻牛角尖。

**完成标准：**只做一个预注册的共享-vs-父类条件化架构比较；父类条件是唯一结构
差异，容量、数据、训练预算和优化相同；routing 质量与 held-out NLL 必须同时
报告，任一不改善都不能宣称架构得到支持。

**恢复动作：**研究者先用自己的话确认或纠正 A15_10 的直接结果、认识边界和上述
唯一问题；确认后另建下一周期 Focus 与 Protocol。当前不直接启动 Router 训练。
