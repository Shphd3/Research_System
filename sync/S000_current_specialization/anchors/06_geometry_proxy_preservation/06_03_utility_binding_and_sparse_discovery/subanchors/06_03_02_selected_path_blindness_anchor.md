# A06_03_02 Selected-Path Blindness

Thinking Card source: [06_03_utility_binding_and_sparse_discovery_thinking_card.md](../06_03_utility_binding_and_sparse_discovery_thinking_card.md)
Status: completed mechanism subanchor.

**Parent:** [`A06_03`](../06_03_utility_binding_and_sparse_discovery_anchor.md).

## Local Clause

A strict top-1 Router observes the selected expert's outcome but not the
counterfactual utility of unselected experts.

## Falsifiable Question

Can ordinary selected-path gradients reliably correct an initially wrong
expert rank without additional semantic credit?

## Evidence And Verdict

Wrong-rank correction and semantic-credit decomposition show that correction
depends on indirect rank-mediated signals and can be absent even when a better
expert exists. This weakens the assumption that end-to-end loss automatically
teaches the Router the counterfactual ordering.

**Disposition:** retain as the causal reason sparse discovery is required.

**Boundary:** blindness is partial, not absolute; shared parameters and soft
probabilities may still transmit indirect information.
