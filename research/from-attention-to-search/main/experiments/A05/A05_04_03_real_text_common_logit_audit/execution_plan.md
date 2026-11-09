# Execution Plan: A05_04_03_real_text_common_logit_audit

Primary anchor:
`Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_04_03_real_text_common_logit_initialization_anchor.md`

Anchor decision question:
On DCLM packed-token text, does random-initialized sparse top-1 linear routing concentrate because \(w_e^T c\) dominates \(w_e^T r_i\) in the actual router-gate input?

Experiment role:
This experiment transfers the Round-2 toy common-logit mechanism to random-initialized real-text Qwen-style MoE geometry and early training.

Stage mapping:
- Phase 0 source/data capture -> reproducibility and exact object contract.
- Phase 1 step-0 audit -> H1/H2.
- Phase 2 virtual expert-count scaling -> H3.
- Phase 3 early-training trajectory -> early persistence or amplification.
- Phase 4 actual expert-count sweep -> actual \(E\) underuse risk.

## 1. Run Goal

Run a 4-GPU ACP job that audits DCLM real-text random-init top-1 linear MoE routing with no shared expert, no oracle gating, and no load-balance loss.

## 2. Data / Material / Case Construction

Data source:
`/data/share/109_cache_dir/hf_data/dclm_bin`

Manifest rule:
Each sample is a 257-token packed span. The first 256 tokens are model inputs, and the next shifted 256 tokens are LM targets. All 256 input positions are valid routed tokens.

Audit split:
Samples `0..8191`.

Training split:
Samples `8192..40959`.

Position rule:
Primary routing metrics aggregate all positions `0..255`. Required diagnostics report buckets `0..63`, `64..127`, `128..191`, and `192..255`.

## 3. System / Procedure / Evaluation Setup

Model:
Small random-initialized Qwen-style decoder-only MoE.

Main config:
`hidden_size=512`, `num_hidden_layers=6`, `num_attention_heads=8`, `num_key_value_heads=4`, `head_dim=64`, `moe_intermediate_size=2048`, `num_experts=8` for the main audit.

Router contract:
`moe_type=moe`, `router_type=linear`, `gating_reference=hidden_states`, `top_k=1`, `router_bias=false`, `use_shared_expert=false`, `router_center_input=false`, `router_aux_gate=false`, `router_acp_transform=false`, `lambda_lb=0.0`, `norm_topk_prob=false`.

The metric object `h_i` is the exact tensor passed into the active linear gate. The runner verifies `router_logits == h @ W.T`.

Initialization:
Use Qwen-style `nn.Linear` initialization from the local model source: `Normal(0, initializer_range)` with `initializer_range=0.02`.

## 4. Configs And Commands

Code workspace:
`/data/250010109/MoE_Router`

Research record:
`/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A05/A05_04_03_real_text_common_logit_audit`

Submit script:
`scripts/submit_real_text_common_logit_4gpu_acp.sh`

Full run command inside ACP:

```bash
torchrun --standalone --nproc_per_node=4 scripts/run_real_text_common_logit_audit.py --run-stage full
```

## 5. Metrics And Artifacts

Primary metrics:
`common_margin`, `residual_margin`, `dominance_ratio`, `common_winner_agreement`, `max_load`, `routing_entropy`, `active_experts`, `active_experts_ratio`, `gini_load`.

Central result files:

```text
results/phase1_step0_metrics.csv
results/phase1_position_bucket_metrics.csv
results/phase1_layer_summary.csv
results/phase2_virtual_scaling_metrics.csv
results/phase2_virtual_scaling_summary.csv
results/phase3_trajectory_metrics.csv
results/phase4_actual_E_sweep_metrics.csv
```

Central figures:

```text
figures/phase1_common_vs_residual_margin.png
figures/phase1_raw_vs_centered_load.png
figures/phase2_E_vs_common_margin.png
figures/phase2_E_vs_active_experts_ratio.png
figures/phase3_max_load_over_steps.png
figures/phase4_E_train_vs_active_experts_ratio.png
```

## 6. Stage Audit

| Stage | Local Question | Input Evidence | Pass / Fail Rule | Debug Artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| Source capture | Are data/code/config fixed? | manifests and checksums | all required paths and checksums recorded | `config/source_manifest.json` | detailed |
| Gate contract | Is `h_i` exactly the gate input? | reconstruction error | max error <= 1e-5 fp32 | `results/gate_contract_checks.csv` | detailed |
| Phase 1 | Does step-0 common dominance exist? | layer/seed metrics | protocol support/weaken rules | phase1 csv/figures | summary |
| Phase 2 | Does virtual E amplify the effect? | E curves | raw worsens more than centered | phase2 csv/figures | summary |
| Phase 3 | Does bias persist in early training? | checkpoint metrics | trajectory before/with LM loss | phase3 csv/figures | summary |
| Phase 4 | Does actual E worsen underuse? | E sweep metrics | active ratio and max-load trends | phase4 csv/figures | summary |

## 7. Pass / Fail Criteria

Supported:
Phase 1 shows common dominance and centering reduces concentration; Phase 2 shows virtual E scaling amplifies raw common-winner dominance.

Stronger support:
Phase 3 shows persistence or amplification and Phase 4 shows actual E worsens early underuse.

Weakened:
Residual margins dominate, centering has little effect, and neither virtual nor actual E scaling worsens concentration.

Insufficient evidence:
The gate input is not captured exactly, shared expert remains enabled, oracle gating is used, or exact data manifests are missing.

## 8. Failure Modes To Check

- shared expert accidentally enabled;
- oracle gating accidentally enabled;
- top-k not equal to 1;
- load-balance loss nonzero;
- position-only concentration mistaken for global common bias;
- virtual router scale incomparable to real gate scale;
- Phase 3 checkpoints not audited at exact steps.

## 9. Result Location

Run root:
`Projects/from-attention-to-search/main/experiments/A05/A05_04_03_real_text_common_logit_audit/runs/real_text_common_logit_audit_v5/<run_name>/`

Curated documents after run:

```text
summary.md
detailed.md
daily_research_reports/0611/real_text_common_logit_audit/05_report_card.md
```
