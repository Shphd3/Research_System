# 执行记录：R01 专家分配

[Protocol](protocol_cn.md) · [English](execution_record.md) · [三部分审计](audit_review_cn.md)

## 提交事实 — 2026-11-06T16:17:35.445885+00:00

**作业`pt-ds9bdaxb`于2026-11-06T16:15:07Z被平台接受排队；GPU实际分配、短测通过与训练完成均尚未核验。**提交是执行事实，不是科学结果。科学接受与机制判断仍为Unknown。

[实际提交回执](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/acp_receipts/submit-hiermoe-depth-ab-1106-20261106T161502Z.json)状态SUBMITTED、exit_code0，平台文字为“submitted successfully, please wait for scheduling”。回执SHA-256为`9e7dcef3cb0efbff23ffbe8f6617f5273ea88c2c0d74cd597854ccf7405ab7ed`。请求元组为envelope的`h100-4-reserved`：单节点4H100／4进程、`n6ls.iu.i40.4`、reserved、当前默认`shphd-lite-0911`镜像。这是请求元组，GPU身份仍需运行pod核验。

已授权入口依次执行共同A／B短测、保存／重载／跨进程重放、不可变共同预算／频率冻结、正式A／B训练与完整评估。用户本轮已授权完整有界范围。短测是工程关卡，既不是结果，也不要求重复审批。本轮不安排C或第二种子。仅排队不满足用户要求的实际启动。

## 提交前已核验的构造

[实际逐层参数CSV](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/parameter_ledger.csv)及[机器账本](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/parameter_ledger.json)枚举隔离适配模型。A为`[8,8,8,8,8,8,8,8]`，B为`[6,6,6,8,8,10,10,10]`，均64专家、hidden1024、中间维度1536、top-2；各层E>k。每专家4,718,592，专家总计301,989,888，router均65,536。唯一全模型总参数507,988,992，均可训练；绑定embedding／输出头只计一次。每层含QK norm的attention6,291,712，block norm2,048。执行CSV层号从0起，易读报告从1起。

[初始张量哈希](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/initial_parameter_hashes.json)支持共同起点核验；CPU检查242共有同形张量及6个异形router的42共有行相等。这不能证明GPU训练有限或断点恢复准确。

[数据manifest](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/data/manifest.json)的SHA-256为`3c0dc6748978ca190ba3334d77799ead1f485da3e1a242d2e4c579d940769ace`，[原字节小副本](supporting_sources/data_manifest.json)记录实际来源。扫描确定性67,108,864token前缀，按边界恢复文档，丢弃8,827碎片／短token、去除16精确重复文档。训练／开发／测试为53,813／528／544文档及65,766,910／630,980／700,308token；最终预测位置700,307。按文档原uint32字节SHA-256取mod100，dev0／test1／train2..99。近重复NOT_CHECKED，前缀不代表全库。完整dev／test整体NLL作为通用验证；原115M holdout本轮NOT EVALUATED。

当前[准备后输入访问证据](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/prepared_data_access.json)与未来checkpoint产出注册不同。[来源审查](source_review_cn.md)保留会议归属。测试metadata／样例已看，模型最终测试指标未用于选设计。

## 冻结、证据与资格

Protocol英文SHA-256为`bdb407cc750afb2ca8920755be364886a59fdaf33f0bcd8e6a0099130d966820`，中文为`04ca3d5cac3216701399402385a2576852b8278093a160efa0dc7baca4485585`。实际共同步数、阈值和runtime哈希待成功双短测后的冻结回执；短测与正式频率使用不同目录，不能由提交记录推断。

此处不声称已有损失、训练checkpoint、有限梯度、负载验收、保存／重放通过、吞吐、ETA或实际GPU分配。下一执行动作是读取本同一作业的持久启动证据。后续实际状态以追加条目保存，包括失败；不重写冻结科学计划。

## 已核验GPU实际进入 — 2026-11-06T16:43:07.344306+00:00

本追加事实更新前述“分配未核验”状态，保留提交时历史不改。作业`pt-ds9bdaxb`的持久pod日志于2026-11-06T16:41:44Z开始，执行证书核验于2026-11-06T16:42:23.410039+00:00。[实际GPU启动记录](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/gpu_startup.json)报告`h100-4-reserved`上4张`NVIDIA H100 80GB HBM3`，每卡85,017,624,576bytes；实际runtime为torch `2.3.0a0+6ddf5cf85e.nv24.04`、CUDA `12.4`。启动记录SHA-256为`73b9eefc8397ade8bde07cd54d6e16256b625e4271187b54f69a6ca3fc5e8c35`。

