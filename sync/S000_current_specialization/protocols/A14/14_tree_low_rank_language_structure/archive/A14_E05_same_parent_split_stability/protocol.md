# Protocol: A14_E05 Same-Parent Split Specificity and Stability Frontier

## 0. Approval Snapshot

Approval status: **approved for direct implementation and execution** by the
researcher's explicit 2026-07-18 instruction to unpack the supplied theory
package and run the aligned experiments without another approval round.

Purpose: decide whether a low-dimensional ordered child-to-parent operator is
specific to the gold binary split when the parent text and token multiset are
held exactly fixed, and whether any such predictor has a non-vacuous stability
certificate.

Primary anchor:
[A14 tree low-rank language structure](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor.md)

Anchor decision question: does a stable shared composition law explain the
observed tree-aligned subspace geometry?

Anchor physical prior tested: parents mainly combine a shared low-dimensional
child state rather than exploiting lexical containment alone.

Anchor core model term tested: ordered low-dimensional affine recursion

$$
z_p=B_Lz_L+B_Rz_R+b+\xi_p.
$$

Anchor falsifier: a same-parent, same-token alternative split is predicted as
well as the annotated split, or every structure-specific predictor remains
unstable or vacuous.

Experiment role: operationalization and root-cause audit of the confounded E03
composition control.

Primary metric: held-out gold-versus-alternative split error advantage for
separately trained, validation-selected ordered operators.

Claim boundary: a pass can support a treebank- and representation-specific
low-dimensional composition surrogate. It cannot show that a Transformer
causally computes the annotated tree or that language is globally low-rank.

Minimal setup: naturally binary Penn Treebank parents; identical parent text;
one alternative internal boundary; independently encoded parent and child
spans; final-layer EOS readout; leaf-only rank selection; ordered ridge maps.

Basic configuration: Qwen2.5-0.5B pretrained and identical random
initialization as primary; Pythia-410m as directional replication; file-level
train/validation/test split; seed 1405; 1,000 sentence-cluster bootstrap
replicates.

Conditions to run: gold split, same-parent alternative split, ordered map, and
commutative mean-child map across the registered ridge penalties.

Pass: Qwen pretrained has at least 5% gold-split advantage with a positive
bootstrap lower bound, at least 5 points more advantage than initialization,
normalized gold prediction error below 0.90, and at least one validation-
eligible ordered point with generic bound ratio below 1.

Fail: Qwen pretrained prediction capability is present but the gold split is
non-positive relative to the alternative split with a non-positive confidence
upper bound.

Insufficient: positive split geometry without a non-vacuous generic bound;
the same advantage is already present at initialization; Qwen/Pythia disagree;
or sample/optimization guards fail.

Cannot claim: an internal parse algorithm, semantic sufficiency, behavioral
use, cross-language universality, MoE value, or a nonlinear composition law.

Approval decision: execute the frozen protocol directly.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Gold split | Annotated direct left/right children | Natural binary Penn Treebank node | boundary index | Candidate linguistic structure | That the annotation is uniquely correct |
| Alternative split | Different boundary inside the same parent | Same words and order; closest tokenizer-length profile among non-gold cuts | boundary index | Removes the E03 content-change shortcut | That every alternative is linguistically impossible |
| Leaf basis | Shared low-dimensional directions learned only from train leaves | Orthogonal basis $U$ retaining 95% train-leaf energy | $k/d$ | Freezes the low-rank premise before parent fitting | Behavioral relevance |
| Ordered operator | Different maps for left and right children | $z_p=B_Lz_L+B_Rz_R+b$ | normalized squared residual | Tests order-sensitive shared composition | Causal internal computation |
| Mean operator | Child-order-insensitive control | $z_p=B(z_L+z_R)/2+b$ | normalized squared residual | Tests whether separate child roles add value | General permutation invariance |
| Split advantage | Relative reduction in parent error under gold splits | $(CE_{alt}-CE_{gold})/CE_{alt}$ | fraction | Primary structure-specificity metric | Stability or causality |
| Operator norm | Largest amplification of a joint latent perturbation | $\rho=\|[B_L;B_R]\|_2$ under row-vector convention | dimensionless after common orthogonal coordinates | Stability axis of the Pareto frontier | Actual average amplification |
| Generic bound ratio | Original worst-case theorem diagnostic | $(\rho\Delta_k(H_c)+\|E\|_F)/\|H_p-\mu_p\|_F$ | ratio | Decides whether the original norm proof is non-vacuous | Tightness |
| Invariant certificate | Error witness for the forced-output leaf space | $\|E\|_F/\|H_p-\mu_p\|_F$ | ratio | Separates useful bottleneck from the generic norm bound | Unconstrained propagation |

