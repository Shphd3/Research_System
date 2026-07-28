---
anchor_id: 14_02_relation_reuse_root_effective_rank
status: frequency_noninferiority_supported_e03_space_blocked
canonical_language: en
companion_cn: 14_02_relation_reuse_root_effective_rank_anchor_cn.md
line: 14_tree_low_rank_language_structure
depends_on: 14_01_relation_reuse_parameter_state_bridge
thinking_card: 14_02_relation_reuse_root_effective_rank_thinking_card_cn.md
protocol_status: e02_completed_e03_parked_at_gate
---

# A14_02 Shared Compositional Rules And Task-Functional Root-State Rank

Thinking Card source: [14_02_relation_reuse_root_effective_rank_thinking_card_cn.md](14_02_relation_reuse_root_effective_rank_thinking_card_cn.md)

Line foundation: [A14_00 conditional low-rank hierarchy](../14_00_tree_low_rank_language_structure/14_00_tree_low_rank_language_structure_anchor.md).

## 1. Problem Definition

**Parent problem:** Determine whether long-range hierarchical structure supports reusable, task-sufficient conditional computation, rather than assuming that tree structure is intrinsically low-rank.

**Sharper problem:** Under next-token prediction, does cross-context reuse of a shared compositional rule require fewer root-state directions to preserve held-out task behavior than an equally sized collection of independent random lookup rules, after excluding trivial effects from answer classes, task failure, final-readout bottlenecks, and lookup cardinality?

**Decision question:**

> After matching exact-relation frequency $F$, rule count $K$, context diversity $D$, output entropy, model, and full-state held-out utility, does a shared compositional rule require a lower-dimensional task-root subspace to preserve held-out utility?

### Terminology

| Term | Plain meaning | Concrete object | Cannot prove |
|---|---|---|---|
| Root state $h_\rho(x)$ | Task summary after all relevant tokens and before the answer | Hidden state at the preregistered `ROOT/QUERY` position | That the network implements an explicit tree |
| Answer prototype $\mu_y$ | Mean root state for one answer meaning | Calibration estimate of $\mathbb E[h_\rho\mid y]$ | A causal computation path |
| Root residual $r(x)$ | Context/computation variation after removing answer identity | $h_\rho(x)-\mu_y$ | That all residual variation is mechanistic |
| Task-functional root rank $k_{\mathrm{func}}$ | Minimum root-state directions needed to preserve held-out behavior | Calibration-fit subspace and test intervention replay | Strict rank, nonlinear intrinsic dimension, or per-example complexity |
| Root-residual effective rank | Effective number of spectral directions in root residuals | Entropy effective rank; secondary diagnostic | Task sufficiency or causal use |
| Task utility gate | The model learned the registered task | Held-out answer accuracy / CE | Why it learned |
| Semantic consistency | Equivalent contexts yield the same answer meaning | Cross-context semantic agreement | Deterministic surface wording |
| Lookup count $K$ | Number of mappings that must be independently memorized | Independent generator tables/permutations | The number of neural modules |
| Local Jacobian image | ROOT directions induced by infinitesimal task-parameter directions at one parameter point | $J_\rho(x;\theta)G$ across held-out contexts | A finite training effect |
| Learned secant image | ROOT directions of one exact finite parameter-block effect | $h_\rho(x;\theta_T)-h_\rho(x;\theta_{\mathrm{ref}})$ | A pointwise-constant Jacobian along training |

## 2. Physical Priors

**P1: Rule reuse can reduce task-required degrees of freedom.** The same composition reused across contexts may permit a shared root-state formation mechanism such that a smaller state subspace preserves the task. This prior is weakened if matched shared and lookup conditions require the same held-out functional rank.

**P2: Answer identity can create trivial spectral concentration and contaminate functional replay.** A final state may encode only a finite answer class. Selecting $\mu_y$ with the test answer would also leak the target. The primary functional intervention therefore uses a calibration mean that does not depend on test-answer identity; within-answer residual rank is secondary.

**P3: Lookup cardinality is a live rival.** Fewer independent tables can lower task-functional rank even under pure memorization. Shared and lookup conditions must be matched in $K$, and the lookup-$K$ curve is reported separately.

