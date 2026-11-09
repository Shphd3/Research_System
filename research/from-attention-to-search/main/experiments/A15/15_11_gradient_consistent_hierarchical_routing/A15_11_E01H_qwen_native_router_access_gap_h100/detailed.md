---
experiment_id: A15_11_E01H_qwen_native_router_access_gap_h100
status: MACHINE_EVIDENCE_COMPLETE
interpretation_status: HUMAN_CONFIRMED_AS_NON_OWNING_H100_SENSITIVITY
eligibility: E01H_PROTOCOL_ELIGIBLE_NON_OWNING_H100_SENSITIVITY
completed: 2026-08-29
acp_job: pt-vkikyszj
run_id: full-20260829T172910Z
resource_profile: h100-4-reserved
---

# Detailed: Qwen3-30B-A3B Native Router Accessibility Chain

Primary Anchor: [A15_11 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md)

Frozen Protocol and registered revision: [protocol.md](protocol.md), SHA-256
`d9d6468a5fca75b274983e0b907c6d34a0db6b39e44ee1ad7e02ca16d0bd6601`

Summary: [summary.md](summary.md)

Curated primary table: [primary_layer_metrics.csv](tables/primary_layer_metrics.csv)

Canonical result directory:
[full-20260829T172910Z/qwen](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/)

Result status: `MACHINE_EVIDENCE_COMPLETE`. Eligibility is scoped to
`E01H_PROTOCOL_ELIGIBLE_NON_OWNING_H100_SENSITIVITY`; all registered E01H
machine admissions passed, and the researcher accepted the bounded
interpretation as non-owning H100 sensitivity evidence.

## 0. Quick Recap

- **Purpose:** locate held-out eight-parent accessibility loss along the exact
  frozen Qwen native interface \(H\rightarrow Z\rightarrow Q\).
- **Hypothesis:** the native Gate projection preserves most accessibility,
  top-8 selection causes material loss, and the sparse route still retains
  label association above a matched null.
- **Direct result:** BF16 and FP32 both produce
  `TOP8_SELECTION_BOTTLENECK_WITH_RETAINED_ASSOCIATION`. In both C4 and C5,
  Blocks 4/12/20/28 pass projection-preserved + material-selection-loss +
  retained-association; Block 36 fails only projection preservation.
- **Registered cross-panel counts:** projection preserved `4/5`; material
  selection loss `5/5`; retained route association `5/5`; near-total sparse
  retention `0/5`; Gate-projection bottleneck `0/5`.
- **Eligibility:** all inputs, devices, Gate tensors, prediction rows, probe
  convergence, bootstraps, nulls, figures, and producer hashes passed. Block 44
  remains visible but is excluded as `PILOT_NOT_BLIND`.
- **Boundary:** this establishes supervised accessibility and route-label
  association under one readout family. It does not establish native causal
  semantic use, expert utility, language-model loss benefit, or a pretraining
  mechanism.
- **Execution ownership:** E01H is a collision-safe reserved-H100 successor.
  It does not execute the current
  [8×RTX5090 Focus](../../../../focus/focus_gradient_consistent_hierarchical_routing.md). The 5090 E01/E03 owner has
  completed its machine-evidence run and retains the workstream's sole next
  decision; E01H creates no second mainline next decision.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| \(H_\ell\) | native hidden input | 2,048-dimensional final-decision-token vector received by MoE MLP/Gate at Block \(\ell\) | vector in \(\mathbb R^{2048}\) | upper end of the native chain | that every coordinate is Gate-visible |
| \(Z_\ell\) | native Gate logits | exact bias-free projection \(W_{g,\ell}H_\ell\) with BF16 \(H\) and BF16 Gate weights | vector in \(\mathbb R^{128}\) | tests Gate-row-space visibility | that the native Gate uses an external label |
| \(Q_\ell\) | native sparse route | FP32 softmax of \(Z\), native top eight, selected-weight renormalization, zeros elsewhere | 128-vector with eight nonzeros summing to one | tests the actual sparse selection interface | expert correctness or utility |
| Balanced accuracy (BA) | recall averaged equally across eight parent classes | mean of eight held-out per-parent recalls | fraction; chance \(1/8=0.125\) | primary accessibility score | calibration or causal use |
| Negative log likelihood (NLL) | probability calibration loss | mean negative log predicted probability of the true parent | nats/example; lower is better | registered calibration guard | replacement of the BA verdict |
| \(D_{proj}\) | projection gap | \(BA(H)-BA(Z)\) | BA fraction | locates loss at \(H\rightarrow Z\) | population information loss |
| \(D_{select}\) | selection gap | \(BA(Z)-BA(Q)\) | BA fraction | locates loss at \(Z\rightarrow Q\) | expert utility loss |
| \(D_{total}\) | total accessibility gap | \(BA(H)-BA(Q)\) | BA fraction | descriptive end-to-end loss | which operation caused the loss by itself |
| \(R_Z\) | chance-corrected Gate retention | \((BA(Z)-0.125)/(BA(H)-0.125)\) | dimensionless, empirical, unclipped | normalizes projection retention above chance | causal fraction of semantic information |
| \(R_Q\) | chance-corrected sparse retention | \((BA(Q)-0.125)/(BA(H)-0.125)\) | dimensionless, empirical, unclipped | normalizes sparse-route retention | causal fraction of expert utility |
| \(I_Q(Y;E)/H(Y)\) | route-label association | mutual information between parent \(Y\) and route-mass expert index \(E\), divided by parent entropy | dimensionless | tests whether \(Q\) remains associated with parent | that the Gate intentionally uses semantics |
| Projection preserved (P) | strict Gate-retention admission | lower 95% \(R_Z\ge0.90\) and upper 95% \(D_{proj}\le0.05\) | Boolean per panel/block | one required verdict component | perfect projection equivalence |
| Material selection loss (S) | practically large sparse-selection loss | lower 95% \(D_{select}\ge0.10\) | Boolean per panel/block | one required verdict component | a language-model loss penalty |
| Retained association (A) | native route association beyond null | observed \(I_Q/H(Y)\) above matched max-layer null q97.5 | Boolean per panel/block | distinguishes sparse loss from complete label-independence | native causal semantic routing |
| Near-total sparse retention (N) | almost all above-chance access survives | lower 95% \(R_Q\ge0.90\) | Boolean per panel/block | rival no-bottleneck profile | functional equivalence |
| C4 / C5 | two controlled expression panels | separate 1,920-row panels sharing semantic atoms | panel identity | required cross-panel agreement | independent replication |
| `PILOT_NOT_BLIND` | values visible before freeze | Block 44 in both panels and numeric paths | exclusion label | prevents pilot leakage into confirmation | evidence for the line verdict |

## 2. Anchor Link And Decision Point

A15_11 separates four evidence layers: semantic accessibility, counterfactual
expert-utility accessibility, native Router use, and end-task functional
benefit. E01H measures only the first layer along the actual frozen Gate and
top-8 interface. It answers whether a fixed linear probe can recover the
external parent label from \(H\), \(Z\), and \(Q\) on held-out template families.

