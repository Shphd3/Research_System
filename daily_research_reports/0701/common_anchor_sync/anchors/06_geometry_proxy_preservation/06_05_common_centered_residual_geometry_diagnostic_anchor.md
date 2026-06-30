---
anchor_id: A06_05_common_centered_residual_geometry_diagnostic
parent_node: rq.feature_specialization.initialization_geometry
status: closed_supported
created: 2026-06-21
updated: 2026-06-21
canonical_language: en
---

# A06_05 Common-Centered Residual Geometry Diagnostic Anchor

## 0. Thinking Card
父问题：uniform feature distribution 下，初始化 dot-product top-1 gate 为什么仍可能产生 step-0 load imbalance，并阻碍 feature-level specialization。
当前子问题：A06_04 已支持 hidden common component 是 synthetic hidden-state step-0 imbalance 的主导 tested source；但 common-centering 后仍有 residual load，需要继续拆。
当前判断：A06_05 已支持 residual covariance / structured residual geometry 是 common-centered residual load 的主要来源；finite-sample noise 不是主解释。
关键证据：primary readout `num_layers=1, post_ln` 中 centered residual `L=0.2577`，whitened `L=0.1071`，matched isotropic `L=0.0874`；样本数从每 pair 256 到 4096 时 `L` 仍约 `0.2694 -> 0.2577`。
最危险边界：这仍只是 initialized synthetic hidden-state replay；白化是诊断控制，不是最终 router 方法；position/pair conditional load 高但不能单独证明 aggregate imbalance 的因果来源。
下一步决策：进入 A06_06 oracle feature-level initialization positive control，测试 feature-level initialization 是否能压过这里确认的 residual geometry。

Question:
After hidden common-centering, what explains the remaining step-0 load imbalance: residual hidden anisotropy, router-direction cell geometry, random-context / position structure, or finite-sample noise?

Physical prior:
Removing the global hidden common component removes the feature-shared effective bias term, but the residual hidden states may still be non-isotropic or structured by context / position.

Core model:
Decompose hidden states as `h_i = c + r_i`. A06_04 tested the common term `w_e^T c`. This anchor studies the residual replay `z_{i,e}=w_e^T r_i` and asks why its top-1 cells remain imbalanced.

Model term being tested:
Residual distribution geometry: covariance anisotropy, residual decision-cell probabilities, context / position conditioning, and finite sample floor.

Primary metric:
Load imbalance `L = m max_e |p_e - 1/m|` under common-centered replay.

Falsifier:
If residual replay imbalance is fully explained by finite-sample noise, or if whitening / isotropic controls / context-position controls do not change or explain the residual load, then the named residual geometry sources are weakened.

Can claim:
Mechanism evidence for the source of residual load after common-centering in this synthetic initialized hidden-state setting.

Cannot claim:
Training collapse, semantic expert specialization, real-text behavior, or a deployable initialization / router method.

Next decision:
Proceed to A06_06 as an oracle feature-level initialization positive control, carrying residual covariance / structured residual geometry as the main boundary.

## 1. Problem Definition

Parent problem:
Uniform symbolic features can still produce non-uniform initialized top-1 routing after embedding and transformer hidden-state formation.

Immediate prior result:
A06_04 showed that hidden common-centering is the main effective control among norm/common/interactions, but residual load remains.

Decision question:
In the same synthetic hidden-state setting, after removing the hidden common component, is the remaining load imbalance caused by residual hidden anisotropy, router-direction cell geometry, context / position structure, or finite-sample effects?

Not in scope:
Training, final collapse, real text, expert utility, method design, or changing the task.

## 2. Physical Priors

P1: Common-centering does not guarantee isotropic residuals.
Meaning: `r_i = h_i - c` may have anisotropic covariance or low-dimensional structure.
Could be wrong if: whitening or matched isotropic controls do not reduce or explain residual load.

P2: Router-direction cells can remain imbalanced on the residual distribution.
Meaning: even if `mean(r_i)=0`, top-1 cells induced by fixed router rows may have unequal probability under the residual distribution.
Could be wrong if: large-sample residual replay has no fixed cell floor beyond sampling error.

P3: Random context / position can condition the residual geometry.
Meaning: residual states may differ by pair start, local context, or background-token configuration even when pair labels are uniform.
Could be wrong if: load and residual geometry are invariant after conditioning or shuffling these factors.

P4: Finite sample can still inflate measured residual load.
Meaning: observed `p_hat_e` may be noisy around true residual cell probabilities.
Could be wrong if: larger samples or bootstrap estimates show a stable nonzero floor.

## 3. Falsifiable Hypotheses

H1: Residual covariance anisotropy contributes.
Supported if: covariance whitening of `r_i` reduces residual replay `L` relative to centered-only replay.
Weakened if: whitening leaves `L` unchanged while preserving numerical validity.

H2: Router-direction cell geometry contributes.
Supported if: a matched isotropic residual distribution has lower `L` than real residuals under the same router rows, or if estimated true residual cell probabilities remain unequal at large sample size.
Weakened if: matched isotropic controls show the same residual `L`.

H3: Context / position structure contributes.
Supported if: `L` or expert assignment changes systematically with pair start, local context, or background-token factors.
Weakened if: conditioning / shuffling these factors leaves residual load unchanged.

H4: Residual load is mostly finite-sample noise.
Supported if: increasing sample count drives residual observed load toward uniform and bootstrap floor is near zero.
Weakened if: larger samples preserve a nonzero fixed residual floor.

## 4. Mathematical Model

