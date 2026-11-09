---
experiment_id: A15_08_E01_layer25_conditional_innovation_matrix
anchor_id: 15_08_target_conditioned_layer_innovation
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN
canonical_language: en
approved_scope: implementation_smoke_and_one_full_run
approved: 2026-08-10
design_frozen_at: 2026-08-10T17:17:37Z
registered_revision: A15_08_E01_v1
---

# Protocol: A15_08_E01 Layer-25 Conditional Innovation Matrix

## 0. Approval Snapshot

- **Document status:** `APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN`.
- **Approval basis:** the researcher explicitly requested that the three proposed approaches be designed and executed without another approval pause on 2026-08-10.
- **Block audit:** A--G `CONFIRMED` under that delegated design authority.
- **Cross-block consistency:** `PASS`.
- **Purpose:** determine whether a named deep-layer write adds target-related linear accessibility beyond the old token state, then test whether two directions retain most of the validated gain.
- **Primary Anchor:** A15_08 Target-Conditioned Layer Innovation.
- **Anchor question:** at the answer token, does the actual layer-25 attention-to-MLP input update add held-out terminal-code prediction value beyond the pre-write state; if so, are two conditional-innovation directions sufficient?
- **Experiment role:** metric audit followed by a gated low-rank operationalization test.
- **Primary metric:** \(G_{full}\), the confirmation cross-entropy reduction from adding the true update after fitting the old-state readout, in nats/example.
- **Minimal setup:** frozen local Qwen3-8B; 128/64/128 independent TRAIN/DEVELOPMENT/CONFIRMATION mapping episodes; eight terminal codes; paired one-hop and two-hop queries; answer token; block 25.
- **Treatment:** old state plus the true normalized attention update.
- **Primary control:** old state alone; update shuffled cyclically across the eight targets inside each episode is the matched nuisance control.
- **Held fixed:** prompt context, terminal answer, class balance, model, token, hook, normalization, readout family, split roles, layer, bootstrap, and selection rules.
- **H2 Pass:** positive lower 95% paired-episode bootstrap bounds for both true full-update gain and true-minus-shuffled gain.
- **H2 Fail:** valid guards and a non-positive upper 95% bound for full-update gain.
- **H2 Insufficient:** every other eligible outcome, or a validity guard failure.
- **H1 Pass:** only after H2 Pass; \(G_2-0.8G_{full}\) has a positive lower 95% bound and \(G_2\) exceeds the q95 of both rank-two random and TRAIN-label-permuted controls.
- **H1 Fail:** after H2 Pass, \(G_2-0.8G_{full}\) has a negative upper bound or \(G_2\) does not exceed either q95 control.
- **H1 Insufficient:** every other eligible gated outcome.
- **Cannot claim:** Shannon-information creation, nonlinear novelty, parameter knowledge storage, native MLP use, expert utility, Router gain, natural-language generality, or a universal depth law.
- **Approval decision:** implementation, model/data smoke, and one complete registered run are authorized. Graph edit, root sync, collaborator sync, commit, push, and Router training are not authorized.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object | Decision role | Cannot prove |
| --- | --- | --- | --- | --- |
| old state \(X\) | what the token already exposes before layer-25 attention writes | \(N_{25}(h)\) at the final `Answer:` token | conditioning variable | complete information in the sequence |
| new state \(Z\) | the matched state after the write | \(N_{25}(h+a)\) with the same \(N_{25}\) | exact post-write comparison | Router or MLP use |
| update \(U\) | what the named computation writes | \(Z-X\) | full candidate increment | target relevance or novelty |
| common pooled basis \(V_{pool}\) | one label-free coordinate shared by old and new states | eigenbasis of TRAIN pooled covariance of episode-centered \(X\) and \(Z\) | locates variance and matrix mass | new information |
| update residual \(R_U\) | update not predicted by the registered linear old-state model | cross-fitted \(U-\hat U(X)\) | input to target matrix | nonlinear unpredictability |
| target residual \(R_Y\) | answer contrast not predicted by the old-state readout | cross-fitted centered one-hot target minus \(\hat Y(X)\) | target error the update may explain | semantic or functional identity |
| conditional innovation matrix | target-related residual-update covariance | \(K_{new}=C_{UY}S_Y^+C_{UY}^{\top}\) | learns candidate directions | evidence before confirmation |
| conditional gain | how much a frozen added input improves target prediction | old-only CE minus augmented CE | H2/H1 evidence | native model use |
| episode | one independently sampled pair of bijections containing all eight targets | one complete \(U\to V\to C\) world | bootstrap and split unit | token-level independence |

