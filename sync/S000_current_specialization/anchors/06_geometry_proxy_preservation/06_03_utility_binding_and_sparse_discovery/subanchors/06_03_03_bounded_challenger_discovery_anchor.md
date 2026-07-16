# A06_03_03 Bounded Challenger Discovery

Thinking Card source: [06_03_utility_binding_and_sparse_discovery_thinking_card.md](../06_03_utility_binding_and_sparse_discovery_thinking_card.md)
Status: completed subanchor.

**Parent:** [`A06_03`](../06_03_utility_binding_and_sparse_discovery_anchor.md).

## Local Clause

Occasionally evaluating one nonselected challenger can provide a local
counterfactual utility signal without executing every expert.

## Falsifiable Question

Does a bounded rotating challenger improve recovery of the best expert beyond
load balancing and random exploration at matched compute?

## Evidence And Verdict

The controlled challenger experiment shows that sparse counterfactual credit
can repair wrong ranking more directly than selected-path feedback. The result
supports bounded audition as a discovery primitive, not as a complete Router
design.

**Disposition:** retain as the active method ingredient.

**Boundary:** compute cost, stale challenger estimates, and real-workload
utility headroom remain unresolved.
