# Detailed: A06_01_05_E01 Warmup Spectral Router Reinitialization

## 0. Purpose

This experiment tests whether failed all-position and expert-spectral router
initialization are failures of step-0 geometry or failures of source choice.
The dataset is the uniform no-position slot bridge, so the question is about
feature distribution across experts, not common/rare frequency imbalance.

## 1. Execution Record

Status: completed.

Run command:

```bash
CUDA_VISIBLE_DEVICES=0,1 torchrun --standalone --nproc_per_node=2 \
  Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E01_warmup_spectral_reinit/scripts/run_a06_25_warmup_spectral_router_reinit.py \
  --run-stage full \
  --run-name a06_25_full_local2gpu_20260703 \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E01_warmup_spectral_reinit
```

Run metadata:

- local devices: two H100 GPUs
- run name: `a06_25_full_local2gpu_20260703`
- seeds: `0--7`
- slot lengths: `1,2,4,8`
- warmup steps: `0,10,40`
- post-reinit checkpoints: `0,10,40,80,160`
- completed cells: `32`
- completed training rows: `3360`
- final checkpoint: `160`

Log:
`logs/local/a06_25_full_local2gpu_20260703.log`

## 2. Data Construction

Each sequence has length `32`. Tokens `0--31` are neutral background tokens.
Feature tokens are `32--35`, corresponding to feature ids `0--3`. Target tokens
are `36--39`, with target token `36+f` for feature `f`.

For each sample:

1. sample feature id \(f \in \{0,1,2,3\}\) uniformly;
2. sample slot start from `2,10,18` with balanced coverage;
3. set a repeated slot of length `slot_len` to token `32+f`;
4. set the target token immediately after the slot to `36+f`;
5. audit the route position at the final token of the repeated slot.

Calibration, warmup, training, and evaluation all use the balanced uniform
feature distribution. The data audit confirms feature fractions `0.25` for all
four features in every audited split and slot cell.

## 3. Model And Training Setup

Model:

- one causal self-attention layer;
- hidden size `64`;
- four attention heads;
- one weighted top-1 MoE layer;
- four experts;
- expert hidden size `128`;
- no explicit position embeddings;
- language-model head for the synthetic target.

Objective:

\[
\mathcal L = \operatorname{CE}(p_\theta(\cdot \mid x_{\le p}), x_{p+1}),
\]

where \(p\) is the route position and \(x_{p+1}=36+f\) is the feature-specific
target token.

Optimization:

- learning rate: `0.002`
- weight decay: `0.0001`
- gradient clip: `1.0`
- warmup train batch size: `256`
- calibration and evaluation samples: `2048`

## 4. Conditions

| Condition | Meaning | Tested rival explanation |
| --- | --- | --- |
| `no_reinit` | Keep the warmed router rows | Warmup alone may explain gains |
| `allpos_centered` | k-means over all token positions after centering | Step-0 all-position geometry may be unformed |
| `route_centered` | k-means over route-position hidden states after centering | Positive control for route-relevant geometry |
| `oracle_centered` | feature-label centers | Upper bound for reachability |
| `expert_svd` | top input singular vector of each expert first layer | Naive expert spectral source |
| `expert_svd_decommon` | expert SVD rows projected away from route common mean | Common alignment as failure source |
| `expert_svd_orth` | QR-orthogonalized expert SVD rows | Row similarity as failure source |

## 5. Primary And Secondary Metrics

Primary metric: feature NMI, the normalized mutual information between feature
id and routed expert on balanced route-position evaluation.

Secondary metrics:

- matched preserve fraction: fraction assigned to the step-0 matched expert;
- margin mean and margin p05: route score gap between matched expert and best
  competitor;
- max load and effective experts: load balance guards;
- target accuracy and loss: task learning guards;
- slot-start NMI: position shortcut guard;
- row pairwise cosine: row similarity diagnostic;
- common alignment: absolute cosine with the route common direction;
- feature-center alignment: best absolute cosine with route feature centers.

## 6. Aggregate Results

