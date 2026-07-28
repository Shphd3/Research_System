---
experiment_id: A14_02_E02_frequency_mapping_rank_separation
status: approved
approved_by: researcher
approved_date: 2026-07-26
execution_scope: local_two_gpu_full_then_e03_if_gate
chinese_companion: protocol_cn.md
---

# Protocol: A14_02_E02 Frequency–Mapping Rank Separation

## 0. Approval Snapshot

**Approval status:** `PROTOCOLS_APPROVED`; implementation, smoke, local
two-H100 full execution, and conditional E03 execution are authorized.  
**Purpose:** test whether lowering a target exact-cell frequency from $8$ to
$1$ inside a learned common mapping raises frozen-readout ROOT functional rank
by more than two directions.  
**Primary anchor:** [A14_02_01](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/subanchors/14_02_01_frequency_mapping_rank_separation_anchor.md).  
**Physical prior:** mapping reuse, rather than one cell's raw frequency, more
directly controls the task-direction budget.  
**Strongest rival:** apparent low rank comes from task failure, unmatched dose
or marginals, output-head bottlenecks, or an invalid projection.  
**Treatment/control:** Common-LowF $F=1$ versus matched
Common-HighF-Duplicate $F=8$.  
**Held fixed:** common mapping, total function dose, alias/entity/answer/context
marginals, token/batch/step counts, model, initialization, optimizer, and eval
slices.  
**Primary metric:**
$D_s=k_{\mathrm{func},s}^{\mathrm{LowF}}-k_{\mathrm{func},s}^{\mathrm{HighF}}$.  
**Pass:** at least eight valid pairs; the one-sided 95% upper bound of the mean
$D_s$ is at most two and at least 80% of valid pairs have $D_s\le2$.  
**Fail:** every hard gate passes and the one-sided 95% lower bound exceeds two.  
**Insufficient:** fewer than eight valid pairs, an interval crossing the
margin, or any capability, rank-validity, replay, matching, or test-isolation
failure.  
**Cannot claim:** frequency never matters, raw ROOT or complete parameters are
low rank, natural-language transfer, or NTP-implied H9-F.  
**Approval decision:** `APPROVED FOR FULL EXECUTION`.

## 1. Terminology / Definitions

### Exact frequency

$$
F_{\mathrm{exact}}(u)
=
\sum_{x\in\mathcal S_{\mathrm{optimizer}}}
\mathbf1\{x\text{ contains cell }u\}.
$$

It is the realized optimizer-presentation count, measured in presentations.
It does not measure independent information or context diversity.

### Unseen-cell accuracy

An unseen cell is disjoint from frequency targets, has $F_{\mathrm{exact}}=0$,
and has both its alias and entity observed separately in training:

$$
Acc_{\mathrm{unseen}}
=
\frac1{|\mathcal D_{\mathrm{unseen}}|}
\sum_{(r,a,c)}
\mathbf1\{\arg\max_y p_\theta(y\mid r,a,c)=\pi(a)\}.
$$

The frozen gate is $Acc_{\mathrm{unseen}}\ge0.75$, lowered before execution by
the researcher for the small sample and model. It tests cross-surface use of
the common mapping but not a unique internal symbolic algorithm.

### Frozen-readout ROOT functional rank

For a basis-fit-calibration mean $\mu$ and ordered orthogonal basis $U$,

$$
\widetilde h_\rho^{(q)}
=
\mu+U_qU_q^\top(h_\rho-\mu).
$$

With the original output head frozen,

$$
k_{\mathrm{func}}^{\mathrm{fix}}
=
\min\{q:\Delta CE_q\le0.02\ \mathrm{nat},\ \Delta Acc_q\le0.01\},
$$

where

$$
\Delta CE_q=CE(\widetilde h_\rho^{(q)})-CE(h_\rho),
\qquad
\Delta Acc_q=Acc(h_\rho)-Acc(\widetilde h_\rho^{(q)}).
$$

The unit is ROOT directions. Persistent passage is required for $q$ and every
higher rank. Rank is selected on a calibration-selection split and only
validated on final test. This is not exact matrix rank or nonlinear intrinsic
dimension.

### Primary non-inferiority contrast

