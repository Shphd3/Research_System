# 待审计 Protocol：A11_03 K=2 Semantic Efficiency Curves

## 0. 审批快照

Approval status: approved by user request on 2026-07-07; implementation and run requested.

Purpose: 检验 K=2 中 next-two 是否不仅有“表示必要性”，而且比 matched fixed-next-one 更早、更稳定地让 $h_T$ 含有早期分支变量 $Z$。

Primary anchor: `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_03_k2_semantic_efficiency_anchor.md`

Anchor decision question: 在受控 K=2 branch-delayed 任务中，next-two 是否比 matched fixed-next-one 更早让 $Z$ 可从 $h_T$ 恢复，同时不损害 $Y_1$ 学习？

Anchor physical prior tested: 当 $Y_1=A$ 共享而 $Y_2=S_Z$ 分支相关时，next-two 在同一个 $h_T$ 上获得直接分支监督；fixed next-one 没有这个监督。

Anchor core model term tested: $L_{\mathrm{next2}}=L_1+\lambda L_2$ 中的 $\lambda L_2=\lambda\operatorname{CE}(q_2(\cdot\mid h_T),S_Z)$ 是否提高 $h_T$ 中 $Z$ 的学习速度。

Anchor falsifier: 如果 next-two 在 `T_0.9_eval` 或早期 `AUC_Q` 上不优于 fixed next-one，则 K=2 efficiency claim 不成立；K=2 objective-level theorem 仍然成立。

Experiment role: metric audit + efficiency test.

Primary metric from anchor: `T_0.9_eval`，即 guarded evaluation score $Q_{\mathrm{eval}}(t)$ 连续若干 checkpoint 达到 0.9 的最早 step。

Claim boundary from anchor: 本实验只能判断受控 K=2 构造中的学习效率；不能证明 MTP 普遍优于 NTP，不能证明自然语言迁移，不能证明 K>2。

Minimal setup: 第一版只跑 `decision_only`。损失只在 prediction site 上计算，直接对应理论对象 $h_T\to(Y_1,Y_2)$。

Basic configuration: `num_branches=4`, `filler_length=16`, `shared_context_length=4`, one-layer one-head Transformer, `d_model=64`, $\lambda_2=1.0$, seeds `971-975`, checkpoints every fixed interval, training budget initially `10000` steps.

Conditions to run:

1. `fixed_next_one_2head`: architecture has future heads, but only $L_1$ is active.
2. `shared_trunk_next_two`: same shared trunk, active loss $L_1+\lambda_2L_2$.
3. Clean regime: $Y_1=A$, $Y_2=S_Z$.
4. Noisy guard: $Y_1=A$, $Y_2=Z_{\mathrm{noise}}$, independent of branch.
5. Redundant guard: $Y_1=S_Z$, $Y_2=T_Z=R(S_Z)$, used only to guard the interpretation.

Pass: next-two has smaller `T_0.9_eval` and larger early `AUC_Q` than fixed next-one in clean regime; $Y_1$ local guard passes; noisy guard does not pass head-2 / branch-swap guards.

Fail: fixed next-one matches or beats next-two on `T_0.9_eval` / `AUC_Q`; or next-two only wins by degrading $Y_1$; or noisy guard behaves like clean branch-specific target.

Insufficient: both conditions fail to reach threshold, curves are too noisy, or matched evaluation decoder/probe is unstable.

Cannot claim: MTP generally improves learning efficiency; all-position LM behavior; real language; K>2.

Approval decision: run.

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 单位或公式 | 为什么影响判断 | 不能证明什么 |
|---|---|---|---|---|---|
| fixed next-one | 只用 immediate next-token loss 训练的容量匹配基线 | 有同样 trunk / head 容量，但 active loss 只有 $L_1$ | condition | 排除“只是多了 head/参数”的解释 | 所有 NTP 行为 |
| next-two | 同一个 $h_T$ 预测 $Y_1,Y_2$ | active loss $L_1+\lambda_2L_2$ | condition | 主干 MTP 条件 | 普遍优越性 |
| matched evaluation decoder | 所有条件共用的评估读出器 | 在冻结 $h_T$ 上训练小读出器预测 $S_Z$，再在 held-out split 上评估 | accuracy / CE | 让 fixed next-one 和 next-two 可公平比较 | native head 是否使用该信息 |
| native head-2 accuracy | next-two 自己的第二头预测准确率 | $q_2(\cdot\mid h_T)$ top-1 是否为 $S_Z$ | 0 到 1 | 证明 next-two 真的学了它的训练目标 | fixed next-one 的公平比较 |
| guarded score $Q_{\mathrm{eval}}$ | 保守语义恢复分数 | $\min\{A_{\mathrm{eval}},P_{\mathrm{eval}},S_{\mathrm{eval}}\}$ | 0 到 1 | 防止 probe-only 假阳性 | 完整因果机制 |
| `T_0.9_eval` | 达到语义恢复阈值的训练时间 | $Q_{\mathrm{eval}}\ge0.9$ 连续通过的最早 step | steps | 主效率指标 | 最终能力上限 |
| local guard | immediate next-token 是否被损害 | $Y_1$ accuracy / loss | accuracy / CE | 防止牺牲局部学习换长程指标 | 长程机制本身 |

