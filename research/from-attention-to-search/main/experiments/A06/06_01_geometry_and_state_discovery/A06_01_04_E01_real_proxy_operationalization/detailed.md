# Detailed: A06_01_04_E01 Real-DCLM Proxy Feature Operationalization

## Decision

A06_01_04_E01 is supported with boundary.

The experiment finds stable label-free real-DCLM proxy clusters. The support is strongest at checkpoint step 10 in late layers 3--5. The main boundary is that raw and residual k-means behave almost identically, so the evidence supports stable hidden geometry but does not support the stronger claim that common-centering is the key operation for cluster discovery.

## Artifact Map

| Item | Path |
| --- | --- |
| Anchor | `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md` |
| Protocol | `protocol.md` |
| Runner | `scripts/run_real_dclm_proxy_feature_operationalization.py` |
| Submit script | `scripts/submit_real_dclm_proxy_feature_operationalization_4gpu_acp.sh` |
| Job id | `pt-796e62re` |
| Run dir | `runs/real_dclm_proxy_feature_operationalization/a06_10_real_dclm_proxy_4gpu_20260622_full01` |
| Runtime log | `logs/acp/a06_10_real_dclm_proxy_4gpu_20260622_full01_runtime_20260622_164510.log` |
| Main table | `runs/real_dclm_proxy_feature_operationalization/a06_10_real_dclm_proxy_4gpu_20260622_full01/results/proxy_cluster_summary.csv` |
| Hidden audit | `runs/real_dclm_proxy_feature_operationalization/a06_10_real_dclm_proxy_4gpu_20260622_full01/results/hidden_audit.csv` |
| Cluster examples | `runs/real_dclm_proxy_feature_operationalization/a06_10_real_dclm_proxy_4gpu_20260622_full01/results/cluster_examples.json` |
| Local figures | `figures/` |

## Exact Setup

Data:

- DCLM packed `.bin` stream at `/data/share/109_cache_dir/hf_data/dclm_bin`.
- Sequence length: 256 input tokens plus shifted targets.
- Splits: calibration A, calibration B, and held-out eval are disjoint contiguous sample-index ranges.
- Per layer and split, 65,536 router-input tokens are collected.

Model:

- Qwen-style top-1 MoE.
- Layers: 6.
- Hidden size: 512.
- Attention heads: 8.
- KV heads: 4.
- Experts: 8.
- Expert hidden size: 2048.
- Router reference: `hidden_states`.
- Shared expert: disabled.

Run:

```text
A06_10_ALLOW_REAL_SUBMIT=1 RUN_NAME=a06_10_real_dclm_proxy_4gpu_20260622_full01 \
Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_04_E01_real_proxy_operationalization/scripts/submit_real_dclm_proxy_feature_operationalization_4gpu_acp.sh
```

ACP status:

```text
job_id: pt-796e62re
state: SUCCEEDED
start_time: 2026-06-22T16:45:10Z
complete_time: 2026-06-22T16:47:09Z
```

## Algorithm

For each seed, checkpoint, layer, and condition:

1. Collect exact router inputs using the gate forward hook.
2. Fit cluster centers on calibration split A.
3. Fit cluster centers independently on calibration split B.
4. Assign the same held-out evaluation tokens with both center sets.
5. Match centers by cosine similarity.
6. Compute held-out assignment NMI and agreement.
7. Compute nuisance NMI against token id, frequency bin, and position bucket.
8. Recompute stability after removing top-frequency tokens.

Conditions:

- `raw`: k-means on raw hidden states.
- `residual`: k-means after subtracting the calibration mean.
- `spherical_residual`: row-normalized residuals.
- `whitened_residual`: diagonal-whitened residuals.

## Primary Results

Mean over seeds and layers:

| Checkpoint | Condition | Eval NMI | Random NMI | Frequency NMI | Position NMI | Token-id NMI | Top 1% removed NMI | Top 5% removed NMI |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | raw | 0.2565 | 0.0002 | 0.0215 | 0.0134 | 0.1311 | 0.2459 | 0.2462 |
| 0 | residual | 0.2565 | 0.0002 | 0.0215 | 0.0134 | 0.1311 | 0.2459 | 0.2462 |
| 0 | spherical residual | 0.2453 | 0.0002 | 0.0198 | 0.0109 | 0.1306 | 0.2376 | 0.2379 |
| 0 | whitened residual | 0.2491 | 0.0002 | 0.0237 | 0.0118 | 0.1315 | 0.2362 | 0.2357 |
| 10 | raw | 0.5211 | 0.0002 | 0.0401 | 0.0736 | 0.1202 | 0.5143 | 0.5124 |
| 10 | residual | 0.5211 | 0.0002 | 0.0401 | 0.0736 | 0.1202 | 0.5142 | 0.5124 |
| 10 | spherical residual | 0.4854 | 0.0002 | 0.0435 | 0.0569 | 0.1477 | 0.4666 | 0.4644 |
| 10 | whitened residual | 0.4339 | 0.0002 | 0.0394 | 0.0735 | 0.1253 | 0.4255 | 0.4236 |

Residual condition by layer:

| Checkpoint | Layer | Eval NMI | Random NMI | Frequency NMI | Position NMI | Token-id NMI | Max cluster load |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.4489 | 0.0002 | 0.0821 | 0.0243 | 0.1820 | 0.2158 |
| 0 | 3 | 0.2005 | 0.0002 | 0.0015 | 0.0123 | 0.1143 | 0.1864 |
| 0 | 4 | 0.1959 | 0.0002 | 0.0011 | 0.0082 | 0.1138 | 0.1714 |
| 0 | 5 | 0.1806 | 0.0002 | 0.0012 | 0.0088 | 0.1143 | 0.1834 |
| 10 | 0 | 0.4488 | 0.0002 | 0.0661 | 0.0574 | 0.1670 | 0.2998 |
| 10 | 3 | 0.4681 | 0.0002 | 0.0462 | 0.0754 | 0.1211 | 0.3120 |
| 10 | 4 | 0.5172 | 0.0002 | 0.0226 | 0.0789 | 0.0935 | 0.3750 |
| 10 | 5 | 0.6501 | 0.0002 | 0.0252 | 0.0828 | 0.0992 | 0.3376 |

## Visualization Results

### Proxy Stability

![Proxy stability by condition](figures/full01_proxy_stability_by_condition.png)

Purpose: test whether independently estimated centers induce stable held-out proxy assignments.
How to read: higher `eval_assignment_nmi` means calibration A and calibration B agree more on the same held-out tokens after center matching.
Observed result: step-10 conditions are far above random; residual mean NMI is 0.5211 at step 10.
Take-home: a real-data proxy exists, especially after early training.
Does not prove: semantic meaning, expert utility, or that a linear router can implement the proxy.

### Frequency Nuisance

![Frequency nuisance NMI](figures/full01_nuisance_frequency_nmi_by_condition.png)

Purpose: test whether proxy labels are mostly token-frequency buckets.
How to read: if frequency NMI approached proxy-stability NMI, the proxy would be frequency-driven.
Observed result: frequency NMI is much lower than stability NMI; step-10 residual frequency NMI is 0.0401.
Take-home: measured frequency bins do not explain the proxy.
Does not prove: no finer token-identity or lexical effect remains.

### Position Nuisance

![Position nuisance NMI](figures/full01_nuisance_position_nmi_by_condition.png)

Purpose: test whether proxy labels are mostly absolute-position buckets.
How to read: lower position NMI means proxy clusters are less position-dominated.
Observed result: step-10 residual position NMI is 0.0736, still much lower than stability NMI.
Take-home: position is a guard, not the primary explanation.
Does not prove: position has no interaction with layer or training.

## Interpretation

Observation:

- Proxy stability is far above random.
- Step-10 late-layer proxy stability is much stronger than step-0 late-layer stability.
- Frequency and position nuisance metrics are lower than proxy stability.
- Removing frequent tokens does not erase the proxy signal.
- Raw and residual k-means are effectively identical.

Interpretation:

- Real DCLM hidden geometry has reproducible structure that can serve as a proxy target.
- The proxy becomes stronger after early training.
- Common-centering is still useful as a router-input diagnostic, but not as the reason k-means clusters exist.

Decision:

- Proceed to A06_01_04_E02.
- A06_01_04_E02 must test the proxy-to-linear-router bridge directly.
- A06_01_04_E02 must report actual raw-input routing and centered-input diagnostic routing separately.

## Failure / Boundary Analysis

H1, stable proxy clusters:
supported.

H2, not reducible to token frequency / position:
supported against measured frequency and position nuisances, but not a semantic claim.

H3, common-centering is needed:
weakened. Translation-invariant k-means makes raw and residual assignments nearly identical.

Most dangerous boundary:
step-0 late-layer proxy stability is modest. If the goal is a pure step-0 initialization, A06_01_04_E02 may fail even though a stronger step-10 proxy exists.

## Local Full02 Rerun (2026-06-25)

Purpose: verify the real-data proxy-discovery result on the local two-GPU surface before syncing the line.

Execution:

```text
run_name: a06_10_real_dclm_proxy_local_2gpu_20260625_full02
run_dir: runs/real_dclm_proxy_feature_operationalization/a06_10_real_dclm_proxy_local_2gpu_20260625_full02
runtime_log: logs/local/a06_10_real_dclm_proxy_local_2gpu_20260625_full02_runtime_20260625_172406.log
launcher: torchrun --standalone --nproc_per_node=2
environment: conda spectral-hier
```

Completion: 96 proxy-summary rows and 72 hidden-audit rows.

Result: reproduced. Step-10 raw/residual stability NMI is 0.5211, random NMI is 0.0002, frequency NMI is 0.0401, and position NMI is 0.0736.

Full02 artifact map:

| Item | Path |
| --- | --- |
| Proxy table | `tables/full02_proxy_cluster_summary.csv` |
| Hidden audit | `tables/full02_hidden_audit.csv` |
| Proxy stability figure | `figures/full02_proxy_stability_by_condition.png` |
| Frequency guard figure | `figures/full02_nuisance_frequency_nmi_by_condition.png` |
| Position guard figure | `figures/full02_nuisance_position_nmi_by_condition.png` |
| Run config | `runs/real_dclm_proxy_feature_operationalization/a06_10_real_dclm_proxy_local_2gpu_20260625_full02/config/run_config.json` |
| Run summary | `runs/real_dclm_proxy_feature_operationalization/a06_10_real_dclm_proxy_local_2gpu_20260625_full02/run_summary.json` |

![Full02 proxy stability](figures/full02_proxy_stability_by_condition.png)

Take-home: the local rerun keeps A06_01_04_E01 supported with the same boundary: stable proxy clusters exist, but this is not yet a method or utility claim.

## Next Decision

Run A06_01_04_E02 proxy-center router initialization.

Required carry-over conditions:

- Evaluate both step-0 and step-10 proxy sources.
- Treat step-0 as the main initialization target.
- Treat step-10 as a stronger proxy-control / warm-start boundary.
- Separate raw-input router routing from centered-input diagnostic routing.
