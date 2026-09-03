---
experiment_id: A15_08_02_E01_layerwise_conditional_fine_added_accessibility
status: COMPLETED_2026-08-16
anchor: ../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_02_layerwise_conditional_fine_added_accessibility_anchor.md
created: 2026-08-16
updated: 2026-08-16
execution_authority: FULL_LOCAL_EXECUTION_APPROVED_2026-08-16
---

# Protocol: A15_08_02_E01 Layerwise Conditional-Fine Added Accessibility

## 0. Approval Snapshot

- **One decision question:** across eligible Qwen3-8B blocks, which same-token normalized attention transitions add held-out within-parent child accessibility beyond an identical old-state branch and target-independent equal-budget controls?
- **Execution shape:** after one explicit full-run approval, run model-independent preflight and then directly process blocks 1--36 in forward order; there is no single-block model smoke.
- **Scientific stage:** freeze every TRAIN/DEVELOPMENT choice for all eligible blocks, then evaluate once on fresh CONFIRMATION if the internal gate passes.
- **Primary output:** the signed all-layer curve $T_\ell$ and the simultaneous-positive set $\mathcal L^+$.
- **Not in scope:** covariance/PCA, public basis, clustering, low-rank retrieval, Router, experts, or training the base language model.

This file is the single canonical execution contract. The researcher explicitly waived the earlier block-25 smoke on 2026-08-16. Synthetic known cases and extraction-identity preflight remain mandatory, but a valid preflight continues directly into the registered all-block run under one later execution approval.

### 0.1 Audit blocks A--G

| Block | Contract owned here | Draft state | What is still required |
| --- | --- | --- | --- |
| A — question/hypothesis | one decision question, H-CF, R-CAP, Pass/Fail/Insufficient | `CONFIRMED` | accepted 2026-08-16 |
| B — data/provenance | existing TAX TRAIN/DEVELOPMENT plus fresh disjoint CONFIRMATION | `CONFIRMED` | fresh manifest/hash still must pass preflight |
| C — model/object | frozen Qwen3-8B; exact $X,Z,U,R_U$ at one decision token | `CONFIRMED` | implementation identity receipts still must pass |
| D — learning/control | same-$X$ base-plus-correction ridge; duplicate-$X$ and 64 mismatch banks | `CONFIRMED` | accepted 2026-08-16 |
| E — evaluation | signed $T_\ell$, simultaneous intervals, capability and leakage guards | `CONFIRMED` | seeds freeze before confirmation access |
| F — analysis/artifacts | all-layer positive-gain figure contract, exact arrays and tables | `CONFIRMED` | accepted 2026-08-16 |
| G — execution/resources | direct blocks 1--36 after model-independent preflight; no block-25 smoke | `CONFIRMED` | one local H100 MIG 3g.40GB; no cloud submission |

**Cross-block state:** `PASS_FOR_CONFIRMED_A_TO_G`.

**Current authorization:** the researcher explicitly authorized all experiments on 2026-08-16. This enters `APPROVED_FOR_IMPLEMENTATION_AND_FULL_FROZEN_ALL_LAYER_RUN` and covers fresh-data construction, implementation, model-independent preflight, direct all-layer extraction/fitting, one-shot CONFIRMATION, and result finalization. Experiment two retains its own Protocol and verdict.

### 0.2 Approval phrases and scope

The only execution approval phrase is:

| Ledger phrase | Authorized scope |
| --- | --- |
| `APPROVED_FOR_IMPLEMENTATION_AND_FULL_FROZEN_ALL_LAYER_RUN` | implement, pass model-independent preflight, process blocks 1--36, freeze all TRAIN/DEVELOPMENT choices, then run one-shot fresh CONFIRMATION only if the internal gate passes |

The phrase authorizes the complete registered functional experiment. The same user turn separately authorizes experiment two's low-rank/parameter-spectrum analysis, but experiment two remains isolated in its own Protocol and cannot alter this verdict. Commit, push, and external publication remain outside scope. Any failed preflight is recorded; a locally ineligible block does not cancel the separately approved experiment-two geometry analysis.

### 0.3 Pre-confirmation implementation amendment A1

The execution audit found that Section 8.3 used the phrase “multinomial cross-entropy plus L2” while the approved A15 linear-readout family and the rest of this Protocol repeatedly specify **ridge** readouts. Before any fresh CONFIRMATION construction or access, A1 freezes the actual estimator as follows:

- fit centered one-hot targets with linear L2 ridge in the primal/dual form;
- choose each branch's ridge coefficient independently by equal-parent DEVELOPMENT cross-entropy;
- keep the old-state base logits frozen while fitting correction targets against out-of-fold TRAIN base logits;
- use the identical estimator, grid, folds, row counts, parent weights, and selection budget for true, duplicate-$X$, and all mismatch branches.

This amendment changes no object, split, branch, control, target, primary metric, uncertainty rule, or Pass/Fail boundary. It removes an objective-family inconsistency and makes the estimator identical to the established A15 “linear ridge readout” meaning. The amendment is frozen before implementation tests and confirmation access.

The researcher's blanket execution authorization also delegates the ten-example fresh-data quality audit to the executing agent. The audit packet must preserve the exact ten stratified examples, duplicate/label/tokenization scans, counts, hashes, and an explicit `AI_EXECUTION_AUDIT_UNDER_RESEARCHER_AUTHORITY` marker; it cannot inspect model representations, losses, or layer curves.

## 1. Terminology And Definitions

- **Parent:** the known coarse taxonomy class, such as mathematics.
- **Child:** one of eight fine classes inside a parent, such as combinatorics or linear algebra.
- **Conditional-fine task:** parent identity is metadata known to the evaluator; the readout chooses one of the eight children inside that parent.
- **Decision token:** the final token occurrence in the frozen prompt immediately after `Classification:`. The same occurrence is used for every layer and sample.
- **Old state $X_\ell$:** the block-$\ell$ post-attention RMSNorm applied to the actual pre-attention residual without adding the current attention write.
- **Actual state $Z_\ell$:** the same RMSNorm applied after adding the current attention write; this is the actual MLP input.
- **Exact update $U_\ell$:** $Z_\ell-X_\ell$ in one shared coordinate.
- **Residual update $R_{U,\ell}$:** the part of $U_\ell$ not recovered by the registered TRAIN-only linear predictor from $X_\ell$.
- **Base logits:** parent-specific logits produced from $X_\ell$ once and frozen for all branches.
- **Correction:** an additive eight-logit vector learned from the true or control correction input while the base is frozen.
- **Added accessibility:** held-out base CE minus held-out base-plus-correction CE, in nats/example.
- **Matched excess $T_\ell$:** true residual-update gain beyond the stronger of duplicate-$X$ gain and the q95 mismatch-bank gain.
- **Preflight:** model-independent known cases, schema checks, and extraction identities that must pass before all-block scientific computation. It has no scientific Pass/Fail.
- **Eligible block:** a block that passes state-scale, extraction-identity, sample-count, fit, and control-validity guards.

“Positive-gain plot” in this Protocol means a plot designed to locate positive gains: it must show every eligible signed estimate and cannot clip negative values or display only selected layers.

## 2. Anchor Alignment

The [Anchor](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_02_layerwise_conditional_fine_added_accessibility_anchor.md) separates three questions:

1. Does a layer update add conditional-fine accessibility beyond its old state? **Owned here.**
2. Can the admitted gain be retained in a low-dimensional space? **Blocked until this experiment passes.**
3. Does such a space improve routing or expert utility? **Not owned here.**

The two broad research hypotheses — deeper cumulative states distinguish finer information and useful new representation may be low rank — motivate the line but are not silently converted into the present verdict. This experiment does not require a monotonic depth law and performs no rank analysis.

## 3. Tested Hypothesis

**H-CF — layer-local conditional-fine added accessibility.** With valid capability and audit guards, at least one eligible block has

$$
\operatorname{LCB}^{sim}_{0.95}(T_\ell)>0.
$$

Define

$$
\mathcal L^+=\{\ell:\operatorname{LCB}^{sim}_{0.95}(T_\ell)>0\}.
$$

Only $\mathcal L^+$ is admitted to a later low-rank experiment. The experiment does not hypothesize in advance that block 25 is positive or that $T_\ell$ grows monotonically with depth.

## 4. Rival Explanations

