# A05_04 Detailed: Oracle-To-Trainable Router Release

## 1. Question

A05_04 showed that oracle slot routing is feasible, while trainable random / feature-init / inhibition variants do not reliably form slot-level specialization. A05_04 release asks the next diagnostic question:

If the router is first placed into a verified oracle slot partition, does normal trainable top-1 training destroy that partition?

## 2. Setup

- Data setting: one-B discriminative uniform slot setting.
- Position control: positional embedding is zeroed and frozen, and the logical feature block is randomly positioned.
- Routing position: logical B token position.
- Slots / experts: 4 slots, 4 experts.
- Seeds: `20260521`, `20260522`, `20260523`.
- Router metric: cosine.
- Training length: 1600 steps.
- ACP job: `pt-k5157gw2`.
- Run name: `a05_05_oracle_to_trainable_release_4gpu_20260609`.

Release procedure:

1. Train with oracle slot routing forced at the logical B token.
2. At release step, calibrate router weights to reproduce the slot-to-expert map from current hidden states.
3. Verify natural top-1 routing immediately after calibration.
4. Continue normal trainable routing without force.

## 3. Variants

| Variant | Release step | Regularizer after release | Purpose |
|---|---:|---|---|
| `O0_oracle_frozen_all` | none | none | positive control |
| `R1_release50_plain` | 50 | none | early release |
| `R2_release100_plain` | 100 | none | mid release |
| `R3_release200_plain` | 200 | none | later release |
| `R4_release100_inhibition` | 100 | current inhibition loss | test whether inhibition stabilizes released routing |
| `R5_release100_route_ce` | 100 | supervised route retention CE | diagnostic upper-bound stabilizer |

## 4. Primary Metrics

- `route_slot_nmi`: primary specialization metric; `1.0` means slot identity fully determines routed expert.
- `max_load`: largest expert load fraction at the logical B token; `0.25` is ideal for 4 experts.
- `post_calibration_nmi`: whether the released natural router starts from the intended partition.
- `first_nmi_below_0.95`: first post-release checkpoint where specialization meaningfully erodes.
- `first_max_load_above_0.35`: first post-release checkpoint where load concentration begins.
- `target_accuracy`: target prediction validity check.

## 5. Summary Table

| variant                  |   num_seeds |   route_slot_nmi_mean |   route_slot_nmi_std |   max_load_mean |   max_load_std |   target_accuracy_mean |   active_experts_mean |
|:-------------------------|------------:|----------------------:|---------------------:|----------------:|---------------:|-----------------------:|----------------------:|
| O0_oracle_frozen_all     |           3 |                 1.000 |                0.000 |           0.250 |          0.000 |                  1.000 |                 4.000 |
| R1_release50_plain       |           3 |                 1.000 |                0.000 |           0.250 |          0.000 |                  1.000 |                 4.000 |
| R2_release100_plain      |           3 |                 0.971 |                0.049 |           0.264 |          0.025 |                  1.000 |                 4.000 |
| R3_release200_plain      |           3 |                 1.000 |                0.000 |           0.250 |          0.000 |                  1.000 |                 4.000 |
| R4_release100_inhibition |           3 |                 1.000 |                0.000 |           0.250 |          0.000 |                  1.000 |                 4.000 |
| R5_release100_route_ce   |           3 |                 1.000 |                0.000 |           0.250 |          0.000 |                  1.000 |                 4.000 |

Interpretation: almost every released run preserves perfect slot specialization. The only non-perfect final run is `R2_release100_plain` seed `20260521`, and it remains close to balanced rather than collapsed.

## 6. Release Transition By Seed

| variant                  |     seed |   release_step |   post_calibration_nmi |   post_calibration_max_load |   first_nmi_below_0.95 |   first_max_load_above_0.35 |   final_nmi |   final_max_load |   final_accuracy |
|:-------------------------|---------:|---------------:|-----------------------:|----------------------------:|-----------------------:|----------------------------:|------------:|-----------------:|-----------------:|
| O0_oracle_frozen_all     | 20260521 |                |                        |                             |                        |                             |       1.000 |            0.250 |            1.000 |
| O0_oracle_frozen_all     | 20260522 |                |                        |                             |                        |                             |       1.000 |            0.250 |            1.000 |
| O0_oracle_frozen_all     | 20260523 |                |                        |                             |                        |                             |       1.000 |            0.250 |            1.000 |
| R1_release50_plain       | 20260521 |             50 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |
| R1_release50_plain       | 20260522 |             50 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |
| R1_release50_plain       | 20260523 |             50 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |
| R2_release100_plain      | 20260521 |            100 |                  1.000 |                       0.250 |                   1600 |                             |       0.914 |            0.293 |            1.000 |
| R2_release100_plain      | 20260522 |            100 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |
| R2_release100_plain      | 20260523 |            100 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |
| R3_release200_plain      | 20260521 |            200 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |
| R3_release200_plain      | 20260522 |            200 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |
| R3_release200_plain      | 20260523 |            200 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |
| R4_release100_inhibition | 20260521 |            100 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |
| R4_release100_inhibition | 20260522 |            100 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |
| R4_release100_inhibition | 20260523 |            100 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |
| R5_release100_route_ce   | 20260521 |            100 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |
| R5_release100_route_ce   | 20260522 |            100 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |
| R5_release100_route_ce   | 20260523 |            100 |                  1.000 |                       0.250 |                        |                             |       1.000 |            0.250 |            1.000 |

