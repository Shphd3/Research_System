# A06_21: Margin-Budget Preservation Audit

Document status: completed post-result anchor. Derived from
`daily_research_reports/0630/docs/A06_preservation_margin_budget_mini_anchor.md`
and `daily_research_reports/0630/docs/margin_budget_math_model_derivation.md`.

## 0. Thinking Card

**Phenomenon:** Feature/proxy-center initialization can create clean top-1 MoE
routing at step 0, and controlled A06 center initialization can preserve it,
but real-DCLM proxy routing is erased by early ordinary training.

**Mechanism guess:** Preservation is a margin-budget problem. The initial
router margin must be large enough to absorb training-induced movement of
router decision boundaries, feature centers, and common/dense directions.

**Key variables:** feature center $\mu_f(t)$, router row $w_e(t)$, pairwise
gap $u_{f,e}(t)=w_{a(f)}(t)-w_e(t)$, pairwise margin
$\gamma_{f,e}(t)=u_{f,e}(t)^\top \mu_f(t)$, initial margin
$\gamma_{f,e}(0)$, drift terms, common center $c(t)$, residual center
$r_f(t)=\mu_f(t)-c(t)$, feature-route NMI, and sign flip rate.

**Causal relation:** If early training consumes the initial margin, then
feature centers cross expert decision boundaries and route NMI falls. If the
margin stays positive, the original partition is preserved even if router rows
do not actively track feature centers.

**Observable metric:** primary metric is feature/proxy-route NMI at steps 5
and 10. Mechanism metrics are margin consumption ratio, sign flip rate, drift
attribution terms, and common/residual margin terms.

**Rival Explanations:** proxy labels unstable; step-0 bridge weak; feature
center drift dominates; router boundary drift dominates; common direction
overwrites residual feature margin; token spread crosses the boundary before
centers do; expert feedback breaks assignment even when center margins look
safe.

**Decision:** Supported for the controlled no-position bridge. Center
initialization preserves because current and cluster-aware margins stay
positive with zero sign flips. The next decision is whether the same
decomposition explains real-DCLM proxy-init failure.

## 1. Problem Definition

**Parent problem:** A06 asks how route-relevant feature/proxy partitions can be
found and preserved for top-1 MoE gating.

**Sharper subproblem:** Explain why a step-0 feature/proxy partition is
preserved in the controlled no-position bridge but erased in harder or real
early-training settings.

**Decision question:** Can early preservation or collapse be explained by the
initial routing margin being consumed by measurable training drift?

**Not in scope:** semantic feature identity, expert utility, long-run scaling,
or a new initialization method.

## 2. Physical Priors

**P1: Top-1 routing is decision-region assignment.**  
Meaning: a router partitions hidden-state space by pairwise logit gaps.  
Could be wrong if: route NMI changes without any center-level or token-level
decision-region crossing.

**P2: Initial alignment is insufficient without positive margin.**  
Meaning: a correct step-0 assignment can be fragile if the nearest competitor
margin is small.  
Could be wrong if: low-margin assignments preserve as reliably as high-margin
assignments under the same drift.

**P3: Feature and common components jointly determine router logits.**  
Meaning: $\mu_f(t)=c(t)+r_f(t)$, and a router can become dominated by
$u^\top c$ even when residual feature structure remains.  
Could be wrong if: common/residual terms do not separate preserved and failed
conditions better than raw margin alone.

## 3. Falsifiable Hypotheses

**H1 margin-buffer hypothesis:** Successful preservation requires initial
margins to exceed the measured drift budget.  
Supported if: preserved conditions have low consumption ratio and no sign
flips, while failed conditions have high consumption ratio or sign flips.  
Weakened if: NMI collapses while consumption is low and cluster-aware margins
remain positive.

Current status: supported for the controlled bridge. Pseudo-center and
oracle-center have NMI `1.0`, positive margins, zero sign flips, and positive
cluster-aware margins across training.

**H2 router-side drift hypothesis:** Failure is caused mainly by movement of
router decision boundaries.  
Supported if: $\Delta u_{f,e}(t)^\top \mu_f(0)$ is the dominant negative term
when NMI falls.  
Weakened if: router drift is small or does not reduce the relevant margins.

Current status: weakened for controlled center-init preservation. Router drift
is not the main negative pressure in preserved pseudo/oracle runs.

**H3 feature-center drift hypothesis:** Failure is caused mainly by hidden
feature centers moving relative to fixed router gaps.  
Supported if: $u_{f,e}(0)^\top \Delta \mu_f(t)$ dominates margin loss.  
Weakened if: feature centers move but not toward margin loss.

Current status: partially supported as the main negative pressure in preserved
center-init runs, but not sufficient for collapse because the positive margin
buffer remains large.

**H4 common overwrite hypothesis:** Failure is caused by common/dense
directions overwhelming residual feature margins.  
Supported if: common terms grow while residual feature terms shrink or become
insufficient, with load concentration and NMI drop.  
Weakened if: common share stays low and residual margins still fail.

Current status: not supported as the explanation for successful center-init
preservation in this controlled bridge. Center-init common share remains low.
Guard conditions have higher common share, but they already lack a valid
positive-margin partition.

## 4. Mathematical Model

**Objects:** hidden state $h_i(t)$, feature label $y_i=f$, feature center
$\mu_f(t)=\mathbb{E}[h_i(t)\mid y_i=f]$, router row $w_e(t)$, initial assigned
expert $a(f)$, and pairwise gap

$$
u_{f,e}(t)=w_{a(f)}(t)-w_e(t).
$$

**Core decomposition:**

