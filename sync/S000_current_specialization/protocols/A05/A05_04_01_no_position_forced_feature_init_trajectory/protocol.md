# A05_04 No-Position Forced Feature-Init Trajectory Protocol

## Goal

Decide whether the desired feature-to-expert partition is visible, useful, and trainably stable after fixed position signals are removed.

## Decision Question

In a one-B discriminative synthetic setting with randomized logical feature position and frozen zero positional embedding, does a feature-to-expert prior survive training, and does it correspond to expert utility?

## Tested Hypothesis

If the intended slot feature is visible and useful, then feature-to-expert initialization or an oracle feature router should preserve high route-feature NMI and show a feature-structured utility matrix. If trainable feature initialization collapses while the frozen oracle remains stable, the failure is training-time lock-in or route/expert co-adaptation rather than representation absence.

## Rival Explanations

- residual common or nuisance signal after position removal still dominates routing;
- the slot feature is visible but not causally useful for expert specialization;
- top-1 training destroys an otherwise valid feature partition;
- the observed structure is a metric artifact rather than feature-level routing.

## Data

- Original H0605a synthetic vocabulary and target rule.
- One-B setting: one B token, four slot features, four experts.
- The logical feature block is placed at a random valid sequence position per example.
- The router is evaluated at the logical B token, not a fixed absolute index.
- Absolute positional embedding is zeroed and frozen from initialization.

## Variants

For each router metric (`cosine`, optionally `dot_product`):

| Variant | Meaning |
|---|---|
| `V0_vanilla_random` | random trainable top-1 router |
| `V1_random_balanced_init` | trainable router initialized from random candidates selected for balanced, low-slot-NMI step-0 routing |
| `V2_feature_init_trainable` | trainable router initialized from slot centroids |
| `V3_oracle_frozen` | route logical B token to its slot expert throughout training |
| `V4_feature_init_inhibition` | slot-centroid initialized trainable router plus current true token-conditioned inhibition |

## Primary Metrics

- `route_slot_nmi`: whether route assignment carries slot feature identity.
- `max_load`: collapse guard.
- `target_accuracy`: validity guard.
- feature assignment survival from step 0 to final.
- feature-by-expert utility matrix and route-utility agreement.

## Secondary Diagnostics

- linear probe accuracy for slot from routed hidden state;
- route flip rate between checkpoints;
- logit decomposition summaries;
- router gradient projection onto common and slot-residual directions.

## Success

Feature-init or oracle routing keeps high route-slot NMI, non-collapsed load, high accuracy, and feature-structured utility across seeds.

## Failure

Trainable variants lose route-slot NMI or collapse despite visible slot information, especially when oracle routing remains stable.

## Insufficient Evidence

Missing trajectories, missing utility matrix, invalid target accuracy, or incomplete seed coverage.

## Claim Boundary

This experiment can distinguish representation visibility, utility alignment, and trainability in the toy setting. It cannot claim a deployable MoE method or real-language transfer.

