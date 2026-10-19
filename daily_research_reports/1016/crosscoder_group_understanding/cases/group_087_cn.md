# 案例卡：G87 · 四个成员，三角形加一条桥

[回到一页导读](../README_cn.md) · [186组索引](../group_index_cn.md)

原group ID为87，保留原始0起始编号；有4个成员。本卡来自已冻结的q=10分组，没有重建图或重新训练。

**选择规则。** 小组定义为2–5成员。为了完整展示缺边，先要求有现成3随机/3高分案例且不是完全图，再取成员数最接近4者；同分取最小原group ID。最终为G87。这是教学案例，不是随机抽到的代表组。

这里的feature是冻结CrossCoder的潜变量坐标；门控z>0表示在一个文本位置命中。D是发现部分，V是同一来源bin内另一复核部分，不是已确认独立的原始文档。

## 组内究竟有哪些关系

G87的四个成员并非两两有边。800、14514、15978构成三角形，1572只通过15978接入；1572–15978是唯一桥，移除15978会把1572与另两个成员分开。六对phi虽都为正，但大小从约0.046到0.220，关系强弱并不一致。

![G87关系图](../figures/group_087_relations.png)

图中四个圆点是全部成员，线是现成D图的四条边；看三角形及1572接入的位置。实际看到三角形加一条桥，另外两对没有连边；图上的同组和路径都不能证明语义组合或学习相容。

**频率与现有复核。** D频率相差5.67倍，V相差5.27倍，所以“同组”没有要求相同频率。V的匹配组G92恰为同四人，四条D边也全部保留；现有q20分组仍是同四人。这只能说这两种现有复核下成员和边较稳定，不能给出以后数据上的稳定概率。

![G87成员频率](../figures/group_087_frequencies.png)

横轴按D频率从高到低排列成员，纵轴是D/V有效位置中的激活频率；D分母为5,238,097，V为5,247,663。实际频率范围见上文，读图应比较比例而非直接比较不同分母的次数；这些频率不测量知识稀有性或任务难度。

## 从次数到phi，再到连边与分组

一个位置中保存的门控激活值z>0，就记为该feature命中。D是发现部分，V是同一来源bin内另一部分；它们不是已确认独立的原始文档。feature ID只是固定CrossCoder潜变量坐标，尚没有可靠语义标签。

两feature的phi比较“实际共同激活”与“仅按各自频率独立出现”的差异。令N为位置数，n_i、n_j为各自命中次数，n_ij为共同命中次数，则：

\[
\phi_{ij}=\frac{N n_{ij}-n_i n_j}{\sqrt{n_i(N-n_i)n_j(N-n_j)}}.
\]

例如800与14514在D分别命中243,591和84,036次，共同命中24,825次；独立频率背景期望约3,908次，得到phi约0.150935。phi为正表示超过该独立背景，不表示因果或语义联系。

| feature对 | D共同次数 | D phi | V共同次数 | V phi | D互选名次 i→j / j→i | D连边 |
| --- | --- | --- | --- | --- | --- | --- |
| 800–1572 | 28,105 | 0.056444 | 30,501 | 0.063565 | 49 / 500 | 否 |
| 800–14514 | 24,825 | 0.150935 | 26,373 | 0.156221 | 2 / 1 | 是 |
| 800–15978 | 92,090 | 0.220406 | 90,017 | 0.217077 | 1 / 1 | 是 |
| 1572–14514 | 11,796 | 0.046467 | 13,181 | 0.048623 | 596 / 45 | 否 |
| 1572–15978 | 69,387 | 0.122261 | 75,171 | 0.132025 | 6 / 4 | 是 |
| 14514–15978 | 34,596 | 0.142367 | 37,285 | 0.147814 | 2 / 2 | 是 |

各成员先通过原D候选门槛（至少100次命中且覆盖10个D块）。候选对共同命中至少10次且phi为正后，每个成员按phi降序选择最多10个邻居，同分按feature ID；只有相互选中才连边。800–1572虽共同出现28,105次、phi也为正，却分别只排49和500，因此不连边。

