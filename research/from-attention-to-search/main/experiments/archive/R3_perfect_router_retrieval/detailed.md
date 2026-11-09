# Detailed Result: R3 Perfect Router Retrieval

## 1. Run Record

| Dataset | ACP job | Seeds | Status | Runtime |
|---|---|---|---:|---:|
| uniform | `pt-7ru2qj3m` | 20260518-20260521 | SUCCEEDED | about 5.6 min wall-clock |
| feature-long-tail | `pt-cmeqtyy1` | 20260518-20260521 | SUCCEEDED | about 3.4 min wall-clock |

每个 job 申请 4 GPUs；每张 GPU 跑一个 seed。

Run root:

```text
XingyuD/Attention_Search_Experiments/active/r2_eseries_router_retrieval/
```

Configs:

```text
configs/r3_perfect_router_uniform_full.json
configs/r3_perfect_router_longtail_full.json
```

Outputs:

```text
outputs_r3_perfect_uniform/
outputs_r3_perfect_longtail/
figures_r3_perfect_uniform/
figures_r3_perfect_longtail/
```

## 2. Specialization Sanity

| Dataset | Best valid CE | Final CE | Feature prob | Feature acc | NMI | ARI | Router acc | Router CE | Fixed diag |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| uniform | 6.6265 | 6.7172 | 0.9972 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000047 | 1.000 |
| longtail | 6.6834 | 6.7716 | 0.9129 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000044 | 1.000 |

解释：R3 的实验前提成立。RouterFeatureCE 成功实现 fixed one-feature-one-expert。

## 3. Dense Attention Sparsity

| Dataset | Top16 mass | Mass90 support | Effective support |
|---|---:|---:|---:|
| uniform | 0.934 | 12.58 | 9.12 |
| longtail | 0.953 | 10.33 | 7.47 |

解释：full block2 attention 仍有 sparse structure，retrieval 检验有意义。

## 4. Retrieval Metrics

### Uniform

| K | Method | Recall | Mass | Candidate KV | Ratio | L2 | CE delta |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | router | 0.310 | 0.346 | 8.9 | 0.279 | 1.101 | 1.4174 |
| 1 | random | 0.279 | 0.282 | 8.9 | 0.279 | 1.057 | 1.0226 |
| 1 | local | 0.404 | 0.681 | 8.9 | 0.279 | 0.420 | -0.0006 |
| 2 | router | 0.536 | 0.528 | 16.9 | 0.529 | 0.846 | 0.8960 |
| 2 | random | 0.530 | 0.530 | 16.9 | 0.529 | 0.735 | 0.7367 |
| 2 | local | 0.680 | 0.838 | 16.9 | 0.529 | 0.204 | -0.0003 |
| 3 | router | 0.749 | 0.746 | 24.0 | 0.751 | 0.521 | 0.4494 |
| 3 | random | 0.750 | 0.749 | 24.0 | 0.751 | 0.432 | 0.4233 |
| 3 | local | 0.864 | 0.931 | 24.0 | 0.751 | 0.092 | -0.0000 |
| 4 | router | 1.000 | 1.000 | 32.0 | 1.000 | 0.000 | 0.0002 |

### Feature-long-tail

| K | Method | Recall | Mass | Candidate KV | Ratio | L2 | CE delta |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | router | 0.328 | 0.378 | 9.5 | 0.298 | 1.198 | 2.0225 |
| 1 | random | 0.298 | 0.297 | 9.5 | 0.298 | 1.141 | 1.6608 |
| 1 | local | 0.433 | 0.735 | 9.5 | 0.298 | 0.423 | 0.0006 |
| 2 | router | 0.582 | 0.614 | 18.5 | 0.578 | 0.729 | 1.3530 |
| 2 | random | 0.580 | 0.577 | 18.5 | 0.578 | 0.743 | 1.1025 |
| 2 | local | 0.746 | 0.887 | 18.5 | 0.578 | 0.172 | 0.0000 |
| 3 | router | 0.804 | 0.751 | 25.3 | 0.790 | 0.555 | 1.2461 |
| 3 | random | 0.790 | 0.783 | 25.3 | 0.790 | 0.423 | 0.5739 |
| 3 | local | 0.913 | 0.961 | 25.3 | 0.790 | 0.062 | 0.0005 |
| 4 | router | 1.000 | 1.000 | 32.0 | 1.000 | 0.000 | 0.0006 |

## 5. Rank-K-Only

Uniform:

| Rank K | Recall | Mass | Candidate KV |
|---:|---:|---:|---:|
| 1 | 0.310 | 0.346 | 8.9 |
| 2 | 0.226 | 0.182 | 8.0 |
| 3 | 0.213 | 0.218 | 7.1 |
| 4 | 0.251 | 0.254 | 8.0 |

Longtail:

| Rank K | Recall | Mass | Candidate KV |
|---:|---:|---:|---:|
| 1 | 0.328 | 0.378 | 9.5 |
| 2 | 0.254 | 0.236 | 8.9 |
| 3 | 0.222 | 0.138 | 6.8 |
| 4 | 0.196 | 0.249 | 6.7 |

Rank-K-only 有弱排序信号，但不足以转化为高质量 sparse attention output。

## 6. Figures

Uniform:

![uniform topk](figures/uniform/r3_uniform_perfect_router_topk_recall_mass_l2_baselines.png)

![uniform rank](figures/uniform/r3_uniform_perfect_router_rank_k_only.png)

Longtail:

![longtail topk](figures/longtail/r3_longtail_perfect_router_topk_recall_mass_l2_baselines.png)

![longtail rank](figures/longtail/r3_longtail_perfect_router_rank_k_only.png)

## 7. Failure Analysis

直接失败点：

```text
feature-aligned bucket 与 dense attention high-mass KV 不充分对齐。
```

更具体地说：

- dense attention sparse，但 sparse mass 更偏 local；
- perfect feature bucket 比 random 只略强；
- same-count local 在 attention mass、output L2、CE delta 上显著更好；
- K=4 才恢复 full prefix，这不是有效 index。

因此 R3 说明：

```text
specialization 是必要候选，但不是充分条件。
```

## 8. Decision

如果组会时间有限，R3 可以用一页讲清楚：

```text
我们做了 perfect-router upper bound，排除了“只要 one-feature-one-expert 就能 retrieval”的解释。
```

后续应转向 block2 attention source 的变量诊断。

