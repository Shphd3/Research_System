# Protocol: A15_08_07_E01 CLINC150 Semantic-Conditioned Geometry And Low-Dimensional Functional Subspace

## 0. Approval Snapshot

- **Document status:** `APPROVED_AND_FROZEN_FOR_EXECUTION`.
- **Human request covered:** audit the referenced 0818 conversation and screenshot, enumerate every condition/data/analysis requirement, and prepare one complete Anchor and one Protocol for review before execution.
- **Execution authorization:** the user explicitly approved the complete design and requested execution on 2026-08-18. The formal run is frozen to one `8x5090` node (resource profile `5090-8-spot`). TEST remains sealed until the freeze receipt passes and is then opened exactly once.
- **Primary Anchor:** [A15_08_07](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_07_semantic_conditioned_functional_subspace_anchor.md).
- **Role:** a new real-task transfer and semantic-conditioning test; it does not supersede A15_08_05.
- **Primary objects:** \(X\), \(U\), and affine-linearly residualized \(R_U\) at frozen Qwen3-8B blocks 24 and 28.
- **Primary data:** CLINC150 in-scope English utterances; official TRAIN/validation/test splits; OOS excluded.
- **Primary decision metrics:** matched within-minus-cross normalized \(r_{90}^{var}\) plus local-subspace orientation/union tests for geometry; equal-domain macro held-out CE gain for function.
- **Functional rank:** do not use class count \(C\); directly report the smallest \(R_U\) projection dimensions reaching \(0.8G_{full}\) and \(0.9G_{full}\).
- **Supervised method:** reduced-rank ridge regression (RRR), fixed in advance.
- **Cannot claim:** intrinsic semantic rank, nonlinear new information, model-native use, expert utility, Router improvement, specialization, or forgetting reduction.

### Pending human confirmations

| Block | Decision to confirm | State |
| --- | --- | --- |
| A | two-clause question and claim boundary | `CONFIRMED` |
| B | CLINC150, in-scope only, complete 10-by-15 mapping | `CONFIRMED` |
| C | frozen Qwen3-8B, prompt/token, blocks 24/28, \(R_U\) definition | `CONFIRMED` |
| D | matched within/cross construction and Global-150 descriptive role | `CONFIRMED` |
| E | full-\(R_U\) admission before rank interpretation | `CONFIRMED` |
| F | supervised RRR and 80%/90% retention curves | `CONFIRMED` |
| G | thresholds, null counts, bootstrap, resource ceiling, outputs | `CONFIRMED` |

All seven blocks are user-confirmed and frozen. The implementation must record this document's SHA-256. Any change to the data, objects, thresholds, comparison family, or TEST-use policy requires a new amendment and may not silently overwrite this approval.

## 1. Decision Questions And Typed Outcomes

### Q1 — geometric mixture

At identical class and sample counts, are within-domain update clouds more concentrated than cross-domain clouds, are the admitted local subspaces stable and differently oriented, and does their union dimension grow beyond a same-domain resampling null?

Typed outcomes:

- `LOCAL_UNION_SUPPORTED`: concentration, orientation stability, and union growth all pass.
- `LOCAL_CONCENTRATION_ONLY`: rank narrows, but orientation or union evidence fails.
- `NO_LOCAL_CONCENTRATION`: the matched rank contrast fails in the opposite/no-effect direction with adequate power.
- `GEOMETRY_INSUFFICIENT`: spectrum, stability, mapping, or sampling guards fail.

### Q2 — low-dimensional functional retention

After full \(R_U\) is admitted on the new task, at what projection dimensions does \(R_U\) retain 80% and 90% of full held-out added accessibility, beyond equal-rank random controls?

Typed outcomes per block:

- `FUNCTION_RANK_80_90_ESTIMATED`.
- `FULL_GAIN_BUT_THRESHOLD_NOT_REACHED`.
- `INSUFFICIENT_NO_FULL_GAIN`.
- `FUNCTION_INSUFFICIENT_GUARD`.

### Q3 — variance ordering

Do PCA-head directions retain the same function as supervised RRR directions at matched rank? This is a method comparison, not a separate promotion gate.

