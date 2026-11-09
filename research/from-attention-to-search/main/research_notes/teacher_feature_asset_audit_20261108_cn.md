# 1108：教师特征与专家分发资产检查

**一句话结论：现有普通 8 层 MoE、其 33B-token 末层 router 输入 SAE，以及已有文本面板，可以支持晚期模型的初步“共享关系—实际路由”检查；最大适配缺口是这份晚期 SAE 在早期 checkpoint 上明显失真，尚不能据它解释早期 feature 语义或决定训练正则。**

本报告由 Codex 于 2026-11-08 核查。研究者要求中文报告，因此本件以中文交付。当前对话已由应用工具成功改名为“1108-教师特征与专家分发检查”，返回的对话 ID 为 `01a1b972-1cf6-73c0-a76a-bc70f258201f`。

## 阅读结论与完成范围

| 状态 | 本轮内容 |
| --- | --- |
| 已完成 | 上传组会稿；相关项目规则与目录；13 个相关对话的最近至多 10 轮；模型配置、checkpoint 清单、三份独立 SAE 的 CPU 严格加载及新算文件哈希；两种 Qwen CrossCoder 的权重形状和保存进度；router 源码；4 个 MoE checkpoint 的固定样本前向适配检查；数据面板行数与来源检查 |
| 已提出、未执行 | 正式共享关系与路由关联分析；跨文本案例统计；功能干预；续训三组候选比较 |
| 仍不能确定 | 11 月 6 日学长新观察对应的完整实验配置、原始曲线与日志；现有 SAE 各 feature 的稳定语义；同一 SAE 坐标跨训练时点的身份；路由对梯度信噪比或学习效率的因果作用；选定状态在未来实际运行环境中的完整恢复 |

本轮只在 CPU 上运行小样本前向。没有更新语言模型、SAE 或 CrossCoder，没有修改原始模型权重和正式训练配置，没有提交 GPU 任务。新代码、质量数值、失败日志和配置快照入口保存在[执行侧核查目录](/data/250010109/MoE_Router/experiments/20261108_teacher_feature_asset_audit)。

## 1. 来源、项目位置与规则

### 实际读到的材料

上传的[1106 组会稿](/data/250010109/MoE_Router/experiments/20261108_teacher_feature_asset_audit/sources/1106_组会勘误转写与总结.md)区分了逐字稿、摘要补充和用户补述。导师讨论提供研究直觉：把相关内容聚集给专家，可能提高有效信号比例，进而帮助长尾学习。但“噪声”依赖专家的学习目标，跨领域信息也可能有用。现有会议材料没有给出可直接测量的梯度信噪比定义，也没有完成“共享结构→路由→更新质量→数据效率”的验证链。

补读对话的范围是与本题相关的 13 个聊天，各取最近至多 10 轮，主题涉及 1030 资产审计、1031 checkpoint 管理、Dense 动态、双 SAE、共享成员、长短程、分层 MoE 和记忆蒸馏。**这是 10 月 30 日至 11 月 8 日相关上下文的定向回查，没有穷尽这 10 天全部聊天或所有长对话的更早分页。**确切对话名、ID、读到的轮次范围和未读分页保存在[阅读范围清单](/data/250010109/MoE_Router/experiments/20261108_teacher_feature_asset_audit/evidence/chat_review_scope.json)。聊天只用于找原始证据；历史训练授权不转移到本轮。

### 现有体系在哪里

| 位置 | 本题用途与权限 |
| --- | --- |
| [Research_System 规则](/data/250010109/Research_System/AGENTS.md)、[项目入口](/data/250010109/Research_System/PROJECTS.md) | 系统规则与导航；不是研究结果 |
| [from-attention-to-search 研究路线](/data/250010109/Research_System/Projects/from-attention-to-search/main/roadmap.md) | 本题相关科学记录的项目入口 |
| 项目 `main/focus/`、`main/problem_anchors/`、`main/experiments/` | 分别持有已激活问题、当前设计、实验协议与结果。此次不新建或改写这些科学身份 |
| 项目 `main/research_notes/` | 本报告所在的支持材料位置；候选方案不构成新实验批准 |
| [资产目录](/data/250010109/Research_System/assets/catalog.json) | 模型、数据、表示和 checkpoint 的唯一地址/身份登记；执行侧保存大文件 |
| [MoE_Router 执行根目录](/data/250010109/MoE_Router) | 代码、正式配置、日志、权重与本轮前向检查输出 |
| [学长仓库](/data/250010109/Research_System/Projects/Ruijun_Separable_Gating) | 只读学习参照；其中 SVD feature 的定义不能替代本题 SAE feature |
| [本对话记忆](/data/250010109/Research_System/.research/memory/conversations/1108-教师特征与专家分发检查/memory.md) | 本轮目标、核实结果、缺口与接续入口；不持有科学批准 |

规则要求研究者决定问题、机制判断与下一实验；Focus/Anchor/Protocol 各自持有问题、设计和执行合同，执行成功不代替科学接受。训练比较按有效预测 token 对齐，并保留初始化、样本顺序、有效 batch、优化器、冻结边界及恢复证据。后续若采用训练候选，先复用现有原生 MoE 数据/保存框架，再适配分析信号；拒绝直接复用旧 S7 联合训练入口或未经适配的 Qwen SAE 权重。

