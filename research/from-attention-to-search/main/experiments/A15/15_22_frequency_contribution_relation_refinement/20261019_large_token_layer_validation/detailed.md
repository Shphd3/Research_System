# Detailed: larger-sample and cross-layer token / feature frequency review

[Summary](summary.md) · [中文](detailed_cn.md) · [Protocol](protocol.md)

**Evidence eligibility: BOUNDED.** Engineering completed with key count and provenance checks passing. Evidence supports descriptive review of frozen caches, not independent-document confirmation, causality or learning judgments. The researcher's scientific interpretation and question closure remain Unknown. DCLM's position profile is weak and ID-weighted direction negative, while its feature-weighted association is positive; these are different estimands, not one success/failure score.

## 1. Question, hypothesis, and objects

Existing Anchor H1 predicts that rarer current tokens may have larger final-layer rare-feature shares. This round expands the sample/layer review and examines direction, magnitude and weighting. Rivals are identity/format/position composition, tail support and the denominator. Freeze Qwen3-0.6B Base and the final 14-layer/F16384 joint CrossCoder. One-based layers 2,4,…,28 are block residual-post; layer 28 precedes final RMSNorm. One z jointly uses all 14 layers; no independent layer activations exist.

Feature p is the reference fraction z_i>0; current-token f uses the same valid window; rarity s=−log10 f. Next targets are excluded. M_low sums shared z times layer decoder norms over the local lowest-frequency pool; T sums all 16,384 features; R=M_low/T. Bias, mean, residual and vector cancellation are omitted. These are not information, explained variance or learning value. Zero denominators and unestimable correlations remain NA. Shared-z hit/count/fraction measures are identical across layers.

The auxiliary feature-weighted statistic correlates −log10 p with mean current-token rarity on a feature's eligible review hits. Exclude p=0/U and features without known-reference-token hits. The ≥20-hit sensitivity is fixed in advance, not selected after seeing outcomes.

## 2. Freeze, actual setup, and deviations

Execution root E: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/token_feature_layer_validation/20261019T_validation`. Producer root P: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z`.

| Item | Registered / expected | Actual and eligibility |
|---|---|---|
| Authorization | Current-session no-training larger-sample/cross-layer analysis | One local CPU execution; no inference/training/GPU; no preconfirmed conclusion |
| Freeze | E/provenance/frozen_execution.json at 2026-10-19 05:19:00UTC | Code SHA256 `0a232e3915b5a26798567f50d5149242d0136ca03e022a4600ce974c8ed6e426`; Markdown organized later, not prior human block confirmation |
| DCLM | Existing10,485,760 window and phase1 D/V | D5,238,097/V5,247,663;10,249 contexts / 81 blocks;41 V blocks, document independence UNKNOWN |
| Tulu | Existing TRAIN/EVAL, cross-layer supplement only | 85,548/22,446;256 EVAL conversations; exposed |
| Frequencies/pools | Reference p/f, four positive-log bands plus U | Tulu B1=1694/U907;DCLM B1=314/U353; all retained |
| Token groups | Equal-ID quantiles, higher method, no split ties | DCLM counts[3,7,14,36];Tulu[1,1,2,4], empty second group remains NA |
| Control | Fixed old 1694 Tulu pool | Distinct from local DCLM rarity |
| Estimation | Overall rho points;1000 block bootstraps for block means/28−2 difference | Seed20261019;no overall-rho CI;paired NA sets verified identical |
| Output metadata | Ten core tables | Frozen code reported tables=8; post-execution metadata-only correction to10, plus three derived/definition/qualification tables,13 total |
| Resources | CPU8/RSS16GiB/new disk1GiB/formal30min,total90min | Core314.8s;peak process RSS 4.1574GiB;soft-guard limitations retained below |

Reuse norm from P/decoder_geometry.npz, shape14×16384. Cross-layer absolute M in different normalized coordinates is not a common-unit physical amplitude; layer-wide positive scaling leaves R unchanged. Geometry SHA256 is `b74cc20f563ea535c5b4d05e9f58bb3411f6bd6138d969afe4b25edbe4c28a8e`; parent saved checkpoint SHA256 is `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`. Phase1 CUDA norms versus old-bridge CPU norms differ by at most4.7684e−7, retained FP32 reduction roundoff rather than bitwise identity.

Input IDs: `representation_crosscoder_qwen3_final14_f16384_val10485760_phase1_20261013t173130z` and `analysis_crosscoder_feature_relation_phase1_20261013t173130z`, with original SFT/bridge bindings for Tulu. Access, manifests and recorded identities qualify addresses/interfaces/provenance, not contamination freedom. No new checkpoint or optimizer exists; training batch/steps/rate are NOT APPLICABLE.

