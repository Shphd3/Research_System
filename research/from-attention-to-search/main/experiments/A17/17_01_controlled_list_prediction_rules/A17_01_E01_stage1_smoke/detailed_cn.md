# A17_01_E01：第一阶段 Smoke 详细记录

[Summary](summary_cn.md) · [English](detailed.md) · [冻结Protocol](protocol_cn.md) · [Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor_cn.md)

## 0. Quick Recap

job `pt-2m4rvpt4` 于2026-10-09T15:34:48Z完成，平台SUCCEEDED，独立工程审计31/31项PASS。科学NOT_EVALUATED；研究者判断Unknown。本记录涵盖实际运行、原始证据、限制与未运行分支。

## 1. Definitions

模型读可见首项/末项规则与有序三词列表，前文结束在“答案：”，然后预测全词表的下一答案词元。正确词合法出现在列表里，已填答案字段不输入。顺序未见保留训练见过的无序组合但隐藏该顺序；组合未见连无序组合也隐藏。未见只相对于本轮任务训练。损失单位nat/答案；更新后减更新前的负差表示该次读出的改善。合并按答案记录数加权；配对和排列不构成独立科学复验，后续不确定性须处理组合分组结构。

## 2. Anchor Decision

当前研究者决定是验收或修复工程准入；它与稳定帮助/干扰、长期收益、功能分解和专家分工分别需要证据。成功运行不改变机制判断Unknown。

## 3. Freeze, Conformance And Deviations

[冻结清单](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/frozen_sources.json)记录源码、config、Protocol、数据manifest与实际模型实现；远程入口加载前重新核对。没有改源码/契约、重试、排除、失败作业、回退或Full。下面的按编号来源选择属于冻结实现，未在看结果后替换。结果文档的完成不修改冻结Protocol。

数据oracle、实际分词、计数、配对、两类未见均PASS。四rank运行、单答案损失、答案坐标、TensorBoard、16/32保存、16外进程恢复、能力分项/合并与有限四格读出均PASS。来源有效性标记不属于科学支持门；32恢复仍NOT_CHECKED。

## 4. Setup And Data

20词：红 蓝 绿 黄 黑 白 紫 灰 金 银 猫 狗 鸟 鱼 牛 马 羊 虎 龙 花。使用Qwen3 Base分词器，不加chat template或special tokens。逐行确认前文加答案恰为前文ID加一个答案ID；上下文里的词允许多个词元。

生成器用20个内容循环轨道×20次词索引平移×5种顺序生成2,000训练列表；剩余第六顺序按训练轨道的两个不重叠半部分生成顺序未见dev/test各200。每个组合未见划分另用5轨道×20平移×2顺序生成200列表。配首项/末项后为4,000/800/800行。训练每词每位置每规则100次，每评价类型10次。完整有序列表跨划分无重合；顺序未见组合故意与训练重合，组合未见组在train/dev/test互不重合。循环结构用于均衡，不是自然语料或iid证据。

输入ID：model_dense_33b、model_qwen3_0p6b_base、model_s7_fresh_lambda0p1_33b；数据data_a17_list_rules_v1。使用前本地与远程strict访问通过。Dense exact33B为8层/宽1024/FFN3072/281,431,040 LM参数；Qwen为28层/宽1024/FFN3072/596,049,920参数；S7 exact33B含sidecar共342,902,064参数。S7保留原生LM前向，训练目标和历史不同；只读能力，没有SAE特征或表征分析。

Dense/Qwen分别顺序执行四rank全LM参数适配。FP32参数/状态，BF16 autocast；新任务AdamW LR1e-4、betas(.9,.95)、eps1e-8、weight_decay0、clip1；不继承预训练优化器，因此不是原预训练精确续训。micro8×4rank×accum2=64有效答案/步，规则均衡，warmup256答案。种子17、数据1009；各32步/2,048答案，16步/1,024答案保存退出，新四rank进程恢复至32步再次保存。模型禁止test读取。

