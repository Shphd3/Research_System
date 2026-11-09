# 五臂统一2000步结果：loss曲线与趋势分析

**本包的主要观察：**A1在八个匹配评估点上均优于随机分发A2，低频teacher feature对应位置的收益更大；A1对A2的总体差距在500步后逐渐缩小。与原生A0相比，A1在250/500步损失较低，从750步起则较高。A1-deep始终低于全层固定分发A1，到2000步时与原生A0数值接近。原生A0在2000步的总体NLL最低。

这些是一个训练种子、同一训练前缀上的观察。下文的机制解释标为 **AI分析**，研究者科学判断 **Unknown**。所有模型的正式比较只到2000步（524288000有效训练token）；已在进行的2573步续训和后续臂不进入本包。研究者已要求停止续训监督；现有任务内自动续训继续。

## 1. 比较了什么，哪些量可直接比较

五个模型从同一seed17的随机初始权重出发，结构均为8层、hidden1024、8专家/top-2、507988992参数。训练数据为DCLM同一视图、同一四rank输入顺序；每步262144有效预测token。AdamW和数值设置沿用原实现，学习率1000步线性预热后恒定；没有因为本次只观察2000步而压缩调度。

A1使用冻结33B teacher在block7 norm2输出上经TopK32 SAE得到的feature，按8个冻结簇给专家打分。A2使用可重放的随机分数。两者都选两个专家、权重各0.5，固定路由分支没有router到表征的梯度回流。A0保留原生可训练路由；A4在原生路由上增加只更新router的teacher蒸馏；A1-deep只在后四层用teacher固定分发，前四层保留原生路由。

EVAL始终为同一留出集的2097152个有效目标token，且评估不更新load bias。总体NLL是每个有效目标token的平均负对数似然，单位是nat；数值越低，只表示这批EVAL数据上的损失越小。

| 臂 | 2000步总体NLL | 相对A0的差值 |
|---|---:|---:|
|A0|4.083142|+0.000000|
|A1|4.157604|+0.074463|
|A2|4.286028|+0.202886|
|A4|4.129442|+0.046300|
|A1-deep|4.085093|+0.001951|

[各步总体NLL数据](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/eval_nll_by_step.csv)；[2000步五臂×十频段表2](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/table2_step2000.csv)。旧A4/A1-deep虽保存到2573步，这里使用其2000步读数，不把较长训练的结果混入比较。

## 2. 整体loss趋势：A1胜过随机，但没有持续胜过原生

![五臂EVAL NLL曲线](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/figures/loss_eval.png)

每条线是一种路由条件；横轴是优化器步数，上轴是相应有效训练token数，纵轴为同一EVAL的NLL。八个测量点间隔250步，未平滑，也没有用误差带暗示不存在的多种子不确定性。右图只放大1000–2000步，便于看清接近的曲线。

五个臂的EVAL NLL都持续下降。A2在这八个测量点中始终最高，A1在这八个点都低于A2。这里能直接说：按teacher feature组织分发，相对于当前随机分发条件，有较低的同预算EVAL损失。

但这个差距没有持续扩大。A1−A2在500步为−0.205311，到1000/1500/2000步分别为−0.162660、−0.144562、−0.128423。A1仍较低，但500步以后的总体优势在收窄。它不是“随着训练越训越领先”的结果。

A1相对A0还有一次方向变化：250步差值−0.092436，500步−0.027840；到750步变为+0.045035，2000步为+0.074463。从750步开始，原生A0的总体EVAL损失低于全层teacher固定分发A1。因此，**相对于随机分发的收益，不能替代相对于原生路由的净收益判断**。曲线下降也不意味着A1已经收敛或决定了长期模型排序。

2000步时，A1相对A0不只是总体NLL较高，十个频率bin的NLL也全部较高；最低频bin0差值为+0.106506，最高频bin9为+0.070889。当前不能叙述为“牺牲高频换来比原生更好的低频学习”。A4相对A0也在十个bin上全部较高。deep相对A1在十个bin上都较低；相对A0，最低频bin0仅低0.004723、最高频bin9高0.002713。这些都是此种子/此评估集的差值，不是跨种子的确定结论。完整数据见[其他对照的十bin差值](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/secondary_contrasts_step2000.csv)。

![匹配步数的总体差值](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/figures/contrasts_over_time.png)

纵轴统一为“前一臂减参考臂”的总体NLL；负值有利于图例中的前一臂。图中同时呈现A1−A2、A1−A0、A4−A0、deep−A1和deep−A0，避免更换基线后混淆收益。数据见[总体对照差值](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/overall_contrasts_by_step.csv)。

