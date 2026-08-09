---
experiment_id: A15_02_04_E01_compositional_attention_write_atlas
anchor_id: 15_02_04_compositional_attention_write_atlas
status: EXECUTED_INSUFFICIENT_CAPABILITY
canonical_language: en
created: 2026-08-06
updated: 2026-08-07
---

# Protocol: A15_02_04_E01 Qwen3 Compositional Attention-Write Spectral Atlas

## 0. Approval Snapshot

**Document status:** `EXECUTED_INSUFFICIENT_CAPABILITY`.

**Approval status:** on 2026-08-06 the researcher explicitly confirmed the frozen research direction, required both full-width attention sites, authorized implementation and complete execution without another approval stop, and selected up to four independent eight-GPU 5090 spot nodes.

**Block audit status:** A `CONFIRMED`; B `CONFIRMED`; C `CONFIRMED`; D `CONFIRMED`; E `CONFIRMED`; F `CONFIRMED`; G `CONFIRMED`.

**Cross-block consistency:** `PASS`. The seven-node hierarchy, equal-sample primary comparison, capability task, two hooked sites, estimators, gates, figures, and execution scope are mutually consistent.

**Execution scope approved:** implementation, local contract tests, smoke, up to four independent single-node `5090-8-spot` ACP jobs, complete extraction/analysis, figure audit, `summary.md`, `detailed.md`, Anchor evidence update, and `daily_research_reports/0807/focus.md`. Registered scientific gates type the result; they do not cancel collection of the complete evidence needed to diagnose a failed gate. Git, graph, sync, publication, and model training remain excluded.

**Purpose:** test whether increasing required semantic composition from one to two to four relation edges causes reliable semantic covariance to occupy relatively lower-background-variance activation directions in deeper isolated attention writes.

**Primary anchor:** [15_01_07 anchor](/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_02_layerwise_representation_spectral_atlas/subanchors/15_02_04_compositional_attention_write_atlas_anchor.md).

**Anchor decision question:** in frozen Qwen3-8B, under matched surface form and evidence, does four-edge relative to one-edge composition show a late-layer rightward redistribution over each layer's own DCLM activation-covariance ranks, especially after `o_proj` and before residual addition?

**Anchor physical prior tested:** common syntax/topic dominate high-background-variance directions, whereas conditional multi-fact semantics may remain distinguishable in lower-background-variance directions.

**Anchor core model term tested:** $T_{\mathrm{rank},\mathrm{post}}$, the late-minus-early change in the post-`o_proj` D2-minus-D0 gap of the 16-band semantic rank centroid.

**Anchor falsifier:** capability and reliability pass, yet deeper composition becomes more discriminable without a positive, stable post-`o_proj` rank redistribution.

**Strongest rival:** deeper layers only increase total answer discriminability or the DCLM background spectrum globally flattens; neither mechanism requires composition-specific semantic mass to move right.

**Treatment:** required path length changes from D0 (one edge) to D1 (two edges) to D2 (four edges).

**Held fixed:** latent world, all four facts, fact order, template, token count, readout index, answer alphabet/entropy, sample count, frozen model, calibration population, layer sets, representation sites, and analysis code.

**Primary controls:** held-out templates, within-world same-token edge intervention, query-binding reversal, two DCLM halves, raw-versus-centered states, and background effective rank.

**Experiment role:** frozen static representation audit; no learning, weight intervention, Router, SAE, or causal module attribution.

**Primary metric from Anchor:**

$$
T_{\mathrm{rank},s}
=\operatorname{median}_{\ell=25:35}
[\rho^{(16)}_{\ell,s,D2}-\rho^{(16)}_{\ell,s,D0}]
-\operatorname{median}_{\ell=1:12}
[\rho^{(16)}_{\ell,s,D2}-\rho^{(16)}_{\ell,s,D0}].
$$

**Claim boundary from Anchor:** a Pass supports only composition-specific redistribution over local activation-covariance rank percentiles in one frozen model and one synthetic spatial-relation distribution. It does not establish literal direction transport, causal composition by attention, universal middle/tail semantics, or downstream utility.

**Minimal setup:** 256 paired five-entity/four-edge worlds, each rendered as a complete seven-node binary composition tree; one equal-sample Latin-selected D0/D1/D2 triplet per world is primary and all seven nodes are the positional robustness audit; four templates; 7,168 node-complete core prompts (including 3,072 primary prompts), 768 counterfactual prompts, and 768 query-binding-reversal prompts; eight balanced compass answers; frozen Qwen3-8B; common `Answer:` readout; full pre-`o_proj` and isolated post-`o_proj` tensors; independent 65,536-token DCLM covariance at each site and block.

**Basic configuration:** 36 blocks, width 4096, 16 equal-rank bands of 256 directions, early blocks 1--12, late blocks 25--35, block 36 separate, 2,000 world-family bootstraps, 2,000 paired condition-swap draws, generator seed `20260806`.

**Conditions to run:** equal-sample primary D0/D1/D2 prompts; all-node L1--L4/C12/C34/ROOT prompts; held-out-template confirmation; same-token edge counterfactuals; query-binding-reversal negative control; raw and nuisance-residualized states; full and half-calibration bases; post primary and pre secondary; equal-dimensional random-subspace diagnostic.

**Pass:** every mandatory gate passes; confirmation-set $T_{\mathrm{rank},\mathrm{post}}$ exceeds the paired D0/D2 condition-swap q95; its world-family-bootstrap 95% lower bound is above zero; both calibration-half estimates and the design-template estimate are positive; the query-binding-reversal control does not independently pass the same rank-shift rule.

**Fail:** every mandatory gate passes, but the post rank-shift rule fails. If late composition discriminability rises while rank shift fails, the typed outcome is `depth_only_pass_rank_shift_fail`.

**Insufficient:** any matching, capability, counterfactual necessity, semantic reliability, hook, covariance, calibration stability, or negative-control guard fails. A normalized location at negligible reliable semantic scale is always insufficient, not a negative scientific result.

**Cannot claim:** that the same direction moved across layers; that the variance maximum moved out of the head; that `o_proj` created information; that attention rather than MLP performs composition; that SAE nodes should be used; or that the result improves routing/training.

