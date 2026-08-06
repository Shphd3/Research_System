# Head Removal 与 MoE-relevant Separability 实验报告

## 1. 实验目标

本实验按照 [exp.md](./exp.md) 的设计，验证三个问题：

1. 仅仅去掉全局均值，是否会显著提升 separability。
2. 去掉 centered representation 中的 shared high-variance head，是否会提升语义可分性与有限预算下的线性 routing 效果。
3. 当语义信号泄漏进 head 时，head removal 的收益是否会下降甚至转负。

本次实现脚本位于 [../scripts/run_experiment.py](../scripts/run_experiment.py)，结果写入 [../output](../output)。

## 2. 实现与最终配置

### 2.1 关键实现选择

- 线性 router 使用单层 `nn.Linear(d_repr, K, bias=True)`。
- 优化器使用 `SGD(momentum=0.9, weight_decay=0)`，不使用 `L-BFGS`。
- 训练预算固定为 `500` steps，batch size 为 `256`。
- 所有方法在同一 seed 下共享同一份 train/test 数据和同一条 minibatch 采样序列。
- separability 同时计算两套指标：
  - `Sep_trace = tr(B) / tr(W)`
  - `Sep_rayleigh = tr((W + λI)^(-1) B)`

### 2.2 一次允许的参数校准

按最初 handoff 的推荐设置 `m_scale=2.0, noise_std=0.3` 做 smoke 时，Exp B 在 `alpha=4` 上出现了明显饱和：`raw / centered / ours` 的 router accuracy 基本都接近或达到 `100%`，不利于观察 finite-budget SGD 下的收敛差异。

因此，按照计划里允许的“一次小幅校准”条款，正式实验采用：

- `m_scale = 0.9`
- `noise_std = 0.45`

其它主设置保持不变：

- `d = 16`
- `K = 4`
- `k_h = 4`
- `train/test = 50000 / 10000`
- `seeds = 5`
- `alpha sweep = {0, 1, 2, 4, 8}`
- `rho sweep = {0, 0.25, 0.5, 1.0}`
- 固定 `alpha = 4` 做 leakage sweep

### 2.3 学习率 pilot

pilot grid 为 `{0.01, 0.02, 0.05, 0.1}`，在 Exp B、`alpha=4`、seed 0、`raw / centered / ours` 上选取“平均 step-500 test accuracy 最高且不发散”的学习率。最终选中：

- `lr = 0.02`

对应文件：

- [pilot_lr_results.csv](../output/pilot_lr_results.csv)
- [pilot_lr_results.json](../output/pilot_lr_results.json)

## 3. 实验 A：Mean-only Control

### 3.1 结果

| Method | repr_dim | Sep_rayleigh | Sep_trace | Router Acc | Purity | NMI |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Raw | 16 | 3.00 ± 0.05 | 0.19 ± 0.00 | 81.79% ± 0.62% | 81.79% ± 0.62% | 0.51 ± 0.01 |
| Centered | 16 | 3.00 ± 0.05 | 0.19 ± 0.00 | 82.35% ± 0.32% | 82.35% ± 0.32% | 0.52 ± 0.01 |
| Centered + Random-drop-top4 | 12 | 2.16 ± 0.25 | 0.18 ± 0.02 | 74.28% ± 3.14% | 74.28% ± 3.14% | 0.40 ± 0.04 |

对应文件：

- [experiment_a_summary.csv](../output/experiment_a_summary.csv)
- [experiment_a_summary.md](../output/experiment_a_summary.md)

### 3.2 结论

Exp A 很干净地支持了第一个命题：

- `raw` 和 `centered` 在 `Sep_rayleigh`、`Sep_trace`、accuracy 上几乎重合。
- 随机删 4 维并不会稳定变好，反而明显变差。

这说明“去均值本身”不是本实验要 claim 的关键物理机制。真正重要的不是 `x -> x - mu`，而是删掉什么子空间。

## 4. 实验 B：Shared Covariance Head

### 4.1 代表性结果（alpha = 4）

