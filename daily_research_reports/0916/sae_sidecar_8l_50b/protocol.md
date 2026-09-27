# Protocol: A8L raw final-Attention-output SAE sidecar 50B

## 0. Approval Snapshot

- Document status: **APPROVED_FOR_IMPLEMENTATION_AND_4H100_SMOKE_THEN_PASS_GATED_50B_SUBMISSION**
- Approval source: researcher messages on 2026-09-16 confirming raw Attention output,
  no sidecar Norm, implementation, Smoke, and a Smoke-PASS-gated full-run submission.
- Experiment role: method construction and training-trajectory collection.
- Purpose: construct one eight-layer model whose final Attention output receives a
  live SAE reconstruction gradient without changing the native LM forward path.
- Condition: one final-layer sidecar; no C/T arms and no second SAE.
- Primary engineering metric: every registered Smoke gate passes.
- Scientific result: `UNKNOWN`; this Protocol does not register semantic-success
  thresholds or treat reconstruction quality as semantic evidence.
- Approved execution: isolated implementation; one four-H100 reserved Smoke; only
  after Smoke `PASS`, submit one fresh 50B run on the same four-H100 reserved profile.
- Unauthorized here: first-layer implementation/Smoke, any eight-5090 run, extra
  conditions/seeds, publication, commit, or push.
- Cannot claim: semantic formation, functional specialization, long-run stability,
  or natural AuxK effectiveness from Smoke or submission health.

## 1. Definitions And Question Boundary

Let `x_7` be the input to Python `blocks[7]`, the eighth Transformer block. Let

\[a_7=\operatorname{Attention}_7(\operatorname{Norm1}_7(x_7))\]

denote the Attention module return after output projection `W_O` and before the
residual addition. The native main path remains

\[r_7=x_7+a_7,\qquad x_8=r_7+\operatorname{MLP}_7(\operatorname{Norm2}_7(r_7)).\]

The SAE sidecar reads `a_7` directly. There is no sidecar normalization and the
SAE reconstruction is not consumed by the main path or inference logits.

The local engineering question is whether this exact computation graph can be
trained, counted, logged, checkpointed, and resumed correctly at the frozen scale.
It is not yet a scientific test of domain-semantic improvement.

## 2. Data And Supervision

- Data: `/data/250010109/training_data_views/dclm_pair_v1/train`.
- Manifest SHA-256:
  `8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d`.
- Tokenizer vocabulary: `/data/share/Qwen3-0.6B-Base`; pretrained model weights
  are not loaded.
- Formal data exposure: fixed 30B continuous prefix, cycled to exactly
  50,000,000,000 valid next-token prediction targets.
- SAE positions: deterministic seed-17 sampling of one eighth of eligible target
  positions. No semantic labels enter training.

## 3. Architecture And Objective

- Backbone: eight layers; hidden1024; FFN3072; Q16/KV8; head dimension128;
  context2048; vocabulary151936; tied embeddings; RoPE theta1e6.
- SAE: one width-30000 Top-32 nonnegative dictionary; no identity skip; no side
  Norm; AuxK256; 10M sampled-position dead window; activity threshold1e-3.
- Parameters: backbone281,431,040; SAE61,471,024; total342,902,064.
- Initialization: fresh random seed17; do not resume from Smoke, serial SAE, or
  retired C/T checkpoints.

For sampled raw Attention outputs \(a_i\), the objective is

\[L=L_{\mathrm{LM}}+L_{\mathrm{rec}}+\frac{1}{32}L_{\mathrm{AuxK}}.\]

The SAE encoder input in \(L_{\mathrm{rec}}\) is live. Its target copy and target
energy denominator are detached. AuxK receives a detached input and detached
main-reconstruction residual, so it updates SAE parameters only. Global LM loss
uses the valid-target denominator; both SAE terms use the global sampled-position
denominator.

Gradient ownership:

- LM loss: native backbone and tied output weight; no SAE gradient.
- Reconstruction: SAE plus block-7 Attention/Norm1 and all upstream computation;
  no block-7 Norm2/MLP or final-model-Norm gradient.
- AuxK: SAE only.

## 4. Optimization, Coordinates, And Checkpoints

- Four ranks, sequence2048, microbatch2/GPU, gradient accumulation16; nominal
  complete-update global target count262144, with actual non-ignore masks authoritative.
- LM AdamW: lr3e-4, betas(.9,.95), epsilon1e-8, matrix weight decay.1.
- SAE AdamW group: lr3e-4, betas(.9,.999), no weight decay.
- Linear warmup for1000 LM and10 SAE updates, then constant; independent clip1.0.
- Primary curve coordinate: cumulative valid prediction tokens; update secondary.
- Permanent checkpoints: 0/.5/1/3/5/10/15/17/19/.../49/50B. Additional
  .1/.3/7/13B snapshots occur after the first complete update reaching the target.
  Recovery every1000 updates, retaining the latest two.
