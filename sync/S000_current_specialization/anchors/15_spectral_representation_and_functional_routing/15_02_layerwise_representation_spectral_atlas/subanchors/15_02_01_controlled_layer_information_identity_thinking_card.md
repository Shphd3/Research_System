# A15_02_01 Thinking Card: What Does Each Layer-Band Cell Encode?

Status: the researcher's judgment was stated in the post-meeting request on 2026-07-31; AI only formalized it as a testable object.

## Current Judgment

A linear Gate learns its own-layer covariance head most easily, but identically named head, middle, and tail bands need not encode the same information at different depths. Cross-layer routing should wait for a `layer x band x information` profile.

## Mechanistic Intuition

A four-layer network may retain a coarse condition first, form a conditional intermediate state next, and compute a composed result later. Covariance rank only orders within-layer variation; independent labels and controls must determine functional identity.

## Strongest Rival

Composition may be more readable at depth only because deeper states are closer to the output. A band advantage may also be reproduced by an arbitrary subspace of equal dimension. A saturated task cannot identify spectral specificity.

## Evidence That Would Change The Judgment

A four-layer MoE must first generalize to held-out component combinations. Across two independent training seeds, a layer-band information increment must then replicate on the sealed test set and exceed equal-dimensional random directions, initialization, and a matched one-step objective.

## Next Decision

Only a stable layer-specific functional coordinate enters the later compatibility gate; otherwise covariance rank is not promoted to a cross-layer routing label.
