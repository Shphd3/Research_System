# A05_04 Detailed: No-Position Forced Feature-Init Trajectory

## 1. Question

In the no-position, randomized routed-position uniform toy setting, does the failure of MoE specialization come from missing slot information, lack of slot-routing utility, or unstable trainable top-1 routing?

## 2. Setup

This experiment audits slot-level specialization after removing fixed positional signals.

- Base protocol: H0605a true-token-conditioned inhibition replay config.
- Data: one-B discriminative uniform setting.
- Logical units: 4 slots and 4 experts.
- Target rule: slot-specific target token.
- Position removal: positional embedding is set to zero and frozen for the whole run.
- Position randomization: the logical B token appears at randomized valid positions; route analysis uses the logical B token position.
- Seeds: `20260521`, `20260522`, `20260523`.
- Training: 1600 steps.
- Router metric: cosine.
- ACP job: `pt-ah9hhx0s`.
- Run name: `a05_04_forced_feature_init_trajectory_4gpu_20260609`.

Position support check:

| slot | valid_position_count | positions |
|---:|---:|---|
| 0 | 26 | 5-30 |
| 1 | 26 | 5-30 |
| 2 | 26 | 5-30 |
| 3 | 26 | 5-30 |

## 3. Variant Matrix

| Variant | Operational meaning | Main question |
|---|---|---|
| `V0_vanilla_random` | vanilla random top-1 router | Does ordinary routing collapse after position removal? |
| `V1_random_balanced_init` | random candidate init selected for more balanced step-0 routing | Does better initial load prevent collapse? |
| `V2_feature_init_trainable` | feature/slot-directed router initialization, trainable | Can a trainable slot-biased router preserve specialization? |
| `V3_oracle_frozen` | frozen oracle slot router | Is slot-level routing feasible and useful for the task? |
| `V4_feature_init_inhibition` | feature/slot-directed initialization plus inhibition | Does current inhibition stabilize feature-init routing? |

## 4. Metrics

- `route_slot_nmi`: normalized mutual information between logical slot id and routed expert at the logical B position. This is the primary specialization metric.
- `max_load`: largest expert load fraction at the logical B position. With 4 experts, `0.25` is ideal load balance, but it is not sufficient evidence for specialization without high `route_slot_nmi`.
- `active_experts`: number of experts used by the logical B tokens.
- `target_accuracy`: target-token prediction accuracy.
- `probe_slot_from_h`: linear probe accuracy for slot identity from the hidden state at the logical B position.
- `route_utility_match`: fraction where the router-selected expert matches the forced-routing best-loss expert at final evaluation.
- `common_ratio`: \(||mean_f h_f||^2 / mean_f ||h_f||^2\) at the logical B hidden centroid. This is recorded but is not the primary decision metric here.

## 5. Primary Result

| variant                    |   num_seeds |   route_slot_nmi_mean |   route_slot_nmi_std |   max_load_mean |   max_load_std |   target_accuracy_mean |   probe_slot_from_h_mean |   route_utility_match_mean |
|:---------------------------|------------:|----------------------:|---------------------:|----------------:|---------------:|-----------------------:|-------------------------:|---------------------------:|
| V0_vanilla_random          |           3 |                 0.000 |                0.000 |           1.000 |          0.000 |                  1.000 |                    1.000 |                      1.000 |
| V1_random_balanced_init    |           3 |                 0.441 |                0.143 |           0.794 |          0.051 |                  1.000 |                    1.000 |                      0.908 |
| V2_feature_init_trainable  |           3 |                 0.289 |                0.408 |           0.833 |          0.236 |                  1.000 |                    1.000 |                      1.000 |
| V3_oracle_frozen           |           3 |                 1.000 |                0.000 |           0.250 |          0.000 |                  1.000 |                    1.000 |                      1.000 |
| V4_feature_init_inhibition |           3 |                 0.236 |                0.333 |           0.833 |          0.236 |                  1.000 |                    1.000 |                      1.000 |

Interpretation: the model can predict the target in every condition, and the hidden state contains linearly decodable slot information in every final run. The difference is whether the router uses that information as a stable slot-to-expert partition.

## 6. Seed-Level Final Results

