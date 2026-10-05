# 完整记录：FIT交叉拟合的路由预测收缩诊断

2026-10-04。[English](router_shrinkage_detailed.md) · [Summary](router_shrinkage_summary_cn.md)。科学设计：[Anchor](anchor_cn.md)。冻结合同：[Protocol的16:20 UTC事后诊断补充](protocol_cn.md)。执行完成；`ELIGIBLE`仅指符合该事后诊断合同，不能作为独立确认。研究者科学结论与下一决定均为`Unknown`。

## 0. 结果速读

本轮检验：只在FIT内部选择输入相关预测的使用幅度，是否能降低原选择器损失，并保留超过固定共同动作的收益。3模型×2输入族×2选择来源共12次α选择，11次选0，只有SALL/base/A选0.1。选定规则的24个总体条件都优于原α1，条件区间均为正；其中22个已精确退回共同动作，另外2个相对共同动作的收益点估计也为负。减少原策略损失成立；本轮没有兑现总体上超过共同动作的自适应收益。

完整执行包含24次训练折ridge求解、300行OOF统计、60套完整最终选择、600行全部候选DEV读出，以及120行选定α的总体／分域结果。没有新语言模型或SAE前向、GPU任务、TEST访问或神经网络训练。[运行收据](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/receipt.json)

## 1. 对象与单位

| 对象 | 本轮具体含义 | 边界 |
|---|---|---|
| 精确33B | Dense、fresh S7、SALL累计训练330亿token的已有检查点 | 不是330亿参数，不是架构因果配对 |
| 事件／记录 | 一条257-token记录中的16个预测位置；每条记录是重采样单位 | 位置不能算独立重复 |
| A/B库 | 两批来源各产生四个领域动作及一个共同动作，均已有真实有限CE测量 | 同名跨库动作由不同来源梯度产生 |
| base389 | 当前／前一token哈希、可见前缀频率、位置与平方、c/a/x的log范数 | 不加入类别标签 |
| fullcx3461 | base加完整投影输入c:2048和残差状态x=r+a:1024 | 特定线性拟合器，不等于信息充分性检验 |
| α | 输入相关预测偏离动作均值的使用幅度 | 只取预定五值，不是新训练步长 |
| OOF | 每条FIT记录只用未见该记录的训练折模型给出预测 | 选优后的OOF最小值仍有选择偏差 |

有限ΔCE是动作后CE减去原CE；负值有利。收益是对照CE减去策略CE；正值有利。表中差异使用微nat/事件，绝对CE使用nat。共同动作先平均原始领域梯度，再独立归一化，并非领域动作损失的平均。

## 2. 与原问题的关系

原问题关注有限资源下的共享／私有学习及保持。本轮只调整固定动作库上的选择器，不改变动作、模型状态或专家学习历史。它区分“当前输入相关规则是否值得用”与“能否通过退回更强固定动作减少损失”。它不能替代共同／私有训练轨迹，失败也不能否决训练分配未来创造专家差异。

## 3. 合同、授权与偏差

研究者15:53:50 UTC的新指令已授权两小时研究并说明无需再次审批。具体交叉拟合配方是该授权范围内的AI选择，不冒充研究者逐项科学确认。Protocol补充时间为16:20 UTC；注册于16:33:23.597671 UTC，先于新拟合。原DEV及切换审计在配方提出前已可见，**这从一开始就是事后诊断**。

| 登记项目 | 实际执行 | 适用边界 |
|---|---|---|
| 原3模型、2族、fixed_five | 全部保留，无PCA／SAE族、无拒绝动作 | 不推广到六动作或其他拟合器 |
| FIT四折、记录不拆、折内标准化 | 24折求解完成；每折384训练、128验证记录 | 文章／近重复依赖仍未知 |
| α五值，精确最小与小α并列规则 | 12次选择完成；同一α用于同／跨库 | 没有DEV重新选α |
| 全部最终选择先冻结 | 16:34:33.646059 UTC完成freeze，再评分DEV | 这是新计算顺序，不消除此前DEV曝光 |
| 原2000次记录bootstrap | 原数组重用，不重拟合／重选α | 不覆盖拟合与选择变动；无多重校正 |
| CPU最多8线程、1800秒 | 工作进程70.58秒完成，未触发时限 | 不报告为LM训练吞吐 |

没有实际运行重试、遗漏条件或事后删去族。源码开发和合成检查均在注册前完成；没有用调试结果替代正式读出。适用范围与登记一致；独立确认资格不存在，不能通过执行成功补足。

## 4. 实际算法与数据

沿用原面板：8类别、4领域；FIT512记录，每类64；DEV1024记录，每类128；每记录位置14、30、…、254共16个事件。原A/B动作来源各256记录。精确token串与记录身份分离已核；文章、近重复及预训练重叠仍为`Unknown`。原模型、方向、有限效应和数据身份由[原Detailed](probe_33b_detailed_cn.md)与[配置](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/configs/probe_33b.json)持有；本轮没有重新加载检查点。

