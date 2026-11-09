# A06_03_04_E02 Utility-Certified Audition Stop: Detailed Record

## Decision

The mean utility certificate fails its safety contract despite strong final
performance and compute savings. H4 is supported: population-mean utility is
not identifiable as a tail-safe phase-switch certificate.

## Validity Audit

| Guard | Result | Status |
| --- | ---: | --- |
| completed seeds | 32 | pass |
| specialist utility gap | `8.894682` | pass |
| generalist absolute gap | `0.004236` | pass |
| minimum rank accuracy | `1.0` | pass |
| minimum adjacent gap p05 | `0.473113` | pass |
| initial load spread | `0` | pass |
| fixed600 correction reproduction | `128/128` | pass |
| fixed600 retention | `128/128` | pass |
| generalist false trigger | `0/32` seeds | pass |
| ACP job | `pt-r30pqxpg`, `SUCCEEDED` | pass |

## Certificate And Controls

For routed incumbent \(e\) and auditioned challenger \(c\),

\[
U_{e,c}=\operatorname{EMA}_{0.9}
[\ell(E_c(h))-ell(E_e(h))].
\]

The all-position certificate requires every directed pair's EMA above zero for
nine assignment-stable updates. The task-oracle certificate differs only by
using task-dependent positions. Score-only requires every incumbent's average
top1-runner-up gap above 1.0. Oracle route stopping requires all four true task
routes correct for five updates.

## Complete Results

| Condition | Correction | Retention | Premature | Trigger | Stop step | Saving | Final margin | Regret |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fixed600 | 1.0000 | 1.0000 | 0 | 0 | 600.0 | 0 | 1.6144 | 0.2870 |
| oracle route | 1.0000 | 1.0000 | 0 | 1 | 242.5 | 0.5958 | 1.9934 | 0.2510 |
| score only | 1.0000 | 1.0000 | 0 | 0 | 600.0 | 0 | 1.6144 | 0.2870 |
| utility all | 0.9922 | 1.0000 | 0.1875 | 1 | 220.5 | 0.6325 | 2.0044 | 0.2472 |
| utility task oracle | 0.9922 | 1.0000 | 0.1719 | 1 | 223.0 | 0.6283 | 2.0044 | 0.2475 |
| generalist utility all | 0 | n/a | 0 | 0 | 600.0 | 0 | -2.2479 | 0.8545 |

The utility rule stops about 22 updates before the global oracle median. The
premature statistic is cell-level: a global stop can occur while one or more
task cells have not yet sustained correction. Most such cells finish under
top-1, but one of 128 does not. The preregistered safety rule therefore correctly
rejects the method despite its 99.22% final correction.

## Visualization Results

### Reliability Versus Compute

![Stopping tradeoff](figures/stopping_rule_tradeoff.png)

- Question: can a label-free stop save audition compute without unsafe stops?
- Result: utility saves over 62% but premature stopping exceeds 17%.
- Boundary: final correction cannot substitute for the stop-time safety metric.

### Aggregate Dynamics

![Margin trajectories](figures/certified_stop_margin_trajectories.png)

- Question: does switching to top-1 destroy the aggregate corrected state?
- Result: utility branches retain and strengthen median margin.
- Boundary: the median conceals minority routed populations, exactly the failure
  identified by the premature-stop metric.

## Mechanism Update

The mean certificate tests

\[
\mathbb E[D_{e,c}]>0,
\qquad D_{e,c}=\ell(E_c(h))-ell(E_e(h)).
\]

This does not imply that every subpopulation prefers the incumbent. A mixture
can satisfy

\[
\mathbb E[D_{e,c}]>0
\quad\text{while}\quad
Q_q(D_{e,c})<0
\]

for a lower quantile \(Q_q\). The observed failure therefore localizes the next
object: utility distribution tails within each routed incumbent/challenger
pair. Task masking does not fix the failure, so the unresolved heterogeneity is
not simply task versus background position.

## Claim Boundary

Supported: mean pairwise utility predicts an efficient phase switch and avoids
generalist false triggers, but violates the tail safety criterion.

Not supported: a deployable safe stop, a particular quantile threshold,
joint-training stability, pretrained LLM transfer, or systems efficiency.

## Artifact Map

- Anchor: `main/problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md`
- Protocol: `main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_04_E02_mean_utility_stop/protocol.md`
- Runner: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_44_utility_certified_audition_stop.py`
- Config: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_44_utility_certified_audition_stop.json`
- Raw result: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_44_utility_certified_audition_stop/a06_44_full_4gpu_20260711_01/`
- Curated figures: `figures/stopping_rule_tradeoff.png`, `figures/certified_stop_margin_trajectories.png`
- Curated table: `tables/condition_summary.csv`
- Job: `pt-r30pqxpg`
