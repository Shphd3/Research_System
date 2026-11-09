# Protocol: A6R1 S0--S6 Functional And Incremental-Learning Audit

## 0. Approval Snapshot

**Document status:** `APPROVED_FOR_LOCAL_IMPLEMENTATION_AND_SMOKE`; the full
scientific design is frozen before post-training outcomes are read. The
researcher requested one unified reserved four-H100 full run, but the numeric
wall/GPU-hour ceiling remains `AI_PROPOSAL` until it is surfaced after smoke.

**Approval status:** Blocks A--F are `CONFIRMED` by the researcher's approval
of the named S0--S6 track on 2026-09-09. Block G is `CONFIRMED` for local
implementation and smoke and `PENDING_NUMERIC_BUDGET_CONFIRMATION` for ACP
creation. Cross-block consistency is `PASS` for the design and local scope.

**Purpose:** Determine whether lower-decay structural routing reaches actual
expert function and creates a bounded learning partition that improves
sequential new-task adaptation beyond fixed-capacity controls.

**Primary Anchor:** `15_13_11_structural_routing_incremental_learning_anchor.md`.
Its decision question is whether a data-driven reuse/growth policy improves
the new-task versus retained-task frontier after six-task training. Its
falsifier is a matched fixed-capacity policy that reaches the same frontier or
any growth advantage that reverses across seeds, damages old tasks, or appears
equally in task-only.

**Experiment role:** root-cause audit (S0--S5) followed by one bounded
sequential-task method test (S6).

**Primary metric:** S6 structural growth increment
\(I^{struct}=I^{gmm_b}-I^{task_only}\) in nat per answer token, where each \(I\) is
the held-out new-task gain of the selected eligible growth treatment over the
best eligible fixed-capacity treatment. Eligibility requires old-task damage
upper 95% interval at most `0.001 nat/token`.

**Minimal setup:** S0--S3 use five conditions by three seeds at update 512;
S4--S5 use matched task-only and selected GMM-B checkpoints with registered
conditional branches; S6 retrains task-only and GMM-B from matched update-zero
initializations on six tasks for seeds 17/29/43, then reveals HumanEval and
MBPP in order.

**Treatment and controls:** structural GMM-B versus task-only; within each,
no update (K), Router-only (R), routed-old-expert (U), joint Router-plus-old
expert (F), constant-gated correction (C), and input-gated correction (G).
Known-boundary invocation is a diagnostic reference; an answer-loss detector
without task ID is the automatic treatment. Old-only and old-mixture-shift
streams are false-growth controls.

**Changed variable:** the registered routing regularizer, intervention, update
parameter subset, or local correction for the current stage only.

**Held fixed:** Qwen3-0.6B backbone and language head, layer 27 input object,
rank 16, eight original experts, answer mask, seeds, task order, support IDs,
replay budget, 16 adaptation updates, optimizer family, evaluation panels,
load-bias semantics, thresholds, and original checkpoints/artifacts.

**Pass:** the S6 Anchor Pass rule holds for at least one later task with at
most 16 support records, and all implementation/leakage guards pass.

**Fail:** fixed capacity matches/wins, the structural increment reverses in a
seed, retained loss exceeds tolerance, input gating does not beat constant
capacity under the registered frontier, or automatic permanent growth occurs
on either control stream.

**Insufficient:** invalid source identity, teacher future-task leakage, failed
tail/no-op parity, unsupported fixed panels, automatic no-trigger, nonfinite
training, incomplete condition coverage, or intervals spanning the decision
region. Automatic no-trigger does not invalidate the known-boundary result.

**Cannot claim:** true semantic classes, backbone-level unseen knowledge,
official benchmark performance, universal capacity exhaustion, deployment-
ready unlabeled change detection, or long-horizon continual learning.

**Approval decision:** local implementation, tests, CPU synthetic smoke, and
single-GPU real-model smoke are authorized. One unified ACP run on one
`n6ls.iu.i40.4` reserved four-H100 node in `share-space/share-cluster` is
requested; create is held only for the numeric budget confirmation surfaced
after measured smoke throughput. Commit, push, publication, Graph edit, root
sync, and external artifact transfer are not authorized.

## 1. Terminology / Definitions

- `task_only`: matched online Router/expert learning with answer-token loss.
- `gmm_b`: the A6R1 pairwise, permutation-invariant relation regularizer using
  a frozen token-level diagonal GMM teacher.
- `S0--S5`: post-training audit on completed A6R1 checkpoints; short updates
  occur only in isolated copies.
- `S6`: separate chronological training in which two tasks are excluded from
  initial adapter training and arrive later.
