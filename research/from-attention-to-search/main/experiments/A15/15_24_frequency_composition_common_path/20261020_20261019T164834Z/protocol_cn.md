# Protocol：频率混合表征与高频路径调用的有界分析／学习

## 0. Approval Snapshot

状态：APPROVED_FOR_BOUNDED_ANALYSIS_AND_CONDITIONAL_LEARNING。用户明确要求自行建模、分析后验证假设，并批准提交4卡H100 Reserved，无需逐步审核。此授权不认可H-L为真。问题为同top2下保留高频路径的增量是否依赖频率组织；不声称检验旧top1与top2的纯计算优势。正式Anchor为对应frequency_composition_common_path/anchor_cn.md；Focus保持原状。类型：root-cause audit＋模型指导的有限方法对照。A–G由AI在本次明确委托内操作化并自审，科学结论仍待研究者讨论。

## 1. Terminology / Definitions

feature频率p为TRAIN有效答案预测位置中z>0比例；不是z幅度、末层z×norm、token频率或语义难度。B1…B4是原四个正频率对数等宽段，U单列。组对是一个频段的两个候选专家，R同编号只是随机组对。高频路径不是已认证共同功能模块。路由top2含2个不同专家，权重固定1/2。目标接收与q都用原始全部z；top2总专家负载和为2而非1。

## 2. Anchor Alignment

先定位混合token/feature结构与评分代理，再区分“高频特定调用”与一般固定路径的策略效果。数学关系、假设与边界见Anchor，报告不能只堆谱和负载。18条导师intuition逐项标可测、局部、未测，不把含糊转写补成事实。

## 3. Tested Hypothesis

H-T当前token身份不足以解释全部feature与频率组成；H-G真实中心化PCA的承载与均值/幅度不同；H-L ΔT<0且I<0。主学习指标共同T-B1逐featureDEV NLL；支持需实际改善而非只较少恶化，配对对话区间和两seed完整公开。

## 4. Rival Explanations

当前/目标token身份、格式/来源、低支持、一般共享路径/负载变化、组大小及更新次数、冻结工具的非正交和失配均是活对手。T使用每段哈希均分子组，不使用旧φ，避免将关系细分作为频率效用。R匹配8人数，不匹配组内频率。四臂完整h、Base都相同。

## 5. Data Construction And Provenance

复用sft_route_learning/20261019T012300Z缓存：TRAIN85548/1024对话、EVAL22446/256、DEV10340/128。TRAIN/EVAL已用，DEV在已核查旧训练/分析入口未读取比较，但已有提取与旧路由；只称本轮新固定复核，不称独立新语料。核对精确prompt/assistant hash交叉，近重复未验证。所有标签是t预测t+1，首答案预测在prompt末位，EOS计目标；padding不入缓存。

## 6. Learning Task And Permitted Supervision

只用原答案target做NTP/SFT CE，所有有效答案位置统一平均；token未来值仅结果分析或监督，不进入路由。Base/head/CC冻结；专家全h输入。低B1和高B4定义共同来自T原频段，不能给R换评价目标。每feature支持与重叠报告，缺项NA。

## 7. Model / Architecture And Frozen Variants

共享14层z，末层raw decodernorm，现成h28 prefinalnorm。新T：原频段内按SHA256(seed:fid)排序，均分2组；R：全15477正频率池按独立种子hash排序，按T八个组大小分配。B1成员原频率定义不变，零命中907项只参与组成。TRAIN均值只计算一次。F两个最高校准组对，H固定第4组对＋其余最高，段内原幅度最大组；平局最小ID，zero/fallback单列，不删输入，每位置2distinct IDs。

8个bias-free SwiGLU1024×1024×1024普通FFN，共25165824参数；激活2个，每token两个专家6×1024² MAC。残差输出为原h＋scale×两FFN输出平均；scale=sqrt(E_TRAIN||h||²/1024)，无均值减法。初始化每seed同CPU随机上投影、down=0；Base路径原样。

## 8. Training Objective And Optimization

仅答案CE；无负载均衡、无辅助谱loss。AdamW lr3e-4、betas(.9,.95)、eps1e-8、wd.01、clip1，1epoch168steps，batch512、micro128，warmup9steps，cosine到lr比例.1。每条件85548目标，同seed同PCG64顺序。梯度loss按实际全batch有效位置平均，不能按专家各自归一化。初始化、数据与预算配对；tensorboard遵循仓库observability合同。

## 9. Conditions, Seeds, And Checkpoints

T_F/T_H/R_F/R_H各seed11/22，共8模型。step0、42、84、126、168记录TRAIN及已暴露EVAL学习曲线；DEV只所有模型完成后终点一次，不调参/选轮。保存2个共享init、42/84/126模型，168完整model/optimizer/RNG/cursor/valid计数；不覆盖旧模型。所有同终点，不能不同步数拼最好结果。

