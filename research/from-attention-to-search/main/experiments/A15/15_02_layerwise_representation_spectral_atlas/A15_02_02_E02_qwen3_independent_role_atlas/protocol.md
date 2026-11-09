---
experiment_id: A15_02_02_E02_qwen3_independent_role_atlas
anchor_id: 15_02_02_natural_hierarchy_role_localization
status: approved_for_implementation_smoke_and_full
approved_by: user
approval_date: 2026-08-02
---

# Protocol: Qwen3-8B Independent-Covariance Semantic-Role Atlas

## 0. Approval Snapshot

Approval status: approved for Protocol, implementation, smoke, and full run. Purpose: determine whether the same concept's parent versus child role occupies different covariance ranks in frozen Qwen3-8B. Primary anchor: [A15_02_02](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_02_natural_hierarchy_role_localization_anchor.md). Physical prior: raw head energy can be mechanical; role selectivity must survive per-direction variance normalization. Experiment role: frozen representation and metric audit. Primary metrics: chain-paired parent-minus-child raw and whitened per-direction band means. Minimal setup: embedding plus all 36 block outputs, 128 independent DCLM documents / 65,536 tokens, 32 fixed hierarchy chains, four exact-position template pairs. Pass requires a stable layer-band role effect through all validity gates; valid null evidence is Fail; failed pairing, basis, reconstruction, or tail robustness is Insufficient. Cannot claim Router utility, compositional computation, or training benefit. Approval decision: user authorized continuous execution on 2026-08-02.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Raw energy | Actual activation carried by one spectral direction | \((u_i^\top(h-\mu))^2\) | activation squared | Shows real contribution including background scale | Semantic selectivity |
| Whitened energy | Activation relative to that direction's ordinary variance | \(a_i^2/\max(\lambda_i,\epsilon)\) | dimensionless | Removes the mechanical singular-value advantage | Utility or causality |
| Same-concept role pair | Identical target concept used once as child and once as parent | Equal token ids, absolute target span, and sequence length | one pair per chain/template | Removes lexical and position confounds | Natural discourse generality |
| Fine band | One twelfth of covariance ranks | F1--F12 | mean per direction | Preserves rank resolution | Single-vector identity under degeneracy |
| H/M/T | Coarse rank groups | F1 / F2--F5 / F6--F12 | mean per direction | Tests head versus non-head | Equal semantics across layers |

## 2. Anchor Alignment

Decision question: does a Qwen3-8B layer contain a stable semantic-role-to-rank association after independent covariance fitting and background-variance normalization? Falsifier: raw differences without stable whitened differences, or effects that fail templates, chain resampling, basis stability, or tail sensitivity. Claim boundary: representation association only.

## 3. Tested Hypothesis

H1: parent and child roles produce a stable paired contrast in at least one layer-band after whitening. The specific descriptive questions are whether the parent role is relatively more head-selective and whether only the final block reverses the pre-terminal pattern.

## 4. Rival Explanations

R0: raw differences are entirely covariance scale. R1: wording or target position causes the effect. R2: unstable eigenvectors or tiny tail eigenvalues create the pattern. R3: isolated layers or outlier chains create an apparent depth trend.

## 5. Data / Model / Algorithm / Objective

Model: local frozen `/data/share/Qwen3-8B`, bfloat16 inference on one H100; no fine-tuning. Surface: embedding output and each decoder block output residual state, layers 0--36. Calibration: 128 distinct documents from the fixed DCLM held-out `.jsonl.zst`, each contributing one deterministic 512-token Qwen slice; exact sentence leakage is prohibited. Evaluation: the existing 32 chain identities rendered into four parent/child minimal-pair templates. Covariance is centered with calibration means and decomposed offline once per layer.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Rival | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| raw vs whitened | scale versus selectivity | R0 | separates actual energy from background advantage | primary | report both | only raw stable | tail invalid | Figures 1--3 |
| four paired templates | role versus wording | R1 | checks wording invariance | primary guard | at least 3/4 same sign | mixed signs | invalid pair | template table |
| split-half basis | stable rank bands | R2 | protects spectral object | validity guard | normalized overlap excess \((O-r/d)/(1-r/d)\geq0.25\) in H/M/T for at least 35/37 layers and both layers 35/36 | unstable bands | no basis | stability table |
| epsilon \(10^{-6},10^{-5},10^{-4}\lambda_1\) | tail robustness | R2 | detects noise amplification | validity guard | conclusion unchanged | effect disappears | too few effective ranks | sensitivity table |
| 2,000 chain bootstraps and 5,000 chain-label swaps | chain-level inference | R3 | avoids token/template pseudoreplication | primary inference | CI excludes zero and permutation/FDR passes | null | missing chains | statistics table |
| all layers 0--36 | depth and terminal reversal | R3 | prevents sparse-layer extrapolation | primary | adjacent/depth-region replication | isolated cells | missing layer | Figures 2--3 |

