# Detailed: A06_01_05_E04 Full-Sequence LM Gradient Selector Guard

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

Summary: `summary.md`

## 0. Quick Recap

Purpose: audit whether A06_01_05_E03's embedding-gradient selector still works when the gradient is computed from the full next-token language-model objective rather than from the supervised route-position objective.

Hypothesis: if embedding-gradient selection is a real route-relevant state selector, then full-sequence LM gradient energy should still select a hidden-state pool that initializes feature-specialized router rows.

Experiment logic: compare route-position loss as the positive control against full-sequence LM loss as the guard condition, while holding the synthetic data, model, seeds, slot lengths, and evaluation fixed.

Conclusion: the raw full-LM embedding-gradient selector has usable signal but fails the method-level margin guard. The route-only success from A06_01_05_E03 cannot be directly promoted to full-LM unsupervised initialization.

Evidence: under full LM at warmup 40, embedding-gradient top-1 immediate feature NMI is 0.823 versus all-position 0.738, but final margin p05 is -1.828. Route-position clustering under the same full-LM warmup reaches immediate NMI 0.988 and margin p05 10.111.

## 1. Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit / formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Feature | Synthetic token identity that determines the target token | \(f\in\{0,1,2,3\}\) | categorical id | Ground-truth routing factor | Semantic feature in real data |
| Slot | Repeated feature-token span inside the sequence | positions from `slot_start` to `slot_start + slot_len - 1` | token span | Holds feature evidence | Natural language structure |
| Route position | Last token position of the feature slot | \(r=\mathrm{slot\_start}+\mathrm{slot\_len}-1\) | token position | Evaluation location for routing | A deployable selector |
| Target token | Feature-specific next token after the slot | token id \(36+f\) | vocabulary id | The supervised next-token consequence | Real semantic target |
| Route-position loss | Loss only at the route position | \(\mathcal L^{route}_i=\mathrm{CE}(\ell_{i,r_i}, y_i)\) | cross-entropy | A06_01_05_E03 positive control | Full-LM validity |
| Full-sequence LM loss | Loss at every next-token position | \(\mathcal L^{full}_i=\sum_{p=0}^{T-2}\mathrm{CE}(\ell_{i,p},x_{i,p+1})\) | cross-entropy | Main guard against route-only leakage | Real language generality |
| Embedding-gradient energy | How strongly the loss changes an input token embedding | \(E^{emb}_{i,p}=\|\nabla_{e_{i,p}}\mathcal L_i\|_2^2\) | squared gradient norm | Candidate unsupervised token selector | Feature labels |
| Hidden-gradient energy | How strongly the loss changes a post-attention hidden state | \(E^{h}_{i,p}=\|\nabla_{h_{i,p}}\mathcal L_i\|_2^2\) | squared gradient norm | Alternative selector | Feature labels |
| Feature NMI | Agreement between feature id and chosen expert | normalized mutual information | 0 to 1 | Primary routing separation metric | Output utility |
| Margin p05 | Low-tail score gap for the matched feature expert | 5th percentile of \(s_{e^*(f)}-\max_{e\ne e^*(f)}s_e\) | logit gap | Preservation and stability guard | Optimality |
| Preserve fraction | Fraction routed to the feature-matched expert | mean of `assign == matched expert` | 0 to 1 | More direct assignment guard | Margin thickness |
| Slot-start NMI | Agreement between slot start and chosen expert | NMI(slot start, expert assignment) | 0 to 1 | Checks position shortcut | Other shortcuts |

## 2. Protocol Audit

Approved conditions match actual conditions: yes. The full run covered both `route_ce` and `full_lm`, all planned methods, warmup steps 0/10/40, slot lengths 1/2/4/8, and seeds 0 to 7.

Primary metric exists: yes. Feature NMI is recorded in `tables/training_trajectory.csv`, `tables/condition_aggregate_reinit.csv`, and `tables/condition_aggregate_final.csv`.

Central figures/tables exist: yes. The report-ready figures are:

- `figures/a06_28_guard_core_reinit_w40.png`
- `figures/a06_28_full_lm_slot_len_boundary_w40.png`
- `figures/a06_28_selector_locality_w40.png`

