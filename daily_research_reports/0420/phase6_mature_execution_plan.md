# Phase6 成熟执行方案：先定义 LM-relevant Specialization，再判断 Middle Tail 与 Recursive Gap

## 0. 总体评估：你修改后的 plan 是否可执行？

结论：**可执行，但需要收束中心与修正执行口径。**

你修改后的 plan 有三个明显进步：

1. **补上 checkpoint 可用性检查。**  
   旧计划默认可以直接后处理已有 checkpoint；新计划要求先检查 `Phase5-C2.5` 是否保存了可加载 checkpoint，如果没有则先做最小重训并保存 `best_model.pt`。这是必要的。

2. **补上 recursive oracle-gap bridge。**  
   旧计划只问单层 specialization 和 Middle Tail；新计划补上 `R6_oracle >> R5_learned` 后该怎么定位递归瓶颈，这个方向是合理的。

3. **把 middle-frequency token bucket 写实。**  
   旧计划要求报告 middle-frequency PPL，但没有定义 bucket；新计划用 `WoS train` 上 next-token type-frequency quantile 来定义 head / middle / rare，这使指标可执行。

但是当前 plan 也有三个需要修正的地方：

1. **Phase6 变成了三个问题并行，中心容易散。**  
   - Phase6-A 回答：当前单层 hier 是否有 LM-relevant specialization。  
   - Phase6-B 回答：expert 应该学 head / middle / extreme / full tail 哪段信息。  
   - Phase6-C 回答：recursive learned hierarchy 为什么追不上 oracle。  
   这三者都重要，但不是同一个问题。Phase6 的中心应该先是 A：**定义并验证 specialization**。

2. **Phase6-C 不应压过 Phase6-B 成为核心主线。**  
   C 是递归方向的瓶颈诊断；它回答的是“为什么 learned recursive hierarchy 没起来”。  
   但如果 A 发现当前单层 expert 根本没有功能性 specialization，那么直接修 recursive router 会过早。  
   因此 C 应作为 **conditional branch**，不是 Phase6 主线的第二优先级。

3. **A / B / C 都有实现细节需要更严谨，否则会产生伪结论。**  
   - A 中 counterfactual expert gap 必须明确是“替换 tail expert contribution 后的 token NLL”，不能只算 expert 单独输出。
   - B 中不同 band 的维度不同，会混入容量变量，必须做 dimension-matched 控制。
   - C 中 oracle routing 必须区分“后处理替换 routing”和“训练时使用 oracle routing”，否则 gap decomposition 会口径混乱。

因此，本成熟方案将 Phase6 收束为：

> **Phase6-Core：先判断当前单层 hier 是否真的有 LM-relevant specialization。**  
> **Phase6-B：若 A 通过，再判断 Middle Tail 是否是 expert 最值得学习的频带。**  
> **Phase6-C：作为递归方向的条件分支，用来解释 `R6_oracle >> R5_learned`，但不直接作为 Phase6 主线核心。**

---

## 1. 当前研究背景

### 1.1 已经比较稳的结论

1. 真实 hidden state 中存在 shared head。
2. tail residual：
   $$
   x_t = P_t(x-\mu)
   $$
   在几何上比 raw hidden 更适合 long-tail / domain 相关结构读出。
3. 真实 `Qwen3-0.6B` 单层 block replacement 中，`combined tail-conditioned routed block` 已经优于 `baseline_ffn` 和 `flat_moe_raw_uniform`。
4. Phase5-C2 / C2.5 / C2.6 显示：
   - 收益不只是 split；
   - 也不只是 expert 数量 / 容量；
   - 在 routed family 里，最稳定的单因素更像是：
     $$
     \text{expert input}: x \rightarrow x_t
     $$
   - `router-only: x -> x_t` 目前仍然弱。
5. Phase5-D1 显示：
   - recursive oracle upper bound 很强；
   - learned recursive hierarchy 尚未成立。

### 1.2 当前不能过度宣称的内容

1. 不能说 estimated projector 已经稳定替代 oracle split。
2. 不能说 router 改成看 $x_t$ 本身已经足够。
3. 不能说 purity / NMI 高就等于 LM specialization。
4. 不能说 recursive learned hierarchy 已经成立。
5. 不能把 WD / LR 重新拉回主主线。

