# MTP common/rare 局部机制 Thinking Card

日期：2026-07-16

所有者：研究者

状态：待研究者闭卷填写。以下提示均不是研究者结论。

> 请先用自己的话填写横线，再看每项下面的候选提示。`Unknown` 是有效答案。

## Phenomenon

我真正观察到、或希望解释的现象是：

`____________________________________________________________________`

这是：

- [ ] 已有实验直接观察
- [ ] 对已有结果的解释
- [ ] 尚未验证的机制猜测

> **AI proposal—not yet the researcher’s judgment**
>
> - 低频潜在特征的标准头 rare loss 下降显著慢于 common。
> - rare 更新与 common 更新共享主导子空间，但净 rare 下降量接近零。
> - 需要区分“rare 低频”与“rare 位于 common 子空间正交补”这两个定义。

## Mechanism guess

我猜 NTP 中 `________________` 导致 rare `________________`；informative-MTP
通过改变 `________________`，使标准 NTP 主头 `________________`。

> **AI proposal—not yet the researcher’s judgment**
>
> - 高频 common 的负梯度覆盖 rare 自身信号；MTP 可能增加 rare-aligned
>   信息特异梯度。
> - rare 主要是频率饥饿而非负冲突；MTP 可能只放大已有方向。
> - MTP 产生了 common 子空间外的新方向，但后续运输/读出接口可能仍无法使用。

## Strongest rival explanation

即使 informative-MTP 的 rare loss 更好，最可能的其他解释是：

`____________________________________________________________________`

> **AI proposal—not yet the researcher’s judgment**
>
> - 只是多头、CE 项数或 loss scale 的变化，而不是未来信息。
> - 只是 common undertraining 或普通 loss reweighting。
> - 只是正则化/梯度模长效应，并没有产生 rare-aligned 新方向。

## Most uncertain point

我现在最不确定的是：

`____________________________________________________________________`

> **AI proposal—not yet the researcher’s judgment**
>
> - informative-MTP 的额外梯度是在重复 common，还是进入了 rare 所需方向？
> - rare 应定义为低频样本、低频潜在特征，还是 common 梯度子空间外的功能方向？
> - 即使形成新方向，标准头是否能在决策位置读取并使用？

## Evidence that would change my mind

如果看到 `__________________________________________________________`，
我会更相信当前机制。

如果看到 `__________________________________________________________`，
我会放弃或显著修改当前机制。

> **AI proposal—not yet the researcher’s judgment**
>
> - 支持候选：matched 对照下 $\Delta I_R>0$、$E_\perp>0$，且 common guard
>   通过；norm-matched 后结论仍在。
> - 反驳候选：$E_\perp>0$ 但 $\Delta I_R\leq0$，说明“新”不等于“有用”。
> - 反驳候选：$\Delta I_R>0$ 但 $E_\perp\approx0$，说明收益更像旧子空间复用，
>   不是新 rare 方向。

## Current next decision

我批准 / 修改 / 否决以下最小决策问题：

> 在同一个参数点，相比 matched shared-aux，informative-MTP 是否产生更大的
> rare 标准头 NTP loss 局部下降，同时不显著损害 common loss？

我的改写：

`____________________________________________________________________`

我认为本轮 rare 的主定义是：

`____________________________________________________________________`

我认为实验中最先区分的两个 rival 是：

`____________________________` versus `____________________________`

> **AI proposal—not yet the researcher’s judgment**
>
> - 保留该问题，把 $\Delta I_R$ 设为唯一主判据，把 $A_R$、$E_\perp$ 和曲率
>   作为机制诊断。
> - 若你只想先回答几何问题，可把问题降为“是否产生新方向”，但不能汇报为
>   “帮助 rare”。
> - 若你认为长期形成/使用才是核心，应明确拒绝一步问题，并接受明日无法给出
>   完整长期结论。

签名/时间：`________________`

在研究者回复和批准前，不生成正式 anchor、Protocol、代码或实验。
