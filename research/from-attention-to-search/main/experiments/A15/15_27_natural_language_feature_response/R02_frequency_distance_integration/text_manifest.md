# R02 text manifest: construction, pairing and positions

All12 scenarios are constructed natural language with controlled edits. Exposed R01 discovery/holdout material is discovery here. New wording/entities were selected before new responses. The new panel failed prefix numerical qualification and is not confirmatory evidence.

Each case has00/10/01/11 × short/long plus11_short_position_control and11_short_unrelated (10sequences). Baseline00 changes only clue1 in10,only clue2 in01,and both in11. Distance is the token gap from the end of clue2 to the final target; clue1 gaps are separately recorded. Near/far final length,position and last5tokens match. Early near/far positions differ; stage analysis uses short only. Direct comparisons require the same token. All positions are zero-based.

| Case | Relation | Entities | Short readout positions | Long readout positions | Cue2 short/long gap | Continuation candidates |
| --- | --- | --- | --- | --- | --- | --- |
|B01|word_sense_selection|Wrenford|90,106,111|48,64,111|6/48|' swims', ' sounds'|
|B02|word_sense_selection|Oakmere|92,106,111|50,64,111|6/48|' swims', ' sounds'|
|B03|word_sense_selection|Hillcross|99,115,120|57,73,120|6/48|' swims', ' sounds'|
|B04|word_sense_selection|Pinevale|93,108,113|51,66,113|6/48|' swims', ' sounds'|
|B05|word_sense_selection|Ridgehaven|95,109,114|53,67,114|6/48|' swims', ' sounds'|
|B06|word_sense_selection|Fairbridge|92,106,111|50,64,111|6/48|' swims', ' sounds'|
|P01|person_attribute_binding|Westhaven, Alice, Ben, Clara, Dylan|117,131,136|75,89,136|7/49|' Alice', ' Ben', ' Clara', ' Dylan'|
|P02|person_attribute_binding|Elmstead, Olivia, Oscar, Emma, Jack|118,132,137|76,90,137|7/49|' Olivia', ' Oscar', ' Emma', ' Jack'|
|P03|person_attribute_binding|Brookstone, Nina, Noah, Lily, Luke|119,133,138|77,91,138|7/49|' Nina', ' Noah', ' Lily', ' Luke'|
|P04|person_attribute_binding|Northwick, Grace, Henry, Julia, James|119,133,138|77,91,138|7/49|' Grace', ' Henry', ' Julia', ' James'|
|P05|person_attribute_binding|Clearwater, Anna, Adam, Laura, David|119,133,138|77,91,138|7/49|' Anna', ' Adam', ' Laura', ' David'|
|P06|person_attribute_binding|Meadowbank, Rose, Ryan, Sofia, Simon|118,132,137|76,90,137|7/49|' Rose', ' Ryan', ' Sofia', ' Simon'|

Word-sense targets are bass/ID21529; person-binding targets are is/ID374,analyzed separately. Bass continuations are sense-compatible readouts,not unique correct next tokens. Stage1 uses only the candidates allowed by the visible prefix. Basic cases retain all variants together across template/source/entity groups. Bass was already exposed in R01; no new-response selection occurred.

[All120 texts,tokens,offsets,clues,candidates and pairs](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/panel/tokenized_sequences.jsonl), [case originals](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/panel/qualified_cases.jsonl), [pre-response exclusions/edits](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R02_frequency_distance_integration/panel/exclusions.json), and [text qualification](provenance/text_qualification.json). Text SHA256:`a172212a9f7840ca63a8e84324a5ba01dde129083e80b8ddaae196713eb3e203`. Raw JSONL remains execution-side.
