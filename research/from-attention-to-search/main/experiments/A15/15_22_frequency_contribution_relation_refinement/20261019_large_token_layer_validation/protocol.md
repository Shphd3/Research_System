# Protocol: larger-sample and cross-layer token-rarity / rare-feature association

[中文](protocol_cn.md) · [Reasoning audit, Chinese](reasoning_audit_cn.md)

## 0. Authorization, question, and stopping point

**Status: APPROVED_FOR_BOUNDED_CPU_ANALYSIS; no observations are reported here.** The researcher explicitly requested larger-sample and cross-layer validation in this session and authorized analysis without training. This protocol operationalizes that bounded scope; the same authorization is not requested again. The execution-side `provenance/frozen_execution.json` froze the formal method and code at **2026-10-19 05:19:00 UTC**. This document was organized afterwards; it does not claim pre-result human block-by-block confirmation. Frozen code SHA256 is `0a232e3915b5a26798567f50d5149242d0136ca03e022a4600ce974c8ed6e426`. Authorization does not preconfirm a result or scientific verdict; receipts own current execution/result status.

The question is: **when the current token is rarer in a specified reference corpus, do rare shared features still tend to have higher hit incidence and layer-specific decoded-amplitude shares?** This is a robustness extension of H1 in the existing [Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_22_frequency_contribution_relation_refinement/15_22_frequency_contribution_relation_refinement_anchor.md). The previous [protocol and results](../20261019_bridge_dispatch/detailed_cn.md) remain exploratory evidence. Do not edit the old Anchor, Focus, or results. A separate Focus for this line is unbound, UNKNOWN; do not borrow an unrelated Focus. The explicit current-session authorization takes precedence over historical pre-execution states retained in older records.

Complete three steps: (1) bind saved caches, frequencies and layer coordinates and freeze reference-defined groups; (2) calculate all 14 layers and hit/amplitude decompositions once; (3) deliver direction, magnitude, weighting sensitivity and block variation, including negative and unestimable results. Stop after delivery. Allowed claims concern descriptive associations in these caches; original-document independence is UNKNOWN, so this is not independent confirmation.

## 1. Objects, data, and reuse

Freeze Qwen3-0.6B Base and the final 14-layer, 16,384-feature CrossCoder. One-based layers are 2, 4, …, 28, observed at block residual-post, before the final RMSNorm at layer 28. Every position has one nonnegative shared activation vector z, jointly encoded from all 14 layers. Only decoder vectors differ across layers. Keep the model, dictionary, TRAIN normalization, original gate and threshold unchanged.

| Corpus / role | Reference | Review | Scope |
|---|---:|---:|---|
| DCLM, primary larger sample | Existing D: 5,238,097 positions | Existing V: 5,247,663 positions | Total 10,485,760; 81 consecutive-context blocks within one bin, at most 128 full contexts per block with the last block retained. Reuse side assignments; blocks are not original documents. |
| Tulu SFT, cross-layer supplement | Existing TRAIN: 85,548 answer-prediction positions | Existing EVAL: 22,446 positions | This does not enlarge the SFT sample. EVAL is exposed. Describe variation by complete conversation. |

DCLM producer root P is `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/feature_relation_phase1/20261013T173130Z`. Reuse `P/feature_cache/manifest.json`, `P/split_manifest.json`, `P/feature_frequency.npz`, `P/decoder_geometry.npz` and original identity records. Frequency rows `n[0]` and `n[1]` correspond to D and V. Geometry `norm` has shape 14×16384; `raw_norm=norm*rms`. Use norm in the TRAIN-normalized layer coordinates. A positive layer-wide scale leaves R unchanged; do not compare absolute cross-layer M as physical amplitudes in common units. Tulu uses the old record's `analysis/sft_route_learning/20261019T012300Z/cache/{train,eval}.pt` and position provenance.

Registered input IDs include `representation_crosscoder_qwen3_final14_f16384_val10485760_phase1_20261013t173130z` and `analysis_crosscoder_feature_relation_phase1_20261013t173130z`. Before payload use, perform current strict access checks and bind all actual dependencies, including Tulu cache lineage, in a small input manifest. Access does not prove loadability or document independence. Check the actual loader, cache interface and parent identity. Reuse saved activations and geometry and adapt CPU statistics only; do not regenerate caches, run model inference, or call training entrypoints.

## 2. Two frequencies and frozen grouping

Within each corpus, estimate frequencies only from D or TRAIN. Feature frequency p is the fraction of valid positions with shared z_i>0. Current-token frequency f is the count of that current ID divided by the same number of valid positions. At position t, v_t is already read; next target v_(t+1) does not enter grouping, profiles or the primary test. Retain Tulu's prompt-end marker for the first answer prediction.