**Approval decision:** `EXECUTE`. No further Protocol approval is required for the registered scope.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| data spectrum | spectrum of activations on background text | eigendecomposition of centered DCLM covariance for one block/site | $\Sigma^{bg}=U\Lambda U^T$ | defines local background-variance order | parameter geometry or universal semantics |
| local normalized rank | percentile inside one block/site's own spectrum | $r_i=(i-0.5)/4096$ after descending eigenvalue sort | unitless | compares rank location without vector identity | tracking direction $i$ across layers |
| D0 / D1 / D2 | required composition depth | query uses 1 / 2 / 4 registered path edges | edge count | manipulates composition while facts stay fixed | generic linguistic complexity |
| pre-`o_proj` | attention aggregation before output mixing | tensor entering `self_attn.o_proj`, width 4096 | activation unit | localizes signal before output projection | per-head causal contribution |
| post-`o_proj` | isolated attention write | direct `self_attn.o_proj` output before residual addition | activation unit | primary residual-coordinate geometry | residual or MLP representation |
| raw state $h$ | unadjusted hooked readout vector | state at the `Answer:` colon | activation unit | shows the actual write | pure semantics |
| nuisance residual $z$ | state after additive world/template centering | registered two-way centering within a split | activation unit | reduces shared prompt offsets | removal of all syntax/interactions |
| between-class covariance $B$ | variance of eight answer-class means | balanced covariance of class centroids | activation$^2$ | semantic signal scale/location | causal computation |
| within-class covariance $W$ | variation inside an answer class | covariance over worlds/templates conditional on depth/answer | activation$^2$ | nuisance denominator | all nonsemantic variation |
| raw semantic scale $V$ | total between-class variance | $\operatorname{tr}(B)$ | activation$^2$ | detects noise-floor normalization | spectral location |
| discriminability $D$ | semantic variance relative to within-class variation | $\operatorname{tr}(B)/(\operatorname{tr}(W)+\epsilon)$ | unitless | tests stable class structure | model accuracy or causal use |
| background-relative scale $R$ | semantic scale relative to DCLM variance | $\operatorname{tr}(B)/(\operatorname{tr}(\Sigma^{bg})+\epsilon)$ | unitless | compares scale across sites/layers | spectral location |
| band share $p_k$ | fraction of semantic covariance in rank band $k$ | $\operatorname{tr}(U_k^TBU_k)/\operatorname{tr}(B)$ | unitless; sums to 1 | compares location across unequal $V$ | reliable signal when $V$ is noise |
| banded rank centroid $\rho^{(16)}$ | average local rank of semantic covariance | $\sum_{k=1}^{16}(k-0.5)p_k/16$ | unitless, $(0,1)$ | stable primary location measure | literal motion of a direction |
| $T_{\mathrm{rank},s}$ | deeper-layer change in the D2-vs-D0 rank gap | late median gap minus early median gap | normalized rank; $4096T$ equivalent ranks | decides right redistribution | destination identity or causality |
| cross-template scale $V^\times$ | answer-class structure shared by T3/T4 | cross-product of T3/T4 class-contrast means | activation$^2$ | blocks noisy normalized shares | semantic purity |
| condition-swap null | paired no-depth-effect reference | swap complete D0/D2 state-label pairs within worlds | empirical null | tests depth assignment | arbitrary-label semantics |
| background effective rank | spread of DCLM eigenvalue mass | $\exp[-\sum_iq_i\log q_i]/4096$ | fraction of full rank | separates flattening from semantic shift | semantic redistribution |

## 2. Anchor Alignment

**Decision question:** exactly the Anchor question; required path length is manipulated and post-`o_proj` semantic covariance location in each layer's own data spectrum is primary.

**Physical prior tested:** multi-edge composition is a more conditional variable than shared syntax/topic and may therefore occupy lower-background-variance local directions in later layers.

**Core model term tested:** $T_{\mathrm{rank},\mathrm{post}}$ based on $\rho^{(16)}$, gated by $V$, $D$, capability, and reliability.

**Falsifier:** positive late composition discriminability with no stable rank-centroid shift, or a shift reproduced by query-binding reversal/background flattening.

**Claim boundary:** static, model-specific, generator-specific association. Pre/post comparison is boundary localization, not causal attribution to `o_proj`.

## 3. Tested Hypothesis

### 3.1 Primary hypothesis

After every gate passes,

$$
T_{\mathrm{rank},\mathrm{post}}>0.
$$

The absolute semantic variance may remain largest in F1. A positive $T$ may end in middle bands and does not require extreme-tail concentration.

### 3.2 Registered secondary questions

1. Does full-state discriminability show a corresponding late increase?

$$
T_D=\operatorname{median}_{25:35}[\log D_{D2}-\log D_{D0}]
-\operatorname{median}_{1:12}[\log D_{D2}-\log D_{D0}]?
$$

2. Is location descriptively graded $D0\rightarrow D1\rightarrow D2$?
3. Is the effect already present pre-`o_proj`, or only expressed post-`o_proj`?
4. Which bands gain normalized share, and do they retain non-negligible raw variance/discriminability?

Secondary results cannot rescue a failed primary post test.

## 4. Rival Explanations

| Rival | Observable signature | Registered separator |
| --- | --- | --- |
| total amplification only | $V$ or $D$ rises but $p_k,\rho^{(16)}$ do not move | scale/location reported separately; typed depth-only outcome |
| background spectrum flattening | DCLM effective rank rises for every condition | effective rank is descriptive; primary is a condition difference-in-differences |
| prompt/template geometry | raw shift vanishes on held-out wording or centering | exact seven-node family matching, T3/T4, raw + centered analyses |
| answer/alias leakage | class structure persists after query binding is reversed | identical complete answer alphabet, alias balancing, query-binding reversal |
| shortest-path shortcut | prediction ignores a required-edge change | same-token counterfactual gate at each required edge position |
| unstable calibration directions | sign changes across halves/unbinned only | 16-band projectors, two half bases, unbinned secondary |
| `o_proj` rescaling | pre/post locations differ under non-orthogonal $W_O$ | separate site covariances; no causal claim |
| composition elsewhere | attention fails despite model capability | allowed conclusion is attention-site-specific; MLP stays open |

## 5. Data Construction And Provenance

### 5.1 Source population and generation

The data are synthetic and generated before model inspection with seed `20260806`. A world has five neutral single-token aliases and four directed spatial edges:

$$
e_0\xrightarrow{r_1}e_1\xrightarrow{r_2}e_2
\xrightarrow{r_3}e_3\xrightarrow{r_4}e_4,
$$

where $r_i\in\{-1,0,1\}^2\setminus\{(0,0)\}$. Composition is integer vector addition; only the final displacement is quantized by coordinate signs into the eight compass answers. Intermediate displacements are not sign-compressed.

Each world produces the complete seven-node binary composition tree:

- D0 leaves: L1 $e_0\rightarrow e_1$, L2 $e_1\rightarrow e_2$, L3 $e_2\rightarrow e_3$, and L4 $e_3\rightarrow e_4$;
- D1 internal nodes: C12 $e_0\rightarrow e_2$ and C34 $e_2\rightarrow e_4$;
- D2 root: ROOT $e_0\rightarrow e_4$.

