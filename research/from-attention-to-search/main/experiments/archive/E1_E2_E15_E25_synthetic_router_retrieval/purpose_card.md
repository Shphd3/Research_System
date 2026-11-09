# Experiment Card: E1/E2 and E1.5/E2.5 Synthetic Router Retrieval

Hypothesis: MoE/H-MoE expert/path buckets can be used as candidate KV indexes for block2 attention.

Question: After training, do router-ranked buckets recover dense block2 attention contributors better than random/local candidates?

Setup: `TransformerBlock1 -> Router/MoE/H-MoE -> TransformerBlock2`. Compare `flat_lb_on`, `spectral_midband_router`, `hmoe_lb_on`, `hmoe_lb_off`. H-MoE has 5 routers: 1 outer + 4 inner, 16 paths.

Tasks:
- E1: synthetic next-token prediction, target `next_token_id`, loss CE.
- E2: retrieval-only analysis over E1 checkpoints.
- E1.5: synthetic reconstruction, target `y_t`, loss MSE.
- E2.5: retrieval-only analysis over E1.5 checkpoints.

Data Difference:
- E1 uses the same latent atom/rule source but emits a discrete next-token label.
- E1.5 emits continuous `y_t` from the h-to-y operator.
- Oracle candidates are diagnostics only, never training labels.

Allowed / Forbidden Losses:
- E1 uses CE; E1.5 uses MSE.
- `flat_lb_on` and `hmoe_lb_on` add LB loss only.
- `spectral_midband_router` and `hmoe_lb_off` use no auxiliary loss.
- Do not add router CE, feature CE, spectral CE, contrastive loss, entropy regularization, orthogonality regularization, or retrieval-aware training.

Spectral Variant:
- `spectral_midband_router` routes on the middle 50% variance eigenspace from EMA mean/covariance of block1 hidden states.
- It drops top 25% and bottom 25% eigenvectors; for `d_model=64`, keep eig indices 16..47.
- It uses no spectral labels and no spectral loss.

Parameter Balance:
- Same `d_model`, heads, sequence length, seed, train steps, data budget, candidate budget.
- Same 16 routing buckets: flat/spectral 16 buckets vs H-MoE 4x4 paths.
- Match active-parameter budget as closely as implementation allows.
- Report `total_params`, `active_params_per_token`, `router_params`, and `expert_params`.
- Current runner also reports `actual_forward_params_per_token`; if soft expert mixing computes all experts, use the active count only as a matched-budget proxy and do not claim sparse MoE execution.

Baselines: `full_kv`, `oracle_topm`, `oracle_feature_overlap`, `local_window`, `random_matched`.

Metrics: convergence, dense attention sparsity, top-k dense recall, attention-mass recall, candidate ratio, output error, CE delta for E2, MSE delta for E2.5, router entropy/utilization, feature-to-path heatmap, parameter counts.

Expected Outcomes: router cumulative-K improves over random/local and approaches oracle; H-MoE may improve retrieval-quality tradeoff over flat under matched 16-bucket budget.

Can Prove: whether router buckets are useful candidate generators in this controlled setup.

Cannot Prove: real speedup, real-LM transfer, or human-interpretable hierarchy.

Status: planned.

Required Figures: loss comparison, dense attention top-M mass, Mass90/effective support, top-k recall, attention-mass recall, candidate ratio vs recall, output error, rank-K-only contribution, routing heatmaps, parameter-count comparison.

Next Decision: if E2/E2.5 are non-random and improve with K at useful candidate ratio, decide whether DCLM transfer is worth running.