---

## 2. Phase6 的核心问题

Phase6 只聚焦一个中心：

> 当前单层 `combined tail-conditioned routed block` 的收益，到底是不是 **LM-relevant specialization**？

这里的 **LM-relevant specialization** 定义为：

> 对某个 token，上游 router 选中的 expert，必须比替代 expert 更能降低 next-token loss。

形式化地，设上下文为 $c$，next token 为 $y$，真实路由 expert 为：

$$
e^\star = r(c)
$$

替代 expert 为 $e'$。定义反事实 expert gap：

$$
G_{\mathrm{cf}}(e')
=
\mathbb{E}
\left[
\ell(y, f_{e'}(c))
-
\ell(y, f_{e^\star}(c))
\right]
$$

若：

$$
G_{\mathrm{cf}}(e') > 0
$$

并且这个优势在 rare / middle-tail token bucket 上稳定存在，才可以说当前 expert 有功能性 specialization。

---

## 3. Phase6 执行总览

### 必须先做

- **Phase6-A：反事实 Expert Gap 审计**

### A 通过后再做

- **Phase6-B：Middle Tail 频带干预实验**

### 条件分支

- **Phase6-C：Recursive Oracle-Gap Bridge**
  - 如果团队短期必须解释 D1 的 `R6 >> R5`，可以并行跑 small-model C-lite；
  - 但它不应替代 A；
  - 不应直接上真实 recursive Qwen。

---

# Phase6-A：反事实 Expert Gap 审计

## A0. 目的

判断当前 `hier_moe_tail_uniform` 的收益是否真的来自 expert selection。

换句话说，回答：

> 被 router 选中的 expert 是否真的比替代 expert 更适合当前 token？

---

## A1. competing hypotheses

### H-A1：LM-relevant specialization 成立

被选中的 expert 对当前 token 的 NLL 低于替代 expert：

$$
G_{\mathrm{cf}} > 0
$$

并且优势在 middle / rare token bucket 更明显。

### H-A2：收益主要来自 expert-tail input

所有 expert 只要看 $x_t$ 都差不多，真实选中 expert并没有明显优势：

$$
G_{\mathrm{cf}} \approx 0
$$

但整体 PPL 仍好于 flat。

### H-A3：收益主要来自 soft ensemble / capacity

均匀 expert 平均或第二高分 expert 接近真实 routing，说明 router selection 不是主因。

---

## A2. 必测对象

优先测试已有或重训后的真实模型 checkpoint：

1. `hier_moe_tail_uniform`
2. `router_raw_expert_tail_uniform`
3. `flat_moe_raw_uniform`

可选：

4. `uniform_expert_mixture_tail`

---

## A3. 执行前检查

必须先检查：

1. checkpoint 是否存在；
2. checkpoint 是否对应最终汇报使用的 config；
3. projector 协议是否一致；
4. 是否保存 router logits / expert outputs 所需的 forward hooks。

如果 checkpoint 不存在，不要做不完整后处理。先补最小重训：

- configs：
  - `hier_moe_tail_uniform`
  - `router_raw_expert_tail_uniform`
  - `flat_moe_raw_uniform`
- seeds：
  - `20260418`
  - `20260419`
  - 资源允许再加 `20260420`
- 训练时必须保存：
  - `best_model.pt`
  - `final_model.pt`
  - `config.json`
  - `projector.pt`
  - `eval_indices.json`

---

## A4. 关键实现：反事实 forward 的正确口径

当前模型输出不是单个 expert 单独决定的，而是：

$$
h_{\mathrm{out}}
=
h_{\mathrm{in}}
+
u_c(x)
+
\sum_i g_i(x_{\mathrm{router}})u_i(x_{\mathrm{expert}})
$$

因此反事实 expert gap 不能只算“expert 单独输出”的 loss。正确做法是替换 tail mixture contribution 后重新计算 token NLL。

### A4.1 真实输出

$$
u_t^\star
=
\sum_i g_i u_i
$$

$$
h^\star
=
h_{\mathrm{in}} + u_c + u_t^\star
$$

得到真实 token loss：

$$
\ell^\star
=
\ell(y, h^\star)
$$

### A4.2 one-hot top expert

令 $e^\star=\arg\max_i g_i$：

$$
u_t^{\mathrm{top1}} = u_{e^\star}
$$

计算：

$$
\ell^{\mathrm{top1}}
$$

### A4.3 second-best expert

令 $e_2$ 为第二高分 expert：

$$
u_t^{\mathrm{second}} = u_{e_2}
$$

计算：

$$
G_{\mathrm{second}}
=
\mathbb{E}[\ell^{\mathrm{second}}-\ell^{\mathrm{top1}}]
$$

### A4.4 random expert

随机选 $e_r\neq e^\star$：

$$
G_{\mathrm{random}}
=
\mathbb{E}[\ell^{\mathrm{random}}-\ell^{\mathrm{top1}}]
$$

### A4.5 uniform average expert

$$
u_t^{\mathrm{uniform}}
=
\frac{1}{N}\sum_i u_i
$$

$$
G_{\mathrm{uniform}}
=
\mathbb{E}[\ell^{\mathrm{uniform}}-\ell^\star]
$$

说明：

- 对 top-k soft routing，`真实 soft mixture` 和 `one-hot top1` 都要报告。
- 如果真实 soft mixture 优于 top1，说明 mixture 本身有集成价值。
- 如果 top1 明显优于替代 expert，才说明 expert selection 有功能性。

---

## A5. 分 bucket 统计

必须报告：

1. all tokens
2. WoS rare tokens
3. middle-frequency tokens
4. head/common tokens
5. DCLM tokens
6. WoS tokens

### token frequency bucket 定义

使用训练集 next-token type-frequency，而不是只用输入 token 频率。

默认：

- head/common：top 25% token types
- middle：25% 到 75% token types
- rare：bottom 25% token types

同时保留旧版 `legacy WoS rare-token PPL` 以便和 Phase5 对齐。

---

## A6. 主指标

1. `G_cf_second_best`
2. `G_cf_random`
3. `G_cf_uniform_avg`
4. `soft_mixture_vs_top1_gap`
5. `gap_by_frequency_bucket`
6. `gap_by_domain_bucket`
7. `route_margin`
8. `corr(route_margin, G_cf)`

---

## A7. 判读规则

### A-pass：specialization 成立

若满足：

1. `G_cf_second_best > 0`
2. `G_cf_random > 0`
3. 在 middle / rare bucket 中更明显
4. 跨 seed 方向一致

则更新为：

> 当前单层 hier 已经出现 LM-relevant specialization。

下一步进入 Phase6-B。

---

### A-factorization：只有 factorization gain

若：

1. `G_cf ≈ 0`
2. 但 `hier_moe_tail_uniform` 仍然主指标更好

则更新为：

> 当前收益主要来自 expert-tail input 与 block factorization，不来自 expert selection。

下一步不应急着做 recursive routing，而应考虑：
- split-first factorized FFN；
- learned projection；
- expert input space 设计。

---

### A-ensemble：soft mixture 主导

若：

1. soft mixture 明显优于 top1
2. top1 不明显优于 random / second

则更新为：

> 当前 MoE 更像 soft ensemble，不是离散 specialization。

下一步应弱化离散 expert 叙事。

---

# Phase6-B：Middle Tail 频带干预实验

## B0. 执行条件

建议只在以下条件至少一个成立时执行：

1. Phase6-A 显示存在 LM-relevant specialization；
2. 或者团队明确希望验证导师的 Middle Tail 观点。

如果 A 显示完全没有 expert selection 价值，B 仍可执行，但结论应解释为：

> 哪个 band 更适合作为 expert input，而不是哪个 band 产生 specialization。

---

## B1. 目的

回答：

> experts 应该学 head、middle tail、extreme tail，还是 full tail residual？

---

## B2. 数学定义

设 centered hidden 为：

$$
x_c = x-\mu
$$

对 centered covariance 做特征分解，得到 $V$。

### head band

$$
x_{\mathrm{head}}
=
V_{1:k_1}V_{1:k_1}^\top x_c
$$

### middle band

$$
x_{\mathrm{middle}}
=
V_{k_1+1:k_2}V_{k_1+1:k_2}^\top x_c
$$

### extreme tail band

$$
x_{\mathrm{extreme}}
=
(I-V_{1:k_2}V_{1:k_2}^\top)x_c
$$

### full tail residual

$$
x_t
=
(I-V_{1:k_t}V_{1:k_t}^\top)x_c
$$

---

## B3. 关键修正：dimension-matched 控制

不同 band 的维度不同，会混入容量变量。

因此每个 band 必须进入同一个 adapter 维度：

$$
z_{\mathrm{band}} = A_{\mathrm{band}}x_{\mathrm{band}}
$$

其中 $A_{\mathrm{band}}$ 输出维度统一为 $d_{\mathrm{band}}$。

推荐：

- `d_band = 64` 或沿用现有 tail expert input dimension
- 所有 band 的 expert width、expert 数、参数量保持一致
- 如使用 projection adapter，所有组都使用同类 adapter

---

## B4. 推荐 band sweep

主设定：

- `k1 = 8`
- `k2 = 32`
- `k_t = 16`

可选附加：

- `(8,16)`
- `(16,32)`
- `(16,64)`

如果资源有限，只跑主设定。

---

## B5. 对照组

固定 router 为 raw，只改 expert input：

1. `baseline_ffn`
2. `router_raw_expert_raw_uniform`
3. `router_raw_expert_head_uniform`
4. `router_raw_expert_middle_uniform`
5. `router_raw_expert_extreme_uniform`
6. `router_raw_expert_tail_uniform`

原因：

- Phase5-C2.5 已经提示 expert input 是更稳定因素；
- 这里先不要同时改变 router input；
- 否则无法判断到底是 band 有效还是 router 有效。

---

## B6. 主指标

1. `DCLM_PPL`
2. `WoS_PPL`
3. `WoS_rare_token_PPL`
4. `middle_frequency_token_PPL`
5. `counterfactual_gap_uniform_avg`
6. `band_energy_fraction`

---

## B7. 判读规则

### B-middle

若 middle 最好或接近 tail 最好，并且优于 head / extreme：

> Middle Tail 是当前更值得押注的 expert 学习对象。

下一步：
- 围绕 middle-tail band 设计 projector；
- recursive hierarchy 只考虑在 middle-tail 内部继续做 local split。

### B-extreme

若 extreme 最好：

> extreme tail 并不只是噪声，之前判断过强。

下一步：
- 可以继续探索 deeper tail；
- 但必须加入样本支持和梯度稳定性判据。

### B-full-tail

若 full tail residual 最好，而 middle / extreme 单独都不够：

> 有用信息不在单一固定 band，而在 residual 的组合中。

下一步：
- 学习 projector；
- 或学习 band weighting，而不是手工切谱段。

### B-head/raw

若 head/raw 最好：

> 当前 split-first / tail residual 主线需要重新收缩；expert 可能仍依赖 common features。

---

# Phase6-C：Recursive Oracle-Gap Bridge

## C0. 执行定位

C 是 **条件分支**，不是 Phase6 主线核心。

执行条件：

1. 团队需要解释 D1 中 `R6_oracle >> R5_learned`；
2. 或 Phase6-A/B 支持继续推进 expert specialization；
3. 仍然只在 small-model family 中执行；
4. 不直接上真实 recursive Qwen。

---

## C1. 目的

回答：

> learned recursive hierarchy 追不上 oracle，到底是 level-1 coarse routing 错、level-2 fine routing 错，还是训练方式 / leaf data support 错？

---

## C2. 递归路由误差指标

报告：

$$
a_1 = \Pr(\hat z_1=z_1)
$$

$$
a_2 = \Pr(\hat z_2=z_2 \mid \hat z_1=z_1)
$$

$$
a_{\mathrm{joint}}=\Pr(\hat z_1=z_1,\hat z_2=z_2)
$$

以及：

- coarse NMI
- fine NMI
- joint NMI
- overall PPL
- common PPL
- coarse-tail PPL
- fine-tail PPL
- rare-fine-tail PPL

---

## C3. 关键修正：区分 evaluation intervention 和 retrained ablation

### C3.1 evaluation intervention

在同一个 trained R5 checkpoint 上，后处理替换 route。

优点：
- 便宜；
- 能快速看 routing error 是否明显。

缺点：
- experts 是按 learned route 训练的，换 oracle route 可能产生分布错位。

因此只能作为诊断，不作最终结论。

### C3.2 retrained oracle ablation

训练时就使用 oracle routing。

这是主结论应该依赖的口径。

---

## C4. 必跑组

在 `rho1 = 0.2, rho2 = 0.1` 下运行：

1. `R5_learned_coarse_learned_fine`
2. `R6_oracle_coarse_oracle_fine`
3. `R5c_oracle_coarse_learned_fine`
4. `R5d_learned_coarse_oracle_fine_local`

建议同时跑：

5. `R5e_aux_ce_coarse`
6. `R5f_aux_ce_coarse_fine`

其中辅助监督为：

$$
L = L_{\mathrm{LM}} + \lambda_1 \mathrm{CE}(\hat z_1,z_1)
$$

或：

$$
L = L_{\mathrm{LM}} + \lambda_1 \mathrm{CE}(\hat z_1,z_1)
+
\lambda_2 \mathrm{CE}(\hat z_2,z_2)
$$

推荐 annealing：

$$
\lambda_1(t),\lambda_2(t)\downarrow 0
$$

---

## C5. 判读规则

注意：PPL 越低越好。

### C-coarse-bottleneck

如果 `R5c` 大幅接近 `R6`，说明：

> 主要瓶颈在 level-1 coarse routing。

### C-fine-bottleneck

如果 `R5c` 仍远差于 `R6`，但 `R5d` 明显改善，说明：

> level-2 fine routing 是主要瓶颈。

### C-training-bottleneck

如果 `R5e/R5f` 明显优于 `R5`，说明：

> router 学习目标或训练信号不足是瓶颈。

### C-structural-failure

如果 `R5c/R5d/R5e/R5f` 都不能缩小 gap，说明：

> 递归失败不只是 router 没训好，可能是 leaf support 太弱、两级误差累乘、局部分支容量不足或任务统计不支持当前递归形式。

---

# 4. 最终执行优先级

## Priority 0：准备与复现

1. 检查 checkpoint。
2. 若无 checkpoint，补最小重训。
3. 确认 projector、seed、eval set 与 Phase5 汇报一致。

## Priority 1：Phase6-A

必须先做。  
它决定我们能否继续使用 “specialized expert” 这个表述。

## Priority 2：Phase6-B

A 通过后执行。  
它决定 Middle Tail 是否是下一阶段应该押注的对象。

## Priority 3：Phase6-C

作为递归方向分支执行。  
如果资源有限，C 只跑 C3/C4 的 minimal oracle-gap decomposition，不跑 teacher-aided variants。

---

# 5. 最小执行集合

如果资源有限，只执行以下最小集合。

## Minimal-A

configs：

1. `hier_moe_tail_uniform`
2. `router_raw_expert_tail_uniform`
3. `flat_moe_raw_uniform`

seeds：

- `20260418`
- `20260419`

outputs：

- `counterfactual_gap_by_bucket.csv`
- `expert_wise_nll.csv`
- `route_margin_vs_gap.csv`
- `phase6A_report.md`

## Minimal-B

configs：

1. `router_raw_expert_raw_uniform`
2. `router_raw_expert_middle_uniform`
3. `router_raw_expert_extreme_uniform`
4. `router_raw_expert_tail_uniform`

band：

- `k1=8`
- `k2=32`
- `k_t=16`

outputs：

- `band_intervention_summary.csv`
- `band_energy_fraction.csv`
- `phase6B_report.md`

## Minimal-C

small-model configs：

1. `R5`
2. `R6`
3. `R5c`
4. `R5d`

outputs：

- `recursive_oracle_gap_summary.csv`
- `recursive_router_accuracy.csv`
- `phase6C_report.md`

---

# 6. 输出报告模板

每个 report 必须包含：

1. 实验目的
2. 对立假设
3. 设置与可复现信息
4. 主要结果表
5. 关键图
6. 结论更新
7. 哪些旧叙事被支持 / 削弱
8. 下一步 gate decision

---

# 7. Phase6 一句话执行口径

Phase6 不是继续证明 “hier 比 flat 好”。

Phase6 要回答的是：

> **当前 hier 的收益是否真的来自 LM-relevant expert specialization；如果是，专家最应该学习的是 Middle Tail、Extreme Tail，还是完整 tail residual；如果还要推进递归结构，递归失败的瓶颈到底在哪里。**
