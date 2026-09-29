# Protocol：自然 NTP 表征预测更新相容性 v1

## 0. Approval Snapshot

- 文档状态：**EXECUTION_AUTHORIZED_PENDING_QUALIFICATION**；实验在本次指令时仍 **NOT RUN**。[英文原文](protocol.md)。
- 2026-09-29研究者在审核交付后明确指令：按本Protocol实现并提交Smoke，监督通过后提交Full。此指令批准本版本的设计与这两个运行阶段；原先仅文档授权的记录是历史状态。数据、数值、拟合、资源、封存和Smoke门槛仍逐项生效；未授权commit、push或改动旧Focus的科学裁决。
- 所属设计：[Anchor 中文](anchor_natural_ntp_representation_compatibility_cn.md)／[English](anchor_natural_ntp_representation_compatibility.md)。下文明确给出的载体、数字、预测器和门槛原为 **AI_PROPOSAL**，已由上述执行指令按原文采纳；资格检查不因此自动通过。
- Focus：[0927原Focus](../../0927/focus_shared_update_conditional_interference.md)持有已完成的受控二元任务，不持有本次自然文本设计。新的Focus确认是**正式晋级阻塞项**，不阻止按用户要求写完供审核的方案；不默认覆盖旧Focus。
- 目的／实验角色：操作化检验，判断原生更新前表征能否在独立文档上预测连续局部NTP更新相容性；不是Router构造。
- 最小设置：S7、重构系数0.1、精确33B训练词元检查点；末块注意力输出矩阵；一个自然文档分片及真实下一词。
- 改变预测器输入／函数族；固定模型、矩阵、语料、事件、标签、划分、拟合和评价规则。预测为观测研究；临时矩阵更新只核对有限步损失联系。
- 主比较：开发集选出的几何／完整表征预测器相对训练均值常数，指标Q（§10），提出门槛0.05。允许所有K为正。
- 支持：95%区间下界>0.05；不支持：上界<0.05；不足：区间包含0.05或资格失败。有限步是独立的资格和结果。
- 不可声称：已测得不可消除不确定性、特征因果使用、路由／隔离收益或跨模型规律。
- A—G已由2026-09-29执行指令按本版采纳；Focus的后续科学状态仍由研究者持有，运行资格须按阶段实测。纸面跨块一致性已审计；工程与结果状态以持久收据为准。

## 1. Terminology / Definitions

**事件**：原文开头256词元作为前缀，第257词元为唯一真实目标。**数据对**：来自两个不同文档的事件。**完整表征**：末位置进入指定矩阵的全部2048维，不代表全部层或下游掌握的全部信息。

矩阵输入c为2048维，输出a和该样本自己的残差r为1024维；e为一次全词表NTP交叉熵对a的1024维导数；G为1024×2048矩阵梯度；K为两梯度的Frobenius内积。普通标量学习率SGD下，K>0是一阶帮助；I为更新后减更新前的nat／目标损失，I<0是实际帮助。Q是相对均方误差降低量，无量纲，不是梯度余弦或路由收益。

OPS／TRAIN／DEV／CONFIRM由不重叠的去重组组成，分别负责工程检查、拟合、预设选择和确认。辅助预测器训练不等于语言模型继续训练。

## 2. Anchor Alignment

保留三个分析步骤：①采集原生表征与纯NTP梯度对标签；②训练仅表征预测器，在独立文档上检验；③核对少量有限步更新，仅在主结果支持后进行已注册的次级结构比较。完成标准是所有必需阶段均有事实结果或明确失败类型，不是一定得到正结果。

Anchor研究连续差异是否可预测，不要求存在负K、不要求完整表征超过几何、不要求SAE获胜、不寻找旧toy的翻标签模式。梯度恒等式是测量资格；新文档预测才是经验检验。当前唯一人类决策为是否接受这份设计，再决定实现／运行晋级。

## 3. Tested Hypothesis

H1：本方案的仅表征估计器，在确认集相对训练均值常数预测降低至少5%的K均方误差。这是指定模型状态下可提取信息的操作化下界检验。DEV选择几何预测器也可支持；完整表征超过几何为次级问题。

单位置公式为：

\[
G_i=e_ic_i^\top,\quad K_{ij}=(c_i^\top c_j)(e_i^\top e_j),\quad
\mu(c_i,c_j)=\mathbb E[K_{ij}\mid c_i,c_j].
\]

