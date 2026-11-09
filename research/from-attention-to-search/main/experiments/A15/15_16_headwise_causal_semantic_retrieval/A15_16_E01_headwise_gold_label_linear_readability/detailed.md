# Detailed: A15_16_E01 headwise gold-label linear readability

Primary Anchor: [A15.16](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_16_headwise_causal_semantic_retrieval/15_16_headwise_causal_semantic_retrieval_anchor.md)  
Frozen Protocol and registered revision: [Protocol](protocol.md), scientific body frozen before first test execution on 2026-09-04  
Summary: [Summary](summary.md)  
Result eligibility: primary evidence `ELIGIBLE`; knowledge wording `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## 0. Quick Recap

- **Purpose:** determine whether the actual context vector returned by individual attention query heads has reproducibly unequal gold-label readability.
- **Hypothesis:** at least one gold task passes a search-corrected head-spread null and retains a development-selected top-four advantage on untouched confirmation.
- **Experiment logic:** freeze the base, fit identical 128-to-3 affine probes for all 28 blocks and 16 query heads, select on development, then confirm once.
- **Direct result:** both tasks selected block 20 and heads `[4,5,13,7]`; their confirmation advantages were positive, but both registered permutation gates failed.
- **Eligibility:** the successful replacement job executed the frozen science contract. The first attempt produced no model or result evidence and is excluded.
- **Verdict:** `NO_REPRODUCIBLE_HEAD_HETEROGENEITY`.
- **Claim boundary:** stable descriptive head ranking is not qualified label-specific head specialization and is not causal or functional evidence.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| Query-head retrieval output | one query head's retrieved context before output projection | input to each block's `self_attn.o_proj`, reshaped to 16×128 | vector | exact audited representation | independent KV cache or causal value |
| Parent readout | three-way broad-domain classifier | one affine 128-to-3 probe per layer/head | cross-entropy in nats | broad-label accessibility | abstraction to unseen children |
| Conditional-child readout | three-way local child classifier selected by true parent | three parent-specific affine probes per layer/head | cross-entropy in nats | within-parent accessibility | deployable parent inference |
| Information gain | improvement over random three-way cross-entropy | \(G=\log3-\mathrm{CE}\) | nats | comparable readability scale | native use |
| Head spread | inequality among 16 heads in one layer | \(Q_{0.90}(G)-Q_{0.10}(G)\) | nats | registered primary metric | task or expert utility |

## 2. Anchor Link And Decision Point

The A15 line already distinguishes representation accessibility from expert utility. E15 found a descriptive block-9 MLP-input candidate but failed one null qualification. A15.15 then found no stable two-seed relation between stronger static readability and LoRA expert benefit. This experiment asks only whether attention retrieval should be resolved by query head before designing a causal follow-up.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
|---|---|---|---|---|---|
| model and data | exact E15 identities | all three hashes match | pass | per-seed development receipts | none |
| representation | 28 `o_proj` pre-hooks, 16×128, positions 63--254 | shape `28×2×192×16×128`, exact reshape | pass | `smoke.json` | none |
| causal boundary | future suffix cannot change earlier retrieval output | maximum difference `0.0` | pass | `smoke.json` | none |
| frozen base | no trainable or changed base parameter | passed before and after smoke | pass | `smoke.json` | none |
| probe training | four seeds, three passes, 768 updates each | 4/4 complete | pass | seed receipts and checkpoints | none |
| development seal | selector before confirmation | hash `2a8cbb...`, `confirmation_loaded=false` | pass | `development_selector.json` | none |
| permutations and bootstrap | 2,000 each | complete for both tasks | pass | `final_result.json` | none |
| required figures/tables | four figures, three tables | all complete and visually audited | pass | render manifest | none |
| resource | one node, 4×RTX 5090 SPOT | exact worker spec `n12lp.nn.i10a.4` | pass | job receipt `om-6043dkfm` | none |

### Amendments, retries, and exclusions

The first job `om-3f4wfbx0` passed the then-current 10 unit tests but stopped before model loading because the shared Transformers runtime was not activated. It produced no train, development, or confirmation evidence and is `INELIGIBLE` except as failure-ledger evidence. Engineering amendment A01 sourced the already verified runtime before Python and added a regression test; the science body was unchanged. Replacement job `om-6043dkfm` ran the complete 11-test suite, smoke, and full contract with zero retries.

CuBLAS emitted the same warning seen in predecessor work: deterministic algorithms were requested with `warn_only=True`, but bitwise GPU determinism was not guaranteed because `CUBLAS_WORKSPACE_CONFIG` was unset. No seed was rerun or selected. Four independent probe seeds agree on the sign and ranking; the warning is recorded as a reproducibility limitation and does not alter the registered eligibility rule.

No post-hoc analysis changes the verdict. The layerwise coarse/fine correlations and overlaps were registered secondary outputs.

## 4. Actual Setup

Training was **not staged model training**. There was one probe-fitting stage, followed by a development seal and one confirmation evaluation.

| Item | Actual execution |
|---|---|
| Trainable objects | 693,504 affine-probe parameters per seed: parent and three true-parent-conditioned child banks for 28×16 layer-head pairs |
| Frozen objects | all 596,049,920 Qwen3 parameters and language head |
| Data passes and updates | three complete train passes; 768 optimizer updates per seed; 3,072 across four isolated seeds |
| Batch and accumulation | 36 windows, four per each of nine cells; no accumulation |
| Objective | parent three-class token cross-entropy plus true-parent-conditioned child cross-entropy |
| Optimizer | AdamW, learning rate `1e-3`, weight decay `1e-4`; no schedule or early stopping |
| Checkpoint rule | final update only; atomic resume state every update |
| Development handoff | average four seed scores; choose earliest maximum-spread block and four largest-gain heads; seal hashes |
| Confirmation handoff | load frozen selector; no layer/head/checkpoint reselection |

Model: `/data/250010109/model_cache/Qwen3-0.6B-Base-official`, revision `da87bfb608c14b7cf20ba1ce41287e8de496c0cd`; model SHA-256 `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`; config SHA-256 `504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59`.

Data: `/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt`, SHA-256 `8cd04d99ad2576d8a149dc145c83b29d5a977178419304c4490cf8e10cba51a8`; 9,216 train, 2,304 development, and 4,608 confirmation windows. The statistical independence unit is a complete window. Probe seeds are optimization repetitions, not independent corpus samples.

Seeds: `171601`, `171611`, `171621`, `171631`; permutation seeds `171641/171642` on development and `171741/171742` on confirmation; bootstrap seeds `171651/171652`.

## 5. Metrics And Registered Decision Rules

Token loss is averaged first within each 192-position window, then within each of nine cells, then equally across cells, and finally across four probe seeds. For task \(q\):

\[
G^q_{\ell,h}=\log3-\mathrm{CE}^q_{\ell,h},\qquad
S^q_\ell=Q_{0.90}(G^q_{\ell,1:16})-Q_{0.10}(G^q_{\ell,1:16}).
\]

Development selects the earliest maximum-spread block and the four largest-gain heads. Each of 2,000 development label permutations contributes its maximum spread over all 28 layers. Confirmation uses the frozen layer and each permutation contributes only that layer's spread. A task passes only when both spread gates pass, the confirmation top-four-minus-rest bootstrap lower 95% endpoint exceeds zero, and every seed's difference is positive.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
|---|---|---|---|---|---|---|---|---|
| parent head heterogeneity | real spread above both null thresholds plus positive frozen-set advantage | per-seed NPZ and selector | `headwise_audit.py` SHA `f333eecf...` | cell-balanced, four seeds, 2,000 permutations/bootstraps | spread gates fail; advantage `0.300311 [0.293544,0.306483]` | eligible | fail | conservative wrong-label null |
| child head heterogeneity | same, with within-parent permutations | same | same | same | spread gates fail; advantage `0.354685 [0.347546,0.362285]` | eligible | fail | true parent selects the probe bank |
| coarse/fine head profile relation | registered descriptive correlation and top-four overlap | `coarse_fine_profiles.csv` | exact ranks and set overlap | all 28 layers | mean \(\rho=0.971534\); 21/28 overlap 4/4 | eligible secondary | shared profile | not causal equivalence |
| overall typed verdict | at least one task must pass all gates | `final_result.json` | frozen verdict function | both tasks | neither passes | eligible | `NO_REPRODUCIBLE_HEAD_HETEROGENEITY` | does not say all heads are equally readable descriptively |

## 7. Main Results

### 7.1 Eligible decision evidence

| Task | Frozen block | Frozen heads | Development spread / null | Confirmation spread / null | Top-four minus rest, 95% interval | Task pass |
|---|---:|---|---:|---:|---:|---|
| Parent | 20 | `4 5 13 7` | `0.401876 / 0.843293` | `0.384120 / 0.836393` | `0.300311 [0.293544,0.306483]` | no |
| Conditional child | 20 | `4 5 13 7` | `0.460696 / 1.353921` | `0.474199 / 1.326489` | `0.354685 [0.347546,0.362285]` | no |

All four individual seed differences were positive: parent `0.302319/0.299399/0.297931/0.301595`; child `0.354759/0.355528/0.354152/0.354301` nat.

At block 20, head 4 was best on both splits and tasks. On confirmation its parent CE/gain/accuracy were `0.563756/0.534856/0.788509`; its child values were `0.443220/0.655393/0.852076`.

### 7.2 Bounded descriptive evidence

Development and confirmation block-20 rankings were identical for both tasks: Spearman correlation `1.0`, with the same ordered top four `[4,5,13,7]`. Across all layers, parent-child head-gain correlation ranged from `0.923529` to `0.997059`, mean `0.971534`. Top-four overlap was 4 at 21 layers, 3 at six layers, and 2 at one layer; it was never 0 or 1.

This strongly repeated pattern is real descriptive evidence. It cannot override the registered null and, because the same heads rank highly for both tasks, it does not support different coarse and fine head roles.

### 7.3 Failed, ambiguous, and ineligible evidence

- Both evaluation-time label-permutation nulls produced thresholds far above the real spread; all four permutation p-values equal `1.000`. The likely reason is that confident probes incur very large and head-dependent cross-entropy when evaluated against mismatched labels. This is an interpretation of the frozen statistic, not a replacement analysis.
- Job `om-3f4wfbx0` is ineligible failure evidence only.
- Causal-history means, random channel partitions, refitted shuffled-label probes, activation replacement, task loss, KV-cache retrieval recall, and LoRA/MoE experts were not run.

## 8. Visualization Results

### 8.1 Layer-by-head readability atlas

![Layer-by-head readability atlas](figures/01_layer_head_readability_heatmaps.png)

- **Purpose:** show every registered layer-head result without selecting only favorable heads.
- **Metric:** \(\log3-\mathrm{CE}\) in nats, averaged window-first, cell-balanced, and across four seeds.
- **Raw source:** [layer-head metrics](tables/layer_head_metrics.csv).
- **How to read:** brighter cells are easier for the affine probe; development and confirmation patterns visibly repeat.
- **Observed result:** a structured but non-monotonic layer/head pattern, with strong cells around blocks 9, 17, 20--21, and 26--27.
- **Boundary:** the heatmap cannot qualify head specialization without the frozen null and cannot show causal use.

### 8.2 Registered head-spread gates

![Registered head-spread gates](figures/02_head_spread_and_nulls.png)

- **Purpose:** display the primary decision evidence.
- **Metric:** 90th-minus-10th percentile head-gain spread in nats.
- **Raw source:** [selected tests](tables/selected_head_tests.csv).
- **How to read:** curves are real spread; crosses are frozen 97.5% permutation thresholds at selected block 20.
- **Observed result:** development and confirmation repeat closely, but both real spreads are below both thresholds.
- **Take-home:** primary heterogeneity verdict fails.

### 8.3 Frozen top heads on confirmation

![Frozen top heads on confirmation](figures/03_frozen_top_heads_confirmation.png)

- **Purpose:** show the positive secondary guard without hiding the failed primary null.
- **Metric:** confirmation information gain per query head at frozen block 20.
- **Raw source:** [layer-head metrics](tables/layer_head_metrics.csv).
- **How to read:** red bars were selected on development; they remain the top four on confirmation for both tasks.
- **Observed result:** exact set and order repeat.
- **Boundary:** this stability does not meet the registered label-specific null.

### 8.4 Coarse versus conditional-fine profile

![Coarse versus conditional-fine profile](figures/04_coarse_fine_head_profiles.png)

- **Purpose:** test the proposed different-head story descriptively.
- **Metrics:** Spearman rank correlation and exact overlap of the two top-four sets.
- **Raw source:** [profile table](tables/coarse_fine_profiles.csv).
- **How to read:** correlation near one and overlap near four mean the two tasks favor the same heads.
- **Observed result:** mean correlation `0.971534`; complete overlap at 21/28 layers.
- **Take-home:** no evidence supports a coarse-head versus fine-head anatomical split.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Failure reason | What this rules out | What remains live |
|---|---|---|---|---|---|
| identity and tensor | exact hashes, 28 hooks, exact reshape | passed | none | silent object/tensor substitution | none at this stage |
| causality and freeze | suffix difference `0`, base unchanged | passed | none | future-token leakage and base training | attention may still retrieve generic context quality |
| fitting | 4×768 updates, finite, reloadable | passed | none | one-seed optimizer accident | probe family remains affine only |
| development/confirmation seal | all hashes agree | passed | none | confirmation-driven selection | none at this stage |
| frozen top-four stability | intervals positive; all seeds positive | passed secondary | none | random development ranking | label specificity remains unqualified |
| permutation qualification | real spread below null | failed scientifically | registered null too high for real spread | qualified heterogeneity claim | shared general head quality |
| coarse/fine separation | same top heads and high correlations | not supported | profiles nearly identical | separate semantic-granularity heads | common retrieval-strength factor |

No implementation or data prior was falsified. The registered operationalization did not qualify label-specific head heterogeneity. A shared, task-general head-readability factor remains the strongest interpretation of the descriptive pattern.

## 10. Full Experiment Record

- Worker job `om-6043dkfm`: `SUCCEEDED`, one replica, zero retries.
- Resource: workspace `share-space`; AEC2 `computing-cluster-5090-01g`; worker spec `n12lp.nn.i10a.4`; one node; 4×RTX 5090; SPOT; 56 vCPU; 240 GiB host memory.
- Image: `registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04`.
- Runtime: shared frozen layer exposing Transformers `4.53.3`, NGC PyTorch `2.8.0a0+5228986c39`, CUDA `12.9`.
- Command: `A15_16_EXPECTED_GPUS=4 A15_16_RUN_DIR=.../runs/full-20260904T071500Z bash scripts/run_remote.sh`.
- Unit tests: `11/11`; smoke: pass; four train/development shards: complete; selector: sealed; four confirmation shards: complete; finalization and rendering: complete.

## 11. Interpretation

The attention retrieval outputs are not uniformly interchangeable to a linear readout: a stable ranking and large top-four advantage are visible. However, the same ranking appears for coarse and fine labels almost everywhere, and the registered label-permutation statistic does not qualify either task. The safest reading is therefore not “semantic heads,” but “some query-head outputs are generally more useful to these two related readouts.” Phase 1 does not determine whether that advantage comes from selective attention, Value content, output scale, calibration, or a generic contextual-information factor.

## 12. Claim Boundary

**Can claim:** the full registered run completed; the same four block-20 heads repeated exactly; both primary null gates failed; coarse and fine profiles are nearly identical.

**Cannot claim:** query heads have distinct coarse/fine semantic roles; attention causally uses the decoded labels; the selected heads improve retrieval or prediction; any KV-cache or LoRA/MoE design is validated.

## 13. Next Decision

- **Decision:** whether to authorize a separately frozen Phase 2 that compares current-token state, causal-history mean, actual selected-head retrieval, and a minimal intervention.
- **Completion criterion:** the researcher accepts either a shared-head, non-specialist interpretation as sufficient reason to test selection, or closes the head-resolved route.
- **Resume action:** draft Phase 2 only after that explicit review; do not implement or execute it in this task state.

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
|---|---|---|---|---|---|---|---|
| `final_result.json` | machine verdict and all derived arrays | `headwise_audit.py` | sealed selector + four confirmation NPZs | `a5d6823b...` | yes | yes | canonical copy |
| `tables/selected_head_tests.csv` | primary values | renderer | final result | `1c948148...` | yes | yes | summary source |
| `tables/layer_head_metrics.csv` | all layer/head metrics | renderer | selector + final result | `ba9ee5d1...` | yes | yes | complete atlas |
| `tables/coarse_fine_profiles.csv` | profile relations | renderer | final result | `148162f7...` | yes | secondary | no verdict rescue |
| `figures/01_layer_head_readability_heatmaps.png` | atlas | renderer | layer-head table | `3b45deb8...` | yes | yes | visually audited |
| `figures/02_head_spread_and_nulls.png` | primary gate | renderer | selected tests | `d7c9fddb...` | yes | yes | visually audited |
| `figures/03_frozen_top_heads_confirmation.png` | frozen-set stability | renderer | layer-head table | `f38be91d...` | yes | secondary | visually audited |
| `figures/04_coarse_fine_head_profiles.png` | task-profile relation | renderer | profile table | `902a9a94...` | yes | secondary | visually audited |
| worker checkpoints and NPZs | reload and raw sufficient statistics | full job | train/dev/confirmation | per-seed hashes in worker receipts | yes | yes | remain outside Research_System |
| first job logs | environment failure ledger | `om-3f4wfbx0` | pre-model startup | job ID | yes | no | no scientific evidence |

## 15. Links

- Anchor: [A15.16](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_16_headwise_causal_semantic_retrieval/15_16_headwise_causal_semantic_retrieval_anchor.md)
- Protocol: [protocol.md](protocol.md)
- Summary: [summary.md](summary.md)
- Code workspace: `/data/250010109/MoE_Router/experiments/20260904_a15_16_e01_headwise_gold_label_linear_readability`
- Result directory: `/data/250010109/MoE_Router/experiments/20260904_a15_16_e01_headwise_gold_label_linear_readability/runs/full-20260904T071500Z`
- Runner: `scripts/run_remote.sh`
- Logs and checkpoints: worker result directory
- Successful job: `om-6043dkfm`; excluded first attempt: `om-3f4wfbx0`
