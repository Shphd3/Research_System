# 0522 Router Factor Audit And Next Experiment Plan

## Conclusion

当前结果不是“没有更新”。它更新的是一个更克制但重要的判断：

> ordinary no-load-balance top-1 MoE 没有自然形成稳定、干净的 feature/rule-level expert bucket；现有证据更支持 mixed router assignment 或 coarse router cell，而不是可直接作为 KV reverse index 的 functional bucket。

但当前结果还不能证明：

> expert function 已经强混合，或 MoE 一定按 token identity 分发，或所有 routing 机制都不能形成 feature-level index。

下一步不要急着换 architecture。先做 router factor audit：明确 router score/expert id 到底由 hidden representation 的哪一部分决定。

---

## Self-Contained Context

主线问题：我们想把 long-context attention 重新理解为 dynamic KV memory 上的 learned search/indexing：先用某种 learned index 找少量候选 KV，再在候选上做 exact sparse attention。

当前子问题：MoE expert id 能不能作为这种 index signal？要成立，expert bucket 至少应当稳定对齐某种 retrieval-relevant factor，例如 feature、rule、mapping、attention winner geometry，而不是只形成混合的 token/context cell。

本轮已有结果：

- `detailed_seq2.pdf`: prediction-position diagnostic。MoE 能学会 A-only/B-only/AB-composite，但 routing matrix 没有形成干净 A/B/AB expert；AB-dominant expert 同时接收 A-only、B-only 和 background。hidden probe 很高，说明 class 信息在 hidden state 中存在；但 expert ablation delta 很小，不能证明 expert function 有强 causal necessity。
- `detailed_seq32.pdf`: source-token diagnostic。seq_len=32 task 可学，但 source token routing 没有稳定 A/B/background bucket。A token 在 A-only 和 AB 中 dominant expert 4/4 一致；B token 只有 1/4 一致；identity/role NMI 都很低。

---

## Corrected Claim From Current Results

### Supported

1. 当前 top-1 no-load-balance MoE 能完成 synthetic A/B/AB prediction task。
2. 当前 router assignment 没有把 A/B/AB/background 分成干净 expert bucket。
3. class 信息在 hidden state 中仍然可线性解码，所以 routing 混合不是因为 representation 完全不可分。
4. 当前 source-token expert bucket 不能稳定作为 A/B/background identity 或 role index。

### Weakened

1. “ordinary MoE expert id 可以直接作为 feature-level reverse index” 被进一步削弱。
2. “只看 routing heatmap 就能判断 expert 的功能” 被削弱，因为 ablation delta 很小。

### Not Yet Supported

1. 不能说 MoE 一般按 token identity 分发。
2. 不能说 expert function 已经强混合。
3. 不能说 top-k/soft routing/load balance 一定没用。
4. 不能说真实语言中也会一样。

---

## Main Scientific Gap Exposed

当前最大缺口不是“再跑一个类似 heatmap”，而是：

> hidden state 可以被 class probe 分开，但 router projection 没有按 class 分开。我们需要知道 router 实际使用的是 hidden state 的哪个 factor。

数学上，假设 hidden state 可粗略分解为：

$$
h = h_{id} + h_{pos} + h_{leftctx} + h_{rule} + h_{target} + \epsilon.
$$

router 对 expert $e$ 的 score 是：

$$
s_e(h) = w_e^\top h.
$$

那么真正决定 routing 的不是“$h$ 里有没有 class 信息”，而是：

$$
w_e^\top h_{id},\quad w_e^\top h_{pos},\quad w_e^\top h_{leftctx},\quad w_e^\top h_{rule},\quad w_e^\top h_{target}
$$

哪个贡献最大。

因此下一步最重要的问题是：

> router score/expert id 的主导 factor 是 token identity、position、left context、rule/function、target，还是更粗的 predictive-signal cell？

---

# Experiment Line: E0522 Router Factor Audit

## Decision Question

在当前 A/B/AB synthetic task 中，ordinary top-1 MoE 的 router 到底主要根据哪个 factor 分发？

候选解释：

1. token identity routing;
2. position routing;
3. left-context routing;
4. rule/function routing;
5. target/prediction routing;
6. mixed predictive-signal routing;
7. seed-dependent arbitrary partition。

---

## Stage 1 - Existing-Run Router Factor Audit

### Purpose

用已有 `seq2` 和 `seq32` artifacts，不重新训练，先判断 router assignment/score 与哪些已知 factor 对齐。这一步回答“router 到底像什么”，避免继续凭 heatmap 直觉判断。

### Relation To Mainline

