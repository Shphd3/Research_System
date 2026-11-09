# 频率区间固定路由的残差MoE旁支：Detailed

## 目的与实际停止点

本轮原问题是：冻结Qwen3-0.6B Base及CrossCoder后，原始概率等宽频率分组的固定路由，能否相对保组大小随机分组改善包含低频feature输入的NTP学习。用户授权先Protocol、逻辑／实现审计、smoke，合格后自主有限执行，不改变旧φ结果。

**实际只完成同窗表示补齐、分组／实际路由诊断和必要工程smoke。正式A/B、C/D学习比较均NOT RUN。** 原因是事前TRAIN覆盖门槛失败；不是预算用尽、训练爆炸或已经观察到“没有学习收益”。问题的学习效用答案仍Unknown。

[一页概要](summary_cn.md) · [冻结Protocol](protocol_cn.md) · [完整输出机器记录](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/provenance/analysis_results.json)

## 假设、竞争解释与对照

主假设是配对A−B终点低频验证位置平均NLL改善；事前实践门槛为每seed差≤−.005 nats，同时每seed总体差≤.005。两seed为20261018、20261019。未达到上述支持或反向门槛、方向混合或可测性失败均不足。A/B检验整体频率分组策略，不能仅凭伴随的输入同频性识别中介。C/D仅比较LB，A/D只是整体方法比较。

A为8个原p线性等宽区间＋固定top1；B同feature池随机分组，逐组人数严格同A，不匹配组内频率。C/D使用同FFN和可学习线性softmax router，D仅多0.01LB；LB=8Σstopgrad(各专家batch分配比例)×各专家softmax均值，完整256位置batch计算。A/B单位gate；C/D选中概率乘专家输出，以保留任务router梯度。C/D另有8192个router参数，不能说四条件总参数严格相等。

竞争解释包括评分的边际频率／幅度优势、实际负载与训练暴露、优化或过拟合。名单同频不等于输入同频。本轮直接检查了这一前提，没有进入收益／中介判断。

## 模型、代码与数据身份

|对象|实际来源与界面|
|---|---|
|基座|`/data/share/Qwen3-0.6B-Base`，原norm／head冻结|
|字典|`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt`，14层16384维、原TRAIN归一化与冻结门槛0.051281172782182693|
|抽取层|零基block 1,3,…27；末层h为第28层residual-post、最终RMSNorm之前|
|本轮执行|`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z`；代码身份以文件SHA为准，MoE_Router根目录没有可读取Git仓库元数据|
|旧学习缓存|`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z/data/{train,eval}.pt`|
|TRAIN|global01/local-shard5/shard41；128上下文，全局context8192…8319；130712有效预测位置|
|EVAL|global01/local-shard2/shard247；64上下文，全局context117658…117721；65402有效预测位置|

上表字典与旧缓存绝对路径以[提取收据](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/provenance/cache_preparation_receipt.json)的inputs为权威。TRAIN文件为`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_5_of_10_shard_00000041_processed.bin`；EVAL为同global目录下`local-shard_2_of_10_shard_00000247_processed.bin`。两文件各从文件offset8388608开始；不能只凭相同offset拼接它们。标签为当前位置t的真实下一token t+1，排除当前／下一token特殊ID及context最后位置，无padding目标。

旧缓存只有正激活ID，没有数值z。本轮同一次冻结前向同时保存h与数值z；TRAIN/EVAL的h、label、CSR指针、IDs、context及绝对offset均与旧缓存同dtype逐元素精确相等。原bin SHA来自已有来源记录，当前stat及逐位置内容交叉核对；未重新hash全原bin。缓存自己的输出SHA由producer新算。完整位置绑定与差异统计见上述收据。

本轮普通FFN为1024→256→GELU→1024，无bias，8个独立专家全参数可训练；专家参数4194304，top1激活其中524288参数，主矩阵FLOPs约1048576/位置（不含head、GELU、索引与教师）。C/D另加8192参数、约16384FLOPs/位置。这里只是必要smoke使用宽度，**未完成正式64/128/256吞吐选择**；width_timing为空，正式宽度／更新预算未确定。