$$
D_s
=
k_{\mathrm{func},s}^{\mathrm{LowF}}
-k_{\mathrm{func},s}^{\mathrm{HighF}},
\qquad
\tau=2\ \text{directions}.
$$

Positive $D_s$ means LowF needs more directions. One-sided paired-bootstrap
95% bounds use 10,000 draws and seed `20260726`.

### Common-space stability

Fit $G_c$ on 32 leave-target-out common AdamW step contrasts and evaluate 32
held-out contrasts $V_{\mathrm{test}}$:

$$
C_{\mathrm{common}}
=
\frac{\|P_{G_c}V_{\mathrm{test}}\|_F^2}
{\|V_{\mathrm{test}}\|_F^2}.
$$

At least eight LowF seeds must have $C_{\mathrm{common}}\ge0.80$ to run E03.
This is a coordinate-registered stability guard, not a unique mechanism.

## 2. Anchor Alignment

This is a root-cause and operationalization test. It decides frequency
non-inferiority only; E01's lookup-$K$ trend remains secondary historical
evidence.

## 3. Tested Hypothesis

$$
H_{\mathrm{reuse}}:\mathbb E[D_s]\le2,
\qquad
H_{\mathrm{frequency}}:\mathbb E[D_s]>2.
$$

## 4. Rival Explanations

Capability gates address task failure; integer audits address dose and
marginals; frozen-head replay addresses readout absorption; shuffle and random
subspaces address trivial projections; three disjoint rank splits address test
selection.

## 5. Data / Model / Algorithm / Objective

The common task is

$$
p(y\mid r,a,c)=\mathbf1\{y=\pi(a)\},
$$

with 16 aliases, 17 entities, and one seed-frozen random bijection $\pi$.

For seed offset $o_s$,

$$
\mathcal T_s=\{(r,(4r+j+o_s)\bmod17):j=0,\ldots,3\},
$$

$$
\mathcal U_s^{cal}=\{(r,(4r+j+o_s)\bmod17):j=4,\ldots,7\},
$$

$$
\mathcal U_s^{test}=\{(r,(4r+j+o_s)\bmod17):j=8,\ldots,11\}.
$$

The sets are disjoint; the remaining five cells per alias are donors. With
donor baseline $B=19196$, HighF removes an integer donor table $X$ satisfying

$$
X_{r,a}\ge0,
\qquad
\sum_aX_{r,a}=28,
\qquad
\sum_rX_{r,a}=7t_a.
$$

Both conditions therefore contain 1,535,744 optimizer presentations and 5,999
batch-size-256 steps. Training context is seed- and alias-fixed, so identical
alias totals imply identical context marginals; evaluation uses disjoint
context offsets.

The model is a two-layer, one-head, width-64, FF-width-128 causal Transformer
trained by full-position NTP cross-entropy with AdamW, learning rate 0.002,
zero weight decay, and gradient clipping at 1. Each condition traverses one
deterministically shuffled materialized stream. The fixed final checkpoint is
used. Paired seeds are 0--9; two H100s execute fixed shards.

## 6. Conditions, Seeds, And Checkpoints

| Item | Role | Primary/secondary | Pass | Insufficient |
|---|---|---|---|---|
| Common-LowF, $F=1$ | treatment | primary | all gates | any gate failure |
| Common-HighF-Duplicate, $F=8$ | matched control | primary | all gates | any gate failure |
| E01 lookup $K=1/4/16$ | historical mapping-count reference | secondary | descriptive only | no causal upgrade |

Common-HighF-Diverse is omitted from the full contract because E01 already
adjudicated the diversity rival and both primary E02 conditions must pass the
same unseen/new-context gate.

## 7. Primary Metric

Only $D_s$ and its paired one-sided interval decide the verdict.
$k_{\mathrm{func}}^{\mathrm{fix}}$ is the physical measurement; raw ROOT rank
and parameter dimension cannot replace it.

## 8. Secondary Metrics

For any evaluation slice $\mathcal D$,

$$
Acc(\mathcal D)
=\frac{1}{|\mathcal D|}\sum_{(x,y)\in\mathcal D}
\mathbf1\{\arg\max p_\theta(\cdot\mid x)=y\},
$$

