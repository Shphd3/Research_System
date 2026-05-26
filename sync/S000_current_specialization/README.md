# S000 Current Specialization Sync

## Current Mainline

The current mainline is:

```text
gating -> expert specialization -> downstream effects
```

The active branch evidence is organized under:

```text
Projects/from-attention-to-search/XingyuD/sync/
```

The current branch anchor is:

```text
Projects/from-attention-to-search/main/problem_anchors/gating_induced_expert_specialization.md
```

## Current Evidence From Branch Sync

Latest useful sync reports:

```text
Projects/from-attention-to-search/XingyuD/sync/0524_router_feature_specialization/report.md
Projects/from-attention-to-search/XingyuD/sync/0525_zipfian_hierarchical/report.md
```

Current evidence says:

- corrected top-1 sparse MoE can learn the task, but AB-specific functional
  expert specialization is unstable;
- semantic or context initialization can create early semantic routing, but the
  semantic route decays during training;
- final hidden states still contain recoverable semantic boundaries, yet the
  trained router does not reliably turn those boundaries into functional expert
  utility;
- Zipfian token frequency changes load structure, but in the current diagnostic
  it does not by itself explain tail specialization failure;
- a minimal common/sense hierarchy increases token/family routing association,
  but does not improve tail functional specialization.

## Current Claim Boundary

Can claim:

```text
The current failure mode is not merely lack of semantic separability.
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

Do not continue broad architecture sweeps. First rewrite the branch anchor so
the physical prior and minimal falsifiable test are clear.

Recommended next anchor question:

```text
When token identity conflicts with slot/context feature, can a gating rule make
expert assignment follow the feature that has causal expert utility rather than
the easier token/frequency shortcut?
```

The next sync should report one minimal diagnostic that updates this anchor.
