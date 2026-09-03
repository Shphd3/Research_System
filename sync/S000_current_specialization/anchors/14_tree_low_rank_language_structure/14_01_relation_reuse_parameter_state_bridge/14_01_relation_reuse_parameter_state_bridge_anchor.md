# A14_01 — Does Relation Reuse Convert QK Functional Compression into Task-Sufficient State Compression?


Line foundation: [A14_00 conditional low-rank hierarchy](../14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor.md).

## 1. Problem Definition

**Parent problem:** A14 asks when a globally high-capacity hierarchy can support conditionally low-dimensional computation without reopening the rejected global shared-linear claim.

**Decision question:** in the controlled ABCD next-token-prediction setting, does the high-reuse `share16` condition require a smaller held-out, task-preserving attention-update subspace than `random_unshared`, thereby supplying a state-side empirical bridge between QK functional compression and the local low-dimensional source premise of the probabilistic active-tree theorem?

| Term | Plain meaning | Concrete object / computation | Decision role | Cannot prove |
| --- | --- | --- | --- | --- |
| share regime | How broadly an A→C mapping is reused across B contexts | `share16`, `share4`, `share2`, `random_unshared` | Controlled composite condition | A pure frequency effect; the number of independent rules also changes |
| QK functional operator | The parameter object that determines attention scores | $B_{QK}=W_Q^\top W_K$ under the repository's orientation convention | Parameter-side compression diagnostic | Hidden-state compression by itself |
| task-relevant state | The state update directly used at the B-end position to predict the first C token | attention residual update $g_{i,t}$, with raw residual as a guard | State-side object | A semantic representation for all language |
| held-out functional state rank | The smallest train-fitted subspace retaining task loss on unseen B contexts | $k_H(s;\epsilon)$ | Primary state-compression quantity | Exact algebraic rank or nonlinear intrinsic dimension |
| bridge | Co-occurrence of nontrivial parameter compression and held-out task-sufficient state compression under the same controlled condition | joint parameter/state evidence with random-subspace and split guards | Connects the senior experiment to A14's local-state premise | The optimization mechanism or natural-language transfer |

This anchor deliberately does not call the share regime “frequency.” The current generator changes exact relation reuse, context reuse, independent rule count, and therefore function complexity together.

## 2. Physical Priors

1. **Reuse prior.** If one A→C function is reused across varied B contexts, a model may reuse fewer task-relevant directions than when each B requires a separate lookup rule.
2. **Parameter-to-state prior.** Functional concentration in the QK score operator matters to A14 only if it changes a state used for prediction; parameter spectra alone do not instantiate a low-dimensional active source.
3. **Task-sufficiency prior.** A low reconstruction error is not enough. The projected state must retain held-out C-token utility.
4. **Local-not-global prior.** A reusable local state can support one active-tree clause while the union of all rules, modes, and tasks remains high-dimensional.

These are empirical priors. The probabilistic active-tree theorem remains conditional and mathematically independent of this experiment.

## 3. Falsifiable Hypotheses

**Primary hypothesis.** At matched full-model fit, a subspace fitted on calibration B identities in `share16` retains held-out C-token loss at a lower normalized rank than in `random_unshared`, and the `share16` rank is nontrivial relative to the ambient width.

**Strongest rival.** The existing Q/K truncation result is entirely explained by fewer independent lookup tables or by a parameterization-specific spectrum. The prediction-relevant attention update remains equally high-dimensional, does not transfer to unseen B contexts, or loses task utility after projection.

**Pass:** all source and capability guards pass; the registered `random_unshared - share16` functional-state-rank contrast is positive with a paired hierarchical-bootstrap confidence interval above zero; `share16` meets the registered nontrivial rank budget; and an equal-rank random subspace does not preserve comparable utility.

**Fail:** guards pass, but the primary contrast is nonpositive, `share16` misses the nontrivial budget, or the learned low-dimensional projection fails held-out utility.

**Insufficient:** source checkpoints or generator semantics cannot be recovered; the original parameter-side effect does not reproduce; B-disjoint splits or intervention replay fail; or numerical/sample guards prevent stable rank selection.

## 4. Mathematical Model

Let $s$ denote a share regime and let $g_i^s\in\mathbb R^d$ be the attention residual update at the B-end position for example $i$. Split B identities into calibration and test sets. Fit the calibration mean $\mu_s$ and the ordered principal basis $U_{s,k}$ using calibration updates only. The rank-$k$ affine intervention on a test update is

$$
\Pi_{s,k}(g)
=
\mu_s+U_{s,k}U_{s,k}^{\top}(g-\mu_s).
$$

Let $L_s^{full}$ be held-out first-C-token cross entropy and $L_s^{(k)}$ the loss after replacing only the registered attention update by $\Pi_{s,k}(g)$. For a preregistered tolerance $\epsilon$, define

$$
k_H(s;\epsilon)
=
\min\left\{k:
L_s^{(k)}-L_s^{full}\le\epsilon
\right\}.
$$

The primary contrast is

$$
C_H
=
\frac{k_H(\texttt{random\_unshared};\epsilon)
-k_H(\texttt{share16};\epsilon)}{d}.
$$

