派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/protocol_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E02_rule_acquisition_diagnosis/protocol_cn.md)；研究修改仍回到原件。

---

# Protocol：A17_04_E02 规则学习诊断

## 0. 审批快照

- 文档状态：`APPROVED_FOR_BOUNDED_DIAGNOSIS_SMOKE_AND_FULL`。依据研究者2026-10-11明确委托，在以下有限范围内诊断、Smoke与训练，不需要再次批准。
- 授权范围：诊断、输入呈现对照、增加可训练范围。精确有限设置属于AI受托具体化，不是研究者已经接受的科学机制结论。
- 分块审计：A–G已按委托诊断范围检查，跨块一致性`PASS`。科学解释和问题闭合仍为`Unknown`。
- 登记版本：`a17_04_e02_acquisition_diagnosis_v1`；书写时`NOT_RUN`。首次GPU执行前，快照双语Anchor/Protocol，并在执行freeze manifest记录源码、配置、数据、预检、所需输入身份及实际冻结时间。
- 目的：区分旧训练输入没有拟合好与未见数据没有泛化，并找出优化、可训练计算或输入呈现哪条路线能修复学习。
- 主Anchor：[A17_04_01](../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/subanchors/17_04_01_rule_acquisition_diagnosis_anchor_cn.md)，继承当前[Focus](../../../../focus/focus_conditional_mapping_transfer_cn.md)。
- 检验前提：只训练末层投影可能改善候选词概率，却没有学会按口令选择。竞争解释包括优化或曝光不足、呈现困难和未见数据泛化问题。
- 实验角色：`root-cause audit`，只研究旧模式学习；没有新规则迁移、专家或SAE分支。
- 主读数：开发集两个口令、两种未见类型的全词表准确率最小值；每一格达到80%才合格。
- 条件：原投影SGD、投影AdamW、最后四层attention AdamW、显式指令投影AdamW，以及通过CPU编码标准后运行的统一分隔符投影AdamW。
- 匹配项：同一Base起点、列表ID、标签、一个训练顺序种子、答案损失、每更新20个有效目标和最终目标预算。不匹配输入token数、时间或FLOPs。
- 完成标准：全部符合预检的有限实验臂及旧终点诊断、工程Smoke和恢复合格、实际保存状态及读数登记、双语有界结果。科学学习成功不是完成条件。
- 不可声称：普遍容量限制、纯参数数量效应、纯分词机制、跨任务干扰、专家收益、统计重复确认或问题闭合。

## 1. 术语与定义

**旧模式记录**含可见模式一、口令甲或乙、三个不同词的列表和一个答案token。甲选首项，乙选末项。**列表对**指同一列表分别用两个口令提问；所有训练有效批次包含完整列表对。**答案目标**指答案前文后唯一一个非忽略下一token；前文和padding不计入训练目标预算。

`neutral`保留原中性口令和空格列表。`explicit`只把口令文字替换为`取第一项`或`取最后一项`，保留列表、模式和目标。`normalized`保留中性口令，只把列表词间空格改成固定顿号`、`。这是呈现干预，不是重新标注。统一视图必须用完整前文的token offsets核验每个候选词边界。

`order_new`表示熟悉无序三元组的未见排列；`combination_new`表示整个无序三元组未见。**固定训练面板**取自训练列表，但评估时不回传梯度。**微型拟合**在固定小集合训练，检验拟合可行性，不检验规则泛化。完整诊断从Base重启，不继承微型训练。

## 2. 与Anchor对齐

父实验旧开发集逐口令、逐类型准确率33%–54%，因此不能解释已经掌握旧规则后的保持问题。本子实验只测试怎样取得合格旧规则起点。证据见[E01 Summary](../A17_04_E01_consistent_reversed_mapping/summary_cn.md)；其中TEST结果是此前已暴露证据，不能用来选择本轮诊断设置。

