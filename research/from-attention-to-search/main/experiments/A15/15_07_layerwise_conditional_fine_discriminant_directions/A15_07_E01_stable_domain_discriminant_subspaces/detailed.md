# Detailed: A15_07_E01 Stable Domain Discriminant Subspaces

Primary Anchor: [A15_07](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor.md)  
Frozen Protocol and registered revision: [protocol.md](protocol.md), SHA-256 `619472d7dfed41fe757967ccc62b549fe10d3a436905ec00b0fad70318f5360c`  
Summary: [summary.md](summary.md)  
Result eligibility: `EVIDENCE_COMPLETE_AWAITING_HUMAN_JUDGMENT`

## 0. Quick Recap

- **Purpose:** confirm exact frozen controlled low-rank spaces on unseen data,
  locate their held-out function in the TRAIN spectrum, and test the analogous
  local-versus-shared statement on natural hierarchical intent data.
- **Hypothesis:** H1 controlled stability; H2 held-out functional spectral
  location; H3 natural shared-dimension expansion after a full-\(R_U\) gate.
- **Experiment logic:** first require full-\(R_U\) to beat matched controls, then
  test projected function, then compare spectral direction with held-out
  keep-only/drop-one function.
- **Direct result:** H1 expression `PASS`; H1 atom `PASS`; H2
  `FUNCTIONAL_BAND_LOCALIZED`; natural entry `PASS` at block 24; H3
  `INSUFFICIENT_EVIDENCE`.
- **Eligibility:** corrected controlled and natural-entry artifacts plus the
  final Amendment 005 natural-rank artifact are claim-eligible. The original
  formal status and earlier conditional retries are audit receipts only.
- **Researcher verdict:** `AWAITING_HUMAN_JUDGMENT`.
- **Claim boundary:** linear diagnostic function in one model, two blocks, one
  controlled hierarchy, and one English natural dataset; no native Router or
  causal mechanism claim.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| \(X_\ell\) | the old state before the layer's attention write | normalized same-token hidden state at block 24 or 28 | 4096-vector | baseline information | causal use |
| \(R_{U,\ell}\) | candidate layer update not linearly predictable from \(X_\ell\) | standardized residual of attention-write update after TRAIN-only affine ridge | 4096-vector | object projected in all rank tests | new knowledge |
| RRR | supervised reduced-rank ridge regression | rank-constrained affine correction from \(R_U\) to residual fine-class target | rank = input-output modes | learns functional directions | covariance rank or task capacity |
| Full gain | improvement over \(X\)-only | paired CE(\(X\))-CE(\(X+R_U\) correction) | nats/example | admission prerequisite | general model quality |
| Retention | projected gain relative to full gain | aggregate projected gain / aggregate full gain | ratio | asks how much function a subspace preserves | stability when denominator is weak |
| Projector overlap | direction-only subspace similarity | \(\lVert Q_1^\top Q_2\rVert_F^2/\min(r_1,r_2)\) | 0–1 | compares orientations | semantic identity or function |
| Conditional Haar | matched random direction baseline | same-rank random subspace inside TRAIN-identifiable PCA span | expected band overlap \(d_b/d_{id}\); task overlap \(r/d_{id}\) | avoids ambient-rank exaggeration | functional relevance |
| Keep-only / drop-one | spectral sufficiency / necessity checks | retain only one band or remove one band from frozen correction | nats/example | converts location into held-out function | native causal computation |

## 2. Anchor Link And Decision Point

