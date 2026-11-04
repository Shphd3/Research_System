派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/detailed.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R10_domain_member_atlas_20261030/detailed.md)；研究修改仍回到原件。

---

# Detailed evidence ledger: R10

[Summary](summary.md) · [Frozen Protocol](protocol.md) · [Definitions](definitions.md). Eligibility: DONE_EXPLORATORY for exposed-data statistics, DONE_VALID for numerical identities; scientific acceptance Unknown. No model forward or parameter update occurred. This is one continuation experiment, not five model experiments.

## Evidence and execution

R04 supplies120 unique source-document groups,192-token original prefixes and160 selected positions/doc. Source labels are content-reviewed math/bio excerpts, not model-derived semantic ground truth. Discovery/development/heldout sizes per domain30/10/20 remain intact. Feature occurrence has a separate65,536-position,256-window reference whose canonical document groups are disjoint. The source manifest hashes actual cache files. R07 paired input targets have equal position within every math/bio pair, while the family target indices span30–38. E0/E1 core text is equal but suffixes differ. R08 target rows align by seq_id, not arbitrary row position.

All-dictionary screening uses document means INCLUDING zeros; the support gate is OR, not AND. Independent Mann–Whitney rank sums reproduce all16384 pair-probability values. Discovery membership/rank was written to freeze.json before heldout or geometry output. Output freeze hash=dbe0a02209a9f47ebf8fd15461777e3b3b48600fb946342993bb25a5ac917946. Config hash=cc17e6164919ec8f1e4a4490c64a3b00180ebc5b9a2f815ef388e5bec6d66407. A rerun must reproduce identical sets/hash or refuse. Old legacy both-domain eligibility and small-list results remain unchanged.

The common basis is the existing R04/R07 one, verified against raw discovery h: mean error0, eigen residual~1.8e−15, orthogonality~3.4e−15, rank1024. Decoder/true h are residual-post block27 before final norm, with no h unit normalization. Decoder model units use TRAIN_RMS27=374.3495121024576. Native BF16 activation readings are reused; linear projection/reconstruction statistics use FP64 saved trained decoder weights. This is a mathematical reconstruction, not an extra native-BF16 model replay.

A01 fine-matched dictionary draws include the main set, preserve half-octave occurrence and5-document total/max-domain support stratum sizes exactly and are disjoint between groups per draw. This avoids a missing replacement stratum without silently changing rules: it estimates conditional dictionary composition, not an outside-main independent population. Source total-pool/stratum counts and all1000 ID arrays remain saved. Bootstrap weights resample documents for AUC and whole paired families for context; per-feature95% tags are pointwise exploratory. No selection-bootstrap uncertainty was claimed.

Contribution uses every heldout token, two groups on both input domains, with scale restored and group vectors summed before square. Direct vector/PC paths agree within5e−14. No vector energy falls below1e−12. The saved deliberately incorrect sum-of-member energies differs and cannot replace the primary values. Shared decoder bias/mean is excluded from group v, since it is not a selected-member term.

Token frequency types count every valid ID, ties stay together. Member thresholds are discovery-positive p90; strict heldout > preserves discreteness. Guarded event-composition summaries exclude62math/55bio only from that panel denominator. All960 remain in master with reasons. All-member high/ordinary/same-ID-low instances and corpus per-ID math/bio counts are stored in execution tables; no future context is used. Because counts are built from this same120-document panel, this is a within-panel association, not independent frequency validation.

## Three audits and conformance

| Audit | Evidence | Result and limit |
|---|---|---|
| Scientific identification | Anchor/Protocol; frequency pool vs matched geometry vs fixed-target controls | Distinguishes descriptive alternatives; pure identity and causal function remain unresolved |
| Data/statistics |120 unique groups,30/10/20 split,disjoint reference; paired family bootstrap; counts/ties retained | All requested cache-supported cells complete; exposed heldout not blind; pointwise tags do not control multiple-member false discoveries |
| Implementation/numerics |Independent ranks,sparse means,OR support,full-PC sums,exact strata,vector sums,token gates,position/ID checks | 5009checks pass,0failed;0trainable parameters/optimizer/forward calls |

| Protocol item | Actual | Status |
|---|---|---|
| Full universe, OR support, AUC.75, fixed rank views |16384→10076→433/527; Top16/64/128 and.70/.80 saved | Conformant |
| New common-all-token discovery spectrum | Archived basis already exactly satisfies requested h/weights; raw covariance audited rather than arbitrary refit | Conformant reuse; R07 independence wording corrected |
| Same main list through five analyses |960 IDs unchanged; missing panel support tagged | Conformant |
| Matched background |1000 exact-stratum same-size disjoint draws from inclusive eligible pool | Conformant with explicit inclusive-pool interpretation |
| Pure target-only B |No such cached contrast;48-new-forward minimum proposal only | BLOCKED by missing measurement/authorization; NOT RUN |
| Independent natural reference spectrum |R07 is same basis; R08 target spectrum is not eligible | BLOCKED for independent robustness only |
| New model/training/distance |0/0/0 | Conformant |

