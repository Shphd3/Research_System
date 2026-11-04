# Protocol 中文：A15_27_05_01 / Dense checkpoint 动态 / 2026-11-01

## 0. Approval Snapshot

状态：APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FORMAL_READ_ONLY_ANALYSIS。授权来自本对话2026年11月1日明确要求先写设计、再审计、smoke及完成正式分析。A–G在用户指定范围内确认；操作选择按本文件和config冻结，审计检查跨块一致性。研究者科学接受与闭合为Unknown。不训练语言模型/字典，不修改原训练，不新建对话，不commit/push或外部发布。

目的：区分规模、谱形状、方向、文本关系和标签可读性的时间曲线。归属[Anchor](../../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/subanchors/15_27_05_01_checkpoint_spectral_dynamics_anchor_cn.md)和既有[Focus](../../../../../focus/focus_spectral_semantic_granularity_cn.md)。主证据为相邻谱/投影距离、每十亿实际训练token变化率与抽样参照。33B只是末端；没有有依据的通用稳定容差，因此不估计趋稳起点。

## 1. Terminology / Definitions

B为十亿累计有效预测token；checkpoint是保存权重及内部训练计数的状态。观测单位是一个固定位置向量；重采样单位是文档记录，N8缺少论文身份。谱带为各点自身按特征值排序的索引，不代表固定语义。residual-post是block中Attention和MLP两次残差相加之后、final norm之前。

## 2. Anchor Alignment

A分别看规模和分配，B看原始方向，C看文本关系和线性分类。竞争解释为坐标旋转和有限抽样。允许时间不同、继续变化或无法估计，不推出因果语义、停止学习、最终收敛或路由效益。先完成几何，再读出。

## 3. Tested Hypothesis

不预设头先中尾后的正向顺序。看连续相邻区间是否减小、是否进入抽样量级、是否反弹。顺序缺失将削弱动力学解释，但不判定其他未完成训练的效益。

## 4. Rival Explanations

纯旋转可保持谱和样本关系；缩放可保持归一化谱及CKA；近简并可使估计基任意旋转；词汇、来源和小标签集可产生类别关联。必须同时展示原始距离、真实token间隔及变化率。

## 5. Data Construction And Provenance

[config.json](config.json)和[manifest.json](manifest.json)在前向前冻结。分词器为本地Qwen3-0.6B-Base，完整文件摘要3b602daf74810b313b8e1eca542d50b639a4e3f9de9b7185a309e09289306eda，与Qwen权重分开。

几何使用ntp_statistics_panel_2048既有2048条文本，每条固定256token，fit/test各1024，八学科平衡。位置为零基7、15、…、255，每条32个；每集32768向量，文档等权。所有点输入、全一mask、位置、上下文和顺序相同。记录家族、全文和token序列不得跨集完全重复。均值/PCA/对齐只用fit。CKA在test自身中心化只用于统计，不用于学习变换。历史暴露与论文级独立性缺口保留为描述性边界。

语义桥接复用R12的96条the文本、token279位置、192token前缀、外部可见前缀标签和文档家族划分。原fitted_document_ids.csv每项任务16TRAIN/8DEV，留出集原样使用，应用保存的H标签审查。任务为数学/生物、数学内代数/分析、生物内细胞/生态演化。不以Dense响应选标签。小面板不拟合大谱。Qwen激活父模型不匹配，排除；不使用CrossCoder。

## 6. Learning Task And Permitted Supervision

统计拟合包括均值、PCA和正交Procrustes。监督拟合仅为TRAIN标签的二元线性logistic，DEV选C，各checkpoint独立重拟合自身基和固定33B基。测量线性关联，不测原生使用。不得用末端固定分类器迁移替代重拟合。

## 7. Model / Architecture And Frozen Variants

原生Dense为8block、隐藏1024、MLP3072、16query头/8KV头、head128、词表151936、输入输出共享、281431040参数、SAE none。严格加载原dense_sae代码。主张量final_raw_h对应blocks[7] residual-post、model.norm之前。0.5/17/33B额外取blocks[0]/[3]输出。原生最后block手动展开，故用norm前hook核对主张量；不能假设blocks[7]输出hook被触发。pre_mlp_input属于另一测点。

参数冻结、eval/inference_mode、FP32前向、关闭TF32、math SDPA、dropout0；协方差/特征分解/对齐用FP64；不白化或归一化激活。

## 8. Training Objective And Optimization

