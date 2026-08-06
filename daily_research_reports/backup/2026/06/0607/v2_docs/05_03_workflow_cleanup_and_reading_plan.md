# 05_03 Workflow Cleanup And Reading Adjustment

## 1. Current Process Evaluation

You are moving in the right direction because you did three important things:

```text
1. You wrote a minimal anchor before accepting a formal anchor.
2. You forced a code/data/init audit before interpreting collapse.
3. You are now asking for protocols before running broad experiments.
```

The main remaining issue is not effort. It is **alignment compression**: you need to reduce every iteration to one decision question before reading papers, running experiments, or writing meeting material.

## 2. Low-Efficiency Patterns To Remove

### Pattern A: Reading a long formal anchor without re-outputting it

Problem:

```text
You feel you understand parts of it, but you do not own the decision logic.
```

Fix:

```text
After reading any AI-written anchor, write a 6-line compression:
1. problem
2. phenomenon
3. hypothesis
4. primary metric
5. failure condition
6. next decision
```

If you cannot write this, the anchor is not aligned yet.

### Pattern B: Mixing anchor, protocol, report, and literature in one mental workspace

Problem:

```text
You start feeling that every task depends on every other task.
```

Fix:

```text
Anchor decides what matters.
Protocol decides how to test it.
Experiment produces observations.
Summary decides claim boundary.
Literature only supports interpretation after the decision question is clear.
```

### Pattern C: Treating visual improvement as mechanism evidence

Problem:

```text
Cleaner route heatmaps can come from arbitrary balancing, not feature-level specialization.
```

Fix:

```text
Always write:
metric observation -> supports what -> cannot claim what -> next decision
```

### Pattern D: Running correction methods before defining the nuisance source

Problem:

```text
Batch mean and broad SVD can remove both nuisance and task signal.
```

Fix:

```text
First identify source and score: c, w_e^T c, source alignment.
Then intervene at the most targeted level: z'_e = z_e - w_e^T c.
```

## 3. New Iteration Rule

Each research iteration must fit this template:

```text
One phenomenon:
Uniform data still collapses.

One hypothesis:
Shared hidden component creates expert-specific common offset.

One primary intervention:
Cancel/equalize w_e^T c before routing.

One primary metric:
Early/final max_load and collapse rate, with target accuracy preserved.

One decision:
Proceed to common-aware init / anti-lockin, or redirect to expert utility / top-1 dynamics.
```

## 4. Reading Plan Adjustment

Do not let paper reading block the closure experiment.

Recommended priority:

```text
1. Queue or prepare the minimal common-offset experiment first.
2. Read only router/init/load-balancing sections needed for the meeting brief.
3. Continue the assigned paper after the experiment is running.
```

### Minimal reading block for this iteration

Time box: 75-100 minutes.

Read only:

```text
1. Switch Transformer: router form, load-balancing loss, reduced initialization scale.
2. ST-MoE: router z-loss / stability motivation.
3. Auxiliary-loss-free balancing: dynamic expert-wise routing bias.
4. Any assigned paper section directly related to routing initialization or load balancing.
```

Output after reading:

```text
5 bullets maximum:
- what method does
- what problem it solves
- what it does not solve
- connection to common-offset hypothesis
- whether to test now or park
```

## 5. System AI Collaboration Protocol

When sending work to system AI, include:

```text
1. Anchor decision question.
2. Locked baseline and seeds.
3. One variable to change.
4. Required output tables.
5. Required success/failure/insufficient-evidence criteria.
6. Claim boundary.
```

Do not ask system AI to “explore broadly” unless the anchor has already been closed.

## 6. Meeting Brief Rule

Meeting brief should not be a timeline. It should be a decision report:

```text
1. We audited code/data/init.
2. What bug explanations are now weaker.
3. What mechanism is now strongest.
4. What decisive intervention we will run.
5. What result would support / weaken / redirect the hypothesis.
```

## 7. Personal Working Rule For This Iteration

Before the next group meeting, your goal is not to solve MoE collapse generally.

Your goal is:

```text
Give a clean answer to:
"In this uniform toy setting, is collapse mainly driven by common-offset routing or not?"
```

Everything else is secondary.
