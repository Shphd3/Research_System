# Frequency-priority, co-activation-assisted dispatch: detailed execution record

[Summary](summary.md) · [User Protocol](protocol_cn.md) · [Implementation freeze](design_freeze.json) · [Reasoning audit](reasoning_audit_cn.md) · [Figure explanations](figures_cn.md)

## 1. Question, operation, and claim boundary

This round studies actual dispatch on fixed representations. Does excluding the ten highest TRAIN-frequency routing candidates, grouping features primarily by frequency, and adding a co-activation adjustment improve reception of low targets by their assigned experts and reduce their within-expert frequency gap relative to accompanying head features? Candidate explanations are head-score dominance and grouping conflicts. A competing explanation is that the original mean-over-members score still favors the remaining high-frequency group.

Every expert input retains the original complete representation h. The frozen CrossCoder's gated z, prediction positions, masks, and decoder-amplitude weights remain unchanged. Only candidates, assigned feature lists, and the resulting top-1 choices change. There was no new model forward pass, expert training, gradient update, or GPU task. T10 remains in the actual inputs and evaluation; excluding score candidates does not delete input information.

The observations do not show that these fixed operations solve dispatch. Lower list-frequency dispersion and higher relation reward did not produce broad low-target reception. Formal researcher judgment remains pending discussion. Learning and capacity benefits were not tested. P's missing asset limits P alone, not the factual record of the completed comparisons.

## 2. Authorization, versions, assets, and paths

The researcher explicitly authorized this dispatch analysis, without expert training, and instructed that a branch's missing assets must not block other comparisons. Uploaded Chinese Anchor and Protocol files were preserved verbatim; English files are companion translations. `protocol_frozen.md` is a byte-identical copy of the uploaded Protocol. `design_freeze.json` records implementation choices without changing the main definitions or thresholds. Previous experiments, the original audit, and caches were not overwritten. There was no commit or push.

|Object|Binding|
|---|---|
|Execution root|`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_priority_dispatch/20261018T160918Z`|
|Parent cache|`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/cache/train.pt`, `eval.pt`, and `grouping.json`|
|Completed original audit|`routing_audit_20261018T143950Z` under the parent run; existing checks and the O reference were reused|
|Base model|`/data/share/Qwen3-0.6B-Base`, 28 layers, hidden size 1024; not loaded for a model forward pass this round|
|Dictionary|Final A22 `checkpoint_000999997440.pt`, 14 selected layers, 16,384 features; SHA256 `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`|
|Selected layers|Zero-based blocks 1,3,…,27: model layers 2,4,…,28, residual-post, before the original final normalization|
|Activations|Shared z jointly encoded from the selected layers; frozen TRAIN centering/RMS and threshold 0.051281172782182693, retaining the parent's strict gating comparison; no online current-batch BatchTopK|
|Cached expert input|Only final-layer raw hidden `[N,1024]`; z is stored as CSR at the same positions; this is not joint H|
|TRAIN|130,712 valid positions, 128 contexts of 1024 tokens; global01/local5/shard41, source contexts 8192–8319|
|EVAL|65,402 valid positions, 64 contexts; global01/local2/shard247, cached context IDs 117658–117721, corresponding to source blocks 8192–8255|
|Reliable pool|TRAIN hits≥200, at least 20 contexts, and 0<n<N: 9,615 features, reused exactly|
|L / C|Original TRAIN lower q10 including ties: 964 features / upper q90 including ties: 962 features; these evaluation lists are not routing intervals|

Strict input-access checks and actual input IDs are in `provenance/asset_access.json`. The new analysis asset is `analysis_crosscoder_frequency_priority_dispatch_20261018t160918z`; the scoped strict check is recorded in repository `assets/checks/2026-10-19_frequency_priority_dispatch_20261018T160918Z.json`. Access checks and saved identities do not grant scientific approval.

The TRAIN file is `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_5_of_10_shard_00000041_processed.bin`; EVAL uses `local-shard_2_of_10_shard_00000247_processed.bin` under the same global shard. Original source SHA and position mappings follow the parent manifests; current access, file statistics, and sample labels were separately checked. EVAL had already been viewed, the CrossCoder had seen the broader corpus, and document/near-duplicate independence is unknown. These results are exploratory holdout checks in the same fixed windows.

## 3. Frozen comparison matrix and implementation

