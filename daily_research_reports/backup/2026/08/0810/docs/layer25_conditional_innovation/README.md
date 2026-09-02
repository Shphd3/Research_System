# 第 25 层新增可访问性 — 读者侧材料

本目录是
[完整日报](../daily_report_layer25_conditional_innovation.md)引用的图表与表格目录。
日报承担唯一的 reader-friendly 解释；canonical 事实仍以 A15_08 的 Protocol、
Summary 和 Detailed 为准。

## 当前人工审计范围

- 已审计：$X,Z,U,R_U$ 的定义，以及由 $G_{true}$、$G_{state}$、$T_{cap}$
  支撑的第 25 层局部新增可访问性结论。
- 未审计：求解广义特征方程并据此构造目标条件方向的实验、二维充分性和后续
  秩阶梯；这些对象不特别直接地回答当前的新增可访问性问题。
- 因此，本目录中的方向/秩图表只属于 canonical 辅助记录，不承担当前日报的
  认识更新或下一决策。

## 文件资格

- `tables/e04_confirmation_metrics.csv` 是 eligible E04 决策表；当前日报只读取
  其中 $G_{true}$、$G_{state}$ 和 $T_{cap}$ 三项。
- `figures/figure_e04_fresh_confirmation_gates.png` 同时含局部增益与方向充分性
  面板；当前人工审计只覆盖局部增益部分，因此日报不把整图作为中央证据。
- `figures/figure_common_basis.png` 只作 TRAIN-only 位置诊断，不能定义新增信息。
- 文件名含 `e03` 的材料来自 `INELIGIBLE_GUARD` 运行，仅作诊断。
- 旧的 `confirmation_metrics.csv`、`confirmation_control_summary.csv` 与文件名
  含 `e02` 的材料不承担本轮结论。

完整来源：

- [A15_08 中文 Anchor](../../../../Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/15_08_target_conditioned_layer_innovation_anchor_cn.md)
- [E04 Protocol](../../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/protocol.md)
- [E04 Summary](../../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/summary.md)
- [E04 Detailed](../../../../Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E04_strict_conformance_repair/detailed.md)
