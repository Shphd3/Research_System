# Metrics Contract: 0531_auto_route_function_binding

## Primary Metric

`BindingPassRate` is the primary decision metric.

A seed-condition pass requires:

```text
route_feature_nmi >= 0.85
assignment_utility >= 0.90
forced_loss_diag_margin >= 0.10 nats or >= 10% relative margin
final_ce <= 1.05 * best_baseline_ce
load_max_fraction <= 0.80 unless oracle says collapse is correct
checkpoint_binding_drop <= 0.10
inference_route_consistency >= 0.85
```

Why this is primary:

```text
It operationalizes feature-level expert specialization as alignment + utility + stability, not a single proxy.
```

False positives prevented:

```text
- diagonal route heatmap without expert utility;
- low CE with route collapse;
- high assignment-utility because one utility-best path handles everything;
- early semantic routing that washes out;
- training-set memorization that fails held-out B.
```

## Supporting Metrics

### `route_feature_nmi`

Question:

```text
Does route assignment align with target-deciding feature / slot?
```

Cannot prove:

```text
That selected expert is useful.
```

### `assignment_utility`

Question:

```text
Does selected route match utility-best route according to forced expert loss?
```

Cannot prove:

```text
Feature-level specialization; can be high under utility collapse.
```

### `forced_loss_diag_margin`

Question:

```text
Does each feature have a specific expert/path whose forced CE is better than alternatives?
```

Cannot prove:

```text
The trained router actually selects that expert.
```

### `factor_logit_R2`

Question:

```text
Which known factor explains router logits/routes?
```

Cannot prove:

```text
Causality unless paired with factor-swap intervention.
```

### `inference_route_consistency`

Question:

```text
Are routes stable after training under held-out/noise/shift?
```

Cannot prove:

```text
Real-corpus transfer.
```

## Minimal Report Table

| Condition | Model | CE | Route-Feature NMI | Route-B NMI | Assign-Utility | Forced Diag Margin | Load Max | Stability Drop | Inference Consistency | BindingPass | Interpretation |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| T2 | M0_flat_top1 | | | | | | | | | | |
| T2 | M1_common_flat | | | | | | | | | | |
| T2 | C1_residual_linear | | | | | | | | | | |
| T2 | C2_utility_binding | | | | | | | | | | |
| T2 | C5_residual_plus_binding | | | | | | | | | | |
