# Next Iteration Plan - 0517

## 一句话结论

下一轮不要继续问“能否 one-feature-one-expert”，而要诊断 **linear top-1 router 在 feature representation 已可分时，到底按什么变量分发 token，以及为什么 NTP loss 不要求它按 ABC/DEF/GHI/JKL 分。**

## Mainline update

**Yes, as experiment plan.** 当前主线应固定为：

```text
representation separability != router specialization
```

下一步必须把这个现象拆成可证伪的 failure modes。

## Decision Question

在 controlled synthetic trigram NTP 中，router input hidden states 已经保留 feature identity；为什么 learned linear router 没有形成 clean feature-aligned expert partition？

更具体：

```text
router choice 是由 feature_id 解释，还是由 token shortcut / target token / frequency / hidden norm / loss difficulty / early expert utility / shared-path bypass 解释？
```

## Mainline Anchor

已有 E2 结果：

- E2.0：MoE 能读回 planted trigram features；`P(expert|feature)` 高于 random；dominant expert ablation 会伤害 readback。
- E2.1：feature identity 在 router input hidden space 中可分；Fisher ratio 高；但 router boundary 与 feature-difference direction alignment 低，router entropy 接近 `log(4)`。
- E2.2：降低 expert capacity 或增加 feature count 没有强制 one-feature-one-expert；readback 仍高，dominant ablation effect 变弱。

当前最稳解释：

```text
NTP loss only rewards prediction.
If prediction can be solved by shared path or multiple experts,
router has no need to learn human-defined feature boundaries.
```

## Hypothesis

### H1: Token shortcut failure

Router 主要按 prefix-end token、target token 或 surface token identity 分，而不是按完整 context relation 分。

**可证伪预测：**

- `expert_id ~ prefix_end_token` 的解释力高于 `expert_id ~ feature_id`。
- 构造同一 prefix-end token 但不同 feature relation 的 counterfactual 后，router 跟 token 走，不跟 feature 走。

### H2: Scale / confidence / difficulty failure

Router 主要按 hidden norm、activation scale、CE difficulty、target margin 或 confidence 分。

**可证伪预测：**

- `expert_id ~ hidden_norm + CE + target_margin` 的解释力显著高于 feature label。
- 同一 feature 内按 difficulty 分桶后，不同桶路由到不同 experts。

### H3: Expert utility degeneracy

多个 experts 都能完成同一 feature prediction；router 只需要选择一个 loss-compatible path，而不是 feature-exclusive path。

**可证伪预测：**

- forced-routing utility matrix `U(feature, expert)` 每行多个 expert 接近最优。
- learned router 选择的 expert 不总是唯一最大 utility expert，但 loss 不受明显影响。
- feature oracle router 的 readback/loss 与 learned router 差距小。

### H4: Shared-path bypass

Attention/residual/LM head 已经承担主要 feature computation，MoE expert path 只是辅助；因此 router specialization 不是必要解。

**可证伪预测：**

- zero/ablate MoE path 后 readback 仍高，或 ablation drop 很小。
- zero/limit residual/attention/LM head contribution 后，router alignment 才增强。
- E2.2 中 dominant expert ablation collapse 与 shared path contribution 增强同步。

### H5: Early routing history / co-adaptation lock-in

初始随机 routing 的微小优势会被 expert co-adaptation 固化；后续 router boundary 不再寻找 feature-separating direction。

**可证伪预测：**

- early checkpoints 的 route assignment 与 final assignment 高相关。
- 早期 force-router / supervised warmup 会显著改变最终 specialization。
- seed 间 expert identity 不稳定，但 early-to-final trajectory 稳定。

## Mechanism / Modeling

把 router 决策写成：

```text
r_t = argmax_k w_k^T h_t
```

当前错误直觉是：

```text
if feature clusters separable in h_t, then router should separate them.
```

正确建模是：

```text
router only receives gradient through downstream loss and selected expert utility.
```

因此 router 更可能近似选择：

```text
expert k that gives enough loss decrease under current co-adapted experts
```

而不是选择：

```text
expert k that maximizes human-defined feature purity
```

下一步要估计：

