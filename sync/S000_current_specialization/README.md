# S000 Current Specialization Sync

## Current Mainline

The current mainline is:

```text
gating -> route-relevant feature partition -> early-training preservation
-> functional expert utility -> downstream effects
```

The active branch evidence is organized under:

```text
Projects/from-attention-to-search/XingyuD/sync/
Projects/from-attention-to-search/main/experiments/
```

The current branch anchor is:

```text
sync/S000_current_specialization/anchors/expert_specialization/00_feature_level_expert_specialization_mainline_anchor.md
```

Current project evidence anchors:

```text
Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_03_real_text_common_logit_initialization_anchor.md
Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_17_all_position_route_relevant_feature_discovery_anchor.md
Projects/from-attention-to-search/main/problem_anchors/07_features_overlap/07_04_common_rare_gradient_conflict_splitting_anchor.md
```

Latest meeting synthesis:

```text
daily_research_reports/0624/meetings/meeting_brief.md
```

## Current Evidence From Branch Sync

Latest useful source reports:

```text
Projects/from-attention-to-search/main/experiments/A05/A05_04_02_round2_dotproduct_common_logit/summary.md
Projects/from-attention-to-search/main/experiments/A05/A05_04_03_real_text_common_logit_audit/summary.md
Projects/from-attention-to-search/main/experiments/A06/A06_17_all_position_route_relevant_feature_discovery/summary.md
Projects/from-attention-to-search/main/experiments/A07/A07_04_common_rare_gradient_conflict_splitting/summary.md
```

Current evidence says:

- A05 supports common-component and early-feedback failure mechanisms, while
  weakening the strong claim that real-text step-0 routing is purely dominated
  by common logits.
- A06 supports route-position feature geometry in controlled settings, but
  shows that all-position clustering is the wrong sample population and that
  ordinary DCLM training can erase a step-0 proxy partition by step 5/10.
- A07 moves the value question from load or route purity to common/rare
  functional interference, but A07_04 is still insufficient evidence for
  functional MoE specialization.

## Current Claim Boundary

Can claim:

```text
Feature-level partition is reachable in controlled route-position geometry,
but ordinary top-1 routing does not naturally discover or preserve it. The
current mainline risk is wrong-object routing plus early-training overwrite.
```

Cannot claim:

```text
Real semantic experts exist.
Balanced load or high route NMI proves functional experts.
The A07 neural proxy already proves useful MoE specialization.
Reverse KV retrieval follows from current evidence.
```

## Next Decision

Do not continue broad architecture, context-length, or feature-existence
sweeps. The next anchor question is:

```text
Can a step-0 DCLM proxy partition be preserved through the step-5/10 training
window without unacceptable language-model loss regression?
```

If preservation succeeds, return to A07 functional utility. If it fails,
decompose gate update, hidden-state drift, expert feedback, and optimizer
geometry before proposing another method.
