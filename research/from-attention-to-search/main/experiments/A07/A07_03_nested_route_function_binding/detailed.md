# Detailed: A07_03 Nested Route-Function Binding

Primary anchor:
`../../../problem_anchors/07_features_overlap/07_03_route_function_binding_anchor.md`

Protocol: `protocol.md`

Summary: `summary.md`

## 0. Quick Recap

Purpose: test whether the route-function binding diagnostic can see causal
expert utility on a controlled nested positive control.

Hypothesis: oracle nested routes should show selective fixed-route ablation
damage; random load-matched routes should not.

Experiment logic: train fixed-route MoE conditions and evaluate forced expert
loss plus fixed-route ablation.

Conclusion: positive-control diagnostic passed, but real utility remains
parked.

Evidence: `tables/a07_03_aggregate.csv`,
`figures/a07_03_route_binding.png`.

## 1. Anchor Link And Decision Point

This validates the diagnostic form. It does not bypass the A06 preservation
bottleneck.

## 2. Protocol Compliance Audit

approved conditions match actual conditions: yes.

primary metric exists: yes, fixed-route ablation selectivity.

central figures/tables exist: yes.

seeds/checkpoints recorded: yes, 8 seeds.

known good/bad/confusing cases reviewed: yes, oracle and random routes.

success/failure/insufficient-evidence criteria applied: yes.

## 3. Setup

Code workspace:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

Runner:
`active/synthetic_data_understanding/scripts/run_a07_nested_singular_interference.py`

Config:
`active/synthetic_data_understanding/configs/a07_nested_singular_interference.json`

Run name: `a07_nested_full_20260628_2`

Curated dir:
`/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A07/A07_03_nested_route_function_binding`

Job id: local CUDA run, no ACP job.

## 4. Metrics And Decision Rules

Primary metric:

\[
A_\ell=CE_{\ell}^{-\mathrm{routed}}-\frac{1}{E-1}\sum_{e\ne \mathrm{routed}}CE_{\ell}^{-e}.
\]

Pass: oracle route has selective damage and random load-matched route does not.

## 5. Main Results

| Condition | Ablation selectivity | Route utility | Selected-best rate | Route concentration | Loss | Acc |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| oracle nested route | `0.5699` | `0.1746` | `0.7500` | `1.0000` | `0.1232` | `0.9714` |
| random load-matched route | `0.0107` | `-0.0024` | `0.2188` | `0.2635` | `0.3177` | `0.9053` |

Interpretation: the diagnostic distinguishes route-function binding from
load-matched random routing.

## 6. Visualization Results

### Nested Route Binding

![Nested route binding](figures/a07_03_route_binding.png)

Purpose: show whether route-function binding is visible under oracle route and
absent under random load-matched route.

Setup: aggregate 8 seeds for fixed-route MoE conditions.

How to read: oracle should have high selectivity and utility; random should be
near zero.

Observed result: oracle positive control is clearly above random.

Take-home: the diagnostic is usable once a preserved partition exists.

Remaining uncertainty: learned route preservation is not tested here.

What this figure does not prove: real-DCLM expert utility or learned top-1
specialization.

Anchor update implication: keep A07_03 conditional.

## 7. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| Oracle route | concentration `1.0` | passed | none | diffuse-route issue absent in positive control |
| Selective ablation | selectivity `0.5699` | passed | none | flat-utility rival weakened |
| Random route guard | selectivity `0.0107` | passed | none | load-only rival weakened |

Falsified physical prior: none.

Falsified mathematical model: none for diagnostic use.

Falsified operationalization / proxy: none.

Falsified implementation: none found.

Falsified metric: none.

Remaining rival explanations: oracle route is hand-coded; learned preservation
is still untested.

## 8. Full Experiment Record

Seeds: `20260628-20260635`.

Conditions: oracle nested route MoE and random load-matched MoE.

Training: `560` steps, batch size `256`, learning rate `0.006`.

Expert count: `4`.

## 9. Interpretation

This diagnostic is useful but downstream. It should be used only after A06
preserves a route partition or after a controlled method creates a stable
partition. Otherwise it risks turning oracle positive-control evidence into an
unsupported learned-specialization claim.

## 10. Claim Boundary

Can claim: route-function binding diagnostic works on controlled positive
control.

Cannot claim: learned expert specialization, real-DCLM utility, or semantic
experts.

## 11. Next Decision

Return to A06 preservation before applying this diagnostic to a real or
learned route partition.

## 12. Links And Artifact Map

anchor:
`../../../problem_anchors/07_features_overlap/07_03_route_function_binding_anchor.md`

protocol: `protocol.md`

summary: `summary.md`

code workspace:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

runner:
`active/synthetic_data_understanding/scripts/run_a07_nested_singular_interference.py`

config:
`active/synthetic_data_understanding/configs/a07_nested_singular_interference.json`

data / manifest:
generated in-memory from config.

result dir:
`active/synthetic_data_understanding/results/a07_nested_singular_interference/a07_nested_full_20260628_2`

figure dir: `figures/`

key tables:
`tables/a07_03_aggregate.csv`, `tables/a07_03_summary.csv`

logs / checkpoints: no persistent checkpoints.

repro command: see A07_01 detailed setup.

job id: local run.
