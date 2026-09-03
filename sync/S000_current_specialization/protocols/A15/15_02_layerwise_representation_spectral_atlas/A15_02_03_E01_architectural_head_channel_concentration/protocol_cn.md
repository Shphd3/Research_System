---
experiment_id: A15_02_03_E01_architectural_head_channel_concentration
anchor_id: 15_02_03_architectural_head_channel_concentration
status: COMPLETED
execution_status: completed_with_analysis_only_repair
canonical_language: en
companion_language: zh
updated: 2026-08-05
---

# 正式 Protocol：Qwen3-8B MLP 输入通道组与真实注意力头的粗细语义集中性

英文 canonical：[protocol.md](protocol.md)。本文件与英文版使用相同对象、数据、指标、门槛和边界。

## 0. Approval Snapshot

- **文档状态：**`COMPLETED`；冻结提取为 canonical，最终分析包含一次纯绘图修复。
- **已经确认：**同时测量真正 MLP 输入的 32×128 连续通道组，以及 `o_proj` 前的 32×128 真实注意力头；计算原始方差、区分度和每单元八个 16 维频带；报告 mean/typical/max。
- **数据确认：**按研究者 2026-08-05 执行修订，主审计精确复用 A15_02_E01 的 512 条语义文本、token ids、设计/确认模板拆分、最终冒号读出位置和 65,536-token calibration；新 taxonomy 只保留为可选外部复现，不进入本轮主裁定。
- **执行授权：**实现、smoke、两个 full、分析、结果文档和 0805 focus；不含 graph、commit、push 或外部同步。
- **执行闭合：**attention 与 MLP 两个 full 均完成全部冻结提取与统计；远端绘图因 NumPy `median` 方法误用退出，随后从同一提取产物完成 analysis-only 修复。模型、数据、指标、随机种子与判据均未变化。
- **唯一问题：**粗/细语义区分度是否更集中在真实注意力头中，而不是经过多头混合后的固定 MLP 输入通道组；两者是否分别超过各自同形状随机通道分组？
- **主指标：**$C_{\ell h}^g=\log(D_{\ell h}^g/D_{\ell,full}^g)$ 的典型值与全局最大值，并用随机 32×128 分组校准。
- **Pass：**至少一个站点在未触碰数据上对一种粒度超过自己的随机分组；典型集中和稀疏最佳单元分别裁定，并给出两个站点的相对强弱。
- **Fail：**所有门通过，但两个站点的固定单元都与随机分组不可区分。
- **Insufficient：**hook、数据、能力、确认、重建、随机零假设、基底或数值门失败。
- **不能声称：**通道组是注意力头、功能模块、因果语义电路或 Router 坐标。

## 1. Terminology / Definitions

| 术语 | 白话含义 | 具体计算 | 单位/公式 | 判断作用 | 不能证明 |
| --- | --- | --- | --- | --- | --- |
| MLP 输入 | block 的 MLP 真正接收的表征 | post-attention RMSNorm 输出 $m_\ell$ | 4096 维激活 | 冻结研究对象 | 头身份 |
| 真实注意力头输出 | 注意力各头在输出投影前的结果 | `self_attn.o_proj` 的 4096 维输入 reshape 为 32×128 | 128 维/头 | 架构边界参考 | MLP 直接输入 |
| 固定通道组 | 原生顺序上的连续 128 维切片 | G1=`[0:128)`…G32 | 128 维 | 检查原生坐标集中 | 架构模块性 |
| 原始语义方差 | 不同类别中心的实际散布 | $\operatorname{tr}(B)/d$ | activation²/方向 | 实际语义能量 | 去除类内噪声后的可分性 |
| 能量份额 | 一组占全表征类别间能量的比例 | $s=\operatorname{tr}(B_h)/\operatorname{tr}(B)$ | 比例 | 检查能量集中 | 功能效用 |
| 区分度 | 类别中心差异相对同类措辞变化 | $D=\operatorname{tr}(B)/(\operatorname{tr}(W)+\epsilon)$ | 无量纲 | 粗/细语义是否清楚 | 因果使用 |
| 组优势 | 组区分度相对完整表示 | $C=\log(D_h/D_{full})$ | 对数比 | part-vs-whole | 不加随机对照时的特异性 |
| 典型/平均/最佳组 | 32 组的 median/mean/max | 分层报告 | 对数比 | 区分广泛与稀疏效应 | 用 max 代表多数头 |
| 随机通道分组 | 随机打乱 4096 通道后再切 32×128 | 提议 1,024 次 | 零假设 | 排除任意切分效应 | 旋转不变模块性 |
| 组内八频带 | 128 维组内按背景 covariance 排名 | F1；F2--F5；F6--F8 | 每带 16 维 | 定位组内信号 | 跨组同方向 |

