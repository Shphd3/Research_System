# Protocol: A06_03_02_E01 Learned-Specialist Rank-Mediated Correction

## 0. Approval Snapshot

**Approval status:** Approved for execution under the persistent research goal
on 2026-07-10.

**Purpose:** Test whether native weighted top-1 can discover a learned useful
expert that starts below top-1, and whether exposing all expert outputs removes
a rank-conditioned correction delay.

**Primary anchor:**
`../../../../problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md`

**Decision question:** With learned specialists, representation, score ladder,
and load controlled, does weighted top-1 recover a useful expert from initial
rank 2 or 4 as reliably and efficiently as a utility-bearing soft mixture?

**Primary statistic:** paired capped correction-time penalty at rank 4,

\[
D_{corr}=\operatorname{median}_{f,seed}
\left[\widetilde T_{corr}^{top1,rank4}
-\widetilde T_{corr}^{soft,rank4}\right].
\]

**Minimal setup:** Deterministically rebuild A06_03_01_E01 specialists and balanced
generalists; freeze experts and representation; initialize one shared four-level
score ladder with the useful expert at rank 1, 2, or 4; train only the router
under full-sequence LM loss.

**Primary conditions:** specialist top-1 and soft mixture at ranks 1, 2, 4.

**Specificity guards:** generalist top-1 and soft mixture at rank 4.

**Support for sparse discovery bottleneck:** rank-4 top-1 has a correction-time
penalty above five updates with positive clustered-CI lower bound and larger
normalized cumulative regret than rank-4 soft mixture.

**Support for no material bottleneck:** both rank-4 methods correct at least 90%
of cells, the correction-time penalty CI upper bound is at most five updates,
and the normalized-regret gap CI upper bound is at most 0.05.

**Insufficient:** specialist utility, rank geometry, state identity, coverage,
finite trajectory, or soft positive-control guard fails.

**Cannot claim:** label-free discovery, natural-language semantic experts,
production sparse-compute speedup, or that soft routing is a final method.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Useful expert | Learned specialist with lowest forced held-out task loss | expert \(u(f)=f\) after correct exposure | functional target | natural semantics |
| Initial useful rank | Position of \(u(f)\) in router score order | 1, 2, or 4 on task positions | controlled search distance | natural initialization frequency |
| Sustained correction | Useful expert remains top-1 across a short window | route accuracy \(\ge0.95\) for 5 consecutive updates | rejects one-step crossings | permanent convergence |
| Capped correction time | Correction time with failures assigned horizon plus one | \(\widetilde T_{corr}=\min(T_{corr},301)\) | includes censored cells | exact survival model |
| Correction rate | Fraction corrected by update 300 | \(C_k(300)\) | coverage co-evidence | efficiency among corrected cells |
| Normalized cumulative regret | Average held-out routing excess relative to its initial value | \(NR=(301)^{-1}\sum_t [E(t)]_+/[E(0)]_+\) | task-learning efficiency | wall-clock efficiency |
| Forward utility coverage | Which expert outputs affect the loss | one output for top-1, four for soft mixture | mechanism intervention | equal activated compute |

## 2. Anchor Alignment

A06_03_01_E02 closes the correct-top-1 confidence question. A06_03_02_E01 changes the useful
expert's score rank so that relative identity utility becomes causally relevant.
The soft condition tests whether utility-bearing forward exposure, rather than
score geometry alone, changes correction.

## 3. Tested Hypotheses

For capped times and normalized regret, use paired seed-clustered 95% bootstrap
confidence intervals.

- **H1 rank-mediated top-1 correction:**
  \(\widetilde T^{top1}_{rank4}-\widetilde T^{top1}_{rank2}>5\) updates and
  \(NR^{top1}_{rank4}-NR^{top1}_{rank2}>0\), both with positive CI lower bounds.
- **H2 utility-coverage advantage:** \(D_{corr}>5\) updates and
  \(NR^{top1}_{rank4}-NR^{soft}_{rank4}>0\), both with positive CI lower bounds.
