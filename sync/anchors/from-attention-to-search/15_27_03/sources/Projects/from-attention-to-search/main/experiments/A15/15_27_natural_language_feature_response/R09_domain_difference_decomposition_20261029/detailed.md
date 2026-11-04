# Detailed: R09 CrossCoder domain-difference decomposition

The complete dictionary reconstructs a substantial directionally aligned part of the fixed-target domain difference, while a material vector residual remains. On original heldout families, the relative residual is 0.5368 for `example` and 0.7214 for `explanation`; the fixed Top32 subsets have larger errors 0.7196/0.8289. Of 64 discovery candidates per preferred domain, 16 math and 20 biology candidates retain their **activation-use preference** under the registered checks. Frequency-group contribution and domain-versus-family variation describe different quantities. The controlled distance sweep completed all 3,842 forwards and has its own construction and replication limits.

Primary owner: [Anchor 15_27_03](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_03_domain_difference_decomposition_anchor.md). Registered plan: [Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/protocol.md), immutable main snapshot [here](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/sources/main_frozen_protocol.md). This record owns full setup, numerical evidence, deviations and reproducibility. Main and frequency/family statistics are usable descriptive decompositions with exposed-data exploratory inference. Distance results are bounded by constructed-context manipulation, unequal domain/date-edit magnitude and finite family support. Researcher scientific acceptance and closure remain Unknown.

## 1. What was measured and why

R07 measured real final-token domain means. R08 showed that a mixed leading subspace could contain nearly all of the center-difference direction while most variance remained within domains. R09 asks which fixed dictionary coordinates compose that center difference and how much the dictionary misses. The hypotheses are concentrated contribution, distributed contribution with reinforcement/cancellation, wording/ending dependence, and a substantial unexplained residual.

Each observation is one final target's 1024-dimensional true vector plus one 16,384-dimensional shared CrossCoder activation. `example` and `explanation` are analyzed separately, keeping target identity fixed within each comparison. “Member” means a fixed dictionary coordinate; “preference” means math-minus-biology mean activation sign. “Individual” means a topic/text family within a domain. This gives three analysis paths: factor controls establish which text changes matter; representations supply vector and activation statistics; numerical/interface checks establish measurement quality. No functional intervention or behavioral prediction test was performed.

## 2. Actual objects and computation

The original 384 constructed English inputs contain 48 families×2 domains×2 wordings×2 endings. The original family split is 24 discovery/12 development/12 heldout, giving 192/96/96 rows. At one ending, old heldout has 48 rows:12 families×2 domains×2 wordings. Families and wordings receive equal weights, and related variants travel together in resampling. Corresponding math/biology family IDs designate constructed contrasts, not matching natural themes. Original final positions are preserved; they are not all 239. F06's original target is position 36.

The Base is frozen Qwen3-0.6B. True vectors are zero-based block 27 residual-post before final normalization. R08 cached all fourteen odd-block target vectors and native A22 shared z; the old final vectors match R07 exactly. A22 jointly encodes blocks 1,3,...,27 using its original centering/RMS and learned native threshold 0.051281172782182693. The native gate has k256. The legacy 256-token encoder row plus normalized-zero padding to 1024 is preserved. There is no last-layer-only encoding. The checkpoint SHA256 is `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`.

The complete source rows and tensor indices are in [R08 panel](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/../R08_within_mixed_subspaces_20261029/data/panel.jsonl) and [saved target readings](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/../R08_within_mixed_subspaces_20261029/forward/target_readings.npz). The main [configuration](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/config.json) names four required input asset IDs; current strict access and exact source hashes are carried by the execution records. The independent spectrum is the same natural-text common basis used by R 07, stored in R 04's actual `real_spectrum_A01/analysis/CC_common_basis.npz`. It is not R 08's mixed-panel PCA.

At fixed ending and split, first average actual vectors and zero-inclusive activations. Let delta be math mean minus biology mean. For member j, multiply its activation difference by the learned block 27 decoder vector and training restoration RMS 374.3495121024576. The result c_j is a vector in the same model coordinates as delta. Sum all c_j to obtain reconstructed difference delta_hat; residual r=delta−delta_hat. Training mean and decoder bias cancel in the domain difference. Statistics use saved master FP 32 decoder parameters cast to FP 64.

Report original lengths, relative residual||r||/||delta|| and cosine (delta, delta_hat). The signed contribution a_j=(c_j·delta)/||delta||² is additive: sum_j a_j plus (r·delta)/||delta||² equals 1. A negative value opposes the true direction; a positive biology-preferring member is possible because its decoder orientation also enters. Signed shares do not measure perpendicular error. The numerical near-zero guard is 1e-12 times mean true-vector norm; no primary condition approaches it. Candidate subset lengths and spectral energies are computed after vector summation, retaining cross terms.