- TensorBoard under each run's `tensorboard/`, rank0 only, with global LM/total,
  raw and weighted reconstruction/AuxK, both coordinates, learning rates, gradient
  norms, valid-token count, SAE sample count, activity, and throughput.

## 5. Smoke And Scale-Up Rule

Resource: one node, four H100 80GB GPUs, `h100-4-reserved`, image
`shphd-lite-0911`. Smoke runs eight logical updates; it saves at update4,
intentionally exits, resumes in an independent process, and verifies update5.
Full-size forced-dead-mask CUDA qualification is separate from natural activity.

Required gates:

1. `sae_input` equals the actual `blocks[7].attn` return, with no side Norm.
2. Changing SAE parameters leaves LM logits unchanged.
3. LM, reconstruction, and AuxK gradients have exactly the registered owners.
4. Four-rank parameters, activity state, denominators, token/sample counts, and
   required scalars are synchronized and finite.
5. TensorBoard/JSONL tags and token/update coordinates satisfy the repository
   observability contract.
6. Model, optimizer, scheduler, RNG, data/sampling cursor, SAE activity buffers,
   and both coordinates restore; next-update replay passes.
7. `smoke_verification.json` is `PASS` and no failure artifact exists.

Any failed or missing gate stops scale-up. If all pass, submit one fresh 50B job
on `h100-4-reserved` without another approval prompt. Observe only scheduling,
four ranks, first finite update, durable logs/checkpoints, and immediate failure;
then stop polling while the job runs.

After that full-run submission, this reserved H100 resource is unavailable to the
first-layer variant. Its later Smoke may use only `5090-2-spot` and requires its
own isolated implementation and evidence; it is not authorized by this Protocol.

## 6. Artifacts And Failure Boundary

- Execution package:
  `/data/250010109/MoE_Router/experiments/20260916_attention_output_sidecar_last_50b`
- Smoke config: `configs/smoke_4h100_last_attention.json`
- Formal config: `configs/formal_4h100_last_attention_50b.json`
- Smoke run: `runs/smoke_last_attention_4h100_v1`
- Formal run: `runs/formal50b_last_attention_4h100`
- Submission entry point:
  `/data/250010109/Research_System/templates/execution/acp_submit_template.sh`

Failure artifacts are retained. No resource fallback, scale reduction, condition
substitution, resubmission, old C/T launcher, or stale checkpoint reuse is allowed.
Smoke PASS is engineering evidence only; full-run submission is not completion.

## 7. Confirmation And Freeze Ledger

| Block | State | Grounding |
|---|---|---|
| A question/claim boundary | CONFIRMED | method-construction scope; scientific result remains unknown |
| B data/provenance | CONFIRMED | inherited frozen manifest and researcher-approved 50B contract |
| C learning task | CONFIRMED | next-token LM plus unsupervised raw-`a_7` reconstruction |
| D architecture | CONFIRMED | researcher selected raw Attention output and rejected side Norm |
| E objective/optimization | CONFIRMED | live reconstruction, detached target/denominator, SAE-only AuxK; inherited optimizer |
| F decision evidence | CONFIRMED | Smoke gates control scale-up; no semantic verdict |
| G execution/reproducibility | CONFIRMED | 4H100 Smoke then PASS-gated 4H100 50B; first-layer variant excluded |

Cross-block consistency: **PASS**. The raw hook, gradient contract, data/optimizer
contract, four-rank batch, Smoke gates, and approved scale-up lead to one
unambiguous engineering decision.

Design frozen and execution approved: 2026-09-16, before the first new submission.

Superseded history: the earlier post-`Norm2` C/T and two/eight-RTX5090 design in
this file's prior revision is retired and must not be executed. Source history
remains in the earlier package and the 05 architecture-confirmation prompt.

## Appendix A — Amendment A01: multi-site plugin engineering Smokes

- Amendment time: 2026-09-16, after the final-layer Smoke and formal submission.
- Before: this Protocol covered only one block-7 raw Attention-output SAE and
  explicitly excluded any additional hook implementation or Smoke.
- After: the researcher authorized implementation and sequential Smoke only for
  (A) independent SAEs at zero-based blocks `3` and `7`, then (B) independent
  SAEs at all eight blocks. Both use `5090-2-spot`; neither may use the reserved
  H100 resource or any retired C/T launcher.
- Reason: test the engineering feasibility of treating SAEs as training-only,
  plug-in observers at multiple raw Attention outputs while preserving the
  native inference path.
- Data visible before amendment: the original final-layer Smoke and partial
  formal-run telemetry were already visible. No data from either amended
  architecture existed.
- Affected blocks: D (architecture), E (multi-layer auxiliary aggregation), and
  G (two-RTX5090 execution).