Seeds/checkpoints recorded: yes. There are 32 completed seed/slot cells and 13440 training trajectory rows.

Known good reviewed: route-position and oracle controls pass.

Known bad reviewed: all-position clustering and no-reinit remain weaker and usually negative-margin.

Confusing case reviewed: full-LM embedding-gradient top-1 has a small positive immediate average margin but loses the margin after post-reinit training and fails for some slot lengths.

## 3. Data Construction

The experiment uses a balanced synthetic no-position slot bridge.

Sequence length: 32.

Neutral tokens: ids 0 to 31, sampled randomly as background.

Feature tokens: ids 32 to 35, one id per feature.

Target tokens: ids 36 to 39, one id per feature.

Feature distribution: uniform over four features. Each calibration, training, and evaluation batch is balanced by construction.

Slot starts: 2, 10, and 18. Slot start is balanced over the available choices.

Slot lengths: 1, 2, 4, and 8.

For each sample with feature \(f\) and slot start \(a\):

\[
x_{a:a+L}=32+f,\qquad x_{a+L}=36+f,\qquad r=a+L-1.
\]

The route-position target is \(y=36+f\). Full LM uses all next-token labels \(x_{p+1}\), including neutral background positions and the feature target position.

Data audit:

| Field | Value |
| --- | --- |
| completed seed/slot cells | 32 |
| seeds | 0, 1, 2, 3, 4, 5, 6, 7 |
| slot lengths | 1, 2, 4, 8 |
| calibration samples per cell | 2048 |
| evaluation samples per cell | 2048 |
| feature fractions | 0.25 each |
| slot start choices | 3 |

## 4. Model And Objectives

Model: one causal self-attention layer, layer norm, one weighted top-1 MoE layer, layer norm, and an LM head.

Router: linear router without bias. The selected expert is the argmax of router softmax probability. The expert output is multiplied by the selected probability.

No position embeddings are used. This is required so position shortcuts can be audited by `slot_start_NMI` rather than built into the input representation.

Core model settings:

| Setting | Value |
| --- | ---: |
| hidden width | 64 |
| attention heads | 4 |
| feed-forward width | 128 |
| experts | 4 |
| optimizer | AdamW |
| learning rate | 0.002 |
| weight decay | 0.0001 |
| gradient clipping | 1.0 |
| router row scale | 1.5 |

Loss modes:

```text
route_ce:
  CE(logits at route position, feature target token)

full_lm:
  CE(logits at every position 0..30, next token at 1..31)
```

## 5. Selector Algorithms

All selectors build router rows by clustering a pool of hidden states, then normalizing the resulting rows to the same router scale.

`no_reinit`: keep the warmup router rows.

`allpos_centered`: collect all hidden states from all positions, subtract the all-position mean, and run k-means with four clusters.

`route_centered`: collect hidden states only at the route position, subtract the route-position mean, and run k-means. This uses route positions and is a positive control, not the candidate unsupervised method.

`oracle_centered`: average route-position hidden states by true feature id, subtract the route-position mean, and use these four feature centers. This uses feature labels and is an upper bound.

`grad_emb_topk_centered`: compute full per-position embedding gradients, score each position by squared gradient norm, select top-k positions per sample, collect the corresponding hidden states, center this selected pool by its own mean, and run k-means.

`grad_h_topk_centered`: same as `grad_emb_topk_centered`, but uses hidden-state gradient energy.

`grad_emb_direction_topk_centered` and `grad_h_direction_topk_centered`: select top-k positions by gradient energy, cluster normalized gradient directions, then average selected hidden states inside each direction cluster. These were diagnostic alternatives and did not improve the main conclusion.

Important implementation boundary: full-LM gradient selection does not use route position to select positions. Route position is used for evaluation, positive controls, and diagnostic masks.

## 6. Metrics

Primary metric:

\[
\mathrm{FeatureNMI}=\mathrm{NMI}(f,\operatorname*{argmax}_e s_e(h_r)).
\]

Here \(f\) is the true feature id and \(s_e(h_r)\) is the router score for expert \(e\) at the route-position hidden state.

Margin:

\[
\mathrm{margin}(i)=s_{e^*(f_i)}(h_{r_i})-\max_{e\ne e^*(f_i)}s_e(h_{r_i}),
\]

