---
anchor_id: A07_high_dim_uniform_expert_geometry_gate
parent_node: rq.expert_specialization
status: proposed_next_anchor
created: 2026-06-16
canonical_language: en
source_anchor: A06_2x2_expert_geometry_gate
---

# A07 High-Dimensional Uniform Expert-Geometry Gate Anchor

## researcher judgment record

- A06 supports M4 matrix response energy as the core 2D static expert-geometry metric.
- The next decision is whether centered/calibrated M4 can generalize from 2D uniform features to high-dimensional uniform features.
- Raw M4 cannot be the theoretical target because average expert energy can create load imbalance even in 2D.
- Centered M4 is exact 50/50 in 2D, but in high dimension centering only guarantees zero mean score difference.
- The high-dimensional claim must therefore be approximate or calibrated, not exact by default.
- M3 top-r projection is the low-rank approximation baseline; prototype metrics remain sign-sensitive baselines.
- The primary read must combine load, margin, degeneracy, oracle agreement, and spectral-spread diagnostics.
- This anchor is static and geometric; it does not claim trainability, real-text transfer, or causal expert utility.

## Problem Definition

- Parent problem: how can a sparse MoE gate connect routing decisions to expert-side geometry rather than to an expert-agnostic random classifier?
- Current subproblem: under high-dimensional uniform feature input, can expert-matrix-induced static scores produce balanced routing with nonzero expert preference?
- Decision question: should the next theoretical and experimental target be raw M4, centered M4, calibrated M4, or a low-rank approximation of M4?

Not in scope:

- trainable router dynamics;
- full transformer hidden-state distributions;
- semantic feature labels;
- causal expert utility;
- common-component removal as a deployed architecture.

Operational definitions:

- Expert geometry: the input-side sensitivity encoded by expert matrix `A_e`.
- M4 score: `q_e(x) = x^T A_e^T A_e x = ||A_e x||^2`.
- Centered M4 score: `q_tilde_e(x) = x^T G_e x - tr(G_e)/d` for `G_e = A_e^T A_e`.
- Calibrated M4 score: `q_e(x) - tau_e`, where `tau_e` is fit only to meet a load target on a reference distribution.
- Metric-defined preference: the selected expert has a positive score margin over the alternative.
- Uniform feature input: `x ~ Unif(S^{d-1})` unless the protocol explicitly uses the unit ball or a finite sampled uniform design.

## 2. Physical Priors
- Expert-aware routing should compare the current feature direction with the input directions to which each expert is sensitive.
- Load balance alone is weak in 2D because many symmetric direction rules split a uniform circle exactly in half.
- The useful signal is not only `50/50` load; it is balanced load plus a stable positive compatibility margin.
- In high dimension, the correct question is not whether centering gives exact 50/50 for every matrix pair; it is whether load becomes approximately balanced under spectral-spread conditions or can be calibrated without destroying margin.

## Hypothesis

H1: Centered/calibrated M4 is the correct high-dimensional theoretical target.

- Supported if centered M4 gives near-balanced load under random high-dimensional anisotropic experts when the score-difference spectrum is not spiky.
- Weakened if centered M4 remains strongly imbalanced in typical random high-dimensional cases or loses margin after calibration.

H2: Spectral spread controls high-dimensional balance.

- Supported if load error is small when `sum |lambda_i|^3 / (sum lambda_i^2)^{3/2}` is small for the centered score-difference matrix.
- Weakened if load error does not track this spectral-spread statistic.

H3: M3 top-r is a useful approximation only when it preserves M4 oracle decisions and margin.

- Supported if increasing rank improves agreement with centered M4 and preserves load and margin.
- Weakened if top-r projection balances load but disagrees with M4 or has low margin.

## 4. Mathematical Model
Two experts:

```math
A_1,A_2 \in \mathbb{R}^{m \times d}, \qquad G_e=A_e^T A_e.
```

Raw M4:

```math
q_e(x)=x^T G_e x.
```

Centered M4:

```math
\tilde q_e(x)=x^T G_e x-\frac{1}{d}\mathrm{tr}(G_e).
```

Centered two-expert score difference:

```math
\tilde D(x)=\tilde q_1(x)-\tilde q_2(x)=x^T H_0x,
```

where

```math
H_0=(G_1-G_2)-\frac{1}{d}\mathrm{tr}(G_1-G_2)I.
```

For `x ~ Unif(S^{d-1})`, centering gives:

```math
\mathbb{E}[\tilde D(x)]=0.
```

But for `d>2`, this does not imply:

```math
\mathbb{P}[\tilde D(x)>0]=1/2.
```

