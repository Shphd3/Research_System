# 05_02 Feature Assumption Relaxation Anchor

## 0. Tiny Summary

Parent problem: ordinary top-1 MoE route consistency may reflect collapse, shortcut, or early lock-in rather than feature-level specialization.

Current subproblem: relax one simplifying feature assumption at a time and test whether route structure remains interpretable.

Core hypothesis: if ordinary top-1 truly follows target-relevant features, route structure should survive compositional tokens and structured many-feature grouping under non-collapse.

Minimal test: P1 compositional target-rule routing and P3 same-expert family grouping, both with target accuracy and load guards.

Current boundary: P1 and P3 are negative or bounded; target learning succeeds but routing often collapses or behaves like seed-dependent buckets.

Next decision: do not use assumption-relaxation results as positive specialization evidence until an explicit non-collapse or anti-lock-in guard changes P3b.

## 1. Problem Definition

Parent problem: the advisor's minimal baseline shows same-feature route consistency, but that does not establish useful expert specialization.

Sharper subproblem: test whether the result survives when tokens can contain multiple candidate features and when multiple features must share experts.

Decision question: under these relaxed feature assumptions, does ordinary top-1 produce target-relevant, non-collapsed structure, or mainly collapse and arbitrary early-locked buckets?

Not in scope: Zipfian frequency, real corpora, utility-binding claims, new router design, or treating inhibition as the main story.

## 2. Physical Prior

P1: compositional inputs expose route-axis ambiguity.
Meaning: if a routed context contains $S1$, $S2$, and nuisance $B_i$, changing the target rule should change the route axis.
Could be wrong if: the router follows a surface token, position, or early expert preference instead of the target-relevant factor.

P2: high consistency remains invalid under collapse.
Meaning: a route-axis metric is interpretable only when target accuracy is high and expert load is non-collapsed.
Could be wrong if: collapsed routes still show feature-specific utility, which was not tested here.

P3: when $F>E$, many-to-one assignment is unavoidable but need not be arbitrary.
Meaning: same-expert features should share family structure more than a load-matched random grouping if the router discovers a meaningful family relation.
Could be wrong if: top-1 forms useful groups only under a stronger load or utility intervention.

## 3. Hypothesis

H1: P1 target-rule-dependent routing.
Supported if: C1 routes by $S1$, C2 routes by $S2$, and C3 routes by $(S1,S2)$ under non-collapse and high accuracy.
Weakened if: C1/C2 collapse or routing follows a fixed surface axis independent of the target rule.

H2: P3 family-structured same-expert grouping.
Supported if: actual family purity is consistently above load-matched random, especially when same-family features share a family-level target.
Weakened if: P3a and P3b are near random, seed-unstable, or collapse-prone.

H3: inhibition is only a comparison condition in 05_02.
Supported if: inhibition changes load or grouping but does not rescue the assumption-relaxation claim.
Weakened if: inhibition robustly turns P1/P3 into non-collapsed positive evidence.

## 4. Minimal Mathematical Model

Objects: $route$ is the expert selected at the pre-target routed position; $F$ is the candidate feature label; $G$ is a family label; $E=4$ experts.

Core decomposition:

$$
P(route=e \mid x) = P(route=e \mid F_{\mathrm{target}}, F_{\mathrm{surface}}, \epsilon)
$$

Mechanism relation:

$$
\Delta_{\mathrm{family}} = \mathrm{Purity}_{actual} - \mathrm{Purity}_{load\ matched\ random}
$$

Observable metrics: target accuracy, max-load fraction, active experts, normalized mutual information between route and candidate axes, and $\Delta_{\mathrm{family}}$.

Falsifier: if target accuracy is high but non-collapsed routing does not track the target rule or family relation, ordinary top-1 route consistency is not robust under this relaxation.

## 5. Minimal Tests

Experiment: A05_02_P1_compositional_token_feature_routing.
Question: does route axis change with target rule when $S1$, $S2$, and $B_i$ appear in one context?
Intervention: use C1 $Y(S1)$, C2 $Y(S2)$, and C3 $Y(S1,S2)$ with matched seeds.
Primary metric: route-axis NMI after target accuracy and non-collapse guards.
Supports: H1 if the dominant axis follows the target rule across seeds.
Weakens: H1 if C1/C2 collapse or a fixed axis dominates.

Experiment: A05_02_P3_same_expert_feature_relation.
Question: do same-expert features share input family or target family more than load-matched random?
Intervention: P3a uses feature-level targets $Y_{gk}$; P3b uses shared family targets $Y_g$.
Primary metric: $\Delta_{\mathrm{family}}$ by seed and condition.
Supports: H2 if P3b is consistently stronger than P3a and both are non-collapsed.
Weakens: H2 if deltas are small, unstable, or collapse-contaminated.

Experiment: inhibition comparison within P1/P3.
Question: does the current inhibition candidate repair relaxed routing?
Intervention: compare B0 with I1 under the same data and seeds.
Primary metric: improvement in load-valid route structure, not consistency alone.
Supports: H3 if inhibition does not rescue the claims.
Weakens: H3 if it creates reliable non-collapsed structure.

## 6. Falsifiable Outcomes

Supported: target-rule routing appears under non-collapse in P1; P3b shows stable family-purity gain over P3a; inhibition improves valid structure.

Weakened: target accuracy is perfect but route load collapses; route-axis evidence is seed-local; P3 family-purity gain is near random or driven by one seed.

Insufficient evidence: target learning fails, the route position is inconsistent across conditions, or only averaged figures are available without seed-level load.

## 7. Current Evidence

Observation: P1 target accuracy is 1.000 in all condition groups, but C1/C2 mostly collapse; final-collapsed C1/C2 seeds are not collapsed at step 0 and are already collapsed by step 200.
Interpretation: easy one-factor targets can be learned without meaningful routing, and collapse is early-training lock-in rather than late drift.
Boundary: C3-B0 remains only a weak positive clue because it is the cleanest non-collapsed compositional condition.

Observation: P3 target accuracy is 1.000 in all condition groups, while mean $\Delta_{\mathrm{family}}$ ranges only from 0.047 to 0.090 and is seed-unstable.
Interpretation: shared family-level target utility did not reliably induce family grouping under ordinary top-1.
Boundary: this does not prove family grouping is impossible under a stronger router objective.

Observation: I1 does not repair P1/P3; it can increase concentration.
Interpretation: current inhibition is not a valid shortcut to positive assumption-relaxation evidence.
Boundary: other anti-lock-in or utility-binding interventions remain untested here.

## 8. Claim Boundary And Next Decision

Can claim: under the tested ordinary top-1 setup, relaxing single-feature and many-to-one assumptions weakens the route-specialization story; target learning survives, but valid route structure does not.

Cannot claim: no router can learn compositional or family grouping; C3-B0 is full specialization; P2 Zipfian frequency has been tested; or inhibition has been solved.

Next decision: treat ordinary top-1 same-expert assignment as arbitrary or early-locked unless a non-collapse or utility-binding guard produces seed-stable P3b family grouping.
