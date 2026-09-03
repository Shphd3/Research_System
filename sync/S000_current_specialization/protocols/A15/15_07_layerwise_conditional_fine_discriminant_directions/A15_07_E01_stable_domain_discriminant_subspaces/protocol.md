# Protocol: A15_07_E01 Dual-Track Held-Out Functional Spectrum

## 0. Approval Snapshot

```text
Document status: APPROVED_FOR_FULL_RUN
Approval status: researcher explicitly approved Protocol, implementation, smoke, and both full tracks on 2026-08-20
Block audit status: A=CONFIRMED B=CONFIRMED C=CONFIRMED D=CONFIRMED E=CONFIRMED F=CONFIRMED G=CONFIRMED
Cross-block consistency: PASS
Execution scope approved: protocol + implementation + local tests + smoke + full controlled track + full natural track
Design frozen at: 2026-08-20 before any C4 activation or MASSIVE TEST activation was loaded
Registered scientific-body revision: pre-receipt SHA-256 efa456d80929e7c4ba1efbfc539889a38811c1df2273212291a8e468b59be4d6
Purpose: test whether the existing supervised low-rank functional spaces survive fresh data, locate their held-out function in the TRAIN spectrum, and test external transport on natural hierarchical intent data
Primary Anchor: A15_07 held-out function and spectral location
Anchor decision question: exact frozen rank-8/rank-56 controlled spaces on fresh data, then analogous local-versus-shared dimension ordering on natural data after a full-R_U gate
Strongest rival: the opened-bank result is a synthetic/template artifact and natural R_U adds no function beyond X
Experiment role: controlled confirmation plus external robustness replication
Primary metric: paired held-out cross-entropy gain over X-only, and its retained fraction after low-rank projection
Claim boundary: fixed model, blocks, linear residualization/readouts, named controlled hierarchy and one natural English intent dataset
Minimal setup: Qwen3-8B, blocks 24/28, two new controlled panels, MASSIVE 1.0 en-US official split
Treatment and controls: full R_U, frozen/learned supervised subspaces, PCA bands; duplicate-X, mismatched-R_U, label permutation and matched conditional-Haar controls
Changed variable: admitted update information and the subspace/band through which it is permitted to act
Held fixed: model, hook, decision token, prompt family within each track, split roles, classifier family, metrics, thresholds and bootstrap plan
Pass: defined separately for controlled stability, functional spectral location and natural external replication in Section 15
Fail: simultaneous upper bound at or below the registered boundary, or a clearly negative prerequisite gate
Insufficient: interval crosses the boundary, identity/leakage/numerical guard fails, or a required artifact is missing
Cannot claim: native causal use, new knowledge, Router/expert utility, LoRA mechanism, no forgetting, universal transfer
Approval decision: RUN BOTH TRACKS; do not publish, commit, push, edit graph, or root-sync
```

The approved [active Focus](/daily_research_reports/backup/2026/08/0820/focus_stable_domain_discriminant_subspaces.md)
states the same question in plain language. This Protocol supersedes the
pre-approval generalized-eigenvector draft; no execution from that draft is
eligible for this experiment.

## 1. Terminology / Definitions

- **$X_\ell$:** normalized old state at the registered same-token block hook.
- **$R_{U,\ell}$:** attention-write update after subtracting the TRAIN-fitted
  linear prediction from $X_\ell$, then applying the TRAIN-only feature
  standardizer. It is a candidate update, not “new knowledge.”
- **RRR:** supervised reduced-rank ridge regression. It learns an affine
  correction from $R_U$ to the residual fine-class target after an out-of-fold
  $X$-only classifier. Rank is the number of input-output modes allowed in the
  correction, not covariance rank or task capacity.
- **TRAIN / DEVELOPMENT / CONFIRMATION(TEST):** TRAIN contributes fits;
  DEVELOPMENT selects ridge values/ranks; CONFIRMATION or official TEST is
  opened only after code and decision rules freeze and never selects a model.
