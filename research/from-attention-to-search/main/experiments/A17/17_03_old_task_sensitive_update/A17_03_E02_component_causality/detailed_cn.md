# Detailed：A17_03_E02成分因果完整证据

[English](detailed.md) · [Summary](summary_cn.md) · [Protocol](protocol_cn.md) · [小型来源清单](artifact_manifest.json)

Primary Anchor：[17_03_01](../../../../problem_anchors/17_shared_and_interference_learning/17_03_old_task_sensitive_update/subanchors/17_03_01_component_causality_anchor_cn.md)。冻结正文：[run内Protocol](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/protocol_frozen.md)，SHA256 `5a2d33e67b66ab9ce8d8c585309bdd955ef397b71e33c7e3f5d49adb5428f773`。结果资格：**ELIGIBLE，限冻结状态的已暴露dev有限干预**。AI解释完整记录；研究者机制裁决、下一决定和问题关闭Unknown。

## 0. 快速回顾

目的为区分删除旧敏感成分和放大剩余成分的作用。H1预期删除本身改善新dev CE，竞争解释是放大才补偿删除代价。630/630条件、全部资格通过后，6案例的平均删除收益均负、放大均正；合并−0.000353638/+0.000589189/+0.000235550 nat。H1在这些案例均值上不支持，放大补偿解释得到局部干预支持。总优势4案例正、2案例负；旧accuracy代价没有按原长期方向重现。本轮不完成100步轨迹机制归因。

## 1. 对象、计算与读数

| 对象 | 获得及用途 | 单位/边界 |
| --- | --- | --- |
| full | 来源20条答案CE平均梯度，经原SGD系数裁剪得到一次位移 | 参数位移，不是新训练轨迹 |
| in/out | 固定秩16旧敏感Q中的投影及其余量，二者和为full | 敏感无帮助/伤害符号 |
| out_norm | 将out放大至full范数 | 删除与放大共同组成原限制操作 |
| random_norm | 同秩随机基的余量，匹配full范数 | 未匹配移除的梯度能量 |
| access/selection | CE精确词对分解的两目标梯度，使用同一CE裁剪系数 | selection就是数学choice；存在交叉作用 |
| margin | 正确词logit减相反规则答案logit | 不等于全词表准确率 |
| b/h | b为两正确margin均值，h为朝新答案的平均偏向 | m_new=b+h，m_old=b−h；输出坐标不是模块 |
| Gdelete/Gamp | 新CE(full)−新CE(out)，新CE(out)−新CE(out_norm) | nat/答案；正表示后者更好 |

CE=access+selection，selection=softplus(−margin)。平均selection不能由平均margin代替。不同方向的实际参数干预建立指定条件的效果；目标损失可加不证明两个独立机制。

## 2. 父问题与决定位置

父问题是共享更新如何帮助或损害不同预测要求。本轮补齐“同一更新中删除与放大分别造成什么”这一局部因果边，不将原没有普通CE遗忘的E01改写成遗忘实验成功。是否进一步解释旧错误修复的轨迹变化，仍由研究者决定。

## 3. 冻结、执行符合性与偏离

| 注册项目 | 实际证据 | 状态及资格 |
| --- | --- | --- |
| 同旧状态、同来源梯度、每单元恢复 | 全部source20重测相同，矩阵恢复、冻结版本/哈希通过 | PASS |
| 6案例×3批×7方向×5尺度 | 630个完整manifest；无遗漏或替换 | PASS |
| Smoke后独立Full | Smoke140单元＋4独立重放；另作业Full | PASS |
| 数据train/dev与test边界 | 固定原ID与hash；test未读 | PASS；dev已暴露 |
| 主尺度1、分别/合并两面板 | 保留所有case/panel/batch；不挑尺度 | PASS |
| 计算规则与分析 | Protocol先冻结；汇总脚本首次正式汇总前记录hash，逐条独立复算1296标量 | PASS，最大差1.11e−16 |
| 分析而非训练 | 0训练更新；504000 dev、12600来源干预读数 | PASS；其他前向用于基线/恢复 |
| 事后轨迹衔接 | 第一实际步核验、原1/16/50/100步回看 | BOUNDED附加描述，不改主要比较 |

