# Detailed：A17_04_E03 单层注意力学习测试

主 Anchor：[A17_04_01](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor.md)。Protocol：[中文版](protocol_cn.md)，版本 `a17_04_e03_single_attention_acquisition_v1`。Summary：[中文版](summary_cn.md)。[English](detailed.md)。

结果状态：`COMPLETE`。两组均具备单种子、已暴露DEV诊断的工程资格。AdamW路线通过；本次SGD路线未通过。研究者科学判断和父问题关闭仍为`Unknown`。后续迁移与机制实验为`NOT_RUN`。

## 0. 快速回顾

- 目的：判断只开放最后一层 Q/K/V/O 投影权重，是否能够学会原来的中性口令规则。
- 模型／逻辑：同一份中性数据、种子29，只训练第27层四权重，共6,291,456参数；比较两套既有SGD／AdamW设置。固定Main1200步，四个DEV分项均须达到80%。
- 直接结果：AdamW合并800/800、四格均200/200、400个列表均能在两口令下答对；SGD合并422/800，最低93/200=46.5%。
- 资格：CPU／数据、两套真实GPU路径、Smoke独立进程恢复、telemetry／冻结检查、独立分析及实际资产访问全部通过。
- 判定：`attn1_adam`为`QUALIFIED_ROUTE`；`attn1_sgd`为`NON_SUPPORT_WITHIN_BUDGET`。后者不是无效运行，也不是所有SGD设置都失败。
- 边界：单种子、已暴露DEV；不能归因纯优化器或纯容量，不能说明只Q/K/V就够、数学最小性、迁移或SAE／expert机制，也不关闭父问题。
- 来源：[独立结果记录](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/results.json)与[分析证据清单](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/analysis_manifest.json)。

## 1. 术语与对象

| 术语 | 具体对象／计算 | 单位和作用 | 边界 |
| --- | --- | --- | --- |
| 中性口令 | 模式一中甲取首项，乙取末项 | 每条记录一个答案目标 | 要学会按口令改变选择，候选词概率高不等于学会 |
| 单层注意力范围 | 第27层 Q/K/V/O 四张投影权重 | 可训练参数6,291,456 | Q/K 归一化和其他参数冻结 |
| Tiny／Main | 64个固定训练目标／独立从 Base 重启的2,400条训练记录 | 160／1,200步 | Tiny 权重不用于初始化 Main |
| 未见顺序／未见组合 | 熟悉无序三词组的新排序／未见无序三词组 | 各400个 DEV 目标 | 已暴露的开发集，非确认集 |
| 最弱 DEV 分项 | 两个口令×两种面板共四格中的最低准确率 | 每格200个目标，达到80%算通过 | 合并平均值不能替代四格标准 |
| 列表候选词概率 | 三个列表词的概率和 | 概率；支持 CE 的访问／选择分解 | 不能单独说明按口令选择 |

## 2. 与 Anchor 的衔接及决定点

E03继承A17_04_01的学习诊断。E02已有单输出投影未通过、四层AdamW可行的证据。本次完成了更小范围的可行路线：最后一层Q/K/V/O加本次AdamW设置。因此，在这份数据和设置中，学会规则不必开放四层。这个结果不识别内部原因，不修改父问题的条件映射迁移假设。用户只授权先完成这个小测试；事实汇报后停止。

## 3. Protocol 冻结、一致性与偏离

注册版本为`a17_04_e03_single_attention_acquisition_v1`。[GPU前冻结清单](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/freeze.json)于2026-10-11 23:01:39 Asia/Shanghai（15:01:39UTC）绑定36个文件。[最终身份核验](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/postexecution_freeze_verification.json)全部36项通过，零不一致。保存了原始EN/CN Protocol、Anchor／Focus快照、源码／配置、数据和Base身份。

