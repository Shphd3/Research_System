---
experiment_id: A14_02_E04_shared_jacobian_path_image
status: completed_supported
verdict: supported_registered_local_h9
confirmation_seeds: [0, 1, 2, 3, 4]
companion_cn: summary_cn.md
---

# Summary: A14_02_E04 Shared Jacobian / Path Image

Primary anchor:
[A14_02 task-functional ROOT rank](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md)

Protocol: [protocol.md](protocol.md) · [中文协议](protocol_cn.md)

## Direct Result

**The registered local H9 operationalization is supported in 5/5 eligible
seeds.** For the calibration-estimated eight-dimensional task-gradient
subspace \(G_m\), the held-out ROOT Jacobian image had:

- mean spectral tail beyond eight directions \(0.0393\), bootstrap 95% interval
  \([0.0259,0.0500]\);
- mean calibration-to-test captured energy \(0.9607\), bootstrap 95% interval
  \([0.9500,0.9741]\).

Every seed passed capability, finite-difference, positive-control, and
negative-control gates. The result supports a context-shared **local** ROOT
image at the trained checkpoint:

\[
J_\rho(x;\theta_T)G_m
\approx
B_mA_x,
\qquad
\dim\operatorname{Col}(B_m)\le 8.
\]

It does not show that this image contains the complete final ROOT state or the
finite effect accumulated over training.

## Key Comparisons

| Probe | Mean tail beyond 8 | Mean held-out capture | Interpretation |
| --- | ---: | ---: | --- |
| Trained task-gradient \(G_m\) | 0.0393 | 0.9607 | Registered H9 support |
| Trained random \(G\) | 0.2206 | 0.7794 | Sharing is not generic to any parameter subspace |
| Initialization task \(G_m\) | 0.1421 | 0.8577 | Training sharpened the shared image |

The trained per-example task gradients placed mean \(0.9681\) of their energy
in the top eight parameter directions. Mean finite-difference disagreement
was \(0.0113\), below the frozen \(0.05\) numerical gate.

## Central Figure

![Held-out Jacobian tail and cross-context transfer](figures/jacobian_tail_and_transfer.png)

The left panel measures energy outside the best eight-dimensional held-out
ROOT image; the right panel measures how much held-out energy is captured by
the calibration image. Green and red lines are the frozen support and
refutation thresholds.

## Functional And Gauge Boundary

The frozen answer-contrast head saw only mean \(0.3617\) of total Jacobian
energy; \(0.6383\) lay in its null space. Nevertheless, the null component also
had a low mean eight-direction tail of \(0.0313\). Thus the result is not merely
the rank-seven answer-contrast bottleneck.

Projecting the **complete final ROOT** onto the local Jacobian image increased
answer CE by \(0.6367\) nat on average and reduced accuracy by \(0.0357\). This is
not a contradiction: H9 describes the image of selected infinitesimal
parameter directions, not the base ROOT, other parameter blocks, or a finite
training trajectory.

## Claim Boundary

Allowed:

> In this one-layer, one-head learned-common-mapping NTP model, the trained
> calibration task-gradient directions induced a shared eight-dimensional
> local ROOT Jacobian image across held-out nuisance contexts.

Not allowed: a full-training parameter-to-ROOT bridge; low rank of the
complete ROOT; a natural-language or multilayer H9 theorem; or Router utility.

## Exactly One Next Decision

Test whether an eight-dimensional subspace estimated from the actual optimizer
trajectory both preserves the learned block update and maps the finite
block-induced ROOT effect into the endpoint Jacobian image.

