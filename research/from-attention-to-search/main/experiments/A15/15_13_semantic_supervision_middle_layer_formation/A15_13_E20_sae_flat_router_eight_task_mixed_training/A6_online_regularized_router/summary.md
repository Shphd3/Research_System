# Summary: A6 Online SAE/GMM Router Regularization

Primary Anchor: [A15_13_10](../../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_10_sae_flat_router_functional_anchor.md)  
Frozen Protocol: [A6 Protocol](protocol.md)  
Detailed record: [A6 Detailed](detailed.md)  
Result status / eligibility: `ELIGIBLE_MEASUREMENTS`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.

## 1. Purpose

Test whether a frozen initial eight-group structure from an SAE or token-level
GMM improves answer prediction when the Router and low-rank experts learn
jointly, compared with an otherwise matched task-only Router.

## 2. Hypothesis

At least one teacher/constraint combination should lower final internal-test
answer-token NLL relative to task-only in all three matched seeds. The strongest
rival is that ordinary task gradients already provide the useful routing
adaptation, or that preserving the initial structure obstructs task learning.

## 3. Analysis Method

- Compare each new condition with the same seed's reused task-only trajectory
  at fixed update 512; initialization, sample schedule, task objective, model,
  and internal-test records are held fixed.
- Compute NLL as total answer loss divided by total answer tokens within each
  seed, then report the equal-weight mean and sample SD over seeds 17/29/43.
- Apply the registered descriptive rule: only three negative
  `new minus task-only` deltas count as a directionally consistent advantage;
  any positive delta rejects that all-seed advantage.

## 4. Conclusion

Verdict: **the registered support criterion was not met.** All four online
regularization conditions were worse than task-only in every matched seed.
The best new condition, SAE-B, had mean test NLL `0.702514 ± 0.000164` versus
task-only `0.696579 ± 0.000782`; its seed-level deltas were `+0.004851`,
`+0.006386`, and `+0.006570` nats/token (`+0.005936 ± 0.000943` on average;
positive is worse).

| Condition | Test NLL mean ± sample SD | Mean delta vs task-only ± sample SD | Seed 17 / 29 / 43 deltas | Registered reading |
| --- | ---: | ---: | --- | --- |
| Task-only | 0.696579 ± 0.000782 | 0 | 0 / 0 / 0 | Baseline |
| SAE-A | 0.703717 ± 0.000761 | +0.007139 ± 0.001541 | +0.005371 / +0.007846 / +0.008199 | No all-seed advantage |
| GMM-A | 0.705128 ± 0.000089 | +0.008549 ± 0.000753 | +0.007693 / +0.008845 / +0.009110 | No all-seed advantage |
| SAE-B | 0.702514 ± 0.000164 | +0.005936 ± 0.000943 | +0.004851 / +0.006386 / +0.006570 | No all-seed advantage |
| GMM-B | 0.704372 ± 0.001801 | +0.007793 ± 0.002576 | +0.004822 / +0.009399 / +0.009158 | No all-seed advantage |

Source: [condition means and paired seed deltas](tables/condition_means.csv),
derived in float64 from the authenticated per-record test sums. The frozen
aggregate's float32 calculation agrees within `4.11e-8` nats/token.

![Fixed-update internal-test NLL](figures/test_nll.png)

How to read: each colored point is one independent training seed at update
512; lower is better, and the black mark is mean ± sample SD. Every colored
point for every online-regularized condition lies above its matched task-only
value. This figure establishes the registered internal-loss comparison only;
it does not establish why the regularizer hurt.

### Claim Boundary

Can claim: under this final-layer, eight-expert, 512-update, fixed
`lambda=0.1` internal-holdout configuration, none of the four SAE/GMM online
regularizers demonstrated a stable task-loss benefit over matched task-only
training.

Cannot claim: that every SAE/GMM teacher or regularization strength is
ineffective; that the groups are or are not true semantic classes; that expert
utility has been established by intervention; or that the ranking transfers
to clean official or external generation benchmarks. The experiment also
lacks a random structural teacher, so it cannot isolate semantic structure
from generic regularization.

### Next Step Analysis

Decision: **AI suggestion — do not advance any A6 arm to external evaluation;
close this fixed `lambda=0.1` online-regularization configuration. Researcher
confirmation is pending.**

Why it follows: the primary fixed-checkpoint criterion failed in all 12 paired
comparisons, including the best new arm.

Unresolved uncertainty: the evidence does not distinguish a harmful structural
prior from excessive or persistent structural-gradient pressure at this single
coefficient.

Completion criterion: the researcher confirms or replaces this one decision
while preserving the measured result and claim boundary.

Stop or redirect condition: if mechanism diagnosis remains important, return
to the Anchor and register one minimal discriminator before any additional run;
do not begin a coefficient sweep from this result record.

Resume action: complete the Researcher Judgment Gate below, then align the Anchor and
active Focus to the confirmed judgment.

### Researcher Judgment Gate

```text
Question: Did any registered A6 condition provide an all-seed task-loss advantage?
Direct result: No; all 12 new-minus-task-only deltas are positive.
Confirmed: AWAITING_RESEARCHER
Weakened or rejected: AWAITING_RESEARCHER
Current mechanism and reason: AWAITING_RESEARCHER
Cannot claim: AWAITING_RESEARCHER_CONFIRMATION_OF_BOUNDARY_ABOVE
Exactly one next decision: AWAITING_RESEARCHER; AI suggestion is stated above.
```