| 注册项 | 预定设置 | 实际执行 | 状态／资格 |
| --- | --- | --- | --- |
| 范围 | 两组单层学习；不执行后续 | 仅attn1_sgd与attn1_adam；不读TEST／模式二 | 一致 |
| 数据／划分 | 现有neutral TRAIN/tiny/panel/DEV | 选定哈希和数量一致；没有重造 | PASS |
| 可训练范围 | 第27层Q/K/V/O四权重，6,291,456 | 实际张量及首步四张变化一致；其他冻结 | PASS |
| 目标 | 每步20答案、micro5×4、CE总和/20 | 原始计数与原生读数一致；无跳过更新 | PASS |
| 优化设置 | 既定SGD／AdamW；四张全局clip1 | 实际梯度／更新与保存状态一致 | PASS；未匹配实际位移 |
| 预算／阶段 | 每组Tiny160，独立Base重启Main1200 | 各完成3,200+24,000答案 | PASS；正式合计54,400 |
| Smoke计数 | 每组每阶段3步；原文误写总数120 | 实际12步=240答案；恢复80另计 | A01算术勘误；源码／配置／次数未变 |
| 保存 | Tiny0/1/160；Main0/1/240/600/1200 | 正式16个、Smoke12个状态 | PASS；实际资产已登记 |
| 资源 | 4H100 reserved节点，2个独立worker | 节点实际4H100；GPU0/1训练，2/3不用 | PASS；非DDP、非复验 |
| 恢复／telemetry／冻结 | 新进程step1→2；7标签；身份不变 | 两组两阶段精确恢复；标签计数及36身份通过 | PASS；Full续训本身未做 |
| 分析 | 四终点格、分开／合并面板、所有里程碑 | 独立核验34预测文件、17,184次记录读数 | PASS；单种子诊断 |

[Protocol](protocol_cn.md)中的A01保留冻结原文，只把Smoke总数120更正为240；每组每阶段3步始终未变。Smoke平台启动前等待约5分钟，原因`Unknown`，不能归因资源不足、代码或某一步容器准备。没有失败重跑、分组排除、新种子、按结果追加预算或新增训练。平台成功、工程资格和是否学会是三个不同证据层次。

## 4. 实际设置

父模型是已登记的官方 Qwen3-0.6B Base，目录 `/data/250010109/model_cache/Qwen3-0.6B-Base-official`，资产ID `model_qwen3_0p6b_base_official_a5`；分词器ID `tokenizer_qwen3_0p6b_base_official_a5`。数据ID为 `data_a17_mapping_acquisition_diagnostic_v1`。只复用其中四个 neutral 文件，保留原 ID、空格列表、口令、标签和 tokenization；没有重新造数据。

| 分组 | 可训练权重 | 参数数 | 固定优化设置 |
| --- | --- | ---: | --- |
| `attn1_sgd` | 第27层 Q/K/V/O | 6,291,456 | SGD lr .01；动量0；衰减0 |
| `attn1_adam` | 相同四权重 | 6,291,456 | AdamW lr1e-4；betas(.9,.999)；eps1e-8；衰减0 |

形状分别为 Q[2048,1024]、K[1024,1024]、V[1024,1024]、O[1024,2048]。Q/K 归一化、MLP、embedding、输出词表头以及其他层均冻结。前向使用原生 FP32 SDPA，evaluation 模式、不启用 dropout 或 TF32，启用确定性算法。没有固定上游激活缓存。

两组同用种子29，每阶段列表配对顺序相同。每个独立 worker 每步处理20个答案，分四个 microbatch，每个5条。Tiny64个目标训练160步，共3,200次呈现／组。Main独立重置 Base、优化器和RNG，用2,400条训练记录训练1,200步，共24,000次呈现／组。Main保存0/1/240/600/1200，Tiny保存0/1/160。两组正式拟合合计54,400个目标。Smoke实际240个、外部恢复80个目标单独计数（A01更正冻结原文的合计算术笔误）。没有按成功率追加训练或提前停止。