## 2. Data, Provenance, And Examples

### 2.1 Canonical source

CLINC150 is an English task-oriented-dialogue intent-classification dataset with ten domains and 150 in-scope intents, fifteen per domain.  
Each intent has 100/20/30 TRAIN/validation/test examples; this experiment excludes OOS and uses 22,500 in-scope examples.

- Official repository: `https://github.com/clinc/oos-eval`.
- Canonical raw file: `data/data_full.json`.
- Expected in-scope structure: 150 intents across ten domains; each intent has 100 TRAIN, 20 validation, and 30 test rows.
- Expected in-scope totals: 15,000 TRAIN, 3,000 validation, 4,500 TEST, 22,500 total.
- Exclude all OOS rows from the primary experiment.

The raw dataset does not by itself provide a trusted complete domain column. Before implementation, create one frozen 10-domain-by-15-intent mapping manifest from the paper/supplementary intent list, independently verify every raw intent appears exactly once, and record source and SHA-256 hashes. Any duplicate, missing intent, non-15 domain, or split-count mismatch is a hard stop.

Expected domain names are banking, credit cards, work, meta, auto and commute, travel, home, utility, kitchen and dining, and small talk. The execution manifest, not this prose list, owns normalized identifiers.

### 2.2 Concrete task examples

The following are paraphrases for interpretation, not data replacements:

| Domain/task | Intent examples | Experimental use |
| --- | --- | --- |
| banking 15-way | transfer, freeze account, balance | shared vocabulary but different requested actions; tests fine distinctions after coarse topic is fixed |
| travel 15-way | book flight, flight status, lost luggage | shared travel/flight words; tests whether lexical topic alone is insufficient |
| cross-domain 15-way | transfer, schedule meeting, book flight, rewards balance, plus eleven frozen intents | exposes coarse domain axes while retaining exactly 15 labels and the same samples per label |

### 2.3 Splits and statistical rows

- One row is one complete utterance represented at one frozen prompt token.
- TRAIN learns every residualizer, standardizer, PCA/supervised/null subspace, and readout.
- Validation chooses regularization separately at every frozen candidate dimension.
- TEST is untouched until the freeze receipt passes.
- Primary bootstrap resamples utterances within intents and then aggregates domains equally; 2,000 frozen draws.
- Official splits are retained. A lexical-nearest-TRAIN similarity diagnostic may stratify TEST difficulty but cannot remove rows or change the primary verdict.

## 3. Condition Construction

### 3.1 `global_150`

All 150 in-scope intents. Compute global covariance and function curves as descriptive context. Because class and row counts differ, this condition cannot create the Q1 verdict.

### 3.2 `within_domain_15`

Ten tasks. For domain \(d\), include all fifteen intents and all official in-scope rows. Thus each task has 1,500/300/450 TRAIN/validation/TEST rows.

### 3.3 `matched_cross_domain_15`

For every target domain \(d\), freeze 64 geometry sets from the other nine domains using seed base `8180601`. Every set contains fifteen intents with source-domain counts \((2,2,2,2,2,2,1,1,1)\) under a seed-frozen permutation, so no source domain contributes more than two intents. Include the same 100/20/30 rows for every selected intent.

Constraints:

- target-domain intents are excluded from its matched sets;
- exact duplicates are disallowed;
- intent exposure across the 64 sets is balanced as closely as combinatorially possible and audited;
- no activation, label difficulty, TEST metric, or spectrum participates in set selection;
- the first 16 pre-frozen sets per target domain receive the secondary functional curves; all 64 receive geometry analysis.

## 4. Model, Prompt, Token, Layers, And Shapes

- Model: frozen local `/data/share/Qwen3-8B`.
- Expected architecture: 36 blocks, hidden width \(d=4096\); verify rather than assume.
- Forward: evaluation/inference mode, `use_cache=False`, deterministic attention backend recorded, bfloat16 forward, float32 promoted analysis arrays.
- Prompt:

```text
Utterance: <utterance>
Category:
```

