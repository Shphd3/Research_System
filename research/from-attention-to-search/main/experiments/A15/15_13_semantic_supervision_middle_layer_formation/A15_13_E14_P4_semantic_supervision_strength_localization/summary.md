# Summary: A15_13_E14_P4 Semantic-Supervision-Strength Localization

Primary Anchor: [A15_13 semantic supervision middle-layer formation](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/15_13_semantic_supervision_middle_layer_formation_anchor.md)

Frozen Protocol: [protocol.md](protocol.md), registered revision `20260907-P4-v1`; the execution amendment is recorded at the end of that file.

Detailed record: [detailed.md](detailed.md)

Result status / eligibility: `COMPLETE`. Both registered weak arms (seeds 17 and 29) completed 512 updates and passed all formal eligibility guards. The two earlier failed smoke attempts are excluded as `INELIGIBLE`; the successful result is bounded to the actual ACP worker label `N6LS-80G-SXM5` (one 80-GB GPU), as recorded in Detailed.

## 1. Purpose

Test whether reducing the parent/child semantic auxiliary weight from 0.5/0.5 to 0.25/0.25 repairs the P3 seed reversal, while separating reduced supervision harm from a genuine net semantic-supervision benefit.

## 2. Hypothesis

If the P3 reversal is caused by an overly strong semantic auxiliary objective, `H-sem-weak` should have lower development answer NLL than current `H-sem` in both seeds. A stronger claim additionally requires `H-sem-weak` to beat matched task-only `H-task` in both seeds; the live rival is that changing the weight does not repair the seed-dependent mechanism.

## 3. Analysis Method

- Compare `H-sem` minus `H-sem-weak` at update 512 separately for seeds 17 and 29; positive paired effect means the weak arm reduces harm relative to current semantic supervision.
- Compare `H-task` minus `H-sem-weak` under the same protocol; positive effect in both seeds is the separate criterion for replicated net semantic benefit.
- Compute per-record, source-stratified paired bootstrap intervals (2,000 draws, NumPy seed `20260907`) on the 8,481-record development split; test each conjunction without pooling seeds.

## 4. Conclusion

Protocol-typed verdict: `HALF_WEIGHT_REPAIR_NOT_REPLICATED`. This is the registered result reading; the researcher still owns the Focus-level wording and next scientific decision.

1. **The 0.25/0.25 weight did not reduce harm in both seeds.** At update 512, seed 17 gave `H-sem − H-sem-weak = -0.001374` with 95% paired interval `[-0.001529, -0.001214]`; seed 29 gave `-0.0000475` with `[-0.000142, 0.0000474]`. Positive favors the weak arm, so the harm-reduction conjunction fails.
2. **There was no replicated net semantic benefit.** The task-only contrast was positive in seed 17 (`+0.008722 [0.008222, 0.009244]`) but negative in seed 29 (`-0.002357 [-0.002732, -0.001971]`). The benefit contrast cannot rescue the failed harm-reduction conjunction.

### Important Figure

![P4 harm-reduction and semantic-benefit effects](</data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/p4-weight-20260907T024100Z/figures/weight_localization_effects.png>)

How to read: the horizontal axis is baseline NLL minus weak-arm NLL (positive favors `H-sem-weak`); at update 512 the orange harm contrasts are not positive in both seeds, and the blue task contrasts reverse sign across seeds. The figure cannot establish a global optimal weight, a population seed effect, expert function, or free-generation/general-benchmark benefit.

### Claim Boundary

Can claim: in this frozen Qwen3-0.6B, block-14, load-off, development-only realization, the exact 0.25/0.25 weak arm did not replicate a two-seed repair of the P3 reversal, and did not show a two-seed net semantic benefit. The two formal arms and their guards are eligible for this bounded claim.

Cannot claim: that semantic supervision is generally harmful or beneficial; that 0.25 is globally optimal; that P3 becomes positive; that GMM pseudo-labels are semantic truth; that routing is functionally necessary; or that the result transfers to test, free generation, deployment, or uncontaminated public benchmarks.

### Next Step Analysis

Decision: **AI 建议 — stop the weight-only explanation for this exact 0.25 repair and have the researcher choose whether to close this branch or register a different mechanism test.**

Why it follows: neither required harm contrast is positive in both seeds, and the task-only contrast reverses sign, so adding more weights or silently pooling seeds would not answer the registered question.

Unresolved uncertainty: the cause of the P3 seed reversal remains open; this P4 does not distinguish other supervision, routing-path, load, or optimization mechanisms.

Completion criterion: the researcher confirms the bounded result, cannot-claim boundary, and exactly one next decision in the active Focus.

Resume action: update the Focus and Anchor only after that confirmation; any new experiment must receive its own frozen Protocol and execution approval.
