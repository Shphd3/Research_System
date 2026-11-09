# Detailed：A17_04_E01 R02 单层 AdamW 条件映射迁移

主Anchor：[条件映射迁移](../../../../../../problem_anchors/17_shared_and_interference_learning/17_04_conditional_mapping_transfer/17_04_conditional_mapping_transfer_anchor.md)。Protocol：[本轮合同](protocol_cn.md)，版本 `a17_04_e01_r02_single_layer_adamw_v1`。Summary：[结果摘要](summary_cn.md)。当前执行状态：`ENGINEERING_COMPLETE; REGISTERED_ACCESS_PASS; BOUNDED_EXPOSED_DEV`。研究者机制判断和下一科研决策：`Unknown`。

## 0. 结果速览

目的：旧规则已经学会后，只改变新模式的口令—位置对应关系，检验共享更新何时保留或损害旧规则。局部优化器干预另问实际更新的方向、幅度和moment作用。

**实际结果：同向继续训练保留旧规则；反转新规则学会后，旧任务准确率三个顺序全部降至0%。共同训练仍可让同一单层四矩阵同时处理旧新两套规则。** 合并DEV三顺序均值：同向旧CE0.00004081、准确率100%、规则优势+23.14596；反转旧CE15.81921、准确率0%、优势−15.79310，反转新CE0.03135015、准确率99.25%、优势+16.18983。joint旧/新准确率99.833%/99.667%，八分项gate全部通过。

主对比E三值−38.38544/−41.28473/−37.14703nat，均值−38.93906，样本SD2.12368；负效应不只是相对少收益，反转旧CE、准确率、优势均发生绝对损害。原生概率分解显示主要损害发生在候选内部的正确选择，而非候选词总体概率消失。

工程资格：Smoke pt-022fae06和Full pt-x0czuelx均SUCCEEDED；九分支全1200步、216000训练答案、72实际Full状态和72原生读数/115200记录出现；七遥测tag、exact恢复、42冻结文件、实际资产登记strict通过。Full34局部干预与独立审计通过。

资格/边界：`BOUNDED_EXPOSED_DEV`，三个顺序共享一个旧端点。描述性结果支持当前设置下关系依赖的保留代价；研究者机制判断/正式结论仍Unknown。joint额外旧监督且新曝光减半，不是分开专家收益实验。Probe排除简单“只把SGD放大就更好”的解释，但未识别AdamW长程成功的唯一原因。

## 1. 对象与计算

| 对象 | 白话含义和实际构造 | 用途与边界 |
|---|---|---|
| 旧模式一 | 甲取首项、乙取末项 | 已学会规则；旧评估始终不改标签 |
| 同向新模式二 | 甲仍取首项、乙仍取末项 | 模式改变，预测映射可复用 |
| 反转新模式二 | 甲取末项、乙取首项 | 新完整输入和同向相同，只翻转标签；模式可见，因此不是同一完整输入的不可满足矛盾 |
| joint_reversed | 每步10旧答案加10反转新答案；同五列表、两口令两模式 | 联合可行性对照；额外旧标签且新曝光减半，不能当等监督分开收益比较 |
| 未见排列 | 熟悉三个词换成训练中没有的排列 | 与未见组合分别汇报 |
| 未见组合 | 训练中没一起出现过的三个熟悉词 | 不是未见词；两面板各400答案，等权合并 |
| CE | 正确答案负对数概率，nat/答案 | 降低不保证正确答案压过错误词 |
| 规则优势 | 正确端点相对相反规则端点的对数概率差 | 衡量是否会选；全词表准确率还需排除第三个竞争词 |
| 实际更新 | 优化器操作后四矩阵逐元素相减 | AdamW位移不能直接替换为负梯度 |
| 继续训练种子 | 29、43、71控制新阶段列表顺序 | 三者共享一个旧端点，不能作为独立旧学习重复 |

## 2. Anchor 衔接与决策点

早期E01旧规则没有学好，不能可靠回答“学到新规则是否损害已有旧规则”。E03给出单层Q/K/V/O加AdamW能学会的旧端点。本轮保留中性口令与列表，只把迁移起点换成实际已学会的端点。它能测当前共享更新在两种任务关系下的保留代价，不能直接决定专家何时分开。

原E01 Protocol和结果保持历史身份。本记录仅拥有R02；问题关闭和后续架构选择由研究者决定。

## 3. 冻结、执行符合性与偏离

冻结时间2026-10-11 16:10:08.549730UTC，共42文件，含双语合同快照、源码、配置、数据、父模型/旧状态身份。冻结清单SHA256 `accb6e360d935278dfa2bbdd3a27e776896eea46482a4730cb7580db97136950`；英文冻结Protocol SHA256 `dc1da949870f36bbb50f41d2b04e28833c7a748219b4b046d85a80972e515a21`；迁移配置SHA256 `5bb5754ce2f8622ec31265a605f6563c1021950c42b70f0d884a414faeeddc1d`。

