---
experiment_id: A15_02_05_E01_balanced_taxonomy_attention_write_atlas
anchor_id: 15_02_05_balanced_taxonomy_attention_write_atlas
status: DRAFT_NOT_EXECUTABLE
canonical_language: en
created: 2026-08-07
---

# Protocol: Balanced Three-Level Taxonomy Attention-Write Atlas

## 0. Approval Snapshot

- **Document status:** `DRAFT_NOT_EXECUTABLE`.
- **Approval status:** researcher review required.
- **Block audit status:** A--G `PROPOSED`.
- **Cross-block consistency:** `AI_AUDIT_PASS_PENDING_RESEARCHER_CONFIRMATION`.
- **Execution scope approved:** none. This draft does not authorize implementation, smoke, or full run.
- **Purpose:** decide whether finer taxonomy granularity shows a late post-`o_proj` redistribution toward larger local DCLM covariance ranks after class-count and sample-count effects are controlled.
- **Primary anchor:** [A15_02_05 draft Anchor](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_05_balanced_taxonomy_attention_write_atlas_anchor.md).
- **Anchor decision question:** does the matched `G2-G0` local rank-centroid gap increase from early to late layers at isolated post-`o_proj` writes?
- **Anchor physical prior tested:** conditional finer distinctions may receive a later, higher-rank allocation, but this is not implied by depth alone.
- **Anchor core model term tested:** $T_{\rho,\mathrm{post}}$ under eight matched binary contrasts and equal child-center sample counts per level.
- **Anchor falsifier:** reliable finer semantic strength rises late, but normalized spectral location does not shift.
- **Experiment role:** static representation and metric audit; no training.
- **Primary metric from Anchor:** post-`o_proj` late-minus-early change in the `G2-G0` local rank centroid.
- **Claim boundary from Anchor:** one frozen model, one English taxonomy, two attention boundaries; no composition, causality, universal spectral semantics, or Router utility.
- **Minimal setup:** 512 label-free prompts, frozen Qwen3-8B, 36 pre/post attention sites, independent 65,536-token DCLM calibration.
- **Basic configuration:** eight binary root families; three nested analyzed levels; four templates; two fact bundles; early blocks 1--12; late blocks 25--35; block 36 separate; 16 equal-rank DCLM bands; 2,000 root bootstraps and 2,000 balanced-tree rerandomizations.
- **Conditions to run:** full pre-`o_proj` concat and isolated post-`o_proj`; matched-count primary and all-parent secondary; template/calibration halves; balanced taxonomy rerandomization; `o_proj` SVD energy-transfer diagnostic.
- **Pass:** all gates pass and the post primary statistic has bootstrap lower bound above zero, exceeds the registered null q95, and replicates in both template and calibration halves.
- **Fail:** all gates pass but the primary statistic fails; positive strength without shift is `strength_pass_rank_shift_fail`.
- **Insufficient:** taxonomy, balance, reliability, matching, hook, numerical, or basis-stability gate fails.
- **Cannot claim:** same eigenvector transport, composition, attention necessity, `o_proj` creation of semantics, SAE identity, Router utility, or training value.
- **Approval decision requested:** confirm, correct, or block any of A--G. Promotion and execution approval are separate later decisions.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| `G0/G1/G2` | coarse, fine, and finer binary taxonomy distinctions | sibling contrast at depth 1/2/3 inside the same balanced tree | normalized mean difference vector | defines granularity without changing prompts | relation-hop depth or composition |
| full pre-`o_proj` concat | attention result before learned output mixing | 32 head outputs concatenated to 4096 dimensions | activation | secondary boundary localization | one single head or residual state |
| isolated post-`o_proj` write | current layer's attention update in residual coordinates | `o_proj(pre)` before residual addition | activation | primary representation requested by the advisor discussion | causal use or necessity |
| reliable strength $S$ | semantic contrast reproducible across wording halves | cross-template contrast trace divided by common within-leaf expression variance | dimensionless | prevents interpreting normalized location at the noise floor | spectral location or downstream use |
| local rank centroid $\rho$ | average position of semantic contrast energy in one layer's own DCLM spectrum | 16-band normalized energy weighted by rank percentile | 0=head side, 1=tail side | operationalizes “rightward” without cross-layer vector identity | literal direction movement |
| parameter-direction activation strength | variance of activation along an `o_proj` singular vector pair | $A^{pre}_j$, $A^{post}_j=\sigma_j^2A^{pre}_j$ | activation squared | shows deterministic energy reweighting by `o_proj` | a data-spectrum semantic claim |

