# Detailed: A06_01_04_E02 Real-DCLM Proxy-Center Router Initialization

## Decision

A06_01_04_E02 is supported with boundary.

The proxy-to-linear bridge exists. The important correction is that actual raw-input routing prefers raw proxy centers. Residual centers are highly linearly readable only when the input is also centered, so residual-center rows diagnose common-bias sensitivity rather than directly solving raw routing.

## Artifact Map

| Item | Path |
| --- | --- |
| Anchor | `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md` |
| Protocol | `protocol.md` |
| Runner | `scripts/run_real_dclm_proxy_center_router_initialization.py` |
| Submit script | `scripts/submit_real_dclm_proxy_center_router_initialization_4gpu_acp.sh` |
| Job id | `pt-dmp3iz0j` |
| Run dir | `runs/real_dclm_proxy_center_router_initialization/a06_11_proxy_center_router_4gpu_20260622_full01` |
| Main table | `runs/real_dclm_proxy_center_router_initialization/a06_11_proxy_center_router_4gpu_20260622_full01/results/router_initialization_summary.csv` |
| Hidden audit | `runs/real_dclm_proxy_center_router_initialization/a06_11_proxy_center_router_4gpu_20260622_full01/results/hidden_audit.csv` |
| Runtime log | `logs/acp/a06_11_proxy_center_router_4gpu_20260622_full01_runtime_20260622_165454.log` |
| Local figures | `figures/` |

## Exact Setup

Data and model match A06_01_04_E01. The experiment uses the same disjoint DCLM audit surfaces and exact router-input capture.

Conditions:

- `raw_center_equal_norm`: k-means centers from raw hidden states, normalized to equal row norm.
- `residual_center_equal_norm`: k-means centers from mean-subtracted hidden states, normalized to equal row norm.
- `whitened_center_equal_norm`: diagonal-whitened residual centers mapped back to hidden coordinates.
- `random_gaussian`: random Gaussian rows.
- `random_equal_norm`: random equal-norm rows.
- `label_shuffled_guard`: residual-center routing evaluated against shuffled proxy labels.

Both route spaces are reported:

- `raw_input`: actual router use case.
- `centered_input`: diagnostic only; it asks whether common bias is the failure source.

## Primary Results

Mean over seeds and layers:

| Source step | Router condition | Route space | Proxy-route NMI | Max load | Active ratio | Common margin |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| 0 | raw center | raw input | 0.7449 | 0.1850 | 1.0000 | 0.2269 |
| 0 | residual center | raw input | 0.5427 | 0.2968 | 1.0000 | 0.9934 |
| 0 | residual center | centered input | 0.8302 | 0.1839 | 1.0000 | 0.9934 |
| 0 | random equal norm | raw input | 0.0343 | 0.2235 | 1.0000 | 0.1463 |
| 10 | raw center | raw input | 0.8811 | 0.3216 | 1.0000 | 0.0496 |
| 10 | residual center | raw input | 0.2612 | 0.7043 | 0.9792 | 2.0352 |
| 10 | residual center | centered input | 0.6373 | 0.2816 | 1.0000 | 2.0352 |
| 10 | random equal norm | raw input | 0.0381 | 0.7752 | 1.0000 | 0.4623 |

Residual-center layer detail:

| Source step | Route space | Layer | Proxy-route NMI | Max load | Common margin |
| --- | --- | ---: | ---: | ---: | ---: |
| 0 | raw input | 0 | 0.4862 | 0.3541 | 0.6300 |
| 0 | raw input | 3 | 0.5113 | 0.3295 | 1.7911 |
| 0 | raw input | 4 | 0.5714 | 0.2726 | 0.8456 |
| 0 | raw input | 5 | 0.6020 | 0.2310 | 0.7068 |
| 0 | centered input | 3 | 0.8335 | 0.1729 | 1.7911 |
| 0 | centered input | 4 | 0.8664 | 0.1671 | 0.8456 |
| 10 | raw input | 4 | 0.1571 | 0.8137 | 3.5957 |
| 10 | raw input | 5 | 0.1423 | 0.8545 | 1.5529 |
| 10 | centered input | 4 | 0.6332 | 0.2643 | 3.5957 |
| 10 | centered input | 5 | 0.6025 | 0.3736 | 1.5529 |