The parameter-side diagnostic uses $B_{QK}=W_Q^\top W_K$ and defines $k_{QK}(s;\epsilon)$ analogously as the smallest truncated product rank retaining held-out C-token loss. It is secondary because A14's missing object is the task-relevant state, not the parameter matrix.

This model measures a linear functional rank at one intervention site. It is neither the strict rank of all hidden states nor a theorem about nonlinear intrinsic dimension.

## 5. Computational Realization

- Recover the exact ABCD generator, checkpoint fingerprints, matched-fit rule, and four share conditions from the researcher-provided NTP study. No evidential run begins until this provenance gate passes.
- Use the clean 64-dimensional, one-layer, one-head setting and all three registered seeds. `share16` and `random_unshared` are the primary contrast; `share4` and `share2` are secondary dose-response diagnostics.
- Keep A/B/C/D marginals, sample count, A→C distance, sequence length, model, optimizer, and matched-fit criterion fixed as in the source study.
- Split by B identity, not by example row. Fit the affine subspace on calibration B identities and evaluate interventions on unseen B identities.
- Use the B-end attention residual update as the primary state. Raw residual-stream state, centered energy rank, and relation-conditioned gradient alignment are diagnostics only.
- For every selected $k$, compare the PCA subspace with equal-rank Haar-random subspaces and a shuffled-state control.
- Recompute a QK product functional-rank curve, while reproducing the source $W_Q/W_K$ truncation curves as provenance diagnostics.
- Do not train a Router, an MoE, or a new natural-language model in this experiment.

## 6. Minimal Falsification Tests

| Test | Why it is needed | Registered reading |
| --- | --- | --- |
| Source replay | Ensures the inherited phenomenon is real on the recovered artifacts | failure makes the bridge test insufficient |
| Matched capability | Prevents rank from tracking undertraining | all primary runs must satisfy the source matched-fit rule |
| B-disjoint transfer | Distinguishes reusable state from in-sample PCA | basis fitted on calibration B, utility measured on unseen B |
| Functional projection | Distinguishes energy compression from useful compression | first-C-token loss after state intervention |
| Equal-rank random control | Prevents “any small subspace works” | learned subspace must outperform random subspaces |
| `share16` vs `random_unshared` | Decisive composite-condition contrast | primary metric $C_H$ |
| `share4/share2` | Checks whether intermediate conditions are orderly | diagnostic only; nonmonotonicity does not override the primary verdict |

The main falsifier is a passed source/capability/intervention audit followed by no positive held-out functional-state-rank advantage for `share16`.

## 7. Current Evidence

The source note reports 64-dimensional median matched-fit steps of
350/750/1100/1200 from `share16` to `random_unshared`, and much stronger Q/K
than V/O tail-truncation robustness for `share16`. The public source repository
does not contain the exact generator, training code, or checkpoints. Therefore
the registered provenance and source-replay gates cannot pass.

A fully documented independent reconstruction was completed under the frozen
E08 operational contract. All 12 condition-seed runs reached matched fit.
`share16` state functional ranks were 13/10/10; `random_unshared` ranks were
16/13/12. The normalized paired gaps were positive in 3/3 seeds, with a
5,000-replicate hierarchical-bootstrap 95% interval of [0.0260, 0.0521]. All
`share16` runs met the 16/64 budget, learned subspaces passed while equal-rank
random spaces failed, and split swapping did not reverse the contrast.

The bridge is quantitatively weak relative to the parameter effect. Mean
combined-QK functional rank was 29.7 for `share16` versus 50.7 for
`random_unshared`, while mean state rank was 11.0 versus 13.7. Across all 12
condition-seed points, their Spearman correlation was weak and nonsignificant
($\rho=0.247$, $p=0.438$). Intermediate state ranks were not monotonic:
`share4` was slightly below `share16`.

The reconstruction also failed to reproduce the source note's near-null V/O
localization. Consequently the **formal registered verdict is insufficient
evidence**, while the operational reconstruction provides conditional evidence
only for a small extreme composite-condition state-rank gap. Full results:
[E08 summary](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/A14_E08_relation_reuse_state_bridge/summary.md).

## 8. Claim Boundary And Next Decision

**Allowed from the independent reconstruction:** under this documented
implementation, the high-reuse/low-rule-count composite condition has a small,
consistent held-out attention-update functional-rank advantage and a much
larger combined-QK functional-rank advantage over `random_unshared`.

**Still not allowed:** exact source replication; relation frequency alone
causes low rank; the relation is monotonic; gradient alignment is the
mechanism; natural language is a tree; NTP generally creates low-rank
semantics; the complete hidden space is low-rank; or an MoE Router should route
by this geometry.

The source-replay contract remains unadjudicated because its artifacts are
missing. The reconstruction is now registered as a bounded standalone evidence
item, but it must not be silently promoted into a source replication or a pure
frequency result.

**Exactly one next decision:** this anchor hands off the orthogonal
exact-frequency, rule-reuse, and lookup-cardinality audit to
[A14_02](../14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md). Router
experiments remain outside this anchor.
