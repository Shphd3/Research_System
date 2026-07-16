# 从录音出发的 low-hanging fruit

日期：2026-07-16，19:00

状态：AI 审计与候选定理；不是正式 anchor，也不是已批准的 Protocol。

英文主文档：
[04_recording_driven_low_hanging_fruit.md](04_recording_driven_low_hanging_fruit.md)

> **当前入口更新：**本文件保留导师录音到 low-hanging fruit 的推导。完整
> 理论边界、曲率修正与最终明日主题见
> [理论澄清与明日汇报锚点](05_theory_clarification_and_meeting_anchor_cn.md)。

## 录音到底要求我们解决什么

**录音确实要求把 MTP 联系进来，但没有告诉我们“MTP 能解决 common/rare
冲突”。**

导师明确表达的是：

1. 当前先回答 next-one 与 next-two 的本质因果差别；
2. MTP、扩散等训练目标只是改变表征形成方式的候选手段；
3. 根本目标是让混合表征更容易拆分；
4. 一个具体目标是让不同频率、不同类型的特征进入不同专家；
5. 每天必须关闭一个小问题，而不是继续扩写开放故事。

因此，明天最小且最符合录音的汇报主题不是“为什么 MTP 对代码有效”，也不是
“如何设计 MTP Router”，而是：

> **信息性 next-two 监督能否让低频潜在特征逃离 common 主导的共享子空间？
> 如果不能逃离，它是否只是在同一子空间里重新加权 common/rare 的妥协？**

## 保留你的两个判断

- **long tail：**低频潜在特征，不是单纯低频 token。
- **冲突：**rare 特征被学入 common 所在的同一子空间；高频 common 的更新
  方向与 rare 所需方向存在偏差时，common 更新持续覆盖 rare 更新，使 rare
  学习极慢甚至停滞。

这意味着：上一版“正交 common/rare 两模式学习率”不是当前主模型，只能作为
背景零假设。

AI 审计必须再收紧一步：**方向不同本身不等于破坏性冲突。**

- 若 $\langle g_R,g_C\rangle>0$，common 更新仍然帮助 rare；
- 若内积接近零，主要问题是 rare 出现太少、自己的更新质量不足，即“频率饥饿”；
- 只有内积为负，且被 $\pi_C\gg\pi_R$ 放大到覆盖 rare 自身信号时，才是
  破坏性 common interference。

因此今晚必须把“频率饥饿”和“负梯度覆盖”作为两个 rival 分开。

## 把你的冲突定义写成可检验公式

令 $L_C$、$L_R$ 分别为普通 NTP 主头在 common 与 rare 潜在特征上的损失：

$$
g_C=\nabla_\theta L_C,\qquad
g_R=\nabla_\theta L_R.
$$

common 与 rare 的出现频率满足 $\pi_C\gg\pi_R$。NTP 的总体训练梯度为：

$$
G_N=\pi_Cg_C+\pi_Rg_R.
$$

进行一步梯度下降后，rare loss 的一阶下降量为：

$$
D_R^N
=
\langle g_R,G_N\rangle
=
\pi_R\|g_R\|^2+\pi_C\langle g_R,g_C\rangle.
$$

$D_R^N>0$ 表示 rare loss 下降。如果 common 与 rare 梯度冲突，那么 rare
停学的条件是：

$$
\pi_C[-\langle g_R,g_C\rangle]_+
\geq
\pi_R\|g_R\|^2.
$$

左侧是高频 common 放大的破坏性压力；右侧是 rare 自己能够积累的学习信号。
这正是你刚才所说机制的最小数学化。

## MTP 必须增加什么才可能有用

为了排除“多一个头、多一个 loss 项、loss scale 改变”，主要比较必须是：

- **matched shared-aux：**第二个头仍重复 next-token 信息；
- **informative next-two：**第二个目标真正包含新增未来信息。

令两者到达共享参数的 auxiliary 梯度分别为
$a_{\mathrm{shared}}$ 和 $a_{\mathrm{info}}$。新增信息对 rare 一阶下降的
特异贡献为：

$$
\Gamma_R
=
\left\langle
g_R,\,
a_{\mathrm{info}}-a_{\mathrm{shared}}
\right\rangle.
$$

于是：

