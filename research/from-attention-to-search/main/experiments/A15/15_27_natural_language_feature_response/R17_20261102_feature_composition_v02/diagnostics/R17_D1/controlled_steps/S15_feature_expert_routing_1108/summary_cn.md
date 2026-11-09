# S15：共享成员与实际专家路由——复用数据探索

**结论：在33B训练token的原生MoE和匹配SAE上，显式文本末冒号的专家选择高度一致，三个主问题均未得到超出随机参照的证据；餐具组的实际路由权重出现次要线索，但尚不能据此决定怎样分配才有利于学习。**

本轮已完成获准的现有数据核验、开发侧成员冻结、原生前向采集、两层路由置换、频率匹配尝试、聚类区间、敏感性分析、案例和独立复算。没有训练、改权重或提交GPU作业。结果是旧文本上的探索；独立新场景确认尚未执行。配置与偏向阈值的补齐时间见[协议](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/protocol_cn.md)与[执行差异](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/amendments.md)，不把后来补齐的文档写成事先逐项审批。

## 先看什么

本问题接续R17_D1的S11/S13与[S14 MoE迁移](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S14_moe_cross_model_1108/summary_cn.md)。S14研究共享成员的参考频率，本轮研究这些成员所伴随的真实路由；S14的频率方向不是router已识别共享结构的证据。Qwen字典的编号没有移用到MoE。

必要模型是8层、隐藏维度1024、每层8专家选2个的普通MoE，训练进度33,000,000,000 token；33B不是参数量。SAE为1024→30000→1024、ReLU后Top32，接在零起block7.norm2输出，与实际router输入逐值一致。路由先对8维logits做softmax，用“概率+已保存load bias”选2个专家，再将所选**原概率**归一化为权重。没有共享专家或token drop。全部参数、load bias冻结。

最小观测单位是一个文本的一个预定位置。router分发整个token；它的32个活跃成员承接同一份路由，不能算32次独立分发。主分析把每个入选expert记作1/2，8维质量之和为1；未经除2的入选概率之和为2。真实权重另列为次要分析。

## 结果一：这两个读取位置主要使用固定专家组合

主条件是旧确认集48家族×24标签的1152条显式文本。末冒号处1129/1152（98.00%）为专家{1,6}，其余23条为{6,7}。末正文位置1123/1152（97.48%）为{4,7}。编号零起算。这只描述两个固定标点／读取位置，不能称为全模型路由坍缩或全语料专家失效。

![两个预定位置的实际负载](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/figures/01_actual_expert_loads.png)

左图是入选质量r/2，右图是实际gate权重；每个位置分别汇总1152条文本。相同专家组合可以有不同权重。位置的差别大于本轮主条件的许多类别差别，但本轮没有操作位置、标点或bias，不能判定由哪个因素造成。原表：[专家组合计数](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/top2_pair_counts.csv)、[全部标签负载](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/all_label_expert_loads.csv)、[逐类别负载](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/expert_loads.csv)。

## 结果二：三个主问题没有得到额外路由结构的证据

**Q1问某成员出现时，expert质量是否偏离同类别的总体负载；Q2问同一共享成员在A/B两类中的expert分布是否不同；Q3问A偏向与B偏向成员分别在各自类别中的分布是否不同。** 都使用总变差距离TV，即两分布差值绝对值之和的一半。下表单位是TV×100，即质量差异的百分点，数值越大表示分布越不相似。Q1先逐成员、逐类别计算再等权；Q2等权平均共享成员；Q3先各自等权汇总成员再比较。

| 类别对 | 共享／A偏向／B偏向成员数 | Q1：成员相对类别负载 | Q2：同一共享成员跨类别 | Q3：两侧偏向成员 | 主结果资格 |
| --- | ---: | ---: | ---: | ---: | --- |
| 猫／狗 | 13/1/1 | 0.227 | 0.013 | 0.000 | 覆盖合格，未决 |
| 汽车／自行车 | 13/1/2 | 0.297 | 0.223 | 0.593 | 覆盖合格，未决 |
| 苹果／香蕉 | 13/2/5 | 0.355 | 0.211 | 0.088 | 覆盖合格，未决 |
| 椅子／沙发 | 11/1/2 | 0.306 | 0.042 | 0.000 | 不足 |
| 衬衫／裤子 | 12/2/2 | 0.238 | 0.121 | 0.743 | 覆盖合格，未决 |
| 钢琴／吉他 | 12/2/1 | 0.089 | 1.056 | 1.116 | 覆盖合格，未决 |
| 玫瑰／郁金香 | 10/3/3 | 0.284 | 0.020 | 0.458 | 覆盖合格，未决 |
| 勺子／叉子 | 12/3/5 | 0.515 | 0.257 | 0.298 | 覆盖合格，未决 |

