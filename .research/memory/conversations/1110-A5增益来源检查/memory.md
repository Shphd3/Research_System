# Conversation Memory: 1110-A5增益来源检查

Conversation name: 1110-A5增益来源检查（用户指定）
Processed by: Codex (harness: Codex; model: unknown)
Created at: 2026-11-10T03:07:57.667008+00:00
Latest update at: 2026-11-10T04:35:05.418401+00:00
Continues from: ../1109-原子集中正则训练与账本分析/memory.md
Environment: repo=/data/250010109/Research_System; exec=/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks; R04=/data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer

## 2026-11-10T03:07:57.667008+00:00 -- 跑前冻结

- Summary: 用户授权6项A5增益来源分析和小探针／字典，禁止主模型训练和改动R04。判读规则、超参数与数值门已冻结；研究者判断Unknown。
- Current work: 输入strict检查及三臂总体NLL一致性门；检查2/3先行。
- Next action: 门通过后计算步数领先与文档块bootstrap，再前向提取冻结宿主和提示探针。
- References: /data/250010109/Research_System/daily_research_reports/1111/meeting_report/a5_checks/protocol_cn.md；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/protocol_freeze.json；R04/evidence/position_manifest_seven.json。


## 2026-11-10T03:09:02.960329+00:00 -- 数值门暂停

- Summary: 跑前协议冻结及资产strict完成；A5/A0通过六位小数门，A1原位置npz量化前NLL4.157614256728676与R04原评估4.157604346902656差9.91e-6。按用户明确边界暂停，不改R04。
- Current work: 检查1–6全部NOT_RUN，GPU0秒；等待研究者对一致性追查或偏差接受的选择。
- Next action: 只有得到用户对数值门处理方式的回复后，才继续依赖分析。
- References: /data/250010109/Research_System/daily_research_reports/1111/meeting_report/a5_checks/README_cn.md；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/stopped_input_gate.json；冻结/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/protocol_frozen_cn.md。


## 2026-11-10T03:11:29.593465+00:00 -- 检查启动门

- Summary: AI分析：A1既有MIG复算缓存与原训练评估微差已追溯并单列；按用户明确接受继续，原数据不改。；研究者判断Unknown。
- Current work: 本项GPU进程用时0.000秒；仅冻结模型前向／小探针。
- Next action: 按原顺序推进未完成项，不改R04。
- References: /data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/results；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/events.jsonl。


## 2026-11-10T03:12:36.667199+00:00 -- 检查2

- Summary: AI分析：等loss步数领先已计算；终点比较臂未达到A5端点loss，1000–2000判据须保留右删失，不能仅凭nat差缩小断言追平。；研究者判断Unknown。
- Current work: 本项GPU进程用时0.000秒；仅冻结模型前向／小探针。
- Next action: 按原顺序推进未完成项，不改R04。
- References: /data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/results；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/events.jsonl。


## 2026-11-10T03:12:51.594646+00:00 -- 检查3

- Summary: AI分析：2000步配对文档区间：A5-A0=-0.044024 [-0.047218,-0.040423]; A5-A1=-0.118495 [-0.122394,-0.114445]; A6-A0=+0.091854 [+0.088927,+0.094469]；仅评估集抽样，不是种子方差。；研究者判断Unknown。
- Current work: 本项GPU进程用时0.000秒；仅冻结模型前向／小探针。
- Next action: 按原顺序推进未完成项，不改R04。
- References: /data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/results；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/events.jsonl。


## 2026-11-10T03:17:40.107883+00:00 -- 检查1前向

- Summary: AI分析：固定分发标签、A0/A1宿主pre-final-norm隐藏态缓存完成；主模型全部冻结。；研究者判断Unknown。
- Current work: 本项GPU进程用时255.643秒；仅冻结模型前向／小探针。
- Next action: 按原顺序推进未完成项，不改R04。
- References: /data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/results；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/events.jsonl。


## 2026-11-10T03:18:37.896441+00:00 -- 检查4

- Summary: AI分析：A5/A1的bias相对集中度变化为0.57%/15.95%，原10%规则触发；分数尺度、组合多样性和bias须单列。；研究者判断Unknown。
- Current work: 本项GPU进程用时0.000秒；仅冻结模型前向／小探针。
- Next action: 按原顺序推进未完成项，不改R04。
- References: /data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/results；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/events.jsonl。


## 2026-11-10T03:24:40.708745+00:00 -- 检查4