- $\Gamma_R>0$：信息性 next-two 相对 matched shared-aux 更帮助 rare；
- $D_R^{\mathrm{shared}}+\Gamma_R>0$：它足以把原本停滞的 rare 救回来。

所以“隐藏状态中信息更多”远远不够。新增梯度必须与普通主头的 rare 目标同向，
而且强到足以覆盖 common 的高频负压力。

## 一个明天可以讲清楚的不可能性结论

令 $P_C$ 是已经形成的 rank-one common 子空间投影。假设在所分析的整个局部
轨迹上：

$$
g_C,\;g_R,\;a_{\mathrm{shared}},\;a_{\mathrm{info}}
\in\operatorname{range}(P_C).
$$

那么这些梯度的任意加权和仍在 $P_C$ 中。

> **命题：**在这个条件下，MTP 不可能把 rare 特征从 common 子空间中拆出来；
> 它只能改变同一维度中 common/rare 的标量妥协。

证明只有一步：线性子空间对加权和封闭；总更新在 $I-P_C$ 上始终为零，所以重复
更新也不可能凭空产生正交的 rare 方向。

若 MTP 要在保留 common 子空间的同时形成新的 rare 方向，至少必须满足：

$$
E_\perp
=
\frac{
\left\|
(I-P_C)
(a_{\mathrm{info}}-a_{\mathrm{shared}})
\right\|^2
}{
\left\|
a_{\mathrm{info}}-a_{\mathrm{shared}}
\right\|^2+\epsilon
}
>0.
$$

$E_\perp$ 表示“未来信息特异梯度中，有多少逃离了 common 子空间”。

但它只是几何必要条件，不是充分条件。要让普通主头真正受益，还需要：

- $\Gamma_R>0$；
- common loss 不恶化；
- 新方向能跨位置保持；
- 普通主头会读取并因果使用它。

## 明天组会能够给出的 decisive 回答

建议只讲：

> **NTP 下的 rare 停学，可以形式化为共享 common 子空间中被频率放大的负梯度
> 压力。信息性 next-two 不会自动解决它：如果新增信息梯度仍留在同一个
> rank-one 子空间，MTP 只是在重新加权 common/rare 的妥协。要真正拆分
> rare，至少需要一个 common 子空间之外、且与 rare 目标一致的新梯度分量。**

这是一个新的条件性认识。它没有声称标准 MTP 已经满足该条件。

## 19:00 到明天 13:00 的唯一主线

| 时间 | 产物 | 决策门 |
| --- | --- | --- |
| 19:00–19:30 | 你确认问题、最强 rival 和改变判断的证据 | 未确认则不写 Protocol |
| 19:30–20:30 | 冻结一阶冲突公式与 rank-one 不可能性证明 | 一个定理、一个反例、一条边界 |
| 20:30–21:00 | 起草三条件最小 Protocol | NTP / shared-aux / informative-next-two |
| 21:00–23:00 | 仅在批准后，于 worker surface 做最小 sanity check | 测 $\Gamma_R$、$E_\perp$、rare loss 与 common guard |
| 23:00–23:30 | 写 pass / fail / insufficient | 不外推代码、规划或 Router |
| 09:00–10:00 | 你闭卷写结论 | 我随后只做证据与边界审计 |
| 10:00–11:00 | 连接 A11、A07 与录音 | 标出已证与假设 |
| 11:00–12:00 | 形成最小组会 brief | 一个 claim、一个表/图、一个下一决定 |
| 12:00–13:00 | 预演反驳并冻结边界 | 若你仍要求，再更新 sync、commit、push |

## 现在需要你批准或修正的三点

以下都是 AI 候选，不是你的既定判断：

1. **最强 rival：**rare 改善只是普通 loss reweighting 或 common
   undertraining，并非 MTP 产生了新方向。
2. **最不确定点：**信息性 next-two 相对 shared-aux 的梯度，是否真的包含
   $P_C$ 之外、且与 rare 目标一致的分量。
3. **改变判断的证据：**如果 informative-next-two 与 shared-aux 的
   $E_\perp$、$\Gamma_R$ 没有差别，或者 rare loss 改善但几何量没有按机制
   改变，就放弃“新增方向解释”。

你确认或修改这三点之前，不建立正式 anchor，不冻结 Protocol，也不启动实验。
