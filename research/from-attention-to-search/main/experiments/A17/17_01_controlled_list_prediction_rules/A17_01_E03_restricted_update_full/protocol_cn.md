# Protocol：A17_01_E03 单投影更新 Full

## 0. 审批快照

`APPROVED_FOR_IMPLEMENTATION_SMOKE_AND_FULL`，冻结时结果NOT RUN。研究者于2026-10-10（北京时间）明确采用末层Attention o_proj直接矩阵为主、LoRA为容量对照，授权Smoke→4卡H100 reserved Full→频率→SAE及完整监督，并委托目前共识下的具体设置。下列数值为该授权内的操作选择；机制判断Unknown。[英文精确合同](protocol.md)、[Anchor](../../../../problem_anchors/17_shared_and_interference_learning/17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor_cn.md)、[Focus](../../../../focus/focus_list_rule_shared_update_cn.md)。

## 1. 术语

FIRST取首项，LAST取末项；可见规则使两者可以同时正确。下一答案全词表CE单位nat/答案。顺序未见保留训练中出现的无序内容，组合未见整组内容未出现。after−before负值为帮助；同规则独立接收集改善才算有效来源学习。

## 2. Anchor 对齐

继续现有共享更新问题，固定数据、答案损失和两种未见。改变一个投影只限定更新位置，不证明它只改表层。频率另有Anchor/Protocol；SAE为后续解释阶段。

## 3. 假设

有效首项学习可能损害末项，反向亦然；对手是共享读列表/答案能力帮助双方。全报四个来源接收格、所有预设状态/步长。直接矩阵为主，R8为容量与参数化敏感性。

## 4. 对手解释

数值漂移、无效来源、大步长、饱和、位置难度与低秩瓶颈。相同LR不等于相同功能位移。用实际矩阵变化、全半步、恢复与固定同扰动双reader辨别；三个seed只描述。

## 5. 数据

使用已登记list_rules_v1：4000 train/800 dev/800 test；20个均衡单token中文答案。当前严格核验Base和数据。每seed每规则五批来源、每批20条，每词恰1条；从train独立分层选定，先冻结ID。Full接收集完整800 dev，独立于来源训练数据。来源批可重叠，不当作科学重复。test只在预注册100步终点打开，不选设置。

## 6. 监督

输入到答案标记为止，只监督下一答案token全词表CE；答案在列表内合法，填好答案不能进输入。没有SAE/路由/辅助训练项。

## 7. 模型

Qwen3-0.6B原始Base，28层hidden1024；layer27 Attention o_proj为1024×2048。L直接2097152参数；R8共享rank8，alpha8/scale1，输出因子零初始化、无dropout/bias，24576参数，原矩阵冻结。其余所有参数包括tied head、norm和MLP冻结；原生logits与CE必须精确一致。

## 8. 优化

AdamW LR1e-4、betas(.9,.95)、eps1e-8、decay0、clip1，首步恒定LR无warmup；独立探针plainSGD不改变Adam状态。FP32储存、BF16训练、确定性SDPA、关TF32。每GPU独立轨迹micro5×accum4=20答案/步，首末各10，loss总和除20。100步=2000答案，完成累积才计数。

## 9. 条件与保存

Full：L/R8×seed29/43/71，六轨迹共12000训练答案。保存评价0/2/8/16/32/50/100。update8独立进程恢复，下一步9与连续参考的完整状态/指标精确相同。Smoke：L/R8×17/19，10步，保存0/2/8/10，update0各规则一来源、80条分层dev探针，test关闭。

## 10. 主指标与冻结分析

Full在0/16/100状态、每规则五来源，先FP32计算一次来源梯度，分别从恢复状态施加eta1e-3/1e-2及半步。冻结实际trainable状态并保存有效矩阵ΔW、hash、范数。同一扰动用FP32/BF16读完整800 dev，不能重新计算BF16梯度。R8半因子步未必产生半矩阵步，记录实际值。

