# Result Summary: A05_02_P3_same_expert_feature_relation

Anchor: `../../../problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md`

Story: P3 tests whether features assigned to the same expert share family structure more than a load-matched random grouping.

## 0. Closure Summary

Purpose: relax the assumption that same-expert multi-feature assignment can be ignored, and test whether same-expert features form structured families.

Hypothesis / question: P3a tests input-family-only grouping. P3b tests input-family plus shared family target. The primary metric is family purity over load-matched random baseline, \(\Delta_{\mathrm{family}}\).

Conclusion: P3a and P3b are **not positive**. All conditions reach target accuracy 1.000, but family-purity gains are small and seed-unstable. P3b is not reliably stronger than P3a.

Key evidence: mean \(\Delta_{\mathrm{family}}\) is 0.055 for P3a-B0, 0.047 for P3a-I1, 0.087 for P3b-B0, and 0.090 for P3b-I1. The P3b gains are mainly driven by seed `20260522`; other seeds are zero, near zero, or negative.

Claim boundary: this supports the weaker interpretation that ordinary top-1 same-expert assignment is closer to arbitrary or early-locked buckets than reliable family grouping.

Next decision: do not move from same-feature route consistency to family-level specialization claims unless a future non-collapse or utility-binding intervention makes P3b seed-stable.

## Observation

Target learning is not the issue: all condition groups reach target accuracy 1.000.

Family grouping is weak: actual family purity is only slightly above load-matched random on average, and not consistently above the random confidence band across seeds.

Shared target utility does not rescue grouping: P3b has slightly larger mean deltas but also stronger concentration and seed dependence.

## Interpretation

The P3 evidence weakens the claim that ordinary top-1 naturally groups related features when \(F>E\). The same expert can receive multiple features, but this assignment is not reliably family-structured.

## Operationalization Boundary

This result weakens: family-structured same-expert grouping under ordinary top-1.

This result does not falsify: family grouping under explicit load balance, utility-binding, supervised grouping, or a different router.

Tested operationalization: \(G=4\), \(K=4\), \(F=16\), \(E=4\), uniform distribution, route at the last \(F_{gk}\) token.

Alternative operationalizations still open: stronger non-collapse guard, utility-bound routing, larger family count, or longer full verification.

## Limitation

Some P3b runs are partially concentrated. This weakens positive grouping claims and is part of the negative result.

## Key Figures

![Family purity vs load-matched random](figures/family_purity_vs_load_matched_random.png)

Supports: actual family purity is only slightly above random and is not seed-stable.

![P3a expert x feature heatmap](figures/P3a_expert_feature_heatmap.png)

Supports: P3a input-family structure alone does not yield stable grouping.

![P3b expert x family composition heatmap](figures/P3b_expert_family_composition_heatmap.png)

Supports: P3b shared family target does not reliably strengthen family grouping.

## Claim Update

- Supported: same-expert assignment under ordinary top-1 is not reliable family grouping.
- Weakened: shared family target utility alone induces structured grouping.
- Still unclear: whether anti-lock-in or utility-binding can make P3b positive.

## What Cannot Be Claimed

Do not claim family grouping is impossible in general, and do not claim expert utility specialization.

## Next Decision

Treat ordinary top-1 same-expert buckets as arbitrary or early-locked until a stronger intervention produces seed-stable P3b family grouping.
