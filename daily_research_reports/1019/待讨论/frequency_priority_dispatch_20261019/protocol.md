# Protocol: frequency first, coactivation second for actual dispatch

Version: 2026-10-19; companion to “Frequency first, coactivation second: from feature membership to actual input dispatch.”

This document translates the [researcher-provided Chinese Protocol](protocol_cn.md). The byte-identical Chinese execution source is retained as [protocol_frozen.md](protocol_frozen.md). Implementation notes below point to the separate frozen record; they do not amend the source's scientific definitions.

## 0. Delegated scope and staged reporting

Once the researcher transfers this document to the existing Agent, execute grouping, route recalculation, statistics, and plotting on existing caches. **Do not create a new Work/Codex conversation, train models or experts, push the repository, or delete old evidence.** Obtain researcher approval before a new external GPU task or an extension to training.

Prioritize existing results. Missing complete representations or φ edges block only their dependent comparisons. Mark them NOT RUN rather than substituting another experiment.

Stages:

1. Check assets and freeze implementation: identify caches, formulas, candidates, comparisons, and estimated runtime.
2. Complete O/F/T: report reception and actual-frequency changes first, then continue the remaining comparisons.
3. Complete Tφ and random-membership references; independently complete P if its assets suffice.
4. Deliver figures, bounded conclusions, and one next decision.

Routine reporting does not request approval at every stage. Pause an affected branch only for a choice that changes the scientific definition or execution authority.

## 1. Assets and fixed objects

Parent result root:
`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z`.

Completed audit: `routing_audit_20261018T143950Z`. The local portable package is named `feature_dispatch_routing_audit_20261018_portable.zip`.

Reuse the fixed Qwen3-0.6B Base, final CrossCoder over 14 selected layers, original gated activations, decoder-norm weights, original token mask, and position mapping. Verify rather than infer hidden size, selected layer numbers, preprocessing, and BatchTopK semantics.

- TRAIN: 130,712 valid positions; EVAL: 65,402.
- Reliable pool P: 9,615 features; original low-frequency targets L: 964; original high-frequency list C: 962.
- New excluded set T10: select exactly the first 10 within the frozen reliable pool, ordered by descending TRAIN p, breaking equal-frequency ties by ascending feature ID.
- Save C and T10 separately. T10 is not C, not the highest 10%, and not a confirmed shared semantic category.
- K=8, hard top-1; discard no tokens and do not use later-token labels to select routes.

Check O's known route counts and sampled scores, and correspondence between h/z/text at the same positions. Perform only necessary consistency checks rather than repeating the complete passed engineering initialization.

EVAL has already been examined; original-document independence is unknown. Comparisons are exploratory held-out-position checks within this window, not a new independent confirmation.

Use a new timestamped output directory without overwriting parent results. First save `design_freeze.json`: sources, IDs, samples, T10, L, strategies, seeds, parameters, metrics, versions, and amendments.

## 2. Notation and counts

Original hits are x_i(t)=1[z_i(t)>0]. If implementation differs, report it and retain the parent definition rather than silently changing the threshold.

For strategy R, g_R(i) is the assigned expert and e_R(t) the expert actually receiving the input. Each strategy uses its own membership and route.

N_e=Σ_t1[e_R(t)=e]; n_i=Σ_tx_i(t); n_ei=Σ_tx_i(t)1[e_R(t)=e].

p_i=n_i/N; a_ei=n_ei/n_i; l_e=N_e/N; q_ei=n_ei/N_e.

- n_i=0: a is not estimable.
- N_e=0: q and enrichment are NA, not zero.
- n_i>0 and n_ei=0: a=0; q=0 only if N_e>0.
- Check Σ_eN_e=N, Σ_en_ei=n_i, and q=p·a/l where defined.

Main-comparison evaluation uses the same original x, including T10, C, and all reliable features. In T/Tφ, T10 has no assigned expert; record owner as unassigned. Continue counting it in q at every actual expert. Unassigned must not be recorded as failed zero reception or removed from actual-frequency profiles.

