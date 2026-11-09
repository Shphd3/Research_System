# Execution Plan: E0 Synthetic Data Sanity

## 1. Run Goal

Generate controlled synthetic token streams and audit whether they contain the intended planted pattern-level features before any model training.

## 2. Data Construction

Use the operational config:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/e0_synthetic_data_sanity.json
```

Default settings:

- seed: `20260513`
- vocabulary size: $V=100$
- corpus length: $N=10^6$
- collision policy: `log`

Regimes:

- `random_only`: iid random tokens.
- `one_feature`: `[1,2]` with target count `10000`.
- `four_feature_zipf`: `[1,2]`, `[3,4,5]`, `[6,7]`, `[8,9]` with target counts `10000`, `5000`, `500`, `100`.

## 3. Commands

From `XingyuD/Attention_Search_Experiments`:

```bash
python active/synthetic_data_understanding/scripts/generate_synthetic_patterns.py \
  --config active/synthetic_data_understanding/configs/e0_synthetic_data_sanity.json \
  --out-dir active/synthetic_data_understanding/data

python active/synthetic_data_understanding/scripts/audit_synthetic_patterns.py \
  --config active/synthetic_data_understanding/configs/e0_synthetic_data_sanity.json \
  --data-dir active/synthetic_data_understanding/data \
  --out-dir active/synthetic_data_understanding/outputs \
  --fig-dir active/synthetic_data_understanding/figures
```

## 4. Metrics And Artifacts

Expected artifacts:

- `outputs/data_audit.json`
- `outputs/feature_count_table.csv`
- `outputs/conditional_probability_table.csv`
- `outputs/rank_frequency.csv`
- `figures/rank_frequency.png` if `matplotlib` is available.

Metrics:

- target count vs actual count;
- background collision count;
- empirical conditional probability;
- prefix entropy;
- background entropy;
- fitted Zipf slope.

## 5. Pass / Fail Criteria

Pass if:

- all target counts and collision counts are reported;
- feature prefixes show lower entropy than random background;
- empirical conditional probabilities reflect the planted transitions;
- four-feature frequency order remains long-tailed.

Fail if:

- collision counts are not reported;
- low-frequency planted features are near collision scale;
- feature prefixes do not show conditional next-token signal.

## 6. Result Location

Generated data and outputs stay in the ignored experiment workspace:

```text
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```

Only a claim-safe result summary should later be copied into:

```text
main/experiments/E0_E3_synthetic_data_understanding/stages/E0_data_sanity/summary.md
main/experiments/E0_E3_synthetic_data_understanding/stages/E0_data_sanity/detailed.md
```
