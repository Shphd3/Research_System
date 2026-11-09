# Protocol: A15_13_E19 A/B Paired Router-Input Readout Re-audit

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_FULL_STATIC_EXECUTION
Approval status: HUMAN_CONFIRMED in the 2026-09-07 execution request and linked frozen plan
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: implementation, local tests, article-provenance reconstruction, smoke, one reserved 4xH100 static job, analysis, candidate review, and bounded report
Design frozen at: before the first E19 probe optimizer update
Purpose: determine qualified functional-pilot layers from the exact current Router input
Primary Anchor: A15.13.07 gold-label layerwise static audit
Anchor decision question: where parent and conditional-child labels become jointly and stably linearly readable at site A
Anchor physical prior tested: a Router candidate must be directly accessible at site A for both label granularities
Anchor core model term tested: two-seed joint recovery J at site A
Anchor falsifier: no stable A candidate or any identity, article, null, numerical, or seed-stability qualification failure
Experiment role: metric and root-cause re-audit
Primary metric from Anchor: earliest three-block run with two-seed mean J >= 0.95
Claim boundary from Anchor: representation accessibility only; no Router, expert, or next-token function claim
Minimal setup: frozen Qwen3-0.6B-Base, M2D2 3x3, A/B sites, two probe seeds
Treatment and controls: A is primary; B is a paired tensor-position control; fixed nonlinear probe is a ceiling; shuffled labels are a null
Changed variable: representation site A versus B, and pre-registered probe seed
Held fixed: data, labels, window order, initialization tensors within seed, probe capacity, optimization, mask, and aggregation
Conditions to run: A/B x seeds 170903/170907; each contains real and shuffled linear heads plus real-label nonlinear heads
Pass: every qualification gate passes and an immutable three-layer A candidate set exists
Fail: any named hard gate fails
Insufficient: a gate cannot be evaluated without changing the frozen contract
Cannot claim: new independent confirmation, causal use, expert utility, language-model gain, or a universal depth law
Approval decision: execute continuously; enter A15.15 only after PASS, without another routine prompt
```

Confirmed Focus: [focus_gmm_pseudolabel_oracle_gap.md](../../../../focus/focus_gmm_pseudolabel_oracle_gap.md)

Confirmed execution plan: [sol_readability_reaudit_then_functional_layers_cn.md](../../../../research_notes/sae_representation/20260906/plans/sol_readability_reaudit_then_functional_layers_cn.md)

## 1. Terminology / Definitions

- **Site A:** the first tensor passed into zero-indexed Transformer block \(\ell\) for the current causal prefix. This is the input read by the maintained Router.
- **Site B:** the first tensor passed into that block's MLP after attention residual addition and normalization. B is not the raw attention update, the MLP output, or an authorized Router replacement.
- **Parent task:** three-way classification of the true coarse M2D2 domain.
- **Conditional-child task:** three separate three-way classifiers, each evaluated only inside its true parent.
- **Window:** one existing 256-token packed example. Positions 63--254 predict positions 64--255.
- **Article component:** the connected group of windows sharing any contributing source article; this is the independence unit when old packed windows mix articles.

## 2. Anchor Alignment

The experiment tests the A15.13.07 clause that a functional Router candidate must expose both parent and conditional-child labels at the actual Router input. The strongest rival is that the old block-9 result was caused by the B tensor, one readout seed, window pseudo-replication, or an unqualified shuffle null. B and the nonlinear probe diagnose representation formation but cannot select a functional layer.

The old E15 `UNQUALIFIED_SHUFFLE_CONTROL` verdict remains unchanged. E19 is a new pre-registered re-audit and not a reinterpretation of E15.

## 3. Tested Hypothesis

At site A, both label granularities reach a reproducible middle-layer plateau under the frozen two-seed linear selector. An eligible result yields exactly three A-only positions: a primary layer, a shallow low-readability reference at least three blocks earlier, and a deep high-readability reference at least three blocks later.

## 4. Rival Explanations

1. The apparent onset exists only at B, so it does not measure the maintained Router input.
2. A fixed nonlinear classifier finds earlier information that the linear Router cannot access.
3. Seed 170903 and 170907 nominate materially different layers.
4. Packed-window dependence or cross-split article reuse creates overconfident intervals.
5. Real-label curves coexist with an invalid shuffled-label control.

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
| Input/target positions | inputs 63--254; next tokens 64--255 |

The old construction selected non-empty source records by stable hash, concatenated tokenized records with EOS separators, and packed 256-token windows. E19 deterministically recreates that construction, checks every stored window hash and dataset order, and records every contributing article title hash, exact article-content hash, and packed-stream offset. If any stored window cannot be exactly recreated, any article identity is missing, or any normalized article title or exact article hash occurs across train/development/confirmation, candidate qualification fails.

Because the confirmation labels and curves were previously viewed, this split is a historical bridge and robustness readout, not a new untouched confirmation. No result may be described as newly independently confirmed.

## 6. Learning Task And Permitted Supervision

Each frozen current-token tensor predicts either its window's parent label or its local child label conditional on the true parent. The labels supervise only newly initialized probes. The base model, language head, online Router, and experts receive no updates. Domain names, future tokens, and confirmation values do not enter probe inputs, training, thresholds, or candidate movement.

## 7. Model / Architecture And Frozen Variants

- Base: frozen 28-block Qwen3-0.6B-Base, hidden width 1,024.
- Linear parent: one `1024 -> 3` affine head per layer, site, and seed.
- Linear child: three parent-specific `1024 -> 3` affine heads per layer, site, and seed.
- Nonlinear ceiling: `1024 -> 32 -> 3` with GELU, parent-specific for child readout.
- Null: independent linear heads trained on one fixed window-level shuffle with seed 170905.
- A and B for the same seed instantiate byte-identical initial probe tensors. Probe families are independent and share only frozen base forward computation within a worker.

The nonlinear ceiling is an audit requested by the researcher. It cannot change the A linear candidate algorithm.

## 8. Training Objective And Optimization

- Float32 probe computation; base inference in bfloat16.
- AdamW; linear learning rate `1e-3`; nonlinear learning rate `3e-4`; weight decay `1e-4`.
- Three deterministic passes; balanced batch 36 with four windows per cell; no scheduler, early stopping, or development-selected checkpoint.
- Seeds: initialization/order `170903` and `170907`; shuffle `170905`; article bootstrap `20260908`.
- Final optimizer update is the only probe checkpoint.
- Each worker atomically writes resume state after every optimizer update.
- `CUBLAS_WORKSPACE_CONFIG=:4096:8`; all non-finite losses or gradients are hard failures.

## 9. Conditions, Seeds, And Checkpoints

| Site | Probe seed | Linear real | Linear shuffle | Nonlinear real | Candidate role |
|---|---:|---|---|---|---|
| A | 170903 | yes | yes | yes | primary |
| A | 170907 | yes | yes | yes | primary |
| B | 170903 | yes | yes | yes | paired control |
| B | 170907 | yes | yes | yes | paired control |

Each condition saves final heads, optimizer state, full window metrics, development analysis, a freeze receipt before historical-confirmation evaluation, and confirmation analysis. A/B outputs use disjoint directories.

## 10. Primary Metric And Frozen Analysis Plan

For task \(q\), seed \(s\), site \(r\), and layer \(\ell\),

\[
R^{r,q,s}_{\ell}=\frac{\log 3-\mathrm{CE}^{r,q,s}_{\ell}}{\log 3-\min_m\mathrm{CE}^{r,q,s}_{m}}.
\]

A non-positive denominator yields no candidate. At site A define \(J^s_\ell\) as the smaller of parent and child recovery. Development defines the primary as the earliest start of three consecutive layers for which the mean of \(J^s_\ell\) across both seeds is at least 0.95. Each seed must also independently yield a joint primary; the two seed-specific primary layers may differ by at most two blocks.

The shallow reference is the minimum mean-\(J\) layer at least three blocks before the primary; the deep reference is the maximum mean-\(J\) layer at least three blocks after it. Ties select the shallower layer. Missing primary, shallow, or deep positions is a failure. B, nonlinear results, and historical confirmation cannot move the development candidates.

Cross-entropy is averaged first over tokens within a window, then over windows within each cell, then equally over nine cells. Accuracy uses the same weights. Both seeds remain separate in every table.

For uncertainty, run exactly 2,000 replicates with seed 20260908. Within each cell, resample article components with replacement; retain all windows in a sampled component. The same resample indexes are applied to A, B, every layer, and both tasks. Report candidate selection rates and A-minus-B CE differences. Window-only intervals remain historical diagnostics and do not qualify the new candidate.

## 11. Secondary Metrics And Guards

1. Linear and nonlinear CE, accuracy, recovery, and stable onset at A and B.
2. Per-layer paired A-minus-B CE with article-component intervals.
3. Nonlinear gain `linear CE - nonlinear CE`; it is descriptive only.
4. Early/middle/late position-bin curves from the same frozen heads.
5. Article-component-weighted sensitivity alongside the historical window-weighted result.
6. Base parameter hashes before/after, probe-only optimizer membership, A/B shape and prefix-invariance checks, and A/B initialization identity.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: analytic uniform logits give CE \(\log3\) and accuracy \(1/3\).
- Known bad: non-positive recovery denominator must produce no candidate.
- Known bad: any shuffled stable onset, out-of-range median accuracy, or median CE more than 0.05 nat from \(\log3\).
- Known confusing: shuffled CE slightly above the upper edge despite chance accuracy still fails, matching the old E15 `0.000132`-nat miss.
- Known confusing: a stronger or earlier nonlinear/B curve does not make that layer eligible for the maintained linear A Router.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input and assumptions | How | Expected output | Pass / fail / insufficient | Artifact | Handoff |
|---|---|---|---|---|---|---|---|
| 1 | Validate objects and independence | frozen model/data and raw source files | reconstruct articles/windows; run unit and hook smoke checks | identities, offsets, components, smoke receipts | exact match and zero cross-split article/title overlap / named hard failure / unrecoverable identity | `article_manifest.json`, smoke JSON | permits full probes only |
| 2 | Measure paired readout | four A/B-seed conditions | train frozen-base linear, shuffle, and nonlinear probes | heads and per-window metrics | all workers complete and finite / worker failure / missing worker | worker directories | permits frozen analysis only |
| 3 | Freeze eligibility and layers | development metrics and article components | apply A-only selector, paired bootstrap, and all guards | `candidate_review.json` | QUALIFIED / QUALIFICATION_FAILED / INSUFFICIENT | analysis JSON/CSV/figures | only QUALIFIED enters A15.15 |

## 14. Algorithm, Output, And Provenance Contract

Worker code and raw outputs remain under:

`/data/250010109/MoE_Router/experiments/20260907_a15_13_e19_ab_paired_readout_audit/`

Canonical Protocol, Summary, Detailed, tables, and selected figures remain in this E19 directory. Every run records the Protocol hash, code hashes, environment, job ID, GPU mapping, data/model hashes, start/end times, and exact artifact paths.

## 15. Success / Failure / Insufficient Evidence

`QUALIFIED` requires: two complete seeds at both A and B; exact hook and tensor contracts; identical paired initialization; traceable article identities; zero known cross-split article/title overlap; finite/reload/frozen-base checks; all old-form shuffle gates for every site, seed, split, and task; an A joint primary with seed gap at most two; and valid shallow/deep references.

`QUALIFICATION_FAILED` names every failed gate and stops before functional submission. `INSUFFICIENT` is used when a required gate cannot be computed without a post-freeze change. No secondary result rescues either state.

## 16. What This Cannot Claim

Even `QUALIFIED` means only that three site-A layer positions are admissible for a bounded functional pilot on this model, dataset, selector, and probe family. It does not prove that any layer will improve next-token prediction, that coarse and fine meanings form at different depths, that nonlinear structure is causally used, or that site B should replace A.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Basis |
|---|---|---|
| A Question and boundary | CONFIRMED | current user execution request and frozen plan |
| B Data and provenance | CONFIRMED | current user plan plus verified old data builder |
| C Task and supervision | CONFIRMED | current user plan and E15 contract |
| D Architecture | CONFIRMED | A primary/B comparison, fixed linear and nonlinear probes |
| E Objective and optimization | CONFIRMED | frozen plan and inherited E15 settings |
| F Comparison and evidence | CONFIRMED | frozen A-only selector and unchanged null gates |
| G Execution and reproducibility | CONFIRMED | reserved 4xH100, zero retries, persistent artifacts |

Cross-block consistency: `PASS` before execution. The researcher explicitly approved full static execution and automatic continuation only after qualification. The scientific body freezes at the first optimizer update. Any later change to data, sites, seeds, probes, metrics, thresholds, selector, or qualification makes affected evidence ineligible unless recorded as an append-only researcher-approved amendment.

Approved resource ceiling for E19: one ACP node, `n6ls.iu.i40.4`, four H100 GPUs, `reserved` quota, four independent single-GPU workers, zero automatic retries, and a one-hour wall-clock timeout (maximum four GPU-hours). No fallback or extra condition is authorized.

### Execution receipts

- `2026-09-07T04:31:37Z`, job `pt-jkkuglxx`: failed before any probe optimizer update because the new worker directories lacked their internal `logs/` subdirectories. The preceding real-tensor preflight passed. No development or historical-confirmation result was produced, and automatic retries remained zero. This is an engineering-only failure with no change to the scientific body.
- Replacement preflight: the directory-creation regression test and the old reload-path compatibility test pass; a local H100 smoke completed with `SMOKE_STATUS=PASS`. The replacement keeps the same sites, seeds, data, heads, optimizer, selector, thresholds, and resource ceiling.
- `2026-09-07T04:36:33Z`, replacement job `pt-0bisktrz`: started at `04:36:55Z` on one reserved `n6ls.iu.i40.4` node with four H100 GPUs and platform retry count zero. All four A/B-seed workers completed three passes (`768` probe optimizer updates each), the registered analysis completed with scientific exit code `3`, and the ACP job reached operational state `SUCCEEDED` at `04:44:42Z`.
- The immutable review is `runs/full-20260907T043632Z/analysis/candidate_review.json`, SHA-256 `31aa761fed8274e9b9b4a7f2b5199474d4494ffbb5ef99377669786331be69a7`. Its registered state is `QUALIFICATION_FAILED` because 5 of 16 shuffled-label rows fail at least one frozen null component. `functional_launch_authorized_by_review=false`; the already-approved stop branch was taken and no A15.15 job was submitted. These receipts do not amend the frozen scientific body.
