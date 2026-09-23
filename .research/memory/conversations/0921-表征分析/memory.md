# Conversation Memory: 0921-表征分析

Conversation name: 0921-表征分析
Processed by: Codex (harness: Codex desktop; model: unknown)
Created at: 2026-09-21T05:00:00Z
Latest update at: 2026-09-22T07:51:19Z
Continues from: `.research/memory/conversations/0920-sae表征空间审计/memory.md`
Environment: `repo=/data/250010109/Research_System` `exec=/data/250010109/MoE_Router`; both roots readable.

Non-canonical working context. Verify science and authorization against the owning artifacts below; the newest entry is current. Historical entries consolidated at the researcher's explicit request, preserving unresolved boundaries and failures.

## 2026-09-21T05:00:00Z -- 领域组会重构（压缩保留）

- Summary: 已读0920 memory及原Codex任务，重构领域主线组会：SALL领域线性读出小幅正差但B/W低于Dense；S7原子集中却领域读出更差，不能声称语义空间改善。S7是重加权续训21B，不能与从零训练支线混接。四张折线/直觉对照图使用配对N8缓存，不混旧P关系面板。
- Boundaries: CKA没有通用相似阈值；K=32是训练预算，不是已证最优维数；子空间并集、模型功能使用和因果机制未检验。用户所指独立原图未提供，无法保证未见图的逐项覆盖。领域小差值的配对不确定性待补。E06—E08结果记录与旧Focus状态冲突当时列交接P0，本次未重新审计其是否修复。
- References: `daily_research_reports/0921/focus_meeting_sae_domain_separation_cn.md`（派生报告/交接，不拥有批准）；该日期`figures/domain_figure_manifest.json`（四图来源）；原科学边界由0920 Focus与A15_17父Anchor及E06—E08合同拥有。21B合格原始证据：`/data/250010109/MoE_Router/experiments/20260920_sae_representation_21b_audit/runs/full_4x5090_retry2_20260921T0200Z/`，不得混入失败根。

## 2026-09-21T05:08:08Z -- 补充实验设计（压缩保留）

- Summary: 已写A领域差异标定、B原子/位置/跨层定位、C条件性子空间检验，状态仍为AI_PROPOSED_NOT_RUN，不能由后续E01授权推及这些提案。最小效应阈值、C主秩/多秩解释和预算未获确认；旧test新增分析只能探索，不是独立确认。
- Boundaries: 原探针使用fit均值中心化+单一全局RMS，不能仅以整体幅值解释S7下降；均值向量范数不是样本范数均值。没有32断崖不证明K不足，尾部得分不等于可恢复语义。不同子空间可有相同类均值，分类/BW不是子空间并集检验。
- Handoff: 新标签映射需将逐shard的token_local_row映射至全局记录，不能直接拼接旧load_observer。原缓存缺K>32的原子ID、完整逐token原生字段及当时的N8逐题预测；如复现探针应沿用冻结C，不重选参数。新E01只补原生Top32和原生均值，未填补全部缺字段或完成A/B/C。
- References: `daily_research_reports/0921/sae_domain_supplementary_experiments_cn.md`为详细提案入口，原会议稿和图谱系为阅读入口。未执行这些补实验或提交/推送仓库。

## 2026-09-22T07:34:17Z -- 共享方向复用实现及smoke修复（压缩保留）

- Summary: 承接0922-sae-feature-analysis，读取其完整memory及仓库0921聊天导出；本轮无read_thread，未宣称在线聊天/附件已核验。新建15_17_01 subanchor、E01 Protocol/Detailed及只读原生支持提取代码。旧缓存top128前32与原生topk32在边界同分时存在ID差异风险，不能直接称原缓存为原生支持。
- Negative evidence: 首个smoke `pt-jztyb3sy` 因零维int64计数器Byte view哈希失败，无有效support批次/科学结果；flatten修复及回归记录在Protocol A1。原terminal的gpu_used=false是默认值错误，实际已GPU加载，不得解释为CPU-only。失败根及source_snapshot_v1保留。
- Historical state: 修复版 `pt-1hi96knu` 此时仅STARTING；当时完整科学判据和full待确认，已被下条A2批准及smoke终态取代。原E06用户修改未动，无commit/push。

