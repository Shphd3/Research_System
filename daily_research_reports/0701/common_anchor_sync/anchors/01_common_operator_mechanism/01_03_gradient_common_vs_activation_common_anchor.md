# Gradient Common Versus Activation Common Anchor

## 0. Thinking Card

**Phenomenon:** Activation top directions can be strong, stable, and visually
"common", but they may not be the directions that create cross-group
optimization interference.

**Mechanism guess:** Optimization-relevant common is closer to the intersection
of group-conditioned gradient outer products than to the top eigenspace of
hidden-state covariance.

**Key variables:** Hidden state $h$, group label $g$, activation covariance
$C_h$, group gradient $G_g$, activation projector $P_{\mathrm{act}}$,
gradient-intersection projector $P_{\mathrm{grad}}$, shared target loss $L_c$,
and gradient-overlap reduction.

**Causal relation:** If gradient common is the optimization object, removing
$P_{\mathrm{grad}}h$ should reduce cross-group gradient overlap more than
removing $P_{\mathrm{act}}h$, especially when high-variance activation
directions are nuisance or unique directions.

**Observable metric:** `gradient_overlap_reduction_advantage`, defined as
gradient-overlap reduction from $P_{\mathrm{grad}}$ minus that from
$P_{\mathrm{act}}$.

**Rival Explanations:** Activation PCA may already capture the same common
object; gradient intersection may only track target scale; estimator
disagreement may disappear when shared-prediction loss is guarded.

**Decision:** If $P_{\mathrm{grad}}$ consistently beats $P_{\mathrm{act}}$ on
gradient-overlap reduction in activation-gradient mismatch regimes, carry
gradient common into the next functional/feedback bridge. If not, revise the
optimization-common hypothesis.

## 1. Problem Definition

**Parent problem:** Common components may erase proxy routing and weaken expert
specialization, but the common operator must be mechanism-defined before a
method can use it.

**Sharper subproblem:** Decide whether the common operator relevant to
optimization interference is activation covariance common or cross-group
gradient common.

**Decision question:** Is optimization-relevant common better explained by
activation covariance or by cross-group gradient covariance?

**Not in scope:** Real-DCLM preservation rescue, final MoE architecture,
layerwise common role, or utility claims.

## 2. Physical Priors

**P1:** Activation energy and update interference are different physical
objects.

**Meaning:** A high-variance hidden-state direction can be irrelevant to
group-gradient overlap, and a low-variance shared direction can dominate
updates.

**Could be wrong if:** Activation PCA and gradient intersection produce the
same residualization effect across activation-gradient mismatch regimes.

**P2:** Functional shared common and harmful optimization common can differ.

**Meaning:** A direction can be useful for shared prediction but not be the
main source of redundant group updates.

**Could be wrong if:** The same projector maximizes shared-loss sensitivity and
gradient-overlap reduction in all regimes.

## 3. Falsifiable Hypotheses

**H1:** Gradient-intersection common better explains optimization interference.

**Supported if:** $P_{\mathrm{grad}}$ beats $P_{\mathrm{act}}$ on
`gradient_overlap_reduction` in most activation-gradient mismatch regimes.

**Weakened if:** $P_{\mathrm{act}}$ matches or beats $P_{\mathrm{grad}}$ on the
same metric.

**H2:** Useful shared common and gradient common are separable.

**Supported if:** A functional shared estimator wins shared-loss sensitivity
while $P_{\mathrm{grad}}$ wins gradient-overlap reduction in a split regime.

**Weakened if:** Functional and gradient criteria select the same projector in
all regimes.

## 4. Mathematical Model

**Objects:** Hidden state $h$, group label $g$, activation covariance $C_h$,
group-conditioned gradient $G_g$, and projectors
$P_{\mathrm{act}}$ and $P_{\mathrm{grad}}$.

**Activation common:**

$$
C_h=\mathbb{E}[hh^\top], \qquad
P_{\mathrm{act}}=U_k U_k^\top
$$

where $U_k$ are the top eigenvectors of $C_h$.

**Gradient common:**

$$
G_g=\mathbb{E}[\delta_g h^\top\mid g]
$$

