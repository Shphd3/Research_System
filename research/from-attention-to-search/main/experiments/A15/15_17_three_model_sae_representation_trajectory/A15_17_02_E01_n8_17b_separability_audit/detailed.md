# Detailed: A15_17_02_E01 Exact-17B N8 Native Separability Audit

Primary Anchor: [A15_17_02 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_02_sae_n8_separability_anchor.md)  
Frozen Protocol and registered revision: [Protocol](protocol.md), Amendment A2  
Summary: [summary.md](summary.md), `DRAFT_AWAITING_RESEARCHER_JUDGMENT`; Chinese companion [summary_cn.md](summary_cn.md)  
Result eligibility: `ELIGIBLE` for the registered checkpoint-conditional N8 comparison

## 0. Quick Recap

Purpose: test whether SAE-associated native representation concentration is
accompanied by stronger N8 domain readability at exact 17B.  
Hypothesis: fresh coefficient-0.1 S7 is more linearly readable than Dense; the
strongest rival is that SAE history changes concentration without improving
domain distinctions.  
Experiment logic: compare Dense, fresh S7 0.1 and reweighted S7 1→0.1 on the
same N8 fit/dev/test records and native layer-8 write; use linear test accuracy
as primary evidence and geometry/K-means as explanatory evidence.  
Direct result: Dense/fresh/reweighted body-mean accuracies are
`87.1875% / 88.6250% / 73.6875%`. Fresh−Dense is `+1.4375` percentage points
with registered 97.5% interval `[−0.1250,+2.9375]`; reweighted−fresh is
`−14.9375` points with `[−17.5000,−12.5000]`.  
Eligibility: all three model roles, 4,800 records/role, identity, alignment,
immutability, finite-value, analysis, artifact and terminal gates pass.  
Registered typed reading: primary H1 `INSUFFICIENT`; history contrast
`REWEIGHTED_LOWER_THAN_FRESH`.  
Human mechanism judgment: `AWAITING_RESEARCHER`.  
Claim boundary: the result concerns three fixed training histories, N8 source
categories and frozen representation readers; it does not establish causality,
model use, broad semantics, language-model quality or training efficiency.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| Native write | Attention contribution entering the residual stream | block index 7 output after output projection, before residual addition | 1,024-vector | Primary representation object | Model use or downstream utility |
| Linear readability | Domain label recoverable by a fixed simple supervised rule | fit L2 logistic reader, dev-select `C`, test accuracy | record proportion | Primary registered evidence | Causal use by the LM |
| Effective dimension | Number of covariance directions carrying appreciable variance | \((\mathrm{tr}C)^2/\mathrm{tr}(C^2)\) | dimensionless | Describes concentration | Semantic concept count or quality |
| \(B/W\) | Between-class centroid scatter divided by within-class scatter | same test matrix and labels | dimensionless | Describes centroid separation | Linear accuracy or causality |
| ARI | Agreement between label-free K-means assignments and domain labels | five fixed K-means seeds | dimensionless | Tests distance-based grouping | Supervised readability |

## 2. Anchor Link And Decision Point

The Anchor's decision is whether to retain the explanation that SAE-associated
concentration strengthens N8 domain separability, or stop using concentration
as support for that explanation. The primary contrast is fresh S7 minus Dense;
the history contrast checks whether the known concentrated reweighted state is
also more readable.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
|---|---|---|---|---|---|
| Scope | one A2-authorized full read-only run | one job, no retry | PASS | `pt-3nidnrq0` receipt | none |
| Conditions | exact-17B Dense, fresh S7, reweighted S7 | 3/3 at 17,000,000,000 tokens | PASS | resolved assets and worker manifests | none |
| Data | N8 fit/dev/test 2,400/800/1,600 | exact counts; 4,800 unique IDs, hashes and source groups | PASS | N8 files and independent audit | none |
| Split leakage | no ID/input-hash/source-group overlap | all three pairwise overlaps are zero | PASS | independent audit | none |
| Native site and pooling | layer 8 native mean primary; last sensitivity | both views complete | PASS | caches and primary metrics | none |
| State | frozen; zero optimizer updates | before/after sampled state identical for every role; zero updates | PASS | worker manifests | none |
| Primary analysis | fixed probe and two 2,000-draw paired intervals | complete with seed 20260923 | PASS | paired statistics | none |
| Explanatory analyses | geometry and five-seed K-means | all three conditions and both views complete | PASS | primary metrics and cluster predictions | none |
| Resource | one four-RTX5090 Spot node | allocated four GPUs; three extraction processes used GPUs 0–2 | DEVIATION | pod log and manifests | none; only three scientific model roles exist |
| Artifacts | predictions, metrics, failures, manifests, terminal receipt | all present; failures `[]`; terminal PASS | PASS | artifact manifest and terminal receipt | none |

