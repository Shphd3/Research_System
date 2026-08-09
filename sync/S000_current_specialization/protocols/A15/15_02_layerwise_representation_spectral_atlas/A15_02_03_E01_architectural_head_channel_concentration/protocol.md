---
experiment_id: A15_02_03_E01_architectural_head_channel_concentration
anchor_id: 15_02_03_architectural_head_channel_concentration
status: COMPLETED
execution_status: completed_with_analysis_only_repair
canonical_language: en
updated: 2026-08-05
---

# Approved Protocol: Qwen3-8B MLP-Input Channel Groups versus True Attention Heads

Chinese review companion: [protocol_cn.md](protocol_cn.md).

## 0. Approval Snapshot

**Document status:** `COMPLETED`; the frozen extraction is canonical and the final analysis includes a plotting-only repair.  
**Approval status:** all blocks are confirmed, including exact reuse of the A15_02_E01 semantic/calibration data, site-specific random-partition nulls, eight bands, and two independent 8×5090 jobs.  
**Block audit status:** A--G `CONFIRMED`.  
**Cross-block consistency:** `PASS`.  
**Execution scope approved:** implementation, smoke, two full frozen audits, analysis, result records, and the 0805 focus; no graph, commit, push, or external sync.  
**Execution outcome:** both site extractions and all statistics completed; the remote processes exited during plotting, and the corrected plots/verdicts were regenerated from unchanged cached tensors.  
**Purpose:** decide whether coarse/fine semantic variance or discriminability is more concentrated in true pre-`o_proj` attention heads than in fixed 128-dimensional channel groups of the post-attention MLP input, after calibrating each site against arbitrary equal-size partitions.  
**Primary anchor:** [A15_02_03](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_03_architectural_head_channel_concentration_anchor.md).  
**Anchor decision question:** do true attention heads or fixed MLP-input groups beat their full 4096-dimensional site state and equally shaped random channel partitions, and which site is more concentrated after null calibration?  
**Physical prior tested:** semantic signal and within-class nuisance can be unevenly distributed across native MLP-input channels.  
**Core model term tested:** random-partition-calibrated group advantage $C_{\ell h}^g$.  
**Anchor falsifier:** fixed grouping is indistinguishable from random repartitioning on untouched evidence.  
**Experiment role:** frozen static representation-concentration and metric audit.  
**Primary metric:** typical and global-maximum $C_{\ell h}^g=\log(D_{\ell h}^g/D_{\ell,\mathrm{full}}^g)$ for coarse and fine semantics, calibrated by random 32×128 partitions.  
**Claim boundary:** channel concentration only; no attention-head identity, causal computation, Router utility, or training benefit.  
**Minimal setup:** frozen `/data/share/Qwen3-8B`; all 36 pre-`o_proj` states and exact MLP inputs; 32 true heads or 32 fixed contiguous groups; the exact A15_02_E01 512-text semantic dataset with sealed template halves; the exact independent 65,536-token DCLM covariance data.  
**Conditions:** full state, fixed channel groups, random channel repartitions, group-internal eight-band covariance, and equal-dimensional random orientations.  
**Pass:** at least one site exceeds its matching random-partition null on untouched data for a registered granularity; typical and sparse-best clauses are typed separately.  
**Fail:** all guards pass but neither site's fixed units exceed random partitioning.  
**Insufficient:** hook, data, capability, confirmation, reconstruction, random-null, basis, or numerical guards fail.  
**Cannot claim:** that a channel group is an attention head or functional module, that covariance rank causes semantics, or that a group should route experts.  
**Approval decision:** approved by the researcher on 2026-08-05.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| MLP input | Representation directly consumed by a block MLP | post-attention RMSNorm output $m_\ell$ | activation, 4096 dims | Exact requested audit site | Attention-head identity |
| True attention-head output | Per-head result immediately before output projection | `self_attn.o_proj` input reshaped 32×128 | activation, 128 dims/head | Architectural reference site | Direct MLP input |
| Fixed channel group | One contiguous native slice of the MLP input | `G1=[0:128)`, ..., `G32=[3968:4096)` | 128 dims | Tests native-coordinate concentration | Architectural modularity |
| Raw semantic variance | Actual spread of class centers | $\operatorname{tr}(B^g)/d$ | activation²/direction | Measures real semantic energy | Class separability after nuisance |
| Energy share | Fraction of full between-class energy in a group | $s_{\ell h}^g=\operatorname{tr}(B_{\ell h}^g)/\operatorname{tr}(B_\ell^g)$ | fraction | Shows concentration; sums to one | Utility or causality |
| Discriminability | Class-center separation relative to same-class wording variation | $D^g=\operatorname{tr}(B^g)/(\operatorname{tr}(W^g)+\epsilon)$ | dimensionless | Direct coarse/fine separation metric | Probe-free causal use |
| Group advantage | Group discriminability relative to the full state | $C_{\ell h}^g=\log(D_{\ell h}^g/D_{\ell,full}^g)$ | log ratio | Compares part with whole | Specificity without random partitions |
| Typical group | Robust center of the 32 group advantages | median across groups; mean also reported | log ratio | Distinguishes broad from sparse effects | Every group is useful |
| Best group | Largest group advantage after searching groups/layers | global maximum with matched null | log ratio | Tests existence of sparse concentration | Typicality; replication |
| Random channel partition | Same 4096 channels randomly permuted then split 32×128 | 1,024 proposed partitions | null distribution | Separates fixed coordinates from arbitrary grouping | Rotation-invariant modularity |
| Eight-band group spectrum | A group's covariance-ranked directions | F1; F2--F5; F6--F8, each 16 dims | relative rank | Localizes signal within a group | Same directions across groups/layers |

