# 文章分析报告：MoE Expert Specialization 的“几何解释”与线性 Router 不形成 one-feature-one-expert 的关系

**论文**：*The Myth of Expert Specialization in MoEs: Why Routing Reflects Geometry, Not Necessarily Domain Expertise*  
**阅读目标**：理解普通线性 router 在训练中到底按什么原则分发 token；特别是为什么在合成 trigram NTP 设置中，feature 表征可分但没有形成严格的 one-feature-one-expert。  
**项目锚点**：long-context attention as model-native search over dynamic KV memory；MoE/H-MoE routing 作为潜在 memory indexing / candidate retrieval 机制。

---

## 0. 最短结论

这篇文章给出的最有用更新是：**线性 MoE router 的专家使用模式首先是 hidden-state geometry 经过一个线性投影后的结果，而不是一个自动学习“人类定义 feature/domain -> expert”的聚类器。** 因此，在你的合成实验里，即使 feature identity 在 router input hidden space 中线性可分、centroid 可分、Fisher ratio 高，也不推出 router 的 row-difference/boundary directions 会对齐这些 feature-difference directions；如果 NTP loss 可以通过多个 experts、共享路径、target shortcut 或低 margin routing 被满足，那么 one-feature-one-expert 没有被目标函数强制出来。

---

## 1. Paper Summary

论文要解释 MoE 中所谓 “expert specialization” 的来源：观察上不同 domain/sequence 会激活不同 experts，但这是否意味着 experts 学到了人类可解释的 domain expertise 并不清楚。作者的核心观点是：token-choice MoE router 通常是线性映射 $g = Ph$，所以 expert usage similarity 很大程度上由 hidden states 的几何关系和 router 对这些方向的投影决定。论文用一个 data-geometry-aware upper bound 说明：hidden states 相似时，router logits 必须相似；但 hidden states 不相似时，router logits 仍然可能相似，因此 routing 是多对一、不可直接语义解释的。作者还分析了 load-balancing loss：在一个简化相关 hidden-state 模型下，它会压制 shared directions，使这些公共方向对 routing 变得不显著。实验上，文章在 token、sequence、rollout、layer depth 上展示了 routing 与 hidden-state similarity 的相关性，以及 prompt-level routing、跨模型同题解答、deep-layer prefilling collapse 等难以人类解释的现象。最安全的 claim 是：**MoE expert usage 可以被 hidden-state geometry 解释，但这不等价于 domain/feature-level specialization，也不保证人类可解释的一一对应。**

---

## 2. 文章的分析链条：problem -> method -> evidence -> claim

```text
problem:
  MoE experts 看起来会 specialization，但这种 specialization 来自哪里？
  它是否等价于 domain expertise / semantic feature alignment？

method:
  把 router 写成线性投影 g = Ph；
  用 hidden-state SVD / principal subspace 分析 hidden-state distance 与 logit distance；
  用 sequence-level expert frequency、pooled hidden states、top-P overlap 等指标比较 routing；
  单独分析 load-balancing 对 shared hidden-state directions 的作用。

evidence:
  Fig. 1：token-level hidden-state distance vs router-logit distance 的三角形关系；
  Fig. 2 / 15-19：shared direction、router retained energy、load balancing 的 suppressive pattern；
  Fig. 4-5：context 和 sequence hidden-state similarity 与 expert usage similarity 相关；
  Fig. 6-10：micro-level routing 很难按语义解释，prompt/rollout/depth 均会改变 routing。

claim:
  specialization 是 representation geometry 的 emergent property，
  不是 linear router 本身自动产生的 human-interpretable expertise。
```

**最弱环节**：论文对 $g=Ph$ 的线性几何分析很强，但对 training dynamics 和 load-balancing 导致 specialization/collapse 的解释仍是简化模型 + observational evidence。它不能直接证明 NTP 训练为什么在你的 synthetic setup 中不产生 one-feature-one-expert，只能给出很强的解释框架和诊断方向。

---

## 3. 核心机制 1：线性 router 只是 hidden-state geometry 的投影

### Paper says

MoE router 对每个 token hidden state $h_t^\ell$ 计算 logits：