以平方误差训练预测器估计条件均值。本轮不检验跨检查点稳定性。

## 4. Rival Explanations

| 竞争解释或捷径 | 区分证据 | 边界 |
|---|---|---|
| 整体均值／大多数更新帮助 | 常数MSE参照、连续目标 | 单一符号仍允许 |
| 仅范数／余弦关系 | 几何基线及完整表征增量 | 几何成功也是表征成功 |
| 记住文档／近重复 | 先去重分组再划分，确认端点不复用 | 仍可能有未检测到的语义重复 |
| 真实目标／梯度／未来词泄漏 | 输入字段白名单、前缀不含目标、确认封存 | 训练明确使用梯度监督 |
| 预测器／样本不足 | 学习曲线、有限值、固定三种子集成和开发搜索 | 不支持不证明所有函数无信息 |
| 一阶近似不可靠 | 两个固定SGD步长和实测余项 | 只限制损失推论，不抹掉合格K预测 |

## 5. Data Construction And Provenance

**选定数据提案：**
`/mnt/bucket/109_cache_dir/hf_data/dclm_eval_holdout/global-shard_02_of_10/local-shard_0_of_10/shard_00000000_processed.jsonl.zst`。
本轮实算SHA256：`4c5ce60258943051758148653c448bb57724af7592cc9d3e9c053cc6f9e10323`。文件存在，读取的首条解压记录含字符串text和url；全量schema、可用数量和去重尚未执行。数量不足就停止，不自动更换分片。相对该检查点的global-shard-01训练视图属于文件级留出，不证明语义上没有预训练重叠。此来源有历史审计使用；只在以下曝光账本允许的范围称本轮为封存预测评价，不宣称文本普遍从未见过。

**构造规则，种子20260930：**按JSONL原行序解析，要求text为非空字符串、不含U+FFFD、同检查点tokenizer以`add_special_tokens=False`编码后至少257词元。前257词元包含tokenizer定义的特殊ID则排除。不得按领域、loss、目标频率、梯度或置信度筛选。前缀为索引0..255，目标为256，无拼接、补齐、额外BOS；仅评价前缀位置255。总体限定为该分片合格文档的开头，不是所有自然语言位置。

仅去重时把text转NFC并合并Unicode空白；实际编码使用原文。doc_id为`source_sha:line_index:normalized_text_sha`的SHA256。以`20260930:pool:doc_id`的SHA256排序，取前20,000个合格记录，不足则取全部。在候选池构建重复连通分量：标准化全文哈希相同、去首尾空白的非空URL相同、前257个token完全相同，或这些token的连续5-token shingle集合Jaccard≥0.80。可用精确倒排阈值连接加速，但不能仅靠近似检索宣称所有高相似对已排除。每组保留最小doc_id，保存全部成员。该阈值仅作泄漏护栏，不代表语义相同；在全候选池上做不看结果的去重需明确记录。

`exposure_ledger.json`记录与可用历史事件／窗口哈希的比较、已知使用来源和不可访问账本。若能够识别此前看过梯度／预测结果的相同257-token事件，在分配前排除；不读取0924仍封存的确认文件来完成此检查。旧12个合成方向族也不复用。若开发时已查看本次CONFIRM结果，停止并判该确认失效，不能看结果后悄悄重抽。

剩余代表按`20260930:split:doc_id`哈希排序，依次分配OPS64、TRAIN4096、DEV1024、CONFIRM2048；不足7232则`DATA_CAPACITY`停止。每组一个事件，多余记录丢弃并记数量。不能自动扩容，也不退回无文档边界的packed bin。

**配对：**TRAIN在所有不同事件的无序对中，取`20260930:train_pair:min_id:max_id`哈希最小的32,768对。DEV和CONFIRM分别按`20260930:pair:<split>:doc_id`哈希重排ID，相邻配对，得到512和1024个不共享端点的对。OPS同规则得到32对。采梯度前保存端点和哈希；不按K符号平衡。确认独立单元是互不共享去重组的文档对，不以同一文档重复出现制造独立样本；区间仍条件于本语料和已拟合模型。

Tokenizer只使用`/data/share/Qwen3-0.6B-Base`的分词资产，绝不加载该目录预训练权重。`tokenizer.json` SHA256为`c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539`，词表151936；其他tokenizer文件须和运行`resolved_config.json`中的指纹核对。

