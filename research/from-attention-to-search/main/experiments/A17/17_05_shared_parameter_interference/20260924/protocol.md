# Protocol：单组正式曲线、共享拖累、隔离收益与局部互损

## 0. Approval Snapshot

**当前契约状态：六条件×三种子的正式训练已获研究者明确授权；§18 是最新执行修订，优先于以下历史性的阻塞与顺序门控表述。实际执行和完成证据由该节指向的执行记录持有；确认分析判据仍待研究者确认。**  
研究者已明确选择从零即采用 \(\lambda_{rec}=0.1\) 的 S7 21B 检查点，要求新增秩 16 的 A-only/B-only 正式曲线，并要求先完成基础工程 Smoke。Smoke 仅检验工程路径；数据资格与六条件正式训练均未获执行授权。

**主要 Anchor：**[anchor_cn.md](../../../../problem_anchors/17_shared_and_interference_learning/17_05_shared_parameter_interference/17_05_shared_parameter_interference_anchor_cn.md)。正式父 Anchor、稳定 problem_key 和 Focus 尚未确认。本次按用户明确要求完成候选文档修订，保持日期目录中的单份草案；不创建或重置其它工作的 Focus，不将草案提升为批准契约。通俗方法与审计见 [README_cn.md](README_cn.md)。

**目的：**用正式 A-only/B-only 曲线先确认各组能学、共享后在相同本组词元暴露量下是否落后；再检验按组隔离能否缓解，以及是否有局部互损。21B 是已训练 210 亿词元，不是模型参数量。第一阶段不构建 SAE 路由器。

**前置资格：**先训练秩 16 的 A-only/B-only 两组正式曲线；其开发集改善承担进入其余四条件的资格门，终点独立确认结果则承担共享拖累对照。数据不按冲突或隔离收益挑选。

**条件：**A-only/B-only 各一套秩 16；原四组 S16/S8/D8/R8 保留。单组与共享秩 16 比较时对齐本组累计有效词元和更新次数；原四组仍对齐总训练词元、数据顺序与全局批量。所有增量只加在第 8 块前馈网络的下投影。

**判定顺序：**独立确认集先逐领域比较 S16 与 A-only/B-only 的同本组暴露量损失，判共享拖累；再以 S16−D8 与 R8−D8 判隔离收益和领域分组价值；回滚诊断另判局部互损。三个判断分别报告，具体阈值仍是待确认提案。

**支持分支：**两组单独可学；至少一组在共享下被拖累；隔离在受拖累领域改善且胜混合分组；局部互损另行成立。每一环节可以分别失败或证据不足，见 §15。

**保留边界：**同一 21B 起点；主干与 SAE 冻结；先人为隔离、后验证 SAE 信号。具体谱系已由研究者定为从零低系数 S7，原稿的重加权候选已被替换。

**新增阈值、数据集与未明确的优化细节仍为 `AI_PROPOSAL`。** 检查点 SHA-256 与本地单步加载已核；数据修订版／文档边界／库存、正式归属和科学执行授权仍阻塞。研究者于 2026-09-24 要求停止四卡 5090 Spot Smoke `pt-xmk3zndq`，并以同范围四卡 H100 Reserved Smoke `pt-8pr2e57p` 替代。5090 任务仅完成运行时与单机预检后被停止；H100 的持久化日志与独立产物审计记录六组工程 Smoke `PASS`。该结果仅证明工程资格，正式科学实验仍 `NOT RUN`；平台状态查询在核验时滞后，不能据此声称 ACP 已给出终态。

**冻结状态：**正式科学设计尚未冻结；A–F 含待确认细节，G 的正式执行仍阻塞。研究者已单独授权基础工程 Smoke；其合成数据结果不判可学性，也不自动授权六条件正式矩阵。

## 1. Terminology / Definitions

- **有效预测词元：**本次下一词元损失中实际参与计算、目标不为忽略值的位置。计数跨数据并行副本合并一次，不把复制计算算成新数据。
- **新增词元 N：**本轮适配从 21B 检查点开始后处理的有效预测词元数。不能把所有曲线仍标成从零预训练，也不能把 21B 加到效率倍率分子分母中。
- **本组暴露量 \(n_d\)：**条件实际用于组 \(d\) 梯度的有效目标数；共享四组的总 \(N=n_A+n_B\)，A-only/B-only 只有一组非零。单组曲线比较以 \(n_d\) 而非 \(N\) 对齐。
- **低秩适配 LoRA：**对冻结线性权重 \(W_0\) 加 \(sBA\)，只训练 \(A,B\)；秩 r 控制增量分解维数，\(s=\alpha/r\)。
- **固定分组 LoRA 专家：**每条文本记录只调用两个 LoRA 中的一个；不含可学习门控、辅助均衡损失或第二个主干。
- **总可训练参数量：**所有独立 A、B 标量总数，包括该词元未用到的专家。**活跃秩：**每个词元本次用到的增量秩。二者不是同一预算。
- **局部互损：**在相同参数、优化器状态上，某组数据引出的更新使另一组独立数据的损失变差。不能由类别不同或最终参数距离直接定义。
- **数据分配单位：**原始文档及其派生窗口；不是 SAE 原子，也不是自动识别出的“纯语义”。

## 2. Anchor Alignment

本实验检验 Anchor 的 H1a（共享拖累）、H1b（隔离缓解）和 H1c（局部互损），分别报告，且受单组正式曲线的开发集可学性门约束：

1. 本组暴露量相同时，单独学习与共享学习的预测质量是否有差距。
2. 原四条件下按组分开是否缓解差距，领域分组是否优于混合分组。
3. 同一共享参数状态上，是否出现可回滚验证的跨组损害。

SAE 的预测能力属于后续 H2。本轮最多留下固定信号与诊断标签的对应材料，不能在本轮提前声称它具有路由价值。

本轮不要求重新从头训练 21B 主干，也不复现学长的完整模型训练方法；只训练已有模型上的少量增量参数。

## 3. Tested Hypothesis

**候选解释：**两组数据对同一增量参数的更新会在一些状态上互相损害；让它们使用不同增量，可能避免这一影响。这不是“数学必须到某个参数终点、生物必须到另一个终点”的假定。

**曲线预测：**A-only/B-only 各用秩 16，在相同本组词元暴露量下，至少一个领域比共享秩 16 的该领域确认损失低。**隔离预测：**D8 优于 S16 和混合分组 R8，并在出现共享拖累的领域减小差距。

**机制预测：**总参数预算主对照——共享秩 16 的预设训练状态上，一类数据的虚拟更新在改善该类独立损失的同时，使另一类独立损失变差；该现象超过同域抽样和无新梯度动量的对照，并在半步长下不完全消失。

这是可证伪的候选，不假定两领域都必然受损，也不把一次负梯度夹角当作长期学习失败。

## 4. Rival Explanations

| 竞争解释 | 为何单纯共享/分开不能区分 | 本轮对应检查 | 剩余边界 |
|---|---|---|---|
| 当前任务没有可测改善空间 | 无差距可能只是两边都学不动 | A-only/B-only 正式曲线的开发集改善资格门 | 未通过不能区分饱和、位置／秩不足和优化失败 |
| 两个专家只是多了参数 | 两个 r=8 专家是共享 r=8 的两倍增量参数 | 共享 r=16 总参数匹配 | 函数类与每词元计算仍不同 |
| 分组/优化统计改善，不需要测得的跨域互损 | 同域批次更一致也可能改善适配 | 固定混合分组与局部互损检查 | 不能完全识别长期中介机制 |
| 负梯度关系只是批次噪声、步长过大或动量 | 梯度夹角和实际更新方向不完全相同 | 独立目标数据、同域、无新梯度、半步长对照 | 局部结论仅对指定状态和更新成立 |
| 平均损失掩盖一方退步 | 一方大幅改善可掩盖另一方受损 | A/B 分开报告；双方验证质量联合达标 | 不预设所有任务同时获益 |
| 标签或词面差异被叫作语义机制 | 外部领域标签可能直接提供有利条件信息 | 不输入标签文字；两种分组都使用固定外部索引；明确上界性质 | 本轮没有学会从文本自动分发 |

