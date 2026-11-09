# 旁路 C/T 各50B：训练交接与脚本复用

> **SUPERSEDED（挂点、条件与资源安排）：**导师讨论后的新要求改为Attention纯分支归一化后接SAE，且先确认两模型架构才允许Smoke。当前唯一续接入口为[05架构确认提示词](05_attention_branch_sae_architecture_confirmation_prompt_cn.md)。以下旧C/T直接提交指令不可执行，仅保留来源与历史。

2026-09-16；依据研究者本轮直接指令整理。**最新执行分工：本任务只固定memory和实施plan；实际审查、修正、GPU Smoke与正式提交由研究者另开的5.6 Sol High任务实施。本任务未提交任何GPU作业。**

**已明确授权的资源/预算：先一个2×RTX5090 Spot作业完成旁路配对Smoke；通过后直接提交两个独立的8×RTX5090 Spot正式作业，每个50B有效预测词元，总100B。无需重新询问是否提交。**正式作业提交后仅做短启动检查，不持续监督、不部署监控循环。Smoke必须确认终态验收通过，不能提交后就假设通过。

研究者已明确“是继续做8层”：规模固定为8层hidden1024/30000维Top32；不再等待规模选择。执行契约见[本轮protocol](../../../../experiments/A15/15_17_three_model_sae_representation_trajectory/supporting_records/sae_pretraining/sidecar_8l/20260916/protocol.md)，新包为 `/data/250010109/MoE_Router/experiments/20260916_sae_sidecar_8l_pair_50b`。当前正式提交以执行记录为准，记忆和本交接文件不证明作业已运行。原G0/G1文件保持不变；本次明确50B授权替代旁路开发预算及等待G1信号的旧候选限制。

## 0. 当前进度与新任务第一步

- 已完成：旧记忆/真实脚本地址提取；八层C/T实施契约；隔离代码草稿；27项本地回归通过，C/T各一次双rank CPU归约检查通过；旁路梯度归属与完整状态恢复检查通过；2卡Spot提交dry-run已解析成功。
- 未完成：新实现独立冷审、GPU Smoke、2卡真实恢复/日志验收、八卡启动检查、两组50B提交。**无Smoke job ID、无正式job ID。CPU PASS不替代GPU Smoke。**
- 准备代码位于 `/data/250010109/MoE_Router/experiments/20260916_sae_sidecar_8l_pair_50b`，这是待审查草稿，不是已验收正式训练包。`audit/frozen_source.json`是准备快照，修正后必须重新冻结，并保留旧版本与差异。
- 保留的准备失败：首次测试因未复制`prepare_paired_data_view.py`中止收集；第二次5个CLI测试仍引用旧四H100配置而失败；适配fixture后27项通过。它们均发生于本地，不存在失败GPU提交。日志为`checks/local_tests.log`；不要把早期失败说成GPU故障。
- 新任务首先冷审代码复用差异与所有提交守卫，确认没有别的任务已提交同一run；继承现有明确授权后推进，不重复询问八层、各50B和Spot选择。

新草稿入口：

| 项目 | 绝对路径 |
|---|---|
| 实施/训练契约 | `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/supporting_records/sae_pretraining/sidecar_8l/20260916/protocol.md` |
| 双卡配对Smoke脚本（待GPU验收） | `/data/250010109/MoE_Router/experiments/20260916_sae_sidecar_8l_pair_50b/scripts/run_pair_smoke.sh` |
| 八卡正式脚本（待Smoke后调用） | `/data/250010109/MoE_Router/experiments/20260916_sae_sidecar_8l_pair_50b/scripts/run_formal.sh`，参数`C`或`T` |
| 两卡配置 | `/data/250010109/MoE_Router/experiments/20260916_sae_sidecar_8l_pair_50b/configs/smoke_2x5090_C.json`、`smoke_2x5090_T.json` |
| 八卡配置 | `/data/250010109/MoE_Router/experiments/20260916_sae_sidecar_8l_pair_50b/configs/formal_8x5090_C.json`、`formal_8x5090_T.json` |
| 当前本地检查 | `/data/250010109/MoE_Router/experiments/20260916_sae_sidecar_8l_pair_50b/checks/gradient_contract.json`、`resume_replay.json`、`local_tests.log` |
| 待产出的Smoke证据 | `/data/250010109/MoE_Router/experiments/20260916_sae_sidecar_8l_pair_50b/runs/smoke_pair_2x5090_v1/pair_verification.json` |
| 两个正式输出位置 | `/data/250010109/MoE_Router/experiments/20260916_sae_sidecar_8l_pair_50b/runs/formal50b_8x5090_C`、`formal50b_8x5090_T` |

