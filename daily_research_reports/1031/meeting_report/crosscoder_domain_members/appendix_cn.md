# 五项分析：定义、完整成员、统计与复现

[唯一中文汇报入口](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/meeting_brief_crosscoder_domain_members_cn.md) · [English companion](appendix.md)

## 定义表

| 对象 / Object | 计算 / Calculation | 分母或边界 / Denominator or limit |
| --- | --- | --- |
| 领域区分度 / domain discriminability | 同一成员的文档平均z在数学高于生物的概率；相等计半次 | 发现每域30文档；留出每域20文档；token非独立文档 |
| 参考发生率 / feature occurrence | 原生共享z>0计数／65536 | 单独DCLM参考；不是激活强度 |
| token参考频率 / input-token frequency | 同tokenizer的token ID计数／65536 | 未见标缺失；已见条件分位数单列 |
| 单位decoder / unit decoder | 最后block27原空间decoder除以L2范数 | 去掉长度；未乘z、RMS或特征值 |
| 参考PCA / reference PCA | R07沿用R04自然发现文本9600真实residual-post位置的1024PC | 固定原基，不用R08混合PCA |
| 逐PC谱分布 / per-PC spectrum | 每个单位decoder与PC内积平方；组内等权平均 | 1024项和1；平方不保留符号 |
| 谱分布重合 / spectral overlap | 各PC两组均值的较小值之和 | 范围0–1；分段合并可提高重合 |
| 实际子空间 / decoder subspace | 两组decoder分别取正交基，再计算主夹角余弦 | 本次rank16/16；平均平方余弦0.07647 |
| 上下文差 / context difference | 同家族／目标／措辞的数学z减生物z | 家族整组重采样；点态区间非多重校正 |
| A/B/C | A有固定token跨措辞响应；B主要词面集中；C证据不足 | 本轮描述规则；旧R09复现资格独立保留 |

## 冻结主名单

下表AUC始终是数学高于生物的原方向概率，生物偏向自然应接近0；主表另给方向固定AUC和原留出点态区间。发现支持是有激活文档数，分母每域30篇；开发10、原留出20也在CSV中。统一字典ID见freeze.json，SHA25609b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628。原生共享z来自14层；decoder只取block27。

