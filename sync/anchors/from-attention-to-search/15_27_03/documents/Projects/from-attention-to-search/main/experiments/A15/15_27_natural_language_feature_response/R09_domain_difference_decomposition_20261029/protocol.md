派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/protocol.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R09_domain_difference_decomposition_20261029/protocol.md)；研究修改仍回到原件。

---

# Protocol: R09 CrossCoder domain-difference decomposition

## 0. Approval Snapshot

Document status: APPROVED_FOR_CACHED_DECOMPOSITION; the distance-forward stage remains pending its own exact configuration and numerical preflight. Execution authorization is already present in the user's 2026-10-29 instruction to start the experiment and run branches in parallel. The root coordinator records the main-stage hash before its execution. The frequency/family branch was separately frozen in its own configuration before its run; this consolidated Protocol is not claimed to predate that branch. The authorized scope is frozen-representation analysis plus the bounded controlled-distance extraction described below, on existing resources, with no training or functional intervention.

Purpose: determine how much of a fixed-target math-minus-biology mean difference this dictionary reconstructs, which reproducible members compose it, and how their reference frequency, family variation and measured distance response relate. This is an exploratory operationalization/robustness analysis under [Anchor15_27_03](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_03_domain_difference_decomposition_anchor.md). It inherits the contextual-response question from the [parent Focus](../../../../focus/focus_natural_language_feature_response.md); the user's present child question controls R09 and does not reset the older Focus states. R07/R08 results remain unchanged.

Three steps: validate cached vectors, decoder and reference statistics; decompose the complete dictionary and evaluate discovery-fixed candidates with family/ending/distance controls; deliver all four main figure families, the requested supplements, full tables and an explanatory summary, then stop. A small, stable subset approaching all-member reconstruction supports a concentrated description. A distributed reconstruction, substantial residual or condition dependence limits it. Invalid interfaces, unstable denominators or inadequate family support yield insufficient evidence. No automatic architecture decision or scientific closure follows.

## 1. Terminology / Definitions

A member/feature is one of A22's16,384 fixed activation coordinates. Each text contributes one final-target1024-dimensional true vector and one shared16,384-dimensional activation vector. “Preference” is the sign of mean activation math minus biology. “Positive contribution” means a member vector points along the true math-minus-biology difference; a biology-preferring member may have positive contribution. “Individual” means a topic/text family within a domain. “Frequency” is the fraction of65,536 independent reference-token positions with native gated activation greater than zero, including every zero in the denominator.

The original heldout split has already been viewed in R07/R08. It is an exposed exploratory replication split, not newly untouched confirmation. Family-level intervals are pointwise uncertainty summaries; this round makes no multiplicity-controlled member-confirmation claim.

## 2. Anchor Alignment

The parent uncertainty is whether contextual differences have reproducible dictionary-coordinate descriptions. R07 established mean association; R08 showed that containing the center-difference direction does not imply that between-domain variation dominates total variation. R09 identifies the dictionary composition and reconstruction shortfall of that specific center difference. Whole-vector residuals separate dictionary inadequacy from apparent member coherence; ending/wording/family controls separate broad panel association from restricted responses.

## 3. Tested Hypothesis

The complete dictionary reconstructs some of the domain mean difference, and discovery-selected member changes recur across original heldout families. The concentration curve measures how many fixed members are needed to approach the whole-dictionary result; it does not assume that64 domain-exclusive members exist. All-member analyses remain valid when candidate gates return fewer members or none.

## 4. Rival Explanations

A: relatively few reproducible members compose the difference. B: many members compose it, with reinforcement/cancellation. C: candidates depend on endings, wording or individual families. D: the dictionary misses important difference, leaving substantial residual. High cosine alone cannot eliminate D. A frequency-group association cannot eliminate C. A controlled distance response does not prove functional necessity or establish natural-language generality.

## 5. Data Construction And Provenance

Reuse the exact384 R07/R08 records:48 family IDs, two domains, two wordings, two endings (`example`, `explanation`). Families are split24/12/12 into discovery/development/original-heldout. Discovery has192 total rows; one ending has96 rows,48 per domain. Original heldout has96 total rows; one ending has48 rows,24 per domain. Average wordings within family, then weight families equally. Resample matched family IDs jointly across domains, endings and wordings. Corresponding math and biology family IDs are constructed contrast units, not identical topics.