The decision point is therefore narrow: does the registered pattern support a
Gate-projection bottleneck, a top-8 selection bottleneck with retained
association, no material bottleneck, or a mixed/not-established profile? E01H
does not execute alternative experts and cannot adjudicate the Anchor's
synthetic utility-supervision or hierarchy-benefit hypotheses.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Protocol and scope | frozen E01H scientific contract; implementation, smoke, and full run approved | exact current Protocol hash `d9d6468a...bd6601` captured before execution | pass | [code receipt](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/code_receipt.json) | none |
| Resource | one reserved worker, exactly 4 H100 GPUs | four `NVIDIA H100 80GB HBM3`; a final read-only scheduler query reported worker spec `n6ls.iu.i40.4` and reserved quota, but its describe response was not persisted | pass / receipt limited | [preflight](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/preflight.json), [submission receipt](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/submit-h100-4-reserved-20260829T172910Z.txt) | no numerical impact; scheduler provenance is not self-contained |
| Frozen data / checkpoint | exact activation, metadata, split, extraction, checkpoint hashes | every expected and actual hash matched | pass | `qwen/preflight.json` | none |
| Gate identity | BF16 `[128,2048]` Gate tensor for each one-based block mapping | all six payload hashes matched; Blocks 4/12/20/28/36/44 map to module indices 3/11/19/27/35/43 | pass | `qwen/preflight.json` | none |
| Panels / blocks | C4 and C5; confirmation 4/12/20/28/36; pilot 44 | exact matrix present | pass | [results](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/results.json) | none |
| Native numeric path | BF16 \(H\), BF16 `F.linear`, FP32 softmax, top-8, selected-weight renormalization | the producer stored the H probe from cached FP32 values while constructing Z/Q through BF16; a final read-only audit checked all 47,185,920 activation values and found zero BF16 round-trip mismatches | pass / identity-receipt limited | [feature manifest](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/feature_manifest.json), prediction audit | H is value-identical to the registered BF16 object, but this check is not a producer receipt |
| Probe contract | A-to-B and B-to-A; train-only mean and C selection; fixed solver/grid | 72/72 outer fits, 72/72 inner selections, and 2,520/2,520 inner fold/C fits converged | pass | fit diagnostics inside `layer_metrics.csv` | none |
| Row identity | every panel/layer/feature has one out-of-fold prediction per row | 36 cells × 1,920 unique rows = 69,120; each direction has 960 | pass | `predictions.csv.gz` | none |
| Bootstrap | 10,000 paired complete-family draws; seed 151101; 30 families | all 12 panel/block cells contain 10,000 draws for all eight reported quantities; positive retention denominators | pass | [bootstrap ledger](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/bootstrap_ledger.json) | none |
| Label null | 1,000 complete-family parent-block permutations; seed 151102; max over five confirmation layers | exact draws, formula, thresholds, confirmation set, and pilot exclusion recorded | pass | [null ledger](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/null_ledger.json) | none |
| FP32 sensitivity | sensitivity only; qualitative line verdict must agree with BF16 | same `TOP8_SELECTION_BOTTLENECK_WITH_RETAINED_ASSOCIATION` verdict | pass | [FP32 rows](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/fp32_sensitivity_layer_metrics.json) | none |
| Pilot | Block 44 rendered but never counted | excluded from `confirmation_layers`, cross-panel booleans, counts, and verdict | pass | `results.json`, bootstrap and null ledgers | none |
| Secondary fine diagnostic | cannot alter primary verdict | 288 rows, explicitly `SECONDARY_DOES_NOT_AFFECT_PRIMARY_VERDICT` | pass / secondary | [conditional fine ledger](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/conditional_fine_ledger.json) | none |
| Required figures | three registered figures, hash-audited and manually readable | all present and local copies match producer hashes; the heat-map Block 44 gray-background claim is not visually realized | pass / cosmetic contract limited | [completion audit](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/completion_audit.json) | no metric or verdict impact |
| Test gates | CPU suite plus dedicated CUDA regression | 86 passed, 1 skipped in CPU-sharded suite; dedicated CUDA regression 1/1 passed | pass | [tests.log](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/logs/tests.log), [cuda_regression.log](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/logs/cuda_regression.log) | none |
| Run completion | final clean run and artifact closure | a final read-only scheduler query reported ACP `pt-vkikyszj` terminal state `SUCCEEDED`; qwen and global completion audits passed | pass / receipt limited | submission receipt; [global completion audit](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/completion_audit.json) | scheduler describe response was not persisted |
| Earlier run | only final clean run may be canonical | `full-20260829T164730Z` was explicitly classified noncanonical and contributes no row, number, or verdict here | excluded | execution-owner canonicalization; final artifact paths in this record | prevents cross-run mixing |
| Code revision identity | exact producer and orchestration identity should be recoverable | worker is not a Git repository; analysis-producer hashes are captured in `code_receipt.json`, but execution-time hashes for `run_pipeline.sh` and `submit_h100_4_reserved.sh` are absent | bounded deviation | live repository check plus code receipt | no numerical eligibility change; orchestration identity is incomplete |
| Runtime warning | no mutation of read-only cached activation arrays | PyTorch emitted a non-writable NumPy-array warning; the audited path only reads/casts the tensor before `F.linear` | recorded warning | `logs/qwen_full.log` and source path | no eligibility impact; in-place reuse would require a successor repair |
| Focus ownership | H100 successor must not impersonate the active 5090 lane | the 8×RTX5090 E01/E03 owner has completed its machine-evidence run and owns the workstream's sole next decision; E01H remains non-owning | scope boundary | [current Focus](../../../../focus/focus_gradient_consistent_hierarchical_routing.md) | E01H is eligible only under its own Protocol, cannot close that Focus, and creates no second mainline next decision |

**Frozen Protocol revision:** SHA-256
`d9d6468a5fca75b274983e0b907c6d34a0db6b39e44ee1ad7e02ca16d0bd6601`.

**Execution scope approved:** E01H implementation, label-blind smoke, and one
reserved 4×H100 full run.

**Amendments:** the successor Protocol changed only resource/provenance
isolation before any scientific result was inspected. No post-start layer,
label, representation, threshold, estimator, numeric primary path, or verdict
rule changed.

**Retries and exclusions:** the earlier noncanonical run is wholly excluded;
the final run contains no replaced layer, panel, probe cell, or prediction row.
Block 44 is the preregistered pilot exclusion, not a failed condition.

**Evidence-completeness limits:** all BF16 primary scientific artifacts required
for the machine verdict are present. FP32 stores its row-specific route-null
thresholds but not a separate raw null-draw ledger; the ACP scheduler describe
response was not persisted; the code receipt omits execution-time runner and
submitter hashes; and the H BF16 identity check was a final read-only
recomputation rather than a producer receipt. These limits do not change the
BF16 verdict or the persisted FP32 qualitative-agreement result, but they block
a claim of fully self-contained final-audit provenance.

**Post-hoc analyses:** none enter the verdict. NLL, conditional fine, adjusted
mutual information, load entropy, effective expert count, top-8 overlap, and
plots remain guards or diagnostics exactly as registered.

## 4. Actual Setup

- **Research question:** where is externally defined eight-parent held-out
  accessibility lost along the exact native \(H\rightarrow Z\rightarrow Q\)
  chain?
- **Data:** frozen C4 and C5 controlled natural-language panels. Each panel has
  1,920 rows = 30 complete template families × 8 parents × 8 children.
- **Split:** pre-existing A/B halves, 15 disjoint complete families and 960 rows
  per half. A trains and B tests, then B trains and A tests.
- **Label:** balanced eight-way `parent_id`. Reused global `child_id` is not a
  shared primary label.
