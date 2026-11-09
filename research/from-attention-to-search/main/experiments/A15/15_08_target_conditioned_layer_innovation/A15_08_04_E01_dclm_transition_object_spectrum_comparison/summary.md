# Summary: A15_08_04_E01 DCLM Transition-Object Spectrum Comparison

Primary Anchor: [A15_08_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_04_transition_object_spectrum_sensitivity_anchor_cn.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status / eligibility: `ELIGIBLE / AI_DRAFT_AWAITING_HUMAN_JUDGMENT`

## Result Snapshot

**注册判据结果：**`DEFINITION_SENSITIVE`。

**直接建立的事实：**在同一 Qwen3-8B、同一段 2,048-token DCLM 序列与同一谱估计器下，谱形状是否显得紧凑，确实依赖所测对象以及是否经过 RMSNorm。但这个 Pass 完全由整层状态对照 \((Z_l,r_l)\) 触发；两个真正的相邻层差分对照 \((\Delta X,\Delta h)\) 和 \((\Delta Z,\Delta r)\) 的中位差只有 0.0137 和 0.0117，均未达到 0.05 的敏感阈值。

**白话结论：**“不同对象不能混着谈秩”得到验证；但不能进一步说“跨层新增信息的秩被 RMSNorm 大幅改变”。特别是 raw residual 中一个极大范数 token 会把多层的协方差能量压到第一方向，RMSNorm 消除了这个尺度支配。因此，后续分析不能拿 raw residual 的低秩外观当作新增信息低秩。

**下一步：**研究者先确认是否接受以下对象选择：后续 token-subspace 分析固定使用具名的同层归一化更新 \(U_l=Z_l-X_l\)，raw 状态 \(r_l\) 只作为尺度诊断，不作为“新增信息”对象。

## Decision-Bearing Setup

Question: 同一批 token 上，raw/RMSNorm 与八种具名层对象的中心化协方差谱是否实质不同？  
Treatment and control: RMSNorm 对象对照相应 raw 对象。  
Changed variable: 对象身份与 RMSNorm 位置。  
Held fixed: 模型、2,048 token、层、中心化、Gram 协方差、float32 eigenspectrum、秩上限与绘图坐标。  
Primary metric and unit: 匹配层 \(r_{80}/2047\) 的绝对差中位数与方向一致率。  
Known limitation: 只有一个相关 token 序列；层和 token 都不是独立重复；该指标只描述几何能量分布。

## Verdict Basis

| 注册对照 | 绝对差中位数 | 有符号中位差 | 方向一致率 | 注册裁定 | 来源 |
| --- | ---: | ---: | ---: | --- | --- |
| \(\Delta X\) vs. \(\Delta h\) | 0.013679 | +0.005862 | 0.6286 | 未达敏感阈值 | [paired_contrasts.csv](tables/paired_contrasts.csv) |
| \(\Delta Z\) vs. \(\Delta r\) | 0.011724 | +0.005374 | 0.5714 | 未达敏感阈值 | [paired_contrasts.csv](tables/paired_contrasts.csv) |
| \(Z\) vs. \(r\) | **0.194675** | **+0.194675** | **0.8056** | **触发 `DEFINITION_SENSITIVE`** | [paired_contrasts.csv](tables/paired_contrasts.csv) |

## Key Evidence

- 283/283 条注册曲线完整；36 层 native MLP 输入身份误差、\(U=Z-X\) 重构误差和 128-token 重放误差均为 0。见 [manifests](manifests)。
- \(U_l\) 的层中位 \(r_{80}/2047=0.1060\)；\(\Delta a_l\) 为 0.1324；\(\Delta X_l\) 与 \(\Delta Z_l\) 分别为 0.2482 和 0.2501。它们是样本几何描述，不是功能低秩结论。见 [spectrum_metrics.csv](tables/spectrum_metrics.csv)。
- raw 状态 \(r_l\) 的层中位 \(r_{80}/2047=0.00147\)，但从 block 8 起首 token 的 raw 范数为 12,414、同层中位数为 46.7（约 266 倍）；因此该极低 rank 主要是尺度异常的结果。见 [raw_state_scale_diagnostic.json](manifests/raw_state_scale_diagnostic.json)。

## Central Figures

![八种对象的统一坐标谱图](figures/all_objects_common_axes_grid.png)

![各层 r80 占比](figures/r80_by_layer_and_object.png)

## Claim Boundary

Can claim: 这一次样本内的协方差谱对具名对象与 RMSNorm 定义敏感；整层 raw 状态会被 token 尺度异常严重扭曲。  
Cannot claim: 哪个方向编码语义、新增信息是否功能低秩、模型是否使用这些方向、总体内禀秩，或该空间能否服务 Router。

## Next Decision

Decision: 由研究者确认是否把 \(U_l=Z_l-X_l\) 冻结为后续 token-subspace 分析的主对象。  
Completion criterion: 明确接受或拒绝“raw \(r_l\) 只作尺度诊断、\(U_l\) 作新增更新候选对象”的判断。  
Resume action: 接受后再为 \(U_l\) 的 token-level 子空间与功能邻近性分析另立实验；本实验不追加语义解释。
