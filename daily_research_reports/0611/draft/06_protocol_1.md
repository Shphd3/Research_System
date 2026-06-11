# Protocol v5: Real-Text Random-Init MoE Common-Logit Dominance Audit

## 0. Goal

Test whether, on real language-modeling data, a randomly initialized sparse top-1 dot-product MoE router produces early route concentration because the hidden-state common component creates expert-specific common-logit offsets.

Mentor-facing question:

```text
Why can a linear MoE router be dominated by common information at initialization instead of using token-level differences?
```

Core decomposition:

```text
h_i = c + r_i
z_i,e = w_e^T h_i = w_e^T c + w_e^T r_i
```

Primary object:

```text
common_margin = top1_e(w_e^T c) - top2_e(w_e^T c)
```

The key test is not whether `||c||` is large, but whether `w_e^T c` creates an expert-specific logit gap large enough to dominate routing.

---

## 1. Decision Questions

### Main decision question

```text
On DCLM real-text data, does a random-initialized sparse top-1 dot-product MoE produce initialization-time route concentration because w_e^T c dominates w_e^T r_i?
```

### Scaling decision question

```text
Does increasing virtual or actual expert count amplify common-winner dominance and expert underuse?
```

### Early-training decision question

```text
Does early training preserve or amplify the initialization-time common-logit routing bias?
```

---

## 2. Claim Boundary

### Can claim if supported

```text
In a real-text random-initialized MoE setting, common-logit bias is a mechanism-level explanation for initialization-time route concentration.
```

### Cannot claim from this protocol alone

```text
- feature-to-expert specialization is achieved;
- common-control is already a deployable method;
- final training collapse is fully solved;
- load balance equals specialization;
- pretrained large MoE models necessarily behave the same way.
```

---

## 3. Execution Plan Overview

Run tonight in four phases.

```text
Phase 0: Source capture + fixed data manifest.
Phase 1: Step-0 common-logit audit.
Phase 2: Virtual larger-MoE expert-count scaling.
Phase 3: Early-training trajectory audit.
Phase 4: Actual expert-count training sweep.
```

Minimum must-finish by tomorrow:

```text
Phase 0 + Phase 1 + Phase 2
```

Strong report if finished:

```text
Phase 0 + Phase 1 + Phase 2 + Phase 3
```

Full report if finished:

```text
Phase 0 + Phase 1 + Phase 2 + Phase 3 + Phase 4
```

Do not run pretrained frozen representation audit in this protocol.

---

## 4. Source Capture

Create source snapshot directory:

```text
source_list/real_text_common_logit_audit_v5/
```

Record dataset path:

```text
data_source_path = /data/share/109_cache_dir/hf_data/dclm_bin
```

Record model/code paths:

```text
model_architecture_source_path = /data/250010109/MoE_Router/src/model/qwen3_moe
execution_script_source_path = /data/250010109/MoE_Router/train_qwen3_moe.py
```

Create these files before running:

```text
source_list/real_text_common_logit_audit_v5/source_manifest.json
source_list/real_text_common_logit_audit_v5/run_config.yaml
source_list/real_text_common_logit_audit_v5/audit_manifest.jsonl
source_list/real_text_common_logit_audit_v5/train_manifest.jsonl
source_list/real_text_common_logit_audit_v5/reproduce.md
```

`source_manifest.json` must include:

```text
- timestamp
- git commit hash, if available
- copied script checksum
- model source directory checksum or file list
- dataset server path
- tokenizer path
- machine name
- python / conda environment
- CUDA version
```

Do not copy the full raw/bin dataset into the repo.

---

## 5. Dataset Boundary

### Dataset

```text
D0 = DCLM-bin
path = /data/share/109_cache_dir/hf_data/dclm_bin
```

No feature labels are required.

### Audit data

Fixed first audit slice:

```text
sequence_length = 256
audit_num_sequences = 8192
audit_max_tokens = 2,097,152
```

Selection rule:

```text
1. Sort available DCLM bin shards lexicographically.
2. Read sequences deterministically from the beginning of the sorted shard list.
3. Keep the first 8192 valid sequences of length 256.
4. Save all selected sample references into audit_manifest.jsonl.
```

Each row in `audit_manifest.jsonl` should include:

```json
{
  "dataset": "DCLM-bin",
  "source_path": "/data/share/109_cache_dir/hf_data/dclm_bin",
  "shard_path": "...",
  "sample_index": 0,
  "start_token_offset": 0,
  "sequence_length": 256
}
```

If exact token offsets are unavailable, record loader-level indices:

```json
{
  "dataset": "DCLM-bin",
  "shard_path": "...",
  "loader_sample_index": 0,
  "sequence_length": 256
}
```

### Training data

Fixed training slice:

```text
sequence_length = 256
train_num_sequences = 32768
train_max_tokens = 8,388,608
```

Selection rule:

```text
Use the next 32768 valid sequences after the audit slice.
Do not overlap train_manifest with audit_manifest.
```

Save:

```text
source_list/real_text_common_logit_audit_v5/train_manifest.jsonl
```

### Token analysis rule

Use all non-padding tokens if feasible.

If memory is too high, use deterministic token subsampling:

```text
max_analyzed_tokens_per_layer = 262144
token_subsample_seed = 20260611
```

Record the subsampling rule in `run_config.yaml`.

---

## 6. Model Boundary

Use Qwen3-MoE-style implementation only as model code source.

Do not load Qwen3-A3B pretrained weights.

### Required router form

```text
router_score_e(h) = w_e^T h
route(h) = argmax_e router_score_e(h)
```

### Main model config

```text
model_type = decoder-only Transformer
initialization = random
d_model = 512
num_layers = 6
num_heads = 8
num_experts = 8
expert_hidden_dim = 2048
top_k = 1
router_bias = false
load_balance_loss_coef = 0.0
shared_experts = disabled
dropout = 0.0
dtype_forward = bf16 or fp16
dtype_metrics = fp32
```

If this config cannot run, fallback:

```text
d_model = 256
num_layers = 4
num_heads = 4
num_experts = 8
expert_hidden_dim = 1024
```

The actual config must be saved to:

```text
source_list/real_text_common_logit_audit_v5/run_config.yaml
```

### Verification before run

The script must explicitly log:

```text
top_k = 1
router_bias = false
load_balance_loss_coef = 0.0
initialization = random
pretrained_weights_loaded = false
```

If any of these are false, the main audit is invalid.

---

## 7. Seeds

Use fixed seeds.

```text
model_seeds = [0, 1, 2]
virtual_router_seeds = [0, 1, 2, ..., 63]
data_seed = 20260611
token_subsample_seed = 20260611
```

For Phase 4 actual expert-count sweep:

```text
E_train = [4, 8, 16, 32]
model_seeds = [0, 1, 2]
```

If runtime is too high, keep all E values but reduce to:

```text
model_seeds = [0]
```

and mark Phase 4 as preliminary.

---

## 8. Routed Hidden States

For each model seed and each MoE layer, collect router-input hidden states:

```text
H_l = {h_i}
```

where `h_i` is the hidden state of one non-padding token immediately before the router at layer `l`.

Route positions:

```text
primary = all non-padding token positions
diagnostic = position buckets
```

Position buckets:

```text
bucket_0 = positions 0-63
bucket_1 = positions 64-127
bucket_2 = positions 128-191
bucket_3 = positions 192-255
```

Do not use only one fixed token position.

### Hidden-state saving rule

Default:

```text
Do not save full hidden states unless necessary.
Stream metrics when possible.
```

Allowed saved artifact:

```text
sampled_hidden_states_per_layer <= 262144 tokens
dtype = fp16
```

Metric accumulation:

```text
accumulate means, logits, counts, and covariance summaries in fp32
```

---

## 9. Common / Residual Decomposition

For each model seed, layer, and checkpoint:

```text
c = mean_i h_i
r_i = h_i - c
```

Router logit decomposition:

```text
z_i,e = w_e^T h_i
      = w_e^T c + w_e^T r_i
```

Define:

```text
common_logit_e = w_e^T c
residual_logit_i,e = w_e^T r_i
```

Primary metrics:

```text
common_margin = top1_e(common_logit_e) - top2_e(common_logit_e)

residual_margin = mean_i [top1_e(residual_logit_i,e) - top2_e(residual_logit_i,e)]

dominance_ratio = common_margin / max(residual_margin, 1e-8)

common_winner = argmax_e common_logit_e

common_winner_agreement = mean_i [argmax_e z_i,e == common_winner]
```

