# exp_tail_router 完整实验报告 v2

本报告整合了原始 full 实验与后续 `baseline_lb` 增量实验，作为当前唯一推荐查阅的总报告。  
它覆盖并取代：

- [baseline_lb_addendum_v1.md](/data/250010109/spectral_router/exp_tail_router/docs/baseline_lb_addendum_v1.md)

## 1. 实验目标

本实验要回答三个问题：

1. 在存在巨大均值偏移和高方差共享 head 噪音时，普通 router 是否会被 head geometry 主导而失效？
2. `Centered Tail Router` 是否能在不加任何 load balancing loss 的前提下恢复语义可分性？
3. 如果只给 `baseline` 加 load balancing loss，而不改变其输入表征，是否足以修复问题？

因此，本轮最终比较 5 个变体：

1. `baseline`
2. `baseline_lb`
3. `mean_centered`
4. `uncentered_tail`
5. `centered_tail`

## 2. 实验设计

### 2.1 数据生成

数据由 [generate_tail_router_probe.py](/data/250010109/spectral_router/exp_tail_router/data/generate_tail_router_probe.py) 生成。

固定配置：

- 隐空间维度：`128`
- 训练样本数：`20000`
- 评估样本数：`5000`
- syntax head rank：`4`
- semantic class 数：`8`
- 每类 semantic subspace rank：`4`
- 均值向量范数：`50`
- head 标准差：`[100, 50, 25, 12]`

构造流程：

- 先采样均值向量 `mu`
- 再构造 4 个正交 head 方向 `U_head`
- 再构造 8 组正交 semantic tail 子空间 `U_tail^(c)`
- 每个样本 `x = mu + x_head + x_tail`
- 标签只由 `x_tail` 决定

本轮使用 3 个 seed：

- `20260413`
- `20260414`
- `20260415`

数据目录：

- `/data/250010109/spectral_router/exp_tail_router/data/generated/tail_router_probe_v1/seed_20260413`
- `/data/250010109/spectral_router/exp_tail_router/data/generated/tail_router_probe_v1/seed_20260414`
- `/data/250010109/spectral_router/exp_tail_router/data/generated/tail_router_probe_v1/seed_20260415`

### 2.2 模型结构

训练脚本为 [train_tail_router_probe.py](/data/250010109/spectral_router/exp_tail_router/train/train_tail_router_probe.py)。

统一结构：

- gate 输入：`preprocess(x)` 后再经过无参数 `LayerNorm(128, elementwise_affine=False)`
- gate：`Linear(128 -> 8)`
- 8 个 experts：`Linear(128, 64) -> ReLU -> Linear(64, 8)`
- Top-1 routing
- expert 输出完整 8 维 logits
- 主任务 loss：`CrossEntropyLoss`

这意味着：

- 每个 expert 都有能力独立完成全部 8 类分类
- 如果仍能形成语义专精，不是因为我们限制了 expert 表达能力

### 2.3 Router 变体

#### `baseline`

- `preprocess(x) = x`

#### `baseline_lb`

- `preprocess(x) = x`
- 与 `baseline` 唯一差别：训练时加入 auxiliary load balancing loss

#### `mean_centered`

- 使用 debiased `mu_ema`
- `preprocess(x) = x - mu_debiased`

#### `uncentered_tail`

- 使用未中心化 debiased 协方差
- 提取 top-`remove_head_rank=4` 主方向
- 构造 `P_tail = I - V_kV_k^T`
- `preprocess(x) = P_tail x`

#### `centered_tail`

- 先减 debiased `mu`
- 再用中心化 debiased 协方差提取 top-4 主方向
- `preprocess(x) = P_tail (x - mu_debiased)`

### 2.4 训练配置

统一训练配置：

- `epochs = 100`
- `batch_size = 256`
- `lr = 2e-3`
- `weight_decay = 1e-4`
- `remove_head_rank = 4`
- `ema_decay = 0.99`
- `gate_norm = LayerNorm(128, elementwise_affine=False)`
- 优化器：`AdamW`

`baseline_lb` 额外配置：

- `lb_coef = 0.01`

auxiliary load balancing loss 形式：

```text
importance = mean(probs)
load = mean(one_hot(top1))
L_lb = num_experts * sum(importance * load)
L_total = L_ce + lb_coef * L_lb
```

### 2.5 工程约束

本轮实现遵守以下工程约束：

