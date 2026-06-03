# S000 Current Specialization Sync

## Current Mainline

The current mainline is:

```text
gating -> expert specialization -> downstream effects
```

The active branch evidence is organized under:

```text
Projects/from-attention-to-search/XingyuD/sync/
Projects/from-attention-to-search/main/experiments/
```

The current branch anchor is:

```text
Projects/from-attention-to-search/main/problem_anchors/01_slot_context_dominance_router_specialization_anchor.md
```

Root-sync copy:

```text
sync/S000_current_specialization/anchors/expert_specialization/01_slot_context_dominance_router_specialization_anchor.md
```

Latest formal mechanism sync package:

```text
sync/S000_current_specialization/reports/0531_2x2_top1_router_lockin/
sync/S000_current_specialization/reports/0531_2x2_top1_router_lockin/05_report_card.md
sync/S000_current_specialization/reports/0531_2x2_top1_router_lockin/summary.md
sync/S000_current_specialization/reports/0531_2x2_top1_router_lockin/detailed.md
```

## Current Evidence From Branch Sync

Latest useful sync reports:

```text
Projects/from-attention-to-search/XingyuD/sync/0524_router_feature_specialization/report.md
Projects/from-attention-to-search/XingyuD/sync/0525_zipfian_hierarchical/report.md
Projects/from-attention-to-search/XingyuD/sync/0526_slot_context_dominance/report.md
```

Current evidence says:

- corrected top-1 sparse MoE can learn the task, but AB-specific functional
  expert specialization is unstable;
- in the 2026-05-31 2x2 NTP-style top-1 proxy, failed seeds are already
  collapsed at step 0, successful seeds are already split at step 0, and router
  bias worsens same-expert initialization risk;
- semantic or context initialization can create early semantic routing, but the
  semantic route decays during training;
- final hidden states still contain recoverable semantic boundaries, yet the
  trained router does not reliably turn those boundaries into functional expert
  utility;
- Zipfian token frequency changes load structure, but in the current diagnostic
  it does not by itself explain tail specialization failure;
- a minimal common/sense hierarchy increases token/family routing association,
  but does not improve tail functional specialization.
- slot context can control routing in a fixed-B diagnostic, but multi-B
  trajectory shows slot-centroid initialization starts non-diagonal, training
  improves NMI only partially, and visible predictive slot information is not
  sufficient for robust route-function binding under B identity variation.

## Current Claim Boundary

Can claim:

```text
The current failure mode is not merely lack of semantic or slot separability.
The sharper issue is route-function mismatch: route assignment, expert causal
utility, and the training objective are not yet reliably aligned.
```

Cannot claim:

```text
Current gating already induces stable expert specialization.
Routing heatmaps or normalized mutual information prove functional experts.
Zipfian frequency is irrelevant in general.
Hierarchical MoE is generally ineffective.
Reverse KV retrieval follows from current evidence.
```

## Next Decision

Do not continue broad architecture or context-length sweeps. The slot-context
dominance diagnostic is now closed enough to redirect toward route-function
binding.

Recommended next anchor question:

```text
Can an explicit route-function binding signal make route assignment align with
expert causal utility in the multi-B / slot-context setting?
```

The next sync should report one minimal route-function binding diagnostic
rather than another broad context-strength or architecture sweep.
