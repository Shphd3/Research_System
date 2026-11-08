# 方法与资产附录：末层知识学习实验

本附录说明实际系统、数据人群、监督、对照、评测和来源。效能与架构解释由主报告承担。[冻结协议](../../../originals/experiment/protocol_frozen.json)记录科学接受为 `Unknown`、问题状态为 `Open`；本附录不改变这些状态。[英文版](methods_assets.md)覆盖相同范围。

## 1. 模型身份与加载

主系统是在原始 Qwen3-0.6B Base 上附加小模块。主干、最终 RMSNorm 和原输出头冻结。Qwen3-4B 提供训练分布；后训练版0.6B和8B保留各自独立的能力对照角色。

| 角色与本地资产 | 参数规模 | 层数／隐藏宽度 | 配置位置上限 | 本轮用途 |
|---|---:|---:|---:|---|
| Qwen3-0.6B-Base-official（[包外资料 E002](../../../EXTERNAL_REFERENCES.tsv)） |596,049,920个独立参数|28／1024|32,768|主学生；两套独立 SAE 的父模型|
| Qwen3-0.6B（[包外资料 E003](../../../EXTERNAL_REFERENCES.tsv)） |596,049,920个独立参数|28／1024|40,960|后训练能力对照；沿用此前 DEV 记录|
| Qwen3-4B（[包外资料 E004](../../../EXTERNAL_REFERENCES.tsv)） |4,022,468,096|36／2560|40,960|后训练教师，原生非 thinking 对话格式|
| Qwen3-8B（[包外资料 E005](../../../EXTERNAL_REFERENCES.tsv)） |8,190,735,360|36／4096|40,960|此前摸底候选；本矩阵没有新增8B教学臂|
| Qwen3-4B-Base（[包外资料 E006](../../../EXTERNAL_REFERENCES.tsv)） |4,022,468,096个存储元素|36／2560|32,768|已定位的 Base 教师候选，仅元数据／tokenizer 核对|
| Qwen3-8B-Base（[包外资料 E007](../../../EXTERNAL_REFERENCES.tsv)） |8,190,735,360个存储元素|36／4096|32,768|已定位的 Base 教师候选，仅元数据／tokenizer 核对|

后训练版0.6B文件含751,632,384个张量元素，其中 embedding 与输出头重复存储且哈希相同。结合配置中的权重绑定，独立参数为596,049,920；重复文件元素不增加模型容量。六个模型的配置均为 `Qwen3ForCausalLM`、`model_type=qwen3`，保存的 `config.transformers_version=4.51.0`。Base 的 generation-config 保存版本与模型 config 是不同字段。局部下载元数据保留，但这些记录没有统一确立精确上游权重提交版本。主 Base 完整权重 SHA256 为 `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`。[配置刷新](../../../originals/experiment/model_config_refresh.json)、存储元素清单（[包外资料 E008](../../../EXTERNAL_REFERENCES.tsv)）、重复／版本证据（[包外资料 E009](../../../EXTERNAL_REFERENCES.tsv)）。

Tokenizer 元数据声明 `Qwen2Tokenizer` 和131,072最大长度；本轮只资格检查短提示，模型配置上限见表，不能据 tokenizer 声明声称验证了131k上下文。已核对完整 token 字符串→ID映射及特殊 token。原生输出头151,936行，共同有定义 ID 为151,669。Base 的结束 ID 为151643（`<|endoftext|>`）；后训练对话模型为151645（`<|im_end|>`）。答案监督排除结束位置。缓存布局（[包外资料 E010](../../../EXTERNAL_REFERENCES.tsv)）保留这些身份和策略。

实际环境为 PyTorch2.8.0+cu128、CUDA12.8、Transformers4.53.3。模型通过 `AutoTokenizer`／`AutoModelForCausalLM` 从本地加载，使用原生 SDPA 和 BF16 原权重。新增模块参数为 FP32，注入增量转换为隐藏状态精度。本矩阵没有量化替代权重或 CPU 权重 offload。教师使用原生 chat template 和 `enable_thinking=False`；Base 学生使用纯文本问答提示。模型类型、提示和终止策略均独立记录。加载实现（[包外资料 E011](../../../EXTERNAL_REFERENCES.tsv)）、提示与身份定义（[包外资料 E012](../../../EXTERNAL_REFERENCES.tsv)）。

## 2. 保留给后续机制研究的 SAE 与小模型

两套独立0.6B SAE 均属于上述精确 Base 父模型，输入1024维、字典30,000、Top32。它们的实际 hook 与本轮最终 RMSNorm 前注入位置不同。

