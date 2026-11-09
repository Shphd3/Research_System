# Detailed: A15_13_E14_P3 Matched Training and Semantic Supervision Comparison

Primary Anchor: [A15_13_05](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md).  
Frozen Protocol and registered revision: [Protocol](protocol.md), `20260906-P3-v1` plus approved amendment `20260906-P3-A1`.  
Summary: [canonical first reading path](summary.md).  
Result eligibility: `COMPLETE / ELIGIBLE`; researcher-confirmed typed verdict `INSUFFICIENT`.

## 0. Quick Recap

Purpose: test whether correct train-only pseudo-label supervision improves online answer likelihood
over both task-only and label-shuffled training in one matched hierarchy.

Hypothesis: H-sem has lower test answer NLL than H-task and H-shuf in each of seeds 17 and 29.

Experiment logic: first freeze one development-selected budget and load policy, then train the complete
D/F/SF/H-task/H-sem/H-shuf two-seed matrix and apply a four-effect conjunction on sealed test data.

Direct result: H-task-minus-H-sem is +0.010320 in seed 17 and -0.002078 in seed 29, with both paired
95% intervals excluding zero. H-shuf-minus-H-sem is positive in both seeds.

Eligibility: all 12 core arms completed 512 updates; every guard passed; every required development
and test array exists; paired identities and answer-token counts match; test values are finite; the
primary 57-entry artifact manifest has zero hash mismatches.

Verdict: `INSUFFICIENT`, because the registered conjunction requires H-sem to beat both controls in
both seeds and the H-task comparison reverses.

Claim boundary: the result is about teacher-forced online answer likelihood under this exact frozen
base, clean split, teacher, hierarchy, budget, and two seeds. It is not a semantic-truth,
hierarchy-necessity, expert-function, free-generation, or public-decontamination result.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Answer NLL | Loss assigned to the reference answer | Sum per-record answer-token negative log probabilities, then divide by total answer tokens | nat / answer token; lower is better | Primary task measure | Free-generation accuracy |
| Online route | Route chosen without supplying the offline teacher path | Router reads the current causal block-14 state | discrete parent/leaf plus raw-softmax coefficients | Tests deployable routing at evaluation | Absence of privileged information from teacher construction |
| Pseudo-label teacher | Frozen grouping used only as training supervision | Train-only final-layer whole-window mean, PCA64, diagonal GMM with 3 parents and 3/3/2 leaves | parent/leaf IDs | Defines H-sem and H-shuf targets | Semantic truth or optimal clustering |
| Primary effect | Baseline loss minus H-sem loss | \(L_{baseline}-L_{H\text{-sem}}\) for H-task or H-shuf | nat / answer token; positive favors H-sem | Directly enters the registered conjunction | Cross-seed population generality from two seeds |
| Seed reversal | The same contrast has opposite signs across model seeds | H-task-minus-H-sem, seed 17 versus seed 29 | signed paired effect | Makes the result insufficient | Its mechanism |
| Post-hoc diagnostic | Analysis chosen after the registered result exists | Development trajectories, per-source contributions, route loads, losses, gradients, deltas | descriptive | Selects one next uncertainty | A causal mechanism or a repaired primary verdict |

## 2. Anchor Link And Decision Point

P1/P2 showed that the historical hard-pseudo model omitted parent supervision and that fitting only
the old parent Router repaired most of its online loss. P3 does not reuse those adapted experts. It
restarts all formal models from the frozen Qwen3-0.6B-Base and asks the remaining question: does
sample-specific pseudo-label supervision add task value when a task-only hierarchy is itself trained
jointly and sufficiently under an audited clean split?

