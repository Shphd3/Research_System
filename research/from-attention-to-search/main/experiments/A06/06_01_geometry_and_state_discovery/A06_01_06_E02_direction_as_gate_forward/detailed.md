# Detailed: A06_01_06_E02 Direction As Gate-Forward

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

Summary: `summary.md`

## 0. Quick Recap

Purpose: convert the A06_01_06_E01 converged direction into a gate-forward row.

Hypothesis: routing by the stable direction recovers the known feature
partition.

Conclusion: supported on controlled synthetic data.

Evidence: `tables/a08_02_aggregate.csv` and `figures/a08_02_gate_nmi.png`.

## 1. Protocol Compliance Audit

approved conditions match actual conditions: yes.

primary metric exists: yes, feature-route NMI.

central figures/tables exist: yes.

seeds/checkpoints recorded: yes, 8 seeds.

known good/bad/confusing cases reviewed: yes.

success/failure/insufficient criteria applied: yes, with an added warning about
single-random-control spikes.

## 2. Setup

Input direction: the A06_01_06_E01 rank-one converged direction.

Routing rule: route by the sign of \(g^\top h\), with two experts.

Controls: equal-norm random direction, shuffled feature direction, and oracle
feature direction.

## 3. Metrics

Feature-route NMI: normalized mutual information between the route and the
known A sign.

Nuisance NMI: agreement with nuisance route key; low is good.

Max load: largest expert fraction; near 0.5 is balanced for a two-way sign gate.

## 4. Main Results

| Condition | Feature NMI | Nuisance NMI | Max load |
| --- | ---: | ---: | ---: |
| direction_gate | `1.0000` | `0.0002` | `0.5097` |
| random_equal_norm_gate | `0.1741` | `0.0004` | `0.5177` |
| shuffled_direction_gate | `0.0001` | `0.0003` | `0.5057` |
| oracle_feature_gate | `1.0000` | `0.0002` | `0.5097` |

Interpretation: the converged direction is route-readable. The random-control
mean is low, but one seed reached NMI `0.5952`, so future controls should sample
multiple random rows per seed.

## 5. Visualization Results

### Gate NMI

![Gate NMI](figures/a08_02_gate_nmi.png)

Purpose: compare route identity across direction and control gates.

Setup: held-out synthetic examples, no post-gate training.

How to read: higher NMI means stronger agreement with the intended feature
route.

Observed result: direction gate and oracle are both near perfect; shuffled gate
is near zero.

Take-home: the A06_01_06_E01 converged direction can become a gate-forward axis.

Remaining uncertainty: random controls need a stronger distributional audit in
later protocols.

## 6. Failure Decomposition

Falsified physical prior: no.

Falsified mathematical model: no.

Falsified operationalization / proxy: no on this surface.

Falsified implementation: no.

Falsified metric: no, but single random controls can understate false-positive
risk.

## 7. Claim Boundary

Can claim: direction-derived routing recovers a known synthetic feature
partition.

Cannot claim: training preservation, real-data routing, or expert utility.

## 8. Links And Artifact Map

runner:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a08_singular_direction_preservation.py`

raw result dir:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a08_singular_direction_preservation/a08_singular_preservation_full_20260628_2`

tables: `tables/a08_02_aggregate.csv`, `tables/a08_02_route_metrics.csv`,
`tables/decision_metrics.json`.

figure: `figures/a08_02_gate_nmi.png`.

job id: local CUDA run, no ACP job id.
