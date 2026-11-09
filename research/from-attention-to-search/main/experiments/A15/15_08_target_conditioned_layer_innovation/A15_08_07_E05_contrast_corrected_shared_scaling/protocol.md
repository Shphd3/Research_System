# Protocol: contrast-corrected local and directly learned shared functional subspaces

## Status

`APPROVED_FOR_FULL_RUN`

Human approval source: the researcher supplied and approved the complete redesign on 2026-08-21 and explicitly requested execution and corrected figures.

## A. Decision and claim boundary

This experiment decides whether held-out fine-class gain added by layer-local \(R_U\) is compressible below the softmax contrast ceiling, whether task-specific directions are reproducible yet distinct, and whether a directly learned shared input space expands as more domains are served. It does not estimate the intrinsic rank of the representation and does not establish Router utility.

## B. Frozen objects

- Model: frozen `/data/share/Qwen3-8B`.
- Layers: blocks 24 and 28.
- Input object: standardized \(R_U=U-\widehat E_{lin}[U\mid X]\) from the E03 train-fitted residualizer.
- Task: within each of eight parent domains, classify its eight child classes.
- Baseline: the frozen old-state \(X\) classifier.
- Primary metric: held-out cross-entropy gain over that baseline, in nats/example.

## C. Contrast correction

For a task with \(C\) classes,

\[H_C=I_C-\frac1C\mathbf 1\mathbf 1^\top.\]

The correction target and every fitted output map are projected as

\[T_{corr}=(Y-\widehat Y_X)H_C,\qquad B\leftarrow BH_C.\]

Mandatory invariants are \(\lVert B\mathbf1\rVert\le10^{-6}\max(1,\lVert B\rVert_F)\) and effective rank \(\le C-1\). A requested rank above \(C-1\) is rejected; outputs record requested and effective contrast ranks separately.

## D. Local functional dimension

For each domain and \(C\in\{2,4,6,8\}\), random balanced class subsets are frozen before confirmation. Ranks \(1,\ldots,C-1\) are fitted on TRAIN; ridge strength is selected on DEVELOPMENT. Let \(G_{p,r}\) be confirmation gain and \(G_{p,full}\) the full contrast-map gain. Define \(\rho_p(r)=G_{p,r}/G_{p,full}\) only when the simultaneous lower confidence bound of \(G_{p,full}\) is positive. The registered dimension is the earliest rank whose familywise 95% lower bound for \(\rho_p(r)\) is at least 0.90. Otherwise it is NA.

## E. Stability and overlap

Each local basis uses its registered \(r_{p,90}\). Report principal angles and normalized projection overlap for (i) two stratified TRAIN bootstraps of the same task and (ii) different tasks. Compare against an ambient-dimension-matched Haar baseline. A distinct-task claim requires same-task reproducibility to be materially larger than cross-task overlap.

## F. Shared-space methods

1. Independent local spaces: single-task oracle.
2. Local-space union SVD: oracle available only after local answers are known.
3. Direct joint shared learner (primary): on TRAIN jointly optimize an orthonormal \(P\in\mathbb R^{4096\times r}\) and task heads \(A_p\) with equal task weights,

   \[\sum_p \|T_{corr,p}-R_{U,p}PA_p\|_F^2+\lambda\sum_p\|A_p\|_F^2.\]

   Optimization is restricted to the pooled TRAIN row span, uses deterministic multi-start orthogonal initialization, alternating closed-form ridge heads and orthogonally retracted \(P\) updates, and selects hyperparameters on DEVELOPMENT only.
4. PCA-head and Haar-random input spaces: unsupervised controls.

Shared ranks are \(1,\ldots,16\), then 20, 24, 28, and every integer from 32 through 56. The registered shared dimension is the earliest rank whose 95% simultaneous lower bound for the minimum task retention reaches 0.90. No rank is predeclared.

## G. Scaling experiments

- Class scaling: \(C=2,4,6,8\), with frozen balanced random class subsets and equal examples per class. Report \(r_{90}(C)\) and \(r_{90}(C)/(C-1)\).
- Task scaling: \(T=1,2,4,8\), with frozen random domain subsets. Report the all-task shared \(r_{90}(T)\) for direct joint learning, union oracle, PCA, and Haar controls.

## H. Data split and one-time opening

- TRAIN learns projection spaces.
- DEVELOPMENT selects all hyperparameters and seeds.
- Existing TEST/v3 is debugging-only because it has already been inspected.
- New CONFIRMATION-v4 has 640 rows, ten per domain-by-child cell, with template families absent from TRAIN/DEVELOPMENT/v3 and fact subsets absent from v2/v3. It contains unseen factual compositions, not unseen atomic facts; the source taxonomy has only six atoms per child and all six have appeared previously.
- Confirmation bootstrap resamples template families within class and uses a familywise maximum-statistic correction across registered ranks. Shared admission uses the bootstrap distribution of the minimum retention across tasks.

## I. Required implementation guards

- Common-logit shifts leave fitted subspaces and overlaps invariant.
- An eight-class map has contrast rank at most seven.
- A union of \(T\) local maps has rank at most \(T(C-1)\).
- A synthetic known subspace is recovered above its Haar baseline.
- CONFIRMATION paths are inaccessible before the freeze receipt is created.
- All output tables include data, code, state, and run receipts.

## J. Execution contract

- One node, eight RTX 5090 GPUs, profile `n12lp.nn.i10a.8`, spot quota, cluster `computing-cluster-5090-01g`.
- Code and raw outputs live under `/data/250010109/MoE_Router/experiments/20260821_a15_08_06_e05_contrast_corrected_shared_scaling/`.
- Canonical summary, detailed record, figures, and tables live beside this protocol.
- Formal figures must be regenerated from frozen CSV/JSON result tables; no hand-entered values are allowed.

