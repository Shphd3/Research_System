派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/audits_cn.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/audits_cn.md)；研究修改仍回到原件。

---

# R05：三类分别记录的审计

状态：`COMPLETE_WITH_BOUNDED_EVIDENCE`；首份事实截点为2026-10-22 16:30 UTC。本文件分别记录科学识别、数据统计、实现数值，不替代Summary或另立设计。[本轮Anchor](../../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/anchor_cn.md)、[Protocol](protocol_cn.md)与[来源审计](source_audit.md)保持各自职责。

协议和操作选择由`/root`在研究者明确委托下进行AI自审。另一个AI处理者`/root/source_audit`独立于写实现的Agent，检查源码与持久回执，撰写本审计；它没有训练模型。三类记录代表不同审计范围和AI身份，不代表三个人类审稿者、独立实验重复或科学批准。研究者机制接受与问题关闭仍为`Unknown`。

执行根为`/data/250010109/MoE_Router/experiments/20261023_autonomous_retention`。初始`queue/plan.json`有90个唯一任务，依赖图无环。正式case矩阵是A21、B27、C3、D5、E10、F4；E包含两个零更新固定路由参考，case数不等于训练轨迹数。工程、读数与恢复任务另计。43/71顺序等待主要最小矩阵全部到终态后再运行；失败保留，不删除。

## 审计一：科学识别

审计者：`/root/source_audit`，相对于方案作者的独立AI源码/设计复核。结论：假设和阶段边界`PASS_WITH_BOUNDARIES`；这资格已授权比较的识别范围，不提供正机制结论。

| 阶段 | 研究模型与主要变化 | 对照及仍存竞争解释 | 允许的结论 |
|---|---|---|---|
| 0 | 精确已习得四矩阵attention、原生/缓存末层与普通训练。 | 父模型旧任务、A/U仅新与B/Full联合。普通习得失败阻止高级机制裁决。 | 已核验范围的实现正确性和任务可达性。 |
| A | 用固定初始top16矩阵原子过滤一次Adam候选实际位移。 | 普通、统一小步/调度、top恒定、random16、tail16。仍可能只是整体减速或保旧专用功能。 | 需新任务合格、不劣且旧收益超过所有主对照，才有选择效用；不识别common。 |
| B | 共同候选系数加全正交补共享/私有增量。 | 共享/分开×正常/保护、Full、row共享/私有正常/保护。完整私有残差增加总容量；匹配总自由度row改变单模式空间。 | 指定预算口径下的条件分配效用，不能排尽容量/优化后归为纯梯度混合。 |
| C | 用TRAIN拟合后的权重在400/800步重选未来保护方向。 | 固定、假重选重置、真重选；匹配选择计算。旧受保护方向可重新正常更新。 | 超过重置对照的动态候选效用，不是永久冻结共同子空间。 |
| D | 冻结共同gate/up，在原生SwiGLU down投影用单/双残差专家。 | 独立专家普通MoE、共同候选+单/双残差、正常/保护。容量、初始化和活跃计算显式披露。 | 受限FFN专家效用；attention不资格FFN机制。 |
| E | 预定D/multi_normal提供固定专家，router输入3072维完整激活或16维候选/随机摘要，再联合训练。 | 已知模式oracle、平衡随机；固定专家分离选择与专家适应。直通训练与推理计算不同。 | 实际选专家的效用/遗憾与摘要效用；模式分类或负载不足以支持。 |
| F | 现有自然文本next-token短续训及保留列表读数。 | dense正常/保护、ordinary2、shared2保护，披露路由。任务/模块改变与预训练曝光仍存。 | 短预算自然文本外推，不是普适保护，也不是旧频率方案的因果解释。 |

attention候选是参数空间选择器；正交不代表功能独立。同起点、幅度匹配的源到对方模式损失变化，只检验局部干扰，不能识别完整训练的唯一原因。终点候选/补空间恢复与放大是偏离训练轨迹的敏感性干预，不是唯一中介或共享语义证明。A/C阴性不删除独立D/E/F，也不允许看结果换有利方向。