$$
\gamma_{f,e}(t)
=
\gamma_{f,e}(0)
+
\Delta u_{f,e}(t)^\top \mu_f(0)
+
u_{f,e}(0)^\top \Delta \mu_f(t)
+
\Delta u_{f,e}(t)^\top \Delta \mu_f(t).
$$

**Mechanism relation:** preservation requires $\gamma_{f,e}(t)>0$ for all
competitors. A sufficient norm-budget guard is

$$
\gamma_{f,e}(0) >
\|\Delta u_{f,e}\|\|\mu_f(0)\|
+\|u_{f,e}(0)\|\|\Delta\mu_f\|
+\|\Delta u_{f,e}\|\|\Delta\mu_f\|.
$$

For token-level robustness, include feature radius $\rho_f(t)$:

$$
\tilde{\gamma}_{f,e}(t)
=
\gamma_{f,e}(t)-\|u_{f,e}(t)\|\rho_f(t).
$$

**Common/residual split:**

$$
\gamma_{f,e}(t)=u_{f,e}(t)^\top c(t)+u_{f,e}(t)^\top r_f(t).
$$

**Observable metrics:** feature-route NMI, pairwise sign flip rate, initial
margin, actual margin consumption, norm-bound consumption ratio,
cluster-aware margin, and common/residual margin terms.

**Falsifier:** NMI collapse or preservation does not track any center-level,
token-level, or common/residual margin quantity.

## 5. Computational Realization

**Input objects:** controlled no-position A06 bridge training snapshots with
route-position hidden states, fixed feature labels, router rows, route
assignments, loss, and expert load.

**Computed variables:** feature centers, common center, residual centers,
initial feature-to-expert matching, pairwise margins, drift terms, consumption
ratios, token radius, cluster-aware margins, sign flips, and NMI.

**Algorithm stages:** train/evaluate existing A06 bridge conditions; collect
checkpoint states; compute pairwise decomposition; aggregate by condition,
step, seed, and cell; render trajectory/scatter/attribution figures.

**Stage-local evidence:** per-pair decomposition table, per-step aggregate
table, final-step decision table, drift attribution table, common/residual
table, and central figures.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`, tables
under `experiments/A06/A06_21_margin_budget_preservation_audit/tables/`, and
figures under `figures/`.

## 6. Minimal Falsification Tests

| Test | Question | Primary metric | Pass / fail / insufficient | Failure means |
|---|---|---|---|---|
| Margin-budget audit | Does consumption explain preservation/collapse? | feature-route NMI at step 5/10 plus sign flip rate | Pass if high NMI aligns with low consumption and no sign flips; fail if not; insufficient if snapshots are missing. | Weakens H1 or exposes missing token/objective factor. |
| Drift attribution | Which term consumes margin? | negative contribution share by drift term | Pass if one term explains margin loss pattern; fail if terms do not align with NMI. | Revises H2/H3 or requires coupled-feedback model. |
| Common/residual audit | Is common direction overwriting residual feature margin? | common term, residual term, common share, load | Pass if common growth coincides with NMI drop or fragile margin; fail if not. | Weakens H4 for this bridge. |

## 7. Current Evidence

**Observation:** A06_17_02 shows controlled center initialization preserves
feature routing but does not support active router-center tracking.

**Observation:** A06_17_03 shows successful center-init runs stay inside the
initial boundary buffer.

**Observation:** A06_17_04 shows margin is a real geometric switch boundary.

**Observation:** A06_17_05 shows there is a wide positive-margin basin around
pseudo centers.

**Observation:** A06_12 shows real-DCLM proxy-center initialization is erased
by step 5/10 under ordinary training.

**Observation:** A06_21 full run completed 8 seeds x C0-C3 x 5 conditions x
12 checkpoints. The decomposition identity error is at most `1.37e-6`.

**Observation:** At step 10, pseudo-center and oracle-center have NMI `1.0`,
zero sign flips, positive min margins (`5.688` and `5.771`), and positive
cluster-aware margins (`4.532` and `4.537`). Random and equal-norm random have
negative min margins (`-1.394` and `-1.420`) and sign flip rate `0.229`.
Label-shuffled center has moderate NMI (`0.869`) but poor matched preserve
fraction (`0.094`) and negative margin (`-0.685`).

**Observation:** At final step 1600, pseudo-center and oracle-center still
have NMI `1.0`, zero sign flips, and positive margins (`3.555` and `3.726`).
Random/equal-norm random remain lower NMI with sign flip rate `0.320` and
negative margins.

**Interpretation:** In the controlled bridge, true preservation is best read
through positive current margin, zero sign flips, and positive cluster-aware
margin. NMI alone is insufficient because label-shuffled center can retain
moderate NMI while failing matched identity preservation.

**Boundary:** A06_21 explains controlled bridge preservation. It does not yet
explain real-DCLM proxy-init failure.

**Evidence links:**

- `../../experiments/A06/A06_21_margin_budget_preservation_audit/summary.md`
- `../../experiments/A06/A06_21_margin_budget_preservation_audit/detailed.md`

## 8. Claim Boundary And Next Decision

**Can claim now:** in the controlled no-position bridge, center-init
preservation is explained by positive current and cluster-aware margins
surviving training drift. Feature-center drift consumes margin, but does not
cause collapse unless it exhausts the buffer.

**Cannot claim now:** margin-budget decomposition already explains real-DCLM
failure, common subtraction solves preservation, NMI proves utility, or
synthetic feature partitions are semantic experts.

**Next decision:** apply the same margin-budget audit to real-DCLM A06_12
proxy-init training. Decide whether real-DCLM failure comes from weak step-0
residual margin, early margin consumption, common overwrite, token spread, or
objective feedback.
