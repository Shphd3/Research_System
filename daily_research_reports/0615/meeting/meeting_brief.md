# Meeting Brief: Common-Filtered Expert-Spectrum Router Initialization

## **Question**

这次汇报要回答一个问题：导师提出的“按照专家初始化后的高增益方向初始化 router”是否能变成一个有效方法？

**父问题：**
真实文本中的 top-1 稀疏混合专家模型为什么会在训练早期出现专家负载集中？这个问题关系到 expert specialization 能否稳定发生。

**当前子问题：**
专家初始化后，每个专家都有自己的高增益方向。我们要检验：把 token 按这些方向初始化路由，尤其在去掉共同方向以后，是否能减少第 0 步和第 10 步的路由集中。

这里的高增益方向指：专家前馈网络对哪些输入方向更敏感。共同方向指：一批 token 进入 router 前的隐藏状态中共同拥有的平均方向和主要变化方向。

## **Conclusion**

> 这个方向有诊断价值，但当前线性 top-1 router 初始化不能作为成功方法推进。它能让第 0 步分布更均匀，但不能阻止第 10 步训练放大。

**主要更新：**

1. 专家高增益子空间确实彼此不同，但这还不是“专家已经负责不同功能子空间”的证据。
2. 专家最高增益方向和表征共同主方向没有强直接重合；问题主要出现在把专家谱分数压缩成线性 router 行时。
3. 去共同方向后的专家谱初始化能减少第 0 步负载偏置，但第 10 步仍严重集中，说明瓶颈更像训练动力学，而不是单纯的初始分布。

## **Key Evidence**

1. **专家谱方向彼此不同，但只能支持几何差异。**  
   **结果：** 不同专家高增益子空间平均重合约 `0.0116`。  
   **解释：** 高斯初始化下专家不是完全一样的；但这不能证明专家已经形成任务相关分工。

2. **专家谱方向没有直接对齐共同方向。**  
   **结果：** 专家高增益子空间与共同方向子空间的平均重合约 `0.0166`。  
   **解释：** 原始专家谱失败，不是因为专家 top 子空间本身就是共同方向子空间。

3. **线性实现阶段引入了共同方向投影。**  
   **结果：** router 行共同方向投影均值：random `0.0830`，raw spectrum `0.2116`，common-filtered spectrum `0.000044`。  
   **解释：** V4 更均匀，是因为它去掉了线性 router 行上的共同方向投影。

4. **V4 改善第 0 步，但不改善第 10 步。**  
   **结果：** 去掉前 1% 高频 token 后，V4 第 0 步负载第一专家为 `13.97%`，random 为 `19.98%`；第 10 步 V4 为 `93.51%`，random 为 `83.16%`。  
   **解释：** V4 解决了一部分初始偏置，但没有挡住早期训练放大。

## **Detailed Setup**

**数据 / 任务：**

- 数据是 DCLM 打包文本。
- 每条序列 256 个输入 token，目标是下一 token 预测。
- 初始化统计和路由审计使用固定 token 批次。

**模型：**

- 随机初始化 Qwen-style 稀疏混合专家语言模型。
- 6 层，8 专家，hidden size 512。
- 训练 0--300 步，随机种子 0、1、2。

**路由器 / 混合专家模型：**

- router 是无 bias 的线性 gate。
- 每个 token 只选择 1 个专家。
- 负载均衡损失关闭。
- 需要注意：协议原本希望没有 shared expert，但当前最小 MoE 实现仍加入 shared expert 路径。router 指标对 top-1 gate 是精确的，但隐藏状态动力学包含 shared expert 计算。

**运行 / 审计：**

- ACP job `pt-tjk7oil5`，状态 `SUCCEEDED`。
- 完整训练：6 个初始化版本，3 个 seed，0--300 步。
- 审计包含 cross-checkpoint replay、forced-routing utility、专家谱 overlap、oracle-to-linear agreement、高频 token 去除审计。
- router logit 重建误差为 `0.0`。

## **Detailed Evidence**

### 1. Expert Spectrum Is Geometrically Distinct

这个证据回答：高斯初始化后的专家是否真的有不同的高增益方向？

专家高增益方向由输入侧能量矩阵定义：

$$
G_e = W_{gate,e}^{\top}W_{gate,e} + W_{up,e}^{\top}W_{up,e}.
$$

| 指标 | 结果 | 含义 |
|---|---:|---|
| inter-expert subspace overlap | 0.0116 | 不同专家高增益方向重合很低 |
| residual utility correlation, V3 | 0.2328 | 原始专家谱有弱效用信号 |
| residual top-1 utility match, V3 | 0.3889 | 高于 random 的 0.2222 |

**解释：**
专家谱不是纯噪声，里面有弱信号。但这个信号弱，且没有直接变成稳定有效的 router 初始化。

### 2. Expert Spectrum Is Not Simply Common Direction

这个证据回答：导师担心的 common feature 是否直接污染了专家 top 子空间？