- **Full gain:** mean per-example reduction in natural-log cross entropy from
  the frozen $X$-only predictor to the predictor augmented by the full-$R_U$
  correction. Unit: nats/example.
- **Retention:** low-rank gain divided by full-$R_U$ gain, computed from paired
  aggregate gains. It is undefined when the full-gain admission gate fails.
- **Projector overlap:** $\lVert Q_1^\top Q_2\rVert_F^2/\min(r_1,r_2)$ for
  orthonormal bases. It measures orientation only, not semantics or function.
- **Conditional Haar control:** a uniformly random same-rank subspace inside
  the numerically identifiable TRAIN PCA span. The expected overlap of a
  rank-$r$ task space with a $d_b$-dimensional band inside a $d_{id}$-dimensional
  span is $d_b/d_{id}$; pairwise task overlap is $r/d_{id}$, not $r/4096$.
- **Keep-only / drop-one:** keep-only allows only one spectral component of a
  frozen correction; drop-one removes only that component. They test held-out
  sufficiency and necessity respectively.
- **Simultaneous 95% interval:** percentile interval from paired stratified
  bootstrap draws with max-statistic correction across the two blocks and all
  registered primary panels/conditions in that hypothesis family.

## 2. Anchor Alignment

The Protocol implements [A15_07](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor.md)
without changing its object, entry gate, metric or claim boundary.

Track A validates exact candidates already learned in E03: requested task rank
8 and shared rank 56. Track B fits an analogous system on a natural hierarchy;
it is a transport test, not pooled corroboration. Spectral overlap is a location
diagnostic; held-out keep/drop function is verdict-bearing.

## 3. Tested Hypotheses

### H1: controlled expression stability

On C4-expression, at least one block passes full-$R_U$ admission, the frozen
task rank-8 system has simultaneous all-domain retention LCB $>0.80$, and the
frozen shared rank-56 system has simultaneous all-domain retention LCB $>0.90$.
C4-atom reports the same tests as a separate stronger shift outcome.

### H2: held-out functional spectral location

At an H1-admitted block, at least one registered PCA band has projector-overlap
excess above conditional-Haar q95 and simultaneous positive keep-only gain or
positive drop-one loss of gain on C4-expression. C4-atom is a separate
transport result and cannot rescue H2.

### H3: natural external replication

On MASSIVE official TEST, at least one block first has a simultaneous full-$R_U$
gain LCB above the stronger of duplicate-$X$, mismatched-$R_U$ and label-null
q95. Conditional on admission, the smallest all-task 90%-retention crossing for
one shared basis is larger than the largest task-local 90%-retention crossing.

## 4. Rival Explanations

| Rival | Control or gate | Consequence if live |
| --- | --- | --- |
| Old expression/template memorization | C4-expression has disjoint normalized text, templates, fact combinations and record IDs | exact old spaces are not expression-stable |
| Old fact-atom dependence | independent C4-atom source propositions and templates | claim remains expression-only if this panel fails |
| Arbitrary low rank works | same-rank conditional-Haar rotations and label permutation | no supervised-subspace claim |
| Ambient-space baseline exaggerates separation | nulls conditioned on the exact TRAIN-identifiable span | report only conditional geometry |
| Overlap is mistaken for function | keep-only and drop-one held-out loss | location-only result |
| Natural prompts contain no added $R_U$ function | full-$R_U$ admission before any low-rank interpretation | downstream natural rank is `NOT_APPLICABLE` |
| Source/class imbalance explains natural result | official split, class-balanced task aggregation, paired within-cell bootstrap | no population-wide domain claim |

## 5. Data Construction And Provenance

### 5.1 Track A: controlled panels

The existing hierarchy has eight parent domains and eight fine classes per
domain. Each new panel contains $8\times8\times30=1,920$ rows.

- **C4-expression (primary):** existing six source propositions per fine class,
  but new template-family IDs and new proposition-subset/order IDs. No prompt
  text, template ID, combination ID or record ID may overlap T, D, C3 or any
  older confirmation bank.