| 项目 | Anchor条款或竞争解释 | 为什么需要、证据角色 | 支持／不支持／不足 | 产物 |
|---|---|---|---|---|
| 旧终点训练面板与DEV | 拟合还是泛化 | 在同一保存状态给原失败分类 | 训练高DEV低指向泛化；两者低保留拟合未知；加载失败不足 | `prior_endpoint_diagnostic.json` |
| A与B | 优化方式还是投影不可行 | 同数据、同范围，改变优化器 | B合格A失败说明优化路线可行；两者失败仍未知；无效运行不合格 | 配对终点表 |
| B与C | 可训练范围 | 同优化器、同数据，开放更多attention | C合格B失败说明范围路线可行；两者失败未修复；不可归因纯数量 | 张量清单、终点表 |
| B与D | 中性或显式指令 | 同标签、范围、优化器，改变呈现 | D合格B失败说明呈现路线可行；其余结果保留 | 视图清单、终点表 |
| B与E | 原列表或统一编码 | 同标签、范围、优化器，固定分隔符 | E合格B失败说明格式路线可行；编码未通过则NOT_RUN | offset预检、终点表 |
| 微型拟合与完整重启 | 拟合还是泛化 | 小集合记忆见证；完整训练独立开始 | 小集合成功不证明泛化；失败不证明不可能 | 微型状态及读数 |

## 3. 检验假设

AI候选H：预先规定的优化、范围或呈现调整中，至少一个能在有限预算内取得合格旧规则起点。候选机制是：当可训练计算或输入提示受限时，提高候选词概率比按照条件选择更容易。不要求任何臂成功。如果原SGD在更多曝光后就成功，则解释实际修复不需要更强的机制改动。

## 4. 竞争解释

1. 原来的两遍训练曝光不足，或SGD动态不合适。各臂完整训练统一24,000目标，并在原4,800目标位置保存读数。
2. 末层投影能拟合见过的输入，却不能泛化到新排列或新三元组。分开训练面板和两种DEV，报告逐口令指标和配对两问都答对率。
3. 中性符号需要学习映射，而预训练语言已提供显式指令含义。D检验这种呈现路线，不能单独排除长度和任务新颖程度。
4. 空格列表中候选词的编码不同于单token答案。E同时改变编码与分隔符，不能只归因于分词。
5. 更多参数改变了实际更新规模或信息处理，不只是原始容量。保留精确张量数、clipping、实际更新范数和计算限制；B/C不识别纯参数数量。
6. 工程或标签错误可能伪装成未学会。CPU标签/token/offset检查、直接损失核验、冻结权重检查、no-op和跨进程精确恢复保护证据资格；工程合格不说明规则已学会。

## 5. 数据构造与来源

所需输入资产为`model_qwen3_0p6b_base_official_a5`、`tokenizer_qwen3_0p6b_base_official_a5`、源`data_a17_conditional_mapping_v1`、派生`data_a17_mapping_acquisition_diagnostic_v1`。使用载荷前查询资产登记并运行当前strict检查。精确Base目录为`/data/250010109/model_cache/Qwen3-0.6B-Base-official`。

只取原模式一`old`的TRAIN和DEV。TRAIN为1,200列表×两口令=2,400记录；DEV两种类型各200列表×两口令=400记录，合计800。保留原列表、划分、类型、标签和词表。派生视图保留记录ID或明确原记录链接、list ID、口令别名、模式、词、目标ID、源划分、panel、呈现类型、前文和input IDs。记录ID加视图前缀；command仍为甲/乙，world仍为old，mode仍为1。派生版本共十二个文件：`data/acquisition_v1/{train,dev,train_panel,tiny}_{neutral,explicit,normalized}.jsonl`。正式生成、训练和诊断分析不复制、加载或评估原TEST。

GPU前确定训练评估面板：取原TRAIN的无序`orbit_id`按字典序前十组；每组选择其有序tuple代表最小的完整20列表词旋转周期。共200列表、400完整口令目标，精确保持词和位置均衡。微型拟合取第一周期20列表，加第二周期按字典序前12列表，共32列表、64目标，不要求词均衡。在manifest冻结所有ID及选择规则，各视图、各臂和旧终点评估使用相同ID；不根据模型loss或准确率挑样本。按声明的循环或shuffle顺序组完整20目标批次；小集合跨epoch边界不丢目标，也不产生未完成累积窗口。

