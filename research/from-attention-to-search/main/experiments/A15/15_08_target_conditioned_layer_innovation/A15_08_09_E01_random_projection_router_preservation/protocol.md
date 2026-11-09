---
experiment_id: A15_08_09_E01_random_projection_router_preservation
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_CONDITIONAL_FULL_RUN
approval_source: user instruction in the 0824 execution task
approval_date: 2026-08-23
anchor: ../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_09_random_projection_router_preservation_anchor.md
worker_root: /data/250010109/MoE_Router/experiments/20260824_a15_08_09_e01_random_projection_router_preservation
created: 2026-08-24
updated: 2026-08-24
---

# Protocol: Full-Space Admission And Conditional Gaussian Preservation

## 0. Approval And Non-Negotiable Boundary

The researcher explicitly authorized Anchor and Protocol formalization without another review round, implementation, smoke testing, and a conditional full run on one **reserved** four-H100 worker. This authorization freezes the scientific contract below.

Engineering failures may be repaired and rerun with an amendment receipt. A genuine scientific `Fail` must remain `Fail`; changing the taxonomy, registered layers, probe family, thresholds, or TEST set to obtain `Pass` is forbidden.

## 1. Question, Object, And Primary Metric

The experiment first asks whether full \(R_U\) has stable positive-margin linear structure. Only if that gate passes does it ask whether an independent dense Gaussian projection preserves the frozen Router at \(m\le d/8\).

At layer \(\ell\) and the registered token,

\[
X_\ell=N_\ell(h_\ell),\quad Z_\ell=N_\ell(h_\ell+a_\ell),\quad
U_\ell=Z_\ell-X_\ell,
\]

\[
R_{U,\ell}=U_\ell-(X_\ell\widehat B_\ell+\widehat b_\ell).
\]

The hard admission metric is the 5th percentile true-label logit margin \(\Gamma_{0.05}^{\mathrm{full}}\) on each of the two TEST panels. Conditional on admission, the primary preservation metric is normalized margin retention, NMR. Balanced accuracy, macro-F1, chance-corrected accuracy retention, full-decision agreement, and distance distortion are secondary guards.

## 2. Frozen Data Contract

### 2.1 Taxonomy identity

Use the prior taxonomy exactly; do not use the altered taxonomy table in the 0824 discussion draft. The frozen grid is:

| Parent | Eight children in frozen order |
| --- | --- |
| mathematics | algebra; analysis; combinatorics; geometry; number theory; probability; statistics; topology |
| physics | condensed matter physics; electromagnetism; mechanics; optics; particle physics; quantum physics; relativity; thermodynamics |
| chemistry | analytical; electrochemistry; inorganic; nuclear; organic; physical; polymer; theoretical chemistry |
| biology | cell biology; developmental biology; ecology; evolutionary biology; genetics; microbiology; molecular biology; physiology |
| computer science | algorithms; artificial intelligence; cybersecurity; databases; graphics; networks; operating systems; programming languages |
| economics | development; econometrics; financial economics; international; labor; macroeconomics; microeconomics; public |
| medicine | cardiology; endocrinology; gastroenterology; immunology; nephrology; neurology; oncology; pulmonology |
| linguistics | morphology; phonetics; phonology; pragmatics; psycholinguistics; semantics; sociolinguistics; syntax |

Expected source-taxonomy SHA-256: `60236fcd675c307a38f1b1ae7b8b7712fa325f437937b6f8febebdaca3ee6bb1`.

Expected frozen-grid SHA-256: `23e51082ff97bc8296545a9de3987ec594db9476baa667c00241ff125145f030`.

### 2.2 Rows and splits

Generate exactly 300 independent English items per fine class, 19,200 total:

| Split | Rows per class | Total | Template policy |
| --- | ---: | ---: | --- |
| TRAIN | 180 | 11,520 | families 1--3 |
| DEV | 40 | 2,560 | families 1--3 |
| TEST-same | 40 | 2,560 | families 1--3, unseen semantic seeds |
| TEST-new | 40 | 2,560 | families 4--5 only, unseen semantic seeds |