| SAE 资产 | 实际输入位置 | 历史质量记录 |
|---|---|---|
| E16最终权重（[包外资料 E013](../../../EXTERNAL_REFERENCES.tsv)） |零起始第27层 `model.layers[27].mlp` 的 forward-pre-hook，即 post-attention layernorm 后的 MLP 输入|原始 summary（[包外资料 E014](../../../EXTERNAL_REFERENCES.tsv)）的 normalized reconstruction MSE 为0.0533820926|
| A17原始 attention 最终权重（[包外资料 E015](../../../EXTERNAL_REFERENCES.tsv)） |零起始第27层 `self_attn.o_proj` 输出，残差相加之前|原始 summary（[包外资料 E016](../../../EXTERNAL_REFERENCES.tsv)）的 global normalized MSE 为0.1684186278|

这些误差属于各自原始数据、过滤方式和 hook。本矩阵不训练或评测 SAE；将其用于后训练版0.6B，或用于解释当前注入增量，都需要单独验证。固定输入序列时，两个 SAE hook 均在当前注入点上游；自回归生成前缀变化后，上游状态也可能随之变化。[辅助资产核查](../../../originals/experiment/auxiliary_assets_refresh.json)保留对应关系。

| 其他本地模型／SAE | 实际身份与路径 |
|---|---|
| Dense baseline |281,431,040参数，8层、隐藏1024；33B-token精确检查点（[包外资料 E017](../../../EXTERNAL_REFERENCES.tsv)）。该 Dense 检查点没有内嵌 SAE。|
| 独立 S7 模型及 SAE |281,431,040主干参数，加61,471,024个内嵌 SAE 参数；S7检查点（[包外资料 E018](../../../EXTERNAL_REFERENCES.tsv)）。其第7层 attention-output 字典属于这一独立训练模型。|
| 普通 MoE baseline |507,988,992总参数，其中 experts301,989,888、router65,536、shared205,933,568；8层、隐藏1024、8 experts／top2；33B-token精确父检查点（[包外资料 E019](../../../EXTERNAL_REFERENCES.tsv)）。|
| MoE gate-input SAE |最终权重（[包外资料 E020](../../../EXTERNAL_REFERENCES.tsv)）对应上述精确 MoE33B 父模型；零起始第7层 `blocks.7.norm2` 输出／原生 router 输入，1024→30,000、Top32；历史 summary（[包外资料 E021](../../../EXTERNAL_REFERENCES.tsv)）的 global NMSE 为0.2267446200。|

这里33B表示训练 token 数。上述资产通过元数据／访问记录核对，没有加入本轮主比较；稳定 ID 与父模型关系见资产注册表（[包外资料 E022](../../../EXTERNAL_REFERENCES.tsv)）。

## 3. 真实文本任务、划分与筛选人群

目标事实是文本明确陈述的“某人物出生年”。资料来自已有本地 Hotpot训练缓存（[包外资料 E023](../../../EXTERNAL_REFERENCES.tsv)）的 Wikipedia 上下文句。每条只抽一个原子 `born` 关系，不把原始双跳问题视为单事实。记录保留上下文、题名／主体、规范四位年份、原记录／文档 ID、JSONL 行号与字节偏移／长度、上下文和句子索引、答案字符跨度。缓存经过本地转换，精确上游 Wikipedia 修订版本为 `Unknown`。

事实 v3 定位47,514个合格声明家族，固定选用24,096条：开发1,024、sentinel候选1,024、传记参考候选2,048、A/B各10,000。自动规则要求明确主体、显式 born、1600–2019精确年份，并核查姓名／题名、日期结构；职业消歧保留，问题中不泄漏年份。24,096条均通过源字节与答案跨度回读，涉及17,577条源记录。另以固定规则抽112条由代理阅读；人类复核0条。旧版抽取错误、冲突家族与拒绝记录保留。这些检查建立与所给文本的一致性，外部历史真实性与完整实体链接仍需另证。[数据卡](../data_prep/v3/DATA_CARD.md)、[质量记录](../../../originals/experiment/data_prep/v3/final_data_receipt.json)。

归一题名和显式主体别名先合并为 source/entity 家族，再按 hash 分集合；重复版本与冲突出生年一起检查。旧40事实仅作 DEV；之前看过的来源家族及记录的71题名排除集不进入新确认池。方法选择使用新的独立开发家族，其中实际开发面板为128事实。自动别名规则提供了已声明家族的隔离证据，尚不构成完整语义消歧。

