# Continuation: 从研究起点到当前结论的交互教学

Record: 1002-自然语言统计规律与更新相容性：两小时研究
Source thread: 01a0fbc9-0936-7421-8c34-196b19fbb642（本机会话元数据已核对标题）
Continues from: 本记录的memory.md；接收方只需本brief及下列任务来源，不要求重读旧聊天。
Updated at: 2026-10-05T03:44:37Z | Status: CURRENT (in this record only)
Processed by: Codex /root (harness: Codex desktop; model: unknown)
Non-canonical: 本文只指向研究来源，不持有科学判断、批准或状态。

## Objective and scope

- 用户要求新开对话，用6.1 Sol ultrafast教学，要求接收模型深入了解整个研究流程。用户基础停留在10月2日研究起点，今天有约8小时，包含公式推导与证据抽查。
- 本机模型目录将组合表示为gpt-6.1-sol、Ultra reasoning、Fast service（priority）。不能把它说成已验证的API service_tier=ultrafast。
- 已授权：新建并启动教学对话、读取研究来源、解释推导、随堂提问和纠错、保存必要教学进度。没有由本次教学新增远程运行或科学状态转换许可。
- 首轮先准备来源并教第一小段，再问一道理解题，等待用户作答。不要替用户回答题目或一口气灌输八小时内容；不另派代理。
- 写入边界：新对话若写学习进度，应在核对自己标题后建立自己的记录，Continues from指向本记录；不得覆盖本对话memory或canonical科学记录。需要更改研究路线时交还研究者决定。
- 环境：repo=/data/250010109/Research_System；exec=/data/250010109/MoE_Router，均可读。当前源代码与图/原数组属于执行侧，本次无需实现或训练。

## Read list for the next action

下列B=/data/250010109/Research_System/daily_research_reports/1002/candidates/ntp_representation_update_channels。首次教学前完整读指南、过程、最初报告、共享主报告和认识更新；读Anchor与三份Summary确认当前设计和裁决。理解依赖按指南，而不是按文件日期机械讲述。

| Path or section | Why | Required now? |
|---|---|---|
| /data/250010109/Research_System/daily_research_reports/1005/learning_guide_cn.md | 8段480分钟安排、完整推理链、18条展示公式、手算、自测和下一决定 | yes, full |
| B/research_process_cn.md | 逐步为何做、曾失败什么、为何改方向；不得把AI选择写成必然推论 | yes, full |
| B/research_report_cn.md | 10月2日起点，原生更新作用及SAE边界 | yes, full |
| B/sharing_routing_report_cn.md | 当前选择、条件风险、分组学习、容量与资源的主论证 | yes, full |
| /data/250010109/Research_System/daily_research_reports/1004/cognition_update_cn.md | 最新匹配/幅度结果、Adam、未来反转、习得保持与窗口终点 | yes, full |
| B/anchor_cn.md | 当前科学问题与设计所有者，不由教学改变 | yes |
| B/probe_33b_summary_cn.md; B/probe_33b_group_summary_cn.md; B/router_shrinkage_summary_cn.md | 三项实测结果与条件边界 | yes |
| B/source_transfer_addendum_cn.md; B/domain_response_structure_cn.md | 来源A/B、99.02%与严格目标前信息 | before session 3 |
| B/mathematical_analysis_cn.md; B/sharing_routing_mathematics_cn.md; B/capacity_mathematics_cn.md | 推导细节，先对象后符号，保留全部条件 | before corresponding derivation |
| B/capacity_report_cn.md; B/protocol_cn.md | 六臂控制、精确合同和历史授权，不把旧许可延伸到教学 | before session 6 |
| /data/250010109/Research_System/daily_research_reports/1004/evidence/final_window_status.json | 截止时正式轨迹0/12与端点读数0/18 | before reporting execution status |

## Current work and reusable assets

- 学习指南与前两天研究记录已commit/push：b1bcd933f8540512f995a966f134f3fcb7b2c1db。指南CN SHA256=528de032ceb9bd5072706b0050e6f096e1e63ffff98ad6a61b77e4e569f0b1c1。若来源有新变更，读取当前源而不是固守brief。
- 学生尚未完成任何模块或测验，不能把计划写成已掌握。12题20/24只是教学建议，不是科学或掌握认证阈值。
- 最新执行事实限定截至2026-10-04 17:48:35 UTC：pt-scl8ek3y资格失败；恢复pt-c44kwvx3等待后停止，SUSPENDED；正式轨迹0/12。教学不需要新查平台或重提任务。
- 防止五种误读：Q不是CE收益；99.02%不是四域共同知识比例；胜使用率随机不等于胜共同；11/12回退不是新路由成功；平方损失反例不是LM实测。
- 区分三批对象：旧单S7本身也是33B-token；新Dense/fresh S7/SALL三模型固定库；另行随机初始化的容量六臂。均不能混同。
- 新固定库92跨来源条件胜使用率随机但输共同；184组内诊断保留匹配而仍输共同；幅度12选11退回共同，24评价22精确共同。以Summary核对，不把次数当独立重复。
- 资源、机制、实用阈值和下一科学优先级由研究者确认。AI建议先补齐原共享/私有完整轨迹，仍是建议。
- 已验证数学源码和链接；根导航有1项既有无关Diffusion文献未跟踪，不要求学生修复。图/CSV不在Git，不应把缺图当正文证据不存在。

## Next action and completion

1. 接收当前用户任务，确认模型实际为gpt-6.1-sol、Ultra、Fast；按上表载入完整必要来源。
2. 第一轮用简短中文建立研究地图，再讲第一个具体问题：为什么研究数据关系要先固定一处更新，测量对另一文本的作用。一次只问一个问题，等学生答后再纠错和推进。
3. 每小节按“为什么需要→对象→最小例子→推导→实测→不能推出什么→一道题”讲。先定义CE/梯度/条件期望，不假设用户已理解两天新增内容；也不重复无关基础。
4. 保存进度时记录学生实际回答、错误和仍待掌握项。用户随时提问时先解答，再回到主线。
5. 本次交接完成条件：新对话已经持久化，实际配置核验，必要来源可读，第一轮已经开始教学并留下第一个问题。不会把八小时教学本身在无人应答时自动完成。

## Handoff completion — 2026-10-05T03:48:57Z

新独立教学对话已创建且首轮完成，名称「1005-研究学习：从更新作用到共享与路由」，ID `01a10a2a-b783-7752-9149-ed2ffd48a40a`。实际创建配置为gpt-6.1-sol / ultra / priority（Fast）。完整必要来源读取已观察，当前停在模块1第一道理解题，等待用户作答；不是全部课程完成。详情见同目录`teaching_thread_receipt_20261005.json`。