$$
g_t^\ell = P^\ell h_t^\ell.
$$

选择 top-$k$ experts 本质上是比较 $P$ 的各行和 $h$ 的内积。Proposition 1 给出一个 data-aware bound：

$$
\|P h_i - P h_j\|_2
\le
\|P\Pi_r\|_2 \|h_i-h_j\|_{\Pi_r}
+ \|P(I-\Pi_r)(h_i-h_j)\|_2.
$$

其中 $\Pi_r$ 是 hidden-state data matrix 的 top-$r$ principal subspace projector。含义是：如果两个 tokens 在 router 对齐的数据主子空间里很近，那么它们的 router logits 也必须接近；但如果 hidden states 很远，router logits 仍可能接近，因为 $P$ 可以忽略或压缩很多方向。

### My interpretation

这不是“router 学会聚类 feature”的定理，而是一个**投影几何定理**：

```text
hidden states close  -> logits close -> expert usage close
hidden states far    -> logits may be close or far
```

因此，feature identity 在 hidden space 中可分，并不意味着 router 选择的 separating directions 对齐 feature directions。router 使用的是 $P$ 的 row differences，即 $p_e - p_{e'}$。只有当这些方向与 feature-difference directions 有足够投影时，feature 才会显著改变 top-1 expert。

### Relation to your synthetic result

你的 E2.1 观察是：feature identity 仍在 router input hidden space 中可见，centroids 可分，Fisher ratio 高；但 router boundary directions 与 feature-difference directions 弱对齐，router margins weak，entropy 接近 $\log E$。这与论文机制高度一致：

```text
representation separability != router specialization
```

更精确地说：

```text
feature-separable hidden space
  != router row differences align with feature directions
  != top-1 decision margin is feature-dominated
  != one-feature-one-expert
```

---

## 4. 核心机制 2：load balancing 会压制 shared directions，而不是制造语义专家

### Paper says

作者用简化模型

$$
h_i = \mu + \xi_i
$$

其中 $\mu$ 是 batch/token 共享方向，$\xi_i$ 是区分各 token 的 residual variation。对简化 load-balancing loss

$$
L_{bal}(P)=\left\|\frac{1}{N}\sum_i \text{softmax}(Ph_i)-\frac{1}{E}\mathbf{1}\right\|^2
$$

在 small-logit regime 下，作者得到近似：

$$
L_{bal}(P) \approx \frac{1}{E^2}\|\Pi_E P\mu\|^2.
$$

near-minimizer 需要满足：

$$
\Pi_E P\mu \approx 0
\quad \Leftrightarrow \quad
P\mu \approx \bar{P\mu}\mathbf{1}.
$$

也就是说，shared direction $\mu$ 对所有 expert 只产生同一个 logit shift；由于 softmax/top-$k$ 对 constant shift 不敏感，这个方向对 routing 变成不可见。

### My interpretation

load balancing 的作用不是“把每个 feature 分给一个 expert”，而是避免所有 token 因共享方向都偏向同一 expert。它会鼓励 router 把公共方向从 expert-separating signal 中移除，让 routing 更多依赖残差方向 $\xi_i$。这可能保持 load diversity，但不会自动保证 residual directions 就是你定义的 trigram features。

### Relation to your synthetic result

在你的 toy corpus 中，可能存在多种 shared/common directions：

- token position / prefix-end position；
- syntactic template；
- target-token anticipation；
- NTP loss difficulty / confidence；
- high-frequency unigram or motif-common direction；
- residual stream 中和所有 feature 共享的 readback circuit direction。

如果 load balancing 或 top-1 competition 压制这些 shared directions，router 可能被迫用其他 residual variations 分流；这些 residual variations 未必是 human-defined feature identity。因此你可能看到：route 比随机更相关，但不形成 clean one-feature-one-expert。

---

## 5. 核心机制 3：context、depth、rollout 会改变 routing；prompt-only routing 不可靠

### Paper says

作者先在 token-level 显示同一个 token 在不同 context 下 routing 会变化：浅层更像 token-ID dependent，深层更 context-dependent。然后在 sequence-level 比较 pooled hidden-state similarity 与 expert frequency similarity，发现二者正相关；不同 domain 之所以 routing 不同，是因为 hidden-state distributions 不同，而不是因为 router 内置 domain classifier。

更重要的是，文章展示了三个 interpretability breakdown：

1. **同一道数学题，不同模型的解答轨迹 expert overlap 只有约 60%，与同模型不同题的 overlap 相近。** 这说明 micro-level expert usage 强烈受 model-specific generation trajectory 影响。
2. **prompt-phase routing 不能预测 rollout-phase routing。** 生成内容开始后，expert usage similarity 可能保持，也可能迅速下降。
3. **deep-layer prefilling 可能出现 router collapse。** 语义无关输入在 prefilling 阶段激活近乎相同的 experts，但生成开始后又分化；被 prefilling 抑制/剪掉的 experts 在 rollout likelihood 上仍然重要。

### My interpretation

routing 不是输入表面语义的静态标签。它可能编码：

```text
token identity -> context interaction -> anticipated next-token/output mode -> generation trajectory
```

在深层，hidden states 可能更接近“模型准备如何输出”的状态，而不是“输入属于哪个 feature/domain”的状态。这对你的 synthetic setting 很关键：如果 router input 位于预测前的深层位置，那么它可能更接近 target-token / readback state，而不是 feature-prefix identity。

### Relation to your synthetic result

你的 synthetic trigram 中 feature 是 `[1,2] -> 22` 等前缀-目标映射。若 router input hidden state 已经强烈编码 target token 或 next-token confidence，而不是前缀 feature identity，那么 router 可能按 target/readback difficulty 分流，或干脆让多个 experts 共同支持相同 target。此时 one-feature-one-expert 不会自然出现。

---

## 6. 文章结论的可靠性评估

| 结论 / 分析点 | 证据类型 | 可靠性 | 主要限制 | 对你研究的可用方式 |
|---|---:|---:|---|---|
| 线性 router 使 hidden-state similarity 约束 logit similarity | 数学定理 + Fig. 1 empirical check | 高 | 定理是 upper bound，不是完整 training explanation；similar logits 不等于 functional specialization | 可直接用于解释“hidden separability 不推出 route purity” |
| dissimilar hidden states 仍可激活相似 experts | 线性投影多对一 + Fig. 1 三角形点云 | 高 | 具体相似程度依赖 $P$、top-k、margin | 用来解释多个 feature 共享 experts |
| specialization 来自 hidden-state geometry，不来自 router architecture 本身 | 数学机制 + 多模型观察 | 中高 | “geometry” 本身未解释其训练来源；不排除某些 experts 有 causal domain function | 可作为 claim boundary：不要把 routing purity 当 semantic expertise |
| load-balancing suppresses shared directions | 简化理论 + Fig. 2/15-19 observational pattern | 中 | small-logit approximation；只分析 load-balancing-only；真实训练中 task loss、top-k、optimizer 都参与 | 可设计 load-balance sweep 和 shared-direction projection 诊断 |
| small batch / low diversity 可能导致 specialization collapse | 理论解释 + 引用既有观察 | 中低 | 不是本文直接 controlled pretraining 实验；“might explain” | 作为假设，不作为结论；可在 toy setup 做 batch-diversity sweep |
| router confidence 可检测 OOD | Fig. 3 + Fig. 23 | 中低 | OOD 是 shuffle/reverse proxy；只测 confidence，不保证泛化 | 可借鉴为 shortcut/perturbation sensitivity 指标 |
| sequence hidden-state similarity 与 expert frequency similarity 相关 | Fig. 5 + appendix 多层 | 中高 | coarse sequence-level；不能解释 causal expert utility | 可用于 dataset-level routing analysis，但别推到 feature-level causality |
| prompt-level routing 不预测 rollout routing | Fig. 7 | 中 | 样例数量较少；instruction-tuned model dependent | 对你的实验提示：测完整 prediction trajectory，不只测 prompt/prefix |
| deep-layer prefilling router collapse | Fig. 8-10 | 中 | 对 gpt-oss/reasoning template 敏感；不是所有模型都有 | 对你提示：检查不同 layer / template / duplication 是否导致 shared-direction collapse |
| “expert specialization 抵抗人类解释” | 多个 case study | 中 | 人类不可解释不等于不存在可被 causal intervention 识别的功能 | 用作解释边界，而非否定 expert functionality |

总体判断：**这篇文章的几何分析很可靠，训练机制解释中等可靠，关于人类语义不可解释的结论有启发但依赖实验设置。** 它非常适合帮助你重新解释 synthetic MoE 的 routing 结果，但不能单独替代你的 controlled diagnostics。

---

## 7. My Card vs Paper

### 你捕捉正确的地方

你已经抓到了论文的核心问题：作者不是只想描述 MoE 有 specialization，而是想解释 specialization 的来源：是 linear router、hidden-state geometry、training dynamics，还是 NTP/pretraining regime。你也正确地把它和“普通 router 到底在学什么”联系起来。

### 需要补全的地方

1. **Result 缺失**：最关键结果不是“MoE 会 specialization”，而是“hidden-state geometry explains expert usage similarity；human-interpretable specialization is not guaranteed”。
2. **Method 需要更具体**：作者不是泛泛分析表征空间，而是把 $P$ 与 hidden-state SVD principal subspace 对齐起来，比较 hidden-state distance、logit distance、expert frequency similarity、top-P overlap。
3. **Claim 需要降调**：论文没有完整解释 MoE training dynamics，也没有证明 NTP 会或不会产生 feature experts；它主要解释 pretrained router 的 expert usage pattern 如何由 hidden states 和 linear projection 诱导。
4. **要区分三种 specialization**：routing specialization、functional specialization、semantic/domain specialization。本文主要分析 routing patterns；只有 pruning/NLL 部分稍微触及 functional consequence。
5. **需要加入 reliability boundary**：Prop. 2 的 load-balancing 分析是 simplified/informal，不能直接当作真实训练定理。

### 更正后的两句话理解

1. 这篇论文说明：token-choice MoE 的线性 router 把 hidden states 投影成 expert logits，因此 expert usage similarity 首先由 hidden-state geometry 与 router-data alignment 决定，而不是由 router 自动发现 human-defined domain/feature experts。  
2. 它的重要限制是：该几何解释能说明 routing pattern 的来源，却不能单独证明 expert 的 causal function 或 NTP training dynamics；越到 micro-level、generation-level、deep-layer prefilling，routing 越难按语义解释。

我改进的 abstraction 是：从“router 是否学到了 feature/domain”改成“router row-difference directions 是否对齐 hidden-state 中哪些 directions，以及这些 directions 是否对 task loss 有唯一 utility”。

---

## 8. 对你的 synthetic trigram 结果的解释

你的当前 E2 事实可以重写为：

```text
Feature identity is visible in h.
But router P does not choose feature-difference directions as its main separating axes.
And expert utility is not unique enough to force one feature -> one expert.
```

这篇文章支持以下解释：

### 8.1 hidden separability 只是必要候选，不是 routing 充分条件

如果 feature centroids $c_f$ 可分，但 $P(c_f-c_{f'})$ 很小，top-1 expert 就不会按 feature 分开。你已经观察到 boundary directions weakly align with feature-difference directions，这几乎就是论文 Prop. 1 的 synthetic 版本。

### 8.2 one-feature-one-expert 不是 NTP loss 的自然目标

NTP 只要求预测正确 target token。只要多个 experts 都能支持 `[1,2] -> 22`，或者 residual/attention/LM head 已经能读回 feature，router 就没有必要形成 clean bijection。你的 “multiple experts can support the same feature prediction under forced routing” 是对这一点的直接支持。

### 8.3 load balancing 可能反而反对自然 feature partition

若 features 的频率、难度、target distribution 或 common directions 不均匀，load balancing 的 uniform expert usage objective 可能与 one-feature-one-expert 冲突。它会让 router 保持 expert usage diversity，而不是保持 feature purity。

### 8.4 router 可能使用 shortcut directions

论文提醒：routing 可能由 hidden-state geometry 中的任何方向决定，不一定是语义/feature方向。在 synthetic setting 中要重点排查：

- token ID shortcut；
- prefix-end position shortcut；
- target-token shortcut；
- hidden norm / activation scale；
- loss difficulty / confidence；
- first PC / common feature direction；
- low-variance but router-aligned directions。

### 8.5 experts 可以功能冗余，routing purity 不等于 functional specialization

如果 forced-routing utility matrix 显示多个 experts 对同一 feature 都有低 NLL，那么 router 即使知道 feature，也不会被迫把 feature 分到唯一 expert。此时 failure 不是 representation failure，而是 objective/utility degeneracy。

---

## 9. 建议的下一轮诊断：把论文机制转成 E3 实验

### E3.0 Router behavior decomposition

**Hypothesis**：router logits/margins 主要由 feature 以外的 directions 解释。  
**Measurement**：对每层 router input $h$ 做分解/回归：feature ID、prefix token ID、position、target token、hidden norm、first PC/shared direction、feature centroid residual。测每个因素对 $g_e$、top-1 expert、margin 的 explained variance / mutual information。  
**Possible result**：feature separability 高，但 $P$ 对 feature direction 投影小；norm/position/target/PC 解释更多 routing variance。  
**Claim update**：从“router 没 specialization”升级为“router specialization 被 X direction 主导”。

### E3.1 Forced-routing utility matrix

**Hypothesis**：多个 experts 对同一 feature 都有足够 utility，所以没有 one-feature-one-expert pressure。  
**Measurement**：对每个 feature $f$ 强制使用每个 expert $e$，记录 NLL/readback accuracy/logit margin，构造 $U[f,e]$；比较 $P(e|f)$ 与 $U[f,e]$ 的相关性。  
**Possible result**：$U[f,e]$ 多列接近，route frequency 只弱相关 utility。  
**Claim update**：routing specialization 弱，但 functional redundancy 强；one-feature-one-expert 不被任务损失要求。

### E3.2 Counterfactual shortcut test

**Hypothesis**：router 跟随 token/target/position shortcut，而不是 feature rule。  
**Measurement**：设计 counterfactual：保持 feature rule 不变但替换 token IDs；保持 prefix token 不变但换 target；打乱 position/template；控制 unigram frequency。观察 $P(e|f)$ 和 route margin 是否随 shortcut 变。  
**Possible result**：routing 随 token ID 或 target token 改变，而不是随 abstract rule 改变。  
**Claim update**：feature-level routing failure 来自 shortcut-dominated hidden geometry。

### E3.3 Training dynamics trace

**Hypothesis**：早期随机 routing + expert utility gap 导致 co-adaptation/lock-in，不一定沿 feature 方向。  
**Measurement**：保存训练 checkpoints，追踪：router entropy、margin、$P(e|f)$、$\langle p_e-p_{e'}, c_f-c_{f'}\rangle$、forced utility matrix、expert gradient/token counts。  
**Possible result**：早期某些 experts 获得 feature readback utility，router 后续只强化已有路径；或一直高 entropy/low margin。  
**Claim update**：区分“几何未对齐”与“早期 co-adaptation 锁定”。

### E3.4 Shared-path bypass diagnostic

**Hypothesis**：attention/residual/LM head 或 shared components 已经承担 readback，MoE routing 只是弱调制。  
**Measurement**：MoE output ablation、expert output norm、route shuffling、uniform routing、dominant expert ablation、residual-only/readout probe。  
**Possible result**：readback 在 route shuffling 下仍高，或只在少数 ablation 下下降。  
**Claim update**：解释为什么 capacity reduction / feature-count increase 没强迫 clean routing。

### E3.5 Load-balance and batch-diversity sweep

**Hypothesis**：load balancing 维持 uniform usage，但压制 feature-pure partition；batch diversity 改变 shared-direction suppression。  
**Measurement**：扫 auxiliary loss coefficient、microbatch composition、feature imbalance；测 first PC retained energy、router-feature alignment、$P(e|f)$ purity、NLL。  
**Possible result**：更强 balancing 提高 uniform usage但降低 feature purity；小 batch/低 diversity 出现 router collapse 或 noisy routing。  
**Claim update**：把“load balancing interference”从可能机制变成实验证据。

---

## 10. 对主线的更新

**Relation classification**：useful after adaptation。  
它不是直接证明你的 long-context / KV memory indexing 假设，但它提供了一个重要警告：**router buckets 不能天然当作 feature reverse index；必须证明 router-aligned directions 与你关心的 retrieval feature/rule directions 对齐，并且 routing has causal utility。**

### Hypothesis update

旧表述：feature representations separable 时，MoE router 可能自然形成 feature-indexed experts。  
更新后：feature representations separable 只是必要候选；one-feature-one-expert 还需要：

```text
router row-difference directions align with feature directions;
feature-specific routing has unique downstream utility;
load balancing / shortcuts / common directions do not dominate;
experts are not functionally redundant for the feature.
```

### Modeling update

把 hidden state 分成：

$$
h = \mu_{common} + z_{feature} + z_{shortcut} + z_{loss/target} + \epsilon.
$$

router 实际使用：

$$
g = P h.
$$

因此需要测的是：

$$
\|P z_{feature}\|,\quad
\|P z_{shortcut}\|,\quad
\|P\mu_{common}\|,\quad
\text{margin}(g),\quad
U[f,e].
$$

### Experiment update

下一步不应只看 $P(e|f)$ purity，还要同步测：

- router-feature alignment；
- router-shortcut alignment；
- expert utility matrix；
- training dynamics；
- shared-path bypass；
- load-balance/batch-diversity effect。

### Interpretation update

如果没有 one-feature-one-expert，不应立即解释为“feature 没被学到”。更合理的解释链是：

```text
feature learned in representation
  but router did not align its separating axes with feature directions
  and/or multiple experts/residual path can implement the same readback
  and/or balancing/shortcut/common directions dominate routing.
```

### Next decision

最小下一步：**优先做 E3.1 forced-routing utility matrix，并同时记录 router-feature alignment。** 因为这能最快区分：

```text
routing specialization weak because experts are redundant
vs
routing specialization weak because router ignores feature directions
vs
routing specialization weak because shared/bypass path solves task.
```

---

## 11. Claim audit

| Claim | Status | Reason |
|---|---|---|
| Feature representations can be separable without router specialization. | supported | 论文几何分析 + 你的 E2.1 直接支持。 |
| NTP loss does not necessarily require feature-aligned routing. | weakly supported | 你的 forced-routing observation 支持；本文没有直接分析 NTP toy dynamics。 |
| Token ID / frequency shortcuts can dominate routing. | unclear but important | 本文显示早层 token/context dependence，但未直接证明 token frequency shortcut；需要 E3.2。 |
| Load balancing can conflict with natural feature distribution. | weakly supported | 本文 Prop. 2 支持 shared-direction suppression；真实 training conflict 需 controlled sweep。 |
| Common experts are justified by common-dominated representations. | weakly supported | 本文 related work 提到 standing committee / shared information explanation，但不是 causal proof。 |
| H-MoE is necessary for real-language specialization. | unsupported | 这篇文章只说明普通 routing 难解释，不证明 H-MoE necessary。 |
| MoE router buckets can serve as a KV reverse index. | unclear / high-risk | 若 bucket 与 retrieval feature 对齐且有 recall utility，才可能成立；本文提醒不能默认成立。 |

---

## 12. 30-second advisor version

这篇 paper 的核心不是说 MoE 没有 specialization，而是说 observed expert usage 首先是 hidden-state geometry 通过线性 router $g=Ph$ 投影出来的结果。相似 hidden states 会路由相似，但不相似 hidden states 也可能因为 $P$ 忽略某些方向而路由相似；load balancing 还可能压制 shared directions 来维持 expert usage diversity。对我们的 synthetic trigram 实验，这解释了为什么 feature centroid separability 和 high Fisher ratio 不足以推出 one-feature-one-expert：router 的 separating axes 可能没对齐 feature directions，而且多个 experts 或 shared path 都能完成 readback。下一步最该做的是 forced-routing utility matrix + router direction decomposition，把“没有一一对应”拆成 router alignment failure、expert redundancy、shortcut domination 或 shared-path bypass。