- **C4-atom (strong shift):** six additional proposition atoms per fine class
  sourced from frozen English Wikipedia revisions, using registered page-title
  disambiguation. Exact child and parent names are removed from candidate
  sentences; rows failing the frozen leakage scanner are rejected before the
  manifest is sealed. New templates and combinations are disjoint from every
  older bank and C4-expression.

Each manifest records source URL/title/revision ID, extracted sentence hash,
normalization rule, templates, proposition indices, labels, prompt hash and
SHA-256. Construction code may inspect labels; activation extraction and model
fitting may not modify rows. If any cell has fewer than 30 admissible rows,
C4-atom is `INSUFFICIENT_DATA`; do not replenish after seeing activations.

### 5.2 Track B: MASSIVE 1.0 en-US

Source: official MASSIVE 1.0 tarball
`https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.0.tar.gz`.
The raw tarball and extracted `1.0/data/en-US.jsonl` are hashed. Permitted fields
are `id`, `partition`, `scenario`, `intent`, and `utt`; worker/judgment/slot
fields are ignored.

Five fixed tasks are used:

1. email: all four intents;
2. transport: all four intents;
3. IoT: four highest-TRAIN-count intents;
4. play: four highest-TRAIN-count intents;
5. question answering: four highest-TRAIN-count intents.

Ties use lexicographic intent name. The label set is frozen from TRAIN counts;
DEVELOPMENT must contain at least five examples per selected intent. During the
pre-Protocol feasibility audit, official partition/schema and per-intent row
counts, including TEST counts, were visible, but no TEST text, activation,
prediction or task metric was inspected. This makes the replication
preregistered after a public-schema/count audit rather than fully data-blind;
TEST counts do not filter, weight or select tasks. Prompt:
`User request: <utt>\nClassification:`.

### 5.3 Split and leakage contract

| Role | Fits | Selects | Final evaluation | Forbidden |
| --- | --- | --- | --- | --- |
| Existing controlled T | frozen residualizer, standardizer, base/full/RRR maps, PCA | old E03 settings only | no new verdict | refit after C4 |
| Existing controlled D | none in this run | already-frozen old settings | no new verdict | use C4 information |
| C4-expression / C4-atom | nothing | nothing | one registered pass each | regeneration or filtering after activations |
| MASSIVE TRAIN | residualizer, standardizer, base/full/RRR maps, PCA | label-set rule fixed here | no final metric | inspect TEST metric |
| MASSIVE DEVELOPMENT | no final fit except registered refit after selection | ridge and registered crossing | diagnostics | choose from TEST |
| MASSIVE TEST | nothing | nothing | one registered final evaluation | rerank, retune, exclude |

## 6. Learning Task And Permitted Supervision

For each known coarse domain, the permitted input is $X_\ell$ or $R_{U,\ell}$
at the registered final prompt token and the required output is the fine-class
ID within that domain. Parent identity selects the task but is never a target
feature. Targets are centered one-hot vectors. An $X$-only affine ridge
classifier is fit first; five-fold TRAIN out-of-fold predictions define the
correction target. RRR maps $R_U$ to that correction target. No language-model,
Router, expert or LoRA parameter is updated.

## 7. Model / Architecture And Frozen Variants

- Model: frozen `/data/share/Qwen3-8B`, evaluation mode, `use_cache=False`.
- Width/layers: verify 4,096 and blocks 24/28 at runtime.
- Hook: exact E03 pre/post-attention same-token normalized $X,Z$ definition.
- Controlled residualizer/standardizer: exact E03 TRAIN states and hashes.
- Natural residualizer: affine ridge $U\leftarrow X$ chosen on DEVELOPMENT
  reconstruction loss; five-fold TRAIN OOF residuals define feature scales;
  final TRAIN residualizer applies unchanged to DEVELOPMENT/TEST.
- Base/full/RRR model: the verified E03 compact affine and RRR routines.
- Task-local controlled rank: requested 8, with used numerical rank recorded.
- Controlled shared basis: 56 leading left singular vectors of equally
  Frobenius-normalized frozen task maps; frozen shared heads from old TRAIN/D.
