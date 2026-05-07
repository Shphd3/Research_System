# EXP Summary

## 1. 主线确认

我们当前的研究主线是：

1. 先把 common / tail 分开，再做 routing，是否优于直接对原表征路由。
2. 即使不做 routing，只把 common branch 和 tail branch 分开，是否已经能改善 long-tail 学习。
3. 如果 tail 内部还有 coarse/fine 结构，再继续分层是否值得。

这条主线目前最稳的推进顺序是：

$$
\text{shared head} \rightarrow \text{split-first block} \rightarrow \text{single-layer tail-conditioned routing} \rightarrow \text{LM-relevant specialization}
$$

对于 recursive 结构，目前当前最稳的诊断是：

$$
\text{在粗粒度上的路由问题是导致问题失败的主要原因}
$$

---

## 2. 最重要的假设确认

- `H1 [Shared-Head Hypothesis]`

  真实 hidden 中存在 shared high-variance head；去掉它后得到的 tail residual 比 raw hidden 在表征空间上更加分得开：

  $$
  x_t = P_t(x-\mu), \qquad P_t = I - V_k V_k^\top
  $$

  当前状态：**强支持**。

- `H2 [Single-Layer Split-First Hypothesis]`

  在单层 block 替换的训练设置下，split-first 的 common/tail factorization 优于 flat raw MoE；进一步地，收益更像来自 tail-side expert 处理 $x_t$，而不是 router-only 改看 $x_t$。当前 `router-only` 在 `with-LB` 下作用较弱，在 `no-LB` 下会出现更强的功能性 gap，但还不能把它写成已经稳定闭环。

  当前更稳的单因素增益来源是：

  $$
  E_i(x) \rightarrow E_i(x_t)
  $$

  当前状态：**主干成立，但归因边界要保守**。

- `H3 [Recursive-Tail Hypothesis]`

  如果 tail 内部仍有 coarse/fine hierarchy，则 recursive factorization / routing 还有潜力进一步改善更细粒度的 rare tail。

  当前状态：**结构上有潜力（因为在toy model上验证，上限很高），但 learned recursive 仍未成立；主要的瓶颈在 coarse routing**。

---

## 3. 核心模型家族

令

$$
x_t = P_t(x-\mu), \qquad P_t = I - V_k V_k^\top
$$

其中 $x_t$ 是去均值并去掉 shared head 后的 `tail residual`。

| 配置 | 数学形式 | router 看什么 | expert 看什么 | 它在控制什么 |
| --- | --- | --- | --- | --- |
| `baseline_ffn` | $h_{\text{out}} = h_{\text{in}} + E(x)$ | 无 | full $x$ | 普通单层 FFN 基线 |
| `flat_moe_raw_uniform` | $h_{\text{out}} = h_{\text{in}} + E_c(x) + \sum_i g_i(x)E_i(x)$ | raw $x$ | raw $x$ | flat raw MoE |
| `split_dense_tail_uniform` | $h_{\text{out}} = h_{\text{in}} + E_c(x) + E_t(x_t)$ | 无 | tail $x_t$ | dense two-branch split |
| `uniform_expert_mixture_tail` | $h_{\text{out}} = h_{\text{in}} + E_c(x) + \frac1N\sum_i E_i(x_t)$ | 无 | tail $x_t$ | 只加 expert 容量，不做 routing |
| `router_tail_expert_raw_uniform` | $h_{\text{out}} = h_{\text{in}} + E_c(x) + \sum_i g_i(x_t)E_i(x)$ | tail $x_t$ | raw $x$ | 只改 router 输入 |
| `router_raw_expert_tail_uniform` | $h_{\text{out}} = h_{\text{in}} + E_c(x) + \sum_i g_i(x)E_i(x_t)$ | raw $x$ | tail $x_t$ | 只改 expert 输入 |
| `hier_moe_tail_uniform` | $h_{\text{out}} = h_{\text{in}} + E_c(x) + \sum_i g_i(x_t)E_i(x_t)$ | tail $x_t$ | tail $x_t$ | full split-first 单层 hier |

---