Objects:
For sample `i`, expert `e`, hidden state `h_i`, router row `w_e`, common component `c`, residual `r_i=h_i-c`, and expert assignment `a_i`.

Common-centered replay:

```math
z^{C}_{i,e}=w_e^T r_i = w_e^T(h_i-c)
```

Observed residual load:

```math
a_i = \arg\max_e z^C_{i,e}, \quad
p_e = \frac{1}{N}\sum_i \mathbf{1}[a_i=e], \quad
L = m \max_e \left|p_e-\frac{1}{m}\right|.
```

Residual geometry decomposition:

```math
r_i \sim P_r, \quad
\Sigma_r = \mathbb{E}[r_i r_i^T], \quad
p_e^r = \Pr_{r\sim P_r}\left(e=\arg\max_j w_j^T r\right).
```

Candidate controls:

```math
r_i^{white}=\Sigma_r^{-1/2}r_i
```

and matched isotropic samples `r_i^{iso}` with the same dimension, sample count, and norm scale.

## 5. Computational Realization

Input objects:
Use the same synthetic `(slot,target)` data, initialized model, extracted router-input hidden states, and router rows as A06_04.

Required controls:

1. `centered_replay`: replay `w_e^T(h_i-c)`.
2. `centered_whitened_replay`: replay `w_e^T Sigma^{-1/2}(h_i-c)`.
3. `matched_isotropic_replay`: replay same router rows on isotropic samples matched in dimension and norm scale.
4. `context_position_stratified_replay`: read load by pair start, local context, and background-token factors.
5. `sample_count_guard`: bootstrap or larger-sample replay to estimate finite-sample floor.

Primary outputs:
Condition-wise `L`, max load, per-expert load, bootstrap intervals, residual covariance spectrum, context / position-conditioned loads.

Secondary outputs:
slot_NMI, per-slot route purity, assignment heatmaps, margin distributions.

## 6. Minimal Falsification Tests

Test 1: Residual whitening.
Question: Does residual covariance anisotropy explain common-centered residual load?
Primary metric: change in `L` from centered replay to centered+whitened replay.
Supports: whitening reduces `L` without destroying sample validity.
Weakens: whitening leaves `L` near centered replay.
Insufficient: whitening implementation changes model state or uses wrong hidden extraction.

Test 2: Matched isotropic residual control.
Question: Is real residual geometry more imbalanced than an isotropic residual baseline?
Primary metric: real-centered `L` vs matched-isotropic `L`.
Supports: real residuals have higher `L` than isotropic controls.
Weakens: both are similar.
Insufficient: isotropic samples are not norm/dimension/sample matched.

Test 3: Context / position stratification.
Question: Does residual load depend on non-feature context or pair position?
Primary metric: conditional load deviation across strata.
Supports: expert assignment or `L` shifts systematically by context / position.
Weakens: no systematic conditional effect.
Insufficient: strata are too sparse or pair distribution is not uniform.

Test 4: Finite-sample floor.
Question: Is residual load just finite-sample noise?
Primary metric: bootstrap / larger-sample estimate of residual true cell imbalance.
Supports finite-sample explanation: residual load shrinks to near zero.
Weakens finite-sample explanation: stable nonzero floor remains.

## 7. Current Evidence

Observation:
A06_03 supports row-norm variation as a causal source in pure gate-only high-dimensional uniform routing.
Boundary:
That result does not include model-generated hidden states.

Observation:
A06_04 supports hidden common component as the dominant tested source in synthetic initialized hidden states: primary readout `RR=0.5578`, `NR=0.5577`, `RC=0.2578`, `NC=0.2407`. Common-centering reduces load strongly; norm-control does not.
Boundary:
Common-centering does not remove all load imbalance. Residual load remains and is not yet decomposed.

Observation:
A06_05 decomposed the remaining common-centered residual load using the same synthetic hidden-state replay surface as A06_04. In the primary readout (`num_layers=1`, `post_ln`), `centered_replay L=0.2577`, `centered_whitened_replay L=0.1071`, and `matched_isotropic_replay_mean L=0.0874`. The sample-count guard stays near `0.2694 -> 0.2577` from 256 to 4096 samples per pair.
Interpretation:
Residual covariance / structured residual geometry is supported as the main tested source of the remaining load. Matched isotropic replay gives a smaller nonzero floor, and finite-sample noise is weakened as the main explanation.
Boundary:
Whitening is a diagnostic control, not a proposed router. Position-conditioned and pair-conditioned loads are high, but the run does not prove that position alone causes aggregate imbalance.
Evidence links:
`../../experiments/A06/A06_05_common_centered_residual_geometry_diagnostic/summary.md`
`../../experiments/A06/A06_05_common_centered_residual_geometry_diagnostic/detailed.md`

Observation:
0608 and later handoff evidence indicate that common-logit bias can seed early routing collapse, but final collapse also involves top-1 training amplification / anti-lockin dynamics.
Boundary:
This anchor stays at initialized replay diagnosis.

## 8. Claim Boundary And Next Decision

Can claim:
In initialized synthetic hidden-state replay, after hidden common-centering, residual covariance / structured residual geometry explains a substantial part of the remaining step-0 load imbalance; finite-sample noise is not the main explanation at the tested sample scale.

Cannot claim:
This solves collapse, gives feature-level specialization, proves expert utility, or transfers to real text.

Next decision:
Run A06_06 as an oracle feature-level initialization positive control. If oracle feature-level initialization cannot overcome this residual geometry, label-free method construction should be weakened. If it can, A06_07 may test whether a label-free common/residual control approximates the oracle.
