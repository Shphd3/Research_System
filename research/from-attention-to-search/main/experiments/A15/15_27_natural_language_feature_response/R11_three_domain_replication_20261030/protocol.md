# Protocol: R11 three-domain replication with a fixed CrossCoder

## 0. Approval Snapshot

Document status: **DRAFT_NOT_EXECUTABLE**. The researcher confirmed planning an extension from math/biology to math/biology/physics with the existing model/dictionary. Exact sample counts, operational margins and resource ceilings below are **AI_PROPOSAL**, not accepted results or run authorization. Execution scope approved: local design writing and read-only checks only. New forwards/training: **0/0**. Scientific acceptance/closure: Unknown. Role: robustness check and operationalization audit, not method training.

Purpose: decide whether the frequency/use/spectral description persists in independent documents and a third domain, or was conditional on the original domain pair, sources, format or finite coverage. [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_04_domain_member_atlas_anchor.md) owns the question. The existing [Focus](../../../../focus/focus_natural_language_feature_response.md) retains R10 history; its appended R11 section records this proposed continuation without scientific state promotion.

One experiment, three steps: (1) build independent three-domain documents and test all old16; (2) freeze symmetric full-dictionary discovery sets; (3) evaluate untouched confirmation and three registered descriptive hypotheses. Pass supports a bounded three-domain account; a contrary primary result narrows the relevant intuition; missing support remains insufficient. No training, routing, activation intervention, new dictionary/model, distance study or external sealed TEST.

## 1. Terminology / Definitions

A document is one original article/book/question family, not a token or paraphrase. A platform family is a website/publisher style group; a document family includes alternate URLs, answers, book chapters and near paraphrases from the same original work. Use one excerpt per document family in the entire study. Discovery D selects members. Development V checks the fixed analysis and stability without changing members. Confirmation H is untouched by feature-response inspection until the scientific configuration and lists are hashed. Independence means independence from this analysis's selection, not verified absence from LM pretraining.

Native activation means the existing shared z after its original gate, with z>0; frequency is a position proportion, not strength. Document response is the mean z over160positions including zeros. Spectral mass means squared projection of a unit decoder, not activation energy or knowledge quantity. Old16 denotes the previously described all-cached-strict7math/9biology members; its original120documents are exposed history.

## 2. Anchor Alignment

The established boundary is descriptive: parent R10 has433math/527biology discriminators, generally frequent reference use; narrower near/strict use sets shift lower; average squared spectral distributions overlap substantially, without exceeding finer matched background. Shared-token response is heterogeneous. These do not establish semantic exclusivity or method utility. R11 tests stability of this account, including physics as a challenge to the old "math-only" label. The unchanged old16 geometry/reference rates alone cannot count as new replication: their decoder and DCLM readouts are constants.

## 3. Tested Hypothesis

F1: three-domain dominant members have a larger high-reference-frequency share than the support-qualified dictionary pool. F2: near-single-domain members have a lower median reference rate than the dominant members within each domain; strict-zero subsets are a separately labeled sensitivity. F3: the three dominant groups have substantial common-spectrum projection overlap and no practically large additional separation relative to occurrence/support/size-matched dictionary backgrounds.

The stronger phrase "domain-exclusive knowledge" is not tested as established truth. Old16 counterexamples in physics are allowed to revise the domain label. A shared-ID conditional response can be associated with preceding context without identifying semantics or causal computation.

## 4. Rival Explanations

Rivals: source/publisher and genre signatures; equations/markup and specialist vocabulary; reference-frequency/support selection effects; group-size smoothing of average projections; zero observations caused by small coverage; using exposed H to select a favorable list. Shared mathematical expressions could make math-biased members active in physics. Record formula/format strata before any model outputs, report source-transfer H separately, and retain every failure/counterexample. No surface token count alone proves preference.

## 5. Data Construction And Provenance

### 5.1 Proposed counts and splits

All450study documents are NEW relative to R04/R10 and their source-document families. Each domain has150: D60,V30,H60. Each excerpt has192real tokenizer positions, with no added BOS/chat template/domain label; analyze indices32..191(160positions).