- **Blocks:** confirmation Blocks 4, 12, 20, 28, 36; visible pilot Block 44.
- **Model:** frozen `/data/share/Qwen3-30B-A3B`; no model parameter is trained or
  updated.
- **Representations:** \(H\in\mathbb R^{2048}\); exact frozen bias-free
  \(W_g\in\mathbb R^{128\times2048}\); \(Z=W_gH\); \(Q\) is the renormalized native
  top-8 route in \(\mathbb R^{128}\).
- **Primary numeric path:** H100 BF16 \(H\) → BF16 `F.linear` → FP32 softmax →
  native top-8 → selected-weight renormalization → sparse \(Q\).
- **Sensitivity path:** FP32 \(HW_g^\top\) and FP32-derived top-8 route; never
  substituted for the primary path.
- **Preprocessing:** coordinate mean estimated on the training half and applied
  to both halves; no coordinatewise scale normalization.
- **Readout:** multinomial L2 logistic regression, `lbfgs`, intercept,
  `max_iter=5000`, `tol=1e-8`; C grid
  \(\{10^{-4},10^{-3},10^{-2},10^{-1},1,10,100\}\).
- **Regularization selection:** five deterministic train-only folds of complete
  template families, three families per validation fold; mean validation NLL,
  with smaller C breaking ties.
- **BF16 selected C:** H 24/24 at 100; Z 22/24 at 100 and 2/24 at 10; Q 24/24
  at 100.
- **FP32 selected C:** H 24/24 at 100; Z 23/24 at 100 and 1/24 at 10; Q 24/24
  at 100.
- **Uncertainty:** 10,000 paired bootstrap draws per panel/block, resampling 30
  complete template families with identical indices for H/Z/Q; seed 151101.
- **Null:** 1,000 complete-family label permutations applied identically across
  features and confirmation layers, using a five-layer max statistic; seed
  151102.
- **Resource:** ACP workspace `share-space`, cluster `share-cluster`, worker
  `n6ls.iu.i40.4`, one node, normal priority, reserved quota, exactly four
  H100-80GB GPUs. Layers rotate by block offset modulo four.
- **Runtime:** PyTorch `2.8.0a0+5228986c39.nv25.06`, CUDA 12.9, NumPy 1.26.4,
  SciPy 1.15.3, scikit-learn 1.6.1, safetensors 0.5.3, matplotlib 3.10.3.
- **Job / run:** ACP `pt-vkikyszj`, `SUCCEEDED`; run
  `full-20260829T172910Z`.
- **Known setup limitation:** this is a frozen-observational representation
  audit on one checkpoint and controlled panels, not a Router intervention.

## 5. Metrics And Registered Decision Rules

For \(K=8\) parents and held-out balanced accuracy \(BA\),

\[
D_{proj}=BA(H)-BA(Z),\qquad
D_{select}=BA(Z)-BA(Q),\qquad
D_{total}=BA(H)-BA(Q).
\]

When \(BA(H)>1/K\),

\[
R_Z=\frac{BA(Z)-1/K}{BA(H)-1/K},\qquad
R_Q=\frac{BA(Q)-1/K}{BA(H)-1/K}.
\]

At each panel/block:

1. **Projection preserved:** lower bootstrap 95% \(R_Z\ge0.90\) and upper
   bootstrap 95% \(D_{proj}\le0.05\).
2. **Material selection loss:** lower bootstrap 95%
   \(D_{select}\ge0.10\).
3. **Retained route association:** observed \(I_Q(Y;E)/H(Y)\) exceeds the matched
   panel's max-confirmation-layer null q97.5.
4. **Near-total sparse retention:** lower bootstrap 95% \(R_Q\ge0.90\).

The registered line verdict is
`TOP8_SELECTION_BOTTLENECK_WITH_RETAINED_ASSOCIATION` when at least four of
five confirmation blocks satisfy conditions 1--3 in both C4 and C5. The Gate
projection rival requires lower bootstrap 95% \(D_{proj}\ge0.10\) in both panels
at at least four blocks. The no-material-bottleneck rival requires at least
four blocks with both projection preservation and near-total sparse retention.

Any missing/invalid cell, hidden BA below its matched null, frozen-input
failure, or BF16/FP32 line-verdict disagreement makes the experiment
`Insufficient`. NLL and all secondary diagnostics cannot rescue or reverse the
BA verdict.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Input and execution eligibility | all identities and exactly four reserved H100s pass | preflight and Gate tensors | SHA-256 and device/type/shape checks | exact, no uncertainty | every required match true | eligible | pass | file hashes, not Git commit |
| Hidden accessibility admission | \(BA(H)\) above matched max-layer null | out-of-fold H predictions and null draws | eight-class BA; label permutations | 1,000 draws, q97.5 over five layers | BA(H) 0.994792--1.000000 vs C4 0.171354 and C5 0.175000 | eligible | pass in 10/10 confirmation cells | one probe family |
| Gate projection preservation | \(R_Z\) lower 95% \(\ge0.90\) and \(D_{proj}\) upper 95% \(\le0.05\) | paired H/Z predictions | registered gaps and chance correction | 10,000 family-bootstrap draws | joint pass at Blocks 4/12/20/28; fail at 36 | eligible | `4/5` | failure of strict preservation is not automatically a Gate bottleneck |
| Material top-8 loss | \(D_{select}\) lower 95% \(\ge0.10\) | paired Z/Q predictions | registered selection gap | same paired bootstrap | all panel/block lower bounds 0.411458--0.544792 | eligible | `5/5` | accessibility loss, not LM loss |
| Retained sparse-route association | \(I_Q/H(Y)\) above matched route null | native Q loads and label-null ledger | route-mass mutual information divided by parent entropy | max-layer q97.5 from 1,000 null draws | all 10 cells pass; smallest observed 0.002660 vs matched 0.001334 | eligible | `5/5` | association is not causal use or utility |
| Near-total sparse retention | \(R_Q\) lower 95% \(\ge0.90\) | paired H/Q predictions | chance-corrected retention | 10,000 family-bootstrap draws | lower bounds 0.293727--0.474405 | eligible | `0/5` | no statement about nonlinear decoders |
| Primary line verdict | at least 4/5 joint P+S+A in both panels | BF16 criterion cells | registered cross-panel Boolean intersection | fixed five confirmation blocks | 4/5 joint triple pass | eligible | `TOP8_SELECTION_BOTTLENECK_WITH_RETAINED_ASSOCIATION` | C4/C5 are not independent replicates |
| Numeric sensitivity | FP32 must not reverse qualitative line verdict | FP32 per-row metrics | same criteria recomputed from FP32 H/Z/Q | same fixed panels and blocks | same `4/5,5/5,5/5,0/5` profile | eligible sensitivity | agrees | no separately persisted FP32 raw null-draw ledger |
| Pilot exclusion | Block 44 cannot enter counts or verdict | pilot rows and ledgers | explicit exclusion before cross-panel count | none | `PILOT_NOT_BLIND` in both panels/paths | ineligible for confirmation | excluded | descriptive only |
| Conditional fine diagnostic | cannot alter primary verdict | parent-conditional child probes | fixed secondary analysis | 288 rows; 1,000 null draws | complete | secondary only | no primary effect | reused child IDs remain parent-conditional |

## 7. Main Results

### 7.1 BF16 primary matrix

The following values are rendered to six decimal places from the
machine-precision rows. `P/S/A/N` means projection preserved / material
selection loss / retained association / near-total sparse retention. Full
precision and NLL are in
[layer_metrics.csv](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/layer_metrics.csv); the compact local source is
[primary_layer_metrics.csv](tables/primary_layer_metrics.csv).