Frozen Protocol revision: scientific body plus Amendments A1–A2.  
Execution approval: exactly one full run under A2.  
Retries and exclusions: none.  
Missing registered conditions: none.  
Post-hoc analyses used for verdict: none.  
Known panel boundary: N8 is a previously used fixed panel, not a newly sealed
external confirmation set.

## 4. Actual Setup

- Data: `N8_v1`, eight named M2D2 academic-source categories; 300/100/200
  records per class for fit/dev/test; 256 frozen body tokens per record.
- Models: exact-17B Dense; final-layer fresh S7 trained throughout at
  reconstruction coefficient 0.1; final-layer reweighted S7 changed from 1 to
  0.1 near 15.47B. All models have eight layers and hidden width 1,024.
- Task: predict the source category from one frozen representation vector.
- Preprocessing: fit-only mean subtraction and one global RMS scale; dev/test
  receive the frozen fit transform.
- Reader: multiclass L2 logistic regression, `lbfgs`, intercept, no class
  weights, `C=[0.01,0.1,1,10,100]`, dev selection with smaller-`C` tie break.
- Clustering: fit-only K-means with eight clusters, `n_init=20`, seeds
  `[17,29,43,71,97]`; test ARI.
- Training or optimization: none; no optimizer instantiated; zero updates.
- Execution: ACP job `pt-3nidnrq0`, `5090-4-spot`, `shphd-lite-0911`, mounted
  SM120 runtime; terminal time `2026-09-23T01:30:33.733903Z`.

Held fixed are training-token coordinate, data records, token order, masks,
native site, pooling, reader family, selection rule and statistics. Training
history is not strictly isolated: known microbatch, CE chunking and stochastic
differences remain between model lineages.

## 5. Metrics And Registered Decision Rules

The primary quantity is test accuracy on native layer-8 body-mean vectors. Two
contrasts use class-stratified paired bootstrap intervals over the same 1,600
test records. Because two directional contrasts were registered, a direction
requires the 97.5% interval to lie wholly above or below zero. Crossing zero is
`INSUFFICIENT`, not equivalence. Geometry and ARI cannot rescue a primary
interval that crosses zero.

## 6. Evidence Lineage

| Decision | Registered criterion | Raw artifact | Computation | Observed value | Eligibility | Typed reading | Limitation |
|---|---|---|---|---|---|---|---|
| Fresh improves on Dense | 97.5% interval for fresh−Dense wholly above zero | test predictions | paired class-stratified bootstrap, 2,000 draws | `+1.4375` pp; `[−0.1250,+2.9375]` | ELIGIBLE | INSUFFICIENT | checkpoint/data conditional |
| Reweighted differs from fresh | 97.5% interval for reweighted−fresh excludes zero | test predictions | same bootstrap | `−14.9375` pp; `[−17.5000,−12.5000]` | ELIGIBLE | REWEIGHTED_LOWER | not an isolated coefficient intervention |
| Reweighted is more concentrated | lower effective dimension and higher top-16 share | test native means | covariance geometry | \(d_\mathrm{eff}\) `7.4958` vs `20.7354`; Q16 `0.7929` vs `0.5496` | ELIGIBLE explanatory | OBSERVED | no uncertainty interval; not quality by itself |
| Distance grouping | higher test ARI after fit-only K-means | cluster predictions | mean across five pre-fixed seeds | Dense/fresh/reweighted `0.3806/0.4328/0.1220` | ELIGIBLE explanatory | REWEIGHTED_LOWEST | ARI cannot replace primary metric |

## 7. Main Results

### 7.1 Primary native body-mean readout