数据频率首轮固定为 1:1，不在本轮增加长尾比例扫描。此举是控制，不是证明频率因素不存在。

## 5. Data Construction And Provenance

### 5.1 候选来源——明确推荐，但尚未冻结

使用 M2D2 官方数据集 `machelreid/m2d2` 的同一维基百科来源：

- A：`Mathematics_and_logic__Mathematics`。
- B：`Natural_and_physical_sciences__Biology`。

本次已在官方数据卡核到这两个配置名；但当前版本含多少合格长文本、源行是否等于完整文档，**本轮未下载验证**。完整版本号/文件哈希与文档边界核验是执行前阻塞项。不得因旧加载脚本要求任意代码执行而直接开启未经审核的远程代码。

选择理由：从同一来源取两个内容领域，减少“论文与网页”“不同语言与不同任务格式”带来的额外变化。它仍不能排除词频、难度等差异，也不能证明标签之间天然冲突。

旧 N8 是已经用于表征审计的固定分类面板，不能直接把其确认集重新作为本轮训练集。可借用数据读取经验，不继承旧划分、旧标签结论或旧确认资格。

### 5.1a 数据选择规则与八来源备选

**AI 建议：先资格检验 M2D2，不因“训练过 21B”直接排除，也不为了更容易得到正结果立刻换数据。** 没有剩余学习空间可能掩盖干扰；但高初始损失也可能来自不可学噪声或容量不足，不能当作可学性证据。必须实际检查独立开发数据上的单组改善（§13 阶段 B1）。

源码核验的旧八来源为 MMLU、MMLU-Pro、BBH、GSM8K、MATH、GPQA、HumanEval、MBPP。旧 `render_record` 将它们分别转换为选项字母、自然语言答案、解题过程或程序代码；旧模型是官方 28 层 Qwen，非本轮 8 层 21B 模型。故“旧任务能学”不是本轮资格证据，旧八来源也不是 N8 表征面板。

若 M2D2 不具备可恢复文档边界、库存不足或单组正式曲线的可学性未通过，**暂停正文路线并记录原因**。不运行其余四条件搜索冲突。备选只做纸面／只读来源筛选：优先从单一问答来源内选两个同格式、同标签规则且库存充足的学科，例如 MMLU 内两个学科；学科身份尚未冻结，不假定数学／生物够用。旧 GPQA/HumanEval 小样本也不因领域鲜明就自动采用。若选跨来源问答，必须明确允许的任务／格式混杂，结论改为任务组适配，而非纯内容领域机制。

切换后训练路线前，重审同一 Protocol 的 B–F。若尚未执行冻结，可直接修订；若已执行 A-only/B-only 正式曲线，必须保留当时正文并追加带前后值、已见证据、批准范围和资格影响的变更记录，不能回写旧判据。新确认部分必须在其训练／确认前重新冻结，至少确定：

- 原题与答案来源、题目家族去重、训练／开发／诊断／新确认的清单；旧测试或反复看过的题不冒充新确认。仅重新划分旧题不能抹去其选择历史；没有可辩护的新确认则限于探索。
- 同一输入模板，只对答案目标计损失，prompt 与 padding 目标置为忽略；空答案、标签歧义或答案被截断的记录排除并记原因。选择题模型输入不能带正确答案，答案仅作为训练目标。
- 从实际答案长度计算有效预测词元，按每组相同有效词元预算构造精确批次；**不得沿用“32 条×512＝16384 个有效目标”**。需要按答案序列边界构造或明确最后批次规则，不能把输入长度作为监督量。
- 参数矩阵沿用只是候选；批量、预算、DEV 改善门槛、主效应实际门槛和效率目标全部按新目标重审。正文 nats/token 和答案 nats/token 不能横向排名。

新路线也必须通过单组资格门。候选队列只含当前正文对与一对经人工确认的同格式问答候选；不自动扩成八来源全配对搜索。所有候选失败和修改均留痕，若根据未来开发诊断选“最冲突”组对，只能称探索发现并另设独立确认。

### 5.2 记录与去重

构造字段：`record_id, source_doc_id, duplicate_cluster_id, source_revision, source_config, domain_id, original_split, text_sha256, text`。

正文外的领域标记、文件名、数据集路径、文档 ID 不输入模型。文档 ID 仅用于去重、划分、固定随机分组和不确定性估计。

先去除精确重复文本，并按近重复簇统一归属。候选近重复规则为规范化文本的词 5-gram Jaccard 相似度至少 0.8；具体实现与版本在数据清单中冻结。跨领域重复簇不允许以两个标签重复进入；本轮直接排除并报告数量。

必须验证原始文档边界；若只有无关联的段落行且无法追溯原文档，不可声称文档级无泄漏。该情况下先阻塞，不静默改成随机行划分。

每个领域从候选训练、开发、确认来源各人工检查至少 20 条，共 120 条：可理解正文、来源标签合理、没有乱码/目录主体/明显重复。记录排除理由，不根据梯度或最终模型表现筛数据。

### 5.3 五种信息角色

优先保持官方训练、验证、测试划分，并在去重后保证跨划分的簇不重叠：

| 划分 | 作用 | 不能用于 |
|---|---|---|
| TRAIN | 正式适配梯度、训练序列 | 确认统计 |
| DEV | 检查训练资格、预定验证阈值、显示学习曲线 | 代替确认集的主要效果判定 |
| DIAG_UPDATE | 只为可回滚诊断产生更新；从官方 train 保留 | 正式训练与最终确认 |
| DIAG_READOUT | 对诊断更新作独立损失读取；与前者不同文档 | 产生该次更新、调整阈值 |
| CONFIRM | 所有配置冻结、全部训练完成后，解封预算末端效果 | 学习率选择、训练停止、选择“有冲突”的数据 |

若官方文件缺少上述任一划分，必须在训练前以文档/重复簇划分、记录并重新确认；不能在训练后补切。

### 5.4 分词、窗口和拟用规模

复用该 21B 检查点对应的实际分词器；不得替换为另一个同名但不同版本的分词器。历史记录指向 `/data/share/Qwen3-0.6B-Base`，需核对实际词表与哈希。

候选统一规则：纯正文，`add_special_tokens=False`，不添加领域前缀；取同一文档中 513 个连续词元，前 512 个作输入、后 512 个作目标，因此每窗恰有 512 个有效预测目标。窗口不跨文档、不重叠，尾部不足部分舍弃。使用因果注意力；不可把多个不同文档随意拼接后仍声称记录级隔离。

拟用规模（全部为 AI 提案、库存不足时必须训练前修订）：

- TRAIN：每域 16,384 个窗口，共 32,768 窗、16,777,216 个有效目标；本轮最多一遍，不用重复曝光补足库存。
- DEV：每域 128 个窗口，尽量来自 128 个不同文档。
- CONFIRM：每域 512 个窗口，尽量来自 512 个不同文档。
- DIAG_UPDATE：每域 512 个窗口，每个文档/近重复簇只取一个窗口；供 32 组、每组 16 窗的局部更新使用。
- DIAG_READOUT：每域 128 个窗口，每个文档/近重复簇只取一个窗口。两个诊断划分及正式训练/开发/确认均无共享文档或重复簇。

每文档训练窗口上限为 4，按固定哈希排序截取，不让少数长文档占据多数梯度。长文档筛选偏差必须写入结果边界。未满足数量时不自动放松过滤或改领域；先记录实际可用规模并修订预算。

### 5.5 同一数据序列和混合分组

在 TRAIN 内，每个领域先按文档固定分成两个近似等量组 R0/R1。用种子 20260924 的哈希及固定贪心分配平衡合格窗口数，并生成不可变的 `route_manifest.jsonl`。同一文档及派生窗口只能落在同一个随机专家。

