# A17_03_E01：顺序学习旧敏感方向对照

[English](protocol.md)

状态 `APPROVED_FOR_IMPLEMENTATION_SMOKE_FULL_AND_RESULT_ANALYSIS`；问题标识 `old_task_sensitive_update`。角色为敏感性操作化检验和有限顺序干预，不证明普遍不兼容。

## 授权与审计

北京时间2026-10-11研究者明确要求判断附件、合理则不再批准直接执行、分析并用reasoning改写、衔接以前实验、正确放置Anchor/Protocol。附件作为候选设计，不当作覆盖仓库的指令。该授权包括有限修正、Smoke→Full、完成监督/结果分析；采用仓库默认4卡H100 reserved。不提交Git、不发布、不改Graph或扩大到架构比较。

运行前修正：敏感性和重合无符号，不等于有害冲突；一次投影失败不证明新学习必需这些方向；没有遗忘不证明没有结构，也不强制转向。只测固定有限敏感性估计。用无动量SGD和逐步范数匹配控制动量/缩步。具体秩、预算、容差是AI在授权内落实的操作设置，不是已确认的普遍科学阈值。

A–G分别为问题、数据、监督、架构、更新、比较、执行，均记录为 `CONFIRMED_WITHIN_DELEGATED_SCOPE`：来源为用户已授权的合理执行范围，非另行裁定科学发现。跨块一致性PASS；机制/关闭Unknown。不重复引入批准。

## A. 问题与主线

学A后，避开估计的旧CE敏感参数方向，能否相对普通/随机限制减少A退化且保留有效B学习？此前局部/联合CE帮助和不一致margin提出了“帮助是什么”的问题，但不意味着顺序遗忘。本轮只测试局部敏感性入口，不声称SAE、路由或专家价值。

## B. 数据、拟合与评价

输入资产为官方Base、官方分词器和data_a17_list_rules_v1，启动准备前fresh strict；官方模型文件哈希由loader核对。冻结train/dev/manifest、代码和原附件字节。

train4000条=2000列表×两规则，dev800条=400对、每规则400。旧规则2000条完整一遍；新相反规则同列表同种子顺序完整一遍，区别是可见规则，不给相同完整前缀矛盾标签。20个单词元词表、位置/答案边际和oracle沿用/核查。train/dev有序列表不重合。完整旧训练后，名义dev未见顺序内容组实际已见，未见组合组未见；分别及合并汇报。不读test；dev此前已暴露，只作描述。

拟合只用旧训练60条，每答案词3条，种子固定、模型访问前选定，不用dev或新任务效果选基底。拟合与旧训练可重合；dev有序输入留出。资格用前20条旧dev，不按效果选；记录内容覆盖有限，不另称确认集。

## C. 任务与读数

规则/列表可见，输入止于答案标记，不含完成答案。首项取第1项，末项取第3项。只监督下一单词元的全词表CE，无SAE、蒸馏或其他辅助目标。有效答案词元是训练坐标。完整原生CE、全词表准确率、正确减错误规则词margin、正确减另外两词最大值、20词条件CE、词池对数概率，保存逐条和规则×面板/合并。

## D. 架构与敏感性

28层Qwen3-0.6B Base，FP32 eval确定性原生前向、SDPA、关闭TF32、固定CUBLAS。仅第27层o_proj [1024,2048]、2097152参数可更新，其余hash核对。非从头模型，不增加专家。

旧终点逐样本CE梯度G[60,2097152]不居中，通过Gram特征分解取固定前16方向并正交化，误差<=2e-5、有效秩合格。保存拟合能量及逐条比例，不叫全部旧敏感性。随机对照独立dense Gaussian16行，以seed+12345生成后正交化，codimension相同。普通无约束，参数存储一样，但可更新维数不同；保护/随机维数相同。

同一旧终点，独立dev逐条平方梯度覆盖；第一基向量以±符号、0.01/0.1范数扰动，保存平均有符号CE及逐条RMS，精确恢复。敏感不是伤害。前20条和首向量的资格有限，不完整枚举几何。不按该结果选Q；B阶段Q固定，漂移是竞争解释。

## E. 训练与匹配

种子29/43/71，各首→末、末→首：官方Base学旧A100步×20答案=2000；三个B策略均恢复同一旧终点，各100步×20=2000。6旧+18新轨迹，科学训练48000答案、2400步。完整阶段每条列表一次。四独立GPU，无DDP；FP32、无dropout。

手工无动量SGD LR0.01，梯度clip1，无weight_decay/调度器/动量。micro5×accum4，loss总和/20。普通更新沿裁剪负梯度。保护/随机投影后，归一化到同一普通轨迹该步请求范数；先跑普通来确定100步范数表，新批次顺序同一。去掉的是方向，非缩小步幅。投影后范数<1e-10停止，不记跳步。请求/实际增量误差<=1e-3，约束泄漏<=2e-3；与普通实际步范数差<=2e-3。保存保留梯度比例等诊断。