| Rival | Registered separator | Required reading if separator wins |
| --- | --- | --- |
| old-only readout is underfit | duplicate-$X$ staged correction with the same frozen base and budget | extra correction headroom, not new input |
| any same-dimensional update helps | 64 balanced, sample-level, within-parent mismatch banks | generic correction capacity or nuisance geometry |
| update is predictable from old state | TRAIN-only grouped residualizer $U\sim X$ | redundant linear re-encoding is removed under the registered family |
| templates or content leak child identity | split-disjoint expression/content/template families and grouped resampling | leakage makes verdict Insufficient |
| target task is not linearly accessible | full-$Z$ and final-layer capability guards | inability makes novelty verdict Insufficient |
| deeper layers have different old-state headroom | primary claim uses within-layer $T_\ell$; old-only CE shown beside each layer | raw cross-layer $G$ magnitudes are descriptive |
| block 1 has no sample variation | structural-constant check before standardization | mark x=1 `STRUCTURALLY_INELIGIBLE`, never force a fit |
| favorable layers are selected after viewing confirmation | all blocks, controls, seeds, axes, and simultaneous procedure frozen first | any selection leak makes verdict Insufficient |

## 5. Data Construction And Provenance

### 5.1 Frozen fitting population

Use only the TAX records from:

`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_01_10_e02_e03_tax_comp_10layer_full/data/taxonomy_full.json`

Registered SHA-256:

`ce91dbbd3c5071e17beeccf0d86a280dc8a3e48e0fdbf2178868da45eea18af4`

The file contains 1,920 records: 8 parents × 8 children × 30 expressions. This experiment uses only its 10 TRAIN and 10 DEVELOPMENT expressions per child, or 640 records per split. Its previously viewed CONFIRMATION records are excluded from every new verdict.

The frozen source properties are:

- eight parents and eight children per parent;
- six label-free fact atoms per child;
- split-disjoint five-template families;
- three facts selected by a deterministic split-specific schedule;
- prompts contain neither parent nor child label text as an answer shortcut;
- every prompt ends at the common `Classification:` readout.

### 5.2 AI_PROPOSAL: fresh scientific confirmation

Before full scientific execution, build exactly 640 new records:

$$
8\ \text{parents}\times8\ \text{children}\times10\ \text{expressions}=640.
$$

The child set and six source fact atoms remain fixed so the target definition is unchanged. New records must use ten expression/content instances per child whose full strings, selected three-fact combinations, ordering schedule, and template family are disjoint from the existing TRAIN and DEVELOPMENT records. No old CONFIRMATION wording may be copied.

Required fresh-confirmation fields:

`record_id`, `parent_id`, `child_id`, `semantic_family_id`, `template_family_id`, `fact_subset_id`, `text`, `split`, `decision_token_char_span`, `generator_version`, and `source_fact_version`.

The generated JSON, generator, configuration, and manifest receive SHA-256 hashes before any model extraction. Under Amendment A1, Block B moves to `CONFIRMED` only after the execution agent saves and inspects ten stratified examples plus class counts, duplicate scans, label-text scans, tokenization, and all hashes, marked `AI_EXECUTION_AUDIT_UNDER_RESEARCHER_AUTHORITY`. This audit cannot access representations, losses, or layer curves.

### 5.3 Independence and leakage units

- Training rows are individual expressions.
- Hyperparameter selection is grouped by `semantic_family_id`; related paraphrases cannot cross a fold boundary.
- Uncertainty uses parent as the outer resampling unit and semantic family inside parent as the inner unit.
- Parent and child receive equal weight regardless of record ordering.
- Confirmation labels, losses, representations, and even aggregate layer curves remain closed until the selection-freeze receipt exists.

### 5.4 Data preflight

The implementation must stop before a model forward unless all checks pass:

1. exact counts and balance by split/parent/child;
2. source file and generator hashes;
3. no exact or normalized-text duplicates across splits;
4. no `semantic_family_id` or `template_family_id` overlap across fitting and fresh confirmation;
5. no parent/child label string in the prompt body;
6. one and only one frozen `Classification:` decision-token occurrence;
7. stable tokenization and no truncation;
8. all fresh confirmation rows remain unread by fitting/selection code paths.

## 6. Learning Task And Permitted Supervision

For every block and parent, fit an eight-class additive-logit model. Parent identity selects the parent-specific readout but is not predicted and is not inserted as a target-bearing prompt suffix.

Permitted supervision:

| Split | Permitted use |
| --- | --- |
| TRAIN | standardization, residualizer fitting/cross-fitting, base and correction fitting, mismatch-map construction |
| DEVELOPMENT | ridge selection and guard thresholds frozen before confirmation |
| fresh CONFIRMATION | one final evaluation under the frozen all-layer design |

Forbidden uses of fresh CONFIRMATION include choosing a layer, regularization, mismatch seed, curve range, y-axis, confidence procedure, capability threshold, early stopping, rank, subspace, or wording.

## 7. Model, Architecture, And Frozen Variants

