---
anchor_id: 15_00_02_gate_common_residual_preference
parent_anchor: 15_00_router_input_spectral_geometry
status: completed_pass_pooled_alignment_with_native_use
canonical_language: en
companion_language: zh
thinking_card: 15_00_02_gate_common_residual_preference_thinking_card_cn.md
updated: 2026-07-31
---

# A15_00_02 Gate 对 pooled common 与局部 residual 的偏好

Thinking Card 来源：
[研究者中文判断](15_00_02_gate_common_residual_preference_thinking_card_cn.md)。

## 1. Problem Definition

A15_00 已证明线性 Gate 对 pooled covariance head 有很强的等能对齐，但没有
区分该 head 是跨数据公共候选还是某个 calibration 样本的偶然方向。

**唯一决策问题：**

> 给每个方向相同输入能量后，decommon Gate 是否对独立 pooled
> centered-common candidate 产生比同维 shard-local residual 更大的专家间
> logit 增益和 native route dependence；这种偏好在 30k/40k/80k 如何变化？

本 subanchor 的直接对象是“pooled candidate vs local residual”。只有
A15_00_01 独立确认前者稳定、后者较不稳定后，联合解释才可写成“Gate 偏向
稳定 common”。

**主指标：**

$$
B_{\ell,P:L}
=\log\frac{G_{\ell,P}+\epsilon}
{\operatorname{median}_s G_{\ell,L_s}+\epsilon},
$$

单位为 log equal-energy gain ratio。它回答 Gate 权重偏向，不回答功能价值。

## 2. Physical Priors

1. **重复方向积累 prior。** 固定线性 Gate 更容易沿跨数据重复出现的方向累计
   一致权重；随 shard 旋转的方向，其更新可能平均抵消。
2. **能量不是选择性。** pooled top directions 的真实输入能量天然更大，必须
   使用完全去掉 covariance eigenvalue 的 $G$，不能用 raw response 判偏好。
3. **endpoint 由 $W$ 与 basis 共同决定。** checkpoint 间变化必须用固定 basis
   crossing 分离 Gate 权重变化和表示漂移。

## 3. Falsifiable Hypotheses

**H1——Gate 偏 pooled common candidate。** decommon 在 80k 的
$B_{P:L}$ 为正并超过保持 Gate 奇异值的 orientation null；40k 方向复现。
去除 pooled candidate 后，原生 winner 的 margin 支撑下降也大于同维 local
residual；route flip 只作辅助。LB 判断该现象是否跨谱系复现。

**最强 rival R0——只有能量差。** raw response 偏 pooled，但 $G$ 与
$B_{P:L}$ 不偏 pooled。

**R1——pooled estimator 特权。** 任何 pooled 同维方向、错误层 basis 或
orientation null 都得到相同偏好。

**R2——只有表征漂移。** endpoint $B_{P:L}$ 变化，但固定 basis 后
$W_{30/40/80}$ 没有相应变化。

**R3——稳定且有用。** Gate 的 pooled 偏好真实存在，但该方向承担共享功能；
本实验不能把这种偏好定性为好或坏。

**Pass：** decommon 主 endpoint 的 $B_{P:L}$ 和 native-margin 支撑对比都
支持 H1，40k 复现且 null/错误层护栏通过。

**Fail：** 有效精确结果支持 R0、R1，或 native route 对 local residual 的依赖
不弱于 pooled candidate。

**Insufficient：** A15_00_01 的稳定性结论可独立为 insufficient；本 anchor
仍可裁定 pooled-vs-local preference，但不得使用“稳定 common”联合解释。
若 actual-input、basis、route replay、checkpoint crossing 或 precision 护栏
失败，则本 anchor 自身 insufficient。

## 4. Mathematical Model

令 $\bar W_\ell=C_EW_\ell$，其中
$C_E=I-\mathbf1\mathbf1^\top/E$ 去除所有专家共有的 logit 平移。

在只用于 basis fit 的独立 pooled documents 上得到 $U_{\ell,P}\in
\mathbb R^{768\times64}$。对每个 shard $s$，先去掉 pooled projector，再在
剩余空间拟合局部 top-64：

