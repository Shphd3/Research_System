# Detailed: A15_08_04_E01 DCLM Transition-Object Spectrum Comparison

Primary Anchor: [A15_08_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_04_transition_object_spectrum_sensitivity_anchor_cn.md)  
Frozen Protocol and registered revision: [protocol.md](protocol.md), frozen 2026-08-17 before execution  
Summary: [summary.md](summary.md)  
Result eligibility: `ELIGIBLE / AI_DRAFT_AWAITING_HUMAN_JUDGMENT`

## 0. Quick Recap

Purpose: 审计“谱低秩”是否依赖对象身份与 RMSNorm，而不是检验语义或功能。  
Hypothesis: 至少一个 raw/RMSNorm 配对会产生材料性、方向一致的 \(r_{80}\) 改变。  
Experiment logic: 同一 forward 捕获 \(h_l,a_l\)，严格构造 \(r_l,X_l,Z_l,U_l\)，对八类矩阵使用完全相同的中心化协方差谱。  
Direct result: \((Z,r)\) 绝对差中位数 0.194675、方向一致率 0.8056；另外两组相邻差分只有 0.013679/0.011724。  
Eligibility: 全部身份、覆盖、有限性、归一化和绘图 guard 通过。  
Verdict: `DEFINITION_SENSITIVE`，由状态对照触发。  
Claim boundary: 只说明几何度量依赖对象；不能说明新增信息、语义、功能或 Router 效用。

## 1. Terminology / Definitions

| Term | 白话 | 具体对象 | 单位 / 公式 | 为什么重要 | 不能证明 |
| --- | --- | --- | --- | --- | --- |
| \(h_l\) | Attention 前的 raw 残差 | block pre-hook | token×4096 | 跨层累积状态 | 新增信息 |
| \(a_l\) | 本层 Attention 写入 | `self_attn.o_proj` 输出 | token×4096 | 本层 Attention 的直接 write | 功能价值 |
| \(r_l\) | Attention 后、RMSNorm 前状态 | \(h_l+a_l\) | token×4096 | 展示 raw 尺度效应 | MLP 实际输入几何 |
| \(X_l\) | 旧状态按本层尺度归一化 | \(N_l(h_l)\) | token×4096 | 与 \(Z_l\) 同坐标定义 | 旧信息全部可预测性 |
| \(Z_l\) | 模型真实 MLP 输入 | \(N_l(h_l+a_l)\) | token×4096 | native hook 已核对 | MLP 使用了哪种语义 |
| \(U_l\) | 同层归一化更新 | \(Z_l-X_l\) | token×4096 | 当前最清楚的同 token 更新候选 | “真正新增信息” |
| \(r_{80}\) | 容纳 80% 方差的最少方向数 | 谱累计阈值 | 除以 2047 | 比较谱紧凑度 | 功能低秩或总体内禀秩 |

## 2. Anchor Link And Decision Point

本实验回答 A15_08_04 的对象身份审计，不重开 A15_08_02 的功能准入，也不替代 A15_08_03 的功能压缩。决策点只有一个：后续 token-subspace 分析必须先冻结一个不会被 raw 尺度异常混淆的具名对象。

## 3. Protocol Freeze, Conformance, And Deviations

