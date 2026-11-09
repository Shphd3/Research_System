# Protocol：A17_02_E01 固定池频率实验

[English](protocol.md)

## 0. Approval Snapshot

状态：`APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL`。北京时间 2026-10-10，研究者明确采纳现有共识，暂不再审计后续内容，要求独立频率 Anchor/Protocol；直接 `o_proj` 为主、LoRA 留作前阶段容量对照；Smoke 后四卡 H100 reserved Full，再执行频率/SAE，并监督到完成。本文件落实已采纳候选，禁止根据 dev 选择条件。A–G 和跨块一致；执行授权来自当前用户直接指令，旧草案/Smoke 不产生授权。科学解释和关闭仍 Unknown。

目的：固定 B 机会时，增加 A 对 B 的作用是否随同/异规则改变。性质：可操作定义/代理检验。竞争解释：通用练习或首末项初始难度。主指标：B200 时种子级规则×呈现交互。统计支持分支不代替研究者关闭。边界：一个 Base、新固定池、单矩阵和两类未见。[Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_02_fixed_pool_frequency/17_02_fixed_pool_frequency_anchor_cn.md) 与[Focus](../../../../focus/focus_fixed_pool_frequency_shared_learning_cn.md)拥有问题含义。

## 1. Terminology / Definitions

FIRST/LAST 从三个不同词取首/末项。A 是额外池，B 是接受影响的池。A/B 元数据不进提示。改变同/异关系时，同一 A 列表的可见规则改变，不给完全相同前缀矛盾标签。一次呈现就是一个有答案监督的训练记录，重复也再计一次。损失为全词表 CE，nat/答案。顺序未见：B 见过内容组的新排列；组合未见：两个训练池均未见的无序内容组。损失增加意味着预测变差。

## 2. Anchor Alignment

独立频率 Anchor 拥有固定 B 的呈现交互。同预算分配、B-only 净额外训练是另外两个次指标。不插 SAE、router、专家，不把 LoRA 混进频率主估计。来源有效学习不能丢弃合格策略结果，只能门控另行声称的有效更新机制。主读数固定原生 FP32；同一个保存矩阵另用 BF16 作次报告。

## 3. Tested Hypothesis

双侧假设：条件种子分布上的交互中位数超过 +0.01 或低于 −0.01 nat/答案。竞争解释为位于实际阈值带内。正交互仍可伴随所有条件都帮助 B；可靠负交互按同一个双侧规则支持相反方向。不得由 dev 选择方向补救。

## 4. Rival Explanations

精确位置/答案边际控制答案先验；未见列表控制完整列表记忆。配对同/异条件共用 A/B 列表和随机呈现顺序，仅 A 可见规则改变。两种 B 方向显露初始位置难度。每条轨迹重置原始 Base。恒定 LR 避免不同总训练量带来不同 warmup 机会。B-only 答净影响；1000 答案对照答分配，不能称同时固定 B 机会的纯频率。单矩阵容量不足可能造成完整模型没有的冲突。

## 5. Data Construction And Provenance

输入 ID：父模型/Tokenizer `model_qwen3_0p6b_base`；新数据 `data_a17_fixed_pool_frequency_v2`。本地和 pod 均重新 strict 检查。数据种子1010。A、B 各200不同有序列表，每个渲染两种规则，故各400元数据行。20个单词元中文答案仅继承词表选择，不继承前一任务数据。每池5个不同内容轨道×2个排列×20个循环词位平移；每池/规则各位置和答案，每词精确10次。各100个无序内容组，A/B 互斥。

B 的其余4排列分别给 order-new dev/test，各2个排列。另两组各5轨道给 combination-new dev/test。Dev/Test 各800规则行：每规则×未见面板200条。所有池/划分有序列表互斥；组合未见相对两个实际训练池定义，且 dev/test 新组互斥。顺序未见相对实际 B 训练，不能相对未用的全集。构造资格检查不调用模型；manifest 固定生成器/tokenizer/文件哈希、oracle 与续写边界。数据不是旧暴露 dev 的修改。

