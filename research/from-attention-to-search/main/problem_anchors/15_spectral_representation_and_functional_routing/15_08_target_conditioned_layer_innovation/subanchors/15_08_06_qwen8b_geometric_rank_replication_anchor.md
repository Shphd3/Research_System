---
anchor_id: 15_08_06_qwen8b_geometric_rank_replication
status: EXECUTED_AWAITING_HUMAN_JUDGMENT
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor.md
depends_on: 15_08_05_aligned_geometric_rank_scale_anchor.md
created: 2026-08-18
updated: 2026-08-18
---

# A15_08_06: Does Qwen3-8B reproduce the aligned broad transition spectra?


## 1. Problem Definition

The aligned Qwen3-0.6B experiment found broad CAR whole-block transitions and ZX projected Attention transitions, with a narrower but still nontrivial \(R_U\). The one question is whether changing only the model to Qwen3-8B materially changes the normalized geometric-rank profiles while data, objects, estimator, and \(r_{90}\) rule remain fixed. This is a model-scale robustness check, not a semantic, functional-rank, clustering, or Router-utility test.

## 2. Physical Priors

Absolute covariance rank scales with feature width, so the cross-model observable is \(r_{90}/d_{object}\). If the same named computations contain similarly heterogeneous token-level changes at both scales, normalized spectral breadth should remain comparable. A material shift would keep model scale alive as a rival explanation.

## 3. Falsifiable Hypotheses

`H-SCALE-STABLE`: all three Qwen3-8B layer-median normalized \(r_{90}\) values differ from their frozen 0.6B references by less than 0.03. `R-SCALE-SHIFT`: at least one absolute difference reaches 0.10. Intermediate or non-converged evidence is `MIXED_OR_INSUFFICIENT`. CAR and ZX medians at least 0.40 are additionally described as broad-spectrum, without implying functional high rank.

## 4. Mathematical Model

For block \(l\), define \(X_l=N_l(h_l)\), \(U_l=N_l(h_l+a_l)-N_l(h_l)\), and \(R_{U,l}=U_l-\widehat{\mathbb E}_{lin}[U_l\mid X_l]\). The evaluated objects are \(H_{l+1}-H_l\), \(Q_{500}^{\top}(a_{l+1}-a_l)\), and \(R_{U,l}\). For descending centered-covariance energy shares \(p_j\), \(r_{90}=\min\{r:\sum_{j\le r}p_j\ge0.9\}\). Cross-model comparison uses layer-median \(r_{90}/d_{object}\).

## 5. Computational Realization

Run the same non-overlapping DCLM TRAIN, DEVELOPMENT, and EVALUATION partitions on local 36-layer Qwen3-8B. TRAIN constructs the final-state PCA-500 basis and ridge fits, DEVELOPMENT selects regularization, and EVALUATION computes spectra. Moving 4096-dimensional sufficient statistics between GPU and CPU is an engineering storage choice and does not alter the estimator.

## 6. Minimal Falsification Tests

Require all three one-million-token spectra and convergence within 0.02 from 524,288 to 1,048,576 tokens. Compare against frozen Qwen3-0.6B medians CAR 0.5625, ZX 0.5940, and \(R_U\) 0.4350586. All differences below 0.03 yield `MODEL_SCALE_INVARIANT`; any difference at least 0.10 yields `MODEL_SCALE_SHIFT`; otherwise return `MIXED_OR_INSUFFICIENT`.

## 7. Current Evidence

The aligned Qwen3-8B run completed on 1,048,576 EVALUATION tokens and all methods converged. Layer-median normalized \(r_{90}\) values were CAR 0.58838, ZX 0.65000, and \(R_U\) 0.32410, changing by +0.02588, +0.05600, and -0.11096 from Qwen3-0.6B. CAR and ZX therefore reproduce broad transition spectra, while the \(R_U\) change reaches the registered model-scale threshold and yields `MODEL_SCALE_SHIFT`. Absolute median \(R_U\) rank is still 1327.5 directions.

CAR target blocks 7 and 17 each have \(r_{90}=1\). Excluding sequence position 0 raises block 7 to867 but leaves block 17 at1, while the CAR layer median remains2410. Boundaries amplify one anomaly but do not create the global broad-rank result.

## 8. Claim Boundary And Next Decision

The evidence supports cross-model CAR/ZX breadth but rejects scale invariance for all three objects because \(R_U\) becomes proportionally narrower. It cannot identify semantic novelty, functional rank, causal use, or Router utility. The one next decision is whether the \(R_U\) shift reflects representation geometry or residualizer calibration, completed by a matched-predictability and fixed-regularization audit before any functional-rank experiment.
