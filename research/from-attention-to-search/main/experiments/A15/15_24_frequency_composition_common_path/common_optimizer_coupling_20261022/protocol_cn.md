# Protocol：common 梯度通过全局裁剪产生的耦合

## 0. 批准快照

文档状态：`APPROVED_FOR_BOUNDED_LOCAL_EXECUTION`，协调 Agent 已完成来源与实现一致性审计并冻结；正式训练仍须通过下述工程检查。研究者已明确授权自主完成与引用对话不同的机制分析和执行，无需中间批准。以下假设、策略和判据属于**授权范围内的 AI 操作化**，不自动代表人类确认了机制解释或问题结论。

主 Anchor：[A15_24_01](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_24_frequency_composition_common_path/subanchors/15_24_01_common_optimizer_coupling_anchor_cn.md)。不创建、重置或升级 Focus。角色：父 common 路径问题中，一项优化竞争解释的原因审计。目的：区分梯度裁剪与实际路由 AdamW 更新，并检查从路由裁剪分母中排除 common 能否改善固定低频预测目标。

已授权本地范围：来源和日志审计、有界 GPU 工程检查、四个完整 T_F plus-common 训练、配对评价、实际 checkpoint 注册和事实分析。不新增远端资源，不扩展普通 MoE，不做超参数搜索，不训练 Base 或 CrossCoder。工程检查与四个模型合计 GPU 活跃时间上限 20 分钟。用户明确授权取代额外的设计确认轮次；来源检查和工程检查仍须完成。

处理为 `route_isolated`，对照为 `global`。两者 common 分支、模型、数据和优化器设置完全相同，只改变施加于路由参数的裁剪系数。主比较为最终 DEV 低频 feature 宏平均 NLL 的处理减对照，种子 11/22 分别报告。均为负才构成探索性支持；方向混合、零或正值不支持稳定改善；缺失或无效配对为证据不足。不声明显著性或独立确认。

执行根目录：`/data/250010109/MoE_Router/experiments/20261022_common_optimizer_coupling`。正式执行前须在 provenance 中补齐冻结时间、科学正文哈希、代码/config 清单、本轮严格资产检查、实际环境和审计通过记录。本草稿不虚构这些状态。

## 1. 术语与定义

T_F 为原固定 feature 频率路由：每个有效位置使用两个不同的已保存专家索引，权重均为 0.5。common 是每个位置必经的第九个专家，系数为 1。所有专家读取完整缓存 hidden state。路由参数组包含八个专家；T_F 没有可训练 router。可复用实现可以处理存在 router 的情况，但本协议不运行 learned-router 条件。

原始梯度指裁剪前累积梯度。实际更新指 AdamW 后参数差值，包含解耦权重衰减。影子更新从同一参数、优化器状态和原始梯度的副本分别执行两种裁剪策略，不另训模型、不推进真实状态。

## 2. Anchor 对齐

父新增 common 实验同时改变活跃容量和优化。本实验固定新增分支，只隔离一个优化规则。完成标准是历史审计、四个有效终点、固定状态更新诊断和一份有边界的结果记录。三步足够：审计已有观察；检查并执行配对策略训练；分别分析当步更新和终点效应。feature 重新分组与冻结表征替换属于引用的 A15_25 对话，本轮不重复。

## 3. 检验假设

从路由梯度裁剪分母中排除 common 的直接贡献，会改变实际路由 AdamW 更新，并在两个种子上降低最终 DEV 低频 feature 宏平均 NLL。实际更新测量和终点预测检验分别回答因果链上的不同环节。裁剪频繁本身不构成假设成功。

## 4. 竞争解释

AdamW 可能吸收大部分正比例梯度缩放；后续矩历史也可能改变轨迹，却没有终点收益。common 仍可通过联合预测损失影响路由原始梯度，本策略没有消除这种函数耦合。两策略的新增容量相同，因此策略差异不能归因于参数量；但也不能据此认定原 baseline/common 差异完全由裁剪中介。设计之前已看到的历史观察不能作为成功的事前预测。

## 5. 数据构造与来源

复用原 Tulu revision `6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752` 及精确缓存：TRAIN 1,024 段对话／85,548 个有效回答目标；EVAL 256／22,446；DEV 128／10,340。目标单位是一个回答 next-token 位置，包含回答 EOS，排除 prompt/padding。输入为 BF16 Qwen3-0.6B block-28 residual-post 向量，宽度 1,024。原路由与 feature 标签来自同一 14 层、16,384 feature CrossCoder，激活阈值 0.051281172782182693。不重新生成缓存或分词。