## 6. Learning Task And Permitted Supervision

输入仅c_i,c_j，输出原始K的一个实数估计。训练监督来自TRAIN真实目标的纯NTP梯度内积。用TRAIN对标签均值m及总体标准差s，把标签标准化为(K−m)/s；所有报告还原到原K。s为0或低于§11测量分辨率则停止。没有对数变换、符号重平衡、标签截断或异常值删除。

允许TRAIN拟合的坐标均值／标准差和注册投影。禁止预测器读取ID、URL、文档／领域标签、y、loss、置信度、e、G、梯度范数、K、更新后激活。真值与允许特征分文件存储；特征schema拒绝额外字段。冻结后的离线诊断可读真值，但不可反馈到拟合或选择。监督是自然下一词，不是人工领域标签。

## 7. Model / Architecture And Frozen Variants

**语言模型检查点：**
`/data/250010109/MoE_Router/experiments/20260920_s7_lambda0p1_from_scratch_4h100/runs/S7_lambda0p1_from_scratch_4h100/milestones/token_033000000000`。
要求manifest完整、tokens_seen=33,000,000,000、optimizer_step=125894；state SHA256为`c30b78e5bcba8f0a09c5e215389be86778874e87fcbb9fe5211175d370bb0803`。运行加载前实算state哈希。8层原生稠密因果LM，主干281,431,040参数，SAE61,471,024，共342,902,064。SAE为sidecar、hook7、注意力输出投影后残差相加前、宽30000、TopK32、历史重构系数0.1；实际源码／配置定义计算，不能另选名字类似的Qwen。

只临时修改`model.blocks[7].attn.o.weight`（1024×2048，预期无bias）；其余权重、缓冲冻结。eval模式，FP32，无autocast／TF32，不导入历史优化器状态。最终全词表log-softmax／CE用FP64，反传经过该转换。每条事件保留自己的残差r；缓存位置255的c、a、r、e。e/G/K不包含重构或AuxK损失。

所有完整表征用TRAIN逐坐标均值／标准差处理，分母max(SD,1e−6)，不按样本归一化长度。几何特征先在原生c上计算：两范数之和、范数差绝对值、内积、余弦（分母max(范数积,1e−12)），再在TRAIN对上标准化这四维。

| 条件 | 架构 | 作用 |
|---|---|---|
| B0 | 常数TRAIN对均值m | 无输入主参照 |
| B1几何 | 4→32→1 MLP，隐层GELU、输出线性、带bias | 简单表征读出 |
| B2完整c | 两端共享2048→256→128编码，两个GELU；拼接两端编码的和、差绝对值、逐元素积；384→128→1头、隐层GELU、带bias | 完整向量读出、精确交换对称 |

不使用dropout／batchnorm。Linear沿用框架默认初始化，记录版本和种子。编码宽度是读出能力选择；输入完整不等于信息论上界。

**仅主结果支持后进行的次级面板：**TRAIN中心化c的精确SVD PCA，秩32/128/512；同秩高斯随机矩阵QR投影，R对角取正，种子101/102/103。先投影原生中心化c，再以TRAIN统计标准化坐标。full-a使用1024维原生输出，SAE-a使用原生a的冻结TopK稀疏代码（30000维）再逐坐标标准化。全部用B2结构，仅改变输入维数；两端用同一空间。不训练SAE、不选原子、不插入重构。采用B2在DEV选出的学习率／weight decay和epoch数，每变体三种子预测取均值，不重新在确认集调参。输入层参数量不同和表示相关的优化难度均须报告；这是操作化读出比较，不是信息丢失证明。等参数量进一步比较留作未来工作，不暗改容量。

## 8. Training Objective And Optimization

B1/B2最小化标准化K的batch均方误差。AdamW，betas=(0.9,0.999)，eps=1e−8，全局梯度范数裁剪1.0。开发搜索：学习率{1e−3,3e−4}×weight decay{0,1e−4}；固定学习率，无调度和warmup。batch512对，一次拟合一GPU，不把不同拟合做梯度平均。每epoch64完整batch，每配置／种子训练50epoch即3200更新，不提前停止。每epoch用本拟合种子生成器打乱TRAIN对；非有限标签、loss、梯度或权重直接失败，不跳过更新。

