# Detailed: A6 Online SAE/GMM Router Regularization

Primary Anchor: [A15_13_10](../../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_10_sae_flat_router_functional_anchor.md)  
Frozen Protocol and registered revision: [A6 Protocol](protocol.md), Sections
0--9 SHA256 `9bd54f34371ef3e4bace0c40ecaa035ff3d185f6bbe05ea0349073bfb3a708c9`  
Summary: [A6 Summary](summary.md)  
Result eligibility: `ELIGIBLE_MEASUREMENTS`; scientific interpretation and
Focus transition remain `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`.

## 0. Quick Recap

Purpose: test whether frozen initial SAE/GMM structure improves task learning
when the Router and experts are trained jointly.

Hypothesis: at least one of four teacher/constraint combinations should beat
matched task-only training in all three seeds.

Experiment logic: four online-regularized arms × seeds 17/29/43 × 512 updates,
with exact task-only initialization and schedule reuse, followed by fixed-final
full internal-test evaluation.

Direct result: all 12 `new minus task-only` test-NLL differences are positive.
The best new arm is SAE-B at `0.702514 ± 0.000164`, versus task-only at
`0.696579 ± 0.000782`; mean paired degradation is
`+0.005936 ± 0.000943` nats/token.

Eligibility: all required qualification, completion, pairing, coverage,
freeze, gradient, and artifact-integrity checks passed. No condition was
excluded or resumed after failure.

Verdict: the registered all-seed advantage criterion was not met by any arm.

Claim boundary: this rejects benefit for the registered fixed configuration,
not every SAE/GMM teacher, coefficient, layer, or expert construction.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Task-only | Router and experts learn only from answer prediction | Reused A5 condition with matched seed initialization and schedule | NLL at update 512 | Strongest inherited baseline | Broad best-method status |
| SAE teacher | Eight-way frozen target from retained SAE activation mass | Normalize summed Top-32 activation mass inside each retained group | Distribution \(q_t^S\) | Tests SAE-derived initial structure | True semantic classes |
| GMM teacher | Eight-way frozen token posterior | PCA-64 plus eight-component diagonal GMM on training-only states | Distribution \(q_t^G\) | Tests a different data-derived teacher | Isolation of clustering algorithm alone |
| Scheme A | Fixed expert-ID alignment | Token-weighted \(D_{KL}(q_t\Vert p_t)\) | Mean KL | Tests explicit teacher-to-expert IDs | Permutation-invariant structure |
| Scheme B | Pairwise relation preservation | Teacher-similarity-weighted attraction and margin repulsion | Registered pair loss | Tests structure without fixed expert IDs | Functional expert utility |
| Test NLL | Average negative log probability on answer tokens | \(\sum_i\mathrm{loss\_sum}_i/\sum_i\mathrm{target\_tokens}_i\) | nats/token; lower is better | Primary task endpoint | Generated-answer accuracy |
| Seed | One independent training trajectory | 17, 29, or 43 | Three units | Unit for directional consistency and SD | Population significance |

## 2. Anchor Link And Decision Point