$$
Y_{\ell,s}=X_{\ell,s}(I-U_{\ell,P}U_{\ell,P}^{\top}),
\qquad
U_{\ell,L_s}=\operatorname{TopSV}_{64}(Y_{\ell,s}).
$$

对任意 64 维 basis $U$，定义每方向等能 Gate 增益

$$
G_\ell(W,U)=\frac1{64}\|\bar W_\ell U\|_F^2.
$$

主指标 $B_{\ell,P:L}$ 比较 pooled candidate 与所有 local residual bases 的
中位增益。实际使用以 64 维去带后的 native-winner margin support 为主，
top-1 flip 只作辅助。

对 $a,b\in\{30k,40k,80k\}$ 计算 $W_a\times U_b$ crossing；固定 basis 的
Gate-weight effect 只说明保存区间的净变化，不等于逐步梯度因果。

## 5. Computational Realization

[已批准的 E01 中文 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_02_E01_gate_common_residual_preference/protocol_cn.md)
复用 A15_00_01 的 frozen actual-input cache、文档 split 和 64 维 bases，但
独立计算 Gate gain、route effect、orientation null 与 checkpoint crossing。

模型为现有 12-layer H768 decommon 与 LB 的 30k/40k/80k checkpoints；80k 是
主 endpoint，40k 是复现，30k 只帮助描述宏观形成状态。所有 12 层报告。

两份 E01 共享 S0 provenance 与一次激活提取，可并行执行分析；任何一个失败都
不会事后改变另一份的 estimator、数据或 metric。

## 6. Minimal Falsification Tests

1. 对 pooled candidate、每个 local residual 和 full/complement Haar-64 使用
   相同的 $G$、flip、margin 实现。
2. 以 256 个保持 Gate 非零奇异值的 orientation null 判断方向偏好；错误层
   pooled basis 排除任意层共享几何。
3. 在相同 held-out documents 上比较 equal-rank band ablation，禁止用 total
   energy 差解释 route effect。
4. 用完整 $3\times3$ checkpoint crossing 分离 $W$ 与 basis 漂移。
5. LB/decommon 分开裁定；二者不是 center/LB 的单变量因果对照。

## 7. Current Evidence

[E01 Protocol](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_02_E01_gate_common_residual_preference/protocol_cn.md)
已完成，裁定为 `pass_pooled_alignment_with_native_use`；见
[中文摘要](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_02_E01_gate_common_residual_preference/summary_cn.md)
与
[完整证据账本](/Projects/from-attention-to-search/main/experiments/A15/15_00_router_input_spectral_geometry/A15_00_02_E01_gate_common_residual_preference/detailed.md)。

40k/80k 时，pooled/local 的等能 Gate 增益比为 decommon 2.83/3.08、
LB 3.94/4.55；pooled 相对 local 多支撑的原生 winner margin 为 decommon
1.998/2.061、LB 1.873/1.953 logit/token。模型级区间均高于零，所有观测
$B$ 也远高于保持 Gate 奇异值的方向 null q95（约 0.06）。

LB 的逐层 gain 为 12/12 通过；decommon 为 11/12，第 12 层是明确例外，
因此 gain 结论是模型级。四个 endpoint 的 margin support 都是 12/12 层
为正。actual-input replay、同维、SVD、错误层、路由重放与数值护栏全部通过。

结合 A15_00_01，联合裁定为
`joint_pass_gate_prefers_transferable_centered_common`：在保留 endpoint，
Gate 更依赖跨文档迁移更强的 centered component，而不是迁移较弱的 local
residual。按研究者修订，30k 不进入结论。

## 8. Claim Boundary And Next Decision

A15_00_02 只建立当前 Gate 的等能权重几何和原生路由依赖。联合结果仍不建立
语义、专家兼容性、验证收益或 decommon 训练结果的因果解释。LB/decommon
差异只能描述，因为 centering、负载均衡与训练路径同时不同。

**唯一下一决策：** 是否正式设计联合 Pass 打开的稳定-vs-局部 residual 匹配
训练干预，以专家更新冲突与 held-out loss/FLOP 作为裁定结果。
