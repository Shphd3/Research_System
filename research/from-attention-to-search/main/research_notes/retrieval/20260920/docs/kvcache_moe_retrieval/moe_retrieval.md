# 从 Expert Specialization 到 Incremental Parametric Memory：今晚汇报前的研究判断与方法调研

## 当前系统位置与今晚最重要的判断

我以你刚提交后的主线入口、E20 Focus/Plan、两篇重新精修的阅读文档，以及你系统里此前与 **counterfactual utility / residual expert growth** 直接相关的 Anchor 为核心重新核对了一遍。你现在的系统主线已经比前几天清晰很多：

> **预训练表征 → 可被 Router 使用的结构 → Expert functional specialization → 进一步考虑 incremental growth。**

当前 E20 仍在回答一个比 incremental 更靠前的问题：**冻结的最后层 SAE 特征分组，通过离线 Router 固定分发以后，能不能产生随机 feature grouping、GMM 和 task-only 不能稳定复现的专家功能收益。**你最新研究路线文档记录的快照是：修订后的八成分扁平 GMM 已完成，九个离线路由与五个单步资格检查通过，正式 512-step 作业已经运行，但该快照仍没有完整功能结论。fileciteturn11file0L2-L2 当前 E20 的实际实现又非常重要：共享专家始终开启，只选择一个专门专家；SAE 教师是**逐 token 的**，而 GMM 仍更接近 prompt/record 级教师，因此未来不能把 SAE-vs-GMM 的差异纯粹解释成“SAE 表示一定优于 GMM”。fileciteturn20file0L2-L2

**今晚我建议你把 incremental idea 提给导师，但不要把它说成“我准备转向一个新的大方向”。**

最好的定位是：

> **“我在尝试把我们现在的 representation → routing → expert function 这条线，延伸到一个更明确的 continual-learning 问题：什么时候现有计算已经不够，值得新增一块独立的参数记忆？”**

这句话非常关键，因为你的 Research System 其实**已经研究过这个思想的前半部分**。A15_11 早就明确区分了四件不能互相替代的事：

\[
\text{semantic separability}
\neq
\text{utility separability}
\neq
\text{Router use}
\neq
\text{functional benefit}.
\]

它还明确提出过“冻结 common function，再对 unexplained functional residual 逐步增加 expert”的机制。更重要的是，那个合成实验的结果并不是“counterfactual utility supervision 成功”：**对齐的 residual tree 确实能工作，但直接 utility supervision 没有带来优势，匹配的非线性 flat Router 也足以解决那个合成问题。**fileciteturn17file0L2-L2 你的 A16 路线也已经把 frozen-expert regret distillation 单独设成研究对象，并记录过“几何方向本身没有通过 frozen expert-choice regret gate”的边界。fileciteturn18file3L80-L89

因此，今晚最有价值的新认识不是：

> “我想到了动态加 Expert。”

而是：

> **“我们以前已经知道 semantic novelty 不等于 functional utility。现在我想把 functional insufficiency 从 Router 监督目标，重新定义成一个 capacity-growth criterion：先判断现有 Expert pool 是‘Router 没选对’，还是‘即使选对也没有足够能力’，只有后一种情况才增长参数。”**

我认为这才是你这个 idea 最值得继续做的版本。

---

## 两篇文章今晚必须真正讲懂什么

### Attention Residuals：不是新的 token attention，也不是 MoE Router

今晚你只需要牢牢记住一个公式变化。

普通 PreNorm Transformer 可以把进入第 \(\ell\) 个子层之前的 residual state 展开为：

\[
h_\ell=\sum_{i<\ell}v_i,
\]

其中 \(v_i\) 是之前各个子层新写入 residual stream 的输出。问题不是“加法一定丢信息”，而是**后面只能直接读到这些来源固定系数相加后的状态，不能重新决定某个早期 write 此刻应该有多大权重**。你的 Research System 已经把这个区分写得很准确：AttnRes 的选择发生在**模型深度来源**之间，而普通 self-attention 选择的是历史 token，MoE Router 选择的是 expert function。三者虽然都可能出现 softmax，但候选集合不同。fileciteturn7file0L2-L2

Attention Residuals 改成：

