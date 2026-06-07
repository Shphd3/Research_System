# Prompt: Revise 05_03 Minimal Anchor Into A Concise Decision Anchor

You are helping revise a research anchor. Do not expand the research scope. Do not write a long report. Preserve the user's current judgment unless it is logically unsupported.

## Inputs

Read:

```text
1. minimal_anchor.md
2. audit_report.pdf or its markdown source
3. research_handoff_0605.md, especially current decision and claim boundary
4. 05_03_concise_anchor_v2.md if available
```

## Task

Rewrite the anchor into a concise, rigorous markdown document.

Target length:

```text
1200-1800 words maximum.
```

The anchor must be readable in one pass and must make the decision logic obvious.

## Required Structure

```text
0. 汇报前 Summary
1. Problem Definition
2. Operational Definitions
3. Physical Priors
4. Mechanistic Hypothesis
5. Mathematical Modeling
6. Computational Realization
7. Minimal Falsifiable Tests
8. Falsifiable Outcomes
9. Current Evidence
10. Claim Boundary And Next Decision
Appendix A. What We Are Not Doing In This Iteration
Appendix B. One-Minute Alignment Check
```

## Locked Research Question

Use this as the decision question unless there is a strong reason to improve wording:

```text
在 verified uniform data 和 verified random router init 下，collapse 是否主要来自 hidden common component 通过 linear gate 产生的 expert-specific common offset？如果是，去除或控制这个 offset 是否能减少 collapse，同时保持 target learning？
```

## Required Mechanistic Core

The anchor must include this decomposition:

```text
h_f = c + r_f + epsilon_f
z_e(f) = w_e^T h_f = w_e^T c + w_e^T r_f + w_e^T epsilon_f
```

Interpretation:

```text
w_e^T c is an expert-specific common offset. It behaves like a bias even when the router has no explicit bias parameter.
```

## Required Boundaries

Explicitly state that the current anchor does not answer:

```text
compositional feature routing
Zipfian frequency
real data
full LM behavior
whether router-selected expert is utility-best
whether anti-lockin is solved generally
```

## Required Appendix

Add an appendix named:

```text
Appendix A. What We Are Not Doing In This Iteration
```

It must include at least:

```text
1. Not continuing P1/P3/P2 feature-assumption relaxation.
2. Not claiming common direction is already the unique root cause.
3. Not using unstable per-batch mean subtraction or broad SVD removal as main claim.
4. Not changing data construction and router intervention in the same experiment.
5. Not equating better load balance with better specialization.
6. Not doing a broad literature review before minimal tests are queued.
7. Not claiming real-data applicability.
```

## Style Requirements

Use concise, precise language.

Avoid:

```text
- broad survey language
- motivational filler
- overclaiming
- vague phrases like “maybe useful” without a metric
- too many hypotheses
- turning the anchor into a runbook
```

Prefer:

```text
- one decision question
- one primary mechanism
- explicit rival explanations
- direct support / weakened / redirected criteria
- observation -> interpretation -> claim boundary
```

## Self-Audit Checklist

Before finalizing, answer:

```text
1. Can the decision question be quoted in one sentence?
2. Is the physical phenomenon distinct from the hypothesis?
3. Is the hypothesis falsifiable by a minimal test?
4. Does every test update the same anchor?
5. Does the appendix prevent scope creep?
6. Are unsupported claims removed or marked as hypotheses?
7. Would a collaborator understand what experiment to run next?
```

Return only the revised markdown anchor.
