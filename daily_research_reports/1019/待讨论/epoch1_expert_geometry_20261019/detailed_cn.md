# Detailed：第一轮expert几何与学习证据

主结果与必要解释见[Summary](summary_cn.md)，冻结契约见[Protocol](protocol_cn.md)。主要训练证据与SVD/PCA分析完成；附加CPU候选替换的13个模型有数值范围限制。研究者机制判断与下一决策Unknown；不修改Focus、Anchor或原第三轮实验结果。

## 1 身份、实际设置与来源

父实验：Tulu答案SFT20模型，10条件×seed11/22。数据revision为6248b175d2ccb5ec7c4aeb22e6d8ee3b21b2c752。TRAIN/DEV/EVAL为1024/128/256个规范化问题hash隔离问答，85548/10340/22446个答案及EOS目标。首user/assistant对，prompt≤256、答案含EOS8–256、总长≤512，无答案截断；问题、模板、pad不参与loss。近重复和Base预训练污染Unknown。EVAL多次查看，非新确认集。

原T/R11名单和L964保持不变，T为旧参考log频率组织、R11为人数匹配固定随机组织。新TRAIN只重新校准p、m、组均值和旁支尺度；S0原始总分、S1组均值校准、S2/S3扩展评分及具体地板沿用父协议，不在本轮重定义。Learned为可学习top1路由，LearnedLB另加原负载正则。本轮20份epoch1状态均为168步/85548监督位置；父实验epoch3为504步/256644位置，原终点记录保留。

冻结Base的28层、14选层/F16384 CrossCoder、末端norm/head。残差专家插在第28个完整block之后、末端norm之前。令h为1024维原隐藏向量，a为TRAIN均方尺度，则计算u=h/a，h_out=h+a*g*E_k(u)。固定路由g=1，学习路由g为选中softmax概率。E_k是无偏置1024→1024→1024 SwiGLU，8专家共25165824个可训练参数，学习router另8192；gate/up随机初始化，down为0。每个专家接收完整h，feature名单只选路。

本轮只读已有epoch1和同seed初始化，未创建optimizer、未训练、未重提取Base/CrossCoder。初始化来自同seed T_S0实际epoch0，已核对匹配初始化。参数/缓存输入ID和每状态路径在[evidence/input_checkpoints.json](evidence/input_checkpoints.json)及配置中。checkpoint SHA256在执行侧每模型complete.json中重新计算。

执行根：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/epoch1_expert_geometry/20261019T030056Z`。父执行根：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/sft_route_learning/20261019T012300Z`。

## 2 冻结、一致性和偏离

|契约项|实际核对|影响|
|---|---|---|
|看谱前固定资格|preflight130/160，门槛及49初步标签先于SVD|不按谱形状挑expert|
|20epoch1/两seed/10条件|20全部完成，输入168步/85548一致|主矩阵完整|
|不训练/不改路由|无新optimizer，无参数写回|原状态保留|
|W0/W1/ΔW全谱|682次实际分解，1024项奇异值，1170指标行|down增量与W1复用；初始化gate/up跨条件复用|
|rank16共同坐标|gate/up用右方向，down用左方向，响应用输出坐标|不比较任意中间神经元坐标|
|GPU自然EVAL回放|20模型前256位置NLL差均0|主收益标签数值通过|
|后处理一次工程失败|单expert模型合法无配对CSV；读取端先前假定文件存在|保留旧失败日志；修复读取空表后只重跑CPU汇总，不重跑GPU|
|附加CPU同输入替换|预先记录amendment，13模型误差≥.01，7通过|13BOUNDED；不裁定小差异、不用于49标签|

原协议英/中与配置冻结SHA见[evidence/freeze.json](evidence/freeze.json)，冻结原文件未改。[附加检查约定](amendment_probe_checks_cn.md)不改主资格、阈值或原协议。epoch1选择本身事后发生，49子集和所有模型比较均属探索分析，未作多重比较校正。

## 3 指标、对象和依赖单位

暴露资格：实际独特TRAIN预测位置≥2048、不同问答≥20、expert更新次数≥20、down有非零变化。第一轮只经过各位置一次，实际接收位置数也是独特位置数。固定路由逐位置还原；学习router只保存累计计数，按TRAIN问答容量降序累计获得保证至少需要多少不同问答的下界，不能用末态路由冒充训练历史。固定来源多样性精确可查，学习router历史来源未知。

