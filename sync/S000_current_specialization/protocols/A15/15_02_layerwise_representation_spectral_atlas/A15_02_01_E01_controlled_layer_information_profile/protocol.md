---
experiment_id: A15_02_01_E01_controlled_layer_information_profile
anchor_id: 15_02_01_controlled_layer_information_identity
status: approved_for_smoke_and_full
approved_by: user
approval_date: 2026-07-31
canonical_language: en
---

# Protocol: Layer x Band x Information Profile In A Four-Layer MoE

## 0. Approval And Decision

The user explicitly authorized dataset construction, capability-gated training, sealed testing, two independent runs per model, and comparison. Implementation must pass smoke before full execution.

## 1. Decision Question

In a capability-valid four-layer MoE, does the same relative covariance band carry different coarse, intermediate, and composed information at different depths?

## 2. Hypothesis And Rivals

- **H1:** the composition objective creates a layer-band readability increment for the intermediate or composed result beyond equal-dimensional random directions.
- **R0:** arbitrary equal-dimensional views are equally readable, reproducing the saturated old pilot.
- **R1:** depth effects reflect output proximity and occur in the matched one-step model.
- **R2:** the model memorizes seen $(a,b)$ pairs instead of recombining components.

## 3. Controlled Dataset

Use $\mathbb Z_{17}$ with $m=(x+a)\bmod17$ and $y=(m+b)\bmod17$. Each input contains a query token, shared shift $a$, value $x$, independent context, shared shift $b$, and ROOT. Eight shifts form an $8\times8$ grid. Final-query training excludes an eight-pair perfect matching while mid queries cover every pair.

Context IDs are disjoint: train 0--15; validation 16--19; covariance calibration 20--23; probe fit 24--25; probe validation 26--27; sealed test 28--31.

| Condition | Mid query | Final query |
| --- | --- | --- |
| one-step control | $m$ | $m$ |
| composition | $m$ | $y$ |

Inputs are identical; only final-query supervision changes.

## 4. Dataset Gates

Require disjoint split hashes, a perfect-matching holdout, complete atomic coverage, exactly balanced answer marginals, perfect oracle accuracy, no answer token in the input, near-chance oracle after shuffling a functional token, and unseen-pair accuracy at most 0.20 for a no-interaction additive one-hot linear shortcut.

## 5. Model

Use a four-layer pre-norm causal Transformer-MoE: width 256, eight attention heads, eight top-1 experts per layer, expert width 512, GELU, sequence length six. The Gate receives the actual MoE-normalized state. Selected softmax probability multiplies expert output to preserve the Gate gradient path. There is no shared expert, capacity drop, or load-balancing auxiliary loss. Every run shares a non-gradient load-free score bias, which is excluded from Gate-weight spectral metrics.

Add a training-only intermediate readout at the layer-2 ROOT state for $m=(x+a)\bmod17$; layer 4 still predicts the condition's registered final target. Training loss is final-target cross entropy plus an equally weighted layer-2 intermediate-state cross entropy. The auxiliary head never receives a held-out composed answer and is not part of the spectral-profile primary metric.

Train conditions with seeds 17 and 29, giving four independent models. Same-seed initialization, data order, and optimizer are paired.

## 6. Preflight And Training

Keep sealed test unopened. Calibration seed 1001 selects the first validation-capable entry from: 2,000 steps at $10^{-3}$; 3,500 steps at $10^{-3}$; 5,000 steps at $5\times10^{-4}$. If all fail, stop and amend the Protocol without opening test.

Formal training uses AdamW, betas (0.9,0.95), weight decay 0.01, 100-step warmup, cosine decay, global batch 512, and gradient clip 1.0. Select the earliest checkpoint passing validation for three consecutive evaluations.

**Pre-test amendment, 2026-07-31:** the first preflight showed that the original non-gradient load-free bias update rate 0.01 with clip 1.0 remained clipped from roughly step 400 onward. This violated the registered no-saturation guard even when capability approached the threshold. Sealed test was never opened. Hold the dataset, model, optimizer, capability thresholds, and schedule ladder fixed; change only the shared bias update rate to 0.003 and clip to 4.0. In a validation-only seed-1001 check at the 2,000-step entry, control passed at step 900 and composition at step 1,400. Composition unseen-pair accuracy was 0.897, NLL 0.615, seen-unseen gap 0.103, recent maximum expert share 0.372, and maximum absolute bias 1.130 without saturation. The amended configuration must repeat full preflight and eight-GPU smoke; the earlier smoke remains engineering provenance and does not authorize full execution.

