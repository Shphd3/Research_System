# S17 详细证据、算法与字段

[Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/summary_cn.md)拥有原始数据→结果分析→认识更新→唯一下一步。此支持轮接续同一R17_D1，不改变S14/S15/S16或Focus/Anchor科学状态。输入使用、CPU缓存统计与当前用户请求一致；附件新增前向先审批的界限仍保留。[protocol.md](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S17_expert_feature_mixture_1108/protocol.md)与config.json在本轮新增统计前固定，但旧CONF早已暴露，不能声称盲确认预注册。

## 真实输入与资产身份

S15/data/token_records.jsonl保存6912原始记录的文本、标签、家族、场景、DEV/CONF、四表达、token_ids和两位置索引。S15/data/token_routes_without_hidden.npz保存[6912,2,...]：indices/values末维32、selected/weight2、probability/logits8、metrics6及load_bias8。轴1固定colon/body。值全部正；R是整token选择，G每位置和为1。没有重载模型、再算原始前向或使用SAE重建替代实际路由。

父模型身份和原生hook/路由/重建质量继承已核查S15记录；当前strict访问在evidence/input_access.json，输入/代码精确哈希在evidence/freeze.json。模型与SAE仍是普通MoE33B的同一对资产，不与Qwen编号混用。当前实际消费的是缓存，未在本轮再加载或全哈希大型权重文件；源权重身份由原记录与缓存冻结链持有。

Q/G来自S15/reference_frequencies.npz完整30000坐标，分别是原生S14题干6000和DCLM6000的末冒号出现率。辅助频率分箱count0、count1–4、支持count≥5的全参考坐标三分位，在data/frequency_bin_definitions.json。正文只借用这些标签与DEV角色，不能当原生正文参考或跨位置语义确认。

DEV576显式colon位置决定候选9对：原53坐标每侧至少24活跃/24不活跃、各至少4场景；高φ≥.5且共同12位置/4场景，低φ≤0，各端点度≤2。4高5低而非满10；屏幕data/DEV_pair_screen.csv完整保留，不按CONF挑边。φ和幅值cosine不可混称相似；低_3φ负但幅值cosine约.58就是定义差别。角色范围按DEV逐标签12/24家族和4/8场景定义，只是使用标签数。输入全观察1825坐标，主CONF实际702；固定候选缺失行另保留。

## 概率、背景、区间与未运行检验

code/common.py composition计算joint=X.T@R，P(feature|expert)=joint/Nexpert，反向=joint/Nfeature。匹配背景为sum_c P(c|expert)*P(feature|c)，先类别内再汇总。P(feature|expert)全坐标和32，反向和2，均已核对。成员列表每坐标权1，事件权重为joint；完整背景的可能成员支持比少量接收样本的实测成员多，不把独特成员数差当公平富集。事件加权背景采用相同类别比例。

固定53成员×8expert的pooled及24类内结果分别保存。bootstrap对16场景整体重采2000次，保留每簇3家族及24标签依赖，区间是原始差值，不是相对null或等价区间。合格需feature活跃/未活跃各12位置8场景、expert入选/未入选各12位置8场景且入选比在.05–.95。八条件全部无expert合格；因此没有运行富集p或专属搭配p，所有这些p及计划10600项Holm为NA，不虚构1或“不显著”。计划族53×8×25=10600，各条件单列；未来若出现意外合格对照，冻结代码会停止而非临时乱换null。

主要expert6全选使差值0是代数恒等，不是排除影响的证据。expert1未选侧只有2场景、expert7入选只有2场景，虽可算原始差值，不能论稳定选择。场景/类别/位置/表达分别显式保存；两个位置分别为ID25和624，身份相同但绝对索引和上下文长度不同。旧条件长度层退化的缺口未被本轮CPU统计修复。

## 输入搭配参照与准则评估

code/organization_analysis.py报告9对的DEV/CONF φ、Jaccard、真实共激活计数、共同/仅一侧token、各自场景数、LOSOφ、R/2和gate-profileTV及场景区间。相似对常为包含关系，g-only太少；低相似对也可能共同出现，必须区分同token不可独立路由与不同token缺乏硬分离。