## 3. Registration order and actual conformance

| UTC 2026-10-29 | Actual event / 真实事件 | Evidence / 凭据 |
| --- | --- | --- |
| 14:41 | Frequency/family config frozen / 频率与家族配置冻结 | [config](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/config.json) |
| 14:43:09–14:43:33 | Cache-only frequency/family run / 纯缓存分支运行 | [started](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/started.json); [completed](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/completion.json) |
| 14:47:43.979745 | Main protocol/code/input hash snapshot / 主协议与代码输入hash冻结 | [freeze](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/freeze.json) |
| 14:47:46.357405 | Discovery-only candidate lists saved / 发现集名单保存 | [candidate freeze](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/analysis/candidate_freeze.json) |
| 14:48:02.062973 | Main decomposition complete / 主分解完成 | [completion](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/analysis/main_completed.json) |
| 14:48:14.013455 | Distance extraction authorized against frozen config / 距离提取配置绑定 | [run authorization](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/run_authorized.json) |
| 14:49:16.345178 | Exact distance statistics file saved during acquisition / 提取中补存精确统计文件 | [statistics config](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/statistics_config.json) |
| 14:50:08.379676 | Independent main audit,1166 checks / 独立主审计 | [audit](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/analysis/main_independent_audit.json) |
| 14:50:29.959926 | Protocol A01 records distance details and chronology / A01记录细节与顺序 | [Protocol](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/protocol.md) |
| 14:51:55.339413 | All 3842distance forwards complete / 距离前向全部完成 | [completion](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/forward/completed.json) |

The frequency/family branch had its own unchanged pre-execution config before the consolidated Protocol existed. The main freeze then saved immutable English/Chinese Protocol copies, Anchor, code, configs and source hashes. Distance acquisition used its frozen construction and extraction config; its exact statistics file was written during acquisition before statistical analysis. A01 states that chronology explicitly. It is not described as a single pristine preregistration before all computation. R07/R08's original heldout was already exposed.

| Registered item | Actual result | Eligibility consequence |
|---|---|---|
| Same384 original main inputs and native A22 interface | Row identity, last-layer equality, checkpoint, normalizer, gate and decoder checked | Main decomposition describes the specified object |
| Full dictionary before candidate interpretation |16,384 members×3 splits×3ending views=147,456 rows | Pooled ending view is auxiliary; neither candidate list substitutes for full statistics |
| Discovery-only selection | Lists saved at 14:47:46;64 math+64 biology,141uniqueunion including Top32 | Old-heldout checks do not change lists or order |
| Independent reference bins | All 65,536 positions, inherited20hit support, fixed log/legacy/linear groups | No target-panel bin fitting; all low-support members retained |
| Family uncertainty |500 replicates with fixed seeds and paired variants | Pointwise exploratory intervals; nonlinear squared statistics can be biased |
| Distance construction |3,840derived rows; exact positions and within-source cross-distance token multisets | Reordered filler/framing remains part of manipulation |
| Distance budget and freeze |3,842/3,842 forwards including2 replays; no retries beyond cap | Parameters unchanged; old near input is not the new240-token near condition |
| Numerical precision | IndependentFP64 identities plus separateCPU BF16 decoder diagnostic | CPU precision comparison is not GPU bitwise replay |

No original source was deleted. No model/dictionary/router training, new PCA, clustering, functional intervention or new resource submission occurred. Old scientific states were not changed.

## 4. Whole-dictionary and subset results

| Ending | True norm | Reconstructed norm | Residual norm | Relative residual [95% interval] | Cosine [95% interval] |
| --- | --- | --- | --- | --- | --- |
| example | 103.515 | 89.285 | 55.565 | 0.536779 [0.521219, 0.579592] | 0.843928 [0.814936, 0.854051] |
| explanation | 52.972 | 38.538 | 38.215 | 0.721408 [0.684047, 0.765007] | 0.693352 [0.649164, 0.731885] |

All 500 bootstrap replicates are valid for these heldout norms, errors and cosines. The directional dictionary totals are 0.727910/0.504418 and directional residuals 0.272090/0.495582. Those sums answer alignment along delta; the 0.536779/0.721408 residual-length ratios answer whole-vector reconstruction. Reporting only the former would omit substantial perpendicular error.

The full 9 condition view is:

| Split / 划分 | Ending / 结尾 | Relative residual / 相对残差 | Cosine / 余弦 | Signed total / 净方向贡献 |
| --- | --- | --- | --- | --- |
| discovery | example | 0.477198 | 0.879719 | 0.809338 |
| discovery | explanation | 0.510190 | 0.860131 | 0.730450 |
| discovery | all | 0.441285 | 0.897408 | 0.797634 |
| development | example | 0.478458 | 0.878819 | 0.803328 |
| development | explanation | 0.652052 | 0.758184 | 0.571945 |
| development | all | 0.481970 | 0.876263 | 0.757806 |
| heldout | example | 0.536779 | 0.843928 | 0.727910 |
| heldout | explanation | 0.721408 | 0.693352 | 0.504418 |
| heldout | all | 0.544345 | 0.839570 | 0.675913 |

[Source: dictionary reconstruction](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/dictionary_reconstruction.csv). Original heldout errors exceed discovery errors, especially for `explanation`. This is a measured split difference, not a model update or new evaluation-population claim.

Each ending's fixed positive discovery ordering gives the following heldout relative errors. Random entries are medians over 1,000 sets from the full dictionary, not activity- or frequency-matched sets.

| k | example fixed list | explanation fixed list | example random median | explanation random median |
| --- | --- | --- | --- | --- |
| 1 | 0.984013 | 0.986100 | 1.000000 | 1.000000 |
| 4 | 0.966011 | 0.934994 | 1.000000 | 1.000000 |
| 8 | 0.828401 | 0.916278 | 1.000000 | 1.000000 |
| 16 | 0.799584 | 0.888531 | 1.000000 | 1.000000 |
| 32 | 0.719568 | 0.828926 | 0.999977 | 1.000000 |

All-member errors are 0.536779/0.721408. Atk 32, the fixed-list 95% family intervals are [0.691360, 0.775842]/[0.773115, 0.881673]. Randomk 32 central 95% ranges are [0.994242, 1.000535]/[0.994127, 1.000892]. [Source: every split/k/random comparison](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/cumulative_reconstruction.csv). Selected members outperform uniform random small sets but do not reproduce the complete-dictionary level at 32 members. Uniform sampling often selects members inactive on this panel; it is not a matched concentration null. No best k is selected and no curve is forced monotone.

## 5. Frozen members and what replication means

For the main lists, strictly positive discovery directional contribution is ranked separately by ending. Expanded per-domain lists require the same activation-difference sign in all four discovery ending×wording cells and a strictly positive mean directional contribution across endings. The two individual ending contributions need not each be positive. Rank by that mean, with member-ID ties; no frequency or heldout information enters. The exact lists are:

| List / 名单 | Frozen IDs in discovery order / 按发现顺序固定的ID |
| --- | --- |
| example Top32 | 13964, 516, 13472, 7971, 16122, 8963, 7388, 3464, 14, 4795, 5494, 14394, 13276, 3196, 13465, 10807, 652, 7182, 15259, 13662, 3483, 3423, 10203, 13855, 3606, 11939, 3018, 3585, 5913, 2138, 359, 12882 |
| explanation Top32 | 13964, 516, 10807, 16122, 7388, 13276, 7971, 3464, 14, 8963, 13465, 4795, 13848, 8399, 9622, 547, 15259, 8060, 1513, 16, 13472, 5494, 3483, 652, 13413, 1676, 7415, 359, 9483, 13662, 2468, 9508 |
| math64 | 516, 16122, 13472, 7388, 8963, 3464, 10807, 4795, 5494, 14394, 15259, 13848, 10203, 359, 8399, 3423, 16, 16323, 9508, 12882, 3585, 9822, 3018, 9713, 15847, 8389, 9277, 13299, 10323, 13925, 2325, 3988, 4040, 8790, 12471, 461, 7303, 11083, 952, 5265, 1237, 1713, 2109, 13473, 258, 8008, 8151, 12957, 4186, 7763, 8909, 5339, 8030, 9900, 9374, 8047, 7820, 7958, 2675, 14024, 15195, 536, 13069, 3640 |
| biology64 | 13964, 7971, 14, 13276, 13465, 652, 3483, 13662, 15057, 12820, 13413, 124, 7978, 9483, 4346, 2468, 12179, 8624, 5900, 8611, 10223, 3837, 11159, 8255, 2163, 10563, 13254, 10862, 6739, 10870, 4371, 10511, 5562, 4529, 10525, 7315, 2431, 7570, 515, 12406, 12976, 13245, 16382, 11013, 7564, 3136, 8594, 6455, 16200, 2396, 8882, 15216, 1765, 10254, 2757, 10200, 16312, 14644, 6369, 11077, 424, 9458, 16262, 3235 |