## 4. 最重要的实验

说明：本摘要只保留最关键的数量口径，便于定位问题。优先记录：

- 数据混合比例
- 模型规模
- 层位 / rank
- 训练步数
- 正式 seed 数

### Phase1：真实表征审计

一句话版本：先确认真实 hidden 里是否真的存在 shared head，以及去掉它后得到的 $x_t$ 是否更适合 long-tail 语义区分。

- 目的：验证 `H1`
- 数据：`DCLM + WoS`，协方差池比例 `4:1`
- 数据量：
  - `WoS covariance docs = 448`
  - `WoS train docs = 896`
  - `WoS test docs = 896`
  - `DCLM sequences = 1792`
  - `WoS domains = 7`
- 模型：冻结 `Qwen3-8B`
- 步骤：
  - 位置：`post-attention / pre-FFN`
  - 扫描层：`5 / 11 / 23 / 35`
  - 扫描 rank：`4 / 8 / 16 / 32 / 64`
  - 比较表示：`raw / centered / tail_residual`
  - 指标：`explained variance / probe accuracy / purity / NMI / Sep_trace`
  - 正式 seed：`2`
- 代表结果：
  - `layer 35` 的 top-8 explained variance 约为 `0.4069`
  - seed1：`raw acc 0.7522 -> tail_residual acc 0.7690`
  - seed2：`raw acc 0.7444 -> tail_residual acc 0.7511`
- 当前结论：

  $$
  \text{shared head exists in real hidden states}
  $$

  以及

  $$
  \text{tail residual is more separable than raw / centered}
  $$

- 可信假说更新：**强支持 `H1`**

### Phase4-C1：真实单层 block replacement 第一次正结果

一句话版本：第一次在真实 `Qwen3-0.6B` 单层 block replacement 上证明，hier tail-conditioned block 优于 baseline 和 flat raw MoE。

- 目的：验证单层真实 block 上，hierarchical 结构本体是否已经成立
- 数据：`DCLM + WoS`
- 数据量：
  - `WoS covariance docs = 448`（`64 × 7`）
  - `WoS train docs = 896`（`128 × 7`）
  - `WoS test docs = 896`（`128 × 7`）
  - `DCLM cov/train/eval sequences = 512 / 2048 / 256`
- 模型：`Qwen3-0.6B`
- 设置：
  - `layer = 8`
  - `k = 16`
  - `frozen backbone`
  - 训练步数：`3000`
  - 评估间隔：`250`
  - 数据比例：`DCLM : WoS = 4 : 1`
  - 主指标：`WoS rare-token PPL`
  - 正式 seed：`2`（最终主结果以 `20260418, 20260419` 为主）
- 最重要对比：
  - `baseline_ffn`
  - `flat_moe_raw_uniform`
  - `hier_moe_tail_uniform`
- 代表结果：
  - `baseline_ffn = 84.0007`
  - `flat_moe_raw_uniform = 85.0412`
  - `hier_moe_tail_uniform = 81.5287`
- 当前结论：

  $$
  \text{hier} < \text{baseline\_ffn} < \text{flat}
  $$

  按 `WoS rare-token PPL` 成立。

- 可信假说更新：**强更新 `H2`**

### Phase5-C2.5：router input vs expert input 机制拆解

一句话版本：把 `hier` 的收益拆开以后发现，当前最稳定的单因素增益更像来自 `expert-tail input`，而不是 `router-only`。

- 目的：

  $$
  \text{收益到底来自 } g_i(x) \rightarrow g_i(x_t) \text{，还是 } E_i(x) \rightarrow E_i(x_t) \text{？}
  $$

- 数据：真实 `DCLM + WoS` token-level block replacement
- 数据量：
  - `WoS covariance docs = 448`（`64 × 7`）
  - `WoS train docs = 896`（`128 × 7`）
  - `WoS test docs = 896`（`128 × 7`）
  - `DCLM cov/train/eval sequences = 512 / 2048 / 256`