Interpretation: calibration succeeded in every released run. No released run crossed the load-concentration threshold `max_load > 0.35`. Only one run crossed `route_slot_nmi < 0.95`, and only at the final checkpoint.

## 7. Figures

### Figure 1: Per-Seed Release Trajectories

![Release trajectories by seed](figures/a05_05_oracle_to_trainable_release_4gpu_20260609/release_trajectory_by_seed.png)

Interpretation: released routers remain at or near `NMI=1.0` and `max_load=0.25` after release. The only visible degradation is the late mild decline of `R2_release100_plain` in seed `20260521`.

### Figure 2: Final Slot-To-Expert Routing

![Final route heatmaps](figures/a05_05_oracle_to_trainable_release_4gpu_20260609/final_release_route_heatmaps_by_seed.png)

Interpretation: final heatmaps are diagonal in all runs except `R2_release100_plain` seed `20260521`, where slot 0 has a small spillover to expert 2.

## 8. The One Mild Erosion Case

`R2_release100_plain`, seed `20260521`:

| step | event | NMI | max load | accuracy |
|---:|---|---:|---:|---:|
| 100 | post-calibration natural | 1.000 | 0.250 | 1.000 |
| 101 | post-release natural | 1.000 | 0.250 | 1.000 |
| 800 | post-release natural | 0.970 | 0.260 | 1.000 |
| 1600 | post-release natural | 0.914 | 0.293 | 1.000 |

Interpretation: this is slow erosion, not collapse. All experts remain active and load remains close to balanced.

## 9. Answers

### Does a verified specialized router immediately collapse after release?

No. Every released run starts from `post_calibration_nmi=1.0` and `post_calibration_max_load=0.25`. Almost all remain perfect through step 1600.

### Is A05_04 mainly evidence for training-time preservation failure?

Weakened. A05_04 release shows that once the router is actually placed in the correct partition, standard training can mostly preserve it. Therefore A05_04's failure is more likely because the trainable router did not enter the correct partition.

### Does inhibition solve a collapse that plain release cannot solve?

Not strongly in this setting, because plain release already mostly works. However, at release step 100, inhibition and route-CE both remove the one mild erosion case seen in plain release.

### Does this solve feature specialization?

No. It proves a diagnostic: the slot-level partition is stable after verified entry. It does not provide an unsupervised method for entering the partition.

## 10. Interpretation

The experiment separates two hypotheses:

1. Initialization / basin-entry failure: the router fails because it does not reach the useful slot partition.
2. Training preservation failure: the router reaches the useful slot partition, but training destroys it.

The evidence supports hypothesis 1 more strongly. A verified slot partition is stable under normal training in this one-B setting. This means the next hard problem is how the router can enter the partition without an oracle/calibration signal.

## 11. Claim Boundary

Can claim:

- The no-position/random-position slot partition can be calibrated into a natural top-1 router.
- Once calibrated, the partition is mostly preserved through 1600 training steps.
- Collapse in A05_04 is not an inevitable consequence of training after correct specialization is established.

Cannot claim:

- The multi-B exact-feature setting will behave the same way.
- Calibration is an unsupervised solution.
- Longer training or more seeds would never erode the partition.
- Inhibition is generally unnecessary; it was not needed for most runs here, but it did remove the one mild erosion case.

## 12. Next Decision

Return to the harder multi-B exact-feature setting with the same separation test:

1. verify that oracle/calibrated exact-feature routing can be preserved;
2. then test whether an unsupervised or weakly supervised router can enter that partition.

If exact-feature oracle release is stable, the mainline problem becomes route-entry / feature-aligned initialization. If exact-feature oracle release fails, the problem becomes preservation under a harder feature definition.

## 13. Artifact Map

- Experiment folder: `Projects/from-attention-to-search/main/experiments/A05/A05_04_01_oracle_to_trainable_release/`
- Protocol: `protocol.md`
- Runner: `scripts/run_a05_04_oracle_to_trainable_release.py`
- ACP submit script: `scripts/submit_a05_04_oracle_release_4gpu_acp.sh`
- ACP job id: `pt-k5157gw2`
- Runtime log: `logs/acp/a05_05_oracle_to_trainable_release_4gpu_20260609_runtime_20260609_052209.log`
- Result dir: `results/a05_05_oracle_to_trainable_release_4gpu_20260609/`
- Figure dir: `figures/a05_05_oracle_to_trainable_release_4gpu_20260609/`
- Main tables: `summary_by_variant.csv`, `release_transition_by_seed.csv`, `final_metrics_by_seed.csv`, `metrics_by_step.csv`, `route_matrix_by_step.csv`, `utility_matrix_by_step.csv`, `logit_decomposition_by_step.csv`, `gradient_decomposition_by_step.csv`
