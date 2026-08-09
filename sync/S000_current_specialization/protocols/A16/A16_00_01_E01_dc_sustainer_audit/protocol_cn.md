---
experiment_id: A16_00_01_E01_dc_sustainer_audit
legacy_experiment_id: A15_00_E04_vanilla_centered_lb_dc_audit
anchor_id: A16_00_01_dc_sustainer_boundary
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-09
design_frozen_at: 2026-08-09-v1
experiment_role: root-cause audit
---

# Protocol：A16_00_01_E01 DC 维持因素审计

## 0. Approval Snapshot

- **文档状态：** `APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL`。
- **区块审计：** A--G 均 `CONFIRMED`，跨区块一致性 `PASS`。
- **目的：** 判断 token 共享的 Router 输入均值是否即时造成 Vanilla 深层硬路由集中，并降低共同负载均衡（LB）目标的局部纠正能力。
- **主 Anchor：** [A16_00_01](/Projects/from-attention-to-search/main/problem_anchors/16_load_control_gradient_interference/16_00_switch_lb_gradient_conflict/subanchors/16_00_01_dc_sustainer_boundary_anchor_cn.md)。
- **处理与对照：** 冻结 Vanilla 去独立均值；冻结 Centered 加回 running center；比较原生路由、错误层平移和 256 个确定性匹配随机平移。
- **唯一改变：** 离线重放中的常数 Router 输入/logit 分量。
- **固定：** 模型参数、Gate、专家、token、文档顺序、检查点、层、Router load bias 与数值分析路径。
- **主指标：** 注册 layer-3/layer-4 检查点单元上“最忙专家占比”的聚合变化。
- **Pass：** Vanilla 去均值和 Centered 加回中心两个方向都为正，文档配对 95% 下界大于零，且超过匹配随机 q95。
- **Fail：** 两个方向都不通过；单方向结果分别记为 `necessary_only` 或 `sufficient_only`。
- **Insufficient：** 任一必要检查点、数据、重放、确定性或产物守卫失败。
- **批准范围：** 文档、实现、本地 smoke、完整冻结测试、分析、图片和结果记录。
- **不能声称：** 累计训练因果、语言模型收益、最佳 LB 系数或普遍 Router 机制。

## 1. 术语解释

- **去中心前 Router 来源 $h$：** sparse MLP 在可选 running-center subtraction 之前收到的真实 `gating_reference`。
- **DC/公共分量：** 在固定 statistics token 之间不变的向量；只有专家相对 logit $C_EW\mu$ 会影响 top-1。
- **最忙专家占比 $M$：** 八个硬 top-1 token 占比中的最大值；$0.125$ 是理想均匀，$1$ 是全部进入一个专家。
- **归一化路由熵 $H$：** 硬专家选择熵除以 $\log 8$；$1$ 均匀，$0$ 单专家。
- **LB 数值：** $8\sum_e f_e\bar p_e$；均匀时为 $1$，完全一致的单专家状态接近 $8$。它是惩罚值，不等于实际改变路由的能力。
- **LB logit 梯度杠杆：** 解析样本归一梯度 $8p_{t,j}(f_j-\sum_e f_ep_{t,e})$ 的 RMS；只描述局部 logit 压力，不包括 LM 梯度、AdamW moment 或上游 Jacobian。
- **随机平移零假设：** 256 个确定性各向同性输入方向，按专家相对 logit 偏置范数匹配真实平移。

## 2. Anchor Alignment

父实验已经确定：相同 $\lambda_{LB}=0.01$ 下，Centered-Full 的专家使用远比 Vanilla 广。本实验只测 Anchor 中的即时 DC-offset 条款，不重开 10B/30B 性能裁定，也不修改正在运行的训练。

## 3. Tested Hypothesis

主假设是双向的：真实公共分量是冻结 Vanilla 坍缩的必要因素，并足以破坏冻结 Centered。预期签名是两个方向都出现超出随机平移的、跨文档稳定的硬负载变化；Vanilla 去中心后还应从“高 LB 惩罚、低梯度杠杆”转向较低惩罚和较高杠杆。

## 4. Rival Explanations

1. **已学习状态解释：** Gate 权重或 residual 已编码坍缩，减均值不能恢复。
2. **任意平移解释：** 任意同幅常数平移都会改变路由，真实中心并不特殊。
3. **只影响训练路径：** Centered 训练产生了不同 $W$/表征，加回中心也不再集中。
4. **指标解释：** max share 改变，但熵、margin 与主导专家身份不一致，只能给出有边界证据。

## 5. Data Construction And Provenance