## 2. Anchor Alignment

**Decision question.** Are fixed native MLP-input channel groups unusually concentrated semantic coordinates relative to the whole and random partitions?  
**Physical prior.** Between-class signal and within-class nuisance can be unevenly allocated over native channels.  
**Core model term.** $C_{\ell h}^g$ and its fixed-versus-random typical/maximum summaries.  
**Falsifier.** Fixed grouping does not exceed the same statistic under random repartitions on untouched evidence.  
**Claim boundary.** Frozen single-model static concentration only.

## 3. Tested Hypotheses

### H1: true-head concentration

True heads have typical and/or global-maximum $C^c/C^f$ exceeding the random 32×128 partition q95 on untouched confirmation data.

### H2: fixed MLP-group concentration

Fixed contiguous MLP-input groups have typical and/or global-maximum $C^c/C^f$ exceeding their random-partition q95.

### H3: site difference after null calibration

True heads show stronger coarse, fine, or fine-relative concentration than MLP groups after each site is calibrated by its own random-partition distribution.

### H4: within-unit spectral specificity

For a concentration-qualified unit, at least one of eight true covariance bands has a stable coarse/fine $b/q/j$ contrast beyond same-unit random 16-dimensional orientations.

H1--H4 are reported separately. Passing only a maximum clause establishes sparse concentration, not a typical-group advantage.

## 4. Rival Explanations

1. **Weighted-average inevitability:** at least one group must have $D\ge D_{full}$ because $D_{full}$ is a within-variance-weighted average.
2. **Maximum-selection artifact:** searching 1,152 layer-group cells produces a large best value under any partition.
3. **Arbitrary native order:** fixed contiguous groups are no more special than random channel partitions.
4. **Low-denominator artifact:** high $D$ or $R$ comes from tiny within-class or coarse variance rather than strong fine signal.
5. **Prompt/taxonomy reuse:** the same known taxonomy reproduces previously observed coordinates without external semantic replication.
6. **Unstable spectrum:** near-degenerate 128-dimensional covariance directions rotate across calibration halves.

## 5. Data Construction And Provenance

### 5.1 Discovery data, frozen and already exposed

Reuse exactly the reviewed 8 parent domains × 8 children × 4 templates × 2 disjoint fact bundles = 512 label-free descriptions from A15_02_E01. Keep the final `Classification:` colon readout, left-padding/position-id contract, labels, token ids, template identifiers, fact bundles, and hashes unchanged.

Because these data have already exposed residual and attention-head patterns, they may develop code, verify signs, and rank candidate groups but cannot alone support a new selected-best-group claim.

### 5.2 Sealed-template confirmation on the reused taxonomy — CONFIRMED AMENDMENT

Per the researcher's 2026-08-05 execution amendment, reuse the exact A15_02_E01 512 texts, token ids, readout position, labels, and hashes. Templates 1--2 are design and templates 3--4 are confirmation. Unit definitions, eight bands, random-partition draws, and metrics were frozen before either new representation site was opened. Design may nominate descriptive units; every verdict uses confirmation and the global random-maximum correction.

This confirmation adjudicates the matched question on the same natural-semantic task. It does not establish cross-taxonomy generality; that limitation is a claim boundary rather than an execution failure.

### 5.3 Independent covariance data

Reuse the audited 128 independent DCLM documents × 512 tokens = 65,536 tokens and token hash `5c2e9f6b7d307436eda018b7719bc38cddab6387881d77f89bc74fb717b2f792`. Verify no confirmation sentence is duplicated verbatim. Split the calibration documents into two frozen halves for basis stability.

