# R03交付清单与证据链

本清单区分完整文件、有资格的测量和仍不足的科学结论。主结果见[中文Summary](summary_cn.md)，详细解释见[Detailed](detailed_cn.md)，图的测量含义见[图解](figures/README_cn.md)。[机器可读逐文件清单](artifact_manifest.json)给出路径、字节数、SHA256、产物角色与预算；原始数组、JSONL、大表、代码和PDF留执行侧，不作为仓库载荷搬入。

## 冻结、预算与身份

冻结于2026-10-27 01:40:58 UTC（北京时间09:40:58），新R03前向/统计观察为0。37项冻结源在完成计算后逐一保持一致。随后只更新Focus的执行事实，原冻结字节另存；[冻结收据](provenance/pre_analysis_freeze.json)、[37项核对](provenance/final_frozen_source_check.json)、[Focus事实更新](provenance/factual_focus_update.json)保留各自时间。协议、Anchor、文本、候选选择、分析代码和阈值未改。原R01/R02记录未改。

36条面板＋2条旧缓存重放＋2条同条件重放＋8条固定前缀检查＝48，父终点1452，累计1500/1500。72条计划文本中其余36条明确NOT RUN。零训练、零干预、零新资源；没有读封存TEST、删除、提交或发布。[执行证书](provenance/execution_certificate.json)记录预算、环境、资格和原权重复哈希。

Model SHA256: `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`.

Dictionary SHA256: `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`.

Panel SHA256: `57c1d0358b5128a116128f73514d6d855454bdb689e706c941ed76f6a27e01b9`.

## 逐项产物