| 组/排名 | 成员 | 发现AUC(Math) | 原留出AUC(Math) | 发现支持M/B | DCLM% | 原组/log组 | 上下文 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| math 1 | f8963 | 0.9989 | 0.9825 | 30/24 | 1.8356 | high/middle | A |
| math 2 | f14394 | 0.9989 | 0.9725 | 30/7 | 1.2756 | middle/middle | A |
| math 3 | f11163 | 0.9933 | 0.9463 | 30/21 | 0.6744 | middle/middle | C |
| math 4 | f14316 | 0.9933 | 0.9775 | 30/15 | 0.6912 | middle/middle | C |
| math 5 | f4309 | 0.9900 | 0.9875 | 30/5 | 1.0284 | middle/middle | C |
| math 6 | f12351 | 0.9900 | 0.9975 | 30/7 | 1.2924 | middle/middle | C |
| math 7 | f3098 | 0.9800 | 0.9750 | 30/14 | 0.8347 | middle/middle | C |
| math 8 | f3464 | 0.9756 | 0.9850 | 30/20 | 3.1845 | high/middle | A |
| math 9 | f8030 | 0.9744 | 0.9500 | 30/18 | 1.5640 | high/middle | C |
| math 10 | f7134 | 0.9722 | 0.9425 | 30/13 | 2.6611 | high/middle | C |
| math 11 | f6718 | 0.9711 | 0.9950 | 30/7 | 0.5936 | middle/middle | C |
| math 12 | f10937 | 0.9578 | 0.9825 | 29/10 | 0.7828 | middle/middle | A |
| math 13 | f11420 | 0.9561 | 0.9075 | 29/25 | 2.1118 | high/middle | C |
| math 14 | f14491 | 0.9533 | 0.9750 | 30/17 | 2.3041 | high/middle | C |
| math 15 | f359 | 0.9522 | 0.9250 | 30/29 | 35.2737 | high/high | C |
| math 16 | f1382 | 0.9478 | 0.9750 | 30/27 | 7.6416 | high/high | C |
| biology 1 | f11710 | 0.0000 | 0.0050 | 17/30 | 1.1383 | middle/middle | C |
| biology 2 | f652 | 0.0044 | 0.0200 | 17/30 | 1.5945 | high/middle | A |
| biology 3 | f12141 | 0.0067 | 0.0700 | 9/30 | 0.1511 | low/low | C |
| biology 4 | f598 | 0.0133 | 0.0225 | 12/30 | 0.5569 | middle/middle | C |
| biology 5 | f8838 | 0.0183 | 0.0550 | 7/30 | 1.0208 | middle/middle | C |
| biology 6 | f4862 | 0.0206 | 0.0300 | 9/30 | 0.1862 | low/low | C |
| biology 7 | f1010 | 0.0278 | 0.0650 | 6/29 | 0.2945 | middle/low | C |
| biology 8 | f14278 | 0.0361 | 0.0000 | 11/29 | 0.5478 | middle/middle | C |
| biology 9 | f3477 | 0.0394 | 0.1537 | 8/29 | 0.9460 | middle/middle | C |
| biology 10 | f12266 | 0.0411 | 0.0500 | 30/30 | 42.9947 | high/high | C |
| biology 11 | f734 | 0.0433 | 0.0600 | 7/29 | 0.9491 | middle/middle | C |
| biology 12 | f13132 | 0.0467 | 0.1113 | 8/29 | 0.7706 | middle/middle | C |
| biology 13 | f9491 | 0.0633 | 0.1537 | 5/27 | 0.0595 | low/low | C |
| biology 14 | f6289 | 0.0644 | 0.0775 | 12/30 | 0.4578 | middle/middle | C |
| biology 15 | f15702 | 0.0733 | 0.1825 | 30/30 | 16.5970 | high/high | C |
| biology 16 | f11852 | 0.0744 | 0.0587 | 16/30 | 0.9766 | middle/middle | C |

## 重合与真实子空间的计算


令 d_f 为成员f在block27的decoder，u_f=d_f/||d_f||，p_k为固定PC列。对组G，逐PC分布为：

\[
q_G(k)=\frac{1}{|G|}\sum_{f\in G}(u_f^\top p_k)^2,\qquad \sum_{k=1}^{1024}q_G(k)=1.
\]

数学、生物组各16名，单位方向等权；这里没有激活、范数或特征值权重。重合系数的精确定义是：

\[
O_{\mathrm{PC}}=\sum_{k=1}^{1024}\min(q_M(k),q_B(k))
=1-\frac12\sum_{k=1}^{1024}|q_M(k)-q_B(k)|.
\]

分段先把各64项相加再取较小值，得到O_band，必有O_band≥O_PC。它们衡量组平均平方谱分布，均不是实际方向夹角。若两个单位方向分别为(p1+p2)/sqrt(2)与(p1-p2)/sqrt(2)，逐PC平方分布完全相同，方向却正交。因此另算256对绝对余弦和真实decoder跨度的正交基Q_M、Q_B；后者平均平方主夹角余弦为||Q_M^T Q_B||_F^2/16。本次无秩不足，不把这个量改名为功能重合。


## 名单身份与历史分母

| 名单 | 原名单人数 | 与本次32名交集 |
| --- | --- | --- |
| main_math16 | 16 | 16 |
| main_biology16 | 16 | 16 |
| R04_new_top16 | 16 | 16 |
| R04_expanded_math64 | 64 | 16 |
| R04_expanded_bio64 | 64 | 16 |
| R04_old_shared32 | 32 | 0 |
| R04_old_math16 | 16 | 0 |
| R04_old_bio16 | 16 | 0 |
| R09_math64 | 64 | 5 |
| R09_biology64 | 64 | 1 |
| R09_contribution32_ending0 | 32 | 5 |
| R09_contribution32_ending1 | 32 | 4 |
| R09_union141 | 141 | 6 |
| R09_replicated36 | 36 | 5 |
| R04_same_token_math16 | 16 | 5 |
| R04_same_token_math32 | 32 | 9 |
| R04_same_token_biology16 | 16 | 3 |
| R04_same_token_biology32 | 32 | 6 |

