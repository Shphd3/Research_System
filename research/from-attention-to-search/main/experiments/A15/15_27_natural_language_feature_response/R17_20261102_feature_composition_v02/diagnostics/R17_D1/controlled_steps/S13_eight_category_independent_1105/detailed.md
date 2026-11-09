# S13 detailed evidence

## Three analysis paths

1. Behavior and factor controls: all sixteen complete fine-class candidate sequences, with correctness/margins evaluated within each sibling pair; literal/implicit wording, actual lengths and token positions. Parents have no fine-class gold.
2. Representations and organization: native Top32 membership, raw z, q=z/L2, continuous Q/G reference frequencies, and fixed local conditional edges. Only block27's two different hooks are measured; no layerwise evolution is inferred.
3. Functional interventions and quality: interventions and checkpoint training were not run. Quality is checked by native old-prefix and variable-answer calibration, immutable split/selection receipts, exact-margin diagnostics and raw-data replay.

## Purpose, scope and hypotheses

The user authorized new controlled-prefix inference and bounded statistics, not training or routing. S13 asks whether S11's relative shared-member frequency observation reproduces on new frames and additional categories, whether members/strength change from parents to children, and whether selected local relations survive individual-incidence/Top32 controls. Marginal frequencies, global activation scale, common backgrounds and lexical/prototype cues are credible rivals. Scientific acceptance and question closure stay Unknown; algorithmic SUPPORT is a frozen-test label, not human endorsement.

## Data and genuine confirmation

6912 freshly extracted prefixes = 72 frames ×24labels ×4wordings. Related settings are grouped into24clusters of3frames:8clusters/24framesDEV;16clusters/48framesCONF. Candidates and readout parameters were selected before the first CONF response. All four new parent groups are present in DEV: this is new-text confirmation and testing the rule on additional categories, not zero-shot withheld-category transfer. DEV has2implicit descriptions per label; CONF uses6different descriptions crossed with backgrounds. Exact duplicate and normalized-template similarity checks are in data/evidence. Low template similarity does not prove semantic independence. Literal names were removed from attribute/scenario descriptions, but lexical cues remain.

## Model, dictionaries and position

Official Qwen3-0.6B Base,28blocks,hidden1024. Exact model/tokenizer/config and SAE hashes, loader files and recorded training parents appear in evidence/asset_lineage_audit.json and frozen_plan.json. ATTN is block27.self_attn.o_proj output before residual; MLPIN is actual block27.mlp input after residual and layer normalization. Each separate native30000dictionary has ReLU/Top32, no extra input or decoder normalization. Same numerical feature ID across dictionaries is unrelated. Every prefix uses a whole-prefix tokenizer and final newline Description: colon(token25), actual index/offset/length saved, no truncation. Fixed suffix does not imply identical integer indices across unequal-length phrases.

## Behavior

Candidate score is full conditional sum log P(' '+fine_label+'.' | prefix); all16answers scored including all tokens; frozen correctness and margins compare the two sibling candidates, while choice16 is separately saved. Unequal answer lengths remain, so mean-token scores are a prespecified sensitivity, not a replacement primary. Each CONFwording has768fineprefixes; parents receive no fabricated correctness. Saved behavior JSONL includes every candidate score/rank, margin, exact token denominator and all wrong cases.

## Shared member and frequency estimator

For positive Top32supports S_a,S_b, I=S_a∩S_b, U=S_a∪S_b, J=|I|/|U|. Empty I gives undefined frequency, not0. p_f^Q/G=count_f/6000 from reused S11 references, one terminal-colon position per reference document, Q stratified by its three sources. Q has22extra identical encoded prefixes, G0; neither corpus is universal. Ref count≥5 is measurement support, not a high/low definition.

Each I contributes the mean p_f with equal member weights, then frames/contextclusters are averaged. Primary D=shared-frequency in a fixed direct-parent block−shared-frequency in the matching sibling pair. Blocks are animal–vehicle,fruit–furniture,clothing–instrument,flower–cutlery. Each domain has its own sibling comparison; shared coarse blocks induce dependence, not independent new samples. Every164pair is separately labeled:28directparent,16ownparent-child,8siblings,112cross-parentfine. Parents explicitly written in text and cross-child mixtures are different objects.

Primary uncertainty uses2000paired contextcluster bootstrap and independent source-stratified reference-document bootstrap, plus paired joint draws. Reference-only and context-only intervals remain separate. Sign-randomization uses9999cluster signs; Holm16/site-domain tests per reference/wording. Atleast36/48validframes,12/16validclusters,≥.8reference-supported member mass and both fine behaviors≥.75 are required. Joint lowerCI>0 and adjustedp<.05 supports, upperCI<0 and adjustedp<.05 is opposite; otherwise unresolved/insufficient. Two reference axes are not independent controlled confirmations. Quantiles are mean within-pair linearly interpolated quantiles, not pooledCDFquantiles; their bootstrap and descriptor sensitivity condition on the fixed reference. Two coarse-baseline sensitivities cannot rescue a failed primary.

