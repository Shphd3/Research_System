# 执行修订与冻结记录

本记录追加修订，不覆盖旧结果或初始 Protocol。所有时间为 UTC；北京时间加8小时。

## R1.1 · 2026-10-15T16:43Z · 学习前评分修复

原 mean-binary score 在 D-only 路由检查中使 F 的99.896%位置并列，151/186组从不胜出。尚无任何学习损失。三种条件统一改为 hit-only D-standardized score，D-only拟合和相同mapping算法不变。修复后 R/F/N tie为0.1007%/0/0，D四专家负载均约25%。原版保存在 execution data/meanbinary_initial。胜出组平均大小仍不同，必须报告；负载相近不证明输入组成相同。

## R1.2 · 2026-10-15T16:47Z · 条件均匀采样计算修复

单槽 heat-bath 的22个二/三成员组慢混合，未放宽资格。对同一个 D-only 条件均匀目标，size2改精确IID合法无序pair采样：按排序第一成员枚举合法第二成员区间，把每个pair唯一对应一个整数，均匀抽整数。size3独立均匀抽三个候选，拒绝重复或不满足D均值约束的提案，每组上限10,000,000提案；每个合法subset有相同3!表示。保留所有合格draw，不查看V来重抽。

size≥4仍用原两链heat-bath；full每链100draw、burn50s、spacing5s。MCMC资格为 SD和D均值 split-Rhat≤1.1、ESS≥20、每链平均原始成员Jaccard≤0.5、原始精确集合出现比例≤0.25。exactIID仅要求算法正确及所有计划draw完成，Rhat/ESS为描述，不能用其随机波动删draw。原单槽attempt完整归档。完整条件对照覆盖186/186组、13807/13807成员。它是对旧暴露结果的计算修复，依然探索性。

## R1.3 · 2026-10-15T16:50Z · 样本控制统一计算预算

sample observed 50draw/链时有一组D均值Rhat=1.103略高于1.1。正式null前，observed和所有null统一改为200draw/链、spacing10s；burn仍50s。不改变目标分布、资格阈值、候选或统计量，不按V筛组或只取有效null。旧资格attempt保留。B99计划3个CPU worker；实际null保留固定proposal时钟，两链32nnz burn、4nnz spacing。若Tb任一draw未定义，则完整Tb Monte Carlo推断缺失；已定义且资格合格的Ta可独立报告，不能用valid-only Tb生成p。

## R1.4 · 2026-10-15T16:53Z · 数据身份守卫修复

学习缓存position_id为各source文件内的绝对offset，两个不同source可能使用相同整数。原仅整数torch.isin会误报泄漏。执行前修为检查source_paths不重合及全局context ID不交；source SHA+文件内offset才定义token身份。缓存TRAIN/EVAL实际分别来自原TRAIN的file0/file1固定窗口，精确offset见manifest。此为身份检查修复，没有据loss修改数据。

## R1.5 · 2026-10-15T16:47:49Z · 资源提交

唯一作业pt-szeffn72使用已授权h100-4-reserved配额和shphd-lite-0911。检查未发现可复用的四卡运行实例；未新增额度或改变其他任务。提交只证明平台接受；本条提交时worker仍Pending，device smoke和学习均未开始。实际设备/吞吐与最终共同预算须以后续持久receipt为准。

## R1.6 · 2026-10-15T17:01Z · 区分因果性与BF16变形状敏感性

16:53:59持久设备回执确认4张完整80GB H100及BF16计算可用。首缓存资格停止：固定形状改变全部未来token时raw、z、门控事件完全不变；截断prefix、改变矩阵形状后BF16 raw有2/2/4的最大绝对差，门控事件差7/13/9，但三个位置的R/F/N路由全部一致。该FAIL及当时source完整保留，尚未抽取学习缓存、查看学习loss。

不能把跨矩阵形状的bitwise一致性当成因果性的必要条件，也不能把这份FAIL隐去。主因果门要求固定形状改变未来时raw/z/events完全一致及截断位置的routes一致；另加FP32/固定形状置零未来的独立诊断，记录相对层误差、完整门控与路由。若同形状未来改变影响结果或测试route仍不一致，停止。BF16截断门控差异作为数值敏感性保留，不称未来泄漏。

原模型logit复现也保持相同矩阵形状，再抽32位置比较，避免把LM head不同GEMM形状的舍入当模型差异。适配器zero输出仍要求相同缓存head计算下严格一致。正式计算继续使用原BF16策略和固定门控，不按诊断改阈值或主模型精度。

## R1.7 · 2026-10-15T17:02Z · 实测吞吐后共同训练预算

缓存TRAIN130712、初版EVAL65402位置。native fullmodel与缓存head的32位置logit和CE误差均严格0。固定形状future变化BF16/FP32均严格不变；FP32截断raw最大误差9.16e-5至1.53e-4、门控事件差0；不隐藏BF16变形状敏感性。12步数值smoke通过，zero适配器、序列化下一步weights+Adam replay及token TensorBoard守卫通过；外部进程恢复尚未资格，明确NOT_QUALIFIED。

