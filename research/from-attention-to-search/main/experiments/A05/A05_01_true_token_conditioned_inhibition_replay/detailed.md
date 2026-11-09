# H0605a Detailed: True Token-Conditioned Inhibition Replay

## Purpose

This experiment tests whether a token-conditioned inhibition loss can improve feature-level MoE routing beyond initialization alone.

The target feature definition is the atomic feature key \((slot,B_i)\). The primary metric is `FeatureKeyConsistency`, but all claims are gated by non-collapse.

## Mechanism Tested

For the B-position hidden state \(h\), the current top-1 expert is \(e^+\). The loss pulls \(h\) toward \(w_{e^+}\) and pushes it away from top-\(k\) competing experts plus the remaining non-selected experts.

No center separation, no supervised token-margin, no feature separation objective.

## Implementation

Files:

- runner: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_h0605a_true_token_conditioned_inhibition_replay.py`
- config: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/h0605a_true_token_conditioned_inhibition_replay.json`
- submit: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_h0605a_true_token_conditioned_inhibition_replay_4gpu_acp.sh`
- anchor/protocol source: `main/problem_anchors/05_failure_mechanism/05_01_geometric_inhibition_anchor.md`

Router bias check:

- `tiny_moe.py` uses `nn.Linear(d_model, num_experts, bias=False)` for the router.

Final inhibition hyperparameters:

- `loss_weight=0.01`
- `pull_weight=0.1`
- `topk_weight=1.0`
- `other_weight=0.25`
- `top_k_negatives=2`
- `topk_margin=0.5`
- `other_margin=0.25`

The weight was reduced from `0.1` after smoke testing showed immediate collapse even for `S1-cos`.

## Data And Training

Data:

- uniform multi-B synthetic
- `num_slots=4`
- `num_experts=4`
- `b_token_count_multi=256`
- `variants_per_key=16`
- feature key: \((slot,B_i)\)

Training:

- model: `top1_selected_gate`
- `d_model=128`, `ffn_dim=256`, `n_heads=4`
- steps: `1600`
- batch size: `384`
- AdamW, lr `8e-4`, weight decay `0.01`, grad clip `1.0`
- seeds: `20260521`, `20260522`, `20260523`

Run:

- ACP job: `pt-hqdf7c8x`
- state: `SUCCEEDED`
- runtime log: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/h0605a_true_token_conditioned_inhibition_replay_4gpu_20260604_runtime_20260604_150329.log`

## Conditions

| Code | Router | Init | Objective |
|---|---|---|---|
| R0-dot | dot-product | random | NTP only |
| R1-dot | dot-product | random | NTP + token-conditioned inhibition |
| S0-dot | dot-product | slot init | NTP only |
| S1-dot | dot-product | slot init | NTP + token-conditioned inhibition |
| R0-cos | cosine | random | NTP only |
| R1-cos | cosine | random | NTP + token-conditioned inhibition |
| S0-cos | cosine | slot init | NTP only |
| S1-cos | cosine | slot init | NTP + token-conditioned inhibition |

## Collapse Rule

A seed is treated as collapsed and removed from the minimal specialization comparison if:

- `active_experts <= 1`, or
- `expert_load_max_fraction >= 0.95`.

Seeds with `max_load=0.75` are not hard-collapsed by this rule, but they are partial-concentration cases and should not be read as robust success.

## Final By-Seed Evidence

See:

- `tables/summary_by_seed.csv`
- `tables/noncollapsed_summary.csv`
- `tables/feature_key_consistency_by_condition.csv`

Decision-relevant final facts:

- `R1-dot`: 0/3 non-collapsed seeds.
- `R1-cos`: 1/3 non-collapsed seeds.
- `S1-dot`: 2/3 non-collapsed seeds, but both kept seeds have max load `0.75` and only 2 active experts.
- `S1-cos`: 2/3 non-collapsed seeds; seed `20260523` is excellent, seed `20260521` is concentrated, seed `20260522` collapses.

## Non-Collapsed Summary

