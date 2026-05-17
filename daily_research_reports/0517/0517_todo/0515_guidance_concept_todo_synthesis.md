# 0515 研究指导：概念澄清 + 下次组会 Todo

## 一句话结论

0515 的主线不是“专家是否有语义标签”，而是：**数据中的重复上下文规则是否形成可读回的表征，并且 Gating 是否能把这些表征分发成可用于 reverse index / KV 压缩的 expert 分工；如果真实特征空间是 Zipfian/common-dominated，普通 MoE 为什么会失败，应该如何诊断。**

## Mainline update

**Yes, as framing update.** 不是实验结果更新，而是把问题从“semantic specialization”收紧为：

```text
data/event distribution
-> representation support
-> router assignment
-> expert update / causal contribution
-> reverse-index usefulness
```

## 1. 语言学概念 vs LLM Training 表征属性

### 1.1 不要把 linguistic concept 和 representation property 一一对应

| 层级 | 例子 | 在语言学里是什么 | 在 LLM training 里是什么 | 能否直接等同？ |
|---|---|---|---|---|
| Token / subword | `common`, `同`, `学`, `MoE` | 字符串切分单位 | embedding index + contextual hidden state 的输入单位 | 不能 |
| Word / morpheme | “同学”, “common” | 词/词素 | 可能被 tokenizer 拆成多个 token；模型未必有单独向量 | 不能 |
| Phrase / local pattern | “安瑞 是 个 好 同学” | 短语/局部构式 | 多 token context event；可形成 hidden-state feature | 不能直接，但可 operationalize |
| Syntax / construction | “今天下雨，所以要带伞” | 句法/因果/语用结构 | 条件预测中的上下文规则；可能分布在多层和多头 | 不能直接 |
| Semantic concept | “好人/学生/城市/下雨” | 人类语义类别 | 可能对应 hidden directions / clusters / probes / circuits | 必须通过 probe/intervention 证明 |
| Synthetic feature | `[1,2]->22`, `ABC` | 人工规则，不是自然语义 | 明确定义的 training event / motif | 可以作为 controlled proxy |

**关键定义：**

```text
linguistic concept = 人类定义的语言/语义/句法类别
training representation property = 模型在训练目标下形成的向量几何、方向、cluster、logit contribution、routing behavior
```

两者的关系只能是：

```text
linguistic concept
-> 在 corpus 中表现为某类 context/event distribution
-> 被 tokenizer 映射成 token sequence
-> 被 NTP loss 压成 hidden-state statistics
-> 可能被 probe / router / expert 使用
```

不能直接说：“一个 expert 负责某个语义概念”。最多先说：“某类被定义的 event / motif 在 hidden space 中可分，并且 router/expert 对它有可测行为。”

## 2. “一个 token 中的 common 部分”到底指什么？

这里的 `common` 不是 token 字符串里的某个子串，也不等于“通用语言学属性”本身。更准确地说：

```text
一个 token 的 common 部分
= 该 token 的 contextual hidden state 中，由大量 token/context 共享、频繁出现、训练更新充分、容易支配相似度匹配的表征成分。
```

它可能对应：

- 高频词/字/子词；
- 基础语法功能；
- 常见语义角色，如“好/坏/同学/人/城市”；
- 位置、格式、标点、转录模板；
- domain boilerplate；
- 训练目标下高频、低损失、强共享的 latent directions。

所以 `common` 是 **representation support / update budget / shared direction** 的概念，不是纯语言学概念。

更严格的写法：

```text
common component = high-support shared representation component
specialized component = lower-support, feature/context-specific representation component
```

需要用实验定义它，例如：

```text
common direction: across many features/tokens has high activation or high variance
specialized direction: feature-conditional activation high, other contexts low
common-dominated matching: cosine/QK/router score mostly explained by common direction
```

## 3. 共识信息中三点的关系

组会笔记中的三点可以重写成一个因果链。

### 点 A：每个 token hidden state 都混合 common + specific

原表述：

```text
每一个 Token 之中都有一些“语义中” common 的信息
```

修正表述：

```text
每个 contextual token representation 通常包含 shared/common 成分和 context-specific 成分。
```

这不是说 token 本体有固定语义组件，而是说经过上下文层后，$h_t$ 同时携带通用语言结构和局部任务/语义/上下文信息。

