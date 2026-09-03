---
anchor_id: 15_02_04_compositional_attention_write_atlas
status: insufficient_capability
canonical_language: en
companion_language: zh
parent_anchor: 15_02_layerwise_representation_spectral_atlas
updated: 2026-08-07
---

# A15_02_04 Compositional Semantic Rank Redistribution in Isolated Attention Writes


## 1. Problem Definition

The single decision question is:

> In frozen Qwen3-8B, when surface form, facts, token length, evidence position, answer space, and sample count are matched, does increasing the required semantic composition depth from one edge to two and four edges produce a late-layer rightward redistribution of reliable between-class semantic covariance over each layer's own DCLM activation-covariance ranks, especially in the isolated post-`o_proj` attention write?

The **data spectrum** at layer $\ell$ and representation site $s$ is the eigendecomposition of activation covariance on an independent DCLM calibration set. It is not a parameter-matrix singular spectrum.

A **rightward redistribution** does not mean that the same eigenvector moves from one rank to another. Every layer has a different activation space and recomputed eigenbasis. It means that the semantic covariance places more of its normalized mass on larger within-layer rank percentiles, whose directions have lower background variance relative to other directions at that same site and layer.

Three distinct phenomena must not be conflated:

1. **Background-spectrum flattening:** the DCLM eigenvalue distribution becomes less head-concentrated with depth. This is a global geometry diagnostic.
2. **Semantic rank redistribution:** one fixed semantic variable places a larger fraction of its reliable between-class covariance at larger normalized ranks. This is the target phenomenon.
3. **Literal direction transport:** the same semantic subspace is aligned and followed through layer maps. This requires an explicit transport, Jacobian, CCA, or Procrustes model and is outside this Anchor.

Composition depth $g\in\{D0,D1,D2\}$ means that the queried answer requires one, two, or four atomic relation edges. Taxonomy depth, SAE feature hierarchy, MLP computation, full residual states, Router utility, and training benefit are outside scope.

## 2. Physical Priors

The candidate prior is that common syntax, topic, and broadly shared context vary across many natural tokens and therefore dominate high-background-variance directions, while a conjunction-specific semantic variable is active only under narrower conditions. If deeper attention writes preserve such conditional variables as distinct coordinates rather than amplifying them into common high-variance directions, greater composition depth may place relatively more semantic covariance at larger background-rank percentiles.

This prior is false for the current representation site if composition becomes more readable with depth but its normalized rank distribution does not move right, if an apparent shift is reproduced by query-binding reversal, or if it is explained by background-spectrum flattening alone.

## 3. Falsifiable Hypotheses

**Primary hypothesis — composition-specific rank redistribution.** After capability, reliability, and matched-scale gates pass, the late-minus-early increase in the $D2-D0$ semantic rank-centroid gap is positive at isolated post-`o_proj` attention writes. Pre-`o_proj` is a registered boundary-localization secondary site.

**Strongest rival.** Deeper layers improve total composition discriminability or amplify all spectral ranks without composition-specific rank redistribution. Apparent movement can also arise from different total between-class scales, background-spectrum flattening, prompt difficulty, lexical leakage, position, or unstable calibration eigenvectors.

**Pass.** At post-`o_proj`, the registered rank-shift statistic exceeds its paired within-world $D0/D2$ condition-swap q95, its paired-bootstrap 95% lower bound is positive, both DCLM calibration halves preserve its sign, and no capability, reliability, matching, or hook guard fails. Band destination is reported separately as head, middle, or tail; Pass does not require the absolute variance peak to leave the head.

**Fail.** All mandatory gates pass, but the registered post-`o_proj` rank-shift statistic does not exceed the null or is not stable across calibration halves. A positive depth-discriminability result with no rank shift is a typed `depth_pass_rank_shift_fail` outcome.

**Insufficient.** The frozen model does not solve the four-edge task, necessary-edge deletion and counterfactual checks fail, reliable between-class signal is at the noise floor, the design is not scale-matched, or either representation/covariance basis fails its validity checks.

## 4. Mathematical Model

Let $h_{\ell,s,g,y,w,t}\in\mathbb R^d$ be the activation at layer $\ell$, site $s\in\{\mathrm{pre},\mathrm{post}\}$, composition depth $g$, eight-way answer class $y$, latent world $w$, and template $t$. The balanced two-way additive nuisance residual is

