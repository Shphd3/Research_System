# 完整记录：A17_03 顺序敏感方向实验

[Summary](summary_cn.md) · [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_03_old_task_sensitive_update/17_03_old_task_sensitive_update_anchor_cn.md) · [Protocol](protocol_cn.md)

证据资格：通过护栏的已暴露dev顺序比较，无盲确认。六案例均NO_ORDINARY_FORGETTING；登记总判定MIXED_OR_NON_SUPPORTING，表示一致防遗忘假设未支持，不表示遗忘符号混合。机制/关闭Unknown。

## 0. 核心结果

六个普通案例均改善旧/新CE；保护策略6/6新CE收益更大，但旧准确率5/6下降。敏感性估计在留出数据有局部覆盖，但不完整；本轮没有普通净CE遗忘可供解释。

## 1. 对象定义

旧敏感性：逐样本CE参数梯度的不居中主方向，敏感无符号，不等于有害冲突。旧D为新训练后减旧终点CE；新G为旧终点减新训练后CE。双答案优势为正确词减错误规则词logit；准确率为全词表最大概率选词是否正确。

## 2. Anchor衔接

同级A17_03比较顺序保持/学习，不给A17_01增加核心轮次。此前局部/联合帮助不推出顺序遗忘，本轮显式检验该新情形。

## 3. 冻结与合规

| Item | Expected | Actual | Status |
| --- | --- | --- | --- |
| Parent / data | exact officialQwen,train/dev | identities matched,no test | PASS |
| Cases / trajectories | 3seeds×2orders,6old+18new | 6/24 | PASS |
| Scientific training | 48000answers,2400steps | independently recomputed | PASS |
| Smoke / externalresume | four workers each,exact1→2 | four PASS each | PASS |
| Stored input / output | all frozen SHA256 | 22 /426 checked | PASS |
| Actual sample order | same2000new records/strategy | exact frozen lists | PASS |
| Parameter scope | one o_proj,frozen others | identical frozen hashes | PASS |
| Norm / constraint | <=.002relative | norm<=3.73e-7,leak<=1.52e-6 | PASS |
| Saved states | old0/16/50/100;new0/1/16/50/100 | 114Full;44Smoke | PASS |
| Telemetry | seven tags,20answers/window |24Full/16Smoke verified | PASS |

冻结英文Protocol SHA256：546d729bafa36e721d21af4d813f817e27ff48b7cdcb569c18047f27c59b5a75. [Run-local contract](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/protocol.md) · [input freeze](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/freeze.json). 无重试、实质修订、秩/阈值调参、缺条件或优化器fallback。事后准确率翻转计数和表格汇总只使用已存终点。

## 4. 实际设置

官方Base，仅第27层o_proj [1024,2048]。FP32完整原生eval梯度/前向，不用尾部近似或SAE。手工SGD LR.01、clip1、无动量/衰减。micro5×accum4，每步20有效答案。60旧训练梯度拟合固定局部rank16；同秩随机；四个H100独立处理案例。旧100步、各新100步，普通提供匹配范数表。暴露dev800条，每规则×面板200答案；旧完整一遍使未见资格成立；test不访问。

[Source](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/source/run.py) · [geometry](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/source/geometry.py) · [config](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/config.json) · [input lineage](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/provenance/input_lineage.json) · [environment/launch](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/execution_certificate.md). 复用已检查E03原生AnswerLM/collate/检查点树/遥测和官方parent carrier/runtime；改造SGD及约束几何；不复用SAE/S7/尾部近似和原AdamW/探针循环。

## 5. 指标与冻结分支

旧收益>=.01、普通新G>=.01、普通D>.01才筛为CE遗忘；保护G>=普通90%且>.01、相对普通/随机旧D都减少>.01才构造性保护。这些是委托运行的操作筛查，不是总体显著性。六案例全支持才一致支持。仅3独立种子，种子内双方向，不做p值/置信区间。

优先分支：旧学习不足、新学习不足、无普通遗忘、构造性保护、新学习代价、无特异保护。本轮全部先进入无普通遗忘；次级新收益不能补救防遗忘前提。

## 6. 证据谱系

