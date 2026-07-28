# Protocol: A14_E01 Theory, Stability, and Counterexample Audit

## 0. Approval Snapshot

Approval status: **approved for direct implementation and execution** by the
researcher on 2026-07-18.

Purpose: verify that the implementation exactly instantiates the low-rank
propagation theorem, quantify noisy stability, and reproduce counterexamples
showing why its assumptions cannot be removed.

Primary anchor:
[A14 tree low-rank language structure](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor.md)

Anchor decision question: can shared low-rank leaves and stable hierarchical
composition give a non-vacuous account of low-rank propagation?

Experiment role: metric and implementation audit.

Primary metric: maximum normalized theorem-bound violation

$$
V_{\max}=max_{c,s,\ell}
\frac{\Delta_k(H_\ell)-B_\ell}{\max(\|H_\ell\|_F,10^{-12})}.
$$

Pass: $V_{\max}\le10^{-5}$ and exact conditions have relative
$\Delta_k\le10^{-6}$ at every layer.

Fail: either numerical contract is violated after double-precision replay.

Insufficient: a failed case is caused by non-finite inputs, an incomplete run,
or a metric implementation that fails unit tests.

Cannot claim: that real language or a pretrained Transformer satisfies the
theorem premises.

Approval decision: execute E01 without another review pause; do not change its
scientific grid after reading results.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| best rank-$k$ error | distance to the nearest rank-$k$ matrix | $\Delta_k(H)$ from singular values | Frobenius norm | theorem left side | semantic low dimensionality |
| propagation bound | recursive upper bound on that error | $B_{\ell+1}=g_\ell B_\ell+\|E_{\ell+1}\|_F$ | Frobenius norm | theorem right side | tightness |
| gain | worst-case amplification of the inherited residual | $g_\ell=\|A_\ell\|_2\|W_\ell\|_2$ | dimensionless | separates contraction and expansion | actual average-case amplification |
| innovation | new matrix component added at a tree layer | $E_{\ell+1}$ | same unit as $H$ | tests approximate rather than exact rank | linguistic novelty |

## 2. Anchor Alignment

Physical prior tested: a shared operator cannot increase the algebraic rank of
the propagated signal; only inherited residual amplification and innovation
contribute to the approximation error.

Core model term tested: $A_\ell H_\ell W_\ell^\top+E_{\ell+1}$.

Falsifier: any valid finite matrix case with $\Delta_k(H_\ell)>B_\ell$ beyond
the registered tolerance.

Claim boundary: this is a theorem/implementation audit only.

## 3. Tested Hypotheses

1. Exact rank-$k$ leaves and zero innovation remain rank at most $k$.
2. Every noisy condition satisfies $\Delta_k(H_\ell)\le B_\ell$.
3. Removing shared-space or bounded-innovation assumptions can increase rank
   to the ambient/sample limit.
4. For the registered additive-noise construction, larger gain produces a
   larger absolute propagated residual at the root, all else equal.

## 4. Rival Explanations

- a row/column orientation error makes the bound appear correct accidentally;
- low rank comes only from $n<d$;
- the metric truncates small singular values incorrectly;
- the generated innovation lies inside the original low-rank space;
- the theoretical bound is confused with a claim that it must be tight.

## 5. Data / Model / Algorithm

Balanced binary forests use $d=128$, $k=8$, depth $L=6$, and 512 root trees.
There are therefore 32,768 leaves, so $n_0\gg d$.

Leaf signal:

$$
H_0=ZU^\top+\sigma N(I-UU^\top),
$$

where $U^\top U=I$ and all random matrices are standard Gaussian before
projection/scaling.

Each parent averages two disjoint children. Hence
$\|A_\ell\|_2=1/\sqrt2$. Set $W_\ell=cQ_\ell$ with orthogonal $Q_\ell$ and
$c=g\sqrt2$ to realize the target gain $g$.