| Split | Math docs | Biology docs | Physics docs | Total docs | Analysis positions |
|---|---:|---:|---:|---:|---:|
| D |60|60|60|180|28,800|
| V |30|30|30|90|14,400|
| H |60|60|60|180|28,800|
| Total |150|150|150|450|72,000|

Per domain H comprises H_same30(new document families on development-source platforms) and H_newsource30(platform/publisher families absent from D/V and the old120). Each is reported separately; do not pool away a source-transfer reversal. There must be at least four platform families in each H stratum/domain; no platform exceeds25%of a split/domain, rounded down. Platform membership must cover≥2domains, avoiding platforms that uniquely encode a label. If the exact sampling constraints cannot be filled, report the failed quota before execution; do not relax after seeing activations.

Use six predeclared topics/domain, with10D/5V/10H documents/topic. Suggested topic grid: math algebra,geometry/topology,analysis,probability/statistics,number theory,discrete/logic; biology cell,molecular/genetics,physiology/neuroscience,ecology/evolution,microbiology/immunity,organismal biology; physics mechanics,electromagnetism,thermodynamics/statistical physics,waves/optics,quantum physics,materials/solid state. These are sampling strata, not feature labels. Mixed-content documents stay if the text's main explanatory object assigns a domain; mark interdisciplinary content rather than filtering by model response.

Match genre across domains: D45expository/15question-answer; V22/8; H45/15. H_same22/8andH_newsource23/7sum to45/15. This preserves the old study's approximate75/25genre mix. Formula presence/density, markup, citation and heading flags are recorded from input text before activation. Do not force biology to have an unrepresentative formula fraction; use common-support strata for conditional comparisons and report unmatched fractions.

### 5.2 Traceability, deduplication and independent H

Store URL/WARC or archive line,canonical document/platform family,language,domain,topic,genre,raw SHA,character span,cleaned SHA,token IDs and split. English only, unmodified contiguous source excerpts. Reuse the R04 extraction principle: skip leading navigation with recorded deterministic rules, retain actual prose/formulas/punctuation, take192tokens; no hand editing to create responsive text. Exclude short/mixed-language/label-ambiguous fragments before outputs. Activation-blind label proposals require independent content review; unresolved labels stay excluded with a reason, not silently relabeled.

Exact and token5-shingle Jaccard≥.8duplicates are grouped or excluded across all splits and against old120plus independent-reference documents; canonical article/book/QA grouping overrides a low shingle overlap. One excerpt/family and a source-family split prevent token leakage. Sort otherwise eligible document-family IDs with SHA256(seed:ID), then solve declared topic/genre/platform quotas before inference. Seed20261030. D/V/H manifest and H record IDs/hash are saved before any response. H text may receive response-blind quality review, but no H z/ranking is available during selection. Existing sealed external benchmarks remain untouched.

The exact450source manifest is **NOT_BUILT**, not a saved dataset. Catalog metadata contains possible physics-bearing archives, but their content has not been qualified as this panel. Dataset construction/review/registration must precede any future forward. Pretraining contamination is Unknown, and no model-unseen-data claim is permitted.

### 5.3 Why this size

Sixty independent H documents/domain makes zero observed active documents a pointwise one-sided95%binomial upper bound1−.05^(1/60)=4.87%, under an IID-document assumption. This is not simultaneous protection over16members/three domains or proof of zero probability. The size supplies source/topic coverage and a readable bound, not a completed power analysis for AUC or subgroup effects. Report intervals and insufficient precision rather than change thresholds or add samples after H inspection.

## 6. Learning Task And Permitted Supervision

There is no learned task/readout. Domain/content labels define document strata and comparisons only. Allowed: raw causal prefixes, frozen activations, input metadata for sampling/matching, D labels for selection. Forbidden: feeding domain/source labels to the LM, choosing excerpts from z, V/H member replacement, tuning the gate, treating post-target text as an instantaneous cause, or fitting a classifier/router. Later full-word spellings are separately named posthoc readability aids.

## 7. Model / Architecture And Frozen Variants

