# Detailed: A12_02 One-Step Standard-NTP Interference

Primary anchor: `../../../problem_anchors/12_structured_compositional_mtp_workload/12_02_one_step_ntp_interference_anchor.md`
Protocol: `protocol.md`
Summary: `summary.md`

## 0. Quick Recap

**Purpose:** Quantitatively test the local gradient-interference equation.
**Hypothesis:** $\Delta_{obs}=\Delta_{pred}+O(\eta^2)$ for small paired updates, relative to an NTP-only update from the same state.
**Experiment logic:** clone one checkpoint and batch into NTP-only and joint updates, then compare the same standard loss.
**Conclusion:** numerical identity supported; intended learned-task mechanism remains insufficient because calibration failed.
**Evidence:** smallest-step slope `1.0174`, correlation `0.9990`, sign `1.0000`; answer accuracy `0.125` in `5/5` seeds.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| $g_N$ | shared standard-loss gradient | $\nabla_\theta L_N$ | parameter gradient | baseline update | long-run path |
| $g_A$ | auxiliary future-loss gradient | $\nabla_\theta L_A$ | parameter gradient | added update | task usefulness |
| Interference prediction | first-order extra standard-loss change | $-\eta\langle g_N,g_A\rangle$ | nats | mechanism prediction | curvature |
| Calibration guard | held-out task learning | answer accuracy after NTP burn-in | probability | makes gradients task-conditioned | why learning failed |

## 2. Anchor Link And Decision Point

The anchor permits the capacity question only after the local equation passes with a calibrated composition checkpoint. Numerical fidelity passed; task calibration did not. The correct decision is therefore not to open A12_03.

## 3. Protocol Compliance Audit

**approved conditions match actual conditions:** yes, except that no checkpoint reached the preregistered calibration threshold; the fallback step-600 checkpoints were audited as specified.
**primary metric exists:** yes.
**central figures/tables exist:** yes.
**seeds/checkpoints recorded:** yes, seeds `971--975`, step 600.
**known good/bad/confusing cases reviewed:** the small-step identity and step-size curvature guard passed; the task-calibration known-good case failed. The preregistered shuffled-gradient negative control was not executed. Because a specified guard is missing and the calibration guard already fails, the result cannot be promoted beyond insufficient evidence.
**success/failure/insufficient-evidence criteria applied:** yes; verdict is insufficient evidence.

## 4. Setup

**Research question:** Does first-order gradient interference predict the paired one-step standard-loss difference?
**Data construction:** $M=8$; two target permutations and four distractor permutations; six tables × 25 tokens plus a five-token query; total input length 155. The answer is $Y=\pi_2(\pi_1(A))$.
**Train / eval / probe split:** train 8192; validation 1024; audit 1024. Split seeds are `71201`, `71202`, `71203`; permutations are unique within each generated split.
**Model:** one Transformer encoder layer with causal mask, tied input/output embeddings, hidden width 64, four attention heads, MLP width 256.
**Input representation / position encoding:** atomic tokens and learned absolute positions.
**Loss / objective:** $L_N=L_{format}(h_T)+L_{answer}(h_{T+1})$; $L_A=L_{answer}^{direct}(h_T)$.
**Optimizer or update rule:** AdamW, learning rate `3e-4`, weight decay `0.01` for burn-in; direct float64 SGD perturbations for audit.
**Training steps / tokens / batch size:** maximum 600 burn-in steps, batch size 64; audit batch size 32.
**Checkpoints:** all step 600 because answer accuracy never reached `0.70`.
**Seeds:** `971--975`.
**Conditions:** standard-gradient update versus standard-plus-auxiliary-gradient update.
**Changed variables:** auxiliary gradient inclusion and relative step norm.
**Held fixed:** all other state, batch, targets, and parameters.
**Script path:** `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a12_02_one_step_ntp_interference.py`.
**Result path:** `Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a12_02_one_step_ntp_interference_full/`.
**Known setup limitation:** one layer did not learn the two-hop task; the protocol intended standard answer-unembedding rows for direct readout, while implementation used the same tied unembedding directly. This is not a separately frozen auxiliary head and narrows the implementation boundary. The shuffled-gradient negative control was also not run.

## 5. Metrics And Decision Rules

The primary slope is

$$
\widehat\beta=\frac{\sum_i\Delta_{pred,i}\Delta_{obs,i}}{\sum_i\Delta_{pred,i}^2}.
$$

For a twice-differentiable controlled standard loss, the local expansion is

$$
\Delta_{obs}
=-\eta\lambda g_N^\top g_A
+\eta^2\lambda g_N^\top H_N g_A
+\frac{\eta^2\lambda^2}{2}g_A^\top H_N g_A
+O(\eta^3).
$$

The sign of the first term compares the joint update with NTP-only; it does not determine whether either update raises or lowers the loss relative to the original checkpoint.

Pass required slope $[0.8,1.2]$, correlation $\ge0.95$, sign $\ge0.90$, median normalized residual $\le0.20$, and calibration accuracy $\ge0.70$. The last guard failed in every seed.

## 6. Main Results

### Decision evidence

| Relative step | Slope | Pearson | Sign agreement | Median normalized residual |
| ---: | ---: | ---: | ---: | ---: |
| $10^{-5}$ | 1.0174 | 0.9990 | 1.0000 | 0.1012 |
| $3\times10^{-5}$ | 1.0570 | 0.9891 | 1.0000 | 0.3046 |
| $10^{-4}$ | 1.3202 | 0.7722 | 0.8000 | 1.0676 |

