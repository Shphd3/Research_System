派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/provenance/protocol_design_snapshot.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_28_sentence_feature_continuation/R01_cached_sentence_pairs/provenance/protocol_design_snapshot.md)；研究修改仍回到原件。

---

# Protocol: A15_28 R01 cached sentence pairs

## 0. Approval Snapshot

- Document status: `DRAFT_NOT_EXECUTABLE` for the proposed statistical implementation. H1/H2 measurements: `NOT RUN`.
- Researcher-confirmed purpose: “一句话中，前面 token 激活的 feature，到后面是继续出现、换成关联 feature，还是不再出现？”
- Scope already authorized: inspect existing conversations, owners, texts, native caches and old graphs; construct this new Anchor/Protocol; reuse cached analysis without training, reclustering, new large forwards or functional intervention. This delivery stops at the requested design-and-feasibility stage. No repeat blanket execution authorization is requested.
- Pending method review: lost-source H2 formalization, sentence/pair eligibility, exact matching, weighting, null procedures, uncertainty and decision parameters below are `AI_PROPOSAL`; they are not silently attributed to the researcher. Their acceptance and the frozen implementation are prerequisites for the subsequent analysis stage.
- [Focus](../../../../../../../../../UNAVAILABLE.md); [Anchor](../../../../../../../../../UNAVAILABLE.md); [中文](../../../../../../../../../UNAVAILABLE.md).
- Experiment role: operationalization/proxy test of coordinate persistence and old-edge association across positions. One experiment has three analysis steps: qualify sentence/cached coordinates; compare identity persistence; compare old-edge association and inspect cases.
- Minimal setup: the existing 120 math/biology document prefixes, native E16 SAE and native A22 CrossCoder caches, fixed DCLM frequency reference, and the original validation-passed raw A22 graph. SAE H2 is blocked by incompatible/unqualified old-graph measurement interface.
- Changed variable: whether the later position belongs to the source sentence or its paired unrelated same-domain document. Held fixed: earlier activation, dictionary, domain, matched target token/category, position strata and target activity range. This is observational matching, not randomized context intervention.
- Supporting: a qualified positive real-minus-control contrast with simultaneous interval above zero and compatible background/degree-null diagnostics. Non-supporting: interval entirely at or below zero. Insufficient: interval crosses zero, matching/denominator support or uncertainty fails, a required null is unqualified, or graph identity is unavailable.
- Cannot claim: complete information retention, causal transfer, semantic hierarchy, why clusters form, or functional usefulness. Statistical separation has no prespecified minimum useful-effect interpretation.

## 1. Terminology / Definitions

A **token position** is an offset in one cached 192-token prefix. A **complete sentence** is a text-audited span with a known start and end inside that prefix; a document/prefix is not itself a sentence. A **feature** is one coordinate of one fixed dictionary and activation interface. Equal numbers in SAE and CrossCoder do not identify equal features.

For one dictionary let \(z_{if}\) be its native activation and \(A_i=\{f:z_{if}>0\}\). Earlier/later positions satisfy \(i<j\) in the same complete sentence, with distance \(d=j-i\). Define \(F_b\) as a fixed DCLM frequency group. A source group is \(B_i=A_i\cap F_b\). Empty source groups give NA, not zero. L0 at a position is the number of nonzero active coordinates, L0(i)=|A_i|; it is a count, not activation magnitude.

The old graph \(E\) contains directed non-self edges. A22 has all 16,384 feature IDs in its universe, including isolated nodes. A source with no outgoing/incoming edges has genuine zero coverage in that direction. This differs from a feature absent from a graph's declared universe, which would make graph coverage unqualified rather than zero.

**T1** is exact target-token-ID matching across paired documents. **T2** is a separately reported fallback matching lexical class and source/target token-ID equality state; it does not control the exact target word. A **document block** is a fixed pair of different canonical documents. A **null** is a randomized reference preserving stated margins; it is not a replacement scientific graph or new dictionary.

## 2. Anchor Alignment