|Strategy|Candidates / assigned lists|Held fixed and distinguishable change|Status|
|---|---|---|---|
|O|Original eight linear equal-width groups|Original routes/scores reused as baseline|Complete|
|F|All 9,615 features, eight log10-frequency K-means groups|Frequency organization changes relative to O; score unchanged|Complete|
|T|Exactly T10 excluded; remaining 9,605 regrouped by the same method|The complete operation of head exclusion plus regrouping, relative to F|Complete|
|Tφ|T's candidates and group sizes; relation swaps within a frequency tolerance|Increment from this relation-adjustment algorithm relative to T|Complete|
|R11/R22/R33|T candidates and exactly T's group sizes, randomized membership|Random reference; T and Tφ share these same random lists|Complete|
|P|F lists; re-encoding after removing the first direction of original joint H|Separate geometric branch, not combined with T10 exclusion or φ|NOT RUN: joint H missing|

T10 is `[13964,516,8060,10807,7388,5147,5913,7415,8345,13830]`, selected by decreasing TRAIN p within the reliable pool, with feature ID ascending for ties. Its frequencies range approximately0.984684–0.811593, and it does not intersect L. `T10.json` and `C.json` are separate. Of C's 962 features, 952 remain T candidates; T cannot be described as using only medium/low-frequency features.

F/T use scikit-learn 1.2.0, float64 log10(p), equal feature weights, and KMeans with `init=k-means++`, `algorithm=lloyd`, seed 20261019, n_init=20, max_iter=300, tol=1e−6, and no sample weighting. Groups are relabeled by ascending center. This is a fixed algorithmic reference, not a global-optimum claim. List dispersion D is the mean squared distance of features from their group's log-frequency center.

F group sizes are `[1253,1351,1511,1650,1867,1147,502,334]`; T/Tφ use `[1257,1347,1506,1629,1824,1189,523,330]`. Random memberships use PCG64 seeds 11/22/33, preserving those eight sizes exactly without matching within-group frequencies.

The common parent score is:

\[
s_e(t)=\frac{\sum_{i\in G_e}z_i(t)w_i}{|G_e|},\qquad
w_i=\sum_{\ell=1}^{14}\|D_{\ell i}\|_2.
\]

Here w sums 14 decoder L2 norms; it is an amplitude scale, not functional importance. Inactive members contribute zero and remain in the denominator. There is no inverse-frequency or baseline calibration. FP64 sparse accumulation is converted to FP32 before maximum-score selection. The parent stateless hash resolves ties/all-zero cases. New strategies share hash seed 20261019; random seeds change membership alone. O retains original seed 20261018. All strategies actually had zero ties and zero all-zero inputs; fallback did not create coverage.

O's complete block counts and 64 sampled scores exactly reproduced the reference. Existing checks were reused without repeating full forward initialization. Every strategy uses its own assigned lists and actual routes for counts.

## 4. Eligible relation edges, reweighting, and swaps

Candidates came only from original D mutual-top10 φ edges in `analysis/feature_frequency/20261015T143300Z/main/edges_D.csv`. Community co-membership and the D/V matched intersection were not substitutes. The generator selects candidates using D counts and coverage alone. Its source is global01/local0/shard1, different from current EVAL local2/shard247. Dictionary SHA, feature IDs, and gating match this round. Source lines and hashes are in `provenance/branch_assets.json`; candidate-file SHA is `006d028e27d4d9ac40d81c24ba68f871c6c8eadbbbf1520e76959dba1bc5b3a0`.

Restricting the original 34,757 rows to endpoints in T, deduplicating undirected pairs, and removing self-edges left 16,763 pairs. Only these pairs were reweighted from current TRAIN binary hits. Requiring co-hits≥10, φ>0, and both marginal probabilities strictly within(0,1) left 16,740 edges. No full 16k² matrix was computed.

\[
\phi_{ij}=\frac{p_{ij}-p_ip_j}{\sqrt{p_i(1-p_i)p_j(1-p_j)}},\quad
\widetilde w_{ij}=\frac{\phi_{ij}}{\sqrt{d_i d_j}},\quad d_i=\sum_j\phi_{ij}.
\]

Degrees d are computed once on the fixed TRAIN graph and do not change with grouping. Each undirected edge counts once; isolated nodes receive no relation reward. Starting from T, features i are visited in ID order. Target groups must contain positive-edge neighbors. Each target group contributes the five current members j nearest to i in log frequency, with ID tie-breaking. A swap must retain total D≤1.05D_T and increase the relation objective by more than 1e−12. The largest legal increase wins; remaining ties use target-group number and j's ID. Centers/objectives update after each swap while group sizes stay fixed. Independent round checks verify conservation and floating-point error; the 5% bound was never relaxed.

