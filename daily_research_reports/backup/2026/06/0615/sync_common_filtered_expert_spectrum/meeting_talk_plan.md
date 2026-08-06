# Meeting Talk Plan: Common-Filtered Expert-Spectrum Router Initialization

## **Goal**

这次会议的目标不是把 A06_01 讲成失败，而是讲成一次有效的 uncertainty reduction：

```text
导师 intuition 被实现了；
其中一部分机制成立；
但当前线性 top-1 router 初始化不是成功方法；
下一步应转向更窄的 early-training 放大机制审计。
```

## **Opening**

建议开场 30 秒这样讲：

```text
上次老师提出的核心 intuition 是：router 初始化不应该随便来，而应该利用 expert 初始化后的高增益方向。我们把这个想法做成了一个完整实验，并且专门处理了老师提醒的 common feature 问题。

结果是：这个想法在第 0 步确实改善了 token 分布，但没有挡住第 10 步训练放大。所以它现在不是一个成功方法，但它帮助我们把问题从“初始化是否均匀”推进到“早期训练如何放大一个优势 expert”。
```

## **Storyline**

### 1. First agree with the advisor's premise

先承认导师的直觉有合理部分：

```text
独立高斯初始化后的 experts 不是完全一样的。
我们测到不同 expert 的高增益子空间重合很低，平均约 0.0116。
所以从 expert 初始化里找 routing signal 是有意义的。
```

不要说：

```text
专家已经负责不同语义子空间。
```

更稳妥说法：

```text
几何上不同，但功能分工还没有证明。
```

### 2. Then separate two objects

要明确区分：

```text
专家谱方向本身
vs
把谱分数压缩成线性 router 行后的实现
```

建议说：

```text
我们发现 expert top directions 和 representation common directions 的直接 overlap 很低，约 0.0166。所以问题不是 expert spectrum 本身等于 common direction。

真正的问题出现在 implementation bridge：raw spectrum 压成线性 router row 后，common projection 反而很大。
```

### 3. Give the partial positive result

这一步很重要，避免让导师觉得我们只是做了一个 negative result。

建议说：

```text
common-filtered 版本确实把第 0 步路由变均匀了。去掉前 1% 高频 token 后，random 的负载第一 expert 是 19.98%，V4 降到 13.97%，接近均匀基线 12.5%。

所以这个初始化不是没有作用。它确实解决了一部分初始 common bias。
```

### 4. Then state the decisive failure

建议说：

```text
但是第 10 步没有被改善。去掉前 1% 高频 token 后，V4 第 10 步负载第一 expert 到 93.51%，比 random 的 83.16% 更严重。

所以不能把 V4 当作成功方法。它改善起点，但没有改善训练动力学。
```

### 5. Connect back to 0614

建议说：

```text
这和 0614 的结果一致。0614 已经说明 step-10 spike 不是 gate-only，而是 hidden drift 和 gate-hidden interaction 参与。因此只修正初始化，不一定能阻断训练放大。
```

## **Boundary To Say Clearly**

可以说：

```text
1. 专家谱里有弱信号；
2. 去共同方向后的线性初始化改善第 0 步负载均匀性；
3. 当前线性 top-1 实现不能解决第 10 步集中；
4. 剩下的问题是早期训练如何放大优势 expert。
```

不要说：

```text
1. 专家谱无用；
2. 导师的想法错了；
3. 所有基于谱的 router 都会失败；
4. experts already specialize into meaningful subspaces；
5. high-frequency tokens are irrelevant during training.
```

如果导师问“那这个方向是不是不行了”，建议回答：

```text
当前 linear initialization 不支持继续作为方法推进。但这个方向还没有被完全否定，因为 oracle / quadratic / learned classifier bridge 没有测。现在更合理的是先确认失败来自 computation 本身，还是来自 linear implementation bridge。
```

## **Likely Advisor Questions**

### Q1: Expert Initialization Coverage

回答：

```text
几何上有覆盖差异。不同专家高增益子空间重合低，说明 experts 不是完全一样。

但“覆盖空间”不是等于“能形成有用 routing”。我们现在只能 claim 几何差异和弱 utility signal，不能 claim 功能分工。
```

### Q2: Expert-Representation Alignment

回答：

```text
和 common top directions 不强 align。overlap 大约 0.0166。

所以 common 问题不是 expert subspace 本身直接 common，而是 spectrum score 线性化成 router rows 后产生 common projection。
```

### Q3: Why V4 Is More Balanced At Step 0

回答：

```text
因为 V4 去掉了 router rows 上的 common projection。共同方向不再给某些 experts 全局加分，所以第 0 步分布更接近均匀。
```

### Q4: Why Step 10 Still Gets Worse

回答：

```text
这说明主要问题不只是初始分布。0614 的 replay / freeze split 已经显示，step-10 spike 需要 hidden drift 和 gate-hidden interaction。V4 修了起点，但没有修训练过程中的放大通道。
```

### Q5: Minimal Next Step

回答：

```text
先不扩大新实验，做 existing checkpoints 的 post-hoc audit：
看第 0 步 common-aligned winner 是否在前 10 步被 router update 进一步放大。

如果是，说明存在 router self-reinforcement。
如果不是，就转向 hidden drift、position structure 或 expert-output feedback。
```

## **Suggested Closing**

建议最后这样收：

```text
所以这次不是一个 positive method result，但它把问题推进了一层：我们已经知道 common-filtered expert-spectrum linear init 能改善初始 balance，却不能阻止 step-10 amplification。

我建议下一步不要先扩大模型或训练，而是先做一个 existing-checkpoint 的更新方向审计，把 early amplification 的直接来源拆出来。
```
