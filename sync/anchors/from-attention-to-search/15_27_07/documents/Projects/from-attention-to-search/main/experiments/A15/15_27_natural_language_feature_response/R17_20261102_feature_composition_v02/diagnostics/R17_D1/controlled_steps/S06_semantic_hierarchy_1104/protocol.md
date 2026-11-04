派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/protocol.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S06_semantic_hierarchy_1104/protocol.md)；研究修改仍回到原件。

---

# S06 Protocol: SAE combinations and semantic hierarchy

## 0. Approval and scope

APPROVED_FOR_BOUNDED_INFERENCE_AND_ANALYSIS by current direct user request. Anchor owners 15_27_06 and 15_27_07 retain their identities; older functional hypotheses and records are preserved. Engineering operationalizations below are AI choices within the explicitly delegated design/execution scope, not researcher scientific acceptance. No waiting gate remains. Scientific acceptance, mechanism judgment and closure: Unknown.

Purpose: distinguish reproducible member replacement (round H1) and joint relative strengths (round H2), including category and wording dependence. No training, classifier, SVD, interventions or router. Complete all applicable steps, figures, bilingual results, daily brief, memory and <20MB package.

## 1. Definitions and design

An SAE feature is a coordinate in its own dictionary. Active means native Top32 output z>0. Top32 bounds support size; if all selected values are positive, both samples have32 members and recruitment equals loss structurally. The Attention hook is final zero-based block27 self_attn.o_proj output before residual addition. MLPIN is actual block27.mlp input, after residual addition and post_attention_layernorm. Both use native linear encoder, ReLU and Top32, no input normalization or decoder-bias subtraction. They are not MLP before/after causal comparisons. Model/SAE/loader IDs, absolute paths and hashes are in frozen_plan.json, inherited and verified from S04.

## 2. Data and confirmation boundary

Exactly16 independently authored frames,8 discovery F01–F08 and8 heldout F09–F16, fixed before responses. Each frame contains animal/cat/dog, vehicle/car/bicycle and chair/stone, each in explicit/synonym/property wording:384 prefixes. This is16 families/domain, but only16 correlated frame clusters, not32 independent clusters. A frame/domain/wording never crosses splits. Fixed manipulated category phrases repeat; this is a controlled panel, not training-unseen language. Record every literal string, template, label, phrase, full tokenizer IDs/pieces/offsets, final suffix token index and explicit-label flag. Three wordings share semantic intent but synonym parents and broad property descriptions are imperfect, stated in data_audit. No sample removal on behavior or representations.

All end with exact newline+Description:, no trailing space. Sample final colon ID25 before any candidate; absolute token positions may vary and are recorded. Semantic swaps within frames control syntax; cross-domain and chair/stone serve negative controls. Synonym/property variants probe lexical dependence. Repeated forms are not independent families. No prompt search.

## 3. Native behavior and extraction

Use frozen official Qwen3-0.6B Base in FP32 CPU2threads, eval/no gradients, physical shape4x128. Complete candidates in fixed order: ' cat.', ' dog.', ' car.', ' bicycle.'. Verify concatenated tokenization retains the prefix; record actual lengths and all per-token log probabilities, including punctuation. Main score=sum log conditional probabilities in nats, no prior/length calibration; max wins, fixed-order ties recorded. Fine children get sibling binary accuracy (each label denominator8/split/wording) and four-candidate accuracy; parent/negative get preferences only. Counts on all384 retained prefixes; behavioral eligibility>=.75 per child on heldout for semantic interpretation; failure limits semantic claims, not descriptive feature reporting. Secondary length-mean scores are explicitly diagnostic if lengths differ.

Representation at prefix end can be captured in teacher-forced candidate calls because causal attention excludes future candidate tokens. Validate prefix-only equivalence, lane equivalence, no-op hooks, native SAE encoding equality, finite values, and reconstruction=residual ledger before extraction. Save preactivation, Top32 ranks/cutoffs, raw z, decoder norms, h and reconstruction error; sparse full z supports portable audit. Freeze input hashes and old S02–S05 hashes. No changes to weights.

## 4. H1 computations

For P→C, P→D, C↔D and all9 cross-domain pairs within frame/wording compute intersection I, union U, J=I/U, I/parent-active-count, counts, recruited/lost IDs and triple intersections. Negative pair comparisons are descriptive. Primary per-domain family contrast = mean of3 within-domain J minus mean of9 cross-domain J. Label null permutes the six labels within each heldout frame independently (4095 Monte Carlo draws, plus-one p); maintains family correlations, TopK and each vector's scale. Also permute family pairing while preserving labels as a template-control diagnostic.

Explicit-discovery common candidates: triple-active in>=6/8, rank frequency then mean raw z, top8. Child recruitment/loss candidates: event frequency>=4/8, rank frequency then absolute mean delta, top6 each. Freeze IDs and direction before heldout inference, then report every candidate/event/wording, including failures. Counts are proportions out of8, not independent candidate replications. Frequency is panel activation rate (count/64 explicit discovery rows), not training-corpus rarity.

