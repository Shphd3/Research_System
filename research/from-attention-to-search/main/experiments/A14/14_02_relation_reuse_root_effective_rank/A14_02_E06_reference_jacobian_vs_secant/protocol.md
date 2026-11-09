# Protocol: A14_02_E06 Reference Jacobian Versus Learned Secant

Primary anchor:
[A14_02 shared compositional rules and task-functional ROOT rank](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md)

Preceding evidence:
[E04 local Jacobian image](../A14_02_E04_shared_jacobian_path_image/protocol.md) and
[E05 trajectory closure](../A14_02_E05_trajectory_jacobian_closure/protocol.md).

## 0. Execution Snapshot

**Approval status:** Covered by the user's autonomous H9 execution
authorization.

**Purpose:** Make the final distinction required by the theorem: does the
reference-point Jacobian fail to share a context-stable image (H9), or does
the image exist locally while a single-point linearization fails to represent
the finite training displacement (H11)?

**Fresh development seed:** 120.

**Fresh confirmation seeds:** 20, 21, 22, 23, 24.

## 1. Reference-Point Construction

Use the same one-layer, one-head learned-common-mapping task and the same
eight-dimensional actual AdamW trajectory subspace \(G_{\mathrm{traj}}\) as
E05. At the capable endpoint, keep embeddings, norms, output head, and every
non-target parameter fixed at their final values, but revert the selected
Transformer block to its initialization. This hybrid is the registered
reference model \(\theta_{\mathrm{ref}}\).

This construction isolates the finite block displacement

\[
\Delta\theta
=
\theta_T^{\mathrm{block}}-\theta_0^{\mathrm{block}}
\]

without confounding it with simultaneous changes in the output head or
embeddings.

Compute:

\[
Z_x^{\mathrm{ref}}
=
J_\rho(x;\theta_{\mathrm{ref}})G_{\mathrm{traj}},
\]

the first-order prediction

\[
\widehat{\Delta h}(x)
=
Z_x^{\mathrm{ref}}
G_{\mathrm{traj}}^\top\Delta\theta,
\]

and the exact block secant

\[
\Delta h_{\mathrm{sec}}(x)
=
h_\rho(x;\theta_T)
-h_\rho(x;\theta_{\mathrm{ref}}).
\]

## 2. Metrics

**Reference H9 metrics:** \(\tau_J^2(8)\) and calibration-to-test capture for
\(Z_x^{\mathrm{ref}}\).

**H11 linearization error:**

\[
R_{\mathrm{lin}}
=
\frac{
\|\widehat{\Delta H}-\Delta H_{\mathrm{sec}}\|_F
}{
\|\Delta H_{\mathrm{sec}}\|_F
}.
\]

**Reference-image effect capture:** held-out energy of
\(\Delta H_{\mathrm{sec}}\) captured by the calibration reference-Jacobian
image.

**Functional linearization:** replay
\(h_{\mathrm{ref}}+\widehat{\Delta h}\) through the frozen final output head.

**Secant positive control:** fit an eight-dimensional image to calibration
\(\Delta H_{\mathrm{sec}}\), transfer it to final test, and replay

\[
h_{\mathrm{ref}}+
P_{\mathrm{sec}}\Delta h_{\mathrm{sec}}.
\]

This control must pass before a failure can be attributed to local
linearization rather than to a genuinely high-dimensional learned ROOT
effect.

## 3. Decision Rules

All seeds must pass E05 capability, block-relevance, trajectory-energy,
parameter-delta-capture, full-replay, and finite-difference guards.

**Reference H9 supported:** At least 4/5 eligible seeds have reference
Jacobian tail \(\le0.10\) and calibration-to-test capture \(\ge0.85\).

**Reference H9 refuted:** At least 4/5 eligible seeds have tail \(\ge0.25\) or
capture \(\le0.70\).

**H11 finite-displacement linearization refuted:** The secant positive control
passes in at least 4/5 eligible seeds, while at least 4/5 have one of:

- \(R_{\mathrm{lin}}\ge0.50\);
- reference image captures at most 0.70 of secant energy;
- linearized frozen-head replay excess CE \(\ge0.20\) or accuracy drop
  \(\ge0.05\).

The secant positive control requires tail \(\le0.10\), cross-context capture
\(\ge0.85\), excess CE \(\le0.05\), and accuracy drop \(\le0.02\).

**Complete reference closure supported:** Reference H9 is supported and at
least 4/5 have \(R_{\mathrm{lin}}\le0.20\), secant capture by the reference
image \(\ge0.85\), excess CE \(\le0.05\), and accuracy drop \(\le0.02\).

**Insufficient:** Fewer than four eligible seeds, failed secant positive
control, or intermediate results without four-seed agreement.

## 4. Claim Boundary

E06 decides whether the current one-layer theorem should use a point Jacobian
plus a small-displacement H11 assumption, or a finite learned secant /
path-integrated ROOT image. It cannot prove either object is low-dimensional
in natural language, multi-layer Transformers, or complete LLMs.

## 5. Post-Registered Rival Guard

After the registered verdict was frozen, one remaining rival was audited from
the saved confirmation checkpoints: the registered first-order prediction
uses \(G_{\mathrm{traj}}G_{\mathrm{traj}}^\top\Delta\theta\), so a small
trajectory-subspace residual might in principle have high ROOT gain. The
guard therefore computes the reference-point directional derivative along
the complete normalized block displacement and separately replays the
eight-dimensional projected-parameter model.

This audit reuses the same checkpoints and final-test split. It cannot alter
the registered E06 verdict or count as independent confirmation; it can only
exclude or retain the named out-of-subspace rival.
