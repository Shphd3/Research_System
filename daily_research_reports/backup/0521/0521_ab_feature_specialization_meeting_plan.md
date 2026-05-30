# 0521/0522 组会前：AB Feature Specialization 诊断计划

## 一句话结论

导师真正要你先回答的不是“怎么设计更好的 MoE”，而是：**在最小可控的 feature-composition 世界里，普通 top-1 token-level MoE routing 到底能不能把 feature 分开；如果不能，它是把 A、B、AB 混成一个 token/context bundle，还是只是没有足够 evidence 让我们判断。**

---

## 1. 导师的核心意思

### 1.1 “I love New York City” vs “I hate New York City” 想说明什么？

这个例子不是在讲情感分析，也不是说 New York City 这个词本身变了。导师要说明的是：

> 在 causal LM 里，一个位置的 hidden state 不是裸 token identity，而是由历史上下文决定的 context-conditioned representation。

数学上可以写成：

$$
h_t = F_\theta(x_{\le t})
$$

router 看到的不是 token id，而是 hidden state：

$$
p(e \mid t) = \mathrm{softmax}(W_r h_t)
$$

所以同样是 “New York City”，在

```text
I love New York City
I hate New York City
```

里面对应的 hidden state 可能不同：

$$
h_{NYC}^{love} \ne h_{NYC}^{hate}
$$

因此 expert routing 也可以依赖历史：

$$
p(e \mid h_{NYC}^{love}) \ne p(e \mid h_{NYC}^{hate})
$$

这个例子是在反驳“expert routing 和历史无关”的直觉。导师的意思是：**如果 router 输入的是 Transformer hidden state，那 routing 理论上就是历史相关的。**

但这只说明“routing 可以依赖历史”，不说明“routing 一定学到了正确的 feature-level index”。这正是后面要实验验证的问题。

---

### 1.2 学长观点想说明什么？

学长的观点可以压缩成一小段：

> 当前普通 MoE 的 forward 是 token-level dispatch：一个 token 的整个 hidden vector 被送到一个或几个 expert。但这个 hidden vector 本身已经混合了很多 feature，例如 A、B、AB、位置、频率、上下文统计等。因此 top-1 MoE 并不是把“某个 feature”送给 expert，而是把“混合后的 token/context 表征”送给 expert。结果是 expert 很可能学到混合 bundle，而不是干净的 feature specialization。

换成公式：

$$
h \approx \alpha a + \beta b + \gamma ab + \epsilon
$$

普通 top-1 router 做的是：

$$
e^* = \arg\max_i w_i^\top h
$$

它选择的是一个 expert 来处理整个 $h$，不是把 $a$、$b$、$ab$ 分别送给三个 expert。

所以学长观点的核心不是“MoE 不行”，而是：**当前 MoE 的分发粒度可能错了：它分发 token representation，而不是分发 latent feature。**

---

### 1.3 Soft Routing / Top-3 到底是什么意思？

导师这里的表述确实有点混，但可以整理成清楚版本。

#### Top-1 routing

每个 token 只激活一个 expert：

$$
y = E_{e^*}(h), \quad e^* = \arg\max_i g_i(h)
$$

问题是：如果 $h$ 里面同时有 A、B、AB，那么 top-1 只能把整个混合表征交给一个 expert。

#### Top-k routing / Top-3 routing

Top-3 的意思通常是：每个 token 选择 router score 最大的 3 个 expert，然后加权求和：

$$
y = \sum_{i \in \mathrm{Top3}(g(h))} \alpha_i E_i(h)
$$

这里的 Top-3 是“一个 token 激活 3 个 expert”，不是“三个 token”，也不是天然等于“三个 feature”。

理想情况下，如果训练真的学到了 feature decomposition，那么一个 AB token 可能激活：

```text
expert_A
expert_B
expert_AB
```

这样就比较像 feature-level composition。

但关键边界是：**Top-3 只是提供了多个 expert 被激活的可能性，不保证每个 expert 对应一个 feature。**如果没有额外约束或诊断，Top-3 也可能只是三个混合 expert。

#### Soft routing

Soft routing 可以有两种含义：

