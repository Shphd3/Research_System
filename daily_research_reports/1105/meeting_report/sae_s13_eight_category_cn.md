# S13组会简报：细类共有feature的平均参考频率更低，类别关系差仍未确认

**先答共享feature是否相对更低频：在本轮八组指定的显式类别文本中，是。32/32项通过冻结标准，平均频率差为0.95–9.93个百分点。名称改写31/32项支持；隐式属性和场景多数未过行为门槛，不能并入显式结论。** 这里说的是选定参考语料和读取位置下的平均频率更低，不是所有共有feature都罕见，也不是已识别语义机制。

## 目的

我们想弄清：从“动物”到“猫、狗”，模型内部哪些成员保留、哪些换入或换出、强弱怎样变化；细类之间共享的成员，是否比粗类之间共享的成员更少在其他文本中出现；某些成员的搭配，是否超出单成员频率，并随类别稳定变化。这三个问题分别需要频率、成员事件和联合关系的证据。

本轮保持官方Qwen3-0.6B Base及两个block27原生Top32 SAE不变。Attention输出和MLP输入各30000坐标，字典ID不对应。6912条前缀全新编写：24开发家族／8场景簇，48确认家族／16场景簇，每家族24标签×4种表述。原四组用新文本确认，另新增衣物、乐器、花、餐用器具四组。统计独立单位为场景簇，不把文本、feature或Q/G重复计作独立确认。未训练底模、SAE或router，未做功能干预。

## 结论与紧随的数据

### 共有成员的平均频率：显式八组获得支持，隐式不足单列

每对文本先取正激活成员交集，再在交集内等权平均各坐标的参考频率，最后场景簇等权。参考频率分母为6000篇文档；本轮复用S11的Q题干和G DCLM缓存，在正文后追加`Description:`的末冒号读取。它不是词频或幅值。粗基线预先固定为动物–交通工具、水果–家具、衣物–乐器、花–餐用器具；比较量为“粗均值−同父细类均值”，正值表示细类共有成员相对更低频。

| 表述 | 主条件 | 支持 | 未决 | 不足 | 可以怎样说 |
| --- | ---: | ---: | ---: | ---: | --- |
| 显式类别词 | 32 | 32 | 0 | 0 | 原四组新文本与新增四组各16/16支持 |
| 保留名称改写 | 32 | 31 | 1 | 0 | 接近复现，仍保留餐用器具MLP/Q未决 |
| 隐式属性 | 32 | 8 | 0 | 24 | 水果和乐器两组通过行为资格 |
| 隐式场景 | 32 | 4 | 0 | 28 | 只有乐器组通过行为资格 |

每项均有48/48有效确认家族、16/16有效簇。全部128项差值点估计为正，但“方向相同”不替代行为资格、联合区间与Holm校正。名称改写的MLP餐用器具Q差为+1.44个百分点，联合95%CI [0.06, 2.70]，Holm p=0.0637，仍未决。

几个决定性的原始值如下，单位为参考频率的%；差和区间单位为百分点：

| SAE／参考 | 粗比较 → 细比较 | 粗均值 | 细均值 | 粗−细及95%联合CI |
| --- | --- | ---: | ---: | --- |
| Attention／Q | 动物–交通工具 → 猫–狗 | 17.05 | 13.04 | +4.01 [2.95, 5.15] |
| MLP／Q | 动物–交通工具 → 猫–狗 | 46.74 | 39.60 | +7.14 [5.61, 8.66] |
| MLP／Q | 衣物–乐器 → 钢琴–吉他 | 47.62 | 37.69 | +9.93 [8.41, 11.34] |
| MLP／G | 花–餐用器具 → 勺子–叉子 | 40.49 | 38.82 | +1.66 [0.39, 2.91] |

39.60%相对46.74%更低，但不能称绝对罕见。替换为另外两种预设粗参照后，显式各32/32项方向和固定参考簇区间仍正；这些是次要敏感性，不救援主未决或行为不足。显式中位数差32/32为正，但上四分位有2项反向点估计且区间跨0，不能据均值或几个分位点宣称整条分布处处下移。

行为门槛为每个子类至少36/48正确。属性未达者为猫32、自行车20、沙发17、长裤26、郁金香1、叉子8；场景未达者为猫25、自行车33、香蕉35、沙发9、长裤17、郁金香0、叉子12。评分使用完整候选序列log概率总和。郁金香的每token均值敏感性虽为1，也不替换冻结主评分；这些不足不能直接解释为模型没有相关知识。

### 数学关系：池化固定边7/22复现，类别差没有通过

“常搭伴”可能只因为另一个成员本来就常见。为此，在每个类别内随机重排完整位置×30000坐标矩阵，精确保留每行Top32和每个坐标的出现次数；再看真实条件共现概率是否高于这个参照。关系超额定义为“真实条件概率−零模型平均条件概率”。零模型约束精确保留，分布和p值仍是有限Curveball链的Monte Carlo估计。