| Claim | Source | Computation | Result / boundary |
| --- | --- | --- | --- |
| Complete engineering | [verification](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/completion_verification.json) | counts/hashes/states/tags | complete,not scientific closure |
| Actual matching/exposure | [trajectory audit](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/trajectory_contract_verification.json) | metrics IDs/20-answer windows/norms | same source order/old state |
| Old/new finite CE | [conditions](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/conditions.csv) | same old reference,new endpoint |6noCEforgetting |
| Direction/seed/panel means | [derived](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/derived_results.json) /[panels](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/panels.csv) | seed equalweights,panel equalweights |no population inference |
| CE vs accuracy | [transitions](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/old_accuracy_transitions.json) | fixed per-record correct flips/CE |old accuracy falls despite CE gains |
| Sensitive directions | full/<case>/subspaces.pt,sensitivity_qualification.json | fit/heldoutgradient energy,±finite RMS |partial local CE sensitivity |

## 7. 主要结果

| 顺序 | 新学习策略 | 旧CE改变↓ | 新CE收益↑ | 旧准确率改变（百分点） | 新准确率改变（百分点） |
| --- | --- | ---: | ---: | ---: | ---: |
| 先首项，再末项 | 普通 | -0.078888 | 0.120197 | -1.083 | +5.417 |
| 先首项，再末项 | 旧敏感方向限制 | -0.087984 | 0.142648 | -1.167 | +4.167 |
| 先首项，再末项 | 同秩随机限制 | -0.078887 | 0.120197 | -1.083 | +5.417 |
| 先末项，再首项 | 普通 | -0.082602 | 0.135452 | +0.417 | +4.833 |
| 先末项，再首项 | 旧敏感方向限制 | -0.084757 | 0.156123 | -2.083 | +4.000 |
| 先末项，再首项 | 同秩随机限制 | -0.082602 | 0.135452 | +0.417 | +4.833 |


| Seed/order | Old acquisition | Ordinary old D | Ordinary new G | Protected old D | Protected new G /ordinary | Frozen branch |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| 29 FIRST→LAST | 0.352756 | -0.080087 | 0.122501 | -0.097782 | 1.260040 | NO_ORDINARY_FORGETTING |
| 29 LAST→FIRST | 0.309410 | -0.080453 | 0.133805 | -0.080614 | 1.179325 | NO_ORDINARY_FORGETTING |
| 43 FIRST→LAST | 0.356378 | -0.079286 | 0.118272 | -0.080582 | 1.125715 | NO_ORDINARY_FORGETTING |
| 43 LAST→FIRST | 0.307560 | -0.084562 | 0.134664 | -0.089204 | 1.153423 | NO_ORDINARY_FORGETTING |
| 71 FIRST→LAST | 0.355724 | -0.077289 | 0.119818 | -0.085588 | 1.172165 | NO_ORDINARY_FORGETTING |
| 71 LAST→FIRST | 0.305796 | -0.082792 | 0.137887 | -0.084452 | 1.125879 | NO_ORDINARY_FORGETTING |

| Order | Strategy | Panel | Old D | New G |
| --- | --- | --- | ---: | ---: |
| 先首项，再末项 | 普通 | order_new | -0.081403 | 0.120012 |
| 先首项，再末项 | 普通 | combination_new | -0.076372 | 0.120382 |
| 先首项，再末项 | 旧敏感方向限制 | order_new | -0.088342 | 0.139370 |
| 先首项，再末项 | 旧敏感方向限制 | combination_new | -0.087627 | 0.145926 |
| 先首项，再末项 | 同秩随机限制 | order_new | -0.081402 | 0.120012 |
| 先首项，再末项 | 同秩随机限制 | combination_new | -0.076372 | 0.120381 |
| 先末项，再首项 | 普通 | order_new | -0.082220 | 0.131583 |
| 先末项，再首项 | 普通 | combination_new | -0.082985 | 0.139321 |
| 先末项，再首项 | 旧敏感方向限制 | order_new | -0.087017 | 0.152564 |
| 先末项，再首项 | 旧敏感方向限制 | combination_new | -0.082497 | 0.159682 |
| 先末项，再首项 | 同秩随机限制 | order_new | -0.082220 | 0.131583 |
| 先末项，再首项 | 同秩随机限制 | combination_new | -0.082984 | 0.139321 |

均值均等权3种子，不将6方向当独立。随机CE终点与普通相差约1e-6；随机只移除2M参数空间中极小的一般比例，是同codimension对照，不是匹配旧敏感能量的对照。

## 8. 可视证据

表格足以比较主要CE与准确率判断，不另生成科学图。完整曲线/未平滑遥测保留各轨迹TensorBoard/metrics。

## 9. 阶段资格与失败解释

