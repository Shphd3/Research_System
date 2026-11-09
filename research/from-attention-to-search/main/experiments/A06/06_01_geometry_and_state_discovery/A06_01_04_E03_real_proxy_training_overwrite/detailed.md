# Detailed: A06_01_04_E03 Real-DCLM Proxy-Init Training Preservation

## Decision

A06_01_04_E03 weakens the preservation hypothesis. The real-DCLM proxy initialization works at step 0 but is quickly overwritten by ordinary next-token training.

## Artifact Map

| Item | Path |
| --- | --- |
| Anchor | `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md` |
| Protocol | `protocol.md` |
| Runner | `scripts/run_real_dclm_proxy_init_training_preservation.py` |
| Submit script | `scripts/submit_real_dclm_proxy_init_training_preservation_4gpu_acp.sh` |
| Job id | `pt-8577iw38` |
| Run dir | `runs/real_dclm_proxy_init_training_preservation/a06_12_proxy_init_training_4gpu_20260622_full01` |
| Main table | `runs/real_dclm_proxy_init_training_preservation/a06_12_proxy_init_training_4gpu_20260622_full01/results/training_preservation_summary.csv` |
| Runtime log | `logs/acp/a06_12_proxy_init_training_4gpu_20260622_full01_runtime_20260622_170429.log` |

## Primary Results

Mean over seeds and layers:

| Variant | Step | Proxy-route NMI | Max load | Active ratio | Common margin | LM loss |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| random | 0 | 0.0379 | 0.1983 | 1.0000 | 0.0521 |  |
| random | 10 | 0.0047 | 0.9830 | 0.9861 | 0.5783 | 10.7190 |
| random | 50 | 0.0339 | 0.7439 | 0.8750 | 0.1764 | 7.8930 |
| raw-center | 0 | 0.7549 | 0.1812 | 1.0000 | 0.1147 |  |
| raw-center | 1 | 0.5037 | 0.2523 | 1.0000 | 0.1615 | 12.0343 |
| raw-center | 2 | 0.3271 | 0.3801 | 1.0000 | 0.2504 | 11.9200 |
| raw-center | 3 | 0.1901 | 0.5839 | 1.0000 | 0.3824 | 11.7440 |
| raw-center | 5 | 0.0410 | 0.9479 | 1.0000 | 0.7527 | 11.1926 |
| raw-center | 10 | 0.0131 | 0.9645 | 1.0000 | 0.6995 | 10.7222 |
| raw-center | 50 | 0.0337 | 0.7575 | 0.8472 | 0.1950 | 7.8827 |
| residual-center | 0 | 0.2712 | 0.2647 | 1.0000 | 0.1972 |  |
| residual-center | 10 | 0.0038 | 0.9953 | 1.0000 | 1.3840 | 10.7246 |
| residual-center | 50 | 0.0399 | 0.6972 | 0.9306 | 0.2209 | 7.8753 |

## Visualization Results

### Proxy Preservation

![Proxy route NMI trajectory](figures/full01_trajectory_proxy_route_nmi.png)

Purpose: test whether proxy routing survives training.
Observed result: raw-center starts at 0.7549, drops to 0.0410 at step 5, and reaches 0.0131 at step 10.
Take-home: the proxy route is not preserved.

### Route Concentration

![Route max load trajectory](figures/full01_trajectory_route_max_cluster_load.png)

Purpose: test whether route collapse accompanies proxy loss.
Observed result: all variants concentrate strongly by step 5--10.
Take-home: ordinary DCLM training rapidly overwrites the initialization basin.

### Common Margin

![Common margin trajectory](figures/full01_trajectory_common_margin.png)

Purpose: test whether common-logit amplification accompanies collapse.
Observed result: common margin rises during the same early window where proxy NMI collapses.

### LM Loss

![LM loss trajectory](figures/full01_trajectory_lm_loss.png)

Purpose: test whether proxy-init collapse is caused by failed training.
Observed result: LM loss is comparable across variants.

## Interpretation

Stage contracts:

- A06_01_04_E01 proxy discovery: passed.
- A06_01_04_E02 linear bridge: passed for raw-center initialization.
- A06_01_04_E03 training preservation: failed.

The failure is training feedback override. The model can start in a proxy-specialized router state, but standard LM training quickly moves routing into the same concentration regime seen in random baselines.

## Claim Boundary

This is not a negative result about all proxy initialization. It is a negative result about preservation under the current ordinary next-token objective, optimizer, scale, and top-1 MoE setup through step 50.

## Local Full02 Rerun (2026-06-25)

Purpose: verify the preservation failure on the local two-GPU surface before syncing the line.

Execution:

```text
run_name: a06_12_proxy_init_training_local_2gpu_20260625_full02
run_dir: runs/real_dclm_proxy_init_training_preservation/a06_12_proxy_init_training_local_2gpu_20260625_full02
runtime_log: logs/local/a06_12_proxy_init_training_local_2gpu_20260625_full02_runtime_20260625_173043.log
launcher: torchrun --standalone --nproc_per_node=2
environment: conda spectral-hier
```

Completion: all 12/12 training tasks completed; 288 trajectory rows written.

Result: reproduced. Raw-center starts at proxy-route NMI 0.7549, drops to 0.0410 at step 5, and reaches 0.0131 at step 10. LM loss stays comparable to random baselines.

Full02 artifact map:

| Item | Path |
| --- | --- |
| Trajectory table | `tables/full02_training_preservation_summary.csv` |
| Proxy NMI figure | `figures/full02_trajectory_proxy_route_nmi.png` |
| Max-load figure | `figures/full02_trajectory_route_max_cluster_load.png` |
| LM-loss figure | `figures/full02_trajectory_lm_loss.png` |
| Common-margin figure | `figures/full02_trajectory_common_margin.png` |
| Run config | `runs/real_dclm_proxy_init_training_preservation/a06_12_proxy_init_training_local_2gpu_20260625_full02/config/run_config.json` |
| Run summary | `runs/real_dclm_proxy_init_training_preservation/a06_12_proxy_init_training_local_2gpu_20260625_full02/run_summary.json` |

![Full02 proxy route NMI trajectory](figures/full02_trajectory_proxy_route_nmi.png)

![Full02 route max load trajectory](figures/full02_trajectory_route_max_cluster_load.png)

Take-home: the local rerun keeps A06_01_04_E03 unsupported. The current bottleneck is preservation under ordinary training, not proxy discovery or step-0 router construction.

## Next Decision

Run A06_01_04_E04 to localize the failure contract and decide whether the next method should add an anti-collapse/preservation objective, freeze schedule, lower router learning rate, or delayed router training.
