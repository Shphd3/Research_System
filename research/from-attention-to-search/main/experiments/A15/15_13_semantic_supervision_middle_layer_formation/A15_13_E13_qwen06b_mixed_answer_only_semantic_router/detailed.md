# Detailed Record: A15_13_E13 Mixed Answer-Only Semantic Routing

## Provenance And Completion

- Canonical ACP job: `pt-ykhpfbfw`
- Resource: one reserved `n6ls.iu.i40.4` worker with four H100 GPUs
- Canonical run root: `/data/250010109/MoE_Router/experiments/20260902_a15_13_e13_qwen06b_mixed_answer_only_semantic_router/runs/full-20260902T190657Z`
- Tests: `7/7` passed.
- Completion: `22/22` final checkpoints, `62/62` registered evaluation arrays, all finite.
- Aggregate SHA-256: `5f28633b814c5bf52465f0ef2e761299252ddf721f64934a61ed1b7904db57c8`
- Completion-audit SHA-256: `bdc2de1ba8e99ea0e8a95601b4f1bd6004fb4bd8062bd76adbf93547039eeb7b`
- Processed-data SHA-256: `31ae01ce74282d983a18b77892edf6772e35799dd699b4a78ecb07043d09f0d2`

The earlier run `full-20260902T182655Z` passed its mechanical audit but used a source-ID bijection instead of a sample-random label null. It is ineligible as the canonical suite and is retained only as the audit trail described by Protocol Amendment C003.

## Data

| Source ID | Cached source | Train | Development | Evaluation | Coarse group |
| ---: | --- | ---: | ---: | ---: | --- |
| 0 | MMLU | 512 | 64 | 64 | general/reading/science QA |
| 1 | RACE-high | 512 | 64 | 64 | general/reading/science QA |
| 2 | ARC-Challenge | 512 | 64 | 64 | general/reading/science QA |
| 3 | GSM8K | 512 | 64 | 64 | mathematical reasoning |
| 4 | MetaMathQA | 512 | 64 | 64 | mathematical reasoning |
| 5 | SciQ | 512 | 64 | 64 | general/reading/science QA |
| 6 | HumanEval | 512 | 64 | 64 | code |
| 7 | MBPP | 512 | 64 | 64 | code |

Sequences were padded or truncated to 512 tokens. Up to 256 answer tokens plus EOS were reserved before truncating the prompt. Prompt labels were `-100`; cross entropy was computed only over the reference answer and EOS. The dataset source name was never inserted into the prompt.

The cache did not contain MMLU-Pro, BBH, MATH, or GPQA and had no external network. RACE-high, ARC-Challenge, MetaMathQA, and SciQ are explicit substitutes. HumanEval's 164 raw rows were cycled, so train/development/evaluation overlap exists. The researcher allowed this for controlled model comparison, but it prevents benchmark-generalization claims.

## Architecture And Parameter Boundary

- Base: frozen Qwen3-0.6B-Base and frozen language head.
- Injection: zero-index block 14 MLP `down_proj` only.
- Dense: one rank-24 LoRA.
- Flat: eight stored rank-24 leaves; one selected leaf per token, so active rank is 24 but total stored leaf rank is 192.
- Hierarchy: one shared, three parent, and eight leaf rank-eight LoRAs; one of each is active, so active rank is 24 and total stored rank is 96.
- Primary semantic-versus-task comparisons are exactly parameter matched inside each topology. Dense, flat, and hierarchy are active-rank matched but not total-parameter matched.

Task-only Routers receive language gradients through the selected softmax coefficient; Top-1 identity itself is non-differentiable. Semantic models additionally use source cross entropy on target positions. Forced-gold uses the source route and unit coefficients for expert output while retaining shadow Router logits for diagnostics.

## Training

- Independent training; no stage handoff.
- Seeds: 17 and 29.
- Four passes over 4,096 source-balanced train examples.
- Microbatch 8, accumulation 16, effective batch 128.
- Exactly 128 optimizer updates per run.
- LoRA learning rate `2e-4`; Router learning rate `5e-4`; AdamW weight decay `0.01`.
- Five-update warmup, cosine decay, gradient norm clip 1.0.
- Fixed-development evaluations at updates 6, 13, 26, 51, 77, 102, and 128, plus update-zero checkpoint storage.
- Final evaluation used 512 examples, 64 per source.

## Corrected Random Null

The null begins with 512 copies of each of eight route IDs, applies a deterministic sample-level permutation with seed 6113, and assigns those labels independently of source. It is exactly balanced globally. Each true source contains several null route IDs; train source/null-label NMI is `0.002844`. Final learned route/source NMI is `0.0505`, compared with `0.7014` under real source labels.

## Complete Final Table

