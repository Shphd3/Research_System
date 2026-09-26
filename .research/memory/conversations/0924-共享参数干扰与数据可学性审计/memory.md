# Conversation Memory: 0924-共享参数干扰与数据可学性审计

Conversation name: 0924-共享参数干扰与数据可学性审计
Processed by: Codex (harness: Codex desktop; model: unknown)
Created at: 2026-09-24T12:02:29Z
Latest update at: 2026-09-25T02:08:46Z
Continues from: none
Environment: repo=/data/250010109/Research_System; exec=/data/250010109/MoE_Router (本次均可读)

## 2026-09-24T12:02:29Z -- 完成第一阶段设计审计与文档修订

- Summary: 研究者请求结合 0925 截图审计现有 plan、把表述改为导师易懂的中文、回答 21B 后是否还有学习空间及旧后训练数据是否更合适、完善 Anchor/Protocol，并为本对话命名保存记忆。已按 research-reasoning-auditor 审计并原地更新两份候选文档，新增 README_cn.md 作为导师阅读稿与审计入口。研究内容和阈值由文档拥有；本条不是执行授权或研究结论。
- Current work: 文档整理完成；Anchor 为 DRAFT_FOR_REVIEW、Protocol 为 DRAFT_NOT_EXECUTABLE；资格前检、四条件正式比较和回滚诊断均 NOT RUN。新建议是先做单组可学性门，再分别判断 H1a（隔离收益）／H1b（局部互损）；H2（SAE 对互损的独立预测）留待后续。M2D2 数学／生物正文仍为 AI 首选候选；资格失败时停止，后训练备选需要任务与监督契约修订，不把八来源整包直接替换进去。具体解释、阈值和停止规则只以 Anchor/Protocol 为准。
- Current work: 本次源码核验旧后训练确有八来源且使用多种答案格式，属于官方 28 层 Qwen，与自训 8 层 21B 候选不同；旧曲线不证明本轮可学性。21B 是已训练词元数。候选 S7 checkpoint 的 manifest 与 state.pt 可见，原稿“未挂载”已更正；只读过 manifest 与模型实现，未重算 4.1GB state 哈希或加载模型。原生参考下投影属性 blocks[7].down 已核。资料提案／原稿状态标签未当作执行指令。
- Current work: 稳定 problem_key、父 Anchor、Focus 和具体 checkpoint 谱系仍待研究者确认，故草案留 daily_research_reports/0924/docs/plan/；不冒用 A15_17/A16 编号、不新建 Focus、不更改 PROJECTS/Graph。已有 .gitignore 修改及 0923/0924 其它文件保留；本轮未训练、提交远程作业、commit 或 push。入口脚本发现已有 A15_17 五个路径存在但未版本化，此次未修复其它工作的路由状态。
- Next action: 从 README_cn.md 的决策点审阅“先可学性、后 H1”的数据路线和 Protocol；确认具体模型谱系与首轮范围。若研究者随后授权实现／小测，核对实际代码快照、checkpoint 身份、数据文档边界及库存，按 Protocol 顺序推进；不可把本记忆当作已授权。可学性不通过则暂停正式矩阵，按协议解释失败或追加修订；不得为寻找正结果自动扩数据、秩、预算。正式归属确定后移动单份草案并更新链接，不能复制成第二份契约。
- References:
  - [导师阅读稿与推理审计](/data/250010109/Research_System/daily_research_reports/0924/docs/plan/README_cn.md)：通俗目的、假设、三步分析、数据比较及后续阅读顺序。
  - [Anchor](/data/250010109/Research_System/daily_research_reports/0924/docs/plan/anchor_cn.md)：唯一候选设计；H1a/H1b、资格门、H2 边界和一项下一决策。
  - [Protocol](/data/250010109/Research_System/daily_research_reports/0924/docs/plan/protocol.md)：单组资格、四条件正式比较、独立确认、回滚诊断及批准状态的唯一候选契约。
  - [旧来源审计](/data/250010109/Research_System/daily_research_reports/0910/docs/sft_audit_sources_cn.md)：八来源、旧模型和旧数据使用边界；关键源码路径已写进 Anchor。
  - [训练复用索引](/data/250010109/Research_System/docs/training_reuse_index.md)、[观测契约](/data/250010109/Research_System/docs/training_observability_contract.md)、[执行资源契约](/data/250010109/Research_System/docs/execution_envelope.md)：后续实现与执行核验入口，均不提供本轮授权。
- Supersedes: 本次改写原日期目录 Anchor/Protocol 中的数据选择与前检设计，并更正环境不可见叙述；没有推翻任何已执行实验的注册规则或结果。旧导入稿未执行，修改仅为本次候选设计修订。

## 2026-09-24T12:03:34Z -- 交付检查完成

