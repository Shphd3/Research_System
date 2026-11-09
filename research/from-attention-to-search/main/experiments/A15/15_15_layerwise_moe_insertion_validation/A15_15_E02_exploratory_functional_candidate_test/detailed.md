# Detailed: A15_15_E02 Exploratory Functional Candidate Test

Primary Anchor: [A15_15](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_15_layerwise_moe_insertion_validation/15_15_layerwise_moe_insertion_validation_anchor.md)

Frozen Protocol: [protocol.md](protocol.md), execution snapshot SHA-256 `fe9483740b064e8efe291f1ba2ed9248c46f20d10344752f86adab18afcd5eb8`

Summary: [summary.md](summary.md)

Result eligibility: `ELIGIBLE`; interpretation `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## 0. Quick Recap

- Purpose: test functional value at the three researcher-approved static candidates without changing Router input from block input A.
- Direct result: all three blocks have \(H>0\) in both seeds; point order `13 > 10 > 0`; both registered block-13 lead intervals overlap zero.
- Eligibility: 24/24 training conditions, 48 native evaluations, 12 wrong-child evaluations, all 24 guards, and frozen analysis are complete.
- Verdict: `MULTIPLE_TESTED_FUNCTIONAL_POSITIONS`.
- Boundary: this is a three-candidate forced-path result, not an all-layer optimum or evidence that task-only routing learns semantic dispatch.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit / role | Cannot prove |
|---|---|---|---|---|
| Site A | state entering the selected Transformer block | exact tensor captured by a block pre-hook | Router input | expert utility |
| Correct forced hierarchy | true parent and child select shared/parent/child rank-8 banks | unit route coefficients; no Router parameters | treatment | learned routing viability |
| Shuffled forced hierarchy | true parent plus frozen within-parent shuffled child | same capacity/topology as correct | structural control | semantic dispatch |
| Wrong child | either other child expert under the same parent | offsets `+1/+2 mod 3`, weights fixed | intervention | global task optimum |
| \(H\) | weakest required functional contrast | \(\min(A,F,W^1,W^2)\) | nats/target token; primary | 28-layer ranking |

## 2. Anchor Link And Decision Point

E01 found that higher readability improved semantic route agreement without reproducibly improving task or expert function. E19 then produced candidates `{0,10,13}` but remained `QUALIFICATION_FAILED`. E02 preserves that failure and directly asks whether any candidate combines correct-grouping task gain with matched child-expert function.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
|---|---|---|---|---|---|
| Scope | one 4×H100 full run, 24 arms, fixed interventions | job `pt-ny8pbfn9`; all required artifacts | PASS | [completion audit](tables/05_completion_audit.json) | none |
| Model/data | frozen Qwen3-0.6B and exact M2D2 tensor | weight/data hashes match | PASS | completion audit | none |
| Conditions | blocks 0/10/13 × seeds 17/29 × four arms | 24 unique completed conditions | PASS | worker `run_manifest.json` and guards | none |
| Training | 512 updates; effective batch 128; 12,582,912 target tokens | exact for every arm | PASS | 24 guards and histories | none |
| Optimizer | expert LR `2e-4`, Router LR `5e-4`, 26 warmup, cosine, WD `0.01`, clip `1.0` | code identity and 13/13 contract tests match | PASS | frozen code SHA and histories | none |
| Freeze/path | base frozen; A input; down-projection expert input; legal forced paths | all guards pass; behavioral tests pass | PASS | guards and tests | none |
| Evaluation | 2,304 development and 4,608 historical-confirmation rows; 192 targets | 48 arrays; row IDs and counts identical | PASS | native arrays and analysis validation | none |
| Intervention | two wrong-child evaluations per correct checkpoint | 12 arrays, no training | PASS | intervention arrays | none |
| Analysis | equal-cell means; 2,000 component replicates, seed `20260909` | exact frozen analysis | PASS | `functional_review.json` | none |
| Runtime | reserved 4×H100; two-hour limit; zero retries | 62.4 minutes; `SUCCEEDED`; zero retries | PASS | ACP job receipt | none |
| Route diagnostics | report online accuracy/NMI/entropy/load | native arrays existed; compact table calculated after completion | DEVIATION, secondary only | [route diagnostics](tables/04_online_route_diagnostics.csv) | primary verdict unchanged |
| Artifact manifest | complete final inventory | generated immediately before completion receipt/final manifest update, so it omits those self-referential final files | DEVIATION, bookkeeping only | worker `artifact_manifest.json` | decision evidence present and independently counted |

No scientific amendment, retry, exclusion, missing condition, or imputation occurred. The Protocol receipt appended after freezing does not alter the execution snapshot.

## 4. Actual Setup

The data contain nine balanced parent-child cells. Every condition trains on 9,216 windows through a deterministic seed-specific repeated-permutation stream. Each 256-token window uses positions 0–63 as context and evaluates the 192 next-token targets at positions 64–255.

The ordinary control activates one rank-24 adapter. Hierarchical arms activate one shared, one parent, and one child rank-8 bank. Correct and shuffled forced arms have no Router parameters and use unit coefficients. The task-only arm has parent and leaf linear Routers that receive only language-model gradients through selected route probabilities. All base-model and language-head parameters are frozen.

Every condition ran 512 AdamW updates with microbatch 8, accumulation 16, effective batch 128, expert LR `2e-4`, Router LR `5e-4`, 26-step linear warmup, cosine decay, weight decay `0.01`, and gradient clipping `1.0`. Update 512 was selected without early stopping. Immutable checkpoints exist at updates `0,1,4,32,128,256,384,512`.

Code workspace: `/data/250010109/MoE_Router/experiments/20260907_a15_15_e02_functional_layer_pilot/`

Run root: `/data/250010109/MoE_Router/experiments/20260907_a15_15_e02_functional_layer_pilot/runs/full-20260907T0620Z/`

## 5. Metrics And Registered Decision Rules

For ordinary, task-online, correct-forced, shuffled-forced, and the two wrong-child losses \(N^D,N^T,N^C,N^S,N^{W1},N^{W2}\),

\[
A=N^D-N^C,\quad F=N^S-N^C,\quad G=N^T-N^C,\quad
W^k=N^{Wk}-N^C,\quad H=\min(A,F,W^1,W^2).
\]

A layer is matched-functional only when \(H>0\) in seeds 17 and 29. A unique winner additionally requires its two-seed mean \(H\) to exceed both competitors with positive paired-bootstrap lower bounds. \(G\) is auxiliary and cannot replace any required component.

## 6. Evidence Lineage

| Claim / decision | Criterion | Raw artifact | Computation | Aggregation / uncertainty | Observed value | Eligibility | Verdict | Limitation |
|---|---|---|---|---|---|---|---|---|
| Each block has matched function | \(H>0\) in both seeds | 24 confirmation arrays + 12 intervention arrays | window NLL contrasts, then minimum | equal mean over nine cells | all six \(H\) values `0.002930–0.004260` | ELIGIBLE | all three pass | tested setup only |
| No unique functional block | top block beats each competitor outside paired interval | same arrays + E19 article map | two-seed mean \(H\) differences | 2,000 paired component replicates | 13−10 CI `[-0.000054,0.001263]`; 13−0 `[-0.000414,0.002093]` | ELIGIBLE | lead unresolved | component intervals are low-information in cells dominated by giant components |
| Static order is not preserved | compare exact point orders | E19 static review + E02 functional review | rank comparison | three candidates | static `10>13>0`; functional `13>10>0`; Spearman `0.5` | ELIGIBLE, descriptive | partial agreement only | three-item correlation is not a depth law |
| Task-only Router is not semantic | diagnostic only | online native arrays | token route versus repeated window label | full confirmation split | parent accuracy `0.324–0.335`; leaf `0.111–0.120`; severe load collapse | ELIGIBLE, secondary | no semantic-dispatch evidence | does not change forced-path verdict |

## 7. Main Results

### 7.1 Required functional components

| Block | Seed | \(A\) | \(F\) | \(W^1\) | \(W^2\) | \(H\) |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 17 | 0.012782 | 0.003425 | 0.008106 | 0.008028 | 0.003425 |
| 0 | 29 | 0.011746 | 0.002930 | 0.007448 | 0.007380 | 0.002930 |
| 10 | 17 | 0.014435 | 0.003967 | 0.009208 | 0.009214 | 0.003967 |
| 10 | 29 | 0.014358 | 0.004001 | 0.009496 | 0.009142 | 0.004001 |
| 13 | 17 | 0.012282 | 0.004196 | 0.010221 | 0.009983 | 0.004196 |
| 13 | 29 | 0.012825 | 0.004260 | 0.010200 | 0.009939 | 0.004260 |

Every \(H\) bottleneck is \(F\), the correct-versus-shuffled grouping contrast. The result is not driven solely by the ordinary-adapter comparison or wrong-child intervention.

### 7.2 Ordering and uncertainty

The point means are block 13 `0.004228`, block 10 `0.003984`, and block 0 `0.003177` nat/token. Bootstrap \(H\) intervals are positive for all three, but the registered winner rule concerns paired leads. Both block-13 lead intervals cross zero, so the point order does not establish a unique layer.

### 7.3 Auxiliary online path

\(G\) is positive at block 0 in both seeds (`0.001860/0.001952`), negative at block 10 (`-0.000635/-0.002240`), and changes sign at block 13 (`0.001032/-0.000458`). Negative \(G\) means task-only online NLL is lower than correct-forced NLL; it does not mean the routes are semantically correct. Route-label diagnostics are approximately chance with pronounced collapse, so this arm supplies no semantic dispatch result.

### 7.4 Absolute confirmation NLL

The correct-forced absolute NLL is lowest at block 0 (`2.867164/2.867144`), followed by block 10 (`2.871883/2.871688`) and block 13 (`2.872870/2.872266`). This was not the registered selection metric; it cannot override \(H\) or the paired winner rule.

## 8. Visualization Results

No figure is required. The six-row component table and two paired intervals expose the decisive relation more directly than a plot.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | What it rules out | What remains live |
|---|---|---|---|---|
| Contract and smoke | 13/13 tests; four real one-update arms | PASS | path, optimizer, recovery, and shape failures | full-run behavior |
| Training | 24 guards, 512 lines each, 24 finals | PASS | missing exposure, nonfinite optimization, base updates | generalization beyond budget/model |
| Native evaluation | 48 arrays with identical rows/counts | PASS | evaluator mismatch | historically viewed split limitation |
| Wrong-child intervention | 12 complete arrays | PASS | interchangeable child experts at tested layers | online discovery of those experts |
| Paired analysis | frozen review JSON | PASS | point-estimate-only winner claim | block-13 versus block-10 uncertainty |

The implementation, metric, and operationalization passed their registered guards. The primary block-10 hypothesis is weakened because block 10 is not the functional point leader and no unique lead resolves. The live rival is that readability nominates viable layers but does not order their functional advantage.

## 10. Full Experiment Record

ACP job `pt-ny8pbfn9` ran from `2026-09-07T05:50:41Z` to `06:53:06Z` on one reserved `n6ls.iu.i40.4` node with four H100 GPUs and zero retries. Training used 3,367.3 seconds, native evaluation 240.7 seconds, and intervention evaluation 107.5 seconds. The completion manifest was written at `06:53:02Z` with status `COMPLETE`.

## 11. Interpretation

Direct observation: correct semantic grouping beats ordinary adaptation and legal shuffled grouping, and both same-parent wrong experts are worse, at all three blocks and both seeds.

Safest AI interpretation: forced semantic specialization is functionally viable throughout this tested set, but E02 does not identify a unique insertion point. Static readability appears useful for candidate generation but not for ranking the top candidates. The task-only Router's collapse keeps online semantic routing unresolved.

Researcher judgment remains required before this interpretation becomes the Focus-level result.

## 12. Claim Boundary

Can claim: all three tested candidates have replicated positive forced-path \(H\) under the exact model, dataset, training budget, controls, and historically viewed split.

Cannot claim: a unique best tested layer; any 28-layer optimum or earliest specialization layer; preserved static/functional ordering; semantic task-only routing; or retroactive E19 qualification.

## 13. Next Decision

`AI 建议`: stop treating E02 as a selection result. Only if a downstream implementation requires one block, ask the researcher to approve a fresh block-10 versus block-13 replication with a prespecified practical equivalence margin. Completion is a resolved paired contrast or declared equivalence; resume from this Summary and the frozen arrays, not from E19's failed qualification.

## 14. Artifact Manifest

| Artifact | Purpose | Producer / identity | Complete | Claim-eligible | Notes |
|---|---|---|---|---|---|
| `protocol_frozen.md` | registered contract | SHA `fe948374…` | yes | yes | scientific body frozen before training |
| `run_manifest.json` | identities and stage status | code SHA `82571352…` | yes | yes | status COMPLETE |
| `conditions/*/final.pt` | 24 trained adapters | each guard binds run identity | 24/24 | yes | update 512 only |
| `evaluations/*.npz` | native dev/confirmation results | frozen evaluator | 48/48 | yes | equal row identity |
| `interventions/*.npz` | fixed wrong-child results | frozen evaluator | 12/12 | yes | no parameter updates |
| `analysis/functional_review.json` | registered adjudication | SHA `093a4986…` | yes | yes | verdict source |
| [component table](tables/01_functional_components.csv) | curated primary values | direct transcription from review JSON | yes | yes | nats/target token |
| [order table](tables/02_functional_order.csv) | point order and paired uncertainty | deterministic replay, seed `20260909` | yes | yes | 2,000 replicates |
| [route table](tables/04_online_route_diagnostics.csv) | secondary online diagnostic | post-completion read-only transform | yes | secondary | does not affect verdict |
| [completion audit](tables/05_completion_audit.json) | counts and identities | independent post-run audit | yes | yes | 13/13 tests |

## 15. Links

- Anchor: [A15_15](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_15_layerwise_moe_insertion_validation/15_15_layerwise_moe_insertion_validation_anchor.md)
- Protocol: [protocol.md](protocol.md)
- Summary: [summary.md](summary.md)
- Code workspace: `/data/250010109/MoE_Router/experiments/20260907_a15_15_e02_functional_layer_pilot/`
- Runner: `run_4gpu_pipeline.sh`; pipeline: `pipeline.py`
- Data: `/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt`
- Result directory: `/data/250010109/MoE_Router/experiments/20260907_a15_15_e02_functional_layer_pilot/runs/full-20260907T0620Z/`
- Logs and checkpoints: under the result directory
- Reproduction: `RUN_ROOT=<new-approved-run-root> bash run_4gpu_pipeline.sh`
- Job: `pt-ny8pbfn9`
