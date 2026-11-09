# 0915 SAE 三模型对比审计与后续小模型决策 Plan

> 状态：分析计划 / 不包含新的训练执行授权  
> 当前优先级：先审计已有 3 个模型，再决定是否启动 0.2B–0.3B 小模型因果复现实验。  
> 核心原则：先回答导师与学长已经明确要求的问题，不把“SAE 图更漂亮”直接解释成“主干语义更好”。

---

## 0. 本轮只回答一个中心问题

### Primary Question

**在预训练过程中，让 SAE 相关辅助损失的梯度进入主干，是否真的改变了主干表征，使我们预先定义的语义关系变得更可分、更稳定，而不是只让 SAE 自己更会重构或让图看起来更整齐？**

把因果链写成：

\[
L_{\mathrm{SAE}}
\rightarrow
\nabla_{\theta_{\mathrm{backbone}}}L_{\mathrm{SAE}}
\rightarrow
\theta_{\mathrm{backbone}}\text{ 改变}
\rightarrow
h\text{ 改变}
\rightarrow
z\text{ 更结构化}
\rightarrow
\text{语言建模/语义任务是否保持或改善}.
\]

其中：

- \(h\)：SAE 插入位置处、**尚未经过 SAE 的原始主干表征**；
- \(z\)：SAE 稀疏系数；
- \(\hat h\)：SAE 重构表征。

**本轮最核心证据是 \(h\)，不是 \(z\)。** 只有 \(h\) 本身发生稳定变化，才支持“SAE loss 塑造了主干 representation”。

---

## 1. 会议要求必须进入本计划

### 1.1 导师要看的内容

0914 会议中导师的要求可以压缩为三件事：

1. 不能只把 SAE 当离线分析器；SAE 相关 loss 必须能够一路反传影响前面的主干参数。
2. 在普通语言模型的交叉熵目标之外，加入一个以 SAE/结构化表征为目标的 regulation / penalty term。
3. 最终要看这种额外梯度是否让表征“更干净、更解耦、更可分”，而不是只报告 SAE 自身训练成功。

因此导师真正关心的实验对象是：

\[
\text{Baseline backbone representation}
\quad\text{vs}\quad
\text{SAE-gradient-shaped backbone representation}.
\]

### 1.2 学长要看的内容

学长会议把审计要求进一步具体化为：

1. **先看原始表征空间 \(h\)** 是否发生变化；
2. 再看 **SAE 激活 \(z\)** 是否更清晰、重构是否更可靠；
3. 不同 checkpoint 若独立训练 SAE，不能把“feature 编号相同”当成“语义相同”；
4. 若是同一套 SAE 连续训练，可以追踪同一参数槽位，但仍不能自动把固定编号解释为固定语义；
5. 当前 feature 对应问题不是第一优先级，应先完成“主干是否被 SAE 梯度改变”这一核心比较。

所以本轮分析顺序固定为：

\[
\boxed{
\text{模型身份/梯度路径}
\rightarrow
\text{训练健康}
\rightarrow
h
\rightarrow
z
\rightarrow
\hat h
\rightarrow
\text{任务性能}
}
\]

---

## 2. 先比较的三个模型

暂时用 M0/M1/M2 作为中性名字，避免在实现身份尚未核实前误命名。

| 模型 | 当前工作定义 | 需要审计的关键点 | 本轮作用 |
|---|---|---|---|
| **M0 Baseline** | 普通语言模型训练 | 是否完全没有 SAE；初始化、数据顺序、模型结构是否与其他模型一致 | 自然预训练基线 |
| **M1 Previous-SAE** | 之前训练的“装入 SAE”模型 | SAE 是旁路观察器还是串联重构进入 MLP；SAE loss 是否只更新 SAE；LM forward 是否经过 \(\hat h\) | 分离“插入 SAE / 重构瓶颈”本身的影响 |
| **M2 SAE-Backprop** | 当前 SAE 梯度反传模型 | SAE loss 的具体公式；梯度确实到达哪些主干层；forward 是否与 M1 完全相同 | 检验 SAE 辅助梯度塑造主干的效果 |

### 2.1 为什么必须先做 Model Identity Audit

现有材料中，M1 至少出现过两种描述：

- 描述 A：SAE 作为旁路观察器，\(h\to\mathrm{MLP}\) 保持原路径，\(h\to SAE\) 只训练 SAE；
- 描述 B：SAE 串联进入主干，MLP 实际接收 \(\hat h\)。

