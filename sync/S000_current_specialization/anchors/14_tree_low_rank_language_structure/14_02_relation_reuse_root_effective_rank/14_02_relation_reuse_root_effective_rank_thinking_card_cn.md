---
status: human_approved_with_amendments
candidate_line: A14_02_supporting_mechanism
approved_date: 2026-07-23
protocol_or_run_authorized: false
human_amendments:
  - primary_rank_object_is_semantic_conditioned_active_tree_root_representation
  - held_out_task_functional_rank_is_primary_causal_metric
  - root_residual_effective_rank_is_secondary_geometric_diagnostic
  - primary_intervention_must_not_use_test_answer_identity
  - downstream_utility_and_semantic_consistency_are_required_gates
  - lookup_rule_count_is_the_strongest_rival
---

# 共享组合规则是否降低任务根状态的功能秩 — Thinking Card

## Human Draft

**Phenomenon / 现象：**

学长的 NTP 合成实验中，`share16` 同时具有更少的独立 A→C lookup 规则、更高的单规则出现频率，以及更大的规则内上下文复用；它学习更快，并更耐受 $W_Q/W_K$ 尾部删谱。

我希望解释的不是单独的参数矩阵现象，也不只是根状态的谱是否集中，而是：

> 在 NTP 下，跨上下文复用的层级/组合规则，是否会使活动树根状态只需更少的线性方向就能在未见样本上保持 downstream task utility？

“相同答案语义内的根残差 effective rank”保留为辅助几何诊断，用来判断功能压缩是否伴随谱集中；它不再代替任务功能秩。

**Mechanism guess / 机制猜想：**

若许多不同输入和上下文调用同一个组合规则，模型可复用相同的中间计算。对于语义答案相同的样本，去除答案类别均值后，根表示的剩余变化应集中在较少方向。

候选链条：

$$
\text{共享组合规则跨上下文复用}
\rightarrow
\text{计算与梯度方向复用}
\rightarrow
\text{held-out 任务所需的根状态方向数降低}.
$$

**Strongest rival explanation / 最强替代解释：**

低任务功能秩可能只是因为独立 lookup 规则较少、函数基数较小，或者最终答案头本身形成了低维瓶颈。即使模型完全死记硬背，只要需要区分的 lookup 表减少，根状态也可能只需较少方向。

因此必须比较相同规则数量、相同 exact relation frequency、相同输出熵和相同上下文多样性下：

- 属于一个共享可组合规则族的映射；
- 相互独立的随机 lookup 映射。

还应单独改变 lookup 规则数量，描述纯记忆情况下有效秩如何变化。

**Most uncertain point / 最不确定之处：**

根状态的低谱有效秩是否真的对应任务充分的压缩，而不是有限答案类别、表示坍缩或高能量 nuisance。主判据必须直接干预根状态并重放模型后缀，测量 held-out loss；按答案语义中心化只用于辅助谱诊断。

主功能干预不得用 test 样本的真实答案选择 $\mu_y$。否则答案原型本身可能泄漏正确标签，使低维残差产生平凡的任务保持。

**Evidence that would change my mind / 改变判断的证据：**

我会削弱或放弃当前机制，如果：

1. 共享规则和独立 lookup 在匹配条件下具有相同的 held-out 根状态任务功能秩；
2. 功能秩只随 lookup 规则数量变化，与是否存在共享组合规则无关；
3. 低频但共享规则的条件不能在未见组合或未见上下文上泛化；
4. 谱有效秩降低，但同维投影不能保持任务，说明几何集中并不任务充分；
5. 功能秩优势只出现在最终答案读出层，不能定位到组合状态；
6. 中间层 `ROOT` 投影后的效用由其他 token 的后续重读取恢复，而不是由低维 `ROOT` 保留；
7. 梯度一致性、根表示谱集中和功能秩之间没有稳定关系。

我会支持该机制，如果：