语言模型训练不适用，更新0次。对X_t^TX_33做SVD得到R=UV^T；允许反射、旋转，不学习尺度。各点用自己的参考均值，评估也用对应参考均值。

分类器TRAIN内逐坐标标准化、类别平衡、L2 logistic，C为0.01/0.1/1/10，max_iter3000、tol1e−8，DEV平衡准确率选参，平局选最小C。三点同划分、同容量和流程；收敛失败显式记录，不放宽容差。

## 9. Conditions, Seeds, And Checkpoints

所有可读12点：0.5、1、3、5、10、15、17、19、21、22.018691584、31、33B。缺失权重和窗口外状态单列，19B读摘要匹配的续训归档，不插值。早/中/晚预定0.5/17/33B用于smoke、语义和层位补充。seed1101。状态内token/step/config须与manifest一致；严格加载和架构匹配是硬门。用原start-pointer和spec连接10B及22.018691584B续训。

## 10. Primary Metric And Frozen Analysis Plan

各点用自己的参考均值中心化，C=X^TX/(N−1)，N32768；分别存奇异值s和特征值lambda=s²/(N−1)、绝对谱、trace、归一化谱p、累计方差、50/80/90/95/99%所需维数、effective rank=exp(−sum p log p)、以lambda_max×1e−10判定的数值秩、均值范数和漂移。

绝对谱距离为||lambda_a−lambda_b||_2；对称相对绝对谱距离为前者除以sqrt(||lambda_a||||lambda_b||)；归一化谱距离为0.5||p_a−p_b||_1。相邻与距33B均报告，变化率除以实际token差/1e9，同时保留原距离。距末端变小不能证明稳定。

子空间为前16/64/128/256维及头1–64、中481–544、尾961–1024。保存所有主夹角、RMS/最大角和归一化投影距离sqrt(max(0,1−||U^TV||²_F/k))。对齐后基为R^TV_t，与原始结果并排。固定V_33中的diag(V_33^TC_tV_33)另称投影方差。报告谱带边界间隙。仅两点左右相邻相对eigengap均≥0.05才给符号不变的逐向量余弦；否则UNIDENTIFIABLE。近简并边界保留抽样敏感性，不追语义向量。

## 11. Secondary Metrics And Guards

独立test完全配对。CKA各自中心化，用交叉矩||X^TY||²_F/(||X^TX||_F||Y^TY||_F)实现，不存大样本Gram。原始/对齐残差为||X−Y||_F/||Y||_F，按各点参考均值；均值漂移另列。Procrustes仅fit拟合，报告正交误差及train/test残差。相邻和末端CKA均存。

0.5/17/33B及最多一个转折点各做8次确定性512/512参考文档拆分，同一位置和跨点配对。转折规则为连续归一化谱变化率对数差绝对值最大处的右端点，平局最早。存每点内拆分的谱、子空间和均值差，给2.5/50/97.5%经验范围，明确是敏感性，不是校准的总体置信区间。早/中/晚距末端另用相同半集配对比较。以抽样参照0.5/1/2倍作描述性敏感性，不报告认证的趋稳起点。

读出为64维头/中/尾，128维head128、head+middle、head+tail，1024维full；自身基与固定末端基分别做。平衡准确率为两类召回均值。留出按类别分层配对重采样2000次，记录C/拟合账本。主增量为head+middle−head128和head+tail−head128，另报对head增量以区分普通扩维收益；3点×2基×3任务×2增量共36个对比Holm校正。区间宽保持不足；仅三时间点不定义分类起点。原来源/格式匹配不足不消失。

## 12. Known Good / Known Bad / Known Confusing Cases

恒等应距0、CKA1；纯旋转应谱不变、原始主方向可变、CKA1、对齐残差近0；正缩放保持归一化谱/CKA但改变trace和残差；打乱配对降低关系指标而自身谱不变。全1024维距离天然0，排除为证据。FP64恒等误差<1e−8；FP32hook相等或相对1e−6以内；协方差有限、基正交、分解及trace相对误差<1e−8。关键失败停止放大。

## 13. Scientific Procedure And Stage Contracts

顺序：清单与当前strict access→输入固定→科学/数据/数值三轮审计→三点各8记录smoke及缓存恢复核验→12点主几何与三点层位补充→同划分语义读出→四图与证据交付。每阶段保存输入、输出、通过/失败及交接。身份失败阻断该点；schema/跨集泄漏失败阻断几何；标签不足只阻断依赖任务；已有缓存保留。完整英文Protocol的阶段表为相同规则的审计展开。

