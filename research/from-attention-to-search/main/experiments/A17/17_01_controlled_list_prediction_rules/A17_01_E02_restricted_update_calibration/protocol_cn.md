# Protocol: A17_01_E02 Restricted Update Calibration

## 0. Approval Snapshot

`APPROVED_FOR_IMPLEMENTATION_AND_SMOKE`；此提交前冻结时结果`NOT RUN`。研究者在2026-10-10（Asia/Shanghai）明确要求子Agent执行LoRA Smoke，并询问直接更新末投影是否更合适。二者不等价，因此保留先前提出的同位置L/R8工程对照。仅授权一次4H100 reserved有界Smoke；频率、SAE/表征执行、Full、发布与科学采纳均未由此授权。

下列具体pilot设置是已授权范围内的工程选择，不是研究者确认的新科学阈值、机制或最优容量。F科学近零阈值、学习器与窗口采纳仍Unknown；它们不妨碍目标/冻结/恢复/有限读出的工程资格测试。

目的：核验受限更新器及可读测量链。工程竞争解释为更新器无效/损坏，或仍迅速饱和。[Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor_cn.md)与[Focus](../../../../focus/focus_list_rule_shared_update_cn.md)保持问题归属。

[English](protocol.md) · [E01](../A17_01_E01_stage1_smoke/summary_cn.md) · [频率草案](../A17_01_E03_fixed_pool_frequency/protocol_cn.md)。

## 1. Terminology / Definitions

受限更新只改指定矩阵或其LoRA因子，其他权重不变。LoRA把新增矩阵写成两个低秩因子的乘积；它不保证仅改变格式响应。“高层”是位置，不是已证实的表层功能。首项/末项共用同一个可训练模块，不增加任务独立adapter、expert或router。

全词表答案CE单位nat/答案；更新后减更新前为负是该次改善；来源还须改善自己的独立同规则损失。两种未见仍相对于本轮任务训练。

## 2. Anchor Alignment

保留首项/末项问题、配对载体、分词器、答案损失和两种未见。限制更新范围有助于定位参数位置，不证明规则独特功能。LoRA可能引入容量瓶颈，其冲突只能归属于该受限学习器；原始两条可见规则可以同时满足。

## 3. Tested Hypothesis

AI假设：末层输出投影能适配任务，同时保留足够误差测有限跨规则作用。竞争：此位置/秩无法有用适配，或仍很快饱和。来源能学、接收作用符号、数值可分辨必须分别核验。

## 4. Rival Explanations

全对终点不保证CE变化可辨。参数少不保证学得慢。初始低准确率可能来自格式/答案先验。LoRA和同位置全秩仍同时涉及参数化、优化与容量；同LR不等于同功能步幅。零初始化输出因子时另一因子初始梯度可为0，不视为路径损坏。

## 5. Data Construction And Provenance

新strict访问后复用data_a17_list_rules_v1：训练4,000/dev800/test800，20词、固定模板、规则可见、训练精确均衡。仅读train/dev，已打开dev不产生确认结论。每规则5个独立种子来源批，每批100行，20个答案词各5行，训练内分层抽样；可行时首项/末项配同列表来源。保存ID/内容组/词频；不再按编号取前缀，不按跨规则损失选择来源。

## 6. Learning Task And Permitted Supervision

输入仅到“答案：”，正确词允许出现在列表中，已填答案不输入；只监督下一答案词元，全词表CE。不开三选一输出、不加辅助损失、不做表征/SAE研究。

## 7. Model / Architecture And Frozen Variants

AI默认用原始model_qwen3_0p6b_base，不用E01适配终点。已核验config为28层、宽1024、16头×128维，最终模块model.layers.27.self_attn.o_proj，矩阵1024×2048。

校准两条件：L直接训练该矩阵，2,097,152参数；R8冻结原矩阵，加共享rank8 LoRA，alpha8/scale1、dropout0、无可训练bias，因子共24,576参数。冻结embedding/绑定head、norm、MLP和其余Attention。输出因子零初始化应在同精度复现原模型。插入最终Attention输出投影，前序计算保持不变；固定后续MLP/norm/head仍会响应新输出，所以不保证仅改格式。

