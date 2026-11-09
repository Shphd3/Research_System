# Result Summary: R3 Perfect Router Retrieval

### Purpose And Hypothesis

R3 测试一个 upper-bound 问题：

```text
当 router 被 RouterFeatureCE 强制到 one-feature-one-expert，
feature-aligned bucket 是否足以作为 block2 KV retrieval index？
```

如果成功，说明 R1/R2 失败主要来自 natural router 没学到 clean partition。  
如果失败，说明即使 specialization 成立，feature label 也不是 block2 attention 的主要 index variable。

### Observation

执行完成：

- uniform feature distribution: 4 seeds；
- feature-long-tail distribution: 4 seeds；
- 每个数据集一个 4-GPU ACP job，每张 GPU 跑一个 seed；
- 两个 job 均成功，checkpoint、retrieval CSV 和 figures 已生成。

训练前提成立：

| Dataset | NMI | ARI | fixed-label routing | router acc | feature readback acc |
|---|---:|---:|---:|---:|---:|
| uniform | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| longtail | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

Dense attention 仍然 sparse：

| Dataset | Top16 mass | Mass90 support | Effective support |
|---|---:|---:|---:|
| uniform | 0.934 | 12.58 | 9.12 |
| longtail | 0.953 | 10.33 | 7.47 |

但 retrieval 没有得到有效提升。Feature queries 上 K=1：

| Dataset | Router recall | Random recall | Local recall | Router mass | Local mass | Router L2 | Local L2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| uniform | 0.310 | 0.279 | 0.404 | 0.346 | 0.681 | 1.101 | 0.420 |
| longtail | 0.328 | 0.298 | 0.433 | 0.378 | 0.735 | 1.198 | 0.423 |

K=4 sanity 通过：router/random/local/oracle 都等于 full prefix，recall=1.0、mass=1.0、L2=0。

### Interpretation

R3 给出负向结论：

```text
即使 router specialization 完美成立，feature bucket 也不是当前 E-series all-trigram block2 attention 的高效 KV index。
```

Router top-K 只略高于 random same-count，显著弱于 local same-count；并且 output relative L2 与 CE_delta 都明显差于 local/oracle。这说明 block2 attention 的主要 high-mass KV 更像由位置/局部性或其他 hidden/value 相似性决定，而不是由 feature label 决定。

### Limitation

这个结论只覆盖：

- E-series all-trigram synthetic；
- `seq_len=32`；
- 4 feature / 4 bucket perfect-router upper bound；
- 当前 block2 attention analysis。

不能推出真实语言模型中 feature bucket 一定无用，也不能推出所有 router index 都失败。

### Key Figures

Uniform:

![uniform key figure](figures/uniform/r3_uniform_perfect_router_topk_recall_mass_l2_baselines.png)

Longtail:

![longtail key figure](figures/longtail/r3_longtail_perfect_router_topk_recall_mass_l2_baselines.png)

Rank-only:

![uniform rank only](figures/uniform/r3_uniform_perfect_router_rank_k_only.png)

![longtail rank only](figures/longtail/r3_longtail_perfect_router_rank_k_only.png)

### Claim Update

Result:

```text
perfect feature specialization 成立，但 feature bucket retrieval 仍不优于 local，并只略高于 random。
```

Interpretation:

```text
R1/R2 的 failure 不只是 natural router 没 specialize；
更关键的是 feature label 本身不是当前 block2 attention 的足够好 index variable。
```

Claim:

```text
在当前 synthetic all-trigram setup 中，feature-aligned router bucket 不能作为高效 KV retrieval index。
```

### Decision

组会可以讲，但应作为“负向澄清实验”而不是正结果。它的重要性在于切断一个解释分支：

```text
不是只要做到 one-feature-one-expert，attention search 就自然成立。
```

下一步应转向诊断 block2 attention 真正依赖的 index variable：locality、token identity、hidden similarity、value/output similarity，或 attention head-specific pattern。

