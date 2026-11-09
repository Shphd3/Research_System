---
experiment_id: A14_02_E02_frequency_mapping_rank_separation
status: completed
verdict: pass_noninferior
---

# Detailed: A14_02_E02 Frequency–Mapping Rank Separation

Primary anchor: [A14_02_01](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_01_frequency_mapping_rank_separation_anchor.md)  
Protocol: [protocol.md](protocol.md)  
Summary: [summary.md](summary.md)

## 0. Quick Recap

**Purpose:** isolate exact-cell frequency from learned common-mapping dose and
measure whether LowF requires more frozen-readout ROOT directions.  
**Hypothesis:** \(\mathbb E[D_s]\le2\) directions.  
**Experiment logic:** redistribute seven presentations per target while keeping
all registered marginals and total optimization fixed; require zero-exposure
cross-surface capability before interpreting rank.  
**Conclusion:** supported. All 10 pairs were valid; mean \(D_s=0.2\) and the
one-sided 95% upper bound was \(0.5\).  
**Boundary:** the parameter common-space gate failed, so E03 was parked.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object | Unit / formula | Decision role | Cannot prove |
|---|---|---|---|---|---|
| exact cell | one surface alias paired with one entity | \((r,a)\) | pair | frequency unit | independent task function |
| unseen cell | exact pair never optimized, with components observed separately | \((r,a)\) with \(F=0\) | cell | reuse capability gate | unique symbolic algorithm |
| ROOT | answer-summary state | post-final-norm state before LM head | 64-vector | intervention surface | explicit internal tree |
| functional rank | directions sufficient for frozen-head behavior | calibration-fit projection | directions | primary physical quantity | exact/raw/intrinsic rank |
| common capture | held-out energy explained by common update basis | common AdamW contrasts | fraction | E03 eligibility | coordinate-free mechanism |

## 2. Anchor Link And Decision Point

E01 showed that exact repetition is not context diversity and gave a
capability-passing lookup \(K\) trend, but it did not isolate frequency inside a
learned common mapping. Archived E02-v1 tested stronger component recombination
and failed. This E02 replaced that strong requirement with a strict but weaker
zero-exposure matrix-cell transfer gate.

## 3. Protocol Compliance Audit

| Contract item | Actual evidence | Status |
|---|---|---|
| conditions | only Common-LowF and matched Common-HighF-Duplicate | pass |
| paired seeds | 0--9, identical initialization per pair | pass |
| realized counts | \(F=1/8\), 1,535,744 presentations each | pass |
| marginal matching | alias/entity/answer/context totals exact for every seed | pass |
| checkpoint | fixed end of one materialized epoch | pass |
| rank splits | basis-fit, rank-selection, final-test disjoint | pass |
| capability | 20/20 condition-seeds pass | pass |
| replay guards | identity, shuffle, random-subspace all pass | pass |
| threshold changes | none after confirmation access | pass |
| E03 gate | 0/10 common-space capture passes | fail; E03 parked |

## 4. Setup

### Data-generating process

\[
p(y\mid r,a,c)=\mathbf1\{y=\pi(a)\}.
\]

There were 16 aliases, 17 entities, 16 nuisance-context tokens, and one random
bijection \(\pi\) per seed. For each alias, 4 cells were frequency targets, 4
unseen calibration cells, 4 unseen final cells, and 5 donors.

LowF target count was 1. HighF target count was 8. With donor baseline
\(B=19196\), an integer table \(X\) satisfied

\[
\sum_aX_{r,a}=28,
\qquad
\sum_rX_{r,a}=7t_a,
\]

so every row, entity, answer, and alias-determined context marginal remained
identical. Each condition had exactly 1,535,744 examples, divisible into 5,999
batches of 256.

### Model and training

- two Transformer layers, one attention head;
- hidden width 64, FF width 128;
- full-position NTP cross-entropy;
- AdamW, learning rate 0.002, weight decay 0, gradient clipping 1;
- one deterministic shuffle and one complete materialized traversal;
- fixed final checkpoint;
- ten paired seeds, sharded over two local H100 GPUs.

### Paths

- runner: `active/tree_low_rank/scripts/run_frequency_mapping_rank.py`;
- config: `active/tree_low_rank/configs/a14_02_e02_frequency_mapping_rank_separation.yaml`;
- raw full result: `active/tree_low_rank/results/a14_02_e02_frequency_mapping_rank_separation/full_v1/`;
- curated tables: [condition seeds](tables/condition_seed_summary.csv) and
  [paired seeds](tables/paired_seed_summary.csv).

## 5. Metrics And Decision Rules

### M1. Realized exact frequency

\[
F_{\mathrm{exact}}(u)
=
\sum_{x\in\mathcal S_{\mathrm{optimizer}}}
\mathbf1\{x\text{ contains }u\}.
\]

