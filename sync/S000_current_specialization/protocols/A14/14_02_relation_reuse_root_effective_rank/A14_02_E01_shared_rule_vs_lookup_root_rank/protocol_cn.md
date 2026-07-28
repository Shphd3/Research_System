---
experiment_id: A14_02_E01_shared_rule_vs_lookup_root_rank
status: completed_insufficient
run_authorized: true
run_id: a14_02_e01_shared_rule_vs_lookup_root_rank_4gpu_20260723_1427
job_id: pt-q6hu0fq5
result_summary: summary_cn.md
primary_anchor: ../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md
---

# Protocol：A14_02_E01 共享规则与 lookup 的任务根状态功能秩

## 0. Approval Snapshot

**Approval status：**2026-07-23 经用户逐项审核后修改批准，并于同日授权按冻结合同完成本地冒烟验证与四卡 full run。  
**Purpose：**判断低 exact-frequency 是否必然对应高任务根功能秩，并区分共享组合规则、lookup 基数与最终答案读出瓶颈。  
**Primary anchor：**[A14_02 共享组合规则与任务根状态功能秩](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor_cn.md)  
**Anchor decision question：**匹配 $K,F,D$、输出熵、模型和完整状态 task utility 后，共享组合规则是否只需更低维的根状态子空间即可保持 held-out utility？  
**Physical prior tested：**规则跨上下文复用允许根状态形成机制复用。  
**Core model term tested：**$k_{\mathrm{func}}(\epsilon_L,\epsilon_A)$，即投影根状态后仍保持 test loss/accuracy 的最小持久维数。  
**Anchor falsifier：**共享与 lookup 的 matched 功能秩无差异，或差异被 lookup 数量、最终答案瓶颈、训练失败解释。  
**Experiment role：**root-cause / operationalization audit；不是 Router 方法实验。  
**Primary metric：**normalized shared-structure functional-rank advantage $\Delta k_{\mathrm{structure}}$。  
**Claim boundary：**仅裁定受控 NTP 任务中的表示机制。  
**Minimal setup：**一个小型两步组合 NTP 任务；matched shared 与 lookup 数据生成器；最终 `post-final-norm ROOT` 主状态；`pre-final-norm ROOT` 次级定位；5 seeds。  
**Basic configuration：**2 layers、1 attention head、$d_{\mathrm{model}}=64$ 的 decoder-only Transformer；full-position NTP CE；paired conditions 使用相同训练与测量合同。  
**Conditions to run：**Stage A 四个主要条件；Stage B lookup-$K$ rival calibration；Stage C duplicate-vs-diverse guard。  
**Pass：**共享低频条件通过 task/generalization gates，且功能秩优势达到冻结阈值、95% 区间为正、4/5 seeds 同号，并通过重放与随机子空间守卫。  
**Fail：**matched 后无功能秩优势，或 lookup 数量/答案读出瓶颈解释全部变化。  
**Insufficient：**任一主要条件未学会、样本/答案/checkpoint 不匹配、使用 test 答案构造主干预、完整维度重放失败或结果不稳定。  
**Cannot claim：**自然语言低秩、树是真实语义结构、QK 参数低秩、Router 有用。  
**Approval decision：**
- [ ] 原样批准
- [x] 修改后批准
- [ ] 拒绝
- [ ] Park

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| exact relation | 一个具体输入—规则实例—答案映射项 | shared 中为 $(a,\alpha,\beta,y)$；lookup 中为 $(a,k,y)$ | tuple | 定义训练暴露频率 $F$ | semantic rule |
| rule-instance count $K$ | 输入中可区分的规则实例或规则 ID 数量 | shared 的参数对数量与 lookup 的随机表数量均为 16 | count | 排除“规则 ID 更少” | 独立算法数量相同 |
| shared rule family | 不同实例共享同一两步组合形式 | $u=\phi_\alpha(a), y=\psi_\beta(u)$ | generator | 可复用结构 | 自然语言语义 |
| lookup family | 每个规则实例为独立随机表 | $y=\pi_k(a)$ | permutation/table | 最强记忆 rival | 模型只会记忆 |
| training exposure $F$ | 一个 exact relation 在训练集出现的次数 | 每个 mapping entry 的训练样本数 | count | 区分低频与高频 | 规则是否共享 |
| context diversity $D$ | 生成器或 split 可用且被平衡分配的 nuisance 模板数量 | context pool 与每个 split 的模板覆盖数 | count | 区分表面重复与跨 context 变化 | 当 $F=1$ 时单个 relation 自身多样 |
| post-final-norm root | 读完全部输入、经过最终 LayerNorm/RMSNorm、进入 LM head 前的状态 | 主 `ROOT` state | $d$-vector | 最终答案任务的主表示对象 | 全部中间组合过程 |
| pre-final-norm root | 最终归一化之前的同一 `ROOT` residual state | 次级定位状态；投影后重放真实 final norm 与 LM head | $d$-vector | 判断主差异是否由最终归一化制造或消除 | 与 post-norm 秩可直接代数等同 |
| root residual | 去除答案类别原型后的根状态 | $h_\rho-\mu_y$ | $d$-vector | 去除平凡 answer rank | 因果路径 |
| task-functional root rank | 保持 test 任务行为至少需要的根状态方向数 | calibration 子空间、test 投影重放 | directions | 主要因果指标 | 严格秩或单样本复杂度 |
| effective rank | 谱能量的等效方向数 | entropy effective rank | directions | 辅助几何诊断 | utility |
| semantic consistency | 等价上下文给出同一答案语义 | pairwise agreement | proportion | “学会”的稳定性门 | 表面 deterministic |
| task utility | held-out 任务表现 | answer accuracy 与 answer CE | proportion / nats | 防止低 rank 坍缩 | 学习机制 |

