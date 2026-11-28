# 执行 prompt：路由—表征共同学习的梯度反馈对照

你是独立执行对话 **1005-路由表征共同学习：梯度反馈对照执行**。模型必须为 **gpt-6.1-sol**，reasoning effort **high**。用中文与研究者沟通。读取本文件后立即推进已授权工作，不要只给计划或再次询问是否提交。

## 1. 用户任务与权限

用户要求把前序对话提出的路由梯度反馈对照作为**另一个临时研究项目**，由你读取必要来源、完成设计与实现、提交训练，并在训练前确定训练后表征研究与相关测试；为自己建立名称明确的独立 conversation memory。

直接用户请求及最新资源修订保存在同目录 `researcher_request_cn.md`。最新修订覆盖原先“两项8卡5090”的安排：

| 条件 | 工程 Smoke | 正式训练 |
|---|---|---|
| A `coupled`：正常路由梯度 | 单节点4卡H100 reserved，`h100-4-reserved` | 单节点4卡H100 reserved，`h100-4-reserved` |
| B `router_input_detached`：阻断路由输入梯度 | 单节点2卡5090 spot，`5090-2-spot` | 单节点8卡5090 spot，`5090-8-spot` |

每项正式训练只提交一次；正式双臂须在两种硬件 Smoke 都合格、共同配置冻结后提交。Smoke 失败时，可在本范围内修复、保留失败记录并重试，先查已有任务，绝不重复创建仍在排队/运行的任务。两项正式训练合计最多两个并发任务，不做额外种子、第三臂或自动扩预算。

**用户明确覆盖默认正式启动观察规则：Smoke 必须观察到足以判定 PASS/FAIL；Smoke 通过后发起正式提交，保存提交调用直接返回的回执、job ID或错误，然后停止轮询。不等待正式任务排队成功、RUNNING、首个训练步或训练完成。不创建后台监控、提醒或定时任务，不自动做后续重提交。** 若提交返回不确定，标明 `SUBMISSION_UNKNOWN`，保存精确线索，停止；不得为了获得job ID盲目重提。若提交命令会内部轮询启动，先移除/绕开其等待阶段，保留正式创建调用与回执逻辑。不要把提交请求已发出写成已接受或已运行。

执行者受托把模型规模、优化器等工程/实验细节具体化并在正式 Protocol 中冻结，不需要为本任务已授权范围重复请求批准。最新用户请求是批准来源；将其规范化到新 Protocol 的 approval/amendment 段，而不是把本 prompt 或 memory 当作独立授权。未获科学判断仍 Unknown；无需为 Unknown 解释停下已授权实现。

## 2. 独立路径与写入边界

- System：`/data/250010109/Research_System`。
- 新项目：`/data/250010109/Research_System/Projects/router-representation-coupling`；目前是独立临时文件夹，不是另一个已发布Git仓库。
- 本项目代码、原始输出、检查点和运行回执：`/data/250010109/MoE_Router/experiments/20261005_router_representation_coupling`（新建）。
- 你的独立 memory：`/data/250010109/Research_System/.research/memory/conversations/1005-路由表征共同学习梯度反馈对照执行/memory.md`。先验证你的实际 thread 名称与ID，若名称已由派发器设置为上述名称，不再改名；初始记录若已创建则全文读取后追加。
- `Continues from`：`/data/250010109/Research_System/.research/memory/conversations/1002-自然语言统计规律与更新相容性两小时研究/memory.md`。它只是前序来源，不要求读取整段旧历史；本 prompt 的精确read list足够。不得改写它。
- 仅修改新项目、新执行目录、自己的memory。更新新项目roadmap，使其指向你创建的唯一Anchor、Protocol、训练后分析Protocol。不要修改旧共享容量实验、原训练仓库、旧结果、其他对话memory、系统skills或其他项目。没有 commit/push/外部发布权限。
- 首先查看新执行目录和回执是否已存在；若存在，按现状续做，不把新对话当作重启理由。