- Approval: researcher message authorizes both implementations and the two
  sequential Smokes.
- Eligibility impact: the original final-layer run remains governed by the
  frozen body above. The new Smokes are engineering-only and cannot support a
  scientific comparison. Arithmetic mean across hook layers for reconstruction
  and AuxK is an explicit AI engineering assumption for Smoke; long-run/Baka
  submission is blocked until the researcher confirms this choice and the
  intended long-run task and budget.

## Appendix B — Amendment A02: dual-site 8x5090 50B and all-layer Smoke

- Amendment time: 2026-09-16, after the first dual-site two-RTX5090 Smoke job
  completed its training body and exposed one mechanical audit-path failure.
- Before: A01 authorized only two sequential two-RTX5090 Smokes; multi-layer
  loss aggregation and every long run remained blocked.
- After: the researcher confirmed arithmetic-mean aggregation across hook
  layers and authorized the following ordered scope: repair and audit the
  dual-site Smoke receipt without erasing its original failure record; submit
  one fresh dual-site 50B run on one node with eight RTX5090 GPUs; then submit
  the all-eight-layer engineering Smoke on one node with two RTX5090 GPUs.
  The all-eight-layer 50B run remains unauthorized until its Smoke passes and
  the researcher separately asks for that submission.
- Dual-site architecture: independent width-30000 Top-32 SAEs on zero-based
  blocks `3` and `7`, each reading the raw Attention return after `W_O` and
  before residual addition. No side Norm or SAE reconstruction enters the
  native LM path or inference.
- Frozen multi-layer objective for \(m\) hook layers:

  \[L=L_{\mathrm{LM}}+\frac{1}{m}\sum_{\ell}L_{\mathrm{rec}}^{(\ell)}
  +\frac{1}{32m}\sum_{\ell}L_{\mathrm{AuxK}}^{(\ell)}.\]

  Each reconstruction term uses a live hook input with detached target and
  denominator; each AuxK term is SAE-only. Layer averaging keeps the total
  auxiliary-loss scale matched across the two-site and eight-site variants;
  it does not keep each layer's individual coefficient matched.
- Formal dual-site execution: fresh seed-17 initialization; exactly 50B valid
  prediction tokens; fixed DCLM paired view and checkpoint schedule; sequence
  2048; microbatch 2/GPU; eight ranks; accumulation 8; 262,144 effective valid
  targets per complete update; `5090-8-spot`; `shphd-lite-0911` plus the
  registered SM120 runtime layer; 160 GiB run-storage ceiling.
- Required observability: existing aggregate tags plus raw and weighted
  reconstruction/AuxK, SAE sample count, dead-feature count, AuxK activity,
  and SAE gradient norm for every registered hook layer. Cumulative valid
  prediction tokens remain primary; optimizer update remains secondary.
- Scale-up evidence: the original dual-site `smoke_receipt.json` remains
  `FAIL` because the trainer looked for `checks/gradient_contract.json` while
  the launcher correctly wrote `checks/multisite_contract.json`. The latter
  is `PASS`, and every other receipt gate passed. A correction audit may issue
  a separate PASS verification only after checking the immutable receipt,
  contract, TensorBoard audit, checkpoint replay, hook set, and absence of any
  non-audit failure. It may not rewrite the original receipt.
- Eight-layer Smoke: fresh run directory, blocks `0` through `7`, two ranks,
  accumulation 32, eight logical updates, independent-process resume at update
  4, per-layer observability, peak-memory and checkpoint/storage gates. It must
  use the corrected source revision and produce `smoke_verification.json=PASS`.
- Data visible before amendment: all eight dual-site Smoke updates, recovery
  artifacts, losses, resource measurements, and its mechanical gate failure;
  no all-eight-layer GPU Smoke data and no dual-site 8x5090 formal data existed.
- Affected blocks: D (two- and eight-site architecture), E (confirmed layer
  mean and per-layer telemetry), and G (one authorized 8x5090 full run followed
  by one authorized 2x5090 Smoke).
- Approval: researcher message `请改进，然后提交8卡，然后开启8层的smoke`.
- Eligibility impact: the original block-7 run remains governed by the frozen
  body. The dual-site full run is engineering-authorized after the correction
  audit PASS. The eight-layer Smoke remains engineering evidence only. Neither
  submission health nor Smoke establishes semantic improvement, functional
  specialization, or long-run completion.

A02 audit ledger: A--G affected fields **CONFIRMED** for the named execution
scope; cross-block consistency **PASS**. Full execution approval is limited to
the dual-site 50B run. The all-layer full run is explicitly excluded.

## Appendix C — Amendment A03: all-layer Smoke before any 8x5090 discussion