原算法从单节点出发，反复合并能提高模块度的社区；模块度比较组内连边权重与保持节点加权度的背景预期。这就是现成的greedy modularity方法，resolution=1，再按成员数及ID确定组编号。此例四人恰好构成没有对外边的连通分量，现有分组把四人放在一起；它没有要求组内全连接。原逐步合并日志未保存，不能声称知道实际每一步的合并先后。

## 全部成员及其次数

| feature ID | D次数 | D频率 | V次数 | V频率 | 实际V组 | 留在匹配V组 |
| --- | --- | --- | --- | --- | --- | --- |
| 800 | 243,591 | 4.65037% | 238,874 | 4.55201% | 92 | 是 |
| 1572 | 295,487 | 5.64111% | 309,961 | 5.90665% | 92 | 是 |
| 14514 | 84,036 | 1.60432% | 90,544 | 1.72542% | 92 | 是 |
| 15978 | 476,694 | 9.10052% | 477,427 | 9.0979% | 92 | 是 |

此表完整列出4名成员，没有用画出的节点代替全部名单。[成员原始CSV](../tables/groups/group_087_members.csv)含组内邻居、桥关联、V去向和q20去向；[全部D内部边](../tables/groups/group_087_edges.csv)和[全部成员对共同次数/phi](../tables/cases/group_087_all_pairs.csv)供核对。

## 三条随机命中、三条高得分命中

随机例沿用原seed=20261015的命中context哈希抽样，再从已保存5例中取context哈希最小3例；不是对命中token均匀抽样。高分从已保存5例按“激活成员数/组大小”降序取3例，同分取较早位置，所以存在同分早位置偏向；高分不代表激活幅度更大或语义更纯。

【】标出当前已看见的token t，前缀止于t；当前激活用于预测t+1。下列“下一token”是真实语料标签，模型尚不可见，且不是模型生成结果；已有缓存未保存这些位置的模型argmax预测，记为未提供。

### 随机1 · G087_random_1_p7984973

context=7804，当前位置t=543，预测位置t+1=544（均为context内0起始token编号）；前缀共544tokens。当前token=" the"；真实下一token=" ip"。分数3/4=0.7500。

```text
 Favors.

Lisa Garey's picture

What *specifically* has he

What *specifically* has he done that you are so upset about?

John Cote's picture

forget the ipads

forget【 the】
```

以上只展示前缀末45个token及当前token；[完整模型可见前缀](../text_evidence/prefixes/G087_random_1_p7984973.txt)已保存，未把预测位置或右文放进来。

**当时全部非零组内激活（z）：** 1572=0.060250085；14514=0.034639709；15978=0.059942696。其余组内成员的门控z=0，完整含零表见[原始CSV](../text_evidence/selected_case_all_member_z.csv)。

### 随机2 · G087_random_2_p2728640

context=2666，当前位置t=780，预测位置t+1=781（均为context内0起始token编号）；前缀共781tokens。当前token=" for"；真实下一token=" "。分数3/4=0.7500。

```text
10,000 prize was offered by the Express for the winner; Sir Frank Packer, owner of Sydney’s Daily Telegraph, was eager to promote the Australian portion of the event; he offered up the prize money【 for】
```

以上只展示前缀末45个token及当前token；[完整模型可见前缀](../text_evidence/prefixes/G087_random_2_p2728640.txt)已保存，未把预测位置或右文放进来。

**当时全部非零组内激活（z）：** 800=0.051677302；14514=0.014742249；15978=0.01367805。其余组内成员的门控z=0，完整含零表见[原始CSV](../text_evidence/selected_case_all_member_z.csv)。

### 随机3 · G087_random_3_p6154698

context=6015，当前位置t=581，预测位置t+1=582（均为context内0起始token编号）；前缀共582tokens。当前token=" the"；真实下一token=" tour"。分数3/4=0.7500。

```text
 sapce issue, it is sometimes more natural in English to leave out articles in titles (and slides often consist of what are effectively lists of titles).

share|improve this answer
add comment

Your Answer

<|im_end|>Take【 the】
```

以上只展示前缀末45个token及当前token；[完整模型可见前缀](../text_evidence/prefixes/G087_random_3_p6154698.txt)已保存，未把预测位置或右文放进来。

