# 截图原报告的补充版

先读[保留原标题与段落顺序的报告](report_cn.md)，逐项改动见[修改清单](modification_list_cn.md)和[文字差异](source_diff.patch)。原截图及逐段转录保存在[sources](sources/)，未推测截图外原文。

- 图1：完整186组的组内log频率标准差，仅两根柱、没有误差条。
- 图2：既有三种分配的低频feature条件学习曲线；总体损失另表。
- 图3、4：在同池、同组大小、同V位置上比较组贡献表征的归一化谱与第一方向占比；它们不是原186个phi组，也不是参数谱。
- 图5、6：追加原始hidden谱，直接读取组命中输入位置的缓存hidden，和贡献谱分开解释。
- 列独立置乱图在附录；该操作只作统计随机化，不是合法模型输入干预或学习因果证明。

[谱定义、模型坐标与归一化还原](spectrum_methods_cn.md) · [附录与完整数据](appendix_cn.md) · [原始hidden来源与规则](raw_hidden_methods_cn.md) · [推理审计](reasoning_audit_cn.md)

所有图均保留PNG/PDF、作图数据及脚本。仅完成原结果重绘和新授权的描述性缓存分析，未训练、未修改原建图参数。

重绘：`python code/replot_all.py --output-dir /tmp/report_replot --font <已有中文字体路径>`。此入口只读取随报告的小型表与谱数据，不需模型或训练缓存；[8图实际重绘检查](provenance/replot_verification.json)均逐字节相同。
