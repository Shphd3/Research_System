# 原生路由表征中，八个领域是否复用稳定判别方向？

```text
type: meeting_cycle_core_task
status: EXECUTION_APPROVED
core_question: HUMAN_CONFIRMED
plain_language_design: HUMAN_CONFIRMED
cycle_start: 2026-08-28
target_meeting: Unknown
active_project: Projects/from-attention-to-search/
anchor: ../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_09_layerwise_coarse_fine_reuse_geometry/subanchors/15_09_01_native_g_domain_consensus_variance_atlas_anchor.md
protocol: ../../Projects/from-attention-to-search/main/experiments/A15/15_09_layerwise_coarse_fine_reuse_geometry/A15_09_01_E01_native_g_domain_consensus_variance_atlas/protocol.md
source_meeting: researcher-confirmed 2026-08-28 MVP reset
core_experiment_count: 1
```

## 1. 核心问题

E06 在原生路由输入 $G=X+U$ 上看到：每个领域区分八个细类别通常需要 6--7 维，而八个领域共用一个空间需要 16 维。现在只问一个最小问题：Block 46 的压缩是否真的来自多个领域复用稳定、标签相关的判别方向，而不是共同协方差、标准化或有限样本不稳定造成的假重合？

## 2. 实验目的

1. 在 Block 46 用匹配标签置换裁定八个领域的判别子空间是否存在超出协方差结构的稳定重合。
2. 若存在候选共识方向，确定它们位于原始 $G$ 的高、中还是低方差区域。
3. 用同一冻结口径扫描 48 层，描述重合、可读性和方差位置如何随深度变化；完整层间图不能改变 Block 46 主判定。

完成标准：Block 46 有 Pass/Fail/Insufficient 类型判定；48 层表格完整；重合热图、共识谱/方差位置图和层间趋势图通过可读性审计。

**本轮不回答：**模型原生路由是否使用这些方向、方向是否提高专家效用、移除方向是否造成因果损失、或是否应训练新路由器。

## 3. 分析方法

1. 只使用 $G$，在每一层为八个领域分别学习秩七的细类别判别空间，并把方向从标准化坐标映回原始表征坐标。
2. 用留一模板族检查同领域方向稳定性，再与保持领域、模板和数据协方差的标签置换对照比较跨领域重合；不稳定时停止解释。
3. 对通过门槛的方向计算八域共识谱和主成分方差位置，并把同一指标画成 48 层趋势。

## 4. 结论

### 执行前：两种预期结果

- **若支持：**Block 46 的八个局部空间自身稳定，真实平均重合超过匹配标签置换上界；可以说 E06 的共享秩压缩与稳定标签相关方向复用一致，并决定是否进入冻结保留/移除干预。
- **若不支持或证据不足：**若空间稳定但重合不超过置换对照，则撤回稳定方向复用解释；若空间自身不稳定，则判为证据不足。两者都不允许直接进入表征学习。

### 执行后：由研究者完成

- **直接结果：**[AWAITING_EXECUTION]
- **我的结论：**[AWAITING_HUMAN_RESULT]
- **仍不能说：**[AWAITING_HUMAN_RESULT]
- **唯一下一决策：**[AWAITING_HUMAN_RESULT]

## 路径

- **Protocol：**[protocol.md](../../../Projects/from-attention-to-search/main/experiments/A15/15_09_layerwise_coarse_fine_reuse_geometry/A15_09_01_E01_native_g_domain_consensus_variance_atlas/protocol.md)
- **Summary：**按研究者要求暂不创建
- **Detailed：**按研究者要求暂不创建
- **Daily Report：**按研究者要求暂不创建
- **Parking Lot：**[README.md](../../../Projects/from-attention-to-search/main/parking_lot/README.md)
