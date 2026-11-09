---
anchor_id: A10_02_frequency_singular_sgd_instability
parent_node: rq.optimizer_learning_rate_mechanism
status: result_updated_boundary_run
created: 2026-07-03
canonical_language: en
source_docs:
  - ../../../../../daily_research_reports/backup/2026/07/0701/docs/design_problem_understanding_revised.md
  - 10_01_common_projected_sgd_lr_anchor.md
---

# 10_02 Frequency-Singular SGD Instability Anchor


## 1. Problem Definition

**Parent problem:** A10 asks why Adam-like methods tolerate larger effective learning rates than SGD in language-model pretraining.

**Sharper subproblem:** Test the 0701 design's first causal chain on a controlled nested-prefix next-token task before proposing a method.

**Decision question:** In a small nested-prefix causal model, does Zipfian frequency produce output-head singular concentration that predicts high-learning-rate SGD instability?

**Not in scope:** Explaining all of Adam, proving SGD-LL or SCALE, proving real-text transfer, proving a final optimizer, or updating the MoE routing-preservation claim.

**Terminology / Definitions:**

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Zipfian nested-prefix data | Short prefixes occur much more often than long extensions | Sample maximum prefix depth from a decreasing distribution over \(A, AB, \ldots, ABCDEFG\) | Token frequencies by target token | Creates controlled common/rare frequency imbalance | Not natural language |
| Singular concentration | Output-head energy is concentrated in a few singular modes | SVD of \(W_{\mathrm{out}}\) and top energy fraction | \(\sum_{i\le k}\sigma_i^2/\sum_i\sigma_i^2\) | Tests whether common learning creates high-gain modes | Not a full Hessian analysis |
| Top spectral-band gradient mass | Fraction of gradient energy inside the current top right-singular subspace | Project output-head gradient onto \(V_{\mathrm{top}}\) | \(B_{\mathrm{top}}(G)=\|G V_{\mathrm{top}}\|_F^2/(\|G\|_F^2+\epsilon)\) | Tests whether updates use the amplified modes | Does not prove causality alone |
| Extra-feature effective rank | Number of independent directions used by prefix extensions | SVD of hidden-state differences between adjacent prefix contexts | \(\operatorname{erank}(E)\) | Tests collapse versus independent extension directions | Does not prove semantic features |
| Instability event | First loss/logit/spectral spike under high LR | First step with non-finite loss or large loss/spectrum jump | Step index | Localizes failure mechanism | Not a theorem about max LR |

## 2. Physical Priors

**P1: Frequency can create coherent common gradients.**  
Meaning: frequent prefix targets such as \(A\) and \(B\) appear in many more examples than rare extensions, so their output-head gradients can align over many updates.  
Could be wrong if: token frequency does not correlate with gradient row norms.

**P2: Common gradients can grow high-gain singular directions.**  
Meaning: repeated coherent updates can increase a small number of output-head singular values.  
Could be wrong if: singular spectrum stays flat or grows only after rare targets are learned.

**P3: High-learning-rate SGD may fail locally, not isotropically.**  
Meaning: the failure should concentrate in token columns or top spectral bands rather than appearing equally in all directions.  
Could be wrong if: instability is distributed uniformly or occurs before top modes form.

## 3. Falsifiable Hypotheses

**H1: Frequency-gradient link.**  
Supported if output-head gradient row norms are positively correlated with target-token frequency during early training.  
Weakened if the correlation is near zero or negative.

**H2: Common-to-spectrum temporal order.**  
Supported if common-prefix accuracy improves before top singular values and top energy grow.  
Weakened if top singular concentration appears without common learning or does not appear at all.

**H3: Instability localization.**  
Supported if high-learning-rate SGD instability occurs after singular concentration and has higher \(B_{\mathrm{top}}(G)\) or token-gradient concentration than stable baselines.  
Weakened if instability appears before singular concentration or has no spectral/token localization.

## 4. Mathematical Model

**Objects:** target token \(y\), hidden state \(h\), output-head matrix \(W_{\mathrm{out}}\in\mathbb{R}^{V\times d}\), output-head gradient \(G\in\mathbb{R}^{V\times d}\), and SVD

\[
W_{\mathrm{out}}=U\Sigma V^\top.
\]

**Readout amplification:**

\[
W_{\mathrm{out}}h=\sum_i \sigma_i \langle h,v_i\rangle u_i.
\]

**Top-band update profile:**

\[
B_{\mathrm{top}}(G)=\frac{\|G V_{\mathrm{top}}\|_F^2}{\|G\|_F^2+\epsilon}.
\]

**Extra-feature rank:**

\[
\operatorname{erank}(E)=\exp\left(-\sum_i p_i\log p_i\right),\quad
p_i=\frac{s_i^2}{\sum_j s_j^2}.
\]

**Mechanism relation:** If Zipfian common gradients create a high-gain subspace, then common accuracy should rise first, top singular energy should grow later, rare extension directions should show nontrivial top-subspace mass, and high-learning-rate SGD failures should be localized in the same top band.

**Falsifier:** no frequency-gradient link, no temporal order, or instability not localized to frequency-shaped or top singular directions.

## 5. Computational Realization

**Input objects:** synthetic Zipfian nested-prefix next-token data; a one-layer one-head causal model; optimizer probes including AdamW, safe SGD, high-learning-rate SGD, output-row clipping, output-row normalization, label smoothing, and spectral clipping.

