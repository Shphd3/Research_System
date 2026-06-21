# Meeting Brief: <topic>

Use this for advisor or group-meeting reporting. The first goal is that the
advisor can quickly understand what problem is being solved. The brief is not
an experiment retelling; it reports how the researcher's judgment changed.

Source of truth:

```text
anchor -> protocol.md -> summary.md -> detailed.md -> anchor update
```

Use `summary.md` for the main conclusion and central figures. Use
`detailed.md` only to check setup, numbers, and evidence boundary.

## Mode A: Cognitive-Update Brief

Use this when one anchor or one experiment line produced the main update.

```markdown
# Meeting Brief: <topic>

## 0. One-Sentence Update

This work updates my judgment from <old/uncertain view> to <new bounded view>.

## 1. Problem

Main problem:

Why this matters:

Current subproblem:

Decision question:

## 2. Updated Judgment

Main conclusion:

1.
2.
3.

No longer safe to say:

-

More accurate wording:

-

## 3. Evidence Supporting The Update

### Evidence 1: <plain title>

What was tested:

Result:

What this rules out:

What this supports:

Figure:

### Evidence 2: <plain title>

What was tested:

Result:

What this rules out:

What this supports:

Figure:

## 4. Integrated Interpretation

How the evidence changes the mainline:

Remaining rival explanation:

Why the current boundary is still narrow:

## 5. Boundary

Can claim:

Cannot claim:

## 6. Next Decision

Meeting decision needed:

Next minimal experiment or action:

## 7. Source Map

Anchor:

Protocol:

Summary:

Detailed:

Figures:
```

## Mode B: Merged Brief

Use this when several days, anchors, or experiment summaries must be reported
together. Do not concatenate old briefs. Merge by main research question and
cognitive update.

```markdown
# Meeting Brief: <merged topic>

## 0. Top-Level Update

Across <days / experiment lines>, my judgment changed from <old view> to
<new bounded view>.

## 1. Shared Problem

Main problem:

Why this matters:

Subquestions merged:

1.
2.
3.

## 2. Merged Mainline Judgment

Higher-level conclusion:

1.
2.
3.

What is now ruled out or weakened:

-

What remains unresolved:

-

## 3. Evidence Modules

### Module A: <source summary / anchor>

Question answered:

Key result:

Mainline update:

Central figure:

### Module B: <source summary / anchor>

Question answered:

Key result:

Mainline update:

Central figure:

## 4. Cross-Result Interpretation

How the modules fit together:

Conflict or tension between results:

What the combined evidence still cannot claim:

## 5. Boundary

Can claim:

Cannot claim:

## 6. Next Decision

Meeting decision needed:

Next minimal experiment or action:

## 7. Source Map

Included anchors:

Included summaries:

Included detailed records:

Included figures:

Excluded material and why:
```

## Rules

- Start from the problem, not from experiment IDs.
- State the judgment update explicitly.
- Use only conclusions already supported by the anchor, `summary.md`, and
  `detailed.md`.
- Use only central figures that support the current claim boundary or next
  decision.
- Keep setup short; define only objects needed to understand the evidence.
- If multiple briefs disagree, preserve the disagreement as an unresolved
  boundary instead of forcing a single stronger claim.
