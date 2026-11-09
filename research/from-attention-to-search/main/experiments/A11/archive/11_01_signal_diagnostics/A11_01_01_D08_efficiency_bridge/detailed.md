# Detailed: A11_05 Semantic Efficiency Bridge

Primary anchor: `problem_anchors/11_informative_future_branch_mechanism/11_05_semantic_efficiency_bridge_anchor.md`
Protocol: `protocol.md`
Summary: `summary.md`

## 0. Quick Recap

Purpose: decompose whether K=3's clean $\tau=3$ all-position semantic-efficiency advantage comes from direct decision-prefix horizon-3 supervision.

Hypothesis: if direct supervision is the mechanism, then adding only $\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$ to K=2 should improve recovery, and masking that term from K=3 should weaken recovery.

Experiment logic: run five clean all-position conditions under identical-branch and random initialization: K1, K2, K3 full, K3 without decision-prefix L3, and K2 plus decision-prefix L3.

Conclusion: direct supervision is supported as a measurable mechanism component. It is sufficient to make K2 match full K3 under identical-branch initialization, and removing it weakens K3. However all-position indirect transfer remains strong, and random initialization saturates $Q$ at step 0.

Evidence: 50/50 training runs completed; 3050 curve rows; 50 seed summaries; 10 condition summaries; ACP job `pt-u0od5jmz` succeeded.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| $Z$ | branch variable present in the prefix | branch label from `BR_Z` | class label | target long-horizon information | natural-language semantics |
| $h_T$ | current decision-prefix hidden state | hidden state after `BR_Z,F_1,\ldots,F_L,U` | vector | object being audited | future-state behavior |
| clean $\tau=3$ | first informative target is 3 steps ahead | $Y_1=A$, $Y_2=C$, $Y_3=S_Z$ | token offset | defines coverage by K | real LM horizon |
| K | active next-token horizon count | condition controls which heads receive loss | integer | intervention variable | capacity alone |
| direct L3 | decision-prefix horizon-3 loss | $\lambda_3\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)$ | CE | proposed mechanism | all MTP benefit |
| indirect transfer | branch recovery through other all-position losses | shared parameter effects excluding direct L3 at $h_T$ | effect | main rival explanation | direct causality |
| $A(t)$ | informative-suffix decoder accuracy | linear decoder from frozen $h_T$ to $Z$ | accuracy | detects branch information in $h_T$ | native prediction |
| $P(t)$ | independent probe accuracy | separate linear probe from frozen $h_T$ to $Z$ | accuracy | guard against one decoder artifact | causal route |
| $S(t)$ | branch-swap consistency | swap branch token and decode swapped branch | accuracy | tests whether readout follows branch identity | natural semantics |
| $Q(t)$ | guarded semantic recovery | $Q(t)=\min\{A(t),P(t),S(t)\}$ | score in $[0,1]$ | primary recovery metric | exact mechanism |
| $T_{0.9}$ | reliable time-to-threshold | first step with $Q\ge0.9$ for 3 consecutive evals | steps | primary speed metric | final convergence |
| early AUC | early recovery area | normalized trapezoid AUC of $Q$ over 0-3000 | score area | early speed/stability | gradient cause |
| full AUC | whole-run recovery area | normalized trapezoid AUC of $Q$ over 0-15000 | score area | full-run stability | direct mechanism |
| local CE / accuracy | local next-token learning | native prediction for $Y_1,Y_2$ at $h_T$ | CE / accuracy | rules out local tradeoff | full LM quality |
| native H3 accuracy | direct head prediction of $S_Z$ | $\arg\max q_3(\cdot\mid h_T)=S_Z$ | accuracy | distinguishes direct prediction from probe-readable recovery | downstream utility |
| gradient diagnostics | horizon-gradient compatibility | cosine, norm ratio, future $\Delta Q$ correlations | diagnostic | optimization audit | causal theorem |

## 2. Anchor Link And Decision Point

Anchor question: does direct decision-prefix horizon-3 supervision explain K=3 semantic efficiency beyond all-position indirect transfer and local-loss tradeoff?

