# A15_27_05_01：Dense 表征在 0.5B–33B 训练 token 内的谱与方向动态

## 1. Problem Definition

问题是：同一 Dense 训练轨迹中，方差规模、方差分配、主子空间、文本关系和外部类别信息，是否在相同训练进度内趋稳？[谱位置与语义粒度主 Anchor](../15_27_05_spectral_semantic_granularity_anchor_cn.md)已有的是固定 Qwen 表征的证据，不能回答 Dense 的训练动态。研究者于2026年11月1日激活并授权本轮设计、审计、smoke及正式只读分析。B表示十亿累计有效预测token；模型参数为281,431,040。本轮不训练语言模型或字典。要判断的是头、中、尾的时间顺序能否支持分工的动力学解释；路由设计效益另需证据。

## 2. Physical Priors

假设同一轨迹的模型坐标兼容，输入完全配对。方差排序不是已知语义层级，33B也不是已知收敛真值。有限文本抽样会使接近简并的方向看似漂移。另一竞争解释是坐标旋转仍在发生，但样本关系近似保持。

## 3. Falsifiable Hypotheses

独立回答A方差规模与分配是否趋稳，B承载方差的方向是否继续旋转，C方向变化时文本关系与类别可读性是否趋稳。“头部先、中尾后”只是待检验猜测。若变化持续、反弹，或中尾没有可复现增量，应削弱该解释；若变化落在抽样不确定性内，只能限于当前估计精度回答。

## 4. Mathematical Model

一个观测是固定文档前缀中固定自然位置的1024维隐藏向量。训练进度t的参考矩阵为H_t，每个checkpoint使用自己的参考均值mu_t中心化。

\[
X_t=H_t-\mathbf1\mu_t^T,\qquad C_t=X_t^TX_t/(N-1)=V_t\operatorname{diag}(\lambda_t)V_t^T.
\]

X_t的奇异值是s_i=sqrt((N−1)lambda_i)，协方差特征值是lambda_i。trace(C_t)表示总方差；p_i=lambda_i/trace描述方差分配；effective rank定义为exp(−sum p_i log p_i)。这些量是描述性估计，不是训练目标。

同维正交基U、V的U^TV奇异值给出主夹角余弦，归一化投影距离为sqrt(1−||U^TV||²_F/k)。全1024维恒等空间不用于方向稳定性证据。中心化线性CKA比较配对评估样本的关系；Procrustes只在参考集拟合满足det(R)=+1的正交矩阵R，使||X_tR−X_33||最小，不学习缩放，独立评估残差仍保留规模差异。固定末端基中的方差diag(V_33^TC_tV_33)不是早期自身特征值谱。每个checkpoint、每种谱基均按相同TRAIN/DEV规则重新拟合线性分类器。

## 5. Computational Realization

[清单](../checkpoint_spectral_dynamics/manifest.json)冻结12个实际可读兼容状态及原始摘要，缺失权重单列。主测点是原生模型final_raw_h，即最后block residual-post、norm之前。已有pre_mlp_input位于另一位置，不能混作本轮缓存。2,048条N8自然文本各使用256token前缀的32个固定位置；参考与评估各1,024条、32,768向量，每条权重相同。现有数据缺少论文级身份，只能按记录近似家族划分。均值、谱基和对齐只拟合参考集。

另复用R12的96篇同一the文本及其192token序列、位置、外部标签与文档家族划分，只在Dense重新前向作为语义桥接。主比较为原始坐标下前16/64/128/256维，以及头1–64、中481–544、尾961–1024维。并排报告原始漂移、对齐漂移和CKA。早/中/晚固定0.5/17/33B，仅这三点补block0/3和标签读出。[Protocol](../../../../../experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/protocol_cn.md)冻结具体计算和执行边界。

## 6. Minimal Falsification Tests

用恒等、纯旋转、缩放和样本打乱检验实现：谱相同不能推出原始方向相同，CKA不变不能推出总方差相同。主要证据为各相邻距离及除以真实十亿训练token间隔后的变化率，并与配对文档拆分波动比较。本轮没有有依据的通用稳定阈值，因此不估计“趋稳起点”；只展示曲线及抽样参照0.5/1/2倍的敏感性。早、中、晚与确定规则选出的最大谱变化率转折点各做8次固定配对参考拆分，得到描述性范围；不能称为模型重复或校准后的总体置信区间。读出增量须通过配对留出区间和预定Holm校正。全空间不可读、区间宽、谱间隙不足及checkpoint缺失均保留不足状态。

## 7. Current Evidence

完整有界分析已完成，12个可读Dense状态、参考/评估各32768向量、18个层位状态及126个读出条件均保存。31→33B总方差86733.1→83565.4（−3.65%）；归一化谱TV0.03068，对33B拆分中位参照0.00721。前16/64维原始距离0.4409/0.3948；中/尾0.8425/0.5991，抽样参照0.8800/0.6617，后两者方向时序分辨率不足。评估CKA0.95503，原始/正定向旋转后残差0.60855/0.35742，说明漂移含旋转成分且仍有剩余变化。自身基领域头部0.5/17/33B读出94.6/94.7/94.7%；数学细类全空间61.1/88.9/83.3%，首点证据不足；生物细类全空间83.3/100/100%。中尾同维新增0/36通过主对比Holm校正。上述为直接观测及有界AI解释，不是研究者机制接受。

[Summary](../../../../../experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/summary_cn.md)解释五类答案；[Detailed](../../../../../experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/detailed_cn.md)保存完整过程、来源、失败和修订。A01将对齐限制为det(R)=+1；A02清除无依据名义网格，12个实测状态不变。8个有manifest而权重缺失状态明确保留。

## 8. Claim Boundary And Next Decision

本轮没有建立头部先固定、中尾随后稳定的顺序，削弱将该顺序当作既成动力学依据的解释。它不否定真实时间分工可能存在，不替未完成路由训练判断效益。结论限于单一Dense轨迹、固定学术文本与pre-final-norm测点；记录级独立性近似、R12历史暴露与细类小样本限制语义解释。半集拆分只是抽样参照，不能将中尾敏感性写成永不稳定；未估趋稳起点，33B不是最终收敛真值。类别可读、样本关系近似、原始方向与原生功能分别解释。

唯一下一项研究者决策是，审阅这些曲线及抽样/标签限制后，是否保留头/中/尾时间分工作为待检验的动力学解释。完成条件为研究者确认有界认识；从Summary与覆盖账本继续。科学接受和问题闭合Unknown，工程分析已完成。没有自动新增实验。


### W01：用户激活的原生权重后续分析，2026-11-01

研究者已明确将下一测量对象改为模型权重，区别于文本表征。12个可读checkpoint的57个独立二维矩阵已另立[协议](../../../../../experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/weight_spectral_dynamics/protocol_cn.md)并完成[事实测量](../../../../../experiments/A15/15_27_natural_language_feature_response/checkpoint_spectral_dynamics/20261101/weight_spectral_dynamics/summary_cn.md)，分别测量输出/左侧与输入/右侧第一方向及前64维空间；不中心化、不使用文本抽样。本条只记录范围激活、完成事实与阅读入口，不替换以上表征证据，不构成科学接受。容差条件起点、首方向不可辨识等结果由原始表拥有；研究者解释与任何最终收敛判断仍待交互讨论。
