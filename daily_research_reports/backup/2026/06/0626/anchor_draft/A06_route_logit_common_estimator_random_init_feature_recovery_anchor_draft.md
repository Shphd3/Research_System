---
anchor_id: draft_A06_route_logit_common_estimator_random_init_feature_recovery
status: draft_researcher_judgment_record_for_user_review
created: 2026-06-26
canonical_language: en
---

# Draft Anchor: Route-Logit Common Estimator Under Random-Init Training

This is a draft researcher judgment record only. It is not a formal anchor, not a protocol,
and does not authorize an experiment run.

## 1. One-Sentence Question

During random-init MoE training, can a routing-aware common-component estimator
remove the shared load-driving directions so that residual hidden states recover
feature-level clustering or positive routing margins?

## 2. Phenomenon

Earlier A06 results suggest that raw hidden states contain common components
that can dominate top-1 routing. Simple mean subtraction or generic PCA is not
enough to define the right common part, because the largest hidden-state
variance may reflect position, frequency, or role structure rather than the
direction that actually biases routing.

The new phenomenon to audit is narrower: under random router initialization
during training, there may be a routing-common direction that creates expert
load bias. If this direction is estimated and removed, feature residual
geometry may become easier to cluster or route.

## 3. Mechanism Guess

The common component should be estimated by how it affects routing, not only by
hidden-state variance.

Candidate estimators:

### A. Mean Estimator

Estimate the common vector by the calibration mean:

$$
c_{\mathrm{mean}}(t)=\frac{1}{N}\sum_i h_i(t).
$$

Risk: this removes global translation only. It may not remove the direction
that actually creates router load bias.

### B. Top-PC Estimator

Estimate a common subspace by the largest hidden-state variance directions.

Risk: top principal components may be position, token frequency, or slot-role
directions, not routing-common directions.

### C. Route-Logit Estimator

Use the current random router rows to define route logits:

$$
z_{i,e}(t)=w_e(t)^\top h_i(t).
$$

The target common direction is not simply the largest hidden direction. It is a
direction whose projection systematically changes expert logits or expert load
across many tokens. Operationally, score candidate directions by how much
removing that direction changes route logits, route margins, or expert load.

Candidate score:

$$
S_{\mathrm{logit}}(v;t)=
\operatorname{Var}_{i,e}
\left(w_e(t)^\top ((v^\top h_i(t))v)\right),
$$

with guards against selecting directions that are merely feature, position, or
frequency directions.

### D. Load-Sensitive Ablation Estimator

For candidate directions $v_j$, ablate one direction:

$$
h_i'(t)=h_i(t)-(v_j^\top h_i(t))v_j.
$$

Then rerun the current router on $h_i'(t)$. A routing-common direction should
cause a large change in expert load or common logit bias when removed.

Candidate score:

$$
S_{\mathrm{load}}(v_j;t)=
\left\|p_{\mathrm{expert}}(h;t)-p_{\mathrm{expert}}(h';t)\right\|_1.
$$

This is closer to routing than plain PCA, but it can still select a shortcut if
load change is driven by position, frequency, or slot role.

## 4. Rival Explanations

1. **True routing-common removal:** the estimator removes directions that cause
   random-router load bias; residual states recover feature clusters or
   positive margins.
2. **Generic PCA / role shortcut:** the estimator removes high-variance
   position, frequency, or slot-role directions; load changes but feature
   discovery does not improve.
3. **Load-only fix:** expert load becomes more balanced after subtraction, but
   feature-route NMI or feature-center margin does not improve.
4. **Random-router artifact:** the estimated direction is specific to one
   random router seed and does not transfer across seeds or checkpoints.
5. **Feature geometry already present / absent:** common subtraction may look
   helpful only because raw feature geometry was already clusterable, or fail
   because random training has already erased the feature-relevant geometry.

## 5. One Primary Metric

Primary metric:

$$
\Delta \mathrm{feature\_NMI}(t)=
\mathrm{feature\_NMI}_{\mathrm{after\ subtract}}(t)
-
\mathrm{feature\_NMI}_{\mathrm{raw}}(t).
$$

This should be measured on held-out route-position states after fitting centers
on the residualized candidate pool.

Why this metric:
the question is not whether subtraction changes load. The question is whether
subtracting an estimated routing-common component makes feature-level geometry
more discoverable or routable.

Required guards:

- expert load before and after subtraction;
- nuisance / position / frequency NMI;
- route margin from residual centers on raw and residual inputs;
- stability across random router seeds and training snapshots;
- random-direction ablation control with the same number of removed directions.

## 6. Pass / Fail / Insufficient

**Pass:** a routing-aware estimator improves held-out route-position
`feature_NMI` over raw, mean-subtracted, top-PC, and random-direction controls,
while not increasing position / frequency / nuisance dependence. The effect
must hold across multiple random router seeds and early training snapshots.

**Fail:** subtraction changes load but does not improve feature NMI or route
margin; or the selected directions are explained by position, frequency,
slot-role, or one random router seed.

**Insufficient:** hidden states, router rows, route assignments, feature labels
for post-hoc audit, or training snapshots are missing; or the estimator uses
feature labels / route-position labels during fitting.

## 7. New Training Or Audit Only

Audit-only if existing A06_17_02 or A06_16 random-init runs saved router rows
and route-position hidden states at every snapshot.

New training / rerun is needed if raw hidden states were not saved. The rerun
does not need a new method objective; it only needs random-init training
snapshots with enough hidden-state logging to estimate and ablate common
directions.

## Initial Review Gate

1. **Question drift:** the question is still inside A06 preservation/geometry,
   but it is not the same as A06_19 margin-aware center search. This anchor is
   about estimating the common component under random-init dynamics.
2. **Missing rivals:** the strongest missing rival would be "the direction is a
   route-position selector rather than common." The protocol must guard this.
3. **Metric fit:** load change alone is not enough. The primary metric must be
   feature discovery / routing improvement after subtraction.
4. **Pass / fail clarity:** pass requires feature-NMI or margin improvement,
   not just better load balance.
5. **Cannot claim:** even if passed, this only supports a controlled common
   estimator. It cannot claim real-DCLM semantic features or utility.
