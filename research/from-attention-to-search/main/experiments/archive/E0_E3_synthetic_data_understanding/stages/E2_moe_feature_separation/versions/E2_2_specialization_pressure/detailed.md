# Detailed Result: E2.2 Specialization Pressure Test

## Run

Workspace:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments
```

New conditions:

```text
bottleneck_ffn16_4feat: 4 features, ffn_dim=16, 3 seeds, 5000 steps
pressure_ffn16_16feat: 16 features, ffn_dim=16, 3 seeds, 5000 steps
```

Baseline:

```text
baseline_e2_ffn128_4feat: reused E2 completed run
```

## Commands

```bash
python active/synthetic_data_understanding/scripts/generate_synthetic_patterns.py \
  --config active/synthetic_data_understanding/configs/e2_2_specialization_pressure_data.json \
  --out-dir active/synthetic_data_understanding/data_e2_2_specialization_pressure

python active/synthetic_data_understanding/scripts/train_moe_feature_separation.py \
  --run-config active/synthetic_data_understanding/configs/e2_2_capacity_bottleneck_four_feature.json

python active/synthetic_data_understanding/scripts/train_moe_feature_separation.py \
  --run-config active/synthetic_data_understanding/configs/e2_2_sixteen_feature_pressure.json

python active/synthetic_data_understanding/scripts/plot_specialization_pressure.py \
  --baseline-dir active/synthetic_data_understanding/outputs/e2_augmented_all_trigram_v1000 \
  --bottleneck-dir active/synthetic_data_understanding/outputs/e2_2_capacity_bottleneck_four_feature \
  --pressure-dir active/synthetic_data_understanding/outputs/e2_2_sixteen_feature_pressure \
  --out-dir active/synthetic_data_understanding/outputs/e2_2_specialization_pressure \
  --fig-dir active/synthetic_data_understanding/figures/e2_2_specialization_pressure
```

## Output Tables

```text
specialization_pressure_summary.csv
specialization_pressure_feature_summary.csv
```

## Main Table

| Condition | Variant | CE | NMI | ARI | Readback | Ablation drop | Routing entropy | Dominant frac | Load imbalance |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | no-LB | 6.624 | 0.816 | 0.838 | 0.913 | 0.503 | 0.208 | 0.909 | 0.356 |
| baseline | LB | 6.625 | 0.823 | 0.841 | 0.948 | 0.479 | 0.126 | 0.935 | 0.015 |
| bottleneck | no-LB | 6.626 | 0.627 | 0.548 | 0.945 | 0.029 | 0.150 | 0.937 | 0.607 |
| bottleneck | LB | 6.625 | 0.644 | 0.591 | 0.917 | 0.003 | 0.204 | 0.922 | 0.014 |
| pressure | no-LB | 6.250 | 0.584 | 0.316 | 0.987 | 0.043 | 0.146 | 0.940 | 0.641 |
| pressure | LB | 6.250 | 0.534 | 0.241 | 0.986 | 0.065 | 0.114 | 0.953 | 0.027 |

## 16-Feature Pressure Notes

No-LB examples:

| Feature | Count | Readback | Dominant frac | Entropy | Ablation drop |
|---|---:|---:|---:|---:|---:|
| F01 | 10000 | 0.999 | 1.000 | 0.000 | 0.078 |
| F05 | 4000 | 0.997 | 0.980 | 0.074 | 0.319 |
| F12 | 800 | 0.992 | 0.827 | 0.410 | 0.027 |
| F16 | 200 | 0.948 | 0.968 | 0.125 | 0.004 |

LB examples:

| Feature | Count | Readback | Dominant frac | Entropy | Ablation drop |
|---|---:|---:|---:|---:|---:|
| F01 | 10000 | 0.999 | 0.967 | 0.109 | 0.259 |
| F05 | 4000 | 0.997 | 0.892 | 0.210 | 0.489 |
| F12 | 800 | 0.987 | 0.903 | 0.261 | 0.010 |
| F16 | 200 | 0.947 | 0.808 | 0.344 | 0.029 |

## Interpretation Detail

The pressure intervention produced three signals:

1. Readback remains high.
2. NMI / ARI decrease relative to baseline.
3. Dominant expert ablation drop collapses.

The third signal is the decisive one. If pressure forced better MoE specialization, dominant expert ablation should become more important. Instead, feature prediction becomes less dependent on dominant expert output.

This suggests the model uses shared computation:

```text
embedding + attention/residual + LM head
```

or broadly shared expert corrections, rather than making the selected expert the unique carrier of each feature.

## Figures

![NMI](figures/specialization_pressure_nmi.png)

![Readback](figures/specialization_pressure_readback.png)

![Routing entropy](figures/specialization_pressure_entropy.png)

![Dominant fraction](figures/specialization_pressure_dominant_fraction.png)

![Load imbalance](figures/specialization_pressure_load_imbalance.png)

![16-feature pressure](figures/sixteen_feature_pressure_by_feature.png)

## Failure Mode Check

- Capacity bottleneck caused task failure: not observed.
- More features forced cleaner specialization: not observed.
- Readback disappeared under pressure: not observed.
- Expert output became more causally necessary: not observed.
- Shared path bypass remains open and should be diagnosed next.
