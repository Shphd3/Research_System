According to a document from 2026-06-23 and the June 8–10 handoff, my judgment is:

## Verdict

**07 支线不是抛弃旧的 initialization / anti-collapse 线，而是把它升级成“gating 是否能产生有因果价值的 expert specialization”的主线。**

旧线回答：

> router 为什么从随机初始化进入 collapse？怎样避免 early common-logit lock-in？

新 07 线回答：

> 即使避免了 collapse，expert partition 是否真的减少 feature interference、提高有效特征容量？

所以关系是：

```text
旧线 = 进入 specialization basin 的前置条件
新 07 线 = specialization 是否有研究价值的主问题
```

你们已有结果说明：slot 信息在 routed hidden state 中，slot-specialization 也可达；失败主要是 common component 在 router score 中形成 effective bias，并被 top-1 训练放大。common-logit cancellation 能显著提升 slot_NMI，同时保持 accuracy。 

---

# 1. 旧线和新线的明确关系

## 旧线：collapse / initialization line

它的对象是：

```text
uniform feature
random dot-product router
early top-1 collapse
common-logit bias
anti-lockin
```

核心模型是：

$$
h_f = c + r_f
$$

router logit：

$$
z_{f,e}=w_e^\top h_f=w_e^\top c+w_e^\top r_f
$$

其中 $w_e^\top c$ 是 feature-independent 的 expert effective bias。旧线已经说明：即使 feature frequency 均匀，hidden state 也不一定 zero-mean，common component 会导致 step-0 dominant expert。

旧线的成功标准是：

```text
random-init router 能否不被 common-logit 劫持，
并进入 slot-to-expert specialization basin。
```

---

## 新 07 线：expert specialization / gating line

它的对象是：

```text
组合 feature
common / rare conflict
expert partition
semantic routing
feature interference
causal utility
```

第二篇文档的核心要求是：expert partition 不能只增加参数量或路由熵，而要减少跨 feature 干扰；否则只是把 dense 表示塌缩转移到 expert 层面。

新线的成功标准是：

```text
expert routing 是否让冲突 feature 分开，
让相关 feature 可控共享，
并在因果测试中降低 interference。
```

---

## 二者关系一句话

```text
旧线解决：gate 能不能别一开始就塌。
新 07 线解决：gate 不塌以后，分出来的 expert 是否真的有语义和因果价值。
```

因此旧线不是过时，而是 07 支线的 **entry-condition module**。

---

# 2. 07 支线的 Decision Question

建议 07 支线的第一个 decision question 写成：

```text
在组合 feature 与 common/rare conflict 数据中，
label-free common-controlled gate 是否能从 random init 进入稳定的 semantic expert partition，
并比 dense / balance-only MoE 更少发生 feature interference？
```

这里每个词都有约束：

| 词                         | 含义                                       |
| ------------------------- | ---------------------------------------- |
| label-free                | 不用 slot label、不用 oracle slot centroid    |
| common-controlled         | 延续旧线：避免 common-logit early lock-in       |
| semantic expert partition | 相关 feature 路由相近，冲突 feature 路由分离          |
| feature interference      | 一个 feature 的训练、消融或高增益子空间移除会伤害另一个 feature |
| dense / balance-only MoE  | 必须有反事实对照，不能只和坏 baseline 比                |

---

# 3. Physical Priors

## Prior 1：router 输入里有 common component

```text
h_f = c + s_f + \epsilon_f
```

* $c$：跨 feature 共享成分；
* $s_f$：真正区分 feature 的成分；
* $\epsilon_f$：噪声或其他残差。

旧线说明，$c$ 会通过 $w_e^\top c$ 形成 expert-specific effective bias，主导 early routing。

**含义**：
07 线不能直接研究“expert 是否 specialize”，必须先保证 router 没有被 common direction 劫持。

---

## Prior 2：load balance 不是 specialization

一个 gate 可以很 balanced，但每个 expert 仍然没有语义分工。

第二篇文档明确把 gating 的三约束拆成：

```text
balance + semantic consistency + stability
```

即：专家要有足够数据，相关 feature 要路由到相关专家，小扰动不能随机改变路由。