## Member retention and amplitude

Original positive supports and rawz are retained. For sharedmembers report both raw changes and q_f=z_f/||z_allTop32||_2, together with L1/L2 and I. q's denominator includes all32members, so q differences may reflect outside-set scale as well as within-set balance. Loss/gain count equality follows row32; zero z means out of selectedTop32. Actual positive preactivation and distance from the destination cutoff are separately audited. Exit-event counts repeat features across pairs; they are not independent observations.

## Local conditional model and frozen selection

HIFER attachment was read directly; exact identity and extracted text are retained. Composite is a single coordinate. Its asymmetric empirical role uses n_u>n_c, P(u|c)≥.8, P(c|u)≤.5, n_u/n_c≥2. S13 applies a local adaptation, not the paper's32768/Top50SAE,128Mtoken corpus or routing evaluation. DEVfineexplicit rows384, nested in8clusters. Atmost96eligible features; center≥32, pair≥20, center in≥6clusters. Full eligibleDAG undergoes transitive reduction before selecting≤4centers/≤3neighbors by exact-margin excess. Both sites choose4centers/11edges. Four-class comparisons must not be inferred from this pooled graph. Structural Jaccard compares fixed constituent sets, not category-varying sets.

## Null, uncertainty and distinctions

Within each label/wording/site, Curveball preserves every row32 and complete30000column counts;4chains×512draws,500burnsweeps,20thin, one prespecified2000/80extension if needed. Recorded margins are asserted at every draw, first/last states saved, movement/retention/locked coordinates recorded. Rhat≤1.05,ESS≥200,nondegenerate is needed. This controls individual incidence and fixed capacity under that stratum, not every background or strength relation.

E=P(u|c)−mean_nullP(u|c). A fixed pooled edge needs CONFcenter≥24,≥10clusters,≥1900/2000validbootstrap,adequate mixing and positiveCI/adjustednullp plus positiveDEVexcess. Original role-threshold retention is separately reported. Per-category counts are descriptive. Each site's available fixed category edge is DEVselected at center≥6bothsiblings/≥4clusters; CONFneeds≥10both/≥6clusters,pairedclusterCI,Holm16/wording,sameDEVdirection. No candidate is replaced after CONF. Unavailable category edges and missing MLPcatdog migration remain NOT RUN.

Parent-child is a prospectively added exploratory application of the same sibling edge, separate parent-label null strata,Holm32/wording,no expected direction. The ATTNdog/cat fixed edge alone migrates unchanged to other7pairs;Holm14,exploratory. It tests same-edge transfer, distinct from reusing the analysis rule on new groups.

A critical scale audit was specified before outcomes: ΔE=ΔrawP−ΔnullP. Positive ΔE can be caused by a changed baseline with unchanged raw implication; this is not automatically a changed interaction parameter. Pairedcluster rawP and smoothedlogOR intervals are supplementary; zero/sparse fourcells make the latter unstable. Null centers are held fixed in relation cluster intervals. These intervals do not integrate null-estimation sampling in every bootstrap, nor preserve cross-label paired background rows. Those are limitations, not silently repaired claims.

## Small statistical readouts

Only CPUlogistic statistical readouts are fit: best single, additive on the same12–14DEVselected binarynodes (≤12base nodes plus fixed endpoints), plus one fixed product where eligible. Group-LOCO among8DEVclusters selects the bestsingle; fixedC=.5,lbfgs,maxiter2000,DEVscaler,explicit-onlyfit. All parameters saved before CONF. CONF48frames/96rows perpair,2000clusterbootstrap,fullBernoullilogloss primary,accuracysecondary; Holm16/wording. Interaction models differ in capacity; deterministicproducts add no new information to the full vector. Single-node ceilings and no-edge configurations are preserved. No LM/SAE/CrossCoder/router update, expert assignment or causal effect is inferred.

## Runtime, changes and errors retained

Only local current-container CPU8 inference; no submitted remoteGPU/cloudjob. Budget10800modelseconds, first24newDEVforecast<budget. Existing checkpoint bytes were hashchecked. Protobuf startup failure and CPU1-vsCPU8 qualification failures were preserved; isolated dependency path and process-local flag repaired imports; matchingCPU8 requalification passed with original1e-4gate, no widened tolerance. Native old-prefix codes match saved S11 exactly. Fresh variable-answer calibration scores agree within7.63e-6nat. All deviations/prospective interpretation additions have dated receipts; protocol and development lock hashes are replayed after results.