- **H3 no material sparse bottleneck:** both rank-4 correction rates are at
  least 0.90, \(D_{corr}\) CI upper bound is at most 5, and normalized-regret-gap
  CI upper bound is at most 0.05.
- **H4 target specificity:** balanced generalists do not show reliable recovery
  to the arbitrary expert-id target. This is supporting evidence, not a
  validity requirement.

Mixed time/regret evidence is reported as mixed, not forced into H2 or H3.

## 4. Rival Explanations

1. **Rank geometry differs:** use one score multiset
   \([0.75,0.25,-0.25,-0.75]\) and only permute expert identities.
2. **Initial load differs:** use cyclic task-wise permutations so every expert
   is top-1 for exactly one task.
3. **Top-1 and soft start differently:** clone the exact router tensor and all
   model state before changing only the forward aggregation rule.
4. **The specialist target disappeared:** recompute held-out forced-expert loss
   matrix and require median utility gap above 5.
5. **The horizon is too short:** use 300 updates, capped-time accounting, and
   report correction rate explicitly.
6. **Soft only changes optimizer scale:** use the same router-only SGD and
   learning rate; report actual update norm and activated functional paths.
7. **A geometric label is being recovered without function:** generalist rank-4
   controls retain the same geometry but remove a unique expert target.

## 5. Data, Model, And Objective

Reuse A06_03_01_E01/A06_03_01_E02 exactly:

- four equally frequent sequence-level modular transformations;
- sequence-start instruction \(f\) and targets \((c+f)\bmod4\);
- sequence length 33 with sixteen content/output pairs;
- all 32 autoregressive positions enter the training loss;
- 32 train and 32 disjoint held-out sequences per seed;
- one causal attention layer, fixed instruction-state visibility control,
  residual plus LayerNorm, no learned positional embedding;
- four MLP experts, fixed readout, and linear router.

Specialist/generalist exposure lasts 200 expert-only AdamW updates. Correction
freezes experts and representation and trains only router rows with full-batch
SGD, learning rate 0.001, no momentum or weight decay.

### Forward rules

Weighted top-1:

\[
y=h+p_rE_r(h),\qquad r=\arg\max_j s_j.
\]

Soft mixture:

\[
y=h+\sum_jp_jE_j(h).
\]

The implementation may materialize all expert tensors for convenience, but
only outputs appearing in \(y\) count as activated functional paths. No system
throughput claim is made.

## 6. Rank Construction

Let task centers be rows of \(C\in\mathbb R^{4\times d}\). For each task, assign
the score ladder \([0.75,0.25,-0.25,-0.75]\) to expert identities so that useful
expert \(f\) has requested rank \(k\). The other experts use cyclic order
\(f+1,f+2,f+3\); therefore the selected wrong expert is the same at rank 2 and
rank 4 and top-1 load remains balanced.

Solve the minimum-norm router:

\[
W^\top=C^+S.
\]

Required step-0 guards on train and held-out task positions:

- useful-rank accuracy at least 0.999;
- p05 adjacent score gap at least 0.40;
- top-1 expert-count spread exactly zero;
- train construction-center score error at most \(5\times10^{-4}\);
- top-1/soft paired router and non-router state error at most \(10^{-7}\).

Held-out centers are not required to reproduce the train target matrix exactly;
their validity is guarded directly by held-out useful-rank accuracy and p05
adjacent score gap. This separates sampling drift from condition mismatch.

No position labels or route-position identifiers enter the model.

## 7. Conditions, Seeds, And Horizon

| Expert state | Forward rule | Useful rank | Role |
| --- | --- | ---: | --- |
| Specialist | weighted top-1 | 1 | correct-route guard |
| Specialist | weighted top-1 | 2 | short search |
| Specialist | weighted top-1 | 4 | strongest sparse-feedback stress |
| Specialist | soft mixture | 1 | soft stability guard |
| Specialist | soft mixture | 2 | matched utility-coverage control |
| Specialist | soft mixture | 4 | primary positive control |
| Generalist | weighted top-1 | 4 | geometry-without-target guard |
| Generalist | soft mixture | 4 | soft geometry-without-target guard |

