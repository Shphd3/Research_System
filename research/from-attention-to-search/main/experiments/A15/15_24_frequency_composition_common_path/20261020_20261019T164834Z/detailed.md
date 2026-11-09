# Detailed record: Frequency-mixed representations and forced high-frequency-path calls

[Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/15_24_frequency_composition_common_path_anchor.md) · [Frozen Protocol](protocol.md) · [Summary](summary.md) · [Model and inference note](model_and_inference_cn.md) · [Chinese Detailed](detailed_cn.md).

Execution root, abbreviated **R** below:

`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_composition_common_path/20261019T164834Z`

Code, log, and array paths relative to R refer to this execution-owned directory. The [artifact manifest](artifact_manifest.json) supplies complete provenance links. Chinese Anchor and Protocol are the frozen originals; English versions are companions rather than new authority.

## 0. Question, direct answer, and evidence qualification

At the same top-2 budget, does forcing a call to the high-frequency list improve learning on inputs containing low-frequency features relative to free choice? Does that increment exceed the same intervention on size-matched random lists?

All 8/8 models completed 168 updates and 85,548 answer targets; unified terminal DEV evaluation is complete. The B1 macro-NLL Delta_T is +0.00098945 and interaction I is +0.00246136. They fail the predicted negative direction. Seed directions disagree, frozen resampling ranges cross zero, and extremely low support additionally limits macro-interval interpretation.

Engineering state: **COMPLETE**. Frozen-design point comparisons: usable as bounded descriptions. Statistical and mechanism interpretation: **BOUNDED**. This round's hypothesis: **NOT_SUPPORTED**, without a universal invalidity claim. The researcher's mechanism judgment, question closure, and next decision remain **Unknown**; Focus state was not changed.

## 1. Objects, computations, and units

| Object | Actual computation | Purpose and boundary |
|---|---|---|
| Feature frequency p | Fraction of TRAIN answer-prediction positions with z > 0 | Frequency, not z amplitude, token frequency, or semantic difficulty |
| Final-layer amplitude proxy a | z times the norm of the raw layer-28 decoder vector | Nonnegative atomic magnitude, not additive energy in a nonorthogonal dictionary |
| Bands B1–B4 | Original four intervals of positive TRAIN p, equally wide in log frequency | Original boundaries retained; U contains 907 TRAIN-zero features and is not deleted from input |
| Current token | input_ids[t] at the cached position t | Already visible; the representation predicts t+1; first-answer prediction is at the template's final position |
| Target token | input_ids[t+1] | Answer supervision including EOS; used for loss/explanation, never routing input |
| Reception r | Probability that a feature's assigned expert is called when that feature fires | Unsupported features remain NA; supported but never received is zero |
| Exposure frequency q | Feature hit rate among positions received by an expert | p × r = load × q; top-2 total load sums to two |
| Signed PCA coefficient beta | Inner product of a projected, centered band vector with projected real centered h, divided by projected h squared norm | Bands, U, and residual sum to one; coefficients may be negative and are not exclusive energy shares |
| B1 macro NLL | Mean NLL per firing feature, then equal mean over supported features | 838 DEV features estimable, 856 NA; one position may contribute to several feature means |
| B1 position NLL | Mean over unique positions containing at least one B1 feature | 1,701 DEV positions, each counted once; a different weighting from macro NLL |

## 2. Research source and the decision this round tests

The two October 19 meeting documents were read in full. Eighteen substantive intuitions are traced to source paragraphs/timestamps in the [mentor-intuition audit](mentor_intuitions_audit_cn.md). Original DOCX files, extracted paragraphs, and earlier read-only audits are preserved under R/provenance. The central distinction is between an input containing shared components, calling shared parameters, and those parameters improving the task.

Previous score calibration, φ subdivision, mean centering, and epoch-one expert-spectrum results are reused as prior evidence, not relabeled discoveries. Reuse/adaptation reasons are in R/provenance/reuse_audit.md and math_design_audit.md. The new T organization splits each frequency band by a fixed hash rather than the previous relation groups, avoiding simultaneous changes due to singleton or unstable relation subgroups. This is not a φ-group learning test.

