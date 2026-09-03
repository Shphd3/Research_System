# Protocol: A15_08_06_E01 Qwen3-8B CAR / ZX / $R_U$ $r_{90}$ Replication

## 0. Approval Snapshot

- **Document status:** `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN`
- **Approval status:** on 2026-08-18 the researcher explicitly requested execution of the same aligned analysis on Qwen3-8B.
- **Block audit / consistency:** A--G `CONFIRMED`; cross-block consistency `PASS`.
- **Execution scope approved:** implementation, focused tests, preflight, smoke, full run, analysis, figures, and canonical result records. No commit, push, root sync, graph edit, or publication.
- **Design frozen at:** 2026-08-18 before the first Qwen3-8B model forward.
- **Purpose / role:** model-scale robustness check of A15_08_05.
- **Primary Anchor:** [A15_08_06](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_06_qwen8b_geometric_rank_replication_anchor.md).
- **Changed variable:** Qwen3-0.6B (28 layers, width1024) to Qwen3-8B (36 layers, width4096).
- **Held fixed:** DCLM token partitions, sequence length, TRAIN/DEVELOPMENT/EVALUATION roles and counts, CAR/ZX/$R_U$ formulas, ZX rank500, centering, ridge grid, nested snapshots, eigensolver, $r_{90}/d$, convergence and gap thresholds.
- **Primary metric:** for each method, Qwen3-8B layer-median $r_{90}/d_{object}$ minus the frozen Qwen3-0.6B reference.
- **Pass (`MODEL_SCALE_INVARIANT`):** all methods converge and all three absolute model differences are below0.03.
- **Fail (`MODEL_SCALE_SHIFT`):** all methods converge and at least one absolute difference is at least0.10.
- **Insufficient:** intermediate differences, non-convergence, or a validity-guard failure.
- **Cannot claim:** semantic novelty, functional rank, nonlinear novelty, causal use, or Router value.

## 1. Terminology / Definitions

For block $l$, $h_l$ is raw input residual, $a_l$ is Attention `o_proj` output, $N_l$ is post-Attention RMSNorm, and $H_l$ is complete block output. Define $X_l=N_l(h_l)$, $U_l=N_l(h_l+a_l)-N_l(h_l)$, and $R_{U,l}$ as the EVALUATION residual after an affine ridge predictor $X_l\to U_l$ is fitted on TRAIN and selected on DEVELOPMENT.

$r_{90}$ is the smallest number of centered-covariance eigen-directions containing90% of variance. $r_{90}/d_{object}$ is dimension-normalized geometric concentration; neither quantity measures function.

## 2. Anchor Alignment

This experiment changes only model scale relative to A15_08_05. It separates the rival that Qwen3-0.6B's broad spectra are small-model-specific. It does not reopen the parent functional-accessibility verdict.

## 3. Tested Hypothesis

`H-SCALE-STABLE`: all three 8B median normalized ranks remain within0.03 of the frozen0.6B values. `R-SCALE-SHIFT`: one or more move by at least0.10. A supportive descriptive label `BROAD_TRANSITION_REPLICATED` applies when both CAR and ZX medians are at least0.40; it does not override the primary verdict.

## 4. Rival Explanations

1. **R-MODEL-SCALE:** wide spectra are specific to0.6B; separated by the one-variable model replacement.
2. **R-SAMPLE-CAP:** small token populations understate rank; controlled by the same1,048,576 EVALUATION tokens and convergence snapshots.
3. **R-OBJECT:** CAR/ZX/$R_U$ definitions cause differences; held fixed and reported separately rather than averaged.
4. **R-RESOURCE-APPROXIMATION:** 8B resource handling changes the estimator; prohibited. GPU/CPU offload may change only storage location, never dtype, rows, sufficient-statistic formula, fit, or eigensolver.

## 5. Data Construction And Provenance

- Source: `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_0_of_10_shard_00000000_processed.bin`, raw `uint32` Qwen token IDs.
- Sequence length2048; no partition overlap.
- TRAIN: offset0, 64 sequences,131,072 tokens.
- DEVELOPMENT: offset131,072, 64 sequences,131,072 tokens.
- EVALUATION: offset262,144, 512 sequences,1,048,576 tokens.
- Nested EVALUATION counts:2,048;8,192;32,768;131,072;524,288;1,048,576.
- Statistical row is one token position. Layers and tokens are not treated as independent experimental replicates.