Each class has 75 definition, 75 comparison, 75 quantitative, and 75 mechanism items. The first robustness build's 4,800 definition and 4,800 comparison **semantic cards** may be retained only after all current guards pass. All 9,600 quantitative/mechanism cards must be regenerated from domain-specific, auditable schemas; no arbitrary number substitution or generic causal wrapper is eligible.

The v1 raw-text bag-of-words development audit reached 0.9254 balanced accuracy on TEST-same and 0.9449 on TEST-new. Therefore a single-topic prompt is ineligible even without literal label leakage. Every v2 item uses a binding-controlled eight-card construction:

1. include exactly one short, label-free semantic card from each of the eight frozen parent domains;
2. assign all eight neutral identifier codes exactly once, independently of labels and card order;
3. separate each card's semantic text from its code by the same neutral marker token, so registered unigrams/bigrams cannot encode the binding;
4. ask for the parent of the card carrying one target code; the target card's parent/fine class is the label;
5. balance distractor child classes, card order, code assignment, length and reasoning type within every target class and split.

Thus the v2 task preserves the old taxonomy but changes what carries the label: not the presence of domain vocabulary, which is matched per item, but the relation between a neutral code and one semantic card. This is a pre-TEST H1 repair, not a scientific-result rescue.

Qwen3-8B is used only as a deterministic offline drafting helper for 512 compact quantitative/mechanism card schemas, each of which is checked and recorded. It is not the measured representation model and contributes no experimental score. Every \(X/U/R_U\) extraction and every H2--H4 result uses the researcher-selected Qwen3-30B-A3B checkpoint.

Split the semantic seed, equation schema and mechanism graph before rendering text. A seed, entity tuple, equation instance, numerical instance, mechanism graph, or paraphrase family belongs to exactly one split.

All text ends in the same `Answer:` suffix. TEST-new changes the surface wrapper, not the terminal token. After Amendment A03, model-token length must be 96--320. Parent/child labels and explicit field-identification phrases are forbidden in item text.

### 2.3 H1 guards

H1 is evaluated before representation extraction:

1. exact row, class, split, scaffold and template balance;
2. zero duplicate normalized texts and zero record-ID overlap;
3. zero semantic-seed, entity-tuple, equation-instance, numerical-instance, mechanism-graph and paraphrase-family overlap across splits;
4. zero direct parent/child label occurrences after registered normalization;
5. maximum cross-split character 5-gram Jaccard \(\le0.35\);
6. after Amendment A03, per-class token-length median difference between any two splits \(\le15\) tokens;
7. registered raw-text TF-IDF unigram+bigram L2 multinomial-logistic baseline; additionally verify that each item contains all eight codes and one card from every parent;
8. a stratified review pack with one quantitative or mechanism row per fine class plus machine-readable provenance and expected solution.

The bag-of-words baseline uses TRAIN only; DEV selects \(C\in\{10^{-6},\ldots,10^2\}\); TEST-same and TEST-new are evaluated once. H1 cannot receive final `Pass` until the complete data guard passes and the TEST-new bag-of-words accuracy is below 90% of the registered full-\(R_U\) probe accuracy. Human review, if unavailable, is reported as an unresolved external guard; automated or model judgments are never mislabeled as human annotation.

Any confirmed label leak, cross-split semantic duplicate, wrong answer, or ambiguous primary class is H1 `Fail` and stops formal inference. Missing review evidence is `Insufficient`, not `Pass`.

## 3. Frozen Model And Extraction Contract

### 3.1 Model