### 训练CE与EVAL应分开读

![五臂训练CE曲线](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/figures/loss_train.png)

淡线为每一步原始训练CE，粗线为相同的50步尾随算术平均，从第50步开始绘制；50步对应13107200个有效训练token。这个平滑只用于阅读，不用于表格数值、评估或判定。右图为后段坐标放大，完整原始范围在左图和[原始曲线CSV](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/train_loss_1_2000.csv)。训练曲线的局部波动不能与八个固定EVAL点混用；上述趋势判断使用EVAL读数。

## 3. 低频teacher feature的收益更大，但不是每个feature都改善

feature ID来自同一个冻结teacher SAE字典，不等于学生内部已经对齐的同名feature。频率由DEV的feature激活率定义，bin0最低、bin9最高。每个bin的NLL是在该bin所有feature激活位置上累加CE，再除以激活次数。同一token可激活多个feature，所以十个bin不是互斥的token分区。

![分频段EVAL曲线](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/figures/loss_eval_by_frequency.png)

五种颜色与总体曲线一致。每个小图固定一个feature频率bin，显示250–2000步的NLL；**各小图使用自己的纵轴范围**，跨bin的差值大小应看下面统一坐标的差值图和CSV。数据见[各步各bin NLL](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/bin_eval_nll_by_step.csv)。

![A1相对A2的分频段差值](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/figures/contrast_frequency.png)

横轴由低频到高频，纵轴为A1−A2；负值表示A1数值较低。2000步十个bin都为负，最低频bin0为−0.286800，最高频bin9为−0.111418。500/1000/1500/2000四条曲线都显示低频端差距较大；低频bin0在1000步达到这四个点中最大的负差值后也收窄，高频端差距则由500步的−0.190451缩到2000步的−0.111418。

| 步数 | A1−A2总体 | bin0低频差值 | bin9高频差值 |
|---|---:|---:|---:|
|500|-0.205311|-0.321437|-0.190451|
|1000|-0.162660|-0.345799|-0.143042|
|1500|-0.144562|-0.314008|-0.126417|
|2000|-0.128423|-0.286800|-0.111418|

[2000步完整十bin差值](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/A1_minus_A2_step2000.csv)；[所有评估点的主差值](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/A1_minus_A2_by_step_and_bin.csv)。这描述的是携带这些teacher feature的EVAL位置集合，不把它直接改称为“所有稀有词都学得更好”。

## 4. A0和deep：实际集中度与路由可适应性都需要看

A1-deep在全部八个评估点的总体NLL都低于A1；2000步为4.085093，对A1差值−0.072511。它同时降低了A1的高频NLL：4.076663对4.144840。改善不只出现在高频端，因此不能简单归纳为“仅保护了高频”。

deep对A0的早期优势逐渐接近零：500步差值−0.075831，1000步−0.006123，1750步−0.001082，2000步+0.001951。最后两条曲线数值很接近；一个种子和未量化的不确定性不足以宣布稳定优胜或等效。

M̄按每层实际专家分配的覆盖率、纯度及共同DEV频率计算，先对8层取算术平均，再对feature汇总。下表是30000个已观测feature的**非加权分布**；所有臂未观测feature数和非正M̄数均为0。它与按有效token平均的总体NLL不是同一个加权总体，不能直接对两个均值拟合比例关系。

| 臂 | M̄的10%分位 | 中位数 | 90%分位 | 非加权均值 |
|---|---:|---:|---:|---:|
|A0|0.326071|1.010460|1.954878|1.086753|
|A1|0.325778|0.585752|1.498841|0.793796|
|A2|0.189535|0.256799|0.324297|0.262353|
|A4|0.344621|0.810892|1.690152|0.943298|
|A1-deep|0.373319|0.870829|1.623020|0.960332|

按本轮的teacher-feature/实际路由定义，A0的集中度并不低：中位数1.010460，高于A1的0.585752。不能把原生A0近似当成随机分发基线。A4的中位数0.810892低于A0，其总体NLL在八个评估点都高于A0；当前没有看到该蒸馏设置带来总体NLL改进。A4在2000步的router/teacher原始top1一致率约37.9%，第500步为26.4%，后者低于原Prompt要求如实报告的50%诊断线。

这不能直接反证“集中信号有用”：A4既没有在分布中位数上超过A0，也没有完整复制teacher的分发。仍应区分监督未形成所需路由，与形成路由后没有收益。分位数不是逐feature同向变化的证明，原始配对数据保留在[五臂逐feature统计](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/feature_stats_all_arms_step2000.csv)。[A0逐feature及逐层M̄](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/A0_Mbar_per_feature.csv)和[按bin/层汇总](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/A0_Mbar_by_bin_and_layer.csv)单独提供。