每次全局更新取 A-R0、A-R1、B-R0、B-R1 各 8 个窗口，再按固定排列交给所有条件。这使每步：A/B 各 16 窗，按域专家各 16 窗，混合专家也各 16 窗。随机专家每个都有 8 个 A 和 8 个 B。

A-only/B-only 每步只取该共享批次中本组原有的 16 窗，保持组内顺序；不得另抽较容易文本或重复另一半窗口凑足 32 窗。单组实际有效批量为 8,192，本组暴露量与 S16 的对应领域逐步一致。

原四条件消费**同一批记录、同一顺序、同一输入和目标**；单组条件消费其中相应领域的严格子序列。验证、确认使用相同领域文档并固定分组，不能每次重新抽路由。

## 6. Learning Task And Permitted Supervision

任务统一为下一词元语言建模；A/B 不使用不同任务头、不同输出格式或不同标签质量标准。

按域专家可使用数据集给出的领域标签作为**外部固定分配信息**。这是检验参数隔离效果的条件，不是模型已经能够从输入自动识别领域的证据。混合专家使用同样固定形式的分组索引，但索引与领域无关。

真实下游推理可能没有这种标签；故当前结果属于已知分组的适配测试，不能叫自动路由性能。SAE 不读取目标答案来决定本轮路由，也不使用未来词元构造在线决策。

## 7. Model / Architecture And Frozen Variants

### 7.1 检查点身份

研究者指定的从零低系数末层 SAE 21B 起点为：

```text
/data/250010109/MoE_Router/experiments/
20260920_s7_lambda0p1_from_scratch_4h100/
runs/S7_lambda0p1_from_scratch_4h100/
milestones/token_021000000000
```

以上为换行展示的一条路径。历史清单记 `tokens_seen=21000000000`，`state.pt` SHA-256：

```text
edd781c8f747477e9f236128d26423d435c800d37da2d446c85e4a6ebc206f33
```

它从第 1 次更新起采用 \(\lambda_{rec}=0.1\)，不是先训练后调权重的 S7。2026-09-24 已重算 4.1GB `state.pt` 哈希并与完整里程碑清单一致；本地 GPU 已加载该权重并核对末层下投影形状及一次冻结主干更新。四卡 5090 环境仍须独立验收。

### 7.2 原生计算链及推荐插入点

源 Protocol 定义：Python `blocks[7]` 为第 8 块；\(a\) 是注意力输出投影后、残差相加前的返回值，SAE 直接读取 \(a\)，没有额外侧路归一化。原生主路是：

```text
第 8 块输入 x（冻结）
    → 注意力（冻结）→ a
                        ├→ 冻结 SAE 编码 z（只观察）
                        └→ x+a → 原 Norm2 → 原前馈网络上投影/门控 → u
                                                                   ↓
                                              原下投影 Wd u + LoRA_e(u)
                                                                   ↓
                                                  残差相加 → 冻结输出端 → 语言损失
```

第一轮只改 **最后一层前馈网络下投影**。这是线性映射的语义定位；已读 0916 原生旁路实现：实际属性是 `blocks[7].down`，其输入为 `silu(gate(norm2(x+a))) * up(norm2(x+a))`。仍须对选定谱系的真实运行源码快照与权重验收，不能把读到工程参考实现等同于加载资格通过。

历史结构为隐藏宽度 1024、前馈中间宽度 3072，所以预计该权重形状为 `[1024,3072]`。若真实权重或张量顺序不同，停止模型资格检查并修订，不能静默换到注意力输出投影。

**为何不首选注意力输出投影：**那会直接改变 SAE 的输入；即使 SAE 权重冻结，其激活也会随训练变化，不能再把它当作所有条件共享的固定先验信号。**为何不全部线性层都加：**首轮需要明确一个受限更新机制，避免多个插入点共同改变表征而无法定位。

### 7.3 LoRA 形式与参数数目

\[W_{eff}=W_d+sBA,\quad s=\alpha/r,\quad A\in\mathbb R^{r\times3072},\quad B\in\mathbb R^{1024\times r}.\]

候选基准秩 \(r=8\)，所有条件统一 \(s=1\)：秩 8 用 \(\alpha=8\)，秩 16 用 \(\alpha=16\)。不自动启用其它秩缩放、增量偏置或变种。

| 条件 | 专家/共享形式 | 总可训练参数 | 每词元使用的 LoRA 参数 | 核心用途 |
|---|---|---:|---:|---|
| S8 | 共享 r=8 | 32,768 | 32,768 | 活跃秩匹配参照 |
| S16 | 共享 r=16 | 65,536 | 65,536 | **总预算匹配主对照** |
| D8 | 两个独立 r=8，按领域固定选择 | 65,536 | 32,768 | 领域隔离 |
| R8 | 两个独立 r=8，固定混合分组 | 65,536 | 32,768 | 分组有效性对照 |
| A-only | 单独学 A 的 r=16 | 65,536 | 65,536 | 与 S16 匹配秩、A 暴露量及更新数 |
| B-only | 单独学 B 的 r=16 | 65,536 | 65,536 | 与 S16 匹配秩、B 暴露量及更新数 |

表中数字由 \(r(3072+1024)\) 推导，须由真实参数枚举复核；不含冻结主干/SAE，不含路由器，因为本轮不训练路由器。

**不存在使上述所有量同时相等的单个共享对照。**S16 与 D8 总参数相同但活跃秩不同；S8 与 D8 活跃秩相同但总参数不同；D8 与 R8 才同时匹配这两者和负载。不能把“固定总参数”写成“函数类、优化几何与运算量完全等价”。

A-only/B-only 每步只消费对应组的 16 窗；S16 每步消费同样 16 窗该组加 16 窗另一组。因此单组与 S16 各领域暴露量、秩和更新数一致，但单组全局有效批量为共享的一半，目标归一化不同。其曲线差是本配置下的共享拖累读数，不能单靠它宣称另一组梯度的纯因果伤害。

### 7.4 初始化与“两个专家是否相同”

同一个配对种子内：D8 和 R8 的两个专家均为 S8 初始 A、B 的**数值复制**，但具有独立参数对象和独立优化器状态。A 使用 `Uniform(-1/sqrt(d_in),1/sqrt(d_in))`，B 为零。两者不能都设为零，否则双线性增量的两组梯度都可能为零。

S16 的前 8 行 A 与 S8 一致，后 8 行独立采样，B 全零。禁止复制相同两半而让秩 16 从完全对称的重复子空间开始。所有条件初始增量均为零，初始预测必须相同。相同缩放和学习率并不保证跨秩有效函数步长相同，因此 S16 比较始终保留秩/条件化函数类的边界。

训练后专家可以不同，也应该允许不同；必须一致的是初始化规则、秩、缩放、模块位置、优化器与负载，不是训练过程中强制权重相等。

### 7.5 精确退化等价测试

工程小测额外构造一个不正式长训的“绑定专家”版本：两个专家的 A、B 引用同一参数对象，而不是各自复制。由于每个样本只选择一个专家，前向退化为普通共享 r=8。

在相同输入、相同全局平均损失、优化器参数去重且无双重更新时，检查：输出、A/B 梯度、一次优化器更新均与 S8 相同。不能用“分别算两个专家局部均值后直接相加”代替全局损失，那会多乘常数。

### 7.6 冻结和缓存边界

- 所有原主干权重、归一化参数、输出头和 SAE 权重 `requires_grad=False`；SAE 活动/死原子计数等缓冲区也不得改变。
- 基座与 SAE 使用确定性评估行为；LoRA dropout=0，且不隐式开启主干 dropout。
- **冻结 SAE 还不够：本轮明确关闭重构/AuxK 损失。**总训练目标只有语言损失；不把旧训练脚本的 SAE 正则默认带入。
- 在相同输入上，\(a,z,u\) 应对各条件和训练时刻一致；保存一个固定 sentinel 面板做差异检查。
- 允许对 LoRA 之前的冻结计算使用 `no_grad`。不允许对 LoRA 之后的冻结归一化和语言头整体使用 `no_grad`，否则会切断到 LoRA 的梯度。
- 第一轮不预缓存整个数据集的巨大 dense 激活；统一在线前向，仅对固定诊断面板保存所需特征。后续缓存加速不得只给某一条件，且系统速度比较要计入缓存成本。

