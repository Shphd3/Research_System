> **⛔ SUPERSEDED — 不要再把它当作入口。**
> 当前唯一入口：[`continuation.md`](../../../../../../../.research/memory/conversations/0910-sft-matrix-execution/continuation.md)（工作流：SFT 路由表示全矩阵）。
> 本文件内容**原样保留、未删改**，仅作历史来源。它是**执行前**（2026-09-09T19:54:59Z 暂停点）的启动 Prompt，**不能当现状依据**。

# Renew执行Prompt：14条件完整矩阵＋离线层级扩展

版本：`full_matrix_v2`；暂停交接更新：2026-09-09T19:54:59Z。处理Agent：Codex。以下正文可整体复制给执行Agent。它取代此前单条件/三条件建议的执行Prompt；旧已启动run的快照不可改写。

---

请完整实施、训练并审计下列实验，持续到full run、图表、离线层级分析和结果交付全部完成。不要只制定计划，不要在smoke通过、作业提交成功、部分条件训练完或画出第一张图时结束。

我明确授权：**SCO ACP单节点4×H100 reserved，14条件×3种子×512更新，共42条完整轨迹；所有条件完整分析、画各自聚类图，保留21个正式检查点；另完成有限十配置的离线层级参数分析及相应聚类。**时长仅估计，今晚可跑较长时间，不设一小时硬停，不按结果或时间缩减范围。上述既定预算、资源与恢复无需反复请求批准。

## 0. 当前交接状态：必须先补齐实现

上一Agent已按我的要求停止继续实现和运行。我现在将剩余工作完整交给你：**接手部分实现，修复并补齐框架、通过资格、执行完整full run、完成全部分析与结果交付**。不是只审阅代码或再交一个计划。

当前代码已写在 `/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/`，但还没有CLI/完整ACP启动器/必要测试/完成验证器，尚未验证整条链路；本次新训练未启动。已有模块的存在不等于可直接提交。首先完整阅读：
`/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/sae_representation/20260910/docs/sft_audit_remaining_work_cn.md`。
它记录准确暂停位置、已有模块、全部待办与需要优先审查的缺口。补齐实际可执行入口再启动，不使用猜测的命令。

你还必须再次阅读组会并完成“能否回答导师问题”的评估与科研假设修正。固定八簇不证明类别诞生；局部SFT不等于随机初始化训练；来源标签不等于语义；参数扫描加深不等于训练中涌现。这些边界必须进入结果读法，不能只跑完模型。

## 0. 当前状态：必须先补齐，不能直接启动未测试框架

本Agent没有前文上下文。已有框架位于 `/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/`，状态为 **IMPLEMENTATION_PARTIAL_UNQUALIFIED**。只有部分模块一次导入检查成功；后续模块未测试。没有新teacher缓存、正式run、资格训练或ACP提交。CLI、四卡启动器、验收器和真实测试仍待实现。

先完整阅读 `/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/sae_representation/20260910/docs/sft_framework_resume_cn.md`，逐项修复其中明确缺口。你的任务是“完成剩余实现→测试→真实资格→42条完整训练→全部审计/离线分析→结果交付”，不是只运行现有脚本，也不是继续写计划。不要从文件存在推断功能已实现。当前暂停仅针对上一Agent；本消息要求你接收后继续完成以下全部范围。

## 1. 先完整阅读、核验并记录

工作仓库为`/data/250010109/Research_System`。先完整阅读当前system/developer指令、适用Skills和研究系统规则；读适用AGENTS.md及执行仓库`/data/250010109/MoE_Router`的适用指令，然后完整阅读下列文件，不只读首屏或摘要：