## 10. Primary Metric And Frozen Analysis Plan

L为DEV中每个B1 feature激活位置NLL平均，再对有命中特征等权。两seed报告独立值及均值；ΔT=TH−TF，ΔR=RH−RF，I=ΔT−ΔR。主支持需ΔT和I均负，主对话bootstrap1000次区间均不跨0；否则描述改善/阴性/不足，不宣布稳定机制。实用量级预登记0.01nats只作实用标记，不能把统计负值自动当有用。两seed同向、均值及区间全部报告；不作总体显著性或多模型普遍结论。整体、low位置union、high宏/union与所有源NLL同交；以同对话共同重采样维持配对。无命中feature为NA，非零激活但未接收为0。

## 11. Secondary Metrics And Guards

静态：全feature current/target top-ID纯度、召回与支持；current-ID条件均值对B1份额的EVAL/DEV MAE/R²和首答案剔除；TRAIN预选每段4feature（TRAIN>=5hits、>=3对话、最小固定hash），复核2随机正/1高/1同ID未激活文本。只给可计算代理，不语义命名。

真实h TRAIN PCA k=1/16；频段向量有符号β、decoderη、偏置/残差与交叉项一并报告，随机正交方向参照。PCA不是参数W谱，不能证明优化主导。

路由：全q/接收、负载和非空槽、实际更新量/梯度步、F/H路线相同率、强制路径无本组激活、同输入多owner与原top1失败分解；事后宏接收oracle仅上界非部署指标。完整原z/c一直评价所有条件。

## 12. Known Good / Known Bad / Known Confusing Cases

好例：单一已知feature可重算分数与两专家；坏例：标签错shift、空/负分母、重复专家或drop token必须拒绝；易混淆：强制路径0mass仍调用是干预本身，不能伪装内容匹配；top2 q与负载sum2不能套top1sum1；初始down零但up不零，初始梯度上投影可能0而down必须有梯度，更新后上下均核验。

## 13. Scientific Procedure And Stage Contracts

S1完整读两报告、18intuition分类；资产与位置、只读源码核对。S2 TRAIN冻结统计、PCA、名单与代码，再EVAL/DEV同型复核。S3 检查F/H确有不同分配、统一top2与无泄漏，完成表征结果先汇报。S4在既定8模型上做GPU smoke通过后正式1epoch；smoke只TRAIN小样本，不用DEV调方案。S5统一最终DEV揭示、配对结论与负结果、限定下一决策。

训练门槛不要求静态H更漂亮；只要求策略有实际差别、原始信息/位置一致，静态无法决定的学习差异值得测。若策略完全相同只复用结果，不制造重复计算。

## 14. Algorithm, Output, And Provenance Contract

所有字段、种子、路径、资源在config/frozen.json。代码/缓存/日志/权重在执行侧；Anchor与Protocol在项目。读本地资源只分析CPU8线程总额，RSS16GiB；训练一节点4H100Reserved，existing envelope image shphd-lite-0911，总CPU8、RSS64GiB、每卡allocated16GiB，新增磁盘24GiB、训练主动35分钟、总主动墙钟120分钟。外部排队单列。禁止Spot降级、新Base/CC训练、跨预算继续、自动commit/push。分支失败继续不依赖的部分。

## 15. Success / Failure / Insufficient Evidence

工程PASS不等科学支持。主指标与边界按第10节，完整阴性必须交；没有收益就修正“共享高频调用”假设，不回头调频段。若所有训练连TRAIN也异常恶化，统一两候选LR(3e-4、1e-4)仅用共同TRAIN smoke取能下降且有限者；若需改正式lr，先append修订、统一所有条件且不得窥DEV。只有训练下降验证上涨属于过拟合，不归咎实现。

## 16. What This Cannot Claim

不能证明稀有知识掌握、语义难度、从头容量扩大、feature自然正交、common等于高频/首主方向、因果attention来源、φ效用、top2比top1同算力收益或共同语义中介。旧top1结果不充当新top2因果对照。

## 17. Block Confirmation, Freeze, And Amendment Ledger

本轮属于用户明确委托的自主建模与有界执行，A问题/B数据/C监督/D模型/E优化/F对照/G资源由本文件与config逐项固定，自审PASS才运行。它不把任何AI机制建议改写成人类科学确认。新方案设计：移除旧关系组、使用频段内均分，避免此前单项/不稳定关系混杂；此变化执行前登记，与旧T_S1等不是同模型。执行后只追加修订与结果链接，不按结果调整主定义。
