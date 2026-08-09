---
anchor_id: 15_02_layerwise_representation_spectral_atlas
legacy_anchor_id: 15_01_05_coarse_fine_semantic_variance_atlas
status: e01_e02_e03_e04_completed_depth_pass_spectral_fail
canonical_language: en
companion_language: zh
thinking_card: 15_02_layerwise_representation_spectral_atlas_thinking_card_cn.md
parent_line: 15_spectral_representation_and_functional_routing
updated: 2026-08-06
---

# A15_02 逐层表征频谱图谱

Thinking Card：[研究者批准版本](15_02_layerwise_representation_spectral_atlas_thinking_card_cn.md)。

## 1. Problem Definition

唯一问题是：在冻结 Qwen3-8B 中，粗类别是否在浅层已较易区分，同一父类内的细类别是否随层深获得更大的相对区分度，以及粗、细语义的类别间方差分别由每层自然背景 covariance 的哪些谱带承担？

语义结构只有父类—子类两级。组合步数、长程/短程依赖、Router 效用和训练收益均不属于本 Anchor。

## 2. Physical Priors

1. 跨领域粗差异可能在早层已经形成，而条件内细差异需要更深的表征重组。
2. 背景高方差会机械抬高谱头实际能量，因此粗、细语义都可能表现为 head-dominant。
3. 细语义的绝对能量仍可主要位于 head，同时在 middle/tail 中占有比粗语义更高的相对份额。
4. 总 variance 不能单独表示区分性；必须以类别间差异相对类别内模板/措辞噪声解释。

## 3. Falsifiable Hypotheses

**H1，深度相对增益：**细语义相对粗语义的区分度随层深增加；主差分是 blocks 25--35 与 blocks 1--12 的细/粗对数区分度比变化，block 36 单列。

**H2，频谱画像：**粗、细语义的第一等秩谱带均具有最高的每方向实际语义方差；细语义在 bands 2--8 与 bands 9--16 中相对自身总语义方差的富集高于粗语义，不要求细语义绝对能量超过粗语义。

**最强 rival：**标签熵、样本数、词汇身份、模板、位置、整体 residual 尺度、极小特征值或任意同维子空间可复现观察模式。

**Pass：**数据与表征能力门有效，H1 与 H2 均在封存模板、父类留一、nested bootstrap、标签置换、calibration half-split 与同维随机对照下成立。

**Fail：**所有有效性门通过，但相应深度或频谱命题不成立。两个命题分别裁定，不用一项替代另一项。

**Insufficient：**自然语义数据不能被模型表征稳定读出，或数据平衡、token、basis、数值稳定和 confirmation 边界任一强制门失败。

## 4. Mathematical Model

对层 $\ell$、父类 $p$、父类内子类 $c$ 与描述模板 $t$，在共同读出 token 得到 $h_{\ell,p,c,t}$。粗、细类别间 covariance 为

$$
B_\ell^{\mathrm{coarse}}
=\operatorname{Cov}_{p}\!\left(\mathbb E_{c,t}h_{\ell,p,c,t}\right),
$$

$$
B_\ell^{\mathrm{fine}}
=\mathbb E_p\operatorname{Cov}_{c\mid p}\!\left(\mathbb E_t h_{\ell,p,c,t}\right).
$$

粗类别内噪声 $W_\ell^{\mathrm{coarse}}$ 包含该父类内子类和模板变化；细类别内噪声 $W_\ell^{\mathrm{fine}}$ 只包含同一子类的模板变化。区分度为

$$
D_{\ell,g}=\frac{\operatorname{tr}(B_\ell^g)}{\operatorname{tr}(W_\ell^g)+\epsilon},
\qquad
R_\ell=\log\frac{D_{\ell,\mathrm{fine}}}{D_{\ell,\mathrm{coarse}}}.
$$

独立自然语料定义 $\Sigma_\ell^{\mathrm{bg}}=U_\ell\Lambda_\ell U_\ell^\top$。隐藏维度 4096 严格切为 16 个连续 256 维等秩带：F1=head，F2--F8=middle，F9--F16=tail。第 $k$ 带每方向实际语义方差为

$$
b_{\ell,g,k}
=\frac{\operatorname{tr}(U_{\ell,k}^\top B_\ell^gU_{\ell,k})}{256}.
$$

同时报告相对背景方差的 $q_{\ell,g,k}$、相对类别内噪声的 $j_{\ell,g,k}$，以及除以全谱每方向均值后的频带富集 $e_{\ell,g,k}$。

## 5. Computational Realization

模型冻结为 `/data/share/Qwen3-8B`：36 decoder blocks、hidden size 4096、bfloat16 forward；统计量使用 FP64。读取 embedding 输出与全部 block residual output，共 37 个位置，不读取概念词自身状态。

背景 covariance 复用经 hash 审核的 128 篇独立 DCLM 文档和 65,536 token；若原 worker basis 不完整，按同一 manifest 重算。语义数据构造为 8 个父类 × 每类 8 个子类 × 每子类 8 条无标签名称的自然定义，共 512 条；共同读取 `Classification:` 的冒号 token。

Qwen 参数不更新。低容量 ridge probe 仅作 held-out 表征能力门，超参数不得访问封存模板。

## 6. Minimal Falsification Tests