- path: `/data/share/Qwen3-30B-A3B`;
- architecture: Qwen3 MoE, 48 blocks, hidden size 2,048;
- dtype: BF16 model forward, FP32 saved \(X/U\) and downstream analysis unless a preflight memory measurement requires FP16 storage with a documented parity check;
- runtime: repository-local Transformers 4.53.3 layer;
- mode: `eval`, no generation, sampling, dropout, gradients or parameter update;
- attention: SDPA;
- tokenizer: the checkpoint-local tokenizer, left padding, no added special token.

Frozen identity hashes: `config.json` = `2850ddb3bf7aecad20b611e2d44f3077fc8193f4827c93beddd4c02ad63c2297`; `model.safetensors.index.json` = `df0d481ec595c55a0ba58426d517390c6214a566ec4ff1c8fc4bbce9f57b3c24`; `tokenizer.json` = `aeb13307a71acd8fe81861d94ad54ab689df773318809eed3cbe794b4492dae4`. Every indexed shard is hashed in the run preflight receipt.

The preflight records hashes of `config.json`, tokenizer files, model index, every weight shard, extraction source and environment. Any missing shard or unexpected architecture is a hard stop.

### 3.2 Layers and token

- block 24 is primary;
- block 28 is a co-registered replication and cannot rescue block 24;
- capture the last unpadded token of the common `Answer:` suffix.

Hooks capture \(h_\ell\) at block input and \(a_\ell\) at `self_attn.o_proj` output. Apply the same native `post_attention_layernorm` counterfactually to \(h_\ell\) and actually to \(h_\ell+a_\ell\).

### 3.3 Extraction identity gates

For every process and registered block:

- deterministic replay maximum absolute error \(\le10^{-5}\);
- attention output-projection replay relative error \(\le10^{-5}\);
- \(\|(Z-X)-U\|/\|U\|\le10^{-6}\);
- \(Z\) matches the native MLP input with relative error \(\le10^{-5}\);
- all values finite and every record appears exactly once after shard merge.

## 4. Residualizer And Full-Space Probe

### 4.1 Residualizer

For each registered block, TRAIN fits ridge \(U=X B+b\). DEV selects \(\lambda\in\{10^{-6},10^{-5},\ldots,10^2\}\) by mean squared error. Freeze \(B,b\), compute \(R_U\) for all splits, and standardize using TRAIN means and standard deviations only. Zero-variance coordinates use scale 1 and are counted.

### 4.2 Registered probe

Fit L2 multinomial logistic regression on TRAIN \(R_U\) to the eight parent labels:

- \(C\in\{10^{-6},10^{-5},\ldots,10^2\}\) selected on DEV balanced accuracy, with DEV log loss as deterministic tie-breaker;
- maximum iterations 10,000; tolerance \(10^{-7}\);
- seeds `24001, 24002, 24003, 24004, 24005` control row order and solver initialization;
- no class weighting;
- after selecting \(C\), refit on TRAIN only and open both TEST panels once.

No other classifier, alternate label level, alternate layer or post-TEST regularization may change H2/H3. Fine-class probes and supervised functional rank are descriptive extensions only.

### 4.3 Full-space controls

1. identity map preserves every score, margin and decision within \(10^{-6}\) relative tolerance;
2. five independently permuted TRAIN-label probes remain compatible with \(1/8\) chance on both tests;
3. adding the same fixed vector to every row preserves sampled pairwise distances within \(10^{-6}\) relative tolerance;
4. for 1,000 fixed TRAIN difference vectors, report this ratio per matrix and require its mean across the 30 registered matrix seeds to differ from 1 by at most 2%; do not rescale a scientifically valid Gaussian draw to force a single matrix through this guard;
5. the synthetic suite contains a positive-margin Gaussian mixture, bounded-noise perturbation, common-offset invariance, XOR non-separability, and concentrated-coordinate counterexample.

Synthetic results validate implementation branches only; they are not evidence for the real-data theorem premise.

## 5. H2/H3 Metrics And Verdicts

