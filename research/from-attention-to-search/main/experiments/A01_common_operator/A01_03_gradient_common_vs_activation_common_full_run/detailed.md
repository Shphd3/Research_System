# Detailed Record: A01_03 Gradient Common Versus Activation Common Full Run

## 1. Result

The run supports the anchor hypothesis: optimization-relevant common is better
explained by cross-group gradient covariance than activation covariance in
controlled activation-gradient mismatch settings.

Primary metric:

```text
gradient_overlap_reduction_advantage =
gradient_overlap_reduction(P_grad) - gradient_overlap_reduction(P_act)
```

Protocol pass rule:

```text
at least 3 / 4 mismatch regimes with positive mean advantage
and seed win rate >= 0.8
```

Observed:

```text
4 / 4 mismatch regimes passed
all mismatch seed win rates = 1.0
```

## 2. Protocol Alignment

Primary anchor:
`Projects/from-attention-to-search/main/problem_anchors/01_common_operator_mechanism/01_03_gradient_common_vs_activation_common_anchor.md`

Protocol:
`Projects/from-attention-to-search/main/experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/protocol.md`

Approval status: user requested execution on 2026-06-29.

Experiment role: root-cause / estimator audit.

Claim boundary: controlled activation-gradient mismatch only.

## 3. Reproduction

Working directory:

```bash
/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run
```

Command:

```bash
python scripts/run_gradient_vs_activation_full_run.py --outdir .
```

Runtime: local CPU run; no cluster job id.

## 4. Data Generation

Hidden states are generated as:

\[
h = s_g A_g z_g + s_f A_f z_f + s_u B_g z_u + s_n A_n z_n + \epsilon
\]

Objects:

- \(A_g\): controlled gradient-common basis.
- \(A_f\): controlled functional shared basis.
- \(B_g\): group-specific unique basis.
- \(A_n\): activation nuisance basis.
- \(z_g,z_f,z_u,z_n\): latent variables.
- \(g\): group label.

Group gradients are computed from zero-readout residuals:

\[
G_g=\mathbb{E}[\delta_g h^\top\mid g]
\]

The gradient-intersection estimator uses:

\[
C_{\cap}=\frac{1}{|G|(|G|-1)}
\sum_{g\neq g'}G_g^\top G_{g'}
\]

The functional shared estimator uses the input-side cross-covariance between
hidden states and shared targets.

## 5. Configuration

| Item | Value |
|---|---|
| hidden dimension | 32 |
| common rank | 2 |
| unique rank | 2 |
| nuisance rank | 2 |
| groups | 6 |
| samples per group | 500 |
| seeds | 0-19 |
| regimes | aligned_common, activation_nuisance, unique_variance, functional_gradient_split, entangled_residual |
| estimators | activation_pca, gradient_intersection, functional_shared, random_control |

Full configuration is stored in `tables/run_config.json`.

## 6. Metrics

`gradient_overlap_reduction`:

\[
\Delta C(P)=
\overline{\cos(G_g,G_{g'})}
-
\overline{\cos(G_g^r(P),G_{g'}^r(P))}
\]

where:

\[
G_g^r(P)=\mathbb{E}[\delta_g((I-P)h)^\top\mid g]
\]

`gradient_overlap_reduction_advantage`:

\[
\Delta C(P_{\mathrm{grad}})-\Delta C(P_{\mathrm{act}})
\]

`shared_loss_sensitivity`:

\[
L_c((I-P)h)-L_c(h)
\]

`gradient_common_alignment`:

\[
\|A_g^\top \hat U\|_F^2/k
\]

`functional_common_alignment`:

\[
\|A_f^\top \hat U\|_F^2/k
\]

## 7. Aggregate Results

| Regime | Activation PCA reduction | Gradient reduction | Advantage | Seed win rate | Pass status |
|---|---:|---:|---:|---:|---|
| aligned_common | 0.8885 | 0.8257 | -0.0628 | 0.05 | sanity check, not counted |
| activation_nuisance | -0.0557 | 0.5936 | 0.6494 | 1.0 | pass |
| unique_variance | -0.0578 | 0.6202 | 0.6779 | 1.0 | pass |
| functional_gradient_split | -0.0354 | 0.6494 | 0.6848 | 1.0 | pass |
| entangled_residual | 0.2300 | 0.7003 | 0.4703 | 1.0 | pass |

Criterion winners:

| Regime | Gradient-overlap winner | Shared-loss winner | Gradient-alignment winner | Functional-alignment winner |
|---|---|---|---|---|
| aligned_common | activation_pca | functional_shared | activation_pca | activation_pca |
| activation_nuisance | gradient_intersection | functional_shared | gradient_intersection | functional_shared |
| unique_variance | gradient_intersection | functional_shared | gradient_intersection | functional_shared |
| functional_gradient_split | gradient_intersection | functional_shared | gradient_intersection | functional_shared |
| entangled_residual | gradient_intersection | functional_shared | gradient_intersection | functional_shared |

## 8. Visualization Results

### Figure 1: Gradient Advantage By Regime

![Gradient advantage by regime](figures/gradient_advantage_by_regime.png)

Question answered: Does gradient intersection reduce cross-group gradient
overlap more than activation PCA?

Metric definition: \(P_{\mathrm{grad}}\) reduction minus \(P_{\mathrm{act}}\)
reduction.

Data source: `tables/gradient_vs_activation_summary.csv`.

Aggregation level: mean and standard deviation over 20 seeds.

How to read: positive bars support gradient common over activation common for
optimization interference.

Observed result: all four mismatch regimes are positive with seed win rate
1.0; the aligned sanity-check regime is negative because mechanisms are
intentionally aligned and activation PCA can recover the same object.

Take-home: gradient common is the better optimization-common estimator when
activation and gradient objects diverge.

Limitation: this is a controlled synthetic mechanism audit, not real-DCLM
evidence.

### Figure 2: Gradient Overlap Reduction

![Gradient overlap reduction by regime](figures/gradient_overlap_reduction_by_regime.png)

Question answered: Which candidate projector reduces redundant group-gradient
overlap?

Metric definition: average pairwise group-gradient cosine before
residualization minus after residualization.

Data source: `tables/gradient_vs_activation_scores.csv`.

How to read: positive values mean residualization reduced group-gradient
overlap.

Observed result: activation PCA works in the aligned sanity-check regime but is
negative or weak in mismatch regimes. Gradient intersection is positive and
large in all mismatch regimes.

Take-home: activation variance can be misleading for optimization common.

Limitation: a lower overlap metric does not by itself prove rare-loss utility
or training preservation.

### Figure 3: Criterion Winners

![Criterion winners by regime](figures/criterion_winners_by_regime.png)

Question answered: Do optimization and shared-function criteria select the
same estimator?

Metric definition: aggregate winner by criterion and regime.

Data source: `tables/gradient_vs_activation_winner_summary.json`.

How to read: each cell shows the estimator with the highest criterion mean.

Observed result: gradient intersection wins gradient-overlap reduction and
gradient-common alignment in mismatch regimes. Functional shared wins
shared-loss sensitivity and functional-common alignment.

Take-home: useful shared common and optimization-interference common are
separable in this controlled audit.

Limitation: the figure does not prove which common should be removed in a real
model; it only separates estimator roles.

## 9. Rival Explanations

R1: Activation PCA already captures the optimization common.

Status: weakened in mismatch regimes. Activation PCA has negative or weak
gradient-overlap reduction when activation energy is nuisance, unique, or
functional shared structure.

R2: Gradient intersection only tracks target scale.

Status: partly open. The controlled construction intentionally places the
optimization signal in the gradient-common basis. This validates the estimator
for the intended mechanism, but real-data validation remains required.

R3: Functional shared common and gradient common are the same object.

Status: weakened. In `functional_gradient_split`, functional shared wins
shared-loss sensitivity with 8.5791, while gradient intersection wins
gradient-overlap reduction with 0.6494 and has shared-loss sensitivity 0.0037.

R4: Estimator differences are seed noise.

Status: weakened. All mismatch regimes have gradient-intersection seed win
rate 1.0.

## 10. Stage-Level Evidence

Generation: complete. Regime configuration is in `tables/run_config.json`.

Estimator validation: complete. All estimators produce finite rank-2
projectors; random control does not win aggregate optimization criteria.

Scoring: complete. Per-seed scores are in
`tables/gradient_vs_activation_scores.csv`.

Aggregation: complete. Summary tables and winner JSON are in
`tables/gradient_vs_activation_summary.csv`,
`tables/gradient_vs_activation_estimator_summary.csv`, and
`tables/gradient_vs_activation_winner_summary.json`.

## 11. Artifact Map

| Artifact | Path |
|---|---|
| runner | `scripts/run_gradient_vs_activation_full_run.py` |
| protocol | `protocol.md` |
| Chinese protocol companion | `protocol_cn.md` |
| summary | `summary.md` |
| detailed record | `detailed.md` |
| run config | `tables/run_config.json` |
| per-seed scores | `tables/gradient_vs_activation_scores.csv` |
| estimator summary | `tables/gradient_vs_activation_estimator_summary.csv` |
| primary summary | `tables/gradient_vs_activation_summary.csv` |
| winner summary | `tables/gradient_vs_activation_winner_summary.json` |
| primary figure | `figures/gradient_advantage_by_regime.png` |
| overlap figure | `figures/gradient_overlap_reduction_by_regime.png` |
| winner figure | `figures/criterion_winners_by_regime.png` |

## 12. Claim Boundary

Can claim: in controlled activation-gradient mismatch settings, gradient
intersection is a better estimator of optimization-common than activation PCA.

Cannot claim: real-DCLM preservation rescue, final layerwise estimator,
residualized MoE improvement, or utility improvement.

## 13. Next Decision

Proceed to the functional/feedback bridge. The next test should decide whether
gradient common is useful shared structure, harmful redundant update signal, or
a contributor to step-0 to step-5/10 proxy-route collapse.

