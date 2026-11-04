# 10月31日组会：领域区分成员的五项分析

准备日期：2026-10-30，北京时间。对象是同一个 A22 CrossCoder 的数学偏向16名、生物偏向16名。它们是**领域区分成员，不默认是领域专有知识**。本轮只读 R04—R09 缓存并补离线统计；新增模型前向、模型／字典训练、新 PCA、距离扩展均为0。原记录没有覆盖。科学接受与问题关闭仍为 Unknown。

先讲五条结论，再按编号读五组主图。定义、全名单、逐成员图和全部统计在[附录](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/appendix_cn.md)。

1. **频率：中高频占多数，具体组名依赖分组。** 原冻结分组下，数学组低／中／高为0／8／8，生物组为3／10／3。合格池8113名本身高频占52.53%；数学组50%没有高于这个组成，生物组18.75%反而较少。换成 R09 log 等宽后变为0／14／2和4／10／2，不能把“高频”当稳定语义类别。
2. **decoder 方向平均偏向谱前部，但不都集中在前部。** PC1–64 的平方投影均值为数学20.55%、生物19.85%，中位数18.96%、14.89%；全字典均值8.85%。数学组超过其精确匹配随机组95%范围上界11.81%；生物组匹配背景因支持不足为NA。数学0/16、生物1/16成员在PC1–64具有超过一半的投影，平均前偏不是“每个成员都主要在头部”。
3. **两域的谱分布相似程度取决于分辨率。** 逐PC重合系数0.7784，64-PC谱段重合系数0.9800。后者掩盖了段内差异。是否高于频率／支持量匹配背景**尚未回答**。它们的实际decoder子空间平均平方主夹角余弦为0.0765，不能把0.7784或0.9800说成方向、语义或功能重合。
4. **真实输入响应跨很多token；与token频率的稳定联系尚未回答。** 每名成员在本面板命中306–2972个不同token ID。激活所在token的面板领域分布与所选方向一致，但这是同一批自然文档的描述。已见token条件下，两种参考发生率的整体Spearman相关为0.022；未见token占8.1%–56.4%，因此不能把这个条件统计当完整关系。
5. **部分成员具有固定token后的上下文响应，不能对全名单作身份归因。** 5/32名达到本轮明确的描述性A类规则；0名分到B类；27名为C类，其中19名在固定目标测试上始终不激活。全零表示覆盖不足。A类削弱纯token身份解释，仍未排除前文术语与主题。

## 统一对象与冻结名单

R04的120篇真实英文文档每域60篇，发现／开发／原留出为30／10／20。每篇192 tokens，先在第33–192位（从0计32–191，共160位，含0）取原生共享激活z的文档均值，再用两域30×30篇文档的排序概率评分。相等计半次。原生最后层贡献幅度只是为每个成员乘固定正数，因此逐成员的排序概率不变。所有文档权重相同，没有把token当独立文档。

沿用R04区分度分析的资格：两域发现集各至少5篇文档有正激活。8113名合格，其中17名评分恰为0.5，保留在背景池、不进入有方向的排名。按距0.5的绝对距离降序、ID升序打破并列，分别截取数学、生物各16名。这与既有自然文档各64名排序的前16一致，但本次16+16汇报截取仍标**探索性**。旧留出已多次暴露，仅作检查。方向固定后的原留出区分度中位数为0.9750／0.9406，最低0.9075／0.8175，没有用于换人。

- 数学偏向，按冻结排序：f8963, f14394, f11163, f14316, f4309, f12351, f3098, f3464, f8030, f7134, f6718, f10937, f11420, f14491, f359, f1382。
- 生物偏向，按冻结排序：f11710, f652, f12141, f598, f8838, f4862, f1010, f14278, f3477, f12266, f734, f13132, f9491, f6289, f15702, f11852。

