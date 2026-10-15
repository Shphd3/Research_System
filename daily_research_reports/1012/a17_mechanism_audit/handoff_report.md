# A17 mechanism audit: discussion entry for Web AI

Date: 2026-10-12. Read this entry before the [complete meeting script](../meeting_report/a17_r02_mechanism_meeting.md). The [portable reading bundle](reading_bundle/README.md) contains the canonical design, results, figures, and audits. This derived entry preserves their scientific boundaries; it does not replace the Anchor, Protocol, Summary, or Detailed record.

## 1. Purpose

The parent question is when different prediction requirements should share trainable parameters and when conditional or separate processing is worth its cost. This round asks which actual parameter changes make an already learned old command rule reverse when training supervises only a reversed new mode. Finite interventions on the last attention layer of Qwen3-0.6B show that matrix combinations participate in the reversal: restoring one matrix recovers some old selection while losing new selection. No independent rule matrix or net advantage of separate parameters has been established.

## 2. Model

Every input contains a visible mode, a neutral command 甲/乙, and three distinct list tokens. Loss applies only to the single answer token. In old mode one, 甲 selects the first item and 乙 the last. Consistent new mode two preserves this mapping; reversed new mode two swaps it. For the list “红 黄 猫”, the old targets are 红/猫 and reversed-new targets are 猫/红. The visible mode makes both mappings jointly satisfiable; no complete input receives contradictory labels within an experiment.

R02 trains only the final attention layer's Q/K/V/O matrices in Qwen3-0.6B Base: 6,291,456 parameters. All other parameters remain frozen. Q/K/V produce the attention readout, and O projects that readout into the downstream representation. These computational roles do not identify dedicated rule functions.

Continuation-order seeds 29/43/71 share one real, fully learned old checkpoint. Primary branches use fresh AdamW with learning rate 0.0001 for 1,200 updates of 20 new answers: 24,000 exposures. Consistent and reversed branches match new inputs, order, target marginals, and budget, swapping only labels. Joint training uses 10 old plus 10 reversed-new answers per update, adding old supervision and halving new exposure; it is a feasibility witness.

R03 performs no training. It loads reversed R02 states at steps 240/1,200 for the three orders, restores each complete state, and applies single-matrix replacements or whole-displacement interpolation. Evaluation uses already exposed DEV panels: 400 answers per mode for unseen order and 400 for unseen combination, or 1,600 old/new predictions per condition. Unseen order rearranges a familiar token set; unseen combination uses familiar tokens in a new set. Neither tests unseen vocabulary.

CE is the negative log probability of the correct answer, lower being better. Accuracy checks the full-vocabulary highest-probability token. Rule margin compares the correct endpoint with the opposite endpoint, higher being better. CE is in nat/answer and margin in nat, using natural logarithms. Tables average the two DEV panels and three continuation orders equally; these are not three independently trained old models.

## 3. Hypothesis

Candidate mechanism H1 states that reversed-new-only training changes reading and output computations used by both modes without sufficiently restricting those changes to the new mode. Rollback/insertion tests the finite predictive participation of realized changes. Four old/new O × old/new QKV combinations test background dependence.

**The strongest retained rival H3 concerns supervision, initial difficulty, and optimization path.** Consistent new-mode accuracy starts at 99.875%, reversed at 0%. New-only training provides no old labels; joint training adds old labels and halves new exposure. H1 explains how internal changes participate in the outcome, whereas H3 explains why training chose that path. Both can hold. These interventions do not exclude H3.

The narrower rival H2 is excessive movement along the realized displacement. Five-point interpolation tests five scales of that displacement, not lower-learning-rate retraining.

## 4. Conclusion

1. **Task relationships change retention under shared continuation; different rules do not automatically require separate parameters.** Consistent continuation retains 100% old accuracy. Reversed continuation reaches 99.25% new accuracy and 0% old accuracy. Joint supervision attains 99.83% old and 99.67% new accuracy in the same parameters. Representational feasibility and retention during sequential training are distinct.
2. **Finite interventions support coordinated predictive participation without identifying an independent rule module.** All 24 rollback comparisons improve old accuracy while reducing new accuracy. Endpoint Q rollback gives 48.54% old/57.04% new; O rollback gives 32.67%/68.71%. The same O change lowers old margin by 3.4685 nat under old QKV and 11.8342 nat under reversed QKV: its effects are not simply additive.
3. **Simple scaling of the realized displacement does not reconcile the tasks at tested points.** None of 30 points reaches 80% in all eight mode × command × panel cells; the best minimum cell is 13.5%. This does not exclude narrow intervals between points, other parameter paths, or real low-learning-rate continuation.

Researcher acceptance of the mechanism, question closure, and the next decision remain `Unknown`. This entry does not promote finite evidence into unique function, universal necessity, or separate-training utility.

## 5. Analysis

### Eight executed steps