每个规模的模块训练前，用原始学生和教师评估两个固定筛选问题。教师两问均闭卷正确者优先；否则须读原文后两问均正确。排除学生两问均正确或评分未决的事实。两种筛选问法与两种保留评测模板不同。最大20,000候选中19,849条合格，A为9,923、B为9,926；平衡后实际最大19,846，另3条合格 B 不使用。[固定选择规则与 manifest](../../../originals/experiment/cohorts/expanded_greedy_semantic_v4/manifest.json)。

| 嵌套训练规模 | A／B独立事实 | 教师闭卷已知标签 | 教师读原文标签 |
|---:|---:|---:|---:|
|2,048|1,024／1,024|38|2,010|
|8,192|4,096／4,096|153|8,039|
|19,846|9,923／9,923|364|19,482|

三行并集为19,846条独立训练事实。每个规模重新初始化模块和优化器，跨规模有意复用事实，不能把三行相加视为更多独立事实。源文本和选择规则先固定；每个规模的实际队列在该规模开训前固定。扩量依据实测时间／存储，六臂与两个种子成套保留，不按成绩挑选扩量臂。

教师按标签使用对应提示：`closed_known` 只读问题；`source_conditioned` 读原文和问题。学生在训练与自由生成时都只读问题。CE标准答案独立来自源文本。读原文教师提供的是资料监督；不能将其全部归为教师参数已有知识。学生筛选失败也包含格式失败，不能据此推断预训练接触少。

固定128条 sentinel 在所有规模接受零监督。另一批独立128段 WikiText 提供15,560个原始 token，其中15,432个为下一 token 预测目标，每段首 token 用作上下文。按记录规则，它与任务／参考来源家族隔离；仍保留本地预处理和可能的句中截断，因此仅承担这一小批通用文本的 NLL 检查。自然文本 manifest（[包外资料 E024](../../../EXTERNAL_REFERENCES.tsv)）、LM缓存布局（[包外资料 E025](../../../EXTERNAL_REFERENCES.tsv)）。

自然事实／实体频率和 Qwen 预训练曝光为 `Unknown`。本轮低曝光变量是人为控制的1次／8次答案监督呈现次数，不能据此划分自然常见／罕见知识。

## 4. 共享记忆、对照与损失

令 \(h\in\mathbb R^{1024}\) 表示冻结学生最后一个 block 输出、最终 RMSNorm 之前的状态。记忆从该状态产生64维查询、256个槽权重和1024维增量：

\[
q=W_qh,\qquad a=\operatorname{softmax}(Kq/\sqrt{64}),\qquad
\Delta h=c\,\sigma(w_g^\top h+b_g)\,W_oV^\top a.
\]

\(K\) 为256×64，\(V\) 为256×1024，\(W_q\) 为64×1024，\(W_o\) 为1024×1024；门控含1024个权重和1个 bias。Value允许正负，各参数在全部事实间共享。固定初始化比例 \(c\) 将参考状态上的增量范数标定到隐藏范数的0.001。原模型从 \(h+\Delta h\) 经冻结 RMSNorm／输出头预测，实际注入采用 BF16 cast。模块通过梯度学习共享参数，不是逐事实数据库写入。模块实现（[包外资料 E026](../../../EXTERNAL_REFERENCES.tsv)）。

| 实验臂 | 新增可训练参数 | 答案目标／对照目的 |
|---|---:|---|
|`none`|0|原始冻结 Base，零优化更新|
|`adapter`|1,393,665|带门控的普通 SiLU 附加模块，瓶颈680，CE＋KL|
|`memory_ce`|1,393,665|共享记忆，仅CE|
|`memory_kl`|1,393,665|共享记忆，CE＋KL|
|`memory_head`|1,393,665|CE＋KL，加头部64维投影能量惩罚|
|`memory_random`|1,393,665|CE＋KL，加固定随机64维投影能量惩罚|
|`memory_l2`|1,393,665|CE＋KL，加全方向增量范数惩罚|

本矩阵实际包含1个冻结基线和6个模块训练臂。常规 LoRA、全主干微调和8B监督训练没有加入本矩阵。

同一 seed 内，各训练臂的事实、规范答案、掩码、实际顺序／曝光与更新预算相同。AdamW 使用学习率0.001、betas(0.9,0.999)、epsilon1e-8、weight decay0、恒定学习率、梯度裁剪1、全局 batch16、累积1。任务损失按有效答案内容 token 取平均。CE使用完整原生151,936行输出头；teacher→student KL在共同151,669个有定义 ID 上精确计算，温度2并含温度平方，权重0.5。267个无定义输出行从KL排除；没有 top-k 截断或 top-k 重归一化近似。