所需原资产 ID：`data_tulu_sft_route_20261019t012300z`、`representation_tulu_sft_route_20261019t012300z`、`model_qwen3_0p6b_base`、`tokenizer_qwen3_0p6b_base`。加载前运行 `tools/check_assets.py --strict`，并将缓存/路由与原生产清单绑定。额外消费的历史资产须先登记。数据和表征条目及源清单绑定 feature 生产 checkpoint；worker 不得默默更换字典。

保留原 split、输入/目标顺序、hidden 归一化尺度和标签支持度。DEV 曾被查看，不是独立确认集，不能选择策略、超参数、checkpoint 或停止时机。同一位置的 feature 事件会重叠，对话是自然的依赖簇。

## 6. 学习任务与允许监督

通过冻结的最终 norm 和词表 head 预测原 next-answer-token。仅训练八个残差专家与 common；Base、CrossCoder 和 head 均冻结。目标只有回答目标交叉熵，不增加 load-balance、谱、重构或 feature loss。监督是原语料下一 token；未来 token 不进入路由或输入。

## 7. 模型、架构与冻结变体

对于完整 hidden 向量 \(h\) 及原 TRAIN RMS 尺度 \(s\)，两策略均计算

\[
h'=h+s\left[\tfrac12E_{r_1}(h/s)+\tfrac12E_{r_2}(h/s)+C(h/s)\right].
\]

九个模块均为无 bias、宽 1,024 的 SwiGLU。保留原两个路由专家及权重，common 不替换其中任何一个，也不做除以三的平均。两策略都额外包含 3,145,728 个 common 参数。复用原路由初始化及独立 common 初始化（`seed+987031`，gate/up 随机、down 为零）。同种子配对初始张量与样本顺序须完全相同。初始 common 输出为零。不丢弃专家容量，也不做结构投影。

## 8. 训练目标与优化

目标为有效 target 的交叉熵之和，除以完整有效批次中的实际 target 数。微批次 128，四次累积为有效批次 512，最后一个批次 44。每模型一个 epoch，恰好 168 个已完成更新、85,548 个有效目标；42/84/126/168 步对应 21,504／43,008／64,512／85,548 个有效目标。

复用 AdamW：lr 0.0003、betas (0.9, 0.95)、epsilon 1e-8、weight decay 0.01、9 步 warmup、原 cosine schedule 末端比例 0.1。以原无状态 schedule 实现及步索引为准，不另行解释 schedule。先完成全部反向传播再裁剪。

令 \(n_R=\lVert g_R\rVert_2\)、\(n_C=\lVert g_C\rVert_2\)、\(q=\min(1,1/(\sqrt{n_R^2+n_C^2}+10^{-6}))\)、\(r=\min(1,1/(n_R+10^{-6}))\)。`global` 对两组都乘 \(q\)；`route_isolated` 对路由梯度乘 \(r\)，对 common 梯度乘 \(q\)。修改任意组之前，用同一批原始累积梯度计算所有范数，然后执行未改动的 AdamW。裁剪 1e-6 与 AdamW epsilon 1e-8 分开。处理后不得再执行第二次全局裁剪。

复用原冻结缓存训练器的模型、loss、schedule、evaluator、checkpoint 和顺序工具；仅调整裁剪、策略来源记录、固定状态影子诊断及其 telemetry。冻结末层缓存任务不复用完整预训练 scaffold。已核对来源为[原训练器](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/shared_common_expert/20261022T103833Z/code/train_shared_common.py) 和[原配置](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/shared_common_expert/20261022T103833Z/config/frozen.json)。保留原源文件哈希和副本，不改写历史 run。

## 9. 条件、种子与 Checkpoint

仅四个条件：`global_s11`、`route_isolated_s11`、`global_s22`、`route_isolated_s22`。核实实际设备身份和空闲资源后，在当前本地 H100 MIG 3g.40gb 串行执行。这不是新申请的 Reserved 资源。两个 global 对照与处理在相同设备/软件上重跑。历史完整 H100 结果只作描述背景，不假定跨硬件字节相等。

保存初始及第 1/42/84/126/168 步完整训练状态，并保存 final 硬链接，包含模型、优化器、scheduler 状态或精确无状态 schedule 身份、RNG、顺序/游标、已完成步数和累计目标数。启动前在执行 config 冻结文件名。终点固定为 168，不选 best checkpoint。恢复检查验证下一步相等和 telemetry 坐标延续。注册实际保存的 final 与里程碑 family；计划文件不是资产。

