# Detailed: A06_02_03_E03 Background Bias And Margin Budget

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`  
Summary: `summary.md`

## 0. Quick Recap

**Purpose:** Separate background amount, zero-mean variance, and systematic common-direction bias.

**Hypothesis:** Only background gradients with nonzero boundary projection create reproducible margin crossing.

**Conclusion:** Supported in the frozen weighted-top-1 model.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Final margin p05 | Low-tail final matched score gap | fifth percentile over feature-seed cells | Catches non-common damage hidden by averages | Utility |
| Ever-cross rate | Fraction that ever reaches nonpositive margin | trajectory event | Detects transient fragility | Irreversible collapse |
| Re-entry | A crossed feature returns to positive margin | later trajectory event | Separates crossing from failure | Real-text recovery |
| Budget closure | Reconstructed pairwise margin equals measured margin | maximum absolute error | Validates attribution | AdamW transfer |

## 2. Protocol Compliance

| Requirement | Completed |
| --- | --- |
| Seeds | 32, seeds 0-31 |
| Signal counts | 32, 16, 8, 4, 2 |
| Background modes | signal-only, orthogonal zero-mean, common balanced, common biased |
| Training | 500 router-only SGD steps |
| Source attribution | separate signal and background gradients every step |
| Budget validity | maximum closure error \(1.79\times10^{-14}\) |

`common_balanced` was added after smoke and before the full run as a named secondary guard between orthogonal background and target-biased common background. The protocol review notes record this change. It separates common geometry from target bias without changing the primary question.

## 3. Data Construction

Feature centers are

\[
\mu_f=c+u_f,
\]

where \(c\) and all \(u_f\) are mutually orthogonal unit directions. Ideal router rows begin near \(u_f\).

Each 32-position unit contains `signal_count` copies of feature state \(c+u_f\) with target \(f\). Remaining positions use one of:

- **orthogonal zero-mean:** symmetric nuisance states orthogonal to every \(c+u_f\), with balanced targets;
- **common balanced:** state \(c\) with balanced target classes;
- **common biased:** state \(c\) with target class 0.

The construction is not a natural-language model. It isolates whether the background update has a signed projection onto route boundaries.

## 4. Budget Model

For every fixed matched/competitor pair,

\[
m_{f,a,b}(T)=m_{f,a,b}(0)
+\sum_t\Delta m^{signal}_{f,a,b}(t)
+\sum_t\Delta m^{background}_{f,a,b}(t).
\]

Both source gradients are weighted by their fraction of the full-position mean loss, summed for the actual SGD update, and accumulated separately for attribution. Pairwise budgets close exactly up to floating-point error even when the strongest competitor changes.

## 5. Decision Results

### 5.1 Background count is insufficient

At signal fraction 0.0625, both orthogonal zero-mean and common-balanced background retained final margin p05 about 1.260, zero crossings, and final matched-route rate 1.000.

Thus a large background fraction is not sufficient in this model.

### 5.2 Common-biased background creates two thresholds

| Signal fraction | Final margin p05 | Ever crossed | Final matched route | Interpretation |
| ---: | ---: | ---: | ---: | --- |
| 0.500 | 1.154 | 0.000 | 1.000 | safe throughout |
| 0.250 | 0.424 | 0.750 | 1.000 | transient crossing, full recovery |
| 0.125 | -0.001 | 0.750 | 0.734 | boundary-limited final state |
| 0.0625 | -1.128 | 0.750 | 0.250 | persistent failure for non-common features |

The crossing rate is 0.75 because target-0 background helps feature 0 and damages features 1-3.

Feature-wise mean first crossing steps for the three damaged features were approximately:

- 34.6 steps at signal fraction 0.25;
- 26.5 steps at signal fraction 0.125;
- 23.9 steps at signal fraction 0.0625.

At 0.25, all damaged features re-entered their matched regions by step 500. Therefore sign flip is a fragility event, not an irreversible-collapse metric.

## 6. Visualization Results

![Margin budget threshold](figures/margin_budget_threshold.png)

**Purpose:** Distinguish final low-tail stability from any transient boundary crossing.

**Metric definitions:** Left: fifth percentile over final feature-seed minimum matched margins. Right: fraction of feature-seed cells that ever reached nonpositive margin.

**Data source:** `tables/decision_summary.csv`.

**Observed result:** Orthogonal and balanced controls overlap and remain safe. Common-biased background has a transient-cross regime and a persistent-failure regime.

**Allowed conclusion:** Directional mean bias, not background count alone, controls the finite buffer in this model.

**Limitation:** The control removes or exactly balances boundary projection; it does not estimate the effect of finite-sample stochastic variance in a trainable model.

Rendered-artifact audit: both metrics, zero line, signal fractions, and condition legend are readable. The low-tail metric prevents feature-0 gains from hiding rare-feature damage.

## 7. Failure Decomposition

- **Any-background hypothesis:** rejected; high background ratios remain safe in both controls.
- **Common direction alone:** weakened; common-balanced background remains safe.
- **Systematic boundary-aligned bias:** supported.
- **Crossing equals final collapse:** rejected; 0.25 signal fraction recovers after crossing.
- **Budget misses top-1 boundary switches:** rejected for fixed centers and SGD; pairwise closure remains within \(1.79\times10^{-14}\).

## 8. Refined Theory

The controlled preservation condition has three separate terms:

\[
\text{survival/recovery}
\quad\Longleftrightarrow\quad
\text{initial buffer}
+\text{utility-aligned signal}
-\text{boundary-projected bias}
+\text{correction after crossing}.
\]

The first-cross condition depends on the early cumulative budget. Final preservation additionally depends on whether top-1 correction and later signal can re-enter the matched region. One threshold cannot summarize both.

## 9. Claim Boundary And Next Decision

Supported: signed projected background bias is a sufficient controlled cause of margin exhaustion.

Not supported: a real-text common operator, AdamW attribution, hidden-state causality, or a preservation method.

Next decision: test an optimizer-aware finite change decomposition on the one-layer Transformer+MoE full-LM bridge:

\[
\Delta m
=(\Delta w_a-\Delta w_b)^\top\mu_f
+(w_a-w_b)^\top\Delta\mu_f
+(\Delta w_a-\Delta w_b)^\top\Delta\mu_f.
\]

The protocol should compare SGD and AdamW and report first crossing plus re-entry, not only final NMI.

## 10. Artifact Map

- Runner: `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_31_33_router_dynamics.py`
- Config: `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_33_background_bias_margin_budget.json`
- Raw run: `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_31_33_router_dynamics/a06_31_33_full_20260710_001757/A06_02_03_E03/`
- Tables: `tables/condition_trajectory_summary.csv`, `tables/decision_summary.csv`, `tables/feature_final_summary.csv`; full cell trajectories remain in the raw run directory.
- Figure: `figures/margin_budget_threshold.png`
- Hardware: two local H100 GPUs; two 16-seed shards, 7,488 curated trajectory rows per shard before aggregation.