where \(e^*(f)\) is the best feature-to-expert matching inferred from assignment counts. `margin_p05` is the 5th percentile of this value over evaluation samples.

Selector locality metrics:

- `top1_route_frac`: fraction of samples where the largest gradient-energy position is the route position.
- `selection_route_frac`: fraction of selected top-k positions that are route positions.
- `score_route_share`: fraction of total gradient energy located at route positions.
- `score_slot_share`: fraction of total gradient energy located inside the full feature slot.

## 7. Main Results

### 7.1 Positive Control: Route-Position Loss

Route-position loss concentrates gradient energy on the route position and recovers feature-specialized routing.

Warmup 40, immediate after reinitialization:

| Method | Feature NMI | Margin p05 | Preserve fraction | Slot-start NMI | Max load | Target accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all-position clustering | 0.876 | -4.398 | 0.798 | 0.001 | 0.420 | 0.961 |
| route-position control | 0.996 | 9.456 | 0.992 | 0.001 | 0.258 | 0.915 |
| oracle feature centers | 1.000 | 10.083 | 1.000 | 0.001 | 0.250 | 0.890 |
| embedding-gradient top-1 | 0.980 | 7.390 | 0.963 | 0.005 | 0.281 | 0.909 |
| embedding-gradient top-4 | 0.971 | 4.216 | 0.945 | 0.001 | 0.305 | 0.903 |
| embedding-gradient top-8 | 0.916 | -2.503 | 0.852 | 0.001 | 0.390 | 0.942 |
| no reinit | 0.816 | -3.154 | 0.695 | 0.001 | 0.523 | 1.000 |

Interpretation: A06_01_05_E03 is reproduced as a positive control. Embedding-gradient top-1 under route-position CE nearly matches route-position clustering, and top-4 remains strong. Larger top-k already shows margin dilution.

### 7.2 Main Guard: Full-Sequence LM Loss

Full-LM embedding gradients improve NMI but do not pass the stable margin guard.

Warmup 40, immediate after reinitialization:

| Method | Feature NMI | Margin p05 | Preserve fraction | Slot-start NMI | Max load | Target accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all-position clustering | 0.738 | -2.609 | 0.735 | 0.020 | 0.477 | 0.297 |
| route-position control | 0.988 | 10.111 | 0.979 | 0.005 | 0.266 | 0.290 |
| oracle feature centers | 1.000 | 11.669 | 1.000 | 0.001 | 0.250 | 0.248 |
| embedding-gradient top-1 | 0.823 | 0.782 | 0.786 | 0.006 | 0.432 | 0.278 |
| embedding-gradient top-4 | 0.827 | -2.071 | 0.779 | 0.005 | 0.462 | 0.296 |
| embedding-gradient top-8 | 0.816 | -2.994 | 0.768 | 0.009 | 0.458 | 0.286 |
| no reinit | 0.800 | -2.459 | 0.688 | 0.001 | 0.546 | 0.408 |

Warmup 40, after 160 post-reinit training steps:

| Method | Feature NMI | Margin p05 | Preserve fraction | Slot-start NMI | Max load | Target accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all-position clustering | 0.612 | -5.835 | 0.595 | 0.029 | 0.578 | 0.553 |
| route-position control | 0.982 | 5.550 | 0.971 | 0.006 | 0.271 | 0.552 |
| oracle feature centers | 0.996 | 6.221 | 0.997 | 0.003 | 0.253 | 0.514 |
| embedding-gradient top-1 | 0.845 | -1.828 | 0.750 | 0.007 | 0.412 | 0.554 |
| embedding-gradient top-4 | 0.796 | -5.159 | 0.685 | 0.017 | 0.468 | 0.554 |
| embedding-gradient top-8 | 0.810 | -5.401 | 0.642 | 0.015 | 0.494 | 0.517 |
| no reinit | 0.701 | -4.245 | 0.649 | 0.116 | 0.508 | 0.568 |

Observation: full-LM top-1 is the best candidate among raw gradient selectors, but it does not maintain a positive margin after training. Top-4 and top-8 do not fix the issue; they bring in more non-route positions and worsen the margin.