There were 489 accepted swaps,175 final changed members, and termination in round 5 when no legal improvement remained. D rose from 0.006344674375 to 0.006661886700(+4.99966%); within-group normalized edge weight rose from 1098.951253 to 1221.536241. Swaps and final changed members differ because a feature may participate repeatedly. This local heuristic does not guarantee optimality.

EVAL was read only after membership froze. Of the fixed 16,740 edges, 16,605 retained positive φ, 15,918 retained both positive φ and co-hits≥10, and 135 were non-positive. No edges or memberships were revised from that check. Sign retention does not establish document independence, semantics, or learning value.

## 5. Metrics and zero/NA semantics

N denotes valid prediction positions; n_i original hits of feature i; N_e inputs received by expert e; and n_ei positions that both contain i and reach e. Main evaluation always uses original x=1[z>0], including T10. Re-encoded events do not replace evaluation targets.

\[
p_i=n_i/N,\quad a_{ei}=n_{ei}/n_i,\quad
\ell_e=N_e/N,\quad q_{ei}=n_{ei}/N_e,\quad q_{ei}/p_i=a_{ei}/\ell_e.
\]

Assigned expert g(i) comes from membership. Excluded T10 has owner=−1 and is masked before indexing; −1 cannot index expert 7 or count as target reception failure. Actual T10 q is retained for every expert. When n_i=0, a is unestimable. When N_e=0, q and enrichment are NA. When an expert has inputs but never receives the target, a/q are zero. Numerators and denominators are saved. Checks verify Σ_eN_e=N, Σ_en_ei=n_i, and q=p×a/ℓ.

Each expert has input/context counts, list size, and actual distinct reliable/low-feature counts. The main “seen” threshold n_ei≥1 is accompanied by n_ei≥5. Type counts depend on input volume and are not capacity. The future training-readiness marker of 200 positions/20 contexts does not stop the current analysis.

Head-frequency advantage is:

\[
B_i=\frac1{10}\sum_{c\in T10}\max\{0,\log_{10}(q_{ec}/q_{ei})\},\qquad e=g(i).
\]

A zero head frequency contributes zero when target q is positive. A zero target frequency with any positive head frequency gives B=∞. Empty experts give NA. If both the target and all head frequencies are zero, B is not comparable while zero-reception failure remains recorded. Rates B≤1/B≤2 always use all 964 targets as denominator; NA/∞ do not pass. These are predetermined descriptive thresholds. Finite-only means do not replace complete state counts. Paired B comparisons report the common finite subset and newly/lost finite targets to expose survivor selection.

## 6. Observations: tighter lists still feed the high-frequency group

List D is 0.186338658 for O, 0.006677074 for F, and 0.006344674 for T. These describe construction; F/T also use different candidate sets. A lower D is not itself successful dispatch.

|Strategy|TRAIN N_e0 / N_e7|EVAL N_e0 / N_e7|EVAL low targets with zero reception|EVAL equal-feature mean low a|
|---|---|---|---:|---:|
|O|0 /119,843(other groups also receive inputs)|0 /58,123(other groups also receive inputs)|964|0%|
|F|0 /130,712|0 /65,402|964|0%|
|T|6 /130,706|1 /65,401|960|0.00230675%|
|Tφ|6 /130,706|1 /65,401|960|0.00230675%|

F has seven empty experts; T/Tφ have six. T has eight nonzero-reception low targets on TRAIN and only four on EVAL. EVAL targets 601/5412/15067/15519 each receive one hit, all from the same expert0 input whose expert denominator is also one. q=1 and B=0 are one-position empirical proportions, not stable or broad low-frequency enrichment. These real small counts are retained without exclusion or a success claim.

T's EVAL B states are 4 finite / 960∞; Tφ has 4 finite / 958∞ / 2NA. Low targets 1289/10262 moved from assigned e0 to empty e1. Their original a was already zero and remains zero. q/B become unestimable: they did not newly lose positive reception, and fewer infinite values do not mean improvement. Both fixed-denominator B≤1 and B≤2 remain 4/964=0.41494%.

## 7. Relation construction did not add actual dispatch value

Tφ and T have identical routes at every TRAIN and EVAL position. Consequently, their complete expert inputs, original-feature counts, and actual per-expert q are identical. The 175 changed assignments can still change owner-specific metrics; not every metric is identical.

No incremental actual-dispatch value was observed for this φ-adjustment algorithm under the original score. A higher edge objective cannot be interpreted as co-activation helping low targets obtain inputs. Conversely, this local-heuristic negative result does not reject all co-activation, semantic grouping, or alternative scores. Mostly positive EVAL edge signs and unchanged actual routing are distinct observations.

## 8. Random references increase reception without resolving the head gap

