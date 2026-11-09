# Detailed: A15_08_09_E01 Random-Projection Router Preservation

Primary Anchor: [A15_08_09](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_09_random_projection_router_preservation_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)  
Result eligibility: `COMPUTATION_COMPLETE_EXTERNAL_H1_GUARD_UNRESOLVED`

## 0. Conclusion First

- Computational protocol completeness: `PASS`, 19/19 registered computational and delivery items have terminal, auditable states.
- External H1 status: `Insufficient`, because no independent human has reviewed the 64-row pack.
- Numerical full-space result: block 24 H2 `Pass`, H3 `Fail`; block 28 H2 `Pass`, H3 `Fail`.
- Conditional projection result: H4 `SKIPPED_H3_NOT_PASS` by the frozen dependency rule.
- Main interpretation: above-chance access exists, but stable positive-margin linear routability was not detected in the registered object.

Raw worker root: `/data/250010109/MoE_Router/experiments/20260824_a15_08_09_e01_random_projection_router_preservation`  
Formal run root: `runs/representation-full-20260823T200240Z`  
Diagnostic run root: `runs/registered-diagnostics-20260823T211500Z`
Theory-conformance repair root: `runs/theory-conformance-repair-20260823T-theoryrepair3` (`pt-qrsdcjs1`, reserved 4-H100)

## 1. Frozen Objects

At registered block \(\ell\) and the last token of the common `Answer:` suffix,

\[
X_\ell=N_\ell(h_\ell),\qquad Z_\ell=N_\ell(h_\ell+a_\ell),\qquad U_\ell=Z_\ell-X_\ell,
\]

\[
R_{U,\ell}=U_\ell-(X_\ell\widehat B_\ell+\widehat b_\ell).
\]

- Model: `/data/share/Qwen3-30B-A3B`, 48 blocks, hidden width 2,048, BF16 forward, FP32 saved arrays.
- Registered blocks: 24 primary; 28 independent replication that cannot rescue block 24.
- Labels: eight parent domains from the frozen 8-by-8 taxonomy. The 64 child labels are used only in descriptive diagnostics.
- Probe: TRAIN-only L2 multinomial logistic regression; DEV selects \(C\); five fixed seeds; TEST opened once.
- Primary H3 metric: the 5th-percentile true-label logit margin with a 95% confidence interval on both TEST panels.
- Projection: frozen dense Gaussian map and frozen Router weights, but only after H3 `Pass`.

Identity hashes matched the protocol: taxonomy source `60236f...6bb1`, frozen grid `23e510...f030`, model config `2850dd...2297`, index `df0d48...3c24`, and tokenizer `aeb133...ae4`. All 16 indexed checkpoint shards were hashed in each reserved-job preflight.

## 2. Dataset Construction And H1 Evidence

### 2.1 Construction

The final v2 build contains 300 independent items per fine class, 19,200 total: 11,520 TRAIN, 2,560 DEV, 2,560 TEST-same, and 2,560 TEST-new. Each fine class contains 75 definition, 75 comparison, 75 quantitative, and 75 mechanism rows.

Every prompt contains exactly one label-free semantic card from each parent domain and each of eight neutral codes exactly once. The target asks for the broad field of the card bound to one code. Consequently domain vocabulary is present in every row; the label is carried by a relation rather than unigram/bigram presence.

The 9,600 quantitative/mechanism rows were rebuilt from 512 auditable compact schemas before the Qwen3-30B-A3B representation run. Qwen3-8B was only an offline schema drafting helper and contributed no measured hidden state or score.

### 2.2 Machine guards

| Guard | Result |
| --- | ---: |
| Rows | 19,200 exactly |
| Literal parent/child label leaks | 0 |
| Normalized text duplicates | 0 |
| Record-ID duplicates | 0 |
| Split-isolation violations over seven registered provenance IDs | 0 |
| Maximum semantic-card character-5-gram Jaccard | 0.3324, threshold 0.35 |
| Qwen3-30B token range | 119--302, registered 96--320 |
| Maximum per-class cross-split median token gap | 13, threshold 15 |
| Binding-invariant violations | 0 |

The one-per-fine-class AI review contains 52 `PASS`, 12 `PASS_WITH_NOTE`, zero class mismatches, and zero arithmetic mismatches. Its explicit status is `AI_REVIEW_ONLY_NOT_HUMAN_GUARD`. Therefore machine H1 evidence is complete, but formal H1 remains `Insufficient` until an independent human reviews the pack.

