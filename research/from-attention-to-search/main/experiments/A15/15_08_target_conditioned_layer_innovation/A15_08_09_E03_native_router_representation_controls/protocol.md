---
experiment_id: A15_08_09_E03_native_router_representation_controls
document_status: COMPUTATION_COMPLETE_EXTERNAL_H1_GUARD_UNRESOLVED
design_frozen_at: 2026-08-24
approval_source: user confirmed the exact representation/statistical design and then explicitly instructed direct execution
anchor: ../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_09_random_projection_router_preservation_anchor.md
focus: ../../../../../../../Projects/from-attention-to-search/main/focus/focus_random_projection_router_preservation.md
predecessor: ../A15_08_09_E02_qwen30b_all_layer_gain_and_preservation/protocol.md
worker_root: /data/250010109/MoE_Router/experiments/20260824_a15_08_09_e01_random_projection_router_preservation
---

# Protocol: Native Router-Input And Adjacent-Layer Difference Controls

## 0. Approval Snapshot

- **Purpose:** determine whether E02's negative standalone result is specific to the constructed \(R_U\) residual or extends to the model's native Router input and its adjacent-layer change.
- **Anchor clause:** E02 cannot claim that another linear representation is impossible.
- **Experiment role:** operationalization comparison; it does not reopen H3/H4 or the random-projection theorem.
- **Treatment A:** native Router input \(G_\ell\) at every block.
- **Treatment B:** adjacent-layer Router-input difference \(\Delta G_\ell\) for blocks 2--48.
- **Control:** chance level \(1/8\), TRAIN-label permutation, unchanged frozen data/splits/token/model observables, and immutable E02 \(R_U\) evidence.
- **Changed variable:** representation only.
- **Held fixed:** Qwen3-30B-A3B, 19,200 rows, final `Answer:` token, eight parent labels, TRAIN/DEV/two TEST panels, linear-probe families, seeds and uncertainty procedure.
- **Primary metric:** balanced accuracy on both TEST panels at the independently DEV-frozen layer for each representation.
- **H5 Pass:** both TEST-panel simultaneous conditions have aggregate 95% lower bounds above \(1/8\), all five fits converge, and the permuted-label control contains chance.
- **H5 Fail:** eligible evidence exists but at least one TEST-panel lower bound is not above \(1/8\).
- **Insufficient:** representation identity, split, selection-freeze, convergence, permutation, completeness, or provenance guard fails.
- **Cannot claim:** that the native gate uses the registered label, that readable labels match expert utility, causal specialization, or pristine confirmation because E02 previously opened the TEST panels.
- **Execution:** implementation, smoke, and one full reserved four-H100 ACP run are explicitly approved. Theory-file edits, commit, push, publication, and root sync are not approved.

## 1. Terminology / Definitions

For block \(\ell\), let \(G_\ell\) be the last-token hidden state after the block's attention residual addition and `post_attention_layernorm`, immediately before `Qwen3MoeSparseMoeBlock.gate`. E02 stores \(X_\ell\) and \(U_\ell\) such that

\[G_\ell=X_\ell+U_\ell.\]

The second representation is

\[\Delta G_\ell=G_\ell-G_{\ell-1},\qquad \ell=2,\ldots,48.\]

\(\Delta G_1\) is undefined and must not be zero-filled. A **class** means one of the eight frozen parent labels, not one of the 64 fine classes. Balanced accuracy is the unweighted mean of the eight per-class recalls; chance is \(1/8\).

For TRAIN rows \(i=1,\ldots,N\), representation dimension \(d=2048\), class mean \(\mu_c\), and global mean \(\mu\), define per-coordinate within- and between-class variances:

\[V_{\mathrm{within}}=\frac{1}{Nd}\sum_i\lVert g_i-\mu_{y_i}\rVert_2^2,\]

\[V_{\mathrm{between}}=\frac{1}{Nd}\sum_i\lVert\mu_{y_i}-\mu\rVert_2^2.\]

Their ratio is descriptive and cannot prove separability because it discards directional overlap and low-tail behavior.

## 2. Anchor Alignment

E02 established conditional added accessibility in \(R_U\) but failed standalone cross-template positive-margin routing. Its registered boundary explicitly leaves other linear representations open. E03 tests that boundary using the actual gate input and a minimal adjacent-layer difference. It does not change E02, does not rerun Gaussian preservation, and does not edit the theory document.

## 3. Tested Hypotheses

- **H5-G:** the DEV-frozen native Router-input layer is linearly readable above chance on both TEST panels.
- **H5-Delta:** the DEV-frozen adjacent-layer difference is linearly readable above chance on both TEST panels.
- **Descriptive geometry:** publish the full TRAIN \(V_{\mathrm{within}}\), \(V_{\mathrm{between}}\), and ratio curves for both representations; these curves do not rescue an H5 failure.