## 3. Evidence lineage

| Claim | Source and transformation | Observation | Eligibility / limitation |
|---|---|---|---|
| Larger-sample position profile | Phase1 CSR→[layer metrics](tables/layer_metrics.csv) | DCLM local layer 28 position0.006191/ID−0.119041 | BOUNDED;does not reproduce Tulu magnitude/weighting direction |
| Feature-level association | Binary-hit transpose products→[all 32768 rows](tables/feature_token_correspondence.csv),[summary](tables/feature_correspondence_summary.csv) | DCLM0.336019;≥20 gives0.339147 | BOUNDED;all eligible features, not lowest-pool position prediction |
| Layers/block variation | [Block correlations](tables/block_correlations.csv),[stability](tables/block_stability.csv),[diagnostics](tables/diagnostics.csv) | All14 layers;block means and28−2 contrast | BOUNDED;shared z and within-bin dependence |
| Hits/denominator | [Binary](tables/binary_metrics.csv),[groups](tables/groups.csv) | DCLM local hit incidence0.05294%;M rho≈0.006191 | BOUNDED;known-only correlation versus all-position means |
| Fixed-pool migration | [Members](tables/members.csv),[migration](tables/migration.csv) | Intersection 25;11 old features become D-zero-frequency | BOUNDED;pool definitions cannot be interchanged |
| Correctness | E/provenance/checks.json,code_audit.json,final_numeric_checks.json | Tulu max position-wise R discrepancy2.5484e−8;all 16384 DCLM V marginals match | Engineering/measurement checks,not new scientific findings |

## 4. Primary results: all 14 layers

These local lowest-frequency-pool correlations are overall point estimates without CIs. All layers share positions and z.

| Layer | DCLM positions | DCLM equal IDs | Tulu positions | Tulu equal IDs |
|---|---:|---:|---:|---:|
| 2 | 0.00619090 | -0.119064 | 0.258395 | 0.116433 |
| 4 | 0.00619132 | -0.119047 | 0.257472 | 0.118361 |
| 6 | 0.00619124 | -0.119046 | 0.256977 | 0.118731 |
| 8 | 0.00619122 | -0.119044 | 0.257078 | 0.119392 |
| 10 | 0.00619105 | -0.119044 | 0.256594 | 0.119301 |
| 12 | 0.00619079 | -0.119046 | 0.256601 | 0.119638 |
| 14 | 0.00619084 | -0.119046 | 0.256588 | 0.119954 |
| 16 | 0.00619086 | -0.119044 | 0.256500 | 0.120242 |
| 18 | 0.00619071 | -0.119044 | 0.256874 | 0.120532 |
| 20 | 0.00619076 | -0.119043 | 0.257332 | 0.121670 |
| 22 | 0.00619086 | -0.119042 | 0.258166 | 0.123168 |
| 24 | 0.00619101 | -0.119040 | 0.258922 | 0.124152 |
| 26 | 0.00619106 | -0.119042 | 0.258935 | 0.124318 |
| 28 | 0.00619124 | -0.119041 | 0.259051 | 0.124371 |

Known-reference-token positions are5,227,462 in DCLM, with20,201 unseen separate;Tulu 19,070 with3,376 unseen. Of DCLM B1's314 features,283 have reference support<20; all 1694 Tulu B1 features do. [Members](tables/members.csv) retains all other bands. Evidence across mostly well-supported features does not qualify the extreme314-feature tail automatically.

Feature-weighted results are DCLM 15,928 eligible features/rho0.336019 at≥1 hit and15,749/0.339147 at≥20;Tulu 14,610/0.374516 and10,220/0.119556. DCLM has 353 reference-zero features and393 with no known-token review hit;Tulu 907 and1753. These sets may overlap and cannot be added as an exclusion count. A positive feature-level statistic can coexist with a weak position-level and negative ID-level statistic because they average different objects first.

[Support qualification](tables/feature_level_support.csv) further bounds the lowest band: 211/314 DCLM members have known-token review hits and only 34 reach 20; Tulu has 962/1694 and only 2. The old Tulu count of 1198 review-active features includes reference-unseen tokens and therefore does not contradict 962. The ≥20 feature-level direction mostly concerns other frequency bands and cannot rescue the weak lowest-pool position association.

## 5. Groups, hits, and amplitude decomposition

All rows below use layer 28 and local pools. Reference current-token counts define groups separately in each corpus. DCLM Q1 is 1–3, not count1;Q5 is≥37, not old Tulu≥5. Shares and hit incidence are percentages. Source rows for bands2–4 repeat B1 hit fields;they are not those bands' own hit incidences.

