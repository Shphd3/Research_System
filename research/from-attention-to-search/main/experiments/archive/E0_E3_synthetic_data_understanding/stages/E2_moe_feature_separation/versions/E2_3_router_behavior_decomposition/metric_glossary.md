# Metric Glossary: E2.3 Router Behavior Decomposition

本文件只解释指标含义：每个指标在问什么、验证什么、如何读结果。

## 1. 基础记录项

| 名称 | 中文含义 | 用途 |
|---|---|---|
| `feature_id` | 人工序列规则编号，例如 ABC / DEF / GHI / JKL | 判断 router 是否按人工 feature 分 expert |
| `A_token` | feature prefix 的第一个 token | 判断完整上下文关系是否重要 |
| `B_token` | prefix-end token，也就是负责预测 target 的位置 | 检查 router 是否只看最后一个 prefix token |
| `target_token` | 需要预测的下一个 token | 检查 router 是否按目标 token 分 expert |
| `selected_expert` | router 最终选择的 expert 编号 | 本实验要解释的核心对象 |
| `router_logits` | router 给每个 expert 的原始分数 | 看 router 对每个 expert 的偏好强弱 |
| `router_margin` | 第一名 expert 分数减第二名 expert 分数 | 越大表示 router 越坚定 |
| `router_entropy` | router 分布的不确定性 | 越大表示 router 越犹豫 |
| `hidden_norm` | hidden state 向量长度 | 检查 router 是否按向量尺度分 expert |
| `target_prob` | 模型给正确 target 的概率 | 检查 router 是否按预测置信度分 expert |
| `ce_loss` | 预测正确 target 的错误程度 | 检查 router 是否按样本难度分 expert |

## 2. 解释力指标

### Expert-id prediction accuracy

中文：专家选择预测准确率。

含义：只用某一类变量，例如 `feature_id` 或 `B_token`，去预测 router 选了哪个 expert，预测对了多少。

验证问题：

```text
哪类变量最像 router 实际使用的依据？
```

读法：

- `feature_id` 准确率最高：router 可能主要按人工 feature 分。
- `B_token` 准确率接近 full hidden：router 可能只看 prefix-end token。
- `hidden_norm / ce_loss` 准确率高：router 可能按尺度或难度分。

### Expert-id NLL

中文：专家选择预测负对数损失。

含义：预测 expert 时，不只看猜没猜对，还看预测是否有把握。越低越好。

验证问题：

```text
哪个变量组不只是偶尔猜对，而是稳定解释 expert choice？
```

读法：

- accuracy 高但 NLL 不低：说明预测可能不稳定。
- NLL 明显低：说明该变量组对 expert choice 有稳健解释力。

### McFadden pseudo-R2

中文：相对解释提升。

含义：相比“永远猜最常用 expert”这个简单基线，某组变量多解释了多少 expert choice。

验证问题：

```text
这个变量组是否比只猜多数 expert 真正有用？
```

读法：

- 接近 0：几乎没有解释力。
- 明显大于 0：比 majority baseline 有额外解释力。

### Mutual information

中文：共享信息量。

含义：某个变量和 expert choice 之间共享多少信息。

验证问题：

```text
feature、token、frequency、norm 哪个和 expert choice 关系更强？
```

读法：

- `B_token` mutual information 高：token shortcut 风险高。
- `feature_id` 高：routing 与人工 feature 关系强。

### Conditional permutation importance

中文：控制其他变量后的打乱重要性。

含义：先把多个变量一起放进模型，再单独打乱某个变量，看预测 expert 的能力下降多少。

验证问题：

```text
某个变量是否有独立解释力，而不是被别的变量替代？
```

读法：

- 打乱 `feature_id` 后预测明显变差：feature_id 有独立作用。
- 控制 `B_token` 后打乱 `feature_id` 几乎没影响：feature_id 可能只是 token shortcut 的影子。

## 3. 控制性指标

### Within-B-token feature effect

中文：固定 B token 后的 feature 作用。

含义：只比较相同 `B_token` 的样本，看 feature 信息是否还能解释 expert choice。

验证问题：

```text
router 是看完整 [A,B] 关系，还是只看 B？
```

读法：

- 固定 B 后 feature 仍有效：支持 relation-level feature。
- 固定 B 后 feature 无效：说明 routing 可能主要依赖 B token。