The **primary** comparison chooses exactly one D0 leaf and one D1 internal node per world with a frozen Latin selector and always uses ROOT for D2. This avoids the original position confound (always using the first edge/left half) while retaining 256 independent world observations at every depth. The **all-node** secondary audit retains all seven nodes, rather than pooling 4/2/1 observations into unequal effective sample sizes.

Worlds with zero displacement at any of the seven nodes are rejected. A large model-independent pool is generated, then deterministic integer selection chooses 256 worlds so (i) every primary depth-answer cell has exactly 32 worlds, (ii) every node-position/answer cell has exactly 32 worlds, (iii) each D0 position is selected in 64 primary triplets and each D1 position in 128, and (iv) the registered token-length constraints hold. Selection uses only generator/tokenizer metadata; Qwen logits and activations are forbidden.

### 5.2 Concrete construction example

| Edge | Fact | Vector | Endpoint coordinate |
| --- | --- | --- | --- |
| $r_1$ | `Elias is located 1 step right and 0 steps up from Mara.` | $(1,0)$ | Elias $(1,0)$ |
| $r_2$ | `Axel is located 0 steps right and 1 step up from Elias.` | $(0,1)$ | Axel $(1,1)$ |
| $r_3$ | `Irene is located 1 step left and 0 steps up from Axel.` | $(-1,0)$ | Irene $(0,1)$ |
| $r_4$ | `Emil is located 0 steps right and 1 step up from Irene.` | $(0,1)$ | Emil $(0,2)$ |

The same facts yield all seven semantic nodes:

| Node | Depth | Query | Required computation | Target |
| --- | --- | --- | --- | --- |
| L1 | D0 | `Where is Elias relative to Mara?` | $(1,0)$ | ` east` |
| L2 | D0 | `Where is Axel relative to Elias?` | $(0,1)$ | ` north` |
| L3 | D0 | `Where is Irene relative to Axel?` | $(-1,0)$ | ` west` |
| L4 | D0 | `Where is Emil relative to Irene?` | $(0,1)$ | ` north` |
| C12 | D1 | `Where is Axel relative to Mara?` | $(1,0)+(0,1)$ | ` northeast` |
| C34 | D1 | `Where is Emil relative to Axel?` | $(-1,0)+(0,1)$ | ` northwest` |
| ROOT | D2 | `Where is Emil relative to Mara?` | $[(1,0)+(0,1)]+[(-1,0)+(0,1)]$ | ` north` |

For illustration, a primary triplet could select L1/C12/ROOT; the actual selector is frozen by the balanced manifest, not chosen after model inspection.

T1 renders D2 as:

```text
Use the facts to answer the query.
Facts:
- Elias is located 1 step right and 0 steps up from Mara.
- Axel is located 0 steps right and 1 step up from Elias.
- Irene is located 1 step left and 0 steps up from Axel.
- Emil is located 0 steps right and 1 step up from Irene.
Query: Where is Emil relative to Mara?
Add the horizontal and vertical steps along the path from the query start to the query end. A positive horizontal total means right and a negative total means left; a positive vertical total means up and a negative total means down. Use the two total signs to answer with exactly one word from: north, northeast, east, southeast, south, southwest, west, or northwest.
Answer:
```

The answer is not appended during state extraction. The readout is the final colon. All eight leading-space answer strings are audited single tokens. A same-token counterfactual changes the horizontal-direction slot in $r_3$ from `left` to `right`, preserves every template's exact token count, and changes the D2 target from ` north` to ` northeast`.

With the frozen tokenizer and `add_special_tokens=False`, all seven nodes have identical length within a world/template and the final-colon readout is the final token. The frozen lengths are T1 160, T2 166, T3 167, and T4 160 tokens for every world, node, and answer; both controls exactly match their source prompt length.

### 5.3 Templates and leakage boundary

- T1/T2 are design templates used for implementation and smoke.
- T3/T4 are sealed confirmation paraphrases; their semantic metrics stay unopened until data, hooks, metrics, and thresholds are frozen.
- Facts use explicit `0/1 step` and `right/left/up/down` slots. One identical rule in every prompt instructs the model to add horizontal/vertical steps and map the two total signs to the complete eight-word answer alphabet; no target-specific option or marked choice occurs.
- Because the complete answer line is constant across every world, node, template condition, and class, it is a shared prompt component rather than answer leakage. Raw states disclose its common effect; world/template centering and query-binding reversal guard class-dependent interpretation.
- Templates vary wording while retaining fact count, task, query slots, and readout boundary.

The frozen wrappers are:

```text
T1: Use the facts to answer the query.
    Facts: <four bulleted facts>
    Query: Where is {query_end} relative to {query_start}?
    Answer:

T2: Determine the requested relation using only these statements.
    Statements: <four numbered facts>
    Query: Relative to {query_start}, where is {query_end}?
    Answer:

T3: Consider the following spatial facts.
    Facts: <four lettered facts, each prefixed by "(a) ", ..., "(d) ">
    Query: Using the relevant facts, where is {query_end} compared with {query_start}?
    Answer:

T4: A small map is described below.
    Description: <four bulleted facts>
    Query: From {query_start}'s position, where is {query_end}?
    Answer:
```

For a fact whose endpoint is `A`, source is `B`, and vector is $(x,y)$, the frozen relation realization is:

```text
A is {prefix} {x_magnitude} {x_direction}
and {y_magnitude} {y_direction} from B.
```

`x_magnitude/y_magnitude` are `0 steps` or `1 step`; a nonzero negative component uses `left/down`, a nonzero positive component uses `right/up`, and a zero component uses the fixed dummy direction `right/up` whose magnitude is explicitly zero. Prefixes are T1 `located`, T2 `positioned`, T3 `placed`, and T4 `situated`. Thus all eight relations have identical token-slot structure within a template while the wrappers remain paraphrases.

This coordinate-factorized realization replaced the initial variable-length phrase lexicon after the pre-model integer audit proved that exact node-position-by-answer token-length histograms were otherwise infeasible. The first engineering capability smoke showed that the grammatical candidate without a fixed answer alphabet was below the continuation threshold; the second improved D0/D2 but not D1. Therefore, before the formal run, wording was simplified to `1 step/0 steps` and the same explicit addition/sign rule plus complete answer alphabet was added to every prompt. No spectral statistic was inspected. The semantic graph, target labels, composition depths, sample sizes, metrics, and gates are unchanged.

All rendered facts end with a period. The tokenizer audit froze the next-token targets as:

