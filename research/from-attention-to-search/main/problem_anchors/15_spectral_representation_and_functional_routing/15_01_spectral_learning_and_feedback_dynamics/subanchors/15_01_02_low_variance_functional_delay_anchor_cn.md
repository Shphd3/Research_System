---
anchor_id: 15_01_02_low_variance_functional_delay
parent_anchor: 15_01_spectral_learning_and_feedback_dynamics
status: completed_weak_pass_delay_strong_fail
canonical_language: en
created: 2026-07-31
---

# A15_01_02：低方差路由接近随机，还是只学得更慢？

## 1. Problem Definition

只看低 route churn（换专家比例）不够，因为随机 Gate 也可能持续路由错误。
本实验唯一问题是：

> 当同一个可学习标签以相同标准化信噪比编码在等维 H/M/T 中时，原生低方差
> tail 是否像无标签随机基底一样，无法同时达到“正确且持续”；还是它只需要
> 更多优化时间？

## 2. Physical Priors

1. 原始 SGD 更新随输入幅度变化，低方差坐标覆盖固定随机初始化所需时间更长。
2. 标准化信噪比固定时，低方差不等于标签信息消失。
3. flip 单独没有功能含义：稳定错误与稳定正确必须分开。
4. 能量均衡应消除方差造成的时间差，但不能挽救无标签随机对照。

## 3. Falsifiable Hypotheses

**强 H1（tail 随机化）：** 在注册时限内，native tail 没有达到功能稳定，且
没有明显优于同尺度无标签随机对照；equal-energy tail 则达到稳定。

**弱 H1（有限时间延迟）：** native H/M/T 最终都到达同一正确稳定分区，但
\(T_{FS,H}<T_{FS,M}<T_{FS,T}\)；能量均衡明显缩小该时间差。

**最强 rival：** 所谓 tail 漂移来自只看 flip 或信号强度未匹配。控制正确率与
标准化信噪比后，tail 只是较慢，并不随机化。

## 4. Mathematical Model

对平衡标签 \(z\in\{-1,+1\}\)，三个独立8维 block 都编码同一标签：

\[
x_b=s_b(zv_b+\sigma\epsilon_b),\qquad(s_H,s_M,s_T)=(4,2,1).
\]

每个频带训练相同容量的二分类线性 Gate。equal-energy 条件把 M/T 放大到 H 的
幅度；匹配随机条件以无标签噪声替代 \(zv_b\)，同时保持维度和尺度。

固定 held-out panel 上，\(A_b(k)\) 是准确率，\(F_b(k)\) 是相对上次评估发生预测
变化的样本比例。功能稳定时间定义为

\[
T_{FS,b}=\min\{k:A_b\ge0.90\ \land\ F_b\le0.02
\text{，连续三次评估成立}\}.
\]

单位是 optimizer step；时限内未通过按 right-censored（右删失）记录，不虚构
一个数值。

## 5. Computational Realization

生成成对在线 minibatch 和固定 held-out panel，同时训练 native H/M/T、
equal-energy H/M/T 与无标签随机对照。它们共享优化器、batch、初始化范数、
评估频率和时限。正式种子分配到单个8卡节点，只有 rank-local 完整性通过后
才合并。

## 6. Minimal Falsification Tests

1. **可学性护栏：** equal-energy H/M/T 必须超过0.90准确率并达到功能稳定。
2. **随机护栏：** 无标签随机对照必须保持机会水平附近，不能通过功能稳定。
3. **native 顺序：** 估计 H--M--T 的 paired \(T_{FS}\) 差异与种子不确定性。
4. **均衡检验：** 比较 native tail 与 equal-energy tail 的功能稳定时间。
5. **长时限护栏：** native tail 若较晚通过，只能报告延迟，不能叫随机化。

## 7. Current Evidence

A15_00_E03-S 已说明受控 covariance 比例改变 Gate 的有限时间学习速度，能量
均衡会恢复顺序。但既有 A15 实验没有要求频带路由同时“正确且持续”，也没有
在匹配标准化信噪比下把 native tail 与无标签随机基底比较。本 Anchor 拥有这项
缺失的功能稳定性裁定。

研究者已于2026-07-31预先授权 E01 的实现与完整运行。

E01完成全部32个正式种子。native H/M/T都是32/32达到功能稳定，restricted
mean分别为552、912、1,938步；equal-energy T为615步，比native T缩短68.3%。
random H/M/T均0次误通过，最终准确率约0.50；native T最终准确率0.953，全部种子
最晚在step 2,460通过。因此强“tail随机化”猜想Fail，弱“有限时间延迟”猜想Pass。

## 8. Claim Boundary And Next Decision

结果支持方差造成的有限时间延迟，并在注册matched-SNR线性系统中否定tail随机化；
不能证明语义稳定性、真实DCLM收敛或专家训练收益。

**唯一下一决策：** 在四层受控layer×band画像中，用“正确性+持续性”作为稳定性
轴。完成条件是预先定义逐层latent target；否则route churn仍没有功能含义。