```text
I(expert; feature_id)
I(expert; prefix_end_token)
I(expert; target_token)
I(expert; frequency_band)
R^2 / accuracy of expert_id from hidden_norm, CE, margin, PCA, logits
U(feature, expert) = forced-routing predictive utility
```

## Empirical Study

### E3.0 Static Router Behavior Decomposition

**Question:** final checkpoint 的 expert choice 最能被什么变量解释？

**Inputs per feature event:**

- `feature_id`: ABC/DEF/GHI/JKL or 16-feature labels
- `prefix_end_token`: B in `[A,B]->C`
- `target_token`: C
- `frequency_band`: high/mid/low
- `hidden_norm`: `||h_t||`
- `router_logits`: `W h_t`
- `router_margin`: top1 - top2
- `router_entropy`
- `CE loss`, `target_margin`, `target_probability`
- PCA coordinates of `h_t`

**Models:**

- multinomial logistic regression / small decision tree predicting expert id from each variable group;
- compare explained accuracy / NMI / pseudo-R2;
- conditional tests: predict expert id after controlling for feature_id.

**Key output table:**

| Predictor group | Expert-id accuracy | NMI with expert | Interpretation |
|---|---:|---:|---|
| feature_id only | | | feature-driven routing |
| prefix/target token | | | token shortcut |
| norm/CE/margin | | | difficulty/scale routing |
| PCA coords | | | geometry routing |
| router logits dims | | | direct linear-boundary explanation |

### E3.1 Forced-Routing Utility Matrix

**Question:** router 不按 feature 分，是因为专家功能不够不同，还是因为多个专家都能用？

For each feature `f` and expert `e`, force all feature examples to expert `e` and measure:

```text
U(f,e) = target probability / CE / readback under forced route
```

**Metrics:**

- best-vs-second-best utility gap;
- learned expert utility rank;
- row entropy over experts;
- correlation between router probability and utility.

**Interpretation:**

- One dominant expert per feature + router ignores it => router training failure.
- Multiple high-utility experts per feature => no pressure for exclusive specialization.
- Learned router selects low-utility expert => serious gating failure.

### E3.2 Counterfactual Shortcut Test

**Question:** router 是跟完整 relation 走，还是跟 token identity 走？

Construct counterfactuals:

```text
same prefix-end token, different preceding token / relation
same target token, different context relation
same feature relation, altered surface token identity if possible
```

**Metrics:**

- route consistency under same feature / changed token;
- route consistency under same token / changed feature;
- readback under counterfactual.

**Interpretation:**

- Router follows token identity: shortcut failure.
- Router follows relation: feature-aware routing.
- Readback follows relation but routing follows token: representation learned, gating not aligned.

### E3.3 Training Dynamics Trace

**Question:** routing 是不是早期固化？

Save checkpoints at:

```text
step = 0, 10, 50, 100, 200, 500, 1000, 2000, 5000, 10000
```

Track:

- `P(expert|feature)`
- NMI / ARI
- route assignment agreement with final checkpoint
- expert load
- router margin/entropy
- forced-routing utility matrix over time
- gradient norm into each expert by feature

**Interpretation:**

- Early agreement high => initialization + co-adaptation lock-in.
- Utility becomes high after routing assigned => expert adapts to router, not router discovers feature.
- Feature clusters appear before router alignment => representation separability precedes specialization but does not cause it.

### E3.4 Shared-Path Bypass Diagnostic

**Question:** feature readback 是否绕过 MoE path？

Ablations:

- zero MoE output;
- zero residual bypass around MoE if architecture allows;
- freeze / randomize LM head after training for diagnostic only;
- compare dense attention contribution vs MoE FFN contribution via logit lens / activation patching;
- reduce shared path capacity rather than expert capacity.

**Metrics:**

- target probability drop by component;
- feature readback after component ablation;
- expert ablation drop vs residual/attention ablation drop.

**Interpretation:**

- If MoE ablation small but shared path ablation large, router specialization is not required by current task.
- If removing shared bypass increases feature-expert alignment, current failure mode is objective/architecture shortcut.

### E3.5 Objective Intervention, Only After Diagnosis