- Amendment time: 2026-09-16, before any A02 eight-RTX5090 formal submission.
- Before: A02 authorized a dual-site 8x5090 50B submission before the all-layer
  two-RTX5090 Smoke.
- After: the researcher explicitly changed the order. The only executable scope
  now is correcting the multi-site implementation and running the all-eight-layer
  Smoke on `5090-2-spot`. No eight-RTX5090 full job may be submitted in this
  stage. After the all-layer Smoke reaches a complete audited PASS, the
  researcher and AI will discuss the eight-card submissions separately.
- Reason: qualify the largest plugin architecture and its observability before
  making the full-run resource and submission decision.
- Data visible before amendment: the dual-site Smoke artifacts and mechanical
  audit failure were visible; no all-layer GPU Smoke or new multi-site 8x5090
  formal run had been submitted.
- Affected block: G execution order and approval scope. Architecture, layer-mean
  objective, data, seed, optimizer, token counting, and Smoke gates are unchanged.
- Approval: researcher message `先改成smoke 8层，完成smoke后再讨论8卡提交事宜`.
- Eligibility impact: A02's 8x5090 authorization is superseded before use. The
  all-layer Smoke is engineering evidence only and cannot itself authorize a
  long run or establish a scientific result.

A03 audit ledger: G **CONFIRMED**; A--F unchanged; cross-block consistency
**PASS** for all-layer Smoke only; 8x5090 full execution is **NOT AUTHORIZED**.

## Appendix D — Amendment A04: Smoke-PASS-gated two-job 8x5090 sequence

- Amendment time: 2026-09-16, before the all-layer Smoke submission and before
  any multi-site 8x5090 formal submission.
- Before: A03 deferred every eight-card submission until a later discussion.
- After: the researcher authorized continuous supervision through completion of
  the all-eight-layer `5090-2-spot` Smoke. Only if its audited verification is
  `PASS`, submit two separate single-node `5090-8-spot` 50B jobs in order:
  first the block-3-plus-block-7 model, then, after the first job has eight
  healthy ranks, finite first-update telemetry, and durable logs, the all-eight-
  layer model. The second job need not wait for the first to finish 50B.
- Each formal job starts fresh from seed 17 and uses its own run directory,
  checkpoints, optimizer, activity buffers, logs, and submission receipt. No
  Smoke or sibling checkpoint may be loaded.
- Both formal jobs use sequence 2048, microbatch 2/GPU, eight ranks,
  accumulation 8, and 262,144 valid prediction tokens per complete update.
  Each targets exactly 50B valid prediction tokens and keeps the frozen data,
  optimizer, token schedules, layer-mean objective, and per-layer telemetry.
- Storage ceilings: 160 GiB for the two-SAE job and 300 GiB for the eight-SAE
  job, derived from observed one-/two-SAE full-state checkpoint sizes and the
  frozen 29-permanent-plus-two-recovery retention plan.
- Failure stop: any incomplete/missing Smoke gate blocks both submissions. A
  failed first formal startup blocks the second submission; no fallback profile,
  resubmission, scale reduction, or old C/T launcher is allowed.
- Data visible before amendment: the dual-site Smoke artifacts and known audit-
  path failure were visible; no all-layer GPU Smoke or multi-site 8x5090 formal
  telemetry existed.
- Affected block: G execution approval and ordered handoff. A--F and the A02
  architecture/objective freeze remain unchanged.
- Approval: researcher message `请监督2卡smoke完成执行，然后顺次提交两个8卡任务，分成两个任务提交`.
- Eligibility impact: both full runs are engineering-authorized only after the
  common all-layer Smoke PASS. Submission and startup health are not scientific
  results and do not establish semantic improvement or long-run completion.

A04 audit ledger: G **CONFIRMED**; A--F unchanged; cross-block consistency
**PASS**; approved execution is exactly one all-layer 2x5090 Smoke followed by
two separate PASS-gated 8x5090 50B submissions in the registered order.

## Appendix E — Amendment A05: submit the second formal job while the first is queued

- Amendment time: 2026-09-16, after the all-layer Smoke verification passed and
  after the dual-site 8x5090 job was accepted but before it acquired a worker.
- Before: A04 required the dual-site job to show eight healthy ranks, finite
  first-update telemetry, and durable logs before submitting the all-layer job.
- After: the researcher explicitly authorized immediate submission of the
  all-layer job. The two jobs remain separate and ordered by submission time,
  but may coexist in the Spot queue. Neither may share a run directory,
  checkpoint, optimizer state, activity buffer, log, or submission receipt.
- Observed state at the amendment: the common all-layer Smoke had an audited
  `PASS`; the dual-site formal job `pt-zzl78jg5` was `STARTING` with zero
  allocated replicas; no formal optimizer update existed.
