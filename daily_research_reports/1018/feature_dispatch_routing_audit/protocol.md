# Protocol | Per-feature audit of actual dispatch

Version: 2026-10-18 v1.0. Companion to the unchanged researcher-supplied [Chinese Protocol](protocol_cn.md) and [Anchor](design/anchor.md). The original Chinese documents own the supplied design. The user's current request authorizes bounded CPU cache analysis and record placement; it does not authorize a new learning experiment, model forward pass, GPU allocation, changed live routing/grouping, or commit/push.

## 0. Execution scope and evidence rules

### 0.1 Existing assets

Start at:
`/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/`.

Resolve actual filenames from the existing summary, protocol, `cache/grouping.json`, plotting code and assignment files; do not assume a file exists. Write into a new timestamped `routing_audit_*` child or the project-required independent directory, with absolute paths and a relative entry.

Verify the model/dictionary checkpoint, selected layers and measurement point, cached z gating, feature-ID mapping, TRAIN/EVAL split, original low/high lists, eight memberships, score, ties/fallback, both B memberships, position indices and text mapping. Existing engineering checks may be reused. Do not repeat training, full model activation extraction, dictionary training, or full φ graph construction. If a required small quantity is missing, assess cost and derive it from caches where possible. New forward passes or training belong to a later proposal.

### 0.2 Consistency and partial blocking

Check N, membership sizes, expert input counts and low-feature union counts against existing summaries. Preserve discrepancies and explain masking, sample scope or version differences.

- Unconfirmed route/feature alignment blocks dependent quantitative claims, not independent asset organization.
- Missing text mapping blocks text examples only.
- Binary events without amplitudes still support p/a/q and co-occurrence; do not invent score contributions.
- EVAL was previously inspected and the CrossCoder saw the learning corpus. Describe held-out-position replication, not wholly new independent confirmation.
- Unknown original document identity means context blocks do not establish document or near-duplicate independence.

Distinguish newly recomputed quantities from citations of old records.

## 1. Frozen objects and basic quantities

A position t is a valid next-token prediction position under the existing mask. Exclude padding and invalid context-final positions. Context IDs support blocking and text explanation, not additional independent evidence.

For each rule R separately:

- b_ti = 1 iff cached feature i activates at position t.
- e_R(t) is that rule's existing hard top-1 assignment.
- g_R(i) is that rule's designated expert for feature i.
- N is the valid-position count; N_e is the number sent to expert e.
- n_i = Σ_t b_ti; n_ei = Σ_t 1[e_R(t)=e] b_ti.

Compute:

```text
p_i = n_i / N                       global occurrence frequency
a_ei = n_ei / n_i                   destination share given feature i
l_e = N_e / N                       expert load
q_ei = n_ei / N_e                   frequency within expert e
enrichment_ei = q_ei / p_i
q_ei = p_i * a_ei / l_e             consistency identity
```

Check Σ_e N_e=N, Σ_e n_ei=n_i and n_ei≤min(N_e,n_i), as well as the identity to floating-point precision. If an older assignment dropped inputs or used special channels, account for them explicitly.

Zero semantics:

- n_i=0: p=0; a and enrichment are not estimable. This does not mean permanent death.
- N_e=0: l=0; q and enrichment are NA, not zero. If n_i>0, a=0.
- N_e>0, n_i>0, n_ei=0: a=q=enrichment=0; preserve the row.

Provide integer numerators/denominators with ratios; no large smoothing constants. Global rarity is not rarity within an input or knowledge difficulty. The union of individually rare features may be frequent.

Use the original A/B memberships. Reuse the original low-frequency list L; if unrecoverable, mark the old union unverifiable rather than redefine it. For the accompanying high-frequency set C, **first reuse the original explicit high-frequency list and definition**. Only if that list/definition is absent, define C diagnostically as reliable TRAIN features with p_i≥0.5 and record IDs, size and selection time. Deduplicate overlaps with groups. Never adjust C on EVAL, and report an empty C rather than relax it. C denotes frequent companions; inspect P(c|i), not φ alone, since p_c=1 makes φ undefined.

## 2. Stage one: actual per-feature and group dispatch

### 2.1 Core tables

For A, B1 and B2 on TRAIN and EVAL:

- `expert_summary.csv`: rule, split, expert, membership count, N_e, l_e, positions hitting its membership, context counts.
- `feature_expert_metrics.csv`: rule, split, feature, g_R(i), p_i, n_i, expert, N_e, n_ei, a, q, enrichment, hit contexts and NA reasons.
- `feature_owner_summary.csv`: metrics at each feature's own designated expert and at its largest actual receiving expert.
- `common_companions.csv`: target–C co-occurrence counts, P(c|i), global frequencies, within-designated-expert q_i/q_c, and denominators.

Compute only the existing reliable pool and required C through sparse aggregation, not a full feature-pair matrix.

### 2.2 Summaries

Report feature-equal medians/IQRs and occurrence-weighted summaries together. Separate designated-target frequency distributions, accompanying-common distributions, zero reception with original support counts, and completely empty experts. Do not introduce a new composite score. A log plot of positive q must separately display zero and NA counts; positive-only dispersion is not a complete group score.

Optionally report log10(q_c/q_i): positive means common is more frequent. q_i=0 is “target not received”; q_c=0 is “companion absent.” Do not add absent common events to force equal frequencies.

### 2.3 B comparison boundary

B preserves group sizes but changes membership. Compare the **same feature at each rule's own designated expert**. A same-numbered B expert is not semantically aligned with A. B is an existing grouping control, not a fully matched optimum. Check input positions, valid masks, feature events and score weights before paired differences. Each rule uses its own e_R(t). A's identical two-seed route is counted once.

### 2.4 Descriptive uncertainty

Show sample sizes. Where intervals are useful, resample existing context IDs in whole blocks, fixed seed and 200 replicates. These are descriptive block intervals, not token-independent or document-independent evidence. Prioritize core tables if interval cost is high. Lack of significance is not no effect.

## 3. Stage two: natural-text demand versus destination

### 3.1 Freeze case IDs on TRAIN

Select only from original L members with TRAIN n_i≥30 and at least five distinct cached contexts. These criteria protect case readability; they do not remove other features from the core tables. State that context IDs are windows rather than verified document identities.

Choose up to three features at the lowest, median and highest designated-expert reception rates, breaking ties by descending hit-context count then ascending feature ID. If every rate is identical, choose three distinct IDs by that tie rule and explicitly say no good/bad contrast exists. A mid-frequency reference may be added only if clearly labeled; report fewer if insufficient.

After freezing IDs, select three fixed-seed random EVAL hits and one high-activation hit per ID, preferring different contexts. If EVAL lacks support, use TRAIN and label it. Do not select only attractive/high-activation examples.

### 3.2 Text-card fields

Provide source file, context, absolute position, token ID, current token and model-visible prefix. Show the correct next token separately as interpretation-only information not used in routing. Include global frequency, designated expert, available activation amplitude, major simultaneous features with frequencies and groups, all original group scores, winner/runner-up/margin, actual destination, and the effect of removing only the target's score term. A target not changing the winner is not evidence it is useless to the model.

Semantic readings are candidate interpretations, not single-example labels. Future text was not available to the encoder. An empty expert has no naturally received text; show target-hit inputs and their actual destinations instead.

## 4. Stage three: score paths and co-occurrence constraints

### 4.1 Score arithmetic

Verify the implementation. If the original score is

```text
s_e(t) = Σ_{i in G_e} z_ti w_i / |G_e|,
```

reuse the original w_i: the sum of the 14 per-layer decoder L2 norms. Do not substitute another norm. Check nonnegative z; signed terms would require their own accounting rather than binary-event explanations.

Split each score into C and non-C terms while retaining the original denominator |G_e|. Compare their contributions to winner–runner-up margins, retaining negative differences. With H_e total active member events, the global mean score equals

```text
[H_e / (N |G_e|)] * [Σ_t Σ_{i in G_e} z_ti w_i / H_e].
```

This is the event-weighted amplitude decomposition, not a product of two ordinary per-token means or two independent causal effects. H_e=0 gives mean score zero and event amplitude NA.

### 4.2 Bounded score-only counterfactual

Virtually set C's **routing-score terms** to zero in the existing cache. Preserve z, membership, denominators, tie/fallback and expert input representations; recompute diagnostic top-1 destinations. Do not modify saved/live routes or train a replacement. Report reassignment, expert counts, target a/q, all-zero and tie counts. Changes driven by zero-score ties do not show learned discrimination.

This is a virtual scoring diagnosis, not a representation intervention, new learning experiment or deployable validated policy. Common removal changes amplitudes and does not isolate common semantics. Reuse an existing suitable matched removal if available: first match removed member counts **within every group**, then inspect TRAIN frequency/support/amplitude comparability. Matching only a global count is insufficient. If C fills a group or no substitute exists, report no effective matched control; do not launch a large search. The counterfactual cannot identify separate causal effects of frequency, amplitude and semantics.