硬件为1节点4×H10080GB reserved，profile h100-4-reserved，spec n6ls.iu.i40.4，镜像shphd-lite-0911，torch2.3/CUDA12.4与挂载的Python3.10 transformers4.53.3层。进程级protobuf设置修复既有TensorBoard导入兼容，不安装包或改镜像。

## 5. Metrics And Analysis

能力为全词表top1和答案平均CE：每规则/类型200、每类型合计400、每规则合并400、全部合并800。模型仅打开train/dev；test生成与结构核验，不做模型评价。没有科学置信区间、多种子或test选择。

32步后，每规则取32训练样本，以普通SGD步长1e-5从同一权重分别更新全部LM参数；来源梯度为批均值，不修改AdamW状态。接收者为独立dev各规则/类型。来源之间恢复权重与RNG，最后读不更新参照。来源标记只要求同规则合并dev差严格为负，没有不确定性阈值，不能当作科学有效性证明。31项合取定义工程PASS，不要求科学信号、未饱和或来源代表性。

## 6. Evidence Lineage

- [数据qualification](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/data/list_rules_v1/qualification.json)与[manifest](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/data/list_rules_v1/manifest.json)：oracle、分词边界、配对、均衡、未见PASS，仅证明此受控发布。
- [CPU receipt](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/local_test_receipt.json)：10项无效数据拒绝、损失/加权聚合、读取边界及恢复测试通过，不代替GPU证据。
- [平台记录](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/completed_platform_status.json)与[完整pod日志](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/acp_receipts/pod/a17-list-rules-smoke-20261009t152323z-20261009T152934Z.log)：作业成功且实际运行GPU。
- 各模型capability JSON、metrics、TensorBoard、保存manifest和每rank resume receipt：聚合答案计数，核验坐标/保存尺寸/采样权重身份；值见下表，原件见[产物manifest](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/artifact_manifest.json)。
- [Dense更新](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/dense/cross_rule_updates.json)、[Qwen更新](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/qwen_base/cross_rule_updates.json)：实际SGD、重新评价、恢复和不更新参照。
- [terminal_verification](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/terminal_verification.json)：auditor独立读文件与遥测，31项全部通过，科学NOT_EVALUATED。

## 7. Results

### 7.1 能力

每格准确率 / CE，单位nat/答案。initial为任务更新前；final为32步后。S7无final，因为未训练。

| Model | State | Order-new | Combination-new | Combined |
|---|---|---|---|---|
| S7-fresh exact33B | initial | 0.00% / 10.577504 | 0.00% / 10.579289 | 0.00% / 10.578396 |
| Dense exact33B | initial | 0.00% / 10.902297 | 0.00% / 10.91214 | 0.00% / 10.907218 |
| Dense exact33B | final | 100.00% / 0.02564373 | 100.00% / 0.027313172 | 100.00% / 0.026478451 |
| Qwen3-0.6B-Base | initial | 73.75% / 1.0347961 | 72.25% / 1.0303237 | 73.00% / 1.0325599 |
| Qwen3-0.6B-Base | final | 98.75% / 0.053326474 | 98.75% / 0.11264566 | 98.75% / 0.082986065 |

规则分项不被合并值替代：

| Model | State | Rule | Order-new | Combination-new | Combined |
|---|---|---|---|---|---|
| S7-fresh exact33B | initial | FIRST | 0.00% / 10.325733 | 0.00% / 10.330257 | 0.00% / 10.327995 |
| S7-fresh exact33B | initial | LAST | 0.00% / 10.829275 | 0.00% / 10.82832 | 0.00% / 10.828797 |
| Dense exact33B | initial | FIRST | 0.00% / 10.474888 | 0.00% / 10.468495 | 0.00% / 10.471691 |
| Dense exact33B | initial | LAST | 0.00% / 11.329706 | 0.00% / 11.355785 | 0.00% / 11.342745 |
| Dense exact33B | final | FIRST | 100.00% / 0.017565764 | 100.00% / 0.017197206 | 100.00% / 0.017381485 |
| Dense exact33B | final | LAST | 100.00% / 0.033721696 | 100.00% / 0.037429139 | 100.00% / 0.035575418 |
| Qwen3-0.6B-Base | initial | FIRST | 69.50% / 1.1395787 | 70.00% / 1.1232676 | 69.75% / 1.1314231 |
| Qwen3-0.6B-Base | initial | LAST | 78.00% / 0.93001355 | 74.50% / 0.9373798 | 76.25% / 0.93369667 |
| Qwen3-0.6B-Base | final | FIRST | 100.00% / 3.1035646e-06 | 100.00% / 6.5285802e-06 | 100.00% / 4.8160724e-06 |
| Qwen3-0.6B-Base | final | LAST | 97.50% / 0.10664984 | 97.50% / 0.22528478 | 97.50% / 0.16596731 |