The statistical units are parents, children within parent, and templates/fact bundles within child, not the 512 sentences.

## 6. Diagnostic Task And Permitted Supervision

The same frozen MLP-input state supports two matched eight-way variables:

1. coarse parent identity;
2. child identity conditional on parent, averaged across parents.

Labels are used only after extraction to estimate $B$, $W$, capability probes, bootstrap draws, label permutations, and plot annotations. Qwen receives no gradients. Design data may choose implementation tolerances and descriptive candidates; confirmation labels cannot choose groups, layers, partitions, eigenvalue floors, or thresholds.

## 7. Model / Architecture And Frozen Variants

- model: `/data/share/Qwen3-8B`;
- architecture: Qwen3ForCausalLM, 36 blocks, hidden size 4096, 32 attention heads, head dimension 128;
- forward: frozen bfloat16, SDPA, no cache; analysis moments in FP64;
- MLP branch hook: `layer.mlp.register_forward_pre_hook`, reading its positional input tensor;
- attention branch hook: `layer.self_attn.o_proj.register_forward_pre_hook`, reshaping its 4096-dimensional input as 32 true query-head outputs × 128 dimensions;
- sites: block 1 through block 36; there is no embedding-site MLP input;
- readout: exact final `Classification:` colon token used by A15_02_E01;
- fixed MLP split: native channels `[128h:128(h+1))`, named `G1--G32`;
- attention split: architectural pre-`o_proj` query-head boundaries, named `H1--H32`;
- forbidden interpretation: no MLP group is called an attention head, and no pre-`o_proj` head output is called the MLP input.

Smoke must show exact post-attention-layernorm/MLP-pre-hook equality; exact head concatenation; and reconstruction of the `o_proj` output by summing each head's sliced linear contribution.

## 8. Training Objective And Optimization

There is no model training, optimizer, model selection, or checkpoint selection. Ridge probes are capability gates only. Random partitions, orientation seeds, numerical floors, and plot scales are frozen before confirmation analysis.

## 9. Conditions, Controls, And Evidence

| Item | Anchor clause tested | Model term / rival | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Site-specific full 4096 state | H1--H3 | part-vs-whole baseline | Defines each site's $D_{full}$ | Primary baseline | valid capability | no capability is not scientific Fail | probe/permutation failure | Figs 2, 4 |
| True H1--H32 | H1/H3 | architectural concentration | Attention reference | Primary | exceeds matched null | does not exceed | reconstruction failure | Figs 1, 2 |
| Fixed G1--G32 | H2/H3 | mixed native-coordinate concentration | MLP treatment | Primary | exceeds matched null | does not exceed | reconstruction failure | Figs 1, 2 |
| 1,024 random channel partitions | all / arbitrary grouping | fixed grouping may be arbitrary | Main falsifier | Primary | fixed statistic > q95 | fixed within null | null incomplete | Figs 2, 5 |
| Mean/median/max summaries | H1--H3 | broad vs sparse effect | Prevent max-only overclaim | Primary typed clauses | corresponding clause passes | clause fails | bootstrap failure | Fig 4 |
| Design/confirmation templates | wording-selection rival | reused taxonomy | Protect selected maxima | Mandatory guard | replication | non-replication | split failure | Tables 1--2 |
| Eight true bands per unit | H4 | local spectral identity | Requested spectral atlas | Secondary clause | true band > random q95 | no band passes | unstable basis | Fig 3 |
| 256 random 16-d orientations | H4 / direction rival | arbitrary band | Spectral falsifier | Primary for H4 | true exceeds q95 | true within null | null incomplete | Figs 3, 5 |
| Three eigenvalue floors | H4 / tail noise | tiny eigenvalues | Numerical guard | Guard | direction stable | sensitivity | floor failure | Table 3 |

## 10. Primary Metric

For $g\in\{c,f\}$ compute all $C_{\ell h}^g$. The fixed-partition summaries are:

$$
T_g^{fixed}=\operatorname{median}_{\ell=1:35,h}C_{\ell h}^g,
\qquad
K_g^{fixed}=\max_{\ell=1:35,h}C_{\ell h}^g.
$$

Block 36 is reported separately. Every random partition $r$ yields the same $T_g^{(r)}$ and $K_g^{(r)}$. Typical or sparse concentration passes only if the fixed statistic exceeds the corresponding random-partition q95 and its parent→child→template bootstrap lower bound for the fixed-minus-random-q95 contrast is above zero on confirmation data.