导航检查：通常模式发现 4 个已有入口未被 Git 跟踪；`--working-tree` 检查 167 项、0 个缺失入口，仍保留这 4 项“文件存在但未跟踪”的状态。本轮没有提交或推送。

## 2. 两套 8 层模型与 checkpoint

### 模型身份

这里的 Dense 和普通 MoE 都是本地从随机初始化训练的小模型；两者都不是把官方 28 层 Qwen 直接截成 8 层所得的相同权重起点。

| 模型 | 结构与实际参数 | 训练历史和用途 |
| --- | --- | --- |
| 原始 Dense baseline，登记 `model_dense_33b` | 8 层，hidden 1024，16 query heads／8 KV heads，head_dim 128；SwiGLU 中间维 3072；词表 151936，绑定 embedding/输出头；**281,431,040 参数**，无内置 SAE | 9 月 13 日原生轨迹，10B 后继续，约 22.019B 后换续训入口；适合作单独架构与表征参照 |
| 普通 Dense-order MoE baseline，登记 `checkpoint_family_moe_baseline_saved_20261104` | 8 层，相同 attention/hidden；每层 **8 个独立 SwiGLU 专家、每专家中间维 1536、top-2**；无共享 expert；**507,988,992 参数** | 10 月 31 日按原 Dense 参考数据流重新训练；沿用 10 月 30 日固定的随机初态，seed 17；未加载 Dense 训练权重或其 Adam 状态 |

MoE 参数实际清点为：非专家公共部分 205,933,568，专家部分 301,989,888，router 65,536。按“公共参数＋所有 router＋每层两个被选专家”的常用口径，理论激活参数为

\[
205{,}933{,}568+65{,}536+301{,}989{,}888\times\frac{2}{8}
=281{,}496{,}576.
\]

这个口径把完整绑定词表矩阵计入公共参数；它不是每个 token 实际访存量，也不是完整 FLOPs。Dense 的对应口径是 281,431,040。两者激活规模接近，**总容量不相等、初始权重不相同**。

### “30B”究竟是什么

这条普通 MoE 配置的 `unique_data_tokens=30,000,000,000` 指每轮可用的 DCLM token 前缀预算；训练进度 `tokens_seen` 指完成更新实际计入的有效预测 token。循环数据后，训练曝光可超过 30B。“33B checkpoint”表示累计 33,000,000,000 个有效预测目标，不是 330 亿参数。也没有在这些固定 milestones 中找到精确 30B 的权重；附近保存点为 29B、31B。

底层 DCLM 文件视图总量约 302.089B token，和语言模型本轮选用的 30B 前缀不是同一个规模。另一个名称中的 `Qwen3-30B-A3B` 属于其他模型命名，不能与本地训练曝光“30B”混用。

### 当前实际可读的保存点

| 对象 | 当前可读权重进度，单位为 B 有效预测 token |
| --- | --- |
| Dense 固定与历史保留点 | 0、0.5、1、3、5、10、15、17、19、21、**22.018691584**、31、33；19B 使用另存的 continuation checkpoint，原同名 milestone 权重缺失 |
| Dense 较新恢复点 | 34.076363264B／step 130000；日志曾达到 34.261436928B，日志进度不等于已保存状态 |
| 普通 MoE milestones | 0、0.5、1、3、5、10、**13.000238080**、15、17、19、21、23、25、27、29、31、33、35、37 |
| 普通 MoE 最新恢复入口 | 37.221773824B／step 142000；日志曾达到约 37.449052672B。本轮未查询平台当前运行状态 |
| Dense 仅存元数据的缺口 | 所查 13.000238080、23、25、27、29B milestone 的 state 已缺失；不能按目录名算作可加载权重 |

完整路径、manifest 哈希、实际/登记文件大小、缺失项和步数见[机器可读清单](/data/250010109/MoE_Router/experiments/20261108_teacher_feature_asset_audit/evidence/inventory.json)与[checkpoint 表](/data/250010109/MoE_Router/experiments/20261108_teacher_feature_asset_audit/evidence/checkpoints.csv)。例如双方 33B 都为 step 125894；13B 一项实际是 13.000238080B，不能抹平精确计数。

### 哪些条件对应，哪些不对应

当前双方共同有权重的同进度 milestones 包括 0、0.5、1、3、5、10、15、17、19、21、31、33B。相同进度不意味着完整训练史配对。

历史源代码与[采样器根因审计](/data/250010109/MoE_Router/experiments/20261031_dense_order_aligned_moe_baseline/analysis/20261104_sampler_root_cause/report_cn.md)表明：双方样本/目标 mask 顺序核实一致到 Dense **22.018691584B／step 84000**。其后 Dense 的续训入口把四参考流改成普通八 rank 采样；MoE 保持原四参考流。两者仍使用 DCLM，但后段分批、更新顺序和 epoch 尾部处理不相同。不能将 31B/33B 的差值全归因于 MoE。