1. 所有 expert 都被 soft weight 加权；
2. top-k experts 被 soft weight 加权。

导师在会议里更像是在说第二种：不是只把 token 丢给一个 expert，而是允许多个 expert 一起贡献，从而有机会把组合 feature 拆开。

但导师真正的意思是：**现在不要急着解决 Soft/Top-k；先诊断 top-1 普通 MoE 的问题是不是真的存在。**

---

## 2. 下一步真正的问题

抛开你最后提出的 AB / A-only / B-only 实验，导师真正想让你回答的问题应该是：

> 在最小可控的 feature composition setup 中，普通 top-1 token-level MoE routing 是否能形成 feature-level specialization？如果不能，它失败在 router assignment、expert function，还是 hidden representation 本身的 feature entanglement？

更短版本：

> top-1 MoE 是按 feature 分 expert，还是按混合 token/context bundle 分 expert？

这不是一个 architecture 问题，而是一个 mechanism diagnosis 问题。

---

## 3. 数学直觉：为什么 feature 会混合？

### 3.1 Transformer hidden state 是上下文的压缩

在 causal LM 中，位置 $t$ 的 hidden state 是：

$$
h_t = F_\theta(x_1, x_2, \dots, x_t)
$$

它必须服务 next-token prediction：

$$
\min_\theta -\log p_\theta(x_{t+1} \mid h_t)
$$

所以 $h_t$ 会倾向于保留一切对预测 $x_{t+1}$ 有用的信息。

如果当前样本里同时存在 A、B、AB 三种有用结构，那么 $h_t$ 很可能是叠加的：

$$
h_t \approx U_A z_A + U_B z_B + U_{AB} z_{AB} + \epsilon
$$

### 3.2 Top-1 router 只能切分整个 hidden state

top-1 router 本质上是在 hidden space 里做一个分区：

$$
e^*(h) = \arg\max_i w_i^\top h
$$

它不是先把 $h$ 分解成 feature，再路由每个 feature。它只看到一个混合向量。

因此 AB 样本如果同时含有 A、B、AB 信息，router 可能把它送到一个 expert，而这个 expert 的梯度会同时来自 A、B、AB 相关的预测需求。

### 3.3 “AB expert 包含 A 和 B”是什么意思？

不是说 expert 里面真的有三个可见变量，而是说：

- AB-dominant expert 接收的 hidden states 中，A/B/AB label 都可线性解码；
- mask 掉 AB-dominant expert 后，A-only、B-only、AB-composite 的 loss 都受影响；
- 该 expert 的 top activation directions 与 A、B、AB 三类 label 都相关。

这就说明这个 expert 不是纯 AB feature expert，而是混合 bundle expert。

---

## 4. 实验设计总览

### 总决策问题

> 普通 top-1 MoE routing 是否形成 feature-level specialization？

### 实验链条

```text
E0 数据 sanity
  -> E1 dense baseline 可学性
  -> E2 top-1 MoE routing specialization
  -> E3 representation entanglement diagnostic
  -> E4 expert intervention / causal ablation
  -> E5 optional top-k/soft routing comparison
  -> E6 gated retrieval alignment
```

E0-E4 是明天组会前最该讲清楚的主实验链条。E5/E6 是后续 gated steps。

---

## 5. Experiment Cards

# Experiment Card: E0521-AB-Feature-Specialization

## 1. Purpose / Main Reason

这个实验的目的不是直接证明 MoE 能加速 long-context attention，而是诊断：**普通 top-1 MoE 是否真的形成了可作为 index 的 feature-level specialization。**

如果 ordinary MoE 只是把混合 token/context representation 分到 expert，那么 expert bucket 不能直接作为 KV retrieval index 是合理的。

## 2. Mainline Position

当前主线是把 long-context attention 重写为 dynamic KV memory 上的 learned search：

```text
query token -> learned index / routing signal -> candidate KV tokens -> exact sparse attention
```

已有结果说明：oracle retrieval 有意义，但当前 router/expert bucket 对 dense attention winners 的 retrieval 不比 random matched 好。下一步瓶颈是弄清楚 expert bucket 为什么不是好 index。

