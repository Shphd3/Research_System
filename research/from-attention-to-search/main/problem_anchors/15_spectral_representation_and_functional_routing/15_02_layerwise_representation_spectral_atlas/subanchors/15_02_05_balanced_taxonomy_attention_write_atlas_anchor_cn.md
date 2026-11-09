---
anchor_id: 15_02_05_balanced_taxonomy_attention_write_atlas
status: completed_nonpositive_location_fail_pending_human_judgment
canonical_language: en
companion_language: zh
english_canonical: 15_02_05_balanced_taxonomy_attention_write_atlas_anchor.md
parent_anchor: 15_02_layerwise_representation_spectral_atlas
updated: 2026-08-09
execution_authorized: false
---

# A15_02_05 粗—细粒度语义的逐层谱定位


## 1. Problem Definition

**唯一决策问题：**

> 在冻结 Qwen3-8B 中，同时审核绝对强度和归一化谱分配后，一个子类相对同父类其他子类的语义残差，是否比粗粒度父类区分形成可复现的深度相关谱定位；总体结果是否也出现在预注册具体子类中，而不是由聚合平均制造？

这是表征认知更新实验，不实现或评估 Router、专家分配、因果使用或训练增益。它只继承 A15_02 的问题：不同层可读出什么语义对象，以及这些对象位于各层哪个已命名的本地谱位置。

实验必须部分回答三个相连的问题：

1. **总体定位：**粗粒度和条件细粒度语义的对比强度、F1--F16 归一化分配及二者差值怎样随层变化？
2. **差值缺陷：**fine-minus-coarse 曲线是否能由总尺度增长、归一化、对比数不等、父均值自包含、表达噪声、本地谱基不稳定或不同 child 相互抵消解释？
3. **具体语义案例：**`combinatorics - mathematics` 与 `linear algebra - mathematics` 是否具有可靠的逐层残差、稳定的跨层相关结构，以及相似或不同的细粒度轨迹？

这里，**粗粒度残差**是一个学科父类中心相对其他父类中心的差；**条件细粒度残差**是一个子学科中心相对同一父类内其他子学科中心的差。后者是可操作的 sibling contrast，不是被纯化或因果隔离的“细粒度 feature”。图中的 `child - parent` 只是 leave-one-child-out 残差的简写，因为固定语料包含子类描述，没有一套独立的 parent-only 描述。

主表征是当前 block 的 attention 对实际 MLP 输入造成的变化：
\(\Delta n_\ell=\operatorname{RMSNorm}_\ell(h_\ell+a_\ell)-\operatorname{RMSNorm}_\ell(h_\ell)\)，其中 \(a_\ell\) 是 isolated post-`o_proj` attention write。这个同层反事实差值有明确定义；禁止把不同层的 covariance、RMS 或 eigenvector 直接相减。\(a_\ell\) 只作来源边界对照。

每层用自己的 DCLM activation-covariance eigenbasis，并等秩分成 16 段。F1 是最高背景方差 head，F2--F8 是 middle，F9--F16 是 tail。不同层相同 local rank 只是可比较的百分位，不是同一方向。

已批准并冻结的数据包含 512 条无标签泄漏描述：8 个父学科、每个父类 8 个子学科、每个子类 8 种表达。为了在总数不变时同时包含两个指定数学案例，新 manifest 用 `linear algebra` 替换旧数据中的 `algebra`。这不是逐条复用旧 512 条。把 `linear algebra` 与 `combinatorics` 作为同级 children 只是操作分组，不证明二者具有相同 taxonomy depth 或 semantic distance。

Pass 只支持这个模型和数据中的受限逐层谱定位认识；Fail 削弱细粒度特有后移；Insufficient 保持问题开放。任何结果都不自动批准 Router 实验。

## 2. Physical Priors

1. **粒度—定位 prior。**如果深层对类内细分与类间区分的组织不同，条件细粒度残差相对粗粒度残差的本地谱位置应发生变化。暴露变量是逐层 fine-minus-coarse F1--F16 分配；若两者共同移动，则细粒度特异性为假。
2. **绝对—相对 prior。**归一化后移只有在底层语义对比能跨独立表达复现时，才允许解释其语义强度。绝对每方向跨表达能量暴露这个条件。若 normalized 后移只出现在绝对可靠性底噪处，只能判为 artifact 或 Insufficient，不能称为“更多细语义”。
3. **总体—案例 prior。**一般性的细语义轨迹不应由单一父类承担，也不应在预注册具体子类中消失。leave-one-parent-out 与具体 child 的 split-half 相关暴露这个 prior。失败时只能得到“聚合异质性”，不能得到统一细粒度坐标。

## 3. Falsifiable Hypotheses

以下操作定义和裁定规则已由研究者确认，并在执行前冻结为 Protocol revision `A15_02_05_E01_r1`。