| 注册项 | 预期 | 实际 | 状态 | 证据 | eligibility 影响 |
| --- | --- | --- | --- | --- | --- |
| 数据 | 指定 DCLM 文件 offset 0、2048 IDs | size 299003652 B；SHA `b5b307...e72ec`；slice SHA `63c9a3...39e88` | PASS | [preflight](manifests/preflight.json) | 无 |
| 模型 | `/data/share/Qwen3-8B`，36×4096 | 一致 | PASS | preflight | 无 |
| 对象身份 | native \(Z\)、\(U=Z-X\)、36 层完整 | 三项最大误差均 0 | PASS | [extraction manifest](manifests/extraction_manifest.json) | 无 |
| smoke | 128 token exact replay | `smoke-v2` replay 最大误差 0 | PASS | worker run | 无 |
| 全谱 | 283 曲线、float32、rank cap 2047 | 283/283，有限、单调、和为 1 | PASS | spectra + metrics | 无 |
| 坐标 | rank 1–2048；log y \(10^{-12}\)–1 | 一致 | PASS | figures | 无 |
| 注册判据 | 三组 paired contrasts | 完整 | PASS | paired table + verdict | 无 |
| 首次 smoke | 使用可运行环境 | 默认 `/usr/bin/python` 缺 `transformers`，模型加载前停止 | RETRY / EXCLUDED | `smoke` 失败目录 | 科学体未执行；无 eligibility 影响 |
| 成功环境 | 复用现有环境 | `spectral-hier`, transformers 5.6.0.dev0, torch 2.5.1+cu121 | RECORDED | execution log | 无 |
| 后验尺度审计 | 非注册主判据 | 定位 raw residual 首 token 范数异常 | POST-HOC DIAGNOSTIC | scale diagnostic | 只解释主结果，不改变 verdict |

Frozen Protocol revision: 2026-08-17 pre-execution freeze。  
Execution scope approved: implementation、smoke、full run、analysis、local figures。  
Amendments: 无科学体 amendment。  
Retries and exclusions: 一次依赖环境失败；无模型 forward、无数据或指标改变。  
Missing conditions or artifacts: 无。  
Post-hoc analyses: raw \(r_l\) 的逐 token L2 范数审计。

## 4. Actual Setup

Research question: 在固定自然文本 token 下，对象定义与 RMSNorm 是否改变中心化协方差谱？  
Data construction and provenance: 指定 `.bin` 的前 2048 个 `uint32` token ID，作为一个连续 causal 序列。  
Train / development / confirmation split: 不适用。  
Learning task and permitted supervision: 无训练、无标签、无选择。  
Model / architecture / algorithm: Qwen3-8B，36 block，bf16 forward，SDPA；float32 Gram eigenspectrum。  
Input representation / position encoding: 一个 shape `[1,2048]` 序列，position 0–2047。  
Training objective / optimizer / steps / checkpoints: 不适用。  
Seeds: 8170401，只用于框架环境固定。  
Conditions: \(\Delta a,\Delta h,\Delta X,\Delta r,\Delta Z,U,r,Z\)。  
Changed variables: 层对象与 RMSNorm。  
Held fixed: token、forward、层、中心化、估计器、归一化、坐标。  
Known limitation: 单序列；首 token 的 raw residual 出现极大尺度；token 和层均非独立重复。

## 5. Metrics And Registered Decision Rules

每个矩阵按 token 行中心化，计算 \(G=MM^T/2047\)，得到归一化谱 \(p_j\)。主量 \(r_{80}/2047\)。若任一配对绝对差中位数至少 0.05 且方向一致率至少 0.70，则 `DEFINITION_SENSITIVE`；若全部绝对差低于 0.02 且方向一致率低于 0.70，则 `DEFINITION_ROBUST_WITHIN_TOLERANCE`；否则 `INSUFFICIENT`。

## 6. Evidence Lineage

| Claim / decision | 注册标准 | 原始产物 | 计算 | 聚合 / 不确定性 | 观测 | Eligibility | Verdict | 限制 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 对象定义敏感 | 任一对达 0.05 与 0.70 | `activations.pt` | 283 个 Gram 谱 | 层配对中位数；无 CI | \((Z,r)\): 0.194675, 0.8056 | ELIGIBLE | SENSITIVE | 由状态对照触发 |
| 相邻 pre-attn RMS 效应小 | 描述主对照 | 同上 | \(\Delta X-\Delta h\) 的 \(r_{80}\) 差 | 35 层 | abs 0.013679, dir 0.6286 | ELIGIBLE | 未达敏感阈值 | 不等于统计等价 |
| 相邻 post-attn RMS 效应小 | 描述主对照 | 同上 | \(\Delta Z-\Delta r\) 的 \(r_{80}\) 差 | 35 层 | abs 0.011724, dir 0.5714 | ELIGIBLE | 未达敏感阈值 | 不等于统计等价 |
| raw 状态低 rank 外观受尺度异常驱动 | 后验解释 | `activations.pt` | token L2 norm | 每层 max/median | block 8: 12414/46.7=265.9 | BOUNDED diagnostic | 支持尺度解释 | 非注册主判据 |

