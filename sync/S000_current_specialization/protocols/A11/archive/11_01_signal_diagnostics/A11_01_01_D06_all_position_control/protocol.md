# Protocol: A11_04_02 K=3 All-Position Control

## 0. Approval Snapshot

Approval status: requested by user on 2026-07-08 after the decision-only K=2/K=3 runs were completed and audited.

Purpose: test whether the $\tau=3$ first-informative-horizon result survives a more language-model-like all-position objective.

Primary anchor: `Projects/from-attention-to-search/main/problem_anchors/11_informative_future_branch_mechanism/11_04_k3_first_informative_horizon_anchor.md`

Decision question: Under all-position LM-style loss, does K=3 still recover the early branch variable $Z$ from the decision prefix $h_T$ beyond K=1/K=2?

Primary metric: clean-regime `coverage_gap`, defined as

$$
\Delta_{\mathrm{cov}}=\operatorname{AUC}_Q(3)-\max\{\operatorname{AUC}_Q(1),\operatorname{AUC}_Q(2)\}.
$$

Pass: clean K=3 has positive coverage gap, K=1/K=2 remain low or clearly lower, noisy controls do not match clean K=3, and $Y_1,Y_2$ local targets are preserved.

Fail: K=1/K=2 match K=3 in clean $\tau=3$, noisy K=3 behaves like clean K=3, or K=3 wins only by damaging local targets.

Claim boundary: this can support only controlled all-position robustness of the $\tau=3$ coverage mechanism. It cannot prove natural-language transfer or broad next-K scaling.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| all-position LM-style loss | Train offset heads at every valid sequence position | for active horizon $j$, predict $X_{t+j}$ from each valid $t$ | tests whether decision-only mechanism survives background LM losses | natural-language transfer |
| decision prefix $h_T$ | hidden state after `BR_z F... U...` | same evaluation position as A11_04 | keeps evaluation comparable | behavior at all hidden states |
| coverage gap | K=3 advantage over K=1/K=2 | $\operatorname{AUC}_Q(3)-\max\{\operatorname{AUC}_Q(1),\operatorname{AUC}_Q(2)\}$ | primary decision metric | universal K scaling |
| clean $\tau=3$ | first branch-informative target at horizon 3 | $Y_1=A,\;Y_2=C,\;Y_3=S_Z$ | main mechanism test | real semantics |
| noisy horizon-3 | horizon-3 target is branch-independent | $Y_3\perp Z$ | false-positive guard | all noise behavior |
| redundant horizon-3 | earlier active target reveals branch | $Y_2=S_Z,\;Y_3=T_Z$ | distinguishes new information from redundancy | new long-horizon information |

## 2. Setup

Use the same data/model matrix as A11_04:

- conditions: `K1_fixed_3head`, `K2_active`, `K3_active`;
- regimes: `clean_tau3`, `noisy_h3`, `redundant_h3`;
- init modes: `identical_branch`, `random`;
- seeds: `971,972,973,974,975`;
- model: one-layer one-head Transformer, `d_model=64`;
- training: `15000` steps, eval every `500` steps.

Only the training scope changes:

$$
\texttt{decision\_only}\quad\rightarrow\quad\texttt{all\_positions\_lm\_control}.
$$

The evaluation remains at the decision prefix $h_T$.

## 3. Artifacts

Code workspace:
`/data/250010109/Research_System/Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments`

Runner:
`active/synthetic_data_understanding/scripts/run_a11_03_04_semantic_efficiency.py`

Config:
`active/synthetic_data_understanding/configs/a11_04_k3_first_informative_horizon_all_positions.json`

Expected result directory:
`active/synthetic_data_understanding/results/a11_04_k3_first_informative_horizon_all_positions/<run_name>/`