| 指标 | 结果 | 含义 |
|---|---:|---|
| overlap($S_e$, $C$) | 0.0166 | 专家谱方向和共同方向直接重合很低 |
| raw spectrum row common projection | 0.2116 | 压成线性行后 common 投影很大 |
| common-filtered row common projection | 0.000044 | V4 成功去掉线性行 common 投影 |

**解释：**
common contamination 不是简单发生在专家谱子空间本身，而是发生在“谱分数到线性 router 行”的实现桥里。这解释了为什么 V4 在第 0 步更均匀。

### 3. Step-0 Balance Improves, Step-10 Concentration Does Not

这个证据回答：V4 是否真的减少路由集中？

去掉前 1% 高频 token 后，后层 3--5 的排序负载如下。负载第一专家指每个层和 seed 中接收 token 最多的专家。

| 版本 | 步数 | 负载第一专家 | 负载第二专家 | 其余专家合计 |
|---|---:|---:|---:|---:|
| V0 random | 0 | 19.98% | 16.81% | 63.21% |
| V4 common-filtered | 0 | 13.97% | 13.31% | 72.72% |
| V0 random | 10 | 83.16% | 13.48% | 3.36% |
| V4 common-filtered | 10 | 93.51% | 6.04% | 0.45% |

**解释：**
V4 的确让第 0 步更均匀。这个结果说明我们不是完全没有实现导师的 intuition。但是训练到第 10 步后，V4 更严重集中，所以不能把它说成解决方法。

### 4. Full Training Metrics Weaken the Method Claim

这个证据回答：V4 是否在关键早期训练指标上优于 random？

后层 3--5 平均：

| 版本 | common-margin increase | step10 max load | effective experts | interaction |
|---|---:|---:|---:|---:|
| V0 random | 0.3878 | 0.8344 | 1.5636 | 0.2795 |
| V3 raw spectrum | 0.6970 | 0.9144 | 1.3197 | 0.3268 |
| V4 common-filtered | 0.5203 | 0.9374 | 1.2177 | 0.1543 |
| V5 hybrid | 0.5971 | 0.8872 | 1.3932 | 0.2529 |

**解释：**
V4 降低 interaction，这是局部机制改善；但它没有降低 common-margin increase、step10 max load 或有效专家数。方法 claim 不成立，机制 claim 可以保留。

## **Current Interpretation**

**观测：**
V4 去掉了线性 router 行上的共同方向投影，使第 0 步 token 分布更均匀；但第 10 步仍然快速集中。

**解释：**
初始共同方向偏置只是早期集中问题的一部分。0614 的结果已经显示，第 10 步 spike 主要涉及隐藏状态变化和 gate-hidden interaction。因此只修正第 0 步线性初始化，不足以阻断训练放大。

**现在可以说：**

```text
1. 专家高斯初始化产生不同高增益方向。
2. 专家谱方向与表征共同主方向没有强直接重合。
3. 原始专家谱的 common contamination 主要发生在线性实现阶段。
4. common-filtered 初始化改善第 0 步负载均匀性。
5. 它不能阻止第 10 步早期负载集中。
```

**仍然只是猜测：**

```text
1. quadratic / oracle router 可能有效。
2. learned classifier bridge 可能比 row-mean linear bridge 更好。
3. 第 10 步集中可能来自 router winner 自强化、隐藏状态漂移、位置结构或专家输出反馈。
```

## **Boundary**

**这个结论覆盖：**

- DCLM 打包文本。
- 随机初始化小型 Qwen-style MoE。
- 6 层，8 专家，top-1 稀疏路由。
- 无负载均衡损失。
- 训练 0--300 步。
- 精确 router 输入审计。

**这个结论不覆盖：**

- 预训练大模型。
- top-2 / top-4 路由。
- 长训练后的最终 expert specialization。
- 专家谱完全无用的结论。
- 导师想法不可能成立的结论。
- oracle / quadratic / learned classifier router 也会失败的结论。

## **Next Step**

**下一步决策：**
会中建议把问题从“继续扩大专家谱初始化实验”转成一个更窄的机制审计：

```text
第 0 步共同方向最占优的 router winner，是否在前 10 步被训练过程进一步放大？
```

**下一轮实验：**
优先做 post-hoc audit，不先开新大实验。使用已有 checkpoint，统计每个 seed、layer、step 上：

```text
c_t = 固定审计 token 的 router 输入均值
s_e(t) = w_e(t)^T c_t
load_e(t) = route 到 expert e 的 token 比例
delta_w_e(t)^T c_t = router 行更新沿共同方向的分量
```

**支持标准：**

```text
1. 第 0 步 load winner 也是 common projection winner；
2. 这个 winner 的 common projection margin 到第 10 步增加；
3. winner 的 router 更新沿共同方向更大；
4. 这个变化和 raw load 增长同步。
```

**削弱标准：**

```text
1. winner 频繁变化；
2. common projection margin 不增加；
3. raw load 增长时 router common projection 不变；
4. 结果更支持 hidden drift、position structure 或 expert-output feedback。
```