Reuse the exact Qwen3-0.6B-Base weights used by the native A22 path(expected model SHAcd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba)and unchanged tokenizer. A22 checkpoint SHA09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628;16,384shared coordinates; joint inputs from zero-index blocks1,3,...27,1024dimensions,original TRAIN centered-RMS statistics. Preserve original BF16 encoder/gate path and saved threshold0.051281172782182693; threshold is applied in its native norm-weighted expression, not as a substituted threshold directly on z. No single-layer encoder approximation.

LM inference is eval/no-grad,BF16,SDPA,fixed1×256padded positions with a192-position attention mask. CC native compute pads to1024positions exactly as the old loader. Capture h27and z in the SAME forward. Unit decoder geometry uses final block27residual-post before final norm in the same coordinates. No new normalizer is fitted. Buffers/parameters remain unchanged. The old dual-readout loader needs a bounded CC-only adapter: do not accidentally load/measure E16. Legacy replay must qualify this adaptation before use.

Primary assets and current read-access receipts are in asset_inputs.json/provenance. Current checks establish registered access only; full runtime weight identity and numerical replay remain NOT RUN. New data/z/h assets will be registered only after actual creation, never as fictitious available outputs.

## 8. Training Objective And Optimization

None. No optimizer,backprop,parameter update,checkpoint selection or new LM/SAE/CrossCoder training. The new three-domain PCA below is unsupervised covariance estimation, not a model/dictionary replacement, and is only a separately labeled robustness analysis.

## 9. Conditions, Seeds, And Checkpoints

One fixed checkpoint pair; three domain conditions; D/V/H and Hsource strata as above. Data seed20261030,bootstrap seed20261031,matched-dictionary seed20261032. Primary inference budget450study sequences plus≤12engineering checks,**cap462including retries/failures**. No unused historical budget is inherited. Proposed checks:4/domain,with two old exact replays each in math/biology plus8disjoint pilot examples; pilots never join450or selection.

Study real input tokens86,400;measured positions72,000;actual LM padding115,200positions. Including12checks gives at most118,272LMpositions at256and473,088CCpadded positions at1024. These are distinct counters, not valid-token training progress. Existing inference resource only,max1GPU,no new resource request. Device profile/ETA are Unknown pending engineering qualification; candidate ceiling2GPU-hours and12CPU-hours for offline statistics, both AI_PROPOSAL. No automatic scale-up or extra domain/data on a ceiling failure.

## 10. Primary Metric And Frozen Analysis Plan

### 10.1 Original16: transfer without reselection

Freeze math[16195,15426,8693,12030,5234,12960,9638]andbiology[2635,6270,13691,10395,7238,12630,11516,15401,11960],with source hash in legacy16_frozen.json. Every old ID is measured in all three D/V/H sets; primary transfer results use the NEW H only. Report each domain's active documents/60,positive positions/9,600,zero-inclusive meanz,old-oriented pairwise AUC and source/topic/format breakdowns. Report pointwise document-cluster-bootstrap95%AUC intervals and exact binomial active-document intervals; old16multiple-member tables are descriptive, not an FDR-controlled semantic discovery list.

Retention of observed strictness requires≥5preferred-domain active H documents and zero active H documents in BOTH other domains; evaluate H_same/H_newsource separately without redefining membership. Any physics positive event is a literal counterexample to "zero physics events in this panel" and remains in the table. A recurrent cross-domain-use tag requires≥5physics H documents across≥2platform families. One to four positives are local counterexamples with insufficient recurrent-use support; never erase them. Preferred support<5or no relevant token/context opportunity is insufficient, not identity coding. The prespecified surface-opportunity guard for a zero-response opponent is that at least ONE of this member's original native-positive Top3exact tokenIDs appears in≥5opponent H documents in the analysis window;freeze those IDs from the previous table before new data. This is only a surface-coverage guard,not proof of equivalent senses/contexts;positive counterexamples are always kept even if that guard fails. Physics activity alone does not refute math-vs-biology preference; report both distinctions separately. Do not remove transferred IDs from the original16.

### 10.2 Symmetric full-dictionary three-domain screening

For each feature f and discovery document i,let r_if=(1/160)sum_(t=32..191)z_itf,including zeros. For domain d versus e, A_f(d,e) is the fraction of all60×60document comparisons with r_d>r_e,plus half the ties. This is a stable response ordering,not every nonlinear discriminator.