For each seed, block and TEST panel report balanced accuracy, macro-F1, fraction of positive margins, median margin and \(Q_{0.05}\) true-label margin. Use 2,000 class-stratified bootstrap resamples nested with probe seed to produce 95% confidence intervals.

### H2

- `Pass`: both TEST panels have balanced-accuracy 95% lower bound \(>1/8\), and seed standard deviation \(\le0.02\).
- `Fail`: H1 and power guards pass, but either panel is not above chance.
- `Insufficient`: confidence half-width \(>0.05\), non-convergence, or seed standard deviation \(>0.02\).

### H3

Block 24 `Pass` requires, on both TEST panels:

1. the 95% lower bound of \(\Gamma_{0.05}^{\mathrm{full}}\) is \(>0\);
2. the balanced-accuracy 95% lower bound is \(\ge0.90\);
3. at least four of five probe seeds individually satisfy both conditions.

Seed `24001` is the pre-registered primary Router and must be among the passing seeds. H4 projects this seed's frozen weights; the other four seeds are an optimization-stability guard and are not searched to select a more favorable Router.

Block 28 receives the same independent verdict but does not alter the block-24 primary verdict.

H3 is `Fail` when H1 and statistical-power guards pass but the conjunction fails. H3 is `Insufficient` when the margin confidence half-width exceeds 20% of DEV margin IQR or optimization is unstable. The only allowed H3-fail claim is: within the registered probe family, sample size and power, stable linear routability was not detected.

## 6. Conditional H4 Gaussian Scan

Run this section only if block-24 H3 is `Pass`. The block-28 scan is reported separately only if block 28 also passes H3.

Freeze the full-space weights before drawing any matrix. For each

\[
m\in\{8,16,32,64,128,256,512,1024\},\quad m<2048,
\]

draw 30 independent \(R_{ab}\sim\mathcal N(0,1/m)\) matrices from registered seeds `8240901000 + 1000*m + j`, \(j=0,\ldots,29\). Use \(z=Rr\), \(\widetilde W=RW\), and the original bias. Do not retrain in projected space.

For each matrix and TEST panel report:

- NMR;
- chance-corrected accuracy retention (AR);
- agreement with full-space predicted labels;
- sampled squared-distance distortion over 100,000 class-stratified pairs.

For each \(m\), take the 5th percentile across the 30 matrix seeds and bootstrap those seeds 2,000 times.

- Dimension `Pass`: on both panels, NMR lower bound \(\ge0.90\), AR lower bound \(\ge0.95\), and agreement lower bound \(\ge0.95\).
- H4 `Pass`: at least one dimension \(m\le256=d/8\) passes; \(m_*\) is the smallest passing dimension.
- H4 `Fail`: H3 passes but no \(m\le256\) passes.
- H4 `Insufficient`: fewer than 30 valid matrices at any decision-critical dimension, identity/scale failure, or any decision-critical confidence half-width \(>0.10\).

## 7. Diagnostics That Cannot Change The Main Verdict

1. **Distance audit:** report the theorem-aligned extreme ratio \(D_{out}/D_{in}\) and robust \(Q_{0.05}(D_{out})/Q_{0.95}(D_{in})\) separately.
2. **Supervised functional dimension:** on fine labels, describe the smallest registered supervised rank retaining 90% of chance-corrected full performance. It does not estimate geometric affine rank.
3. **Random spectral-coordinate sampling:** run only if TRAIN-estimated leverage/coherence is low enough under its explicit bound. Spectral entropy alone is not a uniformity test. This branch never replaces dense-Gaussian H4.

## 8. Execution Contract

### 8.1 Worker surface and stages

All code, raw arrays, logs and plots live under:

`/data/250010109/MoE_Router/experiments/20260824_a15_08_09_e01_random_projection_router_preservation`

Ordered stages:

1. build dataset v2, audit, review pack, and bag-of-words baseline;
2. local CPU unit tests and synthetic contract;
3. reserved four-H100 smoke: 2 classes per parent, 2 rows per split, both blocks, full extraction/merge/residual/probe path;
4. reserved four-H100 full extraction and H1/H2/H3 analysis;
5. conditional H4 scan and diagnostics;
6. render artifacts and write canonical result records.

