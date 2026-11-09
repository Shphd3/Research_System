# R03 delivery manifest and evidence lineage

This index separates complete files, qualified measurements and unresolved scientific questions. Read the [Summary](summary.md), [Detailed](detailed.md) and [figure guide](figures/README.md). The [machine-readable inventory](artifact_manifest.json) records paths, bytes, SHA256, artifact roles and budget. Raw arrays, JSONL, large tables, code and PDF files remain execution-side.

## Freeze, budget and identity

The contract froze at 2026-10-27 01:40:58 UTC, before new R03 forward calls or activation statistics. All 37 frozen sources matched after computation. A later factual Focus update archived the exact pre-run bytes; the Protocol, Anchor, texts, selectors, analysis code and thresholds are unchanged. See the [freeze](provenance/pre_analysis_freeze.json), [37-source check](provenance/final_frozen_source_check.json) and [factual-update receipt](provenance/factual_focus_update.json). R01/R02 records are preserved.

36 panel calls + 2 cache replays + 2 identical replays + 8 fixed-prefix checks = 48. Added to the parent endpoint 1452, this exhausts 1500/1500. Another 36 of 72 planned texts are NOT RUN. Training, intervention and new allocation counts are zero. No sealed TEST, deletion, commit or publication occurred. The [execution certificate](provenance/execution_certificate.json) records runtime, qualification and post-run disk-weight hashes.

Model SHA256: `cd2a512003e2f9f3cd3c32a9c3573f820bb28c940f73c57b1ddaa983d9223eba`.

Dictionary SHA256: `09b432e98dd7426f9ea4170809d75068a2ada2ed38c1e97d3fa18e119cd79628`.

Panel SHA256: `57c1d0358b5128a116128f73514d6d855454bdb689e706c941ed76f6a27e01b9`.

## Artifact roles and production