**Display-rounding limitation:** the table below and the compact local CSV use
different, previously unspecified six-decimal tie conventions in ten cells,
creating display-only differences of `0.000001`. The affected fields are C4
Blocks 4/20 projection upper bounds; C5 Block 4 BA(Z) and projection upper
bound; C5 Blocks 12/20 projection upper bounds; C5 Block 28 BA(H) and selection
lower bound; and C5 Block 36 BA(Q) and \(R_Q\) lower bound. The machine-precision
worker rows own every criterion and verdict; neither raw values nor decisions
are changed here.

| Panel | Block | BA(H) | BA(Z) | BA(Q) | \(D_{proj}\) 95% CI | \(D_{select}\) 95% CI | \(R_Z\) 95% CI | \(R_Q\) 95% CI | \(I_Q/H(Y)\) / null | P/S/A/N |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| C4 | 4 | 1.000000 | 0.997917 | 0.563542 | [0.000000, 0.004687] | [0.411458, 0.457812] | [0.994643, 1.000000] | [0.474405, 0.527396] | 0.009682 / 0.002025 | Y/Y/Y/N |
| C4 | 12 | 1.000000 | 0.994271 | 0.500000 | [0.002083, 0.009375] | [0.469792, 0.519271] | [0.989286, 0.997619] | [0.400595, 0.455952] | 0.012252 / 0.002025 | Y/Y/Y/N |
| C4 | 20 | 1.000000 | 0.986979 | 0.421875 | [0.006771, 0.020312] | [0.544792, 0.585417] | [0.976786, 0.992262] | [0.314881, 0.363690] | 0.013853 / 0.002025 | Y/Y/Y/N |
| C4 | 28 | 0.999479 | 0.971354 | 0.404688 | [0.021875, 0.034388] | [0.544792, 0.589583] | [0.960562, 0.974985] | [0.297024, 0.341667] | 0.009274 / 0.002025 | Y/Y/Y/N |
| C4 | 36 | 0.997396 | 0.941667 | 0.406771 | [0.047396, 0.064583] | [0.510417, 0.558854] | [0.926014, 0.945574] | [0.293727, 0.351464] | 0.004165 / 0.002025 | N/Y/Y/N |
| C5 | 4 | 1.000000 | 0.998437 | 0.536458 | [0.000000, 0.004687] | [0.434375, 0.489062] | [0.994643, 1.000000] | [0.439286, 0.502381] | 0.007902 / 0.001334 | Y/Y/Y/N |
| C5 | 12 | 1.000000 | 0.995313 | 0.491667 | [0.002083, 0.007812] | [0.480729, 0.528646] | [0.991071, 0.997619] | [0.388690, 0.446429] | 0.013659 / 0.001334 | Y/Y/Y/N |
| C5 | 20 | 1.000000 | 0.985938 | 0.437500 | [0.008854, 0.020312] | [0.523958, 0.573958] | [0.976786, 0.989881] | [0.328571, 0.385119] | 0.009000 / 0.001334 | Y/Y/Y/N |
| C5 | 28 | 0.998437 | 0.963542 | 0.450521 | [0.026563, 0.043229] | [0.495312, 0.531250] | [0.950448, 0.969570] | [0.347852, 0.397497] | 0.007026 / 0.001334 | Y/Y/Y/N |
| C5 | 36 | 0.994792 | 0.951042 | 0.448437 | [0.035937, 0.051563] | [0.480208, 0.525000] | [0.940433, 0.958732] | [0.348739, 0.394012] | 0.002660 / 0.001334 | N/Y/Y/N |

At Block 36, BF16 projection preservation fails in both panels because the
exact \(D_{proj}\) upper bounds are `0.06458333333333333` for C4 and
`0.05156250000000007` for C5, exceeding 0.05. Their \(R_Z\) lower bounds remain
above 0.90. No confirmation cell has \(D_{proj}\) lower 95% at or above 0.10, so
the separate Gate-projection-bottleneck verdict receives `0/5` blocks.

### 7.2 FP32 sensitivity matrix

| Panel | Block | BA(H) | BA(Z) | BA(Q) | \(D_{proj}\) 95% CI | \(D_{select}\) 95% CI | \(R_Z\) 95% CI | \(R_Q\) 95% CI | \(I_Q/H(Y)\) / null | P/S/A/N |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- |
| C4 | 4 | 1.000000 | 0.998958 | 0.554167 | [0.000000, 0.002604] | [0.421875, 0.467708] | [0.997024, 1.000000] | [0.464286, 0.516667] | 0.009578 / 0.002043 | Y/Y/Y/N |
| C4 | 12 | 1.000000 | 0.995312 | 0.496875 | [0.001562, 0.008333] | [0.473437, 0.523438] | [0.990476, 0.998214] | [0.396429, 0.452976] | 0.012107 / 0.002043 | Y/Y/Y/N |
| C4 | 20 | 1.000000 | 0.986979 | 0.421354 | [0.007292, 0.019792] | [0.545313, 0.584896] | [0.977381, 0.991667] | [0.314881, 0.364286] | 0.013489 / 0.002043 | Y/Y/Y/N |
| C4 | 28 | 0.999479 | 0.975521 | 0.411979 | [0.017188, 0.030729] | [0.541146, 0.585938] | [0.964839, 0.980322] | [0.305534, 0.350417] | 0.009223 / 0.002043 | Y/Y/Y/N |
| C4 | 36 | 0.997396 | 0.942708 | 0.406250 | [0.046354, 0.063542] | [0.509896, 0.563542] | [0.927250, 0.946771] | [0.292115, 0.351254] | 0.004420 / 0.002043 | N/Y/Y/N |
| C5 | 4 | 1.000000 | 0.998437 | 0.532292 | [0.000000, 0.004687] | [0.439583, 0.492708] | [0.994643, 1.000000] | [0.435104, 0.496429] | 0.007472 / 0.001319 | Y/Y/Y/N |
| C5 | 12 | 1.000000 | 0.995833 | 0.495313 | [0.002083, 0.006771] | [0.476042, 0.526563] | [0.992262, 0.997619] | [0.392857, 0.451190] | 0.013629 / 0.001319 | Y/Y/Y/N |
| C5 | 20 | 1.000000 | 0.984375 | 0.439583 | [0.009896, 0.021875] | [0.521354, 0.568750] | [0.975000, 0.988690] | [0.330952, 0.387500] | 0.008680 / 0.001319 | Y/Y/Y/N |
| C5 | 28 | 0.998437 | 0.966146 | 0.448958 | [0.025000, 0.039583] | [0.496354, 0.538542] | [0.954653, 0.971395] | [0.344253, 0.397260] | 0.007118 / 0.001319 | Y/Y/Y/N |
| C5 | 36 | 0.994792 | 0.955208 | 0.454687 | [0.032292, 0.047396] | [0.477604, 0.522396] | [0.945542, 0.962941] | [0.355262, 0.402753] | 0.002739 / 0.001319 | Y/Y/Y/N |

FP32 C5 Block 36 individually passes projection preservation, but C4 Block 36
does not; the registered cross-panel block condition therefore remains false.
All other confirmation-block criteria and the line verdict match BF16.

