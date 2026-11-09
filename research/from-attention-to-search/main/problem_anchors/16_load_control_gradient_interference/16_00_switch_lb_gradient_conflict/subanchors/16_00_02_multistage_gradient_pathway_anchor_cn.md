# A16_00_02 训练早中晚阶段的梯度路径审计


## 1. Problem Definition

本子 Anchor 继承 A16_00 的问题：可微负载控制是否付出了语言学习代价。唯一更窄的问题是：**在注册的早期、中期和后期状态中，running-centering 是否减少 Router 输入路径与 Gate 更新中的负载控制冲突，减少被送入同一专家的文档之间不兼容的语言模型更新，并降低 LB 分量对 held-out NLL 的即时代价？**

三个对象必须分开。Router 路径冲突是 LM 与乘上系数的 LB 梯度在实际 Router 上游表征和 Gate 权重上的余弦。专家冲突是独立 WoS 文档组在同一专家内产生的 LM 梯度相反程度；专家参数没有直接的 LB 梯度。结果代价是从同一完整状态执行 LM+LB 与 LM-only AdamW 影子一步后的独立文本 NLL 差。

## 2. Physical Priors

1. 大的 token 共享分量可能迫使负载控制消耗更新去修正公共 Router 方向；centering 在 Gate 前移除该分量。
2. 路由决定哪些文档梯度在同一专家内相遇，因此 centering 可以通过分配路径改变专家更新兼容性，而不需要 LB 直接求导到专家。
3. 原始冲突减少只有在 held-out 影子一步代价也下降时才具有学习意义，否则可能只是几何变化或有益正则。

## 3. Falsifiable Hypotheses

- **H1，Centered 中介：** 相比匹配 seed 与 checkpoint 的 Vanilla，Centered 的 Router-source/Gate LM-LB 梯度余弦更少为负，WoS 专家更新的负余弦质量更低，且 LB 引起的 held-out NLL 代价更小。
- **最强竞争解释，分配变化或有益正则：** centering 改变负载与梯度几何，但 Vanilla 的 LB 影子一步并不更有害，或专家冲突不下降。
- **控制失配解释：** LB 在该状态没有改善硬负载，因此任何质量代价都是无效干扰，而不是成功均衡所付出的代价。

只有两个 seed 都支持注册的影子一步 Centered 中介效应，结果命题才通过。共享路径与专家冲突分别给 typed verdict。checkpoint 不配对、optimizer 不完整、batch 不一致或梯度缺失均为 Insufficient。

## 4. Mathematical Model

对阶段 \(t\)、条件 \(a\in\{V,C\}\) 和共享对象 \(q\)（Router source 或 Gate），定义

\[
c^{a}_{q,t}=\frac{\langle g^{a}_{LM,q,t},g^{a}_{LB,q,t}\rangle}
{\|g^{a}_{LM,q,t}\|\|g^{a}_{LB,q,t}\|+\epsilon}.
\]

数值越大表示目标越少相反，但不能单独证明学习更好。对专家 \(e\) 与 WoS 文档组 \(d\)，\(g^{a}_{e,d,t}\) 是该组被路由 token 在该专家全部稀疏参数上产生的 LM 梯度；专家负余弦质量为

\[
I^{a}_{expert,t}=\mathbb E_{e,d\ne d'}
\left[\max\left(0,-\cos(g^{a}_{e,d,t},g^{a}_{e,d',t})\right)\right].
\]

只对达到注册最小 token 支持的 cell 加权。越低表示相反的专家更新越少。阶段主结果为

\[
\Delta NLL^{a}_{LB,t}=NLL_{WoS}\!\left(T(s^a_t,g_{LM}+g_{LB})\right)
-NLL_{WoS}\!\left(T(s^a_t,g_{LM})\right),
\]

Centered 中介效应为 \(M_t=\Delta NLL^{V}_{LB,t}-\Delta NLL^{C}_{LB,t}\)；\(M_t>0\) 支持假设。

## 5. Computational Realization

使用四层 DCLM MoE 的 Vanilla-Full 与 Centered-Full，seed 17/29，固定 50M、6B、10B 三个状态。精确重放 checkpoint 后的下一组 DCLM 全局 optimizer batch，用于 LM/LB 共享路径梯度和 AdamW 影子分支。固定、按领域分层的 WoS train 子集测专家更新冲突；独立 WoS validation 子集测影子一步 NLL；WoS test 保持未触碰。

逐层捕获 centering 之前的 Router source 张量梯度与 Gate 权重梯度。专家侧按注册的 WoS 领域分片计算 LM 梯度，只比较有足够路由 token 的专家/文档组 cell。LB 对专家参数的直接梯度必须数值为零；非零表示实现失败，不是科学结果。

## 6. Minimal Falsification Tests

决定性结果是三个注册阶段取冻结中位数后的两 seed Centered 中介效应，并给出按 WoS 文档配对 bootstrap 区间。每个 seed 至少两个阶段点估计为正，且聚合 95% 下界大于零。共享路径支持还要求每个 seed 至少两个阶段中，Centered 的 Router-source 与 Gate LM/LB 余弦均高于 Vanilla。专家支持要求每个 seed 至少两个阶段的 Centered 负余弦质量更低。

known-good 使用人工同向/反向目标；known-bad 使用零 LB 系数、打乱 LB 梯度和故意不配对 batch。硬守卫覆盖 checkpoint/optimizer 身份、batch hash、影子分支精确重放、WoS split/hash、梯度重构，以及专家直接 LB 梯度为零。

## 7. Current Evidence

完整 12 单元审计裁定为 `fail_global_centering_mediation_with_early_stage_relief`。50M 时，Vanilla 的有效 LB 影子一步使 WoS NLL 上升 0.000845/0.000617 nat/token，Centered 则无法区别于零；Centered 中介效应为 +0.000839/+0.000630，两个配对区间都高于零。但该效应不跨阶段稳定：6B 的两个点估计为负，10B 只有 seed 29 的区间为正。seed 17 的三阶段中位数区间跨零，seed 29 通过，因此两 seed 结果规则失败。

共享路径和专家冲突条款也失败。Centering 只在 50M 使 Router-source 与 Gate 梯度较少相反，6B/10B 的增益均转负；按 token 加权的专家内部负余弦质量也没有下降。Vanilla 的近零值与路由坍缩共存，不能解释为更健康的专业化。[结果记录](../../../../experiments/A16/A16_00_02_E01_multistage_gradient_pathway_audit/summary_cn.md)。

实现审计还确认，源 30B 训练虽然记录 \(\lambda_{LB}=0.01\)，但 re-entrant activation checkpointing 使嵌套辅助张量脱离 backward graph。本实验因此测量冻结状态上合格的可微反事实一步，而不是原轨迹中的长期 LB 作用。

## 8. Claim Boundary And Next Decision

本审计建立了 centering 与较低早期 LB 即时代价之间的可复现关系，同时否定“跨阶段普遍减少干扰”的解释。它不能证明一步效应解释 30B 轨迹、较低的测量冲突更健康，或 dynamic expert bias 已更好。

唯一下一决策是比较 Centered + dynamic expert bias、Centered + 真正可微 LB 与 Centered 无额外负载控制。完成标准是用匹配的硬负载与 held-out NLL/FLOP 证据分离非梯度控制和可微正则。
