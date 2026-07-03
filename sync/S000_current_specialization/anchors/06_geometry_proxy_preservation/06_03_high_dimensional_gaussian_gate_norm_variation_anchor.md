# 06_03 High-Dimensional Gaussian Gate Norm Variation Anchor

## 0. Thinking Card
总目标/父问题：判断是否存在一种更稳健的 gate 初始化，使近似均匀的高维 hidden states 更均匀地分发到 experts，减少早期负载不均诱发的路由坍缩风险。
当前子问题：把高维 gate-only load imbalance 分解为三项：token sampling variance、Gaussian prototype direction/cell imbalance、row-norm variation。
当前判断：token sampling error 会随 token 数增加而下降；normalized directions 的固定 cell imbalance 随维度升高而缩小；Gaussian-scaled gate 的额外 fixed floor 主要来自 row-norm variation。
关键证据：本地 norm-control 实验中，Gaussian-scaled 在全部 6 个 `(d,m)` 组上高于 norm-controlled；norm-controlled 与 normalized directions 重合。
最危险边界：该结论只解释随机初始化、纯 gate-only、均匀高维输入下的初始几何负载不均，不能直接推出 trained MoE collapse 或语义专家分化。
下一步决策：是否把 row-norm variation 作为解释 trained-router load imbalance 前的必要诊断基线。

Question:
Does row-norm variation causally explain the extra true decision-cell imbalance of a standard Gaussian-scaled dot-product top-1 gate in a pure high-dimensional gate-only setting?
Physical prior:
Dot-product scores depend on both row direction and row norm: $z_e=w_e^\top x=\rho_e u_e^\top x$.
Core model:
$w_e=\rho_e u_e$, $z_e=\rho_e u_e^\top x$, and $\hat p_e-1/m=(p_e-1/m)+(\hat p_e-p_e)$.
Model term being tested:
The norm scale term $\rho_e$.
Primary metric:
True cell imbalance $m\max_e |p_e-1/m|$.
Falsifier:
Not observed in the local paired run; norm-controlled Gaussian gates did not remain as imbalanced as Gaussian-scaled gates after row-norm variation was removed.
Can claim:
Mechanism evidence for load imbalance decomposition in pure gate-only uniform high-dimensional routing.
Cannot claim:
Trained MoE collapse, semantic specialization, attention/residual behavior, or a final router method.
Next decision:
Whether row-norm variation should become a required diagnostic baseline before trained-router load imbalance is interpreted as semantic or data-driven specialization.

## 1. Problem Definition

Parent problem:
Can a high-dimensional gate initialization make uniformly distributed features route uniformly across experts, thereby reducing early load-imbalance pressure before training dynamics amplify it?

Sharper subproblem:
For a pure high-dimensional Gaussian dot-product top-1 gate with uniform input, decompose observed load imbalance into:
finite-token sampling noise, normalized random-direction decision-cell imbalance, and Gaussian row-norm variation.

Decision question:
Does removing only row-norm variation reduce the Gaussian-scaled gate's true decision-cell imbalance toward the normalized-direction baseline?

Not in scope:
No attention, residual stream, training, experts, semantic features, learned MoE collapse claim, or final gating method design.

## 2. Physical Priors

P1: Dot-product gate score has a direction term and a norm term.
Meaning: Writing $w_e=\rho_e u_e$ gives $z_e=\rho_e u_e^\top x$, so top-1 cell size can change when $\rho_e$ changes even if $u_e$ is fixed.
Could be wrong if: row norms vary but do not change top-1 cell probabilities after conditioning on direction geometry.

P2: More tokens reduce sampling error but not the fixed cell geometry of one gate initialization.
Meaning: $\hat p_e-p_e$ should shrink with token count, while $p_e-1/m$ is fixed for the sampled gate.
Could be wrong if: large-MC estimates of $p_e$ are too noisy or observed error is dominated by implementation artifacts.

## 3. Falsifiable Hypotheses

H1: Gaussian-scaled gates have larger true cell imbalance than normalized-direction gates.
Supported if: $m\max_e |p^{gaussian}_e-1/m|$ is consistently larger than $m\max_e |p^{normalized}_e-1/m|$ across matched $d,m$ settings.
Weakened if: Gaussian-scaled and normalized gates have similar true cell imbalance despite nonzero row-norm variation.

H2: Removing only row-norm variation reduces true cell imbalance.
Supported if: norm-controlled Gaussian gates move the true cell imbalance close to the normalized-direction condition and below Gaussian-scaled gates.
Weakened if: norm-controlled Gaussian gates remain close to Gaussian-scaled gates after `row_norm_cv` is removed.

H3: Token count increase reduces sampling error but not the fixed gate floor.
Supported if: $m\max_e |\hat p_e-p_e|$ decreases with token count while $m\max_e |p_e-1/m|$ remains stable for the same gate.
Weakened if: the apparent fixed floor disappears after increasing token count or true-cell MC precision.

## 4. Mathematical Model

