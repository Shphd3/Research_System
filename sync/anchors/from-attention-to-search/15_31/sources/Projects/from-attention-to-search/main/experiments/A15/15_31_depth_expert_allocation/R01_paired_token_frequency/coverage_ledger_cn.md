# R01任务覆盖台账

核心A／B训练、评估与报告已完成。UI改名与完整硬件FLOPs不可用；事实与可选条件保留NOT RUN。最终root同步／交接单独记录在第27行，不是实验结果。

[机器可读台账](coverage_ledger.json)

| ID | 请求事项 | 状态 | 证据／owner | 边界／待完成 |
| --- | --- | --- | --- | --- |
| 01 | 会话名／界面改名 | BLOCKED | Task conversation memory and final Summary/brief | 界面改名工具不可用，UI未修改；用户指定名称已用于本任务记忆。 |
| 02 | 本任务研究记忆 | DONE_VALID | .research/memory/conversations/1106-分层MoE长尾学习验证/memory.md | 同名append-only日志已建立，最终事实checkpoint由root追加。 |
| 03 | 会议／旧模型／SAE资料 | DONE_VALID | source_review_cn.md; supporting_sources/source_manifest.json | 无音频，口头质性结果未量化。 |
| 04 | 问题／H1–H3／权限 | DONE_VALID | Anchor EN/CN; Protocol; Focus | 科学接受与机制判断Unknown。 |
| 05 | 指定4H100 reserved实际进入 | DONE_VALID | execution_record; actual GPU-entry certificate | 已核验实际4H100，不仅排队。 |
| 06 | 代码复用／数据tokenizer资产 | DONE_VALID | source_review; actual access/provenance audit | 旧资产未改，新包隔离适配。 |
| 07 | A／B逐层完整参数账本 | DONE_VALID | detailed; execution audit/parameter_ledger.json | 两组507988992，差0%，各层E>top2。 |
| 08 | 真实种子共同初始化 | DONE_VALID | supporting_sources/actual_initial_weight_match.json | 实际seed20261106；旧seed17仅实现资格。 |
| 09 | 真实文档切分／去重 | DONE_VALID | supporting_sources/data_manifest.json | 精确去重；近重复未查；确定性前缀限制。 |
| 10 | 真实曝光分桶／覆盖 | DONE_VALID | joint_freeze; formal frequency manifest | 阈值49／447保留ties，未见单列，低频test1481。 |
| 11 | 样例抽查与时序 | DONE_EXPLORATORY | supporting_sources/sample_review_timing.json | 自动例正式前；Codex逐例读桶在formalA后；无人类review、未改规则。 |
| 12 | 可靠实体／关系／事实任务 | BLOCKED | Protocol and Detailed NOT RUN | 无独立可信出现次数／别名／切分；不阻止token实验。 |
| 13 | 两组短测有限性／负载检查 | DONE_VALID | supporting_sources/actual_smoke_audit.json | 各观察3更新，保留名义4步配置区别。 |
| 14 | checkpoint／恢复／评估复算 | DONE_VALID | actual_smoke_audit; replay receipt | A外部恢复及dev8文档exact，不泛称B／正式恢复。 |
| 15 | 共同超参／预算冻结 | DONE_VALID | joint_freeze; common_frozen.json | 各874步229113856目标，warmup87，test不选配置。 |
| 16 | A完整冻结预算训练 | DONE_VALID | Formal A completion;final_numeric_audit;pipeline_completion | 真实完成874更新／229113856目标；全部成对batchhash一致。 |
| 17 | B完整冻结预算训练 | DONE_VALID | Formal B completion;final_numeric_audit;pipeline_completion | 真实完成874更新／229113856目标；全部成对batchhash一致。 |
| 18 | 起中终点评估／成对区间 | DONE_VALID | frequency_results.csv;independent_final_statistics PASS;figures | 12组模型／checkpoint／split评估，30项成对比较，2000次区间复核最大归约差6.94e-18；低频1481位置分布246／544文档。 |
| 19 | 路由负载／死专家／drop | DONE_VALID | routing.json;Detailed full16layer expert receipts | 每层458227712assignment，drop0／整轮dead0；逐层变化混合，仅相关。 |
| 20 | FLOPs／吞吐／显存／通信／时间 | DONE_VALID | analysis.systems;matrix_flops_formula_check;Detailed systems table | 吞吐／显存／通信／dispatch／墙钟均记录；矩阵按实际算子形状计数，SDPA全量仍缺，保留IO边界。 |
| 21 | 完整硬件指令FLOPs | BLOCKED | matrix_flops_formula_check.json | profiler缺融合SDPA等，报告部分实测与有假设估计。 |
| 22 | 真实checkpoint资产注册 | DONE_VALID | Strict full snapshot20261106T175506021038Z;formal initial audit | 正式A/B家族与analysis_depth_expert_allocation_20261106已注册strict PASS，均含0／437／874状态。 |
| 23 | 可选C／第二种子 | DONE_VALID | Frozen scope excludes them to finish required A/B | 按优先完成A/B计划未跑；单种子限制保留。 |
| 24 | 下一版变宽草图账本 | DONE_EXPLORATORY | next_width_sketch EN/CN and CSV | 393283584仅公式；含投影／绑定头；NOT RUN。 |
| 25 | 完整总结／详细／易读讲稿 | DONE_VALID | Summary/Detailed EN+CN;single daily meeting brief;day README | 原值／差／区间／开销／路由／负结果及短讲稿齐；科学判断Unknown。 |
| 26 | 最终代码／数据／指标可复核 | DONE_VALID | Final numeric/source/statistics/formal-init audits PASS;small source manifests | 冻结8代码／5旧源／11来源hash通过；实际正式初态复核；最终合并artifact_manifest由root维护。 |
| 27 | 阅读包／日入口／记忆最终更新 | DONE_VALID | artifact_manifest.json;delivery_completion_checks.json;execution audit/final_reading_sync_first_pass.json;conversation memory | 本地阅读构建及--check已通过；交接状态更新后再次按精确源字节刷新。仅本地，未发布。 |
