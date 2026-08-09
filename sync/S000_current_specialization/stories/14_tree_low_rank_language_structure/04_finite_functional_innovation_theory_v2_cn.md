# 有限功能创新空间：A14 条件功能秩理论证明 v2

## 从概率活动树、NTP 任务更新到冻结读出秩预算

**文档状态：**A14 中文理论 v2；本文件是有限功能创新定理的当前中文正文，双语综合叙事仍由 story 03 维护。  
**理论范围：**受控 NTP 模型与显式优化动力学条件；不是任意 Transformer 或自然语言定理。  
**核心认识：**训练路径上的局部 Jacobian 坐标可以旋转；稳定对象是完整训练后、冻结输出头可见的有限任务创新并集。

状态标签：`[已证明]` 表示结论由文内条件推出；`[显式假设]` 表示可证伪但尚未由一般 NTP 推出；`[实验支持]` 只表示当前受控模型中的证据；`[尚未解决]` 表示开放桥。

## 1. 问题、活动树与秩对象

**NTP（next-token prediction）**是用前缀预测下一个 token 的交叉熵训练目标。本文问：它何时只需少量跨样本共享的任务功能方向？

**任务 mapping** 是把局部任务充分变量变成后续任务状态的可复用函数。只有在训练互斥的合法 context 或组合上仍有正确行为，才称该 mapping 已学会；训练集拟合不够。

设潜在 mapping 库为 $\mathcal F=\{f_1,\ldots,f_K\}$。输入 $x$ 诱导随机活动模式 $M(x)=m$，并调用活动集合

$$
\mathcal A(m)\subseteq\mathcal F.
$$

把这些调用及依赖展开得到**概率活动树**；它是一次条件计算轨迹，不是语言本体。树中只计算未被后代状态重复包含的局部任务创新。

- **单输入活动预算 $s$：**头部模式满足 $|\mathcal A(m)|\le s$。
- **共享 mapping 并集预算 $k$：**大多数样本的活动集合都包含于同一 $\mathcal H_\star$，且 $|\mathcal H_\star|\le k$。
- **每 mapping 自由度 $r$：**一个 mapping 对冻结读出可贡献的独立有限创新方向至多为 $r$。

若头部事件 $\mathcal E_\star=\{\mathcal A(M)\subseteq\mathcal H_\star,\ |\mathcal A(M)|\le s\}$ 满足 $\Pr(\mathcal E_\star)\ge1-\delta_M$，则 $s$ 控制单样本并发预算，$k$ 控制跨样本方向并集；二者不可互换。

**post-final-normalization ROOT** 是最终归一化之后、冻结语言模型输出头之前的注册任务位置状态，记为 $h_\rho(x;\theta)$。

固定参考端点 $\theta_{\mathrm{ref}}$ 与训练终点 $\theta_T$，定义精确有限任务效应

$$
\Delta h_\rho(x)
=h_\rho(x;\theta_T)-h_\rho(x;\theta_{\mathrm{ref}}).
$$

冻结输出头 $W_o$ 后，两个状态功能等价，当且仅当它们产生完全相同的 logits：

$$
h_1\sim h_2
\quad\Longleftrightarrow\quad
W_oh_1=W_oh_2.
$$

记商空间 $\mathcal Q=\mathbb R^d/\ker W_o$，$[h]$ 表示忽略冻结头不可见分量后的等价类。模式 $m$ 的**有限功能创新空间**是

$$
\mathcal I_m^{\mathrm{fin}}
=\operatorname{span}\{[\Delta h_\rho(x)]:M(x)=m\}.
$$

它控制完整训练后真正改变冻结读出行为的方向，不控制 raw hidden geometry、完整参数矩阵或输出头零空间中的 nuisance（与任务无关变化）。`[定义]`

**冻结读出功能秩**允许只用 calibration split 选择子空间，随后冻结该子空间和 $W_o$，不读取 final-test 标签。对候选 $B\subseteq(\ker W_o)^\perp$，令

$$
h_{\rho,B}(x)=h_\rho(x;\theta_{\mathrm{ref}})+P_B\Delta h_\rho(x),
$$

并定义

$$
k_{\mathrm{func}}^{\mathrm{fix}}(\epsilon;m)
=\min_B\left\{\dim B:
\mathbb E[(\ell(W_oh_{\rho,B},Y)-\ell(W_oh_\rho(\theta_T),Y))_+\mid M=m]
\le\epsilon\right\}.
$$

该量是“在保留 reference/base 的重放中，多少有限效应方向足以保持终点行为”；它不是完整 ROOT 的 raw rank。终点模型还必须先通过 held-out capability，避免把任务失败误称为低功能秩。

## 2. 原证明链保留到哪里