Dense 和 MoE 虽都用 seed 17，架构与随机数消耗不同；MoE 专家独立初始化，没有复制已训 Dense。因此若研究“改变 MoE 分发是否有效”，优先从**同一个精确 MoE 状态**分三臂，Dense 只作另一条参照。

### 能否公平分叉恢复

本轮实际反序列化了双方 33B 的 state：都有 `model`、Adam `optimizer`、`scheduler`、`optimizer_step`、`tokens_seen`、`epoch`、`batch_in_epoch`、`extra_training_state`。Dense Adam 有 90 个参数状态，MoE 有 266 个；两者 scheduler 都保留更新计数与当前 LR 3e-4。MoE 还保存四条 lane 的样本游标和下一批 ID。

双方的逐 rank RNG 文件也实际读取成功，包含 Python、NumPy、Torch CPU、Torch CUDA 和 generators；Dense 8 份，MoE 4 份。[RNG 内容入口](/data/250010109/MoE_Router/experiments/20261108_teacher_feature_asset_audit/evidence/rng_schema.json)。原 MoE 工程记录有独立进程重启对照 PASS，但**本轮没有把精确 33B 状态恢复为训练进程，也未验证换卡数/新版代码后的等价恢复**。结论是“保存内容支持以后资格检查”，不是“任意环境可无条件精确续训”。

官方 Qwen 的公开权重则没有本地原始预训练 Adam、调度器、RNG 或数据游标；它不能提供同等级的原始预训练恢复。

### router 的输入、选择与权重能否取得

可以。原生 [SparseMoE.route](/data/250010109/MoE_Router/experiments/20261031_dense_order_aligned_moe_baseline/moe_baseline/model.py:211) 接收同层 norm2 输出，线性层为 `1024→8`，无线性 bias。先求 FP32 softmax 概率，再在 **概率＋保存的 load bias** 上选 top-2；给专家的真实权重取两个被选 expert 的**原始 softmax 概率并重新归一化**，不是对加 bias 的分数归一化。保存 logits、原概率、bias、所选 ID 和最终权重即可重建实际决策。

没有始终激活的共享 expert，也没有容量截断；代码执行全部选中 assignment，训练统计明确记录 `dropped_assignments=0`，并检查 assignment 总数＝有效 token×2。load bias 每个完整更新按全局负载以 `0.001×sign(目标接收量−实际接收量)` 更新；没有辅助均衡 loss。静态前向使用 checkpoint 的已保存 bias，并保持冻结。本轮前向检查已实际取得该位置并断言 bias 不变；历史完整统计入口在正式 run 的 `metrics.jsonl`，不需要假设存在另一个路由器。

## 3. SAE／CrossCoder 对应关系

### 三份独立 SAE

三者都实际通过 CPU 原生 `TopKSAE.from_pretrained` 严格加载，重新计算了完整 SAE 文件 SHA256，并与保存记录一致。每份都是 61,471,024 个参数，编码 1024→30000，解码 30000→1024，ReLU 后保留最多 32 个正坐标。**字典之间的 feature 编号互不对应。**

| 资产及父模型 | 准确层位与重建对象 | 训练量与历史质量 | 适用性 |
| --- | --- | --- | --- |
| Qwen E16 MLP 输入 SAE；父模型为官方 **Qwen3-0.6B-Base，28 层** | 零起算 block 27，即第 28 层；`model.layers.27.mlp` 的实际输入，已过 `post_attention_layernorm`；重建 MLP 输入 | step 244141，**1,000,001,536 原始激活位置**；验证归一化 MSE **0.053382**，平均 L0=32；训练期间 30000 坐标均曾使用；原 reload 差 0 | 用于本父模型该接口的成员、幅值和共现分析；不能用于 8 层 MoE，也不是普通 Dense 的 SAE |
| Qwen Attention 输出 SAE；同一官方 **Base** 父模型 | 零起算 block 27；`model.layers.27.self_attn.o_proj` 输出，已做输出投影、**尚未加 residual**；重建 raw attention write | step 244380；**1,000,980,480 原始位置**、1,000,002,960 有效预测目标、999,025,471 筛选后 SAE 位置；验证全局归一化 MSE **0.168419**，rank 均值 **0.165243**；L0=32 | 分析 attention 分支写入；不等于 MLP 输入或整层 residual。和 E16 的误差差别不能解释成同一对象的优劣 |
| 普通 MoE gate-input SAE；父模型为上述 **8 层普通 MoE 精确 33B** | 零起算 block 7，即第 8 层；`blocks.7.norm2` 输出＝`blocks.7.moe.router` 的实际输入；位于线性 router、softmax 和 load bias **之前** | step 244141；**1,000,001,536 原始位置**、998,050,956 筛选后位置；全局归一化 MSE **0.226745**，rank 均值 **0.226163**；L0=32；训练期间 30000 坐标均曾使用 | 最直接支持同层、同位置的 SAE—路由关联；跨 checkpoint 风险见第 4 节 |

训练都使用已有 DCLM paired 视图、Qwen tokenizer、1024-token 窗口，按位置范数剔除高端约 0.1%（离散窗口中实际比例可稍高）。输入不先单位化，也不先减 decoder bias；encoder 直接处理该 hook 的向量。训练时 decoder 字典列归一化。重建损失是平方误差除输入能量，并有 AuxK；它不是 L2 正则化模型权重。不能将不同文档中的 rank 均值与全局 token/能量归约混写成一个数。

