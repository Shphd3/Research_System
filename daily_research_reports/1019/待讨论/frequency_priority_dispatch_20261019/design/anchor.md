# Frequency first, coactivation second: from feature membership to actual input dispatch

Version: early-morning plan, 2026-10-19; to be frozen by the existing 11109 Agent before execution.

This English companion translates the [researcher-provided Chinese original](anchor_cn.md). The original scientific definitions and thresholds are retained. The implementation note at the end is separate from the translated source.

## Purpose in one sentence

With **8 experts and exactly 1 expert selected per token**, test whether routing intended to prioritize middle- and low-frequency features, with frequency as the primary grouping criterion and coactivation as an auxiliary criterion, can give target low-frequency features reception opportunities and improve the frequency composition of the inputs experts actually receive.

The parent goal remains greater effective MoE learning capacity under fixed parameter and compute budgets. This round tests dispatch only. It does not train experts or establish improved capacity or learning.

## 1. Established result and the present gap

The old scheme divided the range of raw activation probabilities into eight equal-width intervals and used the weighted mean activation over every member of a group to compete for top-1 routing. The highest-frequency expert received 91.68% of TRAIN inputs. All 964 features on the original low-frequency list had zero reception at their assigned experts.

In the previous diagnosis, setting the high-frequency set C's score terms to zero sent every input to expert 0. This was not a valid repair: C contained 962 features in the original highest-frequency 10%, and every member of groups 1–7 belonged to C. Zeroing C mechanically removed those seven groups' ability to compete.

**This round excludes the 10 features with the highest TRAIN frequency, not 10%. It rebuilds groups over the remaining candidates rather than retaining the emptied old groups.**

The comparison must separate changes due to regrouping, excluding the head features from scoring, and the additional use of coactivation relationships. Their effects must not be combined into one attribution.

## 2. Operational boundary

The researcher selected option A: the main comparison leaves model input representations, the CrossCoder, original activations, and prediction positions unchanged. Only routing candidates, groups, and scores change. Experts receive the complete original representation. The highest-frequency features therefore still accompany inputs into experts and must remain in the evaluation.

Removing the first singular direction is a separate diagnostic branch. As an exception, it changes the routing-side representation and re-encodes it; it does not alter expert inputs or combine all changes into a main method.

## 3. Mechanistic intuition and revisable hypotheses

### H1: excluding head features from routing can improve reception

The most common features may contribute large scores over many inputs and obscure the selecting role of middle- and low-frequency features. Excluding the first 10 and rebuilding candidate groups may improve low-frequency reception.

A non-supporting result is continued domination by the most frequent remaining group, or all inputs moving to another single group. This weakens the intuition that deleting only the head solves the problem. Examine the score definition next; do not increase the deletion count to obtain a favorable result.

### H2: coactivation relationships add dispatch value

At similar frequencies, preferentially placing features with stable positive coactivation relationships in the same group may reduce conflicts in which one input simultaneously calls for different experts.

A non-supporting result is no improvement in actual dispatch under the same score, or deterioration of frequency organization. Report that the relationship showed no additional value in this setting; more within-group edges cannot substitute for dispatch success.

### H3: the first singular direction affects routing selection

Subtracting the first singular direction from routing representations may change high-frequency responses and dispatch. This does not ensure that the direction represents common content or that the fixed dictionary remains well matched after re-encoding.

A non-supporting result is no dispatch improvement or substantially worse reconstruction. The latter indicates representation change and measurement compatibility problems; it does not establish successful removal of common content.

## 4. Two relationships have different roles

- **Frequency distance** compares log10 activation frequencies and measures relative frequency separation. Features with zero frequency are not candidates; the reliable pool remains frozen by the old protocol.
- **Coactivation relationship φ** asks whether two features activate at the same prediction position more often than expected from their marginal frequencies. It is not decoder-direction similarity, semantic composition, causation, or learning benefit.
- **Conditional accompaniment probability P(j|i)** describes how often j accompanies i into an expert. Even with small φ, high-frequency companions must remain in the actual-input audit.

Grouping first seeks K groups with similar feature frequencies. A small, fixed allowance for increased frequency dispersion then permits positive φ to influence membership. Groups need not have equal member counts or equal token loads. Tφ exchanges members while preserving each T group size, separating the relationship adjustment from changes to group sizes and score denominators.

## 5. Minimal model

For prediction position t, let the original activation be z_i(t) and the hit indicator be x_i(t)=1[z_i(t)>0], using the original gated-cache definition.