没有重试、排除、改阈值或新增条件。均值、符号和余项按原合同解释。脚本的1e−8三态符号标签仅用于数值显示，不当作总体显著性门槛。独立审计见[full_engineering_audit](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/analysis/full_engineering_audit.json)。

## 4. 实际设置

官方Qwen3-0.6B Base，28层，仅末层`model.layers.27.self_attn.o_proj.weight` [1024,2048]可变。完整FP32原生前向、eval、SDPA、TF32关闭。数据为三不同词列表，FIRST/LAST提示在答案前可见，只读单答案词元。每规则dev400条，其中未见顺序/未见组合各200；输入列表与训练分开。3种子29/43/71各双顺序。旧模型来自E01完整2000答案旧规则阶段的update100。

每案例来源为原new_order前60条，拆3批20。完整梯度由micro5累积除20，eta_eff=0.01·min(1,1/||g||)，无动量/衰减。7方向独立施加，尺度−0.1、0.1、0.25、1、4，主尺度1。out的放大倍数范围1.188920–1.851537，18批均值1.461656。归一化只用于out_norm/random_norm；access与selection不分别归一化。

Config SHA256 `3bb5337c5dad82beb7d51b9a1dd9c1507d0d8d789474ae8c7ef60d903201d1a5`。模型、tokenizer、数据、6旧状态及分析基底共10输入资产ID完整列在[manifest](artifact_manifest.json)及[freeze](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/freeze.json)，43个冻结输入重新哈希通过。保存的状态、原基底及数据没有重训或修改。

## 5. 指标与判定

正Gdelete/Gamp分别支持指定案例的删除/放大CE收益；两项之和为总收益，不计算接近零时的贡献百分比。不强制六案例同号才允许有界解释；也不把6案例当6个独立种子。每案例先等权平均3批，随后按种子和顺序等权。准确率用百分点；margin变化向上为好，与CE对照的符号相反。

H2检查逐列表Δh>Δb>0是否发生，不把这一关系的代数必然性当新发现。主效果不由次要尺度或目标梯度救回。没有总体p值或独立确认区间；开发集已暴露。Source一阶预测用原生梯度点乘**实际**位移；dev局部斜率来自±0.1的中心差分，不称dev解析梯度。

## 6. 证据链

| 判断 | 原始与变换来源 | 实测/资格 | 边界 |
| --- | --- | --- | --- |
| 删除代价、放大收益 | cell逐条CE→rule/panel均值→每case三批均值；[主case表](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/primary_case_effects.csv) | 6均负/6均正；ELIGIBLE | 3个独立种子，非普遍定理 |
| 来源与dev后果不同 | source20原生读数与实际位移梯度；[source表](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/source_analytic_first_order.csv)、[dev表](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/metric_changes.csv) | full来源下降更多，out_norm dev下降更多；ELIGIBLE | 不据此宣布总体泛化能力 |
| margin/选择CE/accuracy差异 | 同一cell多读数、[逐列表坐标](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/paired_coordinates.csv)、[翻转记录](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/accuracy_transitions.json) | 读数各自保留；ELIGIBLE | 平均margin不决定平均softplus或argmax |
| 小成分一阶解释有限 | ±0.1同曲线斜率与1/4尺度；[component曲线](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/dev_component_curve_checks.csv) | 余项显式保留；ELIGIBLE诊断 | dev曲线外推不是独立预测验证 |
| 与E01第一步衔接 | [first_step_bridge](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/analysis/first_step_bridge.json) | 12条件最大差1.1444e−5，accuracy差0；BOUNDED | 只连接实际第一步 |
| 后续收益时序 | [轨迹回看](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/offline/trajectory_recap/analysis_cn.md)及该目录manifest | 仅原保存1/16/50/100点；BOUNDED | 事后描述，不解耦后续轨迹 |