There is one frozen model and no training seed. Random seeds are 20260802 for document selection, 20260803 for bootstrap, and 20260804 for permutation. Statistical unit: 32 chains.

## 7. Primary Metric

For layer \(\ell\), direction \(i\), chain \(c\), and template-averaged role state, compute parent-minus-child raw and whitened energy. Aggregate fine bands and H/M/T by the mean per direction, never by total dimensions. Report mean difference, paired log ratio, 95% chain-bootstrap interval, sign fraction, label-swap \(p\), and Benjamini--Hochberg \(q\) over layer-by-band cells within each metric/resolution family.

A stable band effect requires: bootstrap interval excluding zero; \(q<0.05\); at least 3/4 templates with the aggregate sign; at least 18/32 chain signs; robustness to all registered epsilon regimes; and either the same sign in two adjacent layers or the separately registered final-layer reversal gate.

Final-layer reversal requires layer 36 to be significant, opposite to layer 35 and the median of layers 1--35, with at least 3/4 templates and 18/32 chains supporting the terminal sign. Otherwise it is not called a reversal.

## 8. Secondary Metrics

Per-direction curves, raw/whitened role means, 12-band heatmaps, H/M/T trajectories, eigenvalue spectra, effective-rank counts, split-half overlaps, covariance reconstruction error, and Parse/token audit fields.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: identical target token ids at identical positions after a fully visible relation. Known bad: root-versus-leaf lexical comparison and relation text after the target. Known confusing: individual eigenvectors inside near-degenerate bands; per-direction curves are descriptive and band inference is primary.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| S0 | Are model, corpus, hashes, and chains fixed? | provenance manifests | exact match | manifests | S1 |
| S1 | Are all minimal pairs valid and all hooks complete? | smoke texts/tokens/shapes | every guard passes | smoke audit | S2 |
| S2 | Is covariance reconstructible and stable? | moments/eigensystems | reconstruction/energy/stability pass | basis audit | S3 |
| S3 | Are raw/white metrics numerically stable? | epsilon/effective-rank table | conclusion invariant | metric audit | S4 |
| S4 | Is a semantic-role effect stable? | bootstrap/permutation/templates/chains | apply Section 7 | full tables/figures | result record |

## 11. Algorithm Specification

Input: frozen model, 128 natural documents, 32 chains, four template pairs. Parameters: 512 tokens/document, 12 bands, three whitening floors, 2,000 bootstraps, 5,000 permutations. Steps: build and hash manifests; extract online layer moments; eigendecompose each layer; extract paired target states; compute raw/white direction scores; aggregate by chain; run guards and inference; render and visually inspect Figures 1--3. Outputs: complete text/token manifest, model/corpus provenance, bases and state caches in worker storage, curated CSVs/figures and result records in mainline.

## 12. Success / Failure / Insufficient Evidence

Pass: at least one stable layer-band parent/child association passes every guard. Fail: all engineering/data/basis gates pass but no stable effect exists, or a claimed uniform mapping is contradicted by layer-specific signs. Insufficient: any mandatory gate prevents interpretation. A model-conditioned layer-specific Pass does not reinstate the previously failed universal cross-model claim.

## 13. What This Cannot Claim

No result establishes that covariance rank causes semantics, that deeper layers compute composition, that a band is a Router target, that experts benefit, or that another model shares the mapping.

## 14. Review Notes And Protocol Changes

The user supplied and approved the complete design on 2026-08-02 and authorized Protocol completion, implementation, smoke, full run, audit, and focus closure without another approval pause. AI additions are the explicit FDR, adjacent-layer, template-sign, chain-sign, epsilon, and terminal-reversal rules; they formalize the supplied stability requirements before observing E02 results.

Before E02 data were inspected, split-half stability was frozen as normalized overlap excess \((O-r/d)/(1-r/d)\geq0.25\) for H/M/T in at least 35 of 37 representation surfaces, with layers 35 and 36 mandatory. This compares observed projector overlap \(O\) with the random same-rank expectation \(r/d\) without imposing an impossible raw-overlap threshold on wide bands.