## 2. Anchor Alignment

- **Decision question:** exactly the Anchor question above.
- **Physical prior tested:** finer conditional semantic contrasts may become later and relatively higher-rank.
- **Core model term tested:** matched-count $T_{\rho,\mathrm{post}}$.
- **Falsifier:** strength changes without normalized location change.
- **Claim boundary:** frozen representation association only.

## 3. Tested Hypothesis

The primary post-`o_proj` `G2-G0` centroid gap increases from blocks 1--12 to blocks 25--35 after matched contrast count, matched node sample count, cross-template reliability, and independent DCLM bases are enforced.

`G1` is an ordered-coherence guard. If the endpoint passes but `G1` has a significant contradictory ordering, report `endpoint_pass_nonmonotonic`; do not call the result a monotone three-level trend.

## 4. Rival Explanations

1. **Broad late readability:** all ranks strengthen, so semantic strength rises but normalized location is fixed.
2. **Class-count/rank-capacity artifact:** `G2` has more nodes and spans more contrast directions than `G0`.
3. **Node-sample artifact:** coarse centers average more descendant prompts and are estimated more precisely.
4. **Prompt/frequency artifact:** different levels use different text distributions. The primary design eliminates this by reusing the exact same 512 states at every level.
5. **Parameter reweighting confusion:** `o_proj` singular values redistribute energy deterministically and are mistaken for a data-covariance semantic effect.
6. **Taxonomy-specific semantic distance:** one chosen tree makes coarse siblings much farther apart than fine siblings. Leave-root and balanced-tree rerandomization limit but do not remove this boundary.

## 5. Data Construction And Provenance

### 5.1 Candidate balanced tree

The proposed bank contains eight complete binary depth-three taxonomies and exactly 64 leaves:

```text
organism
├── animal
│   ├── bird: sparrow / eagle
│   └── mammal: dog / whale
└── plant
    ├── tree: oak / pine
    └── flower: rose / tulip

artifact
├── vehicle
│   ├── land vehicle: car / bicycle
│   └── aircraft: airplane / helicopter
└── musical instrument
    ├── string instrument: violin / guitar
    └── wind instrument: flute / trumpet

consumable
├── food
│   ├── fruit: apple / orange
│   └── grain: rice / wheat
└── beverage
    ├── brewed beverage: tea / coffee
    └── carbonated beverage: soda / sparkling water

place
├── natural place
│   ├── landform: mountain / valley
│   └── water body: river / lake
└── built place
    ├── learning facility: school / university
    └── medical facility: hospital / clinic

material
├── metal
│   ├── ferrous material: iron / steel
│   └── precious metal: gold / silver
└── textile
    ├── plant fiber: cotton / linen
    └── animal fiber: wool / silk

wearable item
├── garment
│   ├── upper-body garment: shirt / jacket
│   └── lower-body garment: trousers / skirt
└── clothing accessory
    ├── headwear: hat / cap
    └── footwear: shoe / boot

tool
├── force-applying tool
│   ├── striking tool: hammer / mallet
│   └── turning tool: screwdriver / wrench
└── measuring instrument
    ├── length tool: ruler / tape measure
    └── temperature tool: thermometer / pyrometer

event
├── natural event
│   ├── precipitation event: rain / snow
│   └── geologic event: earthquake / volcanic eruption
└── social event
    ├── ceremony: wedding / graduation
    └── competition: race / tournament
```