| Label | Leading-space token ID |
| --- | ---: |
| north | 10200 |
| northeast | 40829 |
| east | 10984 |
| southeast | 41452 |
| south | 9806 |
| southwest | 52985 |
| west | 9710 |
| northwest | 52242 |

If a model/tokenizer hash change alters any ID or makes a target multi-token, Block B reopens; no label remapping is allowed silently.

### 5.4 Matching and balancing contract

1. Every alias is one token in every registered context and is screened against spatial words.
2. The frozen 64-name/token-ID pool is listed below. Alias-to-graph-position assignment follows a deterministic Latin schedule: every alias appears exactly four times at each graph position across 256 worlds, while answer-conditioned counts are balanced as closely as the exact $g\times y$ quotas allow.
3. For every world-template seven-node family, all nodes have identical facts, fact order, token count, readout index, and answer-space entropy. Only the two query aliases differ.
4. Within every template and primary depth, and separately within every template and node position, the exact prompt-length histogram is identical across the eight answer classes. If no 256-world selection satisfies this, stop as `insufficient_matching`; do not relax after model inspection.
5. Fact order uses a frozen cyclic/reversal schedule balanced over worlds and reused across depths/templates.
6. Every primary $g\times y$ cell and every node-position$\times y$ cell has 32 worlds. The selected primary subset therefore has equal sample size across D0/D1/D2, while the all-node audit exposes position-specific behavior without pretending its 4/2/1 node counts are independent depth samples.
7. The statistical unit is the world family. Templates/prompts are repeated measurements.

```text
David:6798, Paul:6898, Jack:7607, James:7801, Michael:7937, Alex:8515,
Robert:8397, Bill:8596, Scott:9815, George:9857, Mary:10244, Carol:10252,
Peter:11044, Thomas:11108, Chris:11266, Mike:11268, Martin:11565,
Richard:11867, Jeff:11885, William:12375, Ryan:13646, Steve:13809,
Harry:13928, Charles:14927, Joseph:15115, Daniel:15118, Kelly:18661,
Marc:18880, Matthew:18939, Patrick:19626, Allen:20060, Sarah:20445,
Tony:18528, Anthony:20696, Harris:21071, Clark:21304, Dave:20238,
Andrew:13615, Kevin:16364, Taylor:16439, Brad:17041, Brian:17083,
Jordan:17089, Robin:17143, Albert:17513, Anton:17500, Henry:17599,
Jason:18477, Eric:16247, Wilson:17426, Frank:9270, Rose:15964,
Ross:20482, Lewis:20607, Mara:85504, Elias:85656, Axel:86679,
Irene:87213, Emil:87724, Jenna:87254, Lydia:91206, Fiona:88843,
Howard:19870, Evelyn:95325
```

These IDs are for the leading-space forms under the frozen tokenizer. The generator rechecks them in every registered context; any split/merge is a matching failure.

### 5.5 Additive nuisance control

The primary confirmation analysis uses two-way additive centering within T3/T4 on the selected D0/D1/D2 triplets:

$$
z_{\ell,s,g,w,t}=h_{\ell,s,g,w,t}
-\bar h_{\ell,s,\cdot,\cdot,t}
-\bar h_{\ell,s,\cdot,w,\cdot}
+\bar h_{\ell,s,\cdot,\cdot,\cdot}.
$$

Raw $h$ is always reported. The all-node audit applies the same estimator separately by registered node position. No separate template-only prompt vector is subtracted: it would come from a different semantic/positional context and would not cleanly identify syntax.

### 5.6 Controls

- **Edge counterfactual:** the selected primary nodes of a deterministic 64-world subset, balanced by depth/answer/required-edge position, receive one same-token relation flip per query and a recomputed answer.
- **Query-binding reversal:** for each selected primary node in the same 64 worlds, keep all four facts unchanged, exchange only the query start/end aliases, and retain the original label. The recomputed answer is the exact opposite compass direction, while the query token inventory, token count, and alias positions are preserved. This breaks the registered fact-query-to-label binding without relying on an invalid edge-order permutation.
- **Random subspaces:** equal-dimensional random orthonormal subspaces contextualize band enrichment; they do not replace the primary local-rank test.

This yields exactly 7,168 node-complete core prompts ($256\times7\times4$), of which 3,072 form the equal-sample primary subset ($256\times3\times4$), plus 768 counterfactual and 768 query-binding-reversal prompts, for 8,704 model prompts total. The primary selector, 64-world control subset, interventions, and query reversals are frozen by manifest before logits are computed.

### 5.7 Record schema and provenance

```text
world_id, control_family_id, template_id, split, composition_depth,
node_id, node_position, node_depth, primary_selected, selection_schedule_id,
entity_aliases, edge_vectors, rendered_facts, fact_order,
query_start, query_end, answer_class, target_token_id,
input_text, input_ids, input_token_count, readout_index,
required_edge_ids, intervention_edge_id, generator_seed,
generator_hash, tokenizer_hash, model_hash
```

All JSONL files receive SHA-256 manifests. Wrong answers, refusals, and low-confidence cases remain and count against gates; none may be filtered.

### 5.8 Known distribution shift

This is controlled English spatial language with five entities and four path edges, not natural discourse, arbitrary symbolic composition, or a learned ontology. Any result is restricted to this generator and frozen model.

## 6. Learning Task And Permitted Supervision

There is no learning task in the optimization sense. The frozen audit returns:

1. **Capability output:** logits over eight registered leading-space compass tokens at `Answer:`, with accuracy, correct-token NLL, and margin.
2. **Representation output:** one 4096-dimensional pre and one post vector for every block/prompt.

Inputs contain instruction, four facts, query, and the same complete eight-label answer alphabet. The correct target comes only from coordinate arithmetic and is never marked in the prompt. Labels form $B,W$, capability metrics, and registered controls; they never fit a probe, choose a layer, edit prompts, or select worlds.

Invalid generated worlds are rejected before model calls. Refusals/wrong answers remain. Capability plus edge intervention is required because answer-conditioned covariance is composition-related only if the model predicts computed answers and responds to required facts.

## 7. Model / Architecture And Frozen Variants

- Model: `/data/share/Qwen3-8B`, frozen.
- Audited config: 36 blocks, width 4096, 32 query heads, 8 key/value heads, `attention_bias=false`.
- Forward: plain causal prompt without a chat template, `add_special_tokens=False`, bfloat16, deterministic evaluation, `use_cache=False`, no gradient or model update.
- Readout: final `Answer:` colon.
- Pre site: tensor entering `self_attn.o_proj`.
- Post site: direct `self_attn.o_proj` output before residual addition.
- Primary site: post; secondary localization site: pre.
- Forbidden: residual sum, RMSNorm output, MLP, SAE, learned probe, parameter singular basis.

