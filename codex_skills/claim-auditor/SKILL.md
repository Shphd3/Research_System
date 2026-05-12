---
name: claim-auditor
description: Use when checking whether research conclusions, meeting claims, experiment interpretations, or paper/report statements exceed the available evidence.
metadata:
  short-description: Audit research claims
---

# Claim Auditor

Audit claims against evidence and update claim boundaries.

## Required Output

For each claim:

```markdown
## Claim

Status: supported / weakly supported / unsupported / contradicted / unclear

Evidence:

Counter-evidence or limitation:

Public wording:

What not to say:
```

## Rules

- Read `claim_board.md` when available.
- Separate result, interpretation, claim, and speculation.
- Synthetic evidence cannot automatically justify real-language claims.
- If an oracle result proves recoverability, do not treat it as learned-model success.
- Prefer weaker but defensible claims for meetings.
- When writing Markdown research documents, inline formulas must use `$...$` and display formulas must use `$$...$$`.