Every one of the 112 immediate edges must pass a manual “child is a kind of parent” audit. Polysemy, overlapping sibling membership, mixed instance/type levels, and culturally ambiguous membership are forbidden. A failed edge stops data preflight; it may not be silently replaced after spectral inspection.

The existing 0804 academic-domain bank was considered for reuse because it already has 64 label-free children. It is not the primary candidate: several domains contain cross-cutting methods and topics that cannot be placed under unique binary intermediate `is-a` nodes without inventing ambiguous categories. Preserving its exact text would reduce wording drift but weaken taxonomy validity, so it remains parked rather than mixed into this test.

One label-free prompt example for the `sparrow` leaf is:

```text
Read the description and form a category representation.
This small feathered creature often gathers near buildings, hops along the
ground, and feeds on seeds.
Classification:
```

The strings `sparrow`, `bird`, `animal`, and `organism` must not occur in its body. The same hidden state is assigned offline to all three labels; the model does not see those labels in the representation prompt.

### 5.2 Counts and splits

- 8 roots × 2 `G0` × 2 `G1` × 2 `G2` = 64 leaves.
- 4 templates × 2 disjoint fact bundles = 8 texts per leaf.
- Total = 512 unique texts.
- Templates 0--1 and 2--3 form disjoint reliability halves; both fact bundles occur in both halves.
- The final `Classification:` colon is the common readout. Left padding and explicit position IDs place every readout at the same registered RoPE position after the corpus is frozen.

### 5.3 Why token frequency is matched across granularity

`G0/G1/G2` are three offline groupings of the exact same 512 texts and extracted states. Therefore the marginal prompt-token distribution, sequence length distribution, template counts, and leaf frequencies are identical across granularity. This does not make all semantic distances equal and does not establish generalization beyond the chosen taxonomy.

### 5.4 Leakage and validity gates

- no canonical leaf or ancestor label in its description body;
- no template, fact-bundle, length, padding, or readout-position imbalance by any label;
- every leaf has exactly eight records;
- exact text/token hashes frozen before model extraction;
- manual `is-a` edge audit by two passes, including distractor-like sibling review;
- DCLM calibration corpus contains no exact prompt or fact-string match.

The 64-leaf candidate is now explicit. After design confirmation, implementation must create six label-free fact atoms per leaf, divided into two disjoint three-fact bundles under the frozen rules above. The resulting complete prompt manifest must pass model-independent edge, leakage, balance, tokenization, and hash checks before any activation extraction. A failed preflight yields `insufficient_data_guard`; it does not authorize result-guided leaf or wording replacement.

## 6. Learning Task And Permitted Supervision

There is no model learning. The model receives only the label-free description and shared suffix. Taxonomy labels, template IDs, fact-bundle IDs, and tree positions are analysis metadata unavailable to the forward pass.

A held-template linear readout and macro-balanced accuracy may be reported only as a capability diagnostic. It cannot choose layers, bands, templates, taxonomy leaves, or the primary site. Chance-normalized accuracy must be used when comparing 16/32/64-way diagnostic label spaces.

## 7. Model / Architecture And Frozen Variants

- Model: frozen local `/data/share/Qwen3-8B`; 36 decoder blocks; hidden width 4096.
- Primary site: direct output of each `self_attn.o_proj`, before residual addition.
- Secondary site: direct input of each `self_attn.o_proj`, the true 32-head concatenation.
- Excluded: residual states, RMSNorm outputs, MLP states, SAE features, Router states, and any learned probe as primary evidence.
- Every site/layer receives a separate DCLM activation covariance. Pre and post eigenvectors are not treated as one coordinate system.
- Every `o_proj` matrix receives a local full SVD. Singular-rank percentiles are local to the layer; parameter singular vectors are not tracked across layers.