## 3. 先读这些资料，按用途逐步展开

必读且需要真正核验内容，不得只列出“已读”：

1. System `AGENTS.md`、`docs/skills.md`、`docs/report_writing.md`、`docs/markdown_math.md`。使用最小相关owner：Anchor用problem-anchor-writer，Protocol与结果用experiment-card-writer，执行用remote-experiment-workflow；SCO资源操作按sco-control。只读取当前阶段适用references。
2. 新项目 `README_cn.md`、`main/roadmap_cn.md`、本prompt、`researcher_request_cn.md`、`source_manifest.json`。manifest只是交接时源身份，不是源未变化/已批准的证明。
3. `daily_research_reports/1002/candidates/ntp_representation_update_channels/anchor_cn.md`：已有问题、固定专家选择/学习分配的区别与信息边界；**不继承旧实验执行权**。
4. `daily_research_reports/1004/cognition_update_cn.md`：已完成固定库负结果、Adam/未来轨迹边界。关注§2–5，不再重复已经完成的184条件审计和shrinkage网格。
5. `daily_research_reports/1002/candidates/ntp_representation_update_channels/sharing_literature_20261004_cn.md`：已有Switch/X-MoE/OLMoE/共享专家证据及边界。
6. `docs/training_reuse_index.md`及其当前训练scaffold README、source_audit、实际train/data/checkpoint/model源码。**逐项说明复用、适配、不复用**。优先复用验证过的数据流、DDP、原子checkpoint、resume、日志、SM120环境；在本项目独立适配路由开关，不在旧生产目录直接修改。
7. `docs/training_observability_contract.md`、`docs/execution_envelope.md`、`templates/execution/acp_submit_template.sh`及resolver；5090层激活脚本与最近合格运行回执。脚本存在不等于新架构/新拓扑已合格。
8. 创建memory时读research-memory及memory_contract；canonical文档英文带中文伴随，prompt/memory可以中文。

先运行 `python3 tools/check_current_entrypoints.py --working-tree`。交接前已有无关未跟踪入口 `Projects/diffusion-language-models/main/literature/2026-07-17_diffusion_language_model_evidence_audit.md`；不擅自修复它，不把导航检查当科学审查。

补充原始论文只需定向核查：X-MoE https://proceedings.neurips.cc/paper_files/paper/2022/file/df4f371f1f89ec8ba5014b3310578048-Paper-Conference.pdf §2–3；DeepSeek-V3 https://arxiv.org/html/2412.19437v2 §2.1.2、4.5.3；Demons in the Detail https://arxiv.org/html/2501.11873v2 §5。不要因综述无限延长执行。X-MoE未证明总表示必然塌缩，也未验证本实验detach干预。V3的batch辅助损失可追平aux-free，不能把均衡范围差异称为纯梯度机制。

## 4. 被授权具体化的问题与唯一核心变量

问题键暂定 `router_representation_gradient_feedback`。有限训练预算下，路由分支返回共享主干的直接梯度，对语言建模损失、专家功能分工及表征结构具有什么净作用？

共同前向：专家接收完整计算输入 h；router得到登记的reference r（应写明 r 是实际expert输入h还是attention输出，禁止把二者混称）。
- A：gate = router(r)。
- B：gate = router(stop_gradient(r))。

B仍训练router权重，仍训练专家，仍通过专家/残差等正常路径训练主干；r的数值也会随主干学习而变化。B不等于冻结表征、固定路由、冻结专家或移除全部共同适应。禁止detach专家输入、专家输出、门控权重本身或整个MoE输出。

优先采用已经验证的小型原生MoE骨架（可从约342M、12层、8E/top-2候选检查起），从同一个随机初始化state开始；不要照搬失败/退役生产pair，也不要加载旧模型权重冒称随机初始化。关闭无关de-common/SAE/谱正则。共享专家是否保留、路由reference、top-k归一化、所有层还是固定层必须在两臂完全相同，并在Smoke前冻结；默认干预全部MoE层，保留所选稳定骨架的其他前向行为。

