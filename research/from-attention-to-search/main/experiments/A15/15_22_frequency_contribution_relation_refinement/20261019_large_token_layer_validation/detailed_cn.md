# Detailed：大样本与跨层的token—feature频率复核

[Summary](summary_cn.md) · [English](detailed.md) · [Protocol](protocol_cn.md) · [推理审计](reasoning_audit_cn.md)

**结果资格：BOUNDED。** 本轮工程完成、关键计数与来源检查通过；可用于冻结缓存的描述性复核，不能用于独立文档确认或因果/学习判定。研究者科学解释和问题关闭为Unknown。主观察是DCLM位置画像很弱且ID加权反向，而逐feature等权方向为正；不是一个统一的“成功/失败”分数。

## 1. 问题、假设与对象

旧Anchor H1认为当前token越稀有，最低频feature段末层份额可能越高。扩大样本和层范围，检查方向、幅度及加权是否保留。竞争解释为token身份/格式/位置组成、尾部支持和归一化分母。模型固定为Qwen3-0.6B Base及最终14层/F16384 CrossCoder；层2、4、…、28读取block residual-post，末层在最终RMSNorm之前。共享z联合使用全部14层，没有14套独立层内激活。

p是参考侧z_i>0比例；f是同一窗口当前tokenID的频率；s=−log10 f。下一目标不参与。M_low是最低频feature的z乘该层decoder范数后求和；T是全部16384项的同类总和；R=M_low/T。它们不含偏置、均值、残差和向量抵消，不是解释方差、信息量或学习价值。T=0和不可估相关保持NA。命中、命中数及命中数/总激活数由共享z定义，跨层相同。

逐feature辅助指标把每个feature参考稀有程度−log10 p，与其复核命中位置平均当前token稀有程度相关；feature等权。p=0/U或无参考已知token命中的feature退出该相关；≥20次命中是预定支持敏感性，不依据结果选门槛。

## 2. 冻结、实际设置与偏差

执行根E：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/token_feature_layer_validation/20261019T_validation`。phase1根P：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z`。

| 项目 | 冻结/预期 | 实际与资格 |
|---|---|---|
| 授权 | 本会话无训练大样本/跨层复核 | 一次本地CPU执行，无前向/训练/GPU；授权不预确认结论 |
| 方法冻结 | E/provenance/frozen_execution.json，2026-10-19 05:19:00 UTC | 代码SHA256 `0a232e3915b5a26798567f50d5149242d0136ca03e022a4600ce974c8ed6e426`；Markdown随后整理，不冒称结果前人工确认 |
| DCLM | 完整既有窗口10,485,760，D/V沿用phase1 | D5,238,097/V5,247,663；10,249上下文、81块；V41块，无文档独立性承诺 |
| Tulu | 原TRAIN/EVAL，仅补跨层 | 85,548/22,446；256个EVAL对话；已暴露 |
| 频率与名单 | 各参考侧p/f；4个正频log等宽段，零频U | Tulu B1=1694、U907；DCLM B1=314、U353；均完整保留 |
| token分箱 | 正频ID等权分位，method=higher、并列不拆 | DCLM计数阈值[3,7,14,36]；Tulu[1,1,2,4]，第二组空NA |
| 对照 | 固定旧Tulu1694池 | 与本地重估池分开，不把DCLM旧池称本地低频 |
| 统计/区间 | 全层整体rho点估；1000块bootstrap均值/28−2差 | seed20261019；不是整体rho的CI；两层NA集合已核查一致 |
| 保存与元数据 | 10核心表 | 原completion.tables=8属计数字段错误，执行后修正为10，保留修正说明；另3张派生/定义资格表，合计13张 |
| 资源 | CPU8/RSS16GiB/新增盘1GiB/正式30min、总90min | 核心314.8秒、进程峰值RSS4.1574GiB；软guard等实现限制见第8节，不伪称硬隔离 |

解码几何复用`P/decoder_geometry.npz`的norm，形状14×16384。归一化坐标下跨层绝对M不可作为同单位物理幅度比较；同层共同正尺度不改变R。几何SHA256 `b74cc20f563ea535c5b4d05e9f58bb3411f6bd6138d969afe4b25edbe4c28a8e`，父checkpoint保存端SHA256 `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`。phase1 CUDA范数与旧桥梁CPU范数最大绝对差4.7684e−7，属于已保留的FP32归约差异，不称逐bit相同。

输入ID为`representation_crosscoder_qwen3_final14_f16384_val10485760_phase1_20261013t173130z`和`analysis_crosscoder_feature_relation_phase1_20261013t173130z`；Tulu沿用原SFT缓存与桥梁绑定。当前访问、manifest与保存端身份分别负责地址、数据坐标和来源，不代替文档污染检查。没有新checkpoint或优化器；训练batch/步数/学习率均NOT APPLICABLE。