Routing distribution metrics:

```text
max_load
routing_entropy
active_experts
active_experts_ratio = active_experts / E
gini_load
```

Common-removal counterfactual:

```text
raw_h = h_i
centered_h = h_i - c
```

Compare:

```text
delta_max_load = max_load(raw_h) - max_load(centered_h)
delta_entropy = entropy(centered_h) - entropy(raw_h)
delta_active_experts = active_experts(centered_h) - active_experts(raw_h)
```

---

## 10. Phase 1: Step-0 Common-Logit Audit

### Purpose

Check whether common-logit bias already exists at random initialization on real text.

### Hypothesis

```text
At step 0, w_e^T c creates an expert-specific common offset that dominates w_e^T r_i and predicts the dominant route.
```

### Procedure

For each `model_seed`:

```text
1. Randomly initialize the small MoE.
2. Load audit_manifest.jsonl.
3. Run forward pass without training.
4. For each MoE layer, extract router-input hidden states h_i.
5. Compute c = mean_i h_i.
6. Compute raw router logits w_e^T h_i.
7. Compute common logits w_e^T c.
8. Compute residual logits w_e^T(h_i - c).
9. Measure common_margin, residual_margin, dominance_ratio, common_winner_agreement, max_load, entropy, active_experts.
10. Recompute routing after common removal h_i - c.
```

### Required outputs

```text
results/phase1_step0_metrics.csv
results/phase1_position_bucket_metrics.csv
results/phase1_layer_summary.csv
figures/phase1_load_hist_by_layer.png
figures/phase1_common_vs_residual_margin.png
figures/phase1_raw_vs_centered_load.png
```

### Conclusion rule

Phase 1 supports the hypothesis if at least 2/3 model seeds and at least half of MoE layers satisfy:

```text
dominance_ratio > 1.0
common_winner_agreement > 1 / E + 0.10
max_load(raw_h) > max_load(centered_h) + 0.05
active_experts(centered_h) > active_experts(raw_h)
```

Strong support:

```text
dominance_ratio > 1.5
common_winner_agreement > 0.35 for E = 8
delta_max_load > 0.10
```

Weakened:

```text
dominance_ratio <= 1.0 in most layers/seeds
common_winner_agreement close to 1 / E
raw_h and centered_h have similar max_load
```

---

## 11. Phase 2: Virtual Larger-MoE Expert-Count Scaling

### Purpose

Check whether increasing expert count mathematically amplifies common-winner dominance on the same hidden states.

### Hypothesis

```text
As E increases, max_e w_e^T c becomes more extreme, so common_margin and expert underuse increase.
```

### Procedure

Use hidden states from Phase 1.

For each virtual expert count:

```text
E_virtual = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
```

For each `virtual_router_seed`:

```text
1. Sample W_E ∈ R^{E_virtual × d}
2. Use w_e ~ N(0, 1/d)
3. Compute route_i = argmax_e w_e^T h_i
4. Compute metrics on raw_h
5. Compute metrics on centered_h = h_i - c
```

Use:

```text
virtual_router_seeds = 64
```

### Required outputs

```text
results/phase2_virtual_scaling_metrics.csv
results/phase2_virtual_scaling_summary.csv
figures/phase2_E_vs_common_margin.png
figures/phase2_E_vs_dominance_ratio.png
figures/phase2_E_vs_active_experts_ratio.png
figures/phase2_raw_vs_centered_scaling.png
```

### Conclusion rule

Phase 2 supports expert-count scaling risk if:

```text
common_margin increases with E_virtual
dominance_ratio increases with E_virtual
active_experts_ratio(raw_h) decreases with E_virtual
centered_h weakens the scaling effect
```

Strong support:

```text
raw-vs-centered gap grows with E_virtual
```

Weakened:

```text
raw_h and centered_h have similar scaling curves
common_margin does not increase with E_virtual
active_experts_ratio does not decrease with E_virtual
```

Important boundary:

```text
Phase 2 is a geometry probe. It does not prove actual training behavior.
```

---

## 12. Phase 3: Early-Training Trajectory Audit

### Purpose

Check whether common-logit dominance persists or amplifies during early training.

### Hypothesis

```text
If common-logit bias is an early basin-entry mechanism, it should appear before meaningful LM loss improvement and persist or amplify in early steps.
```

