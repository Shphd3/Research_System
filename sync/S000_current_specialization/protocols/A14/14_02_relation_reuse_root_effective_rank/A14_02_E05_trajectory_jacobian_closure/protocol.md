# Protocol: A14_02_E05 Trajectory Jacobian Closure

Primary anchor:
[A14_02 shared compositional rules and task-functional ROOT rank](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md)

Preceding evidence:
[A14_02_E04 shared Jacobian/path image](../A14_02_E04_shared_jacobian_path_image/protocol.md)

## 0. Execution Snapshot

**Approval status:** Covered by the user's 2026-07-25 authorization to run the
smallest follow-up needed for a decisive H9 judgment.

**Purpose:** Determine whether E04's supported local Jacobian image also
covers the parameter directions actually traversed during learning and the
causal ROOT update produced by those directions.

**Problem exposed by E04:** The final calibration-gradient subspace had a
shared eight-dimensional ROOT image in 5/5 seeds, but projecting the complete
final ROOT onto that image increased answer CE by 0.637 nats on average. H9 is
local and does not by itself guarantee that the probed $G_m$ contains the
training trajectory or that base/other-parameter ROOT components are small.

**Primary question:**

> If $G_{\mathrm{traj}}$ is defined from the actual first-block AdamW update
> increments, does it (a) retain the functionally relevant block update,
> (b) have a shared held-out ROOT Jacobian image, and (c) preserve the
> block-induced ROOT effect when only that effect is projected?

**Fresh development seed:** 110.

**Fresh confirmation seeds:** 10, 11, 12, 13, 14.

**No reused tuning surface:** E04 confirmation examples and seeds are not used
to change the E05 data generator, thresholds, or model. E05 uses the same
frozen generator family with fresh model seeds.

## 1. Registered Objects

During training, record the selected block's parameter vector every five
optimizer steps. Let

$$
u_t=\theta_{t+5}^{\mathrm{block}}-\theta_t^{\mathrm{block}}.
$$

The top eight right singular directions of the uncentered matrix with rows
$u_t^\top$ define $G_{\mathrm{traj}}$.

For the final capable checkpoint, compute

$$
Z_x=J_\rho(x;\theta_T)G_{\mathrm{traj}}
$$

in float64 with the E04-confirmed central-difference contract.

Let $\theta_{\mathrm{rev}}$ be the final model with only the selected block
reverted to initialization. Define its ROOT as $h_{\mathrm{rev}}(x)$ and the
exact finite training effect of that block as

$$
\Delta h_{\mathrm{block}}(x)
=h_T(x)-h_{\mathrm{rev}}(x).
$$

## 2. Primary Metrics

1. **Trajectory parameter capture**

$$
R_\theta
=
\frac{\|G_{\mathrm{traj}}G_{\mathrm{traj}}^\top
(\theta_T^{\mathrm{block}}-\theta_0^{\mathrm{block}})\|_2^2}
{\|\theta_T^{\mathrm{block}}-\theta_0^{\mathrm{block}}\|_2^2}.
$$

2. **Trajectory H9:** E04's frozen
$\tau_J^2(8)$ and calibration-to-test capture metrics, now using
$G_{\mathrm{traj}}$.

3. **Actual block-effect capture:** the fraction of
$\Delta h_{\mathrm{block}}$ captured on final test by the calibration
Jacobian image $\widehat B_J$.

4. **Base-preserving frozen-head replay**

$$
\widetilde h(x)
=h_{\mathrm{rev}}(x)
+\widehat B_J\widehat B_J^\top
[h_T(x)-h_{\mathrm{rev}}(x)].
$$

This intervention projects only the selected block's learned ROOT effect. It
does not incorrectly force the complete base ROOT into the Jacobian image.

5. **Parameter-space causal replay:** use the final model except replace the
selected block by

$$
\theta_0^{\mathrm{block}}
+G_{\mathrm{traj}}G_{\mathrm{traj}}^\top
(\theta_T^{\mathrm{block}}-\theta_0^{\mathrm{block}}).
$$

Report frozen-head answer CE and accuracy.

## 3. Guards

- Final model passes the same seen, held-out-combination, and nuisance
  consistency gates as E04.
- Reverting the selected block is causally nontrivial: answer CE rises by at
  least 0.10 nat or accuracy falls by at least 0.10.
- Top-eight trajectory-increment energy is at least 0.80.
- Central-difference disagreement is at most 0.05.
- Full final-state replay is exact to $10^{-6}$ CE.

## 4. Decision Rules

**Complete local closure supported:** At least 4/5 eligible seeds satisfy all
of:

- $R_\theta\ge0.80$;
- $\tau_J^2(8)\le0.10$;
- calibration-to-test Jacobian capture $\ge0.85$;
- actual block-effect capture by $\widehat B_J\ge0.85$;
- projected-parameter model answer excess CE $\le0.05$ and accuracy drop
  $\le0.02$;
- base-preserving ROOT replay excess CE $\le0.05$ and accuracy drop
  $\le0.02$.

**Local H9 refuted for the actual trajectory:** At least 4/5 eligible seeds
have Jacobian tail $\ge0.25$ or calibration-to-test capture $\le0.70$.

**Eight-dimensional trajectory closure refuted:** H9 itself can pass, but at
least 4/5 eligible seeds have one of:

- $R_\theta\le0.60$;
- actual block-effect capture $\le0.70$;
- projected-parameter excess CE $\ge0.20$ or accuracy drop $\ge0.05$;
- base-preserving ROOT excess CE $\ge0.20$ or accuracy drop $\ge0.05$.

**Insufficient:** Fewer than four eligible seeds, a failed numerical guard,
an irrelevant selected block, or all decisive quantities lying between the
support and refutation regions.

## 5. Interpretation Boundary

- E05 can establish or reject the local trajectory-to-ROOT closure for this
  one-layer model.
- If E04 H9 passes but E05 closure fails, the update is: a low-dimensional
  local final-gradient image exists, but it is not sufficient evidence that
  NTP training used one low-dimensional parameter/ROOT path.
- Even complete E05 support does not establish a general Transformer,
  natural-language, multi-layer, raw-state, or Router claim.
