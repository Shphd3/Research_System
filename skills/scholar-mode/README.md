# Scholar Mode

`scholar-mode` is a Codex skill for research-oriented conversations: academic analysis, literature reading, paper critique, theory building, methodology critique, research notes, and evaluation of research intuitions.

The active skill entrypoint is `SKILL.md`.

## Design Goals

This skill is designed to make the agent behave like a research collaborator rather than a coding agent.

Core goals:

- Prioritize conceptual precision, evidence quality, argument strength, and readable synthesis.
- Avoid turning research questions into code, architecture, project plans, roadmaps, repository scans, or implementation tasks.
- Treat user examples and analogies as provisional material, not as authoritative facts or implicit continuation tasks.
- Clarify ideas before judging them: identify the claim, hidden assumptions, scope, missing baseline, and falsification conditions.
- Avoid generic verdicts such as `partly right` unless they name the exact subclaim that holds and the exact subclaim that fails.
- Use related concepts to sharpen analysis, not to prematurely absorb a new idea into an existing label.

## Role In Research System

This is an upstream research-judgment skill. Use it before artifact-oriented skills when the task is still about whether an idea, analogy, hypothesis, or framing is well-defined and evidence-aligned.

It should not replace:

- `problem-anchor-writer` for anchor / purpose-card documents.
- `experiment-card-writer` for execution plans.
- `research-mainline` for project-state consolidation.
- `handoff-report-writer` for optional meeting or collaborator handoff reports
  after the anchor, summary, and detailed record are already updated.

## Maintenance

Keep the active entrypoint as `SKILL.md`.

Before promoting a new version, test it with pressure cases that include:

- examples that may be wrong;
- prompts that try to make the agent continue a pattern;
- strong but underspecified research intuitions;
- implementation requests that should not trigger scholar-mode;
- research requests that should trigger scholar-mode.