**冷审重点：**源模型新增明确`sidecar`分支及正确采集挂点；trainer的旧H100/串联T约束已适配但需逐条核验；Smoke的torchrun退出码1必须同时有计划退出75的完整持久收据，不能一律当成功；正式脚本须检查Smoke PASS及源配置哈希。另检查旧TensorBoard审计对大token计数的浮点精度：JSONL/checkpoint整数为权威，不能在50B把float32 scalar取整要求逐token相等。若需修正只能修审计表达，不改实际计数。补上全rank配对流摘要更稳妥；现有pair脚本明确只检查rank0流摘要，不能把它声称为全rank证据。

独立理解与冷审预留30–60分钟；必要修正和本地复核候选半天内完成，GPU Smoke耗时以新硬件首步实测为准，不用旧H100吞吐保证5090时间。新任务不需先完成所有梯度/参数分析才允许Smoke。

## 1. 新任务可直接使用的指令

你是研究者新开的5.6 Sol High执行任务。请在 `/data/250010109/Research_System` 接续旁路SAE的配对50B训练。先读本文件、同目录 `04_sidecar_50b_reuse_manifest.json`、`/data/250010109/Research_System/.research/memory/conversations/0914-training-excution/memory.md` 全文，再读 `docs/training_reuse_index.md`、`docs/training_observability_contract.md` 和 `docs/execution_envelope.md`。

模型固定八层，按新protocol和新包继续。既有规模、资源与预算不重复申请；先核查是否已有作业，避免重复提交。

两个条件都是**真正旁路**：最后块post-norm2/pre-MLP的h提供给SAE，但原MLP始终消费h。C的主重构输入detach；T保持输入梯度；二者target和能量分母detach，λ=1，两边都有SAE-only AuxK（k_aux256、系数1/32、10M抽样位置窗口、活动阈值1e-3）。两者LM loss都不经过SAE，SAE连续训练。不要把旧串联模型仅改一个`sae_mode`就当作新旁路。

从同一seed17初始主干/SAE开始，各自50B。不得从旧串联checkpoint或Smoke终点续训。只允许两臂标签、输出位置、aux_backbone_grad等身份/干预字段不同；参数、初值、数据、优化器、日程和抽样规则匹配。

在隔离执行目录准备并测试，然后先提交一个2×5090 Spot配对Smoke作业，顺序跑C与T的双rank路径并验证恢复。Smoke合格后直接提交两个8×5090 Spot正式作业，分别C/T，各一个节点八rank；不是一个16卡跨节点作业。失败先修复并重新验收，不绕过门，也不私自换H100/Reserved。

正式作业只做有界启动检查：rank数、计数、第一有限更新、日志落盘、即时失败。然后交付两个job ID及恢复入口并停止轮询；不要求等50B完成，不创建自动监督/自动重提任务。排队就是排队，不重复制交。Spot中断后的完整checkpoint必须可恢复，恢复不生成新训练谱系。

## 2. 已核实的关键地址

执行根 `/data/250010109/MoE_Router/experiments/`，下面所有来源只读。逐文件现存与SHA256见[复用清单](04_sidecar_50b_reuse_manifest.json)；这是当前磁盘快照，不冒充0914提交时不可变源码。

