# Definitions, frozen members, full evidence and reproduction

[English brief](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/meeting_brief_crosscoder_domain_members.md) · [Chinese full appendix](appendix_cn.md)

## Definition table

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

## Frozen member table

Raw AUC is always math-higher-than-biology, so biology-biased members approach0. Discovery support denominators are30documents/domain. The master CSV also includes development10 and old-heldout20 support, direction-fixed heldout AUC/interval, checkpoint/interface, both frequency labels and all five test statuses. One A22 checkpoint and one block27 decoder are used throughout; fourteen-layer shared activation is not independently encoded block27 activation.

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

## Equations and scope

For unit decoder u_f and orthonormal PC p_k, each member distribution is the squared dot product. Average equally within each16-member group, then sum the smaller group fraction at each of1024 PCs. This equals one minus half the L1 distance between group distributions. Aggregating64 PCs before taking minima can only increase overlap. Sign and member combinations are lost: (p1+p2)/sqrt(2) and(p1-p2)/sqrt(2) are orthogonal but have identical squared PC distributions. Pairwise absolute cosine and actual decoder-span principal angles are therefore separately reported. Both spans rank16; squared Frobenius overlap of their orthonormal bases divided by16 is0.07647.

## Distinct old lists

| List | Original denominator | Intersection with frozen32 |
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

R04_new_top16 is the earlier global16 (math9,biology7), not16/domain. Expanded natural64 lists use document AUC. Earlier original-R04 usage lists and later same-token lists have distinct gates; controlled R09 per-domain64 and per-ending contribution32 use distinct selection objects. R09 union141 and replicated36 retain original denominators. [All ID/rank mappings](tables/list_mapping.csv) preserve them separately. The new16+16 reporting cut is exploratory, even though it reuses the ordered prefixes of old64 lists.

## Frequency history and unavailable matching

Original equal-count cuts are0.002593994140625 and0.0134429931640625, minimum20 reference hits. R09 introduced log-width cuts0.0045172553628813825 and0.06686505701697326 for its own analysis. Both are preserved, original primary. The exact matched-background joint bins use floor(log2(hits+0.5)) and floor(total positive discovery-document support/5), the same eligibility pool, excluding every frozen member and no replacement within a set. f9491's bin(hits39,support5+27) has no alternative; complete biology and paired backgrounds remain NA. Math's supported1000 draws were retained. The unmatched dictionary background is labeled explicitly and does not answer above-matched-background enrichment. No observed selection bootstrap is claimed.

## All-member figures

![All32 unit decoder band projections](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/appendix/member_band_heatmap.png)

![Per-PC spectrum and256 pair cosines](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/appendix/per_PC_and_pair_cosine.png)

![All16 math context responses](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/appendix/all_context_math.png)

![All16 biology context responses](/data/250010109/Research_System/daily_research_reports/1031/meeting_report/crosscoder_domain_members/appendix/all_context_biology.png)

Context x-axis contains example/explanation × W0/W1; y is unstandardized math-minus-biology z. Discovery24 and old-heldout12 paired families are separately bootstrapped2000times; intervals are pointwise descriptive95%. Active0/384 indicates insufficient test coverage, not token identity.

## Token evidence and missing estimates

[Complete actual-input examples](real_token_examples_cn.md), [CSV](tables/real_token_examples.csv), [member summaries](tables/token_member_summary.csv), [active-ID counts](tables/active_token_counts.csv), [reference counts](tables/reference_token_counts.csv). High and median-positive examples plus same-ID low/inactive controls obey maximum2examples/document/member and contain read prefixes only. Reference-unseen IDs are missing estimates, never declared zero true probability. Medians/10th–90th percentiles in the plot condition on seen IDs; the complete unconditional frequency association is unanswered. Domain token counts have9600positions/domain and describe this selected panel only. No vocabulary decoding of decoder weights was added.

Further separating C from identity-only responses would require new paired-prefix acquisition at actual responding natural IDs for the19all-zero and8unstable members. Those tests are missing/NOT RUN. They are not authorized by a delivery or available cache. No further experiments follow this report.

## Reproduction and provenance

Producer directory: /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/meeting_five_20261030. Run the local spectral-hier Python with analyze.py --freeze, analyze.py, audit.py, then render.py. Scripts infer their original cache root from the parent directory, so audit paths before relocating. Copies are in scripts/. [Input hashes](source_manifest.json), [freeze](freeze.json), [frequency history](frequency_history.json), [audit](audit.json) and all CSVs are included. Seeds2026103001/2/3 cover background, fixed-list document variability300draws, and context-family2000draws. Old AUC intervals reuse their original2000document-draw receipt; scalar AUCs were independently recomputed.

All 2795 independent checks passed. Visual checks were self-review; math checks concern source only. Existing navigation issues were reported without changing graph/Focus/Anchor states. Ten selected input assets and tokenizer passed current strict access. No commit, push or external publication occurred. Existing work is clearly separated from new offline statistics in the speaking brief.