All hooks must be `[batch, sequence, 4096]`. Replay must satisfy

$$
\frac{\|y_{hook}-\mathrm{F.linear}(a_{hook},W_O,b_O)\|_F}
{\|y_{hook}\|_F+10^{-30}}<10^{-6}.
$$

The loaded module must confirm $b_O=0$. Every block/site gets its own centered DCLM covariance and eigensystem; pre/post and cross-layer eigenvectors are never shared coordinates.

### 7.1 Calibration reuse contract

Reuse the audited 128-document, 65,536-token DCLM tensor, split into two fixed 32,768-token halves, with SHA-256:

```text
d88620267dbdc9c2b87ec24c2f51d9e6fb317cb8c051ec96503414ea9bff60b9
```

E03 pre moments may be reused only after exact model/tokenizer/calibration/layer/site/count/file-hash checks. Post covariance uses either:

1. complete, guard-passing direct post moments from E04 with identical hashes; or
2. an exact transform of E03 pre moments by frozen $W_O$.

For row-vector activations $y=xW_O^T$:

$$
s_y=s_xW_O^T,\qquad G_y=W_OG_xW_O^T.
$$

Direct DCLM hook samples must agree with transformed moments below $10^{-6}$ relative error. Otherwise stop as `insufficient_covariance`; semantic prompts can never calibrate the basis.

## 8. Training Objective And Optimization

No model is trained; optimizer, learning rate, schedule, validation stopping, and checkpoint selection are not applicable.

Fixed estimators are:

$$
B_{\ell,s,g}=\frac{1}{8}\sum_{y=1}^{8}
(\mu_{\ell,s,g,y}-\bar\mu_{\ell,s,g})
(\mu_{\ell,s,g,y}-\bar\mu_{\ell,s,g})^T,
$$

$$
W_{\ell,s,g}=\frac{1}{8}\sum_y
\operatorname{Cov}_{w,t}(z_{\ell,s,g,w,t}\mid y),
$$

followed by registered $V,D,R,p_k,\rho^{(16)}$, and $T_{rank}$. No model-dependent setting may be selected on T3/T4. Batch size may decrease after OOM if deterministic replay is identical. Changing data, readout, sites, bands, primary statistic, thresholds, or gates reopens the affected block.

## 9. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Rival separated | Why needed | Evidence role | Pass / fail / insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- |
| post D0/D1/D2 | rank redistribution | total amplification | direct Anchor test | primary | Section 15 verdict rules | Figure 1; primary table |
| pre D0/D1/D2 | boundary localization | post-only geometry | locate effect boundary | secondary | sign/effect reported; site guard may be insufficient | Figure 1 overlay |
| L1--L4/C12/C34/ROOT | node-position confounding | first-edge/left-half artifact | expose every constructed semantic node | robustness guard | Section 15 node-position rule | Figure 5; node table |
| T1/T2 design | frozen development | prompt selection | settings freeze before confirmation | guard | design sign positive or report fail; matching failure insufficient | robustness table |
| T3/T4 confirmation | untouched evidence | template artifact | primary inference | primary | full Pass rule / valid Fail / gate insufficient | Figures 1--3 |
| calibration halves | local-basis stability | eigenvector instability | protect rank inference | guard | both primary signs positive / disagreement fails rule | calibration table |
| edge counterfactual | required facts | shortcut | verify prediction follows changed edge | guard | log-odds rule passes / otherwise insufficient | capability table |
| query-binding reversal | fact-query-label binding | lexical leakage | must not reproduce core | guard | reversal fails core rule / otherwise insufficient | control table |
| raw vs centered | nuisance robustness | prompt offset | expose dependence on centering | secondary | both disclosed; primary centered fixed | sensitivity plot |
| random subspaces | destination specificity | arbitrary orientation | contextualize band enrichment | secondary | report relative null; numerical error insufficient | band table |
| background effective rank | spectrum flattening | global geometry rival | separate background from semantic shift | diagnostic | always report if covariance valid | Figure 4 |

**Seeds:** generator/selection `20260806`; bootstrap `15010701`; condition swap `15010702`; random subspace `15010703`; control subset `15010704`.

**Checkpoint:** exact frozen local Qwen3-8B files only, with a model hash manifest. No trained checkpoint is selected.

**Layers:** early 1--12; late 25--35; block 36 separate; all 36 shown. No layer may be removed after inspection.

## 10. Primary Metric

For each block, site, and depth:

$$
p_{\ell,s,g,k}
=\frac{\operatorname{tr}(U_{\ell,s,k}^TB_{\ell,s,g}U_{\ell,s,k})}
{\operatorname{tr}(B_{\ell,s,g})},
\qquad
\rho^{(16)}_{\ell,s,g}
=\sum_{k=1}^{16}\frac{k-0.5}{16}p_{\ell,s,g,k}.
$$

$T_{\mathrm{rank},\mathrm{post}}$ is defined in Section 0. Positive values mean that, relative to D0 and to early layers, D2 allocates more reliable semantic covariance to larger local rank percentiles in late layers.

The primary estimate uses T3/T4 nuisance-residualized states and the full DCLM basis. Uncertainty uses 2,000 cluster bootstraps of whole world families, retaining all depths/templates. The null uses 2,000 within-world D0/D2 swaps of complete state-label pairs; one draw's swap mask is shared across layers/sites/templates.

This metric removes total semantic scale while retaining ordered background-rank location. Capability, reliability, half-basis, and controls prevent a noisy normalized share from becoming a false positive. If early D2 is too weak to locate, the result is `insufficient_reliability`, not evidence of no shift.

### 10.1 Primary pass rule

All are required:

1. every mandatory Section 15 gate passes;
2. the T3/T4 point estimate exceeds condition-swap q95;
3. its world-family-bootstrap 95% lower bound is above zero;
4. T1/T2, calibration-half A, and calibration-half B estimates are each positive;
5. query-binding reversal does not satisfy items 2--4.

No smallest effect size is imposed for this first static audit. Report $4096T$ as equivalent ranks and describe effects below 64 equivalent ranks as small.

## 11. Secondary Metrics

1. $V=\operatorname{tr}(B)$, activation$^2$.
2. $D=\operatorname{tr}(B)/(\operatorname{tr}(W)+\epsilon)$, unitless.
3. $R=\operatorname{tr}(B)/(\operatorname{tr}(\Sigma^{bg})+\epsilon)$, unitless.
4. Raw band variance per direction $\bar b_k=\operatorname{tr}(U_k^TBU_k)/256$.
5. Band semantic-to-nuisance ratio $j_k=\operatorname{tr}(U_k^TBU_k)/(\operatorname{tr}(U_k^TWU_k)+\epsilon)$.
6. Cross-template reliable scale:

$$
V^\times_{\ell,s,g}=\frac{1}{8}\sum_y
(\mu^{T3}_{g,y}-\bar\mu^{T3}_{g})^T
(\mu^{T4}_{g,y}-\bar\mu^{T4}_{g}).
$$

7. $T_D$ from Section 3 and D1 ordered contrasts.
8. Unbinned centroid $\sum_i r_i\pi_i$, sensitivity only.
9. DCLM normalized effective rank/eigenvalue curves, background diagnostic only.
10. Eight-way accuracy, correct-token NLL/margin, and counterfactual log-odds shift.

No learned probe is registered.

## 12. Known Good / Known Bad / Known Confusing Cases

### Known good

- Generator arithmetic reproduces all seven example-node targets.
- All eight leading-space labels are one Qwen token.
- A unit-test covariance placed in F1 has lower $\rho^{(16)}$ than equal trace in F12.
- Hooked post replay matches `F.linear(pre, W_O, b_O)` below $10^{-6}$.
- DCLM full/half moments reconstruct count, mean, trace, and covariance within tolerance.

### Known bad

- A canonical answer occurs outside the one identical complete answer-alphabet line, or one option is marked differently.
- One seven-node family differs in token count/readout position.
- Any record/layer is removed after results.
- Post hook includes residual addition.
- D2 is near chance or ignores counterfactual edges.
- $p_k$ is interpreted without reliable $V^\times$.

### Known confusing

- F1 may remain the largest raw band while $\rho^{(16)}$ moves right.
- Larger D2 $V$ is not a shift; smaller D2 $V$ does not invalidate location if reliability passes.
- A flatter background spectrum is not semantic redistribution.
- Pre/post differences under $W_O$ are not evidence that `o_proj` created information.
- Block 36 is descriptive only.
- An unstable unbinned result cannot override the banded/half-basis result.

## 13. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| 0 data contract | are seven-node arithmetic, primary/node-position balance, leakage, and token contracts exact? | candidate worlds/tokenizer | all checks pass or stop | generator audit | frozen manifests |
| 1 calibration | can pre/post covariance be reused/derived exactly? | E03/E04 moments, $W_O$ | hashes/counts/replay pass or stop | provenance report | full/half bases |
| 2 smoke | do all seven nodes, hooks, storage, metrics, and capability plausibility work? | 32 balanced worlds, T1/T2, blocks 1/12/25/35/36 | engineering gates pass and design primary D2 accuracy $\ge0.25$ | smoke manifest/table | full design |
| 3 design | is the model capable before confirmation opens? | 256 worlds, T1/T2, all seven nodes/sites/blocks | registered primary capability and counterfactual gates are evaluated; complete evidence collection continues so any failure is diagnosable | design gate table | full confirmation |
| 4 confirmation | collect untouched primary evidence | frozen T3/T4 | complete hashes/coverage or stop | state manifests | analysis |
| 5 analysis | does primary pass all rules? | core/control states, full/half bases | one typed Section 15 verdict | bootstrap/null tables | evidence record |
| 6 documentation | do visuals support only allowed claim? | verdict/tables | figure contracts audited | visual checklist | summary, detailed, Anchor update |

## 14. Algorithm Specification

**Input:** frozen Qwen3-8B/tokenizer; E03 pre DCLM moments; optional valid E04 post moments; generator seed/templates; registered layers/sites/splits/controls/seeds.

**Parameters:**

```text
n_worlds = 256
n_entities = 5
n_edges = 4
depths = [D0, D1, D2]
node_positions = [L1, L2, L3, L4, C12, C34, ROOT]
primary_nodes_per_world = 3
answers = 8
templates = [T1, T2, T3, T4]
design = [T1, T2]
confirmation = [T3, T4]
n_bands = 16
band_width = 256
early_layers = 1..12
late_layers = 25..35
terminal_layer = 36
n_bootstrap = 2000
n_condition_swap = 2000
node_complete_core_prompts = 7168
primary_core_prompts = 3072
counterfactual_prompts = 768
query_binding_reversal_prompts = 768
```

**Intermediate variables:** selected worlds, token audits, prompt manifests, capability logits, semantic states, full/half DCLM bases, $B,W,V,D,R,p,j,\rho^{(16)}$, bootstrap/null/control estimates.

**Steps:**

1. Generate candidate worlds; construct L1--L4/C12/C34/ROOT and reject zero displacement at any node.
2. Jointly select 256 worlds and a Latin primary selector using only generator/tokenizer metadata and exact primary/node-position balance constraints.
3. Assign aliases/orders; render T1--T4 for all seven nodes; verify leakage, targets, family matching, and primary/node-position class-length histograms.
4. Generate/audit controls on the 64-world selected-primary subset; hash all data and selector; seal T3/T4.
5. Audit model, hooks, pre/post replay, and target token IDs.
6. Verify calibration provenance; reuse valid direct post moments or transform pre moments; fit full/half eigensystems per block/site.
7. Run smoke; repair engineering failures only within the frozen contract.
8. Extract/analyze T1/T2 for all seven nodes and evaluate the design capability/necessity gates.
9. Extract T3/T4 unchanged for all seven nodes; store float32 analysis states and exact manifests. A failed scientific gate is recorded as `insufficient_*` but does not erase the already authorized diagnostic collection.
10. Compute raw/centered covariances; report $V,D,R$ before location.
11. Apply reliability gates; compute band shares, $T$, bootstraps, nulls, and controls.
12. Assign one verdict; render/audit figures; write summary/detailed and update the Anchor only.

**Approved command shape:**

```text
python generate_composition_data.py --seed 20260806 --worlds 256
python audit_contracts.py --mode data_and_tokenizer
torchrun --nproc_per_node 1 extract_states.py --mode smoke
torchrun --nproc_per_node 8 extract_states.py --mode design
torchrun --nproc_per_node 8 extract_states.py --mode confirmation
python analyze_spectral_atlas.py --bootstrap 2000 --condition-swaps 2000
```

**Outputs:** provenance manifests; capability/control tables; semantic-state/covariance artifact maps; layer-depth and node-position scale/location tables; bootstrap/null/half-basis tables; five central figures; typed verdict; `summary.md`; `detailed.md`; 0807 `focus.md`.

**Debug artifacts:** failed-world report; token mismatches; hook replay by block; covariance transform/reconstruction errors; coverage/energy checks; per-template/half trajectories; counterfactual edge-position table.

