# 0701 Seminar 问题推进 Prompt

请把下面整段内容复制到新的 web AI 对话中使用。目标是回答导师在 seminar 后提出的问题，并判断哪些问题能够接到当前 nested learning / MoE gating 主线，哪些应该作为单独的优化理论学习任务。

---

你是我的研究协作 agent。默认用中文回答。请不要一上来写实验方案或给出强结论；本轮先做 seminar 问题拆解、理论复习、文献技术点抽取、以及和我当前研究主线的关系判断。

## 0. 当前背景

我的当前研究主线是：在 top-1 MoE routing 中，理解为什么通过隐藏状态聚类得到的 feature-level expert specialization 能初始化成功，但训练中会被擦除；当前怀疑与公共成分、高频方向、谱空间高增益方向、以及稀有特征被公共方向干扰有关。

当前边界是：

- 可以说：受控 feature 上，聚类初始化可以建立均匀路由；保持依赖足够大的初始 margin，而不是 router rows 主动追踪 feature centers。
- 可以说：A06_23 显示正 margin 不等于一定保持，margin 太薄会在训练中跨边界。
- 可以说：A06_22 显示 common 是候选机制，但 projector 依赖强，所以不能说 common 已经是根因。
- 不能说：common subtraction 已经是有效方法。
- 不能说：当前 common projector 就是真实公共成分算子。

请把下面 seminar 问题当作需要澄清的研究问题，而不是要强行并入我已有主线的结论。

## 1. 必须阅读的本地材料

如果你能读取我的本地文件，请先读：

- `AGENTS.md`
- `PROJECTS.md`
- `daily_research_reports/0701/docs/design_problem_understanding_revised.md`
- `daily_research_reports/0701/docs/PPT/mingyi_hong_talk_ordered_screenshots.pdf`

然后读 `daily_research_reports/0701/docs/related_papers/` 中的论文。主读层是：

- `2605.17787_revisiting_adam_sgd_gap_large_effective_lr.pdf`
  - 题目：Revisiting the Adam-SGD Gap in LLM Pre-Training: The Role of Large Effective Learning Rates
- `2506.16659_memory_efficient_llm_pretraining_minimalist_optimizer_design.pdf`
  - 题目：Memory-Efficient LLM Pretraining via Minimalist Optimizer Design
- `2605.25395_ema_nesterov.pdf`
  - 题目：EMA-Nesterov: Stabilizing Nesterov's Lookahead for Accelerated Deep Learning Optimization
- seminar/talk：`mingyi_hong_talk_ordered_screenshots.pdf`

补充层是：

- `1711.05101_decoupled_weight_decay_adamw.pdf`
- `1512.00567_rethinking_inception_label_smoothing.pdf`
- `1906.02629_when_does_label_smoothing_help.pdf`
- `1705.08039_poincare_embeddings.pdf`
- `2603.03756_moose_star.pdf`

如果你不能读取本地文件，请先基于文件名和题目给出阅读计划，并明确要求我贴出关键页或摘要。不要编造论文内容。

## 2. 本轮必须回答的导师问题

请围绕四个问题建立分析框架。

### 问题 A：Adam normalization 的贡献是否主要由 common feature 决定？

导师问题：

SGD 的有效学习率小很多，Adam normalization 的主要贡献是否由公共特征决定？如果把公共特征去掉，SGD 能不能用？

请先定义：

- 公共特征：高频、跨上下文复用、对多个预测任务都有贡献的表征方向。
- 稀有特征：低频、组合性更强、需要区别具体语境的表征方向。
- 有效学习率：参数更新量相对于梯度尺度的实际步长；Adam 中不同坐标会被二阶矩估计重新缩放。
- normalization：这里指 Adam 或相关方法对梯度坐标尺度的归一化，不要把它只理解成 LayerNorm。

要回答：

1. Adam 的优势是否可能来自抑制 common feature 造成的梯度尺度不均？
2. 如果去掉 common feature 后，SGD 的稳定最大学习率是否会变大？
3. 如果 SGD 仍不能用，说明剩余问题可能来自什么：曲率、batch noise、layer-wise spike、token-class imbalance、attention dynamics，还是谱高增益方向？
4. 如何把这个问题变成最小可证伪诊断，而不是直接提出新 optimizer？

### 问题 B：3 篇 paper + talk 要抽出什么？

导师要求：

读 3 篇 paper + talk，抽出技术点和现象；用我们的方法解释根因；基于根因建立新方法，解决新问题。

请输出一个表格：

- paper/talk
- 观察到的现象
- 使用的方法
- 方法直接控制的对象
- 作者给出的解释
- 我们可以提出的根因解释
- 和 nested learning / common-high-gain 机制的关系
- 能接到我当前 gating 主线吗：能 / 不能 / 需要补证据
- 如果能接，最小问题是什么

注意：这里“我们的方法解释根因”不能写成口号。必须指出根因对象，例如频率、公共方向、谱增益、梯度噪声、batch 覆盖不足、solution space 几何、或者表征空间曲率。

