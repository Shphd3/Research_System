# 相邻层 Attention 写入在公共参数谱上的变化是否随深度稳定后移？

```text
type: daily_research_report
status: AI_DRAFT_AWAITING_HUMAN_CONFIRMATION
date: 2026-08-12
topic: all_adjacent_attention_write_transitions
canonical_anchor: Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/15_02_layerwise_representation_spectral_atlas_anchor.md
frozen_protocol: Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/protocol.md
canonical_summary: Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/summary.md
canonical_detailed: Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/detailed.md
```

## 摘要

本轮回答：8→9 的负向结果是局部现象，还是“越深越向参数谱后部写入”的整体规律？我们把 36 层 Attention 分支输出全部投到同一个 Mean Response 参数基，计算 35 个相邻层对在预先冻结的 F9--F12 区域中的归一化方差份额变化。35 对同时校正后，16 对显著为正、11 对显著为负、8 对未定，说明局部变化真实但正负交替。注册的早/中/深均值显著不同，却没有显著线性深度斜率，而且阶段结果对 24→25/25→26 边界处的大反转敏感。因此本报告的待确认判断是：该指标具有非单调层位置结构，不能支持“越深越后移”，也不适合作为新增信息的直接定义。

## 1. 从 8→9 到本轮唯一问题

上一轮固定第 8、9 层后发现：F9--F12 的 raw variance 增长约 1.73 倍，但归一化份额下降 1.83 个百分点。这个结果只裁定一个相邻层对，最强竞争解释是它恰好处在一个局部振荡位置。

本轮唯一问题是：

> 在完全固定数据、Attention hook、公共参数基、谱带和归一化方法后，全部相邻层对的 F9--F12 变化是否随深度呈稳定、显著的后移？

这仍是方差代理的稳健性审计，不把方差增长称为新知识。

## 2. 对象、数据与统计单位

Attention 写入 $A_\ell(x)$ 是第 $\ell$ 层 `o_proj` 之后、加 residual 之前的分支输出。所有层使用相同公共基向量 $v_j$：

$$
z_{\ell xj}=A_\ell(x)^\top v_j,
\qquad
e_{\ell j}=\operatorname{Var}_x(z_{\ell xj}),
\qquad
p_{\ell j}=\frac{e_{\ell j}}{\sum_ke_{\ell k}}.
$$

没有对单条样本的投影系数做单位归一化；归一化只发生在跨样本方差统计之后。数据仍是 512 条平衡 taxonomy 记录。统计独立单位是 8 个 parent domain，采用 2,000 次配对 parent bootstrap。层和相邻层对是固定架构位置，不是独立重复样本。

主区域 F9--F12 对应归一化 rank `[0.50,0.75)`，它由前序细粒度实验提前冻结。对相邻层定义：

$$
D_{sem,\ell}=Q_{\ell+1}(F9{:}F12)-Q_\ell(F9{:}F12),
$$

并用 raw 方差对数比 $G_{sem,\ell}$ 防止把相对份额与绝对增长混淆。

## 3. 判定规则

全部 35 个相邻层对进入推断；8 个代表层对只用于分面展示。单对显著性使用覆盖全部 35 对的最大偏差同时置信区间。

注册阶段按 transition start 划为 early 1--12、middle 13--24、deep 25--35。阶段差异使用三个同时校正的对比；另以 $D_{sem,\ell}$ 对层深的线性斜率作为单调性守卫。只有 deep−early 与斜率都显著为正，才能支持“越深越向后”。

所有 36 个缓存、公共基和来源 hash 均通过；最大投影能量误差为 $2.29\times10^{-7}$；8→9 与上一轮 full/A/B 结果完全一致。因此注册结果 eligible。边界移动检查是在结果后追加的解释稳健性审计，不替换注册 verdict。

## 4. 结果

### 4.1 相邻层变化显著，但符号频繁交替

![全部相邻层变化](../../../Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/figures/figure2_all_adjacent_transition_atlas.png)

35 对同时校正后：16 对 $D_{sem}>0$，11 对 $D_{sem}<0$，8 对未定。8→9 为 `−0.01831`，但 7→8 为 `+0.02544`、10→11 为 `+0.01888`。更深处同样交替：24→25 为 `−0.05557`，25→26 随即为 `+0.06033`。

这允许说不同固定层位置的归一化变化确实不同；不允许把正值称为该层新增了细粒度知识。

### 4.2 注册阶段不同，但不是单调深度规律

| 阶段 | 平均 $D_{sem}$ | 95% 区间 | 平均 $G_{sem}$ |
| --- | ---: | ---: | ---: |
| early 1--12 | +0.002168 | [+0.001678,+0.002425] | +0.6831 |
| middle 13--24 | -0.003779 | [-0.004046,-0.003294] | +0.4371 |
| deep 25--35 | +0.007947 | [+0.007512,+0.008050] | +0.2545 |

deep−early 为 `+0.005779`，同时区间 `[+0.005019,+0.006539]`。但全 35 对线性斜率为 $-2.27\times10^{-5}$，区间 $[-4.63\times10^{-5},+1.27\times10^{-5}]$，覆盖 0。因此注册 verdict 是 `stage_dependent_nonmonotonic`，而不是“深度后移”。

![深度差异判定](../../../Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/figures/figure3_depth_difference_inference.png)

阶段平均相邻差分具有 telescoping 性质，只由阶段首尾份额决定。注册 middle 恰好包含 24→25 大幅下降，而 deep 从 25→26 大幅反弹开始。将两个阶段边界各移动一层的后验检查中，deep−early 点估计从 `−0.000535` 到 `+0.006355`。所以注册阶段差异是真的，但其大小和符号不足以形成稳健三阶段规律。

raw 方差增长则从 early 的 `+0.6831` log2/transition 降到 deep 的 `+0.2545`；三个阶段对比均显著为负。这再次表明相对谱位置与绝对规模是两种不同问题。

## 5. 结论、边界与唯一下一决策

### 5.1 待确认认识更新

8→9 的负结果不能推广到全模型；同一公共参数基上的相邻层变化具有大量显著正负局部结构。但这些变化不是随深度单调后移，注册阶段差异又受到阶段边界处大幅反转影响。最安全的更新是：总 Attention-write 的归一化谱方差可以描述层位置差异，却不能稳定定义“本层新增信息”。

### 5.2 不能推出什么

- 不能由正 $D_{sem}$ 推出该层获得了新知识或更细粒度信息。
- 不能由 raw variance 增长推出归一化谱位置后移。
- 不能从固定模型的层位置差异外推到模型总体规律。
- 没有检验低秩、因果使用或 Router 收益。

### 5.3 唯一下一决策

- **决策：** 是否关闭“总 Attention-write 归一化方差 = 新增信息”这一代理，并在一个固定相邻层对上改用 residual-relative、留出目标可访问性指标。
- **完成判据：** 在任何新 run 之前明确接受或拒绝这一指标替换；不得从当前 atlas 挑一个有利层对或另换公共基。

## 6. 证据与来源

- [Frozen Protocol](../../../Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/protocol.md)
- [Canonical Summary](../../../Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/summary.md)
- [Canonical Detailed](../../../Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/detailed.md)
- [All transition metrics](../../../Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/tables/transition_metrics.csv)
- [Stage contrasts](../../../Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/tables/depth_contrasts.csv)
- [Boundary sensitivity](../../../Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_06_E05_all_adjacent_depth_transitions/tables/stage_boundary_sensitivity.csv)
