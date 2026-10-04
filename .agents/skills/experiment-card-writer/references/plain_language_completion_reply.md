# Plain-Language Completed-Experiment Reply

Use this reference after execution to write the complete first reading in
`summary.md`, or when the researcher explicitly requests a standalone
single-experiment speaking or meeting brief. It does not replace the Detailed
record. When a Summary already exists, do not duplicate these four sections in
the ordinary chat response; link the Summary first and use the compact result
delivery rule in [SKILL.md](../SKILL.md).

## 1. Completion And Comparison Audit

Verify completion before saying `full run`. Report counts of required
conditions, seeds, checkpoints, interventions, analysis artifacts, and failed
or resumed shards. A completed matrix may still contain bounded or ineligible
evidence.

List conditions by the rival they separate rather than by internal run name:

- frozen/no-training reference;
- ordinary task-training Baseline;
- architecture- and capacity-matched control;
- task-only treatment topology;
- shuffled or structural null;
- Oracle upper bound;
- learned/self-supervised treatment;
- registered mechanism ablations.

Do not imply that a missing comparison ran. Define any retained internal label
in plain Chinese.

## 2. Actual Training Audit

Apply this section when training occurred. For a fixed-model analysis, identify
the model state, frozen objects and actual measurement procedure instead.
For training, distinguish actual stages and report for each stage:

| Required field | Meaning |
| --- | --- |
| trainable/frozen objects | what can and cannot receive gradients |
| data passes and updates | epochs or tokens plus actual optimizer steps |
| batch construction | micro batch, accumulation, and effective batch |
| objective | task, route, regularizer, and their weights |
| optimizer schedule | optimizer, learning rates, warmup, decay, clipping |
| selection | checkpoint metric and selected point |
| handoff | state loaded, optimizer reset/reuse, and newly added modules |

Distinguish a real checkpoint-and-freeze transition from a continuous run that
is only divided during analysis. State protocol deviations that narrow the
claim.

## 3. Four-Section Reader Format

### Purpose

One sentence stating the whole scientific purpose. Do not clarify
implementation here.

### Hypothesis

Use one or two short falsifiable statements. Include the strongest rival in
the second statement when needed.

### Analysis Method

Group the necessary comparisons into a few short bullets. Each bullet says:

```text
what is compared -> what uncertainty it resolves
```

Order the bullets as a gate: for example, dispatch first, function second,
representation or task benefit last.

### Conclusion

Use one numbered item per answer that changes the research judgment. Each item
contains, in order:

1. a plain direct answer;
2. the smallest decisive result and uncertainty or eligibility boundary;
3. a figure or table when it makes the comparison easier to assess, with one
   sentence explaining its axes/columns, observation and relevant limitation.

Text or numerical evidence can be sufficient. An absent optional figure is not
missing evidence. Do not add a conclusion merely to display another metric;
report an actual evidence gap without manufacturing a visual to fill it.

## 4. Required Separations

For Router, MoE, representation, or specialization experiments, keep these
objects separate:

| Object | Valid evidence | Forbidden substitution |
| --- | --- | --- |
| semantic dispatch | agreement with a held-out semantic label plus load audit | balanced load alone |
| expert utility | deletion, swap, forced-route, or another task intervention | route NMI or geometry alone |
| end-task performance | held-out task loss, F1, accuracy, or registered task metric | positive deletion utility |
| representation | registered probe, margin, scatter, or geometry with uncertainty | Router agreement alone |

When a meeting asks whether the method `works`, answer each applicable row
separately before giving the registered typed verdict. Use plain Chinese and
make the first visible metric the one closest to the meeting question.
