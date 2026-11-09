# Experiment Parameters: E0-E2.2 Synthetic Data Understanding

## 1. Scope

This file records the implementation-level parameters for the E0-E2.2 stage
result. Read the surviving stage summaries for the result judgment.

Runnable scripts, generated data, checkpoints, outputs, and full figures live
outside `main`:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```

Mainline-safe summaries and report figures live under:

```text
main/experiments/E0_E3_synthetic_data_understanding/
```

## 2. Core Dataset

Final dataset used for E0/E1/E2.0/E2.1:

```text
config: configs/e1_all_trigram_v1000.json
data_dir: data_all_trigram_v1000/
regime: four_feature_all_trigram_v1000
seed: 20260513
vocab_size: 1000
corpus_length: 1000000
collision_policy: log
```

Feature construction:

| Feature | Context relation | Target count |
|---|---|---:|
| ABC | `[1,2] -> 22` | 10000 |
| DEF | `[3,4] -> 23` | 5000 |
| GHI | `[6,7] -> 20` | 500 |
| JKL | `[8,9] -> 21` | 100 |

Main control:

```text
random_only: iid tokens from the same vocabulary
shuffled_all_trigram_v1000: same unigram frequency as all-trigram data, token order shuffled
```

## 3. E0 Data Sanity

Purpose:

```text
Check whether planted sequential features are clean enough for model experiments.
```

Key audit metrics:

| Metric | Meaning |
|---|---|
| actual count | how many times the planted feature appears |
| background collision | accidental pattern occurrences from random fill |
| empirical target probability | empirical $P(C \mid A,B)$ for each feature |
| rank-frequency | whether planted features keep the intended long-tail order |

Expected artifacts:

```text
outputs/e0_all_trigram_v1000/data_audit.json
outputs/e0_all_trigram_v1000/feature_count_table.csv
outputs/e0_all_trigram_v1000/conditional_probability_table.csv
figures/e0_all_trigram_v1000/rank_frequency.png
```

## 4. E1 Dense Feature Readback

Model:

```text
architecture: 1-layer causal dense Transformer
seq_len: 32
d_model: 64
n_heads: 4
ffn_dim: 128
dropout: 0.0
vocab_size: 1000
```

Training:

```text
task: next-token prediction
batch_size: 128
optimizer: AdamW
lr: 0.0003
weight_decay: 0.01
grad_clip: 1.0
seed: 20260513
```

Main regimes:

| Regime | Role |
|---|---|
| `random_only` | random background baseline |
| `four_feature_all_trigram_v1000` | planted sequential feature condition |
| `shuffled_all_trigram_v1000` | unigram-frequency control |

Main diagnostics:

| Diagnostic | Meaning |
|---|---|
| feature readback probability | model probability of target token after feature prefix |
| logit margin | target logit minus strongest non-target logit |
| feature/background CE | whether feature prefix positions are easier than background |
| stepwise transition readback | whether model learns intermediate transitions, not only final target |
| raw weight spectrum | unnormalized singular-value distribution of dense/FFN weights |
| top-k singular energy | concentration of parameter spectrum |
| SVD alignment heatmap | relation between feature representations and top singular directions |

Main artifacts:

```text
outputs/e1_augmented_all_trigram_v1000/
figures/e1_augmented_all_trigram_v1000/
```

Report figures promoted to mainline:

```text
stages/E1_dense_feature_readback/figures/
hypotheses/archive/E0_E2_2_synthetic_feature_specialization_0515/figures/
```

## 5. E2.0 MoE Feature Separation

Config:

```text
configs/e2_moe_feature_separation_all_trigram_v1000.json
```

Model:

```text
architecture: 1-layer causal Transformer with top-1 MoE FFN
seq_len: 32
d_model: 64
n_heads: 4
num_experts: 4
expert ffn_dim: 128
dropout: 0.0
router: linear top-1 router over current hidden state
```

Training:

```text
task: next-token prediction
steps: 10000
batch_size: 128
lr: 0.0006
weight_decay: 0.01
grad_clip: 1.0
log_every: 250
seeds: [20260513, 20260514, 20260515, 20260516, 20260517]
```

Variants:

| Variant | Meaning |
|---|---|
| `moe_top1_no_lb` | top-1 routing without load-balance loss |
| `moe_top1_lb` | top-1 routing with load-balance loss, `lb_coef=0.01` |
| shuffled versions | same MoE training on shuffled unigram control |

Main diagnostics:

| Diagnostic | Meaning |
|---|---|
| $P(expert \mid feature)$ | whether a feature prefers specific experts |
| expert purity | feature composition inside each expert |
| NMI / ARI | agreement between feature identity and expert choice |
| feature readback | whether MoE still predicts the target token |
| expert load | global expert usage |
| dominant expert ablation | causal effect of removing selected expert output |
| force routing | whether the router-selected expert is also the best forced expert |
| expert FFN spectrum/alignment | parameter-space diagnostic inside experts |

Main artifacts:

```text
outputs/e2_moe_feature_separation/
figures/e2_moe_feature_separation/
```

## 6. E2.1 Router Input Geometry

Input:

```text
trained checkpoints from E2.0
dataset: four_feature_all_trigram_v1000
position: prefix-end token, e.g. B in [A,B] -> C
```

Purpose:

```text
Decide whether imperfect specialization comes from representation collapse,
router boundary choice, or expert capacity sharing.
```

Diagnostics:

| Diagnostic | Meaning |
|---|---|
| embedding cosine | whether prefix-end tokens are initially separable |
| router input centroid cosine | similarity between feature hidden centroids |
| Fisher ratio | between-feature distance relative to within-feature variance |
| PCA projection | visual check of feature/router grouping |
| router boundary alignment | cosine between feature-difference directions and router boundary directions |
| router margin / entropy | confidence of expert choice |
| hidden-vs-routing similarity | whether similar hidden states receive similar routing |
| force-routing competence | whether dominant expert is actually better for the feature |

Main artifacts:

```text
outputs/e2_1_router_input_geometry/
figures/e2_1_router_input_geometry/
```

## 7. E2.2 Specialization Pressure

Purpose:

```text
Test whether more specialization pressure naturally produces cleaner
feature-aligned expert partition without changing the router objective.
```

Conditions:

| Condition | Feature count | expert ffn_dim | Seeds | Config |
|---|---:|---:|---|---|
| baseline | 4 | 128 | 5 | `e2_moe_feature_separation_all_trigram_v1000.json` |
| bottleneck | 4 | 16 | 3 | `e2_2_capacity_bottleneck_four_feature.json` |
| pressure | 16 | 16 | 3 | `e2_2_sixteen_feature_pressure.json` |

16-feature data:

```text
config: configs/e2_2_specialization_pressure_data.json
vocab_size: 1000
corpus_length: 1000000
feature counts: 10000, 8000, 6000, 5000, ..., 200
```

Main diagnostics:

| Diagnostic | Meaning |
|---|---|
| NMI / ARI | whether routing becomes more feature-aligned |
| readback probability | whether model still learns features |
| dominant fraction | how concentrated each feature is in one expert |
| routing entropy | spread of routing over experts |
| load imbalance | global expert collapse or balance |
| ablation drop | whether selected expert is causally important |

Main artifacts:

```text
outputs/e2_2_capacity_bottleneck_four_feature/
outputs/e2_2_sixteen_feature_pressure/
outputs/e2_2_specialization_pressure/
figures/e2_2_specialization_pressure/
```

## 8. Main Result Files

Stage summaries:

```text
stages/E0_data_sanity/summary.md
stages/E1_dense_feature_readback/summary.md
stages/E2_moe_feature_separation/versions/E2_0_moe_feature_separation/summary.md
stages/E2_moe_feature_separation/versions/E2_1_router_input_geometry/summary.md
stages/E2_moe_feature_separation/versions/E2_2_specialization_pressure/summary.md
```

## 9. Claim Boundary

These parameters support a controlled toy-setting claim:

```text
Synthetic all-trigram features can be audited, learned by dense Transformer,
and can induce measurable MoE feature-expert alignment; however, separable
feature representations do not naturally imply clean one-feature-one-expert
specialization under this setup.
```

They do not support claims about real LLM semantic experts, indexed-KV speedup,
or general MoE specialization behavior.