The decision point is narrower than teacher or layer selection. A replicated positive H-sem advantage
would retain the teacher as a candidate training signal. A replicated negative necessary contrast
would locally reject it. The observed seed disagreement leaves the value unresolved and requires one
diagnostic branch, not an expanded method search.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Protocol and authority | P3 v1; core 3.2--3.4 approved; conditional arms only on trigger plus decision need | Snapshot SHA-256 `98dadafb4e16...`; approval and A1 recorded before decision evidence | CONFORMANT | [Protocol](protocol.md), worker `protocol_snapshot.md` | Eligible |
| Data and split | 56,538 retained; 39,576/8,481/8,481; zero record/content overlap | Exact counts and zero overlaps reproduced | PASS | [data/teacher receipt](tables/data_teacher_receipt.json) | Eligible |
| Teacher | Train-only PCA64 and converged 3/3/2 diagonal GMM; every train leaf nonempty | Frozen assignment SHA-256 `8a04a8ccd736...`; all selected fits valid | PASS | [data/teacher receipt](tables/data_teacher_receipt.json) | Eligible |
| Core matrix | D/F/SF/H-task/H-sem/H-shuf × seeds 17/29 | 12/12 arms, 512 updates each, 12 test arrays | COMPLETE | [formal receipt](tables/formal_receipt.json) | Eligible |
| Common H comparison | Same architecture, initialization, order, budget, and load policy; H-sem/H-shuf differ only in target association; H-task omits auxiliary terms by design | Same-seed H initial tensor hashes identical; 512/load-off frozen; registered objectives used | PASS | [execution audit](tables/execution_audit.json) | Eligible |
| Budget gate | Registered 384-to-512 rule; A1 permits only 512 and requires stop if trigger fires | No baseline trigger; all final H improvements below 0.002 | PASS | [budget](tables/budget_512.json), [H stability](tables/formal_h_stability.csv) | Eligible at 512 |
| Load gate | Run load-on only for dead expert or concentration plus undertraining | Concentration observed, but no undertraining/dead expert; trigger false; load-off selected | PASS | [load trigger](tables/load_trigger.json), [load policy](tables/load_policy.json) | No load-on run required |
| Primary analysis | Four per-seed effects, 2,000 source-stratified paired-record draws, fixed seed 20260906 | Exact registered estimator and verdict rule used | PASS | [primary effects](tables/primary_semantic_effects.csv), [verdict](tables/verdict.json) | Eligible |
| Mandatory guards | Finite histories, expected gradients/changes, frozen base/head, matched masks and test identities | 12/12 guards pass; paired identities/tokens match; finite; zero manifest mismatches | PASS | [execution audit](tables/execution_audit.json) | Eligible |
| Required figures and records | Summary, Detailed, development and primary figures, artifact map | Canonical records and curated outputs now present | COMPLETE | this directory | No missing canonical deliverable |
| Amendment P3-A1 | Resource/concurrency becomes 4×H100 reserved; 512-only stop branch | Approved before update-384/512 evidence; conditions parallelized; no scientific variable changed | RECORDED DEVIATION | [Protocol §17](protocol.md), [execution audit](tables/execution_audit.json) | Does not change 512 eligibility |
| D seed-17 recovery | Resume only from complete atomic state | Resumed from update 224 with contiguous final history and passed guard | RECORDED RECOVERY | [execution audit](tables/execution_audit.json) | Eligible; no schedule or state-field gap found |
| First smoke attempt | Disposable code-path check only | Failed at update 1 because checkpoint directory did not exist; directory creation fixed; weights excluded | EXCLUDED ENGINEERING FAILURE | worker `run_manifest.json`, stage `smoke_attempt_1` | No formal evidence reused |
| Reversal audit | Must remain post-hoc and no-training | Reads saved development arrays/histories/guards only; separate manifest and figures | BOUNDED POST-HOC | [audit decision](tables/reversal_audit_decision.json), [audit manifest](tables/reversal_audit_manifest.json) | Cannot alter primary verdict |
| H-hard / H-oracle | Run only if trigger and next decision require handoff decomposition | No such next-decision need; only a disposable two-update H-hard smoke path ran | `NOT_RUN_NOT_TRIGGERED` | [smoke receipt](tables/smoke_receipt.json), user-selected follow-up branch | Not missing core evidence |

Frozen Protocol revision: `20260906-P3-v1`; scientific-body snapshot hash
`98dadafb4e169e24a876cd17ffc90de590a7b6cea29ce2d83e5e8a7f3c5b1d9d`.

Execution scope approved: data/teacher construction, disposable smoke, preflight, 12-arm core, sealed
test analysis, and canonical records. Amendment A1 authorized four independent single-GPU condition
workers on one reserved 4×H100 node and replaced the 1024 escalation with a 512-only stop rule.

Retries and exclusions: platform automatic retry was zero. The first disposable smoke attempt is
excluded. D seed 17 used one registered atomic recovery state. No failed or partial formal arm enters
the result.

Missing conditions or artifacts: none in the approved core. Formal H-hard/H-oracle are deliberately
not run. Raw checkpoints and logs remain in the worker workspace as required.

Post-hoc analyses: the reversal audit was requested after the P3 verdict. It is explicitly descriptive,
no-training, and excluded from the registered primary decision.

## 4. Actual Setup

