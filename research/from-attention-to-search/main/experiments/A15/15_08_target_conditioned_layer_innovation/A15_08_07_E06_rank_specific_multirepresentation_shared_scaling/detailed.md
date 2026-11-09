# Detailed: A15_08_07_E06 Rank-Specific Multi-Representation Shared Scaling

Primary Anchor: [15_08_07 semantic-conditioned functional subspace](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_07_semantic_conditioned_functional_subspace_anchor.md)  
Frozen Protocol and registered revision: [protocol.md](protocol.md), including append-only H100, OOF-fold, resume, visualization, and numerical-rank amendments  
Summary: [summary.md](summary.md)  
Result eligibility: **AI_DRAFT_AWAITING_HUMAN_JUDGMENT; evidence ELIGIBLE; registered verdict INSUFFICIENT**

## 0. Quick Recap

**Purpose:** correct the old maximum-rank-prefix experiment and test whether domain union increases functional linear rank across \(R_U\), \(U\), \(G\), and \(\Delta G\).  
**Hypothesis:** an independently learned eight-domain shared subspace should require materially more dimensions than a single-domain subspace, and this direction should replicate on fresh expressions.  
**Experiment logic:** select one layer per representation without TEST, fit every rank independently, evaluate retrospective panels, then unseal an independent confirmation set.  
**Direct result:** same-template shared \(r_{90}\) is 18 for \(U\), 16 for \(G\), and 25 for \(\Delta G\), versus identified local values of 6--7; none of the four shared crossings is identified on confirmation, and confirmation \(R_U\) has no admitted positive full-map benefit.  
**Eligibility:** eligible under the amended Protocol. All resource and OOF changes occurred before TEST access; failed extraction attempts wrote no confirmation row; final audits pass.  
**Verdict:** `INSUFFICIENT`.  
**Claim boundary:** retrospective shared broadening exists for some linear label-readout objects, but robust cross-expression shared-rank growth is not established. Native gate use and expert utility remain out of scope.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| \(X_\ell\) | normalized pre-attention residual | post-attention RMSNorm applied to the block input | 2,048-vector | baseline state and residualizer input | native Router utility |
| \(U_\ell\) | normalized attention update | \(N(h+a)-N(h)\) | 2,048-vector | direct attention-written representation | novelty or causality |
| \(G_\ell\) | native MLP/Router input | \(N(h+a)=X_\ell+U_\ell\) | 2,048-vector | actual same-block Router reference | that the gate uses child labels |
| \(\Delta G_\ell\) | adjacent-layer Router-input change | \(G_\ell-G_{\ell-1}\) | 2,048-vector | newly added cross-layer change candidate | monotone new information |
| \(R_{U,\ell}\) | linearly residualized update | \(U_\ell-\widehat{E}_{lin}[U_\ell\mid X_\ell]\) fitted on TRAIN | 2,048-vector | isolates linear unpredictability from \(X\) | label novelty or nonlinear independence |
| Local task | one domain's eight child labels | one rank curve for one parent domain | rank 1--7 | single-domain requirement | independent union cost |
| Shared task | one input basis, eight domain-specific heads | common basis fitted jointly across selected domains | ranks 1--56 | whether one common coordinate system broadens with task union | rank additivity theorem |
| Benefit \(B_r\) | held-out gain over the registered null | \(CE_{null}-CE_r\); conditional branch uses \(CE_X-CE_{X+R_U,r}\) | nats | functional rather than algebraic criterion | accuracy or utility causality |
| \(r_{90}\) | admitted 90%-retention rank | smallest \(r\) with simultaneous LCB of \(B_r-0.9B_{full}>0\) | projection dimensions | primary decision statistic | a point-curve visual crossing alone |
| `NA_FULL_NOT_ADMITTED` | denominator is not reliably positive | one-sided LCB of full benefit is non-positive | typed outcome | prevents ratios to nonexistent gain | failure of every possible classifier |
| `NA_NOT_IDENTIFIED` | full benefit exists but no rank crosses confidently | no simultaneous LCB crossing in registered grid | typed outcome | preserves uncertainty | proof of high rank beyond the grid |
| Numerical rank | count of singular values above source-precision tolerance | SVD of the fitted concatenated coefficient map | directions | implementation diagnostic | functional retention |
| Entropy effective rank | energy spread across singular values | exponential entropy of normalized squared singular values | effective directions | distinguishes nominal from concentrated dimension | a pass/fail rank |

