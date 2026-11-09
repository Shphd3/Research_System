# R13 native spectral decoding protocol

## 0. Identity and authorization
A15_27_05; R13_20261101_native_spectral_decoding. User explicitly authorized frozen-model forward/analysis, at most two existing authorized RTX5090 Spot GPUs, no formal training resources or new conversations. Runnable after CPU audit; full analysis gated by embedded GPU smoke. No new training/classifier, commit, push or publication.

## 1. Purpose
Measure cumulative recovery of next-token distributions under the fixed native output interface; distinguish accuracy, fidelity, corpus commonness and semantic reading.
## 2. Hypotheses and rivals
See owning round anchor sections 2–3. Support requires consistent paired evidence beyond matched-rank references and counterexamples; no expected order is also valid. Semantic order requires independent text validation; frequency alone cannot decide it.
## 3. Models and assets
Exact R12 official Qwen3-0.6B-Base checkpoint (model.safetensors SHA256 cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba), tokenizer, cached raw BF16-derived h27. Hidden size 1024, 28 blocks, tied embeddings/output weight. Original final RMSNorm eps 1e-6 must precede lm_head. Registry checks and exact paths/hashes in manifest.
## 4. Measurement interface
Block index27 output before final global norm, position t after reading token x_t, predicts x_(t+1). No BOS/chat template. Original cache forward shape1x256 mask192; causal-prefix smoke tests verify no future influence. Native BF16 model, SDPA, eval/inference_mode, requires_grad false. Projections accumulated FP64 on CPU then cast BF16; no scale/temperature adjustment in main analysis.
## 5. Data and splits
Primary: all37 R12 H/the documents, frozen original position; exploratory reuse. Position191 next token must be verified from pinned cleaned source with exact first192 IDs. Supplemental: all180 R11 H documents across math/biology/physics, four distinct positions sampled without replacement per document from32..190 with seed20261101; exclude primary target position and five named showcase documents. This yields175 documents/700 positions, outside R04 PCA fitting documents. Preserve domain/source/template fields. Panels never pooled. No output-based position selection.
## 6. Spectrum
Reuse R12 exact basis/mean/band matrices from R10/R04, single pooled centering, 9600 discovery positions. Audit all eigenvalues, rank, orthogonality and gaps. No fitting on evaluation or new classifier/PCA fitting. All-PC is not assumed identity; direct identity separately tested.
## 7. Conditions
Identity; mean-only; nested head k=1,4,16,64,128,256,512,768,1024. R12 head64(1..64),middle64(481..544),tail64(961..1024),head64+middle64,head64+tail64,head128. Exact R12 random1031/1032/1033 64d reference spaces. Three128d controls head64+new random64 orthogonal to head, seeds1034/1035/1036. Duplicate head64/head128 aliases not rerun. All share mu.
## 8. Metrics
Per paired position: true successor NLL nats; KL(full||projected) nats; output entropy nats; full-top1 agreement; fraction of full top10 recovered in condition top10; true target probability/rank; condition top1 accuracy; raw h norm; centered retained energy. TRAIN-covariance retained variance per condition. Store top20 ID/fragments/probability plus full top20 and target rank for all conditions/positions.
## 9. Independent frequency reference
First4,194,304 uint32 tokens from pinned DCLM global01 first training bin; SHA256 of selected bytes, tokenizer mapping and decoded pilot recorded. Laplace alpha0.5 over all non-special vocabulary IDs; special/padding IDs handled separately with output mass reported, never assigned lexical commonness. Report conditional non-special expected log frequency and mass in reference most-common1%, next9%, next40%, remaining50% of non-special IDs. Bins have inherited incomplete raw tokenizer provenance: retain this limitation and audit readable pilot; no eval-derived counts.
## 10. Fixed cases and interpretation
Fixed named R12 cases282/292/262/297/090 plus one seeded ordinary primary document per domain excluding named cases. Fixed examples distinguished from posthoc greatest NLL gain/loss. Read raw token fragments in context; do not call subwords full words. Any content/format interpretation proposed from fixed cases is checked on other documents without renaming by results. No categorical semantic order will be inferred from frequency alone.
## 11. Statistical analysis
Mean metrics first average within document, then across documents. Paired document bootstrap2000 replicates seed20261102,95% percentile intervals; supplemental positions are not independent docs. Descriptive multiple conditions, no significance fishing. Preserve full paired per-position and per-document tables.
## 12. Numerical gates
Check model/tokenizer hashes, basis full rank/orthogonality, source target shift, mask and hook replay. Identity through exact same norm/head path should produce identical logits/NLL. Full-PC reconstruction error <=1e-8 raw FP64, BF16 cast equality; if violated stop. Cross-runtime cache replay compare h normalized L2<=0.02 and NLL abs<=0.05, logits max<=0.5; report exact errors and BF16 limits. Prefix/full causal replay same limits. Exceeding gate stops main run for diagnosis, not tolerance widening. Confirm cached h is finite and target position unpadded.
## 13. Sensitivity
Native RMSNorm removes global scalar norm except epsilon. Only if scale concern remains, compare whole-h norm matching on k64/k256; mark it as sensitivity, not a main replacement. No temperature calibration. Raw norm/angle/covariance energy remain visible.
## 14. Resource and storage
Prefer oneRTX5090 Spot; use up to2 only if no registered single-card profile is available. Existing shphd-lite-0911 plus mounted PyTorch2.8/cu128 SM120 runtime and existing Qwen transformers overlay. CPU performs data audits/statistics/figures. GPU bounded head decoding and3-document full-model smoke, batch<=16 distributions, no N×condition×vocabulary tensor. Per-condition atomic chunks support interruption/resume. Estimate<2GB new cache/results and<1GPU-hour; record actual duration/memory/device.
## 15. Optional generation
Optional only after all numeric results; up to3 fixed prefixes, k64/k256/full, greedy<=64 new tokens, projection applied at each prediction. No claim of paired contexts after divergence. If omitted, status NOT RUN OPTIONAL; does not replace primary results.
## 16. Outputs and branches
Three primary figure groups: cumulative NLL/KL/entropy; frequency/equal-rank controls; fixed-example distributions. Raw metrics, outputs, contexts, bootstrap and per-doc tables. Summary separates observations, rivals, bounds and one AI-suggested next step. Consistent ordering may support bounded prediction recovery; absent ordering weakens proposed output sequence; incompatible assets or wide/heterogeneous effects imply insufficient evidence. No native mechanism/semantic hierarchy/architecture benefit inferred.
## 17. Freeze, audits and amendments
Manifest pins panels, code/config/protocol/asset hashes before GPU output. Three concise audit passes: scientific identification, data/statistics, implementation/numerics. Fixes preserve observed failures and append amendments with reason; do not overwrite R12. Exact implementation and receipts live execution-side; curated evidence/code in owning project.