Across all 10 confirmation panel/block cells, exact BF16/FP32 top-8 set
agreement ranges from `0.9322916666666666` to `0.9890625`, and mean top-8
Jaccard overlap ranges from `0.9849537037037038` to
`0.9975694444444445`. These are sensitivity diagnostics with no registered
pass threshold; only qualitative line-verdict agreement is decision-bearing.

### 7.3 Null audit

The BF16 label-null ledger is directly replayable from its saved 1,000 draws:

| Panel | Confirmation blocks | Excluded pilot | Hidden BA max-layer q97.5 | Route \(I_Q/H(Y)\) max-layer q97.5 |
| --- | --- | ---: | ---: | ---: |
| C4 | 4, 12, 20, 28, 36 | 44 | 0.17135416666666664 | 0.0020251259956450686 |
| C5 | 4, 12, 20, 28, 36 | 44 | 0.17500000000000002 | 0.001333742479409657 |

All ten BF16 hidden BA values and all ten route-association values exceed their
matched thresholds. FP32 retains the same hidden thresholds and persists
route thresholds `0.00204255938905683` for C4 and
`0.0013189106891177025` for C5; all ten FP32 route values exceed them. The
separate FP32 raw draw arrays are not persisted, so those two percentiles can
be checked for use and internal consistency but not independently regenerated
from a dedicated FP32 draw ledger.

### 7.4 Block 44 pilot

Block 44 is shown for context only. Applying the criteria descriptively does
not make it confirmatory.

| Path | Panel | BA(H) | BA(Z) | BA(Q) | \(D_{select}\) 95% CI | \(R_Q\) 95% CI | \(I_Q/H(Y)\) / null | Status |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| BF16 | C4 | 1.000000 | 1.000000 | 0.892188 | [0.095833, 0.120313] | [0.862500, 0.890476] | 0.117319 / 0.002025 | `PILOT_NOT_BLIND` |
| BF16 | C5 | 1.000000 | 1.000000 | 0.868750 | [0.115625, 0.146354] | [0.832738, 0.867857] | 0.102503 / 0.001334 | `PILOT_NOT_BLIND` |
| FP32 | C4 | 1.000000 | 1.000000 | 0.891146 | [0.096354, 0.121875] | [0.860714, 0.889881] | 0.117002 / 0.002043 | `PILOT_NOT_BLIND` |
| FP32 | C5 | 1.000000 | 1.000000 | 0.870313 | [0.114583, 0.144271] | [0.835119, 0.869048] | 0.102120 / 0.001319 | `PILOT_NOT_BLIND` |

The pilot exists in cell-level ledgers but is absent from confirmation-layer
counts, cross-panel verdict booleans, and the final line verdict.

### 7.5 NLL calibration guard

NLL is reported exactly as registered but cannot replace or rescue the BA
verdict. Values below are the BF16 primary path.

| Panel | Block | NLL(H) | NLL(Z) | NLL(Q) |
| --- | ---: | ---: | ---: | ---: |
| C4 | 4 | 0.001906959 | 0.020596144 | 1.283606214 |
| C4 | 12 | 0.001244049 | 0.025736623 | 1.361428358 |
| C4 | 20 | 0.002314971 | 0.056142509 | 1.554946263 |
| C4 | 28 | 0.006553639 | 0.086772247 | 1.615884544 |
| C4 | 36 | 0.011424820 | 0.179429562 | 1.668522710 |
| C4 | 44 | 0.000096621 | 0.002505826 | 0.338933974 |
| C5 | 4 | 0.001967673 | 0.018063366 | 1.380160052 |
| C5 | 12 | 0.001657446 | 0.021509059 | 1.389120686 |
| C5 | 20 | 0.003732141 | 0.050854986 | 1.552699319 |
| C5 | 28 | 0.008232506 | 0.100418638 | 1.523356257 |
| C5 | 36 | 0.014414658 | 0.174111725 | 1.502030877 |
| C5 | 44 | 0.000217230 | 0.002775679 | 0.404744602 |

### 7.6 Exact ledger counts and validity

- `layer_metrics.csv`: 12 rows = 2 panels × 6 blocks.
- `fp32_sensitivity_layer_metrics.json`: 12 rows.
- `predictions.csv.gz`: 69,120 rows = 2 panels × 6 blocks × 3 feature
  objects × 1,920 examples.
- Every `(panel, block, feature)` prediction cell has exactly 1,920 rows and
  1,920 unique `row_index` values; each A→B or B→A direction has 960 rows.
- Every prediction row has `numeric_path=BF16_PRIMARY`.
- BF16 parent probes: 72 outer fits, all converged; 72 train-only model
  selections, all converged; 2,520 C-by-fold fits, all converged.
- Bootstrap ledger: 12 panel/block cells; 10,000 draws for each of BA(H),
  BA(Z), BA(Q), projection, selection, total, \(R_Z\), and \(R_Q\); all
  denominators positive.
- Null ledger: 1,000 draws for each panel's hidden and route max-layer null.
- Conditional-fine ledger: 288 rows = 2 panels × 6 blocks × 8 parents × 3
  feature objects; secondary only.
- Figure set: three E01H figures, each producer-hashed and manually inspected.
- Qwen completion audit: 12 required artifacts, all 12 recomputed SHA-256
  values match.

## 8. Visualization Results

All three local copies were manually inspected after producer-hash comparison.

### 8.1 Where accessibility changes along \(H\rightarrow Z\rightarrow Q\)

![Held-out parent balanced-accuracy ladder](figures/balanced_accuracy_ladder.png)

- **Anchor / Protocol question:** where is eight-parent accessibility lost in
  the exact native chain?
- **Metric and unit:** held-out balanced accuracy, a fraction averaged over
  eight parent recalls; dotted reference is chance 0.125.
- **Raw source:** `layer_metrics.csv`; lineage rows for hidden admission,
  projection preservation, and selection loss.
- **Aggregation / uncertainty:** A→B and B→A combined out-of-fold predictions;
  paired 10,000-draw complete-family bootstrap 95% intervals.
- **Axes / legend:** x is one-based Qwen block; y is BA; black/blue/red are
  H/Z/Q; panels are C4/C5; gray Block 44 is `PILOT_NOT_BLIND`.
- **Observed:** H and Z stay near 1.0 at confirmation blocks, while Q is
  0.404688--0.563542.
- **Allowed conclusion:** supervised parent accessibility is largely retained
  to Z and materially lower in Q on the registered readout.
- **Limitation:** the plot cannot establish native causal use, expert utility,
  or language-model loss.

### 8.2 Whether loss is at Gate projection or top-8 selection

![Projection and top-8 selection gaps](figures/accessibility_gaps.png)

- **Metric and unit:** paired \(D_{proj}\) and \(D_{select}\) in BA fraction.
- **Source / uncertainty:** same paired predictions and family-bootstrap 95%
  intervals as the primary table.
- **Axes / legend:** x is one-based block; y is paired BA gap; blue is H→Z,
  red is Z→Q; C4/C5 are separate; Block 44 is gray pilot.
- **Observed:** selection gaps dominate at every confirmation block; Block 36
  is the only block whose joint strict projection-preservation condition fails.
- **Allowed conclusion:** the registered practical loss is concentrated at
  the top-8 interface rather than meeting the separate Gate-projection-
  bottleneck rule.
- **Limitation:** the horizontal 0.05 and 0.10 decision thresholds are not
  drawn as reference lines, so the numeric table and ledger—not visual bar
  inspection—own the criterion decisions.

### 8.3 Descriptive parent-by-expert route association