### Training setup

Use `train_manifest.jsonl`.

```text
max_train_steps = 300
checkpoints = [0, 1, 10, 50, 100, 300]
optimizer = AdamW
learning_rate = 3e-4
weight_decay = 0.0
batch_size = record actual value
gradient_accumulation_steps = record actual value
```

Evaluate every checkpoint on the same fixed `audit_manifest.jsonl`.

### Metrics

```text
LM_loss
common_margin
residual_margin
dominance_ratio
common_winner_agreement
max_load
active_experts
entropy
```

### Required outputs

```text
results/phase3_trajectory_metrics.csv
figures/phase3_common_margin_over_steps.png
figures/phase3_dominance_ratio_over_steps.png
figures/phase3_max_load_over_steps.png
figures/phase3_lm_loss_over_steps.png
```

### Conclusion rule

Phase 3 supports early-training amplification if:

```text
common_margin is already large at step 0
common_winner predicts early dominant routing
route concentration appears before meaningful LM loss improvement
early training preserves or amplifies the same dominant route
```

Weakened:

```text
route concentration appears only after substantial training
residual_margin dominates early routing
dominant expert changes randomly across early checkpoints
```

---

## 13. Phase 4: Actual Expert-Count Training Sweep

### Purpose

Check whether increasing actual expert count worsens early route concentration during training.

### Hypothesis

```text
Larger actual expert count increases the probability of extreme common projection winners, leading to stronger early expert underuse.
```

### Models

Train random-initialized models with:

```text
E_train = [4, 8, 16, 32]
model_seeds = [0, 1, 2]
```

Keep fixed:

```text
dataset = DCLM-bin
sequence_length = 256
d_model = 512
num_layers = 6
num_heads = 8
expert_hidden_dim = 2048
training steps = 300
optimizer = AdamW
top_k = 1
router_bias = false
load_balance_loss_coef = 0.0
```

If runtime is too high:

```text
Run E_train = [4, 8, 16, 32] with model_seeds = [0] first.
Mark result as preliminary.
```

### Checkpoints

```text
[0, 1, 10, 50, 100, 300]
```

### Metrics

```text
step0_common_margin
step0_dominance_ratio
step0_max_load
early_max_load
final_max_load_at_step300
active_experts_ratio
LM_loss
```

### Required outputs

```text
results/phase4_actual_E_sweep_metrics.csv
results/phase4_actual_E_sweep_summary.csv
figures/phase4_E_train_vs_step0_common_margin.png
figures/phase4_E_train_vs_dominance_ratio.png
figures/phase4_E_train_vs_active_experts_ratio.png
figures/phase4_E_train_vs_early_max_load.png
```

### Conclusion rule

Phase 4 supports actual scaling risk if:

```text
larger E_train has stronger common_margin
larger E_train has lower active_experts_ratio
early route concentration worsens with E_train
centered routing or logit cancellation reduces the effect
```

Weakened:

```text
actual expert-count scaling does not worsen early concentration
common-control does not affect routing
collapse appears only late and is better explained by expert utility co-adaptation
```

---

## 14. Baselines

### Baseline 1: Centered hidden states

```text
route on h_i - c
```

Purpose:

```text
Tests whether route concentration is caused by common component.
```

### Baseline 2: Isotropic Gaussian hidden states

Generate:

```text
g_i ~ N(0, sigma^2 I)
```

where `sigma` matches average hidden norm scale.

Purpose:

```text
Tests whether observed concentration is just finite random top-1 assignment.
```

### Baseline 3: Covariance-matched zero-mean Gaussian

Generate Gaussian samples with the same covariance spectrum as hidden states but zero mean.

Purpose:

```text
Separates mean/common effect from anisotropic covariance effect.
```

Baseline 2 is required.
Baseline 3 is optional for tonight; if skipped, record it as not run.

---

## 15. Result Directory Structure

Use one root directory per run:

```text
runs/real_text_common_logit_audit_v5/<timestamp>_<run_name>/
```

Required structure:

```text
config/
  run_config.yaml
  source_manifest.json
  audit_manifest.jsonl
  train_manifest.jsonl

logs/
  execution.log
  environment.txt
  git_status.txt
  job_id.txt optional

results/
  phase1_step0_metrics.csv
  phase1_layer_summary.csv
  phase2_virtual_scaling_metrics.csv
  phase2_virtual_scaling_summary.csv
  phase3_trajectory_metrics.csv
  phase4_actual_E_sweep_metrics.csv

figures/
  phase1_load_hist_by_layer.png
  phase1_common_vs_residual_margin.png
  phase1_raw_vs_centered_load.png
  phase2_E_vs_common_margin.png
  phase2_E_vs_dominance_ratio.png
  phase2_E_vs_active_experts_ratio.png
  phase2_raw_vs_centered_scaling.png
  phase3_common_margin_over_steps.png
  phase3_max_load_over_steps.png
  phase4_E_train_vs_step0_common_margin.png
  phase4_E_train_vs_active_experts_ratio.png

notes/
  reproduce.md
  interpretation.md
  report_card.md
```

---

## 16. Reproducibility Checklist

Before marking a run complete:

```text
[ ] exact dataset path recorded
[ ] audit sequence manifest saved
[ ] train sequence manifest saved
[ ] tokenizer path recorded
[ ] model source path recorded
[ ] script checksum recorded
[ ] run_config.yaml saved
[ ] model seeds recorded
[ ] virtual router seeds recorded
[ ] checkpoint list recorded
[ ] metric CSV files saved
[ ] figures saved
[ ] no pretrained weights loaded
[ ] load_balance_loss disabled
[ ] top_k = 1 verified
[ ] router_bias = false verified
[ ] shared experts disabled or explicitly recorded
```

---

## 17. Final Decision Logic

### Main anchor supported

The anchor is supported if:

```text
1. Phase 1 shows common_margin > residual_margin at step 0;
2. common_winner predicts dominant routing;
3. common removal reduces route concentration;
4. Phase 2 shows virtual expert-count scaling amplifies common dominance.
```

### Stronger support

The result becomes stronger if:

```text
5. Phase 3 shows the same bias persists or amplifies during early training;
6. Phase 4 shows actual larger E_train worsens early expert underuse.
```

### Weakened

The anchor is weakened if:

```text
1. residual_margin dominates common_margin;
2. common_winner does not predict route load;
3. common removal does not change routing;
4. expert-count scaling does not worsen concentration;
5. concentration emerges only late through training co-adaptation.
```

### Insufficient evidence

Evidence is insufficient if:

```text
1. only common norm is reported without w_e^T c;
2. only max_load is reported without common_margin;
3. only one seed or one layer is tested;
4. virtual router scaling is presented as actual MoE training evidence;
5. hidden states are taken from pretrained weights in the main audit;
6. exact data slice is not reproducible.
```

---

## 18. Report Card Template

Create:

```text
runs/real_text_common_logit_audit_v5/<run>/notes/report_card.md
```

Use this structure.

### 18.1 Purpose

```text
We test whether random-initialized sparse top-1 dot-product MoE routing on real DCLM text is dominated by hidden-state common-logit bias at initialization.
```

Chinese meeting version:

```text
目的：验证真实语言建模数据上，随机初始化的 sparse top-1 dot-product MoE 是否在 step 0 就因为 hidden-state common component 产生 expert-specific common-logit offset，从而导致路由集中。
```

### 18.2 Hypothesis

```text
If h_i = c + r_i, then the router logit decomposes as w_e^T h_i = w_e^T c + w_e^T r_i. If w_e^T c has a large top expert gap, it can dominate top-1 routing before the model learns useful token-level differences.
```

Chinese meeting version:

```text
假设：hidden state 可以分解为 common 部分 c 和 residual 部分 r_i。线性 router 的 logit 会分解为 w_e^T c + w_e^T r_i。如果 w_e^T c 在 expert 之间形成较大的 gap，那么它会在训练开始前主导 top-1 routing。
```

### 18.3 Conclusion

Choose exactly one:

```text
Supported.
Weakened.
Insufficient evidence.
Mixed: supported for initialization geometry, not yet supported for actual training scaling.
```

Chinese meeting version examples:

```text
结论 A（支持）：
实验支持 common-logit dominance。DCLM 真实文本上，随机初始化模型的 step-0 routing 已经被 w_e^T c 主导；common removal 明显降低 route concentration；virtual expert scaling 进一步放大该效应。

结论 B（部分支持）：
实验支持 step-0 common-logit geometry，但实际训练中的 expert-count scaling 证据还不足。

结论 C（削弱）：
实验没有支持 common-logit dominance。residual logit margin 不弱于 common margin，且 common removal 没有明显改变 routing distribution。
```

