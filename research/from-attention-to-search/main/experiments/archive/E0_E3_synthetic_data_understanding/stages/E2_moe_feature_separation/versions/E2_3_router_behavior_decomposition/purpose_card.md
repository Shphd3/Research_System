# Experiment Card: E2.3 Router Behavior Decomposition

## 1. Purpose / Main Reason

E2.3 的目的，是解释 E2 中最重要的反常现象：

```text
feature representation 已经在 router input hidden space 中可分，
但 learned router 没有沿这些 feature-separating directions
形成 clean one-feature-one-expert routing。
```

换成中文说：

```text
模型内部似乎已经能区分 ABC / DEF / GHI / JKL，
但专家选择器没有把这四类上下文规则干净分给四个 experts。
```

E2.3 不再继续证明“模型是否学到 feature”。这个问题 E1/E2 已经有支持证据。E2.3 要回答的是：**router 到底按照什么依据选择 expert？**

## 2. Term Definitions

为了避免术语混乱，本实验先固定以下定义。

- 人工特征 / 序列规则 / feature：数据里人为种下的规则，例如 `[1,2] -> 22`。它是数据层面的结构。
- 表征 / hidden state / representation：模型在某个位置产生的向量，例如 `[1,2]` 中 `2` 位置的 hidden state。它是模型内部状态。
- router / 专家选择器：MoE 中决定当前 token 送给哪个 expert 的小模块。
- expert / 专家：MoE 中的一个 FFN 分支。
- expert choice / expert id：router 最后选择的 expert 编号。
- feature-expert alignment：同一个 feature 的样本更常被分到同一个 expert，且不同 feature 的 expert 分布有差异。
- clean one-feature-one-expert：每个 feature 基本对应一个不同 expert。这是强版本，不是 E2 当前已经证明的结论。
- shortcut / 捷径变量：不是完整上下文规则本身，但可能足够帮助 router 做选择的变量，例如 prefix-end token、hidden 向量大小、样本难度、预测置信度。

## 3. Mainline Position

E2.3 位于 synthetic data understanding 线的 MoE 解释阶段。

前面推理链条是：

```text
E0: 构造干净 all-trigram synthetic corpus，确认 collision 很低。
E1: dense Transformer 能读回 trigram features，shuffled unigram control 失败。
E2.0: MoE 能读回 features，并出现 feature-expert alignment。
E2.1: feature identity 在 router input hidden space 中仍可分，但 router boundary 不沿 feature-difference directions。
E2.2: 降低 expert 容量或增加 feature 数量，没有强制产生更 clean 的 feature-aligned routing。
E2.3: 直接解释 learned router 的 expert choice 到底由什么变量决定。
```

所以 E2.3 是一个解释性实验，不是扩大规模实验。

## 4. Known Narrative / Premise

当前可以作为前提使用的证据：

- all-trigram 数据中的人工序列规则可以被模型读回；
- shuffled unigram control 不能读回这些规则，说明主要信号不是单个 token 频率；
- MoE 的 routing 与 feature label 有 alignment；
- dominant expert ablation 在 E2.0 中会伤害对应 feature readback；
- E2.1 显示 feature representation 在 router input 中仍可分；
- E2.1 同时显示 router boundary 与 feature-difference direction 对齐很弱；
- E2.2 显示仅降低 expert 容量或增加 feature 数量，不会自然推出 clean one-feature-one-expert。

这些前提共同指向一个问题：

```text
router 并不是简单地“看到 feature 可分，就按 feature 分 expert”。
```

## 5. Experiment Purpose

本实验的局部目的，是把 router 的 expert choice 当作要解释的对象，比较几类可能解释：

1. 是否主要由 feature identity 解释；
2. 是否主要由 prefix-end token 或 target token 这种 token shortcut 解释；
3. 是否主要由 hidden 向量大小、激活尺度、预测难度或预测置信度解释；
4. 是否主要由 router 自己权重敏感的 hidden directions 解释；
5. 是否 feature prediction 本来就不依赖 clean expert partition。

一句话：

```text
E2.3 要找出 router 选择 expert 的真实依据。
```

## 6. Hypothesis And Sub-Hypotheses

H2.3 主假设：

```text
feature representation 可分，不等于 router 会按 feature representation 分 expert。
```

子假设：

H2.3a：router 主要按人工 feature 分 expert。  
如果成立，`feature_id` 应该最能解释 expert choice，并且控制 token、向量大小、预测难度后仍然有效。

H2.3b：router 主要按 token shortcut 分 expert。  
如果成立，prefix-end token 或 target token 对 expert choice 的解释力会接近或超过 feature_id。

