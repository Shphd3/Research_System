---
anchor_id: 15_02_03_architectural_head_channel_concentration
status: completed_attention_sparse_pass_mlp_and_band_fail
canonical_language: en
companion_language: zh
parent_anchor: 15_02_layerwise_representation_spectral_atlas
updated: 2026-08-05
---

# A15_02_03 MLP 输入固定通道组与真实注意力头的粗细语义集中性


## 1. Problem Definition

唯一决策问题是：

> 在冻结 Qwen3-8B 中，粗粒度或细粒度语义区分度是否更集中在 `o_proj` 前的真实注意力头中，而不是经过 `o_proj`、残差与 RMSNorm 后的固定 MLP 输入通道组；两者是否分别超过自己的同形状随机通道分组？

令 \(m_\ell\in\mathbb R^{4096}\) 为 post-attention RMSNorm 输出，也就是该 block MLP 的直接输入。按原生通道顺序固定切成 32 个连续 128 维组 \(G_1,\ldots,G_{32}\)。这些组只是分析坐标，不是注意力头或模型中的独立模块。

本 Anchor 对两个站点使用相同的原始类别间方差、相对类内措辞变化的语义区分度、32×128 随机划分校准和单元内 covariance rank 定位；不回答因果计算、Router 效用或训练收益。

## 2. Physical Priors

1. 多头混合、残差相加和 RMSNorm 之后，原生通道上的语义信号与干扰仍可能不均匀分布。
2. 一个组即使包含更少的总语义能量，只要去除了更多类内干扰，也可能具有更高的类别间/类别内比值。
3. 连续通道编号没有天然模块身份；固定分组必须超过相同大小的随机通道重分组，才有资格称为特异集中。

## 3. Falsifiable Hypotheses

**主假设，通道组集中：**在未触碰的语义证据上，固定 128 维通道组对粗语义和/或细语义产生超过随机通道分组的区分度集中；典型组效应和经选择校正的最佳组效应分别裁定。

**频谱定位条款：**在通过集中性门的组内，粗细语义具有跨 calibration split 稳定、并超过同组随机 16 维方向的八频带画像。

**最强 rival：**因为完整区分度本来就是各组区分度的加权平均，所以任意 32 组中都必然有一组高于完整表示；观察到的最大值和频带峰值只是分组与选择效应。

**Pass：**固定分组在独立确认数据上至少对一种语义粒度超过随机分组零假设，并通过能力、区间、多重比较与稳定性门；典型集中和稀疏最佳组分别给出 typed verdict。

**Fail：**所有有效性门通过，但固定分组对两种粒度都不能区别于随机分组；或没有组内频带超过随机方向。

**Insufficient：**MLP 输入 hook、语义能力、确认边界、covariance 重建、数值 floor、随机零假设或基底稳定性任一强制门失败。

## 4. Mathematical Model

对语义粒度 \(g\in\{c,f\}\)，令 \(B_\ell^g\) 和 \(W_\ell^g\) 分别为完整 MLP 输入的类别间 covariance 与类别内 covariance。\(S_h\) 选取 \(G_h\) 的 128 个坐标：

\[
x_{\ell h}=S_hm_\ell,
\qquad
B_{\ell h}^g=S_hB_\ell^gS_h^\top,
\qquad
W_{\ell h}^g=S_hW_\ell^gS_h^\top.
\]

每方向原始类别间方差与能量份额为

\[
v_{\ell h}^g=\frac{\operatorname{tr}(B_{\ell h}^g)}{128},
\qquad
s_{\ell h}^g=\frac{\operatorname{tr}(B_{\ell h}^g)}{\operatorname{tr}(B_\ell^g)}.
\]

它们满足 \(\sum_hs_{\ell h}^g=1\)，且 32 个 \(v\) 的平均严格等于完整表示的每维原始方差。因此平均原始方差只用于能量守恒；集中性要看组间分布、最大份额及随机分组对照。

区分度为

\[
D_{\ell h}^g=
\frac{\operatorname{tr}(B_{\ell h}^g)}
{\operatorname{tr}(W_{\ell h}^g)+\epsilon},
\qquad
D_{\ell,\mathrm{full}}^g=
\frac{\operatorname{tr}(B_\ell^g)}
{\operatorname{tr}(W_\ell^g)+\epsilon}.
\]

忽略数值 ridge 时，\(D_{\ell,\mathrm{full}}^g\) 是各组 \(D\) 按类内方差加权的平均，所以 \(\max_hD_{\ell h}^g\ge D_{\ell,\mathrm{full}}^g\) 是代数必然。真正的决策量是相对完整表示、且相对随机分组校准的组优势：

