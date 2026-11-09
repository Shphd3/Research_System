# Protocol: A15_13_E09 M2D2 Baselines And Last-Layer Pseudo-Label Routing

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN_ANALYSIS
Approval status: HUMAN_CONFIRMED on 2026-09-02
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: implementation, tests, smoke, two-seed full run, reuse-only evaluation of E07/E08, analysis, curated result records
Design frozen at: 2026-09-02 before implementation
Purpose: compare semantic hierarchy against simple post-training baselines and test whether unsupervised labels from the frozen final layer can train a functional causal Router
Primary Anchor: 15_13_04_m2d2_causal_lm_semantic_routing_anchor.md
Experiment role: method construction and matched-baseline audit
Primary metric: equal-domain confirmation NLL in nats per target token; lower is better
Treatments: direct-nine-class hierarchy and final-layer direction-plus-radius pseudo-label hierarchy
Controls: frozen Base, one rank-24 adapter, rank-24 flat leaves, flat gold routing, reused learned task-only/gold/shuffled hierarchies, and reused hard Oracle controls
Changed variables: routing topology and route-supervision source
Held fixed: M2D2 windows, frozen Qwen3-0.6B-Base, block-14 intervention, token objective, target mask, updates, optimizer, seeds, and confirmation split
Pass: a treatment beats the strongest trained simple baseline on NLL in both seeds with positive paired lower confidence bound and also passes route-semantic and expert-intervention gates
Fail: eligible evidence misses the strict NLL gate or either functional gate
Insufficient: any required seed, condition, causal guard, pseudo-label leakage guard, per-window loss, or intervention is missing
Cannot claim: online clustering, abstract semantics beyond topical/domain structure, full-model-training gains, or parameter-matched superiority of literal rank-24 flat leaves
```

## 1. Definitions

The **frozen final-layer output** is `hidden_states[-1]` returned by the frozen Qwen3-0.6B backbone after its final normalization. A window representation is the arithmetic mean over all 256 causal token states. It is an offline teacher object: it may generate a training label but never enters the block-14 Router forward path.

A **direction-plus-radius pseudo label** is a cluster assignment from the normalized direction and log norm of a train-only rank-64 principal-component representation. A **causal Router** reads only the uncentered block-14 state at the position that predicts the next token. **Active rank** is the sum of ranks traversed by one token; it is not total stored adapter rank.

## 2. Anchor Alignment And Rivals

E07 established semantic routes and non-interchangeable children without learned NLL recovery. E08 established small hard-Oracle semantic value. E09 tests the remaining practical rival: ordinary or flat parameter-efficient post-training may preserve NLL better, while pseudo labels may merely copy topic clusters without producing useful experts.

The experiment does not replace or rewrite E07/E08. Their frozen checkpoints and evaluation arrays are reused byte-for-byte and remain governed by their original Protocols.

## 3. Data And Leakage Boundary

Use the existing SHA-recorded M2D2-Wikipedia balanced 3-by-3 cache: 1,024 train, 256 development, and 512 confirmation windows per fine domain, sequence length 256, with targets 64--255. Domain names are never rendered into input. Confirmation truth is never used for clustering, restart choice, checkpoint choice, or training.

The pseudo-label teacher extracts final-layer window means from TRAIN only. The clustering algorithm receives no coarse or fine label. Gold TRAIN labels may be used only after fitting to compute a Hungarian permutation for reporting semantic agreement; that mapping cannot change labels, model training, or method selection. Development and confirmation assignments use frozen train-fitted parameters and are diagnostics only.

## 4. Final-Layer Direction-Plus-Radius Clustering

Fit a train-only PCA basis of rank 64 to final-layer window means. For projected vector \(z\), define direction \(u=z/\lVert z\rVert_2\) and radius \(r=\log(\lVert z\rVert_2+10^{-8})\). Each cluster has a unit direction \(\mu_k\), shared directional concentration \(\kappa\), radial mean \(m_k\), radial standard deviation \(s_k\), and equal prior. Responsibilities are proportional to

\[
q(k\mid z)\propto
\exp(\kappa\mu_k^\top u)
\,\mathcal N(r;m_k,s_k^2).
\]

First fit three coarse clusters. Within each assigned coarse cluster, fit three child clusters. Use 20 deterministic restarts per fit, at most 100 expectation-maximization iterations, convergence tolerance \(10^{-5}\) in mean log likelihood, radius standard-deviation floor \(10^{-3}\), and choose the restart with maximum TRAIN likelihood. Empty clusters are a fit failure, not silently repaired with gold labels. Save PCA, mixture parameters, responsibilities, assignments, restart traces, and input hashes.

This realizes the A15.14 result that whole-window semantics are direction-primary and radius-contributing. Direction-only von Mises--Fisher and full diagonal Gaussian assignments are saved as secondary label diagnostics; covariance is not part of the primary pseudo-label claim.

## 5. Architectures And Objectives

All original Qwen parameters and the language head remain frozen. Every added module enters zero-indexed block 14.

- `DENSE_R24`: one rank-24 adapter, active for every token, trained only by next-token cross-entropy.
- `FLAT_TASK_R24`: nine rank-24 leaf adapters, hard top-1 learned Router, selected residual scaled by its learned probability, trained only by next-token cross-entropy.
- `FLAT_GOLD9_R24`: the same flat model plus unit-weight cross-entropy to the gold nine-way fine-domain label.
- `HIER_DIRECT9`: shared, three parent, and nine child rank-eight adapters; one global nine-way Router selects a leaf and its parent in one stage, with unit-weight gold nine-way route cross-entropy.
- `HIER_PSEUDO_DR`: the E07 staged rank-eight hierarchy. Stage one uses the three pseudo coarse labels. Stage two freezes the coarse Router and parent experts and uses the parent-conditional three-way pseudo child labels.

For route-supervised conditions,

\[L=L_{\mathrm{NTP}}+L_{\mathrm{route}},\]

and route loss updates only Router parameters. Language loss updates the active adapter path and any differentiable selected-probability coefficient. No load-balancing, prototype, contrastive, reconstruction, representation, or expert-classification loss is allowed.

Literal rank-24 flat leaves match per-token active rank but store more adapter parameters than the hierarchy. They are a deliberately strong topology baseline; no total-parameter-matched superiority claim is permitted.

## 6. Optimization, Reuse, And Execution

Seeds are 17 and 29. AdamW uses learning rate `3e-4`, weight decay `0.01`, gradient clipping `1.0`, five-update warmup, and cosine decay. Microbatch is 8 with accumulation 16. Dense, flat, and direct-nine conditions run four complete TRAIN passes, 288 optimizer updates. The pseudo hierarchy runs 144 coarse-stage updates and 144 fine-stage updates. Fixed final checkpoints are primary; development does not select another checkpoint.

Reuse root:

`/data/250010109/MoE_Router/experiments/20260901_a15_13_e07_e08_m2d2_causal_lm_semantic_routing/runs/full-20260901T174147Z`

No E07/E08 model is retrained. The new run stores immutable links or hashes to reused checkpoints and evaluation arrays. The approved resource is one reserved four-H100 ACP node, one process per GPU, with independent one-GPU arms and no distributed training.

## 7. Comparisons And Frozen Analysis

The primary table reports equal-domain confirmation NLL for Base, `DENSE_R24`, `FLAT_TASK_R24`, `FLAT_GOLD9_R24`, `HIER_DIRECT9`, reused `LEARNED_TASK_ONLY`, reused `LEARNED_SEMANTIC`, `HIER_PSEUDO_DR`, and reused hard Oracle controls.

The strict method contrast is strongest trained simple baseline minus each semantic hierarchy. Use 10,000 paired bootstrap draws, resampling windows within each of nine domains and preserving seed/condition pairing. Positive values favor the hierarchy. No post-hoc non-inferiority margin is allowed; a numerically small negative effect is reported as near-baseline descriptively but remains a strict NLL Fail.

Route semantics are normalized mutual information and Hungarian-matched macro F1 against held-out gold domains. Expert function requires positive confirmation NLL increase in both seeds and a positive pooled 95% lower bound for both deleting the active expert and replacing it with another eligible expert. These diagnostics cannot rescue strict NLL Fail.

Required figures are: primary NLL with a shared axis; paired NLL contrasts with confidence intervals; route NMI/F1; and expert deletion/replacement costs. Every figure must use the same condition names as the table.

## 8. Stage Contract And Stop Rules

1. **Preflight:** verify old artifacts, data hashes, last-layer extraction shape, train-only fit boundary, parameter counts, route-loss gradient isolation, and future-token invariance of the block-14 Router. Failure stops all training.
2. **Smoke:** one short update per new topology plus one pseudo coarse/fine transition; require finite loss, unchanged frozen weights, correct trainable sets, nonempty clusters, and complete artifacts. Smoke never contributes scientific evidence.
3. **Full run:** extract teacher states once; freeze pseudo labels; train only new conditions; evaluate intact and required interventions; merge old evaluations read-only; analyze after every required artifact exists.

Expected worker root:

`/data/250010109/MoE_Router/experiments/20260902_a15_13_e09_m2d2_baselines_last_layer_pseudolabel/`

Expected canonical records are this Protocol plus adjacent `summary.md`, `detailed.md`, `figures/`, and `tables/`. Raw checkpoints, caches, logs, and per-window arrays remain in the worker root.

## 9. Confirmation And Freeze Ledger

| Block | State |
| --- | --- |
| A question and boundary | CONFIRMED |
| B data and provenance | CONFIRMED |
| C task and supervision | CONFIRMED |
| D architecture | CONFIRMED |
| E objective and optimization | CONFIRMED |
| F comparisons and evidence | CONFIRMED |
| G execution and reproducibility | CONFIRMED |

Cross-block consistency: `PASS`. Implementation, smoke, full run, and analysis were explicitly approved by the researcher on 2026-09-02. Any material post-start change is append-only and records eligibility impact.