## 7. 主要结果

### 7.1 六案例与两面板

下表各行先平均同case的3来源批；CE单位nat/答案。合并为两面板等权。表中old accuracy最后一列为out_norm−full，正数表示限制后的旧准确率较高。[完整主要case表](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/primary_case_effects.csv)

| Case | Panel | Gdelete | Gamp | Gtotal | Old accuracy out_norm−full (pp) |
| --- | --- | --- | --- | --- | --- |
| s29_FIRST_to_LAST | combined | -0.000061336 | +0.000453617 | +0.000392281 | +0.500000 |
| s29_FIRST_to_LAST | order_new | -0.000085204 | +0.000428621 | +0.000343416 | +0.166667 |
| s29_FIRST_to_LAST | combination_new | -0.000037468 | +0.000478613 | +0.000441145 | +0.833333 |
| s29_LAST_to_FIRST | combined | -0.000165639 | +0.000878025 | +0.000712387 | -0.083333 |
| s29_LAST_to_FIRST | order_new | -0.000209191 | +0.000847834 | +0.000638643 | -0.166667 |
| s29_LAST_to_FIRST | combination_new | -0.000122086 | +0.000908217 | +0.000786131 | -0.000000 |
| s43_FIRST_to_LAST | combined | -0.000227828 | +0.000423685 | +0.000195857 | -0.333333 |
| s43_FIRST_to_LAST | order_new | -0.000293447 | +0.000401767 | +0.000108320 | -0.666667 |
| s43_FIRST_to_LAST | combination_new | -0.000162209 | +0.000445603 | +0.000283394 | -0.000000 |
| s43_LAST_to_FIRST | combined | -0.000832750 | +0.000632354 | -0.000200396 | +0.250000 |
| s43_LAST_to_FIRST | order_new | -0.000691293 | +0.000616224 | -0.000075069 | +0.500000 |
| s43_LAST_to_FIRST | combination_new | -0.000974207 | +0.000648484 | -0.000325723 | -0.000000 |
| s71_FIRST_to_LAST | combined | -0.000497517 | +0.000495217 | -0.000002300 | -0.000000 |
| s71_FIRST_to_LAST | order_new | -0.000600172 | +0.000502763 | -0.000097409 | -0.000000 |
| s71_FIRST_to_LAST | combination_new | -0.000394863 | +0.000487672 | +0.000092809 | -0.000000 |
| s71_LAST_to_FIRST | combined | -0.000336760 | +0.000652233 | +0.000315473 | +0.250000 |
| s71_LAST_to_FIRST | order_new | -0.000382297 | +0.000626834 | +0.000244538 | -0.000000 |
| s71_LAST_to_FIRST | combination_new | -0.000291223 | +0.000677632 | +0.000386408 | +0.500000 |

六个合并删除值全部负，放大全部正；总收益4正2负。s71首→末的总值−2.300e−6来自约−4.975e−4与+4.952e−4抵消，保留其数值而不宣称稳定优劣。18个批次中删除有2正16负，放大18正，总12正6负；批次不作为独立种子。

### 7.2 两顺序、两面板及合并

[完整顺序表](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/primary_order_effects.csv)

| Order | Panel | New Gdelete | New Gamp | New Gtotal | Old CE full−out_norm |
| --- | --- | --- | --- | --- | --- |
| FIRST_to_LAST | order_new | -0.000326274 | +0.000444383 | +0.000118109 | +0.000104309 |
| FIRST_to_LAST | combination_new | -0.000198180 | +0.000470629 | +0.000272449 | +0.000348591 |
| FIRST_to_LAST | combined | -0.000262227 | +0.000457506 | +0.000195279 | +0.000226450 |
| LAST_to_FIRST | order_new | -0.000427594 | +0.000696964 | +0.000269370 | +0.000216421 |
| LAST_to_FIRST | combination_new | -0.000462505 | +0.000744777 | +0.000282272 | +0.000051584 |
| LAST_to_FIRST | combined | -0.000445049 | +0.000720871 | +0.000275821 | +0.000134003 |

