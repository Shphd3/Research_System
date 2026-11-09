# Detailed: A15_08_09_E03 Native Router Representation Controls

Primary Anchor: [A15_08_09](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_09_random_projection_router_preservation_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)  
Result eligibility: `ELIGIBLE_COMPUTATION`; external H1 review unresolved  
Knowledge status: `AI_EVIDENCE_RECORD_AWAITING_HUMAN_JUDGMENT`

## 0. Quick Recap

- **Purpose:** test whether E02's standalone \(R_U\) failure extends to the model's native Router input and its adjacent-layer difference.
- **Direct result:** native block 42 and adjacent-difference block 41 both pass the registered two-panel above-chance accuracy gate.
- **Boundary:** neither representation passes a positive low-tail-margin condition; no native gate-use or expert-utility claim is available.
- **Interpretive update:** class information is present in broader Router states even though global class scatter remains within-class dominated.

## 1. Terminology / Definitions

| Term | Plain meaning | Computation | Decision role | Cannot prove |
| --- | --- | --- | --- | --- |
| \(G_\ell\) | actual state seen by the layer-\(\ell\) MoE gate | \(X_\ell+U_\ell\) | broader accumulated-state control | that the frozen gate weights use the label |
| \(\Delta G_\ell\) | change between adjacent Router inputs | \(G_\ell-G_{\ell-1}\), \(\ell\ge2\) | tests new cross-layer change | an isolated attention or expert write |
| Within variance | average class-local scatter | \(\frac1{Nd}\sum_i\|g_i-\mu_{y_i}\|^2\) | requested geometry curve | directional separability |
| Between variance | scatter of class means | \(\frac1{Nd}\sum_i\|\mu_{y_i}-\mu\|^2\) | requested geometry curve | positive margin |
| Balanced accuracy | equal-weight mean of eight class recalls | mean per-class recall | primary TEST metric | expert utility or calibration |

## 2. Anchor Link And Decision Point

E02 establishes controlled incremental accessibility in \(R_U\) but fails standalone positive-margin H3. Its explicit boundary says that another linear representation remains open. E03 is an operationalization comparison under that boundary. It does not rerun random projection and does not modify the theory file.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Eligibility impact |
| --- | --- | --- | --- | --- |
| Frozen data | E02 19,200-row metadata | SHA-256 `1a653a6fe8f24b8aa3ebf97f0a336a060a9efb1513500c108831441db0b454b0` | Pass | none |
| Frozen extraction | `[48,19200,2,2048]` \((X,U)\) | E02 object SHA-256 `cba20c5e3eb484a82c03246f6471b8da1e1c1a40f29c7cde9a037a99fa8ea144` | Pass | none |
| TEST-blind selection | TRAIN/DEV only | redacted selection metadata; freeze receipts written first | Pass | none |
| Native layer domain | 1--48 | all 48 rows present | Pass | none |
| Delta layer domain | 2--48 | all 47 rows present; no block-1 zero fill | Pass | none |
| Five probe seeds | 24001--24005 | complete for both representations | Pass | none |
| Permutation controls | chance contained on both panels | all four intervals contain 0.125 | Pass | none |
| Formal resource | one reserved 4-H100 worker | `n6ls.iu.i40.4`, 4×80GB H100, 88 CPUs | Pass | none |
| Formal completion | all required artifacts and audit | `pt-bfom1dhm` `SUCCEEDED`; audit passed | Pass | none |

Amendment A01 repaired only TEST-redacted metadata access before any metric existed. Failed smoke `pt-ke7t231v` is ineligible and retained. Passing smoke `pt-9buoxe62` established execution readiness. Amendment A02 reused that smoke's model-identity hashing because E03 performs no model forward; the formal job rechecked four visible 80GB GPUs and the E02 extraction source.

## 4. Actual Setup