## 2. Anchor Alignment

**Decision question：**shared composition 是否在 matched 条件下额外降低 held-out task-functional root rank？  
**Physical prior：**共享函数机制可跨 context 复用。  
**Core model term：**$\Delta k_{\mathrm{structure}}$。  
**Falsifier：**功能秩只跟 lookup $K$、答案读出瓶颈或能力失败变化。  
**Claim boundary：**受控 synthetic NTP。

### 2.1 与学长 Q/K 删谱实验的非重合性

| 维度 | 学长实验 | 本实验 |
|---|---|---|
| 主对象 | $W_Q/W_K$ 参数矩阵 | 指定层 `ROOT` hidden state |
| 干预 | 删除参数尾部奇异方向 | 投影状态并重放冻结模型后缀 |
| 主结果 | A→C loss 对参数删谱的鲁棒性 | held-out 任务至少需要多少状态方向 |
| share 变量 | 复用、单规则频率、独立规则数混合改变 | $K,F,D$ 显式匹配后比较 shared/lookup |
| 泛化要求 | 参数现象定位 | 未见 context/组合的状态任务充分性 |

因此本实验新增的是“参数谱现象是否对应任务充分状态压缩”与“排除频率和 lookup 数量后共享规则是否仍有额外效应”，不是重复测 Q/K 谱。

## 3. Tested Hypothesis

在低 exact-frequency、context-diverse 的 matched 条件下：

$$
\Delta k_{\mathrm{structure}}
=
\frac{
k_{\mathrm{func}}^{lookup}
-k_{\mathrm{func}}^{shared}
}{
d
}
\ge \delta_k
$$

并且 95% paired-bootstrap 区间下界大于 0，5 个 seeds 中至少 4 个为正。

$\delta_k$ 已冻结为 $4/64$；不得依据 test 结果修改。

## 4. Rival Explanations