## 8. Training Objective And Optimization

No model objective, optimizer, checkpoint selection, or parameter update exists. All analysis thresholds, early/late windows, taxonomy splits, and plot definitions must be frozen before any spectral result is inspected.

## 9. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence role | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| post-`o_proj` matched-count atlas | primary hypothesis | $T_{\rho,post}$ | decisive comparison | primary | registered rule passes | valid null/nonpositive result | any hard gate fails | Figures 1--3 |
| pre-`o_proj` matched-count atlas | boundary localization | signal already present before `o_proj` | localizes observation boundary | secondary | same typed result reported | no pre effect | hook/basis failure | Figures 1--3 |
| all-parent estimator | class-count rival | uses 8/16/32 parents | tests whether matching changes direction | guard | same primary sign | direction reverses | unstable | table |
| balanced tree rerandomization | grouping artifact | random balanced leaf-to-tree assignments | tests semantic tree specificity | primary null | observed > q95 | not above q95 | null invalid | Figure 3/table |
| template and calibration halves | wording/basis rivals | independent prompt and DCLM halves | replication | hard guard | signs agree | registered sign guard fails | weak signal | table |
| `o_proj` singular-pair energy | parameter-reweighting rival | $A^{post}=\sigma^2A^{pre}$ | separates parameter and data spectra | secondary diagnostic | numerical identity passes | identity or reconstruction fails | SVD instability | Figure 4 |

There are no stochastic model seeds. Root bootstrap, taxonomy rerandomization, and any schedule tie-breaking use seed `20260807`. Use 2,000 root-family bootstrap replicates and 2,000 balanced-tree rerandomizations. These counts and the seed are proposed frozen settings, not values to be chosen from results.

## 10. Primary Metric

For each layer and site, the primary estimator uses exactly eight binary parent contrasts at each granularity and equal child-center sample counts. Four predeclared rotations cover all non-`G0` parents. The primary statistic is

$$
T_{\rho,\mathrm{post}}
=\operatorname{median}_{25:35}(\rho_{G2}-\rho_{G0})
-\operatorname{median}_{1:12}(\rho_{G2}-\rho_{G0}).
$$

Its unit is normalized local covariance-rank percentile. Multiplying by 4096 gives an “equivalent local ranks” description only; it does not map directions across layers.

This metric decides the hypothesis because it removes total semantic scale and compares the same local rank coordinate across granularities. A false positive would promote a class-count or parameter-reweighting artifact as semantic organization; therefore matching, null, and reliability guards are hard. A false negative may occur if real semantic covariance is too weak for split reliability; that outcome is `insufficient`, not `Fail`.

The strength gate requires the 95% root-bootstrap lower bound of the early-window and late-window median $\operatorname{tr}(B^\times)$ to exceed zero for all three granularities at post-`o_proj`. The primary Pass additionally requires: (i) the 95% bootstrap lower bound of $T_{\rho,post}$ above zero; (ii) the point estimate above the 2,000-rerandomization q95; (iii) positive point estimates in both template halves and both DCLM calibration-half bases; and (iv) positive point estimates in all eight leave-one-root-family-out analyses.

Define $T_{10}$ and $T_{21}$ by replacing `G2-G0` in the primary formula with `G1-G0` and `G2-G1`. A monotone three-level label requires $T_{10}\ge0$ and $T_{21}\ge0$ in the full estimate and no negative sign in either template half. Otherwise an endpoint Pass is typed `endpoint_pass_nonmonotonic`.

## 11. Secondary Metrics

