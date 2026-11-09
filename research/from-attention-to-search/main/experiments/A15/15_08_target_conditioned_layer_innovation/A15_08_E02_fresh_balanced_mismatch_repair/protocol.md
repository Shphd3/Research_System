---
experiment_id: A15_08_E02_fresh_balanced_mismatch_repair
anchor_id: 15_08_target_conditioned_layer_innovation
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_ONE_FULL_RUN
canonical_language: en
approved_scope: implementation_smoke_and_one_full_run
approved: 2026-08-10
design_frozen_at: 2026-08-10T18:08:50Z
registered_revision: A15_08_E02_v1
---

# Protocol: A15_08_E02 Fresh Balanced-Mismatch Repair

## 0. Approval And Repair Snapshot

- **Approval basis:** the researcher authorized construction and execution of a logically correct, self-contained first experiment without another approval pause. E01 exposed a control-construction defect, so repairing that defect is inside the authorized experiment scope.
- **Why this is a new experiment:** E01 confirmation has been opened. E02 changes the full-update object from raw \(U\) to the old-state-residualized update \(R_U\), replaces the globally learnable cyclic control, adds a same-dimensional state gate, and uses wholly fresh TRAIN/DEVELOPMENT/CONFIRMATION episodes. It is not an E01 amendment.
- **Question:** at the answer token, does the layer-25 normalized attention transition add terminal-code accessibility beyond the old state after removing the linearly old-predictable part of the update; if yes, are two conditional-innovation directions sufficient?
- **Primary condition:** complex two-hop composition. The paired simple condition is secondary and cannot rescue the verdict.
- **Registered outcome:** H2 added accessibility, followed only after H2 Pass by H1' rank-two sufficiency.
- **Not tested:** full adjacent-block differences, global representation low rank, Shannon-information creation, native model use, expert utility, or Router improvement.
- **Block audit:** data, supervision, model site, objective, comparisons, execution, and evidence mapping are `CONFIRMED` under the delegated design authority. Cross-block consistency is `PASS`.

## 1. E01 Finding That Motivates This Repair

E01 conformed mechanically to its frozen contract and returned
`H2_INSUFFICIENT_H1_NOT_ADJUDICATED`. Its true raw-update correction improved
complex confirmation cross-entropy by \(0.661428\) nats/example, but the registered
cyclic control improved it by \(0.688412\), giving true-minus-control
\(-0.026983\) with 95% interval \([-0.030384,-0.023705]\).

The cyclic control applied the same invertible map \(y\mapsto y+1\) in every
TRAIN, DEVELOPMENT, and CONFIRMATION episode and fitted a separate correction.
It therefore retained a deterministic one-to-one code for the target and could
learn the inverse relabeling. It did not instantiate target-independent added
capacity. E02 repairs this algebraic defect; it does not reinterpret the E01
registered verdict as a scientific Fail.

E01 also compared a full raw-\(U\) correction with a rank-two \(R_U\) correction.
E02 makes the full reference and its rank-two approximation use the same
residual-update object.

## 2. Precise Objects

At the final `Answer:` token of Qwen3-8B block 25, let \(h\) be the block residual,
\(a\) the attention write, and \(N_{25}\) the block's `post_attention_layernorm`:

\[
X=N_{25}(h),\qquad Z=N_{25}(h+a),\qquad U=Z-X.
\]

\(U\) is the exact matched transition, not knowledge by definition. A TRAIN-fitted
linear ridge residualizer predicts the update from the old state:

\[
R_U=U-\widehat{\mathbb E}_{lin}[U\mid X].
\]

TRAIN residuals are four-fold cross-fitted by complete episode; DEVELOPMENT and
CONFIRMATION residuals use the full TRAIN fit. The target residual is

\[
R_Y=Y_c-\widehat{\mathbb E}_{lin}[Y_c\mid X],
\]

where \(Y_c\) is the centered eight-class one-hot code and TRAIN values are also
four-fold episode-cross-fitted.

The common pooled basis is the TRAIN-only eigenbasis of episode-centered \(X\)
and \(Z\) from both conditions. It only locates \(X,Z,U\) and candidate-direction
mass. It does not enter the primary estimator.