- Natural task ranks: $\{1,2,3\}$; natural shared ranks
  $\{1,2,3,5,8,12,15\}$.

## 8. Training Objective And Optimization

All affine ridge values use the frozen E03 grid
$\{10^{-8},10^{-7},\ldots,10^2\}$ after the same feature scaling. Ties choose
the stronger ridge. RRR solves the regularized least-squares correction with a
hard rank cap using the feature SVD; its validation objective is mean fine-class
cross entropy after adding the correction to the $X$-only logits.

The shared basis is the leading left singular basis of the concatenated task
coefficient matrices after each task map is divided by its Frobenius norm.
Each natural shared head is fit on TRAIN coordinates and its ridge selected on
DEVELOPMENT. No TEST checkpoint or operating point exists.

## 9. Conditions, Seeds, And Checkpoints

| Item | Frozen value |
| --- | --- |
| Layers | 24, 28 |
| Controlled panels | C4-expression, C4-atom; 1,920 rows each |
| Controlled ranks | task 8, shared 56 |
| Natural tasks | 5 domains × 4 intents, official split |
| Natural local ranks | 1, 2, 3 |
| Natural shared ranks | 1, 2, 3, 5, 8, 12, 15 |
| PCA span tolerance | binary64 eps × max(matrix shape) × largest singular value |
| PCA bands | five consecutive bands with sizes differing by at most one inside $d_{id}$ |
| Haar draws | 1,000 per layer/rank/band family, seed 150701 |
| Label/mismatch draws | 256, seeds 150710–150965 |
| Bootstrap | 2,000 paired stratified draws, seed 150799 |
| Model checkpoint | `/data/share/Qwen3-8B` resolved hash recorded at runtime |

No seed is a scientific replicate of a new model. Random draws calibrate nulls
or uncertainty conditional on the fixed examples/domains.

## 10. Primary Metric And Frozen Analysis Plan

For row $i$, $g_i=CE(f_X,y_i)-CE(f,y_i)$. Aggregate first equally within fine
class, then equally across fixed domains. Bootstrap resamples rows with
replacement inside every domain-by-class cell and reuses identical weights for
all paired conditions.

### Controlled H1

1. Admission margin is full-$R_U$ aggregate gain minus the larger of
   duplicate-$X$ and mismatched-$R_U$ q95.
2. Task retention is the minimum domain ratio of frozen task-rank-8 gain to
   full gain; shared retention is the minimum domain ratio of shared-rank-56
   gain to full gain.
3. C4-expression passes only if admission LCB $>0$, task-retention LCB $>0.80$
   and shared-retention LCB $>0.90$ at the same layer. C4-atom is classified
   independently with the same rule.

Ratios whose denominator is nonpositive in a bootstrap draw are missing for
that draw. More than 5% missing draws makes the corresponding retention
`INSUFFICIENT`; no clipping, outlier removal or smoothing is allowed.

### Controlled H2

Pooled parent-centered TRAIN $R_U$ defines $d_{id}$ and five bands. For each
frozen task/shared map and band, report normalized overlap, conditional-Haar
median/q95, keep-only gain and drop-one loss of gain. H2 passes only when the
same band has overlap above q95 and simultaneous LCB $>0$ for keep-only gain or
drop-one loss on C4-expression.

### Natural H3

Admission uses full-$R_U$ gain minus the maximum of duplicate-$X$,
mismatched-$R_U$ and label-null q95. If no layer has LCB $>0$, all natural rank
and band results are `NOT_APPLICABLE`. If admitted, report per-task and shared
retention curves. A 90% crossing is the first registered rank whose retention
LCB exceeds 0.90. H3 passes if a shared all-task crossing exists and is strictly
larger than every local-task crossing. Missing crossings are reported, not
extrapolated.

Multiplicity uses one max-statistic family for controlled H1 across two layers,
one for controlled H2 across layers/bands/maps, and one for natural admission.
H3 crossing intervals are descriptive conditional evidence and cannot rescue
a failed admission.

