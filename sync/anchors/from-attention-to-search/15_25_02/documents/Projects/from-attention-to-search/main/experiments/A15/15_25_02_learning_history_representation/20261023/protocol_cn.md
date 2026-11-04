派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/protocol_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_25_02_learning_history_representation/20261023/protocol_cn.md)；研究修改仍回到原件。

---

# A15_25_02_E01 Protocol：学习经历与任务重要方向

**研究问题：学习经历如何改变条件规则的表征，以及哪些方向对任务作答最重要？**

v1 于 2026-10-23、提取之前冻结。研究者在确认四状态分析路径后，授权完成 Anchor、Protocol、全部分析及解释，普通实现和对照选择由 AI 执行。范围为冻结推理及表征修改，不包括模型或字典训练、新数据采集、读取 TEST、发布或问题关闭。

## 目的与精确比较

[Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_25_joint_feature_graph/subanchors/15_25_02_learning_history_representation_anchor_cn.md) 检验能否把任务相关变化与一般位移区分开。比较 Base、学会 A、A 后只学 B（sequential）、A 后混合学 A+B（mixed）。可见模式决定甲/乙选择首/末词还是反过来。同输入、架构、未变参数、输出头和张量接口均配对。两端点 B 暴露为 24k 对 12k，因此不能归因于学习顺序本身，也不代表从 Base 开始混合学习。

## 输入与身份

执行归属：`/data/250010109/MoE_Router/experiments/20261023_learning_history_representation`。精确配置为 `config/frozen.json`，样本清单为 `data/examples.jsonl`。推理只读取已有 DEV 的 old/reversed 三词列表，不读取 TEST。检查原数据 manifest 和 train/dev 哈希；TRAIN 元数据只用于确认计数。

| 状态 | 权重来源 | SHA256 |
|---|---|---|
| base | `None` | `exact official Base; cd2a5120...` |
| A | `/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full/attn1_adam/main/checkpoints/update_01200/state.pt` | `48595673c24579164e271cfeb1b86be6a234e2dfc06218b74d8ca07e16411b75` |
| sequential | `/data/250010109/MoE_Router/experiments/20261023_autonomous_retention/runs/A/seed_29/U/checkpoints/update_01200/state.pt` | `e3b12604b7f3f205b7e219a85f0c7826e9453caa6663b024ed4228798e7b82b1` |
| mixed | `/data/250010109/MoE_Router/experiments/20261023_autonomous_retention/runs/B/seed_29/Full/checkpoints/update_01200/state.pt` | `97473f54f80a96a16f5758527f010b6eea2d56c2ba6b7b05a25664865642b963` |

每个适配状态只在官方 Base 上覆盖 `model.layers.27.self_attn.{q,k,v,o}_proj.weight`。模型沿用 A17 的 FP32。固定 CrossCoder 有 16,384 个特征，读取零起算块 1,3,...,27 的残差输出，使用保存的 TRAIN 均值、向量 RMS、推理阈值及 BF16 计算。实际检查两个 Base 路径的 safetensors SHA256 相同。模型计算精度不同于 CrossCoder 原训练环境，会在资格中披露。不产生参数梯度或优化器。

必需资产（当前 strict 访问检查，加实际加载身份检查）：
- `model_qwen3_0p6b_base_official_a5`
- `tokenizer_qwen3_0p6b_base_official_a5`
- `data_a17_conditional_mapping_v1`
- `adapter_a17_04_single_attention_20261011t145214z_full_attn1_adam_main`
- `checkpoint_family_a17_r05_20261023_a_seed_29_u_1d84de189a55`
- `checkpoint_family_a17_r05_20261023_b_seed_29_full_8de66cb62ec4`
- `crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013`
- `model_qwen3_0p6b_base`

## 数据划分与独立单位

1,600 条样本来自 400 个无序词组，每组包含同一有序列表的两个世界和两个口令。`unordered_group_id` 的 SHA256 按整数模二：偶数进入发现集，奇数进入评估集，分别为 784/816 条、196/204 组。同组变体不跨划分。选择不使用评估结果。DEV 已被 A17 使用，因此所有统计都是已暴露 DEV 上的探索证据，不是新确认。

## 阶段一：行为与测量资格

每条记录只取最后一个输入 token、即作答前的位置。保存四状态全部十四层原始残差和共享 CrossCoder 激活。测全词表准确率、首末二选一、正确词负对数似然（nat）、正确词减另一端点词的 logit 间隔，以及首、末、中间、其余词概率。按固定规则展示四个评估列表在全部模式和口令下的答案。

原生前向与残差回放的最大间隔误差须 ≤0.001，且全词表预测一致。同输入此前选定层应逐值相同。零修改和同上下文替换的 logits 须完全一致；完整向量替换须在 0.001 内重现供体 logits。检查有限值、固定阈值及各阶段权重版本不变。只有切换已有状态时允许复制参数，不能称为学习。

