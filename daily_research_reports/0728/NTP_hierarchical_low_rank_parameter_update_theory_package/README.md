# A14 从概率树与 NTP 到低秩参数更新子空间

本包回答一个收缩后的问题：

> 共享概率树如何通过 full-position NTP exposure 与 pure SGD，在 Gaussian 满秩初始化上形成主导能量的低维 task spike，从而使完整注册参数矩阵 $W_T$ 具有低有效秩？

主对象不是 $W_T$ 的代数秩，而是

$$
\tau_{kr}(W_T)
=
\frac{\sum_{j>kr}\sigma_j(W_T)^2}{\|W_T\|_F^2}.
$$

记 $q_0:=kr$ 为注册秩预算，$q_\star:=\dim U_\star\le q_0$ 为实际任务维数；全文主指标等价写作 $\tau_{q_0}=\tau_{kr}$。

## 最强定理

在固定特征、线性可分的二类 contrast-NTP writer 中，若：

- 概率树跨 contexts 复用至多 $k$ 个 causal mappings；
- 每个 mapping 以固定坐标传递至多 $r$ 个任务自由度，且注册 writer 只接收这些任务坐标；
- 全部 prefix-position events 对同一 separator 具有正 margin；
- 每个事件在无正则 pure SGD 中获得无限累计步长质量；
- $W_0$ 为独立 Gaussian 初始化；
- $kr\le\min(d,m)$，且矩阵维数在 $T\to\infty$ 时固定；

则

$$
\operatorname{rank}(\Delta W_T)\le q_\star\le q_0=kr,
\qquad
\|\Delta W_T\|_F\to\infty,
\qquad
\tau_{kr}(W_T)\to0.
$$

有限时刻的 $W_T$ 一般仍满秩。对 learned residual MLP 和一层 Transformer，该结论需要稳定 activation envelope、指定 writer block 的持续增长和相对消失的空间外更新。

## 阅读顺序

1. [04_物理先验与假设审计.md](04_物理先验与假设审计.md)：确认每条因果箭头的现实含义、状态和反例；
2. [01_理论论文_层级NTP与低有效秩任务参数更新.md](01_理论论文_层级NTP与低有效秩任务参数更新.md)：阅读系统定义、T1--T6 与最强结论；
3. [02_证明附录.md](02_证明附录.md)：核验 SGD 归约、martingale、Gaussian bulk、outlier 与 entropy-rank 推论；
4. [03_实验协议.md](03_实验协议.md)：审批 shared/disjoint-tree × full-position/root-only 的验证合同；
5. [05_审核清单.md](05_审核清单.md)：检查证明状态、术语与交付完整性。

## 文件状态

| 文件 | 内容 | 状态 |
|---|---|---|
| [01_理论论文_层级NTP与低有效秩任务参数更新.md](01_理论论文_层级NTP与低有效秩任务参数更新.md) | 摘要、模型、T1--T6、边界 | v0.4 自包含草案 |
| [02_证明附录.md](02_证明附录.md) | 完整辅助证明与反例 | v0.4 自包含草案 |
| [03_实验协议.md](03_实验协议.md) | M0/M1 主验证与 M2 条件扩展 | 待审批，未运行 |
| [04_物理先验与假设审计.md](04_物理先验与假设审计.md) | 先验—假设—状态—falsifier | v0.4 |
| [05_审核清单.md](05_审核清单.md) | 自动与人工审核面 | 静态与数值审计已通过；人工审批待定 |
| [MANIFEST.json](MANIFEST.json) | 机器可读范围与状态 | 已更新 |

## 三种状态

### 已证明

- 受控概率树固定实现给出 $q_\star:=\dim U_\star\le q_0:=kr$；
- NTP exposure 在共享 margin 上给出 task-spike 增长下界；
- pure SGD 保持低维 writer-input 行空间，循环暴露进一步使 exposure 与 task spike 发散；
- rank-$q_0$ spike 主导 Gaussian bulk 时，$\tau_{q_0}(W_T)=\tau_{kr}(W_T)\to0$。

### 条件证明

- 小 bias/martingale leakage；
- multiclass softmax；
- learned MLP $W_2$ 与 Transformer $W_O/W_2$。

### 未证明

- 共享 teacher mappings 自动形成 learned fixed coordinates；
- full-position 无条件优于 root-only；
- 完整 Transformer 参数元组或自然语言模型普遍低有效秩。

## Protocol 的唯一决策

判断 capable learned residual MLP 是否按以下顺序闭合：

$$
\text{activation realization}
\to
\text{exposure/coherence}
\to
\text{low-tail }\Delta W_T
\to
\text{task outlier}
\to
\text{low-tail }W_T
\to
\text{held-out function}.
$$

Protocol 未获批准前不实施或运行实验。

## Repository boundary

本轮只修改 0728 focus 与本理论包；不修改 Research_System 的 anchor、story、graph 或根 sync。外部协作者同步是独立、明确授权的 curated copy，不改变本地 source of truth。
