# Detailed: A06_01_04_E04 Real-DCLM Proxy-Init Failure Decomposition

## Decision

The bottleneck is training feedback override.

The stage order is:

```text
h -> q: pass with boundary
q -> a(0): pass
a(0) -> a(t): fail
```

## Artifact Map

| Item | Path |
| --- | --- |
| Anchor | `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md` |
| Protocol | `protocol.md` |
| Script | `scripts/run_failure_decomposition.py` |
| Run dir | `runs/failure_decomposition/a06_13_failure_decomposition_20260622_full01` |
| Bottleneck table | `runs/failure_decomposition/a06_13_failure_decomposition_20260622_full01/results/bottleneck_summary.csv` |
| Collapse timing | `runs/failure_decomposition/a06_13_failure_decomposition_20260622_full01/results/raw_center_collapse_timing.csv` |
| Local figure | `figures/full01_raw_center_proxy_retention.png` |

## Bottleneck Table

| Stage | Contract | Metric | Value | Guard | Status |
| --- | --- | --- | ---: | ---: | --- |
| proxy discovery | stable proxy labels exist above random | late-layer residual eval assignment NMI | 0.1923 | 0.0002 | pass with boundary |
| proxy discovery guard | proxy strengthens after early training | step-10 late-layer residual eval assignment NMI | 0.5451 | 0.0002 | pass |
| linear bridge | proxy centers initialize raw-input router above random | raw-center step-0 proxy-route NMI | 0.7449 | 0.0343 | pass |
| training preservation | proxy routing survives through step 10 | raw-center step-10 proxy-route NMI | 0.0131 | 0.0047 | fail first |
| loss guard | failure is not caused by worse LM optimization | step-10 loss delta | 0.0032 | 0.0000 | pass |

## Collapse Timing

| Step | Proxy-route NMI | Fraction of step-0 NMI remaining | Max load | Common margin |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0.7549 | 1.0000 | 0.1812 | 0.1147 |
| 1 | 0.5037 | 0.6672 | 0.2523 | 0.1615 |
| 2 | 0.3271 | 0.4333 | 0.3801 | 0.2504 |
| 3 | 0.1901 | 0.2518 | 0.5839 | 0.3824 |
| 5 | 0.0410 | 0.0543 | 0.9479 | 0.7527 |
| 10 | 0.0131 | 0.0173 | 0.9645 | 0.6995 |
| 20 | 0.0048 | 0.0064 | 0.9832 | 0.4707 |
| 50 | 0.0337 | 0.0447 | 0.7575 | 0.1950 |

## Visualization Results

![Raw-center proxy retention](figures/full01_raw_center_proxy_retention.png)

Purpose: locate when preservation fails.
How to read: 1.0 means the router keeps all step-0 proxy-route NMI; values near 0 mean random-like preservation.
Observed result: retention drops below 10% by step 5.
Take-home: the failure is an early training-feedback problem.
Does not prove: which anti-feedback intervention will work.

## Interpretation

A06_01_04_E01 and A06_01_04_E02 remain useful. The real-data proxy is measurable, and it can initialize a router. The problem is that ordinary LM training has no reason to keep that partition. It rapidly follows loss gradients into common/load concentration, reproducing the A06_01_01 early-collapse pattern.

## Next Decision

Do not run utility binding as the next mainline step. First test whether a preservation mechanism can keep proxy routing through step 10:

- freeze router for the first steps;
- freeze hidden producers or delay router updates;
- lower router learning rate;
- add proxy-route preservation loss;
- add common/load anti-collapse regularization.
