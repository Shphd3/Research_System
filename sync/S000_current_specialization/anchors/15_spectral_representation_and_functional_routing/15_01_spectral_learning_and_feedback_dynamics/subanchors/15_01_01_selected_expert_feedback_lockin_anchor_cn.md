---
anchor_id: 15_01_01_selected_expert_feedback_lockin
parent_anchor: 15_01_spectral_learning_and_feedback_dynamics
status: completed_pass_feedback_lockin
canonical_language: en
created: 2026-07-31
---

# A15_01_01：已选专家反馈是否锁定 head-first 路由？

## 1. Problem Definition

线性 Gate 会更早学习高方差 head 坐标。当前唯一问题是：后续只训练已选专家，
是否会形成 incumbent（先发专家）的效能优势，使本来有用的 middle/tail（M/T）
变量无法再纠正早期粗分区。

> 当 H/M/T 按数据生成真值共同决定损失最优专家时，相比计算量匹配的
> oracle-functional coverage，只训练当前选中专家是否会降低后续 M/T 路由纠错？

本 Anchor 检验受控 MoE 中的反馈机制，不主张自然 DCLM 的 covariance M/T
已经有功能价值；A15_05 并未给出这种证书。

## 2. Physical Priors

1. covariance 各向异性会使 Gate 更早学到高方差坐标。
2. top-1 选择使已选专家获得更多与当前分区一致的训练更新。
3. 已选专家可能变成局部更优动作，即使早期分区遗漏了决定真值的细变量。
4. 若反馈是关键，只改变专家更新覆盖、同时固定 Router 所见信息与更新总量，
   应当改变 M/T 纠错结果。

## 3. Falsifiable Hypotheses

**H1（反馈锁定）：** selected-only 更新造成 incumbent 优势和 challenger 饥饿；
按真值给专家功能覆盖会恢复正确细专家的相对效能，并提高 held-out M/T 纠错。

**最强 rival（只有方差延迟）：** M/T 纠错只由输入方差和训练时间决定。固定
Router 输入、初始化、数据、优化器和每 token 一次专家更新后，更新覆盖方式不会
产生有意义的 paired-seed 差异。

其他 rival 是 M/T 信号不可读、任务不需要专家分化，或结果来自额外计算；信号
正控、专家真值正控和一更新/token 账本分别排除它们。

## 4. Mathematical Model

令独立平衡比特 $h,m,t\in\{-1,+1\}$，损失最优专家为

$$
e^*(h,m,t)=4\mathbf 1[h=+1]+2\mathbf 1[m=+1]+\mathbf 1[t=+1].
$$

三个等维频带各编码一个不可缺少的比特：

$$
x_b=s_b(bv_b+\sigma\epsilon_b),\qquad(s_H,s_M,s_T)=(4,2,1),
$$

三带标准化信噪比相同，只有整体方差不同。payload $p$ 的目标是
$y=A_{e^*}p$；专家 $e$ 学习 $W_ep$。随机 top-1 Router 从
$a\sim\operatorname{softmax}(Wx)$ 采样，并只观察已选专家损失
$\ell_a=\|W_ap-y\|_2^2$。

因果对照只改变谁获得专家更新：

$$
a_{\mathrm{update}}=
\begin{cases}
a,&\text{selected-only},\\
e^*,&\text{oracle-functional coverage}.
\end{cases}
$$

两组每个 token 都只有一次专家更新。主结果是细粒度纠错准确率

$$
C_{MT}=\tfrac12[\Pr(\hat m=m\mid\hat h=h)+\Pr(\hat t=t\mid\hat h=h)].
$$

## 5. Computational Realization

使用最小八专家合成 MoE：Router 输入24维（H/M/T各8维），一个线性随机 Gate，
八个可训练线性专家。两因果 arm 成对复用 minibatch、Gate/专家初始化、策略优化器、
熵日程和训练步数。正式种子分配到单个8卡节点；每张卡独立完成若干完整种子，
先写 rank-local 证据，再确定性合并。

初始 Gate 只编码 head bit，并在两个 head 半区各偏好一个 incumbent；它不读取 M/T。

## 6. Minimal Falsification Tests

1. **信号门：** 监督式 Gate 必须能在 held-out 上从 H/M/T 恢复 $e^*$。
2. **专家功能门：** 固定 oracle 专家时，$e^*$ 必须是唯一 held-out 最低损失专家。
3. **匹配反馈检验：** selected-only 与 oracle coverage 都保持每 token 一次专家更新。
4. **机制审计：** 测正确 challenger 更新份额，以及 incumbent 相对正确 challenger
   的损失优势。
5. **方差 rival：** 两因果 arm 使用完全相同的各向异性 Router 输入。

## 7. Current Evidence

A15_00 说明真实 Gate 对 covariance head 响应更强；A15_00_E03-S 说明方差会
因果改变有限时间学习速度。A15_05 没有给固定 DCLM M/T 频带功能证书。因此本次
将 M/T 功能直接写入数据真值，只检验 selected-expert feedback 是否足以造成锁定。
这些既有结果都没有提前回答本问题。

研究者已于2026-07-31预先授权 E01 的实现与完整运行。

E01完成32个正式paired seeds。selected-only最终$C_{MT}$中位数为0.500，
oracle-functional coverage为0.977；成对中位效应+0.477，95%区间
[0.476,0.479]，M/T分量效应都约+0.477。32/32计算、可读性、bandit反馈和
初始head护栏通过，32/32也出现注册的“incumbent更优/challenger饥饿”方向。
8×5090正式job `pt-15rmvipu`成功。

## 8. Claim Boundary And Next Decision

结果说明selected-expert co-adaptation在本受控系统中足以锁定head-first分区；
不能说明它解释真实DCLM、自然M/T有用，或oracle coverage可部署。

**唯一下一决策：** 在已知层级latent variable的四层受控模型中，检验稀疏
challenger或counterfactual coverage能否解除同一反馈闭环。完成条件是计算匹配、
逐层功能真值和held-out任务loss，而不是只看route recovery。