Innovations are independently generated outside the propagated signal's
rank-$k$ basis when possible, then scaled to the registered relative norm.
The bound always uses the measured, not nominal, innovation norm.

## 6. Conditions, Seeds, and Outputs

### Exact audit

- $\sigma=0$, innovation $=0$;
- $g\in\{0.5,1.0,1.5\}$;
- seeds 0--2.

### Noisy audit

- $\sigma\in\{0,0.01,0.03,0.1\}$;
- innovation ratio $\delta\in\{0,0.01,0.05,0.1\}$;
- $g\in\{0.5,0.9,1.0,1.1,1.5\}$;
- seeds 0--9.

### Counterexamples

1. shared versus node-specific transforms mapping one common direction to
   distinct basis directions;
2. average versus sum aggregation, evaluated through operator norm and
   absolute bound rather than an unjustified relative-tail monotonicity claim;
3. orthogonal new-direction injection across layers;
4. DAG-style child reuse with reuse count $q\in\{1,2,4,8\}$.

Outputs: `metrics.parquet`, `summary.json`, a bound-versus-actual trajectory
figure, a root tail-energy heatmap, and counterexample tables.

## 7. Primary Metric

$V_{\max}$ is decisive because the theorem is universal over the registered
finite matrices. A false positive would certify an incorrect implementation;
a false negative would stop the empirical chain unnecessarily. Double
precision and an absolute-plus-relative tolerance protect both costs.

## 8. Secondary Metrics

- $\tau_k(H_\ell)$ and $r_{0.05}(H_\ell)$;
- bound ratio $B_\ell/\|H_\ell\|_F$;
- tightness $\Delta_k/B_\ell$ when $B_\ell>0$;
- root residual by gain/noise/innovation;
- realized algebraic/numerical rank in counterexamples.

## 9. Known Good / Bad / Confusing Cases

- Known good: exact zero-noise shared-operator condition.
- Known bad: deterministic node-specific map from $e_1$ to distinct $e_i$.
- Known confusing: a loose but valid bound; looseness is not failure.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Evidence | Rule | Debug artifact |
| --- | --- | --- | --- | --- |
| metrics | are SVD metrics correct? | unit matrices with analytic spectra | exact tolerance | pytest output |
| tree operator | is averaging oriented correctly? | explicit $A$ and implicit pair-average agreement | max error $<10^{-12}$ | operator JSON |
| exact propagation | is rank preserved? | layer table | relative tail $\le10^{-6}$ | exact table |
| noisy propagation | does the bound hold? | all condition/seed/layer rows | $V_{\max}\le10^{-5}$ | violation table |
| counterexamples | do removed assumptions fail as predicted? | rank/operator table | deterministic expected rank/norm | counterexample CSV |

## 11. Algorithm Specification

Input: YAML configuration and seeds.

Parameters: $d,k,L,N_{root},g,\sigma,\delta$.

Steps: generate orthogonal basis and leaves; compute exact $\Delta_k(H_0)$;
propagate by disjoint pair aggregation and shared transforms; generate measured
innovations; update $B$; compute spectra; write row-level records; run
counterexamples; render registered plots.

Pass conditions: all tests and primary numerical criteria pass.

Failure reasons: invalid orientation, inaccurate SVD, non-finite matrices,
bound recurrence mismatch, or deterministic counterexample mismatch.

## 12. Success / Failure / Insufficient Evidence

Success validates only the mathematical/computational bridge. Failure blocks
all later empirical interpretation until localized. Insufficient runs may be
replayed without changing the scientific grid.

## 13. What This Cannot Claim

No natural-language, pretrained-model, causal-language, semantic, or
Transformer-mechanism conclusion follows from E01.

## 14. Review Notes and Protocol Changes

The referenced conversation proposed that summation should necessarily have
higher relative tail energy than averaging. That statement is not implied by
the theorem because a common scalar can also amplify signal energy. E01 tests
the valid consequence: the aggregation operator norm and absolute error bound
increase under summation.
