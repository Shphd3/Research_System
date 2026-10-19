# 从共同出现分组到固定预算学习：执行 Protocol R1

日期：2026-10-16（北京时间）；处理：Codex /root。

本轮检验两件不同的事：关系分组是否超出频率背景；在相同四专家容量和输入曝光下，它是否改善低频特征条件的真实下一 token 预测。结构检验不自动推出学习价值，末端适配器结果也不自动推出早层路由价值。

本次研究者明确授权撰写、自审、修正和执行，不等待逐步审核。科学解释与问题关闭仍由研究者判断。原轮完整 H1 为 INSUFFICIENT；本轮修复是在查看原结果之后登记的探索性补充，不能回写为原确认检验。设计来源为[收到的 Anchor](sources/02_ANCHOR_关系分组到学习验证.md)及[执行要求](sources/03_PROMPT_交给现有Agent自主执行.txt)。没有创建另一个科学设计文件或改变 Focus 状态。

**正式执行冻结 R1.8。** 下文保留执行前设计及初步预算；[逐项修订](execution_amendments_cn.md)具有明确时间与原因。实际TRAIN130712位置/128contexts，EVAL523136位置/512contexts，固定low/high各3916、EVAL支持门槛20。每条件12个drop-last epochs=6120updates=1566720有效target exposures；0/510/1530/3060/4590/6120保存评估，mid3060，虚拟SGD lr0.1。主CI用4个连续context一块的paired2000draw比率线性化近似，非文档独立。实际配置为 execution根config/formal_R1_8.json；原初版缓存与配置不覆盖。

## A. 问题、竞争解释与决策

H1a：在固定行列命中数的二值随机矩阵上重跑全部选择过程后，实际 D/V 分组稳定性高于随机背景。竞争解释是边际频率、图筛选和分组算法已足以产生表面稳定性。

H1b：相同组大小和 D 平均 log 频率下，实际组的 V 组内 log 频率离散较小。竞争解释是 phi 对相近频率的偏好。完整组覆盖及混合资格是估计条件，缺失不是零效应。

探索 H2：关系分组 R 相对频率分组 F、匹配随机分组 N，在共同预算下改善预先固定低频特征条件的平均损失，且总体损失不劣于容差。竞争解释包括路由负载、频率组合、输入曝光、初始化及一般专家化；R 只赢一个条件不构成超出全部频率背景的支持。

局部机制：在同一训练中点，同一参数和 donor/probe 输入下，仅改变哪些输入共同更新哪个专家，是否改变随后 probe 损失？保持每专家 token 数，再分原始步长和每专家等更新范数。该干预支持局部更新交互解释，不能直接说明完整训练轨迹或证明全部根因。

## B. 输入身份与数据分工

冻结 Qwen3-0.6B-Base（revision da87bfb608c14b7cf20ba1ce41287e8de496c0cd），冻结最终 14 源层/F16384 CrossCoder（checkpoint_000999997440.pt，SHA256 09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628）。源层为一基 2,4,…,28，均为 block residual-post、最终 RMSNorm 之前。多层共同产生一个 latent，不把层数当样本数。

推断使用原 TRAIN CenteredRMSStats 和固定 EMA norm-weighted score cutoff 0.051281172782182693，不做 batch top-k、序列归一化或重新拟合阈值。模型、tokenizer、原缓存、数据及 CrossCoder 的[本轮严格访问检查](../../../assets/checks/2026-10-15_crosscoder_relation_learning_inputs.json)已通过；访问可用不等于测量正确。

结构 D/V 沿用旧 VAL 划分及缓存，D=5,238,097、V=5,247,663 个 eligible 位置。旧结果已暴露，且缺少原文档身份，不能声称独立文档确认。q10 是主构造，q20 仅已有构造敏感性，不搜索参数。

学习 TRAIN/EVAL 从原 TRAIN 文件的不同固定 context 窗口抽取，分别计划 128/64 个完整 1024-token contexts；每个位置 t 只使用至 t 的输入，预测真实 t+1。最后位置或 special target 按统一规则排除。它们不与结构 VAL 文件重叠；CrossCoder 曾以该 TRAIN 来源训练，文档/近重复独立性 Unknown，因此学习结论限于探索性分布内验证。精确 source offset、排除计数和实际 N 在缓存 manifest 冻结，不能按结果增删。