- Model: frozen `/data/share/Qwen3-8B`.
- Tokenizer and model revision: resolved local hashes must be written into the run manifest.
- Architecture expectation: hidden width $d=4096$, 36 transformer blocks; implementation must verify rather than assume.
- Forward: evaluation mode, no gradient, deterministic attention backend recorded, bfloat16 model forward with saved analysis arrays promoted to float32.
- Token site: final token occurrence after `Classification:`.
- Blocks recorded: 1--36.
- Science-eligible expectation: 2--36, conditional on guards.

At block $\ell$ save, for every record and the same token:

- $h_\ell$: actual pre-attention block residual;
- $a_\ell$: attention output after output projection and before residual addition;
- $X_\ell=N_\ell(h_\ell)$;
- $Z_\ell=N_\ell(h_\ell+a_\ell)$;
- $U_\ell=Z_\ell-X_\ell$;
- actual post-attention MLP input from the native forward;
- full block output $H_\ell$ as a capability diagnostic only.

Mandatory identities use float32 recomputation and registered tolerances frozen during implementation tests:

$$
\|Z_\ell-X_\ell-U_\ell\|,
$$

native MLP input versus $Z_\ell$, attention output-projection replay versus $a_\ell$, repeated-first-batch determinism, sample ID order, token ID, and token occurrence. A failure makes the affected block ineligible and blocks confirmation if systematic.

Block 1 receives no artificial standardization. `AI_PROPOSAL`: if every feature of $X_1$ has TRAIN standard deviation below $10^{-8}$ after float32 loading, record `STRUCTURALLY_INELIGIBLE_CONSTANT_X`; show x=1 as NA.

## 8. Training Objective And Optimization

### 8.1 Frozen standardization

For each block, fit TRAIN-only feature means and scales. Floors and zero-variance masks are frozen from TRAIN. Apply them unchanged to DEVELOPMENT and CONFIRMATION. Branches with the same input object reuse the same standardized arrays.

### 8.2 TRAIN-only residualizer

Fit a multi-output ridge map from $X_\ell$ to $U_\ell$ using five grouped TRAIN folds:

$$
\widehat m^U_\ell(X)\approx U_\ell.
$$

Each TRAIN row receives an out-of-fold residual. DEVELOPMENT and CONFIRMATION residuals use the predictor refit on all TRAIN rows after the residualizer ridge is selected on DEVELOPMENT. No parent or child target label enters the residualizer.

### 8.3 Same-$X$ dual branch

For parent $p$, fit the base ridge logits from $X$ on TRAIN and select its penalty on DEVELOPMENT:

$$
s^0_{\ell,i}=b_{\ell,p(i)}(X_{\ell,i}).
$$

Freeze these base logits. Do not refit or jointly optimize the base in any added branch.

Fit three linear ridge correction families while holding $s^0$ fixed:

$$
s^{true}=s^0+q^{true}(R_U),
$$

$$
s^{dupX}=s^0+q^{dupX}(X),
$$

$$
s^{mis,b}=s^0+q^{mis,b}(\widetilde R_U^{\,b}),\quad b=1,\ldots,64.
$$

The fitting target is the centered one-hot child target minus the out-of-fold frozen-base TRAIN logits. Ridge minimizes squared target error plus L2 penalty; DEVELOPMENT cross-entropy of the resulting base-plus-correction logits selects the penalty. The base and every correction use the same candidate grid:

$$
\lambda\in\{10^{-4},10^{-3},10^{-2},10^{-1},1,10,100,1000\}.
$$

Select each branch's penalty independently by equal-parent DEVELOPMENT CE; break ties toward the larger penalty. Independent selection makes controls stronger, not weaker. The deterministic linear solve tolerance, primal/dual agreement tolerance, intercept convention, and numerical receipt must be frozen by tests before all-block execution.

### 8.4 Mismatch-bank construction

Freeze 64 seeds before any fit. For each seed and split, create a within-parent one-to-one reassignment of residual-update rows satisfying:

1. no row maps to itself;
2. every source row is used exactly once;
3. within each destination child, source-child counts differ by at most one;
4. the mapping is at sample level, not one deterministic child-to-child label map;
5. TRAIN, DEVELOPMENT, and CONFIRMATION maps are generated independently from IDs and the frozen seed;
6. no text, representation value, predicted logit, or confirmation label affects the mapping.

Every bank receives its own correction fit and DEVELOPMENT ridge selection. Save full maps and balance receipts.