## 7. Main Results

### Eligible decision evidence

| 对象 | 层中位 \(r_{80}/2047\) | 最小 | 最大 | 读法 |
| --- | ---: | ---: | ---: | --- |
| \(\Delta a\) | 0.1324 | 0.0625 | 0.1676 | Attention write 跨层差较集中 |
| \(\Delta h\) | 0.2408 | 0.0005 | 0.2848 | raw 跨层状态差，含异常层 |
| \(\Delta X\) | 0.2482 | 0.0254 | 0.2946 | normalized 旧状态跨层差 |
| \(\Delta r\) | 0.2364 | 0.0005 | 0.2829 | raw post-attn 跨层差，含异常层 |
| \(\Delta Z\) | 0.2501 | 0.0230 | 0.2907 | actual MLP input 跨层差 |
| \(U\) | 0.1060 | 0.0479 | 0.1368 | 同层 normalized Attention update |
| \(r\) | 0.00147 | 0.00049 | 0.1739 | 被首 token raw 尺度支配，不可直接解读为语义低秩 |
| \(Z\) | 0.1976 | 0.0743 | 0.2755 | RMSNorm 后状态不再被 raw 尺度支配 |

### Bounded and diagnostic evidence

raw \(r_l\) 在 block 8 的最大 token 范数从 block 7 的 78.8 跳到 12,414，位置固定为序列首 token（ID 17814）；其相对中位数从 2.0 倍变为 265.9 倍。该异常持续到后层但相对倍数逐步下降。它足以解释为何 raw 状态多层的 \(r_{80}=1\)，以及为何 \((Z,r)\) 出现巨大差别。

### Failed / missing / ineligible evidence

没有缺失主条件。首次 smoke 只证明默认解释器缺依赖，未产生科学数据；不进入任何聚合。

## 8. Visualization Results

### 八种对象统一坐标

![八种对象统一坐标](figures/all_objects_common_axes_grid.png)

Purpose: 同一眼界比较全部谱，不允许各图自动缩放制造假差异。  
Metric: 每个 eigenvalue 占 covariance trace 的比例。  
How to read: 曲线越陡、越早下降，能量越集中；颜色表示层/目标层。  
Observed: \(r\) 的层间变化最大；\(U\) 与 \(\Delta a\) 通常比四种跨层状态差更集中。  
Cannot prove: 曲线方向对应何种语义或功能。

### 80% 能量秩随层变化

![r80 随层变化](figures/r80_by_layer_and_object.png)

Purpose: 将 2048 点谱压缩为可比较的层曲线。  
How to read: 纵轴 0.1 表示约 205 个方向容纳 80% 样本方差。  
Observed: raw \(r\) 在 block 8–25 接近 0，但这与首 token 尺度异常同步；normalized \(Z\) 没有该坍缩。  
Anchor implication: raw state 不适合作为后续新增信息空间的默认对象。

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | 状态 | 说明 | 排除 | 仍可能 |
| --- | --- | --- | --- | --- | --- |
| 对象身份 | native hook 与重构误差 0 | PASS | 公式/钩子一致 | hook 错位 | 模型本身尺度异常 |
| 数据/估计器统一 | 同 tokens 与同谱代码 | PASS | apples-to-apples | 样本/坐标差异 | 单序列特殊性 |
| 相邻差分敏感性 | 两组差均约 1% | 未达敏感阈值 | 没有强 RMSNorm 位移 | “差分必然大变” | 更换数据后可能不同 |
| 状态敏感性 | 19.5%、80.6% | PASS | 注册 H-SENS 成立 | 定义完全稳健 | Pass 由尺度异常驱动 |

