1. **Behavior and factor controls:** when predictions change.
2. **Representations and layerwise organization:** what is observable and readable.
3. **Functional interventions and quality:** how state changes affect predictions and whether measurements are reliable.

# A15_18: relation composition, distance and internal representations

**The model answered 329 of 640 TEST items correctly (51.41%) and selected No 611 times.** Four composition/distance cells and the internal measurements are saved. Mechanism judgment remains **PENDING_RESEARCHER_REVIEW**. This Summary supplies the first reading; [Detailed](detailed.md) explains the computations, and the [itemized appendix](explanation_appendix.md) preserves the original long account and tables.

## Why run this audit?

The MoE program asks which information can be reused and which learning should be separated. The immediate measurable question is: **when an answer requires more relations, or necessary evidence is farther away, how do the frozen model's predictions and internal representations change?** Qwen3-0.6B Base has 28 blocks. Its parameters and the existing dictionaries stay fixed; external linear classifiers are fitted separately.

## One real comparison

Rows 1408 and 1412 both ask `Is Sam located to the left of Bob?` Each contains 12 facts. The table excerpts the decisive fact; complete inputs remain in the [Chinese itemized appendix](explanation_appendix_cn.md).

| Actual row | Decisive fact | Correct answer | Model selection | Correct-answer margin |
|---|---|---|---|---|
| 1408 | `Relative to Bob, Sam is on the left.` | Yes | No, incorrect | −0.625000 nat |
| 1412 | `Relative to Sam, Bob is on the left.` | No | No, correct | +0.750000 nat |

The margin is correct-candidate log probability minus incorrect-candidate log probability. For row 1408, log probabilities are −0.685888 for No and −1.310888 for Yes, giving −0.625000 nat. Positive favors the correct candidate. A nat uses natural logarithms. Reversal-pair accuracy matters because always choosing No can answer one item in such a pair correctly.

**Actual C comparison:** row 1416 requires the left-to-right chain Sam→Carol→Mary→Bob, whereas row 1408 directly states one Sam/Bob relation. Both ask whether Sam is left of Bob.

**Actual D comparison:** rows 1408→1410 retain the same facts and change their order. The necessary evidence moves from 33 to 103 tokenizer positions before the query location.

Three factors are kept distinct:

| Factor | Definition and operation in this round |
|---|---|
| **Composition C** | One or three necessary relations, verified by deleting each necessary graph edge; every item still has 12 facts. This counts task requirements. |
| **Distance D** | Reorder the same facts, moving a fixed five-fact neighborhood containing the evidence nearer or farther. Mean TEST evidence distances are about 33–36 versus 104–106 tokenizer positions. This also changes fact order. |
| **Learning exposure F** | How often a relation or complete combination appeared in model training. No reliable estimate or training manipulation exists here, so F is unmeasured. |

There are 128 families and 2,048 variants, split into 64/24/40 TRAIN/DEV/TEST families. A family contains depth, distance, reversal and wording variants of one entity assignment. Complete families stay together, and TEST templates are held out from TRAIN.

## Behavior across the four cells

Each cell contains 160 items from the same 40 TEST families. Intervals resample entire families 2,000 times and describe item variation for this fixed model. This is Yes/No candidate scoring; free generation was not measured.

| Required relations / distance | Correct-answer margin, nat (95% interval) | Candidate accuracy, % (95% interval) | Both reversal items correct, % |
|---|---|---|---|
| 1 / near | 0.005469 [-0.025020, 0.036719] | 53.125 [50.000, 56.250] | 7.50 |
| 1 / far | ≈0 [-0.026563, 0.028125] | 53.750 [50.625, 57.500] | 8.75 |
| 3 / near | -0.007031 [-0.037500, 0.022656] | 48.125 [45.000, 51.250] | 2.50 |
| 3 / far | 0.011719 [-0.005469, 0.029687] | 50.625 [50.000, 51.875] | 1.25 |

All four **mean** margins are near zero with intervals crossing zero. Individual items need not be near ties: the example pair has a substantial No preference in both items, but the correct-answer sign is opposite, allowing cancellation. TEST truth has 320 Yes and 320 No items. Of 611 No selections, 40 are exact candidate ties resolved by the frozen No-first rule.

The primary paired comparison is deep far-minus-near minus shallow far-minus-near: **+0.024219 nat, 95% interval [−0.011719, +0.060937]**. It asks whether the distance difference changes with composition. The interval includes either sign and zero; it is an estimate, not a declaration of no distance effect or scientific success. [Cell and paired-family results](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E02/results.json)