Main inputs are R08's registered `representation_a15_27_02_r08_fixed_target_layers_jointz_20261029`, actual384×14×1024 targets and384×16384 native shared z, the frozen A22 checkpoint, R07's independent natural-text PCA and R05's matched `reference_CC.npz`. Use the selected-ID current strict asset receipt plus exact paths/hashes in the execution manifest. Main analysis adds no texts or forwards. Distance copies preserve the original domain cores/wordings/endings but are separate controlled-length derived inputs; never overwrite or label them original384 records.

## 6. Learning Task And Permitted Supervision

No language model, dictionary, router or readout is trained. Domain labels, family IDs, wording IDs and ending IDs are permitted only for descriptive statistics, discovery selection and registered controls. Discovery selects candidates and signs; development and original heldout do not alter lists, cutoffs, bins, intervals or distances. No new PCA, clustering or semantic naming is allowed. The user's request for an explanatory conclusion authorizes bounded interpretation of observations; scientific acceptance remains the researcher's decision.

## 7. Model / Architecture And Frozen Variants

Qwen3-0.6B Base is frozen. The primary true interface is zero-based `model.layers[27]` output, residual-post before final normalization. A22 jointly encodes the fourteen odd zero-based block outputs1,3,...,27 with its original centering/RMS and native gate. No final-layer-only encoder is constructed. A22 checkpoint: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/runs/formal_14layer_batchtopk_a22/checkpoint_000999997440.pt`, SHA256 `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`.

The block27 restoration RMS is374.3495121024576. Use master FP32 decoder parameters, cast to FP64 for statistics. Compute contribution as activation difference times the block27 decoder vector times that RMS. The fixed training mean and decoder bias cancel. Independently compare summed FP64 contributions with differences of per-sample FP64 decoded means; record native BF16 decoding roundoff separately, without demanding bitwise equality between precisions. Preserve all original gate and batch conventions.

## 8. Training Objective And Optimization

Not applicable: zero trainable parameters, no objective, optimizer, gradients or checkpoint selection. Descriptive means, vector projections, resampling and controlled frozen-model inference are the only operations. Hashes and freeze checks establish parameter identity. No loss/optimizer telemetry is invented for closed-form statistics.

## 9. Conditions, Seeds, And Checkpoints

Primary conditions are `example` and `explanation` separately. Pooled endings are auxiliary only. Each has discovery, development and original-heldout values; the main figures show original heldout, with all splits retained in tables. Fixed top-k counts are1/4/8/16/32. Main family bootstrap:500 resamples, seed2026102910. Equal-size random subsets:1,000 per k, seed2026102912, sampled without replacement from all16,384 members. Family-variance bootstrap:500 resamples, seed2026102911.

The distance sweep uses actual cue-end-to-target distances16/32/64/96/144, final target position239 and total length240. Move the same neutral filler between the pre-cue and post-cue regions to match total token count and token multiset across distance conditions. For every original text and distance, compare the base construction and one token-length-matched unrelated edit. Maximum3,840 derived forwards plus2 R08 replay checks =3,842 attempted forwards. Full shared z is retained. Use the existing local MIG allocation; no new resource request. Exact filler, edit positions, checks and resource receipt are fixed in the distance configuration before inference.

## 10. Primary Metric And Frozen Analysis Plan

For each ending/split, compute equally weighted true mean difference \(\delta\), complete zero-inclusive activation differences \(\Delta z_j\), vectors \(c_j=s d_j\Delta z_j\), all-member sum \(\widehat\delta\), and residual \(r=\delta-\widehat\delta\). Report original norms, whole-vector relative residual and cosine. A true norm no greater than \(10^{-12}\) times mean sample-vector norm is a numerical undefined-ratio case, not a scientific rejection threshold. Retain raw quantities.

Directional shares are \(a_j=c_j^\top\delta/\|\delta\|^2\) and \(a_r=r^\top\delta/\|\delta\|^2\). Verify their sum equals1 within numerical tolerance. Keep negative values and totals above1. Compute500 paired-family bootstrap replicates of the entire mean-and-decomposition operation, retaining fixed candidate identities and order; report percentile95% intervals and valid replicate counts.

For each ending, select the32 largest strictly positive discovery shares, tie-break by ascending member ID; save both ordered lists and their union. If fewer than32 exist, preserve the shortfall. Original-heldout top-k curves use that ending's fixed order. Add contribution vectors before computing relative error. Plot the full dictionary as a reference and the1,000 equal-size random-set distribution. Never force monotonicity or select a best k.

A separate expanded list retains up to64 candidates per preferred domain. Discovery activation differences must have the same strict sign in all four ending×wording cells: positive for math preference, negative for biology preference. The mean of the two ending-specific, wording-averaged directional shares must be strictly positive; neither ending is required to be positive individually. Rank by that mean, descending, with member ID ties. Do not fill a quota by relaxing gates. These are discovery-consistent candidates, not exclusive semantics.

For each candidate save both domains' mean activation and activation occurrence, activation-difference sign, contribution in both endings and both wordings, all split values and family intervals. An exploratory “cross-condition recurring candidate” has the discovery sign in all four original-heldout cells and a95% family-bootstrap activation-difference interval excluding zero in each ending. Preserve every candidate that fails. This descriptive tag uses pointwise intervals and is not formal confirmation. All-member results and the original top32 lists are unaffected by this extra gate.

## 11. Secondary Metrics And Guards

**Ending response.** Within each domain, compute example-minus-explanation activation and vector differences for the same families/wordings. Show these beside candidate domain responses. Ending and domain associations may coexist; no binary exclusive classification is imposed.

**Frequency grouping.** Use native DCLM occurrence, N=65,536. At least20 hits defines reference-supported frequency, inherited from R05. Of16,384 members,13,357 are supported;3,027 are insufficiently supported, comprising749 zero-hit and2,278 with1–19 hits. Preserve zero and low-count subcategories and any missing values. Main supported-range log10 bins have cut points0.451725536288% and6.686505701697%, over0.030517578125%–98.974609375%; group counts5,808/6,917/632. The original equal-count convention uses cut points0.2593994140625% and1.34429931640625%, with ties not split. Linear equal-width sensitivity uses33.0118815104167% and65.9932454427083%, counts13,281/63/13. Exact inequality rules and legacy counts are stored in the frequency configuration. No boundary is fit to the math/biology panel.

For each frequency group sum all-member positive shares and negative shares separately, label their net, and show residual separately. Report total members and those active in the analyzed panel. Candidate-only totals are a second view. Frequency is occurrence, not average activation strength, reconstruction share, semantic specificity or range.

**Domain versus family.** At each ending/split/member, use equal domain/family/wording weights. Between-domain variance \(B=\Delta z^2/4\); family variance \(F=E_{d,f}(\mu_{df}-\mu_d)^2\); wording variance \(W=E(z-\mu_{df})^2\); verify \(T=B+F+W\). For \(T=0\), fractions areNA. Summarize member-normalized fractions with equal member weight by reference-frequency group; do not sum raw z variance across members as if dictionary parameterization were neutral. Provide continuous rates and valid/zero counts, as well as family-bootstrap uncertainty. These variance fractions are distinct from signed reconstruction contributions.

**Spectrum.** Use the R07 independent natural-text orthonormal PCA basis and its variance-rank ordering. Sixteen equal-width bands each contain64 PCs:1–64,...,961–1024. Plot \(\|P_b\delta\|^2/\|\delta\|^2\) and \(\|P_b\widehat\delta\|^2/\|\delta\|^2\). First sum member vectors, then project and square; memberwise squared energies are not additive because of cross terms. The reconstructed curve need not sum to1. No R08 basis is silently substituted.

**Distance.** Report both domain-pair changes and unrelated-edit response at every tested distance, with discovery-fixed signs/scales, paired-family uncertainty, sample counts and low-support cases. Match positions and filler inventories as registered. This compares finite constructed contexts; filler relocation and positional changes remain part of the manipulation. The exact distance-specific statistics and display rules are owned by its pre-inference configuration and must be linked at freeze.

## 12. Known Good / Known Bad / Known Confusing Cases

Known good: exact cached row/split match, FP64 sum-of-contributions versus sample-decoded mean difference, zero differences mapping to zero contributions. Known bad: a mismatched decoder layer or omitted restoration scale must fail interface/numeric qualification. Known confusing: high cosine with large norm error; biology-preferring members with positive signed contribution; positive-plus-negative totals exceeding1; silent current-panel members with high independent reference frequency; large family effects within a domain; identical lexical inventories reordered across distances. Keep these separate in code checks and prose.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal and input | Operation and reason | Expected output and stop |
| --- | --- | --- | --- |
| Identity | Same384 rows, true interface, native z and decoder | Bind parent hashes, ordering, gate and restoration scale; avoid decomposing another object | Input manifest and numerical audit; stop dependent work on mismatch |
| All-member decomposition | True difference plus all16,384 zero-inclusive activation differences | Sum restored decoder contributions; quantify full residual and directional shares | Full vectors, norms, shares, intervals; undefined ratios remainNA |
| Candidate selection | Discovery only | Freeze original top32 and expanded per-domain lists; evaluate all requested k on old heldout | Exact ordered IDs, random controls and candidate table; no replacement |
| Frequency/family/spectrum | Fixed references and all members | Apply frozen bins; nested variance; project the synthesized vector into R07 basis | Complete group/variance/spectrum tables; missing support retained |
| Distance | Fixed derived texts and checks | Extract native shared z under matched length/inventory conditions | All distance/control readings or exact failures; cap3,842 attempts |
| Delivery | Complete evidence and eligibility | Explain four main figures and supplements with real texts and values | Bilingual Summary/Detailed, one-page Chinese reading, reproducible artifacts; stop |

## 14. Algorithm, Output, And Provenance Contract

Execution root: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029`. Research-owned records remain in this round directory. Freeze the Anchor, Protocol, configs, code revisions/hashes, exact data/source manifest and selected asset access receipt before the corresponding execution. A live dirty workspace is permitted only with explicit file hashes; do not overwrite earlier outputs.