如果 expert id 要成为 KV index，它必须对齐 retrieval-relevant factor。若 router 主要由 token identity、position 或 arbitrary cell 决定，则 expert bucket 不是可靠 index signal。

### Data Needed

从已有 runs 中导出每个 evaluation sample/token 的：

- sample class: A-only / B-only / AB-composite / background;
- source token identity;
- source token position;
- left context summary, e.g. previous token identity, whether previous token is A;
- rule/function label;
- target label;
- hidden state $h$ at routed position;
- router logits $s = W_r h$;
- chosen expert id.

### Metrics

Primary metric:

```text
Explained routing variance / predictive accuracy of expert id from each factor set
```

Concretely fit small diagnostic models:

```text
expert_id ~ token_identity
expert_id ~ position
expert_id ~ left_context
expert_id ~ rule_label
expert_id ~ target_label
expert_id ~ identity + position + left_context + rule + target
```

Report:

- NMI(factor, expert_id);
- conditional entropy H(expert | factor);
- multinomial probe accuracy for predicting expert id from factor;
- router-logit R^2 explained by each factor;
- per-seed stability of the winning factor.

### Expected Outcomes

If identity dominates:

> expert id is closer to token bucket than functional/rule bucket.

If rule/function dominates:

> ordinary MoE may have learned a usable functional index; next step is retrieval alignment.

If position dominates:

> router may be exploiting positional shortcut, not semantic structure.

If no factor dominates and seeds differ:

> router partition is arbitrary/mixed; expert id is not reliable as index.

### What This Cannot Prove

This is still correlational. It does not prove expert function causal necessity.

---

## Stage 2 - Router Logit Component Decomposition

### Purpose

把“表征里有哪些特征”推进到“router 实际用了哪些特征”。这一步直接回应：MoE 是根据 hidden representation 的哪个部分进行路由？

### Mathematical Model

估计 additive components：

$$
h \approx \mu + h_{id} + h_{pos} + h_{leftctx} + h_{rule} + h_{target} + r.
$$

用 group means 或线性回归估计各 component，然后计算每个 component 对 router logit 的贡献：

$$
c_{e,f} = w_e^\top h_f.
$$

### Metrics

- fraction of router-logit variance explained by each component;
- component ablation: subtract $h_f$ from $h$ and recompute expert id;
- flip rate after component removal:

```text
flip_rate_f = P(argmax_e W_r h != argmax_e W_r (h - h_f))
```

### Expected Outcomes

If removing identity component changes routes most:

> router is identity-driven.

If removing rule component changes routes most:

> router is rule/function-driven.

If removing position component changes routes most:

> router is position-driven.

If no clean component dominates:

> router cell is mixed and not easily interpretable as a single factor.

### What This Cannot Prove

Component estimates depend on the additive approximation. This is diagnostic, not a final mechanistic proof.

---

## Stage 3 - Counterfactual Routing / Route Override

### Purpose

Current expert ablation delta is small, so routing heatmap cannot establish function. This stage asks whether forcing samples through alternative experts changes prediction loss.

### Relation To Mainline

An index signal must not only assign tokens; the assigned bucket should contain functionally relevant computation or retrieval candidates. Route override tests functional dependence more directly than heatmaps.

### Procedure

For each evaluation class and each expert:

```text
force route to expert e
measure CE(class)
```

Also test swaps:

```text
A-only natural route -> AB-dominant expert
AB natural route -> A-dominant expert
B-only natural route -> AB-dominant expert
```

### Primary Metric

```text
Delta CE under forced routing relative to natural routing
```

### Expected Outcomes

If forcing AB through non-AB experts hurts AB strongly:

> expert functions may be class/rule specialized.

If forcing routes barely changes loss:

> expert path is not functionally necessary, or task is solved through residual/bypass/shared path.

### What This Cannot Prove

If delta is small, it may mean either no specialization or expert path weakness. Need Stage 4 to disambiguate.

---

## Stage 4 - Expert-Path Necessity Stress Test

### Purpose

Current ablation deltas are tiny. Before concluding experts are not functional, test whether the architecture lets prediction bypass experts too easily.

### Relation To Mainline

If expert path is not necessary, then expert ids cannot be evaluated as functional index candidates. We need a setup where expert computation matters.

### Design Variants

Run the same A/B/AB task with one controlled change at a time:

1. reduce residual bypass around MoE block;
2. make FFN path MoE-only for the relevant layer;
3. reduce dense capacity outside MoE;
4. evaluate at earlier checkpoint before dense/shared path absorbs task;
5. optionally freeze attention or embeddings after dense sanity.

### Primary Metric