## 4. Rival Explanations

The principal rival is that \(R_U\) discarded readily accessible class information already present in the native state. The adjacent-layer arm separates accumulated native readability from new cross-layer change. Label permutation catches estimator leakage. TRAIN-only variance and DEV-only layer selection prevent the requested plots from using TEST labels to choose a layer.

## 5. Data Construction And Provenance

Reuse E02 `data_v2/metadata.jsonl`: 19,200 rows, with 11,520 TRAIN, 2,560 DEV, 2,560 same-template TEST, and 2,560 new-template TEST. Reuse E02's merged all-layer `objects.npy` and its manifest. No model forward, data generation, residualizer fit, or taxonomy edit is permitted. The external 64-row human H1 review remains unresolved and bounds the overall dataset claim.

## 6. Learning Task And Permitted Supervision

Input is one 2,048-dimensional representation at the final `Answer:` token; output is one of eight parent labels. TRAIN labels fit probes, DEV labels select ridge penalty/layer and logistic penalty, and TEST labels are read only after each representation's `layer_freeze.json` exists. Fine labels, template identity, answer text, split name, and E02 TEST performance cannot enter selectors.

## 7. Model / Architecture And Frozen Variants

The frozen source model is `/data/share/Qwen3-30B-A3B`, 48 sparse MoE blocks. `G` covers blocks 1--48. `Delta` covers blocks 2--48. E02's extraction identity receipt must show finite values, exact \(U=Z-X\) reconstruction, exact partition, and BF16-native-input tolerance pass. No parameters are updated.

## 8. Training Objective And Optimization

The all-layer screen uses the existing GPU ridge basis and \(\lambda\in\{10^{-6},\ldots,10^2\}\). For each layer, TRAIN fits one-hot parent targets; DEV chooses minimum cross-entropy and records balanced accuracy. The frozen layer maximizes DEV balanced accuracy, then minimizes DEV cross-entropy, then uses the smaller layer index.

At the frozen layer, use the existing five-seed L2 multinomial-logistic family, seeds 24001--24005, \(C\in\{10^{-6},\ldots,10^2\}\), DEV selection by balanced accuracy then log loss then smaller \(C\), and maximum 10,000 iterations.

## 9. Conditions, Seeds, And Checkpoints

- Representations: `native_router_input`, `adjacent_router_delta`.
- Ridge layers: 1--48 and 2--48 respectively.
- Probe seeds: 24001--24005; primary seed 24001.
- Aggregate bootstrap: 2,000 stratified row-and-seed draws, seeds 8240932001 and 8240932002.
- Permutation seeds: 8240933000 plus probe seed.
- No checkpoints; every output is deterministic from frozen arrays, metadata, and registered seeds.

## 10. Primary Metric And Frozen Analysis Plan

For each representation separately:

1. compute TRAIN variance curves;
2. run all-layer ridge TRAIN/DEV screening and write a TEST-label-redacted freeze file;
3. fit the five-seed logistic family at the frozen layer;
4. evaluate ordinary accuracy, balanced accuracy, macro-F1, and true-label margins on both TEST panels;
5. stratified-bootstrap rows within each class and resample seeds to obtain aggregate two-sided 95% intervals.

H5 Pass requires both balanced-accuracy interval lower bounds to exceed 0.125, all fitted models to converge, both confidence half-widths to be at most 0.05, across-seed standard deviation at most 0.02, and both permuted-label intervals to contain 0.125 with maximum absolute seed deviation at most 0.05. Otherwise a complete guarded run is H5 Fail; a failed guard is Insufficient. No multiplicity claim is made across layers because TEST is evaluated only at one DEV-frozen layer per representation.

## 11. Secondary Metrics And Guards

Full per-layer DEV balanced accuracy and DEV cross-entropy are published. TRAIN \(V_{\mathrm{within}}\), \(V_{\mathrm{between}}\), total-variance identity error, and ratio are published. Ordinary accuracy is reported beside balanced accuracy. Margin is descriptive; it does not activate E02 H3 or H4. Raw E02 \(R_U\) values may be cited as immutable predecessor evidence but are not refit or used to select E03 layers.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: hand-constructed separated class centers must yield positive between variance and high ridge accuracy.
- Known bad: identical class distributions must yield near-zero between variance; permuted TRAIN labels must remain at chance.
- Known confusing: adding a common offset must leave within/between variance unchanged; zero-filling undefined \(\Delta G_1\) must be rejected.

## 13. Scientific Procedure And Stage Contracts

1. Verify frozen inputs, hashes, shapes, split counts, identity receipts, and derive representation views without writing another 15GB copy.
2. Smoke on a balanced subset; require exact hand-checks, layer-domain enforcement, finite outputs, deterministic freeze, readable tables, and both figures.
3. Run full all-layer variance/ridge screens in parallel on two GPUs, freeze one layer per representation, then run formal five-seed confirmation and controls.
4. Render figures and audit every required artifact, hash, layer count, split boundary, and verdict input before interpretation.

