# Protocol: A15_13_E05 CLINC150 Frozen-Base Staged Semantic LoRA Router

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL_RUN
Approval status: direct researcher authorization on 2026-08-31; no additional approval checkpoint requested
Block audit status: A-G CONFIRMED under the researcher's delegated exact-design authority
Cross-block consistency: PASS
Execution scope approved: Focus/Anchor/Protocol update, implementation, tests, smoke, single-node 4xH100 reserved full run, monitoring, analysis, figures, summary, and detailed record
Design frozen at: before the first E05 smoke execution
Purpose: test whether frozen base-model semantics can seed a functional staged coarse-to-fine LoRA Router on real natural-language intents
Primary Anchor: A15_13_02 frozen-base staged semantic LoRA Router
Anchor decision question: can frozen-base semantic partitions guide coarse routing and then fixed-parent fine routing without a trained teacher?
Anchor physical prior tested: domain meaning can be learned first and preserved while local intent distinctions are learned inside each domain
Anchor core model term tested: fixed coarse Router followed by native or coarse-row-space-removed child routing
Anchor falsifier: gold hierarchy fails to beat task-only hierarchy, or pseudo hierarchy fails to recover a positive fraction with functional utility
Experiment role: method construction and mechanism falsification
Primary metric from Anchor: Oracle-relative recovery of held-out domain-local fine-intent linear-probe macro F1
Claim boundary from Anchor: one frozen 0.6B model, one layer, balanced English intent classification, fixed precomputed labels
Minimal setup: official CLINC150, Qwen3-0.6B-Base frozen, sequence-level Router, rank-8 shared/parent/child LoRA at block-index-14 MLP down projection, two seeds
Treatment: train coarse Router and parent experts, fix the coarse Router, then train parent-conditional fine Routers and child experts
Controls: frozen Base, Dense LoRA, flat task-only, flat Oracle, flat spherical-cluster supervision, hierarchical task-only, shuffled hierarchy, gold hierarchy, and three pseudo-label hierarchies
Changed variable: route-label source, flat versus staged topology, parent-expert freeze, and child-Router representation
Held fixed: data, split, base weights, intervention layer, active rank, task head, optimizer family, epoch budget, seeds, checkpoint rule, and analysis
Conditions to run: 10 core conditions plus the complete Oracle and spherical-cluster 2x2 matrices, 16 final conditions per seed and 32 paired final runs total
Pass: admissible Oracle upper bound; primary spherical-cluster recovery positive in both seeds with pooled interval above zero; task guard passes; selective expert utility gate WORK
Fail: admissible Oracle but primary pseudo effect is non-positive in both seeds or pooled upper bound is at most zero, or selective expert utility gate NOT WORK
Insufficient: Oracle denominator invalid, seed directions unresolved, data/freeze/gradient/resource/completion guard fails, or required artifact is missing
Cannot claim: open-domain discovery, generative-task improvement, base-parameter shaping, dynamic online labels, token-level routing, compute efficiency, or MASSIVE transfer
Approval decision: execute all registered conditions even when Oracle or an earlier gate fails; gates constrain interpretation, not completion
```

The confirmed active Focus is [the A15_13 Focus](../../../../../../../daily_research_reports/backup/2026/08/0830/focus_semantic_supervision_middle_layer_separability.md). The scientific owner is [A15_13_02](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_02_frozen_base_staged_semantic_lora_router_anchor.md).

## 1. Terminology / Definitions

- **Frozen-base semantic label:** a route label fitted only from Qwen3-0.6B-Base final-layer training representations. No Qwen weight or label generator is trained.
- **Coarse label:** one of 10 domains for gold supervision or one of 10 frozen clusters for pseudo supervision.
- **Fine label:** one of 15 intents inside a parent for gold supervision or one of 15 frozen child clusters fitted inside a pseudo parent.
- **Sequence-level Router:** one probability vector per utterance, computed from its last non-padding input state, controls the low-rank expert choice for the full utterance.
- **Low-rank expert (LoRA expert):** a trainable rank-8 update \(BA\) added to the frozen MLP down projection. One shared update is always active; a flat condition activates two experts, while a hierarchy activates one parent and one child.
- **Native fine-Router representation:** the frozen block input \(h\).
- **Coarse-removed fine-Router representation:** \((I-P_c)h\), where \(P_c\) projects onto the centered row space of the fixed coarse Router. Only the child Router reads this state.
- **Selective expert utility:** the task-loss increase from deleting the matched expert minus the average increase from deleting non-matched experts. It is a WORK/NOT WORK eligibility gate, not the headline comparison.
- **Oracle recovery:** the fraction of the gold-supervision improvement over task-only routing reproduced by pseudo supervision. It is undefined when Oracle does not improve in the registered direction.

Condition labels are descriptive aliases defined in Section 9; they never denote datasets.

## 2. Anchor Alignment

The experiment keeps the parent problem unchanged: high-layer semantic organization may guide newly added middle-layer computation. It changes the failed E03 operationalization by removing trained-teacher posteriors, using actual low-rank experts, applying semantic loss only to Routers, and completing the registered freeze/removal mechanism audit. The strongest rival remains generic task adaptation or label-shaped routing without functional specialization.

## 3. Tested Hypothesis

First, the gold two-stage hierarchy must improve held-out effective-representation accessibility over the architecture-identical task-only hierarchy. Second, the primary frozen-base spherical-cluster hierarchy must reproduce a positive fraction of that improvement, preserve the task, show Oracle-directed routing entropy and semantic agreement, and pass selective expert deletion. Gaussian-mixture and von Mises--Fisher labels test whether the conclusion depends on the spherical-cluster assumption.

## 4. Rival Explanations

| Rival | Separating evidence |
| --- | --- |
| Any post-training helps | frozen Base and Dense LoRA |
| Any added expert capacity helps | flat and hierarchical task-only controls |
| Any fixed partition helps | frequency-matched shuffled hierarchy |
| Semantic labels help but hierarchy does not | flat Oracle and flat spherical-cluster controls |
| Geometry changes without function | selective expert deletion and expert swap |
| Entropy looks healthy but routes are non-semantic | gold-conditional entropy, mutual information, and adjusted Rand index |
| Removing coarse information is unnecessary or harmful | native versus coarse-removed child-Router input |
| Freezing the parent expert, rather than only its route, causes the effect | parent-expert trainable versus frozen |

## 5. Data Construction And Provenance

Source is the verified local official CLINC150 snapshot:

```text
/data/250010109/MoE_Router/data_sources/clinc_oos_eval_828f8093932c/data/data_full.json
/data/250010109/MoE_Router/data_sources/clinc_oos_eval_828f8093932c/data/domains.json
```

Only in-scope `train`, `val`, and `test` rows are used. Raw counts are 15,000, 3,000, and 4,500. The previously verified train-priority exact-normalized-text filter removes three later development rows and two later test rows, producing 15,000 TRAIN, 2,997 DEVELOPMENT, and 4,498 CONFIRMATION examples. Each of 150 intents maps to exactly one of 10 domains, with 15 intents per domain and balanced raw class counts.

One example contains only the English utterance as operational input. Its fine-intent label trains the common task head. Domain and intent labels may train only Oracle Routers and evaluation probes. Pseudo labels may use only frozen-base TRAIN representations. DEVELOPMENT labels select checkpoints and probe regularization. CONFIRMATION truth is forbidden from clustering, training, checkpoint selection, thresholds, label naming, and condition selection.

Preflight requires source hashes, exact counts, exactly five registered cross-split duplicates before filtering, zero overlap afterward, complete domain--intent mapping, maximum token length at most 96, and no label string rendered in the input.

## 6. Learning Task And Permitted Supervision

Given one utterance, the post-trained system predicts one of 150 natural-language intents from the final last-non-padding hidden state. The task objective is 150-way cross entropy. This is a natural-language semantic classification task, not open-ended generation.

All conditions may use TRAIN intent labels for the common task objective. Only Oracle Routers may use TRAIN domain or intent labels as route targets. Pseudo Routers use frozen cluster assignments. Task-only Routers receive no route-label loss. No condition reads CONFIRMATION labels before unsealing.

## 7. Model / Architecture And Frozen Variants

- Base: official `Qwen/Qwen3-0.6B-Base`, BF16, all original parameters frozen.
- Intervention: the MLP `down_proj` in zero-indexed block 14.
- Router input: last non-padding state entering block 14, centered using TRAIN statistics.
- Common head: trainable linear 1024-to-150 intent classifier over the final last-non-padding state.
- Shared expert: rank-8 LoRA, active for every sample.
- Parent experts: ten rank-8 LoRA updates, sequence-level hard top-1 with straight-through probability scaling.
- Child experts: fifteen rank-8 LoRA updates per parent, one active child per sample.
- Flat experts: 150 rank-8 LoRA updates with two active experts, so shared plus two expert ranks matches the hierarchy's shared plus parent plus child active rank of 24.
- Dense control: one rank-24 LoRA update and the same task head.

The base transformation remains frozen. Route cross entropy terminates at Router parameters. Task cross entropy updates the head, shared LoRA, and selected experts. In stage two the coarse Router is always fixed. The parent expert bank is either trainable or frozen according to the \(2\times2\) matrix. Parent and child experts both read the native MLP activation; only the child Router input changes between native and coarse-removed variants.

## 8. Training Objective And Optimization

For task label \(y\), route label \(z\), and Router distribution \(p\), the loss is

\[
L=L_{\mathrm{task}}+\lambda_{\mathrm{route}}L_{\mathrm{route}},
\qquad
L_{\mathrm{task}}=\operatorname{CE}(y,\hat y),
\qquad
L_{\mathrm{route}}=\operatorname{CE}(z,p).
\]

\(\lambda_{\mathrm{route}}=1\). No load-balancing, contrastive, prototype, reconstruction, margin, or expert classification loss is permitted. The task loss is averaged per utterance; the route loss is averaged over labeled utterances. Route loss updates only Router parameters.

All trainable modules use AdamW, learning rate \(3\times10^{-4}\) for LoRA and Routers, \(10^{-3}\) for the task head, weight decay 0.01, global batch 256, BF16, gradient norm 1.0, 5% linear warmup, and cosine decay within each stage. Stage one runs two complete TRAIN epochs. Stage two starts from the selected stage-one checkpoint and runs two complete TRAIN epochs. Dense and flat baselines run four complete epochs to match total data passes. DEVELOPMENT intent macro F1 selects a checkpoint within each stage; ties use lower development cross entropy and then earlier step. No early stop shortens a registered run.

## 9. Conditions, Seeds, And Checkpoints

Seeds are 17 and 29. Every condition uses the same initialization family and shuffled-example order within a seed. Stage-one checkpoints are reused by all of their registered stage-two branches.

### Core conditions

| Condition | Label source | Topology | Role |
| --- | --- | --- | --- |
| `BASE_FROZEN` | none | no added module | no-post-training reference |
| `DENSE_R24` | task only | one rank-24 LoRA | ordinary parameter-efficient post-training |
| `FLAT_TASK` | none | shared plus flat top-2 | capacity/topology control |
| `FLAT_ORACLE` | gold fine intent | shared plus flat top-2 | flat semantic upper control |
| `FLAT_SKM` | global 150-way spherical clusters | shared plus flat top-2 | flat pseudo-label control |
| `HIER_TASK` | none | ten parents then 10x15 children | task-gradient hierarchy control |
| `HIER_SHUFFLED` | frequency-matched shuffled gold hierarchy | staged hierarchy | fixed-partition negative control |
| `HIER_ORACLE_F1_R1` | gold domain and intent | staged hierarchy | gold upper bound and main mechanism cell |
| `HIER_SKM_F1_R1` | spherical K-means | staged hierarchy | primary self-supervised treatment |
| `HIER_GMM_F1_R1` | diagonal Gaussian mixture | staged hierarchy | density-shape label control |
| `HIER_VMF_F1_R1` | shared-concentration von Mises--Fisher mixture | staged hierarchy | directional soft-cluster control |

`F1` means parent experts are frozen in stage two. `R1` means the child Router reads the coarse-removed representation.

### Complete \(2\times2\) mechanism matrices

Both Oracle and spherical-cluster supervision run all cells:

| Parent expert in stage two | Child Router input | Suffix |
| --- | --- | --- |
| trainable | native | `F0_R0` |
| trainable | coarse-removed | `F0_R1` |
| frozen | native | `F1_R0` |
| frozen | coarse-removed | `F1_R1` |

The two main `F1_R1` conditions already appear in the core table. Adding the other six cells yields 16 final conditions per seed and 32 final runs. `BASE_FROZEN` is evaluated once per seed without optimization.

## 10. Frozen Clustering And Analysis Plan

The frozen base model first produces final-layer last-non-padding TRAIN vectors. A deterministic TRAIN-only 128-component principal-component view is fitted once and reused for all three methods; its outputs are L2 normalized for the directional methods. DEVELOPMENT and CONFIRMATION use the frozen projection. This common view controls clustering cost and prevents method-specific access to different base representations.

1. **Spherical K-means:** 10 coarse clusters and, within each coarse cluster, 15 child clusters; use exact ten-restart K-means for local partitions and five-restart mini-batch K-means for the 15,000-row or 150-way fits; choose the largest training objective without gold labels.
2. **Diagonal Gaussian mixture:** diagonal-covariance mixtures on the common 128-component view with the same 10 then 15 cardinalities; choose the largest training likelihood.
3. **Shared-concentration von Mises--Fisher mixture:** soft expectation-maximization on unit vectors with fixed concentration 100, learned mixture weights and directions, the same 10 then 15 cardinalities, and largest training likelihood selection.

All methods fit TRAIN only and assign later splits by frozen centers or posterior maximum. The entrance report includes restart adjusted mutual information, smallest/largest cluster fraction, normalized load entropy, and effective cluster count. Exact gold alignment is opened only after label objects and hashes freeze. A collapsed method remains in the full-run matrix but its semantic interpretation is ineligible.

For each final condition, extract TRAIN, DEVELOPMENT, and CONFIRMATION states at four objects: native block output, shared residual, selected parent residual, selected child residual, and their effective sum. Fit ten separate 15-way multinomial linear probes on TRAIN states; DEVELOPMENT selects regularization from `C={0.01,0.1,1,10}`; evaluate once on CONFIRMATION and average domains equally.

The primary estimand is spherical-cluster minus task-only domain-local probe macro F1, plus its Oracle recovery ratio. A paired stratified bootstrap with 10,000 draws resamples CONFIRMATION utterances within true intent and reports a pooled two-sided 95% percentile interval. Both seed effects must be positive and the pooled lower bound must exceed zero.

## 11. Secondary Metrics And Guards

### Routing, reported first

- Mean per-example normalized Router entropy: confidence, not semantic correctness.
- Normalized dataset load entropy and maximum expert fraction: collapse and utilization.
- Gold-conditional route entropy \(H(E\mid D)\) for coarse and \(H(E\mid Y,D)\) for fine routing: consistency within true semantic groups.
- Normalized mutual information, adjusted Rand index, and Hungarian-matched macro F1 against gold labels: semantic alignment, evaluation only.
- Jensen--Shannon divergence between pseudo and Oracle expert-load vectors: load-shape gap.

### Task and representation

- CONFIRMATION intent macro F1, cross entropy, per-domain macro F1, and worst-domain F1.
- Domain-local 5-nearest-neighbor macro F1 and fifth-percentile normalized nearest-centroid margin.
- X-MoE representation-collapse statistic \(\operatorname{Tr}(\Sigma_W\Sigma_B^\dagger)\), covariance effective rank, and top-10 eigenvalue mass.
- Frozen-before-training linear readout transfer and retrained linear probe are reported separately.
- Pairwise principal angles and cosine similarity among parent and child LoRA residual subspaces.

### Functional eligibility gate

For each of the ten parent experts in the main Oracle and spherical-cluster conditions, compute confirmation task-loss increase \(\Delta_e(c)\) after deleting that parent expert while preserving every other component. Pseudo experts are matched to gold domains once by TRAIN Hungarian assignment. The selective score is the matched-domain increase minus the mean non-matched-domain increase. `WORK` requires positive mean parent selectivity in both seeds and a positive pooled paired bootstrap lower bound. Active-child deletion and within-parent wrong-child swap are supporting fine-level diagnostics; they do not replace the registered parent-expert gate. A failure cannot be rescued by routing or geometry.

Task preservation requires no condition interpreted as positive to lose more than one intent macro-F1 percentage point versus `DENSE_R24` in either seed.

## 12. Known Good / Known Bad / Known Confusing Cases

- Known good: one small batch must reach at least 99% task accuracy and at least 99% supervised Router accuracy; every non-base condition must change the targeted block state from the zero-LoRA identity.
- Known bad: frequency-matched shuffled labels must not acquire stable gold mutual information above the 97.5th percentile of 1,000 label permutations.
- Known confusing: card-payment cancellation/refund, transfer/routing, and yes/no/maybe intents are audited as fixed groups but never tune the model.
- Identity guard: zero-initialized LoRA modules reproduce frozen-base logits within \(10^{-5}\) FP32 and \(5\times10^{-3}\) BF16.
- Freeze guard: base gradients are absent; stage-two coarse Router gradients are absent; parent-expert gradients match the registered freeze cell; route loss never creates expert gradients.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input and operation | Output | Stop rule and handoff |
| --- | --- | --- | --- | --- |
| P0 | validate the real hierarchy | hash, deduplicate, tokenize, and audit official CLINC150 | immutable data manifest | schema, overlap, mapping, or token guard failure stops execution |
| P1 | construct frozen semantic signals | extract untouched base final states and fit all registered cluster methods | frozen labels, models, hashes, entrance report | nonfinite or missing assignments stop; collapse is recorded but does not cancel full runs |
| P2 | validate implementation | identity, gradient-locality, stage handoff, de-common projector, overfit, checkpoint reload, and metric tests | smoke and gradient ledger | any implementation failure stops scale-up |
| P3 | learn coarse routing | two epochs for every staged label source and seed | selected coarse Router/parent-expert checkpoints | all registered checkpoints continue to P4 even if scientific gates fail |
| P4 | learn fine routing | branch each coarse checkpoint into registered core and 2x2 conditions for two epochs | all final checkpoints and histories | missing arm or invalid freeze makes the relevant paired result Insufficient |
| P5 | run matched baselines | four epochs for Dense and flat controls | baseline checkpoints | active-rank or data-order mismatch is ineligible |
| P6 | freeze and unseal | select on DEVELOPMENT, freeze hashes, evaluate CONFIRMATION once | task, routing, utility, and representation source tables | no result-derived rerun or threshold change |
| P7 | aggregate and render | paired bootstrap, Oracle recovery, entropy panels, representation and utility figures | aggregate JSON, tables, figures, completion audit | missing lineage blocks final interpretation |

## 14. Algorithm, Output, And Provenance Contract

Worker implementation and raw outputs live at:

```text
/data/250010109/MoE_Router/experiments/20260831_a15_13_e05_clinc150_frozen_base_staged_semantic_lora_router
```

Canonical records and curated figures live beside this Protocol. The worker records source, code, configuration, environment, model, cluster-label, checkpoint, analysis, and completion hashes.

The only approved resource tuple is the researcher-selected override:

```text
resource_profile=h100-4-reserved
execution_surface=ACP
workspace=share-space
aec2_cluster=share-cluster
worker_spec=n6ls.iu.i40.4
worker_nodes=1
quota_type=reserved
priority=normal
visible_gpus=4
processes=4
automatic_fallback=forbidden
```

Four processes execute independent condition shards; this is not a multi-node or data-parallel scientific change. Checkpoints are written after every epoch so an infrastructure retry can resume the same frozen condition without changing data order or analysis.

## 15. Success / Failure / Insufficient Evidence

- **Pass:** Oracle is admissible; primary pseudo recovery is positive in both seeds with pooled interval above zero; task guard passes; functional gate is `WORK`.
- **Fail--architecture:** gold hierarchy does not improve over task-only with valid guards. Pseudo results remain descriptive only.
- **Fail--semantic entrance:** gold hierarchy works, but every pseudo method has non-positive recovery or collapsed/non-semantic routing.
- **Fail--functional specialization:** routing or representation improves but selective expert utility is `NOT WORK`.
- **Insufficient:** registered paired evidence, denominator, implementation, resource, completion, or confirmation boundary is invalid.

All conditions still run when an earlier scientific gate fails, as explicitly requested; the gate changes interpretation only.

## 16. What This Cannot Claim

The experiment cannot establish that CLINC150 intent labels exhaust natural-language semantics, that the original Qwen representation was changed, that cluster IDs have human meaning without evaluation, that the method helps generation, that two stages are compute-optimal, that labels can refresh online, or that results transfer to MASSIVE or token-level slot routing.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding |
| --- | --- | --- |
| A Question and boundary | CONFIRMED | researcher final confirmation |
| B Data and provenance | CONFIRMED | researcher required a new natural-language hierarchy; verified CLINC150 E03 source |
| C Task and supervision | CONFIRMED | researcher approved gold and learned labels, no new teacher |
| D Architecture | CONFIRMED | researcher approved staged coarse freeze, fine learning, and 2x2 audit |
| E Objective and optimization | CONFIRMED | delegated exact design; route-only semantic loss and task CE preserve meeting mechanism |
| F comparisons and evidence | CONFIRMED | researcher required complete Baselines, multiple clustering methods, Oracle comparison, entropy, utility gate, and representation analysis |
| G execution | CONFIRMED | researcher explicitly approved implementation, smoke, full run, analysis, and 4xH100 reserved |

Cross-block consistency: `PASS`. Confirmation truth cannot enter fitting or selection. The scientific body freezes at first E05 smoke. Any later material correction is append-only and states evidence eligibility.

## 18. Post-Execution Amendment And Deviation Ledger

This section is append-only. It records what actually ran; it does not rewrite the frozen scientific contract.

| Time / scope | Event | Scientific effect |
| --- | --- | --- |
| 2026-08-31, smoke | Reserved single-node `n6ls.iu.i40.4` smoke job `pt-jtr051b5` completed on four H100 80GB devices. | Execution surface and four-process sharding were validated. |
| 2026-08-31, full run | Jobs `pt-ipyrra1g` and `pt-5ueee3w7` jointly completed the same resumable run root: 12 stage-one checkpoints, all 32 final condition-by-seed runs, and four parent-utility artifacts. | The full registered matrix is complete. The first job stopped after 24 final runs when a flat pseudo-label array reached CUDA cross entropy as `int32`; the correction converted labels to `int64` and was regression-tested before only the missing conditions resumed. No completed arm was retrained under a different scientific setting. |
| 2026-08-31, analysis | Analysis-only jobs `pt-qhl55aor` and `pt-96zomcq7` exposed a missing analysis-directory creation bug; `pt-a17pcesk` completed the corrected parallel analysis. Post-analysis job `pt-le90locj` exposed an invalid comparison between 150-way flat load vectors and 10-way hierarchical load vectors; `pt-bf27nzku` completed the separated flat/hierarchical analysis. | These were artifact-generation and metric-domain corrections. They did not change checkpoints, labels, or registered condition selection. The final aggregate uses intent-stratified confirmation bootstrap and applies the task guard. |
| Actual Router input | The implementation fed the uncentered frozen block input to every Router. The coarse-row-space-removal projector was built from centered coarse-Router rows. | This is a common implementation deviation from the centered-input sentence in Section 7. Results adjudicate the uncentered Router-input variant only. |
| GMM secondary method | The diagonal Gaussian mixture used a method-specific whitened 64-dimensional principal-component view after the registered common 128-dimensional view. | GMM remains a secondary shape diagnostic and cannot support a method-ranking claim against spherical methods. |
| vMF audit value | The recorded vMF restart objective omitted a common per-row maximum-logit offset. Assignments are unchanged, and no result-dependent restart was selected, but the stored absolute objective values are not interpretable as likelihoods. | vMF labels and runs remain descriptive; objective-value comparisons are ineligible. |
| P2 overfit guard | Identity, gradient locality, freeze, checkpoint, metric, smoke, and full learning guards ran; the literal one-small-batch 99% overfit test was not separately executed. | The completed runs demonstrate task and supervised Router learning, but the protocol-specific 99% assertion is not claimed. |
| Provenance | The worker directory was not a Git repository and no immutable pre-run code snapshot was made. Current source hashes are post-run hashes; the execution chronology records the tested dtype and analysis fixes. | Raw artifacts and commands remain auditable, but exact source reconstruction is weaker than a committed worker revision. This limits reproducibility claims, not the stored numeric result. |
| Supporting diagnostics | Child deletion/swap, residual-norm decomposition, principal angles, frozen-readout transfer, 5-nearest-neighbor accuracy, and the 2x2 delta plot were completed after the registered primary aggregate. | These diagnostics explain the registered verdict but cannot rescue it or redefine the primary endpoint. |

Final machine completion state: `32/32 final runs complete`, `completion_audit.complete=true`, and all required final, stage-one, utility, aggregate, representation, diagnostic, and figure artifacts are present. Final registered machine verdict: `INSUFFICIENT_ORACLE`. Research interpretation remains `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION` until the researcher supplies or approves the closed-book result, boundary, and next decision.