两种未见的顺序均值都显示删除代价和放大收益。面板结论不能升级为自然语料泛化结论。

### 7.3 七方向后果与旧选择代价

下面是18个固定来源更新的等权均值，相对各自未干预旧终点。CE负值为改善；margin正值为改善。两个目标方向没有匹配各自范数，故不得直接称同容量/同步长谁更优。[原始均值与条件](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/metric_changes.csv)

| Direction | Old ΔCE | New ΔCE | Old Δmargin | New Δmargin | Old Δaccuracy pp | New Δaccuracy pp |
| --- | --- | --- | --- | --- | --- | --- |
| full | -0.001137093 | -0.001678487 | +0.000903156 | +0.001761810 | -0.166667 | +0.013889 |
| in | -0.000234727 | -0.000370856 | +0.000131625 | +0.000189526 | -0.152778 | +0.000000 |
| out | -0.000914302 | -0.001324849 | +0.000771901 | +0.001571199 | -0.111111 | -0.027778 |
| out_norm | -0.001317320 | -0.001914037 | +0.001127607 | +0.002242881 | -0.069444 | -0.027778 |
| random_norm | -0.001137110 | -0.001678475 | +0.000903262 | +0.001761800 | -0.166667 | +0.013889 |
| access | -0.000893938 | -0.001051852 | +0.000895830 | +0.000980111 | +0.041667 | +0.000000 |
| selection | -0.000246437 | -0.000630086 | +0.000007795 | +0.000780986 | -0.055556 | +0.055556 |

out_norm比full旧准确率高0.097222个百分点，未重现E01长期额外旧准确率代价。旧mean margin在首→末/末→首分别额外增加0.000183894/0.000265008，但旧selection CE反而额外增加0.000027736/0.000146847。softplus(−m)对不同样本的margin变化赋予不同权重，均值margin改善不能替代平均选择CE改善；这不要求任何数值矛盾。

每方向7200个旧评估实例中，full丢失27、修复15，out丢失10、修复2，out_norm丢失11、修复6。out_norm的11次新错误argmax全部是相反规则词；full为22次相反规则词、5次中间词。它们是重复列表上的18次干预计数，不是独立误差率试验。原E01的2400实例和100步计数不混入本表。

### 7.4 配对响应与偏向

out_norm平均Δb=0.001685244、Δh=0.000557637；full为0.001332483、0.000429327。逐列表out_norm有6812/7200次Δb>0（94.61%），其中3117次Δh>Δb>0，从而旧margin下降；只有1037/7200次双侧margin提高（14.40%）。full双侧提高371/7200（5.15%）。大量单侧正负可以在均值上相互抵消，不能由平均Δb>|平均Δh|推到每列表共同改善。[坐标与四象限](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/paired_coordinate_summary.json)

### 7.5 来源解析一阶变化与dev有限曲线

来源CE的余项定义为实测ΔL减去gᵀΔW_actual；均值和比例中位数不同，分别列出。[来源表](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/source_analytic_first_order.csv)

| Direction | Measured ΔCE | g·actual ΔW | Remainder | 余项绝对值 / 效应绝对值的中位数 | Maximum |
| --- | --- | --- | --- | --- | --- |
| full | -0.013797487 | -0.013937400 | +0.000139912 | 0.995% | 1.413% |
| in | -0.007306296 | -0.007374657 | +0.000068361 | 0.925% | 1.363% |
| out | -0.006542337 | -0.006562743 | +0.000020406 | 0.302% | 0.465% |
| out_norm | -0.009466609 | -0.009509562 | +0.000042953 | 0.443% | 0.643% |
| access | -0.005165182 | -0.005207743 | +0.000042560 | 0.648% | 2.795% |
| selection | -0.008639408 | -0.008729664 | +0.000090255 | 0.966% | 1.597% |