| Analysis step | Anchor term / rival | Computation and purpose | Decision role |
| --- | --- | --- | --- |
| Qualify texts and coordinates | Native activity, complete sentences, independent document units | Bind IDs/interfaces; audit all text-only sentence spans; freeze frequency bins and matched document blocks | Missing pieces stop only dependent quantities |
| Identity persistence | H1; prevalence, repetition, domain, L0 | Source-normalized overlap versus T1/T2 and incidence-margin null | Supports only sentence-local coordinate recurrence in its qualified stratum |
| Old-edge association and cases | H2; old-edge hub degree and lost-source selection | Forward/reverse lost-source coverage, all-source diagnostics, fixed-degree nulls and three figure types | Compatible with associated-coordinate replacement; not semantic abstraction |

This changes neither A15_27 results nor A15_25 graph construction. Existing response, classification and attention results do not answer these new estimands.

## 3. Tested Hypothesis

H1: same-feature continuation between earlier/later positions in a sentence exceeds comparable unrelated positions. H2: even when an earlier coordinate disappears, different later active coordinates have more old-graph connections to it than controls. Directions are tested separately. Neither hypothesis presupposes that a later token includes all earlier information.

The exact H2 lost-source denominator is an `AI_PROPOSAL` for the user's “even if no longer present” clause. All-source non-self coverage is retained as a distinct secondary observable. Positive H1 and H2 can coexist.

## 4. Rival Explanations

| Rival | Registered comparison / diagnostic | Remaining limitation |
| --- | --- | --- |
| High-frequency features recur everywhere | Independent fixed DCLM groups; per-feature/per-position margin-preserving incidence null | DCLM is a finite reference, not universal prevalence |
| Repeated lexical material | Same/different source-target IDs separated; exact target ID in T1 | Token IDs do not match syntax, word sense or multi-token phrases |
| Same-domain topic/style | Same-domain different canonical document control; genre/host balance reported | Topic, source and discourse roles may still differ |
| Different active-set sizes | Fixed source; target L0 caliper; narrower sensitivity; both L0 values reported | Conditioning on L0 can restrict the population |
| Graph hubs | Full-universe degree table; directed in/out-degree-preserving graph null | Degree null preserves node-level degree-frequency relations but not every graph motif or endpoint-frequency pairing |
| Lost-source denominator changes | Report lost fraction and both denominators; common-lost-set diagnostic | The primary H2 is conditional association, not a causal replacement effect |
| Matching-induced exclusion | Eligible/all-pair and matched-pair summaries; exclusions by reason | Matched results apply only to represented support |

## 5. Data Construction And Provenance

**Verified source.** Reuse `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/` (R04 root). `data/documents.jsonl` contains 60 math and 60 biology documents, one 192-token prefix each. The original per-domain splits are 30 discovery, 10 development and 20 heldout; all are already exposed. Preserve these labels in outputs but do not advertise any as fresh confirmation. Each document has URL/canonical group, WARC ID, source line/hash, source character offsets, prefix text and token IDs. Reuse all 120 for this descriptive analysis; no new task population is introduced.

The required input IDs are:

1. `model_qwen3_0p6b_base` and `model_qwen3_0p6b_base_official_a5` for parent identity.
2. `tokenizer_qwen3_0p6b_base_official_a5` for exact token/character alignment.
3. `sae_qwen3_0p6b_e16_layer27_final_1b`.
4. `crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013`.
5. `data_a15_27_r04_domain_native_dual_20261027`.
6. `analysis_a15_27_r04_native_sae_joint_cc_domain_20261027`.
7. `analysis_crosscoder_feature_relation_phase1_20261013t173130z`.

These are eight IDs because item1 contains two. Current strict access and bounded schema evidence are in [preflight](../../../../../../../../../UNAVAILABLE.md). Access is not new approval or weight rehashing. Per-token arrays are `forward/documents/<seq_id>.npz`, with `token_ids` and each dictionary's `ptr/ids/z`. Aggregate `documents_SAE.npz`/`documents_CC.npz` cover positions32:192 only and cannot replace full per-token arrays.

