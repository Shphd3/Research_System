# Protocol: A15_15_E02 Exploratory Functional Candidate Test

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_EXPLORATORY_RUN
Approval status: HUMAN_CONFIRMED in the 2026-09-07 execution request
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: Anchor/Focus formalization, implementation, tests, GPU smoke, one reserved 4xH100 ACP job, all 24 conditions, fixed-model interventions, frozen analysis, and run-status handoff
Design frozen at: before the first E02 optimizer update
Purpose: identify which of blocks {0,10,13} combines correct-group task value with matched child-expert function and compare that ordering with static readability
Primary Anchor: A15.15 layerwise readability-guided MoE insertion validation
Anchor decision question: which tested candidate has replicated positive overall specialization, correct-grouping, and same-parent expert-match value
Anchor physical prior tested: static accessibility is useful only when direct task and expert intervention evidence agree
Anchor core model term tested: H_l,s = min(A_l,s, F_l,s, W1_l,s, W2_l,s)
Anchor falsifier: no tested layer has H>0 in both seeds, or the ordering reverses/remains unresolved
Experiment role: exploratory operationalization and functional comparison
Primary metric from Anchor: confirmation H in nats per target token, separately for seeds 17 and 29
Claim boundary from Anchor: functional position among three tested candidates only
Minimal setup: frozen Qwen3-0.6B-Base, M2D2 3x3, blocks 0/10/13, four arms, two seeds
Treatment and controls: correct forced hierarchy versus ordinary rank-24 adapter and matched shuffled forced hierarchy; task-only online hierarchy is auxiliary
Changed variable: insertion block and registered adapter/routing condition
Held fixed: model, data, labels, Router input A, expert input, target mask, exposure, active rank, training budget, and evaluator
Conditions to run: 3 blocks x 2 seeds x 4 conditions = 24, plus two wrong-child evaluations for each correct forced checkpoint
Pass: exactly one tested layer has replicated H>0 and a paired-bootstrap-resolved lead
Fail: no tested layer has matched functional value in either seed under the typed rule
Insufficient: seed reversal, multiple unresolved functional layers, missing/ineligible arm, or failed validity guard
Cannot claim: a 28-layer optimum, earliest specialization layer, universal depth law, or retroactive E19 qualification
Approval decision: preserve E19 failure and execute this independent exploratory experiment on reserved 4xH100
```

Confirmed Focus: [focus_layerwise_moe_insertion_validation.md](../../../../focus/focus_layerwise_moe_insertion_validation.md)

## 1. Terminology / Definitions

- **Site A:** the tensor entering the selected Transformer block. It remains the only Router input.
- **Expert input:** the activation entering that block's MLP down projection. Adapter deltas are added to the down-projection output.
- **Ordinary adapter (`DENSE_R24`):** one rank-24 low-rank update, with no semantic hierarchy or Router.
- **Task-only hierarchy (`H_TASK_ONLINE`):** shared, parent, and child rank-8 banks; parent/child Routers receive only next-token gradients through selected route probabilities.
- **Correct forced hierarchy (`H_CORRECT_FORCED`):** true parent and child labels select the hierarchical expert path with unit coefficients and no Router parameters.
- **Shuffled forced hierarchy (`H_SHUFFLED_FORCED`):** the parent remains true while an existing seed-specific balanced within-parent shuffled child label selects the child expert, again with unit coefficients and no Router.
- **Same-parent wrong-child evaluation:** hold a trained correct forced model fixed and replace the true child expert by either of the two other child experts under the same parent.
- **Historical confirmation:** the frozen confirmation split has been viewed in prior work; it is a matched exploratory evaluation surface, not untouched confirmation.

## 2. Anchor Alignment

E01 showed that higher static readability can improve route-label accessibility without reproducibly improving task or expert function. E19 then nominated site-A candidates `{0,10,13}` but failed its old all-null-pass static qualification. The researcher explicitly preserves that negative static verdict and independently authorizes a direct functional comparison. E02 therefore tests task value and expert matching rather than treating static readability as truth.

## 3. Tested Hypothesis

Block 10, the highest-readability tested candidate, will have positive ordinary-minus-correct, shuffled-minus-correct, and both wrong-child-minus-correct NLL differences in each seed, and its conservative bottleneck score will exceed blocks 13 and 0 under paired article-component resampling.

## 4. Rival Explanations

1. Readability measures accessible labels but not function; block 10 does not dominate task or intervention effects.
2. Any apparent gain comes from hierarchical capacity rather than correct semantic matching; the ordinary active-rank and shuffled-topology controls separate this.
3. A task-only online hierarchy matches or beats forced correct grouping, so routing/training dynamics rather than label partition dominate.
4. A layer effect is a seed or packed-article-component artifact; both seeds and paired component resampling expose this.

## 5. Data Construction And Provenance

| Item | Frozen value |
|---|---|
| Model | `/data/250010109/model_cache/Qwen3-0.6B-Base-official` |
| Model revision | `da87bfb608c14b7cf20ba1ce41287e8de496c0cd` |
| Model weights SHA-256 | `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba` |
| Data | `/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt` |
| Data SHA-256 | `8cd04d99ad2576d8a149dc145c83b29d5a977178419304c4490cf8e10cba51a8` |
| Cells | 3 parents x 3 local children |
| Windows per child | train 1,024; development 256; historical confirmation 512 |
| Context / target positions | context 0--63; next-token targets 64--255 |
| Article provenance | reuse E19 exact article manifest SHA-256 `7e4b29ab4da00be9bf2fce74d9930acf9764367b9347f548b965e674a7669958` |

All layers and conditions use identical stored row order. Existing `random_children[seed_17_{split}]` and `random_children[seed_29_{split}]` provide legal balanced local-child labels for shuffled forced conditions; they never alter the parent. Domain names or future tokens never enter model inputs.

## 6. Learning Task And Permitted Supervision

The task is causal next-token prediction. Loss covers exactly 192 targets per 256-token window. True parent/child labels may select paths only in correct forced conditions and the two fixed wrong-child interventions. Shuffled conditions use only the frozen within-parent shuffled child field. Task-only online conditions receive no route classification loss. Confirmation labels do not select a checkpoint, layer, hyperparameter, or exclusion.

## 7. Model / Architecture And Frozen Variants

All `596,049,920` base-model and language-head parameters are frozen. One selected block is instrumented so the Router reads site A and every adapter bank consumes the down-projection input.

| Condition | Active update | Router | Route | Coefficient | Decision role |
|---|---|---|---|---|---|
| `DENSE_R24` | one rank 24 | none | single path | one | active-rank ordinary-adaptation control |
| `H_TASK_ONLINE` | shared + parent + child, each rank 8 | parent and leaf linear Routers | causal top-1 within legal parent | selected probabilities | learned-path auxiliary |
| `H_CORRECT_FORCED` | shared + correct parent + correct child, each rank 8 | none | true labels | one | correct specialization treatment |
| `H_SHUFFLED_FORCED` | shared + correct parent + shuffled within-parent child, each rank 8 | none | frozen shuffled labels | one | matched topology and capacity control |

The ordinary and hierarchical conditions match active rank 24, not total parameter count. Correct and shuffled forced variants intentionally omit shadow Routers. All conditions start from seed-controlled fresh adapter parameters and do not share trained weights.

## 8. Training Objective And Optimization

- Objective: mean causal language-model cross-entropy over targets 64--255 only; no route or auxiliary classification loss.
- Updates: exactly `512` optimizer steps per condition.
- Microbatch / accumulation / effective batch: `8 / 16 / 128` windows.
- Exposure: `65,536` window draws and `12,582,912` target tokens per condition.
- Optimizer: AdamW; expert-bank LR `2e-4`; online Router LR `5e-4`; weight decay `0.01`.
- Schedule: 26-step linear warmup followed by cosine decay to update 512; gradient clipping `1.0`.
- Stream: deterministic seed-specific repeated permutations of all 9,216 train windows; a condition's exact permutation epoch and offset are checkpointed.
- Selection: no early stopping or best-development selection; update 512 is the only final checkpoint.
- Numerical stop: any non-finite loss, gradient, parameter, or evaluation value fails the affected worker and prevents analysis completion.

## 9. Conditions, Seeds, And Checkpoints

Blocks are `0,10,13`; seeds are `17,29`; condition names are the four rows in Section 7. The first wave is block 10, seed 17, all four conditions on four separate GPUs. The remaining 20 conditions follow a frozen persistent four-worker assignment.

Every condition atomically writes `latest.pt` at least every four updates with adapter, optimizer, scheduler, Python/NumPy/CPU/CUDA random states, stream epoch/offset, update count, condition identity, and code/config/data identities. Snapshots at updates `0,1,4,32,128,256,384,512` remain immutable. Each successful condition writes `final.pt`, `train_history.jsonl`, and `completion.json`.

## 10. Primary Metric And Frozen Analysis Plan

For each seed and layer, historical-confirmation NLL is first averaged over target tokens within a window, then over windows within each of the nine cells, then equally over cells. Let

\[
A=N^D-N^C,\quad F=N^S-N^C,\quad G=N^T-N^C,\quad
W^k=N^{Wk}-N^C,\quad H=\min(A,F,W^1,W^2).
\]

The analysis reports every component and seed. A layer is matched-functional only if \(H>0\) in both seeds. Among passing layers, a unique functional position requires the largest two-seed mean \(H\) and a positive 2.5th percentile for both paired differences from that layer to each competitor.

Uncertainty uses exactly 2,000 replicates with seed `20260909`. Within each M2D2 cell, resample connected article components with replacement and retain all windows in each sampled component. The same replicate indexes apply to every condition, intervention, and layer within a seed. Missing or failed conditions are never imputed or excluded. There is no multiplicity-adjusted global-depth claim because only three frozen candidates are tested.

Static ordering is frozen from E19 site-A two-seed mean joint recovery: block 10 `1.000000`, block 13 `0.920233`, block 0 `0.077255`, hence `10 > 13 > 0`. Report the exact functional order and its Spearman correlation with this three-layer order; this diagnostic cannot rescue a failed \(H\) rule.

Typed outcomes:

- `FUNCTIONAL_POSITION_AMONG_TESTED`: exactly one layer has \(H>0\) in both seeds and paired-bootstrap-resolved superiority.
- `MULTIPLE_TESTED_FUNCTIONAL_POSITIONS`: at least two layers have replicated \(H>0\) but the winner is unresolved.
- `NO_MATCHED_FUNCTIONAL_POSITION`: every layer has one or more non-positive required components in both seeds.
- `INSUFFICIENT`: seed directions conflict, a top-layer comparison overlaps zero, an arm is missing/ineligible, or a guard fails.

## 11. Secondary Metrics And Guards

Report development and historical-confirmation NLL; online parent/child route accuracy, normalized mutual information, entropy, and loads; \(G\) as the task-only learned-path gap; update-time development snapshots; gradient norms; throughput; and per-condition exposure. These are diagnostic and cannot replace \(A\), \(F\), or \(W\). Article-component intervals may be low-information in cells dominated by a giant component; report this without adding a post-hoc gate.

Required guards include model/data/config hashes, candidate list and static-order hash, base parameter identity before/after, optimizer membership, A-site state identity, down-projection expert input, legal shuffled/true/wrong paths, unit forced coefficients, identical evaluation row IDs and target counts, exact 512 updates, complete recovery payloads, finite values, and output-path uniqueness.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: forced correct parent and leaf routes exactly equal stored labels and all forced coefficients equal one.
- Known good: replacing a child by offsets `+1` or `+2 mod 3` preserves its parent and changes every local child.
- Known bad: a forced variant containing Router parameters, a trainable base parameter, a B-site Router state, or unequal target counts.
- Known bad: a recovery checkpoint missing optimizer, scheduler, randomness, or stream position.
- Known confusing: positive route-label agreement without positive task and wrong-expert differences is not matched expert function.
- Known confusing: support for block 10 is only support among `{0,10,13}`, not an all-layer optimum.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input and assumptions | How | Why | Expected output | Pass / fail / insufficient | Named failure | Artifact | Handoff |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Validate contract | frozen model/data/config | tests plus real-tensor one-update smoke for four first-wave arms | protect site, route, freeze, recovery, and exposure identity | smoke receipts and checkpoints | every guard passes / stop / missing environment | implementation or environment | `preflight/`, `smoke/` | permits full matrix only |
| 2 | Train full matrix | 24 fresh conditions | four persistent GPU workers, 512 updates each | create matched functional models | histories, recovery, final checkpoints | 24 complete finite / stop affected queue / missing condition | training or resource | `conditions/`, `queue/` | permits frozen evaluation only |
| 3 | Measure task and route | frozen final checkpoints | identical development/confirmation evaluator | obtain \(A,F,G\) and diagnostics | per-window arrays and summaries | all native evaluations complete / stop / missing | evaluation | `evaluations/` | permits interventions |
| 4 | Measure expert match | correct forced checkpoints | intact, wrong1, wrong2 with no parameter updates | distinguish matched expert function | paired per-window intervention arrays | all 18 evaluations complete / stop / missing | intervention | `interventions/` | permits analysis |
| 5 | Adjudicate tested layers | complete arrays + article map | frozen aggregation and bootstrap | answer the Anchor question | review JSON, tables, figures | typed outcome / guard failure / incomplete | scientific or evidence | `analysis/` | result writing only |

## 14. Algorithm, Output, And Provenance Contract

Worker code and raw artifacts remain under:

`/data/250010109/MoE_Router/experiments/20260907_a15_15_e02_functional_layer_pilot/`

Canonical Protocol and later Summary/Detailed records remain in this E02 directory. Each run freezes the Protocol copy and SHA, code/config hashes, model/data identities, condition matrix, queue assignments, container/runtime metadata, job ID, GPU mapping, timestamps, and artifact manifest.

The runner must support idempotent recovery: an already complete condition is skipped only after its completion identity and final checkpoint validate; an incomplete condition resumes from `latest.pt`; an identity mismatch fails closed. The pipeline writes a completion manifest only after all training, evaluation, intervention, and analysis artifacts validate.

## 15. Success / Failure / Insufficient Evidence

Scientific outcomes are exactly Section 10. Operational completion requires 24/24 final checkpoints at update 512, 24 native development and confirmation evaluations, 6 correct-model intact confirmation evaluations shared with native results, 12 wrong-child confirmation evaluations, all guards, frozen analysis, and a complete artifact manifest.

The full job must not silently reduce updates, layers, seeds, controls, evaluation rows, or interventions. If the two-hour ceiling cannot complete the matrix, save exact recovery state and report the remaining cost; do not call the scientific outcome. Automatic platform retry is zero.

## 16. What This Cannot Claim

Even a positive result can identify only a functional position among blocks `{0,10,13}` for this model, dataset, adapter topology, training budget, and historically viewed evaluation split. It cannot establish block 10 as globally optimal, earliest suitable for semantic specialization, sufficient for online semantic routing, or valid outside M2D2. It cannot retroactively change E19 from `QUALIFICATION_FAILED`.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Basis |
|---|---|---|
| A Question and boundary | CONFIRMED | researcher explicitly supplied the final advisor question and three-layer-only boundary |
| B Data and provenance | CONFIRMED | researcher required identical data/labels/evaluation; frozen M2D2 and E19 article map verified |
| C Task and supervision | CONFIRMED | researcher fixed four conditions and same supervision boundary |
| D Architecture | CONFIRMED | researcher fixed candidates `{0,10,13}`, Router input A, and prohibited B migration |
| E Objective and optimization | CONFIRMED | researcher retained the previously discussed 512-update functional contract |
| F Comparison and evidence | CONFIRMED | researcher required task gain plus matched expert function and static-order comparison |
| G Execution and reproducibility | CONFIRMED | researcher explicitly approved reserved submission and processing |

Cross-block consistency: `PASS`. The researcher approved implementation, smoke, and one full exploratory reserved run. The scientific body freezes before the first E02 optimizer update. Any later material change requires an append-only amendment with eligibility impact.

Resource ceiling: one ACP node, `n6ls.iu.i40.4`, four H100 GPUs, workspace `share-space`, cluster `share-cluster`, reserved quota, normal priority, image `ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04`, four independent single-GPU workers, zero automatic retries, and two hours wall clock / eight GPU-hours. Passing smoke does not itself constitute functional evidence.

### Submission receipt (append-only; no scientific amendment)

- Contract tests: `13/13 PASS` immediately before submission.
- Real H100 smoke: all four block-10/seed-17 arms completed one optimizer update with finite loss and passing eligibility guards; disposable smoke weights are in `runs/smoke-20260907T0615Z/`.
- Measured estimate: `1.7974` wall hours and `7.1897` H100-hours, based on the slowest first-wave update plus a 25% evaluation/intervention margin.
- Frozen full run: `runs/full-20260907T0620Z/`; Protocol SHA-256 `fe9483740b064e8efe291f1ba2ed9248c46f20d10344752f86adab18afcd5eb8`; code SHA-256 `825713526e0f76438b77e13ec131a1c6b61bd11c2eb7f9bf26e8e17dccb9c82e`; data SHA-256 `8cd04d99ad2576d8a149dc145c83b29d5a977178419304c4490cf8e10cba51a8`.
- ACP job: `pt-ny8pbfn9`; submitted `2026-09-07T05:50:27Z`; reserved `n6ls.iu.i40.4`; four H100; zero retry; 7,200-second timeout.
- Completion receipt: job `SUCCEEDED` at `2026-09-07T06:53:06Z` with zero retries; 24/24 final checkpoints, 48 native split evaluations, 12 wrong-child evaluations, and all 24 eligibility guards are complete. The registered mechanical verdict is `MULTIPLE_TESTED_FUNCTIONAL_POSITIONS`. Read the [Summary](summary.md) first and audit the [Detailed record](detailed.md); result interpretation remains `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.
