# 详细记录：远近强Attention来源的跨层feature贡献

本记录保存完整证据，报告不是新Focus、Anchor或研究者机制接受。当前用户授权本次R05缓存内补充；旧R04、R05、R06和上轮跨层结果全部保留。数据为反复查看的旧留出，结论边界为探索性观察。

阅读路径：行为及因素控制，本轮未新测输出行为，只固定Attention原配对；表征及层间组织，本轮测共享z的decoder贡献；功能干预与测量质量，本轮无干预，质量由缓存恒等式、聚合及统计核验保护。

## 输入是什么、计算什么

40篇原数学/生物真实文档，各192tokens，原最后block27的16heads、8query位置、每档原始高/中Attention配对。距离不是句长；高是各query/head/距离档的约前10%，中为40%–60%，不是统一绝对概率。分析来源token，不要求query激活同一坐标。

16384个A22feature共用原14层联合输入产生的一个z。每层贡献是z×对应decoder向量L2范数，未激活0。主单位是训练归一化输入空间；原模型空间逐层乘训练TRAIN_RMS。无需实例化语言模型或编码器。Attention不乘入贡献。

量A：每位置按固定频率成员数取平均，包括零。量B：每位置先用组成员贡献范数和除全部四组和，再平均位置；不是汇总分子分母后相除。参考低支持成员也进入份额分母。组成员数不同会影响B，不能用B替换A。成员范数相加也不是合成向量范数。

原统计32:192已审计的逐位置贡献和直接复用，仅从原CSR补算0:32。所有旧160位置重新与CSR直接点积核对，原最后层频率份额与前文端完整组成结果逐文档/分层/档/组复现。输入哈希、decoder尺度与旧核验记录保存在config与sources中；没有新前向。

## 分割、频率与配对

同一DCLM65536token参考激活率，原z>0阈值。hits<20为参考低支持；其余按旧三等分边界保留并列，固定低4469/中4437/高4451/参考低支持3027，不依领域重分组。完整坐标、频率和14层范数在[全成员表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/all_feature_frequency_and_decoder_norms.csv.gz)。

主分层沿用stratum0：来源与query不同tokenID且非标点；其他sameID/标点层没有删除，在完整均值及主量同型附表中保留，但不参与4项正式检验。近远求两档共同query/head，五档求五档共同支持；无支持保持NA。窗口敏感性要求原pair的高和中来源两端均在32:192内后再求共同query/head，不重配对，不放宽规则。

层级权重：同bin/query/head内位置等权；每query内支持head等权；每文档内支持query等权；每领域文档等权。因有效head数不同，不把所有query/head直接平铺平均。配对高和中用原匹配数量；每个事件的文档内总权重公开在[事件原始表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/retained_source_events.csv.gz)。相邻token、heads、feature不能充当额外独立文档。

## 主判据、区间与失败边界

前7实际接口blocks1..13，后7接口15..27（都为0起点奇数block），仅为用户预先划分。先每文档算低频份额后半平均减前半平均，再作高组远−近、再扣中组变化。两域4项统一BH校正。5000次文档bootstrap和19999次双侧signflip；零假设下文档差值符号对称为检验假设，不是随机分配Attention。领域独立抽样，所有层与组保留文档内配对。少于10篇有效文档只给描述均值，不给区间/检验。所有逐层/五档/窗口/其他stratum只作描述，不以某层显著替代主判据。

## 实际证据

[一页结论](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/summary_cn.md) · [主图与读法](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/figures_cn.md) · [4项主量](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/primary4_tests.csv) · [原尺度/训练尺度全部均值](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/group_layer_means.csv.gz)

### 数学

主判据未得到清楚支持；区间和校正结果保留证据不足，不能据此说两者完全相同。高组主量+0.22 [-0.45, +0.93]pp（q=0.8104），扣中组后-0.00 [-0.44, +0.41]pp（q=0.98365）。

高关注低频份额：近处前/后半8.317%/3.528%；远处7.752%/3.184%。

中关注低频份额：近处前/后半9.183%/4.159%；远处8.331%/3.533%。

low固定成员平均训练空间贡献：近高前/后半2.6672065e-05/4.0237042e-05；远高2.5657144e-05/3.442851e-05。这些大小用来检查份额变化是否伴随其他组增减，不构成因果归因。

