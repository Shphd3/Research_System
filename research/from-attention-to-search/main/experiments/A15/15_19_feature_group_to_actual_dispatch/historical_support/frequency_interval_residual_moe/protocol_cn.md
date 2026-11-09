# 频率区间固定路由的残差MoE旁支：Protocol

状态：**用户已授权审计、smoke及通过门槛后的有限执行**。本文件记录当前用户给定的独立旁支，不修改原φ研究Focus/Anchor。执行run：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z`；用户问题与边界是本轮设计来源。研究者的科学结论与问题关闭状态仍Unknown。

## 目的—假设—对照

在冻结Qwen3-0.6B Base表征上，检验按feature频率区间构造的固定路由，能否相对保组大小随机路由改善包含低频feature的输入的NTP学习。NTP指以当前位置已经可见的前文预测真实下一token，用每个有效预测位置的自然对数交叉熵计量。假设是待检验的A低频验证loss低于B；竞争解释包括诱导的负载/样本重复、评分尺度、旁支优化和过拟合。该实验不验证φ分组，不判断从头预训练容量，不以谱平坦作为成功条件。

| 条件 | 专家与路由 | loss |
|---|---|---|
| A | 8独立普通FFN；TRAIN频率原始p尺度线性等宽8区间；固定top1、单位gate | NTP |
| B | 同一feature池随机重分组，逐组人数严格同A；不匹配组内频率；同型固定top1、单位gate | NTP |
| C | 同8专家；normalized h的可学习线性router，softmax选中概率乘被选专家输出 | NTP |
| D | 与C完全相同 | NTP + 0.01 LB |

A/B主比较；C/D只判断该可学router设置下LB影响；A/D仅整体方法比较。C/D选中概率gate保证任务梯度可进入router，不能把argmax的不可导单位gate误当已学习router。

## 数据与缓存

复用原relation_learning/20261015T164000Z/data/train.pt和eval.pt的同窗原始h、token位置与t+1标签身份：TRAIN128个完整上下文、130,712预测位置；EVAL64个上下文、65,402预测位置。训练源为global01/local-shard5/shard41，验证源为local-shard2/shard247，不同源文件及token位置，不把训练内loss称独立泛化。原文档/近重复独立性Unknown；CrossCoder训练见过这些学习文本，教师表征固定，不声称整个研究流程未见验证文本。

旧cache只有完整门控feature IDs，没有数值z。复用同模型、A22最终checkpoint、14层零基1,3,…27、原TRAIN均值/RMS与严格threshold=0.051281172782182693，以base每批8个完整1024token上下文、coder每批1024位置补提取z，记录教师前向与路由成本。将h、z、target、context及绝对offset作为同一批数据保存；逐项比旧ptr/ids/offset/target/h。若硬件数值造成差异，保存完整新同窗h+z并报告差异，不拼接异窗/异前向。

排除当前或下一token为原特殊ID的位置及context最后位置；不额外删低匹配、全零或多组输入。h是第28层residual-post、最终RMSNorm之前；旧zero-guard和抽查标签通过仅作为复用证据，新smoke重新核等价。用旧native FrozenHead运算顺序（BF16 residual→FP32 RMS→BF16→原norm权重→原head），保持原输出路径。

## 分组、评分与可检验性

所有频率及资格仅来自新TRAIN有效预测位置。p_i=命中次数/N_train，命中指z_i>0；支持池n_i≥200、覆盖≥20个原1024-token上下文、n_i<N_train。以池中[p_min,p_max]在**原始概率尺度**np.linspace成8段，左闭右开，最后含p_max；不按人数或log频率分箱。

预先只读旧事件缓存得到参考人数[9253,183,124,34,7,3,2,9]；正式人数以同窗补提取后的TRAIN为准并冻结。不得因为箱小/分配不好修改线性定义。报告全部边界、人数、命中率、z/贡献量、正分数路由率、fallback、上下文覆盖及空/弱组。

CrossCoder没有强制decoder单位范数，raw z受正尺度重参数化影响。固定贡献分数c_i=z_iΣ14层||d_li||_2，组分数s_e=Σ组内c_i/组总人数，零激活计入平均。c对单个feature的正尺度重参数化不变，仍为归一化解码幅度指标。A/B严格同式；不使用验证或学习结果选score。

固定种子20261018、20261019。B仅将同一池按该seed随机洗牌，再按A各组大小切分，保存成员表。每pair四臂共享专家初始化和数据顺序；router使用独立RNG以免改变专家初始化。并列最高分与全零均用seed+源文件/context/绝对token位置的无状态哈希选专家，不随batch/rank/先后变化。

**正式训练前门槛**：8箱均非空且p有跨度；每个专家在TRAIN有正分数的实际top1路由至少200位置且覆盖至少20contexts。全零fallback不能补足。若失败，线性方案在当前数据/评分定义下记“不可充分检验”，保留preflight与必要smoke，正式A/B和次要C/D标NOT RUN；不改箱、不追加对数方案来替代主结果。

## 模型与训练

8个独立无bias普通FFN：1024→w→GELU→1024，全部矩阵可训练；不是LoRA。输入x=(h−TRAIN mean_h)/TRAIN scalar_rms，四臂同一固定归一化；delta加回原h，再经冻结原final norm/head。上投影按1/sqrt(1024)随机初始化，下投影零初始化。初始logits须与零旁支精确相等；所有基座/头/CrossCoder参数冻结，但head到专家的自动求导保留。首步up与任务router梯度为0属零down的预期，后续检查实际获得输入的专家与router梯度。

候选w=64/128/256，参数量为8×2×1024×w，分别1,048,576/2,097,152/4,194,304；top1每位置FFN主矩阵FLOPs约4×1024×w（FMA按2），GELU及索引另列。C/D router无bias，另加8,192参数及约16,384FLOPs/位置；不声称四臂总参数严格相等。冻结词表头投影与教师成本单列。

AdamW：初始lr=3e-4、betas(.9,.95)、eps1e-8、wd.01、global grad clip1；dropout0。有效batch256，无累积；最多512更新=131,072有效训练目标，约1遍旧窗口。固定数据顺序，不因路由丢弃overflow token；尾部顺接同seed下一epoch的排列，以保持每更新256有效目标。没有early-stop挑best，终点固定。共2seed×4条件8臂；A/B第一波4卡，C/D第二波。

用实际smoke计时后，仅按显存/吞吐选择可在30分钟正式主动计算估计内完成8臂的最大候选宽度；若512更新预算不符，统一从512/256/128中取满足预算的最大值，四臂两seed完全同预算。小于128更新则记录资源不足，不伪装完整。候选宽度与预算规则在学习结果前固定；实际选择写config及补充收据。

C/D的LB定义：在完整有效global batch上f_e=路由到e的位置数/N，P_e=softmax概率的batch均值，LB=8Σstopgrad(f_e)P_e，均匀时为1。C系数0，D为.01，raw/weighted均记录；A/B不加不能改变路由的LB。记录真实负载、各专家目标数、grad/update次数及零暴露，不人为抹平。

## Smoke、异常和运行

先核标签shift、special/padding掩码、source/context/offset对齐，初始等价与冻结hash、后续有效专家和router梯度；统一128位置小集32更新须能拟合，验证loss须有限且记录走势。计时每候选宽度8更新，不用A/B验证排名调参。仅在非有限、实现错误或全部统一小样本无法拟合时作一次有界共同LR降档到1e-4，四臂全重置；保存首轮失败。TRAIN下降而EVAL上涨单列过拟合/分布差异，不称符号错误。smoke与正式结果分目录。

执行面acp、resource_profile=h100-4-reserved、image_id=shphd-lite-0911，遵循execution_envelope及模板；从当前11109会话实际提交，不新开CCI，不改旧作业，不启用Spot/付费后备。当前11109 MIG仅作环境检查，不在未登记profile上偷偷开正式训练。有限pipeline总wall上限90分钟、正式主动计算估计上限30分钟、CPU aggregate RSS64GiB、单卡allocated32GiB、新增磁盘8GiB；超限保存可恢复状态与缺项后停止，无自动扩大资源。

## 评价—解释—结论边界

低频评估集合单独定义为支持池TRAIN频率≤第10百分位的features，高频≥第90百分位；这是评价子集，**路由8箱仍线性等宽**。mask为至少一个相应feature命中的位置并集，各位置仅计一次，来自未插旁支教师。记录低/高mask交集和覆盖，不能称某条低频知识被学会。逐feature验证支持≥20才可估；不足保留NA，不用验证重选feature池。

主指标：每pair终点低频验证位置平均NLL差A−B；同时整体与高频差、逐feature差/宏平均/位置平均、训练预算曲线。实践门槛事先δ=.005 nats/有效位置（约0.5%困惑度相对差，效用判断仍待研究者）：两pair的低频差均≤−δ，且每pair各自总体差均≤.005才记本旁支支持；方向混合、支持不足、gate失败均不足；两pair均≥δ则不支持；其余方向一致但未到实践门槛也记不足。有限两seed不提供总体显著性保证。

报告原基座/初始/训练中/终点loss，eval检查点0/32/128/256/512按实际预算截取。每feature及每expert计算q_i,e=路由e位置中i的命中比例；给名单频率组→实际专家矩阵、组外成员、低频覆盖、负载和零暴露，说明名单归属不保证实际送入该专家。A更同频且学习改善仅是相伴；更同频未改善说明此性质不足；名单同频但输入不更同频说明未落实到输入；全部臂劣于基座先保留训练/保真诊断，不宣布所有分组无效。

先交付A/B学习曲线与C/D独立曲线、分配矩阵/负载、专家内实际q分布。后对训练后专家上/下投影分别报告W和ΔW的完整奇异值摘要（min(w,1024)个），前16展示，绝对值与归一化占比分开。跨策略比较谱分布，不按相同专家号推功能对应；奇异值不是方向相似、平谱不是容量。去首/前16方向响应为附加诊断，本轮不自动执行。

## 产物与批准审计

已核对输入资产ID：`model_qwen3_0p6b_base`、`tokenizer_qwen3_0p6b_base`、`representation_crosscoder_qwen3_final14_f16384_val10485760_phase1_20261013t173130z`、`analysis_crosscoder_feature_frequency_20261015t143300z`、`representation_crosscoder_relation_learning_20261015t164000z`。当前严格访问收据为执行目录`provenance/asset_access.json`；只证明可读，不代替本轮数值和位置检查。A22最终权重精确路径为`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt`。

Protocol英文主件与本中文伴随；execution保存配置、code/sourcehash、分组成员/频率、同窗cache来源、原始JSONL/TensorBoard、参数/激活FLOPs、init/mid/final可恢复状态、逐位置/逐featureloss和图来源。一页中文Summary按目的—假设—对照—现象—解释—结论边界—下一步写，完整Detailed保存偏差与失败。实际保存的checkpoint必须登记registry；禁止commit/push/外部上传。

A–G逻辑审计：用户明确了问题/模型/比较/边界并委托实现与预算选择；AI选择的支持门槛、低/高评价分位、score、gate细节、smoke门槛和δ事先公开并冻结。审计重点是同窗身份、无V调参、C有任务梯度、D只差LB、实际负载是结果、两个seed的有限证据。本旁支不创建新Focus或改旧科学状态。当前字典指标和工程完成均不自动构成机制判断。
