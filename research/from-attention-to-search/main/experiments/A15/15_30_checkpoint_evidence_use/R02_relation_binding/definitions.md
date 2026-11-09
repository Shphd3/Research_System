# Operational definitions of distance and evidence use

Distance describes an input, query and required evidence before model behavior is measured. Failure or slow learning is not part of the distance definition. The same word can be nearby evidence for one query and irrelevant for another; distance is not an intrinsic property of the word.

## Token endpoints and evidence spans

Use the unchanged Qwen tokenizer, with no BOS or chat template and zero-based positions. For a 1,152-token prefix, readout p=1151 predicts the first answer token at index 1152. Define gap=p−e−1, excluding both endpoints. The evidence-to-first-answer index difference is therefore gap+2. Tokenizer identity and SHA256 are in the [data guide](assets_and_data.md).

R01 uses the sole correct value's last token as e: 1134 near, 126 far. R02 keeps both answer words fixed across binding worlds and uses the final listed value B as the stable anchor e, again 1134/126 for anchor gaps 16/1024. The anchor is not always the queried value. Each row separately records the actual correct-value span/gap, full relation-block span/length/end-gap, absolute positions, total input length and final prediction index.

For actual family T1_F1, key/spoon occupy positions 1128/1134 near and 120/126 far in both worlds. Querying box gives correct-value gaps 22/16 near and 1030/1024 far across worlds A/B. The full block has 12 tokens and block-end gaps 15/1023. Across the panel, correct-value gaps span 16–24 and 1024–1032; relation blocks span 10–16 tokens. Every prefix plus generation allowance fits the 2048-token context without truncation. Anchor gaps 16 and 1024 are about 0.78% and 50% of that context, providing relative near/far labels rather than universal thresholds. Moving the relation block also changes absolute position and filler competition.

## Information task and counterfactual answer

Parse an entity–value map M and answer M[q] for the queried entity q. World A says box→key and bag→spoon; world B says bag→key and box→spoon. Both query box. Values retain frequency, order and token positions; query, filler and all other prefix bytes are identical. The answer flips from key to spoon.

Matching the queried entity and copying its corresponding value is allowed. A query-agnostic nearest-value, constant-prior or word-bag rule gives the same candidate in both worlds and cannot answer both correctly. Passing supports selection in these controlled texts; it does not require any particular internal algorithm. Fixed-query and entity lexical preferences remain partially confounded.

## Separate capability levels

| Level | Concrete example | R01 evidence | R02 coverage |
|---|---|---|---|
| Answer-word retrieval | Only “The box contains the key”; replace key with spoon and query box | Restricted candidate ranking on the constructed one-fact task; no free generation | Candidate-only FP32 reference of the original task |
| Object–attribute selection | Display both box/bag facts, swap entities while keeping key/spoon fixed, query box | Original controls do not establish reliable binding-specific selection | Primary controlled one-hop test; candidates and greedy answers reported separately |
| Paraphrase transfer | Independently freeze “The key was placed inside the box” after developing with “The box contains the key” | Multiple exposed templates do not constitute independent transfer confirmation | NOT RUN |
| Multifact composition | “The key is in the box; the box is in the drawer”; infer the key's drawer through both links | NOT RUN | NOT RUN; the competitor fact in R02 is not a second inference hop |

All 24 main families and six engineering families are R01-exposed. There is no new-family independent confirmation. Greedy first-answer-word correctness and restricted candidate ranking are distinct measurements.

## Distance versus exposure and long-tail knowledge

Distance is a relation in the current input. Exposure counts training presentations of a fact or pattern. A hypothetical controlled experiment could present the same fact five versus 1,000 times and cross that factor with near/far distance. This round manipulates neither exposure nor its interaction with distance; pretraining exposure to the selected facts/templates is unknown. Total training tokens describe progress, not per-fact exposure. Word frequency and SAE activation frequency are also different counts.

This round does not identify long range with long tail, train any model or dictionary, or automatically expand the experiment. It does not adjudicate another Base-student knowledge-learning experiment's startup qualification. The researcher decides whether and how to combine exposure and distance after reviewing the separate bounded results.