## 14. Algorithm, Output, And Provenance Contract

Worker outputs live in `runs/e03-native-representations-<mode>-<stamp>/`. Required outputs are `preflight.json`, one variance/scan CSV and JSON per representation, two `layer_freeze.json` files, formal probe JSON, permutation-control JSON, two figure PNGs, a comparison table, and `completion_audit.json`. Every result records input hashes, code hashes, representation definitions, data counts, selected layer, seeds, job id, resource contract, and elapsed time.

## 15. Success / Failure / Insufficient Evidence

H5-G and H5-Delta independently receive `Pass`, `Fail`, or `Insufficient`. The experiment is computationally complete only when both receive a typed verdict and both requested figures/reports have claim-eligible source tables. External H1 remains a separate unresolved overall guard and cannot erase eligible computational measurements.

## 16. What This Cannot Claim

Linear readability of \(G\) or \(\Delta G\) does not show that Qwen's learned gate weights use the parent label, that parent labels correspond to expert utility, that class variance causes routing, or that a learned Router will improve language modeling. Because TEST panels were opened in E02, E03 is a registered successor diagnostic, not a pristine independent confirmation.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A. Question/boundary | CONFIRMED | user requested broader representations and preserved theory-file boundary |
| B. Data/provenance | CONFIRMED | user requested reuse; E02 frozen data and extraction receipts |
| C. Task/supervision | CONFIRMED | approved 8-parent-label design and frozen splits |
| D. Architecture | CONFIRMED | verified Qwen3-MoE gate input plus approved adjacent difference |
| E. Objective/optimization | CONFIRMED | approved ridge screen plus five-seed logistic confirmation |
| F. Evidence/verdict | CONFIRMED | requested variance curves and accuracy data; chance/guard rule frozen |
| G. Execution/reproducibility | CONFIRMED | direct execution approval; reserved four-H100 ceiling retained |

Cross-block consistency: **PASS**. Implementation, smoke, and full run: **APPROVED**. Scientific body freezes before the first test implementation. Post-start changes require an append-only amendment with eligibility impact.

### Amendment A01 — TEST-redacted metadata compatibility (2026-08-24)

- **Before:** the new scanner constructed a dense parent-label vector by reading `parent_id` from every metadata row.
- **After:** exactly as in E02's frozen scanner, it reads `parent_id` only for TRAIN and DEV and assigns the unused sentinel `-1` to every other split.
- **Reason:** the approved selection view deliberately deletes TEST labels. Smoke job `pt-ke7t231v` stopped with `KeyError: parent_id` before completing any layer, metric, selection, or TEST evaluation.
- **Scientific body:** unchanged. Data, representations, layers, classifier, metric, selection rule, thresholds, seeds, and reports are unchanged.
- **Approval:** implementation-fault self-repair is inside the user's direct full-execution authorization.
- **Eligibility impact:** `pt-ke7t231v` is retained and ineligible. The repair is covered by a failing-then-passing regression test; a fresh smoke must pass before the formal run.

### Amendment A02 — reuse passed model-identity hashing in the formal run (2026-08-24)

- **Before:** every E03 job reran SHA-256 over the unchanged 57GB Qwen3 checkpoint even though E03 performs no model forward and consumes only E02's frozen extraction.
- **After:** the formal job reuses successful smoke `pt-9buoxe62`'s complete model/checkpoint identity receipt, while independently requiring four visible GPUs with at least 75 GiB each and re-auditing the E02 extraction source before scanning.
- **Reason:** remove a measured four-minute I/O-only repeat without weakening the representation-source or resource guards.
- **Data visible:** only smoke artifacts; no formal scan, layer selection, or TEST result exists.
- **Scientific body:** unchanged. The representations, data, layers, probes, metrics, thresholds, seeds, and confirmation boundary are identical.
- **Eligibility impact:** none; the reused receipt and the formal worker's device assertion remain in the formal artifact chain.

### Execution receipts

- Failed smoke retained as ineligible: `pt-ke7t231v`, reserved `n6ls.iu.i40.4`, 2026-08-24 03:30:19--03:34:55 UTC.
- Passing smoke: `pt-9buoxe62`, reserved `n6ls.iu.i40.4`, 2026-08-24 03:37:47--03:45:50 UTC; completion audit passed.
- Formal run: `pt-bfom1dhm`, reserved `n6ls.iu.i40.4`, 2026-08-24 03:48:22--04:13:19 UTC; state `SUCCEEDED`; completion audit passed.
- Canonical result records: [summary.md](summary.md) and [detailed.md](detailed.md).
