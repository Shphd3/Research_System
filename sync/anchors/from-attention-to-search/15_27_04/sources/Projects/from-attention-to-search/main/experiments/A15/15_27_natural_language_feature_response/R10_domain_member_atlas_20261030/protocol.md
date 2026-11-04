# Protocol: R10 domain-member atlas

## 0. Approval Snapshot

Document status: APPROVED_FOR_CACHE_ONLY_ANALYSIS. Execution authorization: the researcher's current replacement instruction explicitly requests all cached five-panel statistics, Anchor, Protocol, results and figures without per-step approval. Frozen revision R10-v1 at 2026-10-30T02:41:30.403304+00:00. A–G blocks inherit that explicit instruction; implementation details below are AI operational choices within scope, not independent scientific approvals. Scientific acceptance/closure: Unknown.

Primary Anchor: [15_27_04](/data/250010109/Research_System/Projects/from-attention-to-search/main/problem_anchors/15_spectral_representation_and_functional_routing/15_27_natural_language_feature_response/subanchors/15_27_04_domain_member_atlas_anchor.md). Existing Focus: [natural language feature response](/data/250010109/Research_System/Projects/from-attention-to-search/main/focus/focus_natural_language_feature_response.md). Experiment role: operationalization/proxy audit and bounded descriptive analysis. One question: do whole-dictionary document discriminators have distinctive frequency/spectrum/context association? Main rivals: eligible-pool frequency composition, generic decoder front bias, and lexical/suffix effects. No training/model-forward execution is authorized.

## 1. Terminology / Definitions

Native feature means one of16384 shared-z coordinates, jointly encoded from14 layers under the original gate. Document response includes every zero at positions[32,192). Discovery raw AUC counts all30×30 cross-domain document comparisons, ties one half; direction-fixed AUC uses discovery direction. Occurrence is positive positions/65536 independent DCLM positions. Geometry is squared unit-decoder projection; contribution energy uses summed scaled reconstruction vectors. Token frequency here is count within this120-document panel, not DCLM feature frequency.

## 2. Anchor Alignment

Preserve the researcher's hypotheses and boundaries. Three analysis steps: freeze eligible members and ranks; compare reference frequency and common-spectrum geometry/use; examine real-token and paired context response. Completion means all cache-supported outputs plus precise missing-evidence records. No positive outcome is required for completion.

## 3. Tested Hypothesis

Low-frequency enrichment, separated spectrum distributions, and cross-wording context response are separate hypotheses. Descriptive support for one never establishes the others.

## 4. Rival Explanations

Background composition can explain counts; frequency/support can explain geometric bias; squared distributions hide signed direction differences; vector sums create cancellation; domain vocabulary/format and suffix changes can explain response. Pool matching, full-PC overlap, cosine/subspace checks, summed-vector energies and paired targets address these rivals only within observed panels.

## 5. Data Construction And Provenance

R04 has60 documents/domain, discovery30/development10/heldout20. Use original document IDs/groups and zero-based positions32–191. Equal160 positions/doc means ordinary pooling equals domain/doc/position weighting. Verify no document-group crosses splits. All heldout was previously inspected: exploratory reuse, not a new blind test. Record source hashes. Strict access check passed current session before deserialization.

## 6. Learning Task And Permitted Supervision

No fitted classifier, learned dictionary or optimizer. Natural domain labels are inherited human/AI-reviewed excerpt labels; genre, website and vocabulary confounds remain. PCA is offline covariance calculation only.

## 7. Model / Architecture And Frozen Variants

One A22 checkpoint SHA09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628;14 odd blocks1..27 shared z; native threshold0.051281172782182693. Final decoder is block27 residual-post. Scaled decoder=TRAIN_RMS27 times normalized-space decoder; same scalar leaves unit geometry unchanged. Verify source interfaces and cached scale. Never encode from block27 alone.

## 8. Training Objective And Optimization

NOT APPLICABLE. Zero training, parameter updates and new model forwards. No routing/intervention/distance experiment.

## 9. Conditions, Seeds, And Checkpoints

The exact machine-readable [config](provenance/config.json) is frozen before discovery selection or R10 results. Seed2026103004;1000 stratified document/family bootstrap draws and1000 conditional dictionary-background draws. Direction ranks use abs(AUC-.5), then feature ID ascending; exact.5 has no direction. Main support is >=5 discovery documents in EITHER domain. All qualifying oriented AUC>=.75 are main. Fixed sensitivity:.70/.80 and Top16/64/128 per direction without refill.

## 10. Primary Metric And Frozen Analysis Plan

Figure1 uses original cuts.002593994140625/.0134429931640625 with cut inclusive below; <20 DCLM hits stays unclassified outside plotted denominators. Log-width cuts.0045172553628813825/.06686505701697326 are sensitivity only.

Common PCA uses all60 discovery documents'9,600 true CC_h rows and one shared mean. Reuse old full1024-PC basis only after raw covariance, eigen-equation and orthogonality audits. Its sample covariance denominator9599 differs from normalized population weights only by one scalar and cannot alter directions. R07 is the SAME basis; independent-reference robustness is MISSING.

Figure2 uses unit decoder squared projections, complete sum1;16 bands of64. PC1/PC2–64/PC65+ are1/63/960-dimensional with reference fractions1/1024,63/1024,960/1024. Show member means/medians/distributions.