**P4: Spectral concentration is not functional compression.** High-energy directions can be task irrelevant and low-energy directions can be decisive. The registered root state must be projected and the frozen model suffix replayed; spectral rank is only a companion diagnostic.

**P5: Intermediate root states admit an information bypass.** If only an intermediate-layer `ROOT` is projected, later attention can reread the other token states. Preserved utility would not establish that the projected root itself was sufficient. The primary metric therefore uses the `ROOT` after final LayerNorm/RMSNorm and before the LM head. The corresponding pre-normalization residual state is a secondary localization point that replays the real final normalization and answer head. Intermediate layers can be called functionally low-rank only with a registered no-reread or bypass audit.

**P6: Cross-context sharing and training-time stability are different
conditions.** A point Jacobian may have a shared image across contexts while
that image rotates as parameters move. A finite-training claim must therefore
either bound the Taylor remainder explicitly or use the exact learned secant /
path-integrated image. Pointwise H9 alone is not a finite-displacement bridge.

## 3. Falsifiable Hypotheses

**H1 — Shared-structure functional compression:**

$$
k_{\mathrm{func}}(shared;\epsilon)
<
k_{\mathrm{func}}(lookup;\epsilon)
$$

at matched $K,F,D$ and task utility. The effect remains visible when each exact relation is rare, and the shared condition generalizes to unseen contexts or combinations.

**Strongest rival H0 — Lookup cardinality or answer-bottleneck sufficiency:**

$$
k_{\mathrm{func}}\approx f(K,F,\text{answer bottleneck}),
$$

with no additional contribution from shared composition.

**Pass:** both compared conditions pass matched full-state utility; the rare shared condition passes the unseen-combination/context gate; the preregistered functional-rank advantage has a positive 95% interval and the expected sign in at least 4/5 seeds; the learned subspace beats equal-rank random subspaces; full-rank replay restores the model; lookup cardinality does not explain the full gap.

**Fail:** the shared functional-rank effect vanishes after matching $K,F,D$, or it is explained by the final answer bottleneck, lookup count, or task failure.

**Insufficient:** failed capability, unmatched answer distribution/sample count/root state/checkpoint, test-answer leakage in the intervention, failed full-rank replay, single-seed dependence, post-hoc thresholding, or a floor effect.

## 4. Mathematical Model

For held-out example $x_i$, collect the root state after final LayerNorm/RMSNorm and before the LM head,

$$
h_i=h_\rho(x_i)\in\mathbb R^d.
$$

Estimate a global calibration mean $\mu^{cal}$ that does not use answer identity, and fit a $k$-dimensional orthogonal subspace $U_k$ on calibration data only. On test examples, replace the registered state by

$$
\widetilde h_i^{(k)}
=
\mu^{cal}+U_kU_k^\top(h_i-\mu^{cal}),
$$

then replay the frozen model suffix. For preregistered loss and accuracy tolerances $(\epsilon_L,\epsilon_A)$, define

$$
k_{\mathrm{func}}
=
\min\left\{
k:
\begin{array}{l}
L_{\mathrm{test}}^{(k)}-L_{\mathrm{test}}^{full}\le\epsilon_L,\\
A_{\mathrm{test}}^{full}-A_{\mathrm{test}}^{(k)}\le\epsilon_A
\end{array}
\right\}.
$$

The protocol requires persistent threshold crossing across all higher registered dimensions. If $U_k$ is restricted to calibration PCA directions, this is an auditable upper bound on task-functional rank rather than the unconstrained minimum; a task-aware subspace requires a frozen optimization and overfitting contract. Because the primary state is immediately upstream of the answer head, this quantity means “root-state dimension sufficient for the registered answer task,” not the dimension of all intermediate compositional computation.

The secondary geometric diagnostic uses calibration answer prototypes to construct

$$
r_i=h_i-\mu_{y_i}^{cal},
\qquad
R_\rho=[r_1,\ldots,r_n],
$$

and reports its entropy effective rank without using it for the primary intervention. The primary normalized comparison is

$$
\Delta k_{\mathrm{structure}}
=
\frac{
k_{\mathrm{func}}^{lookup}
-
k_{\mathrm{func}}^{shared}
}{
d
}.
$$

## 5. Computational Realization

Use a controlled two-step compositional NTP task.

In the shared family,

