# A17_02: Fixed-Pool Frequency And Shared Learning

[中文](17_02_fixed_pool_frequency_anchor_cn.md) · [A17](../README.md)

Problem key: `fixed_pool_frequency_shared_learning`. On 2026-10-10 Asia/Shanghai, the researcher activated an independent frequency Anchor/Protocol, selected direct final Attention `o_proj` updates as the main learner, retained LoRA as the preceding capacity control, and authorized Smoke → Full with ongoing supervision. Numerical mechanism interpretation and question closure remain researcher-owned.

`question_state=HUMAN_CONFIRMED`; `design_state=USER_ADOPTED_FROZEN_IMPLEMENTATION`; `result_state=MEASURED_STATISTICAL_BRANCH`; `task_state=FULL_COMPLETED`.

## 1. Problem Definition

With B's 200 presentations fixed, does increasing A from 200 to 800 presentations change B's held-out answer loss differently when A follows B's rule versus another visible rule? FIRST returns a list's first item; LAST its last item. Both instructions are shown and simultaneously satisfiable. Frequency means a fixed number of presentations of the same pool, not more unique content.

The parent direction is to explain helpful or harmful learning through shared parameters under finite resources. This experiment tests an interaction between presentation policy and rule relation, not an intrinsic logical contradiction. A separate equal-total-answer comparison measures allocation. A registered positive or negative interaction motivates a directional mechanism audit; a bounded practical absence limits this mechanism in this carrier. Incomplete or unresolved evidence leaves the answer unknown. Representation and architecture utility are separate downstream questions.

## 2. Physical Priors

Working hypothesis, not established mechanism: extra same-rule A may supply reusable practice, while different-rule A may demand a different selection operation. A credible rival is that extra examples only strengthen vocabulary/list handling or expose an initial FIRST/LAST difficulty. Both B roles are therefore tested, using disjoint but identically generated pools and exact answer/position marginals. The final projection restriction conditions every conclusion on the capacity of this learner; it does not establish unrestricted models must conflict.

## 3. Falsifiable Hypotheses

The registered two-sided hypothesis is a practically nonzero median interaction across independent training seeds. The rival predicts an interaction within ±0.01 nat per answer. Positive interaction means the different-minus-same loss gap grows with A presentations; it need not mean different-rule training causes net harm. B-only controls separately measure net added-training consequences. Equal-budget controls separate an allocation question from fixed-B addition.

## 4. Mathematical Model

The model predicts one correct answer token from a visible rule/list prefix. Loss is full-vocabulary cross-entropy in nats per answer. Let \(L_{s,r,n,p}^{q}\) be mean B loss for seed s, B rule r, A count n, novelty panel p, and relation q∈{same,different}, after exactly 200 B presentations. The seed-level primary is

\[
I_s=\frac{1}{4}\sum_{r\in\{\mathrm{FIRST},\mathrm{LAST}\}}\sum_{p\in\{\mathrm{order},\mathrm{combination}\}}\left[(L_{s,r,800,p}^{\mathrm{different}}-L_{s,r,800,p}^{\mathrm{same}})-(L_{s,r,200,p}^{\mathrm{different}}-L_{s,r,200,p}^{\mathrm{same}})\right].
\]

The target is the seed-distribution median of I, conditional on this pretrained parent, dataset construction, trainable matrix and optimizer. Each I is derived from four completed policy trajectories per B role; it is not a gradient identity or causal decomposition of functions. The threshold δ=0.01 is an adopted practical convention. Fixed-B policies have unequal total training answers; equal-budget 800A/200B versus 500A/500B policies have unequal B opportunities. Neither comparison holds both facts fixed.

## 5. Computational Realization

Construct new A/B pools of 200 different ordered lists each from 20 qualified one-token Chinese answers. Their unordered content groups are disjoint. Cyclic word shifts balance every position and answer exactly. Both rules use the same lists/templates; A/B metadata stays outside model prompts. All conditions reset the original Qwen3-0.6B Base and update only layer27 Attention `o_proj`, with a common constant learning rate and 20 valid answers per update. No rule-specific adapter or expert is added.

For each B rule, same/different A are each presented 200 or 800 times with B200; add B-only and same/different 500A/500B. Order-new uses unseen orders of B-seen groups; combination-new uses groups absent from all actual training. Both are reported separately and equally combined. Three exploratory seeds use dev. Six new confirmation seeds use unopened model test after frozen engineering gates; dev cannot select the confirmation conditions or learning rate.

## 6. Minimal Falsification Tests

Data must pass oracle, exact continuation, disjointness, balance and actual-training-relative novelty checks. Smoke must pass finite answer-normalized telemetry, constant-LR/counts, exact frozen bytes, checkpoint identity, no-op precision and an independent-process restore/next-step comparison before Full.

Exploration is descriptive. Confirmation uses the sole combined seed primary: all six I above +δ or below −δ meets the frozen conservative two-sided sign rule (p=0.03125). The [min,max] seed interval has at least 96.875% median coverage under independent identically generated seed effects. An interval inside [−δ,δ] supports a bounded practical absence; crossing a relevant threshold or a failed engineering gate is insufficient. Subpanels cannot rescue the primary. Effective A learning is required only for a separately claimed local learning mechanism, not for valid policy estimates.

## 7. Current Evidence

Frequency Smoke56/56 engineering checks passed. Full pt-ho4byzg4 completed126 trajectories,90,000 answers,4500 updates; engineering1520/1520 and actual-exposure qualification126/126 passed, platformSUCCEEDED. All126 actual saved families were verified and registered. Six independent confirmation seed primaries exceedδ=.01; median0.066142 nat/answer, conservative interval[0.051485,0.078583], frozen two-sidedp=.03125, branchREGISTERED_POSITIVE_MEDIAN_INTERACTION.

Same-rule extra practice has a larger incremental answer-CE benefit. All96 extra-practice componentCE differences versusB-only are negative, including different-rule additions; no netCE interference is demonstrated. Accuracy need not improve withCE: diff800 combined median83.2500% versusB-only83.4375%. Equal-budget allocation is reported separately. Mechanism, functional partition, architecture utility and question closure remain researcherUnknown. [Complete result](../../../experiments/A17/17_02_fixed_pool_frequency/A17_02_E01_fixed_pool_frequency/summary.md).

## 8. Claim Boundary And Next Decision

An eligible result concerns conditional-rule presentation policies for this Base, two fixed pools and restricted optimizer. It cannot establish expert necessity, a full functional partition, natural-corpus frequency mechanisms or long-term architecture benefit. Combined evidence and all role/novelty disagreements must be preserved. The next researcher decision is whether the frozen median interaction and separate net/allocation effects justify further mechanism analysis; the AI completes factual records without adopting that judgment.

[Frequency Focus](../../../focus/focus_fixed_pool_frequency_shared_learning.md) · [Protocol](../../../experiments/A17/17_02_fixed_pool_frequency/A17_02_E01_fixed_pool_frequency/protocol.md) · [Parent Anchor](../17_01_controlled_list_prediction_rules/17_01_controlled_list_prediction_rules_anchor.md)
