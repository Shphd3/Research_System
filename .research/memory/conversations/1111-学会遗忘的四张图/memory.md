# Conversation Memory: 1111-学会遗忘的四张图

Conversation name: 1111-学会遗忘的四张图
Processed by: Codex (harness: Codex; model: unknown)
Created at: 2026-11-10T16:19:27.888607+00:00
Latest update at: 2026-11-10T16:19:27.888607+00:00
Continues from: ../1109-原子集中正则训练与账本分析/memory.md；../1110-蒸馏路由与自举原子路由训练/memory.md
Environment: repo=/data/250010109/Research_System;exec=/data/250010109/MoE_Router/experiments/20261111_learn_forget_figures

## 2026-11-10T16:19:27.888607+00:00 -- 开始

- Summary: 用户明确授权本地MIG只读前向、只读梯度、离线A表优化及四张图，旧资产只读；四图读法已冻结。
- Current work: 图4与检查点定位；未完成训练只准备代码，不补训。
- Next action: 尽早启动0–10B已存在模型的逐位置前向；CPU并行图3。
- References: /data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/protocol_cn.md；/data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/evidence/protocol_freeze.json。科学判断Unknown。


## 2026-11-10T17:00:38.303785+00:00 -- 四图交付

- Summary: 本地H100MIG3g40GB完成两模型各6个0–10B轨迹状态，另MoE33B与Dense最晚34.076B两个参照，共14状态SHA/strictload/2M逐位置前向。图1恒等式误差1.11e−16；主MoE33B标尺10B掌握率差3.56个百分点，98.7%来自新学会，最晚Dense标尺同方向。所有解释AI分析，研究者判断Unknown。
- Current work: 图2两时点、两模型、16组R4全部完成；原每份1序列和8序列精度敏感性均保留，累计梯度预算收费615.7秒（含失败保守120秒），小于90分钟。图3全部6目标×4起点×30更新已测：lambda1更新映射因47.52%无低频位置无法满足负载；原等权EVAL M1.775444但负载1.257957超约束，固定A的EVAL边缘负载校准敏感性M1.761726、负载1.161573（转导结果）。图4按实际旧区间作图，不补造A0/A4/A1deep的250步数据。
- Next action: 研究者讨论后续模型；没有训练未完造成的本轮待测节点，不提交新训练。单种子、局部梯度、低频分组与学习因果仍分开。
- References: /data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/protocol_cn.md（冻结读法）；protocol_deviations_cn.md（参照、精度和约束澄清）；/data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/results/coverage.csv；/data/250010109/Research_System/daily_research_reports/1111/meeting_report/learn_forget_figures/明早速报_cn.md；/data/250010109/Research_System/daily_research_reports/1111/meeting_report/learn_forget_figures/1111-学会遗忘的四张图_结果.zip（13156374字节、186文件，CRC/SHA/链接核验）；资产analysis_learn_forget_delivery_20261111；/data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/evidence/final_delivery_validation.json。


## 2026-11-10T17:15:48.993759+00:00 -- 追加任务开始

- Summary: 研究者授权追加A逐原子掌握率/router相关、B共同遗忘、C早期存档和D七张中文组会图；只读前向和统计，本地MIG/CPU。
- Current work: followup协议已冻结；旧实验与上一轮输出只读。
- Next action: 先A，再M1–M5，随后B/C和M6/M7；缺失早期Dense不补训。
- References: /data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/followup/protocol_cn.md；/data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/followup/evidence/protocol_freeze.json。研究者判断Unknown。


## 2026-11-10T18:09:53.861011+00:00 -- A–E完成，追加条件协方差谱