- Summary: AI分析：A5/A1的bias相对集中度变化为0.56%/15.95%，原10%规则触发；分数尺度、组合多样性和bias须单列。；研究者判断Unknown。
- Current work: 本项GPU进程用时0.000秒；仅冻结模型前向／小探针。
- Next action: 按原顺序推进未完成项，不改R04。
- References: /data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/results；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/events.jsonl。


## 2026-11-10T03:24:42.014680+00:00 -- 检查1

- Summary: AI分析：A0宿主Δhint_A5=-0.000665 nat；规则套用：泄露不是主要解释。；研究者判断Unknown。
- Current work: 本项GPU进程用时352.974秒；仅冻结模型前向／小探针。
- Next action: 按原顺序推进未完成项，不改R04。
- References: /data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/results；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/events.jsonl。


## 2026-11-10T03:26:12.153246+00:00 -- 检查5

- Summary: AI分析：A6塌缩层bias影响率70.17%，最大gate中位数0.999023；联合判读未同时满足，不强判bias驱动。；研究者判断Unknown。
- Current work: 本项GPU进程用时0.000秒；仅冻结模型前向／小探针。
- Next action: 按原顺序推进未完成项，不改R04。
- References: /data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/results；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/events.jsonl。


## 2026-11-10T03:27:25.785451+00:00 -- 检查5

- Summary: AI分析：A6塌缩层bias影响率70.17%，最大gate中位数0.999023；联合判读未同时满足，不强判bias驱动。；研究者判断Unknown。
- Current work: 本项GPU进程用时0.000秒；仅冻结模型前向／小探针。
- Next action: 按原顺序推进未完成项，不改R04。
- References: /data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/results；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/events.jsonl。


## 2026-11-10T03:31:20.955913+00:00 -- 检查5

- Summary: AI分析：A6塌缩层bias影响率70.17%，最大gate中位数0.999023；联合判读未同时满足，不强判bias驱动。；研究者判断Unknown。
- Current work: 本项GPU进程用时51.705秒；仅冻结模型前向／小探针。
- Next action: 按原顺序推进未完成项，不改R04。
- References: /data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/results；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/events.jsonl。


## 2026-11-10T03:49:37.263339+00:00 -- 检查6a

- Summary: AI分析：24个固定超参数student可读性探针完成；按10个百分点及L7>60%逐项判读，不把分类准确率等同训练收益。；研究者判断Unknown。
- Current work: 本项GPU进程用时1232.472秒；仅冻结模型前向／小探针。
- Next action: 按原顺序推进未完成项，不改R04。
- References: /data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/results；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/events.jsonl。


## 2026-11-10T04:01:17.121671+00:00 -- 检查6b

- Summary: AI分析：6个student自举字典完成，按预登记M阈值逐项判断，未改任何主模型。；研究者判断Unknown。
- Current work: 本项GPU进程用时692.939秒；仅冻结模型前向／小探针。
- Next action: 按原顺序推进未完成项，不改R04。
- References: /data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/results；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/events.jsonl。


## 2026-11-10T04:34:20.328109+00:00 -- 检查交付

- Summary: AI分析：本轮结果ZIP已完成，包体小于20MB，CRC及逐文件SHA校验通过。；研究者判断Unknown。
- Current work: 本项GPU进程用时0.000秒；仅冻结模型前向／小探针。
- Next action: 按原顺序推进未完成项，不改R04。
- References: /data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/results；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/events.jsonl。


## 2026-11-10T04:35:05.418401+00:00 -- 全部检查完成与交付

- Summary: 检查1–6全部完成，40个小探针及6个8192字典已存档；没有主模型训练／续训或R04位置输入改动。AI分析：提示探针按原规则非主要解释；评估文档bootstrap支持本固定模型A5优势，种子方差Unknown；A1 bias干扰规则触发；A6整体未过80%联合条件；6a未过60%及10pp，6b三配置达到1.08，不能直接当NLL收益。
- Current work: 本轮无剩余执行项；最终审计、资产登记、公式检查及ZIP CRC/SHA均通过。交付1667072字节。R04原3个核对位置文件SHA保持一致。
- Next action: 等研究者与其AI讨论下一方案；优先分离score/bias混杂，teacher-free候选需选择同层可因果访问接口，本轮不自动启动主训练。
- References: /data/250010109/Research_System/daily_research_reports/1111/meeting_report/a5_checks/1110-A5增益来源检查_结果.zip；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/final_audit.json；/data/250010109/MoE_Router/experiments/20261110_a5_gain_checks/evidence/delivery_receipt.json；/data/250010109/Research_System/daily_research_reports/1111/meeting_report/a5_checks/README_cn.md及analysis_cn.md。