## 2. Anchor Link And Decision Point

The broad Anchor separates representation geometry, linear accessibility, and Router utility. The active Focus and frozen E06 Protocol own the narrower corrective question: whether local-versus-shared functional-rank growth survives rank-specific learning in four Qwen representations. The older Anchor body still describes the predecessor CLINC-style design and its metadata points to E01, so no Anchor conclusion is silently updated here. Human judgment is required before Sections 7--8 or project state are revised.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Model and data | Qwen3-30B-A3B; frozen 19,200 rows | exact source object SHA `cba20c...ea144`; 19,200 rows | PASS | `freeze/scientific_freeze.json` | none |
| Layer selection | TRAIN/DEVELOPMENT only, scan legal layers | \(R_U\):39, \(U\):48, \(G\):46, \(\Delta G\):47 | PASS | `layer_scan/*/layer_freeze.json` | none |
| Rank fitting | every candidate rank independently optimized | 728/728 rank-specific hashed states | PASS | `fit/fit_manifest.json` | none |
| Conditional OOF baseline | originally five family-grouped folds | changed before TEST to three leave-one-template-family-out folds because TRAIN has exactly three families/domain | AMENDED, PASS | `conditional/manifest.json`; Protocol ledger | preserves family isolation; eligible |
| Compute resource | initially 8×5090 spot | researcher replaced with 4×H100 reserved | AMENDED, PASS | `preflight.json`; Protocol ledger | logistics only |
| Confirmation extraction | sealed 640 rows after freeze | four 160-row H100 shards, exact partition and merge | PASS | `confirmation_extraction/manifest.json` | independent confirmation eligible |
| Failed full/resume attempts | no partial TEST result may leak into tuning | hardcoded device guard, missing `accelerate`, and empty-directory source audit all failed before any confirmation row | PASS | resume receipts and logs | no result-derived tuning |
| Bootstrap | 2,000 template-family resamples; worst-domain simultaneous rule | executed unchanged | PASS | `analysis/results.json` | none |
| Visualization | do not plot undefined retention | first render divided by near-zero non-admitted benefits; corrected to mask ratios and show conditional nats | POST-HOC PRESENTATION FIX | `figures/render_manifest.json` | primary results unchanged |
| Numerical-rank diagnostic | source-precision numerical rank | initial float64 threshold counted float32 noise; complete reaggregation corrected 840/3,360 rows | POST-HOC DIAGNOSTIC FIX | `diagnostic_reaggregation_receipt.json` | six decision-bearing artifacts byte-identical |
| Completion | every registered artifact and guard present | all 17 enhanced audit checks pass | PASS | `completion_audit.json` | full evidence chain complete |

Frozen Protocol revision: scientific rules frozen at execution approval; all later changes are append-only eligibility-preserving amendments.  
Execution scope approved: implementation, smoke, and full execution; user explicitly required 4×H100 reserved.  
Retries and exclusions: two unallocated 5090 submissions are ineligible; H100 runtime and OOF smoke failures are ineligible; only `pt-v0b1o6sb` plus diagnostic correction `pt-riot0k4f` contribute final artifacts.  
Missing conditions or artifacts: none under the Protocol.  
Post-hoc analyses: no new scientific comparison; only visualization admission masking and numerical-rank precision repair.

## 4. Actual Setup