- Gold domain and intent are never inserted into the prompt.
- Token site: the final non-padding token of the literal prompt suffix `Category:`. Record token IDs and require one unambiguous occurrence under the frozen tokenizer.
- Blocks: human-facing 1-based blocks 24 and 28; the implementation receipt must map them to exact module indices.

For split size \(n\):

| Object | Shape |
| --- | ---: |
| \(h_\ell,a_\ell,X_\ell,Z_\ell,U_\ell,R_{U,\ell}\) | \(n\times4096\) |
| local 15-way centered target | \(n\times15\) |
| low-dimensional projection \(P_r\) | \(4096\times r\) |
| projected update \(R_UP_r\) | \(n\times r\) |
| domain-specific logits | \(n\times15\) |

Mandatory identities include native post-attention MLP input versus \(Z\), \(U=Z-X\), hook coverage, repeated-batch determinism, sample order, prompt token identity, and finite-value checks. Any systematic failure makes the affected block ineligible.

## 5. Residualization And Standardization

For block \(\ell\):

\[
X_\ell=N_\ell(h_\ell),\quad
Z_\ell=N_\ell(h_\ell+a_\ell),\quad
U_\ell=Z_\ell-X_\ell.
\]

Fit TRAIN-only feature means/scales. Fit an affine multi-output ridge predictor \(X\to U\) with five TRAIN folds grouped by intent. Every TRAIN row receives an out-of-fold prediction. Validation chooses the dimensionless ridge multiplier from

\[
\{10^{-6},10^{-5},10^{-4},10^{-3},10^{-2},10^{-1},1,10\},
\]

with \(\lambda=\alpha\,\operatorname{tr}(C_{XX})/d\). Refit on full TRAIN, then apply unchanged to validation and TEST:

\[
R_U=U-(XB+b).
\]

No domain or intent label enters residualization. Report TRAIN out-of-fold and validation/TEST reconstruction \(R^2\). The claim remains linear-family-bounded even if residualization is strong.

## 6. Geometry Analysis

### 6.1 Spectra

For every block and condition, center with TRAIN means and compute an unbiased covariance spectrum. Let \(m=\min(n_{train}-1,4096)\) and descending nonnegative eigenvalues \(\lambda_j\). Report

\[
r_q^{var}=\min\left\{r:\frac{\sum_{j\le r}\lambda_j}{\sum_{j\le m}\lambda_j}\ge q\right\},\quad q\in\{0.8,0.9\},
\]

the normalized \(r_{90}^{var}/m\), entropy effective rank, top shares, trace, and cumulative curves. Clip only numerical negative eigenvalues and report clipped mass.

PCA-tail rank \(r\) means the last \(r\) directions within the identifiable positive TRAIN spectrum, not arbitrary zero-nullspace directions.

### 6.2 Within/between intent decomposition

For each 15-intent task decompose

\[
\Sigma_{total}=\Sigma_{within\ intent}+\Sigma_{between\ intent}.
\]

Report spectra and traces for both components. Q1 cannot be interpreted as semantic-union evidence when the entire matched effect is explained by a change in within-intent nuisance covariance.

### 6.3 Local orientation stability

Freeze \(r_0=8\) as the primary orientation budget; \(r_0\in\{4,14\}\) is secondary. Split TRAIN into two fixed, intent-stratified 50-row halves. Learn the local supervised generalized-eigen subspace independently in each half. For orthonormal bases \(P,Q\) define overlap

\[
O(P,Q)=\frac1{r_0}\|P^\top Q\|_F^2.
\]

Primary orientation gap:

\[
\Delta_{orient}=
\operatorname{median}_d O(P_d^{A},P_d^{B})-
\operatorname{median}_{d\ne d'}O(P_d,P_{d'}).
\]

### 6.4 Union growth

For the ten stable local \(r_0\) projectors, form

\[
M_k=\sum_{d\in S_k}P_dP_d^\top
\]

for seed-frozen domain orderings \(S_k\), and compute the entropy effective rank of \(M_k\). Compare the \(k=10\) union with 1,000 same-domain split/bootstrap unions that contain ten independent estimates of one domain's local subspace. This distinguishes different orientations from estimator noise.