Research question: does true record-to-pseudo-label association improve an online hierarchy over both
task-only and legal-pair-shuffled controls when training and evaluation are matched?

Data construction and provenance: eight frozen sources—MMLU, MMLU-Pro, BBH, GSM8K, MATH, GPQA
Diamond, HumanEval, and MBPP—yield 57,099 rendered rows. Global record-ID and normalized
prompt-plus-answer deduplication removes 561 rows, retaining 56,538. Deterministic source-stratified
70/15/15 splitting yields train/development/test counts 39,576/8,481/8,481 with zero record-ID and
normalized-content overlap. The processed tensor SHA-256 is `b2e1b4c5d435...`. This does not remove
semantic paraphrases or base-model pretraining contamination.

Train / development / test: train supplies gradients and teacher fitting. Development freezes budget
and load policy and later supplies the post-hoc reversal audit. Test remains sealed until configuration,
checkpoints, and analysis rules freeze. Development has 572,552 answer tokens in each audited H arm;
test has 562,954.

Learning task and permitted supervision: every arm optimizes teacher-forced answer-only continuation
NLL. H-sem and H-shuf additionally optimize parent and teacher-parent-conditional child cross entropy.
H-shuf uses one fixed permutation of complete legal parent/leaf pairs, seed 20260906, reused across
model seeds. Online forward passes never receive teacher paths or source IDs.

Model / architecture / algorithm: Qwen3-0.6B-Base is frozen. Low-rank residuals replace only
zero-indexed block 14 MLP `down_proj`. Routers read the 1,024-dimensional block input; experts read the
3,072-dimensional down-projection input. D is one rank-24 adapter; F is one selected rank-24 expert;
SF is shared rank 8 plus selected rank 16; H is shared/parent/child rank 8+8+8. Every arm has active
rank 24 per token, but stored parameters, scale factors, sharing, and gate depth differ. H has 393,216
expert and 11,275 Router parameters.

Training objective and constraints:

\[
L_{H\text{-sem/shuf}}=L_{answer}+0.5L_{parent}+0.5L_{child\mid teacher\ parent},
\qquad L_{H\text{-task}}=L_{answer}.
\]

Optimizer: AdamW with adapter LR \(2\times10^{-4}\), Router LR \(5\times10^{-4}\), betas
\((0.9,0.999)\), epsilon \(10^{-8}\), weight decay 0.01, gradient clip 1.0, 26-update warmup, and cosine
decay to zero. Microbatch 8 × accumulation 16 gives effective batch 128. Every formal arm has 512
updates and checkpoints 0/128/256/384/512. Final exposure is 4,338,125 answer tokens for seed 17 and
4,354,753 for seed 29; arms within each seed use the same stream.

Seeds and conditions: seeds 17 and 29; D, F, SF, H-task, H-sem, and H-shuf. Changed variable within
the decisive H comparison is correct versus absent versus shuffled record-label association. Held
fixed are base, split, teacher, hierarchy, initial tensors, per-seed order, budget, load-off policy,
online coefficient rule, optimizer, final checkpoint, and evaluator.

Identities: model `model.safetensors` SHA-256 `cd2a512003e...`; model `config.json`
`504a6b58c427...`; primary analysis producer `analysis.py` `ead9d4a732ed...`; post-hoc
`reversal_audit.py` `0e02b106b946...`. Complete producer and raw-artifact identities are preserved in
the worker manifests.

Known setup limitations: two fixed seeds do not estimate a broad initialization distribution. Natural
source proportions give long-answer GSM8K/MATH records most pooled token weight. Development and test
are internal snapshot splits, and answer NLL is not free generation. H-shuf is one fixed permutation.

## 5. Metrics And Registered Decision Rules

For condition \(m\), record loss sum \(s_i^m\), and answer-token count \(n_i\),

\[
L_m=\frac{\sum_i s_i^m}{\sum_i n_i}.
\]

The primary effects are
\(\Delta_{task}=L_{H\text{-task}}-L_{H\text{-sem}}\) and
\(\Delta_{shuf}=L_{H\text{-shuf}}-L_{H\text{-sem}}\). Positive favors H-sem. Each seed is a separate
replication. Each 95% interval uses 2,000 percentile paired-record bootstrap draws, resampled inside
each source with NumPy seed 20260906. Tokens, checkpoints, conditions, and bootstrap draws are not
independent model replicates.

Registered outcomes:

- Support: all four lower endpoints exceed zero.
- Not supported: one named necessary contrast has nonpositive upper endpoints in both seeds.
- Insufficient: every other eligible pattern, including seed disagreement.
- Budget-limited insufficient, ineligible, and incomplete take precedence when their guards fire.