1. 粗、细均为八分类，同一隐藏状态同时进入两种统计。
2. 正确父/子标签字符串不出现在正文；读出 token、位置、长度分布与样本量匹配。
3. 粗、细完整表征 probe 均超过层级标签置换 q95，才解释内部方差。
4. covariance reconstruction、能量守恒、16 带 half-split 稳定性和特征值 floor 敏感性通过。
5. 逐带结论必须超过同维 Haar 随机子空间；真实 band 失败而完整表征可读时，判定 rank 不特异。
6. 主统计使用父类→子类→模板 nested bootstrap、父类留一和封存模板；不把 512 句当作独立语义单位。
7. block 36 单独报告，不参与早层与晚层主差分。

## 7. Current Evidence

A15_02_01 已在 capability-valid 四层任务中建立：组合结果在完整深层状态中更可读，但没有固定 H/M/T 或细带稳定超过同维随机方向。A15_02_02 已在冻结 Qwen3-8B 中建立层特异父/子角色选择性，同时否定统一“父级=head”映射。

二者都没有估计跨父类的粗语义 covariance 与同父类内细语义 covariance。原 32 条链每个父类只有一个子类，无法定义 $\operatorname{Cov}_{c\mid p}$，因此仅保留为外部描述性对照。

A15_02_E01 已完成并得到分条裁定。细/粗相对区分度的早晚差分为 $T_{depth}=0.4514$，配对 basic-bootstrap 95% 区间为 $[0.3327,1.1891]$；四个模板和八次父类留一均同号，因此深度命题 Pass。第 35/36 个 block 的细/粗区分度比分别为 1.82/1.84，最后一层没有反转。

粗、细语义的实际类别间方差在 blocks 1--35 均以 F1 为 16 带最大值，因此实际方差 head-dominance Pass。细语义在晚层 middle/tail 的相对份额只高约 3.5%/3.7%，区间跨零且未超过同维随机方向 q95；深层细语义的相对区分度提升反而跨越几乎全部 16 带。因此 middle/tail 特异富集 Fail，联合 verdict 为 `depth_pass_spectral_fail`。正式结果见 [中文摘要](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_E01_qwen3_residual_semantic_variance_atlas/summary_cn.md)。

A15_02_E02 把该深度效应定位到 `o_proj` 之前的单注意力头。2026-08-05 的轴顺序审计修正了旧模板 split：修正后全宽 $T_{attention}=0.6106$，区间 $[0.6039,1.2096]$，四个模板与八次父类留一仍全部同向；通过全局 352-cell 最大值校正的单元为 9 个，而非旧报告的 14 个。合格单头内部没有任何 8 维频带超过完整随机方向与稳定性门；旧 `L32H27-F1` 窄结论已撤回。正式修正结果见 [E02 中文摘要](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_E02_qwen3_attention_head_semantic_atlas/summary_cn.md)。

A15_02_E03 进一步补齐 32 头拼接后的完整 4096 维 pre-`o_proj` covariance，包括 E02 单头块对角 moment 无法表达的跨头 covariance。复用完全相同的 512 条语义文本和 65,536 个 calibration token 后，早层/晚层中位 $R$ 为 0.153/0.764，$T_{attention}=0.6106$，basic-bootstrap 区间 $[0.6238,1.1562]$；blocks 35/36 的细粗比为 1.99/2.21，最后一层无反转。粗、细实际类别间方差在 blocks 1--35 均以 F1 最大。晚层 tail 有 +0.162 的描述性相对富集并超过同维随机 q95=0.059，但未在两个 calibration-half 基底的每个晚层保持同号；middle 也未通过，因此 verdict 仍为 `depth_pass_spectral_fail`。正式结果见 [E03 中文摘要](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_E03_qwen3_pre_o_proj_semantic_atlas/summary_cn.md)。

A15_02_E04 补齐 `o_proj` 已完成跨头混合、但尚未与 residual 相加的完整 attention branch。复用相同模型、512 条语义文本和 65,536 个 calibration token 后，早层/晚层中位 $R$ 为 0.131/0.762，$T_{post}=0.6311$，层级 bootstrap 区间 $[0.5529,1.1477]$；blocks 35/36 的细粗比为 2.13/2.36，最后一层仍无反转。实际类别间方差在 blocks 1--35 对粗、细语义均以 F1 最大。晚层细语义相对粗语义的方差份额在 head/middle/tail 为 -0.106/+0.063/+0.159；middle 小效应超过同维随机 q95=0.059 并通过两个 calibration-half、模板、干扰变量和 floor 门，但 tail 未通过独立半集逐晚层方向门，因此联合频谱 verdict 仍为 `depth_pass_spectral_fail`。正式结果见 [E04 中文摘要](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_E04_qwen3_post_o_proj_semantic_atlas/summary_cn.md)。

## 8. Claim Boundary And Next Decision

本 Anchor 已建立：冻结 Qwen3-8B 的完整 residual、pre-`o_proj` attention、post-`o_proj` attention branch 与 MLP input 都在晚层呈现更强的细类相对区分度；信号跨过 `o_proj`，最后一层不反转。粗、细语义的实际类别间方差仍由 F1 主导。post-`o_proj` middle 出现通过本地对照的小幅相对份额富集，但 tail 不稳定，因而没有建立完整 fixed-rank non-head 坐标。它不能证明深层执行组合、attention 或 `o_proj` 是必要原因、某头/频带应指导 Router，或专家训练能够受益。

**唯一下一决策：**是否用一套独立、平衡且无标签泄漏的 taxonomy，同时复现 post-`o_proj` 的正向深度差分和晚层 middle 小幅相对富集。只有这两项同时复现，middle 才进入专家反事实效用或共同训练兼容性准入；复现前不进入 Router 训练。
