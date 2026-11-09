# Step1: native singularity judgment on explicit36texts

Completed and stopped for joint review. Original H1–H4 are not retested or reinterpreted.

## Purpose and data

Test the current frozen Qwen3-0.6B Base when square/singular-square/invertible-square is explicitly stated.12English sentence/context families×3independent descriptions=36, with matched objects/skeletons and necessary a/an agreement only. Square=True for all; singularity unknown/yes/no. No determinant/rank or inferential certificates. Unknown is insufficient textual information, not contradictory properties of one matrix. OldD1texts/scores are not pooled.

## Method

Same official checkpoint/tokenizer hashes asD1, FP32 CPU2threads. Fixed2Chinese question/candidate formats saved before responses. F1 uses yes/no/unknown (2/2/3tokens), F2 equivalent unknown/no/yes(3/4/4tokens). Sum every candidate-token conditional logprob including period, excluding prompt/EOS, FP32token probabilities/FP64accumulation; choose max without length/prior correction. Neutral property-free text scored once/format, diagnostic only. No dictionaries/hooks/features/probes/training/intervention or prompt search.

## Observations

| format   |   correct |   N |   fully_correct_families |   families |
|:---------|----------:|----:|-------------------------:|-----------:|
| F1       |        13 |  36 |                        0 |         12 |
| F2       |        12 |  36 |                        0 |         12 |

| format   | condition        | gold     |   correct |   N |
|:---------|:-----------------|:---------|----------:|----:|
| F1       | 方阵／奇异性未知 | 无法确定 |         0 |  12 |
| F1       | 奇异方阵         | 是       |         1 |  12 |
| F1       | 可逆方阵         | 否       |        12 |  12 |
| F2       | 方阵／奇异性未知 | 无法确定 |         0 |  12 |
| F2       | 奇异方阵         | 是       |        12 |  12 |
| F2       | 可逆方阵         | 否       |         0 |  12 |

| format   | gold     |   pred_unknown |   pred_yes |   pred_no |
|:---------|:---------|---------------:|-----------:|----------:|
| F1       | 无法确定 |              0 |          0 |        12 |
| F1       | 是       |              0 |          1 |        11 |
| F1       | 否       |              0 |          0 |        12 |
| F2       | 无法确定 |              0 |         12 |         0 |
| F2       | 是       |              0 |         12 |         0 |
| F2       | 否       |              0 |         12 |         0 |

Paired preferred labels agree on1/36; both correct on1/36. Per-condition agreement:

| condition        |   N |   same |   both_correct |
|:-----------------|----:|-------:|---------------:|
| 可逆方阵         |  12 |      0 |              0 |
| 奇异方阵         |  12 |      1 |              1 |
| 方阵／奇异性未知 |  12 |      0 |              0 |

Exact candidates, IDs, lengths and neutral scores:

| format   | label    | candidate      | token_ids                     |   tokens |   neutral_total_logprob | neutral_preferred   |
|:---------|:---------|:---------------|:------------------------------|---------:|------------------------:|:--------------------|
| F1       | 是       | 是。           | [20412, 1773]                 |        2 |               -4.292039 | False               |
| F1       | 否       | 否。           | [32376, 1773]                 |        2 |               -2.928918 | True                |
| F1       | 无法确定 | 无法确定。     | [101068, 60610, 1773]         |        3 |               -4.030335 | False               |
| F2       | 无法确定 | 无法判断。     | [101068, 104317, 1773]        |        3 |               -5.991801 | False               |
| F2       | 否       | 不是奇异矩阵。 | [99520, 117223, 115000, 1773] |        4 |               -4.294164 | False               |
| F2       | 是       | 是奇异矩阵。   | [20412, 117223, 115000, 1773] |        4 |               -2.897877 | True                |

[Full36text-and-score casebook](casebook_cn.md) and [first correct/error per class/format](examples_cn.md) retain every outcome and explicitly identify absent examples. OriginalJSONL keeps fullprecision, prefix/candidate/token identities and tokenlogprobs.

## Boundary and stop

Sequence totals can reflect candidate length, lexical prior, period and format. No length-normalized or neutral-corrected alternative decision is substituted. F2changes wording, option order and answer realization together, so no factor is individually identified. English bodies with Chinese questions/answers also involve cross-language instruction behavior of a Base model. This is constrained candidate preference, not free-generation accuracy or universal concept competence. Square labels are manuallyaudited, not a separately asked model task; no nonsquare contrast.

No feature mechanism or concept hierarchy is inferred. Scientific acceptance and next decision remain Unknown. STOP_AFTER_STEP1_FOR_JOINT_REVIEW. No automatic adjustment of text/task/model or next experiment.

[Protocol](protocol.md) · [Detailed](detailed.md) · [Raw](results/raw_scores.jsonl).


## Direct observation: similar totals conceal almost opposite decisions

F1chooses no35/36times, with only F01singular choosing yes. F2chooses yes36/36times. Neither format ever chooses unknown. Preferred meanings agree only1/36, despite similar13/36and12/36correct totals. Balanced classes mean a constantclass choice obtains12/36; F2is exactly constant, F1onlyone better. No family has allthree correct in either format.

Neutral prefixes also prefer no inF1(score−2.928918)and yes inF2(−2.897877), matching the dominant task preference. This is evidence consistent with a response-prior explanation, not unique causal identification. Length alone cannot explain the choices: yes/no are equally2tokens inF1and equally4inF2, whileF2's shorter3token unknown is never chosen. Wording, option order, answer realization, and cross-language instructions still covary. No rescoring correction or prompt search followed.

The fixed measurement has not established a stable three-state behavioral baseline. It does not demonstrate absent internal concepts. Stop here for joint review; no next step performed.
