# A11 精确源 K/V 审计：认知更新与导师回答

日期：2026-07-16
实验：`A11_03_02_E02_exact_source_kv_information_audit`
远程任务：ACP job `pt-rqtb6bw0`，四卡，`SUCCEEDED`
正式证据：[Summary](../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/summary.md)、
[Detailed](../../../Projects/from-attention-to-search/main/experiments/A11/11_03_cross_position_standard_head_use_boundary/A11_03_02_E02_exact_source_kv_information_audit/detailed.md)

表达依据：[科研指导录音整理](../../0713/recordings/0713_科研指导_整理稿.md)要求先讲清物理先验、最小可检验子问题、优先级和对主问题的推进；[导师与学长讨论整理](../../0713/recordings/0713_导师与学长讨论_整理稿.md)要求独立拆解“信息形成—标准头使用”的因果链，并说明 MTP 可能只在结构化、需要规划或中间状态的任务上有价值，不能从合成结果直接外推。

## 一句话结论

这次没有证明“主头利用了更多 MTP 信息”。它补上了上一实验缺失的一环：精确第二层 `U03` K/V 在 NTP、shared-aux 和 informative-MTP 下都能 `100%` 线性读出 branch；informative-MTP 没有增加已注册的可读性，却在 `5/5` 种子明显压缩 branch 内 nuisance 波动。当前最合理的更新是：MTP 可能整理了共享表征的几何，但现有任务存在直接绕行和双重饱和，无法检验主头在必要时是否会消费这种几何。

## 我们原来为什么要做

上一轮 E01 看到：替换 `U03` 的精确 K/V 后，informative-MTP 相对
shared-aux 没有稳定的强答案切换增量。这个负结果有两个不同解释：

1. 被替换的 K/V 根本没有稳定 branch 信息；
2. K/V 已经有信息，但后续标准主头没有形成稳定的强使用。

E02 的目的只是先区分这两者，不能直接证明主头使用。

## 实验实际回答了什么

### 直接回答

- same-contract replay 完整复现 E01 的检查点和行为统计；
- 三个条件、五个种子的精确 $[K_{2,T};V_{2,T}]$ 都能在未见 nuisance
  上以 `1.0` accuracy 和四类 `1.0` recall 预测 branch；
- 因此“精确 K/V 完全没有稳定线性 branch 信息”被排除。

### 没有得到支持

主要指标为

$$
\Gamma_{\mathrm{read}}
=
\operatorname{CE}_{shared}
-
\operatorname{CE}_{info}.
$$

均值为 `-0.002299 nat/example`，95% CI 为
`[-0.004502, -0.000173]`，`4/5` 种子非正。informative-MTP 没有比
matched shared-aux 更容易线性读出 branch。

### 新出现的机制线索

informative-MTP 的 Fisher 分离比在 `5/5` 种子高于 shared-aux，倍数为
`2.91–49.55`。主要变化不是每一对 branch 都离得更远，而是同一 branch
下不同 filler 排列造成的 nuisance 波动被明显压缩。

更准确的话是：

> MTP 没有让一个原本读不出的 branch 标签变得可读；它可能让已经可读的
> branch 表征对 nuisance 更不敏感、更整齐。

这只是次要几何证据，不等于主头使用，也不等于真实任务更好。

## 为什么正式判定仍是证据不足

预注册要求所有标签打乱 probe 的确认集准确率不超过 `0.30`。实际有
`3/15` 超过，最大 `0.3357`，所以自动判定必须保持 `insufficient`。

事后审计发现，15 个打乱 probe 的平均准确率为 `0.2209`，平均 CE 为
`1.4427`，并没有广泛泄漏迹象。更可能的问题是保护项定义不合适：当
真实表示已经形成四个近乎完美的 cluster 时，一次随机打乱会让某个 cluster
偶然对齐到原标签；再对 15 次结果取最大值，很容易跨过 `0.30`。

这个解释只能用于修正下一版 Protocol，不能事后把本轮改判为通过或失败。

## 这次真正更新了哪条认知

原认知：

> E01 没有强答案切换，可能是 K/V 没形成信息，也可能是主头没使用。

更新后：

> 精确 K/V 绝对信息形成已经确认；但它是三种目标都能形成的普通信息，
> 不是已识别出的 MTP 新增信息。MTP 更明确的差别出现在几何压缩，而不是
> 标签可读性。当前任务又允许答案位置直接读取 `BR_z`，所以“主头没有使用
> MTP 信息”仍然不能成立。

被削弱的直觉：

> “只要证明 K/V 可读，再结合补丁负结果，就能证明主头没有利用。”

为什么不成立：可读的是各条件共有的 branch 标签；补丁测的是一条非必要、
可绕行的通道；两者拼起来仍不能识别“MTP 特异信息的未利用”。

## 建议向导师回答的顺序

### 1. 我们在主问题中切了哪个最小子问题

我们先不问 MTP 是否普遍更好，只问：信息性未来目标写入的 branch 信息，
是否进入了后续标准头真正能读取的精确 K/V，以及该通道是否被强使用。

### 2. 为什么这个子问题优先

上一轮强因果补丁是负的，但没有 source-information guard。若 K/V 本身
没有信息，就不能把负结果归因于“主头没用”。所以先补信息形成审计。

### 3. 直接结果

精确 K/V 在三种目标、五个种子上都 `100%` 可读。informative-MTP 相对
shared-aux 的可读性增量没有出现；主要 CE 差异为负且非常小。与此同时，
informative-MTP 在 `5/5` 种子压缩了 branch 内 nuisance，Fisher 比提高
`2.9–49.5` 倍。

### 4. 更新后的机制判断

MTP 在这个极简任务中更像是改变表征组织方式，而不是增加新的 branch
标签。现有数据允许标准头绕过 `U03` 直接读取 `BR_z`，所以无法判断这种
几何在必要时是否会被标准头使用。

### 5. 不能说什么

不能说主头完全不使用 MTP 信息；不能说 MTP 更差；不能把 Fisher 几何
直接解释为行为收益；也不能外推到长程、自然语言或 MoE。

### 6. 唯一下一步

先设计并验证 `relay-required` 构造：答案不能绕过早期消息，而且
shared-aux 的信息指标不能先饱和。只有这个 carrier 通过可学习性和无绕行
守卫后，才重新比较 informative-MTP 是否更早建立并被标准头使用的消息。
共享 unembedding 和 K/V/Q 分解暂时后置。

## 可直接口述的精简版

> 我们这两步实验把“信息形成”和“信息使用”拆开了。第一步在能力、头数和
> loss 项匹配后，替换 `U03` 的精确 K/V，没有看到 informative-MTP 相对
> shared-aux 稳定的强答案控制增量。第二步补做 source-information audit，
> 发现这组 K/V 并不是没有 branch 信息：NTP、shared-aux 和
> informative-MTP 在五个种子上都能百分之百线性读出 branch。但
> informative-MTP 没有增加这个已经饱和的可读性；它更稳定的差别是把
> branch 内的 nuisance 波动压小，Fisher 分离比在五个种子都更高。
>
> 所以我现在不会再说“信息已经进入，但主头没有利用”。更准确的是：当前
> 任务中 branch 信息通过普通路径已经普遍存在，MTP 可能重新组织了表示
> 几何，但答案位置可以直接绕过 `U03`，因此我们还没有检验“当这条消息
> 必须被使用时，MTP 是否有优势”。下一步不是继续扫 K、V、Q，而是先构造
> 一个无绕行、非饱和、可学习的 relay-required 任务，再做同样的因果使用
> 比较。
