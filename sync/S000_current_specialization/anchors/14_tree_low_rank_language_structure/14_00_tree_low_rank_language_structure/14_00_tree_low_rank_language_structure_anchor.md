# A14_00 — When Does Hierarchical Language Composition Preserve a Shared Low-Rank State?

Thinking Card source:
[14_00_tree_low_rank_language_structure_thinking_card_cn.md](14_00_tree_low_rank_language_structure_thinking_card_cn.md)

## 1. Problem Definition

### Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Decision role | Cannot prove |
| --- | --- | --- | --- | --- |
| node state | one vector assigned to one tree node | $h_v\in\mathbb R^d$ | defines the object stacked across trees | that the model internally constructs the annotated tree |
| layer matrix | node states at one tree level or scale across complete-tree samples | $H_\ell\in\mathbb R^{n_\ell\times d}$ | rank is defined on this matrix, not one vector | cross-level subspace alignment |
| tail energy | energy outside the best rank-$k$ approximation | $\tau_k(H)=\sum_{i>k}\sigma_i^2/\sum_i\sigma_i^2$ | primary low-rank error | functional use of the top space |
| 95% energy rank | smallest rank retaining at least 95% energy | $r_{0.05}(H)=\min\{k:\tau_k(H)\le0.05\}$ | empirical rank budget | exact algebraic rank |
| composition innovation | parent component not explained by the shared child operator | $E_{\ell+1}=H_{\ell+1}-A_\ell H_\ell W_\ell^\top$ | tests the theorem premise | that every nonlinear feature is noise |
| tree-specific compression | lower held-out rank/error for true constituents than matched false-tree spans | true-minus-control held-out comparison | separates hierarchy from generic anisotropy | language-wide causality |

**Single decision question:** Do shared low-dimensional leaf states and stable
hierarchical composition provide a non-vacuous explanation of low-rank node
representations in synthetic trees, real constituency structure, and pretrained
language models?

The claim concerns matrices of corresponding node representations across many
trees. A single node or one root vector has rank one and is not the research
object.

## 2. Physical Priors

1. **Shared-state prior.** Reused local linguistic factors place leaf phrases
   near a common low-dimensional affine subspace across samples.
2. **Composition-preservation prior.** A parent mainly transforms and aggregates
   child state rather than creating a fresh independent coordinate system at
   every node.
3. **Learning-origin prior.** If hierarchy is responsible, tree-specific
   compression should emerge through training and weaken when the hierarchy is
   destroyed while token marginals and sequence lengths are held fixed.

These are empirical priors. Only the conditional propagation result below is a
theorem.

## 3. Falsifiable Hypotheses

**Primary hypothesis.** Given a shared rank-$k$ leaf approximation and bounded
composition innovation, every tree layer has best-rank-$k$ error bounded by a
recursive stability term. In real representations, true tree spans should have
lower held-out effective rank and lower shared-composition residual than
matched false-tree controls.

**Strongest rival.** Apparent low rank is caused by sample shape, span length,
pooling, global mean, token position, rogue dimensions, model architecture, or
probe capacity; annotated parent-child relations add no predictive value.

**Pass:** the numerical theorem audit has no bound violations; real leaf
subspaces generalize; true-tree compression and composition gaps are positive
under registered controls; and a hierarchy intervention changes learned rank.

**Fail:** implementation and capability guards pass but true-tree gaps are zero
or reversed and the hierarchy intervention has no registered effect.

**Insufficient:** any apparent rank is limited by $n<d$, disappears after the
registered centering/length controls, is already present at initialization, or
the learned model lacks a matched-capability comparison.

## 4. Mathematical Model

For tree layer $\ell$, assume

$$
H_{\ell+1}=A_\ell H_\ell W_\ell^\top+E_{\ell+1}.
$$

Let

$$
\Delta_k(H)=\min_{\operatorname{rank}(S)\le k}\|H-S\|_F
=\left(\sum_{i>k}\sigma_i(H)^2\right)^{1/2}.
$$

Assume $\Delta_k(H_0)\le\varepsilon_0$. Define

$$
g_\ell=\|A_\ell\|_2\|W_\ell\|_2,
\qquad
B_0=\varepsilon_0,
\qquad
B_{\ell+1}=g_\ell B_\ell+\|E_{\ell+1}\|_F.
$$

### Theorem: approximate low-rank propagation

For every layer $\ell$,

$$
\Delta_k(H_\ell)\le B_\ell.
$$

Consequently, if $B_\ell^2\le\eta\|H_\ell\|_F^2$, then
$r_\eta(H_\ell)\le k$.

### Proof

