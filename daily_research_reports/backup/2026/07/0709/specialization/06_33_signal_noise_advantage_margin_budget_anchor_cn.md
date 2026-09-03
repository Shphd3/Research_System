# 06_33: Signal/Noise Advantage Margin Budget Anchor

文档状态：中文 daily anchor draft。该文件用于 2026-07-09 specialization 机制重定义，不是 `Projects/from-attention-to-search/` 下的 canonical anchor。后续若迁入项目主线，应按项目规则转成 English canonical anchor，并保留中文 companion。

## 0. researcher judgment record

**Phenomenon:** 当前 top-1 MoE gating 可以在 controlled setting 中通过 route-position centers 建立 feature-to-expert routing，但 ordinary training 会擦除 real-DCLM proxy routing；mixed full-LM synthetic 条件下 even ideal center 也会丢 margin，而 no-background full-slot 条件可以保持。现象说明：问题不只是 feature geometry 是否存在，而是 training feedback 是否把 feature-specific signal 转成稳定 route margin。

**Mechanism guess:** Router row 的一步移动由 expert advantage、routing probability 和 hidden direction 共同决定。真正的 specialization 需要 matched expert 对对应 feature 有正 probability-weighted advantage，并且这个正 signal 大于 background / common / noise / hidden drift 对 margin 的消耗。

**Key variables:** feature $f$，matched expert $a(f)$，competitor expert $b$，hidden state $h$，feature center $\mu_f$，router row $w_e$，route probability $p_e$，expert output $E_e(h)$，expert advantage $A_e$，advantage gap $p_aA_a-p_bA_b$，predicted margin change $\Delta m^{pred}$，actual margin change $\Delta m^{actual}$。

**Causal relation:** If matched expert advantage is the real routing signal, then positive $p_aA_a-p_bA_b$ on feature $f$ should predict positive one-step change in matched route margin. If not, route purity or center initialization is not evidence that training can learn specialization.

**Observable metric:** Primary metric is sign agreement and correlation between predicted one-step margin change $\Delta m^{pred}$ and actual one-step margin change $\Delta m^{actual}$ in frozen-hidden conditions.

**Rival Explanations:** Margin movement may be caused by hidden drift rather than router row movement; top-1 hard routing may have no differentiable router feedback; high NMI may hide expert identity changes; expert outputs may not contain any feature-specific utility; background/common positions may dominate only in multi-step training, not one-step frozen-hidden dynamics.

**Decision:** If advantage gap predicts one-step margin change and known bad controls fail, pursue signal/noise margin-budget decomposition and then design router-expert coupling methods. If it fails, revise the specialization definition or move to top-1 selected-feedback audit before proposing a new router.

## 1. Problem Definition

**Parent problem:** The active specialization line asks whether top-1 MoE gating can form a stable, interpretable, and useful feature-level expert partition. Current bottleneck is preservation: a proxy partition can be initialized, but ordinary training overwrites it.

**Sharper subproblem:** Before designing a new router, decide whether expert advantage is a measurable mechanism that explains router row movement and route-margin growth.

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Expert advantage | Whether increasing one expert's contribution would lower the current loss | $A_e=-\langle\nabla_{\hat y}\ell,E_e(h)-\hat y\rangle$ | scalar | Candidate task signal that moves router rows | Semantic identity |
| Advantage gap | Matched expert advantage over competitor | $p_aA_a-p_bA_b$ | scalar | Predicts whether matched margin should grow | Long-run preservation |
| Route margin | Matched expert score over competitor | $m_{f,a,b}=(w_a-w_b)^\top\mu_f$ | logit gap | Direct preservation object | Expert utility |
| Predicted margin change | One-step margin change predicted from advantage model | $\Delta m^{pred}$ | logit gap change | Primary model prediction | Full training behavior |
| Actual margin change | Measured one-step route margin change after applying the router update | $\Delta m^{actual}$ | logit gap change | Primary empirical target | Cause without controls |
| Frozen hidden | Hidden states are held fixed while router rows update | No update to encoder / expert hidden states | condition | Separates router-row movement from hidden drift | Real full-LM training |
| Known bad control | A condition that should not produce feature-specific margin growth | identical experts, shuffled matched labels, or no-utility expert outputs | condition | Catches false positive metrics | All possible bad cases |

**Decision question:** In a frozen-hidden controlled setting, does the probability-weighted expert advantage gap $p_aA_a-p_bA_b$ predict the sign and relative size of one-step matched route-margin change?

