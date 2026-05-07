# 研究主线汇报包

## 0. 这份材料怎么用

这份材料服务三个目标：

1. 让组会时能在 30 秒到 1 分钟内把主线讲清楚；
2. 让老师一听就知道：我们不是在堆实验，而是在朝“**一学就会，永不遗忘**”这个终极目标收束；
3. 让后续每一步实验都知道自己在整条路线中的位置。

---

# 1. 先把总目标定下来

我们的终极目标不是一般意义上的专家分工，也不是只做一个静态语言模型收益更好的 MoE。

我们的终极目标是：

> **做一个能够支持“一学就会，永不遗忘”的 Hierarchical MoE。**

这句话拆开以后，意味着我们需要同时解决三件事：

1. **共享知识要稳**：语言里大量高频、通用、跨任务共享的结构，不能在学习新东西时被轻易破坏；
2. **新知识要能快速写入**：长尾领域、稀有模式、新概念要能用很少样本快速吸收；
3. **写入要局部、低干扰**：新知识不能粗暴写进整个共享空间，而应该写进更合适的可塑子空间。

所以我们从一开始就在做一件事：

> **先找到“什么空间该共享，什么空间该可塑”，再决定 MoE 应该怎么分层。**

---

# 2. 给每个阶段定基调

## Phase0：先把问题改对

### 基调
先纠正旧问题，不再把“专家参数不一样”当成真正的专一性。

### 这一阶段回答了什么
我们把问题从：

> 专家有没有分开？

改成：

> 被选中的专家，是否对当前 token 真有更低的下一词预测损失？

### 它对最终目标的意义
这一步决定了后面所有实验都必须围绕“功能收益”和“低干扰学习”来设计，而不是围绕表面分工来设计。

---

## Phase1-Phase3：先证明共享部分和长尾部分确实混在一起

### 基调
先做表征空间诊断，确认 raw hidden 里确实有一块强共享结构，不能直接拿来做专家分工。

### 这一阶段回答了什么
1. 真实 hidden state 中存在 shared head；
2. 去掉 shared head 后的 residual 在读出上更可分；
3. 去均值不是关键，去 centered covariance 的 shared head 才是关键；
4. Weight Decay / 学习率这条线在 toy 中有解释力，但在真实模型里不是当前主主线。

### 它对最终目标的意义
这一步告诉我们：如果想做“快速学习 + 低遗忘”，就不能把所有东西都丢给同一个共享参数空间。必须先想办法把共享/common 的大方差部分和可塑部分分开。

---

## Phase4-Phase6：先在真实模型里把单层机制钉住

### 基调
先不要急着做完整层级结构，先验证单层 factorized block 有没有真实语言建模价值。

### 这一阶段回答了什么
1. 单层 tail-conditioned block 在真实 Qwen 上优于 baseline FFN 和 flat raw MoE；
2. 最稳定的单因素收益来自：**expert 在 tail-oriented residual 上计算**；
3. router 是否必须只看 tail，还没有被证明；
4. 单层 block 已经出现真正的功能性专一性，而不只是表面分开；
5. recursive 方向不是错，而是 learned coarse routing 还没学出来。

### 它对最终目标的意义
这一步把主线从“表征猜想”推进到“真实 block 机制”。也就是说，我们已经不只是知道“哪里可分”，而是知道“怎样的单层结构真的更有任务价值”。

---

## Phase7-Phase8：进入 CL 前，先重写 expert input

### 基调
进入 continual learning 之前，先把 expert 应该看什么输入这件事重新做对。

### 这一阶段回答了什么
1. 不能再把 full PCA tail residual 直接当作 CL 版 expert input；
2. 真正有前景的是 middle / upper-middle 这一带；
3. 静态 old-stage 更偏窄而稳的 core band，也就是 `u25`；
4. 进入 CL 后，更偏更完整的 functional span，也就是 `u50_ext`；
5. 当前 CL 失败的首要原因不是 band 没切对，而是 adaptation horizon 太长，后几步发生了 over-update；
6. 现在终于进入了可以正式做 matched forgetting 比较的区间。

### 它对最终目标的意义
这一步不是“把主线推翻”，而是把主线从“单层静态 MoE”推进到了“面向 CL 的可塑空间设计”。