### 2.3 Bag-of-words repair

| Dataset | DEV | TEST-same | TEST-new |
| --- | ---: | ---: | ---: |
| Rejected v1 single-topic prompts | — | 0.9254 | 0.9449 |
| Final v2 binding prompts | 0.1316 | 0.1270 | 0.1195 |

The v2 TEST-new result is near the 1/8 chance level and below 90% of block-24 full-\(R_U\) accuracy. This closes the registered lexical-shortcut guard, while the human semantic guard remains external.

## 3. Extraction And Residualization

The formal job loaded and verified the complete 48-layer checkpoint, then executed the exact causal prefix through block 28. A 128-row equivalence smoke established bitwise equality between full-48 execution and prefix-28 execution when both used extraction batch 16. Batch 32 was rejected after a measured relative L2 drift of 0.07220; batch 16 was frozen before the formal run.

Formal merged array:

- shape: `[2 blocks, 19200 rows, 2 objects, 2048 coordinates]`;
- size: 629,145,728 bytes;
- SHA-256: `69f746318e1ec1c81d9d8cf234abd74e89939692056c98da32d93e4d901e3d4a`;
- four shards of 4,800 rows each;
- exact partition, all finite values, and all identity gates: `Pass`;
- replay, output-projection replay, native MLP input, and \(U=Z-X\) relative errors: 0 on all four ranks and both blocks.

DEV selected residualizer ridge \(\lambda=1\) at both blocks. Zero-variance standardized coordinates: 0 at both blocks.

## 4. Full-Space H2/H3 Results

DEV selected probe \(C=0.001\) for all five seeds at both blocks. All selected and permuted-label fits converged. Because LBFGS reached the same optimum under each registered row order, seed accuracy standard deviation is 0.

### 4.1 Main metrics

| Block | TEST panel | Balanced accuracy [95% CI] | Macro-F1 | Positive-margin fraction | Margin median | Margin \(Q_{0.05}\) [95% CI] |
| ---: | --- | --- | ---: | ---: | ---: | --- |
| 24 | same | 0.3258 [0.3179, 0.3334] | 0.3226 | 0.3258 | -0.6046 | -2.8938 [-2.9416, -2.8266] |
| 24 | new | 0.1891 [0.1831, 0.1952] | 0.1638 | 0.1891 | -2.2945 | -9.0587 [-9.2393, -8.9008] |
| 28 | same | 0.2438 [0.2366, 0.2511] | 0.2429 | 0.2438 | -0.6423 | -2.2708 [-2.3197, -2.2377] |
| 28 | new | 0.2258 [0.2190, 0.2326] | 0.2092 | 0.2258 | -1.4883 | -5.7441 [-5.8331, -5.6723] |

H2 passes numerically because every accuracy lower bound is above chance \(1/8\), confidence half-widths are below 0.05, and seed SD is below 0.02. H3 fails numerically because every accuracy lower bound is far below 0.90 and every low-tail-margin interval is below zero. Margin CI half-width divided by DEV margin IQR ranges from 0.0306 to 0.0901, below the 0.20 Insufficient threshold, so this is not a power-width failure.

![Full-space admission result](figures/full_space_admission_gate.png)

### 4.2 Controls

| Control | Block 24 | Block 28 |
| --- | ---: | ---: |
| Identity score relative error | 0 | 0 |
| Common-offset pair-difference relative error | \(4.36\times10^{-17}\) | \(4.23\times10^{-17}\) |
| Permuted-label aggregate, TEST-same | 0.1288; CI contains 0.125 | 0.1259; CI contains 0.125 |
| Permuted-label aggregate, TEST-new | 0.1284; CI contains 0.125 | 0.1200; CI contains 0.125 |
| Maximum individual permutation deviation from chance | 0.0148 | 0.0121 |

The positive Gaussian-mixture, bounded-noise, common-offset, XOR, and concentrated-coordinate synthetic suite passed. These are implementation checks only.

## 5. Conditional H4 State

The formal projection artifact is:

```json
{"h3":"Fail","schema":"a15_08_09_projection_scan_v1","status":"SKIPPED_H3_NOT_PASS"}
```

