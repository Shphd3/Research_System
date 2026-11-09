# A15_08_E02 Fresh Balanced-Mismatch Repair — Detailed Evidence Record

## 1. Evidence Status

- Frozen Protocol: [protocol.md](protocol.md), revision `A15_08_E02_v1`, with
  pre-execution clarification A1.
- Execution: one smoke and one complete local full run on 2026-08-10.
- Mechanical analyzer label: `H2_PASS_H1_FAIL`.
- Post-result Protocol qualification:
  `INELIGIBLE_PROTOCOL_CONFIRMATION_LABEL_PREUSE`.
- H2 and H1': `NOT_ADJUDICATED`.
- Reason: the analyzer materialized confirmation mismatch maps from
  CONFIRMATION labels/groups before writing the freeze receipt, contrary to
  Protocol Sections 5, 7, and Stage S5. No confirmation loss or selection
  metric leaked, so the numerical arrays remain reconstructible diagnostics.

## 2. Frozen Inputs And Objects

| Object | Frozen value |
| --- | --- |
| model | `/data/share/Qwen3-8B`, 36 blocks, hidden width 4,096 |
| site | block index 24 / reported layer 25, final `Answer:` token |
| transition | \(X=N_{25}(h)\), \(Z=N_{25}(h+a)\), \(U=Z-X\) |
| conditional update | \(R_U=U-\widehat{\mathbb E}_{lin}[U\mid X]\) |
| target | centered one-hot terminal code A--H |
| data | 128 TRAIN / 64 DEVELOPMENT / 128 CONFIRMATION episodes per condition; eight records per episode |
| generation seeds | 6101 / 6102 / 6103 |
| full data SHA-256 | `1f38faa9b1a03b2b8d15affe49d100782f9fbba9bcfde7904b9f8caf4e0135de` |
| simple data SHA-256 | `bacc63f82e2492974d0e5b7bd56f95a2b8a8b2f80597f68e0a6c690e3e86dc61` |
| complex data SHA-256 | `cb51426ef4f64fce9ca3337cf6703aab5b71e15da251658ada76faafddb2e31f` |
| bootstrap | 2,000 paired complete-episode draws, seed 6281 |
| H2 mismatch controls | 64 full pipelines, seeds 6200--6263 |
| H1' random controls | 64 seeds, four candidates per seed, seeds 6300--6363 |
| H1' label permutations | 64 full pipelines, four \(\rho\) values per seed, seeds 6400--6463 |

The simple and complex representation files have SHA-256
`cca41dc103e3066d5ebd1d515e561aab8e95002ed41e1d1ac488cc5b839d720c`
and
`4e1032c3c508f7849a58f17bd2c9310d0a6d4db08fc8eb806db19ad1c77d4919`.

The three analysis roles are deliberately separate:

1. the TRAIN-only pooled basis places \(X\), \(Z\), and \(U\) in one coordinate;
2. the exact difference \(U\) names what the attention transition changed;
3. held-out readout risk after residualizing \(U\) against \(X\) determines whether
   that change adds target accessibility.

Neither the common basis nor \(U\) alone defines new knowledge. The generalized
eigenproblem is a supervised direction selector; its matrix is not itself a
knowledge matrix.

## 3. Execution And Freeze Lineage

The E02 data generator produced 5,120 fresh records with `innovation-e02-*`
identifiers and no cross-split context collisions. No E01 episode,
representation, or confirmation value was reused. The 24 deterministic unit and
synthetic tests passed before the full analysis. The smoke used 16 episodes per
split and condition and passed all extraction guards; the full extraction then
processed 2,560 records per condition on two H100s.

The full analyzer first verified that all five E01 source hashes were unchanged.
It fitted residualizers, full readouts, 64 balanced mismatch controls, 64
four-candidate random controls, 64 four-\(\rho\) label-permutation controls, and
the real rank-two direction using TRAIN/DEVELOPMENT outcomes. Before evaluating
any confirmation conditional loss, it froze 192 controls plus every selected
model, direction, hyperparameter, and bank. However, those banks already
included 64 confirmation index maps built from confirmation labels/groups. The
freeze ledger explicitly records
`confirmation_labels_used_before_freeze_only_for_capability_and_structural_bank_map: true`.
That use was not authorized. The ledger SHA-256 is
`a0f468f9f27ea630a76edc62e0ed5a09e74589e7cab74ce2c27557547b947dce`.

The analysis ran on one H100 with NumPy 1.24.4 and PyTorch
2.3.0a0+6ddf5cf85e.nv24.04. It completed in 38.3 seconds after extraction. The
canonical `result.json` SHA-256 is
`1828474932f7b8e13ebd8933563f38bdccc5022233308ce52479e463ebc64f4f`.

## 4. Validity Guards And Protocol-Conformance Failure

### 4.1 Data, capability, and hook identity