分折使用NumPy Generator(seed=1004)。依类别字典序，各类先按record_id排序，再由同一生成器依次打乱，循环分到0—3折。每折每类16记录，每个位置跟随其整条记录。base及fullcx直接从原始因果特征重建；x先按缓存激活dtype计算r+a，再转为float64。各折只用训练折重算特征均值、总体标准差（精确零替换为1）及标签截距；不复用all-FIT标准化矩阵。

拟合复用原ridge：最小化残差平方和加10倍系数平方和，截距不惩罚；A/B各五列共十个输出一起求解，但没有跨输出耦合惩罚。每次训练折有6144事件，验证折有2048事件。记录保存所有折的均值、标准差、截距、系数和OOF预测。

对某个动作，先定义训练折真实有限ΔCE均值μ，以及该折模型对当前输入的预测q。使用分数μ+α(q−μ)选择动作。α1直接使用原q的数值，避免减加相消改变端点；α0使用均值。每个模型／输入族／选择bank单独比较五个α的完整OOF实际ΔCE均值；精确并列取较小α。类别只用于分折／bootstrap，不作为新增输入。

最后把选定α用于原all-FIT冻结预测和all-FIT动作均值；全部60套最终choice数组在读DEV前落盘。α1必须逐事件严格还原原selector，α0必须逐事件等于FIT-fixed common。同一选择在A→A、A→B或B→B、B→A之间只改变评价动作库，不重新选择α。[注册配方与输入hash](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/registration.json)

## 5. 读数和不确定性

主读数是选定α相对原α1及固定α0的配对真实有限CE收益。全部5个α×3模型×2族×2选择bank×2评价bank×5范围产生600行；固定选择后的12×2×5产生120行，其中24行是总体，其余96行是四领域。保留全部候选，并不从DEV另挑最优α或输入族。

直接使用原2000次类别分层、整记录配对bootstrap计数。每次保留记录内全部16位置；模型、FIT拟合、折划分和α选择固定，bootstrap中不重拟合。条件95%区间不包含来源抽样、文章依赖、拟合／选择变动或多重比较校正。24总体条件不是24次独立确认。

切换率是策略偏离common的事件比例。总体额外代价精确等于切换率乘以切换处的平均额外代价；不切换时贡献为0，条件代价记为缺失而不是0。切换条件读数只报点估计，没有虚构比率区间。实际效用门槛未设，研究者科学判断仍为`Unknown`。

## 6. 证据谱系

| 可核实陈述 | 原件与计算 | 结果 | 最大可支持范围 |
|---|---|---|---|
| α只由FIT折外成本选择 | fold_assignment、6份OOF、300行cv_table→精确argmin→selection_freeze | 11个0、1个0.1 | 登记配方的选择结果；非无偏效用估计 |
| 两端含义正确 | 原all-FIT预测／choice与新freeze逐事件比较 | α1完全还原；α0恒为common | 实现身份，不是新机制支持 |
| 减少原策略损失 | 原effects+冻结choice→配对记录均值及原bootstrap | 24总体收益全正且相应区间为正 | 已曝光DEV上的条件结果 |
| 未兑现总体adaptive-over-fixed收益 | 同一读数相对α0 | 22个精确0；另2个负点估计 | 不证明所有潜在路由信息不存在 |
| 作者复算 | 另写特征与正规方程／OOF／point读数代码 | 24折与600点估计通过 | 作者自检，不冒充独立审阅人 |

[完整输出manifest](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/receipt.json)与[作者审计](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/second_window_20261004/crossfit_author_audit.json)保留链路。原bootstrap区间由正式脚本计算；作者审计没有另算全部区间。

## 7. 结果

### 7.1 全部12次α选择

| 模型 | 输入族 | A选α | B选α |
|---|---|---:|---:|
| Dense | base | 0 | 0 |
| Dense | fullcx | 0 | 0 |
| fresh S7 | base | 0 | 0 |
| fresh S7 | fullcx | 0 | 0 |
| SALL | base | 0.1 | 0 |
| SALL | fullcx | 0 | 0 |

SALL/base/A的OOFα0.1相对OOFα0收益为+16.14微nat；这是用来选优的均值，不能当作独立的成功验证。全部12组OOF未收缩的α1均不如各自α0；这些折模型不是原全FIT模型。完整五值及各折读数留在[300行CV表](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/cv_table.csv)，没有只展示胜者。

### 7.2 选定规则的总体读出

24个总体条件相对原α1的收益为+265.74至+707.13微nat，全部相应条件区间为正。22个条件是α0，其相对固定common的收益及区间精确为0，因为两者动作完全相同。这种0不是统计等效性检验。

唯一非零α规则的两个总体读数如下，单位微nat。区间为前述条件95%区间。

| SALL/base/A | 相对原α1收益 [区间] | 相对固定common收益 [区间] | 切换率 |
|---|---:|---:|---:|
| A→A | +283.38 [186.37, 380.23] | −6.23 [−20.88, +9.06] | 2.5269% |
| A→B | +386.35 [297.29, 482.37] | −19.72 [−35.49, −3.45] | 2.5269% |

