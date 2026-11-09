# A15_02_E03：Qwen3-8B 全宽 attention 输出粗细语义方差画像

状态：**已完成**；正式裁定为 `depth_pass_spectral_fail`。结果入口：[中文摘要](summary_cn.md) 与 [完整证据账本](detailed.md)。

## 0. 推进点

E01 在 4096 维完整 block residual 中发现晚层细类相对更可分；E02 已证明该深度效应在 `o_proj` 之前的 32 个真实注意力头中存在，并完成逐头 128 维审计，但其 calibration moment 只包含各头内部 covariance，不能恢复跨头 covariance。E03 复用完全相同的 512 条语义文本和 65,536 个自然语料 token，补齐 32 头拼接后的 4096 维全宽谱画像，使 attention 与 residual 可以在同一指标定义下比较。

## 1. 唯一问题

冻结 Qwen3-8B 的 `o_proj` 前 attention 输出是否已经表现出：

1. 晚层细粒度语义相对粗粒度语义更可分；
2. 这种优势是否稳定落在某段 4096 维自然背景 covariance 谱中。

本实验只做表征审计，不证明 attention 的必要性、模块因果贡献、Router 适用性、专家兼容性或训练收益。

## 2. 对象、数据与指标

- 对象：每个 block 的 `self_attn.o_proj` 输入，即 32×128 注意力头输出按原架构顺序拼接成的 4096 维向量；它位于 `o_proj`、残差相加、后续归一化与 MLP 之前。
- 数据：8 粗类×每类 8 细类×4 模板×2 独立事实组，共 512 条无标签泄漏英文描述；独立 DCLM 128 文档×512 token 拟合 covariance。
- 16 带：每带 256 维；F1=head，F2--F8=middle，F9--F16=tail。
- \(D=B/W\)：类别中心间方差除以同类文本内部扰动；越大表示类别相对更紧凑、更可分。
- \(R=\log(D_{fine}/D_{coarse})\)：正值表示细类相对更可分。
- \(b\)：每方向实际类别间方差；\(q\)：除去自然背景特征值后的语义方差；\(j\)：频带内 \(B/W\)；\(e\)：相对全谱平均的实际语义方差富集。

## 3. 判据与护栏

- 早层为 blocks 1--12，晚层为 25--35，block 36 单列。
- 2,000 次层级配对 bootstrap，并要求 4/4 模板、8/8 父类留一同向。
- non-head 特异性必须超过同维随机方向，并通过 design/confirmation、calibration half、干扰变量残差化和特征值 floor 检查。
- 模型/数据 hash、hook shape、精确 replay、`o_proj` 重构、65,536-token coverage、covariance 数值重构、投影能量守恒及 H/M/T half-split 稳定性为硬护栏。

## 4. 与旧结果的比较边界

旧 E01 对象是完整 decoder block 的 residual 输出，不是严格的 post-attention MLP 输入。attention 与 residual 之间还隔着 `o_proj`、残差合并、归一化和 MLP；因此两者可以比较“信号在哪个架构边界已出现”和“画像如何变化”，但不能把数值差直接归因给某一个中间模块。

## 5. 输出

完成全宽谱、层×16 带热图、深度轨迹、决定性 \(\log(j_{fine}/j_{coarse})\) 热图、residual 对比、compact tables、`summary/detailed` 与 0805 自包含中文报告。
