# 可复用层级规则经过 NTP 后是否形成低任务功能秩的 hidden-state 表征？

## 1. 今日唯一推进点与成功条件

今天只解决 `0721 组会_笔记.md` 最后总结中的第二个问题：

> 假设某类长程、层级、组合结构确实对应一种可复用的语义计算，那么这种数据结构经过 NTP 训练后，是否会形成更低秩的 hidden-state 表征空间？

今天不证明自然语言整体符合该结构，也不研究参数矩阵秩或设计 Router。今天的唯一和进一步分析是：

> **批准、修改或拒绝 A14_02_E01，判断它能否直接检验“共享组合规则是否产生更低的任务充分根状态功能秩”。** + 执行相关实验

同时今天需要阅读最经典的MoE条件计算文章 + 对于Latent MoE进行检查。

### 今日闭环成功条件

今日只有同时满足以下条件才算完成：

1. **问题对象固定：**“低秩表征”明确指许多 held-out 样本的最终 `ROOT` hidden state 所需的任务功能秩，不再混用单个向量、全部 token 拼接矩阵、参数秩或纯谱秩。
2. **因果比较固定：** shared composition 与 independent lookup 在规则数量、exact relation frequency、上下文多样性、答案分布、训练预算和完整模型 held-out utility 上可比。
3. **泛化含义固定：** 子空间和 checkpoint 只由 calibration 数据确定；held-out test 只用于判断未见上下文或组合上的任务是否仍被保留。
4. **裁定规则固定：** 明确 Pass、Fail、Insufficient，以及每种结果允许声称和不能声称的内容。
5. **人工判断完成：** 我在本文第 5、6 节填写中心判断，并对 A14_02_E01 标记 `批准 / 修改 / 拒绝`。

实验运行 + 分析完成是今日最终完成条件；协议未批准前不运行。

## 2. 从组会问题到 A14_02 的完整链路

```text
候选语言直觉
长程语义可能由可复用的层级组合规则形成
        │
        │ 这是真实语言前提，当前尚未证明
        ▼
受控操作化
共享两步组合规则 vs. 独立随机 lookup
        │
        │ 匹配规则数量、频率、上下文和答案分布
        ▼
统一训练机制
使用相同 causal Transformer 和 full-position NTP 训练
        │
        ▼
表征对象
每个样本在答案前最终 ROOT 位置的 hidden state
        │
        │ 跨许多样本按列堆叠成根状态矩阵
        ▼
任务功能秩
在 calibration 上学习低维子空间，
在 held-out test 上投影 ROOT 状态并重放答案头，
寻找仍能保持任务损失和准确率的最小维数
        │
        ▼
决定性比较
shared 是否比 matched lookup 需要更少方向
        │
        ├── 是：受控 NTP 任务中，共享组合结构形成了更低维的任务充分根表征
        ├── 否：当前证据不支持共享规则带来额外状态压缩
        └── 门失败：模型未学会、未泛化或重放无效，结果证据不足
        │
        ▼
后续边界
只有状态功能秩差异成立后，才讨论参数方向需求；
只有真实专家效用差异成立后，才讨论 Router
```

## 3. 关键对象与术语

| 术语 | 本日含义 | 不能混同为 |
|---|---|---|
| shared composition | 不同样本共享同一两步组合形式，只改变输入或规则参数 | 相同完整样本反复出现 |
| independent lookup | 每条规则由相互独立的随机映射表实现，缺少共享组合形式 | 模型一定只会死记硬背 |
| `ROOT` hidden state | 模型读取完整输入后、预测答案前的任务摘要状态 | 把一条序列所有 token hidden states 直接拼接 |
| held-out | 完全不参与 checkpoint、子空间或阈值选择，只用于最终测试的数据 | 训练集重放 |
| effective rank | 根状态谱能量集中在多少个等效方向；仅作几何诊断 | 任务充分性 |
| task-functional rank | 投影 ROOT 状态后，仍能保持 held-out 损失和准确率所需的最小方向数 | 严格矩阵秩、参数秩或语义原子数 |

### 为什么主对象不是“所有 token hidden states 的拼接”

把一条序列的所有 token 状态直接拼接后测秩，会同时受到序列长度、位置变化和样本数量影响，容易得到形状造成的平凡结论。本实验研究的是：

> 模型读取完整任务输入后，最终任务摘要至少需要多少个线性方向才能保留答案功能。

因此主对象是跨样本堆叠的最终 `ROOT` hidden state。

## 4. 核心问题与实验裁定

### Q1：A14_02 是否直接回答组会总结中的第二个问题？

需要裁定：