**H1——细粒度特异的深度定位。**匹配对比数并通过可靠性门后，\(\Delta n\) 中 conditional-fine 相对 coarse 的本地秩重心从早层到晚层进一步向右。

**H2——差值不是统计假象。**H1 效应通过父类保持的 child-label permutation、表达 half、calibration half 和 leave-one-parent-out；完整绝对与 normalized F1--F16 曲线能够区分绝对增长、相对重分配和内部抵消。

**H3——具体案例结构。**`combinatorics - mathematics` 与 `linear algebra - mathematics` 在可用层分别具有正的 split-half 可靠性。它们的跨层方向相关和 16-band 谱形相关图用于判断总体轨迹是案例一致、child-specific，还是仅由平均产生。H3 是类型诊断，不能挽救失败的 H1。

**最强竞争解释——共同增强加异质平均。**深度让所有学科语义共同增强或重定向；归一化与不同 children 的平均制造出平滑的 fine-minus-coarse 曲线。该解释预期 H1 在 controls 后弱或为零，或者总体效应在具体案例中消失或互相矛盾。

**Pass：**H1 和 H2 全部有效性门通过；H3 再把结果标为 `case_concordant` 或 `aggregate_heterogeneous`，不强迫一种具体案例叙事。**Fail：**可靠证据给出非正的细粒度深度交互，或观察量不超过注册 taxonomy/null controls。**Insufficient：**数据身份、绝对语义可靠性、谱基复现、数值重建或精度不合格。区间跨零只算 Insufficient，不算负结论。

## 4. Mathematical Model

令 \(y_{\ell i}\) 表示样本 \(i\) 的主 \(\Delta n_\ell\)；\(a_\ell\) 只作来源边界重放。对表达 half \(s\)、父类 \(p\) 及其 child \(c\)，粗对比是 \(u^s_{\ell p}=\mu^s_{\ell p}-\mu^s_{\ell,-p}\)，条件细残差是 \(r^s_{\ell pc}=\mu^s_{\ell pc}-\mu^s_{\ell p,-c}\)。同父类 sibling residual 共享参照并在加权后和为零，因此互余弦必须与匹配的同父类 child pairs 比较，不能只与零比较。

令 \(P_{\ell k}\) 为 F\(k\) 的 256 方向 projector。绝对跨表达每方向能量 \(A^\times_{\ell gk}\) 是 \(v^{A\top}P_{\ell k}v^B\) 的均值再除以 256，单位为 activation squared/direction；它度量可复现强度，不度量因果使用。normalized allocation \(q_{\ell gk}\) 把两个 expression halves 的投影平方能量平均，再除以全部 16 段能量；它和为 1，不能建立绝对增长。令 \(m_k=(k-0.5)/16\)，\(\rho_{\ell g}=\sum_km_kq_{\ell gk}\)。唯一主指标为

\[
T_{\rho}
=\operatorname{median}_{\ell\in L_{late}}(\rho_{\ell F}-\rho_{\ell C})
-\operatorname{median}_{\ell\in L_{early}}(\rho_{\ell F}-\rho_{\ell C}),
\]

其中 \(L_{early}=\{1,\ldots,12\}\)，\(L_{late}=\{25,\ldots,35\}\)，block 36 单独报告。\(T_\rho\) 的单位是 normalized local-rank percentile interaction；没有 \(A^\times\) 时，它不能识别共享向量，也不能区分强度增长与重分配。具体 child 的跨层稳定性使用两个 expression halves 的交叉余弦；同层 child-pair 余弦与所有 mathematics child pairs 比较，另一个矩阵比较 16-band 谱形。这些量只描述案例稳定性与相似性，不支持总体泛化。

## 5. Computational Realization

冻结 Qwen3-8B（36 blocks，宽度 4096）。在共同 readout position 捕获 \(h_\ell\)、isolated \(a_\ell\) 和实际 normalized MLP input，再 replay \(\Delta n_\ell\)。不拟合模型、probe、Router 或 expert 参数。

冻结的 512 条语料包含 8 个学科领域、每类 8 个 children、4 个模板和 2 组不相交事实。相同状态离线附上 coarse 与 conditional-fine metadata。mathematics 同时包含两个指定案例，并按已批准的新 manifest 用 `linear algebra` 替换 `algebra`。所有描述都不得出现 parent 或 child 标签。

为排除 64 对 8 的对比数量差，预冻结 8 个 rotations，每个 rotation 从每个 parent 选择一个 child，八次恰好覆盖 64 个 children；每个 fine 估计都用 8 个 child contrasts，并与 8 个 coarse parent contrasts 按相同方式聚合。语义独立单位是 8 个 root families，不是 512 个 prompts 或 36 层。

