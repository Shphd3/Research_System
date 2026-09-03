---
anchor_id: 14_02_relation_reuse_root_effective_rank
status: frequency_noninferiority_supported_e03_space_blocked
canonical_language: en
companion_language: zh
line: 14_tree_low_rank_language_structure
depends_on: 14_01_relation_reuse_parameter_state_bridge
protocol_status: e02_completed_e03_parked_at_gate
---

# A14_02 共享组合规则与任务根状态功能秩


研究线基础：[A14_00 条件低秩层次结构](../14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor_cn.md)。

## 1. Problem Definition

**上位问题：**长程、层级、组合结构是否构成一种可复用且任务充分的条件计算，而不是“树天然低秩”。

**更精确的问题：**在 NTP 下，跨上下文复用的共享组合规则，是否比相同规模的独立随机 lookup 只需更少的根状态方向就能保持未见样本上的任务行为；该差异能否排除答案类别、训练失败、最终读出瓶颈和 lookup 规则数量较少等平凡解释？

**唯一决策问题：**

> 在匹配 exact relation frequency $F$、规则数量 $K$、上下文多样性 $D$、输出熵、模型和完整状态 held-out task utility 后，共享可组合规则是否只需更低维的**任务根状态子空间**就能保持 held-out utility？

### 术语

| 术语 | 含义 | 具体对象 | 不能证明 |
|---|---|---|---|
| 根状态 $h_\rho(x)$ | 读取全部任务相关 token 后、生成答案前的任务摘要状态 | 预注册 `ROOT/QUERY` 位置 hidden state | 模型内部真的使用显式树 |
| 答案语义原型 $\mu_y$ | 相同答案的平均根状态 | calibration split 上 $\mathbb E[h_\rho\mid y]$ | 因果计算路径 |
| 根残差 $r(x)$ | 去除答案类别后的上下文/计算变化 | $h_\rho(x)-\mu_y$ | 全部变化都与组合机制有关 |
| 根状态任务功能秩 $k_{\mathrm{func}}$ | 保持 held-out 任务行为至少需要的根状态方向数 | calibration 拟合子空间、test 干预重放 | 严格秩、非线性内在维度或单样本复杂度 |
| 根残差 effective rank | 根残差谱的等效方向数 | 熵有效秩；辅助诊断 | 任务充分性或因果使用 |
| task utility gate | 模型确实学会目标任务 | held-out answer accuracy / CE | 学习机制 |
| semantic consistency | 等价上下文下答案语义稳定 | 同一潜在问题的跨上下文一致率 | 表面 token 必须相同 |
| lookup 规则数量 $K$ | 需要独立记忆的映射表数量 | 数据生成器中的独立 permutation/table 数 | 实际参数中恰有 $K$ 个模块 |
| 局部 Jacobian 像 | 一个参数点处，无穷小任务参数方向诱导的 ROOT 方向 | held-out contexts 上的 $J_\rho(x;\theta)G$ | 完整训练产生的有限效应 |
| 学得 secant 像 | 一个参数块精确有限效应使用的 ROOT 方向 | $h_\rho(x;\theta_T)-h_\rho(x;\theta_{\mathrm{ref}})$ | 训练路径上的 Jacobian 基保持不变 |

## 2. Physical Priors

**P1：共享规则复用可降低任务所需自由度。**  
相同组合算子在不同上下文中重复调用，可能允许模型复用根状态形成机制，使较小的状态子空间已经足以完成任务。  
**反例：**共享规则与随机 lookup 需要相同的 held-out 任务功能秩。

**P2：答案类别会制造平凡谱集中，也会污染功能干预。**  
最终根状态可只编码有限答案类别，因此完整根矩阵低秩不等于组合计算低秩。按真实答案选择 $\mu_y$ 再做功能重放还会泄漏标签。  
**处理：**主功能干预只使用不依赖 test 答案的 calibration 均值；答案条件根残差只作几何诊断。

**P3：lookup 基数是活跃竞争解释。**  
独立 lookup 规则越少，即使完全记忆，也可能需要更少任务方向。  
**处理：**在 matched $K$ 下比较 shared 与 lookup，并单独描述 lookup-$K$ 功能秩曲线。

