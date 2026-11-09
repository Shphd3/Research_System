# Detailed Report: H0522 Router Factor Audit Seq32

## 1. Purpose

本实验回答一个窄问题：

```text
seq_len=32 synthetic setup 中，ordinary top-1 MoE 的 expert id 到底更受
token identity、source position、left context、rule/function 还是 target shortcut 影响？
```

## 2. Run

ACP job:

```text
pt-xceqs84c
```

Run:

```text
h0522_router_factor_audit_seq32_4gpu_20260522
```

Seeds:

```text
20260521, 20260522, 20260523, 20260524
```

Code workspace:

```text
Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/
```

Runner:

```text
active/synthetic_data_understanding/scripts/run_h0522_router_factor_audit_seq32.py
```

Tracked archive copy:

```text
scripts/run_h0522_router_factor_audit_seq32.py
```

Config:

```text
active/synthetic_data_understanding/configs/h0522_router_factor_audit_seq32.json
```

Tracked archive copy:

```text
config/h0522_router_factor_audit_seq32.json
```

Result directory:

```text
active/synthetic_data_understanding/results/h0522_router_factor_audit_seq32/h0522_router_factor_audit_seq32_4gpu_20260522/
```

Figure directory:

```text
active/synthetic_data_understanding/figures/h0522_router_factor_audit_seq32/h0522_router_factor_audit_seq32_4gpu_20260522/
```

## 3. Stage Design

Stage 1 复用 H0521b checkpoint，导出 routed source-token records，并计算 factor 与 expert id 的对应关系。

Stage 2 用 group-mean component 近似不同 factor 对 hidden state 的贡献，测移除该 component 后 expert 是否翻转。

Stage 3 在旧 H0521b 模型上强制 token 走指定 expert，测 cross-entropy change。

Stage 4 训练 residual-reduced stress MoE，让 expert path 更难被 residual/shared path 绕过，再测 force/ablate 的影响。

Stage 5 构造 factor-disentangled seq_len=32 synthetic task，检查 rule/function 是否比 identity 更能解释 expert id。

## 4. Main Metrics

### Stage 1

平均结果：

| Factor | NMI mean | Router-logit \(R^2\) mean | Majority expert accuracy mean |
|---|---:|---:|---:|
| source_position | 0.1205 | 0.3540 | 0.5415 |
| token_id | 0.0861 | 0.3263 | 0.5180 |
| token_identity | 0.0470 | 0.0795 | 0.3932 |
| source_role | 0.0419 | 0.0889 | 0.4022 |
| rule_label | 0.0138 | 0.0269 | 0.3685 |
| target_id | 0.0160 | 0.0323 | 0.3739 |

结论：旧 H0521b router 更受 source_position / token_id 影响，而不是 rule/class。

### Stage 2

平均结果：

| Component | Flip rate mean | Component-logit \(R^2\) mean |
|---|---:|---:|
| source_position | 0.3362 | 0.3540 |
| token_id | 0.3023 | 0.3263 |
| token_identity | 0.1178 | 0.0795 |
| source_role | 0.1288 | 0.0889 |
| rule_label | 0.0834 | 0.0269 |
| target_id | 0.0897 | 0.0323 |

结论：移除 source_position / token_id component 最容易改变 expert choice。

### Stage 3/4

force-route 和 ablate 会在某些 seed/class 上造成明显 \(\Delta CE\)，说明 expert path 有时确实影响输出。但最大敏感 expert 不跨 seed 稳定，且 class-to-expert 对齐不干净。

解释：这支持“expert path 有功能影响”，但不支持“某个 expert 是稳定 A/B/AB 或 rule/function expert”。

### Stage 5

平均结果：

| Factor | NMI mean | Majority expert accuracy mean |
|---|---:|---:|
| target_id | 0.5070 | 0.8416 |
| second_identity | 0.3047 | 0.8416 |
| first_identity | 0.0272 | 0.5673 |
| rule_label | 0.0175 | 0.5723 |
| motif_position | 0.0115 | 0.5845 |

`NMI(rule, expert_id) - NMI(first_identity, expert_id)` 的四 seed 平均值为 -0.0098。

结论：在当前解耦任务中，rule/function 没有稳定胜过 identity；target/second-token shortcut 最强。

## 5. Figures

![Stage 1 factor NMI](figures/stage1_factor_nmi_by_seed.png)

![Stage 1 factor logit R2](figures/stage1_factor_logit_r2_by_seed.png)

![Stage 2 component flip rate](figures/stage2_component_flip_rate_by_seed.png)

![Stage 3 force route delta CE](figures/stage3_force_route_delta_ce.png)

![Stage 4 stress force route delta CE](figures/stage4_stress_force_route_delta_ce.png)

![Stage 5 disentangled NMI](figures/stage5_disentangled_nmi_by_seed.png)

## 6. Artifacts

Copied tables:

```text
tables/stage1_factor_metrics.csv
tables/stage2_component_metrics.csv
tables/stage3_force_route_delta_ce.csv
tables/stage4_stress_force_route_delta_ce.csv
tables/stage5_disentangled_metrics.csv
```

Raw source-token records are intentionally kept in the run directory, not in the mainline:

```text
active/synthetic_data_understanding/results/h0522_router_factor_audit_seq32/h0522_router_factor_audit_seq32_4gpu_20260522/stage1_factor_records.csv
active/synthetic_data_understanding/results/h0522_router_factor_audit_seq32/h0522_router_factor_audit_seq32_4gpu_20260522/stage5_disentangled_records.csv
```

## 7. Claim Boundary

可以说：

```text
在当前 seq_len=32 synthetic 设置里，ordinary top-1 MoE 的 expert id 不能
作为 clean rule/function index；position/token-id/target shortcut 解释力更强。
```

不能说：

```text
MoE routing 一般无效；
router supervision / load balance / top-k 一定无效；
真实语言模型中也一定是同样机制；
Reverse Index 思路已经失败。
```
