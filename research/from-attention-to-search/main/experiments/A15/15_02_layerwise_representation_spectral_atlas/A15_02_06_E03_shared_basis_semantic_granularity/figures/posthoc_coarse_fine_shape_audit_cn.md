# Coarse/Fine 谱曲线 shape 补充审计

```text
status: POSTHOC_DESCRIPTIVE_AUDIT
source_experiment: A15_02_06_E03_shared_basis_semantic_granularity
registered_verdict_changed: no
```

## 1. 问题

原注册谱质心只回答 fine 的完整归一化方差谱是否整体比 coarse 更靠后。本补图回答两个更具体的问题：

1. 把 coarse 和 fine 放在同一组 Mean Response 方向上，两条谱曲线实际长什么样、在哪里分开？
2. “fine 的归一化谱位置更靠后”是否意味着 fine 在这些方向上的原始方差绝对值更大？

本分析复用冻结的 512 条数据、Attention-write、Mean Response 基、层级分解和 2,000 次 parent bootstrap，不重新提取模型激活，不改变 E03 注册结论。

## 2. 计算对象

令冻结的逐方向归一化方差谱为

\[
p_{\ell,g,j}=\frac{e_{\ell,g,j}}{\sum_k e_{\ell,g,k}},
\qquad g\in\{C,F\}.
\]

将 4096 个 rank 固定分为 128 个等宽 bin，每个 bin 含 32 个方向。第 \(b\) 个 bin 的归一化方差份额为

\[
P_{\ell,g,b}=\sum_{j\in b}p_{\ell,g,j}.
\]

曲线图使用归一化密度 \(128P_{\ell,g,b}\)；若谱在所有 rank 上均匀分布，该值恒为 1。差异图使用

\[
D_{\ell,b}=100\left(P_{\ell,F,b}-P_{\ell,C,b}\right),
\]

单位为每个 32-direction bin 占全部归一化方差的百分点。因为两条谱分别归一化，必有

\[
\sum_bD_{\ell,b}=0.
\]

因此红色区域表示 fine 把更多**相对方差份额**放在该处；它不自动表示 fine 的原始方差大于 coarse。

未归一化图由

\[
e_{\ell,g,j}=p_{\ell,g,j}\operatorname{tr}(B^g_\ell)
\]

还原，并在每个 bin 内取 32 个方向的平均值。这张图才直接比较同一层、同一 rank 区间中的原始层级分量方差。

## 3. 图 1：代表层的归一化 shape

![Coarse/Fine normalized spectral shapes](presentation_coarse_fine_spectral_shapes_selected_layers.png)

- 层选择固定复用原 Protocol 的 `1, 6, 12, 18, 24, 30, 35, 36`，不是看结果后挑层。
- 两条曲线面积都为 1；纵轴为 log scale。
- 红色填充表示 fine 的相对份额更大；蓝色表示 coarse 更大。

直接观察：两条曲线在大部分谱上高度重叠，并不存在 coarse、fine 分别占据两个互不相交谱峰的结构。Block 1 的重分配最直观；多数中深层表现为幅度较小、分散在多个 rank 区间的差异。

## 4. 图 2：差异位置与逐点不确定性

![Coarse/Fine binned difference atlas](presentation_coarse_fine_binned_difference_atlas.png)

- A：每层每个 bin 的 \(D_{\ell,b}\) 点估计。
- B：2,000 次配对 parent-bootstrap 的逐点支持；红色为 95% 区间完全高于 0，蓝色为完全低于 0，灰色为跨 0。
- C：先在 blocks 1--35 上取逐 bin 中位数，再在每个 parent-bootstrap draw 内用同一批 parent 索引重新计算整条深度轨迹。

轨迹中位数层面：

- 7/128 个 bin 支持 coarse > fine；它们集中在谱最前端，形成 rank 33--160 和 rank 193--288 两段，中间一个 32-rank bin 未解决。
- 28/128 个 bin 支持 fine > coarse，但从 normalized rank 约 0.20 到 0.91 呈离散分布，没有形成一个连续、唯一的 fine band。
- 93/128 个 bin 的逐点区间跨 0。

这里的区间均为 pointwise，不是对 128 bins 和 35 blocks 同时校正后的置信区间。因此它们适合解释 shape，不足以直接选择 Router 子空间。

## 5. 图 3：未归一化的原始方差

![Coarse/Fine raw variance](presentation_coarse_fine_raw_variance_selected_layers.png)

这张图直接回答“红线在某处更高，是否说明 fine 的原始方差更大”。答案是：通常不能从归一化图推出这一点。

在 blocks 1--35 中，fine/coarse 总 raw variance 比值的中位数为 `0.527`，范围为 `0.309--1.320`。在固定展示层中，只有 block 30 的 fine 总 raw variance 与 coarse 接近并略高（`F/C=1.017`）；其余展示层的 coarse 总 raw variance更大。因此当前正结果主要是**相对谱位置重新分配**，不是“fine 的绝对方差在后谱普遍更大”。

## 6. 当前认识更新与边界

允许的读取：

> 在冻结 Mean Response 基中，coarse 和 fine 使用高度重叠的谱方向；fine 相对 coarse 的位置后移主要来自谱头相对份额减少、较后区域中许多分散 bin 的份额小幅增加。

不能读取为：

- coarse 和 fine 已经被两个低重叠谱段清晰分开；
- 已经确定一个连续且跨层固定的 fine 语义区间；
- 归一化 fine 曲线更高就等于其原始方差更大；
- pointwise 正差 bin 已经可以作为 Router 方向。

如果下一步要选择具体方向，应在独立 selection split 上冻结候选 bins，再在 held-out split 上检验其语义区分和 Router 功能，并与同维随机/Haar、相邻谱段和补空间比较。当前 shape 图只能生成候选，不能完成方向认证。

## 7. 证据来源

- 冻结数组：`/data/250010109/MoE_Router/experiments/20260812_a15_02_06_shared_basis_semantic_granularity/runs/a15-02-06-e03-20260812-granularity/arrays/analysis_arrays.npz`
- 冻结投影 child means：`/data/250010109/MoE_Router/experiments/20260812_a15_02_06_shared_basis_semantic_granularity/runs/a15-02-06-e03-20260812-granularity/arrays/projected_child_means.pt`
- 生成脚本：`/data/250010109/MoE_Router/experiments/20260812_a15_02_06_shared_basis_semantic_granularity/scripts/render_coarse_fine_shape_audit.py`
- [逐层逐 bin 数值](../tables/posthoc_coarse_fine_shape_bins.csv)
- [轨迹中位数逐 bin 数值](../tables/posthoc_coarse_fine_shape_trajectory.csv)