**P4：谱集中不等于功能压缩。**  
高能量方向可能与任务无关，低能量方向也可能决定答案。  
**处理：**直接在注册根状态处投影并重放模型后缀，以 held-out loss 和 accuracy 判定任务充分性；谱指标降为辅助量。

**P5：中间层根状态存在信息旁路。**  
若只投影中间层 `ROOT`，后续 attention 仍可从其他 token 重新读取完整输入，任务保持不代表低维 `ROOT` 本身充分。  
**处理：**主判据使用最终 LayerNorm/RMSNorm 后、LM head 前的 `ROOT`，它直接进入答案头；最终归一化前的同位置状态只作次级定位，并重放真实 final norm 与答案头。中间层只在关闭或审计后续重读取旁路时才能报告为功能秩。

**P6：跨 context 共享与训练过程稳定是两个条件。**  
一个参数点处的 Jacobian 可以在不同 contexts 间共享低维像，但该像仍可随参数
移动而旋转。完整训练结论必须显式控制 Taylor 余项，或直接使用精确的 learned
secant／路径积分像；单点 H9 不能独立承担有限位移桥。

## 3. Falsifiable Hypotheses

**主假设 H1：共享结构额外降低根状态任务功能秩。**

在相同 $K,F,D$ 和 task utility 下：

$$
k_{\mathrm{func}}(\mathrm{shared};\epsilon)
<
k_{\mathrm{func}}(\mathrm{lookup};\epsilon).
$$

该差异在低 exact-frequency 条件中仍存在，并伴随未见组合或未见上下文上的稳定效用。同向的根残差 effective-rank 差异只作为机制一致性证据，不是通过的必要替代物。

**最强竞争解释 H0：lookup 基数或最终读出瓶颈充分解释低功能秩。**

$$
k_{\mathrm{func}}
\approx f(K,F,\text{answer bottleneck}),
$$

是否具有共享组合规则不再贡献额外解释量；低功能秩只是函数表数量较少、答案类别有限或最终读出本来低维的结果。

**Pass：**

1. shared 与 lookup 均通过 matched held-out utility gate；
2. 低 exact-frequency shared 条件通过未见组合/上下文门；
3. shared 的 held-out 根状态任务功能秩相对 matched lookup 至少降低协议冻结的最小效应，且 95% 区间为正、至少 4/5 seeds 同号；
4. 学得子空间优于同秩随机子空间，完整维度重放恢复原模型；
5. lookup-$K$ 曲线不能解释 shared 的全部差异。

**Fail：**

- 控制 $K,F,D$ 后 shared 不再有功能秩优势；或
- 功能秩只由答案读出瓶颈、lookup 数量或模型未学会解释。

**Insufficient：**

- capability gate 失败；
- 样本数、答案分布、root 位置或 checkpoint 不匹配；
- 主功能干预使用了 test 答案身份，或完整维度重放失败；
- 结果依赖一个 seed、一个阈值或事后选择；
- 低频条件处于 floor effect。

## 4. Mathematical Model

对 held-out 样本 $x_i$，取最终 LayerNorm/RMSNorm 后、LM head 前的 `ROOT` 状态

$$
h_i=h_\rho(x_i)\in\mathbb R^d.
$$

仅在 calibration split 上估计不依赖答案身份的全局均值 $\mu^{cal}$，并拟合 $k$ 维正交子空间 $U_k$。在 test 上把注册根状态替换为

$$
\widetilde h_i^{(k)}
=
\mu^{cal}
+U_kU_k^\top(h_i-\mu^{cal}),
$$

然后继续运行冻结的模型后缀。设 $L_{\mathrm{test}}^{full}$ 为完整状态损失，$L_{\mathrm{test}}^{(k)}$ 为干预后的损失。对预注册损失与准确率容忍度 $(\epsilon_L,\epsilon_A)$，定义 held-out 任务功能秩：