[Immutable candidate record](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/analysis/candidate_freeze.json). All four lists together contain 141 distinct members. Expanded lists contain 64 each without relaxing a gate. The original-heldout use-preference rule requires the discovery sign in all four cells and exclusion of zero in each ending's activation-difference interval. It yields 16/64 math and 20/64 biology:

| Preference / 使用偏向 | Recurring IDs / 复现ID |
| --- | --- |
| math | 16122, 7388, 8963, 3464, 14394, 15259, 10203, 359, 13299, 8790, 12471, 461, 1237, 2109, 13473, 4186 |
| biology | 13964, 652, 3483, 12820, 7978, 8624, 10223, 3837, 2163, 4371, 5562, 4529, 12976, 16382, 7564, 16200, 2757, 16312, 6369, 424 |

[All passed and failed candidate rows](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/domain_candidate_replication.csv). These 36 are **recurring use-preference candidates**. As a separately labeled pointwise diagnostic, 26 of 36 (13 perdomain) also have positive signed-contribution intervals at both endings. The complete 141 union has 27 such members. This additional diagnostic neither revises selection nor converts usage recurrence into semantic/causal stability. [Separate flags](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/candidate_replication_flags.csv) retain both quantities.

A real example shows why that distinction matters. In heldout F04, the mathematical core is an integer divisible by both three and five, using relative primality to infer divisibility by their product. The biological core describes a bacterium's glucose/lactose use and glucose suppression of lactose-enzyme production. Both take the same final ending. f13964 occurs in 100% of both domains at both endings, yet heldout math/biology means are 0.033092/0.044375 for example and 0.094827/0.102423 for explanation. Delta z is −0.011284/−0.007596, but signed contributions are +0.023253/+0.026597. Its explanation activation-difference interval excludes zero, while its signed-contribution interval [−0.004537, 0.083930] crosses zero. F04 W0/example even reverses the aggregate preference, 0.039776 math versus 0.034404 biology; W1/example is 0.028789 versus 0.042827. An average preference is not a rule for every text.

f16122 illustrates limited panel specificity: heldout example activation occurs in 24/24 math and 0/24 biology rows; explanation is 19/24 math and 0/24 biology. In F23's budget-allocation mathematical prefix it is 0.027457 with example and zero with explanation. f7971 changes wording sign under explanation. f4186 has only 0.434875% independent reference occurrence but 100% occurrence in both heldout domains under explanation. These cases and actual texts are in the [worked examples](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/examples.md), with [per-text activations](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/candidate_text_activations.csv), [candidate conditions](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/candidate_conditions.csv) and [ending controls](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/candidate_ending_controls.csv).

## 6. Frequency composition and family variation

Reference frequency is native gated z>0 over 65,536 independent DCLM positions. At least 20 hits is inherited support. Of 16,384 members, 13,357 are supported; 3,027 are below support (749 zero, 2,278 with 1–19 hits). No reference member is missing. “Unknown” remains in the unified table label but the present unknown count is zero.

| Grouping | Cut points in occurrence percent | Low/middle/high counts | Meaning |
|---|---|---|---|
| Main log equal width |0.451725536288%;6.686505701697%|5808/6917/632|Equal multiplicative ranges, about14.8fold per interval|
| Original equal count, ties preserved |0.2593994140625%;1.34429931640625%|4469/4437/4451|Relative rank thirds|
| Linear equal width sensitivity |33.0118815104167%;65.9932454427083%|13281/63/13|Equal percentage-point widths|

Both equal-width methods span the supported range 0.030517578125%–98.974609375%. Log bins suit multiplicative differences in this skewed reference; they are not universal semantic categories. [Exact memberships/boundary rules](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/frequency_groups.json) and [all-member rates](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/all_feature_frequency.csv) are saved. The candidate union contains 1 log-low, 62 middle, 78 high and 0 below-support members; all-member analysis remains primary.

For the original-heldout true-difference direction, sum positive and negative contributions across every member in a group:

| Ending | Group | Active/all | Positive | Negative | Net |
| --- | --- | --- | --- | --- | --- |
| example | low | 13/5808 | 0.003415 | -0.000278 | 0.003137 |
| example | middle | 321/6917 | 0.455433 | -0.007074 | 0.448360 |
| example | high | 256/632 | 0.288904 | -0.012491 | 0.276413 |
| example | low_support_or_unknown | 0/3027 | 0.000000 | 0.000000 | 0.000000 |
| example | residual | — | 0.272090 | 0.000000 | 0.272090 |
| explanation | low | 11/5808 | 0.002909 | -0.001234 | 0.001675 |
| explanation | middle | 242/6917 | 0.256824 | -0.011736 | 0.245089 |
| explanation | high | 259/632 | 0.283155 | -0.025479 | 0.257676 |
| explanation | low_support_or_unknown | 1/3027 | 0.000000 | -0.000022 | -0.000022 |
| explanation | residual | — | 0.495582 | 0.000000 | 0.495582 |