![Native top-8 parent-by-expert route heat maps](figures/parent_expert_load_heatmaps.png)

- **Metric and unit:** mean native renormalized top-8 route weight, probability
  mass, for each parent/expert pair.
- **Raw source:** native Q features; panel/block labels from
  `layer_metrics.csv`.
- **Aggregation / uncertainty:** descriptive means; no uncertainty interval or
  heat-map threshold is registered.
- **Axes / legend:** rows are eight parents, columns are 128 experts, color is
  mean route mass; top/bottom are C4/C5; Block 44 remains pilot-labeled.
- **Observed:** load is concentrated on a small set of experts and varies with
  parent and depth; the formal association admission comes from \(I_Q/H(Y)\)
  against the matched null, not visual clustering.
- **Allowed conclusion:** Q carries descriptive parent-associated routing
  structure at the registered blocks.
- **Limitation:** association does not show that selected experts are useful,
  that Gate behavior is causally semantic, or that routing improves LM loss.
- **Cosmetic contract limitation:** the completion audit says Block 44 has a
  gray background, but the current heat-map rendering covers that background
  with the image layer; the panel remains text-labeled `PILOT_NOT_BLIND`. This
  visual-only mismatch does not affect any metric, exclusion, or verdict, and
  the figure is not redrawn in this documentation repair.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| Stage 0: provenance / resource | hashes, block mapping, Gate payloads, four H100s | passed | none | wrong inputs, off-by-one layer mapping, wrong resource | frozen observational scope |
| Stage 1: label-blind smoke | top-8 count, row sums, synthetic BF16/FP32 sensitivity | passed | none | basic reconstruction error | real-data sensitivity |
| Stage 2: held-out prediction | exact rows and convergence | passed | none | row duplication/drop, test-label model choice, nonconvergence | finite-sample readout dependence |
| Stage 3: uncertainty / null | bootstrap and null draw ledgers | passed | none | wrong independence unit, pilot in max-layer scan | empirical rather than population thresholds |
| Stage 3: hidden admission | all H cells above null | passed | none | inaccessible primary label under registered probe | other labels and nonlinear probes |
| Stage 3: Gate preservation | 4/5 joint blocks | mixed by design | Block 36 exceeds strict gap-upper threshold | universal perfect projection preservation | modest deeper projection degradation |
| Stage 3: selection loss | 5/5 joint blocks | passed | none | no-material-bottleneck rival | why the native top-8 discards readout access |
| Stage 3: route association | 5/5 joint blocks | passed | none | complete label-independence of Q under registered null | causal use and expert utility |
| Stage 3: FP32 sensitivity | same line verdict | passed | none | numeric-path verdict reversal | near-tie expert identities |
| Stage 4: render / hash closure | three figures and 12 Qwen artifacts | passed | none | missing decision artifacts | no Git commit identity |

**Falsified physical prior:** none. The advisor's progressive residual-growth
prior is not tested by E01H.

**Falsified mathematical model:** the no-material-access-bottleneck rival is
rejected under the registered readout. The Gate-projection-bottleneck rival is
also not met.

**Falsified operationalization / proxy:** none of the required primary
operationalizations failed. The result does show why native route association
must not be substituted for utility.

**Falsified implementation:** none; all required guards pass.

**Falsified metric:** none. NLL remains a guard rather than a post-result
replacement.

**Remaining rival explanations:** external parent labels may align with route
load correlations without causing dispatch; a nonlinear readout may expose a
different accessibility profile; the controlled templates may overstate
readability; selected experts may be useful, harmful, or tied despite the
association; checkpoint, label taxonomy, and layer choice may not generalize.

## 10. Full Experiment Record

- Protocol frozen: 2026-08-29T15:34:00Z.
- Submission receipt:
  `runs/submit-h100-4-reserved-20260829T172910Z.txt`.
- ACP job: `pt-vkikyszj`; a final read-only scheduler query reported terminal
  state `SUCCEEDED`; retry count configured as zero. The scheduler describe
  response was not persisted as a run receipt.
- Final canonical run: `full-20260829T172910Z`.
- H100 assignment: Blocks 4/12/20/28/36/44 rotate over device indices
  0/1/2/3/0/1.
- Primary bootstrap: seed 151101, 10,000 draws, 30 complete families per draw.
- Label null: seed 151102, 1,000 draws, max over Blocks 4/12/20/28/36.
- Prediction rows: 69,120; missing or replaced rows: zero.
- Primary metric rows: 12 BF16; FP32 sensitivity rows: 12.
- Secondary conditional-fine rows: 288.
- Test record: 86 passed, 1 skipped in CPU-sharded suite; 1 dedicated CUDA
  regression passed.
- Completion: Qwen audit passed; global audit passed and preserved separate
  Qwen-accessibility and E03 mechanism/utility verdicts.
- Canonical-source rule: all numbers in this document come from
  `full-20260829T172910Z`; the earlier noncanonical run is excluded.

## 11. Interpretation

The result supports a specific interface diagnosis. A fixed linear map cannot
create new linear separability; the near-equality of H and Z therefore says
that the frozen Gate row space retains most of the parent-label readout already
available in H at four of five confirmation blocks. It does not say that the
Gate was trained to recover the external taxonomy.

The large Z-to-Q gaps are different. Top-8 makes a discrete, sparse interface,
and the registered linear readout loses roughly 0.43--0.57 BA through that
operation. Yet the route-mass mutual information remains above a max-layer
label null, so Q is neither a near-total preservation of H accessibility nor a
label-independent route. This joint pattern is exactly why the typed verdict
includes both “selection bottleneck” and “retained association.”

Block 36 prevents a stronger claim that Gate projection is uniformly
negligible. Its BF16 projection-gap upper bounds exceed 0.05 in both panels,
and FP32 C4 also fails. However, no block approaches the registered
Gate-projection-bottleneck lower-bound rule, so the evidence does not support
renaming the whole line as a Gate projection failure.

Most importantly, neither BA nor mutual information evaluates the outcomes of
dispatching to alternative experts. Counterfactual expert utility and
language-model loss remain wholly unmeasured. E01H therefore cannot validate
the synthetic common→residual→1→2→4 mechanism or any proposed Router training
benefit.

The resource lane has a separate ownership boundary. E01H was created after a
shared execution surface was concurrently changed to an 8×RTX5090 contract;
its H100-only successor preserves the scientific estimand but is not the
execution named by the current 5090 Focus. The researcher accepted this record
only as collision-isolated non-owning sensitivity evidence under that Focus;
it neither rewrites nor closes the 5090 execution contract.

## 12. Claim Boundary

### Can claim

- the registered BF16 and FP32 analyses agree on the typed accessibility
  profile for this checkpoint, dataset, readout family, and fixed layers;
- the Gate projection preserves the registered parent accessibility at four of
  five confirmation blocks in both panels;
- the top-8 operation produces material held-out accessibility loss at all five
  blocks, while the resulting route retains parent-label association above its
  matched null at all five;
- Block 36 shows enough projection loss to fail the strict preservation rule,
  but `0/5` blocks meet the separate Gate-projection-bottleneck lower-bound
  rule.

### Cannot claim

- that the native Router causally uses parent semantics rather than carrying a
  correlated route pattern;
- that the selected experts are counterfactually useful or functionally
  appropriate;
- that this routing improves Qwen prediction, language-model NLL, training
  efficiency, or sample efficiency;
- that Qwen pretraining produced the pattern through the proposed A15_11
  gradient mechanism;