## 2. Anchor Alignment

The Protocol instantiates the Anchor's exact \(X,Z,U\) relation, its conditional innovation matrix, the H2 full-update gain, and the gated H1 two-direction retention test. It does not redefine new information as variance, covariance difference, update-only readability, local spectral rank, or direction stability.

The strongest rival is redundant re-encoding: \(U\) can be nonzero, structured, low-rank, and readable alone while adding no held-out value beyond \(X\). Old-only versus old-plus-update and matched shuffled controls separate this rival.

## 3. Tested Hypotheses

- **H2:** for complex two-hop queries, the true \(U\) lowers untouched confirmation terminal-code cross-entropy beyond \(X\), and the reduction exceeds a within-episode cyclic target mismatch of \(U\).
- **H1, gated:** conditional-innovation coordinates 1--2 retain at least \(80\%\) of full-update gain and exceed two equal-rank null families.
- **Secondary complexity contrast:** report the same quantities for paired one-hop queries and complex-minus-simple differences. They cannot rescue either primary clause.

## 4. Rival Explanations

| Rival | Registered separator |
| --- | --- |
| nonzero update is only computation motion | old-only versus old-plus-update confirmation CE |
| update repeats information in old state | conditional correction and update-from-old residualization |
| added branch wins only from extra capacity | cyclic within-episode shuffled-update correction with the same fitting budget |
| target matrix overfits eight-class labels | untouched episodes plus 64 full-pipeline TRAIN-label permutations |
| learned directions merely find a favorable two-plane | 64 rank-two random subspaces from the TRAIN residual-update row space |
| context or wording identifies the answer | independent episodes, balanced codes, split-specific wording, episode-level split and bootstrap |
| common PCA creates the result | common basis is diagnostic only and never selects the primary directions |
| CCA/Procrustes alignment erases or invents change | no old/new alignment is fitted; matched residual coordinates are used directly |
| model cannot solve the task | restricted-choice capability gates for simple and complex conditions |
| eight classes make low rank automatic | H1 requires two, not merely at most seven, directions to retain registered gain |

## 5. Data Construction And Provenance

The generator creates two independent random bijections over eight symbols in each episode: source-to-intermediate \(U_i\to V_j\) and intermediate-to-terminal \(V_j\to C_k\), where \(C_k\in\{A,\ldots,H\}\). Every episode includes all eight terminal targets exactly once in each condition.

- TRAIN: 128 episodes, generation seed 5101, symbolic mapping wording family.
- DEVELOPMENT: 64 episodes, seed 5102, lookup-table wording family.
- CONFIRMATION: 128 episodes, seed 5103, prose-table wording family.
- Total: \(320\times8\times2=5{,}120\) records.
- One-hop and two-hop records in a pair share the exact context, intermediate, terminal answer, and answer vocabulary. Only whether the query starts at \(V\) or \(U\) changes.
- The prompt ends at `Answer:` and never contains the answer afterward. Codes A--H must each be one tokenizer token with a leading space.
- No mapping episode, wording template, record, or pair crosses split boundaries.
- Every data manifest records schema, source code hash, seeds, counts, balance checks, prompt-family IDs, and file SHA-256.

The data are newly generated for this Protocol. Prior controlled-composition data nominate the model/site but do not fit directions, hyperparameters, thresholds, or readouts here.

## 6. Learning Task And Permitted Supervision

The frozen-model analysis predicts the eight-way terminal code at the final prompt token.

- **Permitted operational inputs:** \(X\), \(Z\), \(U\), or registered projections/residuals computed from \(X\) and \(U\).
- **TRAIN labels:** may fit old-state and update ridge readouts, residualizers, the innovation matrix, and null directions.
- **DEVELOPMENT labels:** may select ridge strengths and generalized-eigen regularization from fixed grids.
- **CONFIRMATION labels:** may be opened only after every model, direction, rank, regularizer, permutation seed, and verdict rule is frozen.
- **Forbidden:** confirmation labels in centering, basis fitting, residualization, direction construction, rank selection, threshold selection, exclusions, or plot-range selection.