[Full groups, intervals and sensitivity views](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/frequency_signed_contributions.csv). Net group shares plus residual sum to 1. Low-frequency net shares are small in this panel, with only 13/11 active members; middle/high totals are larger, with different group sizes and activation support. Group totals therefore are not per-member advantage measures. Strong reference frequency can coexist with a domain-associated difference in activation strength, as f13964 illustrates.

The separate activation-variance calculation defines B=Delta z²/4 (domain-center separation), F=mean squared family-mean displacement from its domain mean, and W=within-family wording variance. Equal weights and a common population denominator yield T=B+F+W. Compute B/T, F/T, W/T separately for every member, then average equally across currently variable members. T=0 is NA; raw z variance is not summed across differently parameterized members.

| Ending | Frequency | Variable/all | B/T domain | F/T family | W/T wording |
| --- | --- | --- | --- | --- | --- |
| example | low | 13/5808 | 8.94% | 57.28% | 33.77% |
| example | middle | 321/6917 | 12.93% | 52.79% | 34.28% |
| example | high | 256/632 | 11.23% | 54.19% | 34.58% |
| explanation | low | 11/5808 | 18.55% | 43.44% | 38.01% |
| explanation | middle | 242/6917 | 10.07% | 49.31% | 40.62% |
| explanation | high | 259/632 | 7.74% | 49.48% | 42.78% |

For below-support members, example is entirely NA and explanation has one variable member (B/F/W42.87/25.27/31.86%). Frequency versus B/T Spearman rho is −0.0434 [−0.1139, 0.0150] for example and −0.1473 [−0.1814, −0.0662] for explanation. Frequency versus F/T is weak with intervals crossing zero in both endings. Thus the group ordering is ending-dependent; the low-frequency average in explanation represents only 11 members. [Full 98,304 member/ending/split rows](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/all_feature_variance_components.csv), [group tables](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/group_variance_shares.csv) and [continuous associations](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/continuous_frequency_associations.csv) preserve all cases. The squared B term has finite-sample positive bias; percentile intervals can miss the point estimate, and are not semantic-significance gates.

## 7. Independent spectrum and main figures

The R07 natural-text basis partitions 1024 PCs into 16 bands of 64. For both true and reconstructed differences the denominator is the true difference's total squared length. First synthesize the vector, then project and square. The first band is:

| Ending | PC1–64 true energy / true total | PC1–64 reconstruction / true total | PC1–64 residual / true total |
| --- | --- | --- | --- |
| example | 0.476980 | 0.393041 | 0.029252 |
| explanation | 0.298679 | 0.176457 | 0.075392 |

[All 16 bands for all 9 conditions](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/spectral_decomposition.csv). The reconstruction puts less energy than the true difference inPC 1–64 under both endings. Residual energy is not true energy minus reconstructed energy because the cross term remains. The reconstructed spectrum need not sum to 1. This is a comparison of fixed reference directions, not a knowledge-location map.

| Figure | Axes and registered contrast | Actual reading and boundary | Source |
|---|---|---|---|
|1a relative error;1b cosine|Ending versus whole-dictionary residual ratio or cosine, family intervals|High alignment can coexist with incomplete reconstruction;0.537/0.721residual ratios remain|[1a](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure1a_dictionary_relative_error.png),[1b](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure1b_dictionary_cosine.png); dictionary table|
|2 per ending|Fixed member count versus old-heldout vector error; all-member/random references|Few-member matching would support concentration; here32remains above complete-dictionary error|[example](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure2_cumulative_example.png),[explanation](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure2_cumulative_explanation.png); cumulative table|
|3 per ending|Reference group versus positive/negative/net directional contribution, counts and residual|Middle/high net totals dominate current low total; group size/activation and residual remain part of reading|[example](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure3_frequency_example.png),[explanation](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure3_frequency_explanation.png); frequency table|
|4 per ending|64-PC band versus squared projection divided by true total|Differences locate reconstructed-spectrum mismatch; energies are not additive memberwise|[example](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure4_spectrum_example.png),[explanation](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/figures/figure4_spectrum_explanation.png); spectral table|

Frequency distribution, binning sensitivity and family-variance figures are separate supplementary files, linked from their [component report](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/summary.md). Their group-size/NA labels are part of the evidence.