SGD 把四张矩阵梯度合起来计算一个范数，使用同一裁剪系数更新全部四张。这里替换了 E02 只更新一张矩阵的分支。AdamW 也对四张梯度一起裁剪。两者均按答案 CE 总和除以20反传；输入前缀和 padding 不计损失或主要目标计数。优化器之间没有匹配实际参数位移、预条件或步长尺度。

复用原生 Base/AnswerLM、collate、配对顺序、检查点字段和 telemetry；适配四矩阵范围、多矩阵 SGD 以及两组分析程序；不复用旧端点重复审计、数据展示变体、迁移和 SAE／expert 路径。[复用来源](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/configs/reuse_sources.json) 保存旧源码身份和取舍；实现说明见 [/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source/IMPLEMENTATION.md](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source/IMPLEMENTATION.md)。

| 身份 | 路径 | SHA-256 |
| --- | --- | --- |
| 运行配置 | [/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/config.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/config.json) | `bb48841e814e7b93725b165b8eadc4f8481763f01f1746401b570080445f6aa8` |
| 数据清单 | [/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1/manifest.json](/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic/data/acquisition_v1/manifest.json) | `05dfb9ac05ebf20dcf560b51d880acdb9472596b2a0a346aa8401d0dc9438a89` |
| 训练程序 | [/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source/diagnose.py](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source/diagnose.py) | `1df552946bd8f70c517f3aba332f7d5722fdf75736ea364f7c8528ea845879a0` |
| 分析程序 | [/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source/analyze.py](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source/analyze.py) | `915a7a1df77232ac2e0185ee416c242aed806e6816ce7b8caec2a4ccbe7e5de1` |

这些身份与GPU前36文件冻结及最终零不一致核验吻合。原始数据、日志和状态保留在执行侧，不复制到正式研究仓库。

## 5. 指标与注册判断规则

主要指标 `Q_j` 是四个 DEV 分项的最低全词表准确率，每格200条。固定 Main1200步为主要终点。有资格的分组须四格均达到80%才通过；有效但未达标，是本预算下不支持。必要证据缺失或无效则为不足。分别汇报未见顺序、未见组合及800条合并结果，并保留四格、400条已见训练面板和同列表两口令都答对的比例。最早保存的达标检查点仅作描述，不改变终点。

辅助指标包括答案 CE、三个列表词的概率和、访问 CE、条件选择 CE、正确答案相对相反端点的优势、全词表最强竞争答案及口令响应。精确输出分解为 `CE = -log(列表概率和) - log[p(正确答案)/列表概率和]`。候选词概率高或平均优势为正不能替代主要准确率。这里只有一个独立训练种子，不能把800条样本看作800次训练复验。

## 6. 证据链

| 认识／决定 | 注册标准 | 原始产物／计算 | 观测值 | 资格与局限 |
| --- | --- | --- | --- | --- |
| 真实单层训练有效 | 张量／目标／冻结／TB一致 | worker范围／完成、阶段telemetry、[smoke_gate.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/smoke_gate.json) | 两组两阶段PASS | 工程，不是学会 |
| 已测试下一步可恢复 | 独立进程step1→2完全一致 | 两个resume_worker回执 | 两组tiny/main精确一致 | 仅Smoke恢复；Full续训未做 |
| AdamW是一条可行路线 | 最终四格均≥80% | `full/attn1_adam/main/eval_dev_01200.json`及冻结分析器 | 四格200/200、合并800/800、400配对全对 | QUALIFIED_ROUTE；单种子已暴露DEV |
| 本次SGD设置不足 | 同一四格标准 | `full/attn1_sgd/main/eval_dev_01200.json`及同一分析器 | 422/800、最低93/200=46.5% | NON_SUPPORT_WITHIN_BUDGET；非所有SGD失败 |
| Tiny拟合与泛化不同 | Main独立重启；分开Tiny读数 | Tiny160结果与Main初始／顺序身份 | Adam Tiny64/64，DEV523/800 | 拟合不等于泛化；非Tiny初始化效应 |
| 候选词集中不足以学会 | 辅助读数不能救主要准确率 | 逐样本CE／概率／优势 | SGD列表概率98.2288%，准确率52.75% | 输出记账；非参数机制 |
| 实际产物可用 | 保存与选定strict访问 | [独立复审记录](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/independent_final_audit.json) | 第二Agent的CPU复核报告 | PASS；无单独保存的审计脚本 | 工程／证据复核；主要来源仍为原生结果 |
| [full_registration_receipt.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full_registration_receipt.json)及访问快照 | 16状态／4族+分析，共5IDs PASS | 可用性；非科学批准 |
| 独立核验完成 | 规定读数和状态身份 | [analysis/analysis_manifest.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/analysis_manifest.json) | 34文件、17,184读数、16反序列化状态；最大误差1.623109e-6 | PASS；跨阶段／检查点重复读数非独立复验 |

