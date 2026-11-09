# Detailed: A17_01_E02 受限更新工程Smoke

[Summary](summary_cn.md) · [Protocol](protocol_cn.md)

## 0. 快速回顾

修复后作业pt-i3ianttt工程PASS；独立64/64门槛通过。 科学NOT_EVALUATED；研究者采纳Unknown。首尝试明确为工程错误，零训练步；重试保留同profile/四臂/50步，扣除首载荷后1600秒上限。工程资格与真实有限读出分开。

## 1. 对象与术语

L只训练原始末层Attention输出投影矩阵；R8冻结原矩阵，加同位置共享rank8因子，不增加按规则独立adapter。作用是更新后减更新前的答案CE，单位nat/答案；负为这次原始改善。80条数值子面板服务工程读出，不能替代完整dev来源有效性或确认数据。两类未见相对当前任务训练，不指未参与原始预训练。

## 2. Anchor与决策归属

[A17 Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor_cn.md)。研究者选择学习器/状态与科学符号阈值；工程结果不自行关闭Focus或采纳机制。

## 3. 冻结、符合性与修订

授权APPROVED_FOR_IMPLEMENTATION_AND_SMOKE，仅本有界子Agent工程测试；Full/频率/SAE/test不在授权范围。预提交将虚拟更新dev收窄为80条，完整800条能力不变。源码修订01在首pod运行前加强原生全logits/CE守卫；保留原源码与hash。修订02修复每精度基线未恢复的确定错误，并增加实际探针隔离回归测试。源/config/Protocol原hash见各run frozen_sources，英文/中文冻结体在run内归档。失败源码/产物不重写。

| 契约 | 实际证据 | 工程状态/边界 |
|---|---|---|
| Base/tokenizer/data严格当前访问 | 各run input_access | 访问PASS，不证明运行或污染自由 |
| 本地契约 | 重试local_test_receipt | 8项CPU PASS |
| 首提交与GPU | 旧receipt/runtime/failure | 四GPU加载/原生一致已核验，update0探针工程FAIL |
| 重试 | 新receipt、终端/逐臂产物 | PASS |
| 数值/来源科学资格 | 原始探针和窗口读出 | Unknown，无采纳阈值/CI |

未更换载体、目标、四臂、LR、50步上限或80条面板。首尝试0正式训练更新，失败探针不进入汇总。重试是工程修复，不是独立随机科学复验。首载荷保守64秒+重试1600秒+30秒kill宽限=1694秒，不超过原总1800秒；平台排队/容器额外时间另外记录。

## 4. 实际设置

原始资产model_qwen3_0p6b_base，28层HF Qwen3；仅model.layers.27.self_attn.o_proj可训练。L2,097,152权重；R8共享alpha8/rank8/scale1、无bias/dropout，24,576参数。冻结embedding/head/norm/MLP/其余Attention，FP32权重/状态，BF16计算，FP32探针核验。固定下游仍响应投影改变，不保证只影响格式。

data_a17_list_rules_v1：训练4000、dev800；test从未由模型读取。规则可见，prefix仅到答案：，正确词可在列表内但填好答案不输入；只计算下一答案全词表CE。完整dev每规则×未见200条，合并800。

四臂L/R8×AdamW1e-5/1e-4，seed17；betas(.9,.95)、eps1e-8、decay0、clip1。warmup40有效答案，随后常量LR。独立单GPU，无跨臂DDP；micro5×accum4=20答案/步，首末各10。最多50步=1000轨迹训练答案/臂，首末各500，与E01不同batch，不能当作匹配全参数对照。

保存/能力点0/1/2/4/8/16/32/50，训练状态只保存声明参数，加载仍需原Base。8步退出后新进程恢复optimizer/scheduler/RNG/游标/计数；先对照不中断第9步完整状态/metric，再回8步继续正式轨迹。两进程各额外20答案的第9步参照核验不计入正式训练曝光；有限探针和评价计算也独立记录，不混成训练次数。

精度限制：BF16/FP32各自计算来源梯度后再评价，比较包含更新方向和reader两处改变，不是固定同一扰动的读出误差测试；此项为有界工程证据，科学资格未完成。

探针在0/2/8/16：每规则5个独立种子来源，各100条、20答案词各5条，source manifest保留ID/计数，按规则独立抽样，不声明同列表配对。80dev按规则×未见×答案词各1条，结果前固定。普通SGDeta1e-5/1e-4/1e-3，每状态60个来源/步长/精度读出；训练AdamW状态不被改动。每精度前、来源/步长间及结尾恢复参数/RNG；不更新重复5次。

## 5. 指标与判据

工程PASS须范围/计数/原生logits/冻结字节/有限TensorBoard/完整保存/外恢复/分项齐全。明确违反FAIL，缺失INSUFFICIENT。科学近零和源有效性阈值未采纳，原始作用符号仍UNRESOLVED。来源本规则80条面板负号是原始读出，不是完整dev资格，也不支持长期策略结论。