## 8. Controlled distance measurement

The extension keeps each original domain core, wording and ending, moves the original neutral postfix before the core, and redistributes the same neutral filler blocks before/after it. Every derived text has 240 tokens and final target 239. Semantic-core endpoint-to-target distances are 16/32/64/96/144, so the core endpoint positions are 223/207/175/143/95. For every base construction, a date sentence immediately after the core changes Monday to Tuesday at one token. Each source's token multiset is identical across distances. Five families need one leading `brief` compensation after retokenization, affecting 18 original sources and 180/3,840 derived rows. [Complete construction QA](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/construction_audit.json), [all actual texts](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/panel.jsonl) and [text examples](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/examples.md) retain that flag.

All 3,840 derived rows plus 2 exactR 08 replays completed, 3,842/3,842 attempts. Existing H10080 GB MIG3g.40gb was used, with peak GPU allocation 4,540,560,896 bytes and 165.964 seconds measured extraction time. Both replay true joint vectors and z match exactly; native threshold-gate checks pass. Model and A22 state hashes match before/after. No zero-z row or nonfinite value occurred; active members per row range 212–259. [Completion](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/forward/completed.json),[qualification](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/forward/qualification.json).

Distance scale s_j is each member's RMS over the original 192 R08 discovery rows, distinct from the training restoration scale 374.35. Raw D is mean math-minus-biology activation divided by s_j; the oriented version multiplies the original discovery preference sign. E is absolute domain-pair change minus mean absolute Monday/Tuesday change across the two domains, averaged within family/wording and divided by s_j. Signed D preserves reversals that absolute E would hide. Save raw activation and decoder-amplitude units too. Retention D_d/D_16 is NA for abs (D_16)<=1e-6 and flagged unstable when the d16 family interval covers zero.

The 3,840 row cache produces all-member statistics and candidate curves with 500 paired-family bootstraps (seed 2026102913). At distance 144 only, E on 12 original-heldout families receives all 4,096 one-sided sign flips; one BH correction covers 141 unique candidates×2 endings=282 hypotheses. The sign-flip reference assumes family-level null symmetry. E measures excess over this one-token date control; replacing an entire domain core changes more tokens. Filler reordering and framing travel with distance. The newly constructed 16-token condition is not the original short R 08 input.

At 144,83 example and 72 explanation candidate-ending cases have E q<.05. Requiring both wording averages to preserve the original discovery domain direction leaves 37 and 26; their cross-ending intersection has 14 members. Therefore the 83/72 counts cannot be called stable domain preferences. All 141 candidates have nonzero discovery RMS, but across the full dictionary 15,487 members have zero discovery RMS and standardized distance quantities are NA. The log-low group has 5,808 members, only 20 with a nonzero original discovery RMS. New heldout active low members number 4 at both 16/144 for example and 5/6 for explanation; these data do not characterize the entire low-frequency group's range.

The saved [distance summary](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/analysis/summary.json),[candidate curves](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/tables/candidate_distance_metrics.csv),[all-member frequency statistics](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/tables/all_feature_frequency_distance.csv),[all-feature estimates](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/analysis/all_feature_estimates.npz) and [family metrics](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/analysis/family_metrics.npz) preserve all distances, endings, controls, signs, raw units and insufficient support. Additional intersections and real examples are recorded below.


### Distance replication, denominator support and actual examples

The far comparison below requires both E at 144 to pass BH and both wording means to preserve the original discovery direction. It is a narrower descriptive intersection than E significance alone.

| Candidate population / 候选范围 | N | example far | explanation far | Both endings / 两结尾 |
| --- | --- | --- | --- | --- |
| all 141 | 141 | 37 | 26 | 14 |
| domain_math64 | 64 | 10 | 6 | 1 |
| domain_biology64 | 64 | 22 | 17 | 12 |
| domain128 | 128 | 32 | 23 | 13 |
| original_replication36 | 36 | 11 | 12 | 7 |

Among the 14 members passing both far endings, 9 are log-middle and 5 log-high. Adding original-direction consistency at both new 16-token endings leaves 10 of 141. Among the original 36 use-preference candidates, 7 pass both far endings and 3 also retain both new near-ending directions:f424, f4529, f7564. Only 9 of 36 retain both directions at the new near condition in the first place. Consequently the remaining 27 cannot all be described as losing an original preference because of long distance; the 240-token framing already changed their response near the target.