Choose $S_0$ with $\operatorname{rank}(S_0)\le k$ and
$H_0=S_0+R_0$, where $\|R_0\|_F=\Delta_k(H_0)$. Recursively define

$$
S_{\ell+1}=A_\ell S_\ell W_\ell^\top.
$$

Matrix multiplication cannot increase rank, so
$\operatorname{rank}(S_\ell)\le k$ for all $\ell$. With
$R_\ell=H_\ell-S_\ell$,

$$
R_{\ell+1}=A_\ell R_\ell W_\ell^\top+E_{\ell+1}.
$$

Frobenius/spectral norm submultiplicativity gives

$$
\|R_{\ell+1}\|_F
\le
\|A_\ell\|_2\|W_\ell\|_2\|R_\ell\|_F
+\|E_{\ell+1}\|_F
\le B_{\ell+1}.
$$

Induction yields $\|R_\ell\|_F\le B_\ell$. Since $S_\ell$ is an
admissible rank-$k$ approximation,
$\Delta_k(H_\ell)\le\|H_\ell-S_\ell\|_F=\|R_\ell\|_F\le B_\ell$.
Dividing the squared inequality by $\|H_\ell\|_F^2$ gives the energy-rank
corollary. $\square$

The expanded bound is

$$
B_L=
\left(\prod_{j=0}^{L-1}g_j\right)\varepsilon_0
+
\sum_{t=1}^{L}
\left(\prod_{j=t}^{L-1}g_j\right)\|E_t\|_F.
$$

The theorem is exact but may be empirically vacuous when
$B_\ell/\|H_\ell\|_F\ge1$.

## 5. Computational Realization

The evidence chain uses seven separate audits:

1. exact/noisy synthetic matrices verify the implementation and bound;
2. deterministic counterexamples remove shared operators, averaging, or bounded innovation;
3. gold constituency trees with full-dimensional PPMI word vectors test held-out leaf-subspace sharing without a Transformer;
4. pretrained decoder-only models assign each span a common-readout hidden state, then compare true constituents with length-matched non-constituents and true parent-child edges with permuted edges;
5. matched small-Transformer training on hierarchical versus leaf-shuffled corpora tests whether changing hierarchy changes learned rank;
6. a same-parent control keeps every token fixed and changes only the proposed child boundary;
7. a two-sided control gives each eligible parent equal-weight left and right boundary shifts.

For pretrained models, the primary node vector is the hidden state of one
common single-token readout appended after an independently encoded span. Mean
pooling is diagnostic only because averaging can mechanically alter variance
with span length.

All train/validation/test splits occur at whole-tree or whole-sentence level.
The rank budget is chosen on training leaves and frozen for higher layers and
held-out data.

## 6. Minimal Falsification Tests

| Order | One uncertainty | Primary falsifier | Allowed claim if passed |
| --- | --- | --- | --- |
| 1 | Does code instantiate the theorem? | any normalized bound violation above tolerance | implementation matches the conditional theorem |
| 2 | Do real leaves share a held-out subspace? | true leaves do not outperform same-length non-constituents | one theorem premise holds for the chosen representation |
| 3 | Is compression tree-specific in a pretrained model? | final-checkpoint gap is absent or already present at initialization | trained model geometry is tree-conditioned |
| 4 | Does a shared parent operator generalize? | true edges do not beat permuted edges | the chosen model approximately realizes the composition clause |
| 5 | Does hierarchy causally change learned rank? | hierarchy/shuffle rank contrast is absent at matched capability | controlled hierarchy affects learned representation rank |
| 6 | Does the annotated split matter at fixed content? | gold does not beat a same-parent alternative | split geometry adds information beyond lexical containment |
| 7 | Is any split effect direction-independent? | equal-weight left/right alternatives remove the effect | gold preference is not a boundary-direction artifact |

## 7. Current Evidence

An archived controlled one-layer Transformer study reported that distinct
incremental features occupied a shared high-gain subspace in $W_Q$, $W_K$,
and $W_{\mathrm{out}}$, with much weaker $W_V$ concentration. This is a
mechanism prior, not current natural-language evidence:
[archived controlled draft](/daily_research_reports/backup/0623/docs/research_draft_compositional_singular_concentration_with_loss_and_qk_descent_cn.md).

The registered evidence chain is now complete:

| Audit | Verdict | Direct evidence |
| --- | --- | --- |
| [E01 theorem/synthetic](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/A14_E01_theory_synthetic/summary.md) | pass | maximum normalized bound violation $2.92\times10^{-8}$; all 17 counterexamples reproduced |
| [E02 gold syntax + PPMI](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/archive/A14_E02_gold_syntax_ppmi/summary.md) | archived / insufficient | gold projection advantage 34.2%, but $r_{0.05}/d=32.1\%$ misses the 25% budget |
| [E03 pretrained decoders](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/archive/A14_E03_pretrained_tree_geometry/summary.md) | archived / insufficient | Qwen leaf/composition gaps are positive and training-enhanced, but bound ratio is 10.80; Pythia emergence does not replicate |
| [E04 causal intervention](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/archive/A14_E04_causal_hierarchy_training/summary.md) | archived / insufficient | all-pair descriptive tree effect $+0.180$, composition effect $-0.047$, latent-rank Spearman 0.949, and 0/48 non-vacuous bounds |
| [E05 same-parent split](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/archive/A14_E05_same_parent_split_stability/summary.md) | archived / insufficient | Qwen split advantage $-0.0415$; Pythia $+0.1486$ but reverses by boundary direction; minimum Qwen bound 1.3369 |
| [E06 two-sided split](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/boundary/A14_E06_two_sided_split_robustness/summary.md) | boundary evidence | equal-weight Qwen/Pythia effects $+0.0064/-0.0001$; zero prediction--stability compatible points |
| [E07 reachable-space accounting](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/A14_E07_reachable_space_accounting/summary.md) | pass | exact dimension accounting in all 950 registered records; all seven negative controls passed |
| [E08 parameter-to-state bridge](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/A14_E08_relation_reuse_state_bridge/summary.md) | insufficient / conditional reconstruction | source replay unavailable; independent reconstruction gives extreme state ranks 13/10/10 versus 16/13/12, but intermediate conditions are nonmonotonic and the QK gap is much larger than the state gap |
| [A14_02 ROOT-rank and bridge chain](../14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md) | mixed; finite bridge supported | E01/E02 did not establish shared-composition capability; E04 supported local H9 in 5/5; E06 refuted finite single-point linearization in 5/5 while the exact learned secant passed the eight-dimensional functional controls |

Across audits, true spans exhibit shared subspace geometry and controlled
hierarchical order can cause tree-aligned compression. E05 removed lexical
containment by fixing parent content; Qwen then had no registered gold-split
advantage and Pythia was boundary-direction-sensitive. E06 balanced both shift
directions within every parent and reduced both pretrained effects to
approximately zero. Large initialization effects persist, and every real or
trained stability bound remains vacuous.

## 8. Claim Boundary And Next Decision

The theorem proves a conditional matrix statement. It does not prove that
language is a tree, that leaves are naturally low rank, that Transformer
attention implements $A_\ell H_\ell W_\ell^\top$, or that a low-energy
subspace is behaviorally used. Treebank results remain annotation- and
representation-dependent; pretrained-model results remain model-dependent;
synthetic training remains a controlled causal example.

Current adjudication: the theorem is mathematically valid, and tree-aligned
subspace compression has an empirical bridge, but the global stable
shared-linear propagation mechanism is not supported. Content-fixed and
direction-balanced controls do not yield a model-general gold-split advantage,
and every trained/pretrained registered bound is vacuous. E08 adds only a toy
independent-reconstruction bridge between an extreme composite share condition
and task-state functional rank; it does not reopen the global claim or isolate
frequency.

The E08 independent reconstruction is retained as a bounded standalone
evidence item; the original source replay remains insufficient. In A14_02,
E01 showed that duplicate frequency did not produce new-context invariance and
that capability-passing lookup tasks used 10.2, 11.0, and 12.8 task-functional
ROOT directions as independent mapping cardinality increased from 1 to 4 to
16. E02 then failed the shared unseen-component recombination gate in 0/5
seeds, so shared composition itself remains unadjudicated. E04--E06 establish
the bridge boundary: a shared trained-point Jacobian image can be local and
low-dimensional, but one endpoint/reference Jacobian does not represent the
complete training displacement. The exact learned ROOT secant is nevertheless
effectively eight-dimensional and functionally sufficient in the controlled
model, so finite training uses the secant/path-integrated image.
[A14_03](../14_03_state_parameter_functional_rank_demand/14_03_state_parameter_functional_rank_demand_anchor.md)
is a blocked candidate follow-up: only if A14_02 establishes a stable,
task-sufficient state-rank contrast will it test whether that contrast
causally requires more functional directions in a preregistered parameter
operator.

**Exactly one next decision:** construct a composition-capable shared task
surface before revisiting whether reusable rules causally reduce functional
rank. The global shared-linear propagation claim remains closed, the finite
bridge remains the secant/path-integrated image, and a Router protocol remains
outside this decision.