| Corpus | Reference token count | Review positions | B1/B2/B3/B4 mean shares(%) | Any B1 hit(%) |
|---|---|---:|---|---:|
| dclm | unseen | 20,201 | 0.001167 / 1.064537 / 22.076090 / 76.858205 | 0.2525 |
| dclm | 1–3 | 47,138 | 0.002643 / 0.684750 / 21.183217 / 78.129393 | 0.1931 |
| dclm | 4–7 | 70,584 | 0.001352 / 0.625595 / 20.584375 / 78.788668 | 0.1233 |
| dclm | 8–14 | 122,368 | 0.000574 / 0.642611 / 20.048659 / 79.308164 | 0.0858 |
| dclm | 15–36 | 267,536 | 0.000691 / 0.776598 / 19.566390 / 79.656327 | 0.0890 |
| dclm | ≥37 | 4,719,836 | 0.000634 / 0.605671 / 20.926419 / 78.467274 | 0.0467 |
| tulu | unseen | 3,376 | 0.246805 / 2.248937 / 32.182878 / 65.317154 | 39.9882 |
| tulu | 1 | 1,278 | 0.265518 / 2.576698 / 31.435001 / 65.722430 | 35.9937 |
| tulu | empty | 0 | NA / NA / NA / NA | NA |
| tulu | 2 | 761 | 0.253490 / 2.526590 / 30.475861 / 66.743910 | 32.4573 |
| tulu | 3–4 | 1,112 | 0.273441 / 2.644351 / 29.442871 / 67.639124 | 29.0468 |
| tulu | ≥5 | 15,919 | 0.047309 / 2.109321 / 31.235304 / 66.607344 | 8.0533 |

DCLM local R is zero at 99.94706% of all V positions;positive-conditional mean R28 is1.25684%. Tulu values are 83.68529% and0.66156%. DCLM Q1/Q5 hit rates are0.19305%/0.04674%, but conditional R28 means are similar at approximately1.36888%/1.35675%. [Group conditional means](tables/group_conditional_means.csv) are post-execution arithmetic: existing group means divided by hit probability, with no cache reread, fitting or new test. Positive decoder norms and zero_R=1−anylow at every layer were verified;empty groups remain NA.

Final-layer rarity correlations: DCLM any/count/fraction0.006193/0.006193/0.006189,M_low0.006191,T0.325661;Tulu0.256699/0.257504/0.249807,M_low0.260185,T0.194053. The direction is not unique to the ratio R;these statistics still cannot causally allocate identity,format or context effects.

## 6. Variation,layer contrast,and migration

Every DCLM layer has 41/41 estimable V blocks,37 positive. Layer 28 equal-block mean0.007473564 has95% descriptive interval[0.004662572,0.010107547]. The paired layer 28−2 equal-block contrast is6.7059e−7,[4.3177e−7,9.3306e−7]. The tiny difference is not a strong layer mechanism or practical benefit even though this descriptive interval excludes zero.

Tulu has 227/256 estimable conversations,212 positive and29 NA at every layer. Layer 28 equal-conversation mean0.255917856 has interval[0.231403684,0.280123058]. Layer 28−2 difference0.002044106 has interval[−0.000280917,0.004935049]. Estimable/NA sets agree between2 and28 in both corpora/pools,verified by final_numeric_checks. These are block/conversation-mean intervals,not overall-rho intervals.

For the fixed old Tulu pool in DCLM,layer 2→28 position rho changes0.168926→0.157293;equal-ID rho−0.222496→−0.218740. Only25 old features remain local B1,Jaccard0.012607,with11 in U. Its all-V incidence33.8020% and final-layer mean share0.551933% do not make it a locally rare DCLM pool. Tulu local/old pools coincide;their equality is definitional consistency,not another replication.

Prespecified position checks compare<16 with≥16. DCLM final-layer rho is approximately0.010671/0.006137;Tulu0.277395/0.255251. Tulu uses answer position while DCLM uses input-context position;these are different labels and cannot be pooled. This does not control identity,source or full formatting.

## 7. Figures and permitted readings

![All-layer correlations](figures/figure1_layer_correlations.png)

Figure1 uses layer_metrics and block_stability. Upper panels compare overall position/ID rho;lower panels show equal-block/conversation means with descriptive intervals. The weak DCLM position direction and negative ID direction persist across layers. This is not independent-layer confirmation,and lower intervals cannot be attached to upper pooled rho.

![All-band final-layer shares](figures/figure2_r28_token_band.png)