$$
u=\phi_\alpha(a),
\qquad
y=\psi_\beta(u),
$$

where all rule instances share the same factorized forms $\phi,\psi$ and differ only in parameters. Hold out input–parameter combinations.

In the lookup family, preserve sequence length, vocabulary, answer distribution, rule count, and exposure, but replace each rule instance with an independent random permutation/table.

Registered exposure conditions are:

- `unique-diverse`: each exact relation appears once, while many relations share one compositional form;
- `repeat-diverse`: an exact relation repeats across distinct nuisance contexts;
- `repeat-duplicate`: the same surface example repeats, separating count from context diversity.

Train the same small causal Transformer with full-position NTP. Intervene primarily on the post-final-normalization state at the answer-preceding `ROOT` position and replay the frozen answer head. This avoids later attention rereading unprojected token states. Intervene secondarily on the corresponding pre-normalization residual state and replay the real final normalization plus answer head to localize normalization effects; this secondary result does not decide the verdict. Calibration chooses both the capability checkpoint and subspace without test-rank or test-loss access. Early/middle-layer profiles are secondary and cannot be interpreted as functional rank unless a no-reread or explicit bypass audit is added. The final state can still reflect an answer bottleneck, so the claim remains limited to the registered answer task.

## 6. Minimal Falsification Tests

**Decisive test:** compare matched `shared / unique-diverse` and `lookup / unique-diverse`.

Primary metric: $\Delta k_{\mathrm{structure}}$.

Required guards: full-state held-out utility, semantic consistency, balanced answer distribution, equal root-state sample count, fixed checkpoint selection, full-rank replay, and equal-rank random subspaces.

**Lookup-cardinality calibration:** vary $K$ within lookup-only conditions and report $K\mapsto k_{\mathrm{func}}$. This quantifies the memorization rival but is not treated as a universal causal law unless a fully factorial exposure design is achieved.

**Frequency–diversity guard:** compare `repeat-diverse` with `repeat-duplicate` at matched count.

**Non-overlap with the senior Q/K ablation:** the senior experiment removes tail singular directions from Q/K parameter matrices and measures A-to-C loss robustness under a composite share manipulation. A14_02 instead projects a hidden root state, replays the frozen suffix, matches $K,F,D$, and asks how many state directions preserve held-out task utility. It therefore tests the missing parameter-to-task-state and rule-reuse bridge rather than repeating parameter-spectrum ablation.

## 7. Current Evidence

The completed
[A14_01/E08 parameter--state bridge](/Projects/from-attention-to-search/main/experiments/A14/14_tree_low_rank_language_structure/A14_E08_relation_reuse_state_bridge/summary.md)
provided bounded reconstruction evidence that the extreme
high-reuse/low-rule-count condition had a small held-out state-rank advantage,
while parameter compression was much larger and intermediate conditions were
non-monotonic. Because that experiment jointly changed lookup count and
per-rule exposure, it did not identify shared structure.

The completed
[A14_02_E01 four-GPU run](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/summary.md)
returned a formal `insufficient` verdict:

1. both low-exposure primary conditions reached 1.0 training accuracy but
   failed new-context capability in 0/5 seeds; their rank contrast is
   uninterpretable;
2. repeating the identical context eight times also failed in 0/5 seeds,
   whereas diverse-context exposure passed in 4/5 shared seeds;
3. among capability-passing lookup controls, mean post-norm functional rank
   rose from 10.2 to 11.0 to 12.8 as independent lookup-table cardinality rose
   from 1 to 4 to 16;
4. high-exposure shared runs were suggestively lower-rank than `K=16` lookup
   runs by 2.5 directions over four paired passing seeds, but this missed the
   four-direction effect threshold, one shared seed failed, and no shared seed
   passed the unseen-composition gate.

The evidence therefore supports a distinction between exposure count, context
diversity, and independent rule cardinality. It does not yet establish that
shared compositional structure itself lowers root-state functional rank.

The separate
[archived A14_02_E02-v1 capability run](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/summary.md)
then removed the base-capability confound. Shared and lookup conditions both
passed seen-pair new-context capability in 5/5 seeds, but shared unseen-pair
recombination passed in 0/5 seeds and averaged 0.2125 against the frozen 0.80
gate. All four held-out-pair means were below 0.70. The task therefore remains
ineligible for a shared-versus-lookup rank interpretation even after the
component-pair split correction.