## 3. Freeze, conformance, amendments, and deviations

Freeze time: 2026-10-19T16:51:38.506659Z, or October 20 at 00:51 China Standard Time.

- Config SHA256: `dc8a3a886d97caf64d2ac97279056edc89818c7cbf727a1adfb662e47725d14e`.
- Original trainer SHA256: `5bbbad26e2f3bdb65166bdbbbfb3a7b7cb3b6d97f699f3a5fd177fd4502d89e5`.
- Chinese Protocol SHA256: `80c68d0ca4f8fea92659b5799d70c9ee9ae6881e0fe17d459b664a89d964279d`.

| Registered item | Actual execution | Qualification |
|---|---|---|
| Autonomous analysis, learning after analysis, four H100 Reserved GPUs | Authorization and frozen config preserve the user's instruction; continuation stayed within it | No repeated step approval or larger resource envelope |
| Data, feature pool, score, four arms, two seeds | Frozen settings retained | No result-dependent tuning |
| One epoch, 168 updates, 85,548 targets | All eight models complete; five common TRAIN/EVAL milestones | No short-run model presented as a matched endpoint |
| Terminal DEV loss only after all models complete | Receipt records unified evaluation; no DEV model/checkpoint selection | DEV is not external new data; extraction/routing already existed and this round's representation analysis had read it |
| 1,000 whole-dialogue bootstrap draws | Original implementation retained; absent features become NA before each macro mean | Effective feature set varies; fixed-838-feature confidence coverage is unqualified |
| Bounded execution and recovery | AFS flock EAGAIN stopped the first job; completed T_F models reused, six others recovered | Engineering repair only, no scientific parameter changes |
| 120-minute wall-clock limit | Active time stayed within budget, but a roughly nine-hour interrupted conversation exceeded continuous elapsed time | Explicit elapsed-time deviation; interruption is not hidden as computation |
| Companion appendix | Lists/control/seed frozen, but registered after some DEV representation had been inspected | Exploratory, not independent confirmation; no four-arm change followed |

The [recovery amendment](execution_amendment_01_cn.md) and [exploratory appendix](analysis_appendix_01_cn.md) are separate records and do not rewrite the frozen body. Small interface/logging errors and original failure evidence remain in R/logs. Terminal outputs were independently checked; unrelated models were not recomputed.

## 4. Actual setup: data, model, routing, and optimization

### 4.1 Data and position provenance

Assets: `data_tulu_sft_route_20261019t012300z` and `representation_tulu_sft_route_20261019t012300z`. Source data and caches:

`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/sft_route_learning/20261019T012300Z`

Tulu revision: `6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752`. Sources include cot, sharegpt, code_alpaca, gpt4_alpaca, wizardlm, flan_v2, and oasst1. A dataset-source label is not a validated semantic-domain label.

Only the first user/assistant exchange is used, rendered as a Base-model Instruction/Response template. TRAIN has 1,024 dialogues and 85,548 answer-prediction positions; repeatedly exposed EVAL has 256/22,446; DEV has 128/10,340. Supervision covers answer targets including EOS, excluding prompt and padding. Cache hidden states, CSR z, block_id, position_id, and target map exactly to JSONL source_file, source row, input_ids, answer_start, and visible prefix. All splits passed current/next-target position checks; no mismatched windows were joined.

Exact cross-split overlap of original prompts and normalized prompt/assistant/pair hashes is zero. Near-duplicate independence remains **Unknown**. Splits come from the same prepared data and are not an external population. DEV was unused as a metric in the checked earlier named trainers; this round froze design before representation review and revealed final DEV learning loss only after all eight models finished.

### 4.2 Frozen dictionary, hidden states, and routing costs

Base/tokenizer: `/data/share/Qwen3-0.6B-Base`.

CrossCoder checkpoint:

`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt`

It records 244,140 updates and 999,997,440 cumulative training positions. The 14 actual model layers are 2, 4, …, 28, corresponding to zero-based blocks 1, 3, …, 27, at residual-post. Dictionary width is 16,384, hidden width 1,024. TRAIN centering/vector-RMS state and inference threshold 0.051281172782182693 remain frozen.