其绝对CE分别为3.4970349093与3.4969877835。切换处额外代价为246.44与780.48微nat；与2.5269%相乘得到6.23与19.72微nat总体额外代价。跨库时相同切换率来自同一个选择数组，不是两次独立估计。

分域仍全部保留。非零α规则A→A的数学和生物域点估计可以为正，但其相对common区间均跨零；A→B的四域点估计均负，其中计算机科学区间为负。不能把总体结果写成所有域都严格受损，也不能挑正点估计作新策略。[120行选定结果](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/evaluation_selected_alpha.csv)与[600行全部候选结果](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/evaluation_all_alpha.csv)

## 8. 分阶段核验与未解决解释

合成检查通过端点、整记录均衡、记录重复拒绝、验证标签不影响训练折拟合、验证特征不影响训练折标准化、小α精确并列及切换集合嵌套。实际raw FIT特征经原all-FIT ridge重建原预测，最大差6.25×10⁻¹⁷；实际最终两端choice严格一致。原α1读数的均值与区间还原最大差8.67×10⁻¹⁹。switch恒等式最大残差1.08×10⁻¹⁹。

作者另写计算路径，没有导入生产分析helper。24个保存系数的训练折正规方程最大相对残差4.40×10⁻¹⁵；OOF预测重建最大差1.34×10⁻¹⁶；训练折均值、标准差、截距精确一致，训练与验证记录交集为0。这验证保存拟合符合训练折目标，不证明文章／预训练数据独立。

没有观察到实现失败或缺失条件；但不能把拟合正确当作模型假设正确。有限样本估计／选择误差、函数类偏差、FIT/DEV组成差异及不可预测目标仍是相容解释。λ固定为10时，384记录训练折相对512记录all-FIT的正则强度和估计难度也不同，本轮不单独隔离这个变化。

## 9. 本轮完整记录

2026-10-04：问题是FIT内部的幅度选择能否改善原规则且超过common。设置固定3检查点、2原始特征族、5动作、λ10和原有限效应；训练／选择只用FIT512，评价仍用已曝光DEV1024，TEST未打开。注册后完成24折，16:34:33冻结全部最终选择，16:34:54完成全读出，工作进程耗时70.58秒。直接结果为11个α0、1个α0.1，24总体相对原规则改善而未超过common。认识更新限于当前拟合器与固定库；原始负结果保留，研究者下一决定`Unknown`。

## 10. 解释、边界与下一决定

**AI解读：**收缩在本轮主要通过取消当前输入相关切换来减少损失。OOF选择多数在读DEV前就回到固定动作，说明FIT样本内优势没有在当前记录划分中形成稳健选择依据。这不是“自适应路由已经修好”，也不识别唯一失败原因。

可主张该配方在此面板减少原选择器损失。不可主张自适应总体上超过强固定动作、完整输入信息不足、所有router无用、SAE机制、MoE架构因果优势、长期学习或保持改善。研究者科学结论与下一决定保持`Unknown`；剩余问题是当前可见信息、估计器和训练分配之间的未证实联系。本记录不关闭问题或新增运行。

## 11. 原件清单与复现入口

下表hash为12字符前缀；完整SHA-256在注册及收据中。所有计算原件留在执行目录，不复制大数组到研究仓库。

| 原件 | 作用／生产者 | 身份与完成情况 |
|---|---|---|
| [registration.json](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/registration.json) | 配方、代码／helper／原输入身份；新拟合前登记 | `e4fd6ee22698`，完成 |
| [冻结脚本](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/scripts/crossfit_router_shrinkage_20261004.py) | 复用原raw-feature/ridge；新增四折与收缩 | `a25dc736e56b` |
| [fold_assignment.npz](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/fold_assignment.npz)及同名CSV | 512整记录、8192事件的分折 | `794aefaec08d`，完成 |
| [输出目录](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004)内6份OOF文件 | 每模型／族的预测、系数、缩放、标签截距与候选choice | 全部完成，逐文件hash见receipt |
| [cv_table.csv](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/cv_table.csv) | 300行各fold／pooled实际成本 | `4ecdf8e20c26` |
| [selection_freeze.json](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/selection_freeze.json)及同名NPZ | 12次选α、60套最终选择，先于DEV评分 | `4238e426921f` |
| [evaluation_all_alpha.csv](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/evaluation_all_alpha.csv) | 所有候选600行及switch点分解 | `c8c4ed249449` |
| [evaluation_selected_alpha.csv](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/evaluation_selected_alpha.csv) | 预先选定α的120行 | `023b8455d7ed` |
| [receipt.json](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/runs/router_shrinkage_20261004/receipt.json) | 完成、耗时、检查、完整输出hash | `791492c453f0` |
| [作者审计](/data/250010109/MoE_Router/experiments/20261003_sharing_routing/notes/second_window_20261004/crossfit_author_audit.md) | 另写路径复算；披露作者身份 | 完成，不等于独立审阅人 |

复现入口为上述脚本的`--register`和`--run`；既有完成结果会先核身份后返回，不重复拟合。日志位于执行目录`receipts/second_window_20261004/`，不作为模型训练日志。没有GPU job ID、神经网络checkpoint或新图；本次判断由完整数表和原件链路支持。