P also uses original x for its primary evaluation, preserving the content being evaluated. Re-encoded x′ is a separate diagnostic, not a replacement evaluation target.

## 3. Grouping rules

### 3.1 F: frequency reference over all reliable features

Let y_i=log10(p_i). Group these one-dimensional values using K=8 K-means. Each feature has equal weight, not a weight proportional to hit count. Freeze `random_state=20261019, n_init=20, max_iter=300, tol=1e-6`; save the actual implementation version. Renumber groups by ascending center.

Call this the frequency reference obtained by the fixed algorithm, not a global optimum. Equal group sizes are not required. If fewer than K unique frequency values exist or empty clusters cannot be recovered within the specified algorithm, report the condition as not executable; do not fabricate groups.

Membership-frequency dispersion is:

\[
D(g)=\frac{1}{|P_R|}\sum_i\left(y_i-\mu_{g(i)}\right)^2,
\]

where μ is a group's mean y. Besides D, report each group's median, quartiles, extremes, and size so large groups cannot conceal small-group differences.

### 3.2 T: exclude the head and regroup

Candidates are P_T=P\T10. Apply exactly F's frequency algorithm to form eight new groups. Save the reference dispersion D_T.

The F comparison changes both head exclusion and the organization of remaining memberships; it is not the isolated deletion effect. Show O→F separately to isolate the frequency-grouping change.

### 3.3 Tφ: coactivation assistance within the frequency tolerance

Use T's candidates. Freeze D(g)≤1.05D_T, keep K fixed, and preserve each T group's exact member count. This does not require the eight groups to equal each other. Tφ and T therefore retain the same score denominators. The constraint applies to average dispersion over the complete candidate pool, not a 5% limit on every group. Show each group's change separately. This 5% is the round's candidate tolerance, not a theoretical optimum; do not scan other values.

\[
\phi_{ij}=\frac{p_{ij}-p_ip_j}
{\sqrt{p_i(1-p_i)p_j(1-p_j)}}.
\]

Prioritize saved discovery-side candidate edges from the existing φ analysis. Verify dictionary, feature IDs, activation semantics, and data origins. **Shared old-community membership cannot replace original φ edges.**

Check whether candidate selection used this EVAL window. Recomputing weights on TRAIN does not remove selection leakage. If provenance is unknown or current EVAL selected the candidates, mark Tφ NOT RUN, with reason “ineligible candidate provenance.” Do not silently substitute another relationship. Retain the broader exploratory limitation that the researcher has already examined EVAL.

For existing candidate edges, recompute TRAIN hits and φ. Keep edges with at least 10 co-hits, 0<p_i,p_j<1, and φ>0. Do not enumerate all 16k² pairs or select edges on EVAL. Without a usable edge file, mark Tφ NOT RUN, list the missing asset, and continue other branches.

Raw edge weight is w_ij=φ_ij. To reduce domination by high-degree nodes, use fixed normalized weight w_ij/√(d_i d_j), with d_i=Σ_jw_ij. Compute degree once on the fixed, TRAIN-filtered graph; it does not change with grouping. Do not compare normalization variants. Isolated nodes contribute no relationship reward.

Maximize normalized within-group edge weight, starting from T and using deterministic size-preserving swaps:

1. Visit features i in ascending ID order.
2. Consider other target groups only if they contain a positive-edge neighbor of i.
3. For each such group, take its five members j closest in log frequency to i, breaking distance ties by ID.
4. A swap must satisfy the frequency constraint and strictly increase the relationship objective, with numerical tolerance 1e-12.
5. Choose the legal swap with greatest gain; break equal gains by target-group number and j's ID.
6. Update group centers, dispersion, and objective after every swap.
7. Stop after at most 10 rounds, or after a round with no legal improvement.

Report swap count, number of changed members, final objective, and stopping reason. Two-member swaps preserve group sizes and score denominators. This is a local heuristic without an optimality guarantee. If no swaps occur, retain that outcome; do not relax the tolerance to manufacture a relationship effect.

EVAL only checks signs, supports, and grouping behavior for fixed edges. It must not change the edge set. Unstable EVAL relationships constrain claims about stability.

