# A06_03_02_E01 实验总结：Learned Specialist 的 Wrong-Rank Correction

## 结论

在 300 步 router-only full-LM 训练中，native weighted top-1 无法从初始 rank 2
或 rank 4 找回 learned useful expert：两个条件均为 `0/128` 纠正，majority
boundary change 均为 0。完全相同 router 初态的 soft mixture 在两个 rank 上均为
`128/128` 纠正；中位持续纠正时间分别为 29 和 98 步。

rank 4 的 top-1-minus-soft 删失纠正时间差为 203 步，按 seed 聚类的 95% CI 为
\([202,205]\)；normalized cumulative regret 差为 0.7387，95% CI 为
\([0.7342,0.7416]\)。

因此，A06_02_03_E02 固定 expert toy 中的“逐 rank 搜索”没有迁移到 learned full-LM
场景。这里出现的是更强的 **selected-path blind basin**：只要 useful expert 未被
选中，rank 2 并不比 rank 4 更容易纠正。

## 术语解释

| 术语 | 具体含义 | 计算 | 当前作用 | 不能证明 |
| --- | --- | --- | --- | --- |
| useful expert | correct exposure 后 forced task loss 最低的 specialist | \(u(f)=f\) | 功能路由目标 | 自然语义 |
| wrong-rank start | useful expert 初始不在 top-1 | rank 2 或 4 | 检验身份纠正 | 真实出现频率 |
| 持续纠正 | useful expert 连续五步在至少 95% task positions 上 top-1 | \(T_{corr}\) | 排除瞬时 crossing | 永久稳定 |
| 删失时间 | 未纠正单元记作 301 | \(\widetilde T_{corr}\) | 保留失败单元 | 完整生存分析 |
| 归一化累计后悔 | 相对 useful-expert floor 的时间平均 routing excess | \(NR\) | 训练效率证据 | wall-clock 效率 |
| utility coverage | 进入 forward loss 的 expert outputs | top-1 为 1 个，soft 为 4 个 | 机制干预 | 等 activated compute |

## 精确设置

- 四个等频上下文 modular tasks；开头 instruction \(f\) 决定后续目标
  \((c+f)\bmod4\)。
- 序列长 33，全部 32 个 next-token positions 进入训练 loss。
- 一层 causal attention、residual + LayerNorm、四个 MLP experts；无 learned
  positional embedding。
- 200 步 expert-only exposure 重建 specialists/generalists。
- correction 阶段冻结 experts 与 representation，只训练 router。
- full-batch SGD，learning rate 0.001，300 步。
- 所有 rank 使用同一 score ladder \([0.75,0.25,-0.25,-0.75]\)，只 permutation
  expert identity；top-1/soft 使用完全相同 router tensor。
- 32 seeds，每个条件 128 个 task-seed cells。

## 核心结果

| Specialist 条件 | 纠正率 | 中位删失时间 | 中位 boundary changes | 最终 task loss | Normalized regret |
| --- | ---: | ---: | ---: | ---: | ---: |
| top-1 rank 1 | 1.000 | 0 | 0 | 0.0244 | 0.2239 |
| top-1 rank 2 | 0.000 | 301 | 0 | 6.3844 | 1.0133 |
| top-1 rank 4 | 0.000 | 301 | 0 | 6.3817 | 1.0132 |
| soft rank 1 | 1.000 | 0 | 0 | 0.0648 | 0.3299 |
| soft rank 2 | 1.000 | 29 | 1 | 0.0755 | 0.1552 |
| soft rank 4 | 1.000 | 98 | 1 | 0.1178 | 0.2750 |

top-1 rank4-rank2 的删失时间差为 0，CI 为 \([0,0]\)；regret 差的 CI 跨零。
所以 H1 rank-mediated top-1 correction 被证伪。rank-4 top1-soft 的时间与
regret 差均可靠为正，H2 utility-coverage advantage 得到支持。

## 核心图

![纠正曲线](figures/useful_expert_correction_curves.png)

soft rank 2/4 最终全部纠正；top-1 rank 2/4 始终重合在 100% 未纠正。结果不是
“rank 4 比 rank 2 慢”，而是两个 wrong ranks 都没有发生身份搜索。

![训练后悔轨迹](figures/normalized_regret_trajectory.png)

soft rank 4 将 normalized routing excess 降到约 0.025；两个 wrong-rank top-1
反而略高于初始值 1。soft 优势具有 task-loss 含义，不只是 route geometry 改变。

![rank-4 身份搜索](figures/rank4_identity_search.png)

soft 将 useful probability 从约 0.102 提升到 0.575，并发生一次 majority boundary
change；top-1 将其降到约 0.088，且 boundary change 为 0。

## 有效性与控制

- specialist utility gap 中位数 8.8947；generalist -0.0042；
- train/test useful-rank accuracy 最低为 1.000；
- p05 adjacent gap 最低 0.4724；load spread 为 0；
- train center-score error 最大 \(1.97\times10^{-4}\)；
- top-1/soft 与 non-router state error 均为 0；
- rank-1 top-1/soft 都是 128/128 稳定；
- generalist arbitrary-target correction 在 top-1/soft 下均为 0/128。

generalist control 说明 soft 不会仅凭几何标签强制回到 expert \(f\)；specialist
soft correction 依赖 learned expert function。

## 假设更新

| 假设 | 裁定 |
| --- | --- |
| top-1 从 rank 2 到 rank 4 纠正更慢 | 证伪；两边都完全停滞 |
| soft utility coverage 改善 rank-4 correction 与 regret | 支持 |
| 不存在实质 sparse-feedback bottleneck | 证伪 |
| correction 只是几何重标记 | 被削弱；generalist target 不纠正 |

## 边界与下一决策

**可以声称：** 在当前 learned context-task bridge 上，weighted top-1 能保持正确
route，却不能在 300 步内从 rank 2/4 发现 useful specialist；让所有 expert
outputs 进入 forward loss 可以消除该盲区。

**不能声称：** 自然语言 semantic specialization、from-scratch feature discovery、
soft routing 在 production 中更优，或所有 top-1 MoE 永久 lock-in。

**下一唯一决策：** 从同一 wrong-rank state 将 full-LM router gradient 精确拆成
task-position 与 background-position 两部分。若 task-only top-1 仍失败而
task-only soft 成功，方法必须加入 candidate utility coverage；若 task-only top-1
能纠正但 full-LM 失败，方法目标应转为 semantic-credit weighting，并把 MTP 作为
长程 route credit 的候选来源。

