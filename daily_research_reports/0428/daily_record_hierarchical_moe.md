# Daily Record A: Direct Hierarchical MoE

## 1. 路线定位

本路线按照老师要求，直接构造 ground-truth 已知的 synthetic natural Zipfian hierarchy dataset，并训练 hierarchical / routed MoE，检查模型是否能在常规 LLM 训练目标下形成有用的层级路由和专家分工。

这个实验不是为了证明真实语言天然存在 hierarchy，而是一个 mechanism sanity check：

> 如果数据真的由 `common / coarse / fine` 三层机制生成，并且 word / phrase / token 出现频率符合 Zipfian 长尾，那么 hierarchical routed MoE 能不能在 next-token prediction 训练中学出有用的层级结构？

这里有一个关键边界：训练时仍然按照普通 LLM 的 next-token prediction objective 训练，不把 `coarse_label / fine_label / token_source / template_id` 喂给主模型。我们只是在评估时检查 router 是否按照我们设想的语义层级进行分化。

如果 router 没有按照人工定义的 `common / coarse / fine` 语义层级分化，不能直接说明架构是错的。它可能说明：

1. router 学到了另一种对 NTP 更有用的潜在划分；
2. 当前语义标签不是模型最自然的专家划分单位；
3. 训练目标没有足够压力让 route 对齐人工层级；
4. routing 输入、expert input 或训练时长仍需调整。

因此，本路线的正确问题不是“是否精确复现人工标签”，而是：

> 模型是否能形成对预测有用、可解释、可诊断的层级专家分工；其中人工 `common / coarse / fine` 只是第一组重要参照。

---

## 2. Dataset Snapshot

数据集：`Synthetic Natural Zipfian Hierarchy`

核心性质：

- 文本是可读 synthetic natural text，不是随机 token 序列。
- `coarse_label`: 4 类，均匀。
- `fine_label`: 16 类，每个 coarse 下 4 类，均匀。
- Zipfian 控制的是 word / phrase / token 出现频率，不是类别采样频率。
- `common / coarse / fine` 是 token/span source，用于评估 routing 和 expert specialization。
- `common / coarse / fine` 是我们构造数据时设想的语义层级：common 是跨领域通用表达，coarse 是大领域信号，fine 是细主题信号。

Formal v1：

| split | documents | seq_len | label tokens |
|---|---:|---:|---:|
| train | 20000 | 128 | 2560000 |
| valid | 1000 | 128 | 128000 |
| test | 1000 | 128 | 128000 |

Sanity：

- word/phrase Zipf alpha = `1.052`, R2 = `0.974`
- token-id Zipf alpha = `1.014`, R2 = `0.933`
- template-only shortcut 很低：coarse acc = `0.254`, fine acc = `0.064`

---

## 3. Main Hypothesis

**H-A-main:** 如果 synthetic natural text 的生成机制真实包含 `common -> coarse -> fine` 的层级结构，那么一个参数量匹配的 conditional hierarchical MoE 应该能在常规 NTP 训练下形成有用的层级专家分工；理想情况下，这种分工会与人工 `common / coarse / fine` 语义层级对齐，并表现为更低 NTP、更高 route-label/source mutual information、更低 oracle regret 和正 selected expert advantage。

---

## 4. Three Sub-hypotheses

### H-A1: Dataset hierarchy signal 可学习

在 template shortcut 被控制、类别均匀、Zipfian token frequency 成立的前提下，数据中确实存在可恢复的 document-level `coarse/fine` 和 token-level `common/coarse/fine source` 信号；但模型是否按这些标签路由，需要通过训练后的 route analysis 检查，不能在训练时直接监督。

### H-A2: Middle-band routed hierarchy 有结构优势

以

$$
\tilde{x}_M=P_{17:207}(h-\mu)
$$

作为 coarse router input，并在 $M$ 内部继续用 `M_cc / M_tail` 做 source/fine routing，应优于 flat MoE middle、random-subspace routing 和 matched dense。

### H-A3: Expert specialization 必须超过 router recovery

即使 router 与人工标签对齐，也不能直接说明 hierarchy 成立；必须看到 selected expert 的 counterfactual NTP loss 优于 alternative experts，尤其是在 coarse-source、fine-source、rare-frequency tokens 上。反过来，如果 fixed-label router accuracy 不高，也不能直接说明架构失败，因为 expert id 有置换对称性，且模型可能学到非人工标签的有效层级。

---

## 4.5 训练与评估原则

### 训练原则

主训练仍是普通 LLM next-token prediction：

$$
L_{\text{LM}}
=
-\frac{1}{T}
\sum_t
\log p_\theta(y_t|y_{<t})
$$

主实验不使用以下字段作为输入或监督：

```text
coarse_label
fine_label
token_source
template_id
```

这些字段只用于：

```text
evaluation
oracle diagnostic
teacher-aided diagnostic
post-hoc route analysis
```

### 评估原则

评估时不只看固定 label-to-expert accuracy。因为 MoE expert id 有置换对称性，而且模型可能选择不同于人工标签的潜在划分。

必须同时看：

```text
test NLL
loss_source_common/coarse/fine
loss_bucket_common/middle/rare
Hungarian route recovery
route-label/source mutual information
route usage by label/source
selected expert advantage
oracle regret
random router control
oracle router upper bound
```

解释规则：

