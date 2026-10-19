# Feature relationship grouping and frequency: report draft

[中文](report_draft_cn.md) · [Protocol](protocol_draft.md) · [Assets](assets_checked.md) · [Audit](reasoning_audit.md)

Status: DRAFT / NOT RUN, 2026-10-15. This is a report scaffold organized according to the latest integration request, not a new result report. The referenced v0.2 Feishu report body was not supplied, so exact preservation of its contents cannot be claimed. The received Anchor remains unchanged under sources.

## Purpose and boundary

Identify inspectable feature-group candidates for later comparisons of expert allocation. First ask whether co-occurrence in a fixed dictionary forms reproducible groups; then whether groups formed without a frequency-distance objective have more similar frequencies than appropriate controls; finally inspect which inputs hit these groups and how strongly they overlap.

One analysis has four linked operations: frequency/stability→background-adjusted relationships→grouping followed by frequency testing→input mapping. Structure, frequency similarity, input distinction and learning benefit are separate conclusions. This first step contains no expert-training or learning-loss result.

## Fixed measurement object

Recommend the final 14-layer/F16384 CrossCoder, observing model blocks 2,4,…,28. One shared z jointly codes a position; decoder norm is not activation probability. The saved cache contains 10,485,760 eligible positions and approximately 2.669 billion positive activations. Training BatchTopK used an average budget of 256; cached inference used the frozen TRAIN threshold, with realized mean L0 254.54.

These are saved asset identities and sizes, not new measurements. Original-document independence is unknown and both D/V sides are exposed. Current evidence can therefore support within-bin exploration and conditional method checks only.

## Hypotheses and alternatives

H1a: groups reproduce on the review side beyond frequency background and sparse row-count constraints. H1b: groups built from relationships have lower review-side log-frequency dispersion than matched controls. The new H1 requires both, within the relevant data eligibility boundary.

Rivals include ubiquitous features, phi's margin preference, edge/group selection bias, duplicate/source concentration and unreliable rare-event estimates. Size-matched random grouping alone cannot separate these explanations; mean matching and a margin-preserving full-pipeline null are needed. No groups, mixed-frequency groups and substantial input overlap are meaningful possible outcomes. Insufficient precision is not evidence of absence.

H2: later test whether frequency-informed input allocation improves learning on low-frequency-feature inputs without material overall-loss harm at fixed K, capacity, exposure and budget. H2 is planning only. Failure of H1 does not automatically refute a deliberately frequency-based H2 allocation.

## Five planned figures and their captions

### Figure 1: feature activation frequency rank

File: to be generated after authorization. Fix the D ranking and use the same feature order for V. Report percentage units and separate zero-hit counts.

- How to read: x is fixed feature rank; y is activation frequency; distinguish D/V by line style and color.
- Observation: pending, including N, zero-hit counts and uncertainty.
- Meaning for the question: pending; rank shape alone cannot establish natural hierarchy.
- Next decision: pending; use measured reliability to define the estimable relationship population.

### Figure 2: discovery versus review frequency

File: pending. One point per feature; x=p_D, y=p_V, reference y=x. Separate positive and one-/two-sided zero counts.

- How to read: proximity to the reference means similar estimated frequencies across these sides; mark unreliable support.
- Observation: pending; do not replace the plot with one correlation coefficient.
- Meaning for the question: pending; these data are not certified independent original-document confirmation.
- Next decision: pending; do not improve later results by dropping V-zero members.

### Figure 3: relationship matrix and candidate groups

File: pending. Main panel is the phi matrix with group boundaries; a separate frequency strip has its own legend. Local networks are auxiliary and have no causal arrows.

- How to read: both axes use the same feature-ID order; matrix color is relationship strength rather than frequency.
- Observation: pending, including group count, coverage, largest group, replication and raw support.
- Meaning for the question: pending; phi also favors similar margins, so visual blocks alone cannot establish the hypothesis.
- Next decision: pending; report unclear groups honestly rather than forcing one group per expert.

### Figure 4: within-group frequency and three controls

File: pending. Show each group's log10-frequency SD, size, observed point and size-/mean-matched random distributions. Present global full-pipeline-null endpoints separately.

- How to read: lower dispersion means more similar member frequencies; identify the source of each interval.
- Observation: pending, including effects, intervals, missingness and matching error.
- Meaning for the question: pending; retain conflicting controls rather than selecting favorable ones.
- Next decision: pending; retain allocation candidates according to actual same-/mixed-frequency evidence.

### Figure 5: input and activation examples

File: pending. Separate random and high-score samples. Show group ID, visible context, marked target position, active members/z and other groups hit.

- How to read: the marked token is the analyzed position; any right-context aid must be labeled invisible to the model at that position.
- Observation: pending; accompany examples with unique/multiple/no-group percentages over all eligible review positions.
- Meaning for the question: pending; examples do not replace population, semantic or causal evidence.
- Next decision: pending; preserve multi-group conflicts in allocation design rather than hiding them with top-1 assignment.

Design every figure for normal Feishu reading width with consistent fonts and palette. Export PDF/SVG/PNG and retain source tables, scripts, commands and provenance. Open each generated figure to inspect it. No new plot or rendered validation exists yet.

## Second step: candidate groups to actual experts

The researcher must first select the learning task. Freeze feature events→input scores/frequency→multi-group handling→K-expert capacity/load→training and independent loss evaluation. Selected experts still receive complete inputs including common components; this is not a separate common expert.

Later compare frequency-informed allocation with frequency-blind allocation matched in K, capacity, budget and exposure. Add a matched relationship-based allocation only if claiming additional value from relationship groups. Low-frequency targets, difficulty controls and the overall-loss noninferiority margin remain undefined. There is no H2 result or execution approval.

## Current conclusion and stopping point

This round prepares assets and design. H1a, H1b and H2 are NOT RUN; scientific judgment remains Unknown. Reusable caches and joint counts are verified; original-document confirmation and computational qualification of new nulls remain unresolved. See decisions_needed.md for review choices. No statistics, plotting, encoding or training starts without explicit authorization.