本轮 SAE 权重与历史质量入口：

- [Qwen MLP SAE](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/sae_full_final.pt) · [原完整训练记录](/data/250010109/MoE_Router/experiments/20260903_a15_13_e16_dclm_final_layer_sae/runs/full-20260903T150734Z/full_summary.json)
- [Qwen Attention SAE](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/full_20261009T182142Z/sae_full_final.pt) · [原质量记录](/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/runs/full_20261009T182142Z/summary.json)
- [MoE gate SAE](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/runs/formal/sae_full_final.pt) · [正式配置](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/configs/formal.json) · [原质量与路由保真度](/data/250010109/MoE_Router/experiments/20261104_moe_gate_input_sae_33b/runs/formal/summary.json)

这些 final SAE 都是字典权重导出，不能仅靠它恢复 SAE 优化器；完整训练恢复对象另存。官方父模型实际权重头计数为 **596,049,920 参数**。两个本地 Base 地址的 config 与 tokenizer 五类文件本轮逐字节哈希相同；本轮没有重新哈希这两个约 1.19GB 的父模型权重，因此没有把“tokenizer 一样”升级为“父模型权重已新证同一”。Attention SAE 的保存合同另有明确父模型权重 digest；E16 历史缓存的父模型指纹缺口仍保留。

### CrossCoder 不是“每层各一个独立 SAE”

CrossCoder 把同一文本、同一位置在多个层的向量联合编码成**一份共享激活向量**，再分别重建各层。后层也参与编码，所以早层 decoder 上有贡献不意味着某个 feature 在早层已能独立读出。

| 真实资产 | 联合输入 → 编码 → 重建 | 训练/质量与当前访问 |
| --- | --- | --- |
| **Qwen A22，已完成的 14 层 CrossCoder** | Base 模型零起算 **1,3,5,…,27** 共 14 层的 `block residual-post`，最后一层取最终全局 norm 之前；`[N,14,1024] → [N,16384] → [N,14,1024]`；参数 **469,792,768** | 保存位置曝光 **999,997,440**。BatchTopK 训练目标均值 L0=256；推理使用 TRAIN 拟合阈值，不是每 token 硬取 256。完整 10,485,760 验证位置实测 L0 **254.539**，零命中比例 **1.770%**。本轮 CPU mmap 解包和形状检查成功；没有重新完成端到端前向或训练恢复 |
| **Qwen A23，全 28 层 CrossCoder，部分训练** | Base 模型 blocks **0–27** 的相同 residual-post 接口；`[N,28,1024] → [N,32768] → [N,28,1024]`；参数 **1,879,109,632** | 原登记固定 274,976,768 曝光副本缺失。找到原运行 `latest.pt`，实际 header 为 step **67133／274,976,768 位置**，形状匹配，CPU mmap 可解包；旁边日志到 282,214,400 位置，不代表该进度已保存。未重算 22.55GB 全文件哈希；mutable 路径不提升为原固定副本。另有已登记约 0.1B 固定点可读。不能称“全层 1B 已完成” |
| **Dense A24 时间 CrossCoder，补充区分** | 普通 Dense **1B、5B、15B、31B** 四个 checkpoint，各 8 层，合计 **32 个 checkpoint×层空间**，hidden 1024、共享 F32768；不是 Qwen 28 层工具 | 当前保存入口记 774,934,528 位置曝光，日志到 787,251,200；本轮只读入口，没有重新加载此大工具。32 个空间是同一配对位置的观察，不是 32 个独立样本 |

A22/A23 使用各层 TRAIN 均值中心化，再除各层向量 L2 RMS；统计量与阈值随字典保存，不能换成普通 RMSNorm 或逐向量单位化。数据来自 DCLM direct bins：训练约 1B 配对位置、9 个文件，验证 10,485,760 位置、1 个保留文件；文件隔离不保证原始文档或近重复隔离。

A22 原替换检查在 32,694 个预测目标上：原 NLL **2.880745**，最后层重建后 **3.186707**，增加 **0.305962 nat/token**。因此已有码重建质量与行为影响记录，但不构成 feature 功能或路由收益证明。登记中的 `measurement_quality=UNKNOWN` 仍保留，不能把“工程训练完成”当作研究者已认可质量充分。

[A22 固定权重](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt) · [完整验证](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/validation_000999997440.json) · [替换保真度](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/replacement_fidelity.json) · [A23 原运行保存入口](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/recovery_20261015/a23/run_retry_01/latest_checkpoint.json)。

S7/fresh S7/SALL 还属于另一族 **8 层 Dense 主干＋训练时 SAE 重建辅助损失**。fresh S7 的 SAE 读最后层 Attention 输出，历史重建系数 0.1，从第一步影响主干；它不是普通 MoE，也不是这里新训的 gate-input 字典。SALL 是八个旁路 SAE。相同 hidden 1024 不能使这些字典通用。

## 4. 晚期 SAE 对早期 checkpoint 的实际适配检查