## Output and review

All raw exact texts and complete native sparse activations are saved. Full all-pair/family/member tables, relation fourcells/null diagnostics, predictions and actual preactivations remain execution-side. Portable packet contents are listed by exact relativepath/bytes/hash; external payload index does not imply those files are bundled. Independent numeric replay checks70916items and1792full saved null states. Figures have source hashes, PNG/SVG, direct units and sample counts; the visual review receipt is separate from numeric checks. Technical completion is separate from human scientific acceptance/closure.


## Decisive measurements

显式条件下，共有成员相对频率主比较共32/32项通过冻结标准；原四组新文本16/16项，新增四组16/16项。反向0项，未决0项，不足0项。

| SAE | 类别 | Q粗/细均值% | Q差值pp / 联合95%区间 | Q判定 | G差值pp / 联合95%区间 | G判定 |
| --- | --- | --- | --- | --- | --- | --- |
| Attention输出 | 动物 | 17.05 / 13.04 | +4.01 [2.95, 5.15] | 支持 | +2.96 [2.25, 3.74] | 支持 |
| Attention输出 | 交通工具 | 17.05 / 15.06 | +1.99 [1.03, 3.10] | 支持 | +1.60 [0.86, 2.39] | 支持 |
| Attention输出 | 水果 | 16.86 / 14.97 | +1.89 [0.95, 2.82] | 支持 | +2.26 [1.52, 2.96] | 支持 |
| Attention输出 | 家具 | 16.86 / 15.71 | +1.15 [0.32, 2.02] | 支持 | +0.95 [0.37, 1.60] | 支持 |
| Attention输出 | 衣物 | 17.45 / 13.20 | +4.24 [3.21, 5.36] | 支持 | +5.27 [4.09, 6.59] | 支持 |
| Attention输出 | 乐器 | 17.45 / 12.29 | +5.16 [3.87, 6.56] | 支持 | +5.27 [3.94, 6.78] | 支持 |
| Attention输出 | 花 | 16.54 / 13.32 | +3.22 [2.42, 4.02] | 支持 | +1.91 [1.21, 2.61] | 支持 |
| Attention输出 | 餐用器具 | 16.54 / 14.54 | +2.00 [1.17, 2.81] | 支持 | +1.48 [0.99, 1.99] | 支持 |
| MLP输入 | 动物 | 46.74 / 39.60 | +7.14 [5.61, 8.66] | 支持 | +6.90 [5.53, 8.39] | 支持 |
| MLP输入 | 交通工具 | 46.74 / 40.96 | +5.78 [4.34, 7.24] | 支持 | +4.98 [3.67, 6.44] | 支持 |
| MLP输入 | 水果 | 43.95 / 41.05 | +2.90 [1.45, 4.40] | 支持 | +3.36 [2.02, 4.80] | 支持 |
| MLP输入 | 家具 | 43.95 / 41.04 | +2.91 [1.79, 4.15] | 支持 | +2.76 [1.83, 3.80] | 支持 |
| MLP输入 | 衣物 | 47.62 / 39.99 | +7.63 [6.36, 9.04] | 支持 | +7.03 [5.66, 8.49] | 支持 |
| MLP输入 | 乐器 | 47.62 / 37.69 | +9.93 [8.41, 11.34] | 支持 | +8.30 [6.83, 9.90] | 支持 |
| MLP输入 | 花 | 43.09 / 38.15 | +4.94 [3.67, 6.30] | 支持 | +4.04 [2.83, 5.27] | 支持 |
| MLP输入 | 餐用器具 | 43.09 / 41.34 | +1.74 [0.34, 3.20] | 支持 | +1.66 [0.39, 2.91] | 支持 |


两套SAE共固定22条开发边。显式确认中，7/22条通过共激活超额复现；其中7/22条同时保留原条件角色阈值。这不是22个独立的语义机制。

| SAE | 表述 | 预选边 | 超额支持 | 反向 | 未决 | 不足 | 原条件阈值仍成立 | 两者同时成立 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Attention输出 | 显式类别名 | 11 | 3 | 0 | 6 | 2 | 5 | 3 |
| Attention输出 | 保留类别名改写 | 11 | 1 | 0 | 5 | 5 | 4 | 1 |
| Attention输出 | 无类别名属性 | 11 | 2 | 0 | 6 | 3 | 2 | 0 |
| Attention输出 | 无类别名情境 | 11 | 2 | 0 | 9 | 0 | 2 | 1 |
| MLP输入 | 显式类别名 | 11 | 4 | 0 | 5 | 2 | 8 | 4 |
| MLP输入 | 保留类别名改写 | 11 | 4 | 0 | 7 | 0 | 7 | 3 |
| MLP输入 | 无类别名属性 | 11 | 4 | 0 | 5 | 2 | 6 | 4 |
| MLP输入 | 无类别名情境 | 11 | 6 | 0 | 5 | 0 | 7 | 5 |