Interpretation: the signal exists but is not clean enough. The failure is a selector-noise problem, not a representation impossibility, because route-position and oracle controls remain strong under the same full-LM-trained states.

### 7.3 Slot-Length Boundary

Full-LM warmup 40, immediate feature NMI by slot length:

| Slot length | all-position | route-position | emb grad top-1 | emb grad top-4 | emb grad top-8 | no reinit |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.508 | 1.000 | 0.565 | 0.565 | 0.629 | 0.806 |
| 2 | 0.575 | 1.000 | 0.950 | 0.915 | 0.826 | 0.788 |
| 4 | 0.884 | 0.975 | 0.981 | 0.916 | 0.916 | 0.795 |
| 8 | 0.983 | 0.976 | 0.798 | 0.912 | 0.895 | 0.812 |

Full-LM warmup 40, immediate margin p05 by slot length:

| Slot length | all-position | route-position | emb grad top-1 | emb grad top-4 | emb grad top-8 | no reinit |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | -6.314 | 10.553 | -2.979 | -2.919 | -2.529 | -2.931 |
| 2 | -5.552 | 11.241 | 2.466 | -3.017 | -6.680 | -3.248 |
| 4 | -3.944 | 9.137 | 7.077 | -1.131 | -1.130 | -2.023 |
| 8 | 5.374 | 9.512 | -3.437 | -1.218 | -1.636 | -1.634 |

Observation: embedding-gradient top-1 works best at slot lengths 2 and 4. It fails the margin guard at slot lengths 1 and 8. All-position clustering becomes strong at slot length 8, which means longer repeated slots make feature centers easier to separate even without gradient selection.

Interpretation: the selector is sensitive to how much feature evidence is spread over the sequence. This supports a denoising view: the raw top-k score is not an invariant feature-position detector.

### 7.4 Selector Locality

Full-LM warmup 40 selector diagnostics:

| Method | Top-1 route fraction | Route score share | Slot score share | Selected route fraction | Selected slot fraction | Center margin p05 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| embedding-gradient top-1 | 0.267 | 0.111 | 0.201 | 0.267 | 0.404 | 0.386 |
| embedding-gradient top-4 | 0.267 | 0.111 | 0.201 | 0.152 | 0.236 | -1.154 |
| embedding-gradient top-8 | 0.267 | 0.111 | 0.201 | 0.087 | 0.140 | -1.964 |
| hidden-gradient top-1 | 0.114 | 0.047 | 0.073 | 0.114 | 0.146 | -1.520 |

Route-position CE warmup 40 selector diagnostics:

| Method | Top-1 route fraction | Route score share | Slot score share | Selected route fraction | Selected slot fraction | Center margin p05 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| embedding-gradient top-1 | 1.000 | 0.923 | 0.968 | 1.000 | 1.000 | 5.110 |
| embedding-gradient top-4 | 1.000 | 0.923 | 0.968 | 0.250 | 0.655 | 3.029 |
| embedding-gradient top-8 | 1.000 | 0.923 | 0.968 | 0.125 | 0.458 | -1.543 |
| hidden-gradient top-1 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 6.899 |

Observation: under full LM, route positions receive only 11.1% of total embedding-gradient energy, and top-1 selects the route position only 26.7% of the time. Under route CE, the same diagnostic is near 1.0.

Interpretation: full LM creates a mixed gradient field. The raw energy score can find some feature-relevant states, but it is diluted by neutral-token prediction and target-position effects.

## 8. Visualization Results

### Figure: Core Guard Result

![Core guard result](figures/a06_28_guard_core_reinit_w40.png)

Anchor question: Can embedding-gradient selection identify feature-relevant states under full-sequence LM loss?

Protocol question: Does full-LM embedding-gradient top-k beat all-position clustering and pass positive margin?

Metric shown: feature NMI and margin p05.

Metric definition: feature NMI is NMI(feature id, assigned expert); margin p05 is the 5th percentile of the matched expert score gap.

Metric unit: NMI is unitless in [0, 1]; margin is a router-logit gap.

Data source: `tables/condition_aggregate_reinit.csv`.

Aggregation level: mean over 8 seeds and 4 slot lengths at warmup 40.

Axis / legend meaning: bars are methods; left column is route-position CE; right column is full-sequence LM; top row is NMI; bottom row is margin.