Retain true/reconstructed/residual vectors, every member contribution or its exact reconstructible factors, both domain means, activation occurrence, candidate orders, all tables, frequency source, PCA identity, random seeds, formulas/numerical audits, actual distance text/token indexes, runtime/parameter identity and reproduction scripts. Main figures are separate files:1a relative residual and1b cosine;2 top-k curves separately by ending;3 positive/negative/net frequency contribution separately by ending, with counts and residual;4 true/reconstructed spectral energy separately by ending. Supplementary plots cover frequency definitions, family variation and distance responses. Each figure's reader guide states axes, two possible readings, actual observation and claim limit.

## 15. Success / Failure / Insufficient Evidence

Engineering validity requires exact identities, complete row counts and independently checked numerical decompositions. Scientific outcomes are continuous and interpreted against registered competitors; no unregistered “good enough” residual cutoff is introduced. Close-to-full-dictionary error from a few fixed heldout members is evidence of concentration relative to this dictionary. Many required members or cancellations support a distributed description. Wording/ending changes restrict candidate portability. Substantial full residual preserves dictionary inadequacy. Wide intervals, weak activation support or invalid comparisons remain insufficient. Finish independent valid branches when another branch fails.

## 16. What This Cannot Claim

Reconstruction contributions are not causal importance. Domain association is not domain-exclusive knowledge. A few members explaining one mean difference do not imply low-rank domain knowledge or an expert allocation benefit. Frequency does not define semantic level, and tested distance response does not prove a general long-term computation mechanism. No new training, semantic clustering, causal ablation, data expansion, new dictionary, external resource or publication is authorized.