Also compute $T_{rel}$ and $K_{rel}$ from $C^{rel}$. A candidate cell cannot pass if its $D^f$, $D^c$, $\operatorname{tr}(W^f)$, or $\operatorname{tr}(W^c)$ lies below the pre-registered label-permutation/numerical floor. The arithmetic mean over groups is always reported but is not allowed to replace the median or maximum verdict.

This metric decides whether native fixed grouping exhibits more concentration than partitioning itself. It does not decide whether concentrated information is used by the model.

## 11. Required Raw-Variance And Secondary Metrics

Required for every layer, group, and granularity:

- $\operatorname{tr}(B)$ and per-direction $v$ in activation² and activation²/direction;
- energy share $s$ and log enrichment $\log(32s)$ relative to uniform allocation;
- within-class trace $\operatorname{tr}(W)$;
- $D^c$, $D^f$, $R$, $C^c$, $C^f$, and $C^{rel}$;
- group-energy Gini/HHI, descriptive and random-partition calibrated;
- full-state counterparts;
- within-group F1--F8 $b$, $q$, $j$, and fine-minus-coarse contrasts;
- full-state eight relative-rank bands of 512 dimensions as a descriptive profile only; group and full bands share relative rank, not directions;
- early blocks 1--12, late blocks 25--35, and block 36 summaries, secondary to the all-layer primary statistic.

### 11.1 Required heatmap and trajectory contracts

**Figure 0, covariance-spectrum audit.** Show the full 4096-dimensional MLP-input eigenvalue curves and representative 128-dimensional group curves on normalized rank, with F1--F8 boundaries. A companion layer-by-normalized-rank heatmap uses log background variance. This figure validates the spectrum and band geometry; it does not show semantic discriminability.

**Figure 1, raw semantic-variance allocation heatmap.** Rows are blocks 1--36 and columns are G1--G32. Panels show coarse/fine $v$ and coarse/fine $\log(32s)$. The $v$ colorbar is activation²/direction; positive $\log(32s)$ means more than the uniform 1/32 energy share. This figure decides where actual semantic energy is concentrated, not whether classes are discriminable.

**Figure 2, decisive group-versus-full discriminability heatmap.** Rows are blocks and columns are groups. Three primary panels show $C^c$, $C^f$, and $C^{rel}$. Positive color means the group exceeds the full representation. A marker is allowed only when the cell survives confirmation uncertainty and the global random-partition maximum. This figure directly decides coarse, fine, and fine-relative concentration.

**Figure 3, layer-by-eight-band heatmap.** Rows are blocks and columns are F1--F8. Show the typical group and the discovery-fixed best group separately, with coarse/fine $b$, coarse/fine $j$, and fine-minus-coarse $j$. The $b$ unit is activation²/direction; $j$ is dimensionless. Mark only bands that also exceed the same-group random 16-d orientation q95.

**Figure 4, full/mean/median/max depth trajectories.** The x-axis is block and the y-axis shows $D^c$, $D^f$, $R$, or the corresponding group advantage. Lines are full state, arithmetic group mean, group median, and selection-corrected group maximum. Block 36 is visually separate. This figure distinguishes broad concentration from a sparse peak.

**Figure 5, fixed-versus-random partition calibration.** For every layer, show the fixed median/maximum against the envelope from 1,024 random partitions and indicate cells or layer summaries that pass. This figure decides whether native contiguous grouping is more special than arbitrary equal-size slicing.

All figures must be regenerated from source CSVs, opened, and audited for axis meaning, units, colorbars, dynamic range, block-36 visibility, and marker semantics.

## 12. Known Good / Known Bad / Known Confusing Cases

- **Known good:** concatenating G1--G32 exactly reconstructs $m_\ell$; raw $B/W$ traces sum to direct full-state traces.
- **Known bad:** reshaping $m_\ell$ and calling slices attention heads.
- **Known bad:** claiming max group $D>D_{full}$ without a random-partition maximum null.
- **Known confusing:** high $R$ caused by near-zero coarse $D$; always inspect both absolute $D$ values and denominator floors.
- **Known confusing:** a group can hold less raw semantic energy but have higher discriminability by excluding within-class nuisance.
- **Known confusing:** a stable relative-rank F1 across groups does not imply a common direction or function.

## 13. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| S0 provenance | Are model/data/calibration/confirmation frozen? | manifests and hashes | exact match or stop | provenance audit | S1 |
| S1 hook smoke | Is $m_\ell$ the exact MLP input? | hook equality, shapes, replay | all 36 pass or stop | tensor audit | S2 |
| S2 semantic extraction | Are all examples captured once? | rank manifests | exact coverage | extraction manifest | S3 |
| S3 raw/group audit | Do group traces reconstruct full statistics? | $B/W$, energy identities | tolerance pass or stop | reconstruction table | S4 |
| S4 random-partition inference | Are fixed groups special? | $C$, bootstrap, 1,024 nulls | typed H1--H3 verdict | null tables | S5 |
| S5 covariance bands | Where is qualified signal located? | group bases and 256 orientations | typed H4 verdict | stability tables | S6 |
| S6 visualization | Do heatmaps show registered quantities honestly? | source CSVs and PNGs | open and audit all | visual checklist | records |