R04_new_top16是两域混合全局前16，方向人数9／7；R04_expanded_*64是自然文档区分度排序。R04_old_*16是更早的原生使用率偏向名单，评分门槛不同；R04_same_token_*是后来同token资格筛选，仍不是本次名单。R09_*64来自受控目标上的符号与方向贡献规则；R09_contribution32按结尾分别选；R09_union141保留其贡献候选并集；R09_replicated36沿用其原复现规则。本轮不把任何一个分母换成本次32，不继承不存在交集的验证结论。全部ID和各自排名在[list_mapping.csv](tables/list_mapping.csv)。

## 频率分组变更

R05冻结等数量三分组并保留相同发生率的并列，20次以下支持不足。R09为自己的频率贡献分析引入log等宽；它没有废除旧分组或改变原z。当前主图恢复旧分组，R09新分组只作对照。边界、完整字典与合格池的分母均在[分组历史](frequency_history.json)、[计数表](tables/frequency_counts.csv)。

## 附图：全名单与方向检查

![32名×16谱段](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/appendix/member_band_heatmap.png)

每行同一冻结成员，16格合计1；两域内部顺序与主表一致。

![逐PC曲线与256对方向](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/appendix/per_PC_and_pair_cosine.png)

上图不合并PC；下图每格是一对数学／生物成员的绝对余弦，不同于谱平方重合。完整主夹角与实际秩保存在[spectrum.json](spectrum.json)。

![全部数学16名上下文](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/appendix/all_context_math.png)

![全部生物16名上下文](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/appendix/all_context_biology.png)

每格分母是一个成员，横轴四目标／措辞，蓝24发现家族、橙12原留出家族，纵轴未标准化数学减生物z，区间为家族bootstrap点态95%。19个全零格在标题保留active0/384，应读作覆盖不足。

## 真实token：完整实例与词频支持

[完整可读实例](real_token_examples_cn.md)保存所有32名的高、普通和同ID低／不激活实例；[原表](tables/real_token_examples.csv)保留完整已读前文与当前token，当前后方文本未输出。每成员每文档最多2例；高激活两例跨文档，普通为正激活中位附近。token字符串由同一tokenizer解码真实输入ID，不来自decoder词表投影。

[成员token统计](tables/token_member_summary.csv)含活跃位置数、活跃文档数、不同ID数、前1/5ID份额、参考未见份额、已见条件频率分位数和token在两域面板的出现比例。[全部成员×输入ID](tables/active_token_counts.csv)与[参考计数](tables/reference_token_counts.csv)给可核查的原计数；两域自然面板分母各9600位置。某ID只在一域出现只说明本面板。

## 未回答与需要前向的缺项

| C类原因 | 成员 | 状态 |
| --- | --- | --- |
| 固定目标始终全零 | f11163, f14316, f4309, f3098, f11420, f11710, f12141, f598, f8838, f4862, f1010, f14278, f3477, f734, f13132, f9491, f6289, f15702, f11852 | NOT RUN：缺自然响应token上的配对前文测试 |
| 已有激活但稳定性不足 | f12351, f8030, f7134, f6718, f14491, f359, f1382, f12266 | NOT RUN：不能从不稳定直接判identity |

这些缺项只登记、不自动运行。A类也没有前文术语／主题之外的语义排除证据，未做因果或功能测试。完整双组频率／支持量匹配背景因f9491格无替代而NA；数学单组匹配可估且已完成。不能用低支持成员替换、保留原候选占位或放宽匹配后宣称原比较完成。token未见导致无条件频率关系未回答，不是identity的负结果。

## 来源、复现与检查