| Guard | Simple | Complex | Limit | State |
| --- | ---: | ---: | ---: | --- |
| confirmation restricted-choice accuracy | 0.993164 | 0.760742 | 0.80 / 0.60 | pass |
| records and episode balance | complete | complete | exact registered counts | pass |
| cross-split context collision count | 0 | 0 | 0 | pass |
| same-run replay max absolute error | 0 | 0 | \(\le10^{-5}\) | pass |
| direct `o_proj` relative error | 0 | 0 | \(\le10^{-5}\) | pass |
| loaded \(Z-X-U\) relative error | 0 | 0 | \(\le10^{-6}\) | pass |

### 4.2 Common coordinate and covariance identity

The episode-centered pooled TRAIN basis used both conditions and both \(X\) and
\(Z\). Exact episode contrasts reduced 4,096 rows to 3,584 nonzero directions.

| Numerical quantity | Value | Limit | State |
| --- | ---: | ---: | --- |
| stored-basis orthogonality relative error | \(7.5088\times10^{-7}\) | \(10^{-5}\) | pass |
| solver-float64 orthogonality error | \(2.7341\times10^{-10}\) | descriptive | pass |
| trace reconstruction relative error | \(4.1970\times10^{-16}\) | \(10^{-4}\) | pass |
| covariance identity, simple | \(1.2918\times10^{-15}\) | \(10^{-5}\) | pass |
| covariance identity, complex | \(1.4097\times10^{-15}\) | \(10^{-5}\) | pass |

The audited source is
[common_basis_spectrum.csv](tables/common_basis_spectrum.csv), and the display is
[figure_common_basis.png](figures/figure_common_basis.png). It answers where
variance and retrieved directions lie in one TRAIN-only coordinate; it does not
decide H2 or H1'.

### 4.3 Control-construction and synthetic guards

Each balanced control bank has an exactly uniform \(8\times8\) target-source
contingency within every eight-episode block. Empirical target-source mutual
information is zero, split keys differ, and fixed points are allowed. A fixed
global cyclic fixture has empirical mutual information \(\log 8=2.079442\) nats
and is correctly rejected.

The planted rank-two fixture produced a true gain of 0.234414 nats/example
against a mismatch q95 of 0, with planted-plane overlap 0.989849. The
target-independent fixture had top innovation eigenvalue 0.020936; the
redundant-readable fixture had update-only gain 0.231266 but conditional gain
only 0.023384. Clean group partitions were accepted and a one-row episode leak
was rejected. These checks validate implementation behavior, not Qwen3-8B.

### 4.4 Decisive conformance failure

Protocol Section 5 permits pre-freeze CONFIRMATION labels only for the frozen
restricted-choice capability guard. Section 7 states that confirmation use
before freeze makes E02 ineligible, and Stage S5 declares its input
TRAIN/DEVELOPMENT only. In `fit_balanced_mismatch_controls`, the implementation
built `banks["confirmation"]` from `confirmation.labels` and
`confirmation.groups` before `freeze_selection` was called. This exposed no
conditional loss or selection value, but it violated the stronger registered
data-access rule. The raw `eligible: true` field in `result.json` reflects only
implemented mechanical guards and is superseded by this external
Protocol-conformance audit.

## 5. Reconstructible Confirmation Diagnostics

### 5.1 H2 added-accessibility gate

| Quantity | Estimate | Paired-episode 95% interval | Registered reading |
| --- | ---: | ---: | --- |
| old-only CE | 2.064257 | point estimate | reference |
| full-\(R_U\) CE | 1.329175 | point estimate | true conditional update |
| \(Z\)-only CE | 1.342497 | point estimate | same-dimensional state guard |
| \(G_{true}\) | +0.735082 | [0.715608, 0.756246] | lower bound positive |
| \(G_{state}\) | +0.721760 | [0.702151, 0.742898] | lower bound positive |
| \(T_{cap}\) | +0.734620 | [0.715064, 0.755466] | lower bound positive |

For every bootstrap draw, \(T_{cap}\) subtracts the higher-method q95 of all 64
balanced-control gains from the true gain. The controls' point q95 was only
+0.000462 nats/example. All three registered lower bounds are strictly
positive, so the mechanical arithmetic maps to H2 `PASS`. Because E02 is
Protocol-ineligible, this is not a scientific H2 verdict.

The two independent views agree: adding full \(R_U\) to a frozen old-state readout
lowers held-out loss, and an equally dimensional new-state readout also beats an
old-state readout. The balanced controls rule out the narrower explanation that
any target-independent correction branch with the same fitted budget would
produce the gain.

### 5.2 H1' rank-two sufficiency gate

The real generalized eigenproblem selected \(\rho/\bar\sigma_U^2=1\) and
correction ridge \(10^{-4}\). Its first eight eigenvalues were 0.726121,
0.696980, 0.670625, 0.660635, 0.617493, 0.605410, 0.587846, and 0. The first two
held 31.17% of this eigenvalue mass.

