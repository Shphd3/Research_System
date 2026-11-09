---
experiment_id: A15_11_E01_qwen_native_router_access_gap
status: EVIDENCE_COMPLETE_AI_INTERPRETATION_AWAITING_HUMAN_CONFIRMATION
completed: 2026-08-29
resource: 8xRTX5090_SPOT
primary_job: pt-0aopddjj
---

# Summary: Qwen Native Router Accessibility Chain

Primary Anchor: [A15_11 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md)
Frozen Protocol: [protocol.md](protocol.md)
Detailed record: [detailed.md](detailed.md)

## Result Snapshot

**Registered verdict:** `TOP8_SELECTION_BOTTLENECK_WITH_RETAINED_ASSOCIATION`.

In frozen Qwen3-30B-A3B, eight-way parent labels are almost perfectly readable
from the native MoE input \(H\). The 128-dimensional native Gate logits \(Z\)
retain most of that held-out accessibility. Renormalized top-eight routing
\(Q\), however, loses 0.434--0.567 balanced-accuracy points at the five fixed
confirmation blocks. Despite this loss, its weighted expert assignments remain
more parent-associated than the matched max-layer label-permutation null.

The registered cross-panel criterion passes at Blocks 4, 12, 20, and 28:
projection is preserved, top-eight selection loss is material, and native
route association is retained in both C4 and C5. Block 36 misses only the C4
projection-preservation threshold. No confirmation block has near-total sparse
retention. The BF16 primary and FP32 sensitivity paths give the same line
verdict.

The result locates a **semantic accessibility loss at sparse expert selection**.
It does not show that the selected experts have the corresponding function,
that parent routing lowers language-model loss, or that Qwen pretraining formed
the hierarchy through the proposed gradient mechanism.

## Decision-Bearing Evidence

| Block | C4 \(BA(H)\) | C4 \(BA(Z)\) | C4 \(BA(Q)\) | C5 \(BA(H)\) | C5 \(BA(Z)\) | C5 \(BA(Q)\) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 1.0000 | 0.9979 | 0.5635 | 1.0000 | 0.9984 | 0.5365 |
| 12 | 1.0000 | 0.9943 | 0.5000 | 1.0000 | 0.9953 | 0.4917 |
| 20 | 1.0000 | 0.9870 | 0.4219 | 1.0000 | 0.9859 | 0.4375 |
| 28 | 0.9995 | 0.9714 | 0.4047 | 0.9984 | 0.9635 | 0.4505 |
| 36 | 0.9974 | 0.9417 | 0.4068 | 0.9948 | 0.9510 | 0.4484 |

For C4, \(I_Q(Y;E)/H(Y)\) is 0.00416--0.01385 against a common
max-layer null of 0.002025. For C5 it is 0.00266--0.01366 against 0.001334.
These values establish bounded association only; their small scale is visible
and is not promoted to semantic expert function.

![Held-out accessibility ladder](figures/balanced_accuracy_ladder.png)

![Projection and top-eight selection gaps](figures/accessibility_gaps.png)

## Claim Boundary

### Can claim

- parent labels are highly accessible from frozen \(H\) and mostly retained in
  the native Gate row space \(Z\) on the registered cross-template task;
- native top-eight selection removes a large fraction of that accessibility;
- the sparse route retains association above the matched label null;
- the result is stable to the registered BF16/FP32 sensitivity check.

### Cannot claim

- native parent semantics are a training objective or causal routing feature;
- parent-associated experts are counterfactually useful;
- a replacement Router improves Qwen loss;
- the same profile holds outside C4/C5 or outside this checkpoint;
- X-MoE-style projection alone creates nonlinear separability.

## Next Decision

This record does not independently authorize Router training. It contributes
one premise to the A15_11 decision: a real Gate row space can retain a label
while sparse selection fails to preserve most of its accessibility. Any real-
model successor must measure equal-compute expert utility, not substitute
semantic labels or native route IDs for utility.
