# Summary: A15_13_E13 Mixed Answer-Only Semantic Routing

Primary Anchor: [A15_13_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_04_m2d2_causal_lm_semantic_routing_anchor.md)
Frozen Protocol and amendments: [protocol.md](protocol.md)
Detailed record: [detailed.md](detailed.md)
Result status: `ELIGIBLE_FOR_WITHIN_MIXTURE_NLL`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## Result Snapshot

**Primary verdict: `FAIL_LEARNED_SEMANTIC_EFFICIENCY`.**

Source supervision made routing strongly source-related, but it did not make learned routing fit answer tokens faster than the same topology trained only by answer cross entropy. Flat and hierarchical semantic models had worse fixed-development curve area in both seeds. Their final token-weighted evaluation NLL was also worse than task-only by `0.013758` and `0.002341`, respectively.

The forced-gold hierarchy gives the important positive boundary. It reached the task-only model's 75%-budget loss with `1.36x` and `1.43x` fewer answer tokens and improved final NLL by `0.023024`. Therefore the grouping can help when routing responsibility is fixed correctly; the failure lies in turning supervised route predictions into an equally efficient learned forward path.

The senior-style geometry pattern did not reproduce. Source-supervised experts were **more**, not less, similar: mean pairwise update cosine rose from `0.0131` to `0.0545` for flat experts and from `0.0203` to `0.0549` for hierarchical leaves. Their singular-value effective rank also fell from `5.31` to `1.32` and from `2.88` to `1.46`.

## What Actually Ran

This experiment was not staged. Each of eleven conditions was trained independently for four equal data passes and 128 optimizer updates under seeds 17 and 29, giving 22 full training runs. Every condition saw the same source-balanced order within a seed. Qwen3-0.6B-Base and its language head were frozen; only block-14 `down_proj` LoRA experts, Routers, and routing biases were trainable.

The dataset contained 512 train, 64 fixed-development, and 64 evaluation examples from each of eight cached sources: MMLU, RACE-high, ARC-Challenge, GSM8K, MetaMathQA, SciQ, HumanEval, and MBPP. Only answer tokens contributed cross entropy. Source names were absent from prompts. HumanEval has only 164 cached rows, so cycling created overlap; all metrics are fitted-mixture diagnostics, not uncontaminated benchmark scores.

## Final Evaluation

The table reports answer-token NLL, pooling all evaluated answer tokens; lower is better. NMI is normalized mutual information between selected route and source; higher means more source-related routing, but it does not prove task benefit.

| Condition | Mean NLL | Route/source NMI | Load entropy |
| --- | ---: | ---: | ---: |
| Dense rank-24 adapter | `0.683717` | `0.000` | `0.000` |
| Flat task-only | **`0.652395`** | `0.093` | `0.401` |
| Flat source-supervised | `0.666153` | **`0.701`** | `0.666` |
| Flat sample-random-label | `0.699336` | `0.051` | `0.963` |
| Hierarchy task-only | **`0.618807`** | `0.097` | `0.161` |
| Hierarchy source-supervised | `0.621148` | **`0.713`** | `0.668` |
| Hierarchy forced-gold, unit coefficients | **`0.595783`** | `1.000` | `0.669` |
| Flat task-only + loss-free bias | `0.652487` | `0.093` | `0.409` |
| Flat source-supervised + loss-free bias | `0.666173` | `0.702` | `0.666` |
| Hierarchy task-only + loss-free bias | `0.618843` | `0.096` | `0.164` |
| Hierarchy source-supervised + loss-free bias | `0.620900` | `0.713` | `0.668` |

The corrected random-label null used exactly balanced sample-level labels with train source/label NMI `0.00284`. It is no longer a source-ID renaming. Semantic labels clearly beat this random null, but task-only training still beat learned semantic supervision.

## Learning Efficiency

Positive curve-area improvement means semantic supervision learns faster.

| Matched comparison | Seed 17 | Seed 29 | 75%-budget token result |
| --- | ---: | ---: | --- |
| Flat semantic minus flat task-only | `-0.01297` | `-0.01713` | semantic never reached target |
| Hierarchical semantic minus hierarchical task-only | `-0.01102` | `-0.00791` | no gain; seed 29 speed `0.986x` |
| Forced-gold minus hierarchical task-only | **`+0.01140`** | **`+0.01391`** | **`1.36x`, `1.43x` speedup** |

Loss-free bias changed task-only load entropy only from `0.401` to `0.409` for flat routing and from `0.161` to `0.164` for hierarchical routing. The corresponding NLL changes were below `0.0001`; it did not solve learned-routing efficiency.

## Expert Function And Geometry

Deleting or replacing the active expert increased NLL in all matched conditions, so the adapters were functionally used. However, learned semantic supervision did not improve this utility over task-only. For hierarchy, wrong-leaf cost was `+0.02093` under semantics versus `+0.02650` under task-only; forced-gold reached `+0.03777`.

| Expert family | Pairwise update cosine | Effective rank |
| --- | ---: | ---: |
| Flat task-only | `0.0131` | `5.31` |
| Flat source-supervised | `0.0545` | `1.32` |
| Flat random-label | `0.1241` | `1.83` |
| Hierarchy task-only | `0.0203` | `2.88` |
| Hierarchy source-supervised | `0.0549` | `1.46` |

Thus the source loss created interpretable routing without producing the senior's “less similar experts” signature in this one-layer 0.6B setup.

## Central Figures

![Answer-only learning curves](figures/answer_only_learning_curves.png)

How to read: lower curves learn answer tokens faster. Forced-gold is consistently lowest; learned source supervision stays above task-only in both flat and hierarchical topology.

![Task and semantic results](figures/task_and_semantic_results.png)

How to read: the left panel is the task metric and the right panel is route semantics. Source supervision wins only on the right; forced-gold wins on both.

![Expert update similarity](figures/expert_update_similarity.png)

How to read: lower means more different experts. Source-supervised bars are higher than task-only, and random labels are highest, opposite to the senior-style target pattern.

![Loss-free bias controls](figures/loss_free_bias_controls.png)

How to read: each “+ balance” bar is nearly identical to its parent method. The chosen bias step is too small to materially change either task NLL or the already observed load pattern.

## Claim Boundary

**Can claim:** the eight-source labels are learnable by a causal Router; correct forced grouping improves answer-only post-training efficiency and final NLL; the present learned source loss does not recover that gain and does not diversify expert updates.

**Cannot claim:** standard benchmark improvement, uncontaminated generalization, superiority to the senior's 7B model, or that every kind of semantic label is ineffective. This is one frozen 0.6B base model, one modified layer, two seeds, cached substitute tasks, and teacher-forced answer evaluation.

## Next Decision

Do not add more clustering or stronger load balancing yet. First align learned training responsibility with the successful forced-gold path: train experts under hard source routes, then replace the Oracle with a learned Router while keeping unit expert coefficients, and test whether the `1.36x--1.43x` efficiency headroom survives.