## 9. Conditions, Seeds, And Checkpoints

| Item | Frozen contract |
| --- | --- |
| model seed | deterministic seed to be written before implementation preflight |
| mismatch banks | 64 explicit integer seeds, serialized before fitting |
| grouped folds | five explicit fold maps from TRAIN semantic-family IDs |
| bootstrap | 2,000 explicit seeds, serialized before confirmation access |
| blocks | record 1--36; expected science fit 2--36 |
| block execution order | 1--36 in forward order; block 1 may become structural NA only by the frozen guard |
| base/correction ridge grid | $10^{-4}$ through $10^3$ as listed above |
| prediction conditions | old-only, true $R_U$, duplicate $X$, 64 mismatched $R_U$, full $Z$ capability |
| selection checkpoint | all TRAIN/DEVELOPMENT fits and plot schemas frozen before confirmation |

Exact numeric seed lists are an implementation artifact, not chosen in this document. They must be generated once after implementation approval, committed to the run manifest, and never regenerated after seeing results.

## 10. Primary Metric And Frozen Analysis Plan

For record $i$ at layer $\ell$, define

$$
g^v_{\ell,i}=CE(s^0_{\ell,i},Y_i)-CE(s^v_{\ell,i},Y_i).
$$

Within a resampling draw, average expressions equally inside child, children equally inside parent, and parents equally overall:

$$
G^v_\ell=\mathbb E[g^v_{\ell,i}].
$$

For each paired draw, compute the mismatch-bank q95 across the 64 bank means and then

$$
T_\ell=G^{true}_\ell-
\max\{G^{dupX}_\ell,q_{0.95,b}(G^{mis,b}_\ell)\}.
$$

This order is mandatory: the control maximum is recomputed inside every paired resampling draw. Subtracting a point control and then bootstrapping only the true branch is forbidden.

### 10.1 Simultaneous intervals

Use 2,000 paired hierarchical bootstrap draws:

1. resample the eight parents with replacement;
2. inside each selected parent, resample semantic families with replacement;
3. keep the same draw across layers and all branches;
4. compute a max-statistic over every eligible layer for two-sided familywise 95% intervals.

The Protocol's positive layer set is

$$
\mathcal L^+=\{\ell:\operatorname{LCB}^{sim}_{0.95}(T_\ell)>0\}.
$$

Pointwise intervals may be supplied in tables but cannot define $\mathcal L^+$.

### 10.2 Why raw positive gain is not the verdict

$G^{true}_\ell>0$ only says an added correction reduces CE. It does not determine whether the reduction comes from target-aligned new input. $T_\ell$ subtracts the stronger registered capacity explanation while preserving the exact same base $X$ and logits.

### 10.3 Across-depth interpretation

The complete signed $T_\ell$ trajectory is primary. The following are descriptive only:

- old-only CE by layer;
- $G^{true}$ and control envelope separately;
- cumulative full-state $Z$ accessibility;
- adjacent differences $T_{\ell+1}-T_\ell$;
- early/middle/deep medians;
- count and location of positive layers.

No monotonic regression, best-layer test, late-minus-early contrast, or smoothing can replace the registered layerwise set. If explored after the verdict, it must be labeled exploratory.

## 11. Secondary Metrics And Guards

### 11.1 Capability

At every layer report parent-balanced eight-way CE, balanced accuracy, and macro accuracy for:

- old-only $X_\ell$;
- full actual state $Z_\ell$ with a matched ridge readout;
- final block full output $H_{36}$.

`AI_PROPOSAL`: the experiment is globally capability-eligible only if $H_{36}$ balanced accuracy has a simultaneous lower bound above chance $1/8$ and exceeds its within-parent sample-label permutation q95. A layer-specific novelty verdict also requires its $Z_\ell$ full-state readout to exceed chance/permutation; otherwise that layer is Insufficient rather than negative evidence.

### 11.2 Residualization

Report per layer:

- $\|U\|$ and $\|R_U\|$ scales;
- TRAIN out-of-fold and DEVELOPMENT $R^2$ of $U\sim X$;
- cross-covariance norm between standardized $X$ and $R_U$;
- constant/near-zero feature counts;
- residualizer ridge choice.

These diagnose the construct and never substitute for $T_\ell$.

### 11.3 Control validity

Every bank must pass the six mapping constraints in Section 8.4. Report the bank gain distribution, q95, maximum, child-source balance, self-map count, and unique-map hash. If the control becomes a fixed invertible label map or uses confirmation-dependent pairing, the experiment is Insufficient.