- Unchanged: both jobs use `5090-8-spot`, eight ranks, fresh seed-17
  initialization, 50B valid prediction tokens, 262,144 valid targets per
  complete update, and the frozen architecture, objective, data, schedules,
  telemetry, and source manifest. No fallback or old C/T launcher is allowed.
- Approval: researcher message `可以直接提交第二个，完成提交以后汇报`.
- Eligibility impact: platform acceptance or queue state is engineering status
  only; it does not establish healthy startup, long-run completion, or any
  scientific result.

A05 audit ledger: G **CONFIRMED**; A--F unchanged; cross-block consistency
**PASS**; the first-startup gate for submitting the second job is superseded.

## Appendix F — Amendment A06: retain queued 5090 jobs and add two 8xH100 Spot jobs

- Amendment time: 2026-09-17, while both A05 8x5090 jobs remained `STARTING`
  with zero allocated replicas and before either wrote a run artifact.
- Before: A05 authorized exactly the two independent `5090-8-spot` formal
  submissions already accepted as `pt-zzl78jg5` and `pt-s4apl31f`.
- After: keep both 5090 jobs untouched and additionally submit two independent
  single-node `h100-8-spot` jobs: one for blocks 3+7 and one for all eight
  blocks. The researcher will coordinate the resulting four queued/running
  jobs and did not authorize stopping any of them in this amendment.
- Every H100 job starts fresh from seed 17 in its own run directory and has its
  own checkpoints, optimizer, activity buffers, TensorBoard events, pod log,
  and submission receipt. It may not resume from a 5090, Smoke, or sibling run.
- Matched contract: sequence 2048, microbatch 2/GPU, eight ranks,
  accumulation 8, exactly 262,144 valid prediction tokens per complete update,
  exactly 50B valid prediction tokens total, and the same frozen data,
  objective, optimizer, schedules, checkpoints, and per-layer telemetry.
- Resource: `h100-8-spot`, `shphd-lite-0911`, one worker node, eight H100 80GB
  GPUs. The H100 path uses the image's native SM90 runtime and must not activate
  the RTX5090 SM120 dependency layer.
- Data visible before amendment: the common all-layer two-RTX5090 Smoke had an
  audited PASS; both formal 5090 jobs were accepted but still had zero worker
  replicas; no formal multi-site optimizer update existed.
- Interpretation boundary: H100 and 5090 executions are duplicate engineering
  realizations of the same two scientific conditions, not four independent
  treatment arms or statistical replicates. If more than one sibling reaches
  training, the researcher must choose the owning trajectory before a result
  comparison; AI must not pool or cherry-pick them.
- Approval: researcher message `把4、8层的模型和8层模型都换成8卡H100 spot, 请帮我直接提交，不用把前两个停止`.

A06 audit ledger: G resource and execution routing **CONFIRMED**; A--F
unchanged; cross-block consistency **PASS**; exactly two additional H100 Spot
submissions are authorized and no existing job stop is authorized.

## Appendix G — Amendment A07: resume the failed H100 trajectories on 8xRTX5090

- Amendment time: 2026-09-17, after both A06 H100 Spot jobs entered terminal
  `FAILED` state without a trainer traceback, non-finite loss, OOM record, or
  graceful process-end record.
- Durable resume points: the block-3-plus-block-7 trajectory resumes only from
  its complete step-15000 recovery checkpoint at 3,931,659,776 valid prediction
  tokens; the all-eight-layer trajectory resumes only from its complete 3B
  milestone checkpoint at 3,000,000,000 valid prediction tokens. Uncheckpointed
  tail updates are discarded and are not part of the resumed evidence chain.
- After: submit two new single-node `5090-8-spot` jobs, one per trajectory,
  loading those checkpoints and preserving the model, optimizer, scheduler,
  activity buffers, RNG state, data cursor, optimizer-step coordinate, token
  coordinate, sequence length, microbatch 2/GPU, accumulation 8, and 262,144
  valid prediction tokens per complete update. The existing failed H100 jobs
  and suspended fresh-start 5090 jobs are not stopped, restarted, or repurposed.
- Runtime-only deviation: the checkpoint's original H100 execution-scope hash
  is retained so the exact training contract remains loadable. This amendment
  and the execution workspace's dated resume record own the authorized hardware
  transition to RTX5090; the old H100 scope text does not authorize a new fresh
  H100 run or conceal the profile change.
- Performance boundary: no microbatch, accumulation, CE chunk, checkpointing,
  logging, objective, optimizer, or schedule change is combined with this
  hardware migration. Memory-filling candidates for 4xH100, 8xH100, and
  8xRTX5090 are calculation-only until separately smoked. In future resource
  changes, GPU memory capacity and the measured model-specific baseline must be
  used to retune microbatch rather than copying the old hardware configuration.
- Approval: researcher message beginning `请现在检查一下训练情况` explicitly
  requests the two 8xRTX5090 continuation submissions and the retained resource
  calculations.