Shared z jointly reads the 14 layers. The raw final-layer decoder is reused from the existing train_fixed.npz, preserving inverse scale 374.349512 and offsets. In the geometric analysis, h is centered by its frozen TRAIN mean and each band vector by its own frozen TRAIN mean. DEV is not re-centered. Consequently DEV beta includes split-mean shifts and is not a within-DEV covariance about DEV's own mean. This is not a final-layer-only independent activation dictionary, nor a free router deployable at arbitrary earlier layers without computing later layers.

No Base/CrossCoder representation extraction was repeated. Training uses aligned hidden/z caches and computes only the added experts plus the frozen final norm/head. This round includes offline route computation but does not re-charge historical extraction. End-to-end deployment throughput and efficiency gains are **NA**, not inferred from cache-based runtime.

### 4.3 Membership and fixed routing

The 15,477 positive-frequency features have band sizes 1,694/5,673/7,013/1,097. T sorts members within each band by SHA256("20261020:featureID") and splits them into expert groups of sizes:

847, 847, 2,837, 2,836, 3,507, 3,506, 549, 548.

R shuffles the same pool using seed 73129 while preserving these exact eight sizes; it does not match frequency within groups. See [membership](tables/routing_feature_membership.csv) and [group definitions](tables/routing_group_definition.csv).

A pair's score is its sum of atomic amplitudes divided by that pair's TRAIN mean. Within the chosen pair, the subgroup with the larger raw amplitude sum supplies the called expert. F selects the two highest-scoring distinct pairs. H always calls pair four and the highest of the other three. T pair four is the highest-frequency band; R pair four is simply its predetermined random counterpart. Ties choose the smaller ID. All-zero inputs are retained with deterministic lower-ID fallback. No all-zero fallback or zero-amplitude forced-pair event occurred in the analyzed panels. Thresholds were not changed.

### 4.4 Trainable branch and matched budget

Eight independent, fully trainable, bias-free SwiGLU FFNs have hidden/intermediate width 1,024; no LoRA. Each has 3 × 1,024² parameters, totaling 25,165,824. Top-2 activates 6,291,456 expert parameters and approximately 12,582,912 forward matrix-multiplication FLOPs per position, excluding elementwise operations, head, Base, and feature extraction.

A shared TRAIN hidden RMS scale of 15.983072484195144 normalizes inputs as h/scale; expert outputs are multiplied by scale. Each of the two residual outputs receives weight 1/2. No mean is subtracted.

Gate/up weights are random and down weights are zero, producing an exactly zero initial residual branch. The measured smoke maximum logit difference is zero. Down receives a gradient at the first step, and gate/up gradients become nonzero after down updates. Expert gradients and exposure counts are logged. Seeds 11 and 22 pair initialization and data order across all conditions.

Each condition uses one epoch, effective batch 512, microbatch 128, final batch 44, 168 updates, and 85,548 valid answer targets. Total expert-position exposure is 171,096 per condition. Loss is summed answer CE divided by the actual valid target count in the effective batch, never normalized independently per expert. There is no routing regularizer.

AdamW: learning rate 3e−4, betas (0.9, 0.95), epsilon 1e−8, weight decay 0.01, gradient clip 1, nine warmup updates, cosine decay to 0.1 of peak. A second learning rate was not tried.

Steps 0/42/84/126/168 evaluate complete TRAIN and exposed EVAL panels. The terminal step 168 was predetermined, not selected using EVAL. Each seed has shared initial weights; steps 42/84/126 save weights only. Step 168 saves model, optimizer, RNG, order, cursor, tokens, and counters. Formal saved states are **SAVED_NOT_REPLAYED**; exact next-step weight/optimizer/NLL recovery was verified in smoke, not falsely asserted for every formal checkpoint.

## 5. Metrics and frozen decision branches

The primary low-frequency pool is this round's 1,694 T-B1 features, **not the legacy cache.low_ids pool of 964**. All conditions use the same 838 supported DEV features, averaging NLL within each feature's firing positions and then equally over features. Overlapping feature supports are not independent observations. The 1,701 unique B1-containing positions and all 10,340 positions have separate means; high-frequency macro/position results are also delivered.