| 注册项 | 预定 | 实际及资格 |
|---|---|---|
| 授权/合同 | 当前单层迁移+小probe；保留原E01历史 | 本轮双语owner快照和版本匹配；无未授权新增条件 |
| 数据/监督 | 原TRAIN/DEV，无TEST；新prefix/order/答案边际匹配 | data guard及actual consumed rows核验PASS；DEV已暴露 |
| 旧状态/四矩阵 | 共同AdamW1200、6291456；其他冻结 | 九分支step0四tensor逐元素一致；旧四cell均100%；frozen byte/version PASS |
| 优化/目标 | freshAdamW、clip1、micro5acc4/20答案 | 旧moment未carry；Full每步真实20target与7tags通过 |
| Full预算 | 三顺序×三branch×1200步 | 九分支全部完成，共10800update/216000target；无适应延长 |
| Smoke/恢复 | 三branch×3步、各外进程1→2 |180target、另60replay；四权重/optimizer/RNG/metric/counter全exact |
| 保存/输出 | Smoke9state/Full72state |81实际状态；Smoke5与Full11资产登记/current strict通过 |
| Probe | Smoke5/Full34独立条件 | 完整执行，norm最大误差2.13057e-5；no-op全zero |
| 主分析 | E、绝对变化、资格/可比gate/joint | 原analyzer72state载入及115200原生记录核验PASS；独立logit审计PASS |
| 不可变性 | 冻结42文件 | freeze_end_verification PASS42；源码/数据/合同快照未改 |

修正与偏离：冻结前小面板文字算数统一为40记录/world、80旧新合计，源码一直按每panel10列表；裸CPU测试曾因未source既有runtime的protobuf环境失败，使用已有环境变量后资格通过，无依赖变更。冻结后无合同amendment、GPU重试、条件排除、缺失保存或训练延长。事后输出错误类别计数及示例选择属于明确标记的描述补充，未替代主E或新确认。

数值边界：训练/迁移读数保留native FP32 CE，候选进入量由FP64 lognormalizer计算。两者相减时，接近零的候选内选择CE可能出现约1e-7的小负值，这是精度差，不是负损失或功能收益。独立审计观察到nativeCE与FP64 logp最大差3.87e-6，小于冻结2e-5阈值；原始值保留，不剪裁。

## 4. 实际设置与来源

模型为28层Qwen3-0.6B Base。只训练第27层Q/K/V/O权重，Q2048×1024，K/V1024×1024，O1024×2048，总6,291,456。Q/K norm、其他attention参数、前层、MLP、embedding、最终norm和lm_head冻结。FP32、native SDPA、eval无dropout、确定性、禁TF32；不缓存会受Q/K/V训练影响的依赖。

输入资产：model_qwen3_0p6b_base_official_a5、tokenizer_qwen3_0p6b_base_official_a5、data_a17_conditional_mapping_v1、adapter_a17_04_single_attention_20261011t145214z_full_attn1_adam_main。小干预还用注册SGD main240与E02 neutral TRAIN/DEV。实际成员和当前访问由root artifact manifest及execution provenance登记。

共同旧状态是E03 AdamW Main update01200/state.pt，SHA256 `48595673c24579164e271cfeb1b86be6a234e2dfc06218b74d8ca07e16411b75`。只加载四权重，明确重置旧Adammoment/RNG/counter。各分支重新seed、fresh optimizer、本阶段计数归零；已有旧24000答案另记。分支内恢复则须完整恢复自己的状态。

原数据每世界TRAIN2400条/1200列表，DEV800条、两未见面板各400。列表成甲乙对。同向/反转新训练每步前文、顺序、答案词边际相同。旧新复用底层列表为控制内容，完整输入因模式不同而不同。DEV以前已暴露，本轮无新的确认集，不加载TEST。

只计算“答案：”后的一个答案词元。20有效答案/步，micro5×acc4，四次SUM各除20；无前文/填充损失、正则或辅助项。AdamW lr1e-4、betas(.9,.999)、eps1e-8、decay0、foreach/fused=False、恒定LR；四矩阵统一global norm clip1。

每主分支1200步/24000新答案；六主分支共144000新答案。三个joint加72000总答案，其中36000旧/36000新。Full九分支总216000拟合目标。Smoke180目标，外部恢复另60；已有旧训练、固定状态梯度、评估/probe不混入正式新曝光。

保存/评估0、1、16、50、120、240、600、1200；含四权重、完整Adam/RNG/schedule、target/update/cursor/order、parent/config/data/frozen身份。独立单卡worker为DP1，四卡不把每步有效答案乘四。

