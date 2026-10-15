# Continuation: 自然语言局部更新结构与共享参数学习

Record: 0930-自然语言统计规律与相容性
Continues from: none
Updated at: 2026-10-02T08:41:24Z | Status: CURRENT (in this record only)
Processed by: Codex (harness: Codex desktop; model: unknown)
Non-canonical: 本文件只提供续接线索；科学判断、设计、授权和结果由其拥有者持有。

## Objective and scope

- Requested deliverable: 承接研究者的新对话，明确大问题及六个小问题的已有答案，再提出下一项最小区分性研究的讨论稿。
- 大问题：共享参数训练中，哪些数据适合一起学，什么时候分开才有净收益；后续能否根据更新前可见的信息作判断。“需要分开”是待检验结论。
- 已有授权：研究者要求整理问题、生成总结和新对话 prompt。本轮初始 Smoke／Full 授权已履行。新的精度扩样、有限更新、多步训练均未选择或授权；研究者科学判断与下一决定 Unknown。
- Writable files / protected concurrent work: 本 brief 和同目录 new_conversation_prompt.md 是本对话的续接交付。接收对话如保存 memory，使用自己的名称和 Continues from，不修改本对话记录。当前 Focus／Anchor／冻结结果及他人迁移工作保持各自所有权。
- Environment: repo=/data/250010109/Research_System; project=/data/250010109/Research_System/Projects/from-attention-to-search; exec=/data/250010109/MoE_Router，当前均可见。文档已迁入 Projects，旧 daily_research_reports/0930/docs 不是当前拥有者路径。

## 大问题下的六个小问题

以下是对已有工作的解释性整理，不创建六个 Focus，也不是强制串行资格门。

1. **自然语言是否存在稳定的平均更新差异？**主 H1 当前不足：T=0.006637，95% 区间 [−0.003738,0.017012] 跨零及 0.01 候选门槛，不能区分差异弱与精度不足。不是没有结构，也不是测量程序失败。
2. **SAE 能显示什么预测敏感性结构？**模型 Fisher 的共同模式很强；去共同均值后有部分领域偏离的跨池对应，是描述性线索。没有确认性功能门槛，未排除组成／来源／抽样等解释，不救回 H1，不证明 SAE 优越、容量竞争或负干扰。
3. **这些 feature 差别是否只是词面／句式组成，原子是否代表确切词？**320 个预选原子的运行后缓存探索发现部分 token／词面关联及反例；一词一原子、唯一语义和因果解释未成立。匹配目标功能单元有不足覆盖，领域差别与组成解释尚未分开。整体自然关系与条件匹配关系都要保留。
4. **更新前表征能否预测学习相容性？**前序指定 pairwise 读出未支持至少 5% 的改善；只限制那个模型状态、总体、读出器和尺度，不证明所有表征无信息。新群体／功能结构是否能提高事前预测仍未知；真实下一词和反向梯度不是 router 的事前可见信息。
5. **实际学 A 后，B 是净获益还是净受害？**已有旧自然文本一步干预主要见平均帮助；受控构造任务的局部不利项也被更大帮助抵消。当前 33B 自然文本这一轮冻结采集，没有实际有限 W 更新，旧结果不能移植。尚未建立一个可迁移的稳定自然净伤害条件，也未证明永远互助。
6. **分开参数多步训练是否更好？**在本次核对的证据中未建立预算可比的共同／分开收益比较。单次梯度负内积、局部不利、领域偏离或一次净伤害都不构成隔离收益结论；局部互助也不封死其他长期结果。

已明确的机制基础：c 与当前预测、真实目标、下游 Jacobian 共同产生 G；K 是共享矩阵梯度内积，仅给小普通 SGD 步的局部一阶作用。SAE 编码矩阵输出 a，提供方向；Fisher 测预测分布对方向的局部敏感性。平均需求、敏感性和实际损失作用是不同对象。

## Read list for the next action

- 必读 [当前 Focus](/data/250010109/Research_System/Projects/from-attention-to-search/main/focus/focus_domain_update_geometry_cn.md)：研究问题及未确认的下一决定。
- 必读 [本轮 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/summary_cn.md)及 [primary.json](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/evidence/primary.json)：当前判据及边界。
- 必读 [本轮 Anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/shared_updates/ntp_statistics_local_compatibility/anchor_cn.md)与 [Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/protocol_cn.md)：对象、双分支、目标条件、科学与执行范围。正文保留的 NOT RUN 属历史登记快照，执行看结果和追加回执。
- 涉及词面／数值／执行资格时读 [Detailed](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/ntp_statistics_local_compatibility/20260930/detailed_cn.md)：词面附件、来源曝光、独立近似、已修复问题。
- 判断事前预测时读 [前序预测 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/natural_ntp_representation_compatibility/20260930/summary_cn.md)：指定读出器的不支持。
- 讨论下一步交叉更新时必读 [旧自然文本方向干预 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/atom_mechanism/20260926/summary_cn.md)及 [受控更新 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/shared_updates/shared_update_conditional_interference/20260927_controlled/summary_cn.md)：避免把已有有限更新当作完全未做。还需核对具体对象和不同检查点，不合并效应量。
- 需要完整对话工作历史时读 [本对话 memory](/data/250010109/Research_System/.research/memory/conversations/0930-自然语言统计规律与相容性/memory.md)全文；它不是科学权威。

## Current work and reusable assets

- 已完成严格 Smoke、Full 和词面缓存探索；本轮 2048 记录／32768 事件，模型与 SAE 均 0 更新。
- 执行根 /data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility；已有 runs/full_initial、runs/smoke_qualified、runs/lexical_readout_01 及 scripts。解释／讨论阶段无需加载模型或调用这些脚本；实现前核对实际源码、训练复用索引和现行资格。
- Full pt-z162gb1w 已完成，不因换对话重提。失败 Smoke 与 DEBUG_ONLY 轮不作为资格；不得用已曝光 R／CONFIRM 重选有利方向或声称新确认。
- 入口检查当前有 20 个 UNTRACKED 项；上述必需路径均可读。不要把本次迁移跟踪问题说成科学失败，也不在本任务中处理他人的重组。

## Next action and completion

- Next authorized action: 使用 reasoning skill，以精炼中文核对六项答案；比较“提高主检验精度”“澄清组成解释”“实际自然文本交叉更新”分别消除什么不确定性，提出一个优先候选及最小区分性设计讨论稿。
- 上一对话 AI 倾向补有界交叉更新：同状态出发，只让 A 更新共享块，独立验证 A 改善、测 B 实际损失并另测反向，用 SAE 看实际位移及带符号作用。此为 AI_PROPOSAL，尚未被选择；不覆盖当前 Summary 对 H1 精度的建议，不自动激活新问题。
- Verification / expected output: 给出目的、候选机制、最强竞争解释、固定／改变对象、来源与读出分离、已有工作复用差异，以及支持／不支持／不足时如何更新认识。将任何新科学选择留给研究者。
- Stop/redirect condition: 缺决定性来源时只限制依赖该来源的判断；其他解释继续完成。远程运行或长期训练需要其具体任务的授权与契约，brief 不提供权限。
- Complete when: 研究者能够区分六项问题的状态，并据一项可审阅的最小方案选择下一研究；不要求拿到支持结果，也不要求把全部后续路线先实现。