### 问题 C：谱空间打平后理论最大学习率是多少？

导师问题：

假设将谱空间打平的时候，理论的最大学习率是多少？分三种情况：

1. 数据没噪声，均匀，batch 包含所有样本。
2. 数据有噪声，均匀，batch 包含所有样本。
3. 数据有噪声，均匀，batch 不包含所有样本。

请先带我复习基础理论：

- 一维二次函数的梯度下降稳定条件。
- 多维二次函数中 Hessian 最大特征值 $\lambda_{\max}$ 和最大学习率的关系。
- 谱空间打平是什么意思：把不同方向的曲率或增益变得接近，使有效条件数变小。
- full-batch 与 mini-batch 的区别：full-batch 是确定性梯度；mini-batch 会引入梯度噪声。
- label noise / data noise 会改变最优点、噪声地板和泛化，不一定只改变稳定上界。

然后给出三种情况的理论框架：

- 无噪声、均匀、full-batch：稳定上界主要由打平后的最大曲率决定，经典近似是 $\eta < 2/\lambda_{\max}$。
- 有噪声、均匀、full-batch：经验风险仍是确定性目标，局部稳定上界仍看 $\lambda_{\max}$，但最优解、梯度残差和泛化风险会受噪声影响。
- 有噪声、均匀、mini-batch：除 $\lambda_{\max}$ 外，还要考虑梯度噪声协方差；过大学习率会造成稳定但高方差，或直接发散。

请不要只给结论。要说明：

- 大学习率与小学习率学习到底有什么区别？
- 大学习率是否更偏向平坦 basin、噪声平均、快速跨越弱方向，还是更容易放大高增益方向？
- 小学习率是否更稳定但可能被高频/common 方向慢慢锁定？
- 这些说法哪些是理论支持，哪些只是当前假设？

最后请给出“理论量”和“实验量”的对应表，例如：

- $\lambda_{\max}$ 对应 Hessian / Fisher / 梯度局部 Lipschitz 估计。
- 梯度噪声协方差对应不同 batch 的梯度方差。
- 谱打平程度对应奇异值分布、条件数、effective rank。
- common 去除效果对应 common band gradient mass、rare margin、SGD stable LR。

### 问题 D：seminar 中第二个方法为什么有效？

导师提示：

方法一定要从优化 solution space 解释；判断这个解释是否最优；如果不是，提出更优方法。

请先从 talk 中识别“第二个方法”到底是什么。如果无法从截图 PDF 直接识别，请要求我贴出对应页，不要猜。

识别后请回答：

1. 这个方法改变了什么对象：梯度尺度、动量、参数范数、谱方向、输出层 token column、表征几何，还是 solution space 中可达路径？
2. 它为什么可能有效：降低条件数、改变隐式正则、避开尖锐方向、抑制公共方向、扩大稳定学习率，还是提高稀有方向更新？
3. 这和表征空间的哪些根本性质有关：低秩性、谱各向异性、频率不均、组合嵌套、欧氏/非欧几何、层间放大。
4. 它是否是最优解释？如果不是，更好的解释或方法应该控制哪个更根本的量？
5. 如何设计一个最小诊断来区分“方法有效是因为优化路径”还是“方法有效是因为表征空间结构被改变”？

## 3. 和我当前 nested learning / gating 主线的连接规则

请使用下面的判断门：

- 影响当前假设吗？
- 影响 claim boundary 吗？
- 影响 next decision 吗？
- 建议：推进 / 暂停 / 只作为理论学习

目前可以接到主线的只有这类问题：

- Adam/SGD 差异是否来自 common/high-gain 方向造成的梯度尺度不均。
- 谱空间打平是否能提高 rare-feature margin 或减少 sign flip。
- 去 common 后的路由或优化是否提高 SGD 稳定学习率，并且不明显伤害语言模型损失。

不能直接接主线的是：

- 只比较 optimizer 最终 loss。
- 只说某个方法“更好”，但没有指出控制了哪个机制对象。
- 只讨论 general optimization，而没有连接到 common / rare / margin / spectral anisotropy 的可测量量。

## 4. 首轮输出格式

请先输出下面 5 部分，不要直接写完整 protocol：

1. 四个导师问题各自的“最清晰版本”。
2. 需要我补充的 talk 截图页或论文页。
3. 3 篇主读 paper + talk 的阅读顺序和每篇只读什么技术点。
4. 理论学习路径：从一维梯度下降到谱打平学习率，再到 mini-batch 噪声。
5. 能够接到 nested learning / gating 主线的最小问题，最多 2 个。

## 5. 语言和术语要求

- 先用中文解释具体含义，再给英文名或缩写。
- 不要用 common、rare、margin、gating、solution space、normalization 这些词替代解释；第一次出现必须定义。
- 公式必须用 `$...$` 或 `$$...$$`。
- 区分结果、解释、边界、猜想、下一步决策。
- 不要编造论文内容；读不到就说读不到。
