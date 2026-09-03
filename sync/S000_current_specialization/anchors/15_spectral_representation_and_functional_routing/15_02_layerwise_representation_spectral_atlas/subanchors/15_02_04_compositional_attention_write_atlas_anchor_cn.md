---
anchor_id: 15_02_04_compositional_attention_write_atlas
status: insufficient_capability
canonical_language: en
companion_language: zh
parent_anchor: 15_02_layerwise_representation_spectral_atlas
updated: 2026-08-07
---

# A15_02_04 隔离 attention write 中组合语义的谱秩重分配


## 1. Problem Definition

唯一决策问题是：

> 在冻结 Qwen3-8B 中，当表面形式、事实、token 长度、证据位置、答案空间和样本数匹配时，把得到目标语义所需的组合深度从一条边增加到两条和四条边，是否会使可靠类别间语义 covariance 在晚层沿每层自身 DCLM activation covariance 的谱秩向右重分配，尤其是在隔离的 post-`o_proj` attention write 中？

层 $\ell$、表征站点 $s$ 的**数据谱**是独立 DCLM calibration 激活 covariance 的特征分解，不是参数矩阵的奇异谱。

**向右重分配**不表示同一个 eigenvector 从一个编号移动到另一个编号。每层的 activation space 和谱基底都重新定义。它只表示：语义 covariance 在本层内部把更多归一化质量放到更大的 rank percentile；这些方向相对同一层其他方向具有更低的背景方差。

必须分开三种现象：

1. **背景谱变平：**DCLM eigenvalue 分布随层深不再那么 head-concentrated。这只是全局几何诊断。
2. **语义谱秩重分配：**同一个冻结语义变量把更多可靠类别间 covariance 放到更大的归一化 rank。这是本 Anchor 的目标现象。
3. **同一方向的真实跨层运输：**需要显式的 transport、Jacobian、CCA 或 Procrustes 对齐模型，不属于本 Anchor。

组合深度 $g\in\{D0,D1,D2\}$ 分别指答案需要一条、两条或四条原子关系边。taxonomy 深度、SAE feature 层级、MLP 计算、完整 residual、Router 效用和训练收益均不在本 Anchor 内。

## 2. Physical Priors

候选 prior 是：句法、主题和共同上下文在大量自然 token 中变化，因此更容易主导高背景方差方向；依赖多个条件同时成立的组合变量只在较窄的上下文中变化。如果深层 attention write 把这类条件变量保留为独立坐标，而不是把它们放大回共同高方差方向，那么更大的组合深度可能在背景谱的更大 rank percentile 中占有更高相对份额。

若组合变量随深度更可读，但归一化 rank 分布不右移；若 query-binding reversal 复现右移；或表面右移仅由背景谱变平解释，则该 prior 在当前表征站点上失败。

## 3. Falsifiable Hypotheses

**主假设——组合特异的谱秩重分配。**能力、可靠性和尺度匹配门通过后，$D2-D0$ 语义谱秩重心差在晚层相对早层增加；isolated post-`o_proj` attention write 是主站点，pre-`o_proj` 是注册的边界定位次级站点。

**最强 rival。**深层只提高组合变量的总区分度或同时放大全部谱秩，没有组合特异的 rank 重分配。不同类别间总尺度、背景谱变平、prompt 难度、词汇泄漏、位置和不稳定 calibration eigenvector 也可能制造表面右移。

**Pass。**post-`o_proj` 的注册 rank-shift 统计超过同一 world 内 $D0/D2$ 条件交换零假设的 q95，world bootstrap 95% 下界为正，两个 DCLM calibration half 同号，且能力、可靠性、匹配和 hook 强制门全部通过。右移最终落在 head、middle 还是 tail 单独描述；Pass 不要求绝对方差主峰离开 head。

**Fail。**所有强制门通过，但 post-`o_proj` rank-shift 统计不超过零假设或不能跨 calibration half 稳定。若深层区分度增强但没有 rank 右移，裁定为 `depth_pass_rank_shift_fail`。

**Insufficient。**冻结模型不能完成四边任务、删必需边和反事实检查失败、可靠类别间信号接近噪声底、设计未匹配尺度，或任一表征/covariance 基底有效性门失败。

## 4. Mathematical Model

