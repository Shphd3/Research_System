# Detailed experiment record

## 1. Identity and execution

- Experiment: `A15_08_07_E05_contrast_corrected_shared_scaling`.
- Worker root: `/data/250010109/MoE_Router/experiments/20260821_a15_08_06_e05_contrast_corrected_shared_scaling`.
- Frozen model: `/data/share/Qwen3-8B`.
- Layers: blocks 24 and 28.
- Formal extraction job: `pt-sd0hpsc7`; one node, eight RTX 5090 GPUs, `n12lp.nn.i10a.8`, spot quota; terminal state `SUCCEEDED`.
- Selection run: `preconfirmation-20260821T_e05_r1`.
- Confirmation extraction: `confirmation-20260821T_e05_r1`.
- Canonical statistical replay: `formal-results-20260821T_e05_r2`.

## 2. Data

TRAIN and DEVELOPMENT reuse the balanced 8-domain by 8-child taxonomy data, with ten examples per cell per split. Confirmation-v4 adds ten rows per cell (640 total) using ten unseen templates and the five pair/complement fact-subset pairs left unused by v2 and v3.

The source has six atomic facts per child and all six appeared in prior data. Therefore v4 validates new factual compositions and expressions, not unseen atomic facts. Its audit reports zero normalized-text overlap, zero v2/v3 semantic-subset overlap, ten new template families, and a complete 64-cell grid.

## 3. Contrast correction

For \(C\) classes, both target residuals and output coefficients are projected with

\[H_C=I-\frac1C\mathbf1\mathbf1^\top.\]

Every state is checked for \(B\mathbf1\approx0\) and effective rank at most \(C-1\). Requests above \(C-1\) are rejected. The eight-class local grid is exactly \(r=1,\ldots,7\).

## 4. Functional target and split discipline

The old-state classifier is fitted from standardized \(X\). Its TRAIN out-of-fold prediction is removed from the centered one-hot target. The candidate input is standardized \(R_U=U-\widehat E_{lin}[U\mid X]\). TRAIN fits bases and heads; DEVELOPMENT selects ridge and direct-joint optimizer settings; the new confirmation data is opened only after the data, state, code, and protocol hashes are frozen.

The gain for each row is the old-state cross entropy minus the old-state-plus-\(R_U\) cross entropy. A task receives an \(r_{90}\) only when full-map gain has a positive lower bound and the registered lower bound of gain retention reaches 0.90.

## 5. Local fitting and uncertainty

Each domain receives a contrast-corrected reduced-rank ridge map for ranks 1–7. Confirmation bootstrap resamples ten template families within each class. The local rank curve uses a maximum-statistic familywise correction across its seven candidate ranks. All 16 full-map gains have positive 95% lower bounds.

At rank 7, point retention is approximately one for every task, as expected when the complete contrast space is restored. The uncertainty correction is decisive: block-24 rank-7 lower bounds range from -0.514 to 0.889; block-28 bounds range from 0.714 to 0.902. Only block-28 biology crosses 0.90.

## 6. Stability audit

Formal overlap is defined at each admitted task's \(r_{90}\). Since only one task is admitted, a formal cross-task overlap matrix cannot be constructed. A clearly labeled rank-7 diagnostic was therefore added without changing admission:

| Layer | Mean same-task bootstrap overlap | Mean cross-domain overlap | Haar mean |
|---|---:|---:|---:|
| 24 | 14.37% | 1.67% | about 0.17% |
| 28 | 13.79% | 2.03% | about 0.17% |

Same-task overlap is about 6.8–8.6 times cross-task overlap, but the absolute same-task value is low. This is evidence for relative task specificity, not for stable fixed Router axes.

## 7. Direct shared learning versus oracle union

The primary learner directly optimizes one orthonormal input basis with equal task weights and separate ridge heads. It uses pooled supervised cross-covariance initialization and never consumes fitted local coefficient maps. Hyperparameters are selected on DEVELOPMENT.

The oracle baseline contrast-centers each fitted local map, normalizes tasks, concatenates the maps, and takes the SVD. It is available only after all local answers are known.

Under the registered confidence correction, direct joint learning has no admitted \(r_{90}\) for any \(T\ge2\) subset at either block. The oracle union also has no multi-domain formal \(r_{90}\) after correction across the full rank grid. A fixed-rank sensitivity, which keeps simultaneous taskwise bounds but omits cross-rank familywise correction, yields oracle crossings at 54D (block 24) and 52D (block 28) for \(T=8\); direct joint learning remains NA. This sensitivity explains the old near-56D curve but is not the registered result.

## 8. Class and task scaling

- \(C=2\): 25/32 subsets pass at each layer, always at rank 1, exactly \(C-1\).
- \(C=4\): 0/32 pass at either layer.
- \(C=6\): 0/32 pass at block 24 and 1/32 at block 28; the admitted case is rank 5, exactly \(C-1\).
- \(C=8\): 0/8 pass at block 24 and 1/8 at block 28; the admitted case is rank 7, exactly \(C-1\).

Thus no admitted setting demonstrates \(r_{90}<C-1\), and there is no evidence of saturation below the classifier contrast ceiling.

## 9. Deviations and failure trace

Three implementation/statistics events are retained rather than erased:

1. The first TRAIN/DEV run failed when a ridge identity matrix remained on CPU while features were on GPU. No selection state was written; the directory is retained as `preconfirmation-20260821T_e05_r1_failed_device_mismatch`. A CUDA regression test was added.
2. The first confirmation aggregation stopped because `defaultdict` was not imported. No parameter was retuned; the directory is retained as `formal-results-20260821T_e05_r1_failed_missing_import`.
3. The next aggregation used a taskwise lower bound at each shared rank but omitted the protocol's additional familywise correction across ranks. It is retained as `formal-results-20260821T_e05_r1_invalid_shared_rankwise_lcb`. The corrected mechanical replay is r2; no prediction, state, seed, or data row changed. The amendment is stored in evidence.

## 10. Claim boundary

This experiment rejects the previous evidential interpretation; it does not prove that no compact Router-relevant subspace exists. It shows that this eight-class linear held-out protocol, with the current sample size and strict uncertainty control, does not identify one. A Router experiment should not proceed from these axes without substantially better same-task stability and a task definition whose functional dimension is not pinned to \(C-1\).