- Eligibility impact: a successful resume establishes operational continuity,
  not bitwise hardware equivalence or a scientific result. The hardware switch
  and discarded uncheckpointed tails must remain visible in the final evidence
  record.

A07 audit ledger: G execution routing and recovery point **CONFIRMED**; A--F
unchanged; cross-block consistency **PASS** for exact-contract 8xRTX5090 resume.

## Appendix H — Amendment A08: per-hook reconstruction coefficient 0.1 and optimized reruns

- Amendment time: 2026-09-17, after inspecting the active final-layer H100 run
  and while the earlier dual/all-layer trajectories remained separate records.
- Objective: reconstruction losses remain arithmetically averaged across SAE
  hooks. Set the coefficient multiplying that mean to `0.1 * N_hooks`, giving
  total coefficients 0.1, 0.2, and 0.8 for one, two, and eight hooks. Thus each
  hook's own reconstruction term has direct coefficient 0.1 before downstream
  path overlap. AuxK losses remain layer-mean aggregated with one total
  coefficient 1/32; their encoder input and main-reconstruction residual stay
  detached so AuxK updates SAE parameters only. No layer-sum aggregation is
  introduced.
- Final-layer continuation: stop old job `pt-xs9xol7b`. Its durable parent is
  the complete step-59000 checkpoint at 15,465,567,744 valid prediction tokens;
  discard the later uncheckpointed tail. After one 4xH100 Reserved capacity and
  recovery Smoke passes, fork a new training phase on `h100-4-reserved` with
  reconstruction coefficient 0.1, microbatch 16/GPU, accumulation 2, sequence
  2048, four ranks, and unchanged 262,144 valid prediction tokens per complete
  optimizer update. Preserve model, optimizer, scheduler, RNG, data cursor,
  SAE activity, token schedules, and 50B endpoint. This is a recorded objective
  and microbatch-partition change, not an exact-contract or bitwise resume.
- Dual/all-layer reruns: start two new seed-17 trajectories rather than loading
  the earlier unit-weight checkpoints. First run one matching `5090-2-spot`
  Smoke for each condition. The dual-site Smoke uses microbatch 4 and
  accumulation 16; the all-layer Smoke uses microbatch 2 and accumulation 32.
  Both keep sequence 2048 and 262,144 tokens/update. Each formal submission is
  gated by its own audited Smoke PASS.
- Formal resources: submit two separate single-node `5090-8-spot` jobs. The
  dual-site run uses microbatch 4/GPU and accumulation 4 with total
  reconstruction coefficient 0.2. The all-layer run uses microbatch 2/GPU and
  accumulation 8 with total reconstruction coefficient 0.8. Both retain
  262,144 tokens/update, CE checkpointing, fixed data/order, optimizer and
  token-based schedules. CE chunk size is 256 for the new performance configs.
- Capacity policy: perform only the one registered candidate Smoke per
  condition. Do not run a batch-size grid. A Smoke failure blocks only its
  matching formal submission and must not trigger an unapproved resource or
  objective fallback.
- Supervision: after each formal submission, inspect for at most five minutes.
  If it has not entered active execution by then, stop polling but leave the
  platform task scheduled. Do not stop a queued task merely because the
  supervision window ended.
- Existing jobs: this amendment authorizes stopping only `pt-xs9xol7b`. It
  does not stop, rewrite, or reuse any earlier dual/all-layer H100 or RTX5090
  job or run directory.
- Approval: researcher message beginning `现在需要有条理地做完以下几件事情`.
- Evidence boundary: Smoke and runtime health are engineering evidence. The
  coefficient correction does not itself establish semantic improvement,
  better validation loss, or a causal architecture advantage.

A08 audit ledger: objective, gradient ownership, batch arithmetic, fork
boundary, resources, Smoke gates, and supervision window **CONFIRMED**;
cross-block consistency **PASS** for the three named new execution lineages.

## Appendix I — Amendment A09: four-H100 continuation Smoke for the existing all-layer trajectory

- Amendment time: 2026-09-18, while the existing all-eight-layer continuation
  `pt-leyy9ey3` was healthy on `5090-8-spot` and the final-layer continuation
  `pt-2f2s6omm` had passed 21B valid prediction tokens on
  `h100-4-reserved`.
- Before: A07 kept the all-layer trajectory on eight RTX5090 ranks with
  microbatch 2 and accumulation 8. A08 did not authorize stopping or reusing
  that trajectory or the active four-H100 final-layer allocation.
- After: pause only `pt-2f2s6omm`, preserving its latest complete recovery
  checkpoint. Keep `pt-leyy9ey3` running and unmodified. Use the released
  single-node `h100-4-reserved` allocation for one bounded engineering Smoke
  that forks from the complete all-layer step-34000 checkpoint at
  8,912,237,056 valid prediction tokens.
