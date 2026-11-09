# Protocol: A15_13_E20 Last-Layer SAE Flat-Router Eight-Task Mixed Training

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN_IF_QUALIFIED
Approval status: researcher confirmed the five-condition plan on 2026-09-07
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: v2 implementation, data/leakage audit, tests, qualification, smoke, and conditional full run plus evaluation
Design frozen at / registered revision: 2026-09-07T15:38:26Z; plan SHA256 ef1ab981ad7b065e1f66d29f4a5e2cbb80afb4c2aa31f9c1270f60e9242a4bab
Purpose: test whether a frozen final-layer SAE partition produces useful flat expert routing
Primary Anchor: A15_13_10_sae_flat_router_functional_anchor.md
Anchor decision question: does SAE routing beat matched random grouping and task-only routing on paired answer-token loss?
Anchor physical prior tested: recurring SAE co-activation identifies contexts that can support different low-rank updates
Anchor core model term tested: the frozen eight-way teacher and causal linear Router
Anchor falsifier: no stable SAE advantage over frequency-matched random grouping
Experiment role: method construction with functional falsification
Primary metric from Anchor: per-seed paired internal-test answer-token NLL difference and 95 percent source-stratified record-bootstrap interval
Claim boundary from Anchor: one model, one final layer, eight experts, internal split only
Minimal setup: frozen Qwen3-0.6B-Base plus final-layer adapters
Treatment and controls: SAE; random SAE features; prompt-only diagonal GMM; task-only Router; dense rank-16 adapter
Changed variable: expert-routing teacher or removal of routing
Held fixed: data, sample order, seeds, layer, active adapter rank, optimizer family, update count, evaluator, and fixed final checkpoint
Conditions to run: five conditions x seeds 17/29/43 x 512 updates
Pass: SAE beats random and task-only in all seeds with intervals strictly above zero
Fail: SAE has a nonpositive random-control contrast in any seed
Insufficient: sign reversal, interval crossing zero, invalid control, leakage, missing evaluator, or incomplete artifact
Cannot claim: official benchmark performance, semantic truth, optimal layer/expert count, or deployment value
Approval decision: run automatically after all qualification gates pass; otherwise stop without redesign
```

## 1. Terminology / Definitions

An answer-token NLL is cross entropy summed over gold-answer tokens and divided
by their count. `SAE` is the frozen 30,000-feature Top-32 sparse autoencoder.
`GMM` is the approved prompt-only PCA-64 hierarchical diagonal Gaussian mixture.
An internal held-out score uses the repository's post-deduplication split and is
not an official or uncontaminated benchmark score. A frozen Router retains fixed
parameters during expert training, although its output can vary by token state.

## 2. Anchor Alignment

This Protocol implements the Anchor's one-layer functional falsifier. It does
not revisit earlier SAE training, hierarchy claims, layer selection, or GMM
results. It reuses only the verified SAE and the GMM algorithm family.

## 3. Tested Hypothesis

The SAE condition will reduce answer-token NLL relative to the frequency-matched
random-feature condition and task-only Router in every seed, with each paired
95 percent interval excluding zero in the favorable direction.

## 4. Rival Explanations

The random-feature condition tests whether any equally sized SAE grouping is
sufficient. Task-only tests generic learned routing. Dense rank 16 tests active
adapter capacity without routing. Prompt-only GMM tests whether an older offline
partition family performs similarly; it is not an isolated clustering-method
control. Source/length diagnostics test shortcut explanations, and selection
intervention tests whether SAE/GMM outcomes depend on the selected expert.

## 5. Data Construction And Provenance

The immutable source is `/data/250010109/datasets/a15_e14_p3_clean/processed.pt`,
registered SHA-256 `b2e1b4c5d43599c2d48736955a1532a8bd1b2a69787a4fed6da37cfaf793ac13`.
It contains train/development/internal-test counts 39,576/8,481/8,481 from MMLU,
MMLU-Pro, BBH, GSM8K, MATH, GPQA, HumanEval, and MBPP. Sequences are right padded
to 512 with explicit `attention_mask` and answer-only `labels`.

Before model use, reconstruct source-aware prompt identity from `record_id` and
audit normalized question-only duplicates, cross-source same-question different-
answer conflicts, and identical attention-masked token sequences after truncation.
Across-split conflicts retain test over development over train and are written to
a new derived dataset plus exclusion ledger; the source file is never overwritten.
Near-duplicate uncertainty is reported rather than silently claimed absent.

Within each source, sort training records by
`sha256("20260907|" + record_id)`. The first `floor(n/2)` records are discovery
and the remainder Router-fit. Discovery and Router-fit never use development or
test. Expert training uses the complete audited train split. Development selects
Router regularization; internal test remains sealed until update 512 is frozen.

## 6. Learning Task And Permitted Supervision

The model receives prompt plus causal answer prefix and predicts the next answer
token. Gold labels contribute only to answer-token NLL and to the Boolean mask
identifying which state predicts an answer. Source identity and task labels never
enter SAE/GMM fitting, routing targets, model inputs, or gradients. Generation
receives the reconstructed prompt only, never concatenated gold answers.

For Router fitting, a valid state satisfies current-position attention and
`labels[t+1] != -100`. SAE targets use same-position activations `a_t`; using
`a[t+1]` is forbidden. GMM labels use prompt-position states only and are fixed
before Router-fit records are labeled.

## 7. Model / Architecture And Frozen Variants

All conditions use Qwen3-0.6B-Base and zero-indexed layer 27 only. The Router
reads the 1,024-dimensional state passed into `model.layers[27].mlp`; adapters
modify the 3,072-to-1,024 `down_proj`. Routed conditions contain one shared
rank-eight adapter plus eight independent rank-eight experts, select one expert,
and multiply it by the native selected softmax probability. `dense_r16` contains
one rank-16 adapter and no Router. All adapter scales are 1/8; A matrices share
the same initialization family and B matrices start at zero.

The base model, language head, SAE, feature groups, PCA, GMM, and frozen Router
parameters never update. `sae`, `random_features`, and `gmm` train only shared
and expert adapters. `task_only` additionally trains its linear Router.
`dense_r16` trains only the dense adapter.

## 8. Training Objective And Optimization

The offline Router minimizes

\[
\frac{\sum_t m_tD_{KL}(q_t\Vert p_t)}{\sum_t m_t}
+\frac{\lambda_W}{2}\lVert W\rVert_F^2.
\]

Adam uses learning rate 0.001 and weight decay zero; only \(W\) receives explicit
regularization. Sweep \(\lambda_W\in\{0,10^{-5},10^{-4},10^{-3}\}\) with identical
initialization and order, at most 20 epochs, 4,096 valid positions per batch, and
early stopping after three development-KL non-improvements. Test is forbidden.

Expert training uses total answer cross entropy divided by all answer tokens in
the complete effective batch. Microbatch is 8, accumulation 16, and effective
batch 128 records. Every condition runs 512 optimizer updates. Adapters use
AdamW learning rate `2e-4`, weight decay `0.01`; task-only Router uses `5e-4`,
weight decay zero. Warmup is 26 updates, followed by cosine decay, with gradient
clipping 1.0. No online semantic regularizer is added.

## 9. Conditions, Seeds, And Checkpoints

The five conditions are `sae`, `random_features`, `gmm`, `task_only`, and
`dense_r16`; seeds are 17, 29, and 43. All 15 condition-seed runs use the same
seed-indexed sample schedule. Save initialized update 0 and updates 128, 256,
384, and 512; save atomic recovery state every 32 updates. The scientific
checkpoint is always update 512.

## 10. Primary Metric And Frozen Analysis Plan

For each seed and condition, internal-test answer-token NLL is computed per
record with its answer-token count. Every one of the ten condition pairs is
reported separately in each seed. The primary deltas are `random minus SAE` and
`task-only minus SAE`; positive favors SAE. Use 2,000 bootstrap draws, sampling
records with replacement within source, NumPy seed 20260907. Training seeds are
never pooled. Missing or nonfinite records are not imputed.

`FULL_METHOD_ADVANTAGE` requires both primary point estimates and both complete
95 percent intervals to be strictly positive in every seed. `STRUCTURE_ONLY`
requires the random contrast in all seeds but not the task-only contrast.
`NO_STABLE_STRUCTURE_GAIN` applies when a random-control point estimate is
nonpositive. Any seed reversal, interval containing zero, invalid comparison,
or missing evidence is `INSUFFICIENT`. No multiplicity-adjusted discovery claim
is made from the secondary pairwise matrix.

## 11. Secondary Metrics And Guards

Evaluate validation NLL at all five checkpoints and report update, cumulative
actual answer tokens, and elapsed training time. At update 512 report per-source
and overall test NLL. Generate greedily with at most 512 new tokens for every
internal-test record and score source-appropriate accuracy/exact-match/final-
answer/pass@1. Report every task denominator and interval; compute the arithmetic
eight-task macro average only when all evaluators are valid.

For SAE and GMM only, shuffle selected experts across records within each valid
answer-prediction position while preserving native coefficients and expert
counts; report actual changed fraction and paired NLL effect. For every routed
condition report singular values and pairwise absolute Frobenius cosine of
`scale * B_k A_k`; zero pairs are undefined. Route agreement, group stability,
and matrix similarity are diagnostics and never substitute for NLL or task gain.

## 12. Known Good / Known Bad / Known Confusing Cases

Known-good evaluator cases include correct multiple-choice letters, normalized
math final answers, BBH exact/task-specific matches, and terminating passing
HumanEval/MBPP programs. Known-bad cases include wrong letters, wrong numeric
answers, malformed code, timeout, and sandbox escape attempts. A low expert
cosine or high route/source agreement is a confusing case: it may accompany a
result but cannot establish functional benefit.

## 13. Scientific Procedure And Stage Contracts

1. Data audit produces an immutable derived-data manifest or stops on unresolved
   identity/leakage failure.
2. Cache construction passes attention masks, stores answer-state masks and
   record/segment provenance, and excludes padding.
3. SAE spectral grouping, random control, and prompt-only GMM are fit on
   discovery records. SAE audit uses five clustering seeds, 20 record bootstrap
   resamples, and 20 degree-preserving null graphs. GMM uses seed 17029, PCA-64,
   three diagonal parent components, 3/3/2 child components assigned by parent
   size, 20 deterministic restarts per mixture, at most 100 EM iterations, and
   covariance floor `1e-6`; 20 record bootstrap fits audit stability.
4. Three frozen-teacher Routers per training seed are selected on development.
   Collapse, no improvement over the corresponding fixed-frequency/shuffled
   baseline, nonfinite targets, or missing groups stops for researcher review.
5. Full unit/integration tests and five one-update real-GPU smoke conditions
   must prove mask alignment, finite gradients, base freeze, recovery identity,
   and evaluator/sandbox readiness.
6. Only after stages 1-5 pass, freeze hashes and submit all 15 runs. Training,
   checkpoint evaluation, final NLL, generation, intervention, geometry, and
   paired analysis then execute sequentially in one fail-closed pipeline.

Each stage writes success or failure JSON. A later stage refuses to run without
the exact predecessor receipt; a failed qualification never launches training.

## 14. Algorithm, Output, And Provenance Contract

Execution root is `/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate`.
Formal runs use `runs/full-<UTC stamp>/`; smoke uses `runs/smoke-<UTC stamp>/`.
Record source hashes, model/SAE hashes, derived-data hash, group/GMM/Router hashes,
code tree hash, environment and image identity, commands, update/token ledgers,
checkpoint hashes, evaluator identities, failures, and an artifact manifest.

The orchestrator may combine all stages in one script, but it must validate
stage receipts between them. Formal ACP uses one `n6ls.iu.i40.4` node, four H100
GPUs, four independent one-GPU workers, reserved quota, normal priority, zero
automatic retries, 12-hour wall ceiling, 48 H100-hour ceiling, and at most 100 GB
of new artifacts. Preserve inherited runtime paths when prepending the project
root. No Git commit, push, publication, historical-experiment edit, subagent, or
automatic resource fallback is authorized.

## 15. Success / Failure / Insufficient Evidence

Engineering qualification requires every data, mask, clustering, Router,
freeze, recovery, evaluator, and sandbox guard to pass. A hard failure stops
without scale-up. An obvious collapse or failure to beat the registered offline
null stops for researcher review without inventing a threshold or changing the
algorithm. Scientific Success/Failure/Insufficient follows Section 10 only
after all required update-512 artifacts exist.

## 16. What This Cannot Claim

The experiment cannot claim official benchmark performance, contamination-free
generalization, replication of a senior result, semantic truth of any group,
optimal layer or expert count, dynamic-expert value, deployment benefit, or
functional gain from route consistency or parameter similarity alone.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
|---|---|---|
| A Question and boundary | CONFIRMED | researcher approved the five-condition plan on 2026-09-07 |
| B Data and provenance | CONFIRMED | approved v2 plan and verified processed-data identity |
| C Task and supervision | CONFIRMED | approved answer-only causal-position contract and GMM no-answer adaptation |
| D Architecture | CONFIRMED | approved final-layer five-condition matrix |
| E Objective and optimization | CONFIRMED | approved 512-update and Router-fit contracts |
| F Comparison and evidence | CONFIRMED | approved paired NLL, internal scores, SAE/GMM intervention, and claim boundary |
| G Execution and reproducibility | CONFIRMED | approved smoke-gated full run and 4xH100 reserved ceiling |

Cross-block consistency audit: PASS. Implementation, smoke, and qualification-
gated full execution were explicitly approved on 2026-09-07. The scientific
body is frozen before implementation. Any outcome-changing change after this
point requires an append-only amendment and an eligibility decision.

## 18. Execution Ledger

### 2026-09-07 qualification attempt

Run root:
`/data/250010109/MoE_Router/experiments/20260907_sae_flat_router_candidate/runs/full-20260907T164318Z`.

The source/data audit and discovery, Router-fit, and development caches passed.
The registered GMM parent fit converged with sizes `[5724, 13697, 363]`. Its
3/3/2 child fits occupied `[1237, 2753, 1734]`, `[7182, 3729, 2786]`, and
`[363, 0]`. The last child therefore collapsed, leaving only seven occupied
leaves. Section 15's qualification rule stopped execution before Router fitting,
five-condition smoke, or formal submission. The execution state is
`QUALIFICATION_FAILED_GMM_CHILD_COLLAPSE`; no scientific verdict exists.

This ledger entry records execution and does not amend the frozen design. Any
collapse-handling change requires a later researcher-approved amendment.

### Amendment E20-A1: direct eight-component GMM

```text
amendment id: E20-A1-FLAT-GMM
recorded at: 2026-09-07T17:15:58Z
before: PCA-64 -> 3-component diagonal parent GMM -> 3/3/2 diagonal child GMMs -> eight leaves
after: PCA-64 -> one flat 8-component diagonal GMM -> eight groups
unchanged: prompt-only discovery-record means, PCA dimension, seed 17029, n_init 20, max_iter 100, reg_covar 1e-6, condition matrix, all Router/training/analysis rules, and claim boundary
reason: the researcher clarified that GMM has no parents and must directly output eight groups aligned in count with SAE; the prior hierarchical construction was not the intended control
visible before amendment: passed data/cache audits and the hierarchical-GMM collapse diagnostic; no Router, smoke, checkpoint, task evaluation, intervention, or functional comparison
affected blocks: D architecture and G execution provenance for the GMM control; the scientific comparison and verdict rules are unchanged
approval: researcher explicitly required the parent-free eight-group GMM and continuation through full submission on 2026-09-07
execution scope: the prior approval for qualification, five-arm smoke, and qualification-gated full execution remains active for this amended construction
```

Eligibility is deliberately asymmetric. The prior hierarchical GMM fit and any
artifact derived from it are ineligible for the amended comparison; its failure
diagnostic remains eligible only as an engineering record of the first attempt.
The audited derivative and the discovery, Router-fit, and development activation
caches may be reused only after their receipts, complete internal file hashes,
and exact manifest hashes are revalidated. Their decision-bearing inputs were
fixed before GMM construction and the amendment does not change data, model,
SAE, layer, masking, prompt means, or split membership. The recovery pipeline
must write a machine-readable amendment receipt containing those exact hashes
before constructing any new group or Router artifact.

This amendment is the only authority to depart from the registered hierarchical
GMM. It does not authorize a fallback if the flat eight-component fit collapses,
a change to component count or initialization, removal of the GMM condition, or
any redesign after another failed gate. The amended run remains fail-closed.

### Amendment E20-A2: minimum pre-submission audit

```text
amendment id: E20-A2-MINIMAL-AUDIT
recorded at: 2026-09-08T01:04:00Z
before: finish all 20 grouping bootstrap, flat-GMM bootstrap, and fixed-margin-null repetitions before Router fitting and submission
after: retain the existing five initialization checks and 14 completed repetitions per diagnostic; the six outstanding repetitions are deferred and do not block training
reason: researcher explicitly requested fewer cumbersome audits and earliest qualified full submission on 2026-09-08
visible before amendment: data/cache receipts, eight-group construction, and partial discovery/development diagnostics; no fitted Router, training smoke, or functional result
affected blocks: G pre-submission sequencing and completeness of secondary grouping diagnostics
unchanged hard gates: exact data/cache/group provenance; answer-only causal mask and frozen base tests; nine Router fits with all eight hard selections occupied and positive development KL gain over a fixed prior; all five one-update training smokes
unchanged scientific contract: five arms, seeds 17/29/43, 512 updates, data split, model, objectives, final checkpoint, primary metric and verdict, test seal, 4xH100 reserved single-node resource scope
approval: explicit researcher direction to simplify remaining audits and continue through full submission; no additional execution scope is inferred
eligibility: existing partial diagnostics remain descriptive only; neither full 20-repeat stability nor null mixing is established. Primary functional evidence remains eligible under unchanged training and evaluation rules if all retained hard gates pass.
```

Preserve the original partial audit unchanged. Write a separate E20-A2 receipt
identifying its hash, completed/deferred scope, exact data/group identities, and
this amendment. No observed failure may be hidden or waived. A failing retained
Router or smoke gate still stops formal submission without an automatic redesign.

Implementation clarification for E20-A2 (2026-09-08): each one-update smoke
checks its initial evaluation forward pass on the first eight development
records, then performs the unchanged 128-record effective training update.
It does not traverse all development records before a one-update smoke.
Formal update-zero and scheduled development evaluations remain full-split;
no selection, training, or final metric is changed by this smoke-only scope.

### 2026-09-08 qualified formal submission

All retained E20-A1/A2 qualification and five-condition smoke gates passed.
Formal ACP job `pt-b32i9y4r` was created at `2026-09-08T01:22:38Z` on the
approved single-node 4xH100 reserved resource. This is an execution receipt, not
a change to the frozen training or verdict contract. Current operational
evidence and limitations are in [Detailed section 9](detailed.md#9-full-submission-after-retained-gates-passed).

Execution correction: the first job failed before training on a `torchrun`
argument ambiguity. After a regression-tested argument separator correction,
the same qualified inputs and resource scope were resubmitted as `pt-zkpfj2zm`
at `2026-09-08T01:25:04Z`. No scientific configuration or qualified artifact
changed. The preserved failure and replacement receipts are in Detailed.

### Amendment E20-A3: cancel remaining repeated grouping audits

```text
amendment id: E20-A3-CANCEL-REPEATED-AUDITS
recorded date: 2026-09-08
before: E20-A2 deferred six remaining SAE record-bootstrap fits, six flat-GMM record-bootstrap fits, and six fixed-margin randomized-graph diagnostics
after: all 18 outstanding repetitions are CANCELLED for this experiment, not postponed; no later catch-up execution is required
approval: researcher explicitly instructed "删除重复审计" on 2026-09-08
reason: remove secondary repeated grouping diagnostics from this functional-training experiment's remaining scope
visible at cancellation: completed offline Routers and smokes; four update-512 training checkpoints and development curves; failed intervention evaluation; no complete internal-test comparison or generation result
affected scope: secondary grouping-audit completion only
unchanged: all five training conditions, three seeds, 512 updates, data and supervision guards, final paired-loss uncertainty calculation, generation evaluation, and expert-selection intervention
eligibility: completed five initialization checks and 14 repetitions per diagnostic remain descriptive evidence. Full 20-repeat stability and null mixing are not established. No primary functional criterion changes.
```

This amendment supersedes E20-A2's deferred-work obligation, not its immutable
historical receipt. Preserve completed audit files and frozen training identities;
do not change hashed configuration merely to erase a completed run's provenance.
The submitted formal worker does not execute grouping audits, so no active job
or audit process needs stopping to apply this cancellation.

### Engineering amendment E20-A4: exact-checkpoint evaluation repair and resume

The researcher explicitly approved repairing intervention evaluation, regression
tests, preserving the four completed checkpoints, and resuming evaluation plus
the remaining eleven conditions on 2026-09-08. The unchanged single-node
4xH100 reserved full scope is authorized. After submission, inspect at ten-minute
intervals, remain quiet on normal progress, and write result records after
complete eligible evidence exists.

Replace the unsupported nonzero-index call in intervention and source-specific
generation with the supported equivalent. Preserve the exact seeded
within-position permutation, native coefficients, valid-position mask, targets,
generation limits, optimization, and comparison rules. Add regression coverage
of the actual evaluation/generation paths and exact legacy-checkpoint reuse.
The auxiliary Router cache recognizes atomic file replacement by inode; all
offline Routers are already frozen and are neither refitted nor modified.

Reuse is allowed only for the four authenticated update-512 checkpoint files
listed in the E20-A4 receipt, with matching data/model/Router identities and the
exact registered repaired source identity. Preserve their original training
identities in evaluation records; record current evaluation identity separately.
Pairwise comparisons use the common repaired evaluation implementation, not a
fictional rewriting of old checkpoint provenance. Verify the training function
and model/optimizer logic remain unchanged. Preserve failed/incomplete artifacts
before rerunning an evaluation. Do not overwrite the four completed conditions.

Existing development curves and the runtime exception were visible before this
repair. No complete test/generation verdict was visible. This engineering
correction does not alter the hypothesis, primary metric, confidence intervals,
training scope, or E20-A3 audit cancellation. Partial pre-repair evaluation files
are ineligible; authenticated completed training checkpoints remain eligible.

### Amendment E20-A5: new h-input balanced-selection run — capacity blocked

```text
recorded_at: 2026-09-08T09:29:49Z
amendment_status: DRAFT_NOT_EXECUTABLE_CAPACITY_CONFLICT
authorization: researcher explicitly authorized in-scope code changes, necessary smoke tests and a new full training submission after all gates pass
authorization_exclusions: do not overwrite E20; no commit/push; no silent scientific redesign
current_execution_gate: BLOCKED by incompatible dense dimensions/parameter target and unresolved shared-branch contract
scientific_body_of_E20_A1_A4: unchanged
affected_blocks: D architecture, E selection dynamics, F capacity/evaluation controls, G reproducibility
prior_results_visible: completed E20 training, internal-test NLL, generation results and routing diagnostics were already inspected before this amendment
new_run_id: NOT_CREATED
new_job_id: NOT_SUBMITTED
```

This is a prospective new run, not a repair, continuation or retrospective
relabeling of old E20. Preserve the old execution source, configurations,
checkpoints, model hashes, datasets and raw results. The following requirements
come directly from the researcher; recording them is not a claim that an
implementation, benchmark pin or smoke exists yet.

#### A5.1 Representation and capacity: confirmed intent, inconsistent dimensions

Before: the Router/SAE read the layer-27 1,024-dimensional MLP pre-hook input,
but the expert/shared adapters read the 3,072-dimensional down-projection input.
Each routed model has one shared rank-eight branch and eight rank-eight experts;
one expert plus the shared branch are active. Dense rank 16 has 65,536 matrix
parameters. The injected correction is inside down_proj.

Requested after: make the residual adapter/MoE parallel to the original MLP;
SAE teacher, Router and every expert must read the same layer-27 MLP pre-hook
tensor h, hidden size 1,024. Add shape and hook/input-identity checks, including
offline teacher provenance checks. Forbid SAE latents, MLP outputs or other-layer
states as expert inputs. Requested routed expert dimensions are 1024→16→1024,
with exactly 32,768 matrix parameters per expert. Requested dense dimensions are
1024→32→1024, described by the researcher as the same 32,768 parameters.

**Blocked arithmetic:** with two independent low-rank matrices and no biases,
1024×16 + 16×1024 = 32,768, whereas 1024×32 + 32×1024 = 65,536. Both the requested
dense dimensions and its requested count cannot hold simultaneously. Tying or
removing a matrix to force the count would itself change the architecture and is
not authorized by inference.

**Blocked comparison:** the old Protocol includes a shared branch. Its retention
and new rank are not explicit in the request. Retaining a shared rank-16 branch
plus a selected rank-16 expert yields 65,536 active matrix parameters, matching
dense rank 32. Removing the shared branch and using dense rank 16 instead yields
32,768 active matrix parameters on each side. These are different scientific
comparisons; neither is silently selected here. The researcher must resolve the
shared-branch contract and whether dense rank or dense parameter count controls.

#### A5.2 Loss-free balancing requirements for every routed arm

SAE, GMM, random-feature and task-only/learned Router conditions all receive a
dynamic non-parameter bias b initialized to zero; dense is N/A. Router weights
may be frozen, but b must still update without autograd or optimizer membership.
Selection is k=argmax(z+b); the actual multiplier is softmax(z)[k], NEVER
softmax(z+b)[k]. This differs from old E20's native argmax(z) selection.

All gradient-accumulation microbatches in an optimizer step share one b. Count
expert assignments for ALL non-padding valid positions (not just supervised
answer positions), and after the complete effective batch update
b_i ← b_i + 0.001 sign(mean_j(c_j) − c_i). The new bias is used only by the next
optimizer step. With data parallelism, aggregate counts only inside the same
condition; never across experiment arms. The SFT scalar remains original
answer-token CE only; add no auxiliary/load-balancing loss.

Save/restore bias in full and recovery checkpoints; do not update it during
development, internal test or generation. Record each step's counts, bias used
and next bias, load fractions, MaxVio and native argmax(z) versus actual
argmax(z+b) disagreement. MaxVio is maximum relative load excess above mean:
max_i(c_i/mean_j(c_j)−1) on nonempty batches. A zero-valid-token batch is an
explicit implementation failure, not an implicit bias update.

Describe fixed-score SAE/GMM conditions as teacher-scored/initialized with
balanced selection, not strictly unchanged routing choices. The 0.001 update
rate is a frozen literature-transferred initial setting, not an established
optimum for eight experts/512 steps. Report sustained single-expert selection,
nonfinite/exploding bias or oscillatory behavior in smoke rather than silently
tuning the update rate. Operational smoke observation windows and acceptance
checks must be recorded before execution; none have yet been run for A5.

#### A5.3 Standard external benchmark requirements

Replace old E20's nonstandard generation evaluator for the new run's external
capability check with a pinned lm-evaluation-harness commit/package environment.
Resolve actual available task IDs/YAML and versions before freezing a single
evaluation manifest. Task IDs, pinned revision and dataset fingerprints remain
NOT_RESOLVED at this capacity-blocked audit; no placeholder is executable.

Requested public Qwen3-report alignment: MMLU 5-shot; MMLU-Pro 5-shot CoT;
BBH 3-shot CoT; GPQA 5-shot CoT; GSM8K 4-shot CoT; MATH 4-shot CoT;
EvalPlus 0-shot; MBPP 3-shot. Verify those settings against primary sources and
actual task definitions when implementing. If EvalPlus is not natively supported,
use its official executor in the same manifest; never label HumanEval alone as
official EvalPlus. Any unavoidable mismatch must be recorded, not hidden.

Original Qwen3-0.6B-Base and every training condition must use identical backend,
dtype, tokenizer, context length, task YAML, seed and generation/scoring settings.
Base uses no chat template, system prompt or thinking wrapper. First execute
base task-integrity checks, prompt write-out and small-sample smoke; verify the
custom adapter wrapper's loglikelihood and generation interfaces. Save harness
commit/package lock, task YAML hashes, dataset revisions/fingerprints,
show_config, prompt examples, model/checkpoint hashes and raw per-sample results.

Published paper scores are external sanity references only. Main external
comparisons are each arm minus the same base under the frozen manifest, with
no model-specific prompt/scorer tuning. Original paired internal-held-out NLL
and mechanism metrics remain the primary experiment evidence; benchmark scores
do not replace the primary endpoint or rescue its failed criterion.

#### A5.4 Gates, isolation and retention

After resolving capacity, implement in a new isolated execution source snapshot
and a new run directory, not by overwriting old E20 code or run artifacts. Keep
the registered data, seed pairing, five-condition scope, 512 updates and primary
comparison rules unless a separately explicit amendment changes them. Rename
the dense condition only to reflect its actually confirmed shape, not to hide
the resulting capacity difference.

Required minimum tests: exact h hook/shape identity, confirmed parameter counts,
biased selection/unbiased coefficient, accumulation-boundary bias updates,
padding exclusion, checkpoint/resume equality, eval-time bias freeze and lm-eval
prompt/config identity. Then small real forward/backward and short training
smoke across conditions must demonstrate finite loss, nonzero eligible gradients,
correct bias update direction and independent condition state. No test result
from E20 is substituted for these new checks.

Submit the authorized full run only after all gates pass. Record source snapshot
hashes (no Git commit required or permitted), exact config, data identity,
new run ID, platform job ID, output path and directly executable resume command.
Retain formal training data identities and accessible input data, sample order,
all training/balancing histories, initialized/intermediate/final/recovery
checkpoints, optimizer and bias states, dev/test records, evaluation manifests,
raw per-sample predictions and failure artifacts for subsequent audit. Never
discard formal outputs as smoke or replace them with only aggregates.

#### A5.5 Audit disposition

2026-09-08 read-only checks verified the old architecture in model.py and Protocol
section 7, the execution workspace on the shared /data mount, and old ACP job
pt-os72i446 still SUCCEEDED. A direct tensor numel check confirms 32,768 versus
65,536 for the two requested shapes. No new implementation/smoke/full job has
been run. The old E20 source and outputs remain unchanged. Full submission is
paused exactly as requested for a comparison-changing capacity conflict, not
for missing general execution authorization.

#### A5.6 Capacity resolution and implementation authorization

On 2026-09-08 the researcher explicitly accepted the proposed shared-branch
architecture and instructed implementation to proceed. This resolves A5.1's
capacity conflict prospectively; its historical blocked snapshot is retained.
All four routed arms have a shared 1024→16→1024 branch plus eight independent
1024→16→1024 experts, with Top-1 selection. Dense has the same shared branch
plus one always-active 1024→16→1024 branch. The dense arm is named
`dense_shared_r16` in the new run, not old `dense_r16`.

Each branch has exactly 32,768 matrix parameters, without biases or intermediate
nonlinearity/dropout. All branches use scale 1/8, Kaiming-uniform A and zero B.
Per-token active adapter matrices total 65,536 in every arm; total stored
parameters are not matched to dense. Routed expert/shared matrices total 294,912,
plus the identical 8,200-parameter linear Router (frozen for SAE/random/GMM,
trainable for task-only). Dense has 65,536 trainable matrix parameters.
All shared weights and routed expert banks start identically for paired seeds.
No new trained parameters arise from balancing bias.

Architecture and A5.2 balancing requirements are now confirmed. In-scope code,
smokes and the five-arm × three-seed × 512-update training submission are
authorized after the A5 gates pass. Benchmark task/version/data pinning and its
base/interface smoke remain required before full submission; their exact receipt
will supplement this amendment. No additional generic approval is required.
The resource ceiling remains the previously authorized single reserved four-H100
ACP node; no resource fallback, extra seeds or primary-endpoint change is added.
New execution source root:
`/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router`.
Old E20 source and runs remain immutable; reuse only hash-authenticated data,
SAE, groups and offline linear Routers whose h-input contract is unchanged.

Smoke observations are operational, not parameter tuning: run 16 updates for
each routed arm and dense at seed 17, inspect per-step counts/MaxVio/disagreement,
and report if one expert receives every valid token for four consecutive steps
or if a dominant expert alternates on every step for eight consecutive steps.
Bias must be finite and satisfy |b_i| ≤ 0.001×completed_updates + 1e-6; any breach
is an implementation failure. Persist these diagnostics without silently changing
the approved 0.001 rate. Any flagged persistent pathological behavior blocks
full submission for a report, rather than triggering automatic redesign.

#### A5.7 Qualification status receipt — 2026-09-08

This is an execution-gate receipt, not a scientific design change. A5.6 remains
the approved architecture; no full run has been submitted. The new workspace
contains implementation and local checks only. Thirty regression tests passed;
real-model five-arm smoke records and their mechanical verification are retained
under `local_checks/` in the A5.6 execution source root. The interrupted dense
attempt is retained separately from its fresh rerun. No E20 input was modified.

The benchmark submission gate is BLOCKED. Native lm-eval 0.4.12 task discovery
resolved MMLU, MMLU-Pro, BBH, GPQA main/diamond CoT, GSM8K CoT, Minerva MATH,
MBPP and plus task entries, but discovery is not prompt/scorer qualification.
`Idavidrein/gpqa` revision `633f5ee89ab8ad4522a9f850766b73f62147ffdd`
returns HTTP 401 for both main and diamond CSV through the official endpoint;
the local environment has no saved HF authentication token. Existing public
simple-evals GPQA-Diamond is a different provenance path and has NOT been
substituted for the gated native task. Native GPQA CoT YAML also supplies only
answer letters as demonstration targets, so its task name alone does not prove
alignment with five-shot rationale demonstrations.

Evidence: execution-root `local_checks/benchmark_access_audit.json` retains
actual task entries, package version, GPQA YAML/helper hashes, revision and
access failures. `local_checks/training_smoke_verification.json` retains the
separate training qualification receipt. The frozen evaluation manifest,
base benchmark task-integrity/prompt write-out, adapter harness interfaces and
official EvalPlus executor qualification remain incomplete; none is marked PASS.
No new formal run ID, job ID, training ETA or benchmark result exists.

Unblocking requires authorized access to the native GPQA data, or an explicit
researcher-approved amendment for alternate provenance/task scope. Credentials
must be configured privately, never pasted into research artifacts or chat.
After access is resolved, remaining implementation and benchmark checks must
still pass before the already-authorized full submission. The data/checkpoint
retention contract in A5.4 remains unchanged. No commit, push or publication is
part of this receipt.

#### A5.8 Benchmark freeze and actual-image qualification — 2026-09-08

This append-only execution receipt supersedes A5.7's access-blocked status;
the historical receipt is preserved. Authorized GPQA access was configured
privately and the native main population at the same recorded revision was
downloaded and hash-pinned. No alternate GPQA dataset was substituted.
The primary endpoint, five approved arms, three seeds, 512 updates, architecture,
0.001 bias update and reserved four-H100 resource ceiling remain unchanged.

The evaluation implementation pins lm-evaluation-harness v0.4.12, commit
`6d642546f4688648fced259eb3302efd36ece5af`, and resolves 108 native leaf tasks.
Entry families and demonstrations are MMLU 5; MMLU-Pro 5 CoT;
BBH `bbh_cot_fewshot` 3; GPQA `gpqa_main_cot_n_shot` 5 CoT;
GSM8K `gsm8k_cot` 4; MATH `minerva_math` 4; and MBPP 3.
GPQA demonstrations use the five original GPQA rationale examples pinned at
`56686c06f5e19865c153de0fdb11be3890014df7`, not the native YAML's
answer-letter-only demonstration targets. Official EvalPlus 0.3.1 uses
HumanEvalPlus v0.1.10 and MbppPlus v0.2.0 with zero-shot completion prompts;
the four base/plus pass@1 components remain separately available.

All model variants share the same causal HF backend, bfloat16, SDPA, tokenizer,
32768-token context ceiling, seed 1234, batch size one, deterministic decoding,
native frozen task generation limits/scorers, and no chat/system/thinking
wrapper or added BOS. The local base generation configuration's inherited
`max_new_tokens=2048` is cleared in memory for every model so it cannot override
the per-task generation limit. Original model files are not modified.
This aligns publicly specified shots and CoT settings, not Qwen's unpublished
exact prompt/scoring stack. Benchmark-family training contamination prevents
calling these external checks clean generalization measurements.

Execution-root `benchmark_assets/manifest.json` preserves pinned datasets,
fingerprints, task YAML/helper hashes, model/tokenizer hashes and prompt rules.
The formal run's enclosing `evaluation_manifest.json` freezes that manifest's
hash, official code assets, actual ACP package lock and the shared generation
override. The earlier manifest's PINNED_NOT_QUALIFIED label is historical;
qualification is owned by the linked immutable receipts, not a rewritten label.

Qualification evidence under the A5.6 execution root:

- `local_checks/final_regression.json`: 37 tests passed on the final Python
  source, covering input/capacity, balancing, accumulation/padding, resume,
  evaluation freeze, benchmark contracts and formal matrix gates.
- `local_checks/live_teacher_router_expert_h.json`: real backbone and SAE
  verified the identical layer-27 input tensor, shape 1×4×1024.
- `local_checks/benchmark_integrity_v1/`: all 108 leaf tasks passed native
  schema/target/fewshot/request checks with saved full prompt write-outs.
- `local_checks/acp-runtime-20260908T105844Z/runtime/receipt.json`, job
  `pt-4kv7h2nn`: actual approved image, Python 3.12, CUDA 12.9, four GPUs,
  dependencies, isolated code execution and known-correct scoring passed.
- `local_checks/acp-qualification-20260908T110501Z/qualification/receipt.json`,
  job `pt-s14666e2`: all five arms completed 16 updates; no registered
  operational pathology was flagged. SAE/GMM partial held-out intervention
  smoke, base plus five adapter likelihood/generation interfaces, seven-family
  base harness smoke and both official EvalPlus generation/execution smokes
  passed in that same ACP image. Evaluation weights and bias remained frozen.

Earlier failed image probes remain retained: the code metric's unnecessary
Torch import triggered MKL inside the restricted namespace. The final executor
loads the pinned official scoring function and execution helper without that
unneeded model-library import. The scoring function itself was not rewritten.
Known-correct and known-wrong MBPP cases and official EvalPlus correct cases
passed; generated code has no network or mounted user credentials.

These are operational gates, not benchmark capability results or a mechanism
claim. All A5 submission gates are PASS. The previously authorized full training
may now be submitted through `source/acp_full.sh` in a new authenticated run.
Four independent workers divide the 15 conditions without cross-arm count
aggregation; full paired internal test NLL and registered interventions follow
training. The expensive all-model external benchmark is NOT RUN by this
training submission and retains a separate resumable standardized entrypoint.
Old E20 training data/results are not overwritten, and no commit/push is added.

#### A5.9 Formal submission receipt — 2026-09-08 11:23 UTC

New run: `full-20260908T111248Z` under the A5.6 execution root's `runs/`.
ACP job: `pt-j131dsb1`, submitted 11:14:11 UTC, platform RUNNING since
11:14:52 UTC on the approved single reserved four-GPU `n6ls.iu.i40.4` node
and the actual-image-qualified NGC 25.06 / CUDA 12.9 / Python 3.12 image.
The launch is bounded to 12 hours and retains the approved 15-condition matrix.
The immutable `manifest.json` records config, source/input hashes and resume
command; `submission_attempt.json` and `submission_receipt.json` preserve the
exact platform command and job identity. `protocol_at_submission.md` is the
pre-submission protocol snapshot; later operational receipts do not rewrite it.

At 11:23:19 UTC, `monitoring/five_minute_health.json` passed after 358 seconds
of observation from the first recorded optimizer progress. SAE seeds 17/29/43
were at updates 337/338/343 and random-features seed 17 at 338. All four had
finite loss and nonzero gradients, retained recovery and update-256 checkpoints,
and no condition failure record. The platform remained RUNNING. Recovery audits
verified optimizer/bias state, per-step count/update/bound correctness and the
identical paired seed-17 512×128 sample schedule. These checks do not imply
uniform expert load or scientific efficacy.

The operational estimate for all training plus internal evaluation is
12:00–12:20 UTC, not a guarantee. Remaining conditions are assigned to the same
four workers; this receipt is not a claim that 15 conditions have completed.
Formal inputs, initialization/intermediate/final/recovery checkpoints, optimizer
and bias state, sample schedules, histories and raw internal evaluation records
remain in this distinct run for later audit. Full external benchmark scores are
still NOT RUN; only the standardized submission-gate smokes are complete.
