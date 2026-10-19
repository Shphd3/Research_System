# Detailed：CrossCoder 从关系分组到学习 R1

[英文原文](detailed.md)。主要[Anchor](sources/02_ANCHOR_关系分组到学习验证.md)；[Protocol](protocol_cn.md)，实际执行R1.8及另行登记的R1.9数值对照修复、R1.10辅助诊断；[执行修订](execution_amendments_cn.md)。

处理：Codex /root。全部已授权计算已完成，四H100 worker于2026-10-15T17:39:48Z退出。研究者科学批准和问题关闭均为Unknown，未改变。工程守卫不会授予科学PASS。

## 0. 目的与证据范围

本轮问题是：特征联合事件是否具有超出边际频率的组织信息，以及所选组织方式能否在相同学习容量与曝光下，提供更好的末端专家分配。仅频率的几何、负载、输入组成、初始化与一般专家特化都是竞争解释。结构重跑属于看过原结果后的探索。学习在原CrossCoder TRAIN来源内，使用源文件不重叠的适配器TRAIN/EVAL；原始文档独立性为Unknown。中点干预识别有限的局部更新效果，不识别完整训练轨迹机制。

## 1. 对象与定义

| 对象 | 实际计算 | 含义与边界 |
| --- | --- | --- |
| Feature | 最终14层/F16384 CrossCoder共享latent的一个坐标；门控后为正时定义该位置的激活事件 | 不预设语义或知识身份 |
| 频率 | D侧正事件计数除以D有效位置数 | Feature频率，不是目标稀有性或预测难度 |
| 关系组 | D侧正phi、互选q10图上的连通社区 | 经过选择的统计组织，不是已建立的天然专家 |
| 匹配随机N | 在10个D频率分位箱内交换成员，精确保留组大小与各箱组成 | 连续频率仅近似匹配，并非所有统计量相同 |
| 路由 | 仅命中组参与的D标准化评分，选择唯一赢家，再经D负载约束映射到K4专家 | 只有分配决策采用一个赢家；每个专家仍接收完整h |
| 条件损失 | 在每个固定feature的命中位置求真实下一token CE均值，再对feature等权平均 | 相互重叠的条件总体，不是互斥任务或feature知识掌握 |
| 局部干预 | 实际donor标签与频率箱内交换标签对比，严格保每专家token数 | Probe路由与检查点固定；虚拟更新不进入正式训练 |

## 2. 冻结设置与合规证据