呈现500次为完整200列表重复两遍，加固定种子选出的5个完整20平移块（100条），因此边际精确保持。800次为完整4遍。记录列表、池、答案、规则实际呈现；不同样本数量与呈现次数分开。

## 6. Learning Task And Permitted Supervision

前缀：`规则：取第一项/最后一项。列表：w1 w2 w3。答案：`。不追加完成答案，正确词可合法出现在列表。每记录只监督紧接前缀的一个答案词元，其他位置忽略。全词表 CE，无三候选限制头、辅助损失、隐藏池/专家/频率标签。一个固定模板。

## 7. Model / Architecture And Frozen Variants

原始28层 Qwen3-0.6B Base，hidden1024。仅训练 `model.layers.27.self_attn.o_proj.weight`，1024×2048、2,097,152参数，无 bias/adapter/router/SAE 插入。嵌入/共享输出头、norm、MLP、其他 Attention 冻结。权重和优化状态 FP32，训练 BF16 autocast；主评估原生 FP32，关闭 TF32、确定性算法、固定 batch20。每轨迹从原矩阵开始，不接续其他臂。4个独立单 GPU，无条件间 DDP 归约。LoRA 不属本主估计。

## 8. Training Objective And Optimization

AdamW LR1e-4 从首步恒定，无 warmup/decay；betas(.9,.95)、eps1e-8、weight_decay0、clip1。micro5×accum4=20有效答案/update，数据并行1。答案损失总和/20。非有限立即停，不把跳步暗计。完成累积窗才增加20答案。恒定 LR 与 E02 不同，必须本轮新 Smoke 核验。唯一目标为答案 LM CE，总损失相同，不设正则组件。

每轨迹 `tensorboard/<phase>/` 写：`tokens/train_lm_loss`、`updates/train_lm_loss`、`tokens/train_total_loss`、`updates/learning_rate`、`progress/tokens_seen`、`progress/optimizer_step`、`progress/effective_tokens_per_update`。Token 坐标为有效答案；update 调试坐标遵循共享观测合同。每批原始记录含输入ID、池/规则计数、LR、梯度范数。

## 9. Conditions, Seeds, And Checkpoints

B=FIRST/LAST 各七条件：

|条件|A关系|A呈现|B呈现|步数|
|---|---|---:|---:|---:|
|same_200|相同|200|200|20|
|diff_200|不同|200|200|20|
|same_800|相同|800|200|50|
|diff_800|不同|800|200|50|
|b_only|无|0|200|10|
|same_budget|相同|500|500|50|
|diff_budget|不同|500|500|50|

探索种子29/43/71，共42轨迹、30,000答案、1,500步。确认新种子101/113/127/139/151/163，共84轨迹、60,000答案、3,000步。总90,000答案/4,500步不包括 Smoke、评估与恢复回放。条件与确认种子在探索前固定；不得用 dev 选。配对同/异条件具有同一列表呈现順序，仅 A 规则不同。

保存 update0、2、ceil(总步数/2)、final（去重）：矩阵、optimizer、Python/NumPy/CPU/CUDA RNG、答案计数、呈现游标/顺序hash、config/parent/data ID。答案坐标0、40、20×中间步和最终200/400/1000。只保存矩阵，加载需要已登记 Base。Full 终点外部恢复未测须写 NOT_CHECKED；工程 Smoke 单独核验同更新器/游标的外进程恢复。

## 10. Primary Metric And Frozen Analysis Plan

B 损失只取 B 当前规则。每种子/方向/面板，`I=(Ldiff800−Lsame800)−(Ldiff200−Lsame200)`，终点均 B200。种子主值等权平均两方向×两面板。全部分项、逐条 CE/正确率、均值/中位数/范围保留；唯一确认目标是合并主值。四个接受者面板大小相同，等权平均等于记录加权。初始/最终正确率不能代替损失。