Success means additional accessibility only within this target and linear readout family. It does not mean the model or Router uses the signal.

## 7. Model / Architecture And Frozen Variants

- Frozen `/data/share/Qwen3-8B`, local tokenizer and weights, bfloat16 forward, SDPA, `use_cache=False`.
- Block index 24, reported as layer 25.
- Forward-pre-hook captures block residual \(h\); `self_attn.o_proj` forward-hook captures attention write \(a\).
- At the final non-padding token, use the block's same `post_attention_layernorm` for \(X=N(h)\) and \(Z=N(h+a)\); store float32 difference \(U=Z-X\).
- Persist `record_id`, condition, split, episode, target, \(X\), \(Z\), \(U\), restricted-choice logits, tensor hashes, and an extraction manifest.
- No parameter-SVD basis, CCA, Procrustes, trainable backbone, MLP, expert, or Router is used.

The readout and residualization family is ridge regression in dual form. Feature centering and scalar RMS scaling use TRAIN only and preserve rotations; per-coordinate standardization is forbidden.

## 8. Training Objective And Optimization

All fitted components are closed-form ridge models; no gradient training occurs.

1. **Old target readout:** minimize mean squared centered-one-hot error from \(X\) plus \(\lambda\|W\|_F^2\); select \(\lambda\) by DEVELOPMENT cross-entropy.
2. **Full update correction:** freeze the old model, fit \(U\) to the TRAIN target residual, and select correction \(\lambda\) by DEVELOPMENT cross-entropy.
3. **Update residualizer:** predict \(U\) from \(X\) by ridge, selecting \(\lambda_U\) by DEVELOPMENT reconstruction MSE. TRAIN residuals are four-fold cross-fitted by complete episode.
4. **Target residualizer:** obtain four-fold episode-cross-fitted old-state target residuals on TRAIN using the DEVELOPMENT-selected old-state \(\lambda\).
5. **Conditional directions:** construct \(K_{new}\) from cross-fitted complex TRAIN residuals; solve the generalized eigenproblem against \(\Sigma_{R_U}+\rho I\).
6. **Direction selection:** choose \(\rho\) from the fixed grid by complex DEVELOPMENT rank-two correction CE; rank is frozen at two.
7. **Nulls:** repeat the same direction construction for 64 TRAIN within-episode target permutations; draw 64 rank-two random subspaces from the TRAIN residual-update row span. Correction readouts receive identical ridge grids.

Ridge grid: \(\{10^{-4},10^{-3},10^{-2},10^{-1},1,10,100,1000\}\). Ties choose the larger regularization. Generalized-eigen ridge is \(\rho/\bar\sigma_U^2\in\{0.01,0.1,1,10\}\), where \(\bar\sigma_U^2=\operatorname{tr}(\Sigma_{R_U})/d\).

## 9. Conditions, Seeds, And Checkpoints

| Condition | Changed object | Purpose | Decision role |
| --- | --- | --- | --- |
| old-only | no update branch | baseline | primary |
| old + true full update | actual \(U\) | H2 existence | primary |
| old + cyclic-shuffled update | target-mismatched \(U\) inside episode | equal-capacity nuisance control | primary guard |
| old + two innovation coordinates | \(P_2^{\top}R_U\) | H1 retrieval | gated primary |
| old + random rank-two coordinates | 64 row-span random subspaces | geometry null | H1 control |
| old + permuted-label rank-two coordinates | 64 full-pipeline label nulls | supervised-overfit null | H1 control |
| new-state only | \(Z\) with matched readout budget | current-state capacity guard | secondary |
| update only | \(U\) | distinguish readability from conditional gain | secondary |

- Data seeds: 5101/5102/5103.
- Four TRAIN cross-fit folds: episode ID modulo 4.
- Bootstrap: 2,000 paired episode resamples, seed 5181.
- Random rank-two subspaces: seeds 5200--5263.
- Label permutations: seeds 5300--5363; labels permute across the eight target assignments inside every TRAIN episode.
- No checkpoints exist because the model is frozen and fitting is closed form.

## 10. Primary Metric And Frozen Analysis Plan

For each confirmation record, let \(\ell_0\) be old-only cross-entropy and \(\ell_{full}\) old-plus-true-update cross-entropy. The complex-condition full gain is

\[
G_{full}=\frac1N\sum_i(\ell_{0,i}-\ell_{full,i})
\]