Across the full log-low/middle/high groups, nonzero original discovery RMS counts are 20/500/376. Old-heldout near/far active counts are 4/4,224/198,215/195 for example and 5/6,157/156,190/181 for explanation. Near intervals excluding zero support 2/99/101 and 3/52/54 numeric far/near ratios. Among members additionally maintaining the original direction in both near wordings, middle/high median ratios are 0.672/0.702 for example and 0.600/0.687 for explanation; the corresponding low-group samples contain only 1 and 3 members. These are conditional sample summaries, not a group-wide temporal ordering. [Exact support and all binning schemes](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/tables/frequency_near_far_support.csv).

For a concrete successful example, reuse heldout F 06's rectangular-tile floor and leaf-pore biological context. At distance 144 the core ends at 95 and the target remains 239. Under example, W0, f424 math/bio activations are 0.010436746/0.012389871, a signed difference −0.001953125. The matched Tuesday versions are 0.010925028/0.012634012. Mean absolute date-edit change is 0.000366211, leaving 0.001586914 excess absolute domain response for this single wording/family. The complete texts are in [the fixed F06 table](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/tables/fixed_F06_raw_examples.csv); this one-row illustration is distinct from the 12 family estimates.

The full five-distance f424 heldout curve, in original discovery-RMS units, is:

| Distance | example D | example E | explanation D | explanation E |
| --- | --- | --- | --- | --- |
| 16 | -0.7223 | 0.7391 | -0.1680 | 0.1798 |
| 32 | -0.7031 | 0.7622 | -0.1801 | 0.1707 |
| 64 | -0.7471 | 0.8301 | -0.1432 | 0.1314 |
| 96 | -0.4793 | 0.5687 | -0.1627 | 0.1815 |
| 144 | -0.6987 | 0.6048 | -0.1916 | 0.1764 |

f424 example far/near ratio is 0.967 [0.602, 1.547]; the five-point curve is nonmonotonic. Middle-frequency f8624 has ratios 0.390 [0.198, 0.563] for example and 0.664 [0.482, 0.822] for explanation. High-frequency f9900 has example ratio 0.904 [0.727, 1.078], but zero far explanation activation and an unstable near explanation denominator. A clear contrary case is high-frequency f14: its example D is +0.1174 at 16 and +0.0652 at 144, opposite the original biology preference even near the target, while E144 remains positive (q 0.002732). Its E signal therefore cannot be called retention of that original domain preference. [All ratio intervals](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/tables/candidate_retention_intervals.csv).

The distance branch is complete, with its [English component report](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/summary.md), [Chinese report](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/summary_cn.md), [six-figure reading guide](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/figures_cn.md) and [52-file manifest](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/artifact_manifest.json). No additional forwards were used for these intersections or illustrations.

## 9. Numerical checks and the three audits

The main [numerical audit](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/analysis/numerical_audit.json) records exact residual closure, signed closure discrepancy at most 2.22e-16, and independent FP 64 decode-mean versus mean-decode discrepancy at most 1.93084e-13. A CPU BF16 decoder-precision diagnostic is 0.00172–0.0036067 of the true-difference norm across conditions; it is separate from the much larger observed residual. It does not claim a GPU kernel's bitwise reconstruction. A second implementation recomputed checkpoint/scale/gate identity, all 9 means and bootstrap intervals, candidates, spectra, frequency totals and random controls:1,166 checks passed, 0 failed. [Independent audit](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/analysis/main_independent_audit.json).

The family variance identity has maximum absolute error 1.73472e-18 and relative error 1.09131e-15; every member remains in the 98,304 row table. [Family checks](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/analysis/checks.json). Distance replay and parameter checks are actual GPU forward checks, kept separate from the CPU diagnostic.

The three recorded audits are: scientific identification (question, four rivals, reconstruction versus causal/semantic claims); data/statistics (families, exposed splits, candidate freeze, independent reference bins, intervals and controls); implementation/numerics (native interface, scale/gate, zero updates, numerical identities and actual receipts). [Audit record](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/audits.md),[coverage ledger](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/coverage.md). Current-entrypoint checking found 31 pre-existing untracked/stale-map issues; these did not change asset identities. Source/link/math-delimiter checks do not establish rendered mathematics or scientific acceptance.

## 10. Evidence lineage and artifact map