$$
k_{\mathrm{func}}
=
\min\left\{
k:
\begin{array}{l}
L_{\mathrm{test}}^{(k)}-L_{\mathrm{test}}^{full}\le\epsilon_L,\\
A_{\mathrm{test}}^{full}-A_{\mathrm{test}}^{(k)}\le\epsilon_A
\end{array}
\right\}.
$$

协议使用“持久过阈值”：注册网格中所有更高维度均需继续通过，以避免非单调曲线上的偶然单点。$U_k$ 只能在 calibration 上拟合；test 只用于最终判定。

该定义是关于“模型、任务分布、干预层、允许的线性子空间族与容忍度”的物理量，不是单个样本的属性。若协议只沿 calibration PCA 子空间测量，则所得值是任务功能秩的可审计上界，必须按此命名；若使用 task-aware $U_k$，则需预注册优化与过拟合守卫。由于主位置紧邻答案头，该量严格解释为“完成注册答案任务所需的根状态维数”，不能自动解释为全部中间组合计算的维数。

辅助几何诊断仍用 calibration 答案原型 $\mu_y^{cal}$ 在 test 构造

$$
r_i=h_i-\mu_{y_i}^{cal},
\qquad
R_\rho=[r_1,\ldots,r_n],
$$

并报告其熵 effective rank。该量不参与主功能干预，也不能独立通过 anchor。

主比较量：

$$
\Delta k_{\mathrm{structure}}
=
\frac{
k_{\mathrm{func}}^{\mathrm{lookup}}
-
k_{\mathrm{func}}^{\mathrm{shared}}
}{
d
}.
$$

正值表示在相同 lookup 基数和暴露条件下，共享组合结构具有额外的任务充分状态压缩。

## 5. Computational Realization

使用一个可学习的受控 NTP 两步组合任务。

### Shared compositional family

输入由因子化实体、两个规则参数、nuisance context 和 `ROOT` 标记组成。潜在计算为

$$
u=\phi_{\alpha}(a),
\qquad
y=\psi_{\beta}(u).
$$

所有 rule instances 共享同一 $\phi,\psi$ 形式，只改变参数 $(\alpha,\beta)$。数据保留未见 input–parameter 组合用于测试。

### Independent lookup family

保持输入输出词表、序列长度、答案分布、规则数量和出现次数一致，但每个 rule instance 使用独立随机 permutation/table，不能由共同 $\phi,\psi$ 表达。

### 频率与多样性条件

- `unique-diverse`：每个 exact relation 只出现一次，但许多关系共享同一组合形式；
- `repeat-diverse`：同一 exact relation 在不同 nuisance contexts 中重复；
- `repeat-duplicate`：相同 surface example 重复，用于区分“出现次数”和“数据不一样”。

### 模型与目标

- 预注册小型 causal Transformer；
- full-position NTP cross-entropy；
- 根状态固定为答案前 `ROOT` 位置；
- 主干模型冻结后，在最终 LayerNorm/RMSNorm 后、LM head 前的 `ROOT` 状态进行主投影干预，并重放冻结答案头；该位置避免后续 attention 从其他 token 恢复被删除信息；
- 最终归一化前的同位置 `ROOT` residual state 只作次级定位；投影后重放真实 final norm 与冻结答案头，不能与 post-norm 主判据共同决定通过；
- 早／中层曲线只作定位诊断；除非额外关闭或量化后续 `ROOT` 对其他 token 的重读取，否则不称为中间层功能秩；
- 最终层功能秩仍可能受答案类别瓶颈限制，因此必须匹配答案分布并保持相同的注册任务；通过只能支持答案任务充分性；
- 所有条件使用相同初始化分布、优化器、训练预算和评估样本量；
- checkpoint 与子空间都由 calibration 决定，不看 test rank 或 test loss。

## 6. Minimal Falsification Tests

### 决定性测试：低频共享规则反例

比较 matched 的：

- `shared / unique-diverse`
- `lookup / unique-diverse`

