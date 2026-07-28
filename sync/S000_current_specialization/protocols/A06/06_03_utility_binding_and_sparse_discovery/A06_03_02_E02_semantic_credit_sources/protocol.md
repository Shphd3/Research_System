# A06_03_02_E02 Semantic-Credit Source Decomposition Protocol

Approval status: approved by the standing request to continue the active research goal.

Purpose: determine whether learned-specialist wrong-route trapping is caused by
background-position gradient override, selected-only utility blindness, or both.

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/subanchors/06_03_02_selected_path_blindness_anchor.md`.

Anchor decision question: from exactly the same learned-specialist rank-2 state,
does task-position-only weighted top-1 recover when full-sequence top-1 does not?

## Terminology / Definitions

- **Task position:** one of 16 next-token targets whose correct token depends on
  the sequence instruction. The loss mask is used only as an oracle causal
  intervention.
- **Background position:** one of 16 remaining next-token targets whose correct
  token does not directly encode the instruction-dependent transform.
- **Useful expert:** expert whose forced use gives the lowest held-out task loss
  after specialist exposure.
- **Source pressure:** first-order change pressure on the useful-versus-selected
  router margin. For loss source $q$,
  $P_q=-\langle g_u^q-g_r^q,\mu_f\rangle$; positive values favor correction.
- **Sustained correction:** useful-expert route accuracy is at least `0.95` for
  five consecutive updates.

## Fixed Setup

- Data, one-layer causal Transformer, four trainable experts, exposure stage,
  held-out split, no learned positional embedding, and rank installation are
  identical to A06_03_02_E01.
- Each length-33 sequence contributes 32 next-token targets: 16 task positions
  and 16 background positions.
- Expert exposure: 200 expert-only updates.
- Correction: experts and representation frozen; router-only SGD, learning rate
  `0.001`, 300 updates.
- Initial useful-expert rank: rank 2 for the primary decision; rank 4 for
  replication.
- Full run: 32 seeds, four tasks per seed, hence 128 paired cells per condition.

## Conditions

For each rank, clone the same router and non-router tensors and run:

1. `full_top1`: mean loss over all 32 targets.
2. `task_top1`: mean loss over the 16 task targets.
3. `background_top1`: mean loss over the 16 background targets.
4. `half_task_top1`: one half of task-position mean loss, matching its coefficient
   inside the full mean.
5. `task_soft`: task-position mean loss with all-expert soft forward utility.

## Measurement And Validity Guards

Before branch updates, compute full, task, and background top-1 gradients from
the same tensor state. Require

$$
\frac{\|g_{full}-\frac12g_{task}-\frac12g_{bg}\|_2}
{\max(\|g_{full}\|_2,10^{-12})}\le 10^{-5}.
$$

Also require A06_03_02_E01's specialist utility, useful-rank accuracy, adjacent score
gap, balanced-load, state-pairing, and finite-trajectory guards. The task and
half-task gradients must be collinear and have norm ratio `0.5` within `1e-5`.

## Primary Metrics And Decision Rules

Primary comparison at rank 2:

$$
D_{src}=\operatorname{median}
(\widetilde T_{corr}^{full}-\widetilde T_{corr}^{task}),
$$

with seed-clustered 95% bootstrap confidence interval. Failed trajectories are
capped at step 301.

- **H1 background override:** task-top1 correction rate at least `0.90`, full
  rate below `0.10`, positive lower confidence bound for $D_{src}$, median task
  pressure positive, and median background pressure negative.
- **H2 selected-only blindness:** task-top1 rate below `0.10` and task-soft rate
  at least `0.90`.
- **H3 dual bottleneck:** task-top1 improves correction or normalized regret over
  full, remains materially behind task-soft, and background pressure is negative.
- **H4 no source bottleneck:** none of the above while validity and soft-control
  guards pass.

Rank 4 must preserve the qualitative verdict. Half-task is a scale guard, not a
method candidate.

## Claim Boundary

This protocol can identify the causal loss-source bottleneck in the controlled
learned-specialist system. It cannot establish a label-free semantic-position
estimator, natural-language expert semantics, MTP benefit, or a deployable MoE
router.
