# Common Operator Identifiability Anchor

## 0. Thinking Card

**Phenomenon:** Common components affect routing, rare/common conflict, and
early training preservation, but PCA, mean, centering, route-logit contrast,
and gradient-based estimators can name different directions.

**Mechanism guess:** A common operator is not identifiable from hidden-state
geometry and next-token loss alone. It must be defined relative to a mechanism
criterion such as shared-prediction causality, cross-group gradient redundancy,
or proxy-preservation feedback.

**Key variables:** Hidden state $h$, group label $g$, candidate projector $P$,
shared loss $L_c$, rare/group loss $L_r$, group gradient $G_g$, and criterion
rankings across estimator families.

**Causal relation:** If common is criterion-dependent, then the estimator that
best explains activation variance need not be the estimator that best reduces
gradient redundancy or preserves route information.

**Observable metric:** `criterion_winner_diversity`, the number of distinct
estimator families that win across recovery, shared-loss sensitivity, and
gradient-overlap reduction criteria.

**Rival Explanations:** A single hidden-state top direction may dominate every
criterion; estimator disagreement may be caused only by noise or invalid group
labels; gradient criteria may measure update scale rather than common
structure.

**Decision:** If multiple estimator families win different mechanism criteria
in a controlled full run, pursue common as a mechanism-conditioned operator
family. If one estimator wins all criteria across regimes, revise toward a
single common operator route.

## 1. Problem Definition

**Parent problem:** Expert specialization fails when common components, wrong
hidden-state populations, or early-training feedback dominate routing and
optimization.

**Sharper subproblem:** Before designing a common/residual method, decide
whether "common" is a single geometric object or a mechanism-conditioned
operator family.

**Decision question:** Can a common operator be selected from hidden-state
geometry and loss alone, or do different mechanism criteria select different
operators?

**Not in scope:** Proving a residualized MoE method, proving real-DCLM semantic
experts, or selecting a final layerwise estimator.

## 2. Physical Priors

**P1:** Hidden-state variance and optimization influence are not equivalent.

**Meaning:** A direction can have large activation energy without dominating
cross-group gradient updates.

**Could be wrong if:** Activation top directions also dominate shared loss,
gradient overlap, and preservation criteria in every controlled regime.

**P2:** Next-token loss does not identify a unique shared/residual functional
decomposition.

**Meaning:** Shared and routed branches can exchange function mass while
leaving their sum unchanged.

**Could be wrong if:** All valid criteria select the same operator and branch
exchange does not create estimator ambiguity in controlled settings.

## 3. Falsifiable Hypotheses

**H1:** Common is criterion-dependent.

**Supported if:** Different estimator families win different mechanism
criteria in controlled regimes with known $P_c^*$.

**Weakened if:** One estimator family consistently wins recovery,
shared-loss sensitivity, and gradient-overlap reduction.

**H2:** Gradient common is a distinct optimization object.

**Supported if:** Gradient-intersection projectors reduce cross-group gradient
overlap more than activation PCA even when activation PCA has higher variance
or recovery alignment.

**Weakened if:** Activation PCA and gradient-intersection projectors are
functionally equivalent across regimes.

## 4. Mathematical Model

**Objects:** Hidden state $h$, true common subspace $P_c^*$ in controlled runs,
candidate projector $P$, group-conditioned target residual $\delta_g$, and
group gradient $G_g$.

**Core decomposition:**

$$
h = c + u_g + \epsilon
$$

where $c=P_c^*h$ in the controlled positive case.

**Mechanism relation:**

$$
G_g = \mathbb{E}[\delta_g h^\top \mid g]
$$

and residualizing a candidate common operator gives:

$$
G_g^r(P)=\mathbb{E}[\delta_g ((I-P)h)^\top \mid g]
$$

**Observable metrics:** Subspace recovery alignment, shared-loss sensitivity,
rare-loss sensitivity, and gradient-overlap reduction.

**Falsifier:** A single candidate projector dominates all mechanism criteria
across nuisance regimes.

## 5. Computational Realization

**Input objects:** Synthetic hidden states with known $P_c^*$, group labels,
shared targets, rare targets, and simulated feedback drift.

**Computed variables:** Candidate projectors from activation PCA, group means,
gradient intersection, feedback drift, and random controls.

**Algorithm stages:** Generate regimes; estimate projectors; compute recovery,
loss-sensitivity, and gradient-overlap metrics; rank projectors by criterion.

**Stage-local evidence:** Per-regime criterion winner table and aggregate
winner diversity.

**Expected artifacts:** `summary.md`, `detailed.md`,
`tables/operator_criterion_scores.csv`, and
`figures/operator_rank_disagreement.png`.

## 6. Minimal Falsification Tests

**Test:** Controlled criterion disagreement audit.

**Question:** Do different mechanism criteria select different common
estimators?

**Intervention / comparison:** Compare activation PCA, group mean,
gradient-intersection, feedback-drift, and random projectors across controlled
regimes with known $P_c^*$.

**Primary metric:** `criterion_winner_diversity`.

**Pass / fail / insufficient:** Pass if more than one estimator family wins
across the main criteria in multiple regimes. Fail if one estimator wins all
criteria across regimes. Insufficient if metric rankings are unstable across
seeds or the synthetic task does not create measurable common signal.

**Why it decides:** A common/residual method needs to know which mechanism its
common operator is estimating.

**Failure means:** The criterion-dependence model is weakened, not that common
is irrelevant.

## 7. Current Evidence

**Observation:** Prior A05/A06/A07 records show common-related failure and
interference, but estimator definitions differ across studies. The controlled
A01_01 full run now adds a positive-control audit with known $P_c^*$.

**Measured result:** `criterion_winner_diversity = 4`. Activation PCA, group
mean, gradient intersection, and feedback drift each win at least one primary
criterion across the controlled regimes.

**Interpretation:** The single-estimator route is weakened in the controlled
setting. Common should be treated as a mechanism-conditioned operator family,
not as a criterion-free hidden-state direction.

**Boundary:** This evidence identifies criterion dependence in synthetic
positive controls only. It does not identify the real-DCLM common operator or
prove a residualized MoE method.

**Evidence links:** See
`../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/summary.md`
and
`../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/detailed.md`.

## 8. Claim Boundary And Next Decision

**Can claim:** In the controlled full run, common is not identified by one
universal estimator. Different mechanism criteria select different operators.

**Cannot claim:** A final estimator, a real-DCLM common operator, or a working
residualized MoE method.

**Next decision:** Start `01_03_gradient_common_vs_activation_common_anchor.md`
to decide whether the optimization-relevant common in project evidence is
closer to activation covariance or gradient covariance.
