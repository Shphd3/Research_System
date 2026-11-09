# Summary: A06_02_03_E03 Background Bias And Margin Budget

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`

## Result Snapshot

**Verdict: supported in the frozen weighted-top-1 model.**

**What we established:** Background position count alone does not consume routing margin. Damage requires a nonzero mean background update projected onto feature decision boundaries.

**What the experiment shows:** Orthogonal zero-mean background and common-state background with balanced targets never crossed a boundary, even when only 2 of 32 positions were signal. Common-biased background caused the three non-common features to cross when signal was 8/32 or lower. At 8/32 they later recovered; at 4/32 they ended on the boundary; at 2/32 they remained negative-margin.

**What we do next:** Reintroduce trainable hidden states and AdamW on the one-layer Transformer+MoE full-LM surface, and test whether router-row drift, center drift, and optimizer normalization still predict both first crossing and recovery.

## Purpose

The run separates background quantity from the signed projection of background updates onto routing boundaries.

## Terminology / Definitions

| Term | Meaning | Computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Margin p05 | Fifth percentile of final feature-seed minimum matched margin | router-logit gap | Protects against common-feature averaging | Real semantic utility |
| Ever-cross rate | Fraction of feature-seed cells whose margin was nonpositive at any step | binary trajectory event | Detects transient failure | Final irreversibility |
| Common-biased background | Shared common state with target class 0 | systematic mean gradient | Tests directional bias | Real-DCLM common operator |
| Budget closure | Reconstructed pairwise margin equals measured margin | maximum absolute error | Validates source attribution | Causal transfer to AdamW |

## Exact Setup

- Length 32; signal counts 32, 16, 8, 4, or 2.
- Feature state: one shared common direction plus one orthogonal feature residual.
- Four fixed class-specialized experts and ideal residual router rows.
- Weighted top-1, router-only SGD, 500 steps, 32 seeds.
- Background controls: boundary-orthogonal zero-mean, common state with balanced targets, and common state with target-0 bias.

## Primary Result

| Background | Signal fraction | Final margin p05 | Ever-cross rate | Final matched-route rate |
| --- | ---: | ---: | ---: | ---: |
| Signal only | 1.000 | 2.826 | 0.000 | 1.000 |
| Orthogonal zero-mean | 0.0625 | 1.260 | 0.000 | 1.000 |
| Common balanced | 0.0625 | 1.260 | 0.000 | 1.000 |
| Common biased | 0.500 | 1.154 | 0.000 | 1.000 |
| Common biased | 0.250 | 0.424 | 0.750 | 1.000 |
| Common biased | 0.125 | -0.001 | 0.750 | 0.734 |
| Common biased | 0.0625 | -1.128 | 0.750 | 0.250 |

The budget reconstruction error was at most \(1.79\times10^{-14}\).

## Key Figure

![Directional background bias creates crossing and recovery thresholds](figures/margin_budget_threshold.png)

**How to read:** The left panel shows final low-tail margin; the right panel shows whether any boundary was crossed during training.

**Observed result:** Only common-biased background produces crossings. A signal fraction of 0.25 crosses transiently but recovers by step 500.

**Take-home:** “Margin ever became negative” and “routing finally failed” are different outcomes. The controlled model has a first-cross threshold between 0.25 and 0.5 and a final-recovery threshold between 0.125 and 0.25.

**What this does not prove:** The same thresholds or common operator hold in trainable Transformer or real-text training.

## Claim Boundary

**Can claim:** In the frozen controlled model, systematic boundary-aligned background bias can exhaust a finite margin buffer; orthogonal or balanced background count alone does not.

**Cannot claim:** Generic stochastic background noise is harmless, AdamW has the same budget, hidden drift is negligible, or common subtraction is validated.

## Next Decision

On the original trainable full-LM bridge, can the actual finite-step margin change be predicted by router-row drift, feature-center drift, their cross term, and optimizer preconditioning, including both first crossing and re-entry?
