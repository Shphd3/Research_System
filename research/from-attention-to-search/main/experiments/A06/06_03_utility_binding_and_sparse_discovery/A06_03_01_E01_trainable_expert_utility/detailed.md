# Detailed Record: A06_03_01_E01 Trainable Expert Utility Binding

## 0. Quick Recap

**Purpose:** Remove the fixed-expert oracle assumption and test whether route-conditioned data exposure creates held-out task-specific expert function.

**Primary result:** Supported. Correct expert-only exposure produces positive held-out counterfactual utility in 128/128 task-seed cells. Paired correct-minus-shuffle median is 8.892 nats/task-token, seed-clustered 95% CI \([8.694,9.142]\).

**Mechanism update:** Stable route identity creates specialist experts, but the learned utility gap does not monotonically transmit into weighted-top-1 raw router pressure. The pressure comparison reverses: median paired correct-minus-shuffle pressure is -23.44.

**Next decision:** Test route/utility/task co-stability after router release; do not substitute raw pressure magnitude for counterfactual utility.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Unit | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Task | Sequence-level modular transformation | output \((c+f)\bmod4\) | task id | controlled long-range conditional variable | natural semantics |
| Task position | Content predictor whose target depends on the instruction | 16 positions/sequence | positions | isolates conditional prediction | full-sequence quality |
| Utility gap | Assigned expert versus best competitor | \(G_f^{cf}\) | nats/task-token | primary binding decision | route stability |
| Balanced shuffle | Matched compute with changing task-expert identity | four cyclic offsets | update counts | load/count control | real-data nuisance removal |
| Native loss | Loss under actual weighted-top-1 routing | no forced expert | nats/token | bridge deployment path | downstream value |
| Margin pressure | One-step router-gradient boundary movement | \(-\langle g_f-g_b,\mu_f\rangle\) | margin/unit step | local transmission diagnostic | convergence |

## 2. Protocol Compliance Audit

| Requirement | Run 02 result | Status |
| --- | ---: | --- |
| 32 seeds | 32 | pass |
| Primary task-seed cells | 128 | pass |
| Train/test sequence overlap | 0 | pass |
| Initial expert identity error | 0 | pass |
| Minimum native initial route NMI | 0.999999999994 | pass |
| Expert-only non-expert state change | 0 | pass |
| Per-expert update-count spread | 0 | pass |
| Shuffled task-expert pair-count spread | 0 | pass |
| Correct assigned-task loss reduction | 99.968% | pass |
| Finite metrics and complete shard outputs | complete | pass |

Formal run 02 passes all guards. Run 01 is retained separately as an invalid run because its minimum initial route NMI was 0.9198.

## 3. Exact Data Construction

Vocabulary has twelve tokens:

- instruction tokens 0--3;
- content tokens 4--7;
- output tokens 8--11.

For task \(f\) and content value \(c\), the required output value is

\[
y=(c+f)\bmod4.
\]

Each sequence is

```text
[instruction, content_1, output_1, ..., content_16, output_16]
```

giving length 33 and 32 standard autoregressive targets. Content orders use four repeats of values 0--3. Each seed generates eight unique training orders and eight disjoint test orders per task, for 32 train and 32 test sequences. All positions enter the optimization loss; the sixteen content predictors are the primary task positions.

## 4. Model And Optimization

- hidden dimension 64;
- four attention heads;
- one causal attention layer initialized as causal averaging;
- residual plus LayerNorm;
- no learned positional embedding;
- fixed strength-1.0 instruction-state broadcast before LayerNorm;
- four MLP experts, hidden width 128, identical initialization;
- expert output is a residual hidden update;
- fixed readout;
- weighted top-1 router initialized from task-position centers to p05 center margin 0.5.

Exposure training:

- full-sequence cross-entropy;
- 200 updates;
- checkpoints 0, 10, 25, 50, 100, 200;
- expert AdamW LR 0.001;
- representation AdamW LR 0.0005 in joint conditions;
- betas 0.9/0.999, epsilon \(10^{-8}\), weight decay \(10^{-4}\).

## 5. Conditions

| Condition | Trainable blocks | Task-expert assignment | Causal role |
| --- | --- | --- | --- |
| `correct_expert_only` | experts | fixed identity | primary binding test |
| `shuffled_expert_only` | experts | cyclic offsets | load/count control |
| `correct_joint` | experts + representation | fixed identity | moving-representation transfer |
| `shuffled_joint` | experts + representation | cyclic offsets | representation-only control |

The router remains frozen during exposure. Forced assignment uses probability one, so route-score magnitude cannot create the counterfactual utility gap.

## 6. Metric Definitions

For held-out task \(f\) and forced expert \(e\):

\[
L_{f,e}^{cf}
=
\mathbb E_{(h,y)\sim\mathcal D_f^{test}}
\ell(F_{\neg E}(h,E_e(h)),y).
\]