Per-source results, architecture comparisons, route loads, classification losses, gradients, and
parameter deltas are secondary or post-hoc. None can rescue the primary conjunction.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Use 512 updates | No 384-to-512 baseline improvement ≥0.002 with positive lower endpoint; no qualifying order reversal | four seed-17 development arrays per checkpoint | `choose_budget`, frozen analysis | paired source-stratified bootstrap | largest late improvement 0.000171; no trigger | ELIGIBLE | 512 selected | A1 removed 1024 before decision evidence |
| Use load-off | Trigger requires dead expert or concentration plus undertraining | H-task seed-17 histories and guard | registered final-quarter counts and parameter deltas | deterministic trigger | concentration true; dead/undertraining false | ELIGIBLE | load-off | Not a general load-balancing result |
| H-sem versus H-task | Four registered test NPZ pairs | `analysis.py` `ead9d4...` | pooled token ratio; paired source-stratified bootstrap | per seed, 2,000 draws | +0.010320 [0.009795,0.010890]; -0.002078 [-0.002469,-0.001680] | ELIGIBLE | seed disagreement | Two fixed seeds |
| H-sem versus H-shuf | Four registered test NPZ pairs | same primary producer | same estimator | per seed, 2,000 draws | +0.014645 [0.014138,0.015128]; +0.005467 [0.005064,0.005837] | ELIGIBLE | favors H-sem both | One shuffle cannot prove semantics |
| P3 typed verdict | Four effects as conjunction | `verdict.json` | frozen rule | no seed pooling | one necessary effect reliably negative, not both-seed negative | ELIGIBLE | `INSUFFICIENT` | Does not choose mechanism |
| Reversal begins before final checkpoint | No-training audit of saved development arrays | 16 H-task/H-sem checkpoint NPZ files | `reversal_audit.py` `0e02b1...` | same paired estimator, descriptive | opposite signs at 128/256/384/512; all intervals exclude zero | BOUNDED POST-HOC | persistent development reversal | Cannot alter test verdict |
| Source breadth/concentration | Descriptive only | same development arrays | per-source NLL, signed pooled contribution, leave-one-source-out | per-source record bootstrap | final sign counts 6/8 and 4/8; 80% from 2 and 3 sources; both 8/8 leave-one-out stable | BOUNDED POST-HOC | heterogeneous, magnitude-concentrated | Source sizes and answer lengths differ |
| No registered operational anomaly found | Required guards and exact identities | histories, guards, receipts, manifests | continuity/finite/hash/load/parameter checks | deterministic audit | every named check passes; 0 hash mismatches | ELIGIBLE FOR QUALIFICATION | no anomaly observed | Cannot prove absence of unmeasured defects |
| Select supervision-strength branch | User's branch rule: no anomaly + persistent development reversal | audit decision and above rows | deterministic branch selection | no inferential claim | weaker-weight matched localization selected | HUMAN-CONFIRMED BRANCH; exact 0.25 coefficient is AI-proposed | one next experiment | Diagnostics do not prove weight causation |

## 7. Main Results

### Eligible decision evidence

| Seed | D | F | SF | H-task | H-sem | H-shuf |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 17 | 0.752599 | 0.685425 | 0.682956 | 0.686567 | 0.676247 | 0.690892 |
| 29 | 0.750942 | 0.693099 | 0.699017 | 0.676168 | 0.678246 | 0.683713 |

Values are test NLL in nat/answer token. Full precision and denominators are in
[test NLL](tables/test_nll.csv).

| Seed | Registered contrast | Effect | Paired 95% interval | Reading |
| ---: | --- | ---: | ---: | --- |
| 17 | H-task − H-sem | +0.010320 | [0.009795, 0.010890] | H-sem lower |
| 17 | H-shuf − H-sem | +0.014645 | [0.014138, 0.015128] | H-sem lower |
| 29 | H-task − H-sem | -0.002078 | [-0.002469, -0.001680] | H-task lower |
| 29 | H-shuf − H-sem | +0.005467 | [0.005064, 0.005837] | H-sem lower |

The four-effect conjunction does not pass. It also does not meet the registered local non-support rule,
which requires one necessary contrast to be reliably nonpositive in both seeds. The only permitted
typed result is `INSUFFICIENT`.