\[
C_{\ell h}^g=\log\frac{D_{\ell h}^g}{D_{\ell,\mathrm{full}}^g},
\quad
C_{\ell}^{\mathrm{typ},g}=\operatorname{median}_hC_{\ell h}^g,
\quad
C_{\ell}^{\max,g}=\max_hC_{\ell h}^g.
\]

按研究者要求同时报告算术 mean，但不把它与 median 或 max 合并解释。细相对粗的集中为

\[
R_{\ell h}=\log\frac{D_{\ell h}^f}{D_{\ell h}^c},
\qquad
C_{\ell h}^{\mathrm{rel}}=R_{\ell h}-R_{\ell,\mathrm{full}}.
\]

独立自然语料为每个组定义 \(\Sigma_{\ell h}^{\mathrm{bg}}=U_{\ell h}\Lambda_{\ell h}U_{\ell h}^\top\)。128 维严格切成八个连续 16 维等秩带：F1=head，F2--F5=middle，F6--F8=tail。逐带报告每方向实际语义方差 \(b\)、相对背景方差的 \(q\)、相对类内噪声的区分度 \(j=B/W\)。

## 5. Computational Realization

冻结 `/data/share/Qwen3-8B`（36 blocks、hidden size 4096、bfloat16 forward）。在每个 block MLP 上注册 pre-hook，读取共同 `Classification:` 冒号位置的精确 post-attention RMSNorm 输出。只在最后一维按原生顺序切 `G1--G32`；拼接后必须精确重建完整张量。

精确复用经审计的 8 父类 × 每类 8 子类 × 每子类 8 描述语义立方，以及独立 128 篇 DCLM、65,536 token calibration。同一 taxonomy 内模板 1--2 为 design、模板 3--4 为封存 confirmation；它能够裁定当前两站点比较，但不能建立跨 taxonomy 普遍性。Qwen 不接收梯度。

随机分组对照将 4096 个原生通道随机置换后重新切成 32×128；同维 Haar 子空间作为次级方向对照。所有随机 seed、分组次数、阈值和 confirmation manifest 在打开结果前冻结。

## 6. Minimal Falsification Tests

1. 全部 36 个 block 的 MLP pre-hook replay、shape、组拼接和层身份通过。
2. 完整 MLP 输入对粗语义与条件细语义均超过层级标签置换 q95，才解释内部组差异。
3. 32 组精确重建原始语义能量；组级与完整 \(B/W\) trace 和直接计算一致。
4. 固定分组的典型值与最大 \(C\) 都同相应随机 32×128 分组统计比较；最大值零假设覆盖全部注册层与组。
5. 模板 1--2 只允许发现和排序，模板 3--4 裁定当前同 taxonomy 的站点比较；跨 taxonomy 普遍命题仍需独立数据复现。
6. 组内谱带结论必须通过 calibration half-split、三个特征值 floor 和同组随机 16 维方向。
7. 用父类→子类→模板 nested bootstrap、四模板方向和父类留一保护统计单位，不能把句子伪装成独立语义类。

## 7. Current Evidence

A15_02_03_E01 已完成。全部 hook、重放、能力、calibration、标签置换与数值守卫通过。

- 真实注意力头的最大粗、细和细相对粗 \(C\) 分别为 3.221、1.045、2.544，均超过随机通道分组全局最大 q95；对应 bootstrap 下界也通过，故为稀疏最大值 Pass。
- 注意力头中位 \(C\) 分别为 -0.022、-0.067、-0.026，均未通过，故“多数头更有区分力”Fail。
- MLP 固定组最大 \(C\) 分别为 0.877、0.624、0.945，均低于随机最大 q95，故固定原生通道组集中性 Fail。
- 经各站点随机零假设校准后，attention-minus-MLP 最大优势在三项指标上均为正，配对区间不跨零；中位数不支持 attention 普遍优势。
- 通过集中门的 attention 候选单元中，没有固定 F1--F8 超过随机八个 16 维子空间最大 q95，故组内八带特异性 Fail。

结果：[中文摘要](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_03_E01_architectural_head_channel_concentration/summary_cn.md)；[完整证据](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_03_E01_architectural_head_channel_concentration/detailed.md)。

## 8. Claim Boundary And Next Decision

本 Anchor 已建立：当前 taxonomy 中少数真实 pre-`o_proj` attention heads 具有超随机语义集中，而固定 MLP 输入组和固定头内八频带没有获得坐标特异性。它不能把稀疏关联升级为因果语义电路、跨 taxonomy/模型头身份、Router 适用性或训练收益。

**唯一下一决策：**在一个独立、无标签泄漏的平衡 taxonomy 上复现 selection-corrected attention 最大值，并检验通过单元的层/头身份是否跨 taxonomy 稳定；只有复现才进入专家反事实效用或 Router 训练。
