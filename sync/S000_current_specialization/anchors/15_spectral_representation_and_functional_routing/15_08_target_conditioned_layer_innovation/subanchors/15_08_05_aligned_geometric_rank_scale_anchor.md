---
anchor_id: 15_08_05_aligned_geometric_rank_scale
status: EXECUTED_AWAITING_HUMAN_JUDGMENT
thinking_card: 15_08_05_aligned_geometric_rank_scale_thinking_card_cn.md
parent_anchor: ../15_08_target_conditioned_layer_innovation_anchor.md
depends_on: 15_08_04_transition_object_spectrum_sensitivity_anchor.md
created: 2026-08-18
updated: 2026-08-18
---

# A15_08_05: Does the apparent rank gap survive model, token, and metric alignment?

## 1. Problem Definition

The parent line distinguishes geometric concentration from target-conditioned added accessibility. A15_08_04 measured eight named Qwen3-8B objects on 2,048 tokens and emphasized $r_{80}$, whereas the meeting's ZX and CAR analyses used Qwen3-0.6B, approximately one million tokens, and $r_{90}$. The one decision question is:

> On one frozen Qwen3-0.6B, one shared evaluation population, and one centered-covariance $r_{90}$ estimator, do CAR-style whole-block transitions, ZX-style 500-dimensional projected Attention transitions, and our linearly residualized normalized update $R_U$ retain materially different rank profiles?

This is a scale and operationalization audit. It does not test clustering, semantics, causal use, or Router utility.

## 2. Physical Prior

Covariance rank belongs to a named random vector and sampling population. Increasing tokens can remove the sample-rank cap, while projection, differencing, normalization, and linear residualization can change the spectrum. If aligned CAR, ZX, and $R_U$ have nearly identical normalized $r_{90}$ trajectories, this prior is weakened for the present objects.

## 3. Falsifiable Hypotheses

**H-OBJECT:** after token-count convergence, both CAR and ZX differ from the matched destination-layer $R_U$ median normalized $r_{90}$ by at least 0.10. The sign is reported rather than assumed.

**R-NO-GAP:** both absolute differences are below 0.03 after convergence. Intermediate or non-converged outcomes are `MIXED_OR_INSUFFICIENT`.

The model-size explanation is controlled, not separately estimated: all three objects are extracted from the same Qwen3-0.6B forward passes.

## 4. Mathematical Model

For block $l$, let $h_l$ be its raw input residual, $a_l$ its Attention `o_proj` write, $N_l$ its post-Attention RMSNorm, and $H_l$ its complete block output. Define

$$
X_l=N_l(h_l),\qquad U_l=N_l(h_l+a_l)-N_l(h_l).
$$

Fit an affine ridge predictor on TRAIN only and choose its dimensionless ridge multiplier on DEVELOPMENT only:

$$
R_{U,l}=U_l-\widehat{\mathbb E}_{lin}[U_l\mid X_l].
$$

The three evaluated objects are

$$
D^{CAR}_l=H_{l+1}-H_l,
$$

$$
D^{ZX}_l=Q_{500}^{\top}(a_{l+1}-a_l),
$$

and $R_{U,l}$. $Q_{500}$ contains the top 500 PCA directions of the TRAIN final-block state, matching the recorded ZX last-layer-reference construction without using evaluation tokens.

For any centered evaluation matrix with covariance eigenvalue shares $p_1\ge\cdots\ge p_d$,

$$
r_{90}=\min\left\{r:\sum_{j\le r}p_j\ge0.9\right\}.
$$

The primary comparable unit is $r_{90}/d_{object}$; absolute $r_{90}$ and the full cumulative spectrum are retained.

## 5. Computational Realization

Use local Qwen3-0.6B, fixed non-overlapping DCLM token partitions, and sequence length 2,048. TRAIN and DEVELOPMENT each contain 131,072 tokens; EVALUATION contains 1,048,576 tokens. Activations are not materialized at full scale: numerically stable batch-centered covariance and cross-covariance sufficient statistics are streamed. Evaluation snapshots are taken at nested token counts 2,048, 8,192, 32,768, 131,072, 524,288, and 1,048,576.

## 6. Minimal Falsification Test

All three objects share model, evaluation tokens, layer hooks, centering, eigensolver, and $r_{90}$ rule. CAR and ZX transitions at target blocks 2--28 are paired with $R_U$ at blocks 2--28. A method is converged when its full-run layer-median $r_{90}/d$ differs from the 524,288-token snapshot by at most 0.02. The H-OBJECT and R-NO-GAP thresholds are applied only after all methods converge and all identity, finite-spectrum, coverage, and token-count guards pass.

## 7. Current Evidence

The aligned run completed on 1,048,576 Qwen3-0.6B EVALUATION tokens. Median normalized $r_{90}$ changed by only 0.00488, 0.00400, and 0.00244 from the 524,288-token snapshot for CAR, ZX, and $R_U$, respectively. Full-run layer medians were CAR $576/1024=0.5625$, ZX $297/500=0.594$, and $R_U$ $445.5/1024=0.4351$. Paired median gaps were CAR-minus-$R_U=+0.1377$ and ZX-minus-$R_U=+0.1498$, satisfying the registered `METHOD_OBJECT_GAP` rule.

CAR target block 3 was a local singular exception: $r_{90}=1$ and the leading direction contained 99.88% of variance. Excluding sequence position 0 left $r_{90}=1$ and a 90.95% leading share, so boundaries amplify but do not explain the anomaly. The CAR layer median remained 576 versus 575 after this exclusion, leaving the broad-rank result intact.

## 8. Claim Boundary And Next Decision

An eligible result can identify whether the observed geometric-rank gap survives the aligned operationalization and which definition produces it. It cannot call any covariance direction semantic new information, establish functional sufficiency, infer nonlinear novelty, or justify routing.

The evidence supports a stable method/object gap and shows that million-token CAR/ZX transitions are broad-rank, while $R_U$ is narrower but still requires hundreds of directions. The next decision is a closed-book researcher judgment on whether to freeze $R_U$ for a separate functional-rank test. No geometric spectrum establishes semantic novelty or Router utility.