[冻结回执](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/freeze.json) · [主表：版本、区分度、两域支持、发生率和五项状态](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/master_members.csv) · [旧新名单映射](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/list_mapping.csv)。五图全部保留同一32名，不激活、不复现均不替换。

## 1．这些成员属于哪些激活频率组？

**我们问什么：最具文档区分度的成员是否主要低频，是否超出合格池组成？**

![figure1_frequency](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/figures/figure1_frequency.png)

**读图。** 左列横轴为数学／生物组，每柱16名，纵轴是成员数，颜色为低／中／高／支持不足。右列给同一合格池8113名的组成，使用比例轴避免数量级遮蔽。上排沿用原冻结等数量三分组，下排仅作R09 log等宽敏感性对照。这是成员计数，不是R09全字典均值差贡献。

**证据与一句结论。** 原分组阈值为发生率0.259399%与1.344299%；20次参考命中以下单列支持不足。合格池低／中／高／支持不足=602／3241／4262／8。数学0／8／8、生物3／10／3，均无支持不足。中高频占多数，但数学高频比例与候选池接近，生物偏向组比池中更少高频、更多低频；这些只是组成比较，没有选择流程的不确定性或显著性宣告。

**修正的直觉。** “领域区分成员必然罕见”不符合这份名单；“它们大多高频”又依赖阈值。R09 log等宽阈值0.451726%／6.686506%，数学0／14／2、生物4／10／2；同一池为1345／6128／632／8。

**还缺什么。** 参考发生率是原生共享z>0次数／65536个独立参考位置，既不是强度，也不是谱位置。候选资格和评分会影响组成，尚未说明频率为何形成。[原始计数](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/frequency_counts.csv) · [分组变更](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/frequency_history.json)。

## 2．decoder方向位于协方差谱的哪一部分？

**我们问什么：这32个最后层方向是否共同朝向自然文本高方差方向，均值是否由少数成员主导？**

![figure2_decoder_spectrum](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/figures/figure2_decoder_spectrum.png)

**读图。** 两面板分别16名；横轴为PC1–64、65–128，直到961–1024，共16段。纵轴为单位decoder的平方投影比例，每条浅线是一名成员，实线是均值，黑虚线是中位数。灰点线为全字典16384名均值。数学组灰带是1000个同规模、频率／文档支持量精确匹配集合的2.5%–97.5%范围；生物组保留NA。

**证据与一句结论。** 数学／生物PC1–64均值20.55%／19.85%，中位数18.96%／14.89%。全字典均值8.85%、中位数7.14%。数学匹配背景的均值范围6.73%–11.81%，中位8.71%，低于观察值。生物的f9491位于无法替代的稀有匹配格子，故其“超过匹配背景”尚未回答。最大两名分别贡献各组头段总投影的26.80%／34.39%，并非均值完全由一两名决定；但数学0/16、生物1/16超过50%，仍不能称所有方向都主要位于头段。

**修正的直觉。** 平均前偏是分布形状，不表示每名成员都头部集中，更不等于领域知识集中。**还缺什么。** 单位化去掉decoder长度；这里不乘z、RMS或特征值。所有1024个比例合计1，零范数为0/32。没有测量实际贡献或功能。[逐成员谱表](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/member_spectrum.csv) · [背景支持](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/matched_pool_support.csv)。

## 3．重点：同一协方差谱上的分布重合多少？

**我们问什么：两域成员是否占据相似谱位置，而不是ID是否相同？**

![figure3_spectral_overlap](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/figures/figure3_spectral_overlap.png)

**读图。** 横轴为同一16谱段；纵轴是组内16个单位decoder的平方投影等权平均。两条曲线各总和1，阴影是每段两组较小的份额。图旁同时保留逐PC与合并谱段的重合系数。

**证据与一句结论。** 逐PC重合0.778438，分段重合0.980014。两域有相似的粗尺度谱位置；合并把22.16%的逐PC差异压成约2.00%的谱段差异。未经频率／支持量匹配的1000对全字典随机16+16集合，逐PC重合95%范围为0.7792–0.8078、分段0.9285–0.9797，只能说明很高的粗分段重合也可在普通字典集合出现。由于完整匹配背景NA，本轮不宣告两域重合高于匹配背景。

