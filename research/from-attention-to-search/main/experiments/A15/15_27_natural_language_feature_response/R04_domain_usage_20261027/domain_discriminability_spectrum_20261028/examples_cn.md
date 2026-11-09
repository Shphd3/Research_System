# 一个真实算例与反例

以下是缓存内事后解释例子，不参与候选筛选或新确认。只有当前token及可见前缀用于说明。

## 单feature如何由token变成文档读数

SAE f11667来自新固定前16。真实数学文档`DOC_math_28475`中，窗口内154/160个位置有激活。到token **` only`** 时的可见文本片段为：

> ften in applications, an acceptable approximation to a regularly perturbed problem is found by simply replacing the small parameter \varepsilon by zero everywhere in the problem statement. This corresponds to taking only

该token的原空间贡献为45.51366；**这不是整篇平均**。整篇激活时平均贡献为26.47189，故含零平均=(154/160)×26.47189=25.47920。分类与本轮单feature排序用的是最后一个量。

跨20篇数学／20篇生物留出文档：命中比例73.8438%／4.6250%，有活动文档内的条件贡献平均13.9312／4.6291，含零平均10.9976／0.5624。按发现数学方向抽一篇数学与一篇生物，平均贡献排对概率0.9725，文档bootstrap区间[0.9025,1.0000]。这不是该token含数学概念的概率，也不是分类准确率。

注意：域内先按文档等权求平均后，域均值的“命中比例×条件强度”一般不等于域内含零均值。恒等式只在单文档成立；相关性与零命中文档会改变域内加权。原先按所有活跃token汇总的条件均值与现在文档等权数值不同，CSV同时给出position_weighted_conditional以免混用。

## 反例一：生物文本也可强烈激活该数学方向候选

真实生物文档`DOC_biology_24483`讲突触电位、电缆理论与神经元建模；f11667在其中133/160位置激活，含零平均10.93598，并非只在数学文本出现。到token`),`的贡献为25.69179，可见片段：

> the site of the synapse itself. In fact, the voltage decays exponentially with increasing distance from the synapse. The extent of the signal decay is governed by the axial resistance (influenced by dendritic diameter),

这说明数学／生物是人工文档标签，生物文档可包含数学建模内容。可区分不等于领域专属；这种边界例必须保留，不能因其影响解释而删去。

## 反例二：发现方向在原留出反转

新扩展SAE f5662按发现集固定为生物方向，留出排序概率0.3675，区间[0.2025,0.5451]；含零数学/生物平均0.2027/0.0958，不能说已确认生物偏向。它仍在扩展名单与图2中，没有换人。

原共有f29506也是“局部强弱差≠稳定单坐标区分”的例子：原F11相同difference上数学/生物15.19/6.05，第二措辞7.71/7.95反转；文档排序概率0.4975，区间[0.3125,0.6850]。原共有32组合能分类，不要求每个成员单独成功。

全体固定候选的token例子和各token命中次数分别保存在`analysis/selected_token_examples.csv`与`selected_token_hit_summary.csv`。每域最高3个不同文档的例子是高响应展示，不是无偏代表；token命中次数未除以token出现机会，不叫词选择性。原文档URL、序列ID和零起算位置都在表中。


# A01：上述真实feature在共同谱中的读数

数学文档算例SAE f11667的原空间单位decoder有81.95%平方长度落在PC1—64。该feature在原留出单坐标排序概率0.9725，说明这个例子同时有前部几何位置和可读使用差别；没有功能干预证据。

相反，原共有f29506前64有96.75%，却只有0.4975的单坐标排序概率：方向位于高方差子空间，本身不保证实际使用量携带稳定领域读数。CC f11710则只有10.56%方向在前64、最大段PC129—192，但单坐标概率0.995。两套编号不是同一个坐标，CC的z仍是14层共享读数。这说明不能直接用decoder谱位置替代激活使用模式。

本轮没有给任何谱段贴“高级/低级语义”标签；域均值差集中只说明两类文档中心差异的几何分布。
