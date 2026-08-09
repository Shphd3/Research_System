# Protocol: Router Output Counterfactual Audit

## 0. Approval Snapshot

**Approval status:** approved by the researcher in the 2026-07-29 request; full implementation, smoke, and full run authorized.

**Purpose:** determine whether changing only token-to-expert identity at one frozen MoE layer materially changes sparse-expert output geometry and downstream model output.

**Primary anchor:** diagnostic companion to [A06_00 functional specialization contract](../../../../../../Projects/from-attention-to-search/main/problem_anchors/06_geometry_proxy_preservation/06_00_functional_specialization_contract/06_00_functional_specialization_contract_anchor.md). This probe cannot promote an A06 utility claim.

**Experiment role:** operationalization/proxy audit of immediate expert non-interchangeability.

**Decision question:** with the same actual Router reference, expert input, expert parameters, native per-token gate weight, expert loads, shared expert, and all other routes fixed, does changing expert identity materially change sparse output and downstream prediction?

**Hypothesis:** the centered reassignment has much smaller effect than a load-matched random reassignment.

**Strongest rival:** aggregate spectra can remain similar while changed tokens, final logits, or held-out NLL change materially.

**Primary metric:**

$$
R_\ell=
\frac{1-\operatorname{CKA}(Y_{native},Y_{center})}
{1-\operatorname{CKA}(Y_{native},Y_{shuffle})}.
$$

**Minimal setup:** the two registered step-40k 12-layer, 8-expert, top-1 models; 32 calibration and 64 evaluation documents from DCLM `global-shard_02_of_10`; all 12 layers; one fixed shuffle seed per model/layer.

**Conditions:** Native, centered capacity-constrained reassignment, load-matched shuffle, and formal no-op replay.

**Pass H0:** both models independently satisfy all preregistered route, representation, spectral, and functional equivalence gates below.

**Reject H0:** both models independently show centered effects close to shuffle or a repeatable functional change outside the registered equivalence bounds.

**Insufficient:** too few eligible layers, ineffective shuffle, failed no-op, or opposite model-level verdicts.

**Cannot claim:** training-time representation formation, LB versus decommon causality, expert semantic utility, tree/long-range capability, or validation-loss-per-FLOP improvement.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete computation | Decision role | Cannot prove |
| --- | --- | --- | --- | --- |
| Sparse output | Routed expert contribution before the shared expert | native gate weight times the selected expert MLP output | Primary representation object | Expert usefulness |
| Native weight freeze | Keep each token's original top-1 softmax weight under every forced assignment | reuse $w_t^{native}$ | Makes expert identity the only changed MoE term | Deployable centered routing |
| Centered reassignment | Rank experts using $W(h-\hat\mu)$ and repair assignments to exact native quotas | deterministic minimum-penalty quota repair | Structured counterfactual | Globally optimal capacitated assignment |
| Load-matched shuffle | Permute native expert labels | exact native expert counts | Large perturbation reference | Same flip magnitude as centered routing |
| Linear CKA | Similarity of two token-by-feature matrices after feature centering | normalized squared cross-covariance Frobenius norm | Measures token geometry | Tokenwise functional equivalence |
| Flip-only CKA | CKA restricted to tokens whose centered route changed | same formula on flipped rows | Exposes dilution by unchanged tokens | Downstream loss |
| Flip-adjusted $R$ | $R_\ell/(p_{flip,center}/p_{flip,shuffle})$ | dimensionless sensitivity guard | Protects against unequal perturbation sizes | A causal derivative |

## 2. Alignment And Boundary

This audit checks a necessary condition for Router relevance: experts selected for the same state must not be functionally interchangeable. Output change alone is insufficient for functional specialization because a change may be harmful, random, or unrelated to held-out loss. The formal A06 utility decision is not updated by this run.

## 3. Data And Models

- Training logs for both models point to `global-shard_01_of_10`.
- Calibration and evaluation reuse the document-disjoint split already frozen in `../router_layer_band_probe/results/data_manifest.json`: 32 and 64 documents, 256 tokens each, from the independent top-level `global-shard_02_of_10`.
- Models are evaluated separately at checkpoint 40,000:
  - no-center, always-on load-balance coefficient 0.01;
  - running-center, load-balance coefficient 0.
- Both models have 12 MoE layers, hidden width 768, eight sparse experts, top-1 routing, an always-on shared expert, and unnormalized top-1 softmax weights.
- Both checkpoints set `gating_reference=oracle`: the Router reads the attention-branch output, while sparse/shared experts read the post-attention normalized hidden state. Both tensors are captured and held fixed; substituting the expert input for the Router reference is not a valid no-op.

## 4. Conditions And Fixed Variables

For each model and target layer $\ell$:

1. Run the unmodified model and separately cache the exact Router reference $g_\ell$, expert input $h_\ell$, native labels, native top-1 weights, block outputs, and final hidden states.
2. Compute routing scores from $g_\ell$ and every expert output $f_e(h_\ell)$ for all eight experts.
3. Construct Native, centered, shuffle, and no-op sparse outputs using the same $h_\ell$ and the same per-token native gate weight.
4. Keep the shared expert output unchanged.
5. Intervene only at layer $\ell$ and let all later layers route natively.

The centered assignment exactly matches all eight native expert counts. The deterministic repair starts from centered argmax labels and moves the minimum centered-score-penalty tokens from overloaded to underloaded experts until all quotas are exact.

## 5. Conditions And Evidence Roles

| Item | Why needed | Evidence role | Pass / guard | Failure meaning |
| --- | --- | --- | --- | --- |
| Native | Reference trajectory | Primary reference | finite outputs | implementation failure |
| Centered counterfactual | Structured route change | Primary treatment | flip rate $\ge0.20$ | layer is ineligible |
| Load-matched shuffle | Large reassignment reference | Positive control | flip rate $\ge0.50$ and sparse CKA $<0.99$ | denominator invalid |
| No-op replay | Numerical lower bound | Integrity guard | final KL $\le10^{-6}$ and $|\Delta$NLL$|\le10^{-6}$ | run invalid |
| Flip-only CKA | Unchanged-token dilution guard | Required sensitivity | reported for every eligible layer | low all-token $R$ is not sufficient |
| Flip-adjusted $R$ | Unequal flip-rate guard | Required sensitivity | reported for every eligible layer | raw $R$ cannot stand alone |

## 6. Metrics

### Primary representation metrics

- all-token sparse-output CKA and $R_\ell$;
- flip-only sparse-output CKA;
- flip-adjusted $R_\ell$;
- mean per-token cosine similarity and normalized Frobenius change.

### Spectral metrics

For centered sparse-output matrix $Y$ with singular values $s_i$, define $p_i=s_i^2/\sum_j s_j^2$ and effective rank $\exp[-\sum_i p_i\log p_i]$. Also record 90%-energy rank, total-variation distance between normalized spectra, and top-32 right-subspace mean/max principal angle. Every centered change is reported both absolutely and relative to shuffle.

### Functional guards

- target-layer block-output CKA;
- final-hidden CKA;
- native-to-counterfactual logit KL on next-token positions;
- held-out next-token NLL difference;
- the same quantities for shuffle and no-op.

## 7. Preregistered Decision Rules

A layer is eligible only if centered flip rate is at least 0.20, shuffle flip rate is at least 0.50, the shuffle sparse-output CKA is below 0.99, exact load equality holds, and no-op passes.

For one model to support H0, at least eight layers must be eligible and all clauses must hold across eligible layers:

1. median raw $R_\ell\le0.25$;
2. median flip-adjusted $R_\ell\le0.50$;
3. median flip-only CKA $\ge0.90$;
4. median centered/shuffle spectrum-distance ratio $\le0.25$ and median principal-angle ratio $\le0.25$;
5. median centered/shuffle logit-KL ratio $\le0.25$;
6. every eligible layer has $|\Delta\mathrm{NLL}_{center}|\le0.01$ nat/token.

One model rejects H0 if at least eight layers are eligible and either median raw $R_\ell\ge0.75$, median flip-only CKA $\le0.50$, median logit-KL ratio $\ge0.75$, or any eligible layer has repeatable $|\Delta\mathrm{NLL}_{center}|\ge0.02$ nat/token. Intermediate outcomes are model-level insufficient evidence. The combined verdict requires both models to agree.

These thresholds are an AI operationalization added before inspecting counterfactual results because the user draft specified the 20% flip gate but not numerical equivalence bounds.

## 8. Execution Contract

- Fixed shuffle seed: `20260729 + 100 * model_index + layer_index`.
- Evaluation batch size: chosen before the smoke run based only on memory safety.
- No tuning on evaluation results.
- Smoke must verify exact quotas, no-op replay, shared-output invariance, and finite metrics before the full run.
- Raw model checkpoints and DCLM documents remain outside `Research_System`; only code, manifests, compact tables, and result records are retained.

## 9. What This Cannot Claim

This intervention measures an immediate frozen-model effect. It does not show whether Router choices caused experts to form during training. Model-to-model natural-forward differences remain descriptive because centering and load-balance training changed together.

## 10. Review Notes

- Researcher-approved Chinese experiment draft received 2026-07-29.
- Added native-weight freezing so expert identity is the only changed MoE term.
- Added flip-only CKA and flip-adjusted $R$ to remove the strongest confound in the registered ratio.
- No-op debugging established that `gating_reference=oracle`; the protocol now fixes and records Router and expert inputs separately before any full counterfactual result is inspected.
- On 2026-07-29 the researcher explicitly requested the previously unreported natural-forward comparison: complete normalized Native sparse-output spectra for both models on the same evaluation tokens at every layer. This is a descriptive appendix only; it does not change the preregistered verdict and cannot identify an LB or decommon causal effect.