**AI_PROPOSAL sentence rule.** Tokenize the exact stored prefix with the registered tokenizer and require exact ID equality. Derive character offsets. Generate sentence ends at `.`, `?`, or `!` followed by closing quote/bracket characters and whitespace/end; protect decimal points, initials, and the frozen abbreviation list `e.g., i.e., etc., vs., Dr., Mr., Mrs., Prof., Fig., Eq., No., U.S., U.K.`. Paragraph breaks/headings/formula blocks are review flags, not automatic sentences. A text-only reviewer audits every candidate using the prefix and original source offsets, records any merges/splits and reasons, and marks complete/fragment/ambiguous. Freeze this manifest and hashes before pair statistics. Resolve ambiguous spans by exclusion, not by their activations. First/last truncated fragments are excluded; complete edge sentences are admitted only when the original character boundary or source context certifies completeness. If the needed source boundary is inaccessible, mark it unknown and exclude that fragment. Freeze the full token-to-sentence table, audited text and exclusion counts. No activation-based “good sentence” selection is allowed.

Eligible pairs are all \(i<j\) in the same accepted complete sentence. No union over all previous positions is computed. Distance bins (`AI_PROPOSAL`) are 1;2–3;4–7;8–15;16–31;32–63;64+, using only actual within-sentence distances.

Classify each token from its decoded surface: special ID; whitespace-only; contains a Unicode letter or number (lexical); punctuation-only after removing whitespace; other. A leading space on a lexical token does not make it whitespace-only. Pair classes, in priority order, are any-special, any-whitespace, any-punctuation, any-other, both-lexical. Special-token pairs are excluded from primary statistics and counted; other classes are separate diagnostics. Within every class, split exact source/target token-ID equality versus inequality. Retain numeric-containing lexical tokens with a separate count; do not infer semantic categories from IDs.

**Frequency reuse.** Reuse R05 `analyze_A.py:60–62`, `groups(k)`, from R04 `forward/reference_{SAE,CC}.npz`: hits=sum window counts; rate=hits/65,536. Features with at least20 hits are divided by rate quantiles1/3 and2/3, ties unsplit (`<=` lower is low, `<=` upper is middle, otherwise high). Below20 is `low_support`, never merged with low. These are inherited reference-support rules, not a new power threshold. Reference256 windows have254 canonical URL groups and no observed URL/WARC/full-source-hash overlap with the120 documents. Unknown near-duplicates remain possible.

## 6. Learning Task And Permitted Supervision

No learning task, fitting target, optimizer, dictionary training or clustering is introduced. Inputs are existing text metadata, positive native activations, fixed reference counts and old edges. Outputs are deterministic pair metrics, control assignments, conditional uncertainty and illustrations.

Text-only sentence review and domain labels are annotations, not mechanistic ground truth. Outcomes may not influence sentence acceptance, matching thresholds, graph choice, frequency cuts or primary families. No sealed TEST, new corpus harvest, new forward or context replacement is used. Existing split exposure is recorded honestly.

## 7. Model / Architecture And Frozen Variants

SAE: E16, F30000, zero-based block27 MLP input, native FP32 ReLU Top32. CrossCoder: final A22, F16384, shared z from residual-post blocks1,3,...,27; native BF16 GEMMs, saved TRAIN centering/vector RMS and score gate0.051281172782182693. No encoder branch slicing. Shared z is not independent per-layer activity. Heatmaps may show z or native decoder contribution but must name the quantity; inference uses binary z>0 only.