The Anchor asks whether initial SAE/GMM structure can provide stable task
benefit when routing remains trainable. A6 operationalizes that question at
one final layer, eight experts, one structural coefficient, two teachers, and
two constraints. The pre-registered decision is whether any arm has negative
`new minus task-only` test-NLL deltas in all three seeds and therefore merits
continued evaluation.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Protocol | Approved implementation, smoke, and full run; Sections 0--9 frozen | Body SHA256 `9bd54f...708c9`; submission snapshot retained | PASS | [submission snapshot](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z/protocol_at_submission.md) | None |
| Matrix | Four arms × three seeds × 512 updates | 12/12 trajectories; every history has updates 1--512 | PASS | [verification](/data/250010109/MoE_Router/reports/a6_20260909/verification.json) | None |
| Baseline identity | Exact A5 task-only update-0 state and schedule per seed | All three checkpoint/schedule hashes match; seed-17 two-update old/new parity is exactly zero | PASS | [qualification receipt](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z/qualification/receipt.json) | None |
| Teacher construction | Training-only token GMM, shared frozen targets, common SAE mask | GMM converged in 15 iterations; 65,536 sampled positions; 2,617,687 valid cached target positions; teacher/cache freeze guards pass | PASS | [target receipt](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z/teachers/targets.receipt.json) | None |
| GPU qualification | Two-step parity plus four fresh eight-update smokes and evaluation | Parity and all four arms PASS on four GPUs | PASS | [qualification receipt](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z/qualification/receipt.json) | None |
| Checkpoints | 0/128/256/384/512 plus recovery | 60/60 fixed checkpoints and all recovery states present | PASS | [verification](/data/250010109/MoE_Router/reports/a6_20260909/verification.json) | None |
| Development evaluation | Full 8,480 records at five checkpoints | 60/60 new-arm evaluations complete | PASS | [development table](tables/development_curve.csv) | None |
| Test evaluation | Full 8,481 records, frozen bias, no structural loss | 12/12 new and 3/3 reused baseline evaluations; 562,954 answer tokens each | PASS | [all seeds](tables/all_seeds.csv) | None |
| Pairing | Same record IDs, sources, and token denominators | Exact equality across all 15 test record sets | PASS | [verification](/data/250010109/MoE_Router/reports/a6_20260909/verification.json) | None |
| Aggregation | Token-weighted within seed; equal seed mean and sample SD | Independently recomputed in float64; original float32 values differ by at most `4.11e-8` | PASS | [condition means](tables/condition_means.csv) | None |
| Resource | One reserved four-H100 node; no retry; within six node-hours | Job `pt-jn404t7l` SUCCEEDED in 48m10s with zero retries; qualification used 8m08s | PASS | [completion receipt](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z/full_completion_receipt.json) | None |
| Runtime logs | Preserve launch and worker log paths | Files exist but are zero-byte because the runner emits no stdout; worker receipts, checkpoints, manifests, and platform state are complete | OBSERVATION | Run root | No eligibility impact; provenance does not depend on log text |
| External benchmark | Not required for A6 primary endpoint | NOT RUN | CONFORMANT | Protocol Section 9 | Limits claim to internal teacher-forced NLL |

Frozen Protocol revision: Sections 0--9 SHA256
`9bd54f34371ef3e4bace0c40ecaa035ff3d185f6bbe05ea0349073bfb3a708c9`.

Execution scope approved: implementation, teacher preparation, qualification,
four-arm × three-seed full training, internal evaluation, and result records.

Amendments: none after the formal-run scientific body was frozen. Append-only
operational receipts do not change the registered design.

Retries and exclusions: zero platform retries; zero trajectory exclusions.

Missing conditions or artifacts: none among registered A6 conditions. Random,
Dense, and external generation conditions were deliberately outside scope.

Post-hoc analyses: float64 recomputation, curated tables, and report figures
were generated after completion from the frozen raw arrays. They do not change
the primary metric or decision rule.

## 4. Actual Setup

Research question: can an initial eight-way SAE/GMM structure improve online
joint Router/expert task learning relative to task-only routing?

Data construction and provenance: A5 data artifact SHA256
`58e409ca9d903d146c9ae8e3cee834a4eb5f0e6f2e24de4fe521349d05e527f2`.
Teacher fitting used only the registered training Router subset; development
and test did not enter GMM fitting.

Train / development / confirmation split: inherited training split; full
development has 8,480 records; internal test has 8,481 records and 562,954
answer tokens. The test is an existing internal holdout already used by A5,
not an untouched official benchmark.

Learning task and permitted supervision: answer-token cross entropy plus the
registered frozen structural term on causal answer-prediction positions.

Model / architecture / algorithm: frozen Qwen3-0.6B-Base; zero-indexed layer-27
MLP pre-input state; one shared rank-16 branch; eight rank-16 experts; hard
Top-1 dispatch; trainable linear 1024-to-8 Router in all A6 arms.

Input representation / position encoding: the state at position \(t\) predicts
`labels[t+1]`; no target or future answer token enters the teacher state.

Training objective and constraints:

\[
L=L_{task}+0.1R,
\]

where Scheme A uses the globally token-normalized teacher-to-Router KL and
Scheme B uses the registered globally normalized pairwise attraction/repulsion
loss. Structural gradients update the Router directly; task gradients update
the Router, shared branch, and experts. Dynamic count-based balancing bias is
outside autograd and is frozen during evaluation.

Optimizer or update rule: AdamW; shared/expert LR `2e-4`, Router LR `5e-4`;
26-update warmup and inherited cosine schedule; global clipping `1.0`;
weight decay `0.01` for shared/experts and `0` for Router.

Training steps / tokens / batch size: 512 updates; microbatch 8 records;
accumulation 16; effective batch 128 records.

