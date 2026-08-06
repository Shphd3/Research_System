# MoE 长尾特征的梯度饥饿与动力学验证实验报告

## 1. 实验目标

本实验按照 [exp.md](./exp.md) 的要求，用 PyTorch 在本地完成两个 toy experiment：

1. 验证在 **Global WD** 设定下，统一 Weight Decay 会把 Tail 特征的稳态天花板压得极低。
2. 验证在有限训练步数内，**Rare Expert** 会因为低占用率而出现明显的学习迟滞；同时比较 `Global WD`、`Lazy WD` 和 `Dynamic WD` 三种实现的差异。

实验实现脚本位于 [../scripts/run_experiment.py](../scripts/run_experiment.py)。

## 2. 实验设置

### 2.1 合成数据

- 特征维度 `d = 8`
- Head 方差：`[100, 50, 20, 10]`
- Tail 方差：`[1, 0.5, 0.2, 0.1]`
- 采样方式：`x_i ~ N(0, lambda_i)`
- Teacher 参数：`beta_i = 1 / sqrt(lambda_i)`
- 标签：`y = beta^T x + eps`, `eps ~ N(0, 0.1^2)`

因此每个方向的理论目标贡献都是一致的，因为：

`lambda_i * beta_i^2 = 1`

### 2.2 评价指标

对 Head 和 Tail 两组分别计算信号存活率：

`S_sig = sum(lambda_i * a_i^2) / sum(lambda_i * beta_i^2)`

其中 `a_i` 是学到的权重。

## 3. 实验 1：稳态闭式解

### 3.1 设置

- 样本数：`N = 500000`
- 求解方式：岭回归闭式解
- Baseline：统一正则，`Gamma = 10 * I`
- Ours：分支解耦正则，Head 用 `gamma_h = 10`，Tail 用 `gamma_t = 0.1`

在本实验中，协方差矩阵近似对角，因此单维稳态近似满足：

`w_i* = lambda_i / (lambda_i + gamma_i) * beta_i`

于是闭式解的直觉非常直接：

- 对 Head，`lambda_i >> 10`，统一 WD 只会带来中等压缩。
- 对 Tail，`lambda_i << 10`，统一 WD 会把稳态解压到接近 0。
- 若把 Tail 的正则降到 `0.1`，则 Tail 的稳态天花板被显著抬升。

### 3.2 结果

| Setting | Head `S_sig` | Tail `S_sig` |
| --- | ---: | ---: |
| Baseline (uniform WD) | 55.45% | 0.28% |
| Ours (decoupled WD) | 55.45% | 55.39% |

结果文件：

- [closed_form_results.csv](../output/closed_form_results.csv)
- [closed_form_results.json](../output/closed_form_results.json)

### 3.3 结论

这个结果几乎是“教科书式”验证：

- 统一 WD 下，Head 还能保留约一半信号，但 Tail 只剩 `0.28%`，基本等于被稳态直接压死。
- 解耦后，Tail 存活率从 `0.28%` 提升到 `55.39%`，提升约 `200x`。
- Head 几乎不受影响，说明改动主要是在挽救 Tail，而不是牺牲 Head。

## 4. 实验 2：带时间轴的动力学仿真

### 4.1 设置

- 学习率：`lr = 0.01`
- 总步数：`T = 20000`
- Batch size：`32`
- 记录间隔：每 `100` 步记录一次
- 统一 WD：`gamma = 0.1`
- Frequent Expert：`p_e = 0.5`
- Rare Expert：`p_e = 0.05`
- 每个配置平均 `8` 个随机种子，并在图中绘制均值与标准差带

三种机制如下：

1. `Global WD`：未命中时仍做 `w <- w - lr * gamma * w`
2. `Lazy WD`：未命中时完全跳过更新
3. `Dynamic WD`：沿用 Lazy 逻辑，但激活时将衰减改为 `gamma_dynamic = gamma * p_e`

### 4.2 最终结果汇总