## 2026-09-22T07:51:19Z -- 用户要求暂停：补记smoke通过/full提交并显式压缩

- Summary: 用户要求先停止、续写并压缩记忆。本次已终止本会话本地轮询进程，不再监控/分析；**未取消远端full**，也未重提、切资源或设置后续监控。压缩仅去除已被终态/A2取代的等待叙述、重复路径与已解决操作细节；原Created at、历史失败和未决科学边界保留，未改其他对话memory。
- Supersedes: Protocol Amendment A2已承接研究者明确确认，取代旧“指标未确认/full未授权”：固定192条N8、每条256正文token、第8层原生Top32使用频率的样本间平均余弦差ΔR=S7−SALL，2,000次配对记录bootstrap（种子20260922）。合格且同面板S7有效维数更低时，95%区间全大于0才PASS必要条件；上界≤0为FAIL；其余或维数条件不成立为INSUFFICIENT。精确规则由Protocol拥有，不从memory授权。
- Verified smoke: 修复版 `pt-1hi96knu` 于07:39:42Z终态PASS，4 worker合格，每模型16条/4096token、零优化更新；186.92秒，峰值allocated/reserved 3407407104/3535798272 bytes。原生Top32与top128前32支持差异在此smoke为0：边界同分是风险，不是已观测的支持错误。12项本地测试、full聚合对smoke复现及合成绘图检查通过；合成图不是实测证据。
- Current work: full `pt-5snx2hrj` 于07:44:51Z提交，最后平台核验07:47:21Z为STARTING，worker Pending、已分配host、未分配pod IP；**终态与科学结果未核验，不能称完成或PASS**。资源为5090-4-spot（单节点4×5090）、shphd-lite-0911与既有SM120层；每模型192条/49152token，无训练、标签、优化或checkpoint写入。4独立worker，每worker96条，900秒执行安全上限不是排队ETA。当前用户暂停覆盖先前持续追终态的安排。
- Claim boundary: frozen21B S7重加权与原SALL的模型谱系/系数历史不同，不是匹配系数因果实验。复用增加与字典共线/系数协方差解释可并存；PASS仅必要条件，不是机制证明。继承分层面板、记录bootstrap不保证文章独立或训练seed泛化；smoke子集已开发暴露。旧全N8有效维数不能替代当前192条同面板计算。研究者机制判断仍AWAITING_RESEARCHER；没有full Summary。
- Next action: 仅在研究者恢复后，先查**同一个full任务**及其terminal、四worker/stage receipts，绝不因暂停/排队重复提交。终态合格后运行只读`scripts/audit_completed.py`独立核验哈希、余弦/维数/2000次bootstrap与判据，再写E01 summary.md/summary_cn.md/detailed.md及日期本地图/来源。该CPU审计脚本在full冻结后新增，尚未运行，不影响已提交GPU源码快照；工程失败与科学FAIL分开记录。最终机制判断/下一科学决策留给研究者。
- References: canonical Focus `daily_research_reports/0922/focus_sae_shared_direction_reuse.md`；Anchor `Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/15_17_01_sae_shared_direction_reuse_anchor.md`；E01合同/执行账本目录 `Projects/from-attention-to-search/main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E01_shared_direction_reuse_audit/`（protocol.md A1/A2、detailed.md §§11–12）；资源登记 `docs/execution_envelope.md`。只更新本次Memory，不做commit/push，不触碰其他Agent改动。
- Execution entry: `/data/250010109/MoE_Router/experiments/20260922_sae_shared_direction_reuse_audit`；`manifests/current_full_run.txt`指向`runs/full_4x5090_20260922T074451Z`，其中execution_certificate.md、34文件冻结及source_snapshot拥有提交谱系，platform_describe_latest.json为最后已核验平台快照。合格smoke为`runs/smoke_v2_4x5090_20260922T072907Z`，失败为`runs/smoke_4x5090_20260922T072342Z`。独立审计脚本、tests及checks均在执行根，checks/synthetic_plot_only不得用于结果报告。聊天导出 `daily_research_reports/0922/docs/meeting_plans/chats/0921-研究逻辑梳理.md` 仅为背景，不取代合同。
