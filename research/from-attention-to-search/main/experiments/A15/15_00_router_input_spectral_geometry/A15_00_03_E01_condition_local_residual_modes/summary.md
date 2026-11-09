---
experiment_id: A15_00_03_E01_condition_local_residual_modes
status: complete_pass_conditional_modes_shared_envelope
completed: 2026-07-31
primary_anchor: 15_00_03_condition_local_residual_modes
chinese_companion: summary_cn.md
---

# Summary: Condition-Stratified Residual Projectors

## Conclusion

Residual geometry has two scales. When many documents are pooled by
domain/topic, residual bases are highly shared but have small reproducible
condition-specific rotations. When each document independently fits its own
projector, the exact low-dimensional mode changes substantially from document
to document. The supported model is therefore **document-local modes inside a
broad shared residual envelope, with domain/topic explaining a modest part of
the rotation**.

At condition level, same-domain rank-64 overlap is 0.754--0.777 versus
0.698--0.725 cross-domain. A foreign-domain basis retains 95.1--96.4% of
same-domain capture; topics retain 92.2--93.8%. At document level, residual
rank-64 overlap is only 0.301--0.308 within domain and 0.295--0.302 across
domains, still far above Haar q95 0.094. Cross-domain capture is 97.8--98.1% of
same-domain capture, but only 32.7--34.1% of the target document's own rank-64
optimum.

A disjoint-token split-half guard rejects finite-token estimation as the main
explanation: residual rank-32 overlap is 0.516--0.534 within the same document,
0.173--0.181 between same-domain documents, and 0.168--0.177 across domains.

Centered top/common directions are more transferable than residual directions
at both scales. The experiment supports a softened A14-style mixture account,
not the strong claim that removing common exposes incompatible domain spaces,
and not the claim that coarse domain labels identify each local mode.

## Decision Evidence

| Condition | Residual within overlap | Residual cross overlap | Cross/within capture | Decision role |
| --- | ---: | ---: | ---: | --- |
| Domain, all endpoints | 0.754--0.777 | 0.698--0.725 | 0.951--0.964 | condition identity changes exact directions, but transfer stays high |
| Topic, all endpoints | 0.673--0.700 | 0.615--0.646 | 0.922--0.938 | nested topics replicate the direction |
| Document, rank-64 | 0.301--0.308 | 0.295--0.302 | 0.978--0.981 | exact local modes vary; cross-domain is almost as transferable as same-domain |

All 12 layers at all four endpoints have positive within-minus-cross gaps and
positive cross-capture margins above the complement-Haar q95. Actual Gate-input
replay is exact: relative logit error 0 and top-1 agreement 1.0.

![Residual modes rotate inside a shared envelope](figures/condition_overlap_and_cross_capture.png)

![Document-local modes and their shared envelope](figures/document_projector_overlap_and_capture.png)

## Boundary

The result establishes representation geometry for one WOS label system and
two trained Router lineages. The low document overlap still contains finite
128-token estimation error, although the split-half control shows it is not
the dominant explanation. It does not establish that labels are causal
semantic variables or that conditional residual routing improves training.
The separate matched 2B experiment found routing changes without NLL benefit.

Full metrics are in [the evidence ledger](detailed.md) and
[condition-level table](tables/condition_stratified_summary.csv) and
[document-level table](tables/document_projector_summary.csv).