1. **Lookup cardinality：**规则数量少本身降低 rank。
2. **Answer-class bottleneck：**根状态只编码答案类别。
3. **Task failure / collapse：**模型没学会，表示因此低 rank。
4. **Exact duplicate：**重复次数而非跨 context 的共同规则产生谱集中。
5. **Checkpoint selection：**事后选择低-rank checkpoint。
6. **Finite-sample rank：**样本量小于维度或不同条件样本量不等。
7. **Readout bottleneck：**只在最终层看到低功能秩，反映的是答案头而非组合状态。
8. **Arbitrary-subspace tolerance：**模型对任意同维投影都鲁棒，并非学得特定任务子空间。
9. **Label leakage：**按真实 test 答案选择原型，使任务保持变成平凡结果。
10. **Suffix information bypass：**投影中间层 `ROOT` 后，后续 attention 从其他 token 重新读取信息，伪造根状态充分性。
11. **Exact-frequency confound：**shared 中每个 mapping entry 的训练次数更高，而非共享结构降低 rank。
12. **Generalization asymmetry：**要求 lookup 猜测从未见过的随机表项，使 shared 优势变成任务可解性差异。
13. **Final-normalization artifact：**LayerNorm/RMSNorm 本身改变几何，使 post-norm 的差异不能定位到归一化之前的状态形成。

## 5. Data / Model / Algorithm / Objective

### 5.1 Shared two-step generator

选择有限实体集合 $a\in\mathcal A$ 与规则参数 $(\alpha,\beta)$。输入中显式提供因子化 token；潜在答案由

$$
u=\phi_\alpha(a),
\qquad
y=\psi_\beta(u)
$$

生成。

建议第一版采用可精确生成、输出均衡、可做 unseen-combination split 的有限群/位运算形式。具体运算在实现前冻结，不允许根据 rank 结果更换。

### 5.2 Lookup generator

对每个规则 $k$，采样独立随机 permutation $\pi_k$：

$$
y=\pi_k(a).
$$

保持输入 token 结构、答案集合、序列长度和输出边际与 shared 条件一致。

### 5.3 必须严格相同的生成器与训练量

主比较的 paired conditions 必须使用同一组：

1. 实体集合大小 $|\mathcal A|$；
2. 规则实例数 $K=16$；shared 中为 16 个参数对，lookup 中为 16 张独立随机 permutation；
3. 每个 exact relation 的训练暴露次数 $F$；
4. nuisance context pool、各 split 的模板数与平衡分配规则；
5. 训练、calibration、test 的样本数；
6. 输入词表、token 位置、序列长度和 NTP 监督位置；
7. 答案词表、每个规则内的答案边际与全局输出熵；
8. 总训练 token 数与 filler 数量；
9. 模型结构、参数量、初始化 seed、优化器、学习率、batch、训练预算与评估间隔；
10. ROOT 位置、状态样本数、子空间拟合预算、$k$ 网格、随机空间数与 bootstrap 合同。

使用 permutation/bijection 生成 shared 与 lookup 映射，使每个规则实例在遍历实体集合时产生完全均衡的答案边际。两边使用相同的 latent index、context 与 split manifest；只替换“共享组合映射”或“独立随机表”这一列。

### 5.4 主测试与组合泛化测试必须分开

**主功能秩 test：新 context、已见 mapping entry。**每个测试 exact relation 的映射项已在训练中出现，但 test 使用未参与训练或子空间拟合的 nuisance context。shared 与 lookup 因而都能够通过能力门；该 split 决定主功能秩差异。

**附加组合泛化 test：未见 input--rule combination。**该 split 只用于判断 shared 是否学习了组合规则，不进入 shared/lookup 主功能秩差值，也不要求 lookup 猜测未见随机表项。

### 5.5 Sequence

统一格式：

```text
[rule-part-1] [entity] [nuisance-context] [rule-part-2] [ROOT] [ANSWER]
```

- `ROOT` 为唯一根状态采集位置；
- `ANSWER` 为单一 canonical semantic label；
- nuisance context 不改变正确答案。

### 5.6 Model and objective