## 2. Anchor 对齐

Decision question: next-two 是否比 fixed next-one 更早让 $Z$ 可从 $h_T$ 恢复？

Physical prior tested: $L_2$ 给 $h_T$ 直接分支监督。

Core model term tested: $\lambda_2\operatorname{CE}(q_2(\cdot\mid h_T),S_Z)$。

Falsifier: next-two 没有更低 `T_0.9_eval` 或更高 early `AUC_Q`。

Claim boundary: 只裁定 K=2 受控构造中的效率，不裁定普遍 MTP。

## 3. 被检验假设

H1: next-two 在 clean regime 中比 fixed next-one 更早达到 guarded recovery。

H2: 这个优势不来自 $Y_1$ 学习被破坏。

H3: 这个优势只在 branch-informative $Y_2$ 中出现，不在 noisy $Y_2$ 中出现。

## 4. 替代解释

1. Extra-capacity explanation: next-two 只是因为多了 head/参数。
2. Leakage explanation: branch token embedding 或数据频率泄漏让 fixed next-one / next-two 非因果地读出 $Z$。
3. Probe-only explanation: probe 可读但 native prediction 或 branch-swap 不成立。
4. Local-tradeoff explanation: next-two 用牺牲 $Y_1$ 学习换取 $Z$ recovery。
5. Noisy-auxiliary explanation: 任意 future loss 都能产生类似效果。

## 5. 数据 / 模型 / 算法 / 目标

Clean data:

```text
BR_z F00 ... F{L-1} U00 ... U{s-1} A_SHARED S_z STOP
```

Prediction prefix stops after shared context:

```text
BR_z F00 ... F{L-1} U00 ... U{s-1}
```

Targets:

$$
Y_1=A,\qquad Y_2=S_Z.
$$

Fixed next-one objective:

$$
L_{\mathrm{fixed1}}=L_1.
$$

Next-two objective:

$$
L_{\mathrm{next2}}=L_1+\lambda_2L_2.
$$

Model: one-layer causal Transformer, shared trunk, direct horizon heads. 第一版不加入 separate-expert，除非你要求把 interference localization 放进首轮。

Evaluation:

1. 每个 checkpoint 冻结模型。
2. 收集 train/eval split 的 $h_T$。
3. 训练 matched evaluation decoder / probe。
4. 计算 $A_{\mathrm{eval}}$, $P_{\mathrm{eval}}$, $S_{\mathrm{eval}}$。
5. 计算 $Q_{\mathrm{eval}}(t)$、`T_0.9_eval`、`AUC_Q`。

## 6. 条件、seeds、checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Evidence | Pass | Fail | Insufficient | Figure/table |
|---|---|---|---|---|---|---|---|---|
| clean fixed next-one | baseline efficiency | no $L_2$ branch supervision | baseline | $Q(t)$, $Y_1$ | lower than next-two | matches next-two | unstable eval | curves/table |
| clean next-two | main mechanism | $L_2=S_Z$ branch supervision | main test | $Q(t)$, native head2, swap | lower `T_0.9_eval` | no gain | no threshold | curves/table |
| noisy next-two | noisy auxiliary guard | $Y_2\perp Z$ | false-positive guard | head2 near chance, $Q$ low | remains low | behaves like clean | noisy variance high | guard table |
| redundant next-two | redundancy guard | $Y_2=R(Y_1)$ | separates new branch information from local continuation | explained by $Y_1$ | no new claim | unexplained gain | ambiguous | guard table |

Seeds: `971,972,973,974,975`.