Define Delta_T = T_H − T_F, Delta_R = R_H − R_F, and I = Delta_T − Delta_R. Support requires negative Delta_T and I with the original registered ranges below zero, while inspecting both seed directions. The practical marker of 0.01 nats was frozen beforehand. One thousand whole-dialogue draws preserve condition/seed pairing but are conditional on the two trained seeds, not population-level model replication.

The original point estimates fail the support rule. Uncertainty limitations do not justify selecting another test to rescue the hypothesis.

## 6. Decisive evidence chain

| Question | Source and computation | Observation | Permitted interpretation |
|---|---|---|---|
| Does forced high-frequency calling add learning benefit? | final_evaluation condition/paired tables; train_matched.py | Delta_T +0.00098945; I +0.00246136 | Not supported here; directions disagree, ranges cross zero, support is low |
| Does mixture translate into owner reception? | Original CSR z plus fixed routes; route_analysis.py | DEV T 72.76%→66.75%; R 32.38%→24.08% | A forced slot displaces some owner opportunities; functional loss is untested |
| Is high frequency simply the mean? | Real-h TRAIN PCA and raw decoder decomposition | PC1 covers 11.61%; DEV B4 beta 90.13%, first-16 beta 68.30% | Alignment with leading variation, not a share of all information or proof of gradient dominance |
| How predictive is token identity? | TRAIN current-ID mean predicting B1 share | Full DEV R² 0.43351; seen 0.68679; 15.82% positions unseen | Strong identity association, not complete determination; residual is not certified contextual semantics |
| Do particular high-frequency companions exceed background? | TRAIN-selected eight plus equal-bin-count random control | DEV support≥5: 114 features, event-weighted difference +38.06 pp | Exploratory association; token/source/context not isolated |
| Can stable semantics be assigned? | Fixed 16-feature text review, complete visible prefixes | Lowest-band DEV supports 1/0/1/1 | Stable semantic or rare-knowledge labels are unqualified |

The artifact manifest connects source tables, hashes, and qualification. Code and freeze receipts remain execution-side.

## 7. Results, negative outcomes, and uncertainty limits

[Condition values](tables/condition_results.csv), [paired comparisons](tables/paired_comparisons.csv), and [complete DEV feature-level results](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_composition_common_path/20261019T164834Z/tables/learning_final_per_feature_dev.csv), and the [primary B1 reading table](tables/dev_low_feature_results.csv) are delivered. Larger TRAIN/EVAL feature tables remain execution-side. Unavailable quantities remain NA.

| Two-seed mean | Overall DEV NLL | B1 feature-macro NLL | B1 unique-position NLL |
|---|---:|---:|---:|
| Base | 1.24887 | 1.06584 | 1.06049 |
| T_F | 1.22614 | 1.05632 | 1.06189 |
| T_H | 1.22714 | 1.05731 | 1.06276 |
| R_F | 1.22720 | 1.05339 | 1.05525 |
| R_H | 1.22698 | 1.05192 | 1.05346 |

All arms improve overall DEV relative to Base; this is not a case where every training condition worsens because of a common implementation failure. T_F/T_H slightly worsen the B1 position mean relative to Base while improving the feature macro mean. Both weighting schemes are shown.

| B1 macro comparison | Seed 11 | Seed 22 | Paired-seed mean | Registered resampling range |
|---|---:|---:|---:|---:|
| Delta_T | −0.00015215 | +0.00213105 | +0.00098945 | [−0.00303863, +0.00478613] |
| Delta_R | +0.00004101 | −0.00298483 | −0.00147191 | [−0.00736736, +0.00352981] |
| I | −0.00019316 | +0.00511588 | +0.00246136 | [−0.00388754, +0.00983927] |

There is no consistent two-seed primary benefit. Small point differences do not establish equivalence. T_F minus R_F is approximately +0.00293 in B1 macro NLL, providing no observed advantage of frequency organization over this particular random organization; it does not rank random organizations generally. R_H's lowest four-arm macro point is a post hoc description, not a newly certified best method.

