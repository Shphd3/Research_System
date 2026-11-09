# S13: shared-member reference frequency and local coactivation relations

In the eight selected explicit category groups, shared sibling members have lower mean reference frequency than the prespecified direct-parent comparator in32/32conditions:16/16original-domain newtexts and16/16added-domain newtexts. This is relative frequency, not absolute rarity or a universal semantic hierarchy. Named rephrasing has31/32support and oneunresolved. Attributes have8support/24insufficient; scenarios4support/28insufficient, mostly behavior qualification.

Purpose: determine which nativeSAEcoordinates are shared across granularity, how membership/strength changes, and whether fixed local relations exceed individual-frequency/Top32 references. Exact officialQwen3-0.6B Base; block27attentiono_projoutput and postnormalizationMLPinput use independent30000/ReLU/Top32dictionaries.6912newprefixes:DEV24frames/8contextclusters,CONF48frames/16clusters,fourwordings. S11/S12 are historical, not blind confirmation. No base/SAE/routertraining or functionalintervention.

For each shared intersection, average p_f=count/6000, then contextclusters equally. References:Q6000questionprefixes andG6000DCLMprefixes,first≤128bodytokens plus terminalDescriptioncolon. References are reused,not new controlled-data replications. D=direct-parent shared frequency minus sibling shared frequency. Primary jointcluster/reference bootstrap andHolm16/reference/wording; complete rawlevels:

| site | domain | reference | coarse_percent | fine_percent | D_pp | joint95CI_pp | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATTN_SAE | animal | questions | 17.05 | 13.04 | 4.01 | [2.95, 5.15] | SUPPORT |
| ATTN_SAE | animal | general | 15.72 | 12.76 | 2.96 | [2.25, 3.74] | SUPPORT |
| ATTN_SAE | vehicle | questions | 17.05 | 15.06 | 1.99 | [1.03, 3.10] | SUPPORT |
| ATTN_SAE | vehicle | general | 15.72 | 14.12 | 1.60 | [0.86, 2.39] | SUPPORT |
| ATTN_SAE | fruit | questions | 16.86 | 14.97 | 1.89 | [0.95, 2.82] | SUPPORT |
| ATTN_SAE | fruit | general | 16.58 | 14.32 | 2.26 | [1.52, 2.96] | SUPPORT |
| ATTN_SAE | furniture | questions | 16.86 | 15.71 | 1.15 | [0.32, 2.02] | SUPPORT |
| ATTN_SAE | furniture | general | 16.58 | 15.63 | 0.95 | [0.37, 1.60] | SUPPORT |
| ATTN_SAE | clothing | questions | 17.45 | 13.20 | 4.24 | [3.21, 5.36] | SUPPORT |
| ATTN_SAE | clothing | general | 19.62 | 14.35 | 5.27 | [4.09, 6.59] | SUPPORT |
| ATTN_SAE | instrument | questions | 17.45 | 12.29 | 5.16 | [3.87, 6.56] | SUPPORT |
| ATTN_SAE | instrument | general | 19.62 | 14.35 | 5.27 | [3.94, 6.78] | SUPPORT |
| ATTN_SAE | flower | questions | 16.54 | 13.32 | 3.22 | [2.42, 4.02] | SUPPORT |
| ATTN_SAE | flower | general | 16.45 | 14.54 | 1.91 | [1.21, 2.61] | SUPPORT |
| ATTN_SAE | cutlery | questions | 16.54 | 14.54 | 2.00 | [1.17, 2.81] | SUPPORT |
| ATTN_SAE | cutlery | general | 16.45 | 14.97 | 1.48 | [0.99, 1.99] | SUPPORT |
| MLPIN_SAE | animal | questions | 46.74 | 39.60 | 7.14 | [5.61, 8.66] | SUPPORT |
| MLPIN_SAE | animal | general | 43.30 | 36.40 | 6.90 | [5.53, 8.39] | SUPPORT |
| MLPIN_SAE | vehicle | questions | 46.74 | 40.96 | 5.78 | [4.34, 7.24] | SUPPORT |
| MLPIN_SAE | vehicle | general | 43.30 | 38.32 | 4.98 | [3.67, 6.44] | SUPPORT |
| MLPIN_SAE | fruit | questions | 43.95 | 41.05 | 2.90 | [1.45, 4.40] | SUPPORT |
| MLPIN_SAE | fruit | general | 41.04 | 37.68 | 3.36 | [2.02, 4.80] | SUPPORT |
| MLPIN_SAE | furniture | questions | 43.95 | 41.04 | 2.91 | [1.79, 4.15] | SUPPORT |
| MLPIN_SAE | furniture | general | 41.04 | 38.28 | 2.76 | [1.83, 3.80] | SUPPORT |
| MLPIN_SAE | clothing | questions | 47.62 | 39.99 | 7.63 | [6.36, 9.04] | SUPPORT |
| MLPIN_SAE | clothing | general | 44.50 | 37.47 | 7.03 | [5.66, 8.49] | SUPPORT |
| MLPIN_SAE | instrument | questions | 47.62 | 37.69 | 9.93 | [8.41, 11.34] | SUPPORT |
| MLPIN_SAE | instrument | general | 44.50 | 36.20 | 8.30 | [6.83, 9.90] | SUPPORT |
| MLPIN_SAE | flower | questions | 43.09 | 38.15 | 4.94 | [3.67, 6.30] | SUPPORT |
| MLPIN_SAE | flower | general | 40.49 | 36.45 | 4.04 | [2.83, 5.27] | SUPPORT |
| MLPIN_SAE | cutlery | questions | 43.09 | 41.34 | 1.74 | [0.34, 3.20] | SUPPORT |
| MLPIN_SAE | cutlery | general | 40.49 | 38.82 | 1.66 | [0.39, 2.91] | SUPPORT |