**含义**：
07 的 primary metric 不能再是 max_load 或 entropy，而要是 semantic + causal 指标。

---

## Prior 3：MoE 的价值不是“分 token”，而是“降低冲突”

导师文档里的 expert partition 不是为了让 token 均匀散开，而是为了避免所有 feature 经过同一个 global high-gain subspace。理想情况是：不同专家拥有局部子空间，减少 common feature 和 rare feature 的竞争。

**含义**：
07 数据集必须引入 conflict；继续只做 uniform independent feature，不足以回答导师问题。

---

## Prior 4：好的表示应是“受控复用”，不是完全正交

第二篇强调：好表示不是最大各向同性噪声，而是“分布式容量 + 受控复用”；相关 feature 可以共享，但无关或冲突 feature 不应全部挤进同一个 top 子空间。

**含义**：
07 不应该追求所有 feature 都分到不同 expert。应区分：

```text
shared parent feature: 可以共享
conflict extra feature: 应该分离
unrelated feature: 不应强耦合
```

---

## Prior 5：expert partition 也可能只是转移 collapse

如果 gate 把大量 token 送到少数 experts，或者每个 expert 内部仍形成高增益塌缩，那么 MoE 没有真正解决问题。第二篇把这列为主要风险。

**含义**：
07 必须同时测：

```text
global routing collapse
per-expert internal spectral collapse
causal feature utility
```

---

# 4. 初步 07 Anchor 草稿

## Anchor 07: Common-Controlled Semantic Gating for Expert Specialization

### Thinking Card
**07 支线研究：在避免 common-logit early collapse 的前提下，gating 是否能形成稳定、语义一致、能降低 feature interference 的 expert specialization。**

---

## 0. Current State

已有旧线结论：

1. uniform feature frequency 不保证 router 输入均值为零；
2. routed hidden state 中的 common component 会通过 $w_e^\top c$ 形成 expert-specific bias；
3. random top-1 router 会被 early common-logit 带入 collapse basin；
4. slot 信息存在，slot-specialization 可达；
5. common-logit cancellation 能显著提升 slot_NMI，但还不能证明 expert computation 已经因果专门化。 

导师新文档提出的新目标：

```text
expert partition 应降低特征干扰，而不是只改善路由熵或负载均衡。
```

---

## 1. Research Question

```text
Can a label-free common-controlled gate learn a stable semantic expert partition
that reduces common/rare feature interference,
rather than merely balancing expert load?
```

中文：

```text
一个不使用 feature label 的 common-controlled gate，
能否学到稳定的语义专家分区，
并减少 common / rare feature 之间的干扰，
而不只是让 expert load 看起来更均匀？
```

---

## 2. Core Hypothesis

```text
H1:
Early common-logit control is necessary for entering a specialization basin.

H2:
Specialization is only meaningful if expert routing separates conflict features
and preserves useful sharing among related features.

H3:
A successful gate must satisfy balance, semantic consistency, stability,
and causal utility simultaneously.
```

中文压缩：

```text
先去掉 common-logit 劫持；
再测试 gate 是否按 feature conflict 形成语义分区；
最后用因果效用证明 expert specialization 不是 route entropy 假象。
```

---

## 3. Physical Model

### Router-side decomposition

$$
h_f = c + p_f + q_f + \epsilon_f
$$

其中：

| 项            | 含义                              |
| ------------ | ------------------------------- |
| $c$          | across-feature common component |
| $p_f$        | parent / inherited feature      |
| $q_f$        | extra / conflict feature        |
| $\epsilon_f$ | noise or nuisance variation     |

router score：

$$
z_{f,e}=w_e^\top c+w_e^\top p_f+w_e^\top q_f+w_e^\top \epsilon_f
$$

理想 gate 应满足：

```text
1. 不让 w_e^T c 主导 early routing；
2. 对 shared parent p_f 可以共享 expert；
3. 对 conflict extra q_f 应分离 expert；
4. 对 nuisance ε_f 保持稳定。
```

---

## 4. Falsifiable Predictions

### Prediction A：common-control 仍是必要前置条件

如果不控制 $w_e^\top c$，则即使 conflict feature 存在，router 仍可能优先按 common bias collapse。

**支持结果**：

