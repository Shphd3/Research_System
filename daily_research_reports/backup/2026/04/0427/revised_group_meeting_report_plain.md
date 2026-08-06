# 组会汇报：Common / Long-tail 分开学习与下一步 Stage A

## 1. 目的

我目前想验证的是：

> 将 common 信息和 long-tail / specific 信息分开学习，是否能够降低 continual learning 中的干扰，让模型学新领域更快，同时旧领域遗忘更少。

这里的 continual learning 指的是：

1. 先让模块在 old domain 上学习；
2. 再用 new domain 的少量 support data 适配；
3. 观察两个指标：
   - 新领域是否学得更好；
   - 旧领域是否遗忘更少。

---

## 2. 原始假设

原来的假设是：

> 如果把 hidden representation 按 variance band 划分，把 common / high-variance 方向和 tail / low-variance 方向交给不同 branch 学习，那么模型可能在 toy CL 中同时降低旧任务遗忘，并保持新任务学习能力。

two-branch 形式是：

$$
h_{\text{out}} = h_{\text{in}} + F_c(x) + F_t(x_{\text{candidate}})
$$

其中：

- $F_c(x)$ 是 common branch；
- $F_t(x_{\text{candidate}})$ 是 tail / plastic branch；
- $x_{\text{candidate}}$ 可以是 `u50`、`ext`、`u50_ext`、`full_tail_resid` 或 random subspace。

matched dense baseline 是：

$$
h_{\text{out}} = h_{\text{in}} + F_{\text{dense}}(x)
$$

它用来排除“只是参数更多”的解释。

---

## 3. 当前实验结论

目前的结果不支持这个强假设。

更准确地说，结果说明：

> 现在看到的收益，还不能归因于“真实 variance band split”。它可能来自参数量、two-branch 结构、随机投影、任务设置，或者 branch 本身的表达能力。

### 3.1 H3 direct causal audit 的结果

H3 direct audit 中，matched dense 和 raw two-branch 在 new adaptation 后反而让 old loss 下降，并且 new-domain learning gain 很大。比如：

- matched dense: $F_{\text{old}}=-0.025405$, $G_{\text{new}}=0.026537$
- raw two-branch: $F_{\text{old}}=-0.034429$, $G_{\text{new}}=0.034492$
- random split: $F_{\text{old}}=-0.004928$, $G_{\text{new}}=0.005209$
- `u50_ext`: $F_{\text{old}}=-0.001189$, $G_{\text{new}}=0.001416$

这说明 direct-adaptation setting 中没有形成明显的 positive forgetting，而且真实 variance-band split 没有打赢 dense、raw two-branch 或 random split。

### 3.2 Phase8-H3 bridge old-stage audit 的结果

后来我们把 H3-style controls 放回 old-stage 协议中：先 old-stage 训练，再做 new-stage adaptation。

这个协议更接近真正的 CL，因为模块先形成 old-domain state，再被 new-domain support 干扰。

但结果仍然很弱。主要现象是：

- matched dense 有轻微 forgetting，但 new learning 反而为负；
- replay baseline 更稳定；
- `ext`、`full_tail_resid`、`u50_ext` 有一点点更好的 tradeoff；
- 但数值都在 $10^{-3}$ 量级，不能支持强结论。

所以当前不能说：

> common / tail split 已经明显降低遗忘。

只能说：

> 在 old-stage 协议下，tail-oriented split 有一些弱信号，但还不足以支撑 hierarchy 或 many-branch 设计。

---

## 4. 当前应该降级的 claim

现在不能说：

1. `u50_ext` 已经是验证过的 CL plastic input；
2. variance-band split 已经降低 forgetting；
3. two-branch 成功，所以 many-branch / hierarchy 会更好；
4. branch ablation 里 rare token contribution 大，就说明 expert specialization 已经成立；
5. Zipfian distribution 能直接推出 domain-specific hierarchy。

现在可以说：

1. H3 causal audit 已经完成，并且结果不支持原来的强假设；
2. old-stage 协议和 direct-adaptation 协议测的对象不同；
3. 当前更稳妥的下一步是重新检查：Zipfian / long-tail 是否真的在 hidden representation 中形成了可分的层级因素；
4. 如果没有这个证据，就不应该直接做更多 experts。

---

## 5. Zipfian 和 domain-specific hierarchy 的关系

我现在的理解是：

> Zipfian 不能直接推出 domain-specific 分层。

更严谨的逻辑应该是：

$$
\text{Zipfian token distribution}
\rightarrow
\text{token / feature activation frequency is uneven}
$$

$$
\rightarrow
\text{some rare or mid-frequency tokens may be domain-concentrated}
$$

$$
\rightarrow
\text{hidden representation may contain common factors and domain-specific residual factors}
$$

$$
\rightarrow
\text{experts may benefit from processing these factors separately}
$$

也就是说，domain-specific hierarchy 不是 Zipfian 的直接结论，而是一个需要验证的中间假设。

我们需要先检查：

1. 低频或中频 token 是否更容易集中在某些 domain；
2. hidden representation 中是否存在对应的 domain-specific feature；
3. 这些 feature 是否对 next-token prediction 有功能贡献；
4. router / expert 是否能利用这些 feature 做出更好的选择。

---

## 6. 下一步 Stage A

下一步我不直接做 full hierarchical MoE。

我先做 Stage A：

> 检查 Zipfian / long-tail 是否真的在真实 LLM hidden state 中诱导出可分、可测、有功能贡献的层级因素。

Stage A 先不追求最终性能，而是回答：

1. token frequency 和 domain concentration 是否有关；
2. representation operator 是否能把 common / domain-specific / token-specific 成分分开；
3. 这些成分是否对 NTP loss 有真实贡献；
4. random split 是否也能做到同样事情。

---

## 7. 预期可能结果

### 情况 A：支持我们的方向

如果发现：

1. mid / rare tokens 更 domain-concentrated；
2. tail residual 或 sparse residual features 比 raw / random 更能恢复 domain 或 signature token；
3. 去掉这些 features 会显著伤害 domain-specific 或 rare-token NTP loss；

那么说明：

> Zipfian / long-tail 可能确实诱导了可分的 domain-specific 或 token-specific factors。这样才有理由继续做 more branches 或 hierarchy。

### 情况 B：不支持 domain hierarchy

如果发现：

1. token frequency 和 domain concentration 没关系；
2. random split 和真实 split 效果差不多；
3. feature 看起来稀疏，但去掉后 NTP loss 没变化；

那么说明：

> domain-specific hierarchy 不是当前最合适的方向。我们应该转向 token-function / feature-activation 口径，而不是按 domain 做 hierarchy。

---

## 8. 30 秒口头版

我现在的结论是：之前 common / long-tail 分开学的假设，在严格 causal audit 下没有被支持。matched dense、raw two-branch 和 random split 都能解释一部分现象，所以我不能直接把 two-branch 外推到 many-branch hierarchy。  
现在我把问题往前退一步：Zipfian 只能说明 token frequency 不均匀，它不能直接推出 domain-specific hierarchy。中间必须验证：低频或中频 token 是否更 domain-concentrated，hidden representation 里是否有对应的 specific features，这些 features 是否真的影响 NTP loss。  
所以下一步 Stage A 我会先做 representation decomposition audit，比较 raw、PCA band、tail residual、random split 和 sparse residual features，判断什么 operator 能把 common / domain-specific / token-specific 信息分开。如果这一步成立，再讨论 router 和 hierarchical experts。
