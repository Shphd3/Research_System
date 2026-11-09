# S03 protocol: explicit animal/cat/dog membership and relative strength

## Purpose and authority

APPROVED_FOR_BOUNDED_S03 by the current direct user request, 2026-11-03. The user specifies the question, 24 rows, two frozen SAEs, exploration/check split and descriptive scope. Operational thresholds below are AI implementation choices within this scope, not researcher scientific acceptance. Stop after tables, figures, bilingual records and a <10,000,000 byte discussion archive in today's daily folder. No training, probe, intervention, CrossCoder, H3/H4, hypothesis revision or next experiment.

This small observation step follows S02's 12/12 native continuation result and the existing H1/H2 owners (15_27_06 / 15_27_07). Those original hypotheses remain unchanged: H1 concerns extra information from additional members; H2 concerns information from relative strength conditional on identities and total amplitude. This step measures only membership recurrence and relative response direction. It does not run the original functional-information tests.

## Data, sampling and immutable inputs

Keep all 12 S02 cat/dog bodies and complete prefixes byte-identical; copy their original scores without rescoring or filtering. Add P (explicit animal, fine class unknown) and N (explicit chair/non-animal), making six four-condition families. P uses object as referent and animal as class to avoid tautology. N uses object in its suffix for semantic consistency; all other suffixes retain S02's 'The animal is a'. Document every difference. This limits parent-vs-nonparent interpretation because the suffix itself changes animal/object. P is not a negative cat/dog example.

Before responses, freeze data and tokenization; F01-F03 exploration, F04-F06 heldout check. All four rows stay together. Read no generated answer. Observe the final visible prefix token (' a', actual ID and indices recorded per row), before predicting the next token. Both dictionaries use the same functional position; sequence lengths/absolute positions may differ and are reported. No continuation enters any capture.

Use the exact S02 official Qwen3-0.6B Base/tokenizer, verify hashes. Capture block27 self_attn.o_proj output BEFORE residual addition for ATTN_SAE; capture actual block27 mlp input AFTER residual addition and post_attention_layernorm for MLPIN_SAE. These are independent measurement interfaces, not MLP input/output or a causal before/after experiment. Both original native encoders use linear(x)+bias, ReLU, Top32 of 30000. No extra input normalization or decoder-bias subtraction; active iff selected z>0, with exact zeros. A positive preactivation excluded by Top32 is inactive under this rule. Save preactivations and cutoff32/33 to expose competition. Use each native loader and verify encoding equivalence.

## Fixed selection and quantities

For each dictionary, let z_i be raw activation, d_i the L2 norm of its own decoder column, u_i=z_i*d_i. u is individual decoded-direction magnitude, not vector-sum reconstruction norm or semantic contribution; directions need not be orthogonal. Record z, d and u, not just normalized values.

H1 common candidates: in at least 2/3 exploration families active in P,cat,dog together; in at least 2/3 exploration families additionally min(u_P,u_cat,u_dog)>u_N. Rank by triple-active coverage descending, positive contrast coverage descending, mean(min_PCD-u_N) descending, atom ID ascending. Keep at most 6; never fill a short list from check data. This is a candidate shared response, not proved animal semantics.

H1 added candidates: separately for cat and dog, require z_P=0 and z_fine>0 in at least 2/3 exploration families. Rank by this coverage descending, mean u_fine among these events descending, ID ascending; at most 6 per fine class. The opposite fine class and N are always reported but not eligibility gates. New in both fine classes is not class-specific evidence.

H2 candidates: require cat/dog jointly active in at least 2/3 exploration families. Rank by joint-active coverage descending, exploration mean min(u_cat,u_dog) descending, ID ascending; maximum 6. This ranking does not maximize cat-dog contrast. On this fixed list calculate q_raw=z_C/||z_C||2 and q_weighted=u_C/||u_C||2 for every row. A zero norm is undefined (null/gray), without epsilon replacement. Freeze each member's direction sign(mean_exploration(q_cat-q_dog)); absolute mean <=1e-8 is zero, undefined mean has no direction. Holdout reports every selected member's direction per family without reselection, including reversals, zeros, absence and undefined values. Report raw and weighted values, pairwise differences and ratios (undefined when denominator zero), plus original full/selected vector norms.

Record BOTH whole-dictionary support-equal cat/dog pairs and support-equal pairs on the selected list. The latter does not establish full support control. Selected-vector normalization removes that vector's scalar L2 scale algebraically; it does not equate all model amplitudes or identify additional predictive information.

## Stages, evidence and outcome branches

1. Prepare: audit grammar, labels, S02 text identity and exact tokenization, strict asset access, code/data/input hashes. Freeze this protocol and machine-readable plan before capture. No model-response selection of text.
2. Extract ONLY exploration. Native-loader equivalence and hook-noop checks must pass; freeze exact candidates, relative directions and code hashes. Heldout extraction refuses to run without this receipt. No threshold/ranking change after holdout access.
3. Extract heldout once; compute all per-family membership transitions (P-cat, P-dog, P-N, cat-dog, cat-N, dog-N), retained strength changes and denominators. Report fixed-candidate recurrence, complete text/member/value cases, every failed candidate pattern, raw/weighted/relative heatmaps separately per dictionary and descriptive split counts. Then stop.

Supporting weaker observation: selected membership/relative directions recur in check families. Non-supporting weaker observation: absence, opposite direction or lack of N contrast; retain these failures. Insufficient: no eligible candidates, undefined normalization or too few same-support pairs. Six wording families are not statistical confirmation; report integer counts, no significance or population inference. Lexical copying, fixed suffix, object/animal referent changes, position, Top32 competition, fixed dictionary and reconstruction error remain rivals. No causal/model-use or extra-information verdict is made.

CPU FP32, two threads, fixed physical 4x192; FP64 offline analysis. Extra one no-hook forward per stage verifies captures do not mutate native output. Preserve S01/S02 hashes and all original R17 assets; output new S03 only. No GPU submission. Fail on asset mismatch, nonfinite output, native-rule mismatch, changed frozen inputs or overwritten result. A-G audit: user supplies scientific/data/scope boundaries; implementation choices above are explicit. No learning objective/optimizer applies. Scientific acceptance and next decision remain Unknown pending joint review.
