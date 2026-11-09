# Protocol: A15_13_E06 CLINC150 Hard-Route Gradient And Functional Audit

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN
Approval status: HUMAN_CONFIRMED on 2026-09-01
Block audit status: A-G CONFIRMED
Cross-block consistency: PASS
Execution scope approved: implementation, smoke, full run, analysis, curated result records
Design frozen at: 2026-09-01 before implementation
Purpose: decide whether CLINC150 fine intents define functionally useful task-gradient partitions
Primary Anchor: 15_13_03_semantic_gradient_functional_alignment_anchor.md
Experiment role: root-cause and functional-value audit
Primary metric: worst-control confirmation cross-entropy advantage of hard semantic splitting
Minimal setup: frozen Qwen3-0.6B-Base, CLINC150, one block-14 rank-8 shared/parent/child LoRA hierarchy
Treatment: hard gold domain and fine-intent expert assignment
Controls: hard balanced-random within-domain assignment and hard one-child-per-domain assignment
Changed variable: stage-two child grouping rule only
Held fixed: data, tokenizer, base weights, stage-one start, active child rank, updates, optimizer, task, shadow semantic Router
Pass: semantic splitting beats both controls in both seeds with a positive pooled interval and positive child selective utility
Fail: a complete eligible run does not clear the value or functional gate
Insufficient: a required condition, seed, null, confirmation endpoint, intervention, or hard-route isolation check is missing
Cannot claim: deployable routing, unsupervised labels, improved pretraining geometry, generation gain, or cross-task transfer
Approval decision: execute without another approval checkpoint unless a scientific-body amendment is required
```

The approved [Focus](../../../../focus/focus_semantic_gradient_functional_alignment.md) states the same question in plain Chinese. The [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_03_semantic_gradient_functional_alignment_anchor.md) owns the research judgment.

## 1. Terminology And Definitions

- **Hard route:** the registered label directly chooses one expert. The selected expert output is multiplied by exactly `1.0`; no Router probability, logit, confidence, or straight-through estimator enters expert computation.
- **Shadow Router:** a diagnostic classifier that reads a detached native block input and predicts gold domain or intent. Its output never chooses or scales experts. Its loss updates only shadow-Router parameters.
- **Semantic split:** each gold fine intent selects one child expert inside its gold domain.
- **Balanced-random split:** examples are deterministically permuted inside each domain and split round-robin across 15 children separately for each data split. It preserves load but breaks intent grouping.
- **Common child:** all examples inside one gold domain use the same rank-eight child expert.
- **Child functional utility:** two paired confirmation interventions. First, deleting the active child must increase loss. Second, replacing it with every wrong child inside the same parent and averaging those losses must also increase loss. Both are required because deletion alone can show that a residual matters, while wrong-child substitution tests whether the learned children are non-interchangeable.
- **Task-gradient interface:** the gradient of sequence-level intent cross-entropy with respect to the child residual output at the injection point.

## 2. Anchor Alignment

E05 established semantic routing and small parent selectivity but not fine-expert representation or task value. E06 tests whether this failure is upstream route contamination, absence of fine-functional gradient structure, or optimization bypass. It does not search for labels or change the dataset.

The primary falsifier is a complete hard-route comparison in which semantic grouping fails to beat either the balanced-random or common-child control on untouched confirmation task loss, or fails the child functional gate.

## 3. Tested Hypothesis

If fine intents correspond to distinct and reusable task-update requirements, then gold-intent groups should show more compatible task gradients than within-domain alternatives, a norm-matched gold-group update should generalize better on development data, and full semantic splitting should beat both matched controls on confirmation loss with selective child-expert deletion effects.

## 4. Rival Explanations

1. **Label-code rival:** cross-entropy makes same-label gradients appear similar without giving grouped experts held-out value. The norm-matched development update and confirmation training contrasts separate this rival.
2. **Arbitrary-partition rival:** any balanced conditional capacity helps. The balanced-random control matches expert count, active rank, load, and updates.
3. **No-split rival:** an extra domain-conditioned LoRA is sufficient. The common-child control matches active child rank without fine partitioning.
4. **Optimization-bypass rival:** fine-semantic gradients exist, but shared LoRA or the task head absorb the update. Per-module gradients and the conditional child-responsibility branch separate this rival.

## 5. Data Construction And Provenance

The experiment reuses the verified E05 CLINC150 snapshot and deduplication: `15,000` training, `2,997` development, and `4,498` confirmation utterances; 150 intents are evenly nested under ten domains. One example is one raw utterance with one gold domain and one gold intent. No domain or intent string is inserted into the text.

- Training examples contribute optimizer gradients and grouped virtual updates.
- Development examples support gradient alignment, the one-step update diagnostic, smoke checks, and no final scientific claim.
- Confirmation examples remain untouched until code, fixed update count, primary analysis, and checkpoint rules are frozen.
- Gold confirmation labels may choose a hard Oracle path only during final evaluation. They never fit parameters, thresholds, random assignments, or checkpoint choices.
- Balanced-random assignments use only split identity, gold domain, example index, and seed. They do not use fine-intent labels or text.

The exact manifest, hashes, intent/domain maps, and random assignment arrays must be copied into the run root.

## 6. Learning Task And Permitted Supervision

The model receives only the utterance and predicts one of 150 intents. Every trained example contributes sequence-level 150-way cross-entropy. Gold domain and intent may choose hard experts in the diagnostic treatment and may supervise detached shadow Routers. The balanced-random control uses its frozen random child assignment only for expert selection; its task target remains the same gold intent.

Task success does not prove that the frozen representation was reshaped or that the same grouping benefits generation.

## 7. Model, Architecture, And Frozen Variants

The base is Qwen3-0.6B-Base. All original base parameters remain frozen. At zero-indexed block 14, the MLP output receives additive rank-eight shared, parent, and child LoRA residuals. The split conditions therefore activate rank 24 per example. The common-child condition also activates one rank-eight child residual, so active computation is matched although total stored child parameters are lower.

### Stage one

- Gold domain directly selects one of ten parent experts with coefficient `1.0`.
- Train shared LoRA, parent LoRA, 150-way task head, and a detached ten-way shadow domain Router.
- Child experts are absent.
- Base weights never change.

### Stage two natural-responsibility comparison

- Gold domain remains the fixed parent path and parent experts are frozen.
- Common, balanced-random, or gold intent chooses the child path with coefficient `1.0`.
- Train shared LoRA, child experts, task head, and detached shadow fine Router.
- All Routers are excluded from expert selection and scaling.

### Conditional child-responsibility intervention

Run only if the development gradient and one-step gates are positive while the natural semantic condition lacks child utility or task value. Freeze Base, shared LoRA, parent experts, all Routers, and task head; train only semantic or balanced-random child experts from the same stage-two entry checkpoint.

## 8. Training Objective And Optimization

For stage \(t\), the objective is

\[
\mathcal L_t=\mathcal L_{\mathrm{task}}+\mathcal L_{\mathrm{shadow},t}.
\]

The task term updates the trainable LoRA modules and task head. The shadow term has unit weight, reads a detached input, and updates only the corresponding shadow Router. Therefore its gradient with respect to Base, shared, parent, child, and task-head parameters must be exactly absent.

Training matches E05 unless this Protocol states otherwise: AdamW; LoRA and shadow-Router learning rate `3e-4`; task-head learning rate `1e-3`; weight decay `0.01`; gradient clipping `1.0`; five-update warmup followed by within-stage cosine decay; microbatch `64`; gradient accumulation `4`; effective batch `256`.

Each stage is two epochs over 15,000 examples: `59` updates per epoch and `118` fixed updates per stage. The fixed update-118 checkpoint is primary; development performance does not select a different checkpoint. The stage-two optimizer and scheduler restart from step zero.

## 9. Conditions, Seeds, And Checkpoints

Seeds are `17` and `29`.

| Condition | Stage-one source | Stage-two child selection | Trainable in stage two | Evidence role |
| --- | --- | --- | --- | --- |
| `HARD_COMMON` | seed-matched hard-domain checkpoint | one child per gold domain | shared, common child, head, shadow Router | no-fine-split control |
| `HARD_RANDOM` | same seed-matched checkpoint | frozen balanced-random assignment | shared, 150 children, head, shadow Router | arbitrary-partition control |
| `HARD_SEMANTIC` | same seed-matched checkpoint | gold intent | shared, 150 children, head, shadow Router | treatment |
| `CHILD_ONLY_RANDOM` | conditional, same checkpoint/init | balanced random | children only | bypass control |
| `CHILD_ONLY_SEMANTIC` | conditional, same checkpoint/init | gold intent | children only | responsibility intervention |

Stage-one and stage-two checkpoints are saved at updates `0, 1, 5, 15, 30, 59, 118` when feasible; update 118 is mandatory. All stage-two arms for one seed must share byte-identical stage-one trainable state and byte-identical child initialization before routing assignments differ.

Existing E05 learned-Gold, task-only, flat, and Dense results are contextual predecessor evidence, not replacements for the matched E06 controls.

## 10. Primary Metric And Frozen Analysis Plan

For each condition, compute the mean confirmation intent cross-entropy with equal weight over 150 intents. For each seed compute

\[
A_{r}=\bar\ell_{\mathrm{random}}-\bar\ell_{\mathrm{semantic}},\qquad
A_{c}=\bar\ell_{\mathrm{common}}-\bar\ell_{\mathrm{semantic}}.
\]

The primary value is \(V_{\mathrm{task}}=\min(A_r,A_c)\) in natural-log units per example. Positive values mean semantic splitting beats its worse comparison.

- Aggregate the two seeds equally.
- Report each seed direction separately.
- Construct 10,000 paired intent-stratified bootstrap draws by resampling examples inside every intent, preserving arm pairing and equal intent weights; recalculate the two differences and their minimum on every draw.
- No outlier is removed. A missing example, non-finite loss, or mismatched confirmation index makes that condition ineligible.
- No multiplicity correction is needed because one minimum statistic jointly requires both contrasts.
- Confirmation is unsealed only after the implementation identity tests, smoke, fixed checkpoint rule, and analysis script hash are recorded.

**Pass:** \(A_r>0\) and \(A_c>0\) in both seeds, the pooled 95% lower bound for \(V_{\mathrm{task}}\) is above zero, and both registered child functional-utility interventions pass: deletion and wrong-child substitution each increase loss in both seeds with a positive pooled 95% lower bound.

**Fail:** all evidence is eligible but any task-value seed direction is non-positive, the pooled task-value lower bound is not above zero, or either child functional intervention fails its two-seed and pooled-interval requirement.

**Insufficient:** any required arm, seed, confirmation array, intervention, gradient-null artifact, or hard-route isolation check is missing or invalid.

## 11. Secondary Metrics And Guards

1. **Gradient alignment:** on all development examples at stage-two entry, compute same-intent minus different-intent within-domain cosine similarity of the task-gradient interface. Compare it with 1,000 balanced-random assignment nulls. It diagnoses grouping structure but cannot prove value.
2. **Norm-matched one-step gain:** use training gradients to form semantic, random, and common rank-eight LoRA updates; choose one small global step scale using the common control on development and hold it fixed. Compare development cross-entropy after equal update norm. It separates label appearance from local optimization value but cannot replace full training.
3. **Module responsibility:** at updates `0, 1, 5, 15, 30, 59, 118`, record per-parameter gradient root-mean-square, optimizer update norm, parameter norm, exposure count, and child/shared ratios for shared LoRA, parent, child, task head, and shadow Routers.
4. **Child functional utility:** separately report (a) deleted-active-child loss minus intact loss and (b) mean wrong-child-substitution loss minus intact loss. Pair every confirmation example and pool with the same intent-stratified bootstrap. Report every intent and seed; both contrasts must pass.
5. **Task guards:** macro F1, worst-decile intent F1, development learning curve, and updates to a frozen development-loss threshold selected before confirmation.
6. **Representation diagnostics:** child/shared residual norm ratio, child-only incremental linear readout, nearest-neighbor accuracy, and Router-row-space angles. These cannot rescue a failed task-value result.
7. **Shadow semantic performance:** domain/intent macro F1, normalized mutual information, largest load, sample entropy, and load entropy. Balanced load is never called semantic.

## 12. Known Good, Known Bad, And Known Confusing Cases

- **Known good:** manually changing shadow logits must change shadow predictions while leaving expert indices, expert weights, task logits, and task gradients unchanged.
- **Known bad:** if any selected hard expert weight differs from `1.0`, or route loss produces a gradient in a non-Router parameter, the run stops before full execution.
- **Known confusing:** balanced-random routing should have balanced load and low intent agreement; this verifies that load balance is not being interpreted as semantics.
- **No-op identity:** with child residual forced to zero, common, random, and semantic stage-two models must produce identical task logits from the same stage-one state.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input | Operation | Required output | Failure and handoff |
| --- | --- | --- | --- | --- | --- |
| Data preflight | freeze examples and null assignments | verified E05 data | rebuild manifests and balanced random arrays | hashes, counts, balance audit | mismatch stops all work |
| Identity tests | prove hard/shadow isolation | tiny synthetic tensors and real batch | vary shadow logits, backprop losses | unit-weight and gradient-isolation receipts | any influence stops smoke |
| GPU smoke | prove constructibility | one seed, small batches | stage-one and all three stage-two forwards/backwards | finite losses, checkpoints, gradients, utility arrays | no scale-up if incomplete |
| Hard stage one | create common coarse start | frozen Base, gold domains | 118 updates | one checkpoint per seed | all stage-two arms wait |
| Static gradient audit | test local gradient structure | fixed stage-one checkpoint | development interface gradients and random nulls | alignment and one-step artifacts | recorded before confirmation unseal |
| Main stage two | test semantic value | common checkpoint and child init | 118 updates for three arms | final checkpoints and trajectory logs | all six arms required |
| Conditional responsibility | test bypass only when gate triggers | same start and init | child-only semantic/random | paired task and utility artifacts | cannot rescue primary Pass |
| Confirmation and analysis | apply frozen verdict | fixed checkpoints | unseal once and compute all metrics | aggregate, figures, completion audit | missing evidence is Insufficient |

## 14. Algorithm, Output, And Provenance Contract

Worker workspace:

```text
/data/250010109/MoE_Router/experiments/20260901_a15_13_e06_clinc150_hard_route_gradient_functional_audit
```

Expected run root:

```text
/data/250010109/MoE_Router/experiments/20260901_a15_13_e06_clinc150_hard_route_gradient_functional_audit/runs/<run_id>
```

Required artifacts include code/config hashes, environment inventory, data manifest, random assignments, stage-one checkpoints, stage-two checkpoints, per-example task losses and indices, gradient alignment arrays, random-null statistics, one-step diagnostics, module trajectory logs, child deletion/substitution arrays, shadow route metrics, aggregate JSON, completion audit, and report-ready figures.

Execution uses one reserved four-H100 node as previously authorized. Conditions may run in parallel across the four devices; one condition must not silently become data parallel. No resource fallback, extra model, extra dataset, or scientific condition is authorized.

## 15. Success, Failure, And Insufficient Evidence

- `PASS_SEMANTIC_FUNCTIONAL_VALUE`: primary task value and child utility gates pass.
- `FAIL_NO_SEMANTIC_VALUE`: semantic grouping does not beat both matched controls.
- `FAIL_NO_CHILD_FUNCTION`: task value is positive but selective child utility does not pass.
- `DIAGNOSIS_OPTIMIZATION_BYPASS`: gradient and one-step diagnostics are positive, natural child function fails, and the conditional child-only branch restores function. This is not a method Pass.
- `INSUFFICIENT`: eligibility or completeness fails.

No secondary metric changes these typed meanings.

## 16. What This Cannot Claim

Even a Pass does not show that model-generated labels work, that shadow Router predictions can recover the hard-route gain, that original Qwen representations improve, that semantic clustering is solved, or that the result transfers to token routing, MASSIVE, generation, multilingual data, or larger models. Hard confirmation routes consume gold labels and are an upper-bound intervention.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A question and boundary | CONFIRMED | user-approved gradient/function/value boundary |
| B data | CONFIRMED | retain verified CLINC150 contract |
| C task and supervision | CONFIRMED | 150-way sequence cross-entropy and hard labels |
| D architecture | CONFIRMED | unit-weight hard experts plus diagnostic-only shadow Routers |
| E objective and optimization | CONFIRMED | E05-matched two-stage settings and disjoint shadow loss |
| F comparisons and evidence | CONFIRMED | semantic versus balanced random and common controls |
| G execution | CONFIRMED | implementation, smoke, full run, analysis on reserved four H100 |

Cross-block consistency audit: `PASS`. The researcher explicitly approved the adjudication boundary, functional value definition, unit-weight hard routing, diagnostic-only shadow Routers, and immediate execution on 2026-09-01.

Pre-run clarification `C001` (2026-09-01, before smoke and before any result was observed): the approved matched-deletion and wrong-substitution audit is registered as two separate mandatory functional gates. This prevents deletion-only usefulness from being misreported as child selectivity. The clarification strengthens the functional gate without changing data, arms, training, primary task statistic, or execution eligibility.

After implementation begins, any change to data, grouping, hard-route weight, shadow gradient isolation, training stages, primary statistic, verdict rule, or confirmation boundary requires an append-only amendment with eligibility impact.