**Not in scope:** Real-DCLM transfer, semantic expert identity, deployable router design, MTP bridge, full training utility, or proving that linear routers are sufficient.

## 2. Physical Priors

**P1: Router row movement is advantage-weighted hidden movement.**  
**Meaning:** In a differentiable soft-router or probability-weighted top-1 approximation, router row movement should be proportional to routing probability, expert advantage, and hidden direction.  
**Could be wrong if:** The implementation has pure hard argmax with no router gradient, or expert advantage does not match actual router update.

**P2: Feature specialization requires positive matched advantage, not only geometric separation.**  
**Meaning:** A feature-centered router can start with high NMI, but training can only thicken its matched margin if the matched expert has higher advantage on that feature than competitors.  
**Could be wrong if:** Margin grows without measurable advantage gap, or a different mechanism such as auxiliary load loss dominates router movement.

**P3: Preservation failure is a finite budget problem.**  
**Meaning:** Even if initial margin is positive, background/common/noise/hidden drift can consume it. The first audit must separate positive feature signal from margin-consuming terms.  
**Could be wrong if:** Margin crossing is unrelated to measurable signal/noise/common/hidden terms, or high NMI remains decision-equivalent to matched preservation.

## 3. Falsifiable Hypotheses

**H1: One-step advantage-to-margin hypothesis.**  
**Supported if:** In frozen-hidden conditions, $\Delta m^{pred}$ and $\Delta m^{actual}$ have high sign agreement and positive rank/correlation across feature-competitor pairs, while known bad controls do not show positive predicted margin growth.  
**Weakened if:** $\Delta m^{pred}$ is low-correlation, reversed, or only works in conditions where the metric is confounded by row norm, load, or label matching artifacts.

**H2: No-advantage no-specialization-signal hypothesis.**  
**Supported if:** Conditions with identical or no-utility experts have near-zero advantage gap and do not produce matched margin growth despite possible route purity.  
**Weakened if:** They produce strong positive margin growth indistinguishable from utility-bearing conditions.

**H3: Budget-follow-up hypothesis.**  
**Supported if:** Once H1 is valid, multi-step margin erosion can be decomposed into positive signal and negative background/common/noise/hidden terms.  
**Weakened if:** H1 fails, because then the margin budget lacks a valid signal term and should not be promoted to method construction.

## 4. Mathematical Model

**Objects:** Hidden state $h$, feature center $\mu_f$, router row $w_e$, matched expert $a=a(f)$, competitor $b$, expert output $E_e(h)$, route probability $p_e(h)$, loss $\ell(\hat y,y)$.

**Core decomposition:**

$$
h=c+\mu_f+\epsilon.
$$

$$
m_{f,a,b}=(w_a-w_b)^\top\mu_f.
$$

**Mechanism relation:** For a soft mixture,

$$
\hat y=\sum_e p_e(h)E_e(h),
$$

$$
A_e(h,y)=-\langle\nabla_{\hat y}\ell(\hat y,y),E_e(h)-\hat y\rangle.
$$

The soft-router one-step row update is modeled as:

$$
\Delta w_e=\eta\frac{p_e}{\tau}A_eh.
$$

Therefore the predicted margin change is:

$$
\Delta m_{f,a,b}^{pred}
=
\left(\Delta w_a-\Delta w_b\right)^\top\mu_f
\approx
\eta\frac{1}{\tau}\mathbb E[(p_aA_a-p_bA_b)h^\top\mu_f\mid f].
$$

The multi-step budget, used only after the one-step model is validated, is:

$$
\begin{aligned}
m_f(T)&\approx m_f(0)
+\sum_{t<T}\Delta m_f^{signal}(t)
+\sum_{t<T}\Delta m_f^{noise}(t) \\
&\quad +\sum_{t<T}\Delta m_f^{common}(t)
+\sum_{t<T}\Delta m_f^{hidden}(t).
\end{aligned}
$$

**Observable metrics:** sign agreement between $\Delta m^{pred}$ and $\Delta m^{actual}$, correlation or rank correlation, advantage gap distribution, margin p05, matched preserve fraction, sign flip rate, feature NMI as guard, row-norm and load guards.

**Falsifier:** If the computed expert advantage gap does not predict one-step actual route-margin change in frozen-hidden settings, the proposed advantage-based specialization mechanism is not yet a valid router-design basis.

## 5. Computational Realization