The shared eligibility pool is all dictionary members active in≥5D documents in at least one of the three domains. For a candidate bias d,require≥5active D documents IN d and define **S_f(d)=min_(e≠d)A_f(d,e)**. Freeze all S≥.75as the d-dominant main group,rank descendingSthenascendingID. Thus a member withA(math,bio)=.95butA(math,physics)=.55is not a three-domain math-dominant member. The groups are mutually exclusive by score direction,which is not spatial-separation evidence.

Within each frozen group,strict-three-domain requires zero D activations in both other domains. Near-three-domain requires≤3/60active D documents in EACH other domain and≥95%of all three-domain positive positions in d. Main=.75; sensitivities.70/.80,near shares.90/.99andTop16/64/128retain the same support gate. No refilling. Keep all pairwise AUCs; separately show members supported in math AND physics(≥5D docs each)that each outrank biology byA≥.75. This secondary overlap can coexist with a dominant group and must not change primary denominators.

New memberships/ranks,reference cut points,token categories and plotting scripts are hashed after D/Vand before H response release. H evaluates frozen direction/S/support with document-level intervals; no replacement or "reliableTop128" label. New strict/near H retention is a separate subset:preferred support≥5,strict has0opponent documents,near has≤3/60documents in EACH opponent and≥95%preferred positive positions;smaller source strata report their actual denominator and floor(.05*n)cap,not the wider whole-Hcount. V is diagnostic only,never an alternative selection split.

### 10.3 Three predeclared aggregate contrasts

Frequency uses the SAME independent DCLM hit counts/65,536positions,min20hits,original lower-inclusive cuts.002593994140625/.0134429931640625;log cuts.0045172553628813825/.06686505701697326are sensitivity only. Report insufficient-reference exclusions in every denominator; never call them low. F1is the equal-domain mean of(main classified high share−eligible classified high share);predicted>0. F2is the equal-domain mean log10(median valid-reference rate_near/median rate_main);predicted<0. Strict-zero composition is separately reported because its count shrinks mechanically with added documents/domains. Require≥5frequency-classifiable members AND≥80%reference-classification coverage in each relevant group/domain and in the eligible pool for a three-domain aggregate judgment;otherwise mark aggregate insufficient and retain all partial values. Main intervals condition on the fixed DCLM reference counts and sampled platforms;they do not estimate reference-corpus or all-platform sampling uncertainty.

Geometry uses the frozen R10common1024-PCbasis as the primary transfer reference. Unit decoder squared projections sum1;member-equal mean per group;pairwise overlapO_de=sum_jmin(Q_dj,Q_ej);64-PCcoarsening andPC1/PC2–64split are separate. Matched reference uses the new eligible pool INCLUDING selected IDs,half-octave DCLMhit bins×5-document bins of total and maximum-domain Dsupport,exact per-stratum/group sizes,disjoint groups within each draw,1,000draws. Inclusive draws are a conditional dictionary reference,not an independent null;report selected fraction/stratum limitations.

For each of the three pairs letm_de be its matched-reference median. Proposed operational geometry score **G=min over all pairs of{O_de−.80, O_de−m_de+.05}**. Thus support requires all pairs both≥.80and no more than.05below matched background;these are declared practical margins,not semantic constants. Show rawO,m,intervals,not only a binary tag. Zero-norm members are retained as invalid geometry;empty/unmatchable groups are insufficient.

For F1,F2,G,resample D document families within domain/topic/genre3,000times,rerun eligibility/selection without changing gates,and recompute the quantities. For G,redraw100matched backgrounds per bootstrap to estimate its current-size median;report MC error,refine to200/400(up to400)only if a prespecified split-run median difference>.005,on a fixed10%bootstrap audit subset. No post-hoc scientific margin changes. Report three two-sided98.333%percentile intervals(quantiles1/120,119/120),a Bonferroni family for the three planned aggregate contrasts. Domain/pair/member extra intervals are pointwise and labeled descriptive. These intervals reflect selection variation in the sampled domain population,not another independent heldout proof. If>5%replicates have undefined requisite groups or the resource/MC criterion fails,the corresponding aggregate is insufficient,not an interval over only favorable surviving replicates.

