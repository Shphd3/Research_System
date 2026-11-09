# Detailed: A06_02_03_E02 Top-1 Counterfactual Correction Dynamics

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`  
Summary: `summary.md`

## 0. Quick Recap

**Purpose:** Determine what information weighted top-1 uses to correct a wrong selected expert.

**Hypothesis:** It can reject a bad selected expert but cannot directly identify the best unselected expert, producing rank-dependent search.

**Conclusion:** Supported. Rank-4 correction took 153 steps for top-1 versus 30 for soft routing.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Correction step | First step where the useful expert becomes top-1 | integer 0-200 | Measures correction latency | Stability after correction |
| Boundary count | Number of selected-expert changes | trajectory count | Reveals sequential search | Expert utility |
| Unselected utility gap | Useful unselected row update minus other unselected updates | projection on feature center | Tests utility-specific discrimination | Trainable-MoE efficiency |

## 2. Protocol Compliance

All 32 seeds, both router types, all initial ranks, and all 200 steps completed. Correct-init guards remained matched. Maximum formula closure error was \(1.39\times10^{-17}\).

## 3. Controlled Construction

Four orthogonal feature centers make router score columns independently controllable. For each feature, the useful expert is inserted at exact rank 1, 2, or 4. Other expert ranks follow a cyclic order. This removes ambiguity about whether a correction delay came from hidden geometry.

Fixed expert \(e\) favors target class \(e\). Hidden states and expert outputs do not train.

## 4. Top-1 Gradient Model

For selected expert \(r\) and output \(\hat y=p_rE_r\),

\[
\Delta w_j
=\frac{\eta}{\tau}p_r(\mathbf 1[j=r]-p_j)B_rh.
\]

Unselected rows move through the softmax denominator, but their coefficients contain no \(E_j\). Thus “unselected experts receive no gradient” is inaccurate. The precise statement is: unselected row updates do not evaluate their own counterfactual utilities.

## 5. Full Results

| Method | Initial rank | Correction rate | Mean correction step | Boundary count | Final matched rate | Final margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Soft | 1 | 1.000 | 0 | 0 | 1.000 | 2.859 |
| Soft | 2 | 1.000 | 7 | 1 | 1.000 | 2.771 |
| Soft | 4 | 1.000 | 30 | 1 | 1.000 | 2.818 |
| Weighted top-1 | 1 | 1.000 | 0 | 0 | 1.000 | 2.386 |
| Weighted top-1 | 2 | 1.000 | 12 | 1 | 1.000 | 2.266 |
| Weighted top-1 | 4 | 1.000 | 153 | 142 | 1.000 | 1.138 |

The values are invariant across random orthogonal rotations, so the 32 seeds act as a geometry-rotation robustness audit rather than independent stochastic training trajectories.

## 6. Visualization Results

![Correction time by initial rank](figures/correction_time_by_initial_rank.png)

**Purpose:** Test whether recovery depends on how far the useful expert is below the current top-1 boundary.

**Data source:** `tables/condition_summary.csv`.

**Observed result:** The rank penalty is 23 steps for soft routing and 141 for weighted top-1.

**Allowed conclusion:** Weighted top-1 correction is strongly rank-mediated in this model.

**Remaining uncertainty:** A trainable expert can change the selected expert's utility during search, which this audit intentionally freezes.

Rendered-artifact audit: rank values, method legend, correction-step units, and censoring rule are visible.

## 7. Failure Decomposition

- **No-gradient explanation:** rejected. Top-1 has nonzero updates and eventually recovers.
- **Direct counterfactual correction:** weakened. Rank-4 useful experts initially have a negative unselected utility gap.
- **Saturation-only explanation:** weakened by exact rank control and the contrast with soft routing at the same temperature and score scale.
- **Permanent lock-in:** rejected in this finite controlled run; all cells recovered by step 200.

## 8. Refined Mechanism

Top-1 performs two operations:

1. It evaluates whether increasing the currently selected expert's gate amplitude helps.
2. If the selected expert is bad, softmax competition lowers it and raises alternatives according to current probability rank.

It does not know which unselected expert is useful until that expert is selected. The resulting sequential search can be slower than the rate at which external background updates consume margin.

## 9. Claim Boundary And Next Decision

Supported: rank-mediated correction and missing utility-specific unselected comparison.

Not supported: permanent lock-in, natural expert specialization, or a method recommendation.

Next decision: combine correction dynamics with source-separated cumulative margin pressure in A06_02_03_E03.

## 10. Artifact Map

- Runner: `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_31_33_router_dynamics.py`
- Config: `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_32_top1_counterfactual_correction_dynamics.json`
- Raw run: `../../../../XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_31_33_router_dynamics/a06_31_33_full_20260710_001757/A06_02_03_E02/`
- Tables: `tables/cell_results.csv`, `tables/trajectory.csv`, `tables/condition_summary.csv`
- Figure: `figures/correction_time_by_initial_rank.png`
- Hardware: two local H100 GPUs; seeds 0-15 and 16-31.