- `new-task gain`: stage-start test NLL minus post-adaptation test NLL.
- `old-task damage`: post-adaptation old-task test NLL minus stage-start NLL.
- `eligible`: passes source, parity, data-separation, finite-training, and
  retained-loss guards. It does not mean scientifically favorable.
- `permanent growth`: a C/G correction retained after development selection;
  candidate trials that are discarded still count toward compute cost.
- `one-record adaptation`: exactly one unique training record, possibly
  repeated over 16 updates; it is not one supervised token.

## 2. Anchor Alignment

A6R1 asks whether weaker structural pressure restores task loss. It completed
with a GMM-B mean improvement but a seed-43 reversal, so no stable method win
exists. This protocol does not reopen that verdict. S0--S5 locates which link
in \(q\rightarrow p\rightarrow k\rightarrow E_k(h)\rightarrow L\) is present;
S6 tests the Anchor's separate learning-frontier relation. Routing agreement,
expert intervention, local transfer, and sequential end-task gain remain
distinct claims.

## 3. Tested Hypothesis

If pairwise GMM structure organizes examples by compatible future updates,
then GMM-B should show non-interchangeable expert effects or bounded local
interference, and its eligible local-growth advantage over fixed capacity
should exceed the corresponding task-only advantage when later tasks arrive.
The decisive evidence is S6 held-out loss, not S2 route agreement or S5
development selection.

## 4. Rival Explanations

1. The teacher changes probabilities but not selected computation.
2. Experts differ currently but their updates remain mutually beneficial.
3. Routing is wrong and R is sufficient.
4. Old capacity is sufficient under U or joint F adaptation.
5. Generic extra capacity C explains any apparent G gain.
6. A detector responds to ordinary old-task mixture shift rather than new
   learning demand.
7. GMM-B's growth increment is no larger than task-only's and therefore does
   not evidence a structural routing contribution.

## 5. Data Construction And Provenance

The immutable data artifact is
`/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/data/data.pt`,
SHA256 `58e409ca9d903d146c9ae8e3cee834a4eb5f0e6f2e24de4fe521349d05e527f2`.
Its train/development/test record IDs and content hashes remain disjoint.

S0--S5 inherit the stable record-hash split: D versus F by
`SHA256("A6-analysis-v1|"+record_id)` parity; F is split modulo three by
`SHA256("A6-probe-v1|"+record_id)` into route, transfer, and growth panels.
Each panel keeps at most 64 records per task and at most four causal answer
positions per record. D selects; an F panel only evaluates the choice frozen
for that stage.

S6 orders task names by `SHA256("continual-v1|"+task_id)`: MMLU, MATH, GSM8K,
GPQA, BBH, MMLU-Pro, HumanEval, MBPP. Stage 0 may train only on the first six
named tasks in that order; HumanEval and MBPP records are forbidden from
the six-task GMM fit, target construction, schedule, threshold calibration,
or checkpoint selection.

For each later task and seed, sort training records by
`SHA256("S6-support|task|seed|"+record_id)`. The first 64 form the nested
support pool. Known-boundary sweeps use prefixes of 1/4/16/64 and restore the
same stage-start state for each prefix. Automatic S6 uses 64 stream records in
two 32-record detection windows; after a trigger, records are deterministically
split into 48 candidate-update and 16 development-selection records. Final
new-task measurement uses a fixed test panel of at most 64 records sorted by
`SHA256("S6-test|task|"+record_id)` and is never used for treatment selection.

Replay uses 32 deterministic train records from each previously seen task,
sampled by `SHA256("S6-replay|stage|task|seed|"+record_id)`. Old retention uses
up to 64 fixed test records per seen task. Record IDs, not answer text or
loss, determine all panels. Cross-rewrite family metadata is unavailable, so
cross-rewrite independence is unknown.

The early-only GMM uses PCA-64 and eight diagonal components, fit on at most
65,536 answer-position states drawn uniformly without replacement from
Router-fit records belonging only to the first six tasks. Fit seed is 17029,
`n_init=3`, `max_iter=100`, tolerance `1e-3`, covariance floor `1e-6`.
The original SAE and feature groups are frozen; SAE provides only the common
coverage mask. Future-task records cannot affect either fit or mask cache used
by stage-0 gradients.

## 6. Learning Task And Permitted Supervision

The model input is the visible causal token prefix. The required output is the
next answer token; loss is ordinary answer-token cross entropy. During stage-0
training, task ID is permitted only to exclude future tasks and construct the
fixed schedule. It is not a Router input. During automatic adaptation, labeled
answer loss in completed 32-record windows is permitted for detection and
candidate selection; task ID is forbidden to the detector and policy but
retained for audit and stratification.