Primary gap:

\[
G_f^{cf}
=
\min_{b\ne f}
\left(L_{f,b}^{cf}-L_{f,f}^{cf}\right).
\]

Controlled binding time is the first checkpoint after which the paired correct-minus-shuffle median remains positive.

Router pressure for the assigned boundary against the best counterfactual competitor is

\[
P_{f,b}=-\langle g_f-g_b,\mu_f\rangle.
\]

Positive \(P\) predicts an infinitesimal SGD update that increases the assigned margin. It is not a counterfactual expert comparison.

## 7. Primary Results

### 7.1 Expert-Only Functional Binding

| Quantity | Correct | Shuffle |
| --- | ---: | ---: |
| Median final task utility gap | 8.8947 | -0.0042 |
| Mean final task utility gap | 8.9592 | -0.0041 |
| Positive-gap rate | 1.0000 | 0.2656 |
| Mean forced assigned task loss | 0.00227 | 0.08440 |
| Median all-position utility gap | 5.6416 | -0.0029 |

The paired correct-minus-shuffle median is 8.8922 with seed-clustered 95% CI \([8.6938,9.1424]\). Persistent paired separation begins at update 10 and grows monotonically at registered checkpoints: 0.6330, 3.2986, 6.6866, 8.1236, and 8.8922.

### 7.2 Joint-Training Transfer

Correct joint exposure ends with median gap 9.5301 and 100% positive cells. Shuffled joint exposure ends at -0.0337 with 16.41% positive cells. The paired correct-minus-shuffle joint gap is positive in 128/128 cells with median 9.5697.

Representation motion therefore does not erase utility formation on the known-good context-state bridge. It does not show that arbitrary learned representations will preserve the partition.

### 7.3 Native Task Path

| Condition | Native task loss | Native all-position loss | Minimum route NMI | Mean p05 margin |
| --- | ---: | ---: | ---: | ---: |
| correct expert-only | 0.8423 | 1.8630 | 1.0000 | 0.4995 |
| shuffled expert-only | 1.8080 | 2.1333 | 1.0000 | 0.4995 |
| correct joint | 0.6584 | 1.4400 | 1.0000 | 0.3091 |
| shuffled joint | 1.8179 | 1.9433 | 1.0000 | 0.2348 |

Fixed route identity is identical for the expert-only pair, yet native task loss differs by 0.966. This is direct evidence that route purity is not functional specialization.

## 8. Router-Pressure Result

| Quantity | Correct expert-only | Shuffled expert-only |
| --- | ---: | ---: |
| Median task-gradient pressure | 121.942 | 146.993 |
| Positive absolute pressure rate | 1.000 | 1.000 |
| Median normalized pressure | 0.9980 | 1.0000 |

Paired correct-minus-shuffle pressure has median -23.440, seed-clustered 95% CI \([-26.817,-20.983]\), and positive rate 1/128 = 0.78%. Within correct expert-only cells, Spearman correlation between utility gap and pressure is -0.309.

H3 is rejected. This does not mean the correct route receives negative pressure: all correct cells are positive. It means utility magnitude is not a calibrated proxy for raw pressure magnitude.

The weighted-top-1 local identity explains the metric mismatch:

\[
\Delta w_j
=
\frac{\eta}{\tau}p_r(\mathbf1[j=r]-p_j)B_rh,
\qquad
B_r=-\langle\nabla_{\hat y}\ell,E_r(h)\rangle.
\]

The update uses selected expert benefit and current residual loss, not \(L_{f,b}^{cf}-L_{f,r}^{cf}\). The shuffled generalists have higher native task loss and stronger raw pressure. This is consistent with residual-error scaling, but a dedicated mediation intervention would be required to attribute the reversal completely to \(B_r\).

## 9. Visualization Results

### Figure 1: Utility-Gap Trajectory

![Utility-gap trajectory](figures/utility_gap_trajectory.png)

- **Purpose:** Test utility emergence and update efficiency.
- **Data:** 32 seeds x four tasks, held-out content orders.
- **Read:** Positive gap is necessary; correct must exceed shuffle.
- **Observed:** Correct conditions separate by step 10; shuffle ends near zero.
- **Take-home:** Stable conditional exposure creates specialist function.
- **Remaining uncertainty:** Oracle assignment was supplied.

### Figure 2: Counterfactual Loss Matrices

![Counterfactual loss matrices](figures/counterfactual_loss_matrices.png)

- **Purpose:** Distinguish specialists from generalists.
- **Read:** Low diagonal/high off-diagonal is specialization; flat matrix is interchangeability.
- **Observed:** Correct exposure gives a sharp diagonal; shuffle gives a flat low-loss matrix.
- **Take-home:** Equal update count is insufficient; stable identity is causal.
- **Remaining uncertainty:** The task is synthetic and the experts have ample capacity.