Architecture comparisons are context, not a structural theorem. F beats D in both seeds
(D-minus-F +0.067174 / +0.057843). F-minus-SF changes from +0.002468 to -0.005918, and
SF-minus-H-task changes from -0.003611 to +0.022849. Only the D/F ordering replicates; storage,
sharing, scale, and gate-depth confounds remain. See [architecture effects](tables/architecture_effects.csv).

### Bounded post-hoc reversal evidence

| Update | Seed 17 H-task − H-sem | Seed 29 H-task − H-sem |
| ---: | ---: | ---: |
| 128 | +0.001272 [0.000897, 0.001636] | -0.003132 [-0.003524, -0.002737] |
| 256 | +0.010107 [0.009567, 0.010661] | -0.001964 [-0.002347, -0.001589] |
| 384 | +0.010178 [0.009635, 0.010722] | -0.002263 [-0.002630, -0.001905] |
| 512 | +0.010096 [0.009563, 0.010636] | -0.002310 [-0.002690, -0.001948] |

The reversal is visible at the first requested checkpoint and persists. It is not created by selecting
the final checkpoint.

At development update 512, per-source effects and absolute shares of the pooled numerator are:

| Source | Seed 17 effect | Seed 17 absolute contribution | Seed 29 effect | Seed 29 absolute contribution |
| --- | ---: | ---: | ---: | ---: |
| MMLU | +0.006627 | 0.5% | +0.011414 | 2.1% |
| MMLU-Pro | -0.004192 | 0.2% | -0.000220 | 0.0% |
| BBH | -0.012763 | 0.8% | -0.011935 | 1.7% |
| GSM8K | +0.017450 | 46.9% | -0.007961 | 48.4% |
| MATH | +0.005257 | 34.9% | +0.001457 | 21.9% |
| GPQA | +0.003540 | 0.0% | +0.010215 | 0.0% |
| HumanEval | +0.020023 | 0.6% | +0.011131 | 0.7% |
| MBPP | +0.106780 | 16.1% | -0.074042 | 25.2% |

Effects are not uniformly broad: seed 17 has six sources matching its pooled sign and seed 29 has
four. GSM8K/MATH carry most of seed 17's magnitude; GSM8K/MBPP carry the largest negative magnitude
in seed 29 while MATH offsets part of it. At update 512, however, every leave-one-source-out pooled
effect retains its seed's sign. GPQA and HumanEval contain only 30 and 25 records, so their intervals
are especially descriptive. Full checkpoint/source rows are in
[source effects](tables/reversal_source_effects.csv) and
[concentration audit](tables/reversal_source_concentration.csv).

### Stage-level profiling evidence

| Seed | Arm | Parent max share, updates 1–128 → 385–512 | Last parent entropy | Parent CE, early → late | Child CE, early → late | Parent-bank delta | Leaf-bank delta |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 17 | H-task | 0.920 → 0.956 | 0.177 | 0 → 0 | 0 → 0 | 5.875 | 8.926 |
| 17 | H-sem | 0.491 → 0.554 | 0.721 | 0.6602 → 0.3756 | 0.3954 → 0.1673 | 7.081 | 11.178 |
| 29 | H-task | 0.718 → 0.952 | 0.180 | 0 → 0 | 0 → 0 | 6.042 | 10.410 |
| 29 | H-sem | 0.460 → 0.562 | 0.717 | 0.6958 → 0.3896 | 0.4450 → 0.1736 | 6.582 | 11.398 |

Entropy is normalized to \([0,1]\) within the three-parent distribution. H-task auxiliary losses are
exactly zero by design; H-sem losses are positive and finite. Every parent, leaf, and shared expert has
nonzero final parameter change. H-sem changes load and increases the total parent/leaf bank movement,
but the direction of task benefit still differs by seed. These associations nominate supervision
strength as a testable rival; they do not prove it. Full segment gradients, leaf loads, and deltas are
in [training segments](tables/reversal_training_segments.csv) and
[expert updates](tables/reversal_expert_updates.csv).

### Debug-only, failed, ineligible, missing, and not-run evidence

- The first smoke attempt failed before formal evidence because the checkpoint output directory was
  absent. Its weights are discarded and excluded.
- The successful two-update smoke verifies paths and gradients only; none of its task values enter any
  scientific comparison.
- H-hard's smoke path is not a formal H-hard result. Formal H-hard and H-oracle are
  `NOT_RUN_NOT_TRIGGERED` and cannot be read as zero, missing, or negative evidence.
- No post-hoc source exclusion, seed pooling, outlier removal, or extra-seed search was performed.

## 8. Visualization Results

### Registered test effects

