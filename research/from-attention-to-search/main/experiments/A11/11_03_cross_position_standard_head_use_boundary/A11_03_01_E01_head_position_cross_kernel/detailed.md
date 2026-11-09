# A11_03_01_E01 Head-Position Cross-Kernel: Detailed Evidence

## 0. Result

Status: **position bottleneck supported**. Head identity has negligible effect at a fixed state position; moving from \(h_T\) to \(h_{T+1}\) reverses post-burn-in usefulness in all five seeds.

## 1. Four-Cell Design

The same H2-loss gradient \(g_D^S\) is evaluated against four A/B margins on the same seen examples:

| Cell | Changed relative to direct H2 | Purpose |
|---|---|---|
| H2 at \(h_T\) | none | direct self baseline |
| H1 at \(h_T\) | head only | output-readout compatibility |
| H2 at \(h_{T+1}\) | position only | cross-position Jacobian transport |
| H1 at \(h_{T+1}\) | head and position | actual downstream interface |

For each:

\[
\widehat U_{a,p}
=-\frac{\langle\nabla M_{a,p},g_D^S\rangle}
{\|\nabla M_{a,p}\|\|g_D^S\|}.
\]

The primary statistic is trapezoidal AUC over steps `20,100,200`. Step 0 is not used because A11_17 already established a full-vocabulary CE transient.

## 2. Protocol Compliance

- final job `pt-c60nyzy6`: succeeded;
- first submission `pt-sl8wxoqr` exited before Python because the shell left `${R}` undefined; no experiment ran;
- 5/5 final tasks, 25 checkpoints, 100 four-cell rows;
- all diagnostic balance, H2-copy, coverage, finite-value, restore, and split-size guards pass;
- A11_17 NTP curve means reproduce exactly;
- step-20 finite-difference sign validates all four cells in seeds 971, 972, 973, and 975;
- seed 974 has all four predicted values within `0.01` of zero and fails the strict sign guard, leaving the preregistered `4/5` validity threshold satisfied.

## 3. Per-Seed AUC

| Seed | H2@\(h_T\) | H1@\(h_T\) | H2@\(h_{T+1}\) | H1@\(h_{T+1}\) |
|---:|---:|---:|---:|---:|
| 971 | 0.3238 | 0.3234 | -0.0436 | -0.0435 |
| 972 | 0.3206 | 0.3202 | -0.0366 | -0.0366 |
| 973 | 0.0048 | 0.0051 | -0.1140 | -0.1126 |
| 974 | 0.1345 | 0.1346 | -0.1498 | -0.1481 |
| 975 | 0.1198 | 0.1197 | -0.1890 | -0.1828 |

The sign separation is complete: both \(h_T\) cells are positive in every seed, and both \(h_{T+1}\) cells are negative in every seed.

## 4. Time-Resolved Means

| Step | H2@\(h_T\) | H1@\(h_T\) | H2@\(h_{T+1}\) | H1@\(h_{T+1}\) |
|---:|---:|---:|---:|---:|
| 0 | -0.0626 | -0.0622 | -0.0630 | -0.0625 |
| 20 | 0.0775 | 0.0772 | 0.0578 | 0.0575 |
| 100 | 0.0545 | 0.0547 | -0.0676 | -0.0641 |
| 200 | 0.4903 | 0.4899 | -0.3082 | -0.3077 |
| 300 | 0.5653 | 0.5649 | -0.2893 | -0.2887 |

The sign reversal develops between steps 20 and 100 and strengthens by step 200. This is not an initialization artifact.

## 5. Head Is Not The Bottleneck

At every checkpoint, switching H2 to H1 while holding position fixed changes normalized usefulness by at most a few thousandths in the mean. At step 300:

\[
\widehat U_{H2,T}=0.5653,
\qquad
\widehat U_{H1,T}=0.5649,
\]

and:

\[
\widehat U_{H2,T+1}=-0.2893,
\qquad
\widehat U_{H1,T+1}=-0.2887.
\]

Thus copied-head drift and answer-row mismatch do not explain the A11_17 transport failure.

## 6. Cross-Position Kernel Law

Let \(d_2\) be the useful H2 hidden direction after burn-in. The current-state standard-H1 usefulness is:

\[
U_{1,T}=v_1^\top J_TJ_T^\top d_2.
\]

The next-state usefulness is:

\[
U_{1,T+1}=v_1^\top J_{T+1}J_T^\top d_2.
\]

The first expression uses a self-kernel; the second uses a non-symmetric cross-position kernel. Positive current-state formation therefore does not mathematically imply positive later-state transport. A11_03_01_E01 supplies a controlled pretrained example where the signs are opposite in `5/5` seeds by post-burn-in AUC.

## 7. Visualization Results

### Plot Contract

**Question:** does the head switch or position switch remove usefulness?  
**Left:** mean trajectories, with step 20 marking burn-in start.  
**Middle:** positive AUC seed counts; dashed line is the `4/5` pass threshold.  
**Right:** step-20 finite-difference sign validation.  
**Allowed conclusion:** local head versus position transport.  
**Limitation:** the only bridge token is `Decision` and only one-step transport is tested.

![A11_03_01_E01 head-position transmission](figures/a11_18_head_position_cross_kernel.png)

## 8. Hypothesis Audit

| Hypothesis | Result | Decision |
|---|---|---|
| H1 direct baseline | positive AUC 5/5 | supported |
| H2 head transport | positive AUC 5/5 | supported |
| H3 position transport | positive AUC 0/5 | falsified |
| H4 full transport | positive AUC 0/5 | falsified |

## 9. Claim Boundary

**Observation:** head-invariant sign, position-dependent reversal.  
**Interpretation:** semantic update formation at \(h_T\) is locally useful, but parameter effects on \(h_{T+1}\) oppose that direction after burn-in.  
**Claim:** positive cross-position semantic kernel alignment is an additional condition for downstream MTP efficiency.  
**Cannot claim:** all bridge tokens cause reversal, MTP pretraining is harmful, the same holds over longer generation, or final benchmark scores are determined by this local derivative.

## 10. Artifact Map

Raw result:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
results/a11_18_head_position_cross_kernel/
a11_18_head_position_cross_kernel_4gpu_20260711_010000
```

Logs:

```text
.../logs/acp/a11_18_head_position_cross_kernel_4gpu_20260711_010000
```

Code:

```text
configs/a11_18_head_position_cross_kernel.json
scripts/run_a11_18_head_position_cross_kernel.py
scripts/analyze_a11_18_head_position_cross_kernel.py
scripts/submit_a11_18_head_position_cross_kernel_4gpu.sh
```

## 11. Next Decision

Audit whether the one-token transport sign depends on the bridge token under a frozen prompt and gradient. Use only a few natural bridge tokens selected before the run. If the sign is robustly negative, formalize a general cross-position transport condition; if token-dependent, the theory must condition on the intervening token/state transition.
