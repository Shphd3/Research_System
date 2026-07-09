# Protocol: A06_33 Frozen-Hidden Advantage-To-Margin Audit

文档状态：中文 protocol draft for approval。该文件用于 2026-07-09 daily specialization folder。它不是正式项目实验目录下的 canonical `protocol.md`，也不授权直接运行实验。若用户批准并迁入项目，应转写为 English canonical protocol，并保留中文 companion。

## 0. Approval Snapshot

**Approval status:** Draft for user review; not approved to run by this document.

**Purpose:** 判断 expert advantage 是否能预测 router row 的一步更新和 feature route margin 的一步变化。若不能预测，不应继续把 advantage-based specialization 作为新 router 的理论基础。

**Primary anchor:** `06_33_signal_noise_advantage_margin_budget_anchor_cn.md`.

**Anchor decision question:** In a frozen-hidden controlled setting, does the probability-weighted expert advantage gap $p_aA_a-p_bA_b$ predict the sign and relative size of one-step matched route-margin change?

**Anchor physical prior tested:** Router row movement is advantage-weighted hidden movement; feature specialization requires positive matched expert advantage, not only geometric route purity.

**Anchor core model term tested:**

$$
\Delta m_{f,a,b}^{pred}
\approx
\eta\frac{1}{\tau}\mathbb E[(p_aA_a-p_bA_b)h^\top\mu_f\mid f].
$$

**Anchor falsifier:** If $\Delta m^{pred}$ and $\Delta m^{actual}$ have low sign agreement, low correlation, or reversed relation in frozen-hidden settings, the advantage-based margin model is invalid as the next router-design basis.

**Experiment role:** Root-cause audit and mathematical-model audit. It is not method construction.

**Primary metric from anchor:** sign agreement and correlation between predicted and actual one-step route-margin change.

**Claim boundary from anchor:** Can only support or weaken the one-step advantage-to-margin mechanism. Cannot claim real-DCLM transfer, semantic experts, expert utility, deployable gating, or that linear routers are sufficient.

**Minimal setup:** Frozen hidden states, fixed feature centers, fixed expert outputs, differentiable soft-router or probability-weighted top-1 router update, one-step router-row update only.

**Basic configuration:** Use the existing controlled no-position slot-bridge surface when available. If saved hidden/expert snapshots are unavailable, use a minimal synthetic frozen-hidden table with known feature labels and expert outputs. No full model training.

**Conditions to run:**

1. known-good utility-bearing expert geometry;
2. identical/no-utility expert guard;
3. shuffled or crossed matched-label guard;
4. high-NMI confusing guard if available.

**Pass:** $\Delta m^{pred}$ and $\Delta m^{actual}$ have high sign agreement and positive correlation in known-good conditions, while known-bad controls do not show false positive matched margin growth.

**Fail:** Prediction is low-correlation, reversed, or bad controls pass as if they had specialization signal.

**Insufficient:** Required objects are missing, or implementation has pure hard argmax with no measurable router-gradient path and no probability-weighted surrogate.

**Cannot claim:** New router method, MPI improvement, MTP transfer, real semantic experts, utility, or full training preservation.

**Approval decision:** User should approve / revise / park before any run.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Frozen hidden | Hidden states are not updated during the audit | Use fixed $h_i$ and fixed $\mu_f$ | condition | Isolates router row movement | Full training behavior |
| Expert advantage | Whether more weight on expert $e$ would reduce loss | $A_e=-\langle\nabla_{\hat y}\ell,E_e(h)-\hat y\rangle$ | scalar | Candidate task signal to router | Semantic feature identity |
| Advantage gap | Matched expert signal minus competitor signal | $p_aA_a-p_bA_b$ | scalar | Predicts margin growth direction | Long-run preservation |
| Predicted margin change | Model-predicted one-step route margin change | $\Delta m^{pred}$ | logit gap change | Primary prediction | Real causality without actual update |
| Actual margin change | Measured one-step margin change after router update | $\Delta m^{actual}$ | logit gap change | Primary target | Full model behavior |
| Sign agreement | Fraction where predicted and actual margin changes have same sign | mean sign match over feature-competitor pairs | fraction | Decides whether the mechanism predicts direction | Magnitude accuracy alone |
| Correlation | Whether predicted larger changes correspond to actual larger changes | Pearson / Spearman over pairs | scalar | Decides whether model predicts relative strength | Direction for every pair |
| Known bad guard | Condition that should not have specialization signal | identical experts / shuffled labels / no-utility outputs | condition | Catches false positives | Exhaustive invalidation |

