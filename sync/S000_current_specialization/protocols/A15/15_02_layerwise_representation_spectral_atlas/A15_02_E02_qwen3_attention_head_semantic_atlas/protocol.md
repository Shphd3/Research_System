---
experiment_id: A15_02_E02_qwen3_attention_head_semantic_atlas
anchor_id: 15_02_layerwise_representation_spectral_atlas
status: approved_for_implementation_smoke_and_full
execution_status: completed
typed_verdict: attention_depth_pass_head_localization_pass_spectral_fail
approved_by: user
approval_date: 2026-08-04
canonical_language: en
---

# Protocol: Per-Attention-Head Coarse/Fine Semantic Variance Atlas In Qwen3-8B

## 0. Approval Snapshot

**Document status:** `APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL`  
**Execution status:** `COMPLETED`; the 2026-08-05 axis-order correction is incorporated in [summary.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_E02_qwen3_attention_head_semantic_atlas/summary.md) and [detailed.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_E02_qwen3_attention_head_semantic_atlas/detailed.md).  
**Approval status:** the user explicitly authorized the same experiment at single-attention-head resolution on one `5090-8-spot` node without another approval stop.  
**Block audit status:** A--G `CONFIRMED`.  
**Cross-block consistency:** `PASS`.  
**Execution scope approved:** implementation, smoke, full frozen-model extraction, analysis, result records, anchor update, and `daily_research_reports/backup/2026/08/0805/focus.md`; no commit, push, graph edit, or external sync.
**Purpose:** decide whether the late fine-semantic discriminability found in whole residual states is already present in the multi-head attention branch and is localized to reproducible individual heads or distributed across heads.  
**Primary anchor:** [A15_02](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/15_02_layerwise_representation_spectral_atlas_anchor.md).  
**Experiment role:** frozen static mechanism-localization audit.  
**Primary metric:** the early-to-late change in pooled-attention fine/coarse discriminability, plus a family-wise permutation test for any individual late head.  
**Minimal setup:** frozen Qwen3-8B; the exact registered 8-parent × 8-child × 8-description dataset; the exact independent 128-document DCLM calibration corpus; all 36 layers and all 32 query heads.  
**Pass:** the pooled attention branch has a positive registered depth contrast, and at least one individual late head survives the global late-head permutation maximum and robustness guards.  
**Fail:** all validity gates pass but the pooled depth effect or individual-head localization clause fails; clauses are reported separately.  
**Insufficient:** hook/replay, semantic capability, calibration identity, covariance reconstruction, head-basis stability, numerical, or sealed-template guards fail.  
**Cannot claim:** causal semantic computation, universal head identity, attention necessity, Router utility, or training benefit.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Single-head output | What one query head writes before heads are mixed | Input slice of `self_attn.o_proj`, reshaped as 32 × 128 | activation | Preserves the architectural head boundary | A head is independently causal |
| Coarse variance | Separation among eight parent-domain centers | Trace of between-parent covariance $B^c$ | activation² | Measures broad semantic separation | Readability after within-class noise |
| Fine variance | Separation among eight children inside each parent | Mean trace of conditional between-child covariance $B^f$ | activation² | Measures within-domain semantic separation | A fixed spectral coordinate |
| Discriminability | Between-class signal relative to same-class wording variation | $D^g=\operatorname{tr}(B^g)/(\operatorname{tr}(W^g)+\epsilon)$ | dimensionless | Separates larger semantic variance from smaller nuisance spread | Causal use by the model |
| Head contrast | Fine relative to coarse discriminability in one head | $R_{\ell h}=\log(D^f_{\ell h}/D^c_{\ell h})$ | log ratio | Builds the layer × head atlas | Cross-layer identity of head index $h$ |
| Pooled attention contrast | The same comparison after summing signal/noise traces across all 32 heads | $R^{attn}_\ell=\log[(\sum_h B^f/\sum_h W^f)/(\sum_h B^c/\sum_h W^c)]$ | log ratio | Tests whether attention output as a branch carries the residual-state depth effect | MLP contribution or residual causality |
| Within-head spectral band | Eight covariance-ranked directions inside one 128-d head | F1=head, F2--F8=middle, F9--F16=tail | 8 directions per band | Tests spectral localization without mixing heads | Universal semantic meaning of rank |
| Global late-head null | Best apparent head under permuted fine labels | q95 of max $R_{\ell h}$ over layers 25--35 and 32 heads | log ratio | Controls selection among 352 late head cells | External replication |