smoke实测训练update中位0.00572秒、batch256；初步3epoch并非最终冻结预算。尚无正式条件比较结果，依据吞吐统一冻结12个drop-last epochs，每epoch510updates、总6120updates/1566720有效target exposures，每条件三seed共9runs，总14,100,480 exposures。eval/save在0/510/1530/3060/4590/6120，原初步3epoch保留为中间节点；midpoint3060。所有条件lr、batch等不变，不能按赢家延长。虚拟SGD步长0.1的相对expert参数步最大0.0103<0.05且有限，因此固定0.1，不以probe收益择步长。

主 paired bootstrap在每4个连续EVAL contexts构成的块上抽样2000次，用固定支持feature均值之比率线性化；属于近似条件区间，不是document独立置信区间，不替代3seed差异。原初步配置及预算回执保留于config/formal.json、budget_frozen.json。

## R1.8 · 2026-10-15T17:05Z · 唯一一次低频支持计数修复

正式训练尚未启动，未查看条件比较损失。计数审计发现原64个EVAL contexts中，固定low3916仅1300达到≥20hits（33.197%），307个无命中。一次扩EVAL至同一source/file1固定起点的512contexts，原64contexts/cache保持不可变，新根data_eval512；TRAIN硬链原文件，低/高频集合、支持门槛、训练budget、路由和三个seed完全不变。

扩展仅因支持计数不足，不因任何条件输赢。扩一次后接受实际覆盖并披露剩余不可估feature，不循环扩样或降支持门槛。最终配置为config/formal_R1_8.json，另登记新representation资产版本和严格检查；原资产identity不改。primary仍只解释固定low集合中有预定支持的成员，不外推未估部分。

## R1.9 · 2026-10-15T17:04Z · exact三成员采样预算缺口修复

正式null的一个size3组达到原10,000,000拒绝提案上限，Tb按原规则保留NA，Ta照常继续99draw。授权对同一个D-only条件均匀目标实现精确合法三元组计数/索引IID抽样：排序后对最小rank累计合法(j,k)数，以双指针计数，再均匀整数索引所有合法triples。穷举检查通过后，对全部已冻结observed/null groups统一重新计算小组对照，不只补NA draw，不重跑/重选矩阵或图，不改变资格阈值和效应定义。旧采样版本、NA及新全面修复版本分别保存；计算在同一reserved节点CPU进行，不能将算法修复称新机制发现。

## R1.10 · 2026-10-15T17:12Z · 首方向敏感性的单一竞争解释控制

原始首方向辅助操作已完成且保留。观察到L0由249.53增至512.15后，自我反驳发现：原始H投影后仍减原TRAIN均值μ，归一化相当于先投影中心化变化，再额外减固定偏移v(vᵀμ)/rms。方向与μ的alignment不足以判该偏移造成全部变化。

添加一个独立、明确posthoc的小控制，不重做SVD、不训练、不改主结果：同已固定v、同测量H，改为H_c=H−[(H−μ)v]vᵀ，随后仍使用原stats，使中心化变化沿该方向移除且均值保留。三条件比较原始、原始H直接移除、均值保留移除的L0/重构/门控Jaccard及共同可估旧边phi。执行前prediction已单独保存：若固定偏移主导L0倍增，保均值版本应更接近原始L0且事件Jaccard更高；否则不能据直觉编根因。该控制只区分操作的组成，不给v已证实common语义。

工程补充：reserved CPU第一次exact-control进程读入本地动态module的Numba缓存失败（ModuleNotFoundError: '<dynamic>'），日志保留。使用独立空NUMBA_CACHE_DIR重新JIT，科学源码、目标、矩阵、图和参数不变；新进程已产生真实/资格控制输出。

## R1.11 · 2026-10-15T17:35Z · 训练损害的响应分解诊断

正式9runs已完整，三种分配终点都明显劣于原零适配器。主H2结论及budget/模型不改；增加一次posthoc、无训练的有限反事实，用于区分造成当前checkpoint损害的响应组成，不寻找获胜新模型。

同一final参数、原route和完整EVAL，把每个线性专家响应写为δ_e(h)=U_eD_eμ_e+U_eD_e(h−μ_e)，μ_e只由TRAIN原route的h均值估计。完整h始终走原base残差，原完整响应和zero都严格复现已保存的C逐位置loss；另测仅常量响应及仅中心化输入相关响应。3条件×3seed都做，固定原low/high支持集合，不能改变C主指标或据控制结果重训。

执行前prediction单独保存，三种分支：常量响应主导、输入相关响应主导、二者非线性交互主导；interaction为L_full−L_constant−L_centered+L_zero，不假定loss可加。记录响应代数重构误差（relativeL2≤1e-5）及零/完整原数组bitwise复现。该控制识别固定参数下输出分量的损害贡献，不证明如何训练出它，也不把常量响应称语义common。只增补充图/表，不增加五种主图。
