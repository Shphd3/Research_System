# Detailed Notes: R0/R1 Two-Pass Reverse Index Diagnostic

## Run

Workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
```

Command:

```bash
python scripts/run_two_pass_reverse_index_diagnostic.py \
  --mode full \
  --config configs/r0_r1_two_pass_ri_uniform_zipf_soft_router.json \
  --skip-completed
```

Config:

```text
configs/r0_r1_two_pass_ri_uniform_zipf_soft_router.json
```

Seeds:

```text
20260513, 20260514, 20260515
```

## Model

Diagnostic 2-layer model:

```text
token + position embedding
-> layer1 causal attention
-> router on layer1 attention_output
-> MoE FFN
-> layer2 causal attention
-> LM head
```

Reverse Index diagnostic:

1. full forward gives layer2 dense attention teacher;
2. candidate generator selects restricted KV set;
3. exact QK attention is recomputed on candidate KV;
4. logits and CE are compared with full attention.

## Variants

```text
M0: natural router + LB
M1: soft feature-router loss lambda=0.05
M2: soft feature-router loss lambda=0.20
```

`feature-router loss` only applies at planted feature prefix-end positions.

## Metrics

Primary metric:

$$
\Delta CE
=
CE_{\text{candidate attention}} - CE_{\text{full attention}}
$$

Random comparison:

$$
\mathrm{Improvement}
=
\Delta CE_{\text{random}} - \Delta CE_{\text{RI}}
$$

Positive improvement means RI same-bucket is better than random same-count.

## Main Tables

- `aggregate_ri_summary_by_generator.csv`
- `ri_vs_random_ce_summary.csv`

## Important Result Pattern

M1 is the most favorable setting:

```text
uniform: random ΔCE +0.182 -> RI ΔCE +0.034
zipf:    random ΔCE +0.134 -> RI ΔCE +0.030
```

But local / same-feature oracle are almost full-attention equivalent:

```text
uniform M1 local ΔCE +0.001, same-feature ΔCE +0.001
zipf M1 local ΔCE +0.000, same-feature ΔCE +0.001
```

This means router bucket has signal, but it is not yet the right candidate generator.

## Figure Index

- `figures/fig_uniform_ce_delta_baselines.png`: uniform CE delta across candidate generators.
- `figures/fig_zipf_ce_delta_baselines.png`: zipf CE delta across candidate generators.
- `figures/fig_uniform_ri_ce_improvement_vs_random.png`: uniform RI improvement over random.
- `figures/fig_zipf_ri_ce_improvement_vs_random.png`: zipf RI improvement over random.
- `figures/fig_uniform_mean_attention_mass_retained_mean.png`: uniform attention mass retained.
- `figures/fig_zipf_mean_attention_mass_retained_mean.png`: zipf attention mass retained.

## Reliability Checks

Implemented checks:

- candidate attention uses exact QK over restricted KV;
- candidate count is matched for random/local against RI same-bucket;
- causal candidate set only uses positions up to current query position;
- dense layer2 attention is used as teacher;
- CE delta and target probability delta are recorded, not only recall.

Interpretation boundary:

This is not a latency result because full attention is computed for teacher evaluation. It is a candidate-quality diagnostic.