| Artifact | Purpose / criterion | Execution source | Producer / inputs | Completion and claim eligibility |
| --- | --- | --- | --- | --- |
| Frozen design and exact selectors | Pre-analysis identity before new R03 statistics | [pre_analysis_freeze.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/pre_analysis_freeze.json) | /root; 37 files, UTC freeze; Focus frozen bytes archived before factual update | COMPLETE; no post-result threshold change |
| Original O definition and evidence | Retain original same-token graph | [audit/original_graph_audit.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/audit/original_graph_audit.json) | original A15_25 sources, hashes and current cache access | COMPLETE; semantic parenthood not validated |
| Reference matrix and counts | 512 uniform IDs, D/V 64 contexts each | [results/selected_binary.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/selected_binary.npz) | offline/coactivation.py + frozen config; 65464/65484 rows | BOUNDED; missing document/sentence IDs |
| Rates and uncertainty | Counts/N; context bootstrap descriptive only | [results/feature_frequency.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/feature_frequency.csv) | same dictionary/gate/precision cache; 2000 context resamples | BOUNDED finite corpus, not population frequency |
| Raw/corrected graphs and groups | R conditional >=.8; C delta >=.05; support gates | [results/observed_graphs.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/observed_graphs.json) | all supported pairs, max symmetry, greedy modularity resolution1,min3 | COMPLETE within fixed 512 coordinates |
| All edge estimates | Preserve support, conditional, delta, V and interval fields | [results/edges_D_frozen.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/edges_D_frozen.csv) | counts -> exact directed metrics -> descriptive context intervals | BOUNDED intervals; adjacent tokens not independent trials |
| Original O base-rate diagnostics | Post-freeze descriptive audit, not a new tuned test | [audit/original_O_frequency_edges.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/audit/original_O_frequency_edges.csv) | audit/summarize_original_O.py; all 214711 D edges | BOUNDED; delta ceiling limits high-frequency detection |
| Complete randomized reruns | Exact column counts and row L0, 199 draws | [results/null_draws.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/null_draws.jsonl) | offline/coactivation.py + switch.cpp, 4 chains | COMPLETE; finite MCMC diagnostics, not perfect independence |
| Frequency comparison verdict | Stable/supported groups in observed and null | [results/null_results.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/null_results.json) | 0/199 nulls with eligible groups, p/q NA | INSUFFICIENT; never substitute zero/inf for absent group |
| Token/position stratification | Fixed token and position strata | [results/covariate_adjusted_association.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/covariate_adjusted_association.npz) | frozen stratification minus within-stratum independence expectation | BOUNDED; text types/docs unavailable |
| All texts, candidates and pairings | 12 constructed scenarios, 72 tokenized texts frozen | [panel/tokenized_sequences.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel/tokenized_sequences.jsonl) | panel/build_panel.py + finish_panel.py; no feature-result exclusion | 36 MEASURED, 36 NOT RUN due to parent cap |
| Forward ledger and certificate | Charge attempts before calls; maximum48 | [provenance/execution_certificate.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/provenance/execution_certificate.json) | run_forward.py; 36 panel +2 cache +2 replay +8 prefix | COMPLETE; cumulative1500/1500 |
| Native decoder scales | Keep raw z, per-layer and concatenated native norms | [forward/decoder_geometry.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/forward/decoder_geometry.npz) | existing checkpoint/TRAIN rms, no fitting | COMPLETE; shared z is not independent per-layer activation |
| Panel activations and output readouts | Causal visible prefixes, same-token direct pairing | [forward/panel_readouts.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/forward/panel_readouts.jsonl) | 36 sparse sequence NPZs; readout candidate IDs fixed | BOUNDED compatible-candidate probabilities only |
| Measurement qualification | Frozen cache/prefix/replay and reconstruction guards | [forward/panel_qualification.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/forward/panel_qualification.json) | finite fixed positions; cache up to1.936% relative error | PASS within tolerance; does not repair R02 E16 failure |
| Near/far effects and member support | Pre-panel D/V-qualified group union; case blocks | [panel_analysis/results.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel_analysis/results.json) | offline/panel_analysis.py; exact64 sign flips,2000case bootstrap,IUT/BH2 | C03 far bounded support; R union empty, NA |
| Case outputs and sparse dominance | Do not infer comprehension from feature change | [panel_analysis/member_support_dominance.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel_analysis/member_support_dominance.csv) | fixed6cases;1–5/72 members change; candidate_outputs.csv | DESCRIPTIVE; only S01 both meanings compatible |
| Naming evidence | D first32 naming, later contexts descriptive | [naming/naming_groups.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/naming/naming_groups.json) | offline/name_groups.py; multiple members/prefixes/boundaries | MIXED_CONTEXT_CANDIDATES; no fresh blind validation |
| Per-token graph projections | Fixed sentences, all positive coordinates saved | [panel_analysis/fixed_sentence_token_projections.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel_analysis/fixed_sentence_token_projections.jsonl) | actual token prefixes, native norms, frequency, fixed groups/O edges | INSTANCE DESCRIPTION; not cluster stability |
| Central graph/distance figures | Draw source estimates without refitting | [figures/graph_distance_plot_provenance.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/figures/graph_distance_plot_provenance.json) | offline/render_graph_distance.py;6PNG/PDF total across renderers | COMPLETE actual artifacts inspected |
| Original token figures | Keep frozen pooled-max display rule and its failure | [figures/token_figures_provenance.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/figures/token_figures_provenance.json) | offline/render_token_figures.py; target displayed rows all0 | DISPLAY FAILURE RETAINED, not absence of response |
| Target details | Explicit posthoc illustration only | [figures/target_detail_figures_provenance.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/figures/target_detail_figures_provenance.json) | offline/render_target_detail_figures.py; target top12,shared color | POSTHOC; all12 outside512, no C03 membership claim |
| Historical replacement audit | Link actual hook/position/dose only if comparable | [audit/existing_intervention_audit.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/audit/existing_intervention_audit.json) | source-only audit; no current replacement performed | NOT CURRENT FUNCTIONAL EVIDENCE |

每项精确哈希、大小及执行/项目表面见机器清单。源码复用旧图/缓存和原CrossCoder，新增离线统计及绘图为适配，不训练新资产。

## 主结论的证据链

