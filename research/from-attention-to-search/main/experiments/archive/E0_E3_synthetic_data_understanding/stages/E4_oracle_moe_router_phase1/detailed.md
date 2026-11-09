# Detailed Notes: E4 Oracle-MoE Router Phase 1

## Run Status

Local checks passed before ACP:

- C0/C2/C3 training smoke on CPU, `seed=20260513`, `steps=2`;
- D0-D7 behavior diagnostic smoke on smoke checkpoints;
- C-series boundary direction audit smoke.

ACP attempts and final jobs:

| job | state | note |
|---|---|---|
| `pt-jjia1fqr` | stopped | first command did not export remote variables correctly |
| `pt-v40j6g6c` | stopped | 4-card spot queue stayed `STARTING` |
| `pt-z7v3h4tq` | failed | 2-card retry missed remote `GPU_COUNT` export |
| `pt-ynr58ys8` | stopped | 2-card spot retry stopped after switching to guaranteed 4-card policy |
| `pt-l65uzwbz` | succeeded | Phase 1 training, 4-card guaranteed/default resource |
| `pt-vhg9jerf` | succeeded | behavior diagnostic + boundary audit, 4-card guaranteed/default resource |

The ACP submit scripts and `skills/experiment-acp-runner/SKILL.md` now use this quota rule:

- `GPU_COUNT <= 4`: omit `--quota-type=spot`, use guaranteed/default resources;
- `GPU_COUNT > 4`: set `QUOTA_TYPE=spot` and pass `--quota-type="${QUOTA_TYPE}"`.

## Artifact Paths

Ignored workspace outputs:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/oracle_moe_router_phase1_20260519/
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/outputs/router_behavior_diagnostic_20260519/
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/oracle_moe_router_phase1_20260519/
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/router_behavior_diagnostic_20260519/
```

Mainline-safe copied figures:

```text
Projects/from-attention-to-search/main/experiments/E0_E3_synthetic_data_understanding/stages/E4_oracle_moe_router_phase1/figures/
```

## Output Audit

- training checkpoints: 25
- training `metrics_summary.csv`: 25 single-run files plus 1 aggregate table
- diagnostic run folders: 25
- diagnostic `analysis.md`: 25 single-run files plus 1 aggregate report
- boundary direction audit folder: generated

## Training Metrics

| variant | mean NTP loss | token acc | readback | mean NMI | mean ARI-like |
|---|---:|---:|---:|---:|---:|
| C0 standard linear | 6.6431 | 0.0368 | 0.9999 | 0.4623 | 0.3387 |
| C1 fixed parameter center | 6.6414 | 0.0369 | 0.9998 | 0.7732 | 0.5617 |
| C2 trainable center + repulsion | 6.6421 | 0.0369 | 1.0000 | 0.6627 | 0.3993 |
| C3 inhibition margin | 6.6602 | 0.0365 | 1.0000 | 0.6848 | 0.5160 |
| C4 center + inhibition | 6.6578 | 0.0367 | 0.9999 | 0.3644 | 0.2563 |

NTP loss remains near random-background scale because the corpus is mostly random tokens. The readback metric is the relevant feature-prefix metric here.

## Router Behavior Diagnostic

Aggregate factor MI:

| factor | mean MI with expert |
|---|---:|
| attention source token | 0.5571 |
| feature | 0.5553 |
| target token | 0.5553 |
| prefix-end token | 0.5553 |
| loss bin | 0.2979 |
| hidden norm bin | 0.2589 |
| router entropy bin | 0.1873 |
| position mod seq | 0.0057 |

Important limitation: in `unique_uniform`, feature, target token, prefix-end token, and attention source token are highly confounded. Therefore this diagnostic cannot distinguish relation-level feature routing from token shortcut routing.

Expert utility alignment:

| variant | router selects best expert | selected-best CE gap |
|---|---:|---:|
| C0 | 0.9992 | 0.0000 |
| C1 | 0.2949 | 2.2010 |
| C2 | 0.9996 | 0.0000 |
| C3 | 0.9949 | 0.0002 |
| C4 | 0.9956 | 0.0001 |

C1 is the clearest negative control: center geometry can produce apparently structured routing, but it does not select the functionally best expert.

## Boundary Direction Audit

Implementation note:

```text
gate_input = attention_output
router logits are computed from router_ln(gate_input)
center routers additionally use normalize(router_ln(gate_input))
```

Therefore the reported boundary alignment and SVD-band energy are measured in
the actual router-space used by the checkpoint, not in raw attention-output
space. This result should be retained as the `LN(attention_output)` condition.
The next control should remove this router LayerNorm and route from raw
attention output directly.

| variant | feature alignment | top shared | middle | tail | NMI | selects best |
|---|---:|---:|---:|---:|---:|---:|
| C0 | 0.3117 | 0.7855 | 0.1690 | 0.0455 | 0.4650 | 0.9992 |
| C1 | 0.0992 | 0.2893 | 0.4542 | 0.2566 | 0.4098 | 0.2949 |
| C2 | 0.3339 | 0.7977 | 0.1665 | 0.0358 | 0.6650 | 0.9996 |
| C3 | 0.3554 | 0.8852 | 0.0804 | 0.0344 | 0.6853 | 0.9949 |
| C4 | 0.2782 | 0.9228 | 0.0719 | 0.0053 | 0.3575 | 0.9956 |

Position-specific mean absolute cosine:

| variant | prefix first | prefix end | target pos | background |
|---|---:|---:|---:|---:|
| C0 | 0.3185 | 0.3117 | 0.3755 | 0.3140 |
| C1 | 0.1204 | 0.0992 | 0.1108 | 0.1344 |
| C2 | 0.3447 | 0.3339 | 0.3277 | 0.2877 |
| C3 | 0.3746 | 0.3554 | 0.4694 | 0.4753 |
| C4 | 0.3342 | 0.2782 | 0.4602 | 0.4794 |

For C3/C4, background and target positions have high alignment, so prefix-end feature alignment is not uniquely diagnostic of context-feature routing.

## Figure Register

- `figures/fig_e4_training_metrics.png`: NTP loss, readback, NMI by variant.
- `figures/fig_e4_router_factor_mi.png`: factor MI comparison.
- `figures/fig_c_variant_feature_alignment.png`: feature-boundary cosine by variant.
- `figures/fig_c_variant_boundary_band_energy.png`: router boundary energy across SVD bands.
- `figures/fig_c_boundary_alignment_vs_utility.png`: boundary alignment versus expert utility.
- `figures/fig_c_feature_vs_router_svd_band_energy.png`: feature direction band energy versus router boundary band energy.
- `figures/fig_c_position_feature_alignment.png`: position-specific feature-boundary alignment.
- `figures/fig_c_forced_routing_utility_matrix.png`: forced-routing utility matrix.

## Failure Analysis

The run itself completed cleanly. The main scientific limitation is not execution failure; it is dataset confounding. In `unique_uniform`, these variables are almost inseparable:

```text
feature id
prefix-end token
target token
attention source token
```

Therefore, high MI(feature, expert) cannot yet prove feature-level routing. It may be token shortcut or target shortcut.

## Next Required Control

Run Oracle-MoE on:

```text
shared prefix-end token
shared target token
crossed-factorial relation
```

Only if feature assignment, boundary alignment, utility diagonality, and readback survive those controls should this branch proceed to Reverse Index.