- 模型：`Qwen3-0.6B`
- 设置：
  - `layer = 8`
  - `k = 16`
  - `frozen backbone`
  - 训练步数：`500`
  - 数据比例：`DCLM : WoS = 4 : 1`
  - 正式 seed：`3`
- 最重要对比：
  - `flat_moe_raw_uniform`: $g_i(x), E_i(x)$
  - `router_tail_expert_raw_uniform`: $g_i(x_t), E_i(x)$
  - `router_raw_expert_tail_uniform`: $g_i(x), E_i(x_t)$
  - `hier_moe_tail_uniform`: $g_i(x_t), E_i(x_t)$
- 代表结果：`WoS rare-token PPL`
  - `flat_moe_raw_uniform = 472.3493`
  - `router_tail_expert_raw_uniform = 471.7282`
  - `router_raw_expert_tail_uniform = 448.6350`
  - `hier_moe_tail_uniform = 447.1932`
- 当前结论：

  $$
  \text{full hier} \approx \text{expert-only} \ll \text{router-only} \approx \text{flat}
  $$

  当前更稳的增益来源是

  $$
  E_i(x) \rightarrow E_i(x_t)
  $$

- 可信假说更新：**强更新 `H2`**

### Phase5-C2.6：split gain 与参数量 gain 的 disentanglement

一句话版本：`split_dense_tail_uniform` 在 matched-budget 下没有明显打赢 `wide dense`，但如果采用 two-branch 结构，让第二分支看 $x_t$ 是必要的。

- 目的：

  $$
  \text{split gain 到底是不是纯参数量造成的？}
  $$

- 数据：真实 `DCLM + WoS`
- 数据量：
  - `WoS covariance docs = 448`（`64 × 7`）
  - `WoS train docs = 896`（`128 × 7`）
  - `WoS test docs = 896`（`128 × 7`）
  - `DCLM cov/train/eval sequences = 512 / 2048 / 256`
- 模型：`Qwen3-0.6B`
- 设置：
  - `layer = 8`
  - `k = 16`
  - `frozen backbone`
  - 训练步数：`500`
  - 数据比例：`DCLM : WoS = 4 : 1`
  - 正式 seed：`3`
- 最重要对比：
  - `baseline_ffn`
  - `baseline_ffn_wide_match_split`
  - `raw_two_branch_uniform`
  - `split_dense_tail_uniform`
- 代表结果：`WoS rare-token PPL`
  - `split_dense_tail_uniform = 465.8115`
  - `baseline_ffn_wide_match_split = 465.9182`
  - `baseline_ffn = 466.1178`
  - `raw_two_branch_uniform = 472.4337`
- 当前结论：

  $$
  \text{split} \approx \text{wide dense} < \text{baseline} \ll \text{raw two-branch}
  $$

  因此当前更稳的说法是：

  $$
  \text{within two-branch family, feeding the second branch with } x_t \text{ is necessary}
  $$

- 可信假说更新：**收紧 `H2` 的 claim 边界**

### Phase6-A：LM-relevant specialization

一句话版本：第一次拿到比 `purity / NMI` 更硬的证据，说明当前单层 tail-conditioned block 已经出现了 token-level 的 `LM-relevant specialization`。

- 目的：

  $$
  \text{被 router 选中的 expert，是否真的比替代 expert 更能降低 next-token loss？}
  $$

- 数据：沿用单层真实 block setting，在 `WoS middle / rare` token bucket 上做 token-level counterfactual gap
- 数据量：
  - 训练数据仍沿用单层真实协议：
    - `WoS covariance docs = 448`
    - `WoS train docs = 896`
    - `WoS test docs = 896`
    - `DCLM cov/train/eval sequences = 512 / 2048 / 256`
  - 频率 bucket 在 `WoS train` 上按 next-token type frequency quantile 定义
- 模型：`Qwen3-0.6B`
- 设置：
  - 继承 `Phase5` 单层最优结构
  - 比较 `with-LB + no-LB`
  - 正式 seed：`2`
- 最重要指标：

  $$
  G_{\mathrm{cf}}(e') = \ell(e') - \ell(e^\star)
  $$