主测量为逐记录损失变化，来源×接收规则×未见分项及合并全报。训练seed是独立单位；三个seed报均值、中位数、范围、逐seed，不作总体显著性。FP32为主reader；重复no-op及恢复必须精确。|delta|超过max(1e-7nat,10×FP32 no-op最大逐记录漂移)才标记数值可分辨，这是工程数值底线不是实际收益阈值。BF16分辨的反向符号保留为精度不一致；BF16近零不抹去FP32测量。同规则独立损失可分辨下降才允许解释有效更新的跨规则帮助/损害。来源无效、符号不清、reader矛盾或恢复失败均不足。所有状态/步长保留，不按跨规则作用或test挑选。全半步与范数用来显示非线性/步长对手，不静默删除。

## 11. 次指标与SAE阶段

终点test在协议/配置/源hash冻结后以FP32读取，全报规则×未见与合并CE/准确率；另报dev曲线、正确token概率、ΔW范数及相对阈值1e-5的数值rank。冻结参数起终字节hash一致。TensorBoard七个必要tag见英文§11及observability合同。

已授权后续SAE：原Qwen SAE读归一化MLP输入，接口不匹配，所以同E16设置仅改raw layer27 o_proj output，训练1B实际valid token，Base冻结。SAE执行Agent在该阶段开始前以附加合同冻结精确技术设置和自身Smoke→Full门槛，不改本学习比较。S7匹配嵌入SAE为独立比较，不跨模型转坐标。分析保留原生损失、重构残余、no-op/恢复/随机空间对照；不得用SAE结果选择本test设置。

## 12. 正反例

正确：零LoRA同原生；双reader实际权重hash相同；恢复计数和下一步一致。错误：填入答案、冻结head变化、来源只剩一词、精度改变时重算梯度、丢cursor。易混淆：全对仍有CE、初始输入因子梯度零、BF16零而FP32非零、半因子步非半矩阵步。

## 13. 阶段

严格资产/数据/源码前检→10步新Smoke与独立audit→PASS后六轨迹100步Full→完整事实Summary/Detailed和数值资格表→匹配SAE后另冻结分析。非有限、冻结漂移、计数/恢复错误停受影响轨迹；缺输出保留不足，工程成功不替代机制判断。

## 14. 算法与输出

执行根/data/250010109/MoE_Router/experiments/20261010_a17_projection_full。复用E02答案封装、LoRA、冻结/原子保存/完整resume；改均衡来源、固定双reader与恒定LR；不用旧tiny panel、双精度重算梯度、warmup40、旧平台入口、router/SAE模型训练项。每run冻结code/config/Protocol与数据hash。4H100 reserved单节点、最多四独立GPU轨迹，六臂两波，不跨臂DDP；Smoke timeout1200s，Full7200s，上限8分配GPU小时加平台开销。日志、矩阵、状态、TB在执行侧。实际保存通过registration_request.json交root统一登记，不并发修改catalog。

## 15. 判据

工程PASS需要资产/H100/参数范围/原生一致/冻结字节/有限telemetry/计数/保存hash/独立resume/完整探针。明确违反为FAIL，缺产物为不足。局部科学帮助/损害按来源和数值护栏；无合格格子为不足，不证明不存在共享功能。

## 16. 边界

不证明L/LoRA等价或容量归一优劣、不外推自然预训练、不声称只改表面、完整功能分解、专家必要、SAE普遍有效或三seed总体置信结论。E01整模不同优化设置仅历史参照。

## 17. 冻结与修订

研究者已确认载体/主矩阵/容量对照并授权整个执行顺序；以上具体数值为委托范围内操作选择。A-G一致性PASS，机制Unknown。提交前冻结manifest和scientific body。开始后仅附加状态/链接/记录前后值、理由、可见结果、资格影响的修订；不改E01/E02。允许完整监督和范围内工程修复，不复制live任务。未授权commit/push/发布。