$$
C_{\cap}=\frac{1}{|G|(|G|-1)}
\sum_{g\neq g'}G_g^\top G_{g'}
$$

$$
P_{\mathrm{grad}}=V_k V_k^\top
$$

where $V_k$ are the top positive directions of the symmetrized
$C_{\cap}$.

**Primary intervention:**

$$
G_g^r(P)=\mathbb{E}[\delta_g((I-P)h)^\top\mid g]
$$

and the decision metric compares:

$$
\Delta C(P)=\overline{\cos(G_g,G_{g'})}
-\overline{\cos(G_g^r(P),G_{g'}^r(P))}
$$

## 5. Computational Realization

**Input objects:** Controlled hidden states with separate activation nuisance,
functional shared, gradient common, and group-unique components.

**Computed variables:** Activation PCA projector, gradient-intersection
projector, functional shared projector, and random control.

**Algorithm stages:** Generate mismatch regimes; compute candidate projectors;
residualize hidden states; score gradient-overlap reduction and shared-loss
sensitivity; aggregate across seeds.

**Stage-local evidence:** Per-regime gradient advantage table, criterion winner
table, and figures showing optimization/common split.

**Expected artifacts:** `summary.md`, `detailed.md`,
`tables/gradient_vs_activation_scores.csv`,
`tables/gradient_vs_activation_summary.csv`, and
`figures/gradient_advantage_by_regime.png`.

## 6. Minimal Falsification Tests

**Test:** Activation-gradient mismatch audit.

**Question:** Does $P_{\mathrm{grad}}$ explain cross-group gradient overlap
better than $P_{\mathrm{act}}$ when high activation variance is nuisance,
unique, or functionally useful but not the optimization-interference object?

**Intervention / comparison:** Compare residualization by activation PCA,
gradient intersection, functional shared, and random projectors.

**Primary metric:** `gradient_overlap_reduction_advantage`.

**Pass / fail / insufficient:** Pass if $P_{\mathrm{grad}}$ beats
$P_{\mathrm{act}}$ in most mismatch regimes with stable seed win rate. Fail if
$P_{\mathrm{act}}$ matches or beats $P_{\mathrm{grad}}$ on the optimization
metric. Insufficient if random controls win or shared-loss guards show the
comparison is dominated by target destruction.

**Why it decides:** The next preservation bridge should use a gradient-common
estimator only if gradient common is distinct from activation common.

**Failure means:** The gradient-common route is weakened, not that common is
irrelevant.

## 7. Current Evidence

**Observation:** A01_01 showed estimator criterion dependence with
`criterion_winner_diversity = 4`, including gradient-intersection wins in
optimization-visible regimes. A01_03 then directly tested activation-gradient
mismatch regimes.

**Measured result:** `n_passed_mismatch_regimes = 4 / 4`. In
`activation_nuisance`, `unique_variance`, `functional_gradient_split`, and
`entangled_residual`, gradient intersection beats activation PCA on
`gradient_overlap_reduction_advantage` with seed win rate 1.0.

**Functional guard:** In `functional_gradient_split`, functional shared wins
`shared_loss_sensitivity` with 8.5791, while gradient intersection wins
`gradient_overlap_reduction` with 0.6494 and has near-zero shared-loss
sensitivity, 0.0037.

**Interpretation:** Optimization-common and useful shared common are separable
in the controlled audit. Gradient intersection should be carried into the next
bridge as the primary optimization-common estimator.

**Boundary:** Existing evidence is controlled and does not yet establish a
real-DCLM preservation mechanism.

**Evidence links:** See
`../../experiments/A01_common_operator/A01_01_common_operator_identifiability_full_run/summary.md`
and
`../../experiments/A01_common_operator/A01_03_gradient_common_vs_activation_common_full_run/summary.md`.

## 8. Claim Boundary And Next Decision

**Can claim:** Gradient common is the better estimator for
optimization-interference common in controlled activation-gradient mismatch
settings.

**Cannot claim:** A real-DCLM feedback common, a preservation rescue, a
layerwise rule, or a residualized MoE method.

**Next decision:** Write the functional/feedback bridge anchor with gradient
common as the primary optimization estimator and activation PCA as a rival
explanation.
