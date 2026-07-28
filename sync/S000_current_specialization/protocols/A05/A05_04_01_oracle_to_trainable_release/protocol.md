# A05_04 Protocol: Oracle-To-Trainable Router Release

## Question

After no-position/random-position slot specialization is verified under frozen oracle routing, does specialization fail because the router cannot be initialized into the partition, or because training cannot preserve the partition after the router is released?

## Design

Use the same one-B no-position/random-position setting as A05_04.

1. Train with oracle slot routing forced at the logical B token.
2. At a chosen release step, calibrate the linear router to reproduce the oracle slot-to-expert map from current hidden states.
3. Verify natural top-1 routing immediately after calibration.
4. Continue training without forced routing and track when `route_slot_nmi` drops or `max_load` rises.

## Variants

| Variant | Meaning |
|---|---|
| `O0_oracle_frozen_all` | oracle route forced throughout training |
| `R1_release50_plain` | oracle warmup, calibrated router release at step 50 |
| `R2_release100_plain` | oracle warmup, calibrated router release at step 100 |
| `R3_release200_plain` | oracle warmup, calibrated router release at step 200 |
| `R4_release100_inhibition` | release at step 100 plus the current inhibition loss |
| `R5_release100_route_ce` | release at step 100 plus explicit slot-to-router retention loss |

## Primary Metrics

- `route_slot_nmi`
- `max_load`
- `active_experts`
- `target_accuracy`
- `post_calibration_nmi`
- first post-release checkpoint where `route_slot_nmi < 0.95`
- first post-release checkpoint where `max_load > 0.35`

## Interpretation

- If post-calibration natural routing is not specialized, the failure is still an initialization / linear separability / calibration failure.
- If post-calibration natural routing is specialized but later decays, the failure is training-time preservation.
- If retention or inhibition preserves routing after the same verified start, the mechanism is a stabilization problem, not impossibility of slot specialization.

## Boundary

This is still a one-B slot-level diagnostic. It does not decide the full multi-B exact-feature problem.