high固定成员平均训练空间贡献：近高前/后半0.00020467968/0.0010612054；远高0.00021350448/0.0010137288。这些大小用来检查份额变化是否伴随其他组增减，不构成因果归因。

### 生物

主判据未得到清楚支持；区间和校正结果保留证据不足，不能据此说两者完全相同。高组主量+0.21 [-0.49, +0.99]pp（q=0.8104），扣中组后+0.61 [+0.06, +1.19]pp（q=0.2226）。

高关注低频份额：近处前/后半8.292%/4.508%；远处7.990%/4.418%。

中关注低频份额：近处前/后半7.947%/4.525%；远处8.437%/4.618%。

low固定成员平均训练空间贡献：近高前/后半2.6024875e-05/5.7549135e-05；远高2.6013923e-05/5.5962571e-05。这些大小用来检查份额变化是否伴随其他组增减，不构成因果归因。

high固定成员平均训练空间贡献：近高前/后半0.00022606707/0.0010644989；远高0.00023608079/0.0010438634。这些大小用来检查份额变化是否伴随其他组增减，不构成因果归因。

## 真实来源位置算例

展示规则是输入顺序首个合格主配对事件，不按效果选。DOC_biology_02109，query位置164、head0，来源位置157，token片段`Ġ`（解码显示' '），距离7，Attention=6.5690234e-05。

block1：低频成员范数和0.14217406，全部成员范数和3.2084534，相除为4.4312%；若问平均一个低频成员，改除固定4469，得到3.1813394e-05。block27对应份额1.2157%、固定成员均值2.3463154e-05。两个除数不同，回答的问题也不同。单个位置不替代文档检验；[可追溯数值](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/analysis/worked_source_example.json)。

## 竞争解释、缺项与尺度

高/中Attention概率、精确距离、来源绝对位置、前32比例、空白/标点比例全量保留于[诊断表](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/tables/document_weighted_diagnostics.csv)。主stratum非标点，因此标点为0是筛选后属性，不能推广所有来源。其他标点分层另存。结构词只复用上一轮已有词形标注；中间档没有原标注的位置为NA，不当成0，也不新称经过验证的语义角色。

窗口敏感性不等于绝对位置/词面匹配。原文本位置、词面和结构仍可解释差异。原尺度A随层TRAIN_RMS改变，原尺度B与主B逐层完全相同，因为尺度抵消；不能把相同B当新独立验证。固定feature跨层相对轮廓由decoder决定；不同来源条件的曲线变化来自z和成员权重，不是同一feature动态迁层。

缓存内全部适用项已完成；缺新独立确认、词面/位置干预、Attention因果干预，均未在本轮授权中，不补跑。主报告不讨论簇形成或专家分工。研究者机制接受、问题闭合与下一步决定为Unknown。

失败支持保留：same-token-ID的两个原分层在近远共同支持下均没有合格文档，未放宽匹配。五档共同支持的标点层生物0篇、数学6篇；低于预定10篇推断门槛，保留NA区间与均值描述，不拿它补主结论。主stratum0在两域、近远/五档/窗口模式均保留20篇。

## 审计与执行记录

冻结见[protocol](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/protocol_cn.md)与[config](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/config.json)。原输入92个哈希；旧输出不覆盖。新增前向0、训练0、字典0、任务0。无资源申请，无封存TEST读取。[独立计算路径自审计](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/analysis/audit.json)：674项全部通过，包括全事件权重重建A/B、两个真实文档全部192位置的dense点积、旧最后层份额、全部分层共同支持、四检验及BH。独立计算路径不等于独立分析者复核。

技术变更：补入尚无原结构词标注的中间距离档时将该标注保留NA，避免误填0；不改变主指标、成员、配对或支持。没有按结果调整统计阈值或支持规则。三轮事前审计在[pre_run_audits](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/analysis/pre_run_audits.json)，覆盖与交付索引在[data_index](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R05_distance_attention_20261028/crosslayer_frequency_sources_20261028/data_index_cn.md)。

复现：依次运行`python analyze.py compute`、`python analyze.py aggregate`、`python analyze.py statistics`、`python audit.py`、`python render.py`、`python report.py`。脚本从现有execution绝对路径复用原CSR与旧贡献和，无模型调用。便携包包含主统计再计算所需派生值，原CSR/模型不复制；全部源哈希留存。