## 2. Anchor Alignment

决策问题、物理先验、主模型项和 falsifier 均来自 [A15_02_03 Anchor](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_03_architectural_head_channel_concentration_anchor_cn.md)。本实验是冻结静态的表示集中性与指标审计，不构造 Router。

## 3. Tested Hypotheses

1. **H1 注意力头集中：**真实头的典型或最大 $C^c/C^f$ 超过随机 32×128 通道分组 q95。
2. **H2 MLP 通道组集中：**固定连续组的典型或最大 $C^c/C^f$ 超过随机分组 q95。
3. **H3 站点差异：**相对各自随机零假设校准后，真实头在粗、细或细相对粗集中度上稳定强于 MLP 通道组。
4. **H4 单元内谱特异：**通过集中门的单元中，至少一个真实 F1--F8 频带超过同单元随机 16 维方向。

四条分别裁定。只通过最大值时，只允许称“稀疏最佳组”，不能称“单组普遍优于完整表示”。

## 4. Rival Explanations

1. 完整 $D$ 是组 $D$ 的类内方差加权平均，因此最大组高于完整表示是代数必然。
2. 在 36×32 个单元中挑最大值会产生选择偏差。
3. 连续分组没有特殊性，随机通道分组同样有效。
4. 高 $D/R$ 来自极小分母，而不是强细语义信号。
5. 已经看过的 taxonomy 造成坐标复现，不能外推。
6. 128 维组内近简并谱导致频带旋转。

## 5. Data Construction And Provenance

### 5.1 已暴露 discovery 数据

完全复用 A15_02_E01 的 8 父类 × 8 子类 × 4 模板 × 2 事实包，共 512 条无标签泄漏描述，以及相同的最终 `Classification:` 冒号读出位置、token ids 和 hashes。它可用于工程验证和候选排序，不能单独裁定新的最佳组结论。

### 5.2 同 taxonomy 的封存模板确认

既有 512 条数据的模板 1--2 是 design，模板 3--4 是 confirmation。固定单元定义、八频带、随机划分次数和全部指标均已在读取两个新站点前冻结；design 只允许选择描述性候选单元，所有 verdict 使用 confirmation，并由全局随机最大值校正。

该确认能裁定“在同一自然语义任务上，真实头与 MLP 通道组谁更集中”，但不能建立跨 taxonomy 普遍性；后者明确保留为 claim boundary，而不是本轮 `insufficient`。

### 5.3 独立 covariance 数据

复用 128 篇独立 DCLM、65,536 token，hash=`5c2e9f6b7d307436eda018b7719bc38cddab6387881d77f89bc74fb717b2f792`。固定分成两个 calibration half。统计单位是父类、父类内子类和子类内模板/事实包，不是 512 句。

## 6. Diagnostic Task And Permitted Supervision

同一 $m_\ell$ 同时定义八分类粗语义和各父类内八分类细语义。标签只在冻结提取后用于 $B/W$、能力 probe、bootstrap、置换和作图；Qwen 不更新。confirmation 不能选择层、组、分组 seed、特征值 floor 或阈值。

## 7. Model / Architecture And Frozen Variants

- `/data/share/Qwen3-8B`，36 blocks，hidden size 4096、32 query heads、head dim 128；
- bfloat16 forward，FP64 统计；
- 分支 A 对每个 `layer.mlp` 注册 forward pre-hook，读取 blocks 1--36 的 MLP 直接输入；
- 分支 B 对每个 `layer.self_attn.o_proj` 注册 forward pre-hook，读取并 reshape 为 32 个真实注意力头；
- 共同最终冒号 token；
- 原生通道连续切 G1--G32；
- smoke 同时读取 post-attention layer norm 输出，要求与 MLP pre-hook 精确相等；
- attention smoke 要求 32 头拼接精确重建 `o_proj` 输入，分头线性映射之和重建 `o_proj` 输出；
- 禁止把 G1--G32 称为注意力头，也禁止把 `o_proj` 前输出称为 MLP 输入。

## 8. Training Objective And Optimization

没有模型训练、optimizer 或 checkpoint 选择。ridge probe 只作能力门。随机分组、方向 seed、数值 floor 和绘图范围在 confirmation 前冻结。

## 9. Conditions, Controls, And Evidence