## 11. Secondary Metrics And Guards

Fit ONE three-domain discovery covariance as a separately labeled robustness basis:180documents×160positions=28,800real h27vectors,one common mean,equal domains/documents/positions;no domain-wise demeaning,no per-domain PC fits. Freeze before H. Report rank/eigenvalues/normalization/full projection sums and do not pool new-basis overlap with old R10numbers. Bootstrap selection in this secondary basis is conditional on the fitted basis;it does not include PCA-estimation uncertainty. Cross-member absolute cosine and actual decoder-subspace rank/overlap are appendices to prevent function/direction claims from squared spectral overlap.

Nativez>0token statistics use all frozen members with positive H support;no high threshold silently substituted. Save per-member exactIDs,counts,document coverage,all available-token opportunities,and member-equal fractions versus all-position and document-exposure-matched backgrounds. Input token classes freeze on D:shared-all3(≥5Ddocs EACH),shared-exactly2(≥5each in two,0third),single-domain(≥5one,0both others),remaining/insufficient;H-unseen IDs retain a separate unseen flag. Within-panel token-frequency cutpoints and per-IDbins come from D only,ties unsplit;unseenH is missing frequency support,not true zero probability or automatically rare. Primary coverage/denominators and conditional-classified views are both shown. Old all120token classes remain history,not relabeled confirmation truth.

Optional high-response sensitivity:old16uses its original frozen R10p90;new groups use positive-Dp90only when≥20Dpositives,Hcomposition requires≥5events/2docs.No member replacement.

Same-ID natural-context check is offline within H:predeclared mainID279` the`;pairwise compare domains,exacttarget/previousID,genre,40-position-bin,boundary and formula-present flag;second level additionally source platform. Maximize independent document pairs then matched positions,no activation in matching,no document reuse across pairs per token/level. Mean within document pair,then equal pairs;≥10pairs for primary descriptive context interval,5–9exploratory,<5insufficient. Save coverage lost,multiple sources,all fixed members including zeros. Prefix-only cue labels are activation-blind proposals until reviewed;future noun phrases remain posthoc. No natural-context result identifies a pure semantic/causal effect.

## 12. Known Good / Known Bad / Known Confusing Cases

Good metric identities:equal response arrays→A=.5,complete ordering→1,reversal→0;Sis its weaker pair;full squared projection sum1;coarsening cannot decrease overlap. Known bad:token-wise pseudo-document bootstrap,average one-vs-rest hiding an undistinguished opponent,selecting strict IDs using H,forcing reference-insufficient into low,discarding old16physics activations. Confusing:f2635often punctuation andf15401cell-related surfaces;both remain measured without semantic labels. An unchanged old16direction plot is an identity check,not a third-domain empirical discovery.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal / operation | Acceptance / failure | Output / handoff |
|---|---|---|---|
|0,plan/current|verify owners/assets and draft|read-access checks only;no forward|this draft and current access receipt|
|1,data,after authorization|curate450,quarantine oldfamilies,freeze split/metadata|all quotas/traceability/dedup/domain review pass;else stop before inference|registered dataset manifest,Hresponse lock|
|2,engineering,after authorization|≤12checks,exact legacy native replay,hook/normalizer/gate/buffer checks|default native replay exact;hardware numerical mismatch stops for a recorded numerical audit,never automatic gate/tolerance change|runtime and invocation ledger|
|3,D/V,after authorization|one forward/doc,saveall z and h27;freeze new lists/bases/scripts|source/gate/shape checks pass;noVreselection|scientific freeze hashes|
|4,H,after authorization|verify freeze hashes,process allH once,compute fixed results|incomplete coverage saved;never replace members or access anotherH|all-member/old16/heldout tables|
|5,offline|bootstrap,matching,render,audit,write bilingual factual report|identities/source/denominator checks;missing tests retained|five clear figure groups and raw stats,then stop|

## 14. Algorithm, Output, And Provenance Contract

