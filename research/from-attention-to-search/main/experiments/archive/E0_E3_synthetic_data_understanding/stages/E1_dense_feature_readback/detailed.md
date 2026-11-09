# Detailed Result: E1 Dense Feature Readback

## Run

Workspace:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
```

Model:

```text
token embedding
-> positional embedding
-> 1-layer causal self-attention
-> FFN
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
optimizer = AdamW
steps = 10000 per regime
```

Commands:

```bash
python active/synthetic_data_understanding/scripts/train_dense_feature_readback.py \
  --config active/synthetic_data_understanding/configs/e1_all_trigram_v1000.json \
  --data-dir active/synthetic_data_understanding/data_all_trigram_v1000 \
  --out-dir active/synthetic_data_understanding/outputs/e1_augmented_all_trigram_v1000 \
  --regime random_only \
  --steps 10000 \
  --batch-size 128 \
  --seq-len 32 \
  --d-model 64 \
  --n-heads 4 \
  --ffn-dim 128 \
  --lr 0.0006 \
  --log-every 250

python active/synthetic_data_understanding/scripts/train_dense_feature_readback.py \
  --config active/synthetic_data_understanding/configs/e1_all_trigram_v1000.json \
  --data-dir active/synthetic_data_understanding/data_all_trigram_v1000 \
  --out-dir active/synthetic_data_understanding/outputs/e1_augmented_all_trigram_v1000 \
  --regime four_feature_all_trigram_v1000 \
  --steps 10000 \
  --batch-size 128 \
  --seq-len 32 \
  --d-model 64 \
  --n-heads 4 \
  --ffn-dim 128 \
  --lr 0.0006 \
  --log-every 250

python active/synthetic_data_understanding/scripts/train_dense_feature_readback.py \
  --config active/synthetic_data_understanding/configs/e1_all_trigram_v1000.json \
  --data-dir active/synthetic_data_understanding/data_all_trigram_v1000 \
  --out-dir active/synthetic_data_understanding/outputs/e1_augmented_all_trigram_v1000 \
  --regime four_feature_all_trigram_v1000 \
  --output-regime shuffled_all_trigram_v1000 \
  --shuffle-token-order \
  --steps 10000 \
  --batch-size 128 \
  --seq-len 32 \
  --d-model 64 \
  --n-heads 4 \
  --ffn-dim 128 \
  --lr 0.0006 \
  --log-every 250
```

Plot command:

```bash
python active/synthetic_data_understanding/scripts/plot_dense_readback_figures.py \
  --out-dir active/synthetic_data_understanding/outputs/e1_augmented_all_trigram_v1000 \
  --fig-dir active/synthetic_data_understanding/figures/e1_augmented_all_trigram_v1000 \
  --regimes random_only four_feature_all_trigram_v1000 shuffled_all_trigram_v1000 \
  --actual-spectrum \
  --vocab-size 1000
