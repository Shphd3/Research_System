# Phase6 实验执行 Prompt：定义并检验 LM-relevant Specialization 与 Middle Tail

## 0. 为什么这是 **Phase6**，而不是继续记作 Phase5

建议把接下来的工作正式记为 **Phase6**。

原因不是形式上的，而是研究问题已经切换了：

- **Phase5** 已经完成的任务是：
  - `C2 / C2.5 / C2.6`：把真实单层 block 的收益来源拆开，区分 `split`、`capacity`、`router input`、`expert input`
  - `D1`：在 oracle synthetic small-model 中测试 recursive hierarchy 是否有潜力

- **Phase6** 要回答的则是两个新问题：
  1. 当前单层 `hier_moe_tail_uniform` 的收益，是否已经构成 **LM-relevant specialization**
  2. 如果要继续往 hierarchical / recursive 方向推进，**Middle Tail** 是否才是更值得学的对象，而不是盲目继续切 extreme tail

因此，Phase6 不是 Phase5 的一个普通补实验，而是：
> 从“单层结构是否赢”转向“为什么赢 / 赢的东西到底是什么 / 下一层分解该不该做”的新阶段。

---

## 1. 当前研究位置（给执行 Agent 的背景）

### 1.1 当前最稳的已知事实

1. 真实 hidden state 中存在 shared head，Phase1 已经把这件事建立起来。
2. `tail_residual` 的几何比 `raw` 更适合 domain 读出，但这只是几何前提，不自动等于 LM 收益。
3. 真实单层 `combined tail-conditioned routed block` 已经有主任务正结果：
   - 在 `Qwen3-0.6B` 单层 block replacement 上，`hier_moe_tail_uniform` 优于 `baseline_ffn` 和 `flat_moe_raw_uniform`
4. `Phase5-C2` 说明：
   - 当前收益不只是 `split`
   - 也不只是多 expert 容量
5. `Phase5-C2.5` 进一步说明：
   - 在 routed family 里，**最稳定的单因素增益更像是 expert 看 `x_t`**
   - `router-only: x -> x_t` 目前仍然很弱
6. `Phase5-C2.6` 说明：
   - 在 non-routing matched-budget family 里，`split-alone` 还没有完全排除 matched-budget wide dense 解释
   - 但在 two-branch family 内部，给第二分支喂 `x_t` 是必要的
7. `Phase5-D1` 说明：
   - recursive hierarchy 的 **oracle upper bound 很强**
   - 但 **learned recursive hierarchy 还没有成立**

### 1.2 当前不能过度宣称的内容

执行中必须避免把以下内容写成已经成立：

1. `estimated projector` 已经稳定替代 oracle split
2. `router-only` 改成看 `x_t` 已经稳定成立
3. `WD-only` 是当前真实收益的主要来源
4. 更高的 purity / NMI 就等于更好的 LM 主任务收益
5. recursive learned hierarchy 已经成立

### 1.3 当前最需要被回答的问题

接下来最关键的不是继续堆更复杂的 hierarchical 结构，而是先回答：

> **当前的 experts 到底有没有 LM-relevant specialization？**

以及：

> **如果要继续往层次化方向走，我们究竟应该细分什么：Middle Tail，还是 extreme tail？**

---

## 2. Phase6 的总目标

Phase6 的目标不是再次证明单层 hier 比 flat 好，而是：

1. 给出一个 **最小可操作的 specialization 判断**
2. 判断当前 `hier_moe_tail_uniform` 的收益究竟来自：
   - 专家真的被正确选中
   - 还是只是 expert 看 `x_t` 带来的结构修正
3. 判断“Middle Tail”是否比 head / extreme tail 更值得由 expert 学习
4. 用这些结果决定：
   - 后续应继续推进 single-layer specialization
   - 还是再上 recursive hierarchy
   - 还是先收缩为 split-first factorized FFN 主线

---

# Phase6-A：反事实 Expert Gap 审计（首要实验）

## A0. 实验目的

回答：

> 当前 `hier_moe_tail_uniform` 中，被 router 选中的 expert，是否真的比其他 expert 更适合当前 token？

这一步的目标不是看 domain purity，而是定义和检验 **LM-relevant specialization**。

---

## A1. 要区分的 competing hypotheses

### H-A1：真实 specialization 成立
对当前 token，真实选中的 expert 的 next-token NLL 低于替代 expert。

### H-A2：收益主要来自 expert 输入是 `x_t`
不管选哪个 expert，只要 expert 都看 `x_t`，差异就很小；真正的好处来自 block factorization，而不是 expert selection。

### H-A3：收益主要来自软集成 / 容量
真实选中 expert 与均匀 expert 平均、第二高分 expert 的差异很小。

---

## A2. 数学对象

设当前 token 的上下文为 `c`，真实路由 expert 为

$$
e^\star = r(c).
$$

真实 expert 的损失：

$$
\ell^\star = \ell\big(y, f_{e^\star}(c)\big)
$$

