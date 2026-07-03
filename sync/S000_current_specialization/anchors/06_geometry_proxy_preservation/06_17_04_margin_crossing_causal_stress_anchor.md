# A06_17_04: Margin Crossing Causal Stress Test

Document status: result-updated anchor. Static boundary crossing is supported;
the tested training stress lowers margin but does not cross the boundary.

## 0. Thinking Card

**Phenomenon:** A06_17_03 showed that successful center-initialized runs keep
feature centers inside the step-0 routing margin. That is observational: the
training trajectory did not naturally cross the boundary.

**Mechanism guess:** If margin is the real geometric protection mechanism,
then deliberately moving hidden states toward the nearest boundary, weakening
initial router margin, or increasing training drift should cause routing
failure once the margin buffer is consumed.

**Key variables:** feature center $\mu_f$, matched router row $w_{e(f)}$,
nearest competitor $w_{j^*(f)}$, boundary normal
$n_f=w_{e(f)}-w_{j^*(f)}$, initial boundary distance, perturbation strength,
router-row margin scale, training drift strength, feature switch, and
feature-route NMI.

**Causal relation:** Larger positive margin should tolerate more center drift.
When perturbation or training drift crosses the nearest router boundary,
matched feature routing should switch unless router movement compensates.

**Observable metric:** the primary metric is the crossing ratio:

$$
R_f=\frac{\lambda_f^{\mathrm{switch}}}
{d_f(0)+\epsilon},
\quad
d_f(0)=
\frac{(w_{e(f)}(0)-w_{j^*(f)}(0))^\top \mu_f(0)}
{\|w_{e(f)}(0)-w_{j^*(f)}(0)\|+\epsilon}.
$$

Here $\lambda_f^{\mathrm{switch}}$ is the smallest boundary-directed
perturbation that changes the routed expert for feature $f$.

**Rival Explanations:** margin is only correlated with success; feature-cloud
tails switch before the center; common or norm drift drives logits; router
rows compensate during training; weakened training success/failure is caused
by optimization noise rather than geometry.

**Decision:** static crossing supports margin as a geometric boundary. The
training stress remains insufficient because all stressed runs preserve
feature routing; the next step must force actual dynamic-margin crossing.

## 1. Problem Definition

**Parent problem:** why correct center initialization preserves feature routing
in the controlled no-position bridge.

**Sharper subproblem:** decide whether the positive margin observed in
A06_17_02 / A06_17_03 is a causal geometric boundary or only a correlated
diagnostic.

**Decision question:** Can we manufacture margin crossing, and does crossing
predict loss of feature-specialized routing?

**Not in scope:** real-DCLM semantic features, utility, RoPE behavior, or a
deployable initialization algorithm.

## 2. Physical Priors

**P1: Top-1 router boundaries are geometric switch surfaces.**  
For fixed router rows, the boundary between expert $e$ and expert $j$ is the
hyperplane where $(w_e-w_j)^\top h=0$.  
**False if:** boundary-directed perturbations do not change routing near the
predicted crossing point.

**P2: Initial margin is a finite safety budget.**  
Correct center initialization works because matched feature centers start far
enough from competing expert regions.  
**False if:** shrinking the initial margin does not reduce preservation under
the same training conditions.

**P3: Training drift tests whether the safety budget matters dynamically.**  
If larger hidden-state drift consumes the margin, weaker-margin runs should
fail earlier than stronger-margin runs.  
**False if:** training failure is independent of initial margin or boundary
consumption.

## 3. Falsifiable Hypotheses

**H1 static geometry calibration:** Boundary-directed perturbation switches the
matched feature near the predicted boundary distance.  
**Supported if:** $R_f$ concentrates near 1 for center-level routing, with
explainable deviations from feature-cloud tails.  
**Weakened if:** switch thresholds are far from the predicted boundary.

**H2 margin weakening:** Reducing the initial center-init margin lowers
training preservation.  
**Supported if:** smaller initial margins produce lower final feature-route
NMI, higher switch rate, or negative dynamic margins under the same training.  
**Weakened if:** margin scale has little relation to preservation.

**H3 drift amplification:** Increasing training drift breaks preservation
first in low-margin runs.  
**Supported if:** higher learning rate, longer training, or stronger nuisance
causes boundary consumption to approach or exceed 1 before route failure.  
**Weakened if:** drift grows but routing remains unrelated to margin.

## 4. Mathematical Model

**Boundary normal:**

$$
n_f(0)=w_{e(f)}(0)-w_{j^*(f)}(0).
$$

**Initial signed distance:**

$$
d_f(0)=
\frac{n_f(0)^\top\mu_f(0)}
{\|n_f(0)\|+\epsilon}.
$$

**Boundary-directed perturbation:**

$$
\mu_f(\lambda)=
\mu_f(0)-\lambda\frac{n_f(0)}{\|n_f(0)\|+\epsilon}.
$$

The fixed-row prediction is that routing switches when
$\lambda \approx d_f(0)$.

**Margin weakening options:**

$$
w_e^{\mathrm{weak}}(0)
=s\cdot \mathrm{normalize}\big((1-\alpha)c_e+\alpha r_e\big),
$$