## Visualization Results

### Step-0 Source

![Step-0 proxy route NMI](figures/full01_proxy_route_nmi_source_step_0.png)

Purpose: test pure initialization-time proxy-to-router conversion.
How to read: higher bars mean the router's top-1 expert follows proxy labels better.
Observed result: raw-center raw-input routing is strongest; residual/whitened centers become strongest only under centered-input diagnostics.
Take-home: step-0 proxy centers are linearly routable; raw centers are the better actual initialization candidate.
Does not prove: preservation after training.

### Step-10 Source

![Step-10 proxy route NMI](figures/full01_proxy_route_nmi_source_step_10.png)

Purpose: test the stronger A06_01_04_E01 proxy source.
How to read: compare actual raw-input routing with centered-input diagnostics.
Observed result: raw-center rows route strongly; residual raw-input routing collapses relative to centered-input routing because common margin is large.
Take-home: common bias is a real bridge failure mode.
Does not prove: step-10 warm-start is a deployable initialization.

## Interpretation

Observation:

- Raw-center rows strongly route by proxy labels.
- Residual-center rows are highly readable when inputs are centered.
- Residual-center raw-input routing is degraded by common-logit bias.
- Random and label-shuffled guards are near zero.

Decision:

- Use raw-center equal-norm initialization as the main A06_01_04_E03 condition.
- Use residual-center equal-norm as a common-bias comparison.
- Do not claim residual-center initialization is solved.

## Claim Boundary

The experiment proves a linear bridge exists for A06_01_04_E01 proxy labels. It does not prove that this bridge survives optimization or that routed experts have utility.

## Local Full02 Rerun (2026-06-25)

Purpose: verify the proxy-center-to-router bridge on the local two-GPU surface before syncing the line.

Execution:

```text
run_name: a06_11_proxy_center_router_local_2gpu_20260625_full02
run_dir: runs/real_dclm_proxy_center_router_initialization/a06_11_proxy_center_router_local_2gpu_20260625_full02
runtime_log: logs/local/a06_11_proxy_center_router_local_2gpu_20260625_full02_runtime_20260625_172815.log
launcher: torchrun --standalone --nproc_per_node=2
environment: conda spectral-hier
```

Completion: 264 router-summary rows and 48 hidden-audit rows.

Result: reproduced. Raw-center raw-input routing reaches mean proxy-route NMI 0.7449 from source step 0 and 0.8811 from source step 10. Residual-center raw-input routing remains weaker, while centered-input diagnostics remain high.

Full02 artifact map:

| Item | Path |
| --- | --- |
| Router table | `tables/full02_router_initialization_summary.csv` |
| Hidden audit | `tables/full02_hidden_audit.csv` |
| Step-0 figure | `figures/full02_proxy_route_nmi_source_step_0.png` |
| Step-10 figure | `figures/full02_proxy_route_nmi_source_step_10.png` |
| Run config | `runs/real_dclm_proxy_center_router_initialization/a06_11_proxy_center_router_local_2gpu_20260625_full02/config/run_config.json` |
| Run summary | `runs/real_dclm_proxy_center_router_initialization/a06_11_proxy_center_router_local_2gpu_20260625_full02/run_summary.json` |

![Full02 step-0 proxy route NMI](figures/full02_proxy_route_nmi_source_step_0.png)

![Full02 step-10 proxy route NMI](figures/full02_proxy_route_nmi_source_step_10.png)

Take-home: the local rerun keeps A06_01_04_E02 supported with the same boundary: the proxy can initialize a router, but preservation is still untested in this anchor.

## Next Decision

Run A06_01_04_E03 training preservation. The main question becomes: does raw-center proxy routing survive real DCLM next-token training through steps 10 and 50?