**Research question:** does rank-specific eight-domain sharing remain broader than one local domain, and does it replicate?  
**Data construction and provenance:** frozen 19,200-row hierarchy with eight parent domains and eight child classes per parent; object tensor shape `[48, 19200, 2, 2048]`; decision token is the final token following `Answer:`.  
**Train / development / confirmation split:** TRAIN 11,520; DEVELOPMENT 2,560; same-template TEST 2,560; new-template TEST 2,560; independently constructed sealed confirmation 640.  
**Learning task and permitted supervision:** domain identity is known; predict the eight child labels within each domain. No TEST row selects a layer, ridge, restart, or rank.  
**Model:** frozen `/data/share/Qwen3-30B-A3B`, 48 blocks, hidden size 2,048.  
**Representations:** globally TRAIN-standardized \(R_U\), \(U\), \(G\), and \(\Delta G\); conditional audit fits \(R_U\) corrections beyond an \(X\)-only baseline.  
**Objective:** rank-constrained shared linear basis plus domain-specific ridge heads, minimizing TRAIN squared contrast loss; DEVELOPMENT cross entropy selects among six candidates per state.  
**Optimization:** ridge \(\{10^{-3},10^{-2}\}\); three fixed restart seeds; learning rate 0.04; 100 basis steps for eight-domain states and 70 for smaller task-count states.  
**Rank grid:** local ranks 1--7; task counts 2 and 4 use ranks 1--14 and 1--28; eight-domain shared ranks 1--56.  
**Controls:** old rank-56 prefix, local-union oracle, Haar subspace, permutation labels, synthetic known rank, same-layer representation guard, overlap diagnostics.  
**Uncertainty:** 2,000 family-level bootstrap draws; simultaneous one-sided correction across ranks; worst-domain decision statistic.  
**Changed variables:** representation, task count, requested rank, and control construction.  
**Held fixed:** model, token position, taxonomy, source arrays, splits, standardization, task labels, selection data, metric, and bootstrap rule.  
**Known setup limitations:** one model, one taxonomy, one token position, linear objectives, fixed nested domain order for task-count scaling, and only 640 independent confirmation rows.

## 5. Metrics And Registered Decision Rules

For standalone representations, per-row benefit is \(B_r=\log 8-CE_r\). For the conditional branch, \(B_r=CE_X-CE_{X+R_U,r}\). A full per-domain coefficient map supplies \(B_{full}\).

\[
r_{90}=\min\left\{r:\operatorname{LCB}_{sim}(B_r-0.9B_{full})>0\right\}.
\]

The independence unit is the template family. A non-positive one-sided full-map lower bound yields `NA_FULL_NOT_ADMITTED`. A positive full map without a simultaneous crossing yields `NA_NOT_IDENTIFIED`. Secondary balanced accuracy, point retention, numerical rank, effective rank, and overlaps cannot rescue an unidentified primary result.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Per-rank correction is implemented | independent fit at every rank | 728 NPZ states and receipts | six DEVELOPMENT candidates/state | complete receipt audit | 728/728; synthetic rank-3 MSE \(8.89\times10^{-5}\) versus rank-2 0.7134 | ELIGIBLE | PASS | implementation validity, not hypothesis |
| Same-template \(U\) broadens under union | shared \(r_{90}\) above local values | states -> shared/local curves | 2,000 family bootstraps | simultaneous worst-domain LCB | shared 18; locals `[7,6,7,6,7,7,7,7]`; local sum 54 | RETROSPECTIVE | SUPPORT | prior-opened TEST |
| Same-template \(G\) broadens under union | same | same | same | same | shared 16; locals `[7,7,6,7,7,7,6,6]`; sum 53 | RETROSPECTIVE | SUPPORT | prior-opened TEST |
| Same-template \(\Delta G\) broadens under union | same | same | same | same | shared 25; all locals 7; sum 56 | RETROSPECTIVE | SUPPORT | prior-opened TEST |
| \(R_U\) shared rank is identified | admitted full and crossing | same | same | same | no shared crossing on same/new; confirmation full-map minimum LCB -3.270 | ELIGIBLE | INSUFFICIENT | cannot assign \(r_{90}\) |
| Retrospective pattern replicates | identified confirmation crossing | sealed confirmation objects | frozen states evaluated once | 2,000 family bootstraps | \(U\), \(G\), \(\Delta G\): `NA_NOT_IDENTIFIED`; \(R_U\): `NA_FULL_NOT_ADMITTED` | ELIGIBLE | INSUFFICIENT | no robust expansion claim |
| Conditional \(R_U\mid X\) adds access | positive full-map lower bounds | three-fold OOF \(X\) artifacts | frozen correction states | same bootstrap rule | all panels `NA_FULL_NOT_ADMITTED`; confirmation LCBs -10.252 to -2.809 nats | ELIGIBLE | NOT ADMITTED | only linear correction beyond this \(X\) baseline |
| Rank diagnostics are valid | numerical rank \(\le\) requested rank | original and candidate tables | source-precision tolerance; full reaggregation | exact six-artifact hash comparison | 840 corrected rows; 0 violations; main artifacts identical | ELIGIBLE, SECONDARY | PASS | not functional rank |

