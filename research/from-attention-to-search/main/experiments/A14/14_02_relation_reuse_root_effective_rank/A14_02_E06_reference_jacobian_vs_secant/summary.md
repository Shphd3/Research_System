---
experiment_id: A14_02_E06_reference_jacobian_vs_secant
status: completed_decisive
verdict: h11_finite_displacement_linearization_refuted
confirmation_seeds: [20, 21, 22, 23, 24]
companion_cn: summary_cn.md
---

# Summary: A14_02_E06 Reference Jacobian Versus Learned Secant

Primary anchor:
[A14_02 task-functional ROOT rank](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md)

Protocol: [protocol.md](protocol.md)

## Direct Result

**H11's finite-displacement single-point linearization is decisively refuted
in 5/5 eligible seeds.** The exact learned block secant passes the registered
eight-dimensional cross-context and frozen-head controls in all five seeds,
while the reference-point Jacobian prediction has mean relative error
\(1.2595\) and captures only \(0.2935\) of the secant energy.

Reference-point H9 itself is **intermediate**, not refuted: one seed met the
strict support thresholds, none met refutation thresholds. Its mean
eight-direction tail was \(0.1546\) and mean calibration-to-test capture was
\(0.8454\). The decisive failure is therefore the attempted use of one local
image across a large training displacement.

## Primary Results

| Object / test | Mean | Bootstrap 95% interval | Verdict |
| --- | ---: | ---: | --- |
| Reference Jacobian tail beyond 8 | 0.1546 | [0.1123, 0.1892] | Intermediate H9 |
| Reference cal-to-test capture | 0.8454 | [0.8108, 0.8877] | Intermediate H9 |
| Exact secant tail beyond 8 | 0.0171 | [0.0060, 0.0292] | Pass |
| Exact secant cal-to-test capture | 0.9829 | [0.9708, 0.9940] | Pass |
| Secant captured by reference image | 0.2935 | [0.2369, 0.3503] | Refute closure |
| Point-linearization relative error | 1.2595 | [0.9532, 1.5659] | Refute H11 |
| Linearized replay excess CE | 0.4797 nat | [0.1259, 0.8872] | Functionally consequential |
| Secant-image replay excess CE | 0.00022 nat | [0.00002, 0.00046] | Positive control pass |

A post-registered rival audit used the same saved checkpoints and the
**complete**, unprojected block displacement. Its mean linearization relative
error remained \(1.2441\), and all 5/5 seeds still refuted H11. The
eight-dimensional projected-parameter models preserved function in 5/5 seeds
with mean excess CE \(0.00180\) nat. This excludes the small trajectory-subspace
residual as the cause of the H11 result. Because it reuses the same checkpoints
and test split, it strengthens rival separation but is not independent
confirmation and does not change the registered verdict.

## Central Figure

![Reference Jacobian, learned secant, and finite-displacement error](figures/reference_jacobian_vs_secant.png)

The exact learned secant is consistently more concentrated and transferable
than the reference-point Jacobian image. The right panel shows every seed
above the frozen H11 refutation threshold.

## Theory Update

For the target block, define the line path

\[
\theta(t)=\theta_{\mathrm{ref}}+t\Delta\theta,
\qquad 0\le t\le1.
\]

Differentiability gives the exact identity

\[
\Delta h_{\mathrm{sec}}(x)
=
h_\rho(x;\theta_T)-h_\rho(x;\theta_{\mathrm{ref}})
=
\int_0^1
J_\rho(x;\theta(t))\Delta\theta\,dt.
\]

E06 shows that this integrated finite effect has a shared low-dimensional
image even though \(J_\rho(x;\theta_{\mathrm{ref}})\Delta\theta\) does not
approximate it. The finite-training theorem should therefore use a
calibration-identifiable **secant/path-integrated image**:

\[
\Delta h_{\mathrm{sec}}(x)
=
B_m^{\mathrm{sec}}a_x+e_x^{\mathrm{sec}},
\qquad
\dim\operatorname{Col}(B_m^{\mathrm{sec}})\le q,
\]

and retain point H9 plus H11 only as a genuinely local corollary.

## Claim Boundary

Allowed:

> In this controlled one-layer NTP model, local cross-context image sharing,
> an effectively eight-dimensional optimizer displacement, and a
> cross-context low-dimensional finite ROOT effect all occur. A single
> reference or endpoint Jacobian does not identify the finite effect because
> the local linearization remainder is large.

Not allowed: NTP generally guarantees a low-dimensional secant; every point
along the path shares one fixed basis; natural-language or multilayer
Transformers satisfy the finite-image condition; or low rank implies Router
utility.

## Exactly One Next Decision

Rewrite the finite-training branch of the theory around the secant /
path-integrated image, while retaining the point-Jacobian theorem only for
updates with an explicitly measured small remainder.