令 $h_{\ell,s,g,y,w,t}\in\mathbb R^d$ 表示层 $\ell$、站点 $s\in\{\mathrm{pre},\mathrm{post}\}$、组合深度 $g$、八类答案 $y$、潜在 world $w$ 和模板 $t$ 的激活。平衡双向加性 nuisance residual 为

$$
z_{\ell,s,g,y,w,t}
=h_{\ell,s,g,y,w,t}
-\bar h_{\ell,s,\cdot,\cdot,\cdot,t}
-\bar h_{\ell,s,\cdot,\cdot,w,\cdot}
+\bar h_{\ell,s,\cdot,\cdot,\cdot,\cdot}.
$$

它只移除加性 template 和 world 主效应，不产生“纯语义”状态。raw 与 centered 两版都保留。

对每个 $g$ 和答案 $y$：

$$
\mu_{\ell,s,g,y}=\mathbb E_{w,t}[z_{\ell,s,g,y,w,t}],
$$

$$
B_{\ell,s,g}=\operatorname{Cov}_{y}(\mu_{\ell,s,g,y}),
\qquad
W_{\ell,s,g}=\mathbb E_y\operatorname{Cov}_{w,t}(z\mid g,y).
$$

首先分开报告三个尺度量：

$$
V_{\ell,s,g}=\operatorname{tr}(B_{\ell,s,g})
\quad\text{（原始语义规模，单位 activation}^2\text{）},
$$

$$
D_{\ell,s,g}
=\frac{\operatorname{tr}(B_{\ell,s,g})}
{\operatorname{tr}(W_{\ell,s,g})+\epsilon}
\quad\text{（稳定语义区分度）},
$$

$$
R_{\ell,s,g}
=\frac{\operatorname{tr}(B_{\ell,s,g})}
{\operatorname{tr}(\Sigma^{\mathrm{bg}}_{\ell,s})+\epsilon}
\quad\text{（相对背景的语义规模）}.
$$

独立 DCLM activation covariance 为

$$
\Sigma^{\mathrm{bg}}_{\ell,s}
=U_{\ell,s}\Lambda_{\ell,s}U_{\ell,s}^{\top},
\qquad
\lambda_{\ell,s,1}\ge\cdots\ge\lambda_{\ell,s,d}.
$$

令 $r_i=(i-0.5)/d$ 为本层归一化 rank，且

$$
b_{\ell,s,g,i}
=u_{\ell,s,i}^{\top}B_{\ell,s,g}u_{\ell,s,i}.
$$

尺度无关的语义谱秩分布为

$$
\pi_{\ell,s,g,i}
=\frac{b_{\ell,s,g,i}}
{\sum_j b_{\ell,s,g,j}}.
$$

考虑到近简并 covariance 区间内的单个 eigenvector 会发生旋转，注册的定位统计使用 16 个等秩、每个 256 维的 projector $F_k$。令频带中点 $m_k=(k-0.5)/16$，则

$$
p_{\ell,s,g,k}=\sum_{i\in F_k}\pi_{\ell,s,g,i},
\qquad
\rho^{(16)}_{\ell,s,g}=\sum_{k=1}^{16}m_kp_{\ell,s,g,k}.
$$

未分带的 $\sum_i r_i\pi_i$ 只保留为 sensitivity diagnostic。

主统计是 difference-in-differences：

$$
T_{\mathrm{rank},s}
=\operatorname{median}_{\ell\in L_{\mathrm{late}}}
[\rho^{(16)}_{\ell,s,D2}-\rho^{(16)}_{\ell,s,D0}]
-\operatorname{median}_{\ell\in L_{\mathrm{early}}}
[\rho^{(16)}_{\ell,s,D2}-\rho^{(16)}_{\ell,s,D0}],
$$

其中 $L_{\mathrm{early}}=\{1,\ldots,12\}$，$L_{\mathrm{late}}=\{25,\ldots,35\}$，block 36 单列。

为了解释右移落点，把 $d=4096$ 切为 16 个等秩 256 维带：F1=head，F2--F8=middle，F9--F16=tail。逐带同时报告每方向原始方差、归一化语义份额和语义/类内 nuisance 比：

$$
\bar b_{\ell,s,g,k}
=\frac{\operatorname{tr}(U_k^\top B_{\ell,s,g}U_k)}{256},
$$

$$
p_{\ell,s,g,k}
=\frac{\operatorname{tr}(U_k^\top B_{\ell,s,g}U_k)}
{\operatorname{tr}(B_{\ell,s,g})},
$$

