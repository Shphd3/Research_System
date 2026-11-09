---
experiment_id: A15_13_E01_three_layer_semantic_supervision_residual_growth
status: APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN
created: 2026-08-30
primary_anchor: A15_13_semantic_supervision_middle_layer_formation
implementation_authorized: true
smoke_authorized: true
full_run_authorized: true
scientific_contract_frozen: true
execution_surface: acp
resource_profile: h100-4-reserved
---

# Protocol: Three-Layer Final-to-Middle Semantic Supervision and Residual Expert Growth

## 0. Approval Snapshot

| Field | Frozen value |
| --- | --- |
| Document status | `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_RUN` |
| Human authorization | direct 2026-08-30 approval of data construction, implementation, smoke, all full conditions, and one reserved four-H100 node |
| Unique question | whether frozen third-layer labels and staged parent-first expert growth improve second-layer unseen-template conditional-fine geometry without harming full-sequence language function |
| Primary Anchor | [A15_13](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/15_13_semantic_supervision_middle_layer_formation_anchor.md) |
| Confirmed Focus | [active Focus](../../../../../../../daily_research_reports/backup/2026/08/0830/focus_semantic_supervision_middle_layer_separability.md) |
| Primary metric | minimum across parents of the TEST-OOD fifth-percentile normalized fine-label margin at the effective second-layer output |
| Main functional guards | full-sequence and query-answer negative log likelihood, plus query-answer accuracy |
| Main falsifier | staged residual hierarchy does not beat its same-label full-state control, or semantic conditions do not beat matched no-semantic/shuffled controls while preserving language function |
| Seeds | two paired teacher seeds: 1701 and 2903 |
| Full-run rule | Oracle failure never cancels learned-label conditions; it only limits their interpretation to diagnostics |
| Cannot claim | open-domain semantics, native Gate use, expert function, learning-speed or compute advantage, or transfer beyond this synthetic task |

Blocks A--G are `CONFIRMED_BY_DIRECT_EXECUTION_AUTHORIZATION`; cross-block
consistency is `PASS`. This file freezes the scientific execution contract.

## 1. Terminology / Definitions

- **Parent label:** binary direction \(c\) in the hidden affine rule.
- **Conditional fine label:** binary identity \(f\) interpreted within one parent.
- **Leaf label:** the four-way pair \(2c+f\).
- **Oracle label:** the generator-recorded true \(c,f\) values.
- **Learned label:** a frozen candidate partition constructed only from the
  frozen teacher's third-layer pre-answer representation. It is not called
  semantic truth before post-freeze evaluation against Oracle labels.
- **Flat model:** one four-way decision learned in one stage.
- **Staged hierarchy:** one expert, then two parent experts, then four leaf
  experts after the parent gate and experts are frozen.
- **Residual routing:** the fine gate alone reads a state with the learned
  coarse discriminant direction projected out. Experts and the main residual
  stream still receive the complete state.
- **Low-tail margin:** the fifth percentile of normalized held-out linear
  decision margins. It measures difficult-example boundary robustness and
  cannot establish Router use or expert utility.

## 2. Anchor Alignment — A: CONFIRMED

The one experiment tests four dependent links: semantic supervision, staged
parent-first growth, coarse-direction removal, and replacement of Oracle truth
by teacher-discovered labels. Controls and layer-propagation conditions protect
this one verdict and are not independent research questions.

## 3. Tested Hypothesis And Rivals

The registered expected chain is

```text
flat next-token-only
-> flat correct semantic supervision
-> staged full-state hierarchy
-> staged residual-routing hierarchy.
```

Each arrow is tested with the same label source. The strongest rival is generic
adaptation or auxiliary-loss regularization; dense/flat next-token-only and
parent-preserving shuffled-fine labels address it. A learned-label success is
eligible for a semantic interpretation only when the unsupervised construction
passes its entrance guards and the resulting treatment beats its shuffled
control.

## 4. Data Construction And Provenance — B: CONFIRMED

