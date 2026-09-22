# SAE 作为模型正则项的设计

## 1. 基本结构

SAE（Sparse Autoencoder，稀疏自编码器）被作为旁支插件接入 Transformer，而不是模型主干的一部分。

挂载位置是 Attention 的原生输出：

$$
a_l = W_O\bigl(\operatorname{Attention}(h_l)\bigr)
$$

也就是：

- 位于 Attention 输出投影 $W_O$ 之后；
- 位于残差相加之前；
- 不增加额外的 Norm；
- SAE 的重建结果不送入后续 MLP。

局部结构如下：

```text
                           ┌── SAE encoder ── sparse code z
                           │                       │
输入 h ── Attention ── W_O ── a ─────────────────┼── SAE decoder ── reconstruction â
                           │
                           └── 残差相加 ── Norm ── MLP ── 模型主干
```

因此，语言模型实际使用的仍然是原生 Attention 输出 $a$，而不是 SAE 重建结果 $\hat a$。

## 2. SAE 的作用

SAE 尝试把 Attention 输出表示为少量稀疏特征的组合：

$$
z = \operatorname{Encoder}(a)
$$

$$
\hat a = \operatorname{Decoder}(z)
$$

其中：

- $a$ 是原生 Attention 输出；
- $z$ 是稀疏特征激活；
- $\hat a$ 是 SAE 对 $a$ 的重建。

如果 $\hat a$ 能够准确重建 $a$，说明 Attention 表征可以被组织成一组较稀疏、可分解的特征。

## 3. 训练目标

总损失为：

$$
L_{\text{total}}
=
L_{\text{LM}}
+
\lambda_{\text{rec}}L_{\text{rec}}
+
\lambda_{\text{AuxK}}L_{\text{AuxK}}
$$

### 语言模型损失

$$
L_{\text{LM}}
$$

语言模型损失完全沿原模型主干计算，不经过 SAE。因此，SAE 不会用自己的重建结果替换模型原始表征。

### 重建损失

$$
L_{\text{rec}}
=
\frac{1}{N}\sum_{i=1}^{N}
\left\|a_i-\hat a_i\right\|_2^2
$$

它要求 SAE 尽可能准确地重建 Attention 输出。

该损失使用未截断梯度的 Attention 表征，因此梯度会更新：

- SAE 的编码器和解码器；
- 产生该表征的上游 Attention 参数。

因此，$L_{\text{rec}}$ 不仅训练 SAE，也对主模型施加正则约束：它鼓励 Attention 产生更容易被稀疏字典重建的表征。

### 防止死特征的辅助损失

$$
L_{\text{AuxK}}
$$

AuxK 用于激活长期不工作的 SAE 特征，避免大量特征永久“死亡”。

这一项在主干边界处执行梯度截断：

- 更新 SAE 参数；
- 不向 Attention 或其他主干参数传播梯度。

## 4. 梯度关系

```text
L_LM   ───────────────────────────────→ 模型主干

L_rec  ─────────→ SAE
       └────────→ 上游 Attention

L_AuxK ─────────→ SAE
       └─X──────→ 模型主干
```

因此，真正把 SAE 变成主模型正则项的是 $L_{\text{rec}}$。AuxK 只负责维持 SAE 自身的特征活性。

## 5. 推理阶段

推理时可以完全移除 SAE：

```text
训练：主干模型 + SAE 旁支
推理：仅主干模型
```

这是因为：

- SAE 重建从未进入语言模型主干；
- 模型输出不依赖 SAE；
- SAE 只通过训练阶段的梯度影响主模型参数。

所以该设计不会在推理时增加计算量、显存占用或延迟。

## 6. 核心理解

这套方法不是让模型“通过 SAE 进行推理”，而是：

> 在训练过程中，要求 Attention 表征既能完成语言建模，又能被稀疏特征较好地重建。

SAE 因而扮演一个可移除的训练期正则器：它约束表征的组织方式，但不改变模型的主干推理路径。