CPU检查首末标签、列表口令唯一性、每列表两口令、源与派生标签一致、源划分归属、允许的未见排列组复用和未见组合组分离。显式与统一视图保留列表、标签及逐批目标直方图。答案是单词表token；完整前文加答案的编码必须等于前文ID加该目标。原视图和显式视图的输入候选词不要求单token，须记录这一事实。

E要求顿号`、`使每个候选词在完整前文中恰好对应预期目标token ID和字符span，不合并或多出候选token。合同冻结前，CPU检查3,200旧TRAIN/DEV记录的9,600候选出现，以及40个循环词表前文的120候选出现，均为零失败。冻结实际预检JSON，并在正式生成文件上重跑检查。这是分词证据，不是学习结果。若重新生成不满足标准，E为NOT_RUN；不根据GPU结果再寻找新分隔符。

## 6. 学习任务与允许监督

只预测完整前文后的下一个答案token，只该目标计CE。正确词出现在列表中。没有额外解释、隐藏教师、模式二样本、答案重放、蒸馏标签或外部语义监督。显式指令文字是允许的输入干预，不是额外答案。准确率由全词表argmax决定，不得替换为只在候选词中argmax。

## 7. 模型、架构与冻结变体

使用登记的28层Qwen3-0.6B Base和原生forward。全部臂从相同预训练参数开始。已有三个旧adapter只用于此前状态评估，不作为新臂起点。

| 臂 | 呈现 | 可训练范围 | 参数量 | 优化器 |
|---|---|---|---:|---|
| `o_sgd`（A） | neutral | `model.layers.27.self_attn.o_proj.weight` | 2,097,152 | SGD |
| `o_adam`（B） | neutral | 同一末层`o_proj` | 2,097,152 | AdamW |
| `attn4_adam`（C） | neutral | 第24–27层attention的q/k/v/o投影权重 | 25,165,824 | AdamW |
| `explicit_o_adam`（D） | explicit | 同一末层`o_proj` | 2,097,152 | AdamW |
| `neutral_normalized_o_adam`（E） | normalized | 同一末层`o_proj` | 2,097,152 | AdamW |

C精确训练16个权重张量：`model.layers.{24,25,26,27}.self_attn.{q_proj,k_proj,v_proj,o_proj}.weight`。不可变父safetensors header计数25,165,824，是原矩阵十二倍。保存`provenance/parameter_header_audit.json`；训练前独立枚举运行时named parameters，核对名称、形状和总数。不训练attention bias、q/k norm、MLP、embedding、final norm或输出head。单投影形状1,024×2,048，其余所有参数冻结不变。

采用FP32模型和梯度、native SDPA、eval mode无dropout、禁用TF32和确定性算法。训练q/k/v确实可以改变attention读取，所以C同时改变计算位置和参数量。没有LoRA、SAE、router或专家。

## 8. 训练目标与优化

每更新最小化20个有效答案的平均损失：\(L=20^{-1}\sum_{i=1}^{20}-\log p(y_i\mid x_i)\)。四次微批、每次五例；每个微批loss之和除20后回传。前文和padding不进入分母。没有辅助损失、正则项或启用component，component registry为空／NOT_APPLICABLE。

A采用manual plain SGD，学习率0.01，无momentum或decay。B/C/D/E用AdamW，学习率0.0001、betas(0.9,0.999)、epsilon1e-8、weight decay0。各臂在optimizer step前，将聚合可训练梯度的全局L2范数clip到1。学习率恒定，无warmup、scheduler decay、自适应停止或早停。报告raw/clipped gradient norm和实际参数增量范数；同学习率或clip上限不等于实际更新匹配。

微型拟合每臂从Base和全新optimizer开始，在固定64目标集合完成160更新=3,200有效目标。完整训练再次重启Base、optimizer和RNG，完成1,200更新=24,000目标，即2,400完整TRAIN记录十遍。若五臂都符合预检，总完整训练120,000目标，微型训练16,000目标。Smoke、恢复重放和评估额外分别统计。E缺失则明确减少实际总量。

## 9. 条件、种子与检查点