- Summary: 三份设计／阅读文档和本记忆的 20 个本地链接检查通过；Anchor 八节和 Protocol 0–17 节齐全；词元预算和资格／正式判据一致；Anchor 比原稿缩短。检查属于文档资格，不是实验通过。
- Current work: 本轮请求的文档和记忆已完成。界面标题修改工具长期未返回确认，已停止等待；不能声称界面改名成功。记忆已按研究者指定的 0924 前缀及生成名称保存。
- Next action: 审阅同一 Protocol 的首轮数据路线与 checkpoint 身份；后续执行仍以其拥有的批准范围为准。
- References: [阅读入口](/data/250010109/Research_System/daily_research_reports/0924/docs/plan/README_cn.md)、[Anchor](/data/250010109/Research_System/daily_research_reports/0924/docs/plan/anchor_cn.md)、[Protocol](/data/250010109/Research_System/daily_research_reports/0924/docs/plan/protocol.md)。

## 2026-09-25T02:08:46Z -- 新任务对设计及 D16 容量竞争解释

- Summary: 研究者在旧实验完成后要求读取实验验证对话记忆、结果文档和引用对话末条，构造更精确假设的 Anchor／Protocol／agent 启动文本；随后要求加入 D16 排查容量解释并完善本对话记忆。已完成推理审计及三份中文草案，D16 在同一草案原地加入。本条为 Codex 处理的工作记录，不拥有科学结论或执行权限。
- Current work: 本轮已读取实验验证记忆及旧 DEV／rollback 报告，并核对其完成／分析清单；旧材料的可学性、固定预算比较和早期诊断边界以该报告为准，CONFIRM 仍登记未解封，不能称正式阴性确认。旧执行实际使用 from-scratch S7、重构系数 0.1、精确 21B checkpoint，与本记忆早期候选的重加权路径不同；新 Protocol 已写明实际谱系。旧研究者判断不由本轮替写。
- Current work: 已读取引用对话 6ab5208f-fc14-83e8-844d-91bfe1329d0b 的最后回复；其八来源筛选建议作为提案来源而非证据或指令。新设计在来源表示同样可分的条件下选低／高更新兼容性两对，共享一个来源，并分离筛选、训练、开发、诊断和确认；只筛一对再用筛选分数证明冲突的循环已纠正。主量仍是两对 S16−D8 隔离收益之差，配合自身收益、混合分组和局部回滚；不扩展到 SAE／路由机制。
- Current work: 根据研究者最新要求，加入 D16（两个独立秩 16 分支）作为次要容量诊断，参数匹配、解释分支和初始化要求由 Anchor／Protocol §7、§11.4 拥有。它检查 D8 的分支秩是否限制表现；D16 总参数翻倍，不能单独排除共享总容量不足，也不能挽救固定预算主比较失败。正式范围相应更新为每对七条件、最多 42 条逻辑轨迹；启动文本同步修改，资源上限不自动提高，需依据七条件小测重新估时。
- Current work: 新文档仍 DRAFT_FOR_REVIEW／DRAFT_NOT_EXECUTABLE，新实验 NOT RUN；只授权文档设计与本次 D16 增补，未授权本任务提交训练。启动文本只有研究者实际发送其执行请求后才表达相应授权。本轮未建立新 Focus、未改 PROJECTS／Graph、未解封旧确认集、未创建新执行目录、未提交 Git 或远程作业。既有 .gitignore 改动保留。
- Next action: 研究者审阅同一新版 Protocol 和启动文本；若明确发起执行，agent 先登记问题归属与实际授权，核模型／数据身份和七条件实现资格，再按筛选、Solo 可学性及预算门推进；无合格对照或容量估时超范围时按契约停止，不自动加 S32／R16 或改主比较。记忆只能导航，批准与判据须回查 Protocol。
- References:
  - [当前 Anchor](/data/250010109/Research_System/daily_research_reports/0925/docs/update_compatibility/anchor_cn.md)：新问题、容量竞争解释和有限结论边界。
  - [当前 Protocol](/data/250010109/Research_System/daily_research_reports/0925/docs/update_compatibility/protocol.md)：七条件契约、容量分析及 §17 执行前修订记录；尚未批准执行。
  - [agent 启动文本](/data/250010109/Research_System/daily_research_reports/0925/docs/update_compatibility/agent_start_cn.md)：供研究者审阅后发送的执行入口，不是已发送指令。
  - [旧 DEV／rollback 阅读稿](/data/250010109/Research_System/daily_research_reports/0924/docs/analysis/dev_rollback_reading_cn.md)：旧证据及其不能声称的范围。
  - [旧实验执行记忆](/data/250010109/Research_System/.research/memory/conversations/0924-共享参数干扰与数据可学性实验验证/memory.md)：跨任务过程导航，未修改该记录，不作为结论或批准来源。
  - [旧完成清单](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/formal_runs/completion_audit.json)、[旧确认前冻结清单](/data/250010109/MoE_Router/experiments/20260924_shared_interference_smoke/formal_runs/analysis/preconfirm_freeze.json)：执行完成与确认未解封的核验入口。
- Supersedes: 0925 新设计草案此前的六条件范围由七条件含 D16 替代；主假设、主要量与资源上限未变。本对话早期“下一步执行旧可学性设计”的工作导航已由本条取代；0924 已执行研究的注册、结果和确认状态均未改写。