## Internal representations

A state is the 1,024-number vector at a specified layer and token position. The audit saves the answer-prefix final position and necessary-evidence ends at all 28 blocks. A block increment subtracts the same-position block input from its output.

| Question | Operation | Measured observation |
|---|---|---|
| Do many inputs share a small set of variation directions? | Principal component analysis (PCA) finds common directions of largest TRAIN-state variation, then measures TEST retention, separately for states and increments. | State effective rank is 5.803/33.864 at the first/28th blocks (indices 0/27), converting variance concentration into an equivalent direction count. At the 28th block, 64 TRAIN directions retain 71.87% of centered TEST state energy: summed squared deviations from the mean, rather than an amount of answer information. |
| Can a simple external reader recover the answer? | Fit an equal-capacity linear Yes/No classifier at every layer, with shuffled-TRAIN-label controls. | Across 28 layers, true-label TEST accuracy ranges from 48.28% to 52.19%; shuffled-label accuracy ranges from 47.81% to 52.34%. Numerical convergence and these generalization results are separate facts. |
| Can existing dictionaries describe the states? | Qualify reconstruction before reporting feature activations. | A22 CrossCoder, a sparse dictionary reconstructing several layers, covers 14 layers. Reconstruction fraction of variance explained is 0.767563 against its saved TRAIN mean. The single-layer sparse autoencoder (SAE) gives −4.270350 against the task-TRAIN mean: worse than that reference, invalidating its feature interpretation. |

Geometry, external readability and dictionary reconstruction answer different questions. Aligned cross-layer similarities are also measured; [Detailed](detailed.md) explains them and the [appendix](explanation_appendix.md) retains all-layer tables. [All readouts](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E05/probes.json) · [Spectra and retention](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E04/spectra.json) · [Dictionary qualification](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E07/dictionary_coverage.json)

## What happens when a state is changed?

First ask how much prediction survives when a state is confined to a few directions. **Equal-rank random directions** provide the same compression scale, and **self-write** checks the replacement operation itself. Then ask whether an opposite-relation donor shifts the receiver's answer preference. A **same-relation donor** supplies a reference for general wording or order changes. These controls define the comparisons before their values are read.

Direction interventions replace a state by its TRAIN mean plus retained principal coordinates. At the preregistered 28th block (index 27) and rank 16, PCA/random state errors are about 0.64/0.98. Error divides summed squared replacement displacement by summed native centered energy. Correct-margin changes are approximately 0 [−0.025000, 0.025000] and −0.007812 [−0.034375, 0.018750] nat. **State reconstruction and prediction change are separate measurements.** [Detailed](detailed.md) retains exact errors and all 105 conditions, with 80 receivers each.

Donor interventions replace a position's state with the opposite-relation item's complete vector. Independent DEV selection chooses the 16th/28th blocks (indices 15/27). At the 16th block's query position, the mean correct-margin change is −0.014063 nat [−0.032813, 0.007812], over 80 receivers and 10 families. Final self-write changes are zero. Same-relation controls and natively correct/incorrect receiver groups remain visible. Complete states also carry entities and context; their specific content awaits later review. [Projection results](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E08/results.json) · [Donor results](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/E09/results.json)

## Coverage and next reading

| Items | Measurement | Status |
|---|---|---|
| E00 / E01 / E10 | Interfaces, tasks and reproduction | DONE_VALID |
| E02 | Four-cell behavior | DONE_EXPLORATORY |
| E03–E07 | States, spectra, readouts, layers and dictionaries | DONE_EXPLORATORY |
| E08 / E09 | Direction interventions and donor replacement | DONE_EXPLORATORY |

`DONE_VALID` qualifies calibration or accounting; `DONE_EXPLORATORY` records completed exploratory measurements. F is BLOCKED and SAE is INVALID. Separate intermediate labels, feature interventions and unexecuted training dependencies remain in the [coverage ledger](/data/250010109/MoE_Router/experiments/20261022_relation_organization_audit_v3/coverage.json). The applicable C×D audit is measured.

First review what behavior, external readout and interventions each show. Follow [Detailed](detailed.md) for the method, then the [appendix](explanation_appendix.md) for individual tables. The researcher states observations before AI mechanism judgment; scientific conclusion and the next research choice remain Unknown.

One understanding question: how do you read roughly half-correct cell accuracies together with 611 No selections?
