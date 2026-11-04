# 10月31日组会：领域偏向成员的三域复核

**目的：** 数学、生物、物理的领域区分成员，在使用频率和共同谱中是否呈现一致组织？此前三条直觉是：高频成员更常承担区分、近单域成员较低频、不同偏向成员共享谱位置。本轮沿用同一模型与A22字典，用新文档检验这些描述。

**实验已完成，原直觉未得到完整三域复核。** 每域150个新文档家族，60发现、30开发、60留出；每域留出再分30熟悉平台新家族、30新平台。全部450篇，72,000分析位置；450正式＋12工程前向，无训练。以下认识是据实测作出的AI解释，待研究者审阅。

![三域汇报总图](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/figures_A02/meeting_poster_three_domain.png)

## 认识一：领域区分能力不能由出现频率单独概括，“高频富集”依领域而异

结果分析：全16,384成员按文档平均z筛选，任一域≥5篇支持的11,994名进入候选池。偏向域对其余两个域的AUC取较小值，S≥0.75的全部成员冻结：数学129、生物133、物理27。主集合没有根据留出换人。

频率可判成员高频比例为48.8%、27.3%、37.0%，候选池38.3%。数学超过池，生物和物理未超过；三个集合中高频合计仍占多数。三域等权富集差−0.56个百分点，98.333%区间[−3.43,+13.63]个百分点，未确认普遍高频富集。Top16/64/128结果也有变化，不能只选最符合直觉的截取。

![图1：feature参考频率](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/figures_A02/figure1_feature_frequency.png)

读图：每行是成员组，横轴为人数占比，颜色为独立DCLM参考发生率的低／中／高；分母是频率可判人数。生物1名、池395名参考不足单列，不归低频。原阈值0.2593994%和1.3442993%，分母65,536个参考位置。

严格主集合在发现集仅数学f9638一名，为中频；近单域仅2/5/1名，合并5低频、3中频。但后者数学和物理不足每域5名，尚不能推广“单域成员总体更低频”。支持型零异域但未过S的成员26/30/11另存，不替换本次主集合。

## 认识二：领域偏向可以不同，谱位置仍有大量重合；前偏程度依领域对与参考谱而异

结果分析：同一批单位decoder在主参考谱的前64份额均值为数学14.71%、生物15.91%、物理7.72%；中位数为8.52%、14.00%、6.15%。在新三域D共同谱则为14.39%、15.66%、20.23%。物理变化很大，因此不能说所有领域的区分成员都稳定集中在谱前端。前64只占6.25%维数；相对前偏与大部分长度在前段是两件事，后960维仍占84–92%。

![图2：同名单，两套共同谱](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/figures_A02/figure2_spectral_position.png)

读图：横轴PC谱段按数据方差从大到小，每段64维；纵轴单位decoder在该段的平方投影份额，成员等权平均，左右均为0–25%。灰虚线6.25%为维数参照。左右只变参考谱，不换成员。该图展示几何朝向，不能说真实激活能量或知识含量更高。主参考固定R10；新三域PCA作稳健性，未事后互换。

三个领域对逐PC重合为数—生0.906、数—物0.825、生—物0.804；相应匹配背景中位数0.913、0.859、0.844。因此共享谱位置是可见描述，尚没有高于字典背景的特殊重合。预定综合指标区间跨零，稳健复核未确立。

![图3：三个领域对重合](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/figures_A02/figure3_pairwise_overlap.png)

读图：每个小图放两组平均谱曲线，灰色是每段两者的较小份额。标题同时给逐PC和64PC分段重合；分段掩盖内部差异，不能用更高的分段数字代替逐PC数字。谱位置重合不等于方向、功能或语义相同；跨成员绝对余弦均值仅0.025–0.028。

## 认识三：有限文档里的零响应不能固定为全局领域专有性，稳定偏向可以伴随跨域复用

结果分析：原7数学／9生物严格成员，在新物理留出中16/16有正激活，12名达到≥5篇、≥2个平台；没有一名维持三域严格标签。唯一新发现严格成员数学f9638，在新三域留出激活文档为33/1/1篇，仍偏数学但已非严格单域。各域分母均为60篇，按z>0保留所有弱正值。