缓存原始末层 hidden、真实 target、三种固定 route、完整正激活 feature CSR、context/offset；不截断每位置 feature 数。缓存只节省 frozen base 前向，损失仍由原完整 LM head 计算。原完整模型与缓存CPU往返hidden经过同形状原norm/head的32位置logit及CE严格一致；zero适配器另守相同head计算完全不变。固定形状改变未来token因果检查及FP32截断诊断见R1.6，BF16变形状门控敏感性明确保留。

## C. 结构修复与统计量

旧原版 strict-log 端点完整保留。均值匹配按 D log10 频率均值±0.1 dex、相同成员数，对组外候选做 exact 单槽位 heat-bath：随机挑槽位，均匀抽取满足总和约束的允许成员，包含原成员的自环。目标分布为条件均匀，不逐个 draw 按 V 结果筛选。

每组两条独立链，burn-in=50×组大小，每隔 5×组大小步保留一次，每链 100 draws。检验小规模枚举的条件均匀性、链间差异、Rhat/ESS、初始成员更替；资格规则和耗时回执在正式端点前冻结。预算随组大小增长，覆盖全部 186 非单例组；若不合格保留缺失和成员覆盖，不用已合格子集代替总体。并列报告等组权重及成员权重、大小组分层。

二值 null 沿用每侧 128 contexts×32 位置样本，保留每行 L0 和每列命中数。固定 proposal 步数（包含拒绝自环），两链，burn-in=32×nnz、间隔=4×nnz，完整重跑支持筛选、phi、互选 q10、community 和评分；不只打乱组标签。B99 在资格和耗时后执行；若因预算减少，必须在新端点之前登记实际 B、最小可达概率 1/(B+1) 和未完成状态。

样本冻结支持条件为D≥25hits且≥8contexts、pair joint≥5；完整缓存仍D≥100hits且≥10块、joint≥10。各侧只纳入可估phi的正边，互选q10，再使用同一个weighted greedy modularity community算法，保留singleton但非单例为主统计量。支持资格和算法在每个null重算，而非沿用真实组。上述数字来自16:40:36冻结的registered_structure_config，未据null端点更改。

原严格样本 log 频率遇 V 零计数仍未定义。新增统一 Jeffreys 平滑 log10((nV+0.5)/(NV+1))，同时用于实际和每个 null；这是已知定义缺口之后的新探索性统计量，不能伪装原检验。稳定性为一对一非单例组 Jaccard 匹配均值；频率离散为组内 log 频率标准差及均值匹配差。Monte Carlo 解释要求保边际和混合资格，不能把不同链未混合样本称独立随机分布。

## D. 三种组与可执行路由

同一候选池为 R 的 186 非单例组的 13,807 个成员。R 保留实际成员；F 按 D 频率排序、按 R 大小多重集依次成组；N 在 D 频率十分位内打乱原组标签，每组每个频率箱成员数和组大小精确保留。N 在任何学习结果出现前检查旧组内边保留率和成员更替。

统一组得分为活跃成员比例，以 D-only 样本的均值和标准差校准。仅命中组竞争；D 标准差为零的组得分为零。并列由组成员集合的固定 hash 决定，不能用 R/F/N 名称破同分。零命中使用固定 fallback。D-only 负载约束分配把每个组映射至一个专家，可多个组映射至同专家，EVAL 标签与损失均不参与。胜出组未采用的得分质量、tie、组大小偏好、从不胜出的组、实际专家负载及 train update 次数均报告。

执行前修订 R1.1：原 mean-binary score 的 F 在 99.896% D 位置并列，成为 hash 主导对照。尚无学习损失时，三种条件统一改为上述 D 标准化得分；保留原诊断。本修复属于路由测量修复，不能按学习赢家再次选择评分规则。

## E. 学习、主指标与冻结预算

末端插入 K=4、rank=32 的 biasless residual adapters：h'=h+U_e D_e h。每专家 D 为32×1024、U为1024×32，4专家共262144可训练参数，每位置激活65536参数。base、CrossCoder、最终 norm 和 LM head 均冻结；位置不丢弃。down 非零、up 为零；同一 seed 的 R/F/N 初始参数、输入顺序、损失权重、优化器、批次和 exposure 完全配对。

三条件×三种子：20261016、20261017、20261018。AdamW，lr=0.001、weight decay=0；batch=256 valid targets；初步共同预算为3 epochs。吞吐/数值短测只用于确认共同预算和数值可行性；正式训练前另存不可变 budget/config/hash，不能据赢家延长条件。所有条件均算完整真实下一 token CE（nat/token），无伪标签、无其他监督。保存 step0、early、mid、final 完整状态及 per-position EVAL loss。