输入为(h−TRAIN逐维均值)/TRAIN标量中心RMS；上投影随机、下投影零，输出加回原h后用冻结原norm/head。原路径BF16 residual→FP32 RMS→BF16→norm weight→head，CE FP32；冻结head仍传输入梯度。CrossCoder先用14层联合表征生成z，再决定末层路由，属于教师辅助，不是免费中间层router。

## 频率、评分与事前门槛

支持池为TRAIN命中≥200位置、覆盖≥20原1024-token上下文、命中<N_train，共9615feature。p_i=TRAIN中z_i>0的位置比例。在[p_min,p_max]原概率上线性等8段，左闭右开、最后含最大值；下表四舍五入仅为阅读，精确边界见[grouping.json](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/cache/grouping.json)。B按固定seed洗牌后按相同组人数切片。

评分先将c_i=z_i×Σ14层decoder范数，再对组内全部成员取平均（零也计入）。这是对单feature正尺度重参数化不变的解码幅度分数，**没有消除feature激活频率差异，也不是语义／功能贡献**。A/B完全同型。并列／全零用seed、源文件身份、context及绝对offset无状态哈希；本轮四个固定路由方案全零fallback均为0，A无并列。

|组／专家编号|TRAIN激活频率区间|成员数|A正分数命中位置|A实际路由位置|B seed18路由|B seed19路由|
|---|---|---:|---:|---:|---:|---:|
|0|[0.1530%, 12.4424%)|9,253|130,712|0|8,239|11,388|
|1|[12.4424%, 24.7319%)|183|130,700|0|5,728|4,183|
|2|[24.7319%, 37.0213%)|124|130,712|0|26,589|5,973|
|3|[37.0213%, 49.3107%)|34|130,712|129|11,791|6,622|
|4|[49.3107%, 61.6001%)|7|128,235|201|61,270|51,372|
|5|[61.6001%, 73.8895%)|3|125,395|646|3,499|1,741|
|6|[73.8895%, 86.1790%)|2|119,722|9,893|3,231|18,887|
|7|[86.1790%, 98.4684%]|9|130,583|119,843|10,365|30,546|

A两seed路由完全一致。B的expert编号只是各自随机名单的索引；跨策略不认为同编号功能对应。八组均非空，问题发生在实际argmax分配。A前三组每组几乎／完全覆盖训练位置，却路由为0，不能把它解释为这些feature没有出现。

正式资格事前要求每个专家有≥200个正分数实际TRAIN路由位置、覆盖≥20上下文，fallback不补数。A组0/1/2均0；组3为129位置／128上下文；组4…7通过。两个B分组各八专家通过。AI事前选择的200/20是本轮“八专家均有最低学习机会”的规则，不是普适统计定理。

## 三类图及图外解释

### 图1：名单、命中与真实路由

![名单、命中、实际路由](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/figures/analysis_members_hits_routes.png)

上面板是每组feature人数，A/B相同。中面板是各条件自身名单中至少一个成员命中的TRAIN位置数；一个位置可同时命中多组，故不能把各柱相加当token总数。下面板每个位置只选一专家，八柱相加为130712。差别揭示“组有成员／能命中”与“专家得到输入”之间的断开。

### 图2：原频率组的激活事件去了哪些专家

![频率组到实际专家](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/figures/analysis_event_allocation_train.png)

所有A/B面板使用**同一套A的TRAIN频率组**为行，列为实际expert；outside为支持池外feature。每格先数该行feature激活且其输入路由到该expert的事件，再按行总事件归一化。一个位置可贡献多个feature事件，因此这张热图不是位置百分比。右侧负载柱才按位置计数。

A各行事件都主要流入expert7，所有位置中119843/130712=91.6848%进入该专家。低频评价feature共964个（TRAIN p≤池10分位0.002455780647530449），都在A组0；包含这些feature的95544位置中，实际路由为[0,0,0,0,136,603,6281,88524]，其中expert7占92.6526%。EVAL对应逐位置分配为[0, 0, 0, 0, 69, 175, 4439, 44608]，是固定规则的数据分配描述，未用EVAL调规则。