- 代表结果：补充前 + 补充后联合看
  - with-LB
    - `flat`: `G(second) \approx -0.0020 / -0.0026`
    - `expert-tail`: `0.0441 / 0.0567`
    - `hier`: `0.0489 / 0.0604`
  - no-LB
    - `flat`: `0.0041 / 0.0082`
    - `hier`: `0.0356 / 0.0439`
    - `expert-tail`: `0.0679 / 0.0829`
- 当前结论：

  $$
  \text{single-layer tail-conditioned block already exhibits LM-relevant specialization}
  $$

  而且这点对 `no-LB` 稳健。

- 可信假说更新：**把 `H2` 从“结构有效”推进到“功能有效”**

### Phase6-B：expert-input band

一句话版本：当前不能写成“middle uniquely best”或“tail 一定严格优于 extreme”，最稳的结论是：expert 应该看 `tail-oriented band`。

- 目的：

  $$
  \text{experts 最该看的是 raw、head、middle、extreme tail，还是 full tail residual？}
  $$

- 数据：沿用真实单层 block setting
- 数据量：
  - `WoS covariance docs = 448`
  - `WoS train docs = 896`
  - `WoS test docs = 896`
  - `DCLM cov/train/eval sequences = 512 / 2048 / 256`
- 模型：`Qwen3-0.6B`
- 设置：
  - 固定 router，只改 expert input band
  - 比较 `with-LB + no-LB`
  - 正式 seed：`2`
- 最重要对比：
  - `raw`
  - `head`
  - `middle`
  - `extreme tail`
  - `full tail residual`
- 代表结果：补充前 + 补充后联合看
  - with-LB
    - `tail` 在 `WoS rare-token PPL` 上最好
    - `extreme` 在 `middle-token PPL` 上最好
  - no-LB
    - `extreme` 在 `rare-token / middle-token PPL` 上都略优
  - 两轮都稳定成立：

    $$
    \text{extreme / tail / middle} \ll \text{head / raw / baseline}
    $$

- 当前结论：

  $$
  \text{the useful expert-input region is tail-oriented}
  $$

- 可信假说更新：**补强 `H2`，并为下一轮 expert input 设计定向**

### Phase6-C：recursive bottleneck

一句话版本：`R6 \gg R5` 现在已经被拆清了：recursive 的第一瓶颈在 `coarse routing`，不是 `fine-local routing`。

- 目的：

  $$
  \text{recursive learned hierarchy 为什么没学起来？}
  $$

- 数据：synthetic recursive small-model family
- 数据量：
  - `train sequences = 4096`
  - `val sequences = 1024`
  - `seq_len = 128`
  - `2` 个正式 seed
- 模型：recursive small-model
- 设置：
  - 比较 `with-LB + no-LB`
  - 拆分 `R5 / R5c / R5d / R6`
- 最重要对比：
  - `R5`: learned coarse + learned fine
  - `R5c`: oracle coarse + learned fine
  - `R5d`: learned coarse + oracle fine local
  - `R6`: oracle coarse + oracle fine
- 代表结果：补充前 + 补充后联合看
  - with-LB
    - `R5 = 8775.19`
    - `R5c = 2951.38`
    - `R5d = 9121.51`
    - `R6 = 1057.94`
  - no-LB
    - `R5 = 9269.80`
    - `R5c = 2995.38`
    - `R5d = 9445.16`
    - `R6 = 1130.28`
  - 两轮都稳定保持：

    $$
    R5c \ll R5,\qquad R5d \not< R5
    $$

- 当前结论：

  $$
  \text{coarse routing is the primary recursive bottleneck}
  $$

- 可信假说更新：**为 `H3` 提供最清晰的当前诊断**

---

## 5. 非主结果实验的定位

### Phase2：split controller + optimizer decoupling

一句话版本：`WD/LR` 解耦并不是当前真实训练里的主要矛盾。

- 角色：桥接实验，不是最终主结论
- 数据量：
  - `DCLM cov/train/eval sequences = 1024 / 12288 / 1024`
  - `WoS covariance docs = 672`（`96 × 7`）
  - `WoS train docs = 2688`（`384 × 7`）
  - `WoS test docs = 1792`（`256 × 7`）
  - `train_steps = 13000`
  - `2` 个正式 seed