**Capability amendment, 2026-07-31:** the first amended four-model full was stopped before sealed test because both control seeds passed but composition seeds 17/29 had validation unseen-pair accuracy 0.711/0.871 and NLL 2.277/0.909. Load remained valid, so the generic model could still memorize seen pairs without robustly learning a recomposable two-step computation. Keep inputs, held-out combinations, four-layer MoE, formal seeds, primary metric, and all existing thresholds fixed. Add the equally weighted layer-2 intermediate-state supervision above, plus a layer-2 unseen-pair $m$ capability gate of accuracy at least 0.95 and NLL at most 0.20. This exposes the probability tree's known intermediate state, never the held-out $y$ answer. Repeat data audit, tests, mini-run, independent validation preflight, eight-GPU smoke, and full; retain the earlier full as `insufficient_composition_capability`.

## 7. Capability Gates

All four models require unseen-pair mid accuracy at least 0.95 and NLL at most 0.20. Control final requires the same. Composition final unseen-pair accuracy must be at least 0.80, NLL at most 0.75, and seen-unseen gap at most 0.15. Every layer must keep recent maximum expert share at most 0.65, use every expert, and avoid bias saturation. Open sealed test once after checkpoint selection.

The layer-2 intermediate head must additionally reach unseen-final-pair $m$ accuracy at least 0.95 and NLL at most 0.20. This validates the first-step computation; it is not evidence that any covariance band is specific.

## 8. Spectral Profile

Fit each layer's covariance basis on the actual ROOT Gate input using calibration only. Split-half projector overlap must exceed the q95 of 256 equal-dimensional random controls.

Use eight 32-dimensional fine bands and aggregate H=`F1`, M=`F2--F4`, T=`F5--F8`. Probe standardization and hyperparameters use fit/validation only.

## 9. Primary Metric

For $q\in\{a,m,y\}$, fit ridge linear probes with $n\in\{32,64,128,256\}$ examples and average sealed-test accuracy across these sample sizes to obtain $A_{\ell,B,q}$. This measures how sample-efficiently a low-capacity reader extracts the variable.

Compare each real band with 64 equal-dimensional Haar directions:

$$S_{\ell,B,q}=A_{\ell,B,q}-Q_{0.95}(A_{\ell,R_{d_B},q}).$$

The objective increment is $\Gamma=S^{compose}-S^{control}$. Report full-state upper bounds, initialization, and each seed.

## 10. Secondary Causal-Use Audit

On sealed final queries, remove a real band's contribution only from one layer's Gate logits while leaving expert input native. Measure answer NLL, route flips, and margin changes; repeat for 64 matched random directions. This tests current Router use, not training utility.

## 11. Statistics

Random q95 controls directional chance. Use 2,000 paired bootstraps over held-out component combinations. Seeds are replication, not independent sample inflation. Call a cell specific only when both seeds have $S>0$ and the pooled 95% lower bound is positive; call an identity change only when $\Gamma$ agrees across seeds.

## 12. Execution Contract

Run data generation, unit tests, mini-run, and submission dry-run locally. ACP uses one `5090-8-spot` node: workspace `share-space`, AEC2 `computing-cluster-5090-01g`, spec `n12lp.nn.i10a.8`, quota `spot`. Smoke checks eight GPUs, process grouping, Gate gradients, non-gradient bias, actual-input replay, hashes, checkpoint/resume, and analysis closure. Full runs four models in parallel; only capability-valid models enter sealed profile inference.

## 13. Pass / Fail / Insufficient

- **Pass:** all four models are capable and at least one replicated layer-band-information cell exceeds matched random directions with a replicated composition-over-control increment.
- **Fail:** capability is valid but no cell passes; this rejects fixed covariance-band identity in the registered task, not every functional coordinate.
- **Insufficient:** any data, capability, load, basis, replication, or sealed-test guard fails.

## 14. Claim Boundary And Deliverables

Deliver the dataset manifest/hash, four checkpoints, capability table, complete coarse/fine profile CSV, central heatmap, random controls, ablation table, `summary.md`, `detailed.md`, and next-day knowledge update. Even a Pass does not establish cross-layer routing benefit or NLL/FLOP gain; that requires a separate compatibility Protocol.