资源单节点四H10080GB reserved，镜像shphd-lite-0911，7200秒/job。Smoke GPU0/1/2各一分支，GPU3probe；Full GPU0/1/2各一种子顺序跑三分支，GPU3完成34条件。实际拓扑和receipt核对资源，名称不能替代事实。

复用adapt E03四矩阵native训练/恢复/TB与E01配对world reader；不继承O-only恢复、原TEST加载、tiny训练、SAE/LoRA/专家。source/IMPLEMENTATION.md及configs/cpu_qualification.json记录实际复用决策。

## 5. 指标与注册判断规则

旧输入x正确答案y、相反端点o，规则优势为 \(m_A=\log p(y\mid x)-\log p(o\mid x)\)，即logit差，单位nat。M按固定旧DEV、口令与面板等权平均。每个继续顺序：

\[
E_s=\Delta M_{A,s,\mathrm{reversed}}-\Delta M_{A,s,\mathrm{consistent}}.
\]

两边都减同一旧端点。E负表示反转相对同向更不利，不等于绝对损害。分别报3个E、均值、样本SD、min/max、两面板及等权合并。三E全负且均值≤−.01为描述性约定，不是统计显著性。

旧起点和最终新任务分别要求四个口令×面板cell准确率均≥80%；反转新margin还要确实上升，才能解释学到新规则的影响。旧CE/准确率/margin绝对变化另比起点，材料量约定.005nat、1个百分点、.01nat。joint需旧新八cell均≥80%。

可比学习水平取首次保存的四新cell均≥80%点；同向可step0已合格，必须保留。它是共同最低资格，不是严格相同准确率或路径。

候选集合S的CE精确分为进入损失−logP(S)与候选内选择损失−log[p(y)/P(S)]。配合规则margin和全词表准确率，避免把候选词增概率叫作规则学会。配对口令/模式坐标是精确输出描述，不是参数机制。

Probe用Base、SGD240、AdamW240三个固定状态，两批各20旧TRAIN目标、80固定旧DEV目标。条件为no-op、nativeSGD、nativeAdamFresh、SGD缩放到AdamFresh长度、AdamFresh缩放到SGD长度；AdamW240另加nativeAdamCarry与Carry缩放到SGD长度。每条件恢复原权重/moment，Full34、Smoke5。实际四矩阵位移δ定义：

\[
\Delta L_R=L_R(\theta+\delta)-L_R(\theta),\qquad R_{\mathrm{finite}}=\Delta L_R-\langle\nabla L_R(\theta),\delta\rangle.
\]

余项含非线性和残余精度差，不能单独断言原因。相等位移长度不匹配1200步历史。norm match误差≤1%；native CE恒等式误差<2e-5nat。

## 6. 证据链

| 认识 | 注册标准 | 原始证据/计算 | 观察和资格 |
|---|---|---|---|
| 已会旧规则 | 起点四cell≥80% | step0state/原生eval | 四cell100%，PASS |
| 关系改变保留 | 合格新任务下三E全负、均值≤−.01 | 两主branch配对端点、primary_contrast | 均值−38.93906nat，全部负；支持描述性相对代价 |
| 绝对旧损害 | 旧CE/acc/margin比共同起点 | endpoints/原生记录 | 反转旧CE+15.81852、acc−100pp、margin−33.31776；三读数均实际损害 |
| 候选解释 | access/choice及margin | 逐样本概率分解 | 反转旧访问+ .00877、选择+15.80974nat，主要为选择损害 |
| 新规则确实会 | 新四cell≥80%、margin上升 | qualification/原生new endpoints | 三反转全合格，new margin平均+32.22485 |
| 联合可行 | joint八cell合格 | joint endpoints/fourway | 全PASS；fourway100%/99.5%/98.25%，监督/曝光不同 |
| 优化器局部作用 | same state/source、actualδ、norm/cosine/ΔCE | probe真实payload/independent audit |34条件PASS；方向/幅度/history均有状态依赖影响 |
| 工程/资产 | 完整保存恢复/冻结/遥测/current strict |72state审计/登记receipt | 全PASS；科学范围仍单旧端点/暴露DEV |

原始证据完整入口：[主分析](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/results.json)；[独立mapping审计](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/independent_mapping_audit.json)；[Probe审计](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/optimizer_probe/full/independent_audit.json)。三继续顺序只刻画固定旧端点条件下的路径差，不提供独立旧模型的不确定性。

## 7. 主迁移结果

以下每行是一个真实1200步端点，CE单位nat/答案、margin单位nat、准确率来自全词表。两种未见分别及等权合并；每种子每面板旧新各400答案，合并各800。所有old baseline相同；同向新baseline准确率99.875%，反转新0%，因此同向主要是强化已有映射，并非从零学新规则的对称难度比较。