各臂采用训练顺序seed29。这是一个诊断实现，不是三种子确认。冻结完整列表对顺序；A/B/C输入和目标批次完全相同，D/E底层列表与标签顺序相同。每有效批次都含完整口令对。GPU worker代表独立实验臂，不是数据并行副本：worker0先A后E，worker1/2/3并行B/C/D。E串行放置不改变初始化或预算。

完整保存及评估里程碑为0、1、240、600、1200更新，即0、20、4,800、12,000、24,000目标。微型保存0、1、160，并至少在0、160评估其64目标及固定训练/DEV面板。微型集合与训练面板有重叠，不算独立泛化证据。Smoke每个符合预检的臂运行3步，保存用于独立进程下一步重放的状态。

每个可恢复状态保存所有可训练张量、optimizer moments/step或manual SGD描述、恒定schedule、Python/NumPy/CPU/CUDA RNG、完成更新、有效目标数、stage、arm、父资产/hash、配置/源码/数据hash、顺序数据cursor及下一批身份。状态必须配合精确冻结Base，不是独立完整LM导出。保存真实张量/optimizer/state manifest，缺失保存明确记录。

旧终点评估加载登记家族`adapter_a17_04_mapping_full_20261011t095038z_seed_{29,43,71}_old`中实际保存的240更新成员，以及所需Base。这三个诊断读数描述已有状态，不是本轮额外新训练种子。

## 10. 主指标与冻结分析计划

对臂\(j\)、口令\(c\)、类型\(p\)，准确率是全词表argmax等于真实目标的比例。主读数为1200更新处的\(Q_j=\min_{c,p}\operatorname{Acc}_{j,c,p}\)。每个口令/类型单元200目标；先分别报告，再给等权合并均值。合格要求每格至少0.80。门槛继承AI操作性学习资格，不是科学置信水平。

观察单位为列表/口令记录；两问配对指标以列表为单位。新训练只有一个种子，列表数不产生独立训练重复。报告精确单元计数、均值和逐臂配对差异，不给p值、总体区间或三种子表述。不删除困难列表、异常值、失败臂或低分口令。缺任何必要单元即未合格；工程无效臂不是科学负结果。

主比较固定终点。同时报告全部冻结里程碑和首次满足四个DEV单元的已保存里程碑，这个描述性学习时间不改变最终预算。A/B比较优化器，B/C比较可训练范围，B/D比较显式呈现，B/E比较统一呈现。均为描述性诊断，没有多重检验校正的确认性主张。

当前输入访问合格后再读旧状态训练和DEV诊断。新设置先于GPU结果冻结。DEV公开用于诊断，不称未暴露确认集。此前CPU源结构QA检查过父TEST的schema和分词；初步审计还反序列化过同时包含DEV/TEST预测记录的旧eval JSON，但所有模型读数计算都筛选`split == 'dev'`。未使用TEST模型结果选设置，也未把它汇报为本轮新诊断证据。保留这项暴露事实，不能声称从未读取TEST预测记录。本次正式generator/trainer/analysis不得加载原TEST行。不自动把某设置提升为新迁移run。分析在`<run>/analysis/`保存终点表、逐单元轨迹、两问选择表、loss拆分表和证据资格manifest。科学主张限于这些有限设置和这个种子。

## 11. 次指标与资格检查

记录答案CE、全词表准确率、正确答案减相反端点log概率的margin、正确答案减最强全词表错误竞争者的margin和竞争者ID。对列表集合\(S\)，保存总概率\(P_S=\sum_{w\in S}p(w\mid x)\)、候选访问损失\(-\log P_S\)和条件选择损失\(-\log[p(y\mid x)/P_S]\)。两者严格相加等于答案CE；这个输出记账不识别内部模块。

每个配对列表记录两个口令是否都答对。定义\(s_c=\log p(L_3\mid x_c)-\log p(L_1\mid x_c)\)，口令响应\(a=(s_{乙}-s_{甲})/2\)。正响应符合旧映射方向，但正均值本身不构成合格或机制证据。保留逐口令概率、中间词竞争和错误，因为平均端点margin可以掩盖全词表预测错误。