The registered Anchor asks whether layerwise fine-discriminant directions are
stable, task-conditional, and spectrally localized. This experiment closes the
held-out-function and external-transport evidence gaps. It does not choose a
Router design. The next mechanism-level decision remains
`AWAITING_HUMAN_JUDGMENT`.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| approval and freeze | protocol, implementation, smoke and both full tracks approved before new activations | approval recorded; protocol SHA fixed | CONFORMANT | [Protocol §0](protocol.md#0-approval-snapshot) | none |
| data identity | 1,920 expression, 1,920 atom, MASSIVE 6,318 selected rows | exact counts; manifest sealed before activation | CONFORMANT | raw `data_v1/data_manifest.json`, SHA `c09af957...` | none |
| extraction | blocks 24/28, eight 5090 GPUs, complete unique coverage | all three datasets completed with per-rank identity receipts | CONFORMANT | formal run extraction manifests | none |
| controlled analysis | registered H1/H2 aggregation | original joint finite-mask aggregation erased valid block-28 intervals | DEVIATION CORRECTED | Amendment 001 and `postprocess_audit_001/controlled_corrected.json` | corrected artifact eligible; original verdict superseded |
| natural entry | registered admission with stable selected corrections | block 28 selected an unstable email correction; block 24 stable | PARTIAL | corrected natural audit | block 24 eligible; block 28 `INSUFFICIENT_NUMERICAL` |
| natural conditional rank | execute only after corrected admission | separate registered conditional run on block 24 | CONFORMANT AFTER AMENDMENT 002 | final run `conditional-natural-20260820T1700Z` | eligible for H3 |
| device portability | GPU state loading | first conditional retry failed on CPU/GPU state mismatch | IMPLEMENTATION RETRY | Amendment 003; failed run before rank result | no scientific result from failed run |
| tensor serialization | convert CUDA tensors before NumPy export | second retry failed before result | IMPLEMENTATION RETRY | Amendment 004 | no scientific result from failed run |
| numerical used rank | requested local rank 3 | prior successful retry counted a float32 fourth singular direction | DEVIATION CORRECTED | Amendment 005 | final run explicitly truncates to used rank 3; prior result superseded |
| missing crossings | missing registered 90% LCB crossing is `INSUFFICIENT` | final result typed `INSUFFICIENT_EVIDENCE` | CONFORMANT | final natural result | no dimension-ordering claim |

Frozen Protocol revision: `619472d7dfed41fe757967ccc62b549fe10d3a436905ec00b0fad70318f5360c`.  
Execution scope approved: implementation, tests, smoke, controlled full run,
natural full run, conditional natural run, evidence curation.  
Amendments: `001` through `005`, append-only in the implementation workspace.  
Retries and exclusions: two failed conditional jobs produced no rank result; the
1640Z successful result is superseded by Amendment 005; only 1700Z is final.  
Missing conditions or artifacts: no formal natural 90%-retention crossing.  
Post-hoc analyses: curated figures reorganize eligible registered outputs but do
not refit activations, models, bootstrap draws, ranks, or scientific thresholds.

## 4. Actual Setup

- **Research question:** see Summary and Protocol §3.
- **Data construction:** controlled C4-expression and C4-atom each contain 8
  parent domains × 8 fine classes × 30 rows. MASSIVE contains five parent tasks
  × four fine intents using official TRAIN/validation/TEST; selected counts are
  4,389/778/1,151.
- **Split contract:** controlled old TRAIN fitted all objects; new C4 panels only
  evaluated. MASSIVE TRAIN fitted, validation selected, TEST evaluated once.
- **Learning task:** within each known parent, predict the fine class from an
  \(X\)-only affine predictor plus an optional \(R_U\) correction.
- **Model:** frozen `/data/share/Qwen3-8B`, `use_cache=False`, blocks 24 and 28,
  exact same-token pre/post-attention hook.
- **Algorithm:** affine ridge residualization/classifier and supervised RRR;
  no language-model, Router, expert, or LoRA parameters changed.
- **Ranks:** controlled task 8/shared 56; natural local 1/2/3 and shared
  1/2/3/5/8/12/15.
- **Spectrum:** five contiguous equal-size bands inside the TRAIN-identifiable
  parent-centered \(R_U\) span. Controlled block-28 \(d_{id}=632\); natural
  block-24 \(d_{id}=4086\).
- **Randomness:** 1,000 conditional-Haar draws; 256 label/mismatch draws; 2,000
  paired cell-stratified bootstrap draws using frozen seeds.
- **Resources:** one ACP node, eight RTX 5090 GPUs, job `pt-rkw0whez`; final
  conditional job `pt-u9b0tv40`.
- **Code workspace:** `/data/250010109/MoE_Router/experiments/20260820_a15_07_e01_dual_track_heldout_spectrum`.
- **Known limitation:** five natural tasks from one English dataset do not
  establish universal domain structure, and weak taskwise full gains destabilize
  retention ratios.

## 5. Metrics And Registered Decision Rules

H1 passes at one same block when admission-margin LCB \(>0\), frozen task-rank-8
minimum-domain retention LCB \(>0.80\), and frozen shared-rank-56 minimum-domain
retention LCB \(>0.90\). Expression and atom are judged independently.

H2 passes at an H1-admitted block when one spectral band exceeds matched
conditional-Haar q95 in orientation and has positive simultaneous keep-only
gain or drop-one loss of gain on held-out expression data.

Natural admission passes when full-\(R_U\) gain minus the strongest matched
control has simultaneous LCB \(>0\). H3 requires a shared all-task 90%-retention
LCB crossing strictly larger than every local crossing. Missing crossings are
reported, never extrapolated from point estimates.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frozen spaces survive new expressions | H1 three gates at one block | formal controlled bootstrap/result | Amendment 001 condition-specific finite-mask aggregation | 2,000 paired stratified draws; simultaneous 95% | block 28 LCBs `0.03482`, `0.98790`, `0.98778` | ELIGIBLE | PASS | block 24 retention interval insufficient |
| frozen spaces survive new atoms | same H1 rule | same formal run, atom panel | Amendment 001 | same | block 28 LCBs `0.09810`, `0.99220`, `0.98749` | ELIGIBLE | PASS | one controlled hierarchy |
| held-out function lies in a registered spectral band | overlap q95 plus positive functional LCB | controlled spectrum and bootstrap | unchanged spectrum rows, H2 activated by corrected H1 | simultaneous H2 family | band 1; all 8 domains qualify for task8/shared56 | ELIGIBLE | FUNCTIONAL_BAND_LOCALIZED | supervised optimum not equal to PCA projector |
| natural \(R_U\) has added test function | margin LCB \(>0\) | natural gate arrays/result | corrected numerical audit and admission interval | class-balanced paired bootstrap | block 24 margin `0.00986`, LCB `0.00110` | ELIGIBLE | PASS | small absolute gain |
| block 28 natural result is usable | numerical guard | natural layer-28 fit receipt | audit of selected email correction | validation CE and coefficient norms | full CE `4927.65` vs base `0.8197`; coefficient norm `1174.57` | INELIGIBLE | INSUFFICIENT_NUMERICAL | no scientific failure inference |
| shared natural basis needs more dimensions | shared crossing > every local crossing | final natural rank result | Amendment 005 used-rank-3 truncation | taskwise retention intervals | all local crossings `None`; shared crossing `None` | ELIGIBLE RESULT, INSUFFICIENT EVIDENCE | INSUFFICIENT_EVIDENCE | point curves cannot decide H3 |
| natural local directions are geometrically distinct | descriptive projector overlap | final natural geometry rows | exact used rank 3, conditional span 4086 | fixed-task geometry; no replicate claim | off-diagonal mean `0.002285`, range `0.001298–0.003655`; baseline `0.000734` | ELIGIBLE SECONDARY | DESCRIPTIVE | direction only, not function |
| natural learned spaces concentrate in band 1 | descriptive spectral overlap plus taskwise pointwise keep/drop | final natural spectrum rows | registered bands, conditional run | taskwise pointwise intervals | local band-1 overlap `0.691–0.892`; shared `0.761`; email/IoT positive keep/drop | BOUNDED SECONDARY | DESCRIPTIVE | H3 remains insufficient |

## 7. Main Results

### Eligible decision evidence

1. **Controlled expression:** block 28 passes all H1 gates. Block 24 has a
   positive admission margin but unavailable retention intervals and is
   `INSUFFICIENT`, not a failure.
2. **Controlled atom:** block 28 passes all H1 gates. Block 24 is likewise
   insufficient on retention.
3. **Controlled spectrum:** band 1, ranks 1–127 of 632, is the only band that
   jointly passes direction and held-out function for both frozen maps across
   all eight domains.
4. **Natural entry:** block 24 passes. Block 28 is numerically ineligible and is
   not averaged with block 24.
5. **Natural H3:** no registered 90% crossing exists; verdict is
   `INSUFFICIENT_EVIDENCE`.

### Bounded and descriptive evidence

- Natural local rank-3 point retentions are `0.9973`, `1.0013`, `1.0002`,
  `0.9986`, and `0.9991` for email, transport, IoT, play and QA.
- Shared rank-15 point retentions are `0.9971`, `1.0052`, `1.1271`, `1.2845`,
  and `1.1519` in the same order.
- These values motivate, but cannot establish, a local-3/shared-15 dimension
  pattern because their simultaneous lower bounds do not cross 0.90.
- Natural local spaces have low absolute pairwise overlap and are concentrated
  in spectral band 1; only email and IoT have positive pointwise keep and drop
  lower bounds there.

### Debug-only and superseded evidence

- The original formal `status.json` reports controlled/natural failures caused
  by the now-audited aggregation and numerical issues. It is retained only as a
  receipt and must not be cited as the scientific verdict.
- Conditional runs that failed before producing a rank result are operational
  evidence only.
- The 1640Z natural rank result is superseded by explicit numerical rank-3
  truncation in Amendment 005.

## 8. Visualization Results

### Controlled held-out confirmation

![Controlled held-out confirmation](figures/fig1_controlled_confirmation.png)

- **Purpose:** adjudicate H1 on both fresh panels.
- **Metric:** admission margin in nats/example and minimum-domain retention
  ratio, with corrected simultaneous 95% intervals.
- **Source:** [controlled_h1_corrected.csv](tables/controlled_h1_corrected.csv).
- **How to read:** dots and bars are point estimates and intervals; crosses mean
  too many invalid ratio-bootstrap draws. A panel passes only when all three
  lower bounds cross their red thresholds at the same block.
- **Observed:** expression and atom both pass at block 28.
- **Does not prove:** native causal use or transfer beyond this hierarchy.

### Controlled spectral direction and function

![Controlled spectral localization](figures/fig2_controlled_spectral_localization.png)

- **Purpose:** adjudicate H2 at the admitted block.
- **Metric:** left = projector overlap divided by conditional-Haar expectation;
  right = minimum-domain simultaneous lower bound for keep-only/drop-one gain in
  nats/example.
- **Source:** [controlled_spectrum_block28.csv](tables/controlled_spectrum_block28.csv).
- **How to read:** a star requires both unusual direction overlap and positive
  held-out function. Only band 1 has stars for every domain.
- **Observed:** task rank 8 has band-1 overlap `2.14–2.75×` expectation; shared
  rank 56 has `2.28×`; both keep/drop minima are positive only in band 1.
- **Does not prove:** PCA head itself is the best low-rank classifier; the
  supervised space is merely concentrated there.

### Natural entry, point curves, and task geometry

![Natural entry, rank curves, and geometry](figures/fig3_natural_entry_rank_geometry.png)

- **Purpose:** separate the natural admission verdict, descriptive rank pattern,
  and direction geometry.
- **Metric:** entry CE gain (nats/example), retention point estimate, and
  normalized projector overlap (%).
- **Source:** [natural_entry_corrected.csv](tables/natural_entry_corrected.csv),
  [natural_rank_curves.csv](tables/natural_rank_curves.csv), and
  [natural_task_overlap.csv](tables/natural_task_overlap.csv).
- **How to read:** the center curves do not show formal crossings; the right
  heatmap diagonal is self-overlap and off-diagonals are the comparisons of
  interest.
- **Observed:** entry passes at block 24; point estimates approach one by local
  rank 3/shared rank 15; off-diagonal overlaps are `0.13%–0.37%` against a
  `0.073%` conditional baseline.
- **Does not prove:** shared functional dimension expansion.

### Natural descriptive spectral location

![Natural descriptive spectral location](figures/fig4_natural_spectral_location.png)

- **Purpose:** locate the final natural learned spaces without upgrading H3.
- **Metric:** overlap divided by conditional expectation and mean taskwise
  pointwise keep/drop lower bound in nats/example.
- **Source:** [natural_spectral_location.csv](tables/natural_spectral_location.csv).
- **How to read:** dagger means both keep and drop lower bounds are positive for
  that task and band. The plots are explicitly descriptive.
- **Observed:** both local rank 3 and shared rank 15 concentrate in band 1;
  email and IoT supply positive pointwise held-out function there.
- **Does not prove:** a simultaneous all-task natural spectral verdict.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | State | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| data seal | hashes/count/leak scans | PASSED | — | post-activation row construction | one-dataset external limitation |
| smoke/extraction | 16-row parity then full eight-rank coverage | PASSED | — | hook identity/coverage failure | downstream statistical issues |
| controlled H1 | corrected bootstrap | PASSED at block 28 | block 24 ratios unstable | exact-space result is not confined to old expressions | block specificity |
| controlled H2 | overlap plus keep/drop | PASSED band 1 | — | orientation-only explanation | native causal mechanism |
| natural entry | corrected admission | PASSED block 24 | block 28 numerical instability | “natural \(R_U\) has no added function anywhere tested” | small-gain uncertainty |
| natural H3 | final rank result | INSUFFICIENT | weak denominators / no LCB crossing | point estimates as formal dimensions | shared expansion remains unresolved |

Falsified physical prior: none; the experiment is a linear diagnostic.  
Falsified mathematical model: none universally; natural H3 lacks evidence.  
Falsified operationalization: treating natural point-estimate crossings as
formal functional dimensions.  
Falsified implementation: original joint finite-mask aggregation and automatic
float32 used-rank counting; both superseded.  
Falsified metric: none, but retention ratios are weak when full gain is small.  
Remaining rivals: controlled specificity, linear-readout dependence, one-model
and one-natural-dataset scope, and absence of native causal intervention.

## 10. Full Experiment Record

- Formal job `pt-rkw0whez`: `SUCCEEDED`; run
  `runs/formal-20260820T0820Z`.
- Final conditional job `pt-u9b0tv40`: `SUCCEEDED`; run
  `runs/conditional-natural-20260820T1700Z`.
- Formal extraction totals: expression 1,920; atom 1,920; natural 6,318.
- Controlled corrected result:
  `formal-20260820T0820Z/postprocess_audit_001/controlled_corrected.json`.
- Natural entry corrected result:
  `formal-20260820T0820Z/postprocess_audit_001/natural_corrected.json`.
- Final natural rank result:
  `conditional-natural-20260820T1700Z/natural_rank/natural_rank_result.json`.
- Exact final scientific freeze: `frozen/freeze_amendment_005.json`, SHA
  `0f789153ab2e621ca4b8cd3bb6300f9f2d38c4cd14706b62ce4e0c647c2a9e31`.

## 11. Interpretation

`AWAITING_HUMAN_JUDGMENT`.

Evidence-only reading: the controlled data establish stable frozen low-rank
function at block 28 and locate it in the first TRAIN spectral band. Natural
data establish a small admitted update at block 24 and low task-direction
overlap, but do not adjudicate local-versus-shared functional dimension
ordering. This paragraph is not a substitute for the researcher's closed-book
updated judgment.

## 12. Claim Boundary

**Can report as direct evidence:** the typed registered outcomes and bounded
secondary measurements listed above.  
**Cannot claim:** native causal use, new knowledge, a variance-only Router,
expert specialization or utility, LoRA mechanism, no forgetting, universal
task transfer, or a confirmed natural shared-dimension expansion.

## 13. Next Decision

**Decision:** `AWAITING_HUMAN_JUDGMENT`.  
**Completion criterion:** researcher confirms `question`, `direct result`,
`updated judgment`, `cannot claim`, and one `next decision`.  
**Resume action:** propagate only the confirmed judgment to Summary, Anchor,
Focus and the meeting report.

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `protocol.md` | registered scientific design | frozen before data opening | approved Focus/Anchor | `619472d7...` | yes | yes | scientific body unchanged |
| `data_v1/data_manifest.json` | sealed data provenance | build/seal stage | controlled taxonomy, Wikipedia revisions, MASSIVE 1.0 | `c09af957...` | yes | yes | sealed before activation |
| `frozen/freeze_amendment_005.json` | final exact implementation/scientific identities | Amendments 001–005 | protocol, code, states, data | `0f789153...` | yes | yes | final freeze |
| `controlled_corrected.json` | H1/H2 typed result | Amendment 001 postprocess audit | original controlled arrays/bootstrap | source hash in `curation_manifest.json` | yes | yes | supersedes original controlled verdict |
| `natural_corrected.json` | natural entry typed result | Amendment 001 numerical/interval audit | original natural gate arrays | source hash in `curation_manifest.json` | yes | yes for block 24 | block 28 ineligible |
| `natural_rank_result.json` | final H3/geometry/spectrum | Amendment 005 final conditional run | admitted block-24 state | source hash in `curation_manifest.json` | yes | yes with insufficient verdict | 1700Z only |
| `tables/eligible_result_status.json` | one typed eligible status | curation v1 | three eligible result artifacts | schema identity | yes | yes | original status explicitly superseded |
| `tables/remote_job_receipts.json` | verified ACP terminal states | live read-only job descriptions | jobs `pt-rkw0whez`, `pt-u9b0tv40` | queried 2026-08-20 16:33 UTC | yes | operational | both `SUCCEEDED`, one 8-GPU 5090 node each |
| `figures/fig1...fig4` | central explanation | curation v1 | curated CSV tables | listed in `curation_manifest.json` | yes | yes/bounded as labeled | PDFs also saved |

## 15. Links

- anchor: [A15_07 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_07_layerwise_conditional_fine_discriminant_directions/15_07_layerwise_conditional_fine_discriminant_directions_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- active Focus: [focus_stable_domain_discriminant_subspaces.md](../../../../focus/focus_stable_domain_discriminant_subspaces.md)
- code workspace: `/data/250010109/MoE_Router/experiments/20260820_a15_07_e01_dual_track_heldout_spectrum`
- curated result dir: this directory
- curation manifest: [curation_manifest.json](curation_manifest.json)
- reproducible curation command: `python curate_final_results.py --formal-run runs/formal-20260820T0820Z --natural-run runs/conditional-natural-20260820T1700Z --destination <this-directory>`
- job IDs: `pt-rkw0whez`, `pt-u9b0tv40`