沿用A15_11关于标签可读性、效用可读性、实际gate使用与功能收益的区分。A15_24使用不同Base表征、旁支专家、Tulu数据、top-2组合和优化；本轮结果不能因果解释其失败。SAE/CrossCoder可选，但必须匹配父检查点、hook、尺度与重构行为；缺失仅影响字典诊断。

## 审计二：数据与统计

审计者：`/root/source_audit`，基于冻结合同与当前身份/来源记录。结论：`PASS_EXPLORATORY_ONLY`；本轮没有未触碰的独立模型/任务确认总体。

Base/tokenizer精确本地revision为`da87bfb608c14b7cf20ba1ce41287e8de496c0cd`，由六文件HF下载metadata与`model_identity.json`重算hash绑定。这是本地版本身份，不是在线核验最新版。父模型为E03 AdamW1200适配器，SHA为`48595673c24579164e271cfeb1b86be6a234e2dfc06218b74d8ca07e16411b75`，依赖精确Base。`input_access.json`提供当前访问证据，不自动证明完整内容、加载或科学资格。

old/reversed各TRAIN2400、DEV800；每个DEV面板400答案，每个口令cell200答案。unseen-order有意与TRAIN共享无序组，但有序列表不同；unseen-combination无序组不同。前者共享组是任务定义，不改称污染。记录、目标、模式与分组身份必须配对。不混consistent/reversed。仅读TRAIN和已暴露DEV；TEST不读且历史已暴露，不能作为新确认备用。

| 阶段 | 固定终点计划曝光 | 选择/评价边界 |
|---|---|---|
| A | 1200×20=24000新答案，旧重放0。 | 初始权重选择器；按相同新曝光比较旧新DEV。 |
| B | 共24000，其中old/reversed各12000。 | 同一联合batch；私有模式收到一半答案，不暗中翻倍曝光。 |
| C | 24000新答案，旧重放0。 | 仅用TRAIN演化权重，在预定400/800步重选。 |
| D | 共24000，old/reversed各12000。 | 比较前独立识别原生FFN候选。 |
| E | learned固定600、联合600各12000答案，每阶段每模式6000；oracle/random固定参考0更新，联合同样12000。 | 统一预定D/multi_normal端点，不事后选赢家；分阶段报告。 |
| F | 每臂400×20=8000自然预测目标。 | 同一冻结文档/窗口顺序；列表读数是保留能力，不是自然任务习得。 |

29/43/71只改变续训顺序，共享一个旧习得模型；D/E/F及C使用登记的29最小运行。配对记录是观测单位；不确定性按无序列表组同步重采样，保留两个口令和置换。`aggregate.py`内的2000次bootstrap只用于A冻结终点；独立自然文档和旧固定权重对话诊断使用各自保存的配对bootstrap，描述给定模型/顺序的样本不确定性，不代表跨模型总体显著性。主条件合取与所有对比均报告，不挑seed、检查点或有利替代指标。

自然数据`natural/documents.json`已实际保存：训练128、验证64文档，每文档128token、127预测位置。两划分文本与token窗口hash不交叉。它绑定`dclm_raw_holdout_global02`、压缩源SHA `4c5ce60258943051758148653c448bb57724af7592cc9d3e9c053cc6f9e10323`、当前访问回执与tokenizer hash。固定顺序/抽取前共有16256训练、8128验证位置。Base预训练是否见过、语义近重复仍为`Unknown`。新的轮内划分不等于外部未触碰确认总体。

## 审计三：实现与数值资格

实现作者`/root`、`/root/retention_runner`提供自检；`/root/source_audit`独立读源码、比较语义及已保存回执。首份16:30截点为`PARTIAL_PASS`，后续实际资格补充在文末：下列范围已具工程证据，后续模块/阶段仍待实际检查。脚本存在或job成功不等于科学结果。