One sample is a complete causal sequence containing an opening phrase, three
input-to-output demonstrations, one query, its answer, and an end token. The
hidden domain is \(\mathbb Z_{11}\). The four leaves are

| Leaf | Parent \(c\) | Fine \(f\) | Hidden rule |
| --- | ---: | ---: | --- |
| L00 | 0 | 0 | \(y=u+1\pmod{11}\) |
| L01 | 0 | 1 | \(y=u+3\pmod{11}\) |
| L10 | 1 | 0 | \(y=-u+3\pmod{11}\) |
| L11 | 1 | 1 | \(y=-u+1\pmod{11}\) |

All numbers 0--10 are single tokens. Labels, rule names, and split identifiers
are metadata only and never enter visible text. Three demonstrations must
uniquely identify one of the four rules. The first answer token and all later
states are forbidden to semantic heads, label discovery, and probes.

| Split | Rows | Template combinations | Role |
| --- | ---: | ---: | --- |
| TRAIN | 100,000 | 16 | teacher/student fitting and learned-label construction |
| DEV-ID | 8,000 | same 16, new content groups | training diagnostics |
| DEV-OOD | 8,000 | 4 unseen combinations | checkpoint and fixed-strength diagnostics |
| TEST-ID | 12,000 | training combinations, new groups | secondary final evaluation |
| TEST-OOD | 24,000 | 4 untouched combinations | sole primary verdict surface |

The four leaves are exactly balanced. Ordered content tuples and every
paraphrase group are assigned to one split by stable hash; no group crosses
roles. Before training, automated checks must verify rule uniqueness, balance,
counterfactual dependence on both \(c\) and \(f\), split isolation, no visible
label token, pre-answer indexing, maximum length, and a bag-of-token-count
linear leakage accuracy no greater than 55% for parent, fine, or leaf labels.

## 5. Learning Task And Supervision — C: CONFIRMED

The model predicts every non-padding next token. The query-answer positions are
reported separately but are not double-counted in the training objective.
Oracle branches may use generator labels only in their registered semantic
loss. Learned-label construction, selection, and freezing may not read them.
Oracle labels become available to learned-label analysis only after the
candidate centers and assignments are immutable.

The frozen teacher supplies \(h_3\) at the final position before the answer.
Normalized TRAIN \(h_3\) vectors fit a balanced spherical binary split, followed
by one balanced binary split inside each candidate parent. Candidate fitting
uses 16 deterministic starts on at most 20,000 complete paraphrase groups.
Selection uses spherical inertia, paraphrase agreement, exact non-collapse,
and 20 group-bootstrap stability draws; it never uses true labels. Soft targets
are cosine-to-center softmax probabilities with temperature 0.1. Centers and
all TRAIN/DEV assignments are frozen before Oracle alignment is computed.

Entrance guards are: every leaf fraction in \([0.20,0.30]\), paraphrase agreement
at least 0.90, and median bootstrap adjusted mutual information at least 0.80.
Failure marks learned-label semantic interpretation `INSUFFICIENT`, but the
authorized learned-label training still runs as a diagnostic.

## 6. Model And Architecture — D: CONFIRMED

The teacher is a decoder-only three-block Transformer with hidden width 256,
eight attention heads, feed-forward width 1,024, pre-normalization, SwiGLU,
rotary positions, tied input/output embeddings, maximum length 64, and the
frozen generated vocabulary. Semantic and routing objects read only the
pre-answer token.

Second-stage students clone the same seed-matched teacher. Embeddings, all
three teacher blocks, final normalization, and language head are frozen. New
modules are inserted after block two; language gradients traverse frozen block
three into these modules.

- Dense continuation uses one residual adapter with bottleneck 128.
- The staged hierarchy uses two parent adapters of bottleneck 64 and four leaf
  adapters of bottleneck 64; one active path has total bottleneck 128.
- The flat capacity control uses one shared adapter of bottleneck 43 and four
  leaf adapters of bottleneck 85. Its active path bottleneck is 128 and its
  total adapter bottleneck count is 383 versus 384 for the hierarchy.