- TRAIN 11,520; DEV 2,560; same-template TEST 2,560; new-template TEST 2,560.
- Statistical label: eight balanced parent classes; 64 fine labels are not used.
- Observation: final token of the common `Answer:` suffix.
- Ridge screen: \(\lambda\in\{10^{-6},\ldots,10^2\}\); DEV minimum cross-entropy per layer; final layer ranking by balanced accuracy, then cross-entropy, then smaller layer.
- Confirmatory probe: multinomial L2 logistic regression, \(C\in\{10^{-6},\ldots,10^2\}\), maximum 10,000 iterations. All native seeds select \(C=0.1\); all delta seeds select \(C=1.0\).
- Uncertainty: 2,000 stratified row-and-seed bootstrap draws; classes are equally weighted.
- Representations are derived on demand from the memory-mapped E02 array; no second 15GB representation copy and no new model extraction are created.

## 5. Metrics And Registered Decision Rules

H5 Pass requires both TEST balanced-accuracy interval lower bounds above 0.125, convergence, confidence half-width no larger than 0.05, seed standard deviation no larger than 0.02, and valid chance-centered permutation controls. Variance curves and margins are secondary and cannot rescue or negate H5.

## 6. Evidence Lineage

| Claim | Raw artifact | Computation | Observed value | Eligibility | Boundary |
| --- | --- | --- | --- | --- | --- |
| Native input is readable | `probes/native_router_input/result.json` | five-seed logistic + 2,000 bootstrap draws | 0.77898/0.75430 same/new | Eligible, H5 Pass | not native gate use |
| Adjacent difference is readable | `probes/adjacent_router_delta/result.json` | same registered probe | 0.76398/0.71211 | Eligible, H5 Pass | not isolated expert utility |
| Native total scatter is within-dominated | `scans/native_router_input/layer_scan.json` | TRAIN scatter decomposition | selected ratio 0.04038; maximum 0.07449 | Eligible descriptive | not a separability verdict |
| Delta total scatter is within-dominated | `scans/adjacent_router_delta/layer_scan.json` | same decomposition | selected ratio 0.04971; maximum 0.06160 | Eligible descriptive | not a separability verdict |
| Positive low-tail geometry is absent | both probe JSON files | TEST \(Q_{0.05}\) of true-minus-best-rival score | all four values and intervals negative | Eligible descriptive | does not negate high average accuracy |

## 7. Main Results

### Native Router input

The DEV screen freezes block 42 at balanced accuracy 0.77148. Its TRAIN within variance is 0.054919 per coordinate, between variance is 0.002217, and the ratio is 0.040376. Formal accuracy is:

| Panel | Ordinary accuracy | Balanced accuracy [95% CI] | Margin \(Q_{0.05}\) [95% CI] |
| --- | ---: | ---: | ---: |
| Same template | 0.77898 | 0.77898 [0.77195, 0.78602] | -2.1440 [-2.2353, -2.0679] |
| New template | 0.75430 | 0.75430 [0.74695, 0.76164] | -2.8559 [-2.9774, -2.7260] |

The permuted-label means are 0.12375 and 0.12828; both intervals contain 0.125. Across-seed accuracy standard deviation is at most 0.000175.

### Adjacent-layer difference

The DEV screen freezes block 41 at balanced accuracy 0.76133. Its TRAIN within variance is 0.014476, between variance is 0.000720, and the ratio is 0.049712. Formal accuracy is:

| Panel | Ordinary accuracy | Balanced accuracy [95% CI] | Margin \(Q_{0.05}\) [95% CI] |
| --- | ---: | ---: | ---: |
| Same template | 0.76398 | 0.76398 [0.75664, 0.77141] | -2.6626 [-2.7184, -2.5698] |
| New template | 0.71211 | 0.71211 [0.70477, 0.71953] | -4.2588 [-4.3976, -4.1195] |

The permuted-label means are 0.12641 and 0.12266; both intervals contain 0.125. Across-seed standard deviation is at most 0.000175.

## 8. Visualization Results

### Native input

![Native Router-input variance and accuracy](figures/native_router_input_variance.png)

The top panel is the requested TRAIN within/between variance curve on a log scale. The lower panel places the DEV balanced-accuracy curve and between/within ratio beside the TEST-blind frozen block. Both variance components grow with depth, but within variance stays larger. The late increase in between variance accompanies improved readability without creating a between-dominant global scatter.

### Adjacent difference

![Adjacent Router-input difference variance and accuracy](figures/adjacent_router_delta_variance.png)

