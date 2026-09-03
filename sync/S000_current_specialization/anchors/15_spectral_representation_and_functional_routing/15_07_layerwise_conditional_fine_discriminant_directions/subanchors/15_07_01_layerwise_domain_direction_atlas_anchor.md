---
anchor_id: 15_07_01_layerwise_domain_direction_atlas
status: RESULTS_READY_AWAITING_HUMAN_ACCOUNT
canonical_companion: 15_07_01_layerwise_domain_direction_atlas_anchor_cn.md
active_focus: ../../../../../../../daily_research_reports/backup/2026/08/0820/focus_layerwise_domain_direction_atlas.md
parent_anchor: ../15_07_layerwise_conditional_fine_discriminant_directions_anchor.md
created: 2026-08-20
updated: 2026-08-21
---

# A15_07_01: Layerwise Domain Direction Atlas


## 1. Problem Definition

The long-term direction is a low-rank layerwise Router that can expose different
information at different depths. The smallest current blocker is not Router
architecture but representation meaning: for each known parent domain, which
spectral coordinate system, axes, and subspace dimension stably carry its
within-domain fine-class distinctions?

At Qwen3-8B blocks 24 and 28, let $X_\ell$ be the normalized state before the
attention write and let $R_{U,\ell}$ be the same-token attention update after
subtracting the component affinely predictable from $X_\ell$ using TRAIN only.
$R_U$ is a candidate update, not new knowledge.

**Single decision question:**

> On unseen expressions, can fixed-axis discriminant selection identify the
> concrete spectral directions that carry each domain's fine-class function,
> while a freely rotated supervised low-rank model confirms the minimum useful
> dimension; and do the resulting functional directions support a bounded
> shared-versus-domain-specific atlas?

A Pass permits a separate Router-input experiment. Basis sensitivity permits
only a learned projection, not a fixed spectral rule. Failure stops Router
changes based on these directions. No outcome in this Anchor tests expert
utility or specialization.

## 2. Physical Priors

1. **Variance and discrimination order different objectives.** A direction can
   have modest population variance yet reliably separate fine classes.
2. **A spectral location is basis-relative.** Agreement across a local
   parameter-response basis, a common parameter-response basis, and a
   large-sample activation basis is stronger than a claim made in one basis.
3. **Geometry becomes an atlas only after held-out function.** Axis selection,
   subspace overlap, or a semantic-looking heatmap cannot label a direction
   shared or specific unless it preserves unseen-expression classification.

## 3. Falsifiable Hypotheses

**H1 — stable fixed-axis directions.** For at least one registered block and a
majority of the eight domains, DEVELOPMENT selects at most 16 fixed axes in at
least two of the three frozen bases, and those axes retain unseen-expression
fine-class gain beyond matched spectral-head, random-axis, and label-permutation
controls. The result must survive a tenfold stronger denominator shrinkage.

**H2 — freely rotated low-rank confirmation.** On the same admitted
domain-layer pairs, a supervised rank at most four retains the candidate
update's unseen-expression function beyond a label-permutation control. Rank
seven is the centered eight-class algebraic contrast ceiling and is not by
itself evidence of nontrivial low rank.

**H3 — bounded shared and specific candidates.** A fixed axis is shared only
if independently selected for at least two domains and has positive held-out
marginal function in every participating domain. It is a domain-specific
candidate only if selected for one domain and its held-out own-domain utility
exceeds its maximum cross-domain utility. Unqualified components remain
unresolved rather than being forced into either class.

**Strongest rival.** A freely rotated model may work while every fixed basis
disagrees, meaning low-dimensional function exists but no stable spectral axis
atlas has been identified. Alternatively, both methods may fail on new
expressions, exposing prior expression dependence.

## 4. Mathematical Model

For domain $p$, fine class $c$, example $i$, and one orthonormal frozen basis
$V=[v_1,\ldots,v_D]$, let $r_{pci}$ be native-coordinate $R_U$. Define

$$
B_p=\frac1{8}\sum_c(\mu_{pc}-\mu_p)(\mu_{pc}-\mu_p)^\top,
\qquad
W_p=\frac1{8}\sum_c\frac1{n_c}\sum_i(r_{pci}-\mu_{pc})(r_{pci}-\mu_{pc})^\top.
$$

The fixed-axis discriminant score is

$$
s_{pj}=\frac{v_j^\top B_pv_j}
{v_j^\top W_pv_j+\rho_p},
\qquad
\rho_p=10^{-2}\frac{\operatorname{tr}(W_p)}{4096}.
$$

Axes are ranked by $s_{pj}$ using TRAIN only. A tenfold larger $\rho_p$ is the
small-denominator guard. Projected coordinates are TRAIN-standardized before a
ridge correction head is fit, so coordinate scale cannot win by itself.

The freely rotated comparison solves reduced-rank ridge regression from
standardized $R_U$ to the residual centered one-hot target after an
out-of-fold $X$-only classifier. Its native-coordinate input subspace is the
column space of the standardized coefficient after inverse feature scaling.
This method establishes accessible low-dimensional function but does not name
fixed spectral axes.