辅助损失是关键混杂：优先保证两臂**辅助损失对主干的路径相同**，仅改变LM门控反馈。例如辅助目标使用独立live-reference分支计算同值logits，或在两臂统一阻断辅助目标回传主干；不得在B顺手多切一个辅助梯度，再把结果称为纯LM门控反馈。若选现有已验证aux=0配置，可避免该混杂，但要登记负载塌缩失败条件。负载控制方式及窗口、路由温度、共享容量等不得同时作为第二个变量。不要只因新颖而换上aux-free或新归一化。

主要假设为双向开放：直接反馈可能帮助形成可用分工，也可能产生有害竞争；可信对手包括梯度幅度/优化正则效应、实际负载差异、专家样本量差异及硬件数值路径。几何变化只是描述，不能独自证明收益或因果机制。

## 5. 有界首轮预算与工程资格

这是规划者给你的**首轮执行上限**，不是声称用户指定了token数：每臂不超过10,000,000,000 valid prediction tokens，一对共同seed；没有额外seed授权。优先有效batch **262,144 valid tokens/update**，终点取不超过10B的完整优化步边界，记录精确目标；不得静默多跑一步。你可依据实际已验证架构与资源把目标定得更小，但必须在正式提交前把两臂共同目标和理由写入Protocol，不可看到正式比较结果后改终点。不得自行扩大到50B或新增第三臂。

统一tokenizer、冻结数据view、token顺序、共同初始state/hash、优化器初态、全局loss reduction、warmup/decay的token坐标、权重衰减、梯度裁剪、精度与数学模式。4H100与8RTX5090通过microbatch和accumulation反向调整保持global batch。2RTX5090 Smoke也检查同一有效batch或明确标注哪些仅tiny资格、哪些实测了正式batch。

两种硬件不同，算法臂与硬件**完全混杂**；短期数值验证不能证明长期硬件效应为零。必须在两种已授权Smoke中，从共同state和相同小批数据各运行A/B短窗口，比较前向/梯度/短期更新差异、噪声幅度与内存/速度，保存交叉诊断。最终论文级算法结论仍受单seed和跨硬件限制，必要的同硬件重复只能列为待授权后续，不自动创建。

至少证明：
- 同state前向logits/选中专家/gates/loss等价；确定合理精度容差，保留失败，禁止失败后无解释放宽阈值。
- 同state下router参数梯度、专家参数梯度一致；B只去掉指定reference路径，专家输入梯度与残差路径仍在；用autograd隔离被移除项，检查A−B符合该项。
- B router确实更新，任务梯度非零；top-1归一化为1等退化不存在。
- DDP与累计梯度、valid-token计数、要求的TensorBoard tags、checkpoint原子性、外进程resume/重启后计数与采样恢复。
- 5090使用registry默认镜像及隔离SM120运行层；不改base环境，不猜镜像。5090 2卡Smoke通过并不声称8卡全拓扑已验证。正式8卡脚本内置启动自检：world/rank、collectives、分片、全局batch、输入/状态一致性及OOM/有限性，失败即停止，不自动切规格。
- 每臂生产形状的peak allocated/reserved memory、valid tokens/s、预计时长与存储量。生产不同CE分块/activation-checkpointing要预先登记并验证语义等价。
- 所有checkpoint、optimizer/RNG、原始tokens/activation缓存留执行目录。保存token对齐的0B、早期、中期、终点weights用于后测；rolling resume最小保留依照现有合同，不删除旧项目payload。

## 6. 在训练前登记训练后研究与测试

你必须把下列内容具体化为新项目下独立的分析Protocol（英文/中文），并建立可运行或明确待实现的入口与输入清单；不要等训练结果出来才选择指标。此轮要求**确定并准备**后测，不要求等待训练完成或启动长时间后测作业。

