# Detailed Record: A15_13_E14 Diagonal-GMM Pseudo-Label Oracle-Gap Audit

Result status: `FULL_RUN_COMPLETE`; knowledge wording: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## 1. Provenance And Completion

- Canonical worker: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap`
- Canonical run: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z`
- Resource: one reserved ACP worker with four H100 GPUs; conditions were sharded one independent process per GPU.
- Final evaluation job: `pt-nu12nw5x`, completed the batched no-KV-cache benchmark evaluation, analysis, figures, and audit.
- Tests after the final implementation fixes: `30/30` passed; Python compilation and shell syntax checks passed.
- Completion: `30/30` registered training checkpoints; frozen Base reuse entry; 165 NLL/intervention arrays; 21 benchmark model outputs; 10,752 item predictions; eight analysis tables; five figures.
- Completion audit: `FULL_RUN_COMPLETE`, zero errors.
- Checkpoint-manifest SHA-256: `b74f4675b566cc222081a7a787d0cd7d853fe3aa89c3658d21f3158a1d85ef0a`.
- Completion-audit SHA-256: `f372536f783a84d632f06f2cb414eb17820670719c471bb506f0a508603f18c8`.

The registered typed verdict is `B`: semantic structure is visible offline, but neither the ordinary learned GMM route nor the hard-pseudo training route converts it into a two-seed task and learning-efficiency gain over matched task-only training.

## 2. Data And Frozen Label Construction

### 2.1 M2D2-Wikipedia `3×3`

The frozen processed file was `/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt`, SHA-256 `8cd04d99ad2576d8a149dc145c83b29d5a977178419304c4490cf8e10cba51a8`. It contains nine fine domains under three coarse domains, with 1,024 train, 256 development, and 512 confirmation windows per fine domain. Every window has 256 tokens. Positions 0--63 provide context, and positions 64--255 receive standard next-token cross entropy. Domain names are absent from input.

### 2.2 Eight-task answer-only mixture

The sources were MMLU, MMLU-Pro, BBH, GSM8K, MATH, GPQA Diamond, HumanEval, and MBPP. Each source contributes 512 train, 64 fixed-development, and 64 internal-evaluation records, for 4,096/512/512 total records. Sequence length is 512. Prompt positions are masked; only reference-answer tokens plus end-of-sequence receive cross entropy.

- Processed tensor SHA-256: `e6320e7aba92c8d9caa36ce43bda5d695843070a54955e63776893334d58a6b6`.
- Data manifest SHA-256: `864a378dd2c21580421a19b93ad0294cc1375c631ea68a3a8d5ae89e9ca9e379`.
- One train pass contains 227,911 answer tokens; four passes contain 911,644 answer tokens.
- Development contains 28,576 answer tokens; internal evaluation contains 30,442.
- GPQA Diamond has 198 unique records and HumanEval has 164, so deterministic cycling creates repeated records and possible train/evaluation overlap. The researcher explicitly allowed this for controlled comparison. All eight-task scores are therefore called **within-mixture internal capability diagnostics**, not uncontaminated benchmark generalization.
- GPQA was frozen from the public artifact used by OpenAI `simple-evals` at revision `652c89d0ca9df547706735883097e9537d40dc47`; the CSV SHA-256 is `41d1213cd7a4998605a26c2798500652572007161b3a92817ba46b35befcd305`.

### 2.3 Diagonal-GMM pseudo labels

Qwen3-0.6B-Base was frozen. The labeler averaged final-layer states over the complete input window, fitted a 64-dimensional principal-component basis on train representations only, and fitted a three-parent diagonal-covariance Gaussian mixture. Children were then fitted inside the predicted parent assignments. M2D2 uses `3+3+3` leaves; the eight-task surface uses `3+3+2`, assigning fewer children to the smallest parent cluster by a train-only deterministic rule. Every mixture used 20 deterministic restarts, at most 100 expectation-maximization iterations, and train likelihood alone for selection. Truth labels were excluded from fitting, restart selection, and assignment freezing.

Post-hoc truth audits show that the frozen labeler captured task/source structure:

| Surface | Parent NMI | Leaf NMI | Evaluation or confirmation leaf counts |
| --- | ---: | ---: | --- |
| Eight-task internal evaluation | `0.601225` | `0.592382` | `[122, 39, 48, 87, 55, 39, 60, 62]` |
| M2D2 confirmation | `0.239146` | `0.516524` | `[571, 333, 1635, 271, 215, 540, 505, 460, 78]` |

Normalized mutual information, or NMI, measures agreement between two partitions after ignoring arbitrary cluster names. It ranges from zero to one. These values prove offline accessibility of source/domain structure, not causal Router recovery or task value.

## 3. Model And Training Behavior

### 3.1 Shared architecture boundary

- Base and language head: frozen Qwen3-0.6B-Base.
- Injection point: only zero-indexed transformer block 14 MLP `down_proj`.
- Hierarchy: one shared, one selected parent, and one selected leaf rank-eight LoRA residual per token; active LoRA rank is 24.
- Flat: one selected rank-24 expert per token.
- Dense: one rank-24 LoRA.
- Online Routers read only the current and previous causal block-14 state. Future-token perturbation tests passed.
- No coarse-Router-row-space subtraction was used.

Trainable storage differs across topology, although active rank is aligned:

| Topology | Trainable parameters | Active parameters per token |
| --- | ---: | ---: |
| Dense rank 24 | `98,304` | `98,304` |
| Flat rank-24 bank | `794,632` | `106,504` |
| Eight-task hierarchy | `404,491` | `109,579` |
| M2D2 hierarchy | `438,284` | `110,604` |

Therefore comparisons within one topology are parameter matched. Dense, flat, and hierarchical models are active-rank and approximate active-compute controls, not equal-storage-parameter controls.

### 3.2 Registered conditions

M2D2 trained five conditions per seed: GMM learned route; GMM learned route plus gradient-free load bias; GMM hard-pseudo path training; hard-pseudo plus load bias; and frequency-matched random pseudo labels.

The eight-task surface trained ten conditions per seed: dense rank-24 LoRA; flat task-only; hierarchical task-only; frequency-matched random hierarchy; gold-source-supervised hierarchy; GMM learned route with and without load bias; GMM hard-pseudo path with and without load bias; and gold-source unit-coefficient Oracle.

### 3.3 M2D2: genuine two-stage training

| Stage | Trainable objects | Frozen objects | Passes | Updates | Effective batch | Objective | Optimizer schedule | Handoff |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
| 1, coarse | shared LoRA, coarse experts, coarse Router | base, language head, fine experts, fine Router | 2 | 144 | 128 windows | target-token NLL plus unit-weight coarse route CE | AdamW; LoRA `2e-4`, Router `5e-4`, weight decay `0.01`; 5-update warmup, cosine decay, clip `1.0` | save update 144; freeze only coarse Router |
| 2, fine | shared LoRA, coarse experts, fine experts, fine Router | base, language head, coarse Router | 2 | 144 | 128 windows | target-token NLL plus unit-weight fine route CE | optimizer and schedule restart with the same settings | fixed final checkpoint at update 288 |

Microbatch was 8 and gradient accumulation was 16. Every full condition saw 7,077,888 target tokens. Hard-pseudo models selected the frozen pseudo expert with coefficient one during expert training while also training a shadow Router. At deployed evaluation they used the shadow causal Router's hard top-one path with coefficient one. A separately reported forced-pseudo evaluation supplied the offline path and is not deployable.

### 3.4 Eight-task continuation: one-stage by design

Each condition used seeds 17 and 29, four deterministic data passes, 128 optimizer updates, microbatch 8, gradient accumulation 16, and effective batch 128. AdamW used weight decay `0.01`; LoRA learning rate was `2e-4`, Router learning rate `5e-4`, warmup five updates, cosine decay, and gradient clipping `1.0`. The checkpoint rule was fixed before training, and the final update was always selected.

The route cross entropy had weight one and updated Routers only. For learned routes, task loss also flowed through the selected route probability coefficient. Hard pseudo and Oracle expert training used unit coefficient. Gradient-free load bias changed only top-one selection; it received full-effective-batch token counts and never entered the loss.