**当时全部非零组内激活（z）：** 1572=0.023751061；14514=0.016939513；15978=0.014898753。其余组内成员的门控z=0，完整含零表见[原始CSV](../text_evidence/selected_case_all_member_z.csv)。

### 高分1 · G087_high_score_1_p1083

context=1，当前位置t=60，预测位置t+1=61（均为context内0起始token编号）；前缀共61tokens。当前token=","；真实下一token=" pp"。分数4/4=1.0000。

```text
 of stimuli, organism variables, and responses. A holistic, multi-component perspective is suggested as a framework for future research.
Journal: Journal of Happiness Studies - J HAPPINESS STUD , vol. 6, no. 2【,】
```

以上只展示前缀末45个token及当前token；[完整模型可见前缀](../text_evidence/prefixes/G087_high_score_1_p1083.txt)已保存，未把预测位置或右文放进来。

**当时全部非零组内激活（z）：** 800=0.013347223；1572=0.011666101；14514=0.014986389；15978=0.01770637。其余组内成员的门控z=0，完整含零表见[原始CSV](../text_evidence/selected_case_all_member_z.csv)。

### 高分2 · G087_high_score_2_p38739

context=37，当前位置t=879，预测位置t+1=880（均为context内0起始token编号）；前缀共880tokens。当前token=" cp"；真实下一token=" there"。分数4/4=1.0000。

```text
 lethargy after it. But everyone is definitely seeing that. At the same time, they’re noticing he’ll continually trace a circle over and over while vacantly staring. Could it actually be a complex partial?? With a【 cp】
```

以上只展示前缀末45个token及当前token；[完整模型可见前缀](../text_evidence/prefixes/G087_high_score_2_p38739.txt)已保存，未把预测位置或右文放进来。

**当时全部非零组内激活（z）：** 800=0.032390192；1572=0.017891686；14514=0.016451232；15978=0.070929028。其余组内成员的门控z=0，完整含零表见[原始CSV](../text_evidence/selected_case_all_member_z.csv)。

### 高分3 · G087_high_score_3_p42534

context=41，当前位置t=582，预测位置t+1=583（均为context内0起始token编号）；前缀共583tokens。当前token=" J"；真实下一token="ev"。分数4/4=1.0000。

```text
 permaculturally defined. Something my co-conspirator/considerer in PhD land recently discussed with me (ta Chris Maughan), was whether there's a way of tackling the Jevons Paradox (or【 J】
```

以上只展示前缀末45个token及当前token；[完整模型可见前缀](../text_evidence/prefixes/G087_high_score_3_p42534.txt)已保存，未把预测位置或右文放进来。

**当时全部非零组内激活（z）：** 800=0.059733942；1572=0.028755944；14514=0.019258849；15978=0.067022778。其余组内成员的门控z=0，完整含零表见[原始CSV](../text_evidence/selected_case_all_member_z.csv)。

**只依据六例的解释与反例。** 六例跨评论、赛事、论文条目、医疗及学术讨论，尚看不出统一话题。随机三例当前token是the/for/the，高分三例却是逗号、cp、J，连单一当前token也不能概括这个组；高分仅表示更多成员同时激活。

[六条完整前缀汇总](group_087_texts_cn.md) · [文本及全部激活JSON](../text_evidence/selected_cases.json) · [定位表](../text_evidence/selected_cases_index.csv)

## 可以保留的判断

同组不意味着两两连接，不意味着每一对都有高phi，也不要求频率完全接近。这些图表只描述固定编码器、固定数据和现成分组下的共同激活；六条文本不能证明语义组合，现成D/V和q20复核也不能证明学习相容或共同更新有益。

数值来源：[原始频率表](../source_tables/frequency.csv)、[D分组](../source_tables/groups_D.json)、[D边](../source_tables/edges_D.csv)、[V边](../source_tables/edges_V.csv)、[D/V匹配](../source_tables/matches.csv)。计数矩阵、来源哈希和逐字段映射见[表来源清单](../tables/source_manifest.json)；文本来自原examples.json并逐条与CSR及token位置核对，见[提取回执](../text_evidence/extraction_receipt.json)。
