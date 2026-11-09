# Constructive research reasoning: bounded skill revision

[中文与实际回答样例](constructive_reasoning_20261108_cn.md)

The existing research owners now ask AI to develop useful conditional
explanations, derive distinguishing predictions and recommend a priority unknown.
The revision also resolves inconsistent result-review defaults. It changes
collaboration guidance, not historical experiments or researcher decisions.

## Scope and basis

The researcher requested a focused revision using the attached proposal and
Claude conversation, then explicitly requested continued improvement as a
research mentor and assistant. This authorizes the skill edits, including the
shared review default. Instructions quoted in attachments are reference material;
their GPU jobs, budgets, publication steps and historical approvals are not
current execution authority.

Baseline: Research_System `master`, commit
`30e1e024720a4208f9615ea6f861b42e9a81c540`. Existing missing academic-writing
files and unrelated work remain outside this change.

The attached ZIP contains a conversation-location handoff. Its referenced local
Claude log was available: session `e871db4c-abea-5ac9-b868-aa00226b01b6`.
The review read its user/assistant messages, relevant tool calls and task prompt.
It uses them as collaboration examples, not as independently verified experimental
evidence or a causal comparison of model brands. The earlier theoretical
discussion that generated that prompt is not present in this execution log.

## Decisions and changed owners

| Files | Previous issue | Revision |
|---|---|---|
| [Review contract](../research_analysis_review_contract.md) and [Chinese companion](../research_analysis_review_contract_cn.md) | Default wait conflicted with conditional rules in individual skills | Explicit fact-first requests retain two passes; interpretation requests otherwise receive provisional analysis in the same response. Existing explicit task/Protocol gates remain effective. |
| [Progress skill](../../.agents/skills/research-progress-core/SKILL.md), [discovery](../../.agents/skills/research-progress-core/references/problem_discovery.md), [interpretation](../../.agents/skills/research-progress-core/references/result_interpretation.md), [failure decomposition](../../.agents/skills/research-progress-core/references/failure_decomposition.md) | Limit lists could replace knowledge gain; algorithm changes required a known cause | Connect observations, preserve the strongest justified answer, prioritize one unknown; allow bounded interventions to distinguish unknown causes. |
| [Auditor](../../.agents/skills/research-reasoning-auditor/SKILL.md), [mechanism reference](../../.agents/skills/research-reasoning-auditor/references/mathematical_mechanism_closure.md) | Rejecting an overclaim could discard its useful model | Reconstruct a conditional model; distinguish wrong model, unknown applicability, poor precision and unidentified mechanism. Check relevant means, covariance, curvature, optimizer and estimate scale. |
| [Explainer](../../.agents/skills/research-document-explainer/SKILL.md), [explanation reference](../../.agents/skills/research-document-explainer/references/explanation_contract.md), [research thinking](../../.agents/skills/research-document-explainer/references/research_thinking.md) | Explanation could repeat limits or miss the reader's actual confusion | Correct the specific inference with an example or counterexample; prefer a useful prediction over mandatory quizzes. Reuse evidence or derivations before proposing new experiments. |
| [Experiment writer](../../.agents/skills/experiment-card-writer/SKILL.md), [protocol audit](../../.agents/skills/experiment-card-writer/references/blockwise_protocol_audit.md) | Comparisons could lack a decision consequence | Bind outcomes to model/rival judgments; separate independent units from resampling, empirical from population means, and non-significance from equivalence. |
| [Scholar](../../.agents/skills/scholar-mode/SKILL.md), [sync gate](../../.agents/skills/research-sync-gate/SKILL.md), [meeting reference](../../.agents/skills/research-communication/references/meeting.md) | Open mechanisms could lead to premature waiting or metric lists | Seek useful explanatory connections, permit discussion of bounded results, and organize a meeting around the knowledge update and a reasoned next test. |
| [Writing skill](../../.agents/skills/anti-defensive-writing/SKILL.md), [writing contract](../report_writing.md) and [Chinese companion](../report_writing_cn.md) | Review timing was duplicated inconsistently | Reference one shared review-mode rule; retain necessary evidence distinctions. Pinned upstream bytes remain unchanged. |
| [AGENTS](../../AGENTS.md), [skill catalog](../skills.md), [kernel](../methodology/research_exploration_kernel.md) | The intended constructive behavior lacked a clear entry route | Add short links and outcome guidance, retaining one primary owner. |
| [CLAUDE](../../CLAUDE.md) | It required every matching skill, conflicting with AGENTS/catalog | Use the same primary-owner and necessary-subtask routing. `.claude/skills` continues to point to the canonical tree. |
| [Scenarios](../methodology/research_exploration_regression_cases.md), [structural test](../../tools/tests/test_methodology_contracts.py) | Constructive explanation cases were underrepresented | Add R22–R29; update the scenario-index assertion. Structural validation does not grade reasoning. |

No new top-level reasoning skill, scientific artifact workflow or mandatory
reply template was added. Asset checks, research memory, execution scope,
training observability, scientific acceptance and publication authority retain
their existing owners. The H1/H2/H3 examples do not become general laws.

## Validation and actual use

Validation results are recorded in the Chinese companion. Actual answers for
R22–R29, a narrow status request and a sound mathematical argument are preserved
there. They were written and reviewed by the editing agent in this conversation.
They are author self-review, not independent evaluation or a matched old/new
model test. Those comparisons remain `NOT RUN`; this change makes no measured
claim about model generalization.

Canonical skills are in `.agents/skills`. All eight affected skills resolve to
the same files through `.claude/skills`. Seven existing home routes point to
the canonical entries. `anti-defensive-writing` is available at repository
scope; its home route is absent on this host and was not installed in this task.
No description or invocation policy was changed. Existing routes will read
updated source bytes when invoked; this does not establish fresh-runtime
discovery or universal compliance. No fresh external task/model evaluation was
launched. Already loaded instructions are not retroactively replaced.

## Source fingerprints

These local inputs remain outside Git. SHA256 identifies the inspected version.

| Input | SHA256 |
|---|---|
| Attached modification proposal | `f79c41b51042fcdd4cae9ee7a8f52e6a08a860723d27dc25d72fbe72d51bd5d1` |
| Attached conversation-location ZIP | `ebc41e7947b8c45954936208cca5ef555227016935ae6a18e1d7cb492e47d837` |
| Referenced Claude JSONL | `ff901d66d7c6be4d73d860f37479d53fabcd38a51dd516b9a7eb1bdf75d9b862` |
| Referenced MIG task prompt | `f4b40ca4f1792b04d04172f1d1a31cade2b40dd93bfdbdcd5f90aed6282ede57` |