## 3. 决定性证据谱系

| 判断 | 原始/汇总来源 | 操作与观察 | 资格与边界 |
|---|---|---|---|
| 大样本位置画像 | phase1 CSR→[layer_metrics](tables/layer_metrics.csv) | DCLM local层28 rho0.006191；ID等权−0.119041 | BOUNDED；不复现Tulu的幅度或加权方向 |
| 逐feature关系 | 二元命中转置乘已知标记/稀有程度→[完整32768行](tables/feature_token_correspondence.csv)及[摘要](tables/feature_correspondence_summary.csv) | DCLM rho0.336019，≥20为0.339147 | BOUNDED；全部合格feature，非最低池位置预测 |
| 跨层与块波动 | [block_correlations](tables/block_correlations.csv)、[stability](tables/block_stability.csv)、[diagnostics](tables/diagnostics.csv) | 完整14层，块均值及28−2差 | BOUNDED；同z、同bin，非独立层或文档重复 |
| 命中与分母 | [binary](tables/binary_metrics.csv)、[groups](tables/groups.csv) | DCLM local命中0.05294%；层28 M相关约0.006191 | BOUNDED；区分已知token相关分母与全部位置平均 |
| 固定名单迁移 | [members](tables/members.csv)、[migration](tables/migration.csv) | 旧1694与新314交集25；11项新参考零频 | BOUNDED；不能互换低频定义 |
| 测量正确性 | E/provenance/checks.json、code_audit.json、final_numeric_checks.json | Tulu逐位置R与旧值最大差2.5484e−8；DCLM全16384边际相同 | 工程/测量检查，非新科学发现 |

## 4. 主结果：全部14层

下表是本地最低频池的完整逐层相关。总体rho没有CI；不同层共享同一z及位置。

| 层 | DCLM位置等权 | DCLM ID等权 | Tulu位置等权 | Tulu ID等权 |
|---|---:|---:|---:|---:|
| 2 | 0.00619090 | -0.119064 | 0.258395 | 0.116433 |
| 4 | 0.00619132 | -0.119047 | 0.257472 | 0.118361 |
| 6 | 0.00619124 | -0.119046 | 0.256977 | 0.118731 |
| 8 | 0.00619122 | -0.119044 | 0.257078 | 0.119392 |
| 10 | 0.00619105 | -0.119044 | 0.256594 | 0.119301 |
| 12 | 0.00619079 | -0.119046 | 0.256601 | 0.119638 |
| 14 | 0.00619084 | -0.119046 | 0.256588 | 0.119954 |
| 16 | 0.00619086 | -0.119044 | 0.256500 | 0.120242 |
| 18 | 0.00619071 | -0.119044 | 0.256874 | 0.120532 |
| 20 | 0.00619076 | -0.119043 | 0.257332 | 0.121670 |
| 22 | 0.00619086 | -0.119042 | 0.258166 | 0.123168 |
| 24 | 0.00619101 | -0.119040 | 0.258922 | 0.124152 |
| 26 | 0.00619106 | -0.119042 | 0.258935 | 0.124318 |
| 28 | 0.00619124 | -0.119041 | 0.259051 | 0.124371 |

DCLM相关只纳入5,227,462个参考已见ID位置，20,201个未见位置另列；Tulu分别19,070与3,376。DCLM B1的314项中283项参考命中<20；Tulu B1的1694项全部<20。[members](tables/members.csv)保留其余三段，不能把高支持feature总体结论当成尾部314项的可靠性保证。

逐feature等权方面，DCLM≥1命中可估15,928项，rho0.336019；≥20可估15,749项，rho0.339147。Tulu对应14,610项/0.374516和10,220项/0.119556。DCLM参考零频353项、无已知token复核命中393项；Tulu907和1753，两集合可重叠，不能相加当总排除数。逐feature正相关与DCLM位置弱/ID反向可以同时成立，因为它们先平均的对象不同。

[支持资格表](tables/feature_level_support.csv)进一步限定最低段：DCLM314项中211项有参考已知token复核命中，仅34项达到20次；Tulu1694项中对应962项和2项。旧报告Tulu1198项复核命中包含参考未见token，故不与962冲突。≥20逐feature正结果主要来自其他频率段，不能挽救最低段位置R的弱关联。

## 5. 分组、命中与幅度分解

下表全部来自层28、本地池。token组按各自参考计数定义，不能把DCLM最低组误写成只出现1次，也不能把≥37写成旧≥5。四段份额和命中率的单位均为%。后三段行中的命中字段在源表重复的是B1命中率，**不是该段自己的命中率**。