This terminal status implements the protocol exactly. NMR divides projected low-tail margin by a full-space low-tail margin whose positivity must first be established. Here the denominator is negative, so running and interpreting an \(m\times30\) projection table would violate the registered theorem-to-experiment dependency. No dimension or Gaussian seed is missing from an eligible branch; the branch itself is ineligible.

## 6. Registered Diagnostics

### 6.1 Full-space distance geometry

Amendment A09 replaces the sampled-extrema audit with exact enumeration of all unordered pairs in each 2,560-row TEST panel: 3,275,520 total, 408,320 within-parent, and 2,867,200 between-parent pairs.

| Block | Panel | Extreme \(D_{out}/D_{in}\) | Robust \(Q_{.05}(D_{out})/Q_{.95}(D_{in})\) |
| ---: | --- | ---: | ---: |
| 24 | same | 0.3879 | 0.7350 |
| 24 | new | 0.2172 | 0.4324 |
| 28 | same | 0.2811 | 0.6749 |
| 28 | new | 0.2078 | 0.5198 |

All ratios are below 1, so the sampled parent clusters have neither an extreme nor robust Euclidean distance gap. This agrees with H3 but does not replace it.

### 6.2 Fine-label supervised functional dimension

The corrected fine-label diagnostic learns \(W_q=P_qA_q\) with \(P_q^TP_q=I\) on TRAIN, uses DEV-only early stopping, and evaluates the frozen fit once on both TEST panels at ranks 1--512 and five registered seeds. SVD of the frozen full Router is only a warm start. The smallest rank retaining at least 90% chance-corrected full performance on both panels for four of five seeds including `24001` is 64 at both blocks. The earlier block-24 SVD-truncation value 16 is superseded because truncating a full optimum is not the registered low-rank learning problem.

Absolute full fine-label balanced accuracy is weak: block 24 reaches 0.1066 / 0.0453 on TEST-same/new; block 28 reaches 0.0691 / 0.0598, against chance 0.015625. Therefore \(r_{90}\) describes compression of a weak supervised readout, not semantic support-set rank or strong routing.

### 6.3 Precise uniformity audit

For a supervised subspace basis \(P\in\mathbb R^{d\times r}\) and TRAIN covariance eigenbasis \(U=(u_1,\ldots,u_d)\),

\[
\ell_j=\|P^\top u_j\|_2^2,\qquad
\mu(P;U)=\frac dr\max_j\ell_j,
\]

\[
H(P;U)=-\frac{\sum_j(\ell_j/r)\log(\ell_j/r)}{\log d}.
\]

| Block | Rank | Coherence \(\mu\) | Haar mean [95% range] | Entropy \(H\) | Haar mean [95% range] |
| ---: | ---: | ---: | --- | ---: | --- |
| 24 | 16 | 26.03 | 2.68 [2.34, 3.23] | 0.8388 | 0.9920 [0.9915, 0.9925] |
| 28 | 64 | 5.90 | 1.70 [1.58, 1.89] | 0.9179 | 0.9980 [0.9979, 0.9981] |

Thus neither supervised subspace is close to the same-rank Haar-uniform baseline. Block 28 is less concentrated than block 24, but high entropy alone would overstate uniformity because maximum leverage remains elevated.

### 6.4 Coordinate-sampling eligibility

Using 1,000 fixed, parent-stratified TRAIN difference vectors and \(\varepsilon=0.5\), \(\delta=0.05\), the theorem-three sufficient bound gives:

| Block | Median coherence | 95th percentile | Maximum \(\widehat\mu\) | Required \(m\) | Registered maximum |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 24 | 98.56 | 196.75 | 629.34 | 71,135 | 1,024 |
| 28 | 122.57 | 271.64 | 614.33 | 69,439 | 1,024 |

Both branches are `SKIPPED_TRAIN_COHERENCE_BOUND`. TEST data did not enter eligibility. This is a conservative theorem-sufficient audit, not a proof that empirical coordinate sampling could never work.

## 7. Execution Ledger