实际attention代码加载四个Q/K/V/O，共6291456参数；使用FP32原生前向、关闭TF32、精确父模型/适配器身份、答案SUM20/20、fresh零衰减AdamW、裁剪和完整恢复状态。拒绝旧O-only恢复。A先执行一次AdamW，再过滤实际候选位移，只推进一次动量。B在共同系数与投影dense残差坐标上优化，明确不同于A；冗余坐标移动与有效矩阵移动分别报告。

原row-mask与补空间投影不能交换。实现改为每半行用受限原子Gram逆投影；各半行减16维，再加共同16维，两种row策略总有效自由度均为矩阵元素数−16。它小于全补空间族。CPU检查覆盖Gram秩、候选/补空间正交、重构无操作、有效自由度、实际Adam位移及真实外部CPU进程。GPU仍需自己的no-op/冻结/恢复回执。

B每个完整联合优化窗口均出现两个模式。一个tensor存放私有slice，因此没有证明任意缺席模式的idle动量隔离；代码显式断言双模式前提。B也冻结原四矩阵，后续仅guard修订新增显式底座权重/版本检查。保存源码版本与每任务freeze，区分加强后的guard和更早Smoke；不改变运算，也不追溯升级旧检查范围。

| 已检查实际证据 | 数值与范围 | 边界 |
|---|---|---|
| `cache/cache_receipt.json` | TRAIN4800、DEV1600；原生/缓存logits最大绝对误差0，全部argmax相同。 | 同shape重放；worker另验实际训练microbatch。 |
| `runs/smoke/0/seed_29/U/completion.json` | 3更新、60答案，冻结与保存完成。 | 仅工程。 |
| `runs/smoke/resume_verification_0_U_29.json` | 外部进程1→2步，权重、优化器、RNG、计数、batch顺序、投影、确定性读数逐项相等。 | 初始普通族，不代表所有后续模块。 |
| `runs/smoke_A/.../installation_noop.json`与恢复回执 | 无操作误差0、argmax相同；A/TS实际位移过滤的外部下一步重放PASS。 | 3步Smoke，不说明长程效用。 |
| `runs/smoke_B/.../installation_noop.json`与恢复回执 | B/SP零增量误差0；外部下一步重放PASS。 | 对应共享保护族和当时冻结源码。 |
| `runs/mlp_cache_preparation.json` | TRAIN/DEV误差分别3.147125244140625e−5、2.86102294921875e−5，4800/1600样本argmax全部相同。 | FFN接口缓存检查，不说明专家/router效用。 |
| A/U实际1200步评价与completion | 新准确率100%，每个新cell≥95%。 | 新规则可达性，不表示保旧。 |
| B/Full实际1200步评价与completion | 旧99.625%、新99.75%，八cell均≥95%。 | 有旧标签且新曝光减半的联合可达性。 |

后续CPU边界回执`audit/retention_boundary_cpu_20261022.json`显式检查倍率1三步重放，权重和优化器状态与原生Adam逐字节一致。倍率0时，候选坐标最大漂移6.160905741126044e−8，加法roundoff最大9.896757546812296e−8，动量仍逐步一致；整套数值测试通过。训练`retention.py`未改。这资格浮点干预边界，不是实证保留收益；正式方法倍率至少0.01。

专家模块实际执行down投影。先用oracle资格结构，再解释learned路由。直通训练可能为代理梯度执行两个专家，推理只执行选中的专家；必须披露这一区别，不把所有训练计算称为稀疏top-1。自然缓存、专家训练、固定/联合router、自然续训的保存/重放/telemetry，需要最终补齐或明确缺失。此截点不声称D/E/F已有学习结论。

`source/aggregate.py`仅读R05输出，不反序列化权重；分开实现存在、终点完成、学习资格与显式AI假设判断。它从冻结queue读正式矩阵，排除Smoke/重放、区分E阶段，分开自然NLL与列表95%资格。已用人工数值记录检查bootstrap算术和缺失配对保护。检查点存在/manifest不等于独立tensor载荷审计。