### 11.4 Same-$X$ identity

For every split, layer, and branch, save and verify hashes of:

- record order;
- standardized $X$ array;
- frozen base logits $s^0$;
- parent and child order;
- base ridge and intercept.

All branches must have bit-identical record order and base logits. Only the correction logits may differ.

## 12. Known Good, Known Bad, And Known Confusing Cases

Before any all-block model execution, unit tests must cover:

| Case | Construction | Required behavior |
| --- | --- | --- |
| known good | $R_U$ contains an $X$-independent child component; controls do not | $G^{true}>0$ and $T>0$ |
| known bad | $R_U$ is independent noise | true branch does not beat controls |
| known confusing | $U$ is a linear copy of $X$ | raw update can be readable, but residualized $T$ is not positive |
| capacity trap | base is deliberately underfit and duplicate $X$ can improve it | raw true gain cannot pass unless it exceeds duplicate-$X$ |
| invalid mismatch | one fixed child-label rotation | validation rejects the bank as class-level/invertible |
| constant block | all $X$ rows identical | block is marked structurally ineligible without divide-by-zero |
| leakage trap | one semantic family appears in two splits | data preflight stops before model execution |

Direct and kernel/primal implementations on a small synthetic matrix must agree within a frozen tolerance. The additive CE calculation must reproduce a hand-computed example.

## 13. Scientific Procedure And Stage Contracts

### Stage P0 — document review

The Anchor and this Protocol were reviewed. The 2026-08-16 all-experiments authorization advances directly to P1 under Amendment A1.

### Stage P1 — implementation and model-independent preflight

Requires `APPROVED_FOR_IMPLEMENTATION_AND_FULL_FROZEN_ALL_LAYER_RUN`.

Implement the exact data validators, synthetic known cases, extraction identities, residualizer, same-$X$ branches, mismatch banks, metrics, and artifact schema. Validate them without reading fresh CONFIRMATION representations or labels. Any failure stops execution; a valid preflight proceeds directly to P2 under the same approval.

### Stage P2 — all-layer TRAIN/DEVELOPMENT extraction and fitting

Extract TRAIN/DEVELOPMENT blocks 1--36 in one frozen-model pass where feasible. Verify every block, process layers in ascending order, and fit the full registered branch family for every eligible block. Fresh CONFIRMATION remains absent and closed.

The stage must verify:

1. extraction/replay/normalization identities;
2. finite, nondegenerate $X,U,R_U$ scales;
3. grouped residualizer and all ridge fits converge;
4. same-$X$ base logits are identical across branches;
5. all 64 mismatch maps and their balances are valid;
6. all penalties, seeds, maps, exclusions, interval code, tables, and plot axes can be frozen;
7. no code path reads old or fresh CONFIRMATION labels.

If any block fails a local identity or fit guard, record the predeclared eligibility reason. A systematic failure, invalid control bank, or missing registered layer stops before confirmation. Valid local structural ineligibility does not permit post-hoc layer replacement.

### Stage P3 — all-layer selection freeze

Freeze all TRAIN/DEVELOPMENT outputs and write `evidence/selection_freeze.json`. The receipt must include every eligible/ineligible block, exact penalties, control-map hashes, seed hashes, code/config/data/model hashes, interval implementation, table schemas, and fixed figure axes. No fresh CONFIRMATION representation, label, loss, or aggregate is available at this stage.

### Stage P4 — fresh-confirmation internal gate

The runner verifies the fresh data manifest, all block guards, selection-freeze receipt, resource receipt, and intended one-shot command. The already granted full-run approval permits continuation only if every gate is valid; otherwise the runner stops and returns to the researcher without opening confirmation.

### Stage P5 — one-shot all-layer confirmation and finalization

Evaluate every frozen branch for every eligible block, compute paired simultaneous intervals, render registered tables/figures, assign one typed verdict, and save full record-level and resampling arrays. No layer, control, seed, threshold, or display range may change afterward except through a documented amendment that invalidates the original verdict.

## 14. Algorithm, Outputs, Figures, And Provenance Contract

### 14.1 Algorithm