- causal decoder-only Transformer；
- 建议冻结为 2 layers、1 attention head、$d_{\text{model}}=64$；
- full-position NTP CE；
- 根位置固定为答案前 `ROOT`；
- 主干预点固定为最终 LayerNorm/RMSNorm 后、LM head 前的 `ROOT` 状态；投影后只重放冻结 LM head，避免后续 attention 从其他 token 恢复信息；
- 次级定位点固定为最终 LayerNorm/RMSNorm 前的同一 `ROOT` residual state；投影后必须依次重放真实 final norm 与冻结 LM head；
- post-norm 是唯一通过判据；pre-norm 只判断最终归一化是否制造、放大或抹除差异。二者不得合并成共同通过条件；
- 该主指标严格解释为“注册答案任务所需的最终根状态维数”，不能单独定位全部组合计算；
- 早／中层 `ROOT` 只作定位诊断；未加入 no-reread 或显式 bypass audit 前，不称为中间层功能秩；
- 相同 tokenizer、初始化分布、优化器、batch、训练 steps；
- 只允许 calibration split 选择 checkpoint；
- test root states 不参与 checkpoint、子空间、容忍度或阈值选择。

## 6. Conditions, Seeds, And Checkpoints

### Stage A — 决定性 2×2

固定 $K=16$、答案分布、context pool、每个 exact relation 的训练暴露次数与 held-out sample count：

| Condition | Rule type | Exact relation exposure | Context | 作用 |
|---|---|---|---|---|
| S-U | shared | 每个 exact relation 1 次 | 规则家族覆盖 diverse context；单个 relation 训练 context 数为 1 | 低频共享规则关键反例 |
| L-U | lookup | 每个 exact relation 1 次 | 与 S-U 使用相同 context manifest | matched 低频记忆 rival |
| S-R | shared | 每个 exact relation $F_H$ 次 | diverse | 高频 shared guard |
| L-R | lookup | 每个 exact relation $F_H$ 次 | diverse | 高频 lookup guard |

### Stage B — lookup-$K$ calibration

在 lookup-only、`repeat-diverse` 中使用 $K\in\{1,4,16\}$。  
该阶段报告描述曲线；只有在 per-rule exposure、总任务剂量和 filler 完全匹配时，才允许因果解释。

### Stage C — frequency versus diversity

比较：

- `S-R-diverse`
- `S-R-duplicate`

两者 exact count 相同；前者使用不同 nuisance context，后者重复同一 surface context。

### Condition / guard registry

| Item | Anchor clause / rival | Why needed | Evidence role | Pass | Fail | Insufficient | Artifact |
|---|---|---|---|---|---|---|---|
| S-U vs L-U | shared structure beyond $K,F,D$ | 主问题 | Primary | 冻结效应与推断规则通过 | matched 后无差异 | 任一硬门失败 | primary rank table |
| S-R vs L-R | frequency interaction | 判断频率是否有附加作用 | Secondary guard | 方向可解释 | 无附加差异 | 能力不匹配 | exposure table |
| lookup-$K$ | lookup cardinality | 排除较少表导致低秩 | Rival calibration | 不能解释全部主差异 | 完全解释差异 | 训练剂量未匹配 | lookup-$K$ table |
| diverse vs duplicate | context variation | 排除 exact duplicate | Rival calibration | 区分 context 效应 | 无区分 | count 未匹配 | diversity table |
| full-rank replay | intervention hook | 保证测量有效 | Hard gate | 数值恢复 | — | 恢复失败 | replay table |
| shuffled state | state use | 确认 ROOT 被任务使用 | Hard guard | 任务明显受损 | state 不影响任务 | hook 不稳定 | replay table |
| random subspaces | arbitrary tolerance | 排除任意投影都可用 | Hard guard | 学得空间显著更优 | 无优势 | 方差过大 | random-control table |
| pre/post norm | final-normalization artifact | 定位 LayerNorm/RMSNorm 作用 | Secondary localization | 边界明确 | 差异只由接口产生 | 提取或重放失败 | norm table |

### Seeds

预注册 5 个 seeds。所有主要条件共享 seed 列表与初始化采样规则。

### Checkpoint gate

在 calibration split 上选择第一个同时满足：

