# Conversation Memory: 1028-句内Feature延续与旧图关联

Conversation name: 1028-句内Feature延续与旧图关联
Conversation ID: 01a180fc-1484-78d2-acc7-24b8db77739e
Processed by: Codex (harness: Codex VS Code app-server; model: gpt-6-astra)
Created at: 2026-10-28T05:40:14Z
Latest update at: 2026-10-28T08:32:44.558792+00:00
Continues from: none; consulted the named 1026 and 1028 source conversations, not resuming or overwriting their logs
Environment: repo=/data/250010109/Research_System; project=/data/250010109/Research_System/Projects/from-attention-to-search; exec=/data/250010109/MoE_Router; all visible

## 2026-10-28T05:40:14Z -- 创建本对话记录，固定独立问题与设计阶段

Processed by: Codex (harness: Codex VS Code app-server; model: gpt-6-astra)

- Summary: 用户固定问题：一句话前面token的feature，后面是同坐标延续、通过旧图与不同坐标相连，还是不再出现；H1/H2及高频、重复token、领域背景、活跃数量、节点度数竞争解释已明确。用户要求先阅读26号与28号对话，构建新的Anchor/Protocol，再分析数学/生物缓存；范围不含训练、重聚类、大规模新前向或干预。用户确认参考论文是Anthropic 2023 Towards Monosemanticity，并要求简述Cunningham等另一篇、给当前对话命名并建立memory。
- Current work: 已通过正式thread/name/set命名并thread/read核验；当前独立owner为A15_28，problem_key=sentence_feature_continuation。已写双语Focus/Anchor、一页设计入口、当前资产preflight与两论文方法说明；Protocol双语正在完成与独立审阅。H1/H2 NOT RUN，未生成新结果图或案例，不把资产核查当成假设结果。此次按用户“先构建...然后分析”的顺序完成设计阶段；缓存分析范围本身已获指示，不能以后重新索要同一总授权。AI新增匹配、句界、随机化和统计参数在Protocol中标建议，不冒充用户逐条批准。
- Verified sources: 两条指定对话分别为1026-自然语言Feature：上下文响应与关系组、1028-领域区分性：Feature 选择与激活差异。已核当前A15_27固定目标语义响应owner；其R06/R05既有结果保留，不能当作新句内检验结果。
- Asset boundary: R04数学/生物各60篇、192token原生CSR可读；DCLM频率参考独立且沿旧分组；完整A22图passV原始边兼容，箭头为同token非对称共现，频率规则使其无环，不是语义层级。SAE历史图接口等价未合格，H2独立受阻，H1不阻塞。文本均已暴露、句界未标注。详实数值与来源只由preflight持有。
- Next action: 完成并核对Protocol、源链接/数学源码、编号导航与本地Anchor阅读包，追加本log交付checkpoint。后续先冻结只看文本的句界和匹配规则，再开展缓存统计；不能因低支持逐结果改门槛。主对话看结果后决定是否做上下文替换，当前不授权干预。
- References: `Projects/from-attention-to-search/main/focus/focus_sentence_feature_continuation_cn.md`（问题与四类状态）；`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_28_sentence_feature_continuation/15_28_sentence_feature_continuation_anchor_cn.md`（科学设计）；`Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/protocol_cn.md`（精确合同，尚在写）；同目录`one_page_cn.md`、`preflight_cn.md`、`literature_methods_cn.md`与`provenance/`（阅读入口与事实来源）。机制判断和问题关闭Unknown。

## 2026-10-28T05:49:58Z -- 设计与可行性阶段交付完成

Processed by: Codex (harness: Codex VS Code app-server; model: gpt-6-astra)