### 6.1 Immediate reinitialization

| Condition | Feature NMI | Preserve | Margin p05 | Max load | Slot-start NMI | Target acc. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `w0_allpos_centered` | 0.774 | 0.704 | -3.847 | 0.526 | 0.0020 | 0.028 |
| `w0_expert_svd` | 0.736 | 0.732 | -1.088 | 0.496 | 0.0119 | 0.024 |
| `w0_expert_svd_decommon` | 0.797 | 0.763 | -0.574 | 0.410 | 0.0157 | 0.023 |
| `w0_expert_svd_orth` | 0.667 | 0.629 | -1.738 | 0.526 | 0.0109 | 0.027 |
| `w0_no_reinit` | 0.717 | 0.670 | -0.713 | 0.518 | 0.0166 | 0.027 |
| `w0_oracle_centered` | 1.000 | 1.000 | 11.201 | 0.250 | 0.0010 | 0.006 |
| `w0_route_centered` | 0.995 | 0.992 | 10.473 | 0.258 | 0.0011 | 0.014 |
| `w10_allpos_centered` | 0.809 | 0.715 | -5.585 | 0.508 | 0.0022 | 0.955 |
| `w10_expert_svd` | 0.859 | 0.766 | -3.750 | 0.462 | 0.0050 | 0.991 |
| `w10_expert_svd_decommon` | 0.914 | 0.886 | 0.088 | 0.358 | 0.0055 | 1.000 |
| `w10_expert_svd_orth` | 0.750 | 0.661 | -4.030 | 0.543 | 0.0069 | 0.987 |
| `w10_no_reinit` | 0.816 | 0.695 | -1.978 | 0.523 | 0.0007 | 1.000 |
| `w10_oracle_centered` | 1.000 | 1.000 | 10.480 | 0.250 | 0.0010 | 0.908 |
| `w10_route_centered` | 0.964 | 0.937 | 6.407 | 0.297 | 0.0141 | 0.953 |
| `w40_allpos_centered` | 0.876 | 0.798 | -4.398 | 0.420 | 0.0014 | 0.961 |
| `w40_expert_svd` | 0.879 | 0.804 | -2.809 | 0.428 | 0.0021 | 0.992 |
| `w40_expert_svd_decommon` | 0.943 | 0.923 | 0.514 | 0.327 | 0.0037 | 1.000 |
| `w40_expert_svd_orth` | 0.704 | 0.640 | -5.311 | 0.582 | 0.0054 | 0.988 |
| `w40_no_reinit` | 0.816 | 0.695 | -3.154 | 0.523 | 0.0007 | 1.000 |
| `w40_oracle_centered` | 1.000 | 1.000 | 10.083 | 0.250 | 0.0010 | 0.890 |
| `w40_route_centered` | 0.996 | 0.992 | 9.456 | 0.258 | 0.0011 | 0.915 |

Source: `tables/condition_aggregate_reinit.csv`.

### 6.2 Final post-reinit training