## 2. Anchor Alignment

**Decision question.** Is the late fine/coarse discriminability gain localized inside the attention branch, and if so is it carried by reproducible individual heads or only by a distributed sum?  
**Physical prior tested.** Attention heads are distinct information-writing channels, so whole-state fine-semantic tightening may be traceable to a small subset; the strongest rival is that the effect appears only after cross-head output projection, residual accumulation, or MLP updates.  
**Falsifier.** A valid pooled attention branch has no positive late-minus-early contrast, or no individual head exceeds the selection-corrected permutation null.  
**Claim boundary.** This is one frozen model, one balanced English taxonomy, and one attention-output site.

## 3. Tested Hypotheses

**H1, attention-branch depth effect.** The registered pooled contrast

$$
T_{attn}=\operatorname{median}_{\ell=25:35}R^{attn}_\ell-
\operatorname{median}_{\ell=1:12}R^{attn}_\ell
$$

has a paired nested-bootstrap 95% lower bound above zero, with block 36 reported separately.

**H2, individual-head localization.** At least one layer-head cell in blocks 25--35 has positive confirmation-set $R_{\ell h}$ above the global late-head label-permutation q95, the paired-bootstrap lower bound is above zero, design and confirmation signs agree, and at least seven of eight leave-one-parent-out contrasts are positive.

**H3, within-head spectral specificity.** For every H2-qualified head, coarse/fine $B/W$ is inspected in 16 equal-rank bands. A band-specific claim requires a positive paired-bootstrap lower bound and a value above the q95 of 256 equal-dimensional random orientations inside the same head. If H2 has no qualified head, the top confirmation head in each registered late layer is shown descriptively but cannot pass H3.

## 4. Rival Explanations

1. The whole-state result is written by MLP or residual accumulation, not attention output.
2. Fine/coarse differences are spread weakly across many heads and no single head is special.
3. A selected head is a multiple-comparison artifact among 352 late cells.
4. Template, parent, length, residual scale, or lexical leakage produces the contrast.
5. A claimed spectral band is an unstable covariance estimate or an arbitrary 8-d orientation.
6. Head index has no cross-layer identity; layer 20 head 7 is not assumed to be the same function as layer 30 head 7.

## 5. Data Construction And Provenance

Reuse without modification:

- semantic data: 8 parents × 8 children × 4 templates × 2 disjoint fact bundles = 512 label-free descriptions;
- design split: templates T1/T2; sealed confirmation split: T3/T4;
- readout: the common final `Classification:` colon token at one absolute RoPE position;
- calibration: 128 independent DCLM documents × 512 tokens = 65,536 tokens;
- dataset, token, model, and calibration hashes from A15_02_E01.

No sentence, label, split, token position, taxonomy member, or calibration document may be changed after seeing head results.

## 6. Diagnostic Task And Permitted Supervision

Qwen is not trained. The same hidden attention-head output supports two matched eight-way variables: parent identity and child identity conditional on parent. Labels are used only after frozen extraction to form between/within covariance, capability probes, bootstrap samples, and permutation nulls. Sealed templates cannot tune a probe, choose a layer/head, choose an eigenvalue floor, or alter the dataset.

## 7. Model / Architecture And Frozen Variants

- model: `/data/share/Qwen3-8B`;
- 36 decoder blocks, hidden size 4096, 32 query heads, 8 KV heads, head dimension 128;
- frozen bfloat16 forward, SDPA attention, no cache;
- capture the tensor entering each block's `self_attn.o_proj`, reshape its last dimension to `[32, 128]`;
- do not interpret Q/K/V projections, attention weights, block residual outputs, or MLP outputs as the primary single-head object;
- compare to the already completed residual-state trajectory only as a registered external reference.

