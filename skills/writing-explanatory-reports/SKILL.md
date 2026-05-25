---
name: writing-explanatory-reports
description: Use when writing or revising detailed experiment reports, experiment detailed.md files, result analyses, metric explanations, tables/figure interpretations, Markdown reports, or HTML reports under experiments/ where the user needs to understand Codex-run work and make a decision from incomplete context.
---

# Writing Explanatory Reports

Use this skill to write precise, concise, explanatory reports for experiment
execution and result analysis, especially `experiments/<id>/detailed.md` and
substantial `summary.md` support material. The report is not a lab log. It is a
reasoning artifact that returns context and decision power to the user.

Core standard: **precise and concise does not mean terse. Every explanation must earn its place, but necessary context, metric meaning, reasoning, and limits must be explicit.**

## Reader Model

Assume the user may have provided a vague idea, delegated clarification and experiments to Codex, and is now using the report to understand what happened. Before writing, identify:

- What original vague idea or question this report resolves.
- What decision the user needs to make after reading.
- What context the user may have missed while Codex worked.
- Which metrics, terms, or baselines need explanation inside the report.
- What conclusion would be tempting but unsupported.

If these are unclear and cannot be inferred from files, ask at most one clarifying question. Otherwise infer and state assumptions in the report.

## Report Goal

A good report supports three reading modes:

- **2 minutes:** what was tested, what was found, what decision follows.
- **10 minutes:** why the conclusion follows from the evidence.
- **Audit:** whether Codex over-interpreted the experiment.

Prefer explanation that helps judgment over exhaustive detail.

## Meeting / PRISM-Style Reports

When the report is for a group meeting, advisor update, or PRISM-style document,
it is still a mainline-facing decision report, not a chronology. Start from the
scientific question and organize evidence by claim.

Default meeting-report location:

```text
daily_research_reports/MMDD/meeting/
daily_research_reports/MMDD/meeting/prism/
```

Use this structure unless a project template is named:

```markdown
# Meeting Report - <topic/date>

## 1. Report Purpose
## 2. Research Background
## 3. Current Hypothesis
## 4. Modeling / Mechanism
## 5. Empirical Evidence
## 6. Current Interpretation
## 7. Claims To Downgrade
## 8. Next Iteration
## 9. Meeting Version
```

For each evidence block, state:

- experiment or observation;
- what it supports;
- what it weakens;
- what alternative explanation remains.

## Figure Evidence Standard

Reports and closures should use figures as evidence, not decoration. Every
central figure must be embedded near the claim it supports, and every embedded
figure must have a one-sentence caption below it that says exactly what the
figure supports or weakens.

For project-local committed reports, use paths relative to the report file or
relative to `Projects/<project>/`; avoid absolute local/remote paths except in a
compact artifact map for raw remote outputs. If a figure is needed for
reliability audit, generate it in the remote experiment workspace and commit the
curated PNG plus the report text from the remote repo before pulling locally.

When useful, add at most 2-3 likely advisor questions:

```markdown
## Likely Questions

### Question
Short answer:
Evidence:
How to redirect back to the mainline:
```

Assume the advisor knows the high-level topic but not the implementation
details. Before showing metrics, explain what object is being tested, why the
controlled experiment is needed, what the metric means, and what the safest
current claim is.

## Default Structure

Use the shortest structure that preserves understanding. For most experiment reports:

1. **Title** - name the object and judgment type, not just the topic.
2. **TL;DR / 摘要** - 3-6 sentences: conclusion, key evidence, boundary, next move.
3. **This report answers / 这轮在回答什么** - translate the vague idea into a precise question.
4. **Why this was needed / 为什么做这轮** - restore necessary prior context in 1-3 short paragraphs.
5. **Decision / 先读结论** - state what should and should not happen next.
6. **How to read the metrics / 指标怎么读** - define each important metric by what it answers, what it cannot answer, and how conflicts are resolved.
7. **Experiment setup / 实验设置** - enough detail to audit, not a run log.
8. **Main results / 主要结果** - tables or figures plus immediate interpretation.
9. **From result to judgment / 从结果到判断** - make the inference chain explicit.
10. **Not proven / 这轮没有证明什么** - prevent overclaiming.
11. **Next step / 下一步** - few actions, each with a reason.