[GPU进入证书](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/audit/execution_certificate_gpu_entry.json)记录阶段`EMBEDDED_SMOKE_STARTED`、入口`scripts/run_pair.sh`与[持久pod日志](/data/250010109/MoE_Router/experiments/20261106_depth_expert_allocation/acp_receipts/pod/hiermoe-depth-ab-1106-20261106T164144Z.log)。A组短测已launch。此证据确认已实际进入指定4卡H100 reserved；**不表示短测已通过、训练完成、正式共同token预算已冻结或已有科学结果**。这些状态仍待各自回执。继续现有作业，核验后再追加共同冻结事实；本记录不触发重复提交。

## 共同冻结与实际审计范围 — 2026-11-06T17:03:01.834883+00:00

[共同冻结](joint_freeze_cn.md)记录每组229,113,856有效目标、874更新、中点437及正式频率阈值49／447。正式训练已开始；成对终点完成仍为PENDING_RESULTS。

**初始化澄清：**前述`initial_parameter_hashes.json`实际使用seed17，只核验实现规则，不是本轮实际保存的seed20261106初态。独立[真实初态审计](supporting_sources/actual_initial_weight_match.json)在2026-11-06T16:59:42.790524Z检查seed20261106的step0／token0，状态PASS：242个共有参数张量、252个共有状态张量及router重叠行逐位相等，load bias为0、优化器全新。两架构候选路由集合不同，不能据此说初始函数相同。本追加澄清保留旧证据，不改写其种子。

[实际短测审计](supporting_sources/actual_smoke_audit.json)报告A／B已观察更新有限、有效assignment恒等，steps1–3的batch hash一致。名义4步配置下，实际短测均结束于step3／786,432目标；这只是工程短测，不计入正式训练。A连续／外部恢复状态及下一更新逐位相同，未放宽容差；A/dev重载评估8文档／7,331目标的JSON与原始文档数组全部exact。不能扩写为每个B或正式checkpoint都测过外部恢复。

[矩阵profiler核验](supporting_sources/matrix_flops_formula_check.json)在rank0短测更新测得`aten::mm`每token2,000,027,648FLOPs，精确等于6×(激活参数−norm参数)+2×绑定输出矩阵。融合SDPA的QK／AV／反向、其他未计kernel及通信未覆盖。这是实测矩阵工作量，**不是实测完整训练FLOPs**。

[实际注册交接](supporting_sources/actual_output_registration_handoff.json)记录7个已保存短测checkpoint及strict检查过的`checkpoint_family_depth_expert_allocation_smoke_20261106`、`data_depth_expert_allocation_formal_frequency_20261106`；该回执没有注册正式终点或完整分析。约16:55–16:58UTC、formalA刚开始时，SHA核验顺序读取34,545,588,066bytes短测状态。未测其对系统时间的实际影响；吞吐／墙钟比较须保留此外部IO背景。它未改变数据顺序、更新或预算。

[样例检查时序](supporting_sources/sample_review_timing.json)区分正式前的原文／边界检查、自动生成分桶例，以及formalA开始后约67M目标时Codex明确逐例阅读bucket。外部人类review为NOT_PERFORMED。阅读后未改阈值或配置，也未用模型指标选样例。最终报告须保留此时序偏差，不能声称完整人工分桶检查发生在正式训练前。

## 成对完整完成与独立复核 — 2026-11-06T18:01:45.591163+00:00

A于2026-11-06T17:22:01.217476Z、B于17:53:43.402712Z完成；各874更新／229,113,856有效目标。pipeline于17:54:07Z记录COMPLETE；平台最终SUCCEEDED已核验。全部874batchhash一致，规定12组评估完成，最终数值、冻结源码／旧源、独立统计及实际正式初态复核PASS。正式A／B checkpoint家族与分析资产已登记strict PASS。

终点低频B−A为+0.2172100729108415，95%区间[+0.12596861910824345,+0.30035089638778223]；整体+0.014258167152949142[+0.006159870644017267,+0.0256768969077061]。本轮没有低频收益，整体亦更差；原因与机制判断Unknown。完整数值、反向个例、低频自身恶化及所有时序／FLOPs限制由[Summary](summary_cn.md)和[Detailed](detailed_cn.md)持有。此追加不更改Protocol、不关闭科学问题。

## 2026-11-06T18:06:31.028556+00:00 — Final paired completion / 最终成对完成

作业pt-ds9bdaxb已SUCCEEDED，持久pipeline COMPLETE。两组均完成874更新、229,113,856有效目标，起点／中点／终点完整保存与全部DEV／TEST评估齐。874步实际输入／目标／mask哈希一致；最终数值、独立统计、冻结／旧复用代码及正式初态五项审计PASS。正式A／B家族与analysis资产已注册且strict PASS，详见[Summary](summary_cn.md)和[产物manifest](artifact_manifest.json)。旧PENDING条目是其记录时点的历史，不代表当前仍未运行。

终点B−A低频+0.217210、整体+0.014258nat/token；本轮未出现低频收益。科学接受、机制判断、问题关闭仍Unknown，不自动新增训练。完整执行证书保存在执行侧audit/execution_certificate_completed.json。