1. `fixed router accuracy low` 不能直接说明失败。
2. `Hungarian recovery / MI high` 说明 route 与人工层级有置换不变对齐。
3. `selected expert advantage > 0` 才说明被选 expert 真有预测收益。
4. `oracle strong, learned weak` 说明结构有潜力但 router 没学好。
5. `random router >= M-band router` 说明 middle-band routing 的因果优势尚未建立。
6. `oracle also weak` 说明当前数据或 expert 结构可能不需要这个 hierarchy。

---

## 5. 第一阶段模型矩阵

| ID | Model | 作用 |
|---|---|---|
| G0 | Dense matched | 参数量基线 |
| G1 | Flat MoE raw + LB | 普通 MoE 基线 |
| G2 | Flat MoE middle + LB | 检查 middle routing 是否已经够用 |
| G3 | H-Mid-Soft | 浅层 coarse/fine hierarchy baseline |
| G4 | H-CondCT-Soft | 第一阶段主模型 |
| G5 | H-CondCT-Soft + LB | 检查 LB 是否有真实收益 |
| G6 | H-CondCT-LevelInput | 检查 expert input 是否也要分层 |
| G7 | H-Oracle-CondCT | 上界 |
| G8 | H-Rand-CondCT | 随机子空间对照 |
| G9 | Uniform Expert Mixture | 排除只是多 expert capacity |

最新工程中还补充了 top-1 sparse 版本：

| ID | Model | 作用 |
|---|---|---|
| G9 / top1 | H-CondCT-Top1 | 函数行为 top-1 sparse hierarchical MoE |
| G10 / top1 LB | H-CondCT-Top1 + LB | 检查 hard path 下 LB 是否有帮助 |
| G11 / top1 rand | H-CondCT-Top1-Rand | 随机 router input 对照 |
| G12 / top1 oracle | H-CondCT-Top1-Oracle | hard path oracle 上界 |

主模型结构：

```text
x_M -> coarse router
    -> x_Mcc source router
        -> conditional-common expert
        -> conditional-tail branch
            -> x_Mtail fine router
```

---

## 6. 最新实验状态（2026-04-28）

### 6.1 已完成：formal_ablation_v1

设置：`1500 steps`，`eval_every=300`，3 seeds。

这个实验短训比较了 dense、flat MoE、浅层 hierarchy、CondCT soft hierarchy、level-specific input、random router 和 oracle soft path。它主要用于快速筛选结构，不能作为最终结论。

当前结果：

- `G6_h_condct_level_input` 是短训最佳 soft model，test loss 约 `1.6572`。
- dense matched test loss 约 `1.6712`。
- random CondCT、flat MoE、浅层 H-Mid-Soft 明显更弱。

当前解释：

> Level-specific soft hierarchy 是有价值候选，但它是否真的学到我们设想的语义层级，需要看 permutation-invariant recovery、route MI、route usage 和 counterfactual expert advantage，不能只看旧式 fixed router recovery。

### 6.2 已完成：top1_sparse_two_epoch_v1

设置：`40000 steps`，约 2 epoch，3 seeds。

这个实验训练 top-1 hard path CondCT，并与 random top-1 router、LB 版本和 oracle top-1 diagnostic 比较。

当前结果：

| group | test loss | coarse Hungarian | fine Hungarian | route source MI | oracle regret |
|---|---:|---:|---:|---:|---:|
| top1 oracle | 1.1532 | 1.0000 | 1.0000 | 0.3019 | 0.3674 |
| top1 random | 1.1713 | 0.2573 | 0.1226 | 0.0687 | 0.9688 |
| top1 M-band | 1.1741 | 0.2987 | 0.1566 | 0.0295 | 0.8977 |
| top1 M-band + LB | 1.1749 | 0.2799 | 0.1520 | 0.0231 | 0.9808 |

当前解释：

1. Oracle top-1 明显强，说明 hard path 专家结构有表达潜力。
2. Learned M-band top-1 没有超过 random top-1，说明 M-band routing 的因果优势尚未建立。
3. 旧式 recovery gate 不能作为失败结论，因为 fixed label-to-expert 对齐假设不可靠。
4. 当前更准确的说法是：模型尚未证明按我们设想的人工语义层级路由，但这不等于架构错误；下一步需要更好的 route analysis 和 router training。

### 6.3 未完成：two_epoch_core_v1

目标：用 2 epoch 重跑 core controls，作为 top-1 sparse 的正式横向比较。

需要完成：

```text
G0 dense matched
G1 flat raw LB
G2 flat middle
G5 soft CondCT LB
G6 soft CondCT level input
G8 random CondCT
```

当前状态：部分 shards incomplete，需要用 `sco` 复核 ACP job 是否退出；若已退出，需要续跑或重跑 cuda0/cuda1 shards 后再 merge。

## 7. 每日填写区

> 下面是每天必须更新的部分。

### 7.1 今日日期


### 7.2 今日核心问题


### 7.3 今日当前判断


### 7.4 今天具体推进了什么？


### 7.5 今天跑了哪些实验 

| 项目 | 内容 |
|---|---|
| dataset |  |
| model |  |
| training |  |
| evaluation |  |
| cluster / acp / sco |  |

### 7.6 今天得到的关键指标

| 指标 | 数值 / 观察 | 解释 |
|---|---|---|
| train / valid / test NLL |  |  |
| common / coarse / fine token NLL |  |  |
| coarse router acc |  |  |
| source router acc |  |  |
| fine router acc |  |  |
| selected expert advantage |  |  |
| oracle regret |  |  |
| usage entropy |  |  |

### 7.7 今天哪个判断发生了变化？


### 7.8 当前卡点


### 7.9 明天最小下一步


### 7.10 需要问 AI / 导师的问题