## 2. Anchor Alignment

Decision question: can the current stable shared-linear mechanism survive a
content-fixed tree-structure control?

Physical prior tested: a correct child boundary exposes a reusable composition
law that a nearby wrong boundary does not.

Core model term tested: shared ordered low-dimensional child maps and the
innovation residual.

Falsifier: no held-out gold advantage or no non-vacuous stable point.

Claim boundary: observational treebank/model geometry only.

## 3. Tested Hypotheses

### H1: strict shared-space approximation

Let $U\in\mathbb R^{d\times k}$ be selected from training leaves only and
$z=U^\top(h-\mu_{leaf})$. A shared ordered operator should predict independently
encoded parents with normalized test error below 0.90.

### H2: split specificity

An ordered operator fitted and selected on gold splits should achieve lower
held-out error than an otherwise identical operator fitted and selected on
same-parent alternative splits. The registered effect threshold is 5% and the
sentence-bootstrap lower bound must exceed zero.

### H3: role specificity

The ordered operator should improve on the commutative mean-child operator by
at least 5% on gold splits. This is secondary because failure may reflect probe
power rather than absence of linguistic roles.

### H4: prediction--stability compatibility

At least one validation-eligible gold ordered operator should simultaneously
retain H2's 5% split advantage and have generic bound ratio below 1. Otherwise
the original stable-propagation mechanism remains unsupported even if H1--H3
show descriptive geometry.

A ridge penalty is **validation-eligible** exactly when its gold ordered
validation error is no more than $1.05$ times the minimum gold ordered
validation error over the registered grid. This tolerance is fixed before any
test result is inspected.

The smoke run selected the original upper endpoint $10^2$, so before the full
run the registered grid was expanded once to
$\{10^{-6},\ldots,10^2,10^3,10^4,10^5\}$. A full-run gold or alternative
selection at either endpoint fails the ridge-interior validity guard and makes
H2 insufficient rather than permitting another grid change.

### H5: learning increment

Qwen pretrained split advantage should exceed its identical random
initialization advantage by at least 0.05. Pythia reports directional
replication and limits generality but does not override the primary verdict.

## 4. Rival Explanations

1. Lexical containment: removed because parent text and every token are fixed.
2. Child-length profile: the alternative boundary minimizes the pairwise
   tokenizer-length deviation from the gold children.
3. Probe capacity: gold and alternative conditions use identical model class,
   rank, data counts, penalty grid, and split.
4. Architecture prior: identical random initialization receives the same
   inputs and analysis.
5. Order irrelevance: tested by the mean-child control.
6. Leaf-space overfitting: $U$ and $k$ use training coarse leaves only.
7. Ridge selection leakage: penalty selection uses validation data only.

## 5. Data / Model / Algorithm / Objective

Use the same Penn Treebank file split, token normalization, independent-span
EOS representation, frozen model revisions, dtype, and model roles as E03.
Retain naturally binary annotated parents of 3--16 words. The gold boundary is
the direct-child boundary. The alternative is the non-gold internal word
boundary minimizing

$$
|m_L^{alt}-m_L^{gold}|+|m_R^{alt}-m_R^{gold}|,
$$

where $m$ is tokenizer subtoken length; break ties by word-boundary distance
and then boundary index. No parent or token changes.

Use at most 8,192 training coarse leaves and 4,096/1,024/1,024
train/validation/test parent records, sampled by whole sentence. In smoke mode
use 256 leaves and 128/64/64 parents on Qwen only with 100 bootstraps.

For each checkpoint, select $k=r_{0.05}$ from centered training leaves and
freeze $U$. Project left and right states into $U$, concatenate them for the
ordered model, and fit the parent coordinates in $U$ by ridge regression. Add
the unrestricted training parent mean after prediction; all centered variation
must pass through $U$.