1. 低 exact-frequency 的共享规则仍通过未见组合与语义一致性门；
2. 在相同 lookup 数量、频率、输出分布和上下文下，共享规则只需更小的根状态子空间即可保持 held-out utility；
3. 学得的低维子空间优于同秩随机子空间，完整维度重放恢复原模型；
4. lookup 规则数量确实能降低纯记忆条件的功能秩，但不能解释共享规则的额外优势；
5. 谱有效秩与任务功能秩的方向关系跨 held-out split 和 seeds 稳定；任何中间层结论还通过 suffix 不重读其他 token 的旁路守卫。

**Current next decision / 当前唯一决策：**

审核并决定是否运行一个最小受控实验：

> 在匹配 exact relation frequency、上下文多样性、独立规则数量、输出熵、模型和完整状态任务效用后，共享可组合规则是否比独立随机 lookup 只需更低维的活动树根状态，就能保持 held-out task utility？

## Optional Formalization

**Key variables / 关键变量：**

- $K$：独立规则或 lookup 表数量；
- $F$：每个 exact relation 的出现次数；
- $D$：同一规则内的上下文多样性；
- $h_\rho(x)$：读取全部任务相关 token 后、答案前的根状态；
- $\mu_y=\mathbb E[h_\rho\mid y]$：答案语义原型；
- $r(x)=h_\rho(x)-\mu_y$：语义条件根残差；
- $R_\rho=[r(x_1),\ldots,r(x_n)]$；
- $r_{\mathrm{eff}}(R_\rho)$：根残差有效秩；
- $\mu^{cal}$：不依赖 test 答案的 calibration 根状态均值；
- $U_k$：仅在 calibration 上拟合的 $k$ 维根状态子空间；
- $k_{\mathrm{func}}(\epsilon)$：根状态被投影到 $U_k$ 后，仍能在 test 上把损失增量控制在 $\epsilon$ 内的最小持久维数；
- $U_{\mathrm{heldout}}$：下游任务效用；
- $S_{\mathrm{semantic}}$：等价上下文中的答案语义一致性。

**Primary observable metric / 主要观测指标：**

对 calibration-only 拟合的根状态子空间，在 test 上执行干预：

$$
\widetilde h_\rho^{(k)}
=
\mu^{cal}+U_kU_k^\top(h_\rho-\mu^{cal}),
$$

并定义：

$$
k_{\mathrm{func}}(\epsilon)
=
\min\left\{
k:
L_{\mathrm{test}}^{(k)}-L_{\mathrm{test}}^{full}\le\epsilon
\right\},
$$

实际判定要求相邻更高维度持续通过，而不是单点偶然过阈值。该量测量在注册干预位置保留任务行为所需的线性方向数；它依赖任务、数据分布、干预层和容忍度，不是单条样本的属性，也不是非线性内在维数。

**Secondary geometric metric / 辅助几何指标：**

继续报告 $r_{\mathrm{eff}}(R_\rho)$。它只测量相同答案语义内的谱能量集中，不能替代功能干预。

**Pass / fail / insufficient：**

- **Pass：**共享规则在低 exact frequency 下仍通过未见组合 utility 门，并在匹配 lookup 条件下具有稳定、非平凡的更低 held-out 根状态任务功能秩；学得子空间优于同秩随机空间。
- **Fail：**功能秩主要由 $K$、答案读出瓶颈或任务难度解释；共享结构没有额外效应。
- **Insufficient：**任务未学会、输出类别/样本数不匹配、功能投影使用 test 答案、完整状态重放失败、结果只来自一个 seed 或一个事后 checkpoint。

## AI Audit Record

**Judgments to preserve / 必须保留的人的判断：**

1. 学长测的是参数矩阵谱；本问题主对象是活动树根表示矩阵。
2. “学会”由稳定语义决策和 downstream utility 决定，不由低秩单独决定。
3. 低频与低秩没有必然关系，需要构造共享规则反例。
4. 纯 lookup 规则数量是最强竞争解释。

**Candidate correction proposed by AI / AI 候选修正：**

“确定语义表达”应解释为等价输入下答案语义稳定，而不是要求开放式表面 token 序列完全 deterministic。

**Human decision on the proposal / 人的最终确认：**

本卡依据 2026-07-23 用户进一步裁定，将 held-out 任务功能秩提升为主判据，将答案条件根残差 effective rank 降为辅助几何诊断；protocol 仍需按该判断修订和审核，当前不授权运行。