1. validate hashes, splits, labels, tokenization, and task balance;
2. load the frozen model and verify architecture/token site;
3. extract $h,a,X,Z,U,H$ for all authorized records and blocks;
4. verify identities and determine eligible blocks without target results;
5. standardize from TRAIN only;
6. cross-fit $U\sim X$ and construct $R_U$;
7. fit and freeze old-only base logits;
8. fit true, duplicate-$X$, and 64 mismatch corrections;
9. select penalties on DEVELOPMENT;
10. freeze seeds, maps, arrays, exclusions, intervals, and figure schemas;
11. after the internal freeze gate, evaluate fresh CONFIRMATION once;
12. compute $G$, control envelope, $T$, simultaneous intervals, and $\mathcal L^+$;
13. render artifacts and typed verdict; do not start low-rank analysis.

### 14.2 Required primary figure

**Figure 1 — All-layer conditional-fine matched excess.**

- x-axis: block index 1--36 in forward order;
- y-axis: signed $T_\ell$ in nats/example;
- one point and simultaneous 95% interval for every eligible block;
- horizontal zero line;
- block 1 shown as `NA: constant X` if structurally ineligible, not as zero;
- layers in $\mathcal L^+$ highlighted by a fixed marker/color;
- negative and unresolved layers remain visible;
- no smoothing; connecting line may aid reading but never interpolation;
- fixed y-limits determined from TRAIN/DEVELOPMENT diagnostics before confirmation, with overflow markers rather than post-hoc rescaling.

Allowed conclusion: identifies which registered layers have positive target-aligned excess under the simultaneous rule and exposes the complete signed depth trajectory.

Forbidden conclusion: deeper is necessarily better, every positive point is significant, or the admitted information is low rank.

### 14.3 Required same-$X$ control figure

**Figure 2 — Identical-base dual-branch comparison.**

Two all-layer panels:

1. all layers: $G^{true}_\ell$, $G^{dupX}_\ell$, and mismatch q95 envelope, all in nats/example;
2. all layers: old-only CE, old-plus-true-$R_U$ CE, old-plus-duplicate-$X$ CE, and old-plus-mismatch-q95 CE with paired DEVELOPMENT/CONFIRMATION intervals clearly separated.

The caption must state that every branch reuses the same record-level $X_\ell$ and bit-identical frozen base logits; only correction input/logits differ.

### 14.4 Required tables and arrays

- `tables/layerwise_primary.csv`: one row per block with eligibility, old CE, every branch gain, control envelope, $T$, pointwise and simultaneous intervals, and verdict membership;
- `tables/all_layer_branch_audit.csv`;
- `tables/capability_guards.csv`;
- `tables/extraction_identity_guards.csv`;
- `tables/mismatch_bank_audit.csv`;
- `tables/ridge_choices.csv`;
- `evidence/record_level_confirmation.npz` with every record-level CE/gain and IDs;
- `evidence/bootstrap_draws.npz` with every paired layer/branch draw;
- `evidence/selection_freeze.json`;
- `evidence/run_manifest.json` with code, data, model, environment, seed, and artifact hashes;
- `figures/layerwise_signed_matched_excess.{png,pdf}`;
- `figures/same_x_branch_controls.{png,pdf}`;
- final `summary.md` and `detailed.md` only after scientific execution.

### 14.5 Provenance

Every produced artifact records experiment ID, stage, timestamp, git commit or dirty-tree diff hash, data hashes, model/tokenizer hashes, environment lock hash, seed-manifest hash, parent/child ordering, block ordering, and upstream artifact hashes. Raw arrays must be sufficient to recompute every table and figure without a model forward.

## 15. Success, Failure, And Insufficient Evidence

Under all mandatory guards:

### Pass

`CONDITIONAL_FINE_ADDED_ACCESSIBILITY_FOUND` iff $\mathcal L^+\ne\varnothing$.

The result must list every admitted layer and may not generalize to nonmembers.

### Fail

`NO_REGISTERED_LAYER_EXCEEDS_MATCHED_CONTROLS` iff every eligible block satisfies

$$
\operatorname{UCB}^{sim}_{0.95}(T_\ell)\le0.
$$

### Insufficient

Use a typed Insufficient status if:

- $\mathcal L^+=\varnothing$ but at least one decisive simultaneous interval crosses zero;
- global or layer-specific capability fails;
- data independence, identity, same-$X$, control, convergence, or provenance fails;
- an exclusion is made after viewing confirmation;
- confirmation is accessed before the freeze receipt;
- too few eligible layers remain for the registered all-layer question.

Mixed results are allowed: some layers can be admitted while others are negative, unresolved, or structurally ineligible. The signed curve, not a forced single depth narrative, is the knowledge update.

## 16. What This Cannot Claim

This experiment cannot establish:

- Shannon information creation or causal necessity;
- that deeper cumulative representations monotonically improve fine discrimination;
- low representation rank or low functional retrieval rank;
- a common cross-layer subspace;
- semantic clustering or covariance/PCA meaning;
- native MLP use of $R_U$;
- expert identity, specialization, compatibility, or utility;
- Router accuracy, load balance, regret, NLL, speed, or compute benefit;
- cross-model, cross-token-site, cross-language, or natural-corpus generality;
- nonlinear inaccessibility when the registered linear readout fails.

If $\mathcal L^+$ is nonempty, the next experiment may ask how many directions retain a registered fraction of $G^{true}$ for those exact layers. It must use a new Anchor/Protocol and cannot inherit a low-rank Pass from this result.

## 17. Block Confirmation, Freeze, And Amendment Ledger

### 17.1 Researcher review checklist

Please explicitly confirm or revise:

1. exact decision question and conditional-fine target;
2. same-$X$ frozen-base branch design;
3. duplicate-$X$ plus 64 sample-level mismatch controls;
4. conservative $T_\ell$ definition using the stronger control;
5. existing TRAIN/DEVELOPMENT and fresh 640-record CONFIRMATION plan;
6. direct blocks 1--36 processing, with blocks 2--36 as the expected eligible science set;
7. signed all-layer plot and simultaneous-positive set;
8. no single-block smoke; model-independent preflight continues directly into all-block execution under one approval;
9. no low-rank/PCA/public-basis/Router work under E01;
10. resource profile and ceilings after an implementation estimate, to be included in any later full-run approval.

### 17.2 Current freeze state

| Item | State |
| --- | --- |
| Anchor | human design confirmed for direct all-block execution shape |
| Protocol blocks A--F | confirmed 2026-08-16 |
| Protocol block G | confirmed: one local H100 MIG 3g.40GB, at most 32 CPU workers, 256 GiB RAM, 20 GiB new run storage, and 12 wall-clock hours |
| implementation | completed; tests and preflight passed |
| fresh confirmation | generated, frozen, and evaluated exactly once |
| all-layer run | completed; block 1 structural N/A, blocks 2--36 evaluated |
| low-rank analysis | separately completed under A15_08_03_E01; never used to change E01 verdict |

### 17.3 Execution ledger

| Date | Entry | Authority | Scope |
| --- | --- | --- | --- |
| 2026-08-16 | `DOCUMENT_DRAFT_CREATED` | user request | Anchor + Protocol writing only; no experiment |
| 2026-08-16 | `DESIGN_ACCEPTED_DIRECT_ALL_BLOCKS` | researcher | A--F confirmed; block-25 smoke removed; no execution authority |
| 2026-08-16 | `APPROVED_FOR_IMPLEMENTATION_AND_FULL_FROZEN_ALL_LAYER_RUN` | researcher | all experiment-one stages plus separately scoped experiment two approved |
| 2026-08-16 | `PRECONFIRMATION_IMPLEMENTATION_AMENDMENT_A1` | execution audit under blanket approval | resolve ridge-objective inconsistency; delegate label-free fresh-data quality audit; no result accessed |
| 2026-08-16 | `FULL_EXECUTION_COMPLETED` | execution agent under researcher approval | blocks 2--36 evaluated; block 1 structural NA; $\mathcal L^+=\{24,28\}$; block 25 unresolved |

## 18. Executed Result

- Typed verdict: `CONDITIONAL_FINE_ADDED_ACCESSIBILITY_FOUND`.
- Simultaneous-positive set: $\mathcal L^+=\{24,28\}$.
- Block 24: $T_{24}=0.1087$, simultaneous 95% CI $[0.0526,0.1649]$.
- Block 28: $T_{28}=0.0653$, simultaneous 95% CI $[0.0239,0.1067]$.
- Block 25: $T_{25}=0.0693$, simultaneous 95% CI $[-0.0073,0.1460]$; not admitted.
- Raw run root: `/data/250010109/MoE_Router/experiments/20260816_a15_08_02_e01_layerwise_conditional_fine_added_accessibility/runs/a15-08-02-e01-20260816-full`.

### 17.4 Amendment rule

Before confirmation access, a researcher-approved amendment may change the design if the reason, affected blocks, and new falsifier are recorded here. After confirmation access, any change to data, eligible layers, target, branch, control, metric, confidence rule, seed, or figure selection invalidates the original verdict and requires a successor experiment ID. Cosmetic typo fixes that do not change computation remain allowed and must be logged.