Pooled over the two smallest scales: slope `1.0530`, Pearson `0.9741`, sign agreement `1.0000`, and median normalized residual `0.1102` over 320 rows.

### Stage-level profiling evidence

Every seed has validation format accuracy `1.0` but answer accuracy `0.125`. The model learned the local format target and not the two-hop answer.

### Failed or ambiguous evidence

Four seeds have negative batchwise gradient inner product throughout the audit and one seed has positive inner product. Mean gradient cosine is `-0.01349`. This shows that interference sign is checkpoint-dependent and not universally negative.

## 7. Visualization Results

### Predicted versus observed one-step standard-loss difference

![Predicted versus observed one-step standard-loss difference](figures/prediction_fidelity.png)

**Purpose:** validate the first-order equation and inspect curvature scaling.
**Setup:** 5 seeds × 32 batches × 3 relative step norms.
**Metric definition:** predicted versus observed paired standard-loss difference; normalized residual.
**Metric unit:** nats and dimensionless residual.
**How to read:** identity-line agreement supports the equation; rising residual with step size identifies curvature.
**Expected if supported:** tight small-step identity.
**Expected if weakened or incomplete:** small-step disagreement or unresolved signal.
**Observed result:** excellent smallest-step agreement, then progressive deviation.
**Take-home:** the Taylor term is a valid local predictor at $10^{-5}$.
**Remaining uncertainty:** whether the same relation explains optimization after composition learning.
**What this figure does not prove:** a task-conditioned harm mechanism.
**Anchor update implication:** preserve the equation, repair calibration first.

Rendered-artifact audit: the figure renders; axis units, identity reference, step-size legend, and residual definition are readable. The figure is decision-relevant but must be read with the calibration table.

## 8. Stage Evidence And Failure Decomposition

| Stage | Evidence | Status | Failure reason | What this rules out |
| --- | --- | --- | --- | --- |
| data construction | exact lengths and balanced labels | passed | none observed | label/length shortcut as main cause |
| NTP burn-in | format 1.0, answer 0.125 | failed | one-layer learner did not compose | interpreting gradients as learned-task gradients |
| paired finite difference | small-step slope/correlation/sign pass | passed | none | autograd sign or clone mismatch |
| curvature audit | residual increases with step | passed | expected curvature | using $10^{-4}$ as a first-order regime |

**Falsified physical prior:** not falsified; the local geometry prior passed numerically.
**Falsified mathematical model:** not falsified in the small-step regime.
**Falsified operationalization / proxy:** the one-layer burn-in is not a valid learned-composition checkpoint.
**Falsified implementation:** no numerical finite-difference fault was observed, but protocol compliance is incomplete because the auxiliary readout was shared/tied and the shuffled negative control was not executed.
**Falsified metric:** no.
**Remaining rival explanations:** insufficient computational depth, optimization difficulty, and direct-head calibration.

## 9. Full Experiment Record

- Five model seeds, 160 audit batches per step size.
- All requested relative step sizes completed.
- Raw `finite_difference.csv` has 480 rows and remains in the ignored execution result directory.
- Curated tables: `tables/step_size_summary.csv`, `tables/checkpoint_guards.csv`, and `tables/hypothesis_decision.json`.

## 10. Interpretation

The result separates two claims that were previously conflated. The Taylor equation is a reliable local calculus statement at sufficiently small updates. It does not by itself explain small-model Next-2 harm on a learned long-range composition task. The failed calibration guard is substantive: the standard answer gradient and auxiliary answer gradient are measured before the model has acquired the composition function.

## 11. Claim Boundary

**Supported:** numerical first-order fidelity for paired local updates.
**Insufficient:** learned-task gradient-interference explanation.
**Not tested:** effective rank, safe update subspace, curriculum, scale, real data, or long-run MTP/NTP comparison.

## 12. Next Decision

Construct exactly one calibration repair: keep the same permutation data and objectives, but use a minimal architecture known to represent two relation-composition steps. Require held-out answer accuracy $\ge0.70$ before any gradient audit. Do not start capacity or curriculum anchors before this gate passes.

## 13. Links And Artifact Map

**anchor:** `../../../problem_anchors/12_structured_compositional_mtp_workload/12_02_one_step_ntp_interference_anchor.md`
**protocol:** `protocol.md`
**summary:** `summary.md`
**code workspace:** `/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`
**runner:** `active/synthetic_data_understanding/scripts/run_a12_02_one_step_ntp_interference.py`
**config:** command-line contract frozen in protocol; decision JSON records resolved values
**key code files:** runner above
**data / manifest:** raw result `data_manifest.json`
**result dir:** `active/synthetic_data_understanding/results/a12_02_one_step_ntp_interference_full/`
**figure dir:** `figures/`
**key tables:** `tables/step_size_summary.csv`, `tables/checkpoint_guards.csv`, `tables/hypothesis_decision.json`
**logs / checkpoints:** no checkpoint persisted; stdout was execution-only
**repro command:** `python active/synthetic_data_understanding/scripts/run_a12_02_one_step_ntp_interference.py --device cuda:0 --output-dir active/synthetic_data_understanding/results/a12_02_one_step_ntp_interference_full`
**job id:** local GPU execution; no ACP job id