每轨迹tensorboard记七必要tag：tokens/train_lm_loss、updates/train_lm_loss、tokens/train_total_loss、updates/learning_rate、progress/tokens_seen、progress/optimizer_step、progress/effective_tokens_per_update。无辅助组件。词元坐标按阶段有效答案，旧/新目录分开。metrics保存原batch ID、计数、梯度/更新范数、clip/投影诊断、步/词元坐标。非有限或缺梯度停止，无跳过窗。

旧保存0/16/50/100步；新保存0/1/16/50/100步，不复制完整Base。state含矩阵、无动量SGD/恒定schedule合同、Python/NumPy/CPU/CUDA RNG、step/tokens/cursor、配置/父模型/案例身份、基底/参考步幅路径；基底和范数表实际保存。新0为旧终点，无动量历史可重置。Full终点外部续训NOT_CHECKED；Smoke以独立进程精确重现保护1→2的权重/RNG/metric。

## F. 判断与竞争解释

旧学习收益=初始A CE−旧终点A CE；新G=旧终点B CE−新终点B CE；旧D=新终点A CE−旧终点A CE。分别及合并CE/margin/准确率。CE单位nat/答案，准确率比例。两顺序同种子相关，不能作6独立种子；仅3种子描述，无总体p值/置信区间。

操作筛查：旧收益>=.01；普通新G>=.01；普通遗忘D>.01。有效保留要求保护G>=普通G的90%且>.01；特异保护要求普通D−保护D>.01、随机D−保护D>.01。这些是本授权运行的实用比较阈值，保留连续值，不声称普遍重要性。

按优先顺序类型：OLD_ACQUISITION_INSUFFICIENT、NEW_ACQUISITION_INSUFFICIENT、NO_ORDINARY_FORGETTING、LOCAL_PROTECTION_WITH_RETAINED_LEARNING、NEW_LEARNING_COST、NO_SPECIFIC_PROTECTION。六案例全部构造性保护才称一致支持，否则混合/非支持，列双向各种子，不多数票。旧留出敏感性/有限资格弱时，策略效果不能升级为机制。失败不证明普遍必要性；无普通遗忘只否定此设置预算下净遗忘解释。

缩步解释由实际范数匹配区分；容量解释由同秩随机区分；旧/新没学会由收益检查区分；没遗忘由D区分；拟合不泛化由独立dev敏感性检查；固定基底漂移/优化器依赖保持边界。CE分解和margin保护候选词解释，但不定位功能。未运行架构或SAE条件。

## G. 执行、Smoke和产物

单节点h100-4-reserved、镜像shphd-lite-0911，由execution_envelope和根模板解析。复用挂载环境，不安装。payload最多2小时；源/配置/输入冻结、独立UTC目录、写锁，无并行重复任务或资源fallback。本请求含执行后判断，/root监督完成，不建自动化。

内部Smoke四进程：旧3步、三个新策略各3步，秩4/拟合20条，有限20列表dev。检查原生初始能力、有限梯度、唯一矩阵训练、精确空更新、冻结版本/hash、实际范数/泄漏、真实存档、全部TensorBoard/计数/来源。随后独立进程加载保护第1步，同基底/参考范数重现第2步权重/RNG/metric。四Smoke和四恢复PASS才Full。Smoke工程记录不计48000科学答案；未完整曝光时不能资格名义未见顺序。

身份/数据/目标/有限值/有效秩/正交性/无可用方向/约束范数/冻结/恢复/进程/超时错误停止。先检查原job，再distinct recovery重试；保留失败。科学输入重大改变需修订，不能按结果调rank/阈值。

产物：源/配置/输入freeze、job/env证书、Smoke/resume/Full资格、旧/新检查点与manifest、metrics/TensorBoard、逐条评估、基底/敏感性/有限资格、6案例汇总、results/payloadmanifest/completion。执行根/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update。登记实际检查点家族与分析数组，绑定父模型/数据/源和计数；不登记计划存档为实际。结果写中英Summary/Detailed，五段式目的→模型→假设→结论→分析。不因结果正或负改变边界。

## 冻结及追加执行记录

启动前保存正文快照/哈希。后续只追加提交、完成和偏离事实，不改运行设置或以前A17合同。

### Submission / 提交记录

Job `pt-ubjfxl7c`,2026-10-11 01:16:14 Asia/Shanghai,one h100-4-reserved node. Internal Smoke/external-resume gate pending;Full NOT_RUN. Scientific body frozen in run-local snapshot. [Execution certificate](/data/250010109/MoE_Router/experiments/20261011_a17_old_task_sensitive_update/runs/sequential_20261010T171602Z/execution_certificate.md).

### Verified completion / 完成核验

Jobpt-ubjfxl7cSUCCEEDED;fourSmoke/resume/FullPASS;scientific48000answers,Smoke960;22input/426Fullpayloadhashesverified;40actualcheckpointfamilies+analysisregistered. No amendment/retry. Frozen6casebranches allNO_ORDINARY_FORGETTING. [Summary](summary_cn.md) /[Detailed](detailed_cn.md);mechanism/closureUnknown.