Background: all eligible nonzero decoder members INCLUDING main, strata original frequency four classes (including insufficient) × floor(total positive discovery documents/10). Draw math and biology sizes exactly per stratum without replacement and disjoint;1000 repeats. This is a conditional dictionary reference, not an independent null; report selected inclusion. Do not report it as a selection bootstrap or generalization CI.

Figure3 unit overlap is sum of PCwise minima and separately sum of64-PC-band minima. PC2–64 report raw full-vector energy plus within-segment normalized overlap. Appendix: all cross-group absolute cosine, actual decoder subspace principal angles and trace overlap. Separately compute actual heldout group vectors by summing z times restored decoder FIRST; average squared projections per document/domain then normalize; <1e-12 total squared norm yields NA. Four group/input-domain combinations.

## 11. Secondary Metrics And Guards

Heldout oriented AUC uses frozen discovery direction; bootstrap20 documents/domain independently1000 times, ties preserved. Report pointwise95% percentiles. Replication tag iff lower bound>.5; this exposed-data tag is not a confirmatory discovery. No reselection. Development is a separate descriptive check.

Figure4 token counts use all19,200 valid positions of120 equal-length documents, retaining punctuation/subwords/special IDs with explicit inventory. Type-frequency cuts are empirical higher quantiles1/3,2/3 over observed token IDs; ties unsplit. Report both type and position counts. Per-feature high threshold is positive discovery-z90th percentile. AI operational support guard: >=20 positive discovery events to define a usable quantile; >=5 heldout high events across>=2 documents to summarize composition. This guards a noisy conditional composition; no member is removed from the main list. Strictly greater events only; zero-response gaps stay explicit. Member-equal means, baseline all-position proportions. Examples: first3 fixed ranks/direction, high examples max1/doc and same-ID low examples in another doc; include only already-read prefix.

Figure5 uses48 family pairs,24/12/12 split,2domains×2wordings×2endings. Family pairing is a constructed contrast, not identical semantic tasks. A: domain differences at exactly fixed target ID within ending; raw paired points and all-member tables. Context recurrence: at least one ending has same nonzero discovery/heldout difference sign in both wordings, ending-average pointwise95% family interval excludes0 in both splits, and >=3 active families per split. Record agreement with natural-domain discovery direction separately. Suffix effect: paired E1−E0 averaged domains/wordings with same-sign nonzero intervals in discovery and heldout and support; interaction: difference of domain contrasts across endings, same rule. Tags are exploratory pointwise descriptions without multiple-testing confirmation. Context and suffix can coexist. All-zero members have insufficient coverage. Pure target-only B is missing, not inferred from ending contrast.

## 12. Known Good / Known Bad / Known Confusing Cases

Metric check: identical document arrays yield.5, complete math dominance yields1, reversal gives0. Geometry identity: full-PC energy1; coarsening overlap cannot decrease. Contribution check: direct vector-sum projection equals summed PC coefficients; independent member-energy sum is a deliberately wrong comparator retained for audit. Context bad case: all-zero feature cannot be identity; ending changes target and prefix suffix together.

## 13. Scientific Procedure And Stage Contracts

Stage1 validates input IDs/interfaces, disjoint groups, aggregate-vs-position z; failure blocks only dependent measurement. Stage2 freezes full dictionary support/ranks/main/sensitivity sets before further results. Stage3 validates common PCA and generates five statistics, retaining NA and exclusions. Stage4 checks independent formula reconstructions, data/selection contracts and rendered figures, then writes bilingual Summary/Detailed and source/output manifests. Missing pure-B and independent-reference assets do not block other stages.

## 14. Algorithm, Output, And Provenance Contract

Source scripts tracked in scripts/. Execution outputs at /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030. Save frozen IDs/order, all16384 metrics and main member master, per-member frequencies/projections/response/context, every old/new list membership, raw figure tables, examples and bootstrap/background indices. No existing result overwritten. Small selected figures/tables have an explicit payload manifest; raw arrays/checkpoints remain execution-side.

## 15. Success / Failure / Insufficient Evidence

Frequency: relative low enrichment supports H1 only against pool composition; no enrichment weakens it. Geometry: contrast outside matched reference supports special orientation; similarity weakens separation; missing coverage limits conclusion. Context: predefined recurrence weakens pure-identity explanation; suffix sensitivity supports an ending association; no support remains insufficient. AUC.75 is an operational rank cutoff, not semantic truth. Numerical failure blocks the corresponding plot, never triggers threshold tuning.

## 16. What This Cannot Claim

Exclusive knowledge, identical semantics/function from spectrum overlap, causal necessity, full-h explained variance, learning direction/interference, MoE utility, blind generalization or pure token identity. Model-forward supplementation remains NOT RUN pending separate confirmation.

## 17. Block Confirmation, Freeze, And Amendment Ledger

A question/boundary; B model; C data/splits; D selection; E frequency/spectrum; F context/missing-B; G outputs/scope: HUMAN_CONFIRMED by the detailed current instruction. AI additions are the explicitly named operational bootstrap/matching/support/tag implementations, authorized as routine cache statistics; they do not invent scientific pass thresholds. Cross-block audit: main membership never changes after discovery; every figure/table references same feature IDs; primary/common units agree; context target+suffix remains confounded; no full expensive execution. No post-result amendment at freeze. Deviations must be appended, never silently rewrite this document.

### Amendment A01: fine background reference

Active background reference follows [background_amendment.md](background_amendment.md); frozen v1 coarse draws are retained as method sensitivity. Post-v1 audit correction within authorized cache-only statistics; main feature selection and scientific thresholds unchanged,0new forwards. Precise machine revision in provenance/fine_background_config.json.