| 语料 | 参考token计数 | V/EVAL位置数 | B1/B2/B3/B4平均份额（%） | B1任一命中（%） |
|---|---|---:|---|---:|
| dclm | 未见 | 20,201 | 0.001167 / 1.064537 / 22.076090 / 76.858205 | 0.2525 |
| dclm | 1–3 | 47,138 | 0.002643 / 0.684750 / 21.183217 / 78.129393 | 0.1931 |
| dclm | 4–7 | 70,584 | 0.001352 / 0.625595 / 20.584375 / 78.788668 | 0.1233 |
| dclm | 8–14 | 122,368 | 0.000574 / 0.642611 / 20.048659 / 79.308164 | 0.0858 |
| dclm | 15–36 | 267,536 | 0.000691 / 0.776598 / 19.566390 / 79.656327 | 0.0890 |
| dclm | ≥37 | 4,719,836 | 0.000634 / 0.605671 / 20.926419 / 78.467274 | 0.0467 |
| tulu | 未见 | 3,376 | 0.246805 / 2.248937 / 32.182878 / 65.317154 | 39.9882 |
| tulu | 1 | 1,278 | 0.265518 / 2.576698 / 31.435001 / 65.722430 | 35.9937 |
| tulu | 空组 | 0 | NA / NA / NA / NA | NA |
| tulu | 2 | 761 | 0.253490 / 2.526590 / 30.475861 / 66.743910 | 32.4573 |
| tulu | 3–4 | 1,112 | 0.273441 / 2.644351 / 29.442871 / 67.639124 | 29.0468 |
| tulu | ≥5 | 15,919 | 0.047309 / 2.109321 / 31.235304 / 66.607344 | 8.0533 |

DCLM local全V的零R比例99.94706%，非零条件平均R28为1.25684%；Tulu零比例83.68529%，非零条件均值0.66156%。DCLM最低token组命中率0.19305%，最高组0.04674%；但命中后R均值分别约1.36888%与1.35675%，接近。条件均值见[事后算术派生表](tables/group_conditional_means.csv)：由既有组均值除命中概率得到，无缓存重读、拟合或新检验；decoder范数全正、全层zero_R=1−anylow已核验，空组仍NA。

末层稀有程度相关分别为：DCLM any/count/fraction=0.006193/0.006193/0.006189，M_low=0.006191，T=0.325661；Tulu=0.256699/0.257504/0.249807，M_low=0.260185，T=0.194053。主方向不是只在R这个比值里出现，但这些相关不能分解身份、格式和上下文的因果比例。

## 6. 波动、层差与迁移

DCLM每层41/41个V块可估、37块为正。层28块均值0.007473564，95%描述区间[0.004662572,0.010107547]；层28−2的配对块均值差6.7059e−7，区间[4.3177e−7,9.3306e−7]。即使该描述区间未跨零，差值也极小，不是强层机制或实用价值。

Tulu每层227/256对话可估、212为正、29个NA；层28对话均值0.255917856，区间[0.231403684,0.280123058]。28−2差0.002044106，区间[−0.000280917,0.004935049]。两个语料/两个池的2与28层NA集合均一致，配对资格由`final_numeric_checks.json`确认。区间对应等块/对话均值，不对应总体rho。

固定旧Tulu池在DCLM的层2→28位置rho为0.168926→0.157293，ID等权−0.222496→−0.218740；仅25项属于本地B1，Jaccard0.012607，11项进入U。其全V命中率33.8020%，末层平均R0.551933%，也不能称这些成员仍是DCLM最低频feature。Tulu本地与旧池完全相同，属于定义一致性，不是另一次复制。

预定位置诊断仅检查位置<16与≥16。DCLM末层rho约0.010671与0.006137；Tulu0.277395与0.255251。Tulu代码用答案内位置，DCLM用输入上下文位置；二者含义不同，不合并解释。它没有控制token身份、来源或完整格式。

## 7. 图怎样支持阅读

![完整跨层相关](figures/figure1_layer_correlations.png)

图1来自layer_metrics与block_stability。上方比较位置/ID等权总体rho，下方为等块/对话均值及描述区间。它显示DCLM极弱位置方向和反向ID加权在全层一致；不提供独立层确认，也不允许给总体rho附上下方区间。

![四段末层份额](figures/figure2_r28_token_band.png)

图2来自groups，按当前token参考频率组列出四段平均R28，未知与空组单列。B4仍占大部分幅度，最低段绝对份额很小；不证明低频内容主导输入。原空组为NA，不用零填。