### 点 B：普通 MoE expert 也可能被 common 成分污染/支配

原表述：

```text
现有 MoE 架构每个 Expert 里面都有一些 Common 的特征，并且被 Common Dominate
```

修正表述：

```text
如果 router 没有显式分离 common 与 specialized directions，那么每个 expert 接收到的训练样本都会包含大量 common 成分；expert 内部计算也会学习这些高频共享成分，导致 experts 之间冗余，specialized signal 被淹没。
```

这解释了为什么普通 MoE 的 specialization 可能不够“干净”：它可能只是按 token ID、频率、hidden norm、early routing history 或 loss-compatible shortcut 分配，而不是按我们定义的 feature 分配。

### 点 C：真实特征空间可能是 Zipfian / hierarchical，因此 reverse index 需要 common-specialized 分解

原表述：

```text
特征空间是 Zipfian 分布，我们要构建一种适应这种数据分布的 H-MoE 模型。
新来一个 token，新的 token 肯定和 common 匹配，然后和一些 specialized experts 匹配。
```

修正表述：

```text
如果 feature/event distribution 是长尾的，common features 会出现在几乎所有 token/expert 中，tail features 出现少但检索时很关键。若 reverse index 用 common-dominated expert id 匹配 token，会优先匹配 common，而不是真正区分 tail/specific feature。因此架构需要把 common path 与 specialized path 分开，或者让 gating 显式避免 common directions 支配 routing。
```

三点合在一起是：

```text
token representation is mixed
+ expert computation is mixed
+ feature/event frequency is long-tailed
=> common directions dominate router/reverse-index similarity
=> ordinary MoE bucket may not be a useful sparse KV index
=> need diagnose gating failure before proposing H-MoE
```

## 4. Zipf 到底指什么？

最安全定义：

```text
Zipf = 对某种已定义单位做 rank-frequency 统计后，少数高频单位占大质量、多数低频单位形成长尾。
```

它不是天然只指“语义”。它可以指：

| 统计对象 | 是否可直接数 | 对 LLM/MoE 的意义 |
|---|---:|---|
| word frequency | 可数，但中文需分词 | 经典语言学 Zipf |
| subword/token frequency | 可数 | LLM 训练实际看到的离散单位 |
| character/byte frequency | 可数 | byte/char 模型或 tokenizer 下界 |
| phrase/n-gram frequency | 可数 | 局部上下文/短语模式 |
| syntactic construction frequency | 需 parser/template | 句式/构式层面的 Zipf |
| semantic concept frequency | 需 label/ontology/probe/cluster | 不能从 raw corpus 直接得到 |
| synthetic feature/motif frequency | 可数，因为我们定义了 motif | E2 中 ABC/DEF/GHI/JKL 就属于这个 |

因此你组会里应该说：

> 我们不能直接声称“语义是 Zipfian”。我们能先测 token / n-gram / motif/event 的 Zipf。对于真实语义 feature，必须先定义 extractor 或 probe，才能谈它的分布。

## 5. 导师的真实要求

忽略情绪，0515 导师的核心要求是三件事。

### 要求 1：先证明最简单的 specialization 能做出来

录音锚点：研究指导原文 00:04-03:36，多次追问“能不能训出 specialized MoE”。

导师想听到的不是复杂架构，而是：

```text
在最简单 uniform synthetic feature 数据上，现有/标准/前人 MoE 方法是否能让 ABC、DEF 等 feature 分到可解释 expert？
```

**Todo 实验 A：Uniform Feature Specialization Reproduction**

- 数据：ABC、DEF、GHI、JKL 均匀出现；先不要 Zipf。
- 模型：flat top-1 MoE；必要时复现前人 gating / center-style / cosine-routing 方法。
- 指标：feature readback、P(expert|feature)、NMI/ARI、dominant expert ablation、forced-routing utility matrix。
- 判据：不是必须 one-feature-one-expert，但至少要说明能否形成可读回、可干预的 feature-expert alignment。

### 要求 2：在 uniform feature 成立后验证 reverse index 是否 work

录音锚点：研究指导原文 14:26-15:14。

导师给的顺序是：

```text
先 uniform feature
-> 再看 reverse index work 不 work
-> work 后再说真实世界 Zipfian 对架构有新要求
```

