# Detailed: A11_14 Natural-Language Semantic Learning Efficiency

Primary anchor: [11_14_natural_language_semantic_learning_efficiency_anchor.md](../../../problem_anchors/11_informative_future_branch_mechanism/11_14_natural_language_semantic_learning_efficiency_anchor.md)
Protocol: [protocol.md](protocol.md)
Summary: [summary.md](summary.md)

## 0. Decision

The valid four-GPU full run is **insufficient** because neither NTP nor K=2 MTP reaches the common-H1 threshold in any seed. This record preserves the negative result and localizes the failure before the objective is changed.

## 1. Exact Setup

- data: A11_13 `horizon_target=256`;
- train paraphrases: `0,1`; evaluation paraphrases: `2,3`;
- 160 train and 160 evaluation examples per seed;
- deterministic word/punctuation vocabulary, size `495`;
- sequence length `357-383` tokens;
- two Transformer layers, `d_model=128`, 4 heads, `d_ff=512`;
- NTP: $L_1^{all}$;
- MTP: $L_1^{all}+L_2^{all}$;
- AdamW `3e-4`, weight decay `0.01`, batch size `16`, gradient clip `1.0`;
- 5,000 updates and about `29.4M` processed text tokens per run;
- seeds `971-975`.

## 2. Protocol And Implementation Audit

The remote job `pt-xfvrymp5` succeeded. Four shards completed 10 tasks and 120 curve rows. The GPU smoke completed before the full run.

| Guard | Result |
|---|---|
| task/checkpoint coverage | pass |
| paired shared initialization | pass |
| paired H2 initialization | pass |
| paired train/eval samples | pass |
| paired vocabulary | pass |
| paired batch order | pass |
| paired processed tokens | pass |
| answer absent from prompt | pass |
| finite values | pass |
| split sizes | pass |

The implementation was checked twice after the result. First, full-vocabulary H1 accuracy was compared with restricted A/B accuracy; they are identical at the final checkpoint, so output-format competition does not explain the failure. Second, local H1 learning and H2 direct learning were inspected separately; prompt next-token learning succeeds, while state-conditioned answer learning remains weak.

## 3. Metrics

$$
Q_{downstream}
=\min\{A_{H1},C_{para}^{model},S_{cf}^{model}\}.
$$

$A_{H1}$ uses the full-vocabulary argmax at `<DECIDE>`. $C_{para}^{model}$ requires the two held-out paraphrases in a matched group to yield the same prediction. $S_{cf}^{model}$ requires two states with identical later text to yield different predictions.

Threshold time:

$$
T_{0.9}=\inf\{t:Q_{downstream}\ge0.9\text{ for three evaluations}\}.
$$

No run reaches this event. Reported final token values in the paired table are censoring bounds, not threshold estimates.

## 4. Complete Paired Result

| Seed | NTP AUC | MTP AUC | NTP final $Q$ | MTP final $Q$ | Local guard |
|---:|---:|---:|---:|---:|---|
| 971 | 0.0688 | 0.0110 | 0.3125 | 0.0000 | pass |
| 972 | 0.2082 | 0.1442 | 0.2875 | 0.3750 | pass |
| 973 | 0.1843 | 0.1175 | 0.3625 | 0.3000 | pass |
| 974 | 0.2322 | 0.2135 | 0.2375 | 0.3375 | pass |
| 975 | 0.0639 | 0.0331 | 0.3375 | 0.0000 | pass |

MTP AUC is lower in 5/5 seeds, but the protocol explicitly requires adjudicability before an efficiency direction can be claimed. The correct decision is insufficient, not a negative MTP claim.

Final non-answer H1 accuracy ranges:

- NTP: `0.9215-0.9303`;
- MTP: `0.9354-0.9416`.

Final non-answer H1 CE is lower for MTP in every seed. Thus local LM damage does not explain the low downstream score.

## 5. Failure Decomposition

Three observations identify answer-signal dilution:

1. each answer is one target among roughly 380 all-position targets;
2. train H1 loss falls to about `0.015`, and local evaluation accuracy exceeds `0.92`;
3. answer NLL remains near `0.69` in constant-prediction MTP seeds, with $S_{cf}=0$.

The run does not save checkpoints, so train-split answer accuracy cannot be reconstructed post hoc. The follow-up must record it. This missing diagnostic does not invalidate the current decision because evaluation solvability already fails, but it is required to distinguish memorization from paraphrase transfer next time.

## 6. Visualization Results

### Plot Contract

**Question:** does unweighted all-position MTP improve a common standard-H1 downstream score before NTP?
**Data:** 10 valid remote runs, 12 checkpoints each.
**Metrics:** $Q_{downstream}$, full-vocabulary H1/H2 answer accuracy, right-censored threshold budget, non-answer H1 CE.
**Allowed conclusion:** adjudicable or insufficient.
**Limitation:** bars at the final token budget do not indicate threshold crossing.

![A11_14 unweighted learning curves](figures/a11_14_learning_efficiency.png)

The figure is readable and correctly shows that no curve approaches 0.9. The title of the lower-left panel explicitly identifies final-budget censoring.

## 7. Hypothesis Decisions

| Hypothesis | Result | Decision |
|---|---|---|
| H1 common-H1 recovery adjudicable | reach count 0/5 for both | not supported; insufficient |
| H2 MTP earlier/higher AUC | no threshold; AUC lower 5/5 | not adjudicable |
| H3 gain reaches common head | H2 only partial, H1 weak | not supported |
| H4 local learning guarded | 5/5 pass | supported |

Overall: **insufficient evidence**.

## 8. Artifact Map

Raw result:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
results/a11_14_natural_language_semantic_learning_efficiency/
a11_14_natural_language_semantic_learning_efficiency_4gpu_20260710_173742
```

Logs:

```text
.../active/synthetic_data_understanding/logs/acp/
a11_14_natural_language_semantic_learning_efficiency_4gpu_20260710_173742
```

Job: `pt-xfvrymp5`, one `n6ls.iu.i40.4` node, four H100 80GB GPUs.

Code:

```text
configs/a11_14_natural_language_semantic_learning_efficiency.json
scripts/run_a11_14_natural_language_semantic_learning_efficiency.py
scripts/analyze_a11_14_natural_language_semantic_learning_efficiency.py
scripts/submit_a11_14_natural_language_semantic_learning_efficiency_4gpu.sh
```

Canonical tables:

- [paired efficiency](tables/paired_efficiency.csv)
- [trajectory summary](tables/trajectory_summary.csv)
- [decision](hypothesis_decision.json)
- [central figure](figures/a11_14_learning_efficiency.png)

## 9. Next Decision

Create A11_14b. Preserve the same task, model, split, paired schedule, and common H1 metric. Add a shared decision-weighted H1 loss to both conditions and the corresponding earlier decision-weighted H2 loss only to MTP, while retaining all-position losses. Record train and evaluation downstream scores. This tests the intended semantic credit path after removing answer-position dilution, without broadening K, task, or architecture.