The three random lists use T/Tφ's candidates and group sizes with the same score. They are neither fully frequency-matched mechanism controls nor theoretically optimal assignments. EVAL results are:

|Membership seed|Equal-feature mean a|Median a|Zero-reception targets|B≤1(all 964)|B≤2(all 964)|
|---|---:|---:|---:|---:|---:|
|11|16.6280%|12.2200%|31|0%|4.5643%|
|22|17.4438%|14.0560%|20|0%|5.7054%|
|33|17.7257%|14.9477%|26|0%|4.4606%|

All eight experts are nonempty, but most low targets still have B>2 or B=∞. More balanced reception or more observed feature types does not establish better knowledge learning. These seeds probe membership sensitivity, not three independent training replications. Medians above are checked against the saved `summary_eval_R22.json` and `summary_eval_R33.json` values0.1405604338842975 and0.14947716507283937.

## 9. Costs, paired intervals, and complete actual frequency profiles

Complete owner metrics and full16,384×8 actual counts/q remain execution-side. All 9,615 reliable features, including T10, enter the q profiles; only list p is not enough. Costs use fixed original TRAIN log-frequency quintile bands, plus L/C/T10/other subsets. Named subsets may overlap and cannot be summed as disjoint totals.

For F→T on EVAL, L has 4 improvements, 0 reductions, 960 unchanged. Ten of C's 962 features become unassigned and are excluded from owner comparisons; the remaining 952 have 6 improvements, 6 reductions, 940 unchanged. The other 7,689 features have 3 improvements and 0 reductions. For T→Tφ, every L a is unchanged; among 952 paired C features, one improves and one declines. Changes induced by reassignment do not imply changes to actual expert inputs. Concretely, C feature 7228 moves from assigned expert 7 to 6 and its assigned reception falls from a=1 to a=0; feature 15643 moves from 6 to 7 and rises from a=0 to a=1, on both splits. Their changes cancel in the mean but do not erase individual costs. These are assigned-list changes, not transfers of actual inputs.

The 200 bootstrap replicates use original context blocks and seed 20261019. They provide descriptive intervals only. F→T EVAL macro-a difference is 0.0000230675 as a fraction, with 2.5%–97.5% range[0,0.0000970125]. In percentage points: 0.00230675, range[0,0.00970125]. T→Tφ macro-a and fixed-denominator B≤2 differences are zero with intervals[0,0]. These reflect identical routes and these specific metrics, not a population test that relations are universally ineffective.

If resampling gives a feature n_i=0, its a remains NA; macro a uses nanmean over estimable features. The zero-reception numerator requires n_i>0 and zero received hits. B-threshold denominators remain964. Not every resample necessarily defines all 964 a values. Context blocks are not verified independent documents, and EVAL was already viewed. There is no strict confirmation or significance claim.

Full costs, per-feature changes, estimable-set changes, and intervals are in `reception_cost_bands.csv`, execution-side `paired_feature_changes.csv`, `paired_comparison.csv`, and `paired_bootstrap.csv`.

## 10. Natural-text and figure selection: scope and checks

Figure A is a schematic, not a measured mechanism. Each strategy's figure B has two pages of four experts, showing actually received features and then real text positions. Empty experts remain visible. Only the main feature cards hide T10; the accompanying q strip and full frequency profile retain it.

Per expert, deterministic feature selection takes two highest-p actual-hit non-T10 features, two lowest-p features with n_ei≥5, and two assigned L targets with the largest support. The union is deduplicated without backfilling and shown in descending p order, at most six features. The complete untruncated actual-feature list contains 286,341 strategy/expert/feature rows. An expert without inputs has no received-text example, even if its assigned list contains targets.

Each selected feature gets one EVAL position that both reaches the expert and activates the feature, sampled with seed 20261019 and a preference for contexts not yet shown on that expert's page. There are 184 cards. Document boundaries are unknown; snippets stay within one contiguous cached context and never splice files/windows. Figures show previous2/current/following2 tokens; following tokens are post-hoc reading aids, never routing inputs. Complete JSON contains raw token pieces, IDs, the full visible prefix, source/context/position, and next-token label. Current positions, received-hit conditions, labels, and boundaries were checked for all 184 examples. Right context did not select examples.

Display-only string shortening uses an explicit ellipsis and points to complete JSON without changing selection/data. T10 strip order is fixed and listed in `figures_cn.md`. p is TRAIN global frequency; q is EVAL within-expert frequency. Neither is a decoder-amplitude share.