**Todo 实验 B：Uniform Reverse Index Proof-of-Work**

- 数据：uniform ABC/DEF/... sequential features。
- Index：用 expert id / routing bucket 建 candidate KV set。
- Attention：final exact QK reranking。
- Baseline：random matched candidates、oracle feature candidates、dense attention top-M。
- 指标：dense-attention top-key recall@M、attention mass recall、output reconstruction error、target readback drop。
- 判据：如果 expert bucket 不能优于 random matched candidates，不能声称 MoE routing 可作为 KV reverse index。

### 要求 3：进入 Zipf/common-dominated case，解释普通 gating 为什么会失败

录音锚点：研究指导原文 07:31-09:52；笔记中 Gating Failure 机制 019-024。

导师真正关心的是：

```text
当 token 和 expert 都包含 common 成分，且 common dominates similarity/routing 时，普通 MoE reverse index 为什么不准？
```

**Todo 实验 C：Gating Failure Mode / Training Dynamics**

- 数据：先 uniform，再 Zipf frequency sweep；加入 common feature + specialized feature 的可控组合。
- 诊断变量：feature_id、prefix-end token、target token、frequency band、hidden norm、router logit margin、CE difficulty、expert utility。
- 训练过程：保存 early checkpoints，观察 routing 是否早期固化。
- 干预：oracle feature router、common feature ablation、router supervised auxiliary、shared common expert。
- 判据：明确 linear router 到底按什么分；如果 feature 可分但 router 不用，就支持 `representation separability != router specialization`。

### 补充要求：一学就会 / data efficiency

学长讨论原文 10:44-15:48 提到另一个方向：如果数据被送到合适 expert，如何从理论和工程上让 expert 更 data-efficient / aggressive update。这个不是下一步最小主线，但可以作为后续分支：

```text
right expert assignment -> lower effective complexity / lower VC burden -> larger safe update / less interference -> one-shot or few-shot adaptation
```

现在不要把它放在第一优先级；先钉死 gating failure。

## 6. 下一次组会 30 秒版本

我现在把问题收紧了：我们不再直接说 expert 有语义分工，而是先证明数据中的 repeated context feature 是否能形成可读回表征，并驱动 MoE gating。E2 已经显示 feature 在 router input hidden space 中可分，但 learned linear router 没有强烈沿 feature-difference direction 切分，所以 `representation separability != router specialization` 是当前最稳结论。下一步我会做三个最小实验：第一，在 uniform feature 数据上复现最简单的 feature-expert specialization；第二，在 uniform case 验证 expert bucket 能不能作为 reverse index retrieve KV；第三，再进入 Zipf/common-dominated setting，分解 router 到底按 token shortcut、hidden norm、loss difficulty 还是 expert utility 进行分发。

## 7. What cannot be claimed

不能 claim：

- 真实 LLM expert 已经按语义分工；
- synthetic ABC/DEF feature 等价于自然语言 semantic concept；
- Zipfian token frequency 等价于 Zipfian semantic feature；
- router alignment 等价于 expert causal mechanism；
- 当前 MoE bucket 已可作为可靠 KV reverse index；
- H-MoE 已被证明优于 flat MoE。

## 8. 最弱/最容易被攻击点

最弱点是：**“真实语言中的 feature 是 Zipfian”还没有 operational definition。**

必须拆成：

```text
token Zipf: 可直接测
n-gram/phrase Zipf: 可直接测但只是 surface form
semantic/construction Zipf: 必须先定义 extractor/probe/label
training feature Zipf: 在 synthetic data 中可控定义
```

## 9. Suggested file updates

Files to update:

- `daily_research_reports/0517/meeting/meeting_recap.md`: 记录 0515 导师真实关切和三条 todo。
- `daily_research_reports/0517/experiment_analysis.md`: 加入 E0 tokenizer distribution audit 的结论边界。
- `Projects/MoE-Continual-Learning/main/01_current_state.md`: 更新主线为 `data/event distribution -> representation -> gating -> expert causal contribution -> reverse index`。
- `Projects/MoE-Continual-Learning/main/next_iteration_plan.md`: 加入 Uniform specialization、Uniform reverse-index、Gating failure decomposition 三个实验。