Objects:
Gate rows $w_e$, row norm $\rho_e=\|w_e\|$, unit direction $u_e=w_e/\|w_e\|$, uniform high-dimensional input $x$, true cell probability $p_e$, finite-token load $\hat p_e$.

Core decomposition:
$$
w_e=\rho_e u_e,\quad z_e=\rho_e u_e^\top x
$$

Mechanism relation:
$$
p_e=\mathbb{P}\left(e=\arg\max_j \rho_j u_j^\top x\right)
$$

Observed load decomposition:

$$
\hat p_e-\frac{1}{m}
=
\left(p_e-\frac{1}{m}\right)
+
\left(\hat p_e-p_e\right)
$$

Observable metrics:
True cell imbalance $m\max_e |p_e-1/m|$, observed load error $m\max_e |\hat p_e-1/m|$, sampling error $m\max_e |\hat p_e-p_e|$, and `row_norm_cv`.

Falsifier:
If setting all $\rho_e$ equal does not reduce true cell imbalance relative to the same Gaussian directions with original $\rho_e$, row-norm variation is not the main extra source.

## 5. Computational Realization

Input objects:
Sample Gaussian gate rows $W\in\mathbb{R}^{m\times d}$ and random unit inputs $x\in\mathbb{R}^d$.

Computed variables:
$\rho_e=\|w_e\|$, $u_e=w_e/\rho_e$, top-1 assignments under normalized, Gaussian-scaled, and norm-controlled gates.

Algorithm stages:
Estimate $p_e$ by large Monte Carlo; estimate $\hat p_e$ at smaller token counts; compute true, observed, sampling, and row norm metrics.

Stage-local evidence:
Paired comparison of Gaussian-scaled and norm-controlled gates using the same sampled directions.

Expected artifacts:
`tables/results.csv`, `tables/aggregate_by_condition.csv`, `figures/true_cell_imbalance.png`, `summary.md`, and `detailed.md`.

## 6. Minimal Falsification Tests

Test:
Compare normalized random directions, standard Gaussian-scaled gates, and norm-controlled Gaussian gates.
Question:
Does removing only row-norm variation reduce the extra Gaussian true cell imbalance?
Intervention / comparison:
Use identical Gaussian directions for the Gaussian-scaled and norm-controlled conditions, but set all row norms equal in the norm-controlled condition.
Primary metric:
True cell imbalance $m\max_e |p_e-1/m|$.
Supports:
Gaussian-scaled > norm-controlled, and norm-controlled is close to normalized with `row_norm_cv=0`.
Weakens:
Gaussian-scaled and norm-controlled have similar true cell imbalance after row-norm variation is removed.
Insufficient evidence:
Large-MC true cell estimates are noisy, conditions are not direction-matched, or norm control changes another property.

## 7. Current Evidence

Prior observation:
The 0620 high-dimensional gate-only experiment found that token count reduces sampling error, normalized-direction true cell imbalance shrinks with dimension, and Gaussian-scaled gates have larger true cell imbalance.

New experiment:
`Projects/from-attention-to-search/main/experiments/A06/A06_03_high_dimensional_gaussian_gate_norm_variation/`

Result:
The paired norm-control experiment supports row-norm variation as a causal contributor to the extra Gaussian fixed gate-only imbalance. Across all tested `(d,m)` settings, Gaussian-scaled true cell imbalance was higher than norm-controlled Gaussian, while norm-controlled Gaussian matched normalized directions.

Primary evidence:
For `(d=32,m=32)`, true cell imbalance decreased from 1.1910 to 0.2686 after row norms were equalized. For `(d=512,m=32)`, it decreased from 0.3120 to 0.0854. All six tested `(d,m)` groups had positive paired Gaussian-minus-controlled deltas.

Sampling check:
Sampling error decreased when observed tokens increased from 4,096 to 32,768, so the main effect is not explained by finite-token load noise.

Interpretation:
Row-norm variation should be treated as a separable initialization imbalance term in this gate-only decomposition.

Boundary:
The evidence is causal for the tested gate-only intervention, but it does not explain trained MoE collapse, semantic specialization, attention/residual behavior, or final router design.

Evidence links:
`daily_research_reports/0620/results_high/experiment_report.md`
`Projects/from-attention-to-search/main/experiments/A06/A06_03_high_dimensional_gaussian_gate_norm_variation/summary.md`
`Projects/from-attention-to-search/main/experiments/A06/A06_03_high_dimensional_gaussian_gate_norm_variation/detailed.md`

## 8. Claim Boundary And Next Decision

Can claim:
The current evidence supports row-norm variation as a causal contributor to fixed gate-only load imbalance under the tested uniform high-dimensional input setting.

Cannot claim:
This does not explain trained MoE collapse, semantic specialization, route-utility binding, attention/residual dynamics, or a final router method.

Next decision:
Decide whether row-norm variation should become a required diagnostic baseline before interpreting trained-router load imbalance as semantic or data-driven specialization.
