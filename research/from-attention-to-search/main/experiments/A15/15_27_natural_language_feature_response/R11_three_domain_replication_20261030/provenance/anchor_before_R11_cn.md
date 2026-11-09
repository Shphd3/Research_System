# A15_27_04：领域偏向成员的频率、共同谱几何与输入响应

## 1. Problem Definition

父问题是原生CrossCoder如何响应自然文本与受控前文。用户本轮明确续接：从全字典文档区分成员出发，描述其频率、共同谱位置和词面/上下文关联。旧小名单及目标词分解不回答全字典问题。这里沿用现有自然语言响应Focus，一轮R10缓存分析；比较会更新描述性认识，不自动授予语义或因果机制。科研接受与关闭Unknown。

## 2. Physical Priors

用户给出三条待检验直觉及竞争解释：少见成员承担区分，或高频成员靠强度差；两域分占不同谱位置，或位置相近但响应不同；跨措辞上下文，或词汇/格式及交互。均不是预设事实。字典是固定坐标系，不等于互斥语义词条。

## 3. Falsifiable Hypotheses

H1检验低频相对支持合格池富集；H2检验两域平均单位decoder平方投影相对频率/支持匹配背景的差别；H3检验固定目标的领域响应能否跨措辞和已暴露家族划分复现。未见效应可能削弱直觉，支持不足只能判无法回答，不能把未激活判identity。

## 4. Mathematical Model

每文档响应为\(r_{df}=160^{-1}\sum_{t=32}^{191}z_{dtf}\)，包含零。原始区分度\(A_f=P(r_{mf}>r_{bf})+\tfrac12P(r_{mf}=r_{bf})\)。至少一域有5篇发现文档激活，且\(\max(A_f,1-A_f)\ge.75\)的全部成员冻结主集合与方向；该指标只识别稳定响应排序。

真实block27 residual-post向量以单一共同均值计算发现集协方差，得到按方差降序的正交PC\(p_j\)。单位decoder\(u_f=d_f/\|d_f\|\)的逐PC量\(q_{fj}=(u_f^Tp_j)^2\)全谱和为1。组分布是成员等权平均\(Q_{gj}\)，谱重合\(O=\sum_j\min(Q_{mj},Q_{bj})\)；分段会隐藏差别，平方分布相同不推出方向相同。实际使用另算\(v_{dtg}=\sum_{f\in g}z_{dtf}d_f^{model}\)，先求和后投影平方，保留交叉项，不能当完整表征方差解释率。

## 5. Computational Realization

固定A22原生14层共享z、原门控，block27 decoder与真实h同hook及模型单位。R04每域30/10/20发现/开发/旧留出文档，每篇160位置；独立DCLM频率65,536位置。共同谱60发现文档共9,600位置、1024PC满秩；R07复用同谱，不是独立语料。R08保有48家族×2域×2措辞×2目标后缀的384目标z；R09保有TRAIN-RMS还原decoder。本轮无新前向或训练。

## 6. Minimal Falsification Tests

冻结主集合后依次完成五项：feature频率组成；单位谱及PC1拆分；两域谱重合与独立呈现的实际贡献；真实token高响应频率；固定目标上下文及目标+后缀对照。Top16/64/128和AUC0.70/0.80仅作冻结敏感性，不替换主集合。低频认识必须对比池；特殊几何必须对比匹配背景；固定词不激活仅算不足。纯换词B缺失时写NOT RUN方案，不扩展前向。

## 7. Current Evidence

R10缓存统计完成：全字典16,384→支持合格10,076→主集合433数学/527生物；原留出357/431区间下界超过0.5，所有成员保留。频率可判定者高频66.7%/54.3%，池44.1%，没有低频富集。前64单位份额均值10.03%/11.52%，主要来自PC2–64；两组主集合前偏均值在A01细匹配参照内，特殊性依赖冻结截取敏感性；逐PC谱重合0.9493、分段0.9686，未高于匹配参照。实际组能量随输入改变。固定目标至少一条件的上下文复现33/21；789成员所有划分始终全零。既有R07谱经raw-h审计与本轮共同谱完全一致。详见[Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/summary_cn.md)。这些是已暴露数据上的描述/探索结果，科研接受Unknown。

## 8. Claim Boundary And Next Decision

可以描述本字典、本批文本的频率、几何、重构能量及输入关联；不能推出领域专有知识、相同功能、因果重要性、学习干扰或MoE收益。纯目标词替换和真正独立谱稳健性仍缺。按用户范围完成缓存统计、图表、原始数据与复现入口后停止，由研究者判断这三条认识如何更新；后续前向需另行确认。[Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/protocol_cn.md)限定执行。
