# 最新补充：区分成员与严格单域成员的频谱

[本次Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/summary_cn.md) · [逐成员表](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/evidence/member_spectrum.csv) · [数据资格](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/data_gate_cn.md)

## 新增认识：整体谱重合不代表严格单域子集也高度重合

**领域偏向不同的成员可以处于相近谱位置，但这种整体规律不能直接推广到本批严格单域子集；后者的谱位置更不均衡，其特殊性还受到支持量匹配的限制。** 这是旧两域缓存补统计提出的认识更新，不是三域新验证。下方保留前版token／频率汇报作为历史结果，不替换名单。

结果分析：整体数学433／生物527名的逐PC重合0.949，在相应匹配范围0.947–0.958内。严格数学7／生物9名为0.652；全120篇分域支持匹配为0.656–0.702，仅略低于下界，且参照多次抽回原成员，不能作强分离结论。64PC合并后为0.969／0.800，不能用较粗结果替代逐PC。

![两域谱分布重合](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/evidence/figure4_overlap_with_support_audit.png)

读图：横轴越靠右越相似，点是观察值；灰条为发现支持匹配，橙条为全120篇支持匹配，均是条件字典抽样95%范围而非文档置信区间。纵轴两行的分母不同，分别433／527与7／9。

## 新增认识：严格数学的谱前部更突出，但“前偏”不等于“字典中特别”

结果分析：首64维份额，整体数学10.03%、生物11.52%；严格数学36.33%、生物16.30%，中位数42.46%／16.56%。严格数学7名均高于6.25%维数占比。PC1仅0.206%／0.069%，前偏主要在PC2–64。严格数学36.33%在发现支持匹配下超出参照，但全120篇支持匹配后到达上界，特殊性依赖背景条件。

![同一谱上的方向分布](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/evidence/figure3_domain_spectra_clear.png)

读图：横轴每段64PC，纵轴为组内成员等权平均的单位decoder平方投影份额。两图纵轴范围不同，按刻度比较。虚线6.25%只表示维数占比。这不是乘激活后的真实贡献能量；首段占比最高也不是全部长度的多数。严格数学其余960维仍占63.67%。

组会口述：**“能区分领域，不代表在共同谱上占不同位置；但最严格的单域使用子集并没有复现整体的高度重合。严格数学成员的方向更集中于前64维，生物较分散；是否超出字典背景仍受支持匹配影响。我们还不能把它解释成专有知识或功能模块。”**

追问一：为何需背景？成员少、频率和文档支持不同都会改变重合；不能直接用0.949与0.652的差证明单域性造成分离。追问二：为何还不能说物理验证一致？合格450篇清单未完成；新增前向0、物理结果NOT RUN。来源候选已清点，保留原配额，不凑数。

---

以下是此前已交付的token与频率结果，名单和分母继续按各段定义。

# 合并简图：单域使用、feature频率与激活token

[English](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/pooled_simple_20261030/README.md) · [原R10完整结果](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/summary_cn.md) · [发现集冻结补充](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/supplement_near_domain_tokens_cn.md)

## 认识更新

**在原频率规则下，近单域和本批严格单域成员都以低中频为主；但单域使用不等于只响应单域词面。严格单域成员也响应两域共用token，而激活位置中的高频token占比与语料背景接近，尚不能称特殊偏好。**

目的：把用户截图第二条结论画成可直接读懂的比例图，并回答严格单域成员响应多少种共用或本批单域token、激活token有多常见。数学、生物合并后每名成员等权。所有图只用缓存；科研接受Unknown。

## 结果分析一：feature自身的发生率

![合并feature频率](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/pooled_simple_20261030/figure1_pooled_feature_frequency.png)

横轴为独立DCLM参考激活频率组，纵轴为feature人数比例，柱顶同时标比例和人数。左图原近单域55名，频率可判定52名：低21（40.4%）、中28（53.8%）、高3（5.8%）。右图本批严格单域16名，频率可判定14名：低4（28.6%）、中9（64.3%）、高1（7.1%）。支持不足3/2名保留另表，不算低频。

参考频率=独立DCLM中原生z>0次数/65,536，至少20次；原切点0.259399414%和1.344299316%，相等归低一组。该规则下中频最多，不能把“中频”当所有分组规则下的不变标签；旧log敏感性仍保留。

三份名单必须分开：①近单域55（31数学+24生物），发现集偏向域≥5篇、另一域≤1篇、≥95%正激活位置来自偏向域；②发现集严格单域29（14+15），发现集另一域零激活，旧留出仍严格21名；③**本批严格单域16（7+9）**，从29名中要求全部120缓存文档的另一域60篇、9,600分析位置均零激活。16是本次追加的描述性子集，不替换55或29。

“全缓存严格”只指本批分析位置，不能称全语料领域专有。它用到了开发及旧留出，因此下面不是独立留出泛化证据。没有按频率或token图再挑成员。

## 结果分析二：响应多少种token，各占多少位置？

![token类别数量与激活位置](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/pooled_simple_20261030/figure2_strict_token_categories.png)

两图均为严格16名，在旧留出40篇×160位置=6,400位置观察原生z>0。左图对不同token ID去重，纵轴为种类比例；右图先在每名feature内算位置比例，再对16名等权。两种百分比的分母不同，不能互换。