| 显式确认对象 | 通过 | 未决 | 不足 | 无候选未运行 |
| --- | ---: | ---: | ---: | ---: |
| Attention池化固定边11条 | 3 | 6 | 2 | 0 |
| MLP池化固定边11条 | 4 | 5 | 2 | 0 |
| Attention八组类别差 | 0 | 4 | 2 | 2 |
| MLP八组类别差 | 0 | 1 | 4 | 3 |

因此显式池化关系为7/22通过；类别差则0/11个开发有候选条件通过，另5个无候选未运行。池化通过不表示每个细类都有该关系，更不表示能区分猫狗。例：Attention 26542→2254池化768行，四格为(135,11,423,199)，真实条件概率0.9247、零模型0.7554，超额+16.92个百分点，95%CI [8.85, 24.46]；独立单位仍只有16场景簇。

不能把所有类别超额差都叫“交互关系转换”。MLP家具416→5196在椅子和沙发两侧的真实条件概率都为1，超额差却为+33.22个百分点，来自零模型基线差。**同时保留一个不同的局部阳性：**Attention属性描述的fruit→banana，固定边9270→2254的真实条件概率从23/39变为23/27，超额差+24.41个百分点，95%CI [11.53, 35.70]，Holm p=0.0312。它确有原条件概率变化，但属于父子探索，未跨其他表述稳定复现，不能当作统一类别机制已确认。

### 唯一显式读出GAIN可由复制列解释

小型统计读出比较同一节点集合的加性模型与增加一个固定乘积项的模型。辅助复制列替代诊断在查看确认集读出结果前固定；当时频率结果已查看，因此它是辅助解释诊断，不是原主检验。唯一显式GAIN为MLP花：loss从0.075020降到0.074786，收益0.000234 nat/行，95%CI [0.000090, 0.000440]，Holm p=0.0336；两者准确率均98.96%。但乘积416×17390在确认四种表述都完全等于已有416列，用416替代乘积后所有预测和损失不变。复制列会改变L2读出的有效正则化，因此该小收益不需要新增联合信息解释。场景表述另有2项HARM；无边的5项保留未运行，不作失败替代。

## 机制直觉与假设（AI建议，待研究者判断）

目前较可信的描述是：细类共享坐标的平均参考频率相对较低；区分细类时，少见和常见成员都可能参与，成员还会保留、退出、换入和改变幅值。不能把共享成员的均值趋势迁移为“越细，区分feature越低频”：S11显式区分成员仍是6支持／5反向／4未决／1不足；例如MLP/Q汽车自行车，粗区分频率6.73%、细13.50%，差的联合95%CI为[−8.68, −4.84]个百分点。

**AI建议只保留一个下一问题：在词面、背景及单成员依赖基线更匹配的独立描述中，固定关系的类别差还能否复现？** 这是待研究者选择的问题，不是新运行授权。本轮频率结果、局部共现超额、类别差和读出用途分别保留，科学接受、机制判断与问题关闭仍为`Unknown`。

## 具体实验分析与证据入口

本轮确认前固定开发候选、方向、协议和文本。主要均值差使用2000次场景簇／独立参考文档联合重采样、9999次簇符号检验，每个表述和参考轴分别Holm16；分位数及替代粗参照的区间只条件于固定参考。隐式去掉了24个字面标签，但仍有原型、近义词和属性提示；没有完全匹配词面、长度、背景或来源。固定父类块同时改变类别身份，仍不足以识别普适语义粒度规律。

成员事件提供了另一层具体描述：首个确认场景N004中，Attention坐标26542在动物／猫／狗都激活，原始z为2.5044／2.8893／2.5270；动物→猫保留26，换出与换入各6。相等的换出／换入数由Top32名额强制，不是语义发现。显式退出事件中，Attention有10718/11059、MLP有6703/7245仍保留正编码响应，不能把Top32未入选解释为编码器完全不响应；这些是重复配对事件，不能当独立样本。

阅读入口：

- [完整中文Summary与32项显式原始值](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/summary_cn.md)。
- [128条件单臂原始水平和区间](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/results/frequency_raw_arm_levels_all128.csv)、[主差与判定](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/results/primary_frequency_contrasts.csv)。
- [全部关系条件、父子探索与尺度说明](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/relation_results_cn.md)、[完整类别覆盖](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/results/relation_category_complete_coverage.csv)。
- [原文、读取位置与逐成员案例](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/casebook_cn.md)、[完整方法与限制](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/detailed_cn.md)、[阅读副本来源清单](../../../Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S13_eight_category_independent_1105/payload_manifest.json)。

656项主统计独立复算已通过；全部图、冻结合同和所选小表已本地保存，逐文件来源／字节／SHA256在来源清单中。[完整结果包](../20261105_S13_eight_category_independent.zip)为18502887字节（18.50MB），287成员，新解包67472项检查通过；SHA256为`bcc757efa85a139f0e54d233268ebb47f6e4fcf72125fb42cea97fe72de0e7a5`。本简报是研究者审阅前的派生阅读材料，没有改变旧结果或科学状态。
