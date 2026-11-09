# Detailed Report: A06_02_01_E07 Top-1 Lock-In Margin Threshold

## Verdict

A06_02_01_E07 supports a finite-threshold top-1 lock-in mechanism in the controlled
no-position bridge. Step-0 positive assignment alone is not enough. The tested
system preserved feature-to-expert identity for \(q \ge 0.05\), but \(q=0.02\)
crossed decision boundaries during training and lost matched preservation in
many seeds.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | What it cannot prove |
|---|---|---|---|---|---|
| Top-1 routing | Each routed hidden state is sent to one expert. | Expert with largest router logit \(w_e^\top h_i\). | expert index | Creates discrete assignment basins. | Whether the assignment is useful. |
| Router row | One expert's gate vector. | \(w_e\) in the router matrix. | vector | Determines the expert decision boundary. | Feature semantics. |
| Feature center | Average hidden representation for a feature. | \(\mu_f\) estimated on audit route-position states. | vector | Used to audit margins and matched routing. | Real language feature meaning. |
| Pairwise margin | Distance from crossing a specific expert boundary. | \((w_a-w_j)^\top\mu_f\), where \(a\) is the matched expert. | logit gap | Boundary-crossing metric. | Full training dynamics by itself. |
| Current margin | Pairwise margin measured at a training snapshot. | \(\gamma_t\) using current router and current feature centers. | logit gap | Tells whether the route region still contains the feature. | Causal source of drift. |
| Cluster-aware margin | Margin after using current cluster/feature centers consistently. | Minimum matched-vs-competitor logit gap in the current audit geometry. | logit gap | Guards against only measuring the router side. | Utility or semantic quality. |
| Matched preserve fraction | Original feature-to-expert identity preservation. | Minimum fraction of each original matched feature still routed to its original matched expert. | fraction in \([0,1]\) | Primary result metric. | Whether the new partition is still feature-separated. |
| Feature NMI | Feature partition quality. | NMI between feature id and routed expert id. | fraction in \([0,1]\) | Secondary check. | Original expert identity, because labels can swap. |
| Sign flip rate | Boundary-crossing rate. | Fraction of pairwise margins whose sign changed relative to the original match. | fraction in \([0,1]\) | Direct evidence that the margin was consumed. | Why the boundary was crossed. |
| Row-gap scaling | Margin-shrinking intervention. | \(w'_e(q)=\bar w+q(w_e-\bar w)\). | scalar \(q\) | Reduces all pairwise row gaps without changing their signs for \(q>0\). | Real-DCLM behavior. |

## Question

If the initial feature-to-expert assignment is correct but its positive margin
is made very small, does top-1 routing preserve the original assignment during
training?

This directly tests two rival explanations:

- **Thresholded lock-in:** once the feature starts inside a sufficiently thick
  top-1 basin, training preserves the assignment.
- **Passive margin budget:** smaller initial margin is smoothly consumed by
  training drift, causing earlier sign flips and lower preservation.

## Mathematical Intervention

Let \(w_e\) be the pseudo-center initialized router row for expert \(e\), and let
\(\bar w=E^{-1}\sum_e w_e\) be the mean router row. The intervention replaces
each row with

\[
w'_e(q)=\bar w+q(w_e-\bar w).
\]

For any two experts \(a\) and \(j\),

\[
w'_a(q)-w'_j(q)=q(w_a-w_j).
\]

Therefore each pairwise margin scales as

\[
\gamma'_{f,j}(0)=q\gamma_{f,j}(0).
\]

For \(q>0\), this preserves the sign of every pairwise margin and therefore
preserves the step-0 argmax assignment. It only changes how much margin exists
before training starts.

Two guards were included:

- \(q=0\) collapses all router rows to the same row mean and removes positive
  margin.
- The crossed guard moves a matched row beyond its nearest competitor using
  \(w'_a=(1-\alpha)w_a+\alpha w_j\) with \(\alpha=1.25\).

## Experimental Setup

Model and data:

- one-layer Transformer plus top-1 MoE;
- 4 experts;
- hidden size 128;
- no learned absolute positional embedding;
- no B token;
- feature slot length 4;
- route position is the last token of the feature slot;
- slot starts `[2, 10, 18]`;
- target depends only on feature identity;
- training objective is slot-end target cross-entropy.

Cells:

- `C0_clean`;
- `C1_mild_nuisance`;
- `C2_moderate_nuisance`;
- `C3_weak_feature_nuisance`.

Seeds and checkpoints:

- seeds `20260623` through `20260630`;
- checkpoints `0, 1, 2, 5, 10, 20, 50, 100, 200, 400, 800, 1600`.

Conditions:

- `gap_q1p0`;
- `gap_q0p5`;
- `gap_q0p25`;
- `gap_q0p1`;
- `gap_q0p05`;
- `gap_q0p02`;
- `gap_q0p0_guard`;
- `cross_alpha1p25_guard`.

## Run Record

Run name: `a06_23_top1_lockin_full_20260701_1`.

Execution: local two-GPU sharded run.

Shard inventory:

| shard | discovery rows | intervention rows | margin snapshot rows | pair rows |
|---|---:|---:|---:|---:|
| shard 0 | 16 | 128 | 1536 | 18432 |
| shard 1 | 16 | 128 | 1536 | 18432 |

The final aggregate contains 32 rows per condition for C0-C3 and 8 seeds.

## Intervention Audit

The intervention was valid. For every positive \(q\), step-0 feature NMI and
matched preserve fraction stayed at 1.0, sign flips stayed at 0, and margin
scale matched \(q\) exactly.

| Condition | Step-0 NMI | Step-0 preserve min | Post margin min | Mean margin scale | Step-0 sign flip |
|---|---:|---:|---:|---:|---:|
| \(q=1.00\) | 1.000 | 1.000 | 5.667 | 1.000 | 0.000 |
| \(q=0.50\) | 1.000 | 1.000 | 2.834 | 0.500 | 0.000 |
| \(q=0.25\) | 1.000 | 1.000 | 1.417 | 0.250 | 0.000 |
| \(q=0.10\) | 1.000 | 1.000 | 0.567 | 0.100 | 0.000 |
| \(q=0.05\) | 1.000 | 1.000 | 0.283 | 0.050 | 0.000 |
| \(q=0.02\) | 1.000 | 1.000 | 0.113 | 0.020 | 0.000 |
| \(q=0\) guard | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| crossed guard | 0.891 | 0.000 | -9.017 | -0.608 | 0.987 |

Source: [`tables/intervention_audit_aggregate.csv`](tables/intervention_audit_aggregate.csv).

## Early Training Evidence

The threshold appears early. At step 5, \(q=0.05\) already preserved identity
with positive margin, while \(q=0.02\) had near-zero or negative current margin
and nonzero sign flips.

| Condition | Step | Feature NMI | Preserve min | Current margin | Sign flip rate | Cluster-aware margin | Target accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|
| \(q=1.00\) | 5 | 1.000 | 1.000 | 5.750 | 0.000 | 4.479 | 0.996 |
| \(q=0.50\) | 5 | 1.000 | 1.000 | 2.938 | 0.000 | 2.277 | 0.990 |
| \(q=0.25\) | 5 | 1.000 | 1.000 | 1.509 | 0.000 | 1.151 | 0.933 |
| \(q=0.10\) | 5 | 1.000 | 1.000 | 0.648 | 0.000 | 0.467 | 0.771 |
| \(q=0.05\) | 5 | 1.000 | 1.000 | 0.355 | 0.000 | 0.232 | 0.689 |
| \(q=0.02\) | 5 | 0.907 | 0.375 | -0.005 | 0.151 | -0.098 | 0.595 |
| \(q=0\) guard | 5 | 0.580 | 0.000 | -0.478 | 0.555 | -0.586 | 0.441 |
| crossed guard | 5 | 0.906 | 0.000 | -9.071 | 0.992 | -10.793 | 0.851 |

At step 10, task accuracy reaches 1.0 even for failed routing conditions. This
shows that target accuracy alone cannot certify routing preservation.

Source: [`tables/lockin_early_condition_aggregate.csv`](tables/lockin_early_condition_aggregate.csv).

## Final Evidence

Final step 1600 result:

| Condition | Feature NMI | Feature NMI min | Preserve min | Preserve min-min | Current margin | Sign flip rate | Cluster-aware margin | Target accuracy | Max load |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| crossed guard | 0.907 | 0.707 | 0.000 | 0.000 | -6.567 | 0.771 | -7.187 | 1.000 | 0.414 |
| \(q=0.02\) | 0.909 | 0.637 | 0.375 | 0.000 | -0.588 | 0.159 | -0.633 | 1.000 | 0.414 |
| \(q=0.05\) | 1.000 | 1.000 | 1.000 | 1.000 | 0.735 | 0.000 | 0.668 | 1.000 | 0.250 |
| \(q=0\) guard | 0.555 | 0.000 | 0.000 | 0.000 | -2.000 | 0.568 | -2.095 | 1.000 | 0.750 |
| \(q=0.10\) | 1.000 | 1.000 | 1.000 | 1.000 | 0.889 | 0.000 | 0.813 | 1.000 | 0.250 |
| \(q=0.25\) | 1.000 | 1.000 | 1.000 | 1.000 | 1.408 | 0.000 | 1.296 | 1.000 | 0.250 |
| \(q=0.50\) | 1.000 | 1.000 | 1.000 | 1.000 | 2.124 | 0.000 | 1.954 | 1.000 | 0.250 |
| \(q=1.00\) | 1.000 | 1.000 | 1.000 | 1.000 | 3.484 | 0.000 | 3.215 | 1.000 | 0.250 |

Source: [`tables/lockin_final_condition_aggregate.csv`](tables/lockin_final_condition_aggregate.csv).

## Failure Decomposition By Cell

The \(q=0.02\) setting is below the safe threshold in many runs, especially under
nuisance. The most fragile cell is `C2_moderate_nuisance`.

| Cell | Condition | Feature NMI | NMI min | Preserve min | Preserve min-min | Current margin | Sign flip rate | Cluster-aware margin | Max load |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C0 clean | \(q=0.02\) | 0.921 | 0.637 | 0.625 | 0.000 | -0.152 | 0.115 | -0.205 | 0.375 |
| C0 clean | \(q=0.05\) | 1.000 | 1.000 | 1.000 | 1.000 | 0.817 | 0.000 | 0.734 | 0.250 |
| C1 mild nuisance | \(q=0.02\) | 0.900 | 0.866 | 0.250 | 0.000 | -0.681 | 0.177 | -0.712 | 0.438 |
| C1 mild nuisance | \(q=0.05\) | 1.000 | 1.000 | 1.000 | 1.000 | 0.612 | 0.000 | 0.552 | 0.250 |
| C2 moderate nuisance | \(q=0.02\) | 0.883 | 0.866 | 0.125 | 0.000 | -1.102 | 0.219 | -1.145 | 0.469 |
| C2 moderate nuisance | \(q=0.05\) | 1.000 | 1.000 | 1.000 | 1.000 | 0.783 | 0.000 | 0.726 | 0.250 |
| C3 weak feature nuisance | \(q=0.02\) | 0.933 | 0.866 | 0.500 | 0.000 | -0.415 | 0.125 | -0.472 | 0.375 |
| C3 weak feature nuisance | \(q=0.05\) | 1.000 | 1.000 | 1.000 | 1.000 | 0.730 | 0.000 | 0.659 | 0.250 |

Source: [`tables/condition_final_margin_budget_aggregate.csv`](tables/condition_final_margin_budget_aggregate.csv).

## Visualization Results

### Preserve Threshold

![Final preserve versus q](figures/q_threshold_preserve.png)

Purpose: test whether original feature-to-expert identity survives after
initial row gaps are shrunk.

How to read: x-axis is the row-gap scale \(q\); y-axis is final matched preserve
fraction. Higher is better.

Observed result: preserve remains 1.0 for \(q \ge 0.05\) and drops at \(q=0.02\).
The zero-margin and crossed guards fail.

Take-home: the controlled bridge has a finite safe margin region.

Limitation: the plot does not identify a universal threshold; it only brackets
the tested controlled setup.

### Sign Flip Threshold

![Final sign flips versus q](figures/q_threshold_sign_flip.png)

Purpose: test whether preservation loss is tied to boundary crossing.

How to read: y-axis is the fraction of pairwise route margins that changed
sign.

Observed result: sign flips are zero for \(q \ge 0.05\) and nonzero at \(q=0.02\).

Take-home: the failure is a real decision-boundary crossing, not only a metric
artifact.

Limitation: the plot does not by itself separate router drift from feature
center drift.

### Current Margin Trajectory

![Current margin trajectory](figures/current_margin_trajectory.png)

Purpose: show when the boundary is approached or crossed during training.

How to read: y-axis is current minimum margin; negative values mean the feature
has crossed a boundary.

Observed result: \(q=0.02\) reaches negative current margin early. \(q=0.05\) stays
positive and later moves farther into the safe region.

Take-home: preservation is not decided by step-0 sign alone. The margin must
remain positive through early training.

Limitation: the figure does not prove why the drift direction occurs.

### Feature NMI Trajectory

![Feature NMI trajectory](figures/feature_nmi_trajectory.png)

Purpose: show why NMI is secondary rather than primary.

How to read: NMI measures feature separation but not original expert identity.

Observed result: crossed guard and \(q=0.02\) can retain moderate-to-high NMI
while matched preservation fails.

Take-home: future preservation claims must report matched preserve fraction and
margin, not only NMI.

Limitation: NMI can still be useful for discovery quality, but not for identity
preservation.

### Drift Attribution

![Final drift attribution](figures/final_drift_attribution.png)

Purpose: decompose final margin changes into router, feature, and interaction
terms.

How to read: negative shares indicate terms that consume initial margin.

Observed result: successful \(q \ge 0.05\) conditions keep positive total margin
despite drift terms. The \(q=0.02\) condition has no enough initial buffer.

Take-home: the relevant object is margin after drift, not raw initialization
quality alone.

Limitation: this is an empirical decomposition, not a proof of causal update
direction.

## Interpretation

A06_02_01_E06 showed that controlled center initialization preserves because margins
stay positive and sign flips stay zero. A06_02_01_E07 makes that statement sharper:
margin preservation has a finite threshold. The top-1 route does not
automatically protect every positive margin.

The result rejects two overly strong readings:

- It rejects "any positive margin is safe" because \(q=0.02\) starts correct and
  positive but fails after training.
- It rejects "NMI proves preservation" because crossed guard and \(q=0.02\) can
  keep high feature NMI while the original expert identity is lost.

The result supports a more precise model:

\[
\text{preservation requires } \gamma_0 > \Delta_{\text{early drift}},
\]

where \(\gamma_0\) is the initial margin and \(\Delta_{\text{early drift}}\) is the
amount of boundary movement induced by early training.

## Claim Boundary

Can claim:

- Row-gap scaling is a valid controlled intervention in this setup.
- The safe margin region is bounded below between \(q=0.02\) and \(q=0.05\) for
  the tested cells, seeds, and training settings.
- Future route-preservation audits need matched preserve fraction, current
  margin, cluster-aware margin, and sign flips.

Cannot claim:

- The numerical threshold transfers to real-DCLM.
- Center initialization is sufficient for real data.
- The tested margin threshold explains utility binding.
- The intervention tests RoPE, learned position embeddings, or natural
  language feature definitions.

## Artifact Map

Anchor:

- [`../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`](../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md)

Protocol:

- [`protocol.md`](protocol.md)

Result records:

- [`summary.md`](summary.md)
- [`detailed.md`](detailed.md)

Curated tables:

- [`tables/intervention_audit_aggregate.csv`](tables/intervention_audit_aggregate.csv)
- [`tables/lockin_early_condition_aggregate.csv`](tables/lockin_early_condition_aggregate.csv)
- [`tables/lockin_final_condition_aggregate.csv`](tables/lockin_final_condition_aggregate.csv)
- [`tables/condition_final_margin_budget_aggregate.csv`](tables/condition_final_margin_budget_aggregate.csv)
- [`tables/condition_final_margin_budget.csv`](tables/condition_final_margin_budget.csv)
- [`tables/margin_budget_metrics_by_step.csv`](tables/margin_budget_metrics_by_step.csv)
- Pair-level source table (36,864 data rows): `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_23_top1_lockin_margin_threshold/a06_23_top1_lockin_full_20260701_1/tables/margin_budget_by_pair.csv`; SHA-256 `5ed249c11f2d28060125291ccfc3cd89593b35b4a02f59c2b7dac5719146e571`. The byte-identical mainline copy was removed during the 2026-09-24 storage cleanup; the aggregate tables above remain here.

Curated figures:

- [`figures/q_threshold_preserve.png`](figures/q_threshold_preserve.png)
- [`figures/q_threshold_sign_flip.png`](figures/q_threshold_sign_flip.png)
- [`figures/q_threshold_margin.png`](figures/q_threshold_margin.png)
- [`figures/feature_nmi_trajectory.png`](figures/feature_nmi_trajectory.png)
- [`figures/current_margin_trajectory.png`](figures/current_margin_trajectory.png)
- [`figures/final_drift_attribution.png`](figures/final_drift_attribution.png)

Implementation:

- Code workspace:
  `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding`
- Config:
  `configs/a06_23_top1_lockin_margin_threshold.json`
- Runner:
  `scripts/run_a06_23_top1_lockin_margin_threshold.py`
- Raw result directory:
  `results/a06_23_top1_lockin_margin_threshold/a06_23_top1_lockin_full_20260701_1`
- Raw figure directory:
  `figures/a06_23_top1_lockin_margin_threshold/a06_23_top1_lockin_full_20260701_1`
- Logs:
  [`logs/a06_23_top1_lockin_full_20260701_1_shard0.log`](logs/a06_23_top1_lockin_full_20260701_1_shard0.log),
  [`logs/a06_23_top1_lockin_full_20260701_1_shard1.log`](logs/a06_23_top1_lockin_full_20260701_1_shard1.log)

## Next Decision

Apply the same margin-threshold reading to real-DCLM proxy initialization. The
next audit should ask whether the real proxy router has a margin larger than
the measured early drift, instead of only asking whether the step-0 margin is
positive.