H2.3c：router 主要按 hidden scale / difficulty 分 expert。  
如果成立，hidden 向量大小、目标 token 预测概率、loss、logit margin 等变量，比 feature_id 更能解释 expert choice。

H2.3d：router 使用的方向不是 PCA 上最显眼的 feature-separating directions，而是 router 权重敏感的 hidden directions。  
如果成立，feature 在 PCA 上可分，但 expert choice 更容易被 router projection 或少数 hidden dimensions 解释。

H2.3e：feature prediction 不需要 clean expert partition。  
如果成立，feature-oracle routing 不会显著提高 NTP loss/readback，random 或 mean-replaced expert path 也不会严重破坏 feature prediction。

## 7. Experiment Object

实验对象不是新数据结论，也不是重新证明 E2。实验对象是：

```text
E2 trained MoE checkpoint 中，每个样本的 router input hidden state
与 learned top-1 expert choice 之间的关系。
```

主要分析位置：

```text
[A,B] -> C
   ^
   B 位置负责预测 C，所以读取 B 位置的 router input hidden state。
```

## 8. Experiment Paradigm

本实验采用“解释变量竞争”的范式。

把 `selected_expert` 当成要解释的标签，然后分别测试：

- 只看 feature_id，能不能预测 expert；
- 只看 B token，能不能预测 expert；
- 只看 target token，能不能预测 expert；
- 只看 hidden norm / loss / confidence，能不能预测 expert；
- 只看 PCA coordinates，能不能预测 expert；
- 只看 router projection，能不能预测 expert；
- 把这些变量放在一起后，哪个变量仍然有独立解释力。

如果 feature representation 可读出，但 expert choice 不是由 feature_id 最好解释，那么就支持：

```text
模型知道 feature 不同，但 router 没有按这些差异分 expert。
```

## 9. Expected Outcomes And Hypothesis Update Logic

### Outcome A: feature_id 最强

说明 router 确实主要按人工 feature 分 expert。  
更新：E2 的问题不是“不按 feature 分”，而可能是 feature-to-expert 映射不够一一对应，或多个 features 共享 expert。

### Outcome B: B token 或 target token 最强

说明当前 routing 可能主要来自 token shortcut。  
更新：E2 的 feature-expert alignment 需要降级解释，不能直接说是 relation-level feature specialization。下一步必须做 shared-B crossed-feature control。

### Outcome C: hidden norm / loss / confidence 最强

说明 router 可能按“样本强弱、难度、置信度”分 expert。  
更新：router 更像 difficulty / confidence allocator，而不是 feature classifier。

### Outcome D: router projection 最强，而 PCA / feature centroid 不强

说明 router 使用的是自己权重敏感的方向，不是人眼在 PCA 图上看到的主方向。  
更新：PCA 可分不能推出 router boundary 会使用这些方向。

### Outcome E: feature-oracle routing 不改善 readback 或 CE

说明 clean one-feature-one-expert 对当前 NTP 任务不是必要解。  
更新：router 没有这样分，可能不是失败，而是当前优化目标没有要求它这样分。

## 10. What This Can Prove

E2.3 可以在 toy all-trigram setting 中判断：

- expert choice 是否主要由人工 feature 解释；
- feature_id 的解释力是否只是 token shortcut 的副产品；
- router 是否更依赖 hidden scale、预测难度、置信度或 router-specific directions；
- feature representation 可分是否真的没有转化为 router specialization。

如果结果满足“feature probe 高，但 feature_id 不能解释 expert choice”，E2.3 可以支持：

```text
representation separability does not imply router specialization.
```

中文表达：

```text
表征空间里能区分，不等于 router 会按这种区分来分专家。
```

## 11. What This Cannot Prove

E2.3 不能证明：

- 真实 LLM 的 experts 是否语义分工；
- 所有 MoE router 都不会按 feature 分工；
- synthetic trigram feature 等价于自然语言语义；
- router 不能用于任何检索或索引任务；
- PCA direction、router direction、semantic direction 三者存在普遍对应关系。

## 12. Result

TBD.

## 13. Conclusion

TBD.

## 14. Next Step

如果你认可该 plan，下一步执行 E2.3-A：先不重训，只读取 E2 checkpoint，做 router behavior decomposition。

如果 E2.3-A 显示 token shortcut 风险很高，再进入 E2.4 crossed-feature control，例如：

```text
[1,2] -> 22
[3,2] -> 23
```

这样可以强制模型必须看完整 context relation，而不能只看 `B=2`。