Checkpoints: update 0, 128, 256, 384, and 512; recovery every 64 updates.

Seeds: 17, 29, and 43.

Conditions and plain-language labels: SAE-A and GMM-A align teacher groups to
fixed expert IDs; SAE-B and GMM-B preserve pairwise teacher relations without
fixing expert IDs; task-only is the matched no-structural-loss baseline.

Changed variables: teacher construction and structural constraint. Held fixed:
model, data, task loss, initialization, sample schedule, optimizer, updates,
Router/expert architecture, balancing rule, evaluation, and checkpoint choice.

Code / config / data identities: [formal manifest](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z/formal_manifest.json).

Script and result paths: [immutable source](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z/source),
[formal run](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z),
and [read-only report builder](/data/250010109/MoE_Router/reports/a6_20260909/build_report.py).

Known setup limitations: one layer, eight experts, one coefficient, one
training budget, internal reused holdout, no random structural teacher, no
intervention-based utility evaluation, and no external generation benchmark.

## 5. Metrics And Registered Decision Rules

Primary metric: final-update internal-test answer-token NLL in nats/token,
computed as total answer loss divided by total answer tokens; lower is better.

For each condition and seed,

\[
\Delta_s=\operatorname{NLL}_{new,s}-\operatorname{NLL}_{task-only,s}.
\]

Three negative deltas mean a directionally consistent advantage under this
configuration. Any positive delta rejects the all-seed advantage. Sign
reversal is unstable ordering; invalid or missing trajectories make the
comparison incomplete. The seed mean and sample SD are descriptive, not a
population hypothesis test. Lower structural loss cannot substitute for lower
task NLL.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Any A6 arm merits continued evaluation | Three negative new-minus-task-only deltas | 15 paired `test/records.npz` files | Float64 total loss / total tokens; paired differences by seed | Equal mean and sample SD over three seeds | All 12 deltas positive; best arm SAE-B mean delta `+0.005936 ± 0.000943` | ELIGIBLE | Registered support criterion not met | Fixed configuration and internal holdout only |
| Constraint A or B is preferable within a teacher | Same-seed A-vs-B signs | Same raw arrays | Right-minus-left paired NLL | Three seeds, descriptive | SAE-B beats SAE-A in all seeds by `-0.001203 ± 0.000598`; GMM-B vs GMM-A reverses sign | ELIGIBLE_SECONDARY | B is consistently better only within SAE, but neither beats task-only | Does not select a successful method |
| SAE or GMM teacher is preferable within a constraint | Same-seed SAE-vs-GMM signs | Same raw arrays | GMM-minus-SAE paired NLL | Three seeds, descriptive | A: GMM is worse by `+0.001410 ± 0.000790` in all seeds; B reverses sign | ELIGIBLE_SECONDARY | SAE is consistently better only under A | Teachers differ in construction and fitting subset |
| Structural objective was active | Nonzero structural gradient and Router movement | 12 `training.json` histories and 60 checkpoints | Read registered norms at fixed updates | Per-seed records; no inferential pooling | All arms have nonzero structural gradients and Router deltas through update 512 | ELIGIBLE_GUARD | Rules out an accidentally inactive regularizer | Does not prove regularization caused the loss gap |
| Formal result is operationally eligible | Qualification, freeze, completion, pairing, and coverage pass | Receipts, manifests, checkpoints, raw arrays | Hash, schema, count, and finite-value checks | All registered units | 12 trajectories, 60 checkpoints, 60 dev evaluations, 12 new tests; no retries/exclusions | ELIGIBLE | PASS | Empty stdout logs reduce narrative trace, not artifact trace |

## 7. Main Results

### Eligible decision evidence

| Condition | Test NLL mean ± sample SD | Seed 17 delta | Seed 29 delta | Seed 43 delta | Mean delta ± sample SD |
| --- | ---: | ---: | ---: | ---: | ---: |
| SAE-A | 0.703717 ± 0.000761 | +0.005371 | +0.007846 | +0.008199 | +0.007139 ± 0.001541 |
| GMM-A | 0.705128 ± 0.000089 | +0.007693 | +0.008845 | +0.009110 | +0.008549 ± 0.000753 |
| SAE-B | 0.702514 ± 0.000164 | +0.004851 | +0.006386 | +0.006570 | +0.005936 ± 0.000943 |
| GMM-B | 0.704372 ± 0.001801 | +0.004822 | +0.009399 | +0.009158 | +0.007793 ± 0.002576 |
| Task-only | 0.696579 ± 0.000782 | 0 | 0 | 0 | 0 |