## 带日期的R2资格修订：2026-10-22 16:41:48 UTC

[完整FFN修订Protocol](protocol_ffn_repair_v2_cn.md)在初始D五臂失败后、R2结果前登记。这是唯一科学配置修订，不新增owner，不改写历史批准。D/E/F全部用`ffn_repair_v2.json`在`runs/repair_full_ffn`共同重跑，身份为`R05_FFN_qualification_repair_V2`；R1保留，A/B/C不变。

科学识别：R2在原非线性位置训练完整gate/up/down，每专家9437184矩阵元素，同时改变非线性适应与容量。即使成功，也不能确定哪张新增投影必要或证明共同分量。E完整输入变为x1024，三个learned router统一64单元SiLU隐藏层；summary/random16容量匹配，完整输入不匹配。R1/E与R2/E是分轮实验，不能当纯router输入消融。

数据统计：相同记录顺序、已习得父模型、29种子与自然文档/文本/窗口身份；每个受影响方法与对照共同按1200/600/400步重跑，学习率和95%列表门槛不变。自然NLL无95%分类线。各自绑定源码/config与端点lineage，不跨R1/R2合并，不挑最好终点。

实现数值：R2必须有自己的no-op、梯度、计数、冻结、外部下一步恢复及辅助loss遥测。在本补充时这些仍`PENDING`，不继承R1 Smoke资格。仍只用既有四个单H100 worker。工程修复保留失败；R2仍不合格时不允许第二次科学配置修订。整体完成必须覆盖R2全部必需case，不由queue调度优先级取代。

## 当前F匹配复放资格补充

四个旧T_F/T_H×11/22固定权重复放已实际执行，并通过原H10080/batch128门槛。`runs/F_frequency/replay/*/receipt.json`记录全10340 DEV、1701 B1及Base位置均与原GPU NLL逐值匹配，mean error/MAE/最大误差均0，替换子集1015位置。旧CPU/local-MIG不匹配保留为历史事实，不再阻塞当前四个匹配干预；未放宽阈值，未改旧检查点或源码。

这是推理干预，不是拟合；优化器更新、LM训练目标数、恢复为`NOT_APPLICABLE`。六个半权重分支、五类对比检验同一已训状态下的即时输出/组合边际；数值及2000次对话bootstrap现已保存到`analysis/frequency_replay_summary.json`：全B1的TF/TH交互为+.004957/+.005331nat，区间不跨0，加入/替换c的区间均跨0。不唯一解释原跨模型学习结果，不识别common语义或更新干扰；Tulu特征面板不与本轮列表准确率、DCLM文档损失合并。

## 后续R2工程与自然统计回执

R2列表缓存原生/完整FFN重放实测通过：TRAIN4800最大误差4.57763671875e−5，DEV1600为4.100799560546875e−5。自然缓存TRAIN16256最大误差1.18255615234375e−4，DEV8128为5.9604644775390625e−5；全部argmax相同，容差仍为2e−4。因此“小于5e−5”只适用于列表缓存，不适用于所有自然token检查。R2三步multi_normal的外部进程1→2步，bank、router、优化器、RNG、摘要frame、计数及batch顺序逐项相等。来源为该run的`mlp_cache_preparation.json`、`natural_cache_preparation.json`、`smoke/D/seed_29/multi_normal/external_resume_verification.json`。这只资格已测工程范围，不把学习失败升级为通过。

`analysis/natural_comparisons.json`独立核验64文档×127位置=8128目标及文档/总体CE一致；按文档配对2000次，seed20261023，只覆盖固定端点的文档不确定性。R1 dense保护减普通dense为−.000786862[−.001044237,−.000556584]nat/目标；shared2保护减ordinary2为−.000670356[−.009293992,.008466520]。原生attention端点将TS直接对比每个控制，不把全部方法相对父模型的共同NLL下降当选择特异性。自然文档、续训顺序和旧Tulu对话单位不合并。

## 完成与更新规则