```text
baseline max_load 高，slot_NMI / conflict_NMI 低；
common margin > feature/conflict margin；
early dominant expert 可预测 final route。
```

**证伪结果**：

```text
baseline 已自然学到 high semantic partition，
且 common margin 不主导 early route。
```

---

### Prediction B：balance-only 不足以产生 specialization

如果只加 load-balance loss，可能出现：

```text
max_load 改善
但 conflict features 仍被同一 expert 处理
rare feature 仍受 common feature 干扰
```

这直接对应第二篇的边界：路由熵高但因果专门化弱，不能算解决表示塌缩。

**支持结果**：

```text
balance-only: load entropy ↑, but forced-routing utility 不分化，rare accuracy 不改善。
```

**证伪结果**：

```text
balance-only 同时提升 semantic purity、causal utility、rare robustness。
```

---

### Prediction C：真正 specialization 应降低 common/rare interference

在 common / rare conflict 数据中，成功 gate 应该：

```text
rare accuracy ↑
common update 对 rare logit 的负迁移 ↓
forced-routing utility 更稀疏
expert ablation 选择性损害对应 feature
```

导师文档的主实验计划也要求报告稀有特征准确率、有效维度、top 子空间质量、路由熵、专家负载和子空间消融下的因果损害，而不是只报告验证损失。

---

### Prediction D：MoE 不应只是把 collapse 转移到 expert 内部

成功的 expert partition 应该：

```text
global M_k(u_extra) ↓
per-expert effective rank ↑ or not collapse
top-subspace ablation 损害更局部
```

失败模式：

```text
global route balanced，
但每个 expert 内部仍有 high-gain collapse；
或者 top expert ablation 仍损害大量无关 feature。
```

---

# 5. 07 的最小实验设计

## Dataset: D07_common_rare_conflict

从你们当前的 `SLOT_s B_CONST Y_s` 扩展，不直接跳真实语言。

### Base structure

```text
PARENT_a  SLOT_s  B_CONST  Y_{a,s}
```

其中：

* `PARENT_a`：共享父特征；
* `SLOT_s`：区分子特征；
* `B_CONST`：routed token；
* `Y_{a,s}`：目标 token。

### 加入 common / rare conflict

构造两类：

```text
common: PARENT_a SLOT_common B_CONST -> Y_common
rare:   PARENT_a SLOT_rare   B_CONST -> Y_rare
```

要求：

```text
common 和 rare 共享 parent，
但需要不同 output。
```

这样可以测试：

```text
expert 是否把 shared parent 复用，
同时把 conflict extra 分开。
```

---

# 6. 模型对照组

| 模型                                           | 作用                                             |
| -------------------------------------------- | ---------------------------------------------- |
| Dense Transformer                            | 测没有 expert partition 时的 interference baseline  |
| Random top-1 MoE                             | 测自然 gate 是否 collapse                           |
| Balance-only MoE                             | 测 load balance 是否足够                            |
| Common-controlled MoE                        | 延续旧线，测去掉 common-logit 后是否进入 semantic partition |
| Common-controlled + stability regularization | 测小扰动稳定性是否必要                                    |
| Oracle feature gate                          | specialization 上界，不作为最终方法                      |

注意：oracle gate 只能做 upper bound，不能当主方法。

---

# 7. Primary Metrics

## 必须主指标

| 指标                              | 含义                                       |
| ------------------------------- | ---------------------------------------- |
| conflict_NMI                    | route 与 conflict feature 的归一化互信息         |
| parent_NMI                      | route 与 inherited parent feature 的归一化互信息 |
| rare accuracy                   | 稀有冲突 feature 是否学好                        |
| forced-routing utility matrix   | 强制送到每个 expert 后的 loss/accuracy           |
| expert ablation selectivity     | 关掉 expert 是否只伤害对应 feature                |
| route stability                 | 加无关扰动后 route 是否保持                        |
| common margin / conflict margin | early routing 被 common 还是 feature 主导     |

## 次要指标

