# A17_01_01: Rule-conditioned answer margin

[中文](17_01_01_rule_conditioned_answer_margin_anchor_cn.md)

Parent problem_key: `list_rule_shared_update`. This subordinate Anchor formalizes one E03 diagnostic, not a new Focus or fourth core experiment. The parent Anchor owns the shared-learning question and adopted direct-projection learner. The researcher accepted paired-rule answer-margin analysis and authorized sub Anchor, sub Protocol and execution on four H100 reserved GPUs on 2026-10-10. Operational settings are delegated. Mechanism judgment remains `Unknown`.

## 1. Problem Definition

When a FIRST update lowers independent LAST answer loss, does it also improve the correct LAST answer relative to the answer that FIRST would select? Ask the reverse direction separately. Distinguish local answer selection from a general increase in probability assigned to the answer vocabulary. The same three-word list receives both visible instructions; both targets are therefore jointly satisfiable. The parent seeks useful versus harmful shared learning; this check resolves whether its observed loss help reaches this relative choice. Support permits that narrower reading; non-support stops it; insufficient evidence leaves it open.

## 2. Physical Priors

A conditional model can distinguish the two instructions. This is task solvability, not evidence of actual rule use. For a fixed prefix, a log-probability difference equals the corresponding logit difference because the common softmax normalizer cancels. A uniform logit increase for all 20 answer words can lower answer loss without changing their relative margins. These algebraic facts motivate the diagnostic; they do not establish any internal decomposition. No assumption about expert separation, feature meaning or parameter orthogonality is needed.

## 3. Falsifiable Hypotheses

H1: an effective source-rule update that helps the other rule's loss also increases that recipient's correct-versus-other-rule answer margin. Rival R1: loss help comes from changes outside this relative choice, including answer-pool mass. Rival R2: a content-position bias changes both prompts similarly, without greater instruction-conditioned separation. Rival R3: the two-word margin improves while the middle word or another vocabulary item remains preferred. Mixed, unresolved or ineffective updates remain insufficient for stable transfer. These are exposed-development diagnostics, not blind confirmation.

## 4. Mathematical Model

Let a list be \(L=(w_1,w_2,w_3)\), with distinct one-token answer words. Let \(x_A=T(\mathrm{FIRST},L)\), \(x_B=T(\mathrm{LAST},L)\); the prefixes end before the answer. The model's answer logit is \(z_\theta(w\mid x)\) and loss is \(\ell=-\log p_\theta(y\mid x)\), in nats per answer.

\[
m_A(\theta,L)=\log p_\theta(w_1\mid x_A)-\log p_\theta(w_3\mid x_A)
=z_\theta(w_1\mid x_A)-z_\theta(w_3\mid x_A),
\]
\[
m_B(\theta,L)=\log p_\theta(w_3\mid x_B)-\log p_\theta(w_1\mid x_B),\qquad S(\theta,L)=m_A+m_B.
\]

For one saved actual source update \(\Delta W_s\), restore the exact parent \(W\) and read both endpoints. The local treatment effect on recipient B is

\[
\tau_{A\to B}=\overline{m_B(W+\Delta W_A,L)-m_B(W,L)}.
\]

The averaging set is fixed and independent of source content groups. Reverse A/B for the other direction. \(\Delta S=\Delta m_A+\Delta m_B\). An identical additive change to the last-versus-first logit difference under both prompts cancels in \(\Delta S\); other nonlinear position-bias explanations are not universally excluded. Positive \(\tau\) identifies a local relative-prediction effect of the specified parameter intervention, not a unique internal rule mechanism or population-wide causal transfer.

Also measure correct-minus-best-other-list-word margin, list-restricted top-1, full-vocabulary top-1, answer CE, 20-word conditional CE and log answer-pool probability. With pool \(V_{20}\), \(\ell=\ell_{20}-\log P(V_{20}\mid x)\). This exact identity distinguishes pool mass from within-pool discrimination without assuming either is the only cause.

## 5. Computational Realization

Goal: read the previously observed effects with a diagnostic that cancels shared probability normalization. How: replay saved strict actual matrices through the complete FP32 Qwen3-0.6B Base model, modifying only layer27 Attention `o_proj`; all other weights are frozen. Why: the same parent and perturbation permit paired comparisons without changing training history or re-estimating gradients.

Use saved initial, early and terminal states of the adopted learner, deduplicating the shared Base. Use selection-v2 heldout development pairs and existing source updates whose content groups are independent of recipient groups. No test access, new data selection, LM training or SAE training. The primary descriptive comparison is early-state transfer in both directions across three training seeds; additional batches and update sizes are sensitivity views. Repeated batches are not independent seeds. Report nominal order-new/combination-new panels, actual exposure reclassified from training ledgers, and combined. [Sub Protocol](../../../../experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E03_restricted_update_full/subprotocols/paired_rule_margin/protocol.md) owns exact replay coverage and decision aggregation.

## 6. Minimal Falsification Tests

Engineering admission: seven exact checkpoints, 280 finite matrices, complete paired lists, no source/recipient group overlap, exact checkpoint ledger, finite logits, deterministic no-op, exact matrix replay/restore and unchanged frozen weights. Four independent GPU Smoke readers must pass before Full. Failure stops the run and preserves failure evidence.

Qualify each source update by lower independent own-rule CE beyond measured numerical resolution; qualify recipient help likewise. Then classify its recipient margin as improved, worsened or unresolved. Resolution is max(1e-6,10×repeat drift), an engineering threshold, not a scientific effect-size requirement. Positive mean must be accompanied by individual batch and seed values. Consistent positive effects in all six primary seed×direction cells and their three source batches allow only descriptive local pair-margin support. Loss help with unresolved/worse margin challenges the inference from loss help to relative selection; failed source qualification or mixed signs yields insufficient/heterogeneous evidence. No significance test or population confidence interval is claimed from three seeds.

## 7. Current Evidence

Paired analysis complete:7states/280conditions. Primary early slice:18/18source-effective and recipient-CE-helping,but12/18recipient pair margins improve and6 worsen;S improves18/18,mean+0.003115. Frozen consistency criterion unmet. Actual local prediction effects are measured;stable relative-choice transfer remains insufficient. Exposed dev,three training seeds;scientific mechanism/closure Unknown. AI-proposed bounded interpretation and lineage in [Summary](../../../../experiments/A17/17_01_controlled_list_prediction_rules/A17_01_E03_restricted_update_full/subprotocols/paired_rule_margin/summary.md).

## 8. Claim Boundary And Next Decision

Allowed: the specified actual update locally changed a heldout pair's relative prediction at the saved model state, with separate source qualification and numerical checks. Not established: general rule reasoning, natural-text pretraining benefit, a common/unique module partition, expert necessity, SAE feature causality, or architecture superiority. The researcher owns whether the observed bounded answer is sufficient and what comes next. Execution completion is separate from scientific closure.