## 4. Unified Evaluation Definitions

- **Answer-token NLL:** summed reference-answer negative log probability divided by the number of answer tokens; nats/token, lower is better. This is the primary task-fit quantity.
- **Normalized loss-curve area:** trapezoidal development NLL over seen answer tokens divided by the total token budget; lower means faster learning at the same budget.
- **Task score:** native multiple-choice accuracy, strict match, final-answer accuracy, or executable `pass@1`, then unweighted mean over the eight tasks. It is an internal capability guard, not a clean generalization estimate.
- **Route semantics:** route/source NMI and mapped route accuracy. These indicate what the Router partitions resemble but cannot prove task gain.
- **Selective expert utility:** changed-minus-intact answer-token NLL after deleting the chosen expert or replacing it. Positive values mean the original selected expert mattered functionally.
- **Parameter geometry:** pairwise low-rank update cosine, singular values, stable/effective rank, and update norm. These describe parameters and cannot independently prove function.

All generation used the same task-specific prompt, greedy decoding, answer extractor, no KV cache, and batches of eight same-task examples. HumanEval and MBPP used actual subprocess test execution under Python isolated mode, a two-second CPU limit, 512 MB address-space limit, one-megabyte file limit, 32 file descriptors, and eight processes. This is process-level containment, not a separate network-isolated operating-system sandbox.

## 5. Task And Learning-Efficiency Results

The complete seed-resolved eight-task table is in [summary.md](summary.md) and [tables/01_benchmark_table.csv](tables/01_benchmark_table.csv).

### 5.1 Primary NLL

| Condition | Seed 17 | Seed 29 | Mean |
| --- | ---: | ---: | ---: |
| Frozen Base | — | — | `0.908483` |
| Dense rank-24 LoRA | `0.849371` | `0.849127` | `0.849249` |
| Flat task-only | `0.828130` | `0.834529` | `0.831329` |
| Hierarchical task-only | `0.807642` | `0.805004` | `0.806323` |
| Frequency-matched random | `0.821347` | `0.817804` | `0.819575` |
| Source-supervised | `0.808483` | `0.807951` | `0.808217` |
| GMM learned route | `0.818518` | `0.816198` | `0.817358` |
| GMM learned + load bias | `0.818298` | `0.816237` | `0.817267` |
| GMM hard-pseudo training | `0.845991` | `0.827523` | `0.836757` |
| Hard-pseudo + load bias | `0.846379` | `0.828301` | `0.837340` |
| Gold-path Oracle | **`0.796570`** | **`0.793270`** | **`0.794920`** |

The learned GMM route is worse than task-only by `0.010876` and `0.011194` NLL in seeds 17 and 29. Hard-pseudo training is worse by `0.038349` and `0.022519`. Oracle is better than task-only by `0.011072` and `0.011734`.

### 5.2 Learning efficiency

Mean normalized curve areas were Oracle `0.834334`, task-only `0.839792`, GMM learned `0.848492`, and hard-pseudo `0.865017`. Relative to Oracle, the learned-GMM gaps were `0.014064` and `0.014253`; hard-pseudo gaps were `0.035961` and `0.025405`. Only Oracle and task-only reached the task-only 75%-budget target; GMM models never reached it within the registered budget.

![Learning efficiency](figures/01_learning_efficiency.png)

How to read: lower is better at every equal answer-token budget. The hard-pseudo curve moves away from Oracle.

### 5.3 Eight-task macro score

Two-seed macro means were Base `12.11%`, dense `13.77%`, flat task-only `13.67%`, hierarchical task-only `15.82%`, GMM learned `15.04%`, hard-pseudo `14.36%`, and Oracle `16.50%`. Oracle exceeded task-only in both seeds by `0.98` and `0.39` percentage points. GMM learned was below task-only in both seeds by `1.37` and `0.20` points. Hard-pseudo was below by `2.15` and `0.78` points.

Because each task has only 64 evaluation items and two seeds, task-level changes are coarse and high variance. The NLL and curve-area agreement provides the firmer decision evidence.

## 6. Routing, Load, And Causal Localization

