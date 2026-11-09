# 会议简报：K=2 长时距分支任务中的 next-two 目标压力

## 0. 执行摘要

**研究问题：** 在一个最小长时距分支分布中，多词元预测是否比下一词元预测更直接要求同一个前缀隐藏状态 $h_T$ 保留早期分支信息？

**机制解释：** 当第一个未来 token $Y_1=A$ 对所有分支相同、第二个未来 token $Y_2=S_B$ 由早期分支 $B$ 决定时，next-two 的 second-token loss 直接作用在同一个 $h_T$ 上，而 next-one at $T$ 不提供这个分支相关监督。

**主要结果：** clean K=2 实验证实了最小机制：fixed-next-one 学会 shared token 但保持 branch-blind，next-two 让 $h_T$ 可预测 branch-specific suffix；该结果不支持 MTP 在所有语言任务上优于 NTP。

**证据说明：** 主要指标是“从同一个 $h_T$ 直接预测 $S_B$ 的准确率”；fixed-next-one 为 0.000，next-two 为 1.000，并且 probe 和 branch-swap 两个 guard 同时通过。

1. fixed-next-one 在三组 seed 中都能预测 shared token $A$，但 $h_T$ 不区分 branch。
2. next-two 在三组 seed 中都让同一个 $h_T$ 成功预测 $S_B$，并通过 frozen probe 和 branch-swap guard。
3. 该实验支持 K=2 objective-level separation 的可运行实现，但仍不支持 curriculum 或自然语言迁移结论。

**结论边界：** 当前证据只覆盖 deterministic、symmetry-controlled、direct-head K=2 设置，不证明真实 LLM 的长程推理收益。

**执行动作：** 下一步建立最小 K>2 branch-controlled suffix anchor/protocol，判定多个未来 token 共享同一早期原因时是否保持同样压力。

## 1. 术语解释

| 术语 | 中文含义 | 具体对象或计算方式 | 单位或公式 | 为什么影响当前判断 | 不能证明什么 |
|---|---|---|---|---|---|
| 长时距依赖 | 早期信息只在较远未来才决定目标 | $B$ 决定 $Y_2=S_B$，中间隔着 filler 和 shared context | 条件关系 | 对应“第一章影响最后一章”的最小形式 | 全部自然语言长程任务 |
| 多词元预测（MTP） | 一个前缀状态预测多个未来 token | 当前为 $h_T$ 同时预测 $Y_1,Y_2$ | 训练目标类型 | 对应导师问题中的 multi-token prediction | 普遍优于下一词元预测 |
| 下一词元预测（NTP） | 一个前缀状态只预测下一个 token | 当前为 $h_T$ 只预测 $Y_1$ | 训练目标类型 | 当前对照目标 | 不能学习长时距依赖 |
| fixed-next-one | 架构有两个 direct heads，但只训练第一个未来 token | active loss 为 $\operatorname{CE}(q_1(\cdot\mid h_T),A)$ | loss condition | 控制“多了 head 或容量”的解释 | 全部 NTP 行为 |
| next-two | 同一个 $h_T$ 同时预测 $Y_1$ 和 $Y_2$ | active loss 为 $\operatorname{CE}(q_1,A)+\operatorname{CE}(q_2,S_B)$ | loss condition | 测试 second-token supervision | 优化必然成功 |
| branch-blind | $h_T$ 不区分早期分支 | branch hidden states 距离为 0，probe 为 chance | 判定条件 | 理论 lower bound 的对象 | 整个模型完全不知道 branch |
| offset2 single-prefix accuracy | 从同一个 $h_T$ 直接预测 $S_B$ 的准确率 | $q_2(\cdot\mid h_T)$ 的 top-1 accuracy | 0 到 1 | 当前主要指标 | 自然语言推理能力 |
| frozen probe accuracy | 冻结模型后从 $h_T$ 线性读出 branch 的准确率 | linear probe $h_T\to B$ | 0 到 1 | 检查成功是否写入表示 | native head 本身可用 |
| branch-swap consistency | 只换 early branch token 后预测是否切换到新 suffix | `BR_b -> BR_c` 后应预测 $S_c$ | 0 到 1 | 检查预测是否因果依赖早期 branch | 排除所有记忆捷径 |

## 2. 机制解释与建模

**核心模型：**

$$
X=(\operatorname{BR}_B,F_1,\ldots,F_L,U,A,S_B),\qquad Y_1=A,\qquad Y_2=S_B.
$$

$$
L_1(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),A),
$$

$$
L_2(h_T)=\operatorname{CE}(q_1(\cdot\mid h_T),A)+\lambda\operatorname{CE}(q_2(\cdot\mid h_T),S_B).
$$

**符号含义：**

- $B$：早期分支变量。
- $S_B$：由分支 $B$ 决定的第二个未来 token。
- $h_T$：停在 shared context 后、预测 $A$ 之前的前缀隐藏状态。
- $q_1,q_2$：分别从同一个 $h_T$ 预测 offset 1 和 offset 2 的 direct heads。

**机制链条：**

1. 因为 $Y_1=A$ 对所有 branch 相同，next-one at $T$ 可以用 branch-blind $h_T$ 最小化 loss。
2. 因为 $Y_2=S_B$ 一一对应 branch，branch-blind $h_T$ 的 second-token 最优 cross-entropy 仍是 $\log m$。
3. 因此 next-two 的 second-token term 会排除 branch-blind $h_T$，实验应表现为 offset2 accuracy、probe、branch-swap 同时提升。

**当前问题分解：**

