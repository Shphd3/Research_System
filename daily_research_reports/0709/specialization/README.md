# 0709 Specialization Reframing Package

Status: migrated and adjudicated. This folder remains the original Chinese audit surface. Canonical anchors, protocols, and result records now live under `Projects/from-attention-to-search/main/`.

## Files

| File | Role |
| --- | --- |
| `story_cn.md` | Research-line story: redefines expert specialization as advantage-separable margin preservation and places router-method ideas after mechanism audit. |
| `06_33_signal_noise_advantage_margin_budget_anchor_cn.md` | Full anchor draft: one adjudicable decision question for the next mechanism audit. |
| `06_33_frozen_hidden_advantage_margin_protocol_cn.md` | Protocol draft: approval-facing experiment design for the frozen-hidden advantage-to-margin audit. |

## Current research thought

The immediate move is not to train a new MoE or promote a new router. The move is to make the mechanism measurable:

1. Define specialization as a functional object, not just route purity.
2. Measure whether expert advantage creates feature-conditioned margin growth.
3. Decompose why margin is lost: missing positive signal, background/common drift, top-1 selected-feedback weakness, or hidden drift.
4. Only after the mechanism is isolated, design a router that couples routing to expert utility more directly.

## Next decision

The daily draft was split because formula/autograd agreement is a chain-rule validity check, not a standalone mechanism result. Canonical chain:

1. `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_31_soft_router_advantage_margin_dynamics_anchor.md`
2. `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_32_top1_counterfactual_correction_dynamics_anchor.md`
3. `Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_33_background_bias_margin_budget_anchor.md`

All three 32-seed full runs completed. The next decision is an optimizer-aware trainable-hidden full-LM margin bridge, not a new gating method.