### Pre-output amendment A1 (2026-11-01)
Add exact output mass on lexical IDs decoding entirely to Unicode punctuation or whitespace. This is a surface-format proxy, not syntax or semantics. Symbol-only math tokens are excluded. Masks are frozen before outputs. No condition, sample or parameter changes.

### A2 implementation repair (before any valid outputs)
R12 band arrays B are PC-coordinate selectors/rotations. Raw projector columns must be Q=V@B, including exact R12 random controls. Correct this conversion; preserve original exact PC indices. First GPU attempt failed before forward because image FlashAttention ABI mismatched mounted PyTorch. Explicitly disable optional FlashAttention availability and retain SDPA, without editing shared packages or weights. Save initial source/freeze as invalid predecode provenance. Numerical tolerances unchanged.

### A3 identity-gate repair (no transformer forward or valid output yet)
Full-PC FP64 error6.82e-13 passes the original1e-8 limit. Exactly562/754688 originally-zero entries become <=1.50e-13 nonzero after BF16 cast; all other entries match. BF16 has enough exponent range to preserve this negligible roundoff. Replace the inappropriate input-bit-equality stop with direct full-PC vs identity native-logit maximum error<=1e-4 and target-NLL maximum error<=1e-6 on all737 positions, matching batch shapes. Direct identity still must be exact. Record cast nonidentity, retain failed gate and original replay thresholds unchanged.

### A4 same-interface cache refresh after failed legacy replay
Legacy cache on current5090 exceeded the unchanged0.05 NLL gate (292:0.1153); raw h relative difference1.03–1.61%. Preserve this failed audit and exclude legacy h from primary native decoding. Re-extract all180 fixed documents once using exact same official weights/tokenizer/block27 pre-norm hook, BF16 SDPA, fixed1x256 mask192. Cache per document, then replay three fresh documents. Keep original TRAIN mean/PCA unchanged, all position/target/condition/frequency selections unchanged. This is a runtime cache refresh, not a model/hook substitution or PCA fit. Causal-prefix comparison uses the same1x256 tensor shape, masks/zeros all unseen future IDs, avoiding a BF16 kernel-shape change. Original cache/fresh replay and causal numerical thresholds are unchanged. Model calls total180+6, no training.