| 用途 | 绝对路径 | 如何复用 |
|---|---|---|
| 0914训练记忆 | `/data/250010109/Research_System/.research/memory/conversations/0914-training-excution/memory.md` | 读完整记录，最后一条才是50B阶段；前面的1024方案已被替换 |
| 旧50B正式契约 | `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/supporting_records/sae_pretraining/sae_mediated/20260914/protocol.md` | 参考token端点、数据循环、优化器和存盘；其授权不替代本轮旁路条件 |
| 正式训练配置 | `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/configs/formal_4h100_sae_mediated_50b.json` | 复制后适配规模、条件、rank/accumulation和输出；不能直接提交 |
| 完整分布式训练循环 | `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/dense_sae/train.py` | 复用全局计数、精确端点、完整恢复、日志；移除仅适用于旧串联T的资格假设并替换为旁路C/T守卫 |
| 更新与DDP归约 | `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/dense_sae/engine.py` | 复用独立LM/SAE归一化和裁剪、活动归约、优化器；系数已显式传入，不再重复旧“强制1未传”描述 |
| SAE / AuxK | `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/dense_sae/model/sae.py` | 复用目标/分母detach与防死分支 |
| 完整存盘恢复 | `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/dense_sae/checkpoint.py` | 模型/优化器/调度器/RNG/采样游标/SAE活动计数恢复，原子写入完整标记 |
| torchrun入口 | `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/scripts/run_train.sh` | 适配新包路径与2/8个rank |
| 旧正式启动器 | `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/scripts/run_formal_4h100_sae_mediated_50b.sh` | 仅参考恢复/退出收据；硬编码4H100，严禁原样调用 |
| 梯度检查参考 | `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/scripts/qualify_gradient_contract.py` | 旧串联断言必须改为旁路：LM对SAE梯度为零；C/T重构归属不同 |
| 恢复检查参考 | `/data/250010109/MoE_Router/experiments/20260914_sae_mediated_live_auxk/scripts/qualify_resume_replay.py` | 复用完整状态/下一更新回放思路，使用新架构与rank配置 |
| 真正旁路实现 | `/data/250010109/MoE_Router/experiments/20260915_sae_sidecar_small/sidecar_smoke.py` | 复用`SidecarQwen3ForCausalLM`的挂点和前向；单卡Smoke循环不等于合格DDP长训练器 |
| 已验收C/T配置 | `/data/250010109/MoE_Router/experiments/20260915_sae_sidecar_small/configs/smoke_C.json`、`smoke_T.json` | 四层候选的参数来源；若研究者选八层则需显式替换尺寸并重新验收 |
| 已有旁路证据 | `/data/250010109/MoE_Router/experiments/20260915_sae_sidecar_small/reports/pair_verification.json` | 仅两独立单H100、每臂100步验收；不冒充2/8卡5090证据 |
| 5090运行层激活 | `/data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/scripts/activate_5090_runtime.sh` | 复用SM120 torch2.8/cu128层；新runtime须显式识别5090-2-spot与5090-8-spot |
| 持久运行层 | `/data/250010109/dependency_packages/dense_baseline_torch280_cu128_py310/manifest.json` | 已存在；只读校验，不改基础镜像 |
| 唯一正式提交入口 | `/data/250010109/Research_System/templates/execution/acp_submit_template.sh` | 从execution_envelope解析2/8卡Spot与默认image，先dry-run再提交，保存收据 |

**特别容易踩错的地方：**旧模型的`sae_mode=observer`读取的是最终归一化h，不是这里要求的最后层MLP输入。必须移植真实旁路前向并验收挂点，不能只把`bottleneck`字符串改成`observer`。旧`train.py`还写死单T条件、bottleneck、四卡等验证，均需在隔离副本中适配。不要直接改正在训练的旧目录。

## 3. 两卡Smoke和八卡正式训练怎样匹配

共同完整更新262,144有效预测词元，seq2048、每卡microbatch2：

