# Summary: A06_02_03_E01 Soft-Router Advantage-To-Margin Dynamics

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`

## Result Snapshot

**Verdict: supported in the frozen soft-router model.**

**What we established:** Expert function, not initialized route geometry alone, determines the sign of local matched-margin pressure.

**What the experiment shows:** Across 32 seeds, matched expert utility produced positive geometry-matched margin change in every feature-seed cell. Identical experts produced exactly zero router update. Permuting expert utility made the original geometry-matched margin negative while increasing the utility-aligned margin.

**What we do next:** Test whether weighted top-1 retains this direct utility-directed correction when the useful expert is initially unselected.

## Purpose

The run asks whether expert advantage is a real mechanism variable or only a re-description of router geometry.

## Terminology / Definitions

| Term | Plain meaning | Computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Geometry-matched margin | Score lead of expert \(f\) on feature center \(f\) | \((w_f-w_b)^\top\mu_f\) | Measures reinforcement of the initialized binding | Long-run preservation |
| Utility-aligned margin | Score lead of the expert whose fixed output predicts feature \(f\) | same margin with the utility map | Separates function from row label | Semantic identity |
| Formula closure | Analytical row update equals autograd SGD update | maximum absolute row-update error | Validates implementation | Mechanism by itself |

## Exact Setup

- Four balanced features; 16-dimensional orthogonal feature centers.
- 256 frozen hidden states per feature with isotropic noise 0.05.
- Four fixed expert output tables and a softmax router.
- Router-only one-step SGD at learning rates 0.01 and 0.05.
- Conditions: matched utility, identical experts, and cyclically permuted utility.
- Seeds: 0-31.
- Run: `a06_31_33_full_20260710_001757` on two local H100 GPUs.

## Primary Metric

The primary metric is the fraction of feature-seed cells with positive geometry-matched margin change. It decides whether matched utility consistently reinforces the intended boundary.

## Result

| Condition | LR | Positive matched-margin rate | Mean geometry-margin change | Mean utility-margin change |
| --- | ---: | ---: | ---: | ---: |
| Matched utility | 0.01 | 1.000 | +0.002391 | +0.002391 |
| Matched utility | 0.05 | 1.000 | +0.011953 | +0.011953 |
| Identical experts | 0.01 / 0.05 | 0.000 | 0.000000 | 0.000000 |
| Permuted utility | 0.01 | 0.000 | -0.001906 | +0.003219 |
| Permuted utility | 0.05 | 0.000 | -0.009529 | +0.016093 |

The maximum formula-closure error was \(2.61\times10^{-18}\).

## Key Figure

![Utility intervention changes the sign of matched-margin pressure](figures/utility_intervention_margin_change.png)

**What this tests:** Whether local router pressure follows expert function or the initialized row label.

**How to read:** Positive bars reinforce the original geometry-matched expert. Negative bars damage that binding.

**Observed result:** Matched utility is positive, identical utility is zero, and permuted utility is negative for the original binding.

**Take-home:** Formula closure is only a numerical guard; the causal evidence is the sign reversal under the utility intervention.

**What this does not prove:** Sparse top-1 correction, accumulated preservation, learned expert utility, or real-text behavior.

## Claim Boundary

**Can claim:** In the frozen soft-mixture model, feature-conditioned expert utility is sufficient to create positive local matched-margin pressure.

**Cannot claim:** The same signal is available to an unselected top-1 expert or survives trainable hidden-state dynamics.

## Next Decision

Measure correction latency when the useful expert starts at router rank 2 or 4 under soft and weighted top-1 routing.

