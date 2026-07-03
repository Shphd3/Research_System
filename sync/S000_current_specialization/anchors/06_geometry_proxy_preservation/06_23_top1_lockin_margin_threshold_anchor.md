# A06_23: Top-1 Lock-In Margin Threshold

## 0. Thinking Card

**Phenomenon:** In A06_17_04, a half-norm plus high-learning-rate stress made
the controlled bridge margin much smaller, but feature routing still preserved
perfectly. This suggests that positive margin may trigger top-1 routing
lock-in rather than acting only as a passive geometric budget.

**Mechanism guess:** Once step-0 top-1 assignment is correct and pairwise
margin is positive, the same feature repeatedly enters the same expert. This
path dependence may stabilize the routing basin even when the initial margin
is thin.

**Key variables:** row-gap scale $q$, router rows $w_e$, feature center
$\mu_f$, pairwise margin $\gamma_{f,e}$, sign flip rate, matched preserve
fraction, feature NMI, target loss.

**Causal relation:** If top-1 lock-in is real, then shrinking all pairwise
router-row gaps by $q>0$ should shrink the step-0 margin but still preserve the
original feature-to-expert identity after training. If preservation is only a
passive margin budget, smaller $q$ should cause earlier sign flips and lower
matched preserve fraction.

**Observable metric:** primary metric is matched preserve fraction at steps 5,
10, and 1600. Mechanism metrics are feature NMI, current margin, sign flip
rate, cluster-aware margin, and target loss.

**Rival Explanations:** the margin was not actually reduced; q-scaling
silently changed the assignment; training success comes from the task being
too easy; NMI remains high after expert identity changes; crossed initialization
can recover the original mapping during training.

**Decision:** supported with revision. Row-gap scaling was valid, and the
controlled bridge preserved for $q\ge 0.05$ but failed at $q=0.02$. Therefore
top-1 preservation behaves like a finite positive-margin basin, not like the
stronger rule "any positive margin is enough."

## 1. Problem Definition

**Parent problem:** A06 asks why controlled center initialization preserves
feature-to-expert routing while real-DCLM proxy routing is erased by ordinary
training.

**Sharper subproblem:** Determine whether positive margin is merely a passive
buffer or whether it creates a top-1 lock-in basin.

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
|---|---|---|---|---|---|
| Row-gap scaling | Shrink expert-row differences while keeping their common center. | $w'_e=\bar w+q(w_e-\bar w)$ | scalar $q$ | Controls initial margin without changing the argmax signs for $q>0$. | Real-DCLM behavior. |
| Thin positive margin | Correct step-0 assignment with small positive logit gap. | $\gamma'_{f,e}=q\gamma_{f,e}$ for $q>0$ | logit gap | Tests whether small positive margin still locks in. | Utility. |
| Matched preserve fraction | Fraction that stays in the original matched expert region. | route assignment compared with step-0 fixed match | fraction | Detects expert identity loss hidden by NMI. | Semantic expert value. |
| Crossed initialization | Router rows deliberately moved across the nearest competitor boundary before training. | $w'_a=(1-\alpha)w_a+\alpha w_j$ with $\alpha>1$ | scalar $\alpha$ | Negative guard: initial matched identity should fail. | Natural training crossing. |

**Decision question:** If step-0 assignment is correct but the positive margin
is made very small, does training preserve the original feature-to-expert
identity?

**Not in scope:** real-DCLM proxy preservation, semantic features, expert
utility, or a new deployable initialization method.

## 2. Physical Priors

**P1: Row-gap scale controls top-1 margin.**  
Meaning: pairwise score gaps scale as
$(w'_a-w'_j)^\top\mu_f=q(w_a-w_j)^\top\mu_f$.  
Could be wrong if: numerical ties, optimizer effects, or implementation
details make step-0 assignment change for $q>0$.

**P2: Top-1 routing has path dependence.**  
Meaning: if a feature is repeatedly routed to one expert, expert/router
updates can preserve that assignment basin.  
Could be wrong if: thin positive margins are erased smoothly by drift.

**P3: NMI is not enough for lock-in.**  
Meaning: a partition can remain feature-separated while the original
feature-to-expert identity is lost.  
Could be wrong if: matched preserve fraction and NMI always agree.

## 3. Falsifiable Hypotheses

**H1 lock-in threshold hypothesis:** Any sufficiently positive step-0 margin
enters a stable top-1 basin.  
Supported with threshold: $q=0.1$ and $q=0.05$ preserve perfectly, while
$q=0.02$ fails.  
Weakened stronger version: the run rejects the claim that every positive
margin, however thin, is enough.

**H2 passive budget hypothesis:** Initial margin is only a passive budget.  
Partially supported: $q=0.02$ is consumed by training drift, producing negative
current margins, sign flips, and lower matched preserve.  
Weakened as a smooth-collapse claim: $q\ge 0.05$ preserves perfectly instead
of degrading gradually.

**H3 crossed-init guard:** If initialization starts beyond the matched
boundary, training should not be counted as preserving the original identity.  
Supported: crossed initialization has final matched preserve 0.000 even though
feature NMI remains 0.907.