Fit gold and alternative operators separately. Select their penalties by their
own validation error. Evaluate both on the same test parents. Also evaluate the
gold-fitted operator on alternative children as a transfer diagnostic.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gold ordered | Shared ordered recursion | $B_L,B_R$ | Primary model | Primary | $CE<0.90$ | $CE\ge1$ | 0.90--1.00 without clear control gap | frontier/table |
| Alternative ordered | Tree specificity | Same parent/tokens | Removes lexical shortcut | Primary control | Gold advantage $\ge0.05$ | Advantage $\le0$ | Positive but below threshold | frontier/table |
| Gold mean | Role sensitivity | $B_L=B_R$ after averaging | Detects order value | Secondary | Ordered advantage $\ge0.05$ | Non-positive | Small positive | table |
| Initialization | Learning origin | Architecture prior | Separates learned geometry | Guard | Increment $\ge0.05$ | Pretrained no better | Mixed | table |
| Pythia | Model dependence | Replication | Limits generality | Secondary | Same direction | Opposite | Small/mixed | table |
| Ridge grid | Stability | Prediction versus norm | Finds Pareto frontier | Primary | Eligible point with bound $<1$ | None and split effect absent | Split effect but bound vacuous | central figure |

Seed: 1405. Model checkpoints are deterministic conditional on their frozen
weights; bootstrap uncertainty is clustered by sentence.

## 7. Primary Metric

For separately fitted gold and alternative ordered maps,

$$
CE_c=\frac{\|Y-\widehat Y_c\|_F^2}{\|Y-\mu_Y\|_F^2},
\qquad
Adv_{split}=\frac{CE_{alt}-CE_{gold}}{CE_{alt}}.
$$

The primary Qwen estimate uses the validation-selected penalty in each
condition and a 1,000-replicate sentence-cluster paired bootstrap. A false
positive would preserve the confounded linear mechanism; therefore same-token
control and positive confidence lower bound are mandatory.

## 8. Secondary Metrics

- ordered-versus-mean advantage;
- gold-fit transfer error on alternative children;
- parent projection error outside frozen leaf $U$;
- operator norm and effective binary perturbation factor $\sqrt2\rho$;
- generic theorem bound ratio;
- invariant certificate ratio and whether it reaches $\sqrt{0.05}$;
- pretrained-minus-initialization increments;
- Pythia directional replication.

## 9. Known Good / Known Bad / Known Confusing Cases

- Known good: a synthetic generator using one ordered low-dimensional map must
  prefer its registered split and recover a non-vacuous point.
- Known bad: parent-independent shuffled targets must not show split advantage.
- Known confusing: a high-capacity operator can predict lexical containment;
  same-token alternative fitting and random initialization protect against it.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Unit | Is alternative splitting content-preserving? | toy trees | exact parent text/token equality | pytest | smoke |
| Synthetic | Can the metric recover a known ordered law? | constructed latent records | positive split advantage, bound below 1 | JSON/CSV | smoke |
| Smoke | Does the full Qwen path complete? | reduced PTB | all expected artifacts, finite metrics | manifest/frontier | full |
| Full | Does pretrained geometry pass the frozen rule? | full Qwen/Pythia | Section 12 | summary/figure | anchor update |

## 11. Algorithm Specification

Input: leaf texts; parent/gold/alternative child texts; frozen decoder states.

Parameters: leaf rank $k$; ridge penalty $\lambda$; ordered or mean design.

Steps: fit leaf basis on train; encode child coordinates; fit every penalty on
train; read validation error and norms; select penalty; evaluate paired test
parents; bootstrap by sentence; construct Pareto frontier.

Outputs: condition metrics, per-parent residual records, full penalty frontier,
run manifest, one central figure, and protocol compliance record.

Pass conditions: exact same-parent/same-token guard, file separation, finite
metrics, and primary rules above.

Failure reasons: missing alternative boundary, model/data unavailability,
singular fit, sample leakage, or non-finite spectrum.

## 12. Success / Failure / Insufficient Evidence

Support requires all primary Qwen clauses in the Approval Snapshot. Failure
requires valid parent prediction but a confidently non-positive gold split
effect. All mixed outcomes, especially positive split geometry with a vacuous
generic bound, are insufficient for the stable propagation mechanism and may
still support a weaker tree-conditioned subspace description.

## 13. What This Cannot Claim

This experiment cannot identify a causal internal computation, validate a
particular semantic theory, prove a unique parse, establish behavioral use of
the low-dimensional coordinates, or support MoE/diffusion/world-knowledge
extensions.

## 14. Review Notes And Protocol Changes

No post-result changes are allowed. The protocol replaces E03's cross-parent
permutation with a same-parent boundary intervention and replaces mean-child
full-space regression with the ordered leaf-space model discussed on
2026-07-18. The researcher explicitly waived another approval round.