不可变数据为
`/data/250010109/MoE_Router/experiments/20260802_a15_01_04_progressive_band_source_2b_5090/artifacts/eval_tokens.pt`，SHA-256 为 `5c8cca2b0821f25b8e7abc50d7653dfba8d71e9ccf167fee61b82624116a52e4`。

- statistics：`wos[0:512,:128]`，65,536 token，SHA-256 `6dd7b83df791c75dd62307b4256acc9d399ed2df8df32ef79e68cb0fb16b930f`；
- validation：`dclm[0:1024,:1024]`，1,048,576 token，SHA-256 `91acad820e5521832a4e54033fd062d4d275819856725d9803981c0c972a289c`；
- statistics 只拟合均值，validation 只产生判断指标；独立单位是一篇验证文档。

## 6. Learning Task And Permitted Supervision

没有训练或预测任务。唯一拟合量是冻结 statistics 激活的逐层无监督均值；validation 指标、专家标签和损失都不得影响均值、对照、检查点或裁定规则。

## 7. Model / Architecture And Frozen Variants

使用已有四 block、hidden 768、8 个 sparse expert、1 个 shared expert、top-1 的 Qwen3 MoE。只测 seed 17，因为 20B 属于注册的单 seed 30B 续训。两个 arm 为 `vanilla_full: z=Wh` 与 `centered_full: z=W(h-c)`。Gate 线性且无 bias；反事实不运行专家。

## 8. Training Objective And Optimization

本实验不优化。两个来源训练都从 step 0 使用相同目标：

$$
L=L_{LM}+0.01L_{LB}.
$$

它只说明问题背景，不在本实验重新估计。

## 9. Conditions, Seeds, And Checkpoints

检查点为 step `0,64,127,318,636,1272,12716,25432`，约对应初始化、50M、100M、250M、500M、1B、10B、20B token。step 0 只作诊断；主聚合使用其余七个检查点和 layer 3--4。

条件包括：Vanilla 原生 raw 与减 WOS 均值；Centered 原生 centered 与加回检查点中心；两个 DC-only；循环错误层平移；256 个按 $\|C_EWd_{true}\|_2$ 匹配的随机平移。随机种子固定为 `20260809 + 1009*step + 97*layer + arm_offset`。

## 10. Primary Metric And Frozen Analysis Plan

在每个固定单元池化验证文档的硬专家计数并计算 $M$：

$$
\Delta_V=M_{Vanilla,raw}-M_{Vanilla,centered},\qquad
\Delta_C=M_{Centered,raw}-M_{Centered,centered}.
$$

正值支持机制。主 estimand 是 14 个注册单元的等权平均。2,000 次 bootstrap 使用同一批 1,024 文档索引配对重采样，再重算所有单元和聚合量。256 个随机编号分别跨相同单元聚合，其 q95 是方向零假设阈值。

- 两方向都满足“95% 下界 $>0$ 且点估计 $>$ random q95”：`pass_bidirectional_dc_support`；
- 仅 Vanilla：`necessary_only`；
- 仅 Centered：`sufficient_only`；
- 均不满足：`fail_no_bidirectional_dc_support`；
- 缺失或守卫失败：`insufficient_*`。

全部 arm/checkpoint 的原生重放与均值产物完成后才解封分析。

## 11. Secondary Metrics And Guards

逐单元报告路由熵、top1-top2 margin、route flip、LB 值、解析 LB 梯度 RMS、降低赢家 margin 的下降方向、DC-only 主导专家、DC 对原生 margin 的支持比例，以及 Centered 独立均值与 running center 的范数/cosine。它们只能解释，不能替代主裁定。

硬守卫包括：检查点 step/载荷/source receipt、数据 hash、BF16 原生 winner 精确重放、FP32 agreement 报告、控制确定性、有限数值、完整 32 个含 step-0 的 arm/checkpoint 单元，以及可重建的表/数组/图源。

## 12. Known Good / Known Bad / Known Confusing Cases

- known-good：10B/20B Vanilla layer 3/4 应重现接近单专家，Centered 应重现较广使用；
- known-bad：Centered 中错误符号的中心必须使原生精确重放测试失败；
- confusing：step 0 中心为零或未训练，不进入主聚合；随机平移也可能偶然强烈改变负载，因此真实效应必须超过 q95。

## 13. Scientific Procedure And Stage Contracts

S0 核对文件/hash/shape；S1 用字面合成 logits 先红后绿测试计数、LB 导数、匹配随机方向与 bootstrap；S2 对两个 arm 的 step 0/127 做小 smoke；S3 提取全部冻结证据；S4 按注册规则推断；S5 打开图片并完成证据链。S0--S2 失败时只修工程实现；任一 S3 主单元缺失则判 Insufficient，不能删除。