Curveball是输入二部图degree-preserving参照：每scene×label块3行，随机两行分出独有坐标，合并后均匀重新分配相同数量，公共成员不动。每行永远32，每个坐标在每块计数不变；四链每链250draw、burn20整块sweep、thin5sweep。端点保全约束和p独立核对。Rhat>1.1或不变null留不足，不伪造p；有变动的6对Rhat约1.00。高尾／低尾方向继承DEV高/低选择，Holm计划10含缺失一项。有限MCMC与旧数据探索限制保留，不是严格独立随机实验；家庭跨标签配对并未被这种输入重组完整保留。expert几乎全接收/稀有，不继续其“独有”搭配检验。

analysis_addendum_01.md明确一个事后补充：跨feature活跃token集合的完全相同expert对比例，排除同一原始token自配。分母NfNg−Njoint，分子expert组合计数内积−Njoint；共享expert数另去掉2Njoint贡献。更严格的f-only/g-only集合不交。其笛卡尔对数不是独立样本，未作二项推断。该描述及N029/N051排除TV在单独补充表，冻结主程序未改。

## 文件与行数

| 文件 | 含义 |
| --- | --- |
| results/all_observed_feature_expert.csv | 49,008行，全观察成员的双向概率/计数/背景/支持；含776缺失候选，反向分母为0留NA |
| results/candidate_enrichment.csv | 3392行，8条件×53×8的pooled候选区间、资格、未运行p |
| results/candidate_within_label.csv | 81,408行，另含24类分层；与pooled不可当独立重复 |
| frequency_summary/ecdf.csv | 每成员或事件权重的均值/逆CDF分位与完整累积分布；Q/G分开；背景清单支持与实样本列表区别在note |
| role_frequency_joint / sharing_range_frequency | 角色交集bit0–7及DEV标签覆盖数×参考频率分箱；不强制语义优先级 |
| pair_relative_roles / nonexclusive_role_composition | 旧各类别对角色与全局任一对角色分开，分母为32×位置数，重叠标签可超过100% |
| expert_overlap / overlap_region_frequency | 每条件28对expert，交集/两独有/均未选；共用和独有部分的频率清单及事件画像 |
| leave_one_scene_and_family / main_leaveout_feature_enrichment | 所有16场景LOSO，额外N029/N051/both家族排除；保留全样本主结果 |
| fixed_pair_alignment / different_token_route_overlap | 9对×8条件；相似性与硬/权重TV，后者为A01不同原始token重合，非独立对数 |
| input_pair_coactivation_null | 9对真实边际与共同数、1000参照、Rhat、不变null、p及计划10校正；不代表expert机制 |
| data/input_pair_null_draws.npz | 4×250×9共同计数；四链最终完整1152×32端点另存，用于degree约束核验 |
| data/observed_dictionary_coordinates.csv | 1825全缓存观察ID的旧DEV角色、使用范围和原生Q/G频率 |
| results/position_token_inventory.csv | 8条件位置ID和索引范围；身份实际固定，非泛化自然token |
| casebook_cn.md / data/case_rows.jsonl | 真实输入与行号、两成员激活、整token专家权重、例外与不可判定案例 |

## 复算与实际执行

composition约26秒、organization约61秒，全部CPU；无模型forward或GPU工具调用。代码模型无关合成矩阵检查平衡无关联差0、植入关联差.5、全选/全活跃不可识别，通过不算MoE证据。独立verify.py从原始token记录逐条重新建Counter、类背景、接收集合，覆盖48,232观察行/256频率均值/224重叠，最大误差3.33e−16；额外776缺失候选的NA及9对不同token重合由verify_addendum.py核对，误差0。Curveball端点每行32和所有块频次、p复算通过；sourcehash未改。

无运行失败。organization中个别正文条件LOSO φ无定义产生All-NaN提示，原样留NaN/缺失，不改成零或挑另一位置。图一初稿角色图例覆盖部分柱面，图二高相似标签接近，已仅改布局再检查。追加source_architecture_audit是实际原生模型/训练/config的只读实现核查，未改训练设置；其无SAE相似目标结论不当作加入新目标的效用证据。

主复算：`python code/verify.py`与`python code/verify_addendum.py`，需原S15地址可见；阅读包另含消费缓存的原字节副本与portable_replay.py，不含模型权重或hidden（本轮不用hidden）。原源码冻核之外，包装只变链接，不变数值。科学接纳与下一步新位置执行均待研究者决定；不commit/push/发布。

便携点值复算的路由与参考数组均改为一次加载以消除解压开销；首版和中间版均自然完成，两次停止请求时已无匹配进程；最终版2.15秒通过，前两版与实际过程有记录。这项导出修复不更改已冻统计和原始独立复算。
