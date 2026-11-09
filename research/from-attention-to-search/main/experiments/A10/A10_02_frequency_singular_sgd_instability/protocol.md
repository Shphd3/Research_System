# A10_02 Frequency-Singular SGD Instability Protocol

## 0. Approval Snapshot

Approval status:
Approved by the user in the 2026-07-03 chat for immediate execution, including local execution and remote/SCO execution if available.

Anchor:
`Projects/from-attention-to-search/main/problem_anchors/10_optimizer_learning_rate_mechanism/10_02_frequency_singular_sgd_instability_anchor.md`

Decision question:
In a small nested-prefix causal model, does Zipfian frequency produce output-head singular concentration that predicts high-learning-rate SGD instability?

Physical prior tested:
Frequent common prefixes create coherent gradients, coherent gradients grow high-gain singular modes, and high LR SGD fails locally along those modes.

Primary metric:
Instability-localization profile: high-learning-rate SGD must fail after common learning and singular concentration, with elevated top spectral-band gradient mass \(B_{\mathrm{top}}(G)\) or token-gradient concentration.

Falsifier:
Instability occurs before common learning or singular concentration, or instability is not localized in the top spectral band or token columns.

Claim boundary:
Controlled synthetic nested-prefix task only. No real-text, full Adam explanation, final optimizer, or MoE routing-preservation claim.

## 1. Purpose

This protocol operationalizes the 0701 design as a diagnostic experiment. The goal is not to rank optimizers by final validation loss. The goal is to test which geometric quantities predict high-learning-rate SGD instability.

## 2. Data

Use nested-prefix next-token sequences:

\[
A\to AB\to ABC\to ABCD\to ABCDE\to ABCDEF\to ABCDEFG.
\]

Each example samples a maximum prefix depth from a Zipfian distribution. Training labels are the next token at each available prefix position. Therefore early tokens such as \(A\) and \(B\) are common, while later tokens such as \(F\) and \(G\) are rare.

Guard:
The implementation records the realized target-token frequencies. The current run does not claim natural-language transfer.

## 3. Model

Use a one-layer, one-head causal next-token model with token embeddings, position embeddings, causal attention, a small feed-forward block, and an output head. Hidden dimension is small enough for full SVD logging.

Default local configuration:

| Field | Value |
| --- | --- |
| hidden dimension | 32 |
| maximum prefix depth | 7 |
| batch size | 192 |
| steps | 240 |
| seeds | 0, 1, 2 |
| logging interval | 5 steps |

## 4. Conditions

| Condition | Role | Learning-rate role |
| --- | --- | --- |
| `adamw_ce` | stable adaptive baseline | standard CE AdamW |
| `sgd_safe_ce` | safe SGD baseline | lower LR SGD |
| `sgd_high_ce` | instability probe | high LR SGD |
| `sgd_high_row_clip` | SGD-LL-style probe | high LR with output-row gradient clipping |
| `sgd_high_row_norm` | SCALE-like probe | high LR with output-row gradient normalization |
| `sgd_high_label_smoothing` | margin-pressure probe | high LR with label smoothing |
| `sgd_high_spectral_clip` | direct spectral probe | high LR with output-head singular-value cap |

## 5. Metrics

Primary metric:
`instability_localization`: first instability step, \(B_{\mathrm{top}}(G)\) near that step, token-gradient concentration near that step, and whether common learning plus singular concentration preceded the event.

Secondary metrics:
`common_accuracy`, `rare_accuracy`, `top_singular_value`, `top_energy_fraction`, `frequency_gradient_correlation`, `token_gradient_imbalance`, `extra_feature_effective_rank`, `extra_feature_top2_mass`, `final_eval_loss`, and `stable`.

Metric definitions:

\[
B_{\mathrm{top}}(G)=\frac{\|G V_{\mathrm{top}}\|_F^2}{\|G\|_F^2+\epsilon}.
\]

\[
\operatorname{erank}(E)=\exp\left(-\sum_i p_i\log p_i\right),\quad
p_i=\frac{s_i^2}{\sum_j s_j^2}.
\]

## 6. Pass / Fail / Insufficient Rules

Support the mechanism if all are true:

1. Frequency-gradient link: early output-head gradient row norms correlate positively with realized target-token frequency.
2. Temporal order: common accuracy rises before top singular value / top energy rises.
3. Localization: high LR SGD instability occurs after that rise and has higher \(B_{\mathrm{top}}(G)\) or token-gradient concentration than stable baselines.

Weaken the mechanism if:
Instability is not localized, occurs before common learning, or top singular concentration does not appear.

Insufficient evidence if:
No high-LR condition becomes unstable, all high-LR conditions fail before common learning, or the Zipfian frequency imbalance is not present.

## 7. Planned Outputs

Tables:
`tables/step_metrics.csv`, `tables/condition_summary.csv`, `tables/final_by_seed.csv`.

Figures:
`figures/temporal_profile.png`, `figures/stability_by_condition.png`, `figures/spectral_localization.png`, `figures/extra_feature_geometry.png`.

Reports:
`summary.md`, `detailed.md`, and an evidence update in the anchor.

## 8. Remote Execution Note

The local workspace has the SCO binary under `/root/.sco/bin/sco`. If SCO workspace and image settings are usable, the same script may be submitted through an ACP job. If remote submission fails, the local run remains the decision artifact and the failure reason must be recorded in `detailed.md`.
