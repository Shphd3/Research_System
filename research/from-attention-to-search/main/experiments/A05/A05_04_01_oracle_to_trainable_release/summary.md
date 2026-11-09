# A05_04 Summary: Oracle-To-Trainable Router Release

## Question

After no-position/random-position oracle routing proves that slot specialization is feasible, does a verified specialized router collapse after it is released into normal trainable top-1 routing?

## One-Line Verdict

No: once the router is calibrated into the oracle slot partition, specialization is mostly preserved after release; the previous failure is therefore more likely an initialization / basin-entry failure than an unavoidable training-time preservation failure.

## Setup

- Base setting: same one-B no-position/random-position data as A05_04.
- Routing position: logical B token position.
- Experts / slots: 4 experts, 4 slots.
- Seeds: `20260521`, `20260522`, `20260523`.
- Training: 1600 steps.
- Job: ACP `pt-k5157gw2`, run `a05_05_oracle_to_trainable_release_4gpu_20260609`.
- Release procedure:
  1. train with forced oracle slot routing;
  2. calibrate router weights to reproduce slot-to-expert routing from current hidden states;
  3. verify natural top-1 routing;
  4. continue training without forced routing.

## Variants

| Variant | Meaning |
|---|---|
| `O0_oracle_frozen_all` | oracle routing forced throughout |
| `R1_release50_plain` | calibrated natural router released at step 50 |
| `R2_release100_plain` | calibrated natural router released at step 100 |
| `R3_release200_plain` | calibrated natural router released at step 200 |
| `R4_release100_inhibition` | step-100 release plus inhibition loss |
| `R5_release100_route_ce` | step-100 release plus explicit slot-route retention loss |

## Primary Result

| variant                  |   num_seeds |   route_slot_nmi_mean |   route_slot_nmi_std |   max_load_mean |   max_load_std |   target_accuracy_mean |   active_experts_mean |
|:-------------------------|------------:|----------------------:|---------------------:|----------------:|---------------:|-----------------------:|----------------------:|
| O0_oracle_frozen_all     |           3 |                 1.000 |                0.000 |           0.250 |          0.000 |                  1.000 |                 4.000 |
| R1_release50_plain       |           3 |                 1.000 |                0.000 |           0.250 |          0.000 |                  1.000 |                 4.000 |
| R2_release100_plain      |           3 |                 0.971 |                0.049 |           0.264 |          0.025 |                  1.000 |                 4.000 |
| R3_release200_plain      |           3 |                 1.000 |                0.000 |           0.250 |          0.000 |                  1.000 |                 4.000 |
| R4_release100_inhibition |           3 |                 1.000 |                0.000 |           0.250 |          0.000 |                  1.000 |                 4.000 |
| R5_release100_route_ce   |           3 |                 1.000 |                0.000 |           0.250 |          0.000 |                  1.000 |                 4.000 |

## Key Evidence

![Release trajectories by seed](figures/a05_05_oracle_to_trainable_release_4gpu_20260609/release_trajectory_by_seed.png)

Interpretation: after release, route-slot NMI stays at or near 1.0 and max load stays near 0.25; only `R2_release100_plain` seed 20260521 shows late mild erosion.

![Final route heatmaps](figures/a05_05_oracle_to_trainable_release_4gpu_20260609/final_release_route_heatmaps_by_seed.png)

Interpretation: final routing is diagonal for all conditions except a small slot-0 spillover in `R2_release100_plain` seed 20260521.

## Transition Judgment

All release variants had `post_calibration_nmi=1.0` and `post_calibration_max_load=0.25` in all seeds. Therefore the experiment achieved the intended verified specialized start.

Only one run crossed the `route_slot_nmi < 0.95` threshold: `R2_release100_plain`, seed `20260521`, at step 1600. No run crossed `max_load > 0.35`.

## Interpretation

This shifts the likely bottleneck from "training inevitably destroys the correct partition" to "the normal trainable router usually fails to enter the correct partition." Once the partition is established and verified, ordinary training can mostly preserve it in this slot-level setting.

Inhibition and route-retention are not needed for most seeds here, but they remove the one mild erosion case observed in plain step-100 release.

## Claim Boundary

Can claim:

- Verified oracle-to-natural release preserves slot-level specialization across almost all tested runs.
- The A05_04 trainable-router failure is more likely a basin-entry / initialization problem than a necessary training-preservation problem.

Cannot claim:

- The full multi-B feature-level task is solved.
- Calibration is a deployable unsupervised solution; it uses slot labels for the diagnostic.
- Training-time collapse cannot occur under longer runs, more seeds, or a harder feature definition.

## Next Decision

Move from one-B slot routing to the harder multi-B exact-feature setting, but keep the same decisive structure: first verify that a calibrated/oracle feature partition can be preserved, then remove supervision and test whether the router can enter that partition without labels.
