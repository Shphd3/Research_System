# 大范围特征层级关联图：整体概览与320节点连接图

当前主图已去掉底部文字并规范标题，左侧“展示／总体”替代缩写。[逐项术语与读图说明](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/reading_guide_cn.md)。原节点、边和排布不变。


**本次补图展示现有 V 统计图；不改变建图规则，也不产生新的学习结论。** 主图含 320 个 Feature、1,250 条已有约简直接边，其中 261 条跨越多个 h。原 30 个节点和 101 条边全部保留，新增更多分支。

## 先看总体，再看展示子图

| 统计图层级 h | 完整分析集合 Q 的真实节点数 | 本次连接图节点数 |
|---|---:|---:|
| 5 | 2 | 2 |
| 4 | 63 | 63 |
| 3 | 1,209 | 75 |
| 2 | 5,347 | 80 |
| 1 | 8,896 | 80 |
| 0 | 20 | 20 |
| 合计 | 15,537 | 320 |

![完整15537个非孤立合格节点的统计图层级概览](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure1_full_hierarchy_overview.png)

每个小方点代表一个真实 Feature，在每个 h 带内按固定 200 列点阵排版；缩小时会呈密度纹理，放大 SVG/PDF 可看点阵。h=5 在上，h=0 在下。点阵没有连线，内部位置只为容纳数量，不表示模型层号或相似度。

Q 是两侧支持 ≥200 且 V 图非孤立的集合。**h=0 的20个节点不代表完整16,384字典中的所有终点。** 完整字典 h=0 为867个，其中847个孤立节点不纳入 Q。原19／22节点分支不是总体分布；本图纠正这一展示范围歧义，而不是人为改变节点数。

[概览SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure1_full_hierarchy_overview.svg) · [概览PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure1_full_hierarchy_overview.pdf)。

## 大型连接图：谁与谁相连

![320个节点与1250条真实直接边](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure1_expanded_connections.png)

节点上方为稳定 Feature ID，下方是 **V 激活频率（%）**，统一节点大小，不同颜色仅标统计图层级 h。h 沿用完整 V 图，不在展示子图重算。左右排布只用于减少交叉，不表示相似度。

箭头 **A→更常见的 u**，是保存的 V 约简图中原有的直接统计边，不是已确认的因果或语义组合。选中端点之间的全部 1,250 条边都画出，包括跨 h 边；没有按解码分布、边是否漂亮或是否符合假设过滤。棕色仅帮助认出原两个锚点分支，其他边仍完整保留。这里的“直接”指约简图中的出邻接边，不是将原始图传递边重新加回。

本图是分层展示选择，**不按完整 Q 的数量比例抽样**。图旁同时标出本页节点数与全 Q 数。h=0、h=4、h=5 全部纳入；中间层部分展示，不能用子图密度替代全体结论。

[可放大SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure1_expanded_connections.svg) · [可放大PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure1_expanded_connections.pdf) · [高分辨率PNG（6877×3031）](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure1_expanded_connections.png)。

### 密集连接如何读

[17页直接边分面PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure1_expanded_connections_facets.pdf)每页最多20个起点，按起点的 h 和行内顺序分批；起点及其选中直接邻居保留完整图 h 和主图横坐标。**每条展示边在分面文件中恰好出现一次**，总计仍为1,250，不因分面添加／删除。[分面页码与起点清单](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/facets_index.json)给每页 ID 范围。

15个节点在所选320节点间没有边，但在完整图中非孤立，主图用 **†** 标记；这来自邻居在展示范围之外，不能判作完整图中无关系。每个节点的完整／展示／遗漏入出度都在CSV中。合计遗漏入邻接条目102,824、出邻接条目1,693，属于逐节点条目数，不是不同外部Feature的数量。

## 与连接图分开的解码占比热图

热图使用**完全相同的320个ID**，按h=5到h=0分组，组内顺序与连接图从左到右一致。横轴才是实际模型层号2、4、…、28；颜色为跨层解码幅度占比 p，单位%，每个Feature的一行合计100%。它不是激活频率，也不把图中的上下位置变成模型深度。

[TRAIN归一化坐标：完整320×14热图PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure2_expanded_decoder_train.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure2_expanded_decoder_train.svg) · [PNG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure2_expanded_decoder_train.png)。

