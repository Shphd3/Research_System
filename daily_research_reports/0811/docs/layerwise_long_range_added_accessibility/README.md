# 逐层长程新增可访问性 — 0811 读者侧文件夹

## 作用

本文件夹承接
[完整日报](../daily_report_layerwise_long_range_added_accessibility.md)后续引用的
读者侧图表。日报仍是唯一完整解释；本 README 只负责导航，不复制实验方法或
形成第二份结论。

## 当前状态

- 问题、方法、判定边界和图表合同已经人工审计通过。
- 正式结果已经返回，注册 verdict 为 `H2_LC_FAIL_CONTROL_DEGRADATION`。
- 结果性认识更新仍为 `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`。
- H1-REP 只报告表征有效秩与公共基能量，不设 Pass/Fail 阈值。

## 当前读者图

- `figures/figure_1_layerwise_accessibility.png`：blocks 2--36 的条件增益、
  差中差及五项判据区间；
- `figures/figure_2_representation_rank_common_basis.png`：表征有效秩、80% 方差
  秩、总方差与公共基能量。

Canonical evidence: [Summary](../../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_01_E02_layerwise_long_range_gain_and_representation_rank_blocks_2_36/summary.md) / [Detailed](../../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_01_E02_layerwise_long_range_gain_and_representation_rank_blocks_2_36/detailed.md).

不得把运行日志、原始张量、缓存、完整 bootstrap 数组或调试图放入本目录。
