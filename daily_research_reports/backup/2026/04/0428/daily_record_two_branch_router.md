# Daily Record B: Two-branch + Router

## 0. 背景和阅读说明

本文件记录的是 **two-branch split 为什么没有稳定转化为下游收益，以及下一步为什么要转向 router audit** 这条路线。

最初的问题是：如果用某个 reference representation，例如

$$
P(x-\mu)
$$

把 hidden state 投影到某些 PCA/SVD variance band，能否把 common / tail-sensitive 表征分开，并减少 continual learning 中的干扰？

这里需要区分三件事：

1. **Representation separability**：投影后样本或 token bucket 在表征空间中更容易分开。
2. **Branch contribution pattern**：two-branch 模型中某个 branch 对 middle / rare token loss 的贡献更大。
3. **Downstream / CL gain**：模型在 NTP、new-task learning、old-task forgetting 上真正优于 matched dense、random split 等 control。

当前证据说明：前两者可能存在信号，但第三者还没有稳定成立。因此，这条路线不应该继续简单追问“哪个固定 split 更好”，而应该转向：

> learned / oracle router 能不能把 $P(x-\mu)$ 暴露出的 separability 变成真正可用的 expert specialization？

---

## 1. 路线定位

本路线承接 Phase8 / H3 causal audit。当前不能再把 fixed two-branch split 直接作为 CL 成功证据，因为 matched dense、raw two-branch、random split、head16 等 controls 已经削弱了原始 H3 claim。

研究中心应从：

> 固定 split 是否直接带来 CL 收益？

转向：

> 为什么 $P(x-\mu)$ 类 reference representation 可以让表征分得更开，却不能稳定转化为下游收益？learned router 能否把这种 separability 转化为真正的 expert specialization？

---

## 2. Evidence Snapshot

来自 `Phase8-H3 Bridge Old-Stage Causal Audit`：

本轮实验做的不是 full hierarchical MoE，而是把旧 Phase8 two-branch 信号放回更严格的 old-stage continual-learning protocol，并加入 H3 causal controls。

实验流程：

1. **Old-stage**：先用 old-domain data 训练 layer-8 replacement block，使模型形成 old-task state。
2. **New-stage**：从 old-stage checkpoint 出发，用 new-domain support data 做少步 adaptation。
3. **评估**：比较 old loss 是否上升、new query loss 是否下降，以及 middle / rare token bucket 是否有特殊贡献。

关键结果：

1. Dense、replay、raw two-branch、random split、head16、u50、ext、u50_ext、normalized variants、full_tail_resid 均已比较。
2. Gate decision 是 `no_valid_forgetting_object`：matched dense baseline 没有稳定 positive new-task learning / forgetting object，因此当前 setting 不适合直接评估 anti-forgetting claim。
3. Branch ablation 显示 middle/rare contribution 可见，但这只能说明 fixed split 有 contribution pattern。
4. Hidden-gradient conflict 多数不是明显负冲突，说明当前 old/new task 可能没有制造足够强的梯度干扰。
5. Stage B routing diagnostics 尚未运行，因此不能声称 routing advantage 成立或失败。

### 2.1 重要实验具体做了什么

| 实验 | 做的要点 | 解释作用 |
|---|---|---|
| Matched dense baseline | 用同等参数量的单个 dense replacement block 做 old-stage 和 new-stage adaptation | 排除“two-branch 只是参数更多” |
| Matched dense + replay | new-stage 适配时加入 old replay item，old replay token 数与 new support token 数匹配 | 检查 replay 是否已经足够减少 forgetting |
| Raw two-branch control | 不使用 projection split，两个 branch 都吃 raw hidden 或非特定分割输入 | 检查收益是否来自 two-branch 结构本身，而不是特定 band |
| Random split | 使用与目标 variance band 同维度的随机子空间 | 排除“只要随便投影/降维就有效”的解释 |
| Head16 split | 使用最高方差 common directions | 检查 adaptation 是否主要依赖 high-variance/common directions |
| u50 / ext / u50_ext split | 使用 middle band、extreme low-variance band、或二者组合 | 检查 frequency/variance-aware split 是否有真实优势 |
| Normalized projected split | 对 projected representation 做 LayerNorm 后再输入 branch | 检查 projected scale 是否导致 branch underfit |
| Full-tail-residual split | 移除 head16 后使用 residual representation | 检查非 high-variance 部分整体是否更适合作为 plastic input |
| Branch ablation | 移除 plastic branch，计算 loss 变化，并按 common/middle/rare token bucket 分桶 | 只能说明 branch contribution pattern，不能等同 expert specialization |
| Hidden-gradient conflict audit | 比较 old/new loss 对 hidden state 的 gradient cosine，并按 variance band 分桶 | 检查 forgetting 是否来自特定 subspace 的梯度冲突 |

