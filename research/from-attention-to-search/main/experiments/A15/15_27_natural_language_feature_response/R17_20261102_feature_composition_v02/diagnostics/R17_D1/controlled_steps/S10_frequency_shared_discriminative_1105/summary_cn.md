# S10：粗细粒度类别的共同与区分 feature 统计

本轮认识更新：**共同成员在相对意义上偏高频，但“共有＝高频、区别＝低频”不是本轮得到的规律。细类区分没有呈现跨类别、跨措辞一致的中低频迁移；共享成员本身的强弱变化可以区分类别，但这种方向依赖措辞。** AI 操作判定；科研接受、机制判断与问题关闭保持 Unknown。

## 目的与假设

我们要知道粗类和细类共同使用、反复区分的 SAE 坐标分别落在哪些独立参考频率上。H1 预测跨大类共享更偏高频、同父细类额外共享较低频；H2 预测细粒度区分向中低频延伸；H3 区分成员更替、共同成员强弱和超边际联合结构。三个假设均不预设成立。训练效率和真实专家分发不是本轮测量对象。

## 原始数据与频率定义

复用原 S06 全384行和两套稀疏激活。原 F01–F08用于本轮新候选选择，F09–F16的新增统计全部是事后探索。新增16个从未用于候选或调参的 N01–N16模板，每家族6类别×4措辞，共384条；原3措辞复用旧词组，第4种使用新改写。另有48条事先固定的最简词组/短语境诊断。没有训练或干预。

同一 Qwen3-0.6B Base、末块27的 Attention 输出 SAE 与实际 MLP 输入 SAE，各30000维、原生 Top-32，字典编号互不对应。所有类别文本均读末尾 `Description:` 的冒号。独立频率参照为 Magicoder problem、GSM8K question、MMLU question 各128篇，共384篇；保留首至多128 token并追加同后缀，每文档一个冒号位置。**这是有限题干在指定位置的激活频率，不是普适频率。**

- Attention：0次单列；1–7次不足；低频8–11次，中频12–18次，高频19–384次。三组分别118/86/101个坐标。
- MLP输入：低频8–11次，中频12–32次，高频33–384次；三组66/55/61个坐标。另有1260个支持不足、28558个参考未出现。
- Attention另有2362个支持不足、27333个参考未出现。没有把这些成员强行记为低频。完整分母及2000次等源文档重采分组稳定性见[频率表](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/data/frequency_reference.csv)。

## 分析、对照与原始结果

### 1. 共有：跨大类的高频占比相对更高，但不是所有共享都属于高频

下表是新确认显式文本每家族交集中的频率组成，再等权平均；分母是该配对全部共有成员，包括不足和参考未出现组。

| site | pair | low | mid | high | insufficient | unseen |
| --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | animal_vehicle | 8.179369 | 7.099762 | 43.098268 | 28.097256 | 13.525345 |
| ATTN_SAE | car_bicycle | 5.851588 | 12.136973 | 41.836324 | 28.83844 | 11.336676 |
| ATTN_SAE | cat_dog | 10.023285 | 8.910096 | 35.627042 | 30.497994 | 14.941583 |
| MLPIN_SAE | animal_vehicle | 2.433307 | 10.09363 | 67.218342 | 12.470777 | 7.783945 |
| MLPIN_SAE | car_bicycle | 5.785445 | 8.362726 | 60.98819 | 13.558887 | 11.304752 |
| MLPIN_SAE | cat_dog | 3.290864 | 9.180722 | 60.140811 | 17.98535 | 9.402253 |


![主图](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/figures/main_frequency_shared_discriminative.png)

读图：同一行的颜色合计100%，深蓝代表独立参照中的高频。左栏是16个新家族的真实交集，右栏是发现侧锁定的区分候选，**右栏包含未复现候选，不等于确认成功的成员分布**。同父细类、直接父类词和细类等权汇总分别报告。

Attention跨大类高频占比43.10%，猫狗35.63%；差7.47百分点，95%家族区间[1.95,13.49]、Holm4 p=.02310。MLP输入对应67.22%与60.14%，差7.08[3.85,10.20]、p=.00244。MLP交通细类也同向；Attention交通差1.26[−2.14,4.92]，未分辨。4项主要高频对比有3项通过。进一步说“细类额外共享中低频”则更弱：MLP猫狗low+mid份额与跨类几乎相同（差−.055百分点），高频占比下降主要被其他频率未知成员补上。

竞争解释没有排除：错配整条家族向量能保留每类feature频率和Top-32，但明显改变共享组成；独立自然题干对自身的共有成员高频占比已达到95.62%/98.60%。因此高频共享的裸占比或相对30000坐标的富集，不能单独证明类别特有组合。原S09对自然正文重叠差的82.9%–97.0%数值复现仍成立，**不能直接套到本层级实验**。[所有关系与错配参照](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/results/core_pair_summary.csv)保留逐对Jaccard，未用交集期望替代Jaccard均值。

### 2. 区分：没有形成统一的粗高频、细低频分工

发现侧多措辞出现率规则锁定的候选如下；数目是坐标数，不是独立样本数。

| site | pair | locked_count | supported_count | low_mid_count | high_count | insufficient_count | unseen_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | animal_vehicle | 16 | 8 | 2 | 6 | 5 | 3 |
| ATTN_SAE | cat_dog | 2 | 0 | 0 | 0 | 1 | 1 |
| ATTN_SAE | car_bicycle | 9 | 3 | 1 | 2 | 5 | 1 |
| ATTN_SAE | pooled_children | 21 | 11 | 4 | 7 | 6 | 4 |
| MLPIN_SAE | animal_vehicle | 24 | 10 | 4 | 6 | 6 | 8 |
| MLPIN_SAE | cat_dog | 1 | 1 | 0 | 1 | 0 | 0 |
| MLPIN_SAE | car_bicycle | 9 | 4 | 1 | 3 | 4 | 1 |
| MLPIN_SAE | pooled_children | 16 | 11 | 5 | 6 | 3 | 2 |