### 6.5 Q1 thresholds

Let

\[
\Delta_{rank}=\operatorname{median}_{d,s}
\left[
\widetilde r_{90}^{cross(d,s)}-
\widetilde r_{90}^{within(d)}
\right],
\]

where \(\widetilde r=r/m\).

`LOCAL_UNION_SUPPORTED` requires all of:

1. simultaneous 95% LCB of \(\Delta_{rank}>0\) and point estimate at least 0.05;
2. simultaneous 95% LCB of \(\Delta_{orient}>0\) and point estimate at least 0.10;
3. \(k=10\) union effective rank exceeds the q95 same-domain union null;
4. projector/test-capture and covariance-trace guards pass at both blocks or at the explicitly named eligible block under two-block correction.

If rank concentration passes but items 2 or 3 fail, return `LOCAL_CONCENTRATION_ONLY`. If the 95% UCB of \(\Delta_{rank}\le0\), return `NO_LOCAL_CONCENTRATION`. Intermediate intervals are `GEOMETRY_INSUFFICIENT`.

## 7. Functional Admission And Rank Curves

### 7.1 Frozen \(X\) baseline

For each domain and block, fit a 15-way centered-one-hot ridge readout from standardized \(X\) on TRAIN, using grouped out-of-fold TRAIN logits. Select its penalty on validation and freeze validation/TEST base logits.

The domain selects its readout head but is not predicted and is not inserted into the prompt.

### 7.2 Full and null corrections

Hold base logits bit-identical. Fit correction targets equal to centered one-hot targets minus out-of-fold base logits.

- `true_full_ru`: correctly paired standardized \(R_U\).
- `duplicate_x`: a second standardized \(X\) branch with the same fitting family.
- `mismatch_ru`: 64 seed-frozen within-domain, different-intent derangements, length-decile matched where feasible; the map is built separately inside each split and never crosses splits.

Primary full gain is equal-domain macro TEST CE reduction. Define the null envelope as the maximum of duplicate-\(X\) gain and the q95 mismatch gain. H-ADMIT passes per block only if the simultaneous 95% LCB of true gain minus that envelope is positive. If neither block passes, Q2 is `INSUFFICIENT_NO_FULL_GAIN`.

### 7.3 Candidate subspaces

Frozen grid:

\[
r\in\{1,2,4,8,16,32,64,128,256,512\}.
\]

For each rank evaluate:

1. global TRAIN PCA head of \(R_U\);
2. global TRAIN identifiable PCA tail;
3. 64 TRAIN-frozen nested Haar random bases;
4. supervised reduced-rank ridge regression;
5. 64 intent-label permutations with RRR refitted;
6. full \(R_U\).

The supervised method is fixed to reduced-rank ridge regression. For every functional condition, let \(T_{corr}\) be the centered target minus the TRAIN out-of-fold \(X\)-baseline logits and solve

\[
\min_{P_r^\top P_r=I,\,A_r}
\|T_{corr}-R_UP_rA_r\|_F^2+\lambda\|A_r\|_F^2.
\]

\(P_r\in\mathbb R^{4096\times r}\) is the learnable input projection and \(A_r\) the learnable correction head, so \(P_rA_r\) is a linear module of rank at most \(r\). Use the closed-form TRAIN RRR solution (ridge whitening followed by a truncated SVD of the target cross-covariance), and verify it against direct optimization on a small matrix. Validation selects, for each \(r\),

\[
\lambda=\alpha\,\operatorname{tr}(R_U^\top R_U)/d,
\qquad
\alpha\in\{10^{-6},10^{-5},10^{-4},10^{-3},10^{-2},10^{-1},1,10\}.
\]

RRR is learned separately for each primary condition so the test directly asks whether that condition's \(R_U\) function survives low-dimensional projection. A single \(P_r\) shared across all ten domains is a secondary robustness analysis and does not define functional rank.

For random seed \(s\), draw one Gaussian matrix and QR-factor it into \(Q_s\in\mathbb R^{4096\times512}\); the point at dimension \(r\) uses \(P_{s,r}=Q_s[:,1:r]\). Thus every seed produces one nested curve rather than unrelated spaces at each rank. Plot all 64 thin gray curves, their dashed median, and a 5th--95th percentile band.

