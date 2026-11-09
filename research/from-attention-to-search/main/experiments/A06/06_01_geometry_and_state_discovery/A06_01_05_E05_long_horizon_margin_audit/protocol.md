# Protocol: A06_01_05_E05 Long-Train Margin Audit

## 0. Approval Snapshot

Approval status: user requested immediate implementation and completion.

Purpose: Test whether the full-LM embedding-gradient margin failure observed
at 160 post-reinit steps is merely a short-training artifact.

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Anchor decision question: Can embedding-gradient selection identify
feature-relevant hidden states under full-sequence LM loss?

Anchor physical prior tested: raw full-LM gradients contain feature signal, but
neutral-token prediction noise may make the selected state pool margin-thin.

Anchor core model term tested: post-reinit margin preservation under extended
training.

Anchor falsifier: embedding-gradient top-k remains negative-margin or degrades
while route-position and oracle controls remain positive-margin.

Experiment role: long-train robustness audit, not a new method construction.

Primary metric from anchor: feature NMI after router reinitialization and
after extended post-reinit training.

Claim boundary from anchor: synthetic uniform no-position bridge only.

Minimal setup: same one-layer causal Transformer, one weighted top-1 MoE layer,
no position embeddings, four uniformly sampled features, repeated feature
slots, neutral background, and feature-specific target token as A06_01_05_E05.

Basic configuration: full-sequence LM loss only, warmup 40, seeds 0--7, slot
lengths 1/2/4/8, post-reinit checkpoints 0/160/500/1000/2000.

Conditions to run: no-reinit, all-position centered, route-position centered,
oracle centered, embedding-gradient top-1/top-4/top-8 centered.

Pass: embedding-gradient top-k recovers positive margin p05 and stable feature
NMI by 2000 steps while controls stay valid.

Fail: embedding-gradient top-k keeps negative margin or worsens while
route-position/oracle controls stay strong.

Insufficient: route-position or oracle controls fail, the full seed/slot grid
does not complete, or outputs are missing the 2000-step checkpoint.

Cannot claim: real-DCLM transfer, semantic experts, rare-feature routing,
expert utility, or a new denoised selector.

Approval decision: execute a tiny local smoke using the existing A06_01_05_E05 runner,
then submit a four-GPU remote full run.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Full-sequence LM loss | Predict every next token | CE over all next-token positions | \(\mathcal L^{full}\) | Main loss whose gradient selector is audited | Real language semantics |
| Long-train audit | Extend post-reinit training beyond the original 160 steps | train to 2000 steps after router reinit | optimizer steps | Tests whether the margin failure is temporary | Global convergence |
| Embedding-gradient top-k | Select k positions per sample by embedding-gradient energy | top-k of \(\|\nabla_e\mathcal L\|^2\) | token positions | Candidate label-free state selector | Feature labels |
| Feature NMI | Agreement between feature id and routed expert | NMI(feature, route) | 0--1 | Primary separation metric | Utility |
| Margin p05 | Low-tail matched expert score gap | 5th percentile of target expert minus competitor score | logit gap | Stability guard | Optimality |

## 2. Anchor Alignment

Decision question: whether the full-LM gradient selector can become a stable
router initializer under longer post-reinit training.

Physical prior tested: if the raw selector only needs longer optimization,
margin should recover by 2000 steps. If the selected state pool is intrinsically
noisy, longer training should not rescue the low-tail margin while clean
controls remain stable.

Core model term tested: margin preservation:

\[
\mathrm{margin}(i)=s_{e^*(f_i)}(h_{r_i})-\max_{e\ne e^*(f_i)}s_e(h_{r_i}).
\]

Falsifier: gradient-selected methods fail margin p05 at 2000 steps while
route-position and oracle controls remain positive.

Claim boundary: synthetic balanced no-position bridge only.

## 3. Tested Hypothesis

H1: The A06_01_05_E05 full-LM margin failure is a short-training artifact.

Supported if: embedding-gradient top-1/top-4/top-8 regain positive margin p05
and maintain high feature NMI by 2000 steps.

Weakened if: NMI remains moderate/high but margin p05 stays negative.

Rejected if: route-position/oracle controls stay positive-margin while
gradient-selected methods remain negative-margin or degrade.

## 4. Rival Explanations

R1: Short training caused a transient margin dip.

R2: Raw full-LM gradient selection chooses a noisy hidden-state pool, so longer
training cannot create a stable feature margin from that initialization.