逐更新记录答案加权CE、raw/clipped gradient norm、实际step norm、相对权重增量、有效目标和实际prefix token、批次ID、吞吐与累计stage坐标。保留七个必需TensorBoard标签：`tokens/train_lm_loss`、`updates/train_lm_loss`、`tokens/train_total_loss`、`updates/learning_rate`、`progress/tokens_seen`、`progress/optimizer_step`、`progress/effective_tokens_per_update`。token loss的global step为完成窗口的有效答案数；update loss以optimizer step为坐标。独立臂不做四worker聚合。恢复保存两个坐标，避免重复冲突事件。

数值和工程检查：loss/gradient/weight有限，无跳过更新，独立目标计数，no-op评估相同，冻结参数version和byte hash不变，CE拆分误差小于2e-5 nat，跨进程下一步权重、optimizer、RNG、计数和批次身份精确相同。失败停止受影响臂并保留证据。执行前后源码/配置/数据/冻结合同hash必须一致。

## 12. 已知正确、错误与易混淆例子

- 正确标签：`红 蓝 绿`配旧甲应为红，乙应为绿；显式文字不改变标签。完整配对标签按要求选择两个端点。
- 错误构造：同一视图完整输入矛盾标签、缺一个口令、答案位置错误、原TEST行泄漏到新生成，或E候选编码不符合预检承诺。拟合前拒绝。
- 易混淆结果：正确CE下降，但两问都答对率仍低或条件选择变差，不能称规则掌握。微型拟合可能只是记忆；E成功可能是分隔符或呈现帮助；C成功可能是读取或优化变化，不只是参数数量。

## 13. 科学步骤与阶段合同

| 阶段 | 目标／输入 | 如何做及为什么 | 输出／产物 | 通过、失败及交接 |
|---|---|---|---|---|
| CPU预检 | 核验登记Base、源旧TRAIN/DEV及派生视图 | strict资产；标签、划分、配对ID、token边界与运行时张量清单 | 数据/视图/参数manifest、访问检查 | 无效数据`DATA_INELIGIBLE`；E编码失败`NOT_RUN`；合格视图进入freeze |
| 冻结 | 防止结果驱动设计变更 | 快照双语合同、源码/配置/数据/输入身份及授权 | `freeze.json`、执行证书 | 关键hash缺失`FREEZE_INCOMPLETE`，不放大GPU执行 |
| 旧状态读数 | 区分已有拟合与未见表现 | 三个旧240状态上评固定训练/DEV，无梯度 | `prior_endpoint_diagnostic.json` | 有效读数参与诊断；缺状态记录missing，不编造 |
| Smoke／恢复 | 核验真实五臂trainer | 每合格臂3步；检查遥测/freeze；新进程恢复并精确重放下一更新 | Smoke状态、tags、恢复比较、gate | 工程PASS即可进入已授权Full；低科学准确率不是Smoke失败 |
| 微型拟合 | 检验小集合拟合 | 独立Base起点、64固定目标、每臂160步 | 保存状态与读数 | 有限结果不论成功与否；完整训练重启，不继承 |
| 完整训练 | 比较学习路线 | 独立Base、相同列表标签顺序、每臂1200更新 | 必需状态、固定训练/DEV读数 | 完成有界训练；失败或部分结果保留，不自动延长 |
| 分析／登记 | 得到可审计有界答案 | 重算指标、查计数/hash、登记实际状态和读数、strict输出访问 | 分析表、登记回执、Summary/Detailed | 完成事实交付；科学裁决及下一run选择属于研究者 |

## 14. 算法、输出与来源合同

执行根目录：`/data/250010109/MoE_Router/experiments/20261011_a17_mapping_acquisition_diagnostic`；实现`source/diagnose.py`。源码、配置、派生数据、预检、合同快照、环境、回执、日志、TensorBoard、检查点和分析保留执行侧。规范科学记录保留本实验目录；原始权重和批量预测不进入Git。

使用系统execution envelope、根`templates/execution/acp_submit_template.sh`、资源`h100-4-reserved`、镜像`shphd-lite-0911`。单节点四H100，每任务最长7200秒。保留dry-run解析、实际profile/spec/image URL、直接job ID和提交命令。只有本实现有界Smoke合格才运行已授权Full。触及时间上限记录部分完成，不静默续时或新增臂。

