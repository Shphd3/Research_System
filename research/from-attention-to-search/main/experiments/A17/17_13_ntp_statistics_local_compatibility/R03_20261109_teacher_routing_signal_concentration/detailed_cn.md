> 当前紧急计划与匹配读数见 [执行事实附录](urgent_execution_appendix_cn.md)。下面保留早期执行快照；旧monitor_status.json不代表当前任务。

# R03 执行记录

正式训练已启动并产生读数；本轮尚未解释科学结果，研究者判断Unknown。早期快照按历史保留；最新执行状态见执行侧 startup_report_cn.md 和 evidence/monitor_status.json。

执行根：`/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/`。精确授权与条件见 [Protocol](protocol_cn.md) 及执行侧 `evidence/authorizing_prompt.md`。

## 当前证据与任务

- share A0对齐Smoke：`pt-ojnhplqh`，提交已确认，等待实际训练证据。
- P12恢复/全部模式Smoke：`pt-w7uc42ce`，按当前对话追加授权并行，提交已确认，等待实际训练证据。
- 训练输入检查：初始状态、原teacher33B、原SAE、DCLM视图和tokenizer限定strict通过。全库strict包含历史缺失，保留为全库快照，不冒充本轮失败。
- DEV/EVAL各2097152位置编码、8簇、feature频率、蒸馏tau和零bias集中度已冻结；完整DEV未量化编码的bf16/fp32 top2一致率通过0.99门。
- 本地工程检查：fixed router无梯度、A4辅助仅router有梯度、hybrid层界、stateless RNG重放、实际input_ids哈希拒错；12项原模型/数据顺序测试通过。不是四卡训练Smoke PASS。
- 原代码复用/改动：`evidence/change_list_cn.md`、`evidence/source_changes.diff`、`evidence/original_code_and_logs_audit.json`。完整原日志已流式扫描，前200步loss与3815步样本顺序独立保存。

## 持久执行证据

`evidence/jobs.json` 映射当前/历史任务，`evidence/monitor_status.json` 保存最近平台状态和实际进度；`evidence/supervision.jsonl` 为追加监督记录。平台成功、训练进度、启动门和全部完成分别记录。`runs/<arm>`保存完整训练状态；`tb/<arm>`保存正式TensorBoard；Smoke位于`smoke/`，其评估不混入正式`eval/`。

## 资产与边界

已登记 `dataset_teacher_routing_dev_eval_20261109`、`representation_teacher_routing_sparse_codes_20261109`、`analysis_teacher_routing_frozen_clusters_20261109`；当前访问回执 `evidence/derived_inputs_access.json`。训练实际存档在完成相应阶段后按发布manifest登记；未保存的计划状态不登记。

fixed臂没有router对表征的梯度回流，权重0.5；teacher训练见过训练前缀；单种子；仅原调度前3815步。DEV/EVAL源分片与训练排除，按预处理分隔token切文档；没有全语料文本近重复穷尽证明。

## 未运行/失败项

正式训练、各GPU Smoke放行门仍待执行证据。初次MIG因分隔token不符在前向前退出；随后修正读取设置并保留失败日志。后台启动方式首次未持续，改用可追踪的前台会话；分片写锁升级时从实际已发布分片接续，没有改teacher/SAE/聚类定义。目标loss阈值、feature家族定义未给出，相关统计Unknown，不造阈值或bootstrap区间。

## 2026-11-09 02:19:33 北京时间：正式启动验证

share `pt-b4vbd8yu` 和P12 `pt-sdk1sj3u` 均已通过250步完整启动门；主链A0从200存档续行，次链A4从共同初态开始。两个allocation内派发正式控制器，未重复ACP create。八臂仍RUNNING，科学解释Unknown，分析按研究者要求暂不展开。

A0前200步逐位同原日志；恢复配对40步完整模型哈希一致；实际A0恢复201–297步同原日志差0。原容差未放宽。全部验证、资产ID、修复和监督入口见 `/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/startup_report_cn.md`。未执行2B。

## 2026-11-09：紧急计划与历史更正

研究者已明确暂停旧链并优先share A2/P12 A1各2000步；两者从共同初始状态正式训练。完整条件、失败恢复、已交付500/1000步匹配结果、三类审计和资产访问证据见[执行事实附录](urgent_execution_appendix_cn.md)。科学判断Unknown，未更新Anchor/Focus。

对早期“八臂仍RUNNING”表述作明确更正：当时实际运行的是A0和A4，其余臂为计划或等待状态，不是八臂同时训练。旧share任务后因通信不一致超时失败，旧P12任务因分数补算失败；旧后台监督也退出。当前以urgent_jobs.json/urgent_live_status.json及新任务持久日志为准。旧存档和原失败证据未删除。


## 2026-11-09：五臂2000步结果归档，按研究者要求停止续训监督

A0/A1/A2/A4/A1-deep的2000步评估已统一；A1/A2均完成2000次更新、完整存档与2097152目标token评估。完整趋势、条件解释与边界见[Summary](summary_cn.md)，来源与实际资产见[执行事实附录](urgent_execution_appendix_cn.md)。早期未运行/等待文字为历史状态。

研究者要求先打包2000步结果、绘制loss并停止续训监督。已停止前台urgent_watch；未停止集群内任务，任务脚本的自动恢复/接续仍保留。后续训练未继续监督，不能宣称已完成。未commit/push，研究者科学判断Unknown。