![Registered test effects](figures/primary_semantic_effects.png)

Purpose: show all four conjunctive semantic effects. Setup: final load-off checkpoints at update 512.
Metric: baseline-minus-H-sem test NLL, nat/answer token. Raw source and lineage: paired test NPZ arrays,
[primary effects](tables/primary_semantic_effects.csv), lineage rows 3–5. Points are pooled token-weighted
effects; bars are 2,000-draw paired source-stratified 95% intervals. Positive/right favors H-sem.
Three points are positive; seed-29 H-task is reliably negative. Take-home: the conjunction is
insufficient. The figure cannot explain the reversal or establish a seed distribution.

### Persistent development reversal

![Persistent development reversal](figures/reversal_development_effects.png)

Purpose: determine when the opposite seed directions appear. Setup: saved H-task/H-sem development
arrays at updates 128/256/384/512. Metric and uncertainty match the primary estimator but remain
post-hoc. Positive favors H-sem. Seed 17 is positive and seed 29 negative at every checkpoint; every
interval excludes zero. Take-home: the reversal is persistent development behavior, not a final-step
artifact. It cannot identify auxiliary-weight causation.

### Source heterogeneity at update 512

![Source effects at update 512](figures/reversal_source_effects_update512.png)

Purpose: distinguish a broadly uniform effect from source concentration. Each panel shows per-source
development H-task-minus-H-sem; intervals resample records within that source and are post-hoc. The
horizontal scales differ between panels because MBPP magnitudes differ sharply; compare signs and each
panel's own axis, not visual distances across panels. Observed signs are mixed, with large GSM8K and
MBPP contributions. Take-home: source heterogeneity is real and pooled magnitude is concentrated, yet
no single source determines either final pooled sign. This cannot establish a source-specific semantic
mechanism.

The required all-condition seed-17 development curves are retained in
[development curves](figures/development_curves_seed17.png); they support budget/stability auditing but
are not needed to interpret the registered test verdict.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| Data / teacher | exact counts, overlaps, GMM restarts, leaf counts, hashes | PASS | — | direct split overlap under registered key; empty teacher leaf | paraphrases, pretraining contamination, teacher semantics |
| Implementation tests | 9 tests recorded before execution; current local regression 11/11; causal prefix state/logit max difference 0 | PASS after disposable repair | first checkpoint directory absent | registered code paths and prefix leakage at tested shape | unmeasured implementation defects |
| Smoke | eight condition paths, gradients, parameter movement; weights discarded | PASS | — | missing gradient/path construction in smoke | long-run scientific performance |
| Preflight | four baselines through 512; budget/load rules | PASS | — | registered budget instability and load-trigger requirement | broader convergence beyond 512 |
| Formal training | 12/12 arms; histories contiguous; all guards pass | PASS | — | missing arm, frozen-weight drift, nonfinite training | seed-specific optimization dynamics |
| Test / registered analysis | 12 paired arrays; fixed estimator | PASS | — | identity/token mismatch, post-hoc primary rule | replicated semantic value |
| Scientific hypothesis | four-effect conjunction | UNCLEAR / INSUFFICIENT | H-task comparison reverses by seed | universal positive claim in these two seeds | supervision strength, other seed-specific dynamics |
| Post-hoc reversal audit | checkpoints, sources, load/loss/update diagnostics | COMPLETE / BOUNDED | — | late-only reversal; registered recovery/eval anomaly found by these checks | causal explanation of reversal |

Falsified physical prior: not falsified generally. The result does not show a stable positive task
increment from the current teacher/objective, but one seed improves and true labels beat shuffled in
both.

Falsified mathematical model: the registered all-seed positive conjunction is not satisfied; the
answer-NLL estimator itself remains valid.

Falsified operationalization / proxy: not decisively. The current \(0.5/0.5\) auxiliary weighting is a
live rival, as are teacher quality and seed-dependent routing dynamics.

Falsified implementation: no. The registered guards and post-run audit found no qualifying defect.

Falsified metric: no. It measures the intended teacher-forced answer likelihood, while its boundary
to generation remains explicit.

Remaining rival explanations: auxiliary supervision strength, interaction between semantic targets
and seed-specific Router/expert dynamics, source-weighted task mixture, teacher proxy quality, and the
limited two-seed replication set. The next experiment isolates only the first.

## 10. Full Experiment Record

Worker root:
`/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training`.
Eligible run root:
`/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/full-20260906T170500Z`.

