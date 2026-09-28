# Continuation：任务信号作用定位与 SAE／PCA／probe 对照

Record: 0926-共享参数冲突整理分析（01a0db36-5ae0-7e23-8e61-6f154608d8a4）  
Continues from: none  
Updated at: 2026-09-28T02:41:38Z | Status: CURRENT（仅在本记录内）  
Processed by: Codex（harness: Codex desktop; model: unknown）  
Non-canonical：本说明只导航，不持有科学结论、批准或状态。

## Objective and scope

- 下一任务：用**已保存的192次虚拟更新**完成信号／非信号位移与候选表征空间的交叉分析，解释任务相关不利作用被何种帮助抵消。SAE不是要优化的目标；PCA/SVD和线性probe提供不同的测量视角。
- 唯一具体方案：[追加分析 Protocol](/data/250010109/Research_System/daily_research_reports/0928/docs/shared_update_signal_localization/protocol.md)，当前SHA256 `b81893d50079f177217b0b082b6bc2bdf62bf673d5c36ec890ea9390531ce8cf`。这是新一轮事后分析，不改原注册实验。
- 用户当前要求：完成memory、to do与具体计划，交给自己的Agent；本交接尚未执行新增分析。接收“按方案执行”的明确用户指令时，核对本地范围并在Protocol中登记；不要把此说明本身当作GPU提交或科学裁决授权，也不要重复请求已给出的同范围许可。
- 可写：新计划目录的结果文档、新执行目录和0928日期图。保护：原0927的Protocol、Anchor、Focus、Summary/Detailed、原raw和源码；不commit/push。repo=/data/250010109/Research_System，exec=/data/250010109/MoE_Router，当前均可见。

## Read list for the next action

| 来源 | 用途 | 现在必读 |
| --- | --- | --- |
| [新Protocol](/data/250010109/Research_System/daily_research_reports/0928/docs/shared_update_signal_localization/protocol.md)全文 | 完整对象、切分、计算、秩、probe标签权限、分支和产物 | 是 |
| [原Summary](/data/250010109/Research_System/daily_research_reports/0927/docs/shared_update_research_pack/summary_cn.md)；[Detailed](/data/250010109/Research_System/daily_research_reports/0927/docs/shared_update_research_pack/detailed.md)第4—7节 | 核对原完成结果与限制 | 是 |
| [原Focus](/data/250010109/Research_System/daily_research_reports/0927/focus_shared_update_conditional_interference.md)；[Anchor](/data/250010109/Research_System/daily_research_reports/0927/docs/shared_update_research_pack/documents/anchor.md)第4—5、8节 | 保留研究者问题／判断所有权，不从本计划切换科学状态 | 是 |
| [配对补查](/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/checks/pairwise_direction_audit_y4hq_pjj/result.json)及同目录reproduce.py | 复现原生信号／非信号分解；不是新确认证据 | 是 |
| [原Protocol](/data/250010109/Research_System/daily_research_reports/0927/docs/shared_update_research_pack/documents/protocol.md)第5、10—11、15节 | 核对数据与旧判据；不修改 | 实现遇到接口或解释疑问时 |

## Current work and reusable assets

- 已完成：原四卡full run、冻结SAE分析、导师稿润色、配对分解补查、当前计划与memory。未完成：新方案的空间交叉分解、PCA/probe读数、配对区间与新结果报告。
- 关键区别：参数位移≠表征位移≠任务所需变化；b（不随t翻转的位移）含背景及无关变化≠SAE common；原生任务差重构≠更新预测。
- 原执行根：`/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z`。旧作业pt-yzq8kkur已在执行记录中终态成功；本任务不需要重启或新提交。
- 复用：原analyze_full.py的配对bootstrap语义、原common_span.npz、结构a/a_hat和更新da/e；新Protocol第14节给出确切源码与数组。原PCA-32未截数值秩，不能照搬为本轮低秩对照。
- 数据已查看；新切分只防拟合泄漏，不能制造未见确认集。工具失败照实报告，不追加扫参寻找支持。

## Next action and completion

1. 核验用户给接手Agent的执行范围与新Protocol版本，检查输入身份，复现已存I/I1/C_S及配对分解。
2. 只在结构集拟合坐标和probe，固定配置后流式评价全部条件；先做原生分量，后做各工具同秩定位。
3. 新执行输出写`/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/posthoc/signal_localization_<UTC>/`；研究结果写新Protocol同目录summary.md、summary_cn.md、detailed.md。
4. 数值闭合或必需数据身份失败，停依赖结论并留下具名失败；某个工具秩不足或无定位信息，不阻止其他独立分析。

完成标准：全部必需条件有数值或具名失败，四项分解与原损失闭合，有同秩对照及配对区间，三张必要图可追溯；最终回答“任务相关不利作用在哪里、总体帮助在哪里、各工具能测到什么”。不能宣布共同原子因果成立、事前预测成功或隔离有收益。唯一后续科学判断交研究者：这些定位证据是否足以提出针对性表征干预；本轮不执行该干预。