普通来源下降更大，符合其一阶最快下降性质。dev表使用同一方向±0.1实测曲线构造中心斜率，再外推到主尺度1；下表不是dev解析Taylor核验。[小对照余项](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/dev_component_curve_checks.csv)

| Contrast | Measured | Central extrapolation | Remainder | 余项绝对值 / 效应绝对值的中位数 | Maximum |
| --- | --- | --- | --- | --- | --- |
| deletion | -0.000353638 | -0.000416187 | +0.000062549 | 16.950% | 415.038% |
| amplification | +0.000589189 | +0.000600395 | -0.000011206 | 1.728% | 5.344% |
| total | +0.000235550 | +0.000184208 | +0.000051343 | 16.661% | 80.863% |

小删除对照的最大误差比例415.038%说明某个接近零或较小的对照不能由一阶外推解释；不得拿大CE效果的好拟合覆盖该误差。主判定始终使用实际有限对照。

### 7.6 尺度与四角交互

[四角表](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/four_corner_interactions.csv)和[有限对照表](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/deletion_amplification_contrasts.csv)。两顺序、三种子、三来源等权。

| Scale | Gdelete | Gamp | Gtotal | Mean geometric interaction |
| --- | --- | --- | --- | --- |
| 0.25 | -0.000100299 | +0.000149402 | +0.000049102 | +0.000001398 |
| 1.0 | -0.000353638 | +0.000589189 | +0.000235550 | +0.000017218 |
| 4.0 | -0.000642529 | +0.002225570 | +0.001583041 | +0.000280840 |

0.25/4是预设次要检查，不选最好尺度。四角交互非零表示有限效果不能简单相加，但极小值也包含FP32各角实际位移不严格相加及读数精度影响，不能只凭非零就声称模型曲率。来源实际一阶值可辅助检查舍入；本轮未计算dev解析梯度来排除全部数值交互。

次要目标分量交互也由同一七方向读数计算：I_obj=ΔCE(full)−ΔCE(access)−ΔCE(selection)。主尺度、两顺序等权时，旧/新dev均值分别为+0.000003282/+0.000003451 nat。这些有限读数不等于两个目标梯度独立，也不替代主要几何四角交互；同样保留数值精度边界。[全部目标方向读数](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/metric_changes.csv)

## 8. 图形与阅读边界

主要判定使用上面的表及逐条产物，不依赖新图。组会的黑灰白端点图属于原E01事后解释；两侧最小一阶改善的max-min候选方向未在E02执行，不能当成本轮方法有效的证据。

## 9. 阶段资格与失败分解

| 检查 | 实测最大值/状态 | 阈值/意义 |
| --- | --- | --- |
| 原旧基线复现 | 0 | ≤2e−5 |
| source梯度重组相对误差 | 3.177037e−6 | <2e−4 |
| 逐条CE分解绝对误差 | 1.158142e−6 | <2e−5 |
| 实际位移相对舍入 | 0.002663046 | <0.01 |
| Q外泄漏 | 4.746678e−6 | <0.002 |
| 随机R外泄漏 | 3.506868e−6 | <0.002 |
| source20恢复/独立进程重放 | 全部精确一致 | 仅工程资格 |
| 冻结参数开始/结束哈希和version | PASS | 唯一可变矩阵合格 |
| 43冻结输入、630cell完整性、1296标量复算 | PASS；最大复算差1.11e−16 | 完整性与算术，不证明机制 |

未发现数据、实现或工程失败；H1的不支持属于实测科学分支。无符号敏感方向=有害新功能这一推理受限，敏感性估计本身未被否定。长期准确率代价仍需轨迹证据。

## 10. 本轮完整记录

2026-10-11检验删除/放大的局部作用。先沿用10项登记输入与原旧状态，冻结43文件。Smoke `pt-1gvachp3`在4H100 reserved完成140单元及4独立重放；再提交Full `pt-majgvu5m`，平台02:22:46Z启动、02:31:02Z完成并SUCCEEDED，四worker均exit0。无重试。主实验读取18批×20来源答案，630单元×800dev+20source；总539520前向答案包含重复基线/恢复，梯度答案计360、backward objective调用216，新增训练更新0。

