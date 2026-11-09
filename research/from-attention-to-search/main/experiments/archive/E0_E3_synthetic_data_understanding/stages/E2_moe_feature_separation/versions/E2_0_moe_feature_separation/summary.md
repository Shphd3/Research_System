# Result Summary: E2 MoE Feature Separation

## Purpose And Hypothesis

E2 的目的，是在 E1 已经确认 dense Transformer 学到的是 sequential context relation、而不是单纯 token frequency 之后，判断 MoE 是否会在同一 NTP 任务中形成 feature-level expert preference。

主假设 H2：

```text
在 controlled all-trigram sequence 中，MoE 会通过 next-token loss 学到 feature-expert alignment；
如果这种 alignment 反映真实 feature 使用，那么 dominant expert ablation 应该损伤对应 feature readback（给定A B 预测 C）。
```

本轮完善版加入了 E1 同款诊断：shuffled unigram control、feature/background CE、逐步 transition readback、expert FFN spectrum、feature representation 与 expert singular directions 的 alignment。

## Observation

本轮完整运行 20 个模型：

```text
dataset = four_feature_all_trigram_v1000
controls = all-trigram, shuffled unigram
variants = no-LB, LB
seeds = 20260513-20260517
steps = 10000 per run
```

Loss：

| Regime | Final CE mean |
|---|---:|
| no-LB all-trigram | 6.624 |
| LB all-trigram | 6.625 |
| no-LB shuffled | 6.796 |
| LB shuffled | 6.798 |

Feature readback：

| Feature | no-LB | LB | shuffled no-LB | shuffled LB |
|---|---:|---:|---:|---:|
| ABC | 0.999 | 0.998 | 0.010 | 0.011 |
| DEF | 0.998 | 0.997 | 0.005 | 0.005 |
| GHI | 0.975 | 0.967 | 0.001 | 0.001 |
| JKL | 0.679 | 0.829 | 0.001 | 0.001 |

All-trigram 的 routing alignment 明显高于 random routing：

| Variant | NMI mean | ARI mean | Random NMI | Random ARI |
|---|---:|---:|---:|---:|
| no-LB | 0.816 | 0.838 | 0.0004 | 0.0000 |
| LB | 0.823 | 0.841 | 0.0004 | 0.0000 |

Dominant expert ablation 会损伤 all-trigram feature readback：

| Feature | no-LB prob drop | LB prob drop |
|---|---:|---:|
| ABC | 0.501 | 0.646 |
| DEF | 0.727 | 0.440 |
| GHI | 0.377 | 0.302 |
| JKL | 0.407 | 0.527 |

Shuffled control 中 ablation drop 接近 0，说明没有形成可用的 feature path。

## Interpretation

E2 完善版支持 H2：在这个 controlled synthetic setting 中，MoE 不只是学会 NTP，而是形成了可测的 feature-expert alignment。

关键增强点是 shuffled control。Shuffled model 保留 unigram frequency，loss 也低于 $\log(1000)$，但 feature readback、transition readback、dominant expert ablation 都基本消失。因此 E2 的主要证据不是 token frequency，而是 all-trigram 顺序关系驱动的 expert preference。

LB 的作用比最初担心更温和：它把全局 expert load 拉近均匀，但没有消除 feature alignment。低频 feature 的 readback 和 expert identity 仍更不稳定，frequency 仍是二级解释。

Expert spectrum 也出现与 E1 一致的结构信号：all-trigram expert `fc1` top-10 energy 高于 shuffled control，stable rank 更低。这说明 MoE expert 的 input projection 在学到 context features 后更集中，但 singular-vector alignment 仍只能作为诊断，不能单独当作因果证明。

## Limitation

Shuffled control 中部分 feature prefix 在 corpus 中几乎不出现，因此 shuffled routing NMI/ARI 不作为主证据；主证据来自 readback、transition 和 ablation failure。

E2 仍然不能说明：

- 真实 LLM expert 也按语义 feature 分工；
- expert 编号跨 seed 固定；
- singular direction 本身就是 feature mechanism；
- MoE router 可以直接作为 KV retrieval index。

## Key Figures

![E2 loss](figures/moe_ntp_loss_comparison.png)

![E2 routing matrix](figures/routing_matrix_heatmap_no_lb_vs_lb.png)

![E2 feature readback](figures/feature_readback_no_lb_vs_lb.png)

![E2 context loss](figures/context_loss_feature_vs_background.png)

![E2 transition readback](figures/stepwise_transition_readback.png)

![E2 dominant expert ablation](figures/ablation_delta_by_feature.png)

![E2 expert load](figures/expert_load_no_lb_vs_lb.png)

![E2 expert SVD top10 energy](figures/expert_ffn_svd_top10_energy.png)

![E2 expert SVD alignment](figures/expert_svd_alignment_fc1_right.png)

## Claim Update

Supported:

- controlled all-trigram features can drive MoE feature-expert alignment;
- this alignment is stronger than random routing and survives LB;
- dominant expert ablation damages corresponding feature readback;
- shuffled unigram control fails, so the effect depends on sequential context relation;
- expert `fc1` spectrum becomes more concentrated under all-trigram training.

Still unclear:

- which expert singular directions are causally necessary;
- whether alignment is stable under more seeds, model sizes, top-2 routing, or noisier data;
- whether real-language repeated context features have comparable structure.

## What Cannot Be Claimed

不能声称真实 LLM expert 已经按语义分工，也不能声称 MoE router 已能作为 KV retrieval index。E2 只支持 controlled synthetic MoE specialization。

## Next Decision

下一步做 E2.1：对 trained MoE 做 expert-direction causal diagnostic，直接 ablate / project out candidate singular directions，判断哪些 expert spectral directions 对 feature readback 有因果作用。