### 2.2 当前最重要的解释修正

不能把 “middle/rare branch contribution 较大” 直接写成 “two-branch 已经专一化”。更严谨的说法是：

> Fixed split 在 middle/rare token bucket 上存在 contribution pattern，但它没有证明 selected expert 在 routed setting 中优于 counterfactual experts，也没有证明 CL forgetting 被降低。

因此，下一步必须引入 router audit，比较 learned routing、oracle routing、uniform mixture、flat raw MoE 和 random routing。

---

## 3. Main Hypothesis

**H-B-main:** $P(x-\mu)$ 及其 variance-band projection 暴露了某种 representation separability，但 fixed two-branch split 缺少 task-conditional routing 和有效 expert assignment，因此 separability 不会自动转化为 downstream / CL gain；需要通过 learned router 检验这种分离是否能变成可用的 functional specialization。

---

## 4. Three Sub-hypotheses

### H-B1: 表征“分得开”不等于任务“用得上”

Projection 或 variance-band split 可能提高 distribution separation / branch ablation contribution，但如果 task loss 主要依赖 raw common directions，或者 projected branch underfits，就不会带来 NTP / CL 收益。

### H-B2: 当前 CL setting 没有稳定 forgetting object

Phase8-H3 bridge 中 dense baseline 没有形成清晰 positive forgetting，且 old/new hidden-gradient conflict 多数不呈明显负冲突，因此不能直接评估 anti-forgetting claim。

### H-B3: Router 是下一阶段核心变量

如果 fixed split 失败但 branch contribution 在 middle/rare tokens 上仍有信号，那么下一步不是继续堆 split，而是做 routed expert：比较 learned routing、uniform mixture、oracle routing、flat raw MoE，并用 expert advantage / oracle regret 判断 routing 是否真正有用。

---

## 5. Router Audit 最小模型矩阵

| Model | 作用 |
|---|---|
| fixed two-branch | 保留当前固定 split，不做 learned routing，作为历史 baseline |
| uniform expert mixture | 有多个 experts，但平均混合或均匀使用，排除只是多 expert capacity |
| flat raw MoE | router 和 experts 使用 raw hidden，检查普通 learned routing 是否足够 |
| flat projected MoE using $P(x-\mu)$ | router 使用 projected representation，检查 $P(x-\mu)$ 是否是有用 routing signal |
| random-subspace routing | 使用同维随机投影做 router input，排除随机投影解释 |
| oracle routing | 用 token bucket / domain / source 等真实或诊断标签给出 routing 上界 |
| learned routing | 训练 router，检查 separability 是否能变成 selected expert advantage |

Router audit 的核心不是只看 route accuracy，而是看：

```text
selected expert advantage
oracle regret
router entropy
route-token bucket MI
NTP by common/middle/rare
matched parameter comparison
```

---

## 6. 当前 Claim Boundary

### 现在可以说

1. Fixed split 的 branch contribution 在 middle/rare tokens 上有可见 pattern。
2. 当前 CL stress setting 不足以支撑 anti-forgetting claim。
3. 下一步应转向 routing audit，而不是继续直接声称 two-branch 有 CL 价值。
4. $P(x-\mu)$ 类 reference representation 是一个候选 routing signal，但还不是已经验证的 expert input 或 router input。

### 现在不能说

1. 不能说 variance-band split 已经减少 forgetting。
2. 不能说 $u50_ext$ 或任何 projected split 是最佳 expert input。
3. 不能说 branch contribution 就等于 expert specialization。
4. Stage B 未运行前，不能说 routing advantage 成立或失败。
5. 不能说表征分得更开就必然能带来 downstream / CL gain。

---

## 7. 每日填写区

> 下面是每天必须更新的部分。

### 7.1 今日日期


### 7.2 今日核心问题


### 7.3 今日当前判断


### 7.4 今天具体推进了什么？


### 7.5 今天跑了哪些实验 / 改了哪些代码？

| 项目 | 内容 |
|---|---|
| split / projection |  |
| router |  |
| training |  |
| evaluation |  |
| cluster / acp / sco |  |

### 7.6 今天得到的关键指标

| 指标 | 数值 / 观察 | 解释 |
|---|---|---|
| NTP by common/middle/rare |  |  |
| selected expert advantage |  |  |
| oracle regret |  |  |
| router entropy |  |  |
| route-token bucket alignment |  |  |
| matched parameter count |  |  |
| old/new forgetting object |  |  |

### 7.7 今天哪个判断发生了变化？


### 7.8 当前卡点


### 7.9 明天最小下一步


### 7.10 需要问 AI / 导师的问题