- Summary: 新A15_28双语Focus、八节Anchor、18节Protocol草案、一页说明、preflight和论文方法说明已完成；旧A15_27科研owner未改写。独立冷读与论文检查已完成，修复了H2条件丢失集合、随机基线固定mask、度与频率不变量、示例排序字典及无延续/非正超额的区别。正式H1/H2仍NOT RUN，未产生三类结果图、实测两例一反例或正式统计脚本；不能把本阶段当最终分析交付。
- Current work: 当前阶段完成。新文件15份Markdown源链接无缺失，Anchor 8节/Protocol18节结构通过，4份数学源码通过；这些不是渲染或科学批准。阅读包`sync/anchors/from-attention-to-search/15_28/`生成并--check确认Current，含原字节/hash、原生资产与对话来源摘要、草案/Unknown状态。仅本地同步，未commit/push。全库导航保留两条开始时已有问题：MISSING_MAP_ANCHOR 15_25_03和STALE_MAP_SOURCE 15_27；新增15_28无新增该类问题。
- Next action: 向研究者交付一页入口和具体Protocol方法选择。后续接受当前设计或修正影响解释的参数后，先实现文本盲审句界清单及匹配覆盖审计，再按冻结规则做缓存统计。固定文档伙伴会造成规则性支持损失，必须与全库本就无同ID的稀缺分开。原缓存范围已获用户指示，不重讨总授权；训练、重聚类、额外大规模前向、干预和发布仍无新授权。
- References: `Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/one_page_cn.md`（首先阅读）；同目录`protocol_cn.md`（AI新增匹配/统计建议与精确范围）、`preflight_cn.md`（实际资格）、`literature_methods_cn.md`（两篇原论文）、`provenance/source_validation.json`和`provenance/independent_design_review.md`（检查与已落实修复）；`Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_28_sentence_feature_continuation/15_28_sentence_feature_continuation_anchor_cn.md`与`main/focus/focus_sentence_feature_continuation_cn.md`（相对于同一project的科学owner）；`sync/anchors/from-attention-to-search/15_28/README.md`（本地派生阅读包）。

## 2026-10-28T08:32:44.558792+00:00 -- 授权缓存分析、三类图与双语结果交付完成

Processed by: Codex /root (harness: Codex desktop; model: unknown)

- Summary: 用户在解释H1/H2、三类图及距离读法后，明确要求按固定思路执行缓存分析，并要求先给定问题／表征组织，再给结论与认识更新，最后分析证据。原范围已执行：509个完整句段、两字典H1、CC正反向H2、冻结匹配、文档块区间与5组各398次随机基线；未训练、重聚类、新增前向或干预。
- Current work: 双语Summary/Detailed、一页入口、三类实测图、数学／生物极值例及最弱例、数据与完整脚本已生成。严格三项均非正反例未找到，明确标为最弱例。H1通过完整背景诊断41格（31格为非重复词面），H2无通过完整背景诊断的格；强结论以Summary/Detailed为准。严格匹配率SAE2.19%、CC1.48%，目标约84%为五个常见功能词；低频随机空分母及64+无匹配保留。共同消失源集合上的正向差值为零。SAE H2仍接口受阻。科学机制判断／问题关闭Unknown。
- Audit: 核心统计代码与匹配未变；实际直接集合复核、完整匹配合同与336主族保留通过。终审发现等价浮点聚合路径可把H2与度数包络的相等误报为约1e-18超额，已统一同一冻结权重算子，未调门槛／抽样；原临时判断保留为INELIGIBLE。
- Next action: 交付当前本地阅读包；后续先读Summary及匹配词面偏向，研究者决定是否值得另设上下文替换设计。不要自动补前向或重建SAE旧图；不重跑现有缓存结果。无commit/push授权或发布。
- References: `Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/summary_cn.md`（当前结论与边界）；同目录`detailed_cn.md`、`evidence/primary_336_final.csv`、`provenance/aggregation_consistency_fix.md`、`artifact_manifest.json`（精确证据及修正）；`main/focus/focus_sentence_feature_continuation_cn.md`（同项目，独立四状态与下一决定）；`/data/250010109/MoE_Router/experiments/20261028_sentence_feature_continuation/R01_cached_sentence_pairs/`（完整数据／脚本／抽样）；资产ID `analysis_a15_28_sentence_feature_continuation_r01_20261028` 已登记且严格访问通过；`sync/anchors/from-attention-to-search/15_28/README.md`（派生本地阅读包）。