Qwen初始216/800个错误，最终10/800，最终错误全在末项；首项100%，合并首项CE约4.82e-6。Dense最终0/800个观测错误，CE约.02648。Dense/S7初始0%表示这个格式下不受限top1没有命中答案，不证明内部没有有用能力。饱和限制更新测量；没有新模板、新词表或自然语言泛化结果。

### 7.2 四格有限更新

单位nat/答案，更新后减更新前。每模型各格来自同一32步基准状态；符号只描述这次有限探针，不判定稳定规则不相容。

| Model | Source → recipient | Order-new | Combination-new | Combined |
|---|---|---|---|---|
| Dense exact33B | FIRST → FIRST | -0.0002076101415 | +5.335594105e-05 | -7.712710023e-05 |
| Dense exact33B | FIRST → LAST | +2.06774519e-05 | -2.567980679e-05 | -2.501177441e-06 |
| Dense exact33B | LAST → FIRST | -0.0001506422108 | +4.551036545e-06 | -7.304558712e-05 |
| Dense exact33B | LAST → LAST | -0.0001632075394 | +0.0001860331221 | +1.141279135e-05 |
| Qwen3-0.6B-Base | FIRST → FIRST | +0 | +0 | +0 |
| Qwen3-0.6B-Base | FIRST → LAST | +0 | +0 | +0 |
| Qwen3-0.6B-Base | LAST → FIRST | +6.496430363e-08 | -3.099544983e-08 | +1.69844269e-08 |
| Qwen3-0.6B-Base | LAST → LAST | -0.01443916529 | -0.02247138387 | -0.01845527458 |

| Model | Source | Combined self-rule loss decreased |
|---|---|---|
| Dense exact33B | FIRST | True |
| Dense exact33B | LAST | False |
| Qwen3-0.6B-Base | FIRST | False |
| Qwen3-0.6B-Base | LAST | True |

| Model | FIRST gradient norm | LAST gradient norm | Gradient dot | No-op loss drift |
|---|---|---|---|---|
| Dense exact33B | 0.6643844322 | 4.19089028 | +0.02294991768 | 0.0 |
| Qwen3-0.6B-Base | 0.0002172169021 | 66.98821593 | -5.305072301e-05 | 0.0 |

冻结runner第176–177行按record_id排序取前32条。直接核验训练记录：首项来源32/32答案为“红”，末项来源覆盖15个答案词。完整训练均衡不等于选出的探针均衡；不能据此识别整条规则的平均作用，没有事后替换来源。

Dense首项→末项合并差−2.50118e-6，但顺序未见为正、组合未见为负。Dense末项来源同规则合并损失上升，来源标记失败。Qwen首项测得变化全0，标记失败；Qwen末项同规则合并改善−.0184553，而首项变化约+1.70e-8未经分辨率资格，两类型符号也不同。来源梯度内积只是该批诊断，不证明规则功能、因果分工或专家收益。

### 7.3 训练、观测与保存

两载体准确完成32步/2,048答案，无非有限值/跳步。没有辅助损失，LM与总训练损失相同。TensorBoard分initial/resume两段，保留答案/更新坐标与优化器/吞吐诊断；审计核对32点及JSON一致。各4份resume receipt确认从16步恢复优化器、scheduler、RNG、计数、采样权重身份及由下一更新编号确定的数据位置。每16/32保存包含state.pt和4份rank RNG。32步重新加载与不中断轨迹对照未测试；保存存在和尺寸核验，大载荷未重新hash。