| variant                    |     seed |   route_slot_nmi |   max_load |   active_experts |   target_accuracy |   probe_slot_from_h |   route_utility_match |   common_ratio |
|:---------------------------|---------:|-----------------:|-----------:|-----------------:|------------------:|--------------------:|----------------------:|---------------:|
| V0_vanilla_random          | 20260521 |            0.000 |      1.000 |                1 |             1.000 |               1.000 |                 1.000 |          0.632 |
| V0_vanilla_random          | 20260522 |            0.000 |      1.000 |                1 |             1.000 |               1.000 |                 1.000 |          0.779 |
| V0_vanilla_random          | 20260523 |            0.000 |      1.000 |                1 |             1.000 |               1.000 |                 1.000 |          0.728 |
| V1_random_balanced_init    | 20260521 |            0.301 |      0.865 |                2 |             1.000 |               1.000 |                 0.885 |          0.590 |
| V1_random_balanced_init    | 20260522 |            0.384 |      0.767 |                3 |             1.000 |               1.000 |                 0.839 |          0.657 |
| V1_random_balanced_init    | 20260523 |            0.637 |      0.750 |                2 |             1.000 |               1.000 |                 1.000 |          0.640 |
| V2_feature_init_trainable  | 20260521 |            0.000 |      1.000 |                1 |             1.000 |               1.000 |                 1.000 |          0.583 |
| V2_feature_init_trainable  | 20260522 |            0.866 |      0.500 |                3 |             1.000 |               1.000 |                 1.000 |          0.727 |
| V2_feature_init_trainable  | 20260523 |            0.000 |      1.000 |                1 |             1.000 |               1.000 |                 1.000 |          0.666 |
| V3_oracle_frozen           | 20260521 |            1.000 |      0.250 |                4 |             1.000 |               1.000 |                 1.000 |          0.843 |
| V3_oracle_frozen           | 20260522 |            1.000 |      0.250 |                4 |             1.000 |               1.000 |                 1.000 |          0.913 |
| V3_oracle_frozen           | 20260523 |            1.000 |      0.250 |                4 |             1.000 |               1.000 |                 1.000 |          0.818 |
| V4_feature_init_inhibition | 20260521 |            0.000 |      1.000 |                1 |             1.000 |               1.000 |                 1.000 |          0.916 |
| V4_feature_init_inhibition | 20260522 |            0.707 |      0.500 |                2 |             1.000 |               1.000 |                 1.000 |          0.402 |
| V4_feature_init_inhibition | 20260523 |            0.000 |      1.000 |                1 |             1.000 |               1.000 |                 1.000 |          0.967 |

Interpretation: the outcome is seed-dependent for trainable structured controls. Seed 20260522 recovers structure under `V2` and `V4`; seeds 20260521 and 20260523 collapse. Therefore mean performance alone is misleading.

## 7. Figures

### Final Slot Routing

![Final slot route heatmaps](figures/a05_04_forced_feature_init_trajectory_4gpu_20260609/report/final_slot_route_heatmaps_by_seed.png)

Interpretation: `V3_oracle_frozen` is a clean positive control: all three seeds route each slot to a distinct expert. `V2` and `V4` show partial success only for seed 20260522.

### Per-Seed Dynamics

![Per-seed trajectory](figures/a05_04_forced_feature_init_trajectory_4gpu_20260609/report/trajectory_by_seed.png)

Interpretation: target accuracy reaches 1.0 across variants, but route specialization does not follow automatically. Routing structure is stable only when externally forced.

### Final Specialization Bars

![Final specialization bars](figures/a05_04_forced_feature_init_trajectory_4gpu_20260609/report/final_slot_specialization_by_seed.png)

Interpretation: `V3` is the only condition with high NMI, ideal max load, and all 4 active experts in every seed.

## 8. Collapse Timing

| variant                    |     seed |   first_step_max_load_ge_0.95 |   final_nmi |   final_max_load |   final_accuracy |
|:---------------------------|---------:|------------------------------:|------------:|-----------------:|-----------------:|
| V0_vanilla_random          | 20260521 |                         0.000 |       0.000 |            1.000 |            1.000 |
| V0_vanilla_random          | 20260522 |                        20.000 |       0.000 |            1.000 |            1.000 |
| V0_vanilla_random          | 20260523 |                         0.000 |       0.000 |            1.000 |            1.000 |
| V1_random_balanced_init    | 20260521 |                        10.000 |       0.301 |            0.865 |            1.000 |
| V1_random_balanced_init    | 20260522 |                        10.000 |       0.384 |            0.767 |            1.000 |
| V1_random_balanced_init    | 20260523 |                        10.000 |       0.637 |            0.750 |            1.000 |
| V2_feature_init_trainable  | 20260521 |                         0.000 |       0.000 |            1.000 |            1.000 |
| V2_feature_init_trainable  | 20260522 |                         0.000 |       0.866 |            0.500 |            1.000 |
| V2_feature_init_trainable  | 20260523 |                         0.000 |       0.000 |            1.000 |            1.000 |
| V3_oracle_frozen           | 20260521 |                              |       1.000 |            0.250 |            1.000 |
| V3_oracle_frozen           | 20260522 |                              |       1.000 |            0.250 |            1.000 |
| V3_oracle_frozen           | 20260523 |                              |       1.000 |            0.250 |            1.000 |
| V4_feature_init_inhibition | 20260521 |                         0.000 |       0.000 |            1.000 |            1.000 |
| V4_feature_init_inhibition | 20260522 |                         0.000 |       0.707 |            0.500 |            1.000 |
| V4_feature_init_inhibition | 20260523 |                         0.000 |       0.000 |            1.000 |            1.000 |

Interpretation: `V2` and `V4` are not clean step-0 successful feature-init controls in this randomized-position/no-position setting. They start from collapsed assignments, and only seed 20260522 later recovers structure.