Candidate updates may use only the registered support and replay records.
Development records select among K/R/U/F/C/G and cannot contribute gradients.
Test records confirm the frozen action and cannot select, stop, or tune it.
Invalid or insufficient windows produce a typed no-action/Insufficient state.

## 7. Model / Architecture And Frozen Variants

The frozen backbone and language head are Qwen3-0.6B-Base. At zero-indexed
layer 27 MLP pre-input \(h_t\), one shared rank-16 branch and eight rank-16
experts add a parallel residual. The Router is a trainable 1024-to-8 affine
map. Top-1 uses logits plus the nonparameter load bias; the selected expert is
scaled by its unbiased softmax probability. Original A6R1 artifacts are
read-only.

R updates only Router weight/bias. U updates only routed old experts. F updates
Router and all old experts jointly and is the strongest fixed-capacity control;
the shared branch remains frozen to isolate local capacity. C/G freeze the old
system and append one rank-16 correction under a parent-route mask. C uses one
learned scalar sigmoid gate; G uses a learned affine sigmoid of \(h_t\). Both
start with zero correction output and gate 0.5, reproducing K within the S0
loss tolerance. At most two corrections may be committed in the sequential
stream, one per later task.

## 8. Training Objective And Optimization

Stage-0 task-only minimizes token-normalized answer loss. Stage-0 GMM-B adds
the A6R1 pairwise relation term with structural coefficient linearly decaying
from `0.01` at update 1 to `0.001` at update 512. It uses 512 effective
updates, 128 sampled records per update, microbatch 8, expert/shared AdamW LR
`2e-4`, Router LR `5e-4`, expert weight decay `0.01`, warmup 26, cosine decay,
and gradient clip 1.0. The two lineages use identical per-seed six-task
schedules generated by `torch.randint` over only early-task record indices.

Every S5/S6 short treatment uses 16 updates, four target and four replay
records per update, cycling a fixed record order. Its objective is one half
target token-normalized loss plus one half replay token-normalized loss. R and
gate parameters use LR `5e-4`; old experts and correction banks use LR
`2e-4`; weight decay is zero and gradient clip is 1.0. K has no optimizer.
Load bias is frozen during short adaptation. Known-boundary support-size runs
restore the exact stage start and cannot inherit a larger-support state.

For automatic selection, each candidate starts from the same stage state.
Choose the lowest development new-task NLL among candidates whose development
old-task damage upper 95% record-bootstrap interval is at most `0.001`; ties
use K, R, U, F, C, G in that order. If no non-K candidate is eligible, commit
K. Test results cannot alter the selected treatment.

## 9. Conditions, Seeds, And Checkpoints

S0--S3 inputs are task-only, SAE-A-decay, GMM-A-decay, SAE-B-decay, and
GMM-B-decay times seeds 17/29/43: 15 authenticated update-512 checkpoints.
Old constant-0.1 A6, frozen-router A5 SAE/GMM, random, and Dense conditions are
excluded. S4/S5 use task-only and GMM-B-decay for all three seeds after seed-17
D selection. K/R/U/F/C/G are isolated derivatives, not pretrained models.

S6 stage 0 has task-only and early-only-GMM-B times seeds 17/29/43. Each later
task evaluates support sizes 1/4/16/64 at checkpoints 0/1/4/8/16. The automatic
stream and known-boundary reference use the 64-record buffer; the primary
few-shot verdict is restricted to at most 16 records.

## 10. Primary Metric And Frozen Analysis Plan

For every record, sum answer-token cross entropy and retain answer-token count.
Aggregate NLL as total loss sum divided by total answer tokens. New-task gain,
old-task damage, \(I\), and \(I^{struct}\) follow the Anchor equations and use
`0.001 nat/token` as the practical threshold.

The record is the observation unit; seed is the independent training unit.
Use 1,000 record-level bootstrap draws stratified by task and recompute
token-weighted quantities. Single prespecified effects use two-sided 95%
intervals. Report every seed separately and an equal-seed mean/sample SD;
bootstrap draws never replace seeds. Missing records, failed conditions, and
nonfinite values yield Insufficient; there is no outlier exclusion or
interpolation.

Primary Pass/Fail/Insufficient is exactly Section 6 of the Anchor. The unsealing
point is creation of the first A6R1 S0 output or S6 stage-0 update, whichever
comes first. After that point no task order, model list, support ID, treatment,
selection rule, threshold, interval, or verdict mapping may change without an
append-only amendment and explicit eligibility ruling.

## 11. Secondary Metrics And Guards