## 7. Main Results

### Eligible decision evidence

| Representation | Selected block | Same-template local \(r_{90}\) | Same-template shared \(r_{90}\) | New-template shared \(r_{90}\) | Confirmation shared result | Minimum confirmation full-map LCB |
| --- | ---: | --- | ---: | --- | --- | ---: |
| \(R_U\) | 39 | 7 for seven domains; one unidentified | `NA_NOT_IDENTIFIED` | `NA_NOT_IDENTIFIED` | `NA_FULL_NOT_ADMITTED` | -3.270 |
| \(U\) | 48 | 6--7, sum 54 | 18 | `NA_NOT_IDENTIFIED` | `NA_NOT_IDENTIFIED` | 0.340 |
| \(G\) | 46 | 6--7, sum 53 | 16 | `NA_NOT_IDENTIFIED` | `NA_NOT_IDENTIFIED` | 0.346 |
| \(\Delta G\) | 47 | all 7, sum 56 | 25 | 43 | `NA_NOT_IDENTIFIED` | 0.202 |

The full map is positively admitted on confirmation for \(U\), \(G\), and \(\Delta G\), but the frozen shared rank-specific curves do not achieve an uncertainty-controlled 90% worst-domain crossing. This is not the same failure as \(R_U\), whose full map itself is not admitted.

### Secondary accuracy observations

At shared rank 56, mean/worst-domain balanced accuracy is 0.367/0.188 for \(U\), 0.425/0.263 for \(G\), and 0.338/0.163 for \(\Delta G\) on confirmation. \(R_U\) is 0.134/0.063, near or below the eight-class chance reference. These values describe readability; they do not determine \(r_{90}\).

### Bounded retrospective task-count scaling

On the same-template panel, identified \(U\) ranks grow `7 -> 9 -> 11 -> 18` for 1, 2, 4, and 8 tasks; \(G\) grows `7 -> 9 -> 12 -> 16`; \(\Delta G\) grows `7 -> 9 -> 12 -> 25`. The fixed nested domain order and lack of confirmation crossings prevent a general task-count scaling law.

### Failed or ambiguous evidence

- \(R_U\) shared rank is never identified and its confirmation full map fails admission.
- The conditional \(R_U\mid X\) branch is negative on all panels.
- Confirmation point curves are noisy and often non-monotone; point crossings cannot replace simultaneous LCB crossings.
- No secondary control rescues the registered confirmation requirement.

### Ineligible evidence

The stopped 5090 jobs, failed H100 smoke jobs, failed extractor attempts, invalid-ratio figures, and pre-correction numerical-rank table are retained for provenance but are not claim evidence.

## 8. Visualization Results

### Functional rank across representation and evaluation panel

![Functional rank comparison](figures/functional_rank_comparison.png)