- A preflight parameter ledger must show total trainable parameters within 1%
  and active-path adapter multiply-adds within 1% for every primary flat versus
  hierarchical comparison. Failure is `INSUFFICIENT`.

Gates use straight-through hard top-one routing: hard selection in the forward
pass and softmax gradients in the backward pass. No load-balancing regularizer
is used. Gate collapse in the no-semantic flat baseline is recorded, not
repaired after seeing results.

Hierarchical training uses 500 root next-token-only steps, 1,500 coarse steps,
and 2,000 fine steps. The coarse gate and both parent experts are immutable
during fine training. The full-state and residual-routing conditions differ
only in the tensor read by the fine gate.

## 7. Objective And Optimization — E: CONFIRMED

The language term averages cross entropy over all valid next-token positions.
Semantic branches add equal-weight gate and post-expert representation terms.
Flat semantics use one four-way target. Hierarchical semantics use a binary
coarse target during the coarse stage and a parent-conditioned binary fine
target during the fine stage.

At each semantic stage, \(\lambda\) is frozen from the first eight TRAIN batches
so the median semantic-gradient norm on shared trainable modules is 10% of the
language-gradient norm. The resulting scalar is clipped to \([10^{-3},100]\) and
recorded before further updates. There is no result-dependent sweep.

Both stages use AdamW, learning rate \(3\times10^{-4}\), weight decay 0.1,
global batch 256, 5% linear warm-up, cosine decay, gradient clipping at 1.0,
and bfloat16 autocast with float32 losses. Teacher training lasts 8,000 updates;
every second-stage condition lasts 4,000 updates. Checkpoints are selected by
DEV-OOD answer negative log likelihood, with full-sequence negative log
likelihood breaking ties; semantic truth never selects a checkpoint.

## 8. Conditions, Seeds, And Checkpoints — F: CONFIRMED

Every row below runs for both paired teacher seeds.

| Code | Architecture | Label source | Scientific role |
| --- | --- | --- | --- |
| T0 | frozen teacher | none | entrance and unadapted representation reference |
| B0 | one dense adapter | none | absolute continuation baseline |
| B1 | flat matched experts | none | matched multi-expert/no-semantic baseline |
| O-F | flat matched experts | Oracle leaf | effect of correct semantic supervision |
| O-HF | staged hierarchy, full fine-gate state | Oracle parent/fine | value of staged hierarchy over flat semantics |
| O-HR | staged hierarchy, residual fine-gate state | Oracle parent/fine | value of coarse-direction removal |
| O-S | staged residual hierarchy | Oracle parent + group-shuffled fine | generic auxiliary-loss control |
| S-F | flat matched experts | learned leaf | learned labels as flat supervision |
| S-HF | staged hierarchy, full fine-gate state | learned parent/fine | learned-label staged hierarchy |
| S-HR | staged hierarchy, residual fine-gate state | learned parent/fine | primary advisor-intuition realization |
| S-S | staged residual hierarchy | learned parent + group-shuffled fine | learned-label auxiliary-loss control |
| L1-SEQ | freeze trained S-HR at layer two; add staged layer-one module | learned parent/fine | whether final-layer supervision adds information at layer one after layer two is fixed |
| L1-JOINT | jointly train staged modules after layers one and two | learned parent/fine | joint versus sequential depth propagation |

Shuffling operates on complete paraphrase groups inside each parent and
preserves label counts. Learned-label rows execute even if Oracle or learned-
label entrance guards fail.

## 9. Primary Metric And Frozen Analysis Plan

At every condition and seed, fit the same L2-regularized binary logistic probe
on TRAIN effective second-layer states separately inside each true parent.
Choose the penalty once on B1 DEV-OOD from
\(C\in\{10^{-4},10^{-3},10^{-2},10^{-1},1,10\}\) and reuse it everywhere.
For sample \(i\) with signed fine label \(y_i\in\{-1,+1\}\), compute normalized
margin \((y_i(w^Tz_i+b))/\lVert w\rVert_2\). The primary value is the smaller of
the two TEST-OOD parent-specific fifth percentiles.