## 5. 图3：正关联存在，噪声机制仍没有被直接确认

![2000步逐feature收益与集中度差](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/figures/fig3_A1_vs_A2.png)

每点为一个teacher feature。横轴为log M̄(A1)−log M̄(A2)，纵轴为NLL(A2)−NLL(A1)，因此上半平面表示A1的该feature条件NLL较低。所有30000个feature均进入本图。2000步Spearman秩相关为0.255924；500/1000/1500步分别为0.311408、0.260775、0.233929。点估计均为正，但不呈单调增加。

图中也有反例：176个feature的纵轴为负。为展示边界而事后选出的最负例是feature1595，在693个EVAL激活位置上，Δlog M̄=1.833863，收益=−1.604415。它说明“集中度更高就逐feature必然改善”不是这些读数的确定性规律；不赋予该feature语义标签，也不据这个挑选例推断总体失败。

作为**事后探索性诊断**，分别在十个冻结频率bin内部计算同一秩相关，点估计全部为正，范围0.101266–0.356988，低频两个bin约0.340/0.357。粗频率分箱没有消除关联，但这不等于已经排除了频率、共激活或路由结构的所有共同影响。各臂使用共同p_i，取集中度比值时其共同频率因子会抵消；不能仅用“公式除以p_i”解释Δlog M̄的相关。该诊断没有预登记为主裁决，不替代原判据。

[图3逐点数据](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/fig3_A1_vs_A2_points.csv)；[原登记的相关点估计](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/primary_spearman_by_step.csv)；[探索性分bin秩相关](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/tables/exploratory_within_bin_spearman.csv)。feature之间存在依赖，不是30000次独立训练重复。研究者尚未指定feature家族映射，家族bootstrap区间Unknown；梯度噪声遥测依新授权关闭，当前没有直接的训练中噪声下降测量。因此，不把正相关写成噪声机制已确认，也不套用缺少区间的支持/削弱判据。

## 6. AI分析：当前最合理的读法与仍活着的解释

**AI分析，尚未由研究者确认：**有组织的teacher分发比当前随机分发更有利，这个读法与同预算NLL方向及低频条件差值一致。但固定teacher分发也可能限制router与学生表征共同适应当前NTP目标；A0后来超过A1、deep接近A0，与这个候选解释相容。

一个可信的竞争解释是：收益来自teacher提供的token共享结构或语义信息，而非集中度单独造成的噪声下降。A1/A2共同固定0.5权重且没有router梯度反馈，可比较其分数来源；A1/A0和deep/A1同时改变了路由方式、权重或梯度路径，不能从它们单独识别是哪一个因素造成差异。

已经授权但本包尚无结果的对照提供区分预测：A3只按teacher频率信息分组。若A3复现A1，频率组织可能足以解释部分收益；若A3接近A2而A1保留收益，就限制“仅频率信息”的解释。高学习率臂的峰值为三倍：若低频的(A1-hi−A0-hi)比(A1−A0)更有利，符合可用步长增加的预测；一个三倍学习率点仍不能估计最大稳定学习率。这里不对未运行结果给结论，也不新增训练任务。

## 7. 本次可以交付的结论边界

可以确认这批保存读数的事实：五臂共同到2000步的评估完整；A1优于当前随机A2；低频teacher-feature位置差值较大；A0和deep在2000步的总体NLL更低；M̄与收益有正秩相关点估计。

仍不能确认：噪声下降的中介机制、teacher固定分发优于原生MoE、长周期或多种子收益、三倍学习率预测及A3频率控制结果。teacher训练时见过训练前缀，当前各臂只一个种子；0.52B是原调度前段；固定路由分支没有router梯度回流到表征。科学判断保持 **Unknown**，下一科学决定仍由研究者确认。

目标loss阈值未指定，因此没有临时制造“达标token数”。所有图和表的来源、选择范围与哈希见[来源清单](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/provenance/source_manifest.json)及[检查记录](/data/250010109/MoE_Router/experiments/20261109_teacher_routing_signal_concentration/deliverables/1109_teacher_routing_2000_20261109T022417Z/provenance/validation.json)。本包没有使用2000步以后的读数。


所属记录：[Protocol](protocol_cn.md)、[Detailed](detailed_cn.md)、[执行事实附录](urgent_execution_appendix_cn.md)。本轮挂靠既有A17_13，不修改其历史Anchor裁决或Focus状态。