独立 DCLM activation 为每层/站点定义一个 full basis 和两个 calibration-half bases；语义投影前冻结 F1--F16。父类保持的 child-label permutations 与同维 Haar partitions 控制语义分组和秩分段。统计使用未平滑方向。必须交付绝对/normalized 逐层图谱、全段与逐方向抵消视图、具体案例方向/谱形相关及 mathematics pair envelope，以及一张差值缺陷表。

具体案例图可以回答操作性残差是否稳定、案例是否一致；它不能回答是否减去了独立的 `mathematics` 概念向量，因为该语料没有 parent-only state。

## 6. Minimal Falsification Tests

唯一决定性比较是在匹配对比数后，\(\Delta n\) 上的 fine-minus-coarse 深度交互 \(T_\rho\)。

1. **数据与数值门：**恰好 512 条平衡、无标签泄漏记录；manifest 冻结；站点身份精确；\(\Delta n\) replay 与投影能量重建满足 Protocol 容差。
2. **绝对可靠性门：**coarse 和 fine 的 \(A^\times\) 在早、晚层窗口的 root-bootstrap 下界均大于零。没有这个门的 normalized 曲线为 Insufficient。
3. **H1 主检验：**\(T_\rho\) 的 95% hierarchical-bootstrap 下界大于零，点估计超过父类保持 permutation q95，两个 expression halves 和两个 calibration-half bases 均为正，且任一 leave-one-parent-out 不反号。
4. **H2 缺陷审计：**必须报告完整绝对与 normalized F1--F16 曲线、匹配 rotations、Haar partitions 和逐方向视图。正 \(T_\rho\) 但没有绝对增长时标为 `relative_reallocation_only`；重心为零但存在稳定、相反符号的 band 变化时标为 `redistribution_without_centroid_shift`，不能算 H1 Pass。
5. **H3 具体案例：**两个指定数学案例只有在同层 split-half 可靠性为正后，才打开相应跨层相关格。与 H1 一致标为 `case_concordant`；不一致标为 `aggregate_heterogeneous`。两者都不改变 H1 verdict。

主反例是：绝对 coarse/fine 结构可靠，但 \(T_\rho\) 非正或不过 null control。对平滑总体曲线的最小反例是：总体通过，但两个预注册案例不可靠或趋势相反。

## 7. Current Evidence

此前 post-`o_proj`、parameter-rank 和自然层级图谱为平衡的 sibling-relative activation 审计提供了动机，但都没有建立细粒度特异定位。A15_02_05_E01 现已按冻结的 `A15_02_05_E01_r1` Protocol 完成；数据、tensor、谱基、可靠性、重采样、数值和图件证据均 eligible。

注册 verdict 是 `nonpositive_location_fail`。在实际 \(\Delta n\) 中，fine-minus-coarse 的配对秩重心在 1--12 层中位数为 +0.009334，在 25--35 层为 -0.000239，因此 \(T_\rho=-0.009573\)，注册的单侧 95% 下界/上界为 [-0.011199, -0.004492]。两个 expression halves、两个 calibration-half bases 和八个 leave-one-parent-out 值全部为负。与此同时，早晚窗口的 coarse 和 fine 绝对对比都可靠，因此 Fail 不是因为细粒度残差测不到。

孤立 attention write 的描述性 \(T_\rho=+0.011327\)，说明定位符号依赖 representation site，不能把 post-`o_proj` 曲线直接提升为实际 MLP 输入增量上的普遍规律。两个指定数学残差都可靠且各自原始秩重心后移，但它们的 16-band profile 高度相似，实际同层与跨层方向却弱或不稳定。因此具体案例定型为 `aggregate_heterogeneous`，不能挽救 H1。见 [结果摘要](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/summary.md) 与 [完整证据记录](../../../../experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_05_E01_balanced_taxonomy_attention_write_atlas/detailed.md)。

## 8. Claim Boundary And Next Decision

本 Anchor 现在拒绝如下主张：在这个模型和数据中，actual \(\Delta n\) 里的 conditional-fine residual 相比 coarse parent residual 会额外获得随深度向右的本地秩定位。保留的三个更窄事实是：粗细残差都可复现并随深度增强；符号在 isolated-write 与 actual-input 边界发生变化；稳定的 band profile 不等于稳定的语义方向。

结果不能建立信息创造、一般语义复杂度、纯 child-minus-parent feature、attention 或 MLP 因果使用、跨层 eigenvector 同一、通用 middle/tail 含义、Router compatibility、expert utility 或训练收益。它也没有排除其他逐层语义组织形式，或另行定义的 middle 对象。

**唯一下一决策：**停止把固定谱段或归一化秩后移解释为条件新增性，把具名更新交给 A15_08 的“相对旧状态、在新鲜留出目标上的增量可访问性”门。完成标准是在匹配的目标无关对照下，更新相对旧状态读出仍提供留出目标增益；本图谱不启动 Router 实验。
