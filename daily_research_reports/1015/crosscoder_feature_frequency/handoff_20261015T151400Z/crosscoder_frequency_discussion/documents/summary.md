# CrossCoder feature relations and frequency: results

[中文](summary_cn.md) · [Five figures](figures_cn.md) · [Evidence ledger](detailed.md)

**Inspectable relationship groups recur within this window, but the full H1 of reliable structure plus closer within-group frequencies remains insufficient.** Mean-matched controls do not cover every group, leaving the primary dispersion endpoint undefined and null qualification unsuccessful. This computational/control insufficiency is not evidence that frequency structure is absent. Original-document independence also remains unknown. Interpretations below are AI analysis awaiting researcher judgment.

## Purpose and system

Identify candidate groups for later allocation comparisons. H1a concerns group replication; H1b concerns whether relationship-defined groups have closer frequencies than appropriate controls. Both constitute H1. H2 concerns learning benefit from actual expert allocation and was not trained.

Reuse the final14-layer/F16384 dictionary's gated cache over10,485,760 eligible positions. An event is saved z>0; frequency is hits divided by all eligible positions. Positive phi relationships feed a mutual-neighbor graph and one weighted modularity grouping algorithm. Frequency distance is not directly optimized, but phi favors similar margins, requiring mean matching and row/column-preserving full-pipeline controls.

D has5,238,097 positions; V has5,247,663. Both are exposed parts of one bin. Context blocks are not original documents; replication and intervals cannot be promoted to independent-document confirmation.

## Findings and limits

Frequency ranks are stable within this window: all-feature D/V Spearman is0.99792. Among V-positive features, median frequency is0.380% and maximum99.264%. D has353 zero-hit features, V393, and the union window290. Zero hits do not imply permanent death or natural hierarchy. See the [frequency table](../tables/frequency.csv) and figures1–2.

At mutual q10,15,666 eligible candidates yield186 non-singleton D groups with13,807 members, versus185 V groups. One-to-one matched mean member Jaccard is0.54838, an intersection/union readout rather than accuracy or an independent success probability. The largest D group has735 members,4.69% of candidates. At q20 there are65 D groups and mean Jaccard0.54242. Thus inspectable relations do not establish a unique natural partition. See [main results](../evidence/main/summary.json), [q20](../evidence/sensitivity_q20/summary.json) and figure3.

The186 real groups have mean V log10-frequency SD0.35331dex, versus0.67565dex for size-matched random groups, a descriptive difference−0.32234dex. Lower dispersion means closer frequencies. This control does not remove group-mean differences or phi preference. Only142 mean-matched controls qualify, covering48.37% of grouped members;44 groups lack qualified controls. Therefore the all-group primary T_b is undefined. Bounded-sample null qualification also encounters undefined endpoints; the99-draw formal calibration was correctly not started. There are no valid p-values. Figure4's NA values are substantive missing evidence, not zero effects. See [all group metrics](../evidence/main/group_metrics.csv) and [qualification](../evidence/null/qualification.json).

## Input mapping and judgment

Freeze D-only hit thresholds requiring at least2 active members and at most1% D hits per group. On all V positions,34.66% hit no group,39.52% exactly one, and25.82% multiple groups. Conditional contiguous-block bootstrap95% intervals are34.28%–34.98%,39.31%–39.73%,25.48%–26.31%; they are not document-valid intervals. There are1,760 random/high-score examples from176 groups;10 groups cannot achieve the threshold. See [coverage](../evidence/inputs/coverage.json) and figure5. Substantial overlap limits a direct one-group/one-top-1-expert mapping. Text cases span comments, technical material and bibliographic fragments; no single semantic function is established.

The result supplies concrete group/frequency/input objects, but full H1 is **INSUFFICIENT** and H2 **NOT RUN**. **One AI-proposed next decision is whether to repair mean-control budget scaling and preregister a bounded H1 rerun.** A10,000-proposal cap cannot furnish20 draws for groups larger than333 under10×size burn-in and size-proposal spacing. This engineering mismatch was not fully checked beforehand. Repair does not itself solve document independence. No thresholds or budget were extended after observing results, and expert training should not be inferred from this analysis.


Aggregation matters: real dispersion is0.35331dex with equal group weights, but0.66846dex when weighted by group membership (size-control0.85257dex). Small groups cannot stand in for the feature population. Equal-group weighting remains the primary descriptive aggregation; report both separately.