## 附加SAE技术合同：2026-10-10北京时间

独立SAE沿用E16实际设置，改hook及请求预算，新增工程观测/恢复资格。原始Qwen Base冻结eval，读layer27 self_attn.o_proj原始输出1024维；30000原子、ReLU Top32、每步decoder列归一化、无输入减bias/单位归一。DCLM资产dclm_pair_v1：2419训练文件、独立validation；seqlen1024、micro1、DP4、accum1，rawglobal4096。AdamW LR3e-4、betas(.9,.999)、eps1e-8、decay0、warmup10更新后恒定、clip1；AuxK512、dead_after50、权重1/32、norm过滤quantile.999、seed17。保留旧每rank NMSE优化目标，新增globalnormalized重构与冻结LM CE诊断。

每步4092有效下一token位置；过滤后SAEeligible数量另计，旧1B raw不改称1B valid。Full244380更新=1000002960 valid；100M/300M/1B保存更新24438/73314/244380。新增TensorBoard、各rank RNG/optimizer/dead-feature/data-cursor完整恢复。Smoke连续100步参考与60步停→新进程100步必须精确一致。

执行根/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae；configs/smoke.json和full.json、provenance/reuse_audit.json为该阶段依据。SAE monitor owner=/root/historical_question，root按首阶段、频率后交接GPU slot。该附加合同只冻结下游SAE技术阶段，不改已提交更新Smoke或主分析。SAE提交前另存实际stage源/配置/协议hash，真实保存交root登记。

## 附加SAE分析合同：2026-10-10北京时间

在学习Full已RUNNING时记录root委托分析设置，尚未读SAE原子排名/干预结果。这是后续独立stage，不改已归档学习body、来源或主原生指标。

Qwen直接L的29/43/71三个seed，0/16/100全部状态，所有eta1e-3/1e-2及全半步actualΔW，不挑状态。recipient无序content_group按固定hash a17-sae-analysis-v1排序交替分discovery/heldout，配对规则/顺序整组同side。来源batch0–1用于discovery、2–4评价；原来源批可重叠，所以审计跨边record/group重叠，称batch-ID留出而非严格未见source记录。recipient group保持严格留出，不静默更换Full来源。

唯一候选 pooled task-effect space：discovery接收rule×novelty及来源rule均衡，按平均绝对lossweighted signed-atom contribution排名，每个扰动除其实际Frobeniusnorm仅用于排名。top64 decoder列SVD前32方向，不足32如实降rank，留出读出前冻结方向/atomIDs；不预设common/specific语义赢家。对照discovery原生h的PCA及同rank随机空间seed1729/1730/1731。全更新/no-op/恢复；PΔW及补空间原幅度，以及各恢复全ΔW范数的改向分别报告，记录实际Δh范数。FP32基线/全扰动replay须与旧native probe一致，所有rule×novelty测finiteCE及来源护栏。

h0/h1分别编码，保留Δh=D(E(h1)−E(h0))+Δu、lossweighted残余和finite remainder；不能用E(Δh)，不能把空间投影等同输入相关SAE分解，不能丢残余。S7不训练，用匹配raw SAE：相同列表dev原生CE/accuracy与静态/位移；另小DCLM来源+独立validation做工具资格，各自报告不合并跨模型taskperformance。分析Agent执行前冻结实际source/config/observer接口；原生三seed及proxy不足保留。

## 附加分析修订A01：独立virtual来源

root在当前明确委托执行授权下记录；理由是严格source留出，不按有利native符号或test选设置。此前主分析用原Full b0–1发现、b2–4评价；改为另生成严格独立virtualsources为primary，原Full全部矩阵/读出及b2–4干预保留敏感性。学习Full body/来源/更新/指标/确认边界不改，native资格原样；此修订时SAE原子排名/干预仍NOT RUN。