A22 graph source: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z/graphs/raw_edges.npz`. Use `A[passV] -> u[passV]`, exactly206,136 validation-passed raw edges, all16,384 nodes. `passV` is case-sensitive. No self-loops. Keep the original graph hash and direction. Do not choose reduced edges after seeing coverage.

An old A→B arrow counts **same-token** coactivation: nA,nB>=200; nAB>=20; P(B|A)>=0.8; P(A|B)<=0.5; nB>=2nA. DeltaP/lift were diagnostics, not acceptance gates. Frequency doubles along every arrow, so the absence of cycles/bidirectional edges follows the construction. The existing reduced graph removes transitive direct edges and changes one-hop coverage despite preserving reachability; it is not the primary graph. Neither depth nor degree is semantic level. No semantic-layer plot is proposed.

SAE H2 remains `INCOMPATIBLE_INTERFACE_UNQUALIFIED`: historical E17 used BF16 encoding, FP16 values, norm filtering and selected-index counts; R04 uses native positive FP32 z. No CrossCoder-ID substitution or new SAE graph is allowed. This blocks only SAE graph analysis.

## 8. Training Objective And Optimization

Not applicable: zero training steps, no fitted parameters and no optimizer state. The observable is a source-normalized fraction and its observational matched contrast. Sentence rules and randomization settings are analysis parameters, not learned model parameters.

## 9. Conditions, Seeds, And Checkpoints

All new numeric choices in this section and Sections10–15 are `AI_PROPOSAL` pending method review. Proposed base seed:20261028. Derive independent streams with explicit fixed integer offsets: document pairing+0, matching ties+1, document bootstrap+2, incidence null+3, graph null+4. Do not use process-dependent Python hash values. Record generator name/version and actual seeds.

Conditions are real within-sentence pairs; T1 exact-ID unrelated targets; T2 fallback targets; T1 with narrower L0 caliper; fixed-margin incidence null; and directed-degree graph null (CC only). Metrics for the same dictionary share frozen pairs/matches whenever their denominators allow. Model checkpoints are identity-only parents: no weights need be loaded for this cache analysis.

**Fixed document blocks.** Within each domain, sort documents by full-source-text hash then seq_id, shuffle with the frozen seed and pair adjacent documents. With60 documents/domain this creates30 blocks/domain. Each document can be source and its partner alone supplies unrelated target positions. No same-document fallback and no cross-block donor reuse. Record matched and unused support; reduced coverage caused by this block restriction is an analysis limitation, not genuine scarcity of all corpus matches.

**Target matching.** For a real pair `(i,j)`, hold i fixed and search accepted complete-sentence positions j' in its partner document. T1 requires tokenID(j')=tokenID(j), same target sentence-relative decile `min(9,floor(10*r/L))` (r zero-based within sentence, L length), same prefix-position quartile `floor(position/48)`, and target L0 ratio in[0.8,1.25]. If target L0=0, allow only0; source or metric-specific empty denominators are handled separately. Rank candidates by absolute L0 difference, absolute sentence-relative-position difference, absolute prefix-position difference, then SHA256 of dictionary/source-seq/i/j/donor-seq/j'/seed. Select one target. Reuse inside a document block is allowed and counted; block inference preserves its dependence.

If no T1 match, T2 keeps all the same positional/L0 rules but replaces exact target ID with token lexical class and equality state `ID(i)==ID(j')` equal to `ID(i)==ID(j)`. Report T2 only for T1-unmatched pairs, with a distinct population label; never pool T1 and T2 as word-controlled evidence. For same-ID pairs, equality necessarily fixes the target ID, so T2 may add no support. Do not relax requirements after seeing results. Narrow sensitivity uses the selected T1 match only, retaining pairs with ratio in[0.9,1.1]; do not rematch to recover a desired effect.

## 10. Primary Metric And Frozen Analysis Plan

For a source frequency group \(B_i=A_i\cap F_b\), identity persistence is

\[
S_{ij,b}=\frac{|B_i\cap A_j|}{|B_i|}.
\]

For replacement coverage, define lost source coordinates \(D_{ij,b}=B_i\setminus A_j\), then

\[
G^{\to}_{ij,b}=\frac{\sum_{f\in D_{ij,b}}\mathbf1\{\exists g\in A_j:g\ne f,(f,g)\in E\}}{|D_{ij,b}|},\qquad
G^{\leftarrow}_{ij,b}=\frac{\sum_{f\in D_{ij,b}}\mathbf1\{\exists g\in A_j:g\ne f,(g,f)\in E\}}{|D_{ij,b}|}.
\]

Each source coordinate counts at most once regardless of how many edges reach the target set. Empty denominators are NA. Compute the analogous quantity for j'. H2 uses each condition's own lost set; pairwise contrast requires both lost denominators nonempty. This compares conditional coverage over potentially different lost coordinates. Report both lost counts/fractions and the common-lost-set diagnostic in Section11; do not describe the contrast as a coordinate-specific causal replacement effect.

For metric M, calculate \(M_{ij,b}-M_{ij',b}\) on the identical eligible matched-pair mask. Aggregate in order: equal pair weight within sentence/cell; equal sentence weight within source document/cell; equal contributing-document weight within its fixed two-document block/cell; equal block weight within domain/cell. Report whether one or both documents contributed to each block. Unmatched all-real means remain descriptive and do not enter matched excess. A source-count-weighted fraction is secondary only.

Primary cells are T1, both-lexical, separately math/biology, SAE/CC for H1 and CC forward/reverse for H2, low/middle/high source frequency, the seven distance bins, and same/different ID. Keep the full predefined family of336 possible cells in the ledger; unavailable cells are NA, not removed to improve multiplicity. `low_support`, all-frequency, punctuation/whitespace/other, T2 and narrower-caliper panels are diagnostics and cannot rescue a failed primary cell. All strata retain their own denominators.

**AI_PROPOSAL uncertainty.** Resample whole paired-document blocks within each domain, using the same resampled block indices across dictionaries, metrics and cells,5000 draws. Fixed matching and all within-block dependencies remain intact. For each estimable cell, use the block-mean sample standard error and the bootstrap distribution of `(resampled mean - observed mean)/original SE`; use the95th percentile of the maximum absolute statistic across the predefined estimable primary cells for simultaneous two-sided intervals `mean ± q*SE`. These are approximate conditional block-bootstrap bands, not exact randomization intervals or fresh-confirmation evidence. Require at least two contributing blocks and finite positive SE to compute this form; these are mathematical requirements, not power qualification. If any bootstrap draw has no eligible contributor for a cell, mark that cell's interval unavailable rather than dropping bad draws or rerunning until it works. Report cell-specific block counts, missing draws and stability. No claims of useful equivalence follow a small or zero estimate. Secondary curves have explicitly pointwise95% block-bootstrap intervals and no confirmatory verdict.

Once outcomes are unsealed, the estimands, masks, bins, graph, aggregation, primary family and interval method cannot change silently. A change requires a dated amendment and a new exploratory label for affected evidence.

## 11. Secondary Metrics And Guards

Report all-source non-self graph coverage with denominator \(|B_i|\), forward and reverse, separately from lost-source coverage. Report source/target L0, lost counts, distinct incident-feature support, isolates, denominator-zero counts, and numeric-token composition. Whole graph universe coverage is100% for A22; “source has an edge” coverage is a different quantity and must not redefine the primary denominator.

A paired common-lost sensitivity uses \(B_i\setminus(A_j\cup A_{j'})\) for both conditions, with NA when empty. This reveals differences induced by the primary condition-specific lost sets; it cannot replace the primary result. If the primary and common-lost contrasts have opposite directions, or the common-lost diagnostic lacks support, retain changing lost-set composition as an unresolved rival. A positive primary alone does not establish stable replacement; a positive common-lost diagnostic cannot rescue a failed primary. The fixed narrower L0 comparison is similarly diagnostic.

**Margin-preserving incidence baseline (`AI_PROPOSAL`).** For each dictionary/domain, form the binary token-by-feature matrix on every accepted-sentence token. Use double-edge/checkerboard switches: choose two existing incidences `(r,f),(s,g)` uniformly; if r≠s, f≠g and cross incidences `(r,g),(s,f)` are absent, replace the two edges. Otherwise keep the state. Row L0 and every feature's total appearances remain exactly fixed; token metadata, sentence structure and matched rows are unchanged. Do not threshold or resample activations. Use two independent seeded chains, each with199 saved draws after5×nnz attempted switches and spacing ceil(nnz/10) attempts (398 saved draws total). Verify margins on every draw; record acceptance, original-edge overlap, autocorrelation of prespecified probes and between-chain comparison. Exact mixing is not guaranteed by a number of proposals. `AI_PROPOSAL` diagnostics: acceptance below0.001, original-edge overlap not decreasing during burn-in, or chain mean differences larger than twice the pooled between-draw SD in any of the fixed global overlap/coverage probes flags `MIXING_UNQUALIFIED`. Report the finite-draw envelope, not an exact permutation p-value. The operator removes lexical/sequence organization and is a marginal-background control, not a replacement for T1.

**Graph degree baseline (`AI_PROPOSAL`, CC only).** Keep all16,384 nodes and the binary activity matrix. Select two directed edges `(a,b),(c,d)` uniformly and replace them with `(a,d),(c,b)` only when a≠c and b≠d, and both proposed new edges are distinct, non-self, different from the original edges, and absent from the current graph; otherwise keep state. Preserve every node's in/out degrees and edge count; verify each draw. Use two chains with199 saved draws each (398 total), burn-in5×edges per chain and spacing ceil(edges/10) attempted switches, with the same recorded overlap/acceptance/between-chain diagnostics. These randomized null graphs may have cycles; imposing the old DAG constraint would change the null. They are explicitly synthetic degree references, never newly constructed old graphs. Real old graph bytes are immutable. With node identities and their frequencies fixed, this null preserves the node-level degree-frequency relation exactly. It does not preserve conditional-coactivation validity, the frequency pairing of edge endpoints, frequency-doubling/DAG constraints, or all motifs. Positive excess versus its envelope only addresses the specified degree explanation.

For each null draw recompute real and fixed-match metrics and their contrast with the same sentence/document/block weighting, without choosing new matches. The observed matched-pair eligibility mask is fixed separately for each cell/metric before randomization. Incidence H2 lost sets are recomputed per condition/draw on that exact mask. If any required pair denominator becomes empty in a draw, or any required cell/block value is otherwise undefined, mark that cell-null comparison `UNAVAILABLE` for envelope-based inference and record the draw/pair/block counts. Do not silently drop pairs, replace NA by zero, pool only valid draws or rematch. Purely descriptive changed-support diagnostics may be saved under a distinct label and cannot provide the stronger interpretation. For fully defined cell-null comparisons, pool the199 draws from each chain only after both chains pass diagnostics; the two chains together give398 draws. Null envelopes alone do not constitute valid hypothesis-test p-values. To claim excess beyond prevalence/activity and graph degree, require the observed real-minus-T1 contrast to exceed the97.5th percentile of its relevant fixed-null contrasts with qualified diagnostics; preserve the multiple-cell limitation of these diagnostic envelopes. A failed null stops only that stronger interpretation, not factual matched measurement.

## 12. Known Good / Known Bad / Known Confusing Cases

Before real pair metrics, use tiny hand-constructed arrays only. Identity: Ai={1,2},Aj={2,3} gives1/2; empty source gives NA. Replacement: E={(1,3)} gives forward coverage1 over lost set{1}; reverse0; a self-loop must contribute0. An isolated lost node has0, not NA. Empty lost set is NA even when identity=1. Restricting source frequency groups changes the denominator before division.

Check a complete repetitive-token sentence, different-token equal-support rows, an abbreviation/decimal fragment, one-token sentence, graph-hub target, swapped graph direction, and CSR row with all-zero support. All-null switches must preserve exact margins/degrees; failed proposals leave the state unchanged. Test block aggregation with unequal pair/sentence counts and shared donor targets, including one-document-contributing blocks. These verify implementation and do not count as empirical discoveries.

## 13. Scientific Procedure And Stage Contracts

| Stage | Goal / input | How and why | Output / handoff / failure |
| --- | --- | --- | --- |
| 1: identity and text freeze | Verified native caches, text and graph | Refresh required asset access; exact token alignment; text-only audit every sentence; freeze rules, bins, document blocks and hashes before outcomes | `sentence_manifest.jsonl`, source receipt, immutable config; missing cache/identity stops affected branch, ambiguous sentence excluded with reason |
| 2: implementation and matching | Frozen text/coordinates | Run Section12 synthetic checks; construct T1/T2 and fixed narrower mask without inspecting persistence/coverage; tally support losses | Matching table and calibration receipt; no usable matches yields insufficient cells, not arbitrary global sample gate |
| 3: metrics, nulls and delivery | Fixed pair/match tables | Compute H1, compatible H2, document-block intervals and fixed nulls; render three figure types and cases | Complete observed/unavailable cells, one-page summary and evidence; failed null mixing limits claims; no new models/graph reconstruction |

Preflight is design and source qualification, not observed H1/H2. This turn completes the draft and feasibility endpoint. Later method review can accept/correct the listed choices within already authorized cache scope; no extra training/run authority is implied.

## 14. Algorithm, Output, And Provenance Contract

The later implementation belongs execution-side at `/data/250010109/MoE_Router/experiments/20261028_sentence_feature_continuation/R01_cached_sentence_pairs/`; source/config copies and small provenance belong with this Protocol. Proposed entrypoints: `prepare_sentence_pairs.py` (text/cache audit and matching), `analyze_cached_pairs.py` (metrics/nulls/intervals), `render_figures.py`, and `audit_results.py`. These are planned names, not claims that scripts or results already exist.

Freeze input asset IDs, exact source files/digests, original producer evidence, Protocol/Anchor hashes, scientific config, code revision/dirty files, Python/package versions and RNG streams. Save all refusals, attempted/accepted swaps, pair/match reuse, conditional denominators and audit checks. A mismatch must stop the affected computation with a named error. Never regenerate missing cached activations.

Proposed resource ceiling: local CPU only, at most4 worker threads,16GiB peak RAM,4h wall time,5GiB new outputs. This is an engineering proposal, not a measured runtime estimate. Stop at the cap, save partial receipts and mark uncompleted nulls/cells NOT RUN; do not add resources or silently lower randomization effort. Before execution, synthetic runtime/memory checks must show a credible path within this cap.

Expected complete artifacts: source/freeze manifests; full sentence and token tables; all pair identities/matches/exclusions; pair-, sentence-, document- and block-level metrics; complete primary and diagnostic tables; raw null summaries and diagnostics; figures with exact plotting data; full scripts/configs; audit log; English/Chinese Summary and Detailed with missing work explicit. Raw arrays stay execution-side; only selected small evidence with a payload manifest enters research Git. Register actually produced reusable outputs after analysis, never planned assets.

Exactly three figure types:

1. **Sentence feature heatmap:** every token displayed; binary activity is the default color. If contribution is shown, declare native scaling and never compare unnormalized magnitudes across dictionaries. At most24 rows/dictionary, selected by decreasing number of active positions in that sentence, then summed native z, then feature ID. State total active union, omitted member count and per-token omitted-active counts. All tokens remain visible through consecutive panels if needed. Fragments, if shown as context, are distinctly shaded and excluded from metric counts.
2. **Persistence versus distance:** real and T1 control curves, separate frequency small panels; both source/target support and interval/matching coverage tables beside them. Same/different ID and nonlexical diagnostics separate. Pointwise curve intervals and simultaneous contrast verdicts have different labels.
3. **Old-edge coverage versus distance:** CC lost-source coverage real versus T1, forward/reverse separate; include all-source and null results as table/inset rather than changing the primary quantity. One sentence line diagram uses actual saved edges and states the original same-token arrow meaning. SAE graph panel explicitly says unavailable.

**Fixed case rule (`AI_PROPOSAL`).** From sentences with at least one both-lexical, different-ID T1 matched pair, choose one math sentence with the largest all-frequency SAE identity contrast; choose one biology sentence with the largest all-frequency forward lost-source CC contrast. Rank using equal-pair sentence means, tie by source hash and sentence start. These are deliberately selected illustrations, not representative or independent evidence. Choose a different-document counterexample minimizing the maximum of identity/forward/reverse CC contrasts among sentences where all three are defined; if that maximum is at most0, label a measured nonpositive extra-association case. This is a counterexample to excess over controls, not proof of zero raw persistence; state raw S and never call it complete non-continuation unless raw S is actually zero. If none qualifies, report that no such counterexample was found under this rule and show the weakest available case as such; do not invent a negative example. If either positive illustration has nonpositive maximum, call it the largest observed/weak case, not a supporting case. Display the same chosen real texts for both dictionaries where available, full quotes with token boundaries and a prose account of continuations, changes and absent coordinates. Show graph-diagram edges only among displayed features; state how many qualifying source/edge endpoints are omitted. All illustrative choices and alternative eligible scores are saved.

## 15. Success / Failure / Insufficient Evidence

| Outcome | Recognition update | Boundary |
| --- | --- | --- |
| H1 simultaneous lower bound>0, qualified controls/nulls | Bounded sentence-local coordinate continuity in that stratum | No complete information retention or causal propagation |
| H1 weak/unresolved, H2 lower bound>0 with qualified graph/degree controls | Compatible with associated-coordinate replacement | Not abstraction, semantic upgrading or a proved state machine |
| Excess only high-frequency or same-ID | Prefer public-pattern or lexical-continuity explanation | Do not generalize to rare/nonrepeated coordinates |
| Simultaneous upper bound<=0 | No positive excess supported under this measurement/population | Not proof of forgetting or zero effect in other representations |
| Interval crosses0, denominator/match/uncertainty insufficient, null unqualified | Insufficient; expose support and unresolved rivals | No negative mechanism conclusion |
| Only some domains/distances/sentences qualify | State those conditions and exceptions | No “all later tokens contain earlier tokens” claim |

Zero is a directional null, not a power-justified useful-effect threshold. No minimum64 documents, arbitrary effective-sample pass gate, or outcome-tuned threshold is introduced. At most30 paired-document blocks/domain exist; usable counts may be much smaller. Report both genuine corpus scarcity and losses caused by paired-donor restriction, position strata, ID matching, L0 caliper and metric denominators.

## 16. What This Cannot Claim

The study does not establish complete preservation of previous information, causal information transfer, semantic parent/child relations, a hierarchical semantic progression with token position, layer-local CrossCoder activation, cluster formation, expert learning benefit, or functional importance. Matching cannot remove every contextual confound. Already exposed documents support conditional descriptive analysis, not new independent confirmation. An inactive SAE/CC coordinate does not imply that the model forgot the earlier text.

## 17. Block Confirmation, Freeze, And Amendment Ledger

| Block | State | Grounding / pending item |
| --- | --- | --- |
| A Question/boundary | CONFIRMED | Current researcher prompt fixes the purpose, H1/H2, rivals and claim limits |
| B Data/provenance | PROPOSED | Reuse boundary confirmed; exact sentence rules, all120 exposed population and fixed document pairing require method review |
| C Task/supervision | CONFIRMED | Cache-only statistics; no training, reclustering, new large forwards or interventions |
| D Model/architecture | PROPOSED | VERIFIED_SOURCE: native identity verified from producers; CC V-passed raw graph as primary and SAE-H2 blocked documented for review |
| E Optimization | CONFIRMED | NOT_APPLICABLE: no optimizer or model fitting |
| F Evidence/decision | PROPOSED | Lost-source estimand, matching, weighting, simultaneous bands and null diagnostics/thresholds |
| G Reproducibility/scope | PROPOSED | Cache scope already authorized; exact seeds, resource ceiling, future scripts and freeze pending |

Cross-block consistency: draft self-audit and independent cold-reader review completed; corrections to null support, graph-degree invariants and case selection incorporated; not promoted. The user has not separately confirmed every AI-proposed statistical parameter. Scientific acceptance/closure remains Unknown. `design_frozen_at` and registered implementation/config hashes are pending; no real H1/H2 outcomes have been opened by this Protocol author.

Pre-execution promotion requires method choices resolved, applicable blocks confirmed, exact implementation synthetic checks passed and immutable text/config/code/source receipts. Existing cache-scope authorization is reused; missing approval is not invented from this review process. The later researcher decision about context replacement remains outside this round.

After the first authorized pair-statistic computation, preserve this scientific body. Any material change is an append-only amendment stating before/after, reason, already-visible results, affected cells/blocks, authority and evidence-eligibility effect. Execution receipts and result links may be appended without rewriting rules. No commit/push/external publication is authorized by this Protocol.