## 7. 主要结果

### 固定 Main 终点

来源：[analysis/results.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/results.json)及[analysis/trajectories.csv](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/trajectories.csv)。每组一个种子。表中均为全词表预测，保留正确／总数。每个DEV面板400条、合并800条；配对指标以400个列表计算。

| 分组 | 已见TRAIN | 未见顺序DEV | 未见组合DEV | 合并DEV | 最低分项 | 两口令都对 | 改口令仍同答案 | 首个保存的达标步 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| attn1_sgd | 246/400 (61.5%) | 208/400 (52%) | 214/400 (53.5%) | 422/800 (52.75%) | 46.5% | 67/400 (16.75%) | 305/400 (76.25%) | Not reached / 未达标 |
| attn1_adam | 400/400 (100%) | 400/400 (100%) | 400/400 (100%) | 800/800 (100%) | 100% | 400/400 (100%) | 0/400 (0%) | 240 |

| 分组 | 甲／顺序 | 乙／顺序 | 甲／组合 | 乙／组合 |
| --- | --- | --- | --- | --- |
| attn1_sgd | 112/200 (56%) | 96/200 (48%) | 121/200 (60.5%) | 93/200 (46.5%) |
| attn1_adam | 200/200 (100%) | 200/200 (100%) | 200/200 (100%) | 200/200 (100%) |

AdamW的800条均正确；SGD在相同800条中正确422条。对应逐样本终点差异是多正确378条，即47.25个百分点。两组同时改变优化器和学习率，不能把这个差异说成纯优化器家族的因果效应。

### Main 保存轨迹

| 分组 | 更新步 | 有效答案 | 合并DEV | 最低分项 | CE，nat | 操作达标状态 |
| --- | ---: | ---: | --- | --- | ---: | --- |
| attn1_sgd | 0 | 0 | 266/800 (33.25%) | 30.5% | 2.44652492 | BELOW_THRESHOLD |
| attn1_sgd | 1 | 20 | 299/800 (37.375%) | 33% | 2.33569756 | BELOW_THRESHOLD |
| attn1_sgd | 240 | 4800 | 358/800 (44.75%) | 41.5% | 1.13323379 | BELOW_THRESHOLD |
| attn1_sgd | 600 | 12000 | 357/800 (44.625%) | 42.5% | 1.07828572 | BELOW_THRESHOLD |
| attn1_sgd | 1200 | 24000 | 422/800 (52.75%) | 46.5% | 0.941982446 | BELOW_THRESHOLD |
| attn1_adam | 0 | 0 | 266/800 (33.25%) | 30.5% | 2.44652492 | BELOW_THRESHOLD |
| attn1_adam | 1 | 20 | 324/800 (40.5%) | 36.5% | 2.05406645 | BELOW_THRESHOLD |
| attn1_adam | 240 | 4800 | 795/800 (99.375%) | 98.5% | 0.0243161194 | PASS |
| attn1_adam | 600 | 12000 | 800/800 (100%) | 100% | 0.00114245424 | PASS |
| attn1_adam | 1200 | 24000 | 800/800 (100%) | 100% | 0.000691031676 | PASS |

