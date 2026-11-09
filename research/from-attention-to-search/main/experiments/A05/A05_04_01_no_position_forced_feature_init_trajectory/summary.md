# A05_04 Summary: No-Position Forced Feature-Init Trajectory

## Question

After removing trainable positional embeddings and randomizing the logical routed feature position, can top-1 MoE routing form stable slot-level feature-to-expert specialization?

## One-Line Verdict

Oracle slot routing is perfectly learnable, but the trainable router still does not reliably discover or preserve slot-level specialization across seeds.

## Setup

- Data: one-B discriminative uniform setting; 4 logical slots, 4 experts.
- Position control: positional embedding is zeroed and frozen; the logical B token is evaluated at randomized valid sequence positions.
- Routing analysis position: logical B token position, not a fixed absolute position.
- Seeds: 20260521, 20260522, 20260523.
- Training: 1600 steps, 4-GPU ACP job `pt-ah9hhx0s`, run name `a05_04_forced_feature_init_trajectory_4gpu_20260609`.

## Variants

| Variant | Meaning |
|---|---|
| `V0_vanilla_random` | vanilla random top-1 router |
| `V1_random_balanced_init` | random candidate init selected for more balanced step-0 routing |
| `V2_feature_init_trainable` | feature/slot-directed router initialization, trainable |
| `V3_oracle_frozen` | frozen oracle slot router |
| `V4_feature_init_inhibition` | feature/slot-directed initialization plus inhibition |

## Primary Metrics

`max_load=0.25` is ideal load balance for 4 experts, but load balance alone is not specialization. The decisive specialization metric is route-slot normalized mutual information (`route_slot_nmi`): `1.0` means slot identity fully determines the routed expert.

| variant                    |   num_seeds |   route_slot_nmi_mean |   route_slot_nmi_std |   max_load_mean |   max_load_std |   target_accuracy_mean |   probe_slot_from_h_mean |
|:---------------------------|------------:|----------------------:|---------------------:|----------------:|---------------:|-----------------------:|-------------------------:|
| V0_vanilla_random          |           3 |                 0.000 |                0.000 |           1.000 |          0.000 |                  1.000 |                    1.000 |
| V1_random_balanced_init    |           3 |                 0.441 |                0.143 |           0.794 |          0.051 |                  1.000 |                    1.000 |
| V2_feature_init_trainable  |           3 |                 0.289 |                0.408 |           0.833 |          0.236 |                  1.000 |                    1.000 |
| V3_oracle_frozen           |           3 |                 1.000 |                0.000 |           0.250 |          0.000 |                  1.000 |                    1.000 |
| V4_feature_init_inhibition |           3 |                 0.236 |                0.333 |           0.833 |          0.236 |                  1.000 |                    1.000 |

## Key Evidence

![Final slot route heatmaps](figures/a05_04_forced_feature_init_trajectory_4gpu_20260609/report/final_slot_route_heatmaps_by_seed.png)

Interpretation: `V3_oracle_frozen` gives perfect one-slot-one-expert routing in all seeds; `V2` and `V4` only recover structured routing in seed 20260522 and collapse in the other two seeds.

![Per-seed trajectory](figures/a05_04_forced_feature_init_trajectory_4gpu_20260609/report/trajectory_by_seed.png)

Interpretation: all variants learn the target, but only oracle routing remains stably specialized across seeds; trainable routing has strong seed dependence after position removal.

## Main Observations

1. Representation visibility is not the bottleneck: `probe_slot_from_h=1.0` for every final run.
2. The target task is compatible with perfect specialization: `V3_oracle_frozen` reaches `accuracy=1.0`, `NMI=1.0`, and `max_load=0.25` in all seeds.
3. Vanilla routing collapses: `V0` has final `NMI=0.0`, `max_load=1.0`, and one active expert in all seeds.
4. Balanced random init weakens collapse but does not solve specialization: `V1` keeps partial structure, final `NMI=0.301/0.384/0.637`.
5. Current feature-init and inhibition are not robust under randomized feature position: `V2` and `V4` succeed only in seed 20260522 and fail in seeds 20260521/20260523.

## Claim Boundary

Can claim: slot-level specialization is feasible and useful in this no-position/random-position setting when routing is externally forced.

Can claim: the trainable top-1 router does not reliably discover or preserve that specialization under the tested initialization/inhibition controls.

Cannot claim: inhibition is generally ineffective; only the current implementation and hyperparameters were tested.

Cannot claim: full multi-B feature-level specialization has been solved or ruled out; this run is a one-B slot-level diagnostic.

## Next Decision

Do not continue position-source ablations as the main bottleneck. The next minimal test should isolate why trainable routing fails to preserve the oracle-feasible partition: either a stronger feature-aligned initialization that is verified at step 0, or a frozen-to-trainable release schedule that starts from the oracle partition and measures when/why it breaks.