在第 1/42/84/126/168 步，使用每个 run 更新前的状态及该有效批次原始梯度，计算两种影子更新。记录参数组和各专家更新范数、相对差值、内积/余弦；任一更新范数为零时明确记录未定义。影子计算不得改动真实参数、矩状态、RNG、计数器或梯度。该测量条件于采样到的当前轨迹，不可混用不同历史。

## 10. 主指标与冻结分析计划

对原 1,694 个 B1 feature，分别平均其 DEV 激活位置上的最终 NLL，再对至少有一个 DEV 命中的 feature 等权平均。原固定面板为 838 个有支持、856 个无支持 feature；重新核对，若不一致则停止。无支持不是零损失。DEV 共 10,340 个位置，低频并集共 1,701 个独立位置。

每种子计算 \(\Delta=L_{\mathrm{route\_isolated}}-L_{\mathrm{global}}\)，单位为上述宏平均下每 target 的自然对数损失。报告两个差值及算术均值。均严格为负才构成探索性支持；方向混合或零不能满足稳定改善判据；均为正构成探索性不支持。无效或缺失终点为证据不足。均值不能替代逐种子规则。微小差异须以足够精度展示，并结合实际重放/数值一致性解释。

不以两个种子声明置信水平或显著性。feature 事件不是独立试验。若报告描述性重采样，使用固定对话簇并标为次分析；它不能改变种子符号判据。报告全部条件，不删异常种子/feature，不做事后分箱或调参。仅四个终点全部完成后才统一评估最终 DEV；partial/failure 不打开 DEV。公开后不能修改主规则。

## 11. 次指标与有效性检查

分开报告整体位置平均 NLL、低频并集位置平均 NLL 和高频 feature 宏平均 NLL。记录原里程碑 TRAIN/EVAL、路由曝光、输出范数、裁剪前后梯度范数、两种系数、实际参数更新与累计路径长度。即使低频判据支持，整体恶化也必须明确保留。路由曝光与 target 数相等是必要检查。

TensorBoard 位于各 run 的 `tensorboard/`。系统必需标签为 `tokens/train_lm_loss`、`updates/train_lm_loss`、`tokens/train_total_loss`、`updates/learning_rate`、`progress/tokens_seen`、`progress/optimizer_step`、`progress/effective_tokens_per_update`。token 标签以累计有效目标为横轴，update 标签以完成更新为横轴；progress 坐标遵守 observability contract。唯一目标项是系数 1 的 task CE，分母为实际有效目标数；辅助目标为 `NOT_APPLICABLE`。

在冻结 config 中登记稳定的额外标签，记录 route/common 原始范数、global/route 裁剪系数、实际 route/common 更新和路由/common 曝光。所有适用步数值必须有限；零范数余弦明确未定义，不伪造为零。机器可读步骤记录保留各专家数据和影子测量。影子诊断不重复增加训练目标计数。

## 12. 已知正确、错误与易混情形

已知正确：common 梯度为零时两策略一致；相同初始模型/顺序给出相同更新前 logits、loss 和原始梯度。工程检查须与独立标量/范数参考计算一致。

已知错误：common 使用自身范数裁剪；全局裁剪之后才计算路由范数；第二次全局裁剪；改变 common 系数；恢复时重置矩状态。这些都改变了已登记干预。

易混情形：裁剪后梯度明显减小，第一步 AdamW 更新却几乎不变。累计参数路径更长不能证明有用学习。终点收益不能证明语义分组机制。推理时关闭 common 回答另一个问题，不是本轮必需附加条件。

## 13. 科学过程与阶段契约

| 阶段 | 目的与操作 | 产物／通过条件 | 失败与交接 |
|---|---|---|---|
| 历史审计 | 读取原八个日志、绑定身份、重算裁剪和实际更新统计 | `observational/` 表格、完整 168 步覆盖、源哈希；保留已查看状态 | 缺失字段保持缺失，不能从裁剪后梯度猜更新 |
| 工程检查 | 检查资产/来源/缓存/顺序；核对策略数学；完整 GPU 有效批次；保存恢复比较下一步；检查影子无副作用和 TensorBoard | `qualification/` 身份、梯度、分母、finite loss、resume、token、标签均 PASS；实测 ETA 在剩余上限内 | 数据/实现/telemetry 不一致时停止正式执行并保留证据 |
| 配对训练 | 四个条件固定数据/顺序/config，训练 168 步 | `training/<condition>/` 状态、步骤记录、里程碑、有限曲线、相等计数 | 非有限数、资源上限或意外状态改变则停止相关工作，不自动换远端或加种子 |
| 最终分析 | 固定终点后统一公开 DEV，应用宏平均规则，汇总影子/轨迹差异 | `analysis/` 逐位置数组、支持度检查、配对表、次指标表和诊断 | 无效/缺失配对为证据不足，不替换指标 |

