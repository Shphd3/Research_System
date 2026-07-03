---
anchor_id: A06_14_real_dclm_proxy_expert_utility_binding
parent_node: rq.real_data_feature_specialization.utility_binding
status: parked_dependency_failed
created: 2026-06-22
canonical_language: en
---

# A06_14 Real-DCLM Proxy Expert-Utility Binding Anchor

## 0. Thinking Card
父问题：feature-level routing 只有在 assignment 与 expert function 绑定时才是 expert specialization。
当前子问题：若 A06_12 保持 proxy routing，所选 experts 是否对对应 proxy tokens 有更高 causal utility？
当前判断：暂停。A06_12 没有保持 proxy routing，因此现在测试 utility binding 会混淆“没有 utility”和“路由已经坍缩”。
关键证据：A06_12 raw_center proxy_route_NMI 从 step0 0.7549 降到 step10 0.0131；A06_13 判定第一失败点是 training feedback override。
最危险边界：不能在 proxy routing 未保持时，用 utility 结果否定 expert specialization。
下一步决策：先做 preservation / anti-feedback；只有 proxy routing 能保持后再恢复 A06_14。

Question: Does preserved real-DCLM proxy routing select experts that causally improve prediction for the same proxy token groups?
Physical prior: useful specialization requires assignment-function binding, not just stable buckets.
Core model: compare normal routing loss with forced-to-assigned, forced-to-other, and expert-ablation losses within each proxy group.
Model term being tested: causal utility of routed experts for proxy groups.
Primary metric: proxy-conditioned utility gap between assigned expert and alternative experts.
Falsifier: high proxy_route_NMI but no assigned-expert utility advantage.
Can claim: assignment and expert utility are aligned for the proxy groups.
Cannot claim: semantic specialization or full downstream utility.
Next decision: build utility-aware gating init if supported; otherwise study route-function mismatch.

## 1. Problem Definition

Parent problem: expert specialization is not only where tokens route, but what experts do.
Sharper subproblem: test whether proxy-routed experts have causal prediction utility.
Decision question: do assigned experts reduce loss more than alternative experts for their proxy tokens?
Not in scope: semantic labels, long-run pretraining, downstream tasks.

## 2. Physical Priors

P1: Top-1 assignment may be decoupled from utility.
Meaning: a router can form stable buckets that do not select the best expert for prediction.
Could be wrong if: assignment consistently matches forced-routing utility.

P2: Utility must be proxy-conditioned.
Meaning: aggregate utility can hide that different proxy groups need different experts.
Could be wrong if: all experts are functionally identical at this training stage.

P3: Loss is the immediate causal utility signal.
Meaning: forced routing / ablation loss deltas measure expert contribution to prediction.
Could be wrong if: short-window loss is too noisy or proxy groups are too small.

## 3. Falsifiable Hypotheses

H1: assigned experts have proxy-conditioned utility advantage.
Supported if: forced assigned expert has lower loss than forced alternatives within proxy groups.
Weakened if: utility is flat or alternatives outperform assigned experts.

H2: utility binding strengthens after early training.
Supported if: gap grows from step 0 to step 50/300.
Weakened if: routing remains stable but utility gap stays absent.

## 4. Mathematical Model

Objects: proxy group $q$, assigned expert $a$, forced expert $e$, loss $\ell(x,y;e)$.

Utility gap:
$$
U_q=\mathbb{E}_{i:q_i=q}\left[\ell_i(e\neq a_i)-\ell_i(e=a_i)\right].
$$

Support requires $U_q>0$ for most proxy groups with confidence / seed stability.

## 5. Computational Realization

- Use A06_12 checkpoints with preserved proxy routing.
- For each proxy group, evaluate normal routing, forced assigned expert, forced random alternative, forced best oracle expert, and expert ablation where feasible.
- Save loss deltas by layer, proxy group, expert, checkpoint.
- Plot utility heatmaps and assignment-utility agreement.

## 6. Minimal Falsification Tests

Test: proxy-conditioned forced routing.
Question: does assigned expert causally help its proxy group?
Primary metric: assigned-vs-alternative loss delta.
Supports: positive utility gap and seed stability.
Weakens: no utility advantage.
Insufficient: proxy groups too small, loss estimates noisy, or forced-routing implementation changes non-expert paths.

## 7. Current Evidence

- A06_09 provides routing preservation only, not utility.
- A06_01 forced-utility correlations were weak for spectrum initializations.
- Project definition requires utility binding before claiming expert specialization.
- A06_12 failed the preservation dependency; A06_13 localized the bottleneck to training feedback override.

## 8. Claim Boundary And Next Decision

Can claim: whether preserved proxy routing has causal expert utility in the tested DCLM model.
Cannot claim: semantic expert roles, long-run usefulness, or downstream task gains.
Next decision: parked until a preservation intervention restores proxy routing through the early training window.