Checkpoints: enough to estimate `T_0.9_eval`; recommended every `250` or `500` steps.

## 7. Primary Metric

Primary metric:

$$
T_{0.9}^{\mathrm{eval}}=\inf\{t:Q_{\mathrm{eval}}(t)\ge0.9\text{ for consecutive evaluations}\}.
$$

Why it decides: anchor 的问题是“是否更早学到 $Z$”，不是“最终是否能学到”。因此 time-to-threshold 比 final accuracy 更直接。

False positive cost: 如果 decoder/probe 太强或数据泄漏，fixed next-one 和 next-two 都可能高分。用 noisy/redundant controls 和 branch-swap guard 降低风险。

False negative cost: 如果任务太难或训练不足，二者都达不到阈值。此时不能否定理论，只能说效率实验 insufficient。

## 8. Secondary Metrics

- `AUC_Q_early`: 早期 $Q_{\mathrm{eval}}$ 曲线面积。
- `final_Q`: 最终 guarded score。
- `native_head2_accuracy`: next-two native target 是否学会。
- `branch_swap_consistency`: 是否随 branch token causally 切换。
- `Y1_accuracy`, `Y1_loss`: local guard。
- optional gradient usefulness $U_2$: $L_2$ 是否沿降低 branch-recovery loss 的方向。

## 9. Known Good / Known Bad / Known Confusing Cases

Known good: A11_01 next-two final offset-2 / probe / swap 全部为 1.0。

Known bad: A11_01 fixed next-one 在 identical branch init 下保持 branch-blind。

Known confusing: A11_02 中 C-noisy 可以有较高 probe，但 head-2 仍 near chance；因此 probe 不能单独裁定。

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
|---|---|---|---|---|---|
| data audit | clean/noisy/redundant 是否按定义生成 | sample table | no leakage / leakage | sample table | detailed |
| training smoke | loss 是否下降、checkpoint 是否产生 | small run logs | no crash / crash | smoke logs | not central |
| eval decoder audit | matched decoder 是否稳定 | train/eval split metrics | eval stable / overfit | decoder table | detailed |
| main curve | next-two 是否更早过阈值 | $Q(t)$ curves | pass/fail/insufficient | main figure | summary |
| guard audit | $Y_1$ 和 noisy guard 是否通过 | local/noisy metrics | pass/fail | guard table | summary |

## 11. 算法说明

input: trained checkpoints, train/eval split sequences, branch-swap prefixes.

parameters: threshold `0.9`, consecutive evaluations `3` unless你审核后改动。

intermediate variables: $h_T$, eval decoder logits, branch probe logits, swap logits.

steps:

1. For each condition/seed/checkpoint, collect frozen $h_T$.
2. Fit evaluation decoder/probe on train split only.
3. Evaluate on held-out split.
4. Compute $Q_{\mathrm{eval}}(t)$.
5. Aggregate `T_0.9_eval`, `AUC_Q`, final metrics across seeds.

outputs: main curves, compact result table, guard table, artifact map.

failure reasons: leakage, decoder overfit, no threshold, local-loss tradeoff, noisy guard false positive.

## 12. Success / Failure / Insufficient Evidence

Success: next-two beats fixed next-one on `T_0.9_eval` and early `AUC_Q`, local guard passes, noisy guard stays negative.

Failure: fixed next-one matches or beats next-two, or next-two only wins by local degradation, or noisy guard also passes.

Insufficient: neither reaches threshold, evaluation decoder is unstable, or data audit finds unresolved leakage.

## 13. What This Cannot Claim

- MTP universally improves NTP.
- NTP cannot encode long-horizon variables.
- K>2 follows automatically.
- Natural-language transfer.
- Shared-gradient conflict is harmless in all settings.

## 14. Review Notes And Protocol Changes

需要你审核的点：

1. 第一版是否只跑 `decision_only`？我建议是。`all_positions_lm_control` 更真实，但会把效率问题和背景 LM loss 混在一起。
2. 是否使用 `identical_branch` 作为主 init？我建议主结果用 identical，random 只作为后续 robustness。
3. 是否把 `filler_length=16` 固定为第一版？我建议先对齐 A11_02；若太容易再做 32/64。
4. `fixed_next_one_2head` 是否作为唯一基线？我建议是；true one-head NTP 可以作为 appendix，不做主比较。
5. 是否把 separate-expert 放入首轮？我建议不放，除非主问题转为 interference localization。