| Job | Role | Terminal state |
| --- | --- | --- |
| `pt-349l20jt`, `pt-dw4nw35f` | early schema-generation development attempts | failed; pre-data development only |
| `pt-a1s83i6j` | first representation smoke submission | stopped at zero replicas for missing control implementation |
| `pt-o5gile5s` | short reserved 4-H100 smoke | succeeded |
| `pt-jttinfvr` | long-sequence full-48, batch-16 smoke | succeeded |
| `pt-heuj3gts` | prefix-28, batch-32 equivalence smoke | succeeded operationally; rejected by parity guard |
| `pt-il2q3dma` | prefix-28, batch-16 equivalence smoke | succeeded; bitwise parity |
| `pt-cg4u6b1n` | first formal submission | stopped at zero replicas before prefix optimization |
| `pt-x588ixj0` | formal 19,200-row extraction, residualizer, H2/H3, conditional H4 | `SUCCEEDED`, reserved 4-H100 |
| `pt-ffundzmt` | distance, functional-rank, uniformity and coordinate-eligibility diagnostics | `SUCCEEDED`, reserved 4-H100 |
| `pt-9gobrdb0` | first A09 repair attempt | stopped after mirror found redundant CPU refits; no result |
| `pt-fk7tdmjm` | second A09 repair attempt | stopped after detecting irrelevant full-checkpoint hashing; no result |
| `pt-qrsdcjs1` | exact all-pair distance and learned orthogonal-rank repair | `SUCCEEDED`, reserved 4-H100 |

The formal and diagnostic jobs both resolve to `share-space`, `share-cluster`, one `n6ls.iu.i40.4` worker, four H100 80-GB GPUs, `RESERVED`, normal priority, and the frozen runtime image. The SCO compatibility wrapper is `/data/250010109/MoE_Router/experiments/20260808_online_spectral_router_30b_v1/scripts/sco_acp_compat.sh`.

## 8. Amendments And Deviations

Protocol amendments A01--A03 repaired data-interface and measurement contracts before representation extraction. A04--A05 made controls and distance/scale rules executable before smoke. A06--A07 established exact prefix execution and fixed batch-16 parity before the formal run. A08 operationalized descriptive diagnostics only after H3 was known. A09 then repaired two theory-conformance errors: sampled extrema and SVD-as-learning. A09 explicitly remained barred from changing H1--H4.

No TEST-driven taxonomy, layer, residualizer family, probe family, threshold, or H4 dimension was changed. The only scientific negative result remains negative.

## 9. Completeness And Artifact Map

The original suite reported `44 passed`; the A09 diagnostic unit subset freshly reports `8 passed`. All theory-listed branches now have a valid terminal state: executed, scientifically failed, or conditionally skipped. The sole unresolved external guard is independent human semantic review.

| Artifact | Purpose | Status |
| --- | --- | --- |
| `data_v2/manifest.json` | frozen data identity and machine audit | Complete |
| `data_v2/ai_review_one_per_class.md` | 64-class AI review pack | Complete, not human evidence |
| `runs/v2-bow-parent.json` | lexical shortcut baseline | Complete |
| `runs/representation-full-20260823T200240Z/preflight.json` | formal model/GPU hashes | Complete |
| `.../extraction/manifest.json` | identity and exact merge | Complete |
| `.../residualizer/manifest.json` | ridge selection and artifacts | Complete |
| `.../full_space_probe/result.json` | H2/H3 and controls | Complete |
| `.../projection_scan/result.json` | registered H4 dependency stop | Complete terminal skip |
| `runs/registered-diagnostics-20260823T211500Z/diagnostics/result.json` | distance, rank and uniformity diagnostics | Complete |
| `runs/theory-conformance-repair-20260823T-theoryrepair3/repair/result.json` | exact pair geometry and learned orthogonal functional rank | Complete; supersedes A08 distance extrema and SVD rank |
| `runs/completion_audit.json` | machine-readable 17-item closure audit | Complete |
| [Full-space admission figure](figures/full_space_admission_gate.png) | audited core negative result | Complete |
| [Theory-experiment closure figure](figures/theory_experiment_closure.png) | admission, exact geometry, and diagnostic repair in one figure | Complete and visually audited |

## 10. Claim Boundary And Next Decision

The result establishes only that the registered \(R_U\) and linear probe expose above-chance but non-positive-margin parent structure. It does not establish projection failure under a valid positive-margin premise, because that premise was not observed. It also does not establish expert utility, nonlinear impossibility, intrinsic rank, or distribution-free behavior.

The sole proposed next decision is **yes, open representation-space learning as a new bounded anchor**, after closing the independent human H1 review. Its first experiment must test whether an expert-utility-aligned learned representation makes the held-out low-tail routing margin positive; it is not authorization for a broad training sweep. Replace, rather than tune, this preservation question. The active Focus remains human-owned and is not silently marked complete here.
