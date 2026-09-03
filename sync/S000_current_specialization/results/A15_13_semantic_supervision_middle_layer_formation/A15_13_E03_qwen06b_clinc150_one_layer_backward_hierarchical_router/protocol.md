# Protocol: A15_13_E03 Qwen3-0.6B CLINC150 One-Layer Backward Hierarchical Router

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN
Approval status: direct researcher authorization on 2026-08-30
Block audit status: A-G CONFIRMED under delegated AI selection
Cross-block consistency: PASS
Execution scope approved: data preparation, implementation, smoke, 8xRTX5090 Spot full run, analysis, local result records
Design frozen at: before first training job submission
Purpose: test whether final-layer learned semantics can organize one middle layer better through parent-first growth than through flat routing
Primary Anchor: A15_13_01 CLINC150 one-layer backward hierarchical Router
Experiment role: real-task transfer and method falsification
Primary metric: equally weighted mean of 10 domain-local 15-intent test macro-F1 scores from frozen linear probes at block 14
Minimal setup: Qwen3-0.6B-Base, official CLINC150 in-scope splits, two paired seeds, only block-14 residual module trainable in stage two
Treatment: learned final-layer soft semantics -> shared expert -> 10 parent experts -> freeze -> 15 child experts per parent with coarse-subspace removal
Controls: dense residual continuation; learned-semantic flat 150-expert top-2 Router; gold-label hierarchical Oracle
Changed variable: one-layer conditional organization and supervision source
Held fixed: teacher seed, data order, tokenization, base checkpoint, block, active expert count, bottleneck, optimizer-step budget, task objective, analysis
Pass: both seeds positive for treatment minus flat, pooled paired 95% interval lower bound > 0, and intent macro-F1 degradation <= 1 point
Fail: pooled interval upper bound <= 0, or both seed effects <= 0, with all guards valid
Insufficient: teacher, data, implementation, resource, completeness, paired-seed, uncertainty, or functional guard fails
Cannot claim: unsupervised semantic discovery, native Router use, counterfactual expert utility, compute efficiency, larger-scale transfer, or open-domain hierarchy
Approval decision: execute without a second review; never use or fall back to H100
```

The confirmed active task card is
[the A15_13 Focus](/daily_research_reports/backup/2026/08/0830/focus_semantic_supervision_middle_layer_separability.md).
The scientific owner is
[A15_13_01](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_01_clinc150_one_layer_backward_hierarchical_router_anchor.md).

## 1. Terminology And Definitions

- **Teacher:** Qwen3-0.6B-Base fine-tuned on CLINC150 training data with token next-token loss plus domain and intent classification losses; development data select the checkpoint, which is then frozen.
- **Backward semantic chain:** the frozen final classification distribution supplies a soft semantic target to a Router inserted after an earlier block. It is knowledge distillation across depth, not access to future test labels.
- **Parent-conditioned fine separability:** how well 15 fine intents can be linearly predicted inside each of the 10 known domains from a frozen block-14 representation.
- **Flat Router:** one 150-way gate with 150 bottleneck experts and top-2 activation, trained in one stage from teacher fine-intent distributions.
- **Hierarchical Router:** one 10-way parent gate followed by a 15-way child gate inside the selected parent. One parent and one child expert are active per example.
- **Coarse-subspace removal:** only the child gate input removes the row space of the frozen parent gate; the residual stream and expert inputs remain complete.
- **X-MoE representation-collapse statistic (RC):** $\operatorname{Tr}(\Sigma_W\Sigma_B^\dagger)$ using 150 intents as classes. Smaller values mean stronger within-class neural collapse in the source paper. RC is a collapse guard, not the primary semantic-separability score.

Condition names are `DENSE`, `FLAT150`, `HIER_ORACLE`, and `HIER_BACKCHAIN`.

## 2. Anchor Alignment

The experiment tests whether staged final-to-middle supervision improves one
earlier representation beyond generic adaptation. It preserves the boundary
that readable geometry and functional expert utility are different claims. The
strongest rival is that added capacity or any classification auxiliary loss
explains the change.

## 3. Tested Hypothesis

`HIER_BACKCHAIN - FLAT150` is positive on held-out domain-local fine-intent
linear-probe macro F1, replicates across both paired teacher seeds, and passes
the final-task non-degradation guard. `HIER_ORACLE` estimates whether label
quality is the bottleneck. `DENSE` estimates ordinary one-layer continuation.

## 4. Rival Explanations

| Rival | Separating evidence |
|---|---|
| Any extra parameters help | `DENSE` and the before/after teacher comparison |
| Any semantic Router helps | `HIER_BACKCHAIN` versus `FLAT150` |
| Only gold labels organize the layer | `HIER_ORACLE` versus `HIER_BACKCHAIN` |
| Probe improves while task breaks | intent/domain F1 and cross-entropy guards |
| States become low-rank or degenerate | X-MoE RC, effective rank, covariance audit |
| Router memorizes load without semantics | route-label mutual information and load entropy |

## 5. Data Construction And Provenance

Source is the local official CLINC snapshot:

```text
/data/250010109/MoE_Router/data_sources/clinc_oos_eval_828f8093932c/data/data_full.json
/data/250010109/MoE_Router/data_sources/clinc_oos_eval_828f8093932c/data/domains.json
```

Only in-scope `train`, `val`, and `test` entries are used. The raw counts are
15,000, 3,000, and 4,500. A pre-training audit found five normalized exact-text
duplicates across splits: three train--development and two train--test. The
training occurrence is retained and the five later-split occurrences are
deterministically excluded without using their labels, giving effective counts
15,000, 2,997, and 4,498. No replacement examples are introduced. Each intent
maps to exactly one of 10 domains with 15 intents per domain. One example is
one English utterance plus intent and derived domain labels. The rendered input
is `User request: <utterance>` followed by the tokenizer end token. Labels are
never rendered in the input.

Training labels may fit the teacher and Oracle. Training utterances may create
teacher soft targets for learned conditions. Development labels select teacher
and stage-two checkpoints. Test utterances and labels remain sealed until all
models and analysis rules freeze. Out-of-scope examples are excluded.

Preflight requires the exact raw counts and balance, exactly five registered
cross-split normalized-text duplicates, zero cross-split overlap after the
deterministic train-priority filter, a total label-domain mapping, token length
at most 96, and SHA-256 manifests. Any other overlap or audit failure stops.

## 6. Learning Task And Permitted Supervision

Given an utterance, the model predicts one of 150 intents and one of 10 domains
from the last non-padding state. The visible utterance also supports causal
next-token prediction. Gold labels are permitted for the common teacher and
Oracle only. Learned conditions receive the frozen teacher's training-split
soft posteriors; they never receive test labels or states during fitting.

## 7. Model, Architecture, And Frozen Variants

- Base: official `Qwen/Qwen3-0.6B-Base`, BF16, 28 layers, hidden size 1024.
- Intervention: a zero-initialized residual module after zero-indexed block 14.
- Teacher heads: linear 1024-to-150 intent and 1024-to-10 domain heads over the last non-padding final state.
- Stage two freezes all Qwen weights and both heads; only the residual module trains. Frozen upper blocks remain differentiable with respect to their input.
- Expert: `Linear(1024,48) -> SiLU -> Linear(48,1024)` with zero-initialized output projection.
- `DENSE`: two residual experts, both active.
- `FLAT150`: 150 experts with soft top-2 routing.
- `HIER_*`: 10 parent plus 150 child experts with top-1 parent and top-1 child.
- Gates use centered inputs and linear logits. X-MoE projection is not added; X-MoE is used only for analysis.

The hierarchical output is $h'=h+0.1E_c(h)+0.1E_{c,f}(h)$. During the child
stage, parent gate and experts are frozen. Only the child gate reads the
coarse-subspace-removed state; both experts read complete $h$.

## 8. Training Objective And Optimization

The teacher minimizes

$$
L_T=L_{\mathrm{NTP}}+L_{\mathrm{intent}}+0.2L_{\mathrm{domain}}.
$$

Teacher training uses AdamW, three epochs, global batch 256, base learning rate
$2\times10^{-5}$, head learning rate $10^{-4}$, weight decay 0.01, 5% warmup,
cosine decay, gradient norm 1.0, BF16, and maximum length 96. Development
intent macro F1 selects the checkpoint; ties use lower intent cross entropy,
then earlier step.

Each teacher seed must reach development intent macro F1 at least 85%, domain
macro F1 at least 95%, minimum domain-local intent macro F1 at least 75%, and
finite losses. Both seeds must pass before stage two.

Each stage-two condition receives four complete training passes, AdamW learning
rate $3\times10^{-4}$, weight decay 0.01, global batch 256, 5% warmup, cosine
decay, gradient norm 1.0, and residual scale 0.1.

- `DENSE`: both residual experts train for four passes on $L_T$.
- `FLAT150`: four passes on $L_T+0.5\operatorname{CE}(q_T(y|x),p_{14}(y|x))+0.01L_{balance}$.
- `HIER_ORACLE`: pass 1 shared expert; pass 2 train 10 parent experts with hard domain CE; freeze parent path; passes 3-4 train children with hard within-domain intent CE.
- `HIER_BACKCHAIN`: the same schedule with teacher soft domain and conditional-fine distributions.

All groups use the same utterance order per paired seed. Development selects
the stage-two checkpoint by the primary probe subject to the task guard; ties
use lower intent cross entropy and then earlier checkpoint.

## 9. Conditions, Seeds, And Checkpoints

Teacher seeds are 17 and 29; stage-two randomness is teacher seed plus 1000.
Each seed runs all four conditions from the identical teacher checkpoint. The
matrix is eight stage-two runs plus two teachers.

| Condition | Router target | Growth | Parent freeze | Child de-common | Role |
|---|---|---|---|---|---|
| `DENSE` | none | two shared residual experts | no | no | generic continuation |
| `FLAT150` | teacher soft intent | one-shot 150-way top-2 | no | no | flat semantic control |
| `HIER_ORACLE` | gold domain and intent | 1 -> 10 -> 10x15 | yes | yes | upper bound |
| `HIER_BACKCHAIN` | teacher soft domain and conditional intent | 1 -> 10 -> 10x15 | yes | yes | primary treatment |

## 10. Primary Metric And Frozen Analysis Plan

For each selected checkpoint, extract the last non-padding state immediately
after block 14 for every split. Within each domain, standardize training
representations, fit multinomial logistic regression over its 15 intents with
regularization selected from `C={0.01,0.1,1,10}` on development macro F1, and
evaluate once on test. Average the 10 domain macro F1 scores equally. The unit
is percentage points.

The primary estimand is

$$
\Delta=\mathrm{F1}_{\mathrm{HIER\_BACKCHAIN}}-
\mathrm{F1}_{\mathrm{FLAT150}}.
$$

The independence unit is an utterance. A stratified paired bootstrap with
10,000 draws resamples test examples within intent, recomputes all 10 domain
macro F1 values, and reports the percentile 95% interval. Both seed effects
must be positive and the pooled interval lower bound must exceed zero. There is
one primary comparison, so no multiplicity correction applies. Missing rows,
nonfinite states, probe convergence failure, or incomplete pairs make the
result Insufficient; no outliers are removed.

## 11. Secondary Metrics And Guards

1. Final intent macro F1, domain macro F1, intent cross entropy, and token-
   average next-token cross entropy. The treatment may not lose more than one
   intent-F1 point versus flat within either seed.
2. Domain-local 5-nearest-neighbor macro F1 and normalized nearest-centroid
   margin fifth percentile. They cannot rescue the primary result.
3. X-MoE RC with 150 intent classes, effective covariance rank, and top-10
   eigenvalue mass. The pseudoinverse cutoff is $10^{-6}$ of the largest
   between-class eigenvalue.
4. Router-domain/intent normalized mutual information, load entropy normalized
   by log expert count, utilization, and paired-seed adjusted mutual
   information. They describe routing, not expert utility.
5. Trainable parameters, active expert multiply-add count, peak memory, and
   examples per second. Flat and hierarchical conditions must both evaluate
   two experts per example; their total expert-count difference remains
   explicitly reported.

## 12. Known Good, Known Bad, And Known Confusing Cases

- Known good: an overfit batch reaches at least 99% intent accuracy, and every
  condition changes block-14 states from its initial no-op.
- Known bad: shuffled intent labels do not pass the held-out teacher entrance.
- Known confusing: `routing` versus `transfer`, reservation cancellation
  intents, and yes/no/maybe meta intents receive a frozen confusion audit but
  never tune the model.
- Identity guard: before training, zero-initialized modules reproduce teacher
  logits within $10^{-5}$ in FP32 and $5\times10^{-3}$ in BF16.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input and operation | Output | Stop rule and handoff |
|---|---|---|---|---|
| P0 | validate the real hierarchy | hash and audit official files; render inputs | data manifest and audit JSON | any schema or leakage failure stops |
| P1 | prove 0.6B capability | train two teachers; select only on development | two frozen checkpoints and entrance report | either seed fails: repair teacher only, with test sealed |
| P2 | validate one-layer causality | identity, gradient locality, split/freeze, overfit, metric tests | smoke report and parameter/gradient ledger | any failure stops full run |
| P3 | execute paired matrix | eight stage-two runs on one 8x5090 node | checkpoints, logs, states | after Spot preemption, retain complete conditions and deterministically restart each incomplete condition from its frozen teacher; no H100 fallback |
| P4 | freeze and unseal | select on development; freeze hashes; evaluate test | primary table, bootstrap arrays, metric audit | incomplete pair is Insufficient |
| P5 | report machine evidence | render only eligible comparisons | summary, detailed, figures | human judgment remains pending |

## 14. Algorithm, Output, And Provenance Contract

Implementation lives at
`/data/250010109/MoE_Router/experiments/20260830_a15_13_e03_qwen06b_clinc150_backward_hierarchical_router`.
Raw outputs and checkpoints remain in its `runs/` tree. Canonical records and
compact figures live beside this Protocol. The worker emits data, model,
training, checkpoint-selection, metric, resource, and completion manifests.
Source and configuration hashes freeze before submission.

The only permitted resource tuple is:

```text
resource_profile=5090-8-spot
execution_surface=ACP
workspace=share-space
aec2_cluster=computing-cluster-5090-01g
worker_spec=n12lp.nn.i10a.8
worker_nodes=1
quota_type=spot
priority=normal
visible_gpus=8
H100_fallback=forbidden
```

## 15. Success, Failure, And Insufficient Evidence

- **Pass:** the primary paired rule and functional guard pass. This supports
  only the named final-to-middle hierarchy relative to flat routing.
- **Fail:** the primary rule is non-positive with valid teachers and guards.
  This rejects promotion of this exact algorithm even if Oracle or secondary
  metrics are positive.
- **Typed failure:** Oracle positive and learned hierarchy negative localizes
  failure to the teacher-posterior chain; Oracle negative localizes it to the
  architecture/objective package.
- **Insufficient:** any entrance, conformance, completeness, paired-seed,
  resource, uncertainty, or task guard fails.

## 16. What This Cannot Claim

Even a Pass cannot establish unsupervised semantic discovery, native
pretrained Gate use, causal expert specialization, lower compute, faster
convergence, out-of-scope detection, arbitrary semantic hierarchies, or
transfer beyond Qwen3-0.6B and CLINC150. RC alone is not evidence of semantic
separability.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
|---|---|---|
| A question and boundary | CONFIRMED | direct researcher instruction plus parent A15_13 |
| B data and provenance | CONFIRMED | CLINC150 selected under explicit delegated selection |
| C task and supervision | CONFIRMED | direct real-task and backward-chain requirement |
| D architecture | CONFIRMED | direct one-layer constraint; exact block/capacity delegated |
| E objective and optimization | CONFIRMED | frozen AI selection under direct no-reapproval instruction |
| F comparison and evidence | CONFIRMED | direct request for controls, own algorithm, separability and X-MoE audit |
| G execution | CONFIRMED | full run authorized; 8x5090 selected; H100 forbidden |

Cross-block consistency is `PASS`. The researcher explicitly instructed the AI
to select the task and design and start without another approval round. This is
confirmation of the enumerated delegated choices, not evidence that the method
works. Implementation, smoke, and full-run scopes are approved. Commit, push,
publication, destructive cleanup, and H100 fallback are unauthorized.

After the first submission, scientific changes require an append-only
amendment with before and after values, reason, evidence already visible,
affected conditions, approval basis, and eligibility effect.

### Pre-start correction P0-01 (2026-08-30)

- **Before:** the candidate text said the raw official splits had zero exact
  text overlap and that all 3,000/4,500 development/test rows would be used.
- **After:** the raw audit must find the five named train-priority duplicates;
  later-split copies are removed, yielding 2,997 development and 4,498 test
  examples.
- **Reason:** direct model-independent inspection of the official local files
  found 3 train--development and 2 train--test normalized exact-text overlaps,
  including conflicting labels.
- **Evidence visible:** data rows only; no model was implemented, trained, or
  evaluated and no metric result existed.
- **Affected blocks:** B and F. The scientific comparison, labels, model,
  primary metric, thresholds, conditions, seeds, and resources are unchanged.
- **Approval basis:** the researcher delegated data audit and repair and
  instructed execution without a second approval round.
- **Eligibility:** all later runs use the corrected effective splits and remain
  eligible; using unfiltered evaluation rows is ineligible.