- Smoke topology and batch: four physical H100 ranks, microbatch 16/GPU,
  accumulation 2, sequence length 2048, and exactly 262,144 valid prediction
  tokens per optimizer update. Eight frozen logical reference lanes must map
  onto the four physical ranks so the source sampler cursor and per-lane SAE
  sampling RNG continue from the eight-rank checkpoint. The candidate is
  `mbs16/acc2` only; this amendment authorizes no batch-size grid or fallback.
- Held fixed: the existing all-layer model and eight Attention-output hooks,
  unit total reconstruction coefficient 1.0, layer-mean reduction, AuxK
  coefficient 1/32 with no backbone gradient, optimizer and scheduler state,
  seed 17, frozen DCLM view, 50B endpoint, token schedules, and cumulative
  token/update coordinates. This Smoke does not convert the trajectory to the
  later 0.8 reconstruction-weight contract.
- Smoke PASS requires: complete source-manifest validation; strict model,
  optimizer, scheduler, step, and token restoration; exact 262,144 valid
  tokens/update; the registered eight-lane sample-index and SAE-mask
  continuation; finite losses and gradients; four synchronized replicas;
  peak memory below the physical 80 GiB limit; a complete four-rank recovery
  checkpoint; and a durable `smoke_verification.json` reporting measured
  throughput and memory. Performance is measured but has no predeclared PASS
  threshold.
- Stop rule: any OOM, non-finite value, coordinate discontinuity, source
  mismatch, sample/RNG mismatch, missing artifact, or incomplete checkpoint is
  `FAIL` and stops this candidate. Do not stop `pt-leyy9ey3` and do not submit
  a four-H100 Full run under this amendment.
- Data visible before amendment: both 5090 and historical H100 throughput,
  loss, checkpoint, and memory telemetry were visible. The Smoke is therefore
  an engineering migration qualification, not an untouched scientific
  comparison or statistical replicate.
- Approval: researcher message `请先暂停当前的 4×H100 单层任务，然后在这上面进行 smoke，先不用停八卡 5090`.
- Eligibility impact: a PASS can establish constructible continuation and
  measured candidate throughput only. It cannot establish bitwise hardware
  equivalence, model-quality improvement, or authorization for the formal
  migration.

A09 audit ledger: A--F unchanged; G execution routing, source checkpoint,
batch arithmetic, Smoke gates, artifact contract, and stop boundary
**CONFIRMED**; cross-block consistency **PASS**; execution scope
**APPROVED_FOR_ONE_4xH100_RESERVED_SMOKE_ONLY**.

## Appendix J — Amendment A10: migrate the suspended all-layer trajectory to 4xH100 Reserved

- Amendment time: 2026-09-18, after the A09 migration Smoke passed and after
  administrator action suspended `pt-leyy9ey3`.
- Source boundary: resume from the newest complete source checkpoint, step
  35000 at 9,174,381,056 valid prediction tokens. Discard the later
  uncheckpointed tail through step 35054.
- Resource and topology: one `h100-4-reserved` node, four physical H100 ranks,
  microbatch 16/GPU, accumulation 2, and eight preserved logical source lanes.
  Each complete update remains 262,144 valid prediction tokens.
- Held fixed: all eight Attention-output SAE hooks, unit total reconstruction
  coefficient 1.0 with layer-mean reduction, AuxK coefficient 1/32, detached
  AuxK backbone boundary, model/optimizer/scheduler state, seed, frozen data
  order, token schedules, checkpoint targets, and 50B endpoint.
- Qualification: A09 Smoke `pt-476ixasa` is `PASS`, including exact coordinate,
  eight-lane sampler/SAE-RNG continuation, finite losses, synchronized replicas,
  complete four-rank checkpointing, and 51.5GB peak reserved memory below the
  80GB physical limit.
- Interpretation: this replaces the runtime continuation of the suspended
  8xRTX5090 job; it is not a new model arm or evidence of bitwise hardware
  equivalence. The measured throughput is approximately equal, so the reason
  for migration is Reserved-resource stability rather than an expected speedup.
- Approval: researcher request `pt-leyy9ey3 被管理员停止了，请提交4卡H100 reserved的资源，开始训练`.

A10 audit ledger: A--F unchanged; G source checkpoint, four-rank topology,
logical-lane continuity, batch arithmetic, profile, and 50B continuation scope
**CONFIRMED**; cross-block consistency **PASS**; execution scope
**APPROVED_FOR_4xH100_RESERVED_FORMAL_CONTINUATION**.

## Appendix K — Amendment A11: fresh S7 lambda-0.1 trajectory moved to 4xH100 Reserved