1. **主要效用**：冻结独立heldout文档、按valid token加权的CE；以相同累计tokens对齐检查点。预先声明主要终点和最小可解释差异的设定方式；未获确认的科学阈值标为AI建议。置信区间按文档/序列聚类，不能把token当独立样本，也不能把数据bootstrap当seed不确定性。
2. **梯度路径诊断**：在相同checkpoint/样本上记录expert-path与router-path返回reference/主干的梯度范数、夹角和相对量；这些是局部归因，不是未来效用或完整因果证明。训练detach关闭的离线读数与真实训练路径要明确分开。
3. **表征几何**：在冻结的同一组前缀上取干预层输入、router输入和专家输出；登记中心化、norm控制、协方差谱/effective rank、CKA等不超过必要数量的描述指标。按token位置、长度、词频/领域控制组成；禁止凭可视化簇或有效秩单独给优劣结论。
4. **路由与专家功能**：负载、熵、dead expert、固定前缀的route churn；跨模型专家编号不可直接等同。主功能测试采用每个模型内部、保持层级专家使用率与计算量的路由置换/替换，对比heldout CE变化；置换不能引入未来token到因果前向，数据集标签不能作为部署router输入。跨模型需要时仅FIT集合匹配专家功能，不按test最优排列。
5. **更新相容性**：少量独立诊断样本，在checkpoint副本上执行预先登记的有限更新，比较同路由/异路由样本的帮助与损害，并有类别/词频/负载匹配对照。冻结更新量、优化器状态是否使用、评价对象与有限步长；不改正式checkpoint，不把gradient dot当实际有限损失。
6. **判定分支**：更低CE且有功能干预支撑；只几何变化无效用；CE差异但负载/硬件/优化解释未分清；区间/预算不足。分别给出支持、反对、INSUFFICIENT的界限。两条matched trajectories尚不足以证明普遍改善或所有共同学习机制。

核心后测应可利用现有两项训练保存的checkpoint开展。昂贵全专家遍历、大规模SAE训练、新预训练或更多GPU任务不在本轮范围；需要时只估计费用并列为后续建议。

## 7. 顺序、交付与停止

1. 验证你的模型/effort与thread名称，创建/追加自己的memory；读required sources及实际源代码。
2. 在新项目形成唯一Anchor及匹配的训练Protocol、分析Protocol，写清本轮用户授权、资源修订、预算与科学Unknown；初始结果 `NOT RUN`。Focus如创建，problem_key用本文件已命名的问题，下一决定是该直接反馈是否值得保留/进一步验证，不替研究者宣布机制结论。
3. 独立适配代码，登记reuse/provenance与文件hash；做有意义的局部/梯度/分布式测试，准备两种Smoke与正式launchers，做dry-run tuple校验。
4. 提交并观察4H100 reserved Smoke与2RTX5090 spot Smoke，完成预先资格。可在两者之间并行等待，但同一个run只能一个owner；不影响任何既有job。
5. 两种Smoke合格后冻结共同正式配置，依次或并行发起A的4H100 reserved与B的8RTX5090 spot正式创建请求，记录每个独立结果。此后停止轮询。一个提交失败不重复另一个，错误明示。
6. 最终向用户报告：项目/Protocol/分析计划/memory路径、两种Smoke证据、正式提交的精确状态和job ID（有则给）、未验证启动状态、跨硬件和single-seed边界。你的memory追加当前状态、回执和下次只读查看入口。

完成标准是“对照任务已完成资格并发出正式提交，后测计划与必要留存已确定”，不是训练完成。若Smoke/必要环境无法通过，完成其余独立交付，记录具体阻碍；绝不能把FAIL写成PASS来提交。除真实新增范围或不可替代的人类判断外，不再次请求本范围执行许可。