- answer accuracy $\ge 0.95$；
- answer CE $\le 0.10$；
- 连续 3 个 checkpoint 满足；
- 无答案类别缺失。

阈值已经审核冻结。任何条件在预算内不通过，主要比较记为 insufficient，不延长训练或单独调参。

checkpoint 只由 calibration 决定。选择后，主 paired comparison 还必须在 held-out full-state utility 上满足：

- accuracy 绝对差 $\le 0.01$；
- answer CE 绝对差 $\le 0.02$ nat。

test 只用于检查该预注册匹配门，不参与 checkpoint 选择。若匹配门失败，结果为 insufficient，不用 test 结果重新选 checkpoint。

## 7. Primary Metric

### 7.1 Calibration-only functional subspace

在 calibration split 估计不依赖答案身份的全局根状态均值

$$
\mu^{cal}
=
\mathbb E[h_\rho].
$$

对每个注册维数 $k$，模型主体与后缀全部冻结，仅在 calibration 上拟合正交基 $U_k$，最小化状态投影后的 answer CE：

$$
U_k^\top U_k=I_k.
$$

任务感知子空间使用固定优化器、固定 steps 和预注册初始化集合；按 calibration loss 选取一次，在 test 上只评估。主干预不得按 test 答案选择均值、原型或子空间。

### 7.2 Root-state intervention and replay

在 test 上替换注册状态：

$$
\widetilde h_{\rho,i}^{(k)}
=
\mu^{cal}
+U_kU_k^\top(h_{\rho,i}-\mu^{cal}),
$$

并继续运行冻结的模型后缀。定义：

$$
k_{\mathrm{func}}(\epsilon_L,\epsilon_A)
=
\min\left\{
k:
\begin{array}{l}
L_{\mathrm{test}}^{(k)}-L_{\mathrm{test}}^{full}\le\epsilon_L,\\
A_{\mathrm{test}}^{full}-A_{\mathrm{test}}^{(k)}\le\epsilon_A
\end{array}
\right\}.
$$

采用“持久过阈值”：注册网格中所有更高 $k$ 都必须继续通过。主指标为 S-U 相对 L-U 的：

$$
\Delta k_{\mathrm{structure}}
=
\frac{
k_{\mathrm{func}}(L\text{-}U)
-
k_{\mathrm{func}}(S\text{-}U)
}{
d
}.
$$

冻结容忍度为：

$$
\epsilon_L=0.02\ \text{nat},
\qquad
\epsilon_A=0.01.
$$

冻结最小重要效应为：

$$
\delta_k=\frac{4}{64}=0.0625.
$$

### 7.3 Required replay controls

1. $k=d$ 与恒等映射必须数值恢复完整模型；
2. $k=0$ 使用同一个 calibration 全局均值，不能使用答案原型；
3. 学得的 $U_k$ 必须优于多组同秩 Haar 随机子空间；
4. shuffled-state 应破坏任务，确认 replay hook 生效；
5. 投影曲线、loss 容忍度和 accuracy 容忍度均需报告。

### 7.4 Why it decides

S-U 与 L-U 均为 exact relation 低频，使用相同的 context manifest，并匹配 $K$ 与答案分布。若 S-U 用更少 post-final-norm ROOT 方向便能保持新 context 中的已见 mapping utility，则功能压缩不能只归因于出现频率或较少 lookup 表。未见 input--rule combination 的结果单独报告，不能替代该主比较。

## 8. Secondary Metrics

分析顺序固定为：

1. **有效性 gates：**generator matching、capability、full-state utility matching、full-rank replay；
2. **唯一主指标：**post-final-norm ROOT 的 $\Delta k_{\mathrm{structure}}$；
3. **主指标守卫：**accuracy/loss 双容忍度、同秩随机空间、shuffle、等样本重采样；
4. **机制定位：**pre-final-norm ROOT 功能秩，以及 pre/post norm 差值；
5. **辅助几何：**calibration PCA replay rank、完整根矩阵 effective rank、答案原型中心化后的根残差 effective rank、within-answer residual energy 与 $r_{95}$；
6. **泛化诊断：**semantic consistency 与 unseen input--rule combination accuracy；不进入主秩判定；
7. **rival calibration：**lookup-$K$ 曲线与 repeat-diverse / repeat-duplicate；
8. **探索性桥接：**relation-conditioned gradient alignment，以及根功能秩与 $W_Q/W_K/B_{QK}$ 功能秩相关性；不得改变主 verdict；
9. **早／中层定位：**只有关闭或量化 suffix 重读取旁路后，才可称为中间层功能秩。