Protocol role: mechanism decomposition at fixed clean $\tau=3$.

Primary falsifier: if K2 plus decision L3 fails to improve over K2, and K3 no decision L3 matches K3 full, then direct supervision is not the measured efficiency cause.

## 3. Protocol Compliance Audit

| Item | Expected | Observed | Status |
| --- | --- | --- | --- |
| data regime | clean $\tau=3$ only | `clean_tau3` only | pass |
| objective | all-position LM-style only | `all_positions_lm_control` only | pass |
| conditions | K1, K2, K3 full, K3 no decision L3, K2 plus decision L3 | all five present | pass |
| seeds | 971-975 | all five present | pass |
| initializations | identical-branch and random | both present | pass |
| training runs | 5 conditions × 2 init × 5 seeds = 50 | 50 seed summaries | pass |
| primary metric | $Q(t)$ and $T_{0.9}$ with 3 consecutive evals | recorded | pass |
| local guard | $Y_1/Y_2$ CE and accuracy | recorded | pass |
| learning curve csv | `curve_metrics.csv` | 3050 rows | pass |
| summary table | `condition_summary.csv` | 10 rows | pass |
| gradient diagnostics | optional | recorded, diagnostic only | pass with boundary |

## 4. Setup

Data construction:

$$
X=(\operatorname{BR}_Z,F_1,\ldots,F_L,U,A,C,S_Z).
$$

Decision state:

$$
h_T=f_\theta(\operatorname{BR}_Z,F_1,\ldots,F_L,U).
$$

Targets:

$$
Y_1=A,\qquad Y_2=C,\qquad Y_3=S_Z.
$$

Information structure:

$$
I(Z;Y_1)=0,\qquad I(Z;Y_2\mid Y_1)=0,\qquad I(Z;Y_3\mid Y_1,Y_2)=H(Z).
$$

Model: one-layer causal Transformer with shared trunk and up to 3 prediction heads.

Training: 15000 steps, learning rate 0.003, AdamW, weight decay 0.0, eval every 250 steps, early AUC window 3000, $T_{0.9}$ requires 3 consecutive evals.

Conditions:

| Condition | Loss structure | Mechanism tested |
| --- | --- | --- |
| K1 | all-position $L_1$ | NTP-style baseline and indirect-transfer boundary |
| K2 | all-position $L_1+L_2$ | non-covering MTP baseline |
| K3 full | all-position $L_1+L_2+L_3$ | direct plus indirect K=3 |
| K3 no decision L3 | all-position K=3 with $L_3(h_T,S_Z)$ masked | indirect transfer without direct decision-prefix supervision |
| K2 plus decision L3 | all-position K=2 plus only $L_3(h_T,S_Z)$ | isolated direct supervision |

Known limitation: random initialization is saturated at step 0 under $Q$, so it cannot decide learning speed. It is reported as a boundary condition.

## 5. Metrics And Decision Rules

Guarded recovery:

$$
Q(t)=\min\{A(t),P(t),S(t)\}.
$$

Reliable threshold:

$$
T_{0.9}=\min\{t_i:Q(t_i),Q(t_{i+1}),Q(t_{i+2})\ge0.9\}.
$$

Early AUC over window $W=3000$:

$$
\operatorname{AUC}_{early}=\frac{1}{W}\int_0^W Q(t)\,dt.
$$

Full AUC:

$$
\operatorname{AUC}_{full}=\frac{1}{15000}\int_0^{15000} Q(t)\,dt.
$$

Local guard:

$$
\operatorname{Acc}_{Y_j}=\Pr[\arg\max q_j(\cdot\mid h_T)=Y_j],
$$

$$
L_{Y_j}=\operatorname{CE}(q_j(\cdot\mid h_T),Y_j).
$$

Native horizon-3 accuracy:

$$
\operatorname{Acc}_{H3}=\Pr[\arg\max q_3(\cdot\mid h_T)=S_Z].
$$

Gradient diagnostics:

$$
c_{13}=\frac{\langle g_1,g_3\rangle}{\|g_1\|\|g_3\|},
$$

