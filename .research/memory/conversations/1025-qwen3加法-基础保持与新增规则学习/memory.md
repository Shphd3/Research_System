# Conversation Memory: 1025-Qwen3加法：基础保持与新增规则学习

Conversation name: 1025-Qwen3加法：基础保持与新增规则学习
Source conversation ID: 01a17386-0ea7-75c3-a757-55c83a20cbc4
Processed by: Codex (harness: Codex desktop; model: unknown)
Created at: 2026-10-26T01:34:01Z
Latest update at: 2026-10-26T01:35:51Z
Continues from: none
Environment: repo=/data/250010109/Research_System; exec=/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification; both visible at checkpoint creation.

## 2026-10-26T01:34:01Z -- 统一任务名称并保存已完成阶段

- Summary: 用户要求规范本对话名称并加入memory。已通过当前线程重命名工具核实名称与线程ID；任务名称统一为“Qwen3 加法：基础保持与新增规则学习”。实验目录与B01/I01/P01编号保持原样。本记录是非规范工作记忆，科学结论与执行状态以引用的协议和结果记录为准。
- Summary: 本项目研究同一Qwen3-0.6B Base在基础加法及新增偏移规则上的学习与保持。原严格整段评分为零，r01在看过DEV后修订为首个换行/EOS答案字段，基础起点261/300。B01仅训练block14 Q/K/V/O的81,920个rank8 LoRA参数，基础DEV达到300/300；共同起点为下列B01 endpoint，登记SHA-256为e0b5321c343d88aac3c8118fb400086ee853f2157c58a12d53a3ad77ea1aecbb。I01独立A/B各200步未通过95%连续确认，基础行为明显下降；这些是历史背景，不与P01不同loss尺度直接作因果比较。
- Summary: P01已完成旧输出诊断和三个续训顺序种子11/22/33的N/R配对训练。旧A/B的基础错误均是偏移一致错误与其他整数错误混合。每支固定200步，每步同64A+64基础输入；逐序列平均答案+EOS loss后除128，N基础权重0、R权重1，A系数一致，各支独立空AdamW。结果记录支持本轮操作性条件：基础准确率R相对N平均+99.44个百分点，A平均-2.00个百分点，最大A代价4.00个百分点；逐种子数值、曲线、输出和终点身份均在P01来源中。只支持当前显式基础监督下的行为保持改善，不证明内部加法电路、共同子空间、参数容量或模块独立，也不证明MoE无用。DEV已用于开发，三个种子是训练顺序重复，不是独立预训练重复。
- Current work: 所有授权实验已完成并停止；本次仅改当前对话名称、建立本日志与全局memory增补指针。没有新训练或推理，没有新任务、额外付费资源、TEST推理、MoE/CrossCoder、删除或提交推送。旧实验材料及冻结manifest不修改。用户要求完成后等待审核，不能将本记忆视作下一轮运行授权。
- Next action: 等待用户与主对话审核。AI建议的唯一下一问题为“保持收益是否特异依赖正确的基础监督，而不只是加入额外梯度约束？”这是待决定建议，尚未批准或执行。未来续接先重读拥有者协议/结果与当前用户授权，不能凭memory扩展实验。
- References: `/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/summary_cn.md`：当前已完成轮次的自含中文结论；`/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/protocol.md`：冻结比较、loss与预算；`/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/artifact_manifest.json`：代码、数据、输出及六终点身份；`/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/evidence/independent_audit.json`：工程配对审计；`/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/diagnosis_cn.md`：旧输出完整差值诊断；`/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/independent_learning/i01_ab_seed20261025/summary_cn.md`：独立学习历史；`/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/base_training/b01_lora14_seed20261025/checkpoints/endpoint.pt`：唯一共同起点引用，重用前重新核验身份。


## 2026-10-26T01:35:51Z -- 对话命名规范化与memory路径迁移

- Processed by: Codex (harness: Codex desktop; model: unknown).
- Summary: 用户要求再次检查普遍命名规则并修改memory名称。本轮核对研究对话现有样式，采用“MMDD-模型或研究对象：问题主题”；这属于已有会话惯例，memory contract本身未强制所有会话含日期。对话起始日期为北京时间2026-10-25，因此使用1025，不用本次编辑日期1026。当前线程通过应用工具重命名为“1025-Qwen3加法：基础保持与新增规则学习”。
- Summary: 同一会话日志迁移到本目录；原创建时间、线程ID、既有时间条目和全部科学记录保留。旧目录仅保留指向本目录的兼容符号链接，不产生第二份日志。先前条目中的旧标题属于历史，现标题由本条及页首替代；没有改写实验结论。此处“重塑”落实为标题、目录和当前状态的统一。
- Current work: B01基础起点、I01独立续学、P01偏移诊断与配对基础监督均已结束。P01原始结论与局限保持不变，当前没有运行中的新增训练；本轮只整理名称与工作记忆。全局memory使用新增更正记录覆盖旧指针的效力，不编辑或删除早期增补。
- Next action: 等待用户审核。继续研究的候选问题仍是正确基础监督是否具有特异保持收益；尚无下一轮训练授权。恢复时先核验P01协议、结果、manifest与最新用户指令。
- References: 本目录memory.md是当前唯一实质会话日志；旧路径`/data/250010109/Research_System/.research/memory/conversations/qwen3-加法-基础保持与新增规则学习/memory.md`为兼容入口。命名及日志规则来源为`/data/250010109/Research_System/.agents/skills/research-memory/references/memory_contract.md`。科学证据入口为`/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/summary_cn.md`及同目录protocol.md、artifact_manifest.json；本次未修改。