[低频位置并集小表](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/tables/analysis_low_position_union_routes.csv)每位置只数一次；[EVAL矩阵](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/figures/analysis_event_allocation_eval.png)为描述性复核，不是学习收益。

### 图3：每个专家内实际暴露频率q

![专家内实际feature频率](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/figures/analysis_within_expert_q_train.png)

主量q_i,e=“送入expert e的位置中feature i命中的比例”，分母是expert位置数。图横轴为q，纵轴经验累计比例：9615个合格feature中有多少比例q≤横轴值；一条线对应一个专家，不是某个神经方向。q=0代表该feature在已有输入中未命中；没有任何输入的expert0/1/2分母0，整列NA、无曲线，不能当q=0。每个expert样本量不同，尤其expert3只有129位置，曲线不是显著性证据。

另存allocation_share=P(expert e | feature i active)，其分母是feature总命中次数，回答“该feature的输入去了哪”，与q不能互换。全部16384feature（含池外）的count、q及allocation_share均存NPZ/CSV。主图没有功能编号匹配，也没有同频中介结论。

这里的q分母为各expert在固定缓存窗口的一次路由位置数，**不是正式训练中累积暴露**；正式训练未启动。以后实际训练q需按每update保存的路由与数据顺序累加，允许同一源位置在不同更新进入不同专家。

## Smoke：通过什么，没有证明什么

原模型与缓存路径匹配输出head矩阵形状的32位置logits／CE误差0；分支zero guard也精确0。基座／CrossCoder参数版本及buffers未变，head前后SHA一致。下投影首步获得梯度，上投影和可学习router首步任务梯度0符合零down预期，后续均非零；未获得输入的专家没有梯度属真实路由结果。

smoke只有seed20261018，四条件共享128训练位置、初始化和顺序，反复32更新；另固定128个EVAL位置只核有限性与走势，不用于调参／排名。lr=3e-4，无重试。

|条件|128个训练位置NLL：初始→32步|另128个验证位置NLL：初始→终点|工程资格|
|---|---|---|---|
|A|3.642010 → 2.183547|3.039889 → 3.058244|PASS|
|B|3.642010 → 1.333752|3.039889 → 3.056395|PASS|
|C|3.642010 → 1.176653|3.039889 → 3.056019|PASS|
|D|3.642010 → 1.192075|3.039889 → 3.059398|PASS|

小训练集下降、另小验证集略升，支持“可以拟合但不保证泛化”的诊断；不能简单归为loss符号或shift错误，也不能从这个刻意重复小集给出A/B或C/D学习优劣。逐step日志／TensorBoard与有效目标坐标通过持久化核对。同进程序列化下一更新完全相等；外部进程恢复NOT_QUALIFIED。

每臂主smoke32步=4096重复目标曝光，唯一训练位置128；另有一次128位置恢复replay诊断。实际保存的四个checkpoint都是step16／2048重复曝光，不是训练终点。正式run目录没有8臂完成记录。

## 基线、评价覆盖与缺项

本轮低频位置并集TRAIN95544/130712=73.10%，EVAL49291/65402=75.37%。高频集合962feature（TRAIN p≥池90分位0.045861129812106）的位置并集覆盖全部TRAIN/EVAL。所有低频位置同时包含高频feature，因此低／高输入不是互斥分类；低频知识是否掌握未直接测到。EVAL低频feature中944/964达到≥20支持，20个保持不足；高频962/962达到。

当前严格完整EVAL基座loss未重测，TRAIN全窗基座lossUnknown。本轮仅有上表128位置的原基座等价诊断。另复用旧512上下文保存的zero NLL前65402行；原h、label、CSR与位置前缀逐字节相等，得到**历史参考**整体3.023366253、低频位置2.886969903、低频qualified宏平均2.585700217。它使用head batch256，本轮设128且末批形状不同，故标`HISTORICAL_REFERENCE_ONLY / BATCH_SHAPE_NOT_QUALIFIED`，不进正式比较。旧整体2.949103620来自完整512上下文，与本轮64上下文不同，不能混用。[复用证明](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/provenance/baseline_reuse_receipt.json)及[小表](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/tables/baseline_reuse.csv)保留完整来源。