S1 reports complete internal NLL and curves but cannot decide mechanism. S2
reports teacher entropy, \(KL(q\Vert p)\), pairwise route relation, unbiased and
balance-biased choices, selected coefficient, and loads. S3 reports shared and
expert deletion, fixed-coefficient all-expert replacement, self-replacement
error, and choice gap. S4 reports 2-by-2 transfer matrices. S5 reports
gain-damage-cost and gate-mean ablation. S6 reports unique support records,
answer-token exposure, updates, detection latency, unnecessary alerts/checks/
growth, candidate and committed cost, cumulative parameters, and per-stage
new/old NLL.

S2 enters S3 only after valid teacher variation and a registered path/probability
change. S3 enters S4/S5 only after self-parity and adequate fixed support. S4
enters S5 for supported cross-damage, persistent local learning failure, or an
S3 routing/capacity rival. S6 known-boundary sweeps always execute as requested;
its automatic growth branch may legitimately commit K when detection or
development constraints do not support adaptation.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: native route and target loss replay; self-expert replacement;
  C/G zero-output initialization; nested supports are exact prefixes.
- Known bad: a future-task record inserted into early schedule/GMM sample; a
  one-record run inheriting a 64-record state; detector receiving task ID; test
  loss selecting a candidate; correction initialization changing K.
- Known confusing: GMM high posterior means relative component assignment, not
  familiarity; route agreement is not expert utility; no trigger is detector
  failure but not missing known-boundary evidence; frozen old parameters do not
  guarantee frozen old outputs when a correction gate fires.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input and assumptions | How | Why | Expected output | Pass / fail / insufficient | Named failure | Artifact | Handoff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S0 | Eligibility and replay fidelity | 15 final checkpoints, immutable data/source | authenticate hashes/init/schedules; build fixed panels; prove tail parity | prevent old-A6 or wrong-path evidence | input, panel, parity ledgers | pass or typed affected-scope stop | identity/cache/parity failure | `S0/*.json`, cache | eligible inputs to S1--S3 |
| S1 | Task effect | complete registered A6R1 evaluations | paired total/per-task NLL and AUC | define effect without mechanism | four tables, candidate lock | descriptive complete/incomplete | unpaired/missing eval | `S1/*` | mean-selected GMM-B as audit candidate |
| S2 | Route transfer | D/F-route causal states | compare q,p,k,k0,coefficient,bias/load relations | separate probability from path | relation/load tables | path/probability branch or stop | teacher/denominator/support failure | `S2/*` | valid path question to S3 |
| S3 | Current expert function | same fixed states and coefficients | deletion and all-eight expert replacement | separate route from function and unused capacity | ablation/counterfactual/gap tables | functional candidate, reroute candidate, or stop | self-replay failure | `S3/*` | fixed candidate to S4/S5 |
| S4 | Local update compatibility | D-locked pair; disjoint U/F-transfer | 0/1/8 expert-only updates from identical copies | expose sharing/interference | lock, matrices, invariant/cost ledgers | interference/failure/share/insufficient | support or frozen-state failure | `S4/*` | registered trigger to S5 |
| S5 | Local action frontier | one locked group and common target/replay | K/R/U/F/C/G, 16 updates, gate-mean ablation | separate reroute/reuse/generic capacity/input gate | curves/frontier/gate/cost | local winner or bounded stop | init/retain/selection failure | `S5/*` | action definitions to S6; not result reuse |
| S6a | Future-clean stage 0 | update-zero states; first six tasks only | fit early GMM; train task-only/GMM-B 512 updates | create chronological starts | six checkpoints and leakage ledger | all valid or affected lineage insufficient | future leak/schedule/training failure | `S6/stage0/*` | per-seed stage starts |
| S6b | Known-boundary few-shot | fixed later-task order and nested supports | independent K/R/U/F/C/G runs at 1/4/16/64 | estimate sample-efficiency frontier | learning curves and test effects | pass/fail/insufficient per size | inherited-state or support mismatch | `S6/known_boundary/*` | frozen comparative effects |
| S6c | Automatic stream | old calibration, mix shift, then two later tasks | 32-record NLL windows; two exceedances; candidate trial/commit | test detection plus bounded action | alerts/checks/commits/cost/state ledger | correct/false/no trigger and retained result | task-ID/test leakage | `S6/automatic/*` | final S6 metrics |
| Final | Completeness | all stage states and receipts | verify hashes, coverage, thresholds, costs | preserve evidence lineage | completion and artifact manifest | complete or typed partial/invalid | missing artifact | root manifest | result records after audit |

## 14. Algorithm, Output, And Provenance Contract