- Summary: A/B/C及M1–M7已完成，E新增0.5/3/5B原8序列和10B扩展32与扩展8控制全部完成。用户明确批准扩展独立DEV；旧EVAL完整文档排除。主读法下10B两模型32版均0/120负组对，原8版唯一跨时点负候选32版均转正；全表、稳定帮助10对和96段内容上下文已生成。A关联弱、B共同遗忘11.42倍、C早Dense缺失均在速报。
- Current work: 用户新增F，先完成A–E后已启动4臂DEV/EVAL FFN输入提取；Dense/A0/A5已通过loss/Top2回放，A2进行中。本地MIG只读，参数/bias不更新。F读法先冻结；明确谱越平与熵有效秩越低不能同时作同一判据；低频方向在各模型本层DEV坐标定义。
- Next action: 完成F各自表征/共同A0切片、标签打乱控制、低频子空间及协方差内外拆解；统一结果包小于20MB，raw Markdown便携预览但CSV保留全部行与精度。旧实验、旧ZIP不改，科学判断Unknown。
- References: /data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/followup/protocol_E_cn.md、protocol_F_cn.md、evidence/E_complete.json；/data/250010109/Research_System/daily_research_reports/1111/meeting_report/learn_forget_figures/followup/明早速报_追加_cn.md。


## 2026-11-10T18:26:18.757636+00:00 -- A–F统一交付

- Summary: 全部授权分析完成，新增F的四臂八层谱、共同A0条件切片、标签打乱、低频/高频32/64/128维方向与EVAL方向留出核验齐全。原始条件秩A5<原生<A2顺序0/8，条件/全局秩和低频放大的联合顺序各自2/8、共同A0为0/8；保留反例，不写成已证实机制。A–E结论沿追加速报。
- Current work: 已交付19890531字节、306文件ZIP，CRC/每文件SHA/相对链接/合并表全部CSV单元保留核验通过。raw Markdown为20行阅读视图，完整CSV精度和行保留；F逐臂底表合并到F_statistics.csv。7个新输出/交付资产strict通过。原13.16MB四图ZIP SHA未变；源码数学按用户美元语法通过；151入口0问题。本人全部GPU工作已结束，未训练或更新参数，未提交新资源、未commit/push。
- Next action: 研究者与其AI讨论下一架构，判断Unknown；不以当前谱或局部梯度结果自动启动训练。Dense更早正式存档与旧A0部分250步逐位置数据仍缺失，未造点；任务C明确限定。
- References: /data/250010109/Research_System/daily_research_reports/1111/meeting_report/learn_forget_figures/followup/README_cn.md；/data/250010109/Research_System/daily_research_reports/1111/meeting_report/learn_forget_figures/followup/明早速报_追加_cn.md；/data/250010109/Research_System/daily_research_reports/1111/meeting_report/learn_forget_figures/followup/1111-学会遗忘_追加分析_结果.zip（SHA256 388eb06a93a6e0d1418e9695be1ce2a267d2566b51c509dbd0853339769fdd54）；/data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/followup/evidence/final_audit.json；资产analysis_learn_forget_followup_delivery_20261111；执行日志/data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/followup/evidence/events.jsonl。

## 2026-11-11T00:06:45.211059+00:00 -- 组会前补图完成

- Summary: followup2 四项全部完成。统一损失差图纳入 A5 约 1B 的实测优势及 R04 500 步补算文档区间。原生专家秩比满足早期形成并保持判据，A5 3816 步前向已完成；共同遗忘内容按一个代表窗口做关键词粗分。
- Current work: 已交付 /data/250010109/Research_System/daily_research_reports/1111/meeting_report/learn_forget_figures/followup2/1111-组会前补图_结果.zip（CRC 与逐文件 SHA 验证），PNG/PDF、逐层 CSV、协议与执行回执齐全；11/11 检查点，无参数更新。
- Next action: 组会讨论；不要把相对秩缩减当绝对秩下降或训练收益的已证机制。研究者判断 Unknown。
- References: /data/250010109/Research_System/daily_research_reports/1111/meeting_report/learn_forget_figures/followup2/组会前速报_cn.md；资产 analysis_learn_forget_followup2_20261111；执行根 /data/250010109/MoE_Router/experiments/20261111_learn_forget_figures/followup2。
