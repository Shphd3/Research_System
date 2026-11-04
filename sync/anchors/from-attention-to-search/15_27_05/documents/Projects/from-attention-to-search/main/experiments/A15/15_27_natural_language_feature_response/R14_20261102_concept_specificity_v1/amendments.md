派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/amendments.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R14_20261102_concept_specificity_v1/amendments.md)；研究修改仍回到原件。

---

# Amendments

Initial v1: no scores opened. Final user revision fixes frequency-group deletion as primary; all spectral conditions retained.

## A1 — pre-output analysis implementation detail
Time: 2026-11-01T16:51:05.886158+00:00
Before inspecting numerical outputs: representative members in six fixed families are selected within each reference frequency group by the mean of |z(xA)-z(xB)| times raw last-decoder norm across both paraphrases, at first-answer position. This is response-change selection, not feature causal attribution. Also show the highest pooled-response member with a small response difference as a counterexample. No new intervention/selection of families or change in primary endpoint. Analysis implementation after initial freeze is hashed on completion; data/config/protocol remain frozen. No scientific result viewed at this amendment.

## A2 — before first scoring, smoke and applied-precision diagnostics
2026-11-01T16:52:47.398446+00:00
No condition outputs exist. Preserve initial run_gpu.py and freeze in audit/. Extend new-task smoke to include prefix-last first-answer position explicitly, in addition to later candidate positions. Save intended vector displacement and actual BF16-entering displacement separately, including zero-after-rounding. No candidate, data, condition, model, threshold or main estimand changes. Effective code hash in current freeze; initial protocol remains unchanged.

## A3 — pre-output diagnostic-case metric
2026-11-01T16:53:51.937438+00:00
Beyond the six fixed evaluation families, diagnostic cases are chosen by family J change under high-frequency deletion versus full: largest loss, largest improvement (smallest signed loss), and smallest absolute change; ties by family name. They are labelled result-selected and cannot replace fixed cases or all-family statistics. All three groups remain primary, this case rule does not select a winning group.

## A4 — model-independent factual clarification before any forwards
2026-11-01T16:58:05.958621+00:00
No smoke or cache exists. Preserve data_v1_pre_correction and freeze_before_A4. Symmetric-matrix paraphrase2 now requires a nonzero off-diagonal pair, excluding the zero-matrix overlap. Replication-enzyme paraphrase2 specifies deoxyribonucleotides, excluding RNA-primer synthesis. Same families/split/conditions/answers/metrics; only these two independently identified cue ambiguities corrected. All affected data rebuilt before GPU access, no scored item chosen by model success. Current manifest is data v1.1; initial protocol and original hashes preserved.

## A5 — complete algebraic alias ledger before any cache
2026-11-01T17:13:34.096984+00:00
Add six explicit full-rank random-control aliases: three retain1024 equal full; three centered-remove1024 equal mean-only. There is no distinct full-rank random subspace; not six new empirical measurements. Unique measured matrix remains167, alias count19. No scoring or primary comparisons change. Original conditions archived.

## A6 — align native decoder GEMM shape before any forward
2026-11-01T17:16:12.574336+00:00
Prior R13 recorded native256-row versus smaller cached-head GEMM BF16 logit differences. Before any new cache/smoke, use fixed256-row norm/head batches (including zero-row padding) instead of64, matching the frozen model full-forward row shape. Same native weights, norm, h, candidates, intervention and metric; no tolerance relaxation. Old code/config archived; current freeze hashes effective code/config. This removes a known avoidable precision rival and increases head batching efficiency. All R14 conditions use this same shape.

## A7 — complete special/padded output mass diagnostics before any forward
2026-11-01T17:18:43.087580+00:00
Add two saved first-position fields: declared special-token probability mass and unassigned/padded output-row mass, separately from non-special frequency and punctuation metrics. This completes original output diagnostics; no change to data, intervention or primary endpoint. No model outputs exist.