Formal seeds: 0--31. Correction horizon: 300. Evaluate held-out task loss,
route state, score ranks, and router update every update. Sustained window:
five updates. Smoke: two seeds, full 200-step exposure, 50 correction updates.

## 8. Metrics

For task \(f\) with frozen forced useful-expert floor \(L_{f,u}^{cf}\):

\[
E_f(t)=L_f^{native}(t)-L_{f,u}^{cf},
\]

\[
NR_f(T)=\frac1{T+1}\sum_{t=0}^T
\frac{[E_f(t)]_+}{\max([E_f(0)]_+,10^{-12})}.
\]

Report:

- capped sustained correction time and correction rate;
- normalized cumulative regret;
- useful-expert probability and rank trajectory;
- task-level majority selected expert and boundary-change count;
- native task/all-position loss and forced floor;
- router gradient/update norms;
- specialist utility retention and generalist interchangeability.

## 9. Stage-Level Profiling

| Stage | Question | Pass | Failure meaning | Artifact |
| --- | --- | --- | --- | --- |
| Exposure rebuild | Is learned utility reproduced? | specialist gap \(>5\), generalist \(|gap|<0.5\) | no functional target/control | exposure audit |
| Rank construction | Are ranks/gaps/load exact? | all registered guards | geometry confound | rank audit |
| Step 0 pairing | Do top-1 and soft start identically? | max error \(\le10^{-7}\) | invalid comparison | state audit |
| Early correction | Which boundaries are crossed? | diagnostic | mechanism trajectory | rank/identity plot |
| Horizon 300 | Does useful identity recover? | H1--H3 rules | decision | correction plot/table |
| Generalist guard | Does arbitrary identity recover? | supporting only | geometric target bias | specificity table |

## 10. Plot Contracts

### Figure 1: Useful-Expert Correction Curves

- Unit: fraction not yet sustainably corrected.
- X-axis: router updates; lines: method and initial rank.
- Allowed conclusion: correction coverage and latency ordering.
- Limitation: controlled context task only.

### Figure 2: Normalized Cumulative Regret

- Unit: fraction of initial routing excess, integrated through time.
- X-axis: updates; Y-axis: median normalized excess remaining.
- Allowed conclusion: task-learning efficiency conditional on the fixed expert
  floor.
- Limitation: not wall-clock or FLOP-normalized efficiency.

### Figure 3: Rank-4 Identity Search

- Unit: useful-expert rank/probability and cumulative majority-boundary changes.
- Allowed conclusion: sequential search versus direct utility coverage.
- Limitation: does not identify a production candidate-selection rule.

## 11. Success, Failure, And Insufficient Evidence

**Sparse discovery bottleneck:** H2 passes; H1 supplies rank-mediated support.

**No material bottleneck:** H3 passes.

**Rank effect without soft advantage:** H1 passes but H2 does not; the cause is
not specifically missing forward utility coverage.

**Soft advantage without rank effect:** H2 passes but H1 does not; report a
forward-rule advantage without a rank-search claim.

**Insufficient:** fewer than 32 seeds; any rank/state/utility/finite guard fails;
or soft rank-4 correction rate is below 0.90.

## 12. Artifact Contract

- Config: `configs/a06_40_learned_specialist_rank_correction.json`.
- Runner: `scripts/run_a06_40_learned_specialist_rank_correction.py`.
- Four-GPU submitter:
  `scripts/submit_a06_40_learned_specialist_rank_correction_4gpu_acp.sh`.
- Formal run name: `a06_40_full_4gpu_20260710_01`.
- Output root:
  `results/a06_40_learned_specialist_rank_correction/<run_name>/`.

## 13. Review Notes

- Router-only SGD preserves the clean selected-versus-unselected gradient
  distinction.
- The 0.001 learning rate is ten times the A06_03_01_E02 diagnostic SGD rate so that a
  0.5 score ladder can cross multiple boundaries within 300 updates; rank-1
  stability is a mandatory guard.
- Capped time prevents censored rank-4 cells from being silently dropped.
- Soft mixture is a mechanism positive control with four utility-bearing expert
  outputs; it cannot be declared the final gating method from this experiment.