[恢复原始坐标：完整320×14热图PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure2_expanded_decoder_raw.pdf) · [SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure2_expanded_decoder_raw.svg) · [PNG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure2_expanded_decoder_raw.png)。两坐标使用相同0–100%色标。

![同320节点TRAIN归一化坐标解码占比，按h分面方便阅读](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure2_expanded_decoder_facets.png)

分面只是完整热图的阅读版本；各面板画布等高不表示样本数相同，标题写明展示数／总体数。[分面PDF](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure2_expanded_decoder_facets.pdf) · [分面SVG](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/figures/figure2_expanded_decoder_facets.svg)。

## 预先固定的选择规则

规则在读取本次展示用 p 之前保存：[完整冻结规则JSON](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/selection_rules_frozen.json)；[冻结节点与63条分支路径](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/selection_frozen_before_p.json)。

1. 保留937、3461原完整出边可达并集30个节点。
2. 纳入全部合格 h=0、h=4、h=5 节点，数量为20、63、2。
3. 按 h=4 根节点 ID 升序，为每个根选一条到 h=0 的最长路径见证：每步只从已有直接出邻居中选择 h 低一级者，优先复用已选邻居；候选按ID排序，以固定种子20261014的PCG64抽取。全部63个h=4分支都有路径，不只重复两个h=5小分支。并未保留这些根的全部后代，所以范围外邻居另行说明。
4. 依次补充 h=3、h=2、h=1 到75、80、80个。每个完整 h 组按 D 激活频率及ID排序，按秩分四组；从当前选中数最少且仍有候选的秩组补取，数量并列时按低组优先，组内固定种子抽取。频率并列用ID打破，秩组不是严格不相交的频率区间。种子、分组和配额不看 p、L、文本或深层假设结果。
5. 保留选中ID之间的全部已有直接边，不重约简。若路径保护节点超配额则保留并报告，不删除路径；本次未超配额。选择冻结时保护节点数 h=0至5为20、20、18、33、63、2，之后按规则补齐320个。

本选择覆盖分支和激活频率范围，目的是看连接。它不是概率代表样本，也不重新计算／替代全体15,537节点的趋势。

## CSV与来源

| 文件 | 行数 | 内容 |
|---|---:|---|
| [expanded_nodes.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/tables/expanded_nodes.csv) | 320 | ID、原h、D/V支持与激活频率、选择原因、频率秩组、完整／展示／遗漏入出度、排版坐标 |
| [expanded_edges.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/tables/expanded_edges.csv) | 1,250 | A/u、原h、D/V共同支持、条件概率、背景频率、lift、跨h幅度、原分支标记 |
| [expanded_decoder_p.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/tables/expanded_decoder_p.csv) | 8,960 | 320×14×2坐标的p，数值保持0—1，图中乘100 |
| [overview_counts.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/tables/overview_counts.csv) | 6 | 各h总体与展示数量 |
| [display_frequency_coverage.csv](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/tables/display_frequency_coverage.csv) | 24 | 每h各频率秩组完整／展示人数与D频率范围 |

原关系图：`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/graphs/reduced_V.json`。边支持从同run的raw_edges.npz按(A,u)查已有D/V计数；没有新计数。p直接复用`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/hierarchy_decoder_distribution/20261014T020014Z/derived_geometry.npz`。父checkpoint是既有最终14选定层、16,384特征CrossCoder；阈值、归一化、数据划分不变。精确来源路径和hash见 [完成回执](/data/250010109/Research_System/daily_research_reports/1014/crosscoder_feature_phase1/hierarchy_decoder_protocol_handoff_20261014T012430Z/results_20261014T020014Z/expanded_graph_20261014T032050Z/receipt.json)。

CPU作图及来源核对约63.91秒；仅点阵／主图可读性修正另18.27秒；峰值进程RSS约1.13GiB。本次没有GPU任务、推理、训练、激活缓存扫描、关系计数或重新构图。JSON序列化的两次启动错误已修复，未改变选择规则或结果；记录见engineering_note.json。PNG已实际查看；PDF/SVG容器和来源一致性已检查，但未独立验证用户客户端PDF渲染。客户端“不显示”的具体原因尚未确定，不能宣称已修复客户端。

整体统计结论仍以原15,537特征结果为依据；本次只补充可读性与展示范围，不修改科学状态，不commit/push。完成后停止。