**Failure reasons:** `matching`, `capability`, `necessity`, `node_position`, `hook`, `covariance`, `basis_stability`, `reliability`, `negative_control`, `resource_ceiling`, `artifact_incomplete`.

## 15. Success / Failure / Insufficient Evidence

### 15.1 Mandatory gates

1. **Data/matching:** all seven node targets, leakage, primary and node-position balance, selector/hash, token counts, target tokens, and readout checks pass exactly.
2. **Confirmation capability:** T3/T4 accuracy is at least 0.70 for D0, 0.55 for D1, and 0.40 for D2; each depth's Wilson 95% lower bound exceeds 0.25, twice eight-way chance.
3. **Counterfactual necessity:** for every depth and in aggregate, the paired change in new-vs-old answer log odds has a world-bootstrap 95% lower bound above zero; each required edge position has a positive point estimate.
4. **Hook:** all 36 pre/post shapes, direct replay, deterministic replay, and no-residual checks pass.
5. **Covariance:** exact calibration/model/site/count hashes; 65,536 tokens and two 32,768 halves; direct/transform replay below $10^{-6}$; reconstruction below $5\times10^{-4}$; trace error below $5\times10^{-5}$; orthogonality below $5\times10^{-4}$.
6. **Basis:** each site's aggregate head (F1), middle (F2--F8), and tail (F9--F16) full/half projector overlap exceeds random expectation by normalized excess at least 0.25 in at least 34/36 blocks; blocks 35/36 must pass. All 16 band overlaps are reported, and the primary $T$ sign must agree across half bases.
7. **Reliable semantic scale:** for post D0 and D2 separately, the world-bootstrap 95% lower bound of median T3/T4 cross-template $V^\times$ is above zero in both early and late sets. At least 8/12 early and 8/11 late blocks have positive point estimates. D1 reliability is needed only for the graded secondary claim.
8. **Negative control:** query-binding reversal must not independently satisfy the full core rank-shift Pass rule; otherwise `insufficient_negative_control`.
9. **Node-position robustness:** all seven positions are reported. The post primary $T$ sign must be preserved for at least three of the four equal-sample D0 leaf substitutions, and neither D1 half may show a statistically significant opposite early-to-late depth ordering. Otherwise `insufficient_node_position`.
10. **Coverage:** every registered world/template/node/control/layer/site record appears once, with no result-dependent filtering.

### 15.2 Typed outcomes

- `rank_shift_pass`: every gate and Section 10.1 primary rule pass.
- `depth_only_pass_rank_shift_fail`: every gate passes, $T_D$ bootstrap lower bound is above zero, but rank shift fails.
- `joint_fail`: every gate passes and neither primary rank shift nor $T_D$ passes.
- `rank_shift_pass_depth_not_established`: rank shift passes but $T_D$ does not; claim only redistribution.
- `insufficient_<gate>`: any mandatory gate fails; no scientific Pass/Fail on redistribution is assigned.

Band destination comes from $p_k,\bar b_k,j_k$ and cannot change the primary verdict. Pass never requires a tail destination.

### 15.3 Central figure contracts

**Figure 1 — decisive rank-redistribution trajectory**

- Question: does D2 relative to D0 shift right more in late than early blocks?
- Metric/unit: $\rho^{(16)}$ and $\Delta\rho^{(16)}=\rho_{D2}-\rho_{D0}$; normalized rank, plus equivalent ranks.
- Data: T3/T4 centered core prompts; full DCLM basis; world bootstrap.
- Axes: blocks 1--36; D0/D1/D2 post trajectories above; post/pre D2-D0 gaps below; early/late shading; block 36 hollow.
- Decides: primary direction and magnitude.
- Limitation: does not show raw signal scale or causal transport.

**Figure 2 — scale-versus-location audit**

- Question: is location supported by non-negligible signal despite D0/D2 scale differences?
- Metric/unit: log $V$, log $D$, and $\rho^{(16)}$ by depth.
- Decides: whether normalized location is above the reliability floor.
- Limitation: does not identify destination alone.

**Figure 3 — layer-by-band destination map**

- Question: which bands gain D2 share relative to D0?
- Metric/unit: $p_{D2,k}-p_{D0,k}$ with companion $\bar b_k$ and $j_k$.
- Axes: F1--F16 by block; F1 head, F2--F8 middle, F9--F16 tail.
- Decides: descriptive destination with scale/reliability context.
- Limitation: no band is a universal semantic module.

**Figure 4 — background/control separation**

- Question: can flattening, calibration instability, or query-binding reversal explain Figure 1?
- Metric/unit: DCLM effective-rank fraction, core/reversal $T$, and half-basis $T$.
- Decides: rival guards.
- Limitation: controls do not prove attention causality.

**Figure 5 — seven-node hierarchy audit**

- Question: is the depth effect shared across leaf/internal positions rather than caused by always selecting one path segment?
- Metric/unit: layer-by-node heatmaps for $\rho^{(16)}$, log $V$, log $D$, and accuracy, separately for pre and post.
- Axes: blocks 1--36 by L1/L2/L3/L4/C12/C34/ROOT, with primary-selected aggregate beside position-specific cells.
- Decides: the node-position robustness gate and which hierarchy levels are interpretable.
- Limitation: nodes from the same world are repeated measurements, not seven independent samples.

Figures 1, 3, and 5 are mandatory for the advisor readout if the corresponding gates are interpretable; Figure 2 supplies the scale guard. If a gate fails, the failed-gate evidence is shown alongside, not hidden by, the scientific plot.

## 16. What This Cannot Claim

1. The 500th or any individual direction is the same across layers.
2. Semantic information literally travels from head to middle/tail eigenvectors.
3. Deeper representations generally contain more complex semantics.
4. Attention causally computes the four-edge relation.
5. `o_proj` creates/removes semantic information; pre/post is a coordinate-boundary audit.
6. The absolute variance peak leaves the head.
7. A middle/tail band has universal semantic identity across tasks/layers/models.
8. SAE dictionary features correspond to the atomic/composition nodes here.
9. Residual, MLP, Router, expert utility, or training benefit follows.
10. The synthetic spatial result generalizes to natural language or other models.

## 17. Block Confirmation Ledger And Review Notes

### 17.1 A--G ledger

