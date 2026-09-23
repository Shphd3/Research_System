# Conversation Memory: 0922-sae-feature-analysis

Conversation name: 0922-sae feature analysis
Processed by: Claude Code (harness: Claude Code; model: mimo-v2.6-pro)
Created at: 2026-09-22T06:44:25Z
Latest update at: 2026-09-22T06:44:25Z
Continues from: `.research/memory/conversations/0921-表征分析/memory.md`
Environment: `repo=/data/250010109/Research_System` `exec=/data/250010109/MoE_Router`; both roots readable, but the exec-root cache inventory was NOT completed this session (see open items).

## 2026-09-22T06:44:25Z -- 全部停止、进度封存：SAE 共享方向复用审计尚未开始执行

- Summary: 本轮承接 0922 Focus `sae_shared_direction_reuse`（HUMAN_CONFIRMED，问题：S7 的低有效维数是否伴随跨样本同-ID SAE 原子复用增加；竞争解释为 decoder 方向共线/系数协方差）。已完成：(a) 读取 Focus 与 0921 研究逻辑梳理聊天记录；(b) 加载 research-progress-core / problem-anchor-writer / experiment-card-writer / remote-experiment-workflow / research-communication 及其协议与 Anchor 参考契约；(c) 对 0921 阅读面核验了决策数字出处——第 8 层 N8 正文均值有效方差维数 Dense/SALL/S7=15.45/18.63/13.72（定义为协方差特征值参与率，见 0921 结构诊断补充分析）、固定面板曾入选不同原子数 24596/17060/142、S7 为末层重加权（系数 1→0.1）分叉版而非系数消融；(d) 读取 `docs/execution_envelope.md`，确认用户所说的「四张 5090 spot」对应 profile `5090-4-spot`（单节点 4x RTX 5090 Spot，image 默认 shphd-lite-0911，提交入口 `templates/execution/acp_submit_template.sh`）；(e) 在项目仓库（branch Xingyu）只创建了两个空目录：`main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/subanchors/` 与 `main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_01_E01_shared_direction_reuse_audit/`。**subanchor 与 protocol 均未写入**（聊天记录中有 ChatGPT 草稿全文，但只是非规范草稿，从未落盘）；**未实现任何分析代码、未提交任何任务、未运行任何实验**。研究者随后明确叫停全部执行工作，要求封存进度。
- Current work: 已停止。后台资产侦察代理（目标：`exec` 根下 `20260920_sae_representation_21b_audit` 与 `20260921_sae_domain_structure_stage1` 的缓存/逐 token Top-K 原子 ID 可得性/提交脚本盘点）在上一会话退出时被中止，无完成结论——Block B（数据与缓存身份）仍为 BLOCKED。项目仓库有一处**用户未提交修改** `main/experiments/A15/15_17_three_model_sae_representation_trajectory/A15_17_E06_21b_sidecar_representation_audit/protocol.md`，不得触碰或回退。
- Next action: 等研究者重新启动。重启后第一件事：完成 exec 根缓存身份盘点（尤其逐 token Top-K 原子 ID 是否已落缓存，决定是否需要重新前向提取），然后把 subanchor `15_17_01_sae_shared_direction_reuse_anchor.md` 与 protocol `A15_17_01_E01_shared_direction_reuse_audit/protocol.md` 写入上述空目录并保持 `DRAFT_NOT_EXECUTABLE`。停止/转向条件（来自 Focus §6，仍然有效）：主指标、统计判据、同面板缓存身份三项经研究者确认之前，Protocol 不得升格、不得提交任务。研究者此前口头要求的执行链（5090-4-spot 提交 → 结果汇报+认识更新 → 新建文件夹写四段式分析）尚未开始，恢复执行需研究者再次给出。
- References:
  - `daily_research_reports/0922/focus_sae_shared_direction_reuse.md` — 本轮唯一科学状态来源；§6 待研究者决定与 §4 预注册分支决定一切升格与解读边界。
  - `daily_research_reports/0922/docs/meeting_plans/chats/0921-研究逻辑梳理.md` — 非规范聊天导出；含 subanchor/protocol 草稿全文（usage-profile cosine 主指标提案、paired bootstrap 2000 提案），仅为草稿来源，无规范效力。
  - `Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_17_three_model_sae_representation_trajectory/15_17_three_model_sae_representation_trajectory_anchor.md` — 父 Anchor；subanchor 须继承其问题而不得复制其故事。
  - `docs/execution_envelope.md` — `5090-4-spot` / 默认镜像 / 提交入口与门控（PROTOCOL_APPROVED=1 等）的唯一登记处；若恢复执行，研究者的资源决定应记入此处后再提交。
  - `daily_research_reports/0921/meeting_domain_complete/结构诊断补充分析_cn.md` 与 `N8结构诊断阶段I_完整结果报告_cn.md` — 15.45/18.63/13.72 与原子数口径的已核验出处；有效维数=参与率。
  - `PROJECTS.md`（A15_17 行）— 放置说明：subanchor/protocol 在写入项目仓库前不具规范地位。