24个预定主比较中，21个覆盖合格但未决，3个家具比较不足。家具sofa旧行为评分25/48，未达0.75；其Q3成员覆盖也只有0.5，不能因表中距离小就算一致。其余7组在全局和条件置换下，均未通过各问题八组Holm校正；合并24项校正也未通过。**未拒绝零假设不等于证明分布相等、没有组织结构或没有有用分工。**

![三个主问题及场景聚类区间](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/figures/02_primary_questions.png)

每条线是以16个场景簇为抽样单位的2000次bootstrap原始TV的95%百分位区间；空心点表示覆盖或行为不足。各主区间下界均为0。钢琴／吉他Q3最大，约1.116个百分点，区间0至3.392。原始TV区间并非相对零模型的效应区间，也不是等价性检验。

逐成员的开发侧方向同样不能包装为复制成功：264个成员×类别角色中238个在DEV的八个expert上差值并列，18个未出现，8个有唯一偏向，全部属于行为不足的sofa。因此主条件无一条满足预定资格的“开发侧方向复现”记录；并列时表中机械argmax=0不是识别出了expert0。

原表：[三个问题的全部192行](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/primary_questions.csv)、[16,896行成员×类别×expert统计](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/feature_expert_statistics.csv)、[跨类别共享成员](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/shared_feature_cross_category.csv)、[开发侧方向复查](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/development_confirmation_direction.csv)。另保留[池化统计](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/feature_expert_pooled.csv)、[expert内部成员出现率](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/expert_internal_feature_composition.csv)、[样本共有／仅一侧集合](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/sample_set_changes.csv)。后两表是描述，成员重叠，不能将其解释成互斥语义模块。

## 结果三：餐具的权重差异值得保留，但尚不足以升级结论

勺子／叉子的Q3硬选择TV仅0.298个百分点；改用真实gate权重为**6.511个百分点**，场景聚类95%区间5.017至8.169。条件置换均值4.387个百分点，观察值超出2.124个百分点；条件置换原始p=1/1001，局部八组Holm后0.00799。全局置换八组校正后0.03197。

然而，把全部192项权重次要比较一并校正，条件p为**0.19181**，全局为0.73526；保留类别名改写的餐具Q3条件八组校正p=0.07992。餐具频率匹配参照没有合格抽样。因此这是**局部次要候选**，没有跨表达的独立确认。不是把主指标不显著改写成权重主检验成功。权重区间针对原始TV，不能用其下界>0替代置换检验或排除类别固有权重差异。

![硬选择和权重的Q3点估计](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/figures/03_gate_weight_sensitivity.png)

图中横轴同为TV×100，圆点为主硬选择，方点为次要gate质量，空心为不足。它只展示点估计，区间及各层校正见[权重完整复算表](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/gate_weighted_resampling.csv)；[幅值加权敏感性](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/weighting_sensitivity.csv)只作描述。

## 随机参照实际控制了什么

全局参照1000次把完整expert对与权重记录按场景块、家族槽位与统一标签置换，保持整体专家负载与组合结构，但类别组成可变化。条件参照1000次固定类别、表达和位置，映射完整场景与共同家族槽位，保留类别负载；一个token的多个feature不被拆开。bootstrap共同重采16个场景簇，保留每簇3家族及对应类别。6912条文本、132个逐对成员或16/24个检验都不是独立实验次数。

**长度控制不足：** 开发场景平均长度中位数30.608划出的确认场景两层为3/13簇；按冻结的稀疏合并规则最终合并成一层。因此条件参照没有有效长度分层。它保留了模板相关块，不等于排除了模板或词面解释。属性／情境版本的大量行为失败，以及正文位置的低成员覆盖，均保留为不足；正文餐具Q1/Q2/Q3虽有较大距离，覆盖仅0.1875/0.0833/0.4，不能挽救主结果。正文仍使用冒号侧冻结成员与频率匹配池，不能称为正文原生频率确认。