in nats/example. Positive means the true update improves the registered old-state readout.

The matched nuisance contrast is

\[
T_{shuffle}=G_{full}-G_{shuffle}.
\]

The unit of observation is a prompt; the unit of independence is the complete episode. Every episode receives equal weight, and all eight targets within it remain together in each of 2,000 paired bootstrap draws. Report percentile 95% intervals.

H2 uses the two simultaneous requirements \(LCB_{.95}(G_{full})>0\) and \(LCB_{.95}(T_{shuffle})>0\). H2 Fail requires \(UCB_{.95}(G_{full})\le0\). No multiplicity correction is needed because these form one conjunctive gate, not alternative discoveries.

For H1, let \(G_2\) be the same gain using two innovation coordinates and

\[
D_{80}=G_2-0.8G_{full}.
\]

H1 requires \(LCB_{.95}(D_{80})>0\) plus \(G_2\) greater than the empirical q95 of both 64-control gain families. H1 is not evaluated unless H2 passes.

Missing records, nonfinite values, schema imbalance, model/hook guard failure, incomplete null families, or any confirmation leakage makes the affected clause `INELIGIBLE`; no outlier or episode exclusion is allowed.

## 11. Secondary Metrics And Guards

- Restricted-choice capability: simple confirmation accuracy \(\ge0.80\) and complex \(\ge0.60\).
- Exact difference reconstruction: \(\|Z-X-U\|/\|U\|\le10^{-6}\) in stored float32 values.
- Same-run attention-write replay maximum absolute error \(\le10^{-5}\) on the first smoke batch.
- Direct `o_proj` identity relative error \(\le10^{-5}\).
- Exact split/episode/condition/target balance.
- Common-basis orthogonality relative error \(\le10^{-5}\) and covariance trace reconstruction relative error \(\le10^{-4}\).
- Covariance-difference identity relative Frobenius error \(\le10^{-5}\).
- Full-update, shuffled, rank-two, new-state-only, and update-only confirmation CE.
- Conditional-innovation eigenvalue spectrum, top-one/top-two mass, and its mass over common pooled-basis rank.
- Complex-minus-simple gains are descriptive and cannot rescue H2/H1.

## 12. Known Good / Known Bad / Known Confusing Cases

Before model extraction, deterministic synthetic tests must pass:

- **Known good:** \(Y\) enters \(U\) through a planted rank-two signal independent of \(X\); H2 gain is positive and the recovered two-plane has high planted-subspace overlap.
- **Known bad:** \(U\) is target-independent noise after conditioning on \(X\); conditional gain and innovation spectrum are near the null.
- **Known confusing:** \(X\) already contains the full target signal and \(U\) repeats it; update-only readability is high but conditional gain is near zero.
- **Algebraic identity:** matched \(Z=X+U\) and covariance decomposition reconstruct numerically.
- **Leakage guard:** moving any episode rows across split or cross-fit folds is rejected.

Synthetic thresholds verify implementation behavior only; they do not adjudicate Qwen3-8B.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input | How / why | Output | Pass / stop | Named failure | Handoff |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S0 data | construct independent balanced pairs | registered seeds/templates | generate all eight targets per episode; validate tokenization-independent schema | data JSON + manifest | exact counts/balance | data construction | S1 |
| S1 metric preflight | show the estimator distinguishes known cases | synthetic arrays | run known-good/bad/confusing tests and algebraic identities | unit-test log | all tests pass | metric/implementation | S2 |
| S2 model smoke | validate model, task, and hooks cheaply | 16 episodes/split | forward layer 25, replay first batch, compute restricted-choice logits | smoke tensors + manifest | hook guards and capability pass | capability/site | S3 |
| S3 full extraction | obtain frozen representations | complete 5,120 records | run simple and complex shards on two H100s, store \(X,Z,U\) | extraction tensors/manifests | complete hashes/schema | execution/artifact | S4 |
| S4 common-coordinate audit | locate changes without target selection | TRAIN \(X,Z,U\) | pooled covariance basis and covariance decomposition | common-basis tables/figure | numerical guards pass | coordinate/metric | S5 |
| S5 conditional matrix | learn candidate target directions | TRAIN/DEV only | cross-fit residuals, build \(K_{new}\), select \(\rho\), freeze \(P_2\) | direction/eigenvalue ledger | no confirmation access | leakage/overfit | S6 |
| S6 confirmation | adjudicate H2 and gated H1 | frozen models/directions + confirmation | CE comparisons, controls, episode bootstrap | primary table/figure/verdict JSON | registered mapping | scientific result | S7 |
| S7 records | preserve evidence and reader explanation | complete eligible artifacts | conformance, lineage, curated copy, canonical records, daily report | summary/detailed/report | cross-file audit pass | evidence/report | human review |