For any condition $m$, the primary functional unit is per-example
cross-entropy gain

$$
g_i^{(m)}=CE(f_X(x_i),y_i)-CE(f_X(x_i)+f_m(r_i),y_i)
$$

in nats per example. Retention is aggregate projected gain divided by admitted
full-$R_U$ gain. It does not prove native model use.

## 5. Computational Realization

1. Freeze Qwen3-8B, blocks 24/28, the E03 same-token hook, TRAIN residualizer
   and feature standardizer, and the eight-domain by eight-fine-class task.
   TRAIN fits directions and heads; DEVELOPMENT selects dimension and ridge;
   a new 1,920-row expression bank is opened once for confirmation.
2. Compare three orthonormal rulers in the same native 4,096-dimensional hidden
   coordinate: the eigensystem of the current layer's MLP input Gram operator;
   the trace-normalized mean MLP-response eigensystem across all layers; and
   the existing top-500 activation PCA basis fit from 131,072 DCLM TRAIN tokens.
   The activation ruler supports claims only inside its identified top-500
   span; its orthogonal complement is one unresolved bin, not invented axes.
3. Evaluate fixed-axis ranks $\{1,2,4,8,16,32,64\}$ and freely rotated ranks
   $\{1,2,4,7\}$. For each domain, record function, selected axis indices,
   normalized spectral bands, pairwise domain overlap, and the held-out
   high-versus-low fine-class response fingerprint.

Exact splits, controls, bootstrap family, seeds, artifacts, and stop rules are
frozen in the linked Protocol.

## 6. Minimal Falsification Tests

The confirmation bank first requires full $R_U$ to beat duplicate-$X$ and
within-domain mismatched-$R_U$ controls. A fixed-basis/domain result qualifies
only when its selected rank is at most 16, its simultaneous 95% retention lower
bound exceeds 0.80, and its gain exceeds the strongest registered fixed-axis
control with a simultaneous lower bound above zero under both shrinkages.

The freely rotated result qualifies at rank at most four under the same
retention boundary and a permutation-excess lower bound above zero. Results are
typed per domain as stable basis-robust, stable basis-sensitive, stable only at
the full contrast ceiling, no stable compact direction, or insufficient.

Shared/specific labels are conditional on these functional gates. Confidence
intervals use paired resampling inside every domain-by-class cell; missing or
nonpositive full-gain denominators make retention insufficient rather than
clipped.

## 7. Current Evidence

The completed predecessor experiment provides three verified premises but not
the present atlas. Frozen supervised spaces survived new expression and fact
panels at block 28 with minimum simultaneous retention lower bounds above
0.987. Their held-out function concentrated in the first of five task-TRAIN
PCA bands, whereas the older opened diagnostic had placed a different rank-7
projector mainly in ranks 257–639. On MASSIVE, block 24 admitted a small
candidate-update gain, but local/shared rank ordering was insufficient. These
observations motivate a direct method-and-basis comparison; they cannot serve
as the new confirmation evidence.

E02 is complete on a sealed 1,920-row expression bank. Full-$R_U$ admission
passes for 15/16 domain-layer pairs; block-24 mathematics is unresolved. All
domains select the full seven independent output contrasts rather than rank
1/2/4, and no fixed-basis condition passes the registered robustness gates.

The learned rank-seven spaces concentrate in the final parameter-response
band: mean energy is 0.246/0.270 at block 24 and 0.411/0.435 at block 28 for
the local/common rulers, versus matched-Haar q95 near 0.066. Their activation-
PCA complement energy is 0.751 and 0.621. Mean cross-domain projector overlap
rises from 0.152 at block 24 to 0.297 at block 28, well above Haar q95 0.0023.
These are full-contrast geometry and spectral-band observations, not qualified
shared functional directions. Canonical evidence is in the E02
[Summary](/Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E02_fixed_axis_and_learned_subspace_atlas/summary.md)
and [Detailed record](/Projects/from-attention-to-search/main/experiments/A15/15_07_layerwise_conditional_fine_discriminant_directions/A15_07_E02_fixed_axis_and_learned_subspace_atlas/detailed.md).

## 8. Claim Boundary And Next Decision

A supporting result can establish only a basis-explicit linear atlas for one
frozen model, two blocks, eight named domains, and one controlled expression
population. Fine-class response fingerprints identify label contrasts, not
natural-language concepts independent of the task. Shared means replicated
held-out linear function, not universal semantic identity.

The result cannot establish new knowledge, causal use, expert utility, Router
quality, expert specialization, LoRA behavior, forgetting resistance, or
transfer to other models, layers, languages, and datasets.

**Exactly one next decision:** the researcher confirms or corrects the boundary
that E02 establishes a shared tail/complement spectral-band pattern but no
compact fixed-axis atlas, so no Router proxy change is promoted from this
result. The 16 outcomes and three registered figures are complete; the
researcher-owned result account remains pending.