|必须回答的学习量|本轮状态|
|---|---|
|配对A−B低频／整体／高频验证差|NOT RUN，两学习seed未执行|
|逐feature学习收益与宏平均|NOT RUN，只有支持及历史基线参考|
|整体／低频正式学习曲线|NOT PRODUCED，不用smoke替代|
|C−D负载均衡影响|NOT RUN|
|正式训练累积q、各专家更新量|NOT RUN；已有固定路由窗口及smoke日志|
|训练后W及ΔW全谱／前16|NOT RUN，无正式终点|
|去首／前16方向响应|未授权为必做，本轮未执行|

验证与训练源文件／token位置不重叠，原文档／近重复独立性Unknown；CrossCoder原训练见过这些文本，冻结教师辅助分析不能称全流程未见验证数据。有限两seed、单个训练窗口与64个验证上下文不支持总体稳定性结论。

## 实际时间、资源与来源审计

任务pt-vv7zkyxf于10:52:51 UTC被接收，平台10:58:26启动、最终SUCCEEDED；进程10:58:31验证四张H100 80GB。缓存准备35.50秒，完整受控pipeline72.46秒；正式更新0。实际教师base前向1.765秒、CrossCoder编码0.521秒，另原生guard前向0.085秒；192上下文196608原始token另加guard8192token。其余时间包括加载、CPU处理、保存及smoke检查，不称全部GPU核心计算。

本地CPU后处理22.55秒、最多4线程，无新模型前向；历史NLL仅做CPU读取和聚合。Reserved分配4卡，但本轮因门槛停止，仅GPU0做提取与必要smoke，未启动原计划两波四卡正式训练。PyTorch峰值allocated为8.381GiB（非Torch内存不含）。smoke进程峰值RSS约2.82GiB；监督每2秒检查aggregate RSS≤64GiB、disk≤8GiB、wall≤90min，未记录连续全流程CPU峰值，不能用终点0.385GiB冒充峰值。

初freeze与实际训练源码有一个仅记录逐位置路由的观测补丁，发生在任何smoke更新前；旧source、旧freeze及[修订收据](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/provenance/freeze_observability_amendment.json)均保留。英文完整Protocol晚于初freeze翻译完成，中文设计SHA未变。A22确切ID补充strict访问核验晚于提取，已标明，不冒称事前选中检查。SCO仅run-local响应兼容补丁处理新增workspace字段，不改变提交身份／权限／profile。

## 认识变化与唯一下一问题

此前待检验的是“这种频率组织是否有学习收益”，用户已指出名单未必落实为输入。本轮证据把风险具体定位：原p线性八段都非空，但当前贡献均值argmax令三个专家完全无输入，低频输入主要进入最高频组专家。保留频率组织的学习假设，缩窄为当前名单＋评分无法提供足够八专家训练覆盖；未回答收益、同频中介、预训练容量或语义功能。

竞争解释仍是评分的频率／幅度耦合，而非频率分组天然无效。**AI建议唯一下一检验，尚未执行：**保持这八段、A/B成员、数据与tie规则，只登记一个TRAIN均分校准版本s_g / mean_TRAIN(s_g)，与原s_g比较是否恢复八专家及低频输入有效暴露。A/B同型，先只用缓存检验覆盖；不在本轮追补训练，不改原主结果。若研究者不接受该评分语义，则先讨论评分应表示什么，不开新跑。

## 交付索引

Protocol／Summary／Detailed由Research_System持有，代码、cache、模型状态、逐组成员和图表由本执行目录持有；不复制大payload到研究Git。所有图给PNG/PDF，源表与来源在[分析收据](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/provenance/analysis_receipt.json)。[分组成员](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/tables/feature_members.csv)、[支持表](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/tables/analysis_feature_support.csv)、[缓存分组](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/cache/grouping.json)、[smoke收据](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/smoke/smoke_receipt.json)、[资产指南](../../../../../../../../assets/frequency_interval_moe_cn.md)。本轮未commit/push，未进入下一实验或更新旧科学状态。
