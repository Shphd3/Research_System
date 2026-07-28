# 待审计 Protocol：A11_04 K=3 First-Informative-Horizon Experiment

## 0. 审批快照

Approval status: approved by user request on 2026-07-07; implementation and run requested.

Purpose: 检验 next-$K$ 优势是否由“active horizon 覆盖第一个含早期变量的信息位置”决定，而不是 next-two 的特殊性。

Primary anchor: `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_04_k3_first_informative_horizon_anchor.md`

Anchor decision question: 在 $\tau=3$ 的 branch-delayed 任务中，K=3 是否比 K=1/K=2 更能让 $Z$ 从 $h_T$ 中恢复，同时不损害 $Y_1,Y_2$ 学习？

Anchor physical prior tested: 若 $K<\tau$，active loss 没有 branch-specific target；若 $K\ge\tau$ 且 $Y_\tau=S_Z$，低 offset-$\tau$ loss 要求 $h_T$ 含有 $Z$。

Anchor core model term tested: K=3 中的 $\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$。

Anchor falsifier: 如果 K=2 在 clean $\tau=3$ regime 中与 K=3 表现相同，且未发现泄漏，则 first-informative-horizon coverage 机制被削弱。

Experiment role: mechanism generalization test / operationalization test.

Primary metric from anchor: `coverage_gap`，即 K=3 与最强 non-covering condition K=1/K=2 的 guarded recovery 曲线面积差。

Claim boundary from anchor: 本实验只判断受控 $\tau=3$ 构造中的 coverage principle；不能证明 larger K always helps，不能证明 curriculum 或自然语言迁移。

Minimal setup: 第一版只跑 `decision_only`，loss 只在 prediction site 计算。这样直接测试 $h_T\to(Y_1,Y_2,Y_3)$。

Basic configuration: `num_branches=4`, `filler_length=16`, `shared_context_length=4`, one-layer one-head Transformer, `d_model=64`, $\lambda_2=\lambda_3=1.0$, seeds `971-975`, training budget initially `15000` steps.

Conditions to run:

1. `K1_fixed_3head`: model has up to 3 heads but active horizon only 1.
2. `K2_active`: active horizons 1 and 2.
3. `K3_active`: active horizons 1, 2, and 3.
4. Clean $\tau=3$ regime: $Y_1=A$, $Y_2=C$, $Y_3=S_Z$.
5. Noisy horizon-3 guard: $Y_3\perp Z$.
6. Redundant horizon-3 guard: earlier target already reveals $Z$, so $Y_3$ should not create a new coverage claim.

Pass: K=3 has positive `coverage_gap`, reaches guarded branch recovery earlier or uniquely, local $Y_1,Y_2$ guards pass, noisy control does not pass.

Fail: K=2 matches K=3 in clean $\tau=3$ without leakage; or K=3 fails despite task realizability; or all conditions recover $Z$ equally.

Insufficient: K=3 does not learn due to optimization failure, leakage audit unresolved, or evaluation decoder unstable.

Cannot claim: broad next-$K$ scaling, real language, curriculum benefit, or that K=2 is useless in other distributions.

Approval decision: run.

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 单位或公式 | 为什么影响判断 | 不能证明什么 |
|---|---|---|---|---|---|
| first informative horizon $\tau$ | 第一个提供 $Z$ 新信息的未来位置 | $\tau=\min\{j:I(Z;Y_j\mid Y_{<j})>0\}$ | token offset | 主机制变量 | 自然语言 horizon |
| covering condition | active horizon 覆盖 $\tau$ | $K\ge\tau$ | Boolean | 应该有直接分支监督 | 优化一定成功 |
| non-covering condition | active horizon 小于 $\tau$ | $K<\tau$ | Boolean | 不应有直接分支监督 | 完全无泄漏 |
| K=1 | 只预测 $Y_1$ | active horizons `{1}` | condition | NTP / fixed baseline | 所有 NTP 行为 |
| K=2 | 预测 $Y_1,Y_2$ | active horizons `{1,2}` | condition | $\tau=3$ 下的 non-covering control | K=2 一般无用 |
| K=3 | 预测 $Y_1,Y_2,Y_3$ | active horizons `{1,2,3}` | condition | main covering condition | broad next-K |
| guarded score $Q_K$ | 保守语义恢复分数 | $\min\{A_K,P_K,S_K\}$ | 0 到 1 | 防止 probe-only 假阳性 | 完整机制 |
| `coverage_gap` | K=3 相对 non-covering 条件的优势 | $\operatorname{AUC}_Q(3)-\max(\operatorname{AUC}_Q(1),\operatorname{AUC}_Q(2))$ | score gap | 主判定指标 | 单独阈值速度 |