结果为6合并案例删除负、放大正，4总正2总负；新dev帮助与来源拟合下降不同，局部旧accuracy并非长期额外退化方向。认识是旧敏感成分可以同时有利于新旧CE，重新分配更新长度需与删除分开。下一研究者决定仍Unknown，不自动启动方法构造或新轨迹。

## 11. 解释与已有轨迹的衔接

AI有界解释：在固定初始状态，限制策略的平均新CE优势来自放大补偿了删除代价，而非删除了已证实有害的新学习成分。方向选择与范数分配共同重要；随机同秩对照近似普通，但没有匹配删除能量，不能承担更强因果任务。

第一批同源对照与E01实际第一步的12条件共用读数最大差1.144409e−5、accuracy差异0；浮点运算顺序不同，不宣称逐字节完全复现原限制步骤。该对账支持第一步衔接。独立来源批次2/3仍从同一旧终点出发，不是E01实际第二/三训练步。

原保存检查点1/16/50/100步的新CE普通−限制差（两顺序等权）为+0.00028500/+0.00417299/+0.01164035/+0.02156073。第一已保存点5/6有利，第16步6/6有利；不能定位未保存步的首次出现，也不能将后续差归给固定初始d。该回看是事后描述，与E02注册平均三来源的主要估计分开。

## 12. 可声称与不可声称

可声称：指定状态、来源更新、尺度和读数下的有限删除/放大作用；有符号作用与无符号敏感性的区别；实测输出坐标与竞争答案后果。不可声称：发现基础/独特模块、专家必要性、旧参数功能已分开、普遍最优策略、自然NTP结论、全部100步机制或未执行候选方向有效。

## 13. 下一决定

研究者下一决定Unknown。AI建议：优先判断是否把目标收紧为解释旧错误修复在后续轨迹为何减少；如果继续，须固定该预测要求及能区分解释的对照，不能以更多CE优势替代答案。此记录不授权或启动额外运行。

## 14. 产物与资产

[artifact_manifest.json](artifact_manifest.json)拥有29项小型来源路径/哈希，包含两job回执、完成manifest、冻结、分析与独立审计、第一步核验及离线/轨迹回看。所有大payload保留执行侧。主要分析输出清单：[output_manifest](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/output_manifest.json)；每条变换输入和脚本hash：[input_manifest](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/input_manifest.json)。两者均完整，不以平台成功代替产物核验。

实际输出登记为`representation_a17_03_component_causality_full_20261011t020424z`及`representation_a17_03_component_causality_smoke_20261011t020424z`，新访问检查[2026-10-11输出strict](/data/250010109/Research_System/assets/checks/2026-10-11_a17_component_causality_outputs_0233.json)通过。没有新训练检查点。Full主分析`results.json` SHA256 `82c5770bf4193e568503ef2a4830e25002705845814464cfea225a57e5f7a532`。

## 15. 核心入口

- [执行证书](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/execution_certificate.md)、[平台终态](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/analysis/full_platform_terminal.json)、[工程审计](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/analysis/full_engineering_audit.json)。
- [运行源码](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/source/run.py)、[位移/目标构造](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/source/components.py)、[冻结config](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/config.json)、[汇总源码](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/analysis/summarize.py)。
- [逐条结果与主表](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/results.json)、[来源/脚本manifest](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/runs/causal_20261011T020424Z/analysis/full/input_manifest.json)、[第一步核验](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/analysis/first_step_bridge.json)。
- [原终点离线解释](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/offline/analysis_cn.md)、[保存轨迹回看](/data/250010109/MoE_Router/experiments/20261011_a17_component_causality/offline/trajectory_recap/analysis_cn.md)。

记录自检：与冻结范围一致，全部主要数值有源表及独立复算；资格、实测、推导和AI解释已分开。研究者科学裁决未由代理代填。