## 8. Training Objective And Optimization

### 8.1 唯一目标和归一化

\[L=\frac{\sum_{t\in V}\ell_t}{|V|},\qquad \ell_t=-\log p(w_t\mid w_{<t}).\]

原四组全局每步 A/B 各一半。D8、R8 的每个专家接收全局样本一半，因此其局部梯度在该目标中具有 1/2 的权重；不能私自按专家独立均值再做一次等权求和。A-only/B-only 则只对本组 16 窗求有效目标平均，不填充或重复另一组窗口。每条轨迹的日志须同时写实际有效目标数与每组暴露量；数据并行必须还原各自全局词元分母。

### 8.2 候选统一优化设置

| 设置 | 提案值 | 理由与边界 |
|---|---|---|
| 训练器 | 同一个训练循环和 loss reduction | 避免“共享版”和“专家版”不同脚本 |
| 优化器 | AdamW；仅包含 LoRA A/B | 原基座优化器不恢复进新任务 |
| 学习率 | 峰值 1e-3 | 待工程小测验证数值资格，不是已证最优 |
| 动量系数/epsilon | (0.9,0.999) / 1e-8 | 全条件一致 |
| 权重衰减 | 0 | 避免把额外正则差异当隔离效应 |
| 梯度裁剪 | 首轮关闭；发现非有限即停止 | 避免联合范数裁剪产生额外专家间耦合；改动须预先修订 |
| 批量 | 原四组 32 窗；单组各 16 窗，每窗 512 目标 | 每步单组的本组窗口与共享相同；总有效批量不同须明确限定比较 |
| 日程 | 前 32 次更新线性 warmup，之后恒定；等价于每组前 262,144 暴露词元 | 本组暴露量与更新序列匹配；原四组对应总 524,288 词元 |
| 预算 | 原四组各 16,777,216；单组各 8,388,608 有效目标 | 均为 1,024 次更新；每组训练窗口各用一遍 |
| 精度 | 基座按合格原实现的 BF16；A/B 与 Adam 状态 FP32 | 精确混合精度路径由小测冻结 |
| 量化 | 不引入额外量化 | 避免量化成为另一个变化量 |

这里的动量状态在不同专家间独立是“更新隔离”的一部分。所得效应同时包括参数共享和优化器统计共享的变化。单组与共享比较还改变总有效批量与损失归一化；它优先回答同组暴露量下的曲线差，不能冒称严格只操纵了 B 梯度。

所有专家每个全局更新都获得等量有效目标并进行一次更新。未选中样本不产生该专家的梯度；本轮不应出现整步完全无样本的专家。

若小测表明学习率无法给出有限、基本可学习的过程，先修订所有条件的统一设置；不得看过确认结果后只调某个条件。若确需后续独立调参，只能在单独开发预算中为各条件给相同搜索额度，另立修订后的确认运行。

## 9. Conditions, Seeds, And Checkpoints

正式候选矩阵：A-only/B-only/S8/S16/D8/R8 × 配对种子 {17,29,43}，共 18 条轨迹。先完成六条单组轨迹的开发集资格读数，再决定是否启动其余 12 条；单组轨迹仍是正式对照，不从短程探测检查点续训。三个种子用于增量初始化与训练顺序；同种子六条件的本组窗口顺序配对。固定混合分组清单在三个种子中不变，因此不声称对所有随机分组泛化。

共同更新网格为 0、16、32、…、1024 次。原四组每次更新共 32 窗、16,384 有效词元，终点 16,777,216；A-only/B-only 每次更新各 16 窗、8,192 本组有效词元，终点各 8,388,608。每 16 次更新评估与保存，即共享总词元每 262,144、本组每 131,072；单组曲线与共享曲线按本组 131,072 的网格对齐。所有曲线另如实记录实际总有效词元，不把两种坐标混称同一批量。

局部诊断主状态固定为 **S16 在新增 1,048,576 词元处**。诊断对象与固定总预算的主共享对照相同，不用 S8 的冲突替代 S16 的机制证据。这是预先选定的早期非零适配状态，不根据冲突或最好曲线选择。0 词元只做初始化和退化等价测试，避免双线性 LoRA 零 B 初期梯度结构被误读为一般机制。

预训练来源永久记录为 21,000,000,000；每条训练曲线记录实际新增有效词元，跨单组与共享比较使用本组暴露量。六条件完成后才用各自终点检查点解封 CONFIRM；不因 DEV 曲线漂亮而选择中途最优检查点。

## 10. Primary Metric And Frozen Analysis Plan

### 10.1 同本组暴露量的共享拖累，随后判隔离收益

**第一读数（H1a）：**对每个领域 \(d\in\{A,B\}\)，令 \(O_d\) 为仅训练该组的秩 16 轨迹，\(n=8,388,608\) 为该组终点暴露量。比较同一确认文档上的

\[I_{d,s}=L_{S16,s,d}(N=2n)-L_{O_d,s,d}(n).\]

两条轨迹同为 1,024 次更新，使用相同种子的该组训练窗口次序、同秩、同学习率点和同确认文本；正值表示这组在本次单组对照下共享学习损失更高。A-only/B-only 的训练目标只按本组有效词元平均，故全局批量为共享的一半；这一读数是有边界的共享拖累比较，不能单独证明另一组梯度直接造成伤害。

**AI 提案门槛：**逐领域按确认文档／近重复簇与三个固定种子配对重采样 2,000 次。为保护 A/B 两次方向判断，各用双侧 97.5% 区间；若至少一组 \(I_d\) 的下界大于 0.01 nats/token 且该组三个种子方向均正，H1a 对该组支持；两组上界均不超过 0.01 则未支持预设大小的拖累；其它为不足。两组结果必须全报，不按优势领域事后选主要领域。

**第二读数（H1b）：**原四组仍在相同总训练进度比较隔离收益。只有第一读数指向的受拖累领域也在 D8 相对 S16 的确认读数上改善，才称本配置下“隔离缓解共享拖累”；若只有总体均值改善，则只称隔离的平均收益。

对领域 d 的所有确认位置累计损失和与有效词元数，求 \(L_{c,s,d}(N_{max})\)。条件 c、种子 s 的总体指标是 \(\bar L_{c,s}=\frac12(L_{c,s,A}+L_{c,s,B})\)。

原四组的固定总参数预算效应：

\[\Delta_s=\bar L_{S16,s}-\bar L_{D8,s},\qquad \Delta=\tfrac13\sum_s\Delta_s.\]

主要统计单位为原始文档/近重复簇，不把一个文档的词元或窗口当作独立样本。全条件按相同记录配对；在每个领域内按簇重采样 2,000 次，每次保留三个既定训练种子，重新算词元加权领域损失，再取领域与种子平均。报告双侧 95% 百分位区间；分析 RNG 固定 20260924。

该区间只描述**这三个固定训练种子条件下的确认文档抽样不确定性**；三个种子不支撑精确的训练种子总体结论。单独列出三个种子的方向。

**AI 提案门槛：**实际关注差异 \(\delta_L=0.01\) nats/token。S16−D8 区间下界大于 0.01 且三个种子点值都大于零，标隔离主比较支持；区间上界不超过 0.01，标未支持预设大小的收益；其余标不足。不得把“未支持”写成“严格证明没有任何小效应”。

同时报告两个领域分别的差值；若一方明确退步，必须说明这是平均意义的收益，而不是双方都更好。

**缺失与选择规则：**以全部已冻结确认簇和全部三个种子计算，不剔除困难文档、异常但有限的损失或方向不一致的种子。所需条件／种子失败时，对应 H1a 或 H1b 记 INCOMPLETE，不以成功子集给支持判断；恢复同一身份可继续，替换种子须新登记。只有预先登记的数据质量排除规则可在解封前应用。分析脚本版本和哈希必须在 CONFIRM 解封前登记；确认集身份及访问日志同时封存。单组 DEV 已参与资格判断，不能代替独立确认。

