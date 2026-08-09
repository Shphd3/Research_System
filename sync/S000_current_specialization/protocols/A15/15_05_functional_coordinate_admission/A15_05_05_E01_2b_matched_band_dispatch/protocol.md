---
experiment_id: A15_05_05_E01_2b_matched_band_dispatch
status: completed_fail_distribution_only
created: 2026-07-31
approval_date: 2026-07-31
primary_anchor: 15_05_05_matched_fixed_band_dispatch
chinese_companion: protocol_cn.md
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
resource_profile: 5090-8-spot
result: summary.md
---

# Protocol: Nine-Arm Matched 2B Band-Dispatch Training

## 0. Approval Snapshot

**Execution outcome (2026-07-31):** all nine arms completed step 2,544
(2.000683B nominal tokens). Every true band changed frozen-token dispatch, but
all four had strictly worse paired held-out NLL than native. Head beat
random64 but not native; middle and middle+tail lost to their random controls;
tail was indistinguishable from random448. The registered verdict is
**Fail / distribution-only**. See [summary.md](/Projects/from-attention-to-search/main/experiments/A15/15_05_functional_coordinate_admission/A15_05_05_E01_2b_matched_band_dispatch/summary.md).

The researcher explicitly authorized implementation, multiple 8x5090 jobs,
and complete 2B training without another approval stop. This is a new causal
ablation, not an unlock of the failed old compatibility-gated experiment.

## 1. Terminology / Definitions

Band-only means the Gate sees only frozen-band token variation while experts
receive the full representation. H/M/T/N are ranks 1--64, 65--320, 321--768,
and 65--768. Each has an independent equal-rank Haar control. Matched branch
means identical model, optimizer, scheduler, data cursor, and RNG at step 800.

## 2. Anchor Alignment

The primary metric is 2B DCLM held-out NLL. Fixed-token route disagreement is
a required manipulation check and cannot substitute for quality.

## 3. Tested Hypothesis

At least one true band changes dispatch and lowers held-out NLL relative to
both native and its equal-rank random control. Routing change without NLL gain
is a valid distribution-only result.

## 4. Rival Explanations

Equal-rank random controls generic reduction; load/overflow/drop controls load
artifacts; common branch/data/measured FLOPs control initialization and compute;
frozen/current overlap checks spectral identity.

## 5. Data / Model / Algorithm / Objective

Train on DCLM shard 01 and evaluate on 1,024 independent DCLM held-out
documents. WOS domain/topic test abstracts are diagnostic only. Use H768,
four layers, eight sparse plus one shared expert, top-1, running center,
$\lambda_{LB}=0.01$, sequence 1024, local batch 12/GPU, eight GPUs,
accumulation 8, global batch 768, AdamW LR $10^{-4}$, weight decay 0.01,
636-step warmup, and the established 100B scheduler horizon.

Resume the common step-800 branch (629,145,600 tokens) and stop at step 2544
(2,000,683,008 nominal tokens). Estimate and freeze per-layer actual-input
$P,\mu$ at the branch. Implement

$$z=W\mu+(WP)(r-\mu),$$

which is algebraically identical to projecting the Gate input while keeping a
full-shaped Gate and matched token-level Gate FLOPs.

## 6. Conditions, Seeds, And Checkpoints

Nine arms: native; H64/R64; M256/R256; T448/R448; N704/R704. Registered
checkpoints are 800, 954, 1272, 1908, and 2544. One paired branch seed gives a
strict causal ablation for this branch, not cross-initialization replication.

## 7. Primary Metric

$$\Delta L_{a:b}=L_a^{heldout}(2B)-L_b^{heldout}(2B).$$

Compare every true arm with native and its corresponding random arm on the
same held-out documents using 2,000 paired document bootstraps. This establishes
branch-specific benefit/harm, not a scaling law.

## 8. Secondary Metrics

Fixed-probe expert disagreement, margin, load/entropy/overflow/drop; WOS
$p(e\mid domain/topic)$, condition JS distance, and label predictability;
expert parameter displacement per routed token; frozen/current band overlap;
and held-out loss-token AUC. These explain routing paths but cannot replace NLL.

## 9. Known Good / Known Bad / Known Confusing Cases

Native identity must replay logits/top-1. Every projector must be symmetric,
idempotent, and have registered rank. Large route divergence with unchanged
NLL is functional failure, not measurement failure. Random improvement is
generic reduction, not spectral benefit. WOS purity is not LM utility.

## 10. Stage-Level Profiling Plan

S0 hashes; S1 basis and algebraic no-op; S2 two-step resume smoke; S3 nine-arm
submission and milestone monitoring; S4 DCLM/WOS/routing/expert evaluation;
S5 paired verdict and knowledge update.

## 11. Runtime And Resource Contract

One ACP job per arm: workspace `share-space`, AEC2
`computing-cluster-5090-01g`, spec `n12lp.nn.i10a.8`, one node, eight RTX5090,
spot, normal priority, fixed Blackwell image. Queue/sequential completion is
allowed; debug cluster or shortened endpoint is forbidden.

## 12. Pass / Fail / Insufficient

Band-specific Pass requires manipulation plus a 2B NLL paired upper bound
below zero against native and equal-rank random with compute/load guards.
Distribution-only means routing changes without NLL advantage. Generic
reduction means true/random similarity. Precise non-benefit/harm for all true
arms is Fail. Failed resume, completion, evaluation, compute/load, or basis
guards is Insufficient.

## 13. Output Contract

Job IDs, hashes, logs, document NLL, routing/load/domain/topic/expert tables,
central figures, summary/detailed records, and an experiment-named Chinese
five-section knowledge update. No graph/root-sync/commit/push.

## 14. Claim Boundary And Next Decision

Claims are restricted to one H768 four-layer DCLM branch seed at 2B tokens.
No fixed covariance-rank arm merits cross-seed replication under the registered
benefit rule. Close band-only dispatch and require a directly functional
expert-update or task-utility admission gate before another large training.