The primary groups B1–B4 divide the positive log10(p) range into four equal-width intervals in ascending order, with the last interval including its right endpoint. Put p=0 in U. Keep all 16,384 features, including high-frequency features and U, in the amplitude denominator. Save edges, members, reference counts and review support. Do not exclude features with reference n<20; report their counts, coverage and amplitude separately. A degenerate range or empty band that invalidates the prescribed construction is measurement insufficiency; do not silently change the number of bands.

For token groups, weight each positive-frequency reference token ID equally and compute its frequency's 20th, 40th, 60th and 80th percentile thresholds using the frozen code's `method='higher'`. Form five groups; do not split tied frequencies, assign edge ties to the lower group and retain empty groups as NA. The continuous rarity score is s=−log10 f. Review IDs unseen in reference form a separate group and leave the primary correlation; retain their other profiles without smoothing them into the lowest positive-frequency group.

Separately retain the exact old Tulu B1 pool of 1694 features and calculate the same profiles in both corpora as a **pool-migration control**. Report its new reference frequencies and allocation across the new bands and U. This is not synonymous with corpus-specific B1, and cannot replace or rescue a primary result.

## 3. Separate hits, amplitude, and denominator

For each position t, layer ℓ and feature i, multiply shared activation z by the layer decoder vector's L2 norm and sum by band:

\[
c_{i,\ell}(t)=z_i(t)\lVert d_{\ell,i}\rVert_2,\quad
M_{b,\ell}(t)=\sum_{i\in B_b}c_{i,\ell}(t),\quad
T_\ell(t)=\sum_{i=1}^{16384}c_{i,\ell}(t),\quad
R_{b,\ell}(t)=M_{b,\ell}(t)/T_\ell(t).
\]

c and M are nonnegative decoded-amplitude proxies. They omit bias, mean, reconstruction residual and vector cancellation. R is a unitless share, not information, explained variance or learning value. Set R to NA at T=0, retain counts and add no small constant.