## 14. Algorithm, Output, And Provenance Contract

worker 代码位于 `/data/250010109/MoE_Router/experiments/20260808_online_spectral_router_30b_v2/`；原始输出位于 `/data/250010109/MoE_Router/outputs/online_spectral_router_training/analysis/A15_00_E04_vanilla_centered_lb_dc_audit/`。该 worker 路径保留完成运行时的旧 A15 编号；A16 所有权迁移不重命名不可变原始产物。主线只接收 Protocol、summary、detailed、策展 CSV 和审核图片，不复制 checkpoint、原始激活或完整日志。

必须保存 manifest、逐单元 JSON/压缩文档计数、聚合与单元 CSV、bootstrap/null 数组、typed verdict、plot contract、图片与 smoke/full receipt。Aggregator 遇到缺失单元必须拒绝聚合。

## 15. Success / Failure / Insufficient Evidence

裁定严格使用第 10 节。Pass 只支持这些冻结模型中的即时 DC 机制；`necessary_only` 表明 DC 维持 Vanilla 坍缩但 Centered 的训练状态使加回不足；`sufficient_only` 表明中心可破坏 Centered，但 Vanilla 坍缩不能由独立均值去除；Fail 转向 Gate/residual 或梯度反馈机制。

## 16. What This Cannot Claim

即使 Pass，也不能说 DC 是历史唯一原因、centering 改善所有 MoE、$0.01$ 天生太小、提高系数安全，或任何 Router 变化会改善 held-out NLL。离线反事实不执行专家，不能测 Router--Expert 反馈或专业化。

## 17. Block Confirmation, Freeze, And Amendment Ledger

A--G 均由用户的测量认可、Centered 对照要求和直接执行授权明确确认；数据、模型、目标与代码来源均已核验。跨区块一致性 `PASS`。科学正文在实现前冻结为 `2026-08-09-v1`。执行开始后的任何实质变化只能追加 amendment，写明前后值、原因、是否已见结果、影响区块、批准与证据资格。

## 18. 追加式 Amendment Ledger

### A1 — 补齐两项已注册的次级诊断

- **时间：** 2026-08-09，首次解封主分析之后。
- **修改前：** 第 11 节要求 route flip 与 DC 对原生赢家 margin 的支持量，但第一版完整提取器没有持久化这两个字段；主裁定所需的逐文档计数与随机零分布均已完整。
- **修改后：** 新增

  $$
  F_{flip}=\Pr[\arg\max z_{deployed}\ne\arg\max z_{treatment}]
  $$

  以及对原生赢家 $w$、第二名 $r$、原生 margin $m$ 和真实 DC logit 偏置 $d$ 的

  $$
  q_{DC}=\frac{d_w-d_r}{m+10^{-12}}.
  $$

  同时报告 $d_w-d_r>0$ 的 token 比例、平均支持量和 $q_{DC}$ 中位数。Vanilla 使用 $d=W\mu_{WOS}$，Centered 使用 $d=Wc$。
- **原因：** 补齐已批准的次级指标；假设、处理、数据、检查点、主指标、零假设与阈值均未改变。
- **是否已见结果：** 已看到 `necessary_only` 主裁定。
- **影响区块：** 只影响 G 的次级诊断与输出 schema；A--F 和 typed verdict 不变。
- **批准：** 用户已明确要求完成认可的测量，并允许在首轮结果后继续完善解释指标。
- **证据资格：** 这些是解封后补齐的次级解释量，不能改变注册裁定。实现前单测失败、实现后通过；随后重提取全部 16 个单元。主数组 SHA-256 未变，点估计、区间、随机 q95 与 typed verdict 均精确复现。

### A2 — 从 A15 迁入 A16 的管理性变更

- **时间：** 2026-08-09，结果完成之后。
- **修改前：** 该实验和所属子 Anchor 使用 `A15_00_E04` 与 `A15_00_02`，因为负载失败最初由频谱路由训练暴露。
- **修改后：** 不变的证据由 `A16_00_01_E01` 与子 Anchor `A16_00_01` 所有；不可变 worker 产物保留旧 A15 路径，策展元数据同时记录新旧编号。
- **原因：** 把负载控制证据归入新 A16 研究线，同时避免复制或重写已完成实验。
- **是否已见结果：** 全部结果已经公开。
- **影响区块：** 仅编号、链接和所有权；假设、条件、指标、零假设、数值、图片与裁定均不变。
- **批准：** 研究者明确批准把已有负载均衡 Anchor 与训练证据迁入 A16。
- **证据资格：** 不变。
