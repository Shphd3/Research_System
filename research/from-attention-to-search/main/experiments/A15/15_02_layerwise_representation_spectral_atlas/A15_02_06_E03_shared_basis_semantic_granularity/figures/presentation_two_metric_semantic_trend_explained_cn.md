# 两指标语义粒度图：生成与阅读说明

![清晰标注后的两指标图](presentation_two_metric_semantic_trend_explained.png)

## 1. 图使用的表征与公共坐标

每个 block 使用同一批 coarse、medium、fine 样本在 `self_attn.o_proj` 之后、加 residual 之前的 Attention-write 表征。三种语义粒度全部投影到同一个冻结的 Mean Response MLP 参数基；语义激活不参与公共基的构造或选择。

公共方向按平均参数响应由强到弱排序，归一化 rank 记为

\[
q_j=\frac{j-1}{d-1}\in[0,1].
\]

对语义粒度 \(g\)、block \(\ell\) 和公共方向 \(j\)，先计算跨样本投影方差，再在该语义粒度内部归一化：

\[
p_{\ell,g,j}=
\frac{\operatorname{Var}_x(a_{\ell,g}(x)^\top v_j)}
{\sum_k\operatorname{Var}_x(a_{\ell,g}(x)^\top v_k)}.
\]

因此，图比较的是归一化方差在参数谱上的**相对位置**，不是 raw variance 大小。

## 2. 左图：无阈值谱位置

每种粒度的谱重心为

\[
r_{\ell,g}=\sum_j q_jp_{\ell,g,j}.
\]

纵轴实际绘制

\[
100\times(r_{\ell,F}-r_{\ell,C}),
\]

单位是 `rank-percentile points`。例如纵轴 `+2` 对应原始谱重心差 `+0.02`，约等于在 4096 个方向上后移 82 个 rank；它不是放大后的新实验结果，只是单位换算。

## 3. 右图：固定 middle-late 谱带

冻结谱带为归一化 ranks \([0.50,0.75)\)，对应 4096 维时的一基 ranks 2049--3072。定义能量占比

\[
s_{\ell,g}=\sum_{j:q_j\in[0.50,0.75)}p_{\ell,g,j}.
\]

纵轴实际绘制

\[
100\times(s_{\ell,F}-s_{\ell,C}),
\]

单位是 `percentage points`。例如纵轴 `+2` 表示 fine 比 coarse 在该谱带多分配 `0.02` 的归一化总能量，即多 2 个百分点；不是相对增长 2%。

## 4. 线、点、阴影和统计汇总

- 红色实线 `F−C` 是主比较；红点表示该 block 为正，蓝点表示该 block 为负。
- 蓝色虚线 `M−C` 与紫色虚线 `F−M` 是 medium 有序性辅助比较。
- 红色阴影是每个 block 的 pointwise 95% parent-bootstrap 区间；bootstrap 单位是 8 个 parent domain，而不是把 36 个 block 当作独立样本。
- 右上角汇总是 blocks 1--35 的 trajectory median 及其 95% parent-bootstrap 区间。
- Block 36 只展示，不进入汇总统计。

## 5. 允许与不允许的结论

允许：在冻结 Mean Response 基和当前数据下，semantic granularity 与更靠后的归一化谱位置存在 trajectory-level 正趋势。

不允许：每一层都满足该关系；fine 的绝对方差更大；Attention-write 一定是 residual 中不存在的新知识；该谱位置已经能用于 Router。
