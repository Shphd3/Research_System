# 单图版谱质心差：生成与阅读说明

![单图版 fine−coarse 谱质心差](presentation_rank_centroid_single_clear.png)

## 1. 这张图回答什么

在冻结的 Mean Response 公共参数基中，对每个 Transformer block，细粒度语义变化的归一化方差谱质心是否比粗粒度语义变化更靠后？

这张图不寻找“差异最大的维度”，也不选择一个谱段。每个点只是一个标量：同一 block 中 fine 与 coarse 两条完整归一化方差谱的质心之差。

## 2. 数据不是两套 coarse/fine 文本

原始数据是同一套 512 条平衡英文描述：8 个 parent，每个 parent 有 8 个 child，每个 child 有 4 个表达模板和 2 个不重叠事实包。文本中不直接出现 parent/child 标签，读取位置统一为末尾 `Classification:` 的冒号。

实际例子：

- `parent = mathematics, child = linear algebra`

  > Topic description: This topic studies vector spaces organized by bases and coordinates; it also uses linear transformations preserving addition and scalar multiplication; a central concern is eigenvalues and eigenvectors characterizing invariant directions. Identify the broad academic field and the specific subfield. Classification:

- `parent = mathematics, child = geometry`

  > Topic description: This topic studies shapes, distances, angles, and spatial incidence; it also uses congruence, similarity, and rigid transformations; a central concern is constructions involving points, lines, and surfaces. Identify the broad academic field and the specific subfield. Classification:

- `parent = physics, child = optics`

  > Topic description: This topic studies propagation, reflection, and refraction of light; it also uses interference between coherent waves; a central concern is polarization and wavelength-dependent behavior. Identify the broad academic field and the specific subfield. Classification:

从同一批 child 均值中分解三个层级：

\[
d^C_p=\mu_p-\mu,
\qquad
d^M_{pm}=\mu_{pm}-\mu_p,
\qquad
d^F_{pc}=\mu_{pc}-\mu_{p,m(c)}.
\]

因此，coarse 是 parent 间变化，fine 是同一 medium pair 内 child 间变化；它们不是分别输入一条“数学文本”和一条“线性代数文本”得到的两个 hidden state。

## 3. 指标如何生成

所有 block 使用同一组冻结 Mean Response 向量 \(V=[v_1,\ldots,v_{4096}]\)。对层级 \(g\in\{C,M,F\}\)，先把相应语义分量投影到方向 \(v_j\)，得到方向能量 \(e_{\ell,g,j}\)，再在每一层级内部归一化：

\[
p_{\ell,g,j}
=
\frac{e_{\ell,g,j}}{\sum_k e_{\ell,g,k}}.
\]

令归一化 rank 为 \(\rho_j=(j-1)/(4095)\)，谱质心为：

\[
r_{\ell,g}
=
\sum_j\rho_jp_{\ell,g,j}.
\]

图中纵轴是：

\[
y_\ell=100(r_{\ell,F}-r_{\ell,C}).
\]

单位是 **rank-percentile point**：纵轴 `+1` 表示 fine 质心比 coarse 质心晚 `0.01` 个归一化 rank，约等于 \(0.01\times4095\approx41\) 个 rank 位置。

## 4. 坐标、点和区间

- 横轴：Transformer block，1--36。
- 纵轴：fine−coarse 谱质心差，不是空间维数。
- 红色实心点：点估计为正且 pointwise 95% parent-bootstrap 区间完全高于零。
- 红色空心点：点估计为正，但区间跨零。
- 蓝色空心点：点估计为负，但区间跨零。
- 灰色方点：block 36，仅展示，不进入 blocks 1--35 的轨迹汇总。
- 灰色误差线：逐 block 的 pointwise 95% parent-bootstrap 区间；不是 simultaneous 多层区间。

blocks 1--35 中，fine−coarse 的轨迹中位数为 `+0.818` rank-percentile points，95% parent-bootstrap 区间为 `[+0.196,+1.262]`；28/35 个点估计为正，13 个逐 block 区间完全高于零，22 个跨零。

## 5. 允许和不允许的结论

允许：在当前数据、Attention-write hook 与冻结 Mean Response 基下，fine 相对 coarse 的完整方差谱质心存在正的 trajectory-level 趋势。

不允许：每个 block 都成立；纵轴代表差异子空间维数；某个固定 band 是唯一 fine 区间；Attention-write 已被证明是旧状态之外的新增信息；该方向能够改善 Router。

## 6. 生成来源

- 冻结数值：[layerwise_metrics.csv](../tables/layerwise_metrics.csv)
- 原始运行数组：`/data/250010109/MoE_Router/experiments/20260812_a15_02_06_shared_basis_semantic_granularity/runs/a15-02-06-e03-20260812-granularity/arrays/analysis_arrays.npz`
- 渲染脚本：`/data/250010109/MoE_Router/experiments/20260812_a15_02_06_shared_basis_semantic_granularity/scripts/render_rank_centroid_single_clear.py`
- 图片 SHA-256：`0e5079cf172a3498686e022cdc8f56b68b8e74fb5c027ca88c45881cf76a34eb`

本图只改变展示方式，不重新估计数据、不改变注册指标或 verdict。