### order_new

共同旧起点：CE 0.00127738，准确率100.00%，规则优势+17.772339。

| 顺序 | 分支 | 旧CE | 旧准确率 | 旧margin | 新CE | 新准确率 | 新margin |
|---|---|---:|---:|---:|---:|---:|---:|
|29|consistent|0.00006588|100.00%|+23.49333|0.00006418|100.00%|+23.27145|
|29|reversed|15.68115433|0.00%|-15.68097|0.00013121|100.00%|+16.19936|
|29|joint_reversed|0.00066337|100.00%|+18.01054|0.00210712|100.00%|+16.21053|
|43|consistent|0.00007171|100.00%|+24.01831|0.00008870|100.00%|+23.69150|
|43|reversed|18.04170294|0.00%|-18.04156|0.00016271|100.00%|+18.32382|
|43|joint_reversed|0.00986870|99.75%|+19.17451|0.00546464|99.75%|+16.77371|
|71|consistent|0.00003527|100.00%|+22.58500|0.00005406|100.00%|+22.27763|
|71|reversed|14.98203873|0.00%|-14.88023|0.12231636|97.00%|+15.22662|
|71|joint_reversed|0.00451493|99.75%|+17.52288|0.01617212|99.25%|+15.24384|

### combination_new

共同旧起点：CE 0.00010468，准确率100.00%，规则优势+17.276967。

| 顺序 | 分支 | 旧CE | 旧准确率 | 旧margin | 新CE | 新准确率 | 新margin |
|---|---|---:|---:|---:|---:|---:|---:|
|29|consistent|0.00003465|100.00%|+23.12525|0.00001572|100.00%|+22.86536|
|29|reversed|14.47183299|0.00%|-14.47133|0.00043789|100.00%|+15.01100|
|29|joint_reversed|0.00086448|100.00%|+17.81123|0.00105215|100.00%|+15.16046|
|43|consistent|0.00000892|100.00%|+23.58619|0.00000606|100.00%|+23.25453|
|43|reversed|16.92403853|0.00%|-16.92340|0.00029296|100.00%|+17.24498|
|43|joint_reversed|0.01004807|99.75%|+19.07236|0.00617058|99.75%|+15.83166|
|71|consistent|0.00002839|100.00%|+22.06770|0.00001717|100.00%|+21.74756|
|71|reversed|14.81447115|0.00%|-14.76112|0.06475976|98.50%|+15.13319|
|71|joint_reversed|0.00308751|99.75%|+17.04616|0.02368015|99.25%|+14.68096|

### combined

共同旧起点：CE 0.00069103，准确率100.00%，规则优势+17.524653。

| 顺序 | 分支 | 旧CE | 旧准确率 | 旧margin | 新CE | 新准确率 | 新margin |
|---|---|---:|---:|---:|---:|---:|---:|
|29|consistent|0.00005027|100.00%|+23.30929|0.00003995|100.00%|+23.06840|
|29|reversed|15.07649366|0.00%|-15.07615|0.00028455|100.00%|+15.60518|
|29|joint_reversed|0.00076393|100.00%|+17.91089|0.00157963|100.00%|+15.68549|
|43|consistent|0.00004032|100.00%|+23.80225|0.00004738|100.00%|+23.47302|
|43|reversed|17.48287074|0.00%|-17.48248|0.00022783|100.00%|+17.78440|
|43|joint_reversed|0.00995838|99.75%|+19.12343|0.00581761|99.75%|+16.30268|
|71|consistent|0.00003183|100.00%|+22.32635|0.00003561|100.00%|+22.01260|
|71|reversed|14.89825494|0.00%|-14.82068|0.09353806|97.75%|+15.17991|
|71|joint_reversed|0.00380122|99.75%|+17.28452|0.01992613|99.25%|+14.96240|

### 主对比与绝对损害

| 面板 | E29 | E43 | E71 | 均值 | 样本SD |
|---|---:|---:|---:|---:|---:|
|order_new|-39.174297|-42.059870|-37.465231|-39.566466|2.322288|
|combination_new|-37.596576|-40.509583|-36.828826|-38.311662|1.941778|
|combined|-38.385436|-41.284726|-37.147029|-38.939064|2.123679|

三panel所有E均负，均值远超−.01描述阈值。反转旧平均CE比起点增加15.81852nat，准确率下降100个百分点、margin下降33.31776nat；同时新margin平均增加32.22485nat。因此当前影响不是“少修复”，而是旧规则实际丧失。它不证明所有任务反转都如此。

### 首次新规则合格点