## 9. Known Good / Known Bad / Known Confusing Cases

**Known good：**shared generator 在 oracle implementation 中应对所有 split 给出确定答案。  
**Known bad：**随机标签或打乱 rule parameter 后，unseen-combination accuracy 应接近 chance。  
**Known confusing：**
- 最终答案类别过少使完整根矩阵天然低 rank；
- 低 rank 但 accuracy 低；
- lookup $K=1$ 可能低 rank，却没有组合泛化；
- shared 任务过难导致 floor effect。
- 最终层功能秩很低，但中间层并不低，说明只是答案读出瓶颈；
- post-norm 功能秩显著低于 pre-norm，但 shared--lookup 差异只在 post-norm 出现，说明差异可能由 final norm 接口产生；
- 投影中间层 `ROOT` 后任务保持，但移除其他 token 的后续访问即失败，说明存在 suffix 信息旁路；
- 答案条件中心化产生低谱秩，却不能作为无标签功能干预；
- PCA replay rank 高于 task-aware rank，说明任务方向不是高能量方向。

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear | Debug artifact | Handoff |
|---|---|---|---|---|---|
| Generator audit | 边际、split、答案是否匹配 | manifests | exact checks | generator table | training |
| Capability | 所有 Stage A 条件是否学会 | calibration curves | gate above | curves by seed | root extraction |
| Root extraction | pre/post-final-norm ROOT 与注册位置是否正确 | cached states | shape/sample checks | state manifest | intervention |
| Final-norm audit | 主差异是否只由 final norm 接口产生 | paired pre/post curves | post-norm primary; pre-norm localization | norm comparison table | boundary |
| Replay audit | hook、全秩重放与 shuffle 是否正确 | replay outputs | required controls | replay table | functional rank |
| Functional-rank audit | shared 是否有功能秩优势 | primary table | protocol rule | loss-rank curve | mechanism |
| Spectrum audit | 功能压缩是否伴随谱集中 | residual states | secondary only | spectrum plot | bridge |
| Rival audit | lookup $K$ / duplicate 是否解释 | Stage B/C | descriptive/guard | rival tables | verdict |

## 11. Algorithm Specification

**Input：**trained checkpoints、calibration/test root states、calibration/test task labels。  
**Parameters：**root layer/position、子空间优化合同、$k$ 网格、$(\epsilon_L,\epsilon_A)$、bootstrap seeds。  
**Steps：**

1. 按 condition/seed 读取 calibration 的 pre-final-norm 与 post-final-norm ROOT states；
2. 用 calibration 全局均值与标签分别拟合各 $k$ 的 task-aware $U_k$；
3. 在 test 上投影 post-norm 主状态并重放冻结 LM head；
4. 次级地投影 pre-norm 状态并重放真实 final norm 与冻结 LM head；
5. 验证 full-rank、zero-rank、shuffle 和 random-subspace controls；
6. 由持久阈值定义 $k_{\mathrm{func}}$；
7. 另用 calibration 答案原型计算 test 根残差谱；
8. 计算 paired seed differences 与 paired bootstrap CI；
9. 严格按 gates、主指标、守卫、pre/post norm 定位、几何、泛化、rival 的顺序报告。

**Outputs：**

- `tables/capability_gate.csv`
- `tables/root_functional_rank.csv`
- `tables/root_functional_rank_pre_post_norm.csv`
- `tables/root_projection_replay_curve.csv`
- `tables/root_effective_rank_secondary.csv`
- `tables/lookup_k_calibration.csv`
- `tables/diverse_duplicate_guard.csv`
- `figures/root_functional_rank_by_condition.png`
- `figures/root_projection_loss_curve.png`
- `figures/root_spectrum_secondary.png`

