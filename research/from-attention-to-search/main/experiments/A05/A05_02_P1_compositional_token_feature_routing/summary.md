# Result Summary: A05_02_P1_compositional_token_feature_routing

Anchor: `../../../problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md`

Story: P1 tests whether routing follows the target-relevant factor when one input context contains \(S1\), \(S2\), and nuisance \(B_i\).

## 0. Closure Summary

Purpose: relax the single-feature-token assumption and test whether ordinary top-1 routing changes its route axis with the target rule.

Hypothesis / question: C1 should route by \(S1\), C2 by \(S2\), and C3 by \((S1,S2)\) if routing follows the target-relevant factor. The route-axis metric is normalized mutual information (NMI), but it is valid only under high target accuracy and non-collapsed load.

Conclusion: P1 is **not a positive result overall**. Target accuracy is 1.000 in all condition groups, but C1/C2 mostly collapse. C3-B0 is the only interpretable positive clue: it is relatively non-collapsed and its highest route-axis NMI is with \((S1,S2)\).

Key evidence: C1/C2 have mean active experts 1.33 or lower and mean max-load 0.917 to 1.000; C3-B0 has mean active experts 3.00, max-load 0.686, and NMI(route,\((S1,S2)\))=0.528.

Claim boundary: target learning can succeed without meaningful routing. P1 does not show robust target-rule-dependent routing under ordinary top-1.

Next decision: do not use P1 as specialization evidence; require a load/entropy guard or anti-lock-in intervention before re-interpreting compositional route-axis metrics.

## Observation

C1 and C2 are easy target-learning tasks, but most seeds route almost all samples to one expert. Under the collapse rule max-load \(\ge 0.95\), 9 of 12 C1/C2 runs are final collapsed, and all 9 first cross the threshold by step 200.

C3-B0 is the cleanest condition: all three seeds learn the target, use multiple experts, and route more by \((S1,S2)\) than by \(S1\), \(S2\), or \(B_i\) alone.

I1 does not repair P1. It hard-collapses C2 and makes C3 close to collapse.

## Interpretation

The P1 evidence weakens broad target-rule-dependent routing under ordinary top-1. The remaining positive clue is narrow: C3-B0 suggests that a compositional target can sometimes align routing with a compositional feature axis when collapse is not severe.

## Operationalization Boundary

This result weakens: the claim that ordinary top-1 robustly follows target-relevant factors in compositional contexts.

This result does not falsify: the possibility that a stronger anti-collapse or utility-binding objective could make P1 positive.

Tested operationalization: route NMI at the \(B_i\) pre-target position under matched target rules and seeds.

Alternative operationalizations still open: harder one-factor tasks, explicit load balancing, delayed top-1, or utility-bound routing.

## Limitation

The run used two visible H100 GPUs even though the original request asked for 4-card completion. This does not change the recorded result, but it should be reported as an execution boundary.

## Key Figures

![B0 target-rule route-axis NMI](figures/B0_target_rule_route_axis_nmi.png)

Supports: C3-B0 is the only condition where NMI can be interpreted as a route-axis clue.

![I1 target-rule route-axis NMI](figures/I1_target_rule_route_axis_nmi.png)

Supports: I1 does not repair the P1 failure.

![C1/C2 route load over checkpoints](figures/collapse_route_load_over_checkpoints_C1_C2.png)

Supports: C1/C2 final collapse is early-training lock-in by step 200, not late drift.

## Claim Update

- Supported: target learning is not enough to validate routing.
- Weakened: robust target-rule-dependent routing under ordinary top-1.
- Still unclear: whether anti-lock-in control can rescue C1/C2 and preserve C3 structure.

## What Cannot Be Claimed

Do not claim expert utility specialization, robust compositional routing, or inhibition success from P1.

## Next Decision

Use P1 only as bounded negative evidence unless a future anti-lock-in run makes C1/C2 non-collapsed and seed-stable.
