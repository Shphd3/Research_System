---
anchor_id: 15_00_01_cross_document_subspace_stability
parent_anchor: 15_00_router_input_spectral_geometry
status: completed_pass_energy_transfer_gap_projectors_shared
canonical_language: en
companion_language: zh
thinking_card: 15_00_01_cross_document_subspace_stability_thinking_card_cn.md
updated: 2026-07-31
---

# A15_00_01 去均值后的公共子空间稳定性

Thinking Card 来源：
[研究者中文判断](15_00_01_cross_document_subspace_stability_thinking_card_cn.md)。

## 1. Problem Definition

A15_00 已证明：给各方向相同输入能量后，训练后的线性 Gate 仍明显偏向 actual
Router input 的 covariance head；middle/tail 可见但较弱。尚未区分的是，
“去均值后的 head”究竟是跨数据复现的 centered-common 子空间，还是每批数据
各自不同的高方差方向。

**唯一决策问题：**

> 在不重叠 DCLM 文档组之间，去掉各组均值后的 top-64 子空间是否稳定迁移；
> 移除 pooled top-64 后，同维的组特异剩余子空间是否明显更不稳定？

这里的“稳定”只指一个数据组拟合的方向能解释另一未见数据组的中心化变化。
它不等于语义公共、专家功能公共或训练收益。

**主指标：** top-64 held-out cross-capture 相对同维 Haar q95 的差值
$\Gamma_{64}$，单位为 held-out activation-energy fraction。

**主证伪：** top-64 的跨组 capture 不超过 Haar/错误层，或正交剩余 top-64
与原 top-64 同样稳定。

## 2. Physical Priors

1. **平移不改变中心化 covariance。** 对冻结 checkpoint 的固定 center $c$，
   $\operatorname{Cov}(g-c)=\operatorname{Cov}(g)$。decommon 只直接删除
   mean/DC，不会自动删除 centered common variation。
2. **可学习坐标需要跨数据复现。** 若同一方向在独立文档组反复出现，统一 Gate
   可累积一致投影；若方向随组旋转，单一固定线性 Gate 只能学习其平均或更稳定
   的部分。
3. **有限样本 PCA 是强 rival。** 768 维下的局部子空间差异可能只是 token 数
   不足，因此稳定性结论必须随文档数收敛并超过方向零假设。

## 3. Falsifiable Hypotheses

**H1——稳定 centered-common + 不稳定局部剩余。** 去均值后的 top-64 在独立
文档组之间有正的 $\Gamma_{64}$；移除独立 pooled top-64 后，局部 residual
top-64 的 cross-capture 显著更低并落入或接近 matched null。

**最强 rival R0——只有估计噪声。** 原 top-64 与 residual top-64 都不能稳定
超过 Haar，且结果随文档数显著改变。

**R1——稳定结构比 64 维更宽。** 原 top-64 与正交 remainder 都跨组稳定；
此时不能称 residual 不稳定，只能说 centered-common 的维度大于注册的 64。

**R2——谱稳定但非功能。** H1 在几何上成立，但稳定方向与 expert utility
无关；本 subanchor 无权排除该 rival。

**Pass：** top-64 在 decommon 的 80k 主 endpoint 上稳定超过 matched null，
40k 方向复现，且同维 residual transfer 明显更低；LB 用于判断现象是否跨
谱系复现。

**Fail：** 有效且精确的测量支持 R0 或 R1。

**Insufficient：** actual-input replay、文档独立、sample-size、center
invariance、rank 或数值护栏失败。

## 4. Mathematical Model

对 layer $\ell$、文档组 $s$ 的 Router 上游表征，研究者机制可写成

$$
g_{\ell,s,t}
=\mu_\ell+U_{\ell,*}a_{\ell,s,t}+\epsilon_{\ell,s,t}.
$$

$\mu_\ell$ 是全局均值；$U_{\ell,*}$ 是待检验的跨组 centered-common
子空间；$\epsilon$ 是组特异剩余。actual Gate input 为
$r=g-c$，组内中心化后

$$
x_{\ell,s,t}
=r_{\ell,s,t}-\mathbb E_s[r_{\ell,s,t}]
=g_{\ell,s,t}-\mathbb E_s[g_{\ell,s,t}].
$$

令 $U_{\ell,s,k}$ 由 source shard 的 fit 文档估计。对 target shard 的独立
evaluation 矩阵 $X_{\ell,t}^{eval}$，

$$
E_{\ell,s\rightarrow t,k}
=\frac{\|X_{\ell,t}^{eval}U_{\ell,s,k}\|_F^2}
{\|X_{\ell,t}^{eval}\|_F^2}.
$$