各状态/层记录中心化方差解释率、相对平方重建误差、重建前后行为、活跃特征数及样本出现率。较强字典分解资格要求末层中心化方差解释率 ≥0.8，且全词表准确率变化绝对值 ≤0.05。未通过不抹去原生行为或原始几何；保留误差的干预仍可描述特定方向，但不能证明字典覆盖完整机制。

## 阶段二：配对几何与发现选择

报告配对位移相对原向量的范数、余弦、此前层最大差异，以及 mixed 减 sequential 的末层奇异谱。出现率、条件激活强度、共现分别统计。频率描述本轮样本，不表示预训练暴露或语义身份。小热图展示选定特征在各状态/任务中的激活；高频特征只是描述对照。

用冻结输出头求答案间隔对末层残差的精确梯度。候选分数是发现集上 `z_f * scale * dot(decoder_f, gradient)` 正部的均值。按分数降序，特征 ID 打破并列。分别选学会 A 的旧任务、顺序模型的新任务、混合模型的旧任务和新任务各 32 个特征；另保留混合模型出现率最高的 32 个。混合旧/新集合为主要集合。一阶分数只提出候选。

只在发现集对 mixed 减 sequential 的残差差值做 SVD，不去除均值变化。固定秩 1、4、16。评估干预前保存候选 ID、分数、匹配诊断及子空间基。

## 阶段三：有限干预与对照

对每个候选集合、每个模型，将激活削弱 0.5 和 1.0，保留原重建误差：`h_edit = h + scale * (z_edit-z) @ D_last`。无论在哪个任务选择，都同时评估两任务；不改其他层。每个主要集合构造八个随机特征集合，排除全部候选 ID，按标准化对数出现率和对数解码行范数的距离，从最近二十个未使用候选随机选匹配特征，数量相同。每个样本的随机修改再缩放到候选修改的欧氏范数。记录零支持；随机修改为零但目标非零时使用固定种子的各向同性方向补足，并明确计数，不伪装成成功匹配。

对相同输入，将混合状态的候选系数移入顺序、学会 A、Base 三种状态。比较匹配随机特征替换、零/同上下文替换及完整供体向量替换。完整替换只检验实现，不证明稀疏定位或跨任务复用。

原始几何使用发现 SVD 的 rank 1/4/16 投影，将 mixed 减 sequential 的变化移入 sequential。各与八个同秩随机正交子空间比较，并逐样本配平扰动范数。另测 rank-16 补空间和完整差值。该操作定位状态差异，不是删除接收模型整个子空间，也不能宣称找到普适最重要方向。

## 估计与三个主要判断

先在无序词组内平均，再跨组平均。只在评估集检验三个主要对比：(1) 混合旧候选削弱一半对旧任务的间隔损害减八个对照均值；(2) 新候选对新任务的对应量；(3) rank-16 替换对旧任务的间隔改善减随机子空间均值。以同一 204 组做 5,000 次配对 bootstrap，种子 20261023，报告双侧 98.333% 百分位区间。下界严格正支持局部对比，上界非正削弱，跨零证据不足。不能评估后再挑最好秩或特征数作为主要检验。

其他削弱强度、接收模型、特征集合、单特征、概率、共现及准确率变化均为描述性结果；需要时给 95% 组级区间。一个训练种子不构成训练重复。后续选择必须标记事后分析。

## 资源、复用与停止规则

使用一个单节点 `h100-1-reserved` ACP 任务、`shphd-lite-0911` 镜像、挂载 CrossCoder runtime，完整分析最长 3,600 秒。遵循研究者所述单/双卡可用条件；本范围不采用无关的四卡默认。先在本地 MIG 对发现样本做有界工程 smoke；它只检查数值和接口，不证明完整 H100 节点运行资格。使用仓库模板，先 dry run，再记录提交回执。研究者要求完成分析，因此跟进到任务结束；不重复提交活跃任务，不自动切换资源。

复用 `carriers.QwenCarrier`、`FrozenQwenExtractor`、`data_routes.encode` 及已有归一化/解码类；适配选择与干预。不复用旧四卡启动器或布尔题逻辑。零修改、身份、有限值、权重不变、完整样本或超时检查失败时停止依赖阶段。冻结范围内的工程修复须保留失败输出和偏差记录，不静默放宽科学标准。

## 交付与审计

执行侧保存原生/原始/特征缓存、逐样本干预量、候选选择、几何、资格、bootstrap、完成回执、代码/配置/数据哈希和图。登记可复用表征产物。中英 Summary 按目的→模型→观察→受控修改→有边界的回答解释；Detailed 保存契约对照、科学/数据/实现审计、偏差与证据链。图包括样例答案卡、小特征热图和带不确定性的干预对比，均链接原始数据与脚本。通过既有 builder 同步 Anchor/Protocol/Summary/Detailed 的本地阅读副本。不 commit 或 push。