在受控 ROOT–softmax 模型中，$\phi_m$ 拼接活动 mappings 的任务系数，$R_m$ 把任务参数块送到 ROOT。单样本 NTP 梯度具有外积形式

$$
\nabla_{\Delta\Theta}\ell
=R_m^\top W_o^\top(p-e_Y)\phi_m^\top.
$$

若 next token 在 $(\phi_m,M)$ 给定后与 nuisance context 条件独立，且 nuisance 特征 $\psi$ 满足 $\mathbb E[\psi\mid\phi_m,M]=0$，则零 nuisance 写入点的 population gradient 为零。独立 contexts 使经验 nuisance 梯度按 $n_{\mathrm{eff}}^{-1/2}$ 集中；重复同一个 context 仍有 $n_{\mathrm{eff}}=1$。`[已证明：条件结论 T2/T3]`

若每个 mapping 的任务系数空间至多 $r$ 维，任务梯度左右因子均落在固定子空间，且优化器保持该矩阵子空间，则模式 $m$ 的参数任务更新秩至多为 $r|\mathcal A(m)|$。`[已证明：条件结论；一般逐坐标 AdamW 不自动满足]`

但低维参数任务更新不推出低维 ROOT 效应：令一个标量更新 $\alpha$ 在 context $x_i$ 上产生 $h_\rho(x_i;\alpha)=\alpha e_i$，参数方向只有一个，跨样本 ROOT 增量却可有任意秩。`[已证明：严格反例]`

所以原链中的必要缺口仍是

```text
低维参数任务方向
→ context-dependent 参数到 ROOT 作用
→ 冻结读出可见的有限功能方向
```

## 3. 不可能性命题：行为复用不等于隐藏几何复用

**命题。** common mapping 的行为复用、held-out capability 与低 NTP loss，不能单独推出完整隐藏状态具有共享低维 finite image。`[已证明]`

**证明。** 取任意已经实现正确 next-token logits 的任务状态 $b(x)$。增加 $n$ 个隐藏坐标并令冻结头为 $W_o'=[W_o\ 0]$。选择线性独立的 $u_1,\ldots,u_n\in\mathbb R^n$；其扩展向量 $[0;u_i]$ 均属于 $\ker W_o'$。定义

$$
\Delta h_\rho'(x_i)=\begin{bmatrix}\Delta b(x_i)\\u_i\end{bmatrix}.
$$

则 $W_o'\Delta h_\rho'(x_i)=W_o\Delta b(x_i)$，所以 mapping 行为、预测、held-out capability 和每个样本的 NTP loss 完全不变；但 raw finite-effect 矩阵可因 $\{u_i\}$ 达到随 context 数增长的秩。$u_i$ 还可由 context-dependent 旋转坐标生成。故这些行为事实不约束完整隐藏空间的共享线性几何。证毕。

该命题排除的是“语言复用自动等于内部线性基复用”；它不排除冻结读出商空间中的有限功能低维。`[已证明；边界]`

## 4. 精确路径恒等式与新的主优化假设

对任意连接两端点的可微训练路径 $\theta(t)$，微积分基本定理给出

$$
\Delta h_\rho(x)
=\int_0^1J_\rho(x;\theta(t))\dot\theta(t)\,dt.
$$

这是一条精确恒等式，不是单点线性化。`[已证明]`

路径旋转不否定有限低维。例如若

$$
J_\rho(x;\theta(t))\dot\theta(t)
=b\,\dot a_x(t)+\dot q_x(t),
\qquad q_x(0)=q_x(1)=0,
$$

则瞬时 $q_x(t)$ 可以沿 context-specific 高维方向旋转，积分后却完全抵消，终点效应只剩 $b(a_x(1)-a_x(0))$。因此局部坐标的并集秩与 endpoint finite image 的秩是不同对象。`[已证明：构造例]`

对 calibration 选择的候选空间 $B_m$，定义精确功能路径残差

$$
\eta_{\mathrm{path}}(m;B_m)
=\mathbb E\!\left[
\left\|W_o(I-P_{B_m})\Delta h_\rho(x)\right\|_2
\mid M=m\right].
$$

**主优化假设。** 对当前模型的每个已学 mapping $f_j$，存在有限功能创新子空间 $\mathcal I_j^{\mathrm{fin}}\subseteq\mathcal Q$，$\dim\mathcal I_j^{\mathrm{fin}}\le r$；模式 $m$ 的 endpoint effect 在冻结头可见部分，可由

$$
\sum_{f_j\in\mathcal A(m)}\mathcal I_j^{\mathrm{fin}}
$$

表示到残差 $\eta_{\mathrm{path}}$。$B_m\subseteq(\ker W_o)^\perp$ 是该商空间之和的 calibration-admissible 代表空间。`[显式假设：可证伪的优化动力学条件]`

