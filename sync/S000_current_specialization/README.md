# S000 Current Specialization

This is the compact cross-project reading surface for the current
feature-specialization project. Project-local anchors and experiment records
remain the source of truth.

## Current State

The synchronized surface now exposes three independent current decisions:

```text
A06: decide whether to test training-time selective sharing after the frozen
     CrossCodeEval headroom clause failed.
A15: decide whether layerwise long-range innovation should be adjudicated by
     direct absolute G_{ell,2F}, not by a positive interaction alone.
A16: run the approved two-seed frozen expert-choice-regret gate before any
     conditional-innovation 30B continuation.
```

These lines do not gate one another. A06 owns expert-utility formation on a
registered workload; A15 owns representation coordinates and functional
admission; A16 owns load control and the functionally supervised incremental
Router branch. Geometry or load balance alone does not justify an LLM Router.

## Research-Line Map

| Line | Current role | Reading entry |
|---|---|---|
| 05 | Failure priors for ordinary top-1 routing | [failure line](research_lines/05_failure_mechanism_line_cn.md) |
| 06 | Main chain from route geometry to expert utility and the real-workload gate | [current A06 line](research_lines/06_proxy_preservation_line_cn.md) |
| 07 | Functional interference and value diagnostics | [value line](research_lines/07_interference_value_line_cn.md) |
| 11 | Objective-level difference between NTP and MTP on a minimal delayed branch | [informative-future branch](research_lines/11_informative_future_branch_mechanism_cn.md) |
| 12 | Structured composition, task capability, and standard-head causal use | [structured composition](research_lines/12_structured_compositional_mtp_workload_cn.md) |
| 13 | Task-property decomposition from hard relay to the soft-relay measurement blocker | [A13 anchors](anchors/13_mtp_task_property_decomposition/README.md) |
| 14 | Conditional low-dimensional computation under a globally high-capacity hierarchy | [A14 anchors](anchors/14_tree_low_rank_language_structure/README.md) |
| 15 | Spectral representation geometry, public-coordinate audits, functional admission, and target-conditioned layer innovation | [A15 anchors](anchors/15_spectral_representation_and_functional_routing/README.md) |
| 16 | Load control and functionally supervised incremental-information routing | [A16 anchors](anchors/16_load_control_gradient_interference/README.md) |

Read [the overall synthesis](research_lines/00_overall_current_line_cn.md) first.

## Supporting MTP Route

The MTP work is now explicitly split:

```text
A11: informative future target
-> direct current-state signal
-> shared-parameter reachability
-> formation is not sufficient for later standard-head use

A12: ordered composition workload
-> reject the fixed-table exact-tail and asymmetric query-structure carriers
-> complete balanced per-sample E04 NTP-only Stage A
-> no scale passes both task depths; no threshold is frozen
-> row-removal necessity guard is invalid under bijection completion
-> decide whether to close E04 or redesign the carrier under a new Protocol
-> standard-head causal intervention remains downstream
```

A11 is a stable bounded baseline. A12 E04 failed the NTP capability and
row-removal validity gates. A13 established the hard-relay sufficient
condition; soft-relay Stage 0 showed ordered causal path use but no common
non-saturated comparison window. The next decision is measurement-only carrier
repair, not an objective-effect claim.

## Independent A14 Route

A14 retains the controlled conditional-functional-rank theorem and closes the
global shared-linear propagation claim. The improved frequency comparison
supports non-inferiority only in its registered common-mapping task. The raw
parameter-update basis is parked as unidentified, while E04--E06 retain the
local Jacobian versus finite secant result. Router utility and a complete
state-to-parameter rank claim remain unverified.

## Independent A15 Route

A15 is now organized by decision ownership rather than experiment chronology:
Router-input geometry, learning and feedback dynamics, layerwise representation
atlases, functional coordinate admission, online routing, and target-
conditioned layer innovation. A15_03 is archived and A15_07 remains parked
unrun. The public-coordinate sequence establishes only basis-conditioned
description: Mean Response orders coarse--medium--fine on average, while a
second parameter basis disagrees on depth shift, same-layer shapes overlap,
and adjacent-layer variance redistribution is non-monotonic. A15_08 E04 keeps
one local added-accessibility fact, but two directions retain only 33.24% of
the full gain. A15_08_01 E02 has a positive depth interaction and negative
absolute remote two-hop gain, so the next decision is whether to test direct
absolute $G_{\ell,2F}$.

## Independent A16 Route

A16_00 closes the global Centered-mediation explanation while retaining one
early counterfactual relief result. A16_01 is active after the NLL-only
increment branch failed to show a replicated 20B advantage. Its immediate
decision is the approved two-seed frozen expert-choice-regret gate comparing
Conditional-Utility with Native, Raw-Utility, and Conditional-Haar. The 30B
continuations remain fail-closed unless that functional gate passes.

## Claim Boundary

Current controlled evidence supports route-geometry reachability, finite-margin
preservation mechanisms, trainable expert utility under correct exposure,
bounded challenger discovery, and a safe phase switch in the frozen bridge.
It does not establish real repository-code routing headroom or an LLM Router.

For MTP, current evidence supports a direct informative-future signal, a
controlled linear missing-rank tradeoff, and an exactly learnable but
memorization-prone fixed-rule surface. E03 was rejected for asymmetric
query-relevant structure; E04 failed the NTP capability and row-removal
validity gates. No broad convergence advantage, neural causal use, model-scale
benefit, or real-task transfer is established.

For long-context retrieval, R3/R4 establish only that perfect feature alignment
is insufficient for a useful sparse index in the controlled all-trigram setup.
They do not establish the correct Router target, million-token performance, or
transfer to real agents.

## Copy Boundary

The complete `anchors/` tree is a generated mirror of
`Projects/from-attention-to-search/main/problem_anchors/`, including every
active parent anchor, subanchor, and bilingual companion.
Links inside the anchor tree remain relative. Links that leave
`problem_anchors/` are rewritten to repository-root absolute paths so they are
directly usable from the published mirror.

Generate or verify the mirror with:

```text
python .agents/skills/research-mainline/scripts/publish_anchor_mirror.py
python .agents/skills/research-mainline/scripts/publish_anchor_mirror.py --check
```

Do not hand-edit `anchors/`; update the project-local source and republish.

The `stories/` tree mirrors current line-level syntheses and excludes archived
historical snapshots with stale evidence links. The `protocols/` tree mirrors
canonical protocols, Chinese companions, and explicitly labeled legacy or
draft protocol documents only; it does not copy summaries, detailed ledgers,
scripts, figures, logs, or raw outputs. See [protocol index](protocol_index.md).

Generate or verify the additional mirrors with:

```text
python .agents/skills/research-mainline/scripts/publish_anchor_mirror.py --source Projects/from-attention-to-search/main/stories --target sync/S000_current_specialization/stories --exclude-dir archive
python .agents/skills/research-mainline/scripts/publish_anchor_mirror.py --source Projects/from-attention-to-search/main/experiments --target sync/S000_current_specialization/protocols --include-name protocol.md --include-name protocol_cn.md --include-name protocol_for_approval.md --include-name protocol_draft_cn.md
```

This root sync was refreshed on 2026-08-15. Project-local anchors, stories,
and experiment records remain authoritative.