| Condition | Selected C | Test accuracy | Effective dimension | Q16 | B/W | K-means ARI mean |
|---|---:|---:|---:|---:|---:|---:|
| Dense | 0.01 | 87.1875% | 13.7074 | 0.6356 | 0.4425 | 0.3806 |
| fresh S7 0.1 | 0.01 | 88.6250% | 20.7354 | 0.5496 | 0.3704 | 0.4328 |
| reweighted S7 1→0.1 | 1.0 | 73.6875% | 7.4958 | 0.7929 | 0.1324 | 0.1220 |

Fresh has a `+1.4375`-point estimate over Dense, with 95% interval
`[+0.0625,+2.7500]`, but the registered 97.5% interval crosses zero. It is also
less concentrated than Dense by effective dimension and Q16. Reweighted is the
most concentrated condition and has resolved lower accuracy than fresh plus the
lowest B/W and mean ARI.

### 7.2 Sensitivity and observer-only evidence

- Last-token accuracy, Dense/fresh/reweighted: `81.25% / 80.25% / 78.25%`.
- S7 reconstruction-mean accuracy, fresh/reweighted:
  `87.1875% / 64.9375%`.

These observations do not replace the registered native body-mean comparison.

### 7.3 Failed, ambiguous, missing or ineligible evidence

- Primary fresh−Dense direction is ambiguous under the registered 97.5% rule.
- No model seed replication was run; record bootstrap does not estimate
  training-seed uncertainty.
- No functional intervention tested whether the language model uses these
  readable distinctions.
- No post-hoc metric is promoted to repair the primary ambiguity.

## 8. Visualization Results

### Exact-17B N8 primary accuracy and registered intervals

![Exact-17B N8 primary accuracy and registered intervals](figures/n8_17b_separability_primary.png)

Purpose: show the smallest decision-bearing result.  
Raw sources: `analysis/primary_metrics.json` and
`analysis/paired_statistics.json`; curated tables
[`primary_results.csv`](tables/primary_results.csv) and
[`paired_contrasts.csv`](tables/paired_contrasts.csv).  
Metric/unit: absolute test accuracy in percent on the left; paired accuracy
difference in percentage points with 97.5% intervals on the right.  
How to read: fresh−Dense crosses zero; reweighted−fresh is wholly negative.  
Limitation: the interval conditions on these checkpoints and records, and the
figure does not establish causal mechanism or cross-seed generality.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | What it rules out | What remains live |
|---|---|---|---|---|
| Target preflight | four RTX5090 and mounted SM120 runtime | PASS | wrong GPU/runtime | none operational |
| Asset/data identity | exact checkpoint and N8 manifests | PASS | missing or nearby checkpoint substitution | historical confounding |
| Extraction | 3 × 4,800 caches, finite values, unchanged states | PASS | hook/cache/mutation failure | scientific comparison |
| Primary analysis | predictions and paired intervals | PASS | missing estimator | fresh−Dense direction unresolved |
| Explanatory analysis | geometry and five-seed K-means | PASS | missing structure diagnostics | causal mechanism |
| Terminal/artifacts | full gate, artifact manifest, terminal PASS | PASS | incomplete run | researcher judgment |

Falsified implementation: no.  
Falsified metric: no.  
Evidence against the candidate physical prior: the more concentrated
reweighted condition is markedly less readable and less distance-grouped.  
Remaining rival: SAE history may concentrate shared, scale-related or
cross-domain directions rather than domain-discriminative directions.

## 10. Full Experiment Record

### Round 1 — 2026-09-22/23 engineering qualification

1. Question: can the exact-17B N8 measurement path run correctly?
2. Setup: three roles plus an independent fresh replay on 16 fixed dev records.
3. Training data: none.
4. Confirmation data: 16 preselected dev records; test labels unused.
5. Result: `SMOKE_PASS`; no scientific result.
6. Boundary: engineering eligibility only; Protocol Amendment A1 records the
   local H100 MIG surface after an ACP create failure before job creation.

### Round 2 — 2026-09-23 full registered audit

1. Question: does SAE-associated concentration accompany stronger exact-17B
   N8 domain separability?
2. Setup: three exact-17B models, frozen native layer-8 mean primary and last
   sensitivity, same N8 records, one authorized 4×RTX5090 Spot node.
3. Training data: none; fit labels train only the linear reader.
4. Confirmation data: 1,600 fixed test records; labels unavailable to fitting,
   preprocessing, `C` selection and K-means fitting.
5. Result: all conditions complete. Fresh−Dense is `+1.4375` pp with registered
   interval crossing zero; reweighted−fresh is `−14.9375` pp with interval
   wholly below zero.
