# mathematics 与 physics 的细类判别功能能否跨父类迁移？

```text
type: meeting_cycle_core_task
workstream: A15_cross_parent_fine_function_transfer
status: EVIDENCE_COMPLETE_AWAITING_HUMAN_RESULT
core_question: HUMAN_CONFIRMED
plain_language_design: HUMAN_CONFIRMED
cycle_start: 2026-08-26
target_meeting: Unknown
active_project: Projects/from-attention-to-search/
anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_10_cross_parent_fine_function_transfer/15_10_cross_parent_fine_function_transfer_anchor.md
protocol: Projects/from-attention-to-search/main/experiments/A15/15_10_cross_parent_fine_function_transfer/A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer/protocol.md
source_meeting: daily_research_reports/backup/2026/08/0826/docs/0826会议记录.md
research_reset: 2026-08-28 human-confirmed real-data-only cross-parent transfer question
core_experiment_count: 1
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
resource_profile: h100-4-reserved
acp_job: pt-9dwr9q52
run_stamp: 20260828T032514Z
```

## 1. 核心问题

> 在冻结 Qwen3-30B-A3B 的原生完整表征中，mathematics 与 physics 的细类
> 判别功能，是由一组可以跨父类承载目标任务的共同方向承担，还是只能由目标
> 父类自己的局部方向承担？这种关系在六个固定层和 C4/C5 两套面板中是否复现？

“跨父类承载”只表示：源父类估计出的七维空间，在重新训练目标父类自己的分类头
后仍保留目标细分类功能。它不表示两个父类共用标签，也不表示原生 Router 已经
使用这些方向。

## 2. 实验目的

在不训练 Qwen 或 Router、不删除任何原生表征分量的前提下，比较目标自己的细类
空间、另一父类的细类空间、完整流程标签置换空间和共同粗类空间。主连续效应量是
相对功能保留量 RR；0.9 只作读图参照，不作科学门槛。

完成标准：Block 4/12/20/28/36/44、mathematics→physics 与
physics→mathematics、C4/C5 全部按同一 A/B cross-fit 合同完成；每个比较保留
Own、Cross、完整 pipeline permutation null、共同粗类对照、RR、样本外 NLL、
平衡准确率和模板家族级不确定性。无效单元保留并报告，不替换层、父类或面板。

**本轮不回答：**共享或父类专属 Router 是否降低语言模型 loss、原生 Gate 是否
使用这些方向、删除某个空间是否具有因果收益、未测父类或自然文本总体是否相同。

## 3. 分析方法

1. 在同一面板、层和 A/B 半边内，用全部 64 个叶类的残差拟合一个共同的 pooled
   Fisher 度量；mathematics、physics、Own、Cross 和所有置换条件严格复用它。
2. 严格交叉拟合：A 估计空间并用目标 A 训练目标分类头，去目标 B 测试；然后
   B→A 反做一次。Own 与 Cross 除空间来源外，目标训练样本、目标标签、七维输入、
   分类头规则、训练内正则化选择和测试样本完全一致。
3. 置换 null 对每次置换重跑“源空间估计→目标投影→目标头训练→独立测试”的完整
   流程；置换和 bootstrap 都以完整模板家族为统计单位。C4/C5 分开报告后再判断
   是否复现，几何重合只作辅助解释。

## 4. 结论

### 执行前：两种预期结果

- **若支持可迁移的共同 fine 功能：**目标自己的空间首先有效，Cross 在两个方向
  均稳定超过完整流程置换 null，RR 明显高于零，并在 C4/C5 的相同层复现。允许说
  存在跨父类可迁移的线性细分类功能；不能说它已被 Router 使用或应立即采用共享
  Router。
- **若不支持或证据不足：**若 Own 有效而 Cross 回到完整流程 null，只能说本轮
  未建立跨父类迁移，并把父类局部空间保留为更相容的候选；若 Own 无效、方向不
  对称、C4/C5 不复现或 RR 分母无效，则记为证据不足，不能用失败显著性证明严格
  的父类特异性。

### 执行后：由研究者完成

- **证据状态：**full run 已完成；24 个注册单元和三张图通过完成审计。请先阅读
  [Summary](../../../Projects/from-attention-to-search/main/experiments/A15/15_10_cross_parent_fine_function_transfer/A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer/summary.md)
  与 [Detailed](../../../Projects/from-attention-to-search/main/experiments/A15/15_10_cross_parent_fine_function_transfer/A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer/detailed.md)。
- **直接结果：**待研究者用自己的话确认或纠正 canonical evidence 中的结果。
- **我的结论：**待研究者填写。
- **仍不能说：**待研究者填写。
- **唯一下一决策：**待研究者根据真实迁移结果填写；不得直接启动 Router 训练。

## 路径

- **Anchor：**[15_10 Anchor](../../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_10_cross_parent_fine_function_transfer/15_10_cross_parent_fine_function_transfer_anchor.md)
- **Protocol：**[A15_10_E01 Protocol](../../../Projects/from-attention-to-search/main/experiments/A15/15_10_cross_parent_fine_function_transfer/A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer/protocol.md)
- **Predecessor Summary：**[A15_09_E01 Summary](../../../Projects/from-attention-to-search/main/experiments/A15/15_09_layerwise_coarse_fine_reuse_geometry/A15_09_E01_qwen3_30b_cross_depth_coarse_fine_reuse/summary.md)
- **Parking Lot：**[README.md](../../../Projects/from-attention-to-search/main/parking_lot/README.md)