---

## 下一阶段：先裁决 CL，再回到 hierarchy

### 基调
现在最重要的不是继续切 band，也不是直接上 hierarchy，而是做一个能裁决主线是否成立的正式 CL 比较。

### 这一阶段要回答什么
在 matched learning gain 下，`G2_u50_ext` 或 `G4_u50_ext` 是否比 `G0` 忘得更少，是否接近或超过 `G0_ER`。

### 它对最终目标的意义
如果这一步成立，说明“共享分支 + 可塑 functional span”这条路线对“一学就会，永不遗忘”是有希望的；如果不成立，就要先修单层 CL 机制，不能强推 hierarchy。

---

# 3. 30 秒到 1 分钟的汇报说辞

## 版本 A：总主线版（45 秒）

我汇报的主题是：**我们怎样一步步把 MoE 从“专家分得开”推进到“更接近一学就会、永不遗忘”的层级结构。**

本阶段更新，我的核心结论是：**前六个阶段已经证明，真实 hidden 里存在 shared head，单层 tail-conditioned block 在真实模型上成立，而且真正稳定的收益来自 expert 在去 common/head 化的空间里计算。进入 Phase7-Phase8 后，我们进一步发现 full tail 过粗，进入 CL 更合适的 expert input 是 `u50_ext`，当前真正卡住的第一瓶颈是 adaptation horizon 太长，而不是 band 没切对。**

证据是：**Phase4-Phase6 证明了单层 block 的真实语言建模收益和功能性专一性；Phase7 否掉了“full tail 直接进 CL”；Phase8 smoke 说明 `u50_ext > u25`，而且短 horizon 已经进入可做 matched forgetting 比较的区间。**

我现在的理解是：**我们不是还没找到方向，而是已经把问题收缩到一个更具体的问题：共享部分如何稳定保留，可塑部分如何局部写入。当前最值得正式裁决的是 `u50_ext + short horizon` 这条 CL 主线。**

还不确定的是：**这种 factorized block 是否真的比 dense baseline 更适合 continual learning；以及 router 在 CL 里到底带来多大额外价值。**

下一步我想做：**固定 `u50_ext`，固定短 horizon，正式做 matched forgetting 比较，只比较 `G0`、`G0_ER`、`G2_u50_ext`、`G4_u50_ext`。**

---

## 版本 B：当前阶段版（30 秒）

我汇报的主题是：**进入 continual learning 之前，expert input 应该怎么重定义。**

本阶段更新，我的核心结论是：**full PCA tail residual 不适合作为 CL 第一版 expert input，进入 CL 后模型更偏向 `u50_ext`，并且当前主要失败来源是 adaptation horizon 过长。**

证据是：**Phase7 的 gate 否掉了 full tail 直接进 CL；Phase7.6 说明静态最稳的是 `u25`，但功能覆盖更强的是 `u50`；Phase8-smoke 和 Phase8.1 说明 CL 更偏向 `u50_ext`，并且 `U=4/8` 已经进入正 learning gain 区间。**

我现在的理解是：**对 CL 来说，更重要的不是最窄 core，而是更完整的 functional span。**

还不确定的是：**在 matched learning gain 下，`G2_u50_ext` 或 `G4_u50_ext` 能否真正比 `G0` 忘得更少。**

下一步我想做：**回到 formal matched forgetting，而不是继续切 band 或直接进 hierarchy。**

---

# 4. 当前最重要的 3 个假设

## 假设 1
**如果要支持“一学就会，永不遗忘”，模型内部必须把共享/common 空间和可塑学习空间分开。**

直白讲就是：

> 通用语言知识不能和长尾新知识一直挤在一个空间里更新。

---

## 假设 2
**对 CL 来说，更合适的 expert input 不是 full tail，也不是最窄的 core，而是更完整的 functional span，也就是 `u50_ext`。**

直白讲就是：

> 静态 block replacement 更喜欢“干净、窄、稳”的输入；但一旦进入新知识适配，模型需要的是“功能覆盖更完整”的输入。

---

