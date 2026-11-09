# Execution Plan: E2 MoE Feature Separation

## 1. Run Goal

Train a 4-expert top-1 MoE on the validated all-trigram corpus and measure whether routing aligns with feature identity.

The main comparison is:

```text
moe_top1_no_lb vs moe_top1_lb
```

The augmented control is:

```text
all-trigram sequence vs shuffled unigram sequence
```

The main claim target is feature-expert alignment, not frequency specialization.

## 2. Data Construction

Use the E0/E1 validated corpus:

```text
config: active/synthetic_data_understanding/configs/e1_all_trigram_v1000.json
data_dir: active/synthetic_data_understanding/data_all_trigram_v1000/
regime: four_feature_all_trigram_v1000
```

Features:

| Feature | Pattern | Target count |
|---|---|---:|
| ABC | `[1,2] -> 22` | 10000 |
| DEF | `[3,4] -> 23` | 5000 |
| GHI | `[6,7] -> 20` | 500 |
| JKL | `[8,9] -> 21` | 100 |

Evaluation position:

- for pattern `[A,B,C]`, evaluate router at token `B`;
- this is the position whose hidden state predicts next token `C`;
- background positions are sampled from non-feature-prefix positions.

## 3. Model / Training / Evaluation Setup

Model:

```text
token embedding
-> positional embedding
-> 1-layer causal self-attention
-> MoE FFN
-> LM head
```

MoE:

- `num_experts=4`;
- `top_k=1`;
- expert MLP: `Linear(d_model, ffn_dim) -> GELU -> Linear(ffn_dim, d_model)`;
- variants:
  - `moe_top1_no_lb`, `lb_coef=0.0`;
  - `moe_top1_lb`, `lb_coef=0.01`.

Training defaults:

```text
steps = 10000
batch_size = 128
seq_len = 32
d_model = 64
n_heads = 4
ffn_dim = 128
lr = 0.0006
weight_decay = 0.01
grad_clip = 1.0
seeds = 20260513,20260514,20260515,20260516,20260517
```

## 4. Configs And Commands

Config:

```text
active/synthetic_data_understanding/configs/e2_moe_feature_separation_all_trigram_v1000.json
```

Full run:

```bash
python active/synthetic_data_understanding/scripts/train_moe_feature_separation.py \
  --run-config active/synthetic_data_understanding/configs/e2_moe_feature_separation_all_trigram_v1000.json

python active/synthetic_data_understanding/scripts/plot_moe_feature_separation.py \
  --out-dir active/synthetic_data_understanding/outputs/e2_moe_feature_separation \
  --fig-dir active/synthetic_data_understanding/figures/e2_moe_feature_separation
```

Smoke test:

```bash
python active/synthetic_data_understanding/scripts/train_moe_feature_separation.py \
  --run-config active/synthetic_data_understanding/configs/e2_moe_feature_separation_all_trigram_v1000.json \
  --variants moe_top1_no_lb,moe_top1_lb \
  --seeds 20260513 \
  --steps 2 \
  --out-dir active/synthetic_data_understanding/outputs/e2_moe_feature_separation_smoke
```

Augmented full run:

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

## 5. Metrics And Artifacts

Tables:

```text
routing_matrix_p_expert_given_feature.csv
expert_purity_p_feature_given_expert.csv
feature_readback_table.csv
expert_load_table.csv
ablation_delta_table.csv
alignment_summary_table.csv
seed_stability_table.csv
context_loss_table.csv
transition_readback_table.csv
expert_weight_svd_summary.csv
expert_weight_singular_values.csv
expert_svd_alignment_table.csv
force_routing_table.csv
force_routing_summary.csv
force_routing_stability.csv
```

Figures:

```text
routing_matrix_heatmap_no_lb_vs_lb.png
feature_readback_no_lb_vs_lb.png
expert_load_no_lb_vs_lb.png
ablation_delta_by_feature.png
routing_entropy_vs_frequency.png
moe_ntp_loss_comparison.png
context_loss_feature_vs_background.png
stepwise_transition_readback.png
expert_ffn_svd_top10_energy.png
expert_svd_alignment_fc1_right.png
force_routing_probability_by_expert.png
dominant_vs_best_forced_expert.png
dominant_advantage_by_feature.png
```

Raw checkpoints stay ignored:

```text
active/synthetic_data_understanding/outputs/e2_moe_feature_separation/*/*.pt
```

Report-ready figures should be copied into:

```text
main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_0_moe_feature_separation/figures/
```

After the real run, write:

```text
main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_0_moe_feature_separation/summary.md
main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_0_moe_feature_separation/detailed.md
```

## 6. Pass / Fail Criteria

Strong support:

- MoE readback is close to E1 dense readback;
- $P(\text{expert}\mid\text{feature})$ is clearly non-uniform;
- NMI is above random routing baseline;
- dominant expert ablation lowers corresponding feature target probability;
- dominant expert is stable across most seeds.

Weak support:

- readback succeeds, but feature-expert alignment is mixed;
- no-LB has alignment but LB weakens it;
- high-frequency features route more stably than low-frequency features.

No support:

- MoE learns NTP but routing is near random with respect to feature identity;
- routing mainly follows global load balance or token identity;
- dominant expert ablation does not affect corresponding feature readback.
- shuffled unigram control reads back the same feature transitions, which would mean the setup has not separated sequential relation from token frequency.

## 7. Failure Modes To Check

- expert collapse: one expert receives almost all tokens;
- LB over-regularization: load is balanced but feature purity disappears;
- readback failure: MoE fails to reproduce E1 feature probabilities;
- seed instability: dominant expert assignment changes randomly across seeds;
- token identity leakage: routing follows current token ID rather than feature relation.
- shuffled control: loss improves but feature readback and dominant-expert ablation should disappear.
- spectrum overinterpretation: expert SVD changes are diagnostic only unless followed by direction-level causal ablation.
- force-routing: dominant router expert should have higher forced target probability than non-dominant experts if it is intrinsically better for that feature.

## 8. Result Location

Ignored working outputs:

```text
active/synthetic_data_understanding/outputs/e2_moe_feature_separation/
active/synthetic_data_understanding/figures/e2_moe_feature_separation/
active/synthetic_data_understanding/outputs/e2_augmented_all_trigram_v1000/
active/synthetic_data_understanding/figures/e2_augmented_all_trigram_v1000/
```

Mainline result closure:

```text
main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_0_moe_feature_separation/summary.md
main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_0_moe_feature_separation/detailed.md
```