这两种模型科学含义完全不同。因此 **AI 在任何数值比较前，必须从实际 config、代码与 checkpoint 元数据核实真实路径**。

### 2.2 三模型比较的因果含义

若 M1 和 M2 **forward 完全一致，唯一差异是 SAE loss 是否反传主干**，则：

\[
M2-M1
\]

是本轮最干净的“SAE 梯度效应”对照。

而：

\[
M1-M0
\]

回答“仅加入 SAE 模块/重构路径是否改变训练”。

\[
M2-M0
\]

回答“整个 SAE 干预方案相对自然预训练的总效果”。

若 M1/M2 的 forward、初始化、数据顺序或训练 token 数不匹配，则 **M2-M1 不能直接解释为因果梯度效应**；这时三模型只能作为探索性证据，后续 0.2B 小模型负责补上严格匹配的因果实验。

---

## 3. Phase 0：模型身份与可比性审计（所有其他分析的 Gate）

AI 先为 M0/M1/M2 填完下面这张表。未核实项写 `UNKNOWN`，禁止猜测。

| 项目 | M0 | M1 | M2 |
|---|---|---|---|
| 参数规模 / 层数 / hidden size |  |  |  |
| 初始化是否相同 |  |  |  |
| tokenizer |  |  |  |
| 训练数据源 |  |  |  |
| 数据顺序 / seed |  |  |  |
| optimizer / LR schedule |  |  |  |
| 累计训练 token |  |  |  |
| 公共 checkpoints |  |  |  |
| SAE 插入层及精确 tensor |  |  |  |
| MLP 接收 \(h\) 还是 \(\hat h\) |  |  |  |
| LM loss 更新哪些参数 |  |  |  |
| reconstruction loss 更新哪些参数 |  |  |  |
| sparsity / dead-feature loss 更新哪些参数 |  |  |  |
| SAE 是否连续训练 |  |  |  |
| SAE 是否发生重置/重编号 |  |  |  |

### Phase 0 通过标准

至少明确：

1. 三个模型真正的 forward graph；
2. 每个 loss 的梯度归属；
3. 可进行公平比较的公共 checkpoint；
4. 哪些 pair 是严格匹配对照，哪些只是辅助比较。

若这四件事没有锁死，停止机制解释，只做实现审计。

---

## 4. 数据：三层数据各司其职

本轮**不新增训练**，先使用已有模型完成审计。

### 4.1 DCLM held-out：语言模型健康检查

用途只有一个：判断 SAE 干预是否损害/改善普通语言建模。

固定同一批 held-out token windows，对 M0/M1/M2 计算：

- NLL / perplexity；
- 按 sequence/window 的 paired difference；
- 不用训练集 loss 代替 held-out loss。

### 4.2 之前自己生成的层级语义数据：Primary Mechanism Panel

这是本轮**最重要的机制评测数据**。不要重新生成，先定位并冻结现有 manifest。

沿用已有外部语义定义：

\[
Y(x)=(\text{粗领域},\text{子领域},\text{具体事实},\text{内容属性}).
\]

关系顺序固定为：

\[
\text{同事实不同表达}
\succ
\text{同子领域不同事实}
\succ
\text{同粗领域不同子领域}
\succ
\text{不同粗领域}.
\]

这套数据的价值在于：语义关系由外部标签预先定义，不由 SAE、聚类或二维可视化反过来定义。

**AI 首先要定位并报告：**粗领域名称、子领域名称、事实数、每事实 paraphrase 数、train/dev/test 或模板族划分。当前计划不凭记忆补写这些数字。

### 4.3 M2D2：真实自然语言 External Validation

作为第二层外部验证，沿用项目已经使用过的 3×3 M2D2-Wikipedia hierarchy：

- Culture and the arts → Mass media / Performing arts / Visual arts
- Health and fitness → Exercise / Nutrition / Public health
- Natural and physical sciences → Biology / Earth sciences / Physical sciences

优先复用已有固定 split 与 window，不重新选择最容易出结果的领域。

M2D2 的定位不是训练数据，而是检查：

> 在受控合成/构造语义面板上观察到的 representation effect，是否能在真实领域文本中复现。

---

## 5. Phase 1：先证明模型和 SAE 都“有资格被解释”

这一阶段只做 measurement qualification，不讨论“语义变好”。

### 5.1 语言模型健康