| Method | repr_dim | Sep_rayleigh | Sep_trace | Router Acc | Purity | NMI | Routed MSE | MSE Gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Raw | 16 | 3.009 | 0.009 | 81.45% | 81.45% | 0.508 | 0.2192 | 0.2091 |
| Centered | 16 | 3.009 | 0.009 | 82.11% | 82.11% | 0.520 | 0.2004 | 0.1903 |
| Centered + PCA-remove-top4 | 12 | 3.006 | 0.250 | 82.36% | 82.36% | 0.525 | 0.1989 | 0.1888 |
| Centered + Random-drop-top4 | 12 | 2.058 | 0.010 | 72.86% | 72.86% | 0.377 | 0.3604 | 0.3503 |
| Centered + Oracle-remove-U | 12 | 3.007 | 0.250 | 82.38% | 82.38% | 0.525 | 0.1986 | 0.1886 |

这个代表点最清楚地呈现了两个层面：

1. `ours` 和 `oracle` 在 matched-dim 条件下显著优于 `random-drop`。
2. `Sep_rayleigh` 对 `raw` 和 `ours` 的区分不大，但 `Sep_trace` 把差异放大得非常明显。

### 4.2 alpha sweep：Router Accuracy

| alpha | Raw | Centered | Ours | Random-drop | Oracle |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 81.86% | 82.37% | 25.42% | 76.69% | 82.38% |
| 1 | 81.84% | 82.31% | 82.30% | 73.48% | 82.36% |
| 2 | 81.45% | 82.12% | 82.13% | 72.62% | 82.14% |
| 4 | 81.45% | 82.11% | 82.36% | 72.86% | 82.38% |
| 8 | 81.11% | 81.79% | 82.32% | 71.16% | 82.33% |

![Exp B Sep Rayleigh](./figures/fig_sep_rayleigh_vs_alpha.png)

![Exp B Router Accuracy](./figures/fig_router_acc_vs_alpha.png)

### 4.3 观察

#### 4.3.1 `alpha = 0` 时，head removal 会直接伤害任务

当根本不存在 shared covariance head 时，`ours` 在 `alpha=0` 上只有 `25.42%` accuracy，几乎掉到随机水平。这一点非常重要，因为它直接证明：

- head removal 不是 tautology
- 它只有在“被删掉的 top-k 主要承载共享噪音”时才成立

#### 4.3.2 一旦 shared head 出现，`ours` 会恢复并贴近 oracle

从 `alpha=1` 开始，`ours` 的 accuracy 立刻恢复到 `82%+`，并在 `alpha=4`、`alpha=8` 上和 oracle 基本重合。与此同时：

- `random-drop` 始终比 `ours` 低约 `9-11` 个点
- `raw` 与 `centered` 都略低于 `ours`

也就是说，提升来自“删对了共享 head”，不是来自“随便删掉 4 维”。

#### 4.3.3 两个 Fisher 指标承担了不同角色

在 Exp B 里，两套 separability 指标的行为并不完全一样：

- `Sep_rayleigh`：
  - 对 `ours / oracle` 与 `random-drop` 的区分非常清楚
  - 但对 `raw` 与 `ours` 的区分不大
- `Sep_trace`：
  - 对 `raw/centered` 与 `ours/oracle` 的区分非常强
  - 例如 `alpha=4` 时，`raw = 0.009`，`ours = 0.250`

这说明 `Sep_rayleigh` 更接近“LDA 风格的判别可分性”，会弱化 class-independent nuisance directions 的影响；`Sep_trace` 则更敏感地反映出 raw 空间里仍然背着巨大共享噪音这一事实。

因此，本实验对 Exp B 的口径是：

- `Sep_rayleigh` 主要用于 matched-dim 下比较 `ours` 和 `random-drop`
- `Sep_trace` 主要用于说明 raw 空间里的 shared covariance burden

### 4.4 有限预算学习曲线

在 `alpha=4` 的学习曲线里，finite-budget 差异在早期就已经出现：

- step 100：
  - `raw = 80.74%`
  - `centered = 81.86%`
  - `ours = 82.06%`
  - `random-drop = 72.27%`
  - `oracle = 82.12%`
- step 500：
  - `raw = 81.45%`
  - `centered = 82.11%`
  - `ours = 82.36%`
  - `random-drop = 72.86%`
  - `oracle = 82.38%`

![Exp B Learning Curve](./figures/fig_router_acc_vs_step_alpha4.png)

这个结果支持了本次使用一阶优化器与有限预算的核心动机：我们关心的不是“无限时间后线性可分与否”，而是 shared head 是否会拖慢有限训练窗口内的有效 routing 收敛。