- EMA 使用 bias correction
- 协方差更新与特征分解均在 `torch.no_grad()` 下
- 协方差和 SVD 不进入反向图
- `eval` 使用 batch size `1`
- 不对 `uncentered_tail` / `centered_tail` 加 LB loss

## 3. 实验步骤

### 3.1 原始 4 路由 full 实验

```bash
cd /data/250010109/spectral_router
GPU_IDS=0,1 DATASET_NAME=tail_router_probe_v1 RUN_PREFIX=tail_router_probe \
  bash exp_tail_router/scripts/run_tail_router_probe_sweep.sh
```

执行内容：

1. 生成 3 个 seed 的 synthetic manifold
2. 运行 `4 routers x 3 seeds = 12` 个任务
3. 生成汇总表
4. 生成 4 路由图

### 3.2 `baseline_lb` 增量实验

分别对 3 个 seed 执行：

```bash
cd /data/250010109/spectral_router
CUDA_VISIBLE_DEVICES=0 DATASET_NAME=tail_router_probe_v1 RUN_PREFIX=tail_router_probe \
  ROUTER_VARIANT=baseline_lb SEED=20260413 LB_COEF=1e-2 \
  bash exp_tail_router/scripts/run_tail_router_probe.sh
```

对 `20260414`、`20260415` 仅替换 seed。

### 3.3 输出目录

总输出目录：

- `/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1`

单 run 目录示例：

- `/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/tail_router_probe_centered_tail_seed20260413`

每个 run 包含：

- `config.json`
- `train_log.jsonl`
- `train.stdout.log`
- `metrics.json`
- `train_confusion.csv`
- `eval_confusion.csv`
- `eval_batch1_predictions.csv`

汇总文件：

- 4 路由原始汇总：
  [summary_tail_router_probe.md](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/summary_tail_router_probe.md)
- 5 路由总汇总：
  [summary_tail_router_probe_with_lb.md](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/summary_tail_router_probe_with_lb.md)

## 4. 评估指标

本报告主要关注：

- `Eval Accuracy`
- `Eval Load Variance`
- `Routing Purity Eval`
- `Diag Mass Eval`
- `Tail Variance Ratio Eval`

解释：

- `Routing Purity` 是 permutation-invariant，更适合判断是否形成了“语义簇 -> expert 簇”的专精
- `Diag Mass` 依赖 expert id 与 label id 的固定对齐，因此在没有显式绑定 expert-label 的设定下，数值可能偏低
- 所以本轮更应优先看：
  - `Eval Accuracy`
  - `Routing Purity`
  - `Tail Variance Ratio`
  - confusion heatmap

## 5. 主结果

### 5.1 五路由总表

| Router | Eval Acc | Eval Load Var | Eval Purity | Eval Diag | Tail Var Ratio |
|---|---:|---:|---:|---:|---:|
| `baseline` | `0.1286±0.0034` | `227768.8±115080.6` | `0.1408±0.0004` | `0.1272±0.0010` | `1.0000±0.0000` |
| `baseline_lb` | `0.1247±0.0020` | `11624.8±1344.8` | `0.1428±0.0016` | `0.1269±0.0042` | `1.0000±0.0000` |
| `mean_centered` | `0.1208±0.0031` | `334144.3±141179.0` | `0.1409±0.0028` | `0.1260±0.0048` | `1.0000±0.0000` |
| `uncentered_tail` | `0.8169±0.0182` | `32643.8±26950.1` | `0.4110±0.0208` | `0.1034±0.0235` | `0.0111±0.0001` |
| `centered_tail` | `0.8682±0.0096` | `31629.2±13228.5` | `0.4329±0.0293` | `0.0431±0.0236` | `0.0003±0.0000` |

### 5.2 按组解读

#### `baseline`

- 准确率接近 8 类随机水平
- 路由高度塌缩
- `Tail Var Ratio = 1.0`

结论：

- 统一 gate norm 并不能拯救 baseline
- 问题不是单纯 scale，而是 head geometry 主导

#### `baseline_lb`

- `Eval Load Var` 从 `22.8万` 降到 `1.16万`
- 但 `Eval Acc` 仍只有 `0.1247`
- `Tail Var Ratio` 仍是 `1.0`

结论：

- LB 确实能让路由更均匀
- 但不能让 baseline 看见正确语义特征
- 它只是让系统“更均匀地犯错”