- Amendment time: 2026-09-20, after a separate fresh-start S7 lambda-0.1
  two-RTX5090 Smoke passed and after its eight-RTX5090 Spot full job
  `pt-bbrhajht` was accepted but had not emitted a formal training metric.
- Before: the fresh seed-17 trajectory was configured for eight RTX5090 ranks,
  microbatch 8/GPU, accumulation 2, and 262,144 valid prediction tokens per
  update. The researcher owns stopping `pt-bbrhajht`; this amendment does not
  authorize the AI to stop, resume, or reuse it.
- After: create a separate fresh run on one `h100-4-reserved` node. Preserve the
  block-7 raw Attention-output sidecar architecture, no side Norm, native LM
  path, objective `L_LM + 0.1 L_rec + (1/32) L_AuxK`, gradient boundaries,
  seed 17, data/tokenizer/manifest, optimizer, learning-rate schedules,
  `ce_chunk_tokens=128`, CE checkpointing, 50B endpoint, checkpoint schedule,
  loss normalization, and observability contract. Loading the RTX5090 Smoke,
  `pt-bbrhajht`, the 15.466B checkpoint, or any other checkpoint is forbidden.
- Batch and capacity candidate: four ranks, sequence length 2048, microbatch
  32/GPU, accumulation 1. This keeps 128 sequences and 262,144 nominal valid
  prediction tokens per complete update. It is the largest integer microbatch
  factorization that preserves the frozen global batch on four ranks.
- Qualification: because microbatch 32 is a new performance configuration, run
  one bounded eight-update capacity Smoke on `h100-4-reserved`, with intentional
  stop/recovery after update 4. It must pass the existing hook, gradient,
  fresh-start, finite-loss, token-count, synchronization, TensorBoard,
  checkpoint-replay, storage, and physical-memory gates. OOM or any missing
  gate blocks scale-up; no batch-size grid or silent CE/optimizer change is
  authorized.
- Scale-up: only after the matching Smoke writes audited
  `smoke_verification.json=PASS`, submit one independent 50B full job on the
  same `h100-4-reserved` profile. Observe only submission and bounded startup;
  do not resubmit because it queues.
- Reason: the researcher replaced the eight-RTX5090 Spot execution with the
  stable four-H100 Reserved resource and requested the largest safe microbatch
  compatible with the fixed global batch. Existing 4xH100 evidence at
  microbatch 16/accumulation 2 measured about 33.87 GB reserved per rank, but it
  does not qualify the untested microbatch-32 setting.
- Eligibility impact: this is a separate engineering realization of the same
  fresh S7 lambda-0.1 condition, not a second treatment arm or statistical
  replicate. Smoke and submission health cannot establish model quality,
  semantic improvement, or 50B completion.
- Approval: researcher message `我认为还是不要使用8 * 5090了, 换成4 * H100
  reserved ... 如果需要 smoke 的话，直接使用 4 卡 H100 reserved`.

A11 audit ledger: A--F unchanged; G resource profile, topology, fresh-run
lineage, batch partition, capacity Smoke, scale-up gate, and stop ownership
**CONFIRMED**; cross-block consistency **PASS**; execution scope
**APPROVED_FOR_ONE_4xH100_RESERVED_CAPACITY_SMOKE_THEN_ONE_PASS_GATED_FRESH_50B_RUN**.

## Appendix L — Amendment A12: repair pre-training H100 topology guard and repeat Smoke

- Amendment time: 2026-09-20, after A11's first H100 Smoke submission
  `pt-2i57hchd` reached four-GPU preflight but failed before its first
  optimizer update. The isolated trainer still required the prior RTX5090
  profile despite the A11 H100 config and launcher.
- Before: the intended four-rank `mbs32/acc1` capacity test did not run. The
  failed job and `runs/smoke_S7_lambda0p1_from_scratch_4h100_mbs32` retain
  their logs and failure artifacts; they are not a capacity result.
- After: change only the isolated trainer topology guard to require four H100
  ranks on `h100-4-reserved` and the already approved `mbs32/acc1` partition.
  Keep all architecture, objective, data, optimizer, CE, schedule, token,
  and fresh-initialization settings unchanged. Submit one corrected Smoke into
  a new `_v2` run directory; it may gate the full run only if its own durable
  verification is `PASS`.
- Reason: align the safety guard with A11's authorized execution tuple without
  using or deleting a failed training artifact. The researcher explicitly
  asked to continue Smoke and submit after completion.
- Eligibility impact: A11's scientific condition and comparison boundary are
  unchanged. The first job is an engineering setup failure, not an OOM or
  training result. No full run is authorized from that failed attempt.

A12 audit ledger: A--F unchanged; G guard repair and clean repeat Smoke
**CONFIRMED**; cross-block consistency **PASS**; corrected Smoke then one
PASS-gated independent 4xH100 Reserved full run remains the approved scope.