## 6. 证据链

| 读出 | 原始产物/计算 | 观察/资格 | 限制 |
|---|---|---|---|
| 原生/范围/冻结 | runtime、arm_completion | 按实际产物与terminal判定 | 参数位置不是功能名 |
| 开发集能力 | capability/update_*.json；逐条CE/全词表argmax→分项/记录加权合并 | 见下表 | 单seed、固定格式、dev已打开 |
| 有限四格 | probes/update_*.json；after-before逐条与均值 | raw_source_window_readout | 80条工程面板、未采纳精度阈值 |
| 保存与恢复 | checkpoints/manifest、resume_verification | 单独核验实际状态 | 最终50步重新载入未测，不用8步资格替代 |
| 终端 | terminal_verification独立audit | PASS | 工程状态不等于科学结论 |

## 7. 主结果

| 条件 | 更新数 | 顺序未见 | 组合未见 | 合并 | 合并CE | 原始记录 |
|---|---:|---:|---:|---:|---:|---|
| l_lr-5 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-5/capability/update_00000.json) |
| l_lr-5 | 50 | 78.00% | 77.25% | 77.62% | 0.89746392 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-5/capability/update_00050.json) |
| l_lr-4 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-4/capability/update_00000.json) |
| l_lr-4 | 50 | 80.25% | 82.50% | 81.38% | 0.64701936 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/l_lr-4/capability/update_00050.json) |
| r8_lr-5 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-5/capability/update_00000.json) |
| r8_lr-5 | 50 | 73.50% | 73.00% | 73.25% | 1.02801167 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-5/capability/update_00050.json) |
| r8_lr-4 | 0 | 73.50% | 72.75% | 73.12% | 1.02885462 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-4/capability/update_00000.json) |
| r8_lr-4 | 50 | 73.75% | 76.00% | 74.88% | 0.96421549 | [JSON](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/r8_lr-4/capability/update_00050.json) |


分项完整CE/概率和全部检查点在原JSON；不只报告有利终点。有限来源结果保留BF16/FP32、各5批/3步长所有原始符号，并保留精度不一致/实际参数零步等混淆。无确认CI，无专家/SAE分析。

## 9. 阶段与失败分解

首尝试在零步原生、范围/数据加载后，混入上一精度虚拟更新的FP32基线违反同状态契约，守卫停止。新增回归对实际probe检查两精度基线同为原始状态；8/8测试PASS。失败不能反证低秩容量、位置先验或共享假设。重试证据按新run独立核验，不合并失败数值。

## 10. 完整轮次

2026-10-10（Asia/Shanghai）：(1)目的核验受限学习链；(2)L/R8同位置四臂及Base固定；(3)train4000配对载体；(4)dev800/数值子面板80，test闭；(5)首job工程失败0训练步，修复后job pt-i3ianttt当前PASS；(6)科学采纳Unknown，后续窗口/学习器由研究者决定。不是新增频率或SAE轮。

## 11. 解释

LoRA与直接矩阵的参数化/容量/优化均不同；同LR不同实际功能步幅。任何冲突只能归属于当前参数范围、状态和更新尺度。零因子另一因子梯度0合法；全对准确率仍可有残余CE；微小非零需数值审定。

## 12. 能与不能声称

可报告已核验工程行为与固定dev原始观测。不能声称LoRA更优、只改表层、稳定干扰、共同/独特功能、自然预训练、专家必要性、长程频率效应。科学NOT_EVALUATED。

## 13. 下一决策

Unknown：研究者从资格证据选择/修复学习器和早期状态、审定精度及来源判据；记录不授权后续Full/频率/SAE。

## 14. 产物清单

[重试冻结清单](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/frozen_sources.json) · [修复台账](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/repair_amendment_02.json) · [失败保存资产](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_20261009T162413Z/registered_outputs.json) · [完整重试产物](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z)。

实际重试保存资产ID及strict访问：[registered_outputs](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/registered_outputs.json)。

配置hash `81fce24c82c5effa4cc74013113cbece295cc8b8348ac7fabe9db1da5c748530`；实际runner `0ddc70175e069641bb811fbd99b471f17392e487630e06497cb5a3c59b6bcdba`；冻结Protocol `b27e76e749426ea3bf680a8490b608b2b1dbdd2f9698001f79f4a5ff93e042df`。所有checkpoint state SHA256写入manifest并由audit重算；完整原Base GB hash未由本轮重算。无复合科学状态。

## 15. 入口

[runner](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/source/runner.py) · [config](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/configs/smoke_retry_01.json) · [独立audit](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/source/audit.py) · [原始窗口](/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z/raw_source_window_readout.json)。作业pt-bw3s1pxw（失败）→pt-i3ianttt（唯一修复重试）。查询既有作业，不自行再次提交。
