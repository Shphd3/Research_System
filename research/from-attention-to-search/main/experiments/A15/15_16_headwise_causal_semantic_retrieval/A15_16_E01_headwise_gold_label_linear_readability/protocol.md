# Protocol: A15_16_E01 headwise gold-label linear readability

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_ONE_FULL_RUN
Approval status: HUMAN_CONFIRMED
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: implementation; local unit tests; remote smoke; one full run; figures; summary; detailed evidence
Design frozen at: 2026-09-04 before implementation
Purpose: test whether actual query-head retrieval outputs contain reproducibly unequal gold-label information
Primary Anchor: A15.16 headwise causal semantic retrieval audit
Anchor decision question: whether a head-resolved Phase 2 is warranted
Anchor physical prior tested: query heads can retrieve different information despite shared Key/Value groups
Anchor core model term tested: between-head spread of affine-readout information gain
Anchor falsifier: search-corrected permutation null plus untouched confirmation of development-selected heads
Experiment role: operationalization and proxy test
Primary metric from Anchor: within-layer 90th-minus-10th percentile head spread in log(3)-minus-cross-entropy gain
Claim boundary from Anchor: accessibility only; no native use, intervention, sparse-retrieval utility, expert utility, or language-model gain
Minimal setup: frozen Qwen3-0.6B-Base; frozen M2D2 3x3; 28 blocks; 16 query heads; gold parent and conditional-child labels
Treatment and controls: real labels versus window-label permutation null; development-selected top four heads versus remaining 12
Changed variable: query-head identity within a block
Held fixed: model, data split, positions, vector width, probe family, optimizer, updates, and evaluation aggregation
Conditions to run: four probe seeds, one per approved RTX 5090 SPOT GPU
Pass: at least one task passes development max-null, frozen-layer confirmation null, and top-four bootstrap gates
Fail: neither task passes with all qualification checks valid
Insufficient: any identity, causality, sealing, null, reload, finiteness, or artifact guard fails
Cannot claim: a causal semantic head, useful KV-cache compression, LoRA/MoE placement, expert function, or next-token gain
Approval decision: execute Phase 1 only; Phase 2 remains unauthorized
```

## 1. Terminology And Definitions

- **Query-head retrieval output:** one query head's 128-dimensional attention result after causal softmax-weighted Value aggregation and before the shared output projection.
- **Key/Value group:** one stored Key/Value pair shared by two query heads in this grouped-query-attention model. Query heads are the audited units; they are not independent KV caches.
- **Affine readout:** a learned linear map plus bias from 128 dimensions to three logits. It is a frozen-representation diagnostic, not an online Router or an expert.
- **Parent task:** prediction of one of three M2D2 parent domains.
- **Conditional-child task:** selection by the true parent followed by prediction of one of that parent's three local child domains.
- **Information gain \(G\):** random three-class cross-entropy \(\log 3\) minus measured held-out cross-entropy, in nats.
- **Head spread \(S\):** the 90th percentile minus the 10th percentile of the 16 head gains inside one block, in nats.

## 2. Anchor Alignment

This experiment tests only whether a head-resolved attention retrieval object is worth carrying into a causal follow-up. Its strongest rival is selection noise from inspecting 448 layer-head pairs. Window-label permutations protect that comparison. No history-average comparator or activation intervention is present, so the experiment cannot distinguish information available in history from information selectively retrieved by attention.

## 3. Tested Hypothesis

At least one registered task has a development-selected block whose true head spread exceeds a family-wise permutation threshold and whose top four development heads retain a positive confirmation advantage over the other 12 heads.

The exact coarse-versus-fine profile overlap is a secondary measurement. It cannot rescue a failed primary heterogeneity verdict.

## 4. Rival Explanations

1. Every query head carries nearly the same label information.
2. All heads are near random and the apparent maximum comes from searching many pairs.
3. A development ranking is overfit and does not repeat on confirmation.
4. A capture error, future-token leakage, or true-parent misindexing creates artificial separation.

## 5. Data Construction And Provenance

| Object | Frozen identity |
|---|---|
| Model | `/data/250010109/model_cache/Qwen3-0.6B-Base-official` |
| Hugging Face revision | `da87bfb608c14b7cf20ba1ce41287e8de496c0cd` |
| `model.safetensors` SHA-256 | `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba` |
| `config.json` SHA-256 | `504a6b58c4271583724e66584b6b7698aea18450209df6b2f7582df0e89cee59` |
| Model structure | 28 blocks; hidden width 1,024; 16 query heads; eight Key/Value heads; head width 128 |
| Data | `/data/250010109/datasets/m2d2_wikipedia_3x3/processed/m2d2_3x3_seq256.pt` |
| Data SHA-256 | `8cd04d99ad2576d8a149dc145c83b29d5a977178419304c4490cf8e10cba51a8` |
| Windows per child | train 1,024; development 256; confirmation 512 |
| Positions | representation positions 63--254, predicting targets 64--255 |

The example and statistical unit is one existing 256-token window. Domain names are forbidden model inputs. Existing train, development, and confirmation windows are immutable; tokens from one window cannot cross branches. Gold labels contribute gradients only to probes, never to the frozen language model.

## 6. Learning Task And Permitted Supervision

For every zero-indexed block \(\ell\in[0,27]\) and query head \(h\in[0,15]\), fit:

1. one `128 -> 3` affine parent readout;
2. three parent-specific `128 -> 3` affine child readouts, with the true parent selecting the readout and the local child as target.

Every probe reads the complete 128-dimensional head output. No direction is deleted or projected out. Only train labels fit probes. Development labels select the block and four heads. Confirmation labels are unavailable until the selector artifact is frozen.

## 7. Model / Architecture And Frozen Variants

A forward pre-hook on each `self_attn.o_proj` captures its first input, expected as `[batch, 256, 2048]`. Reshaping gives `[batch, 256, 16, 128]`; positions 63--254 are retained. Concatenating the 16 heads must reconstruct the exact captured input bit-for-bit.

The base and language head stay in evaluation mode with every parameter `requires_grad=False`. Attention uses the same causal model computation as the frozen checkpoint. No output projection, MLP input, residual stream, Key alone, Value alone, causal mean, whole-window mean, or attention map is a probe input.

## 8. Training Objective And Optimization

Each independent probe minimizes mean three-class token cross-entropy over its assigned labels. Because probe parameters do not overlap, summing their losses changes no scientific coupling.

- Probe computation: float32; captured frozen representation: bfloat16 converted to float32 for readout.
- Optimizer: AdamW; learning rate `1e-3`; weight decay `1e-4`; no scheduler or early stopping.
- Exactly three deterministic passes over train windows.
- Balanced batches: 36 windows, four from each of the nine cells; 256 updates per pass; 768 total updates.
- Final optimizer update is the only checkpoint; development never selects a checkpoint.
- Four independent initialization/data-order seeds: `171601`, `171611`, `171621`, `171631`.
- Any non-finite loss or missing update hard-stops that seed and makes the full result insufficient unless rerun from the last pre-confirmation checkpoint under the unchanged contract.

## 9. Conditions, Seeds, And Checkpoints

One single-node `4×RTX 5090 SPOT` job runs four isolated processes, one seed per visible GPU. Every process loads the same frozen base and trains all 28-by-16 probe pairs. Processes do not average probe parameters. Rank 0 merges only completed per-seed checkpoints and held-out sufficient statistics.

SPOT resume state is atomically replaced after every optimizer update and includes probe/optimizer state, seed, code hash, frozen configuration, and next update. Resumption cannot change the data order or confirmation state.

## 10. Primary Metric And Frozen Analysis Plan

For every window, token cross-entropy is averaged across its 192 audited positions. Window values are averaged within each of the nine parent-child cells, and the nine cell means receive equal weight. The four probe-seed cross-entropies are then averaged. Define

\[
G_{\ell,h}=\log3-\mathrm{CE}_{\ell,h},\qquad
S_\ell=Q_{0.90}(G_{\ell,1:16})-Q_{0.10}(G_{\ell,1:16}).
\]

For each task independently:

1. Development selects \(\ell^*\) as the earliest block attaining \(\max_\ell S_\ell\) and selects the four heads with largest \(G_{\ell^*,h}\), breaking ties by lower head index.
2. Generate 2,000 window-label permutations. Parent labels are permuted across development windows. Child labels are permuted only within their true parent. Recompute all gains and spreads without refitting probes. Each development permutation contributes \(\max_\ell S_\ell\); the one-sided 97.5th percentile is the family-wise threshold.
3. Write `development_selector.json` containing \(\ell^*\), the four heads, all real development values, the null threshold, code/checkpoint/development hashes, and `development_pass`; atomically seal it before confirmation loading.
4. Confirmation evaluates the same frozen block and four heads. Its 2,000 label permutations contribute only \(S_{\ell^*}\); no layer or head is reselected.
5. A 2,000-replicate bootstrap resamples complete confirmation windows with replacement within each of the nine cells. Each replicate computes the mean gain of the frozen top four minus the mean gain of the remaining 12 after averaging probe seeds.

A task passes only when:

- real development \(S_{\ell^*}\) is strictly above its family-wise 97.5% permutation threshold;
- real confirmation \(S_{\ell^*}\) is strictly above its fixed-layer 97.5% permutation threshold;
- the confirmation top-four-minus-rest bootstrap 95% lower bound is strictly above zero;
- all four individual probe seeds have positive confirmation top-four-minus-rest differences.

No missing layer, head, seed, or window is imputed. Any such absence is insufficient. The analysis is one-sided because only greater heterogeneity supports the hypothesis. Confirmation is unsealed once and cannot change a selector or threshold.

## 11. Secondary Metrics And Guards

- Report domain-balanced accuracy and the window-level 5th percentile of true-class logit minus strongest wrong-class logit for every layer, head, task, split, and seed.
- Report per-layer Spearman correlation between the 16 coarse and 16 conditional-fine gains and the exact overlap of their top-four sets. These describe shared versus different head profiles and do not change the primary verdict.
- Report best-head gain, median-head gain, all heatmaps, per-seed ranking stability, and development-to-confirmation rank correlation.
- Record permutation Monte Carlo uncertainty and bootstrap intervals. A secondary metric cannot rescue a failed primary gate.

## 12. Known Good / Known Bad / Known Confusing Cases

- **Known good:** a synthetic head bank with one label-coded head must select that head and beat its permutation null.
- **Known bad:** independent random labels must not produce a passing frozen confirmation advantage.
- **Known confusing:** identical label signal copied into every head can be highly readable but must have near-zero head spread and fail the heterogeneity claim.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input and assumptions | How | Why | Expected output | Pass / fail / insufficient | Named failure | Artifact | Handoff |
|---|---|---|---|---|---|---|---|---|---|
| Preflight | protect identity and semantics | frozen paths and schema | verify hashes, counts, config, labels, and resource tuple | prevents silent object replacement | identity manifest | all exact / hard stop | data, model, or resource mismatch | `artifacts/preflight.json` | unit tests |
| Unit tests | validate analysis rules | synthetic arrays | test capture reshape, selectors, permutation, bootstrap, verdict, and reload | prevents metric and indexing bugs | test log | all pass / stop | implementation failure | `logs/unit_tests.log` | remote smoke |
| Remote smoke | validate real tensor and causality | two windows and actual checkpoint | check 28 hooks, shapes, reconstruction, suffix perturbation, frozen base, finite losses, one update, checkpoint reload, and synthetic controls | protects scale-up | smoke record | every guard pass / stop | capture, leakage, freeze, or reload failure | `artifacts/smoke.json` | full training |
| Train | fit fixed probe family | train only | four seeds, three passes, final-update checkpoint | measures accessibility without changing base | four complete checkpoints | all complete / insufficient | non-finite, missing, or drifted seed | `checkpoints/seed_*/final.pt` | development |
| Development | freeze selection | development only | evaluate, permute labels, select layer/top four, seal hashes | controls model selection | sealed selector | complete and immutable / insufficient | upstream confirmation access or missing score | `artifacts/development_selector.json` | confirmation |
| Confirmation | test reproducibility once | sealed selector plus confirmation | fixed-layer evaluation, permutation, bootstrap | distinguishes stable heterogeneity from search noise | raw result and typed verdict | pass/fail/insufficient | reselection or incomplete statistics | `artifacts/confirmation.json` | figures and records |

## 14. Algorithm, Output, And Provenance Contract

Worker root: `/data/250010109/MoE_Router/experiments/20260904_a15_16_e01_headwise_gold_label_linear_readability`.

Required worker outputs are source and tests; preflight/smoke/full logs; per-seed final and resume checkpoints; per-window class-negative-log-probability arrays; frozen development selector; confirmation analysis; one machine-readable verdict; tables; and audited figures. The complete token-by-layer-by-head activation tensor must never be saved.

Canonical result root: `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_16_headwise_causal_semantic_retrieval/A15_16_E01_headwise_gold_label_linear_readability/`. Only curated tables, figures, `summary.md`, and `detailed.md` enter Research_System.

Resource contract: workspace `share-space`; AEC2 cluster `computing-cluster-5090-01g`; worker spec `n12lp.nn.i10a.4`; one node; four RTX 5090 GPUs; SPOT quota; image `registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04`. If the platform cannot resolve this exact tuple, submission stops. No H100, reserved quota, eight-GPU, debug-cluster, or alternative worker-spec fallback is permitted.

## 15. Success / Failure / Insufficient Evidence

- `HEAD_HETEROGENEITY_BOTH`: both gold tasks pass every primary gate.
- `HEAD_HETEROGENEITY_PARENT_ONLY`: only the parent task passes.
- `HEAD_HETEROGENEITY_CHILD_ONLY`: only the conditional-child task passes.
- `NO_REPRODUCIBLE_HEAD_HETEROGENEITY`: neither passes and all qualification checks pass.
- `INSUFFICIENT`: at least one mandatory qualification, sealing, completeness, or provenance guard fails.

Exact coarse/fine top-set overlap is reported beside these verdicts; it is not silently folded into the typed verdict.

## 16. What This Cannot Claim

Even a positive result cannot show that attention intentionally selects semantic evidence, that the readable information is necessary for prediction, that a head should receive an expert, that KV cache can be reduced, or that any LoRA/MoE system improves next-token likelihood. Those questions require the separately reviewed Phase 2.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Item | State | Source |
|---|---|---|
| A. question and boundary | CONFIRMED | researcher approved the headwise audit and requested Phase 1 first |
| B. data and provenance | CONFIRMED | exact E15 model/data reuse plus researcher approval |
| C. task and supervision | CONFIRMED | gold-label headwise affine readout approved |
| D. architecture | CONFIRMED | actual per-query-head retrieval output approved; no other representation in Phase 1 |
| E. objective and optimization | CONFIRMED | identical-capacity linear readout and fixed full execution approved |
| F. comparison and evidence | CONFIRMED | headwise analysis, label null, development/confirmation separation, and four-part result approved |
| G. execution boundary | CONFIRMED | implementation, smoke, one full `4×RTX 5090 SPOT` run, plots, and records approved |

Cross-block consistency passed before implementation. The scientific body and all decision rules freeze at first test execution. Any later material change requires an append-only amendment and explicit researcher approval. Phase 2 design, intervention, KV-cache compression, LoRA/MoE training, graph edit, root sync, commit, and push remain unauthorized.

### Execution receipt and engineering amendment A01

- First submitted job: `om-3f4wfbx0`, exact approved 4×RTX 5090 SPOT tuple.
- Outcome: remote unit tests passed `10/10`; the smoke stopped before model loading because the base image did not expose the frozen shared `transformers` runtime on `PYTHONPATH`. No train, development, or confirmation evidence was produced.
- Change: source the already verified shared runtime activation script before any Python command. This changes only environment discovery; model, data, representation, probes, metrics, thresholds, splits, and verdict rules are unchanged.
- Guard: a regression test now requires runtime activation to precede the first Python command. The suite passes `11/11`.
- Evidence eligibility: job `om-3f4wfbx0` is failure-ledger evidence only. A fresh job must repeat the full smoke before scale-up.

### Successful execution receipt

- Replacement job: `om-6043dkfm`, `SUCCEEDED`, one replica, zero retries.
- Exact resource: `computing-cluster-5090-01g / n12lp.nn.i10a.4 / one node / 4×RTX 5090 / SPOT`.
- Completed scope: `11/11` unit tests, real-model smoke, four independent 768-update probe fits, development seal, one confirmation pass per seed, 2,000 permutations per task and split, 2,000 confirmation bootstraps per task, four figures, and three tables.
- Result records: [Summary](summary.md) and [Detailed](detailed.md).
