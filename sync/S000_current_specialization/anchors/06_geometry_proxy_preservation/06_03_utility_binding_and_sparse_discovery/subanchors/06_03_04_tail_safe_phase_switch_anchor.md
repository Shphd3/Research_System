# A06_03_04 Tail-Safe Phase Switch

Thinking Card source: [06_03_utility_binding_and_sparse_discovery_thinking_card.md](../06_03_utility_binding_and_sparse_discovery_thinking_card.md)
Status: completed subanchor.

**Parent:** [`A06_03`](../06_03_utility_binding_and_sparse_discovery_anchor.md).

## Local Clause

Exploration should stop only when uncertainty is small for weak and rare
conditions, not when mean expert utility appears stable.

## Falsifiable Question

Can a lower-confidence utility certificate stop sparse audition without
increasing rare-condition routing regret?

## Evidence And Verdict

Duty-cycle and stopping audits reject mean-utility stopping as a safe rule.
Lower-tail confidence protects weak conditions better in the controlled task
and provides an explicit explore-to-exploit phase switch.

**Disposition:** retain as the stopping rule paired with bounded challenger
discovery.

**Boundary:** calibration under nonstationary experts and large-scale language
model workloads is not established.
