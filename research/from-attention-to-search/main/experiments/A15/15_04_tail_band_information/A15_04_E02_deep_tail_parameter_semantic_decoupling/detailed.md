# Detailed: A15_04_E02 Deep-Tail Parameter/Semantic Decoupling

Primary Anchor: [A15_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_04_tail_band_information/15_04_tail_band_information_anchor.md)  
Frozen Protocol and registered revision: [A15_04_E02_r1](protocol.md)  
Summary: [summary.md](summary.md)  
Result eligibility: `ELIGIBLE`; researcher knowledge-update state `AWAITING_HUMAN_JUDGMENT`.

## 0. Quick Recap

- **Purpose:** determine whether the old narrow deep-tail parameter overlap and the A15_04_E01 negative broad-tail semantic change are genuinely decoupled when evaluated in the same pre-fixed terminal spaces.
- **Hypothesis:** terminal parameter geometry is shared across layers, but late conditional-fine variance does not increasingly occupy it.
- **Experiment logic:** exactly reproduce the old source result, construct cross-fitted shared terminal spaces at 128/256/512/2,048 directions, then measure parameter overlap and conditional-fine semantic depth change in those same spaces.
- **Direct result:** all four parameter overlaps exceed matched random q95; all four semantic changes have 95% upper endpoints below zero; all 16 split signs are negative.
- **Eligibility:** all registered inputs, source reproduction, numerical guards, tests, conditions, and artifacts passed without amendment.
- **Registered verdict:** `SUPPORTED_DECOUPLED_TERMINAL_SKELETON`.
- **Claim boundary:** static frozen-set geometry only; no use, task, causality, nonlinear readability, or Router claim.

## 1. Terminology And Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| terminal width | how many lowest-gain parameter directions are retained | last 128/256/512/2,048 eigenvectors | directions | tests resolution dependence without post-hoc selection | functional module |
| old pairwise overlap | average similarity of the same terminal band between every pair of layers | mean \(\|V_i^\top V_j\|_F^2/w\) over 630 pairs | normalized projector overlap in [0,1] | closes the old evidence source | independent model replication |
| global consensus overlap | similarity of terminal orientations learned from mutually exclusive layer groups | \(\|Q_{odd}^\top Q_{even}\|_F^2/w\) | normalized projector overlap in [0,1] | operational definition of a shared parameter-geometric component | identical directions at every layer |
| conditional-fine covariance | child-class variation after removing each parent-class center | equal weight over 8 parents and 8 children | activation squared before normalization | sole semantic object | all fine information |
| dimension-normalized enrichment | semantic variance captured relative to a random same-size space | capture divided by \(w/4096\) | ratio; random mean 1 | permits width comparison | task accuracy or causal use |
| semantic entry change \(T_w\) | difference in occupancy between late and early layers | median enrichment on layers 25--35 minus layers 1--12 | enrichment difference | tests “increasingly enters” | literal information transport |
| parameter skeleton | a shared component of terminal parameter orientation | old source reproduction plus global overlap above Haar q95 at all registered widths | conjunctive geometric status | function, necessity, or complete invariance |

## 2. Anchor Link And Decision Point

A15_04_E01 closed the registered broad F9--F16 shared-tail explanation: the broad tail's conditional-fine enrichment decreased from early to late depth although global parameter-tail overlap exceeded random. The remaining explanatory rival was resolution averaging: a narrower terminal core might be both highly shared and a destination of late semantic entry, while the full 2,048 directions decline.

A15_04_E02 was frozen to test that rival only. It cannot reopen the original broad-tail verdict, select a new tail boundary from the result, or infer tail function.

## 3. Protocol Freeze, Conformance, And Deviations

| Registered item | Expected | Actual | Status | Evidence | Eligibility impact |
| --- | --- | --- | --- | --- | --- |
| Protocol revision | `A15_04_E02_r1` | `A15_04_E02_r1` | pass | run input manifest and verdict | none |
| execution scope | implementation, tests, preflight, one full artifact-only reanalysis | exactly one full run; no model replay or training | pass | worker run root | none |
| parameter source | complete native bases and 630 old pair records | all present and finite | pass | input manifest | none |
| semantic source | eligible A15_04_E01 recovered raw \(\Delta n\) | recovery manifest valid; 36 × 512 × 4096 finite values | pass | input manifest | none |
| widths | 128/256/512/2,048 | exact | pass | parameter and semantic tables | none |
| semantic object | conditional-fine only | exact | pass | analysis code and layer table | none |
| source reproduction | absolute error at most \(10^{-12}\) | zero for all four widths | pass | [source table](tables/source_reproduction.csv) | none |
| consensus numerical guards | orthogonality and residual at most \(10^{-5}\) | all pass | pass | [guard table](tables/consensus_guards.csv) | none |
| random control | 512 Haar draws, seed `15040201` | exact | pass | worker resampling artifact | none |
| uncertainty | 2,000 paired grouped resamples, seed `15040202` | exact | pass | worker resampling artifact | none |
| split guards | odd/even layers and design/confirmation expressions | 16/16 present | pass | [split table](tables/semantic_split_robustness.csv) | none |
| required figures | primary joint figure plus stage diagnostic | both present and visually audited | pass | [figures](figures) | none |

