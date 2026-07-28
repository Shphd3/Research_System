# Protocol: A05_02_P3_same_expert_feature_relation Same-Expert Feature Relation

Anchor: `Projects/from-attention-to-search/main/problem_anchors/05_failure_mechanism/05_02_feature_assumption_relaxation_anchor.md`

User approval status: approved in the 2026-06-04 task instruction. The user revised P3 into P3a/P3b and asked to run directly after the execution plan.

Goal:
Test whether multiple features assigned to the same expert form family-structured groups rather than arbitrary buckets.

Decision question:
Does same-expert grouping share ground-truth family more than a load-matched random baseline?

P3a: input-family-only grouping

Purpose:
Test whether the router groups features by input-side family structure alone.

Data:

- $G=4$ families.
- $K=4$ features per family.
- $f=(g,k)$.
- $F=16$ total features.
- $E=4$ experts.
- uniform feature distribution.

Sequence:

$$
x=[r_{\mathrm{start}},G_{g1},G_{g2},G_{g3},F_{gk1},F_{gk2},F_{gk3},Y_{gk},r_{\mathrm{end}}]
$$

Target:
Each feature has its own unique target $Y_{gk}$.

P3b: input-family + target-family grouping

Purpose:
Test whether the router groups features when same-family features also share prediction utility.

Data:
Use the same $G=4$, $K=4$, $F=16$, $E=4$ structure.

Sequence:

$$
x=[r_{\mathrm{start}},G_{g1},G_{g2},G_{g3},F_{gk1},F_{gk2},F_{gk3},Y_g,r_{\mathrm{end}}]
$$

Target:
All features within the same family share $Y_g$.

Model:
Tiny Transformer with one top-1 selected-gate MoE FFN.

Routing / algorithm:
Analyze routing at the last $F_{gk}$ token position, immediately before predicting $Y_{gk}$ or $Y_g$.

Loss / objective:
Standard full-sequence next-token prediction.

Conditions:

- `B0`: no-inhibition baseline.
- `I1`: true token-conditioned inhibition comparison condition.

Seeds:
`20260521`, `20260522`, `20260523`.

Primary metric:
Family purity over load-matched random baseline:

$$
\Delta_{\mathrm{family}}=\mathrm{Purity}_{actual}-\mathrm{Purity}_{random}
$$

Secondary metrics:
target accuracy, active experts, expert max-load fraction, expert load entropy, route-family NMI, route-feature NMI.

Required figures:

1. Expert x feature heatmap ordered by family.
2. Expert x family composition heatmap.
3. Family purity vs load-matched random baseline.
4. Expert load histogram.
5. Target accuracy table.

Decision rule:

- P3a positive: input-side family alone can induce structured grouping.
- P3b positive but P3a negative: shared target utility is needed for grouping.
- Both negative: same-expert assignment is closer to arbitrary bucket.
- Collapse or low accuracy: invalid for positive grouping claims.

What this cannot claim:
No expert utility specialization, causal expert function, Zipfian robustness, real-data generalization, or new router design.