$$
z_{\ell,s,g,y,w,t}
=h_{\ell,s,g,y,w,t}
-\bar h_{\ell,s,\cdot,\cdot,\cdot,t}
-\bar h_{\ell,s,\cdot,\cdot,w,\cdot}
+\bar h_{\ell,s,\cdot,\cdot,\cdot,\cdot}.
$$

This removes only additive template and world main effects. It is not a pure semantic state. Raw and centered analyses are both retained.

For each $g$ and answer $y$,

$$
\mu_{\ell,s,g,y}=\mathbb E_{w,t}[z_{\ell,s,g,y,w,t}],
$$

$$
B_{\ell,s,g}=\operatorname{Cov}_{y}(\mu_{\ell,s,g,y}),
\qquad
W_{\ell,s,g}=\mathbb E_y\operatorname{Cov}_{w,t}(z\mid g,y).
$$

The three scale-separated summaries are:

$$
V_{\ell,s,g}=\operatorname{tr}(B_{\ell,s,g})
\quad\text{(raw semantic scale, activation}^2\text{)},
$$

$$
D_{\ell,s,g}
=\frac{\operatorname{tr}(B_{\ell,s,g})}
{\operatorname{tr}(W_{\ell,s,g})+\epsilon}
\quad\text{(stable semantic discriminability)},
$$

$$
R_{\ell,s,g}
=\frac{\operatorname{tr}(B_{\ell,s,g})}
{\operatorname{tr}(\Sigma^{\mathrm{bg}}_{\ell,s})+\epsilon}
\quad\text{(semantic scale relative to background)}.
$$

The independent DCLM activation covariance is

$$
\Sigma^{\mathrm{bg}}_{\ell,s}
=U_{\ell,s}\Lambda_{\ell,s}U_{\ell,s}^{\top},
\qquad
\lambda_{\ell,s,1}\ge\cdots\ge\lambda_{\ell,s,d}.
$$

Let $r_i=(i-0.5)/d$ be normalized within-layer rank and

$$
b_{\ell,s,g,i}
=u_{\ell,s,i}^{\top}B_{\ell,s,g}u_{\ell,s,i}.
$$

The scale-free semantic rank distribution is

$$
\pi_{\ell,s,g,i}
=\frac{b_{\ell,s,g,i}}
{\sum_j b_{\ell,s,g,j}}.
$$

Because individual eigenvectors can rotate inside nearly degenerate covariance regions, the registered location statistic uses 16 equal-rank, 256-dimensional projectors $F_k$. With midpoint $m_k=(k-0.5)/16$,

$$
p_{\ell,s,g,k}=\sum_{i\in F_k}\pi_{\ell,s,g,i},
\qquad
\rho^{(16)}_{\ell,s,g}=\sum_{k=1}^{16}m_kp_{\ell,s,g,k}.
$$

The unbinned centroid $\sum_i r_i\pi_i$ is retained only as a sensitivity diagnostic.

The primary statistic is the difference in differences

$$
T_{\mathrm{rank},s}
=\operatorname{median}_{\ell\in L_{\mathrm{late}}}
[\rho^{(16)}_{\ell,s,D2}-\rho^{(16)}_{\ell,s,D0}]
-\operatorname{median}_{\ell\in L_{\mathrm{early}}}
[\rho^{(16)}_{\ell,s,D2}-\rho^{(16)}_{\ell,s,D0}],
$$

with $L_{\mathrm{early}}=\{1,\ldots,12\}$, $L_{\mathrm{late}}=\{25,\ldots,35\}$, and block 36 reported separately.

For interpretation, $d=4096$ is divided into 16 equal-rank 256-dimensional bands: F1=head, F2--F8=middle, and F9--F16=tail. Each band reports raw variance per direction, normalized semantic share, and within-band semantic-to-nuisance ratio:

$$
\bar b_{\ell,s,g,k}
=\frac{\operatorname{tr}(U_k^\top B_{\ell,s,g}U_k)}{256},
$$

$$
p_{\ell,s,g,k}
=\frac{\operatorname{tr}(U_k^\top B_{\ell,s,g}U_k)}
{\operatorname{tr}(B_{\ell,s,g})},
$$