Remove an individual case target's term only for selected cases to inspect its local routing role; do not enumerate the full dictionary.

### 4.3 Necessary co-occurrence bound

Use existing cross-group records or case candidates to find high-overlap targets without a new full quadratic matrix. For i,j with different designated experts and counts n_i,n_j,n_ij, any top-1 assignment delivering at least the same fraction τ of both features to their respective experts must satisfy

```text
τ(n_i+n_j) ≤ n_i+n_j−n_ij,
τ ≤ 1−n_ij/(n_i+n_j).
```

Intersecting positions cannot reach both experts. Complete pair co-occurrence gives an upper bound of 0.5; k completely co-occurring groups require kτ≤1. This bounds specific reception requirements, not learning capacity. Satisfying the necessary condition does not establish overall feasibility; not finding a conflict does not establish its absence. Do not solve a full optimal assignment, lower reception requirements silently or change lists. Concrete conflicts may motivate later regrouping discussion.

## 5. Four key figures

1. **Actual reception:** expert input counts, alongside designated-target zero reception. Feature counts and token counts use separate axes.
2. **Global versus within-expert frequency:** the same feature's p and designated-expert q, faceted by A/B. Display zero and empty-expert cases separately rather than false logs.
3. **Target versus common:** fixed target q and major companion q by expert, with supports; avoid overstating sparse cases.
4. **Natural text and score explanation:** 2–3 representative positions, selected features, group scores and destination; full cards in the appendix.

If informative, include original/virtual-removal panels within figures 1 or 2 rather than expand the figure count. Titles and axes state quantities/units; explanations belong in `figures_cn.md`. Export PNG plus SVG/PDF, preserve source tables/scripts, keep colors consistent, and inspect meeting-size readability.

## 6. Stage reports and delivery

Report each stage when complete rather than wait for every figure. Authorized read-only steps need no repeated approvals; continue independent work if a dependency is missing.

- Stage 0: assets, counts and evidence-based cost estimate; GPU count does not guarantee a deadline.
- Stage 1: per-feature results and one substantive understanding update with its table.
- Stages 2/3: text, score paths, co-occurrence; distinguish supported, weakened and unresolved explanations.
- Final: full evidence and one priority next decision.

Suggested records: `summary_cn.md` (one page), `analysis_cn.md` (definitions → methods → observations → explanations → limits), `figures_cn.md`, `text_cases_cn.md`, `metrics/`, `figures/`, `scripts/`, `manifest.json`, `reasoning_audit_cn.md`, and `next_decision_cn.md`. The latter proposes one change and a later learning test, without executing them.

Use cached column/sparse aggregation and reuse existing verified plots where appropriate. Estimate remaining time from actual progress. Core p/a/q and cases take priority; intervals and a missing figure must not block all delivery.

## 7. Logical audit and acceptance

The executing Agent checks:

1. Frequency A is not confused with φ grouping; B expert IDs are not semantically aligned.
2. p/a/q/load denominators are explicit; q at an empty expert is NA.
3. Common is inspected, not imposed on every expert or asserted to require equal frequency.
4. Do not improve results by dropping zero targets, inputs or post hoc case selection.
5. Select from TRAIN only; disclose prior EVAL use and unknown document independence.
6. Separate score removal, representation intervention and learning intervention.
7. Diagnostic support is bounded; learning benefit/capacity remain `NOT TESTED`.
8. A reception necessary condition is not an optimal-allocation or capacity theorem.
9. Each claim traces to CSV rows, figures and text positions; unsupported descriptions remain hypotheses.
10. Do not conflate overcompleteness, full rank, sparse reconstructability or expert predictability.

Use the designated reasoning skill if accessible, otherwise state unavailability and apply this explicit checklist. Deliver auditable definitions, evidence, counterexamples and claim boundaries, not private reasoning traces.

## 8. Stop condition

Finish core metrics, available text cases, score decomposition and finite co-occurrence conflict checks. Recommend with evidence one of: prioritize scoring, prioritize grouping-conflict inspection, or insufficient evidence. Do not open all directions simultaneously.

A future routing optimization or learning experiment needs a new Protocol defining variables, frequency objectives, reception constraints, feasibility, frozen validation and training budget, plus the user's next decision. Do not automatically start training as continued refinement.