$$
r_3=\frac{\|g_3\|}{\|g_1\|},
$$

$$
\rho_3=\frac{\langle g_1+\lambda_3g_3,g_1\rangle}{\|g_1\|^2}.
$$

Decision rules:

- Direct supervision supported if K2 plus decision L3 improves over K2 and K3 no decision L3 weakens relative to K3 full.
- Indirect transfer sufficient if K3 no decision L3 matches K3 full and K2 plus decision L3 does not improve over K2.
- Local tradeoff if $Q$ improves while active $Y_1/Y_2$ CE or accuracy worsens.
- Gradient bridge remains insufficient unless diagnostics are consistent and not saturated by initialization.

## 6. Main Results

### 6.1 Identical-Branch Initialization

Identical-branch is the primary speed setting because all conditions start at $Q=0.25$.

| Condition | Reach rate | Mean $T_{0.9}$ reached-only | Early AUC | Full AUC | Final $Q$ | Final suffix acc | Final probe acc | Final swap | Native H3 acc | Final $Y_1/Y_2$ acc |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| K1 | 0.60 | 250 | 0.838 | 0.834 | 0.85 | 0.90 | 0.85 | 0.90 | NA | 1.00 / 0.00 |
| K2 | 0.60 | 333 | 0.771 | 0.731 | 0.85 | 0.85 | 0.90 | 0.85 | NA | 1.00 / 1.00 |
| K3 full | 1.00 | 300 | 0.965 | 0.993 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 / 1.00 |
| K3 no decision L3 | 0.60 | 833 | 0.817 | 0.750 | 0.70 | 0.80 | 0.70 | 0.80 | 0.00 | 1.00 / 1.00 |
| K2 plus decision L3 | 1.00 | 250 | 0.969 | 0.994 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 / 1.00 |

Direct intervention effect:

- K2 plus decision L3 minus K2: reach rate +0.40, early AUC +0.198, full AUC +0.263, final $Q$ +0.15, native H3 accuracy +1.00.
- K3 full minus K3 no decision L3: reach rate +0.40, early AUC +0.148, full AUC +0.243, final $Q$ +0.30, native H3 accuracy +1.00.

Interpretation: direct L3 is both sufficient and measurably important in the clean identical-branch setting.

### 6.2 Random Initialization Boundary

Random initialization starts with $Q=1.0$ for all conditions, so speed metrics are not meaningful. Final results:

| Condition | Reach rate | Mean $T_{0.9}$ reached-only | Early AUC | Full AUC | Final $Q$ | Native H3 acc | Final $Y_1/Y_2$ acc |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| K1 | 0.80 | 0 | 0.956 | 0.935 | 0.95 | NA | 1.00 / 0.00 |
| K2 | 0.80 | 0 | 0.952 | 0.929 | 0.95 | NA | 1.00 / 1.00 |
| K3 full | 1.00 | 0 | 1.000 | 1.000 | 1.00 | 1.00 | 1.00 / 1.00 |
| K3 no decision L3 | 0.80 | 0 | 0.956 | 0.945 | 0.95 | 0.00 | 1.00 / 1.00 |
| K2 plus decision L3 | 1.00 | 0 | 1.000 | 1.000 | 1.00 | 1.00 | 1.00 / 1.00 |

Interpretation: random initialization confirms a boundary. Probe-readable $Q$ can be high without direct native horizon-3 prediction. This prevents using random-init $T_{0.9}$ as learning-speed evidence.

### 6.3 Local-Loss Guard

For active local targets, all K2/K3/intervention conditions reach final $Y_1=1.00$ and $Y_2=1.00$ with near-zero CE. K1 does not train $Y_2$, so its $Y_2$ accuracy 0 and high CE are expected.

Conclusion: direct supervision did not trade off against active local next-token learning.

### 6.4 Gradient Diagnostics

For identical-branch, horizon-3 diagnostics are supportive for K2 plus decision L3 across all-parameters, embedding, shared attention, and shared MLP groups at $\Delta=1000$. K3 full has some supportive signals. K3 no decision L3 also shows supportive diagnostic flags for indirect horizon-3 gradients.