The conditional innovation directions solve the same regularized target-
residual generalized eigenproblem as E01 using \(R_U\) and \(R_Y\). The rank is
frozen at two. The matrix is a supervised direction-selection operator, not a
"new knowledge matrix."

## 3. Hypotheses And Rival

**H2 — target-conditioned added accessibility.** Relative to a frozen old-state
readout, the full residual update \(R_U\) lowers confirmation terminal-code
cross-entropy, outperforms a same-budget correction whose update-target pairing
is exactly independent in aggregate and independently regenerated across
splits, and agrees in sign with the same-dimensional \(X\)-only versus \(Z\)-only
comparison.

**H1' — gated rank-two sufficiency.** Only after H2 Pass, the two frozen
conditional-innovation coordinates must retain at least 80% of the full-\(R_U\)
gain and exceed both equal-rank row-span random and TRAIN-label-permutation null
families under paired episode resampling.

**Strongest rival:** a high-dimensional added correction branch can improve a
readout through generic capacity, stable relabeling, or nuisance geometry even
when its input is not the target-matched transition. The balanced mismatch bank
and same-dimensional state comparison separate this rival.

Eight centered classes have discriminant rank at most seven. H1' therefore
tests whether two directions are sufficient; it never tests whether the whole
representation is low rank.

## 4. Fresh Data And Independence

Generate the same balanced paired composition task as E01, but no E01 record,
mapping episode, or model representation is reused:

| Split | Episodes | Records per condition | Generation seed | Wording family |
| --- | ---: | ---: | ---: | --- |
| TRAIN | 128 | 1,024 | 6101 | symbolic map |
| DEVELOPMENT | 64 | 512 | 6102 | lookup table |
| CONFIRMATION | 128 | 1,024 | 6103 | prose table |

Every episode contains all eight terminal targets once in each of the simple
and complex conditions. Paired conditions share the exact mapping context,
intermediate state, and terminal answer. Splits use disjoint generated maps and
prompt-family wording. The independent unit is the complete eight-target
episode; no row, pair, map, or episode crosses splits.

The data manifest freezes schemas, seeds, counts, balance, generator hash, and
file SHA-256 before model extraction.

## 5. Model Site And Extraction

- Frozen `/data/share/Qwen3-8B`, bfloat16 forward, SDPA, `use_cache=False`.
- Block index 24, reported as layer 25; final prompt token only.
- Capture block input residual and `self_attn.o_proj` output; compute \(X,Z,U\) in
  float32 with the same \(N_{25}\).
- Persist record IDs, representations, restricted A--H logits, hashes, and
  manifests separately for simple and complex conditions.
- Required guards: restricted-choice confirmation accuracy simple \(\ge0.80\) and
  complex \(\ge0.60\); same-run replay max error \(\le10^{-5}\); direct `o_proj`
  relative error \(\le10^{-5}\); stored difference reconstruction \(\le10^{-6}\).

Confirmation target labels may be used before selection only for this frozen
restricted-choice capability guard. No confirmation representation loss,
conditional gain, direction, or hyperparameter is exposed before the selection
ledger is frozen and hashed.

## 6. Readout And Residualization Family

All fitted components are closed-form ridge models. Feature centering and one
scalar RMS scale are fitted on TRAIN; coordinate-wise scaling is forbidden.
The ridge grid is
\(\{10^{-4},10^{-3},10^{-2},10^{-1},1,10,100,1000\}\); DEVELOPMENT selects by
cross-entropy for target readouts and reconstruction MSE for \(U\mid X\). Ties
choose larger regularization.

1. Fit old-state \(f_X\) from \(X\) to \(Y_c\).
2. Fit \(U\mid X\) and form cross-fitted TRAIN \(R_U\) plus full-TRAIN DEV/CONF
   residuals.
3. Fit the full correction \(g_{full}:R_U\to R_Y\) while freezing \(f_X\).
4. Fit a separate same-budget state readout \(f_Z:Z\to Y_c\).
5. Build \(P_2\) from complex TRAIN \(R_U,R_Y\); select
   \(\rho/\bar\sigma_U^2\in\{0.01,0.1,1,10\}\) and the rank-two correction ridge
   using complex DEVELOPMENT only.
