# S02: animal/cat/dog native continuation

Observed12/12correct (cat6/6,dog6/6). Choice changes6/6pairs, both correct6/6, reversed0/6. Complete and stop for joint review; no hypothesis revision or next-step execution.

Six matched English context pairs differ only by explicitcat/dog; labelsanimal+cat/dog. One fixed newline+'The animal is a' suffix; exact candidates ' cat.'/' dog.'. Token IDs/lengths and neutral scores:

| candidate   | token_ids   |   tokens |   neutral_sequence_logprob |
|:------------|:------------|---------:|---------------------------:|
| " cat."     | [8251, 13]  |        2 |                  -5.834870 |
| " dog."     | [5562, 13]  |        2 |                  -5.656862 |

All26token concatenations frozen/checked before model responses. Same officialQwen3-0.6BBase/tokenizer hashes asS01, FP32CPU2threads, native full sequence logprob, FP64sum, argmax without length/prior correction, includingperiod and noEOS/chattemplate. No trained classifier, dictionary, feature capture/analysis, intervention, extra data or prompt search. Both candidates happen to contain2tokens; lexical priors and contextual/period probabilities still differ.

| class_label   |   correct |   N |
|:--------------|----------:|----:|
| cat           |         6 |   6 |
| dog           |         6 |   6 |
| all           |        12 |  12 |

| family   | cat_choice   | dog_choice   |   cat_delta |   dog_delta | choice_changed   | both_correct   | reversed_switch   |
|:---------|:-------------|:-------------|------------:|------------:|:-----------------|:---------------|:------------------|
| F01      | cat          | dog          |    2.781256 |   -1.895151 | True             | True           | False             |
| F02      | cat          | dog          |    3.640498 |   -2.930142 | True             | True           | False             |
| F03      | cat          | dog          |    4.782505 |   -4.198835 | True             | True           | False             |
| F04      | cat          | dog          |    4.295776 |   -3.825254 | True             | True           | False             |
| F05      | cat          | dog          |    3.135507 |   -4.452133 | True             | True           | False             |
| F06      | cat          | dog          |    3.825219 |   -3.709584 | True             | True           | False             |

Neutralprefix: 'An animal is mentioned in this note.
The animal is a'. Delta S_cat−S_dog=-0.178008199, preferreddog; diagnostic only, not a correction. Allerrors=0, explicitly[retained or absent](errors_cn.md). [All12texts,prefixes,scores,IDs](casebook_cn.md).

Success may be literal copying of the visiblecat/dog word. It does not prove abstraction, hidden concept hierarchy, feature composition or causal use/generalization. The change fromS01also changes task, language and candidates, so it cannot isolate one explanation for between-round differences. All81S01sourcefiles remain byte-identical. H1–H4and scientific acceptance are unchanged; next decision awaits researcher review.
