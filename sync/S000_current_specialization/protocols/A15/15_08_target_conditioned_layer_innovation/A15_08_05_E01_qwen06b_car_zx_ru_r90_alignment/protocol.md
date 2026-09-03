# Protocol: A15_08_05_E01 Qwen3-0.6B CAR/ZX/$R_U$ $r_{90}$ Alignment

## 0. Approval Snapshot

- **Document status:** `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN`
- **Approval status:** on 2026-08-18 the researcher explicitly requested no clustering, expanded token count, $r_{90}$ comparison, Qwen3-0.6B alignment, CAR/ZX methods, our $R_U$, and immediate experiment completion.
- **Block audit status:** A--G `CONFIRMED`; cross-block consistency `PASS`.
- **Execution scope approved:** implementation, unit tests, smoke, full local run, analysis, figures, and canonical result records. No commit, push, graph edit, publication, or root sync.
- **Purpose:** determine whether the apparent low-versus-high geometric-rank gap survives alignment of model, evaluation tokens, centering, and $r_{90}$.
- **Primary Anchor:** [A15_08_05](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_05_aligned_geometric_rank_scale_anchor.md)
- **Experiment role:** robustness and operationalization audit.
- **Treatment / objects:** CAR whole-block adjacent difference; ZX final-layer-PCA-500 projected Attention adjacent difference; affine-ridge residualized same-layer normalized update $R_U$.
- **Held fixed:** Qwen3-0.6B, DCLM source, EVALUATION tokens, layer hooks, token centering, covariance estimator, eigensolver, and $r_{90}$ rule.
- **Primary metric:** destination-layer paired difference in $r_{90}/d_{object}$ at 1,048,576 evaluation tokens.
- **Pass (`METHOD_OBJECT_GAP`):** all methods converge and both CAR-minus-$R_U$ and ZX-minus-$R_U$ layer-median differences have absolute value at least 0.10.
- **Fail (`NO_METHOD_OBJECT_GAP`):** all methods converge and both absolute differences are below 0.03.
- **Insufficient:** intermediate/mixed result, non-convergence, or any validity guard failure.
- **Cannot claim:** semantic new information, functional low rank, nonlinear novelty, causal use, or Router utility.

## 1. Terminology / Definitions

For block $l$, $h_l$ is its raw input residual, $a_l$ is the raw `self_attn.o_proj` output, $N_l$ is `post_attention_layernorm`, $H_l$ is the complete block output, $X_l=N_l(h_l)$, and $U_l=N_l(h_l+a_l)-N_l(h_l)$. $R_{U,l}$ is the EVALUATION residual after an affine ridge predictor from $X_l$ to $U_l$ is fitted on TRAIN and its regularization is chosen on DEVELOPMENT.

$r_{90}$ is the minimum number of centered-covariance eigen-directions containing 90% of total variance. Absolute $r_{90}$ is in directions; $r_{90}/d_{object}$ is a dimension-normalized geometric concentration measure. Neither measures function.

## 2. Anchor Alignment

This experiment tests whether sample scale and object construction explain the descriptive conflict between A15_08_04 and meeting-reported ZX/CAR spectra. It does not reopen A15_08's functional admission verdict or perform token clustering.

## 3. Tested Hypothesis

`H-OBJECT`: after convergence, CAR, ZX, and $R_U$ retain materially different normalized $r_{90}$ profiles on the same model and evaluation tokens. The strongest rival is `R-NO-GAP`, under which the aligned profiles differ by less than 0.03.

## 4. Rival Explanations

1. **R-MODEL:** Qwen3-8B versus Qwen3-0.6B caused the apparent discrepancy. Controlled by running all conditions on Qwen3-0.6B.
2. **R-SAMPLE-CAP:** 2,048 tokens truncated the estimable rank. Controlled by dimensions at most1,024 and up to1,048,576 EVALUATION tokens, with nested convergence snapshots.
3. **R-METRIC:** $r_{80}$ versus $r_{90}$ caused the narrative difference. Controlled by one $r_{90}$ rule; $r_{80}$ is auxiliary only.
4. **R-LEAKAGE:** evaluation tokens selected the ZX basis or $R_U$ predictor. Controlled by non-overlapping TRAIN/DEVELOPMENT/EVALUATION partitions.
5. **R-BOUNDARY:** sequence-start tokens dominate raw CAR covariance. Guarded by per-position norm summaries; no token is silently removed from the primary population.

## 5. Data Construction And Provenance

