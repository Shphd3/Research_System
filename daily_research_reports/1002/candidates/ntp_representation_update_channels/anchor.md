# Temporary Anchor: sharing utility for better MoE routing and architecture

Updated 2026-10-03, routing-r2. This refines the same question in the original temporary location; no formal project or new Focus. The researcher names MoE improvement as the aim; spectra and SAE are tools. [Current authorization](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/receipts/user_authorization.json) and [prior owner snapshots](history/20261003_before_routing_refinement/) preserve scope and history.

## 1. Problem Definition

When should inputs share parameter updates, and when should they use separately learned experts, to improve acquisition and retention under limited resources? The immediate gap is whether a target-blind router can use input information to choose expert updates with lower actual loss, rather than merely predict update responses with lower mean squared error.

Training-time sharing determines which examples update common parameters; inference routing selects existing computations. This round connects finite utility of frozen candidate updates to the existing architecture comparison without equating local selection with long-run sharing benefit. States: task IN_PROGRESS, question OPEN, design STAGED_EXPLORATORY_AMENDMENT, result PARTIAL_PRIOR_EVIDENCE_NEW_CHECKS_PENDING. Concrete analyses are AI-selected within explicit authorization; practical thresholds remain Unknown.

## 2. Physical Priors

Working hypotheses, not universal language laws: tasks may reuse structure while responding differently to one common update. Sharing can save repeated storage or improve estimation by pooling data, while old experts may depend on the previous common computation. Actual old-task effects therefore matter.

The routing model assumes a fixed expert bank and input distribution, integrable finite losses, and decision information available before the future target. Expert retraining, coupled capacity constraints and long-horizon learning need separate evidence.

## 3. Falsifiable Hypotheses

H1: differences readable from the prefix improve finite-CE choices among frozen candidate expert updates. The strongest rivals are merely rejecting updates on vulnerable inputs or preferring one globally stronger expert. A gain that vanishes without rejection or after matching action usage does not establish useful source matching.

H2: a router may use decision-relevant information while each expert retains the full layer input. Lossless compression must retain at least one pointwise optimal action for the current expert bank; target sufficiency alone is not enough. Mathematical conditions and counterexamples constrain the claim. A particular compression still requires empirical utility evidence.

The prior architecture hypothesis remains open: common computation and serial coupling may improve finite-budget acquisition/retention. That queued experiment is neither replaced nor pre-adjudicated by H1.

## 4. Mathematical Model

H is the causal state available before routing; Z=φ(H) is the router observation. The abstract model allows experts to retain full H. Actual complete module input is interface-relative: the residual matrix here reads c while the shared tail retains r. Action a denotes a candidate computation/update, with conditional risk Q_a(H)=E[ℓ_a(H,Y)|H]. Then

\[
R_H=\mathbb E\min_a Q_a(H),\qquad
R_Z=\mathbb E\min_a\mathbb E[Q_a(H)\mid Z]\ge R_H.
\]

Equality requires a Z-measurable selector that remains pointwise optimal. Information sufficient to predict the target need not identify which frozen expert errs. A common task loss does not require router and experts to receive identical representations or learn identical functions.

For learning, first isolate a precise local comparison: the new source uses w+δ under both schemes; old tasks use either w+δ or the original w. Shared minus separate risk is exactly the weighted old-task finite loss change. Gradient inner products are only small-step approximations. Copying cost, curvature, optimizer state and future updates remain separate, so inference selection and training sharing cannot be interchanged.

## 5. Computational Realization

The minimal test reuses actual finite S7 interventions: common output a₀=W₀c and candidate residual experts −ηM_dc, each receiving full c. Existing target-blind predictors use causal lexical features, optionally augmented with SAE/PCA/random projections. Select the predicted action and read its measured finite CE, retaining the true norm/MLP/head tail. Derivative scores are not measured CE; averaging action losses is not averaging parameter updates.

This is a local conditional residual architecture after the final Attention output, not a newly trained MoE. SAE encoding, routing and multiple stored matrices have costs. The exact-33B Dense/S7/SALL panel is now registered and submitted, comparing pre/post-projection and residual information. It is a within-state check with descriptive cross-state replication, not an architectural causal effect.

## 6. Minimal Falsification Tests

At most three necessary evidence activities remain active: inspect the existing architecture trajectories and checkpoint interventions; reuse actual finite-action tables to evaluate frozen or FIT-only-fitted routing rules; test information/routing on a new fixed panel across equal-token model states. The third scope is frozen in the Protocol before execution, not automatically expanded into a training sweep.

The primary routing quantity is actual CE difference at selected token positions, in nats. Compare a fixed expert chosen on F, a target-independent random selector with the same action usage, and source selection without rejection. Report both source-transfer directions and every receiving domain. Consistent improvement supports this bounded selection; absent/reversed gains weaken this operationalization; state/source inconsistency or identity/numerical failures yield insufficiency. No post-hoc usefulness threshold is invented.

## 7. Current Evidence

Finite selection on the old S7 panel and the declared post-hoc group decomposition are complete. SAE gains over the FIT-fixed expert are 3.391/−5.788 micro-nat for A→B/B→A, with both conditional intervals crossing zero; category-matched random controls also leave no stable positive residual. Ordinary random projections retain some positive utility, so local gains are not specific to SAE. The old panel was exposed, and fixed gradient actions are not jointly trained full MoE experts. The [round report](sharing_routing_report.md) preserves all conditions and boundaries.

The additional pooled-four-action study completed eight input families, 16 pooled conditions and 80 receiving-scope rows. Every feature-added family beats category-usage random allocation, yet no pooled condition stably beats the finite-FIT-fixed action; the full-input fitted linear rule does not dominate lower-dimensional representations. Its bank, labels and baseline differ from the preceding study, so between-study numerical differences do not identify input effects.

Theory separates equal function families from functional trajectories, statistical pooling from serial structure, and present computation selection from future learning allocation. A bank with no initial selection utility can develop useful differences under causal training allocation. This is a restricted analytical counterexample, not a confirmed natural-text mechanism. A same-data, equal-conditional-step quadratic model further shows that mean-gradient heterogeneity must outweigh curvature and estimation noise; those population quantities have not been estimated for NTP.

Existing logs support lower fresh-S7 training CE in specified intervals, without establishing lower cost to reach a quality target. Later Dense/S7 window data overlap strongly but updates are not paired. The old 21B classification probe completed, but does not establish general downstream ability. At 10:44 UTC both 8×5090 SPOT tasks were STARTING / worker Pending, without new GPU qualification or training results; timestamped receipts govern subsequent execution state.

## 8. Claim Boundary And Next Decision

Faster training-loss decline, better downstream performance, superior compressed routing and a better overall sharing method are unestablished. Static separability, finite routing utility, full-trajectory efficiency and downstream value each need matched evidence; an open bridge does not refute a bounded result.

Next decide whether target-blind input information improves actual finite selection beyond rejection and fixed-expert preference. Local completion requires all frozen comparisons with source/domain boundaries to judge this particular selector. Read the existing architecture experiment independently for acquisition and retention; success of the local selector is not a prerequisite for studying learned allocation. Keep the temporary location and scientific question open.