Execution sequence: data/teacher receipt at 17:24 UTC; successful smoke at 17:28 UTC; A1 recorded at
18:06 UTC; preflight completed at 18:21 UTC; formal analysis completed at 18:57 UTC. ACP job
`pt-86wcqrbi` ran from 18:05:44 to 18:57:28 UTC on one reserved `n6ls.iu.i40.4` node with four NVIDIA
H100 80GB GPUs, one independent single-GPU condition per worker and no automatic retry. Platform
state is `SUCCEEDED`. Formal-stage producer elapsed time was 2,133.27 seconds; the whole ACP wall time
was approximately 3,105 seconds.

Container image:
`registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04`.
Workspace `share-space`; AEC2 `share-cluster`; quota `reserved`. The amendment preserved the original
GPU-hour ceilings and changed only concurrency/resource placement and the 512-only stop branch.

Formal mapping reuses eligible seed-17 D/F/SF/H-task preflight checkpoints because 512/load-off was
selected; seed-29 baselines and both-seed H-sem/H-shuf are under `formal_512`. Every final H stability
effect from 384 to 512 is 0.000218 or smaller, below the 0.002 trigger. Test was unsealed only after
these checks.

The no-training reversal command was:

```text
python reversal_audit.py --run-root runs/full-20260906T170500Z
```

It loads saved NPZ/JSON artifacts only and creates separate `reversal_*` CSV/JSON/PNG outputs. No model
checkpoint is loaded for optimization and no training call is made.

Post-hoc verification: all 11 current worker tests pass, including a synthetic regression that checks
per-source point effects use only the requested source subset. All 57 primary manifest hashes still
match after the audit; all 27 declared audit inputs and eight declared audit outputs match their
separate audit manifest.

## 11. Interpretation

Direct observation: correct labels outperform shuffled labels in both seeds, but they outperform a
task-only hierarchy in only seed 17. The development contrast has the same seed-specific directions
from update 128 onward. H-sem produces substantially less concentrated parent routing than H-task,
finite declining auxiliary losses, and larger parent/leaf bank movement; all experts remain trained.

Interpretation: the data justify testing whether the current auxiliary objective is too strong. They
do not yet justify saying it is too strong. Load, loss, gradient, and parameter-change measurements are
correlated consequences of changing the objective. Only a held-fixed weight intervention can test
that candidate explanation, and even that next development-only localization will not retroactively
confirm P3 on its already-open test.

## 12. Claim Boundary

Can claim: under this exact base, data construction, teacher, H architecture, 512-update load-off
schedule, and two seeds, H-sem beats H-shuf in both seeds but has a sign-reversing comparison with
H-task. The registered conclusion is `INSUFFICIENT`. The opposite development signs are present by
update 128 and persist through 512. The audited run contains no registered operational anomaly.

Cannot claim: a general semantic-supervision gain or harm; that \(0.5/0.5\) weighting causes the
reversal; that balanced routing is better; that GMM groups are semantic truth; that hierarchy is
necessary; that any expert has non-interchangeable semantic function; or that answer NLL implies
free-generation, clean public-benchmark, or deployment gains.

## 13. Next Decision

Decision: the researcher-selected branch is exactly one matched semantic-supervision-strength
localization. The AI-proposed exact operationalization, pending Protocol confirmation, runs H-task
\((\lambda_p=\lambda_c=0)\), H-sem-weak \((\lambda_p=\lambda_c=0.25)\), and current H-sem
\((\lambda_p=\lambda_c=0.5)\) for seeds 17/29 at 512 updates and load-off from common initial states.
Hold the architecture, frozen teacher, data order, optimizer, checkpoint schedule, and evaluator
fixed. Use development only for this adaptive localization; the already-open P3 test is not a new
confirmatory surface.

Completion criterion: before execution, freeze a Protocol whose primary localization asks whether
the weak arm has lower update-512 development NLL than the current arm in both seeds under paired
intervals. H-task separately records whether the weaker signal retains task value. If the weak arm
does not improve over the current arm in both seeds, stop the over-strong-weight explanation. Do not
add seeds until a positive result appears, and do not add H-hard/H-oracle, layers, or another mechanism
to this experiment.

