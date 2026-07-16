# Thinking Card — A06_03 Utility Binding And Sparse Discovery

> Migrated from [06_03_utility_binding_and_sparse_discovery_anchor.md](06_03_utility_binding_and_sparse_discovery_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** Correct conditional exposure creates specialists even when
route purity is matched by a shuffled control. A correct specialist route is
preserved, but the same useful specialist remains undiscovered when initialized
below top-1.

**Physical judgment:** Expert specialization forms through conditional update
distributions. Top-1 discovery is then a partial-feedback problem: the selected
expert is evaluated, while unselected expert functions are hidden. One bounded
challenger supplies the missing comparison, and a lower-tail utility certificate
ends exploration after weak conditions are safe.