## 假设 3
**如果固定 `u50_ext` 并限制 adaptation horizon，factorized block 应该能在 matched learning gain 下比普通 dense 更少遗忘；如果这一步成立，才值得继续推进真正的 hierarchical MoE。**

直白讲就是：

> 先证明单层 CL 值得做，再回来做 hierarchy；不能跳步。

---

# 5. 按学长模板整理最重要的实验和证据

## 实验 1：真实 hidden 里有没有 shared head

**假设：** 语言的 Zipf 分布会在真实 hidden state 中形成一块高方差共享结构，这块结构会遮住真正适合专家学习的长尾变化。

**实验：** 在真实 Qwen hidden 上做 centered covariance 的 PCA，比较 raw、centered、tail residual 在 domain probe、purity、NMI 上的差异。

**结论：**
1. 真实 hidden 中确实存在 shared head；
2. 去掉 shared head 后的 tail residual 在读出上更可分；
3. 去均值不是关键，去掉 shared high-variance head 才是非平凡操作。

**它证明了什么：**
> 专家不该直接吃 raw hidden；至少需要先做一次 global common/head 去除。

---

## 实验 2：统一 Weight Decay 会不会压死 tail

**假设：** 如果共享部分和 tail 共用统一正则，低方差、低占用的 tail 方向会更容易被压制。

**实验：** 在线性 toy 中写出带正则的最优解，比较不同方差方向的 survival factor；再把 expert 占用率引入最小模型。

**结论：**
1. 低方差方向的 survival factor 更小；
2. 低占用 expert 也会更容易被统一正则压制；
3. 但这是 toy 机制，不能直接等价为真实模型主机制。

**它证明了什么：**
> 优化器确实可能伤害 tail，但真实主线不能只靠 WD/LR 解耦来解释。

---

## 实验 3：单层 tail-conditioned block 在真实模型上能不能站住

**假设：** 如果 expert 在去 common/head 化后的空间里计算，单层 block 就应该比 baseline FFN 和 flat raw MoE 更好。

**实验：** 在 Qwen3-0.6B 的第 8 层替换 FFN block，比对 `baseline_ffn`、`flat_moe_raw_uniform`、`hier_moe_tail_uniform`。

**结论：**
1. `hier_moe_tail_uniform` 优于 `baseline_ffn`；
2. `hier_moe_tail_uniform` 也优于 `flat_moe_raw_uniform`；
3. 所以真正有效的不是“有多个 expert”本身，而是“专家在 tail-oriented 空间里计算”。

**它证明了什么：**
> 单层 factorized tail-conditioned block 在真实模型上不是空想，而是有真实语言建模收益。

---

## 实验 4：到底是 router 看 tail 更重要，还是 expert 看 tail 更重要

**假设：** 当前主收益不是来自 router-only 的 tail 输入，而是来自 expert 输入空间改变。

**实验：** 做机制消融，比较 raw-router/raw-expert、tail-router/raw-expert、raw-router/tail-expert、tail-router/tail-expert。

**结论：**
1. 最稳定的提升来自 `expert: x -> x_t`；
2. 单独让 router 看 tail，不如让 expert 看 tail 稳定；
3. 当前更成熟的说法是：tail residual 更像是 expert computation space，不一定是唯一最优 router input。

**它证明了什么：**
> 结构设计的重点先放在 expert 输入空间，而不是先死盯 router 输入。

---

## 实验 5：我们现在说的专一性，到底是不是真正有用

**假设：** 有价值的 expert 专一性，不是 purity/NMI 高，而是被选 expert 对当前 token 真有更低的下一词损失。