```

## Output Tables

Ignored output directory:

```text
active/synthetic_data_understanding/outputs/e1_augmented_all_trigram_v1000/
```

Important tables per regime:

```text
*_feature_probability_table.csv
*_transition_readback_table.csv
*_context_loss_table.csv
*_weight_svd_summary.csv
*_weight_singular_values.csv
*_svd_alignment_table.csv
*_top_singular_direction_probe.csv
*_representation_spectrum.csv
*_centroid_cosine.csv
*_centroid_pca_projection.csv
*_train_metrics.jsonl
*_dense_transformer.pt
```

## Loss

| Regime | Final loss | Last-10 mean |
|---|---:|---:|
| random-only | 6.865 | 6.868 |
| all-trigram features | 6.647 | 6.622 |
| shuffled control | 6.811 | 6.810 |

Reading:

- all-trigram learns more than random-only;
- shuffled control is below random-only because unigram statistics are preserved;
- shuffled control remains far worse than all-trigram because sequential relations are destroyed.

## Feature Readback

| Feature | Empirical prob | All-trigram model prob | Shuffled model prob | All-trigram margin | Shuffled margin |
|---|---:|---:|---:|---:|---:|
| ABC | 1.000 | 0.999 | 0.010 | 11.307 | -0.119 |
| DEF | 1.000 | 0.997 | 0.005 | 10.500 | -0.809 |
| GHI | 1.000 | 0.961 | 0.001 | 7.090 | -2.624 |
| JKL | 0.971 | 0.710 | 0.001 | 4.476 | -2.557 |

Reading:

- all-trigram feature readback is strong for all four features;
- shuffled control removes the feature relation even though unigram frequency remains.

## Stepwise Transition Readback

| Transition | Empirical prob | Model prob |
|---|---:|---:|
| `ABC: 1 -> 2` | 0.915 | 0.918 |
| `ABC: 1 2 -> 22` | 1.000 | 0.999 |
| `JKL: 8 -> 9` | 0.098 | 0.108 |
| `JKL: 8 9 -> 21` | 0.971 | 0.710 |

Reading:

- high-frequency feature has both first-step and second-step signal;
- low-frequency `JKL` has weak first-step signal but strong two-token prefix signal;
- this supports defining feature as context relation rather than single token.

## Context Loss

| Group | All-trigram CE | Shuffled CE |
|---|---:|---:|
| ABC prefix | 0.001 | 6.914 |
| DEF prefix | 0.002 | 6.890 |
| GHI prefix | 0.020 | 6.942 |
| JKL prefix | 0.696 | 6.916 |
| background | 6.723 | 6.812 |

Reading:

- feature-prefix contexts are easy under all-trigram;
- background remains high entropy;
- shuffled control turns feature-prefix contexts back into background-like contexts.

## SVD Summary

| Regime | Matrix | Top-1 energy | Top-10 energy | Stable rank |
|---|---|---:|---:|---:|
| random-only | `ff1` | 0.045 | 0.359 | 22.474 |
| all-trigram | `ff1` | 0.086 | 0.410 | 11.701 |
| shuffled | `ff1` | 0.044 | 0.354 | 22.562 |
| random-only | `ff2` | 0.121 | 0.447 | 8.285 |
| all-trigram | `ff2` | 0.121 | 0.471 | 8.296 |
| shuffled | `ff2` | 0.133 | 0.456 | 7.519 |

Reading:

- the strongest structural change appears in `ff1`, the FFN input projection;
- all-trigram has higher `ff1` top-10 energy and lower stable rank than random/shuffle;
- raw spectrum alone still does not identify which direction is the feature mechanism.

## SVD Alignment

Best absolute cosine with `ff1` right singular vectors:

| Regime | Group | Best singular vector | Singular value | Abs cosine |
|---|---|---:|---:|---:|
| all-trigram | ABC | 6 | 2.108 | 0.273 |
| all-trigram | DEF | 15 | 1.772 | 0.327 |
| all-trigram | GHI | 8 | 1.952 | 0.317 |
| all-trigram | JKL | 11 | 1.867 | 0.231 |
| all-trigram | background | 1 | 3.354 | 0.434 |

Reading:

- feature representations align with high but not necessarily top singular directions;
- background aligns strongly with the top singular direction;
- this matches the warning from `abc_motif_study`: top singular vector may represent broad/global structure, not the task feature.

## Top Singular Direction Probe

Cosine with `ff1` top singular vector:

| Regime | Probe | Cosine | Abs cosine |
|---|---|---:|---:|
| all-trigram | all token embedding mean | -0.268 | 0.268 |
| all-trigram | non-feature token embedding mean | -0.312 | 0.312 |
| all-trigram | feature token embedding mean | 0.524 | 0.524 |
| shuffled | all token embedding mean | -0.033 | 0.033 |
| shuffled | non-feature token embedding mean | 0.010 | 0.010 |
| shuffled | feature token embedding mean | -0.479 | 0.479 |
| random-only | all token embedding mean | 0.161 | 0.161 |

Reading:

- feature-token frequency affects top singular direction;
- but because shuffled also has feature-token alignment without feature readback, this is not enough to claim feature mechanism;
- sequence-specific readback requires the context relation.

## Figures

![E1 loss comparison](figures/e1_dense_ntp_loss_comparison.png)

![E1 context loss](figures/e1_context_loss_feature_vs_background.png)

![E1 transition readback](figures/e1_stepwise_transition_readback.png)

![E1 dense weight spectrum](figures/e1_dense_weight_spectrum_actual_ylog_comparison.png)

![E1 FFN weight spectrum](figures/e1_ffn_weight_spectrum_actual_ylog_comparison.png)

![E1 FFN top10 energy](figures/e1_ffn_svd_top10_energy.png)

![E1 SVD alignment](figures/e1_ffn_svd_alignment_fc1_right.png)

## What To Inspect Next

- singular-direction causal ablation;
- seed stability of feature-aligned singular directions;
- contrastive directions such as feature prefix minus shuffled/background prefix;
- dense-vs-MoE comparison of feature direction alignment.
