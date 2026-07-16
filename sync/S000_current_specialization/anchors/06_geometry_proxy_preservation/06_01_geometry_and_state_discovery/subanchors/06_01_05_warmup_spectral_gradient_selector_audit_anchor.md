# A06_01_05 Warmup, Spectral, And Gradient Selector Audit

Thinking Card source: [06_01_geometry_and_state_discovery_thinking_card.md](../06_01_geometry_and_state_discovery_thinking_card.md)
Status: completed method-falsification subanchor.

**Parent:** [`A06_01`](../06_01_geometry_and_state_discovery_anchor.md).

## Local Clause

Stronger hidden-state separation is useful only if it selects the correct
routed-state population and yields positive held-out low-tail margin.

## Falsifiable Question

Do warmup, expert singular directions, manifold power iteration, Fisher-style
scores, or full-sequence gradient scores provide a safe label-free
initializer?

## Evidence And Verdict

Warmup increases pairwise feature-center distance, while the state pool remains
mixed. Spectral and gradient selectors improve selected clustering statistics
but fail the joint route-agreement and low-tail-margin contract under the
registered full-language-model objective.

**Disposition:** park these methods as diagnostics, not active initializers.

**Boundary:** failure applies to the tested score constructions and controlled
model; it is not a theorem against all gradient-based discovery.
