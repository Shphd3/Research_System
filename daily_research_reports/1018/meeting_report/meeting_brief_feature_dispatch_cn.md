# 10月18日讨论：名单中的低频 feature，为什么没有到达负责专家？

**当前证据更支持先规定并校准评分。** 本轮已定位原评分的胜出路径，有限共现检查没有迫使零接收；但新评分是否可用、全局分组是否可行、学习是否改善，都还没有答案。本稿是已保存证据的讨论摘录与AI建议，待研究者审阅。

[一页正式概要](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/feature_group_to_actual_dispatch/20261018_routing_audit/summary_cn.md) · [完整执行与解释](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/feature_group_to_actual_dispatch/20261018_routing_audit/detailed_cn.md) · [Anchor](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/crosscoder_feature_relations/feature_group_to_actual_dispatch/anchor_cn.md) · [Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/feature_group_to_actual_dispatch/20261018_routing_audit/protocol_cn.md) · [近期结果索引](/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/qwen3_crosscoder_tooling/20261018_routing_progress_cn.md) · [12张文本卡](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/feature_group_to_actual_dispatch/20261018_routing_audit/text_cases_cn.md) · [四图术语](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/feature_group_to_actual_dispatch/20261018_routing_audit/figures_cn.md)

## 目的与必要模型

长期目的仍是为内容分工和共享／分离学习找依据。今天只解决前置问题：一个低频 feature 已在当前输入中激活，为什么完整输入没有去名单为它指定的专家？不是在确认低频知识学会了没有。

使用冻结 Qwen3-0.6B Base 与最终14选定层 CrossCoder 的既有z缓存，按原TRAIN激活频率分八个原始概率等宽区间，名单A的组人数是 `[9253,183,124,34,7,3,2,9]`。B1/B2是保留这八个人数的两套原随机名单。所有规则只让完整输入进入一个专家。本轮只做CPU缓存诊断，没有模型前向或训练。

## 方法：把名单、输入与分数接起来

对同一个feature，分别检查它在全局有多常见、含它的输入有多少进入负责专家、进入专家的输入中它又有多常见。空专家的后一个比例为NA。再拆原组均分中的高频名单C与其余项，做一次仅评分项置零的虚拟诊断；按TRAIN冻结3个案例和27个跨负责专家对，到EVAL读文本／分数／共现。TRAIN为130,712位置，EVAL为65,402位置，原低频集合964项。

## 最多三条证据结论

### 1．“放进名单”并不等于“得到输入”

A的964项低频feature在两侧负责专家接收率全为0。EVAL同一批feature在各自B1／B2负责专家的等权平均接收率为4.44%／10.30%，仍有122／48项为0。A0完全无输入，q不可估计，不能说q=0。

![各专家实际接收与零接收目标](../figures/routing_audit_figure1_actual_reception.png)

图1上排是输入比例，下排是每个名单中零接收feature的比例，分母不同。蓝色为原规则，橙色仅把C的评分项置零；橙色全送A0显示退化，并不表示成功。B专家编号不能与A强行对应语义。

![全局频率与负责专家内频率](../figures/routing_audit_figure2_global_vs_owner_frequency.png)

图2每个点是一项feature。横轴p是全局激活频率，纵轴q是负责专家输入中的频率。A有9,560项因专家为空而NA，另外30项q确实为0。虚线q=p仅表示没有相对全局富集，不是学习合格线。原始整数及组汇总：[表](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/feature_group_to_actual_dispatch/20261018_routing_audit/tables/group_summary.csv)。

### 2．原组均分让低频命中失去评分竞争，但删除高频项不是解决方案

TRAIN含低频feature的位置中，原赢家比A0平均高0.567492；C项差额为+0.569428，其余项为−0.001935。低频所在组虽有响应，仍被压过。C是原TRAIN高频962项名单，阈值约4.5861%，不是语义上的“共同知识”。

仅将C评分项置零会把全部位置改送A0，但A组1–7全部属于C，操作使它们机械得0分；七个专家随后全空，另25个原来有正接收的feature失去负责专家接收。因此这只定位计算路径，不是有效路由，也没有分别识别频率、幅度和组构成的独立原因。

![三个目标与伴随项的专家内频率](../figures/routing_audit_figure3_target_common.png)

图3把同一个目标本身U与TRAIN固定选出的三个伴随C分别画出。A第一列是负责专家0，因无输入而NA；第二列是真实主要去向专家7。不能把收到大量输入的专家7重新叫成负责专家。