AdamW首次在保存的240步达标：795/800=99.375%，最低197/200=98.5%。600步达到100%，1200步仍100%。SGD任何保存里程碑都未达标。两组都执行完整1200步，没有根据结果提前停训。

### Tiny 拟合单独报告

| 分组 | Tiny已见64条 | Tiny两口令配对全对 | 仅Tiny160步后DEV | DEV CE，nat |
| --- | --- | --- | --- | ---: |
| attn1_sgd | 38/64 (59.375%) | 6/32 (18.75%) | 370/800 (46.25%) | 1.12980054 |
| attn1_adam | 64/64 (100%) | 32/32 (100%) | 523/800 (65.375%) | 1.95976332 |

AdamW能拟合Tiny64/64，但该条训练轨迹的DEV只有523/800=65.375%。Main独立从Base重启后达到800/800。因此，Tiny拟合不能替代泛化判断；Tiny权重也没有带入Main。

### 终点输出分解

| 分组 | 答案CE，nat | 列表候选词概率 | 访问CE，nat | 条件选择CE，nat | 口令响应a |
| --- | ---: | --- | ---: | ---: | ---: |
| attn1_sgd | 0.941982446 | 98.2288% | 0.0181517312 | 0.923830715 | 0.266854887 |
| attn1_adam | 0.000691031676 | 99.9994% | 5.93932e-06 | 0.000685092356 | 17.5246531 |

SGD把98.2288%的概率放到三个列表词，但400个列表中305个（76.25%）改口令仍输出同一答案，只有67个（16.75%）能两口令都答对。AdamW的400个列表均两口令正确，没有改口令仍输出相同词的列表。这说明候选词集中与按口令选择可以区分；没有说明内部哪种参数操作造成成功。

### 实际呈现与更新幅度

来源：[analysis/training_exposure.csv](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/training_exposure.csv)。前缀token另计，不代替有效答案次数。

| 分组 | 阶段 | 更新步 | 有效答案 | 前缀token | 平均步范数 | 步范数之和 | 最后20步训练CE |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| attn1_sgd | tiny | 160 | 3200 | 65100 | 0.0100000001 | 1.60000002 | 0.927465092 |
| attn1_sgd | main | 1200 | 24000 | 489600 | 0.0100000002 | 12.0000002 | 0.86540369 |
| attn1_adam | tiny | 160 | 3200 | 65100 | 0.0439364153 | 7.02982645 | 0.000172431538 |
| attn1_adam | main | 1200 | 24000 | 489600 | 0.0152092912 | 18.2511494 | 3.76110808e-05 |

目标次数和张量数相同，不等于参数实际位移相同。SGD Main路径长度12.0000002，AdamW18.2511494。整个轨迹涉及不同状态，不能用这两个数分离预条件与步长作用。

### 工程和资产

Smoke `pt-gwd1382k`、Full `pt-8fizcddl`均成功。Full在2026-10-11 23:09:55开始，23:15:03结束（Asia/Shanghai）。[平台终态回执](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full_platform_terminal_status.json)不能代替张量与读数检查。独立分析器反序列化全部16个正式状态，核验四张FP32权重形状／有限性、Adam各张量step／moment形状／有限性、父模型／配置／数据身份及答案／更新计数。它核验34预测文件、17,184次记录读数和损失等式，最大误差1.623109e-6nat，小于注册2e-5容差。