本地4个反例/对照检查通过；四Smoke、四恢复、四Full通过，无实现失败。估计方向覆盖拟合能量80.9–83.6%，20旧dev平均逐样本能量51.6–61.3%，随机6.27e-6–8.03e-6。范数.01首向量双符号RMS比176.9–528.4。它验证局部信号，不验证剩余空间完全不敏感或后期基底稳定。

未支持的是注册的一致防遗忘标准，因为普通净CE遗忘没有出现。未测试全局必要性、功能划分、SAE、MoE/架构收益、盲重复、Full终点外部续训。准确率退化是实测预测，不是数值失败。

## 10. 完整轮次与执行记录

问题：顺序相反规则学习中的旧敏感限制。设置：同官方Base、旧终点、三策略、双顺序、三种子。训练：登记配对train4k，每旧/新规则各一遍。评价：暴露dev800、名义/实际合格未见顺序/组，不读test。结果：6普通旧CE改善，保护6新CE收益更大但5旧准确率下降。认识：遗忘机制以目标读数实际退化为条件；投影余空间只是估计。下一机制或停止由研究者判断。

作业pt-ubjfxl7c，单节点4H100reserved，UTC2026-10-10T17:16:14（北京时间2026-10-11 01:16）提交，容器Pending后RUNNING，内部Smoke/独立恢复通过才Full。原job成功，无重试/重复提交。按请求监督有限完成，无自动化。

## 11. 推理审定与解释

敏感无符号，不决定有害更新符号，这些方向也可承载有益变化。无CE遗忘使CE防遗忘解释没有现象前提，但不抹去局部准确率退化。Q外新收益仅否定这组估计方向在该有限策略中不可避开的说法，不证明所有实际旧敏感坐标都可避开。CE收益更大但argmax变差，不能叫总体能力更优。随机控制范数/codimension，不控制任意基底选择或敏感能量。固定Q漂移及未覆盖留出梯度保留为竞争解释。主方向不等于功能。

## 12. 结论边界

可说：指定顺序策略对真实旧/新CE、准确率、margin的作用，Q有局部旧CE敏感性，Q余空间允许新学习。不能说：普遍更新必要性、完全旧不敏感方向、共同/独特模块、SAE结论、自然文本遗忘机制、共享/分开专家或计算效率。暴露dev、三种子，依赖优化器/模型/秩/预算。机制/关闭Unknown。

## 13. 下一判断

由研究者决定当前列表对是否结束本CE遗忘入口，或哪个目标读数/竞争解释值得接续。完成标准是明确限定答案和目标性质；从案例/准确率证据接续。只是AI建议，本结果不授权新run。

## 14. 产物清单

| Artifact | Meaning | Identity/completion |
| --- | --- | --- |
| [Frozen Protocol](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/protocol.md) | pre-run body | 546d729bafa36e721d21af4d813f817e27ff48b7cdcb569c18047f27c59b5a75 |
| [Freeze](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/freeze.json) |code/data/parent/sourceattachments |22verifiedfiles |
| [Payload manifest](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/payload_manifest.json) |fullnativearrays/checkpoints/events |426verifiedfiles |
| [Results](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/results.json) |sixcases/frozenbranch |complete |
| [Byte/count audit](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/completion_verification.json) |engineeringqualification |PASS |
| [Source/norm audit](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/trajectory_contract_verification.json) |actualsequence/constraints |PASS |
| [Per-seed table](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/conditions.csv) /[panel table](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/panels.csv) |derivedexistingendpoints |complete |
| [Accuracy transitions](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/old_accuracy_transitions.json) |oldcorrect flips |posthoc arithmetic |
| [Registration request](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/registration_request.json) |40actualcheckpointfamilies+analysis |41assetIDs |
| [Registration receipt](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/audit/registration_request_registered_outputs.json) |actualIDs/318memberhashchecks |complete |
| [Current strict access](/data/250010109/Research_System/assets/checks/2026-10-10_a17_outputs_20261010T172742Z.json) |selected41newoutputs |PASS,notwholelibrary |
| [Execution certificate](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/execution_certificate.md) |resource/command/stategates |complete |
| [Platform terminal](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/acp_receipts/describe_terminal.json) |samejob |SUCCEEDED |

检查点是需匹配Base的矩阵适配状态，不是独立LM；存SGD/RNG/计数/游标/子空间/参考范数信息，Full终点外部续训NOT_CHECKED。Smoke960不计科学48000。原始产物留执行侧，无Git/发布。

## 15. Links

[Summary](summary_cn.md) · [Protocol](protocol_cn.md) · [Execution root](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update)