每个公共 checkpoint、每个模型记录：

1. held-out NLL；
2. perplexity；
3. \(\|h\|_2\) 的均值、标准差与分位数；
4. 若 forward 使用 \(\hat h\)，同时记录 \(\|\hat h\|_2\)。

目的：防止“表征整体缩小”“forward 被重构瓶颈破坏”等情况被误解为 regularization 成功。

### 5.2 SAE 健康

对 M1/M2 在完全相同的固定评测文本上记录：

1. **归一化重构误差**

\[
E_{rec}=
\frac{\sum_i\|h_i-\hat h_i\|_2^2}
{\sum_i\|h_i-\bar h\|_2^2};
\]

2. 每 token 平均 active feature 数；
3. active feature 数分布；
4. 全数据 feature coverage；
5. dead feature ratio；
6. feature activation frequency distribution；
7. 激活频率集中度（可用 entropy 或 Gini，二选一并固定）；
8. 随机抽取约 20 个高频但非 common feature，列出 top activating texts。

**判定边界：**“每 token 激活少”本身不是语义证据；若整个数据集始终只有极少 feature 工作，更可能是 dictionary collapse / dead features。

### Phase 1 Gate

若 SAE reconstruction 明显失真、dead feature 比例极端或模型 LM health 异常，则后续语义分析标记为 `INSUFFICIENT_MEASUREMENT`，不能用漂亮热图下结论。

---

## 6. Phase 2：主结果——原始主干表征 \(h\) 是否更结构化

这是导师最想看的层，也是三模型比较的主判据。

**必须从 SAE 之前读取同一个位置的 \(h\)**。三个模型使用完全相同的 token、position、pooling 和 normalization 规则。

### 6.1 外部语义关系 margin（Primary Metric）

对固定语义面板，计算四类 pair 的余弦相似度：

\[
S_{fact},\quad S_{sub},\quad S_{coarse},\quad S_{cross}.
\]

并计算三个层级 margin：

\[
M_1=S_{fact}-S_{sub},
\]

\[
M_2=S_{sub}-S_{coarse},
\]

\[
M_3=S_{coarse}-S_{cross}.
\]

还需报告 ranking accuracy：在多少独立事实/模板组中，正确关系排序成立。

### 6.2 粗粒度/细粒度可读性

在 \(h\) 上分别计算：

- coarse-domain Fisher ratio；
- fine-domain Fisher ratio；
- coarse linear probe；
- parent-conditional fine linear probe。

probe 的 train/test 必须按 **事实或模板族隔离**，不能随机打散同一句 paraphrase，否则会把词面记忆当语义可读性。

### 6.3 高维关系矩阵

固定同一批样本构造：

\[
C^{(m,t)}_{ij}
=
\cos(h^{(m,t)}_i,h^{(m,t)}_j).
\]

用途：

- 比较同一模型随 checkpoint 的 geometry evolution；
- 比较三模型在同一 checkpoint 的关系矩阵差异；
- 量化整体变化，而不是依赖二维投影视觉判断。

### 6.4 可视化只作为辅助

可画 PCA / t-SNE；若已有统一 UMAP 规则也可补充。

规则：

- 固定样本；
- 固定颜色/标签定义；
- 同一比较尽可能共享投影规则；
- 不能用“哪个投影最漂亮”选择结论。

**二维成簇不是成功的必要条件。** 若高维 relation/probe 提升而二维图不成团，应报告“可读性增强，但强成簇假设未支持”。

---

## 7. Phase 3：SAE 系数 \(z\) 是否把结构读得更稀疏、更稳定

只有 Phase 2 完成后再解释 \(z\)。

### 7.1 在 \(z\) 上重复与 \(h\) 相同的语义任务

分别计算：

- coarse / fine probe；
- coarse / fine Fisher ratio；
- 同事实 / 同子领域 / 同粗领域 / 跨领域的系数相似关系。

这样才能比较：

\[
\text{semantic readability}(h)
\quad\text{vs}\quad
\text{semantic readability}(z).
\]

### 7.2 Sparse-combination reuse

对每个样本的 active set \(A(x)\)，计算同语义与异语义样本的：

- Jaccard overlap；
- weighted coefficient cosine（若数值尺度稳定）。

目标不是证明“一 feature = 一语义”，而是检验：

> 同一语义是否越来越倾向于复用相似的一组稀疏 feature，而不同语义的 feature combination 是否分化。

