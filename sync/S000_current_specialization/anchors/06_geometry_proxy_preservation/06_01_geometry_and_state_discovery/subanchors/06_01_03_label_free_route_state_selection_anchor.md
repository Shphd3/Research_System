# A06_01_03 Label-Free Route-State Selection

Thinking Card source: [06_01_geometry_and_state_discovery_thinking_card.md](../06_01_geometry_and_state_discovery_thinking_card.md)
Status: completed subanchor with a negative verdict.

**Parent:** [`A06_01`](../06_01_geometry_and_state_discovery_anchor.md).

## Local Clause

The discovery problem is to select the hidden states carrying route-relevant
conditions without knowing the route position or feature label.

## Falsifiable Question

Can common-residual scores, clustering stability, margin-aware center search,
or Router-logit statistics recover the oracle routed-state population?

## Evidence And Verdict

Route-position clustering recovers the intended partition, while mixed
all-position pools merge conditions. The tested label-free selectors improve
individual proxies but do not jointly recover oracle agreement and positive
low-tail margin.

**Disposition:** close the tested selector family; keep the result as the state
population mismatch diagnosis.

**Boundary:** this does not prove that all label-free selection is impossible.