Resume action: draft and obtain approval for that one Protocol. No follow-up training was started.

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [Protocol](protocol.md) | Registered contract and A1 ledger | `20260906-P3-v1` + A1 | Anchor, approved design | worker snapshot `98dadafb4e16...`; A1 `5f52f9d86dee...` | yes | yes | live file adds execution receipt only |
| [Data/teacher receipt](tables/data_teacher_receipt.json) | Split, raw revisions, PCA/GMM and assignment identity | worker data/teacher stage | raw snapshots and frozen base | copied SHA-256 `66ab09ea4d52...` | yes | qualification | Full raw-file map retained |
| [Execution audit](tables/execution_audit.json) | Job, 12-arm completeness, identities, hashes | post-run audit 2026-09-06 19:58 UTC | receipts, conditions, test arrays, manifest | `c95bb967d91b...` | yes | yes | 57 entries; zero mismatch |
| [Worker artifact manifest](tables/worker_artifact_manifest.json) | Raw checkpoints/log/array map | primary pipeline | 12 conditions and analysis | `b9e1c4c60c82...` | yes | yes | Raw artifacts stay in worker |
| [Test NLL](tables/test_nll.csv) | All 12 final losses | `analysis.py` `ead9d4...` | test NPZ arrays | `39131dd47889...` | yes | yes | 8,481 records per arm |
| [Primary effects](tables/primary_semantic_effects.csv) | Four registered contrasts | same | paired test arrays | `d3600062c2ff...` | yes | yes | Verdict-bearing |
| [Typed verdict](tables/verdict.json) | Frozen rule output | same | primary and architecture effects | `f35a54ec82ad...` | yes | yes | `INSUFFICIENT` |
| [Formal H stability](tables/formal_h_stability.csv) | Final budget qualification | primary pipeline | development 384/512 arrays | `9076b0735207...` | yes | qualification | All below 0.002 |
| [Reversal audit manifest](tables/reversal_audit_manifest.json) | Post-hoc input/output lineage | `reversal_audit.py` `0e02b1...` | saved H development/history/guards | `fd9c6cdb81f9...` | yes | bounded | No-training diagnostic |
| [Reversal checkpoint effects](tables/reversal_checkpoint_effects.csv) | Onset and persistence | same | 16 development arrays | `7c9d3d026f62...` | yes | bounded | Post-hoc |
| [Reversal source effects](tables/reversal_source_effects.csv) | Source breadth and contributions | same | same development arrays | `329886878bfa...` | yes | bounded | Per-source descriptive |
| [Training segments](tables/reversal_training_segments.csv) | Load, loss and gradient audit | same | four histories | `8ac6c2b162a2...` | yes | bounded | Does not prove mechanism |
| [Expert updates](tables/reversal_expert_updates.csv) | Final bank/Router movement | same | four eligibility guards | `0bb645bda2bc...` | yes | bounded | Norms, not functional intervention |
| [Primary figure](figures/primary_semantic_effects.png) | Registered verdict visualization | primary pipeline | primary effects CSV | `47940a02cf38...` | yes | yes | Visually inspected |
| [Reversal figure](figures/reversal_development_effects.png) | Persistent opposite directions | reversal audit | checkpoint effects CSV | `5358cd0fb431...` | yes | bounded | Visually inspected |
| [Source figure](figures/reversal_source_effects_update512.png) | Source heterogeneity | reversal audit | source effects CSV | `8ad21bd9c443...` | yes | bounded | Panels use different x scales |

Canonical copies are curated reading artifacts. Raw NPZ arrays, initial/final/checkpoint tensors,
complete histories, environment logs, teacher objects, and recovery states remain under the eligible
worker run. No checkpoint, raw dataset, or unfiltered log was promoted to Research_System.

## 15. Links

- Anchor: [A15_13_05](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_05_gmm_pseudolabel_oracle_gap_anchor.md)
- Protocol: [P3](protocol.md)
- Summary: [P3 first reading path](summary.md)
- Code workspace: `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training`
- Primary runner: `parallel_pipeline.py`; condition runner: `condition_worker.py`; orchestration: `run_4gpu_pipeline.sh`
- Configuration: `config.py`; models: `models.py`; primary analysis: `analysis.py`; post-hoc audit: `reversal_audit.py`
- Data / teacher: `/data/250010109/datasets/a15_e14_p3_clean/processed.pt`; worker `teacher/`
- Result directory: `/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/full-20260906T170500Z`
- Figures: [canonical figures](figures/primary_semantic_effects.png)
- Logs / checkpoints: eligible run `logs/`, `conditions/preflight_512/`, and `conditions/formal_512/`
- Formal command: `RUN_ROOT=<eligible-run> timeout --signal=TERM 129600s bash run_4gpu_pipeline.sh`
- Audit command: `python reversal_audit.py --run-root <eligible-run>`
- Job ID: `pt-86wcqrbi`
