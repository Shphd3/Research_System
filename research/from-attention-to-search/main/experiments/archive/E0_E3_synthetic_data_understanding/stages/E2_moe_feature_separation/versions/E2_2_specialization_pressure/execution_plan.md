# Execution Plan: E2.2 Specialization Pressure Test

## 1. Run Goal

Test whether specialization pressure makes top-1 MoE routing more feature-aligned without changing router objective.

## 2. Conditions

Baseline:

```text
condition = baseline_e2_ffn128_4feat
features = ABC / DEF / GHI / JKL
ffn_dim = 128
source = active/synthetic_data_understanding/outputs/e2_augmented_all_trigram_v1000/
```

Capacity bottleneck:

```text
condition = bottleneck_ffn16_4feat
features = ABC / DEF / GHI / JKL
ffn_dim = 16
steps = 5000
seeds = 20260513,20260514,20260515
```

Feature-count pressure:

```text
condition = pressure_ffn16_16feat
features = F01-F16
ffn_dim = 16
steps = 5000
seeds = 20260513,20260514,20260515
```

## 3. Commands

Generate 16-feature data:

```bash
python active/synthetic_data_understanding/scripts/generate_synthetic_patterns.py \
  --config active/synthetic_data_understanding/configs/e2_2_specialization_pressure_data.json \
  --out-dir active/synthetic_data_understanding/data_e2_2_specialization_pressure
```

Run bottleneck:

```bash
python active/synthetic_data_understanding/scripts/train_moe_feature_separation.py \
  --run-config active/synthetic_data_understanding/configs/e2_2_capacity_bottleneck_four_feature.json
```

Run 16-feature pressure:

```bash
python active/synthetic_data_understanding/scripts/train_moe_feature_separation.py \
  --run-config active/synthetic_data_understanding/configs/e2_2_sixteen_feature_pressure.json
```

Aggregate:

```bash
python active/synthetic_data_understanding/scripts/plot_specialization_pressure.py \
  --baseline-dir active/synthetic_data_understanding/outputs/e2_augmented_all_trigram_v1000 \
  --bottleneck-dir active/synthetic_data_understanding/outputs/e2_2_capacity_bottleneck_four_feature \
  --pressure-dir active/synthetic_data_understanding/outputs/e2_2_sixteen_feature_pressure \
  --out-dir active/synthetic_data_understanding/outputs/e2_2_specialization_pressure \
  --fig-dir active/synthetic_data_understanding/figures/e2_2_specialization_pressure
```

## 4. Metrics

- final CE;
- NMI / ARI;
- mean feature readback probability;
- dominant expert ablation drop;
- routing entropy;
- dominant expert fraction;
- expert load imbalance.

## 5. Artifacts

Tables:

```text
specialization_pressure_summary.csv
specialization_pressure_feature_summary.csv
```

Figures:

```text
specialization_pressure_nmi.png
specialization_pressure_readback.png
specialization_pressure_entropy.png
specialization_pressure_dominant_fraction.png
specialization_pressure_load_imbalance.png
sixteen_feature_pressure_by_feature.png
```

## 6. Result Location

Ignored workspace:

```text
active/synthetic_data_understanding/outputs/e2_2_specialization_pressure/
active/synthetic_data_understanding/figures/e2_2_specialization_pressure/
```

Mainline:

```text
main/experiments/E0_E3_synthetic_data_understanding/stages/E2_moe_feature_separation/versions/E2_2_specialization_pressure/
```
