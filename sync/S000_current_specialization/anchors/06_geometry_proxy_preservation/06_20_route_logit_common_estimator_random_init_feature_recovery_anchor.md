# A06_20: Route-Logit Common Estimator Under Random-Init Training

Document status: completed post-result anchor. This anchor is derived from
`daily_research_reports/0626/anchor_draft/A06_route_logit_common_estimator_random_init_feature_recovery_anchor_draft.md`.

## 0. Thinking Card

**Phenomenon:** In controlled A06, correct route-position centers can preserve
feature routing by positive margin, but label-free all-position methods often
fail to find those centers. One possible reason is that random-init training
creates routing-common directions that dominate expert load and hide feature
residual geometry.

**Mechanism guess:** The useful common component is not necessarily the global
mean or top hidden-state variance. It should be estimated by how much a
direction changes relative router logits or expert load.

**Key variables:** hidden state $h_i(t)$, router rows $W(t)$, relative route
logits, candidate common direction $v$, residualized state
$h_i'(t)=h_i(t)-P_C h_i(t)$, held-out route-position feature NMI, raw route
margin, expert load, and nuisance/position/frequency guards.

**Causal relation:** If a route-logit common estimator removes directions that
drive shared expert bias, then residualized hidden states should expose
feature-level centers better than raw, mean-subtracted, top-PC, or random
direction subtraction.

**Observable metric:** primary metric is improvement in held-out
route-position `feature_NMI` after subtraction:

$$
\Delta \mathrm{NMI}
=\mathrm{NMI}_{\mathrm{after\ subtract}}
-\mathrm{NMI}_{\mathrm{raw}}.
$$

**Rival Explanations:** generic PCA / role shortcut; load-only fix; random
router seed artifact; route-position selection rather than common estimation;
feature geometry already present or already erased.

**Decision:** The audit is complete. Park this route-logit common estimator as
a main path because it changes load but does not improve feature recovery.

## 1. Problem Definition

**Parent problem:** A06 asks how to find and preserve route-relevant
feature/proxy partitions for top-1 MoE routing.

**Sharper subproblem:** Determine whether routing-aware common subtraction can
make feature centers easier to discover under random-init training.

**Decision question:** Does a route-logit common estimator recover feature
residual geometry better than mean, top-PC, load-only, and random-direction
controls?

**Not in scope:** real-DCLM semantic features, expert utility, final
initialization method, RoPE, or long-run training preservation.

## 2. Physical Priors

**P1: Routing common is router-relative.**  
Meaning: the common direction that matters for routing is the direction that
changes relative expert logits or load, not necessarily the largest hidden
variance direction.  
Could be wrong if: top-PC or mean subtraction matches route-logit subtraction
on feature NMI and margin.

**P2: Load balance is not feature recovery.**  
Meaning: removing a direction can balance experts while still failing to
recover feature centers.  
Could be wrong if: load change reliably predicts feature NMI improvement
across seeds and checkpoints.

**P3: A valid common estimator must transfer across random seeds.**  
Meaning: a direction that works only for one random router is a router-seed
artifact, not a stable mechanism.  
Could be wrong if: seed-specific directions consistently improve held-out
feature readout without nuisance shortcuts.

## 3. Falsifiable Hypotheses

**H1 route-logit common removal:** A route-logit estimator reveals feature
residual geometry.

**Supported if:** it improves held-out route-position feature NMI and/or raw
route margins over raw, mean, top-PC, and random-direction controls across
seeds/checkpoints.

**Weakened if:** it improves only load, or does not beat top-PC/random
subtraction.

**Current status:** weakened. Route-logit subtraction has mean
$\Delta\mathrm{NMI}=-0.014$ and mean margin delta $-0.080$ versus raw
all-position clustering across 40 seed-checkpoint cases.

**H2 top-PC shortcut:** top hidden variance is mainly position/frequency/role
structure, not routing common.

**Supported if:** top-PC subtraction changes load but does not improve feature
NMI or margins.

**Current status:** partly supported as a negative control. Top-PC subtraction
does not solve feature recovery and has mean margin delta $-0.598$ versus raw.

**Weakened if:** top-PC subtraction matches or beats route-logit subtraction.

**H3 load-only confound:** load-sensitive directions are not enough.

**Supported if:** load ablation improves load balance without improving
feature NMI or route margin.

**Current status:** supported. Load-sensitive and route-logit directions change
expert load, but this does not imply feature NMI or margin improvement.

**Weakened if:** load-sensitive ablation and route-logit estimator both
improve feature readout.

## 4. Mathematical Model

**Objects:** hidden states $H_t=\{h_i(t)\}_{i=1}^N$, router matrix
$W_t\in\mathbb{R}^{E\times d}$, expert-centering matrix
$P_E=I-\frac{1}{E}\mathbf{1}\mathbf{1}^\top$, candidate unit direction $v$,
and selected common subspace $C_t$.

**Core decomposition:**

$$
h_i(t)=c_{\mathrm{route}}(t)+r_i(t)+\epsilon_i(t).
$$