每个正式case始终保留完成、部分、失败、阻塞或未运行身份。最终补实际受测版本、cell数、保存恢复、曝光与失败，不改冻结科学判据。事实先于独立AI初步解释；V3取消等待审核，不把AI解释变成人类接受。本审计不授权commit、push、发布、新付费资源或问题关闭。

## 后续事实核验：2026-10-22 17:14 UTC

按165项完整冻结范围`queue/plan_full_before_scheduler_v2.json`核验，R2 D5/E10/F4端点均已完整保存，三类阶段各自独立身份。D ordinary、多残差正常/保护、单残差正常/保护最弱cell分别51%、54%、58%、46.5%、45%，均未通过95%资格；这使D/E架构与选择效用保持证据不足。抽查实际completion：D1200步/24000答案、E joint600步/12000答案、F400步/8000自然目标，均标工程PASS，冻结hash为`2d5b81f0b4dae14add3b58245daecfbf9fa82865682314e38575ee10ffc6c434`。这是回执/计数审计，未在CPU重新反序列化全部检查点。

A功能恢复与局部更新均已实际完成。C重选后的几何重叠在Q/V/O明显下降（1200步约.635/.421/.460，K约.844）；其保旧阴性不能解释为方向完全没有变化。恢复R翻回旧规则，但C/R实际扰动范数相差约1185倍；等范数随机R不翻回旧规则，只支持条件方向敏感性。局部候选幅度匹配需约63–72倍放大；有限更新不是整程遗忘的唯一原因。

调度迁移期间旧queue/plan的146项只是排空子集，不能缩小总体165项范围。调度临时文件rename失败属于工程事件；其根因竞争writer尚未唯一确认，不声称已证明共享文件系统锁失效。父controller退出时已有single_protected子任务真实保存完成，经核对后恢复DONE，不重复训练。两个更早single零步读数失败及重试保留，仍只有一次科学配置修订。A/B重复尚未全部完成，整体状态仍RUNNING。

## 后续环境与泛化定位：2026-10-22 17:24 UTC

`analysis/final_code_environment_audit.json`对R1/R2各19个D/E/F端点记录已测范围：gate top1及单位缩放、bank冻结buffer、摘要frame、TRAIN归一化均通过；每轮17个训练端点的遥测PASS，两个零更新reference不适用，三个fixed learned端点的专家逐字节未变。R2十九份独立环境检查通过，可追溯4个修前与15个修后runner源hash；R1没有逐case环境源hash，明确保留BOUNDED_MISSING_EVIDENCE，不追溯补造。两轮全部自然端点读数已保存。

R2完整词表TRAIN读数确认ordinary/multi_normal新准确率96.708%/96.208%，四个TRAIN命令cell均≥95%。DEV的主要缺口集中于乙口令×新排序（各200）：51%/54%，CE2.285740/2.444560；其他三个新DEV cell约90.5%–94.5%。TRAIN记录仅panel=train，按DEV新颖性匹配的TRAIN面板仍Unknown。`analysis/ffn_generalization_panels.json`只定位固定端点的泛化缺口，没有拟合、重训练或唯一因果归因。

## 最终执行范围：2026-10-22 17:27 UTC

`analysis/final_scope_check.json`为PASS，独立核对165项全部DONE、89个正式端点、85次训练+4个零更新参考、86000更新、1720000预测目标，以及每正式case的最终检查点、逐样本eval与TB文件存在。`analysis/queue_v2_compatibility_audit.json`核对146个历史terminal结果+19个新v2结果，无active claim、未知结果、owner/exit或config-freeze不匹配。它是执行库存和调度兼容性核对，不是科学资格。

资源回执`analysis/resource_audit.json`记录十个本轮单卡Reserved作业均终态，九SUCCEEDED、旧worker0控制器FAILED但其子任务真实完成并已核对；四个替换controller均SUCCEEDED。最大并发为4，start→complete区间合计约3.551667 GPU小时是时间代理而非计费值。本轮GPU作业已全部停止。R1/R2结果、两次单专家零步读数失败/工程重试与调度修复均保留，仍只有一次科学配置修订。

