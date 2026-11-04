派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/protocol.md`。
[精确原始文件](../../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R17_20261102_feature_composition_v02/diagnostics/R17_D1/controlled_steps/S08_dataset_support_overlap_1104/protocol.md)；研究修改仍回到原件。

---

# S08 Protocol: within/cross dataset SAE support overlap

APPROVED_FOR_BOUNDED_EXTRACTION_AND_STATISTICS by current direct user request. The existing H1 owner15_27_06 supplies the member-overlap question. This is a new natural-dataset robustness round, not a new hypothesis of domain knowledge. No model/SAE/readout training or functional interventions.

## Data and object

Actual readable cached Magicoder-OSS75K problem(train), GSM8K question(train), MMLU question(test), as exact Arrow files/revisions/SHA in data/sources.json. Exclude Magicoder solution/seed and MMLU choices/answer; no prompts/chat wrappers or answer suffixes. Neither Numina nor the senior exact SFT path was found in the bounded recorded locations. Continue the three available sources; do not claim senior replication. Historical E18 caches lack this exact two-hook/document/position binding and are not reused.

Deduplicate full question text by NFKC+casefold+collapsed whitespace hash; retain original internal formatting for inference. Remove all occurrences of exact normalized cross-dataset duplicates symmetrically; within-dataset retain first source row. Seeded uniform rejection sampling requires>=16token questions, selecting 257per dataset. Available source counts refer to complete deduplicated text pools; token length eligibility is checked on uniformly shuffled candidates until quota, not falsely claimed for every corpus row. Save all IDs, source rows, texts, exclusions, full/visible lengths and actual tokens/offsets.

Use the same verified official Qwen3-0.6B Base and two separate native30000/ReLU-Top32 dictionaries. Attention hook=zero-based block27.o_proj output before residual addition; MLPIN hook=actual block27.mlp input after residual/post_attention_layernorm. No input renormalization or decoder-bias subtraction. Active iff native z>0; same feature IDs across dictionaries unrelated. Frozen FP32 CPU2threads, physical8x128, no output scoring.

For each question use first min(full_length,128)tokens without special tokens. Sample8positions floor((j+.5)*visible_length/8),j0..7; min16makes them distinct. No suffix. Keep all selected tokens as one document cluster. Also capture absolute position31when available, excluded otherwise. Each position is causal prefix-only; later tokens cannot affect it. Check full-window vs truncated32state equivalence at this position and a hook no-op before scaling.

## Metrics and pairing

Per token pair J=|support intersection|/|support union|, binary only. Main document-pair kernel averages8same-quantile-position Jaccards. Within each dataset use all distinct unordered pairs; cross-domain use cyclic offsets1..(N-1)/2 in pre-fixed hash order. Odd N gives exactly N(N-1)/2distinct pairs for A-within,B-within,cross; no within self pair. Cross graph has equal document degree. Report original unique pairs and8position comparisons, not independent sample counts. Save explicit pair IDs.

Report A-within,B-within,cross, A-minus-cross,B-minus-cross and pooled average-within-minus-cross.1999document bootstrap resamples independently in A/B; all original edges involving a resampled document get multiplicity count_i*count_j, same weighting for all its token positions. No token/edge bootstrap.999whole-document label permutations, plus-one p; reapply same balanced pairing rule to each relabeling. This tests source-label association under whole-document exchangeability, not causal semantic content. Main6pooled tests (3pairs x2dictionaries) Holm.05; preserve each side even if pooled is positive.

## Controls, amplitudes and limits

Pair-specific length controls match exact counts in frozen full-question token bins16/32/48/64/96/128/192/256/512/1024/2048+, selected before activations; oddify by removing one from the same bin in both groups. Same text part and8positions remain. Length-null permutes whole documents within bins, retaining counts. Fixed31control uses equal odd document counts from questions with>=32tokens, same32-token causal prefix, all else fixed. Literal-token control uses up to3tokens selected before activations by minimum document coverage>=20/source; average only same-token pairs among sampled positions within each document pair. Missing matching pairs remain missing, coverage and effective document counts reported; bootstrap document clusters, no label-permutation claim for this conditional control. These controls are exploratory and cannot rescue failed main tests.

Supplement: shared-coordinate raw RMS amplitude difference=sqrt(mean over shared positive members of(z_i-z_j)^2) per aligned position, then average eligible positions/document pairs; report coverage and whole-zL2. Separate from Jaccard. Publish frequent tokens/punctuation, newline/code/question-mark rates and full/visible-length distributions. Dataset source, topic, language, code format, task structure, near duplicates and128token truncation remain alternatives to domain-knowledge interpretation. MMLUsubject mixture is not homogeneous. No claimed training-unseen split or task accuracy.

## Outcome and delivery

Support only the bounded statement that within-source activations are more similar if both side differences have positive95%document intervals and the pooled Holm test passes; report local/asymmetric/reversed cases. Persistence/shrinkage under controls narrows interpretation, not uniquely identifies a cause. Wide intervals, matching loss or missing datasets are insufficient, never fabricated negatives. Statistical thresholds are AI operational choices frozen before activations within the user's delegated scope, not researcher mechanism approval. Scientific acceptance/closure Unknown.

Sequence: source/asset audit→text/sample/control freeze→dual-hook capture→all dataset-pair/SAE metrics and document uncertainty→controls/format/amplitude→independent numerical audit and plots→bilingual result, concise daily meeting report and review package. Old S06/S07 untouched. Reuse native model/SAE loaders and adapt extraction, write this dataset/document-pair analysis separately. Record code/data hashes, actual resources/time and any amendment without replacing initial protocol. No commit/push/publication. Exact registered definitions in frozen_plan.json; freeze UTC 2026-11-04T01:07:11.265822+00:00.
