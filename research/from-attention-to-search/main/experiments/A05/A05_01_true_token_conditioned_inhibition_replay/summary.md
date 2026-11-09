# H0605a Summary: True Token-Conditioned Inhibition Replay

## Conclusion

Token-conditioned inhibition does not yet solve non-collapsed feature-level expert specialization. It makes same-feature routing extremely stable, but it also strongly increases collapse or partial concentration risk.

The useful reading is: same-feature consistency is easy; non-collapsed specialization is still the hard part.

## Question

Does true token-conditioned inhibition help route the same operational feature key \((slot,B_i)\) to the same expert, while also keeping different features distributed across experts?

## Result

Full 4-GPU run completed.

- ACP job: `pt-hqdf7c8x`
- status: `SUCCEEDED`
- run: `h0605a_true_token_conditioned_inhibition_replay_4gpu_20260604`
- code: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding`

Primary observation:

- All inhibition conditions reach near-perfect `FeatureKeyConsistency`.
- But random-init inhibition collapses badly.
- Slot-init inhibition is seed-sensitive.
- `S1-cos` has one excellent non-collapsed seed, one collapsed seed, and one partial-concentration seed.

## Non-Collapsed Final Metrics

Collapse filter: discard seeds with `active_experts <= 1` or `expert_load_max_fraction >= 0.95`.

| Condition | Kept / Total | FeatureKeyConsistency | Load Entropy Norm | Max Load | Route-Slot NMI | Route-FeatureKey NMI | Accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|
| R0-dot | 2 / 3 | 0.9981 | 0.5694 | 0.5925 | 0.5183 | 0.3356 | 0.9998 |
| R1-dot | 0 / 3 | n/a | n/a | n/a | n/a | n/a | n/a |
| S0-dot | 2 / 3 | 0.9948 | 0.7513 | 0.5514 | 0.6355 | 0.3834 | 0.9995 |
| S1-dot | 2 / 3 | 1.0000 | 0.4056 | 0.7500 | 0.6369 | 0.2848 | 1.0000 |
| R0-cos | 3 / 3 | 0.9945 | 0.4643 | 0.6680 | 0.3132 | 0.2943 | 0.9983 |
| R1-cos | 1 / 3 | 1.0000 | 0.4905 | 0.5811 | 0.5381 | 0.3132 | 1.0000 |
| S0-cos | 2 / 3 | 0.9986 | 0.8694 | 0.4067 | 0.8566 | 0.4151 | 0.9998 |
| S1-cos | 2 / 3 | 1.0000 | 0.7028 | 0.5000 | 0.8184 | 0.3660 | 1.0000 |

## Interpretation

`S1-cos` is the most important condition, but it does not beat `S0-cos` after removing collapsed seeds:

- FeatureKeyConsistency improves only trivially: `0.9986 -> 1.0000`.
- Load entropy worsens: `0.8694 -> 0.7028`.
- Route-slot NMI slightly worsens: `0.8566 -> 0.8184`.
- Route-feature-key NMI worsens: `0.4151 -> 0.3660`.

So the current inhibition loss is better described as a lock-in/sharpening force than as a robust specialization mechanism.

For the specific question "do different features enter different experts?", the answer is mostly no if feature means the atomic key \((slot,B_i)\). The better non-collapsed cases mostly show slot-level routing: all or nearly all \(B_i\) keys inside the same slot choose the same expert. The best `S1-cos` seed maps four slots cleanly to four experts, but it does not split different \(B_i\) keys within a slot.

## Key Figures

![Feature-key consistency histogram](figures/feature_key_consistency_histogram.png)

This figure shows why consistency alone is not enough: many collapsed runs also have perfect consistency.

![Expert load distribution](figures/expert_load_distribution.png)

This is the decisive collapse guard. The inhibition conditions frequently concentrate load into one or two experts.

![Feature-key route heatmap](figures/feature_key_route_heatmap.png)

This shows seed-level route composition. The `S1-cos` seed 20260523 is strong, but it is not stable across seeds.

![Feature main-expert composition](figures/feature_main_expert_composition_s0_s1_cos_by_seed.png)

This is the most direct figure for "different feature to different expert." Values show the fraction of \(B_i\) keys in each slot whose main expert is each expert. `S1-cos` seed 20260523 is a clean slot-to-expert mapping; `S1-cos` seed 20260522 collapses; `S1-cos` seed 20260521 uses only two experts.

All-seed versions for every condition are in `figures/all_seed_feature_heatmaps/`. The most important checked figures are:

- `figures/all_seed_feature_heatmaps/S0-cos_feature_main_expert_composition_by_seed.png`
- `figures/all_seed_feature_heatmaps/S1-cos_feature_main_expert_composition_by_seed.png`
- `figures/all_seed_feature_heatmaps/S1-cos_feature_to_expert_probability_matrix_by_seed.png`

![S1-cos all-seed feature composition](figures/all_seed_feature_heatmaps/S1-cos_feature_main_expert_composition_by_seed.png)

This all-seed figure shows the key point: one `S1-cos` seed is balanced and slot-aligned, one collapses, and one uses only two experts.

## Claim Boundary

Supported:

- Token-conditioned inhibition can make selected routing extremely stable.
- The weak advisor claim remains true: same feature keys can lock to the same expert.

Not supported:

- It does not robustly improve non-collapsed specialization.
- It does not consistently make different feature keys occupy better expert composition than slot-init cosine alone.
- It does not show robust fine-grained \((slot,B_i)\)-level expert differentiation; the non-collapsed structure is mostly slot-level.

## Next Decision

Do not move this loss directly into route-utility binding. The next step should be a mechanism audit of why token-conditioned self-reinforcement collapses: selected-expert positive feedback, top-1 discreteness, or loss weight/margin shape.