1. `/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/sae_representation/20260910/docs/sft_representation_audit_plan_cn.md`：完整矩阵、训练梯度、教师定义、分组比较、检查点和完成合同。
2. `/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/sae_representation/20260910/docs/sae_hierarchy_offline_extension_cn.md`：十配置、四种图视图、严格复核、所有新增层级的聚类分析及直白解释要求。
3. `/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/sae_representation/20260910/docs/sft_audit_sources_cn.md`：资产身份与过时memory边界。
4. `/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/sae_representation/20260910/docs/sft_audit_agent_handoff_cn.md`：交付、验收及回审问题。
5. `/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/sae_representation/20260910/docs/sae_relations_explained_cn.md`：把原子、层级、输入聚类、路由和专家输出分清。
6. `/data/250010109/Research_System/daily_research_reports/0909/docs/0909_组会逐句校订稿_含原文对照.md`：导师要求的上下文，不把直觉当事实。
7. `/data/250010109/Research_System/.research/memory/conversations/0910-clustering-change/memory.md`：完整读至最新条目；旧条目保留历史，最新v2覆盖此前缩小范围。memory本身不是批准来源，本条消息明确授权执行。

**必须读取聊天记录。**使用可用的任务/聊天读取工具，按需分页读相关讨论和用户决定：当前任务 `01a08725-f7b0-75e2-bb6d-3e8e86989e47`（0910-clustering change）、Router任务 `01a081e5-b3fa-7f53-bdf1-826e1d87cfab`、SAE任务 `01a07c43-d099-7d63-8e11-83867d8f7c6b`、ChatGPT讨论 `6a9f7fa8-3f50-83e8-9c41-f6aa870777de`（0908 SAE understanding andForward）。主任务重点核对最终14条件范围、28节点与router-only决定、暂停交接；不要从早期消息恢复已被覆盖的三轨迹范围。记录读到的范围和不可达项，不能假称已读。聊天补充研究者意图，科研证据仍回到所属原始文档与实际产物。

还须完整阅读system入口 `/data/250010109/Research_System/AGENTS.md`、`README.md`、`PROJECTS.md`、`docs/skills.md`，按当前任务加载 `.agents/skills/remote-experiment-workflow/SKILL.md`、`experiment-card-writer/SKILL.md`、`research-memory/SKILL.md`及各自必读参考，平台操作读 `/root/.codex/skills/sco-control/SKILL.md`。只读实际相关Focus/Anchor/Protocol；正式归属不明不创建虚构问题，不把旧批准移植为新科学批准。本消息已给本次执行范围授权，不因Skill默认流程重复询问同一授权。

阅读聊天记录：用可用的任务读取工具（如read_thread）分页读取当前源任务 `01a08725-f7b0-75e2-bb6d-3e8e86989e47`（0910-clustering change），以及相关任务 `01a081e5-b3fa-7f53-bdf1-826e1d87cfab`、`01a07c43-d099-7d63-8e11-83867d8f7c6b`、ChatGPT任务 `6a9f7fa8-3f50-83e8-9c41-f6aa870777de`。重点读用户对完整矩阵、high28、router-only、离线分析及完整执行的确认，和从旧范围变更到v2的上下文。不要只读任务标题，不要将全部工具日志倒入上下文。工具无法访问则写具体不可读记录，继续以本消息及完整文件限定执行，不假称读过、不将聊天作为canonical科学证据。

写入新run的read_receipt：每份实际阅读文件路径/哈希、各聊天读取范围/不可读原因、最新约束及仍需验证事实。新任务若写memory，按自己的真实任务标题新建记录并Continues from旧memory，不覆盖源任务记录。

阅读`PROJECTS.md`用于归属导航；实际运行状态用源文件/receipt核验。使用remote-experiment-workflow、sco-control及相关参考；正式结果写作使用experiment-card-writer结果证据规范。用户已选reserved，优先于Skill的SPOT默认；不要要求我重新选SPOT，不随意新建科学Focus/Anchor或修改Graph。

完整阅读并核验旧正式快照：
`/data/250010109/MoE_Router/experiments/20260909_online_sae_gmm_regularized_router_decay/runs/full-20260909T020300Z/`
中的formal_manifest.json、full_submission_receipt.json、source/config.py、backbone.py、model.py、train.py、teacher.py、targets.py、data.py、artifacts.py、runtime.sh、acp_full.sh、full_run.py。尤其验证结构梯度旧实现仅更新router，不能对新模型直接R.backward影响attention。