Frozen Protocol revision: `A15_04_E02_r1`.  
Execution scope approved: implementation, tests, preflight, and one full reanalysis.  
Amendments: none.  
Retries and exclusions: none.  
Missing conditions or artifacts: none.  
Post-hoc analyses: none.

## 4. Actual Setup

- **Data:** frozen 512 records = 8 parents × 8 children × 4 templates × 2 expression bundles.
- **Representation:** \(\Delta n_\ell=RMSNorm_\ell(x_\ell+a_\ell)-RMSNorm_\ell(x_\ell)\), recovered from the already eligible A15_04_E01 source.
- **Parameter operator:** \(W_{gate,\ell}^{\top}W_{gate,\ell}+W_{up,\ell}^{\top}W_{up,\ell}\) in native MLP-input coordinates.
- **Decision layers:** 1--35; early 1--12; late 25--35; block 36 descriptive only.
- **Cross-fitting:** evaluated odd layers use an even-built consensus space and evaluated even layers use an odd-built space.
- **Changed variable:** terminal width only.
- **No learning:** no train/development split, model fitting, objective, optimizer, step, checkpoint, or selection rule.
- **Randomness:** 512 Haar overlap draws and 2,000 grouped parent/template resamples with registered seeds.
- **Known limitation:** one frozen model and one balanced synthetic semantic set; layers and layer pairs are repeated measurements rather than independent model replicates.

Worker code and full-run output:

- `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_e02_deep_tail_parameter_semantic_decoupling/`
- `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_e02_deep_tail_parameter_semantic_decoupling/runs/a15-04-e02-full-20260809T162751Z/`

## 5. Metrics And Registered Decision Rules

For every terminal width \(w\), the parameter clause requires global odd/even consensus overlap \(C_w\) above the q95 of 512 random rank-\(w\) overlaps. The semantic clause requires the 95% upper endpoint of

\[
T_w=\operatorname{median}_{\ell=25:35}e_{\ell,w}
-\operatorname{median}_{\ell=1:12}e_{\ell,w}
\]

to be below zero, where \(e_{\ell,w}\) is conditional-fine variance capture divided by \(w/4096\). All odd/even layer and design/confirmation expression changes must also be negative. All four widths must pass both clauses for `SUPPORTED_DECOUPLED_TERMINAL_SKELETON`.

A protected positive contradiction requires one width's 98.75% lower endpoint above zero and all four split signs positive. Anything else is `MIXED_RESOLUTION_OR_INSUFFICIENT`.

## 6. Evidence Lineage

| Claim or decision | Protocol criterion | Raw artifact | Computation / revision | Aggregation and uncertainty | Observed value | Eligibility | Verdict | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| old tail-overlap source is reproduced | error \(\le10^{-12}\) | 630 pair records and old consolidated table | `A15_04_E02_r1` source reproduction | all pair records | zero error at all widths | eligible | pass | no independent models |
| terminal parameter geometry is shared | \(C_w>\) Haar q95 for all widths | complete native parameter bases | opposite-parity projector consensus | 512 Haar draws | 0.824/0.739/0.636/0.694 versus 0.032/0.063/0.125/0.500 q95 | eligible | pass | shared component, not identity |
| same terminal spaces do not gain late conditional-fine occupancy | each 95% upper endpoint \(<0\) | recovered raw \(\Delta n\) and frozen labels | cross-fitted capture divided by \(w/4096\) | 2,000 paired parent/template resamples | \(T_w=-3.040/-1.755/-0.946/-0.103\); every interval below zero | eligible | pass | static covariance, not literal transport |
| result is not controlled by a layer or expression split | all 16 split signs negative | same raw inputs | parity- and expression-restricted median changes | 4 checks per width | 16/16 negative | eligible | pass | correlated guards |
| joint registered interpretation | all parameter and semantic clauses pass | preceding eligible rows | `A15_04_E02_r1` adjudicator | conjunctive; widths not averaged | all four widths pass | eligible | `SUPPORTED_DECOUPLED_TERMINAL_SKELETON` | geometry only |