本实验回答：**expert bucket 失败是否源于 feature-level specialization 根本没形成。**

## 3. Known Narrative / Premise

- attention 是 selective 的，所以需要 index；
- MoE expert id 可能是一个现成 index candidate；
- 但普通 MoE 是 token-level dispatch；
- token hidden state 可能包含多个 feature；
- 因此 expert 可能学到混合 bundle，而不是纯 feature。

## 4. Experiment Purpose

在一个最小 synthetic feature-composition setup 中，测量 top-1 MoE routing / expert function 是否按 A、B、AB feature 分离。

## 5. Hypothesis And Sub-Hypotheses

### H1: top-1 MoE routing 会 entangle features

AB-composite 样本的 dominant expert 会同时接收或表示 A-only、B-only 信息。

### H2: feature-level specialization 若存在，应表现为 routing 和 causal ablation 都按 feature label 分离

如果 AB 是独立 feature，那么 AB-dominant expert 被 mask 后应主要伤害 AB-composite，而不是同时大幅伤害 A-only/B-only。

### H3: load balance 不是当前主实验变量

因为当前目标是诊断 natural specialization，不是优化 expert utilization。load balance 只能作为后续对照。

## 6. Experiment Object

Controlled synthetic trigram / bigram-to-target dataset：

```text
A-only:       [A, r] -> y_A
B-only:       [r, B] -> y_B
AB-composite: [A, B] -> y_AB
background:  random -> random / distractor target
```

其中 $r$ 是非 A/B 的随机 token。

## 7. Experiment Paradigm

训练 dense baseline 和 top-1 MoE model，然后统计：

- feature class 到 expert 的 routing distribution；
- expert 到 feature class 的 purity；
- hidden state 中 feature label 的可解码性；
- mask expert 后各 feature class 的 loss change。

## 8. Expected Outcomes And Hypothesis Update Logic

### Outcome A: AB-dominant expert 同时包含 A/B/AB

解释：top-1 token routing 学到混合 bundle，不是 feature-level specialization。

Claim update：支持“当前 expert bucket 不适合直接作为 KV index，因为其 partition 不对齐 feature”。

### Outcome B: AB 和 A/B cleanly separated

解释：ordinary top-1 MoE 在这个可控 setup 中可以形成 feature-level specialization。

Claim update：下一步应测试这种 specialization 是否对齐 dense attention top tokens。

### Outcome C: routing 混乱但 dense baseline 成功

解释：任务可学，但普通 MoE routing objective 不足以诱导 specialization。

Claim update：后续可以考虑 top-k/soft routing 或 additional objective，但必须建立在这个 failure diagnosis 上。

### Outcome D: dense baseline 失败

解释：数据构造或模型容量有问题。

Claim update：不能对 MoE specialization 下结论。

## 9. What This Can Prove

- 在 controlled synthetic feature-composition setup 中，top-1 MoE 是否形成 feature-level specialization；
- 如果不形成，它是否表现为 feature entanglement；
- expert bucket 作为 index candidate 的一个局部失败原因。

## 10. What This Cannot Prove

- 不能证明 MoE routing 在真实语言中一定失败；
- 不能证明 load balance 一定有害；
- 不能证明 top-k/soft routing 一定能解决；
- 不能证明 long-context inference 可以加速；
- 不能把 synthetic feature 直接等同于真实语义。

---

# Execution Plan: E0521-AB-Feature-Specialization

## 1. Run Goal

用最小 synthetic setup 跑出三类图：

1. feature class × expert id routing heatmap；
2. expert purity / NMI / entropy；
3. expert mask 后 A-only / B-only / AB-composite 的 loss change。

## 2. Data Construction

Vocabulary:

```text
special tokens: A, B, y_A, y_B, y_AB
random tokens: r_i
```

Sample classes:

```text
A-only:       [A, r] -> y_A
B-only:       [r, B] -> y_B
AB-composite: [A, B] -> y_AB
background:  [r_i, r_j] -> y_bg or random target
```

Recommended controls:

- balance sample counts across A-only, B-only, AB-composite;
- include background distractors;
- vary frequency ratios in a later ablation, but not first run;
- keep sequence length short first, e.g. 3-token or 4-token pattern.