The autonomous H9 audit then separated the local and finite parameter-to-ROOT
bridges:

1. [E04](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E04_shared_jacobian_path_image/summary.md)
   supported the registered trained-point local H9 in 5/5 seeds. The
   calibration task-gradient image had mean eight-direction tail 0.0393 and
   held-out capture 0.9607, compared with random-subspace tail 0.2206.
2. [E05](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E05_trajectory_jacobian_closure/summary.md)
   found that the actual block displacement was 0.9975 captured by eight
   trajectory directions and functionally preserved, and that the exact block
   ROOT effect had tail 0.0132. Nevertheless, the endpoint Jacobian image
   captured only 0.3672 of that exact effect; registered closure was refuted
   in 4/5 seeds.
3. [E06](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E06_reference_jacobian_vs_secant/summary.md)
   made the distinction decisive. The exact learned secant passed all
   eight-dimensional cross-context and frozen-head controls in 5/5 seeds,
   while the point linearization had mean relative error 1.2595 and H11 was
   refuted in 5/5. Reference-point H9 itself was intermediate rather than
   refuted. A post-registered complete-block-displacement guard retained 5/5
   H11 refutation with mean relative error 1.2441, excluding the small
   trajectory-subspace residual as the cause; it reused the same checkpoints
   and is not independent confirmation.

The resulting evidence supports local cross-context image sharing, an
effectively low-dimensional training displacement, and a low-dimensional
finite ROOT effect in this model. It rejects the use of one point Jacobian as
the finite-training bridge. The probabilistic sparse-activation theorem should
therefore use a learned secant/path-integrated image for finite updates and
retain point H9 only as a local corollary with an explicit remainder bound.
There remains no evidence that ROOT rank equals QK parameter rank or that low
ROOT rank creates Router value.

The improved
[E02 frequency--mapping separation](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E02_frequency_mapping_rank_separation/summary.md)
then isolated exact frequency inside one learned common mapping. All 10 paired
seeds passed capability and rank-validity gates. LowF and HighF mean functional
ranks were 7.6 and 7.4 directions; the paired mean difference was 0.2 and its
one-sided 95% upper bound was 0.5, below the frozen two-direction margin. LowF
also achieved 1.0 zero-exposure unseen-cell accuracy in every seed. This
establishes frequency non-inferiority in the registered task, not a shared
versus independent-mapping advantage. The approved
[E03 rare--common intervention](/Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E03_rare_common_subspace_reuse/summary.md)
was parked before treatment: a 32-probe common AdamW step basis captured only
0.478--0.631 of held-out common-step energy, so 0/10 seeds passed the 0.80
stability gate.

## 8. Claim Boundary And Next Decision

**Currently allowed:** In this controlled NTP generator, raw duplicate
frequency was insufficient for new-context invariance; diverse-context
exposure was necessary. Among solved lookup tasks with matched exposure and
context allocation, more independent mapping tables were associated with
larger task-functional ROOT rank. After matching seen-pair capability, the
registered shared task still did not support reliable unseen component-pair
recombination. In the separate learned-common-mapping bridge audit, trained
task directions had a shared local ROOT Jacobian image, the actual optimizer
and finite ROOT effects were effectively eight-dimensional, and a single
point Jacobian failed to approximate the finite learned effect. In the improved
frequency audit, reducing one exact-cell frequency from 8 to 1 did not inflate
the frozen-readout ROOT functional rank beyond the two-direction margin after
strict zero-exposure cross-surface capability. This state-functional result did
not automatically identify a stable common raw-AdamW update space.

**Not allowed:** all rare shared rules are low-rank; shared composition causes the
observed high-exposure rank gap; the E02 network learned the shared algorithm;
frequency is universally irrelevant; the three-point lookup curve is universal;
NTP guarantees a shared secant image; the instantaneous Jacobian basis is
constant along training; natural language is globally tree-structured or
low-rank; parameter and ROOT ranks coincide; or low rank establishes expert
specialization or Router utility.

**Exactly one next decision:** retain the positive frequency non-inferiority
result and preregister a leave-target-out common ROOT-functional/secant space
on fresh probes before retrying the rare-direction intervention.
