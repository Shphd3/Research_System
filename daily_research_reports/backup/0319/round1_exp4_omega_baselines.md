# exp_multihead Round1 Exp4（Omega + Baselines）实验报告

## 1. 实验具体描述

### 1.1 实验对象
- 模型：`Qwen3-4B`
- 数据：`river-martin/web-of-science-with-label-texts`（`train`）
- 领域：`CS, Medical, ECE, Civil`
- 层：`4, 16, 30`
- 头：每层取 `head_0 ~ head_7`
- 特征：每条样本在指定层 `q_proj` 的 head 向量（token mask 平均池化）

### 1.2 方法与指标
- 目标指标：子空间重叠度
  \[
  \Omega(\mathcal S_i,\mathcal S_j)=\frac{1}{k}\left\|U_i^\top U_j\right\|_F^2
  \]
- **Exp4-A（Spike vs Random）**：同层 head 两两计算 Spike 子空间 \(\Omega\)，并与随机子空间先验比较。
- **Exp4-B（Tail vs Tail）**：同层 head 两两在 \((R,r)\) 网格下计算 Tail 子空间 \(\Omega\)。
- **Exp4-C（Cross-Layer Spike）**：跨层 \((4,16),(4,30),(16,30)\) 的 head 组合计算 Spike 子空间 \(\Omega\)。

### 1.3 本次运行配置说明
- 本次已完成结果来自：`results/round1_multihead_layers_4_16_30`
- `head_dim=128`（见 layer 配置快照）
- Spike 扫描 `k={4,8,16,32,64}`
- Tail 扫描 `R={4,16,32,64}, r={8,16,24,32,48,64}`
- 随机基线试验次数：`64`
- 说明：本次结果是“固定 rank 网格”版本；后续脚本已支持按 `head_dim` 的百分比自动换算。

## 2. 实验结果与指标解读

### 2.1 结果目录结构
- 结果根目录：`exp_multihead/results/round1_multihead_layers_4_16_30/exp4_omega_baselines/`
- 表格：
  - `tables/spike_vs_random.csv`：逐层、逐 head-pair 的 Spike 与随机基线对比
  - `tables/spike_vs_random_aggregate.csv`：按层聚合
  - `tables/tail_vs_tail.csv`：逐层、逐 `(R,r)`、逐 head-pair 的 Tail 重叠
  - `tables/tail_vs_tail_aggregate.csv`：按层与 `(R,r)` 聚合
  - `tables/cross_layer_spike.csv`：跨层逐 head-pair
  - `tables/cross_layer_spike_aggregate.csv`：跨层聚合
- 图像：
  - `figures/spike_vs_random.png`
  - `figures/tail_vs_tail_layer_4.png`
  - `figures/tail_vs_tail_layer_16.png`
  - `figures/tail_vs_tail_layer_30.png`
  - `figures/cross_layer_spike.png`

### 2.2 关键定量结论

#### A) Spike 相对随机基线显著抬升（核心结论）
- 按层平均 `lift_over_random`：
  - `layer_4`: `+0.0411`
  - `layer_16`: `+0.1122`
  - `layer_30`: `+0.2004`
- 按层平均倍率 `mean_omega_spike / mean_random`：
  - `layer_4`: `1.49x`
  - `layer_16`: `2.51x`
  - `layer_30`: `3.54x`
- 代表点（`k=16`）：
  - `layer_4`: `0.1590 vs 0.1241`（`+0.0349`）
  - `layer_16`: `0.2492 vs 0.1241`（`+0.1251`）
  - `layer_30`: `0.4057 vs 0.1241`（`+0.2816`）
- 原始 head-pair 统计中，`layer_30` 在全部 `k` 上均为 `spike > random`（比例 `1.000`），显示最强结构化一致性。

#### B) Tail vs Tail 呈现“前段有结构，后段趋近随机”的分层现象
- 在固定 `R` 下，`r` 从 `8 -> 64` 时，`Omega` 单调上升（所有层均明显成立）。
- 小带宽 `r=8` 时更能区分是否接近随机：
  - 随机先验（`k=8`）约 `0.0642`
  - `R=64` 时：
    - `layer_4`: `0.0651`
    - `layer_16`: `0.0719`
    - `layer_30`: `0.0686`
  - 说明深尾部更接近随机先验。
- 但 `R=4`（靠近 spike 边界）时显著偏高，尤其 `layer_30_R4,r=8=0.2464`，说明“1%之后的早期 tail”仍携带结构信号，不可简单视作纯噪声。

#### C) Cross-Layer Spike 显示层间语义漂移
- 跨层均值（所有 `k` 平均）：
  - `16 vs 30`: `0.2476`（最高）
  - `4 vs 16`: `0.2058`
  - `4 vs 30`: `0.1905`（最低）
- 结论：相邻层的 spike 一致性高于跨度更大的层对，符合“层深语义逐步漂移”的预期。

## 3. 对假设的更新（基于 Exp4）

- **H3（多头一致性）**：多头一致性很弱？需要进行分析，可能似乎比随机高一些，但是还是不高。