where $c_e$ is the center-initialized row, $r_e$ is a random row,
$\alpha$ controls center corruption, and $s$ controls row norm.

**Training stress relation:** with training snapshots,

$$
B_f(t)=1-\frac{n_f(0)^\top\mu_f(t)}
{n_f(0)^\top\mu_f(0)+\epsilon}.
$$

Boundary-consumption explanation predicts failure as $B_f(t)$ approaches or
exceeds 1, guarded by dynamic margin
$M_f(t)=\min_{j\neq e(f)}(w_{e(f)}(t)-w_j(t))^\top\mu_f(t)$.

## 5. Computational Realization

**Base setup:** reuse the controlled no-position bridge from A06_17_02 /
A06_17_03: no learned absolute positional embedding, no B token, route on the
last token of the feature slot, and uniformly sampled feature slots.

**Test family 1: static crossing calibration.** Freeze trained or step-0
router rows, move feature centers or held-out route-position states along the
nearest boundary direction, and measure the first expert switch.

**Test family 2: margin weakening.** Start from pseudo-center or oracle-center
initialization, then reduce margin by row-norm scaling and/or mixing each row
with a random direction. Train under the same baseline setting.

**Test family 3: drift amplification.** Keep initialization fixed, then
increase drift pressure with limited, named knobs such as longer training,
higher learning rate, or stronger nuisance construction. This is a stress
test, not a new main training recipe.

**Stage-local evidence:** threshold table, switch curves, feature NMI curve,
boundary consumption curve, dynamic margin curve, and route heatmap.

## 6. Minimal Falsification Tests

**Primary test:** static boundary-directed crossing calibration.

**Why first:** it checks whether the margin metric is a valid geometric ruler
before using it to interpret training dynamics.

**Primary metric:** crossing ratio $R_f$.

**Pass:** routed expert switches near $R_f=1$ for most features, and deviations
are explainable by feature-cloud spread or competitor changes.

**Fail:** switches occur far before or far after the predicted boundary without
a clear geometric explanation.

**Insufficient:** router-feature matching, centers, or nearest competitors
cannot be reconstructed.

**Training stress follow-up:** if the static ruler passes, run a small
two-axis stress grid: margin weakening $\times$ drift amplification.

**Training decision metric:** final feature-route NMI and switch rate, guarded
by boundary consumption and dynamic margin.

## 7. Current Evidence

**A06_17_02:** correct pseudo/oracle center initialization preserves feature
NMI at 1.0 while active router-center movement alignment is negative. This
supports positive-margin preservation over active tracking.

**A06_17_03:** observed successful trajectories consume only part of the
initial boundary buffer and keep positive dynamic margins. This supports the
margin-buffer explanation for natural observed trajectories, but does not yet
show that crossing the boundary causes failure.

**A06_17_04 result:** full local two-GPU run
`a06_17_04_margin_crossing_full_20260629_1` executed C0-C3 over 4 seeds and
seven stress conditions. Static boundary-directed crossing passes: feature
centers switch near the predicted boundary, with mean center switch ratio
about `1.04-1.07`. Training stress does not create failure. All conditions
end with feature NMI `1.0` and zero dynamic switch rate. The strongest tested
stress, `pseudo_norm0p5_lr3x`, lowers final minimum dynamic margin to `0.701`
and raises max boundary consumption to `0.718`, but still does not cross the
boundary.

**Interpretation:** margin is a valid static geometric ruler in this setup.
The tested training stress moves in the predicted direction but is not strong
enough to manufacture margin crossing or preservation failure.

**Forced-crossing addendum:** rerun
`a06_17_04_forced_crossing_full_20260629_2` on two representative conditions
and post-hoc interpolated each matched router row toward its nearest
competitor. The mean first alpha where dynamic margin becomes negative is
`0.578`; the mean first alpha where feature NMI drops below `0.95` is `0.656`.
Matched-region preserve fraction drops from `1.000` at alpha `0.0` to about
`0.31` at alpha `0.75` and near zero by alpha `1.25`.

**Addendum interpretation:** explicit boundary crossing breaks the original
feature-to-expert preservation region. NMI alone is not sufficient because it
is permutation-invariant; preserve fraction is the identity-sensitive guard.

**Evidence links:**

- `../../experiments/A06/A06_17_04_margin_crossing_causal_stress/summary.md`
- `../../experiments/A06/A06_17_04_margin_crossing_causal_stress/detailed.md`
- `../../experiments/A06/A06_17_04_margin_crossing_causal_stress/tables/static_crossing_aggregate.csv`
- `../../experiments/A06/A06_17_04_margin_crossing_causal_stress/tables/condition_final_stress_aggregate.csv`

## 8. Claim Boundary And Next Decision

**Can claim:** in the controlled no-position bridge, positive margin is a
real geometric boundary: pushing feature centers toward the nearest router
boundary produces switches near the predicted distance, and forced router-row
crossing breaks the original feature-to-expert region.

**Cannot claim:** the exact training failure threshold, real-DCLM
preservation, semantic expert value, or a complete training-dynamics theory.

**Next decision:** move toward method design. The next minimal test should ask
whether label-free candidate centers can be accepted or rejected by their
initial positive margin before training, and whether insufficient-margin
candidates are exactly the ones that later fail preservation.
