# Meeting Brief: A07_E01 High-Dimensional Uniform Centered-M4

## Question

Core question:
二维里中心化 M4 可以严格 50/50；高维均匀 feature 下，centered/calibrated M4 是否还能接近均匀分发，并保留非零专家偏好？

Why it matters to the mainline:
如果高维均匀情形都不能解释，后续 real-text hidden states 和 trainable router 初始化就没有清楚的静态目标。

Current subproblem:
比较 raw M4、centered M4、calibrated M4、weighted top-r proxy。这里的“专家偏好”只表示被选 expert 的分数更高且 margin 不太小，不表示语义或真实任务收益。

## Conclusion

One-sentence summary:
Centered/calibrated M4 是当前高维静态目标；raw M4 被削弱；top-r 是 rank-dependent 近似，不是天然足够。

1. raw M4 在高维随机/各向异性谱下严重偏载，因为平均 expert 能量差会主导负载。
2. centered M4 明显改善负载，但高维不保证精确 50/50；spiked spectrum 会按预期失败。
3. calibration 能把负载拉回接近 50/50，但必须同时读 margin；near-identical experts 仍然是低信心。

## Setup

Input是什么？

Expert是什么？

Distance是什么？

Uniformity怎么定义？



Data / task:
输入是 $x\sim\mathrm{Unif}(S^{d-1})$，$d=2,4,8,16,32,64,128,256,512$。每个 condition 100 seeds，每个 seed 20,000 eval samples，5,000 calibration samples。

Model / router:
两个 experts，通过 $G_e=A_e^\top A_e$ 定义静态分数；没有训练。

Comparison:
raw M4: $q_e=x^\top G_ex$。centered M4: $q_e=x^\top G_ex-\mathrm{tr}(G_e)/d$。calibrated M4: 用 calibration split 拟合阈值。weighted top-r proxy: 只用前 r 个谱方向的加权近似。

Primary metric:
先看 load error，再同时读 mean margin、low-margin fraction、退化比例和谱分散指标 $r_3$。

Important omission:
`random_gaussian` 是快速 Gaussian-like spectrum proxy，不是 exact dense Gaussian matrix eigendecomposition。因此它支持谱机制判断，但不能作为精确随机高斯矩阵定理证据。

## Key Evidence

1. **Raw M4 被削弱**
   Evidence:
   $d=512$ random Gaussian spectrum proxy / random anisotropic。
   Result:
   raw M4 load error = 0.4644 / 0.4556。
   Interpretation:
   raw M4 会被平均响应能量差强烈偏置，不适合作为均匀负载目标。

2. **Centered M4 有效但不是无条件定理**
   Evidence:
   $d=512$ centered M4。
   Result:
   random proxy load error 降到 0.0358；random anisotropic 降到 0.0574；balanced spectrum control 为 0.0029；spiked counterexample 仍为 0.1824。
   Interpretation:
   centering 是正确方向，但高维必须加谱分散条件或 calibration。

3. **Calibration 和 top-r 的边界**
   Evidence:
   $d=512$ calibrated M4 和 weighted top-r。
   Result:
   calibrated M4 load error 在 random proxy / random anisotropic 为 0.0070 / 0.0065；near-identical margin 只有约 0.0005。weighted top-r 在 random anisotropic 中 agreement 从 r=8 的 0.8004 升到 r=128 的 0.9322。
   Interpretation:
   calibration 是负载控制，不是专家偏好证明；top-r 需要足够 rank 才接近 full centered M4。

4. **A07_E02 semi-real text-like full run**
   Evidence:
   controlled hidden states with common direction, corpus slice, position, token-frequency, syntax, and latent utility factors。
   Result:
   mean-centered calibrated M4 load error = 0.0029、mean margin = 3.1910、agreement with full centered M4 = 0.9967；mean-centered weighted top-r=32 load error = 0.0048、agreement = 0.9832；M1/M2 prototype agreement 只有 0.4977 / 0.5460。
   Interpretation:
   semi-real hidden-state run 继续支持 empirical-centered/calibrated M4 和 weighted top-r≈32；prototype 仍只是 baseline。

## Boundary

This conclusion does not cover:

- 不证明 trainable router 会学到 centered/calibrated M4。
- 不证明 real text hidden states 服从 uniform sphere。
- 不证明 exact dense Gaussian experts 已完整审计。
- 不证明 load balance 等于语义专家特化或真实任务收益。

## Next Step

Full-run status:
A06_E01 已完成 full run；A07_E01 已完成 high-dimensional uniform full run；A07_E02 已完成 semi-real text-like hidden-state full run。尚未完成的是 true frozen-transformer hidden-state run，它现在是下一步而不是已完成结果。

Next decision:
执行 true frozen-transformer hidden-state version of A07_E02。

Next minimal experiment or action:
在真实 frozen transformer activations 上比较 empirical-centered M4、calibrated weighted low-rank M4、top-r proxy 和 prototype baselines；核心看 load、margin、与 full centered M4 的 agreement、common-direction sensitivity，以及需要多大 rank 才稳定。
