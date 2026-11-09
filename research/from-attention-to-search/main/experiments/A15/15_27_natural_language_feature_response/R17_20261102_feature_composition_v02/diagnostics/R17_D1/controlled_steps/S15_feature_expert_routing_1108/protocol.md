# S15: frozen feature groups and actual MoE expert routing

Status: APPROVED_FOR_REUSED_DATA_INFERENCE_AND_STATISTICS by the user's current direct instruction. The supplied original attachment is preserved under sources/. Its older phase-A wait is superseded by this direct approval. No training, weight changes, routing intervention, new text generation, new paid resources, or independent confirmation is included. No new Focus/Anchor or scientific acceptance is created. This bounded supporting analysis follows R17_D1/S14 on the existing A15 natural-language feature line; historical Anchor questions and S11/S13/S14 verdicts remain unchanged.

## Purpose, rival and claim

Measure whether DEV-defined common and category-biased dictionary members have stable conditional expert-receipt profiles in the actual trained MoE. The rival is token/category/template/length composition and expert load, rather than a feature-specific organizational principle. A token is routed as a whole; 32 active members inherit the same top-2 record. Observational correspondence does not establish expert utility, independent feature routing, gradient interference, or learning efficiency.

## Assets and data

Use the exact matched ordinary8-layer MoE33B and its block7.norm2/router-input SAE (1024/30000/ReLU-Top32). Preserve FP32 model/SAE weights and load_bias, evaluation/inference only, TF32 disabled. Native route uses softmax(logits)+load_bias to choose8E/top2; the two selected original softmax probabilities are renormalized for expert weights. No capacity truncation or shared expert.

Reuse S14's6912 S13 prefixes, original IDs/tokenization,24DEV families/8scene clusters and48CONF families/16clusters,24labels,4wordings. Both text and previous CONF responses have been exposed. Main inference is explicit wording at the final Description: colon; named rephrasing and attribute/scenario each remain separate. Attribute/scenario and any explicit pair failing inherited .75 sibling behavior remain descriptive. Also retain the original final-body-token position as sensitivity; no best-position search. Q/G are the exact matched S14 own-SAE6000/6000 reference counts. All input access IDs and hashes are preserved.

## Selection before routing

Shared candidates: identical to S14 DEV explicit pair intersection frequency>=.75. Biased A/B candidates: DEV marginal-rate difference>=.25 toward that side and signed mean difference in>=6/8scene clusters. Both are fixed per pair; overlap is allowed. Universal control:>=.90 of DEV explicit24-label panel. All30000 coordinates can participate, with full encountered-member screening exported. Biased thresholds are transparent pre-routing technical defaults completing the attachment's unspecified numbers, not a claim that the user individually approved those exact historical values. The current user authorized completion under the bounded analysis. No outcome-dependent tuning follows.

Matched random-member pools exclude all selected members of the pair; require DEV pair-pooled rate>=.125, absolute gaps<=.10 for Q reference frequency,G reference frequency,and pair-pooled DEV rate; retain nearest32 by squared gap, tie by ID. Draw1000 no-replacement member sets using only these fixed pools. Empty pools remain insufficient; no caliper relaxation. Match diagnostics expose gap/support limitations.

## Frozen primary estimands

Represent actual membership as route mass r_e/2 (sums1, while raw inclusion probabilities sum2); actual gate mass is a separate sensitivity. For a feature and category, p_f,c(e) is the mean route mass at positions where that feature is positive. Category load is the mean over all48 frames. Zero occurrence is NA.

Q1: average TV(p_f,c,category load) over unique fixed(feature,label) roles: shared candidates in both sides,A-biased in A,B-biased in B. Export every selected member on both labels, expert-wise inclusion/mass/load/difference and uncertainty; low-coverage cross-side rows are retained. Q2: equal shared-member mean TV between its A and B profiles. Q3: TV between equal-member average profiles of A-biased on A tokens and B-biased on B tokens; these are distinct tokens. TV is half the L1 distribution difference, in[0,1]. Baseline group composition and expert mixture are also exported.

Use>=12/48 observed frames and>=8/16scene clusters per feature-label as adequate coverage. At least80%of planned relevant roles must meet this rule for a group-level inference; raw estimates and missing/low-support members remain visible. Bootstrap intervals are raw-statistic sampling intervals, not causal or null-corrected effects. Five percentage points of excess TV is a pre-outcome display screen only, not a scientific utility criterion.

## Resampling and multiplicity

Seed2026110815;1000 permutations and2000 shared scene-multinomial bootstrap draws. Preserve all3family slots,24labels and4wordings in each scene record. Global null permutes whole scene blocks, family slots within each mapped scene, and one common24-label-role permutation. It preserves all actual expert pairs/weights/load but can break category composition. Conditional null maps whole scenes within prefix-length bins, preserving category/wording roles and hence class loads. Length cutoff is the DEV scene-mean median; merge sparse bins if any CONF bin contains<4scenes, and report lost conditioning. Family-slot permutations are common across all labels/wordings. These exchangeability assumptions are exploratory; they do not create randomized causal interventions.

For each question, Holm8 across the eight fixed pairs; also report Holm24 across allthree questions. Member-level Q1 corrections cover all primary explicit-colon selected member/category tests; expert differences have simultaneous8expert bootstrap max-deviation bands. Report p minimum1/1001 and valid draw counts. Matched member draws provide a descriptive control distribution, not calibrated permutation p-values. The main status is conditional association, global-only association, unresolved or insufficient; failure to reject is not no organization. Formal independent new-scene confirmation is NOT RUN because it was not separately approved.

## Implementation, budget and order

Existing local H100 MIG3g40GB only; no resource submission. FP32/batch16,12GiB ceiling,1800s forward ceiling. Reuse mounted tokenizer dependencies; no training-environment modification. First verify all token IDs, observed norm2=actual router input, exact native route formula, batch/single error<=1e-4 and unchanged Top32/routes; calibration mean normalized reconstruction error<1. Stop dependent collection on failure, retaining logs. Extract only6912 prefix forwards, both preselected positions; no repeated Q/G model forward. Record every row's actual full8logits/probabilities,2IDs/weights,32feature IDs/values,1024hidden vector and quality. Compare the entire new Top32 cache against S14 without substituting it. Parameter version counters and load_bias must remain unchanged.

Selection/config/input hashes precede collection. Statistics code and complete resampling plan are frozen before any routing statistic is inspected. Complete main/secondary analyses, independent row-level route/SAE/statistic replay, cases, tables, figures,coverage ledger and bilingual factual summaries. Statistical missingness is not replaced with0. Preserve implementation failures/amendments; do not rewrite scientific metrics after viewing outcomes. Human scientific judgment and next experiment remain pending. Only one AI next-test proposal is delivered, with no automatic training.