$$
CE(\mathcal D)
=-\frac{1}{|\mathcal D|}\sum_{(x,y)\in\mathcal D}
\log p_\theta(y\mid x).
$$

Target/new-context gates are $Acc\ge0.95$ and $CE\le0.10$ nat; the unseen-cell
gate is $Acc\ge0.75$. Accuracy is a fraction and CE is measured in nat. These
metrics establish behavior, not implementation mechanism.

At the calibration-selected rank,

$$
\Delta CE_q^{\mathrm{test}}=CE_q^{\mathrm{test}}-CE_{\mathrm{full}}^{\mathrm{test}},
\qquad
\Delta Acc_q^{\mathrm{test}}=Acc_{\mathrm{full}}^{\mathrm{test}}-Acc_q^{\mathrm{test}}.
$$

The frozen-rank final-test gates are $\Delta CE\le0.02$ nat and
$\Delta Acc\le0.01$; they verify transfer of the selected rank but do not select it.

Full-rank identity replay uses

$$
E_{\mathrm{identity}}=|CE_{q=d}-CE_{\mathrm{full}}|\le10^{-5}\ \mathrm{nat}.
$$

ROOT shuffle uses

$$
\Delta CE_{\mathrm{shuffle}}=CE(h_{\rho,\sigma(i)},y_i)-CE(h_{\rho,i},y_i),
\qquad
\Delta Acc_{\mathrm{shuffle}}=Acc_{\mathrm{full}}-Acc_{\mathrm{shuffle}},
$$

and must increase CE by at least $0.10$ nat or reduce accuracy by at least
$0.10$. These two guards validate the intervention surface; they do not prove
that the selected subspace is unique.

For each of 32 Haar random bases $Q_j$ at the selected rank,

$$
\widetilde h_j^{(q)}=\mu+Q_{j,q}Q_{j,q}^\top(h-\mu).
$$

Zero random subspaces may pass the same CE/accuracy tolerances. This checks
task specificity, not global optimality over every possible nonlinear subspace.

Finally, for centered-root singular-value energies $\lambda_i=\sigma_i^2$,

$$
p_i=\frac{\lambda_i}{\sum_j\lambda_j},
\qquad
r_{\mathrm{eff}}=\exp\left(-\sum_i p_i\log p_i\right).
$$

This raw ROOT entropy effective rank is reported only as H12 geometry. It cannot
replace frozen-head functional rank. $C_{\mathrm{common}}$ is defined in Section
1.5 and serves only as the E03 eligibility gate.

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: exact full-rank replay. Known bad: shuffled ROOT destroys the
answer. Known confusing: high target accuracy with low unseen-cell accuracy;
such a run is not evidence of reuse.

## 10. Stage-Level Profiling Plan

| Stage | Question | Pass | Artifact |
|---|---|---|---|
| generator | exact counts/splits/marginals? | all exact | generator_audit.json |
| smoke | hooks/checkpoints/three-split replay? | schema complete | smoke/ |
| training | final capability? | capability gates | jobs/* |
| rank | calibration select, test validate? | replay guards | replay_curves.csv |
| merge | non-inferiority? | frozen rule | decision.json |

## 11. Algorithm Specification

Raw checkpoints, logs, and probe vectors stay in the runnable workspace.
Mainline receives only curated records, small tables, and central figures. Any
implementation repair must preserve/version the original output and must not
change thresholds after confirmation test access.

## 12. Success / Failure / Insufficient Evidence

The Approval Snapshot rules are binding. The E02 verdict and the E03 execution
gate are distinct: E03 may run after a frequency fail if capability,
rank-validity, and common-space gates all pass; otherwise E03 is parked.

## 13. What This Cannot Claim

In particular, E01's $K$ trend and E02 frequency non-inferiority cannot be
combined into a universal causal law that mapping count determines rank.

## 14. Review Notes And Protocol Changes

- 2026-07-26: the researcher approved the exact unseen-cell definition and
  lowered its final-accuracy gate from the candidate 0.90 to 0.75 for the small
  sample/model; all other definitions and thresholds were approved.
- 2026-07-26: local two-GPU full execution and gated E03 continuation approved.