### 10.2 同学习质量：计算词元效率倍数

“相同训练进度”和“达到相同质量”不是同一个问题。损失差不直接换算倍数。

预先用未适配基座在 DEV 测得每域 \(L_{0,d}\)，固定目标 \(\tau_d=L_{0,d}-0.05\) nats/token（0.05 为待确认提案）。各领域可以有不同阈值；但同一领域的阈值对所有条件相同。阈值不得看完训练曲线后挑选。

对每个条件，\(T_c\) 定义为在共同评估网格上，首次**两个领域都达标并在下一次评估仍达标**的首个 N。不得为达标而选择未来最优检查点，最后一个网格点没有后继复核时不算稳定达标。

固定预算主对照的词元倍率为：

\[S_{tokens}=T_{S16}/T_{D8}.\]

1.5 倍意味着达到该固定质量目标，D8 约只需 S16 的 2/3 新增词元。它不是墙钟训练速度；也不能除两条 loss 数值计算。

若只有 D8 达标，报告 S16 的达标时间在预算内未观察到及可给出的下界，不伪造有限倍数；两者都未达标则倍率 `UNDEFINED`，保留预算末端主指标。若仅 S16 达标，明确隔离未显示目标质量优势。

可另列 S8/D8、R8/D8 倍率，但注明各自预算含义。倍率基于固定 DEV 面板，不与 CONFIRM 主效果混称独立确认。图上保留原始网格和达标范围，不通过任意平滑制造精确交点。

### 10.3 系统效率单独测

报告实际训练 GPU 秒、训练吞吐和达到目标所需训练墙钟；另列数据准备、SAE 特征导出、验证、诊断与排队开销。各条件使用相同测时边界、硬件和 batch；若融合共享权重但专家不融合，或只给一组预缓存，则墙钟不可作干净速度对照。

本轮不事先承诺任何加速倍数。

## 11. Secondary Metrics And Guards

### 11.1 分组对照与预算对照

固定顺序检验：先看主比较 S16−D8，再看 R8−D8。后者采用同样文档配对区间，区间下界大于 0 且三个种子方向一致，才说“按域分组优于本次等负载混合分组”。按预设顺序报告，不从多个对照中选显著的一项替代主比较。

S8−D8 仅作每样本活跃秩相同的参照：若只胜 S8、不胜 S16，不能宣布固定总参数预算下隔离更好。若 D8≈R8，两专家结构的收益不能归因为按域分开。

### 11.2 局部互损：同一状态、虚拟更新、全部回滚

在每个种子的 S16 预设状态，复制 LoRA 的 A/B 矩阵、Adam 一二阶矩、步数、学习率与随机状态。正式训练暂停在该状态但不得被诊断改写。

DIAG_UPDATE 每域 512 窗分成 32 组，每组 16 窗；每窗来自不同文档/近重复簇。来源批量与正式每步该领域的 16 窗一致。对每一组，均从同一原状态独立产生以下虚拟分支：

- 只用 A 的平均损失梯度；为对应正式混合目标中的贡献，乘 1/2。
- 只用 B 的平均损失梯度，同样乘 1/2。
- 新梯度显式设为零，但保留原 Adam 动量及步数推进规则的对照。

以上分支均明确实例化全部 LoRA 梯度张量，保证零新梯度对照推进同一组状态；每个分支只执行一次与正式训练相同的 AdamW 更新；分别在所有独立 DIAG_READOUT A/B 文档上计算更新前后逐文档损失。不是把“零梯度”设为 `None` 跳过优化器，也不是沿 32 次诊断连续训练。

记录：

\[H_{A\to B}=L_B(\phi+u_A)-L_B(\phi),\qquad
H^{new}_{A\to B}=L_B(\phi+u_A)-L_B(\phi+u_0).\]

\(u_0\) 是无新梯度但有历史动量的更新。前者问 B 实际是否变差；后者问新 A 梯度相对动量对照是否更不利。若后者为正而前者不为正，只能叫相对进展减弱，不能叫 B 损失上升。

同步检查 \(H_{A\to A}\)：只有独立 A 读出确实改善，才将这次结果解释为“对 A 有效、对 B 有害”的更新。报告所有分支，不按是否伤害 B 筛选后再统计。

同域来源/独立同域读出就是同域噪声参照；另外以原学习率的 1/2 重做同一组分支，检查伤害是否对这次步长缩减敏感。不得据半步结果重新调正式运行曲线。

独立性与不确定性：以诊断来源小组和目标文档簇两层重采样 2,000 次（分析 RNG 固定 20260924），保留配对关系及三个既定种子；A→B、B→A 两个方向使用 97.5% 双侧区间以保护双方向检验。32 组不是 32 条独立训练轨迹，不将其冒充训练种子。

候选局部支持规则：在 A→B、B→A 中至少一个预定方向，完整步长下实际跨域损害及相对无新梯度分支的增量损害，其 97.5% 区间下界均为正；同一方向的源域独立读出损失变化区间上界小于零。半步长下须仍满足这三条方向判据，才称该步长范围内存在“源域改善、目标域受损”。全部来源小组均纳入统计，不先筛掉同域未改善的组。未满足时只按对应读数报告，机制保持不足；半步长检查不能排除所有优化器或曲率解释。

即使通过，这也只支持该预设状态附近的更新互损。R8/D8/S16 的长期差距并未被完整做因果中介识别。

### 11.3 梯度只作解释辅助

可以在同一个 S16 参数化、同一状态上记录 A/B 梯度内积、范数及夹角。禁止比较独立专家的 A/B 因子距离后声称它们学了不同机制，因为低秩因子有等价重参数化。

梯度余弦为负不是充分结果；Adam 的实际更新也不等于原始负梯度。判局部伤害以实际可回滚的损失变化为准。

### 11.4 SAE 保存什么、不能声称什么

在未适配起点，对固定 DIAG 面板保存输入哈希、词元位置、原生 \(a\) 的记录级汇聚、SAE Top-32 的索引/系数，以及必要的重构误差。实际编码必须调用冻结检查点原实现，不重训字典或另加归一化。

SAE 的激活对同输入在本轮应保持不变。此时可以将固定特征与未来诊断标签对齐，但**不能把“两个领域的激活不同”作为本轮预测干扰成功**。真正的预测检验要另分拟合/开发/确认数据，并与原生表示、领域标签等基线比较；只有两个领域的一次组间差异不够证明普遍预测规律。

## 12. Known Good / Known Bad / Known Confusing Cases

- **已知应当相同的工程情形：**全零增量时全部条件与同一基座输出相同；绑定专家时与 S8 的前向、梯度、一次更新相同。此处“相同”指登记容差内，不是经验期待。
- **已知会失效的实现：**A 与 B 全零而无梯度；误更新 SAE 缓冲；每专家局部均值导致损失翻倍；多个专家更新同一参数对象两次；在 LoRA 后使用 `no_grad`。
- **合成方向单元测试：**标量损失 \(L_A=(w-1)^2/2,L_B=(w+1)^2/2\) 在 \(w=0\)，向 A 的小步更新应减 A、增 B。它只检验损失差正负号和回滚实现，不能作为真实语义冲突证据。再令两损失相同，更新不应被判为方向性互损。
- **容易误读的科学结果：**S8 落后而 S16 追平；D8 与 R8 同样好；只有平均损失改善；有局部负梯度但实际损失不升；四个适配器都不改善。每种情况按 §15 限定结论。

## 13. Scientific Procedure And Stage Contracts

### 阶段 A：身份与数据预检

**输入：**用户确认的模型目录、原模型实现、数据候选。**操作：**检查文件哈希/谱系、源码读点和下投影形状；建立文档级数据划分、路由清单与词元清单。**为什么：**这些决定本轮是不是同一模型、同一数据以及同一干预点。