Do not force all sections when a shorter report is clearer.

## Project Location

Default locations:

```text
Projects/<project>/main/experiments/<experiment_id>/detailed.md
```

Do not create worker-local `main/` folders such as
`Projects/<project>/<worker>/main/`. Worker folders can hold sync reports and
remote code-workspace notes, but detailed evidence reports belong under the
canonical project `main/`.

Use `summary.md` for the short decision-facing result. Use `detailed.md` for
metric explanations, setup details, tables, figure interpretation, seed notes,
failed-run analysis, and audit trail.

Implementation audit rule: when an experiment uses a nontrivial intervention or
diagnostic implementation, `detailed.md` must include enough operational detail
for another researcher to audit the result without reading the chat. This
especially applies to router/model initialization, custom losses, ablations,
dispatch rules, data sampling, probe construction, surrogate gradients,
interventions, and stopping gates. Record the code path/function, config fields,
objects being computed, formulas or pseudocode, hyperparameters, and what the
implementation is **not** doing when that distinction affects the claim.

Do not use this skill for hypothesis closures by default. Closures should use
`hypothesis-closure` and should be shorter, self-contained, and claim-focused.

## Reasoning Discipline

Separate these layers:

- **Observation:** measured result, table value, run outcome.
- **Interpretation:** what the observation suggests.
- **Decision:** what to do next.
- **Boundary:** where the interpretation stops.

Use explicit chains when helpful:

`observed X -> suggests Y -> but because Z, only supports W`

Every strong claim needs its boundary. Especially mark limits from small samples, proxy metrics, oracle upper bounds, synthetic tasks, failed runs, baselines that are not equal-budget, and implementation caveats.

For synthetic experiments, explicitly separate:

- feature-level specialization;
- function-level specialization;
- routing-level specialization;
- transfer to real hidden states.

## Metric Explanation

For important metrics, do not only define the formula. Explain:

- What question the metric answers.
- What failure mode it catches.
- What it cannot prove.
- Which metric should dominate when metrics disagree.

Example pattern:

`mass` measures how much full-attention probability the candidate set covers. It is useful for fidelity, but it does not prove answer behavior is preserved. If `mass` looks good while answer logprob or logits agreement degrades, trust the behavior metric for decision-making.

## Tables And Figures

Every table or figure must have a nearby plain-language interpretation. The user should not need to infer the conclusion from numbers alone.

If figures exist and are central to the result, the report must include the most
important report-ready figure(s), not only text or tables. A result report should
show the evidence that makes the conclusion visible, then explain what the
reader should see in the image.

Good table commentary names:

- the largest relevant contrast,
- the baseline that matters,
- whether the difference changes the decision,
- and the caveat.

Avoid dumping full raw outputs unless the report is explicitly archival.

## Markdown Rules

Markdown is the source of truth. Prefer:

- clear headings,
- compact paragraphs,
- tables for comparable numbers,
- bullets only for scan-friendly claims,
- code spans for exact method names, metrics, run names, paths, and commands.

Keep terminology stable. If a report uses mixed Chinese and English technical terms, preserve exact method and metric names.

## HTML Rules

HTML should improve readability without changing the logic. If producing HTML:

- keep the Markdown structure as the content source,
- surface TL;DR, decision, metric guide, and not-proven sections early,
- use readable typography, sticky navigation, responsive tables, and simple section cards,
- avoid decorative complexity that competes with the evidence,
- ensure tables and figures are legible on mobile and desktop.

## Common Mistakes

- Writing a chronology instead of a decision report.
- Explaining methods but not the decision they enable.
- Treating proxy metrics as final evidence.
- Hiding uncertainty in vague language.
- Saying what improved without naming the baseline.
- Listing next steps without explaining why those are the right next steps.
- Making the report terse where the user needs reconstruction of context.

## Final Self-Check

Before delivering, verify:

- Can the user state the main conclusion after reading only the TL;DR?
- Is the original vague idea translated into a precise question?
- Are observation, interpretation, decision, and boundary separated?
- Does every key table or chart have an interpretation?
- Is there a clear "not proven" section for nontrivial experiments?
- Are next steps few, justified, and decision-relevant?