\[
h_{\ell,t}
=
\sum_{i<\ell}
\alpha_{i\rightarrow \ell,t}v_{i,t},
\]

其中大致：

\[
z_{i\rightarrow\ell,t}
=
w_\ell^\top \operatorname{RMSNorm}(v_{i,t}),
\]

\[
\alpha_{i\rightarrow\ell,t}
=
\operatorname{softmax}_{i<\ell}(z_{i\rightarrow\ell,t}).
\]

最容易产生误解的是 \(w_\ell\)：**它是每个目标层学到的 pseudo-query，不需要随输入生成；输入依赖来自不同样本产生不同的历史 \(v_{i,t}\)，因此打分仍然随内容改变。**完整 AttnRes 保存所有深度来源；Block AttnRes 把相邻层先组合成 block，再在 block 间选择，以减少保存和通信负担。Moonshot 的官方实现就是按这个形式做的。citeturn14search0turn14academia25

论文不是一个小规模 LoRA 后训练结果。作者把它用于 Kimi Linear 的大规模预训练设置，报告的是 48B 总参数、3B 激活参数和 1.4T token；官方结果中，AttnRes 相对 baseline 在他们的下游面板上普遍提高，例如 GPQA-Diamond 从 36.9 到 44.4、HumanEval 从 59.1 到 62.2。这个证据支持“depth-wise content-dependent source selection 可以改善训练”，**不支持把一个已有 Qwen 的 residual connection 换掉以后做几百步 SFT 就必然有效。**citeturn14search0turn14academia25

### 你今晚可以这样向导师解释

> “Attention Residuals 给我的启发不是再做一个 token attention。它指出普通 residual 把不同深度 write 混在一个累计状态里，而 AttnRes 把来源保留下来，让后面的层按当前内容重新选择。它是 depth-wise information routing。对我们的启发是：如果未来把新增知识存在不同 memory expert 里，也许不应该不断 merge 回一个共享参数，而应该保留独立来源，再让 Router 决定什么时候读哪个来源。”

**最后一句是你的研究类比，不是论文结论。**

这个类比恰好能接到：

\[
\boxed{\text{stable backbone}+\text{plastic modular memory}+\text{adaptive routing}}.
\]

AttnRes 给你的不是“memory 方法”，而是一个**source preservation + adaptive read** 的架构思想。

---

### Advancing Expert Specialization：核心不是语义标签，而是让专家真正变得不同

这篇 NeurIPS 2025 工作从另一个方向触碰你现在最核心的问题：

> **为什么有 MoE，不等于有 specialization？**

作者观察到，在 downstream post-training 中，传统 load-balancing auxiliary loss 虽然让专家使用更均衡，却可能让 Router 对不同输入给出越来越相似的分布，同时多个 Expert 接收高度重叠的训练信号，从而形成较高功能重叠。于是作者同时处理**专家端**和**Router 端**。citeturn16view0

总目标是：

\[
\mathcal L
=
\mathcal L_h
+
\alpha\mathcal L_{\rm aux}
+
\beta\mathcal L_o
+
\gamma\mathcal L_v.
\]

其中并没有删除 load balancing。citeturn16view0

专家端的 orthogonality loss \(\mathcal L_o\) 大意是在同一个 token 同时选择的 Expert 输出之间，惩罚互相投影：

\[
\mathcal L_o
\sim
\sum_{i,j\neq k}
\left\|
\operatorname{Proj}_{\tilde x_{ik}}
\tilde x_{ij}
\right\|^2.
\]

目标是：

\[
E_j(x)
\not\approx
E_k(x)
\]

至少不要对同一输入不断写出重复方向。citeturn16view0

Router 端用：

\[
\mathcal L_v
=
-
\sum_{i,j}
(s_{ij}-\bar s_j)^2/n,
\]

也就是最大化不同输入的 routing-score variation，让 Router 不要对所有 token 给出近似相同的偏好。citeturn16view0

这篇论文最值得你吸收的不是某个 loss，而是：

> **Specialization 必须同时检查 Expert 有没有变得功能不同、Router 有没有根据输入区别使用它们、最终任务有没有收益。**

这和你这几天逐渐形成的认识高度一致。