## 8. Failure Decomposition And Stage Coverage

数据、本地与远程工程阶段均实际运行通过，无worker failure、重试或回退。早先STARTING/Pending/RUNNING记录保留为启动历史；当前状态由completed_platform_status.json更新。包兼容设置在提交前完成。

科学限制分别为终点饱和、编号来源偏置、来源有效性标记失败、单种子/单来源批、BF16读出无校准分辨率带、无置信区间/复验。模型未开test。S7训练、频率、表征/SAE、专家分配与Full为按范围NOT RUN，不是测试失败。

## 9. Completed Round Record

1. 问题/假设：核验条件规则载体和有限链路；经验帮助/干扰未解。
2. 设置/控制：两独立训练载体、第三只读；可见规则、同一列表生成器、均衡训练、四格/不更新/恢复。
3. 数据：4,000训练行，规则曝光相等，每行一个监督答案。
4. 确认划分：800dev分两类型评价；800test生成核验，但模型封闭。
5. 结果：平台SUCCEEDED，31/31工程PASS；能力与有限作用见上；科学NOT_EVALUATED。
6. 洞见/边界/下一决定：载体和执行可用；快速饱和、来源覆盖限制科学。研究者验收/修复工程后选择独立前瞻科学契约。

## 10. Interpretation And Claim Boundary

观测：Qwen已有但不完整的任务表现，Dense快速学会当前载体。待评判解释：32步终点可能过饱和，不适合信息充分的更新探针。初始零的竞争解释包括格式条件化与答案先验，不限于规则能力不存在。

未建立稳定共享/干扰、可复用/差异内部功能、随机初始化习得、干净架构因果、预训练未见、长期收益或专家必要性。有限局部作用到长期决定也要明确桥梁。机制判断保留。

research-reasoning-auditor检查用于阻止“观测→普遍掌握”“单探针→稳定干扰”“来源梯度→规则功能”“工程成功→科学支持”的推理跳跃。欠缺的是科学资格的未检验环节，已完成的数据与实现证据不能描述为不存在。

## 11. Next Decision

研究者唯一决定：验收或修复工程准入。AI建议下一科学Protocol前瞻选较早未饱和状态、均衡独立来源批、校准数值/不更新分辨率与步长，并冻结不确定性/复验和未打开test的使用。未形成科学采纳或Full授权；本记录不再提交训练。

## 12. Artifact Manifest And Asset Lifecycle

[执行产物manifest](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/artifact_manifest.json)记录路径、身份、小文件hash和保存尺寸。输入见[A17快照](/data/250010109/Research_System/assets/checks/2026-10-09_a17_inputs.json)及run内本地/远程检查；数据ID为data_a17_list_rules_v1。

实际保存输出ID：

- `model_a17_list_rules_dense_smoke_20261009t152323z_u32`。
- `model_a17_list_rules_qwen_base_smoke_20261009t152323z_u32`。

选择最终32步，catalog明确列出实际16/32家族、加载器、优化器/RNG、上游输入、源码/config/数据/Protocol/job。2026-10-09T15:38:30.055714+00:00 [strict输出访问](/data/250010109/Research_System/assets/checks/2026-10-09_a17_smoke_outputs.json)通过。GB载荷SHA256未计算，16恢复通过、32恢复未测试；是Smoke状态，不是科学确认检查点。

## 13. Navigation And Reuse

[执行README](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/README.md)、[runner](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/source/runner.py)、[生成器](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/source/data.py)、[auditor](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/source/audit.py)、[config](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/configs/smoke.json)、[执行证书](/data/250010109/MoE_Router/experiments/20261009_a17_list_rules/runs/smoke_4h100_20261009T152323Z/execution_certificate.md)。复用原生Dense/S7 LM实现和分词指纹函数；适配既有DDP、观测与保存恢复模式；新写列表、单答案wrapper、未见分项与真实四格探针。不把原预训练循环直接用于任务训练。源码/原始结果/权重保持执行侧，科学记录在此。