主指标为

$$
\Gamma_{\ell,64}
=\operatorname{median}_{s\ne t}
\left[
E_{\ell,s\rightarrow t,64}
-q_{0.95}\!\left(E_{\ell,R_{64}\rightarrow t}\right)
\right].
$$

对独立 pooled basis $U_{\ell,*}$ 先投影掉
$P_{\ell,*}=U_{\ell,*}U_{\ell,*}^{\top}$，再在
$(I-P_{\ell,*})x$ 上构造同维局部 residual bases，得到
$\Gamma_{\ell,64}^{res}$。H1 的关键对比是
$\Gamma_{\ell,64}>\Gamma_{\ell,64}^{res}$。

## 5. Computational Realization

[已批准的 E01 中文 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_01_E01_cross_document_subspace_stability/protocol_cn.md)
使用现有 12-layer H768 LB/decommon checkpoints，直接 hook Gate 输入及
decommon 上游 $g$。主 endpoint 为 80k，40k 复现，30k 只作宏观轨迹支持。

使用新的、与 Q1/Q2 manifest 不重叠的 DCLM held-out documents，按文档 hash
冻结为八组；每组再分 fit/evaluation 文档。所有 12 层都报告，注册主维度
$k=64$，$k\in\{16,32,128,256\}$ 只用于判断维度与样本量敏感性。

该实验与 A15_00_02 共用一次冻结激活提取，但稳定性指标和 verdict 独立计算，
因此在明确授权执行后可以并行。

## 6. Minimal Falsification Tests

1. 同一 decommon checkpoint 上验证 $g$ 与 $r=g-c$ 的中心化 covariance
   数值一致；否则停止解释。
2. 在完整文档级 split 上计算 top-64 cross-capture，超过 256 个同维 Haar
   orientations 与错误层基底。
3. 在移除独立 pooled top-64 后，对 residual top-64 重复完全相同的检验。
4. 用 8/16/32 fit documents 的 sample-size curve 排除局部 PCA 噪声。
5. uncertainty 以文档组和文档 block bootstrap 计算，不把 token 当独立样本。

## 7. Current Evidence

[E01 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_01_E01_cross_document_subspace_stability/protocol_cn.md)
已完成，裁定为 `pass_stable_centered_less_stable_local_residual`；见
[中文摘要](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_01_E01_cross_document_subspace_stability/summary_cn.md)
与
[完整证据账本](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_01_E01_cross_document_subspace_stability/detailed.md)。

40k/80k 时，decommon 的 centered top-64 随机零假设校正后跨文档迁移量为
0.600/0.580，LB 为 0.584/0.564。独立去掉 pooled top-64 后，local
residual-64 仍明显超过匹配随机方向：decommon 为 0.414/0.402，LB 为
0.409/0.392。top 减 residual 的模型级差值分别为 decommon 0.179/0.176、
LB 0.162/0.167；四个 endpoint 的全部层均为正，配对 bootstrap 区间也均
高于零。

已注册的次级 projector overlap 进一步收紧了解释。40k/80k 的模型中位数为：
centered top-64 约0.760--0.791，residual-64 约0.704--0.730；匹配随机
q95 分别只有0.086与0.094。top 减 residual 的模型级 overlap 差只有
0.045--0.047，且部分层有例外。因此 residual 的能量迁移较弱，但 residual
projector 本身在随机文档 shard 间高度共享。

actual-input replay、center invariance、rank、样本量、Haar 与数值护栏全部
通过。各 shard 均值高度对齐，但裁定不依赖均值余弦。直接观察是分层稳定性：
centered top-64 跨文档迁移更强，local residual-64 也具有实质性迁移。

因此，“去均值后只剩彼此无关 residual”的强竞争解释被否定；“固定平移仍
留下能量集中程度不同的全局共享层级结构”的较窄解释得到支持。按研究者
执行修订，30k 不进入证据链。

## 8. Claim Boundary And Next Decision

A15_00_01 只建立跨文档统计迁移，不建立语义 common 或功能价值。它不能说明
residual 无用、稳定性差导致 decommon 的训练结果，或 pooled 成分应该保留/
删除。“local residual”也不等于随机噪声：它本身通过了迁移零假设。

当前 stable-hash shard 混合了 DCLM 条件，因此仍不能排除共享 residual
envelope 内部存在 condition-specific 低维模式。

**唯一下一决策：** 是否先按 domain/topic 构造条件化文档组，并以同条件
half-split 可靠性、projector overlap 与 cross-capture 完成冻结检验，再决定
是否进入匹配训练。