## 2. Anchor Alignment

**Decision question:** Does $p_aA_a-p_bA_b$ predict one-step matched margin movement?

**Physical prior tested:** Expert specialization has a training signal only when matched expert advantage is positive and feature-conditioned.

**Core model term tested:** The advantage-gap contribution to $\Delta m_f$.

**Falsifier:** Low or reversed prediction quality in frozen-hidden conditions.

**Claim boundary:** This is a mechanism audit. It does not construct or validate a new router.

## 3. Tested Hypothesis

**H1:** In a differentiable frozen-hidden router update, the one-step matched margin change is predicted by the probability-weighted expert advantage gap.

Supported pattern:

$$
\operatorname{sign\_agree}(\Delta m^{pred},\Delta m^{actual})\text{ high},
$$

and

$$
\operatorname{corr}(\Delta m^{pred},\Delta m^{actual})>0.
$$

Weakened pattern:

$$
\operatorname{sign\_agree}\text{ low},
\qquad
\operatorname{corr}\le 0,
$$

or bad controls pass.

## 4. Rival Explanations

| Rival explanation | Why plausible | Protocol guard |
| --- | --- | --- |
| Hidden drift, not router row update, moves margin | Full training changes both $w_e$ and $\mu_f$ | Freeze hidden states and feature centers |
| Pure hard top-1 has no router-gradient path | Some implementations use argmax without differentiable gate weight | Record router-gradient path; mark insufficient if no surrogate exists |
| NMI hides wrong expert identity | Feature partition can remain pure after label permutation | Report matched preserve and margin, not NMI alone |
| Expert outputs have no utility difference | If all experts behave alike, routing cannot learn specialization | identical/no-utility expert guard |
| Row norm or load scale creates fake margin growth | Scaling rows can change score gaps without utility | record row norm, load, and known bad controls |

## 5. Data / Model / Algorithm / Objective

**Data:** Controlled synthetic feature-labeled examples from the no-position slot-bridge surface, or a minimal frozen-hidden table if existing snapshots are unavailable.

**Model:** One-layer Transformer + one-layer MoE surface when using existing project snapshots; otherwise fixed hidden states, fixed expert functions, and a differentiable router update. The audit does not require full training.

**Router:** Prefer soft router or probability-weighted top-1 surrogate because the anchor's formula assumes differentiable route probability. If the available implementation is pure hard top-1, record this as implementation boundary and do not force the formula.

**Expert outputs:** For each hidden state $h_i$, compute or load $E_e(h_i)$ for every expert $e$.

**Objective:** Use the local supervised loss already attached to the synthetic task. The protocol needs $\nabla_{\hat y}\ell$ to compute $A_e$.

**No full training:** Only one-step router update is allowed in this protocol. Multi-step background-ratio budget is a follow-up after this model is validated.

## 6. Conditions, Seeds, And Checkpoints

| Item | Anchor clause tested | Model term / rival explanation | Why needed | Primary or secondary evidence | Pass | Fail | Insufficient | Figure/table |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 known-good utility geometry | H1 | $p_aA_a-p_bA_b$ predicts $\Delta m$ | Tests main mechanism | Primary | high sign agreement and positive correlation | low/reversed relation | missing $A_e$ or update path | `advantage_margin_prediction.csv`, scatter |
| C2 identical/no-utility experts | H2 guard | no true advantage | Catches false positives | Secondary | advantage gap near zero; no matched growth | positive support despite no utility | expert outputs unavailable | guard table |
| C3 shuffled/crossed matched labels | NMI guard | matched identity vs pure partition | Ensures NMI cannot decide alone | Secondary | margin/matched preserve catches failure | NMI-only would pass and margin guard misses | mapping unclear | matched-preserve table |
| C4 high-NMI confusing case, if available | metric guard | high route purity without correct identity | Protects claim boundary | Secondary | high NMI does not override negative margin | confusing case passes as supported | unavailable but not blocking | confusion table |