#### `mean_centered`

- 和 `baseline` 一样接近随机精度
- 负载方差仍然极高

结论：

- 只减均值不够
- 未去除高方差 head 时，router 仍被噪音主导

#### `uncentered_tail`

- `Eval Acc = 0.8169±0.0182`
- 相比 baseline/mean-centered 大幅提升
- `Tail Var Ratio = 0.0111`
- `Routing Purity = 0.4110`

结论：

- 去掉 top head directions 本身已经非常有效
- 但未中心化协方差中仍残留均值相关污染

#### `centered_tail`

- `Eval Acc = 0.8682±0.0096`，全组最高
- `Tail Var Ratio = 0.0003`，全组最低
- `Routing Purity = 0.4329`，也最高

结论：

- 这是本轮最强结果
- “先中心化，再去头” 比单独去头更干净
- 在不加 LB loss 的前提下，已经明显优于所有对照

## 6. 核心结论

本轮实验支持以下结论：

1. `baseline` 和 `mean_centered` 都稳定失败，说明普通一阶 router 在强 syntax head 下几乎无法恢复语义结构。
2. `baseline_lb` 证明了一个重要反例：
   - 负载均衡本身可以被人为做出来
   - 但这并不等于语义可分性恢复
3. `uncentered_tail` 已经显著恢复分类能力，说明“移除主 head 子空间”是关键方向。
4. `centered_tail` 在 3 个 seed 上 consistently 优于 `uncentered_tail`，说明中心化后再估计协方差确实更贴近语义 tail。
5. 因此，本轮最重要的信息是：
   - **router 成败的关键不在于是否做了 LB**
   - **而在于 router 是否看到了正确的 tail geometry**

## 7. 与最初理想目标的距离

本轮结果已经足够说明主问题，但还没有达到最初最强版本的目标：

- `centered_tail` 的负载方差仍不是接近 0
- `routing_purity` 虽明显领先，但仍未接近 1.0
- confusion matrix 显示的是明显结构性偏好，而不是近乎完美的置换对角

因此更准确的表述应是：

- 本轮已经成功证明 `centered_tail > uncentered_tail >> baseline/mean_centered`
- 也成功证明 `baseline_lb` 不能替代正确的 preprocessing
- 但尚未证明“只靠 centered tail 就能达到近乎完美专精”

## 8. 图表索引

### 8.1 原始 4 路由图

- [fig_eval_accuracy.png](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/figures_tail_router_probe/fig_eval_accuracy.png)
- [fig_eval_load_variance.png](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/figures_tail_router_probe/fig_eval_load_variance.png)
- [fig_eval_routing_purity.png](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/figures_tail_router_probe/fig_eval_routing_purity.png)
- [fig_tail_variance_ratio.png](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/figures_tail_router_probe/fig_tail_variance_ratio.png)
- [fig_eval_confusion_grid.png](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/figures_tail_router_probe/fig_eval_confusion_grid.png)
- [fig_eval_expert_load.png](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/figures_tail_router_probe/fig_eval_expert_load.png)

### 8.2 含 `baseline_lb` 的 5 路由图

- [fig_eval_accuracy.png](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/figures_tail_router_probe_with_lb/fig_eval_accuracy.png)
- [fig_eval_load_variance.png](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/figures_tail_router_probe_with_lb/fig_eval_load_variance.png)
- [fig_eval_routing_purity.png](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/figures_tail_router_probe_with_lb/fig_eval_routing_purity.png)
- [fig_tail_variance_ratio.png](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/figures_tail_router_probe_with_lb/fig_tail_variance_ratio.png)
- [fig_eval_confusion_grid.png](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/figures_tail_router_probe_with_lb/fig_eval_confusion_grid.png)
- [fig_eval_expert_load.png](/data/250010109/spectral_router/exp_tail_router/output/tail_router_probe_v1/figures_tail_router_probe_with_lb/fig_eval_expert_load.png)

## 9. 建议的最终表述

如果要对外简洁陈述，本轮实验最建议的结论是：

> 在强均值偏移与高方差 syntax head 干扰下，普通 router 即使加上负载均衡也无法恢复语义分类；真正有效的是先中心化、再移除主 head 子空间的 `Centered Tail Router`。  
> 这说明问题的关键不是“如何把 token 均匀分给专家”，而是“router 是否看到了正确的 tail 几何结构”。