| 顺序/分支 | 保存步 | 总/新答案 | 旧CE/准确率/margin | 新CE/准确率/margin |
|---|---:|---:|---|---|
|29/consistent|0|0/0|0.000691/100.00%/+17.5247|0.002756/99.88%/+16.0350|
|29/reversed|120|2400/2400|5.360900/2.88%/-5.2348|0.125393/96.00%/+5.3643|
|29/joint_reversed|240|4800/2400|0.050897/98.50%/+9.2351|0.072754/98.00%/+7.7939|
|43/consistent|0|0/0|0.000691/100.00%/+17.5247|0.002756/99.88%/+16.0350|
|43/reversed|120|2400/2400|5.285163/2.50%/-5.1767|0.109601/96.62%/+5.2495|
|43/joint_reversed|240|4800/2400|0.042722/98.50%/+9.3520|0.092443/96.75%/+6.9561|
|71/consistent|0|0/0|0.000691/100.00%/+17.5247|0.002756/99.88%/+16.0350|
|71/reversed|240|4800/4800|7.885022/2.75%/-7.7300|0.153205/95.12%/+8.0192|
|71/joint_reversed|600|12000/6000|0.005058/99.88%/+14.2557|0.219132/93.12%/+10.3064|

同向全部step0已过四cell门槛；反转29/43在step120，71在step240。此门槛读数仍见旧受损，但学习难度、初始熟练度和路径没有被完全匹配。joint对应读数只是补充，不是同预算主比较；最终旧新八cell均≥98.5%，three四模式口令同时全对比例100%/99.5%/98.25%。

### 输出上的共享响应与条件差异

| 顺序/分支 | a1旧 | a2新 | C平均响应 | K模式差异 | 四条全部正确 |
|---|---:|---:|---:|---:|---:|
|29/consistent|+23.30929|+23.06840|+23.18885|-0.12044|100.00%|
|29/reversed|-15.07615|-15.60518|-15.34067|-0.26452|0.00%|
|29/joint_reversed|+17.91089|-15.68549|+1.11270|-16.79819|100.00%|
|43/consistent|+23.80225|+23.47302|+23.63763|-0.16462|100.00%|
|43/reversed|-17.48248|-17.78440|-17.63344|-0.15096|0.00%|
|43/joint_reversed|+19.12343|-16.30268|+1.41037|-17.71306|99.50%|
|71/consistent|+22.32635|+22.01260|+22.16947|-0.15688|100.00%|
|71/reversed|-14.82068|-15.17991|-15.00029|-0.17962|0.00%|
|71/joint_reversed|+17.28452|-14.96240|+1.16106|-16.12346|98.25%|

口令均衡使旧M=a1，同向新M=a2、反转新M=−a2；C=(a1+a2)/2、K=(a2−a1)/2。反转端点a1和a2一起为负，表现为旧新模式的口令响应一起翻转；joint则a1>0、a2<0，表现为按模式区分映射。输出坐标的精确恒等式不是参数模块或方向因果机制。独立审计从原始logit重算72文件/115200记录及466011标量，最大代数误差3.77e-15，PASS。

### 具体样本与事后错误归类

选取seed29列表“红 黄 猫”，甲口令，红为首项、猫为末项。下面每行的期望答案由可见模式和分支映射决定，红/猫没有固有正确或错误身份。样本是事后按“起点答对、反转后旧答错、joint后旧答对”筛选，仅帮助解释，不能估计发生频率。

| 阶段 | 世界/模式 | 正确答案 | 实际预测 | p首项 | p末项 | margin |
|---|---|---|---|---:|---:|---:|
|old_start|old/1|红|红|0.99999876|8.9285774e-08|+16.23142|
|old_start|consistent/2|红|红|0.99998824|4.0021251e-07|+14.73126|
|same_end|old/1|红|红|0.99999901|2.8717369e-08|+17.36576|
|same_end|consistent/2|红|红|0.99999844|3.1520116e-08|+17.27264|
|reverse_end|old/1|红|猫|2.1545547e-06|0.9999899|-13.04792|
|reverse_end|reversed/2|猫|猫|6.201953e-07|0.99999103|+14.29322|
|joint_end|old/1|红|红|0.99999987|6.773877e-09|+18.81019|
|joint_end|reversed/2|猫|猫|1.3060646e-06|0.99999276|+13.54848|

事后错误类别计数另显示：反转29/43的旧错误全部选相反端点；71旧合并97.5%选相反端点，1.5%中间词、1%列表外，正确0%。因此old0%不能独自推出“所有样本只翻转端点”。这份计数不是注册主指标或新确认。

[逐样本示例](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/illustrative_sample.json) · [事后错误分类](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis_posthoc_rule_choice.json) · [原生全轨迹表](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/trajectories.csv) · [完整模式坐标表](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/mode_command_trajectories.csv)。

### 训练轨迹图

![旧新规则轨迹](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/figures/transfer_trajectory.png)