| Artifact | Purpose / criterion | Execution source | Producer / inputs | Completion and claim eligibility |
| --- | --- | --- | --- | --- |
| Frozen design and exact selectors | Pre-analysis identity before new R03 statistics | [pre_analysis_freeze.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/pre_analysis_freeze.json) | /root; 37 files, UTC freeze; Focus frozen bytes archived before factual update | COMPLETE; no post-result threshold change |
| Original O definition and evidence | Retain original same-token graph | [audit/original_graph_audit.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/audit/original_graph_audit.json) | original A15_25 sources, hashes and current cache access | COMPLETE; semantic parenthood not validated |
| Reference matrix and counts | 512 uniform IDs, D/V 64 contexts each | [results/selected_binary.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/selected_binary.npz) | offline/coactivation.py + frozen config; 65464/65484 rows | BOUNDED; missing document/sentence IDs |
| Rates and uncertainty | Counts/N; context bootstrap descriptive only | [results/feature_frequency.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/feature_frequency.csv) | same dictionary/gate/precision cache; 2000 context resamples | BOUNDED finite corpus, not population frequency |
| Raw/corrected graphs and groups | R conditional >=.8; C delta >=.05; support gates | [results/observed_graphs.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/observed_graphs.json) | all supported pairs, max symmetry, greedy modularity resolution1,min3 | COMPLETE within fixed 512 coordinates |
| All edge estimates | Preserve support, conditional, delta, V and interval fields | [results/edges_D_frozen.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/edges_D_frozen.csv) | counts -> exact directed metrics -> descriptive context intervals | BOUNDED intervals; adjacent tokens not independent trials |
| Original O base-rate diagnostics | Post-freeze descriptive audit, not a new tuned test | [audit/original_O_frequency_edges.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/audit/original_O_frequency_edges.csv) | audit/summarize_original_O.py; all 214711 D edges | BOUNDED; delta ceiling limits high-frequency detection |
| Complete randomized reruns | Exact column counts and row L0, 199 draws | [results/null_draws.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/null_draws.jsonl) | offline/coactivation.py + switch.cpp, 4 chains | COMPLETE; finite MCMC diagnostics, not perfect independence |
| Frequency comparison verdict | Stable/supported groups in observed and null | [results/null_results.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/null_results.json) | 0/199 nulls with eligible groups, p/q NA | INSUFFICIENT; never substitute zero/inf for absent group |
| Token/position stratification | Fixed token and position strata | [results/covariate_adjusted_association.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/covariate_adjusted_association.npz) | frozen stratification minus within-stratum independence expectation | BOUNDED; text types/docs unavailable |
| All texts, candidates and pairings | 12 constructed scenarios, 72 tokenized texts frozen | [panel/tokenized_sequences.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel/tokenized_sequences.jsonl) | panel/build_panel.py + finish_panel.py; no feature-result exclusion | 36 MEASURED, 36 NOT RUN due to parent cap |
| Forward ledger and certificate | Charge attempts before calls; maximum48 | [provenance/execution_certificate.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/provenance/execution_certificate.json) | run_forward.py; 36 panel +2 cache +2 replay +8 prefix | COMPLETE; cumulative1500/1500 |
| Native decoder scales | Keep raw z, per-layer and concatenated native norms | [forward/decoder_geometry.npz](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/forward/decoder_geometry.npz) | existing checkpoint/TRAIN rms, no fitting | COMPLETE; shared z is not independent per-layer activation |
| Panel activations and output readouts | Causal visible prefixes, same-token direct pairing | [forward/panel_readouts.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/forward/panel_readouts.jsonl) | 36 sparse sequence NPZs; readout candidate IDs fixed | BOUNDED compatible-candidate probabilities only |
| Measurement qualification | Frozen cache/prefix/replay and reconstruction guards | [forward/panel_qualification.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/forward/panel_qualification.json) | finite fixed positions; cache up to1.936% relative error | PASS within tolerance; does not repair R02 E16 failure |
| Near/far effects and member support | Pre-panel D/V-qualified group union; case blocks | [panel_analysis/results.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel_analysis/results.json) | offline/panel_analysis.py; exact64 sign flips,2000case bootstrap,IUT/BH2 | C03 far bounded support; R union empty, NA |
| Case outputs and sparse dominance | Do not infer comprehension from feature change | [panel_analysis/member_support_dominance.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel_analysis/member_support_dominance.csv) | fixed6cases;1–5/72 members change; candidate_outputs.csv | DESCRIPTIVE; only S01 both meanings compatible |
| Naming evidence | D first32 naming, later contexts descriptive | [naming/naming_groups.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/naming/naming_groups.json) | offline/name_groups.py; multiple members/prefixes/boundaries | MIXED_CONTEXT_CANDIDATES; no fresh blind validation |
| Per-token graph projections | Fixed sentences, all positive coordinates saved | [panel_analysis/fixed_sentence_token_projections.jsonl](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel_analysis/fixed_sentence_token_projections.jsonl) | actual token prefixes, native norms, frequency, fixed groups/O edges | INSTANCE DESCRIPTION; not cluster stability |
| Central graph/distance figures | Draw source estimates without refitting | [figures/graph_distance_plot_provenance.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/figures/graph_distance_plot_provenance.json) | offline/render_graph_distance.py;6PNG/PDF total across renderers | COMPLETE actual artifacts inspected |
| Original token figures | Keep frozen pooled-max display rule and its failure | [figures/token_figures_provenance.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/figures/token_figures_provenance.json) | offline/render_token_figures.py; target displayed rows all0 | DISPLAY FAILURE RETAINED, not absence of response |
| Target details | Explicit posthoc illustration only | [figures/target_detail_figures_provenance.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/figures/target_detail_figures_provenance.json) | offline/render_target_detail_figures.py; target top12,shared color | POSTHOC; all12 outside512, no C03 membership claim |
| Historical replacement audit | Link actual hook/position/dose only if comparable | [audit/existing_intervention_audit.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/audit/existing_intervention_audit.json) | source-only audit; no current replacement performed | NOT CURRENT FUNCTIONAL EVIDENCE |

Exact hashes, sizes and surfaces are in the inventory. The original graph/cache and CrossCoder are reused; new code adapts offline statistics and rendering without training.