### 3.4 Random references

Because T and Tφ have the same candidates and group sizes, reuse one set of random references rather than recomputing duplicates. Redistribute members with fixed seeds 11, 22, 33, retaining the same score and samples.

Their purpose is comparison of membership dispersion and actual dispatch. Frequency-optimized grouping outperforming random grouping is not discovery of natural same-frequency structure: frequency is the construction objective. Random references alone do not exclude φ's marginal-frequency preference.

Tφ versus T is the relationship's incremental comparison. Random groups do not replace it.

## 4. Unified score without additional calibration

O directly reuses its baseline. F/T/Tφ/random groups use the same-form parent score:

\[
s_e(t)=\frac{\sum_{i\in G_e}z_i(t)w_i}{|G_e|}.
\]

Reuse the exact parent decoder-norm definition and record its layer aggregation. Inactive members contribute zero while remaining in the denominator. The weight is an amplitude scale, not functional importance.

Use the parent tie/fallback rule and report tie and all-zero rates. Do not add ad hoc load constraints to make every expert nonempty.

**The researcher's newly requested “exclude 10 and regroup” comparison keeps scores fixed; it does not additionally introduce inverse-frequency weights or baseline calibration.** If concentration persists, conclude that head exclusion and grouping changes were insufficient, then separately define a calibration comparison. Do not silently combine the previous round's calibration suggestion with this round.

## 5. P: independent first-singular-direction branch

Pair P only with F. Freeze F's membership, original TRAIN frequencies, and same-form score. Experts retain the complete original h; only the representation used for re-encoding and routing changes.

Default: no additional mean subtraction. A row of H is the joint input actually received by the CrossCoder for one prediction position after original preprocessing. With 14 layers, concatenate them in the original fixed order. **This removes one first singular direction of the joint input, not one per layer and not only layer 28.** Before implementation, identify matrix shape, layer order, and scales. Result titles must explicitly say “joint input.”

Estimate the largest right singular vector v1 on TRAIN using streaming matrix products and power iteration. Freeze seed 20261019, at most 50 iterations. For G=HᵀH and λ=vᵀGv, require ||Gv−λv||/max(λ,1e-12)≤1e-4. Do not construct all of G or perform full SVD. If not converged, record approximation quality and pause P's formal comparison; do not label it an accurate first direction.

After fixing v1, apply h′=h−(h·v1)v1 to TRAIN/EVAL. Subtract the projection only, without rescaling or extra normalization. Split h′ back into original layer segments for the encoder. Inject it directly after the original preprocessing; do not preprocess or normalize it a second time.

Re-encode with the fixed CrossCoder. If encoding has BatchTopK or batch dependence, preserve original chunks, batches, and threshold mode. First confirm on a sample that unchanged H through the same path reproduces the original cached codes. Failure means measurement inconsistency for this branch; do not combine it with main results.

Prefer an existing H cache. Do not substitute zD for missing H. Record the missing asset. If new model forwards or a GPU task are necessary, report the resource and permission need first without blocking F/T/Tφ.

Use coordinates matched to the encoder/decoder to compute
E(H)=||H−Decode(Encode(H))||²_F/||H||²_F. Apply the same definition to H′. Also report both absolute squared errors with the common original denominator ||H||²_F to separate error changes from denominator shrinkage. Biases and inverse normalization must match the actual implementation.

Report normalized reconstruction errors for original/projected inputs, active-feature counts, active-set changes, projected energy fraction, and route changes. Main reception evaluation still uses original x; x′ is measurement diagnosis only. Do not assume “first direction=common.” Worse reconstruction or large active-set drift prevents using route changes alone as evidence for a removed-common mechanism. No training or rank-16 scan is required.

## 6. Evaluation: counts, reception, frequency, and costs

### 6.1 Counts

Per expert, report N_e, load, context-block count, member count, reliable features actually observed, and L members actually observed.

The primary “observed” definition is n_ei≥1, with n_ei≥5 as a separate support version. Do not choose whichever looks better. Distinct-feature counts depend on token count and are not capacity measures; broader random-group coverage does not establish better learning.

