# 0513 Purpose-First Experiment Cards - Synthetic Data Understanding

## 0. 总的抽象目的

建立学习的直觉，构建稳定的科研思路链条。

这组实验不是先证明 MoE 或 router 有用，而是先让我们在做实验前把脑子稳住：

- 我们构造的 synthetic 数据到底有什么可学习结构？
- Transformer dense FFN 会如何学习不同频率的重复表征？
- Transformer MoE 是否会把这些表征分开？
- synthetic 数据和真实语言数据的统计结构有哪些相同与不同？

## 1. 已知叙述 / 基于的知识

语言是 sequence。语言里的意义由上下文决定，而不是由孤立 token 决定。

因此，在 toy synthetic 数据中，feature 不应该被定义成单个 token，而应该定义成重复出现的上下文关系：

```text
A -> B
C D -> E
```

如果一个模型真的学到了 feature，它不只是整体 loss 下降，而应该在对应上下文上提高目标 next-token 的概率，并在内部表征、FFN activation 或 MoE routing 中留下可诊断的结构。

## 2. 实验逻辑链

```text
构建 controlled synthetic sequence
-> 审计数据中是否真的有目标 pattern / frequency / collision
-> 训练 dense Transformer 做 next-token prediction
-> 分析 dense FFN 是否学到不同频率 feature
-> 训练 Transformer MoE 做同一任务
-> 分析 MoE 是否把不同 feature 分到不同 expert
-> 比较 synthetic 数据和真实数据的统计特征
```

核心顺序：先理解数据，再理解 dense model，再理解 MoE。

## 3. 总研究问题

通过这组实验，我们最终想知道：

> 不同频率、具有特定上下文语义的表征，在 Transformer FFN 和 Transformer MoE 中是怎么被学习和分开的？模型学到这些表征时，外部预测和内部机制分别表现成什么？

---

## Experiment E0: Synthetic Data Sanity

### 1. Purpose / Main Reason

先确认 synthetic corpus 真的包含我们设计的 sequential features。否则后续 dense FFN、MoE specialization 或 router retrieval 的结果都不可解释。

### 2. Hypothesis To Decide

H0: synthetic 数据中存在受控的 pattern-level feature；这些 feature 以设定频率重复出现，而随机背景只产生可记录的 accidental collision。

### 3. Data And Task Construction

数据是 token sequence，不训练模型。

构造三类 corpus：

- random-only control：全随机 token，用于估计背景 collision。
- one-feature corpus：在随机背景中插入 `[A,B]`。
- four-feature corpus：插入 Zipf-like 频率的 `[A,B]`、`[C,D,E]`、`[F,G]`、`[H,I]`。

### 4. Metrics

- 每个 feature 的 target count vs actual count。
- background collision count。
- empirical $P(\text{next token} \mid \text{prefix})$。
- feature-context entropy vs random-context entropy。
- feature rank-frequency plot。

### 5. Decision

只有 E0 通过，才进入 dense NTP。若低频 planted feature 与随机 collision 同量级，则数据不干净，不能用来解释模型学习。

---

## Experiment E1: Dense Transformer Feature Readback

### 1. Purpose / Main Reason

在随机背景没有稳定语义的 synthetic 数据中，测试传统 dense Transformer 是否能从重复出现的上下文 feature 中学到稳定表征。

### 2. Hypothesis To Decide

H1: 在传统 Transformer 中，FFN 更倾向于学习训练数据中高频出现的 feature；feature 频率越高，其在 FFN 中形成的表征越稳定、越可分，对模型输出的因果影响越大。

细化假设：

- H1a: 高频 feature 的 $P_\theta(\text{target} \mid \text{prefix})$ 高于低频 feature。
- H1b: 高频 feature 在 hidden state / FFN activation / logit-delta 中形成更稳定、更可分的方向。
- H1c: feature-context 的有效秩低于随机背景，主要可学习信号来自 planted repeated patterns。

### 3. Experiment Question

给定随机背景中重复出现的若干 feature，dense Transformer 能否在 NTP 任务中读出这些 feature，并把它们和随机背景区分开？

### 4. Data And Task Construction

数据：

- vocabulary size: $V=100$。
- corpus: random background + planted sequential patterns。
- feature frequency: high / medium / low / very low。

任务：

```text
input prefix: A
target: B
```

训练范式：next-token prediction。

测试重点：特定 feature prefix 上预测 target token 的准确度、概率和 logit margin。

### 5. Model / Analysis Setup

模型：小型 dense autoregressive Transformer，结构为 Transformer + FFN。

分析：