E05/E06 支持该假设在当前一层、一头、宽 64 的受控任务中成立；一般 NTP、任意 Transformer 和自然语言尚未推出它。`[实验支持；尚未解决]`

更强的充分条件是整条路径存在同一个固定 $B_m$，使 $J_\rho\dot\theta=B_ma_x(t)+e_x(t)$。它能通过积分推出主假设，但 E04–E06 没有支持“固定局部基贯穿训练”，因此不作为 v2 主前提。`[显式假设：更强且当前未获支持]`

## 5. 主定理：活动创新预算控制冻结读出功能秩

**定理。** 固定模式 $m$。若：

1. $|\mathcal A(m)|\le s$；
2. 每个活动 mapping 的有限功能创新维数至多为 $r$；
3. 主优化假设成立，$B_m$ 只由 calibration 决定，且测试前冻结；
4. 终点模型通过 held-out capability，reference/base 与输出头 $W_o$ 在重放中冻结；

则在容忍度 $\epsilon_m=\sqrt2\,\eta_{\mathrm{path}}(m;B_m)$ 下，

$$
k_{\mathrm{func}}^{\mathrm{fix}}(\epsilon_m;m)
\le\dim B_m\le sr.
$$

若头部事件中所有活动集合都包含于 $|\mathcal H_\star|\le k$ 的共同 mapping 并集，则存在一个共同 calibration 空间 $B_\star$，使

$$
k_{\mathrm{func}}^{\mathrm{fix}}(\sqrt2\eta_\star;\mathcal E_\star)
\le\dim B_\star\le kr,
$$

其中 $\eta_\star=\mathbb E[\|W_o(I-P_{B_\star})\Delta h_\rho\|_2\mid\mathcal E_\star]$。`[已证明：在显式条件下]`

**证明。** 活动 mapping 的商空间之和满足

$$
\dim\!\left(\sum_{f_j\in\mathcal A(m)}\mathcal I_j^{\mathrm{fin}}\right)
\le\sum_{f_j\in\mathcal A(m)}\dim\mathcal I_j^{\mathrm{fin}}
\le sr.
$$

取其在 $(\ker W_o)^\perp$ 中的代表空间 $B_m$；精确路径残差给出投影重放的 logit 误差。softmax 交叉熵满足 $\|\nabla_z\ell\|_2=\|p-e_Y\|_2\le\sqrt2$，故

$$
(\ell(W_oh_{\rho,B_m},Y)-\ell(W_oh_\rho(\theta_T),Y))_+
\le\sqrt2\|W_o(I-P_{B_m})\Delta h_\rho\|_2.
$$

取条件期望并代入功能秩定义，得到 $sr$ 结论。把活动集合替换为共同并集 $\mathcal H_\star$，同理得到 $kr$ 结论。证毕。

证明链正是：活动 mapping 数量 $\to$ 有限功能创新空间维数 $\to$ exact path residual $\to$ 冻结头 logit 误差 $\to$ softmax CE 界 $\to$ 固定读出功能秩。

## 6. 推论一：frequency 不直接决定方向预算

**推论。** 若 rare exact relation 调用的 mappings 已包含于原有限功能创新并集，终点仍通过 held-out capability，且 $\eta_{\mathrm{path}}$ 未越过同一容忍度，则降低该 relation 的频次不增加上述 $kr$ 维上界。`[已证明：条件推论]`

**证明。** 定理的维数项只含 $\dim\sum_j\mathcal I_j^{\mathrm{fin}}$；当 mapping 并集及每个创新空间不变时，样本计数不进入维数和。证毕。

frequency 仍可决定 mapping 能否学会、估计误差、margin 和 nuisance 消除；exact duplicate 不增加独立 context diversity。因此不能推出“所有 rare 数据低秩”或“频率不重要”。`[边界]`

E01 的 duplicate/diverse 对照与 lookup $K=1/4/16$ 的 $10.2/11.0/12.8$ 方向只支持变量分离。改进后 E02 在同一 common mapping 下注册

$$
D_s
=k_{\mathrm{func},s}^{\mathrm{LowF}}
-k_{\mathrm{func},s}^{\mathrm{HighF}},
$$

并得到 LowF/HighF 均值 $7.6/7.4$、$\bar D=0.2$、单侧 95% upper bound $0.5<2$，10/10 pairs 通过。strict zero-exposure unseen-cell 能力也全部超过 $0.75$ 门。因此“频次不直接进入方向并集”在当前受控 common-mapping 任务中得到支持；它仍不是自然语言或任意模型的普适结论。`[实验支持；受控边界]`

## 7. 推论二：什么时候功能秩必须增加

**推论。** 设旧评估分布已有 $q$ 维功能空间 $\mathcal S_{\mathrm{old}}$，且旧切片的任何合格空间都必须包含它。若新 mapping 或 rare exposure 的输出可见 finite effect：