### 8.2 ACP resource

- workspace: `share-space`;
- cluster: `share-cluster`;
- worker spec: `n6ls.iu.i40.4`;
- workers: 1;
- GPUs/processes: 4;
- quota type: `reserved` exactly; spot/idle is forbidden;
- priority: `normal`;
- mounted storage: `/data` through the registered share-space AFS mount;
- runtime image: the previously audited Qwen3/Transformers image, frozen in the submission receipt before launch.

Submission must fail closed if the resolved job spec does not show one worker, four H100-class 80-GB GPUs and `reserved` quota. The installed SCO component incompatibility may be handled only through the previously audited workspace-response compatibility wrapper; the wrapper and its hash must enter `detailed.md`.

### 8.3 Run and repair policy

Every stage emits a manifest with source/data/model hashes, command, environment, start/end times and artifact hashes. A failed engineering gate may be repaired only after recording root cause, changed files and an amendment identifier. No TEST-driven scientific setting change is allowed. A scientific gate ends its dependent branch according to the frozen rule.

## 9. Required Outputs

- data manifest, audit receipt, BoW metrics and 64-row review pack;
- model/source/environment/preflight receipts;
- extraction identity and shard-merge receipts;
- full-space per-seed and bootstrap tables for both blocks/panels;
- conditional projection table for every valid \((m,R)\);
- one central figure with \(m\) on the x-axis and NMR plus AR on the y-axis, faceted by TEST panel, with thresholds and \(m_*\); render only if H3 passes;
- `summary.md` with the registered verdict and boundary;
- `detailed.md` with complete provenance, failures, amendments, jobs and artifacts;
- update the active Focus only after the researcher states or confirms the result.

## 10. A--G Freeze Audit

| Block | Frozen decision | Audit |
| --- | --- | --- |
| A. question | full-space positive-margin admission, then conditional preservation | pass |
| B. data | old taxonomy, 19,200 rows, split-isolated semantic schemas, H1 guards | pass after correcting the 0824 taxonomy drift |
| C. model/object | Qwen3-30B-A3B; blocks 24/28; exact \(X,Z,U,R_U\) | pass |
| D. methods | one residualizer family, one probe family, frozen Gaussian map | pass |
| E. metrics | \(Q_{0.05}\) margin primary; NMR conditional; accuracy guards | pass |
| F. verdicts | explicit Pass/Fail/Insufficient and dependency stops | pass |
| G. provenance/execution | immutable receipts; reserved 4-H100 ACP; repair log | pass |

Cross-block consistency audit: `PASS` after amendment A01 below. The only external evidence that cannot be fabricated is genuine human semantic review; if it is absent, H1 is reported `Insufficient` rather than silently promoted.

## 11. Amendment A01 — Bag-Of-Words Binding Repair

- Trigger: rejected v1 development audit, before v2 data freeze or any Qwen3-30B-A3B representation extraction.
- Direct evidence: v1 parent-label TF-IDF unigram+bigram balanced accuracy = 0.925390625 on TEST-same and 0.944921875 on TEST-new (`runs/v1-bow-parent.json` in the worker root).
- Root cause: each v1 prompt exposed only one academic topic, so lexical topic presence predicted the parent label even without literal labels.
- Repair: replace the single-topic surface with the eight-card neutral-code binding construction above; preserve the exact taxonomy, target semantic cards, counts, splits, model object and all H2--H4 rules.
- Eligibility: v1 remains development evidence only. Only a newly frozen v2 dataset whose own BoW guard passes may enter formal extraction.
- Authorization: covered by the researcher's explicit instruction to repair failed implementation/data guards while preserving the theory and meeting correction. Scientific gates remain immutable.