| Evidence question | Actual input and computation | Result evidence | Eligibility and remaining boundary |
|---|---|---|---|
| Does the dictionary describe the real difference?|Same384h/z; normalized decoder linear sum|[norm/cosine table](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/dictionary_reconstruction.csv),[vectors](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/analysis/decomposition_vectors.npz)|Valid descriptive decomposition; residual remains|
| Is it concentrated in fixed members?|Discovery ordered positive shares; old-heldout vector sums and1000random sets|[subset table](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/cumulative_reconstruction.csv),[freeze](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/analysis/candidate_freeze.json)|Exploratory fixed-list portability; random sets not activity matched|
| Does use preference recur?|Fourheldout cell signs plus two activation-difference intervals|[replication](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/domain_candidate_replication.csv),[conditions](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/candidate_conditions.csv)|36usage candidates; signed contribution is a separate quantity|
| Which frequency groups compose it?|Independent reference bins; all-member signed sums|[frequency table](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/frequency_signed_contributions.csv),[rates](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/all_feature_frequency.csv)|Group totals with size/activity; not per-member advantage|
| Domain or individual-family variation?|Nested B/F/W per member, ending and split|[full components](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/tables/all_feature_variance_components.csv)|Family/wording associations; T0NA and nonlinear-bootstrap bias|
| Is spectrum reproduced?|Sum vector then project into fixedR07 bands|[spectrum](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/tables/spectral_decomposition.csv)|Geometric distribution with shared true denominator|
| What happens across distances?|Matched-length/inventory derived inputs; date edit; native shared z|[raw parts](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/forward),[distance statistics](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/analysis/summary.json)|Constructed-context response; filler/order/edit-magnitude confounds retained|

Primary output producers are `main/analyze.py`, `frequency_family/analyze.py`, `frequency_family/render.py`, `distance/prepare.py`, `distance/acquire.py` and `distance/analyze.py`. Exact hashes/inputs are in [main freeze](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/freeze.json),[family manifest](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/artifact_manifest.json),[distance authorization](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/run_authorized.json) and [distance statistics freeze](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/analysis/pre_statistics_freeze.json). Decoder/scale factors, vectors, full tables and raw shards remain execution-side; research records do not duplicate checkpoint payloads. Main and family stages performed 0 new forwards; distance 3, 842. All stages performed 0 parameter updates.

## 11. Reproduction and completion boundary

The following are the actual stage entry points, run with the preserved environment and frozen files. Main analysis refuses to overwrite a completed result; reproduction requires a separate output workspace with preserved source hashes. These are records of commands, not an automatic rerun request.

```bash
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/analyze.py
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/render.py
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/main/analyze.py
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/audit_main.py
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/prepare.py
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/acquire.py
python /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/analyze.py
```

The saved protocol/configs contain the 500 bootstrap counts and seeds 2026102910/11/13, random-reference seed 2026102912 with ending offset, fixed lists and exact input revisions. No new checkpoint was trained or selected. The substantive result is a bounded reconstruction and response description: residual size, member-combination requirement, ending dependence and reference-frequency/family distinctions are now measured. The next decision belongs to the researcher reviewing these observations. No automatic new experiment, dictionary, router, intervention or publication follows.


## 12. Final output registration and cache-only supplement

The [separate A–D supplement](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/supplement_ABCD.md) retains the additional request, fixed definitions and post-hoc status. It links all 141 candidate rows, unit-decoder spectra, full-dictionary and matched backgrounds, and the frequency-by-band signed contribution matrix. The original frozen Protocol and primary output arrays were not revised. C/D passed 2,141 independent checks, with maximum discrepancies of 2.11e-15 for unit-decoder energy and 2.22e-16 for joint contribution. D rows, including residual, equal B's signed group totals; columns equal true-difference band energies; all cells sum to one. Residual contributions span the spectral bands. [Independent C/D audit](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/supplement_ABCD_20261029/analysis/independent_CD_audit.json). The background audit passed 26 checks. These are computation checks, not semantic or causal confirmation.

The distance branch independently passed all 16,239 construction/statistical checks after the extraction and primary reporting stages. The audit recomputed all saved member/candidate metrics and fixed 282 far hypotheses, retaining zero-RMS NA cases and the assumptions of the family sign-flip reference. [Distance audit](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/frequency_family/analysis/distance_independent_audit.json).

All six actual output groups are registered in [the asset index](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/asset_registration.json) and explained in [the input/output guide](/data/250010109/Research_System/assets/domain_difference_decomposition_r09_20261029.md). The [current strict access receipt](/data/250010109/Research_System/assets/checks/20261029T152118Z_r09_actual_outputs.json) passed all six on 2026-10-29 at 15:21 UTC. Exact IDs are preserved in the index; no training checkpoint is claimed. The [execution manifest](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/artifact_manifest.json) contains 67 main/supplement file records and branch manifests. [Reading payload manifest](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/payload_manifest.json) and [source guide](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/sources.md) preserve selected figure/table identities for local delivery. Payload registration and local reading synchronization do not promote scientific acceptance or publish the work.