- Source: `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_0_of_10_shard_00000000_processed.bin`, raw `uint32` Qwen token IDs.
- Sequence length: 2,048; no overlap between sequences or partitions.
- TRAIN: offset 0, 64 sequences, 131,072 tokens.
- DEVELOPMENT: offset 131,072, 64 sequences, 131,072 tokens.
- EVALUATION: offset 262,144, 512 sequences, 1,048,576 tokens.
- EVALUATION snapshots: 2,048; 8,192; 32,768; 131,072; 524,288; 1,048,576 nested tokens.
- Statistical row: one token position. Tokens within documents and layers are correlated; no population confidence interval is claimed.
- Record byte/source hashes, token-slice hashes, token ranges, sequence count, and vocabulary guard.

## 6. Learning Task And Permitted Supervision

There are no labels. TRAIN may determine the ZX reference basis and $X\to U$ affine ridge fits. DEVELOPMENT may select one ridge multiplier per layer from the frozen grid. EVALUATION may only compute spectra and registered comparisons.

## 7. Model / Architecture And Frozen Variants

- Model: local `/data/share/Qwen3-0.6B`, 28 blocks, hidden width 1,024, intermediate width 3,072.
- Weight/forward dtype: bfloat16; sufficient statistics, solves, and eigendecompositions: float32 with batch-centered stable merges. TF32 matrix multiplication is permitted as an engineering acceleration and recorded.
- Attention: SDPA, `use_cache=False`, eval/inference mode.
- Hooks: block pre-hook for $h_l$; `self_attn.o_proj` forward hook for $a_l$; block forward hook for $H_l$; native MLP pre-hook for $Z_l$ identity.
- Batch: 4 sequences × 2,048 tokens on one H100.

### ZX reference basis

On TRAIN only, center the complete final-block state $H_{28}$, compute its 1,024-dimensional covariance, and take the descending top 500 eigenvectors $Q_{500}$. Require orthogonality relative error at most $5\times10^{-4}$ and projected-energy conservation at most $5\times10^{-4}$ relative error.

### $R_U$ residualizer

For each layer, fit centered affine ridge regression from $X_l$ to $U_l$. The frozen dimensionless multipliers are $\{10^{-6},10^{-5},10^{-4},10^{-3},10^{-2},10^{-1}\}$, applied as $\lambda=\alpha\,\operatorname{tr}(C_{XX})/1024$. DEVELOPMENT selects minimum per-coordinate MSE; ties choose the larger multiplier. No EVALUATION statistic participates.

## 8. Training Objective And Optimization

The language model is frozen. The only fitted objects are closed-form TRAIN ridge predictors minimizing squared reconstruction error. There is no gradient optimizer, checkpoint, or early stopping.

## 9. Conditions, Seeds, And Checkpoints

| Condition | EVALUATION matrix | Dimension | Layers |
| --- | --- | ---: | ---: |
| `car_block_transition` | $H_{l+1}-H_l$ | 1,024 | target blocks 2--28 |
| `zx_attention_transition_pca500` | $(a_{l+1}-a_l)Q_{500}$ | 500 | target blocks 2--28 |
| `ru_linear_residual` | $U_l-(X_lB_l+b_l)$ | 1,024 | blocks 1--28 |

Framework seed is 8180501. Data and nested checkpoints are deterministic, not randomly sampled.

## 10. Primary Metric And Frozen Analysis Plan

For each matrix, stream batch-centered sufficient statistics and form the unbiased sample covariance. Symmetrize, compute `eigvalsh`, clip only negative numerical roundoff to zero, normalize by trace, and compute $r_{90}$ and $r_{90}/d_{object}$.

At 1,048,576 tokens, pair CAR and ZX target blocks 2--28 with $R_U$ blocks 2--28. Report per condition and pair:

1. layer-median and full range of absolute $r_{90}$;
2. layer-median $r_{90}/d_{object}$;
3. median paired CAR-minus-$R_U$ and ZX-minus-$R_U$ normalized differences;
4. fraction of paired layers with positive difference.

A condition converges when its full-run layer-median normalized $r_{90}$ differs from its 524,288-token value by at most 0.02. All three must converge before a verdict. No layer or token is excluded; a failed curve makes the result insufficient.

## 11. Secondary Metrics And Guards