作者不仅看任务分数，还看 Expert Overlap、Routing Variance、Silhouette、负载等指标；他们报告 Expert overlap 最多降低约 45%、routing-score variance 增加超过 150%，同时 downstream performance 有改善。主设置中，每个 benchmark 是**分别**用约 6,000 个高质量样本 fine-tune，约 550 steps，并使用 rank-32 LoRA 更新 Router 与 Expert；这不是默认把全部 11 个 benchmark 混在一个 continual/SFT checkpoint 中训练。citeturn16view0turn17view0

这点对你尤其重要，因为学长告诉你“从这篇找 downstream dataset”，你可以借：

> **数据类型、SFT 任务合同、specialization diagnostics。**

但不能直接说：

> “他们已经证明八任务混合语义 Router 应该这样训练。”

### 它和你当前 SAE 路线的真正关系

二者其实代表两种完全不同的 specialization 思路：

\[
\boxed{\text{SAE/GMM 路线}}
\quad
\text{external structure}\rightarrow\text{Router}
\]

而这篇文章是：

\[
\boxed{\text{Expert Specialization 路线}}
\quad
\text{task gradient}
+
\text{specialization objective}
\rightarrow
\text{experts/router jointly differentiate}.
\]

前者问：

> “我能不能先发现结构，然后用结构指导分工？”

后者问：

> “我能不能不告诉语义类别，直接让不同专家产生更少重复的功能？”

这恰恰解释了为什么你不能只盯着 SAE label accuracy。

还有一个与你当前 E20 非常具体的边界：你的 E20 当前实现是**每 token 只选一个专门 Expert**。fileciteturn20file0L2-L2 而论文的 \(\mathcal L_o\) 定义在同一 token 的多个被选中 Expert 输出之间。严格按公式，Top-1 时不存在 \(j\neq k\) 的同时激活 Expert 对，因此这个 orthogonality term **不能原样移植到你当前结构**。这是从论文公式和你实现共同推出的结论。citeturn16view0

但是它的两个诊断思想非常值得借：

\[
\boxed{\text{Expert functional overlap}}
\]

和

\[
\boxed{\text{input-conditioned routing variation}}.
\]

这比“某个 Expert 看起来像数学 Expert”严谨得多。

---

## 你的 incremental idea 在现有文献里到底处在什么位置

这里需要非常诚实：**你的大方向是好的，但按照你现在的宽泛表述，已经不是一个足够新的方法主张。**

最危险的是你提的三个词：

\[
\boxed{
\text{stable backbone}
+
\text{plastic modular memory}
+
\text{adaptive routing}
}
\]

这三者组合，在已有文献中已经有非常直接的近邻。

| 工作 | 与你 idea 的直接重合 | 没有完全回答你的地方 |
|---|---|---|
| **WISE, 2024** | 原模型作为 main memory；另建 side parametric memory；只编辑 side memory；训练 routing 决定走 main 还是 side；继续编辑时还做 memory sharding/merging | 重点是 lifelong factual model editing，不是基于“现有 Expert 功能不足”自动决定是否长新 Expert citeturn10view0 |
| **PMoE, 2024** | 浅层保持 general、深层 progressively add LoRA experts；Router 用深层特征分发；连续任务上训练 | 新 Expert 基本跟随任务增长；用了 1% replay；不是无边界数据流中的功能缺口检测 citeturn24view0 |
| **Parametric RAG, 2025** | 文档先参数化，再检索对应参数并注入 FFN；不必把全部 passage 塞进 context；还能和 text RAG 联用 | 仍然由 document retrieval 驱动，没有自动决定哪些知识值得永久 internalize citeturn11academia3 |
| **MoE-CL, 2025** | 每个任务 dedicated LoRA + shared LoRA，在 continual instruction tuning 中隔离旧知识并做跨任务 transfer；有工业实验 | task-level 专家结构比较明确，不解决无 task-ID 的“什么时候需要新容量” citeturn25view0 |
| **MLP Memory / Memory Decoder, 2025–26** | 明确把 reasoning model 与 parametric memory 分开；Memory Decoder at Scale 甚至单独把 memory 扩到 6.9B | 主要是预训练出来的 memory capacity，不是在线逐步添加的小型 memory expert citeturn11academia2turn23academia1turn23academia0 |
| **PEAM, 2026** | 明确提出 parameterization-worthiness 和 self-triggered consolidation，决定什么 experience 值得 internalize；memory 还是 MoE-LoRA | Minecraft embodied skill setting，不是普通文本 LLM knowledge/SFT；但概念上已经和“什么时候值得参数化”高度重合 citeturn20view0 |
| **UniMem, 2026-07** | **非常接近你的故事**：novel/sparse 放 episodic retrieval；recurring/reliable pattern 写进 expandable parametric memory；无 task label、按需扩展 | 仍有空间研究“functional insufficiency”而不是 recurrence/task pattern，及 token-level language-model routing，但 broad story 已经重合 citeturn19view2 |
| **Dual-Layer Agentic Memory, 2026-08** | 同样直接讨论 externalize/update/internalize；先外部存储，之后选择性 parametric consolidation | 最新预印本、agent-memory 方向；但再次说明“什么时候 retrieve、什么时候 internalize”本身已经成为公开研究问题 citeturn9academia1 |