High-dimensional approximate-balance condition:

Let `lambda_i` be the eigenvalues of `H_0`, and define

```math
r_3(H_0)=\frac{\sum_i |\lambda_i|^3}{\left(\sum_i \lambda_i^2\right)^{3/2}}.
```

If `r_3(H_0)` is small, the centered quadratic score difference is approximately symmetric, so load should be close to 50/50.

Low-rank approximation:

```math
q^{(r)}_e(x)=\sum_{k=1}^r \sigma_{e,k}^2 (v_{e,k}^T x)^2 - c_{e,r}.
```

The centering term can be sphere-theoretic,

```math
c_{e,r}=\frac{1}{d}\sum_{k=1}^r \sigma_{e,k}^2,
```

or empirical,

```math
c_{e,r}=\mathbb{E}_{x\sim \mathcal{D}_{ref}}\sum_{k=1}^r \sigma_{e,k}^2 (v_{e,k}^T x)^2.
```

## Minimal Tests

Test 1: High-dimensional centered-M4 uniform-sphere audit.

- Compare raw M4, centered M4, quantile-calibrated M4, M3 top-r, and linear baselines across dimensions.
- Primary metrics: natural load error, calibrated load error, mean margin, low-margin fraction, degeneracy rate, spectral-spread statistic, and finite-sample stability.
- Main question: does centered M4 become near-balanced when the score-difference spectrum is non-spiky?

Test 2: Low-rank approximation audit.

- Compare top-r weighted projection against full centered M4.
- Primary metrics: agreement with full M4, margin retention, load error, rank-energy captured, and failure under near-identical or isotropic experts.
- Main question: can a low-rank static router preserve the M4 oracle sufficiently to be useful?

Test 3: Text-facing static proxy audit.

- Apply raw, centered, calibrated, and low-rank M4-style scores to sampled hidden states from real or semi-real text.
- Primary metrics: load, margin, common-direction sensitivity, empirical-centering stability, probe-label correlation, and forced-utility match if available.
- Main question: which static score is most plausible as a bridge to real router construction?

## Falsifiable Outcomes

Supports centered/calibrated M4 if:

- raw M4 is imbalanced when expert energy budgets differ;
- centered M4 reduces load error under uniform high-dimensional input;
- load error is predicted by spectral-spread diagnostics;
- quantile calibration enforces balance without collapsing margin;
- low-rank M4 approximations preserve oracle agreement when rank captures response energy.

Weakens centered/calibrated M4 if:

- centered M4 remains imbalanced in typical random high-dimensional settings despite non-spiky spectra;
- calibration balances load only by routing near-zero-margin points;
- low-rank approximations have high load balance but poor agreement with full M4;
- prototype baselines match M4 margin and stability without extra assumptions.

Insufficient evidence if:

- only load is reported;
- only one dimension is tested;
- raw and centered scores are not separated;
- margin scale is omitted;
- near-identical and isotropic controls are omitted;
- text results are interpreted semantically without causal utility evidence.

## Current Evidence

- A06_E01 shows M4 is the best 2D core metric in decisive anisotropic conditions: natural load error is `0.0000` in C3/C5 and mean margin is `1.5444 / 2.3873`.
- A06_E01 also shows M4 correctly degenerates in equal-singular-value isotropic control, where the scores have no expert preference.
- M3 top-1 works in anisotropic 2D cases but has smaller margin than M4, making it an approximation candidate rather than the core metric.
- M1/M2 prototypes can split uniform 2D input but are sign-sensitive or prototype-dependent.
- The centered-M4 proof shows exact 2D 50/50 only after removing average response energy; it also states that high-dimensional centering alone does not guarantee exact 50/50.

## Claim Boundary And Next Decision

Can claim:

- M4 is the current 2D core expert-geometry metric.
- Raw M4 is not the right theoretical target for uniform-load guarantees.
- Centered/calibrated M4 is the correct next high-dimensional candidate.
- M3 top-r should be evaluated as a low-rank approximation to M4, not as an equal replacement.
- High-dimensional uniform routing requires spectral-spread or calibration arguments.

Cannot claim:

- centered M4 gives exact 50/50 in all high-dimensional cases;
- high-dimensional random experts always have useful margin;
- a trainable router will learn M4;
- real text hidden states are uniform or isotropic;
- load balance implies semantic or causal expert specialization.

Next decision:

Run A07_E01 to test high-dimensional centered/calibrated M4 under uniform-sphere features, then run A07_E02 to decide which static expert-geometry score is the best bridge to real text hidden states.