**Input objects:** Controlled synthetic hidden states or saved no-position slot-bridge hidden states; feature labels; router rows; expert outputs on hidden states; loss gradients with respect to mixture output; temperature or gate scaling; matched feature-to-expert map.

**Computed variables:** $p_e$, $A_e$, $p_eA_e$, $\Delta w_e^{pred}$, $\Delta w_e^{actual}$, $\Delta m^{pred}$, $\Delta m^{actual}$, row norm change, margin p05, sign flip, matched preserve, feature NMI.

**Algorithm stages:**

1. Freeze hidden states and feature centers.
2. Compute expert outputs and mixture loss gradients.
3. Compute $A_e$ and advantage gap for matched-vs-competitor pairs.
4. Predict one-step row update and margin change.
5. Apply the actual one-step router update under the same differentiable rule or record implementation mismatch.
6. Compare predicted and actual margin change, then run known bad / confusing guards.

**Stage-local evidence:** advantage table, row-update table, margin-prediction table, known-good/bad/confusing guard table, scatter or paired table for $\Delta m^{pred}$ vs $\Delta m^{actual}$.

**Expected artifacts:** `protocol_cn.md`, later English canonical `protocol.md` if moved; post-run `summary.md`, `detailed.md`, `tables/`, and optional central figure after protocol approval.

## 6. Minimal Falsification Tests

| Test | Question | Intervention / comparison | Primary metric | Pass / fail / insufficient | Why it decides | Failure means |
| --- | --- | --- | --- | --- | --- | --- |
| Frozen-hidden advantage-to-margin audit | Does expert advantage predict one-step margin movement? | Compute $\Delta m^{pred}$ from $p_eA_e$, apply one router update with hidden frozen, compare to $\Delta m^{actual}$ | sign agreement and correlation | Pass if prediction is high-sign-agreement and positively correlated; fail if low or reversed; insufficient if actual router gradient path is absent | Directly tests the proposed mechanism relation | Falsifies or supports the mathematical model, not real utility |
| No-utility / shuffled guard | Does the metric create false positives? | identical experts, shuffled matched labels, or no-utility expert outputs | advantage gap and margin change | Pass guard if advantage gap near zero or does not predict matched growth; fail if bad control looks supported | Protects against route-purity false positive | Metric or operationalization is invalid |
| High-NMI confusing guard | Can NMI hide wrong identity? | label-shuffled or crossed-match condition with possible high NMI | matched preserve, margin p05, NMI | Pass guard if matched preserve / margin catches failure even when NMI is high | Keeps preservation metric stricter than NMI | NMI-only reading would be unsafe |

## 7. Current Evidence

**Observation:** Existing A06 evidence supports route-position feature geometry and center initialization in controlled settings, but real-DCLM proxy routing is overwritten by ordinary training. A06_23 shows positive margin must exceed a finite threshold; A06_30 shows no-background full-slot sequences preserve ideal feature routing under long full-LM training, making background / non-feature signal a necessary mechanism candidate.

**Interpretation:** The next uncertainty is no longer whether feature geometry can exist. The next uncertainty is whether training supplies a feature-conditioned advantage signal strong enough to thicken and preserve route margin.

**Boundary:** Current evidence does not prove real semantic experts, common-subtraction method validity, MTP-to-MoE transfer, or neural functional utility. This anchor only opens a mechanism audit.

**Evidence links:**

- `sync/S000_current_specialization/anchors/06_geometry_proxy_preservation/research_map.md`
- `sync/S000_current_specialization/stories/06_geometry_proxy_preservation/story_cn.md`
- `sync/S000_current_specialization/anchors/06_geometry_proxy_preservation/06_23_top1_lockin_margin_threshold_anchor.md`
- `sync/S000_current_specialization/anchors/06_geometry_proxy_preservation/06_30_noise_free_full_slot_preservation_anchor.md`
- `sync/S000_current_specialization/research_lines/07_interference_value_line_cn.md`

## 8. Claim Boundary And Next Decision

**Can claim:** This anchor defines a falsifiable mechanism audit for expert specialization: whether expert advantage predicts one-step route-margin movement under frozen hidden states.

**Cannot claim:** A new router method, deployable gating, real-DCLM transfer, semantic expert identity, expert utility, or that linear routing is sufficient.

**Next decision:** Review and approve the paired protocol `06_33_frozen_hidden_advantage_margin_protocol_cn.md`; if approved, run only the frozen-hidden advantage-to-margin audit before writing any new router method anchor.
