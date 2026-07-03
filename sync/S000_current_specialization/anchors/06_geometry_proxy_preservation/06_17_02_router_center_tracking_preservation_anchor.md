# A06_17_02: Router-Center Tracking Preservation

Document status: post-result anchor update. The experiment supports
positive-margin preservation and weakens active center tracking in the
controlled A06 no-position bridge.

## 0. Thinking Card

**Phenomenon:** In A06_16 / A06_17, route-position pseudo-center or
oracle-center router initialization can keep feature routing clean through
training, while random-style initialization does not preserve the same clean
feature partition.

**Mechanism guess:** Good initialization may work because router rows either
actively track moving feature centers, or because the initial center rows give
each feature a positive routing margin that remains stable enough during
training.

**Key variables:** router row $w_e(t)$, route-position feature center
$\mu_f(t)$, common mean $c(t)$, common-centered center
$\tilde{\mu}_f(t)=\mu_f(t)-c(t)$, feature-route NMI, raw route margin, common
share, and row-norm growth.

**Causal relation:** If center initialization creates feature-specific router
regions with enough margin, the route partition can remain clean even when
router rows and feature centers move during training.

**Observable metric:** the primary active-tracking metric is
$A_{\mathrm{move}}(t)=\frac{1}{F}\sum_e
\cos(\Delta w_e(t),\Delta \tilde{\mu}_{\pi(e)}(t))$. The decisive preservation
guard is raw route margin at matched feature centers.

**Rival Explanations:** active center tracking; positive-margin preservation;
random rediscovery; common-direction or norm-growth drift; expert matching
artifact.

**Decision:** Active center tracking is weakened. The supported mechanism is
positive-margin preservation under correct center initialization.

## 1. Problem Definition

**Parent problem:** Can a discovered route-relevant proxy be turned into a
router initialization that survives early training?

**Sharper subproblem:** When good center initialization preserves the feature
partition, what geometric mechanism preserves it?

**Decision question:** Does the router preserve the partition by actively
tracking feature centers, or by maintaining positive feature-specific routing
margins?

**Not in scope:** real-DCLM behavior, semantic feature value, expert utility,
RoPE behavior, and deployable routing initialization.

## 2. Physical Priors

**P1:** Top-1 dot-product routers define cone-like regions in hidden-state
space.

**Meaning:** A feature is preserved when its route-position states remain
inside the same intended router region.

**Could be wrong if:** clean feature-route NMI remains high even when matched
feature centers have negative margins and no stable row-feature relation.

**P2:** Active tracking is stronger than preservation.

**Meaning:** The router can preserve a partition without moving in the same
direction as the feature-center drift.

**Could be wrong if:** preservation only occurs when $A_{\mathrm{move}}$ is
high and positive.

**P3:** Common or norm growth can fake raw logit improvement.

**Meaning:** margin evidence must be guarded by common share and row-norm
growth.

**Could be wrong if:** common / norm drift alone preserves feature NMI with the
same margin profile as correct center initialization.

## 3. Falsifiable Hypotheses

**H1 active tracking:** Router rows follow their matched common-centered
feature centers.

**Supported if:** center-initialized rows preserve feature NMI and have high
positive $A_{\mathrm{move}}$ without common / norm dominance.

**Weakened if:** feature NMI is preserved but $A_{\mathrm{move}}$ is low or
negative.

**Status:** weakened by A06_17_02.

**H2 positive-margin preservation:** Center initialization creates router
regions whose raw feature-center margins remain positive through training.

**Supported if:** center initialization keeps feature NMI at 1.0 and raw
margins positive, while random and shuffled guards do not.

**Weakened if:** random or shuffled guards reach the same margin and NMI
profile.

**Status:** supported by A06_17_02.

**H3 common / norm drift:** The apparent preservation is driven mostly by
common projection or row-norm growth.

**Supported if:** successful runs have high common share or norm growth that
explains margins better than matched feature-center evidence.

**Weakened if:** successful center runs have low common share and failed guards
have higher common dominance.

**Status:** weakened for the controlled bridge.

## 4. Mathematical Model

**Objects:**