Internal repair ledger: one independently written norm audit initially misread `CC_all_native` as unscaled; source shows it already includes RMS. Comparing saved GPU-FP32 norms with recomputed FP64 norms then exposed relative1.32e−7 rounding. The corrected audit uses the standard1024-term FP32 accumulation bound, not a scientific-effect tolerance; no decoder, membership, metric or result changed. A coding indentation error was caught before execution of that revision. Coverage audit also caught3 members active only in development: the all-zero flag was corrected from discovery+heldout to ALL splits (789 total). The frozen set/context recurrence criterion did not change. Actual image inspection caught an unset symlog transition and crowded legend; set linthresh=.001, correct count labels and re-render. Tail-trimmed/front-dimensional-share and top5-token concentration are labeled additional descriptive diagnostics, never selection criteria.

## Files, replication and bounds

Execution root: /data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030. Source hashes: provenance/source_manifest.json. Primary tables: tables/master_members.csv,frequency_counts.csv,member_spectrum.csv,group_pc_spectrum.csv,group_reconstruction_energy.csv,context_effects.csv,context_categories.csv. Full execution-only tables include all_dictionary_screen.csv,old_new_list_mapping.csv,token_member_summary.csv,high_response_token_counts.csv,context_family_pairs.csv. Raw sparse z,PC basis/full feature projections,paired arrays,bootstrap and matched IDs stay execution-side. Five main images and four appendices have explicit payload_manifest.json. No raw/checkpoint payload, no old result replacement and no publication.

Reproduce with the local spectral-hier Python: scripts/analyze.py --output /tmp/r10_reproduction_unique (copies the frozen config; requires accessible registered source caches), then scripts/refine_background.py --output /tmp/r10_reproduction_unique, scripts/render.py --output /tmp/r10_reproduction_unique and scripts/audit.py --output /tmp/r10_reproduction_unique. Each script accepts the same output root; no source edit is required. The reproducibility entry is also in README.md; no forward/training import is present.

Coverage totals: five cache-supported groups DONE_EXPLORATORY; numerical checks DONE_VALID; pure-B and independent-spectrum robustness BLOCKED only for those claims. Completion means the available analysis is delivered, not those missing measurements were run. One next researcher decision: assess these bounded conceptual updates and separately decide whether the48-forward target-only supplement is warranted. Stop without expanding.

## Final delivery checks

Static CPU read verified the actual A22 checkpoint SHA09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628 and exact equality of all cached model-scale block27 decoder coefficients to TRAIN_RMS27 times checkpoint decoder. No model constructed/forwarded. All local deliverable links and eight-section/balanced-math Anchor checks pass. Input207-file and execution output manifests match bytes. Navigation checker has38 issues vs37 preexisting: the new child is registered in anchor_ownership and linked from Focus/day/reading entry; its derived research-map entry remains pending. Existing research Graph was outside this request. See provenance/navigation_check.txt; this does not alter scientific measurements.

## 2026-10-30 near-domain/token factual supplement

The [supplement](../../../../../../../../UNAVAILABLE.md) separately freezes31math/24biology,strict14/15,within parent960.Heldout near retention19/21,strict8/13;all original IDs remain.High-response composition has25/18supported members.Exact-ID matching,unmatched states,blind prior-window proposals and separate posthoc referent blanks are saved.18independent cache/denominator/freeze/document-pair audit categories pass.Three main figures and their actual display were inspected.Human semantic review PENDING;rule proposals are not scientific semantic results.

Actual assets`analysis_a15_27_r10_token_context_audit_20261030`and`analysis_a15_27_r10_near_domain_token_context_20261030`pass the[current selected access check](../../../../../../../../sources/assets/checks/2026-10-30_r10_near_domain_outputs_20261030T0445Z.json).New presentation directories retain input/output manifests;selected evidence is infigure_variants/near_single_domain_20261030.The old speaking brief is retained byte-for-byte with a hash receipt;the current brief integrates new results.No forward/training/PCAfit.Scientific acceptance and source/annotation limits remain unchanged.The existing38navigation issues were not turned into measurement failures or automatic Graph edits.


## Pooled simple figures (2026-10-30)

The user requested pooled domains and less plot text.[New derived reading](../../../../../../../../UNAVAILABLE.md)keeps original55/29sets and separately describes16all-cached-zero-opposite members(7/9),not independent heldout confirmation.Token categories add explicit all-cache input coverage;old discovery-frozen categories remain unchanged.Nativez>0main views and frozenp90appendices have separate type/position denominators.No forward/training/PCAfit.Old brief bytes preserved.
