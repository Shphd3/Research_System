---
anchor_id: 15_05_01_shallow_feature_guidance
legacy_anchor_id: 15_01_shallow_head_guided_deep_routing
parent_anchor: 15_05_functional_coordinate_admission
status: layer_band_profile_pass_compatibility_pending
canonical_language: en
canonical_file: 15_05_01_shallow_feature_guidance_anchor.md
thinking_card: 15_05_01_shallow_feature_guidance_thinking_card_cn.md
depends_on: 15_00_router_input_spectral_geometry
updated: 2026-07-31
---

# A15_05_01 浅层 covariance head 指导深层 Router

Thinking Card：[研究者方向已批准版本](15_05_01_shallow_feature_guidance_thinking_card_cn.md)。

## 1. Problem Definition

这是 A15_00 明确不回答的功能 sibling parent：

> 在控制深层 native Router 分数、负载、容量、参数、token 数和计算后，同一
> token 的浅层 head 坐标能否增量预测哪些 token 放入同一深层专家训练更兼容？

对 $k<\ell$，浅层 head 坐标为

$$
c_{k,H}(x)=U_{k,H}^\top(g_k(x)-\mu_k).
$$

它来自同一 token。没有注册的跨层 transport 时，不能直接用 $U_{k,H}$ 投影
$g_\ell$。

父 anchor 主指标是浅层 head 在线性深层分数和 nuisance controls 之外，对
独立 token 一步交叉更新兼容性的 held-out 增量预测。它判断功能准入，不直接
证明端到端收益。

## 2. Physical Priors

1. 浅层高方差因子可能较早形成稳定、低噪声的粗粒度 token cohort；
2. 高方差不等于兼容性，head 可能主要是公共、位置、长度或来源频次；
3. 跨层复用同一粗分区可减少抖动，也可造成过早锁定和专家功能重复。

## 3. Falsifiable Hypotheses

**H1：**独立 token 上，$c_{k,H}$ 在线性深层分数之外预测深层一步兼容性，并
超过同维随机和 token-shuffled 对照；通过该门后，浅层 head 指导改善匹配
计算的早期训练。

**最强 rival：**收益来自额外参数、边际尺度、负载变化或 token identity，
而非浅层 head 的谱和 token-specific 信息。

**Pass：**兼容性准入与匹配计算训练测试均通过，且负载/容量护栏有效。

**Fail：**模型 capable，但 shallow head 不能超过兼容性对照；或计算/负载匹配
后，训练收益不能同时超过 native 和匹配旁路对照。

**Insufficient：**注册变量没有稳定进入浅层 head、基础模型无能力、兼容性
估计不精确或路由护栏失败。

## 4. Mathematical Model

深层 score 为

$$
z_\ell(x)
=W_\ell g_\ell(x)+A_\ell c_{k,H}(x),
\qquad \ell>k.
$$

$A_\ell$ 是可训练辅助读出；$A_\ell=0$ 时原生路径仍可达。随机和 shuffled
条件使用相同张量形状与运算。

令 $Y_{ij}^{(\ell)}$ 是独立测得的 token 组一步交叉更新兼容性，准入量为

$$
\Delta_{\rm comp}
=\operatorname{Perf}(Y\mid s_{\rm native},c_{k,H},q)
-\operatorname{Perf}(Y\mid s_{\rm native},q),
$$

其中 $q$ 包含负载、范数、位置、长度和离群值对照。具体 performance score
由 Protocol 冻结。

## 5. Computational Realization

首个 subanchor 使用四层受控 MoE。第 1--2 层先形成稳定表示并冻结第二层 head
基底；真正普通的 native 四层模型与第 3--4 层接收 head、同维随机或 token-
shuffled 坐标的三种旁路模型比较。三种旁路使用相同辅助读出；全部四臂不使用
load-balance loss，并共享一个不反传的 expert-score bias 规则。informative 与
nuisance 两种任务分开“有用浅层结构”和“仅有大方差”。

## 6. Minimal Falsification Tests

1. 注册受控变量在第二层 head 中的 capture 超过随机，并在 nuisance 任务中
   不成为功能预测量；
2. 独立 token 组上，head 的兼容性增量必须超过 native、范数/离群值、random
   和 shuffled 后才进入联合训练；
3. 匹配累计 FLOPs，比较真正 native 四层模型，以及辅助参数、负载目标、容量、
   数据和 seeds 匹配的 head、random、shuffled；
4. 审计 margin、flip、load、专家更新冲突和专家功能重复，定位 loss 差异。

## 7. Current Evidence

A15_00 只证明训练 Gate 能强烈访问本层 covariance head，没有证明浅层语义或
深层兼容性。旧错误层基底对照削弱直接搬运基底，但没有测试向前传递同一 token
的浅层系数。

A15_05_02 的首个四层 pilot 因 head 与同维随机子空间都达到满分而在 Stage A
停止，不能裁定浅层指导。A15_02_01 随后使用未见组合能力有效、低样本且有随机
方向 q95 的任务，建立了更窄但可用的结果：组合训练使 L3/L4 的 F1/head 特异
携带一步中间状态，使 F2 特异保留粗条件；两种结果在 seeds 17/29 复现。完整
组合结果只在深层完整表征中形成，没有特异落入 H/M/T 的任一固定频带。

Gate 去带干预又显示原生 Gate 仍主要依赖 F1/head，而几乎不使用携带粗条件的
F2。这提供了候选层别坐标，但尚未提供共同训练兼容性或训练收益证书。结果见
[A15_02_01 summary_cn.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_01_E01_controlled_layer_information_profile/summary_cn.md)。

A15_05_03 随后显式训练了本层 H→M→T 和第一层频带 relay。前者最终比 native
差，后者在两套续训的 2B 终点都略好，但两种处理的全程 NLL AUC 都更差；relay
也只有 route regret 同向改善，专家效用离散度、冗余和冲突没有形成一致专业化。
因此固定频带日程能改变学习路径，却没有训练效率证书。见
[A15_05_03 summary_cn.md](/Projects/from-attention-to-search/main/experiments/A15/15_05_functional_coordinate_admission/A15_05_03_E01_progressive_band_source_routing_2b/summary_cn.md)。

## 8. Claim Boundary And Next Decision

本父 anchor 最多建立受控任务上的增量兼容性和匹配计算 pilot 效果；不能证明
自然语言普遍规律、大规模效率或 covariance head 就是领域语义。
当前 subanchors 已证明频带含义会随层重组，也证明显式频带日程会改变专家功能，
但仍没有提供兼容性准入或全程训练效率收益。
尤其不能把 F1=中间状态、F2=粗条件外推到自然语言，也不能因为一个变量可读就
认定深层专家应按它分发。

**唯一下一决策：**把 A15_02_01 中复现的层别功能坐标蒸馏成固定低秩读出，并
先测它是否在线性 native score 之外预测深层一步共同训练兼容性；只有超过同维
随机、token-shuffled 与错误层对照，才批准匹配计算的跨层指导训练。