6. Insight boundary: the direct result makes concentration an invalid proxy for
   domain separability in this comparison. Initial mechanism wording and the
   next scientific decision remain awaiting researcher confirmation.

## 11. Interpretation Scaffold

Question: whether concentration corresponds to improved N8 readability.  
Direct result: fresh−Dense unresolved; reweighted markedly below fresh while
more concentrated.  
AI draft interpretation: representation concentration is not a monotonic proxy
for domain readability; SAE history reorganizes which directions remain
prominent.  
Confirmed by researcher: `AWAITING_RESEARCHER`.  
Cannot claim: isolated coefficient causality, broad semantics, model use,
language-model quality or training efficiency.

## 12. Claim Boundary

Can claim from eligible measurement: for these exact checkpoints and N8 panel,
fresh S7 is not directionally established above Dense by the registered rule;
the more concentrated reweighted S7 is substantially less linearly readable
than fresh and has weaker centroid separation and clustering agreement.  
Cannot claim: SAE always harms or helps semantic information; concentration
caused the accuracy difference; N8 exhausts semantic content; the LM uses the
readable information; or the result generalizes across seeds and tasks.

## 13. Next Decision

AI suggestion: test whether reweighted's gap reflects loss of
domain-discriminative directions or a reversible scale/conditioning change.  
Completion criterion: a transform determined only on fit data either recovers
a large share of the `−14.9375`-point gap or leaves it unresolved/unchanged.  
Resume action: formalize the smallest discriminator in the Anchor only after
the researcher confirms the current result judgment and next question.

## 14. Artifact Manifest

| Artifact | Purpose | Hash / identity | Complete | Claim-eligible | Notes |
|---|---|---|---|---|---|
| `analysis/primary_metrics.json` | probe, geometry and ARI aggregates | `4e22c736...12899b8` | yes | yes | all roles/views |
| `analysis/paired_statistics.json` | registered contrast intervals | `77aa50a8...2e678280` | yes | yes | 2,000 draws |
| `analysis/test_predictions.jsonl` | record-level supervised predictions | `4bd8c571...17fa216` | yes | yes | 9,600 rows across roles/views |
| `analysis/cluster_predictions.jsonl` | record/seed cluster assignments | `50850070...5b5bb2` | yes | explanatory | five seeds |
| `analysis/failures.json` | typed analysis failures | JSON `[]` | yes | guard | no failures |
| three cache manifests | identity, state, memory and throughput | hashes in run artifact manifest | yes | yes | 4,800 records each |
| `stages/FULL_MEASUREMENT_PASS.json` | aggregate completion gate | `48ea28c1...294db84` | yes | execution | scientific verdict awaiting researcher |
| `terminal_receipt.json` | terminal execution receipt | `e71cc6ba...9f0dee` | yes | execution | exit 0, PASS |
| `tables/primary_results.csv` | curated primary and explanatory table | `d5d99c53...0279e0b` | yes | yes | exact reading table |
| `tables/paired_contrasts.csv` | curated registered contrast table | `b0c1b74c...afbd767` | yes | yes | exact interval table |
| `figures/n8_17b_separability_primary.png` | central reading figure | `9fadd6f9...be79e18` | yes | yes | derived from the two analysis JSON files |
| `summary.md` / `summary_cn.md` | draft first-reading surfaces | `e731599e...68efed` / `c89aaf8e...565dcf` | yes | measurements yes; judgment pending | awaiting researcher confirmation |

## 15. Links

anchor: `15_17_02_sae_n8_separability_anchor.md`  
protocol: `A15_17_02_E01_n8_17b_separability_audit/protocol.md`  
summary: `summary.md` and `summary_cn.md`, both draft pending researcher judgment  
meeting brief (E01 historical): `daily_research_reports/0923/meeting_report/history/meeting_brief_sae_n8_separability_e01_17b.md`  
code workspace: `/data/250010109/MoE_Router/experiments/20260923_sae_n8_separability_audit`  
runner: `scripts/run_full.sh`  
data / manifest: `manifests/resolved_assets.json`  
result dir: `runs/full_4x5090_20260923T011428Z`  
pod log: `acp_receipts/pod/a15-17-02-e01-n8-17b-full-4x5090-*.log`  
job id: `pt-3nidnrq0`
