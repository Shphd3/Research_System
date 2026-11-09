# S02: animal/cat/dog native continuation only

Authorized by the current direct user request. Complete only this bounded step, then wait for joint review. It follows S01's format/answer preference problem without rewriting S01 or any H1–H4hypothesis.

Purpose: determine whether the same frozen0.6BBase changes continuation preference when the body explicitly changes cat↔dog.6paired English contexts/12texts, labels animal+cat or animal+dog. Only literal fine-class word changes within each pair; varied sentence/context across6families. No prediction-based selection. All text/labels/prefixes/candidate tokenizations freeze before responses.

One fixed suffix, exactly newline+'The animal is a'. Candidate order/text exactly ' cat.' and ' dog.', including initial space and final period. Actual concatenated tokenization must preserve prefix token IDs; record all candidate IDs/counts. One property-free-with-respect-to-cat/dog neutral body 'An animal is mentioned in this note.' uses the same suffix/candidates, diagnostic only, excluded from accuracy. No alternative prompts, calibration or candidate changes.

Use the same official Qwen3-0.6BBase/tokenizer hashes asS01, FP32CPU2threads, no chattemplate or specialtokens/EOS. Fixed4x192physicalshape with2candidate lanes repeated for numeric checks. Score every candidate token including period, FP32logsoftmax and FP64sum. Choose max total without length/prior correction, exact ties use frozenorder and are recorded. No training, classifiers, dictionaries, feature hooks/storage/analysis, or intervention.

Report all12texts and exact prefixes/labels/candidates, full rawscores/token IDs/counts, delta=S_cat−S_dog, chosenlabel/correct; cat/dog counts outof6; all6pair changes and correct-direction changes separately; neutral totals/preference; all errors (explicitlynoneifnone) plus at leastonefullpair. Independently replay token sums/argmax/counts and verify S01hashes unchanged.

This checks constrained continuation sensitivity to explicit animal words. Success may be copying; it does not identify abstraction, feature organization, causal use, generalization or performance improvement caused by a single change from S01. No extra concepts/data, hypothesis revision, automatic next step, commit/push/publication. Researcher judgment and next decision remain pending.