| 指标                           | 含义                           |
| ---------------------------- | ---------------------------- |
| max_load                     | 是否塌缩                         |
| active experts               | 用了几个 experts                 |
| route entropy                | 负载分散程度                       |
| $M_k(u_{\mathrm{extra}})$    | extra feature 是否仍集中在 top 子空间 |
| per-expert effective rank    | expert 内部是否也塌缩               |
| top-subspace ablation damage | 共享高增益子空间是否因果支撑多个 feature     |

第二篇给出的有效维度、奇异有效秩和 top 子空间质量可以作为 07 的 representation metrics。

---

# 8. Minimal Protocol

## Protocol 07A: Common-Controlled Gate on Conflict Features

### Question

```text
common-controlled gate 是否能在 common/rare conflict setting 中
形成稳定语义分区，并减少 rare feature interference？
```

### Fixed

```text
router = dot-product sparse top-1
position embedding = zero / frozen
routing token = B_CONST
experts receive full hidden state
router input may be common-controlled
loss measured at B_CONST position
```

### Variants

```text
A. Dense baseline
B. Random top-1 MoE
C. Balance-only MoE
D. Early-window logit common cancellation
E. Router-input residual/common control
F. Oracle feature-aware gate
```

### Measurements over checkpoints

```text
step-0 / step-10 / final:
common margin
parent margin
conflict margin
route entropy
max_load
parent_NMI
conflict_NMI
rare accuracy
forced-routing utility
expert ablation selectivity
per-expert effective rank
M_k(u_extra)
```

---

# 9. Success / Failure Criteria

## Success

可以初步 claim：

```text
common-controlled gating improves causal expert specialization
in a controlled conflict-feature setting.
```

必须同时满足：

```text
accuracy 不下降；
rare accuracy 上升；
conflict_NMI 上升；
route stability 上升；
forced-routing utility 出现 feature-expert specificity；
expert ablation 选择性损害对应 feature；
M_k(u_extra) 或 top-ablation shared damage 下降。
```

---

## Failure

下面任一情况都不能 claim specialization：

```text
max_load 下降但 conflict_NMI 不升；
route entropy 上升但 forced-routing utility 不分化；
rare accuracy 不改善；
expert ablation 损害所有 feature；
per-expert 内部仍 high-gain collapse；
方法依赖 slot label 或 oracle decomposition。
```

---

# 10. Claim Boundary

## 可以 claim

```text
在受控 common/rare conflict setting 中，
common-controlled gate 能否改善 semantic routing 和 causal utility。
```

## 暂时不能 claim

```text
解决了真实 LLM 的 expert specialization；
MoE 天然提高语义容量；
load balance 等于 specialization；
slot_NMI 等于 expert functional specialization；
common cancellation 是可部署架构；
所有 high-gain concentration 都是坏的。
```

最后一点尤其重要：导师文档也指出，奇异集中可能是高效压缩机制，不一定全是病态；需要区分有用复用和过度全局集中。

---

# 11. 这个 anchor 对旧工作的重新定位

| 旧工作内容                         | 在 07 中的位置                              | 是否继续               |
| ----------------------------- | -------------------------------------- | ------------------ |
| random init collapse          | 07 的 entry failure mode                | 继续，但不再是最终问题        |
| common-logit cancellation     | 进入 specialization basin 的 intervention | 继续，作为 07A 关键变量     |
| residual-control router input | label-free common-control candidate    | 继续                 |
| slot_NMI                      | routing specialization 指标              | 保留，但降级为必要不充分       |
| max_load / entropy            | anti-collapse 指标                       | 保留为 sanity check   |
| load-balance warmup           | anti-lockin baseline                   | 保留为对照，不可单独 claim   |
| slot-init / oracle gate       | upper bound                            | 保留，不作为方法           |
| forced-routing utility        | 以前是 open question                      | 升级为 primary metric |
| expert ablation               | 以前缺失                                   | 必须加入               |
| common/rare conflict          | 以前没有                                   | 07 的核心数据变化         |

---

# 12. Minimal Next Action

**只做一个动作：写并实现 `Protocol 07A: Common-Controlled Gate on Conflict Features`。**

不要先扩到自然语言，不要先做复杂 hierarchy。
第一轮只回答：

```text
在最小 common/rare conflict 数据中，
common-control 是否让 random-init top-1 MoE 从 anti-collapse
推进到 causal expert specialization？
```