```text
max_class_delta_CE_after_mask_or_force_route
```

A useful run should make expert-path interventions produce nontrivial loss changes.

### Expected Outcomes

If expert necessity increases and routing remains mixed:

> mixed assignment may become mixed functional dependency.

If expert necessity increases and clean class experts emerge:

> previous weak ablation was an architecture/bypass artifact.

If expert necessity cannot be created:

> current toy task is too easy or architecture too redundant for functional specialization diagnosis.

---

## Stage 5 - Factorially Disentangled Synthetic Task

### Purpose

Current A/B/AB setup partially confounds token identity, rule, target, and predictive signal. This stage creates a more fundamental test where identity and function are independently varied.

### Relation To Mainline

A useful KV index should group tokens by retrieval-relevant function/rule, not merely by surface token identity. We need a dataset where these two hypotheses make different predictions.

### Data Design

Create many surface identities and many rule labels.

Requirements:

1. same token identity appears in multiple different rules;
2. same rule is realized by multiple different token identities;
3. target frequencies are balanced;
4. positions are balanced;
5. background tokens are frequency-matched.

Example:

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

Here token A1 appears in multiple rules, and rule R1 appears across multiple identities.

### Competing Predictions

Identity routing predicts:

```text
same surface token -> same expert, even across rules
```

Rule/function routing predicts:

```text
same rule -> same expert, even across different surface tokens
```

Position routing predicts:

```text
same position -> same expert
```

### Primary Metric

```text
NMI(rule, expert_id) - NMI(identity, expert_id)
```

and per-seed stability of this difference.

### Expected Outcomes

If rule NMI > identity NMI stably:

> ordinary MoE can form rule-level specialization under controlled disentanglement.

If identity NMI > rule NMI stably:

> ordinary MoE is closer to identity routing than functional routing.

If both are low:

> expert id is not a stable index signal in this setup.

---

## Stage 6 - Gated Retrieval Alignment

### Gate

Only run this if earlier stages show a stable factor-aligned expert bucket.

### Purpose

Return to the mainline: check whether the factor-aligned expert bucket retrieves dense-attention high-mass KV tokens better than matched random.

### Metrics

- Recall@K of dense attention top-M tokens;
- attention mass covered;
- output reconstruction error under exact sparse attention over retrieved candidates;
- matched-random baseline.

### Decision

If expert bucket improves retrieval:

> continue toward learned index / exact sparse attention.

If expert bucket is clean but retrieval fails:

> specialization exists but is not attention-retrieval relevant.

If no clean bucket exists:

> do not spend time on retrieval yet.

---

# Immediate Agent Task Spec

## Task 1 - Parse Existing Artifacts

Extract per-token/per-sample records from existing `h0521` and `h0521b` results.

Required output CSV/parquet columns:

```text
run_id
seed
sample_id
sample_class
position
token_id
token_role
left_token_id
right_token_id_if_available
target_id
rule_label
hidden_state_path_or_array
router_logits
expert_id
loss
```

## Task 2 - Compute Factor Metrics

For each seed and each routed position:

```text
NMI(factor, expert_id)
H(expert_id | factor)
expert prediction accuracy from each factor
router-logit R^2 by factor
```

Factors:

```text
token_id
position
left_context
sample_class
rule_label
target_id
background_vs_signal
```

## Task 3 - Make Figures

Required figures:

1. per-seed factor NMI bar plot;
2. per-seed router-logit R^2 by factor;
3. expert_id confusion conditioned on strongest factor;
4. route flip rate after subtracting each component;
5. route override Delta CE heatmap, if available.

## Task 4 - Summary.md

Write claim-safe result summary:

```markdown
# Result Summary: E0522 Router Factor Audit

## Purpose And Hypothesis
## Observation
## Interpretation
## Claim Update
## What Cannot Be Claimed
## Next Decision
```

---

# 30s Meeting Version

当前结果不是直接证明“MoE 按 token id 路由”，而是更克制地说明：ordinary no-load-balance top-1 MoE 没有形成稳定、干净的 feature/rule-level bucket。seq2 里 AB-dominant expert 同时接收 A/B/background，hidden probe 说明 class 信息还在 hidden state 中，但 router projection 没有按 class 切；seq32 里 A token 在不同 context 下稳定到同一 expert，但这在 causal source-token 位置是预期的，因为 A 看不到未来 B。真正下一步是做 router factor audit：把 hidden state 分解成 identity、position、left context、rule、target 等 component，直接看 router logit 的方差主要由哪个 component 解释。只有当 expert id 稳定对齐 rule/function 后，才继续测它能不能当 KV reverse index。