| Mechanism | Expert | Final Head `S_sig` | Final Tail `S_sig` | Tail 到达 50% 的步数 |
| --- | --- | ---: | ---: | ---: |
| Global WD | Frequent | 100.27% | 38.54% | 未达到 |
| Global WD | Rare | 87.95% | 3.86% | 未达到 |
| Lazy WD | Frequent | 100.87% | 55.41% | 1500 |
| Lazy WD | Rare | 98.28% | 52.50% | 14700 |
| Dynamic WD | Frequent | 103.42% | 70.35% | 1000 |
| Dynamic WD | Rare | 99.77% | 76.39% | 7400 |

结果文件：

- [dynamic_results_summary.csv](../output/dynamic_results_summary.csv)
- [dynamic_results.json](../output/dynamic_results.json)

### 4.3 曲线图

#### Global WD

![Global WD Tail Survival](./figures/global_tail_signal_survival.png)

#### Lazy WD

![Lazy WD Tail Survival](./figures/lazy_tail_signal_survival.png)

#### Dynamic WD

![Dynamic WD Tail Survival](./figures/dynamic_tail_signal_survival.png)

### 4.4 观察与解释

#### 4.4.1 Global WD：Rare Expert 被“持续磨损”

- Frequent Expert 的 Tail 最终只有 `38.54%`。
- Rare Expert 的 Tail 只有 `3.86%`，几乎贴地。

这说明只要未激活时依然做全局衰减，低占用专家的参数会长期承受“只有衰减、没有梯度驱动”的更新，Tail 特征最先死亡。

#### 4.4.2 Lazy WD：不会被直接压死，但会被时间拖慢

- Frequent Expert 在 `1500` 步左右就达到 Tail `50%`。
- Rare Expert 要到 `14700` 步才达到同样水平。

这和 handoff 的核心判断一致：Lazy WD 去掉了“空转衰减”，但没有解决 Rare Expert 训练时钟过慢的问题。它不是死于稳态天花板，而是死于全局训练预算有限时来不及长大。

#### 4.4.3 Dynamic WD：显著改善 Rare Expert 的 Tail 生存

- Rare Expert 的 Tail 最终从 Lazy WD 的 `52.50%` 提升到 `76.39%`
- Rare Expert 达到 Tail `50%` 的时间从 `14700` 步缩短到 `7400` 步

也就是说，把 WD 与 `p_e` 绑定之后，Rare Expert 既获得了更高的最终稳态，也减少了长尾方向上的“正则化摩擦”。

需要诚实说明的是：在本 toy 配置下，Dynamic WD **没有让 Frequent 和 Rare 在全局步数轴上完全重合**。Rare 依然更慢，只是明显好于 Lazy WD。这是因为激活频率 `p_e` 仍然直接决定了 Rare 能接收到多少次有效梯度更新；Dynamic WD 主要解决的是“正则过强”问题，而不是完全消除“训练时钟变慢”本身。

## 5. 总结

本次实验得到三个明确结论：

1. **闭式解层面：** 统一 WD 会把 Tail 的稳态天花板压到几乎为 0；分支解耦正则可以在不损伤 Head 的情况下救回 Tail。
2. **动力学层面：** `Global WD` 最危险，因为 Rare Expert 在大量未命中步上仍被衰减，Tail 几乎无法存活。
3. **有限训练预算层面：** `Lazy WD` 虽然消除了空转衰减，但 Rare Expert 仍会因为低占用率而显著变慢；`Dynamic WD` 则进一步抬高 Tail 存活率，并明显缩短 Rare Expert 的恢复时间。

因此，这个 toy experiment 支持如下结论：

- 如果不做正则解耦，MoE 中的 Tail 特征会因为统一 WD 而系统性死亡。
- 仅仅把未激活步的 WD 跳过还不够，因为 Rare Expert 仍然受限于极慢的学习动力学。
- 将正则强度与专家占用率或分支结构解耦，是挽救长尾信号的重要方向。

## 6. 复现实验

在仓库根目录执行：

```bash
python exp_tail_decay/scripts/run_experiment.py
```

默认产物会写入 `exp_tail_decay/output/`。