**结论：接口一致，早期表示分布却不一致。1B 和 15B 上不宜直接把 33B 字典解释成可靠语义测量。**31B 比这两个时点接近训练父模型，但仍明显劣于 33B。

本轮固定 MoE 33B 字典，在同一普通 MoE 轨迹的 1B／15B／31B／33B 上检查。架构均为相同 8 层/1024 维，hook 均为 block 7 的 norm2 输出；相同 tokenizer、同一输入 ID、相同预处理。挂钩取得的 norm2 输出与线性 router 实际收到的输入、生产者的快捷提取函数，四个 checkpoint 上最大差均为 **0**。

样本是已有 DCLM 验证文件偏移 0、16384 开始的两个固定 1024-token 窗口，每个 checkpoint **2048 个原始位置**。按每窗 0.999 范数分位筛选后为 **2044 个位置**。这是两段已暴露验证文本的工具检查，没有独立确认地位。模型保留原 FP32 权重与 FP32 load bias，在 CPU BF16 autocast 下前向；SAE 以 FP32 计算。该执行层与历史 CUDA 训练评估存在数值差异，因此采用本次四点的内部比较，不要求复刻历史指标每一位。

归一化误差为全部合格位置的重建平方误差总和／输入平方能量总和，零向量重建基线为 1。中心化解释方差为 `1−重建误差平方和／面板中心化方差总和`，小于 0 表示比本面板均值常数重建还差。它们不是同一个指标。

| 模型进度 | 能量归一化 MSE↓ | 中心化解释方差↑ | 输入 RMS | 正激活均值 | 平均 L0 | 面板命中坐标数 | 重建前后 top-2 集合完全相同↑ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1B | **0.9717** | **−0.0733** | 1.0908 | 3.6622 | 32 | 13231 | **23.58%** |
| 15B | **0.6281** | 0.2338 | 1.0229 | 3.2684 | 32 | 11969 | **39.68%** |
| 31B | **0.3161** | 0.5961 | 0.9892 | 2.4425 | 32 | 11692 | **77.25%** |
| 33B | **0.2252** | 0.7159 | 0.9893 | 2.5853 | 32 | 11751 | **83.81%** |

未过滤位置的完整结果、激活最大值、命中次数分位数、路由概率 L1/KL 和逐点耗时见[完整适配数值](/data/250010109/MoE_Router/experiments/20261108_teacher_feature_asset_audit/evidence/adapter_results.json)。面板未命中某个坐标不能称其全局死亡；L0 恰好 32 是 TopK 机制约束，不能当作语义稀疏性已确认。1B 命中坐标更多也不能解释成语义更丰富。

原父模型 33B 的历史验证 top-2 集合一致率为 **82.63%**、slot overlap **91.28%**；两者分母不同。重建不是实际分析时必须执行的干预，这个检查测的是字典保真度，尚未检验 feature 对行为的因果作用。

**AI 建议：**先在精确 33B 上检查现象；需要跨时点时，先考虑 31B 并单独做目标文本的质量检查。若研究必须从 1B/15B 开始，可候选地为早期 checkpoint 训练新 SAE，或先直接比较原生 hidden/router、同 token 路由与表示几何。本轮没有训练任何新工具。即使重建合格，也仍需检验 feature 身份是否稳定。

## 5. 数据可复用性

