# 04 Judgment Cheatsheet

## 1. Mentor Loop

```text
hypothesis -> operational definition -> minimal test
-> metric + visual evidence -> failure analysis -> refined hypothesis
```

One loop should reduce one uncertainty, not produce many facts.

## 2. What The User Must Judge

For every AI-generated theory, plan, or result summary, judge only five things:

1. Object: is the AI testing the object I care about?
2. Claim: is the claim route-pattern, utility-aligned, or something else?
3. Metric: what judgment does this metric support, and what can it not support?
4. Rival: what other explanation could produce the same observation?
5. Decision: does this change the hypothesis, claim boundary, or next step?

If these five are unclear, do not run the next experiment yet.

## 3. What AI May Draft

AI may draft:

- theory derivation candidates;
- experiment plans;
- metric tables;
- result summaries;
- rival explanations;
- advisor-facing oral reports.

The user must approve:

- the hypothesis;
- the operational definition;
- success / failure / insufficient evidence;
- the primary metric;
- the claim boundary;
- the next decision.

## 4. Metric-To-Claim Rule

Every metric must be translated into a claim boundary:

```text
metric observation -> supports what -> cannot claim what -> next decision
```

Example:

```text
route-feature alignment is high
-> supports router-level feature separation
-> cannot claim expert utility alignment
-> next decision: test expert utility or remove favorable prior
```

## 5. Advisor Version

After experiments, explain in this order:

1. Purpose: what uncertainty did I try to reduce?
2. Model: what physical or mathematical picture did I test?
3. Test: what was the smallest experiment?
4. Result: what happened on the primary metric?
5. Interpretation: what explanation is supported or weakened?
6. Boundary: what can I not claim yet?
7. Next: why is the next step the highest-value step?

Keep the advisor version short. Do not report every run; report the decision.