**修正的直觉。** “两组ID互斥，所以谱空间分开”错误；“曲线几乎重合，所以方向相同”同样错误。附录256对成员绝对余弦均值0.03044，最大f359–f12266为0.97850；两个16维decoder子空间的平均平方主夹角余弦为0.07647，只有第一主夹角余弦很高（0.97934），其余至多0.25187。存在一个近同向或反向的成员对，不能据此说两组整体相同。

**还缺什么。** 主匹配格子使用floor(log2(参考命中+0.5)) × floor(两域发现文档总支持/5)，排除全部32名。f9491参考39次、数学／生物文档支持5／27，所在格要求1名、可用0名。未放宽、未复制、未换人。固定名单的几何量没有选择波动置信区间；随机集合范围也不是这种区间。谱平方丢失符号和组合，不能推出相同语义、计算需求、学习方向或功能重合。[逐PC数据](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/group_PC_overlap.csv) · [256对绝对余弦](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/pair_absolute_cosine.csv) · [实际子空间数值](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/spectrum.json)。

## 4．响应哪些真实token？与token频率有什么联系？

**我们问什么：响应是否局限少数词，两种发生率是否稳定相关？**

![figure4_tokens](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/figures/figure4_tokens.png)

**读图。** 4a固定展示两组发现排名第一名f8963、f11710的高激活、普通激活、同token低／不激活例子；不按谱或测试结果挑换代表。表中保留token ID、字符串、0起算位置与已经读到的前文尾部。完整前文、来源和每名最多每文档2例在附录。4b每点为主名单一名，共32点；横轴为feature参考发生率，纵轴为激活位置上**参考中已见token**的参考频率中位数，误差线为其10%–90%分位范围；两轴取对数。不同成员间相同数值可重叠。

**证据与一句结论。** 120篇×160位=19200个真实输入位置；每名命中306–2972个不同ID，最常见一个ID占其激活位置0.78%–32.34%。f8963在token5322 ` problems`上的一处z=0.16433，另一篇生物文档同ID为0；f11710在token785 `The`上一处z=0.11758，数学文档同ID为0。自然文档没有做严格配对，因此这些只是上下文实例。数学16名激活所在token的面板数学占比中位数均>0.5，生物16名均<0.5；各组再取成员中位数为0.631／0.278。该描述仍受来源、词面和发现选择影响。

**频率关系。** feature发生率分子为该成员z>0位置数；token发生率分子为该token ID在同tokenizer参考中的计数；二者分母恰好同为65536，但计数对象不同。32名的已见token条件相关Spearman ρ=0.02165，按两域自然文档整篇重采样300次的区间[-0.01377,0.04735]。数学组ρ=-0.1001，区间[-0.1605,-0.0507]；生物组ρ=-0.0147，区间[-0.0590,0.0252]，没有一致的正向关联。这些区间只反映固定名单的文档构成波动，未重做成员选择，不能当选择不确定性或独立泛化。

**修正的直觉。** 高频feature不必只响应常见词，领域偏向也不等于只响应某个术语。**还缺什么。** 参考256窗来自254个规范文档组。成员各有8.1%–56.4%激活位置token在参考中未见。它们标缺失并单列，不设伪计数、不把未见当真实零概率。故无条件中位数和完整频率关系**尚未回答**；不能由本面板单域出现称全语料专有。本轮没有decoder到词表的输出词分析。[全部token计数](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/active_token_counts.csv) · [独立参考计数](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/reference_token_counts.csv) · [全部实例](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/real_token_examples.csv)。

## 5．上下文相关，还是主要反映token identity？

**我们问什么：固定当前token后，仅改变领域前文与措辞，响应方向是否仍复现？**