- p_i: fraction of all positions at which feature i activates.
- g(i): expert assigned to i by candidate membership; this does not mean that the expert has learned i.
- e(t): expert that actually receives the complete input.
- a_ei: fraction of positions containing i that enter e.
- q_ei: fraction of e's received positions that contain i.
- l_e: fraction of all positions that enter e.

Where defined, these satisfy q_ei=p_i·a_ei/l_e. An empty expert has q=NA, not zero.

Grouping uses global p, whereas final evaluation must read actual q and a. **Similar membership frequencies do not automatically produce similar frequencies inside experts.**

## 6. Comparison matrix

|Label|Candidates and grouping|Scoring/encoding|Question answered|
|---|---|---|---|
|O|Old eight equal-width raw-frequency groups|Old mean score|Reuse the historical baseline|
|F|All reliable features, new log-frequency groups|Same-form mean score|Separate the regrouping change|
|T|Exclude the top 10 TRAIN features, then regroup by log frequency|Same-form mean score|Compare the head-exclusion operation with F|
|Tφ|Same candidates as T, adjusted using φ within the frequency constraint|Same score as T|Does the relationship add value?|
|P|Same memberships as F|Remove only the first singular direction of routing input, then re-encode|Separate geometric diagnosis against F|

T versus F tests the complete operation “exclude the head and regroup by the same method.” It does not separately identify deletion and movement of group boundaries.

T/Tφ share random-membership references with the same candidates and exact group sizes, to assess whether membership frequency separation and actual dispatch improve relative to random grouping. Repetition is sensitivity analysis, not independent training replication.

## 7. Diagram and required interpretable outputs

```text
Complete token representation h
      ↓ fixed CrossCoder
Original activations z and global frequencies p
      ↓ main comparison keeps h and z unchanged
All reliable features F / exclude top 10 for T
      ↓ frequency first
K candidate groups
      ↓ optional φ adjustment within frequency tolerance
Feature → assigned-expert membership
      ↓ same-form score and top-1
Complete h → actual expert
      ↓
Per-feature reception a + within-expert frequency q + costs to other groups
      ↓ separate decision after dispatch qualification
Learning and capacity validation
```

The core figure is **expert ID → feature IDs actually received, ordered by descending global frequency → natural-text activation positions: previous 2 tokens / current token / next 2 tokens**.

Hide the top 10 only in the main view to make the remaining features readable. A separate panel must show how much those head features still enter experts. Later tokens are retrospective display only and must never enter routing.

## 8. Conclusions allowed in this round

The round can compare reception, actual frequency composition, and costs under the specified fixed strategies. It can assess whether φ adds dispatch value beyond frequency grouping.

It cannot establish that experts learned knowledge, removed learning interference, increased capacity, or found the best expert for new knowledge. Low frequency does not mean unlearned; a dictionary hit is not functional evidence.

With mixed or non-supporting results, select one evidence-grounded next question. Do not automatically add deletion thresholds, PCA ranks, training, or a new architecture.

## 9. Execution prompt for the existing Agent

Read this Anchor and the accompanying Protocol. Perform this dispatch analysis in the existing conversation without creating a new Work or training experts. Reuse the parent experiment and completed audit. Freeze the implementation and report it briefly before staged execution. The researcher has confirmed that only the 10 highest-frequency TRAIN features are excluded from routing candidates, φ is auxiliary within the frequency constraint, and removal of the first singular direction is an independent diagnostic branch.

Separate O/F/T/Tφ/P and the necessary random references. Do not attribute regrouping, deletion, and relationship effects to one another. The main figure must show “expert → features actually entering → previous 2/current/next 2 tokens.” Although hidden in the main figure, head features remain in the complete actual-frequency audit. Follow the Protocol for reasoning audits and individual visual inspection of figures. Explain observations, costs, and one next decision clearly. Missing assets pause only affected branches; complete runnable comparisons. Do not increase the deletion count, scan PCA ranks, or start downstream learning.

## Implementation note accompanying the frozen execution record

The opening purpose expresses the researcher's intended priority. Its exact operationalization is **P_pool minus the 10 highest-frequency TRAIN features**; it can retain other high-frequency features and must not be described as excluding every high-frequency feature. Here P_pool denotes the reliable feature pool; condition P denotes the independent singular-direction diagnostic.

Implementation details and asset-dependent branch status are recorded separately in the execution run's frozen design: `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_priority_dispatch/20261018T160918Z/provenance/design_freeze.json`. This note clarifies terminology without changing the uploaded Chinese Anchor or its scientific thresholds.