对任意替代 expert `e'`，定义反事实 gap：

$$
G_{\mathrm{cf}}(e')
=\mathbb{E}\left[
\ell\big(y, f_{e'}(c)\big)
-
\ell\big(y, f_{e^\star}(c)\big)
\right].
$$

如果

$$
G_{\mathrm{cf}}(e') > 0
$$

并且这种优势稳定出现在某些 token bucket 上，那么才可以说：
> 被选中的 expert 具有功能性 specialization。

### 推荐替代 expert

1. `second_best`
2. `random_expert`
3. `uniform_average_expert`
4. `best_other_expert`（如实现方便）

---

## A3. 实验对象

优先使用已有 checkpoint，不先重训：

### 必测 checkpoint
1. `hier_moe_tail_uniform`
2. `router_raw_expert_tail_uniform`
3. `flat_moe_raw_uniform`

### 可选附加
4. `uniform_expert_mixture_tail`

---

## A4. 具体执行步骤

1. 加载已有 Phase5-C2.5 checkpoint
2. 在验证集上逐 token 跑 forward
3. 对每个 token 记录：
   - 真实路由 expert
   - top-2 router scores
   - 每个 expert 单独前向时的 token NLL
   - 均匀 expert 平均的 token NLL
4. 分桶统计：
   - all tokens
   - WoS rare tokens
   - middle-frequency tokens
   - common/high-frequency tokens
   - 若可行，再加 domain buckets
5. 计算：
   - `G_cf(second_best)`
   - `G_cf(random)`
   - `G_cf(uniform_avg)`
6. 额外统计：
   - route margin（top1-top2）
   - margin 与 `G_cf` 的相关性
   - expert-wise token count
   - expert-wise rare-token NLL

---

## A5. 关键指标

### 主指标
1. `counterfactual_gap_second_best`
2. `counterfactual_gap_random`
3. `counterfactual_gap_uniform_avg`

### 辅助指标
1. `gap_by_frequency_bucket`
2. `gap_by_domain_bucket`
3. `route_margin`
4. `route_margin_vs_gap_corr`

---

## A6. 预期结果与如何更新主线

### 结果 A
如果：

- `G_cf > 0` 明显成立
- 且在 rare / middle-tail bucket 上尤其明显

则更新为：
> 当前单层 hier 不只是 factorization gain，而是已经出现 **LM-relevant specialization**。

下一步：
- 可以继续研究更细的 specialization 结构
- 也可以更有底气讨论 Middle Tail / recursive hierarchy

### 结果 B
如果：

- `G_cf ≈ 0`
- 但 `hier_moe_tail_uniform` 主指标仍优于 flat/baseline

则更新为：
> 当前收益主要来自 **expert-tail input + block factorization**，而不是 expert selection 本身。

下一步：
- 暂时弱化“specialized experts”叙事
- 先把主线写成 split-first factorized block

### 结果 C
如果：
- `router_raw_expert_tail_uniform` 与 `hier_moe_tail_uniform` 的 `G_cf` 都很弱
- 但二者主指标都好于 flat

则更新为：
> 当前最稳收益来自 `expert input: x -> x_t`，不是 router 选择。

---

# Phase6-B：Middle Tail 频带干预实验（第二关键实验）

## B0. 实验目的

回答：

> 如果 experts 不该去盲目学习 head 或 extreme tail，那么“Middle Tail”是否真的是更值得学习的对象？

这一步直接检验导师的 Middle Tail 观点是否成立。

---

## B1. 要区分的 competing hypotheses

### H-B1：Middle Tail 最值得学
把 expert 输入限制在 middle-tail band 上，rare/middle-token PPL 最优，或最接近最优。

### H-B2：Extreme tail 最值得学
越接近残差尾部越好，middle-tail 并不特殊。

### H-B3：Head 仍然最重要
专家看 head 或 raw 就已经最好。

### H-B4：band 不重要，主要是参数量或两分支结构
不同 band 差异很小，matched-budget dense 能追平。

---

## B2. 基本思路

固定当前最稳的 single-layer family，只改变 **expert 输入 band**，不同时大改 router / loss / optimizer。

设 centered hidden 为：

$$
x_c = x - \mu
$$

对协方差做特征分解，记前向基为 `V`。

定义三个 band：

### head band
$$
x_{\mathrm{head}} = V_{1:k_1}V_{1:k_1}^\top x_c
$$

### middle-tail band
$$
x_{\mathrm{middle}} = V_{k_1+1:k_2}V_{k_1+1:k_2}^\top x_c
$$

### extreme-tail band
$$
x_{\mathrm{extreme}} = \left(I - V_{1:k_2}V_{1:k_2}^\top\right)x_c
$$

另外保留完整 tail residual：

$$
x_t = \left(I - V_{1:k_t}V_{1:k_t}^\top\right)x_c
$$

---

## B3. 推荐 band 划分

以当前 `Qwen3-0.6B layer=8` 为主 setting，先用一个小 sweep：

### 推荐主设定
- `k1 = 8`
- `k2 = 32`
- `k_t = 16`

### 可选附加设定
- `(k1, k2) = (8, 16)`
- `(k1, k2) = (16, 32)`
- `(k1, k2) = (16, 64)`

如果资源有限，先只跑主设定。

---

## B4. 对照组

### G0
`baseline_ffn`

### G1
`router_raw_expert_raw_uniform`

### G2
`router_raw_expert_head_uniform`

### G3
`router_raw_expert_middle_uniform`

### G4
`router_raw_expert_extreme_uniform`

### G5
`router_raw_expert_tail_uniform`

> 注：优先固定 router 为 raw router，只改变 expert input。  
> 原因：Phase5-C2.5 已经显示 expert input 是更稳定的单因素，Phase6-B 先不要把 router 变量再混进来。

---

## B5. 具体执行步骤

1. 沿用当前真实单层 replacement setting：
   - model = `Qwen3-0.6B`
   - layer = `8`
   - projector 统计方式沿用当前 Phase5
   - frozen backbone，只训替换块
2. 构造不同 expert input band
3. 保持 expert 数、宽度、总参数预算尽量一致
4. 每组至少 2 个 seed，推荐 3 个 seed
5. 训练后报告：
   - DCLM PPL
   - WoS PPL
   - WoS rare-token PPL
   - middle-frequency token PPL
   - optional: counterfactual expert gap

---

## B6. 关键指标

### 主指标
1. `WoS_rare_token_PPL`
2. `middle_frequency_token_PPL`
3. `DCLM_PPL`

### 诊断指标
1. `counterfactual_gap_uniform_avg`
2. `expert_wise_token_count`
3. `expert_wise_rare_token_nll`
4. `band_energy_fraction`

---

## B7. 预期结果与如何更新主线

### 结果 A
如果 `middle` 最好或接近 `tail` 最好，且优于 `head` 与 `extreme`：

更新为：
> Middle Tail 不是口号，而是当前最可用的 expert 学习对象。

下一步：
- 优先围绕 Middle Tail 设计 projector / local conditional common
- recursive hierarchy 只在 middle-tail 内部继续做

### 结果 B
如果 `extreme` 最好：

更新为：
> 当前“extreme tail 可能只是噪声”的判断过强，需要重新评估。

下一步：
- recursive tail 细分仍值得继续
- 但必须小心样本支持与优化稳定性

### 结果 C
如果 `head` 或 `raw` 最好：

更新为：
> 当前 split-first 主线还没真正抓到“可学习的结构频带”，Middle Tail 叙事应暂缓。

### 结果 D
如果 `tail residual` 最好，但 `middle` / `extreme` 单独都不够：

更新为：
> 有用信息不在单一 band，而在 tail residual 的组合中。  
> 后续应该学 projector / learned band，而不是手工固定 band。

---

# 3. 执行顺序与优先级

## 优先级 1：Phase6-A
先做反事实 Expert Gap 审计。

原因：
- 它直接回答“现在到底有没有 specialization”
- 它大概率可以先基于已有 checkpoint 做，不必先重训
- 它是后续是否继续讲 recursive / Middle Tail 的前提

## 优先级 2：Phase6-B
只有在 A 给出结果后，再做 band intervention。

原因：
- A 先回答“当前专家有没有功能性”
- B 再回答“如果有，应该学哪一段信息”

---

# 4. 执行约束

1. **不要重新把 WD/LR 作为主主线。**
2. **不要把 purity / NMI 当成主结论，只保留为诊断。**
3. **不要在 Phase6 里直接上 recursive real-model。**
   - recursive hierarchy 只有 oracle upper bound 很强
   - learned recursive 还没有成立
4. **所有结论优先看 LM-relevant 指标：**
   - token NLL
   - rare-token PPL
   - counterfactual expert gap

---

# 5. 输出物要求

## Phase6-A 输出物
1. `phase6A_counterfactual_gap_report.md`
2. `counterfactual_gap_by_bucket.csv`
3. `expert_wise_nll.csv`
4. `route_margin_vs_gap.csv`
5. 可选图：
   - gap histogram
   - gap by bucket
   - margin-gap scatter

## Phase6-B 输出物
1. `phase6B_middle_tail_band_report.md`
2. `band_intervention_summary.csv`
3. `band_energy_fraction.csv`
4. 可选图：
   - rare-token PPL by band
   - middle-frequency PPL by band
   - DCLM PPL by band

---

# 6. 最后一句执行口径

Phase6 的核心不是继续证明“hier 比 flat 好”，而是：

> **把“当前为什么好”讲清楚，并判断专家真正应该学的是哪一段信息。**

如果只能记一句话，请记：

> 先用反事实 expert gap 定义并检验 specialization，再用频带干预判断 Middle Tail 是否真是下一阶段应该押注的对象。