**Purpose:** show how direct per-rank shared fits compare with the old prefix, local-union oracle, and Haar control.  
**Metric and unit:** worst-domain point retention, \(B_r/B_{full}\); x-axis is requested projection dimensions.  
**Raw source:** [shared_curves.csv](tables/shared_curves.csv).  
**Aggregation and uncertainty:** plotted lines are point summaries; typed verdicts use the separate 2,000-draw simultaneous bootstrap in `results.json`.  
**Observed result:** clean early same-template growth for \(U/G/\Delta G\); no confirmed shared crossing on the independent confirmation panel.  
**Allowed conclusion:** retrospective linear-accessibility broadening exists for some representations.  
**Does not prove:** confirmation, native gate use, or expert utility.

### Conditional \(R_U\) benefit beyond \(X\)

![Conditional R_U comparison](figures/conditional_rank_comparison.png)

**Purpose:** expose whether \(R_U\) adds linear child-label access after an \(X\) baseline.  
**Metric and unit:** equal-domain mean cross-entropy benefit in nats; zero is no improvement. Undefined retention ratios are intentionally not drawn.  
**Raw source:** [conditional_shared_curves.csv](tables/conditional_shared_curves.csv).  
**Observed result:** direct, prefix, and local-union conditional corrections are negative; Haar remains around zero but no full-map benefit is admitted.  
**Allowed conclusion:** this registered linear correction does not establish incremental \(R_U\) access.  
**Does not prove:** \(R_U\) contains no nonlinear or differently conditioned information.

### Task-count scaling on confirmation

![Task-count scaling](figures/task_count_scaling.png)

The \(R_U\) panel is intentionally blank because every full-map denominator is unadmitted. Other representations show point curves only; none yields an eight-task confirmation \(r_{90}\).

### Layer selection and same-layer guard

![Layerwise predictive utility](figures/layerwise_predictive_utility.png)

![Matched-layer guard](figures/matched_layer_dev_accuracy.png)

TRAIN/DEVELOPMENT selection places \(R_U\) at block 39, well below the late-layer readability of \(U/G/\Delta G\). The matched-layer panel shows this is a representation difference under the frozen linear probe, not evidence of causal Router usefulness.

### Corrected numerical and effective rank

![Corrected rank diagnostics](figures/rank_diagnostics.png)

Numerical rank now respects float32 source precision and never exceeds requested rank. Entropy effective rank is smaller and measures energy concentration. Neither curve is the registered functional \(r_{90}\).

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out | What remains live |
| --- | --- | --- | --- | --- | --- |
| Source freeze | hashes, split checks, preflight | PASS | — | source drift | one-model external validity |
| Layer scan | all legal Qwen blocks | PASS | — | blind reuse of old block 24/28 | selected-layer variance across reps |
| Rank implementation | synthetic and prefix gap | PASS | — | maximum-rank prefix masquerading as direct fit | non-convex optimization limits |
| Null control | eight permuted-domain LCBs non-positive | PASS | — | trivial label leakage | semantic shortcuts in real data |
| Retrospective rank | same/new panels | MIXED | several shared crossings identified | old literal `7/56` fact | bounded same-template broadening |
| Independent confirmation | 640 rows | INSUFFICIENT | no shared simultaneous crossing; \(R_U\) full not admitted | robust cross-expression rank-growth claim | better-defined stable target or more confirmation power |
| Conditional \(R_U\mid X\) | all panels | FAIL TO ADMIT | correction decreases CE benefit | old conditional increment reading | alternate nonlinear conditioning, untested |
| Visualization audit | all six figures | PASS after repair | undefined ratios and precision bug corrected | misleading \(10^{30}\) axes and rank 64 at rank 1 | figure interpretation limits |

**Falsified physical prior:** not falsified globally; the experiment only fails to confirm robust cross-expression shared-rank expansion.  
**Falsified mathematical model:** the old `rank-56 prefix = optimal rank-r solution` operationalization is rejected.  
**Falsified operationalization / proxy:** `7 versus 56` and the conditional \(R_U\mid X\) gain are not valid established facts here.  
**Falsified implementation:** initial resource-specific extractor and float64-on-float32 rank threshold were invalid and corrected.  
**Falsified metric:** no; typed nonadmission behaved as intended.  
**Remaining rival explanations:** confirmation expressions may shift the label-accessible subspaces; 640 rows may leave simultaneous bounds underpowered; same-template broadening may rely on expression-family regularities; linear child-label access may not match Router-relevant utility.