Full and projected branches use identical standardization, base logits, targets, penalty grids, and evaluation code. Class count \(C\) never enters the functional-rank definition, thresholds, normalization, or Pass criteria.

### 7.4 Q2 thresholds

For \(\eta\in\{0.8,0.9\}\) define

\[
r_{func}(\eta)=\min\{r:G_r\ge\eta G_{full}\}.
\]

TEST returns `FUNCTION_RANK_80_90_ESTIMATED` only if H-ADMIT passes and all guards pass. Report the first point-estimate rank reaching each threshold; call it confirmed only if the simultaneous 95% LCB of \(G_r-\eta G_{full}\) is positive. Also report its percentile among the 64 random curves and the interval for \(G_r-q_{0.95}(G_{Haar,r})\).

If a threshold is not reached on the frozen grid, report `>512`; if full gain is not admitted, report `NA`; if the interval crosses the line, retain the point estimate but mark it `UNCERTAIN`. A fixed \(r\le32\) budget or class count cannot rescue the verdict.

Projected gain may exceed full gain through regularization. Report ratios above one but do not interpret them as more information; the matched fitting audit is mandatory.

### 7.5 Condition-specific diagnostic curves

To cover every screenshot condition without changing the primary decision:

- `global_150` receives one 150-way \(X\) baseline and matched full/PCA-head/PCA-tail/Haar/RRR rank curves. It remains descriptive.
- every `within_domain_15` task receives PCA-head/PCA-tail/64 nested Haar/full/RRR curves;
- the first 16 frozen `matched_cross_domain_15` sets per target domain receive the same 15-way curves with one set-specific readout and no domain selector.

Every functional figure must show absolute \(G_r\), horizontal \(0.8G_{full}\) and \(0.9G_{full}\) lines, PCA head/tail, RRR, all 64 random curves with median/band, and the full-\(R_U\) line. A companion retention curve shows \(G_r/G_{full}\) and marks both \(r_{func}(0.8)\) and \(r_{func}(0.9)\).

For the local-versus-cross functional comparison, report the ranks needed to reach both 80% and 90% of each condition's own admitted full gain. This comparison is secondary because the labels define different tasks. It is valid only when both members have positive matched full gain and uses paired class/sample counts; missing full gain is shown as `NA`, never imputed or rescued by accuracy.

## 8. Nonlinear Re-encoding Diagnostic

Fit one frozen, validation-selected two-layer \(X\)-only MLP per domain with a parameter budget no larger than the full-\(R_U\) correction family. This is secondary. If it closes the linear \(R_U\) gain, record `NONLINEAR_X_RIVAL_CLOSES_GAP` and limit wording to linear accessibility. It does not erase the linear-gating measurement, nor does failure prove Shannon-new information.

## 9. Statistics And Multiple Comparisons

- Bootstrap: 2,000 intent-stratified utterance draws, equal domain aggregation.
- Blocks 24/28: family-wise simultaneous intervals using max-\(t\) bootstrap or Holm-corrected paired intervals, selected before TEST.
- Geometry sets, ranks, and random seeds are frozen before representation results.
- Rank curves receive simultaneous intervals; the first crossings of the 80% and 90% thresholds enter Q2 adjudication.
- Report effect sizes and intervals, not accuracy alone.
- Macro accuracy, macro-F1, calibration, and \(R_U\)-only accuracy are secondary; none can override CE-gain verdicts.

## 10. Guards And Stop Conditions

Hard stops before TEST:

1. official data/hash/count or 10-by-15 mapping failure;
2. train/validation/test duplicate or sample-ID overlap;
3. prompt token ambiguity or hook identity failure;
4. nonfinite matrices, negligible covariance trace, or eigensolver disagreement;
5. residualizer leakage or missing out-of-fold TRAIN predictions;
6. any subspace, rank, regularizer, layer, or matched set selected using TEST;
7. base logits differ between correction branches;
8. null maps contain fixed rows when a valid derangement exists or cross split/domain illegally;
9. full/projection fitting code paths are not matched;
10. TEST has already been opened during debugging.

