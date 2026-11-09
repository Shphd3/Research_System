# Summary: A15_08_09_E01 Random-Projection Router Preservation

Primary Anchor: [A15_08_09](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_09_random_projection_router_preservation_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status: `COMPUTATION_COMPLETE_EXTERNAL_H1_GUARD_UNRESOLVED`

## Result Snapshot

The registered full-space representation is **above chance but does not have stable positive-margin linear routing structure**. At primary block 24, balanced accuracy is 0.3258 on TEST-same and 0.1891 on TEST-new, but the corresponding 5th-percentile true-label margins are -2.8938 and -9.0587. Both margin confidence intervals are entirely negative. Block 28 independently replicates the same qualitative result.

Therefore the numerical branch verdict is H2 `Pass`, H3 `Fail`. The dense-Gaussian H4 scan was correctly not run because H3 was its frozen admission condition. This is a completed conditional experiment, not a missing run.

The overall formal result remains `Insufficient` only because the registered independent human semantic review has not occurred. The 64-row AI review is complete but cannot be relabeled as human evidence. If that external H1 guard later passes, the already-frozen scientific branch is H3 `Fail` and H4 remains ineligible.

![Full-space admission result](figures/full_space_admission_gate.png)

The figure compares the two registered TEST panels at blocks 24 and 28. Accuracy is above the 1/8 chance line but far below the 0.90 H3 threshold; every low-tail margin interval is below zero. It supports only failure of the registered positive-margin gate, not absence of all linear or nonlinear information.

## Registered Verdicts

| Gate | Result | Direct basis |
| --- | --- | --- |
| H1 data validity | `Insufficient` overall; all machine guards pass | 19,200 rows; no registered leaks/duplicates/split overlap; token guard passes; TEST-new BoW 0.1195; independent human review missing |
| H2 full-space accessibility, block 24 | `Pass` numerically | TEST-same lower CI 0.3179; TEST-new lower CI 0.1831; both above chance; seed SD 0 |
| H3 positive-margin admission, block 24 | `Fail` conditional on H1 | accuracy lower bounds far below 0.90 and margin lower bounds -2.9416 / -9.2393 |
| Block 28 replication | H2 `Pass`, H3 `Fail` | accuracies 0.2438 / 0.2258; margin \(Q_{0.05}\) -2.2708 / -5.7441 |
| H4 dense-Gaussian preservation | `SKIPPED_H3_NOT_PASS` | frozen dependency rule; NMR is undefined without a positive full-space margin denominator |

## Data And Control Results

- The binding-controlled v2 dataset contains all eight parent-domain cards in every prompt, uses all neutral codes once, and changes only the code-to-card relation that carries the target. It passes all registered structural, isolation, literal-label, duplicate, character-5-gram, token-range, and per-class length-balance guards.
- The registered raw-text unigram+bigram baseline is near chance: 0.1270 on TEST-same and 0.1195 on TEST-new, compared with the rejected v1 values 0.9254 and 0.9449.
- All 19,200 Qwen3-30B-A3B records passed four-shard exact partition, finiteness, replay, native-MLP-input, and \(U=Z-X\) identity checks.
- Both blocks passed identity projection, common-offset invariance, five permuted-label controls, convergence, and statistical-power guards.

## Descriptive Diagnostics

These diagnostics cannot change H1--H4:

| Diagnostic | Block 24 | Block 28 | Boundary |
| --- | ---: | ---: | --- |
| Exact \(D_{out}/D_{in}\), TEST-same | 0.3879 | 0.2811 | All 3,275,520 unordered pairs; below 1 |
| Exact \(D_{out}/D_{in}\), TEST-new | 0.2172 | 0.2078 | All 3,275,520 unordered pairs; below 1 |
| Robust between/within ratio, TEST-same | 0.7350 | 0.6749 | Complete pair population; below 1 |
| Robust between/within ratio, TEST-new | 0.4324 | 0.5198 | Complete pair population; below 1 |
| Learned orthogonal fine-label \(r_{90}\) | 64 | 64 | Functional readout only; not geometric rank |
| Supervised-subspace coherence | 26.03 | 5.90 | Far above same-rank Haar means 2.68 / 1.70 |
| Normalized spectral entropy | 0.8388 | 0.9179 | High entropy does not imply low coherence |
| TRAIN difference-vector theorem bound | 71,135 | 69,439 | Exceeds registered maximum 1,024; coordinate sampling ineligible |

The uniformity audit directly resolves the meeting ambiguity: the relevant supervised energy is broad enough to have moderately high entropy, but it is not close to Haar-uniform under the maximum-leverage criterion. Random spectral-coordinate sampling was therefore stopped by its TRAIN-only sufficient bound.

The A09 theory-conformance repair supersedes two earlier descriptive readings. Sampled pair extrema were replaced by exact all-pair extrema, and frozen-Router SVD truncation was replaced by TRAIN-supervised orthogonal subspace learning with DEV-only early stopping. The old block-24 value \(r_{90}=16\) was therefore exploratory and is not retained as evidence; the corrected value is 64.

![Theory and experiment closure](figures/theory_experiment_closure.png)

## Claim Boundary

**Can claim:** for frozen Qwen3-30B-A3B, the registered token, blocks, robustness distribution, residualizer, and L2 multinomial probe, full-space \(R_U\) exposes reproducible above-chance parent accessibility but fails the registered stable positive-margin admission gate. Hence this experiment provides no valid premise for a dense-Gaussian preservation claim.

**Cannot claim:** that no linear subspace contains useful structure; that nonlinear routing is impossible; that projection generally fails; that the labels measure expert utility; or that high spectral entropy proves uniform embedding.

## Next Decision

**Decision: open representation-space learning as the next research question, but do not yet launch a large training sweep.** After an independent human closes the sole H1 review guard, stop this preservation branch and formulate one new anchor whose minimal falsifier asks whether a learned, expert-utility-aligned representation can make the held-out low-tail routing margin positive. Do not tune this dataset, layer, probe, or threshold to reopen H4.
