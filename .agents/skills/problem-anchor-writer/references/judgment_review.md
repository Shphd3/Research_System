# Researcher Judgment And Design Readiness

Use only for a new or reopened scientific core, including clarification before
a formal Anchor. It does not require a new Focus or a separate judgment file.

## Human Account

For a new or reopened scientific core, reuse the researcher's explicit account
already present in the request, session or active Focus. Ask only for missing
decision-bearing items; do not re-request approved direction or require a new
intake form. The account covers:

```text
Parent research direction or problem:
Phenomenon:
Mechanism guess:
Strongest rival explanation:
Most uncertain point:
Evidence that would change my mind:
Current blocking uncertainty:
Why this decision is needed now:
Current next decision:
Known source material, or Unknown:
```

The human may mark an item `unknown`. Do not manufacture a confident answer.
Keep this judgment in the active Focus or the conversation until it is approved
for formalization in the Anchor.

## Short AI Audit

Before a formal anchor, return a short audit:

```text
Judgments to preserve:
Direction placement and why this question is next:
Unclear definitions:
Hidden assumptions or causal overclaims:
Strongest rival still alive:
Can the proposed metric separate the rivals?:
Smallest falsifier:
Grounding gaps and source links needed:
AI-proposed correction, if any:
```

Label every AI-added prior, variable, metric, or model as a proposal. Formalize only the direction the human has corrected or approved; an existing
explicit approval satisfies this requirement.

## Grounding And No-Invention Gate

Every decision-bearing statement must be grounded in an explicitly confirmed
human judgment, an approved parent Anchor, or a verified linked artifact. An
AI-added prior, definition, variable, metric, threshold, mechanism, or claim
must remain labeled `AI_PROPOSAL` until the researcher approves it.

When required information is absent, write `Unknown` or `BLOCKED`, state why it
matters, and link the most direct artifact that could resolve it. Do not infer a
claim from a filename, run ID, expected pattern, neighboring Anchor, or missing
result. A link supports audit; the Anchor must still state the local meaning
needed to understand its question and boundary.

## Formalization Gate

The approved researcher account must support all of these:

- exactly one phenomenon and one decision question;
- the parent direction, current blocking uncertainty, and why this is the
  smallest decision that can change the direction;
- one mechanism guess with a stated causal direction;
- the mechanism-selection decision and source-grounded alternatives when prior
  work materially changes what computation is admissible;
- a minimal variable set;
- one primary observable metric;
- at least one live rival explanation;
- pass, fail, and insufficient-evidence meanings;
- one next decision;
- a conservative cannot-claim boundary.

If the metric cannot distinguish the mechanism from its rival, return to the
researcher account. More experiments do not repair an undefined decision.

## Physical-Prior Review

Before writing the anchor, check:

```text
Candidate physical prior:
Why it follows from the human judgment:
What would make it false:
Variable that exposes it:
Rival explanation it separates:
```

## Mathematical-Model Review

Then check:

```text
Core model:
Variables:
Mechanistic relation:
Observable metric:
What the model explains:
What it cannot explain:
Mismatch with the human intuition:
```

Every equation must map to a prior, a concrete computation, and an experiment
or analysis artifact. Do not promote a metaphor into a mathematical claim.
