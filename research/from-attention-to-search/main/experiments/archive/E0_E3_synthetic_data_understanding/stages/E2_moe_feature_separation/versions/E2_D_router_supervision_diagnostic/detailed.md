# Detailed Notes: E2-D Router Supervision Diagnostic

## Run Setup

数据：

| feature | relation | feature id | count |
|---|---|---:|---:|
| ABC | `[1,2] -> 22` | 0 | 3900 |
| DEF | `[3,4] -> 23` | 1 | 3900 |
| GHI | `[6,7] -> 20` | 2 | 3900 |
| JKL | `[8,9] -> 21` | 3 | 3900 |

模型：

```text
1-layer causal Transformer
d_model = 64
n_heads = 4
top-1 MoE FFN
num_experts = 4
expert_ffn_dim = 128
```

训练：

```text
steps = 10000
batch_size = 128
feature_router_batch_size = 128
seq_len = 32
lr = 0.0006
seeds = 20260513-20260517
```

训练目标：

$$
L = L_{\text{NTP}} + \lambda L_{\text{router-feature}}
$$

其中：

$$
L_{\text{router-feature}} =
\frac{1}{|\mathcal{B}_{feat}|}
\sum_{(t,y_f)\in \mathcal{B}_{feat}}
\mathrm{CE}(W_r h_t+b_r,\ y_f)
$$

## Smoke Check

Smoke run:

```text
variant = router_aux_lam_1_0
seed = 20260513
steps = 500
```

结果：

```text
step 1: router_ce = 1.4022, router_acc = 0.180
step 250: router_ce = 0.0031, router_acc = 1.000
step 500: router_ce = 0.0011, router_acc = 1.000
```

Smoke 通过后直接进入 full run。

## Metric Meaning

`router_acc`：在 feature prefix-end 位置，router top-1 expert 是否等于固定 feature id。

`router CE`：router logits 对真实 feature id 的交叉熵。

`NMI/ARI`：feature label 与 expert id 的聚类一致性。

`readback`：feature prefix 下预测目标 token 的概率。

`ablation drop`：删除 dominant expert 后 target probability 下降多少。

`load entropy`：expert 使用是否均匀，4 experts 的均匀上限为 $\log 4 \approx 1.386$。

## Main Result

| variant | router acc | router CE | NMI | ARI | readback | ablation drop | load entropy |
|---|---:|---:|---:|---:|---:|---:|---:|
| `moe_top1_no_lb` | 0.5100 | 1.2815 | 0.6369 | 0.4902 | 0.9951 | 0.4669 | 1.2493 |
| `moe_top1_lb` | 0.2829 | 1.3815 | 0.6452 | 0.5192 | 0.9945 | 0.4328 | 1.3859 |
| `router_aux_lam_0_1` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.9964 | 0.9587 | 1.2397 |
| `router_aux_lam_1_0` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.9962 | 0.9700 | 1.2617 |
| `router_aux_lam_5_0` | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.9963 | 0.9668 | 1.2320 |

## Routing Matrix

Baseline `moe_top1_no_lb`:

| feature | E0 | E1 | E2 | E3 |
|---|---:|---:|---:|---:|
| ABC | 0.996 | 0.000 | 0.001 | 0.003 |
| DEF | 0.250 | 0.179 | 0.311 | 0.260 |
| GHI | 0.076 | 0.122 | 0.398 | 0.403 |
| JKL | 0.041 | 0.098 | 0.394 | 0.467 |

Router auxiliary variants all form the fixed diagonal:

| feature | E0 | E1 | E2 | E3 |
|---|---:|---:|---:|---:|
| ABC | 1.000 | 0.000 | 0.000 | 0.000 |
| DEF | 0.000 | 1.000 | 0.000 | 0.000 |
| GHI | 0.000 | 0.000 | 1.000 | 0.000 |
| JKL | 0.000 | 0.000 | 0.000 | 1.000 |

## Readback By Feature

| feature | no-LB | LB | aux 0.1 | aux 1.0 | aux 5.0 |
|---|---:|---:|---:|---:|---:|
| ABC | 0.997 | 0.996 | 0.997 | 0.997 | 0.997 |
| DEF | 0.991 | 0.993 | 0.996 | 0.996 | 0.996 |
| GHI | 0.997 | 0.995 | 0.997 | 0.996 | 0.996 |
| JKL | 0.996 | 0.993 | 0.996 | 0.996 | 0.997 |

## Ablation By Feature

| feature | no-LB | LB | aux 0.1 | aux 1.0 | aux 5.0 |
|---|---:|---:|---:|---:|---:|
| ABC | 0.418 | 0.350 | 0.983 | 0.987 | 0.986 |
| DEF | 0.343 | 0.680 | 0.979 | 0.983 | 0.975 |
| GHI | 0.602 | 0.503 | 0.970 | 0.975 | 0.974 |
| JKL | 0.505 | 0.198 | 0.903 | 0.935 | 0.931 |

## Figure Index

```text
figures/router_feature_accuracy_by_lambda.png
figures/router_feature_ce_by_lambda.png
figures/routing_matrix_by_lambda.png
figures/feature_readback_by_lambda.png
figures/expert_load_by_lambda.png
figures/ablation_delta_by_lambda.png
figures/ntp_loss_and_router_aux_loss.png
```

## Raw Output

Ignored workspace:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/e2_d_router_supervision_diagnostic/
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/e2_d_router_supervision_diagnostic/
```

## Bottom Line

E2-D 是一个清楚的代码与机制诊断 pass：

```text
explicit feature signal is sufficient for clean router specialization.
```

因此，自然 E2 不 clean 的解释应从“实现是否坏了”转向“为什么 NTP objective 下 router 没有自然采用 feature identity 作为切分依据”。
