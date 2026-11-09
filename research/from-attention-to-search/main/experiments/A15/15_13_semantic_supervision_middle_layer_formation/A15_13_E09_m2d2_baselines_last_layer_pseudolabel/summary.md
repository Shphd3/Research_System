# Summary: A15_13_E09 M2D2 Baselines And Last-Layer Pseudo-Label Routing

Primary Anchor: [A15_13_04](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_04_m2d2_causal_lm_semantic_routing_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status: `ELIGIBLE`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## Result Snapshot

**Registered verdict:** `PASS_PSEUDO_METHOD`.

The final-layer unsupervised labels produced a causal hierarchical Router that beat the strongest newly trained simple Baseline on held-out next-token NLL in both seeds, routed tokens by held-out domain more than task-only routing, and used child experts that were not freely interchangeable. This is positive evidence that the architecture can retain ordinary language-modeling performance while adding semantic organization without human route labels.

The result does **not** show that the registered direction-plus-radius clusterer is optimal. On the frozen final-layer representations, its confirmation fine-domain NMI was `0.444`; direction-only clustering reached `0.457`, and diagonal Gaussian clustering reached `0.524`. Only the registered direction-plus-radius labels were used to train a Router in E09.

## Decision-Bearing Setup

The strongest simple Baseline was nine flat rank-24 experts trained only by next-token loss. The treatment used train-only offline clusters of the frozen model's final-layer 256-token window means as labels for a two-stage rank-eight hierarchy. Stage one trained coarse routing for 144 optimizer updates. Stage two loaded that checkpoint, froze the coarse Router and parent experts, and trained fine routing for another 144 updates. The online Router always read causal block-14 token states; final-layer states never entered its forward path.

The primary metric is equal-domain confirmation negative log-likelihood, in natural-log units per predicted token. The registered contrast is strongest simple Baseline minus method, so a positive value favors the hierarchy.

## Verdict Basis

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
| --- | --- | --- | --- | --- |
| Pseudo hierarchy beats the strongest simple Baseline in both seeds | seed effects `+0.002524`, `+0.001158`; pooled `+0.001841` | paired 95% interval `[0.001684, 0.002003]` | Pass | [Detailed evidence](detailed.md) |
| Pseudo Router has held-out fine-domain association | mean NMI `0.237`; matched macro-F1 `0.336` | task-only flat Router: NMI `0.007`, F1 `0.047`; causal guard error `0.0` | Pass diagnostic | [Detailed evidence](detailed.md) |
| Pseudo child experts are not freely interchangeable | deletion `+0.000932 [0.000853,0.001011]`; wrong child `+0.000485 [0.000417,0.000552]` | positive in both seeds | Pass functional gate | same aggregate |
| Final-layer clustering contains domain-readable structure | direction-plus-radius NMI `0.444`; direction-only `0.457`; diagonal Gaussian `0.524` | train-only fit; confirmation truth used only for audit | Positive diagnostic; registered clusterer not best | same aggregate |
| Language fitting is not visibly slowed | final 24-update train language CE `2.5001` pseudo versus `2.5008` flat task-only; held-out NLL `2.881270` versus `2.883111` | same 288 updates and four data passes; post-hoc trajectory audit | No large observed optimization penalty | [`learning_efficiency_summary.csv`](tables/learning_efficiency_summary.csv) |

## Key Evidence

| Condition | Plain meaning | Confirmation NLL; lower is better |
| --- | --- | ---: |
| Frozen Base | no post-training | `2.969889` |
| Dense rank 24 | one adapter used by every token | `2.887619` |
| Flat task-only rank 24 | nine flat experts, no semantic loss | `2.883111` |
| Flat gold rank 24 | nine flat experts, gold nine-way route loss | `2.890184` |
| Reused staged task-only hierarchy | previous hierarchy, no fine semantic loss | `2.880368` |
| Direct gold-nine hierarchy | one-stage global gold route supervision | `2.880737` |
| **Final-layer pseudo-label hierarchy** | **two-stage unsupervised semantic routing** | **`2.881270`** |
| Reused hard semantic Oracle | correct route forced | `2.877571` |

The pseudo method beats every newly trained simple Baseline, but it is `0.000903` NLL worse than the reused staged task-only hierarchy. Therefore E09 supports practical semantic organization at competitive task performance; it does not establish that pseudo-semantic supervision itself improves NLL over the same staged topology.

The two-seed training trajectories provide a narrower learning-efficiency statement: under the same 288 optimizer updates, the pseudo hierarchy's final 24-update language cross-entropy was `2.5001`, essentially the same as the flat task-only Baseline's `2.5008`. This supports “no large observed language-fitting penalty,” not faster wall-clock training or better sample efficiency.

A post-hoc four-model trajectory audit gives the same bounded reading. Final-24-update training cross-entropy was `2.5078` for the single rank-24 adapter, `2.5008` for flat task-only, `2.5001` for the final-layer pseudo hierarchy, and `2.4986` for the direct gold-nine hierarchy. These are descriptive training traces; the held-out confirmation NLL table above remains the task verdict.

## Central Figure

![Strict comparison with the strongest simple Baseline](figures/02_strict_baseline_contrasts.png)

How to read: every point above zero has lower NLL than the strongest simple Baseline; all three intervals are fully above zero, including the final-layer pseudo-label hierarchy.

![Four-model matched-update training loss](figures/07_four_model_learning_curves.png)

How to read: all four curves use 288 optimizer updates; the vertical line changes the stage only for the pseudo model, and the four endpoints remain close enough to rule out a large visible language-fitting slowdown rather than to establish equal compute or statistical equivalence.

## Claim Boundary

**Can claim:** the frozen final layer contains unsupervised domain-readable information, and its train-only pseudo labels can supervise a causal hierarchical Router that passes the registered task, route-semantic, and expert-intervention gates.

**Cannot claim:** that clustering is online, that abstract semantics beyond Wikipedia topical domains were discovered, that direction-plus-radius clustering is optimal, that the frozen Base representation was reshaped, or that pseudo supervision beats the architecture-identical staged task-only hierarchy. Flat rank-24 leaves match active rank but store more parameters, so this is not total-parameter-matched superiority.

## Next Decision

**Proposed, awaiting researcher confirmation:** do not retrain the Router yet. First use cached frozen states and train/development only to select one layer-and-clusterer combination among direction-only, direction-plus-radius, and diagonal Gaussian candidates. The existing confirmation labels have already been inspected in the post-hoc cluster comparison, so choosing diagonal Gaussian from that comparison and scoring it on the same confirmation set would be exploratory rather than a fresh confirmatory test. After selection is frozen, a separate protocol can decide whether two-seed Router training needs a new untouched holdout.
