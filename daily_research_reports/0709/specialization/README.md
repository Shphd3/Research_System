# 0709 Specialization Reframing Package

Status: daily working package. This folder is a Chinese audit surface for the 2026-07-09 specialization reframing. It is not yet the canonical project-local anchor/story under `Projects/from-attention-to-search/`.

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

Approve or revise the `06_33_frozen_hidden_advantage_margin_protocol_cn.md` protocol. Do not run a broad sweep or write a new gating method until the one-step advantage-to-margin model is falsified or supported.