TEST opening requires a machine-readable freeze receipt containing data/model/token hashes, sample lists, domain map, seeds, residualizer choices, candidate bases, rank selection, base logits, null maps, and analysis version.

## 11. Required Figures, Tables, And Plain-Language Reading

### Three decision figures

1. **Matched geometry and union figure:** within versus cross normalized \(r_{90}\), local stability/between-domain overlap, and union-growth curve.
2. **Added-gain versus rank figure:** \(X\) baseline, PCA head/tail, all 64 nested random curves and their band, supervised RRR, and full \(R_U\), with both \(0.8G_{full}\) and \(0.9G_{full}\) lines.
3. **Outcome matrix:** geometry verdict versus functional verdict for blocks 24/28, including null excess and claim boundary.

### Required tables

- data/domain/intent/split counts and hashes;
- concrete matched-set manifest and balance audit;
- residualizer and identity receipts;
- total/within/between covariance metrics;
- local overlap and union-null metrics;
- base/full/duplicate/mismatch gains;
- all rank/method gains and validation selection;
- per-domain gains, nonlinear rival, and typed verdicts.

Plain-language interpretation:

- covariance spectrum asks "how many axes does the cloud occupy?";
- matched within/cross changes semantic grouping while keeping task size fixed;
- principal angles ask "are the local axes actually different?";
- PCA head chooses the largest-motion axes, not necessarily the useful axes;
- supervised RRR asks TRAIN labels to learn a low-rank input projection and correction head;
- full \(R_U\) is the ceiling only after it beats duplicate/mismatch controls;
- TRAIN learns, validation decides, TEST judges once.

## 12. Stage Contract And Resource Envelope

| Stage | Purpose | Gate/output |
| --- | --- | --- |
| review | human confirms A--G | approved amendment; otherwise stop |
| preflight | verify data/model/mapping/prompt | hashes, counts, token and architecture receipt |
| unit tests | validate formulas and estimators | red-to-green tests for hooks, covariance, RRR, nulls |
| smoke | 2 intents/domain and small rows, TRAIN/validation only | identities and all branches; no TEST |
| extraction | freeze blocks 24/28 arrays for all official rows | complete manifest and split hashes |
| fit/freeze | residualizers, conditions, per-rank bases, nulls, base logits | freeze receipt |
| TEST | one immutable evaluation | row-level metrics and typed verdict |
| rendering | produce canonical evidence | summary, detailed report, tables, three figures |

Frozen resources: one ACP node with `8x5090`, profile `5090-8-spot` (`share-space` / `computing-cluster-5090-01g` / `n12lp.nn.i10a.8` / spot / normal), at most 32 CPU workers, 256 GiB RAM, 40 GiB new storage, and 24 wall-clock hours. A read-only hardware-and-mount smoke runs first; formal execution begins only after eight actual 5090 GPUs and both model/data mounts are observed. Batch size may change for engineering reasons only if identity outputs are rechecked; data, layers, prompt, objects, thresholds, sets, and metrics cannot change after first eligible extraction, and no substitute GPU profile may be used silently.

Expected code root after approval:

```text
Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/
a15_08_06_e01_clinc150_semantic_conditioned_functional_subspace/
```

Expected raw run root after approval:

```text
/data/250010109/MoE_Router/experiments/
20260818_a15_08_06_e01_clinc150_semantic_conditioned_functional_subspace/runs/
```

No directory above is an authorization to create code or run the experiment.

## 13. What Results Can And Cannot Mean

`LOCAL_UNION_SUPPORTED` says different stable local subspaces contribute to broad geometry; it does not prove they are the dominant source. `FUNCTION_RANK_80_90_ESTIMATED` says the reported projection dimensions retain 80%/90% of held-out intent added accessibility; it does not say the model or Router uses them. Supervised-over-PCA supports an objective mismatch for intent classification only. The next downstream experiment, if separately approved, must replace intent labels with expert-relative utility or update-compatibility targets under matched Top-\(K\) and capacity constraints.