### 7.3 Domain × Feature heatmap

对粗领域/子领域计算平均激活，形成 domain × feature 矩阵。

至少同时给两版：

1. 原始激活；
2. 去掉最高频 common features 后的激活。

去 common 的阈值必须在看结果前固定，不能为了得到更清晰对角结构临时调整。

### 7.4 Feature 语义 sanity check

对候选高选择性 feature 列出 top activating texts 和语义反例。

只有满足：

- 不同表面表达的正例稳定激活；
- 语义反例低激活；
- 不是简单 position / punctuation / 高频 token shortcut；

才能把它称为“具有某种可验证内容选择性”，不能直接命名为“语义原子”。

---

## 8. Phase 4：重构表征 \(\hat h\) 是否保留了原始语义关系

对 M1/M2：

1. 在 \(\hat h\) 上重复 Phase 2 的 relation margins；
2. 在 \(\hat h\) 上重复 coarse/fine readability；
3. **固定 probe transfer**：只在 \(h\) 上训练 probe，不重新拟合，直接用同一个 probe 读取 \(\hat h\)。

核心量：

\[
R_{preserve}
=
\frac{\text{score}(\hat h)}{\text{score}(h)}.
\]

这一步回答的是 SAE 是否保留了我们真正关心的内容，而不是仅仅 MSE 很低。

---

## 9. Phase 5：M2 独有——SAE 梯度到底在怎样作用于主干

只有 M2 能直接回答这一层。

### 9.1 每层梯度强度

记录：

\[
r_l=
\frac{\|g^{SAE}_l\|_2}
{\|g^{LM}_l\|_2+\epsilon}.
\]

若 \(r_l\ll1\)，即使 M2 与 baseline 没区别，也不能立刻说 SAE regularization 无效——可能只是梯度太弱。

### 9.2 两个目标是否冲突

记录梯度余弦：

\[
c_l=
\frac{
\langle g^{LM}_l,g^{SAE}_l\rangle
}{
\|g^{LM}_l\|_2\|g^{SAE}_l\|_2+\epsilon
}.
\]

解释：

- \(c_l>0\)：两个目标局部大体一致；
- \(c_l\approx0\)：近似独立；
- \(c_l<0\)：SAE 结构目标与语言模型目标发生冲突。

### 9.3 若历史训练没有保存分 loss 梯度

不要伪造历史值。可以：

- 若 checkpoint + batch + loss 实现足以重放，做固定 batch 的 offline gradient audit；
- 若无法精确重放，标记 `NOT AVAILABLE`，只使用能够真实取得的 parameter/representation evidence。

---

## 10. Phase 6：跨 checkpoint 与 feature 对应问题怎么处理

### 10.1 对 \(h\) 的跨时刻比较

\(h\) 坐标来自同一主干架构，因此可以在固定位置、固定输入下比较关系指标随训练演化。

### 10.2 对 \(z\) 的 feature ID

分三种情况：

**A. 同一套 SAE 连续训练且从未重置/重排**  
可以把 feature ID 当“同一参数槽位”追踪，但不能自动声称语义恒定。

**B. 不同 checkpoint 独立训练 SAE**  
禁止直接比较 `feature 17 at t1` 与 `feature 17 at t2`。

**C. 跨 M0/M1/M2 的不同 SAE**  
默认不存在 feature-coordinate correspondence。主比较使用 permutation-invariant 指标：probe、relation score、Jaccard 分布、NMI/ARI、coverage、选择性统计等。

### 10.3 交叉读取（若实现允许）

选择早/中/晚三个时刻，例如公共 checkpoint \(t_a,t_b,t_c\)，测试：

\[
E_{t_a}(h_{t_a}),\quad E_{t_a}(h_{t_b}),\quad E_{t_a}(h_{t_c}),
\]

以及晚期 SAE 读取早期表征。

若固定 SAE 后晚期 \(h\) 仍明显更可读，才支持“变的是主干，而不只是 SAE 自己越来越会解释”。

---

## 11. 三模型最终比较矩阵

每个公共 checkpoint 至少形成以下主表：