还有两类 MoE continual-learning 近邻。DIMoE-Adapters 2026 已经研究动态 expert evolution，不过是在 vision-language continual learning；LLaVA-CMoE 更直接使用 probe 判断某层是否需要扩充知识并自适应扩展 Expert，也是在视觉—语言模型上。citeturn11academia1turn12academia2

所以你今晚**千万不要对导师说**：

> “我发现了一个新的范式，就是冻结 Backbone，新增 Expert，当作 Memory。”

这个 broad idea 已经明显碰到 WISE、PMoE、UniMem、PEAM 等工作。citeturn10view0turn24view0turn19view2turn20view0

### 但这并不意味着不值得做

相反，我认为**值得继续深挖，价值大约是“方向 8/10、当前方法新颖性 4/10、如果重新定义问题后潜力 8/10”**。

真正的机会在于把问题从：

> “动态增长 Expert”

改成：

> **“模型怎样知道自己缺的不是 Router，而是 capacity？”**

这是目前你所有实验最自然的汇合点。

因为新数据 \(D_{\rm new}\) 上性能差，至少有两种根本不同原因：

\[
\boxed{\text{Routing failure}}
\]

现有专家中其实已经有人会，只是 Router 没选到；

和

\[
\boxed{\text{Capacity failure}}
\]

即使从现有专家中给它选最好的，仍然没有专家能够解决。

如果不区分这两个原因，就会出现：

> Router 坏了 → 误以为模型需要长新 Expert → Expert 越长越多。

而你过去几个月刚好一直在学一件事：

> **semantic separability 不能替代 expert utility。**

所以你的独立问题可以非常自然地写成：

\[
\boxed{
\textbf{Can counterfactual functional insufficiency,
rather than semantic novelty or task identity,
determine when modular memory should grow?}
}
\]

中文就是：

> **能否根据现有 Expert pool 的反事实功能不足，而不是根据任务 ID 或语义新颖性，决定什么时候真正需要新增参数记忆？**

这和 UniMem 的“recurring/reliable pattern”、PMoE 的“新 task → 新 expert”、SAE 的“新 feature group → 新 expert”都不完全一样。是否最终足够新，需要进一步逐项做 novelty audit，但这已经是一个**可以由你自己拥有的问题**。citeturn19view2turn24view0

而且它正好和你 Research System 的 A15_11 接上：系统已经正式写过“semantic separability 不推出 utility separability”，也已经做过 residual expert growth 的合成 falsification。fileciteturn17file0L2-L2

---

## 把 idea 改造成真正干净的最小假设

### 不要先问“新 Expert 有没有被使用”

对于新数据 \(D_2\)，我建议先定义三个损失，而不是直接 train 一个新 Expert。

当前部署 Router：

\[
L_{\rm native}(D_2).
\]

假设允许我们在**已有** \(K\) 个专家中反事实地逐一试用，得到最好的已有专家：

\[
L_{\rm best\ existing}(D_2).
\]

再允许训练一个很小的候选新 Expert，并在独立 validation split 上评估：