### 18.4 Evidence

Use this table.

```text
Evidence 1: Phase 1 step-0 audit
- common_margin:
- residual_margin:
- dominance_ratio:
- common_winner_agreement:
- max_load raw:
- max_load centered:
- active_experts raw:
- active_experts centered:
- interpretation:

Evidence 2: Phase 2 virtual expert scaling
- E range:
- common_margin trend:
- dominance_ratio trend:
- active_experts_ratio trend:
- raw vs centered gap:
- interpretation:

Evidence 3: Phase 3 early training trajectory
- checkpoint range:
- LM loss trend:
- common_margin trend:
- max_load trend:
- dominant expert persistence:
- interpretation:

Evidence 4: Phase 4 actual expert-count sweep
- E_train range:
- step0_common_margin trend:
- active_experts_ratio trend:
- early max_load trend:
- interpretation:
```

### 18.5 Claim Boundary

```text
Can claim:
- common-logit bias explains initialization-time route concentration in this random-init real-text setting;
- virtual expert-count scaling increases common-winner dominance if Phase 2 supports;
- actual expert-count scaling increases early underuse only if Phase 4 supports.

Cannot claim:
- feature-to-expert specialization;
- final collapse is fully solved;
- deployable initialization method;
- pretrained large MoE behavior.
```

### 18.6 Next Decision

Choose one:

```text
If Phase 1 + Phase 2 supported:
Next: design label-free common-aware initialization / router-input common-control.

If Phase 1 supported but Phase 2 weakened:
Next: focus on early lock-in dynamics, not expert-count scaling.

If Phase 1 weakened:
Next: return to representation-source audit or alternative collapse mechanism.

If Phase 4 supported:
Next: test common-aware initialization under actual E_train scaling.
```

---

## 19. Meeting Narrative: Purpose → Hypothesis → Conclusion → Evidence

Use this order in the meeting.

### Purpose

```text
这轮实验不是为了证明 feature specialization，而是为了回答导师的问题：为什么线性 router 会被 common 信息影响，而不是利用 token-level difference。
```

### Hypothesis

```text
我的假设是：真实文本输入下，随机初始化模型的 router-input hidden state 存在 common component c。线性 router 的 logit 可以分解成 w_e^T c 和 w_e^T r_i。如果 w_e^T c 在 expert 之间产生较大 gap，它就会成为 feature-independent 的 expert bias，导致很多 token 在 step 0 被分到同一个 expert。
```

### Conclusion

Fill after result.

```text
当前结论是：supported / weakened / insufficient evidence。
```

If supported:

```text
结果支持 common-logit dominance：step 0 时 common_margin 大于 residual_margin，common winner 能预测 dominant expert；去掉 common 后，max_load 下降、active experts 上升。virtual expert scaling 进一步显示，专家数越大，common winner dominance 越强。
```

### Evidence

Report in this order:

```text
1. Step-0 decomposition:
   common_margin vs residual_margin.

2. Route prediction:
   common_winner_agreement and max_load.

3. Counterfactual:
   raw_h vs centered_h.

4. Scaling:
   E_virtual scaling curve.

5. Training trajectory:
   step 0 / 1 / 10 / 50 / 100 / 300.

6. Actual E_train sweep:
   E = 4 / 8 / 16 / 32.
```

### Boundary

```text
这个实验只能说明初始化分发偏置和 common-logit dominance，不能直接说明 feature specialization，也不能说明最终 collapse 已完全解决。下一步才是 common-aware initialization 或 router-input common-control。
```

---

## 20. One-Sentence Summary For Mentor

```text
We tested a randomly initialized sparse top-1 dot-product MoE on real DCLM text and found whether the step-0 routing distribution is explained by the common-logit term w_e^T c rather than residual token differences w_e^T r_i; then we checked whether the effect scales with expert count.
```

Chinese version:

```text
我们用 DCLM 真实文本和随机初始化 sparse top-1 dot-product MoE，测试 step-0 routing 是否主要由 common-logit 项 w_e^T c 解释，而不是由 token residual difference w_e^T r_i 解释，并进一步测试这个效应是否随 expert 数量增加而放大。
```