## 10. Full Experiment Record

| Job | Role | Outcome | Eligibility note |
| --- | --- | --- | --- |
| `pt-qka7865q` | initial 5090 smoke | stopped before allocation | no run root |
| `pt-hob3j8jq` | corrected 5090 smoke | stopped at zero replicas | superseded by user-approved H100 resource |
| `pt-735me1i6` | first H100 smoke | failed before run root | wrong 5090 runtime |
| `pt-znkcm1kx` | second H100 smoke | failed in conditional construction | exposed infeasible five-fold family split before TEST |
| `pt-ft8h2x91` | corrected H100 smoke | SUCCEEDED | all smoke guards passed |
| `pt-21hckxi9` | full fit | partial: completed pre-TEST chain, 728 fits, overlaps | extractor had hardcoded 5090 guard; no confirmation row |
| `pt-huqq6imc` | first resume | failed before forward | missing optional `accelerate`; no confirmation row |
| `pt-q5gc50uo` | second resume | audit-stopped | empty directory only; no extraction |
| `pt-v0b1o6sb` | third resume | SUCCEEDED | 640-row extraction, analysis, figures, completion |
| `pt-riot0k4f` | diagnostic reaggregation | SUCCEEDED | main result hashes identical; rank diagnostic corrected |

Final resource receipt: ACP workspace `share-space`, cluster `share-cluster`, spec `n6ls.iu.i40.4`, one node, four NVIDIA H100 80GB GPUs, four processes, `reserved` quota.

## 11. Interpretation

The corrected experiment changes the old mental model in two ways. First, a shared eight-domain space is not forced to use the sum of eight seven-dimensional label contrasts: it can reuse directions, so 16--25 dimensions can support tasks whose individual requirements are 6--7. Second, this retrospective pattern is not stable enough across a genuinely fresh expression bank to be called a confirmed property of the representation. The evidence therefore supports a bounded “partial union growth with sharing” observation, not a robust or intrinsic semantic-rank theorem.

This interpretation remains an AI draft. The researcher must confirm or correct the knowledge wording before it is promoted to the Focus, Anchor, or daily report.

## 12. Claim Boundary

**Can claim:** per-rank correction invalidates the old maximum-rank-prefix interpretation; same-template \(U\), \(G\), and \(\Delta G\) show a shared linear label-accessibility requirement broader than one local task; that relation is not independently confirmed on fresh expressions.  
**Cannot claim:** stable intrinsic semantic rank, a universal `7/56` law, native Router use, expert utility, causal benefit of projection, nonlinear low rank, or justification to start representation-space learning.

## 13. Next Decision

