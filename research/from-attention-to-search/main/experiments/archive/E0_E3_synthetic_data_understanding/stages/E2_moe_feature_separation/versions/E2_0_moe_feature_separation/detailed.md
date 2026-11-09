# Detailed Result: E2 MoE Feature Separation

## Run

Workspace:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
```

Output:

```text
active/synthetic_data_understanding/outputs/e2_augmented_all_trigram_v1000/
active/synthetic_data_understanding/figures/e2_augmented_all_trigram_v1000/
```

Model:

```text
token embedding
-> positional embedding
-> 1-layer causal self-attention
-> 4-expert top-1 MoE FFN
-> LM head
```

Training:

```text
task = next-token prediction
seq_len = 32
batch_size = 128
d_model = 64
n_heads = 4
ffn_dim = 128
steps = 10000
lr = 0.0006
seeds = 20260513,20260514,20260515,20260516,20260517
```

Runs:

```text
moe_top1_no_lb
moe_top1_lb
shuffled_moe_top1_no_lb
shuffled_moe_top1_lb
```

`shuffled_*` 保留 all-trigram corpus 的 token frequency，但打乱 token order，用来检查 MoE 是否只利用 unigram frequency。

## Commands

```bash
python active/synthetic_data_understanding/scripts/train_moe_feature_separation.py \
  --run-config active/synthetic_data_understanding/configs/e2_moe_feature_separation_all_trigram_v1000.json \
  --out-dir active/synthetic_data_understanding/outputs/e2_augmented_all_trigram_v1000

python active/synthetic_data_understanding/scripts/train_moe_feature_separation.py \
  --run-config active/synthetic_data_understanding/configs/e2_moe_feature_separation_all_trigram_v1000.json \
  --out-dir active/synthetic_data_understanding/outputs/e2_augmented_all_trigram_v1000 \
  --shuffle-token-order \
  --variant-prefix shuffled_

python active/synthetic_data_understanding/scripts/plot_moe_feature_separation.py \
  --out-dir active/synthetic_data_understanding/outputs/e2_augmented_all_trigram_v1000 \
  --fig-dir active/synthetic_data_understanding/figures/e2_augmented_all_trigram_v1000