[执行后身份检查](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/postexecution_freeze_verification.json)确认36文件完全未变。Smoke12状态、正式16状态分别登记为每阶段四个checkpoint族及一个原生分析族，两次共10IDs。选定当前strict访问全部通过。strict访问本身不反序列化权重；独立分析器提供另一层实际张量资格。第二个只读审计Agent也独立在CPU加载16个状态，核对Base重启四权重相同、Adam状态、保存顺序、7标签、34文件和36哈希，结果PASS。[独立复审记录](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/independent_final_audit.json)是root记录的同行报告；没有保存独立脚本文件，不作为新的主要测量来源。[最终选定14项访问](/data/250010109/Research_System/assets/checks/2026-10-11_a17_single_attention_delivery_access.json)通过。独立进程恢复仅在Smoke做过。Full重新启动／续训测试为`NOT_RUN`，正常训练完成不等于做过Full恢复。

## 8. 阶段证据与失败分解

| 阶段 | 证据 | 状态 | 已说明／仍未知 |
| --- | --- | --- | --- |
| CPU helper | 实际四矩阵helper／toy attention | PASS | 更新、归一化、恢复检查；非Qwen科学结论 |
| 中性数据及输入 | 既有数据、当前strict、冻结成员 | PASS | 未改内容或格式，继承原tokenization |
| 真实GPU Smoke／恢复 | [smoke_gate.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/smoke_gate.json) | PASS | 两套优化器、阶段重置和恢复有效 |
| Tiny拟合 | 160步64目标 | Adam100%；SGD59.375% | Tiny成功不足以说明DEV泛化 |
| Main学习 | 固定1200步四格DEV | Adam通过；SGD有效但未通过 | 一层可行；普遍必要性未知 |
| 独立分析／保存 | 16状态、34文件、17,184读数 | PASS | 张量／优化器／计数／读数核验完成 |
| 最终身份／平台 | 36文件一致、两job成功 | PASS | 无源码漂移或重跑；非机制证据 |

“一定要开放四层才学得会这份中性任务”的强说法，被相同数据下的一层AdamW成功削弱。没有裁定纯容量极限、所有优化器失败或内部机制假设。SGD未达标也不能只归因漏更新Q/K/V，实际四张变化和保存已经核验；这套优化设置仍可能有限制。候选词集中依旧不能作为学会的替代标准。

## 9. 完整实验记录

2026-10-11（Asia/Shanghai）本轮：

1. 问题：最后一层Q/K/V/O在两套既有优化设置中是否有一套足以学会中性映射？
2. 设置：同一登记Base、四张权重、其他冻结；同一种子29和有限预算。两组只改变优化设置及学习率。
3. 训练：64目标独立Tiny训练160步，再独立Base重启，用2,400训练目标训练1200步；正式两组共54,400次答案呈现。
4. 测量：固定400条已见面板及800条DEV，分别报告未见顺序／未见组合；不读TEST，没有未暴露确认集。
5. 结果：两job和工程检查通过。Adam最终DEV800/800，四格200/200；SGD422/800，最低93/200。正式16状态和Smoke12状态登记；独立分析与最终36文件核验通过。A01仅更正Smoke合计240，恢复80不变。
6. 认识／边界／下一步：一层四投影AdamW是当前案例可学会的起点，比原四层范围更小。优化器／学习率、单种子和DEV暴露边界保留。事实汇报后停止；后续迁移／机制／分发均未做，等待研究者授权。

## 10. 解释

直接观测：一层AdamW满足全词表分项标准，且每个配对列表能按口令正确切换。推导：本次可训练参数是25,165,824四层范围的四分之一，是2,097,152单O矩阵范围的三倍。AI解释：在这份数据上无需开放四层，成功的一层路线也无需改数据。但这不能识别容量原因，历史范围比较还同时改变可训练位置及优化动态。两组新实验也同时改变学习率尺度、预条件和轨迹，不能说成功仅来自AdamW，或SGD无法学会。

## 11. 结论边界

能说：两组有限测试完成；本次AdamW设置下，只开放最后一层Q/K/V/O能够学会固定已见和DEV面板上的中性规则；本次SGD在1200步预算内未通过；所有规定输出和检查可用。

不能说：只Q/K/V就够、Attention关联参数全部训练、数学最小参数范围、纯参数数目或优化器家族因果作用、一层普遍足够、所有SGD失败、统计或未暴露确认、新模式迁移／干扰、专家分开收益或SAE机制。父问题的科学判断仍开放。