冻结analysis_selection.json位于/data/250010109/MoE_Router/experiments/20261010_a17_raw_projection_sae/configs/，SHA256=720445839a4e9b7d131f8f00507b4de7d8068923ee3fb169f8490e1bd2611405。排除三个seed原发现批0–1全部contentgroup及全部发现recipientgroup。新FIRST/LAST各5批、每批20答案各1；十批组互斥、共110组，两规则来源未配对。两批发现、三批留出干预。recipient发现120/留出120，每novelty20组保留完整双规则记录；完整dev800 native单列。原来源pooled跨seed record/group重叠审计单列。

候选score为|Δz_k(D_k·g)|/实际||ΔW||F平均，仅排名用归一，recipientrule×novelty及sourcerule/batch/eta/fullhalf各等权。top64 decoder列SVD rank32，不足则实际rank；同rank PCA/随机1729/1730/1731、原幅度/恢复全矩阵范数改向双报告。native finiteCE为主，无净伤害入场门槛，保留答案格式/词表概率对手。新增独立virtual矩阵与旧Full矩阵区分保存；消费/执行前需资产/loader/配置来源、runtime Smoke与恢复护栏。

## 附加资格审计A02：真实呈现未见

root在发现100步并未曝光所有名义训练组后授权面板资格后处理。不改训练/来源/阈值/test规则/主指标，不补跑。state0无本轮任务曝光，nominal order_new仅设计属性。0/16/100仅用已完成trajectory record IDs定义真实seen-group unseen-order及unseen-group，virtual source探针不计训练曝光。保留全部注册名义面板和整800主值，新增record/group计数及rule/seed/reader finite重汇总，只作资格审计、不作新预注册主结果。L/R8同seed呈现计划已核验完全一致。实际输出actual_exposure_panel_qualification.json由Detailed链接；qualify_panels.py及hash单独标后处理，不替换冻结runner来源。精确未见科学措辞须遵守此资格。

## 附加提交前selector修复A03：跨角色联合独立

此前A01排除了发现recipient组，但仍可能出现跨角色source/recipient组交集。root在SAE排名/干预尚未读出时批准提交前修复，不改native学习。保留v1，实际用analysis_selection_v2.json，SHA256=c6db6d645d5b260e7bfcd65a46c5236d5ab763c7f5bf435d065e93b72de23d6e。排除全部dev组与旧三seed发现源组，125个候选训练组；十批各20答案均衡记录来自74组、各批组互斥，source/recipient/joint cross-role交集均0。每批7–8无序组，因此20记录及virtual批不当独立科学重复。recipient固定120/120不变。root登记实际prepared selector后再消费。原Full全部矩阵仍为敏感性输入；G独立重算保存，不从ΔW/eta假定恢复。actual FP32扰动、请求/实际差、replay/no-op/resolution与有效来源护栏决定后续分析资格。旧selector/hash保留。
## 附加SAE工程修订A04：独立进程精确恢复

授权：root依据研究者已经明确委托的Smoke→Full执行，在原范围内修复工程问题。此修订只适用于SAE观察器训练，不改冻结的学习Full正文、已保存原生作用、科学来源池及分析selector。首个SAE Smoke `pt-8bnbcqqj`保留为FAIL，不曾据此提交SAE 1B Full。旧trainer归档SHA256为`1844ad3ab0ceceea2db02889a708e73e035a84124f3c37220407bb30c0e0d3bc`；失败证据保留于执行侧`runs/smoke_20261009T174900Z/resume_difference_audit.json`和`registration_request_failure_v2.json`。

实际失败：连续参考与独立恢复在update100有6个encoder权重元素不同（共30720000，最大绝对误差1.862645149230957e-9），以及1个decoder元素不同（共30720000，最大5.820766091346741e-11）。bias、各rank RNG、dead-feature状态、token计数及共同记录的原始JSON指标均一致；Adam矩张量有少量元素不同。即使指标近乎相同，也违反逐字节状态恢复门槛。新进程DDP桶与连续进程已重建桶的浮点归约路径，是可信候选原因，尚未独立证明。旧参考update60恢复槽已被覆盖，第一处状态分歧无法定位。精确门槛不放宽。