| 问题 | 冻结比较 | 来源 | 观察/聚合 | 资格与允许裁定 |
| --- | --- | --- | --- | --- |
| 频率基准与旧图 | O的条件概率不等于超基准关联 | [original_O_frequency_summary.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/audit/original_O_frequency_summary.json) | 57.7045% delta<.05；21.038%≤0；极高频存在delta上限 | 描述性相容，不能归因为因果份额或无功能 |
| 超边际共激活组织 | 保次数/每位置L0的全流程null | [null_results.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/null_results.json) | C 2792边；null中位108、最大137；V同规则约70.0%复现 | 有限子图支持；缺文档身份限制总体外推 |
| 组内是否更同频 | 固定组和相同null流程 | [null_results.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/null_results.json) | 0/199合格频率null；p/q=NA | 证据不足，不能把空组替换为数值 |
| 低频→高频联系 | 低频节点也须达到支持门槛 | [feature_frequency.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/feature_frequency.csv) | 低频四分位124节点全部低于200次支持 | 不可估，不是没有联系 |
| 远处上下文响应 | 预定C并集的相关−无关变化 | [results.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel_analysis/results.json) | 6/6正；均值.160037，区间[.039337,.320294]；q=.03125 | 有界支持前文编辑响应；语义特异性、纯距离未分离 |
| 组或整句语义 | 成员支持和候选输出另检 | [member_support_dominance.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel_analysis/member_support_dominance.csv) | 每例仅1–5/72成员变化；仅S01两种候选均兼容 | 不支持整组联合语义、专家或理解成功 |
| 双线索整合Q3 | 本轮未新做四组合整合面板 | [summary_cn.md](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R02_frequency_distance_integration/summary_cn.md) | 沿用R02证据不足；当前CC资格不修复E16失败 | 本轮未解决，不能以远处响应替代 |

## 协议符合性、偏差与缺口

| 注册合同 | 实际完成 | 资格影响 |
| --- | --- | --- |
| 先冻结再看新响应 | 37源冻结后执行，结果后只补解释图/描述性原O审计 | 事后项目不作新确认 |
| 72文本最多，遵守更严父预算 | 预定6完整情境36条；另36条NOT RUN | 不把未测写作阴性 |
| 原图保留，新R/C固定分簇 | 全部复用与199次完整重聚类完成 | 频率null缺组导致NA |
| 句子/文档区间 | 原始身份无法可靠恢复；仅context描述区间 | 总体置信推断不足，不造句界 |
| 匹配精度与缓存 | 原Base batch16改batch1，z最大相对差1.936%，冻结容差内 | 近似重现，不称逐比特一致 |
| 原显示名单 | 全句top12被首token主导，目标全0 | 保留失败；目标细图事后，仅实例解释 |
| 近远线索 | 目标位置/长度/后缀匹配，仍搬动中性段 | 句序/新近性混杂；不称纯距离因果 |
| 无关编辑 | 星期替换保持长度，相关线索编辑改更多词 | 语义关系特异性未隔离 |
| 独立命名验证 | D前32命名、后32及已复用V描述 | 只命名混合语境候选，不称新盲验证 |

初次原O CSV工程写出中断留下`original_O_frequency_edges_attempt1_partial.csv`，随后完整结果独立保存；最初命名环境缺transformers，改用已有匹配环境成功。两次工程失败均留日志，不作科学结果，不改变分析规则。人工张量测试只验证实现。

## 资产、数据位置与未解决问题

[资产ID与访问快照](/data/250010109/Research_System/assets/same_token_coactivation_r03_20261027_cn.md) · [Selected evidence copy manifest](selected_evidence_payload_manifest.json).

Execution root: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation`. [Full inventory](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/artifact_manifest.json). 同名PDF、全部72文本、36稀疏缓存、完整边表、199次null和全部成员案例都保留此处。图的六个PNG和五张小表按精选证据例外复制并哈希核对，原件不删除。

缺口分别是：频率统计对极低频支持不足；频率比较的null组缺失；文档/句单位缺失；距离仍混句序；语义编辑量未匹配；簇命名与功能证据不足。三者不能合并成笼统“未通过”。唯一后续问题见Summary末尾；本轮不执行。机制接受与问题关闭Unknown。本地同步不等于发布。