The frozen macro bootstrap sets a feature to NA when a resampled dialogue panel contains none of its firing positions, then averages the remaining features. Its effective feature set therefore changes. Preserve the original ranges, but do not call them calibrated confidence coverage for the original fixed 838 features. The [pre-reveal primary uncertainty audit](provenance/primary_uncertainty_audit_cn.md) was written before its author read DEV learning values. It distinguishes an ambiguity in the frozen finite-sample estimand from a false assertion that all point comparisons are invalid. Scientific support remains BOUNDED; the point estimates already fail the hypothesis's direction rule.

Terminal TRAIN overall NLL across eight models is 0.94702–0.95967; Figure 4 retains the learning curves. The 64-position smoke fit falls from 1.78766 to approximately 0.0000294 while an auxiliary 64-position validation loss rises from 1.40844 to 7.13281. This was a bounded overfitting diagnostic, not the outcome of the eight formal models, and did not trigger a wider tuning search.

### 7.1 Token and feature are not interchangeable

DEV R² is 0.433508 over all positions and 0.686793 over 8,704 TRAIN-seen-ID positions. The 1,636 unseen-ID positions fall back to the TRAIN global mean and have R² −0.116889. On seen IDs, MAE is 0.00056299 versus 0.00140018 for the global predictor. EVAL all/seen R² is 0.432356/0.597763. Excluding the first-answer template prediction position gives similar values.

Within-ID variance accounts for 13.69% of variance in the DEV seen-ID panel and 20.11% in EVAL. This is a descriptive decomposition, not the causal contribution of context. It also does not complement the TRAIN-fitted predictor's R², which uses a different fitting side and reference.

### 7.2 Companion association and its uncertainty qualification

For each of the 1,694 B1 features, TRAIN selects eight B4 companions by positive P(high|low) − p_high, breaking ties by feature ID. A fixed-seed random control matches the number of companions in each of ten log-frequency bins. No route search or EVAL example selection is repeated.

Across all 838 DEV-supported B1 features, selected/control macro hit rates are 57.87%/21.52%, a descriptive +36.35 pp difference. Among the 114 with at least five DEV hits, macro rates are 56.02%/20.08%, difference +35.94 pp. The event-weighted rates are 58.15%/20.10%, difference +38.06 pp, with a whole-dialogue percentile range of +34.04 to +42.66 pp. The latter uses 831 low-feature hit events, not 831 unique positions. No DEV feature reaches support 20; that panel stays NA.

The TRAIN macro point is +69.86 pp, outside its original +67.32 to +68.57 pp range. The same missing-feature/re-normalized-macro mechanism is present in the companion code. DEV uses it too; an interval containing its point is not a coverage qualification. The main narrative therefore retains macro points as descriptions and uses event-weighted association with explicit boundaries, without rerunning to obtain a more attractive interval. See the [companion uncertainty audit](provenance/companion_uncertainty_audit_cn.md).

Even the aggregate event ratio's range is conditional on the fixed lists, random control, and original support panel; it excludes membership-selection and residual within-bin frequency uncertainty. This appendix was registered after partial DEV representation exposure and is exploratory. Current ID, continuation target, source, format, and shared context remain competing explanations. Association is not functional calling, dependence, learning, or capacity.

### 7.3 Historical top-1 failure decomposition is background

The previous φ-R1 EVAL macro reception is reproduced at 72.218%. Unselected frequency bands account for 22.832 percentage points, and selected bands with an unselected subgroup account for 4.950 points. Its post hoc top-1 macro-reception oracle is about 97.02%; this is a panel-specific diagnostic bound, not a deployable rule.

The new T lists and top-2 compute differ from the old lists/top-1 setting. Their contrast cannot certify φ utility or equal-compute top-2 benefit.

## 8. The five figures and how to read them

The [figure reading notes](figures/reading_cn.md) separate observations, permitted conclusions, and design implications. Figure-source CSVs and plot_manifest preserve source hashes.