## 14. Algorithm, Output, And Provenance Contract

Worker code root:

`Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_08_e01_layer25_conditional_innovation/`

Worker result root:

`.../runs/a15-08-e01-full-20260810/`

Canonical record root:

`Projects/from-attention-to-search/main/experiments/A15/15_08_target_conditioned_layer_innovation/A15_08_E01_layer25_conditional_innovation_matrix/`

Required worker artifacts:

- data JSON and manifest;
- synthetic test log;
- smoke manifest and tensors;
- simple/complex extraction tensors, logits, and manifests;
- common-basis and covariance-decomposition tables;
- frozen model-selection ledger;
- full per-record losses and per-episode aggregates;
- random/permutation control ledgers;
- primary result JSON/CSV;
- plot contracts, PNG/PDF figures, and artifact manifest;
- stdout/stderr logs and environment receipt.

Resource ceiling: two local H100 80GB GPUs, two wall-clock hours for model extraction, five wall-clock hours total, and 10 GiB worker disk. Any OOM, nonfinite output, guard failure, or missing condition stops before confirmation interpretation.

Central figures are frozen as: (1) common-basis old/new/update/innovation mass; (2) confirmation gains for true full update, two innovation directions, shuffled, random q95, and permutation q95 with episode intervals. Figures use source CSVs and cannot determine the verdict independently.

## 15. Success / Failure / Insufficient Evidence

- `H2_PASS_H1_PASS`: H2 conjunctive gate passes and gated H1 passes.
- `H2_PASS_H1_FAIL`: H2 passes and gated H1 fails.
- `H2_PASS_H1_INSUFFICIENT`: H2 passes and gated H1 remains ambiguous.
- `H2_FAIL_H1_NOT_ADJUDICATED`: H2 fails; H1 is not interpreted.
- `H2_INSUFFICIENT_H1_NOT_ADJUDICATED`: H2 interval or matched control is unresolved.
- `INELIGIBLE_GUARD`: a required construction, capability, hook, leakage, numerical, or artifact guard fails.

No secondary plot, update-only readout, simple-condition result, or common-basis localization can upgrade these outcomes.

## 16. What This Cannot Claim

Even a joint Pass does not establish information-theoretic novelty, nonlinear uniqueness, natural semantic knowledge, model-native use, causality, MLP function, expert specialization, expert utility, Router loss improvement, trainability, or generalization beyond the frozen controlled-composition object. It admits only a later independent functional experiment.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A question/boundary | CONFIRMED | 2026-08-10 researcher instruction and approved A15_08 Anchor |
| B data/provenance | CONFIRMED | researcher requested obvious matched pairs and delegated exact construction |
| C task/supervision | CONFIRMED | frozen terminal-code target and explicit TRAIN/DEV/CONFIRMATION roles |
| D model/architecture | CONFIRMED | frozen Qwen3-8B, layer-25 site nominated by verified prior evidence |
| E objective/optimization | CONFIRMED | linear conditional-accessibility definition and delegated method choice |
| F comparison/evidence | CONFIRMED | three requested method views, primary conditional gain, registered nulls |
| G execution/reproducibility | CONFIRMED | explicit instruction to complete the experiment; local two-H100 ceiling |

Cross-block consistency audit: `PASS`. The data expose the target relation; supervision obeys split roles; architecture realizes the named objects; the objective represents conditional accessibility; controls isolate redundancy and supervised overfit; confirmation cannot select the method; resources cover all conditions; verdicts map to the Anchor boundary.

The scientific body is frozen at revision `A15_08_E01_v1` before data generation. After the first execution command, only execution receipts, result links, or append-only amendments with before/after values, timing, approval basis, and eligibility impact may be added. No silent post-start change is eligible.

### Amendment A1 — verified dependency environment for smoke retry