| Quantity | Estimate | Paired-episode 95% interval | Registered reading |
| --- | ---: | ---: | --- |
| rank-two CE | 1.825439 | point estimate | two-coordinate correction |
| \(G_2\) | +0.238819 | [0.228856, 0.248747] | 32.49% of full point gain |
| \(D_{80}\) | -0.349247 | [-0.362226, -0.336496] | 80% retention rejected |
| \(T_{random}\) | +0.030400 | [0.020933, 0.037635] | exceeds matched random q95 |
| \(T_{perm}\) | +0.219446 | [0.209049, 0.229597] | exceeds label-permutation q95 |

Numerically, the two coordinates are non-null but insufficient. H1' was
conjunctive, and the upper bound of \(D_{80}\) is below zero; the mechanical
arithmetic therefore maps to H1' `FAIL` even though both null contrasts pass.
The Protocol violation prevents formal adjudication. Even after a compliant
replication, such a result would reject only the registered rank-two retrieval,
not establish that the full representation is high rank or that no other
low-rank method can work.

### 5.3 Secondary simple condition

The simple condition is not verdict-bearing. Its full residual-update gain was
+0.058813 [0.041563, 0.075835], its same-dimensional state gain was +0.104500
[0.089907, 0.119195], and its two-direction gain was +0.034664
[0.027491, 0.041860]. Its \(D_{80}\) was -0.012387
[-0.023144, -0.001012], matching the primary numerical rank-two failure pattern
but unable to change either the mechanical label or the ineligible status.

Complete point estimates and intervals are in
[confirmation_metrics.csv](tables/confirmation_metrics.csv). Per-control
selection and point gains are in
[confirmation_control_summary.csv](tables/confirmation_control_summary.csv),
and all control-by-episode gains are in
[confirmation_control_per_episode_gains.csv](tables/confirmation_control_per_episode_gains.csv).

## 6. From Result To Knowledge Update

The prior uncertainty was whether a positive update readout merely reflected a
larger correction model or an invertible relabeling. E02 made source updates
exactly independent of target labels in aggregate, regenerated that relation
across splits, refitted every control, and required a same-dimensional state
comparison. The full true residual update exceeded all numerical gates by a
wide positive interval, but confirmation-label pre-use breaks the registered
qualification chain. The bounded update is only that the repaired metric and
controls produce a strong diagnostic pattern worth one clean,
fresh-confirmation test.

The prior low-rank hypothesis was operationalized as a stronger and auditable
claim: two frozen supervised directions should retain at least 80% of the full
gain. They retained only 32.49% numerically. Until a compliant repair, the
correct update is not even “rank two failed”; it is “E02 predicts a rank-two
failure pattern, but H1' remains unadjudicated.”

## 7. Reproducibility And Artifact Map

Worker root:
`Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_e01_layer25_conditional_innovation/`.

Complete worker run:
`runs/a15-08-e02-fresh-balanced-repair-20260810/` relative to that root. It
contains fresh data, smoke/full representations and logits, extraction logs,
the 54.4 MB common basis, frozen linear models and directions, frozen balanced
banks, per-record gains for every control, and complete manifests.

Curated canonical evidence beside this record includes:

- `evidence/result.json`, `guard_report.json`, `synthetic_guard_report.json`,
  `frozen_selection_control_ledger.json`, `selection_freeze_receipt.json`,
  environment/code receipts, plot contracts, and artifact manifest;
- paired bootstrap replicates and compact per-control episode arrays under
  `evidence/`;
- complete decision tables under `tables/`;
- both decision-relevant figures in PNG and PDF under `figures/`.

The canonical copies of all decision-bearing text, tables, arrays, and figures
match the worker artifacts by SHA-256. Large frozen model and basis arrays remain
in the worker and are named, hashed, and sized in the canonical artifact
manifest.

## 8. Visualization Audit

- [figure_e02_confirmation_gates.png](figures/figure_e02_confirmation_gates.png)
  is legible and matches the registered metrics. The right panel separates H2
  capacity evidence from H1' retention and null tests; it must not be read as a
  Router result.
- [figure_common_basis.png](figures/figure_common_basis.png) is legible. Its
  first panel truncates display to the leading 256 pooled ranks for readability;
  the table contains all 3,584 retained directions. The cumulative red curve is
  conditional-innovation eigenvalue mass located in the pooled coordinate, not
  cumulative variance or proof of knowledge location.
- Plot question, unit, source, aggregation, allowed conclusion, and limitation
  are recorded in [plot_contracts.json](evidence/plot_contracts.json).

## 9. Claim Boundary And One Next Decision

Established: E02's arrays, bank balance, paired aggregation, bootstrap, and
mechanical verdict mapping are reconstructible; its control stage violated the
frozen confirmation-label access rule. It therefore establishes neither H2 nor
H1'.

Not established: adjacent-block information novelty, whole-representation rank,
Shannon-information creation, facts stored by the model, nonlinear uniqueness,
native use of the increment, natural-language generality, expert utility, or
Router gain.

**Exactly one next decision:** execute a fresh-confirmation repair in which all
TRAIN/DEVELOPMENT-selected objects and label-free confirmation-bank recipes are
hashed before any new confirmation label is opened. Only an eligible repair may
open a rank-ladder decision.