复用并适配已读A17_04 E01 AnswerLM/collate、原生加载、列表配对、评估、SGD、来源、freeze和遥测；扩展张量选择和AdamW可恢复optimizer状态。保留源码来源及差异。拒绝继承敏感方向投影、SAE hooks、模式二任务、TEST加载和旧科学分支逻辑。执行前读实际源码及training reuse/observability要求；加入多张量更新不能削弱父工程检查。

逐阶段输出含原始update metrics、精确批次ID、带源list/command/panel/view ID的读数、checkpoint成员hash、冻结权重检查、环境和源码/配置/输入manifest。只登记实际Smoke、微型和完整保存，使用稳定family ID、真实成员清单、Base依赖、已达答案/更新和恢复边界。运行当前selected strict输出检查，在artifact manifest/Detailed链接回执。单纯job成功不能证明保存产物合格。

## 15. 成功、失败与证据不足

**学习合格**：固定终点四个DEV口令/类型单元均达到80%，工程合格且输出齐全。它说明一个种子中存在可行旧学习路线。保留训练/DEV及两问成功指标；不构成跨任务机制支持。

**不支持修复**：有效实验臂在冻结预算未合格。与相应匹配臂比较，不宣称普遍无容量。若只有训练拟合好，标为泛化限制。若全部有效臂失败，报告`NO_QUALIFIED_ACQUISITION_ROUTE_IN_BOUNDED_DIAGNOSTIC`，不是模型不可能。

**证据不足或不合格**：缺必要单元/检查点、标签/数据/freeze无效、非有限更新、恢复失败或超时部分执行，限制相应比较。E编码未过为NOT_RUN。次指标不能挽救缺失的主学习资格。这些分支都不授权任意追加训练或迁移主张。

## 16. 不能声称什么

不声称任务不相容、已经掌握规则的遗忘、专家收益、SAE机制、自然文本结论、普遍0.6B容量限制、纯参数数量作用或独立分词原因。B/C改变计算范围；B/D/E改变呈现；A/B改变optimizer及其数值动态。同答案数不等于同FLOPs或时间。一个种子和已暴露DEV提供有界诊断，不是独立确认。将来确认性迁移需要新留出集和独立明确合同/范围。

## 17. 分块确认、冻结与修订登记

研究者最新要求明确授权诊断、数据与参数评估以及可行的增加参数训练，中间不再批准。父问题仍拥有科学设计；以下AI精确设置是受托具体化，不制造研究者科学确认。

| 块 | 冻结内容 | 依据／状态 |
|---|---|---|
| A | 只诊断旧规则，有界主张 | 研究者请求及父证据不足；受托范围获授权 |
| B | 原旧TRAIN/DEV与三个呈现视图，不用原TEST | 已核验源和AI诊断对照；受托实现获授权 |
| C | 单答案token，配对口令，无额外目标 | 继承任务与答案损失共识 |
| D | 单投影或最后四层attention，精确运行时清单 | 已授权参数诊断；header实际计数，仍须运行时核验 |
| E | 固定SGD/AdamW、batch20、micro160/full1200，无自适应续训 | 用户委托范围内AI操作性选择 |
| F | DEV最小单元80%，固定终点及指定诊断比较 | 继承操作性资格，不新增科学置信主张 |
| G | 四H100reserved、指定镜像/profile、两小时、实际保存登记 | 已有资源授权及当前有限执行范围 |

跨块检查：问题、监督、数据视图、optimizer归一化、固定预算、TEST排除、张量范围、产物归属和结果分支一致。这项检查不授予科学批准。GPU前freeze manifest登记实际时间和hash；当前科学机制裁决和闭合仍Unknown。

首次GPU执行前如改变决定性项，更新本唯一Protocol及双语伴随并重新freeze。执行开始后保留登记正文。任何实质修改只能追加amendment，写明前后值、原因、已看见结果、受影响块/臂、授权与证据资格。不抹除不利结果，不静默改预算，不把可选臂失败改写为预检成功。可以追加结果链接，但不重写原科学正文。