上排为旧模式，下排为新模式；三列为答案CE、全词表准确率、正确相对相反端点margin。横轴是每步20总答案的继续更新次数；joint每步仅10新答案。颜色区分同向、反转、joint，曲线是3继续顺序均值，阴影是最小到最大范围，不是置信区间。图中反转新模式学会时旧模式丧失，joint经早期损害后旧新同时恢复。图源为冻结规则下的原生轨迹CSV，rendered PNG已检查标题/图例/坐标未截断。它是连续读数描述，不能将曲线形状直接归因为特定参数模块。

[图来源](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/figures/provenance.json)。

## 8. 阶段证据与失败分解

CPU、Smoke、Full训练、Full独立分析、probe、输出登记和当前strict均PASS。Smoke pt-022fae06；Full pt-x0czuelx于2026-10-11 16:30:49UTC完成（北京时间10月12日00:30:49）。Full72完整状态实际载入检查四权重/Adammoment/计数/shape/dtype/finite，七遥测与实际批次计数通过。冻结42文件前后不变。81实际Smoke/Full状态登记为12adapterfamily及4analysis/probefamily。

被削弱解释：旧起点没学会、反转新任务仍不会、只因列表候选概率降低、这两套映射在该四矩阵范围一定不可共存。仍开放：为何只训练新模式时更新没有保留旧模式条件区分，哪些参数更新分量导致跨模式响应改变，以及等监督/参数/计算下分开是否有收益。joint控制改变监督与新曝光，不能完成后三项因果裁决。

## 9. 完整本轮记录

1. 问题：旧规则已会后，反转是否改变共享更新保留代价？probe只问局部更新作用。
2. 设置：一个AdamW1200旧端点、单层四权重、freshAdam、三继续顺序/三分支；主比较其他条件固定。
3. TRAIN：模式二同前文、标签互换；joint显式10旧+10新。
4. 评估：两个已暴露DEV面板分别及等权合并，无TEST/新确认。
5. 结果：九Full分支全完成；同向保留旧、反转旧0%、joint旧新接近100%；34probe完成、81实际状态/16资产strict通过，完整值见主结果和probe表。
6. 认识/边界/决策：获得关系依赖的实际保留代价及条件兼容实例，未证明分开架构收益或参数机制；本轮有限授权完成，科研下一步Unknown。

## 10. 解释与结论边界

观察：关系标签改变后，新任务学会且旧规则实际损害，joint则旧新均合格。派生：E和CE分解把关系代价与候选适应区分。AI解释：共享参数的预测作用是否有益取决于更新能否维持可见条件之间的区分，映射不同本身不等于不可共享。研究者机制裁定仍Unknown；没有定位参数级必要机制。

可说：此任务、共享旧端点、单层四矩阵/freshAdamW和预算下，反转相对同向造成稳定旧margin代价，并实际破坏旧预测；同一模型范围在joint监督下可共同学会两模式。不可说：反转必然冲突、分开专家有益、参数模块已识别、AdamW长程底层原因已查明、三个独立旧重复、自然文本迁移或新确认。

## 11. 下一决策

科研下一步Unknown，待研究者评估本轮结果。当前授权训练、分析、保存和实际登记均完成；未新增架构、SAE、数据或训练预算。

## 12. 资产与复现入口

Execution root：/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer。Run：runs/transfer_20261011T160256Z。root拥有[artifact manifest](artifact_manifest.json)。实际输出ID及current strict见Smoke/Full登记receipt；全部来自真实保存，不用计划当资产。

| 资产 | 作用 | 身份/完整性 | 当前资格 |
|---|---|---|---|
| 双语owner快照 | 合同/边界 |42文件freeze | 已冻结 |
| config/freeze | 参数/不可变输入 | SHA见上；42文件endcheck | PASS |
| old update1200 | 共同权重 | 上文stateSHA/注册family | 输入访问PASS |
| CPU资格 | 实现检查 | configs/cpu_qualification.json | PASS，非科研结果 |
| Smoke receipt | 工程执行身份 | pt-022fae06，2026-10-11 16:10:25UTC提交 | SUCCEEDED，工程PASS |
| Smoke输出 | 9state+原生读数/5probe条件 | smoke_registration_receipt.json；5资产 | REGISTERED_ACCESS_PASS |
| Full states/readouts | 主证据 | pt-x0czuelx；实际72state/72读数 | REGISTERED_ACCESS_PASS |
| Probe payload | 位移/有限变化 | 实际34条件；results/manifest/独立审计 | REGISTERED_ACCESS_PASS |

[Protocol](protocol_cn.md) · [Summary](summary_cn.md) · [Run配置](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/config.json) · [Freeze](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/freeze.json) · [实现说明](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/source/IMPLEMENTATION.md)。