| Condition | Seed 17 NLL | Seed 29 NLL | Mean NLL | Mean route NMI | Mean load entropy |
| --- | ---: | ---: | ---: | ---: | ---: |
| `DENSE_R24` | `0.684158` | `0.683277` | `0.683717` | `0.000` | `0.000` |
| `FLAT_TASK_R24` | `0.648007` | `0.656783` | `0.652395` | `0.093` | `0.401` |
| `FLAT_SEM_R24` | `0.661049` | `0.671258` | `0.666153` | `0.701` | `0.666` |
| `FLAT_SHUFFLED_R24` | `0.701587` | `0.697085` | `0.699336` | `0.051` | `0.963` |
| `HIER_TASK_R8` | `0.617925` | `0.619689` | `0.618807` | `0.097` | `0.161` |
| `HIER_SEM_R8` | `0.622231` | `0.620065` | `0.621148` | `0.713` | `0.668` |
| `HIER_GOLD_R8` | `0.595861` | `0.595705` | `0.595783` | `1.000` | `0.669` |
| `FLAT_TASK_R24_LFB` | `0.647879` | `0.657095` | `0.652487` | `0.093` | `0.409` |
| `FLAT_SEM_R24_LFB` | `0.661006` | `0.671340` | `0.666173` | `0.702` | `0.666` |
| `HIER_TASK_R8_LFB` | `0.617916` | `0.619769` | `0.618843` | `0.096` | `0.164` |
| `HIER_SEM_R8_LFB` | `0.621877` | `0.619923` | `0.620900` | `0.713` | `0.668` |

The primary token-weighted metric and an equal-source post-hoc sensitivity disagree for learned hierarchy: semantics is `0.002341` worse on the primary but `0.028177` better when each source NLL receives equal weight. The equal-source gain is driven mainly by RACE-high and is not stable across all sources. It is a distributional sensitivity, not a replacement verdict.

## Learning-Efficiency Details

The normalized curve area is the trapezoidal mean of fixed-development NLL over seen answer tokens; positive task-only-minus-semantic values favor semantics. The target is the task-only NLL interpolated at 75% of its token budget.

- Flat semantics: curve-area effects `-0.012971`, `-0.017132`; neither seed reaches the task-only target.
- Hierarchical semantics: `-0.011018`, `-0.007912`; seed 17 never reaches the target and seed 29 has speed `0.986x`, not a speedup.
- Forced-gold hierarchy: `+0.011397`, `+0.013905`; target-loss speedups `1.358x`, `1.434x`.

## Interventions

Changed-minus-intact token-weighted NLL; positive means the selected expert path is functionally useful.

| Condition | Delete active expert | Replace by next leaf |
| --- | ---: | ---: |
| Flat task-only | `+0.09250` | `+0.09113` |
| Flat source-supervised | `+0.07874` | `+0.07032` |
| Flat random-label | `+0.04556` | `+0.04283` |
| Hierarchy task-only | `+0.02822` | `+0.02650` |
| Hierarchy source-supervised | `+0.02434` | `+0.02093` |
| Hierarchy forced-gold | `+0.04135` | `+0.03777` |

The wrong-leaf intervention advances the global leaf ID by one and holds the original route coefficient fixed. It measures route-specific leaf substitution, not strictly within-parent substitution. Task-only controls already have positive costs, so positive semantic costs alone do not establish added semantic utility.

## Geometry

Singular values were computed exactly from the small LoRA core after thin QR factorization; this is algebraically equivalent to SVD of the full update matrix. Pairwise cosine uses the exact low-rank Frobenius inner product.

Source supervision increased similarity and reduced effective rank relative to matched task-only experts. The result is opposite to the senior's plotted direction. A plausible interpretation is that one-layer answer fitting retains a dominant shared update direction even when route identities become source-predictive; this interpretation is not itself causally established.

## Loss-Free Bias

The non-gradient bias used update size `1e-3`, mean centering, and clamp `[-0.1,0.1]`. It changed only Top-1 selection, not the auxiliary loss or the learned probability used as the residual coefficient. Its NLL effects were between `-0.000248` and `+0.000092`. It modestly increased task-only load entropy but did not change the primary verdict.

## Deviations And Boundary

- The intended four unavailable datasets were replaced before training; see Protocol C001.
- A stale coarse mapping partial launch was stopped before final checkpoints; see C002.
- A source-ID renaming was discovered in the first shuffled control; the complete suite was rerun after the C003 correction. Only `full-20260902T190657Z` is canonical.
- Evaluation reports teacher-forced answer-token NLL and token accuracy, not benchmark-native free-generation exact match or code execution. This is sufficient for the registered NLL efficiency question but not for standard leaderboard claims.

## Artifact Map

- Aggregate: `/data/250010109/MoE_Router/experiments/20260902_a15_13_e13_qwen06b_mixed_answer_only_semantic_router/runs/full-20260902T190657Z/analysis/aggregate.json`
- Completion audit: `/data/250010109/MoE_Router/experiments/20260902_a15_13_e13_qwen06b_mixed_answer_only_semantic_router/runs/full-20260902T190657Z/completion_audit.json`
- Conditions and histories: `.../conditions/`
- Evaluation arrays: `.../evaluations/`
- Curated figures: [learning curves](figures/answer_only_learning_curves.png), [task and route semantics](figures/task_and_semantic_results.png), [expert geometry](figures/expert_update_similarity.png), [loss-free controls](figures/loss_free_bias_controls.png), [aggregation sensitivity](figures/aggregation_sensitivity.png)