**输出：**`source_audit.json`、`checkpoint_manifest.json`、`data_manifest.json`、`route_manifest.jsonl`、人工审核记录。任何不明文档边界、错误模型谱系或目标模块不匹配均 `BLOCKED`，不进入训练。

### 阶段 B：工程小测，不能据此宣称机制

**输入：**确定性合成小批、六条件及绑定专家测试模块。**操作：**先 FP32 CPU/小张量等价检查，再按研究者最新选择在四卡 H100 Reserved 上六条件各 8 次更新；第 4 次保存、第 5 次独立进程恢复并对照连续执行。此前四卡 5090 Spot 任务已停止，不作为本轮通过证据。A-only/B-only 使用同一配对批中的本组子序列，每步 8,192 有效目标；其余四组每步 16,384。合成词元只验证工程，不能回答数据可学性。

**通过标准：**FP32 相对容差 1e-5、绝对容差 1e-6；BF16 基座初始输出/损失对照使用相同内核，损失绝对差不超过 1e-4，若不达标需查明后再冻结容差而非掩盖误差。冻结参数和 SAE 缓冲逐项无变化；固定 \(a,z,u\) 不随训练改变；适配器参数数目正确；全局词元数和损失重算一致；恢复坐标和下一更新可复现；所有必需日志有限。

**输出：**执行根下的 `start_checks.json`、`resume_checks.json`、`smoke_verification.json`，各条件的 `step4.pt`、`shadow_step5.json` 与 TensorBoard；本地小张量等价结果另记。目标机器应另记实测吞吐/显存。任一失败停止。小测不自动授权正式矩阵。

### 阶段 B1：A-only/B-only 正式曲线与可学性资格

**目标与原因：**让每个领域都有完整的单独学习正式曲线；其开发集末端改善先检验“这套冻结模型＋增量是否仍能学”，独立确认集在六条件结束后用于 H1a 对照。不以共享劣势作为入选条件。

**输入：**A、B 各自完整 TRAIN 与固定 DEV；从零增量开始的同一冻结基座；通过工程小测的秩 16 单适配器。CONFIRM 与 DIAG 两区保持封存。所有未确认数值均 AI_PROPOSAL。

**操作：**A-only/B-only 各按正式种子 {17,29,43} 运行，共六条完整轨迹；每条使用本组 16,384 个互异训练窗口、8,388,608 有效目标、1,024 次更新。每步取与共享条件同种子同位置的 16 窗、8,192 本组目标；训练损失按这 8,192 个目标平均。学习率随同一 32 更新 warmup 进度，之后恒定；每 131,072 本组目标评估 DEV 并保存小型增量检查点，含 0 与终点。它们不从 Smoke 或短程资格探测续训，而是正式对照曲线。

**读数与通过规则：**对每域计算未适配基座减该域正式单组曲线的 DEV 损失 \(G_d\)（nats/token）。在本组暴露量 8,257,536 与 8,388,608 两个预定末端网格点，按 DEV 文档／近重复簇配对重采样 2,000 次、保留三个固定正式种子、RNG=20260924，给双侧 95% 区间。两个域在两点的区间下界都 >0.02，且每个种子在各自两点均改善，才记 `HEADROOM_PASS`。此门不使用 S16/D8/R8 结果，亦不证明 H1a 或充分统计功效。

**失败与不足：**若任一域任一终点区间上界 ≤0.02，记 `NO_QUALIFYING_GAIN`；其它未通过情况记 `HEADROOM_UNCERTAIN`。两种情况均暂停其余四条件；单组轨迹保留为已执行证据，CONFIRM 仍封存。若训练集改善而 DEV 不改善，记泛化资格未过；训练集也不改善则先查梯度路径、冻结范围和优化。即使工程正确，也只能说“当前数据×位置×秩 16×预算未显出足够空间”，不能断言模型已经学完。禁止自动加秩、换位置、延长预算或换数据追逐通过。

**输出与交接：**`runs/A_ONLY/<seed>`、`runs/B_ONLY/<seed>` 保存完整曲线、终点增量与 TensorBoard；`qualification/headroom.csv` 与 `qualification/decision.json` 仅记录 DEV 资格结论。两域均过门且其余四条件的范围已获授权，才交阶段 C。单组终点在阶段 D 参加 H1a 正式确认比较，但不把其实际总词元与 S16 的总词元直接比较。

### 阶段 C：正式配对适配与局部诊断

**输入：**工程小测与 B1 两域可学性均通过的代码、数据和冻结配置，并具备剩余正式范围授权。**操作：**原四条件×三种子运行固定新增预算；预设节点做 DEV 和适配器保存；在 S16 的预设节点执行全部回滚诊断。非有限梯度/损失或数据游标不匹配时保留故障并停止该比较，不自动替换种子或换模型。

**输出：**完整原始曲线、适配器/优化器检查点、逐文档诊断损失、参数/特征冻结检查。诊断分支不得影响主训练哈希。结束不意味着得到正结果。

### 阶段 D：一次确认与结论分型

**输入：**六条件全部终点适配器、冻结分析脚本、未解封 CONFIRM。**操作：**先按本组暴露量计算单组与共享差，再计算原四条件的隔离与分组效应，另列局部互损；按 §15 分型。**为什么：**避免先看结果再改问题和阈值。

**输出：**`summary_cn.md` 的目的/假设/方法/结论，`detailed.md` 完整证据和偏差；这些是将来执行后的文件，本轮不会预先生成虚假结果。研究者裁定后才能更新 Anchor 的证据与下一决策。

## 14. Algorithm, Output, And Provenance Contract

### 14.1 应复用、改写和拒绝的部分

本次已读本地训练复用索引、干净框架的 source audit/README、0912 复用清单、0916 原生旁路模型实现与旧八来源 data.py/config.py；这些路径当前可见。源码阅读不是适配实现验收。

**复用候选：**原生旁路模型结构／同谱系加载、分词器身份、全局有效词元计数、原子化恢复与 TensorBoard；上述模型入口已读，其余组件需在实现前按实际源码快照逐项验证。旧后训练的文本渲染／答案掩码可适配，不直接加载旧已分词张量或标签分区。

**必须适配：**只训练末层下投影增量的包装器；固定分组分发；按各条件实际有效目标数作全局 loss reduction；文档级采样；虚拟更新回滚；确认统计。原四条件的分母相同，A-only/B-only 各使用本组一半大小的分母。

**明确不沿用：**旧 0912 将 SAE 串联进入主路径的架构、旧预训练优化器状态、旧默认重构/AuxK 目标、旧“所有 Linear 都挂 LoRA”的配置、过期提交命令以及旧面板结果作为本轮证据。

六条件工程 Smoke 代码已建立，目标四卡验收结果待写回；正式数据流水线、回滚诊断及训练矩阵尚未实现或验收。本文件不提供假称可执行的正式训练命令。

### 14.2 观测契约

每个 run 单独写 `run_root`，仅指定日志进程写全局聚合量。必需：

```text
tokens/train_lm_loss
tokens/train_total_loss
updates/train_lm_loss
updates/learning_rate
progress/tokens_seen
progress/optimizer_step
progress/effective_tokens_per_update
```

前两个在本轮应相同，因为只有语言目标。另记录 `tokens/dev_lm_loss_A`、`tokens/dev_lm_loss_B`、`tokens/dev_lm_loss_macro`、每域累计目标数、每专家累计目标数、梯度/更新范数、trainable parameter count、吞吐和显存。A-only/B-only 的另一领域计数保持零。未启用的 SAE 损失登记为 `NOT_APPLICABLE`，不伪造零重构曲线。Smoke 只验证前述必需标量及实际每步词元计数，不伪造未构建数据集的 DEV 曲线。

词元计数在一个完整梯度累积窗口完成后推进。本轮禁用自动跳过非有限更新：出现则中止并保留故障，因此不产生“处理过但更新被跳过”的模糊坐标。恢复必须恢复有效词元、优化器步、数据游标及随机状态。

