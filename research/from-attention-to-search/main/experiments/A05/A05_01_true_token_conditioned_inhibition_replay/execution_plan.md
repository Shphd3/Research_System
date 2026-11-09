# H0605a True Token-Conditioned Inhibition Replay Execution Plan

## Conclusion

Run the H0604a feature-key stability diagnostic again, but replace center separation with true token-conditioned inhibition. The main judgment is whether inhibition improves non-collapsed same-feature routing and different-feature expert composition.

## Difference From H0604a

Same data, model size, seeds, train/eval split, and feature-key eval.

Changed part:

- H0604a tested center separation only.
- H0605a tests token-conditioned inhibition only.
- H0605a keeps random/slot init and dot/cos router ablations.
- H0605a does not include center separation or supervised token margin.

## Data And Training

Data is uniform multi-B synthetic:

\[
x_{s,i,r}=[r_{\mathrm{start}}, C_s, B_i, Y_{s,i}, r_{\mathrm{end}}]
\]

with nuisance variants for each \((slot=s,B_i)\).

Fixed settings:

- `num_slots=4`
- `num_experts=4`
- `b_token_count_multi=256`
- `train_samples_per_slot=5000`
- `eval_samples_per_slot=1600`
- `variants_per_key=16`
- seeds: `20260521, 20260522, 20260523`
- model: `top1_selected_gate`, no router bias
- `d_model=128`, `ffn_dim=256`, `n_heads=4`
- steps: `1600`, smoke steps: `80`
- batch size: `384`
- optimizer: AdamW, lr `8e-4`, weight decay `0.01`, grad clip `1.0`
- inhibition total weight: `0.01`

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

## Metrics And Required Figures

Primary:

- `FeatureKeyConsistency`
- `expert_load_entropy_norm`, `expert_load_max_fraction`, `active_experts`
- `route_feature_key_nmi`
- `within_slot_main_expert_diversity`
- `target_accuracy_feature_eval`

Figures:

- `feature_key_consistency_histogram.png`: same-feature lock-in strength.
- `expert_load_distribution.png`: collapse guard.
- `feature_key_route_heatmap.png`: whether different \((slot,B_i)\) keys occupy different experts.
- `checkpoint_feature_drift.png`: whether feature routing is stable over training.
- `route_slot_heatmap_step0_final.png`: slot-level comparison to older metric.
- `router_weight_pca_step0_final.png`: whether router rows collapse or separate.

## Run Command

ACP submit script:

```bash
H0605A_ALLOW_REAL_SUBMIT=1 \
bash scripts/submit_h0605a_true_token_conditioned_inhibition_replay_4gpu_acp.sh
```

The job runs:

```bash
python scripts/run_h0605a_true_token_conditioned_inhibition_replay.py \
  --config configs/h0605a_true_token_conditioned_inhibition_replay.json \
  --run-name h0605a_true_token_conditioned_inhibition_replay_4gpu_20260604 \
  --run-stage full \
  --conditions R0-dot,R1-dot,S0-dot,S1-dot,R0-cos,R1-cos,S0-cos,S1-cos \
  --parallel \
  --max-parallel 4 \
  --trajectory
```

## Success Boundary

Token-conditioned inhibition is useful only if it improves matched R1 vs R0 or S1 vs S0 comparisons in non-collapsed seeds, without hurting target accuracy. High feature-key consistency alone is insufficient because collapse can produce the same weak signal.

## Submission Record

Submitted on 2026-06-04:

- ACP job id: `pt-hqdf7c8x`
- display name: `ats-h0605a-token-inhib-4gpu`
- state at submission check: `STARTING`
- submit log: `logs/acp/h0605a_true_token_conditioned_inhibition_replay_4gpu_20260604_submit_20260604_150130.log`
- run name: `h0605a_true_token_conditioned_inhibition_replay_4gpu_20260604`

Smoke checks:

- `R0-dot/R1-dot`, one seed, 80 steps: script completes; `R1-dot` collapses in smoke, so random-init inhibition must be filtered by collapse guard.
- `S0-cos/S1-cos`, one seed, 80 steps: original `loss_weight=0.1` collapses; final config uses `loss_weight=0.01`.
- `S1-cos` with `loss_weight=0.01` completes without immediate single-expert collapse in smoke, but max-load remains high, so final claims must be based only on non-collapsed full-run seeds.