- 2卡Smoke：accumulation32。
- 每个8卡正式作业：accumulation8。

边界部分更新的mask、全局分母、实际token计数沿用旧50B准确停止实现。两臂正式数据顺序/抽样流需匹配；跨rank数的Smoke不要求参数位级相同，但必须证明全局有效批量和全局样本覆盖契约。正式C/T同为八卡，配对流摘要必须吻合。

按“和之前一样50B”继承的候选数据契约是现有冻结DCLM 30B前缀循环至精确50B，不是新抓50B语料；必须在正式protocol明确写出，并与最新研究者规模/数据裁定一致。数据入口：`/data/250010109/training_data_views/dclm_pair_v1/train`；manifest SHA256为`8a91bdbb0eb537bd80612015b99f178ca1cbb54a2fa7cf8442ab1eae7f0a2f2d`。tokenizer只加载词表，不加载Qwen预训练权重。

复用旧50B公共端点：0/0.5/1/3/5/10/15/17/19/.../49/50B；额外0.1/0.3/7/13B按完整更新后首次到达保存，不能引入未匹配部分更新。两臂统一端点、恢复间隔与保留策略。磁盘预算按实际尺寸重算，不能原样称四层也需旧模型同样体积。

LM AdamW lr3e-4、betas(.9,.95)、weight_decay.1；SAE lr3e-4、betas(.9,.999)、无weight decay。分别1000/10完整更新预热后恒定，不引入余弦。所有日程以匹配有效token进度解释；50B终点保留精确计数，不降成5B或开发步数。

## 4. Smoke通过标准

采用与0914正式任务前相同的每臂8逻辑更新，并在第4步进行真实独立进程恢复和第5步回放；每臂额外1次物理回放更新单列。另做full30k CUDA强制AuxK，覆盖下列门；不把短Smoke当自然死亡窗口的长期证据。

- 同初值/输入时C/T的LM logits相同；改变SAE权重不改变LM logits。
- LM-only不给SAE梯度；C主重构只到SAE；T主重构到SAE和上游。目标/分母detach；AuxK直接SAE-only。共享embedding按输入端上游判定，物理参数去重。
- 两rank的参数与活动计数一致，全局LM/抽样位置分母正确；自然死亡窗口未覆盖时如实记录，强制dead-mask分支验证非零有限AuxK，强制状态不进入正式训练。
- TensorBoard与JSONL写全局LM、总损失、raw/weighted reconstruction及AuxK、学习率、更新号、有效token和吞吐；只有指定rank写。λ有权重传递测试，不能只改JSON。
- resume恢复模型、AdamW、scheduler、RNG、采样游标、SAE活动缓冲与两个坐标；下一更新数据/抽样摘要一致，损失与状态差在预先声明容差内。
- 终态成功、receipt全部门PASS、无未解释失败；保存源码/配置/运行层哈希后才提交正式两臂。
- 两卡Smoke不直接证明八rank通信正常，正式启动器增加八rank/world_size/globalbatch守卫及首更新检查；这属于启动检查，不新增持续监督任务。

## 5. 提交与交付限制

旧文件有H100 Reserved及已弃用1024记录，不继承那些资源/预算。本轮使用`5090-2-spot`与两个`5090-8-spot`，image取当前`shphd-lite-0911`；不改默认资源，不改旧作业，不提交旧串联启动器。

执行记录应含新包路径、两配置/源码哈希、Smoke job ID与终态证据、两个正式job ID、run roots、TensorBoard路径、恢复命令、最后一次启动检查。若实际只排队，明确报QUEUED；若失败，保留失败收据而不宣称通过。Spot长训练完成依赖实际未中断运行或后续恢复；提交成功不是50B完成。

训练所得checkpoint供既有四对象分析使用；训练完成与工程验收均不拥有“更语义化”的科学结论。新问题stable problem_key/Anchor不由memory创建。科学解释仍由研究者确认。