此前使用DDP自动同步及桶构造/重建，并把整个恢复payload加载到CUDA。改为纯SAE module：初始全部named_parameter从rank0广播；每次backward后，按固定named_parameter顺序显式all-reduce SUM，再除world_size4，之后执行原有clip与AdamW。恢复payload先加载CPU，保留非capturable Adam step张量的CPU hosting；optimizer加载负责把moment迁至参数设备。DP4、每rank局部归一化重构加AuxK的rank平均目标、E16全部超参、TF32设置、数据流/cursor、过滤、decoder归一化及每rank特征/dead状态均保持。声明的目标与超参相同，但有限精度轨迹可能与旧DDP版本在末位不同。两项工程修复同时实施，不构成定位旧故障单一原因的因果实验。

修订后100步Smoke保留连续参考与60步停→新进程恢复到100步的比较，新增永久保存双方update60/61恢复trace。SAE参数、optimizer、各rank RNG/dead状态/计数必须精确一致，并通过原有原生/freeze/telemetry资格；状态不一致即FAIL，缺比较为INSUFFICIENT，均不得启动1B Full。执行Agent在新提交前重新冻结源码/配置及当前双语Protocol，保留失败版本及全部证据；新Smoke经独立全门PASS后，才自动提交已经获准的1B valid-token Full。实际trace/checkpoint按资产生命周期登记。本修订不改变其他训练或科学边界。

## 附加分析工程修订 A05：直接原生读出恢复

记录于2026-10-10北京时间，依据研究者已有的完整执行及范围内工程修复授权。旧分析`pt-azc2zkl5`已经失败：八个Qwen状态和S7列表状态有完整局部产物，Qwen L/seed71/update100有80份矩阵效果、仅104/960份干预；另S7原生DCLM分支在来源梯度外积核验处失败。旧run与失败记录不改，原生学习Full与频率Full不受影响。

此前S7把原生矩阵梯度与另行分块tail算出的raw输出梯度比较，实测相对误差1.106448e-4超过2e-5。修复工程副本改为：在实际原生raw输出上对完整窗口CE.sum求梯度，另对矩阵独立计算完整窗口CE.mean梯度，再用外积除256核验。2e-5门槛、完整256预测位置、固定窗口、全部64种有限条件、SAE及原生损失定义均不改。分块tail梯度差作为诊断保留；CPU代数通过不能替代真实S7 GPU资格。

此前Qwen受影响状态因20条原生端点与replay CE误差2.026557922e-5超过2e-5而停止，恢复精确、隐藏端点误差较小。现在仅对seed71/update100新建独立恢复run：固定120条留出接收样本全部做完整模型原生before/after/restore；固定矩阵效果也读实际原生端点。逐字节复用旧发现阶段冻结candidate文件及80份actual矩阵，并绑定SHA；不重新排名、不换来源或接收样本、不删失败条件、不改全词表CE指标。实际原生raw梯度加权实际原生端点变化。保存原生相对旧tail的before/after/delta差，以及真实位移相对投影公式的误差。旧tail端点/有限差门槛仍为2e-5/4e-5，超限仍是FAIL，不能为tail机制解释提供资格。原生重复/恢复精确、有限值、矩阵身份及完整条件覆盖只资格化新增的直接原生测量。

本修订时已有结果可见；这是数值reader修复，不是新盲测，也不放宽旧门槛。其余八个Qwen状态及S7列表状态保留归档reader，不静默改称统一的三seed原生reader比较；跨状态综合必须同时报告reader差异。提交前需要CPU正反例/失败路径、独立源码审核、新的source/config/input SHA冻结；终态需要四恢复分片完整合计80矩阵/960干预、S7原生资格或明确进一步失败、真实日志和登记请求。频率分析释放后使用同一已授权单节点4H100 reserved配置，不新增训练、资源回退、科学条件、commit或发布。仅在执行根`engineering/native_repair/`编写工程副本，不改共享冻结分析helper。机制判断仍Unknown。

