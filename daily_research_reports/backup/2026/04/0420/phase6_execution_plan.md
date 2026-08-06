# Phase6 执行计划：LM-relevant Specialization、Middle Tail 与 Recursive Oracle-Gap Bridge

> Canonical Phase6 plan.  
> 请优先把这份文档交给实验 agent，而不是根目录 `docs/` 下的旧 prompt。

## 0. 这版计划相对旧 prompt 修了什么

这版不是简单搬运旧 prompt，而是补了 3 个会影响执行和结论的关键缺口。

1. 修正了 `checkpoint` 假设。  
旧 prompt 默认可以直接复用 `Phase5-C2.5` checkpoint，但当前 `phase5_recursive_hierarchical_moe` 目录下默认并没有保存好的 real-model checkpoint。因此 `Phase6-A` 必须先验证 checkpoint 是否存在；若不存在，需要补做最小重训并显式保存 `best_model.pt`。

2. 补上了 `R6 \gg R5` 之后最该做的递归桥接实验。  
旧 prompt 主要关注单层 specialization 与 Middle Tail，但没有正面回答：
\[
R6_{\text{oracle}} \gg R5_{\text{learned}}
\]
以后，我们到底该怎样逼近 oracle recursive routing。  
这版新增 `Phase6-C`，专门做 recursive oracle-gap decomposition 与 teacher-aided routing。

3. 把 `middle-frequency token` 的定义写实了。  
旧 prompt 里要求报告 `middle-frequency token PPL`，但没有定义 bucket。  
这版规定：默认用 `WoS train` 上 label token 频次的 type-frequency quantile 来定义 `head / middle / rare`。

---

## 1. 当前研究位置

### 1.1 已经成立的内容

1. 真实 hidden state 中存在 shared head；`tail residual`
\[
x_t = P_t(x-\mu)
\]
在几何上比 raw hidden 更适合 long-tail 语义区分。

2. 在真实 `Qwen3-0.6B` 单层 block replacement 上，`combined tail-conditioned routed block` 已经优于 `baseline_ffn` 和 `flat_moe_raw_uniform`。

3. `Phase5-C2/C2.5/C2.6` 进一步说明：
   - 收益不只是 `split`
   - 也不只是 expert 容量
   - routed family 里最稳定的单因素增益更像是 `expert input: x \to x_t`
   - `router-only: x \to x_t` 目前仍然很弱
   - `split-alone` 还没有明确打赢 matched-budget wide dense
   - 但在 two-branch family 内部，给第二分支喂 `x_t` 是必要的

4. `LB` 不是当前 real-model 主指标的关键因子。`with_lb / no_lb` 在主 PPL 上几乎等价，但 `no_lb` 经常给出更高的 specialization proxy。

5. `Phase5-D1` 说明：
   - recursive hierarchy 的 oracle upper bound 很强
   - learned recursive hierarchy 还没有成立

### 1.2 当前不能过度宣称的内容

1. `estimated projector` 已经稳定替代 oracle split
2. `router-only` 改成看 `x_t` 已经稳定成立
3. 更高的 purity / NMI 就等于更好的 LM 主任务收益
4. recursive learned hierarchy 已经成立

---

## 2. Phase6 的总目标

Phase6 不再重新证明“单层 hier 比 flat 好”，而是回答 3 个更窄、也更关键的问题：

1. 当前单层 `hier_moe_tail_uniform` 的收益，是否已经构成 **LM-relevant specialization**？
2. 如果 experts 主要在学 tail 信息，那么更值得学的是哪一段：`head / middle / extreme tail / full tail residual`？
3. 从
\[
R6_{\text{oracle}} \gg R5_{\text{learned}}
\]
出发，下一步到底应该优先修哪个递归路由瓶颈？

---

# Phase6-A：反事实 Expert Gap 审计

## A0. 目的

回答：

> 当前 `hier_moe_tail_uniform` 中，被 router 选中的 expert，是否真的比替代 expert 更适合当前 token？