Implementation root:
`/data/250010109/MoE_Router/experiments/20260909_a6r1_post_training_analysis`.
The unified entry point is `source_all/run_all.py`; local diagnostic smoke uses
`source_all/run_smoke.sh`, and the one-node four-GPU formal entry point is
`source_all/acp_full.sh`. S0--S3, S4, S5, future-clean S6 preparation, six
stage-0 lineages, known-boundary matrices, automatic streams, and finalization
all execute inside that one run directory.
Formal runs are immutable unique directories below `runs/`. Source, Protocol,
input checkpoints, data, teacher, panel manifests, and resource tuple are
hashed before submission. Resume is exact at stage/condition boundaries; an
existing final artifact is never overwritten.

Machine states are `NOT_STARTED`, `RUNNING`, `COMPLETE`,
`STOPPED_BY_DECISION_RULE`, `INSUFFICIENT`, or `FAILED_IMPLEMENTATION`.
Every stage writes its status atomically. Four GPU workers partition immutable
condition/seed/treatment assignments and merge only after all worker receipts
exist. Raw logs/checkpoints/caches remain in the execution workspace. Curated
`summary.md` and `detailed.md` will be written beside this Protocol only after
evidence completeness and human result judgment requirements are met.

Required final outputs are `input_manifest.json`, `selection_manifest.json`,
`stage_status.json`, per-stage tables, `evidence_ledger.csv`,
`artifact_manifest.json`, `completion.json`, and the ACP submission/worker
receipts. All compute, including discarded candidate trials, is recorded.

## 15. Success / Failure / Insufficient Evidence

Success means every registered stage either executes or reaches its frozen
typed stop, all mandatory model/seed/support/control coverage is present, and
the primary S6 mapping yields one auditable Pass/Fail/Insufficient verdict.
A stop branch is complete but cannot be relabeled favorable. Implementation
failure is repaired and rerun only before outcome-dependent choices are seen;
a scientific setting change requires amendment and renewed approval.

The preliminary full-run ceiling is `AI_PROPOSAL: 6 wall-hours on one reserved
4xH100 node = 24 H100 GPU-hours`, including qualification and all S0--S6
branches, with fail-closed partial artifacts at the cap. Smoke throughput will
produce the narrower estimate surfaced for confirmation before `sco acp jobs
create`. No seeds, support sizes, stages, or controls may be silently removed
to fit the cap.

## 16. What This Cannot Claim

Even a Pass cannot identify true semantic classes, prove the pretrained
backbone lacked the later-task knowledge, establish official HumanEval/MBPP
generation accuracy, show that all fixed model capacity is exhausted, or
validate an unlabeled deployment detector. It establishes only the registered
internal next-token adaptation frontier on this two-arrival stream and these
parameter/update budgets.

## 17. Block Confirmation, Freeze, And Amendment Ledger

- `2026-09-09`: the researcher explicitly changed the execution target to
  S0--S6, required missing smoke first, required S6 implementation, and
  requested one unified reserved four-H100 run. This confirms the named S0--S6
  track and local implementation/smoke scope.
- A--F: `CONFIRMED`; G local implementation/smoke: `CONFIRMED`; G ACP resource
  tuple: `CONFIRMED`; G numeric wall/GPU-hour ceiling: `AI_PROPOSAL_AWAITING_CONFIRMATION`.
- Cross-block consistency: `PASS` for scientific design and local scope. ACP
  create remains blocked only on the numeric budget confirmation.
- Design frozen at: first local A6R1 S0 output or S6 stage-0 update, whichever
  occurs first. Registered body: every byte before this Section 17 heading.
- Post-start changes use append-only amendments with before/after, reason,
  visibility of prior outcomes, affected blocks/conditions, approval, and
  eligibility impact. This ledger does not own observed results.
- `2026-09-09T05:12:00Z`, execution-boundary amendment `A6R1-PA-EXEC-001`:
  before = `AI_PROPOSAL: 6 wall-hours / 24 H100 GPU-hours`; after =
  `RESEARCHER_CONFIRMED: 4 wall-hours / 16 H100 GPU-hours` on the already
  confirmed one-node reserved `n6ls.iu.i40.4` tuple. Reason: measured
  exact-source smoke completed in about 9 minutes 22 seconds and the
  researcher instructed that the ceiling need not be increased and to submit.
  Visible evidence was limited to diagnostic smoke outputs explicitly marked
  `NOT_A_RESULT`; no formal result existed. Affected block: G execution and
  reproducibility only; conditions, seeds, support sizes, controls, metrics,
  thresholds, and verdict rules are unchanged. Approval: full unified ACP
  S0--S6 execution is authorized. Eligibility impact: none; the runner must
  fail closed at the confirmed cap without silently reducing coverage.