## 14. Algorithm Specification

**Input:** frozen model; semantic manifests; calibration manifest; hook sites; fixed channel selectors; frozen random seeds.  
**Parameters:** 32 groups, 128 dims/group, 8 bands, 16 dims/band, 2,000 nested bootstraps, 5,000 hierarchical label permutations, 1,024 random channel partitions, 256 within-group random orientations, eigenvalue floors $10^{-6},10^{-5},10^{-4}\lambda_1$.  
**Steps:** extract $m_\ell$ once; compute full and group $B/W$; validate trace identities; compute fixed and random $C$ families; fit group covariances from calibration only; compute F1--F8 $b/q/j$; run confirmation inference; render and open figures.  
**Outputs:** compact CSVs, manifests, Figure 0--5, `summary.md`, and `detailed.md`; raw activations and bases remain on the worker surface.  
**Stop conditions:** any mandatory data/hook/capability/reconstruction/confirmation/random-null/basis guard failure.  
**Forbidden repair:** removing adverse groups/layers/taxonomy members, lowering null strength after results, or renaming channel groups as heads.

## 15. Success / Failure / Insufficient Evidence

Typed verdicts are clause-specific:

- `typical_group_concentration_pass_<coarse|fine|both>`: $T_g$ passes fixed-vs-random confirmation;
- `sparse_group_concentration_pass_<coarse|fine|both>`: $K_g$ passes but typical does not;
- append `_fine_relative_pass` if $C^{rel}$ passes;
- append `_spectral_pass` only if H4 passes for a concentration-qualified group;
- `channel_group_concentration_fail` if all guards pass and no fixed-group statistic exceeds its null;
- `insufficient_<guard>` for any mandatory guard failure.

Passing raw-energy concentration without discriminability concentration is reported as an energy-allocation result, not as semantic separation. Passing discriminability without fixed-versus-random specificity is descriptive heterogeneity only.

## 16. What This Cannot Claim

The experiment cannot establish that a fixed channel group is an attention head, neuron module, semantic circuit, or Router coordinate; that group removal would causally impair semantics; that the grouping transfers across models; that covariance rank creates coarse/fine meaning; or that any group/band improves expert utility, NLL, or training efficiency.

## 17. Block Confirmation Ledger And Review Notes

| Block | Status | Frozen or proposed decision |
| --- | --- | --- |
| A Question / boundary | CONFIRMED | matched comparison of true attention heads and exact MLP-input groups |
| B Data / provenance | CONFIRMED | exact A15_02_E01 reuse with sealed template confirmation; external taxonomy is outside the primary verdict |
| C Diagnostic task | CONFIRMED | matched coarse and conditional-fine variables; raw variance and discriminability |
| D Model / representation | CONFIRMED | all 36 pre-`o_proj` head states and MLP pre-inputs; 32×128 units; eight 16-d bands/unit |
| E Objective / optimization | CONFIRMED | frozen Qwen; no model training |
| F Comparison / evidence | CONFIRMED | both sites: full vs fixed vs random partitions; typical/mean/max; Figures 0--5 |
| G Execution | CONFIRMED | two independent ACP single-node jobs, each `5090-8-spot`, 8 GPUs, spot; one job per site |

**Cross-block audit:** PASS. The two branches share data, labels, calibration, unit shape, metrics, nulls, and thresholds; only the representation site changes.

**Approval note:** the researcher authorized implementation, smoke, two full runs, analysis, experiment records, and `daily_research_reports/0805/focus.md` on 2026-08-05. Graph edits, commit, push, and external sync remain unauthorized.

## 18. Execution Closure

- attention job `om-y32ahxua`: full extraction valid; repaired verdict `attention_sparse_concentration_pass`;
- MLP job `om-vjowli0r`: full extraction valid; repaired verdict `mlp_concentration_fail`;
- cross-site: maximum concentration favors attention, while median concentration does not establish broad attention superiority;
- H4: fixed eight-band specificity fails the random 16-d orientation null;
- result entry points: [summary.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_03_E01_architectural_head_channel_concentration/summary.md) and [detailed.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_03_E01_architectural_head_channel_concentration/detailed.md).