**Meaning:** actual optimizer presentations of cell \(u\).  
**Unit:** presentations.  
**Role:** treatment-integrity metric.  
**Observed:** every target was exactly 1 or 8; every unseen cell was 0.  
**Analysis:** generator treatment and reuse guard were realized exactly. This
does not equate presentations with independent contexts.

### M2. Target and unseen capability

\[
Acc(\mathcal D)
=
\frac1{|\mathcal D|}
\sum_{(x,y)\in\mathcal D}
\mathbf1\{\arg\max p_\theta(\cdot\mid x)=y\}.
\]

\[
CE(\mathcal D)
=
-\frac1{|\mathcal D|}
\sum_{(x,y)\in\mathcal D}\log p_\theta(y\mid x).
\]

**Units:** accuracy fraction and nat.  
**Gates:** target-new-context accuracy \(\ge0.95\), target CE \(\le0.10\) nat,
unseen accuracy \(\ge0.75\).  
**Observed:** LowF target accuracy 1.0 in 10/10; LowF unseen accuracy 1.0 in
10/10. HighF unseen mean 0.9926, minimum 0.96875.  
**Analysis:** the low-rank result is not a task-failure floor. The zero-exposure
result directly supports cross-surface behavior under the same mapping.

### M3. Frozen-readout functional rank

\[
\widetilde h_\rho^{(q)}
=
\mu+U_qU_q^\top(h_\rho-\mu),
\]

\[
k_{\mathrm{func}}^{\mathrm{fix}}
=
\min\{q:\Delta CE_q\le0.02,\ \Delta Acc_q\le0.01\}.
\]

**Unit:** ROOT directions.  
**Role:** primary physical measurement.  
**Observed:** LowF \(7.6\pm0.52\); HighF \(7.4\pm0.52\), both range 7--8.  
**Analysis:** the direction budget remained stable even though target
presentation changed eightfold. It does not imply the full 64-dimensional raw
state has exact rank 7--8.

### M4. Paired non-inferiority contrast

\[
D_s=k_{\mathrm{LowF},s}-k_{\mathrm{HighF},s}.
\]

**Unit:** directions.  
**Decision:** at least 8 pairs; one-sided 95% upper bound \(\le2\) and at least
80% of valid pairs \(D_s\le2\).  
**Observed:** \([0,1,0,0,-1,1,0,0,1,0]\); mean \(0.2\); one-sided bounds
\([-0.1,0.5]\); 100% within margin.  
**Analysis:** the result passes with 1.5 directions of headroom between the
observed upper bound and the preregistered margin. This is non-inferiority, not
proof of exact equality.

### M5. Final-test rank validity

At the calibration-selected \(q\),

\[
\Delta CE_q^{test}
=CE_q^{test}-CE_{full}^{test},
\qquad
\Delta Acc_q^{test}
=Acc_{full}^{test}-Acc_q^{test}.
\]

**Observed:** all 20 runs passed. Mean LowF \(\Delta CE=0.00537\) nat; maximum
0.01261. Mean HighF \(\Delta CE=-0.00326\) nat; maximum 0.01375. Accuracy drop
never exceeded zero.  
**Analysis:** rank was not selected on final labels and transferred to final
test within tolerance.

### M6. Full-rank identity replay

\[
E_{\mathrm{identity}}
=
|CE_{q=d}-CE_{full}|.
\]

**Gate:** \(\le10^{-5}\) nat.  
**Observed:** maximum \(6.71\times10^{-8}\) nat.  
**Analysis:** replay implementation recovers the unmodified ROOT path.

### M7. ROOT shuffle damage

\[
\Delta CE_{\mathrm{shuffle}}
=CE(h_{\rho,\sigma(i)},y_i)-CE(h_{\rho,i},y_i),
\]

\[
\Delta Acc_{\mathrm{shuffle}}
=Acc_{full}-Acc_{shuffle}.
\]

**Gate:** CE increase \(\ge0.10\) nat or accuracy drop \(\ge0.10\).  
**Observed:** mean CE increases 14.65 nat (LowF) and 14.42 nat (HighF); mean
accuracy drops 0.943 and 0.928.  
**Analysis:** ROOT identity is causally tied to the registered answer; the
functional-rank replay is not observing an unused state.

### M8. Matched-rank random-subspace guard

For Haar basis \(Q_j\) at the selected rank,

\[
\widetilde h_{j}^{(q)}
=
\mu+Q_{j,q}Q_{j,q}^\top(h-\mu).
\]

**Gate:** zero random subspaces pass the same CE/accuracy tolerance.  
**Observed:** 0/640 pass.  
**Analysis:** task-aware direction selection is necessary; dimension alone is
not sufficient.

### M9. Raw ROOT entropy effective rank

For centered-root singular-value energies \(\lambda_i=\sigma_i^2\),

