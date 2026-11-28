# 哪些结果已经改变了小模型的设计选择

2026 年 11 月 28 日，北京时间。两个对话共享一段早期历史。这里按实验对象各记一次。旧模型名中的 B、Flat、Oracle 都曾指过不同的网络，因此下文同时给出层位、路由和激活宽度。[1125 对话](thread://01a20e9a-7bcf-7690-8369-b97f86500c09?hostId=remote-ssh-codex-managed%3Amig) · [1126 分支](thread://01a21840-edb6-7bf2-bc25-753065149a11?hostId=remote-ssh-codex-managed%3Amig)

## 我们测到了哪一步

| 问题与证据类型 | 已完成的比较 | 对下一步的约束 |
|---|---|---|
| 哪些表征可以共享？冻结几何与读出 | Qwen3.5 Base 的 2B、9B、35B-A3B，分别用末块 L23/L31/L39 的 Top-50 SAE 读最终归一化前的残差。在问答和论文摘要的四叶领域中，扣去四域及同学科共有成分，跨学科全维重叠下降 65%–96%。去八个共变伙伴，相对等能量随机删除的净信干比为 1.30–1.46 倍，在同一套 32 对题上六组都没有区间支持原生 NLL 改善。 | 共有成分解释了一部分几何重叠。把某个方向读得更清楚，与模型更会答题之间仍缺一项检验。[末层报告与分母](/data/250010109/MoE_Router/experiments/1123_four_leaf/scaling_1124/last_layer/last_layer_report.md) |
| V5 中各层等活跃可否代入？冻结测量 | Qwen 2B L23、16 万篇建图，在同两叶按相同规则选前 6 个或 756 个特征，独立文档上每词元平均根/叶激活数之比分别为 230.07、10.46。后者仅两片叶能取满。 | 分别测每级激活特征数、候选池大小和实际专家调用率。HRJ 这次问的正是逐 token 的分布，已有均值只回答了一部分。[同叶同配额对照](/data/250010109/MoE_Router/experiments/1126_qwen_dclm_last_scaling/summary_cn.md) |
| 分流什么时候能使长尾学得快？受控训练 | 八叶、已知真特征的合成标量回归，48 次运行。弱特征误差下降 70% 时，相对 Dense 的全批 GD 步数比，在伙伴共变强度约 3.3 时，V5 硬树 2.36×、V6 宽共享 2.39×、理想正交 12.90×；小批 AdamW 的后两者为 2.75×、5.67×。相同分块步长可在稠密参数化中重现宽共享更新。 | 需要分开考察信息进入了哪里和优化器怎样缩放更新。此处 GD 与 AdamW 的 batch 也不同。[三种子与成本定义](/data/250010109/MoE_Router/experiments/v6_dynamics_1125/v6_dynamics_report.md) · [更新等价性与实词实验](/data/250010109/MoE_Router/experiments/v6_architecture_1125/architecture_report.md) |
| 预测低频词能否代表学会了知识？小模型训练与任务读出 | 163 万参数模型保留共享主干，用开头 24 个词推断领域、在词表端修正分数。同质量含预热步数 340→320；双方配平记录流程后，15 对计时的中位速度比 1.010×。条件改变会翻转答案的题需要额外能力。 | 主题词表先验就能带来长尾词收益。应有表面词相近、改变一个条件会改变答案的题来验证方向代理。[同质量与条件题](/data/250010109/MoE_Router/experiments/v6_architecture_1125/architecture_report.md) |
| 不看低频目标，常见线索能找回多少？冻结路由读出 | Qwen3.5-2B L23 同 token 共激活 PPMI 建七个平坦簇。固定七簇，在 16 万篇上补归属。新留出 1,009 篇中 15,205 个可判位置，按全部隐藏低频系数平方和计，Top-2 从 6.01% 到 48.67%，打乱新增归属为 34.65%，保负载打乱选路为 32.21%。另一比较固定同一套叶，跨父二选覆盖 44.69%，限在同父为 36.01%，原始配对差 8.67 个百分点。9B 分支已停止。 | 常见线索有预测力，单父资格会挡住部分可找回的细节。两组实验的分组与位置口径各自固定，覆盖百分比只在各自的对照间比较。[七簇与分母](/data/250010109/MoE_Router/experiments/1126_sae_feature_clusters/v5_clustering_analysis_report.md) · [固定叶组对照](/data/250010109/MoE_Router/experiments/1126_sae_feature_clusters/night_overlap/overlap_alignment_report.md) |
| 路由能让叶专门化吗？冻结模型上的局部干预与梯度 | HD4-T 第 2,000 步末层，同位置、同误差信号交给原配叶，参数梯度平方范数为保负载打乱的 2.035 倍，初始权重只为 1.006 倍。扩到 512 段后，叶内低频词与其余词的平均梯度余弦为 −0.850。两组争夺总词表概率这一项占完整负内积的 84.9%。 | 叶对经常分给它的位置反应更强。梯度大、负余弦或浅层冲突小，各自都不足以解释训练提速。要观察一次更新对另一篇文本的净作用。[固定输入与权重互换](/data/250010109/MoE_Router/experiments/1127_opt_dynamics_diag/l7_mechanism/sequence_variance/report.md) · [词表概率分解](/data/250010109/MoE_Router/experiments/1127_opt_dynamics_diag/l7_mechanism/report.md) |

1126 分支已经检验过“同一特征在两类文本里是否指向相同的下一词预测”。问答与论文的 5,391 条特征–领域对记录中，只有 51 条在两域各自拆半后，目标梯度方向余弦都高于 0.5；这 51 条中有 49 条跨域也一致。DCLM 则有 153/2,050 条通过拆半，其中 66 条跨域一致，41 条负向。频率低时方向本身就估不准。这是本轮把同特征跨文本正对照和不可判定分支写进主实验的直接依据。[分面板的方向与可靠性](</data/250010109/MoE_Router/experiments/1126_sae_feature_clusters/night_overlap/overlap_alignment_report.md>)

## 哪些架构实际训练过

DCLM 学生主线是 8 个 Transformer 块，残差宽 1,024。表中“宽”指 SwiGLU 中间宽度；每个启动的专家仍可读完整残差，除非注明了输入投影。专家组之间的层级、Transformer 的网络深度和教师 SAE 的取样层位是三个不同的坐标。[模型记录](../../../../Projects/small_model/users/XingyuDeng/ablation/training_record.md) · [八层父叶与 Flat 源码](/data/250010109/MoE_Router/experiments/1127_hier_teacher_50b/arms.py) · [HD4 源码](/data/250010109/MoE_Router/experiments/1127_qwen_hd4_oracle/hd4_model.py)

| 架构 | 设计依据和实际执行 | 可判读的结果 |
|---|---|---|
| A0 | 每层 8 个宽 1,536 的专家，自学习路由选 2，激活宽 3,072。 | 原生平坦对照。 |
| 原 B → C005 → R005 | 前四层原生；后四层共享 1,536 加 14 个宽 768 的专家选 2。C 约束同时写回的输出重叠，R 从 C 第 500 步继续监督路由器选互补的两位专家。 | 30 亿 tokens 稀有词 PPL 为 B 242.89、C 243.41、R 240.82、A0 241.74。R 相对 C 改善；R 相对 A0 的稀有词配对区间跨零。[同起点对照](/data/250010109/MoE_Router/experiments/1126_v62_tree/assessment_1126_3b/report.md) |
| T1、T1-LR×1.5、T2、T3 | T1 全层共享加 7 选 1，路由专家扣去输入的前 64 个大方差方向；学习率变体仅提高这批专家的步长。T2 另外改路由输入和负载偏置。T3 改为根 1,536、2 个父选 1、该父的 4 个叶选 1，父叶各宽 768，总参数随之改变。 | 同为 30 亿 tokens，总体 NLL 依次 3.42672、3.42248、3.48263、3.49195，A0 为 3.39428。现有输入剥离或树实现均未追回差距。单换步长的收益有限。[最终原表](/data/250010109/MoE_Router/experiments/1126_v62_tree/assessment_1126_2045/step_11446/holdout.csv) |
| B-Std、R005-1S7E1、B-Flat-SAE | 八层各用 1 个共享和 7 个路由专家选 1，均宽 1,536。新版 R005 的互补选择变为单专家；Flat-SAE 只给后四层的学生路由加冻结七簇教师 KL，系数 0.01。T3-FixedGrad 单列验证修复后的门梯度。 | 三个标准化对照臂已到 10 亿，B-Flat-SAE 也已到 10 亿。Flat-SAE 相对 B-Std 的总体 NLL 高 0.01510、稀有词 NLL 高 0.02568。旧 R005 的结果依赖搭配拓扑。[同预算表](/data/250010109/MoE_Router/experiments/1127_hier_teacher_50b/progress_1128/holdout_1b.csv) · [路由梯度核验](/data/250010109/MoE_Router/experiments/1126_v62_tree/router_gradient_check/formulas.md) |
| Flat-Std-50B、早期 Hier-Oracle / Learn | Flat-Std 全层共享 1,536 加 7 个宽 1,536 的专家选 2，激活宽 **4,608**。早期树是共享 1,536 加 4 个父选 1、该父下的 2 个叶至多选 1，父叶各宽 896，激活宽为 2,432 或 3,328。Oracle 用教师，Learn 在学生残差上学选路。 | 2.5 亿时 Flat、Learn、Oracle 总体 NLL 分别为 4.6823、4.7539、4.7563。早期 Learn 出现父流量集中；这些臂均提前停止。16k 建图使四父八叶都有成员，旧执行规则仍只在 20,588/64,576 位置调用叶。层位、教师、激活宽度、写回权重都会影响这些比较。[2.5 亿同预算三组原表](/data/250010109/MoE_Router/experiments/1127_hier_teacher_50b/runs/formal) · [建树记录](../../../from-attention-to-search/main/explore/1126_sae_feature_clusters/log.md) · [执行回放](/data/250010109/MoE_Router/experiments/1126_sae_feature_clusters/tree16000/leaf_execution_replay.json) |
| HD4-T、Qwen-HD4-Oracle | 浅四块沿用 A0。深四块各有一个宽 1,664 的共享根和 2/4/8/16 个宽 352 的分支专家。每个 token 必走四次二分，各级取一，合计 3,072。旧教师用 Qwen3-0.6B L27 MLP 前 E16 SAE Top-32；新教师用 Qwen3.5-2B L23 块后 SAE Top-50，共现建图、按激活幅值与逆频权重选路。验证也使用教师。 | 1,008 篇独立前缀上，新教师给 64,512 个位置全部分配路径，16 个叶各占 4.99%–8.91%。学生能否只凭自身前缀选路，并保住教师带来的收益，仍需同骨架直接比较。[旧教师定义](../../../from-attention-to-search/main/explore/1113_hd4/log.md) · [新教师标定](/data/250010109/MoE_Router/experiments/1127_qwen_hd4_oracle/map_audit.json) |

还有一项能约束 8 维门控基线的读出。HD4-T 第 500 步，学生第一个深层路由入口的线性探针，整条四级路径准确率为 48.47%，同一留出上的 token-ID 基线为 41.69%。后续深层的表示已接收教师选路信息。因此，检验学生能否自主选路，应先读第一处尚未经过教师分发的位置，并在接管路由后重测损失。[冻结探针与对照](../../../from-attention-to-search/main/explore/1113_hd4/log.md)

### 深层树的同预算留出结果

同一留出面板有 1,024 条序列、每条 2,048 个预测位置。稀有词按训练中目标词的累计事件质量最低约 20% 分桶；低频 SAE NLL 按冻结字典最低三个频档在这些位置的激活事件加权。同一个词位可以出现多次特征激活。模型均只把词预测损失计入 NLL。下表越低越好。[频带与重放定义](/data/250010109/MoE_Router/experiments/1127_hier_teacher_50b/progress_1128/compare.py)

| 有效训练 tokens | 模型 | 总体 NLL | 稀有词 PPL | 低频 SAE NLL |
|---|---|---:|---:|---:|
| 10 亿 | A0 | 3.77943 | 532.03 | 3.44572 |
| 约 10 亿 | HD4-T（多 0.034% tokens） | 3.75081 | 499.11 | 3.41450 |
| 10 亿 | Qwen-HD4-Oracle | 3.75089 | 503.79 | 3.39225 |
| 10 亿 | B-Std / B-Flat-SAE | 3.79673 / 3.81183 | 545.11 / 559.29 | 3.47097 / 3.48629 |
| 30 亿 | A0 | 3.39428 | 241.74 | 2.85390 |
| 30 亿 | Qwen-HD4-Oracle | **3.38649** | **235.39** | **2.83380** |

10 亿处，新旧教师总体差 +0.00009 nat，留出序列配对 95% 区间 [−0.00239, +0.00219]。换用新教师，稀有词 NLL 高 0.00933，低频 SAE NLL 低 0.02225。严格 30 亿处，新版与 A0 的总体差为 −0.00780 [−0.00929, −0.00631]；这项差值在 5 亿、10 亿时分别为 −0.05874、−0.02853。区间反映序列抽样；重复训练种子的波动待测。30 亿结果是在两个对话最后汇报之后落盘，来自正式第 11,446 步。[10 亿原表](/data/250010109/MoE_Router/experiments/1127_hier_teacher_50b/progress_1128/holdout_1b.csv) · [配对区间](/data/250010109/MoE_Router/experiments/1127_hier_teacher_50b/progress_1128/paired.csv) · [30 亿逐模型实测](/data/250010109/MoE_Router/experiments/1127_qwen_hd4_oracle/runs/formal/Qwen-HD4-Oracle/paired_3000000000.csv)

组会的 **1.22×** 来自 A0 和历史 HD4-T 的训练 CE 首次到 6.4，约第 261.45 对 215.01 步，同批量折成 token 比 1.216。它描述一个早期阈值。V5 的 8× 指理想平方回归的叶方向更新，二者的目标、优化器、路由与成本都需要分别对齐。[阈值原表](/data/250010109/MoE_Router/experiments/1115_night_efficiency/1115-figure_threshold_check.csv)

## 两位学长各自补了什么

协作仓本次从远端拉取 main 后，HEAD、origin/main、FETCH_HEAD 均为 **7a03131d9e0d00b5f26be461be6334c2de41fd64**。CHJ 的第 4–5 轮在 7a03131；HRJ 的报告在 ee22e06。以下用报告中的模型配置和原始结果文件解释两者的不同判断。

- **CHJ（曹恒杰）检验了分组的必要性。** Gemma 2 9B 的 128 个 token 上下文簇上，实测 feature 受众对 80.7% 交叉，等受众大小随机为 87.2%。在他的小 LM 中，固定激活预算的扁平细粒度配置、硬层级配置、普通 Dense 验证损失为 3.6783、3.7187、3.7339；若加大总参数，宽专家 top-1 另有 3.6689。分组进入 SAE 前向并加重构对齐的另一组实验里，同宽 E=64 真实分块 4.9796、随机分块 4.9705，同一真实分块换种子为 5.0040。E=4 的 4.9308 也需要与不分发的两个种子 4.9554、4.7091 一起看。对齐与教师冻结参数是实质性条件；其估算这条 SAE 前向约为基线 20 倍计算。真实 LM 中按专家频率调学习率的效果该组尚无直接结果。[CHJ 报告](../../../../Projects/small_model/users/HengjieCao/code/SAE_MOE_FINDINGS.md) · [分块与未分发原始 JSON](../../../../Projects/small_model/users/HengjieCao/code/lm/results_sae)
- **HRJ（仓库名 ruijunHuang）检验了跨组复用时还剩多少富集。** Gemma 2 9B L27，在 8 个 SFT 领域上测试，深 HIFER 组已激活时，浅组也激活的平均比例 63.9%，频率匹配随机 54.7%。Depth 2 的长尾特征在主要专家内的出现率是全局的 3.59 倍；从该特征的全部激活反过来看，主要专家接住的中位比例是 47.9%。两项中位数分别汇总。受控八叶回归中，将重叠从 0 提至约 0.4，达到 70% 长尾标准的步数优势从 4.94× 降至 1.24×，80% 标准从 6.09× 降至 2.12×。交叉率来自 CHJ 测量的引用，不能算作两次独立复现。[HRJ 报告](../../../../Projects/small_model/users/ruijunHuang/tree_moe_report/report.md)
- **11 月 28 日 HRJ 自述的周末计划**有三项。逐 token 数每个 HIFER 层级激活了几个 feature，以指导平坦专家分配；改变建图样本量和阈值，复核“入图约占字典 25%”；检验统计父子关系是否对应导师关心的语义。25% 是待复核的初估，分母是全字典 feature 数。[沟通原文](../../sources/meetings/1128-沟通内容.md)

**AI 建议。** 保留学长实验里最有信息的两个对照。用 HRJ 的分层计数定位跨父需求，再用 CHJ 的同频随机分组和学习型扁平路由检验替代解释。优先判断分组是否让一次参数更新帮助未见文本，再给结构改动分配算力。[本轮问题、推导与预先判断](../explore/1128_feature_grouping/log.md)