## 14. Algorithm, Output, And Provenance Contract

执行根为/data/250010109/MoE_Router/experiments/20261101_dense_checkpoint_spectral_dynamics；prepare/collect/analyze和数值校准代码归该处，研究目录保存精确小代码副本。前向前保存科学正文、config、manifest与代码摘要。缓存键包含checkpoint权重/manifest摘要、面板字节、位置、层、精度、预处理和collector代码；原子写入且核验payload摘要，partial无效。逐checkpoint加载，完成后释放模型权重和CUDA缓存。

输入ID包括原Dense33B、A24 Dense1/5/15/31B、N8面板、tokenizer、R11A02数据、R12分析，以及新登记的12状态家族。使用前做当前strict检查。资产与代码/原数据父身份和hook明确。

研究者明确选择最多两张5090、与其他分析共享两卡上限。使用执行envelope的5090-2-spot、shphd-lite-0911及已验证SM120运行层，不fallback。分配前检查本人活动分析；一个分配覆盖smoke及formal，单进程同时至多用一张卡，第二张属于同一两卡资源组。运行上限6小时，新缓存上限20GiB；达到就保存并停止，不放宽分析。原训练不动。用仓库提交模板先dry-run；旧CLI workspace schema仅用局部兼容代理修复。日志、提交及终止收据落盘。

交付清单、配置、代码、全部谱/均值/基、距离/主夹角/末端投影/抽样/读出/预测/对比、拟合与覆盖账本、四图、缓存索引、中英Summary/Detailed、实际输出资产登记及本地Anchor阅读同步。横轴真实训练B，标注缺失区间、数值误差和抽样波动。

## 15. Success / Failure / Insufficient Evidence

工程完成指所有适用项均完成或显式记录失败/缺失。各科学问题独立：下降且超出不确定性可支持该量在区间内趋稳；明确相反模式削弱顺序；宽区间、弱标签、无法分辨方向属于不足。不用合并正向结论，不强造时间，不插值观测。

## 16. What This Cannot Claim

不声称最终收敛、语义掌握、因果使用、没有学习、路由分阶段最优或其他未完成训练的效益。相同tokenizer不等于相同模型；Qwen/CrossCoder不是Dense证据；8次拆分不是8模型。分类可用与几何稳定可以不同步。

## 17. Block Confirmation, Freeze, And Amendment Ledger

2026-11-01研究者已给A–G范围及实现/smoke/formal授权；确定性操作规则在此登记。写入时DRAFT_NOT_EXECUTABLE，范围内审计后一致性通过即按既有授权执行，不重复请求。稳定容差Unknown，按用户允许不估起点。首次前向前将初始正文/config/manifest/代码摘要写freeze.json。之后正文不可覆盖；实质更改追加时间、前后值、原因、已见结果、授权和资格影响。结果进入Summary/Detailed。


### 修订 A01：只允许正定向旋转

2026-11-01。原第8节允许正交反射；现增加det(R)=+1，与R^TR=I同时约束。仍在相同参考集交叉矩上SVD，R=U diag(1,…,det(UV^T)) V^T，不学习缩放。本修正落实研究者“只允许旋转”的明确要求。此时已见全部原始缓存、谱和部分配对指标；没有按语义结果选此修正。仅重算受影响对齐指标并重新生成派生表图；旧负行列式对齐结果保留为被替代的非最终证据。输入、原始方向、CKA、划分、读出及判定规则保持冻结。只用缓存CPU重算，不新增前向或GPU分配。初始字节及摘要保留在audit/frozen_sources，修订与核验分别见audit/amendment_A01.json和audit/rotation_only_correction.json。


### 清单澄清 A02：不假定名义checkpoint网格

初版清单将7/9/11B列作未测量名义点，但原训练合约没有要求该网格。移除这些例子，只将有原状态manifest但权重不可用的8个状态计为缺失。12个实测checkpoint行、输入、位置、划分、指标和选参均不变。初版manifest字节保留，见audit/amendment_A02.json。


### 工程修订 A03：统计缓存身份

登记入口run.sh在复用统计NPZ前，核对checkpoint权重/manifest、表征缓存键、精确面板/位置、层位/预处理、配置与统计代码的指纹，并核验完成数组摘要。当前本轮新生成且已独立核验的结果只做一次显式绑定；身份改变或没有合格来源的缓存拒绝复用。无统计/数据/选参更改，无新增前向或重拟合。见audit/amendment_A03.json及执行侧analysis/cache_context.json。
