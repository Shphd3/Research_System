派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R08_within_mixed_subspaces_20261029/protocol.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R08_within_mixed_subspaces_20261029/protocol.md)；研究修改仍回到原件。

---

# Protocol: R08 domain-internal and mixed subspaces

## 0. Approval Snapshot
APPROVED_FOR_BOUNDED_EXECUTION by explicit current user task; A–G confirmed by supplied specification, operational seeds/counts fixed here under delegated routine implementation. Purpose: distinguish the four geometric competitors, not discover semantic modules. [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_02_within_mixed_subspaces_anchor.md); [Focus](../../../../focus/focus_within_mixed_domain_subspaces.md). Role: robustness/operationalization analysis. Frozen UTC 2026-10-29T13:13:36.000857+00:00. Existing-resource only; up to384 existing-text forwards, zero new text. Old heldout is exposed exploratory data.

## 1. Definitions and fixed data
Each row is one final target1024vector, not a concatenation. Copy384 original rows byte-for-byte with24/12/12 families. Math/bio/wordings/endings equally weighted. Zero-based model.layers[1,13,27] outputs, residual-post before final norm. NativeBF16 model, FP32 stored, FP64 statistics. Last layer reuse R07; new last-layer extraction is only same-forward identity check.

## 2. Native CrossCoder
A22 checkpoint /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt; SHA 09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628. Fourteen odd block residual-post inputs are jointly encoded with training centering/RMS and learned native threshold. Same1024 encoder batch as R04 (256 LM padded tokens plus768 normalized-zero padding); native shared16384z, no layer-local surrogate. Preserve normalization, decoder, gate and parameter hashes. No SAE.

## 3. Statistical fitting
Discovery192rows:96perdomain; single-ending48perdomain. Subtract domain means before single-domain PCA, pooled mean before mixed PCA. Denominator n, no whitening or per-coordinate standardization. k4/8/16/32; numerical rank tolerance smax*max(n,1024)*FP64eps; unsupported basis is NA. Save means/eigenvalues/top32bases and ranks. Verify C_mix=C_within+delta delta^T/4 numerically (relative Frobenius error<1e-10), orthonormality<1e-9 and overlap identity bounds. Store principal angles.

## 4. Comparable stability and intervals
200 fixed family half splits, seed2026102908:12discoveryfamilies each half, all versions together. Within math A–B, bio A–B; cross math A–bio B and math B–bio A, average both. Every comparison uses48samples/domain/half (24at single ending), so single-ending k32 half-overlap NA. Show full24family cross overlap separately from matched-half comparison. Partition percentile ranges are sensitivity, NOT population CIs. 200 family bootstrap discovery refits seed2026102909 give pointwise95% intervals for full overlap, mixed-domain overlap, delta coverage and between variance. For heldout delta coverage resample12heldoutfamilies with discovery bases fixed. Do not redraw directions based on development/heldout. 200 Haar random-space pairs in1024D seed2026102910, k nested; expected overlap k/1024. No formal p-value decision/multiple-test claim; all layers,k,endings reported. No arbitrary high/stable cutoff introduced after seeing results.

## 5. Covariance explanation
Within contribution trace(U_mix^T C_within U_mix); between ||U_mix^T delta||²/4; divide each by total mixed retained variance. Full covariance identity checked with equal weights and denominator. Also retain each-domain total variance and fixed-space explained variance on development/heldout. Unit center-difference projection uses discovery and separately original heldout deltas in fixed discovery spaces. This projection is not classification-information fraction.

## 6. Ending control and UMAP
Repeat key numeric comparisons all/E0/E1 with same family splits. UMAP true raw1024vectors separately for blocks1/13/27, and one shared16384z. Discovery only fit; development and exposed-heldout transform separately. cosine, neighbors15,min_dist.1,seeds42(main),17,73,transform_seed42,n_epochs500,n_jobs1. No whitening, feature normalization or winner selection. Record zero/nonfinite rows and exclude only those from UMAP. Use same coordinates for domain/ending coloring; domain colors, ending marker, split outline. Three-seed neighborhood-overlap diagnostics describe layout sensitivity. No classification or cluster inference from UMAP.

## 7. Procedure, guards and stop
Check asset IDs/current access, hashes, token/row/split invariants. Main same384forward also captures jointinput; compare all final targets with R07 exact expected values, stop if relativeerror>.01. Firsttwo native encode outputs verify manual legacy threshold gate exactly, offline on same tensors. Charge before each attempt, no automatic retry. All parameters frozen, no optimizer; compare state hashes before/after, no gradients. Missing UMAP dependency blocks only its visualizations, not main geometry; do not replace algorithm. No new text/resources/Work tasks. PCA/UMAP statistical fitting explicitly allowed; no model/dictionary fitting.

## 8. Decision branches and deliverables
Four competitors reported as bounded AI interpretation with numerical stability and ending qualifications; research acceptance Unknown. Full and matched-half estimates distinguish sample-size effects. If internal spaces unstable, low cross overlap is insufficient. Save6independent numbered figure families, early/midcontrols, covariance decomposition, full tables, text/vector index, means/bases, scripts, one-page Chinese summary and overall layer judgment table. Include two possible readings, actual outcome and cannot-claim for each figure. Do not cover up unsupported k. Stop after delivery.

## 9. Freeze and audits
Inputs and settings in config.json; pre-execution freeze.json hashes Anchor,Protocol,config and input texts. Three audits: scientific identification (four rivals/no semantic naming), data/statistics (family independence/exposed heldout/rank), implementation (nativehooks/gates/zero updates/identities). Result-owned Summary/Detailed preserve failures and factual counts. User explicitly requests interpretations now; human acceptance remains Unknown. No external publication authorized.