> shared 与 lookup 均由 NTP 学会且通过 held-out utility gate 后，shared 是否只需更少的 `ROOT` 状态方向保留任务行为？

这直接检验“可复用组合结构是否被 NTP 编码成更低维的任务相关 hidden-state 表征”。它不检验自然语言是否真的采用这种结构。

### Q2：实验是否排除了最强替代解释？

最强替代解释是：

> 观察到的低秩不是共享组合规则造成的，而只是规则数量少、关系出现频率高、答案类别有限、重复完整样本、模型没学会，或最终答案头本来低维。

协议必须确保：

1. shared 与 lookup 匹配独立规则数量 $K$；
2. 匹配 exact relation frequency $F$；
3. 匹配 context diversity $D$ 与答案分布；
4. 两者均通过完整模型 capability 和 held-out generalization gate；
5. 完整维度重放恢复原模型，学得子空间优于同秩随机子空间；
6. 功能秩优势不能由 lookup-$K$ 曲线或最终答案瓶颈解释。

### Q3：什么结果能够改变我们的认知？

**Pass：**

- shared/unique-diverse 与 matched lookup/unique-diverse 均学会任务；
- shared 在 held-out test 上用稳定、显著更少的 `ROOT` 方向保持同等任务效用；
- 至少 4/5 seeds 同向，置信区间排除零；
- 重放、随机子空间和答案瓶颈守卫通过。

允许更新：

> 在该受控 NTP 任务中，低 exact-frequency 不必导致高任务功能秩；可复用组合规则可以形成比 matched lookup 更低维的任务充分根状态表征。

**Fail：**

- 控制 $K,F,D$ 和 task utility 后，shared 不再具有功能秩优势；或
- 差异完全由 lookup 数量、答案瓶颈或其他已注册 rival 解释。

需要更新：

> 当前受控证据不支持“共享组合规则通过 NTP 形成额外 hidden-state 功能压缩”。

**Insufficient：**

- 任一主要条件没有学会或没有泛化；
- calibration/test 泄漏；
- full-rank replay 不能恢复原模型；
- 结果依赖单一 seed、单一阈值或事后选择；
- shared 任务过难而出现 floor effect。

此时不能支持或否定主假设，只能修复测量合同。

### 无论结果如何都不能声称

- 自然语言或语义世界整体是树；
- 长程、层级或高频本身必然低秩；
- 全部 token hidden states 或参数矩阵低秩；
- hidden-state 低秩自动推出多个专家、稀疏 Router 或更好下游效用。

## 5. 我的中心判断与讲述主线（我填写）

1. **现象与中心判断：** 对于 ______，我认为 ______。
2. **机制与问题链：** 如果 ______，NTP 可能 ______，因此 A14_02 应比较 ______。
3. **最强替代解释；最不确定一环：** ______；______。
4. **改变判断的证据：** 如果看到 ______，我会修正或放弃上述判断。

## 6. 今日逐题闭环（我填写）

| 问题 | 我的一句话回答 | 决定性证据或缺失实验 | 不能声称 |
|---|---|---|---|
| Q1：A14_02 是否直接回答第二个组会问题？ | ______ | A14_02_E01：______ | ______ |
| Q2：实验是否排除了 lookup、频率和答案瓶颈？ | ______ | 协议控制：______ | ______ |
| Q3：Pass / Fail / Insufficient 如何改变判断？ | ______ | 裁定规则：______ | ______ |

### 总体收束

- **这些回答共同说明：**______。
- **我对 A14_02_E01 的裁定：** 批准。
- **若需修改，唯一阻塞项：**______。
- **会后唯一下一决策：**______。
- **恢复时第一动作：**打开 A14_02_E01 protocol，核对唯一阻塞项并完成裁定。

## 7. 路由与证据

- **原始组会问题：**[0721 组会_笔记.md](meeting_recordings/0721%20组会_笔记.md)
- **A14_02 researcher judgment record：**14_02 researcher judgment record
- **A14_02 anchor：**[共享组合规则与任务根状态功能秩](../../../../../Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/14_02_relation_reuse_root_effective_rank_anchor_cn.md)
- **A14_02_E01 protocol：**[共享规则与 lookup 的任务根状态功能秩](../../../../../Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/protocol_cn.md)
- **A14_02_E01 result：**[四卡 full-run 结果摘要](../../../../../Projects/from-attention-to-search/main/experiments/A14/14_02_relation_reuse_root_effective_rank/A14_02_E01_shared_rule_vs_lookup_root_rank/summary_cn.md)
- **聚焦审计：**`focused`
- **正式状态更新：**`A14_02_E01 completed_insufficient; anchor and project map updated.`
