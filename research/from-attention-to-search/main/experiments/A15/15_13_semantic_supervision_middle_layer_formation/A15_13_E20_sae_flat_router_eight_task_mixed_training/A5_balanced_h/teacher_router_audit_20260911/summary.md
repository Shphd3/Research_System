# A5 teacher → router audit

[中文阅读](summary_cn.md) · [Protocol](protocol.md) · [Detailed evidence](detailed.md) · [Ranked text examples](teacher_examples_cn.md)

Status: both authorized audit steps completed locally. Interpretation is AI audit assessment awaiting researcher confirmation; no Focus or Anchor scientific transition. No experts, backbone or SAE were trained.

## Purpose

Locate whether A5 has an unreliable teacher or a teacher-to-linear-router imitation gap before considering expert explanations.

## Hypothesis

A usable coactivation teacher should retain nonrandom held-out structure under grouping perturbations. A fixed-h linear router should reduce teacher KL and transfer its fit to held-out records. Semantic coherence, class balance and useful expert specialization do not follow automatically.

## Analysis method

- Authenticate A5 inputs; replay five grouping seeds and three full-record bootstraps, inspect activation-ranked texts, and compare twenty size/frequency-matched random groupings on the same held-out edges.
- Reevaluate three original offline routers on train and validation. Fit one fresh affine 1024→8 router with KL only for twenty epochs, frozen h/q, no expert computation and no validation checkpoint selection.
- Separate token-weighted agreement, per-group recall and teacher-margin strata; do not count correlated tokens as independent experiments.

## Conclusion

1. **The teacher has reproducible coactivation structure, but is not a validated eight-class semantic taxonomy.** Five-seed feature ARI is 0.999793–1.000000; three record-bootstrap ARIs are 0.731208–0.779742, with aligned token argmax agreement 95.89–97.18%. Held-out within-minus-between phi is 0.059252, versus −0.003417 to −0.000051 for twenty matched random groupings. Ranked examples expose lexical continuations and math/code formatting; some groups lack a defensible unified semantic label. This bounded result justified testing imitation, not certifying semantic categories.

![Teacher audit](figures/teacher_audit.png)

How to read: seed stability, held-out structure advantage, and concentrated target usage answer different questions. Groups1/3 hold 98.59% of validation argmax targets; imbalance alone is not a failure.

2. **A gross train-to-validation generalization failure is not observed.** The fresh router obtains train/validation KL **0.046010/0.046495**, and argmax agreement **92.15%/91.91%**. Validation constant-prior KL is 0.212122 and majority accuracy is 56.48%. Original seed17 was already 0.055356/0.055616 KL and 90.52%/90.40% agreement. Training fits are not perfect and twenty epochs do not establish a global optimum.

![Router audit](figures/router_audit.png)

How to read: close train/validation curves oppose gross overfitting, while per-group recalls reveal heterogeneous imitation. For teacher top-two probability gap ≥0.1, validation agreement is 98.18%. Group7 has zero training argmax positives and only two validation positives, although its mean training soft mass is nonzero (0.006146). Its zero recall is not evidence of intrinsic capacity failure. Macro recall on the SAME seven supported groups is 63.41% train / 65.65% validation; the all-eight validation value 57.44% has a different denominator.

Boundary: fixed-dictionary grouping stability is not independent SAE-training-seed stability. Text interpretations are ranked-example observations, not blind semantic validation. No inference about task-loss superiority, forced teacher paths or expert utility was tested.

AI next-decision proposal: decide whether the intended teacher is a reproducible lexical/formal coactivation partition or a semantically named partition. The latter still needs explicit content validation; these results do not justify declaring the linear router incapable or expanding expert training.