E01全参数结果只作历史参照，新batch/优化网格下不构成匹配对照。Dense留作后续载体复验；本校准不训练S7、不扩大秩。若R8失败而L能学，可再前瞻提出rank16，不能默默加入。

## 8. Training Objective And Optimization

AI网格：两条件都取AdamW LR1e-5/1e-4，betas(.9,.95)、eps1e-8、decay0、clip1。可训练参数/状态FP32，冻结载入精度一致；BF16计算，有限作用加FP32核验。答案损失和除以实际有效目标数。每条件独立单GPU，micro5×accum4=20答案/步，首项末项曝光均衡；warmup40答案后固定LR，不随最终预算拉伸。每臂最多50步/1,000答案。与E01的64答案batch不同，跨E01比较不匹配；网格不是批准的最优值。

## 9. Conditions, Seeds, And Checkpoints

试点4臂=L/R8×2LR，seed17。0/1/2/4/8/16/32/50步测能力与CE并保存；0步保存初始状态。有限来源探针放在0/2/8/16，优先早期状态。保存优化器/scheduler/RNG/数据游标/计数与base身份；8步外进程恢复并用不中断下一步参照核验。所有状态保留，不由test选状态。

## 10. Primary Metric And Frozen Analysis Plan

主要产物是状态×来源×接收者CE变化图。从同一状态，分别对声明参数做普通SGD，候选步长1e-5/1e-4/1e-3，来源间恢复权重/RNG，按记录保存预先选定80条工程dev子面板的配对差（规则×未见×20答案词各1条）。完整800条dev仍在每保存点测能力与CE；有限探针不资格化完整dev上的来源有效性。训练优化器不被探针改动。报告全部候选，不只挑有利符号；来源资格由自己的dev作用判断，跨规则符号不能选择LR/检查点/来源。因子梯度内积不与全矩阵梯度内积当作相同功能更新。

分别报告规则×未见、类型合计与按记录加权合并，以及来源批间差异。数值检查含5次不更新、参数恢复及相同有限差的BF16/FP32对照。未校准的非零符号仍未解。AI操作候选：R8至少一个早期状态，两来源在某候选步长各至少4/5批产生可辨同规则改善，且BF16/FP32已分辨符号不相反。近零容差与共同步长选择规则待pilot数值和研究者判断，标记BLOCKED；本校准不做确认裁决/CI。

## 11. Secondary Metrics And Guards

记录来源/接收损失、新增有效矩阵范数、冻结权重漂移、可训练参数数、各规则曝光、总有效答案、优化步、必需TensorBoard、优化器和恢复、正确答案概率。同载入精度下冻结漂移必须0；不要求初始化两因子梯度都非零。另两种同义提示可作为未来格式/规则诊断，目前未激活，也不声称已有结果。

## 12. Known Good / Known Bad / Known Confusing Cases

已知好：零adapter与原生logits/CE一致，恢复后不更新一致。坏：填好答案输入、冻结head改变、来源塌到一词、恢复游标丢失、跨作用选状态。混淆：全对仍有残余CE、第一步因子梯度0、BF16差0但FP32可辨、R8不能学但L能学。

## 13. Scientific Procedure And Stage Contracts

1. 数据/shape预检：strict输入、目标范围、来源计数、模块身份，错则停止。
2. 本地契约：零adapter、冻结、归一化和恢复核验，写资格回执。
3. 有限试点：4臂、早期保存/CE与固定探针；非有限、冻结漂移、错计数/恢复或时间上限停止；值全部dev。
4. 审计：输出有效来源与精度/残余误差图，研究者选择窗口或修复，再决定频率实验。LoRA不是频率研究必需条件，其他合格学习器也可用。

## 14. Algorithm, Output, And Provenance Contract

冻结执行根/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update；需新源码/config/run，不改E01。复用答案wrapper/生成器/聚合；适配已读1007 SingleBranch的末投影低秩/冻结/恢复检查，不复用router、SAE诊断、benchmarks、旧1/8 scale或旧提交命令；本候选scale1明确。