The GMM learned Router's route/source NMI was `0.370888` and `0.314242`, versus task-only `0.375344` and `0.096651`. It therefore failed the Protocol requirement to improve semantic agreement over task-only in both seeds. Its frozen-pseudo-leaf accuracy was `0.195125` and `0.446751`; the frequency-only leaf majority was `0.263058`. Parent accuracy was `0.206557` and `0.530616`, below the parent majority `0.583405` in both seeds.

The hard-pseudo shadow Router was weaker: pseudo-leaf accuracy `0.218415` and `0.283227`, and parent accuracy `0.240786` and `0.316602`. This shows that training experts on offline labels does not make the causal Router recover those labels.

The strongest localization comes from forcing the frozen pseudo path at evaluation:

| Hard-pseudo condition | Deployed causal NLL | Forced-pseudo NLL | Forced minus deployed |
| --- | ---: | ---: | ---: |
| Seed 17 | `0.845991` | `0.805663` | `-0.040328` |
| Seed 29 | `0.827523` | `0.804393` | `-0.023130` |
| Mean | `0.836757` | `0.805028` | **`-0.031729`** |

This is evidence that the online path handoff is a major bottleneck. It is not evidence that each pseudo label corresponds to a uniquely correct expert, because forced wrong pseudo labels were not compared.

Load bias did not pass its registered gate. For learned GMM, it improved NLL by `0.000220` in seed 17 but worsened it by `0.000039` in seed 29. For hard-pseudo, it worsened both seeds by `0.000388` and `0.000778`. Although macro scores rose in both seeds, the primary NLL and Oracle-gap result did not, so the method is not adjudicated effective.

## 7. Expert Function And Parameter Geometry

Changed-minus-intact mean NLL:

| Condition | Delete selected | Wrong leaf in same parent | Wrong expert in other parent |
| --- | ---: | ---: | ---: |
| Hierarchical task-only | `+0.024529` | `+0.023494` | `+0.051461` |
| GMM learned route | `+0.014830` | `+0.011947` | `+0.040649` |
| GMM hard-pseudo training | `+0.011095` | `+0.007851` | `-0.000828` |
| Gold-path Oracle | `+0.029325` | `+0.024341` | `+0.049011` |

Task-only already forms strongly non-interchangeable experts. Learned GMM expert effects are positive but weaker. In the hard-pseudo model, replacing the deployed expert with one from another parent slightly improves NLL on average, so its deployed route fails the strongest functional test.

Parameter geometry is secondary. For leaves, mean pairwise update cosine was task-only `0.022491`, GMM learned `0.048732`, hard-pseudo `0.228752`, and Oracle `0.147195`. Effective ranks were `2.908942`, `3.002933`, `1.514611`, and `1.479596`, respectively. Hard training therefore creates more similar, lower-rank expert updates, not stronger functional specialization. Geometry is consistent with the functional failure but cannot cause-identify it.

## 8. M2D2 Secondary Surface

M2D2 was the exact staged-training check. Mean final NLL was random `2.886909`, GMM learned `2.884899`, GMM learned plus bias `2.884930`, hard-pseudo `2.883648`, and hard-pseudo plus bias `2.883595`. GMM route/source NMI was about `0.283`, versus random `0.003`; pseudo-target accuracy was about `0.558`, versus random `0.337`.

These descriptive effects confirm that the staged implementation runs and that a causal Router can partially reproduce M2D2 pseudo labels. This new E14 M2D2 subset does not contain a contract-matched task-only and Oracle pair under the same reimplemented code path, so it is not used to override the eight-task primary verdict.

The requested diagonal-GMM versus old direction-plus-radius comparison has one positive representation result and no positive task result. E09's train-only frozen-state audit reported fine-domain confirmation NMI `0.444` for direction plus radius and `0.524` for diagonal GMM. However, only direction-plus-radius labels were trained in E09, and its saved adapter schema differs from E14's. The old Router therefore could not enter the unified E14 evaluator as an unchanged model. Its historical NLL (`2.881270`) is lower than the new E14 GMM learned-route NLL (`2.884899`), but this cross-implementation difference is contextual rather than a clean causal contrast. The bounded answer is: diagonal GMM improves offline label agreement, but no evidence here shows that it improves the downstream causal Router or task NLL over direction plus radius.