探索 n3 仅描述，不给95%种子 CI 或显著结论。独立训练种子才是重复，内容组/平移不能增加 n。确认 α.05、δ=.01，保守双侧符号规则：6/6 I>δ 为登记正分支；6/6 I<−δ 为负分支，双侧p=.03125。报告[minI,maxI]：独立同生成机制种子效应假设下，种子中位数至少96.875%覆盖，非均值 CI。区间完全在[−δ,δ]内为有界实际无效；其余未过/未解决属 INSUFFICIENT，非零效应证明。分项不能补救主值。机制解释/关闭仍 human Unknown。

主读数 FP32。固定矩阵另用 BF16 读，不像旧探针重算另一种虚拟更新。分歧完整保留。Smoke 固定状态 FP32/BF16 no-op 都必须精确重复；失败读数不合格。确认只用模型未打开的新 test，探索仅 dev；test 不选 LR/checkpoint，也不用来选择重试。

## 11. Secondary Metrics And Guards

净额外训练：同/异 A200/800 对 B-only，均 B200，但总计算不同。分配：同关系800A/200B 对500A/500B，总1000答案但 B 机会不同。分别、合并报告面板、方向、种子；记录 CE、正确率、目标概率、实际 ΔW 范数。饱和或不利轨迹保留，不挑checkpoint。终点策略不能直接证明跨任务单更新因果。来源有效不门控主估计。

强制工程：目标/配额正确、遥测有限、独立答案计数、冻结版本不变及每worker开始/结束冻结权重全字节哈希、真实保存哈希、确定性 no-op。Smoke 独立进程恢复update2，下一update3 对连续参考。LoRA、SAE、新模板/词表、rank扫描、局部探针均不得作为自动救援条件。

## 12. Known Good / Known Bad / Known Confusing Cases

好：恢复原矩阵；精确配额和完整块500余项；正交互同时净帮助。坏：答案追加在marker后；池标签进入提示；test选 LR；冻结头漂移；游标损坏；未完整累积计20。易混：两个方向交互抵消；正确率全对却 CE 不同；异规则帮助较少仍优于 B-only。分开解释。

## 13. Scientific Procedure And Stage Contracts

1. Preflight：重新strict、oracle/分词/划分/边际，覆盖所有任务的CPU调度测试，源/config/Protocol哈希。失败不训练。
2. Smoke：B首/末×同/异800，种子29，共4独立任务，各至多8步/160答案。初进程到2并保存下一步参考、恢复；另进程从2恢复，核验3，继续到8。恢复校准额外80答案另记，不重复计科学轨迹。只评dev。冻结、遥测、计数、no-op、恢复和四输出全部通过。
3. Full 探索：Smoke PASS 后42轨迹、只评dev；不选超参/窗口。
4. Full 确认：全部探索工程检查通过后84新种子和未打开模型test。门控完整性，不能门控探索好坏。合格不利/无效轨迹保留，科学分支与成功独立。
5. 完成真实保存、分析、清单、终端/平台证据及双语 Summary/Detailed，按资产生命周期登记输出。所有失败保留，不暗重跑已打开的确认。

## 14. Algorithm, Output, And Provenance Contract

`execution_surface=acp`；`resource_profile=h100-4-reserved`；`image_id=shphd-lite-0911`；`env_layer=source/runtime.sh`。envelope 拥有展开tuple/image，使用唯一模板、先dry-run。单节点4独立GPU、完整任务分waves，无资源fallback。Root 协调本轮总live reserved节点，不假设可占第二个四卡节点。

执行根 `/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency`。提交前冻结 code/config/Protocol/data 与命令；每次独立不可覆盖run、持久pod日志、证书、提交回执。复用E02答案wrapper、末投影/CPU-tree/精确比较/遥测/保存接口与当前runtime；改写确定配额调度和多轨迹阶段。不继承旧虚拟探针、warmup、暴露dev、LoRA、SAE/router目标。数据改用循环均衡构造但新建池/划分。