\[
L_{\rm new\ candidate}(D_2).
\]

于是可以定义两种完全不同的残差。

**Router regret：**

\[
R_{\rm route}
=
L_{\rm native}
-
L_{\rm best\ existing}.
\]

**Capacity residual：**

\[
R_{\rm cap}
=
L_{\rm best\ existing}
-
L_{\rm new\ candidate}.
\]

现在判断变得非常清楚。

| 情况 | 解释 | 动作 |
|---|---|---|
| \(R_{\rm route}\gg0,\ R_{\rm cap}\approx0\) | 专家已经会，是 Router 没选对 | **修 Router，不增长** |
| \(R_{\rm route}\approx0,\ R_{\rm cap}\gg0\) | Router 已经选得差不多，现有 capacity 不够 | **值得增长** |
| 两者都大 | Router 和 capacity 都有问题 | 先隔离两者再决定 |
| 两者都小 | 新数据并没有形成新的功能需要 | **不增长** |

我认为这是你今晚最应该给导师看的公式。

因为它把你当前的：

\[
\text{representation}
\rightarrow
\text{Router}
\rightarrow
\text{expert utility}
\]

第一次真正接到了：

\[
\text{expert growth}.
\]

### 原 H1 还需要一个关键修正

你原来写：

> 冻结 base、冻结旧 Expert，只更新新 Expert 和 Router，因此旧知识应该保留。

这里有一个重要漏洞：

**旧 Expert 冻结，不代表旧能力一定不忘。**

因为只要 Router 被更新，旧样本：

\[
x\in D_1
\]

就可能从原来的 Expert 被重路由到新的 Expert。因此，**routing drift 本身可以产生 catastrophic forgetting**。WISE 正是显式训练 main/side memory 的 scope routing；已有 continual-MoE 工作也反复把 Router 稳定性作为问题。citeturn10view0turn12academia1

因此第一版更干净的结构不是重新训练整个 \(K+1\) 类 Router，而是：

\[
\boxed{\text{append-only innovation gate}}.
\]

冻结：

\[
F_\theta,\quad M_1,\ldots,M_K,\quad r_{\rm old}.
\]

只增加：

\[
M_{K+1}
\]

和一个新 gate：

\[
g_{\rm new}(h)\in[0,1].
\]

旧计算保持原样：

\[
h_{\rm old}'=\operatorname{ExistingSystem}(h),
\]

新模块只做：

\[
h'
=
h_{\rm old}'
+
g_{\rm new}(h)M_{K+1}(h).
\]

这样新模块没有被激活时：

\[
g_{\rm new}(h)\approx0,
\]

旧计算路径在结构上保持不变。

这并不能自动保证零遗忘，因为 gate 仍可能对旧样本误激活，但它把旧能力破坏压缩成了一个非常容易分析的问题：

\[
\boxed{\text{new-gate false positive on old inputs}}.
\]

这比重新 softmax 所有 Expert、导致所有旧概率一起变化干净很多。

它也和 Attention Residuals 给你的“**不要把来源重新混回一个不可分状态，先保留来源再选择**”形成一个很自然的概念呼应；再次强调，这一连接是研究设计类比，而不是 AttnRes 论文已经验证的 continual-memory 机制。citeturn14search0

---

### 你的“新能力/旧损失”比值不适合直接作为唯一主指标

你原来想：

\[
\frac{\text{new ability gain}}
{\text{old ability loss}}.
\]

直觉完全正确，但数学上有一个问题：

当

\[
F_{\rm old}\approx0
\]

时，分母趋近零，比值会变得极不稳定；如果旧任务反而提高，即 \(F_{\rm old}<0\)，解释也很别扭。

更稳妥的是把研究目标写成一个**约束优化/Pareto 问题**：

\[
\boxed{
\max \Delta_{\rm new}
\quad
\text{s.t.}\quad
F_{\rm old}\le\epsilon
}
\]

同时限制：

\[
P_{\rm growth}\le B_P,
\qquad
C_{\rm online}\le B_C.
\]

然后报告四个主要量：

\[
\Delta_{\rm new}
=
L_{D_2}^{before}
-
L_{D_2}^{after},
\]