The environment lacks transformers/tokenizers. Decoding existing token IDs only requires the frozen `tokenizer.json` ByteLevel mapping; no installation, download, or model forward was needed. Before generating new text, the decoder exactly matched 36 saved reference strings: current token, next token, and full prefix for 12 original audit cards generated with HuggingFace Qwen2TokenizerFast. See `provenance/text_decoder_receipt.json`. This is an engineering read-path adaptation, not new tokenization or a routing-input change.

## 11. P branch: exact missing asset and rejected substitutes

P requires the original preprocessed joint input at these positions, `[N,14,1024]→[N,14336]`, preserving layer order. It would not additionally subtract the current window's mean; original frozen TRAIN preprocessing would remain. Only then could its leading right singular direction be estimated, followed by original-threshold re-encoding and reconstruction checks.

The bounded search covered relevant representation registry entries, parent caches and writer code, previous relation-learning `data/data_eval512` interfaces, and φ input manifests. The parent writer saves only `raw[:,-1,:]`. Existing hidden arrays have shapes`[130712,1024]`/`[65402,1024]`; `model_input_norm` contains final-layer side-branch parameters, while phase1 stores sparse z. No same-position original joint H was found in these inspected owners. This is not a claim of absence across all storage.

The minimum missing asset is joint H with layer order and position manifest. Final-layer h and zD are not substitutes; a different PCA object was not used. No model activations were re-extracted. Projection, re-encoding, energy, reconstruction error, and x' changes are all NOT RUN. There is no fabricated figure E. This does not negate completed comparisons.

## 12. Completion, actual cost, and stopping point

Completed: TRAIN/EVAL statistics for O/F/T/Tφ and three random lists(7 strategies × 2 splits), fixed-condition bootstrap, group/expert/feature tables, complete actual-feature lists, scores/routes, 184 cards, and 19 figures A/B/C/D in PNG/SVG/PDF. P alone is NOT RUN; it neither replaces nor cancels other comparisons. B comprises 14 pages; C has three pages with separate quantities, not new scientific conditions.

Local resources stayed within the existing eight-core quota, aggregate RSS cap 16 GiB, and new-disk cap 2 GiB. No GPU or paid task was added. Main statistics took 36.22 seconds initially plus 11.37 seconds for Tφ/final tables(total 47.59 seconds); relation reweighting/swaps took 8.85 seconds; initial text/figures took 25.99 seconds. Their process peaks were approximately 1.10 / 0.99 / 1.10 GiB. Other checks, writing, and display-only fixes are recorded separately. Tasks overlapped, so summing them does not give end-to-end wall time. Final time, disk, and monitoring scope are in `provenance/completion_receipt.json` and `manifest.json`.

Execution scripts `core_dispatch.py`, `relation_adjust.py`, `visual_dispatch.py`, and the bounded display-fix renderer have recorded hashes. `provenance/core_receipt.json`, `relation_receipt.json`, and `visual_receipt.json` retain results/checks. Label checks and actual visual reviews have separate receipts; code/math checks are not presented as render verification.

Scientific parameters did not change after results: no expanded deletion count, tolerance/PCA-rank scan, or score calibration. The reasoning audit, source bindings, and selected-evidence payload manifest accompany project records; long tables/routes/caches remain execution-side. Models were not copied into research documents. No commit/push was performed.

The global navigation checker still reports two preexisting unrelated issues: a missing NTP project README and an untracked diffusion literature record; neither was changed. The current delivery passed checks of 20 documents, 136 local reading links and selected evidence hashes. These checks do not establish scientific approval.

## 13. Updated understanding, rivals, and one next question

The initial intuition was that frequency-near lists, removal of a few head features, and co-activation assistance might suffice to direct low-frequency inputs to their assigned experts. We now know more specifically that the original group-mean score gives complete concentration for F, near-complete concentration for T, and unchanged routing after Tφ's list-relation optimization. “Better organized lists suffice” was not supported in this implementation.

This does not reject pairing frequency/co-activation organization with a different score. Frequency, amplitude, and semantics were not separately identified as mechanisms. Remaining high-frequency score winners, comparability of group-mean scales, genuine co-activation conflicts, and future learning utility remain rivals or untested bridges. Random references increase reception without eliminating B gaps, showing that neither load nor reception alone settles the objective.

**AI recommendation: retain the current lists and inputs, first define whether scores should compare raw amplitude or response relative to each group's TRAIN baseline, then preregister one finite calibration comparison.** Required reception, head-frequency gaps, and costs to other targets must be considered together. Formula, thresholds, and resources remain researcher decisions. This round does not run calibration, delete more features, or enter learning/capacity experiments. Final researcher interpretation and next-stage approval remain pending.
