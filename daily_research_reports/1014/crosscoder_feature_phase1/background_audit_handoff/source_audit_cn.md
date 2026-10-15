# 阶段一既有证据只读审计与转交记录

## 目的

裁定展示的高组成列表重叠是否主要由普遍背景造成。这里记录审计线程实际读取的材料和可核验事实；后续统计计算唯一由原对话执行。本文不修改旧结果、主图阈值、审批或科学状态。

## 模型

本机 `SLAI2025008379` 的既有 SSH 配置：别名 `mig-cci`，HostName `118.145.32.132`，Port `11109`，User `root`。未猜测地址、改认证或安全配置。实际连接容器hostname为 `app-110ebd7841a6480ebe272362b5d54844-6cd8b84d9b-zjdqg`，初始工作目录 `/root`；持久研究目录为 `/data/250010109/Research_System`。

读取 `/data/250010109/AGENTS.md`、Research_System根AGENTS、项目 `Projects/from-attention-to-search/AGENTS.md`，以及仓库 `research-reasoning-auditor`、`problem-anchor-writer` 和其自包含／判断契约，报告与数学写作指引。用户本轮明确要求中文，公式不使用美元分隔符；沿用该要求。

联合CrossCoder固定14个偶数residual-post层、16384共享特征。TRAIN冻结阈值0.051281172782182693。完整VAL10,485,760位置，D5,238,097／V5,247,663，81个连续上下文块，128上下文/块，尾块保留。原文档／近重复独立性未知。V图仅复核D原始边，不是独立重新发现V边。

模型来源为 `/data/share/Qwen3-0.6B-Base`，revision `da87bfb608c14b7cf20ba1ce41287e8de496c0cd`；最终checkpoint为 `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt`，已有input_identity记录checkpoint SHA256 `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`、训练曝光999,997,440。此线程只读身份记录，未重新加载或重哈希该权重。

数据来自既定DCLM direct bins：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/data/direct_dclm_bins_a15/data_manifest.json`，manifest SHA256 `874794a8657f8982f7abb12ee517ec551fce840d9f20dfe103f48589a6779849`。118条文本记录的source_bin为 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_0_of_10_shard_00000001_processed.bin`，可由固定index_val与有效位置映射到10,249个上下文；原文档ID未知，不能将bin称为独立原文档。14层使用同一token配对，10,485,760位置不能乘14作为独立样本数。

## 待裁定解释

共同项比例、背景频率、直接共激活和学习收益是不同量。87.5%只能指出展示的组成列表多数共同项属于发现侧最高频10节点，不能单独裁定全部关系无意义，也不能宣布排除背景后仍稳健。新诊断的删除／匹配口径均为探索性，保留原主结果。

## 已核实结论

1. 两对高J展示的是同一8项列表：[14,516,5913,7388,7415,8060,10807,13964]；其中7项属于固定D Top10，故87.5%=7/8。不是全图比例、全部高J的平均，也不是16个独立共同项。Top10按D支持数降序选取，同分按ID；已保存频率约81.5%–99.3%。非Top10共同项14在V仍有67.934%频率。
2. 1／17的V直接共同激活2次、lift0.0285154721；1／242为245次、lift0.6793952118。两对组成列表均J=1，不代表常常同时激活，更不能直接代表内容相同。0／3为0次、0／4为7次。两对低J的正式D/V列表均非空，因此这两行的低J不是空列表所致；20个支持充分空列表节点另有诊断表。
3. 候选选择存在代表性限制。源码每个极端有理J组最多保留8个代表，并按A/B ID排序；它尝试少共享ID，但最终高J两对都用1、低J两对都用0，频率没有匹配。已有高J并列排名115,027,260–120,380,886；不能从四对外推全群体。候选池资格也用了V侧支持≥200、V列表非空，因此V已参与筛选，不是完全隔离的确认集。逐个删除Top10均J不变未排除共同支配。

原边审计保存发现214,711、复核通过206,136、失败8,575、约简146,947。已有完成核对报告214,711条逐块计数与D/V加总一致，16384节点命中与原验证逐项一致，118文本位置／类别／z核验一致。以上是既有核对记录，本线程未重新推理、计数或重新验证大型缓存。