- per-feature CE / accuracy。
- $P_\theta(\text{target} \mid \text{prefix})$。
- logit margin。
- hidden state / FFN activation / logit-delta 的 SVD 或 effective rank。
- feature-context 与 background-context 的表征可分性。

### 6. Expected Outcome

如果 H1 成立，dense FFN 的可学习信号应接近低秩：主要由我们植入的重复 feature 解释；高频 feature 更稳定、更可分，对输出影响更大。

如果 loss 下降但模型不能在 feature prefix 上输出 planted next token，则不能说模型学到了 feature。

### 7. What This Cannot Prove

不能证明 MoE 会 specialization。
不能证明真实语言数据里有同样干净的 feature。
不能证明 router bucket 能作为 KV retrieval index。

---

## Experiment E2: Transformer MoE Feature Separation

### 1. Purpose / Main Reason

在同一个受控 synthetic 世界中，测试 Transformer MoE 是否能把不同上下文 feature 分到不同 expert，而不是只学 token frequency 或 load balance。

### 2. Hypothesis To Decide

H2: 在 Transformer MoE 中，router / expert 会通过 next-token loss 学到不同 feature 的分离结构；如果 feature identity 是主要可学习机制，则不同 feature 应该表现出不同 expert preference。

细化假设：

- H2a: $P(\text{expert}=e \mid \text{feature}=f)$ 对不同 feature 有明显差异。
- H2b: $P(\text{feature}=f \mid \text{expert}=e)$ 显示 expert purity 高于 random routing。
- H2c: 若 MoE 只跟随 token frequency 或 load balance，则 feature-expert alignment 会弱或不稳定。

### 3. Experiment Question

在四个 planted feature 和四个 expert 的容易设定下，MoE 是否能学到 feature-level separation？

### 4. Data And Task Construction

数据：使用 E1 中已通过审计、且 dense model 可读出的 four-feature corpus。

任务：next-token prediction。

训练：Transformer + MoE FFN，top-1 routing 优先，top-2 routing 可作为后续消融。

### 5. Metrics

- Expert purity: $P(\text{feature}=f \mid \text{expert}=e)$。
- Routing concentration: $P(\text{expert}=e \mid \text{feature}=f)$。
- NMI / ARI between feature ID and expert ID。
- Per-feature next-token accuracy。
- Expert load distribution。
- Seed stability。

### 6. Expected Outcome

强支持：接近 one-to-one feature-expert mapping，NMI 高，并且跨 seed 稳定。

弱支持：routing 好于 random，但 mixed，需要进一步分析 frequency、load balance 和 token identity leakage。

不支持：routing 主要由 token frequency 或 load balance 决定，而不是 feature identity。

### 7. What This Cannot Prove

不能证明真实 LLM 中的 MoE expert 也按语义 feature 分工。
不能证明 H-MoE 更好。
不能证明 MoE routing 与 dense attention winners 对齐。

---

## Experiment E3: Synthetic vs Real Data Statistics

### 1. Purpose / Main Reason

比较 synthetic 数据假设和真实语言数据统计之间的相同与不同，避免把 toy 结果直接误认为 real data 结论。

### 2. Hypothesis To Decide

H3: 真实语言也包含 repeated sequential patterns 和 heavy-tailed popularity，但真实数据的 hierarchy、ambiguity 和 context dependence 会比 toy synthetic 数据复杂。

### 3. What To Compare

- n-gram / phrase rank-frequency distribution。
- conditional entropy $H(x_{t+1}\mid x_{t-k:t})$。
- high-confidence contexts 的比例。
- repetition / burstiness。
- subpattern 与 phrase 的共现结构。

### 4. Decision

不要先问 “synthetic model 能不能迁移到 real data”。先问：

> synthetic generator 捕捉到了真实数据的哪些统计属性？哪些没有捕捉到？

---

## 与旧版 0513 实验卡的区别

旧版 0513 更像按 E0-E4 顺序排列的实验清单：数据审计、one-feature dense、four-feature dense、MoE、hierarchical phrase。

新版改成目的主因文档：

- 先写总目的：建立学习直觉和稳定科研思路链条。
- 先写已知叙述：语言是 sequence，意义由上下文决定。
- 明确总研究问题：不同频率的上下文 feature 在 FFN / MoE 中如何被学习和分开。
- 把 E1 dense 和 E2 MoE 写成主实验，而 E0 是前置数据审计。
- 每个实验都从 Purpose / Main Reason 开始，而不是直接从 Hypothesis 或 Setup 开始。

结论：新版更适合作为“实验前稳定脑子”的目的主因卡；旧版更适合作为执行清单或拆分到 detailed execution plan。