- that C4/C5 are independent replications or that the result generalizes to
  other checkpoints, datasets, labels, or probe families;
- that E01H completes the current 8×RTX5090 synthetic/Qwen Focus or authorizes
  a Router intervention.

## 13. Next Decision

**Decision:** E01H is admitted as non-owning H100 sensitivity evidence. The
sole A15_11 next decision is to freeze a frequency (high/low) by cross-child
gradient-consistency (high/low) representation-formation test before another
Router intervention.

**Completion criterion:** the successor contract holds total tokens, target
positions, parent/child counts, vocabulary, templates, and label entropy fixed
and defines frozen measurements for gradient consistency, parent between-class
energy, held-out fifth-percentile normalized margin, and discriminant-subspace
spectral location.

**Resume action:** retain E01H only under the non-owning sensitivity label and
use the current Focus/Anchor to design the \(2\times2\) successor. Do not create a
second E01H decision, reinterpret accessibility as utility, or launch a Qwen
intervention before a new confirmed Anchor and Protocol.

## 14. Artifact Manifest

Every Qwen producer hash below was independently recomputed against the final
canonical files. The Qwen completion audit canonical-payload SHA-256 is
`e14a2d848ea4056af93bf73c1f912643944c119dcf77933533bb8a2512c5521c`.

| Artifact | Purpose | Producer / revision | Source inputs | SHA-256 / identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frozen E01H Protocol | scientific contract | execution-time file | Anchor and approved H100 successor scope | `d9d6468a5fca75b274983e0b907c6d34a0db6b39e44ee1ad7e02ca16d0bd6601` | yes | yes | no post-start scientific amendment |
| `code_receipt.json` | analysis-producer file identity | global pre-run receipt | Protocols and analysis scripts | `1bed5c7e254e4679606ed9d03c6954859e7927c71944b47bc2e9d6ba0d8216df` | limited | yes, bounded | worker has no Git commit; runner and submitter execution-time hashes are absent |
| [smoke receipt](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/smoke/qwen/smoke_receipt.json) | label-blind numeric smoke gate | `qwen_audit.py` smoke mode | synthetic inputs only | `8cac6f6bfc9b8323c0fd945d017c6e267728db3f956964dce9f655ae3a4c50e8` | yes | guard | records no scientific input read and no scientific metric produced |
| [CPU test log](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/logs/tests.log) | implementation test gate | pytest shard | worker code | `d728245af6a85289055bff401a93afb5eff61d414683cf81d1c82bf1c5ef00ad` | yes | guard | 86 passed, 1 skipped |
| [CUDA regression log](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/logs/cuda_regression.log) | GPU numeric regression gate | dedicated pytest item | worker code and CUDA | `bca578e979facf4e637beb4cee9a8304a6abdfb9abb6fc61370af4612719b8c9` | yes | guard | 1 passed |
| [submission receipt](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/submit-h100-4-reserved-20260829T172910Z.txt) | submission identity | submitter stdout | ACP submission | `667aeb4aaa866272e8040d2670e5a810a221661c790a5a5c67beee5f28dc703f` | limited | provenance | contains only job ID; no worker spec, quota, command, or terminal state |
| ACP scheduler describe receipt | reserved-resource and terminal-state provenance | ACP scheduler | job `pt-vkikyszj` | `MISSING_PERSISTED_RECEIPT` | no | provenance limited | final read-only audit observed `SUCCEEDED`, `n6ls.iu.i40.4`, one replica, and reserved quota, but did not persist the response |
| Runner / submitter execution identity | orchestration provenance | execution-time receipt | `scripts/run_pipeline.sh`, `scripts/submit_h100_4_reserved.sh` | `MISSING_EXECUTION_TIME_HASHES` | no | provenance limited | current files are linked below, but their executed revisions are not established by `code_receipt.json` |
| H BF16 identity guard | check Protocol H object against the stored producer H path | independent final-audit recomputation, not producer output | both frozen activation arrays | `47,185,920 values; 0 BF16 round-trip mismatches; NO_PERSISTED_PRODUCER_RECEIPT` | limited | bounded support | establishes value identity in the final audit, not execution-time provenance |
| `qwen/preflight.json` | frozen-input/resource gate | `preflight.py` / `qwen_contract.py` | inputs, checkpoint, Gate tensors, devices | `7f093850b76479524f5fbe41471bd54da782829f3ad08a774b51979e5506d24d` | yes | yes | all checks pass |
| `qwen/feature_manifest.json` | H/Z/Q numeric construction and sensitivity | `qwen_audit.py` | activations and Gate tensors | `f5c562b7570c8c4adc91ad296e1ffb6bd6b753eb673a8b169776811c85c29ea8` | yes | yes | records device rotation |
| `qwen/predictions.csv.gz` | sample-level held-out parent predictions | `qwen_audit.py` | H/Z/Q and cross-fit probes | `0cb2245f948ef13f398e0157ce3ef8a88548aa995308b86e3587937db34d457b` | yes | yes | 69,120 rows |
| `qwen/layer_metrics.csv` | full BF16 cell metrics and fit ledgers | `qwen_audit.py` | predictions, route loads, bootstrap/null | `e638e14c4bfba41d55ac6d8ee113b4650abaee0e1d5eab87eab162edb0dfc231` | yes | yes | 12 rows; large embedded diagnostic fields |
| `qwen/bootstrap_ledger.json` | paired uncertainty and criterion booleans | `qwen_audit.py` | predictions and family IDs | `4535a23a83487d249f2bfa9f49b9cce171493e281102be93b00e4fae3e819e9d` | yes | yes | 10,000 draws/cell |
| `qwen/null_ledger.json` | primary hidden/route label null | `qwen_audit.py` | frozen predictions and Q loads | `0a19a92ce9b7edddc61fd49d5576d0c8285dc08b0f4942f39debf00e78bef378` | yes | yes | 1,000 draws/panel |
| `qwen/fp32_sensitivity_layer_metrics.json` | FP32 qualitative stability | `qwen_audit.py` | FP32 H/Z/Q | `34a5af79af6d9659c7b5d27e54f8e5fd8affbefccba5ddefdd5088ee3189df9f` | limited | sensitivity | 12 rows and persisted verdict inputs; no separate FP32 raw-null draw ledger for direct percentile replay |
| `qwen/conditional_fine_ledger.json` | parent-conditional child diagnostic | `qwen_audit.py` | H/Z/Q, child labels within parent | `44f88b9cd90e7f0edc24dcae493dd1aa0497a0b0d2b66e7bb3906f73d0cb7c83` | yes | secondary only | 288 rows; cannot affect primary |
| `qwen/results.json` | typed Qwen verdict and thresholds | `qwen_audit.py` | all primary ledgers | `0bc5b14109a1284b20635b086e4fb0dd66feb988eaeae1bce068cfa717d4afdb` | yes | yes | machine verdict source |
| `qwen/completion_audit.json` | producer hash / figure closure | `qwen_audit.py` | 12 Qwen artifacts | `cd7f90b3b64fbbc6f7c0005f8b1a9293ff08ff74531cf944b3c88fadf895470a` | yes | yes | all artifact hashes match |
| Global `completion_audit.json` | separated E01H/E03 run closure | `completion_audit.py` | Qwen and E03 artifacts | `acafbbc3ba496fd8424cae5e2841cea3b250718971b3c10b56535833913e9d38` | yes | provenance | does not merge scientific verdicts |
| Balanced-accuracy figure | access-chain location | `qwen_audit.py` | `layer_metrics.csv` | `e23320b010b67cfdac55fcab4e7abcac903f44d11505dbf37c23f84cd2262bb9` | yes | yes | local copy hash matches |
| Accessibility-gap figure | projection versus selection | `qwen_audit.py` | `layer_metrics.csv` | `f5d9668d3e5a82ca4956b9b9e1d0f91f59c37656f760c16539da3ba49023bb28` | yes | yes | local copy hash matches |
| Parent-expert heat maps | descriptive route association | `qwen_audit.py` | native Q route loads | `7a96cd96ce634e2f77178a5e586a27c16ee97400863c1bbe485eac292b5d45af` | limited | diagnostic | local copy hash matches; Block 44 is labeled but its contracted gray background is not visually realized |
| Local curated primary table | short canonical reading table | copied/curated from final BF16 rows | final `layer_metrics.csv` | `554999d753c88b809a902efce8b14f5e1405e9758b7df787b50decec0c175c76` | limited | yes | ten cells differ from the Detailed six-decimal display by `0.000001`; raw owns full precision and verdicts |