The estimator observes only $H_t$ and $W_t$, not feature labels or route
position during fitting.

**Mechanism relation:** the relative-logit contribution of a one-dimensional
component $v$ is

$$
\Delta z_i(v;t)=
P_E W_t \left((v^\top h_i(t))v\right).
$$

The route-logit score is

$$
S_{\mathrm{logit}}(v;t)
=\operatorname{Var}_i(v^\top h_i(t))
\left\|P_E W_t v\right\|_2^2.
$$

High score means the direction has both hidden-state variation and relative
router sensitivity.

**Observable metrics:** held-out route-position feature NMI, route margin,
expert load, load-change under ablation, nuisance/position/frequency NMI, and
seed/checkpoint stability.

**Falsifier:** $S_{\mathrm{logit}}$ directions change load but do not improve
feature NMI or margins beyond controls.

## 5. Computational Realization

**Input objects:** controlled no-position A06 bridge snapshots under random
router initialization, including all-position hidden states, route-position
held-out states, router rows, feature labels for post-hoc audit, and nuisance /
position metadata for guards.

**Computed variables:** candidate common directions, selected common subspace,
residualized states, k-means centers, route assignments, feature NMI, margins,
load, and shortcut guards.

**Algorithm stages:** collect snapshots; compute candidate directions; select
route-logit common subspace without labels; subtract it; cluster residualized
calibration states; evaluate on held-out route-position states; compare against
controls.

**Stage-local evidence:** direction score table, load-change table,
feature-NMI table, route-margin table, nuisance guard table, and heatmaps.

**Artifacts:** `protocol.md`, `summary.md`, `detailed.md`,
`tables/estimator_comparison.csv`, `tables/direction_audit.csv`, and core
figures under `experiments/A06/A06_20_route_logit_common_estimator_random_init_feature_recovery/`.

## 6. Minimal Falsification Test

**Test:** Route-logit common estimator audit.

**Question:** Does routing-aware common subtraction reveal feature centers
better than non-routing common subtraction?

**Intervention / comparison:** raw all-position clustering, mean subtraction,
top-PC subtraction, random-direction subtraction, load-sensitive ablation, and
route-logit subtraction.

**Primary metric:** held-out route-position feature NMI improvement over raw.

**Pass / fail / insufficient:** Pass if route-logit subtraction improves
feature NMI or raw margin over all controls with nuisance guards clean. Fail if
it changes only load or matches controls. Insufficient if snapshots or router
rows are missing, or if fitting leaks feature/position/route labels.

**Why it decides:** the anchor claims a routing-aware common estimator, so the
estimator must improve feature readout, not just hidden variance or load.

**Failure means:** failure weakens this common-estimator operationalization,
not the existence of route-position feature geometry.

## 7. Current Evidence

**Observation:** A06_17_02 supports positive-margin preservation when correct
route-position centers are known.

**Observation:** A06_18 and A06_19 weaken generic all-position representation
and minimal-prior center search methods.

**Observation:** A06_20 full run used 8 seeds and checkpoints
`0, 5, 10, 100, 1600`. Route-only control remains high
(`feature_NMI=0.995` mean), so route-position feature geometry is present. But
route-logit subtraction does not improve recovery over raw all-position
clustering (`feature_NMI=0.815` versus raw `0.829`; mean
$\Delta\mathrm{NMI}=-0.014$). Mean subtraction is stronger than route-logit
subtraction (`feature_NMI=0.883`; mean $\Delta\mathrm{NMI}=+0.054$).

**Interpretation:** this operationalization estimates directions that are
router-relative and load-sensitive, but not feature-recovery directions. It
selects router-contrast directions in every seed-checkpoint case, so it is too
close to current-router load manipulation.

**Boundary:** this weakens the tested estimator, not the existence of feature
geometry and not every possible routing-aware common estimator.

**Evidence links:**

- `../../experiments/A06/A06_17_02_router_center_tracking_preservation/summary.md`
- `../../experiments/A06/A06_18_label_free_route_relevant_state_selector/summary.md`
- `../../experiments/A06/A06_19_minimal_prior_margin_aware_center_search/summary.md`
- `../../experiments/A06/A06_20_route_logit_common_estimator_random_init_feature_recovery/summary.md`
- `../../experiments/A06/A06_20_route_logit_common_estimator_random_init_feature_recovery/detailed.md`

## 8. Claim Boundary And Next Decision

**Can claim now:** in the controlled no-position bridge, the tested
route-logit common estimator does not expose feature residual geometry better
than raw all-position clustering or mean subtraction.

**Can also claim:** load-changing directions are not sufficient for feature
recovery; route-only positive control confirms that the feature geometry itself
is still present.

**Cannot claim:** real-DCLM semantic features, expert utility, final router
initialization, preservation under real language training, or that all
routing-aware estimators fail.

**Next decision:** do not continue this estimator as the main path. Return to
minimal-prior center selection that directly tests route-margin geometry
without feature labels or route-position labels, or redesign common estimation
so router-contrast directions cannot win solely by changing load.
