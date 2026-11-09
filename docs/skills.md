# Repository skills

Canonical skills live in `.agents/skills/<name>/`. Pick one primary owner; add
another only for a distinct necessary subtask. Read its `SKILL.md`, then only the
references it routes to.

## Exploration lane (default: 3 skills)

| Need | Skill |
|---|---|
| Choose or refine a question, a minimal falsifier, interpret a result | `research-progress-core` |
| Audit an inference, mechanism, rival or proxy | `research-reasoning-auditor` |
| Run or inspect an authorized remote/container job | `remote-experiment-workflow` |

## Formal lane or explicit request

| Need | Skill |
|---|---|
| Anchor / scientific design | `problem-anchor-writer` |
| Protocol, Summary, Detailed | `experiment-card-writer` |
| Meeting brief, Story, handoff | `research-communication` |
| Final report for a settled question | `research-final-report` |
| Explain a document or result | `research-document-explainer` |
| Prose editing | `anti-defensive-writing` |
| Conversation memory / continuation | `research-memory` |
| Advisor-readiness check | `research-sync-gate` |
| Place, archive or publish artifacts | `research-mainline` |
| Critique an unsettled idea or paper | `scholar-mode` |
| Research graph | `research-graph-sop` |
| Local Sidecar app | `sidecar-thinking` |

Skill selection grants no execution, approval or publication authority.

## Validation

Changed skills: `python tools/check_skills.py` plus the skill-creator
`quick_validate.py`. Independent repositories (e.g. NTP) install thin routes
with `python tools/install_skill_routes.py --backup <dir> --apply`; routes point
to the canonical source and never copy a second workflow.