上限：频率Smoke≤1800秒；Full探索≤7200、确认≤14400、合计≤21600秒payload，加有界kill grace。非有限、漂移、计数/配额、身份、恢复/no-op/遥测错误或超时停止，不能当科学负结果。用户要求监督到完成：随进度逐步拉长轮询，读现有job与持久进度，不重提。必有终态保存family、原始分析、清单与terminal receipt。无commit/push/发布/无关job停止授权。

## 15. Success / Failure / Insufficient Evidence

工程PASS：全部数据、运行、遥测、冻结、保存、恢复检查和必需轨迹齐全。明确合同违约为FAIL；缺产物为未完成。确认统计仅§10，实际无效仅限注册区间与载体，未显著不等于无效。正交互不等于净伤害；B-only次比较另定方向。机制解释、效用与关闭 Unknown。

## 16. What This Cannot Claim

不能同时固定计算/B机会的纯频率、按答案量精确匹配FLOPs、自然预训练机制、从零习得、完整功能分解、无限制模型冲突、专家必要性或长期架构收益。独立种子仍条件于一个父模型/池族。SAE须独立精确接口与合同，不能改写频率冻结结果。

## 17. Block Confirmation, Freeze, And Amendment Ledger

A–C：研究者采纳已有首末项、独立频率问题、精确答案监督和两面板。D：明确直接矩阵、LoRA前阶段容量对照。E–G：当前明确委托采纳已写完整候选，授权实现/Smoke/PASS后reserved Full与监督。δ/符号规则、种子、恒定LR和上限为采纳候选的冻结落实，不称物理定律。旧A17_01_E03保留历史草案；本文件为当前唯一频率Protocol，新A17_02 Anchor拥有设计。不授权根据dev调参或救援确认。

提交前在run记实际哈希和复用谱系，正文执行侧归档。必要修复只追加带资格影响的amendment，保留源/失败，不放松护栏。此freeze尚无结果。研究者明日可调整后续范围，不能暗改已完成证据。

## 提交前数据资格修复01

初版v1独立种子构造通过内部检查，但有限列表空间使test中40个规则行与旧E01已评估dev重合。本轮尚未提交或模型评估。v1保留历史生成资产；实际输入改为新v2，只用E01所有split未使用的27个循环内容轨道中的20个。新四池/划分与旧train/dev/test全部内容组互斥；筛选仅用旧列表身份，不用模型结果或答案损失。大小/边际/条件/种子/估计不变。原prepared未提交freeze保留，提交前重新冻结实际源。

## 追加执行账本：频率Smoke

核验前job pt-ujjb8f7a平台SUCCEEDED/终态后，提交pt-cgmiw5f3，四卡H100reserved。实际v2源/config/Protocol/data冻结与证书：/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/smoke_4h100_v2_20261009T172146Z。统计计划不变；Full仍须实际Smoke门控。

## 追加执行账本：频率Full

pt-cgmiw5f3实际56/56工程PASS、平台SUCCEEDED后提交pt-ho4byzg4，四卡H100reserved。使用Smoke前预冻结Full源/条件/新确认种子，不以dev选择；实际证书和回执：/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z。终点科学判断仍由研究者保留。

## 追加终点台账：频率 Full

pt-ho4byzg4 于UTC2026-10-09 17:48:33／北京时间2026-10-10 01:48:33达到平台SUCCEEDED。126轨迹、90,000训练答案、4500步完成；探索508/508、确认1012/1012、实际曝光126/126资格通过。1008个成员文件SHA核验后登记全部126保存家族。统计事实写入Summary/Detailed；归档的结果前设计正文与判据未改。实际SAE终点描述NOT_RUN，人类机制与关闭Unknown。终点/平台/登记证据：/data/250010109/MoE_Router/experiments/20261010_a17_fixed_pool_frequency/runs/full_4h100_v2_20261009T172612Z。
