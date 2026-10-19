# 数据与来源

主要组统计由执行侧phi_input_hidden.py产生，作图CSV由plot_phi_input_hidden.py产生，结果后上下文诊断由phi_context_diagnostic.py复算。统计来源由provenance/frozen_config.json冻结；provenance/cache_identity_check.json是本轮完整字节SHA校验，input_access.json是本轮严格访问检查。

| 文件 | 内容及口径 |
| --- | --- |
| data/group_members.csv | R/F/N全部41,421条成员行；每条件13,807成员，每行带n_D、N_D、p_D。 |
| data/per_group_winner_support.csv | 全558组条件行；未采样前胜出位置、context和原D胜出数，包含零支持。 |
| data/per_group_input_hidden_metrics.csv | 全558行的抽样数、状态、频率、context、原方差、删去方差、剩余方差及两占比；空值为明确不可估。 |
| data/population_summary.csv | 主145组、R/N161组、按大小分层和每条件全部支持组的等权汇总；人口不同不能混为同一比较。 |
| data/paired_group_contrasts.csv | 同组ID大小匹配的R-F/R-N差值和方向计数，差值并非相同文本上的干预效应。 |
| data/sample_context_coverage.csv | 实际抽样位置的context构成，context不是已验证独立文档。 |
| data/phi_input_normalized_spectrum_plot_data.csv | 原/余全部1024方向的组等权平均占比，以及哪些方向画出。 |
| data/phi_input_first_direction_plot_data.csv | 主145组的逐组原/余第一占比。 |
| data/R_input_hidden_spectra.npz等三文件 | 全186组的抽样行/绝对位置ID、原/余特征值及归一化谱、各条件支持和可估标记；不足行保留NA，不含原始hidden或decoder。 |
| provenance/plot_selection.json | 主145组及R/N161组的共同支持/可估名单，原谱与剩余谱使用同一名单。 |

计算代码和原评分源码副本在code；代码默认执行路径依赖真实缓存，作图通过显式参数可只读报告内小数据。主score/分组、位置抽样、中心化和删首分量均已独立复核，详见provenance中audit文件。数值资格只是计算核验，不是科学批准。