注意：当前原始 E2 数据里每个 feature 的 B token 不同，所以这个指标在原始数据上能力有限；真正强检验需要 shared-B 新数据。

### Within-norm bucket feature effect

中文：固定 hidden 向量大小后的 feature 作用。

含义：把 hidden norm 类似的样本放在一起，再看 feature 是否还能解释 expert。

验证问题：

```text
router 是按 feature 分，还是按 hidden 向量大小分？
```

读法：

- 固定 norm 后 feature 仍有效：feature 有独立解释力。
- 固定 norm 后 feature 无效：router 可能按 activation scale 分。

### Within-CE bucket feature effect

中文：固定预测难度后的 feature 作用。

含义：把 CE loss 类似的样本放在一起，再看 feature 是否还能解释 expert。

验证问题：

```text
router 是按 feature 分，还是按样本难度分？
```

读法：

- 固定 CE 后 feature 仍有效：feature 有独立解释力。
- 固定 CE 后 feature 无效：router 可能按 easy/hard sample 分。

## 4. 表征与方向指标

### Feature linear probe accuracy

中文：从 hidden state 读出 feature 的准确率。

含义：训练一个简单线性分类器，用 hidden state 预测 ABC / DEF / GHI / JKL。

验证问题：

```text
feature identity 是否真的在线性层面存在于 router input hidden state 中？
```

读法：

- 准确率高：feature representation 可读出。
- 准确率低：PCA 图上看起来分开可能不可靠。

### PCA-coordinate predictor

中文：PCA 坐标解释 expert 的能力。

含义：只用 PCA 前几个坐标预测 expert choice。

验证问题：

```text
router 是否沿着人眼最容易看到的高方差方向分 expert？
```

读法：

- PCA 能解释 expert：router 可能使用可视化中看到的主方向。
- PCA 不能解释 expert：router 可能使用别的方向。

### Router-projection predictor

中文：router 权重方向解释 expert 的能力。

含义：用 router 自己的线性打分方向，例如 $W_{router}h$，预测 expert choice。

验证问题：

```text
expert choice 是否由 router 自己敏感的方向决定？
```

读法：

- router projection 解释力高但 PCA 低：router 使用的不是 PCA 主方向。
- router projection 也低：需要检查非线性、噪声或实现问题。

### Feature-subspace projection intervention

中文：去掉 feature 方向后的干预。

含义：从 hidden state 中移除能区分 feature 的方向，再看 expert choice 和 feature probe 变化。

验证问题：

```text
router 是否真的使用 feature-separating directions？
```

读法：

- feature probe 下降，但 expert choice 不变：router 没用 feature 方向。
- feature probe 和 expert choice 都变：router 用了 feature 方向。

## 5. 路由必要性指标

### Learned vs oracle vs random routing readback

中文：已学习路由、人工 feature 路由、随机路由的读回对比。

含义：

- learned routing：模型自己学到的 router；
- oracle routing：人为规定 ABC 去 expert 0、DEF 去 expert 1 等；
- random routing：随机选 expert，但保持总体 expert 使用比例。

验证问题：

```text
clean one-feature-one-expert 对当前 NTP 任务是否真的有用？
```

读法：

- oracle 明显更好：模型可能没有学到更优 feature partition。
- oracle 差不多：clean partition 对 loss 不是必要解。
- random 也差不多：feature prediction 可能主要绕过 expert path。

### Expert-path necessity

中文：expert 路径必要性。

含义：把 selected expert 输出置零、替换成平均输出，或随机换 expert，看 feature readback 是否崩掉。

验证问题：

```text
feature prediction 是否真的依赖 selected expert？
```

读法：

- readback 大幅下降：selected expert 对 feature prediction 必要。
- readback 基本不变：prediction 可能由 shared path 或多个 experts 共同承担。

## 6. 最重要的组合判据

最支持 E2.3 主 claim 的组合是：

```text
feature linear probe accuracy 高
但 feature_id 不能最好解释 selected_expert
并且去掉 feature subspace 不怎么改变 expert choice
```

它说明：

```text
hidden state 里能读出 feature，
但 learned router 没有按这些 feature directions 分 expert。
```

最危险的 shortcut 组合是：

```text
B_token 可以几乎完美预测 expert choice
并且控制 B_token 后 feature_id 没有额外解释力
```

它说明：

```text
当前 routing 可能只是 token shortcut，
不是完整 context relation 的 expert specialization。
```
