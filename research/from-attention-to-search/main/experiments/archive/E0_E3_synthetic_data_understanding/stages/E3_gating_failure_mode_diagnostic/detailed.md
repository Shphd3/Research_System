# Detailed Notes: E3 Gating Failure Mode Diagnostic

## 1. Run Record

Smoke:

```bash
python scripts/run_e3_gating_failure_modes.py --mode smoke
```

Full:

```bash
python scripts/run_e3_gating_failure_modes.py --mode full
```

Full run 完成内容：

| item | value |
|---|---:|
| datasets | 4 |
| variants | 3 |
| seeds | 5 |
| training runs | 60 |
| steps per full run | 10000 |
| model | 1-layer causal Transformer + 4-expert top-1 MoE |

Ignored run workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/e3_gating_failure_modes/
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/e3_gating_failure_modes/
```

Mainline report figures:

```text
Projects/from-attention-to-search/main/experiments/E0_E3_synthetic_data_understanding/stages/E3_gating_failure_mode_diagnostic/figures/
```

## 2. Metric Meanings

`readback probability`：在 feature prefix 位置预测目标 token 的概率。高表示模型学会了 NTP 任务。

`NMI / ARI`：人工 feature label 与 top-1 expert id 的一致性。`1.0` 表示 clean one-feature-one-expert；接近 random baseline 表示没有按 feature 分。

`feature-linear-probe`：用 hidden state 线性预测人工 feature label 的准确率。高表示 feature identity 在 hidden representation 中可读出。

`feature-only -> expert`：只用人工 feature label 预测 learned expert id 的准确率。低表示 router choice 不是简单按 feature label 切分。

`router-projection -> expert`：用 router 权重方向上的投影预测 expert id。高是 sanity check，因为 learned router 本身就是线性投影决策。

`PCA-only -> expert`：用 hidden state PCA 坐标预测 expert id。高表示 expert choice 可以由 hidden geometry 的若干方向解释，但不等于按人工 feature label 切分。

`force_random_expert_expectation`：强制每个 expert 的预测概率后取平均。高表示多个 experts 都能支持该 feature prediction。

`mean_expert_output`：把多个 expert 输出平均后接回模型。高表示 prediction 不依赖单一 expert 的独占功能。

`zero_moe_output`：去掉 MoE 输出后的 readback。低表示 MoE path 对任务有贡献。

## 3. Core Result Tables

### 3.1 Routing Alignment

| dataset / variant | NMI | ARI | readback probability |
|---|---:|---:|---:|
| unique / no-LB | 0.724 | 0.600 | 0.995 |
| unique / LB | 0.556 | 0.398 | 0.994 |
| unique / supervised | 1.000 | 1.000 | 0.996 |
| shared-B / no-LB | 0.660 | 0.477 | 0.995 |
| shared-B / LB | 0.560 | 0.411 | 0.995 |
| shared-B / supervised | 1.000 | 1.000 | 0.996 |
| shared-target / no-LB | 0.560 | 0.386 | 0.997 |
| shared-target / LB | 0.592 | 0.462 | 0.997 |
| shared-target / supervised | 1.000 | 1.000 | 0.996 |
| crossed-factorial / no-LB | 0.625 | 0.463 | 0.997 |
| crossed-factorial / LB | 0.589 | 0.464 | 0.997 |
| crossed-factorial / supervised | 1.000 | 1.000 | 0.997 |

Interpretation:

```text
Natural router 学会任务，但只形成 partial alignment；
supervised router 保持任务能力，同时形成 clean alignment。
```

### 3.2 Predictor Decomposition

| dataset / variant | feature-linear-probe | feature-only | token / target shortcut | PCA-only | router-projection |
|---|---:|---:|---:|---:|---:|
| unique / no-LB | 1.000 | 0.539 | 0.525-0.539 | 0.941 | 0.973 |
| shared-B / no-LB | 1.000 | 0.510 | 0.456-0.502 | 0.968 | 0.984 |
| shared-target / no-LB | 1.000 | 0.435 | 0.384-0.435 | 0.908 | 0.963 |
| crossed-factorial / no-LB | 1.000 | 0.457 | 0.390-0.456 | 0.957 | 0.978 |
| unique / LB | 1.000 | 0.460 | 0.460-0.462 | 0.910 | 0.970 |
| shared-B / LB | 1.000 | 0.500 | 0.452-0.500 | 0.946 | 0.974 |
| shared-target / LB | 1.000 | 0.507 | 0.374-0.507 | 0.875 | 0.963 |
| crossed-factorial / LB | 1.000 | 0.426 | 0.366-0.368 | 0.934 | 0.976 |

Interpretation:

```text
feature label 可从 hidden 中读出；
但 learned expert id 更像 router projection / PCA geometry 的函数，
不是人工 feature label 的函数。
```

### 3.3 Component And Utility Diagnostics

| dataset / variant | learned | random expert mean | mean expert output | zero MoE |
|---|---:|---:|---:|---:|
| unique / no-LB | 0.995 | 0.796 | 0.972 | 0.355 |
| shared-B / no-LB | 0.995 | 0.756 | 0.970 | 0.440 |
| shared-target / no-LB | 0.997 | 0.874 | 0.990 | 0.251 |
| crossed-factorial / no-LB | 0.997 | 0.890 | 0.988 | 0.269 |
| unique / supervised | 0.996 | 0.299 | 0.341 | 0.038 |
| shared-B / supervised | 0.996 | 0.289 | 0.314 | 0.067 |
| shared-target / supervised | 0.996 | 0.331 | 0.346 | 0.017 |
| crossed-factorial / supervised | 0.997 | 0.459 | 0.656 | 0.037 |

Interpretation:

```text
Natural router 下，多个 experts 具有相近 utility；
supervised router 下，prediction 更依赖 feature-aligned expert。
```

`zero MoE` 不高，说明 MoE path 对 readback 有实际贡献；但 natural setting 中 `random expert mean` 和 `mean expert output` 仍然很高，说明贡献不是 clean one-feature-one-expert 的独占贡献。

### 3.4 Training Dynamics

| dataset / variant | step | NMI | feature probe acc | router margin | router entropy |
|---|---:|---:|---:|---:|---:|
| unique / no-LB | 10000 | 0.723 | 1.000 | 0.298 | 1.336 |
| unique / supervised | 50 | 1.000 | 1.000 | 4.208 | 0.173 |
| unique / supervised | 10000 | 1.000 | 1.000 | 13.347 | 0.000 |
| crossed / no-LB | 10000 | 0.626 | 1.000 | 0.321 | 1.331 |
| crossed / supervised | 500 | 1.000 | 1.000 | 7.195 | 0.013 |
| crossed / supervised | 10000 | 1.000 | 1.000 | 13.092 | 0.000 |

Interpretation:

```text
Natural training 中 feature probe 已经可分，但 router margin 低、entropy 高；
supervised training 很早形成高 margin、低 entropy、clean routing。
```

这支持 objective insufficiency：feature signal 存在，但 natural NTP loss 没有把 router 推到 clean feature partition。

## 4. Failure-Mode Attribution

| failure mode | support | evidence |
|---|---|---|
| objective insufficiency | strong | supervised router 在所有 datasets 上 `NMI=1`，natural router 只有 partial NMI |
| representation不可分 | rejected | feature-linear-probe 在所有 datasets / variants 中为 `1.000` |
| expert utility degeneracy | strong | natural setting 中 random/mean expert readback 仍高 |
| pure token shortcut | weak to moderate | token-only predictor 不足以解释 expert id；shared controls 不导致 clean token-only collapse |
| target shortcut | weak to moderate | shared-target 中 target-only 不是最强解释变量 |
| difficulty/scale routing | weak | difficulty/norm predictors 解释力低于 PCA/router projection |
| shared-path bypass | partial | zero MoE drop 明显，说明 MoE path 重要；但多个 experts 都可用，说明不是单 expert 独占 |
| early lock-in | not primary | natural early-final agreement 不稳定；supervised 快速 clean 更像 objective signal 差异 |
| LB solves routing | not supported | LB 没有让 routing 变 clean，且部分数据 NMI 低于 no-LB |

## 5. Figure Index

- `figures/predictor_accuracy_by_group_unique_uniform.png`：unique 数据下不同 predictor group 对 expert id 的解释力。
- `figures/predictor_accuracy_by_group_shared_b_uniform.png`：shared prefix-end token control。
- `figures/predictor_accuracy_by_group_shared_target_uniform.png`：shared target control。
- `figures/predictor_accuracy_by_group_crossed_factorial_uniform.png`：crossed relation control。
- `figures/nmi_over_training_steps.png`：natural vs supervised routing alignment dynamics。
- `figures/early_to_final_route_agreement.png`：早期路由与最终路由一致性。
- `figures/component_ablation_readback_drop.png`：组件删除和 forced-routing 对 readback 的影响。

## 6. Claim Boundary

可以更新的主线判断：

```text
在 synthetic trigram setting 中，模型内部知道 feature 不同；
但 natural top-1 MoE router 不一定按这些人工 feature 分 expert。
```

更准确地说：

```text
representation separability != router specialization
```

不能扩展到：

```text
真实语言 MoE 没有语义分工；
真实模型应该用人工 feature label 训练 router；
所有 router failure 都来自 objective insufficiency。
```