The independence unit is the training seed. Records, answer tokens,
checkpoints, tasks, and arms are not additional training replicates.

### Bounded and secondary evidence

- SAE-B improves over SAE-A in all seeds by a mean `-0.001203` nats/token, but
  both remain worse than task-only in all seeds.
- GMM-A is worse than SAE-A in all seeds by a mean `+0.001410`; GMM-B versus
  SAE-B and GMM-B versus GMM-A both reverse sign across seeds.
- Per task, no arm is better than task-only in all three seeds on any of the
  eight task families. SAE-A, GMM-A, and GMM-B are worse in all seeds on seven
  of eight tasks; SAE-B is worse in all seeds on five and mixed on three.
  These task rows are secondary and do not replace the overall token-weighted
  endpoint. Source: [per-task deltas](tables/per_task_mean_deltas.csv).

### Stage-level profiling evidence

At update 512, the mean structural Router-gradient norm remains nonzero for
every arm: SAE-A `0.0987`, GMM-A `0.0624`, SAE-B `0.0731`, and GMM-B `0.0552`.
The corresponding mean Router parameter deltas from initialization are
`1.234`, `1.593`, `1.172`, and `1.311`. This establishes that the registered
regularizers acted on the Router; it does not identify whether teacher content,
coefficient, duration, or interaction with task gradients caused the worse NLL.

### Debug-only, failed, ambiguous, or ineligible evidence

No registered trajectory is failed, ambiguous, or ineligible. Zero-byte stdout
logs are not used as result evidence. Intermediate training NLL and structural
loss are diagnostics, not substitute primary endpoints.

## 8. Visualization Results

### Fixed-update internal-test NLL

![Fixed-update internal-test NLL](figures/test_nll.png)

Purpose: show every independent training seed for the primary endpoint.

Setup: fixed update 512, matched task-only baseline, all 8,481 internal-test
records and 562,954 answer tokens.

Metric definition and unit: answer-token NLL, nats/token; lower is better.

Raw source and lineage row: authenticated test `records.npz`, summarized in
[all seed values](tables/all_seeds.csv) and lineage row 1.

Aggregation and uncertainty: colored dots are seeds 17/29/43; black marks are
equal-weight means ± sample SD, not confidence intervals.

How to read: compare each new-arm point with task-only; every new point is
higher.

Expected under registered outcomes: a supported arm would have lower NLL than
its task-only baseline in all three seeds.

Observed result: no arm has one negative paired delta, let alone three.

Take-home: the registered fixed configuration does not demonstrate stable task
benefit.

Remaining uncertainty: why the active structural objective hurt task NLL.

What this figure does not prove: broad SAE/GMM ineffectiveness, semantic
invalidity, intervention-tested expert utility, or external capability ranking.

Anchor update implication: pending researcher judgment; do not promote an arm.

### Full-development checkpoint curves

![Full-development checkpoint curves](figures/development_loss.png)

Purpose: test whether the final ranking is confined to the test snapshot.

Setup: identical 8,480-record development set at updates 0/128/256/384/512.

Metric definition and unit: answer-token NLL, nats/token; lower is better.

Raw source and lineage row: evaluation manifests summarized in
[development curves](tables/development_curve.csv).

Aggregation and uncertainty: bold line is the three-seed mean; faint lines are
individual seeds.

How to read: all conditions share the same update-0 value. GMM-A is transiently
lower than task-only at update 128 by about `0.00234` mean NLL, but task-only is
lower by update 256 and finishes at `0.706973` versus `0.713029--0.715563` for
the online arms.

Expected under registered outcomes: stable benefit should survive to the
fixed final checkpoint and the test surface.

Observed result: the early GMM-A development advantage does not survive.

Take-home: the test result is consistent with the final development ordering,
not an isolated test-only reversal.

Remaining uncertainty: whether a pre-registered early-stop or transient
regularization design would behave differently; A6 did not test that design.

What this figure does not prove: that update 128 is a valid selected checkpoint
or that overfitting is the cause.

Anchor update implication: preserve fixed-final failure; do not select update
128 post hoc.