Expected pattern if supported: full-LM embedding-gradient methods should approach route-position control and have positive margin.

Expected pattern if weakened or incomplete: NMI improves but margin is zero or negative.

Observed result: full-LM embedding-gradient methods improve NMI over all-position clustering, but only top-1 has a small immediate positive margin, and later training removes it.

Allowed claim: full-LM gradient contains feature signal.

What this figure does not prove: a stable unsupervised router initialization method.

Anchor update implication: A06_01_05_E03 remains route-loss-local unless the gradient score is denoised.

### Figure: Full-LM Slot-Length Boundary

![Full-LM slot-length boundary](figures/a06_28_full_lm_slot_len_boundary_w40.png)

Anchor question: Is the selector robust across the synthetic slot configurations?

Protocol question: Does the full-LM selector recover feature routing for slot lengths 1, 2, 4, and 8?

Metric shown: feature NMI and margin p05.

Data source: `tables/training_trajectory.csv`.

Aggregation level: mean over 8 seeds at full-LM warmup 40 and checkpoint 0.

Axis / legend meaning: x-axis is slot length; each line is a method.

Expected pattern if supported: high NMI and positive margin across all slot lengths.

Observed result: top-1 works at slot lengths 2 and 4 but fails at 1 and 8. All-position clustering becomes strong at length 8.

Allowed claim: full-LM gradient selection has a clear robustness boundary.

What this figure does not prove: which denoising method will remove the boundary.

Anchor update implication: the next test should target signal normalization, not only more warmup or larger top-k.

### Figure: Selector Locality

![Selector locality](figures/a06_28_selector_locality_w40.png)

Anchor question: Does full-LM gradient energy concentrate on route-relevant positions?

Protocol question: Is the selected token pool clean enough to explain feature-specialized router rows?

Metric shown: top-1 route fraction, selected route fraction, and route score share.

Data source: `tables/selector_diagnostics_aggregate.csv`.

Aggregation level: mean over 8 seeds and 4 slot lengths at warmup 40.

Axis / legend meaning: bars are selector-locality diagnostics; left panel is route CE; right panel is full LM.

Expected pattern if supported: full-LM diagnostics should be substantially concentrated on route/slot positions.

Observed result: route CE is concentrated on route positions; full LM is not.

Allowed claim: full-LM raw gradient energy is diluted across sequence positions.

What this figure does not prove: that all full-LM-derived gradient scores must fail.

Anchor update implication: raw energy is insufficient; the next selector needs denoising or contrastive normalization.

## 9. Failure Decomposition

What passed:

- Full run coverage passed: 32 seed/slot cells and 13440 trajectory rows.
- Route-position and oracle controls passed under both loss modes.
- Full-LM embedding-gradient top-1 improved immediate NMI over all-position clustering at warmup 40.
- Slot-start NMI stayed low for the main immediate comparisons, so the main gain is not explained by absolute slot start routing.

What failed:

- Full-LM top-1 did not preserve positive margin after post-reinit training.
- Full-LM top-4 and top-8 had negative margin at initialization.
- Hidden-gradient selectors were weaker than embedding-gradient selectors.
- Short slots and long slots expose different failure modes: too little feature evidence at length 1; diluted or mixed position selection at length 8.

Mechanism interpretation:

The full-LM gradient is a mixed signal:

\[
\nabla_e \mathcal L^{full}
=\nabla_e \mathcal L^{feature-target}
+\nabla_e \mathcal L^{neutral-background}
+\nabla_e \mathcal L^{other-token}.
\]

The useful component is present, but the raw squared norm does not isolate it. Increasing top-k selects more positions but also increases contamination from non-route states:

\[
\mathcal H_{sel}(k)=\{h_{i,p}:p\in\mathrm{TopK}(E^{emb}_{i,p})\}.
\]

As \(k\) grows, the selected pool becomes less route-local under full LM, so the k-means centers become less margin-preserving.

## 10. Claim Boundary

Can claim:

- In this synthetic no-position setting, full-sequence LM gradients contain a measurable feature-routing signal.
- Raw embedding-gradient top-1 is better than all-position clustering on immediate full-LM feature NMI at warmup 40.
- Raw embedding-gradient top-k is not yet a stable method because margin is not preserved.
- The A06_01_05_E03 route-only result is a valid positive control but has a narrower claim boundary than the main unsupervised goal.

Cannot claim:

- The method solves feature discovery in real language data.
- The selected gradient positions are semantic features.
- The method identifies rare features or common/rare routing mechanisms.
- Full-LM gradient energy is sufficient without denoising.
- More selected positions improve the selector.

## 11. Next Decision

Decision question: can a denoised full-LM gradient score isolate feature-slot signal from neutral-token prediction noise without route-position labels?

Candidate next tests should compare raw embedding-gradient energy against one or two denoised scores, with the same primary metrics:

- immediate feature NMI;
- margin p05;
- selected route/slot fractions for diagnosis only;
- slot-start NMI as a shortcut guard.

The next run should be treated as method construction only if the denoised score has a clear physical target: remove neutral-token gradient energy while preserving feature-dependent gradient energy.

## 12. Artifact Map

Experiment folder:
`Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E04_full_lm_gradient_guard/`

Runner:
`scripts/run_a06_28_full_sequence_lm_gradient_selector_guard.py`

Submission script:
`submit_a06_28_full_lm_guard_4gpu_acp.sh`

Remote job:

| Field | Value |
| --- | --- |
| run name | `a06_28_full_lm_guard_full_4gpu_20260706` |
| job id | `pt-jkdhdacq` |
| status | `SUCCEEDED` |
| runtime log | `logs/acp/a06_28_full_lm_guard_full_4gpu_20260706_runtime_20260706_065441.log` |
| submit log | `logs/acp/a06_28_full_lm_guard_full_4gpu_20260706_submit_20260706_065109.log` |

Tables:

| File | Role |
| --- | --- |
| `tables/data_audit.csv` | seed/slot/data balance audit |
| `tables/training_trajectory.csv` | complete per-condition checkpoint trajectory |
| `tables/condition_aggregate_reinit.csv` | checkpoint-0 aggregate by loss/method/warmup |
| `tables/condition_aggregate_final.csv` | final-step aggregate by loss/method/warmup |
| `tables/condition_trajectory_aggregate.csv` | aggregate trajectories |
| `tables/selector_diagnostics.csv` | per-cell selector locality and row diagnostics |
| `tables/selector_diagnostics_aggregate.csv` | aggregate selector diagnostics |

Report figures:

| File | Role |
| --- | --- |
| `figures/a06_28_guard_core_reinit_w40.png` | main route-CE versus full-LM guard comparison |
| `figures/a06_28_full_lm_slot_len_boundary_w40.png` | slot-length robustness boundary |
| `figures/a06_28_selector_locality_w40.png` | selector locality and gradient dilution |

Generated diagnostic figures:

- `figures/full_lm_reinit_feature_nmi_by_method_warmup.png`
- `figures/full_lm_reinit_margin_p05_by_method_warmup.png`
- `figures/full_lm_final_feature_nmi_by_method_warmup.png`
- `figures/full_lm_final_margin_p05_by_method_warmup.png`
- `figures/route_ce_reinit_feature_nmi_by_method_warmup.png`
- `figures/route_ce_reinit_margin_p05_by_method_warmup.png`
- `figures/route_ce_final_feature_nmi_by_method_warmup.png`
- `figures/route_ce_final_margin_p05_by_method_warmup.png`
- `figures/diagnostic_common_alignment_by_method_warmup.png`
- `figures/diagnostic_feature_center_alignment_by_method_warmup.png`
- `figures/diagnostic_row_similarity_by_method_warmup.png`
- `figures/diagnostic_top1_route_frac_by_method_warmup.png`

## 13. Repro Command

Four-GPU full command:

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 torchrun --standalone --nproc_per_node=4 \
  Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E04_full_lm_gradient_guard/scripts/run_a06_28_full_sequence_lm_gradient_selector_guard.py \
  --run-stage full \
  --run-name a06_28_full_lm_guard_full_4gpu_20260706 \
  --output-dir Projects/from-attention-to-search/main/experiments/A06/06_01_geometry_and_state_discovery/A06_01_05_E04_full_lm_gradient_guard
```