## 8. Objective And Optimization

There is no model optimization. Statistics are accumulated from frozen activations. Calibration batch Gram matrices may be formed in FP32 on GPU and accumulated in FP64 on CPU; smoke must compare this path with direct FP64 covariance on a subset and require relative spectral/trace error below $10^{-4}$.

## 9. Conditions, Controls, And Evidence

| Item | Clause / rival | Why needed | Evidence | Pass / fail / insufficient | Figure / table |
| --- | --- | --- | --- | --- | --- |
| All layers × all heads | H1/H2 | Prevent layer/head cherry-picking | Primary | Full 36 × 32 atlas | Figure 1 |
| Pooled attention output | H1 / MLP rival | Localize the branch before selecting heads | Primary | $T_{attn}$ interval | Figure 1, Table 1 |
| Global max label permutation | H2 / selection rival | Correct 352-cell head search | Primary | candidate exceeds q95 | Table 2 |
| Design vs confirmation | Template rival | Require out-of-template direction | Guard | same sign | Table 2 |
| Leave-one-parent-out | Parent outlier rival | Reject one-domain heads | Guard | ≥7/8 positive | Table 2 |
| Per-head 16-band basis | H3 | Reproduce the same spectral audit within heads | Secondary | basis and energy guards | Figure 2 |
| Random 8-d orientations | H3 / arbitrary orientation | Test covariance-rank specificity | Primary for H3 | true band exceeds q95 | Table 3 |
| Existing residual trajectory | branch comparison | Show what attention explains and does not | Secondary | descriptive, no tuning | Figure 3 |

## 10. Primary Metrics And Decision Rules

### 10.1 Attention-branch depth clause

Point estimate: $T_{attn}$ above. The paired nested bootstrap resamples parent, child within parent, and templates within child. 2,000 draws use the pre-registered seed `2026080501`. Pass requires the 95% lower bound $>0$, all four template-family late-minus-early contrasts positive, and all eight leave-one-parent-out contrasts positive.

### 10.2 Individual-head localization clause

Compute $R_{\ell h}$ on sealed confirmation data. Generate 5,000 child-label permutations within each parent, recompute all late cells, and retain the maximum per draw. A head is qualified only if it exceeds the global q95 and passes the bootstrap, split, and leave-parent guards in H2. No practical effect-size threshold is imposed.

### 10.3 Spectral clause

For each qualified head, fit its 128-d covariance basis from calibration only and split into 16 × 8-d bands. Report actual between-class variance per direction $b$, background-whitened variance $q$, and semantic discriminability $j=B/W$. H3 is pass only for bands exceeding both paired uncertainty and same-head random-orientation q95. Head, middle, and tail aggregates always average per direction.

### 10.4 Typed verdicts

- `attention_depth_pass_head_localization_pass`: H1 and H2 pass;
- `attention_depth_pass_head_localization_fail`: H1 passes and H2 fails;
- `attention_depth_fail`: validity gates pass and H1 fails;
- append `_spectral_pass` or `_spectral_fail` when H2 passes and H3 is adjudicable;
- `insufficient_<guard>` when any mandatory guard fails.

## 11. Secondary Metrics

- number and fraction of positive $R_{\ell h}$ cells per layer;
- median, upper quartile, and maximum $R_{\ell h}$;
- leave-one-head-out change in pooled $R^{attn}_\ell$;
- top-1/top-4/top-8 positive influence share, descriptive only;
- raw $B$, within-class $W$, $D$, and 16-band $b/q/j/e$;
- attention pooled trajectory versus the existing residual-state trajectory;
- block 36 separately.

## 12. Mandatory Validity Gates