The [structural-loss](figures/structural_loss.png) and
[Router-drift](figures/router_checkpoint_drift.png) figures are retained as
guard diagnostics. They are not promoted as task-benefit evidence.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| Frozen design and source | Protocol/body hash and formal manifest | PASSED | N/A | Silent post-start design change | Broader design alternatives |
| Teacher construction | GMM convergence, target coverage, freeze hashes | PASSED | N/A | Missing/constant/changed teacher | Teacher usefulness for task loss |
| Baseline equivalence | Init/schedule hashes and exact two-update parity | PASSED | N/A | Obvious baseline implementation drift | Longer-horizon interactions |
| Four-arm GPU smoke | Finite losses, gradients, Router movement, evaluation | PASSED | N/A | Basic implementation or device failure | Full-budget task benefit |
| Twelve full trajectories | 12 × 512 updates and fixed checkpoints | PASSED | N/A | Missing-seed explanation | Scientific efficacy |
| Primary internal evaluation | Paired coverage and finite raw arrays | PASSED | N/A | Evaluation incompleteness | External generation behavior |
| Registered efficacy prediction | All-seed new-minus-baseline deltas | FAILED | All 12 deltas are positive | Benefit under this fixed configuration | Cause of harm; other coefficients/designs |

Falsified physical prior: not broadly falsified. A6 falsifies only the concrete
prediction that one registered teacher/constraint combination at
`lambda=0.1` improves final internal-test NLL in all three seeds.

Falsified mathematical model: the A and B objectives are constructible and
active, but neither produced the predicted task benefit under this coefficient.

Falsified operationalization / proxy: task NLL itself did not fail as a metric;
the unresolved question is whether persistent structural pressure or teacher
content is the relevant failed operationalization.

Falsified implementation: no; qualification, gradient, freeze, pairing, and
completion guards passed.

Falsified metric: no; the registered endpoint is measured completely. It is
still an internal teacher-forced loss, not an external capability score.

Remaining rival explanations: ordinary task gradients already provide the
useful routing adaptation; the frozen structures are task-misaligned; or one
fixed persistent coefficient exerts harmful pressure. A6 cannot separate these
three explanations.

## 10. Full Experiment Record

- Qualification job: `pt-80s7l3fm`; started `2026-09-08T18:34:12Z`, completed
  `18:42:20Z`, state `SUCCEEDED`.
- Formal job: `pt-jn404t7l`; created `18:43:59Z`, started `18:44:15Z`, completed
  `19:32:25Z`, state `SUCCEEDED`.
- Formal resource: one reserved `n6ls.iu.i40.4` node with four H100 GPUs,
  `share-space/share-cluster`, image
  `ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04`.
- Retry count: zero; maximum retry count: zero.
- Measured allocation: qualification 8m08s plus formal job 48m10s, about
  0.94 four-GPU node-hours (about 3.75 GPU-hours), below the six-node-hour cap.
- Formal run: `full-20260908T183139Z`.
- Completion: 12 training trajectories, 60 fixed checkpoints, 60 full
  development evaluations, 12 full new-arm tests, and three reused matched
  task-only tests.

## 11. Interpretation

Observation: every online-regularized arm is worse than task-only at the fixed
final test checkpoint in every seed; the same ordering holds for final mean
development NLL.

AI interpretation awaiting researcher confirmation: the registered evidence
does not support adding persistent SAE/GMM structural regularization at
`lambda=0.1` to this task-trained Router. Scheme B is less harmful than A for
SAE, but that relative ordering does not create a benefit over task-only.

Claim: no registered A6 arm demonstrates stable internal task-loss benefit in
this configuration.

Speculation, not established: the harm may come from teacher-task mismatch or
from the magnitude/duration of structural gradient pressure.

Boundary: no statement about true semantic groups, causal expert utility,
external generation, or all possible regularization strengths.

## 12. Claim Boundary

Can claim: under this final-layer, eight-expert, 512-update, fixed
`lambda=0.1` internal-holdout configuration, none of the four SAE/GMM online
regularizers demonstrated a stable task-loss benefit over matched task-only
training.

Cannot claim: that every SAE/GMM teacher or regularization strength is
ineffective; that the groups are or are not true semantic classes; that expert
utility has been established by intervention; or that the ranking transfers
to clean official or external generation benchmarks. The experiment also
lacks a random structural teacher, so it cannot isolate semantic structure
from generic regularization.

## 13. Next Decision

Decision: **AI suggestion — do not advance any A6 arm to external evaluation;
close this fixed `lambda=0.1` online-regularization configuration. Researcher
confirmation is pending.**