**Seeds:** Use the smallest available seed set that covers known-good and known-bad controls. If using existing A06-style synthetic snapshots, prefer 4-8 seeds. If not available, run 3 minimal seeds only for smoke-level mechanism audit. Do not expand seed count before the primary metric is valid.

**Checkpoints:** Frozen hidden checkpoint only. Optional one-step post-update checkpoint for router rows.

## 7. Primary Metric

Primary metric has two parts.

### 7.1 Sign agreement

$$
\operatorname{sign\_agree}
=
\frac{1}{N}\sum_i \mathbf 1[\operatorname{sign}(\Delta m_i^{pred})=\operatorname{sign}(\Delta m_i^{actual})].
$$

Why it decides: the physical prior predicts direction of margin movement. If direction fails, the mechanism is wrong or incomplete.

Expected support threshold: at least 0.80 in known-good conditions and clearly above known-bad controls.

### 7.2 Correlation

Use Pearson and Spearman between $\Delta m^{pred}$ and $\Delta m^{actual}$ across feature-competitor pairs or examples.

Why it decides: even if sign is mostly right, the model should rank stronger and weaker margin updates.

Expected support threshold: positive and substantial correlation, target $\ge 0.70$ for the first controlled audit. If sample size is small, report confidence intervals or mark as smoke-level only.

## 8. Secondary Metrics

| Metric | Definition | Why needed | Cannot prove |
| --- | --- | --- | --- |
| advantage gap distribution | distribution of $p_aA_a-p_bA_b$ by feature | shows whether positive matched signal exists | preservation |
| margin p05 | lower-tail matched route margin | catches fragile assignment | utility |
| matched preserve fraction | fraction staying in original matched expert region | catches label permutation | semantic expert |
| sign flip rate | fraction of pairwise margins crossing nonpositive | detects boundary crossing | cause of crossing |
| feature NMI | NMI(feature, route) | collapse / alignment guard | expert value |
| row norm change | $\|w_e^+\|-\|w_e\|$ | catches norm-only artifacts | utility |
| max load / active experts | route concentration | catches collapse | specialization |
| local loss | supervised loss before/after one step | ensures one-step update is not pathological | routing value |

## 9. Known Good / Known Bad / Known Confusing Cases

**Known good:** A constructed or existing condition where matched experts have feature-specific utility. Expected: positive matched advantage gap and positive $\Delta m$.

**Known bad:** Identical experts or no-utility expert outputs. Expected: no stable positive advantage gap; if route margin grows anyway, the metric is confounded.

**Known confusing:** High feature NMI with wrong matched expert identity, such as shuffled labels or crossed initialization. Expected: NMI may be high, but matched preserve and margin should fail.

If any of these cannot be instantiated from existing artifacts, record it in the setup audit. Missing known-good is blocking; missing optional high-NMI confusing case is not blocking if shuffled guard exists.

## 10. Stage-Level Profiling Plan

| Stage | Local question | Input evidence | Pass / fail / unclear rule | Debug artifact | Handoff |
| --- | --- | --- | --- | --- | --- |
| S0 setup audit | Are required objects available? | hidden states, feature labels, router rows, expert outputs, loss gradients | pass if all primary objects exist | setup readiness table | stop if blocking |
| S1 advantage computation | Can $A_e$ be computed for every expert? | expert outputs and $\nabla_{\hat y}\ell$ | pass if no missing expert rows | advantage table | protocol result table |
| S2 predicted update | Does formula produce $\Delta w^{pred}$ and $\Delta m^{pred}$? | $p_e$, $A_e$, $h$, $\mu_f$ | pass if finite and stable | prediction table | main metric input |
| S3 actual update | Can actual one-step router update be measured? | differentiable router path | pass if update path exists; insufficient if pure hard argmax blocks it | actual-update table | primary metric input |
| S4 comparison | Does prediction match actual? | predicted/actual margin change | pass/fail by primary metric | scatter/table | summary |
| S5 guards | Do known bad/confusing cases behave correctly? | bad/control conditions | fail if bad controls pass | guard table | boundary update |

## 11. Algorithm Specification

**input:**

