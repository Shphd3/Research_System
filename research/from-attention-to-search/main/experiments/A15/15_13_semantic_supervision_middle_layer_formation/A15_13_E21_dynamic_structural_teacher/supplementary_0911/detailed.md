# E21 supplementary audit — evidence ledger

Status: COMPUTED / BOUNDED / EXPLORATORY. Scientific interpretation remains AI_DRAFT_AWAITING_HUMAN_CONFIRMATION. This is a supplement to the frozen [E21 Protocol](../protocol.md), not a retroactive amendment or a claim that all original E21 gates passed.

## 1. Scope, authority, and actual execution

The researcher requested analysis completion and a four-part meeting report on 2026-09-11, then supplied the intended story: an overcomplete SAE may expose useful existing semantic features for LoRA-MoE routing; fixed and changing coordinates must be separated. This authorizes the bounded analysis/replay described in the date-local [execution scope](../../../../../research_notes/sae_representation/20260911/0911_minimal_followup/execution_scope_cn.md), not new main-model training or scientific state promotion.

Execution root E: `/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix`.
Run R: `E/runs/full-20260909T203104Z`.
Supplement O: `E/audits/0911_minimal_followup`.

| Stage | Actual scope | State |
|---|---|---|
| Existing geometry | task_f, task_u, sae_b_u, dynamic_sae_b_u × seeds17/29/43 ×21 checkpoints ×2 splits =504 shards | Recomputed and SHA/checkpoint-linked |
| Clustering ruler | K-means K8 n_init20; diagonal GMM K8 n_init1/max_iter200; both fixed t0 partitions. Additional 6 endpoints ×5 solver seeds ×2 methods ×3 training seeds =180 noise fits | Completed; solver repeats are not training seeds |
| Standardized model replay | static/dynamic SAE ×3 seeds ×6 points {0,32,64,128,256,512}=36 shards;247 records,1247 answer-prediction positions | Forward only; model states unchanged |
| SAE readout | fixed D0/G0 and each dynamic seed's saved refreshed D/G on both replayed arms;72 metric rows | No dictionary optimizer updates |
| Cross readout |12 H/D comparisons and12 encoder/group-map comparisons | Fixed inputs for each swap |
| Content/route | systematic group positive/counterexamples, neighborhood examples, source/format descriptive association, probability/actual-route responses | Completed with semantic/causal boundary |

Local runtime: available NVIDIA H100 MIG slice, approximately40GB; Python/Torch/Transformers loaded via E/runtime.sh. No new remote submission. Main-model optimizer updates **0**; SAE optimizer updates **0**. Representative recorded stage times: geometry about80 seconds/seed, replay127.96 seconds, SAE analysis97.71 seconds, group decomposition30.57 seconds, full shard integrity266.88 seconds. Some stages ran concurrently; these times must not be summed as wall time or interpreted as original training cost. Exact terminal receipts live in O.

The existing model is Qwen3-0.6B-Base, last block27 MLP pre-hook input h (1024 dimensions),8 top-1 experts plus shared rank16 adapters. U opens the final attention (6,291,712 parameters); the adapter has303,112 trainable parameters. F freezes attention. Earlier blocks, final MLP, final norm and vocabulary head stay frozen. Existing training used512 AdamW updates, microbatch8 × accumulation16, expert/shared lr2e-4, router5e-4, attention2e-5,26-step warmup then cosine decay; structural weight0.01→0.001 linearly, router-only structural gradients, per-group norm clipping1.0. Attention/shared/experts receive task gradients only. Balance bias increments by0.001 per update according to expert load; actual dispatch uses logits+bias, while p is softmax of raw logits. All eight source schedules are retained; t512 seed17 contains4,339,651 answer-token presentations. These are repeated presentations, not unique training examples. Checkpoints are saved at0,1,4,8,16 and every32 to512, without best-checkpoint selection.

