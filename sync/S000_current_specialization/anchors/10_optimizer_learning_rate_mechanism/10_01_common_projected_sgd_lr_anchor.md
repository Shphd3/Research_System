# 10_01 Common-Projected SGD Learning-Rate Anchor

Thinking Card source: [10_01_common_projected_sgd_lr_thinking_card.md](10_01_common_projected_sgd_lr_thinking_card.md)

## 1. Problem Definition

**Parent problem:** The seminar optimizer line asks why Adam and related methods can support much larger effective learning rates, and whether this advantage is tied to common or high-gain directions.

**Sharper subproblem:** Test first in a minimal controlled output-head setting whether a common gradient component limits the stable learning rate of SGD-style updates.

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Common direction | A hidden direction shared by many batch examples | $u=\mathrm{mean}(h_i)/\|\mathrm{mean}(h_i)\|$ | Unit vector | Defines the input-side direction removed from the gradient | Not the unique real-LLM common operator |
| Common gradient | Output gradient along the common direction | $G_c=uu^\top G$ | Gradient matrix | Candidate loud-direction bottleneck | Not all instability sources |
| Common-projected gradient | Gradient after removing the common direction | $G_r=(I-uu^\top)G$ | Gradient matrix | Tests whether removing common raises stable LR | Not a final optimizer |
| Critical learning rate | Largest learning rate stable in a fixed window | $\eta_{\mathrm{crit}}$ | Scalar | Primary decision metric | Does not prove generalization |
| Rare-token loss | Cross-entropy on low-frequency token classes | Rare-subset evaluation CE | Loss | Guards against stability at the cost of rare learning | Not semantic rare features |

**Decision question:** In a synthetic output-head task, does removing the batch common gradient significantly increase SGD's critical learning rate without worsening rare-token learning?

**Not in scope:** Explaining all of Adam, comparing all optimizers, proving Nesterov, or updating the MoE routing-preservation claim.

## 2. Physical Priors

**P1:** Output-head gradients can separate into common and token-specific components.  
**Meaning:** Frequent tokens repeatedly write into shared directions, making them loud update directions.  
**Could be wrong if:** The common direction is unstable or unrelated to token frequency.

**P2:** High-learning-rate SGD may fail first along loud directions rather than failing isotropically.  
**Meaning:** A single global learning rate must satisfy the most unstable direction, so a common loud direction can lower the usable learning rate.  
**Could be wrong if:** Instability is mainly from Hessian curvature, batch noise, normalization layers, or attention dynamics.

**P3:** Removing common signal must be checked against rare-token learning.  
**Meaning:** If rare tokens also need the common direction, projection may improve stability but damage learning.  
**Could be wrong if:** Rare-token learning is mostly common-direction dependent.

## 3. Falsifiable Hypotheses

**H1:** Common-projected SGD increases the critical learning rate.  
**Supported if:** $\eta_{\mathrm{crit}}(\mathrm{projected}) / \eta_{\mathrm{crit}}(\mathrm{vanilla}) \ge 3$ and norm-matched SGD does not explain the improvement.  
**Weakened if:** The increase is below 1.5x, or norm-matched / random-projected controls match it.

**H2:** Common projection does not sacrifice rare-token learning.  
**Supported if:** Near each method's critical learning rate, projected SGD has no worse rare-token evaluation loss than vanilla SGD and does not reduce rare update share.  
**Weakened if:** Stability improves but rare loss worsens materially.

## 4. Mathematical Model

**Objects:** Fixed hidden states $h_i\in\mathbb{R}^d$, output-head gradient $G\in\mathbb{R}^{d\times V}$, target token $y_i$, and error vector $e_i=p_i-\mathrm{onehot}(y_i)$.

**Core decomposition:**

$$
G=\frac{1}{B}\sum_i h_i e_i^\top
$$

$$
u=\frac{\mathrm{mean}_i(h_i)}{\|\mathrm{mean}_i(h_i)\|}
$$

$$
G_c=uu^\top G,\qquad G_r=(I-uu^\top)G
$$

**Mechanism relation:** If the common direction is the limiting large-learning-rate direction, removing $G_c$ should increase the stable learning-rate ceiling. If the increase is only gradient-norm shrinkage, norm-matched SGD should show the same increase.

**Observable metrics:** $\eta_{\mathrm{crit}}$ ratio, rare-token loss, rare-token update share, $\|G_c\|_F/\|G\|_F$, and top singular energy.

**Falsifier:** Common-projected SGD does not increase $\eta_{\mathrm{crit}}$ beyond norm-matched control, or it increases stability while materially worsening rare-token loss.

## 5. Computational Realization

**Input objects:** Synthetic hidden-token data; a fixed output-head training task; vanilla SGD, common-projected SGD, norm-matched SGD, and random-projected SGD.

**Computed variables:** $G_c$, $G_r$, critical learning rate, frequent/rare losses, per-token update norm, and common energy ratio.

**Algorithm stages:** Construct hidden data with a common direction; train only the output head; sweep learning rates; classify stable windows; compare projected and control updates.

**Stage-local evidence:** Learning-rate stability curve, rare-vs-frequent loss curve, common/residual energy trajectory, and control comparison table.

**Expected artifacts:** `protocol_cn.md` approval draft, approved `protocol.md`, `summary.md`, `detailed.md`, one stability figure, one rare-loss figure, and one main result table.

## 6. Minimal Falsification Test

**Test:** Synthetic output-head common-projected SGD critical-learning-rate audit.

**Question:** Is the common gradient alone sufficient to lower SGD's critical learning rate?

**Intervention / comparison:** On synthetic data $h=\alpha_c c+\alpha_y z_y+\epsilon$, compare vanilla SGD, common-projected SGD, norm-matched SGD, and random-projected SGD.

**Primary metric:** $\eta_{\mathrm{crit}}(\mathrm{common\text{-}projected})/\eta_{\mathrm{crit}}(\mathrm{vanilla})$.

**Pass / fail / insufficient:** Pass if the ratio is at least 3 and controls do not explain it. Fail if the ratio is at most 1.5 or norm/random controls match it. Insufficient if projected SGD is stable but rare loss collapses, or if the synthetic common direction is not present.

**Why it decides:** This test first decides whether the common-gradient LR bottleneck exists in a controlled setting. Only then is it worth connecting to small-real LM, Adam, or Nesterov diagnostics.

**Failure means:** Failure weakens this common-gradient operationalization. It does not falsify Adam/Nesterov explanations or the MoE mainline.

## 7. Current Evidence

**Observation:** The seminar prompt records that Adam's effective learning rate is much larger than SGD's and that large-learning-rate SGD failures are associated with layer-wise spikes, output-layer per-token-class imbalance, and frequent-token gradient dominance.

**Interpretation:** These observations motivate a common/frequent loud-direction mechanism, but they do not prove that common projection raises the critical learning rate.

**Boundary:** This anchor is part of the seminar optimizer line. It does not update the feature-level MoE specialization claim.

**Evidence links:** `daily_research_reports/0701/prompts/0701_seminar_questions_next_conversation_prompt_cn.md`; `daily_research_reports/0701/docs/design_problem_understanding_revised.md`; seminar screenshots referenced there.

## 8. Claim Boundary And Next Decision

**Can claim:** This anchor tests whether common-gradient projection raises the stable learning rate of SGD in a synthetic output-head setting.

**Cannot claim:** It cannot explain all of Adam, prove Nesterov, prove real-LM transfer, or explain MoE routing preservation.

**Next decision:** Approve and run the synthetic protocol. Only if the synthetic test passes should we design small-real LM / Adam / Nesterov follow-ups.
