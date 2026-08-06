---
thinking_card_id: 15_01_shallow_head_guided_deep_routing
status: human_direction_approved_details_pending
source_language: zh
source_file: 15_01_shallow_head_guided_deep_routing_thinking_card_cn.md
formalization_authorized: true
protocol_authorized: false
implementation_authorized: false
full_run_authorized: false
updated: 2026-07-30
---

# Thinking Card: Shallow-Head Guidance For Deep Routers

This is a faithful translation of the researcher-owned
[Chinese Thinking Card](15_01_shallow_head_guided_deep_routing_thinking_card_cn.md).

## Human Judgment

- **Phenomenon:** The group-meeting proposal is to use high-variance information
  already formed in earlier layers to guide later dispatch. This mechanism is
  distinct from same-layer middle/tail dispatch.
- **Mechanism guess:** A shallow head may form stable coarse domain or common
  structure early. Supplying the same token's shallow-head coordinates to a
  deeper Gate may reduce route churn and let deep experts receive compatible
  tokens earlier.
- **Strongest rival:** `Unknown`; AI was asked to propose it for itemized review.
- **Most uncertain point:** Whether high variance adds deep-expert compatibility
  information rather than position, length, common semantics, or load collapse.
- **Evidence that would change the judgment:** After controlling the native
  deep score, parameters, load, capacity, and tokens, shallow head fails to beat
  same-dimensional random, token-shuffled, or nuisance controls; or route
  stability does not improve held-out loss at matched FLOPs.
- **Current decision:** Review the controlled four-layer pilot subanchor and
  Approval Snapshot. No implementation or 8x5090 run is approved.

## AI Audit

The strongest rival is extra parameters, marginal scale, load changes, or
shared token identity rather than token-specific shallow-head information. A
shallow basis cannot be applied directly to deep coordinates; the valid object
is $U_{2,H}^\top(g_2-\mu_2)$ for the same token. The smallest separator is a
controlled head/random/token-shuffled comparison with a held-out one-step
compatibility gate.

## Confirmation

The four-layer direction is approved. Side-channel form, controlled task,
controls, capability gate, primary training metric, seeds, and budget remain
pending. Implementation and execution are not authorized.