| 条件 | 回答什么 | 最强 rival | 证据角色 | 图表 |
| --- | --- | --- | --- | --- |
| 各站点完整 4096 维 | 分别定义 site-specific $D_{full}$ | 站点尺度混淆 | 主基线 | Figures 2/4 |
| 真实 H1--H32 | 架构头是否集中 | 注意力参考 | 主证据 | Figures 1/2 |
| 固定 G1--G32 | 混合后原生通道集中 | MLP treatment | 主证据 | Figures 1/2 |
| 1,024 随机分组 | 固定切分是否特殊 | 任意切分 | 主 falsifier | Figures 2/5 |
| median/mean/max | 广泛还是稀疏 | max 过度概括 | typed evidence | Figure 4 |
| design/confirmation 模板 | 是否跨措辞复现 | 模板复用 | 强制门 | Tables 1/2 |
| 每组八频带 | 信号位于组内哪里 | 无 rank 身份 | H4 | Figure 3 |
| 256 随机 16 维方向 | 真频带是否特殊 | 任意方向 | H4 falsifier | Figures 3/5 |
| 三个特征值 floor | tail 是否数值放大 | 极小特征值 | 数值门 | Table 3 |

## 10. Primary Metric

对 $g\in\{c,f\}$：

$$
C_{\ell h}^g=\log\frac{D_{\ell h}^g}{D_{\ell,full}^g},
$$

$$
T_g^{fixed}=\operatorname{median}_{\ell=1:35,h}C_{\ell h}^g,
\qquad
K_g^{fixed}=\max_{\ell=1:35,h}C_{\ell h}^g.
$$

block 36 单列。每个随机分组计算同样的 $T_g^{(r)}$ 和 $K_g^{(r)}$。只有固定统计超过随机 q95，且 confirmation 上固定减随机 q95 的 nested-bootstrap 95% 下界大于零，才 Pass。$C^{rel}$ 同理。

若候选组的 $D^f$、$D^c$ 或任一 $W$ 低于预注册置换/数值 floor，则不能通过。mean 必须报告，但不代替 median/max verdict。

## 11. Required Raw-Variance And Secondary Metrics

每个层×组×粒度都必须输出：

- $\operatorname{tr}(B)$、每方向原始方差 $v$；
- 能量份额 $s$ 和相对均匀 $1/32$ 的 $\log(32s)$；
- $\operatorname{tr}(W)$；
- $D^c,D^f,R,C^c,C^f,C^{rel}$；
- 能量 Gini/HHI；
- 完整表征对应量；
- 组内 F1--F8 的 $b/q/j$ 和细减粗；
- 完整 4096 维按相对 rank 切八个 512 维带，只作描述性对照；
- 早层 1--12、晚层 25--35、block 36 摘要。

### 11.1 必须生成并审核的热力图合同

**Figure 0：covariance 谱审计。**在归一化 rank 上画完整 4096 维 MLP 输入和代表性 128 维组的特征值曲线，标出 F1--F8；另画 layer × normalized-rank 的 log 背景方差热力图。它验证谱和分带几何，不表示语义区分度。

**Figure 1：原始语义方差分配热力图。**按站点分面；行是 block 1--36，列是真实 H1--H32 或 MLP G1--G32；子面板为粗 $v$、细 $v$、粗 $\log(32s)$、细 $\log(32s)$。$v$ 的 colorbar 是 activation²/方向；$\log(32s)>0$ 表示超过均匀的 1/32 能量份额。

**Figure 2：决定性单元对完整表示区分优势热力图。**两个站点分别画 layer×unit 的 $C^c$、$C^f$、$C^{rel}$；正色表示单元高于本站点完整表示。只有超过 confirmation 区间和全局随机分组最大值的 cell 才标星。

**Figure 3：层 × 八频带热力图。**两个站点分别对典型单元与 discovery 固定的最佳单元画 F1--F8，显示 coarse/fine 的 $b$、$j$ 和 fine-minus-coarse $j$；只有超过同单元随机 16 维方向 q95 的真实带才标星。

**Figure 4：完整表示、平均、典型和最佳组的层深轨迹。**横轴为 block，纵轴显示 $D^c$、$D^f$、$R$ 或对应组优势；线为 full、mean、median、selection-corrected max，block 36 单列。它区分广泛集中与少数峰值。

**Figure 5：两站点相对随机分组的校准图。**逐层显示真实头或固定连续组的 median/max 与各自 1,024 个随机分组包络，并把两站点的标准化超额集中并列。

所有图必须从源 CSV 重算、实际打开，并检查轴、单位、colorbar、动态范围、block 36 和星号含义。

## 12. Known Good / Known Bad / Known Confusing Cases