## 7. Main Results

### 7.1 Source closure

The old all-layer-pair native-tail means reproduce exactly: 0.232453 at width 128, 0.203921 at 256, 0.219606 at 512, and 0.528657 at 2,048. Relative to random expected overlap, these are 7.44×, 3.26×, 1.76×, and 1.06×. The new analysis therefore uses the same parameter phenomenon rather than a reconstructed substitute.

### 7.2 Global joint result

| Width | Consensus overlap | Haar q95 | Early semantic enrichment | Late semantic enrichment | \(T_w\) | 95% interval |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 128 | 0.823956 | 0.031773 | 3.869970 | 0.829706 | -3.040264 | [-3.280149, -2.257119] |
| 256 | 0.738803 | 0.063033 | 2.617225 | 0.861949 | -1.755276 | [-2.083955, -1.334088] |
| 512 | 0.635814 | 0.125481 | 1.834037 | 0.887597 | -0.946441 | [-1.165518, -0.755682] |
| 2,048 | 0.694019 | 0.500324 | 1.053568 | 0.950114 | -0.103453 | [-0.142254, -0.074373] |

Parameter stability becomes particularly strong inside the deepest 128--512 directions, but their semantic depth change becomes more negative, not positive. Late median enrichment is below the random-dimension mean of 1 at every width; this is a point comparison, not a separately registered significance test against a semantic Haar distribution.

### 7.3 Split reliability

All four registered split changes are negative at every width. At width 128 they range from -3.138 to -2.299; at 256 from -1.960 to -1.395; at 512 from -1.048 to -0.794; and at 2,048 from -0.134 to -0.096. Full values are in [semantic_split_robustness.csv](tables/semantic_split_robustness.csv).

## 8. Visualization Results

### Same terminal spaces are parameter-stable but do not gain late conditional-fine enrichment

![Parameter stability and semantic entry are decoupled](figures/figure0_parameter_semantic_decoupling.png)

- **Purpose:** inspect the two clauses for all pre-fixed widths without selecting a width afterward.
- **Raw source:** [parameter geometry](tables/parameter_geometry.csv) and [semantic depth change](tables/semantic_depth_change.csv).
- **Aggregation:** odd/even consensus overlap with 512-Haar q95; early/late medians with 2,000 grouped-bootstrap intervals.
- **How to read:** left above dashed random q95 means a cross-layer parameter component exists; right below zero means that exact shared space loses rather than gains conditional-fine enrichment at late depth.
- **Observed result:** all four widths satisfy both clauses.
- **Allowed conclusion:** parameter stability and increasing late conditional-fine occupancy are decoupled at these resolutions.
- **Does not prove:** function, use, necessity, semantic absence, or nonlinear behavior.

### Stage diagnosis

![Stage-resolved geometry](figures/figure1_stage_diagnostics.png)

- **Purpose:** distinguish complete global invariance from a stable component with stage reorientation.
- **Raw source:** [stage semantic geometry](tables/stage_semantic_geometry.csv) and [stage parameter overlap](tables/stage_parameter_overlap.csv).
- **Observed result:** every early/late internal and early-built-versus-late-built parameter overlap exceeds matched Haar q95, but the early-built terminal spaces capture late semantics below the random-dimension mean while late-built spaces still capture early semantics above it.
- **Interpretation:** the terminal parameter geometry contains a shared component but is not perfectly unchanged across stages; the semantic asymmetry is tied to evaluated representation depth rather than merely which stage supplied the parameter basis.
- **Limitation:** stage diagnostics are non-primary and cannot establish a temporal mechanism.

## 9. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | What this rules out | What remains live |
| --- | --- | --- | --- | --- |
| source reproduction | four exact old means | passed | source-definition drift | old pair dependence |
| global parameter geometry | four overlaps above q95 | passed | random terminal orientation | incomplete stage invariance |
| global semantic geometry | four negative intervals | passed | hidden narrow terminal destination | other semantic objects or nonlinear codes |
| split reliability | 16/16 negative | passed | one parity or wording half drives sign | other data distributions |
| stage parameter geometry | all stage overlaps above q95 | passed | wholly unrelated early/late random spaces | partial rotation |
| stage semantic transfer | late evaluations stay low; early evaluations stay high | explanatory | basis-source stage alone explains semantic result | representation-dependent alignment mechanism |