R3: Full-LM training itself destroys any feature partition. This is separated
by route-position and oracle controls.

## 5. Data / Model / Algorithm / Objective

Data, model, and objective are inherited from A06_01_05_E05.

Only one objective is run here: `full_lm`.

Only one warmup state is run: `warmup_step=40`.

Router inputs during training and evaluation are raw hidden states. Mean
subtraction is used only to construct initialization rows.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| oracle centered | clean upper bound | separates R3 | shows whether full-LM training can preserve true centers | primary control | positive margin at 2000 | negative margin | missing checkpoint | trajectory table |
| route-position centered | route-state proxy control | separates R2/R3 | shows whether label-free feature clustering is possible when route states are known | primary control | positive margin at 2000 | negative margin | missing checkpoint | trajectory table |
| all-position centered | baseline noisy pool | tests pool contamination | compares gradient selection to naive all-hidden pool | secondary | lower than gradient | stronger than gradient | missing checkpoint | trajectory table |
| embedding-gradient top-1 | best A06_01_05_E05 candidate | tests R1 vs R2 | asks whether raw selector recovers with longer training | primary | positive margin at 2000 | negative margin | missing checkpoint | trajectory table |
| embedding-gradient top-4/top-8 | top-k rescue hypothesis | tests whether more selected positions help | checks whether k expansion rescues margin | secondary | positive margin at 2000 | negative margin | missing checkpoint | trajectory table |
| no reinit | warmup-only baseline | baseline drift | shows ordinary full-LM warmup behavior | secondary | not decisive | not decisive | missing checkpoint | trajectory table |

Seeds: 0--7.

Slot lengths: 1, 2, 4, 8.

Checkpoints: 0, 160, 500, 1000, 2000.

## 7. Primary Metric

Primary metric: feature NMI at checkpoint 2000.

Guard metric: margin p05 at checkpoint 2000.

Why it decides: if longer training rescues the selector, both feature NMI and
margin p05 should improve. A high NMI with negative margin remains insufficient
because it indicates thin or unstable routing.

## 8. Secondary Metrics

- matched preserve fraction;
- max load;
- slot-start NMI;
- target accuracy;
- trajectory of feature NMI and margin p05 across checkpoints.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: oracle and route-position centered conditions should remain
positive-margin if feature geometry is still learnable under full LM.

Known bad: all-position centered and no-reinit are expected to be weaker.

Known confusing: embedding-gradient top-1 may have high NMI but negative
margin; this weakens but does not support the method.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| smoke | Does the parameterized runner work in a separate output dir? | tiny local run | produces summary.json and tables | smoke logs | no |
| full run | Did all seed/slot cells finish? | summary.json and runtime log | 32 cells, checkpoint 2000 exists | ACP logs | yes |
| result audit | Did longer training rescue margin? | aggregate final/trajectory tables | compare checkpoint 160 and 2000 | figures/tables | summary/detailed |

## 11. Algorithm Specification

Input: the existing A06_01_05_E05 runner and synthetic data generator.

Parameters:

- `--loss-modes full_lm`
- `--warmup-steps 40`
- `--train-steps 2000`
- `--checkpoints "0 160 500 1000 2000"`
- central methods only.

Steps:

1. Warm up the model for 40 full-LM steps.
2. Build router initialization rows for each condition.
3. Train each initialized model for 2000 full-LM steps.
4. Evaluate route-position feature NMI and margin at each checkpoint.
5. Aggregate over seeds and slot lengths.

Outputs: `summary.json`, aggregate tables, trajectory tables, central figures,
`summary.md`, and `detailed.md`.

## 12. Success / Failure / Insufficient Evidence

Success: at least one embedding-gradient top-k condition has positive margin
p05 at 2000 and maintains feature NMI close to route-position control.

Failure: embedding-gradient top-k conditions remain negative-margin at 2000
while route-position and oracle controls remain positive.

Insufficient evidence: missing full coverage or broken positive controls.

## 13. What This Cannot Claim

This run cannot claim a new selector, real language transfer, semantic experts,
rare-feature routing, or expert utility. It only audits whether the A06_01_05_E05
negative margin could be explained by too-short post-reinit training.

## 14. Review Notes And Protocol Changes

This is a narrowed continuation of A06_01_05_E05. It intentionally omits route-position
CE and hidden-gradient direction variants because the current uncertainty is
only the long-train behavior of the full-LM raw embedding-gradient selector.