每配置、每函数族均使用17/29/43三个种子。每epoch计算三种子平均预测的DEV MSE；在4配置×50epoch中选择最小者。精确并列依次选更早epoch、更小weight decay、更小学习率。保留同一选定epoch的三个权重，不挑最好种子。B1/B2各自选择后，以DEV MSE选q_*，精确并列选B1。不把TRAIN与DEV合并重训。CONFIRM特征／预测评价前冻结预处理、全部选定权重、q_*和pair manifest。

拟合资格：各保留运行有限，并且标准化TRAIN MSE相对初始化降低至少1e−4，否则`FIT_UNQUALIFIED`，不能把优化未成立当成表征无信息。此护栏和三种子也不证明优化充分；所有候选学习曲线均保存。

**观测合同：**遵循[训练可观测性要求](../../../docs/training_observability_contract.md)，但不伪造LM训练。主干优化器更新数为0；纯NTP测量使用`measurement/ntp_loss`和`measurement/valid_targets_seen`，每事件只有1个有效目标，256前缀词不是256个监督目标。LM训练／辅助损失标签在scope registry中记`NOT_APPLICABLE`。预测器写`<run>/tensorboard/<variant/config/seed>/`，标签为`pairs/train_mse`、`updates/train_mse`、`pairs/train_total_loss`、`updates/learning_rate`、`progress/pairs_seen`、`progress/optimizer_step`、`progress/effective_pairs_per_update`=512；组件`compatibility_mse` raw=weighted、系数1、分母512对。仅完成更新后累计pair暴露；同一文档反复入对不能记作新LM token。比较条件保持相同pair batch／顺序／预算。保存optimizer、RNG、epoch、batch游标和两种坐标，恢复须复现下一更新且不重复日志步。不以这些拟合曲线声称LM训练效率。

## 9. Conditions, Seeds, And Checkpoints

固定一个主干检查点。构造种子20260930，拟合17/29/43，投影101/102/103，bootstrap20260931；这些种子不是不同模型状态重复。B0/B1/B2必做，DEV预选主预测器。条件式面板共14个读出：PCA3＋随机9＋full-a1＋SAE-a1，每个三种子集成。不论结果如何都保留主条件预测和标签；每条件状态为已执行、NOT_RUN_BY_GATE或FAILED。

实现前读[复用索引](../../../docs/training_reuse_index.md)。复用检查点／配置／tokenizer；适配`.../20260927_common_rule_controlled/scripts/smoke_worker.py`的load_model/capture以及`.../20260920_s7_lambda0p1_from_scratch_4h100/dense_sae/model/modeling_qwen3_sae.py`。本轮已读源码，确认样本残差捕获与末块逐位置尾部。**拒绝原样复用make_tail**：旧代码只取词表[100,101]且用固定残差；本轮必须改为逐事件残差、全词表，并重新做数值资格。拒绝旧合成生成器、共同原子选择、范数归一化更新和确认数组。本轮只写文档，没有复制或实现实验代码。

## 10. Primary Metric And Frozen Analysis Plan

1024个不共享文档的确认对等权，原始K上计算：

\[
Q=1-\frac{\sum_{ij}(K_{ij}-q_*(c_i,c_j))^2}{\sum_{ij}(K_{ij}-m)^2}.
\]

不按符号分层、不截尾。这是相对TRAIN均值的留出MSE技巧分数，不在测试真值上重新拟合常数。NumPy PCG64种子20260931，2000次有放回抽取1024个pair索引；同一索引用于所有条件分子分母。用linear quantile的2.5/97.5百分位形成双侧95%区间；不在bootstrap中重训。区间条件于已拟合预测器与语料，不含训练集、模型种子或语义来源不确定性。独立单元为不共享去重组的文档对，仍明确同站点依赖可能存在。

下界>0.05支持，上界<0.05不支持，否则不足。0.05是供审核的继续结构研究门槛，不是测得的效应或路由价值。唯一主预测器由DEV选定，不在测试结果中选赢家。次级指标使用相同bootstrap作描述区间，无多重检验校正，不升级成多个确认性假设。

任何必需事件／pair缺失或非有限，主结果判`INSUFFICIENT`，不得按K/loss删除或替换。有限异常值全部保留。不得在确认集选检查点。如果基线MSE≤100δ_K²或K经验方差≤100δ_K²（§11），标记`LOW_RESOLUTION_TARGET`，不解释不稳定比值。符号单一但变化可分辨仍有效；K完全恒定则无可预测的变化。