- **Time:** 2026-08-10T17:33:30Z, after the first smoke launch and before any model forward pass.
- **Observed failure:** both condition processes stopped at Python import with `ModuleNotFoundError: No module named 'transformers'`.
- **Before:** invoke the system Python process without sourcing the project-verified dependency environment.
- **After:** source `../a15_01_09_e01_qwen3_mlp_parameter_commonality_attention_write_semantic_location/scripts/env.sh` before invoking the unchanged extraction command. This environment exposes the previously installed `transformers==4.51.3` and `torch==2.3.0a0+git7f1453a` stack.
- **Approval basis:** execution-environment repair is within the researcher-authorized implementation, smoke, and full-run scope.
- **Eligibility impact:** none. The failure occurred before model loading, data access, hook execution, metric computation, or result observation. Data hashes, model, site, sample counts, estimators, thresholds, and verdict rules remain unchanged. The original failed logs are retained; the retry uses a new run directory.

### Amendment A2 — remove an unsupported redundant CLI argument

- **Time:** 2026-08-10T17:36:17Z, after retry A1 and still before any model forward pass.
- **Observed failure:** `argparse` rejected `--condition simple` and `--condition complex`; `extract.py` derives and validates the unique condition from each registered data file and does not expose a `--condition` option.
- **Before:** pass both the condition-specific data path and a redundant unsupported `--condition` argument.
- **After:** remove only the unsupported argument; retain the same condition-specific data paths, output separation, devices, batch size, and smoke sample ceiling.
- **Approval basis:** correcting a command-to-script interface mismatch is within the authorized implementation and execution scope.
- **Eligibility impact:** none. Argument parsing stopped both processes before model loading or data reading. No scientific object, data, method, threshold, or evidence was observed or changed. Both failed retry logs are retained; the next retry uses another new run directory.

### Clarification A3 — validity guards map to ineligible, not scientific insufficient

- **Time:** 2026-08-10T17:45:10Z, after extraction and before confirmation analysis.
- **Ambiguity found:** the Approval Snapshot's shorthand H2-Insufficient sentence includes “validity guard failure,” while Sections 10 and 15 explicitly map any required guard failure to `INELIGIBLE_GUARD`.
- **Controlling interpretation:** Sections 10 and 15 govern. A failed required data, capability, hook, numerical, leakage, null-family, or artifact guard produces `INELIGIBLE_GUARD`; `H2_INSUFFICIENT_H1_NOT_ADJUDICATED` is reserved for an eligible but statistically unresolved scientific comparison.
- **Approval basis:** this resolves an internal status-label contradiction without changing any guard, threshold, scientific comparison, or decision boundary.
- **Eligibility impact:** none. It prevents a validity failure from being misreported as scientific uncertainty.

### Execution and post-result evidence ledger

- **Completed:** 2026-08-10; 5,120 full records, two H100s for extraction, one H100 plus CPU linear algebra for analysis.
- **Selection freeze:** `frozen_selection_ledger.json` was written before confirmation conditional losses with SHA-256 `2dddc9bf938ce71560142118790fbd3e94815c7363009e11c21620820855b5ee`.
- **Mechanical registered label:** `H2_INSUFFICIENT_H1_NOT_ADJUDICATED`.
- **Primary values:** \(G_{full}=0.661428\) [0.646973, 0.675533] and \(T_{shuffle}=-0.026983\) [-0.030384, -0.023705] nats/example.
- **Post-result construct qualification:** `PRIMARY_H2_INELIGIBLE_CONTROL_DESIGN`. The globally fixed cyclic target map was invertible and separately learned in every split, so it did not instantiate the intended target-independent capacity control. The registered arithmetic label is retained, but E01 cannot adjudicate H2 scientifically.
- **H1' audit:** not adjudicated; additionally, raw \(U\) defined the full reference while \(R_U\) defined the rank-two reference, and null search budgets did not match the real four-\(\rho\) selection.
- **Canonical result SHA-256:** `613e081c984f692fe102e523f53277b38c1b4a9988b654ae18bc654e445cf8a2`.
- **Records:** [summary.md](summary.md), [detailed.md](detailed.md), and [evidence/result.json](evidence/result.json).
- **Authorized repair:** [A15_08_E02](../A15_08_E02_fresh_balanced_mismatch_repair/protocol.md) is a new fresh-data experiment, not an amendment to the opened E01 confirmation set.