## A8 — final name-form audit, before any cache
2026-11-01T17:22:32.187761+00:00
Damped-oscillation first cue used no continuing drive, a stem related to the alternative driven oscillation. Replace by without any subsequent applied force. This removes an unintended target word-form clue. Data1.1, source and exact indices archived; effective data1.2 preserves family/split/answer/condition/position counts. Only this one visible prefix and its four causal candidate sequences changed. No model outcomes available or used.

## A9 — existing local CPU BF16 qualification after unavailable Spot allocation
2026-11-01T17:26:45.537349+00:00
No GPU cache, smoke or score exists. Original5090 job pt-oqno0y4q remainedPending, current visible AEC2 list has only H100/share and debug pools; do not use H100 or another GPU class. Stop only our unallocated job, retain all receipts. Existing workspace has8CPUquota; use2threads. Benchmark256x1024x151936 BF16 native-head GEMM took0.058s after warmup. Adapt run_gpu.py to CPU with same Qwen BF16 weights/native head and the identical A22 post_relu BF16 autocast equation, FP32 parameters, fixed threshold and raw-scale decoder; original class CUDA training guard is replaced by an explicit read-only CPU inference context. No fitting or parameter/buffer change. A new development-only identity/cache/causality/gate/reconstruction smoke must pass before formal CPU scoring. Model/checkpoint/tokenizer/data/basis/groups/metric unchanged. CPU environment is explicitly different from prior5090 measurements; not an independent hardware replication. If smoke fails, no evaluation values are eligible. Resource choice is within authorized existing CPU,0GPUs, no paid resource expansion.

## A10 — complete all-candidate name guard; data1.3
2026-11-01T17:51:29.994570+00:00
The original audit prohibited literal A/B names but omitted U/V. Exhaustive text-only scan found20prefixes in7evaluation families with literal U; no A/B or V match. v1.2 had completed167conditions, but no numerical scores were read to select edits. Preserve all original data, source, raw167conditions, affected caches and terminal receipt under versions/data_v1p2. Replace ALL20literal-name prefixes by operational descriptions; same48families,288prefixes,U/V/A/B answers,2640positions,source definitions,split,frequency groups,basis,conditions and metrics. Regenerate only80affected model sequences and their coefficients; qualify reuse of1072unchanged sequence caches by exact input IDs/indices, original frozen CPU model and parent manifest. Re-encode joint coefficients with same1024padding and require unaffected z and h bit equality. Recompute all167interventions at affected scoring positions, reuse unchanged per-position raw scores only after untouched native replay matches exactly. Reaggregate all family metrics. Old raw outputs remain identifiable v1.2, not mixed into current names/coordinates. No dataset selection based on full-model success, no additional family or classifier. This is a data-contract implementation repair, not positive-result search.

## A11 — repair false high-response counterexample label, existing-cache only
2026-11-01T18:10:37.428555+00:00
After results, review found the sparse member pool median contrast was zero; the selector could return an all-zero inactive member but label it high_response_small_difference_counterexample. Preserve original member CSV. Require pooled response>0 for that original-rule counterexample; if no such member exists, mark NOT_FOUND and do not substitute a new threshold/member rule. Frozen top-two response-difference members unchanged; broad-context responses of those same fixed members provide honest non-exclusivity examples. This fixes casebook eligibility/wording only, not any intervention, family, score, primary effect, CI or figure point. No model forward or classifier.

## A12 — display-only clarity and deprecated length metadata
2026-11-01T18:50:27.091762+00:00
Final figure audit preserves the earlier figure04 under figures/archive/04_means_before_individual_points.png and adds each paraphrase point plus per-paraphrase correct counts to current figure04; family means alone must not hide failures. No score, plotted family mean, group or comparison changes. The immutable input field AB_prefix_token_length_difference was a deprecated clue-only diagnostic, not the scored full-prefix length; an explicitly corrected metadata view and length-diagnostic CSV are supplied, preserving original input bytes and exact model tokens. This field never entered the complete-candidate likelihood, answer-length sensitivity subset, grouping or selection. See audit/length_metadata_erratum.json. No forward or result resampling is required.
