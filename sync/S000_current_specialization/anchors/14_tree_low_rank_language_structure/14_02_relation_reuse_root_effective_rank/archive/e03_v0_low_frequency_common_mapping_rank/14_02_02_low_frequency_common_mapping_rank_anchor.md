---
anchor_id: 14_02_02_low_frequency_common_mapping_rank
status: parked_stopped
canonical_language: en
companion_cn: 14_02_02_low_frequency_common_mapping_rank_anchor_cn.md
parent_anchor: 14_02_relation_reuse_root_effective_rank
thinking_card: /Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_thinking_card_cn.md
experiment_id: A14_02_E03_low_frequency_common_mapping_rank
protocol_status: not_retained_stopped
---

# A14_02_02 Low-Frequency Calls To A Learned Common Mapping

Parent anchor:
[A14_02 shared compositional rules and task-functional root-state rank](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md)

Thinking Card:
[14_02 relation-reuse ROOT effective-rank Thinking Card](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_thinking_card_cn.md)

Protocol status: E03 was stopped before approval or execution, and no protocol
is retained in the experiment tree.

## 1. Problem Definition

The parent line asks whether task-function reuse, rather than raw sample
frequency, controls how many `ROOT`-state directions are needed to preserve a
learned NTP task. E03 isolates one narrower non-entailment:

> Conditional on both common-mapping conditions learning and reusing the same
> mapping, does reducing target exact-relation frequency from $F=8$ to $F=1$
> avoid inflating fixed-readout `ROOT` functional rank by more than two
> directions?

This is not a claim that an individual sample has a rank. Rank is defined on a
frozen evaluation slice containing many target relations and contexts.

### Decision-relevant terms

| Term | Plain meaning | Registered object | Cannot establish |
| --- | --- | --- | --- |
| Exact relation | One surface alias paired with one entity | Cell $t=(r,a)$ | An independent task function |
| $F_{\mathrm{exact}}(t)$ | Actual number of times cell $t$ reaches the optimizer | Count in the finite realized training stream | Function-level exposure |
| $E_{\mathrm{function}}$ | Total calls to one underlying mapping across all aliases and entities | Sum of the common-condition count matrix | Per-cell frequency |
| $K_{\mathrm{map}}$ | Number of bottom-level mappings the model must distinguish | $1$ for common; $16$ for independent | Number of neural modules |
| Common-mapping reuse | Different surface aliases call the same mapping | $y=\pi(a)$ for every alias $r$ | A particular internal algorithm |
| Fixed-readout functional rank | Fewest calibration-selected orthogonal `ROOT` directions that preserve the frozen original output head's behavior and then validate on disjoint test data | $k_{\mathrm{func}}^{\mathrm{fix}}$ | Strict matrix rank, nonlinear intrinsic dimension, or absolute universal “low rank” |

## 2. Physical Priors

**P1 — Functional reuse can dominate local frequency.** If many surface
branches call one learned mapping, a target cell observed once can use
directions learned from other calls to that mapping. Local rarity need not
create a new task direction.

**P2 — Total common-function exposure is the relevant competing dose.** A
low-frequency target condition could be easier merely because the common
mapping received more total updates elsewhere. E03 therefore holds
$E_{\mathrm{function}}$, alias totals, entity totals, answer totals, context
marginals, tokens, batches, and optimizer steps exactly fixed between the two
common conditions.

**P3 — Capability precedes rank.** A smaller rank from a model that cannot
solve target or unseen alias–entity cells is not compression. Common-mapping
held-out capability and full-state utility are hard gates.

**P4 — Readout retraining can hide missing state information.** The original
trained output head remains frozen. The primary intervention is at the
post-final-normalization `ROOT`, immediately before that head.

**P5 — Mapping count is a distinct reference variable.** A matched
$K_{\mathrm{map}}=16$ condition is informative about the direction of the
mapping-union effect, but it cannot replace the primary low- versus
high-frequency comparison at $K_{\mathrm{map}}=1$.

## 3. Falsifiable Hypotheses

For paired seed $s$, let

$$
D_s
=
k_{\mathrm{func},s}^{\mathrm{Common,LowF}}
-
k_{\mathrm{func},s}^{\mathrm{Common,HighF}}.
$$

The primary operational hypothesis is the non-inferiority statement

$$
\mathbb E[D_s]\le \tau,
\qquad
\tau=2\ \text{ROOT directions}.
$$

It says that low target frequency does not force a meaningful rank inflation
on this generator. It does not assert exact equality.

