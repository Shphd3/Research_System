# 可直接交给下一 Agent 的 Prompt

以下消息授权你完成计划中的本地实现、证据核验与比例适当的本地分析；不自动授权新增完整远程训练。不要在读完材料、写出脚本或第一次检查通过后停止。把无需新科学决策的工作做完，昂贵运行若缺少授权则先交付完整可审阅的代码、资格与预算。

---

你是实验实现与证据审计 Agent。工作目录 `/data/250010109/Research_System`；实验代码和原始数据保留在 `/data/250010109/MoE_Router`。请用中文解释，遵守 system/developer、仓库 AGENTS.md 和相关 Skills。

**目的：** 基于0909组会提出的“训练中结构如何演化”，补齐当前表征—SAE—路由的证据链。不要把“训练完成”“聚类更漂亮”当研究目标。我们先要回答：旧实验哪些部分可用、哪些必须补测或补训；再回答：原先结构预期与实际差在哪里，差异可能出在哪一段。最终主汇报只用两张关键图，并帮助研究者自己讲清。

## 必读材料

1. 本次唯一补足方案：
   `/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/sae_representation/20260911/0911_minimal_followup/plan_cn.md`，全部读完。
2. 同目录 `source_audit.json`：这是当前只读盘点，不是资格通过。先验证路径、数量和当前源码，不把它当历史执行身份保证。
3. 下列 memory 全日志：
   `/data/250010109/Research_System/.research/memory/conversations/0910-clustering-change/memory.md`；
   `/data/250010109/Research_System/.research/memory/conversations/0910-sft-matrix-execution/memory.md`；
   `/data/250010109/Research_System/.research/memory/conversations/0910-clustering-analysis/memory.md`。
4. `/data/250010109/Research_System/daily_research_reports/0909/docs/0909_组会逐句校订稿_含原文对照.md`，重点08:53–09:35、13:09、14:13–15:19。老师没有规定越训越细。
5. 用 `read_thread(threadId="6aa2dc1b-1410-83ee-933b-b4a35b5a75ee", turnLimit=10)` 读取讨论；按cursor补必要历史。若接口或附件不可读，记录限制，继续本地证据核验；聊天只用于理解问题。
6. `/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/sae_representation/20260911/0911_0130_0530_document_inventory/handoff_cn.md` 与
   `/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/sae_representation/20260911/0911_dynamic_structural_teacher/report_cn.md`。
7. `/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_13_semantic_supervision_middle_layer_formation/A15_13_E21_dynamic_structural_teacher/protocol.md`，及后来若出现的 Summary/Detailed；计划中指出的代码/报告冲突必须自己确认。

本轮只是补审计和候选试验实现，不重定义研究问题。若需要修改注册问题的正式文件，先 `./researchctl context A15.sae_hierarchical_teacher_construction --task "0911 geometry and teacher-route supplementary audit"`，并核实该key确属当前任务；不要另造问题key。任务完成释放登记。重叠提示不阻塞工作。

## 执行根与不可破坏的边界

`E=/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix`

`R=E/runs/full-20260909T203104Z`

正式动态轨迹在 `R/dynamic/run2/<condition>__seed<seed>/`，不是直接在 `R/dynamic/`。SAE快照名 `saesnapshot_0032.pt` 等。静态矩阵在 `R/conditions/`，表征在 `R/representations/` 与 `R/dynamic_representations/`。从训练/抽取sidecar建立一一映射，不依赖mtime和完成标签。保留失败记录。

新增只读后处理放 `E/audits/0911_minimal_followup/`；未来训练修正版另建源码快照/运行根，绝不原位修改已运行的 fm、dynamic 或旧产物。不要运行带删除pilot/重跑全部条件的旧launcher。不要自动commit、push、改Graph、发布或外部同步。

## 按顺序完成

### A：先补测量与资格，不补主模型训练

按 plan §2逐项出结论：确认、排除、影响未知，附具体函数/文件/数值。特别核查：

- 报告使用来源权重，代码使用簇等权；两者不同不是训练坏了。固定样本权重重算W/B；旧数单独保留。测试不等簇大小下恒等式与分组变化。
- 动态W/B是否每点重新聚类；主结果统一固定共同t0成员，K-means/GMM并列且用同等证据标准。
- 同时刻跨臂C矩阵直接差异；不能用两个到起点的距离相减判轨迹相同。
- 求解器噪声按条件、训练seed、对应端点比较；不能把算法重复当训练重复。
- 当前SAE辅助项是否在no_grad里，做梯度存在性最小检查；零top-k值是否被算入共激活。代码疑点和历史实际影响分开。
- 区间buffer何时收满、表征产生于哪些更新；若buffer未保存不可假称精确还原。
- 静态缓存q与动态当前h的差别；动态源码的历史身份是否完整；GMM快照能否找到。
- pilot与正式证据分开，缺Summary/Detailed如实记录。现有数字不能自动获得规范资格。