时间门槛根据实际硬件的工程检查计时计算，只判断可执行性，不判断科学成功。保留 partial 和失败结果。本轮不自动授权修复后的第二套完整实验；有效正式启动前的无害实现修复，须保留失败审计与新源哈希。

## 14. 算法、输出与来源契约

执行输入/config/源副本保存在执行根目录，下设 `observational/`、`qualification/`、`training/`、`analysis/`、`provenance/`。实际代码路径和稳定 checkpoint 文件名在源清单中冻结。记录软件版本、设备/MIG UUID、torch/CUDA、dtype、确定性设置、config 哈希、输入清单、配对初始化与样本顺序哈希。正式叙述属于本实验目录，原数组和 checkpoint 留在执行侧。

工程检查、四模型与评价合计 GPU 活跃时间上限 20 分钟。使用一个本地设备、单进程、两个 CPU 线程。沿用 16 GiB allocated GPU memory、16 GiB worker RSS、16 GiB 新产物上限；如工程检查证明原测量方式不兼容，任何调整都须在正式启动前记录同一授权任务内的 amendment，不静默替换资源。非有限值、哈希错配、计数错误、冻结状态检查失败或资源超限时停止。不覆盖旧输出。实际 checkpoint 注册与交接的本轮 selected strict check 遵守 `assets/README.md`。

## 15. 成功、失败与证据不足

工程成功要求 qualification PASS、四模型完整、目标/顺序/路由精确配对、持久终点数组、来源/config 身份和必需 telemetry。它不代表方法有效。科学探索性支持按主规则判断，并与当步更新诊断分开。如果裁剪改变实际更新却不改善主指标，报告真实优化影响而没有支持的补救。如果实际更新几乎不变，保留 AdamW 缩放抵消解释，不能从裁剪系数声称学习减少。

## 16. 不能声称什么

本干预估计当前模型及已暴露面板中一条裁剪策略的效果。它不证明原 common/baseline 差异的完全中介、最优优化、一般 MoE 收益、feature 语义正确、分组质量、Rank-one 有效或长程推理。两组都保留新增 common。common 后续原始梯度和更新变化是策略的下游结果，并非被独立固定的 common 轨迹。

## 17. 分块确认、冻结与修订记录

用户确认范围：自主完成不同的机制分析和执行，无需中间批准。源已核实：原数据维度/计数、模型、路由、学习目标和优化器设置。AI 操作化：分母干预、仅 T_F 的四 run 矩阵、固定影子步、本地上限、双种子探索性判据。没有将任何 A–G 块描述成人类另行确认的科学判断。

草稿内部审计：A 问题/边界已覆盖；B 输入身份待本轮运行核验；C 任务/来源已核实；D 相同架构已明确；E 裁剪规则和优化器来源已明确；F 主次分析已明确；G 环境资格与代码/config 冻结待完成。协调 Agent 在升级为已授权本地执行状态前记录一致性 PASS 和冻结；该内部检查不增加用户批准步骤。

在结果 Detailed 附录记录三轮简短审计：来源与数学一致性；干预/代码/工程检查一致性；独立结果/分母/声明审计。正式启动后保留冻结科学正文。材料性修订须记录时间、旧/新值、原因、已暴露证据、受影响条件、授权和证据资格。结果解释写入 Summary/Detailed，不覆盖本 Protocol。

### 冻结记录（首次执行前）

2026-10-22T15:35:06.582991+00:00，协调 Agent `/root`：B 输入严格访问检查通过，G 源码与配置审计通过；两名实现审计者独立核对裁剪和影子更新。一致性 PASS，状态为已授权有界本地执行。GPU 数值、恢复和 TensorBoard 资格由工程检查决定。冻结配置与源摘要见执行侧 `provenance/design_freeze.json`。实际保存文件名为 `initial_resumable.pt`、`resumable_step{1,42,84,126,168}.pt`、`final_resumable.pt`；每个均包含完整状态。时间上限按所有执行进程累计 wall time 保守计数，排除进程间审阅间隔。