### Figure 3: Utility-To-Pressure Audit

![Utility-to-pressure audit](figures/utility_router_pressure.png)

- **Purpose:** Test local transmission from utility gap to router pressure.
- **Read:** If H3 held, high-gap correct cells should lie above near-zero-gap shuffle cells.
- **Observed:** The ordering reverses in pressure magnitude.
- **Take-home:** Counterfactual utility and selected-benefit gradient are distinct.
- **Remaining uncertainty:** Actual multi-step router-release stability is not measured.

## 10. Hypothesis Adjudication

| Hypothesis | Verdict | Reason |
| --- | --- | --- |
| H1 correct exposure creates held-out utility | supported | 128/128 positive; paired CI excludes zero |
| H2 representation drift is necessary | rejected | non-expert state change 0; H1 passes expert-only |
| H3 utility magnitude strengthens router pressure | rejected | paired pressure difference is negative in 127/128 cells |
| H4 route purity alone is insufficient | supported | NMI 1.0 in correct and shuffle; utility differs sharply |

## 11. Invalid Run Ledger

Run 01:

- run: `a06_38_full_4gpu_20260710_01`;
- ACP job: `pt-hcom4dn8`, succeeded computationally;
- completed seeds: 32;
- validity failure: minimum native initial route NMI 0.9198;
- decision: H1 and H3 not certified; utility numbers excluded from evidence.

The failure came from instruction information decaying under causal averaging at late task positions. Run 02 adds a fixed instruction-state broadcast as a known-good visibility control. This change protects the supplied-partition assumption and does not alter the primary comparison or threshold.

## 12. Updated Theory

The controlled specialization process now has two distinct contracts:

1. **Utility formation:** stable task-conditioned expert exposure creates function differences. A06_03_01_E01 supports this.
2. **Utility transmission:** the router update must use a signal aligned with relative expert function. Raw weighted-top-1 pressure is not calibrated by \(G_f^{cf}\). A06_03_01_E01 rejects the naive monotonic link.

This yields a concrete gating-design requirement: a useful gate needs persistent context representation, conditional expert exposure, and a relative-utility transmission mechanism. Route purity and selected-expert gradient magnitude are not substitutes for the relative-utility term.

## 13. Claim Boundary

**Supported:** Controlled context-task utility formation, frozen-representation sufficiency, joint-training transfer, route-purity insufficiency, and non-monotonic utility-to-pressure transmission.

**Not supported:** Natural-language semantic experts, label-free discovery, actual router-release stability, real downstream benefit, sparse-compute efficiency, or scaling.

## 14. Next Decision

A06_03_01_E02 should perform the missing multi-step causal handoff. Start from matched correct routers with either specialist checkpoints from correct exposure or generalist checkpoints from shuffled exposure. Release router updates under native weighted top-1 while tracking:

- counterfactual utility gap;
- route NMI and low-tail margin;
- native task and all-position loss;
- selected-benefit pressure and actual finite-step movement.

The primary question is whether functional specialization yields task-preserving route/utility co-stability, not whether it has the largest raw gradient.

## 15. Artifact Map

- Anchor: `main/problem_anchors/06_geometry_proxy_preservation/06_03_utility_binding_and_sparse_discovery/06_03_utility_binding_and_sparse_discovery_anchor.md`
- Protocol: `main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_01_E01_trainable_expert_utility/protocol.md`
- Summary: `main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_01_E01_trainable_expert_utility/summary.md`
- Curated figures: `main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_01_E01_trainable_expert_utility/figures/`
- Curated tables: `main/experiments/A06/06_03_utility_binding_and_sparse_discovery/A06_03_01_E01_trainable_expert_utility/tables/`
- Runner: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/run_a06_38_trainable_expert_utility_binding.py`
- Config: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/configs/a06_38_trainable_expert_utility_binding.json`
- Submitter: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/scripts/submit_a06_38_trainable_expert_utility_binding_4gpu_acp.sh`
- Formal raw results: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_38_trainable_expert_utility_binding/a06_38_full_4gpu_20260710_02/`
- Formal ACP job: `pt-oivsn732`, `SUCCEEDED`.
- Invalid raw results: `XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/a06_38_trainable_expert_utility_binding/a06_38_full_4gpu_20260710_01/`
- Invalid ACP job: `pt-hcom4dn8`, computationally succeeded but failed validity.

Reproduction:

```bash
A0638_ALLOW_REAL_SUBMIT=1 RUN_NAME=a06_38_full_4gpu_20260710_02 JOB_NAME=ats-a0638-context-control-4gpu bash scripts/submit_a06_38_trainable_expert_utility_binding_4gpu_acp.sh
```