```

## Output Tables

```text
routing_matrix_p_expert_given_feature.csv
expert_purity_p_feature_given_expert.csv
feature_readback_table.csv
expert_load_table.csv
ablation_delta_table.csv
alignment_summary_table.csv
context_loss_table.csv
transition_readback_table.csv
expert_weight_svd_summary.csv
expert_weight_singular_values.csv
expert_svd_alignment_table.csv
force_routing_table.csv
force_routing_summary.csv
force_routing_stability.csv
seed_stability_table.csv
```

## Training Summary

| Regime | Final CE mean | Final CE range | LB proxy mean |
|---|---:|---:|---:|
| no-LB all-trigram | 6.624 | 6.589-6.649 | 1.126 |
| LB all-trigram | 6.625 | 6.589-6.653 | 1.000 |
| no-LB shuffled | 6.796 | 6.773-6.805 | 1.068 |
| LB shuffled | 6.798 | 6.775-6.808 | 1.000 |

Reading:

- all-trigram learns more than shuffled control;
- shuffled still beats $\log(1000)$ slightly because unigram frequency is preserved;
- LB balances load without materially changing CE.

## Feature Readback

| Feature | no-LB | LB | shuffled no-LB | shuffled LB |
|---|---:|---:|---:|---:|
| ABC | 0.999 | 0.998 | 0.010 | 0.011 |
| DEF | 0.998 | 0.997 | 0.005 | 0.005 |
| GHI | 0.975 | 0.967 | 0.001 | 0.001 |
| JKL | 0.679 | 0.829 | 0.001 | 0.001 |

Reading:

- all-trigram MoE reads back all four features;
- shuffled control fails on all four features;
- low-frequency `JKL` remains the hardest feature, but LB improves it in this run.

## Context Loss

| Group | no-LB CE | LB CE | shuffled no-LB CE | shuffled LB CE |
|---|---:|---:|---:|---:|
| ABC prefix | 0.001 | 0.001 | 4.555 | 4.569 |
| DEF prefix | 0.003 | 0.003 | 5.270 | 5.354 |
| GHI prefix | 0.021 | 0.021 | n/a | n/a |
| JKL prefix | 0.229 | 0.186 | n/a | n/a |
| background | 6.748 | 6.749 | 6.801 | 6.803 |

Reading:

- all-trigram feature prefixes are much easier than background;
- shuffled GHI/JKL exact prefixes have no usable accidental count, so they are marked `n/a`;
- shuffled ABC/DEF prefix losses remain far above all-trigram.

## Stepwise Transition Readback

| Transition | no-LB model | LB model | shuffled no-LB | shuffled LB |
|---|---:|---:|---:|---:|
| `1 -> 2` | 0.915 | 0.914 | 0.012 | 0.012 |
| `1 2 -> 22` | 0.999 | 0.998 | 0.010 | 0.011 |
| `8 -> 9` | 0.089 | 0.080 | 0.001 | 0.001 |
| `8 9 -> 21` | 0.679 | 0.829 | 0.001 | 0.001 |

Reading:

- all-trigram MoE learns both first-step and two-token prefix transitions;
- shuffled control removes the transition structure.

## Routing Alignment

| Variant | NMI mean | NMI range | ARI mean | ARI range |
|---|---:|---:|---:|---:|
| no-LB | 0.816 | 0.722-0.872 | 0.838 | 0.741-0.904 |
| LB | 0.823 | 0.741-0.894 | 0.841 | 0.715-0.922 |

Random routing baseline:

```text
random_nmi ~= 0.0004
random_ari ~= 0.0000
```

Reading:

- feature identity is strongly reflected in routing;
- LB does not erase this alignment;
- shuffled routing NMI is not used as a main metric because accidental feature positions are sparse and unstable.

## Expert Load

| Variant | E0 | E1 | E2 | E3 |
|---|---:|---:|---:|---:|
| no-LB | 0.200 | 0.260 | 0.307 | 0.233 |
| LB | 0.255 | 0.248 | 0.249 | 0.248 |
| shuffled no-LB | 0.250 | 0.268 | 0.226 | 0.257 |
| shuffled LB | 0.248 | 0.251 | 0.253 | 0.248 |

Reading:

- LB produces near-uniform load;
- no-LB does not collapse to a single expert;
- load balance alone does not explain feature readback.

## Dominant Expert Ablation

| Feature | no-LB drop | LB drop | shuffled no-LB drop | shuffled LB drop |
|---|---:|---:|---:|---:|
| ABC | 0.501 | 0.646 | 0.003 | 0.003 |
| DEF | 0.727 | 0.440 | 0.001 | 0.001 |
| GHI | 0.377 | 0.302 | 0.000 | 0.000 |
| JKL | 0.407 | 0.527 | 0.000 | 0.000 |

Reading:

- all-trigram dominant expert ablation damages feature readback;
- shuffled ablation has no meaningful effect because there is no learned feature readback to damage.

## Expert Spectrum

| Variant | Matrix | Top-10 energy | Stable rank |
|---|---|---:|---:|
| no-LB | `fc1` | 0.409 | 12.450 |
| LB | `fc1` | 0.401 | 12.917 |
| shuffled no-LB | `fc1` | 0.370 | 18.210 |
| shuffled LB | `fc1` | 0.368 | 18.330 |
| no-LB | `fc2` | 0.492 | 7.565 |
| LB | `fc2` | 0.489 | 7.561 |
| shuffled no-LB | `fc2` | 0.478 | 6.573 |
| shuffled LB | `fc2` | 0.474 | 6.822 |

Reading:

- the cleanest structural change is in expert `fc1`;
- all-trigram produces more concentrated input projection than shuffled control;
- spectrum is diagnostic, not a causal mechanism proof.

## SVD Alignment

Mean best absolute cosine between feature representation and expert `fc1` singular directions:

| Feature | no-LB | LB | shuffled no-LB | shuffled LB |
|---|---:|---:|---:|---:|
| ABC | 0.400 | 0.342 | 0.284 | 0.300 |
| DEF | 0.353 | 0.399 | 0.284 | 0.250 |
| GHI | 0.308 | 0.343 | n/a | n/a |
| JKL | 0.300 | 0.287 | n/a | n/a |

Reading:

- feature representations have nontrivial alignment with expert singular directions;
- the alignment is not enough to identify causal directions;
- E2.1 should directly ablate candidate singular directions.

## Force-Routing Diagnostic

Question:

```text
If the B-position hidden state for feature [A,B]->C is forced through every expert,
is the router-selected dominant expert also the expert that gives the highest P(C)?
```

Mean forced-routing summary:

| Feature | Variant | Dominant P | Best P | Other mean P | Dominant-is-best | Dominant advantage |
|---|---|---:|---:|---:|---:|---:|
| ABC | no-LB | 0.999 | 0.999 | 0.729 | 0.80 | 0.269 |
| DEF | no-LB | 0.998 | 0.998 | 0.770 | 1.00 | 0.228 |
| GHI | no-LB | 0.975 | 0.975 | 0.689 | 1.00 | 0.286 |
| JKL | no-LB | 0.679 | 0.851 | 0.428 | 0.40 | 0.251 |
| ABC | LB | 0.998 | 0.999 | 0.881 | 0.80 | 0.117 |
| DEF | LB | 0.997 | 0.998 | 0.870 | 0.40 | 0.127 |
| GHI | LB | 0.967 | 0.970 | 0.749 | 0.60 | 0.218 |
| JKL | LB | 0.829 | 0.830 | 0.354 | 0.80 | 0.475 |

Shuffled control:

| Feature | shuffled no-LB dominant P | shuffled LB dominant P | Shuffled dominant advantage |
|---|---:|---:|---:|
| ABC | 0.010 | 0.011 | approximately 0 |
| DEF | 0.005 | 0.005 | approximately 0 |
| GHI | 0.001 | 0.001 | approximately 0 |
| JKL | 0.001 | 0.001 | approximately 0 |

Reading:

- all-trigram dominant expert usually has higher direct forced probability than other experts;
- no-LB `DEF/GHI` are strongest: dominant expert is best in all seeds;
- LB keeps positive dominant advantage but weakens strict best-expert matching for `DEF/GHI`;
- no-LB `JKL` shows low-frequency instability: dominant expert helps, but another expert is often better under forced routing;
- shuffled control has no meaningful forced expert advantage.

## Figures

![E2 loss](figures/moe_ntp_loss_comparison.png)

![E2 routing matrix](figures/routing_matrix_heatmap_no_lb_vs_lb.png)

![E2 feature readback](figures/feature_readback_no_lb_vs_lb.png)

![E2 context loss](figures/context_loss_feature_vs_background.png)

![E2 transition readback](figures/stepwise_transition_readback.png)

![E2 dominant expert ablation](figures/ablation_delta_by_feature.png)

![E2 expert load](figures/expert_load_no_lb_vs_lb.png)

![E2 expert SVD top10 energy](figures/expert_ffn_svd_top10_energy.png)

![E2 expert SVD alignment](figures/expert_svd_alignment_fc1_right.png)

![E2 force routing probability](figures/force_routing_probability_by_expert.png)

![E2 dominant vs best forced expert](figures/dominant_vs_best_forced_expert.png)

![E2 dominant advantage](figures/dominant_advantage_by_feature.png)

## Failure Mode Check

- Expert collapse: not observed.
- LB erases feature alignment: not observed.
- Token-frequency-only explanation: weakened by shuffled control.
- Spectrum-only explanation: insufficient; needs E2.1 causal direction test.
- Router-only explanation: weakened by force-routing, because dominant experts usually have direct predictive advantage.
- Strong one-feature-one-expert claim: weakened by forced-routing mismatch in LB `DEF/GHI` and no-LB `JKL`.
- Real-language transfer: still untested.