Canonical owner is this R11directory. Planned execution-only output root `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R11_three_domain_replication_20261030` is NOT a currently completed run. Preserve old results. Save document manifests,label/duplicate/source audits,all16384document responses and support,sparsez and h27,new basis,old16and all lists/ranks,reference counts,token tables/prefixes/bootstrap/background IDs,figure CSVs,run/config/code/checkpoint/source hashes,failed attempts and stop reasons. Register actually produced dataset/representations with their parentIDs before delivery;never register planned files as available.

Five main groups:(1)old16×3domains active-document matrix;(2)pooled/per-domain feature-frequency composition;(3)common-spectrum means/PC1split and overlaps vsmatched;(4)native token types/positions/frequency with input backgrounds;(5)same-ID matched context with coverage. Large member tables/cosine/subspace/sensitivity plots stay appendices. Main figures use clear axes and few words,not dozens of panels. Summary results remain NOT RUN until measured;no hypothetical positive conclusion.

## 15. Success / Failure / Insufficient Evidence

| Registered item | Support | Contradiction / revision | Insufficient |
|---|---|---|---|
|F1frequent discriminators|adjusted interval lower>0andall domain pointcontrasts≥0|upper<0opposes overall trend;one supported domain reversal narrows a universal claim|crosses0,missing group/reference coverage|
|F2lower-frequency nearuse|adjusted upper<0andall domain logratios≤0|lower>0opposes shift;strict/near divergence is reported,not hidden|crosses0or<5validgroup members|
|F3overlap|adjustedGlower>0|Gupper<0fails at least one proposed overlap/background clause;show which|crosses0,unmatchable/invalidgeometry/MCfailure|
|old16strict labels|preferredHsupport≥5,opponents0,source coverage reported|any newopponent event breaks literal observedzero;≥5physicsdocs/≥2platforms supports recurrent reuse|lowpreferredsupport/no relevant opportunities|
|conditional context|matched response difference interval excludes0with adequatepair/source support|oppositeorformat-only/source-specific patterns narrow the interpretation|fewpairs,allzero,source-transfer loss|

Global "three-domain account replicated" requires F1–F3support AND heldout evidence that frozen domain rankings persist:in each group median H S>.5and≥50%of members have H S≥.75,reported separately inH_same/H_newsource.The50%guard is AI_PROPOSAL,not a reliability theorem;failureofsource-transfer guard narrows the account rather than permitting pooled rescue.Missing old16strictness does not veto frequency/geometry replication;its own label is revised.Any primary mixed/insufficient outcome stays mixed/insufficient;no forced all-or-nothing method recommendation.

## 16. What This Cannot Claim

Domain-exclusive knowledge,pure tokenidentity,identical decoder directions/functions,causal semantic processing,gradient alignment,learning interference,MoE/router benefit,training advantage,pretraining-unseen data,or utility from spectrum overlap.No intervention,newmodel/dictionarytrainingor methodprototype is in this round.The next permissible scientific decision is whether the bounded account merits a separately designed method comparison.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | Grounding / state |
|---|---|
|A,question/domain/model boundary|HUMAN_CONFIRMED for planning math/biology/physics with existing model/dictionary;hypotheses/margins proposed|
|B,data150/60-30-60/source split|AI_PROPOSAL;exact source manifest/domain review NOT_BUILT|
|C,measurement/no learned supervision|inherited native observable;new selection/conditional rules AI_PROPOSAL|
|D,model/hook/gate|VERIFIED_SOURCE metadata/loader and current access;runtime replay NOT RUN|
|E,optimization|NOT_APPLICABLE;no training is human-specified|
|F,statistics/decision margins|AI_PROPOSAL,including.75,.95,.80,.05andmajorityguard;no post-Htuning|
|G,budget/runtime/output|AI_PROPOSAL cap462,resourceprofile notyetqualified;execution NOT_AUTHORIZED|

Cross-block read-only audit:sample/token arithmetic and list identity PASS;new data/runtime/feature outcomes NOT RUN;source quotas and final choices await researcher review. Do not promote merely because the draft is complete. Planning authority does not authorize data forwarding. There is no automatic request for a separate approval at every stage; any later authorized scope is recorded once and honored within its limits.