- 作用：说明 toy 里的 optimizer recipe 没有直接转移到真实训练
- 当前结论：

  $$
  \text{WD/LR decoupling is not the main contradiction in real training}
  $$

### Phase3：tail-conditioned routing proxy

一句话版本：`tail-conditioned routing` 在 proxy setting 下有方向性支持，但不能作为真实 block 结论。

- 角色：探索性实验，不作为最终主结果
- 数据量：
  - `DCLM cov/train/eval sequences = 96 / 96 / 32`
  - `WoS covariance docs = 168`（`24 × 7`）
  - `WoS train docs = 224`（`32 × 7`）
  - `WoS test docs = 224`（`32 × 7`）
  - `train_steps = 50`
  - `1` 个 seed 为主的本地 proxy 验证
- 原因：使用了 `domain auxiliary loss`，不能反映当前真实训练范式

---

## 6. 当前最稳的结论

到目前为止，最稳、最适合汇报的结论可以压成下面四条：

1. `Phase1` 证明真实 hidden 中确实存在 shared head，且 $x_t$ 的几何更利于 long-tail 语义区分。
2. `Phase4-C1` 证明真实单层 block replacement 下，`hier_moe_tail_uniform` 已经优于 `baseline_ffn` 和 `flat_moe_raw_uniform`。
3. `Phase5-C2.5 / C2.6` 说明当前最稳定的单因素增益更像来自 `expert-tail input`，而不是 `router-only`；同时 `$x_t$` 在 two-branch family 中是必要的。
4. `Phase6-A / B / C` 进一步说明：单层已经出现 `LM-relevant specialization`，expert 输入应落在 `tail-oriented band`，recursive 的第一瓶颈在 `coarse routing`。

---

## 7. 当前仍然存在的问题

当前仍需要保守写法的地方有四个：

1. 不能把 `split-alone` 写成已经明确打赢 matched-budget dense。
2. 不能把 `router-only 改看 x_t` 写成已经稳定成立。
3. 不能把 `tail` 与 `extreme` 的精细排序写成已经钉死。
4. 不能把 recursive learned hierarchy 写成已经成立；当前只定位了第一瓶颈。

---

## 8. 下一步最自然的规划

如果只从当前旧任务继续推进，下一步最自然的是：

1. 把 `no-LB geometry routing` 作为默认概念口径继续研究。
2. 继续研究为什么 `route margin` 与真实 `G_{\mathrm{cf}}` 的相关性仍然很弱。
3. 在 expert-input 设计上，从 `full tail residual / extreme tail` 二选一，推进到更连续化、可学习的 tail band。
4. recursive 方向优先修 `coarse routing objective`，而不是先修 `fine-local route`。

---

## 9. 实验定位与原因

实验定位统一分成三类：

1. `Real`
   - 使用真实数据
   - 主训练目标与当前主线一致，核心仍是 next-token LM
   - 允许存在 scale reduction、冻结 backbone、单层替换等工程简化
2. `Half-Real`
   - 使用真实数据
   - 但实验目标是表示审计、proxy 指标或额外辅助目标
   - 因此不能把结果直接当作真实主线结论
3. `Toy`
   - 完全由 synthetic 数据生成机制定义
   - 用来隔离结构上界和机制瓶颈

各 phase 的定位如下：

- `Phase1 = Half-Real`
  - 原因：使用真实 `Qwen3-8B + DCLM + WoS`，但做的是表示几何审计，不是 LM 训练收益实验
- `Phase2 = Half-Real`
  - 原因：使用真实数据，但训练目标包含 `WoS domain` 辅助头，不等同于当前主线训练目标
- `Phase3 = Half-Real`
  - 原因：使用真实数据，但依赖 `domain auxiliary loss` 做 proxy routing 验证
- `Phase4-C1 = Real`
  - 原因：回到真实 `Qwen3-0.6B` 单层 block replacement，主目标是 LM-only block 替换
