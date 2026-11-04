派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/anchor.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R13_20261101_native_spectral_decoding/anchor.md)；研究修改仍回到原件。

---

# R13 round extension: cumulative spectral projection and native decoding

Owner: A15_27_05. This file owns only the authorized R13 round extension, not a parallel main design. R12 is preserved.

## 1. Problem Definition
At fixed Qwen3-0.6B-Base native final norm/output head, which next-token predictions return as variance-ordered residual directions are added? Does recovery favor common/format tokens before contextual content? Unknown T5 settings are not a replication target.

## 2. Physical Priors
R12 block27 residual-post precedes final RMSNorm. Its linear classifier accessibility is not native use. Variance, training-reference token frequency, predicted probability and semantic specificity are different objects. Existing heldout documents are exposed and exploratory.

## 3. Falsifiable Hypotheses
A prespecified cumulative recovery pattern may favor common/format output mass at small k and contextual targets later. Rivals: mean-only output bias; arbitrary rank/retained energy; nonlinear normalization and changed angle; the-specific lexical conditioning. No word-frequency decline alone establishes semantic refinement.

## 4. Mathematical Model
Use the inherited TRAIN-centered full-rank covariance eigenbasis V and mean mu: h_B=mu+V_B V_B^T(h-mu). Decode using the original final RMSNorm followed by its tied frozen lm_head. Identity uses h itself, separately from all-PC reconstruction. Paired NLL measures target accuracy; KL(full||condition) measures model fidelity. These may move in opposite directions.

## 5. Computational Realization
Use all 37 fixed R12 H/the documents at their frozen positions, recovering the true next token from pinned source where a cache ends. Presample a separate natural-position panel outside PCA fitting documents. No model, classifier or dictionary training. Protocol freezes conditions, examples and reference frequency corpus before output inspection.

## 6. Minimal Falsification Tests
Audit hook/shift/padding, exact source token prefix, mean/basis provenance/rank/eigengaps, identity and cache replay. Compare equal-rank bands and seeded random spaces, cumulative head versus head-plus-middle/tail/random. Report norm, retained variance and entropy; keep common-token proxy and semantics separate. Bootstrap documents, not positions.

## 7. Current Evidence
R12 trained simple readouts: coarse head/middle/tail balanced accuracies 94.74/62.28/51.32%; biological fine head/middle each 88.89% with disjoint mistakes. These motivate this question but supply no native-output evidence. R04 reference basis uses 9,600 TRAIN discovery positions, all 1,024 eigenvalues positive; exact numerical audit is in manifest. R13 completed2026-11-01:737 positions,21 native conditions, fresh-cache/identity PASS. Common-reference-ID predictions recover earlier descriptively, while mean-only already creates strong format bias; no external semantic hierarchy established. [Results](summary.md).

## 8. Next Decision
Complete the currently authorized bounded measurements. Scientific closure and mechanism judgments remain researcher-owned. The next scientific experiment will be suggested only after inspecting prediction distributions, frequency controls and counterexamples.
