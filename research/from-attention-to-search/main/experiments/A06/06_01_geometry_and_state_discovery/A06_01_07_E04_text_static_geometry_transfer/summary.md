# Summary: A06_01_07_E04_text_static_geometry_transfer

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`
Protocol: `protocol.md`

## Purpose

This experiment tests which static expert-geometry score is the best bridge from uniform synthetic features to non-uniform text-like hidden-state distributions.

This is a semi-real synthetic hidden-state full run. It does not use a frozen transformer. The hidden states are controlled to include common direction, corpus slice, position, token-frequency, syntax, and latent utility factors.

## Exact Setup

Hidden dimension: 128.

Splits:

- calibration: 12,000 hidden states per layer-position condition;
- evaluation: 24,000 hidden states per layer-position condition.

Conditions:

- layers: early, middle, late;
- position modes: controlled, natural.

Preprocessing variants:

- raw;
- mean-centered;
- common-removed;
- diagonal-whitened.

Compared methods:

- full empirical-centered M4;
- quantile-calibrated M4;
- weighted top-r M4 proxy for r in 1,2,4,8,16,32,64;
- M1 signed prototype;
- M2 unsigned prototype.

## Primary Metric

Primary metric: load error read together with mean margin, agreement with full empirical-centered M4, and common-direction sensitivity.

Load error alone is not enough, because prototype baselines can split load while failing to match the matrix-response rule. Agreement with full centered M4 decides whether a scalable proxy preserves the intended expert-geometry target.

## Result

Full empirical-centered M4 and quantile-calibrated M4 are the strongest static text-facing scores in this controlled hidden-state run. Weighted top-r becomes usable around r=32. Prototype baselines are weak despite good load.

Aggregate highlights:

| Method / preprocess | Load error | Mean margin | Agreement with full centered M4 | Utility match |
| --- | ---: | ---: | ---: | ---: |
| full empirical-centered M4 / mean-centered | 0.0046 | 3.1912 | 1.0000 | 0.5001 |
| quantile-calibrated M4 / mean-centered | 0.0029 | 3.1910 | 0.9967 | 0.5004 |
| weighted top-r=32 / mean-centered | 0.0048 | 3.1869 | 0.9832 | 0.5009 |
| weighted top-r=16 / mean-centered | 0.0112 | 3.0076 | 0.8882 | 0.5005 |
| M2 unsigned prototype / mean-centered | 0.0113 | 0.0676 | 0.5460 | 0.4993 |
| M1 signed prototype / mean-centered | 0.0030 | 0.0641 | 0.4977 | 0.5027 |

Common-direction sensitivity:

| Method | Route change after common removal |
| --- | ---: |
| weighted top-r=16 | 0.0820 |
| weighted top-r=32 | 0.0853 |
| quantile-calibrated M4 | 0.0854 |
| full empirical-centered M4 | 0.0855 |
| M2 unsigned prototype | 0.1214 |

Interpretation:
Weighted top-r=32 nearly preserves full centered-M4 decisions while remaining low-rank. Prototype baselines are load-balanced but do not preserve the matrix-response target.

## Key Figures

### Figure: Load-Margin By Method

![Load-margin by method](figures/load_margin_by_method.png)

What this tests:
Whether methods control load while preserving a clear score advantage.

How to read:
Lower x is better load balance; higher y is stronger score margin.

Observed result:
Full centered/calibrated M4 and weighted top-r=32/64 occupy the strong-margin, low-load-error region. Prototype baselines have low margin.

Take-home:
Load-balanced prototypes are not enough.

What this does not prove:
It does not prove real task utility.

### Figure: Agreement Versus Rank

![Agreement versus rank](figures/agreement_vs_rank.png)

What this tests:
Whether weighted top-r approaches full empirical-centered M4.

How to read:
Higher agreement means the proxy matches full centered-M4 assignments more often.

Observed result:
Agreement rises sharply with rank and is high by r=32.

Take-home:
Weighted top-r is a practical approximation family, but rank selection matters.

What this does not prove:
It does not prove a trainable linear router can implement the same decisions.

### Figure: Common-Direction Sensitivity

![Common-direction sensitivity](figures/common_control_effect.png)

What this tests:
How much routes change when the top common direction is removed.

How to read:
Lower route-change rate means less sensitivity to common-direction preprocessing.

Observed result:
M2 prototype is more sensitive than full/low-rank M4 methods.

Take-home:
Matrix-response methods are more stable under common control in this synthetic text-like setting.

What this does not prove:
It does not cover real transformer hidden states.

## Claim Boundary

Can claim:

- In controlled text-like hidden states, empirical-centered/calibrated M4 remains the best static expert-geometry target.
- Weighted top-r around r=32 can approximate full centered M4 well in this setting.
- Prototype baselines can balance load but have weak margin and poor agreement with full M4.

Cannot claim:

- Real transformer hidden states behave the same way.
- Text labels prove semantic specialization.
- Utility match was established; the synthetic utility label is only a control factor.
- A trainable router will learn this score.

## Next Decision

Run a true frozen-transformer hidden-state version of A06_01_07_E04 when model activations are available. Keep empirical-centered or calibrated weighted low-rank M4 as the leading static initialization target.