## 实際材料与证据地址

研究系统根路径记为 R=`/data/250010109/Research_System`，执行侧结果根记为 E=`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z`。

| 实际阅读材料 | 实际绝对路径／字段 | 本地可读副本 |
|---|---|---|
| 1014日报讨论入口 | R/daily_research_reports/1014/meeting_report/meeting_brief_crosscoder_feature_phase1_cn.md | 摘要已完整核对，本文保存关键含义 |
| 完整便携包入口 | R/daily_research_reports/1014/crosscoder_feature_phase1/reading_bundle/README.md | [README](reading_bundle/README.md) |
| 中文Summary／Detailed／原Anchor／Protocol | 同一reading_bundle/documents下相应文件 | [Summary](reading_bundle/documents/summary_cn.md)、[Detailed](reading_bundle/documents/detailed_cn.md)、[原Anchor](reading_bundle/documents/anchor.md)、[Protocol](reading_bundle/documents/protocol_cn.md) |
| 候选4行 | E/candidate_metrics.csv；pair_id 1_17、1_242、0_3、0_4 | [候选表](reading_bundle/selected_tables/candidate_metrics.md) |
| 组成列表、共激活、87.5%分母、并列排名 | E/pair_metrics.json；pairs对应pair_id，lists／supports／background_common_items字段 | [pair_metrics](reading_bundle/selected_provenance/pair_metrics.json) |
| 固定Top10与逐个删除 | E/sensitivity.json；top10_discovery／versions.frequency_D／fixed_candidate_rows | [sensitivity](reading_bundle/selected_provenance/sensitivity.json) |
| 候选选择与Top10定义实现 | E/code_snapshot_v2/candidates.py；pair_search／sensitivity | 已只读检查源码，冻结身份见[源码清单](reading_bundle/selected_provenance/code_snapshot_manifest_v2.json) |
| 空列表低J诊断20行 | E/empty_list_J0_diagnostics.csv | [诊断表](reading_bundle/selected_tables/empty_list_J0_diagnostics.md) |
| 118条随机／高激活展示，完整读完 | E/pair_examples_cn.md；JSON保存model_visible_prefix、目标位置等 | [可读文本](reading_bundle/pair_examples_cn.md)、[JSON](reading_bundle/selected_provenance/pair_examples.json) |
| 16幅局部图，均实际查看 | E/figures/local_0_00至05、local_1/3/4/17/242_00至01；研究复制R/sync/1014_crosscoder_feature_phase1_evidence/ | [本地图目录](1014_crosscoder_feature_phase1_evidence) |
| 14层热图，实际查看 | E/figures/layer_contribution_heatmap.png | [热图](1014_crosscoder_feature_phase1_evidence/layer_contribution_heatmap.png) |
| 原始逐层数值 | E/layer_contribution.csv | [逐层数值](reading_bundle/selected_tables/layer_contribution.md) |
| 输入身份、既有完成核对、来源清单 | E/input_identity.json／completion_audit.json；reading_bundle/manifest.json | [输入](reading_bundle/selected_provenance/input_identity.json)、[核对](reading_bundle/selected_provenance/completion_audit.json)、[清单](reading_bundle/manifest.json) |

复制的44个小文件（含17幅图）全部与原便携包manifest中的reading_copy_sha256匹配；没有重哈希模型checkpoint或大缓存。见[复制哈希核对](reading_copy_hash_audit.json)。local copies保持原文，少数仓库相对图链接依赖原仓库结构；本文提供本地图入口，最终ZIP会保存可读入口。

## 读图和文本观察

局部图箭头是统计包含方向；深度是图上最长出路径，不是模型层。图中1→7415的V条件概率0.8019低于该节点背景0.92938，这说明原门槛不是“相对背景富集”的判据。节点0→327和0→10915则呈现明显超出背景的候选统计边。不把高J代理受挫扩为全图没有可检查关系。

