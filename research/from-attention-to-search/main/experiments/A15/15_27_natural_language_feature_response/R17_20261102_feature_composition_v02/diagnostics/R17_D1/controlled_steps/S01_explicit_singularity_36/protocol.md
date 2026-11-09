# S01: explicit singularity, native behavior only

Status: EXECUTION_AUTHORIZED by the current direct user request. This is a first-step prerequisite check within R17_D1, not a feature hypothesis retest or a new Focus. Stop for joint review after reporting.

Purpose: establish a small readable object for square→singular-square concept refinement.12families×3independent descriptions=36Englishtexts, explicit square/singular-square/invertible-square; no determinant/rank or derived certificates. Square=True for all; singularity unknown/yes/no. Unknown means the text does not determine the property, not a contradictory fixed matrix.

Use the exact frozen official Qwen3-0.6B Base and tokenizer from D1. FP32 CPU inference, no optimizer or classifier. Scores adapt only the native sequence-scoring portion of D1; do not import Capture or load any dictionary. Model/source identity checked before execution. No old scores or data are pooled.

Two fixed Chinese questions and equivalent candidate sets are saved byte-for-byte in formats.json. F1 uses the researcher's exact question and order yes/no/unknown. F2 changes question wording and lists unknown/no/yes with equivalent full answers. All36rows use both. A single property-free neutral text is scored once per format. These are diagnostics of candidate expression/length/prior, not corrections. No further formats, examples or prompt search.

For each candidate c, sum log P(c_t | prefix,c_<t) over all answer tokens including the full stop, excluding prompt, EOS and masked padding. Score every candidate's actual concatenated tokenization; require prefix stability and no truncation. Primary argmax uses unnormalized sequence totals; no length/prior adjustment or temperature. Save exact prefix and candidate texts, all token IDs/counts, token logprobs, totals, preferred answer, margins and correctness. Fixed4×192physical shape;3candidate lanes plus duplicated first lane for a numerical identity check. FP32 model/logsoftmax, FP64 score accumulation.

All36labels and within-family matching are audited and frozen before model responses. Report both total correct/36 and each class/12, gold×predicted confusion, family-level agreement across formats, all36texts with both scores, and the first ID correct/error per class/format if such cases exist. If none, explicitly report absence. No inference of feature organization, native causal mechanism or broad mathematical ability.12constructed families are not a natural population sample; repeated formats are paired observations.

Bounded audits: identification—explicit text comprehension, not theorem inference; data/statistics—12matchedfamilies, no fitting/split, fixed2formats andneutral; implementation—frozenmodel/nohooks/nooptimizer, exacttokenboundaries, finite logprobs, token-sum and duplicated-lane checks. Outputdata and rawscores stay execution-side; project owns this Protocol/Summary/casebook.

Completion: deliver records, stop; researcher acceptance and next decision remain Unknown. Do not alter either format after responses. No subsequent feature analysis, training, intervention, other concept, commit/push or publication.