6. Freeze every model, residualizer, direction, rank, null, seed, and ledger
   before confirmation conditional losses are computed.

## 7. Balanced Episode-Specific Mismatch Banks

For each seed and split, partition consecutive episodes into blocks of eight.
Within each block, construct eight target-to-source permutation matrices whose
sum is the \(8\times8\) all-ones matrix. A randomized base permutation and a
randomized ordering of all eight cyclic offsets produce the bank. Fixed points
are allowed; what matters is exact independence rather than forced mismatch.

Consequently, for every eight-episode block and every target \(y\), the source
update label \(s\) takes each value A--H exactly once. The aggregate target-source
contingency is uniform and empirical \(I(Y;S)=0\). TRAIN, DEVELOPMENT, and
CONFIRMATION use independent split keys.

For each bank, fit a correction from the bank-permuted \(R_U\) to the true TRAIN
\(R_Y\), select its ridge on the independently bank-permuted DEVELOPMENT set, and
evaluate it on the independently bank-permuted fresh CONFIRMATION set. The
correction receives no explicit episode identifier and no joint \(X\times R_U\)
interaction; \(f_X\) remains frozen and additive.

- Bank seeds: 6200--6263, 64 complete full-pipeline controls.
- TRAIN/DEVELOPMENT/CONFIRMATION split salts are distinct and their mapping-key
  hashes must differ.
- Every bank/split contingency cell must equal `episodes / 8`.
- A fixed global cyclic fixture must fail the contingency/empirical-MI guard.
- Missing bank, shared split key, nonuniform cell, or confirmation use before
  freeze makes E02 `INELIGIBLE_GUARD`.

## 8. H1' Null Families

- 64 rank-two random subspaces drawn from the complex TRAIN \(R_U\) row span,
  seeds 6300--6363.
- 64 full-pipeline within-episode TRAIN-label permutations, seeds 6400--6463;
  DEVELOPMENT and CONFIRMATION retain true labels.
- Every null uses the same \(R_U\) object, rank, correction architecture, ridge
  grid, split roles, and confirmation episodes as \(P_2\).

## 9. Primary Metrics And Paired Resampling

For complex CONFIRMATION, define per-record gains

\[
g_{true}=CE(f_X(X))-CE(f_X(X)+g_{full}(R_U)),
\]

\[
g_{state}=CE(f_X(X))-CE(f_Z(Z)),
\]

and \(g_{ctrl,s}\) analogously for balanced-mismatch bank \(s\).

For each of 2,000 paired complete-episode bootstrap draws, seed 6281, compute
\(G_{true}^{(b)}\), \(G_{state}^{(b)}\), every \(G_{ctrl,s}^{(b)}\), and

\[
T_{cap}^{(b)}=G_{true}^{(b)}-
Q_{0.95}^{higher}\left(\{G_{ctrl,s}^{(b)}\}_{s=1}^{64}\right).
\]

Report percentile 95% intervals. H2 Pass requires all three lower bounds to be
strictly positive: \(G_{true}\), \(G_{state}\), and \(T_{cap}\). H2 Fail requires the
upper bound of \(G_{true}\) to be non-positive. Every other eligible outcome is
H2 Insufficient.

For H1', let \(G_2\) be the rank-two gain and
\(D_{80}=G_2-0.8G_{true}\). Within each same paired bootstrap draw compute

\[
T_{random}=G_2-Q_{0.95}^{higher}(G_{random,1:64}),
\]

\[
T_{perm}=G_2-Q_{0.95}^{higher}(G_{perm,1:64}).
\]

H1' Pass requires positive lower 95% bounds for \(D_{80}\), \(T_{random}\), and
\(T_{perm}\). H1' Fail requires a non-positive upper bound for any of the three.
Otherwise H1' is Insufficient. H1' is never adjudicated unless H2 Passes.

Quantiles use NumPy `method="higher"`. Every episode receives equal weight and
all eight targets remain together in every resample.

## 10. Common-Coordinate And Synthetic Guards