Falsified physical prior: none; the old parameter-sharing observation reproduces.  
Falsified mathematical model: the rival in which broad width hides a narrower terminal semantic destination is rejected on this set.  
Falsified operationalization / proxy: none within the registered conditional-fine covariance; other semantic operationalizations remain outside scope.  
Falsified implementation: none.  
Falsified metric: none.  
Remaining rival: late fine information may occupy nonterminal parameter regions, a nonlinear code, or a semantic object not captured by this covariance.

## 10. Full Experiment Record

- Full run: `a15-04-e02-full-20260809T162751Z`.
- Runtime: 79.888 seconds on one NVIDIA H100 80GB GPU.
- Tests before full run: 9 passed.
- Full-run conditions: 2,000 grouped bootstrap replicates; 512 Haar overlap draws; four widths; 36 available layers; 35 decision layers.
- Failed runs: none.
- Smoke scientific runs: none by Protocol; only engineering tests and preflight.
- Publication, sync, commit, and push: not performed.

## 11. Interpretation

The evidence separates two objects that were previously easy to conflate. The parameter result says that a terminal orientation can be recovered consistently from mutually exclusive layer groups. The semantic result says that conditional-fine attention-induced MLP-input increments become less aligned with that orientation at late depth. The narrower and more parameter-stable the tested terminal core is, the larger the observed semantic decrease becomes.

Calling this a “skeleton” is therefore a geometric shorthand: a stable shared component of parameter orientation. It is not a functional label. The evidence supports decoupling between parameter rank identity and the depth chronology of one semantic covariance, not a claim that the model stores nothing useful in the tail.

## 12. Claim Boundary

**Can claim:** on the frozen 512-record set, native terminal parameter spaces at widths 128/256/512/2,048 are globally shared above matched random, while conditional-fine \(\Delta n\) enrichment in those same cross-fitted spaces decreases from early to late layers.

**Cannot claim:** the tail is unused, random, semantically empty, task-irrelevant, causally inert, a near-null sink, or unsuitable for nonlinear routing. The experiment does not test MLP output effect, task loss after intervention, nonlinear probes, or distribution shift.

## 13. Next Decision

**Decision:** researcher confirms or corrects the proposed knowledge update and boundary.  
**Completion criterion:** a human-approved statement explicitly distinguishes shared parameter geometry from increasing late semantic occupancy and rejects any function claim.  
**Resume action:** after confirmation, update only A15_04 Anchor sections 7--8 and create the bounded problem focus; do not start a functional or Router experiment from this result.

## 14. Artifact Manifest

| Artifact | Purpose | Producer / revision | Source inputs | Complete | Claim-eligible | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `protocol.md` | frozen decision contract | `A15_04_E02_r1` | A15_04 Anchor and user approval | yes | yes | no amendment |
| `tables/source_reproduction.csv` | old evidence closure | full analysis | 630 pair records and old summary table | yes | yes | zero reproduction error |
| `tables/parameter_geometry.csv` | primary parameter clause | full analysis | complete native bases and Haar draws | yes | yes | all widths above q95 |
| `tables/semantic_depth_change.csv` | primary semantic clause | full analysis | recovered raw \(\Delta n\) and grouped bootstrap | yes | yes | all intervals negative |
| `tables/semantic_split_robustness.csv` | reliability guards | full analysis | same eligible inputs | yes | yes | 16/16 negative |
| `tables/stage_semantic_geometry.csv` | non-primary stage diagnosis | full analysis | early/late consensus spaces | yes | bounded | cannot change verdict |
| `tables/stage_parameter_overlap.csv` | non-primary stage geometry | full analysis | early/late parameter bases | yes | bounded | cannot prove invariance |
| `figures/figure0_parameter_semantic_decoupling.png` | central joint evidence | full analysis | two primary tables | yes | yes | visually audited |
| `figures/figure1_stage_diagnostics.png` | stage explanation | full analysis | two stage tables | yes | bounded | visually audited |
| worker `artifact_manifest.json` | hashes and full run inventory | full analysis | all worker outputs | yes | yes | remains on worker surface |

## 15. Links

- anchor: [A15_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_04_tail_band_information/15_04_tail_band_information_anchor.md)
- protocol: [protocol.md](protocol.md)
- summary: [summary.md](summary.md)
- code workspace: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_e02_deep_tail_parameter_semantic_decoupling/`
- result directory: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/a15_04_e02_deep_tail_parameter_semantic_decoupling/runs/a15-04-e02-full-20260809T162751Z/`
- reproducibility command: `python full_analysis.py --output runs/<new-full-id> --device cuda:0 --bootstrap 2000 --haar 512`
- job IDs: local run; not applicable