| Block | State | Candidate decision | Confirmation accepts |
| --- | --- | --- | --- |
| A question/boundary | CONFIRMED | activation data spectrum; local rank redistribution; post primary; static claim | hypothesis, rival, falsifier, cannot-claim boundary |
| B data/provenance | CONFIRMED | 256 seven-node worlds; equal-sample Latin-selected primary triplets; all-node audit; 4 templates; 8 labels; 64 control worlds | generator, splits, filters, leakage guards, example unit |
| C task/supervision | CONFIRMED | frozen eight-way next-token capability + state extraction; generator labels only; no probe | input/output, target source, necessity logic, invalid behavior |
| D model/architecture | CONFIRMED | Qwen3-8B; all 36 full-width pre/post sites; separate DCLM bases; no residual/MLP/SAE | information flow, dimensions, frozen site choices |
| E objective/optimization | CONFIRMED | no training; fixed centering/covariance/bands; no confirmation tuning | estimator and no-optimization boundary |
| F comparison/evidence | CONFIRMED | $T_{rank,post}$; scale/reliability and node-position gates; paired null; controls; typed outcomes; figures | metric, comparisons, pass/fail/insufficient rules |
| G execution/reproducibility | CONFIRMED | fixed seeds/paths; up to four single-node jobs; complete evidence collection; curated records/focus | resources, artifacts, stops, execution authorization |

### 17.2 Material AI audit decisions

1. The object is the activation data covariance spectrum, never a parameter spectrum.
2. Primary location uses 16 stable 256-dimensional projectors; individual eigenvector ranks are sensitivity only because near-degenerate directions rotate.
3. The null swaps D0/D2 within worlds. Renaming class labels would leave between-class covariance unchanged and is invalid.
4. $V$, $D$, and $p_k/\rho^{(16)}$ are separate; D0/D2 scale differences cannot alone pass.
5. Template nuisance uses balanced two-way centering, not an out-of-context template-only vector.
6. E03/E04 calibration assets require exact hashes; post covariance can use an exact $W_O$ congruence transform with direct-hook guard.
7. Post is primary as the isolated residual-coordinate write; pre is secondary and pre/post difference is not causal evidence.
8. Every world exposes the complete seven-node tree. The primary comparison uses one balanced D0/D1/D2 observation per world; all-node results are a repeated-measures robustness audit, not unequal-depth pooling.
9. The first model-independent selection attempt proved the variable-length relation lexicon incompatible with exact token matching. Block B was corrected before any model call to the frozen coordinate-factorized, equal-slot realization in Section 5.3; dependent Blocks C and F were re-audited and remain consistent.
10. Permuting relation vectors across a complete path cannot change ROOT because vector addition is commutative. The invalid candidate control was replaced before any model call by exact query-binding reversal, which preserves facts and query token inventory but deterministically changes the correct label to its opposite.

### 17.3 Preliminary cross-block consistency

| Check | Candidate result |
| --- | --- |
| data exposes A's phenomenon | PASS: all facts stay fixed; the primary selector changes required path depth without fixing one leaf/half |
| fields/targets obey C | PASS: the complete alphabet is constant; the arithmetic target is unmarked and computed from facts/query |
| task matches D | PASS: next-token capability and exact pre/post hooks use frozen Qwen |
| estimator represents task success | PASS: fixed answer-conditioned covariance, no learned shortcut |
| controls isolate registered rivals | PASS: paired worlds, token matching, interventions, and query-binding reversal |
| metric separates strongest rival | PASS: scale, flattening, and location are distinct |
| development cannot access confirmation | PASS: T3/T4 sealed until design gates pass |
| resources/stops cover conditions | PASS: Block G authorizes at most four `5090-8-spot` single-node jobs; live preflight remains an execution check |
| verdict yields one boundary update | PASS: outcomes are exhaustive |

### 17.4 Requested execution boundary

The researcher approved:

```text
APPROVE implementation
APPROVE smoke
APPROVE automatic full design + sealed confirmation extraction,
analysis, visual audit, summary/detailed records, and Anchor evidence update
including complete diagnostic collection when a scientific gate types the result as insufficient
```

Resource ceiling: at most four independent one-node `5090-8-spot` ACP jobs, each with `WORKER_NODES=1`, `SPEC=n12lp.nn.i10a.8`, `NPROC_PER_NODE=8`, `QUOTA_TYPE=spot`, and `PRIORITY=normal`; maximum aggregate use is 32 GPUs. Multi-node jobs and the debug cluster are forbidden. Batch-size-only changes after OOM are allowed if deterministic replay passes. Crossing the four-job ceiling needs new approval.

Worker code/raw outputs:

```text
Projects/from-attention-to-search/XingyuD/MoE_Routing_Experiments/active/
a15_01_07_e01_qwen3_compositional_attention_write_spectral_atlas/
```

Required worker layout:

```text
data/worlds.jsonl
data/core_prompts.jsonl
data/counterfactual_prompts.jsonl
data/query_binding_reversal_prompts.jsonl
data/manifest.json
runs/smoke/
runs/design/
runs/confirmation/
runs/analysis/tables/
runs/analysis/figures/
runs/analysis/verdict.json
```

Curated records remain in this experiment folder. No commit, push, graph edit, root sync, collaborator sync, or publication is requested.

### 17.5 Review note

The 2026-08-06 researcher instruction confirmed A--G, required both full-width representations (concatenated multi-head output before `o_proj`, and isolated output after `o_proj`), requested a complete self-contained report and 0807 focus, and authorized complete execution on up to four eight-GPU 5090 spot nodes without another approval stop. This same file was promoted to `APPROVED_FOR_EXECUTION` after the cross-block consistency audit passed and is now retained as the executed contract.

## 18. Execution Outcome

Execution completed with typed verdict **`insufficient_capability`**. The first mandatory failure is frozen next-token capability: confirmation accuracy is 0.262/0.227/0.230 for D0/D1/D2, below the registered 0.70/0.55/0.40 thresholds, and all three Wilson lower bounds are below 0.25. Required-edge necessity passes, while the early cross-template reliability gate fails at both representation sites and the post node-position gate also fails.

The registered post diagnostic is $T_{rank}=0.00276$ with bootstrap interval $[-0.00269,0.01229]$, below paired condition-swap q95 0.00792. The pre diagnostic is $T_{rank}=0.02409$ with interval $[0.00189,0.02811]$, above q95 0.01393, but it is not interpretable after mandatory gate failures. The result record is [summary.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_04_E01_compositional_attention_write_atlas/summary.md); the complete setup, data example, gates, execution history, figures, and artifact map are in [detailed.md](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_04_E01_compositional_attention_write_atlas/detailed.md).

Formal ACP jobs were `om-pbybysxg` (extraction, succeeded), `om-bj8mm9ot` (all scientific arrays completed; final JSON serialization failed after one retry), and `om-v4omoym1` (deterministic finalization, succeeded). The serialization repair changed no scientific array, condition, metric, threshold, or random draw. Five central figures passed file and human visual audit.