- TRAIN-only pooled-basis orthogonality relative error \(\le10^{-5}\).
- Pooled covariance trace reconstruction relative error \(\le10^{-4}\).
- For each condition,
  \(\Sigma_Z-\Sigma_X=\Sigma_U+\operatorname{Cov}(X,U)+\operatorname{Cov}(U,X)\)
  relative Frobenius error \(\le10^{-5}\).
- Known-good planted rank-two update: H2 signal and high planted-plane overlap.
- Known-bad target-independent update: near-null conditional gain/spectrum.
- Known-confusing redundant readable update: high update-only readability but
  near-zero conditional gain.
- Fixed cyclic control fixture: empirical target-source MI is nonzero and guard
  rejects it.
- Balanced bank fixture: exact uniform contingency and empirical MI zero.
- Leakage fixture: moving one episode row across a split/fold is rejected.

Synthetic tests validate implementation only; they do not adjudicate Qwen3-8B.

## 11. Stage Contract

| Stage | Input | Output | Pass / stop |
| --- | --- | --- | --- |
| S0 data | seeds 6101--6103 | fresh JSON + manifest | exact counts, pairs, balance, hashes |
| S1 unit preflight | deterministic fixtures | test log | all tests pass |
| S2 smoke | 16 episodes/split/condition | smoke tensors/manifests | capability and hook guards pass |
| S3 extraction | all 5,120 fresh records | full tensors/logs/manifests | complete and hash-valid |
| S4 common coordinate | TRAIN \(X,Z,U\) | spectrum/table/identity | numerical guards pass |
| S5 freeze | TRAIN/DEV only | models, 192 controls, direction and hashed ledger | no confirmation conditional metric exposed |
| S6 confirmation | frozen S5 + fresh CONFIRMATION | per-record/episode losses, bootstrap, verdict | registered mapping only |
| S7 records | eligible artifacts | summary, detailed, Anchor update, daily report | lineage and cold-read pass |

## 12. Verdict Labels

- `H2_PASS_H1_PASS`
- `H2_PASS_H1_FAIL`
- `H2_PASS_H1_INSUFFICIENT`
- `H2_FAIL_H1_NOT_ADJUDICATED`
- `H2_INSUFFICIENT_H1_NOT_ADJUDICATED`
- `INELIGIBLE_GUARD`

No simple-condition result, raw update-only readout, common-basis localization,
E01 value, or post-hoc diagnostic can upgrade E02.

## 13. Outputs, Provenance, And Resources

Worker code root remains
`Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_e01_layer25_conditional_innovation/`, with E02-specific scripts and immutable E01 code hashes.

Worker result root:
`runs/a15-08-e02-fresh-balanced-repair-20260810/`.

Required artifacts: fresh data and hashes; test log; smoke/full extraction
manifests and tensors; environment/code receipt; guard report; common-basis and
covariance tables; frozen selection/control ledger and hashes; all per-record,
per-episode, per-control, and bootstrap metrics; result JSON; plot contracts;
PNG/PDF figures; artifact manifest.

Canonical record root:
`Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E02_fresh_balanced_mismatch_repair/`.

Resource ceiling: two local H100 80GB GPUs, two hours extraction, five hours
total, and 10 GiB additional worker storage. Any OOM, nonfinite value, incomplete
control family, guard failure, or missing lineage stops scientific interpretation.

## 14. Claim Boundary And Next Decision

Even a joint Pass establishes only target- and linear-family-specific added
accessibility for one layer-25 normalized attention transition plus rank-two
sufficiency for that increment. It does not establish adjacent-layer novelty,
whole-representation low rank, natural semantic knowledge, native MLP use,
expert utility, or Router gain.

After eligible execution, the next decision is determined only by the registered
verdict. A joint Pass may open one independent functional intervention; rank-two
failure opens a fresh rank-ladder decision; H2 uncertainty allows only a frozen
precision extension; H2 Fail closes this named object unless the researcher
explicitly selects a different layer/target/nonlinear object.

The scientific body is frozen as `A15_08_E02_v1` before E02 data generation.
After the first E02 generation command, changes require an append-only amendment
with before/after values, timing, approval basis, and eligibility impact.

### Pre-execution clarification A1 — match H1' direction-search budgets