$$
j_{\ell,s,g,k}
=\frac{\operatorname{tr}(U_k^\top B_{\ell,s,g}U_k)}
{\operatorname{tr}(U_k^\top W_{\ell,s,g}U_k)+\epsilon}.
$$

Different hierarchy levels may have very different $V$. Therefore $V$ and $D$ decide whether a signal is real, while $\pi$, $\rho^{(16)}$, and $p_k$ decide where that signal lies. A normalized location is not interpreted when reliable total signal is absent. Equal answer count, entropy, worlds, and templates prevent class-count scale from entering the comparison.

Background-spectrum flattening is reported only through normalized eigenvalue mass and effective rank; it cannot trigger the semantic rank-shift verdict.

## 5. Computational Realization

The model is frozen `/data/share/Qwen3-8B` with 36 decoder blocks and hidden size 4096. At the common `Answer:` readout token, the two registered tensors are:

1. full pre-`o_proj` attention output $a_\ell\in\mathbb R^{4096}$, formed by concatenating 32 attention-head outputs;
2. isolated post-`o_proj` attention write $y_\ell=\mathrm{o\_proj}_\ell(a_\ell)\in\mathbb R^{4096}$ before residual addition.

No residual, RMSNorm output, MLP state, SAE decomposition, parameter spectrum, Router, or model update enters this test. Pre- and post-`o_proj` use separate DCLM activation covariances at every layer. Their raw values and eigenvectors are not treated as one shared coordinate system.

Each latent spatial-relation world contains five random single-token entity aliases and the same four ordered relation facts forming a binary composition tree over the path $e_0\to e_1\to e_2\to e_3\to e_4$. The complete node set is:

- four $D0$ leaves: $(e_0,e_1)$, $(e_1,e_2)$, $(e_2,e_3)$, and $(e_3,e_4)$;
- two $D1$ internal nodes: $(e_0,e_2)$ and $(e_2,e_4)$;
- one $D2$ root: $(e_0,e_4)$, admitting $(r_1\oplus r_2)\oplus(r_3\oplus r_4)$.

The primary comparison selects exactly one $D0$ leaf and one $D1$ internal node per world using a frozen Latin schedule, plus the unique $D2$ root. This keeps 256 world-level observations at every depth and prevents composition depth from being confounded with a fixed left/right node position. All seven nodes are extracted as a registered secondary position audit.

All prompts contain the same four facts. Query syntax, answer position, eight compass answer classes, fact count, token count, and evidence-position schedule are matched. Fact phrases do not contain canonical answer tokens; the complete eight-word alphabet appears only in one identical, unmarked computation instruction shared by every condition and class. World and node-schedule selection rejects zero-displacement answers and is constrained so both the three-node primary subset and every one of the seven node positions have equal answer-class counts.

The approved realization uses 256 paired world families and four paraphrase templates. It contains 7,168 node-complete semantic prompts; the equal-sample primary subset contains 3,072 of them, with exactly 32 worlds in every primary $g\times y$ cell. The statistical unit is the world family, not the node, prompt, template, or token; the Protocol owns the additional pre-registered control count.

Independent DCLM calibration uses the audited 65,536-token manifest, split into two 32,768-token halves. Each layer and site receives its own centered covariance basis. Model capability uses next-token accuracy and correct-answer NLL; the static representation analysis uses no learned probe as primary evidence.

## 6. Minimal Falsification Tests

1. **Generator and matching gate:** every world's seven node prompts have identical facts, exact token length, answer position, answer-space entropy, and registered fact-order schedule; the three-node primary subset and each node position are class-balanced, aliases are single tokens, and no target-specific answer mark or class-correlated answer-token occurrence exists.
2. **Capability and necessity gate:** every depth passes the frozen accuracy/NLL threshold; deleting any required edge reduces correct-answer support, and changing one required edge changes the generated answer as specified.
3. **Representation gate:** all 36 pre/post hooks replay exactly; native `o_proj` output equals the hooked isolated post-write within numerical tolerance; no residual is included.
4. **Scale and reliability gate:** $V$, $R$, and $D$ are reported before normalized location. Template split-half class-mean cross-products and world bootstrap must show positive reliable total semantic signal before $\pi$ or $\rho^{(16)}$ is interpreted.
5. **Primary rank-shift test:** evaluate $T_{\mathrm{rank},\mathrm{post}}$ against paired within-world $D0/D2$ condition swaps, world-family bootstrap, held-out templates, and both calibration-half bases. Pre-`o_proj` is evaluated identically as a boundary-localization secondary result.
6. **Rival controls:** query-binding reversal preserves all facts and the query token inventory while changing the correct answer to its opposite; same-dimensional random subspaces test whether the registered covariance bands are special; background effective-rank changes are reported separately.
7. **Destination and scale audit:** report raw $\bar b_k$, normalized $p_k$, and $j_k$ together. A large-level/small-level difference in raw $V$ cannot by itself count as a rank shift, and a normalized shift at negligible $V$ is insufficient.
8. **Layer aggregation:** early and late blocks are frozen as above; block 36 is excluded from the primary difference and reported separately.