Baselines:512 uniform32-of30000 support pairs and512 discovery-frequency-weighted pairs (count+.5 smoothing), sampling without replacement. Report exact budgets and baseline distributions. For selected lists,256 count-matched random lists, each coordinate active-count within+/-2 on explicit discovery, own list excluded; unmatched lists remain failures, never broaden matching after results. Compare common/event coverages and joint projection pattern against matched references; primary label-null judgment remains separate from these descriptive random diagnostics.

## 5. H2 computations and joint patterns

H2 list per domain consists of triple-active features in ALL8 explicit discovery families, sorted mean raw z descending, max8; no selection on class contrast. All raw values and q=z_list/L2(z_list), along with whole-z L1/L2 and list L2, are reported. Zero norm undefined. Decoder norm weighted sensitivity uses its own exact denominator and is retained even if equivalent. Fixed-list q is distinct from pair-dynamic common-member normalization; the latter is paired explanation only and never a single-input router.

For each of P→C/P→D/C→D calculate discovery mean q difference. Primary sibling statistic is heldout q difference projected onto unit discovery mean sibling difference; only pairs with identical support on the fixed list and>=2 positive members are eligible. Need>=6/8 eligible heldout families; insufficient otherwise. Freeze discovery directions before heldout; report all ineligible pairs and full-vector values descriptively. Exact independent sibling sign swaps yield p. Parent-child and pair-dynamic common deltas are descriptive, not rescue tests. Show four discovery-chosen most changing pairwise member strength orders, joint support patterns and all paired difference vectors. Distinguish raw total scale from relative differences.

For full30000 differences decompose retained-amplitude/recruited/lost components (disjoint per pair); squared-norm shares denominator=full paired squared norm, pooled shares=sum component squared norms/sum full squared norms. Mean components can overlap across families, so do not add their squared lengths. Cat−P/dog−P and car−P/bicycle−P share P; report similarity against within-frame random reassignments of P/C/D preserving shared-parent structure and against family-mismatched pairs; never call positive cosine itself a semantic direction. SVD and classifier are NOT RUN by choice; joint differences answer the present question without them.

## 6. Uncertainty and verdict

Explicit primary tests: H1/H2 x2 domains x2 SAE=8; Holm familywise .05, no auxiliary rescue.4096 family bootstrap resamples(seed20261104),95% percentile intervals, equal family weights. These small constructed-frame intervals do not estimate all natural language. Local support: eligible, behavior>=.75 per child, positive estimate/lower interval>0 and Holm pass. Cross-wording support additionally needs positive lower interval and behavior qualification in synonym/property, plus H2 same-support eligibility. Valid contrary/failed replication limits or does not support that specific prediction; inadequate behavior, matching, eligibility or resolving power is insufficient, not falsification. Explicit-only results may be locally supported while generalized hypotheses remain insufficient. All posthoc observations labeled exploratory. Human scientific acceptance remains Unknown.

## 7. Ordered execution, outputs and audits

1. Asset/schema/old-source audit, write Anchors/Protocol, freeze panel and hashes.2. Explicit-discovery extraction+native scoring and numerical calibration.3. Select candidates/directions on discovery ONLY, save hash gate.4. Extract remaining discovery controls and all heldout conditions.5. Compute all H1/H2/negative/random/lexical/family/preactivation/reconstruction comparisons without further fitting.6. Figures: preselected complete F09 animal and vehicle, within/cross comparisons with every family, wording-control and failures.7. Independent numerical recomputation and source preservation.8. Bilingual Summary/Detailed, Chinese daily report, bounded Anchor evidence update, append-only own memory, synchronized local reading copies.9. Package complete sparse activations/texts/summaries/selected preactivations and scripts, full cache external indexed with bytes; check<20,000,000bytes, ZIP CRC, extraction and main files.

CPU time ceiling3600s for extraction, no cloud job or GPU use. On isolated failure preserve partial receipts and finish independent work. Resume only missing output IDs, never silently rerun completed outputs. Scientific, data/statistics and implementation audits recorded separately. Environment dependencies reused from /data/250010109/dependency_packages/hf_transformers_qwen3; native loaders reused; S04 capture/scoring adapted to384rows/four candidates, new analysis separately authored. Training reuse index inspected; training infrastructure unused. No commit, push, external publication or Graph edits.

## 8. Freeze and amendment ledger

Initial revision: 2026-11-03T16:51:17.839496+00:00. Scientific body, data, config and script hashes in evidence/protocol_freeze.json. User authorizes delegated in-scope design and execution now; operational thresholds are AI registered choices, not attributed human mechanism judgment. A–G cross-consistency PASS for this bounded scope. After first forward, preserve initial body. Material repairs are appended with timestamp, old/new value, reason, response exposure and eligibility impact in amendments.md; original versions remain in versions/. No result-driven candidate or threshold changes.