![命中、幅度与分母](figures/figure3_binary_contribution.png)

图3来自layer_metrics、binary_metrics与groups。它把份额、低频绝对幅度、总幅度及二元命中分开；DCLM这些最低池指标的整体相关都很弱，分母本身相关较大。它不建立因果分解或分类效用。逐feature结果另见完整表与其摘要，不能从此位置图读出同一个估计量。

![逐feature频率与命中token稀有程度](figures/figure4_feature_level_correspondence.png)

图4来自feature_token_correspondence及feature_correspondence_summary，仅呈现既定≥20已知token复核命中的支持口径。横轴是参考feature稀有程度，纵轴是其命中位置的平均当前token稀有程度；每个点是feature，绝大多数不属于最低频段。DCLM显示ρ0.339147、Tulu0.119556，不能读成位置可靠性或最低314项专门获验证。

## 8. 工程完成、异常与未测内容

核心执行成功，无失败回执；扫描339个含V行的既有缓存chunk，逐文件SHA核对，读取8,531,540,850字节；V非零事件1,336,496,568，全部16384边际计数与原phase1相同。先前全部640chunk绑定/连续性、索引、D/V块计数与来源小文件另经只读审计。CPU独立行求和检查3位置通过；Tulu复现逐位置R和rho通过。不能把3位置直接求和测试说成全部位置独立重算。

核心耗时314.8126秒，记录进程峰值RSS4.1574GiB，未用GPU/新推理/训练。该时间不是总交付墙钟或CPU核秒，RSS不是整机峰值。10张核心表+3张派生/定义资格表（合计13张）；原计数8→10仅改元数据，未改冻结代码或核心指标。

审计状态PASS_WITH_LIMITATIONS。主要工程限制：guard按周期检查RSS和时间，长操作间不是硬上限；磁盘1GiB没有冻结代码强制检查；异常退出线程池可能等待已提交任务；DCLM中途结果没有可恢复checkpoint，失败只保留traceback；写文件非原子。原始DCLM bin与大checkpoint未在本审计重hash，使用保存端身份、当前size/mtime与小型索引核对；Tulu CSR未被审计重复加载/hash，沿用已有绑定及本次逐位置末层复现。这些限制如实保留，本次无失败且实际资源低于预算。

未测：独立原始文档复核、分类精度/召回评估、语义真值、因果干预、学习loss、专家效用、其他模型与独立单层编码器。协议曾要求保持的U仍在完整分母，但未输出独立U幅度表或分组幅度分位数，不能声称已测。条件均值仅是事后算术派生。

## 9. 本轮记录、解释及唯一下一问题

2026-10-19这一轮：问题为旧H1的样本/层稳健性；设置是冻结相同模型和字典，参考侧定义池，复核侧测三种权重；数据是同bin D/V及已暴露Tulu；结果是上述有界关联与敏感性；认识更新是“逐feature联系”与“少见token的可靠最低池画像”应分开。DCLM未复制旧Tulu位置相关强度，也不支持加权不敏感的对应；逐feature描述性正方向保留。人类科学裁决Unknown，旧Anchor/Focus保持不变。

**唯一AI建议问题：这种逐feature正关联，在按原始文档隔离的数据上，控制格式、来源和位置后能否保留？** 完成当前交付即停止；下一问题是否激活、何种控制和资源均由研究者决定，不自动训练或补跑。

## 10. 完整产物与复现入口

研究侧保存本双语Summary/Detailed、协议/审计、一页说明、13张小源表及静态图；执行侧E拥有code/analyze.py、code/plot.py、provenance/frozen_execution.json、source_identity.json、checks.json、code_audit.json、final_numeric_checks.json、completion.json及日志。核心代码hash见第2节；输入manifest/checkpoint/norm身份见source_identity与code_audit；各源表hash及行数由code_audit.small_table_output_consistency绑定。新增条件表由code/finish_checks.py生成，身份与范围见final_numeric_checks。feature_memberships.csv导出两个语料全16384项的冻结分组定义（32768行）；feature_level_support.csv只连接已保存feature表与名单作支持资格计数，均无缓存重读或新检验。

核心表行数：feature_token_correspondence32768；feature_correspondence_summary4；members10；migration2；layer_metrics56；binary_metrics4；groups840；block_correlations8316；block_stability56；diagnostics20。全成员位置输出留执行侧，不把原缓存复制到研究仓库。图的格式、来源及hash见figure_manifest；最终交付manifest由本轮交付登记负责。

没有job提交ID、训练checkpoint、optimizer或外部同步；这些项目均NOT APPLICABLE。当前分析不得按复现入口自动重跑；本轮执行已完成，后续只读现有结果。
