# S10详细报告：定义、统计、竞争解释与执行记录

## 阅读顺序

行为与条件：[逐文本候选分数](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/results/behavior_confirmation.jsonl)和[逐标签分母](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/results/core_behavior.csv)。表征与组织：[中文总结](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/summary_cn.md)、[全部逐家族配对](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/results/pair_family_frequency.csv)、[全部锁定feature确认](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/results/core_feature_confirmation_BH.csv)。功能与质量：本轮没有功能干预；[独立数值复核](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/evidence/independent_verification.json)与[联合复核](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/evidence/joint_independent_verification_all.json)只验证缓存、接口和算术。旧S07干预另报。

## 对象、分母和频率

一条文本末冒号是一个向量；整个家族才是独立单位。类内或类间feature数不是样本数。Attention与MLP输入各30000维，模型和SAE冻结。11个真实类别配对逐个报告，不混合同父细类和跨父细类。直接父词与汇总子类不等价：汇总类的presence为两个子类0/1的等权均值，强度为rawz均值，重叠为4跨父子类pair指标均值。后者不是support并集，也不是另一个32成员向量。

参考384篇来自固定S09 discovery IDs，三源各128，保留原首至多128token，追加固定后缀，读取冒号。以实际token ID为准；截断末边界解码再编码可能不同，未伪称完全相同。count>=8支持充分，支持内三分位不拆同次数；0次和1–7次单列。分源128文档以及原正文8/后4位置轴另存，2000次文档bootstrap按三源各128重采。频率组的不确定性未完全传递到每条主区间，因此区间是以固定参照分组为条件。

## 共有和机会参照如何算

逐对交集为两行z>0的共同坐标，Jaccard为交集/并集；每个家族先计算再平均。每频率组同时报告字典坐标基数、两侧活跃机会、交集/退出/进入和rawz。类别边际p_A、p_B可给交集期望sum(p_A*p_B)，不能直接代入J。整条B向量在家族间错配保留每行32、各列次数和幅值，全部候选对实际计算J；这个参照同时打断模板背景对应。它不能证明或否定类内联合语义机制。

发现侧共同名单要求显式共现>=6/8，另两措辞各>=4/8。A保留完整名单，C取排序前8且固定。区分名单要求显式出现率差>=.25、另两措辞同向>=.125，强度差至少2/3措辞同向；全30000坐标筛选。RMS尺度固定于原144发现行，含0。amplitude-only另列，不与出现率名单混用。确认只使用锁定ID/符号；反向和0保留。

频率富集参照只匹配发现presence/幅值，不能同时匹配参考频率本身；强度复现参照才另匹配频率组。256预算、分箱3、>=75%匹配门、失败不松阈值。C的同support随机参照进一步要求同维和足够激活，实际没有形成足够有效预算，所以不称胜过匹配参照。

## H1/H2/H3的统计解释

H1四个显式主比较为直接父类高频共有份额减两个siblings，分别两SAE，整家族2000bootstrap、精确符号随机化、Holm4。3/4通过只支持当前频率描述，不能自动提升为超边际规律。所有父子和4跨父细类以及三种措辞控制均保留；CI跨0不能证明没有差异。

H2固定方向的质量是每个锁定feature新出现率差乘发现符号后求和。low+mid为较低频；unseen/insufficient没有被叫低频。质量比可能因负贡献超过概率范围，分母非正为NA。最初笼统sign/Holm约定无法直接成为这种比值的有效随机化检验；补充分析明确留空p，报告同16家族重采的条件描述性比值差和调整尾部区间。不能把两个单独CI的大小当成差值检验，更不能把猫狗少候选与不稳分母包装为无低频区别。>=4名单/>=3支持是确认前固定；.975正分母比例只是事后数值提示。全部修订及结果曝光时间见amendments。

H3的q是固定名单z除该名单L2，0范数不定义；只有两侧支持完全一致且至少2成员才是纯强弱。显式发现方向固定后投影，新条件要求>=12/16家族资格。CI主条件于eligible家族，并另做统一16家族重采敏感性；不在不同eligible集合之间伪造独立比较。强度主4Holm，其余原措辞62和新措辞22单列。不是训练或因果作用。

联合结构另以每类/措辞精确行32与各列次数Curveball重排，4链100burn/10thin/64样本，混合不足仅固定扩至128一次。各label和各siblings独立24成员全276对，发现侧残差方向先锁，确认不重拟合。0方差约束和正的forced基线不能当证据；主投影需双Holm4（nullp和family符号）及CI/混合均合格。所有4主区间跨0，检测能力有限，结论是未明确复现而非结构不存在。联合公式与全部零模型审计保留一次于results/joint/reading_cn.md。

## 竞争解释与反例

显式四类新行为全16/16；同义猫/自行车各14/16；属性猫6/16；新改写猫10、狗8/16。不因行为失败删数据。两个猫狗q方向在新改写反向，不能称普遍语义。48最简短上下文可出现部分原方向，仅说明词面线索可能足够，不是唯一原因的因果隔离。显式6类同家族token位置一致；其他措辞长度/位置不同，词长、信息内容和模板仍混杂。父词不是细类混合的同义物。

Top32保留/换入换出平衡来自固定名额；退出后多数编码器仍正。整体L1/L2、原始值、名单范数和q并报，不能把总尺度误作比例。模型/字典重构、有限题干参照、类别词重复与小面板都限制推广。S08没有独立格式匹配，S09只对它自己的自然正文频率检验，不能把83–97%套到层级面板。

## 案例、运行和来源

两SAE各4个不同家族，由first/median/lowest规则选，完整原文、索引、所有并集成员z/p_ref/group见casebook_cn.md和core_case_values.csv。N10 Attention车辆低重叠例、MLP低频粗区分24399、新改写反转是保留的反例。图中最多8坐标不代替完整名单。

CPU4/FP32/eval/no-grad，没有GPU/云训练；参考121.70秒、新确认193.47秒、短上下文25.66秒。候选每个2token，求完整条件log概率，父类gold=None；所有prefix与4lane检查通过。旧文件逐个SHA保存；参考推理启动代码版本原样保留并匹配启动SHA。首次数值导入前protobuf失败，只修环境。原代码、旧结果、旧权重没有覆盖。来源审计、3轮规则审核、原协议和时间戳修订都保留。

两份最新命名文档未找到，不臆造导师原话；当前用户转述就是此次假设来源。12,298项独立缓存检查、300项联合检查通过，不赋予科研接受或问题关闭。大文件原位并给字节/哈希索引，结果包内容见README与payload_manifest。没有commit/push或外部发布。

完整数值对照表与英文逐项执行记录见[detailed.md](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/detailed.md)；[coverage_ledger.csv](/data/250010109/MoE_Router/experiments/20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S10_frequency_shared_discriminative_1105/coverage_ledger.csv)逐条说明完成、探索、缺失和证据不足。