收益资格：在暴露资格外，自然EVAL位置≥200、问答≥20；TRAIN末态自身自然区域相对零旁支ΔNLL<0；EVAL自身自然区域ΔNLL<0且1000次对话bootstrap95%区间上界<0。自然区域随模型路由定义；不同expert区域不同，不能直接把区域平均loss作专家能力排名。保留未通过、支持不足和零暴露，不将它们合并成失败原因。

SVD将实际FP32矩阵提升FP64，用CUDA gesvd求1024项奇异值和前16方向。q_j=σ_j²/Σσ_i²，stable rank=1/q1，有效秩=exp(−Σq_j logq_j)。报告完整权重、初始化与增量，不混用强度尺度；零矩阵的归一化谱/方向/有效秩为NA。ΔW是端点参数差，不能恢复中间更新轨迹。

每个expert输出PCA用同一1024位置、每EVAL问答4位置，固定抽样seed20261019；r=aE(h/a)，不含g或共同h。沿位置中心化，取前16输出主方向。Q_a、Q_b为共同坐标中的1024×16正交基，overlap=||Q_a^T Q_b||_F²/16；另存首方向绝对余弦、主角余弦、第16/17谱间隔。数值秩<16则NA，不补任意方向。16/1024仅随机几何参考，不作零假设显著性检验。

专家在同模型中共用数据和训练；专家对共享端点。专家、token、谱方向和配对不是独立实验重复。两个seed分别报告；跨seed曲线先seed内平均，再等权平均两seed，未画伪造的总体置信带。

## 4 证据链与完整结果

|结论|原始证据→计算|聚合与范围|资格/边界|
|---|---|---|---|
|130暴露充分、49有收益|preflight及outputs/*/seed*/expert_training_evidence.csv → expert_training_evidence.csv|160逐项；对话bootstrap1000次|主证据可用；收益标签探索性|
|响应主方向不同|outputs/*/seed*/probe_responses.npz和expert*.npz → within_model_similarity.csv|同1024位置、rank16；种子分开|几何可用；不识别语义功能|
|gate/up未平谱|outputs/*/seed*/spectra_and_directions.npz → paired_initial_changes.csv|每expert配对W0/W1；全部130及49子集|FP64分解核对通过|
|down仅训练后描述|spectra_and_directions.npz → matrix_summary_by_seed.csv|每模型专家均值；两个seed不作大量独立重复|初始化为0，前后比较NA|
|来源NLL有差异|父实验readouts的原GPU EVAL → epoch1_source_learning.csv|分别报告位置/问答平均和支持量|可描述来源；不是纯领域|
|候选替换不能裁定细分工|probe_responses.npz → cached_probe_NLL.npz → probe_loss_checks.json|20模型中7PASS、13BOUNDED|最大误差0.12491；不进入主收益标签|

|条件|seed|暴露充分数|充分且有留出收益的expert ID|零接收ID|
|---|---|---|---|---|
|T_S0|11|1|7|0,1,2,3,4,5,6|
|T_S0|22|1|7|0,1,2,3,4,5,6|
|T_S1|11|8|0,1,3|无|
|T_S1|22|8|1,3|无|
|T_S2|11|1|7|0,1,2,3,4,5|
|T_S2|22|1|7|0,1,2,3,4,5|
|T_S3|11|8|1,3|无|
|T_S3|22|8|1,3|无|
|R11_S0|11|8|0,4,6|无|
|R11_S0|22|8|0,4,6|无|
|R11_S1|11|8|0,4,6|无|
|R11_S1|22|8|4,6|无|
|R11_S2|11|8|0,1,4|无|
|R11_S2|22|8|0,1,4,6|无|
|R11_S3|11|8|4|无|
|R11_S3|22|8|0|无|
|Learned|11|8|1,3|无|
|Learned|22|6|2,4,6|无|
|LearnedLB|11|8|0,1,3,7|无|
|LearnedLB|22|8|1,2,3,4,5,6,7|无|

