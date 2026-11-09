# Summary: A06_02_01_E07 Top-1 Lock-In Margin Threshold

## Result

The controlled no-position bridge shows a finite positive-margin threshold for
feature-to-expert preservation. Shrinking the initial router row gaps by
\(q \ge 0.05\) preserved the original feature-to-expert identity perfectly across
C0-C3 and all 8 seeds. Shrinking to \(q=0.02\) no longer preserved identity:
final matched preserve fraction dropped to 0.375, final sign-flip rate rose to
0.159, and final current margin became negative.

This supports a thresholded top-1 lock-in interpretation, not the stronger
claim that any positive margin is enough. A small positive step-0 margin can be
valid at initialization and still be consumed by training drift.

## Terminology / Definitions

| Term | Plain meaning | Concrete computation | Why it matters | Cannot prove |
|---|---|---|---|---|
| Router row | One expert's linear gating vector. | Row \(w_e\) in the router matrix. | Determines which expert receives a hidden state. | Expert utility. |
| Margin | How far a feature is from changing its selected expert. | Difference between the matched expert logit and nearest competitor logit. | The experiment asks whether positive margin is enough to preserve routing. | Semantic feature quality. |
| Row-gap scaling | A clean way to reduce initial margin. | \(w'_e(q)=\bar w+q(w_e-\bar w)\), where \(\bar w=E^{-1}\sum_e w_e\). | Keeps the common row center fixed and scales pairwise gaps by \(q\). | Real-DCLM behavior. |
| Matched preserve fraction | Whether the original feature-to-expert identity is kept. | Fraction of features still routed to their step-0 matched expert. | Primary metric; NMI can stay high after expert identities swap. | Whether the expert is useful. |
| Feature NMI | Whether routing still separates features as clusters. | Normalized mutual information between feature id and routed expert id. | Secondary metric; catches feature separation. | Original feature-expert identity. |
| Sign flip rate | Fraction of pairwise margins that crossed the decision boundary. | Rate of \(\gamma_{f,e}(t) \le 0\). | Direct boundary-crossing evidence. | Why the drift happened. |

## Setup

This is the A06 controlled bridge: one-layer Transformer plus top-1 MoE, 4
experts, hidden size 128, no learned absolute positional embedding, no B token,
slot length 4, route on the last token of the feature slot, and target depends
only on feature identity.

The run used C0-C3 cells, 8 seeds from `20260623` to `20260630`, and checkpoints
through step 1600. For each run, pseudo-center router rows were first discovered
from route-position hidden states, then the row-gap intervention was applied
before training.

## Intervention Validity

For \(q>0\), row-gap scaling preserved the step-0 assignment and scaled the
initial margin exactly as intended. The zero-margin guard and crossed guard
failed the original matching, so the negative controls behaved correctly.

| Condition | Step-0 preserve | Step-0 margin | Margin scale | Step-0 sign flip |
|---|---:|---:|---:|---:|
| \(q=1.00\) | 1.000 | 5.667 | 1.000 | 0.000 |
| \(q=0.50\) | 1.000 | 2.834 | 0.500 | 0.000 |
| \(q=0.25\) | 1.000 | 1.417 | 0.250 | 0.000 |
| \(q=0.10\) | 1.000 | 0.567 | 0.100 | 0.000 |
| \(q=0.05\) | 1.000 | 0.283 | 0.050 | 0.000 |
| \(q=0.02\) | 1.000 | 0.113 | 0.020 | 0.000 |
| \(q=0\) guard | 0.000 | 0.000 | 0.000 | 1.000 |
| crossed guard | 0.000 | -9.017 | -0.608 | 0.987 |

Source: [`tables/intervention_audit_aggregate.csv`](tables/intervention_audit_aggregate.csv).

## Primary Evidence

At final step 1600, all \(q \ge 0.05\) conditions preserved perfectly. The
\(q=0.02\) condition did not: it retained high NMI on average but lost the
original feature-to-expert identity in many runs. This is why matched preserve
fraction is the primary metric.

| Condition | Final feature NMI | Final preserve min | Final margin | Sign flip rate | Cluster-aware margin | Max load |
|---|---:|---:|---:|---:|---:|---:|
| \(q=1.00\) | 1.000 | 1.000 | 3.484 | 0.000 | 3.215 | 0.250 |
| \(q=0.50\) | 1.000 | 1.000 | 2.124 | 0.000 | 1.954 | 0.250 |
| \(q=0.25\) | 1.000 | 1.000 | 1.408 | 0.000 | 1.296 | 0.250 |
| \(q=0.10\) | 1.000 | 1.000 | 0.889 | 0.000 | 0.813 | 0.250 |
| \(q=0.05\) | 1.000 | 1.000 | 0.735 | 0.000 | 0.668 | 0.250 |
| \(q=0.02\) | 0.909 | 0.375 | -0.588 | 0.159 | -0.633 | 0.414 |
| \(q=0\) guard | 0.555 | 0.000 | -2.000 | 0.568 | -2.095 | 0.750 |
| crossed guard | 0.907 | 0.000 | -6.567 | 0.771 | -7.187 | 0.414 |

Source: [`tables/lockin_final_condition_aggregate.csv`](tables/lockin_final_condition_aggregate.csv).

## Main Figures

![Final preserve versus q](figures/q_threshold_preserve.png)

This figure tests whether the original feature-to-expert identity survives as
the initial row gap is reduced. The visible threshold is between \(q=0.05\) and
\(q=0.02\) in this controlled setup.

![Final sign flips versus q](figures/q_threshold_sign_flip.png)

This figure tests whether routing preservation loss corresponds to decision
boundary crossing. Sign flips remain zero through \(q=0.05\) and become nonzero
at \(q=0.02\).

![Current margin trajectory](figures/current_margin_trajectory.png)

This trajectory shows that \(q=0.02\) starts with a positive margin but enters
negative-margin territory early, while \(q \ge 0.05\) remains positive.

## Failure Decomposition

The \(q=0.02\) failures were not uniform across conditions. The moderate nuisance
cell was most fragile: only 0.125 mean final preserve-min, with mean sign-flip
rate 0.219. This suggests nuisance strength raises the minimum safe margin.

| Cell | Condition | Final NMI | Preserve min | Final margin | Sign flip rate | Cluster-aware margin |
|---|---|---:|---:|---:|---:|---:|
| C0 clean | \(q=0.02\) | 0.921 | 0.625 | -0.152 | 0.115 | -0.205 |
| C1 mild nuisance | \(q=0.02\) | 0.900 | 0.250 | -0.681 | 0.177 | -0.712 |
| C2 moderate nuisance | \(q=0.02\) | 0.883 | 0.125 | -1.102 | 0.219 | -1.145 |
| C3 weak feature nuisance | \(q=0.02\) | 0.933 | 0.500 | -0.415 | 0.125 | -0.472 |
| all C0-C3 | \(q=0.05\) | 1.000 | 1.000 | positive in every cell | 0.000 | positive in every cell |

Source: [`tables/condition_final_margin_budget_aggregate.csv`](tables/condition_final_margin_budget_aggregate.csv).

## Interpretation

The result updates the A06 preservation mechanism in a precise way:

1. Positive initial assignment is necessary but not sufficient.
2. The correct object is the amount of positive margin left after expected
   early training drift, not just whether the margin is positive at step 0.
3. Top-1 routing does have path dependence, but the basin has a finite
   thickness. In this controlled bridge, the tested threshold lies between
   \(q=0.02\) and \(q=0.05\).
4. Feature NMI alone overstates preservation because crossed or swapped
   mappings can still look feature-separated.

## Claim Boundary

Can claim:

- In the controlled no-position A06 bridge, row-gap scaling cleanly changes the
  initial margin while preserving step-0 assignment for \(q>0\).
- Controlled preservation behaves like a finite-threshold margin basin.
- \(q=0.02\) is below the safe region for many seeds and nuisance cells, while
  \(q \ge 0.05\) is safe in this run.

Cannot claim:

- The same numerical threshold transfers to real-DCLM hidden states.
- Margin preservation explains semantic utility.
- Any positive margin is enough.
- The exact threshold is universal across model sizes, slot designs, RoPE, or
  natural language data.

## Next Decision

Use the A06_02_01_E07 threshold logic in the real-DCLM preservation audit: estimate
whether real-DCLM proxy initialization has not only positive step-0 margin, but
margin large enough to survive the measured step-5 and step-10 router/feature
drift. The next experiment should report matched preserve fraction, current
margin, cluster-aware margin, and sign-flip rate, not NMI alone.