\[
p_i=\frac{\lambda_i}{\sum_j\lambda_j},
\qquad
r_{\mathrm{eff}}=\exp\left(-\sum_i p_i\log p_i\right).
\]

**Unit:** effective directions.  
**Observed:** LowF mean 14.35; HighF mean 14.10.  
**Analysis:** raw geometry is substantially broader than the 7--8 directions
needed by the frozen answer head. This directly demonstrates why raw effective
rank and functional rank must remain separate.

### M10. Common-step parameter-space capture

\[
C_{\mathrm{common}}
=
\frac{\|P_{G_c}V_{test}\|_F^2}{\|V_{test}\|_F^2}.
\]

**Unit:** energy fraction.  
**E03 gate:** \(\ge0.80\) in at least 8 LowF seeds.  
**Observed:** mean 0.5717, range 0.4780--0.6314; 0/10 pass. Fitted ranks were
24--26 from 32 fit contrasts.  
**Analysis:** one common task function and low ROOT functional rank did not
produce a stable low-dimensional raw AdamW contrast space across held-out
cells. Outside-common parameter novelty is therefore undefined under the
registered estimator; E03 must not run.

## 6. Main Results

| Quantity | LowF | HighF | Decision |
|---|---:|---:|---|
| mean functional rank | 7.6 | 7.4 | paired \(\bar D=0.2\) |
| rank range | 7--8 | 7--8 | complete overlap |
| unseen accuracy mean | 1.0000 | 0.9926 | both pass |
| raw ROOT effective rank mean | 14.35 | 14.10 | descriptive only |
| rank-valid seeds | 10/10 | 10/10 | pass |

## 7. Visualization Results

### Frequency contrast and functional rank

![Frequency contrast and functional rank](figures/frequency_functional_rank.png)

**Purpose:** show the registered rank distributions.  
**Metric/unit:** frozen-readout functional rank/directions.  
**Aggregation:** ten paired seeds.  
**Observed:** both conditions remain at 7--8 directions.  
**Take-home:** frequency reduction did not inflate rank beyond the margin.  
**Limitation:** the plot alone does not encode pairing or confidence bounds;
the paired statistic decides.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | What it rules out |
|---|---|---|---|
| generator | exact counts and marginals | pass | dose/marginal confound |
| capability | unseen and target gates | pass | task-failure floor |
| functional replay | identity/shuffle/random | pass | invalid proxy |
| frequency verdict | upper bound 0.5 < 2 | pass | strong frequency inflation |
| common parameter space | capture 0.478--0.631 | fail | stable registered \(G_c\) |

No physical prior about frequency reuse was falsified. The E03 parameter-space
operationalization failed its prerequisite; this does not falsify functional
reuse.

## 9. Full Experiment Record

- smoke completed before full run;
- full execution used two local NVIDIA H100 80GB GPUs;
- 20 training jobs completed;
- each full job used 1,535,744 sequences and 5,999 optimizer steps;
- all raw checkpoints include model state, optimizer state, last 64 LowF
  updates, common basis, and common probe contrasts;
- no threshold, seed, condition, or checkpoint rule changed after final-test
  access.

## 10. Interpretation

**Observation:** LowF and HighF require nearly identical ROOT task subspaces
after both demonstrate strict cross-surface common-mapping behavior.

**Interpretation:** the direction used to answer a rare cell can be supplied by
other calls to the same mapping. Exact frequency is therefore not a sufficient
rank-control variable here.

**Separate observation:** per-example AdamW step contrasts are not captured by
a stable 32-probe common parameter space.

**Mechanism boundary:** functional state reuse can coexist with broad or
surface-dependent parameter-update geometry. The result supports the state
phenomenon but does not yet identify the parameter mechanism.

## 11. Claim Boundary

Can claim the registered frequency non-inferiority result. Cannot claim exact
rank equality, universal frequency irrelevance, parameter low rank, mapping-\(K\)
causality, natural-language transfer, or automatic H9-F.

## 12. Next Decision

Keep E02 closed as positive phenomenon evidence. A future E03 version must
choose and validate a stable common space without using the current held-out
probe split for design selection; a ROOT-functional common space is the most
direct rival to the failed raw AdamW contrast space.

## 13. Links And Artifact Map

- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- paired table: [tables/paired_seed_summary.csv](tables/paired_seed_summary.csv)
- condition table: [tables/condition_seed_summary.csv](tables/condition_seed_summary.csv)
- figure: [figures/frequency_functional_rank.png](figures/frequency_functional_rank.png)
- runnable workspace: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/tree_low_rank`
- raw result: `results/a14_02_e02_frequency_mapping_rank_separation/full_v1`
- config: `configs/a14_02_e02_frequency_mapping_rank_separation.yaml`
- runner: `scripts/run_frequency_mapping_rank.py`
- tests: `tests/test_frequency_mapping_rank.py` (3 passed)