![Raw frequency levels](figures/shared_frequency_levels.png)

Colored intervals condition on fixed reference frequencies; gray segments only connect armmeans. PrimaryDusesjointreference/context uncertainty separately. Secondary parent/child-mixture baselines are not primaryrescues. Positive means do not establish stochasticdominance:twoexplicitq75contrasts have opposite nonsignificantpointestimates.

Local model: a node is oneSAEcoordinate. c→u means the less prevalent c often coactivates with a moreprevalent u, under DEVconditional/support thresholds. Transitive reduction compresses graphreachability,not causalmediation or semanticcomposition. The22fixededges are tested against label-stratified fullmatrixCurveball nulls preserving eachrow32andeverycolumncount; finite-chain distribution/pvalues areMonteCarloapproximations. E=P(u|c)−mean_nullP(u|c). In explicitCONF,7/22have excesssupport and7/22also retain originalconditionalrolethresholds. PooledEisweightedbycentersupport,not evidence in everyclass.

Categoryexcesscontrasts are separate: ΔE=Δrawconditional−Δnullbaseline. They cannot automatically identify changing pure dependence. Rawconditionals,allfourcells,smoothedlogORandcoverage remain in scaleaudit. Nullrandomization does not preserve pairedfamily/contextrows acrosslabels;clusterintervals do notrepairthisnull. Explicitcategoryoutcomes: {'INSUFFICIENT': 6, 'UNRESOLVED': 5},with5/16configurations having noDEVedge and henceNOTrun.

Smallstatisticalreadoutscompare bestsingle,additive12–14binarynodes,andonefixedproduct;parameters locked onDEV. FullCONFlogloss/accuracy/status and rawpredictions retained. ThreeDEVproductcolumns duplicate anexistingcenter;auxiliary fixed-parameter duplicate substitution locked before readout outcomes, after frequency summaries were available, diagnoses L2regularization alternatives without refitting. Any gain is neithernewinformation norcausalmodeluse.

Knowledgeupdate: explicit mean-relative-frequency result extends to these eightgroups; implicitsemantic interpretation remains behaviorlimited. EarlierS11distinguishing-memberfrequency had6support/5opposite/4unresolved/1insufficient,not a universal fine-to-rarefeature rule. Membership turnover/amplitude descriptions and genuine relation claims are distinct. No causalfeaturefunction,training-timeevolution,optimalexperts orlearningefficiency is established; scientificacceptance/closureUnknown.

Read [Chinese full explanation](summary_cn.md), [methods](detailed.md), [Chinese detail](detailed_cn.md), [literal cases](casebook_cn.md), [all relations](relation_results_cn.md), and [reproduction](README_reproduce.md).