| 证据层 | 指标 | M0 | M1 | M2 | 主比较 |
|---|---|---:|---:|---:|---|
| LM health | held-out NLL/PPL |  |  |  | M2 是否付出性能代价 |
| Representation scale | \(\|h\|\) |  |  |  | 排除缩放假象 |
| Raw semantic geometry | \(M_1,M_2,M_3\) |  |  |  | **Primary** |
| Raw readability | coarse/fine Fisher |  |  |  | **Primary** |
| Raw readability | coarse/fine probe |  |  |  | **Primary** |
| SAE health | normalized rec. error | N/A |  |  | 尺子质量 |
| SAE health | active count / coverage / dead ratio | N/A |  |  | 尺子质量 |
| Sparse semantics | coefficient relation / Jaccard | N/A |  |  | SAE 是否更结构化 |
| Reconstruction | fixed-probe retention | N/A |  |  | SAE 是否保留内容 |
| Gradient | \(r_l,c_l\) | 0/N.A. | 0 或 N.A. |  | SAE 梯度机制 |

### Primary statistical unit

优先按**独立事实、模板族或 window**做 paired bootstrap / confidence interval；不要把同一句话里的大量 token 当成独立样本。

---

## 12. 结果判断树：我们允许得出什么结论

### Branch A：M2 的 \(h\) 明显优于 M1/M0，LM health 基本保持

支持：

> 在当前训练配置中，SAE 辅助梯度能够改变主干训练轨迹，并提高预定义语义关系的可读性/可分性。

若同时 \(z\) 更稀疏稳定、\(\hat h\) 保留语义，则证据链更完整。

**仍不能声称：**已经得到最优 regularizer、普适大模型收益或因果“语义原子”。

### Branch B：M2 只在 \(z\) 上更漂亮，但 \(h\) 不变

结论：

> 当前改善主要发生在 SAE 读法，尚无证据证明主干 representation 被有益重塑。

下一步应检查 gradient strength、loss design，而不是直接强化语义主张。

### Branch C：M2 的 \(h\) 更可分，但 LM NLL 明显恶化

结论：

> 正则项确实塑造了 representation，但存在明确的任务 trade-off；当前 loss 不是合格的最终方案。

下一步才进入 \(\lambda\)、loss 形式或 sidecar regularizer 的设计。

### Branch D：M1 与 M0 已有明显差异，M2 与 M1 差异不大

首先检查 M1 是否改变了 forward path。

若 M1 使用 \(\hat h\) 串联主干，则可能说明主要变化来自 reconstruction bottleneck，而不是 SAE auxiliary gradient。

### Branch E：M2 与所有模型都无明显差异

不能立刻宣布假设失败。依次检查：

1. SAE 梯度是否真的到达主干；
2. \(r_l\) 是否过小；
3. SAE 是否 collapse；
4. 当前 token budget 是否足以产生目标结构；
5. 评测面板在成熟模型上是否具有检测能力。

这些均排除后，才支持“当前 SAE loss 在该设置下没有可检测的 representation shaping effect”。

### Branch F：三模型实现不匹配，无法做干净因果比较

本轮仍完成描述性审计，但把结论限定为 association / diagnostic evidence。

随后启动 0.2B–0.3B 严格匹配小模型实验。

---

## 13. 什么时候启动 0.2B 小模型

**现在先不启动。** 先把已有三模型审计做完。

满足下列任一条件再启动：

1. 三个已有模型之间 forward / init / data 不匹配，现有结果无法隔离 SAE gradient；
2. M2 出现明确 representation signal，需要用低成本严格匹配实验复现因果；
3. M2 出现疑似负作用，需要快速区分“regularizer 本身有问题”还是“大模型训练噪声/配置问题”。

小模型的第一版不要做复杂新 loss，先做最小因果 pair：

\[
\text{same init + same data + same forward}
\]

只改变：

\[
\nabla_{\theta_{backbone}}L_{SAE}=0
\quad\text{vs}\quad
\nabla_{\theta_{backbone}}L_{SAE}\neq0.
\]

0.2B 小模型的作用是**机制复现**，不是替代当前三模型证据，也不是直接证明大模型 Scaling 结论。

---

## 14. AI 协同执行顺序

### Agent A：Model / Gradient Auditor

只负责 Phase 0 与 Phase 5。

交付：

- `00_model_identity.md`
- `00_model_identity.csv`
- 三模型 forward graph；
- loss → parameter 梯度表；
- 公共 checkpoint 列表；
- 严格可比 / 不可比 pair 判定。

**禁止：**在实现未核实前解释实验结果。

### Agent B：Representation Auditor

只使用固定数据面板分析 \(h\)。

交付：

