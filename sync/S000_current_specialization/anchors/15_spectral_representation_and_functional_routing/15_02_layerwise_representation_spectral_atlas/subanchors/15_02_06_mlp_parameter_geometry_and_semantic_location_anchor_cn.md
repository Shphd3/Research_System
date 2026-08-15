# A15_02_06：MLP 参数共同子空间与 attention write 的粗细语义位置

英文 Anchor 为规范版本：[anchor](15_02_06_mlp_parameter_geometry_and_semantic_location_anchor.md)。研究者原始判断见 [Thinking Card](15_02_06_mlp_parameter_geometry_and_semantic_location_thinking_card_cn.md)。

## 1. 问题定义

冻结 Qwen3-8B 后，MLP 的高增益输入子空间是否比 middle/tail 更跨层共享？细粒度相对粗粒度语义在每层独立 `post-o_proj` attention write 中，是否随深度把更大方差比例放到本层参数谱的后部，并且这一位置能通过 RMSNorm、参数增益和非线性 MLP 响应检验？

## 2. 物理先验

- $a_\ell$ 是本层 `o_proj` 后、加 residual 前的写入，但它由历史 residual 条件化，不是纯粹新信息。
- MLP 真正接收 $n_\ell=RMSNorm(x_\ell+a_\ell)$；attention 引起的输入增量是 $\Delta n_\ell=n_\ell-RMSNorm(x_\ell)$。
- 原始方差位置只表示几何占据；参数增益和非线性响应才约束是否“有效”。

## 3. 可证伪假设

1. 参数谱 head 的等秩投影子空间比 matched middle/tail 和同维随机子空间更跨层对齐。
2. 细减粗的本层参数秩重心从早层到晚层增加。
3. 该方向在增益加权、实际 $\Delta n$ 和 MLP broad-band 响应中保留。

最强替代解释是：head 对齐仅是尺度/RMSNorm 几何，tail 相对富集只是低能量归一化残差，MLP 并未有效传递。

## 4. 数学对象

$$K_\ell=W_{gate,\ell}^TW_{gate,\ell}+W_{up,\ell}^TW_{up,\ell}=V_\ell\Gamma_\ell V_\ell^T.$$

跨层共同性比较投影子空间 $O_{\ell m k}=tr(P_{\ell,k}P_{m,k})/r$，不比较单个奇异向量。每层参数秩横轴独立排序；同一秩不是同一向量。

主统计量是实际 MLP 输入增量中“细减粗秩重心”的晚层中位数减早层中位数。16 个 256 维频带中，F1 为 head，F2--F8 为 middle，F9--F16 为 tail。

## 5. 计算实现

复用 8 父类×8 子类×4 模板×2 fact bundle 的 512 条平衡数据和既有 post-`o_proj` 缓存；只为 $x$、$\Delta n$ 与 MLP 响应重跑同一批文本，不新增数据。

## 6. 最小证伪

- 检验 eigendecomposition、正交性、能量守恒、缓存复现与 128/256/512 维敏感性。
- 粗细使用相同样本和相同表达噪声可靠性分母。
- raw、gain、RMSNorm 坐标控制、$\Delta n$、非线性 $\Delta m$ 分开报告。
- block 36 仅展示，不进入早/晚主对比。

## 7. 当前证据

0806 的数据 covariance 实验说明 post-`o_proj` 粗细绝对方差都由 head 主导，细相对粗在 middle 有小幅局部富集，tail 不稳定。它没有使用参数谱，也没有检验跨层参数共同性和实际 MLP 响应，因此不能回答本 Anchor。

0807 full run 的参数共同性为 U 形：native head/middle/tail-256 是随机期望的 2.20/1.04/3.26 倍，折叠 RMSNorm 后是 2.05/1.13/7.04 倍，因此 head-only common 假设失败。粗、细 raw write 重心都从早层约 0.35 后移到晚层约 0.47，但 raw 细减粗 $T=-0.0107$ 且区间跨零。gain-weighted 实际 $\Delta n$ 的 $T=+0.01630$、95% 区间 [0.00599, 0.02833]，主位置统计量通过；nonlinear MLP response 的区间跨零。typed outcome 为 `location_without_commonality`。

后续公共坐标实验又拆开了三个问题。E02 中 Mean Response 基的 fine-only 早晚后移为 $+0.03171$，Rank Consensus 基则为 $-0.00755$ 且区间跨零，因此深度结论是 `basis_sensitive_shift`。E03 冻结 Mean Response 后得到轨迹级 coarse < medium < fine，fine-minus-coarse 为 $+0.008175$，区间 $[+0.001964,+0.012620]$；但 shape 审核显示粗细曲线大部分重叠，平均差异来自谱头份额减少和较后多个离散位置的小幅增加，不是一个连续语义谱段。E04 的 8→9 不向该后部区域增加相对份额；E05 在全部相邻层中得到 16 个正、11 个负、8 个未决，整体定型为 `stage_dependent_nonmonotonic`。

直接记录：[E02](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E02_shared_parameter_basis_attention_projection/summary.md)、[E03](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E03_shared_basis_semantic_granularity/summary.md)、[E04](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E04_layer8_to9_shared_basis_growth/summary.md) 与 [E05](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/summary.md)。

## 8. 边界与下一决策

完整机制未通过：参数 common guard 和 nonlinear response 均失败，只有 gain-weighted $\Delta n$ 的位置统计量通过；公共坐标中的深度变化还依赖基且非单调。保留的窄结论是：Mean Response 可以作为描述性的平均参数响应标尺，语义粒度在这把标尺上整体有序，但它不能定位唯一谱段或层新增信息。不能声称词频、稀有知识、知识学习位置、因果必要性或 Router utility。

唯一下一决策是结束用归一化 Attention-write 方差重分配定义层新增信息的路径，把问题交给 A15_08 的“相对旧状态、在新鲜留出目标上的增量可访问性”检验。完成标准是固定一个旧状态、一个具名更新、一个冻结目标，并在匹配的目标无关对照下获得相对旧状态的留出增益；本 Anchor 不启动 Router 实验。