## 7. Current Evidence

[A15_02](../15_02_layerwise_representation_spectral_atlas_anchor.md) established that fine relative to coarse taxonomy semantics becomes more discriminable in late Qwen3-8B residual and full pre-`o_proj` attention states, while actual between-class variance remains head-dominant and fixed middle/tail specificity fails. That result concerns taxonomy granularity, not required composition depth.

[A15_02_03](15_02_03_architectural_head_channel_concentration_anchor.md) found sparse pre-`o_proj` architectural-head concentration but no fixed within-head covariance-band identity. This warns against assuming that a rank band is a semantic module.

The 2026-08-05 full-attention audit already validates the 4096-dimensional pre-`o_proj` hook, independent DCLM calibration, covariance reconstruction, and half-split workflow. It does not contain true 1/2/4-edge composition data or isolated post-`o_proj` semantic covariance.

The senior SAE result projects SAE decoder features onto dense-MLP parameter singular vectors and therefore does not answer this activation-covariance rank question.

The completed [A15_02_04_E01 experiment](/Projects/from-attention-to-search/main/experiments/A15/15_02_layerwise_representation_spectral_atlas/A15_02_04_E01_compositional_attention_write_atlas/summary.md) has typed verdict `insufficient_capability`. Confirmation accuracy is 0.262/0.227/0.230 for D0/D1/D2, below the registered 0.70/0.55/0.40 thresholds, and all three Wilson lower bounds are below 0.25. Required-edge counterfactual log-odds shifts are positive, so the model responds to necessary relations but does not execute the requested answer interface reliably enough for the representation claim.

At isolated post-`o_proj`, $T_{rank}=0.00276$ (11.3 equivalent ranks), bootstrap interval $[-0.00269,0.01229]$, below condition-swap q95 0.00792. The pre-`o_proj` diagnostic is positive, $T_{rank}=0.02409$ (98.7 ranks), interval $[0.00189,0.02811]$, above q95 0.01393, but both sites fail the registered early cross-template semantic-reliability gate; post also fails node-position robustness. Composition-relative discriminability decreases from early to late at both sites: post $T_D=-0.547$ and pre $T_D=-0.686$, with both intervals entirely negative.

This evidence does not establish composition-specific rightward rank redistribution. It also cannot assign a valid scientific Fail to the general hypothesis because mandatory capability and reliability prerequisites fail.

## 8. Claim Boundary And Next Decision

This Anchor can establish only whether a frozen Qwen3-8B attention representation, under one controlled spatial-relation generator and one independent DCLM calibration distribution, shows composition-specific redistribution over local activation-covariance rank percentiles. E01 does not reach the prerequisites for that adjudication. The absent post diagnostic and negative $T_D$ describe this task/model interface only; they do not refute a general theory of deeper compositional representation.

It cannot establish literal transport of one direction across layers, that attention causally performs the composition, that `o_proj` creates information, that middle or tail ranks have universal semantic identity, that an SAE feature is a composition node, or that any rank partition improves Router or expert utility. A negative attention result cannot rule out composition in MLP or another representation boundary.

**Exactly one next decision:** decide whether to run a spectrum-sealed capability-interface repair that freezes the worlds, hierarchy, balancing, pre/post sites, covariance bases, metrics, and thresholds while changing only the prompt interface or model scale. A candidate becomes eligible for a new spectral confirmation only if held-out D0/D1/D2 accuracy reaches 0.70/0.55/0.40, every Wilson lower bound exceeds 0.25, and early D0/D2 cross-template covariance lower bounds are positive. No candidate spectral result may be inspected during interface selection.