## 17. Block Confirmation, Freeze, And Amendment Ledger

A–F are grounded in the explicit user task and its clarification of “individual”; the user also delegated the frequency-bin choice and requested detailed distance measurement. Numeric seed/count choices are operational choices inside this scope. G is confirmed for cached decomposition after the current selected asset access check; main-stage consistency passes. The distance stage awaits only its final exact config/hash and implementation preflight. This dependency does not block cached decomposition and creates no new user approval requirement.

Stage freezes: the frequency/family config was frozen at2026-10-29 14:41 UTC, SHA256 `6632e2ff7a67578bfd66ea9bd4c6eb42747568627ee124f1c8290e8df942e2d3`, before its cache-only execution. Its result was visible before this consolidated Protocol was written; the frozen definitions are copied unchanged. Main decomposition freeze timestamp/hash are recorded by the root coordinator in the execution root before that stage. Distance config/hash: PENDING, required only before distance inference. Three audits cover scientific identification, data/statistics and implementation/numerics in `audits.md`; the complete task ledger is in `coverage.md`. Each stage has its own pre-execution snapshot; no later consolidated hash is backdated. After execution begins, preserve the registered body. Any material change is an appended amendment with old/new values, reason, exposure state, affected conditions, authorization and evidence-eligibility impact. Result records hold observations and interpretation, not the frozen scientific body.