低/高频集合均由 D n≥100、至少10块支持的可靠候选15666个 feature 按 D p 排序，各取底/顶25%，并在同频处按 feature ID 排序；所有条件同一集合。low 可以含 route-pool 外 singleton，必须报告其覆盖而不能 outcome 删除。主指标先在 EVAL 对每个 low feature 的命中位置算平均 CE，再对固定 feature 等权平均；预定每 feature 至少20个 EVAL hits，未达者列明，并对全候选支持覆盖单独报告。条件使用同一个支持子集，该子集仅由计数决定。高频同法，另报总体 CE、零适配器到终点改善和 token 轴曲线。

实际意义阈值为 low 0.01 nat/feature，整体非劣容差0.01 nat/token；在结果前固定，并用零适配器 context 变动说明量级。支持方向要求 R 对 F 和 N 都达到阈值、三个 paired seeds 方向一致且总体满足容差；相反方向、任一对照未赢或总体变坏应分别报告负向、条件性或权衡。区间跨零与支持不足均不等于无效。分别报告 seed 差异及 paired context-block bootstrap，不把 token 当独立样本或把3种子均值称稳定。

训练遵守 token-axis TensorBoard、数据/forward/backward/optimizer/eval/checkpoint timing、loss/grad/lr、目标数和 resume 合同。缓存和 checkpoints 均留 execution，不进入 Git；新资产在交付前按实际保存登记，planned endpoint 不算保存。

## F. 局部干预与首方向辅助分析

局部干预使用预定 mid checkpoint，16个 donor batches（256 positions），固定 probe（512 positions），选样仅依 D 频率/context及支持，不依效果。每个 donor 的 D-row 平均 log 频率分箱，在箱内置换路由标签，严格保留每专家 token 数；记录实际交换比例，空/低多样性箱不能声称有效交换。

同一初始参数分别计算 actual-route 与 exchanged-route 的一次无 momentum/weight decay SGD 更新，probe 始终按原 route。学习率先以0.1做只看有限性/量级的数值检查，若超预定数值界限回退0.01并在干预效果前冻结。每次恢复相同 checkpoint，虚拟更新不进入正式轨迹。第二版把交换更新每个专家的范数缩放至该专家实际更新范数，零范数不匹配明确标记。probe loss 改善为主结果，gradient cosine 与范数仅解释。R/F/N各自都做；共同出现条件专属解释必须有条件间区分，不能把共同效应归给 R。

辅助分析对固定 D 样本每个源层原始 H、不减均值，求第一右奇异方向 v；移除 (Hv)v^T，再用原 preprocessing/encoder/threshold 计算同一共享 z。先做 no-op 原样复现。报告每层移除能量、重构误差、L0、频率和固定原边/组变化；同文本同 feature 顺序画原始、移除和差值，共用原始/移除颜色尺度。首方向不命名为已证实 common。该支线不扩展成 projected training，不能阻碍主线交付。

## G. 资源、停止与交付

资源键：docs/execution_envelope.md 的 h100-4-reserved / shphd-lite-0911，单个四卡作业，任务内并行，不新增额度。当前管理容器仅一张 H100 MIG；本轮查询没有可复用的四卡运行实例，因此启动一个使用已授权 Reserved 配额的作业。先核实4张完整H100、占用、BF16计算、依赖，再做缓存/数值 smoke；不干扰另有3个8×5090恢复任务。资源上限6小时/24 GPU-hours，空闲25分钟自动退场；无额外 profile fallback 或重训CrossCoder。

本地CPU结构工作最多60分钟墙钟，先计时，B99可双worker优化但不能变统计量。无效前缀/目标泄漏/zero-adapter不复现时停止问题分支，保存证据并修实现；不改成合成任务交差。北京时间07:30收束，08:30前报告；实际早完成可提前交付，未完成分支明确计数，不写成假设失败。

工作根：/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z。代码根：同实验 analysis_tools/relation_learning。报告根为本目录。交付一页中文摘要、英文报告及中文伴随、实际Protocol及连续简短audit、CSV、≤5种主图和绘图代码、配置/checkpoint/log地址、变更清单。每项解释写明观察→竞争解释→区分干预→排除的解释→未解决部分。不存在数据时不预填结论，不改变原轮结果或科学状态，不修改skills或commit/push。
