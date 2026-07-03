# A06_17_03: Feature Drift Margin Boundary

Document status: result-updated minimal anchor. Full local two-GPU audit
supports the observed margin-buffer boundary explanation.

## 0. Thinking Card

**Phenomenon:** A06_17_02 showed that correct center initialization preserves
feature routing without active router-center tracking. The open question is
how much feature-center drift the initial routing margin can tolerate.

**Mechanism guess:** Preservation holds while the feature center remains inside
the step-0 router region. Failure should appear when center drift consumes the
initial distance to the nearest expert boundary, unless router movement
compensates.

**Key variables:** feature center $\mu_f(t)$, router rows $w_e(t)$, step-0
matched expert $e(f)$, nearest step-0 competing expert $j^*(f)$, initial
boundary distance, center drift, dynamic margin, and feature switch.

**Causal relation:** Larger initial margin should create a larger safety
buffer. Feature switch should occur only when drift or router movement erodes
that buffer.

**Observable metric:** boundary consumption and switch relation:

$$
B_f(t)=1-\frac{(w_{e(f)}(0)-w_{j^*(f)}(0))^\top \mu_f(t)}
{(w_{e(f)}(0)-w_{j^*(f)}(0))^\top \mu_f(0)+\epsilon}.
$$

**Rival Explanations:** margin buffer; router compensation; common/norm drift;
feature cloud tail crossing before center crossing; matching artifact.

**Decision:** observed center-init preservation stays inside the margin buffer.
This supports margin-buffer geometry for the observed trajectory.

## 1. Problem Definition

**Parent problem:** why center-initialized routing can survive controlled early
training.

**Sharper subproblem:** after active tracking is weakened, identify the
geometric boundary of margin-based preservation.

**Decision question:** In observed A06 bridge trajectories, do feature switches
or margin failures occur when center drift consumes the initial boundary
buffer?

**Not in scope:** real-DCLM preservation, semantic experts, utility, or a full
synthetic perturbation phase diagram.

## 2. Physical Priors

**P1:** A top-1 dot-product router defines linear decision boundaries between
experts.  
**Meaning:** each matched feature center has a signed distance to its nearest
step-0 expert boundary.  
**Could be wrong if:** routing changes despite large positive distance and no
dynamic-margin erosion.

**P2:** Margin preservation has a finite drift budget.  
**Meaning:** if the center crosses the initial or dynamic boundary, preserved
routing should fail.  
**Could be wrong if:** large boundary consumption does not reduce margin or
increase switch risk.

**P3:** Router movement can compensate or worsen hidden drift.  
**Meaning:** frozen-boundary distance and dynamic margin must both be reported.
**Could be wrong if:** frozen-boundary metrics alone perfectly explain all
switches.

## 3. Falsifiable Hypotheses

**H1 margin-buffer boundary:** switches or near-zero margins appear when
boundary consumption approaches or exceeds 1.  
**Supported if:** preserved cases stay below the boundary and failed cases have
high boundary consumption or negative dynamic margin.  
**Weakened if:** switches occur with low consumption and positive margins.
**Status:** supported for the observed center trajectories.

**H2 router compensation:** router movement changes the boundary enough that
frozen step-0 distance is insufficient.  
**Supported if:** frozen consumption is high but dynamic margin remains
positive and routing stays preserved.  
**Weakened if:** frozen and dynamic boundaries agree.
**Status:** not required for the current center-init conclusion; dynamic margin
remains positive while frozen boundary consumption stays below crossing.

## 4. Mathematical Model

**Objects:** at step 0, match feature $f$ to expert $e(f)$ and nearest
competitor $j^*(f)$. Define the step-0 boundary normal

$$
n_f(0)=w_{e(f)}(0)-w_{j^*(f)}(0).
$$

**Core decomposition:** initial signed distance:

$$
d_f(0)=\frac{n_f(0)^\top \mu_f(0)}{\|n_f(0)\|+\epsilon}.
$$

Frozen-boundary signed distance:

$$
d_f^{\mathrm{frozen}}(t)=
\frac{n_f(0)^\top \mu_f(t)}{\|n_f(0)\|+\epsilon}.
$$