- `01_lm_health.csv`
- `02_raw_h_semantic_metrics.csv`
- relation margins / Fisher / probe / relation matrix；
- 必要的 PCA/t-SNE 辅助图。

这是导师主问题的负责人。

### Agent C：SAE Auditor

负责 \(z\) 与 \(\hat h\)。

交付：

- `03_sae_health.csv`
- `04_sparse_semantic_metrics.csv`
- `05_reconstruction_preservation.csv`
- dead-feature / coverage / frequency 图；
- domain × feature heatmap；
- top-feature activating text 审计。

这是学长要求的“SAE 本身是否可靠、激活是否更清晰”的负责人。

### Agent D：Evidence / Story Auditor

最后才读取 A/B/C 的结果。

交付：

- `06_three_model_comparison.md`
- 每个核心差值的 confidence interval；
- strongest rival；
- supporting / non-supporting / insufficient 三类判断；
- **不能声称什么**；
- 是否触发 0.2B 小模型的唯一 next decision。

禁止从 PCA/heatmap 单独下结论。

---

## 15. 最终汇报结构

最终汇报不要按“我跑了哪些脚本”组织，而按下面故事线：

### 15.1 实验前直觉

> 自然预训练会逐渐产生语义组织；如果额外 SAE 结构梯度能够帮助这种形成过程，那么在相同训练阶段，M2 的原始主干表征 \(h\) 应比 baseline / no-backprop SAE 更早或更强地表现出外部定义的粗细语义关系。

### 15.2 实验设计

三个模型、同一批固定语义样本，依次比较：

\[
\text{LM health}
\rightarrow h
\rightarrow z
\rightarrow \hat h
\rightarrow \text{gradient mechanism}.
\]

### 15.3 真实结果

只展示能回答下面三个问题的图：

1. **主干真的变了吗？** —— \(h\) 的 relation margin / coarse-fine readability；
2. **SAE 是否把结构读得更好？** —— SAE health + \(z\)；
3. **这种变化付出了什么代价？** —— held-out LM loss。

### 15.4 差异与竞争解释

重点区分：

- natural pretraining formation；
- SAE observer adaptation；
- reconstruction bottleneck；
- SAE auxiliary gradient；
- feature/dictionary collapse；
- lexical/template shortcut。

### 15.5 认识更新

结论必须落在以下四种之一：

- `SUPPORTED`：SAE 梯度改变主干并改善目标关系；
- `TRADEOFF`：主干改变但语言建模受损；
- `NOT SUPPORTED`：有足够干预但未检测到目标变化；
- `INSUFFICIENT`：实现、SAE 测量资格或对照条件不足。

最后只给一个 next decision：**是否值得启动严格匹配的 0.2B 小模型。**

---

## 16. 今晚执行优先级

若时间有限，按以下顺序停止也能形成完整的阶段性结论：

1. **Phase 0：三模型身份与梯度路径审计**；
2. **Phase 1：LM + SAE health**；
3. **Phase 2：原始 \(h\) 的 coarse/fine relation + probe**；
4. Phase 3：\(z\)；
5. Phase 4：\(\hat h\)；
6. Phase 5/6：gradient decomposition 与 cross-read；
7. M2D2 外部验证；
8. 最后才决定 0.2B 新训练。

如果今晚做到第 3 步，就已经能回答导师当前最重要的问题：

> **让 SAE loss 回传以后，原始主干 representation 到底有没有发生我们想要的结构变化？**

---

## 17. 审计底线

- 不把 SAE 重构误差降低等同于语义更好；
- 不把二维 cluster 更漂亮等同于语义形成；
- 不把独立 SAE 的同编号 feature 当作同一语义；
- 不把 M2 与不匹配 baseline 的差异直接称为 SAE gradient 因果效果；
- 不把一个小模型结果推广成大模型普遍规律；
- 不因结果不符合直觉而修改样本、投影、阈值或主要指标；
- 未核实的信息写 `UNKNOWN`，没有结果的实验写 `NOT RUN`。

---

## 18. 本轮最简一句话

> **先用已有 M0/M1/M2 做一次从“实现身份 → SAE 测量资格 → 原始表征 → 稀疏系数 → 重构 → 任务损失”的完整审计；只有确认 SAE 梯度确实对主干产生了可解释信号，或现有三模型因配置混杂无法裁决时，再启动 0.2B 小模型作为严格匹配的机制复现实验。**