1. [Current-ID prediction](figures/figure1_token_identity.png): EVAL/DEV on the horizontal axis, R² vertically; full and seen-ID panels are shown alongside unseen-ID support. Identity is predictive, not a semantic explanation.
2. [Signed geometry](figures/figure2_signed_geometry.png): TRAIN-fitted PC1 and first-16 subspaces, with beta separate from total variance coverage. Whole-dialogue resampling holds the projection fixed. Beta is not exclusive energy or total information.
3. [Static routing](figures/figure3_static_routing.png): Common-pool B1 reception, pair-four calls, and expert loads are distinct. Total load is 200%; H's 100% forced-pair call rate is a definition, not mechanism evidence.
4. [Learning curves](figures/figure4_learning_curves.png): Actual updated answer targets 0/21,504/43,008/64,512/85,548; complete TRAIN and exposed EVAL overall/B1-macro NLL; both seeds retained. EVAL did not select the endpoint.
5. [Terminal DEV](figures/figure5_terminal_dev.png): Four-arm seed values, three paired differences, zero reference, and original percentile ranges. The changing estimable-feature set is explicit. The primary direction is unsupported; ranges are not certified fixed-838-feature coverage.

`rendering_review.json` records the visual checks of all five PNGs. PDFs are also available for enlargement. Extra decorative plots did not substitute for answering the question.

## 9. Failures and what they rule out

| Stage | Observed checks | Explanation limited or excluded | Still unresolved |
|---|---|---|---|
| Positions and supervision | Current/target mapping, one-token shift, EOS across all splits | Mismatched windows or prompt loss mistaken for answer loss | Near duplication and source mixture |
| Initialization and gradients | Zero logit difference, down gradients first, gate/up later, exact smoke resume | Dead all-zero branch or an immediate Base-logit change | Whether each expert learns useful function |
| Original job | AFS blocking flock EAGAIN; six models stopped before formal updates | Numerical model failure was not the cause; learning parameters need not change | Future shared-storage lock semantics |
| Full training | Same 168 steps for eight models, TRAIN decreases, overall DEV beats Base | Universal training deterioration is not the explanation | Feature-level improvement or sufficient convergence |
| Main hypothesis | Delta_T/I fail support; seed directions disagree | Mixture alone does not justify a beneficial forced high-frequency call | Frequency proxy error, slot displacement, limited budget, adequate frozen Base |
| Semantics/statistics | Very low support and changing bootstrap feature pool | No stable knowledge labels from a few peak activations | Feature meaning, within-token context, task-useful directions |

The round does not refute a specific physical mechanism. It weakens the decision leap from frequency/co-occurrence/PCA proxies to a beneficial forced call.

## 10. Execution history, costs, and recovery ledger

The round began around October 20 at 00:48 China Standard Time: complete meeting reading, hypothesis/setup freeze, CPU token/geometry/routing analysis, analysis gate, GPU smoke, then partial success and a storage-lock failure. On continuation, the failed job was verified, both T_F models reused, the remaining six completed, and DEV evaluated jointly. R's October 19 UTC timestamp is not a separate new experiment.

- Original GPU job `pt-gzle2ypd`: FAILED, 109.453 active seconds.
- Recovery job `pt-4kefocs4`: SUCCEEDED, platform interval 2026-10-20T02:03:08Z–02:05:12Z.
- Recovery supervisor active time: 119.481 seconds; cumulative active GPU-job time: 228.934 seconds, approximately 3.82 minutes. Platform/scheduling boundaries are reported separately.
- A roughly nine-hour interrupted conversation contained no training execution and is excluded from active compute. Continuous elapsed wall time nevertheless exceeded the original 120-minute envelope and is explicitly recorded as a deviation. No second concurrent reservation was opened.

CPU statistical durations are 16.61 seconds for token/context, about 23.04 seconds for geometry, about 29.16 seconds for routing, and 8.27 seconds for the exploratory companion appendix. Independent work respected the aggregate eight-thread envelope; per-task peak RSS was approximately 0.90–2.49 GiB.