## 9. Answers To The Audit Questions

### Q1. Is slot information visible in hidden states?

Yes. Final `probe_slot_from_h=1.0` for every variant and seed. This means the routed-position hidden state contains enough linearly accessible slot information. The router failure is not explained by absence of slot information in \(h\).

### Q2. Is slot-level routing useful for the target?

Yes. `V3_oracle_frozen` reaches `target_accuracy=1.0` with `route_slot_nmi=1.0`, `max_load=0.25`, and 4 active experts in every seed. Therefore a perfect slot-to-expert partition is compatible with the prediction objective.

### Q3. Does vanilla top-1 routing discover specialization after position removal?

No. `V0_vanilla_random` collapses to one active expert in all seeds while still reaching perfect target accuracy.

### Q4. Does balanced random initialization solve the issue?

No. `V1_random_balanced_init` improves structure relative to `V0`, but final NMI remains partial (`0.301`, `0.384`, `0.637`) and max load remains high (`0.865`, `0.767`, `0.750`).

### Q5. Does current feature-init solve the issue?

No. `V2_feature_init_trainable` succeeds only in seed 20260522 (`NMI=0.866`, `max_load=0.5`) and collapses in seeds 20260521 and 20260523. Also, it is not a successful step-0 feature-routing initialization under this randomized-position setup because step-0 routing is already collapsed.

### Q6. Does current inhibition solve the issue?

No. `V4_feature_init_inhibition` mirrors the seed dependence of `V2`: seed 20260522 partially succeeds (`NMI=0.707`, `max_load=0.5`), while the other two seeds collapse. This weakens the current inhibition implementation as a robust stabilization mechanism.

### Q7. What does route-utility match show?

At final evaluation, collapsed runs often have `route_utility_match=1.0` because the experts have co-adapted to the routing pattern. This does not prove that the initial route was utility-optimal. It only shows that final forced-routing utility is endogenous to the learned routing/expert state.

## 10. Interpretation

The decisive contrast is `V0/V2/V4` versus `V3`.

`V3_oracle_frozen` proves that slot-level specialization is both feasible and sufficient for perfect target prediction after removing positional embeddings and randomizing the logical feature position.

`V0` proves that ordinary trainable top-1 routing does not find this partition by itself.

`V2` and `V4` show that the current feature-init and inhibition mechanisms are not robust enough in the harder randomized-position setting. The result does not rule out feature initialization or inhibition in general; it says the current tested versions do not reliably create or preserve specialization.

## 11. Claim Boundary

Can claim:

- The target task does not require collapse: oracle slot routing solves it with perfect accuracy and perfect specialization.
- The hidden state contains slot information: the final probe is perfect in all conditions.
- The tested trainable router variants are not robust: only one of three seeds recovers structure under `V2`/`V4`.

Cannot claim:

- The full multi-B feature-level problem is solved; this is a one-B slot-level diagnostic.
- The current result proves the exact cause of trainable routing failure; it identifies the failure surface.
- Inhibition is generally ineffective; only the tested inhibition implementation and hyperparameters are audited.
- Final forced-routing utility identifies the causal initial utility landscape; experts co-adapt during training.

## 12. Next Decision

The next minimal experiment should not be another broad position ablation. It should directly test stability after a verified specialized start:

1. Start from frozen oracle slot routing until target accuracy is high.
2. Unfreeze the router with controlled release schedules.
3. Measure the first step where `route_slot_nmi` drops or `max_load` rises.
4. Compare no regularizer, load balance, inhibition, and explicit route-retention regularization.

This asks whether collapse is caused by failure to initialize the partition or by failure to keep it once expert-route co-adaptation begins.

## 13. Artifact Map

- Experiment folder: `Projects/from-attention-to-search/main/experiments/A05/A05_04_01_no_position_forced_feature_init_trajectory/`
- Protocol: `protocol.md`
- Runner: `scripts/run_a05_04_forced_feature_init_trajectory.py`
- ACP submit script: `scripts/submit_a05_04_forced_feature_init_trajectory_4gpu_acp.sh`
- Report asset script: `scripts/make_a05_04_report_assets.py`
- ACP job id: `pt-ah9hhx0s`
- Runtime log: `logs/acp/a05_04_forced_feature_init_trajectory_4gpu_20260609_runtime_20260609_032413.log`
- Result dir: `results/a05_04_forced_feature_init_trajectory_4gpu_20260609/`
- Figure dir: `figures/a05_04_forced_feature_init_trajectory_4gpu_20260609/`
- Report figure dir: `figures/a05_04_forced_feature_init_trajectory_4gpu_20260609/report/`
- Derived table dir: `tables/a05_04_forced_feature_init_trajectory_4gpu_20260609/`
- Main raw tables: `final_metrics_by_seed.csv`, `summary_by_variant.csv`, `metrics_by_step.csv`, `route_matrix_by_step.csv`, `utility_matrix_by_step.csv`, `logit_decomposition_by_step.csv`, `gradient_decomposition_by_step.csv`
