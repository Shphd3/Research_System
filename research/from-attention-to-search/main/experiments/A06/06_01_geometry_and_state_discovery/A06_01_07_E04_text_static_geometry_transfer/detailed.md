# Detailed: A06_01_07_E04_text_static_geometry_transfer

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`
Protocol: `protocol.md`
Summary: `summary.md`

## 0. Quick Recap

Purpose:
Evaluate static expert-geometry scores on non-uniform text-like hidden-state distributions.

Hypothesis:
Empirical-centered or calibrated weighted low-rank M4 should be the best bridge from uniform-sphere geometry to text-facing hidden states.

Experiment logic:
Generate controlled semi-real hidden states with common direction, corpus slice, position, frequency, syntax, and utility factors. Compare full centered M4, calibrated M4, weighted top-r, and prototype baselines under raw, centered, common-removed, and whitened preprocessing.

Conclusion:
The semi-real full run supports empirical-centered/calibrated M4 as the static target and weighted top-r around r=32 as a practical proxy. Prototype baselines balance load but do not preserve the full matrix-response rule.

Evidence:
Mean-centered quantile-calibrated M4 has load error 0.0029, mean margin 3.1910, and agreement 0.9967 with full centered M4. Mean-centered weighted top-r=32 has load error 0.0048, mean margin 3.1869, and agreement 0.9832. M1/M2 prototype agreement is only 0.4977 / 0.5460 with much smaller margin.

## 1. Anchor Link And Decision Point

Anchor decision:
Which static expert-geometry score should bridge high-dimensional uniform geometry to text-facing hidden states?

Decision after this experiment:
Keep empirical-centered or calibrated weighted low-rank M4 as the leading static initialization target. The next required run is true frozen-transformer hidden states.

## 2. Protocol Compliance Audit

approved conditions match actual conditions:
Partially. The protocol allowed real or semi-real hidden states. This run uses semi-real synthetic hidden states, not a frozen transformer.

primary metric exists:
Yes. `load_error`, `mean_margin`, `low_margin_fraction`, `agreement_with_full_centered_M4`, `common_sensitivity`, and `utility_match` are recorded.

central figures/tables exist:
Yes. Central tables and figures are listed in the artifact map.

seeds/checkpoints recorded:
No training checkpoints. Synthetic generation uses fixed deterministic seeds in the runner.

known good/bad/confusing cases reviewed:
Yes. Full centered M4 is the teacher; prototypes are confusing load-balanced baselines; common removal tests common-direction sensitivity.

success/failure/insufficient-evidence criteria applied:
Yes. The result supports full/calibrated M4 and weighted top-r, weakens prototypes as core methods, and remains insufficient for real transformer transfer.

## 3. Setup

Code:
`run_text_static_expert_geometry_transfer.py`

Command:

```bash
python run_text_static_expert_geometry_transfer.py
```

Hidden states:

- dimension: 128;
- calibration: 12,000 per layer-position condition;
- evaluation: 24,000 per layer-position condition;
- layers: early, middle, late;
- position modes: controlled, natural.

Synthetic factors:

- common direction;
- corpus slice;
- position;
- token frequency;
- syntax;
- latent utility label.

Preprocessing:

- raw;
- mean-centered;
- common-removed;
- diagonal-whitened.

Methods:

- full empirical-centered M4;
- quantile-calibrated M4;
- weighted top-r for r=1,2,4,8,16,32,64;
- M1 signed prototype;
- M2 unsigned prototype.

## 4. Metrics And Decision Rules

Primary metrics:

- `load_error`;
- `mean_margin`;
- `low_margin_fraction`;
- `agreement_with_full_centered_M4`;
- `route_change_after_common_removal`;
- `utility_match`.

Diagnostic label metrics:

- `corpus_nmi`;
- `position_nmi`;
- `frequency_nmi`;
- `syntax_nmi`.

Decision rules:

- A method is useful if it controls load, preserves margin, and agrees with full centered M4.
- Prototype baselines are weakened if they balance load but have low agreement or low margin.
- Common-sensitive methods are weakened if route changes sharply after common removal.

## 5. Main Results

### Aggregate Result

| Method / preprocess | Load error | Mean margin | Low-margin fraction | Agreement | Utility match |
| --- | ---: | ---: | ---: | ---: | ---: |
| full empirical-centered M4 / mean-centered | 0.0046 | 3.1912 | 0.0000 | 1.0000 | 0.5001 |
| quantile-calibrated M4 / mean-centered | 0.0029 | 3.1910 | 0.0000 | 0.9967 | 0.5004 |
| weighted top-r=32 / mean-centered | 0.0048 | 3.1869 | 0.0000 | 0.9832 | 0.5009 |
| weighted top-r=16 / mean-centered | 0.0112 | 3.0076 | 0.0000 | 0.8882 | 0.5005 |
| M2 unsigned prototype / mean-centered | 0.0113 | 0.0676 | 0.0051 | 0.5460 | 0.4993 |
| M1 signed prototype / mean-centered | 0.0030 | 0.0641 | 0.0011 | 0.4977 | 0.5027 |

Interpretation:
Prototype baselines can balance load, but their margin and agreement with the expert-matrix rule are weak.

### Common Sensitivity

| Method | Route change after common removal |
| --- | ---: |
| weighted top-r=16 | 0.0820 |
| weighted top-r=32 | 0.0853 |
| quantile-calibrated M4 | 0.0854 |
| full empirical-centered M4 | 0.0855 |
| M2 unsigned prototype | 0.1214 |

Interpretation:
Prototype routing is more sensitive to common-direction control than the matrix-response methods.

## 6. Visualization Results

### Load-Margin By Method

![Load-margin by method](figures/load_margin_by_method.png)

Purpose:
Show load and margin jointly.

Setup:
All layer-position conditions aggregated by method and preprocessing.

How to read:
Lower x is better load balance; higher y is stronger score margin.

Observed result:
Full/calibrated M4 and weighted top-r=32/64 have low load error and large margin. Prototype baselines have much smaller margin.

Take-home:
Balanced load alone is insufficient.

Remaining uncertainty:
This is synthetic text-like data, not real transformer activations.

### Agreement Versus Rank

![Agreement versus rank](figures/agreement_vs_rank.png)

Purpose:
Measure how weighted top-r approaches full centered M4.

Setup:
Middle-layer condition under mean-centered and common-removed preprocessing.

How to read:
Higher agreement is better.

Observed result:
Agreement rises with rank and is high by r=32.

Take-home:
Weighted top-r is plausible, but rank choice matters.

Remaining uncertainty:
This does not test a trainable router.

### Common-Direction Sensitivity

![Common-direction sensitivity](figures/common_control_effect.png)

Purpose:
Test route changes under common-direction removal.

Setup:
Compare routes before and after common removal.

How to read:
Lower bar means more stable to common control.

Observed result:
M2 changes more than matrix-response methods.

Take-home:
Prototype baselines are less stable under common control.

Remaining uncertainty:
The generated common direction is controlled and may not match a real transformer's common component.

## 7. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| Hidden-state generation | fixed layer/position semi-real states | Passed with boundary | synthetic, not frozen transformer | Rules out only uniform-sphere evidence. |
| Full M4 teacher | full centered M4 has strong margin and low load error | Passed | n/a | Establishes static target. |
| Calibration | calibrated M4 load error 0.0029 under mean-centered states | Passed | n/a | Shows load can be controlled without margin collapse. |
| Low-rank proxy | top-r=32 agreement 0.9832 | Passed | needs rank | Rules out tiny-rank assumption. |
| Prototype baselines | agreement 0.4977 / 0.5460 | Failed as core metric | weak matrix agreement | Rules out load-only prototype success. |
| Common sensitivity | M2 route-change 0.1214 vs ~0.085 for M4 methods | Passed | prototype line sensitivity | Supports common-control caution. |

Falsified physical prior:
None.

Falsified mathematical model:
Prototype-as-core is weakened.

Falsified operationalization / proxy:
Load-balanced prototype routing is not a sufficient bridge to text-facing expert geometry.

Falsified implementation:
None.

Falsified metric:
Load-only judgment is insufficient.

Remaining rival explanations:
Real transformer hidden states may have different common components, covariance, and utility relation.

## 8. Full Experiment Record

Run command:

```bash
python run_text_static_expert_geometry_transfer.py
```

Rows:

- `text_static_metric_per_condition.csv`: per layer-position-preprocess-method rows.
- `text_static_metric_summary.csv`: aggregate method summary.
- `common_sensitivity.csv`: route-change after common removal.
- `utility_match.csv`: utility diagnostic.
- `layer_position_breakdown.csv`: position-level load and margin.

## 9. Interpretation

Observation:
Full/calibrated M4 and weighted top-r=32 have low load error, strong margin, and high agreement.

Interpretation:
The high-dimensional matrix-response target survives this non-uniform text-like distribution when empirical centering/calibration is used.

Claim:
Empirical-centered or calibrated weighted low-rank M4 is the leading static text-facing bridge.

Boundary:
The hidden states are synthetic.

Observation:
M1/M2 prototypes can balance load but have low agreement and small margin.

Interpretation:
Prototype load balance is not enough to represent expert matrix geometry.

Claim:
Prototype baselines remain controls, not core methods.

Boundary:
A better sign convention might improve a future prototype variant.

## 10. Claim Boundary

Can claim:

- A06_01_07_E04 semi-real full run supports empirical-centered/calibrated M4.
- Weighted top-r around r=32 approximates full centered M4 well in this setting.
- Prototype baselines are weak despite load balance.

Cannot claim:

- Real frozen-transformer hidden states are solved.
- Text labels prove semantic specialization.
- Synthetic utility match proves task utility.
- A trainable router can learn the static score.

## 11. Next Decision

Run the true frozen-transformer hidden-state version when activations are available. Keep empirical-centered/calibrated weighted low-rank M4 as the leading router-initialization target.

## 12. Links And Artifact Map

anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

protocol:
`protocol.md`

summary:
`summary.md`

code workspace:
`Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_07_E04_text_static_geometry_transfer/`

runner:
`run_text_static_expert_geometry_transfer.py`

figures:
`figures/`

tables:
`tables/text_static_metric_summary.csv`, `tables/layer_position_breakdown.csv`, `tables/common_sensitivity.csv`, `tables/utility_match.csv`

logs / checkpoints:
No training checkpoints.

repro command:
`python run_text_static_expert_geometry_transfer.py`