**读图数字更正**：本线程初读时将局部图中附近的737／605标注对应到0→327，转交时明确请原对话按原始数值核查。原对话已交叉检查原始边表、总计数矩阵及81块加总；0→327正确D/V共同支持为765／600，V条件概率0.8849557522、背景0.0121724661、lift72.70143491，原始边row_index=1。0→10915为719／566，V条件概率0.8348082596、背景0.0100109325、lift83.38966033，row_index=35。最终以原始表为准，不保留初读错误作为结果，也不据此断言旧图或统计代码错误。

高J列表的三个锚点1／17／242都深度1，指向相同8个叶节点；0有32直接邻居、深度3。低J可能和约简后邻居所在层级不同有关，不能把J=0讲成原图可达对象或背景完全不共享。

热图左侧为逐特征层间幅度占比，右侧为含零位置的平均z乘decoder范数。共享z使左图等于范数占比。0在第2层占比约0.486；1／17／242的晚层占比更大。这是decoder几何描述，不是功能或层内独立关系。图明确保留第28层FVE86.4722%、替换CE+0.305962nats的工具边界。

完整读完118条展示文本：0的随机与高激活多见officer词族；1的高激活多见序号，3个高激活位置同在上下文10239；17的高激活多见姓名碎片，随机例更多样；242的高激活多见医学引用，both多例集中于上下文3196／3197。仅是阅读观察，不能称单义语义或独立文本复现。目标token的门控激活决定类别；右文不是模型当时可见信息。1/17的两个both属于低激活、不同上下文；0/3没有both，按实保留。选例集中程度待原对话用已有记录核查。

## 原对话连接与分工

通过远端现有正式app-server的WebSocket control socket，复用仓库已用的AppServerClient，调用thread/read准确读取指定线程。未直接读取 `/root/.codex/sessions`、任何会话数据库或修改对话存储；未启动新app-server。原对话标题“1013-CrossCoder 分析目的讨论”，cwd R、idle，最近已完成阶段一和1014便携包commit/push。本轮不继承为新的commit/push授权。

UTC2026-10-13T21:59:31.396728，正式turn/start接受准确指令，轮次 `01a13747-234c-7f82-998a-08829f82a3e8`，原线程ID不变、无配置覆盖。见[准确prompt](prompt_to_original_thread_cn.md)、[发送回执](send_receipt.json)、[独立anchor](crosscoder_background_audit_anchor_cn.md)。UTC22:01:30.577092通过turn/steer补充上述两行反例和文本集中现象，未新增一套工程；见[补充指令](steering_notice_cn.md)。

原对话已回话确认有限CPU分析、不重复推理／完整共同计数／全池排名、不分配GPU、不commit/push；已严格查资产当前可访问。由它实施背景lift核查、共同Top10删除的重约简与仅过滤区别、少量D侧频率／列表大小匹配对照并交付。审计线程不运行这些统计。原对话执行前记录固定D频率0.8–1.25倍、D列表大小完全相等、D支持≥200、排除6个展示节点、种子20261014，每高J对最多32对；不按J/V/text换对象，也不在不足时放宽匹配。当前容器8CPU时间核、128GiB，最多2进程；预估交付15–25分钟，主动计算1–5分钟，非承诺截止时间。

父对话最新澄清已补进新anchor第2／5节，并于UTC22:04:47.535510正式turn/steer送入同轮次；初版保留为[anchor初版](crosscoder_background_audit_anchor_v1_cn.md)，原send_receipt的hash对应该初版。补充强调高频不等于无意义，删除仅诊断指标依赖，固定名称“过滤原组成列表的重叠”与“原始图删节点后重新约简的重叠”。见[澄清文本](anchor_clarification_01_cn.md)。

最终结果由原对话独立落到R/daily_research_reports/1014/crosscoder_feature_phase1/background_audit_results/；本线程已完整阅读Summary／Detailed／discussion与文本核查、查看3幅新图，并审读analyze.py。最后把图3遮挡低J点的图例移到绘图区外，原对话执行且未重跑统计。UTC22:24:13.597514正式thread/read确认同一轮次completed、error=null，最终回答明确停止。完整结果说明见[parent_report](parent_report_cn.md)，[完成回执](completion_receipt.json)保留原最终回答。运行无阻塞；语义、原文档独立性和学习收益仍未回答。