执行根R为 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z`；代码根为该实验的 `analysis_tools/relation_learning`。唯一新增分配作业为 `pt-szeffn72`，执行配置键为 `h100-4-reserved` / `shphd-lite-0911`。4张完整80GB H100已通过设备与BF16预检。既有恢复作业未受影响。资源上限6小时/24 GPU小时；本地结构计算墙钟上限60分钟。

| 合同 | 实际记录及证据 | 资格边界 |
| --- | --- | --- |
| 冻结base/CrossCoder/norm/head | Protocol中的模型与检查点身份；缓存buffer检查和训练版本守卫 | 必须通过的守卫，不是科学证据 |
| 真实目标与因果位置 | `data_eval512/native_zero_guard.json`、`data/prefix_precision.json`；最终norm/head之前的末端residual | 原完整模型32位置logits/CE完全复现；没有早层路由主张 |
| 相同输入/参数/曝光 | `config/formal_R1_8.json`、各run的 `run_contract.json`、`metrics.jsonl` | K4/rank32，总参数262144/每位置激活65536，种子和顺序配对 |
| 实际预算 | 每arm为6120更新×256=1566720目标；共9 arms | 12个丢弃尾部不足批次的epochs；固定学习预算，不代表收敛 |
| 数据 | TRAIN130712位置/128 contexts；EVAL523136位置/512 contexts | 来自不同源文件；原文档/重复独立性Unknown |
| 固定低/高频集合 | 各3916个；EVAL至少20命中；低频3737有支持、179不足，其中7零命中 | 低频覆盖95.429%；高频全部有支持 |
| 保存阶段 | 0/510/1530/3060/4590/6120 | 完整adapter/optimizer/RNG/order/counters；外部进程恢复NOT_QUALIFIED |
| 训练遥测 | Token/update TB标签、资源/梯度/负载及分环节耗时 | 串行GPU下一步weights+Adam重放完全一致 |
| 结构对照 | `structure/full_group_controls.csv`、`method.json`、`triple_counting_repair/` | 完整条件对照与样本全流程校准是不同证据 |
| 辅助分析 | `data/first_direction/` | 未中心化原始H删除；事后中心化控制另行登记 |

优化器为AdamW：lr0.001、betas(0.9,0.999)、eps1e-8、weight decay0、gradient clip1。非零down/零up初始化在条件间配对。冻结完整151936词表head以BF16投影；adapter与CE使用FP32。各条件的源h、真实目标和完整门控CSR完全相同。不做推断BatchTopK或依据结果拟合门控。

## 3. 修订、失败与不追溯改写

[执行修订](execution_amendments_cn.md)拥有完整历史。关键资格变化包括：在学习前以D-only信息修复F原评分的并列退化；以size2/3精确IID替代慢混合或罕见条件采样，同时保留其均匀目标；样本真实/随机条件统一增加Monte Carlo预算；区分文件内offset碰撞与源身份；严格BF16跨shape事件一致检查失败并保存，而固定shape改变未来完全不变，FP32截断事件差异为零。原head比较采用相同矩阵shape。正式学习前按支持计数一次扩EVAL，提高低频支持覆盖；旧缓存和全部学习设置保留。

样本严格经验log频率统计量，在V零支持时仍未定义。Jeffreys平滑后继版本是探索，不是原确认检验。罕见三元组拒绝采样触及固定上限；完整修复版本使用精确三元组计数，重新抽取每个固定图的小组对照，不只填缺失draw。Reserved节点的动态module Numba缓存导入失败；使用独立空缓存目录重新JIT，未改变科学代码或设置。

## 4. 汇总与不确定性

结构统计量T_a为非单例组一对一Jaccard匹配的组等权均值。完整T_b平均实际V组内log10频率标准差减去条件对照平均标准差。并列报告组等权、成员加权和组大小。保边际的样本null在两条链上共有99个计划draw（50/49），burn-in为32nnz个提案、间隔4nnz，包含拒绝自环。3个worker仅并行评分。有限混合诊断与平稳性论证不能证明全局混合或IID draws。近似尾概率分辨率为0.01；不保证名义家族错误率（FWER）。样本null不能校准完整1049万位置图。

样本支持筛选为D至少25命中/8 contexts、配对共同命中至少5；完整缓存支持为D至少100命中/10块、共同命中至少10。每次真实/null重跑，都将正且可估的phi与互选q10送入加权贪心模块度分组。Donor频率箱使用完整活跃feature的平均log10(Dp)，D零频率feature采用p_floor1e-12；TRAIN/EVAL分别仅3/9个门控事件的Dp=0。该规则和固定切点在条件间共用，未在看到结果后改变。

学习中，令a_i(t)表示固定feature i在EVAL位置t命中。一个feature的条件损失是其n_i命中位置的平均CE。主损失在提前按计数确定有支持的M个低频feature上，再平均这些均值。各seed的R−F/R−N差使用相同位置与feature。

配对区间把每4个连续context合为一个块，共128块。对逐位置配对差Δ_t和逐feature差μ_i，固定feature的比率线性化块影响为：

\[
u_b=\frac{1}{M}\sum_i\frac{\sum_{t\in b}a_i(t)\Delta_t-n_{ib}\mu_i}{n_i},
\qquad \sum_bu_b=0.
\]

其中n_ib是feature i在块b中的命中数。抽取2000次多项式块权重w，计算d*=d+Σ_b w_bu_b，分位数给出近似条件配对区间。它保留条件集合的重叠与块内配对；不是精确重算比率的bootstrap，不证明文档独立、总体泛化，也不包含seed不确定性。三个配对seed分别展示。

R相对F/N的实用改善阈值为0.01 nat/feature，总体非劣容差为0.01 nat/token；方向须在三个seed一致。每个条件也与原始零适配器基线比较。一个条件损害更小，不等于绝对学习收益。低频条件不必然更难；必须报告其实际基线。

局部干预每arm/seed使用16个固定donor/probe批次。每个频率箱与专家的token数完全保持；预检最小交换比例为0.640625。共同固定中点为3060、SGD lr为0.1，在效果比较前按数值资格选择。每个512位置probe仅平均全局有支持、且在该probe出现的低频feature；各批probe支持不同，但配对更新间相同。批次bootstrap描述这些固定donor/probe的变化，不表示独立文档或seed不确定性。原始/等范数版本都须展示绝对改善及actual−exchange差。

## 5. 证据来源

| 主张 | 原始记录 | 计算 | 边界 |
| --- | --- | --- | --- |
| 完整组频率比较 | `structure/full_repair_summary.json`、`full_group_controls.csv` | 全部186/186组、13807/13807成员；同size/D均值 | 已暴露窗口内，看过结果后的补充 |
| 组稳定性依赖权重与图 | `structure/recheck_summary.json`、`q10_q20_member_stability.csv` | 按组/成员/配对加权 | 不能推断稳健天然专家分区 |
| 样本组织超出边际背景 | `structure/triple_counting_repair/null_results.json`及99 draw表 | 样本完整流程重跑 | 有限链近似、仅校准该样本 |
| 学习比较 | 各run评估数组/JSON及analysis CSV | 配对seed和同一有支持feature集合 | 固定末端分配/预算，不声称稀有知识掌握 |
| 局部更新后果 | `intervention/seed_*/*/effects.csv`、`norms.csv` | 同状态/数据、精确token数与范数控制 | 训练后特化与有限局部一步分别解释 |
| 首方向敏感性 | `data/first_direction/summary.json`、固定边/features | 同原始v/留作测量contexts，no-op已验证 | 不赋予common语义，无随机方向对照 |
| 中心化竞争解释 | `data/first_direction/centering_control/` | 同v/H，在冻结标准化前保原均值 | 事后操作分解，不是训练机制 |

## 6. 实际结果账本与交付

| 环节 | 已完成证据 | 结果与资格 |
| --- | --- | --- |
| 完整匹配对照 | 186/186组、13807/13807成员 | 严格完整T_b组等权−0.25147064dex/成员加权−0.15500075dex；看过结果后的窗口内补充 |
| 样本全流程null | 99/99 draw，两链分配50/49，完整修复对照 | T_a0.195311，对照均值0.039274、范围0.033353–0.059838；平滑T_b−0.067770，对照均值+0.015066；近似p各0.01/Holm0.02，无名义FWER保证；保留严格样本T_b NA |
| 局部关系/分区 | 相同旧计数/图 | D边86.60%保留，边Jaccard0.764；完整成员加权社区Jaccard0.322；q10→q20 pair保留0.383 |
| 正式学习 | 9/9完成，54保存状态/9final | 低频R/F/N均值3.358713/3.342884/3.352730，零参考2.439615；总体3.864719/3.866344/3.872289，零参考2.949104；固定合同下H2未支持 |
| 局部干预 | 9/9 runs，每个16批，原始/等范数 | 9个actual−exchange低频损失下降均值都为负；R等范数−0.019405/−0.013705/−0.008306；部分区间跨零；仅为有限的同条件SGD |
| 专家现象 | 36专家单元×3指标 | 全部单元损害，单专家贡献不超过29%；主指标权重贡献和与完整损害一致 |
| 原始首方向删除 | 8186拟合/8182测量位置 | L0249.527→512.147，事件Jaccard0.394；仅为敏感性 |
| 保均值控制 | 相同固定原始v/H；原输出完全复现 | L0232.604，原事件Jaccard0.819；方向投影L0变化−16.923，加固定偏移+279.543；全部层重构仍恶化 |
| 响应组成控制 | 9/9 final状态，zero/full数组完全一致 | R总体full/constant-only/TRAIN-centered-only损害0.915616/0.175456/0.858384，交互−0.118224；F/N同模式。反驳该TRAIN常量响应主导解释，保留EVAL偏移及其他训练竞争解释 |

完整缓存匹配、样本校准与H2低频集合是不同总体。特别是样本支持25/4096不校准最稀有feature尾部；不能将其p值移植到完整图或全部H2低频feature。成员加权null本身有弱负离散差（均值−0.010646），弱于实际−0.060562；因此它确实解释了部分频率组织。

响应控制在看过结果后进行。适配器为线性，因此常量U_eD_eμ_e既是TRAIN平均响应，也是adapter(TRAIN平均hidden)。TRAIN中心化响应在EVAL仍可有非零均值。Loss不具可加性，已明确报告交互。CrossCoder参考均值投影与适配器响应分解干预不同对象，不能称同一个common机制。

本轮检验三座桥：联合输入组织、有界学习分配、局部更新后果。观察支持有界的额外组织，缩小天然硬分区主张，不支持登记的关系路由学习优势。局部干预在该中点反驳其预期优势，不识别Adam轨迹成因。唯一下一项AI建议读出是在适配器未使用的contexts上，固定feature清单与共同计数支持集合，检查损害是否随出处变化；它不识别出处因果，也不授予新实验执行权限。

不从计划端点推断结果。检查点留在execution；`checkpoint_manifest.json`列54个实际正式保存及重核hash身份。登记family为 `checkpoint_family_crosscoder_relation_learning_20261015t164000z`；已保存smoke为 `checkpoint_crosscoder_relation_learning_smoke_20261015t164000z`。缓存版本为 `representation_crosscoder_relation_learning_20261015t164000z`及 `_eval512_`版本。[本次保存状态访问检查](../../../assets/checks/2026-10-15_crosscoder_relation_learning_saved_states.json)已通过。图与小CSV在报告目录携带来源manifest。讨论包不含原始contexts、完整缓存、矩阵和权重；可复现入口保留其地址。

原结果文件和此前讨论包均保留。未修改skills或无关已有改动，未commit/push、外发消息、改变Focus或科学状态。