**主指标：**$\Delta k_{\mathrm{structure}}$。  
**必要 gates：**完整模型 held-out utility、semantic consistency、answer balance、root-state sample count、full-rank replay、同秩随机空间；任何中间层扩展还需 suffix 信息旁路守卫。  
**为什么决定：**若 exact relation 均低频，但 shared 条件仍只需更少根状态方向即可保持未见组合效用，则“低频必然需要高任务功能秩”被直接削弱。

### Rival calibration：lookup 数量曲线

在纯 lookup 条件中改变 $K$，记录

$$
K\mapsto k_{\mathrm{func}}.
$$

该曲线只用于量化“少量 lookup 表也会产生低功能秩”的竞争解释。由于 $K$、单规则频率和总任务剂量可能互相约束，除非协议实现完全 factorial matching，否则不把该曲线单独解释为因果定律。

### 频率—多样性控制

比较 `repeat-diverse` 与 `repeat-duplicate`，检验相同出现次数下，跨上下文变化是否提供额外任务功能压缩和语义一致性。

### 与学长 Q/K 删谱实验的非重合性

| 维度 | 学长实验 | A14_02 |
|---|---|---|
| 主对象 | $W_Q/W_K$ 或 QK 参数方向 | 指定层 `ROOT` hidden state |
| 干预 | 删除参数矩阵尾部奇异方向 | 投影根状态并重放冻结模型后缀 |
| 主要结果 | 参数删谱后 A→C loss 是否保持 | 多少状态方向足以保持 held-out 任务 |
| 数据变量 | share 条件混合复用、频率与独立规则数 | 显式匹配 $K,F,D$ 后比较 shared/lookup |
| 泛化要求 | 来源实验主要定位参数鲁棒性 | 未见上下文／组合上的任务充分性 |

A14_02 因而不是复做参数删谱，而是在回答学长实验没有回答的桥接问题：参数方向集中是否对应可泛化、任务充分的状态压缩，以及共享规则是否在排除频率和规则数量后仍有额外作用。

## 7. Current Evidence

1. 已完成的
   [A14_01/E08 参数—状态桥](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/A14_E08_relation_reuse_state_bridge/summary_cn.md)
   只提供了有边界的独立重建证据：极端高复用／低规则数量条件有小幅
   held-out 状态功能秩优势，但参数压缩远大于状态压缩，中间条件不单调。
   因为它同时改变 lookup 数与单规则曝光，不能识别共享结构本身。
2. 已完成的
   [A14_02_E01 四卡实验](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/summary_cn.md)
   正式判定为 `insufficient`：
   - 低曝光主对比两组均达到 1.0 训练 accuracy，但在新 context 上 0/5
     通过，二者秩差不可解释；
   - 相同 context 重复八次仍为 0/5 通过，多样 context 的 shared 条件为
     4/5 通过；
   - 在全部通过能力门的 lookup 控制中，独立映射表数量从 1、4、16
     增加时，post-norm ROOT 功能秩均值从 10.2、11.0 增到 12.8；
   - 高曝光 shared 相对 `K=16` lookup 的四个配对秩差均值为 2.5 方向，
     低于冻结的 4 方向阈值；shared 还有一个训练失败 seed，且没有
     passing seed 通过未见组合门。
3. 因此当前证据支持把“出现次数”“上下文多样性”和“独立规则数量”
   分开，但尚未证明共享组合结构本身降低 ROOT 功能秩。
4. 独立的
   [归档 A14_02_E02-v1 能力实验](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/summary_cn.md)
   排除了基础任务能力这一解释：shared 与 lookup 的已见配对新 context
   能力均为 5/5 通过，但 shared 未见组件配对为 0/5 通过，平均 accuracy
   0.2125，远低于冻结的 0.80 门槛；四个 held-out pair 的均值也都低于
   0.70。因此，即使修正 split，当前 shared 任务仍不具备解释
   shared-versus-lookup 秩差的资格。