**实验：** 定义反事实 expert gap
$$
G_{\mathrm{cf}}(e')
=
\mathbb{E}\left[\ell(y,f_{e'}(c))-\ell(y,f_{e^\star}(c))\right]
$$
比较被选 expert 和替代 expert 的损失差。

**结论：**
1. 单层 tail-conditioned block 在 middle / rare token 上有正 gap；
2. no-LB 下仍然成立；
3. 这说明当前已经出现真正有任务价值的功能性专一性。

**它证明了什么：**
> 我们已经把“专家分得开”推进到了“专家分得好”。

---

## 实验 6：recursive 为什么一直起不来

**假设：** 如果 hierarchical MoE 真的有潜力，当前 learned recursive 失败的第一瓶颈应该是 coarse routing，而不是 fine routing。

**实验：** 在 synthetic recursive setting 中比较 `R5`、`R5c`、`R5d`、`R6`。

**结论：**
1. 只把 coarse routing 换成 oracle，性能大幅改善；
2. 只修 fine-local routing，几乎不改善；
3. 所以 recursive 的第一瓶颈是 coarse routing。

**它证明了什么：**
> hierarchy 方向还没死，但现在不能直接扩真实 recursive，必须先把 coarse objective 设计对。

---

## 实验 7：进入 CL 后，full tail 还适合做 expert input 吗

**假设：** full PCA tail residual 太粗，真正适合 CL 的可塑空间应该是 middle / upper-middle 这类 functional span。

**实验：** 做 Phase7 的 probe、functional intervention、PCA top-K 与 sparse dictionary top-K 比较；再做 `u25`、`u50_ext` 的候选筛选与 CL smoke。

**结论：**
1. Phase7 否掉了“full tail 直接进 CL”；
2. 静态 old-stage 更偏 `u25`；
3. 进入 CL 后更偏 `u50_ext`；
4. 当前首要失败原因是 horizon 太长，不是 band 选错。

**它证明了什么：**
> CL 版 expert input 需要重新定义，当前最合理的候选是 `u50_ext`。

---

# 6. 一秒钟就能明白的提纲

## 提纲 1：我们到底在做什么

### 一句话
我们在为“一学就会，永不遗忘”的 Hierarchical MoE 找到一个正确的单层基础块。

### 这句话后面接什么
1. 先证明共享/common 结构真实存在；
2. 再证明专家应该在去 common/head 化后的空间里计算；
3. 再证明这种单层结构已经出现真正有任务价值的专一性；
4. 再把这个机制改成更适合 continual learning 的输入定义；
5. 最后才回到真正的 hierarchy。

### Shang 老师最可能问 1
**“为什么你们一直在做单层，不直接做最终的 hierarchical MoE？”**

**引导式回答：**
尚老师，正如我们之前讨论的，真正的 hierarchy 必须建立在一个已经站住的单层可塑模块之上。我这次顺着这个思路做了验证，发现当前真正稳定成立的是“expert 在去 common/head 化后的空间里计算”，而 learned recursive 还卡在 coarse routing，所以如果现在直接扩 hierarchy，问题会被搅乱，而不是被解决。

### Shang 老师最可能问 2
**“你们现在到底证明了什么，不是在不断换说法吗？”**

**引导式回答：**
尚老师，正如我们之前讨论的，研究里最怕的是把“看起来分开”误当成“真的有用”。我这次顺着这个思路回看，发现我们真正固化下来的不是某一个 band 永远最优，而是三件更硬的事：shared head 真实存在，expert-tail computation 是当前最稳机制，单层 block 已经有功能性专一性。后面的 Phase7-Phase8 不是推翻，而是把这套机制改写成更适合 continual learning 的版本。

---

## 提纲 2：当前阶段最核心的结论是什么

### 一句话
当前阶段最核心的结论是：进入 CL 后，full tail 太粗，模型更偏向 `u50_ext`，而且当前第一瓶颈是 over-update。

### 这句话后面接什么
1. `u25` 是静态最稳 core；
2. `u50` 承载更多功能；
3. `u50_ext` 是当前 CL 最好的候选输入；
4. `U=16/32` 过长，`U=4/8` 才是可比区间；
5. 下一步要做 formal matched forgetting。

### Shang 老师最可能问 1
**“既然 `u25` 静态最好，为什么不直接用 `u25` 进 CL？”**

**引导式回答：**
尚老师，正如我们之前讨论的，静态 block replacement 的“最稳输入”和 continual learning 的“最有功能覆盖输入”不一定相同。我这次顺着这个思路把 `u25` 和 `u50_ext` 都带进 CL smoke，发现进入 CL 后模型更偏 `u50_ext`。这说明 CL 更需要完整 functional span，而不只是最窄、最干净的 core。

### Shang 老师最可能问 2
**“会不会不是 band 的问题，而是你们训练没调好？”**

**引导式回答：**
尚老师，正如我们之前讨论的，我这次把 band 问题和训练问题拆开了。Phase8.1 固定 `u50_ext` 后专门扫了 horizon 和学习率，结果发现真正的系统性失败来自 horizon 太长，而不是 band 再切不细。这也是为什么我认为下一步应该回到短 horizon 的 formal matched forgetting，而不是继续切谱空间。

---

## 提纲 3：下一步为什么不继续切 band、不直接上 hierarchy

### 一句话
因为现在最缺的不是更多候选，而是一个能真正裁决主线是否成立的 CL 正式比较。

### 这句话后面接什么
1. band 已经从 full tail 收缩到 `u50_ext`；
2. horizon 已经从无序状态收缩到 `U=8` 左右；
3. 现在该回答的是：在 matched learning gain 下，谁忘得更少；
4. 只有这个问题答完，hierarchy 才有资格继续。

### Shang 老师最可能问 1
**“为什么不趁热把 router 也继续做大，或者直接做 recursive？”**

**引导式回答：**
尚老师，正如我们之前讨论的，如果单层 CL 主线还没有正式站住，继续加 router 复杂度或直接做 recursive，只会让解释空间变大。我这次顺着已有结果回看，发现现在最该裁决的是 `G2_u50_ext` 和 `G4_u50_ext` 在 matched forgetting 下到底能不能赢 `G0` 和接近 `G0_ER`。这一步是 hierarchy 之前的必答题。

### Shang 老师最可能问 2
**“如果 formal matched forgetting 做出来还是不行，那前面这些工作还有意义吗？”**

**引导式回答：**
尚老师，正如我们之前讨论的，研究里很重要的一件事就是把错误的解释排掉。我这次回看后觉得，前面的工作已经帮我们排掉了很多伪主线：不是 flat raw MoE，不是 WD/LR 强解耦，不是 full tail 整块 residual，也不是现在就能上的 learned recursive。即使 formal CL 不通过，这些排错本身也把问题收缩到了很明确的边界。

---

# 7. 当前最稳的模型图景

如果现在必须给出一个负责任的模型图景，我建议这样讲：

## 当前最稳的一层结构
$$
h_{\mathrm{out}}
=
h_{\mathrm{in}} + F_c(x) + F_t(x_{\mathrm{plastic}})
$$

其中：

- $F_c(x)$ 负责稳定共享/common 部分；
- $x_{\mathrm{plastic}}$ 是更适合可塑写入的子空间；
- 当前进入 CL 时，最有前景的 $x_{\mathrm{plastic}}$ 是 `u50_ext`。

## 当前最有希望的 routed 版本
$$
h_{\mathrm{out}}
=
h_{\mathrm{in}} + F_c(x) + \sum_e g_e(x)F_e(x_{u50\_ext})
$$

也就是：

- router 先继续看 raw $x$；
- experts 在 `u50_ext` 上计算。

这不是最终 hierarchy，只是当前最合理的单层 CL 候选。

---

# 8. 现在能强讲什么，不能强讲什么

## 能强讲的
1. shared head 是真实存在的；
2. flat raw MoE 不是好方向；
3. expert 在 tail-oriented residual 上计算是当前最稳结构信号；
4. 单层 block 已经出现真正有任务价值的专一性；
5. full tail 不适合作为 CL 第一版 expert input；
6. 进入 CL 后更偏 `u50_ext`；
7. 当前 CL 第一瓶颈是 horizon 太长。

## 不能强讲的
1. 不能说 router 一定只该看 tail；
2. 不能说 dictionary 已经能直接替代当前 residual 定义；
3. 不能说 routing 已经带来本质性的 CL 增益；
4. 不能说 hierarchy ready；
5. 不能说 full Phase8 ready；
6. 不能说我们已经得到最终 Hierarchical MoE。

---

# 9. 最后一句总收束

> **我们现在不是还没有主线，而是已经把主线收缩到了一个非常具体的问题：在 `u50_ext + short horizon` 这个 regime 下，稳定 common 分支加可塑 expert 分支，能不能在 matched learning gain 下比普通 dense 更少遗忘。只要这一步站住，真正的 Hierarchical MoE 才有资格继续推进。**
