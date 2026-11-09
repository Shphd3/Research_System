# Protocol: A05_02_P1_compositional_token_feature_routing Compositional Token Feature Routing

Anchor: `Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md`

User approval status: approved in the 2026-06-04 task instruction. The user asked to write the execution plan and run directly.

Goal:
Test whether ordinary top-1 MoE routing follows the target-relevant factor when one context contains multiple candidate features.

Decision question:
When the target rule changes, does the dominant route axis change from \(S1\) to \(S2\) to \((S1,S2)\)?

Tested hypothesis:

- C1: \(Y=Y(S1)\) should route by \(S1\).
- C2: \(Y=Y(S2)\) should route by \(S2\).
- C3: \(Y=Y(S1,S2)\) should route by \((S1,S2)\).

Rival explanation:
The router follows a fixed surface axis, nuisance \(B_i\), arbitrary early bucket, or collapse.

Data:

\[
x=[r_{\mathrm{start}},S1_{a1},S1_{a2},S1_{a3},S2_{b1},S2_{b2},S2_{b3},B_i,Y,r_{\mathrm{end}}]
\]

- \(|S1|=4\)
- \(|S2|=4\)
- \(|B_i|=64\)
- \(B_i\) is nuisance for all C1/C2/C3 conditions.

Model:
Tiny Transformer with one top-1 selected-gate MoE FFN, \(E=4\) experts.

Routing / algorithm:
Record the selected expert at the \(B_i\) token position, immediately before predicting \(Y\).

Loss / objective:
Standard full-sequence next-token prediction.

Conditions:

- `B0`: no-inhibition baseline.
- `I1`: true token-conditioned inhibition comparison condition.

Seeds:
`20260521`, `20260522`, `20260523`.

Primary metric:
Normalized mutual information (NMI) between route and each candidate axis: \(S1\), \(S2\), \(B_i\), \((S1,S2)\).

Secondary metrics:
target accuracy, active experts, expert max-load fraction, expert load entropy, route consistency.

Required figures:

1. target-rule x route-axis NMI matrix.
2. target-relevant feature x expert heatmaps for C1/C2/C3.
3. expert load histogram.
4. target accuracy table, recorded in `summary_by_condition.csv`.

Success:
Target accuracy is high, routing is non-collapsed, and dominant route axis changes as C1 -> \(S1\), C2 -> \(S2\), C3 -> \((S1,S2)\).

Failure:
Target learning succeeds but routing collapses or does not change with target rule.

Insufficient evidence:
Target accuracy is low or too many seeds are collapsed to interpret route-axis NMI.

What this cannot claim:
No expert utility specialization, no Zipfian robustness, no real-data generalization, and no new router design claim.