**Computed variables:** common/rare accuracy, common/rare loss, output-head singular values, top energy, \(B_{\mathrm{top}}(G)\), token-gradient imbalance, frequency-gradient correlation, extra-feature effective rank, extra-feature top-\(k\) mass, and instability step.

**Algorithm stages:** generate nested-prefix batches; train each optimizer probe with matched seeds; log per-step profile; aggregate stability and spectral diagnostics; write summary and detailed evidence.

**Expected artifacts:** `protocol.md`, `summary.md`, `detailed.md`, `tables/condition_summary.csv`, `tables/step_metrics.csv`, and diagnostic figures.

## 6. Minimal Falsification Test

**Test:** A10_02 controlled nested-prefix frequency-singular instability diagnostic.

**Question:** Does frequency-shaped singular concentration predict high-learning-rate SGD instability in the controlled setup?

**Intervention / comparison:** Compare AdamW, safe SGD, high-learning-rate SGD, output-row clipping, output-row normalization, label smoothing, and spectral clipping on the same Zipfian nested-prefix task.

**Primary metric:** Instability-localization profile: the unstable condition must show high \(B_{\mathrm{top}}(G)\) and high token-gradient concentration near the first instability event after common accuracy and top singular energy have already increased.

**Pass / fail / insufficient:** Pass if H1-H3 all hold in the controlled run. Fail if instability is not localized or occurs before spectrum formation. Insufficient if no high-learning-rate condition becomes unstable, or if all probes fail before the model learns the common prefix.

**Why it decides:** The experiment tests the design's causal chain before any optimizer method claim.

**Failure means:** The 0701 frequency-singular operationalization is incomplete for this small model; it does not falsify Adam's advantage or the MoE mainline.

## 7. Current Evidence

**Observation:** The 0701 design articulates a causal chain from Zipfian frequency to common-feature gradient coherence, singular-value growth, gradient amplification, and high-learning-rate SGD instability.

**Interpretation:** This is a clear problem-understanding anchor, not yet evidence that the chain holds.

**Boundary:** The claim is optimizer-line diagnostic only; it does not update the current nested learning / MoE gating preservation claim.

**Evidence links:** `../../../../../daily_research_reports/backup/2026/07/0701/docs/design_problem_understanding_revised.md`; `10_01_common_projected_sgd_lr_anchor.md`.

**Observation:** A10_02 main local boundary run (`high_lr=0.9`, seeds `0,1,2`) did not produce a qualifying late instability event, but `sgd_high_ce` showed rare-prefix suppression: rare accuracy `0.4335`, common accuracy `0.8949`, top-SV growth `3.6756`, top-2 energy `0.6622`, top-band gradient mass `0.5564`, extra-feature effective rank `2.4621`, and extra top-2 mass `0.4721`.

**Interpretation:** This supports a narrower mechanism: high SGD learning rate can push rare prefix extensions into a lower-rank, more top-subspace-dependent regime before clean divergence appears.

**Boundary:** This is controlled synthetic evidence for rare suppression, not proof of real-LM high-LR divergence.

**Evidence links:** `../../experiments/A10/A10_02_frequency_singular_sgd_instability/summary.md`; `../../experiments/A10/A10_02_frequency_singular_sgd_instability/detailed.md`.

**Observation:** Row clipping and row normalization rescued the main boundary run: both reached rare accuracy `1.0000`; row clipping reduced top-band gradient mass to `0.2130` and extra top-2 mass to `0.2584`; row normalization reduced token-gradient concentration and extra top-2 mass to `0.2436`.

**Interpretation:** Output-row scale control is a useful causal probe for the rare-suppression regime.

**Boundary:** This does not establish row clipping or row normalization as final optimizers.

**Evidence links:** `../../experiments/A10/A10_02_frequency_singular_sgd_instability/tables/local_full_condition_summary.csv`.

**Observation:** The remote SCO stress run (`pt-c6a1nhsr`, `high_lr=2.0`) succeeded and produced early spectral blow-up: `sgd_high_ce` stable rate `0.0000`, mean instability step `12.33`, top-SV growth `3248.10`, top-2 energy `0.9955`, top-band gradient mass `0.9450`, and rare accuracy `0.0000`.

**Interpretation:** Very high SGD LR can create early spectral divergence, but this is too aggressive to prove the full temporal chain from common learning to late instability.

**Boundary:** Stress-run evidence is auxiliary and should not replace the calibrated boundary result.

**Evidence links:** `../../experiments/A10/A10_02_frequency_singular_sgd_instability/tables/remote_stress_condition_summary.csv`; `../../experiments/A10/A10_02_frequency_singular_sgd_instability/logs/acp/full_sco_20260703_033834_runtime_20260703_033917.log`.

## 8. Claim Boundary And Next Decision

**Can claim:** In this controlled nested-prefix task, high-LR SGD can enter a rare-suppression regime associated with stronger output-head spectral concentration, higher top-band gradient mass, lower extra-feature effective rank, and higher extra top-2 mass. Row clipping, row normalization, and label smoothing rescue rare learning in the calibrated boundary run.

**Cannot claim:** The run does not prove that high-LR SGD divergence in real LMs is caused by frequency-driven singular amplification. It does not explain all of Adam, prove a final optimizer, or update MoE routing preservation.

**Next decision:** Run an LR/noise boundary map: noiseless full-batch, noisy full-batch, and noisy mini-batch. The decision target is the transition from stable learning to rare suppression to spectral divergence.