| Condition | Feature NMI | Preserve | Margin p05 | Max load | Slot-start NMI | Target acc. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `w0_allpos_centered` | 0.767 | 0.656 | -4.883 | 0.547 | 0.0006 | 1.000 |
| `w0_expert_svd` | 0.868 | 0.758 | -3.705 | 0.453 | 0.0007 | 1.000 |
| `w0_expert_svd_decommon` | 0.891 | 0.805 | -2.720 | 0.406 | 0.0010 | 1.000 |
| `w0_expert_svd_orth` | 0.786 | 0.579 | -5.730 | 0.532 | 0.0008 | 1.000 |
| `w0_no_reinit` | 0.823 | 0.688 | -3.018 | 0.516 | 0.0007 | 1.000 |
| `w0_oracle_centered` | 1.000 | 1.000 | 2.014 | 0.250 | 0.0010 | 1.000 |
| `w0_route_centered` | 0.996 | 0.992 | 2.852 | 0.258 | 0.0010 | 1.000 |
| `w10_allpos_centered` | 0.839 | 0.695 | -4.923 | 0.500 | 0.0007 | 1.000 |
| `w10_expert_svd` | 0.905 | 0.758 | -2.936 | 0.391 | 0.0009 | 1.000 |
| `w10_expert_svd_decommon` | 0.896 | 0.810 | -0.719 | 0.414 | 0.0016 | 1.000 |
| `w10_expert_svd_orth` | 0.859 | 0.727 | -4.254 | 0.492 | 0.0010 | 1.000 |
| `w10_no_reinit` | 0.816 | 0.695 | -2.773 | 0.523 | 0.0007 | 1.000 |
| `w10_oracle_centered` | 1.000 | 1.000 | 3.680 | 0.250 | 0.0010 | 1.000 |
| `w10_route_centered` | 0.973 | 0.916 | 1.198 | 0.297 | 0.0014 | 1.000 |
| `w40_allpos_centered` | 0.899 | 0.789 | -3.724 | 0.430 | 0.0008 | 1.000 |
| `w40_expert_svd` | 0.919 | 0.784 | -1.246 | 0.391 | 0.0013 | 1.000 |
| `w40_expert_svd_decommon` | 0.913 | 0.825 | 0.225 | 0.386 | 0.0031 | 1.000 |
| `w40_expert_svd_orth` | 0.869 | 0.627 | -4.123 | 0.445 | 0.0021 | 1.000 |
| `w40_no_reinit` | 0.830 | 0.695 | -2.509 | 0.508 | 0.0007 | 1.000 |
| `w40_oracle_centered` | 1.000 | 1.000 | 9.289 | 0.250 | 0.0010 | 1.000 |
| `w40_route_centered` | 0.996 | 0.984 | 8.828 | 0.258 | 0.0010 | 1.000 |

Source: `tables/condition_aggregate_final.csv`.

## 7. Diagnostic Results

Key diagnostic values:

| Condition | Common max cosine | Row max cosine | Feature-center best cosine | Center margin p05 |
| --- | ---: | ---: | ---: | ---: |
| `w10_expert_svd` | 0.417 | 0.301 | 0.583 | -2.510 |
| `w10_expert_svd_decommon` | 0.000 | 0.327 | 0.504 | -0.002 |
| `w10_expert_svd_orth` | 0.404 | 0.000 | 0.567 | -2.937 |
| `w40_expert_svd` | 0.388 | 0.387 | 0.501 | -2.036 |
| `w40_expert_svd_decommon` | 0.000 | 0.381 | 0.419 | 0.248 |
| `w40_expert_svd_orth` | 0.373 | 0.000 | 0.481 | -3.564 |
| `w40_route_centered` | 0.127 | 0.509 | 0.813 | 6.482 |

Source: `tables/spectral_diagnostics_aggregate.csv`.

Interpretation:

- Common-projected SVD supports common alignment as a meaningful failure
  component.
- Orthogonalized SVD weakens the row-similarity explanation because removing
  row similarity does not improve routing.
- Route-position centers have much stronger feature-center alignment and
  margin, so source relevance remains the central bottleneck.

## 8. Visualization Results

### Immediate feature NMI after router reinit

![Immediate feature NMI after router reinit](figures/reinit_feature_nmi_by_method_warmup.png)

Question answered: Does warmup make each source immediately usable as router
rows?

How to read: bars show mean feature NMI over 8 seeds and 4 slot lengths.

Observed result: all-position and expert SVD improve with warmup; route and
oracle controls remain highest.

Allowed conclusion: warmup helps, but it does not remove the route-relevance
gap.

Limitation: feature NMI can be high while margins remain thin or negative.

### Immediate margin p05 after router reinit

![Immediate margin p05 after router reinit](figures/reinit_margin_p05_by_method_warmup.png)

Question answered: Which source gives a positive lower-tail routing basin?

Observed result: route and oracle centers have thick positive margins.
Common-projected SVD becomes slightly positive at warmup 10/40, while raw SVD,
orthogonalized SVD, and all-position clustering stay negative.