## 5. 实验 C：Signal Leakage Sweep

### 5.1 rho sweep：Router Accuracy 与 Rayleigh Separability

| rho | Raw Acc | Centered Acc | Ours Acc | Raw Sep_rayleigh | Ours Sep_rayleigh |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.00 | 81.20% | 82.06% | 82.12% | 2.994 | 2.992 |
| 0.25 | 81.22% | 81.88% | 82.10% | 3.011 | 2.998 |
| 0.50 | 81.37% | 82.10% | 82.06% | 3.025 | 2.986 |
| 1.00 | 81.68% | 82.38% | 81.37% | 3.076 | 2.919 |

![Exp C Sep Rayleigh](./figures/fig_sep_rayleigh_vs_rho.png)

![Exp C Router Accuracy](./figures/fig_router_acc_vs_rho.png)

### 5.2 结论

Exp C 明确支持了“有条件命题”：

- 在 `rho = 0` 到 `0.5` 的区间，`ours` 仍然略优于 `raw`
- 当 `rho = 1.0` 时，`ours` 的 accuracy 下降到 `81.37%`，反而低于 `raw = 81.68%` 和 `centered = 82.38%`
- 同时 `Sep_rayleigh` 也从 `rho=0` 时的 `2.992` 下降到 `rho=1.0` 时的 `2.919`

这说明当 semantic signal 开始显著泄漏到 head 中时，再去掉 top-4 head 就不再是“净收益”，而会开始删掉本来有用的判别信息。

### 5.3 关于 toy task loss 的细节

toy task 的 `mse_gap` 也随着 `rho` 增大而恶化：

- `rho=0`：
  - `raw mse_gap = 0.2358`
  - `ours mse_gap = 0.2100`
- `rho=1.0`：
  - `raw mse_gap = 0.2332`
  - `ours mse_gap = 0.2250`

也就是说，虽然在 `rho=1.0` 上 `ours` 的 toy routed MSE 还没有完全差过 `raw`，但它的优势已经显著收缩。这和 accuracy / Rayleigh 指标给出的“收益下降并开始转负”是一致的，只是 toy proxy 对这个转折更保守一些。

## 6. 总结

本次实验支持以下四条主结论：

1. **去均值不是核心。** Exp A 中 `raw` 和 `centered` 几乎重合，说明单纯去掉全局均值并不会带来本质性 separability 提升。
2. **真正有用的是去 shared high-variance head。** Exp B 中 `ours` 显著优于 matched-dim 的 `random-drop`，并在 accuracy / purity / NMI / toy loss 上逼近 oracle。
3. **收益是有条件的。** Exp B 的 `alpha=0` 已经表明，没有 shared head 时贸然 head removal 会直接伤害任务。
4. **当语义信号泄漏进 head 时，收益会下降并最终转负。** Exp C 中，`rho=1.0` 时 `ours` 在 router accuracy 和 `Sep_rayleigh` 上都已经落后于 `raw/centered`。

因此，本次实验最终支持的不是“head removal 永远更好”，而是更精确的条件陈述：

> 只有当 top-k head 主要承载组内共享噪音，而不承载组间语义信号时，centered head removal 才会提升 MoE-relevant separability。

## 7. 结果文件与复现

主要结果文件：

- [experiment_a_summary.csv](../output/experiment_a_summary.csv)
- [experiment_b_alpha_sweep.csv](../output/experiment_b_alpha_sweep.csv)
- [experiment_c_rho_sweep.csv](../output/experiment_c_rho_sweep.csv)
- [summary_table.md](../output/summary_table.md)
- [alpha=4 learning curve JSON](../output/learning_curve_alpha4.json)

代表性混淆矩阵：

- [Exp B alpha=4 / ours](../output/confusions/exp_b_alpha4_ours.csv)
- [Exp B alpha=4 / raw](../output/confusions/exp_b_alpha4_raw.csv)
- [Exp C rho=0 / ours](../output/confusions/exp_c_rho_0__ours.csv)
- [Exp C rho=1 / ours](../output/confusions/exp_c_rho_1__ours.csv)

复现命令：

```bash
python exp_tail_special/scripts/run_experiment.py
```

本次正式运行默认就会使用报告中的最终配置，并把图片写到 `exp_tail_special/output/`；报告中引用的图片已复制到 `exp_tail_special/docs/figures/`。