- **Good：**32 组拼接精确重建 $m_\ell$，组 $B/W$ trace 求和等于完整 trace。
- **Bad：**把 MLP 输入切片称为注意力头。
- **Bad：**没有随机最大值零假设就声称最佳组更强。
- **Confusing：**高 $R$ 可能只是粗 $D$ 很小；必须同时读绝对粗/细 $D$。
- **Confusing：**原始能量更少但区分度更高，可能只是类内干扰更少。

## 13. Stage-Level Profiling Plan

| 阶段 | 局部问题 | 通过条件 | 交付 |
| --- | --- | --- | --- |
| S0 | provenance 是否冻结 | hashes 精确 | manifest |
| S1 | hook 是否是真 MLP 输入 | 36 层 equality/shape/replay 全过 | tensor audit |
| S2 | 语义提取是否完整 | 每条记录一次 | extraction manifest |
| S3 | 组统计是否重建完整统计 | 能量与 trace 守恒 | reconstruction table |
| S4 | 固定组是否超过随机分组 | H1--H3 typed verdict | null tables |
| S5 | 合格信号位于哪一谱带 | H4 typed verdict | stability tables |
| S6 | 图是否忠实显示注册量 | 实际打开视觉审计 | visual checklist |

## 14. Algorithm Specification

- **输入：**冻结模型、两套语义 manifest、calibration manifest、MLP pre-hooks、固定 selector、冻结随机 seeds。
- **参数提案：**32 组、128 维/组、8 带、16 维/带、2,000 nested bootstraps、5,000 标签置换、1,024 随机通道分组、256 随机组内方向、三个 eigenvalue floors。
- **步骤：**一次提取全部 $m_\ell$；算完整/组 $B/W$；做守恒；计算固定/随机 $C$；只用 calibration 拟合组 covariance；算八带 $b/q/j$；confirmation 推断；作图并打开审计。
- **停止：**任一强制门失败。
- **禁止：**删不利组/层/概念、看结果后减弱零假设、把通道组改称 heads。

## 15. Success / Failure / Insufficient Evidence

- `typical_group_concentration_pass_<coarse|fine|both>`：median 条款通过；
- `sparse_group_concentration_pass_<coarse|fine|both>`：max 通过、median 未通过；
- `_fine_relative_pass`：$C^{rel}$ 通过；
- `_spectral_pass`：H4 在已通过集中门的组中通过；
- `channel_group_concentration_fail`：所有门通过但固定组不超过随机组；
- `insufficient_<guard>`：任一强制门失败。

只有 raw 能量集中时，只报告能量分配；只有区分度异质但不超过随机分组时，只报告描述性异质性。

## 16. What This Cannot Claim

不能声称固定通道组是注意力头、神经元模块、语义电路或 Router 坐标；不能证明删除该组会因果损害语义；不能外推跨模型通道身份；不能说 covariance rank 产生粗细语义；不能说它改善专家效用、NLL 或训练效率。

## 17. Block Confirmation Ledger And Review Notes

| Block | 状态 | 决策 |
| --- | --- | --- |
| A 问题/边界 | CONFIRMED | 真 MLP 输入；固定通道组集中，不是单注意力头 |
| B 数据 | CONFIRMED | 精确复用 A15_02_E01 数据；同 taxonomy 封存模板确认；外部 taxonomy 不进入主裁定 |
| C 任务 | CONFIRMED | 同状态的粗/条件细变量；raw variance + discriminability |
| D 模型/对象 | CONFIRMED | 36 个 MLP 输入；G1--G32；每组八带 |
| E 优化 | CONFIRMED | 冻结 Qwen，无训练 |
| F 比较/证据 | CONFIRMED | 两站点 full/fixed/random；median/mean/max；Figures 0--5 |
| G 执行 | CONFIRMED | 两个独立 ACP 单节点作业；每个 `5090-8-spot`、8 GPU、spot，分别执行 attention 与 MLP 分支 |

Cross-block consistency：PASS。A--G 已全部确认。研究者于 2026-08-05 授权实现、smoke、两个 full、结果分析、实验文档和 `daily_research_reports/backup/2026/08/0805/focus.md`；未授权 graph、commit、push 或外部同步。

## 18. Execution Closure

- attention job：`om-y32ahxua`，完整提取有效，修复后 verdict=`attention_sparse_concentration_pass`；
- MLP job：`om-vjowli0r`，完整提取有效，修复后 verdict=`mlp_concentration_fail`；
- cross-site：最大值 attention 胜出；median 不支持 attention 普遍优势；
- H4：固定八频带未超过随机 16 维方向，Fail；
- 正式结果入口：[summary_cn.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_03_E01_architectural_head_channel_concentration/summary_cn.md) 与 [detailed.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_03_E01_architectural_head_channel_concentration/detailed.md)。