5. 随后完成的 H9 桥接审计把局部和有限训练版本分开：
   - [E04](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E04_shared_jacobian_path_image/summary_cn.md)
     在 5/5 seeds 支持训练完成点的注册局部 H9：八维外谱尾均值
     0.0393，calibration 到 test 捕获 0.9607；同维随机参数空间的谱尾为
     0.2206。
   - [E05](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E05_trajectory_jacobian_closure/summary_cn.md)
     发现实际 block 位移的八维捕获为 0.9975，且精确 block ROOT 效应的
     八维外谱尾仅为 0.0132；但 endpoint Jacobian 像只能捕获该效应的
     0.3672，闭包在 4/5 seeds 被否定。
   - [E06](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E06_reference_jacobian_vs_secant/summary_cn.md)
     给出决定性区分：真实 secant 在 5/5 seeds 通过八维跨 context 与功能
     正对照，单点线性化相对误差均值为 1.2595，H11 在 5/5 seeds 被否定；
     参考点 H9 本身处于中间区，并未被否定。注册后完整 block 位移方向审计
     仍以相对误差 1.2441 在 5/5 否定 H11，排除了少量轨迹空间外位移解释；
     该审计复用同一 checkpoints，不是独立确认。
6. 因此，局部跨 context 共享、低维实际参数位移和低维有限 ROOT 效应可以
   同时成立，但单点 Jacobian 不能代表完整训练位移。有限训练理论应使用
   learned secant／path-integrated image；point H9 只保留为带显式小余项的
   局部推论。当前仍没有证据证明 ROOT rank 等于参数 QK rank，或低 ROOT
   rank 会产生 Router 效用。
7. 改进后的
   [E02 frequency--mapping separation](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E02_frequency_mapping_rank_separation/summary_cn.md)
   在一个已学 common mapping 内隔离 exact frequency：10/10 paired seeds
   通过能力和 rank validity；LowF/HighF 平均功能秩为 7.6/7.4，paired mean
   difference 为 0.2，单侧 95% upper bound 为 0.5，低于两方向门。LowF 的
   零曝光 unseen-cell accuracy 在 10/10 seeds 为 1.0。该结果建立的是注册任务
   内的 frequency non-inferiority，不是 shared 对 independent mapping 的优势。
   批准的
   [E03 rare--common intervention](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E03_rare_common_subspace_reuse/summary_cn.md)
   在 treatment 前 parked：32-probe common AdamW step basis 对 held-out common
   updates 的 capture 只有 0.478--0.631，0/10 达到 0.80 稳定门。

## 8. Claim Boundary And Next Decision

**当前可以声称：**

> 在这项受控 NTP 生成任务中，重复相同样本并不足以形成新 context
> 不变性；多样 context 暴露是必要条件。对已经学会的 lookup 任务，在
> 曝光和 context 配置相同的情况下，独立映射表越多，任务 ROOT 功能秩越高。
> 在匹配已见配对能力后，注册的 shared 任务仍未形成可靠的未见组件配对
> 重组能力。在独立的 learned-common-mapping 桥接实验中，训练后的任务方向
> 具有共享局部 ROOT Jacobian 像，真实优化器位移和有限 ROOT 效应也都有效
> 八维；但单点 Jacobian 不能近似该有限效应。改进 E02 进一步表明，在严格
> 零曝光跨 surface 能力通过后，把 exact-cell frequency 从 8 降到 1 没有使
> 冻结读出 ROOT 功能秩超过两方向非劣效边界；该状态功能结果不自动给出稳定的
> raw AdamW common-update space。

**不能声称：**

- 所有低频 shared rule 都具有低 ROOT 功能秩；
- 共享组合结构导致高曝光条件下的秩差；
- E02 模型已经学会共享组合算法；
- frequency 在所有任务中无关；
- 三个 lookup 点构成普适定律；
- NTP 自动保证共享 secant 像；
- 训练路径上的瞬时 Jacobian 基保持不变；
- 自然语言或语义世界整体是低秩树；
- 参数矩阵与 ROOT 表示具有相同 rank；
- 低秩自动产生 expert specialization 或 Router utility。

**唯一下一决策：**

保留 frequency non-inferiority 的正结果；在 fresh probes 上预注册并验证
leave-target-out common ROOT-functional/secant space 后，才重试 rare-direction
intervention。