核验旧A5根目录`/data/250010109/MoE_Router/experiments/20260908_sae_h_input_balanced_router/runs/full-20260908T111248Z/`的data、三seed task-only t0、sample_schedule、groups；GMM使用A6R1的token_gmm。阅读实际导入的Qwen3相关attention/norm/block代码并锁定依赖。

离线部分完整读旧hierarchy_presets.json、hierarchy.py、static_run.py、static_analysis.py、stage1_cluster.py、two_stage_inputs.py、prepare_inputs.py、evaluate.py和相关source manifest。核验static-20260909T085200Z的六配置真实结果、输入与图，不从旧README或部分stage2文件推断完成。继承代码时保留原证据，新修改放新目录。

读取同目录`sft_audit_matrix_v2.json`，核验14条件、42任务、39个G1–G6对比定义、882点和十离线配置与主计划一致。

简短给出阅读回执、14条件清单、教师/梯度定义、资源元组、待核验的实际事实，然后继续执行，不把回执当最终回复。

## 2. 不得遗漏的矩阵和最新决定

方法为task、sae_a、sae_b、gmm_a、gmm_b、high28_a、high28_b，各自包含F/U两版本；F冻结全部主干，U只开放最后attention；**两者router/shared/experts都训练**。每个条件17/29/43三个seed、512有效更新。使用同一数据、各seed同一起点和样本顺序，原微批8、累积16、有效批128。

研究者确认：high28主教师来自固定参考支持量合格图深度≥2的28个原子；不能换成226个非叶节点或从今晚扫描选最深图。高层关系需重新构图分组，不能截旧全原子top50矩阵。按主计划第7节保留全部28原子、显式处理孤立分量、总八组并锁定共同映射。

研究者确认：**结构约束只更新router；U attention和shared/experts仅由任务损失更新。**采用参数组分别裁剪，避免结构梯度通过共同裁剪系数即时影响attention。教师参数冻结；主计划默认在共同t0固定监督target，F/U面对同一目标。明确报告这一默认和覆盖差异，不能悄悄改成逐checkpoint更新教师。

全部结构条件lambda从update1的0.01线性降至512的0.001，A/B、学习率、精度、有效批归一化按v2主计划。统一重训主矩阵以获得匹配实现和早期点；旧轨迹仅作历史核验。完全符合v2且已有全部21点的轨迹可以身份核验复用，不重复计算；不能用旧五点冒充21点。

每条保存：0、1、4、8、16、32、64、96、128、160、192、224、256、288、320、352、384、416、448、480、512。共882点，含attention、adapter及完整恢复状态。保留原始向量和checkpoint，不能只留PCA图。

## 3. 资源、资格和持续执行

使用SCO ACP、share-space/share-cluster/n6ls.iu.i40.4候选元组、worker_nodes=1、quota_type=reserved、priority=normal。实时核验确为4×H100及镜像/挂载，不能切SPOT、5090、多节点。已有明确资源授权，核验后按范围提交。不输出凭证，不干预其他用户或其它任务的作业。

四个独立GPU worker从42任务清单取完整轨迹；一进程一GPU、一份optimizer/random/balance，禁止跨条件all-reduce。四卡满队列分批运行，42条约11轮容量，不把四张卡等同于只训四个模型。训练结束后四卡分片提取/NLL，离线大稀疏共现任务控制内存并发。

资格预算为14条件各seed17两有效更新＋一个high28-B-U连续/恢复对照共8更新，合计36更新；与正式run分开。完成参数/梯度隔离、目标覆盖、A/B归一化、取点/因果前缀、注入重建、保存恢复、零输出、固定面板/投影及高层分组资格检查。真实执行检查不能被纯合成测试替代。

记录F/U各种方法的时间/显存、目标构造和提取成本、882点与原始表征存储预算，资格通过后直接full run。磁盘不足先解决安全存储，不删除正式点或缩数据。故障从最近完整有效批恢复同一逻辑run，不并发重复提交，不重复消费样本；改实现影响语义则新身份记录，不能拼接伪装同一轨迹。