## 6. Learning Task And Permitted Supervision

There are no semantic labels. TRAIN may construct $Q_{500}$ and ridge fits; DEVELOPMENT may select ridge alpha; EVALUATION may only produce spectra and frozen comparisons.

## 7. Model / Architecture And Frozen Variants

- Model: local `/data/share/Qwen3-8B`,36 blocks, hidden width4096, intermediate width12288.
- Forward dtype bfloat16; sufficient statistics, ridge solves, and eigendecomposition float32.
- Attention SDPA, `use_cache=False`, eval/inference mode.
- Hooks: block input $h_l$, Attention `o_proj` output $a_l$, complete block output $H_l$, native MLP input identity.
- Batch is an engineering choice capped at one sequence per40GB MIG for the registered run; changing it requires identical counts and formulas.
- 4096-dimensional sufficient statistics are accumulated on GPU and may be stored on CPU between stages without numerical casting.

### ZX reference basis

On TRAIN only, center final-block state $H_{36}$ and take covariance top500 eigenvectors $Q_{500}$. Require orthogonality and projected-energy relative errors each at most $5\times10^{-4}$.

### $R_U$ residualizer

For each layer, fit centered affine ridge regression $X_l\to U_l$. Use multipliers $\{10^{-6},10^{-5},10^{-4},10^{-3},10^{-2},10^{-1}\}$ with $\lambda=\alpha\operatorname{tr}(C_{XX})/4096$. DEVELOPMENT selects minimum per-coordinate MSE; ties select the larger multiplier.

## 8. Training Objective And Optimization

The language model is frozen. Only closed-form ridge predictors minimize squared reconstruction error; no gradient training, checkpoint selection, or early stopping occurs.

## 9. Conditions, Seeds, And Checkpoints

| Condition | EVALUATION matrix | Dimension | Target blocks |
| --- | --- | ---: | ---: |
| CAR | $H_{l+1}-H_l$ |4096|2--36|
| ZX | $(a_{l+1}-a_l)Q_{500}$ |500|2--36|
| $R_U$ | $U_l-(X_lB_l+b_l)$ |4096|1--36|

Framework seed8180601. Data and checkpoints are deterministic nested prefixes.

## 10. Primary Metric And Frozen Analysis Plan

Stream batch-centered sufficient statistics, form the unbiased covariance, symmetrize, compute full `eigvalsh`, clip negative numerical roundoff to zero, normalize by trace, and compute $r_{90}/d$.

At1,048,576 tokens, take the unweighted layer median per method. Frozen0.6B references are CAR0.5625, ZX0.5940, and $R_U$0.43505859375. Define $\Delta_m=\operatorname{median}_{8B}(r_{90}/d)-\operatorname{median}_{0.6B}(r_{90}/d)$. All methods must first converge: full versus524,288-token median difference at most0.02.

- all $|\Delta_m|<0.03$: `MODEL_SCALE_INVARIANT`;
- any $|\Delta_m|\ge0.10$: `MODEL_SCALE_SHIFT`;
- otherwise or non-converged: `MIXED_OR_INSUFFICIENT`.

No layer or token is excluded from the primary population. Missing, failed, non-finite, or incomplete curves make the result insufficient. The unsealing point is creation of the first full-run EVALUATION spectrum.

## 11. Secondary Metrics And Guards