- `Phase5-C2.5 / C2.6 = Real`
  - 原因：在真实数据、真实单层 block replacement 协议下做机制拆解
- `Phase6-A / B = Real`
  - 原因：沿用真实单层 setting，只是在同一训练目标下补做反事实分析与 band intervention
- `Phase6-C = Toy`
  - 原因：使用 synthetic recursive small-model family，目的在于隔离 recursive bottleneck

---

## 10. 数据口径说明

本报告中的数据量要分清 `doc` 和 `sequence` 两种口径。

- `WoS ... docs`
  - 表示从 `WoS` 数据集中抽取的**文档条数**
  - 每条通常对应一个 `abstract`
- `DCLM ... sequences`
  - 表示从 `DCLM` 二进制 shard 中抽取的**token 序列条数**
  - 它不是文档数，而是切成定长后的训练序列数

例如：

- `WoS covariance docs = 448`
  - 表示为了估计 projector / covariance，从 `WoS` 中抽了 `448` 篇文档
  - 在当前真实主线设置下，这通常等于 `64 × 7`，即 `7` 个 domain、每个 domain `64` 篇
- `WoS train docs = 896`
  - 表示用于训练或 token bucket 统计的 `WoS` 文档数
  - 当前真实主线设置下通常等于 `128 × 7`
- `WoS test docs = 896`
  - 表示用于 held-out 测试的 `WoS` 文档数
  - 当前真实主线设置下通常等于 `128 × 7`
- `DCLM sequences = 1792`
  - 表示从 `DCLM` 里抽出的 `1792` 条 token 序列
  - 它不是 `1792` 篇文档，而是 `1792` 条训练序列

每条数据的长度口径如下：

- `Phase1`
  - `WoS doc` 与 `DCLM sequence` 都按 `max_length = 512` token 处理
- `Phase2`
  - 正式 long-run 报告口径为 `max_length = 256`
- `Phase3`
  - proxy 实验口径为 `max_length = 128`
- `Phase4 / Phase5 / Phase6-A / B`
  - 真实单层 block replacement 统一使用 `max_length = 256`
- `Phase6-C`
  - synthetic recursive family 使用固定 `seq_len = 128`

因此，当你看到：

$$
\text{WoS covariance docs = 448}, \qquad \text{DCLM sequences = 1792}
$$

它的含义不是“所有数据一共只有这些样本”，而是：

- 前者是用于该 phase 统计 / 训练 / 评估的 `WoS` 文档采样条数
- 后者是用于该 phase 的 `DCLM` 定长序列采样条数

---

## 11. 当前需要保守写法的边界

下面这些内容目前还不能写得太满：

1. `Phase1`
   - 这是表示几何审计，不是语言建模收益实验
   - `NMI / purity` 只作为辅助证据，不应单独当 headline
2. `Phase4-C1`
   - 这是单层 block replacement，不是全模型 MoE
   - `baseline / flat / hier` 参数量不同
   - `flat / hier` 是 routed family，默认带 `LB`
   - 因此 `C1` 证明“结构有效”，但不能单独完成机制归因
3. `Phase5-C2.5`
   - 不能把结论写成“router-only 已经成立”
   - 更高的 `purity / NMI` 不等于更好的 LM 主任务收益
4. `Phase5-C2.6`
   - 还不能说 `split-alone` 已经明确打赢 matched-budget dense
   - 这一步更像是在证明 `$x_t$` 在 two-branch 结构里是必要条件
5. `Phase6-A`
   - 当前能说的是“选对 expert 有用”
   - 还不能说“router calibration 已经很好”
   - 因为 `route margin` 与真实 `G_{\mathrm{cf}}` 的相关性仍然很弱
6. `Phase6-B`
   - `tail` 与 `extreme` 的精细排序仍不稳定
   - 下一轮更合理的问题是做“连续化 / 可学习的 tail band”，而不是二选一钉死
7. `Phase6-C`
   - 不能进一步写成“只要 coarse 对了就够了”
   - 因为仍有：

     $$
     R5c \gg R6
     $$

   - 剩余 gap 还包含 `fine routing / training signal / support`