\[
F_{\rm old}
=
L_{D_1}^{after}
-
L_{D_1}^{before},
\]

以及参数增长和在线代价。

Continual-learning 文献通常还报告 Overall/Average Performance 和 Backward Transfer；PMoE 明确定义了 OP/BWT，MoE-CL 也同时报告 Accuracy、Backward Transfer 和 Forward Transfer。citeturn24view0turn25view0 对纯事实记忆，WISE 的 **reliability / generalization / locality** 三分法尤其适合你的实验：不仅记住训练问题，还要看 paraphrase 能否泛化，以及无关旧知识是否保持。citeturn10view0

---

## “参数 Memory vs RAG”真正应该怎么研究

你提出的最重要判断是对的：

\[
\boxed{\text{不要讲替代 RAG。}}
\]

RAG 从最初就被设计成把 parametric model 和显式 non-parametric memory 结合起来；它的重要价值之一恰恰是外部知识能够被更新和检索，并让模型访问显式来源。citeturn22academia0 最近的 HippoRAG 2 甚至证明 non-parametric memory 还能通过图结构和 Personalized PageRank 改善 factual、associative 和 sense-making memory，因此“向量 RAG 不擅长关系 → RAG 本身不行”这个推理是不成立的。citeturn22academia2

另一方面，parametric memory 也已经越来越有证据支持。Parametric RAG 把 retrieved document 编码进 FFN 参数，而且作者明确报告 parametric 与普通 in-context RAG 可以组合；Memory Decoder 系列则更进一步，把 memory capacity 从 reasoning model 中分离出来，最新 scale 工作将 memory 扩到 6.9B，并在其评估中显示“小 reasoning model + 大 memory”可以获得很强的 parameter-performance tradeoff。citeturn11academia3turn23academia0

但系统性研究也给了很重要的反例：2025 年对 parametric RAG 的系统分析发现，**只靠 parameterized documents 会丢失一部分文档语义，单独使用时不如 text-level interaction；参数和原文一起使用反而最好。**citeturn22academia1

所以真正有价值的问题不是：

\[
\text{RAG vs Parametric Memory，谁淘汰谁？}
\]

而是：

\[
\boxed{
\text{什么知识应该 remain external，
什么知识值得 internalize？}
}
\]

但这里要注意：**截至 2026 年 9 月，这句话本身也已经不是全新的。**PEAM 有 parameterization-worthiness，UniMem 根据 novelty/recurrence 决定 episodic vs parametric，8 月刚出现的 Dual-Layer Agentic Memory 甚至直接把问题写成 knowledge lifecycle 中的 externalize / update / internalize。citeturn20view0turn19view2turn9academia1

你的差异因此应该放在：

\[
\boxed{
\text{internalization 由 functional capacity residual 触发}
}
\]

而不是：

\[
\text{由任务 ID、使用频率、人工 category 或单纯 novelty 触发}.
\]

### 这里还能得到一个很好的成本问题

RAG 的写入成本很低，但每次查询要 retrieval、读取文本并进行 context prefill；参数 Memory 的写入需要训练，但重复使用后在线成本可能下降。Parametric RAG 和 Memory Decoder 的出发点都包含减少 retrieval/long-context online cost。citeturn11academia3turn23academia1

因此可定义知识 \(k\) 的生命周期成本：

\[
C_{\rm RAG}(k,Q)
=
C_{\rm write}^{R}
+
Q C_{\rm read}^{R},
\]

\[
C_{\rm param}(k,Q)
=
C_{\rm train}^{P}
+
Q C_{\rm read}^{P},
\]

其中 \(Q\) 是未来重复使用次数。

如果：

\[
C_{\rm read}^{R}>C_{\rm read}^{P},
\]

那么存在一个粗略 break-even：

\[
Q^\star
=
\frac{
C_{\rm train}^{P}-C_{\rm write}^{R}
}{
C_{\rm read}^{R}-C_{\rm read}^{P}
}.
\]

这给你一个比“Parametric Memory 推理快”更科学的问题：

> **一条知识需要被重复调用多少次，internalization 的训练成本才值得？**

我认为这个角度非常适合导师提出的“小模型知识库”场景。

