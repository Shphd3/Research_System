---
experiment_id: A14_02_E05_trajectory_jacobian_closure
status: completed_refuted
verdict: eight_dimensional_trajectory_closure_refuted
confirmation_seeds: [10, 11, 12, 13, 14]
companion_cn: summary_cn.md
---

# Summary: A14_02_E05 Trajectory Jacobian Closure

Primary anchor:
[A14_02 task-functional ROOT rank](../../../../problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor.md)

Protocol: [protocol.md](protocol.md)

## Direct Result

**The eight-dimensional endpoint-Jacobian closure is refuted in 4/5 eligible
seeds.** The actual optimizer trajectory is low-dimensional and functionally
sufficient, and the learned block's exact ROOT effect is also
cross-context low-dimensional. However, the endpoint Jacobian image captures
only \(0.3672\) of that exact effect on average.

This separates three statements:

1. the selected block's finite parameter displacement is almost entirely
   eight-dimensional: mean capture \(0.9975\);
2. the block's exact learned ROOT effect has mean eight-direction tail
   \(0.0132\) and mean calibration-to-test capture \(0.9868\);
3. the endpoint image \(J_\rho(x;\theta_T)G_{\mathrm{traj}}\) has mean tail
   \(0.1555\) and captures only \(0.3672\) of the exact effect.

The low-dimensional phenomenon survives. What fails is identifying the finite
learned effect with a single endpoint Jacobian image.

## Causal And Functional Checks

| Check | Mean result | Reading |
| --- | ---: | --- |
| Top-8 parameter-delta capture | 0.9975 | Actual block displacement is effectively 8D |
| Projected-parameter excess CE | 0.00026 nat | Eight directions preserve the learned function |
| Block reversion excess CE | 1.3965 nat | The selected block is causally relevant |
| Exact block-effect tail beyond 8 | 0.0132 | Finite ROOT effect is low-dimensional |
| Endpoint image capture of exact effect | 0.3672 | Local endpoint image is misaligned |
| Base-preserving endpoint-image excess CE | 0.2212 nat | Misalignment is functionally consequential |
| Empirical secant-image excess CE | 0.00020 nat | Exact effect itself admits a sufficient 8D image |

## Central Figure

![Trajectory parameter capture, endpoint Jacobian tail, and functional closure](figures/trajectory_closure.png)

The parameter projection preserves function in every seed. In contrast, the
endpoint ROOT-image projection crosses the refutation threshold in four seeds.

## Claim Boundary

Allowed:

> In this registered model, AdamW training used an effectively
> eight-dimensional parameter displacement, and its exact learned ROOT effect
> was cross-context low-dimensional. The endpoint Jacobian image did not
> represent that finite effect.

Not allowed: H9 is globally false; the learned effect is high-dimensional; or
the mismatch must come from context rotation rather than movement along the
parameter path.

## Exactly One Next Decision

At the block-reverted reference point, compare the point-Jacobian prediction
directly with the exact learned secant to distinguish reference H9 from the
finite-displacement linearization assumption H11.