The GPU phase's total CPU limit was eight threads. Sampled worker RSS peaked around 6.69 GiB, excluding lightweight supervisor overhead; peak allocated memory per GPU was about 1.01 GiB. At supervisor completion, distinct files under R totaled 5.26 GiB, with later small tables/documents recorded in the final receipt. These remain below the 64-GiB RSS, 16-GiB-per-GPU allocation, 24-GiB new-disk, and 35-minute active GPU limits. Historical feature extraction is excluded, so no end-to-end efficiency claim follows.

All model milestones, logs, TensorBoard outputs, and resumable terminal states remain execution-side. Completed T_F models were not retrained. There was no new Base/dictionary training, full ten-million-position relation recount, or additional model extraction.

## 11. What changed in our understanding

The initial intuition could be read as: rare-feature inputs also contain common structure, so adding a high-frequency path should help them learn. The results separate three links: representations are mixed; forced calls change update opportunities; the predicted learning gain is unsupported. Retain mixture, but withdraw the direct prescription to reserve a high-frequency expert slot from mixture alone.

High-frequency vectors can align with leading variation without aligning with task-useful shared updates. The frozen Base already supplies common computation, and the added high-frequency-list experts have not been functionally validated as common modules. Negative learning evidence therefore does not imply common structure is useless. Conversely, T_F's higher owner reception than R_F does not produce a corresponding held-out low-frequency advantage; reception alone is an insufficient design target.

## 12. Claims not established

This does not establish common semantic modules, token difficulty, rare-knowledge mastery, parameter-gradient interference, causal attention origins, cross-model capability changes, pretraining capacity gains, φ learning utility, equal-compute top-1/top-2 superiority, or equivalence between h spectra and weight-matrix spectra. No first-direction removal followed by re-encoding was performed. Previous out-of-distribution centering degradation is not successful removal of common information.

## 13. The single next decision

Researcher decision: **Unknown**.

**AI suggestion:** On the fixed trained checkpoints, do high-frequency-list experts provide task contribution that can be tested by controlled call replacement? Preserve the two-expert budget and compare fixed-weight calls to connect list/representation proxies more closely to actual function. Even that would not identify the training mediator. It has not been executed and is not new authorization or automatic continuation.

## 14. Assets, source tables, text, and hashes

The [artifact manifest](artifact_manifest.json) and [completion receipt](completion_receipt.json) cover input access, code reuse, implementation/recovery audits, statistical qualifications, figure sources, and output hashes. Full feature/routing/group tables, cross-terms, and NLL arrays remain under R. The project carries selected small evidence and five figures, not raw caches or weights.

Eight formal checkpoint families, one actual smoke-resume state, and one analysis asset are registered in assets/catalog.json and passed the round's strict-access check. Registration confirms existence/saving, not scientific qualification. Formal resume state is **SAVED_NOT_REPLAYED**. The access snapshot is `assets/checks/2026-10-20_020552_frequency_composition_outputs.json`, relative to the Research_System root.

The fixed 16-feature evidence and 50 available display slots are in the [reading index](texts/feature_meaning_reading_cn.md) and [full texts](texts/token_context_cases_cn.md). The two later uncertainty audits take precedence over early, unqualified macro-CI wording in the reading notes; original notes are not promoted to primary conclusions. Complete machine-readable lists, contexts, and original tables remain traceable.

## 15. Navigation and stopping boundary

[Summary](summary.md) · [Chinese Summary](summary_cn.md) · [Chinese Detailed](detailed_cn.md) · [Protocol](protocol.md) · [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/15_24_frequency_composition_common_path_anchor.md) · [Figure notes](figures/reading_cn.md) · [Mentor-intuition audit](mentor_intuitions_audit_cn.md).

Execution has stopped, with no pending training. MoE_Router retains ownership of code, raw data, logs, and checkpoints; Daily is a discussion entry. No subsequent experiment, scientific-state transition, commit, push, or external synchronization was started.

## 16. User-requested frozen diagnostics, 2026-10-21

The stopping statement above belongs to the original round. Subsequent authorized replacement, paired-position and frozen-residual checks are recorded in [diagnostic results and numerical limits](diagnostics_20261021/results.md). Local GPU inference completed, but replay qualification against old T_H NLL failed. The original primary and conclusion remain unchanged. Ordinary-MoE restoration is recorded separately in the diagnostic execution history.
