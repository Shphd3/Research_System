# 逐层长程新增可访问性 — 0811 读者侧文件夹

## 作用

本文件夹承接
[完整日报](../daily_report_layerwise_long_range_added_accessibility.md)后续引用的
读者侧图表。日报仍是唯一完整解释；本 README 只负责导航，不复制实验方法或
形成第二份结论。

## 当前状态

- 问题、方法、判定边界和图表合同已经人工审计通过。
- 正式实验结果尚未返回，状态为 `AWAITING_CANONICAL_RESULTS`。
- 当前没有结果图、结果表或 H2-LC verdict。
- H1-REP 只报告表征有效秩与公共基能量，不设 Pass/Fail 阈值。

## 结果返回后允许加入

- `figures/figure_layerwise_added_accessibility.png`：36 层的条件增益、差中差及
  五项判据区间；
- `figures/figure_representation_rank_common_basis.png`：表征有效秩、80% 方差
  秩、总方差与公共基能量；
- 只包含上述两图直接使用、并能回溯到 canonical `summary.md` / `detailed.md`
  的紧凑表格。

不得把运行日志、原始张量、缓存、完整 bootstrap 数组或调试图放入本目录。
