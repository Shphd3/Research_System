# A11_16 Pretrained Shared-Gradient Transmission: Detailed Evidence

## 0. Result

Status: **missing or signed transmission supported**. The extra H2 gradient has positive held-out common-H1 usefulness at initialization in `1/5` seeds and positive NTP-path `0-200` usefulness AUC in `1/5`. This validly explains why A11_15 can fit H2 without a stable common-H1 advantage.

## 1. Definitions And Mathematical Decision

The standard H1 evaluation margin and shared gradients are:

$$
M_E(\theta)=\frac{1}{|E|}\sum_{i\in E}
[\ell_{1,Y_i}(X_i;\theta)-\ell_{1,\bar Y_i}(X_i;\theta)],
$$

$$
r_E^S=\nabla_{\theta_S}M_E,
\quad
g_D^S=\nabla_{\theta_S}L_D,
\quad
g_N^S=\nabla_{\theta_S}(L_S+L_I).
$$

Task-directed usefulness is:

$$
U_D^E=-\langle r_E^S,g_D^S\rangle,
\qquad
U_N^E=-\langle r_E^S,g_N^S\rangle,
$$

$$
U_M^E=U_N^E+U_D^E.
$$

The normalized primary metric $\widehat U_D^E$ is the signed cosine between the evaluation-margin ascent direction and the H2-loss descent direction. The separate cosine $\cos(g_N,g_D)$ only measures mutual training-gradient alignment and cannot determine whether either gradient helps the task.

## 2. Protocol Compliance

- final remote job: `pt-rmyzkcq2`, succeeded;
- 10/10 tasks, five diagnostic checkpoints per task;
- 50 gradient-transmission rows, 300 layer-group rows, 50 task-curve rows;
- seeds `971-975`, NTP and MTP trajectories;
- identical model, tokenizer, samples, schedule, optimizer, and processed tokens within each pair;
- diagnostic batches contain every domain-state pair, labels `5/5`, paraphrase IDs `5/5`, option order `6/4` (closest feasible under the state-option label relation);
- all float values finite; copied H2 guard, diagnostic balance, parameter restore hashes, and checkpoint coverage pass;
- step-0 $Q=0$ reproduces exactly; maximum condition-checkpoint mean difference from A11_15 is `0.0475`.

## 3. Numerical Derivative Audit

The diagnostic uses float32 central differences:

$$
\Delta_{central}
=\frac{M_E(\theta-\delta g_D)-M_E(\theta+\delta g_D)}{2},
$$

with $\delta\|g_D\|=10^{-6}\|\theta_S\|$. The first-order prediction is $\delta U_D^E$.

| Seed | Predicted | Central measured | Relative error | Sign match | Guard pass |
|---:|---:|---:|---:|---:|---:|
| 971 | -0.004151 | -0.002398 | 0.422 | yes | yes |
| 972 | 0.000523 | 0.000062 | 0.882 | yes | no |
| 973 | -0.006127 | -0.003489 | 0.431 | yes | yes |
| 974 | -0.004292 | -0.002533 | 0.410 | yes | yes |
| 975 | -0.001948 | -0.001000 | 0.487 | yes | yes |

All signs match; `4/5` also satisfy the `0.50` magnitude tolerance. Seed 972 has the smallest predicted change and the largest relative numerical error. The derivative decision is therefore valid under the preregistered rule.

Two pre-final smoke attempts are retained as implementation evidence. A one-sided `1e-5` perturbation was curvature dominated. A central `1e-5` perturbation restored the sign but remained too nonlinear. These failures changed only the finite-difference implementation radius, not the target derivative or training run.

## 4. Primary Trajectory Results

| Seed | Step-0 $\widehat U_D^E$ | NTP AUC `0-200` | MTP AUC `0-200` | NTP final | MTP final |
|---:|---:|---:|---:|---:|---:|
| 971 | -0.0569 | -0.0134 | -0.0045 | -0.0948 | 0.1301 |
| 972 | 0.0092 | 0.0144 | 0.0815 | -0.2217 | 0.0314 |
| 973 | -0.0721 | -0.0831 | -0.0650 | -0.1076 | 0.3091 |
| 974 | -0.0614 | -0.0759 | 0.1058 | -0.2687 | 0.1436 |
| 975 | -0.0259 | -0.1509 | 0.0591 | -0.1753 | -0.0124 |

At the shared step-0 initialization, four seeds are negative. Along the NTP path, only seed 972 has positive usefulness AUC. At steps 200 and 300, all NTP seeds are negative. The MTP path changes the geometry and becomes more positive late, but it is not uniformly positive and does not retrospectively establish learning efficiency.

## 5. Gradient Routing Versus Direction

The H2-loss shared squared-norm fraction is:

$$
R_{shared}=\frac{\|g_D^S\|^2}
{\|g_D^S\|^2+\|g_D^{H2}\|^2}.
$$