1. 在商空间中位于 $\mathcal S_{\mathrm{old}}$ 之外；
2. 在正概率评估切片上具有稳定非零幅度；
3. 旧 $q$ 个方向仍各自必要，且精确 endpoint `drop-new` 隔离删除该新分量后，冻结读出任务损失越过预注册容忍度；

则联合评估分布的最小固定读出功能秩至少为 $q+1$。若有 $p$ 个彼此独立且逐一必要的新创新，则下界为 $q+p$。`[已证明：条件下界]`

**证明。** 任何合格空间必须包含仍然必要的 $\mathcal S_{\mathrm{old}}$；新效应与它线性独立且不能功能删除，所以合格空间还必须包含至少一个新方向。维数至少增加一。对 $p$ 个独立方向重复该论证。证毕。

新增 mapping 数量、参数空间外分量或 ROOT 几何新颖性本身都不足以满足条件 3。E03 原计划用 exact endpoint `drop-new` 作为因果接口，但其前置 common parameter-space gate

$$
C_{\mathrm{common}}
=\frac{\|P_{G_c}V_{\mathrm{test}}\|_F^2}
{\|V_{\mathrm{test}}\|_F^2}
$$

只有 $0.4780$--$0.6314$，0/10 达到 $0.80$，因此 full treatment 按协议停止。这个结果不能裁定新功能方向是否必要；它只表明 raw AdamW step space 不能在当前 probes 上稳定充当 common functional space。`[实验边界；尚未解决]`

## 8. 理论—实验—边界对应

| 证明步骤 | 数学状态 | 实验支持 | 当前边界 |
|---|---|---|---|
| context diversity 消除 nuisance | T2/T3：条件证明 | E01：duplicate 0/5，diverse 4/5 capability | 不等于 mapping reuse |
| 参数任务更新有效低维 | 条件参数子空间结论 | E05：八维位移捕获 0.9975，功能保持 | 不等于完整参数矩阵低秩 |
| 局部 Jacobian image 共享 | H9-L/T6-L：条件桥 | E04 5/5；tail 0.0393，capture 0.9607 | 只适用于局部更新 |
| 单点坐标跨完整训练 | H11 | E06 5/5 否定；线性化误差 1.2595 | 小更新且显式小余项时可保留 |
| exact finite functional effect 低维 | v2 主优化假设 | E06 secant capture 0.9829，重放 CE +0.00022 nat | 一般 NTP 尚未推出 |
| frequency–mapping union | 推论一 | 改进后 E02：10/10 frequency non-inferiority，95% upper $0.5<2$ | 不能声称 rare 普遍低秩 |
| 新功能方向必要性 | 推论二的条件下界 | E03：common parameter-space gate 0/10，full run parked | 未裁定功能新颖性；几何新颖不等于功能必要 |

## 9. 当前结论、不能声称与唯一开放问题

- 概率活动树、mapping 复用与每 mapping 自由度给出的是**条件方向预算**。`[已证明：在显式假设下]`
- 路径旋转只否定“一个局部坐标系贯穿训练”，不否定 endpoint 有限功能创新低维。`[已证明；E04–E06 支持当前模型]`
- 方向预算由活动功能创新的并集维数直接决定；频次只通过 capability 与误差项间接进入。`[已证明：条件推论]`
- E02 支持“common mapping 下 exact frequency 不迫使功能秩上升”；E03 同时否定了把 raw AdamW update space 无条件当作该复用机制。`[实验支持；受控边界]`
- 只有输出可见、稳定、独立且功能必要的新创新，才能给出秩增长下界。`[已证明：附加最小性条件下]`
- 不能声称 raw ROOT、完整参数矩阵、所有 rare 数据、自然语言、多层 Transformer 或 Router utility 已经低秩。`[边界]`

**唯一仍未解决的理论问题：**哪些可检查的 softmax-attention 架构条件与 NTP 优化动力学，能够推出有限功能创新假设及 $\eta_{\mathrm{path}}$ 界，而不是把它保留为当前受控模型中的经验事实？`[尚未解决]`

## 证据入口

- [原理论 v1](/daily_research_reports/backup/2026/07/0724/NTP_conditional_low_rank_theory_package/01_理论论文_共享组合结构与条件低有效秩.md)
- [A14_02 parent anchor](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor_cn.md)
- [E04](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E04_shared_jacobian_path_image/summary_cn.md) · [E05](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E05_trajectory_jacobian_closure/summary_cn.md) · [E06](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E06_reference_jacobian_vs_secant/summary_cn.md)
- [E01](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/summary_cn.md) · [改进后 E02](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E02_frequency_mapping_rank_separation/summary_cn.md) · [E03](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E03_rare_common_subspace_reuse/summary_cn.md)