1. **Audit data and saved states.** CPU checks cover 9,600 original prefixes, tokenizations, answer positions, and labels, 72 states, and 72 native caches, including the shared old start.
2. **Recompute existing trajectories and weight displacements.** Read saved points without rerunning training; describe each matrix's norm and direction. Both modes' mean command responses change sign between saved steps 16 and 50 for all three orders; this bounds an interval rather than an exact first update.
3. **Run a matching GPU Smoke.** Use a four-H100-reserved allocation to verify native replay, no-op, restoration, and frozen-weight guards. Smoke `pt-p6uri2px` succeeds before successful formal finite analysis `pt-o3rvi0s1`.
4. **Rollback and insert each matrix.** Restore one Q/K/V/O matrix to its old value inside the reversed model; separately insert one reversed matrix into the old model. Fully reset between interventions. Measure both checkpoints, three orders, and both DEV panels.
5. **Evaluate five interpolation scales.** Scale all four matrices jointly by 0, 0.25, 0.5, 0.75, or 1 of the old-to-reversed displacement: 30 points, each checked against all eight 80% qualification cells.
6. **Connect representations to predictions.** At order 29/step 1,200, preselect the first ten sorted list IDs in each panel. Evaluate 80 inputs across two modes and two commands under all four O × QKV states. These are repeated measurements of one fixed panel.
7. **Independently recompute the outputs.** CPU review covers 88 native readouts, 140,800 record appearances, 300 summary rows, 30 interpolation verdicts, and representations with zero errors. It reads saved outputs and vectors rather than independently rerunning the entire GPU experiment.
8. **Register outputs and complete the report.** Saved analysis and four-state representations are registered; results, provenance, five figures, and the full meeting script are complete. No new training checkpoint is produced.

### Training phenomenon and parameter interventions

R02 endpoint readings are absolute levels. Old baseline CE is 0.000691, accuracy 100%, and margin +17.5247.

| Continuation | Evaluated rule | CE | Accuracy | Rule margin |
|---|---|---:|---:|---:|
| Consistent new only | Old | 0.000040806 | 100.00% | +23.1460 |
| Consistent new only | Consistent new | 0.000040982 | 100.00% | +22.8513 |
| Reversed new only | Old | 15.819206 | 0.00% | −15.7931 |
| Reversed new only | Reversed new | 0.031350 | 99.25% | +16.1898 |
| Joint old/reversed-new | Old | 0.004841 | 99.83% | +18.1063 |
| Joint old/reversed-new | Reversed new | 0.009108 | 99.67% | +15.6502 |

After reversal, old predictions predominantly select the endpoint required by the new mapping, while list-candidate mass remains 99.6211%. The failure therefore cannot be reduced to inability to predict list words. Joint training changes old supervision and new exposure, so it is not a matched sharing/separation utility comparison.

All single-matrix interventions at step 1,200 follow. Rollback uses the reversed background; insertion uses the old background. They are not additive contributions.

| Parameter condition | Old CE | Old accuracy | Old margin | New CE | New accuracy | New margin |
|---|---:|---:|---:|---:|---:|---:|
| Full reversed | 15.819206 | 0.00% | −15.7931 | 0.031350 | 99.25% | +16.1898 |
| Rollback Q | 3.729379 | 48.54% | −0.2193 | 2.154850 | 57.04% | +2.3963 |
| Rollback K | 6.810371 | 22.46% | −5.4037 | 1.045201 | 80.54% | +6.6957 |
| Rollback V | 7.538096 | 23.96% | −6.7037 | 0.747970 | 78.17% | +6.9512 |
| Rollback O | 5.571890 | 32.67% | −4.3377 | 1.172081 | 68.71% | +4.5621 |
| Insert Q only | 4.300164 | 51.21% | +1.5551 | 5.692210 | 48.12% | −0.9955 |
| Insert K only | 1.713204 | 78.71% | +6.8236 | 7.170560 | 33.54% | −4.3167 |
| Insert V only | 0.014439 | 99.54% | +10.9963 | 9.697651 | 0.46% | −9.6763 |
| Insert O only | 0.036819 | 98.71% | +14.0772 | 12.461385 | 1.29% | −12.4113 |

Replacing actual matrix combinations changes both modes' predictions, supporting their causal participation at specified states. No tested single-matrix condition retains both tasks. Two-/three-matrix combinations were not exhausted, so the results do not establish that all four are necessary.

### The 80-input representation bridge

Let c be the attention readout and W the O matrix; the attention output is Wc. Four real forward states combine old/reversed readouts with old/reversed O.

| Four-state combination | Old correct-endpoint margin | Reversed-new correct-endpoint margin |
|---|---:|---:|
| Old QKV + old O | +15.8824 | −14.9373 |
| Old QKV + reversed O | +12.4139 | −11.0762 |
| Reversed QKV + old O | −3.1091 | +3.5102 |
| Reversed QKV + reversed O | −14.9432 | +15.7408 |
| Four-cell interaction | −8.3657 | +8.3695 |

The four-cell interaction subtracts the two separate changes from their joint change and restores the old baseline. It measures nonadditive predictive effects. This demonstrates background dependence, not a unique mediator, independent task module, or shared representation subspace. Fixed downstream nonlinear computation also contributes to this functional interaction.

### Three questions for continued Web AI discussion

1. **Which rival is most valuable to distinguish next?** Given H1's finite parameter evidence and open H3 supervision/difficulty/path explanations, what minimal comparison could change the judgment about why changes were not restricted to the new mode? State discriminating predictions before methods.
2. **How should conditional restriction be tested beyond preserving old weights?** Control new-task proficiency, exposure, and old supervision to test simultaneous retention and new learning. Do not treat rollback, interpolation, or a frozen old copy as an already superior training design.
3. **When is a sharing/separation utility comparison justified?** Which evidence threshold and matched-budget baseline distinguish sequential optimization costs, inadequate conditional computation, and benefits of independent parameters? Separate observations from candidate explanations.

These questions request conceptual discussion and design suggestions only. **They authorize no new training, submission, mechanism acceptance, or question closure.** Evidence is conditional on one old checkpoint, three continuation orders, and exposed DEV. Fresh TEST confirmation, low-learning-rate retraining, and expert-separation utility comparisons have not been run.