## 4. 全部条件都分析、全部条件都画图

固定dev/test面板，主取点为首答案预测前的h；每个条件所有seed和21时刻都提取。h、路由、八专家输出、实际贡献、shared、最终v分别报告。初始零专家输出的方向不可定义，标记而不填假数。

交付训练/留出NLL、方向位移D、相对关系变化R、来源B/W/S、norm、近邻、教师覆盖/梯度/路由分配，以及规定配对区间。共同PCA坐标/颜色/轴范围；每条轨迹包含所有21时刻的静态完整附件、八专家面板，并有按来源/实际路由/固定八组探索聚类着色的对应图。不得独立降维拼出“越来越分开”，不得只交最好seed。

结果必须按主计划G0–G8组织：总览；同状态结构对task；同方法U对F；A对B；SAE对GMM；high28对原SAE；交互与覆盖；42条轨迹逐条；离线层级。每组带完整表、图、读法、原始身份和边界，便于按问题阅读。

## 5. 新增离线分析也必须完整完成

按离线详细方案运行十个固定配置。H0–H5核验可复用，H6–H9本次纳入，不能因旧preset名含deferred跳过。四个视图分别为发现、配置内复现、支持量合格、统一严格复核；全部重算深度并比较参考图。

所有深度增加配置都要有真实最长路径、每条边/组合的discovery与replication证据、节点层级图和聚类分析。发现变深但严格复核未变深同样要报告。深度≥2主集合与非叶补充集合、三聚类seed、20次频率匹配及记录级覆盖按附件执行；不可构造则给具体原因/诊断图，不删节点造簇，也不以“没更深”跳过结果解释。

交一份直白的explanation_cn.md，清楚说明SAE未改变、参数怎样改变关系图、图更深不等于新语义、更深节点覆盖了哪些输入。主28教师保持固定，新配置不自动加入模型训练。十配置结束即停止参数扫描，不追求达到六层。

## 6. 最终完成必须有证据

代码与原始结果：`/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/`，每run独立时间戳。保留原single-condition目录和其他任务结果。研究文档留在Research_System。

最终核验42/42轨迹、882/882checkpoint、1764/1764主提取分片、全部NLL/聚类图/G0–G8、十配置离线输出及复现入口。receipt分别列训练、分析、离线完成度，不用一个COMPLETE掩盖缺失。不可定义或没有深度增加是有效结果；实现失败/缺产物是PARTIAL，不能冒称完成。

完整结果以Summary四部分和Detailed证据账本交付（若正式归属未定，先交明确标注的唯一结果草稿，不伪造科学归属）。最终先给结果阅读入口，再按组解释训练效果、h/路由/专家变化、层级参数结果和最近边界。研究者看完后确认科学判断与下一决定；不要自动发布、commit/push、改Graph或外部同步。

还须交付导师问题评估与科研思辨修正文档。重读组会07:55–09:35、12:41–14:52：不把导师问题偷换为越来越细；明确固定K8不证明类别诞生、来源不等于语义、预训练模型局部SFT不等于从随机初始化研究形成、离线参数增深不等于时间增深。先定义观察对象/横纵轴、预测与最强竞争解释，再对照真实结果。允许非单调、零变化、Unknown。此处不授权新增预训练或功能干预；建议标AI建议，科学判断待研究者。

无需再次问是否开始、是否继续全部条件或是否完成图。运行失败先定位并在原范围修复，严格身份恢复，不减少条件/seed/步数/正式点。真实外部阻塞则明确缺口与恢复入口，不能承诺不存在的完成。完成不仅检查数量，还检查身份、可加载性、同seed初始化/日程、每项分析和图链接。

**请持续完成全部已授权工作，不能以“脚本已准备好”“job已提交”或“一个条件已完成”作为结束。**外部不可恢复阻塞时保留证据、恢复入口和真实未完成清单，不削减合同来获得COMPLETE。