头部／随机惩罚逐 token 计算“投影增量平方范数／脱离梯度的隐藏平方范数”，再按有效 token 平均。两者系数均为3.107190799106226；L2为0.19419942494413914，即前者乘64/1024。DEV梯度标定目标是头部惩罚／任务梯度比0.1；实际标定中位数为头部0.1、随机0.0373431、L2 0.0298862。同维、同系数或各向同性能量缩放不等于实际梯度强度相等。[标定及冻结参数](../../../originals/experiment/protocol_frozen.json)。

`semantic_content_v4` 将连续、单独解码为纯空白的答案开头 token 移入已知 teacher-forcing 前缀；空白与内容合并的 token 整体保留，双方完整输入 ID 序列不变，EOS不监督。每个入选四位年份实际监督4个内容 token。自由生成仍使用原问题提示，答案／空白前缀、文档和教师缓存都不提供。旧空白掩码与有效解码默认值故障作为带版本的 DEV 记录保留；正式更新使用修复后的规则和真实 GPU 正式缓存。掩码定义（[包外资料 E012](../../../EXTERNAL_REFERENCES.tsv)）、[v4源码修订](../../../originals/experiment/source/source_manifest_amendment_v4.json)。

## 5. 独立参考谱

谱基取自冻结学生的实际注入 hook，即最终 RMSNorm 输入。参考文本每篇最多256 token，每篇最多64个等间隔合格位置；对全体位置统一中心化后计算协方差特征空间，等价于中心化激活矩阵的右奇异向量。正式矩阵为32,768行、1024维，覆盖903个独立传记家族。来源位置清单记录末尾行数截断前的候选位置；实际32,768行拟合以 summary 和矩阵摘要为准。[参考谱 summary](../../../originals/experiment/spectrum/biographical_v3/summary.json)、位置采样实现（[包外资料 E027](../../../EXTERNAL_REFERENCES.tsv)）。

稳定性按 source family 的 SHA 奇偶将整家族分半，以两个头部64维子空间的平方 Frobenius 重叠除64计量。传记参考重叠为0.8998475671，高于预先固定的0.7门槛；以最大特征值的1e-6为相对阈值，有效秩为1024。另一次非传记参考实际包含432段、94来源家族、26,590位置，重叠0.6794761419未过同一门槛；失败记录保留。因此正式谱基有明确的传记分布范围。非传记失败参考（[包外资料 E028](../../../EXTERNAL_REFERENCES.tsv)）。

“头部64维”表示参考激活最大方差方向。惩罚它们仅表达少改头部的软偏好，没有把较小奇异方向标注为某类语义知识，也没有定位特定尾部谱段。随机64维基由固定种子1105001的 QR 构造。谱损失作用于门控和 \(W_o\) 之后返回的已 cast 增量；同时单独记录名义增量与数值相加后实际位移 \((h+\Delta h)-h\)。

## 6. 曝光账本、更新计数与设备续接

种子1105／1106使用同一 source/entity 分配 seed1105，并在1106交换1次／8次组。高曝光事实先呈现7次，末次低／高曝光尽可能放在同一有效更新内。真实 schedule 事件记录缓存 `index` 和逐事实 `exposure_index`。全局账本核算实际事实和有效 token，保留不满 batch；不靠 epoch 倍数或 DDP padding 补数。同一 seed 内1次与8次组是不同事实；配对方法比较在同一事实和同一配额内进行。

| 规模 | 每阶段事实 | 每阶段每轨迹更新数 | seed1105每阶段内容token预算 | seed1106 |
|---:|---:|---:|---:|---:|
|2,048|1,024|288|18,432|18,432|
|8,192|4,096|1,152|73,728|73,728|
|19,846|9,923|2,792|178,628|178,600|

最大阶段的9,923个家族为奇数：1105含4,961个1次事实和4,962个8次事实，1106交换，因此分别有44,657／44,650次呈现。配对调度的实际更新列表均为2,792步，计数包含前缀／末次配对边界，不能只用总呈现数除16后取整。最大 A→B 设计累计5,584更新，分别357,256／357,200内容 token。这些是计数定义／预算；实际完成状态由独立完成证据承担。调度与训练实现（[包外资料 E029](../../../EXTERNAL_REFERENCES.tsv)）、已保存A计数核对（[包外资料 E030](../../../EXTERNAL_REFERENCES.tsv)）。

初始 GPU 资格检查使用2张 RTX5090，每张报告显存33,668,988,928字节。完整4步与2步＋恢复2步在模块、优化器、scheduler、全部 rank RNG、身份、游标与账本上精确一致；单 rank／双 rank 的账本也精确一致。正式各臂采用独立 world size1。资格记录（[包外资料 E031](../../../EXTERNAL_REFERENCES.tsv)）将这些工程检查与训练效能分开保存。

