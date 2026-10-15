派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/summary.md`。
[精确原始文件](../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/A17_04_E01_consistent_reversed_mapping/summary.md)；研究修改仍回到原件。

---

# A17_04_E01: Consistent versus reversed conditional mapping

Execution and measurement complete. Registered outcome: `INSUFFICIENT_OLD_MAPPING_NOT_ACQUIRED`. Scientific mechanism acceptance and question closure remain `Unknown`.

## Purpose

Determine whether changing a new task's conditional prediction mapping changes shared learning's effect on an old task. This asks when task relations produce a learning cost, before deciding whether to separate parameters.

## Model

The model is registered Qwen3-0.6B Base. Only its last attention output projection, `model.layers.27.self_attn.o_proj.weight`, is trained. All other weights stay frozen. Inputs contain a visible mode, neutral command and three-word list. Mode one teaches 甲→first item and 乙→last item. New mode two either preserves or reverses that mapping. For `红 蓝 绿`, mode-one 甲 predicts 红; reversed mode-two 甲 predicts 绿. Visible modes make both mappings label-consistent within one experimental world.

Each of three training-order seeds trains the old mode for 240 updates, then starts consistent/reversed branches from the identical endpoint. All seeds begin with the same pretrained weights; they are not different random weight initializations. New inputs, answer marginals, minibatch order and 4,800 answer targets match within each pair; labels differ. Training uses answer-only CE and ordinary SGD. A joint reversed branch gives additional old supervision as a feasibility check. It is not an equal-supervision performance comparison.

Old answer advantage is the correct endpoint's log probability minus the opposite endpoint's log probability. The primary effect is its reversed change minus its consistent change. Negative means less benefit under reversal; net old harm additionally requires deterioration from the common starting point. We also measure CE, full-vocabulary accuracy, strongest competitor and selection among the three list words. Output contrasts are prediction coordinates, not internal parameter modules.

## Hypothesis

Reversal may give less old rule-sensitive answer advantage than consistency at matched exposure. The strongest rival is task difficulty, initial competence or learning path. General candidate-word adaptation and update-scale differences remain live. Equal-norm probes, comparable-learning readers and joint training constrain these explanations, but they do not identify a complete parameter mechanism.

## Conclusion

1. **This experiment cannot adjudicate retention of a well-acquired old mapping.** Old endpoint DEV accuracy ranged from 33% to 54% across commands/panels, below the registered 80% qualification in every seed. Old TEST accuracy was 49.75%. All specified training and measurements completed, but the scientific outcome is insufficient. This does not prove the model learned nothing; it means the required learned-rule starting condition was not established.
2. **Reversal produced a small relative cost, without mean net old CE or answer-advantage harm.** Its primary effect was −0.005165 nat, negative in all three seeds but below the 0.01-nat operational magnitude convention. Old CE improved in both branches. These are effects on an incompletely acquired mapping, not evidence that reversal damages a retained old rule or requires separate experts.
3. **Correct-token CE benefit was dominated by assigning more probability to list candidates.** In both branches, old list-access CE improved while mean conditional selection CE slightly worsened. Therefore CE improvement cannot be described as established shared rule-learning transfer. Exact output accounting supports this limited explanation; it does not identify a unique internal cause.

The primary and diagnostic values below come from the [registered analysis](../../../../../../../../UNAVAILABLE.md). Scientific mechanism approval remains with the researcher.

## Analysis

The old endpoint is the common reference for all continuations. These are equal-seed means on the same 800 old TEST answers per seed, with unseen panels equally weighted. Lower CE is better; higher advantage is better.

| Old TEST quantity | Old endpoint | After consistent new training | After reversed new training |
|---|---:|---:|---:|
| Correct CE, nat | 1.120444 | 1.038598 | 1.041736 |
| Accuracy | 49.7500% | 49.7083% | 49.9583% |
| Correct-versus-opposite advantage, nat | 0.045724 | 0.064280 | 0.059115 |

Reversal gives less margin improvement than consistency, but both mean margins rise and both mean losses fall. The seed effects are −0.005229, −0.005132 and −0.005135 nat; their sample SD is 0.0000552. This is descriptive replication on one fixed dataset, not a population significance claim. The failed old-acquisition gate takes precedence over a directional retention interpretation.

| Heldout panel | Reversed-minus-consistent old advantage change, nat |
|---|---:|
| Unseen order | −0.001529 |
| Unseen combination | −0.008802 |
| Equal-weight combined, primary | −0.005165 |

The stronger difference on unseen combinations is retained as a measured descriptive pattern. It does not fix the missing acquisition prerequisite.

For the three-word list set \(S\), correct CE splits exactly into access \(-\log\sum_{w\in S}p(w)\) and selection \(-\log[p(y)/\sum_{w\in S}p(w)]\). Relative to the old endpoint, consistent old CE change is −0.081846 = −0.086275 access +0.004429 selection; reversed change is −0.078708 = −0.085028 +0.006319. Thus candidate access more than accounts for the mean CE benefit, while conditional selection becomes slightly worse. An endpoint-only mean advantage can improve at the same time: conditional selection includes the middle candidate and averages a nonlinear loss, so the quantities are not equivalent.

New CE also improves: consistent 1.192306→1.078515 and reversed 1.197546→1.088236. Their accuracies move 46.75%→47.2083% and 46.25%→48.1667%. None of the six seed/world DEV trajectories reaches the fixed 80% comparable-level criterion, so that reader is unavailable. Reversed mode-two's command response remains +0.005931 nat, whereas the intended reversed mapping calls for a negative response; successful conditional inversion has not been established. Joint reversed training ends at old/new TEST accuracies 50.2083%/47.50%; joint feasibility stays Unknown, and its failure does not prove insufficient model capacity.

Equal-norm immediate probes qualify at the same old state. Reversed-minus-consistent old-margin effects are −0.00001656, −0.00001497 and −0.00001284 nat; both probes improve old CE in all seeds. These small local effects do not explain the complete trajectory or remove the acquisition failure.

Smoke, four external resume replays and Full worker qualification passed. Full completed 2,880 updates and 57,600 answer targets; 120 actual checkpoint states were verified and registered through 28 adapter families plus two readout families. Independent numerical recomputation checked 102 files and 460,920 record occurrences, with maximum error 0.000001013 nat. A registry enum error caused an initial strict-access failure and analysis to start before correction; provisional outputs were retained. After schema correction and strict access PASS, analysis was rerun with unchanged results. No GPU rerun or scientific parameter change occurred. [Detailed](../../../../../../../../UNAVAILABLE.md) owns that deviation and complete provenance.

This merger adds a task-relation intervention to the earlier update-component route. The earlier [trajectory Summary](../../../../../../../../UNAVAILABLE.md) already established why CE and answer competition must be separate. The present update is that explicit conditional mapping and meaningful acquisition must be demonstrated before interpreting a relative probability effect as rule retention or rule transfer. **AI suggestion:** qualify the old-only neutral-command task first with a bounded diagnostic; do not yet add costly separation or SAE experiments. This is a suggestion, not an activated new experiment.