**开封：**OPS/DEV资格通过后，将预测器、步长及科学文档／配置／源码哈希写入不可变`registration.json`；先保存并哈希`confirmation_predictions.npz`，才释放CONFIRM真值给分析。测量进程可提前计算真值，但不得供拟合或选择使用。运行收据可追加，不能改注册正文。

## 11. Secondary Metrics And Guards

**OPS数值资格：**检查state实算哈希和FP32 eval。完整前向的唯一末位置纯CE对W的autograd梯度，与e*c^T比较相对Frobenius误差≤1e−5（分母max(norm,1e−12)）。其他位置输出损失导数范数≤末位置导数范数的1e−7，否则`POSITION_CONTRACT`停止。相同完整batch形状的Wc与捕获a相对范数误差≤1e−5；尾部和完整前向logit最大绝对差≤2e−4、CE差≤2e−5。精确重复、batch形状变化、尾部回放分别记录差异，保守取最大损失差δ_L（下限1e−10）和对直接梯度内积的最大K差δ_K（下限1e−12）。OPS32对全部检查，形状差异不能叫精确重复噪声。DEV选好步长后，至少8个OPS事件还需通过临时W完整前向与尾部更新一致性检查。W精确恢复，所有冻结tensor前后hash一致。恒等式通过不是科学发现。

**有限步校准：**取DEV按hash前32对，两个更新方向，选择共同学习率：

\[
\eta(\alpha)=\alpha\|W_0\|_F/\operatorname{median}_{i\in\mathrm{OPS}}\|G_i\|_F,
\qquad\alpha\in\{10^{-4},3\times10^{-5},10^{-5},3\times10^{-6}\}.
\]

分母是一个固定OPS尺度，不是按来源分别归一化。OPS梯度中位范数必须>0。按alpha降序逐个检查本步及半步；两个步长都要求：≥90%的DEV有向对满足

\[
|I+\eta K|\le0.1|\eta K|+5\delta_L;
\]

≥90%来源事件自损失下降超过5δ_L；≥80%有向作用满足|ηK|>20δ_L；每次相对矩阵更新范数≤1e−3。选择第一个合格候选；无候选则`FINITE_BRIDGE_UNQUALIFIED`，跳过确认更新，不自动扩展搜索。只要K自身测量／预测合格，主结果仍可判断。零／很小梯度的来源保留在记录中。

**确认有限步面板：**真值开封前，按(预测K,pair_id)对1024对排序，以floor(3*rank/1024)分三等份；每份按种子20260930哈希取32对，共96对。不看真实K/I选样本。每对两个方向、η和η/2，从同一W0独立更新，共384个有向后果。保存实际I、源自损失、一阶项、余项、范数和恢复收据。同样要求90%余项／源改善、80%分辨率以及步幅护栏，不重调。以−η*q_*预测实际I，以−η*m为常数参照，按§10公式计算Q_I；对96个无序pair整体bootstrap2000次，每次把该pair的双向／双步长一起抽取。三等份样本各等权；报告这是分层面板估计量，不当成总体表现。全部护栏通过且Q_I的95%下界>0，才记`FINITE_LOSS_PREDICTION_SUPPORTED`；否则分清数值桥失败还是预测未迁移。主K结果不回写。

**次级读数：**K符号比例、秩相关、梯度余弦κ（零梯度标undefined）、B1/B2各自Q及归一化增量`(MSE_B1−MSE_B2)/MSE_B0`。完整优于几何支持额外读出结构；两者均成功而相等支持简单几何。残差不是不可消除方差估计。结构曲线显示full/PCA/random成绩、秩和实际预测器参数量；SAE只与full-a对齐。低维接近完整须以完整预测本来有效为前提，且只条件于所测估计器，不作因果定位或信息丢失证明。

## 12. Known Good / Known Bad / Known Confusing Cases

仅作工程测试：标量平方损失同目标例得到正K；相反目标得到负K；正交输入交叉项为0；小扰动有限差分与autograd一致。检验交换对称、目标不进入前缀、重复评价端点拒绝、故意TRAIN/CONFIRM碰撞拒绝、禁止字段拒绝、原检查点精确恢复。全正但变化的合成回归目标必须可评分；恒定目标必须拒绝不稳定方差分数。故意失败的拟合不能产生科学“不支持”。每项留预期／实测通过状态，不作自然数据发现。