另尝试匹配Q题干、G通用参考频率及DEV出现率的随机成员组，每组1000次；三维绝对差各≤0.10，候选池至少DEV出现率0.125、排除该对已选成员，保留最近32个，无放宽。

| 类别对 | 共享组有效参照／1000 | 偏向组有效参照／1000 |
| --- | ---: | ---: |
| 猫／狗 | 0 | 1000 |
| 汽车／自行车 | 0 | 136 |
| 苹果／香蕉 | 0 | 31 |
| 椅子／沙发 | 0 | 21 |
| 衬衫／裤子 | 0 | 724 |
| 钢琴／吉他 | 0 | 199 |
| 玫瑰／郁金香 | 0 | 0 |
| 勺子／叉子 | 0 | 0 |

有效数同时要求完整抽出和评估覆盖；八个共享组都不足，偏向组仅动物达到800次门槛。动物Q3观察0，匹配均值1.789个百分点，没有额外分离。其余部分有效抽样仍有数值，但不可当成充分参照。匹配统计是描述性经验对照，不是校准p。高频共有成员缺少可替代者是本次重要支持域缺口，不能省略。原表：[匹配候选覆盖](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/matching_coverage.csv)、[匹配参照结果](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/frequency_matched_reference.csv)、[完整成员与参考频率](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/feature_groups.csv)。

## 工具质量和真实案例

全部6912文本重分词与保存token一致；实际norm2输出与router输入相同，原生路由和手工复算完全一致。13,824个位置的Top32集合全部与S14缓存相同，最大激活数值差2.29e−5。主条件各域（含父类）平均重建相对平方误差0.197–0.223；将重建向量离线送同一冻结router，Top2集合一致率97.22%–99.31%。这检查测量保真度，没有用重建路由替换真实观测，也未测量模型功能或学习收益。

案例是本轮确实输入的构造英语文本。猫／狗同一家族中，A偏向成员#29184的激活5.131／0，B偏向#21462为1.526／4.874，两个token仍都路由至{1,6}；偏向不是排他。反例中，同一共享成员#14800在钢琴／吉他两侧激活2.933／2.894，却分别伴随{6,7}与{1,6}。同成员不决定完整token的路由。

[五个详细案例与完整输入](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/paired_examples.md)覆盖两个共享成员展示、两侧偏向展示和一个事后找到的反例；前四例部分使用同一家族，不是五次独立试验。[逐案例索引](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/case_rows.csv)可回查[全部13,824条位置记录](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/results/token_routes.csv)和[data/token_records.jsonl](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/data/token_records.jsonl)。

## 完成范围与下一步

独立CPU复算核对全部13,824条router记录、32个SAE位置、全部384个主／权重点估计，以及主条件各24个硬选择和权重区间、各48个置换p，均通过。模型／SAE全文件哈希仍与输入一致。首次依赖导入失败、案例导出低效重试、协议补齐及次要全192项校正的时间均在[详细记录](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/detailed_cn.md)与执行差异中。

已完成数据、feature分组、路由、随机参照尝试、结果复算与交付。**未完成的证据**是充分频率匹配、有效长度控制、全新独立确认及任何功能／学习对照；它们并不因流水线完成而变成通过。当前结果还不能证明错误分发、梯度干扰、专家功能专一化、训练效率下降，也不能确认哪类信息应共享学习。

**AI建议，仅一项优先后续：** 先审批一轮冻结“餐具gate权重差异”的独立场景测量复核。保持同模型、同SAE、同定义，单列类别基准权重，预先匹配长度与读取位置，涵盖保留类别名的改写；按新场景与近重复隔离，并在看路由前冻结筛查规则和主要比较。若候选不复现或缺少足够支持域，就停留在测量问题，不强行进入训练。本轮未生成这些新文本，也未启动续训。科学接纳和下一实验决定仍由研究者确认。

[配置](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/config.json) · [数据字典与复算入口](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/detailed_cn.md) · [原始交付入口](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/README_cn.md) · [独立复算](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/evidence/independent_verification.json) · [次要复算](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/evidence/secondary_verification.json)

[餐具权重的补充真实案例](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S15_feature_expert_routing_1108/cutlery_weight_example_cn.md)：事后按首个显式确认家族展示，不参与检验。