### 14.3 文件和数据结构

运行前建立唯一执行根 `EXEC_ROOT`；准确绝对路径由执行环境确认后写入，不覆盖任何已有 run。建议结构如下，不代表这些运行文件现在存在：

```text
EXEC_ROOT/
  manifests/                  # 模型、代码、分词器、数据、路由、协议注册哈希
  data/                       # 清单或链接；原始语料不入研究仓库
  runs/<condition>/<seed>/
    frozen_config.json
    metrics.jsonl
    tensorboard/
    checkpoints/              # 只存 LoRA/优化器/游标；引用不可变基座
    checks/
  qualification/              # 正式单组曲线的 DEV 可学性判定与词元账本
  diagnostics/<seed>/         # source/target、前后损失、动量/半步分支、回滚哈希
  analysis/
    primary_effect.csv
    per_domain_effects.csv
    token_efficiency.csv
    local_interference.csv
    eligibility.json
    figures/
```

训练原始记录至少含 `condition, seed, pretrained_tokens, added_valid_tokens, optimizer_step, tokens_A, tokens_B, expert0_tokens, expert1_tokens, loss_sum, target_count, lm_loss, lr`。

诊断记录至少含 `seed, checkpoint_tokens, source_group, source_batch_id, target_doc_id, branch, step_scale, loss_before, loss_after, loss_after_zero_gradient, target_count, rollback_pass`。

每个主要值追踪：原始损失/目标数 → 文档级聚合 → 域内词元平均 → 两域等权 → 三固定种子 → 配对区间 → 注册判据。不得只保留图片。

### 14.4 资源与提交边界

实际资源选择和提交入口只引用 System 的 `docs/execution_envelope.md`，不从旧 Protocol 复制镜像 URL 或直接提交命令。研究者先指定四卡 5090 Spot 工程 Smoke，随后明确要求停止 `pt-xmk3zndq` 并重提四卡 H100 Reserved；当前 Smoke 选择 `h100-4-reserved`。正式数据资格及矩阵没有随之获授权。提交前已用当时有效的 envelope、资源和镜像键核验。

以四数据并行进程为候选执行形态时，每卡微批量 2 窗、累积 4 次可保持全局 32 窗。换卡数须调整微批量/累积，不得改全局有效批量。专家均在每个副本内本地保存，不引入专家并行通信变量。

时间和显存上限待小测实测后、正式授权前冻结。工程 Smoke 六组各 8 步：原四组共 524,288、单组两组共 131,072，合计 655,360 个合成有效目标。拟议正式矩阵中，原四组×三种子共 201,326,592，单组两组×三种子共 50,331,648，合计 251,658,240 个真实有效目标，另计评估和诊断。Smoke 预算上限设为 30 分钟墙钟；触限停止并保存已有证据，不把未完成判为通过。正式训练的 GPU 小时上限由吞吐测量后确认，未冻结上限前不得启动对应阶段。本轮不声称已知耗时或可提升倍数。

### 14.5 来源及核验程度

