# 组会总稿：领域区分成员、近单域使用与真实 token

目的：最能区分数学／生物的 CrossCoder 成员，在参考频率、共同谱和真实上下文里如何组织？三个待检验直觉是“区分成员更罕见”“两域分占不同谱位置”“领域偏向来自领域专属词或语义”。模型、字典和原门控固定；本轮只复用缓存。以下认识是观察证据支持的有限解释，科研接受仍为 Unknown。

## 认识更新一：能区分领域与几乎单域使用不同，关于稀疏性的判断须说明选的是哪一组

**结果分析。** R10从16,384坐标出发，发现集至少一域5篇激活、包含零的文档平均z排序概率≥0.75，冻结数学433／生物527名。频率可判定者432／525名，高频占66.7%／54.3%，并不以低频为主。

在同一名单中，以偏向域≥5篇、另一域≤1/30篇，且≥95%正激活位置来自偏向域的发现规则，另冻结近单域31／24名。频率可判定30／22名，数学低/中/高9/19/2，生物12/9/1；比父集合更偏低中频。参考频率中位数0.400%／0.217%。旧留出19/31、21/24仍满足近单域规则，其余保留，不重新选人。严格零异域激活为14／15名，留出仍严格8／13名；它与55名是不同分母。

![近单域参考频率](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/near_single_domain_20261030/figure_frequency_near_domain.png)

**如何读图。** 横轴是父集合／近单域／严格子集／支持池，纵轴是可判定成员人数比例；柱顶为可判定／冻结人数。独立DCLM频率=z>0计数/65,536，原分组切点0.259399%和1.344299%，至少20次。近单域3名参考支持不足，保留另表。log等宽规则下数学多数改称低频，故“中频最多”依规则；不能把组名当绝对属性。

## 认识更新二：领域响应可以不同，而共同谱位置相近；几何与真实使用是不同读数

**结果分析。** 完整960名单位decoder在同一发现集共同谱上的逐PC分布重合0.9493；64PC合并后0.9686。匹配背景逐PC95%参照0.9466–0.9576，实测在其中，未建立超出字典背景的特殊重合。前64份额数学10.03%、生物11.52%，PC1仅0.053%／0.120%，其余前部方向承担主要前偏；两组均落在细匹配背景内。不能仅从前部高就称领域成员特殊。

![完整名单的谱位置与重合](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figures/figure3_overlap_and_use.png)

**如何读图。** 上排横轴共同PC／谱段，纵轴为单位decoder的组平均平方投影；阴影是较小份额。下排固定同一输入域，先对全部组成员z×还原decoder求向量和，再投影平方；它是组贡献向量自身能量分布，不是完整表征方差解释率。数学组在数学／生物文本前64能量51.93%／27.27%，生物组20.88%／49.70%。相近几何与不同使用方式可以并存，不能推出功能相同。

本轮55名另算逐PC0.8303、分段0.9562；相同31/24组规模及频率/支持匹配背景0.8203–0.8459，实测仍在其中。[55名谱图](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/near_single_domain_20261030/appendix_near_geometry.png)放附录。组规模变小会改变平均分布，不能直接与960名0.9493比较而称更分离；未新增55名重构能量。

## 认识更新三：近单域使用不等于词面专属；同词面仍有前文关联，但整组主要成因和领域语义尚未确定

**结果分析：真实激活了哪些 token。** 高响应沿用发现集正激活p90，不改阈值。数学25/31、生物18/24名满足≥5高响应事件、≥2文档的构成支持；各6名留表，不换人。每名先统计位置比例，再成员等权。类别只按发现集输入文档覆盖冻结，留出40篇6,400位置评估。

![图A：哪些token，两域共用还是本语料偏域](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/near_single_domain_20261030/figureA_token_categories_and_names.png)

**如何读图A。** 上排横轴四类token，纵轴成员等权高响应份额；彩柱对照全部可用位置灰柱，黑菱形再匹配高响应所在文档的暴露量。两域各≥5篇出现才称共用；某域≥5且另一域≤1篇才称本语料偏域，均不是语义专属性。

数学／生物的共用份额33.2%／31.7%，本域关联5.4%／10.2%；其他或支持不足61.2%／58.0%。不能把未归类多数当成领域词，也不能说多数是共用词。共用份额并未高于37.0%的全部位置背景。数学本域5.4%与同文档5.1%很接近，生物本域10.2%对2.4%有组成偏移，但这仍非语义证明。

