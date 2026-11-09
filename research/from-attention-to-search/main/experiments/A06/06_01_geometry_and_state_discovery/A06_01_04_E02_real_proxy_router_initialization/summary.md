# Summary: A06_01_04_E02 Real-DCLM Proxy-Center Router Initialization

## Purpose

This experiment tests whether the real-DCLM proxy clusters from A06_01_04_E01 can be converted into linear top-1 router rows.

## Setup

- Model/data: same DCLM MoE surface as A06_01_04_E01.
- Seeds: 0, 1, 2.
- Proxy source checkpoints: 0 and 10.
- Layers: 0, 3, 4, 5.
- Main metric: raw-input `proxy_route_nmi`, the mutual information between proxy cluster and routed expert.
- Diagnostic metric: centered-input `proxy_route_nmi`, used only to identify common-bias failure.

Run:

```text
job_id: pt-dmp3iz0j
run_name: a06_11_proxy_center_router_4gpu_20260622_full01
run_dir: runs/real_dclm_proxy_center_router_initialization/a06_11_proxy_center_router_4gpu_20260622_full01
```

## Result

Decision: supported, with boundary.

Proxy centers are linearly routable, but the best actual raw-input bridge is raw proxy centers, not residual centers. Residual centers are very readable under centered-input diagnostics, but actual raw-input routing can be suppressed by common-logit bias, especially at source step 10.

Key numbers:

| Source step | Router condition | Route space | Mean proxy-route NMI | Random NMI |
| --- | --- | --- | ---: | ---: |
| 0 | raw center equal norm | raw input | 0.7449 | 0.0343 |
| 0 | residual center equal norm | raw input | 0.5427 | 0.0343 |
| 0 | residual center equal norm | centered input | 0.8302 | 0.0338 |
| 10 | raw center equal norm | raw input | 0.8811 | 0.0417 |
| 10 | residual center equal norm | raw input | 0.2612 | 0.0417 |
| 10 | residual center equal norm | centered input | 0.6373 | 0.0811 |

Label-shuffled guard is near zero: 0.0002 at source step 0 and 0.0003 at source step 10.

## Local Full02 Rerun (2026-06-25)

Run:

```text
run_name: a06_11_proxy_center_router_local_2gpu_20260625_full02
run_dir: runs/real_dclm_proxy_center_router_initialization/a06_11_proxy_center_router_local_2gpu_20260625_full02
runtime_log: logs/local/a06_11_proxy_center_router_local_2gpu_20260625_full02_runtime_20260625_172815.log
```

Decision: reproduced.

The local two-GPU rerun completed 264 router-summary rows and 48 hidden-audit rows. It reproduced the full01 bridge: raw proxy centers are strongly routable on raw inputs, while residual centers remain mostly a centered-input diagnostic.

Key aggregate numbers:

| Source step | Router condition | Mean proxy-route NMI | Frequency NMI | Position NMI | Max load |
| --- | --- | ---: | ---: | ---: | ---: |
| 0 | random equal norm | 0.0343 | 0.0023 | 0.0026 | 0.2235 |
| 0 | raw center equal norm | 0.7449 | 0.0183 | 0.0050 | 0.1850 |
| 0 | residual center equal norm | 0.5427 | 0.0142 | 0.0089 | 0.2968 |
| 10 | random equal norm | 0.0381 | 0.0036 | 0.0133 | 0.7752 |
| 10 | raw center equal norm | 0.8811 | 0.0343 | 0.0627 | 0.3216 |
| 10 | residual center equal norm | 0.2612 | 0.0238 | 0.0332 | 0.7043 |

Curated artifacts:

- `tables/full02_router_initialization_summary.csv`
- `tables/full02_hidden_audit.csv`
- `figures/full02_proxy_route_nmi_source_step_0.png`
- `figures/full02_proxy_route_nmi_source_step_10.png`

## Central Figures

![Step-0 proxy route NMI](figures/full01_proxy_route_nmi_source_step_0.png)

This figure tests whether step-0 proxy centers can become router rows. Raw-center rows give the strongest actual raw-input routing. Residual and whitened centers become stronger only when evaluated on centered inputs, which is diagnostic rather than a deployable raw router.

![Step-10 proxy route NMI](figures/full01_proxy_route_nmi_source_step_10.png)

This figure tests whether the stronger A06_01_04_E01 step-10 proxy is linearly routable. Raw-center rows are highly routable, while residual-center raw-input routing is weakened by common bias.

## Claim Boundary

Can claim:

- A06_01_04_E01 proxy clusters can be made linearly routable.
- Raw proxy centers are the best candidate for actual raw-input router initialization.
- Residual centers expose a common-bias bottleneck: centered routing is strong, but actual raw routing can collapse.

Cannot claim:

- training preservation;
- expert utility;
- semantic expert roles;
- that residual-center routing is the best deployable initialization.

## Next Decision

Proceed to A06_01_04_E03 with:

1. `raw_center_equal_norm` as the main proxy initialization;
2. `residual_center_equal_norm` as the common-bias comparison;
3. random and equal-norm random guards;
4. proxy-route NMI at steps 10 and 50 as the primary preservation test.