## 4. Mathematical Model

**Objects:** pseudo-center initialized router rows $w_e$, row mean
$\bar w=E^{-1}\sum_e w_e$, feature center $\mu_f$, matched expert $a(f)$, and
competitor $j$.

**Row-gap intervention:**

$$
w'_e(q)=\bar w+q(w_e-\bar w).
$$

For any pair $a,j$:

$$
w'_a(q)-w'_j(q)=q(w_a-w_j).
$$

Therefore:

$$
\gamma'_{f,j}(0)=q\gamma_{f,j}(0).
$$

For $q>0$, the sign of each pairwise gap is unchanged; the margin scale is
reduced.

**Crossed guard:**

$$
w'_a(\alpha)=(1-\alpha)w_a+\alpha w_j,\quad \alpha>1.
$$

This intentionally makes the matched row move past the nearest competitor.

**Falsifier:** if $q>0$ does not preserve step-0 assignment or does not reduce
margin approximately by $q$, the intervention is invalid.

## 5. Computational Realization

**Input objects:** controlled no-position A06 bridge, pseudo centers from
route-position k-means, audit hidden states, feature labels, router rows, and
training snapshots.

**Computed variables:** row-gap scale, step-0 margin ratio, feature NMI,
matched preserve fraction, sign flip rate, current margin, cluster-aware
margin, target accuracy, and loss.

**Algorithm stages:** discover pseudo centers; initialize pseudo router rows;
apply row-gap scaling or crossed guard; verify step-0 assignment and margin
ratio; train; run A06_21 margin-budget audit.

**Stage-local evidence:** step-0 intervention audit, per-step margin table,
final condition aggregate, lock-in threshold table, and trajectory figures.

**Expected artifacts:** protocol, summary, detailed report, tables, figures,
and updated anchor.

## 6. Minimal Falsification Tests

| Test | Question | Intervention / comparison | Primary metric | Pass / fail / insufficient | Failure means |
|---|---|---|---|---|---|
| Row-gap scale sweep | Does thin positive margin preserve? | $q\in\{1,0.5,0.25,0.1,0.05,0.02\}$ | matched preserve fraction | Pass lock-in if all $q>0$ preserve; pass passive budget if small q fails; insufficient if step-0 assignment changes. | Separates H1 from H2. |
| No-gap guard | Does zero margin break identity? | $q=0$ | matched preserve fraction and sign flips | Guard passes if identity is not preserved; insufficient if tie-breaking is ambiguous but not recorded. | Validates positive margin is needed. |
| Crossed-init guard | Can training recover original identity after crossing? | $\alpha=1.25$ nearest-competitor row interpolation before training | matched preserve fraction | Guard passes if matched preserve is low; fail if original matching recovers. | Tests H3. |

## 7. Current Evidence

**Observation:** A06_17_04 half-norm plus 3x LR lowered final dynamic margin to
about 0.701 but preserved feature NMI at 1.000.

**Interpretation:** the current evidence is consistent with lock-in but does
not decide it because half-norm was not a systematic margin threshold sweep.

**A06_23 full-run evidence:** row-gap scaling preserved step-0 assignment and
scaled margin exactly for every $q>0$. Final matched preserve remained 1.000
for $q=1.0,0.5,0.25,0.1,0.05$, with zero sign flips and positive final
current margins. At $q=0.02$, final feature NMI stayed high at 0.909, but
matched preserve dropped to 0.375, current margin became -0.588, and sign flip
rate reached 0.159. The $q=0$ and crossed guards failed original identity as
expected.

**Result interpretation:** preservation requires positive margin that is large
enough to survive early training drift. The decisive object is not the sign of
the step-0 margin alone, but the margin after expected router/feature movement.

**Boundary:** controlled no-position bridge only.

**Evidence links:** [`A06_17_04 summary`](../../experiments/A06/A06_17_04_margin_crossing_causal_stress/summary.md),
[`A06_21 summary`](../../experiments/A06/A06_21_margin_budget_preservation_audit/summary.md),
[`A06_23 summary`](../../experiments/A06/A06_23_top1_lockin_margin_threshold/summary.md),
[`A06_23 detailed`](../../experiments/A06/A06_23_top1_lockin_margin_threshold/detailed.md).

## 8. Claim Boundary And Next Decision

**Can claim:** In the controlled no-position bridge, row-gap scaling is a valid
margin intervention, and preservation has a finite margin threshold. The tested
safe region includes $q\ge 0.05$ and excludes $q=0.02$ under C0-C3, 8 seeds,
and this training setup.

**Cannot claim:** the numerical threshold transfers to real-DCLM, any positive
margin is enough, or feature NMI alone proves original expert-identity
preservation.

**Next decision:** apply the same margin-threshold audit to real-DCLM proxy
initialization: compare real step-0 margins with measured step-5/10
router/feature drift using matched preserve fraction, current margin,
cluster-aware margin, and sign-flip rate.