$$
j_{\ell,s,g,k}
=\frac{\operatorname{tr}(U_k^\top B_{\ell,s,g}U_k)}
{\operatorname{tr}(U_k^\top W_{\ell,s,g}U_k)+\epsilon}.
$$

不同层级的 $V$ 可以相差很大。因此，$V$ 与 $D$ 先回答“信号是否真实”，$\pi$、$\rho^{(16)}$ 与 $p_k$ 再回答“真实信号位于何处”。可靠总信号不存在时，不解释归一化位置。八类答案数、熵、world 和模板数完全相同，防止类别规模进入比较。

背景谱是否变平只用归一化 eigenvalue mass 和 effective rank 报告，不能触发语义 rank-shift verdict。

## 5. Computational Realization

冻结模型为 `/data/share/Qwen3-8B`，共 36 个 decoder blocks，hidden size 4096。在共同 `Answer:` 读出 token 上只读取：

1. full pre-`o_proj` attention output $a_\ell\in\mathbb R^{4096}$，即 32 个 attention head 输出的拼接；
2. isolated post-`o_proj` attention write $y_\ell=\mathrm{o\_proj}_\ell(a_\ell)\in\mathbb R^{4096}$，位于 residual addition 之前。

本实验不读取 residual、RMSNorm 输出、MLP state，不使用 SAE、参数谱、Router 或模型更新。pre/post-`o_proj` 每层分别拟合自己的 DCLM activation covariance；二者 raw 数值和 eigenvector 不视为共享坐标系。

每个潜在空间关系 world 含五个随机 single-token 实体别名，以及路径 $e_0\to e_1\to e_2\to e_3\to e_4$ 上四条有序关系事实形成的二叉组合树。完整节点集合为：

- 四个 $D0$ 叶子：$(e_0,e_1)$、$(e_1,e_2)$、$(e_2,e_3)$、$(e_3,e_4)$；
- 两个 $D1$ 内部节点：$(e_0,e_2)$ 与 $(e_2,e_4)$；
- 一个 $D2$ 根节点：$(e_0,e_4)$，对应 $(r_1\oplus r_2)\oplus(r_3\oplus r_4)$。

主比较在每个 world 内按冻结 Latin schedule 恰好选择一个 $D0$ 叶子、一个 $D1$ 内部节点，并使用唯一 $D2$ 根节点。这样每个层级都有 256 个 world-level observation，且组合深度不会与固定左/右节点位置混淆。全部七个节点仍作为注册的次级位置审计提取。

所有 prompt 包含相同四条事实。查询句式、答案位置、八个 compass 答案类别、事实数、token 数和证据位置日程匹配；事实措辞不出现 canonical answer token，完整八词答案表只出现在所有条件与类别完全相同、无标记的计算指令中。world 与 node schedule 的选择排除零位移，并约束三节点主子集以及七个单独节点位置都具有相等答案类别数。

批准后的 realization 使用 256 个配对 world families 与四个 paraphrase templates，共 7,168 条 node-complete semantic prompts；其中等样本主子集为 3,072 条，且每个主 $g\times y$ cell 恰好含 32 个 world。统计单位是 world family，不是 node、prompt、template 或 token；额外预注册 control 数由 Protocol 管理。

独立 DCLM calibration 复用已审计的 65,536-token manifest，并切成两个 32,768-token half。每个层和站点单独拟合 centered covariance。模型能力使用 next-token accuracy 与正确答案 NLL；静态表征主证据不使用 learned probe。

## 6. Minimal Falsification Tests

1. **生成与匹配门：**每个 world 的七条节点 prompt 具有相同事实、精确 token 长度、答案位置、答案熵和注册事实顺序；三节点主子集与每个节点位置都类别平衡，别名为 single-token，不存在 target-specific 标记或与类别相关的答案 token 出现差异。
2. **能力与必要性门：**三个深度均通过冻结 accuracy/NLL 阈值；删任一必需边会降低正确答案支持，反事实修改一条必需边会按生成规则改变答案。
3. **表征门：**36 层 pre/post hooks 全部精确重放；native `o_proj` output 与 hooked isolated post-write 在数值容差内一致；不包含 residual。
4. **尺度与可靠性门：**在归一化位置之前报告 $V$、$R$、$D$。template split-half 类别均值 cross-product 与 world bootstrap 必须显示可靠总语义信号为正，才解释 $\pi$ 或 $\rho^{(16)}$。
5. **主 rank-shift 检验：**用同一 world 内 $D0/D2$ 条件交换、world-family bootstrap、held-out templates 与两个 calibration-half basis 检验 $T_{\mathrm{rank},\mathrm{post}}$。pre-`o_proj` 以完全相同流程作为边界定位次级结果。
6. **rival 对照：**query-binding reversal 保留全部事实和 query token inventory，但把正确答案变为相反方向；同维随机子空间检查注册 covariance bands 是否特殊；背景 effective-rank 变化单独报告。
7. **落点与尺度审计：**同时报告 raw $\bar b_k$、normalized $p_k$ 和 $j_k$。大/小层级 raw $V$ 的差异本身不构成 rank shift；若 $V$ 可忽略，归一化右移判为 insufficient。
8. **层聚合：**冻结上述 early/late blocks；block 36 不进入主差分并单列。