完整160项计数、TRAIN自然区域差、EVAL点估计/对话区间和资格见[tables/expert_training_evidence.csv](tables/expert_training_evidence.csv)。主相似度见[tables/similarity_summary.csv](tables/similarity_summary.csv)，4350条逐对见[tables/within_model_similarity.csv](tables/within_model_similarity.csv)。所有130个合格专家的1170行参数指标见[tables/parameter_spectral_metrics.csv](tables/parameter_spectral_metrics.csv)，不是只分析49赢家。

## 5 数值与资源核查

任务pt-96wch7l2，平台终态SUCCEEDED，h100-4-reserved/shphd-lite-0911，既有runtime。协调进程活动墙钟153.238秒，非纯GPU kernel时间；CPU制表制图30.694秒，附加CPU缓存读取55.341秒/4线程。没有追加GPU或训练任务。实际完成682次唯一FP64分解、130个响应PCA、4350配对、1170谱指标行。

分解以4个固定向量作重构核查，最大相对残差1.07164e−14；前16基正交性误差2.66454e−14；奇异值能量与矩阵Frobenius能量相对差3.11894e−15。它们验证数值实现，不构成科学发现。主自然EVAL与原GPU保存NLL核对差0。运行、资源、每模型耗时及冻结身份见[evidence/runtime.json](evidence/runtime.json)、[evidence/completion.json](evidence/completion.json)、[evidence/summary.json](evidence/summary.json)和执行侧outputs每模型complete.json。

附加CPU分支恢复缓存expert输出的BF16中间量，并保持原g、a乘法顺序，用同一冻结head比较候选expert。与原GPU自然NLL最大差0.124913，Base单独核对最大0.000566；13模型BOUNDED、7PASS。BF16、batch形状、CPU算子是可能来源，未唯一诊断。保留全部机器结果但不据此给功能排名，不能以此反证主SVD/PCA或原GPU收益标签。[数值核对](evidence/probe_loss_checks.json)、[分支状态](evidence/probe_loss_status.json)。

## 6 图与来源解释

13组图，每组PNG/PDF/SVG。所有主要图已实际查看；逐图的对象、轴、聚合、证据和不能证明什么见[图索引](figures_cn.md)。图像不是替代数据，完整数表同目录保存。来源分发使用原全EVAL自然路由，来源NLL分别保留位置和问答平均；小来源保留样本量。来源不是纯领域，学习router的末态来源分发也不是训练历史。

## 7 本轮记录与推断边界

问题：第一轮哪些expert有足够训练及留出收益，主方向是否不同，谱是否更均匀。设置：上述20固定模型、同seed初始化、原路由；输入是父TRAIN/EVAL与保存checkpoint；本轮无训练数据更新，EVAL已暴露。结果：130暴露合格、49通过本轮收益判据；输出方向不完全相同；gate/up全部略集中，down无初始归一化谱对照。认识更新：几何差异已量化，平谱不能当作训好证书，未建立频率路由特有功能优势。

科学物理先验未在本轮裁决；形式模型没有被证明或推翻；“有参数变化/平谱便是有效分工”的代理替代不成立。工程核查通过仅说明主计算可信，附加CPU核查失败保留。共享数据、初始化、训练量及路由门差别仍是竞争解释。不能声称语义分工、有效容量提高、长期隔离、模型通用能力改善或确定收敛。

研究者机制判断与下一决策Unknown。AI建议只有一个：先以统一GPU路径核对自然路由，再对有收益expert做同输入替换，检验内容选择性能否造成任务损失差。该后续NOT_RUN；本轮完成后停止。

## 8 产物与复现入口

[artifact_manifest.json](artifact_manifest.json)记录选入仓库的表/图来源、hash、角色及允许声明；原始数组、checkpoint、完整代码/日志在执行侧，不进入讨论包。分析资产`analysis_tulu_epoch1_expert_geometry_20261019t030056z`与主方向数组资产`representation_tulu_epoch1_expert_pca_svd_20261019t030056z`分开。它们都不产生新checkpoint或科学批准。

执行代码：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/epoch1_expert_geometry/20261019T030056Z/code/analyze_model.py`、`summarize_and_plot.py`、`benefit_subset_figures.py`、`render_top16_benefits.py`、`cached_probe_losses.py`；实际文件身份见manifest，禁止以复现导航暗示自动重跑许可。配置`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/epoch1_expert_geometry/20261019T030056Z/config/frozen.json`；作业/日志在执行根。完成及交付核查见[completion_receipt.json](completion_receipt.json)。
