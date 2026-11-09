# Detailed: A06_02_01_E05 Margin-Basin Robust Initialization

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`

## Executive Judgment

The experiment supports the margin-basin hypothesis. In the controlled
no-position bridge, exact pseudo-center rows are not required. The original
feature-to-expert routing region survives substantial random-direction row
perturbation as long as the minimum initial margin remains positive.

## Protocol Compliance

The run used the approved setup:

- C0-C3;
- four seeds;
- oracle rho 0 guard;
- pseudo rho sweep: `0, 0.05, 0.1, 0.2, 0.35, 0.5, 0.7, 1.0`;
- step-0 and final measurements.

No extra conditions were added after seeing results.

## Data / Model / Training

Data:

- sequence length 32;
- feature slot length 4;
- route on the last slot token;
- no B token;
- no learned absolute positional embedding;
- feature, nuisance, and slot start uniformly sampled.

Model:

- one-layer Transformer;
- top-1 selected-gate sparse MoE;
- 4 experts;
- `d_model = 128`.

Training:

- slot-end target cross-entropy;
- 1600 steps;
- AdamW;
- base learning rate `0.0008`.

## Perturbation

For pseudo-center row \(c_e\) and random row \(r_e\):

\[
w_e(\rho)=\alpha\cdot
\mathrm{normalize}\left((1-\rho)\hat c_e+\rho \hat r_e\right).
\]

The original feature-to-expert match is defined before perturbation from the
unperturbed center initialization. Preserve fraction always asks whether a
feature remains in that original matched expert region.

## Complete Result Table

| Center | Rho | Stage | Preserve fraction | Min margin | Feature NMI | Max load |
|---|---:|---|---:|---:|---:|---:|
| oracle | 0.00 | step0 | 1.000 | 6.004 | 1.000 | 0.250 |
| oracle | 0.00 | final | 1.000 | 3.719 | 1.000 | 0.250 |
| pseudo | 0.00 | step0 | 1.000 | 6.004 | 1.000 | 0.250 |
| pseudo | 0.00 | final | 1.000 | 3.765 | 1.000 | 0.250 |
| pseudo | 0.05 | step0 | 1.000 | 5.977 | 1.000 | 0.250 |
| pseudo | 0.05 | final | 1.000 | 3.730 | 1.000 | 0.250 |
| pseudo | 0.10 | step0 | 1.000 | 5.938 | 1.000 | 0.250 |
| pseudo | 0.10 | final | 1.000 | 3.702 | 1.000 | 0.250 |
| pseudo | 0.20 | step0 | 1.000 | 5.795 | 1.000 | 0.250 |
| pseudo | 0.20 | final | 1.000 | 3.680 | 1.000 | 0.250 |
| pseudo | 0.35 | step0 | 1.000 | 4.953 | 1.000 | 0.250 |
| pseudo | 0.35 | final | 1.000 | 3.289 | 1.000 | 0.250 |
| pseudo | 0.50 | step0 | 1.000 | 3.773 | 1.000 | 0.250 |
| pseudo | 0.50 | final | 1.000 | 2.733 | 1.000 | 0.250 |
| pseudo | 0.70 | step0 | 1.000 | 1.531 | 1.000 | 0.250 |
| pseudo | 0.70 | final | 1.000 | 2.142 | 1.000 | 0.250 |
| pseudo | 1.00 | step0 | 0.222 | -1.337 | 0.729 | 0.528 |
| pseudo | 1.00 | final | 0.219 | -4.205 | 0.793 | 0.547 |

## Visualization Results

### Preserve fraction versus perturbation

![Preserve fraction versus rho](figures/preserve_fraction_vs_rho.png)

**Purpose:** test whether the matched feature-to-expert region survives row
perturbation.

**Observed result:** preservation remains perfect through `rho = 0.7` and
collapses at `rho = 1.0`.

**Take-home:** the successful center initialization is a basin, not a point.

### Margin versus perturbation

![Margin versus rho](figures/margin_vs_rho.png)

**Purpose:** test whether margin tracks the basin boundary.

**Observed result:** margin remains positive through `rho = 0.7` and becomes
negative at `rho = 1.0`.

**Take-home:** positive margin is the operational basin coordinate.

### Feature NMI versus perturbation

![Feature NMI versus rho](figures/feature_nmi_vs_rho.png)

**Purpose:** show the standard cluster-alignment metric alongside the
identity-sensitive preserve fraction.

**Observed result:** NMI remains 1.0 through `rho = 0.7` and drops at `rho =
1.0`.

**Take-home:** NMI agrees here, but preserve fraction remains the stricter
metric for this mechanism.

### Preserve fraction versus margin

![Preserve fraction versus margin](figures/preserve_fraction_vs_margin_scatter.png)

**Purpose:** test whether final preservation is organized by margin.

**Observed result:** positive-margin points preserve; negative-margin points
fail.

**Take-home:** margin is more method-relevant than exact center distance.

## Artifact Map

Code:
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_17_05_margin_basin_robust_initialization.py`

Raw results:
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_17_05_margin_basin_robust_initialization/a06_17_05_margin_basin_full_20260629_1/`

Raw figures:
`../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/figures/a06_17_05_margin_basin_robust_initialization/a06_17_05_margin_basin_full_20260629_1/`

Curated tables:

- `tables/basin_metric_aggregate.csv`
- `tables/basin_metrics.csv`
- `tables/basin_feature_metrics.csv`
- `tables/discovery_summary.csv`

Curated figures:

- `figures/preserve_fraction_vs_rho.png`
- `figures/margin_vs_rho.png`
- `figures/feature_nmi_vs_rho.png`
- `figures/preserve_fraction_vs_margin_scatter.png`

## Claim Boundary

Can claim: controlled route-position center initialization has a wide
positive-margin basin. Exact center rows are not required in this setting.

Cannot claim: real-DCLM semantic correctness, utility, or that the same basin
can be detected without labels in real data.

## Next Decision

Build a label-free margin acceptance gate. The method-facing idea is to
generate candidate centers, compute pre-training margin-like guards, and only
train candidates whose margins indicate they are inside a preservation basin.