For random initialization, many diagnostics are insufficient or unstable because $Q$ is already saturated at step 0.

Conclusion: gradient diagnostics are consistent with the direct-supervision result in the clean setting, but they do not prove an unconditional optimization theorem.

## 7. Visualization Results

### Identical-Branch Q Curves

![Identical-branch Q curves](figures/q_curves_identical.png)

Purpose: test whether direct decision-prefix L3 changes the learning trajectory from chance-level initialization.

Setup: clean $\tau=3$, all-position training, 5 seeds, identical-branch initialization.

Metric definition: $Q(t)=\min\{A(t),P(t),S(t)\}$.

Metric unit: score in $[0,1]$.

How to read: higher and earlier curves mean faster and more stable recovery of $Z$ from $h_T$.

Expected if supported: K2 plus decision L3 should approach K3 full, and K3 no decision L3 should be weaker than K3 full.

Observed result: K2 plus decision L3 and K3 full rapidly reach and maintain $Q=1.0$; K1/K2/K3 no decision L3 remain less stable.

Take-home: direct decision-prefix L3 explains a measurable part of the efficiency gain.

Remaining uncertainty: indirect transfer still gives nonzero recovery.

### Guarded Recovery Versus Direct Horizon-3 Prediction

![Final Q versus native horizon-3 accuracy](figures/final_q_vs_native_h3.png)

Purpose: distinguish probe-readable $h_T$ recovery from native direct $S_Z$ prediction.

Setup: final-step condition means under both initializations.

Metric definition: final $Q$ and native horizon-3 accuracy.

Observed result: K3 full and K2 plus decision L3 have native H3 accuracy 1.0. K3 no decision L3 has native H3 accuracy 0.0 even when $Q$ is nontrivial or high.

Take-home: all-position indirect transfer can make $h_T$ readable, but direct supervision is needed for the decision-prefix horizon-3 head to predict $S_Z$.

Remaining uncertainty: native H3 accuracy is a head-level diagnostic, not a full downstream usefulness measure.

### Local Next-Token Guard

![Local guard final loss](figures/local_guard_final_loss.png)

Purpose: test whether direct supervision sacrifices local next-token learning.

Setup: final $Y_1/Y_2$ CE across conditions and initializations.

Metric definition: cross entropy of the native local prediction heads at $h_T$.

Observed result: active local targets have near-zero final CE and 1.00 accuracy in K2/K3/intervention conditions.

Take-home: direct supervision is not a local-loss tradeoff in this run.

Remaining uncertainty: this only protects the synthetic local targets, not broad language modeling quality.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Passed / failed / unclear | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| direct add test | K2 plus decision L3 beats K2 under identical-branch | passed | NA | direct L3 is not useless |
| direct mask test | K3 no decision L3 weaker than K3 full under identical-branch | passed | NA | full K3 advantage is not purely indirect |
| indirect transfer test | K1/K2/K3 no decision L3 still recover partly | passed as boundary | all-position shared parameters transfer branch information | exclusivity claim |
| local guard | active $Y_1/Y_2$ accuracy 1.0 | passed | NA | local tradeoff explanation |
| random init audit | step-0 $Q=1.0$ for all conditions | boundary warning | initial branch readability | random-init speed evidence |
| gradient bridge | mixed / saturated outside identical-branch | insufficient | diagnostic not intervention | unconditional gradient usefulness claim |

Remaining rival explanations:

- all-position indirect transfer remains a real contributor;
- the $Q$ metric can be saturated by initialization;
- gradient usefulness needs sharper intervention or harder dynamics.

## 9. Full Experiment Record

Code workspace:

`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

Runner:

`active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py`

Config:

`active/synthetic_data_understanding/configs/a11_05_semantic_efficiency_bridge.json`

Submit script:

`active/synthetic_data_understanding/scripts/submit_a11_05_semantic_efficiency_bridge_4gpu.sh`

Run name:

`a11_05_semantic_efficiency_bridge_4gpu_20260708_100650`

ACP job:

`pt-u0od5jmz`

Resource:

`n6ls.iu.i40.4`, one worker, 4 GPUs.

Raw result directory:

`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_05_semantic_efficiency_bridge/a11_05_semantic_efficiency_bridge_4gpu_20260708_100650`

Log directory:

`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/logs/acp/a11_05_semantic_efficiency_bridge_4gpu_20260708_100650`

Curated result directory:

`/data/250010109/Research_System/Projects/from-attention-to-search/main/experiments/A11/A11_05_semantic_efficiency_bridge`

Completeness:

| Artifact | Count / status |
| --- | ---: |
| training runs | 50 |
| curve rows | 3050 |
| seed summaries | 50 |
| condition summaries | 10 |
| gradient profile rows | 7700 |
| gradient usefulness summaries | 420 |
| ACP status | succeeded |

Key tables:

- `tables/curve_metrics.csv`
- `tables/condition_summary.csv`
- `tables/efficiency_by_seed.csv`
- `tables/report_compact_summary.csv`
- `tables/local_loss_guard_summary.csv`
- `tables/gradient_profile_summary.csv`
- `tables/gradient_usefulness_summary.csv`
- `tables/sample_table.csv`

Key figures:

- `figures/q_curves_identical.png`
- `figures/q_curves_random_boundary.png`
- `figures/final_q_vs_native_h3.png`
- `figures/local_guard_final_loss.png`

Repro command:

```bash
A11_ALLOW_REAL_SUBMIT=1 RUN_NAME=a11_05_semantic_efficiency_bridge_4gpu_20260708_100650 \
  active/synthetic_data_understanding/scripts/submit_a11_05_semantic_efficiency_bridge_4gpu.sh
```

## 10. Interpretation

The experiment supports a narrower but cleaner mechanism claim than the previous all-position result. The direct term

$$
\operatorname{CE}(q_3(\cdot\mid h_T),S_Z)
$$

is not just an accounting detail: adding it to K2 gives K3-like recovery, and removing it from K3 weakens K3. This is exactly the intervention pattern expected if direct decision-prefix supervision contributes to semantic efficiency.

The result also shows why all-position evidence must be handled carefully. K1/K2 and K3 no decision L3 can still recover $Z$ in $Q$, and random initialization can start with $Q=1.0$. Therefore the correct claim is not "only K=3 can learn $Z$" but "direct horizon coverage gives a stronger, more stable, directly predictive path."

## 11. Claim Boundary

Can claim:

- Direct decision-prefix horizon-3 supervision is a supported mechanism component in clean $\tau=3$ all-position training.
- In identical-branch initialization, K2 plus direct L3 matches full K3 and clearly improves over K2.
- Masking direct L3 weakens K3 under identical-branch initialization.
- Local active $Y_1/Y_2$ learning is preserved.
- All-position indirect transfer remains real.

Cannot claim:

- direct supervision is the only way all-position training recovers $Z$;
- random-init speed metrics are meaningful;
- gradient diagnostics prove the optimization cause;
- larger K is generally better;
- natural-language MTP, MoE routing, or expert utility follows.

## 12. Next Decision

The next decision should be one of two narrow options:

1. tighten the optimization bridge with a no-leakage setup and a sharper gradient intervention;
2. move to a harder all-position construction where indirect transfer exists but does not saturate $Q$ at initialization.

Do not broaden to K>3 or natural language until this boundary is settled.

## 13. Links And Artifact Map

anchor: `../../problem_anchors/11_informative_future_branch_mechanism/11_05_semantic_efficiency_bridge_anchor.md`
protocol: `protocol.md`
summary: `summary.md`
runner: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py`
config: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a11_05_semantic_efficiency_bridge.json`
submit script: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_a11_05_semantic_efficiency_bridge_4gpu.sh`
raw result dir: `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a11_05_semantic_efficiency_bridge/a11_05_semantic_efficiency_bridge_4gpu_20260708_100650`
curated table dir: `tables/`
curated figure dir: `figures/`
ACP job id: `pt-u0od5jmz`