复现worker先source runtime.sh，再运行transfer.py --config CONFIG --run RUN --seed SEED --branch BRANCH --phase smoke|full|resume_verify。需授权H100环境，不是重新提交指令。analyze.py只读已保存结果，不训练模型。

## 14. 已完成的局部优化器干预

以下是独立固定状态干预的实际结果，主迁移和局部干预均已完成，实际输出登记/current strict通过。每一行都从同一组原状态恢复；不能把34行连成训练轨迹。SGD与Adam的source批次相同，收受读数是80条固定旧DEV。表中的Δ为after−before，CE/访问/选择用nat/答案，margin用nat，准确率为全词表。

数值核验PASS：34条件、6状态批次、54原manifest条目、40读数文件/3200记录出现、17152标量，最大复算误差3.55e-15，normmatching最大相对误差2.13057e-5，低于1%阈值。六组no-op严格零位移/相同读数。审计没有重新模型forward/backward；它检查保存证据的一致性。

### base

基线CE 2.48594952，候选内选择CE 1.05783763，准确率 31.25%。

| 批次 | 条件 | 实际位移范数 | ΔCE | Δ进入CE | Δ选择CE | Δmargin | 更新后准确率 |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | no_op | 0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | 31.25% |
| 1 | sgd_native | 0.01000000 | -0.08928511 | -0.09512305 | +0.00583794 | -0.00009819 | 30.00% |
| 1 | adam_fresh_native | 0.24970120 | -0.34151231 | -0.36363134 | +0.02211903 | +0.00196093 | 38.75% |
| 1 | sgd_direction_adam_norm | 0.24970120 | -0.65049217 | -0.90394093 | +0.25344876 | +0.00634164 | 40.00% |
| 1 | adam_direction_sgd_norm | 0.01000004 | -0.01555123 | -0.01545294 | -0.00009830 | -0.00003591 | 31.25% |
| 2 | no_op | 0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | 31.25% |
| 2 | sgd_native | 0.01000000 | -0.08887200 | -0.09738725 | +0.00851526 | +0.00060871 | 30.00% |
| 2 | adam_fresh_native | 0.24976435 | -0.33157214 | -0.38150294 | +0.04993080 | +0.00366417 | 35.00% |
| 2 | sgd_direction_adam_norm | 0.24976435 | -0.61713265 | -0.90427491 | +0.28714226 | +0.01214031 | 31.25% |
| 2 | adam_direction_sgd_norm | 0.00999993 | -0.01536337 | -0.01652385 | +0.00116049 | -0.00000131 | 31.25% |

### sgd_240

基线CE 1.12111264，候选内选择CE 1.06732633，准确率 41.25%。

| 批次 | 条件 | 实际位移范数 | ΔCE | Δ进入CE | Δ选择CE | Δmargin | 更新后准确率 |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | no_op | 0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | 41.25% |
| 1 | sgd_native | 0.01000000 | -0.01346762 | +0.00170648 | -0.01517409 | +0.00176554 | 40.00% |
| 1 | adam_fresh_native | 0.24971328 | +0.02691839 | +0.01672923 | +0.01018915 | +0.01048062 | 41.25% |
| 1 | sgd_direction_adam_norm | 0.24971328 | +0.97544721 | +0.24170962 | +0.73373759 | +0.04586498 | 33.75% |
| 1 | adam_direction_sgd_norm | 0.01000008 | -0.00439561 | +0.00038841 | -0.00478402 | +0.00044768 | 41.25% |
| 2 | no_op | 0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | 41.25% |
| 2 | sgd_native | 0.01000000 | -0.00454064 | +0.00080609 | -0.00534673 | +0.00146341 | 38.75% |
| 2 | adam_fresh_native | 0.24975745 | +0.06879095 | +0.01136036 | +0.05743059 | +0.01540835 | 40.00% |
| 2 | sgd_direction_adam_norm | 0.24975746 | +1.53273929 | +0.24565940 | +1.28707990 | +0.03777144 | 26.25% |
| 2 | adam_direction_sgd_norm | 0.01000001 | -0.00200071 | +0.00013966 | -0.00214037 | +0.00063355 | 41.25% |

### adam_240

基线CE 0.00922627，候选内选择CE 0.00912325，准确率 100.00%。