Do not start here. Run only after E3.0-E3.4 identify failure.

Interventions:

- feature-supervised router auxiliary loss;
- contrastive router loss: same feature close, different feature apart;
- router margin regularization;
- common/specialized split: one shared common expert + routed specialized experts;
- top-2 routing to expose sharing;
- load-balance variants: no-LB, LB, loss-free/bias-style balancing if implemented;
- frozen representation + train router/expert separately.

Purpose:

```text
turn diagnosis into architecture idea
```

Not allowed yet:

```text
claiming new architecture solves real language specialization
```

## Expected Outcomes and Claim Updates

### Outcome A: feature_id is not the best predictor of expert id

Claim update:

```text
Supported: router does not primarily use human-defined feature identity despite feature separability.
```

### Outcome B: forced-routing shows many experts can predict each feature

Claim update:

```text
Supported: lack of one-feature-one-expert is not representation collapse but utility degeneracy / expert sharing.
```

### Outcome C: shared-path ablation carries most readback

Claim update:

```text
Supported: current NTP setup has a shortcut; MoE specialization is underdetermined by the loss.
```

### Outcome D: early assignment predicts final assignment

Claim update:

```text
Supported: routing dynamics are path-dependent; early co-adaptation matters.
```

### Outcome E: supervised/oracle router improves reverse-index recall but not NTP loss

Claim update:

```text
Supported: NTP quality and reverse-index usefulness are different objectives.
```

## What Must Be Clearer

1. What exactly is a `feature` in the synthetic setup: motif/event label, not semantic concept.
2. Whether `expert specialization` means routing purity, expert causal contribution, or reverse-index retrieval quality.
3. Whether failure is in representation, router, expert utility, or task objective.
4. Whether current readback is carried by MoE expert output or shared residual/attention/LM head.
5. Whether Zipf/common-dominated data changes the failure mode or only amplifies it.

## Minimal Next Action

Run **E3.0 + E3.1** first.

```text
E3.0: final-checkpoint router behavior decomposition
E3.1: forced-routing utility matrix
```

These two are decisive because they separate:

```text
router not seeing feature
vs
router seeing feature but not using it
vs
experts not functionally distinct
vs
NTP loss not requiring distinct experts
```

## Implementation Notes for Experiment Agent

Output one CSV per event and one aggregate table:

```text
artifacts/E3_router_behavior/events.csv
artifacts/E3_router_behavior/predictor_group_scores.csv
artifacts/E3_router_behavior/forced_routing_utility.csv
artifacts/E3_router_behavior/training_dynamics.csv
```

Required figures:

```text
figures/predictor_group_expert_accuracy.png
figures/forced_routing_utility_heatmap.png
figures/router_assignment_over_time.png
figures/feature_vs_token_shortcut_counterfactual.png
```

Required result block:

```markdown
## Result R3

### Observation

### Interpretation

### Failure Mode Selected

### Claim Update

### What Cannot Be Claimed

### Next Decision
```

## 30s Advisor Version

E2 已经说明 feature representation 没有消失，但 router 没有沿 feature-difference direction 做 clean partition。所以下一步我不再追求 one-feature-one-expert，而是做 router behavior decomposition：用 feature id、prefix token、target token、hidden norm、CE difficulty、PCA 坐标分别预测 expert id，同时做 forced-routing utility matrix。这样可以判断 linear router 是按 token shortcut、scale/difficulty、expert utility，还是 early co-adaptation 分发。如果 feature 可被 probe 读出但 expert choice 主要由别的变量解释，就可以把 failure mode 钉成 `representation separability != router specialization`，再决定是否需要 common/specialized split 或新的 gating objective。

## Files to update

- `Projects/MoE-Continual-Learning/main/next_iteration_plan.md`: Replace broad next-step discussion with E3.0/E3.1 as the minimal decisive diagnostics.
- `daily_research_reports/0517/experiment_analysis.md`: Add this plan as the next experiment card.
- `Projects/MoE-Continual-Learning/main/claim_board.md`: Add claim boundary: current evidence supports representation separability but not feature-aligned router specialization.
