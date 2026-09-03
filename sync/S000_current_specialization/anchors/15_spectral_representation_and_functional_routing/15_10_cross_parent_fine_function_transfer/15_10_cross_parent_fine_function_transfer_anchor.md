# A15_10: Cross-Parent Fine-Function Transfer


## 1. Problem Definition

The decision question is whether a stable seven-dimensional fine-class Fisher
space learned inside mathematics can carry held-out physics fine-class function
after a physics-specific linear head is retrained, and vice versa, across the
six fixed Qwen3-30B-A3B blocks and the independent C4/C5 panels.

“Transfer” means that only the input subspace comes from the source parent;
the target head, target labels, target training rows, and target held-out rows
remain target-specific. It is not label transfer, native Router use, causal
necessity, or language-model utility. This is the smallest successor to
A15_09 because that audit established low coarse--fine geometry but could not
distinguish functionally interchangeable fine spaces from parent-local ones.

## 2. Physical Priors

The sole prior is: if two parent-conditional fine functions use a transferable
linear input space at a fixed layer, then replacing the target's own stable
fine space with the source parent's stable fine space should retain target
held-out discrimination beyond a source-estimator-matched label-permutation
pipeline. The prior is false at a layer when the target-own space is valid but
the source space provides no reproducible target gain beyond that null.

## 3. Falsifiable Hypotheses

The primary hypothesis is that mathematics and physics contain cross-parent
transferable fine function at one or more registered layers: both directions
retain target fine discrimination beyond their complete-pipeline source-label
permutation null and reproduce from C4 to C5. The strongest rival is that fine
function is parent-local: each target-own space works, while the other parent's
space does not provide reproducible excess target function.

Evidence that fails to establish transfer does not by itself prove strict
parent specificity. Directional asymmetry, C4/C5 disagreement, or an invalid
target-own space is insufficient rather than evidence for either global
architecture.

## 4. Mathematical Model

For panel $p$, layer $\ell$, split $a\in\{A,B\}$, and parent
$c\in\{m,p\}$, let $S_{c,p,\ell}^{a}\in\mathbb{R}^{2048\times7}$ be the
Euclidean-orthonormal fine-class Fisher basis. Both parents at the same
$(p,\ell,a)$ use exactly one pooled within-leaf Ledoit--Wolf metric
$\widehat W_{p,\ell}^{a}$ fitted from all 64 leaf classes in that split.

Let $L_t(S)$ be target $t$'s cross-fitted held-out negative log likelihood
after projecting target states into $S$ and fitting a target-label logistic
head using training data only. Let $L_{s\rightarrow t}^{null}$ be the median
held-out loss over complete source-label-permutation pipelines. The primary
continuous effect is the relative retention quantity

$$
RR_{s\rightarrow t}=
\frac{L_{s\rightarrow t}^{null}-L_t(S_s)}
{L_{s\rightarrow t}^{null}-L_t(S_t)}.
$$

$RR=0$ places Cross at its matched null and $RR=1$ places it at Own. The value
is empirical, may leave $[0,1]$, and is never clipped. A horizontal reference
at $0.9$ may aid reading but is not a scientific threshold or verdict gate.

## 5. Computational Realization

The experiment reuses frozen native MoE-input activations from Qwen3-30B-A3B
at Blocks 4/12/20/28/36/44. C4 is primary and C5 is independent replication;
each panel contains 8 parents by 8 children by 30 complete template families.
Only mathematics and physics are targets.

For fold A-to-B, a source or target fine space is estimated from split A,
the target head is trained on target-A projected states, and it is evaluated on
target-B. Fold B-to-A reverses every role. Own and Cross use the same target
rows, true target labels, seven-dimensional input, head family, train-only
regularization-selection rule, and held-out scoring; only the parent that
supplies the Fisher space changes. Every permutation rebuilds the source space,
target projection, target-head fit, and held-out evaluation. Whole template
families are the independence unit for both randomization and bootstrap.

## 6. Minimal Falsification Tests

The decisive comparison is Cross versus its complete-pipeline source-label
permutation null, conditioned on the target-own space passing rank, split-half
stability, and held-out function admission. Own, Cross, a rank-seven common
coarse-space control, and matched permutation spaces differ only in the
registered projection-space source; every target-head operation is otherwise
matched.

The primary output is the full layerwise matrix of $RR_{m\rightarrow p}$ and
$RR_{p\rightarrow m}$ with template-family uncertainty, reported separately
for C4 and C5. A layer supports transferable function only under the
Protocol's pre-registered null-excess and replication rule; $0.9$ never enters
that rule. A valid Own with no replicated Cross excess means transfer is not
established, not that strict parent specificity has been proved. Invalid Own,
undefined RR denominator, numerical failure, or panel disagreement is
Insufficient.

## 7. Current Evidence

A15_09_E01 found that all 24 registered coarse/fine spaces were rank-seven and
A/B stable, while raw coarse--fine overlap was 0.00649--0.03858 and below its
matched permutation median in every cell. The empirical corrected overlap was
0.05964--0.14452, and no universal depth law reproduced across both parents.
This disfavors dominant reuse of the common coarse discriminant but does not by
itself measure mathematics--physics fine-function transfer.

A15_10_E01 is now complete. The immutable run contains all 24 registered
panel--layer--direction cells; 18 pass all admissions and six are retained as
Insufficient. Eligible RR values are 0.0339--0.1810 with median 0.0743. Only
one directional cell, C5 Block 36 mathematics to physics, beats its registered
complete-pipeline Cross-null 2.5th percentile; it does not reproduce in C4 and
the reverse C5 cell is ineligible. Consequently 0/6 layers satisfies the
registered bidirectional C4/C5 transfer rule. The result is recorded in the
[Summary](/Projects/from-attention-to-search/main/experiments/A15/15_10_cross_parent_fine_function_transfer/A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer/summary.md)
and [Detailed record](/Projects/from-attention-to-search/main/experiments/A15/15_10_cross_parent_fine_function_transfer/A15_10_E01_qwen3_30b_cross_parent_fine_function_transfer/detailed.md).

These are direct results. The bounded knowledge wording remains an AI draft
until the researcher confirms or corrects the active Focus result account.

## 8. Claim Boundary And Next Decision

This anchor may establish a bounded, layerwise linear transfer profile between
mathematics and physics on two controlled natural-language expression panels.
It cannot establish native Gate use, expert utility, causal necessity,
language-model loss improvement, a universal taxonomy law, or the value of a
shared or parent-local Router architecture.

The executed evidence does not admit a shared-fine premise: no layer meets the
registered transfer rule. It also does not prove strict parent locality,
because coarse and permutation-derived seven-dimensional controls retain high
fine-label readability.

The proposed next decision, awaiting the researcher's confirmation, is whether
to test a correct-parent-conditioned local fine Router against one global
shared fine Router under matched data, capacity, optimization, supervision,
and compute. The completion criterion would require both held-out routing
quality and language-model NLL, with parent conditioning as the only structural
difference. The resume action is human result/boundary confirmation followed
by a new Focus and Protocol; this anchor does not authorize Router training.