## 9. Failure And Repair Ledger

No failed attempt was deleted.

| Job or run | Outcome | Cause | Repair and eligibility |
| --- | --- | --- | --- |
| `pt-zziy20du`, `full-20260903T035001Z` | failed before training | ACP could not reach Hugging Face | data were downloaded and revision-frozen on the directly connected local host; run ineligible |
| `pt-awh3pyxg`, `full-20260903T044500Z` | failed before checkpoints | bfloat16 diagnostic arrays could not be serialized through NumPy | cast diagnostic confidence arrays to float32 and add regression test; run ineligible |
| `pt-539b664j`, canonical run | training and NLL complete; benchmark stage failed | tokenizer was referenced through a runtime module that did not export it | import tokenizer directly; all 30 checkpoints and 165 arrays retained |
| `pt-ay47ocja`, canonical evaluation resume | manually stopped, zero complete model outputs | single-example no-cache generation was valid but too inefficient | replace only batching with batches of eight same-task samples; decoding semantics unchanged |
| `pt-nu12nw5x`, canonical evaluation resume | succeeded | batched no-cache evaluation | produced every per-item prediction, analysis table, figure, and final audit |

Two further correctness fixes were made before final analysis: expand MMLU-Pro answer parsing from `A--D` to `A--J`, and ensure pseudo-hard paths use unit coefficient only during forced-label expert training while deployed evaluation uses the learned causal hard top-one route.

The current SCO client could not re-query remote job states after completion because its workspace decoder rejects a newer server field. Local immutable artifacts, terminal-observed outcomes, the successful final job output, and the completion audit are the evidence owners for this ledger.

## 10. Verdict, Boundary, And Proposed Next Decision

### Direct result

The gold route has real value, but the present diagonal-GMM label-to-causal-Router handoff does not recover it. Hard-pseudo training increases the deployment gap. Gradient-free load bias does not stably repair the primary NLL. The registered outcome is `B`.

### Can claim

1. Frozen final-layer whole-window representations contain source/task structure readable by diagonal-GMM clustering.
2. Correct unit-coefficient source routing improves both NLL and the internal macro score relative to matched task-only in both seeds.
3. Experts trained on frozen pseudo paths become much better when those same paths are externally restored, localizing substantial loss to causal route recovery.
4. The current learned Router, hard-pseudo training, and load-bias variant do not deliver a stable task or efficiency gain.

### Cannot claim

1. The clusters represent reasoning semantics rather than dataset source or topic.
2. The eight-task scores are uncontaminated benchmark-generalization results.
3. Forced-pseudo experts are semantically matched or uniquely functional without forced-wrong-pseudo interventions.
4. More clustering methods, more seeds, or different causal Router inputs would necessarily fail.
5. Parameter spectra establish expert function.

### One proposed next decision, awaiting human confirmation

Test a prefix-conditioned teacher-to-Router handoff while holding the hard-pseudo expert bank fixed. Add forced-correct-pseudo and frequency-matched forced-wrong-pseudo interventions. Stop this route unless both seeds reduce the `0.031729` deployed-versus-forced gap, move final NLL toward task-only or Oracle, and increase selective expert cost.

## 11. Artifact Map

- Checkpoint manifest: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/checkpoint_manifest.json`
- Completion audit: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/completion_audit.json`
- Frozen pseudo labels and traces: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/pseudo_labels/`
- Checkpoints and histories: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/conditions/`
- NLL, routes, and interventions: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/evaluations/`
- Per-item benchmark predictions: `/data/250010109/MoE_Router/experiments/20260903_a15_13_e14_gmm_pseudolabel_oracle_gap/runs/full-20260903T042000Z/benchmark/`
- Curated tables: [tables](tables)
- Curated figures: [learning efficiency](figures/01_learning_efficiency.png), [task scores](figures/02_benchmark_average.png), [Oracle gap](figures/03_oracle_gap.png), [expert interventions](figures/04_expert_function.png), and [route semantics](figures/05_route_semantics.png)