## 12. Amendment A02 — Semantic-Duplicate Measurement Object

- Trigger: the second v2 machine audit, before model extraction or any TEST representation result.
- Direct evidence: all structural guards and literal-label checks passed, but full-prompt character 5-gram Jaccard reached 0.3719745222929936. On that maximum pair, the eight semantic-card payloads alone scored 0.17967332123411978; the excess overlap came from the deliberately fixed binding instruction, neutral `marker` scaffold, and common `Answer:` suffix.
- Root cause: after Amendment A01, full prompt text conflates task-interface invariance with semantic duplication. The registered guard is intended to detect cross-split semantic copies, not to penalize the common decision-token contract.
- Repair: keep the threshold at 0.35 and compute character 5-gram Jaccard over the ordered concatenation of the eight semantic-card contents. Continue to audit the fixed wrapper separately through template-family IDs, the eight-code binding invariant, and the common-suffix check.
- Boundary: this amendment changes only the similarity measurement object. It does not change any row, split, label, threshold, H2--H4 setting, or scientific verdict rule.
- Authorization: covered by the same pre-TEST engineering/data-guard repair authorization as Amendment A01.

## 13. Amendment A03 — Eight-Card Token-Length Contract

- Trigger: formal Qwen3-30B-A3B tokenizer audit after the binding dataset passed all structural and semantic-duplicate guards, before representation extraction.
- Direct evidence: the approved eight-card interface measured 119--302 tokens (median 198, 95th percentile 279). The former single-topic 40--120 range admitted only 4 of 19,200 rows. Nine classes exceeded the former 10-token cross-split median-gap guard only marginally; the maximum gap was 13 tokens.
- Root cause: the former range was inherited from a one-topic prompt and is structurally incompatible with eight semantic cards plus a fixed binding query. Remaining split-length variation comes from independently written semantic cards, not class-count imbalance; each split remains exactly reasoning-balanced.
- Repair: freeze the admissible range to 96--320 Qwen3-30B-A3B tokens and the maximum per-class cross-split median gap to 15 tokens. Record the full per-class medians, not only the maximum.
- Boundary: this amendment uses only prompt text and the frozen tokenizer. It does not inspect hidden states, labels predicted by a model, margins, or any H2--H4 result. The taxonomy, counts, split IDs, semantic similarity threshold, target token, model and all scientific verdict rules are unchanged.

## 14. Amendment A04 — Permuted-Label Control Decision Rule

- Trigger: pre-smoke static implementation audit found that the registered five permuted-TRAIN-label probes were named but lacked an executable decision rule. The first smoke job `pt-a1s83i6j` was stopped while still at zero allocated replicas so the shared source could be frozen before execution.
- Repair: for each registered probe seed, fit one additional Router using an independently permuted TRAIN-label vector and that seed's DEV-selected \(C\); do not use permuted DEV or TEST labels. On each TEST panel, nest class-stratified row bootstrap inside bootstrap over the five permutation seeds. The aggregate 95% interval must contain \(1/8\), and no individual seed's point accuracy may differ from \(1/8\) by more than 0.05.
- Verdict role: a failed permutation control or any selected-model non-convergence makes H2/H3 `Insufficient`; it cannot make either hypothesis `Pass` or scientific `Fail`.
- Added real-space controls: the primary Router's identity projection must reproduce scores within \(10^{-6}\) relative error, and adding one deterministic common offset must preserve 1,000 sampled TRAIN pair differences within \(10^{-6}\) relative error.
- Boundary: the audit occurred before any Qwen3 representation extraction or TEST hidden-state result. No scientific threshold or favorable model was selected from TEST behavior.

## 15. Amendment A05 — Executable Distance And Gaussian-Scale Audit

