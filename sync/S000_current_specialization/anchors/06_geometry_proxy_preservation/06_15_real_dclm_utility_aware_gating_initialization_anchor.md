---
anchor_id: A06_15_real_dclm_utility_aware_gating_initialization
parent_node: rq.real_data_feature_specialization.utility_aware_initialization
status: parked_dependency_failed
created: 2026-06-22
canonical_language: en
---

# A06_15 Real-DCLM Utility-Aware Gating Initialization Anchor

## 0. Thinking Card
父问题：真实 DCLM gating init 最终应让 router 选择对 token/proxy group 有用的 expert，而不只是稳定分桶。
当前子问题：若 A06_14 找到 proxy-conditioned utility signal，能否把 utility signal 合入 router initialization 并改善 early training？
当前判断：暂停。A06_14 因 A06_12 preservation 失败而暂停，因此 A06_15 没有合法输入 utility table。
关键证据：A06_13 判定当前 bottleneck 是 training feedback override，下一步应优先测试 preservation/anti-feedback，而不是 utility-aware init。
最危险边界：不能在未证明 routing 可保持、utility 可测的情况下构造 utility-aware initialization。
下一步决策：等 preservation anchor 通过并恢复 A06_14 后再执行。

Question: Can proxy-conditioned utility information produce a better real-DCLM gating initialization than proxy centers alone?
Physical prior: a router should dispatch tokens to experts with causal utility for those tokens; proxy geometry alone may not encode this utility.
Core model: initialize rows from a combination of proxy residual centers and utility-weighted expert compatibility scores.
Model term being tested: route-function binding inside initialization.
Primary metric: combined preservation/utility score: proxy_route_NMI, utility gap, LM loss, and common/load guards.
Falsifier: utility-aware init improves load or loss but loses proxy utility binding, or worsens early common amplification.
Can claim: utility signal can improve real-data gating initialization in the tested model.
Cannot claim: final DCLM method, semantic experts, or large-scale transfer.
Next decision: scale/robustness if supported; otherwise decompose proxy vs utility mismatch.

## 1. Problem Definition

Parent problem: real expert specialization requires assignment and utility to agree.
Sharper subproblem: use measured utility to guide initialization, not only hidden-state clusters.
Decision question: does utility-aware initialization improve early routing and loss compared with proxy-center init?
Not in scope: pretrained MoE, long-run scaling, semantic labels.

## 2. Physical Priors

P1: Utility is not necessarily the same as geometric cluster identity.
Meaning: proxy centers may form clean buckets whose experts are not best for prediction.
Could be wrong if: A06_14 shows geometry and utility already align perfectly.

P2: Utility-weighted initialization can reduce route-function mismatch.
Meaning: rows should favor directions whose assigned experts reduce loss for that proxy group.
Could be wrong if: utility estimates are too noisy or nonlinearly encoded.

P3: Common/load guards remain necessary.
Meaning: utility-aware rows can still enter common collapse.
Could be wrong if: utility binding alone prevents concentration.

## 3. Falsifiable Hypotheses

H1: utility-aware init improves utility gap over proxy-center init.
Supported if: assigned-vs-alternative utility gap increases without loss penalty.
Weakened if: utility gap is unchanged or worse.

H2: utility-aware init preserves proxy routing.
Supported if: proxy_route_NMI stays near proxy-center init.
Weakened if: utility improvement destroys proxy partition.

H3: utility-aware init does not worsen early common/load amplification.
Supported if: step-10 common_margin_delta and raw_max_load are no worse than proxy-center init.
Weakened if: it reintroduces common collapse.

## 4. Mathematical Model

Objects: residual center $\nu_q$, utility score $u_{q,e}$, router row $w_e$.

Utility-weighted row target:
$$
w_e \propto \sum_q \operatorname{softmax}_q(u_{q,e}/\tau)\nu_q.
$$

Decision metrics:
proxy_route_NMI, utility gap, LM loss, common_margin_delta, and load $L$.

## 5. Computational Realization

- Inputs: A06_10 proxy centers, A06_14 utility table.
- Conditions: random, proxy-center init, utility-only init, utility-weighted proxy init, label-shuffled utility guard.
- Train 0--300 steps with exact gate audit.
- Save trajectory, utility heatmaps, loss curves, common/load metrics.

## 6. Minimal Falsification Tests

Test: utility-aware initialization comparison.
Question: does utility information improve initialization beyond proxy centers?
Primary metric: utility gap with proxy_route_NMI and loss guards.
Supports: utility gap improves and routing remains stable.
Weakens: no utility gain, proxy collapse, or worse common amplification.
Insufficient: A06_14 utility signal absent or noisy.

## 7. Current Evidence

- A06_01 suggests expert-spectrum utility signal can exist but is not enough through current linear bridge.
- A06_14 is required to determine whether proxy-conditioned utility is measurable.
- A06_12 is required to ensure proxy-center routing can be preserved before adding utility.
- A06_12 failed preservation and A06_13 localized the failure to training feedback override, so this anchor is parked.

## 8. Claim Boundary And Next Decision

Can claim: whether measured utility can improve real-data gating initialization in the tested small DCLM MoE.
Cannot claim: final method, semantic experts, or large-scale transfer.
Next decision: parked until proxy routing preservation and A06_14 utility binding are both supported.