## 2. Anchor 对齐

Decision question: $\tau=3$ 时，K=3 是否产生 K=1/K=2 没有的 branch recovery？

Physical prior tested: horizon 覆盖第一个 informative token 后，MTP 才获得直接语义监督。

Core model term tested: $\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$。

Falsifier: K=2 在没有泄漏的 $\tau=3$ clean task 中匹配 K=3。

Claim boundary: 只裁定 first-informative-horizon coverage，不裁定 K 越大越好。

## 3. 被检验假设

H1: 在 clean $\tau=3$ regime 中，K=3 的 $Q_K(t)$ 显著高于 K=1/K=2。

H2: K=3 的优势不是通过损害 $Y_1,Y_2$ 获得。

H3: noisy horizon-3 和 redundant horizon-3 controls 不产生同样的 coverage claim。

## 4. 替代解释

1. Extra-head explanation: K=3 只是因为有更多 heads/参数。
2. Loss-scale explanation: K=3 只是因为总 loss 更大。
3. Leakage explanation: $Z$ 泄漏到 $Y_1,Y_2$、filler、position 或 token frequency。
4. Probe-only explanation: probe 可读但 horizon-3 prediction / swap 不成立。
5. Optimization-failure explanation: K=3 有正确目标但当前模型/优化器学不会。

## 5. 数据 / 模型 / 算法 / 目标

Clean $\tau=3$ data:

```text
BR_z F00 ... F{L-1} U00 ... U{s-1} A_SHARED C_SHARED S_z STOP
```

Prediction prefix:

```text
BR_z F00 ... F{L-1} U00 ... U{s-1}
```

Targets:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

Information:

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

Objectives:

$$
L_K=\sum_{j=1}^{K}\lambda_j\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
$$

For K=1/K=2, no active loss directly targets $S_Z$. For K=3, active loss includes $q_3(\cdot\mid h_T)\to S_Z$.

Model: same base Transformer with heads up to horizon 3. Change active horizons only.

Evaluation:

1. 每个 checkpoint 冻结 $h_T$。
2. 用同一套 matched evaluation decoder 评估所有 K 的 $h_T\to S_Z$。
3. 计算 branch probe、branch swap、local guards。
4. K=3 额外报告 native head-3 accuracy。

## 6. 条件、seeds、checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
|---|---|---|---|---|---|---|---|---|
| clean K=1 | non-coverage baseline | no branch target | baseline | $Q_1(t)$, local loss | low/delayed | high without explanation | unstable eval | main curve |
| clean K=2 | non-covering control | active $Y_1,Y_2$ only | tests next-two special case | $Q_2(t)$ | similar to K=1 | matches K=3 | leakage unclear | main curve |
| clean K=3 | covering condition | active $Y_3=S_Z$ | main mechanism | $Q_3(t)$, head3, swap | high/earlier | fails despite realizable | optimization unclear | main curve |
| noisy K=3 | noisy control | $Y_3\perp Z$ | false-positive guard | head3 near chance | stays low | behaves like clean | high variance | guard table |
| redundant control | redundancy guard | earlier target reveals $Z$ | separates new info from local continuation | explained by earlier target | no new claim | unexplained gain | ambiguous | guard table |

Seeds: `971,972,973,974,975`.

Checkpoints: recommended every `500` steps; enough to estimate `AUC_Q` and threshold crossing.

## 7. Primary Metric

Primary metric:

$$
\Delta_{\mathrm{cov}}=
\operatorname{AUC}_Q(3)-\max\{\operatorname{AUC}_Q(1),\operatorname{AUC}_Q(2)\}.
$$