1. Cross-template reliable semantic strength $S_{\ell,s,g}$ with one common within-leaf expression-noise denominator.
2. Signed cross-template band energy for reliability and nonnegative per-half band allocation for visualization.
3. `G1` ordered coherence: whether the intermediate granularity lies between `G0` and `G2` in the registered aggregate and contradicts neither increment significantly.
4. Full-parent versus matched-parent direction agreement.
5. Chance-normalized held-template readout accuracy as capability only.
6. Background DCLM spectrum and effective rank, reported separately from semantic allocation.
7. `o_proj` singular values and paired pre/post parameter-direction activation strengths.

## 12. Known Good / Known Bad / Known Confusing Cases

- **Known good:** organism branch above; label strings absent; all three offline labels exist for the same prompt state.
- **Known bad:** a prompt body says “sparrow” or “bird”; a leaf has fewer templates; a `G2` category is an instance while its sibling is a type; post capture includes residual.
- **Known confusing:** low reliable strength but visually extreme normalized centroid; positive `G2-G0` endpoint with nonmonotone `G1`; parameter singular-rank heatmap mistaken for DCLM data spectrum; block 36 reversal hidden inside the primary late window.

## 13. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| data preflight | is the tree balanced, valid, and leak-free? | complete prompt bank and tokenizer output | all hard checks pass | data audit JSON/table | extraction smoke |
| local smoke | are both hooks exact and states nontrivial? | 16 prompts, layers 1/18/35/36 | reconstruction and replay pass | hook audit | full extraction |
| calibration smoke | do pre/post covariances and SVD identity reconstruct? | small DCLM slice | energy/reconstruction tolerances pass | numerical audit | full calibration |
| reliability gate | are all three semantic levels measurable? | full matched split contrasts | registered lower bounds positive | strength table | spectrum unseal |
| primary analysis | is the post rank interaction positive and specific? | sealed spectra and nulls | pass/fail/insufficient rules | decisive tables/figures | evidence records |

No candidate spectral plot may be used to repair the taxonomy, templates, matching schedule, or reliability threshold.

Hard numerical tolerances proposed for review are: deterministic hidden-state replay exact at stored precision; hooked post output versus direct `o_proj(pre)` relative error below $10^{-6}$; covariance projection-energy reconstruction relative error below $10^{-5}$; full `o_proj` SVD reconstruction relative error below $10^{-5}$; and Frobenius-relative error of the paired energy identity $A^{post}=\sigma^2A^{pre}$ below $10^{-5}$. Failure stops interpretation as `insufficient_numerical_guard`.

## 14. Algorithm Specification And Figure Contracts

### 14.1 Matched estimator

- **Input:** frozen 512-state tensor per layer/site plus tree and template metadata.
- **Parameters:** eight roots, binary paths, four templates, two bundles, four rotations.
- **Steps:** form equal-sample child means; form normalized sibling contrasts; select eight parents per level; compute per-half and cross-half moments; project onto the independently frozen DCLM basis; aggregate layers only after sitewise outputs are saved.
- **Outputs:** strength, band allocation, centroid, nulls, bootstrap intervals, and all guard results.
- **Failure reasons:** imbalance, low reliable strength, rank-cap mismatch, template disagreement, basis instability, or hook failure.

### 14.2 Required figures

**Figure 1 — Semantic strength across model depth.**

- Question: are `G0/G1/G2` contrasts reliably present, and does strength change with depth?
- Metric/unit: $\log S$; dimensionless; negative or nonpositive reliable estimates marked missing rather than clipped.
- Data/aggregation: matched eight-contrast estimator; root bootstrap; post solid and pre dashed; block 36 open marker.
- Allowed conclusion: stable semantic contrast magnitude relative to the same wording-noise denominator.
- Limitation: no spectral location or causal use.

**Figure 2 — Three post-`o_proj` layer-by-rank heatmaps.**

- Question: where does each granularity allocate semantic contrast within each layer's DCLM spectrum?
- Metric/unit: normalized 16-band allocation; row sums equal one within each valid layer/granularity.
- Axes: x local rank band F1--F16; y block 1--36; one shared color scale for `G0/G1/G2`.
- Allowed conclusion: within-layer relative location and qualitative redistribution.
- Limitation: rows with failed strength are masked; no cross-layer direction identity.