## 12. Success / Failure / Insufficient Evidence

### Success

- 所有 Stage A 条件通过 capability；
- S-U 与 L-U 通过主 held-out split 的 matched full-state utility gate；
- S-U 在附加组合泛化 split 上达到 unseen-combination accuracy $\ge 0.80$ 与 semantic consistency $\ge 0.95$；该项只确认 shared generator 被作为组合规则学习，不要求 L-U 猜测未见随机表项；
- $\Delta k_{\mathrm{structure}}\ge\delta_k$；
- paired 95% CI 下界 $>0$；
- 至少 4/5 seeds 同号；
- full-rank replay、shuffle 与同秩随机空间守卫通过；
- 功能秩结果在 accuracy/loss 双容忍度和等样本重采样下方向一致；
- lookup-$K$、答案瓶颈与 final-norm 定位不能解释全部主差异。

### Failure

- matched 后 shared functional-rank advantage 不存在；
- shared 的低功能秩被最终答案瓶颈或 task collapse 解释；
- lookup $K$ 完全解释功能秩；
- low-frequency shared 无法通过主 utility gate，或通过能力匹配后没有功能秩优势。

### Insufficient

- 任一主要 condition capability 失败；
- generator marginal/split guard 失败；
- root extraction、projection hook 或 full-rank replay 不稳定；
- task-aware 子空间对 calibration 过拟合，test 结果不稳定；
- 主功能干预使用 test 答案选择原型；
- effect 只在一个 seed / 一个 metric 出现；
- 需要事后延长训练或改 generator 才能得到结论。

## 13. What This Cannot Claim

- 自然语言语义结构已被证明为树；
- 所有低频关系高秩或所有高频关系低秩；
- 根表示 rank 与参数 rank 相同；
- NTP 一般产生低秩空间；
- 单条数据学会后自身从高维变成低维；
- 低 rank 对 MoE Router 有直接价值；
- shared rule 在真实 LLM 中按相同方式编码。

## 14. Review Notes And Protocol Changes

已冻结的人工裁定：

1. 接受 shared composition 与 independent lookup 的基本对照；
2. 要求明确并严格匹配 $K,F,D$、答案边际、样本、序列、训练和测量合同；
3. 主功能秩 split 使用新 context 中的已见 mapping；未见组合只作 shared 泛化诊断；
4. post-final-norm ROOT 为唯一主状态，pre-final-norm ROOT 为次级定位；
5. 主指标为 calibration-only task-aware 功能秩；PCA 与谱指标降为辅助；
6. 冻结 $\epsilon_L=0.02$ nat、$\epsilon_A=0.01$、$\delta_k=4/64$、5 seeds、4/5 同号与 paired 95% CI 下界大于 0；
7. capability gate 与 paired full-state utility matching 均为硬门；
8. Protocol 已批准并完成四卡 full run；冻结判据给出
   `insufficient`，不得用失败能力门下的秩值裁定主假设。

修改记录：

```text
2026-07-23: 初始中文审核稿；未授权运行。
2026-07-23: 主判据由根残差 effective rank 修订为 held-out 根状态任务功能秩；加入 label-leakage、重放、随机子空间、答案瓶颈与 suffix 信息旁路守卫；仍未授权运行。
2026-07-23: 经用户审核修改批准；冻结严格匹配清单、主/附加 test 分离、post-norm 主判据、pre-norm 次级定位、指标顺序、能力匹配门与效应阈值；尚未授权实现或运行。
2026-07-23: 用户授权并完成四卡 full run，ACP job `pt-q6hu0fq5`，35/35 任务结束。低曝光 shared/lookup 主对比均未通过 held-out 能力门，正式判定为 `insufficient`。详见 [summary_cn.md](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/summary_cn.md) 与 [detailed.md](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/detailed.md)。
```