## 11. Secondary Metrics And Guards

- Cross-panel point estimates and class-balanced accuracy for interpretability.
- Pairwise task-subspace heatmaps with both ambient and conditional baselines,
  with the conditional baseline visually primary.
- Coefficient-energy overlap is reported separately from projector overlap.
- Used rank, normal-equation residual, orthogonality error, finite checks,
  duplicate prompt counts, label leaks and class counts.
- Native $U$, standardized $R_U$ and $X$ hashes are separate.
- Full-recompute versus cached-object parity on 16 rows per track must have
  max absolute error $<10^{-5}$ in float32 activations.

## 12. Known Good / Known Bad / Known Confusing Cases

- **Known good:** identity projection reproduces the full frozen correction to
  $10^{-6}$ logits; sum of five band components reproduces the identifiable
  projection; keep-all equals low-rank.
- **Known bad:** zero projector yields exactly the $X$-only predictor; permuted
  labels and mismatched $R_U$ must not be silently treated as true pairs.
- **Known confusing:** a band may have high overlap but near-zero function, or
  function without excess overlap. These are registered mixed outcomes, not
  plotting errors. A natural gate failure is a valid completed negative result.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal | Input and assumptions | How / why | Expected output | Pass / fail / insufficient | Artifact and handoff |
| --- | --- | --- | --- | --- | --- | --- |
| S0 | Freeze design and sources | approved Focus/Anchor/Protocol | hash scientific body, code plan, old states, raw source URLs | freeze receipt | all required IDs present | `freeze.json`; permits construction |
| S1 | Build and seal data | old taxonomy; Wikipedia revisions; MASSIVE 1.0 | construct/audit before any activation | manifests and hashes | schema/leakage/count pass or stop affected panel | `data/*manifest.json`; permits extraction |
| S2 | Verify implementation | synthetic fixtures and 16-row real smoke | unit tests, hook identity, cache parity, band reconstruction | test/smoke receipts | every registered invariant passes | `smoke/*`; permits full run |
| S3 | Extract representations | sealed prompts, frozen model | 8-way data parallel blocks 24/28 | X/U shards and manifests | complete unique coverage, finite arrays | raw extraction; permits residualization |
| S4 | Controlled admission/function | frozen old states and C4 arrays | evaluate only; no refit | H1 table, curves | Pass/Fail/Insufficient | controlled result; permits H2 only if admitted |
| S5 | Controlled spectrum | TRAIN PCA and frozen maps | conditional overlap plus keep/drop | band table and figure | registered H2 mapping | controlled spectrum evidence |
| S6 | Natural fit/admission | MASSIVE TRAIN/D/TEST | fit TRAIN, select D, open TEST once | admission table | fail stops natural rank interpretation | natural gate receipt |
| S7 | Natural rank/spectrum | admitted layer only | local/shared curves and bands | H3 table and figure | Pass/Fail/Insufficient/NA | final raw result |
| S8 | Evidence curation | all raw receipts | conformance audit, render and visual check | summary/detailed, figures/tables | no unsupported number | human result handoff |

Failure in one C4 panel does not invalidate the other if its identity chain is
independent. Failure in natural admission stops only natural downstream
interpretation. Any post-unseal scientific change makes the affected condition
ineligible and requires an append-only amendment.

## 14. Algorithm, Output, And Provenance Contract

Implementation workspace:
`/data/250010109/MoE_Router/experiments/20260820_a15_07_e01_dual_track_heldout_spectrum`.

Raw output root:
`/data/250010109/MoE_Router/experiments/20260820_a15_07_e01_dual_track_heldout_spectrum/runs/<run_id>`.

Curated result root is this Protocol directory with `summary.md`,
`detailed.md`, `figures/` and `tables/`. The runner must refuse an existing
run directory, save per-rank coverage receipts, and write `status.json` on
every terminal path.

Formal resource profile is the researcher-selected `5090-8-spot`:

```text
execution_surface=ACP
workspace=share-space
aec2=computing-cluster-5090-01g
worker_spec=n12lp.nn.i10a.8
worker_nodes=1
quota=spot
priority=normal
GPU/process_count=8
image=registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04
mount=01995892-d478-76d8-aec7-13fd8284477e:/data
```

The SCO v1.3.0 workspace-field incompatibility is handled only by the existing
audited local compatibility proxy; it changes transport parsing, not the job
contract. The formal runner checks eight visible 5090 GPUs, model access,
package imports, data hashes and available disk before extraction.

## 15. Success / Failure / Insufficient Evidence

| Verdict | Exact rule | Allowed update |
| --- | --- | --- |
| `CONTROLLED_EXPRESSION_PASS` | C4-expression admission and 0.80/0.90 retention LCBs pass at one layer | exact candidates generalize to new expressions |
| `CONTROLLED_EXPRESSION_FAIL` | a required UCB is at/below its boundary | weaken exact-space expression stability |
| `ATOM_TRANSFER_PASS` | same registered gate passes on C4-atom | supports stronger proposition/style transport |
| `ATOM_TRANSFER_FAIL` | expression may pass but atom panel clearly fails | bound claim to expression distribution |
| `FUNCTIONAL_BAND_LOCALIZED` | overlap q95 and keep/drop LCB gate pass on same band | band carries held-out correction function |
| `LOCATION_ONLY` | overlap passes but keep/drop does not | orientation without functional attribution |
| `NATURAL_ENTRY_FAIL` | no block clears natural admission | natural low-rank/spectrum are `NOT_APPLICABLE` |
| `NATURAL_SHARED_EXPANSION_PASS` | admitted and shared 90% crossing > every local crossing | one common natural basis needs more dimensions |
| `NATURAL_REPLICATION_FAIL` | admitted but ordering clearly fails | no external replication of union expansion |
| `INSUFFICIENT_EVIDENCE` | interval, data, identity, numerical or artifact guard fails | no directional claim from affected condition |

The overall result is typed, not a single majority vote. Controlled and natural
tracks must be stated separately.

## 16. What This Cannot Claim

Even a complete positive result cannot establish that the language model uses
these linear directions causally, that $R_U$ is new knowledge, that PCA tail
coordinates are generally better, that a Router should gate on these exact
coordinates, that experts become useful/specialized, that LoRA works for this
reason, or that learning is immune to forgetting. MASSIVE is realistic intent
text but remains one English dataset with scenario labels and class imbalance.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Time (UTC) | Event | State / scope | Basis |
| --- | --- | --- | --- |
| 2026-08-20 | researcher confirmed dual-track proposal | A–G `CONFIRMED`; consistency `PASS` | “直接构写 protocol 然后开始执行实验，双轨都要执行” following the audited proposal |
| 2026-08-20 | execution authorization | implementation + smoke + both full runs | same explicit instruction; prior explicit selection of remote 8×5090 |
| 2026-08-20 | scientific body frozen | `APPROVED_FOR_FULL_RUN` | before new activation extraction or TEST evaluation |

Post-start updates may append only execution receipts, result links, or a formal
amendment containing before/after values, reason, observed-data status,
affected conditions, approval and eligibility impact. No result or
interpretation belongs in the frozen scientific body.

### Final pre-execution audit

```text
Anchor question and claim boundary unchanged: PASS
Every decision-bearing choice grounded or explicitly approved: PASS
Approval snapshot cold-readable: PASS
Treatment, controls, changed and fixed variables explicit: PASS
Every stage has input, operation, output, stop and handoff: PASS
Primary analysis yields unambiguous typed verdicts: PASS
Preflight and smoke protect scale-up: PASS
Confirmation truth cannot guide fitting or selection: PASS
Artifacts and provenance are auditable: PASS
A-G confirmed and cross-block consistency passes: PASS
Only approved execution scope is active: PASS
Post-start freeze/amendment rule recorded: PASS
```