## 12. 下一步决定

已授权小测试和事实汇报完成。到此停止执行。研究者科学判断仍为`Unknown`；同向／反转迁移、参数机制、分发／分开训练收益、更多分组或种子均为`NOT_RUN`，需要后续授权。已有合格检查点是一项可用输入，不是后续实验的执行许可。

## 13. 产物清单

| 产物 | 作用／产出方 | 身份与完成 | 结论资格 |
| --- | --- | --- | --- |
| [Protocol](protocol_cn.md)及冻结快照 | 注册合同 | v1+A01；保留冻结原文 | 已授权范围；未用结果改设计 |
| [freeze.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/freeze.json)、[postexecution_freeze_verification.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/postexecution_freeze_verification.json) | root前后36文件绑定 | 全部一致，零偏离 | 工程来源 |
| [config.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/config.json)及实现复用清单 | 固定设置和检查源码 | §4精确SHA，未变 | 执行可复现 |
| [execution_certificate.md](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/execution_certificate.md) | 资源／image／command／计数 | 实际4H100reserved，两个独立worker | 执行证书 |
| [smoke_gate.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/smoke_gate.json)及恢复回执 | 真实Smoke／下一步恢复 | 两组两阶段PASS | 仅工程，无准确率门槛 |
| [smoke_terminal_status.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/smoke_terminal_status.json) | ACP完成 | pt-gwd1382k，SUCCEEDED | 平台，不是学会 |
| [full_platform_terminal_status.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full_platform_terminal_status.json) | ACP完成 | pt-8fizcddl，SUCCEEDED | 平台，不是学会 |
| [full_worker_qualification.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full_worker_qualification.json) | 实际worker完成 | 两exit0，固定160/1200 | 工程完成 |
| [analysis/results.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/results.json)、轨迹及训练呈现表 | 冻结分析器处理实际输出 | PASS；34文件、17,184读数、16反序列化状态 | 有边界的DEV测量 |
| [analysis/analysis_manifest.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/analysis/analysis_manifest.json) | 各成员身份和读数来源 | 列出预测／状态成员 | 精确产物来源 |
| [smoke_registration_receipt.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/smoke_registration_receipt.json) | 12状态／4族+分析族 | 共5IDs，选定strict访问PASS | 可用性，不是科学批准 |
| [full_registration_receipt.json](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full_registration_receipt.json) | 16状态／4族+分析族 | 共5IDs，选定strict访问PASS | 可用性，不是科学批准 |

检查点ID按`adapter_a17_04_single_attention_20261011t145214z_{smoke|full}_{attn1_sgd|attn1_adam}_{tiny|main}`命名；分析ID按`analysis_a17_04_single_attention_20261011t145214z_{smoke|full}`命名。每个回执链接本次strict访问快照。合计28保存状态、8个检查点族和2个分析族；不重复保存完整Base。所有adapter需要精确登记的Base。

## 14. 链接与复现

- 正式记录：[Anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor.md)、[Protocol](protocol_cn.md)、[Summary](summary_cn.md)。
- 执行：[目录](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition)、[运行](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z)、[源码](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/source)、[配置](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/config.json)；[日志](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/logs)、[检查点族](/data/250010109/MoE_Router/experiments/20261011_a17_single_attention_acquisition/runs/single_attention_20261011T145214Z/full)。
- Worker接口：`python source/diagnose.py --config RUN/config.json --run RUN --arm attn1_sgd --phase full`；这是复现文档，不是重复提交已完成job的许可。
- 冻结分析：在已检查运行环境使用`python source/analyze.py --config RUN/config.json --run RUN`；实际结果及分析器哈希在清单中。
- Jobs：Smoke `pt-gwd1382k`；Full `pt-8fizcddl`。均成功，无重试。后续迁移／机制／分发未执行。