Allowed conclusion: margin p05 keeps common-projected SVD as a candidate but
prevents overclaiming spectral readiness.

### Final feature NMI after post-reinit training

![Final feature NMI after post-reinit training](figures/final_feature_nmi_by_method_warmup.png)

Question answered: Does the post-reinit training phase preserve or improve
feature routing?

Observed result: warmup 40 all-position and spectral variants improve final
feature NMI, but route/oracle still dominate.

Limitation: all final conditions learn the target, so this figure should be
read with margin and preserve fraction.

### Feature-center alignment diagnostic

![Source row best feature-center cosine](figures/diagnostic_feature_center_alignment_by_method_warmup.png)

Question answered: Are source rows aligned with feature centers?

Observed result: warmup increases expert SVD feature alignment, but
route-position and oracle rows remain substantially more aligned.

### Common alignment diagnostic

![Expert/source row common alignment](figures/diagnostic_common_alignment_by_method_warmup.png)

Question answered: Do candidate rows align with the common route direction?

Observed result: raw and orthogonalized expert SVD show elevated common
alignment after warmup; common-projected SVD removes this component.

## 9. Rival Explanation Audit

| Rival explanation | Evidence status | Reason |
| --- | --- | --- |
| Step-0 hidden states are too unformed | Partly supported | Warmup improves all-position NMI from 0.774 to 0.876 |
| All-position pool is the wrong population | Supported | Route-position centers remain higher and have much thicker margins |
| Expert SVD rows are too similar | Weakened | Orthogonalized SVD removes row similarity but performs worse |
| Expert SVD rows are common-aligned | Supported as partial explanation | Common projection improves immediate NMI and margin |
| Expert SVD rows are completely feature-unaware | Weakened | Warmup SVD reaches 0.879 immediate NMI; decommon reaches 0.943 |
| Position shortcut explains gains | Weakened | Slot-start NMI stays near zero |
| Target learning explains specialization | Weakened | All final conditions reach target accuracy 1.000 with different routing quality |

## 10. Artifact Map

Anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol:
`protocol.md`

Runner:
`scripts/run_a06_25_warmup_spectral_router_reinit.py`

Tables:

- `tables/data_audit.csv`
- `tables/training_trajectory.csv`
- `tables/spectral_diagnostics.csv`
- `tables/condition_aggregate_reinit.csv`
- `tables/condition_aggregate_final.csv`
- `tables/spectral_diagnostics_aggregate.csv`

Figures:

- `figures/reinit_feature_nmi_by_method_warmup.png`
- `figures/reinit_margin_p05_by_method_warmup.png`
- `figures/final_feature_nmi_by_method_warmup.png`
- `figures/final_margin_p05_by_method_warmup.png`
- `figures/feature_nmi_trajectory_central_methods.png`
- `figures/diagnostic_common_alignment_by_method_warmup.png`
- `figures/diagnostic_row_similarity_by_method_warmup.png`
- `figures/diagnostic_feature_center_alignment_by_method_warmup.png`

Run summary:
`summary.json`

Log:
`logs/local/a06_25_full_local2gpu_20260703.log`

## 11. Claim Boundary

Supported:

- Warmup improves all-position clustering and expert SVD feature awareness.
- Common-projected expert SVD is a better spectral candidate than raw or
  orthogonalized SVD.
- Route-position centers remain the best tested source.
- The result is not explained by slot-start leakage or target failure.

Not supported:

- all-position delayed reinitialization as a finished method;
- raw expert SVD or simple orthogonalized SVD as a finished method;
- real-DCLM transfer;
- semantic expert specialization;
- optimality of the tested common projection.

## 12. Next Decision

The next anchor should connect router specialization to nested learning:

Can a long-horizon or multi-token auxiliary objective create feature-aware
route states early enough that delayed reinitialization can use them without
label-known route-position selection?

Required guards:

- feature NMI;
- margin p05;
- matched preserve fraction;
- slot-start NMI;
- target/language-model loss;
- comparison against route-position and oracle controls.