| token类别 | 不同ID数／1,182 | 种类占比 | 成员等权激活位置占比 |
|---|---:|---:|---:|
| 两域共用 | 108 | 9.1% | 33.1% |
| 本批单域 | 48 | 4.1% | 8.6% |
| 其他／支持不足 | 1,026 | 86.8% | 58.3% |

“常用”在此落实为可核对的“两域共用”，不是凭词义判断。**本次新描述分类**使用全部120篇输入：两域各≥5篇出现为共用；一域≥5篇且另一域0篇出现为本批单域；其余为其他／支持不足。单域类别会包含子词、数学符号和格式，不能自动称领域术语。精确ID、标点、大小写和空格均保留。[逐token表](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/pooled_simple_20261030/token_ID_details.csv)可查看具体词形与两域文档覆盖。

这套全缓存分类与前版“发现集冻结、偏域允许另一域≤1篇”的分类不同，旧结果不重写、不直接拼接。它回答当前语料内的覆盖，不能作为独立语义验证。其他类别尚不能判断，也不能全部叫通用或领域专有。

同文档暴露量匹配背景，共用42.7%、本批单域5.2%、其他52.1%；全部可用位置背景为43.3%/5.2%/51.5%。共用位置有激活不等于对共用词富集；本批单域8.6%相对背景5.2%是描述性组成偏移，尚无语义或因果认定。

## 结果分析三：激活token的低中高频组成

![激活token词频](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/pooled_simple_20261030/figure3_activated_token_frequency.png)

横轴为token语料内频率组，纵轴为成员等权激活位置比例。数学、生物合并；同一16名，原生z>0。低频14.1%、中频9.3%、高频76.6%。

词频计数沿用原R10：在全部120篇有效19,200位置上统计同一tokenizer的精确ID，按token类型计数分位点1、2分组，计数并列不拆分。低=出现1次，中=2次，高=至少3次。“高频”是本批类型分组，不是日常语言或全语料常用程度。类型数与位置数见[token频率表](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/pooled_simple_20261030/token_frequency_composition.csv)，此图纵轴分母为激活位置，不是token类型数。

全部可用位置的高频token占77.1%，与激活位置76.6%接近。因此“激活大多发生在高频token上”成立，但“特别偏好高频token”尚未建立。feature的DCLM频率与这里的token词频是两个不同变量。

## 原高响应阈值对照、方法变化与复现

原发现集正激活p90阈值没有改变；作为单独[高响应词频图](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/pooled_simple_20261030/appendix_high_token_frequency.png)及[高响应类别图](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/pooled_simple_20261030/appendix_high_token_categories.png)保留。16名中12名满足原≥5高响应位置、≥2文档的构成支持，4名支持不足不换人。12名高响应对应243种ID：共用61种（25.1%）、本批单域15种（6.2%）、其他167种（68.7%）；成员等权高响应位置比例35.5%/14.1%/50.4%，低中高词频12.4%/7.9%/79.7%。原生激活与高响应不能混用分母。

本轮变化明确为：数学/生物合并；追加全缓存零异域16名描述子集；全缓存token覆盖分类；新增原生z>0的全激活视图。旧发现名单、分类、阈值与结果全部保留。presentation_amendment.json记录了新增全激活主视图与旧高响应附录的关系。没有新增模型前向、训练、PCA或领域。

原始绘图数据、16名名单、29/55映射、每成员组成、确切token ID及语料计数、输入与输出哈希均在本目录；原始缓存留执行侧。核查包括：16名均属于旧29、全部异域分析位置零激活、高响应计数与原表逐成员一致、ID去重以及比例合计1。脚本为`/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/scripts/pooled_simple_figures.py`，再运行`package_pooled_simple.py`整理稿件；使用本地spectral-hier Python，零模型调用。

汇报追问：**为什么能区分“数量多”与“偏好”？** 比较激活位置和全部可用位置的组成，并保留同文档背景。**为什么不能说领域语义专有？** 单域只在本批中观察到，类别含格式/子词，大量token支持不足，且未进行对象语义人工确认或因果干预。缓存补统计与简图完成后停止。


此前上下文对照与完整三项认识保留在[历史稿](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/history/meeting_brief_crosscoder_domain_members_cn_pre_pooled_simple_20261030.md).


## 逐成员token核查表

严格16名的z>0逐成员总量、前三token及完整Top10现已[单独整理](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/strict16_per_member_tokens_20261030/README_cn.md)，含每token次数与文档覆盖、各成员的三类位置/种类比例。沿用旧留出40篇、6,400位置，不改变正文三张简图；原始次数不直接证明token偏好。


## 后续三域扩展（方案，未执行）

拟数学／生物／物理各150篇全新文档，60发现、30开发、60独立留出；留出再分同平台新原文档30、新平台30。原16名全部迁移测试，另按全字典的较弱域对AUC统一筛选新三域名单。具体支持／修正／不足判据见[完整草案](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R11_three_domain_replication_20261030/protocol_cn.md)。这是待审AI方案，不是新增实验结果；前向和训练均0。