- hidden states $h_i$;
- feature labels $f_i$;
- feature centers $\mu_f$;
- router rows $w_e$;
- expert outputs $E_e(h_i)$ for all experts;
- loss gradient $\nabla_{\hat y}\ell_i$;
- route probabilities $p_e(h_i)$ or a differentiable surrogate;
- matched map $a(f)$;
- learning rate $\eta$ and temperature $\tau$ used only for one-step prediction.

**parameters:**

| Parameter | Meaning | Default | Reason | Too small / too large risk |
| --- | --- | --- | --- | --- |
| $\eta$ | one-step router update scale | same as local router update if available; otherwise normalized to 1 for relative prediction | prediction mostly judged by sign/correlation | too large may leave local approximation |
| $\tau$ | router softmax temperature | use model value if available | affects $p_e$ and update scale | too small mimics hard top-1 and may saturate |
| matched map | feature-to-expert identity | step-0 matched assignment or oracle mapping | needed for margin | wrong map creates false failure |

**intermediate variables:**

- $p_e(h_i)$;
- $A_e(h_i,y_i)$;
- $p_eA_e$;
- $\Delta w_e^{pred}$;
- $\Delta w_e^{actual}$;
- $\Delta m_{i,a,b}^{pred}$;
- $\Delta m_{i,a,b}^{actual}$.

**steps:**

1. Load or construct frozen hidden states and feature labels.
2. Compute feature centers $\mu_f$.
3. Compute route probabilities $p_e(h_i)$.
4. Compute each expert output $E_e(h_i)$.
5. Compute mixture output $\hat y_i$ and loss gradient $\nabla_{\hat y}\ell_i$.
6. Compute $A_e(h_i,y_i)$ for every expert.
7. For each feature and competitor pair, compute advantage gap $p_aA_a-p_bA_b$.
8. Compute $\Delta m^{pred}$ from the anchor formula.
9. Apply or read one actual router update while hidden states remain frozen.
10. Compute $\Delta m^{actual}$.
11. Compare sign agreement and correlation.
12. Run bad/confusing guards and record whether they fail as expected.

**outputs:**

- `tables/setup_readiness.csv`;
- `tables/advantage_by_feature_expert.csv`;
- `tables/margin_prediction_by_pair.csv`;
- `tables/guard_results.csv`;
- optional `figures/pred_vs_actual_margin_change.png` after plot contract.

**debug artifacts:**

- sample-level rows for 10 representative examples;
- router-gradient path audit;
- row norm before/after table;
- any missing-object report.

**pass conditions:**

- setup objects complete;
- known-good condition shows sign agreement $\ge 0.80$ and positive correlation;
- known-bad controls do not produce false positive margin-growth evidence;
- matched preserve / margin guards catch high-NMI wrong-identity cases.

**fail conditions:**

- prediction and actual update are low-correlation or reversed;
- known-bad controls look supported;
- metric passes only through row-norm or load artifacts.

**failure reasons:**

- physical prior false;
- mathematical model missing top-1 selected-feedback term;
- implementation has no differentiable router update path;
- expert outputs have no utility distinction;
- operationalization confounds route purity with matched identity.

## 12. Success / Failure / Insufficient Evidence

**Success:** The one-step expert-advantage model predicts route-margin movement and guards pass. Next action: write the follow-up signal/noise/background margin-budget anchor or protocol.

**Failure:** The model does not predict one-step margin movement, or bad controls pass. Next action: do not design new router; revise the mathematical model, likely toward top-1 selected-feedback dynamics or direct expert-utility instrumentation.

**Insufficient evidence:** Required objects are missing, or hard top-1 implementation gives no measurable router feedback. Next action: write a setup-recovery or implementation-boundary note before any experiment claim.

## 13. What This Cannot Claim

This protocol cannot claim:

- real-DCLM preservation;
- real semantic expert identity;
- expert utility;
- dense-beating MoE;
- final router method validity;
- MPI / spectral-router success;
- MTP improves MoE routing;
- linear router sufficiency.

It can only decide whether the next theory should keep expert advantage as the central mechanism variable.

## 14. Review Notes And Protocol Changes

- 2026-07-09 draft: created as daily specialization reframing protocol.
- User review needed before execution.
- If user wants to move this into `Projects/from-attention-to-search/`, convert to English canonical `protocol.md` after anchor approval and place beside the canonical experiment folder.