### 6.2 Target reception

For all fixed 964 L features, report a, q, q/p, and supports at each feature's own assigned expert. Primary descriptions are zero-reception count, feature-equal median/mean, and quantiles. Also give event-weighted results without replacing feature-equal results.

Check whether T10 intersects L. If it unexpectedly does, report the membership-definition conflict rather than silently dropping targets.

### 6.3 Actual frequency separation

Do not show membership p alone. List q of every reliable feature at every expert, including original high-frequency features.

For a fixed comparison, for each target i∈L at its assigned expert, compare against the fixed T10:

\[
B_i=\frac{1}{10}\sum_{c\in T10}\max\left(0,\log_{10}\frac{q_{ec}}{q_{ei}}\right).
\]

B measures the head companions' relative frequency advantage over the target, not total capacity or gradient competition.

- q_ei>0 and q_ec=0: this term is0; do not force a common feature back in.
- q_ei=0 with any q_ec>0: B_i=+∞; do not hide this failure with smoothing.
- Empty expert: B_i=NA, separately count no reception; do not silently exclude it.
- q_ei=0 and all q_ec=0: incomparable, retaining the target's zero-reception failure.

Report fractions of all L with B≤1 and B≤2, using the fixed denominator 964. NA/∞ do not count as qualifying. These thresholds mean average log advantages of at most one/two orders of magnitude; they are fixed descriptive points, not natural scientific success thresholds.

Report paired differences on commonly calculable targets, along with newly calculable and lost calculable counts to avoid survivorship bias. Also show each expert's complete q profile and middle-/low-frequency range. B improvement does not imply every feature became equally frequent.

### 6.4 Costs and uncertainty

Summarize reception changes over TRAIN log-frequency quantile intervals for all reliable features. Separately show T10, C, L, and others; overlaps are allowed but must be explicit.

Retain per-feature increased/decreased/unchanged counts. Expert numbering changes between strategies; compare each feature's own assigned expert and complete actual destinations rather than assigning identical semantics to identical expert numbers.

Use 200 context-block bootstrap replicates, seed 20261019, for descriptive 95% intervals on key paired differences. These are not document-independent confidence intervals; previously examined EVAL does not support strict confirmation.

### 6.5 Decision rules

Do not combine metrics into a single compulsory winner.

- Nonempty experts alone, without better target reception or actual frequency composition, do not meet the purpose.
- Better low-frequency reception and B, without new single-expert domination or widespread loss of other targets, identify a potentially useful dispatch candidate; report all costs and do not automatically start learning.
- Better reception with worse frequency separation or other-group outcomes is a tradeoff for the researcher, not an automatic pass.
- If Tφ only improves within-group edge weight but not actual dispatch, no additional dispatch value of the relationship is observed.
- If T remains concentrated in the most frequent remaining group, do not delete more features; prioritize the scoring question next.
- P compatibility failure means insufficient evidence for that branch only.

The old ≥200 positions and ≥20 contexts per expert can remain a future training-readiness marker. It is **not this round's stopping gate**. Complete statistics and figures for nonqualifying strategies and continue other comparisons.

## 7. Figures and text cards

### Figure A: strategy overview

Draw a simple flow diagram separating the fixed h/z main comparison from P's routing-input change. Identify candidates, grouping, score, and actual input as distinct objects. Show O→F, F→T, T→Tφ, F→P and explain each contrast.

### Figure B: expert → actual feature → text position (core)

Use one page per strategy, or two pages with four expert columns each. Do not put all strategies in one crowded figure. Show expert ID and N_e on top. Below, show feature IDs actually received, in descending original TRAIN p. Hide T10 only in the main view and show its actual q in a separate small panel.

Each expert column has six fixed slots: the two highest-global-frequency actual non-T10 hits; the two lowest-frequency hits with n_ei≥5; and the two most-supported L features assigned to that expert. Deduplicate; leave missing slots empty. Sort the final display by p and save complete untruncated lists. This sample is not the entire distribution.

