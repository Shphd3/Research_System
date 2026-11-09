# Result Summary: E1 Dense Feature Readback

## Purpose And Hypothesis

E1 的目的，是在 E0 已确认 synthetic corpus 足够干净之后，判断 dense toy Transformer 是否能通过 NTP 学到这些上下文 feature，并检查这种学习是否能在 FFN 谱空间中留下可诊断结构。

主假设 H1：

```text
clean sequential feature 可以被 dense Transformer 读回；
如果模型学到的是顺序关系，而不只是 token marginal frequency，
那么 shuffle unigram control 应该不能读回 feature。
```

本轮补强了 `abc_motif_study` 中更细的 dense diagnostic：feature/background loss、逐步 transition、fc1/fc2 SVD、stable rank、top-k energy、singular-vector alignment、top singular direction probe。

## Observation

本轮重新运行 E1，比较三组：

```text
random_only
four_feature_all_trigram_v1000
shuffled_all_trigram_v1000
```

`shuffled_all_trigram_v1000` 保留 all-trigram corpus 的 unigram frequency，但打乱 token order，用来区分 sequential relation 和 token marginal frequency。

Loss：

| Regime | Final loss | Last-10 mean |
|---|---:|---:|
| random-only | 6.865 | 6.868 |
| all-trigram features | 6.647 | 6.622 |
| shuffled control | 6.811 | 6.810 |

Feature readback：

| Feature | All-trigram prob | Shuffled prob | All-trigram margin | Shuffled margin |
|---|---:|---:|---:|---:|
| ABC | 0.999 | 0.010 | 11.307 | -0.119 |
| DEF | 0.997 | 0.005 | 10.500 | -0.809 |
| GHI | 0.961 | 0.001 | 7.090 | -2.624 |
| JKL | 0.710 | 0.001 | 4.476 | -2.557 |

Context CE：

| Group | All-trigram CE | Shuffled CE |
|---|---:|---:|
| ABC prefix | 0.001 | 6.914 |
| DEF prefix | 0.002 | 6.890 |
| GHI prefix | 0.020 | 6.942 |
| JKL prefix | 0.696 | 6.916 |
| background | 6.723 | 6.812 |

逐步 transition 也显示顺序关系被学到：

| Transition | Empirical prob | Model prob |
|---|---:|---:|
| `ABC: 1 -> 2` | 0.915 | 0.918 |
| `ABC: 1 2 -> 22` | 1.000 | 0.999 |
| `JKL: 8 -> 9` | 0.098 | 0.108 |
| `JKL: 8 9 -> 21` | 0.971 | 0.710 |

Shuffle 后这些 transition 接近随机或消失。

## Interpretation

E1 现在更强地支持 H1：dense Transformer 学到的是 sequential context relation，而不是只利用 token unigram frequency。

证据是：shuffle control 保留 token 频率后，loss 仍略低于 random-only，但 feature readback 基本消失；这说明 unigram frequency 可以降低一部分 loss，但不能产生 `[A,B]->[C]` 读回。

谱空间方面，all-trigram 的 `ff1_weight` 比 random-only / shuffle 更集中：

| Regime | ff1 top-10 energy | ff1 stable rank |
|---|---:|---:|
| random-only | 0.359 | 22.474 |
| all-trigram | 0.410 | 11.701 |
| shuffled | 0.354 | 22.562 |

这说明 sequential feature training 会让 FFN input projection 出现更强各向异性。但 singular-vector alignment 需要谨慎解释：feature contexts 与若干 high singular directions 有对齐，但 background 与 top singular direction 的对齐也很强。因此不能把最大 singular vector 直接解释成 feature direction。

## Limitation

E1 仍然只证明 dense toy model 可以读回 controlled synthetic features，并显示 FFN 谱空间出现诊断性结构。

它不能证明：

- FFN 中已经形成唯一、干净、可命名的语义方向；
- 最大 singular direction 就是最重要 feature；
- MoE expert 一定会按同样方向分工；
- synthetic 结果能直接迁移到真实语言。

## Key Figures

![E1 loss comparison](figures/e1_dense_ntp_loss_comparison.png)

`e1_dense_ntp_loss_comparison.png` 支持 all-trigram、shuffle、random-only 的训练差异。

![E1 context loss](figures/e1_context_loss_feature_vs_background.png)

`e1_context_loss_feature_vs_background.png` 支持 feature-prefix CE 与 background CE 的分离。

![E1 transition readback](figures/e1_stepwise_transition_readback.png)

`e1_stepwise_transition_readback.png` 支持模型学到局部 transition，而不只是最终 `[A,B]->C`。

![E1 FFN spectrum](figures/e1_ffn_weight_spectrum_actual_ylog_comparison.png)

`e1_ffn_weight_spectrum_actual_ylog_comparison.png` 支持 all-trigram feature training 使 FFN spectrum 发生变化。

![E1 FFN top10 energy](figures/e1_ffn_svd_top10_energy.png)

`e1_ffn_svd_top10_energy.png` 支持 all-trigram 的 `ff1` energy concentration 高于 random/shuffle。

![E1 SVD alignment](figures/e1_ffn_svd_alignment_fc1_right.png)

`e1_ffn_svd_alignment_fc1_right.png` 支持 feature representation 与若干 FFN input singular directions 有对齐，但不是单一 top direction。

## Claim Update

Supported:

- clean all-trigram synthetic context relations 可以被 dense Transformer 读回；
- shuffle unigram control 不能读回 feature，因此模型学到的是顺序关系；
- feature-prefix CE 显著低于 background CE；
- all-trigram training 使 `ff1` spectrum 更集中，说明 FFN input geometry 出现结构变化。

Weakened:

- 仅凭 raw spectrum 判断 feature 机制是不够的；
- “最大 singular direction = feature direction”的说法不成立。

Still unclear:

- 哪些 singular directions 对 feature readback 有因果作用；
- feature direction 是否稳定跨 seed；
- dense feature directions 与 E2 MoE expert directions 是否一致。

## What Cannot Be Claimed

不能声称：

- FFN 已经形成完整语义机制；
- 谱方向 alignment 本身就是因果证明；
- dense toy result 可以直接解释真实 LLM；
- MoE expert 会自动继承 dense FFN 的谱方向。

## Next Decision

E1 现在可以作为 E2/E2.1 的 dense baseline。

下一步应做 E2.1：在 E2 MoE checkpoint 上复用本轮 E1 的谱方向方法，测 expert-level `fc1/fc2` SVD、feature representation alignment、dominant expert singular-direction ablation。
