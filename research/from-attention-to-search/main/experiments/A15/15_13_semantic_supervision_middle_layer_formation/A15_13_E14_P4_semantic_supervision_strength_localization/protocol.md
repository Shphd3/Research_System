# Protocol: A15_13_E14_P4 Semantic-Supervision-Strength Localization

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL
Approval status: A--F HUMAN_CONFIRMED on 2026-09-07 by the instruction to follow
  "0906 校正Router假设并规划验证"; G full execution scope HUMAN_CONFIRMED in the same instruction
Block audit status: A--G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: implementation, disposable two-update smoke, two weak-arm 512-update runs,
  development-only analysis, and canonical result records
Design frozen at / registered revision: 20260907-P4-v1 before implementation
Purpose: separate reduced harm from a positive semantic-supervision increment
Primary Anchor: 15_13_05_gmm_pseudolabel_oracle_gap_anchor.md
Anchor decision question: does halving the current auxiliary weight repair the replicated instability,
  and does the repaired signal then beat task-only training?
Anchor physical prior tested: the P3 seed reversal may be caused by an avoidable cost of the current
  auxiliary weight rather than absence of useful sample-to-label information
Anchor core model term tested: current-minus-weak and task-minus-weak development answer-NLL effects
Anchor falsifier: weak fails to improve over current in both seeds under the registered intervals
Experiment role: root-cause localization on an already-open development surface
Primary metric from Anchor: summed reference-answer NLL divided by summed answer tokens
Claim boundary from Anchor: local 512-update development behavior only
Minimal setup: frozen P3 data, teacher, hierarchy, load-off policy, seeds 17/29, and checkpoints
Treatment and controls: H-sem-weak at 0.25/0.25 versus current H-sem at 0.5/0.5 and H-task at 0/0
Changed variable: the common parent and child auxiliary-loss coefficient
Held fixed: base, data, teacher, architecture, initialization, record order, optimizer, schedule,
  512-update budget, load policy, evaluator, and checkpoint rule
Conditions to run: only H-sem-weak for seeds 17 and 29; reuse verified P3 controls
Pass: weak beats current and task-only separately in both seeds
Fail: half-weight repair does not replicate against current; exact typed outcomes are in Section 15
Insufficient: missing/ineligible evidence or a comparison whose interval does not resolve its boundary
Cannot claim: P3 is retrospectively positive, 0.25 is globally optimal, general semantic benefit,
  teacher truth, expert function, free-generation gain, or untouched-test confirmation
