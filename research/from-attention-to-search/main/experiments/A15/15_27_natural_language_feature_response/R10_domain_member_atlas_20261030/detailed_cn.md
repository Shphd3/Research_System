# R10详细证据记录

[完整结果](summary_cn.md) · [冻结协议](protocol_cn.md) · [定义](definitions_cn.md)。本轮为一个固定模型的缓存描述实验；已暴露数据相关统计为DONE_EXPLORATORY，数值恒等核对为DONE_VALID。科研接受与关闭Unknown。

## 数据、单位与复用

R04的120个原文档组互不重复，每域30/10/20发现/开发/原留出，固定160位置，平均含零；独立DCLM的256窗口65,536位置与本批原文档组不重叠。全字典16,384坐标；OR门槛和原始文档配对概率由逐位置稀疏z独立复算；Mann–Whitney秩和复现全部AUC。成员在任何留出/几何统计之前写入freeze.json并冻结。

真实h与decoder都对应block27 residual-post、final norm之前；h不先L2归一化或白化。共同谱直接使用60发现文档9,600真实h，单一共同均值。旧R04/R07基正好满足本次权重；raw-h均值误差0、特征方程残差约1.8e−15、正交误差约3.4e−15、完整秩1024，因此复用而不另造PCA。R07并非独立稳健性参照；R08最后目标词谱也不能替代全部token谱。

R09 decoder用TRAIN_RMS27=374.3495121024576还原模型单位。原生BF16门控z保持不变；离线向量分解按保存权重做FP64计算，不冒称新增原生BF16前向复现。组向量不含共享bias/均值，因为它们不归某个入选成员。先向量和再投影平方，与直接模型坐标路径误差约5e−14；四种组×输入条件齐全。保存错误的“成员平方能量之和”作数值对照，不能替代主读数。

匹配背景从整个支持合格池含主集合抽样，按A01实际发生率半octave区间及总/最大域支持各5篇区间，每层精确同规模、无放回、两组不重叠，1000次。包含主集合约40.0%/40.5%，属于条件字典背景，不是独立零假设或选择波动区间。所有stratum和ID保存。AUC重采样单位为文档；上下文重采样单位为成套家族，所有条件一起带走；点式标签不作多成员确认性发现。

token计数用19,200位置并按ID保留标点子词；类型分位点1/2次，同频不拆。阈值仅用发现正z，严格>；支持不足62/55只离开该组成图分母，仍在960主表。完整逐成员高、普通激活及同ID低响应实例，以及每ID数学/生物次数保留执行侧，不用未来文本。384个目标条件按seq_id对应；每个数学/生物配对及E0/E1目标位置相同，跨家族位置30–38，目标ID各后缀固定。E0/E1仅核心前文相同，整后缀也改变，故B仍缺。

## 三类审计与修复记录

科学识别审计：频率池、几何匹配、方向检查、实际贡献和固定词控制分别对应竞争解释；不跨越功能/因果边界。数据统计审计：完整文档划分、独立参考分组、点式探索区间及不换人均保留。实现审计：5009项通过，0失败；全谱投影和误差约1.1e−15；训练、优化器、参数更新、模型前向均0。审计文件provenance/numerical_audit.json保留每项证据。

修复记录：独立审计最初误读旧字段CC_all_native为未还原范数，源代码说明已乘RMS，修正比较对象。FP32保存范数对FP64重算相对误差1.32e−7，以1024项标准舍入误差界核验，未改变decoder或筛选。脚本缩进在运行前编译检查发现并修复。覆盖核对发现3名成员只在开发集激活，将“始终零”改为全划分检查，最终789名；上下文复现规则和主集合未改。实际图片检查修正symlog线性阈值未设置和图例拥挤，数据不变。去最高10%均值、维数参照超出比例和top5词集中性为附加描述诊断，未用于挑人。

## 覆盖与复现

| 请求 | 状态 | 边界 |
|---|---|---|
| 全字典筛选、频率及敏感性 | DONE_EXPLORATORY | 新主集合960，不拼旧32分母 |
| 共同真实谱、单位几何、PC1拆分 | DONE_EXPLORATORY | 验证旧基等价，无独立参考支持 |
| PC/段重合、匹配背景、余弦/子空间、四条件实际能量 | DONE_EXPLORATORY | 几何/使用不等于功能 |
| token计数、高阈值、逐成员真实例子 | DONE_EXPLORATORY | 本语料内频率、支持分母分开 |
| 固定词A及目标+后缀敏感性 | DONE_EXPLORATORY | 大量目标未覆盖，逐成员点式标签 |
| 纯目标词B | BLOCKED / NOT RUN | 最小48新前向方案另列，须确认 |
| 真正独立自然谱稳健性 | BLOCKED | R07同基，R08目标谱不替代 |

脚本见scripts/，执行根/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030。保存源hash、freeze、全部16,384筛选、960主表、旧新全映射、完整1024投影、全部家族配对、真实例子、重采样/匹配索引及绘图原表。研究库只放精选小证据；raw数组与完整大表留执行侧。README给命令。旧结果不覆盖；本地阅读同步不等于提交或推送。完成缓存支持范围后停止，下一决定归研究者。

## Final delivery checks

Static CPU read verified the actual A22 checkpoint SHA09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628 and exact equality of all cached model-scale block27 decoder coefficients to TRAIN_RMS27 times checkpoint decoder. No model constructed/forwarded. All local deliverable links and eight-section/balanced-math Anchor checks pass. Input207-file and execution output manifests match bytes. Navigation checker has38 issues vs37 preexisting: the new child is registered in anchor_ownership and linked from Focus/day/reading entry; its derived research-map entry remains pending. Existing research Graph was outside this request. See provenance/navigation_check.txt; this does not alter scientific measurements.

## 2026-10-30近单域token补充的事实记录

[补充报告](supplement_near_domain_tokens_cn.md)另冻发现集31数学/24生物，严格14/15；不替换父960。留出近单域复核19/21、严格复核8/13，成员全保留。高响应构成支持25/18；真实token、同ID匹配、未配对状态、盲前文提议和事后对象空白栏已保存。18类独立缓存/分母/冻结/文档配对核查通过；主图A/B及参考频率图完成显示检查。人工语义核查PENDING，未将标签提议当科学结果。

两个实际输出资产：`analysis_a15_27_r10_token_context_audit_20261030`与`analysis_a15_27_r10_near_domain_token_context_20261030`，通过[当前访问检查](/data/250010109/Research_System/assets/checks/2026-10-30_r10_near_domain_outputs_20261030T0445Z.json)。源/输出manifest在两个新增presentation目录，精选证据在figure_variants/near_single_domain_20261030。旧组会总稿逐字节副本与哈希保留在history及meeting_history_receipt.json，当前总稿已整合新结果。新前向/训练/PCA为0；来源覆盖、人类标注和科学接受边界不变。38项导航问题仍为原检查结果，没有编辑Graph或关闭问题。


## 合并简图补充（2026-10-30）

用户要求合并数学生物并减少图中文字。新增[简图说明](figure_variants/pooled_simple_20261030/README_cn.md)保留55/29原名单，另列全部缓存另一域零激活16名（7/9），作为描述子集而非留出复核。token类别新增全缓存输入覆盖口径，区别于旧发现冻结分类。原生z>0主视图与原p90高响应附录分开，分母、类型数和位置份额显式保存。无新前向/训练/PCA；旧稿逐字节保留。