这一步的目标不是继续看 `purity/NMI`，而是定义 **LM-relevant specialization**。

## A1. 数学对象

设上下文为 \(c\)，真实被选中的 expert 为
\[
e^\star = r(c).
\]

真实 expert 的 token loss 为
\[
\ell^\star = \ell\big(y, f_{e^\star}(c)\big).
\]

对任意替代 expert \(e'\)，定义反事实 gap：
\[
G_{\mathrm{cf}}(e')
=
\mathbb{E}\left[
\ell\big(y, f_{e'}(c)\big)
-
\ell\big(y, f_{e^\star}(c)\big)
\right].
\]

如果
\[
G_{\mathrm{cf}}(e') > 0
\]
并且这种优势稳定出现在某些 token bucket 上，才能说被选中的 expert 具有功能性 specialization。

## A2. 必测对象

优先比较：

1. `hier_moe_tail_uniform`
2. `router_raw_expert_tail_uniform`
3. `flat_moe_raw_uniform`

可选附加：

4. `uniform_expert_mixture_tail`

## A3. 执行前检查：checkpoint 可用性

先检查下面两件事：

1. 现有 `Phase5-C2.5` 结果目录里是否有可加载的 real-model checkpoint。
2. checkpoint 是否对应最终汇报使用的 config / seed / projector 协议。

如果 checkpoint 不存在，**不要硬做后处理**，而是先补最小重训：

- 至少重训 `hier_moe_tail_uniform / router_raw_expert_tail_uniform / flat_moe_raw_uniform`
- seed 至少 `20260418, 20260419`
- 若资源允许，再加 `20260420`
- 训练时显式保存 `best_model.pt`

## A4. 具体步骤

1. 加载 checkpoint
2. 在验证集上逐 token forward
3. 对每个 token 记录：
   - 真实选中的 expert
   - top-2 router score
   - 每个 expert 单独前向时的 token NLL
   - 均匀 expert 平均的 token NLL
4. 分 bucket 统计：
   - all tokens
   - WoS rare tokens
   - middle-frequency tokens
   - head/common tokens
   - 若可行，再加 domain buckets
5. 计算：
   - `G_cf(second_best)`
   - `G_cf(random_expert)`
   - `G_cf(uniform_avg)`
   - 可选：`G_cf(best_other_expert)`
6. 额外统计：
   - route margin `m = s_{(1)} - s_{(2)}`
   - `corr(m, G_cf)`
   - expert-wise token count
   - expert-wise rare-token NLL

## A5. 主判读

### 结果 A
若 `G_cf > 0` 稳定成立，且在 rare / middle bucket 尤其明显，则更新为：

> 当前单层 hier 已经出现 LM-relevant specialization。

### 结果 B
若 `G_cf \approx 0`，但 `hier` 主指标仍好于 flat / baseline，则更新为：

> 当前收益主要来自 `expert-tail input + block factorization`，而不是 expert selection 本身。

### 结果 C
若 `router_raw_expert_tail_uniform` 与 `hier_moe_tail_uniform` 的 `G_cf` 都很弱，但主指标都好于 flat，则更新为：

> 当前最稳收益来自 `expert input: x \to x_t`，不是 router 选择。

---

# Phase6-B：Middle Tail 频带干预实验

## B0. 目的

回答：

> 如果 experts 不该盲目学习 head 或 extreme tail，那么 Middle Tail 是否才是更值得学的对象？

## B1. 表示 band 的定义

设 centered hidden 为
\[
x_c = x-\mu.
\]

对 centered covariance 做特征分解，得到基 \(V\)。定义：

head band：
\[
x_{\mathrm{head}} = V_{1:k_1}V_{1:k_1}^\top x_c
\]

middle band：
\[
x_{\mathrm{middle}} = V_{k_1+1:k_2}V_{k_1+1:k_2}^\top x_c
\]

extreme tail band：
\[
x_{\mathrm{extreme}} = \left(I - V_{1:k_2}V_{1:k_2}^\top\right)x_c
\]

full tail residual：
\[
x_t = \left(I - V_{1:k_t}V_{1:k_t}^\top\right)x_c
\]

## B2. token frequency bucket 的定义

用 `WoS train` 上 label token 的 type-frequency 定义：

1. `head/common token bucket`
   - 频次位于 top 25% 的 token types
2. `middle-frequency bucket`
   - 频次位于 25% 到 75% 分位的 token types
3. `rare bucket`
   - 频次位于 bottom 25% 的 token types

为了与旧 `Phase5` 保持可比，也请额外保留 legacy `WoS rare-token PPL`。

## B3. 推荐 band sweep

主设定：

- `k1 = 8`
- `k2 = 32`
- `k_t = 16`

可选附加：

- `(8,16)`
- `(16,32)`
- `(16,64)`

## B4. 对照组

固定 router 为 raw，只改 expert input：

1. `baseline_ffn`
2. `router_raw_expert_raw_uniform`
3. `router_raw_expert_head_uniform`
4. `router_raw_expert_middle_uniform`
5. `router_raw_expert_extreme_uniform`
6. `router_raw_expert_tail_uniform`

原因：`Phase5-C2.5` 已经显示 expert input 是更稳定的单因素，`Phase6-B` 先不要把 router 变量再混进来。

## B5. 主指标

1. `DCLM PPL`
2. `WoS PPL`
3. `WoS rare-token PPL`
4. `middle-frequency token PPL`

可选诊断：

1. `counterfactual_gap_uniform_avg`
2. `expert_wise_token_count`
3. `expert_wise_rare_token_nll`
4. `band_energy_fraction`

## B6. 主判读

### 结果 A
若 `middle` 最好或接近 `tail` 最好，且优于 `head/extreme`，则更新为：

> Middle Tail 是当前更值得押注的 expert 学习对象。

### 结果 B
若 `extreme` 最好，则更新为：

> “extreme tail 多为噪声”的判断过强，需要重新评估。

### 结果 C
若 `head/raw` 最好，则更新为：

> 当前 split-first 主线还没真正抓到最可学习的结构频带。

### 结果 D
若 `tail residual` 最好，但 `middle/extreme` 单独都不够，则更新为：

> 有用信息不在单一 band，而在 tail residual 的组合中；下一步应考虑 learned projector / learned band。

---

# Phase6-C：从 `R6 \gg R5` 出发的 recursive oracle-gap bridge

## C0. 目的

回答：

> 既然 `R6` 很强、`R5` 很弱，那么 recursive learned routing 到底是卡在 level-1 coarse router，还是 level-2 fine router，还是训练方式本身？

## C1. 先做误差分解，而不是直接上真实 recursive Qwen

本阶段仍然留在 `D1` small-model family。  
不要直接进入真实 recursive Qwen。

原因很简单：

- `R5` 当前还没打赢一级结构
- `R6` 的价值是做结构上界诊断
- 在 small-model 里先拆清瓶颈，性价比最高

## C2. 递归路由误差的诊断量

对 learned recursive router，报告：

level-1 正确率：
\[
a_1 = \Pr(\hat z_1 = z_1)
\]

条件 level-2 正确率：
\[
a_2 = \Pr(\hat z_2 = z_2 \mid \hat z_1 = z_1)
\]

joint 正确率：
\[
a_{\mathrm{joint}} = \Pr(\hat z_1 = z_1,\hat z_2 = z_2)
\]

同时继续报告：

- `coarse/fine/joint NMI`
- `overall/common/coarse-tail/fine-tail/rare-fine-tail PPL`

## C3. 第一步：oracle-gap decomposition

在 `rho1 = 0.2, rho2 = 0.1` 的最佳区间，至少跑下面 4 组：

1. `R5_learned_coarse_learned_fine`
   - 现有 `R5`
2. `R6_oracle_coarse_oracle_fine`
   - 现有 `R6`
3. `R5c_oracle_coarse_learned_fine`
   - level-1 用 oracle coarse routing
   - level-2 保持 learned fine routing
4. `R5d_learned_coarse_oracle_fine_local`
   - level-1 保持 learned coarse routing
   - level-2 在选中的 coarse branch 内使用 oracle fine-local index

### 这 4 组分别回答什么

若
\[
R5c \approx R6
\]
则说明主要瓶颈在 level-1 coarse routing。

若
\[
R5c \ll R5,\quad R5d \approx R5
\]
则更强地说明 coarse routing 是第一瓶颈。

若
\[
R5c \text{ 仍远差于 } R6
\]
则说明即使 coarse 对了，fine routing 或训练方式仍然有大问题。

## C4. 第二步：teacher-aided recursive routing

只有在 `C3` 跑完后，再进入 teacher-aided 学习。

优先尝试：

1. `R5e_aux_ce_coarse`
   - 对 coarse router 加辅助监督：
\[
L = L_{\mathrm{LM}} + \lambda_1 \mathrm{CE}(\hat z_1, z_1)
\]

2. `R5f_aux_ce_coarse_fine`
   - 对 coarse / fine router 同时加辅助监督：
\[
L = L_{\mathrm{LM}} + \lambda_1 \mathrm{CE}(\hat z_1, z_1) + \lambda_2 \mathrm{CE}(\hat z_2, z_2)
\]

推荐加一个 annealing 版本：

\[
\lambda_1(t), \lambda_2(t) \downarrow 0
\]

也就是训练早期更强地教 router，后期回到以 LM 为主。

## C5. Phase6-C 的 gate

### 通过条件

至少出现下面之一：

1. `R5c` 大幅接近 `R6`
2. `R5e` 或 `R5f` 明显优于 `R5`
3. `a_1`、`a_2` 的瓶颈定位非常明确，足以指导下一轮结构修改

### 不通过时的结论

如果 `R5c`、`R5d`、`R5e`、`R5f` 都不能显著缩小 oracle gap，则更新为：

> 当前 recursive gap 不只是“router 没训好”，而更像是 leaf data support 太弱、两级误差累乘过重，暂时不值得直接推进真实 recursive Qwen。

---

## 3. 优先级

### 优先级 1：Phase6-A

因为它先回答：

> 当前真实单层 hier 到底有没有 LM-relevant specialization？

### 优先级 2：Phase6-C

因为它直接回答：

> `R6 \gg R5` 以后，递归下一步该修哪个瓶颈？

### 优先级 3：Phase6-B

因为它更像是：

> 当我们确认专家确实在学某些东西后，再问“哪一段信息最值得学”。

---

## 4. 执行约束

1. 不要重新把 `WD/LR` 作为主主线。
2. 不要把 `purity/NMI` 当成主结论，只保留为诊断。
3. 不要在 Phase6 里直接上真实 recursive Qwen。
4. 所有结论优先看 LM-relevant 指标：
   - token NLL
   - rare-token / rare-fine-tail PPL
   - counterfactual expert gap
   - oracle-gap decomposition

---

## 5. 输出物要求

### Phase6-A

1. `phase6A_counterfactual_gap_report.md`
2. `counterfactual_gap_by_bucket.csv`
3. `expert_wise_nll.csv`
4. `route_margin_vs_gap.csv`

### Phase6-B

1. `phase6B_middle_tail_band_report.md`
2. `band_intervention_summary.csv`
3. `band_energy_fraction.csv`

### Phase6-C

1. `phase6C_recursive_oracle_gap_report.md`
2. `recursive_oracle_gap_summary.csv`
3. `recursive_router_accuracy.csv`
4. `teacher_aided_recursive_summary.csv`

---

## 6. 一句话执行口径

Phase6 的核心不是继续证明“hier 比 flat 好”，而是：

> 先用反事实 expert gap 判断单层 hier 到底有没有功能性 specialization，再用 oracle-gap decomposition 回答 recursive 为什么没学出来，最后才讨论 Middle Tail 是否是下一阶段应该押注的对象。