下排按预定份额排名保留前8个真实ID和标点。数学常见` the`、` of`、` a`、逗号，也有`sum`、` =`、`}`；生物有` cells`、` cell`、句点、` the`、逗号。`cells`5.17%来自3/18名，不能代表全部；` Bat`来自一名一篇，保留但不赋予群体含义。菱形还显示生物组`the`高响应份额低于输入背景，常见不能直接称偏好。

**结果分析：同token比前文。** 匹配不使用激活，精确固定目标及前一token ID、体裁、40位置区间与句/段边界；来源层级再固定网站。主词为用户指定、发现集中最常见共用词` the`（279），留出118数学／171生物位置，各20文档。

![图B：同一token不同前文](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/near_single_domain_20261030/figureB_same_token_context.png)

**如何读图B。** 上排横轴为偏向域减另一域的高响应成员比例差；对全部31/24名含零统计，再对文档对等权，线为1,000次文档对重采样95%探索区间。15文档对／24位置对下，数学+1.22百分点[0.43,2.15]，生物+1.39[0.14,3.06]。至少一次匹配高响应者仅6/31、5/24名。再匹配来源仅6文档对／10位置对，保留原the位置8.5%／5.8%，只有一网站；生物区间[0,4.51]触及零，来源解释保留。

下排固定两组发现排名首位，不换成员。f16271同ID在数学前文后z=0.0934、另一前文为0；f1391两边都0，明确覆盖不足。例子只示意，完整匹配支撑统计。总共34个共用ID均尝试匹配，只有5个达到≥5文档对；其他4个的区间均触及零，不能把the图推广成所有token或全部55名的复现。

**认识边界。** 当前token身份不足以解释部分响应；前文术语、主题、格式和来源尚未分离。因此“主要由哪一因素驱动整组”和“是否编码领域对象”尚未回答，不把共用词上的激活直接称领域语义。

## `the`指代对象：已读前文与事后描述分开

已生成全部6,400个前文盲标注窗口，只有随机ID与目标之前的40token。五类为领域术语/对象、领域关系/推理、通用叙述、格式/引用、无法判断。规则提议、反例和人工核查栏保存，人工状态PENDING。初版把术语未命中误当通用叙述；保留旧版并另记v2改为需正面话语证据，否则无法判断。规则标签不是人工语义真值，主结论不使用其比例。

后续名词短语只作事后描述。四种the/The精确ID共333位置，主279有289位置，55名×289=15,895行核查表保留全部前文、z、单列后文和空白对象标签。主ID后续首词223种，其中211次在发现结构未见，48次仅单域≤2篇支持；不能靠后续词给对象判专属性。`set`发现仅数学而生物留出也出现，是反例。**the所指对象是否强领域特殊，尚缺可靠标注；没有把缺标注当成否定结果。**

## 汇报追问与证据入口

**为什么这个比较有用？** 固定当前及前一token，限制位置和体裁后仍有差异，削弱当前词面单独解释；同文档输入背景检查避免把“词本来常见”当偏好。它们不等于配对干预，仍有前文词汇与来源的竞争解释。

**为什么还不说领域语义或功能？** 语义对象尚未人工标注，来源匹配覆盖损失大，旧留出已暴露，匹配只近似局部句法；没有模型干预或任务收益。谱分布相似也会隐藏方向符号和组合。

[完整五项 R10 Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/summary_cn.md) · [本轮定义、全部结果与复现](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/supplement_near_domain_tokens_cn.md) · [55名逐成员总表](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/near_single_domain_20261030/near95_members.csv) · [每成员前10 token](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/near_single_domain_20261030/per_member_token_top10.csv) · [全34ID匹配状态](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/figure_variants/near_single_domain_20261030/matched_same_token_group_summary.csv)。全部高响应阈值、原始z与排序保留；完成18类数值/分母核查。3张主图，其余3张附录。新前向0、训练0、新PCA0；人工对象核查仍待完成。此次缓存汇总后停止，不自动开新实验。

历史16+16小名单总稿已逐字节保留在[历史副本](history/meeting_brief_crosscoder_domain_members_cn_pre_near_domain_20261030.md)，不能混用旧分母或将旧R07称独立谱稳健性。