Approval decision: execute this exact bounded P4 without extra weights, seeds, layers, or teacher changes
```

The one-H100 serial execution choice is an engineering realization of the approved two-run scope. It
uses one `n6ls.iu.i40.1` worker under reserved quota, retry zero, and a two-H100-hour ceiling. If the
measured job cannot fit that ceiling, stop and record `RESOURCE_LIMITED_INCOMPLETE`; do not change the
scientific design.

## 1. Terminology / Definitions

- **Reduced harm:** H-sem-weak has lower development answer NLL than current H-sem. This says the
  current 0.5/0.5 penalty has avoidable cost; it does not say adding semantic supervision helps.
- **Net semantic-supervision benefit:** H-sem-weak has lower development answer NLL than H-task. This
  is the minimum task-facing evidence that adding the weaker semantic target helps in this setup.
- **Answer NLL:** summed negative log probability of reference-answer tokens divided by their token
  count, in nat per answer token; lower is better. It is not free-generation accuracy.
- **Weak/current/task arms:** identical online hierarchical adapters with parent/child auxiliary
  coefficients 0.25/0.25, 0.5/0.5, and 0/0 respectively.
- **Development-only localization:** the P3 development split was already inspected and now selects a
  causal explanation. It may diagnose P3 but cannot serve as untouched confirmation.
- **Replicate:** the registered paired interval satisfies the same directional rule separately in
  both model seeds. Two seeds are not a population estimate.

## 2. Anchor Alignment

P3 found that current H-sem beats a legal-pair-shuffled auxiliary control in both seeds but beats the
same-architecture task-only control only in seed 17. A no-training audit found the opposite seed
directions from update 128 through 512, no registered operational anomaly, and a large route-load shift
under H-sem. Those observations nominate auxiliary strength as one live cause but do not prove it.

P4 changes only that coefficient. It does not rewrite the frozen P3 Protocol, reopen its test verdict,
or compare another teacher, layer, hierarchy, load policy, or privileged path.

## 3. Tested Hypothesis

Let \(L_{w,s}\), \(L_{c,s}\), and \(L_{t,s}\) be update-512 development answer NLL for weak, current, and
task-only arms in seed \(s\in\{17,29\}\). Define

\[
\Delta_{harm,s}=L_{c,s}-L_{w,s},\qquad
\Delta_{benefit,s}=L_{t,s}-L_{w,s}.
\]

The causal hypothesis is that the current auxiliary penalty is too strong. It predicts
\(\Delta_{harm,s}>0\) in both seeds. The stronger method-value hypothesis additionally predicts
\(\Delta_{benefit,s}>0\) in both seeds. The strongest rival is that lowering the penalty merely moves
the model toward task-only training, reducing a cost without extracting positive semantic value.

## 4. Rival Explanations

1. **Different initialization or order:** require matching initial adapter tensors and deterministic
   same-seed record streams across all three arms.
2. **Different implementation path:** add one explicit coefficient field while proving the default
   0.5 path remains numerically identical and the 0.25 path changes only the auxiliary combination.
3. **P3 artifact drift:** hash and validate every reused control array, initial checkpoint, final
   checkpoint, guard, teacher assignment, processed dataset, and relevant source file before use.
4. **Late checkpoint selection:** update 512 is fixed before execution; 128/256/384 are descriptive.
5. **Averaging away seed disagreement:** apply every decision rule separately to seeds 17 and 29;
   no seed pooling enters the verdict.
6. **Calling less damage a gain:** keep \(\Delta_{harm}\) and \(\Delta_{benefit}\) as separate conjunctions.

## 5. Data Construction And Provenance

Reuse the exact P3 processed tensor at
`/data/250010109/datasets/a15_e14_p3_clean/processed.pt`: 39,576 train, 8,481 development, and 8,481
test records from eight sources after global record-ID and normalized prompt-plus-answer deduplication.
P4 trains on the same train rows and reads only the existing development rows. It must not evaluate,
select, or report a new P4 effect on test.

Reuse the exact P3 train-only teacher assignments from eligible run
`/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training/runs/full-20260906T170500Z`.
The teacher is final-layer whole-window PCA64 plus a three-parent diagonal GMM with 3/3/2 leaves. It is
privileged training supervision, not semantic truth.

## 6. Learning Task And Permitted Supervision

Every arm predicts the next reference-answer token from the ordinary causal prefix. Routers read only
the current block-14 input. Weak and current arms receive the same train-record parent and conditional
child pseudo-labels; task-only receives no pseudo-label loss. No teacher path, source ID, final-layer
state, future token, or test field enters online routing.

## 7. Model / Architecture And Frozen Variants

Freeze Qwen3-0.6B-Base, embeddings, and language head. At zero-indexed block 14, the same hierarchy
adds rank-8 shared, selected parent, and selected child low-rank residuals. Routers read the 1024-wide
block input; experts read the 3072-wide down-projection input. Online selection and probability scaling
are identical to P3; load balancing remains off.

All three same-seed arms must begin from byte-identical trainable tensors. P3 H-task and current H-sem
checkpoints and development arrays may be reused only after their recorded initial tensors match each
other and a freshly constructed weak initial state under that seed.

## 8. Training Objective And Optimization

For answer loss \(L_{answer}\), parent classification \(L_{parent}\), and child classification restricted
to the teacher parent \(L_{child\mid teacher\ parent}\),

\[
L(\lambda)=L_{answer}+\lambda L_{parent}+\lambda L_{child\mid teacher\ parent}.
\]

P4 runs only \(\lambda=0.25\). Reused P3 current and task arms have \(\lambda=0.5\) and \(0\). Losses are
means over answer-prediction positions per microbatch. Use the P3 AdamW groups, learning rates
(`2e-4` experts, `5e-4` Routers), betas `(0.9,0.999)`, epsilon `1e-8`, weight decay 0.01, gradient clip
1.0, microbatch 8, accumulation 16, 26-update linear warmup, cosine decay, and 512 updates.

## 9. Conditions, Seeds, And Checkpoints

Run `H-sem-weak` at seeds 17 and 29 from update zero. Save update 0, 128, 256, 384, and 512 plus final
and recovery state. Run the two conditions serially on one H100. Reuse P3 `H-task` seed 17 from
`preflight_512`, P3 `H-task` seed 29 from `formal_512`, and both P3 `H-sem` controls from `formal_512`.
No other condition is authorized.

## 10. Primary Metric And Frozen Analysis Plan

For each arm \(m\) and complete development record \(i\), store loss sum \(x_i^m\) and answer-token count
\(n_i\). Compute

\[
L_m=\frac{\sum_i x_i^m}{\sum_i n_i}.
\]

The observation and resampling unit is one complete development record; the replication unit is one
model seed. For each seed separately, compute current-minus-weak and task-minus-weak at update 512.
Use 2,000 percentile paired bootstrap draws with NumPy seed 20260907, resampling records with
replacement within each of the eight sources while preserving source counts. Report the point effect
and two-sided 2.5/97.5 percentiles. Positive favors weak.

No outlier removal, source exclusion, seed pooling, multiplicity rescue, missing-value imputation, or
checkpoint selection is allowed. A mismatch in record IDs, sources, answer-token counts, or split makes
the affected contrast ineligible. The two harm contrasts form one conjunction; the two benefit
contrasts form a second conjunction. Section 15 maps them to typed outcomes.

## 11. Secondary Metrics And Guards

Report the two effects at updates 128/256/384 as descriptive trajectories; route loads, parent/child
classification loss, gradient norms, expert deltas, runtime, and exposure counts are diagnostics only.
Required guards are finite histories; exact data and teacher identity; expected parameter counts;
unchanged frozen embedding/head hashes; all expected expert A/B matrices changed; exact control hashes;
same-seed initial-state identity; same record stream; and matched development arrays.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: a pure loss-combination test returns \(1+0.5(2)+0.5(4)=4\) for current and
  \(1+0.25(2)+0.25(4)=2.5\) for weak.
- Known bad: weak resumes from a current checkpoint, changes a teacher/data field, or differs in initial
  tensors/order; stop and exclude it.
- Known confusing: weak beats current but ties or loses to task-only. This is reduced harm without
  replicated semantic benefit, not method success.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input / how | Expected output | Pass / stop | Artifact / handoff |
| --- | --- | --- | --- | --- | --- |
| Identity audit | establish valid reuse | hash P3 controls, data, teacher, code; compare same-seed initial tensors and record streams | machine-readable receipt | all exact or stop `INELIGIBLE` | `receipts/identity.json` |
| Unit tests | isolate coefficient behavior and verdict logic | run red-green regressions plus full worker tests | test log | zero failures or stop | `logs/tests.log` |
| Disposable smoke | prove weak path on real model | two updates, seed 17, 32-record development evaluation | finite loss, gradients, changed banks | pass or stop; discard weights | `conditions/smoke/`, `receipts/smoke.json` |
| Formal weak training | create only missing evidence | seed 17 then 29, 512 updates each | histories, checkpoints, dev arrays, guards | both complete and eligible or stop affected arm | `conditions/formal_512/` |
| Frozen analysis | separate two questions | registered paired bootstrap on development | effects, typed verdict, figure | exact Section 15 mapping | `analysis/`, then Summary/Detailed |

## 14. Algorithm, Output, And Provenance Contract

The worker must: validate identities; snapshot this Protocol; run tests; run and discard smoke; train
the two weak arms; collect existing and new development arrays; assert pair identities; compute four
registered update-512 intervals; render one figure with separate harm and benefit panels; emit a typed
verdict; and write a complete artifact manifest. Raw checkpoints/logs remain in the worker workspace.
Curated Protocol, Summary, Detailed, decisive CSV/JSON, and one figure are copied here.

Execution surface: ACP workspace `share-space`, AEC2 `share-cluster`, one node, worker spec
`n6ls.iu.i40.1`, one H100 80GB, reserved quota, retry zero. Container image is the last eligible P3
image unless platform inspection shows it unavailable. Code root is
`/data/250010109/MoE_Router/experiments/20260906_a15_13_e14_p3_matched_training`; P4 outputs go to a
new `runs/p4-weight-<UTC>` root. Record code/config/protocol/data/teacher/control hashes before smoke.

## 15. Success / Failure / Insufficient Evidence

Apply this precedence after eligibility:

1. `HALF_WEIGHT_REPAIR_WITH_REPLICATED_SEMANTIC_BENEFIT`: all four lower endpoints exceed zero.
2. `HALF_WEIGHT_REDUCES_HARM_WITHOUT_REPLICATED_SEMANTIC_BENEFIT`: both harm lower endpoints exceed
   zero, but at least one benefit lower endpoint does not exceed zero. State each benefit direction;
   do not collapse uncertain and reliably negative evidence.
3. `HALF_WEIGHT_REPAIR_NOT_REPLICATED`: at least one harm interval upper endpoint is at most zero.
   This rejects the exact 0.25 repair as the two-seed explanation, not every lower weight.
4. `HALF_WEIGHT_LOCALIZATION_INSUFFICIENT`: no harm interval is reliably nonpositive, but the two harm
   lower endpoints do not both exceed zero.
5. `INELIGIBLE` or `INCOMPLETE`: a guard fails or an approved weak arm is absent. These take precedence
   over scientific outcomes.

The benefit conjunction never rescues a failed harm-reduction conjunction because P4 first tests the
named cause of the P3 reversal.

## 16. What This Cannot Claim

Even the strongest P4 outcome cannot turn P3's test verdict into Pass, establish 0.25 as an optimum,
estimate a population seed effect, validate the GMM groups as semantic truth, prove hierarchy or expert
function, or establish free-generation, deployment, or uncontaminated public-benchmark gains. A P4
positive result requires a future untouched confirmation before a general method claim.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A question/boundary | CONFIRMED | user selected the referenced harm-versus-benefit correction |
| B data | CONFIRMED | exact P3 train/development artifacts reused; no P4 test use |
| C task/supervision | CONFIRMED | 0/0.25/0.5 distinction in the referenced instruction |
| D architecture | CONFIRMED | identical P3 H architecture and online path |
| E objective/optimization | CONFIRMED | only common auxiliary coefficient changes; 512 fixed |
| F evidence | CONFIRMED | separate harm and task comparisons in both seeds |
| G execution | CONFIRMED | user requested execution; bounded one-H100 realization, retry zero, two-hour ceiling |

Cross-block audit: `PASS`. The data expose the registered development behavior; supervision fields obey
the online boundary; all three arms share architecture and schedule; only the coefficient changes;
the two control contrasts answer different questions; and the resource/stage contract can execute the
two missing arms without opening test.

2026-09-07 approval record: the researcher instructed this task to follow “0906 校正Router假设并规划
验证”, make the correction, and advance the understanding while distinguishing “减少监督带来的伤害”
from “真正获得语义监督收益”. That referenced instruction fixes the 0/0.25/0.5 arms, seeds 17/29,
fresh weak training from common initial states, 512 updates, development-only localization, and no
multi-agent execution. It authorizes this exact implementation, smoke, full two-run execution, analysis,
and result recording. It does not authorize another weight, seed, layer, teacher, H-hard/H-oracle,
commit, push, sync, or publication.

After execution starts, the registered scientific body is immutable. Any material change requires an
append-only amendment recording before/after values, reason, visible evidence, affected blocks and
conditions, approval, and eligibility impact.

## 18. Append-Only Execution Amendments

### Amendment P4-A1 — Runtime environment propagation (2026-09-07)

- **Before:** the first submitter omitted the audited runtime-layer activation. The second submitter
  activated it but then overwrote `PYTHONPATH` in the remote command; the worker wrapper also replaced
  the inherited `PYTHONPATH`. Jobs `pt-yajflax0` and `pt-n4ilzz1d` therefore stopped at the registered
  smoke boundary with `ModuleNotFoundError: transformers` and produced no eligible weak-arm evidence.
- **After:** the approved runtime layer is sourced before the P4 runner; the remote command prepends
  the P4 root while preserving the activated `PYTHONPATH`; child worker environments prepend the P4
  root while preserving the inherited runtime path.
- **Reason:** repair an execution-environment propagation failure identified from the failed smoke logs.
- **Visible evidence before repair:** `runs/p4-weight-20260907T021000Z/receipts/failure.json` and
  `runs/p4-weight-20260907T023600Z/receipts/failure.json`.
- **Affected blocks and conditions:** Block G and code/config provenance only; no change to data,
  teacher, architecture, supervision coefficient, seeds, checkpoints, metric, verdict rule, or
  confirmation boundary.
- **Approval:** the researcher-authorized execution instruction covered implementation repair, smoke,
  full run, analysis, and result recording within this bounded P4.
- **Eligibility impact:** the two failed attempts are `INELIGIBLE` for scientific comparison. The
  subsequent successful job `pt-ahj3yiaw` is eligible only under the unchanged guards and registered
  analysis rules, all of which are recorded in the result files.