See detailed_cn.md, relation_results_cn.md and complete CSVs for every opposing, unresolved and insufficient condition.


## Actual readout and supplementary diagnostic / 读出实测与辅助诊断

| SAE | 细类 | 节点数 | 最佳单成员loss | 加性loss | 加乘积loss | 加性−乘积loss | 95%CI | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Attention输出 | 动物 | 13 | 0.331929 | 0.293917 | 0.294705 | -0.000789 | [-0.002511, 0.000803] | UNRESOLVED |
| Attention输出 | 交通工具 | 13 | 0.390208 | 0.274586 | 0.277577 | -0.002991 | [-0.009862, 0.003476] | UNRESOLVED |
| Attention输出 | 水果 | 13 | 0.521877 | 0.428293 | 0.425655 | 0.002639 | [-0.004659, 0.009696] | UNRESOLVED |
| Attention输出 | 家具 | 12 | 0.489031 | 0.393272 | 未运行 | 未运行 | 未定义 | NOT_RUN_NO_EDGE |
| Attention输出 | 衣物 | 13 | 0.620104 | 0.609254 | 0.610637 | -0.001384 | [-0.026146, 0.020175] | UNRESOLVED |
| Attention输出 | 乐器 | 12 | 0.685819 | 0.634429 | 0.633619 | 0.000810 | [-0.000656, 0.002044] | UNRESOLVED |
| Attention输出 | 花 | 12 | 0.356924 | 0.259127 | 未运行 | 未运行 | 未定义 | NOT_RUN_NO_EDGE |
| Attention输出 | 餐用器具 | 12 | 0.677875 | 0.623764 | 0.605770 | 0.017994 | [-0.004011, 0.039170] | UNRESOLVED |
| MLP输入 | 动物 | 12 | 0.099017 | 0.098404 | 未运行 | 未运行 | 未定义 | NOT_RUN_NO_EDGE |
| MLP输入 | 交通工具 | 12 | 0.130838 | 0.071767 | 未运行 | 未运行 | 未定义 | NOT_RUN_NO_EDGE |
| MLP输入 | 水果 | 12 | 0.099017 | 0.061615 | 未运行 | 未运行 | 未定义 | NOT_RUN_NO_EDGE |
| MLP输入 | 家具 | 13 | 0.602018 | 0.481877 | 0.481417 | 0.000460 | [-0.000099, 0.000997] | UNRESOLVED |
| MLP输入 | 衣物 | 13 | 0.652001 | 0.647110 | 0.653613 | -0.006503 | [-0.019645, 0.004280] | UNRESOLVED |
| MLP输入 | 乐器 | 12 | 0.462034 | 0.459726 | 0.457855 | 0.001870 | [-0.005650, 0.010188] | UNRESOLVED |
| MLP输入 | 花 | 14 | 0.135491 | 0.075020 | 0.074786 | 0.000234 | [0.000090, 0.000440] | GAIN |
| MLP输入 | 餐用器具 | 13 | 0.247754 | 0.184018 | 0.184083 | -0.000065 | [-0.000219, 0.000077] | UNRESOLVED |


| wording | GAIN | HARM | NOT_RUN_NO_EDGE | UNRESOLVED |
| --- | --- | --- | --- | --- |
| attribute | 0 | 0 | 5 | 11 |
| explicit | 1 | 0 | 5 | 10 |
| named_rephrase | 0 | 0 | 5 | 11 |
| scenario | 0 | 2 | 5 | 9 |


| SAE | 类别 | 固定乘积 | 开发复制列 | 确认不相同行/96 | 原交互loss | 复制列替代loss |
| --- | --- | --- | --- | --- | --- | --- |
| Attention输出 | 水果 | 9270×2254 | 9270 | 5 | 0.425655 | 0.428506 |
| MLP输入 | 家具 | 416×5196 | 416 | 0 | 0.481417 | 0.481417 |
| MLP输入 | 花 | 416×17390 | 416 | 0 | 0.074786 | 0.074786 |


Actual additive node count is12–14; interaction adds one coordinate. Three development product columns duplicate existing columns; this can change L2 effective penalties. Full128frequency arm levels and complete no-DEV-edge coverage are linked by Summary. Calibration v1 failed before additional confirmation because its paddedbatch16 test differed from the original passing batch1CPU8 qualification; v2 reused the unchanged original check design and passed. Original frozen producer/protocol/DEVlock untouched. Supplemental primary replay checks all128keys,armmeans,jointCI,Holm/status and selected reference bootstrap draws (656checksPASS). See review_mathematical_model.md and primary_complete_replay.json.
