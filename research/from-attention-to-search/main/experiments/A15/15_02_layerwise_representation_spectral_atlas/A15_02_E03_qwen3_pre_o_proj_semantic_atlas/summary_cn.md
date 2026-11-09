# A15_02_E03 结果摘要：Qwen3-8B 全宽 attention 输出的粗细语义方差画像

## 结论

正式裁定为 **`depth_pass_spectral_fail`**：

- **深度命题 Pass：**在 `o_proj` 之前的完整 4096 维 attention 输出中，同一粗类内部的细粒度语义相对粗粒度语义，确实在晚层更容易区分。
- **实际方差的谱头主导 Pass：**从 block 1 到 block 35，粗、细语义的每方向实际类别间方差都在 F1 最大。
- **固定 non-head 坐标 Fail：**晚层 tail 有描述性的细语义相对富集，但它没有在两个独立 calibration half 的每个晚层基底中保持同号；middle 也没有通过设计集、特征值 floor 与 half-split 护栏。

最准确的认识更新是：

> 细粒度语义相对粗粒度语义的深层增强，在 attention 经过 `o_proj`、残差合并和 MLP 之前已经存在；但两类语义的实际方差仍主要位于谱头，且没有形成可跨自然语料半集稳定复现的固定 middle/tail 语义通道。

## 实验对象与指标

本实验直接捕获每个 block 的 `self_attn.o_proj` 输入：32 个 query head 的 128 维输出按真实架构顺序拼接成 4096 维向量。它是 attention 对 value 向量加权聚合后的结果，但尚未经过 `o_proj`、残差相加、post-attention normalization 和 MLP。

复用 E01 的 512 条语义文本和独立自然语料：8 个粗类 × 每类 8 个细类 × 4 个模板 × 2 组事实；自然背景 covariance 由 128 篇 DCLM 文档的 65,536 个 token 拟合。频谱按背景方差从大到小切成 16 个等秩 256 维带：F1=head，F2--F8=middle，F9--F16=tail。

区分度定义为

\[
D=\frac{\text{类别中心之间的方差}}{\text{同一类别内部由模板和措辞造成的方差}},
\qquad
R=\log\frac{D_{fine}}{D_{coarse}}.
\]

\(R>0\) 表示细类相对粗类更容易区分；它不表示细类的绝对激活更大，也不证明模型使用了该信号。

## 决定性结果

| 表征边界 | 早层 blocks 1--12 中位 \(R\) | 晚层 blocks 25--35 中位 \(R\) | 早晚差分 \(T\) | block 35 / 36 细粗比 |
| --- | ---: | ---: | ---: | ---: |
| `o_proj` 前完整 attention 输出 | 0.153（1.17×） | 0.764（2.15×） | 0.611，basic-bootstrap 95% 区间 [0.624, 1.156] | 1.99× / 2.21× |
| 完整 block residual（E01） | 0.001（1.00×） | 0.452（1.57×） | 0.451，95% 区间 [0.333, 1.189] | 1.82× / 1.84× |

四个模板的 attention 早晚差分均为正，八次父类留一也全部为正。Block 36 的细粗比高于 block 35，因此最后一层没有反转。

![attention 与 residual 的深度轨迹](figures/figure1_attention_depth_and_residual_comparison.png)

右图的纵轴 \(R\) 是细类区分度与粗类区分度的自然对数比：0 表示两者相同，0.69 约表示细类是粗类的 2 倍。紫线表示 `o_proj` 前 attention，深灰线表示完整 block residual。attention 的相对细类信号在更早的架构边界已存在，但数值差不能归因给某一个中间模块。

## 16 带画像

![层×频带语义方差画像](figures/figure2_attention_layer_band_heatmaps.png)

- \(b\)：每方向实际类别间方差，保留自然背景的大奇异值优势；曲线或颜色越高，表示该类语义实际在该带贡献的激活方差越多。
- \(q\)：\(b\) 除以自然背景特征值，表示相对该方向日常波动的语义异常程度；它不是可分性。
- \(j\)：该带内类别间方差除以类别内方差；越大表示类别中心相对同类措辞扰动更清楚。
- 每行第三列是 \(\log(fine/coarse)\)；红色表示细类相对更强，蓝色表示粗类相对更强。

粗、细语义的实际 \(b\) 在 blocks 1--35 都以 F1 最大，说明主能量并未从 head 迁移到深谱带。晚层细类相对粗类的实际方差份额在 head、middle、tail 的对数比依次为 -0.107、-0.010、+0.162；tail 的点估计超过同维随机方向 q95=0.059，但 calibration half 的逐晚层方向不稳定，所以不能升级为固定 tail 坐标。

![决定性的频带区分度热图](figures/figure3_decisive_attention_band_discriminability.png)

左图颜色是 \(\log(j_{fine}/j_{coarse})\)：红色表示该层该带对细类更可分，黑点表示配对区间不跨零；右图把 16 带聚合为 head/middle/tail。晚层细类优势跨越多个谱带，而不是只驻留在某个固定 middle/tail 位置。

## 与 residual 结果的严格比较

旧 E01 读取的是**完整 decoder block 的 raw residual output**，并非严格意义上的“MoE post-attention 输入”。E03 读取的是 `self_attn.o_proj` 的直接输入。两者之间包含 `o_proj`、残差合并、归一化和 MLP，因此本实验只允许说：

1. 细类相对区分度的深层增强在 `o_proj` 前已经出现；
2. 两个架构边界都呈现晚层细类优势、F1 实际方差主导和固定 non-head 坐标失败；
3. attention 的 \(R\) 较大是描述性差异，不能解释成 residual 路径“削弱了”细类信号，更不能归因给单个模块。

## 有效性与边界

- 36/36 个 block、两个 32,768-token calibration half 和 512 条语义文本均完整覆盖。
- hook 重放误差与头拼接误差为 0；`o_proj` 重构相对误差为 \(1.50\times10^{-7}\)；FP32 Gram 与直接 FP64 的最大相对误差为 \(7.03\times10^{-8}\)。
- H/M/T 的 calibration half-split 基底稳定性和 covariance/能量重构均通过。
- 本结果只建立冻结模型中的表征关联；它不证明 attention 因果产生细语义、深层执行组合计算、某个频带应交给 Router、或专家训练会受益。

## 下一决策

在不进入 Router 训练前，唯一下一决策是：是否用独立 taxonomy 复现两个**不依赖固定频带**的结论——`o_proj` 前的深度差分 \(T_{attention}>0\)，以及完整 residual 的 \(T_{depth}>0\)。固定 middle/tail 频带继续不准入 Router。

完整数据入口沿用 E01 的 [actual_semantic_text_sequences.json](../A15_02_E01_qwen3_residual_semantic_variance_atlas/provenance/actual_semantic_text_sequences.json)。完整证据账本见 [detailed.md](detailed.md)。