- **Time:** 2026-08-10T18:12:03Z, before any E02 data-generation, implementation-test, extraction, or analysis command.
- **Reason:** the E01 evidence audit found that its real direction searched four \(\rho\) candidates, while its null directions did not receive the same candidate-search budget.
- **Label-permutation null:** every seed must rebuild \(R_Y\) from its permuted TRAIN labels, solve and DEV-evaluate all four registered \(\rho\) candidates, select \(\rho\) and correction ridge with the same tie rules as the real direction, then freeze the selected candidate.
- **Random row-span null:** every seed must draw four independent rank-two row-span candidates, fit the complete correction ridge grid for each, select candidate and ridge by DEVELOPMENT cross-entropy with the same tie rule, then freeze the selected candidate.
- **Evidence requirement:** persist candidate-level selection ledgers and per-episode confirmation gains for all H2 and H1' controls, so every within-bootstrap q95 contrast is independently reconstructible.
- **Eligibility impact:** none. This clarification closes an equal-search-budget omission before E02 starts and does not use E02 data or outcomes.

### Execution and evidence ledger

- **Completed:** 2026-08-10; smoke plus one full mechanically complete run on 5,120 fresh
  records, using two H100s for extraction and one H100 for analysis.
- **Preflight:** all 24 deterministic implementation and synthetic tests passed.
- **Data:** generation seeds 6101/6102/6103; full data SHA-256
  `1f38faa9b1a03b2b8d15affe49d100782f9fbba9bcfde7904b9f8caf4e0135de`.
- **Selection freeze:** 192 controls plus all models, directions, banks, and
  hyperparameters were frozen before confirmation conditional evaluation;
  ledger SHA-256
  `a0f468f9f27ea630a76edc62e0ed5a09e74589e7cab74ce2c27557547b947dce`.
- **Mechanical analyzer guards:** all implemented guards passed, including exact
  uniform target-source contingency for every balanced bank, split-key
  independence, capability, hook identity, common-coordinate reconstruction,
  and synthetic fixtures.
- **Mechanical analyzer label:** `H2_PASS_H1_FAIL`; see the controlling
  post-result Protocol-conformance audit below.
- **Primary values:** \(G_{true}=0.735082\) [0.715608, 0.756246],
  \(G_{state}=0.721760\) [0.702151, 0.742898], and
  \(T_{cap}=0.734620\) [0.715064, 0.755466] nats/example; H2 passes.
  \(G_2=0.238819\) [0.228856, 0.248747] and
  \(D_{80}=-0.349247\) [-0.362226, -0.336496]; H1' fails.
- **Canonical result SHA-256:**
  `1828474932f7b8e13ebd8933563f38bdccc5022233308ce52479e463ebc64f4f`.
- **Records:** [summary.md](summary.md), [detailed.md](detailed.md), and
  [evidence/result.json](evidence/result.json).

### Post-result Protocol-conformance audit D1 — confirmation labels used before freeze

- **Detected:** 2026-08-10 during independent evidence audit, after E02
  confirmation was opened.
- **Frozen rule:** Section 5 permits pre-freeze confirmation labels only for the
  restricted-choice capability guard; Section 7 makes any other pre-freeze
  confirmation use ineligible; Stage S5 is TRAIN/DEVELOPMENT only.
- **Observed implementation:** before writing the selection-freeze receipt,
  `fit_balanced_mismatch_controls` read CONFIRMATION labels and groups to
  materialize and validate 64 confirmation bank index maps. The frozen ledger
  explicitly records this structural-bank-map use.
- **Leakage boundary:** no confirmation loss, gain, representation criterion,
  direction, ridge, rank, threshold, or exclusion was used before freeze. All
  reported arrays and bootstrap arithmetic are independently reconstructible.
- **Controlling qualification:**
  `INELIGIBLE_PROTOCOL_CONFIRMATION_LABEL_PREUSE`; H2 and H1' are
  `NOT_ADJUDICATED`. The raw analyzer label remains provenance only.
- **Repair:** a separately frozen E03 may reuse only E02 TRAIN/DEVELOPMENT-
  selected objects, freeze label-free confirmation bank recipes, and evaluate
  on wholly fresh confirmation episodes opened only after that receipt.
