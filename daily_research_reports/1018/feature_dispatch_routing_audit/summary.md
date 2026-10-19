# Why did active low-frequency features miss their designated expert?

[Full analysis](detailed.md) · [User Anchor](design/anchor.md) · [User Protocol](protocol.md) · [Four-figure guide](figures.md) · [12 text cards](text_cases_cn.md) · [One next decision](next_decision.md) · [中文](summary_cn.md)

**The current evidence favors defining and calibrating the score before concluding that regrouping is necessary.** We localized how the original score defeats the low-frequency group; the inspected co-occurrence constraints do not force its current zero reception. Neither global grouping feasibility, a replacement score nor learning benefit has been established. This is a bounded AI recommendation; researcher judgment remains pending.

## Purpose and comparisons

This round asks only why an input containing an active low-frequency feature fails to reach the expert designated by its membership list. Designation does not mean that the expert learned the content. Fixed top-1 sends the complete position representation to one expert; it does not split its features among experts.

We reused existing caches from frozen Qwen3-0.6B Base and the final selected-14-layer CrossCoder. A uses eight equal-width raw-probability intervals. B1/B2 preserve A's group sizes with their original random memberships and their own routes. TRAIN contains 130,712 positions and EVAL 65,402; the reliable pool has 9,615 features, including the original 964 low-frequency targets. EVAL is previously inspected held-out-position replication; document independence is unknown.

## Three measured findings

**1. Membership did not translate into per-feature reception.** All 964 low-frequency features have zero reception by their designated expert under A on both splits. B1/B2's feature-equal EVAL means are 4.44%/10.30%, with 122/48 zero-reception targets. Positive reception is not better learning. A0 receives no inputs, so its within-expert frequency q is NA, not zero.

![Figure 1: actual reception and zero-reception targets](figures/figure1_actual_reception.png)

[Expert source table](tables/expert_summary.csv); [feature-equal and event-weighted summaries](tables/group_summary.csv). Figure 1's upper row is the input-position percentage; its lower row is the zero-reception feature percentage within each membership group.

**2. Low-frequency activation did not win the score competition.** The original score averages decoder-norm-weighted activations over all group members, including inactive members. At the 95,544 TRAIN positions containing low-frequency features, the mean winner-minus-A0 margin is 0.567492: +0.569428 from original high-frequency list C and −0.001935 from non-C terms. The low-frequency group responds but loses under the combined effects of raw amplitude, frequency and membership composition. Their separate causal effects were not identified.

Virtually zeroing only C's score terms sends every position to A0. This is not a usable remedy: groups A1–A7 consist entirely of C, so they mechanically become zero, and 25 other features lose their previously positive designated-expert reception. High-frequency terms should not be treated as removable noise. See [score decomposition](tables/winner_vs_A0_margin_components.csv) and [costs](tables/frequency_band_costs.csv).

**3. The inspected co-occurrence tradeoffs do not make zero reception necessary.** Three cases were frozen on TRAIN. For each rule, at most nine cross-owner high-overlap pairs were selected before reading EVAL, giving 27 fixed pairs. A's necessary upper bounds on a common reception fraction are 99.18%–99.61% on TRAIN and 98.84%–99.72% on EVAL. These restrict extremely high simultaneous coverage; they do not force a low-frequency target's reception to zero. The finite search does not prove global feasibility.

![Figure 4: fixed random text positions and original scores](figures/figure4_text_and_score.png)

Features 9297, 1133 and 2704 each have three random plus one high-activation text example. All 12 A positions reach expert 7. Figure 4 uses the first frozen random sample for each ID. Current tokens and next-token labels are separate; [the cards](text_cases_cn.md) contain full-prefix provenance and 36 rule-specific target-removal sensitivity checks.

## Knowledge update and next step

We advanced from “expert loads are imbalanced” to a checked computational path: per-feature zero reception → competition between original group means → the winning margin from high-frequency-list terms. **The one AI recommendation is to retain membership and top-1, define what the score should compare, and separately register a bounded score-calibration comparison with explicit costs.** First decide per-feature reception requirements and acceptable reception losses elsewhere. No calibration, regrouping or learning was run.

Core counts, 200 descriptive context-block resamples, all low-target × C companion tables, virtual score diagnosis, 12 text cards and finite conflict checks are complete. Full machine-readable outputs and receipts remain in the [execution directory](/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/frequency_interval_moe/20261018T103820Z/routing_audit_20261018T143950Z). This was CPU-only, with no new GPU, model forward or training. [Detailed](detailed.md) records completion, unexecuted work and actual resources.