At step 0, mean $R_{shared}=0.9213`. Across NTP checkpoints, the per-seed mean ranges `0.9405-0.9544`; across MTP checkpoints it ranges `0.8762-0.9254`.

Thus most H2 gradient norm is already on shared parameters. The missing downstream benefit is not explained by a vanishing shared path. The shared path has the wrong or unstable task direction.

## 6. Layer Decomposition

Mean step-0 $U_D^E$ contributions on the NTP path:

| Parameter group | Contribution |
|---|---:|
| layers 0-6 | -166.0 |
| layers 7-13 | -190.8 |
| layers 14-20 | -103.3 |
| layers 21-27 | -7.8 |
| tied embedding/interface | 0.4 |
| final norm/other | approximately 0 |

The negative initial direction is distributed through early and middle Transformer layers rather than caused by the tied answer rows. By step 200 on the NTP path, every large layer group is negative. This argues against fixing the interpretation by looking only at output-head cosine.

## 7. Why Gradient Conflict Is Not The Conclusion

At step 0, mean $\cos(g_N,g_D)=-0.0642`, while mean $\widehat U_D^E=-0.0415`. On the MTP path at step 100, mean gradient cosine is strongly negative (`-0.7999`) but mean task usefulness is positive (`0.0431`). Therefore a negative gradient cosine can coexist with positive downstream usefulness, exactly as the earlier claim boundary required.

The correct statement is about $U_D^E$, not whether $g_N$ and $g_D$ conflict.

## 8. Reproduced Task Behavior

The instrumented rerun preserves the A11_15 qualitative behavior:

| Step | NTP mean $Q$ | MTP mean $Q$ | MTP mean H2 accuracy |
|---:|---:|---:|---:|
| 0 | 0.0000 | 0.0000 | 0.4412 |
| 100 | 0.1725 | 0.0700 | 0.4838 |
| 200 | 0.7100 | 0.5875 | 0.7575 |
| 300 | 0.7975 | 0.8350 | 0.8962 |

Neither condition reaches the preregistered sustained threshold. The final mean reversal relative to A11_15 is within cross-job seed variability and cannot be used as an efficiency claim.

## 9. Visualization Results

### Plot Contract

**Question:** is the H2 gradient locally useful for the held-out standard-H1 semantic boundary?  
**Data:** five paired seeds at five checkpoints.  
**Upper left:** mean and seed range of normalized usefulness; positive is helpful.  
**Upper right:** predicted versus central finite-difference margin change.  
**Lower left:** shared versus private H2-gradient squared norm.  
**Lower right:** reproduced task curve.  
**Allowed conclusion:** local direction, routing volume, and trajectory dependence.  
**Limitation:** train/evaluation wording and H2/H1 interface changes are still combined.

![A11_16 shared-gradient transmission](figures/a11_16_pretrained_shared_gradient_transmission.png)

## 10. Theoretical Consequence

The earlier representation result remains valid: an informative covered future target can force the current hidden state to encode the branch variable under its prediction head. A downstream efficiency claim needs an additional interface-transfer condition.

For paired one-step SGD updates from the same point:

$$
M(\theta-\eta(g_N+g_D))-M(\theta-\eta g_N)
=\eta U_{D\rightarrow M}+O(\eta^2),
$$

where

$$
U_{D\rightarrow M}=-\langle\nabla M,g_D\rangle.
$$

Coverage answers whether a direct semantic signal exists. $U_{D\rightarrow M}$ answers whether that signal helps the interface and data distribution used by the downstream task. These are distinct conditions.

## 11. Claim Boundary

**Observation:** stable positive $U_D^E$ is absent on the NTP path.  
**Interpretation:** shared gradient volume is large, but its held-out common-H1 direction is mostly adverse.  
**Claim:** missing/signed cross-interface transmission can explain A11_15's private-H2/common-H1 mismatch.  
**Cannot claim:** MTP is globally harmful, raw gradients determine AdamW's full trajectory, pure MTP pretraining has the same sign, or external tasks will behave identically.

## 12. Artifact Map

Raw result:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
results/a11_16_pretrained_shared_gradient_transmission/
a11_16_pretrained_shared_gradient_transmission_central_4gpu_20260710_190500
```

Logs:

```text
.../logs/acp/a11_16_pretrained_shared_gradient_transmission_central_4gpu_20260710_190500
```

Code:

```text
configs/a11_16_pretrained_shared_gradient_transmission.json
scripts/run_a11_16_pretrained_shared_gradient_transmission.py
scripts/analyze_a11_16_pretrained_shared_gradient_transmission.py
scripts/submit_a11_16_pretrained_shared_gradient_transmission_4gpu.sh
```

Canonical evidence:

- [summary](summary.md)
- [trajectory usefulness](tables/trajectory_usefulness.csv)
- [finite differences](tables/finite_difference.csv)
- [decision](hypothesis_decision.json)
- [central figure](figures/a11_16_pretrained_shared_gradient_transmission.png)

## 13. Next Decision

Decompose usefulness into a fixed 2-by-2 table: H2 versus common H1 interface, crossed with seen versus unseen paraphrases. This is the smallest test that distinguishes interface/location transmission failure from semantic generalization failure.
