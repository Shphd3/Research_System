# 0522 Next Experiment Guide

## Conclusion

下一步不是继续画新的 routing heatmap，而是做一个 **router factor audit**：

> 在当前 vanilla no-load-balance top-1 MoE 中，router logit / expert assignment 主要由 identity、position、left context、rule/function、target、frequency，还是 residual-preserved common component 决定？

如果这个问题答不清，后续无论做 top-k、soft routing、hierarchical MoE、attention-score regularization，都无法判断到底修复了什么。

---

## Decision Question

> 当前 expert bucket 是否有资格作为 reverse-index candidate？

可操作化为：

> expert assignment 是否稳定对齐 retrieval-relevant factor，而不是被 token identity / high-frequency / residual component 主导？

---

## Experiment A: Existing-Run Router Factor Audit

### Purpose

用已有 H0521 / H0521b runs，不重新训练，先回答 router 到底跟哪个 factor 相关。

### Mainline Position

这是 reverse-index 路线的前置诊断。如果 expert ID 不对齐 feature/rule/slot，就不能直接当 KV index。

### Data / Artifacts

使用已有 runs：

```text
H0521 AB Feature Specialization
H0521b Seq32 Contiguous AB
```

导出每个 sample/token：

```text
sample_id
token_id
position
left_context_label
class_label: A-only / B-only / AB-composite / background
rule_label
target_id
frequency_bin
hidden_state_before_router
router_logits
expert_id
```

### Metrics

最重要指标：

```text
factor -> router_logit explained variance / R²
```

辅助指标：

```text
NMI(expert_id, token_id)
NMI(expert_id, position)
NMI(expert_id, left_context)
NMI(expert_id, rule_label)
NMI(expert_id, target_id)
NMI(expert_id, frequency_bin)
route flip rate after component removal
```

### Component Removal Test

估计加性分解：

$$
h \approx h_{id} + h_{pos} + h_{ctx} + h_{rule} + h_{target} + h_{freq} + \epsilon
$$

对每个 component 计算：

$$
\mathrm{flip\_rate}(f) = \Pr[e^*(h) \ne e^*(h - h_f)]
$$

### Expected Outcomes

- 如果 identity / frequency flip rate 最高：支持 common/high-frequency component dominates routing。
- 如果 rule flip rate 最高：支持 router 已经部分 rule-specialized。
- 如果所有 factor 都低：说明 router cell 是 mixed / seed-dependent，需要换数据或增强 expert-path necessity。

### What This Cannot Prove

不能证明 reverse index 一定有效；只能判断 expert assignment 的主导 factor。

---

## Experiment B: Factorially Disentangled Synthetic Task

### Purpose

当前 A/B/AB setup 中 identity、rule、target、frequency 仍混在一起。这个实验要把它们拆开，做真正的竞争假设检验。

### Mainline Position

如果我们要 claim “expert bucket 可以成为 feature-level index”，必须证明它跟 rule/function 对齐，而不是跟 token identity 对齐。

### Data Construction

构造多个 token identity 实现同一个 rule，同时让同一个 token identity 出现在多个 rule 中：

```text
Rule R1:
  [A1, B1] -> y_R1
  [A2, B2] -> y_R1
  [A3, B3] -> y_R1

Rule R2:
  [A1, C1] -> y_R2
  [A2, C2] -> y_R2
  [A3, C3] -> y_R2
```

加入频率控制：

```text
uniform frequency
Zipf-like nonuniform frequency
frequency-balanced sampling
```

### Most Important Metric

```text
Delta_NMI = NMI(expert_id, rule_label) - NMI(expert_id, token_identity)
```

### Expected Outcomes

- $\Delta NMI > 0$ 且跨 seed 稳定：支持 rule/function specialization。
- $\Delta NMI < 0$：支持 identity/common component routing。
- nonuniform 下低频 rule recall 降低：支持 frequency dominance。

---

## Experiment C: Attention-Relation Constrained Routing vs Baselines

### Purpose

验证“一名同学提出的 attention-score constrained routing”是否真的比 oracle/post-attention/vanilla 更接近 feature slot。

### Mainline Position

这一步测试一种可能的 specialization-inducing mechanism。

### Baselines

```text
vanilla top-1 MoE
oracle slot MoE
post-attention V similarity routing
attention-score constrained routing
attention-score constrained + hierarchical frequency grouping
```

### Required Controls

```text
uniform vs nonuniform feature frequency
small vs larger number of experts
single-head vs multi-head attention score
shallow vs deeper model
```

### Metrics

```text
slot purity
slot recall
frequency-bin balanced recall
low-frequency rule recall
expert utilization entropy
router sharpness
```

### Key Figure

```text
Method × Frequency Regime × Expert Count -> Slot Recall / Purity heatmap
```

### What This Cannot Prove

Synthetic attention relation success cannot prove real-language success; it only proves the signal can induce slot-like specialization under controlled conditions.

---

## Experiment D: Reverse-Index Utility Test

### Purpose

只有 specialization 指标变好还不够。必须验证它是否真的帮助 KV reverse index。

### Mainline Position

这是从 “specialization exists” 到 “specialization useful for retrieval” 的关口。

### Setup

对每种 candidate index：

```text
vanilla expert id
oracle slot id
attention-constrained expert id
hierarchical frequency-balanced expert id
random matched baseline
```

测试：

```text
candidate budget = 5%, 10%, 20%, 35%, 50%
expert count = 4, 8, 16, 32, 64
```

### Most Important Metric

```text
attention mass covered @ candidate budget
```

辅助指标：

```text
Recall@K dense-attention top-M
output reconstruction error
next-token accuracy drop
low-frequency rule retention
```

### Expected Outcomes

- 如果 oracle/attention-constrained index 在同预算下显著高于 random：reverse-index hypothesis strengthened。
- 如果 slot purity 高但 retrieval 不提升：specialization factor 不对齐 attention winners。
- 如果只有 oracle 有效、learned method 无效：说明 learned index 仍未解决。

---

## Experiment E: Engineering Feasibility Audit

### Purpose

导师明确要求考虑大模型高效训练和 GPU/通信架构。任何 nested/hierarchical MoE 都要记录工程成本。

### Metrics

```text
number of dispatches per token
all-to-all communication count
activation memory
router compute overhead
training throughput
inference throughput
```

### Pass Criteria

一个方法进入主线候选，至少要满足：

```text
specialization metric improves
reverse-index metric improves
engineering cost has plausible scaling path
```

---

## Minimum Agent Task Spec

### Task 1: Factor Audit From Existing Runs

```text
Input:
  H0521/H0521b result dirs
Output:
  factor_table.csv
  factor_nmi_summary.csv
  router_logit_r2_summary.csv
  component_flip_rate.csv
  figures/factor_nmi_bar.png
  figures/router_logit_r2_bar.png
  figures/component_flip_rate_bar.png
```

### Task 2: Disentangled Synthetic Generator

```text
Implement:
  rule_identity_disentangled_generator.py
Required controls:
  num_rules
  identities_per_rule
  shared_identity_across_rules
  frequency_regime: uniform | zipf | balanced
```

### Task 3: Baseline Sweep

```text
Run:
  vanilla MoE
  dense baseline
  oracle slot routing
Seeds:
  at least 4
Experts:
  4, 8, 16
```

---

## Next Action

Do not launch all experiments at once. The immediate next action is:

```text
Run Experiment A on existing artifacts and produce one factor-attribution summary.
```

If Experiment A says router is dominated by identity/frequency, then build Experiment B.  
If Experiment A says rule already explains routing, then skip to Experiment D and test reverse-index utility.