猫狗只有2/1个候选，支持充分的只有0/1个，无法判断频率梯度。车辆各9个中，支持充分只有3/4个，且低中频并未一致增加。以固定方向在新家族的出现率差加总、low+mid质量除以全部锁定坐标质量，Attention由粗类9.62%变为车辆细类8.33%；MLP由32.84%变为21.28%。这些是含未知频率坐标和负贡献的**有符号质量比**，不是概率。MLP显式条件呈局部反向，但新改写并不稳定。

补充[配对差与条件区间](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/results/core_H2_gradient.csv)使用同一16家族重采；猫狗的分母不稳及候选不足原样报告。初始协议笼统的H2 sign/Holm没有被包装成有效频率梯度主检验；这里是带调整尾部区间的条件描述性分析，精确的.975分母稳定阈值为事后数值提示，非预注册验证。详见[修订](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/amendments.md)。逐feature的独立确认符号检验及BH另见[完整确认表](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/results/core_feature_confirmation_BH.csv)，没有用它重新筛出主频率名单。

一个直接反例：MLP输入 **24399** 在主参考10/384篇中出现，属低频；新显式动物16/16激活、交通工具0/16，动物平均z=7.292602，交通工具0。N01原文 `A radio producer chose an animal/a vehicle as the subject of a short segment. The segment has now been recorded.`，末冒号索引22；z为7.196411/0。它的同义、属性方向也复现（BH q=.000340/.001190）。**较低频成员也能区分粗类。** 相反，高频8048（281/384）在新显式汽车16/16、自行车3/16激活，也参与细类区别，但属性措辞下减弱（q=.140），不能称跨措辞稳定专用成员。

频率轴本身依赖位置：24399在S09正文8位置参照中被分为高频（33/3072），同文档末冒号参照却是低频；8048由正文支持不足变为末冒号高频。不能把一个频段当作feature的固有语义层级。频率中性匹配和分源/位置敏感性见[频率模块说明](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/results/frequency_reading_cn.md)。

### 3. 组合：成员可更替，共同成员强弱也可改变；尚未确认超边际类别联合结构

固定共同名单的相对强度方向只在发现集拟合。新显式条件：Attention猫狗13/16合格、投影.063218 [.053309,.074040]；车辆13/16、.011457 [.005491,.016499]。MLP猫狗15/16、.040067 [.037043,.043311]；MLP车辆11/16，低于事先12/16门槛，保留不足。前三项Holm4通过；等范数/同支持匹配随机名单的有效参考不足，**不能称胜过匹配参照**。

两套猫狗在新改写中都反向：Attention−.010648，MLP−.011056。猫的新改写行为仅10/16，狗8/16；属性猫6/16。由此只能解释当前文本条件，不能命名为通用猫狗语义方向。参见[词面与行为图](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/figures/audit_wording_behavior.png)。

保持各类别/措辞每行32、每列激活次数的4链Curveball零模型全部通过约束和规定混合诊断；4个兄弟类别联合差异投影的区间均跨0（Attention .0772/.0868，MLP −.0075/−.0497），没有明确复现发现侧超边际方向。小样本、锁定成员与宽区间仍限制检测能力，不能据此证明不存在联合结构。完整公式、名单、原始值、匹配失败和独立复核见[强度/联合模块](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/results/joint/reading_cn.md)。

## 认识更新与边界

| 假设 | 本轮AI操作判定 | 认识更新 |
| --- | --- | --- |
| H1共享 | 局部支持频率描述 | 跨类共有相对更偏高频；细类额外共享中低频并非两类两SAE一致，边际/家族解释仍在 |
| H2区别 | 未支持一致的方向性直觉；猫狗证据不足 | 粗细区别都可涉及较低频或高频成员，不能按粒度直接分配频段；整体主频率梯度推断不足 |
| H3组合 | 局部支持成员及强弱描述；超边际联合结构证据不足 | 相同成员的相对强度可重复变化，且明显依赖措辞；共现并未自动成为语义机制 |

所有结论限本模型、末层两字典、当前参考语料和文本。直接父类与细类汇总不等价；原留出新统计不是独立验证，新家族仍复用部分词组。行为失败条件没有删除。Top-32退出不等于编码器响应归零：本轮全部11关系/4措辞的退出事件中，Attention8412/10534、MLP4983/7207仍有正编码响应。退出/换入数相等主要来自固定名额。没有测量模型训练效率、路由用途或因果必要性。

两份指定最新20261104原文尚未取得，已完成本地、Pages、文档会话和可见Drive的有界检索；导师方向仅按用户本次转述记录。[来源审计](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/evidence/source_audit_cn.md)列出范围。其余来源、统计、补充前向、图及原始记录已完成；[独立复核](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/evidence/independent_verification.json)12298项0失败，另有300项联合复核。

## 组会讲法与唯一下一问题

“我们用独立自然题干在相同位置给feature划频段，再看16个新家族。跨大类共有成员相对偏高频，但不等于共有只在高频。细类区别没有稳定地转向中低频；相同成员的强弱变化反而很明显，但换措辞会反向，超边际联合方向也尚未复现。因此现在不能把共有高频、区别低频直接用作专家分发规则。”

**AI建议唯一继续检验的问题：在覆盖更充分、仍与目标位置匹配的独立自然参照中，粗细区分成员的频率分布能否在行为可靠的新措辞上保持？**

[详细报告](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/detailed_cn.md) · [完整案例](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/casebook_cn.md) · [执行配置](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/frozen_plan.json) · [运行说明](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/reproduce.md)