| 批次 | 条件 | 实际位移范数 | ΔCE | Δ进入CE | Δ选择CE | Δmargin | 更新后准确率 |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | no_op | 0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | 100.00% |
| 1 | sgd_native | 0.00554498 | +0.00010287 | -0.00000186 | +0.00010473 | +0.02055962 | 100.00% |
| 1 | adam_fresh_native | 0.22784859 | +0.00479873 | +0.00002195 | +0.00477677 | +0.22594852 | 98.75% |
| 1 | sgd_direction_adam_norm | 0.22784858 | +0.76863069 | +0.54020321 | +0.22842749 | -2.64858398 | 85.00% |
| 1 | adam_direction_sgd_norm | 0.00554486 | +0.00007263 | -0.00000085 | +0.00007348 | +0.00961094 | 100.00% |
| 1 | adam_carry_native | 0.02815626 | +0.00082547 | -0.00001789 | +0.00084336 | -0.00516751 | 100.00% |
| 1 | adam_carry_direction_sgd_norm | 0.00554498 | +0.00013241 | -0.00000467 | +0.00013708 | -0.00077660 | 100.00% |
| 2 | no_op | 0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | +0.00000000 | 100.00% |
| 2 | sgd_native | 0.00699001 | -0.00045633 | -0.00000259 | -0.00045374 | +0.03915598 | 100.00% |
| 2 | adam_fresh_native | 0.23073323 | +0.00068687 | -0.00001011 | +0.00069698 | -0.12724063 | 100.00% |
| 2 | sgd_direction_adam_norm | 0.23073321 | +0.36452944 | +0.02498934 | +0.33954010 | -2.89275424 | 90.00% |
| 2 | adam_direction_sgd_norm | 0.00698992 | -0.00010639 | -0.00000076 | -0.00010564 | +0.00277281 | 100.00% |
| 2 | adam_carry_native | 0.03141858 | +0.00021756 | -0.00001819 | +0.00023575 | +0.01923754 | 100.00% |
| 2 | adam_carry_direction_sgd_norm | 0.00699001 | -0.00000563 | -0.00000538 | -0.00000025 | +0.00517023 | 100.00% |

### 可获得的局部认识及边界

1. 只放大SGD步幅不足以解释或修复长程失败。Base两批放大SGD的ΔCE为−.65049/−.61713，SGD240却变为+.97545/+1.53274，Adam240为+.76863/+.36453。它反驳“步幅越大越好”的简单解释，没有检验其他SGD学习率的完整训练。
2. Base上更大CE改善仍主要是候选进入：进入CE降低.90394/.90427，同时选择CE增加.25345/.28714。候选词适应仍必须保留为解释，不能以CE改善直接判规则增强。
3. SGD与freshAdam方向余弦约.192—.306；Adam240的fresh/carry余弦.0862/.2104。改变了方向和历史，不只是同方向换步长。当前局部优劣依赖状态、批次和读数，不能据此给出1200步AdamW成功的唯一机制。
4. 平均margin也不足以替代所有预测行为：SGD240批2放大SGD，margin+.03777，CE+1.53274，准确率降至26.25%。margin只比较两个端点，且平均数掩盖个体差异；应继续联合报告CE、规则margin、全词表准确率。

### 一阶预测与有限余项

| 状态 | 批次 | SGD→Adam范数的一阶CE项 | 实际ΔCE | 有限余项 |
|---|---:|---:|---:|---:|
| base | 1 | -2.43499633 | -0.65049217 | +1.78450416 |
| base | 2 | -2.43282950 | -0.61713265 | +1.81569685 |
| sgd_240 | 1 | -0.42982354 | +0.97544721 | +1.40527074 |
| sgd_240 | 2 | -0.18309738 | +1.53273929 | +1.71583668 |
| adam_240 | 1 | +0.00273537 | +0.76863069 | +0.76589532 |
| adam_240 | 2 | -0.02291621 | +0.36452944 | +0.38744566 |

上述较大步长下一阶预测与实际变化有时连符号都不同；应测实际位移和有限变化，不能只用梯度点积。余项定义本身不能分开非线性效应与残余数值差，也没有证明长期机制。

[原始结果](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/optimizer_probe/full/results.json) · [独立核验](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/optimizer_probe/full/independent_audit.json) · [完整读数说明](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/optimizer_probe/full/independent_audit_cn.md)。

## 15. 完成与资产交付

Smoke5资产、Full11资产均实际登记且selected strict通过。Full含9adapterfamily（各8member，72完整状态）、mapping与probe两analysisfamily。Smoke含3adapterfamily（共9状态）、mapping/probe两analysisfamily。adapter必须和注册Base共同加载，不是standaloneLM。不同执行阶段和只读独立审计不能互相替代资格。

[Smoke登记](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/smoke_registration_receipt.json) · [Full登记](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/full_registration_receipt.json) · [当前Full访问](/data/250010109/Research_System/assets/checks/2026-10-11_a17_transfer_20261011t160256z_full_outputs.json) · [72状态实载核验](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/analysis/checkpoint_verification.json) · [冻结核验](/data/250010109/MoE_Router/experiments/20261011_a17_single_layer_mapping_transfer/runs/transfer_20261011T160256Z/freeze_end_verification.json)。

任务完成是执行与证据事实；科研状态迁移、机制确认、下一实验和问题关闭仍由研究者决定。本轮没有commit/push或发布。
