# Summary: A06_01_05_E04 Full-Sequence LM Gradient Selector Guard

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

## Result Snapshot

Verdict: **gradient signal improves feature separation, but the full-LM margin guard failed.**

What we established: under full-sequence next-token language-model loss, embedding-gradient selection is not just random; at warmup 40 it improves immediate feature routing over all-position clustering. However, it does not yet provide a stable method-level guarantee because the low-tail router margin is not preserved after training.

What the experiment shows: route-position loss remains a near-oracle positive control, while full-sequence LM loss dilutes gradient energy across many non-route positions. Under full LM at warmup 40, embedding-gradient top-1 reaches feature NMI 0.823 with immediate margin p05 0.782, but after 160 post-reinit steps its margin p05 becomes -1.828. Top-4 and top-8 keep similar immediate NMI but have negative margin from the start.

What we do next: do not promote the current full-LM selector as solved. The next decision is whether a denoised gradient score can separate feature-slot signal from neutral-token LM noise without using route-position labels.

## Purpose

A06_01_05_E03 showed that embedding gradients can select feature-relevant states when the loss is computed only at the supervised route position. This run tests the main guard: whether the same idea still works when gradients come from the full next-token LM objective over all positions.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Full-sequence LM loss | Predict every next token in the sequence | Cross-entropy over logits at positions 0 to 30 against tokens 1 to 31 | \(\mathcal L^{full}=\sum_p \mathrm{CE}(\ell_p,x_{p+1})\) | Removes the route-only loss locality shortcut | Real language transfer |
| Route-position loss | Predict only the feature target after the feature slot | Cross-entropy at the final feature-slot position | \(\mathcal L^{route}=\mathrm{CE}(\ell_r,y)\) | Positive control for A06_01_05_E03 | Full-LM validity |
| Embedding-gradient top-k | Select positions whose input embedding receives large loss gradient | Per sample top-k of \(E^{emb}_{i,p}=\|\nabla_{e_{i,p}}\mathcal L_i\|_2^2\) | token positions | Tests whether gradients can locate feature-relevant states | Feature semantics |
| Feature NMI | Agreement between true feature id and routed expert | NMI(feature id, expert assignment) at route position | 0 to 1 | Primary separation metric | Utility or optimality |
| Margin p05 | Lower-tail router-score gap for the matched feature expert | 5th percentile of target expert score minus strongest competitor | logit gap | Guard for stable preservation | Correct output prediction |
| Slot-start NMI | Whether routing follows absolute slot start instead of feature | NMI(slot start, expert assignment) | 0 to 1 | Position-bias guard | Absence of other shortcuts |

## Exact Setup

Research question: Can embedding-gradient selection identify feature-relevant hidden states under full-sequence LM loss?

Data / model / objective: four uniformly sampled synthetic features, three possible slot starts, no position embeddings, one causal Transformer layer, one weighted top-1 MoE layer, four experts, and two loss modes: route-position cross-entropy and full-sequence next-token LM.

Conditions: no reinitialization, all-position clustering, route-position clustering, oracle feature-center initialization, hidden-gradient top-k, and embedding-gradient top-k.

Changed variables: loss mode, warmup steps, slot length, and selector method.

Held fixed: sequence length 32, feature count 4, expert count 4, neutral-token background, no position embeddings, optimizer, model size, evaluation protocol.

Seeds / checkpoints: 8 seeds, slot lengths 1/2/4/8, warmup steps 0/10/40, post-reinit checkpoints 0/10/40/80/160.

Paths: result tables are in `tables/`, central figures are in `figures/`, and the full runner is `scripts/run_a06_28_full_sequence_lm_gradient_selector_guard.py`.

Known limitation: the data are synthetic and balanced. Full-LM gradient selection does not use the route position to select tokens, but the evaluation and positive controls still use the known route position.

## Primary Metric

Definition: Feature NMI is the normalized mutual information between the true feature id and the expert chosen by the router at the route position.

Unit: 0 means no agreement; 1 means perfect feature-to-expert separation.

Why it decides: the anchor asks whether selected hidden states can initialize router rows that separate features. Feature NMI directly measures that routing separation.

Guard: Margin p05 must be positive for the low-tail samples. A high NMI with negative margin means the routing assignment is not robust.

## Result

The guard is weakened, not supported. Full-LM embedding gradients carry feature information, but the raw score is too noisy to be a stable initialization method.

At warmup 40, full-LM embedding-gradient top-1 improves over all-position clustering in immediate feature NMI, from 0.738 to 0.823, and has a small positive immediate margin p05 of 0.782. The gain is real but not stable: after 160 post-reinit steps, top-1 has feature NMI 0.845 but margin p05 -1.828. Top-4 and top-8 have similar immediate NMI, 0.827 and 0.816, but already have negative immediate margin p05, -2.071 and -2.994.

Route-position controls show the geometry is recoverable when the right states are available: full-LM route-position clustering at warmup 40 reaches feature NMI 0.988 and margin p05 10.111. Therefore the failure is not that the model cannot represent the feature split; the failure is that raw full-LM gradient selection does not isolate the right state pool reliably enough.

## Key Evidence

Full-LM warmup 40, immediate after reinitialization:

| Method | Feature NMI | Margin p05 | Preserve fraction | Slot-start NMI | Max load |
| --- | ---: | ---: | ---: | ---: | ---: |
| all-position clustering | 0.738 | -2.609 | 0.735 | 0.020 | 0.477 |
| route-position control | 0.988 | 10.111 | 0.979 | 0.005 | 0.266 |
| oracle feature centers | 1.000 | 11.669 | 1.000 | 0.001 | 0.250 |
| embedding-gradient top-1 | 0.823 | 0.782 | 0.786 | 0.006 | 0.432 |
| embedding-gradient top-4 | 0.827 | -2.071 | 0.779 | 0.005 | 0.462 |
| embedding-gradient top-8 | 0.816 | -2.994 | 0.768 | 0.009 | 0.458 |
| no reinit | 0.800 | -2.459 | 0.688 | 0.001 | 0.546 |

Full-LM warmup 40, after 160 post-reinit training steps:

| Method | Feature NMI | Margin p05 | Preserve fraction | Slot-start NMI | Max load |
| --- | ---: | ---: | ---: | ---: | ---: |
| all-position clustering | 0.612 | -5.835 | 0.595 | 0.029 | 0.578 |
| route-position control | 0.982 | 5.550 | 0.971 | 0.006 | 0.271 |
| oracle feature centers | 0.996 | 6.221 | 0.997 | 0.003 | 0.253 |
| embedding-gradient top-1 | 0.845 | -1.828 | 0.750 | 0.007 | 0.412 |
| embedding-gradient top-4 | 0.796 | -5.159 | 0.685 | 0.017 | 0.468 |
| embedding-gradient top-8 | 0.810 | -5.401 | 0.642 | 0.015 | 0.494 |
| no reinit | 0.701 | -4.245 | 0.649 | 0.116 | 0.508 |

## Key Figures

### Figure: Core Guard Result

![Core guard result](figures/a06_28_guard_core_reinit_w40.png)

What this tests: whether the full-LM selector still gives feature separation and positive margin when the route-only loss shortcut is removed.

Anchor question: Can embedding-gradient selection identify feature-relevant states under full-sequence LM loss?

Protocol question: Does full-LM embedding-gradient top-k beat all-position clustering and pass the positive margin guard?

Metric shown: feature NMI and margin p05.

Data source: `tables/condition_aggregate_reinit.csv`.

Aggregation level: mean over 8 seeds and 4 slot lengths at warmup 40.

How to read: higher NMI is better; margin p05 must be above zero to pass the preservation guard.

Observed result: full-LM embedding-gradient top-1/top-4/top-8 beat all-position NMI, but only top-1 has a small positive immediate margin, and this margin is not preserved after training.

Allowed claim: full-LM gradients contain feature signal.

What this does not prove: a stable unsupervised router-initialization method.

Anchor update implication: the A06_01_05_E03 route-only success cannot be fully promoted to full-LM settings.

### Figure: Slot-Length Boundary

![Slot-length boundary](figures/a06_28_full_lm_slot_len_boundary_w40.png)

What this tests: whether the result is uniform across feature-slot length.

Metric shown: feature NMI and margin p05 by slot length.

Data source: `tables/training_trajectory.csv`.

Aggregation level: mean over 8 seeds at full-LM warmup 40 and checkpoint 0.

How to read: each line is one method; stable recovery should keep high NMI and positive margin across all slot lengths.

Observed result: embedding-gradient top-1 works best for slot lengths 2 and 4, but fails the margin guard for slot lengths 1 and 8.

Allowed claim: full-LM gradient selection has a slot-length dependent boundary.

What this does not prove: the exact cause of the boundary.

Anchor update implication: the next method must denoise the gradient score, not just increase top-k.

### Figure: Selector Locality

![Selector locality](figures/a06_28_selector_locality_w40.png)

What this tests: whether full-LM gradient energy concentrates on route-relevant positions.

Metric shown: route-position fraction among top-1 selections, route-position fraction among selected top-k positions, and route-position share of total gradient score.

Data source: `tables/selector_diagnostics_aggregate.csv`.

Aggregation level: mean over 8 seeds and 4 slot lengths at warmup 40.

How to read: if the selector is clean, these quantities should be high. Route-position CE is the positive control.

Observed result: route-position CE concentrates almost entirely on the route position; full LM does not. For embedding-gradient top-1 under full LM, only 26.7% of top-1 selections are route positions, and route positions hold only 11.1% of total gradient score.

Allowed claim: full-LM gradient energy is diluted across positions.

What this does not prove: that no denoised full-LM signal can work.

Anchor update implication: the next test should target gradient denoising or contrastive normalization.

## Claim Boundary

Can claim:

- Full-sequence LM gradients contain route-relevant feature signal in this synthetic no-position setting.
- Raw embedding-gradient top-k is weaker than route-position control and does not pass a stable margin guard.
- The A06_01_05_E03 route-only result remains valid as a positive control but is not enough to claim full-LM unsupervised discovery.

Cannot claim:

- This solves unsupervised router initialization in real language data.
- The selected positions are semantic features.
- Attention context or full-LM gradient signal is equivalent to rare-feature routing.
- Increasing top-k is sufficient; in this run larger top-k often worsens margin.

## Next Decision

Test whether a denoised full-LM gradient score can isolate feature-slot signal from neutral-token prediction noise without using route-position labels.