## 13. Scientific Procedure And Stage Contracts

| 阶段 | 输入→操作→输出 | 目的、资格、失败和交接 |
|---|---|---|
| S0溯源 | 已批准范围及确切资产→哈希、schema、去重／划分、运行环境→manifest | 排除替换／泄漏；身份、数量、schema失败即停；不打开确认真值 |
| S1工程 | OPS64→捕获、autograd、尾部／no-op、预测器和恢复smoke→资格收据 | 只证明接口／资源；OPS临时拟合不计科学成绩 |
| S2训练开发 |4096+1024事件→标签、预设拟合、DEV选择及步长→不可变选定权重／步长 | 估计读出结构；拟合失败为不足，步长失败单独处理 |
| S3冻结确认 | 选定设置及哈希→注册、封存预测、释放真值、主分析→Q／区间／结果 | 唯一主证伪；不得反馈S2或替换pair |
| S4有限步 | 预测选出的96对→双向／双步长→Q_I及护栏 | 建立损失联系；仅DEV桥失败可跳过 |
| S5条件结构 | 主结果支持＋缓存→14注册读出→PCA/random和full-a/SAE曲线 | 次级；失败不救回／推翻主结果，否则NOT_RUN_BY_GATE |
| S6审计报告 | 所有成功／失败证据→完整性、身份及分析复核→Summary／Detailed | 事实与人类判断分离，不自动结题 |

未来远端smoke只使用OPS64，执行全部工程测试、B1/B2各20步临时拟合及一次保存恢复重放；不打开确认集。要求有限日志、schema完整、恢复计数精确，下一步预测相对差≤1e−6。smoke成功不授予full批准。

**资源提案：**遵循[执行envelope](../../../docs/execution_envelope.md)默认`h100-4-reserved`、镜像键`shphd-lite-0911`及现有ACP模板；单allocation、四独立worker，不对不同事件／拟合做DDP平均。总分配≤24 GPU小时（4GPU×6小时，包含远端smoke），smoke≤20分钟，产物≤50GiB；无自动重试或换资源。按envelope，本地只读准备≤60分钟。OPS实测吞吐后，以1.5安全因子估计剩余时间，若超剩余预算则`RESOURCE_UNQUALIFIED`，不暗减条件。本轮无ETA；设备内存、runtime、镜像资格NOT RUN。预算扩大或换语料需要审阅修订。

## 14. Algorithm, Output, And Provenance Contract

未来执行根提案：`/data/250010109/MoE_Router/experiments/20260930_natural_ntp_compatibility/`，本轮未创建；每次尝试独立`runs/<UTC>/`。研究仓库只持有Anchor／Protocol和后续小型报告。接口职责提案（全部 **NOT IMPLEMENTED**）：`prepare_data.py`、`qualify_measurement.py`、`collect_events.py`、`fit_predictors.py`、`freeze_and_predict.py`、`finite_check.py`、`analyze.py`、`audit.py`。下个代码对话须落实实际源码／配置和哈希，不能把名称当成已存在脚本。

| 产物 | 最小schema |
|---|---|
| data_manifest.json、events.jsonl、pairs_<split>.npz | 数据／tokenizer哈希、排除和重复组、ID／split／原行／前缀与目标哈希、数量、pair端点、种子、曝光账本 |
| features_<split>.npz | ID、c[2048]、a[1024]、r[1024]；可附冻结SAE索引／值；导出给预测器时无真值字段 |
| truth_<split>.npz | ID、y、CE、e[1024]、梯度范数、pair K、dtype和允许访问阶段；OPS保留直接G，其余用因子 |
| preflight.json、smoke_receipt.json | 实际哈希、架构断言、误差／阈值、δ_L／δ_K、恢复、资源估计、失败门槛 |
| fits/、selection.json、registration.json | 每配置／种子／epoch、optimizer/RNG/计数、TRAIN变换、选定集成及q_*、步长、科学源／代码哈希 |
| confirmation_predictions.npz | 冻结pair ID及所有主条件预测，开封前哈希／时间；真值另存 |
| finite_pairs.csv、finite_results.npz | 预测分层、来源／目标ID、η、I、自损失、ηK、余项、范数、no-op／恢复 |
| analysis/primary.json、secondary.csv、condition_ledger.json | 指标分子分母、bootstrap索引、区间、类型裁决、所有条件状态 |
| verification.json、failure.json、environment.json、tensorboard/ | 完整性／身份／数值／分析检查；失败原因／阶段／已完成部分；版本设备runtime；观测日志 |