For each token group report: any rare-feature hit probability (anylow), rare hit count (lowcount), mean position-level lowcount/totalactive (totalactive is the position's total active count; NA at zero denominator); per-layer means of M_low, T and R_low; and all four band mean shares. For the full review side additionally report zero-R probability, the positive-conditional mean, and hit-quantity correlations with rarity. Shared-z hit quantities are identical across layers; duplicated table rows do not add independent evidence. Retain R>0 separately from anylow; do not assume no zero decoder norms. Frozen code does not separately output group quantiles, group positive-conditional means or U amplitude, so do not claim these were measured; U remains fully inside the denominator. The zero/nonzero decomposition is descriptive, not causal.

Add a **feature-level auxiliary test**: for each feature, average current-token rarity over its V/EVAL hit positions whose current ID was seen in reference; correlate this mean with −log10 p_i across equally weighted features. Save all 16,384 features with reference p, eligible hit support and mean rarity. Reference p=0/U has undefined reference rarity and is excluded, as are features with no eligible review hit. A retained U hit-mean does not make its frequency comparison estimable. Report fixed eligible-hit thresholds ≥1 and ≥20, without result-based threshold selection. Compute binary-hit-matrix transpose products with rarity/known-ID flags only, not a feature co-occurrence graph. This directly checks feature frequency versus hit-token rarity and remains distinct from the primary position-level R1 analysis.

## 4. Primary analysis, weighting, and variation

For each corpus's review side and both primary B1 and old Tulu pool, report Spearman(s,R_low) for every layer. Use average ranks for ties; fewer than three valid observations or fewer than two distinct values in either variable yield NA. **Position weighting** gives each eligible position equal weight. **Token-ID weighting** first averages review R for each ID and then correlates these ID means with rarity across IDs. Retain eligible-position counts; mark ID/singleton counts not separately reported if absent from frozen outputs. These weights answer different questions; their difference is not an identified causal bias contribution. Show all other three primary band mean shares beside B1; a relative B1 ratio alone is insufficient.

Compute DCLM V's overall rho point estimate. Do not perform 1000 whole-sample reranking bootstraps. Calculate every layer's rho within each existing V block and retain the block table, distribution and estimable/NA counts. With seed=20261019, resample blocks 1000 times to obtain 2.5%–97.5% descriptive percentile intervals for the **equal-block mean rho** and **layer-28 minus layer-2 block-mean difference**, using the same resamples across layers. Frozen code averages each layer after independently dropping NA: a complete-pair interpretation requires identical estimable-block sets in both layers and must be checked in the result record. Otherwise retain this limitation rather than claiming a complete-pair difference. These are not confidence intervals for overall rho, independent-document intervals or population significance tests. Report every layer without selecting a best layer or choosing a post-hoc successful-layer count.

For Tulu, calculate corresponding rho and variation by complete conversation. Keep small unestimable conversations as NA with reasons; do not replace them with zero or independent-position inference. If none are estimable, mark this stability evidence insufficient. Position count cannot repair missing document independence.

## 5. Rivals and interpretation branches

The strongest rival is a combination of token identity, format/source/position composition and the amplitude denominator, rather than rare features generally identifying rare tokens. Two weighting schemes expose ID-composition sensitivity; separate M and T expose denominator changes; zero incidence and conditional amplitude reveal effects carried by a few events; matched positions across all layers prevent layer selection. Retain Tulu's existing source, prefix, answer-position and prompt-boundary metadata. Mark unavailable DCLM original-document/source labels UNKNOWN; do not fabricate controls. Such descriptions do not isolate all contextual causes.

- **Bounded support:** a positive overall primary rho supports the direction only for the reported corpus/layers, interpreted jointly with magnitude, block directions and both weights. Tiny effects or block heterogeneity permit only weak or conditional support, not universal correspondence.
- **Non-support:** zero/negative primary rho or positive direction confined to one weight, a few blocks/layers or the old pool weakens the corresponding generalization. Do not replace pools, layers or metrics to obtain success. Positive R without corresponding M/hit evidence supports a relative-share association only.
- **Insufficient:** unestimable or low support, incomplete execution, unestimable block/conversation variation or inconsistent directions. Unresolved identity/format/denominator explanations do not become mechanism evidence. Within-bin limitations remain regardless of descriptive intervals.

Do not invent thresholds for a strong association or practical gain. Metric direction does not automatically confer the researcher's scientific verdict. Finish factual records and stop under all three branches.

## 6. Procedure, correctness, and resource ceilings

New execution root: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/token_feature_layer_validation/20261019T_validation`. The pre-execution `provenance/frozen_execution.json` owns formal parameters, code identity and freezing time; later organization of this text does not rewrite that time. Previously exposed inputs remain exposed after freezing.

1. **Bind inputs.** Verify D/V counts, block sides, token-position alignment, sparse pointers, feature IDs, nonnegative finite z, geometry shape/finiteness, complete denominator and separate U. Check saved p against a small original-event sample. Stop on identity or alignment errors; do not change data or regenerate caches.
2. **Check correctness.** Independently sum M/T/R for a small set of actual positions. Explicit NA rules handle constant rho, unseen tokens, empty groups and zero total amplitude; do not claim unexercised branches were tested. Tulu layer-28 primary position-weighted rho must reproduce 0.259051203 within the frozen code's absolute tolerance 2e−5; position-wise R uses rtol=4e−5 and atol=1e−7. Otherwise treat measurement/implementation as unqualified before scientific interpretation. These checks do not assess model quality.
3. **Run once and deliver.** Stream sparse CPU inputs without a positions×features dense matrix, process layer ranks sequentially and retain paired block statistics. Record reads, computation, elapsed time, process RSS and incremental disk; save complete tables, logs, manifest and completion/failure receipt, then stop.

Hard ceilings: 8 CPUs; process RSS≤16 GiB; new disk≤1 GiB; formal CPU statistics≤30 minutes elapsed; total task≤90 minutes elapsed. On excess usage, nonfinite values, identity/alignment error or failed key replication, save partial receipts and stop. No automatic subsampling, retry, expansion or GPU switch. No new inference, activation-cache regeneration, GPU/paid remote task, training, commit, push or external sync.

## 7. Deliverables, audit, and freeze

Execution owns small code/config, input identities/current-access evidence, groups/edges, all corpus×pool×layer×weight tables, token groups, feature-frequency/hit-token-rarity tables, hit/amplitude decompositions, block/conversation rho including NA, layer differences and pairing limitations, resource records and receipts. New Summary/Detailed records own actual results and missing evidence; they do not enter this protocol. Raw caches and large arrays remain execution-side. The run manifest binds actual filenames, code hashes, dependencies and outputs.

| A–G audit block | Current operationalization |
|---|---|
| A Question/boundary | No-training robustness extension of existing H1; no question closure |
| B Data/provenance | Existing D/V and TRAIN/EVAL; exposed and within-bin limits retained |
| C Task/supervision | Current token and frozen z only; no learning target or next-target substitution |
| D Model | Shared z and 14 decoder norms; no independent per-layer activations |
| E Optimization | NOT APPLICABLE; create no optimizer |
| F Evidence | Separate primary/migration pools, weights, denominator and block variation |
| G Execution | Current-session authorization covers bounded CPU analysis under these ceilings |

This ledger records authorized scope and AI-formalized execution details; it does not retroactively approve older Anchor/Focus states or a conclusion. Actual preflight records cross-block consistency and input binding without another human approval round. Preserve the scientific body after execution starts. Append amendments for changes affecting question, data, groups, primary metrics, resources or interpretation; record old/new values, reason, whether results were visible, authorization and evidence eligibility. Unrun results, absent document-independent validation and unmeasured learning value remain explicit.