### A01: distance-stage construction and statistics registration

Recorded UTC: 2026-10-29T14:50:29.959926+00:00. Scope: complete the previously authorized distance stage; no change to the frozen main-decomposition body. Before: distance extraction/statistics were described in outline. After: bind the exact prepared text set, extraction configuration and statistical definitions below. Reason: make the approved distance measurement reproducible. Main and frequency/family results were already visible. Distance extraction was authorized at2026-10-29T14:48:14.013455+00:00 against its existing config/text/code hashes; the exact statistics file was recorded at2026-10-29T14:49:16.345178+00:00 while acquisition was running, before distance statistical analysis. This amendment does not retroactively claim that its text or the statistics-file hash existed before all forwards. The numerical definitions were communicated during coordination; no distance outcome was used to select them. Evidence remains exposed exploratory analysis.

Extraction configuration: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R09_domain_difference_decomposition_20261029/distance/config.json`, SHA256 `107ebc8e18c601c5efdb31986f3a981eb368bdb8637ba5b259eb6d7cbc8ae89f`. The independently stored `run_authorized.json` binds the3,842 attempt ceiling, original text hash, code hash and existing H10080GB MIG3g.40gb allocation. No new resource submission is included.

Construction QA contains3,840 rows:1,920 discovery,960 development and960 original-heldout. Every row ends at target239 with240 tokens. Actual domain-core-end to target distances are16/32/64/96/144. The original domain core and ending remain. The original neutral postfix moves before the core; identical neutral filler blocks move before/after the core. Each source's token multiset is identical across its distances. Immediately after the core, Monday changes to Tuesday in one token. Five families require a fixed leading `brief` compensation after retokenization, affecting18 original records and180/3,840 derived rows. Preserve that flag and its framing limitation. Distance is measured from the semantic core endpoint, not every changed token. Domain replacement and a one-token date replacement are not equal-sized edits.

Statistics configuration: `distance/statistics_config.json`, SHA256 `ff0141593ac16896a8402885c469ece9d5ad6b973d63bd7f0d7eee6ab1a07e63`. For member j, fix scale s_j to the RMS of its z across all192 original R08 discovery rows, before distance results. If s_j=0, standardized values areNA. For each ending/distance, D is mean family/wording math-base minus biology-base activation, divided by s_j; its original sign is retained. Also save D multiplied by the original R08 discovery activation-difference sign for that ending. Retention is D_d/D_16 only when absolute D_16 exceeds1e-6. If its95% family interval covers zero, keep the numeric ratio but flag `unstable_ratio=true` and do not describe it as stable retention.

For each family/distance, E is the wording average of absolute math-base minus biology-base activation, minus half the sum of absolute Monday/Tuesday changes in the two domains, divided by s_j. It measures excess magnitude over this particular date-edit control. It does not identify general semantic specificity. Save raw z differences and decoder-norm×restoration-scale contribution-amplitude units alongside standardized values.

Use500 paired-family bootstrap replicates, seed2026102913, resampling all domains/endings/wordings/distances/control versions together. Only original-heldout E at distance144 receives a formal numeric sign-flip comparison: all4,096 sign assignments of the12 family values, one-sided alternative mean(E)>0, p=count(null mean >= observed mean)/4,096 including identity. Validity of that randomization reference requires a symmetric family-level null; edit-magnitude mismatch remains a scientific limitation. Apply one BH correction across the frozen unique141-member candidate union times two endings,282 hypotheses. No second D test is added. Zero-RMS hypotheses remainNA; p=1 is only a multiplicity-bookkeeping value for the original denominator, not a performed test. No global long/short semantic label follows from these tests.

Affected blocks: B/F/G distance details only. Authorization: the user's explicit current experiment/detailed-distance request plus root coordination within the specified existing resources. Main pre-execution snapshots stay immutable; all distance results retain construction, selection and exposure limits.