The six loaded Gate tensor payload hashes are:

| Block | Gate tensor SHA-256 |
| ---: | --- |
| 4 | `dc4f558c07513e45629e33936f7b01aa02cbed9fb45f5abec488d1948bdb31e3` |
| 12 | `80a517bd484ce86f2ecfaab14b9b939a89e4451146efb7eb0f68c1d579a49ff6` |
| 20 | `29c28f809e9293c29f03e293f311c14420204024521579ece0186175cb73560c` |
| 28 | `a37ac22bf3c84eb066ac71f95096918c843b7c3c0580d02bdcb65a78212ecbe9` |
| 36 | `68bb7a65e9195508084ecae20b3ed7613ccbdcca1a9272cf5842bbd1e5fd8a46` |
| 44 | `5e23d4b713cf5b19d4e681c36b465c494d589a2d1dd5f5e5e9d9f3fde8648d33` |

The immutable source hashes are:

| Source | SHA-256 |
| --- | --- |
| `c4_activations.npy` | `c1748f785e4563689f52cb94951861dbb994d6437f559baeb1a3306e34d43107` |
| `c5_activations.npy` | `cf68c95288306386d1b82bed0ca64066af0073873f41aa278da9cd86010a2422` |
| `c4_metadata.jsonl` | `a94a2f59655fd152953f8a2e0086bc69a4f15bb2886a2a15b93eb83fca888ad9` |
| `c5_metadata.jsonl` | `4708b9e655d6152102f9d58f363d947ef4ced1c74658b7078bc0988d01f1bc52` |
| `split_manifest.json` | `e815b6acf13774ed438186bb86ab9233898a7fdfbcb409c7f4b517f2daa25773` |
| `extraction_manifest.json` | `09716a299db3decbd12086799ef90c15ec0ded18d40065b27bbf72bd08cc1282` |
| checkpoint `config.json` | `2850ddb3bf7aecad20b611e2d44f3077fc8193f4827c93beddd4c02ad63c2297` |
| checkpoint safetensors index | `df0d481ec595c55a0ba58426d517390c6214a566ec4ff1c8fc4bbce9f57b3c24` |

## 15. Links

- Anchor:
  [A15_11](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md)
- Frozen Protocol: [protocol.md](protocol.md)
- Summary: [summary.md](summary.md)
- Current owning 5090 Focus:
  [focus_gradient_consistent_hierarchical_routing.md](../../../../focus/focus_gradient_consistent_hierarchical_routing.md)
- Code workspace:
  `/data/250010109/MoE_Router/experiments/20260829_a15_11_h100_closure`
- Runner:
  [scripts/run_pipeline.sh](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/scripts/run_pipeline.sh)
- Submitter:
  [scripts/submit_h100_4_reserved.sh](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/scripts/submit_h100_4_reserved.sh)
- Qwen producer:
  [qwen_audit.py](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/qwen_audit.py)
- Qwen contract:
  [qwen_contract.py](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/qwen_contract.py)
- Canonical run:
  [full-20260829T172910Z](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/)
- Qwen result root:
  [qwen/](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/qwen/)
- Logs:
  [logs/](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/full-20260829T172910Z/logs/)
- Submission receipt:
  [submit-h100-4-reserved-20260829T172910Z.txt](../../../../../../../../MoE_Router/experiments/20260829_a15_11_h100_closure/runs/submit-h100-4-reserved-20260829T172910Z.txt)
- Reproduction entry point: set `MODE=full`, `RUN_STAMP` to a fresh unique
  stamp, `EXPECTED_GPUS=4`, and run `scripts/run_pipeline.sh` under the frozen
  file hashes and reserved-H100 contract; the runner refuses to overwrite an
  existing run directory.

## 16. Final Audit

| Audit item | Status |
| --- | --- |
| Researcher supplied the initial judgment, or the document remains scaffolded | PASS — the researcher accepted the bounded result, claim boundary, non-owning H100 label, and the single upstream next decision |
| Frozen Protocol revision and approved execution scope are identified | PASS |
| Frozen Protocol contains the required active-Focus link, A-G confirmation ledger, full stage contract, cross-block consistency result, and pre-execution Final Audit | **FAIL** — these records are absent from the frozen Protocol; this post-run document does not retroactively repair them |
| Conformance, retry exclusion, warning, and bounded code-identity deviation are recorded before interpretation | LIMITED — scientific conformance is recorded, but scheduler describe and runner/submitter execution identity are not persisted |
| Every primary result is eligible or explicitly excluded/secondary | PASS within the frozen E01H Protocol; E01H remains non-owning H100 sensitivity evidence |
| Every decision-bearing number traces to a raw artifact, estimator, uncertainty rule, criterion, and verdict | LIMITED — BF16 primary lineage is complete; FP32 route-null percentiles lack a separate raw-draw ledger |
| Observation, derived statistic, interpretation, claim, and boundary remain separate | PASS |
| Summary is conclusion-first and links the curated primary table and raw ledgers | PASS |
| Detailed is the only complete E01H evidence ledger | **FAIL** — existing smoke/test/submission artifacts are now indexed, but the persisted scheduler describe receipt, runner/submitter execution-time hashes, producer H identity receipt, and FP32 raw-null ledger remain absent |
| All three figures state source, aggregation, observed result, allowed conclusion, and limitation | LIMITED — the heat map is correctly pilot-labeled, but its contracted Block 44 gray background is not visually realized |
| Summary, Detailed, and the owning Anchor use the same verdict and boundary | PASS — the Anchor records E01H only as non-owning sensitivity and preserves the accessibility-versus-utility boundary |
| Block 44 pilot and conditional-fine diagnostic cannot alter the primary verdict | PASS |
| E01H does not impersonate, update, or close the separately owned RTX-5090 Focus | PASS |
| E01H records only one non-owning admission decision and creates no second mainline next decision | PASS |
| No missing value, expected pattern, filename, or cosmetic rendering claim is used as scientific evidence | PASS |
| Active Focus contains the human-confirmed result before any E01H daily report is drafted | PASS — the Focus accepts E01H only as collision-isolated sensitivity, not as its 5090 execution |
| Any E01H daily report preserves canonical eligibility, verdict, lineage, boundary, and next decision | PASS for the current AI draft; human audit of the complete story remains required before cycle closure |