## Decision-bearing lineage

| Question | Frozen comparison | Source | Observation / aggregation | Eligibility and verdict |
| --- | --- | --- | --- | --- |
| Original base-rate explanation | Conditional probability versus destination baseline | [original_O_frequency_summary.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/audit/original_O_frequency_summary.json) | 57.7045% delta<.05;21.038% nonpositive; high-p ceiling | Descriptive compatibility, not causal decomposition |
| Organization beyond margins | Full null pipeline preserves counts and row L0 | [null_results.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/null_results.json) | C2792 vs null median108,max137;~70% V threshold replication | Bounded subgraph support; document identity unavailable |
| Within-group frequency similarity | Same group/qualification pipeline on all nulls | [null_results.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/null_results.json) | 0/199 valid nulls;p/q NA | INSUFFICIENT; missing group is not zero |
| Low-to-high links | Support gate also applies to low-rate nodes | [feature_frequency.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/results/feature_frequency.csv) | All124positive bottom-quartile nodes fail200hits | UNESTIMABLE, not absent |
| Far-context response | Fixed C union relevant-minus-unrelated changes | [results.json](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel_analysis/results.json) | 6/6positive;mean.160037,CI[.039337,.320294],q=.03125 | BOUNDED response; edit extent/order remain rivals |
| Group meaning or comprehension | Member dominance and candidate checks | [member_support_dominance.csv](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/panel_analysis/member_support_dominance.csv) | Only1–5/72change percase;onlyS01bothcandidatescompatible | No joint group semantics,expert or comprehension claim |
| Two-clue integration Q3 | No new four-combination integration panel in R03 | [summary_cn.md](/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R02_frequency_distance_integration/summary_cn.md) | R02 remains insufficient; CC does not repair E16 failure | UNRESOLVED; far response is not an integration test |

## Conformance, deviations and gaps

| Contract | Actual completion | Eligibility impact |
| --- | --- | --- |
| Freeze before new response | 37 sources frozen; later O summaries/target details are descriptive | Posthoc items are not confirmation |
| At most72texts and stricter parent cap | Six complete cases/36calls;36others NOT RUN | Unmeasured is not negative |
| Preserve O; fixed R/C and full null reruns | Completed199reruns | No qualified null groups means frequency NA |
| Sentence/document intervals | Reliable original IDs unavailable; context sensitivity only | No fabricated population CI |
| Match native precision/cache | Base batch16→1; max z relative difference1.936%,within frozen gate | Approximate, not bit-exact replay |
| Fixed token display | Whole-sequence top12first-token dominated,target all0 | Failure retained;target detail posthoc only |
| Near/far clues | Target/length/suffix matched; neutral filler relocated | Order/recency confounded |
| Unrelated edit | Weekday changed,semantic edit changes more words | Relation-specific semantics not isolated |
| Naming validation | D first32names;later D/reusedVdescriptive | Mixed-context candidates only |

The interrupted original-O CSV writer retains `original_O_frequency_edges_attempt1_partial.csv`; the completed output is separate. The first naming environment lacked transformers; rerunning in the existing matched environment succeeded. Both engineering attempts remain logged and do not alter scientific selection. Artificial tensors test implementation only.

## Assets, data locations and unresolved questions

[Asset IDs and access snapshot](/data/250010109/Research_System/assets/same_token_coactivation_r03_20261027.md) · [Selected evidence copy manifest](selected_evidence_payload_manifest.json).

Execution root: `/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation`. [Full inventory](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R03_same_token_coactivation/artifact_manifest.json). PDF companions, all72texts,36sparse caches,complete edge tables,199nulls and all-member examples remain here. Six PNGs and five small tables are hashed selected-evidence copies; originals are retained.

Distinct gaps are very-low-rate support, absent qualified frequency-null groups, unavailable document/sentence units, distance/order confounding, unmatched edit extent, and uncertain naming/function. They are not a single failed test. The sole follow-up question is at the Summary end and was not run. Mechanism acceptance and closure are Unknown. Local synchronization is not publication.