- absolute $r_{50}$/$r_{80}$/$r_{90}$, effective rank, top-1/top-16 shares, trace, complete spectrum;
- within-8B CAR-$R_U$ and ZX-$R_U$ paired-layer median normalized differences using the existing0.10/0.03 object-gap rule;
- `BROAD_TRANSITION_REPLICATED` when CAR and ZX layer medians are both at least0.40;
- native MLP identity relative error at most $10^{-5}$;
- complete36-layer hooks and exact token counters;
- split hash uniqueness, finite solves, ZX basis guards;
- CAR position-0 versus other-position norm table. Any post-hoc exclusion is diagnostic only.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: synthetic rank-$k$ covariance returns $r_{90}\le k$; streaming matches direct covariance.
- Known bad: nonpositive covariance trace is rejected.
- Known confusing: absolute ranks cannot be compared across4096 and500 dimensions without $r_{90}/d$.
- Known confusing: $R_U$ removes affine-linear old-state predictability only.
- Known confusing: model layers differ36 versus28; primary cross-model aggregation compares layer medians, not nominal layer IDs.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input / operation | Required output and gate |
| --- | --- | --- | --- |
| Preflight | verify model/data/resource identity | inspect config, hashes, GPU and vocabulary | exact36×4096 model and unique splits |
| Unit tests | validate width/layer-generic estimators and offload | synthetic moments,36-layer verdict, storage moves | focused tests pass after red state |
| Smoke | validate8B hooks, identities and memory route |2 TRAIN +2 DEV +4 EVAL sequences | all conditions, counts, spectra, guards pass |
| Fit | construct basis/residualizers | full TRAIN/DEVELOPMENT; CPU storage between stages | basis and36 selected ridge fits |
| Evaluation | compute shared population spectra | frozen basis/predictors; million tokens | all six snapshots and complete spectra |
| Analysis | apply frozen comparisons | metric tables only | one typed model-scale verdict |
| Rendering | produce common reading surfaces | frozen arrays/tables | convergence, layerwise and cross-model figures |

Any failed earlier gate stops interpretation. A resource retry may change batch size or storage location only and must be recorded; scientific choices cannot change.

## 14. Algorithm, Output, And Provenance Contract

- Code root: `Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_06_e01_qwen8b_car_zx_ru_r90_replication/`.
- Raw run root: `/data/250010109/MoE_Router/experiments/20260818_a15_08_06_e01_qwen8b_car_zx_ru_r90_replication/runs/`.
- Canonical root: this Protocol directory.
- Required artifacts: preflight, test/smoke receipts, basis and ridge selection, all spectra and metrics, model comparison table, verdict, manifest, summary, detailed and selected figures.
- Resource ceiling: one40GB H100 MIG, batch1,120 minutes. A timeout yields incomplete evidence, not a scientific failure.

## 15. Success / Failure / Insufficient Evidence

The primary typed outcomes are `MODEL_SCALE_INVARIANT`, `MODEL_SCALE_SHIFT`, and `MIXED_OR_INSUFFICIENT` exactly as Section10. Secondary object-gap or broad-spectrum labels cannot rescue a missing primary result.

## 16. What This Cannot Claim

Stable or shifted geometric rank cannot establish semantic new information, functional necessity, nonlinear novelty, causal use, or Router value. It also cannot identify whether any shift is caused by width, depth, training, or another architectural difference inside the bundled model-scale change.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A Question/boundary | `CONFIRMED` | researcher requested same analysis on8B |
| B Data/provenance | `CONFIRMED` | same frozen DCLM partitions as approved0.6B run |
| C Task/supervision | `CONFIRMED` | geometry-only replication |
| D Model/architecture | `CONFIRMED` | researcher explicitly selected Qwen3-8B |
| E Objective/optimization | `CONFIRMED` | same closed-form residualization |
| F Comparison/evidence | `CONFIRMED` | same $r_{90}$ analysis plus frozen cross-model reference |
| G Execution/reproducibility | `CONFIRMED` | “请执行分析” authorizes implementation through full analysis |

Cross-block consistency: `PASS`. Scientific body frozen before first8B forward on2026-08-18. Post-start changes require an append-only amendment with eligibility impact.

### Append-only execution notes

1. The first smoke command used the container default Python, which lacked `transformers`, and stopped before model loading or any scientific observation. The retry used the same `spectral-hier` environment as A15_08_05. Scientific configuration was unchanged; eligibility impact: none.
2. The second smoke reached the fit-receipt stage but attempted to read the TRAIN final-state count after that accumulator had been released for memory. The retry saved the already-known integer count before release. No tensor, sample, fit, estimator, threshold, or analysis changed; eligibility impact: none.
3. The registered CAR position guard triggered a post-hoc all-position versus non-boundary versus position-0 diagnostic. It did not alter the primary population, exclusions, verdict, or eligibility.