## 3. Model Setup

Models:

```text
Dense tiny Transformer baseline
Top-1 MoE tiny Transformer, no load balance
Optional: Top-3 MoE tiny Transformer, no load balance, only after top-1 result
```

Router position:

```text
Use hidden state at prediction position, i.e. after seeing [A, B] or [A, r] / [r, B].
```

## 4. Metrics

### Data learnability

```text
loss / accuracy by feature class
```

### Routing specialization

```text
P(expert | feature_class)
P(feature_class | expert)
routing entropy by feature class
expert purity
NMI(feature_class, expert_id)
```

### Entanglement

For AB-dominant expert $e_{AB}$:

```text
P(e_AB | A-only)
P(e_AB | B-only)
P(e_AB | AB-composite)
```

Probe diagnostics:

```text
linear probe: h -> has_A
linear probe: h -> has_B
linear probe: h -> is_AB
```

### Causal ablation

For each expert $e$:

```text
DeltaLoss_A-only(e) = Loss_A-only(mask e) - Loss_A-only(original)
DeltaLoss_B-only(e)
DeltaLoss_AB(e)
```

A pure AB expert should mostly increase AB loss. A mixed expert will increase multiple class losses.

## 5. Figures

Minimum figures for meeting:

```text
fig1_routing_heatmap.png
fig2_expert_purity_entropy.png
fig3_expert_mask_delta_loss.png
```

Optional:

```text
fig4_probe_accuracy_by_layer.png
fig5_svd_label_correlation.png
```

## 6. Pass / Fail Criteria

### Pass for diagnosis

Even if top-1 MoE fails, the experiment passes if it clearly distinguishes one of:

```text
feature-level separation
feature entanglement
routing collapse / no specialization
```

### Fail for diagnosis

The experiment fails if:

```text
dense baseline cannot learn the task
routing logs are missing
feature labels are ambiguous
the result cannot distinguish A/B/AB mixing from random noise
```

## 7. Agent Task Spec

Please implement and run `E0521-AB-Feature-Specialization`.

Required outputs:

```text
1. synthetic data generator with labels: A-only, B-only, AB-composite, background
2. dense baseline sanity result
3. top-1 MoE no-load-balance result
4. routing log per sample: feature_class, expert_id, router_logits, loss
5. metrics table: accuracy/loss by class, routing entropy, purity, NMI
6. figures:
   - feature class × expert id routing heatmap
   - expert purity / entropy plot
   - expert mask delta loss plot
7. short summary.md with result / interpretation / claim boundary
```

Do not add load balance in the primary run.
Do not start from top-k routing unless top-1 diagnostics are finished.
Do not claim real-language behavior.

---

## 6. 明天组会 30s 版本

> 我把问题重新压缩了一下：现在不是先做更复杂的 router，而是先诊断 ordinary top-1 MoE 是否形成 feature-level specialization。因为当前 MoE 是 token-level dispatch，一个 hidden state 里可能同时有 A、B、AB 等 feature，所以 expert 可能学到混合 bundle，而不是可作为 KV index 的干净 feature bucket。我会做一个最小 AB synthetic setup，先去掉 load balance，统计 feature class 到 expert 的 routing heatmap、expert purity，以及 mask expert 后 A-only/B-only/AB loss 的变化。如果 AB expert 同时影响 A/B/AB，就说明 top-1 MoE 没有把 feature 拆开；如果 AB 能干净分离，下一步再测这个 expert bucket 是否能帮助 dense attention retrieval。

---

## 7. 明天组会 1min 版本