- $r_{50}$, $r_{80}$, effective rank, top-1 and top-16 shares, covariance trace.
- Full cumulative spectra at each nested token count; full eigenspectrum at 1,048,576.
- Native MLP-input reconstruction $Z_l=N_l(h_l+a_l)$ relative error at most $10^{-5}$.
- $U_l=Z_l-X_l$ exact construction audit.
- Complete 28-layer hooks and exact token counters.
- TRAIN/DEVELOPMENT/EVALUATION hash non-overlap.
- ZX basis orthogonality and projected-energy guards.
- TRAIN and DEVELOPMENT ridge MSE tables and finite solve guards.
- Sequence-position norm summary for CAR, including position 0 versus nonzero positions.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: synthetic rank-$k$ data return $r_{90}\le k$; streaming and direct covariance agree.
- Known bad: constant centered data are rejected for negligible trace.
- Known confusing: projection to 500 dimensions changes the denominator, so absolute ranks are not compared without the normalized value.
- Known confusing: $R_U$ removes only affine-linear predictability under the frozen ridge family.
- Known confusing: many tokens make sampling rank full but do not turn covariance rank into functional rank.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input / operation | Required output and gate |
| --- | --- | --- | --- |
| Preflight | verify exact source/model/environment | hashes, config, GPU, vocabulary | `preflight.json`; all guards pass |
| Unit tests | validate estimators | synthetic streaming moments, ridge, object formulas | focused tests pass after recorded red state |
| Smoke | validate hooks and split mechanics | 2 TRAIN + 2 DEV + 4 EVAL sequences | identities, counts, three spectra pass |
| Fit pass | construct token-independent evaluation machinery | full TRAIN/DEVELOPMENT | `basis.pt`, residualizers, selection table |
| Evaluation pass | stream the shared million-token population | frozen basis and predictors | all snapshots and layer spectra |
| Analysis | apply frozen comparison and convergence rules | metric tables only | one typed verdict or insufficient |
| Rendering | create common reading surfaces | frozen arrays/tables | convergence figure, full-rank figure, paired summary |

Any failed earlier gate stops interpretation. A resource retry may change batch size only if outputs are bitwise/reconstruction checked and recorded as an engineering amendment; data, objects, metrics, thresholds, or partitions cannot change after the first execution starts.

## 14. Algorithm, Output, And Provenance Contract

- Code root: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_05_e01_qwen06b_car_zx_ru_r90_alignment/`.
- Raw run root: `/data/250010109/MoE_Router/experiments/20260818_a15_08_05_e01_qwen06b_car_zx_ru_r90_alignment/runs/`.
- Canonical result root: this Protocol directory.
- Expected raw artifacts: preflight and split manifests; basis/residualizer receipts; snapshot spectra NPZ; per-layer metric and paired comparison CSVs; norm-position diagnostic; figures; verdict and artifact manifest.
- Expected canonical artifacts: `summary.md`, `detailed.md`, selected tables/figures, and result links in A15_08_05.

## 15. Success / Failure / Insufficient Evidence

- `METHOD_OBJECT_GAP`: all convergence/validity guards pass and both absolute paired median differences are at least 0.10.
- `NO_METHOD_OBJECT_GAP`: all guards pass and both absolute paired median differences are below 0.03.
- `MIXED_OR_INSUFFICIENT`: any intermediate result, sign mixture not covered above, non-convergence, or validity failure.

The sign and exact scale remain direct observations. Secondary metrics cannot rescue the registered verdict.

## 16. What This Cannot Claim

Even a stable high $r_{90}$ cannot establish that new semantic information is high-rank, that all retained directions are required for a task, that the model uses them, or that they improve a Router. A low $R_U$ rank cannot establish nonlinear novelty or functional sufficiency. This experiment does not reproduce CCA or clustering.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A Question/boundary | `CONFIRMED` | researcher requested aligned explanation and excluded clustering/CCA |
| B Data/provenance | `CONFIRMED` | researcher requested expanded tokens; one million matches the meeting scale |
| C Task/supervision | `CONFIRMED` | geometry-only CAR/ZX/$R_U$ comparison |
| D Model/architecture | `CONFIRMED` | researcher explicitly requested Qwen3-0.6B alignment |
| E Objective/optimization | `CONFIRMED` | frozen model; existing $R_U$ linear residualization |
| F Comparison/evidence | `CONFIRMED` | researcher explicitly fixed $r_{90}$ and the three method families |
| G Execution/reproducibility | `CONFIRMED` | “请开始补全对齐实验” authorizes implementation and run; no external publication action |

Cross-block consistency: `PASS`. Scientific body frozen before model execution on 2026-08-18.

### Post-start execution note (does not alter the primary analysis)

The registered sequence-position norm guard exposed an extreme CAR spectrum at target block 3 and a weaker boundary-sensitive spectrum at target block 28. A post-hoc diagnostic therefore recomputed CAR covariance for all positions, non-boundary positions only, and position-0 tokens only. This diagnostic did not change the registered population, thresholds, verdict eligibility, or primary result. It is reported only to localize the observed singularity.