以 task_u 三seed为几何主对象，task_f阴性对照，复用现有21点固定面板。数据顺序、位置、权重、有效掩码与hash先核对。输出来源均衡与旧簇均衡的并列表，明确何种结论改变。新分析是探索性，不能改旧Protocol的登记判据。按计划补稳定/返回/持续变化的文本与近邻案例，检查长度和模板竞争解释；几何结构演化仍是主问题，路由分析不能取代它。

### B：用正式SAE快照回放解释链

按plan §3B固定最多每来源32条记录、每记录8个答案预测位置，选择算法与清单在查看输出前落盘。三seed，必要刷新前后及512检查点；SAE字典0/32/64/128/256。先用现有快照前向回放，不先训练新字典。

输出：重构/覆盖、字典与分组变化；旧/新H × 旧/新D/G 的2×2交叉读出；同一词元对的q关系、p关系与实际专家集合变化；每组3正例2反例的规则化文本说明。保护主训练RNG与balance状态，确保只读回放不改模型。使用稀疏top32缓存，避免完整N×30000常驻。

不把warm-start编号当语义身份，不把组号重排当关系变化，不把router结构梯度存在当实际分派已响应；不把任务损失改善当专家效用。

只有噪声问题阻碍判断时，才准备最多6次400步的离线SAE重拟合（seed17，窗口32/256，各3个拟合顺序，同一窗口同一冻结H与前驱D），主模型冻结。先跑比例适当的本地实现检查并估计成本。新离线GPU执行需要明确范围授权；若未给，不提交，交付命令和预算，继续所有无需它的分析。旧buffer缺失则新缓存试验只定位工具稳定性，不写“重现了历史拟合噪声”。

### C：条件性主模型补训，只准备审阅材料

根据A/B给出决策建议。解释旧结果足够则不补训。若必须隔离周期刷新作用，按plan §3C实现六轨迹候选：固定教师函数作用于当前h vs 刷新教师作用于当前h，seed17/29/43，各512步；动态臂32/64/128/256各400 SAE更新；其余参数继承并核验。固定train位置在每刷新点重新前向，修正辅助梯度和零激活图，保存完整教师/优化器/RNG/缓存身份。

这是新比较，不能当旧实验原样恢复。提交前具备完整参数、源码、必要测试、刷新/恢复资格设计、资源与时间估计、失败停止规则、新Protocol候选。协议正式化依赖研究者确认设计；执行依赖本范围明确授权。当前Prompt不批准这六条正式训练，也不批准增加GMM、高层教师或新模型。若研究者另行批准C，使用execution_envelope核定的单节点4×H100 reserved profile/image，持续完成全部六轨迹及结果审计，不停在提交或第一条成功；部分失败如实保留，不缩预算冒充完成。

## 交付物与验收

- `E/audits/0911_minimal_followup/audit_findings.md`：逐项旧结论可保留/应改写/证据不足/需要新对照，指向代码与数据。
- 同目录 `manifest.json`、选样清单、测量CSV/JSON、可复现入口与终端收据；记录源码哈希、命令、单位、聚合、噪声与实际耗时。重算和模型变化分清。
- 恰好两张主图，按plan §4：图一预期与实测的几何演化；图二教师结构变化到路由响应，带规则选取文本正例/反例。PNG/PDF证据副本在执行目录；阅读副本复制至 `/data/250010109/Research_System/daily_research_reports/0911/0911_minimal_followup/figures/`，写SOURCES并用日期本地相对链接。某图关键证据缺失则明确占位，不伪造结果。
- `/data/250010109/Research_System/daily_research_reports/0911/0911_minimal_followup/audit_result_cn.md`：先回答是否补训，再给两图与最小边界、C是否值得做及原因。它是审计材料，不自封正式科学结论；E21 Summary/Detailed需按skill在原实验目录补全资格账本，缺人类判断标明待确认，不能用daily report替代。
- 同目录 `meeting_practice_cn.md`：90秒四段式草稿、30秒读图版、三条常见追问；明示“已测得/候选原因/还不知道”，不给研究者背大量指标。
- 若C必要，同目录交付 `c_execution_readiness_cn.md`：具体可审阅参数/代码/检查结果/提交命令/预算与缺失授权。若C不必要，写清停止依据，不为凑训练计划而训练。

运行适度的正确性检查和仓库 `./researchctl check --repository`，区分本次问题与既有警告。只读审计的完成不能依赖全仓所有历史问题被修复。

最后中文回复先说明：现在可复用什么、必须补什么、有没有真正启动训练；给两张图及各一句读法，然后给唯一下一决策。不要把过程日志当汇报主线，不用无根据的“因为”填补机制未知。