Existing dynamic teachers refresh at32/64/128/256,400 SAE optimizer steps each, warm-start weights but recreated Adam optimizer. The t0 block reads cached targets; subsequent blocks evaluate the teacher on current h. Buffers are historical mixed-step observations, not fresh forward passes at the refresh checkpoint. The present audit changes none of that training.

## 2. Identity and eligibility before interpretation

| Guard / conflict | Evidence | Impact |
|---|---|---|
| 504 NPZ SHA256 values match their sidecars, and sidecars match exact checkpoint hashes | O/input_manifest.json; integrity_receipt.json, PASS,0 errors | File identity established for audited subset |
| Current frozen fm source matches R/run_identity.json | integrity_receipt.json | Current fm identity matched |
| Initial attention/adapter tensors and schedules match between static/dynamic SAE, all3 seeds | integrity_receipt.json; implementation_checks.json | No initial-weight mismatch found |
| Stored preanswer t0 h differs between arms: direct relation RMS0.001978; maximum h difference2.203125 | tables/geometry_pairs.csv,update0 | Historical extraction/runtime equivalence is not established; cannot attribute small cross-arm effects solely to refresh |
| Unified local replay gives exact static/dynamic t0 h,p,actual equality, all3 seeds | O/implementation_checks.json | Current replay comparisons use one pipeline; does not repair historical training confounding |
| Full wrapper vs skip-lm-head h and future-suffix invariance checks | O/replay_parity.json | Tests extraction path and causal observation position on8 fixed records |
| Historical dynamic source identity omits dynamic/*.py | Current identity and source_hashes implementation | Exact historical dynamic-code identity remains UNVERIFIED; current-source findings are not automatically historical execution facts |
| E21 calls for fixed-t0 membership; previous dynamic analysis refits every checkpoint | Current dynamic/analyze_dynamic.py; new geometry_audit.py | Previous W/B comparison is not the registered ruler; new fixed-membership values are exploratory corrections |
| Previous report gives source-balanced equations but phase1 code weights clusters equally | phase1_core.py::structure_terms | Old values are a different statistic, not automatically arithmetic errors; both retained in tables/geometry.csv |
| Auxiliary loss computed inside no_grad in current SAE refresh source | O/implementation_checks.json: auxiliary requires_grad=false, gradients identical with/without auxiliary | Current recipe defect verified; historical impact not proven without code identity |
| Top-k index graph may include zero activations | Probe checks show zero selected values in all measured codes | Not observed on this held-out panel; does not certify the missing training buffer |
| Formal SAE snapshots present, no fallback in12 refresh records | R/dynamic/run2; original source_audit | Component-merge fallback is not an evidenced explanation for these SAE results |
| GMM teacher parameter snapshots absent from expected saved-state path | Current save code and inventory | Historical changing-GMM teacher replay not completed; no fabricated reconstruction |

A small stored t0 discrepancy may be numerical/pipeline related, but its exact historical cause was **not** identified. Do not call it proven harmless roundoff. Unified replay versus original preanswer shards also differs (static relative-L2 around1.5%, dynamic below0.1% in measured rows); the replay cohort uses fixed sequence shapes and the same runtime across conditions. Inspect O/replay_progress.json for every value. Compare relative effects within each coherent readout, not by splicing old/new outputs.

## 3. Computation and aggregation

### Fixed geometrical ruler

Normalize each nonzero h to u in float64. All audited h are finite/nonzero. For each split, source-balanced weights are `w_i=1/(8 n_source)`. Fit K-means and diagonal GMM at common task_u t0 separately per training seed/split; fix those members across all arms and times. Use weighted cluster mass/centres and global centre. Compute W,B,B/W and enforce `W+B=sum(w||u||²)-||sum(wu)||²` to1e-10. Old cluster-equal versions remain separate columns. GMM solver noise uses the prior float32 normalization/n_init1 definition, explicitly separate from the float64 corrected geometric ruler. A solver precision difference must not be described as identical labels.

Relationship RMS is the root source-weighted squared off-diagonal difference of pairwise cosine matrices, normalized by `1-sum(w²)`. MAD retains the original unweighted all-pairs definition. Direct same-time arm differences are saved separately from differences of distances to t0. The best weighted affine fit `C_t-C_0 ≈ a(C_0-mean C_0)+b` describes only43.64–46.06% of squared task_u development drift; this is a descriptive fit, not a semantic/causal mechanism. Ten-neighbor retention is87.71–88.36%. Residual relational changes remain and cannot be dismissed as a pure common rotation or a uniform shift.

Noise tables compare each time pair with both endpoint-specific same-h repeated-fit distributions. For0→512, only K-means seed43 narrowly exceeds both endpoint observed maxima (0.031117 vs0.030872/0.005112); other seed/method pairs do not. Five solver seeds yield an empirical range, not a formal significance threshold. Do not state that every point lies inside noise or that clusters are unchanged.

### Fixed held-out token panel and dictionaries

Before inference, select at most32 development records/source by SHA256(`0911-sae-probe|record_id`); retain all smaller sources. Result:247 records. For each, take at most8 evenly spaced valid answer-prediction positions including first/last:1247 total. Equal source→equal record→equal selected-position weighting. Owners, positions, content hashes and decoded context are in O/probe_manifest.json. No selected development record enters SAE fitting. Test is used only for geometry, and both existing splits are historically reused, not new confirmatory data.

Top32 positive SAE values and indices are stored sparsely. Group q normalizes only activation mass assigned to nonnegative group IDs; zero assigned mass is uncovered. Coverage is100% on this probe, but retained mass for fixed D0/G0 drops from0.8312 at0 to0.7964 at512; refreshed D/G retains0.9996. Coverage and mass retention are different checks. Reconstruction is weighted MSE divided by weighted **per-coordinate centred variance**, not the earlier flattened training-buffer variance metric. The numbers are not interchangeable with pilot reconstruction values.

For each refreshed dictionary, compare old/new H × old/new (D,G). Then on the same current H swap encoder D and map G independently. Comparison uses cosine(q_i,q_j), invariant to a global group-label permutation. Interaction `C11-C10-C01+C00` is preserved; RMS terms do not add as causal contribution percentages. A common-support robustness check sets both maps to unassigned outside their shared assigned feature IDs; all four combinations have nonzero assigned mass at every probe position. Regrouping exceeds encoder-only change in12/12 windows, ratio2.44–9.87 (tables/grouping_common_support.csv; O/grouping_common_support_receipt.json). This excludes newly covered feature IDs as a sufficient explanation of the ordering. Warm-start feature IDs are retained but do not guarantee semantic identity: final decoder-ID cosine medians are0.9565–0.9583, fifth percentiles0.6547–0.6575.

For the static trained arm, “changing” rows mean **counterfactual application of the paired dynamic arm's dictionary**, not a teacher actually used during static training. For t512 the latest dictionary is the saved t256 dictionary.

### Router/content analysis

Exclude within-record pairs and normalize product weights. At refresh r, hold H_r fixed to measure the teacher-function change; compare it with `-||p_i-p_j||²` change from r to the next sampled checkpoint, and separately with actual top-1 same-expert change. Save direct/excess-over-static correlations and top-quartile response fractions. Windows have different lengths, so no rate comparison is licensed. No pairwise-iid confidence interval or universal uptake/failure threshold is asserted.

The router's weighted structural gradient is nonzero in formal histories, so the auxiliary guidance is operationally present. In final32-update windows the structural/task router-gradient norm ratio is0.035–0.072 across dynamic seeds. On held-out final positions, balance bias changes the native argmax on15.38–22.21%. These are candidate pressure/dispatch constraints, not proof of why responses differ; gradient direction and functional utility remain untested. Source and coarse next-token-type NMI are descriptive, unweighted, confounded by source/position, not semantic ground truth.

## 4. Evidence lineage and bounded findings

| Finding | Raw inputs | Producer → curated table | Aggregation / inference |
|---|---|---|---|
| W rises4.19–5.13%, B rises10.97–12.55% by method |504 authenticated original shards | geometry_audit.py → decisive_geometry.csv / geometry.csv | Mean of3 seed-wise changes, development; test same directions; not semantic labels |
| Fixed dictionary top32 retention72.07%; q RMS0.0534 vs refreshed0.3527 |36 replay shards, D0 and12 snapshots | replay_sae.py + sae_analysis.py → sae_metrics.csv | Fixed247-record cohort; source/record/position weights |
| On same h, regrouping > encoder change in12/12 windows,2.45–9.90× | Fixed H_r, old/new encoders and maps | grouping_decomposition.py → grouping_decomposition.csv |12 dependent descriptive windows; interaction retained |
| Reconstruction0.2252→0.3374 fixed vs0.1078 refreshed | Same probe h and reconstructions | sae_analysis.py → sae_metrics.csv | Weighted centred-variance definition; better reconstruction does not establish semantic correctness |
| Teacher/next-probability correlations−0.128…+0.160, seed reversals | Same cross-record pair teacher changes and next-checkpoint p | sae_analysis.py → route_response.csv | Observational; cannot conclude complete lack of guidance |
| Format/position examples constrain semantic naming | tokenized source data, fixed selected positions and q | content_audit.py + group_examples.json | Rule-selected positive/counterexamples; no human semantic labels |

The data reject the measured **geometric tightening prediction** on this panel. They support a narrower diagnosis: the largest observed teacher-relation change resides in the feature-to-group readout, while dictionary refitting helps reconstruct h. They do **not** establish a causal explanation for all h drift, semantics of the groups, downstream improvement, or superiority over SVD/PCA. No “SAE is ineffective” conclusion is warranted.

## 5. Failure, omissions, and next decision

No audited shard failed the hash/record alignment checks; no new training occurred. Material limitations are historical dynamic-code identity, old cross-pipeline t0 mismatch, unavailable original mixed-step buffers/GMM snapshots, unmeasured same-h repeated SAE-fitting noise, and absent independent semantic/function/data-efficiency tests. The optional six repeated SAE fits were not run: direct fixed-input readout swaps already locate the observed difference, but cannot adjudicate fitting noise versus semantic adaptation. Full-matrix parent E21 finalization is not claimed.

**AI proposed next decision:** assess whether refreshed groups are stable and semantically meaningful enough to use as supervision before new paired training. Keep h/encoder fixed for group repeatability, use fixed examples/pairs for independent semantic judgment, and stop adaptive-grouping claims if either fails. Researcher confirmation is required for mechanism judgment and new scope; the existing Focus/Anchor scientific state remains unchanged.

## 6. Reproduction and artifact map

From E, activate `source runtime.sh`. Run scripts under O in this dependency order:

1. `geometry_audit.py --seed 17|29|43` and `noise_audit.py --seed 17|29|43` (separate seed invocations).
2. `replay_sae.py`, then `sae_analysis.py`, `grouping_decomposition.py`, `grouping_common_support.py`, `content_audit.py`.
3. `integrity_audit.py`, `implementation_checks.py`, `replay_parity.py`, `figures.py`.

CPU stages cap BLAS threads; GPU stages use one local device. Inputs/outputs/hashes are recorded in O/input_manifest.json, integrity_receipt.json, probe_manifest.json, stage receipts and figures/figure_manifest.json. Main readout scripts never modify existing fm/dynamic code or R. Do not treat the scripts as a main-training launcher. Raw token contexts, sparse codes and unfiltered logs stay in O; this directory holds only the evidence ledger, curated tables and figures. The date reading copy records identical figure SHA256 values in its SOURCES.md.

Reading aids: [Chinese four-part report](../../../../../../../../daily_research_reports/backup/2026/09/0911/0911_minimal_followup/meeting_report_cn.md), [systematically selected text examples](../../../../../research_notes/sae_representation/20260911/0911_minimal_followup/examples_cn.md).

Equal32-update local relation drift confirms the slowdown descriptively: task_u development,32→64 RMS 0.01554–0.01652, versus480→512 0.000116–0.000164. This uses pair matrices at both interval endpoints, not subtraction of distances to t0. The warmup/cosine schedule is a candidate explanation, not a measured causal attribution; no constant-rate matched run was performed.

Final proportional verification: O/validation_receipt.json PASS (35 local links, expected table counts, exact figure/table copies, covered common-support probes, replay parity, group-permutation relation error2.22e-16). Repository check reports True with zero errors; existing advisory categories concern same-problem work, incomplete older execution receipts, older figures without source manifests, and stale derived navigation/mirrors. Figure reading copies used by the report live in `daily_research_reports/0911/figures/0911_minimal_*`; that date directory owns their SOURCES.md.


## 7. Follow-up: fixed-input grouping and masked text audit

### Scope and relation to earlier results

The researcher explicitly requested the proposed repeatability and semantic analysis, followed by a plain-language explanation and a return to the advisor's question. This authorizes local bounded grouping/replay, not new model training or a scientific-state transition. This section supplements the earlier observations; the next-decision wording in Section5 is superseded by the narrower decision at the end of this section. Computation is complete; AI mechanism interpretation remains unconfirmed.

Execution subdirectory P: `E/audits/0911_minimal_followup/group_stability`. Before extraction, P/plan.json fixed four states (common initial state using seed17, then each dynamic seed17/29/43 at256), five solver seeds17/29/43/101/211, five record-bootstrap seeds101/211/307/401/503, and the masked-pair rule. `prepare.py` chose at most128 train records/source by a fixed hash and at most32 evenly spaced answer-prediction positions/record. Result:1010 records,16341 positions. The same raw records/positions were used across states; per-state0.999 norm trimming left16324 positions each. Thus raw panels match, while trimmed membership can differ slightly. All top32 values were positive. The247-record/1247-position development probe is record- and content-hash-disjoint from fitting records.

There were **zero** main-model/SAE optimizer updates. Four forward-only model/encoder extractions took110.50 seconds. `repeat.py` built24 graphs and40 partitions in98.16 seconds; all40 were connected, no fallback, and all held-out readouts had full assigned-mass coverage. It used the actual current fm.grouping code unchanged: positive phi top50 symmetrized affinity and component-aware spectral partition with eight groups. Atom counts ranged9732–15506. For fixed-data repeats, both the eigensolver start and final K-means seed changed. Record bootstraps resampled whole records within sources, retaining all their selected positions; five draws are empirical sensitivity checks, not a calibrated confidence interval or original-training noise estimate.

### Direct repeatability results

All relation metrics compare cosine matrices of group-mass vectors on the same held-out h/encoder and use source→record→position weights, excluding within-record pairs. A global group-label permutation leaves this quantity unchanged. Hard argmax adjusted Rand is also recorded, but does not replace the soft relation metric. Changed feature support is reported through full coverage; no claim says mass retention is identical.

| Fixed state | Same-graph solver pair RMS range (10 pairs) | Record-bootstrap pair RMS range (10 pairs) | Saved G0 vs G256 on same current encoder | Fresh-panel G0 vs G256 on same current encoder |
|---|---|---|---|---|
| initial seed17 |0.00595–0.09017|0.08987–0.16949|not applicable|not applicable|
| seed17 at256 |0.00043–0.00211|0.06816–0.12157|0.36850|0.21606|
| seed29 at256 |0–0.00253|0.08801–0.26677|0.34170|0.22516|
| seed43 at256 |0–0.00391|0.07308–0.12248|0.28339|0.19180|

Source: P/repeat_metrics.csv and repeat_summary.csv, curated under tables/group_stability. The later identical-graph partitions are highly repeatable; initial partitions are less stable. Record composition affects readout even with a frozen encoder. All three saved-map endpoint contrasts exceed the corresponding observed bootstrap pair maxima, but old maps and new graphs have different fitting units/support/sample histories. It is invalid to call this a significance test or claim that all historical change is noise. Fresh initial versus saved initial map already gives0.3040 with unchanged initial h/encoder; this localizes an additional readout-construction discrepancy, not a proven cause such as data-domain shift.

### Post-discovery co-occurrence-unit guard

Following old group artifact lineage revealed a material mismatch, so P/unit_guard_scope.json recorded an additional in-scope fixed-input guard before its computation. The old groups.pt points to an exact discovery-cache manifest; the linked segment-incidence matrix hash matches. It has23520 rows, each representing a segment of at most256 tokens, and row positive-feature count median1105 (maximum3018), rather than at most32 per token. Saved configuration specifies segment_length256 and min_support32. Current graph.py matches the old manifest hash; current analysis.py/cache.py do not, so do not claim every old source is identical. The group payload records the E20-A1 cache-reuse identity. The current dynamic refresh source builds rows per answer position and retains every nonconstant observed feature. Its historical source hash is missing, as recorded earlier.

`unit_audit.py` holds all actual sparse activations and eligible feature IDs fixed, then compares each token as a binary row with the union of sampled positions inside each record's original256-position segment. Both use the same current phi graph, positive/nonconstant common support and seed17/eight groups. There are16324 token rows and1089 sampled-segment rows per state. It is not a replay of every original segment token or its min_support32 policy. Four contrasts/eight graphs completed in32.58 seconds, all connected and fully covering the evaluation probe.

| State | Unit-only teacher-relation RMS |
|---|---|
| initial seed17 |0.35278|
| seed17 at256 |0.19091|
| seed29 at256 |0.32997|
| seed43 at256 |0.29543|

Source: tables/group_stability/unit_comparison.csv; P/unit_lineage.json, old_incidence_receipt.json and unit_receipt.json. This directly shows that redefining co-occurrence can change the teacher substantially without any model/encoder change. It does not quantify how much of the actual historical refresh effect arose from that difference. “Appeared somewhere in the same passage” and “active at the same prediction position” are different constructs; neither is universally the correct semantic construct.

### Masked text-pair audit

P/blind_pairs.py selected48 pairs from the existing development probe at256. For each training seed and each of four strata (gain, loss, persistent relatively high, persistent relatively low), two within-source and two cross-source pairs were selected. Both members share coarse next-token type and first-versus-later answer status. Candidate gain/loss tails and persistent-score tails are fixed top10% within each matched stratum; “persistent” uses below-median absolute change. Hash order chooses pairs, no record pair repeats, and any record appears at most4 times. Therefore “low” means relative within a stratum, sometimes still numerically high, and the panel is not representative of population prevalence.

The comparison uses the **same h and current encoder** with G0 versus saved G256. `blind_pair_sheet.json` exposed only prompt/context/next-token text and anonymous pair IDs. The one Codex annotator already knew the project and earlier examples, but did not read the pair key (seed/stratum/similarities) until all48 labels and reasons were saved and SHA-locked in annotation_lock.json at2026-09-11T04:28:52Z. Labels distinguish topic0/1/2 (different/broad same/specific same), operation0/1/2 (different/general family/same concrete operation), format0/1 and token role0/1. The decision is content-only AI judgment, **not independent human validation**; no claim of inter-rater reliability or objective semantic truth is made.

| Selected stratum,12 pairs each | Broad-or-specific common topic | Same concrete operation | Same surface format | Same token role |
|---|---|---|---|---|
| gain |9|0|6|8|
| loss |7|1|6|1|
| persistent relatively high |4|0|12|12|
| persistent relatively low |9|0|6|7|

Source: all labels/reasons/keys in tables/group_stability/semantic_pairs.csv, including within/cross-source summaries. These are deliberate-case counts, not accuracy estimates, independent pairs or hypothesis-test outcomes. With only one concrete-operation-positive pair, general semantic-superiority inference is particularly underpowered.

Examples provide narrower counterexamples: P35 trigonometric identity versus moral judgment rises0.572→0.999; both start their answer. P21 two remaining-budget problems drops0.959→0.490 but the sampled positions differ (currency marker versus equation marker). P04 two orbital-period questions stay0.999; P11 complex polynomial expansion versus constrained seating count drops0.885→0.070. Together they show both semantically plausible and role-driven-looking relations; they do not prove all groups are mere format or functionally useless.

### Interpretation, correction and one next decision

The earlier phrase “stop the need-for-dynamic-grouping claim if repeatability or semantic coherence fails” was a proposed evidence boundary, not a measured conclusion or an instruction to abandon the advisor's structural-evolution question. The new later-state repeatability result does not support rejecting grouping as arbitrary solver output. Sampling/unit effects and text counterexamples prevent calling its large changes new semantic classes. Eight fixed groups cannot establish the birth time/number of natural classes, and a pretrained-model fine-tune is not from-scratch emergence. Operationally nonzero structural gradients, meaningful subject grouping, and useful expert specialization remain different claims.

**Corrected AI proposed next decision:** define one content/operation relation under a common co-occurrence unit and observation rule, verify it on independently judged same-operation/different-format versus different-operation/same-format pairs, then trace that relation over training. If only format is supported, narrow the interpretation to format/position structure; do not claim semantic expert formation or that adaptive grouping is necessary. This does not assert that adaptive grouping is useless. The researcher owns the intended semantic granularity and any new training or canonical scientific transition.

### Follow-up artifact lineage

| Stage | Raw inputs | Producer | Curated evidence | Receipt / identity |
|---|---|---|---|---|
| fixed fit-panel replay | authenticated train data, saved model/SAE checkpoints | P/prepare.py | repeat tables depend on saved sparse codes | P/fit_manifest.json; prepare_receipt.json hashes all4 outputs and checkpoints |
| repeat grouping | four fixed code matrices, unchanged fm.grouping | P/repeat.py | tables/group_stability/repeat_metrics.csv, repeat_summary.csv, group_fits.csv | P/repeat_receipt.json; all maps and graphs retained |
| co-occurrence unit | same fixed codes/common IDs, old group/cache identities | P/unit_audit.py | tables/group_stability/unit_comparison.csv | P/unit_guard_scope.json; unit_lineage.json; old_incidence_receipt.json; unit_receipt.json |
| text audit | held-out positions, old/new maps and masked content | P/blind_pairs.py; locked Codex annotations; P/summarize.py | tables/group_stability/semantic_pairs.csv and semantic_summary.csv | P/blind_pair_receipt.json, annotation_lock.json, semantic_receipt.json |
| figure | curated summaries and unit contrasts | P/plot.py | figures/0911_grouping_followup.png/pdf | P/figure_manifest.json; date-local SOURCES.md |

Reproduce from E after `source runtime.sh`: P/prepare.py → P/repeat.py; P/unit_audit.py; P/blind_pairs.py → content-only annotation lock → P/summarize.py → P/plot.py. Do not overwrite the locked labels during reproduction. Raw contexts, graphs, sparse codes and logs remain in P. This is a supplementary audit, not a main-training launcher.

A further comparison boundary: the existing static training arm consumes cached teacher targets. Fixed-D0/G0 applied to current h in this supplement is an offline replay readout, not evidence of a trained fixed-dictionary online-current-h arm. No fixed-current-h-versus-refreshed-current-h matched main-training comparison was added.

Follow-up verification: P/validation_receipt.json PASS checks all expected48 partition maps, four replay output hashes, locked48-pair identities/stratification, all curated tables/figure copies, local links and the hand-computed regrouping example. The group-permutation relation error is2.22e-16. P/repository_check.json reports ok=true, zero errors; advisories concern pre-existing receipts, figure manifests, concurrent problem tasks and stale derived views. No commit, push, publication or scientific state promotion was performed.
