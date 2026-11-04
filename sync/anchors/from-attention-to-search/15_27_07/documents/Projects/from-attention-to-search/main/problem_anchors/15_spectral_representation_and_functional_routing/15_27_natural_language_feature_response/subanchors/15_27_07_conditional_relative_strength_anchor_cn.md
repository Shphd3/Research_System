派生阅读副本；原件位置：`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_07_conditional_relative_strength_anchor_cn.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_07_conditional_relative_strength_anchor_cn.md)；研究修改仍回到原件。

---

# A15_27_07：固定成员上的相对强弱

## 1. Problem Definition

H1 冻结的共同集合 C 中，相对强弱是否提供超出二值支持与总强度的细标签信息？

## 2. Physical Priors

CrossCoder原子是未知真实feature的观测代理。文本的语义包含不直接推出字典成员包含。措辞、整体尺度、来源和抽样都是竞争解释。

## 3. Falsifiable Hypotheses

在二值支持 b 和总范数 r 上加入归一化逐成员强度 q，跨措辞改善留出对数损失。

## 4. Mathematical Model

固定官方 Qwen3-0.6B-Base（28块、1024维）；A22 联合读取1、3、…、27层，产生16384维共享原子响应。测固定回答前后缀的最后token。原尺度末块重建为偏置加各 z_i D_i 之和，保留残差。仅 CPU L2逻辑回归在发现集拟合，开发集选择正则。构造矩阵面板的可逆性标签跨家族一致；粗条件为Unknown。频率来自300篇自然发现文档，不来自语义面板。

末层原尺度 decoder 范数为 d_i，定义 u_i=z_i d_i，r 为 u 的二范数，q=u/(r+1e-12)，b_i=1(z_i>0)。比较 [b,r] 和 [q,b,r]。C 不按细标签重选。活跃支持完全相同的配对作为独立子集报告。


D1实际观测模型：两处独立block27 SAE（30000成员、ReLU-Top32），分别为残差相加前的attention o_proj输出，以及残差相加／RMSNorm后的真实MLP输入。各用自身编码、decoder、频率边界、C/F及状态编号；A22联合14层CC仍单列残差输出参照。加权响应u=z乘自身decoder范数，不作跨字典坐标对应。

## 5. Computational Realization

384条构造材料：48矩阵家族×三条件×两措辞，加96条非矩阵对照。24/12/12家族及相关定理组整组划分，定理组为6/3/3。复用600自然文档，按300/150/150划分。执行[冻结协议](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/H2/protocol.md)与[修订](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/amendments.md)。

### 2026-11-04 研究者激活的自然语言层级轮次

本轮目的：通过动物→猫／狗、交通工具→汽车／自行车及跨大类对照，观察成员更替和共同成员的强弱搭配如何对应自然文本。当前用户明确授权设计、执行、检查、结论更新和打包。旧矩阵命题及S02–S05冻结结果保留。本轮H1是共同使用与换入换出的可复现关联；H2是共同成员强弱搭配的可复现关联。它们是本轮可观察命题，不替代旧的额外信息／功能命题。

竞争解释包括显式词复制、同义词和属性提示、模板／后缀／位置、固定Top32竞争、整体幅度、字典重构及小样本筛选。本轮固定两个大类各16家族，模板整体8发现／8留出，三种措辞及椅子／石头负类。相同末尾Description:冒号取样；两套原生SAE分别分析。共同成员既报告逐对交集，也报告发现集固定列表；q为固定列表原始z除其L2范数。零范数未定义。

最小检验是留出家族内的成员关系对照、固定共同列表的联合相对差及改写／属性复现。若仅显式词成功，更新为词面条件下的组合候选；有效对照下不复现则未支持对应预测；行为或共同成员资格不足则证据不足。H3/H4和真实router训练留在parking lot。研究者科学接受及关闭仍Unknown。

当前状态：S06有界计算完成，科学接受Unknown。具体协议与先于推理的冻结规则见[本轮Protocol](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/protocol.md)。

### S07干预补充：2026-11-04研究者明确授权

主S06完成并保存后，研究者授权对发现集固定组合临时删除／重组强弱。注入原表征加decoder线性改变量，保留原重构残差。按发现频率／强度／数量及实际扰动范数设对照，原留出文本读取完整候选分数、词表排名／分布与跨域变化。此补充检验局部输出敏感性，不判定唯一自然机制或真实概念转换。[S07完整协议](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S07_feature_interventions_1104/protocol_cn.md)。启动时状态NOT RUN；科研接受Unknown。

## 6. Minimal Falsification Tests

一个留出损失主差，给家族95%区间，另报定理组敏感性和两种措辞。跨措辞方向不一致限制内容解释。

用户于2026-11-03明确启动R17_D1：保持本Anchor原命题，在末层Attention输出SAE与MLP输入SAE各自重测；分别使用自身字典、激活及自然频率。旧CC单列参照。修正后的旧发现／开发拟合，24新家族288条主材料及48条单因素材料锁定只测试。修正必须实际进入全部受影响H1–H4，保留旧结果并记录重算范围。

[D1 protocol](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/protocol.md)

## 7. Current Evidence

执行事实及AI解释分别见[路线Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/H2/summary_cn.md)和[Detailed](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/detailed_cn.md)。附件v0.2原稿保留指纹；数学符号修订版复用已暴露留出。科学接受Unknown。结果引用不改写冻结假设。


D1 completed bounded computation2026-11-03: H2 no-answer relative-strength gains−0.28474/−0.01238; stable cross-cue claim not supported. [Current D1 synthesis](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/summary.md) / [中文](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/summary_cn.md). Two nativeSAE routes and independent CC reference each retain originalhypothesis, before-input old48, corrected-old48 and locked-fresh192 results. Original results are not overwritten. AI verdict is evidence-limited; researcher scientific acceptance and question closure remain Unknown.

### S06 bounded result evidence · 2026-11-04

本轮完成384条、两套SAE、16模板簇的固定8/8划分、全部行为／H1／H2／改写对照与数值复核。ATTN_SAE/vehicle: estimate=0.027506352770407007, n=8/8, Holm p=0.015625; ATTN_SAE/animal: estimate=0.040139372458710784, n=8/8, Holm p=0.0234375; MLPIN_SAE/animal: estimate=0.00478142999113622, n=7/8, Holm p=0.0234375; MLPIN_SAE/vehicle: estimate=0.05304508942780347, n=5/8, Holm p=0.03125。这些是激活坐标中的局部操作统计，完整列表复现、反例、跨措辞资格和AI分支判定由[本轮Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/summary_cn.md)拥有。H1重叠子预测不能代替具体成员复现；H2不适用配对保持缺失资格。旧候选和S02–S05原件保留。本轮任务事实完成，科学接受、机制判断和关闭仍Unknown。

### S07 completed local intervention evidence · 2026-11-04

主S06文件保留；完成96原留出前缀、14976干预条件。Attention动物alpha.5相对同成员等范数打乱的正确边际损失差0.00623nats，[0.00135,0.01340]，8家族，Holm p=.03125；主要条件仍16/16正确。共同大组删除经常增强正确边际并改变无关域分布，完整删除匹配不足；交通工具反侧预测未支持或共同支持不足。该结果只支持有界decoder方向敏感性。[干预Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S07_feature_interventions_1104/summary_cn.md)拥有完整数值和AI分支判定；科学接受、唯一机制、关闭仍Unknown。

S07追加控制几何审核：Attention交通工具的2成员固定范数列表只有1个角度自由度，16条目标/打乱有6条近同向、10条近反向；有限方向对比不代表任意独立组合控制，跨类差异亦可能来自控制能力。主统计和名单未改。

## 8. Claim Boundary And Next Decision

结论限于固定模型、字典和面板的静态对应及可读性。下一科学决策Unknown，等待研究者阅读；明确标记的AI假设修正建议见Summary。学习收益、原生因果使用和router效用需独立证据及授权。