最大规模 A 在5090作业 `pt-vbvlpop3` 上训练。用户重新授权后，作业 `pt-5gno22e6` 获得4张 H10080GB，通过实测资格后接续 B，并重测匹配设备的 pre/A/B。模块、Adam、scheduler 和 RNG 从各自精确 A 检查点加载。4卡并行执行4条独立 world1 臂，每臂 batch／曝光不变；跨架构 BF16 未来更新轨迹不声称逐位一致。原5090 pre/A输出保留，新 H100 评测进入主统计。[H100资格](../../../originals/experiment/resource_transition_20261106/qualify/qualification.json)、[续接 manifest](../../../originals/experiment/resource_transition_20261106/handoff_manifest.json)。

独占 B 目录预约使 H100 B 可与旧5090只读 A 评测重叠。旧 worker 随后到达原有 B 目录 guard，保留 FAILED／RECOVERY_REQUIRED。新门控要求该历史、真实 H100 阶段／队列完成、源码哈希及12条父检查点血缘，不将旧失败改写成成功。最终统计显式选用匹配设备计划，并引用已完成旧规模的原结果位置。续接桥契约（[包外资料 E032](../../../EXTERNAL_REFERENCES.tsv)）。

## 7. 生成、评分与不确定性

学生各臂使用同一纯文本短答案模板。显式设置 `do_sample=False`、`num_beams=1`、`use_model_defaults=False`，batch64，最多32个新 token；首个完成的非空答案行或原生 EOS 停止。原始 Base 的物理基线 seed1105；训练后端点在实际计划中记录对应运行 seed1105／1106，均为 greedy。显式参数避免 Transformers 默认值覆盖预期解码。自由生成实现（[包外资料 E033](../../../EXTERNAL_REFERENCES.tsv)）。

完整评测覆盖全部 A/B 和同一128条 sentinel，包含训练原问法与两个固定未训练模板。主要事实指标要求两个保留问法都正确；原问法准确率和 teacher-forced 内容 token NLL 是独立次要指标。一问明确错、另一问未决时，联合事件明确失败；其他未决情况保留 Unknown。Unknown 不移出分母，分别报告保守值与识别上下界。归一别名、单一无修饰年份、不确定／多年份和格式失败保留原评分状态及原始输出。独立词法复核仅标记问号、未覆盖概率词／否定和年份格式风险，不自动改标签。[统计规则](../analysis_tools/v2/README.md)、复核规则（[包外资料 E034](../../../EXTERNAL_REFERENCES.tsv)）。

B后固定192事实诊断包含64A、64B、64sentinel。记忆开启、关闭、只排列 keys、只排列 values 使用相同事实、顺序、batch和单独测得的同形状基线，排列 seed1105002。K/V共同排列只作函数不变的实现检查。Sentinel有完整生成分母；因未提供其 NLL 缓存，sentinel NLL 为 `NOT_RUN`。

95%配对区间对 source family 做5,000次 bootstrap，基础 seed11050031，各比较另有确定性 seed 记录。问法数不增加事实分母；训练 seed、教师模式、阶段和曝光组分别报告。事实／家族重采样区间不估计训练 seed 变异。A保持同时报告全部 A 在B后相对A后的变化，以及条件于A后已正确事实的保持；条件分母为0时记未定义。通用 LM NLL 为自然对数总损失除15,432个有效目标；区间为描述性结果，没有多重比较校正。

## 8. 成本与审计阅读边界

可训练参数和学生更新预算是控制量。端到端成本还包括教师／学生前向缓存、谱参考、检查点 I/O 和完整自由生成。每规模教师缓存由各臂／seed共享一次，不能当成每臂各自重新做过的教师成本。共用 trainer 对仅 CE 臂仍计算原始 KL 诊断，但其 KL 目标权重为0；实测成本反映这一共用实现，不等于独立优化的 CE trainer 成本。训练段耗时包含在 unit 耗时内，unit 又包含在并行阶段墙钟内，三者不相加。单进程 allocator 峰值不是整节点同步峰值；分配窗口乘卡数也不是账单或纯 kernel 时间。

大权重、缓存、检查点和原始输出都保留在执行侧。[冻结源码清单](../../../originals/experiment/source/source_manifest_amendment_v4.json)、[资料清单](../../../originals/experiment/data_prep/v3/frozen_files_manifest.json)、[READY源码／计划哈希](../../../originals/experiment/resource_transition_20261106/HANDOFF_READY.json)和资产注册表（[包外资料 E022](../../../EXTERNAL_REFERENCES.tsv)）提供复查入口。地址可访问、实际完成、数值效能、机制解释与研究者接受各有独立记录。