**Figure 3 — Decisive rank-centroid interaction.**

- Question: does `G2-G0` move relatively right from early to late, and is `G1` intermediate?
- Metric/unit: $\rho_{G0},\rho_{G1},\rho_{G2}$ and $\rho_{G2}-\rho_{G0}$; normalized rank percentile.
- Data/aggregation: matched estimator, template-half traces, calibration-half sensitivity, bootstrap interval, and balanced-tree null q95.
- Allowed conclusion: typed Pass/Fail/Insufficient for the Anchor question.
- Limitation: one taxonomy/model and no functional use.

**Figure 4 — Requested `o_proj` parameter-direction activation transfer.**

- Question: how does `o_proj` reweight activation energy along its own singular-direction pairs?
- Metric/unit: $\log_{10}A^{pre}_{\ell,j}$, $\log_{10}A^{post}_{\ell,j}$, and $\log_{10}\sigma^2_{\ell,j}$; activation squared or gain.
- Data/aggregation: independent DCLM activations; x local parameter singular-rank percentile; y layer; pre uses right singular vectors and post uses paired left singular vectors.
- Required identity audit: maximum relative error of $A^{post}-\sigma^2A^{pre}$ under the frozen tolerance.
- Allowed conclusion: deterministic parameter-direction energy reweighting by `o_proj`.
- Limitation: this is not the DCLM covariance eigenbasis, does not show cross-layer direction transport, and cannot prove semantic creation or semantic rank shift.

Every central figure must be opened and audited for labels, shared color scales, masked invalid cells, layer 35/36 visibility, and boundary text before delivery.

## 15. Success / Failure / Insufficient Evidence

- `rank_shift_pass_monotone`: all hard gates pass; post primary passes; `G1` ordering is coherent.
- `endpoint_pass_nonmonotonic`: endpoint primary passes, but `G1` contradicts a monotone three-level interpretation.
- `strength_pass_rank_shift_fail`: reliable strength gates pass, but post rank shift fails.
- `joint_fail`: all gates pass and neither reliable late relative-strength nor rank-location claim holds.
- `insufficient_<guard>`: any mandatory data, matching, reliability, hook, numerical, or basis gate fails.

Pre-`o_proj` receives a separate secondary typed result and cannot promote a failed post primary outcome.

## 16. What This Cannot Claim

The experiment cannot claim relation-hop reasoning, compositional semantics, a shared direction across layers, attention or `o_proj` causal necessity, semantic purity after template control, universal head/middle/tail meaning, correspondence to SAE dictionary atoms, Router compatibility, expert utility, or training benefit.

## 17. Block Confirmation Ledger And Review Notes

| Block | State | Decision requiring review |
| --- | --- | --- |
| A question/boundary | PROPOSED | one post-`o_proj` `G2-G0` rank-centroid interaction; `G1` as monotonicity guard |
| B data/provenance | PROPOSED | approve/correct the explicit 64-leaf/112-edge bank and deterministic label-free fact construction/audit |
| C task/supervision | PROPOSED | same label-free states grouped offline; probe diagnostic only |
| D model/architecture | PROPOSED | frozen Qwen3-8B; full pre concat and isolated post write only |
| E objective/optimization | PROPOSED | no training; all choices spectrum-sealed |
| F comparison/evidence | PROPOSED | matched eight contrasts and equal node samples; common-noise strength; centroid primary; rerandomization null |
| G execution/reproducibility | PROPOSED | local preflight then one 8×5090 node proposed; no scope approved |

**AI-detected consistency status:** the question, data skeleton, metric, sites, and claim boundary are internally aligned. Promotion is blocked only by the absence of explicit researcher confirmation for A--G. Any change to the taxonomy skeleton, primary semantic object, sites, or matching estimator reopens dependent blocks.