Dynamic margin:

$$
M_f(t)=\min_{j\neq e(f)}
(w_{e(f)}(t)-w_j(t))^\top \mu_f(t).
$$

**Mechanism relation:** margin-buffer preservation predicts $d_f(t)>0$ and
$M_f(t)>0$ for preserved features.

**Observable metrics:** boundary consumption, Euclidean drift ratio,
dynamic margin, feature switch, and route heatmap.

**Falsifier:** switch occurs while frozen distance and dynamic margin remain
strongly positive, or preservation holds despite negative dynamic margin.

## 5. Computational Realization

**Input objects:** A06_17_02 controlled no-position bridge setup, route-position
hidden states, router rows, feature labels, and snapshots.

**Computed variables:** per-feature centers, step-0 nearest boundary,
frozen-boundary distance, center drift, dynamic margin, current expert, and
switch flag.

**Algorithm stages:** rerun the A06_17_02 audit with added per-feature boundary
metrics; aggregate by seed, cell, condition, feature, and snapshot.

**Stage-local evidence:** boundary table, condition aggregate, drift-margin
scatter, switch table.

**Expected artifacts:** protocol, summary, detailed, `tables/boundary_by_step.csv`,
`tables/boundary_aggregate.csv`, and figures.

## 6. Minimal Falsification Test

**Test:** observed drift versus initial boundary buffer.

**Question:** does margin-buffer geometry explain observed feature preservation
or failure?

**Intervention / comparison:** compare pseudo-center, oracle-center, and
random Gaussian conditions across C0-C3 and 8 seeds.

**Primary metric:** maximum boundary consumption before final step, with
dynamic margin and switch flags as guards.

**Pass / fail / insufficient:** pass if preserved center-initialized cases keep
positive frozen distance and positive dynamic margin while random failures show
boundary or margin erosion. Fail if switches/margins contradict the boundary
metrics. Insufficient if router rows or feature centers cannot be reconstructed.

**Why it decides:** it tests the geometric limit implied by A06_17_02's
positive-margin explanation.

**Failure means:** failure weakens the margin-buffer model and points to router
compensation, common drift, or feature-cloud tails.

## 7. Current Evidence

**Observation:** A06_17_02 found perfect preservation for pseudo/oracle center
initialization, negative movement alignment, and positive final raw margins.

**Observation:** A06_17_03 full local two-GPU run
`a06_17_03_feature_drift_margin_boundary_full_20260629_011201` reran C0-C3
over 8 seeds with pseudo-center, oracle-center, and random Gaussian
conditions. Pseudo/oracle final feature NMI remained 1.0 with zero dynamic
switch rate. Their mean final boundary consumption was about 0.40, worst max
consumption was below 0.70, and worst dynamic margin stayed positive
(`1.838` for pseudo, `2.312` for oracle). Random Gaussian had mean feature NMI
0.783, negative mean dynamic margin, and switch rate 0.375.

**Interpretation:** preservation does not require active tracking because the
observed feature-center drift does not exhaust the step-0 boundary buffer. The
center stays inside both frozen and dynamic router regions.

**Boundary:** this quantifies only the observed training trajectory, not an
adversarial perturbation phase diagram or within-feature tail safety.

**Evidence links:**

- `../../experiments/A06/A06_17_02_router_center_tracking_preservation/summary.md`
- `../../experiments/A06/A06_17_03_feature_drift_margin_boundary/summary.md`
- `../../experiments/A06/A06_17_03_feature_drift_margin_boundary/detailed.md`

## 8. Claim Boundary And Next Decision

**Can claim:** in the controlled no-position bridge, observed preservation is
consistent with a finite margin-buffer boundary. Correct center initialization
creates enough step-0 boundary distance that observed center drift does not
cause expert switch.

**Cannot claim:** full perturbation limit, real-DCLM behavior, or utility.

**Next decision:** use boundary consumption and dynamic margin as design gates
for future label-free center search. A candidate center set should not advance
to preservation training unless it gives sufficient positive boundary buffer.