R04正式来源：[Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/summary.md)、[对象设置](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R04_domain_usage_20261027/objects_and_settings_cn.md)。自然文本评分来源：[R04区分度配置](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/domain_discriminability_spectrum_20261028/config.json)。R09旧结果：[Summary](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/summary.md)、[补充A–D](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/supplement_ABCD.md)。完整输入哈希与实际缓存路径见[source_manifest.json](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/source_manifest.json)。

所有新增计算由[analyze.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/meeting_five_20261030/analyze.py)执行；先以--freeze输出freeze.json，再读冻结名单完成五项分析。[render.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/meeting_five_20261030/render.py)只作图；[audit.py](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/meeting_five_20261030/audit.py)从原始输入独立重算。指定解释器为/root/anaconda3/envs/spectral-hier/bin/python，使用本地tokenizers读取原tokenizer.json，不构建模型或加载模型权重。

```bash
/root/anaconda3/envs/spectral-hier/bin/python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/meeting_five_20261030/analyze.py --freeze
/root/anaconda3/envs/spectral-hier/bin/python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/meeting_five_20261030/analyze.py
/root/anaconda3/envs/spectral-hier/bin/python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/meeting_five_20261030/audit.py
/root/anaconda3/envs/spectral-hier/bin/python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/meeting_five_20261030/render.py
```

上述命令只会重算本轮新建执行目录的派生结果；不会自动运行，这里保留复现入口。要在全新目录复现，复制四个脚本和freeze.json并设置原缓存父目录（analyze.py的B、render/audit的B）后先审阅路径；脚本默认用自身目录的父目录作为原缓存根。本轮已完成并停止。统计种子：匹配/普通字典背景2026103001，固定名单文档重采样2026103002（300次），固定目标家族重采样2026103003（每分割2000次）。R04旧留出AUC区间直接沿用旧2000次文档重采样结果，已重新核对AUC本身。

独立检查2795项全部通过；它验证数值和来源，不是科学批准或独立读者理解。导航检查报告已有37项登记／组织问题（多数为未跟踪入口，另有15_25_03缺map、15_27/15_28 map来源陈旧），本次没有改旧Graph、Focus、Anchor或科研状态。输入资产本轮10项及tokenizer严格访问检查通过；这不等于重新验证checkpoint训练资格。没有commit、push或外部发布。


## 表格入口

| 表 | 作用 |
| --- | --- |
| [active_token_counts.csv](tables/active_token_counts.csv) | 本轮离线统计；原缓存只读 |
| [context_categories.csv](tables/context_categories.csv) | 本轮离线统计；原缓存只读 |
| [context_effects.csv](tables/context_effects.csv) | 本轮离线统计；原缓存只读 |
| [context_family_values.csv](tables/context_family_values.csv) | 本轮离线统计；原缓存只读 |
| [frequency_counts.csv](tables/frequency_counts.csv) | 本轮离线统计；原缓存只读 |
| [frozen_list.csv](tables/frozen_list.csv) | 本轮离线统计；原缓存只读 |
| [group_PC_overlap.csv](tables/group_PC_overlap.csv) | 本轮离线统计；原缓存只读 |
| [group_band_overlap.csv](tables/group_band_overlap.csv) | 本轮离线统计；原缓存只读 |
| [list_mapping.csv](tables/list_mapping.csv) | 本轮离线统计；原缓存只读 |
| [master_members.csv](tables/master_members.csv) | 本轮离线统计；原缓存只读 |
| [matched_pool_support.csv](tables/matched_pool_support.csv) | 本轮离线统计；原缓存只读 |
| [member_spectrum.csv](tables/member_spectrum.csv) | 本轮离线统计；原缓存只读 |
| [pair_absolute_cosine.csv](tables/pair_absolute_cosine.csv) | 本轮离线统计；原缓存只读 |
| [real_token_examples.csv](tables/real_token_examples.csv) | 本轮离线统计；原缓存只读 |
| [reference_token_counts.csv](tables/reference_token_counts.csv) | 本轮离线统计；原缓存只读 |
| [spectrum_summary.csv](tables/spectrum_summary.csv) | 本轮离线统计；原缓存只读 |
| [token_member_summary.csv](tables/token_member_summary.csv) | 本轮离线统计；原缓存只读 |