![原16逐成员复核](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/figures_A02/appendix_legacy16_H.png)

读图：行前的领域是旧冻结标签；三列是新数学、生物、物理，每格数字为激活文档数/60。看右列，16名都有跨域反例。新严格组1/0/0无法计算三个域对的重合，报告NA，不填零。f9638前64几何份额42.46%是单成员描述，不概括“严格成员普遍前偏”。

### 证据4：哪些真实token承载响应？

![图4：激活token频率和跨域可用性](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/figures_A02/figure4_token_composition.png)

读图：左边是激活位置上的token低／中／高频组成，右边是跨域共用、D单域和支持不足；每名先计算再成员等权。底行是全部有效位置背景。feature频率来自独立DCLM，token词频来自新D，不能混用。D词频按类型分位数为1次/2次/≥3次；H在D未见者单列灰色，不能当低频。

数学／生物／物理高频token比例75.4%/58.0%/71.2%，同激活文档暴露背景75.1%/68.9%/71.6%。因此数学、物理的高频占比很大程度随文档中本来常见的词出现，不能直接称特殊偏好。

f9638激活1,150次、35篇、434种token：共用63种(14.5%)对应436次(37.9%)；D单域14种(3.2%)对应58次(5.0%)；其余357种/656次支持不足。主要token包括换行58次/8篇、「 of」52/17、「 the」46/18、逗号27/13、「 a」23/11，以及「 prime」13/7。类型数和事件数必须分别给分母。“D单域”是出现记录，不自动等于专业术语；“共用”也不自动等于领域语义。

### 证据5：固定the后是否还有上下文关联？

![图5：同词面、来源格式匹配后的响应](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/figures_A02/figure5_same_token_context.png)

读图：目标固定ID279「 the」，还匹配前一token、位置、文体、边界、已读前文公式标记和来源平台。纵轴为组与域对，横轴偏向域减对手域的平均z差，区间按独立文档对重采样。数—生15对、数—物18对、生—物20对；六个组级差均为正，说明相同目标词面下仍与不同自然语境相关。

前文术语、主题和句法还会变化，故当前证据削弱纯目标身份解释，尚未识别纯领域语义。固定面板全零者标覆盖不足。预定例子包括两边都零的成员，不按结果补漂亮案例；只用已读前文解释即时响应，后文另存事后描述。纯换词B、物理受控跨措辞、长短程机制尚未回答。

## 留出检查与五项回答

数学在新平台留出只有24.0%达到S≥0.75，低于预定至少50%；熟悉平台67.4%。生物66.9%/51.9%、物理77.8%/85.2%分别通过来源层。不能用合并均值或更换成员救回数学来源失败。新三域与旧两域还同时改变了样本、来源和评分对手，不能将差别单独归因于物理。

1. 频率：主集合以中高频为多数；高频富集不是三域通用规律。近／严格单域总体趋势不足。
2. 谱位置：数学、生物均值前偏；物理依赖参考谱，且均值不等于多数成员。
3. overlap：三对谱位置重合大，低于匹配中位数；严格组不足，无法回答其跨域重合。
4. token：响应跨多种真实token，常见词、格式和本批偏域词并存；机会背景已报告。
5. 上下文：固定the后保留自然语境关联；语义因果、纯identity与长短程未决。

## 组会可能追问

**为什么这次检验比重画旧16有信息？** 450篇新原作家族、完全独立的新来源留出、全字典对称S筛选，让旧零响应标签和新三域排序均能遭遇反例。原16保留不换人。

**为什么不能据高重合直接设计MoE或称相同功能？** 投影只保留平方长度，丢失符号与方向组合；相同谱位置可以有很小余弦。当前没有任务收益、干预或训练对照，方法收益没有被测量。

完整依据：[三域结果与全部边界](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/summary_A02_cn.md) · [完整方法与核查](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/detailed_A02_cn.md) · [16名逐成员token清晰表](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/legacy16_tokens_A02_cn.md) · [预定同词面实例](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/context_examples_A02_cn.md) · [冻结名单、全部统计、映射与复现](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/reproduce_A02.md)。旧两域报告已另存历史文件，未混入当前分母。
