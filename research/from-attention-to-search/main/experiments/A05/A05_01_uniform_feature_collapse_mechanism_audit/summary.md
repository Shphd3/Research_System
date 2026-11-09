# Result Summary: A05_01_uniform_feature_collapse_mechanism_audit

Anchor: `../../../problem_anchors/05_failure_mechanism/05_01_geometric_inhibition_anchor.md`

Story: this audit asks whether collapse in the original uniform feature setting is already determined by early hidden-router geometry or emerges later during top-1 training.

## 0. Closure Summary

Purpose: diagnose collapse in the original pre-relaxation uniform feature experiment before using inhibition or feature-assumption relaxation as main evidence.

Hypothesis / question: final collapse may be driven by early geometry and then amplified by top-1 routing, rather than appearing as a late training drift.

Conclusion: choose **A. Early-geometry dominated collapse**, with a secondary common-direction clue. In the 9 final-collapsed condition-seeds, the final dominant expert is already the step-0 dominant expert in all 9 runs, and it is again the dominant expert at steps 50 and 100 in all 9 runs.

Key evidence: 9/24 condition-seeds are final collapsed; their first collapsed checkpoint is step 10 in 4 runs, step 20 in 3 runs, and step 100 in 2 runs. Mean top-1 margin in final-collapsed runs rises from 0.078 at step 0 to 0.797 at final.

Claim boundary: this audit does not prove that common direction is the only cause, does not solve collapse, and does not claim utility mismatch because forced-routing utility was not recomputed here.

Next decision: test a minimal anti-lock-in control on the same uniform setting before returning to inhibition or feature-utility claims.

## Observation

Final collapsed seeds are not late surprises. They start with a strong early dominant expert, briefly fluctuate in some cases, then lock back to the final expert by step 50 or step 100.

Top-1 margin grows during training. The early margin is not enough to call the model fully locked at initialization, but it gives a preferred expert that training amplifies.

The final collapse expert aligns increasingly with the common hidden direction. In final-collapsed runs, final-expert common-direction cosine rises from 0.148 at step 0 to 0.873 at final, while residual alignment remains small.

## Interpretation

The safest mechanism statement is: early hidden-router geometry selects a likely dominant expert, and top-1 training amplifies that early preference into collapse. The common direction is a plausible source of that early preference, but the causal role still needs intervention evidence.

## Operationalization Boundary

This result weakens: the idea that final collapse is primarily a late-stage drift from balanced early routing.

This result does not falsify: the possibility that a different router, a load guard, or a utility-binding objective can prevent collapse.

Tested operationalization: route load, feature-to-expert assignment, hidden-router cosine, top-1 margin, common-direction alignment, and router-vector geometry on all available seeds and conditions.

Alternative operationalizations still open: forced-routing utility during early training and controlled common-offset intervention.

## Limitation

Original early model states at steps 10, 20, and 50 were not available for every run. Those early hidden/router geometry measurements come from same-config diagnostic replay, so they are mechanism evidence rather than byte-identical checkpoint replay.

## Key Figures

![Collapse load timeline by seed and condition](figures/collapse_load_timeline_by_seed_condition.png)

Supports: final collapsed seeds become concentrated early and then stay locked.

![Top-1 margin dynamics](figures/top1_margin_dynamics.png)

Supports: top-1 margins grow during training, especially in final-collapsed runs.

![Common-direction alignment](figures/common_direction_alignment.png)

Supports: final collapse experts increasingly align with the common hidden direction.

![Seed contrast evidence](figures/evidence_s1cos_seed_contrast_load_margin_common.png)

Supports: seed-level contrasts are necessary because averaging hides lock-in and recovery cases.

## Claim Update

- Supported: final collapse in this audit is early-geometry dominated plus training-amplified.
- Weakened: late-collapse-only and target-failure explanations.
- Still unclear: whether common direction is causally sufficient and whether utility misalignment exists before experts co-adapt.

## What Cannot Be Claimed

Collapse is not solved. Common direction is not proven to be the only cause. Lower target loss does not imply valid routing. Utility mismatch cannot be claimed without forced-routing utility analysis.

## Next Decision

Run a minimal uniform-setting anti-lock-in test, prioritizing common-direction control or auxiliary load-balance warmup, and judge it by final max-load, load entropy, active experts, and target accuracy.