Falsified operationalization: raw residual 的视觉低秩不能直接当作新增信息低秩。  
Remaining rival explanations: 首 token/连续序列的特殊性、单个 DCLM slice、模型版本特异性。

## 10. Full Experiment Record

- Unit tests: 11/11 pass。
- Smoke: `a15-08-04-e01-20260817-smoke-v2`, 128 tokens, exact replay。
- Full extraction: `a15-08-04-e01-20260817-full`, 2048 tokens, 36 layers, activation SHA `7cc640...4454`。
- Analysis: 283 curves, 23.1 seconds, registered verdict `DEFINITION_SENSITIVE`。
- Rendering: 11 PNG + 11 PDF families；canonical 保存 11 PNG。

## 11. Interpretation

最稳妥的认识更新不是“表征低秩”，而是：“谱秩首先属于一个明确对象；raw residual 的 token 尺度可以制造极端低秩外观。”相邻 raw/normalized 差分的中位影响很小，说明这次 Pass 不应被讲成“跨层新增信息对 RMSNorm 高度敏感”。\(U_l\) 的谱相对集中是几何观察，必须经过功能或语义条件化检验后，才能进入新增信息叙述。

## 12. Claim Boundary

Can claim: 同一样本内对象定义敏感；raw 状态谱会被单 token 尺度支配。  
Cannot claim: 新增语义、功能低秩、总体内禀秩、因果使用、Router 效用。

## 13. Next Decision

Decision: 研究者确认是否冻结 \(U_l=Z_l-X_l\) 为后续 token-subspace 分析对象。  
Completion criterion: 接受或拒绝“raw \(r_l\) 只作尺度诊断”的边界。  
Resume action: 接受后另立 token-level、功能条件化的子空间分析，不在本实验追加后验语义标签。

## 14. Artifact Manifest

| Artifact | Purpose | Producer | Source | Hash / identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `protocol.md` | 冻结科学体 | researcher + AI | approved design | pre-run 2026-08-17 | yes | yes | 未被结果改写 |
| `activations.pt` | 原始 \(h,a\) | `extract.py` | model + DCLM slice | `7cc640...4454` | yes | yes | worker-only |
| `arrays/spectra.npz` | 283 个全谱 | `analyze.py` | activations | `3ef6b9...cda7` | yes | yes | worker-only |
| [spectrum_metrics.csv](tables/spectrum_metrics.csv) | 每曲线指标 | `analyze.py` | spectra | `86bf40...b3f1` | yes | yes | canonical copy |
| [paired_contrasts.csv](tables/paired_contrasts.csv) | 注册主对照 | `analyze.py` | metrics | `decece...25c0` | yes | yes | canonical copy |
| [verdict.json](manifests/verdict.json) | 阈值裁定 | `analyze.py` | paired table | `d2dafa...e98f` | yes | yes | canonical copy |
| [scale diagnostic](manifests/raw_state_scale_diagnostic.json) | raw 尺度审计 | `audit_scale.py` | activations | `828243...bc5` | yes | bounded | post-hoc |
| [grid](figures/all_objects_common_axes_grid.png) | 全对象总图 | `render.py` | spectra | `c0de79...2f07` | yes | yes | common axes |
| [r80](figures/r80_by_layer_and_object.png) | 层曲线 | `render.py` | metrics | `1013fc...6361` | yes | yes | no CI |

## 15. Links

anchor: [A15_08_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_04_transition_object_spectrum_sensitivity_anchor_cn.md)  
protocol: [protocol.md](protocol.md)  
summary: [summary.md](summary.md)  
code workspace: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_04_e01_dclm_transition_object_spectrum_comparison/`  
result dir: `/data/250010109/MoE_Router/experiments/20260817_a15_08_04_e01_dclm_transition_object_spectrum_comparison/runs/a15-08-04-e01-20260817-full/`  
repro: `extract.py --token-count 2048`, then `analyze.py`, then `render.py` under the existing `spectral-hier` environment.