The delta curve shows a similar late-depth accessibility transition. The ratio is non-monotone and peaks at block 45, while the DEV accuracy selector freezes block 41. This separation is evidence that maximizing a global variance ratio is not equivalent to maximizing held-out classification.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | What it rules out |
| --- | --- | --- | --- |
| Source identity | E02 completion audit and object hash | Pass | stale or incomplete extraction |
| Representation algebra | total-variance identity error below \(3.85\times10^{-15}\) | Pass | variance-accounting error |
| TEST-blind freeze | block 42 / 41 receipts | Pass | TEST-guided layer choice |
| Confirmatory accuracy | both H5 verdicts Pass | Pass | broad absence of linear class information |
| Positive low-tail margin | all four intervals negative | Fail as descriptive geometry | robust all-row positive-margin interpretation |
| Native gate / expert utility | not measured | Not run | nothing; remains open |

## 10. Full Experiment Record

- Failed smoke: `pt-ke7t231v`, 03:30:19--03:34:55 UTC, ineligible metadata-reader fault.
- Passing smoke: `pt-9buoxe62`, 03:37:47--03:45:50 UTC, completion audit Pass.
- Formal: `pt-bfom1dhm`, 03:48:22--04:13:19 UTC, `SUCCEEDED`, completion audit Pass.
- Resource for all jobs: reserved `n6ls.iu.i40.4`, one worker, 4 H100 80GB, 88 CPU cores, 960 GiB memory.
- Fresh local verification after implementation: 62 tests passed.

## 11. Interpretation

Direct observation is not “the classes have more between-class than within-class variance.” The opposite is true for the summed scatter. The direct result is that small, aligned discriminative directions inside a within-dominated high-dimensional state are sufficient for strong held-out classification. \(R_U\) removed or reorganized much of this readily accessible accumulated signal, so its standalone failure cannot be generalized to the original Router state.

## 12. Claim Boundary

Can claim: stable linear parent-class accessibility in \(G\) and \(\Delta G\) under the registered successor protocol.  
Cannot claim: native gate use, expert usefulness, causal routing, positive low-tail margin, or independent untouched TEST replication.

## 13. Next Decision

Proposed, awaiting human judgment: if representation-space learning is opened, define its target as expert utility plus positive low-tail margin, and require \(G\) and \(\Delta G\) as frozen baselines. Do not justify it as recovering absent semantic information.

## 14. Artifact Manifest

| Artifact | Purpose | SHA-256 / identity | Complete | Eligible |
| --- | --- | --- | --- | --- |
| [native figure](figures/native_router_input_variance.png) | native variance/readability evidence | `b07d27cb7cae8192cee4e81e9ca08d7ac83d29e513adcd222e3ac1520b66191c` | Yes | Yes |
| [delta figure](figures/adjacent_router_delta_variance.png) | delta variance/readability evidence | `7e93303c964c513d648ac1e113681705c064d8ff11d921e34efa4984f99b41b9` | Yes | Yes |
| [accuracy table](tables/accuracy_summary.csv) | two-panel formal values | `7775d6a70a343e04eaf80a47efd161bcfe9b1dfed72e956edadd8bddea039492` | Yes | Yes |
| [native scan](tables/native_router_input_layer_scan.csv) | 48-layer source table | `6755d0ebdf5632818a91c983ea1abdb16730eabefa1bc26ffb07a3bbf32414da` | Yes | Yes |
| [delta scan](tables/adjacent_router_delta_layer_scan.csv) | 47-layer source table | `89f40b5ec8d1c0bbcddfed2b6739543e4ffa87ccb7e2efb661cd35d794acaaf7` | Yes | Yes |
| Formal raw run | complete JSON, controls, logs, audit | `runs/e03-native-representations-full-20260824T034800Z` | Yes | Yes |

## 15. Links

- Worker root: `/data/250010109/MoE_Router/experiments/20260824_a15_08_09_e01_random_projection_router_preservation`
- Formal result root: `/data/250010109/MoE_Router/experiments/20260824_a15_08_09_e01_random_projection_router_preservation/runs/e03-native-representations-full-20260824T034800Z`
- Runner: `scripts/run_e03_native_representation_pipeline.sh`
- Formal job: `pt-bfom1dhm`