**Support:** At least eight paired seeds pass all capability and intervention
guards; the one-sided 95% paired upper confidence bound for
$\mathbb E[D_s]$ is at most $2$; at least eight of ten paired passing seeds
satisfy $D_s\le2$; and the low-frequency condition passes the unseen-cell
common-mapping gate.

**Falsification:** After all gates pass, the one-sided 95% paired lower
confidence bound is greater than $2$.

**Insufficient:** Fewer than eight valid pairs; a capability, matching,
realized-frequency, replay, shuffle, or random-subspace guard fails; or the
confidence interval crosses the margin.

The secondary directional hypothesis is

$$
k_{\mathrm{func}}^{\mathrm{Independent,HighF}}
>
k_{\mathrm{func}}^{\mathrm{Common,LowF}},
$$

but it cannot determine the primary verdict.

## 4. Mathematical Model

### Conditional probability tree and task mapping

For alias $r\in\{0,\ldots,15\}$, entity $a\in\mathbb Z_{17}$, and nuisance
context $c$, a common-condition path is

$$
r\rightarrow a\rightarrow c\rightarrow \rho\rightarrow y.
$$

The sixteen alias branches converge to one mapping node:

$$
p(y\mid r,a,c)
=
\mathbf 1\{y=\pi(a)\}.
$$

Thus $r$ is a surface condition but not a new task function. In the independent
reference,

$$
p(y\mid r,a,c)
=
\mathbf 1\{y=\pi_r(a)\},
$$

with sixteen distinct permutation tables. This makes the experimental
counterfactual a change in mapping union, not a change in answer vocabulary.

### Exposure variables

For a finite realized stream $\mathcal S$,

$$
F_{\mathrm{exact}}(r,a)
=
\sum_{x\in\mathcal S}\mathbf 1\{x\text{ uses }(r,a)\},
$$

and, for either common condition,

$$
E_{\mathrm{function}}
=
\sum_{r=0}^{15}\sum_{a=0}^{16}F_{\mathrm{exact}}(r,a).
$$

Manifest counts are not accepted as a substitute for these realized counts.

### Fixed-readout functional rank

Let $h_\rho(x)\in\mathbb R^{64}$ be the post-final-normalization `ROOT` state,
and let the trained output head $W_o$ remain frozen. An ordered orthogonal
basis $U$ and affine center $\mu$ are learned on basis-fit calibration data
only. Rank is selected on a separate calibration-selection split:

$$
\widetilde h_\rho^{(k)}
=
\mu+U_kU_k^\top(h_\rho-\mu).
$$

The registered $k_{\mathrm{func}}^{\mathrm{fix}}$ is the smallest rank whose
calibration-selection loss increase is at most $0.02$ nat and accuracy drop is
at most $0.01$, with persistent passing at every higher rank. That rank and
projection are frozen before final-test labels are read. The same thresholds
must then pass on the mutually exclusive final test; otherwise the run is not
rank-valid.

This is a task-, split-, intervention-, and tolerance-dependent linear
sufficiency measure. It is not the rank of a sample or the rank of all
intermediate computation.

## 5. Computational Realization

Use 64 target cells,

$$
\mathcal T_s
=
\{(r,(4r+j+o_s)\bmod17):r=0,\ldots,15,\ j=0,\ldots,3\},
$$

with a preregistered seed offset $o_s$. Each alias contributes four targets;
each entity contributes three or four.

Two disjoint 64-cell sets are absent from training:

$$
\mathcal U_s^{cal}
=
\{(r,(4r+j+o_s)\bmod17):j=4,\ldots,7\},
\qquad
\mathcal U_s^{test}
=
\{(r,(4r+j+o_s)\bmod17):j=8,\ldots,11\}.
$$

Every alias has eight held-out cells and nine observed cells; every entity
remains observed under four or five aliases. Holding out eight entries per
independent permutation also makes its correct permutation-completion chance
baseline $1/8$, rather than the misleading $1/2$ baseline produced by holding
out only two entries.

For a frozen baseline $B=19196$, Common-LowF assigns count $1$ to target cells,
$0$ to unseen cells, and $B$ to all remaining cells. Common-HighF assigns
count $8$ to target cells and removes the added seven presentations using an
integer transportation table $X$ over non-target, non-unseen cells:

$$
0\le X_{r,a}\le8,\qquad
\sum_aX_{r,a}=28,\qquad
\sum_rX_{r,a}=7t_a,
$$

where $t_a$ is the number of targets containing entity $a$.

Consequently, both common conditions have exactly:

- $95{,}984$ presentations per alias;
- $1{,}535{,}744$ common-function calls;
- $5{,}999$ batches of size $256$;
- identical entity and answer marginals.

The stream is traversed exactly once, with deterministic shuffling and no
resampling. A separate integer context allocation holds the global context
marginal fixed and gives both common conditions the same one target-training
context per target cell; the extra HighF occurrences are exact duplicates.
The common mapping is nevertheless exposed across a diverse family-level
context pool through the other cells.

The independent reference uses sixteen distinct, seed-random permutation
tables jointly conditioned only on the exact type and answer marginals needed
for matching. “Independent” here means sixteen separately memorized functions,
not unconditional iid sampling after the marginal constraint. A second
integer table matches its alias, entity, answer, context, token, and batch
marginals to Common-HighF.

Model, initialization, optimizer, and functional-rank machinery inherit the
E01 configuration: two layers, one head, width $64$, FF width $128$, full
position NTP CE, AdamW at $0.002$, no weight decay, and ten paired seeds.

## 6. Minimal Falsification Tests

1. **Exact frequency/function-dose audit:** Materialized and optimizer-realized
   counts must agree; target counts must be exactly $1$ or $8$; all registered
   common-condition marginals must match exactly.
2. **Common-mapping capability:** Seen-target/new-context accuracy at least
   $0.95$, unseen-cell accuracy at least $0.90$, semantic consistency at least
   $0.95$, full-state CE at most $0.10$ nat, and at least eight of ten paired
   common seeds passing.
3. **Fixed-readout functional-rank test:** Common-LowF versus Common-HighF on
   the post-norm `ROOT`, using the frozen output head and disjoint basis-fit,
   rank-selection, and final-test splits.
4. **Intervention validity:** Exact full-rank identity replay, harmful `ROOT`
   shuffle, and zero passing equal-rank random subspaces.
5. **Mapping-count reference:** Independent-HighF must learn seen entries in
   new contexts; its completely unseen random entries must remain at or below
   the registered leakage guard.

The E01 one-direction rank grid makes $\tau=2$ resolvable. E01's borderline
full-rank numerical replay was a floating-point identity-reconstruction issue,
not two directions of rank uncertainty. E03 therefore keeps the $0.02$-nat
and $0.01$-accuracy tolerances and requires the full-rank path to return the
cached unmodified state exactly.

## 7. Current Evidence

[A14_02_E01](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/summary.md)
showed that one observed surface per exact relation did not support
new-context capability in either shared or lookup conditions. Diverse
family-level exposure, not exact duplication alone, enabled capability. Among
capability-passing lookup tasks, mean post-norm functional rank increased from
$10.2$ to $11.0$ to $12.8$ as independent mapping count increased from
$K=1$ to $4$ to $16$. The curve is suggestive, but its three points do not
separate every exposure rival.

[historical A14_02_E02 result](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/summary.md)
then passed seen-pair new-context capability in both conditions but failed its
stronger unseen component-pair recombination gate: shared recombination passed
in $0/5$ seeds and averaged $0.2125$. E02 therefore does not authorize a rank
claim about component composition.

E03 does not reinterpret that failure. It changes the operational question:
the teacher explicitly defines all aliases as calls to one mapping, and held-out
alias–entity cells test whether the model learned that common mapping. If this
gate passes, a target relation with one presentation can legitimately reuse a
function learned from other relations.

The integer design is feasible before model outcomes are observed. Even after
reserving eight unseen cells per alias, five compensation cells remain. For
every one of the 17 possible target offsets, their registered
common-condition flow has an integral value of $448$, exactly the required
moved dose. A margin-conditioned independent construction and its integer
reduction table were also feasible for all ten preregistered seed layouts in
the design audit. Implementation must reproduce these checks; the audit does
not authorize a run.

## 8. Claim Boundary And Next Decision

**If supported, the allowed claim is:**

> On this controlled synthetic NTP task, after fixing the underlying common
> mapping, total function exposure, training budget, output distribution, and
> evaluation contract, reducing target exact-relation frequency from eight to
> one did not force more than two additional fixed-readout `ROOT` functional
> directions. Therefore low exact frequency does not necessarily imply high
> functional rank.

**Not allowed:** frequency never affects rank; all rare natural-language facts
reuse a common function; the model implements an explicit tree; the absolute
rank is universally low; root-state rank equals parameter rank; or the
independent reference alone proves causality.

**Exactly one next decision:** none is active for this parked subanchor. Reopen
it only if the researcher returns to the exact-frequency question after a
composition-capable shared task surface has been established.