Why it decides: anchor 的问题不是“最终 K=3 是否能学会”，而是“覆盖 $\tau$ 是否带来相对 non-covering horizons 的优势”。`coverage_gap` 直接比较 covering vs non-covering。

False positive cost: 若 K=2 因泄漏而高分，会误判 coverage principle。必须做 leakage audit。

False negative cost: 若 K=3 因优化失败学不会，不能直接否定 coverage theorem，只能说明当前实现不足。

## 8. Secondary Metrics

- `T_0.9_Q`: K=3 是否更早达到 threshold。
- `native_head3_accuracy`: K=3 是否学会自己的 informative target。
- `branch_swap_consistency_for_Sz`: 是否随 branch token 切换。
- `frozen_probe_hT_to_Z_accuracy`: 表示可读性。
- `Y1/Y2_accuracy`, `Y1/Y2_loss`: local guards。
- optional $U_3$: offset-3 gradient 是否有助于 branch recovery。

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: A11_01 $\tau=2$ 中 K=2 可以迫使 $h_T$ 含有 branch information。

Known bad: noisy target 不应产生 native informative-horizon accuracy。

Known confusing: 如果 K=1/K=2 的 probe 高，但 horizon-3 prediction/swap 不高，不能说 non-covering condition 学会了可用 branch future prediction。

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
|---|---|---|---|---|---|
| data audit | $\tau=3$ 是否真的成立 | sample/frequency table | no leakage / leakage | sample table | detailed |
| training smoke | K=1/2/3 是否稳定训练 | small run logs | no crash / crash | smoke logs | not central |
| eval pipeline | K=1/2/3 是否公平评估 | eval decoder split | stable / overfit | decoder table | detailed |
| coverage curve | K=3 是否超过 K=1/2 | $Q_K(t)$ | pass/fail/insufficient | main figure | summary |
| guard audit | local/noisy/redundant 是否通过 | guard metrics | pass/fail | guard table | summary |

## 11. 算法说明

input: K=1/K=2/K=3 checkpoints, train/eval split, branch-swap prefixes.

parameters: threshold `0.9`, same base architecture, same seeds, same checkpoint schedule.

intermediate variables: $h_T$, eval decoder logits, branch probe logits, swap logits, native head-3 logits.

steps:

1. Generate clean $\tau=3$ data and controls.
2. Train K=1, K=2, K=3 with matched architecture and active-horizon masks.
3. At each checkpoint, evaluate $Q_K(t)$ with the same frozen-state evaluation pipeline.
4. Compute `coverage_gap`, `T_0.9_Q`, final $Q$, local guards, noisy/redundant guard outcomes.

outputs: main K=1/K=2/K=3 curve, coverage table, guard table, leakage audit, artifact map.

failure reasons: leakage, optimization failure, evaluation overfit, loss-scale confound, local-loss tradeoff.

## 12. Success / Failure / Insufficient Evidence

Success: K=3 has positive `coverage_gap`, reaches or approaches threshold earlier than K=1/K=2, local guards pass, noisy guard stays negative.

Failure: K=2 matches K=3 in clean $\tau=3$ without leakage, or all conditions recover equally, or K=3 only wins by harming local targets.

Insufficient: K=3 fails to learn despite direct target, leakage audit unresolved, or evaluation decoder unstable.

## 13. What This Cannot Claim

- Larger K always helps.
- K=2 is generally useless.
- Natural-language long-horizon learning improves.
- Curriculum helps.
- The same result holds under all-position LM training.

## 14. Review Notes And Protocol Changes

需要你审核的点：

1. 第一版是否只跑 `decision_only`？我建议是，因为它最干净地测试 first-informative-horizon coverage。
2. K=3 是否必须等 A11_03 跑完再跑？我认为可以和 A11_03 同时跑，因为它检验不同 anchor；但汇报解释上应先讲 A11_03。
3. 是否固定 `filler_length=16`？我建议先固定以对齐 A11_02；如果 K=1/K=2 泄漏太强，再加长 filler 或 identical init。
4. 是否使用 `K1_fixed_3head` 作为 K=1 基线？我建议是，避免 K=3 只是因为多 head/参数。
5. 是否把 `all_positions_lm_control` 放入首轮？我建议不放，除非你希望第一轮就更接近真实 LM；代价是解释会更复杂。