---

### 最小实验不要只做随机事实，最好分成两类 memory

你的人工事实流：

> Zorvia 的首都是 Melun。  
> Fentra 的货币是 Jex。

非常适合做**资格实验**，因为可以控制模型预训练不可能见过这些事实。

但它有一个天然问题：

> **一次性新事实，本来就是 RAG 最擅长的对象。**

你若要求参数模型看几百条新事实、训练以后再赢一个只需插库的 RAG，问题设置本身可能并不公平。

所以更好的假设是：

> **低频、易变、需要出处的事实 → 保持 external。**  
> **反复访问、相对稳定、需要参与大量后续计算的知识/操作模式 → 更有 internalization 价值。**

这个区分也和 UniMem 把 novel/sparse 事件保留为 episodic memory、将 recurring/reliable pattern consolidation 到 parametric memory 的设计相吻合。citeturn19view2

因此你以后可以有两个 panel：

**Fact-memory panel**：随机实体关系，测试 exact QA、paraphrase、冲突更新、两跳组合。

**Reusable-function panel**：反复出现但表面形式变化的规则/操作，例如一个新的符号变换规则、代码 API 使用规则、数学操作约定或领域决策规范。

后一个 panel 更贴合：

\[
\text{Expert specialization}
\]

而不是单纯：

\[
\text{fact memorization}.
\]

这也自然接回你最新 Research System 里提出的“同一操作在不同表面表达下是否稳定保留”的机制问题。fileciteturn11file0L2-L2

---

## 值不值得做，以及今晚怎么向导师讲

### 我的最终评价

**值得做，但不要按你现在的大标题直接开工。**

我会这样评分：

| 维度 | 判断 |
|---|---|
| 科学问题的重要性 | **高**：stability–plasticity、continual adaptation、memory lifecycle 都是真问题 |
| 与导师 intuition 的匹配 | **很高**：小模型/模块化知识库、持续更新、动态 Expert 都直接接得上 |
| 与你现有 Router 主线的匹配 | **很高**：从 representation → routing → utility → growth 自然延伸 |
| “stable backbone + new memory expert + Router”本身的新颖性 | **低到中**：WISE、PMoE、MoE-CL、UniMem 等已覆盖大量空间 citeturn10view0turn24view0turn25view0turn19view2 |
| “RAG 还是 internalize”本身的新颖性 | **中低**：2026 已出现多篇直接研究该 lifecycle citeturn20view0turn9academia1 |
| **functional insufficiency → growth** | **中高潜力**：与你自己的 counterfactual-utility 历史最契合；需要进一步 novelty audit |
| 现在立刻投入大规模训练 | **不建议** |
| 现在拿去和导师讨论 | **强烈建议** |

### 今晚不要说成完整 proposal，先说成一个“我找到的更具体问题”

你可以直接这样讲：

> **“老师，我这两天重新想了一下您说的 incremental expert 和小模型知识库。我感觉真正的问题可能不是‘来了新 domain 就加一个 Expert’，因为这已经很接近已有 progressive MoE 和 continual adapter 的做法。我现在更感兴趣一个更具体的问题：模型怎么判断自己是真的缺新容量，而不是 Router 没把已有 Expert 用好。”**

然后画：

\[
L_{\rm native}
\quad\rightarrow\quad
L_{\rm best-existing}
\quad\rightarrow\quad
L_{\rm new-expert}.
\]

接着说：

> **“第一个差值是 routing regret，第二个差值才是 capacity residual。只有现有 Expert 即使 oracle 选择以后仍然解释不了，而且新增小模块能在 held-out 数据上稳定改善，我才认为应该长一个 Expert。”**

然后接你的导师愿景：

> **“这样我们现在的 representation 研究就不是为了给每个语义类命名，而是希望最终预测这个 functional residual：哪些输入已经超出现有计算能力，值得新增一个独立 memory module。”**

再连接 AttnRes：

> **“Attention Residuals 给我的启发是保留不同信息来源再按内容读取，而不是所有东西都重新加进一个共享状态。所以 incremental 模型里，我也倾向于冻结已有 memory，不反复 merge，而是 append 一个新模块，再学习什么时候读它。”**