- router row $w_e(t)$;
- route-position feature center $\mu_f(t)$;
- common mean $c(t)$;
- common-centered feature center $\tilde{\mu}_f(t)=\mu_f(t)-c(t)$;
- fixed step-0 row-feature matching $\pi(e)$.

**Core decomposition:**

$$
h_i(t)=c(t)+\tilde{h}_i(t),
\quad
\mu_f(t)=c(t)+\tilde{\mu}_f(t).
$$

**Mechanism relation:** Routing is preserved when the matched router row keeps
a positive margin over competing rows at the feature center:

$$
M_f(t)=\min_{j\neq \pi(f)}
(w_{\pi(f)}(t)-w_j(t))^\top \mu_f(t)>0.
$$

**Observable metrics:** feature-route NMI, $A_{\mathrm{move}}$, raw margin
$M_f(t)$, matched router-center dot product, common share, row-norm growth, and
matching stability.

**Falsifier:** feature-route NMI remains clean without positive margins,
without stable matching, or only through common / norm dominance.

## 5. Computational Realization

**Input objects:** A06 corrected no-position bridge runs with C0-C3 data cells,
center and guard initializations, and full training snapshots.

**Computed variables:** route-position hidden states, feature centers, common
mean, router rows, route logits, route assignments, margins, movement
alignment, common share, and norm growth.

**Algorithm stages:** run / load snapshots; compute centers and matching;
compute movement and margin metrics; compare center initialization against
random, equal-norm random, and shuffled-center guards.

**Stage-local evidence:** snapshot completeness, fixed-versus-per-step
matching, route heatmaps, feature NMI trajectories, movement trajectories,
margin trajectories, and common / norm guards.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`, trajectory
figures, and decision tables under
`experiments/A06/A06_17_02_router_center_tracking_preservation/`.

## 6. Minimal Falsification Tests

**Test:** Router-center preservation-mode classification.

**Question:** Which mechanism preserves clean feature routing after center
initialization?

**Intervention / comparison:** Compare pseudo-center and oracle-center
initialization against random Gaussian, equal-norm random, and label-shuffled
center guards across C0-C3 and 8 seeds.

**Primary metric:** $A_{\mathrm{move}}$ for active tracking, with raw route
margin as the decisive preservation guard.

**Pass / fail / insufficient:** Pass if one preservation mode separates center
initialization from guards. Fail if complete metrics contradict each other.
Insufficient if snapshots, route-position states, random guards, or matching
information are missing.

**Why it decides:** Active tracking predicts positive movement alignment.
Margin preservation predicts positive raw margins under correct center
initialization even if movement alignment is not positive.

**Failure means:** Failure would falsify the current operationalization of
preservation-mode classification, not necessarily the existence of route
geometry.

## 7. Current Evidence

**Observation:** In the full run
`a06_17_02_router_center_tracking_full_20260626_024804`, pseudo-center and
oracle-center initialization preserve feature NMI at 1.0 for all C0-C3 cells
and all 8 seeds.

**Interpretation:** Preservation is real in the controlled bridge, but it is
not active tracking. Pseudo-center final $A_{\mathrm{move}}$ averages -0.412
and oracle-center averages -0.398. Both keep positive raw route margins,
about 3.5 on average, while random and equal-norm random have negative final
margins.

**Boundary:** This result is controlled synthetic bridge evidence. It does not
prove real-DCLM preservation, expert utility, or semantic feature value.

**Evidence links:**

- [summary.md](../../experiments/A06/A06_17_02_router_center_tracking_preservation/summary.md)
- [detailed.md](../../experiments/A06/A06_17_02_router_center_tracking_preservation/detailed.md)
- [final_step_decision_table.csv](../../experiments/A06/A06_17_02_router_center_tracking_preservation/tables/final_step_decision_table.csv)

## 8. Claim Boundary And Next Decision

**Can claim:** In the corrected no-position A06 bridge, correct route-position
center initialization preserves feature routing through training by maintaining
feature-specific positive route margins. Active row-center tracking is not
supported.

**Cannot claim:** real-DCLM preservation, semantic features, utility, RoPE
behavior, or a general deployable method.

**Next decision:** Test whether label-free route-relevant states can be used
to initialize router rows with positive raw routing margins that remain
positive during early training.