产物：源码/config/数据/来源ID清单、strict输入、shape与冻结身份、损失/能力/探针/TensorBoard、保存和恢复、数值/终端审计。实际adapter保存后连同base登记并strict查输出。授权Smoke资源h100-4-reserved，4个独立单GPU条件，臂间不DDP归约；pilot载荷上限1,800秒，最多2H100分配卡时，平台额外开销另记。提交前重读当前envelope/image。仅此有界工程Smoke获授权，不授权Full或频率作业。

## 15. Success / Failure / Insufficient Evidence

工程PASS为目标/计数/冻结/原生一致、有限遥测、完整保存恢复与分项齐全；明确违约FAIL，缺失INSUFFICIENT。操作支持：声明范围存在合格有效来源/精度窗口；非支持：完整候选都没有；来源或精度未解则不足。这不裁决稳定共享/干扰，采纳由研究者决定。

## 16. What This Cannot Claim

不证明LoRA更优、低秩纯因果、只改格式、任务自然冲突、功能分解、预训练习得、普遍掌握、表征或专家必要性。同LR不是同功能步幅；dev不是未打开确认。

## 17. Block Confirmation, Freeze, And Amendment Ledger

已确认问题与任务边界不变。A/C继承已确认载体事实。研究者本轮授权实现及子Agent Smoke；B/D/E/G的具体pilot值为该范围内工程选择，不代表科学采纳。F工程门槛固定为目标计数、原生一致、冻结字节、有限日志、完整保存/重启和分项齐全。F科学近零阈值、后续窗口和学习器采纳Unknown，本轮不判定；不据此促进频率科学协议。

2026-10-10（Asia/Shanghai）提交前工程收窄：有限探针用固定80条分层dev子面板，适配总载荷1,800秒上限。0/2/8/16状态仍保留5个答案均衡来源×3步长×BF16/FP32，完整800条dev保留在每能力保存点。来源按规则独立分层；本工程收窄不做同列表配对来源，manifest记录false。原生一致用20条dev及双精度；不更新重复5次。只评定精确工程漂移/恢复；科学符号仍未解。

首次提交前记录源码/config/Protocol/数据hash和实际命令。E01冻结体不改。开始后保存本正文；故障修复仅追加修订及资格影响。非有限、冻结漂移、计数/恢复违约或总载荷1800秒停止，不扩pilot、不打开test。

依据：[LoRA论文](https://arxiv.org/abs/2106.09685)、[观测契约](/data/250010109/Research_System/docs/training_observability_contract.md)。

## 仅追加执行台账：2026-10-10 Asia/Shanghai

一次作业pt-bw3s1pxw，4H100 reserved，无重试/扩范围。提交前冻结正文归档`/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_20261009T162413Z/protocol_frozen_cn.md`，原hash在frozen_sources.json。源码修订01在pod实际运行前，将原生一致门槛加强为BF16/FP32全词表logits与逐条CE精确一致；保留原runner字节/hash和修订后hash。目标、数据、优化、探针、采纳判据均未改变。运行/终端事实由Summary/Detailed持有，不重写注册正文。

## 仅追加工程修复02

首个job pt-bw3s1pxw在update0探针恢复守卫失败；4个初始原生一致状态实际已保存，正式训练0步。FP32基线错误地保留了最后一个BF16虚拟更新；每种精度开始前恢复声明参数/RNG即可修复。含实际探针隔离回归在内的8项CPU测试PASS，保留失败产物与源码revision1。研究者已授权的有界工程Smoke内允许一次同profile/四臂/50步范围修复重试；不采纳科学设计、不扩Full/频率/SAE。重试1600秒+首载荷保守64秒+kill宽限30秒，小于总1800秒。新run `/data/250010109/MoE_Router/experiments/20261010_a17_restricted_update/runs/smoke_4h100_retry01_20261009T163401Z`冻结精确源码/config/父状态。失败探针数值不复用为结果。

## 仅追加数值符合性边界

此pilot分别在BF16/FP32计算来源梯度，并在相同精度读出。因此这是两条完整“更新+读出”管线的比较，不是固定同一实际功能扰动后的两个reader。它只提供有界工程精度事实，不能独立归因reader误差或资格化科学来源符号。未来若做科学数值资格，须固定同一真实扰动分别用两reader评价，或明确分开梯度方向与reader改变；本轮未因此再运行作业。