| Condition | Kept / Total | FeatureKeyConsistency | Entropy Norm | Max Load | Route-Slot NMI | Route-FeatureKey NMI | Accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|
| R0-dot | 2 / 3 | 0.9981 | 0.5694 | 0.5925 | 0.5183 | 0.3356 | 0.9998 |
| R1-dot | 0 / 3 | n/a | n/a | n/a | n/a | n/a | n/a |
| S0-dot | 2 / 3 | 0.9948 | 0.7513 | 0.5514 | 0.6355 | 0.3834 | 0.9995 |
| S1-dot | 2 / 3 | 1.0000 | 0.4056 | 0.7500 | 0.6369 | 0.2848 | 1.0000 |
| R0-cos | 3 / 3 | 0.9945 | 0.4643 | 0.6680 | 0.3132 | 0.2943 | 0.9983 |
| R1-cos | 1 / 3 | 1.0000 | 0.4905 | 0.5811 | 0.5381 | 0.3132 | 1.0000 |
| S0-cos | 2 / 3 | 0.9986 | 0.8694 | 0.4067 | 0.8566 | 0.4151 | 0.9998 |
| S1-cos | 2 / 3 | 1.0000 | 0.7028 | 0.5000 | 0.8184 | 0.3660 | 1.0000 |

## Figure Interpretation

![Feature-key consistency histogram](figures/feature_key_consistency_histogram.png)

This answers the weak question: does each \((slot,B_i)\) route consistently? Yes. But the figure alone cannot distinguish specialization from collapse.

![Expert load distribution](figures/expert_load_distribution.png)

This is the decisive guard. Inhibition makes several runs perfectly consistent by routing everything to one expert. Therefore high consistency is not specialization evidence.

![Feature-key route heatmap](figures/feature_key_route_heatmap.png)

This shows the seed-level structure. `S1-cos` seed `20260523` is the strongest positive case, with balanced use of four experts and route-slot NMI near 1. But `S1-cos` seed `20260522` collapses and seed `20260521` uses two experts heavily.

![Feature main-expert composition](figures/feature_main_expert_composition_s0_s1_cos_by_seed.png)

This is the central figure for "different feature to different expert." Each cell is the fraction of \(B_i\) keys inside one slot whose main expert is a given expert.

Reading:

- `S0-cos` seed `20260521`: mostly a clean slot-to-expert map, except slot 3 has some split.
- `S0-cos` seed `20260522`: all slots go to expert 3, so it is collapse.
- `S0-cos` seed `20260523`: mostly slot-to-expert, but slots 0 and 2 share expert 2.
- `S1-cos` seed `20260521`: slot 0 goes to expert 0, but slots 1/2/3 all go to expert 2.
- `S1-cos` seed `20260522`: all slots go to expert 3, so it is collapse.
- `S1-cos` seed `20260523`: clean one-slot-to-one-expert mapping.

Therefore the positive H0605a evidence is slot-level composition, not fine-grained \((slot,B_i)\) composition.

All-seed versions for every condition are stored under `figures/all_seed_feature_heatmaps/`. Each condition has:

- feature main-expert composition by seed;
- main expert feature map by seed;
- feature-to-expert probability matrix by seed.

Complete all-seed figure index:

| Condition | Composition | Main expert map | Probability matrix |
|---|---|---|---|
| R0-dot | `figures/all_seed_feature_heatmaps/R0-dot_feature_main_expert_composition_by_seed.png` | `figures/all_seed_feature_heatmaps/R0-dot_main_expert_feature_map_by_seed.png` | `figures/all_seed_feature_heatmaps/R0-dot_feature_to_expert_probability_matrix_by_seed.png` |
| R1-dot | `figures/all_seed_feature_heatmaps/R1-dot_feature_main_expert_composition_by_seed.png` | `figures/all_seed_feature_heatmaps/R1-dot_main_expert_feature_map_by_seed.png` | `figures/all_seed_feature_heatmaps/R1-dot_feature_to_expert_probability_matrix_by_seed.png` |
| S0-dot | `figures/all_seed_feature_heatmaps/S0-dot_feature_main_expert_composition_by_seed.png` | `figures/all_seed_feature_heatmaps/S0-dot_main_expert_feature_map_by_seed.png` | `figures/all_seed_feature_heatmaps/S0-dot_feature_to_expert_probability_matrix_by_seed.png` |
| S1-dot | `figures/all_seed_feature_heatmaps/S1-dot_feature_main_expert_composition_by_seed.png` | `figures/all_seed_feature_heatmaps/S1-dot_main_expert_feature_map_by_seed.png` | `figures/all_seed_feature_heatmaps/S1-dot_feature_to_expert_probability_matrix_by_seed.png` |
| R0-cos | `figures/all_seed_feature_heatmaps/R0-cos_feature_main_expert_composition_by_seed.png` | `figures/all_seed_feature_heatmaps/R0-cos_main_expert_feature_map_by_seed.png` | `figures/all_seed_feature_heatmaps/R0-cos_feature_to_expert_probability_matrix_by_seed.png` |
| R1-cos | `figures/all_seed_feature_heatmaps/R1-cos_feature_main_expert_composition_by_seed.png` | `figures/all_seed_feature_heatmaps/R1-cos_main_expert_feature_map_by_seed.png` | `figures/all_seed_feature_heatmaps/R1-cos_feature_to_expert_probability_matrix_by_seed.png` |
| S0-cos | `figures/all_seed_feature_heatmaps/S0-cos_feature_main_expert_composition_by_seed.png` | `figures/all_seed_feature_heatmaps/S0-cos_main_expert_feature_map_by_seed.png` | `figures/all_seed_feature_heatmaps/S0-cos_feature_to_expert_probability_matrix_by_seed.png` |
| S1-cos | `figures/all_seed_feature_heatmaps/S1-cos_feature_main_expert_composition_by_seed.png` | `figures/all_seed_feature_heatmaps/S1-cos_main_expert_feature_map_by_seed.png` | `figures/all_seed_feature_heatmaps/S1-cos_feature_to_expert_probability_matrix_by_seed.png` |

![S1-cos all-seed feature composition](figures/all_seed_feature_heatmaps/S1-cos_feature_main_expert_composition_by_seed.png)

This is the checked all-seed version for the key condition. It shows one partial-concentration seed, one collapse seed, and one clean four-expert slot map.

![S1-cos feature-to-expert probability matrix](figures/all_seed_feature_heatmaps/S1-cos_feature_to_expert_probability_matrix_by_seed.png)

Rows are feature keys sorted by slot and \(B_i\); columns are experts. This separates consistency from composition: rows are mostly one-hot, so each feature key is stable, but one-hot rows can still all choose the same expert.

![Main expert feature map](figures/main_expert_feature_map_s0_s1_cos_by_seed.png)

This shows the same fact as a slot-by-\(B_i\) map. The vertical uniform bands show that the router mostly binds to slot identity rather than varying across \(B_i\) inside a slot.

![Route-slot NMI trajectory](figures/route_slot_nmi_trajectory.png)

This shows that some conditions lock their routing early. Inhibition can stabilize a chosen routing pattern, but if the early selected pattern is collapsed, the same lock-in effect preserves collapse.

## Interpretation

The inhibition loss is a strong self-reinforcement mechanism. Because \(e^+\) is selected by the current router, the loss rewards the router for becoming more confident in its own current assignment. If the early assignment is balanced, this can preserve a clean structure. If the early assignment is imbalanced, it amplifies collapse.

Therefore, H0605a does not support using this loss as-is for the next route-utility binding stage.

For different-feature assignment, the most precise interpretation is:

- If "feature" means slot, then `S1-cos` seed `20260523` gives a strong positive example.
- If "feature" means atomic \((slot,B_i)\), then H0605a does not show robust different-feature-to-different-expert specialization. It mostly routes all \(B_i\) within the same slot to the same expert.

## Claim Boundary

Supported:

- Token-conditioned inhibition can create perfect same-feature consistency.
- A strong positive case exists: `S1-cos`, seed `20260523`, non-collapsed, balanced, route-slot NMI `1.0`.

Weakened:

- The mechanism is not robust across seeds.
- Compared with `S0-cos`, `S1-cos` does not improve the non-collapsed mean route-slot NMI or route-feature-key NMI.
- The routed feature axis appears closer to slot than to atomic \((slot,B_i)\) in the successful cases.

Rejected for now:

- Do not claim that token-conditioned inhibition solves expert specialization.
- Do not move it directly into utility-binding experiments.

## Next Decision

Run a mechanism audit before using inhibition again:

1. Is collapse caused mainly by selected-expert self-reinforcement?
2. Would stop-gradient on \(e^+\), entropy/load guard, or delayed activation prevent collapse?
3. Should inhibition be applied only after slot-init reaches a non-collapsed state?