### A05后续：S7完整原生端点读取器

首个恢复job `pt-czzk7rb3`保留FAILED。四个S7原生来源梯度外积相对误差均0.0，通过原2e-5门槛；后续分块预测端点replay在固定tuple train_w2/eta0.01/multiplier0.5/validation_w3的最大CE误差为2.0806720138821788e-5，未通过。已保存47/64条件仍属partial。这是另一个端点reader故障，不抹去真实梯度修复。Qwen四分片已保存全部80矩阵/960干预，只做CPU完整性检验和导出，不重跑Qwen GPU，也不声称失败父job整体通过。

依据原完整执行中的工程修复授权，另建仅S7恢复：复用完全相同的四个已保存原生矩阵梯度、八个固定257-token窗口、eta0.001/0.01及multiplier1/0.5定义的16个actual FP32扰动。对全部64条件的每个256位置测量完整原生before/after/restore CE，编码真实原生raw输出h0/h1，使用不变的原生raw梯度加权真实位移；不以h0+a delta_W代替实际h1。保存实际矩阵及来源SHA，要求实际矩阵回加精确、上游输入/残差不变、原生重复/恢复精确，以及完整数组均finite。

仅用真实原生h0/h1，在原生完整batch×sequence布局上重放后续计算，作为独立资格核验；端点/有限差门槛仍2e-5/4e-5，超限仍失败。保留旧分块预测h的before/after/delta误差及原PASS/FAIL、完整序列预测h差、投影公式端点/位移误差。直接原生reader通过不能把旧分块FAIL改为PASS。原生符号继续使用max(1e-7,10×精确no-op漂移)。这是结果可见后的reader修复，不是新盲测，不改来源、模型、SAE、损失、扰动、窗口或科学边界。

新工程副本位于`engineering/native_s7_fullseq_recovery/`，旧冻结源码和产物均不变。提交前需CPU正反例/失败路径、绑定全部新源码SHA的独立审核、实际已登记47-of64 partial输入的新鲜strict访问、新source/config/input冻结、上一job真实终态/资源释放，以及同4H100 reserved配置。最终完整性要求64唯一tuple、16实际矩阵、完整256位置signed-code/endpoint/native-effect数组、manifest/request/实际文件集合相等及实际SHA核查。此后续不授权Qwen重跑、新训练或门槛放宽，机制判断仍Unknown。



## 追加分析工程修订 A06：保存数组的均值与最终验收修复

北京时间2026-10-10，研究者明确授权修复、确保所有已授权实验完成，必要时重新提交。`pt-f9dhsb6w`已保存全部64个S7原生条件，但320个数组均值比对中2项失败：GPU float32与NumPy float32的求和路径在存在抵消的线性项上相差3.4106e-12与5.4570e-12。原job保持FAILED，原始测量、原汇总、梯度与旧数值失败全部保留。

在独立CPU恢复目录中，先后核验原275个导出成员SHA，再从保存的逐位置数组以统一CPU float64求均值写入新汇总；最终验收要求与同一计算精确相等，不放宽容差。原生端点/差值门槛2e-5/4e-5、梯度门槛2e-5、64条件/16矩阵/每条件256位置、带符号SAE数组、绝对端点、no-op/恢复及完整文件清单检查均不变。旧chunk失败保留。无重新选feature、无训练与GPU测量变更。

冻结修复源码/配置/Protocol证据，全部验收后登记真实恢复产物。CPU验收修复可完成本阶段而无需新GPU任务；若原测量完整性或原生资格失败，则保留失败并按原资源配置补交受影响GPU范围。所有阶段通过后再进行总体解释，研究者机制判断保持Unknown。
