# A15_27_09：罕见配置与内容对应

## 1. Problem Definition

常见单原子状态能否形成罕见配置，跨语境对应细数学内容，并提供加性状态之外的增量？

## 2. Physical Priors

CrossCoder原子是未知真实feature的观测代理。文本的语义包含不直接推出字典成员包含。措辞、整体尺度、来源和抽样都是竞争解释。

## 3. Falsifiable Hypotheses

有限发现选择的双原子状态配置具有稀有性，跨语境复现目标内容，并可能增加所有单变量状态主效应之外的信息。这是三个分开的主张。

## 4. Mathematical Model

固定官方 Qwen3-0.6B-Base（28块、1024维）；A22 联合读取1、3、…、27层，产生16384维共享原子响应。测固定回答前后缀的最后token。原尺度末块重建为偏置加各 z_i D_i 之和，保留残差。仅 CPU L2逻辑回归在发现集拟合，开发集选择正则。构造矩阵面板的可逆性标签跨家族一致；粗条件为Unknown。频率来自300篇自然发现文档，不来自语义面板。

从 H1 的 C∪F 取至多8个高频原子；自然发现正值75分位分弱／强；至多20对、80配置，选择至多10个。单状态频率至少.01；发现联合频率至多.005，支持至少30位置和10文档。自然验证与语义面板读出分别报告。


D1实际观测模型：两处独立block27 SAE（30000成员、ReLU-Top32），分别为残差相加前的attention o_proj输出，以及残差相加／RMSNorm后的真实MLP输入。各用自身编码、decoder、频率边界、C/F及状态编号；A22联合14层CC仍单列残差输出参照。加权响应u=z乘自身decoder范数，不作跨字典坐标对应。

## 5. Computational Realization

384条构造材料：48矩阵家族×三条件×两措辞，加96条非矩阵对照。24/12/12家族及相关定理组整组划分，定理组为6/3/3。复用600自然文档，按300/150/150划分。执行[冻结协议](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/H4/protocol.md)与[修订](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/amendments.md)。

## 6. Minimal Falsification Tests

验证稀有性要求同时频率上界≤.005，并满足支持和单状态门槛。内容对应需匹配可见前缀标注。独特增量需同时优于加性和匹配配置，按2M校正。自动标注局限明确记录。

用户于2026-11-03明确启动R17_D1：保持本Anchor原命题，在末层Attention输出SAE与MLP输入SAE各自重测；分别使用自身字典、激活及自然频率。旧CC单列参照。修正后的旧发现／开发拟合，24新家族288条主材料及48条单因素材料锁定只测试。修正必须实际进入全部受影响H1–H4，保留旧结果并记录重算范围。

[D1 protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/protocol.md)

## 7. Current Evidence

执行事实及AI解释分别见[路线Summary](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/H4/summary_cn.md)和[Detailed](../../../../experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/detailed_cn.md)。附件v0.2原稿保留指纹；数学符号修订版复用已暴露留出。科学接受Unknown。结果引用不改写冻结假设。


D1 completed bounded computation2026-11-03: H4 ATTN support11positions/6docs; MLPIN rarity upper.005156; target enrichment2/0; semantic correspondence insufficient. [Current D1 synthesis](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/summary.md) / [中文](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/summary_cn.md). Two nativeSAE routes and independent CC reference each retain originalhypothesis, before-input old48, corrected-old48 and locked-fresh192 results. Original results are not overwritten. AI verdict is evidence-limited; researcher scientific acceptance and question closure remain Unknown.

## 8. Claim Boundary And Next Decision

结论限于固定模型、字典和面板的静态对应及可读性。下一科学决策Unknown，等待研究者阅读；明确标记的AI假设修正建议见Summary。学习收益、原生因果使用和router效用需独立证据及授权。
