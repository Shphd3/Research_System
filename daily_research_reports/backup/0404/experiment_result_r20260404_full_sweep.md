# Synthetic MoE Full Sweep 实验记录（r20260404）

## 1. 实验具体描述

- 实验对象：两层 Transformer + Layer2 Top-1 MoE 路由。
- 数据集：`continuous_hmm_v2`，三类可控数据（Type1/Type2/Type3），每类 `train=2500, val=400, test=400`，序列长度 `128`，维度 `64`。
- 对比路由：
  - `linear_running_center`
  - `acp_lite`
  - `old_diagonal_quadratic`
  - `hybrid_subspace_energy`
  - `subspace_energy`
- 训练设置：`RUN_MODE=full`，`epochs=6`，`batch=32`，`d_model=64`，`d_ff=128`，`n_experts=4`，`freeze_backbone=true`，4 卡 DDP。
- 学习率解耦：`embedding_lr=3e-4`，`router_lr=3e-3`，`backbone_lr=2e-4`。
- 输出目录：`/data/250010109/spectral_router/exp_synthetic_data/output/continuous_hmm_v2/r20260404_full_type*_*`

## 2. 结果与指标说明

- 指标定义：
  - `TaskLoss↓`：test MSE。
  - `NMI↑/ARI↑`：路由分配与 `z_token` 的对齐。
  - `CV_load↓`：专家负载均衡度（越低越均衡）。
  - `ratio_top8_last`：最后一次 eigen 日志中的前 8 特征值能量占比（用于谱结构观察）。

### Type1（Mean-separable）

| Router | TaskLoss↓ | NMI↑ | ARI↑ | CV_load↓ | ratio_top8_last |
|---|---:|---:|---:|---:|---:|
| linear_running_center | 0.46408 | 0.12427 | 0.11131 | 0.15736 | 0.62894 |
| acp_lite | 0.47565 | 0.16181 | 0.13692 | 0.46701 | 0.57591 |
| old_diagonal_quadratic | 0.46388 | 0.02281 | 0.01828 | 0.69601 | 0.62007 |
| hybrid_subspace_energy | 0.47347 | 0.09457 | 0.08338 | 0.25128 | 0.60071 |
| subspace_energy | 0.48361 | 0.02434 | 0.02607 | 0.40270 | 0.57084 |

### Type2（Covariance-separable）

| Router | TaskLoss↓ | NMI↑ | ARI↑ | CV_load↓ | ratio_top8_last |
|---|---:|---:|---:|---:|---:|
| linear_running_center | 2.23541 | 0.00471 | 0.00430 | 0.11028 | 0.50741 |
| acp_lite | 2.23631 | 0.01662 | 0.01379 | 0.25819 | 0.50787 |
| old_diagonal_quadratic | 2.23346 | 0.01310 | 0.00392 | 1.14033 | 0.50596 |
| hybrid_subspace_energy | 2.23187 | 0.01674 | 0.01319 | 0.38879 | 0.51036 |
| subspace_energy | 2.23630 | 0.02765 | 0.02825 | 0.38773 | 0.51228 |

### Type3（Hybrid-separable）

| Router | TaskLoss↓ | NMI↑ | ARI↑ | CV_load↓ | ratio_top8_last |
|---|---:|---:|---:|---:|---:|
| linear_running_center | 1.31221 | 0.02082 | 0.02024 | 0.11564 | 0.49046 |
| acp_lite | 1.31547 | 0.03862 | 0.03094 | 0.49740 | 0.47219 |
| old_diagonal_quadratic | 1.30992 | 0.01445 | 0.00977 | 0.94966 | 0.48684 |
| hybrid_subspace_energy | 1.31751 | 0.02459 | 0.02127 | 0.28247 | 0.48558 |
| subspace_energy | 1.32021 | 0.01129 | 0.01135 | 0.32706 | 0.47150 |

## 3. 关键结论与分析

- **Type1（均值主分离）**：
  - 对齐最优是 `acp_lite`（NMI/ARI 最高），符合一阶强基线预期。
  - `linear_running_center` 在 TaskLoss/CV_load 上更稳，说明“任务拟合与语义对齐”并不完全同向。
- **Type2（协方差主分离）**：
  - `subspace_energy` 在 NMI/ARI 上最优，提示纯子空间能量分支对协方差差异更敏感。
  - 但其 TaskLoss 未优于 `hybrid`，且 `linear` 的负载最均衡（CV 最低），说明“对齐提升”尚未转化为“任务损失明显优势”。
- **Type3（混合分离）**：
  - `acp_lite` 仍是对齐最优，`linear` 负载最稳，`old_diagonal` 仅在 TaskLoss 上略优但对齐弱且负载失衡明显。
  - 当前并未出现“hybrid 全面赢下 Type3”的模式。
- **关于旧 diagonal 路线**：
  - 在 Type2/Type3 上负载均衡显著更差（CV 高），且 NMI/ARI 不占优，不支持继续作为主线。
- **谱结构观察**：
  - 各路由 `ratio_top8_last` 在 `0.47~0.63` 范围，没有出现单一路由显著异常集中特征值模式，仍需结合更细粒度谱演化图判断。

## 4. 假设更新

- 支持更新：
  - `acp_lite` 仍是强一阶 comparator（尤其在 Type1/Type3 的对齐上）。  
  - 纯 `subspace_energy` 在 Type2 对齐上有优势，说明二阶子空间信息确有可用性。
- 暂不支持更新：
  - “hybrid 在 Type2/Type3 全面领先”的强结论尚未成立。  
  - “二阶路线可直接带来任务损失优势”的结论尚未成立。
- 下一步建议：
  - 在固定当前数据口径下做多 seed 复现实验（至少 3 seeds），避免单次波动误判。  
  - 对 `hybrid` 做小范围超参扫描（`low_rank`, `router_lr`, 正则），检验是否存在稳定优势区间。  
  - 报告中继续把“token-level specialization”与“严格 token semantic routing”分开表述。