- 需要判定的模型项：$\operatorname{CE}(q_2(\cdot\mid h_T),S_B)$ 是否让 $h_T$ 暴露 branch。
- 最危险的替代解释：success 只是 offset-2 head artifact，或 local context 泄露 branch。
- 当前实验只能区分：clean K=2 objective pressure；不能区分自然语言迁移或 curriculum 是否更好。

## 3. 主要结果

**一句话总结：** 在 clean K=2 分支任务中，next-two 让同一个 $h_T$ 可预测 branch-specific $S_B$，而 fixed-next-one 学会 shared $A$ 后仍保持 branch-blind。

### 结果 1：fixed-next-one 学会 shared next token，但 $h_T$ 保持 branch-blind。

**机制对应：** 对应第 2 节中 $Y_1=A$ 不含 branch 信息这一环。

**指标或条件定义：** fixed-next-one 只训练 $\operatorname{CE}(q_1,A)$；offset-1 accuracy 测 $A$ 是否学会；offset-2 accuracy、probe、branch-swap 测 $h_T$ 是否含 branch。

**证据：** 三组 seed 中，fixed-next-one 的 offset-1 accuracy 为 1.000；offset-2 single-prefix accuracy 为 0.000；frozen probe 为 0.333；branch-swap consistency 为 0.000；hidden pairwise distance 为 0。

**解释：** 该结果说明 fixed-next-one 的目标足以解决 shared token，但没有把 branch 信息写进 $h_T$。

**边界：** 该结果依赖 identical branch-token initialization；随机初始化下 fixed-next-one 可能有 identity leakage。

**来源：** `summary.md`；`detailed.md`；`tables/condition_summary.csv`。

### 结果 2：next-two 让同一个 $h_T$ 成功支持 branch-specific second-token prediction。

**机制对应：** 对应第 2 节中 $\operatorname{CE}(q_2,S_B)$ 直接作用在 $h_T$ 的机制环节。

**指标或条件定义：** next-two 训练 $\operatorname{CE}(q_1,A)+\operatorname{CE}(q_2,S_B)$；primary metric 是 offset2 single-prefix accuracy。

**证据：** 三组 seed 中，next-two 的 offset-1 accuracy、offset-2 single-prefix accuracy、frozen probe accuracy、branch-swap consistency 均为 1.000；worst-branch offset-2 probability 均值为 0.99999。

**解释：** 该结果说明 second-token supervision 不只是训练了一个 head；它使 $h_T$ 中的 branch 信息可线性读出，并且 suffix prediction 会随 early branch token 切换。

**边界：** 该证据仍是 direct-head、K=2、deterministic 数据，不证明更复杂 suffix 或自然语言。

**来源：** `summary.md`；`detailed.md`；`tables/per_seed_metrics.csv`；`tables/branch_swap.csv`。

### 结果 3：当前证据关闭了 K=2 最小机制，但下一步必须转向 K>2 而不是直接讨论 curriculum。

**机制对应：** 导师的 next-K 问题要求多个未来 token 共同携带早期原因；K=2 只验证最小 second-token case。

**指标或条件定义：** 当前 K=2 指标只问 $h_T\to S_B$；K>2 应扩展到 $h_T\to S_{B,1:k}$ 或多个 branch-specific suffix tokens。

**证据：** A11_01 已通过最小 K=2 pass/fail gate，但没有测试多个 future offsets 的 signal accumulation、gradient alignment 或 noisy filler。

**解释：** 因此下一步应先做 K>2 branch-controlled suffix，再讨论 SNR、curriculum、latent decoder 或真实语言。

**边界：** K>2 规划是下一步研究判断，不是当前实验证据。

**来源：** anchor；`long_horizon_next_k_theory_design.md`；`summary.md`。

## 4. 执行动作

**下一步动作：** 写一个最小 K>2 branch-controlled suffix anchor/protocol。

**目的：** 检验多个未来 token 共享同一早期 branch cause 时，next-k 是否继续让同一个 $h_T$ 暴露 branch，并开始对应导师 next-K token prediction 的更一般问题。

**完成判据：** 新 protocol 必须定义 suffix 长度、branch-specific token set、primary metric、probe/swap guard、pass/fail/insufficient 标准，并明确仍不能 claim curriculum 或自然语言迁移。

## 5. 证据索引

| 结果 | 证据 | 主要指标或图 | 支持什么 | 不能证明什么 | 来源 |
|---|---|---|---|---|---|
| 结果 1 | fixed-next-one 三 seed 表现 | offset1 1.000；offset2 0.000；probe 0.333；swap 0.000 | shared next token 不迫使 $h_T$ 暴露 branch | 全部 NTP 行为 | `tables/condition_summary.csv` |
| 结果 2 | next-two 三 seed 表现 | offset2/probe/swap 均 1.000 | second-token loss 让 $h_T$ 支持 $S_B$ | 自然语言迁移 | `tables/per_seed_metrics.csv` |
| 结果 3 | 当前 anchor next decision | 无图；机制边界判断 | K=2 关闭后应转 K>2 | curriculum 已成立 | anchor / summary |

## 6. 来源索引

**Anchor：** `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_01_k2_branch_delayed_next_two_anchor.md`

**Protocol：** `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/protocol.md`

**Summary：** `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/summary.md`

**Detailed：** `Projects/from-attention-to-search/main/experiments/A11/A11_01_k2_branch_delayed_next_two/detailed.md`

**Figures：** none. The main evidence is tabular and does not require a central figure.

## 7. 补充材料

运行环境：当前远程容器可见 2 张 H100。已创建 4-GPU ACP dry-run submitter，但最终实验直接在当前容器完成；job id 为 none。

初始 1200-step run 中，next-two 在 seed `972` 只达到 2/3 branch 分离；延长到 4000 steps 后三组 seed 全部通过。因此该中间结果被解释为收敛不足，不作为机制失败。