![figure5_context](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/figures/figure5_context.png)

**读图。** 每组冻结前两名作为主面板示例；所有32名见附录，未用成功者替换失败者。横轴为固定token与W0／W1措辞，纵轴为原生z的数学减生物平均差。蓝点是24个发现家族，橙点是12个原留出家族；每家族保留两域配对，区间以整个家族为单位重采样2000次。不同成员的z刻度不可当共同重要性刻度。

**证据与一句结论。** 同一个384位置的R07文本／R08共享z缓存覆盖全部32名，开发12家族也保存在表中。按example W0/W1、explanation W0/W1，有激活的成员数分别为发现11／11／8／8，原留出12／9／7／8，分母都32。13/32名至少在一个条件有激活，19/32名始终全零，保留为“测试覆盖不足”。

本轮先定义描述性读图规则：某一固定目标词的两种措辞，在发现和原留出都沿自然文档选定方向，四个单元的点态95%家族区间都不跨0，每单元至少一域有3个活跃家族，才记A。它是本轮说明标签，不冒充R09原复现标准，不是多重校正显著性。A类为f8963、f14394、f3464、f10937、f652；其中f8963／f3464／f652两目标都满足，f14394／f10937仅example满足。B类要求有受控目标激活且自然响应前5个token合计≥50%、同时不满足A，本次0名；这是词面集中描述，也不证明身份专一。其余27名C，含19名全零和8名稳定性不足。

**修正的直觉。** 固定目标后仍有跨措辞响应的5名削弱纯身份解释；自然文档中很有区分度却在固定目标上全零的f11710不能反过来被判为identity成员。旧R09的36名复现名单仅与本名单交5名（f8963、f14394、f3464、f359、f652），其结论不能覆盖32名；本轮A类5名与这个交集也不是同一批。

**还缺什么。** example换explanation同时改变目标词与结尾，二者差异不能单独证明上下文作用。A类仍可能响应前文术语、主题或措辞；没有因果／功能证据。区间是探索性点态区间，旧留出已暴露。[所有条件与支持](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/context_effects.csv) · [家族原值](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/context_family_values.csv) · [逐成员A/B/C](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/tables/context_categories.csv)。

## 汇报时的两条追问

**为什么这次比较能区分主要解释？** 文档评分先固定领域排序；谱图把激活大小拿掉，只比较方向几何；同token测试再把当前token身份固定。三者回答不同问题，只有最后一项能直接削弱“当前token身份单独决定响应”的解释，且仍保留前文词面竞争解释。

**为什么还不能说领域知识共享、功能共享？** 谱平方投影不保留符号，平均后也丢失成员组合；实际方向／子空间检查与谱分布重合不等价。我们也没有干预、任务性能或学习梯度。本次五项分析完成后停止，不从这些统计自动启动训练、前向或距离实验。

## 交付与缺项

已有结果：R04文档与参考缓存、发现评分和各64名排序、R07自然文本PCA、R08全部共享z、R09还原decoder及旧名单。本轮补统计：冻结16+16汇报截取、两套频率计数、重算的单位decoder分布与重合、可支持的匹配背景、真实token实例／参考计数、32名固定目标效应和A/B/C描述。

**需要新增前向才能补的证据，未运行：** 若要进一步区分C类的词面与上下文解释，需要在本名单实际响应的真实token上做固定token与位置、配对改变前文的测试；现有19名全零和8名不稳定成员没有这项证据。这里仅登记缺项，不设计或执行新实验。匹配格子空缺、参考中未见token属于背景／计数限制，不能靠新增前向冒充解决。

主表、冻结名单、旧新映射、分组历史、全部原始统计表、脚本和哈希均在[材料目录](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members)；[复现与定义](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/appendix_cn.md)。独立重算通过2795项检查，包含AUC、几何、token分母、无未来前文、家族区间、精确匹配与输入未变。图像已目视自检；没有独立听众理解测试，数学只作源文件检查。
