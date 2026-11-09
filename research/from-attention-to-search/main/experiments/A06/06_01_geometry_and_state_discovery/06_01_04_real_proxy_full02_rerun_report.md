# 06_01_04 Real-DCLM Full02 Local Rerun Report

## Decision

The local two-GPU full02 rerun reproduces the three real-proxy clauses now
owned by parent `06_01`, subanchor `06_01_04`. Historical run identifiers are
kept unchanged for reproduction.

Real DCLM hidden states contain stable proxy clusters, and those clusters can be converted into strong step-0 router rows. Ordinary next-token training still overwrites the proxy route by step 5--10. The active bottleneck is preservation, not proxy discovery or step-0 router construction.

## Runs

| Anchor | Run name | Completion | Primary result |
| --- | --- | --- | --- |
| `A06_01_04_E01` proxy discovery | `a06_10_real_dclm_proxy_local_2gpu_20260625_full02` | 96 proxy rows, 72 hidden rows | step-10 raw/residual stability NMI = 0.5211 |
| `A06_01_04_E02` Router bridge | `a06_11_proxy_center_router_local_2gpu_20260625_full02` | 264 Router rows, 48 hidden rows | step-10 raw-center proxy-route NMI = 0.8811 |
| `A06_01_04_E03` preservation | `a06_12_proxy_init_training_local_2gpu_20260625_full02` | 12/12 tasks, 288 trajectory rows | raw-center NMI 0.7549 -> 0.0410 at step 5 -> 0.0131 at step 10 |

Execution surface:

```text
environment: conda spectral-hier
launcher: torchrun --standalone --nproc_per_node=2
local GPUs: 2
date: 2026-06-25
```

## Key Evidence

### A06_01_04_E01: Proxy Exists

Primary metric: held-out proxy assignment stability, `eval_assignment_nmi`.

| Checkpoint | Condition | Stability NMI | Random NMI | Frequency NMI | Position NMI |
| --- | --- | ---: | ---: | ---: | ---: |
| 0 | raw/residual | 0.2565 | 0.0002 | 0.0215 | 0.0134 |
| 10 | raw/residual | 0.5211 | 0.0002 | 0.0401 | 0.0736 |
| 10 | spherical residual | 0.4853 | 0.0002 | 0.0435 | 0.0569 |
| 10 | whitened residual | 0.4339 | 0.0002 | 0.0394 | 0.0735 |

![Proxy stability](A06_01_04_E01_real_proxy_operationalization/figures/full02_proxy_stability_by_condition.png)

Interpretation: the proxy is stable above random and measured nuisance labels. This does not prove semantic expert roles.

### A06_01_04_E02: Proxy Is Routable

Primary metric: held-out raw-input `proxy_route_nmi`.

| Source step | Router condition | Proxy-route NMI | Max load |
| --- | --- | ---: | ---: |
| 0 | raw center equal norm | 0.7449 | 0.1850 |
| 0 | residual center equal norm | 0.5427 | 0.2968 |
| 10 | raw center equal norm | 0.8811 | 0.3216 |
| 10 | residual center equal norm | 0.2612 | 0.7043 |

![Step-10 proxy route NMI](A06_01_04_E02_real_proxy_router_initialization/figures/full02_proxy_route_nmi_source_step_10.png)

Interpretation: raw proxy centers are a strong actual router initialization. Residual centers are mainly a centered-input diagnostic because common bias weakens raw-input routing.

### A06_01_04_E03: Ordinary Training Does Not Preserve It

Primary metric: `proxy_route_nmi` at steps 5 and 10.

| Variant | Step 0 NMI | Step 5 NMI | Step 10 NMI | Step 50 NMI | Step 10 loss |
| --- | ---: | ---: | ---: | ---: | ---: |
| random | 0.0379 | 0.0147 | 0.0047 | 0.0339 | 10.7190 |
| equal-norm random | 0.0351 | 0.0166 | 0.0037 | 0.0297 | 10.7171 |
| raw-center | 0.7549 | 0.0410 | 0.0131 | 0.0337 | 10.7222 |
| residual-center | 0.2712 | 0.0282 | 0.0038 | 0.0399 | 10.7246 |

![Proxy route trajectory](A06_01_04_E03_real_proxy_training_overwrite/figures/full02_trajectory_proxy_route_nmi.png)

Interpretation: the raw-center bridge is real at step 0, but ordinary training erases it before utility can be claimed.

## Claim Boundary

Can claim:

- real-DCLM proxy clusters are reproducible;
- proxy centers can initialize a router that follows those clusters at step 0;
- ordinary real-DCLM training in this setup overwrites the proxy route by step 5--10.

Cannot claim:

- semantic expert specialization;
- utility improvement;
- that proxy initialization is intrinsically useless;
- that a preservation objective, freeze schedule, or router learning-rate control cannot work.

## Next Decision

Do not move directly to utility. The next decisive question is:

```text
Which preservation control keeps proxy_route_NMI high through step 5/10 without hurting LM loss?
```

The current candidate mechanisms are anti-collapse regularization, router-freeze schedules, lower router learning rate, and delayed router release.

## Source Artifacts

```text
./A06_01_04_E01_real_proxy_operationalization/summary.md
./A06_01_04_E01_real_proxy_operationalization/detailed.md
./A06_01_04_E02_real_proxy_router_initialization/summary.md
./A06_01_04_E02_real_proxy_router_initialization/detailed.md
./A06_01_04_E03_real_proxy_training_overwrite/summary.md
./A06_01_04_E03_real_proxy_training_overwrite/detailed.md
```