- Trigger: the same pre-smoke implementation audit found that H4 emitted NMR/AR/agreement but did not yet emit the registered real-data distance diagnostics or TRAIN Gaussian-scale guard. No representation job had allocated a GPU.
- Repair: before scanning matrices, draw fixed class-stratified pair indices separately for each TEST panel: 50,000 within-parent pairs and 50,000 between-parent pairs. For every matrix, report squared-distance distortion mean, 5th percentile, median, 95th percentile and maximum absolute error, plus the extreme and robust between/within Euclidean-distance ratios before and after projection.
- Gaussian-scale guard: draw a separate fixed set of 1,000 class-stratified TRAIN difference vectors. At each \(m\), average the per-matrix mean squared-norm ratio over all 30 registered Gaussian matrices and require absolute deviation from 1 to be at most 0.02. A violation makes the corresponding decision-critical dimension ineligible and H4 `Insufficient` if no eligible registered dimension passes.
- Boundary: distance quantities are diagnostics and cannot rescue NMR, AR, or agreement. Pair seeds, counts, Gaussian seeds, dimensions and all scientific thresholds remain frozen before hidden-state extraction.

## 16. Amendment A06 — Exact Prefix-Execution Optimization

- Trigger: after a successful long-sequence smoke but before any full extraction GPU was allocated, measured throughput implied more than five hours because every input executed all 48 Transformer blocks although the latest registered capture is block 28. The first full submission `pt-cg4u6b1n` was stopped at zero allocated replicas.
- Repair: load and verify the complete 48-layer Qwen3-30B-A3B checkpoint, then retain and execute the exact prefix through block 28. Capture blocks 24 and 28 exactly as registered; blocks 29--48 are a causal suffix and cannot alter earlier hidden states. Record architecture depth, executed prefix, and skipped suffix in every shard manifest.
- Equivalence guard: rerun the 128-row long-sequence smoke with identical data and compare its merged \(X/U\) tensor against the prior 48-layer smoke. Require exact equality up to the existing extraction tolerance before authorizing full execution.
- Boundary: no weights, inputs, hooks, target tokens, captured layers, precision, or scientific settings change. This is a forward-prefix optimization only.

## 17. Amendment A07 — Extraction Batch Freeze

- Trigger: the A06 prefix smoke was initially run with batch 32, while its 48-layer reference used batch 16. Although both runs passed within-run deterministic replay, their merged arrays differed (maximum absolute difference 0.45556640625; relative L2 difference 0.07219980657100677). Metadata hashes were identical.
- Isolation result: rerunning the 28-layer prefix on the identical 128 long-sequence rows with batch 16 produced exact array equality against the 48-layer batch-16 reference: maximum absolute difference 0 and relative L2 difference 0. All identity and merge guards passed, and job `pt-il2q3dma` succeeded.
- Repair: freeze extraction batch size to 16 for the full run. Batch 32 is rejected for this experiment even though it did not OOM. Within-run replay remains required.
- Boundary: the observed batch dependence is an implementation/numerical reproducibility issue, not evidence about H2--H4. No TEST metric, Router, residualizer, or projection result was inspected to make this choice.

## 18. Amendment A08 — Descriptive-Diagnostic Operationalization

