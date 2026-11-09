# Protocol: A11_03_01_E01 Head-Position Cross-Kernel

## 0. Approval Snapshot

**Purpose:** separate output-head and state-position causes of A11_17's cross-interface sign loss.  
**Experiment role:** root-cause audit.  
**Primary metric:** post-burn-in `20-200` AUC of four normalized usefulness cells.  
**Conditions:** five NTP trajectories only.  
**Cannot claim:** global MTP efficiency or architecture superiority.

## 1. Fixed Setup

- exact A11_17 model, data, seen diagnostic batch, H2 copy, NTP training, optimizer, seeds, schedule, and checkpoints;
- cells: `h2_at_t`, `h1_at_t`, `h2_at_t1`, `h1_at_t1`;
- primary interval: steps `20-200`; step 0 is reported as the known CE transient;
- central perturbation relative norm `1e-6` and exact restore;
- A11_17 NTP curve mean reproduction tolerance `0.05`.

## 2. Metric

For each head \(a\) and position \(p\):

\[
\widehat U_{a,p}
=-\frac{\langle\nabla_{\theta_S}M_{a,p},g_D^S\rangle}
{\|\nabla_{\theta_S}M_{a,p}\|\|g_D^S\|}.
\]

The same seen examples, labels, H2 gradient, and shared parameters are used in all four cells.

## 3. Decision Rules

- direct baseline pass: `h2_at_t` AUC positive `4/5`;
- head switch pass: `h1_at_t` AUC positive `4/5`;
- position switch pass: `h2_at_t1` AUC positive `4/5`;
- full transport pass: `h1_at_t1` AUC positive `4/5`.

Classify head, position, both/interaction, no local bottleneck, mixed, or insufficient exactly as stated in the anchor. The finite-difference sign must match all four cells in at least `4/5` seeds at step 20; all restore, balance, coverage, and curve guards must pass.

## 4. Required Outputs

- per-seed four-cell trajectories and post-burn-in AUC;
- finite-difference sign table;
- one four-cell trajectory/decision figure;
- canonical summary, detailed, anchor, and story updates.

## 5. Boundary

The experiment isolates a local bilinear cross-kernel factor. It does not test pure MTP pretraining, optimizer-level convergence, matched FLOPs, or external tasks.