Each item shows ID, p, q, n_ei, and “assigned member/accompanying input.” A feature may appear at multiple experts because actual inputs are not disjoint feature sets.

For each selected item, select one EVAL position actually received by that expert and containing that feature, using the fixed random seed and preferring different contexts. Show previous 2 tokens | current token | next 2 tokens. Preserve actual token boundaries and escaping; mark sequence boundaries and do not stitch across documents. Later text is retrospective only and does not enter scoring. Separately retain the complete visible prefix and next-token label for checking, without crowding the main figure.

Empty experts must say “no actual inputs.” An appendix may show where their assigned features went, but must not invent received examples.

### Figure C: dispatch comparisons

Separate (i) expert token counts/fractions; (ii) distinct features actually seen per expert; (iii) L zero-reception fraction and feature-equal reception distributions; (iv) fixed-denominator B fractions with NA/∞ counts. Do not share a y-axis across different units.

### Figure D: relationship increment

Separately display T versus Tφ membership-frequency dispersion, retained edge weight, moved members, target reception, and B changes. Add the random-reference range without treating improvement in the construction objective as validation success.

### Figure E: P branch

If completed, separately show F/P routing outcomes, projected energy, reconstruction error, and active-set changes. Label “uncentered joint-input first direction”; do not label it successful common removal.

Export PNG plus SVG/PDF, with short readable labels. Explain outside each figure: what is plotted; what is observed; what can/cannot be inferred. Save source CSVs and filters. Inspect each figure visually, not just for file existence.

## 8. Delivery and self-audit

- `summary_cn.md`: one page covering purpose, strongest conclusion, 2–3 evidence points, boundary, and next decision.
- `protocol_frozen.md`, `design_freeze.json`.
- `group_membership.csv`: original p, candidate eligibility, T10/C/L labels, and owner per strategy.
- Per-expert and per-feature p/a/q tables, membership dispersion, random results, scores, and text index.
- `figures_cn.md`, `text_cases_cn.md`, complete text/position origins.
- `reasoning_audit_cn.md`: actual use of available research skills; otherwise explicitly report unavailability and apply the stated checks.
- `manifest.json`: completed/missing components, sources, code versions, parameters, time, resources, and paths.
- `next_decision_cn.md`: one prioritized next question, without several expanded directions.

Audit whether score-term exclusion is confused with removal of input information; top10 with top10%; regrouping gains with φ; membership with actual input; omission of high-frequency companions; empty-expert q=0; hidden coverage costs or success-only target subsets; future-token leakage; original versus re-encoded measurements; or nonempty experts, spectrum changes, or reception being treated as learning/capacity benefit.

Stop at dispatch results. Without further authorization, do not train experts, increase expert count, or search thresholds. Record the researcher's final judgment as pending.

## Implementation notes tied to the execution freeze

The separate frozen implementation is recorded in `design_freeze.json`, copied from `/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_priority_dispatch/20261018T160918Z/provenance/design_freeze.json`.

- F/T use float64 log10(p), scikit-learn 1.2.0 KMeans, k-means++ initialization, Lloyd iterations, and no sample weighting, with all source parameters unchanged.
- New strategies share routing-hash seed 20261019. Seeds 11/22/33 control random membership only. O retains its original route.
- Tφ uses an undirected simple graph, no self-loops, both endpoints in P_T, and one contribution per pair. Degree is fixed before swaps.
- A feature with owner=−1 is unassigned; mask it before owner indexing. It still contributes to actual-input statistics at all experts.
- P's “uncentered” wording means no additional centering in this round, while retaining original frozen TRAIN preprocessing. Missing same-position preprocessed joint 14-layer H blocks P; last-layer hidden and zD cannot substitute for it.
- Top10 exclusion retains other high-frequency features. Neither the wording “middle-/low-frequency priority” nor the source's diagram should be read as excluding all such other features.
- The Protocol gives no numerical pass line for “domination” or “widespread loss.” Report measured loads and costs; do not invent a scientific acceptance threshold.

These are implementation/terminology notes, not new scientific thresholds, a replacement design, or observed comparison results.
