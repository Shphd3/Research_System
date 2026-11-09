# Detailed evidence record: mean components and frequency routing

The frozen contract is the received [Chinese Protocol](protocol_cn.md), with the pre-result [numerical guard amendment](numerical_amendment_01_cn.md). The [complete Chinese Detailed record](detailed_cn.md) contains the coordinate derivation, conformance ledger, exact sources, negative outcomes and inspection history. This companion preserves the scientific decisions and measurement boundaries.

## Purpose, hypotheses, and controls

H1 concerns the positive signed contribution of frequent-feature average decoded vectors to the actual representation mean. H2 concerns whether persistent group score baselines participate in routing concentration. The key rival explanations are group cardinality, coactivation, within-band competition, and frozen-encoder distribution shift. Learning utility is a separate untested bridge. All strategies retain the same original inputs and membership; only routing information is changed.

## Objects and provenance

The final Qwen3 CrossCoder checkpoint has244,140 updates and999,997,440 paired positions. Actual model blocks2,4,…,28 correspond to zero-based indices1,3,…,27. Shared nonnegative z uses all14 layers and the saved TRAIN gate0.051281172782182693. The target is block28 residual-post, before the original final RMSNorm. Analysis covers85,548 TRAIN positions/1,024 dialogues and22,446 already exposed review positions/256 dialogues, aligned to answer-only next-token targets including EOS. DEV is unused. Original-document independence remains unverified.

The original coordinate restoration is hhat=o+s*b_dec+sum(z_i*s*D_i), with s=374.3495121024576. The preprocessing offset o is distinct from the current SFT TRAIN mean mu. Four positive TRAIN-frequency bands and two relation subgroups per band remain frozen; sizes are1,694/5,673/7,013/1,097, with907 TRAIN-zero features U. Relation subgroup sizes are1308/386,5670/3,1861/5152,1096/1. Every B1 feature has only1–17 TRAIN hits, all below20; no outcome-dependent reliability filter was added. They are candidate receiving slots, not established functional experts.

## Measurements and results

The signed coefficient alpha is dot(component,mu)/||mu||². TRAIN coefficients sum to1. The fixed-direction review coefficients sum to1.026570, because the review mean is not exactly TRAIN mu; renormalizing to one would change the definition. Explicit positionwise reconstruction independently checks the mean identity to2.27e-13/1.99e-13 maximum coordinate error. Feature direction cosines, actual mean projections, activation probabilities and conditional positive means are separately retained.

R0 chooses the band with largest raw contribution sum, then largest raw subgroup sum. R1 divides only the band score by its TRAIN mean. R2 subtracts the band mean and retains negative scores. R2b also subtracts subgroup means. Tie handling uses minimum ID and the common all-zero fallback is expert0; neither ties nor fallbacks occurred. R0/R1 exactly reproduced all old TRAIN/review assignments despite the prior hash tie rule. Manual event accumulation verified8,192 routes and5,120 feature/expert counts.

The complete results and intervals are in [Summary](summary.md), [mean components](tables/mean_components.csv), [loads](tables/expert_loads.csv), [paired strategy differences](tables/paired_strategy_differences.csv), [composition](tables/input_composition.csv) and [transitions](tables/route_transitions.csv). R2 selected the lowest band for26.70% of review positions, but5,233/5,992 of those positions contained no original low-band activation. Its macro target receipt was17.58%, versus72.22% for R1. The paired difference was−54.63 percentage points, with dialogue-bootstrap interval[−56.92,−52.18]. R2b filled all slots but reached16.86% receipt. The score margin decomposition is arithmetic, not a causal percentage attribution.

C re-ran necessary frozen forward passes at the original texts and batches, subtracting only the target-layer TRAIN mu before the unchanged joint encoding. Original final-layer h was bitwise identical at all107,994 positions. BF16 gate comparisons differed at28/26,299,223 TRAIN events and7/6,838,973 review events; original R0 routing differed atone TRAIN position andzero review positions. This is transparently recorded as bounded, not hidden by retuning thresholds. C had0% low-feature receipt; review MSE increased33.5877→61.9925 and activation count304.686→415.493. Reconstruction added back mu has the same paired error, and all diagnostics use the same raw coordinate units. Input-distribution mismatch limits mechanism interpretation.

## Uncertainty, cases, and omissions

All1,000 bootstrap draws resample complete dialogues, conditional on the frozen TRAIN lists, baselines and reference direction. No independent test claim is made. Unobserved low features remainNA; zero receipt is distinct from absence. Complete feature/expert q point matrices are saved for all10 split/strategy conditions; owner-low-feature q/r intervals, load, composition, transition, mean-projection and reconstruction-quality intervals are supplied. Intervals for every16384×8 q cell were not computed. The optional TRAIN-center similarity supplement was not run. Training loss, learning utility and capacity are NOT RUN.

Five main figures and one supplementary load figure are provided in PNG/PDF. The fixed complete Chinese natural-language dialogue was chosen by a predeclared SHA256 order, with all233 answer-prediction positions. Sixteen changed/unchanged case cards are hash-selected, including duplicate positions if shared across conditions. Future tokens are reading aids only; isolated byte-token displays do not define feature semantics.

## Execution, review, and next decision

This analysis used the existing8-core CPU quota and existing H100 MIG3g.40GB, without a new external task, installation, download or resource allocation. No Base, dictionary or expert was trained. The Base/tokenizer dedicated strict registry check was added after the C forward; initial strict checks covered dictionary, data, representation and predecessor analysis. This timing is disclosed rather than retroactively described as fully prechecked. Actual inputs, hashes, costs, failures and output registration are in [manifest](artifact_manifest.json), [receipt](completion_receipt.json) and [source-table index](tables_index_cn.md).

AI proposal: retain only R1 as the scoring hypothesis for a separately researcher-approved same-budget learning comparison with R0. More balanced load, higher receipt, spectra or coactivation are not evidence of learning gains. No next experiment is started; researcher judgment remains Unknown.