1. Config and weight hashes match A15_02_E01.
2. All 36 `o_proj` pre-input hooks have shape `[batch, seq, 4096]` and reshape exactly to `[batch, seq, 32, 128]`.
3. Two identical forwards reproduce head tensors exactly.
4. Summing 32 separately projected head slices reconstructs native `o_proj` output within relative error $10^{-5}$.
5. All 512 semantic records and 65,536 calibration tokens match prior hashes.
6. Pooled attention representation exceeds the hierarchical permutation q95 for both variables at the registered late sites before semantic interpretation.
7. Covariance symmetry, nonnegative spectrum within tolerance, energy conservation, and split-half basis guards pass.
8. Spectral conclusions are blocked for any head whose relevant band basis is unstable.
9. FP32-batch/FP64-accumulation agrees with subset direct-FP64 within $10^{-4}$.
10. Block 36 and every head are reported; no head/layer may be removed because of its result.

## 13. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass rule | Handoff |
| --- | --- | --- | --- | --- |
| S0 provenance | Are model/data/calibration identical? | hashes and config | exact match | S1 |
| S1 smoke | Is the single-head hook valid? | shapes, replay, projection reconstruction | all guards pass | S2 |
| S2 distributed extraction | Are all records/tokens captured once? | rank manifests | exact global coverage | S3 |
| S3 covariance/basis | Are 1,152 head bases numerically usable? | moments, spectra, half splits | mandatory gates pass | S4 |
| S4 semantic analysis | Does H1/H2/H3 hold? | bootstrap/permutation/random controls | typed verdict | S5 |
| S5 visualization audit | Do plots encode the registered quantities? | opened PNGs and source tables | visual + numeric audit | result records |

## 14. Execution And Reproducibility

- resource profile: `5090-8-spot`;
- execution surface: ACP;
- workspace / cluster / spec: `share-space` / `computing-cluster-5090-01g` / `n12lp.nn.i10a.8`;
- one worker node, eight GPUs/processes, spot quota, normal priority;
- each process receives a disjoint document and semantic-record shard while loading the same frozen model;
- smoke runs before full in the same fail-closed job;
- worker code and raw outputs remain under `XingyuD/MoE_Routing_Experiments/active/a15_01_05_e02_qwen3_attention_head_semantic_variance_atlas/`;
- Research mainline receives only protocol, summary, detailed ledger, compact tables, decisive figures, and small provenance manifests.

## 15. Required Figures

1. **Layer × head discriminability atlas:** heatmap of $R_{\ell h}$, with pooled attention and prior residual trajectories beside it.
2. **Selected-head 16-band atlas:** coarse/fine actual variance and fine-minus-coarse $j$ across F1--F16 for qualified heads or descriptive top heads.
3. **Localization and stability:** head effects with global permutation q95, design/confirmation, and leave-parent evidence.
4. **Within-head covariance spectra:** eigenvalue decay and split-half stability for representative qualified/descriptive heads.

Every figure must be opened and audited. Color bars must define sign and unit. The central figure cannot imply cross-layer identity of a numerical head index.

## 16. What This Cannot Claim

The experiment cannot establish that a head computes a semantic concept, that attention is necessary, that the same head number has the same role across layers or models, that a covariance band causes meaning, or that any head/band should route experts or improve NLL/FLOP.

## 17. Confirmation Ledger

| Block | Status | Frozen decision |
| --- | --- | --- |
| A Question / boundary | CONFIRMED | attention-branch depth and individual-head localization |
| B Data / provenance | CONFIRMED | exact E01 semantic and calibration data |
| C Diagnostic task | CONFIRMED | matched coarse and conditional-fine variables |
| D Model / representation | CONFIRMED | pre-`o_proj` 32 × 128 attention-head outputs |
| E Objective / optimization | CONFIRMED | frozen Qwen; statistics only |
| F Comparison / evidence | CONFIRMED | pooled depth, global head null, per-head 16 bands |
| G Execution | CONFIRMED | smoke + full on one 8×5090 spot node |

The user message on 2026-08-04 explicitly approved execution without a further approval stop. Cross-block consistency passed: the data and readout are unchanged; the hook matches the architectural head object; pooled and per-head metrics separate branch localization from head selection; controls protect multiplicity, basis stability, and template/parent rivals; and the requested resource profile is explicit.
