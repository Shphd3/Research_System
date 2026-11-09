# A15_27_05_01: Dense checkpoint spectral dynamics, 0.5B–33B training tokens

## 1. Problem Definition

During the existing native Dense trajectory, do variance scale, variance allocation, principal subspaces, paired-text relations and externally labeled readability become approximately stable at the same training progress? The parent [spectral position and semantic granularity Anchor](../15_27_05_spectral_semantic_granularity_anchor.md) established only frozen Qwen observations. Its results cannot answer this Dense dynamics question. The researcher activated this bounded extension on 1 November 2026 and explicitly authorized design, audit, smoke and formal read-only analysis. Here B denotes one billion cumulative valid prediction tokens; the model has 281,431,040 parameters. No new language model or dictionary is trained. The decision is whether the observed temporal ordering warrants a dynamics explanation of the proposed head/middle/tail division; architecture utility remains separately untested.

## 2. Physical Priors

This analysis assumes paired inputs and compatible model coordinates along one documented training lineage. It does not assume that variance rank is a semantic hierarchy or that the last checkpoint is converged. Finite text sampling can produce apparent direction drift, particularly across nearly equal eigenvalues. A second live rival is coordinate rotation that preserves sample relations.

## 3. Falsifiable Hypotheses

The researcher asks three independent questions: A, whether variance scale and allocation stabilize; B, whether the directions carrying variance continue rotating; C, whether paired-text relations and classification information stabilize despite rotation. A possible head-before-middle/tail ordering is a conjecture, not a prerequisite. Continued changes, reversals, absent incremental readability or differences comparable to sampling variation weaken that explanation or leave it insufficient. No positive ordering is forced.

## 4. Mathematical Model

One observation is the hidden vector at a fixed natural token position in a fixed document prefix. At training progress t, reference vectors form H_t with N rows and 1024 columns. Its own reference mean is mu_t. The centered covariance and its ordered eigenvalues are

\[
X_t=H_t-\mathbf1\mu_t^T,\qquad C_t=X_t^TX_t/(N-1)=V_t\operatorname{diag}(\lambda_t)V_t^T.
\]

The singular values of X_t are s_i=sqrt((N-1)lambda_i), not lambda_i. Total variance is trace(C_t); normalized eigenvalues p_i=lambda_i/trace(C_t) describe allocation; effective rank is exp(-sum_i p_i log p_i). These are descriptive estimators, not learning objectives.

For two equal-dimensional orthonormal bases U and V, singular values of U^TV give cosines of principal angles, and sqrt(1-||U^TV||_F^2/k) is the normalized projection distance. All 1024 dimensions span the entire space and are excluded as evidence of direction stability. Linear centered CKA compares paired evaluation sample relations. Reference-only orthogonal Procrustes minimizes ||X_t R-X_33||_F with R^TR=I; independent evaluation residuals retain scale differences because no scaling is fitted. Fixed V_33 projected variances diag(V_33^T C_t V_33) describe variance in endpoint directions and are not the early checkpoint's eigenvalues. Logistic readouts separately refit each checkpoint and basis on the same labeled TRAIN and DEVELOPMENT splits.

## 5. Computational Realization

Freeze the twelve actually readable compatible states and their source hashes in [manifest.json](manifest.json). Preserve absent payloads as missing. Use the native eight-block model's final_raw_h, the last block residual-post before norm. Existing pre_mlp_input caches are a different location and are not reused as this tensor. A 2,048-record N8 natural-text panel contributes 32 positions per 256-token prefix; 1,024 reference and 1,024 evaluation records give 32,768 vectors each, equal record weights. Paper-level identity is unavailable, so record grouping is an explicit approximation. Reference means, covariance bases and alignment never fit evaluation samples. R12's separate 96-document common-the panel retains its exact 192-token sequences, positions, labels and document-family splits. It supplies a Dense semantic bridge, not Qwen activations or a large covariance sample.

Compare adjacent and endpoint-relative raw subspaces at ranks16/64/128/256 and equal 64D head1–64, middle481–544, tail961–1024. Compare raw drift, aligned drift and CKA side by side. Early/mid/late are fixed at0.5/17/33B; only these points receive block0/3 supplements and labeled readouts. Deterministic paired reference splits quantify estimator sensitivity. [Protocol](../../../../../experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/protocol.md) freezes computation, fit boundaries, controls, resource budget and stop rules.

## 6. Minimal Falsification Tests

Numerical calibration must separate identity, pure orthogonal rotation, scaling and sample permutation: equal spectra do not imply fixed raw directions; scale-invariant CKA does not imply equal variance. The primary descriptive evidence is the vector of adjacent distances and distances per actual billion training tokens, checked against paired document-split variability. No universal stability tolerance is justified, so this round reports curves and 0.5/1/2-times sampling-reference sensitivity, without declaring an onset time. Eight fixed paired reference splits at early/mid/late and a deterministically selected largest spectral-rate turn provide uncertainty references. This is sampling sensitivity, not eight model replicates or a calibrated population confidence interval. Positive readout increments require paired heldout intervals above zero and Holm correction across prespecified increments. Wide intervals, weak full-space readability, unresolved eigengaps or missing checkpoints yield explicit insufficiency.

## 7. Current Evidence

NOT RUN at initial registration. The inventory confirms twelve readable states at0.5,1,3,5,10,15,17,19,21,22.018691584,31,33B. Some original manifests outlive their deleted weights;19B is read from its hash-matched continuation archive. Original state counters, strict weight loading and hook equality remain runtime gates. Qwen R12 results remain separately owned and do not count as Dense observations.

## 8. Claim Boundary And Next Decision

Results concern this model, trajectory, interface and fixed corpus. Approaching33B only means approaching the end of this window. Stable eigenvalues, stable directions, stable sample relations, linear readability, native causal use and routing utility are distinct claims. Tail direction instability at inadequate sample resolution means unidentifiable under this estimator, not permanently unstable. The single next decision, after the complete evidence is reviewed, is whether a temporal head/middle/tail explanation is supported enough to retain as a hypothesis. Researcher mechanism acceptance and question closure remain Unknown. Resume from the bilingual Summary and coverage ledger; do not infer staged-routing optimality or judge unfinished training experiments from these curves.