### 3．已有共现取舍不能解释“必须零接收”

仅从三个固定案例找27个跨负责专家对，不做全池两两搜索。若两目标分别要求相同接收比例τ，则top-1必要界为τ≤1−共同命中数／两者命中数之和。A选中对在TRAIN的界为99.18%–99.61%，EVAL为98.84%–99.72%。这些界限制非常高的同时覆盖，却不能迫使某目标为0。没有指定τ，不能给达标或失败判定；有限配对也不证明全体可行。

![随机文本位置与评分](../figures/routing_audit_figure4_text_and_score.png)

图4每个ID用第一条固定随机命中，而非挑漂亮例子。三个案例各有3随机＋1高激活卡，共12张；所有A输入去了专家7。当前token与下一token标签分开，模型未用下一标签评分。36个位置—规则组合中单独移除目标评分项均未改赢家，只说明局部评分敏感性，不能说feature无用。

## 这段时间真正推进了什么？

|阶段|得到的认识|仍不能跨越的桥|
|---|---|---|
|特征关系图与共同背景|部分统计边可复核；展示高J可能由同一批高频伴随项支撑|组成列表重叠不能替代实际共激活、语义或学习收益|
|图层级与14层decoder|整体h—L负相关，同级有不同轮廓|h不能当模型深度；L不能替代整条幅度分布，更不是功能贡献|
|旧4专家rank32学习实验|9个正式run登记的非零EVAL点均差于原模型；有TRAIN下降而EVAL上涨|不能写成训练loss全部上涨，也不是当前8普通FFN的正式比较|
|φ组探索|关系组并非全员同时出现，几何与共现也不同|不把φ社区当频率路由组或已验证学习单元|
|新8普通FFN旁支smoke|原A前三专家零输入，覆盖门槛未过，正式学习NOT RUN|B负载更完整不等于学得更好|
|本轮逐feature诊断|确认低频逐项零接收，定位原评分项差额；有限共现界不能迫使0|没有训练／校准／重分组，没有证明全局可行|

六段记录的精确来源见[项目近期结果索引](/data/250010109/Research_System/Projects/from-attention-to-search/main/research_notes/qwen3_crosscoder_tooling/20261018_routing_progress_cn.md)，旧实验记录未覆盖。以上是事实与推断边界的整理，不是对长期研究问题的科学关闭。

## 已做、没做、下一步只讨论什么

**已做完当前诊断：** 原始计数／位置核对、A/B逐feature p/a/q和富集、200次上下文块描述性重采样、每侧927,368个低频×C伴随对、评分分解／虚拟置零与逐feature代价、12张文本卡、27对TRAIN固定的有限共现界、四类图及来源。

**没有做：** 新评分校准、调整名单、完整最优分配、真实表征消融、学习训练和训练后谱。这些不是被省略的本轮步骤；其中有效逐组匹配消融因没有既有可比对照而不能成立，独立原因仍未识别。

**唯一AI建议：先明确评分应比较原幅度还是相对组自身常态的响应，再登记一次保持名单、检查其他频段代价的评分校准比较。** 在新设计冻结与授权前不执行。重点不是把输入从专家7搬到专家0，而是低频目标有机会、其他目标代价可接受，随后才有理由检验学习。

组会可以用四个白话问题对齐：

1. 我们要求的是“含这个feature的输入去负责专家”，还是“专家收到的输入里这个feature更常见”？前者是接收率a，后者是专家内频率q。
2. 什么接收比例才够用？为了低频组，允许其他组失去多少机会？
3. 如果去C后全部去了专家0，为什么不能称成功？因为七组评分被机械归零，另一批目标失去接收。
4. 若下轮校准改善接收但NTP不改善，我们是否愿意放弃“接收改善就有学习收益”的桥？本轮尚未测试这条桥。

这轮认识更新可以说成：**昨天把分组名单当成可能的学习分工；今天发现必须先验证名单是否落实成输入接收。先缩窄并修清评分问题，保留分组冲突与学习效用两条未答边界。**

图件为执行侧原图的逐字节日期副本，见[图件来源](../figures/SOURCES.md)。完整成本和执行状态见[Detailed](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/crosscoder_feature_relations/feature_group_to_actual_dispatch/20261018_routing_audit/detailed_cn.md)及执行目录回执。本轮交付后停止。
