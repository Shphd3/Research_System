派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/detailed.md`。
[精确原始文件](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/detailed.md)；研究修改仍回到原件。

---

# R17_D1 detailed execution and evidence

[Summary](summary.md) · [Protocol](protocol.md) · [Applied corrections](corrections.md) · [Full Chinese Detailed](detailed_cn.md)

## Design and inference boundary

The original four positive hypotheses are retained. The user explicitly requested a combined factual and AI-interpretation delivery, so execution and bounded assessment are completed together. Scientific acceptance, mechanism attribution, question closure and next decision remain researcher-owned Unknown. All probes are additional linear readouts, not evidence of native causal use.

## Objects and native adapters

Official Qwen3-0.6B Base has28blocks/width1024. ATTN is block27 self_attn.o_proj output before residual addition; MLPIN is actual mlp pre-hook after post_attention_layernorm. Each30000-member SAE uses FP32 linear→ReLU→Top32, no input unit normalization or decoder-bias subtraction. Preserve h, own reconstruction bias+zD and residual h−reconstruction. u_i=z_i times own decoder norm. A22 jointly encodes odd residual-post blocks1..27 using frozen FP64 centering/RMS then FP32 encoding and saved threshold0.051281172782182693 on ReLU×joint decoder norms; target reconstruction is raw block27. No equal-ID alignment.

Training counters differ: A17 raw1000980480/prediction-valid1000002960/SAEeligible999025471; E16 raw1000001536 with no exact cumulative postfilter count; A22 total999997440 positions including4096000A21 positions. Historical metadata Unknown is not this run's loading status: all3 were loaded and native smoke-tested.

## Data, freeze and fitting

Old384 rows span48families,24/12/12family and6/3/3theorem splits. Correct object/certificate/n binding while changing only answer vs neutral sentence. Old heldout is diagnostic_old. Fresh288main comprises192fine=24families×2labels×2cueconditions×2paraphrases, plus48coarse and48nonmatrix. n52–75 is paired. Theorems include6old-discovery,3old-development,3unseen groups; new instance is not a new theorem. Appendix48 varies only array frame or logical negation on the first family per theorem, no-answer/p0. Frozen models score it without refit.

Natural600R15documents/76800positions use300/150/150document splits,128positions/document. Own frequencies/bounds fit38400discovery positions; require20positive positions/5documents; count-tercile ties stay intact. This reuses previously studied data and may overlap A22 source training.

C up to8 ranks common minimum standardized contrasts over matrix conditions; F up to8 ranks discovery fine-label differences; A=F−C. Track actual support transitions, not only continuous changes. H2 b=(z>0), r=||u_C||2, q=u/(r+epsilon), compares[b,r] versus[q,b,r] and same-support pairs. These are covariate controls, not exact magnitude interventions. H3 uses equalK16/12/8 budgets and requires both J-vs-H and J-vs-M gains. H4 searches at most8high atoms/20pairs/80states, discovery positive-q75 bins and min30positions/10documents, marginals≥.01/joint≤.005. Primary first configuration and≤9exploratory configurations are fixed before fresh access.

L2 logistic CPU lbfgs5000,class balanced,C=.01,.1,1,10,100. Fit scaler/discovery only, choose development meanLL, lowerC tie. Original mixed/mixed first diagnoses; all corrected H1-H4 use mixed olddiscovery training and no-answer olddevelopment C selection fixed before fresh. Core continuous/binary/high16 retain all3schemes. Old measurements enabled one description selection andK16/32/64+20matched seeds for both SAEs; CC gate did not enable. No temperature fitting or nonlinear test-time optimization. Random mean-arm loss is mean of individual-model losses, not loss of mean probability.

Family bootstrap2000 plus theorem-group sensitivity, seed20261103; within-family conditions resample together. Comparison multiplicities H1=5,H2=1,H3=2,H4primary=2; direct same-index between-site first5contrasts usem5. Conditional cue/paraphrase strata are diagnostic, not independent new confirmations. Only12theorem groups limit precision. Full per-item probabilities/margins/loss/Brier and five-bin reliability counts, coefficients/scalers are saved.

## Behavior, position and numeric quality

Native complete candidates “ invertible.”/“ singular.” have3/2tokens; score summed logprob in2frozen formats without length/prior correction; no-content priors saved. Plotted probabilities normalize only these two complete candidates. Continuation direct-answer controls2/2; question1/2. Fresh no-answer continuation73/96,question50/96. Question-prefix final-token linear fits use only original oldtrain/dev and frozen members: original h ATTN79/96LL0.5071/MLPIN76/96LL0.5203; reconstruction60/96LL0.6541 and59/96LL0.7443; selected sets48/96LL0.7467 and54/96LL0.6798. This changes context and position together, not pure location causality.

One2x5090spot job pt-viic7g4p created02:11:23UTC/completed02:30:02UTC. An earlier SDK rejection created no job; D1-only compatibility proxy removes unsupported service_time_expression. Existing torch2.8cu128 runtime reused, no installation, no LM/dictionary gradients. Fixed shapes panel8x128,natural2x512,precision8x64,native4x192; no truncation. No-op and fixed-shape single/batch h differences0; reconstruction ledger<1e-6. Primary FP32 chosen before fresh, storedBF16 promotion does not recover lost training precision.

Precision24old: relative hL2 .01737/.01434/.01402 and zL2 .06368/.03652/.05196 for ATTN/MLPIN/CC; support flips36/32/147. Fixed continuous probes0class flips but maxprob shifts.199/.312/.272; binary MLPIN2/24 andCC1/24class flips. OldBF16reference is separate from consistentFP32 D1 data/frequencies/probes. Source/scaler/replay implementation repairs and failed-attempt logs remain documented.

## H4 source, annotation and missing evidence

All600full source documents recovered with600/600exactSHA after correcting initial erroneous1-based source_line to0-based (failed payload retained). Automatic full-document labels544non_target/52undetermined/4coarse_unknown, no fine. These are not recall-certified absence claims. Current-agent text review: old49=39non_target+10unknown; ATTN6allnon_target; MLPIN40=39non_target+1unknown. These are not independent human annotations. Known20controls improve9→20correct afterv4repair; not natural-recall estimation.

Relabel7roots including originalCC copy and3before snapshots; pre_v4 copies retained. Fine labels require visible prefix certificate and single-object scope; future full text never supplies current labels. Unknown/coarse unknown not counted as semantic negatives in determinate-pair diagnostics. ATTN validation11positions/6documents fails support; MLPIN75/37 has rarity upper.005156>.005. Natural matching has0ATTN/37MLPINpairs. Both frozen configuration-matching pools fail20/20; additive/configuration readouts still fit. OriginalCC10/208pairs retained, correctedCC10/228pairs separate.

One bounded100000source-line search gives48unique natural windows≤512tokens, starting128before first fine term; one final visible position/document. Content search tags are not labels. v4 yields2invertible/0singular/43unknown/2coarse/1non_target, below10fine documents/class. Save every event/rawz and stop enrichment. Never pool enrichment with natural frequency baseline, never rename nonmatrix topics as newly discovered concepts. v4 changed only2label metadata fields; reconstructingv3 reproduces encoded-inputSHA exactly, token IDs unchanged.

## Figures and artifacts

Five figures: full-text own-coordinate heatmaps; discovery-frozen pair scatter with paraphrase arrows; no-answer representation LL plus correct counts andNMSE; fixedcase probe/native confidence in separate columns; actualhookdiagram. See Chinese Detailed for captions and casebook for full token-level data. Zero-overlap and high-confidence failures are preserved. Tables separate original old48, corrected old48 and fresh192; different-N differences do not causally allocate repairs.

[Coverage](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/tables/coverage_ledger.csv) records every actual module and measured inapplicability, including failed configuration controls. [Data guide](dataset_guide.md) maps payloads. [Verification](verification.md) records independent numerical/lineage checks. Identification/statistics/implementation audits are executionevidence/audit_*.md. Eight SAE route computations and four correctedCC routes completed; scientific acceptance Unknown. No commit/push/publication or indefinite monitor.


### Final localization: configuration response, valid controls and visible context

MLPIN primary H4 configuration11234strong+47strong never occurs in any old-discovery/development/diagnostic or fresh fine-label row. All20candidate controls have exactly the same semantic-panel indicator and fail IDENTICAL_INDICATOR_FAILED. ATTN has no admissible distance-matched pool (20MATCH_FAILED); its no-answer primary event occurs in2/48invertible and2/48singular rows. Thus current-configuration response, distinguishable controls and natural target coverage are separate measured bottlenecks. A zero gain is not evidence of no interaction mechanism, and configurations are not reselected.

Description-selection is not uniformly unchanged: ATTN K16/32/64 no-answer LL=.6840/.6716/.6854; K32 improves over original union.7064 and classifies58/96, but matched-random gain.02203 has theorem simultaneous interval[−.00539,.04949]. ATTN K64 matching succeeds0/20, so no matched gain is estimated; K16/32 each20/20. MLPIN each20/20 has LL=.8213/.8245/.7433, not better than original union.7034. These do not establish stable or monotonic organization.

“No-answer” in the question-position diagnostic refers to the body withholding the correct answer. The appended question contains both option words but does not reveal the correct class. This is not a replication in a prefix entirely without option words.

[H4event counts](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/tables/H4_semantic_panel_event_counts.csv) · [Kmatching status](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/tables/optional_K_matching_status.csv) · [Kconditional effects](../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/tables/optional_K_conditioned_effects.csv). Read-only frozen-output diagnostics; no forward, reselection, fit or search.