> 现在主线还是 long-context attention as search：如果 attention 很 selective，就希望找到一个 learned index，从 KV memory 中先召回少量候选再做 exact attention。之前用 expert bucket 当候选 index 效果不好，所以我现在要诊断原因。导师提醒我，specialization 和 retrieval 要拆开：先问 expert 能不能 specialize，再问 specialization 能不能帮助 reverse index。
>
> 我现在把第一步问题改成：普通 top-1 MoE routing 是不是能形成 feature-level specialization？因为一个 token hidden state 本身是 context-conditioned 的，里面可能混了 A、B、AB 等多个 feature。top-1 routing 只是把整个 hidden vector 送给一个 expert，不是把每个 feature 分开发给 expert。所以我会做最小 AB synthetic task，包含 A-only、B-only、AB-composite。先不加 load balance，只看 natural routing。指标是 routing heatmap、expert purity/NMI、以及 mask expert 后不同 feature class 的 loss change。这个实验只证明 synthetic mechanism，不证明真实语言或速度提升；它的作用是判断 expert bucket 失败是不是因为 feature-level specialization 根本没形成。

---

## 8. 三小时执行与交付计划

当前日期：2026-05-21。明天组会日期：2026-05-22。

### 0:00-0:15 清空压力，只写一个问句

交付物：一行问题。

```text
在最小 AB synthetic setup 中，ordinary top-1 MoE routing 能否把 composite feature AB 从 atomic feature A/B 中分离出来？
```

规则：这 15 分钟不要读论文、不要想 load balance、不要想新 architecture。

### 0:15-0:40 写清导师逻辑

交付物：半页导师逻辑。

结构：

```text
attention 是 selective -> 需要 index
MoE expert id 可能是 index candidate
但普通 MoE 是 token-level dispatch
token hidden state 是 history-conditioned mixed representation
所以先诊断 expert 是否真的 feature-specialized
```

### 0:40-1:10 写数学直觉

交付物：三条公式。

```text
h_t = F(x_≤t)
p(e|t)=softmax(W_r h_t)
h ≈ a + b + ab + noise
```

目的：明天被问时，你可以把直觉落到数学对象上。

### 1:10-1:40 写 Experiment Card

交付物：purpose_card.md 初稿。

必须包含：

```text
Purpose
Mainline position
Hypothesis
Experiment object
Expected outcomes
What cannot be claimed
```

### 1:40-2:15 写 Agent Execution Plan

交付物：execution_plan.md 初稿。

必须包含：

```text
data generator
models
metrics
figures
pass/fail criteria
required artifacts
```

### 2:15-2:35 写组会口播

交付物：30s + 1min script。

要求：开头就是结论，不讲过程。

### 2:35-2:50 自我审计

检查 5 个禁止点：

```text
我有没有说 MoE 一定失败？不能。
我有没有说 synthetic 等于真实语言？不能。
我有没有把 top-k 当作已证明方案？不能。
我有没有把 load balance 当主问题？不能。
我有没有跳过 dense sanity？不能。
```

### 2:50-3:00 打包交给 Agent

交付物：复制 Agent Task Spec。

最低可交付版本只需要：

```text
one-sentence question
experiment card
execution plan
30s advisor script
```

---

## 9. What I should not say tomorrow

不要说：

```text
我们要证明 MoE 不行。
我们要证明语义是什么。
我们要解决 soft routing。
我们要加 load balance 改善 specialization。
这个实验能证明真实语言中也这样。
```

应该说：

```text
我现在只诊断 ordinary top-1 MoE 在 controlled feature-composition setup 中是否形成 feature-level specialization。
```

---

## 10. Claim Boundary

### Supported / grounded by meeting discussion

- 需要把 specialization 和 retrieval 分开验证；
- ordinary MoE 是 token-level dispatch；
- hidden state 是 context-conditioned representation；
- feature mixing 是当前需要诊断的核心机制问题。

### Weakly supported / pending experiment

- top-1 MoE 可能把 A/B/AB 混到同一个 expert；
- expert bucket retrieval 失败可能来自 feature-level specialization 不足。

### Unsupported

- MoE routing 一般无用；
- top-k/soft routing 一定解决问题；
- synthetic AB 结果能推出真实语言结论；
- expert specialization 存在就能带来推理加速。

---

## 11. Files to update

```text
daily_research_reports/0522/meeting/pre_meeting_pack.md
Projects/from-attention-to-search/XingyuD/main/experiments/E0521_ab_feature_specialization/purpose_card.md
Projects/from-attention-to-search/XingyuD/main/experiments/E0521_ab_feature_specialization/execution_plan.md
```

