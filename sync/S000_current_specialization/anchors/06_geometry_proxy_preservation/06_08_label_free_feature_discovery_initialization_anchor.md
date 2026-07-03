---
anchor_id: A06_08_label_free_feature_discovery_initialization
parent_node: rq.feature_specialization.initialization_method
status: supported_pending_training_basin
created: 2026-06-22
canonical_language: en
---

# A06_08 Label-Free Feature Discovery Initialization Anchor

## 0. Thinking Card
父问题：uniform feature 下，random-init top-1 MoE 为什么不能自然形成 feature-level specialization。
当前子问题：A06_06 证明 oracle feature centers 可达；A06_07 证明 global centering / projection / whitening 只修 load。A06_08 只问：无标签 route-position clustering 能不能找到 pseudo-feature centers。
当前判断：A06_08 支持 label-free route-position residual clustering；这是 step-0 discovery 成功，不是训练成功。
关键证据：k-means 和 spherical k-means 在 48/48 full-grid cells 都达到 `feature_NMI=1.0, L=0`；calibration mean 主读数只到 NMI `0.2072`。
最危险边界：`pair_id` 只能用于 evaluation；spectral/dictionary 不稳定；还没证明 training 会保留这个 partition。
下一步决策：把 `route_kmeans_residual_K4` 作为 best pseudo init 交给 A06_09。

- Question: Can label-free route-position clustering recover pseudo-feature centers close to the A06_06 oracle partition?
- Physical prior: Feature signal exists, but a single global control cannot construct one center per feature.
- Core model: $h_i=c+r_i$; discover centers $\nu_k$ from calibration residuals $r_i$ without labels.
- Model term being tested: label-free recoverability of feature-aligned residual centers.
- Primary metric: held-out `feature_NMI`; load $L$ is a guard.
- Falsifier: load improves but NMI does not, labels leak, or clusters are nuisance-aligned.
- Can claim: label-free residual clustering works in synthetic initialized hidden states.
- Cannot claim: training stability, real DCLM transfer, expert utility, or reliability of spectral/dictionary discovery.
- Next decision: pass `route_kmeans_residual_K4` pseudo init to A06_09.

## 1. Problem Definition

Parent problem: uniform feature frequency does not imply feature-level MoE specialization.
Sharper subproblem: oracle centers work, global label-free controls fail; test whether label-free pseudo-centers bridge that gap.
Decision question: can route-position discovery without `pair_id` improve held-out feature_NMI over A06_07 controls and toward A06_06 oracle?
Not in scope: training, anti-lockin, real text, expert utility, broad method search.

## 2. Physical Priors

- P1: Residual hidden states may contain feature-aligned centers. Could be wrong if residual structure is mainly position/context/noise.
- P2: Global controls are load controls, not feature discovery. Could be wrong if global preprocessing plus random rows reaches oracle-level NMI.
- P3: The test is invalid if labels enter discovery. `pair_id` is evaluation-only.

## 3. Falsifiable Hypotheses

- H1: Route-position residual clustering recovers pseudo-feature centers. Supported: k-means and spherical k-means pass 48/48 cells.
- H2: Spectral and dictionary discovery are less reliable. Supported: spectral passes 13/48 and dictionary K4 passes 8/48.
- H3: Nuisance alignment must be ruled out. Supported for k-means: primary cluster-pair NMI `1.0`, pair-start NMI about `0.0024`.

## 4. Mathematical Model

Objects: hidden state $h_i$, common mean $c$, residual $r_i=h_i-c$, discovered center $\nu_k$, router row $w_e$, evaluation-only feature label $f_i$.

Core model:
$$
h_i=c+r_i,\qquad r_i\approx \mu_{f_i}+\epsilon_i.
$$

Label-free centers:
$$
\{\nu_k\}_{k=1}^{4}=\operatorname{Discover}(\{r_j:j\in C\}),\qquad
w_e=\alpha\frac{\nu_e}{\|\nu_e\|}.
$$

Observable metrics: `feature_NMI`, oracle-gap fraction, load $L$, margin p05, feature purity, route heatmap, leakage and nuisance audits.
Falsifier: low NMI with good load.

## 5. Computational Realization

- Input: same A06_04-A06_07 synthetic hidden-state replay surface, with balanced calibration/evaluation split.
- Compute: $c_{\text{calib}}$, residuals, optional normalized residuals, discovered centers, equal-norm router rows.
- Run: reproduce random / A06_07 calibration-mean / A06_06 oracle baselines; fit clustering, spectral, and dictionary route-position discovery; evaluate held-out routing.
- Audit: split balance, label leakage, cluster occupancy, nuisance alignment.
- Artifacts: `protocol.md`, `summary.md`, `detailed.md`, `tables/discovery_summary.csv`, `figures/nmi_by_method.png`, `figures/route_heatmap_by_method.png`.

## 6. Minimal Falsification Tests

Test 1: route-position pseudo-center discovery.
Question: do unsupervised centers improve held-out feature_NMI?
Comparison: random/equal-norm, A06_07 calibration mean, k-means, spherical k-means, spectral, dictionary, oracle.
Supports: NMI/oracle-gap gate passes without leakage.
Weakens: load-only improvement or many-to-one merge.

Test 2: nuisance guard.
Question: are clusters feature-aligned rather than position/context-aligned?
Comparison: cluster NMI with `pair_id` and nuisance variables.
Supports: feature alignment explains the gain.
Weakens: nuisance alignment explains the clusters.

## 7. Current Evidence

- A06_08 full: k-means and spherical k-means recover the oracle partition in all 48 cells (`feature_NMI=1.0`, $L=0$). Summary: `../../experiments/A06/A06_08_label_free_feature_discovery_initialization/summary.md`.
- A06_08 guards: split balanced, route position valid, and label-free leakage is zero. Spectral/dictionary are partial and unstable.
- A06_06/A06_07 context remains: oracle centroids are reachable, while global controls improve load without recovering feature_NMI.

## 8. Claim Boundary And Next Decision

Can claim: label-free route-position residual clustering recovers pseudo-feature centers in the synthetic initialized A06 setting.
Cannot claim: training stability, real-data transfer, expert utility, semantic specialization, or reliability of spectral/dictionary discovery.
Next decision: use `route_kmeans_residual_K4` as the A06_09 pseudo initialization and test whether ordinary training preserves the partition.