Figure2 uses groups and retains unknown/empty groups. B4 supplies most amplitude while B1's absolute share remains small;this does not show rare content dominating an input. Empty groups remain NA.

![Hits,amplitude,and denominator](figures/figure3_binary_contribution.png)

Figure3 uses layer_metrics,binary_metrics and groups. It separates share,absolute low-band amplitude,total amplitude and binary hits. DCLM's lowest-pool associations are all tiny while the denominator has a larger correlation. It does not identify causes or classification utility. Feature-weighted results are separately sourced and are not the same estimand as this position plot.

![Feature frequency versus hit-token rarity](figures/figure4_feature_level_correspondence.png)

Figure 4 uses feature_token_correspondence and feature_correspondence_summary under the fixed ≥20 known-token review-hit criterion. The horizontal axis is reference feature rarity and the vertical axis mean current-token rarity on its hits. Each point is a feature; most are outside the lowest band. DCLM rho is 0.339147 and Tulu 0.119556. This does not establish position reliability or separately validate the lowest 314 features.

## 8. Engineering completion,limitations,and unmeasured evidence

Core execution succeeded without a failure receipt. It read 339 existing chunks containing V rows,checked their SHA256,and read8,531,540,850 bytes. V has1,336,496,568 nonzero events;all 16384 marginals match phase1. A read-only audit separately checked all 640 original chunk bindings/continuity,indices,D/V counts and small source identities. Independent direct-sum checks covered 3 positions,not all rows. Tulu position-wise R/rho reproduction passed.

Core elapsed time 314.8126s;peak recorded process RSS 4.1574GiB;no GPU,inference or training. This is neither total delivery elapsed time nor CPU-core seconds;RSS is not whole-machine peak. Ten core tables plus three derived/definition/qualification tables (13 total) were saved. The8→10 correction changed metadata only,not frozen code or core metrics.

Audit status is PASS_WITH_LIMITATIONS. The guard periodically checks RSS/time rather than enforcing a hard limit during operations;the recorded disk cap has no frozen-code check;exception unwinding may wait for submitted thread tasks;DCLM has no resumable partial checkpoint;writes are non-atomic. Raw DCLM bin and large checkpoint were not rehashed by this audit;recorded identities,current size/mtime and small indices were checked. Tulu CSR was not independently reread/rehashed by the audit;existing bindings and current position-wise final-layer reproduction provide evidence. These limitations remain explicit;the actual successful run used resources far below budget.

Not measured:independent-original-document validation,classification precision/recall,semantic ground truth,causal interventions,learning loss,expert utility,other models or independent single-layer encoders. U remains inside the full denominator,but no separate U amplitude table or grouped amplitude quantiles were output. Conditional means are arithmetic decompositions only.

## 9. Round record,interpretation,and one next question

The 2026-10-19 round tested sample/layer robustness of existing H1 with the same frozen model/dictionary,reference-defined pools and three weighting units,on same-bin D/V plus exposed Tulu. The observations above separate a feature-level association from reliable low-pool identification of rare tokens. DCLM does not reproduce Tulu's position association magnitude or weighting-invariant direction;its feature-level positive direction remains. Human scientific verdict is Unknown;old Anchor/Focus stay unchanged.

**One AI-suggested question:does the feature-level association persist with original-document-separated data after accounting for format,source and position?** Stop after this delivery. The researcher chooses activation,controls and resources;no automatic training or extra run follows.

## 10. Artifact ownership and reproduction entry

Research owns bilingual Summary/Detailed,protocol/audit,Chinese one-page note,13 small source tables and static figures. E owns code/analyze.py,code/plot.py,provenance/frozen_execution.json,source_identity.json,checks.json,code_audit.json,final_numeric_checks.json,completion.json and logs. Section 2 gives frozen code identity;source_identity/code_audit bind input manifests/checkpoint/norm. code_audit.small_table_output_consistency binds core table hashes/counts. code/finish_checks.py generates the conditional table, with scope in final_numeric_checks. feature_memberships.csv exports frozen groups for all 16,384 features in each corpus (32,768 rows); feature_level_support.csv joins existing feature/support definitions for qualification counts only. Neither requires cache rereads or a new test.

Core row counts:feature_token_correspondence32768;feature_correspondence_summary4;members10;migration2;layer_metrics56;binary_metrics4;groups840;block_correlations8316;block_stability56;diagnostics20. Full position payloads remain execution-side. Figure sources/formats/hashes belong to figure_manifest;the delivery manifest binds final artifacts.

Job submission IDs,training checkpoints,optimizer and external synchronization are NOT APPLICABLE. Reproduction entrypoints do not authorize rerunning this completed analysis;subsequent inspection reads existing results.
