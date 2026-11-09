# Detailed: E14-P2 parent-only supervision repair

[Primary Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md) · [Protocol](protocol.md), revision `20260906-P2-v1` · [Summary](summary.md).
Execution COMPLETE; eligible matrix; verdict `ONLINE_PARENT_REPAIR_SUPPORTED`.
Interpretation: `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.

## 0. Quick Recap

Question: does adding missing parent supervision restore online dispatch with fixed experts? Four parent-only training conditions (two label conditions × two source checkpoints) and ten full evaluations completed. All eight required full/disjoint original/control contrasts have positive 95% lower endpoints. Mean full NLL is 0.836757276 before and 0.804182618 after repair. No expert or child-Router update, teacher refit, new layer, probability attenuation, or free-generation test occurred.

## 1. Terminology / Definitions

NLL: summed reference-answer negative log probability divided by valid answer-token count, nats/token, lower is better. Parent agreement: count of scored prediction positions whose executed parent equals original pseudo parent divided by scored token count; B/C are forced and therefore trivially 100%. Parent CE measures original classifier logits versus pseudo targets and may remain high in B/C even though executed paths agree perfectly. Do not confuse executed agreement with classifier quality.

Online O/R/S: no forced parent or child provided to model forward; permitted causal states still contain reference previous answer tokens during likelihood evaluation. R changes the parent classifier only. S uses identical learning with shuffled sample-label assignments. B/C supply original pseudo paths and are not gold-trained Oracle models. A record-disjoint subset excludes matching training record IDs; it does not screen semantic near-duplicates or base-pretraining contamination.

## 2. Anchor Link And Decision Point

P1 measured externally supplied parent correction and audited missing parent gradients in the benchmark hard-pseudo trainer. P2 intervenes on that supervision route rather than layer, teacher, architecture or expert responsibility. It adjudicates one local handoff repair; the historical E14 verdict for its original unmodified conditions is not retroactively changed.

## 3. Protocol Freeze, Conformance, And Deviations

All A–G and implementation/smoke/full-run/analysis scopes were explicitly confirmed by the researcher. Worker `protocol_snapshot.md` preserves the approved scientific body. The live protocol contains append-only execution receipts; its draft-era prose is historical, superseded by the approval receipt.

| Registered item | Actual | Status / eligibility |
|---|---|---|
| Only 3075 parent parameters trained | Four standalone parent fits; expert and child tensors exactly unchanged | PASS |
| Two original checkpoints, labels, data | Exact original SHA-256 identities | PASS |
| 128 updates, 4 passes per condition | All four: 128 updates, 911644 target exposures | PASS |
| True/shuffled targets | One fixed train-example permutation, counts preserved; 36.0596% labels unchanged | PASS |
| Last checkpoint, no tuning | Final update 128 in all cases; development only logged | PASS |
| Full and record-disjoint evaluation | 512/30442 and 384/27133 records/tokens respectively | PASS |
| Historical O/B/C replay | Both seeds, smoke and full, zero aggregate and per-example errors; paths exact | PASS |
| Cache and causal input | Matched-shape computations exact; suffix-change hidden/logit max difference zero | PASS |
| Supplied paths invariant to parent replacement | B/C small-sample losses/routes exact under both repaired parent types | PASS |
| Eight conjunctive contrasts | All lower endpoints positive under fixed paired-record bootstrap | PASS |
| Initial smoke failure | Incorrect unequal-shape cache guard stopped first job before formal training | EXCLUDED, engineering-only correction |

The first job `pt-i5ukbgg1` failed because the strict cache check compared logits recomputed over 511 positions with logits from a 512-position calculation sliced afterwards. This violated the intended same-operation comparison. The correction recomputed full-shape logits before masking; no tolerance or scientific variable changed. Failed run `reserved-20260906-p2-v1` is excluded. Replacement fresh run `reserved-20260906-p2-v2` is the only eligible full matrix. No automatic retries, no post-hoc scientific amendment.

The small disposable training checks use two updates on the first eight records per seed/condition; these eight smoke updates are separate from the 512 formal updates and their weights never initialize full training. Smoke can establish gradient reachability and invariants, not task performance.

## 4. Actual Setup And Training Stages

This round has **one parent-only optimization stage per condition**, following offline cache preparation. It does not rerun the historical coarse/fine expert stages and does not convert the original single-stage expert training into a staged experiment.

Base: Qwen3-0.6B-Base, bf16, frozen. Historical expert checkpoints are E14 `benchmark__HIER_GMM_HARD_R8__seed17/final.pt` and seed29 counterpart, final historical update 128. The existing parent linear weight and bias are cast from bf16 to float32 for optimization. A fresh AdamW optimizer is created for each condition. Final parent tensors are cast to bf16 and inserted into the original frozen model for deployment. No newly initialized classifier parameters replace the original starting values.

Trainable: parent weight 3×1024 and bias 3, total 3075. Frozen: base, output head, shared rank-8 expert, three rank-8 coarse experts, eight rank-8 fine experts, child Router and all balance buffers. Route input remains zero-indexed block 14 pre-attention state. Experts remain in that block's down projection. All expert coefficients remain one.

Data: original train 4096 records, 3434 unique IDs, 227911 answer-prediction positions; development 512 records/28576 target positions; full evaluation 512 records/30442 target positions. Each complete training run exposes 911644 target positions over four passes. Sampling uses the unchanged historical source-balanced ordering per source seed and epoch. Teacher: original frozen final-layer whole-sequence means, train-fitted projected hierarchical Gaussian-mixture assignments; no fitting or access to evaluation targets for parameter optimization.

Targets: per-example pseudo parent expanded only at positions predicting nonmasked answer targets. Shuffled labels use NumPy generator seed 20260906, one permutation across all 4096 training records, reused for both checkpoint seeds. Example label counts are [1693,1431,972]; unchanged fraction is 0.360595703125. Counts are not constrained at the answer-token-weighted level because sample lengths differ. The null therefore controls example class frequencies under the same microbatch objective, not every possible token-prior adjustment.

Objective: mean parent cross entropy within each eight-example microbatch, divided by accumulation 16. No language-model loss, child CE or balancing term is optimized. Batch 8 × accumulation 16 gives effective batch 128; 32 updates per pass, four passes, 128 updates. AdamW lr 5e-4, betas (0.9,0.999), eps 1e-8, weight decay .01; five-update warmup then historical cosine decay to zero, gradient norm clip 1.0. Save 0/32/64/96/128 and select final 128 without development selection. Each training stream has 128 finite update rows; nonzero finite parent gradients and actual parent tensor changes are verified. [Training audit](tables/training_audit.json).

Cache preparation reads causal block states from each original checkpoint and preserves bf16 values at answer-prediction positions; row offsets preserve ragged sample boundaries. This is frozen feature extraction, not network training. Float32 cache/direct checks are shape-matched and within 1e-5; actual values are exact. Parent updates cannot affect the pre-adapter block input. All frozen adapter tensors are checked before/after and restored to original after evaluation; the separate parent optimizer has no base/child/expert parameter references.

## 5. Metrics And Registered Decision Rules

Token-weighted NLL is reduced in float64. Primary comparisons: O−R (repair) and S−R (label-specific advantage), each on full and disjoint populations, separately for two seeds. Positive means repair is better. Pass requires all eight percentile 95% lower endpoints positive; non-support requires the same necessary clause to have nonpositive upper endpoints in both seeds; otherwise Insufficient. Finite/missing/hash/freeze failures invalidate or leave incomplete, rather than producing scientific failure.

Bootstrap uses 2000 paired-record draws, NumPy default generator seed 20260906; separate draws for full/disjoint populations and same indices across compared conditions/seeds within each population. Unit of independence is record, not token or model condition. Both populations use their own token denominator on each resample. Mean seed loss is descriptive, not a population-of-training-seeds estimate. This is a conjunction of required evidence, not selection among multiple favorable tests. No exclusions beyond the predeclared record-ID subset and failed smoke.

Recovery fraction is (O−R)/(O−B), with no clipping. Values exceed one because R has lower point-estimate loss than B, not because of an impossible probability or proof of gold-Oracle superiority. Residual R−B/R−C intervals are auxiliary descriptive evidence. [Recovery](tables/recovery.csv), [auxiliary comparisons](tables/auxiliary.csv).

## 6. Evidence Lineage

| Claim | Raw artifact | Computation | Registered criterion | Evidence / boundary |
|---|---|---|---|---|
| Online parent repair helps | Per-seed O/R.npz | Paired loss differences / valid token totals; bootstrap | Full and disjoint lower endpoints positive both seeds | Registered support, conditional on these checkpoints |
| Real association beats shuffled supervision | S/R.npz | Same paired computation | Same four positive endpoints | One fixed example-permutation control, not universal semantic proof |
| Parent learns teacher mapping | Classification histories, evaluated parent counts | Token agreement and CE | Descriptive only | Pseudo-label agreement, not task gain by itself |
| No unrelated parameter changes | Original tensors and per-seed guards | Exact equality outside parent, fresh optimizer membership | All frozen guards pass | Parent-only intervention |
| Historical identity | Original P1 arrays and O/B/C replay | Exact paths and losses | Loss tolerance 1e-4, actual error zero | Excludes evaluator drift explanation |

## 7. Main Results

| Seed | Population | Condition | NLL | Executed parent agreement |
|---|---|---|---:|---:|
| 17 | full | O | 0.845991414 | 24.079% |
| 17 | full | R | 0.804240328 | 87.471% |
| 17 | full | S | 0.839391729 | 38.542% |
| 17 | full | B | 0.806372044 | 100.000% |
| 17 | full | C | 0.805663412 | 100.000% |
| 17 | disjoint | O | 0.843758550 | 24.236% |
| 17 | disjoint | R | 0.806343705 | 86.728% |
| 17 | disjoint | S | 0.839200033 | 41.916% |
| 17 | disjoint | B | 0.808470499 | 100.000% |
| 17 | disjoint | C | 0.808053305 | 100.000% |
| 29 | full | O | 0.827523137 | 31.660% |
| 29 | full | R | 0.804124908 | 86.532% |
| 29 | full | S | 0.839132733 | 34.577% |
| 29 | full | B | 0.805791562 | 100.000% |
| 29 | full | C | 0.804393423 | 100.000% |
| 29 | disjoint | O | 0.824844750 | 33.008% |
| 29 | disjoint | R | 0.806225117 | 85.689% |
| 29 | disjoint | S | 0.837054715 | 37.331% |
| 29 | disjoint | B | 0.808263460 | 100.000% |
| 29 | disjoint | C | 0.807194435 | 100.000% |

[Full source table](tables/conditions.csv).

| Seed | Population | Required comparison | Reduction | 95% interval |
|---|---|---|---:|---|
| 17 | full | O − R | 0.041751086 | [0.035440500, 0.048617485] |
| 17 | full | S − R | 0.035151401 | [0.029974241, 0.040884740] |
| 17 | disjoint | O − R | 0.037414844 | [0.031418940, 0.044384431] |
| 17 | disjoint | S − R | 0.032856327 | [0.027605232, 0.039045552] |
| 29 | full | O − R | 0.023398230 | [0.019733886, 0.027877898] |
| 29 | full | S − R | 0.035007825 | [0.029936917, 0.040916958] |
| 29 | disjoint | O − R | 0.018619633 | [0.014763391, 0.022976717] |
| 29 | disjoint | S − R | 0.030829598 | [0.025683539, 0.036935689] |

| Seed | Population | Auxiliary residual | Difference | Descriptive 95% interval |
|---|---|---|---:|---|
| 17 | full | R − B | -0.002131716 | [-0.003658045, -0.000847448] |
| 17 | full | R − C | -0.001423083 | [-0.003072639, 0.000009051] |
| 17 | disjoint | R − B | -0.002126793 | [-0.003806492, -0.000696556] |
| 17 | disjoint | R − C | -0.001709599 | [-0.003518099, -0.000165261] |
| 29 | full | R − B | -0.001666654 | [-0.003160145, -0.000414858] |
| 29 | full | R − C | -0.000268516 | [-0.001888893, 0.001160550] |
| 29 | disjoint | R − B | -0.002038342 | [-0.003752551, -0.000607943] |
| 29 | disjoint | R − C | -0.000969318 | [-0.002763042, 0.000601656] |

All required comparisons are eligible. No null was discarded. S improves relative to O in seed 17 but worsens in seed 29, whereas R beats both in both seeds. R's point estimates are below B and C; the auxiliary intervals, especially seed29 R−C, must be consulted before asserting superiority. No separate task-only or gold-Oracle model was evaluated in this round. Per-source losses and condition-specific correct/wrong-parent strata are in [source and strata table](tables/source_and_strata.csv); strata are selected by each condition's route and are descriptive, not a matched causal subgroup contrast.

## 8. Visualization Audit

![Registered online repair contrasts](figures/online_parent_repair.png)
Question: does parent-only learning improve task loss beyond original and shuffled routing? Source: paired arrays through conditions/contrasts tables. Left x-axis: O/R/S/B/C; y: answer NLL in nats/token. Right x-axis: O−R/S−R; y: NLL reduction with 95% intervals. Blue/orange are seeds17/29; upper/lower rows are full/disjoint populations. All eight lower endpoints are positive. Both PNG panels are visually inspected; labels/units readable and intervals trace to tables. It cannot establish clean eight-task generalization or a gold-Oracle advantage.

![Readout evidence](figures/parent_readout_and_task.png)
Question: did the parent learn the intended mapping, and is that accompanied by task improvement? Left x: optimizer updates, y: development true-pseudo-parent agreement; solid R versus dashed S. Right x: full-evaluation agreement, y: NLL reduction versus original for each condition. Sources: classification history and condition tables. Both real-label curves improve and both task deltas are positive. Rendered labels and scales inspected. No regression or accuracy-to-loss causal slope is fitted; development includes overlapping records and is monitoring only. No debug-run result is plotted.

## 9. Stage Evidence And Failure Decomposition

Identity/cache: PASS; smoke: PASS after unequal-shape guard correction; four parent fits: PASS; ten full evaluations: PASS; fixed analysis: PASS. Original parent supervision absence is an implementation defect; P2 shows a narrow repair suffices to remove the original large online task-loss deterioration on this workload. It does not falsify all layer/context mismatch hypotheses. The offline labels remain imperfect/proxy labels, and training still sees privileged targets, while inference uses causal states.

## 10. Full Experiment Record

Job `pt-diap9xc9` SUCCEEDED, single reserved H100 80GB worker `n6ls.iu.i40.1`; job start 2026-09-06 10:44:34 UTC, runner start 10:45:01 UTC. Runner elapsed **128.280 seconds** including checks, caches, smoke, training and evaluation, excluding scheduling and separate local analysis. Image: `registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04`. Runtime: Python 3.12.3, PyTorch 2.8.0a0+5228986c39.nv25.06, Transformers 4.53.3, NumPy 1.26.4. Local analysis: float64 NumPy reductions and matplotlib; its script hash is in the artifact manifest. Tests: 3 passed in the cloud; initial local missing-module RED followed by GREEN was recorded in task execution.

Formal updates: 512 across four fits. Disposable smoke updates: 8 separately. Frozen references: six full evaluations; learned conditions: four full evaluations. All evaluation calls use batch 8. Prior failed job: `pt-i5ukbgg1`, excluded; no successful partial training from it was reused.

## 11. Interpretation

Observed: correct sample-label supervision of only the parent layer outperforms both original and shuffled controls. AI interpretation: missing parent supervision is a sufficient practical explanation for the large handoff loss in these fixed models; the earlier experiment was not an adequate falsifier of final-layer semantic supervision itself. This does not prove that the label semantics are optimal or that better label prediction always improves tasks. In fact R's lower point-estimate task loss than forced labels illustrates that exact offline-label imitation is not the task objective.

## 12. Claim Boundary

Can claim the registered parent-only repair succeeds in this internal answer-likelihood workload under fixed budget. Cannot claim clean public-task generalization, free-generation gains, universally semantic experts, best insertion layer, best teacher context, or successful staged expert training. Disjoint subset excludes two sources and only addresses exact record IDs. Only one null permutation was used. No prior historical gold/task-only comparison is promoted into a new paired result here.

## 13. One Next Decision

Use the repaired checkpoints as the candidate fixed online baseline for subsequent teacher/readout diagnosis, subject to the researcher's knowledge confirmation. Completion criterion: preserve the verified checkpoint identities and audited loss boundary; do not start a third-step label change solely to explain the now-repaired original gap. No further experiment was launched.

## 14. Artifact Manifest

[Manifest](tables/artifact_manifest.json): raw evaluation arrays, four trained parent checkpoints, per-update logs, subset/permutation, frozen protocol and producer hashes. [Execution metadata](tables/execution_metadata.json): data/pseudo/source identities, per-seed replay/causal/freeze/training guards and runtime. [Training audit](tables/training_audit.json) and [classification history](tables/classification_history.json) are curated extracts. Raw cached representations, checkpoints and logs remain on the worker; no publication, commit or push occurred.

## 15. Reproduction And Links

Worker: `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair`.
Eligible run: `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/runs/reserved-20260906-p2-v2/full`.
Analysis: `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p2_parent_router_supervision_repair/runs/reserved-20260906-p2-v2/analysis`.
Run command: `RUN_STAMP=reserved-20260906-p2-v2 timeout 5400 bash <worker>/run_remote.sh`.
Analysis command: `python <worker>/analyze.py --run <eligible-run> --output <analysis>`.
Final parent checkpoints: `<eligible-run>/seed17/R/final.pt` and `seed29/R/final.pt` (S counterparts are controls). These contain parent tensors only: load the corresponding original E14 full adapter, then cast and replace only parent tensors with bf16 values. They are not standalone language-model checkpoints. Preserved source hashes and the original adapter path are required for reconstruction.