The independence unit is the complete paraphrase group. Use 2,000 paired
bootstrap draws within each seed, then pool equal numbers of groups from both
seeds for the reported interval. A treatment comparison is `STABLE_POSITIVE`
only when both seed deltas are positive and the pooled paired 95% interval
lower bound is above zero. Two seeds do not support a broad random-seed
population theorem; disagreement is `INSUFFICIENT`.

The function guard passes only when, relative to the matched control, the
pooled 95% upper bound is at most +0.02 nats/token for full-sequence negative
log likelihood, at most +0.05 nats/query for answer negative log likelihood,
and the lower bound on answer-accuracy change is at least -1 percentage point.

Teacher entrance targets are DEV-ID answer accuracy at least 95%, DEV-OOD at
least 85%, frozen \(h_3\) parent-probe balanced accuracy at least 80%, and no
already-saturated positive conditional-fine low-tail margin at raw \(h_2\).
Failure does not cancel authorized runs but makes the main causal verdict
`INSUFFICIENT`.

Secondary diagnostics are true parent/leaf balanced accuracy, full margin
distribution, class-conditional residual effective rank, routing accuracy,
gate entropy, learned-label Oracle alignment after freezing, and training
curves. None can rescue a failed primary metric or language guard.

## 10. Result-Reporting Contract

Tomorrow's first view contains only single-variable comparisons with complete
artifacts, both seed directions consistent, and the primary metric plus
function guard. The order is fixed:

1. semantic supervision: B1 versus O-F, then B1 versus S-F;
2. staged hierarchy: O-F versus O-HF, then S-F versus S-HF;
3. coarse removal: O-HF versus O-HR, then S-HF versus S-HR;
4. label specificity: O-HR versus O-S, then S-HR versus S-S.

There is no best-versus-worst headline. Layer-one conditions are explanatory
unless their prerequisite S-HR artifacts are eligible.

The primary figure is a point-and-interval chart of TEST-OOD conditional-fine
fifth-percentile margin. A second figure may show full-sequence and answer NLL
changes. Conditions have one fixed order and color mapping across figures;
axes state metric and unit, legends define label source and architecture, and
all comparable panels use identical axis limits. PCA plots are forbidden as
verdict evidence.

## 11. Execution And Reproducibility Boundary — G: CONFIRMED

| Item | Frozen value |
| --- | --- |
| Worker code | `/data/250010109/MoE_Router/experiments/20260830_a15_13_semantic_supervision_hierarchical_experts` |
| Execution surface | SCO ACP, one worker node |
| Workspace / cluster | `share-space` / `share-cluster` |
| Worker spec | `n6ls.iu.i40.4` |
| GPU processes | four independent GPU workers on four H100 80GB GPUs |
| Quota / priority | `reserved` / `normal` |
| Image | `registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04` |
| Storage | `01995892-d478-76d8-aec7-13fd8284477e:/data` |
| Raw run root | worker-local `runs/full-<UTC stamp>/` |
| Canonical result docs | this experiment directory's `summary.md`, `detailed.md`, `figures/`, and `tables/` |

Preflight requires data tests, causal no-answer leakage, metric toy cases,
parameter/FLOP matching, frozen-backbone gradients, parent-freeze identity,
residual projection orthogonality, exact condition enumeration, four visible
GPUs, environment imports, and atomic artifact writes. Smoke uses reduced rows,
steps, and one seed, writes to a separate path, does not read TEST-OOD results,
and cannot produce a scientific verdict. Full execution starts only after all
tests and smoke gates pass.

Stop only for implementation/data corruption, missing artifacts, non-finite
loss, invalid resource identity, or overwrite risk. A scientifically negative
Oracle result is not a stop condition. No commit, push, root-sync publication,
or external handoff is authorized.

## 12. Protocol Freeze And Amendments

The scientific body is frozen before the first full run. Any later change to
data, labels, condition logic, loss, architecture, seeds, metric, threshold,
checkpoint selection, or exclusion rule requires an append-only amendment with
before/after values, timing, reason, human approval, and evidence-eligibility
effect. Execution receipts and result links may be appended without reopening
the design.