## 7. Current Evidence

[A15_02](../15_02_layerwise_representation_spectral_atlas_anchor_cn.md) 已建立：Qwen3-8B 的 residual 与 full pre-`o_proj` attention 中，细 taxonomy 语义相对粗语义在晚层更可分，但实际类别间方差仍由 head 主导，固定 middle/tail 特异性失败。该结果测试 taxonomy 粒度，不测试所需组合深度。

[A15_02_03](15_02_03_architectural_head_channel_concentration_anchor_cn.md) 发现少数真实 pre-`o_proj` attention heads 的语义集中超过随机分组，但没有固定头内 covariance-band 身份。这说明不能预设某个 rank band 就是语义模块。

2026-08-05 full-attention audit 已验证 4096 维 pre-`o_proj` hook、独立 DCLM calibration、covariance reconstruction 和 half-split 流程，但没有真实 1/2/4-edge 组合数据，也没有 isolated post-`o_proj` semantic covariance。

学长的 SAE 结果把 SAE decoder feature 投影到 dense-MLP 参数奇异方向，不能回答本 activation-covariance rank 问题。

已完成的 [A15_02_04_E01 实验](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_04_E01_compositional_attention_write_atlas/summary.md) 的 typed verdict 是 `insufficient_capability`。确认集 D0/D1/D2 accuracy 为 0.262/0.227/0.230，低于注册门槛 0.70/0.55/0.40，且三者 Wilson lower 均低于 0.25。required-edge counterfactual log-odds shift 全为正，说明模型响应必要关系，但未可靠执行当前答案接口，不能支撑表征结论。

isolated post-`o_proj` 的 $T_{rank}=0.00276$（等价 11.3 ranks），bootstrap 区间 $[-0.00269,0.01229]$，低于 condition-swap q95 0.00792。pre-`o_proj` 诊断为正：$T_{rank}=0.02409$（98.7 ranks），区间 $[0.00189,0.02811]$，超过 q95 0.01393；但两个站点都未通过注册的早层跨模板语义可靠性门，post 还未通过节点位置鲁棒性门。组合相对区分度从早层到晚层在两个站点都下降：post $T_D=-0.547$，pre $T_D=-0.686$，区间均完全为负。

这些证据没有建立组合特异的谱秩右移；由于能力和可靠性前提失败，也不能对一般假设给出有效科学 Fail。

## 8. Claim Boundary And Next Decision

本 Anchor 最多建立：在一套受控空间关系生成器和一个独立 DCLM calibration 分布下，冻结 Qwen3-8B attention 表征是否出现组合特异的本地 activation-covariance rank percentile 重分配。E01 没有达到作出该判断的前提。post 诊断不成立和负 $T_D$ 只描述当前任务/模型接口，不能否定深层组合表征的一般理论。

它不能证明同一方向跨层真实迁移、attention 因果执行组合、`o_proj` 创造信息、middle/tail 具有普遍语义身份、SAE feature 就是组合节点，或任何 rank partition 能提高 Router/专家效用。attention 负结果也不能排除 MLP 或其他表征边界中的组合。

**唯一下一决策：**是否执行一次“谱结果封存”的能力接口修复：冻结 world、层级、平衡、pre/post 站点、covariance bases、指标和阈值，只改变提示接口或模型规模。候选版本只有在 held-out D0/D1/D2 accuracy 达到 0.70/0.55/0.40、每个 Wilson lower 超过 0.25，且早层 D0/D2 跨模板 covariance 下界为正后，才可进入新的谱确认；接口选择期间不得查看候选谱结果。
