# E2 MoE Feature Separation

E2 is the MoE branch of the synthetic data understanding line. It asks one
question:

```text
When controlled trigram features repeatedly appear in a next-token corpus,
does a top-1 MoE naturally route different feature representations to
different experts?
```

Current answer:

```text
The MoE learns feature readback and shows feature-expert alignment, but it does
not cleanly become one-feature-one-expert. The important follow-up question is
why the router does not use the feature-separating directions that are visible
in the hidden representation.
```

## Read Order

1. `versions/E2_0_moe_feature_separation/` - initial MoE feature-expert alignment and ablation test.
2. `versions/E2_1_router_input_geometry/` - whether feature identity is still available at router input and whether router boundaries use it.
3. `versions/E2_2_specialization_pressure/` - whether reducing expert capacity or adding more features forces cleaner specialization.
4. `versions/E2_3_router_behavior_decomposition/` - shared-B control and router behavior decomposition.
5. `versions/E2_H_hmoe_hierarchical_routing_side_branch/` - H-MoE side branch on two-level synthetic hierarchy.
6. `versions/E2_S_spectral_covariance_router_side_branch/` - spectral covariance router side branch without LB on spectral variants.
7. `versions/E2_S_uniform_frequency_control/` - uniform-frequency control for the spectral covariance router branch.
8. `versions/E2_D_router_supervision_diagnostic/` - supervised router diagnostic with true synthetic feature labels.
9. `versions/E2_B_prototype_center_gating/` - prototype / center gating router diagnostic.
10. `versions/E2_C_contrastive_router_loss/` - contrastive router representation diagnostic.
11. `E2_theory_ai_prompt.md` - compact prompt for external theoretical discussion.

## Current Interpretation

Use these terms precisely:

- `feature` / `motif` / `pattern`: the planted data rule, such as `[1,2] -> 22`.
- `representation` / `hidden state`: the model vector at the prefix-end position, such as $h_{[1,2]}$.
- `expert specialization`: whether router decisions map different feature hidden states to distinct experts.

The key phenomenon is:

```text
The data contains distinct artificial features.
The model hidden states preserve feature-separating structure.
The router does not turn that structure into clean one-feature-one-expert routing.
```

## Current Next Plan

E2.3 should be read before any new run. It formalizes the next decision:

```text
Treat selected expert id as the object to explain, and compare whether it is
best predicted by feature identity, token shortcut, hidden scale, prediction
difficulty/confidence, PCA coordinates, or router-specific hidden directions.
```

E2.3 has now been executed with shared-B control. It weakens the simple
prefix-end token shortcut explanation, while showing that expert choice is
better explained by full hidden geometry and router projection than by a clean
feature-label partition. The next control is shared-target.

The H-MoE side branch is a separate architecture check, not a replacement for
the E2 mainline. It shows that H-MoE can preserve L1/L2 readback on a
two-level synthetic corpus, but in the current tiny top-1 setup it does not
produce more stable hierarchy-aligned routing than Flat-MoE.

The spectral covariance router side branch is also separate from the E2
mainline. Its current result is negative: trained-covariance middle-to-late
projection preserves readback, but does not improve feature-aligned routing
over full-hidden router or same-dimensional random projection.

The uniform-frequency control shows that frequency imbalance is part of the
difficulty: when all four features have equal count, spectral midlate routing
becomes stronger. But shuffled covariance controls are also strong, so this
still does not support the claim that trained global covariance midlate bands
are a clean semantic routing statistic.

The router-supervision diagnostic shows that the implementation can form clean
specialization when given true synthetic feature labels: ABC/DEF/GHI/JKL route
to experts 0/1/2/3 with fixed-label accuracy 1.0. This shifts the E2 question
away from "can the model specialize?" and toward "why does the natural NTP
objective not require feature-identity routing?"

E2-B shows that prototype / center gating alone is not enough: without feature
supervision it remains mixed, but with feature-to-prototype CE it reaches clean
routing and strong ablation effects. E2-C shows that contrastive representation
pressure is also not enough in this implementation: feature labels are linearly
readable from router representations, yet expert assignment remains mixed.

Together, E2-B/E2-C sharpen the current claim:

```text
Clean specialization appears when the loss directly supervises the router-to-expert
assignment, but not merely when the representation is made feature-readable.
The unresolved mechanism is the boundary from feature-readable router input to
top-1 expert choice.
```

## Package

`E2_theory_ai_package.zip` contains this E2 folder plus the current project
mainline files needed for external theoretical analysis.