Completion criterion: the researcher confirms or replaces this one decision
while preserving the measured result and claim boundary.

Resume action: after confirmation, update Anchor Sections 7--8 and the active
Focus. If diagnosis is selected instead, first register one minimal causal
discriminator in the Anchor; this record does not authorize a coefficient
sweep or another run.

Researcher judgment still required:

```text
Question: Did any registered A6 condition provide an all-seed task-loss advantage?
Direct result: No; all 12 new-minus-task-only deltas are positive.
Confirmed: AWAITING_RESEARCHER
Weakened or rejected: AWAITING_RESEARCHER
Current mechanism and reason: AWAITING_RESEARCHER
Cannot claim: AWAITING_RESEARCHER_CONFIRMATION_OF_BOUNDARY_ABOVE
Exactly one next decision: AWAITING_RESEARCHER; AI suggestion is stated above.
```

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Frozen Protocol body | Registered scientific contract | A6 Sections 0--9 | Anchor and confirmed Focus | `9bd54f...708c9` | Yes | Yes | Ledger excluded from body hash |
| Formal manifest | Frozen source/config/input/resource identity | `prepare_run.py` | Source, teachers, A5 inputs | `743e8dcb...c922f` | Yes | Yes | Matrix and resource guards |
| Qualification receipt | Parity, preflight, target, and four-arm smoke | job `pt-80s7l3fm` | Frozen run | `2712d1fc...b358` | Yes | Yes | All stages PASS |
| Completion receipt | ACP terminal state and timing | post-run read-only query | job `pt-jn404t7l` | `d2f12208...52cf` | Yes | Operational | Zero retries |
| Token GMM | Frozen GMM teacher | `prepare_teacher.py` | Training-only Router cache | `18ad70c0...f2c2` | Yes | Yes | Converged, 15 iterations |
| Target receipt | Common target-cache identity and coverage | `targets.py` | Data, SAE, GMM, backbone | `0f5046ad...ecf` | Yes | Yes | 2,617,687 valid positions |
| Raw aggregate | Original run-level summary | frozen `analysis.py` | Raw evaluations and histories | `4ed15bc6...ad88` | Yes | Yes | Float32 aggregation |
| Report verification | Independent pairing, coverage, hash, and float64 audit | `build_report.py` | Raw artifacts above | `21bd30b7...c702` | Yes | Yes | Max float32 difference `4.11e-8` |
| All seeds table | Fifteen seed-level test values and hashes | report builder | Raw paired arrays | `8aaea1ef...d830` | Yes | Yes | Primary source table |
| Condition means | Means, SDs, and paired deltas | report builder | All seeds table | `90b9b127...ef69` | Yes | Yes | Primary comparison table |
| Paired contrasts | Teacher and constraint contrasts | report builder | All seeds table | `c3273333...120d` | Yes | Secondary | No population inference |
| Per-task deltas | Task-family diagnostics | report builder | Raw paired arrays | `843002db...6de` | Yes | Secondary | Not official benchmark scores |
| Test NLL figure | Primary visual | report builder | All seeds table | `efaf6960...4798` | Yes | Yes | Dots are seeds; bars are sample SD |
| Development figure | Fixed-checkpoint supporting visual | frozen analysis; curated copy | 60 dev manifests plus A5 curves | `14553374...e942` | Yes | Supporting | No checkpoint selection |

Complete per-condition checkpoint, training, and raw-record hashes are retained
in [verification.json](/data/250010109/MoE_Router/reports/a6_20260909/verification.json).

## 15. Links

anchor: [A15_13_10](../../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_10_sae_flat_router_functional_anchor.md)  
protocol: [A6 Protocol](protocol.md)  
summary: [A6 Summary](summary.md)  
code workspace: [immutable source](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z/source)  
runner: [full_run.py](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z/source/full_run.py) and [acp_full.sh](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z/source/acp_full.sh)  
config: [config.py](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z/source/config.py)  
data / manifest: [formal manifest](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z/formal_manifest.json)  
result dir: [formal run](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z)  
figure dir: [curated figures](figures)  
logs / checkpoints: [formal run root](/data/250010109/MoE_Router/experiments/20260908_online_sae_gmm_regularized_router/runs/full-20260908T183139Z)  
repro command: `cd /data/250010109/MoE_Router/reports/a6_20260909 && python -m pytest -q test_build_report.py && python build_report.py`  
job ids: qualification `pt-80s7l3fm`; formal `pt-jn404t7l`.