- Trigger: the post-run completeness audit found that Section 7 named three descriptive diagnostics but did not fully specify the fine-label rank estimator or the numerical eligibility rule for random spectral-coordinate sampling. The block-24 H3 result was already known, so every quantity below is barred from changing H1--H4 or reopening the dense-Gaussian branch.
- Full-space distance audit: independently of H3, use the A05 pair seeds and 100,000 parent-stratified pairs per TEST panel (50,000 within-parent and 50,000 between-parent) to report \(D_{out}/D_{in}\) and \(Q_{0.05}(D_{out})/Q_{0.95}(D_{in})\) in unprojected \(R_U\).
- Supervised functional dimension: use fine labels and ranks \(\{1,2,4,8,16,32,64,128,256,512\}\). TRAIN fits the same L2 multinomial-logistic family; DEV selects \(C\in\{10^{-6},\ldots,10^2\}\) with the same balanced-accuracy/log-loss ordering. Refit five registered seeds, take the best rank-\(r\) SVD truncation of each frozen Router weight, and evaluate both TEST panels without refitting. The reported \(r_{90}\) is the smallest rank with at least 90% chance-corrected full performance on both panels for at least four of five seeds including `24001`. This is a supervised readout diagnostic, not geometric affine rank.
- Spectral-uniformity diagnostic: on TRAIN only, compute the covariance eigenbasis of standardized \(R_U\). At the registered \(r_{90}\), report supervised-subspace leverage coherence, normalized entropy, head-energy coverage, and a 1,000-draw same-rank Haar null. High entropy alone is never treated as low coherence.
- Coordinate-sampling eligibility: use the fixed A05 seed to draw 1,000 parent-stratified TRAIN difference vectors. Let \(\widehat\mu\) be their maximum vector coherence in the TRAIN covariance eigenbasis and freeze \(\varepsilon=0.5\), \(\delta=0.05\), \(M=1000\). The branch is eligible only if the theorem-three sufficient bound
  \[
  m_{bound}=\left\lceil\frac{8\widehat\mu}{3\varepsilon^2}\log\frac{2M}{\delta}\right\rceil
  \]
  is at most the registered maximum \(m=1024\). Otherwise emit `SKIPPED_TRAIN_COHERENCE_BOUND`. TEST data cannot enter this eligibility decision. If eligible, use the registered dimensions and 30 fixed-seed coordinate samples; because H3 failed, NMR and the dense-Gaussian comparison remain undefined/skipped and the coordinate result is descriptive only.
- Execution: these diagnostics reuse the immutable Qwen3-30B-A3B residual arrays produced by reserved four-H100 job `pt-x588ixj0`; run them on another exact reserved four-H100 worker for provenance consistency.
- Boundary: A08 closes missing implementation detail only. It cannot convert H3 `Fail`, authorize H4, select another layer or Router, or support a theorem/mainline claim.

## 19. Amendment A09 — Theory-Conformance Repair

- Trigger: the closure audit compared the implementation line by line with the 0824 theory document and found two descriptive-diagnostic mismatches. A08 estimated extrema from 100,000 sampled TEST pairs although the theory defines extrema over all TEST pairs; A08 also used SVD truncation of a frozen full Router although the theory requires learning a supervised orthogonal input subspace and its low-dimensional classifier.
- Exact-distance repair: enumerate every unordered pair in each 2,560-row TEST panel, separately for each registered block. Report the exact maximum within-parent distance, exact minimum between-parent distance, and quantiles over the same complete pair population. The expected counts are 3,275,520 total pairs, 408,320 within-parent pairs, and 2,867,200 between-parent pairs per panel.
- Functional-dimension repair: for every registered rank and seed, parameterize the fine-label softmax weight as \(W_q=P_qA_q\) with \(P_q^TP_q=I\). Fit on TRAIN only, use DEV-only early stopping, and open the two TEST panels only for the frozen evaluation. SVD of the registered full fine-label Router is permitted only as a deterministic warm start. Ranks \(q\ge64\) are capacity-equivalent because a 64-way linear softmax weight has rank at most 64; they are still reported explicitly.
- Frozen settings: ranks, seeds, fine labels, full-Router regularization selected before TEST, 90% chance-corrected retention rule, both TEST panels, registered blocks, and all H1--H4 results remain unchanged. Optimization is AdamW, learning rate 0.01, maximum 80 epochs, patience 15, and weight decay \(10^{-4}\).
- Provenance: execute both repairs from the immutable residual arrays of job `pt-x588ixj0` on a new exact reserved four-H100 ACP worker. Preserve the A08 sampled/SVD output as superseded exploratory evidence rather than overwriting it.
- Boundary: these repairs can change only the descriptive distance and functional-rank readings. They cannot rescue H3, authorize H4, estimate affine-union rank, prove expert utility, or change the main verdict.