这里必须补一句：

> **“这个只是架构启发，AttnRes 本身研究的是 depth-wise residual，不是 continual memory。”**

然后连接 Expert Specialization：

> **“另一篇 Expert Specialization 让我意识到，我们不能把语义标签一致当 specialization。要同时看 Expert 的 functional overlap、Router 的输入依赖，以及最后任务收益。所以 SAE/GMM 如果有用，只是 teacher；最终要看它是不是产生真正不重复的功能。”**

最后把 novelty 风险主动告诉导师：

> **“我查了一下，这个大方向已经有 WISE、PMoE、UniMem、Parametric RAG、Memory Decoder 等非常近的工作，所以我不想讲成‘我们发明 parametric memory’。我想先看我们能不能把创新点收敛到：用 counterfactual functional insufficiency 决定什么时候增长，而不是用 task ID 或语义新颖性决定。”**

**这一段我认为会让导师比较容易听懂你到底在想什么。**

---

### 导师如果问“那你下一步具体做什么？”

不要回答：

> “我今晚就实现 RAG + memory + continual MoE 全系统。”

回答：

> **“我先不做完整系统。我想做一个最小 D1→D2 实验，把 routing failure 和 capacity failure 分开。”**

最小的第一轮其实**不需要 RAG**。

只要：

\[
\boxed{\text{shared LoRA continual update}}
\]

vs

\[
\boxed{\text{new isolated LoRA expert + oracle gate}}
\]

vs

\[
\boxed{\text{new isolated LoRA expert + learned append-only gate}}.
\]

第一组告诉你共享更新的 stability–plasticity trade-off。

第二组告诉你**如果路由完全正确，模块化增长本身有没有价值**。

第三组才告诉你 Router 能不能接住这份价值。

RAG 应该进入下一阶段的 **memory-medium comparison**，而不是第一轮机制验证。

第一轮用：

\[
D_1\rightarrow D_2
\]

而不是立刻：

\[
D_1\rightarrow D_2\rightarrow\cdots\rightarrow D_{20}.
\]

记录：

\[
A_{\rm new},\quad A_{\rm old},\quad
R_{\rm route},\quad R_{\rm cap},
\]

以及 added parameters 和 active compute。

**只有这一步成立，再研究“什么时候自动 grow”。**

否则你会同时不知道：

- 新 Expert 会不会学；
- Router 会不会选；
- old route 会不会漂移；
- growth detector 会不会判断；
- RAG 对照是不是公平。

---

### 今晚你真正应该记住的五句话

> **Attention Residuals：**不是 token attention；它让模型按内容重新读取不同深度的 residual writes。citeturn14search0  
>
> **Expert Specialization：**不是给 Expert 贴语义标签；它通过减少 Expert 输出重叠、增加 Router 区分性来促进功能分工，并同时检查任务收益。citeturn16view0  
>
> **当前 SAE：**是在验证“外部表征结构能不能指导有用分工”，尚不能把 label recovery 当功能收益。fileciteturn12file0L2-L2  
>
> **Incremental 真问题：**不是“什么时候看见新语义”，而是“什么时候现有 Expert 即使选对了也不够用”。这与你系统原有 semantic-vs-utility distinction 完全一致。fileciteturn17file0L2-L2  
>
> **真正值得做的长期问题：**
>
> \[
> \boxed{
> \text{When should a model retrieve existing memory,
> and when is the functional residual large enough to justify new parametric capacity?}
> }
> \]
>
> 但鉴于 UniMem、PEAM、WISE 和最新 memory-lifecycle 工作已经占据大量相邻空间，**你自己的落点必须是 functional capacity residual / routing-vs-capacity decomposition，而不是“参数记忆”或“self-incremental”这两个宽泛名词本身。** citeturn19view2turn20view0turn10view0turn9academia1

今晚最稳的汇报策略因此是：**先用两篇论文说明你已经理解“信息来源怎样选择”和“专家怎样真正专门化”，再把 incremental 作为这一主线的自然下一问；提出“routing regret vs capacity residual”这个具体 idea，请导师判断这个研究问题是否值得作为下一阶段，而不是当场承诺一套尚未验证的 self-incremental 系统。**