原子写入，不覆盖其他run；失败保留原错误及终态。恢复复用同manifest/config/model/封存状态，跳过已验证事件，恢复预测器optimizer/RNG/计数；不一致时新建attempt并判断证据资格。原checkpoint不写，前后检查源及非W参数hash。单位置资格通过后，c/e因子可精确重建K，无需每事件保存巨大G；主标签不采用有损梯度sketch。worker收据记录不重叠ID及完整校验数量，GPU个数不当作样本数。

执行后应有三类图：①确认预测对K散点和常数／Q区间；②预测分层对双步长实际I，注明分层面板；③条件式秩／读出曲线、完整基线和随机范围。标明模型、矩阵、单位、划分、计数、来源和可支持边界，保留负结果，区分实测与示意。原图置执行根，所需阅读副本进日期`figures/`并记`SOURCES.md`。现在不制造结果或图。

## 15. Success / Failure / Insufficient Evidence

主结果严格按§10。B1通过就报告表征预测获支持、简单几何在此读出下足够，不把B2没有增益叫失败。区间低于0.05但高于0，可报告小量可提取信息，未达继续门槛。单符号有效；不可分辨变化不足。拟合／数据／测量失败不是科学反证。有限步和结构分析有独立状态，不倒改主结果；结构失败只收窄相应读出结论。

完成可以是“不支持”或“不足”。事实Summary／Detailed仍须含目的、假设、方法、结果或NOT RUN、失败定位、证据路径和待定人类判断。不未经独立验证就把负K样本称稳定自然冲突群。

## 16. What This Cannot Claim

单一2.81亿参数主干、检查点、矩阵、文档开头总体和预测器，不能建立一般大模型几何、SAE因果原子、不可消除条件方差、长期隔离收益、Expert数量或可部署Router。本轮不比较LM训练token效率。源事件改善不是源任务泛化；梯度监督训练不等于整个方法无梯度；full-c与full-a／SAE的成绩差可能来自读出能力而非纯信息损失。

## 17. Block Confirmation, Freeze, And Amendment Ledger

| 块 | 提交审核的确定提案 | 状态／晋级依赖 |
|---|---|---|
| A问题 | 连续自然NTP K预测，几何可支持 | 2026-09-29指令采纳；Focus结论仍Unknown |
| B数据 | 指定原始分片、256→1、去重、64/4096/1024/2048、评价不共享端点 | 指令采纳；容量／曝光资格依收据 |
| C任务 | 测试仅表征，训练真实K监督 | 指令采纳 |
| D模型 | S7 λ=0.1/33B、末块attention W、固定读出 | 指令采纳；运行身份／梯度资格依收据 |
| E拟合 | 标准化MSE、固定搜索／三种子集成、DEV选择 | 指令采纳；拟合资格依收据 |
| F判据 | Q相对常数、0.05门槛、有限步分开、条件式结构 | 指令采纳；0.05仍仅为本实验继续标准 |
| G执行 | 单allocation≤24GPU小时／50GiB、不可变产物和停机条件 | Smoke与通过后的Full已获明确指令；各门槛不放宽 |

历史记录：用户先要求具体Anchor交审核，随后要求完整Protocol与memory，明确代码另开对话。2026-09-29用户在新对话明确要求完成任务、提交并监督Smoke，Smoke通过后提交Full；这项较晚的直接指令采纳了本版A—G并授权相应执行。Focus的科学结论与后续决策未被运行指令自动确认。中英文是同一Protocol的语言版本；旧两轮Reasoning报告不是另一个执行合同。

纸面一致性：数据→纯NTP→末块W梯度→pair标签→允许输入拟合→独立确认→有限步扩展已明确。执行指令不代替持久技术资格：来源／代码／配置／数据身份和各阶段收据须逐项核对；通过Smoke后才可提交Full。未确认Focus结论不被写作科学裁决。

首次运行前，实质变更重开相关块；注册／运行开始后保留科学正文，追加修订及证据影响、确认曝光，不得看到结果后改门槛。真实收据出现前保持NOT RUN。
