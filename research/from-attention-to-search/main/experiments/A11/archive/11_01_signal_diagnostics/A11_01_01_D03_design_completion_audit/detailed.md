# Detailed Results: A11_02b Advisor K=2 Design Completion Audit

## 1. Decision And Run Integrity

**Decision:** the controlled K=2 useful-signal claim survives the complete advisor diagnostic suite. Shared-gradient conflict has a measurable but small local $L_1$ convergence cost; it does not cause final next-token failure. Refinement difficulty and strong hidden-to-parameter rotation are not supported as explanations of that conflict.

Final evidence run:

| Item | Value |
|---|---|
| ACP job | `pt-27zjtage` |
| platform state | `SUCCEEDED` |
| worker | one `n6ls.iu.i40.4` node, 4 GPUs |
| run name | `a11_02b_advisor_design_completion_4gpu_20260710_034038` |
| tasks | 240/240 |
| shards | 60/60/60/60 |
| seeds per condition | 5/5 |
| objective scopes | 120 decision-only + 120 all-position |

Two earlier submissions are not evidence. `pt-4ck5dan0` was stopped after the first implementation audit found that refinement buckets lacked branch-readout accuracy. `pt-jjj0r6zt` was stopped before execution after the second audit found that $D_t/G_t$ were final-only and could not test dynamics. Both omissions were fixed and smoke-tested before the final job.

## 2. Data Construction And Information Condition

Let $B\in\{1,2,3,4\}$ be the early branch token. Every sequence then contains 16 filler tokens and four shared local-context tokens before decision state $h_T$.

| Regime | Future targets | Conditional branch information |
|---|---|---|
| A-clean | $Y_1=U,\;Y_2=S_B$ | $I(B;Y_2\mid Y_1)=H(B)=2$ bits |
| B-redundant | $Y_1=S_B,\;Y_2=T_B$ | $I(B;Y_2\mid Y_1)=0$ because $Y_1$ already identifies $B$ |
| C-noisy | $Y_1=U,\;Y_2=N,\;N\perp B$ | $I(B;Y_2\mid Y_1)=0$ |

The training objectives are:

$$
L_{\mathrm{NTP}}=L_1,
\qquad
L_{K=2}=L_1+\lambda L_2.
$$

`decision_only` applies these losses only at $h_T$. `all_positions_lm_control` averages offset-1 and offset-2 losses over every valid sequence position.

## 3. Metric Definitions And What Each Decides

### 3.1 Native prediction and representation

**Head-2 accuracy** is the top-1 accuracy of $p^{(2)}(Y_2\mid h_T)$. It asks whether the model itself can use $h_T$ to predict the informative future token. It does not prove that the branch token caused the prediction.

**Two-token exact match** is:

$$
\mathbf 1[\hat Y_1=Y_1\;\land\;\hat Y_2=Y_2].
$$

It is the exact suffix success rate. In A-clean, because $Y_1$ is shared, it is numerically governed by head-2 success.

**Frozen branch probe** fits $S_\phi(h_T)\to B$ on a held-out training batch and reports accuracy and cross-entropy on an independent evaluation batch. It asks whether branch identity is linearly readable. It cannot establish use by the model's own prediction head.

**Branch-swap consistency** replaces the early branch token with $B'$ while preserving the remaining prefix and asks whether head 2 prefers $S_{B'}$ over $S_B$:

$$
\operatorname{Swap}=
\mathbb E\,\mathbf 1[ell_2(S_{B'})>\ell_2(S_B)].
$$

It guards against a fixed suffix or sample-identity shortcut. It is undefined for C-noisy because there is no branch-specific target to swap.

**Representation separation** measures branch-center distance:

$$
\Delta_h=\mathbb E_{b\ne b'}\|\mu_b-\mu_{b'}\|_2^2.
$$

It measures scale-dependent separation, not calibrated usability across architectures.

### 3.2 Duplicate-target refinement

The same $Y_2$ is predicted by head 2 before seeing $Y_1$ and by head 1 one position later. Their distribution discrepancy is:

$$
D_t=\operatorname{KL}\left(
p^{(1)}(\cdot\mid x_{\le t+1})\,\|\,
p^{(2)}(\cdot\mid x_{\le t})
\right).
$$

Target-specific log-probability change is:

$$
G_t=-\log p^{(2)}(Y_2\mid x_{\le t})
+\log p^{(1)}(Y_2\mid x_{\le t+1})
=\log\frac{p^{(1)}(Y_2\mid x_{\le t+1})}{p^{(2)}(Y_2\mid x_{\le t})}.
$$

$G_t>0$ means the revealed $Y_1$ makes the true $Y_2$ more probable; $G_t<0$ means the later head-1 forecast is worse. Its sign is meaningful only when both prediction sites are trained. Therefore decision-only final $G_t$ cannot be interpreted as intrinsic refinement difficulty.

### 3.3 Gradient geometry and usefulness

For $g_j=\nabla_{\theta_s}L_j$ on the same shared parameter group:

$$
c_s=\frac{\langle g_1,g_2\rangle}{\|g_1\|\|g_2\|},
\qquad
r=\frac{\|g_2\|}{\|g_1\|},
$$

$$
\rho=\frac{\langle g_1+\lambda g_2,g_1\rangle}{\|g_1\|^2}
=1+\lambda\frac{\langle g_1,g_2\rangle}{\|g_1\|^2}.
$$

$c_s<0$ means local directional conflict. $\rho<0$ means the combined first-order update reverses the $L_1$ gradient direction on that parameter group. Neither quantity proves realized damage when gradient norms are tiny.

At the shared decision activation:

$$
c_h=\frac{\langle\nabla_{h_T}L_1,\nabla_{h_T}L_2\rangle}
{\|\nabla_{h_T}L_1\|\|\nabla_{h_T}L_2\|}.
$$

Comparing $c_h$ and $c_s$ tests whether the trunk Jacobian materially rotates horizon gradients. A comparison is invalid when either norm has nearly vanished.

For a detached frozen readout $R_\phi=\operatorname{CE}(S_\phi(h_T),B)$:

$$
U_2=\langle\nabla_{\theta_s}R_\phi,g_2\rangle.
$$

Under gradient descent by $-g_2$, $U_2>0$ predicts a first-order decrease in readout loss. This is a one-step directional diagnostic, not proof of long-run sample efficiency.

### 3.4 Realized local learning cost

Normalized loss area is:

$$
\operatorname{AUC}_{L_1}=\frac{1}{T}\int_0^T L_1(t)\,dt.
$$

Larger AUC means slower next-token cross-entropy convergence. Final accuracy and AUC answer different questions: accuracy may already be saturated while confidence is still converging.

## 4. Result 1: Useful Signal Survives Every Guard

All-position, both initializations combined (`n=10`):

| Regime / model | $Y_1$ acc | head-2 acc | probe | swap | $L_2$ |
|---|---:|---:|---:|---:|---:|
| A / NTP | 1.000 | NA | 0.825 | NA | NA |
| A / shared K=2 | 1.000 | 1.000 | 1.000 | 1.000 | $2.21\times10^{-5}$ |
| A / separate expert | 1.000 | 0.975 | 0.975 | 0.975 | 0.0347 |
| A / fully separated | 1.000 | 1.000 | 1.000 | 1.000 | $1.55\times10^{-5}$ |
| B / shared K=2 | 1.000 | 1.000 | 1.000 | 1.000 | $1.64\times10^{-5}$ |
| C / shared K=2 | 1.000 | 0.0656 | 0.875 | NA | 2.777 |

The C-noisy chance level is $1/16=0.0625$. The high C probe is therefore a false positive for direct second-token supervision. A-clean passes the stricter native-head and branch-swap guards.

Decision-only A-clean is less stable: shared trunk averages `0.775` head-2 accuracy with `6/10` runs at or above `0.9`; separate expert averages `0.900` (`7/10`), and fully separated averages `0.900` (`8/10`). The paired mean improvements over shared trunk are both `+0.125`, but their 95% intervals are `[-0.086,0.336]` and `[-0.204,0.454]`. This is suggestive stabilization, not a resolved method advantage.

## 5. Result 2: Task-Directed $L_2$ Gradient Is Specific To A-Clean

All-position final shared-trunk results, both initializations combined:

| Regime | mean $U_2$ | positive seeds/runs | cosine$(\nabla R_\phi,g_2)$ | mean $\|g_2\|$ |
|---|---:|---:|---:|---:|
| A-clean | $1.166\times10^{-3}$ | 10/10 | 0.983 | $6.57\times10^{-4}$ |
| B-redundant | $-3.57\times10^{-6}$ | 3/10 | -0.047 | $9.34\times10^{-5}$ |
| C-noisy | $-1.02\times10^{-3}$ | 5/10 | -0.028 | $7.08\times10^{-2}$ |

A-clean's final direction is consistently aligned with reducing branch-readout loss. C-noisy has a much larger unresolved $g_2$ norm but no consistent branch direction. At step 0, random initialization has high variance and tied-branch initialization gives exactly zero readout gradient by symmetry. Therefore the experiment does not establish that the useful direction exists before representation symmetry breaks.

## 6. Result 3: Conflict Emerges During Training And Has A Small Local Cost

All-position A-clean shared trunk, $\lambda=1$, both initializations and five seeds:

| Step | group | $c_s$ | $\rho$ | $\|g_1\|$ | $\|g_2\|$ |
|---:|---|---:|---:|---:|---:|
| 0 | embedding | 0.016 | 1.017 | 0.166 | 0.172 |
| 0 | attention | 0.004 | 1.005 | 0.369 | 0.387 |
| 200 | embedding | -0.889 | -0.130 | 0.00128 | 0.00213 |
| 200 | attention | -0.894 | -0.157 | 0.00476 | 0.00831 |
| 4000 | embedding | approximately -0.999 | near 0 | approximately $10^{-5}$ | approximately $10^{-5}$ |
| 4000 | attention | approximately -1.000 | near 0 | approximately $4\times10^{-5}$ | approximately $4\times10^{-5}$ |

The conflict is not present at initialization. It becomes strong by step 200, when structured $L_1$ is already below `0.01`, and becomes numerically extreme as both gradients vanish. This explains why an average cosine near `-0.94` can coexist with perfect final $Y_1$ accuracy.

The matched lambda audit nevertheless finds a small realized cost:

| $\lambda$ | $L_1$ AUC increase vs NTP | runs with increase | final $Y_1$ | final head-2 |
|---:|---:|---:|---:|---:|
| 0.25 | 0.589% | 10/10 | 1.000 | 1.000 |
| 0.50 | 0.835% | 10/10 | 1.000 | 1.000 |
| 1.00 | 1.071% | 10/10 | 1.000 | 1.000 |

At step 100, mean structured $L_1$ is `0.00547` for NTP and `0.01745` for $\lambda=1$ K=2, while both already have $Y_1$ accuracy `1.00`. The supported interpretation is slower confidence convergence, not an accuracy tradeoff.

## 7. Result 4: Refinement Metrics Do Not Explain The Conflict

All-position shared-trunk dynamics:

| Regime | $D_0$ | $D_{4000}$ | $G_0$ | $G_{4000}$ | early/final head-2 target probability |
|---|---:|---:|---:|---:|---:|
| A | 0.318 | $1.07\times10^{-5}$ | -0.162 | approximately 0 | 0.0211 / 1.0000 |
| B | 0.317 | $2.27\times10^{-5}$ | -0.0436 | approximately 0 | 0.0167 / 1.0000 |
| C | 0.318 | $4.15\times10^{-4}$ | 0.0624 | approximately 0 | 0.0206 / 0.0628 |

The two forecasts become distributionally consistent under all-position training. However, low/medium/high $G_t$ buckets do not show a monotonic relation with $c_s$, $r$, or branch readability. A and B each have only four distinct $G_t$ values per seed because samples are repeated within branch. The bucket test is therefore too coarse to establish a general difficulty law.

Under decision-only training, the head-1 prediction at $t+1$ is not optimized. Final A-clean $D_t$ grows to about `16` and $G_t$ becomes strongly negative even when head 2 succeeds. This is an objective-scope artifact and must not be interpreted as the intermediate token making prediction harder.

## 8. Result 5: Hidden-To-Parameter Rotation Is Not Established

For all-position A-clean shared K=2:

| Step | $c_h$ | $\|\nabla_hL_1\|$ | $\|\nabla_hL_2\|$ |
|---:|---:|---:|---:|
| 0 | -0.0058 | 0.0725 | 0.0713 |
| 4000 | 0.0565 | $4\times10^{-6}$ | $5\times10^{-6}$ |

At step 0, both hidden and parameter cosines are near zero; there is no strong rotation to explain. At final, hidden gradients have nearly vanished, so the cosine is ill-conditioned. The requested metric is implemented, but the hypothesis remains insufficiently supported.

## 9. Result 6: Separation Localizes Sharing But Does Not Establish A Better Method

The structural audit passes:

- Separate-expert model: $g_2=0$ on expert 1 and $g_1=0$ on expert 2; embedding and attention remain shared.
- Fully separated model: $g_2=0$ on horizon-1 trunk and $g_1=0$ on horizon-2 trunk; no cross-horizon shared trunk remains.
- All-position A-clean: shared and fully separated models both reach head-2/probe/swap `1.00`.

Thus separation removes the intended gradient interaction by construction. The data do not show that this removal is needed in the all-position setting, and decision-only gains are not stable enough for a method claim.

## 10. Advisor Clause Coverage

| Advisor clause | Evidence artifact | Judgment |
|---|---|---|
| A/B/C useful, redundant, noisy regimes | `core_outcomes.csv` | completed; useful/noisy contrast supported |
| NTP/shared/separate/full controls | `core_outcomes.csv`, `separation_control.csv` | completed; structural localization supported, method gain insufficient |
| $\lambda=0.25,0.5,1$ | `lambda_local_cost.csv` | completed; small monotonic $L_1$ cost |
| global and structured $L_1/L_2$ | raw `training_history.csv` | completed |
| head-1/head-2/joint/exact/swap | raw `per_seed_metrics.csv`, `branch_swap.csv` | completed |
| $D_t/G_t$ dynamics | `refinement_dynamics.csv` | completed; explanatory hypothesis weakened |
| $c_h,c_s,r,\rho$ | raw and `gradient_timeline.csv` | completed; conflict timed, rotation insufficient |
| branch probe at four positions | raw `probe_by_position.csv` | completed |
| $\Delta_h$ | raw `representation_separation.csv` | completed; scale-dependent representation evidence |
| $U_2$ | `usefulness_summary.csv` | completed; final A-clean specificity supported |
| low/medium/high $G_t$ buckets | raw `refinement_bucket_metrics.csv` | completed; nonmonotonic/coarse support |

## 11. Visualization Results

![A11_02b core signal and interference](figures/a11_02b_core_signal_and_interference.png)

**Plot contract**

- Question: separate useful branch signal from noisy readability, and compare gradient conflict with realized $L_1$ cost.
- Metrics: head-2/probe/swap rates; paired normalized $L_1$ AUC increase; shared-parameter $c_s$; cosine between $g_2$ and frozen-readout gradient.
- Data source: final 240-task run, aggregated over five seeds and both initializations where shown.
- Axes: rates and cosines are unitless; AUC difference is percent relative to matched NTP; training step is optimizer step.
- Allowed conclusion: useful A-clean signal coexists with small dose-dependent local slowdown and late negative cosine.
- Limitation: C-noisy swap is undefined; no confidence intervals are displayed in the compact figure; exact uncertainty is in tables and text.

**Rendered-artifact audit:** PNG renders successfully at `2160x1530`; titles, axes, legends, category labels, and zero lines are readable. The plot requires metric definitions above, not source-code knowledge. No panel is used to claim natural-language or general MTP performance.

## 12. Claim Boundary And Next Decision

Supported:

- controlled K=2 branch-informative supervision is model-usable;
- the final $L_2$ direction is branch-directed only in the informative regime;
- shared conflict emerges during optimization and is associated with a small lambda-dependent $L_1$ CE slowdown;
- final local accuracy is preserved;
- separation removes interaction only where sharing is removed.

Not supported:

- general MTP efficiency over NTP;
- harmful conflict inferred from cosine alone;
- refinement gain as the cause of conflict;
- strong hidden-to-parameter rotation;
- a general benefit from expert separation.

**Next decision:** close A11_02b. A theoretical continuation should derive a finite-step decomposition of branch-margin gain versus integrated $L_1$ cost under $g_1+\lambda g_2$, using this run as evidence rather than opening a broader ablation.

## 13. Artifact Map And Reproduction

- Code workspace: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`
- Runner: `active/synthetic_data_understanding/scripts/run_a11_02b_advisor_design_completion.py`
- Analyzer: `active/synthetic_data_understanding/scripts/analyze_a11_02b_advisor_design_completion.py`
- Config: `active/synthetic_data_understanding/configs/a11_02b_advisor_design_completion_audit.json`
- Submitter: `active/synthetic_data_understanding/scripts/submit_a11_02b_advisor_design_completion_4gpu.sh`
- Raw result dir: `active/synthetic_data_understanding/results/a11_02b_advisor_design_completion_audit/a11_02b_advisor_design_completion_4gpu_20260710_034038`
- Remote logs: `active/synthetic_data_understanding/logs/acp/a11_02b_advisor_design_completion_4gpu_20260710_034038`
- Curated tables: `Projects/from-attention-to-search/main/experiments/A11/A11_02b_advisor_design_completion_audit/tables/`
- Figure: `Projects/from-attention-to-search/main/experiments/A11/A11_02b_advisor_design_completion_audit/figures/a11_02b_core_signal_and_interference.png`
- Reproduction command: `A11_ALLOW_REAL_SUBMIT=1 bash scripts/submit_a11_02b_advisor_design_completion_4gpu.sh`