- System `Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/supporting_records/sae_pretraining/sidecar_8l/20260916/protocol.md` §1–3：已读原生末层 SAE 读点与历史尺寸。
- 本次直接读取从零 \(\lambda_{rec}=0.1\) 的 S7 `token_021000000000/manifest.json`，重算 `state.pt` SHA-256 与清单一致，并在本地 GPU 加载做一次真实冻结主干 LoRA 更新；四卡目标环境仍待本轮 Smoke 核验。
- System `docs/training_reuse_index.md` 与 `docs/training_observability_contract.md`：已读复用和有效词元契约。旧串联架构不属于本轮。
- System `docs/execution_envelope.md` §1–2：已读资源选择与授权边界；本轮仅四卡 5090 Spot 工程 Smoke 获研究者授权。
- [LoRA 原论文](https://arxiv.org/abs/2106.09685)及[官方 Linear 实现](https://github.com/microsoft/LoRA/blob/main/loralib/layers.py)：低秩参数化、零初始增量。本文矩阵计数与绑定等价为按该参数化自行推导。
- [任务分组论文](https://arxiv.org/abs/2109.04617)：更新影响另一任务损失的诊断思路。本轮回滚 Adam 与对照是本设计提案，不是该论文结论。
- 本轮局部证据以实际损失变化定义，不把原始梯度夹角替代 Adam 更新或长期机制。
- [M2D2 官方论文](https://aclanthology.org/2022.emnlp-main.63/)及[数据卡](https://huggingface.co/datasets/machelreid/m2d2)：候选来源与配置名；原始文件版本、文档边界和可用库存未核验。

## 15. Success / Failure / Insufficient Evidence

分开报告三个结论层，不给一个混合“PASS”掩盖不同证据。

| 结果组合 | 允许的判断 | 本轮决策 |
|---|---|---|
| A-only/B-only 可学；S16 在同本组暴露量下落后；D8 在受拖累组改善且胜 R8；局部互损通过 | 本配置下分别支持共享拖累、隔离缓解和预设状态局部互损；三者之间的长期因果中介仍未识别 | 可由研究者决定是否设计 SAE 预测检验 |
| 单组可学，但 S16 未达到预设大小的共享拖累 | 未建立 H1a；即使 D8 较好，也只能独立报告隔离收益 | 不把隔离收益反写成共享拖累 |
| S16 落后单组，而 D8 未改善受拖累组 | 共享拖累有证据，当前按领域隔离未解除 | 检查秩分配与优化，保留 H1a 结论边界 |
| 共享拖累与隔离缓解成立，局部互损未支持 | 曲线及隔离读数成立，当前回滚未证实局部机制 | 不把长期差距归因为已测局部更新 |
| D8 仅胜 S8，不胜 S16 | 未建立同总参数预算优势 | 不能把多参数收益讲成固定预算机制胜利 |
| D8 胜 S16，但不胜 R8 | 条件分配结构可能有益，按领域隔离的特殊价值未确立 | 不推进“按语义冲突分发”的结论 |
| D8 有收益，局部互损未支持 | 有分配收益，当前互损解释未建立 | 优先改机制判断，不用 SAE 类别图补足 |
| 有局部互损，但 D8 无稳定收益 | 局部伤害不保证整体隔离值得 | 不宣称该信号已适合路由 |
| A-only/B-only 正式曲线未过开发集可学性门，或读点/数据/恢复检查失败 | 实验资格不足，其余四条件不启动 | 区分数据、泛化、插层／秩和优化，不直接断言“21B 已学会” |
| 单组开发集过门，但共享和隔离条件没有可靠改善 | 混学或隔离条件的优化资格仍不足 | 核查批量和归一化差异，不把单组过门当作无条件保障 |
| 区间跨判据或目标损失未达到 | 对相应效应/倍率证据不足 | 报告未知或截尾，不选择最有利曲线 |

显式停止规则：冻结主干参数或 SAE 参数／缓冲被修改、绑定等价失败、训练计数或数据顺序不匹配、非有限损失/梯度、确认集泄漏、代码在不同条件中未经登记改变，均中止受影响比较并保存故障。不得自动切换秩、位置、模型或数据后沿用原预注册资格。

## 16. What This Cannot Claim

不能证明“数学和生物本质上不兼容”、容量问题已排除、所有负梯度都有害、无限参数下干扰仍存在、SAE 训练塑造了有用路由结构、SAE 已能自动识别应隔离数据、专家数最优或端到端 MoE 预训练优势。

主干与 SAE 在本轮不变，因此本轮不能识别 SAE 正则的训练因果效应。最后下投影的正/负结果也不能代表其它层、其它秩或全参数训练。

“达到同一验证质量的词元倍数”“相同词元的损失差”“GPU 墙钟速度”分别报告，不能互相替代。静态 \(z\) 可读不等于预测冲突，预测冲突也不等于已能带来路由收益。

## 17. Block Confirmation, Freeze, And Amendment Ledger

| 区块 | 当前状态 | 确认/阻塞内容 |
|---|---|---|
| A 问题与边界 | PROPOSED；原稿方向保留 | 单组可学性门；H1a/H1b 分别判断；稳定问题与 Focus 待确认 |
| B 数据 | PROPOSED / BLOCKED | M2D2 首选／同格式后训练备选；需清单、边界、库存与学习资格 |
| C 任务 | PROPOSED | 下一词元学习，外部分组只给分配器 |
| D 结构 | 研究者选定谱系；工程验收进行中 | 从零 \(\lambda_{rec}=0.1\) S7，SHA-256、源码、权重及本地一步已核；四卡 Smoke 待核 |
| E 目标与优化 | PROPOSED | 语言目标、统一 AdamW、有效批量和词元日程 |
| F 对照与分析 | 六条件结构由研究者明确；阈值仍 PROPOSED | S8/S16/D8/R8 加秩 16 A-only/B-only、按本组词元对齐；回滚、阈值及统计规则待确认 |
| G 执行 | H100 工程 Smoke 已审计 PASS；正式 BLOCKED | 5090 `pt-xmk3zndq` 依研究者要求停止；H100 `pt-8pr2e57p` 六组通过；正式归属、数据、范围及资源上限仍待确认 |

本轮完成可审阅候选的修订；研究者已授权基础工程 Smoke，并指定模型谱系和两条单组秩 16 对照。没有把其余未确认数值提升为已批准设计。正式矩阵范围仍需单独确认。

首次执行批准时冻结科学正文与配置，记录时间和哈希。此后改变数据、秩、位置、目标、预算、指标、排除规则或判定阈值，必须追加变更记录，包含前后值、原因、是否已见结果和证据资格；不得覆盖原约定。

**当前下一决策：**完成并审阅基础工程 Smoke，然后确认数据路线、正式六条件阈值及执行范围。单组正式曲线的 DEV 资格未过时不启动其余四条件。H2 的 SAE 预测任务另行设计。

2026-09-24 预执行修订记录：将 A-only/B-only 从短程资格检查升为秩 16 正式曲线，以本组词元暴露量与 S16 配对；原四条件和回滚保留；研究者选择从零 \(\lambda_{rec}=0.1\) S7。无本轮训练结果被用于改阈值。正式 A–G 尚未确认，故未执行冻结；仅工程 Smoke 范围获授权，未来科学执行仍遵守追加变更规则。

2026-09-24 Smoke 资源变更记录：原 `5090-4-spot` 任务 `pt-xmk3zndq` 在完成运行时与单机 GPU 预检后按研究者最新指令停止，平台终态 `SUSPENDED`、零 worker；改由 `h100-4-reserved` 任务 `pt-8pr2e57p` 在新运行目录执行同样六条件、同批量和同判据的基础工程 Smoke。没有复用原任务的部分结果为通过证据，也未改变正式科学设计。

2026-09-24 工程结果记录：`pt-8pr2e57p` 的持久化日志及执行根 `smoke_verification.json` 记录六条件各 8 步、必需 TensorBoard 标量、独立进程恢复第 5 步状态与词元坐标全部通过；审计脚本在执行容器外对共享产物复核为 PASS。合成数据不检验真实数据可学性或 H1a/H1b/H1c，后续并行正式训练仍须完成数据与科学契约冻结。

## 18. 2026-09-24 Explicit Execution Amendment

**Execution scope approved by the researcher in this conversation:** submit all six arms for all three fixed seeds now, using at most one four-card H100 Reserved job and additional four-card RTX 5090 Spot jobs. The earlier B1→C launch gate in §§9 and 13 is superseded **for scheduling only**: single-arm headroom remains the first scientific analysis gate, but the four shared/isolation arms are allowed to train concurrently before that result is known. If headroom later fails, those already submitted arms remain engineering/exploratory material and must not be presented as confirmatory H1 evidence. This is an explicit researcher choice to trade possible unused compute for calendar time. Do not resubmit an existing job on a delayed platform state alone.

The researcher selected the exact official M2D2 Mathematics and Biology configurations and accepted reconstructed article boundaries from two or more consecutive blank lines. A manual sample of 20 selected records per configuration and original train/valid/test split found many off-topic articles, especially in the Mathematics configuration and Biology valid split. The researcher explicitly chose to continue with **configuration-defined text distributions**. Hence A and B are source configurations, not pure mathematical and biological semantic domains; H1 may describe these two distributions only. This supersedes all earlier wording that assumes content-pure mathematics versus biology. No data was selected by observing gradients or final learning effects.

Official M2D2 revision is `6ae613ba744ee56f645aee9c577d04f7e3d48b30`. The frozen derived view is `/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/data_v1/data_manifest.json` (SHA-256 `9b62a1ee3c424e00a30387d08bba7c6b536ab2fb11fc1eff5545be210fa3e1f9`). Its separate audit is `data_audit.json` (SHA-256 `c69b42244a17f5ec7cac1fd6a4bee5dbb5f81a8903caebfbd8da9f5bfdf25425`). It includes 16,859 selected derived documents and 102 candidate near-duplicate pairs; exact word-5-gram Jaccard checks found none at or above 0.8. MinHash candidate retrieval is probabilistic, so this does not certify absence of missed near duplicates. The Mathematics CONFIRM view has 512 windows from 457 unique derived articles; 55 second windows are a declared exception to the 512-distinct-document preference. All preassigned windows and splits are frozen before model training. The original Wikipedia page IDs are unavailable.

Three jobs, not 18 simultaneous allocations, implement the 18 trajectories. Seed 17 runs six arms sequentially on the sole `h100-4-reserved` allocation; seeds 29 and 43 each run six arms sequentially on an independent `5090-4-spot` allocation. This keeps all six conditions of a given seed on one accelerator type and lets the three seeds run in parallel. Profiles and default image resolve only through `docs/execution_envelope.md`; every job first runs the target four-GPU preflight and real-data trainer qualification, then the fixed full schedule. The H100 six-arm synthetic Smoke passed; the 5090 target did not previously pass this six-arm training Smoke, so each submitted 5090 job must fail closed before formal training if its embedded qualification fails. No resource fallback is authorized.

The training entry is `/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/scripts/run_formal_4gpu.sh`; the trainer is `train_formal.py`. The actual layout is `<job run root>/formal/seed<seed>_<condition>/`, with one TensorBoard directory, `metrics.jsonl`, `progress.jsonl`, `latest.pt`, and `checkpoints/step_XXXX.pt` per arm. This replaces the illustrative layout in §14.3. Required domain validation tags are `tokens/dev_lm_loss_A`, `tokens/dev_lm_loss_B`, and `tokens/dev_lm_loss_macro`, in addition to §14.2's fixed training tags. For R8 DEV readout, route is the parity of the stable window index within each configuration. All four shared arms use 16,384 targets/update; the two single arms use 8,192. The chosen profile changes device type across seeds, so seed variation and device-specific numerics are confounded; within-seed comparisons stay on matched devices.

This amendment authorizes **training submission**, not a positive scientific verdict. Numerical interpretation cutoffs in §§10 and 13 remain labeled `AI_PROPOSAL`; they must be accepted or revised without looking at CONFIRM before a registered confirmatory verdict. CONFIRM stays sealed until the selected analysis code, thresholds, and all required trajectories are complete. The rollback diagnostic stays in scope and must be run from the preserved S16 step-64 checkpoint without modifying the formal trajectory. Job creation receipts, worker logs and durable run files own execution status; a platform state field alone does not.

2026-09-24 启动后的产物偏差记录：当前 `RoutedDown.state_dict()` 同时包含冻结的下投影基座权重，因此每个 `latest.pt` 和里程碑文件除了 LoRA 参数、Adam 状态、坐标外，还重复保存约 6 MiB 冻结权重。主干没有进入优化器，六条件工程和真实数据资格检查均检查其不变性；该偏差增加存储而不改变训练目标、输入、可训练参数或对照定义。此轮已运行代码不热修改，后续结果账本保留这项偏差；不能把这些文件误称为纯 LoRA 权重。
