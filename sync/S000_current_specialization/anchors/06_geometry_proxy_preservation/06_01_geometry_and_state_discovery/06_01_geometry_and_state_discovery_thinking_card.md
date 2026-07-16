# Thinking Card — A06_01 Geometry And Route-Relevant State Discovery

> Migrated from [06_01_geometry_and_state_discovery_anchor.md](06_01_geometry_and_state_discovery_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** The intended feature partition is linearly reachable when the
correct route-position states are known. Clustering all positions, waiting for
warmup, or extracting stronger spectral directions does not reliably identify
the same population. Real-text proxies can initialize a Router but are rapidly
overwritten by ordinary training.

**Physical judgment:** The initialization problem has three contracts:
route-relevant information must exist, the correct state population must be
selected without privileged labels, and the resulting rows must enter a
trainable basin. Existing evidence passes the first contract, partially passes
the second only with controlled supervision, and fails the third on real proxy
training.