| 现有数据与实际入口 | 规模、来源和构造 | 可以复用什么；风险 |
| --- | --- | --- |
| [S06](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/data/panel.jsonl) | **384** 条英语构造前缀；动物/交通等标签及模板家族；16 个 frame、原 8/8 发现/保留划分 | 适合解释粗细类别、词面与共同后缀下的成员变化。已经反复看过，模板家族相关；不能作新的独立测试，也不足以作通用续训语料 |
| [S11](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S11_four_domain_relative_frequency_1105/data/controlled_panel.jsonl) | **4608** 条；96 家族，开发 1536/确认 3072 条；英语显式/改写/属性等构造 | 可复核原 16 项判定与共享/非共有口径。原确认集已暴露；不能重划后称独立确认 |
| [S13](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/data/controlled_panel.jsonl) | **6912** 条；72 家族/24 场景簇；开发 2304/确认 4608，24 标签×4 表述；原确认48家族/16簇 | 有明确粗参照和同父细类对。适合复用解释结构，但现已用于选择、检验和展示。原独立性的历史身份保留，本轮复用不重新获得独立性 |
| [S08 自然题干](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/data/panel.jsonl) | **771 篇，3×257**；Magicoder problem/train、GSM8K question/train、MMLU question/**test**；规范化精确去重，前128 token，8个分位读出；原生源 ID、revision、文件哈希齐备 | 最小真实文本路由检查的现成候选。以英语为主，代码/换行/长度差明显；来源组不等于纯语义领域。近重复未排除；MMLU test 来源应留在分析/评估，不能顺手并入续训 |
| S11 的 Q/G 参考缓存 | Q 为三来源各2000题干，共6000；G为6000篇DCLM；指定末尾冒号位置的 Top32 频率 | 可复核原 Qwen 坐标的参考频率；**不能直接当作 MoE SAE 坐标频率**。同样的文本可重读，频率必须用 MoE 原生字典重新计数 |
| [DCLM paired 视图](/data/250010109/training_data_views/dclm_pair_v1/manifest.json) | uint32 预分词；训练 **2419 文件／302,089,493,820 token**；验证单独文件 **114,988,106 token**；原始来源为既有 `/data/share/109_cache_dir/hf_data/dclm_bin` | 与两条8层模型及三SAE的 tokenizer 兼容。适合未来普通续训与通用 NLL 参照；具体语言比例未做全面识别，固定小验证前缀已反复使用，原始文档/近重复去污染未知。LM 当前只循环30B前缀 |
| [R15 自然文本面板](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R15_20261102_natural_phenomena_output_geometry_v1/report_cn.md) | 相关对话与原记录记 **600 篇网页／557 网站**、76800位置、300/150/150篇分拆 | 可作为另一现有文本来源候选；关键词来源组不是人工学科标签。原 Qwen 表示/CC 缓存不能当 MoE 表示；本轮未重新取得 MoE 前向 |
| [A15_31 分层短训数据](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_31_depth_expert_allocation/R01_paired_token_frequency/summary_cn.md) | 原67,108,864-token小前缀，经处理约65,766,910 token；训练约229M目标，循环约3.48遍；测试544文档/700307目标 | 已有低/中/高频监督计数及负结果。低频是子词目标代理，不能替代长尾事实；不宜把此小循环集当充分通用续训设计 |

S06/S11/S13 的“共享”首先是外部类别/模板设计，再测指定位置的 SAE 交集或激活差异。S08 的“共享”是同数据来源下更高的成员重叠；两者不能混作一个语义真值。原记录中，S13 显式条件细类共有成员平均参考频率较低有 32/32 项冻结支持；**非共有成员**的等权比较没有统一低频规律，动物 8 项差值区间均跨零。开发集类别偏向加权与所有非共有成员等权是不同估计对象。本轮不重判 S11，也不把这些 Qwen 结果外推到 MoE。

现有小面板的主要价值是分析与评估。用于训练会有重复暴露、模板记忆、规模不足、测试污染和通用能力受损风险。未来训练应另确认自然文本流及未用于调参的验证材料。现有八任务/旧 SFT 也含已暴露或官方 test 来源重分割；不能称新独立测试。本轮没有换数据、构造大数据集或训练。

## 6. 学长记录及此前分层实验，应怎样接起来

找到了已有归档 [0903 feature.pdf，37 页](/data/250010109/Research_System/daily_research_reports/backup/2026/09/0903/docs/feature.pdf)，并读取文本；首页两张图也直接检查了原图。另读了 [0813 feature (1).pdf，10 页](</data/250010109/Research_System/daily_research_reports/backup/2026/08/0813/meeting_notes/feature (1).pdf>)。它们是多日期、多署名、多实验汇编，**文件所在日期不能当作每项实验日期或同一配置身份**。

| 记录 | 实际展示/实现 | 必须保留的边界 |
| --- | --- | --- |
| 0903汇编 p1，标记2026/09/02 | 图例为 **Llama2-7B-ffn-lora-moe** 与 offline-router；800 step 图读数约0.3926/0.3841，八任务简单平均27.81/30.09；文字报告专家相似度下降 | 没有完整 seed、token 预算、精确底座、teacher版本、分组算法、LoRA rank/top-k/插层和评测合同，不能称已复现；800 step不是800 token |
| p2–3 SAE 层级观察 | 30000 个1024维向量、每位置32个；组合节点与domain区分、叶节点与PCA方向的观察 | 不足以把这些1024维SAE与p1的7B训练链逐项绑定；图层级不是模型深度，重构可用也不推出局部数据流形已证明低秩 |
| p5–6及p18的层级尝试 | 去掉粗类判别分量再细分，记录loss变差或不优于baseline；给出不同粗类复用同一细维度的反例 | 失败结果不能被首页正结果覆盖；PCA大方差并不自动等于粗语义方向 |
| p29–30的合成模型 | 3层Transformer、2父×2子；8000步预训练、1500步粗路由、2000步细路由；oracle改善分发，末层聚类标签未明显帮助，去粗方向的margin增量约0.000052且区间跨零 | 与p1的7B真实数据实验、p30后的Qwen3-30B-A3B探针均是不同实验 |
| 本轮上传1106口头报告 | 报告“教师feature指导分发的收益更偏低频”，并讨论信噪比 | 尚缺那次频率分桶、主指标、样本量、teacher/student和原曲线；不能由旧PDF或本地0.6B配置补齐 |
| 我方 A15_31/R01 | 同参数总量、每token top-2；均匀8×8专家对6,6,6,8,8,10,10,10分配；各229,113,856有效目标 | B−A低频NLL **+0.217210**，整体 **+0.014258**；本配置/预算下B更差。单seed、低频子词代理限制外推；不能先把失败归因为信噪比 |

另一个学长仓库中的 [feature-grained 说明](/data/250010109/Research_System/Projects/Ruijun_Separable_Gating/017_feature_grained_moe_logic.md)把 feature 定义为权重 SVD 的方向/投影。它提出 token 含多 feature、token 路由不等于 feature 独立路由，这对本题有启发；但它的 feature 不是这里的 ReLU-Top32 SAE 坐标，不能混用频率、语义或结论。

目前仍缺**11月6日所说那一次教师指导学生分发的完整实验记录**。以后提供该记录时，应按实验/页面分别补齐身份，保留负结果。此次找到的旧汇编提供历史背景，不代替新实验合同。

## 7. 一个最小“共享关系—实际专家分发”候选方案

以下是 **AI 建议，尚未执行正式分析，也不是训练 Protocol**。先只用普通 MoE **精确33B**及其原生 gate-input SAE，在最后层回答一个描述性问题：**跨文本很少一起出现、或偏向不同来源的两个可靠成员，是否对应相似的实际专家接收分布；这种重合是否超过负载、频率和词面条件所能解释？**

### 共享要先分清对象

| 定义 | 实际计数 | 能说明什么 |
| --- | --- | --- |
| 同 token 共同激活 | 同一位置两个 SAE 坐标均为正；报告边际频率和校正后的共同出现 | 局部组合/背景共现；不等于语义相同或彼此功能依赖 |
| 同类文本都出现 | 按文档记每个成员是否在固定位置集出现，再在指定来源/类别内比较 | 文档级关联；受长度、格式与读取位置影响 |
| 跨数据组稳定出现 | 各组分别统计成员出现率，在家族/文档层面给稳定性与支持数 | 分布层面的共享覆盖；不能仅据“多个组出现过一次”命名通用概念 |

最小方案采用**文档级出现关系**作为主要共享定义；同时单列同 token 共现和来源分布。低共现不等于互斥，支持不足不填0。类别差异可以来自同一坐标强弱变化，二值成员不覆盖全部差异。

### 输入与样本单位

1. 复用 S08 的 771 篇真实题干，每篇前128 token、同样8个正文分位位置，冻结文本ID、SAE文件哈希、零起算layer7和读取规则。原Qwen缓存只作历史参照，**重新取得MoE表示与路由**。
2. 先审核正文/近重复与来源，再按整篇文档/重复簇分配“候选选择部分”和“固定规则复查部分”。由于这些材料已暴露，两部分都称探索性复用；不叫新独立测试。
3. 每个观测行保存 checkpoint、文档ID、来源、token ID/piece、绝对/相对位置、可见前文、输入范数、SAE索引/值、线性logits、原始softmax、bias、实际top-2与归一化权重。推理时冻结load bias。
4. 独立不确定性单位是文档或重复簇。一个文档8个位置、一个位置32个成员和2个expert，不能乘起来当独立样本量。

在选择部分只保留至少20篇文档有正激活的成员；这个数是可审核的初始建议，不是已确认科学阈值。固定最多6对“低文档共现”候选和6对频率/支持数接近的“高共现”参照。若没有足够支持则报告不足，不降低门槛救结果。候选数量、低/高分位与匹配容差在执行前冻结。

### 怎样统计专家，而不误称 feature 被独立路由

对某个位置，把实际被选两个专家各记质量1/2，得到总和为1的8维接收向量；另以真实gate权重作敏感性分析。某个 feature 出现时，汇总这些**整 token 的接收向量**，形成该 feature 条件下的专家接收分布。

同一位置若激活32个成员，它们都会关联到同一份token路由；这只是共同观测，不能拆成32次独立路由决策。feature对的“去同一expert倾向”可用两成员在**不同文档中的出现位置**接收分布内积描述，并同时展示每个expert的接收量与区间。该数衡量条件接收分布重合，不衡量独立feature分配率。

### 随机参照必须保留什么

- 固定整行 SAE 激活，保留每位置的多 feature 共现；将完整的“top-2 ID＋权重”向量在不同文档位置之间置换。不能独立打乱两个expert槽，也不能独立打乱32个feature。
- 主置换在 token ID、上下文长度/位置和输入范数的可支持分层内进行，保留top-k和分层专家负载。相同token过稀、分层过细无法交换时报告覆盖不足，不靠合并产生虚假确定性。
- 另做来源组内置换，回答“超出来源本身路由差异后还有多少关联”。这是更强条件下的另一个估计对象，可能消掉本来关心的组间结构，必须与主结果分开。
- 低/高共享候选之间匹配 feature 边际出现率、有效文档数和激活规模；以文档/重复簇成对 bootstrap 给区间。多候选同时判断时报告多重比较规则，不只选漂亮pair。

置换能检验指定条件下是否超出机会重合，**不能创造随机分发干预，也不能证明feature导致路由**。router与SAE同读一个hidden state，残余关联仍可来自未控制的表示因素。

### 主要交付与反例

先给“3个来源×8个expert”接收图，再给每对固定候选的文档支持、共享程度、专家分布和相对置换的差值。最先展示真实全文片段：例如 S08 的一道代码题与一道数学题，在匹配token/位置后，各自哪些MoE成员激活、实际选了哪两个expert。**现在还没有这类MoE实测案例，不能用旧Qwen feature号填充。**

固定展示：低共享且同expert、低共享但不同expert、高共享却不同expert三类；按选择部分预先约定的普通/边界例规则选例，不按复查部分的效果挑选。再用S13中实际“animal/cat/dog”文本作可读性补充，注明模板和末尾冒号影响。

若差值未超过参照、只剩格式/词面效应、换读取位置就消失，或字典质量/成员支持不足，则缩小或放弃该路由现象。观察到稳定重合也只允许说“条件接收分布相似”。一个expert可以有足够容量处理多个不同feature，跨组共享还可能有用；所以仍不能称错误分发、梯度干扰或效率下降。下一步需匹配expert功能干预或更新/续训对照，测主任务损失与保持；若要谈信噪比，还要先定义目标梯度、信号均值和扰动方差。

### hook距离怎样处理

本候选的SAE输入与同层router输入完全同点，已经实测最大差0，因此无需猜测中间变换。若改用Qwen Attention SAE，Attention输出之后还要经过残差相加和norm2；它与MLP输入之间的关联不能被称为同一张量上的直接分发。若改用residual-post CrossCoder，已经包含本层FFN输出，甚至用到后层联合信息；与本层路由的关系可能含下游/后层信息，不能拿它当路由前已可用的独立feature。

## 8. 后续续训候选对照

**当前不选最终正则公式，也不启动任何一臂。**若现象在合适字典和参照下仍值得研究，建议最多保留下列三臂，从同一精确 MoE checkpoint 分叉：

| 候选臂 | 改变什么、回答什么 | SAE是否进入训练 |
| --- | --- | --- |
| A 普通续训 | 保持原LM目标、router及load-bias更新；测同一模型多见这段数据后的自然变化 | 只作冻结分析工具 |
| B 结构信号续训 | 只加入一种已定义、可证伪的feature关系指导；具体选择“分发目标”或“关系约束”之一，待审核 | 若进入目标，固定字典/teacher、输入位置、有效mask、尺度与系数，明确梯度只到router还是也到主干 |
| C 结构打乱参照 | 打乱指导关系/目标与输入的对应，同时尽量保留目标质量、熵、负载、幅度、有效位置和更新强度，区分结构内容与额外训练信号 | 与B相同的teacher提取和梯度范围 |

**仅把expert编号做一个全局置换往往只是标签重命名，不是有效随机结构对照。**C应破坏所要检验的输入—结构关系，并保留可匹配边际；不能按训练结果反向调强度或挑最好随机映射。

共同条件包括：同一模型/Adam/scheduler/RNG/数据游标、相同后续有序样本与目标mask、有效batch/token预算、专家容量和top-k、均衡机制、裁剪、保存/评估规则，以及相同验证与通用保持集。B/C的teacher前向、缓存和附加损失成本单列；数据效率与总计算效率分别比较。Dense不进入这三臂的共同初态定义。

分叉进度仍待研究者决定。若在31B或33B检查现象，结论只约束晚期；若必须研究早期学习，应先解决早期字典/测量问题。使用晚期训练字典监督早期模型还是一种引入额外teacher先验的处理，不是中性的“同feature追踪”，必须单独说明其信息来源与成本。

若没有可靠路由现象，先停在描述性结论或改用不依赖SAE的原生hidden/router对照；若字典失配，先修测量工具或改检查时点。均不自动进入训练。已有A15_31负结果也不授权继续堆架构。

## 9. 下一次需要研究者确认的事项

按依赖顺序：

1. **补齐/指定学长11月6日那次实验记录。**需要对应页面、teacher/student、checkpoint、数据及分桶、损失定义、实际top-k/共享专家和原曲线；旧归档是否就是拟引用对象也需明确。
2. **是否先在普通MoE精确33B执行第7节的有界观察。**我的建议是先用原生gate SAE与S08真实文本，保留S13作直观补充。当前只交方案，未运行。
3. **本轮主要“共享”采用哪一种。**建议先用文档级出现关系，同token共现和跨来源稳定性分别报告；频率、强弱和二值成员不要混为一个量。
4. **长尾的对象与下一判据。**是参考语料低频SAE成员、训练低曝光子词，还是实体/关系？这些选择影响“效率”终点，不能互代。
5. **只有现象可靠后，再确认续训起点、监督位置、梯度范围及随机参照。**同MoE分叉优先；早期若用晚期teacher，先接受其额外先验这一处理定义。
6. **未来训练与独立评估用什么材料。**已看过的S06/S08/S11/S13只作探索/开发；官方test来源不得混入训练。自然文本流、去重单位与通用保持评估另行冻结。

核查脚本、固定样本身份、配置/日志来源、文件哈希、已知失败与未做的检查见[证据索引](/data/250010109/MoE_Router/experiments/20261108_teacher_feature_asset_audit/evidence_index_cn.md)。本次实际质量数值和来源作为 `analysis_teacher_feature_asset_audit_20261108` 追加到既有资产目录，[输出访问检查](/data/250010109/Research_System/assets/checks/2026-11-08_teacher_feature_asset_audit_outputs.json) strict 通过。没有保存新模型权重或可复用激活缓存。原始记录、S11历史判定、各Focus/Anchor与已批准实验状态均保持原有权属。