**Decision:** `AWAITING_HUMAN_JUDGMENT` — confirm or correct this proposed update: “the old `7/56` fact is rejected; retrospective shared-rank expansion remains for some representations, but robust cross-expression expansion is unestablished.”  
**Completion criterion:** the researcher records `Direct result`, `My conclusion`, `Cannot claim`, and exactly one next scientific decision in the active Focus.  
**Resume action:** after that confirmation, synchronize the Anchor boundary and create the delayed daily report; do not open a new Router or representation-learning run before the decision is explicit.

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Hash or identity | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [protocol.md](protocol.md) | frozen contract and amendments | experiment-card | Focus + Anchor | append-only execution ledger | yes | yes | owns registered verdict rule |
| worker `preflight.json` | resource/source gate | full pipeline | source arrays + ACP | `h100-4-reserved`, passed | yes | yes | four H100 devices |
| worker `fit/fit_manifest.json` | 728 state registry | four-process fit | TRAIN/DEV features | 728 hashed receipts | yes | yes | all `fit_kind=rank_specific` |
| worker `confirmation_extraction/manifest.json` | sealed extraction identity | four model replicas | confirmation v5 | objects SHA `95b3fe...0f03` | yes | yes | exact 4×160 merge |
| worker `analysis/results.json` | typed \(r_{90}\) outcomes | aggregate_results | frozen states + three panels | SHA `c79f23...746d2` | yes | yes | main result unchanged by diagnostic fix |
| [local curves](tables/local_curves.csv) | per-domain ranks | aggregate_results | results | `548f3e...1ea04` | yes | yes | primary support |
| [shared curves](tables/shared_curves.csv) | shared/control rank curves | aggregate_results | results | `0360e4...9bc16` | yes | yes | primary support |
| [task-count curves](tables/task_count_curves.csv) | nested task scaling | aggregate_results | results | `ceed35...cc615` | yes | bounded | fixed nested domains |
| [conditional local curves](tables/conditional_local_curves.csv) | local \(R_U\mid X\) | aggregate_results | OOF baseline | `be12d0...c165` | yes | yes | nonadmission evidence |
| [conditional shared curves](tables/conditional_shared_curves.csv) | shared \(R_U\mid X\) | aggregate_results | OOF baseline | `4a2609...079` | yes | yes | nonadmission evidence |
| [rank diagnostics](tables/rank_diagnostics.csv) | numerical/effective rank | corrected reaggregation | coefficient maps | `e05540...bc8f` | yes | secondary | 0 rank violations |
| [functional figure](figures/functional_rank_comparison.png) | central point curves | renderer v2 | shared table | `2b9e21...38c6` | yes | yes with table | visual crossing is not verdict |
| [conditional figure](figures/conditional_rank_comparison.png) | conditional benefit | renderer v2 | conditional table | `38caaa...4294` | yes | yes | nats, not undefined ratio |
| [task-count figure](figures/task_count_scaling.png) | confirmation scaling | renderer v2 | task table | `29160b...f517` | yes | bounded | masks nonadmitted \(R_U\) |
| [layerwise figure](figures/layerwise_predictive_utility.png) | selected blocks | renderer v2 | layer scans | `5dcf37...aaf` | yes | diagnostic | TEST-blind |
| [matched-layer figure](figures/matched_layer_dev_accuracy.png) | representation guard | renderer v2 | matched panel | `e4760d...b2b1` | yes | diagnostic | no rank verdict |
| [rank figure](figures/rank_diagnostics.png) | corrected rank accounting | renderer v2 | corrected table | `ceb73c...e006` | yes | secondary | not \(r_{90}\) |
| worker `completion_audit.json` | final completeness | audit v1 enhanced | all artifacts | 17/17 checks pass | yes | yes | final gate |
| worker `diagnostic_reaggregation_receipt.json` | diagnostic-only proof | verification script | original/candidate analysis | 6 main hashes identical | yes | yes | 840 corrected rows |

## 15. Links

- anchor: [15_08_07 anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_08_target_conditioned_layer_innovation/subanchors/15_08_07_semantic_conditioned_functional_subspace_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- active Focus: [focus_rank_specific_multirepresentation_subspace.md](../../../../focus/focus_rank_specific_multirepresentation_subspace.md)
- code workspace: `/data/250010109/MoE_Router/experiments/20260827_a15_08_06_e06_rank_specific_multirepresentation_shared_scaling/`
- result directory: worker `runs/full-20260827T151500Z`
- figure directory: [figures/](figures)
- table directory: [tables/](tables)
- model: `/data/share/Qwen3-30B-A3B`
- job IDs: `pt-ft8h2x91`, `pt-21hckxi9`, `pt-v0b1o6sb`, `pt-riot0k4f` (eligible chain); earlier failures listed in Section 10
- reproducibility: worker `scripts/resume_after_fit.sh`, `scripts/reaggregate_diagnostic_fix.sh`, and `audit_completion.py`