## 最终保存与登记审计：2026-10-22 17:37 UTC

最终回执为执行侧`audit/registration_receipt_20261022T173707087537Z.json`，状态REGISTERED_ACCESS_PASS，failures为空。105个checkpoint family覆盖686个实际state，包含89个正式case及工程Smoke/外部重放family，不能把105当正式科学case数。共请求210项family/选定实际checkpoint资产，新增54项；并非686个独立资产ID。每family audit记录fresh完整文件SHA256、size与独立CPU保存状态审计。资产payload仍在执行侧。

严格访问快照为`Research_System/assets/checks/20261022T173707087537Z_a17_r05_actual_outputs.json`。该strict检查的范围是stat、可读性、目录遍历和已登记probe，不含反序列化、完整hash、GPU或科学资格；fresh hash/CPU审计来自上述family审计，不混称由strict检查完成。源码/优化器/RNG/数据cursor的保存与代表族恢复证据仍按各自范围解释；R1十九case环境缺证没有追溯补造。

## 源码版本证据的专门限制

`environment.source_sha`是记录时对磁盘文件计算的hash，不证明实际已载入bytecode。R2 F/dense_protected的task freeze在16:53:25记录修前c49，单专家自然读数guard于16:53:37修复，environment在16:53:48记录修后40eb。这个case的实际import版本保持Unknown，不能用4个旧/15个新环境磁盘hash声称载入版本均已证明。两份源码的差异仅为`evaluate_natural`单专家oracle两行guard；该F条件route=`none`不进入该分支，故本case训练运算及功能路径等价的范围可由源diff限定。这不是完整源码载入逐字节一致证明，也不改变科学配置或已保存数值。

## 最终登记证据版本补充：2026-10-22 17:44 UTC

最新覆盖回执为`audit/registration_receipt_20261022T174400242571Z.json`，对应strict快照`Research_System/assets/checks/20261022T174400242571Z_a17_r05_actual_outputs.json`，REGISTERED_ACCESS_PASS且failures为空。仍为105 family、686实际state、210项覆盖资产；18个迁移后A/B family补上位于queue_v2的task freeze后登记新的证据版本。它复用17:37已完成的686份完整payload hash/CPU审计，没有重新训练、重写旧endpoint或把新增证据版本计作新科学case。

`analysis/R2_source_version_reconciliation.json`保存五个修前task freeze与环境磁盘hash的分时记录、精确两行diff，以及去除evaluate_natural后的全顶层AST相同检查。`/root/source_audit`也独立比较了保留旧文件与当前文件，确认差异范围；这不恢复未捕获的import bytecode身份。

## 最终公平性冻结回执：2026-10-22 17:47 UTC

最终`audit/final_fairness_receipt_20261022T174706217246Z.json`的SHA256为`196be64c152ecaa81f1fc952c5a5acd74d927df064999e8411133feefbb22f4d`。它记录89个正式case工程完成，70个case审计PASS，19个R1 case因环境/精度版本回执缺失保持BOUNDED_MISSING_EVIDENCE；无observed_failed_checks或issues。A的15个主配对曝光、B的27份容量匹配、C三臂、E二十份专家血缘、F八份分母及父模型+七个顺序29 A自然读数均完成对应检查。PASS针对这些工程/曝光/血缘检查，不改变学习资格失败或AI科学判断。

直接同case外部下一步重放在89个正式case中6个PASS、83个NOT_RUN（含零更新参考），不能把保存了优化器/RNG/cursor或代表族Smoke重放，扩大成所有case恢复通过。五个工程Smoke与三份外部重放family有各自回执。最终审计复用17:37 fresh完整hash/CPU结果，检查当前manifest签名与size；最新17:44仅补来源元数据，无payload重开。19份R1环境缺证与R2 dense_protected确切import版本Unknown继续保留。
