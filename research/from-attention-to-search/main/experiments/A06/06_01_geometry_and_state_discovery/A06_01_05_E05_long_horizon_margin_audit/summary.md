# Summary: A06_01_05_E05 Long-Train Margin Audit

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol: `protocol.md`

## Result Snapshot

Verdict: **2000 full-LM steps do not rescue raw embedding-gradient initialization; they also reveal that full-LM training gradually erodes even oracle and route-position center margins.**

What we established: the A06_01_05_E05 gradient-selector failure at 160 steps is not a too-short-training artifact. Extending post-reinit training to 2000 steps makes embedding-gradient top-k worse, not better.

What the experiment shows: the clean center controls remain clearly better in feature NMI, but their margin p05 also crosses below zero during long full-LM training. This means there are two distinct effects: raw gradient selection starts from a noisier, thinner-margin partition, and the full-LM objective later rewrites router geometry even when the initial centers are clean.

What we do next: separate the next work into two decisions: first improve the full-LM selector signal, then test a preservation intervention for long full-LM training.

## Purpose

A06_01_05_E05 showed that full-LM embedding-gradient top-1 had moderate feature NMI but lost margin by 160 steps. This audit tests whether longer training to 2000 steps can recover the margin.

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Long-train audit | Extend post-reinit training beyond the original 160 steps | same A06_01_05_E05 setup, but train to 2000 steps | optimizer steps | Tests whether margin failure is temporary | Global convergence |
| Full-sequence LM loss | Predict every next token | CE over all next-token positions | \(\mathcal L^{full}\) | Main objective being audited | Real language transfer |
| Feature NMI | Agreement between true feature id and routed expert | NMI(feature, route) at route position | 0 to 1 | Primary routing separation metric | Utility |
| Margin p05 | Lower-tail matched expert score gap | 5th percentile of target expert score minus strongest competitor | router-logit gap | Stability guard | Correct output prediction |
| Oracle center | True feature-center initialization | average route-position hidden states by feature label | router rows | Clean upper-bound initialization | Label-free method |
| Route-position center | Cluster route-position hidden states without feature labels | k-means on route-position hidden states | router rows | Route-state proxy control | Unknown route discovery |
| Embedding-gradient top-k | Select positions by embedding-gradient energy, then cluster selected hidden states | top-k of \(\|\nabla_e\mathcal L\|^2\) | token positions | Candidate label-free selector | Stable preservation |

## Exact Setup

The run reuses the A06_01_05_E05 synthetic no-position bridge: four uniformly sampled features, three slot starts, slot lengths 1/2/4/8, one causal Transformer layer, one weighted top-1 MoE layer, and four experts.

Objective: full-sequence next-token LM loss only.

Warmup: 40 steps.

Post-reinit training: 2000 steps.

Checkpoints: 0, 160, 500, 1000, 2000.

Seeds and slots: 8 seeds and 4 slot lengths, giving 32 completed cells.

Methods: oracle feature centers, route-position centers, embedding-gradient top-1/top-4/top-8, all-position centers, and no reinit.

Router input: raw hidden states during training and evaluation. Mean subtraction is used only to construct initialization rows.

Run: remote four-GPU ACP job `pt-e1vs7ci9`, status `SUCCEEDED`.

## Primary Result

At step 2000, embedding-gradient top-1 does not recover. It has feature NMI 0.717 and margin p05 -9.142. Top-4 and top-8 are worse in both NMI and margin.

The clean controls also lose positive low-tail margin by step 2000: oracle centers have feature NMI 0.845 and margin p05 -5.359; route-position centers have feature NMI 0.857 and margin p05 -4.531. Therefore, 2000-step full-LM training changes the preservation problem itself.

| Method | Step 0 NMI | Step 0 margin p05 | Step 160 NMI | Step 160 margin p05 | Step 2000 NMI | Step 2000 margin p05 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| oracle feature centers | 1.000 | 11.669 | 0.996 | 6.221 | 0.845 | -5.359 |
| route-position centers | 0.988 | 10.111 | 0.982 | 5.550 | 0.857 | -4.531 |
| embedding-gradient top-1 | 0.823 | 0.782 | 0.845 | -1.828 | 0.717 | -9.142 |
| embedding-gradient top-4 | 0.827 | -2.071 | 0.796 | -5.159 | 0.583 | -13.366 |
| embedding-gradient top-8 | 0.816 | -2.994 | 0.810 | -5.401 | 0.602 | -13.256 |
| all-position centers | 0.738 | -2.609 | 0.612 | -5.835 | 0.449 | -14.249 |
| no reinit | 0.800 | -2.459 | 0.701 | -4.245 | 0.473 | -8.819 |

## Interpretation

Observation: longer full-LM training improves target prediction accuracy but weakens feature-route margins. At step 2000, target accuracy is near 0.95--0.98 for all methods, while routing margins are negative for all methods.

Interpretation: full-LM optimization can solve the token-prediction objective without preserving the original feature-to-expert partition. The router assignment can remain partially feature-aligned by NMI while the score gap becomes margin-thin or sign-flipped.

Decision: do not treat longer training as a fix for the raw selector. The next model must distinguish selector quality from preservation under full-LM optimization.

## Key Figures

### Figure: NMI And Margin Trajectory

![NMI and margin trajectory](figures/a06_28_long_train_nmi_margin_trajectory.png)

What this tests: whether longer post-reinit training rescues margin.

Observed result: embedding-gradient methods do not recover. Oracle and route-position controls decay more slowly, but their margin p05 also becomes negative after long training.

Allowed claim: full-LM long training does not rescue raw gradient-selected margins.

What this does not prove: which preservation intervention will work.

### Figure: Step-2000 Final State

![Step-2000 final state](figures/a06_28_long_train_final_step2000.png)

What this tests: the final state after 2000 full-LM steps.

Observed result: route-position and oracle centers retain the highest NMI, but all methods have negative margin p05.

Allowed claim: clean initialization remains better than raw gradient selection in NMI, but clean initialization is not sufficient for long full-LM margin preservation.

### Figure: Step-2000 Slot-Length Boundary

![Step-2000 slot boundary](figures/a06_28_long_train_slot_boundary_step2000.png)

What this tests: whether the long-train result is driven by one slot length.

Observed result: the negative-margin pattern is broad across slot lengths, with only route-position centers at slot length 1 slightly above zero.

Allowed claim: the long-train margin failure is not a single-slot artifact.

## Claim Boundary

Can claim:

- 2000 full-LM steps do not rescue raw embedding-gradient top-k initialization.
- Clean feature/route center initialization remains better than raw gradient selection by feature NMI.
- Long full-LM optimization can erode positive margins even from clean centers.

Cannot claim:

- Feature centers are useless; they are very strong at initialization and through early training.
- The same margin erosion will occur in real language data.
- A denoised selector or preservation method cannot solve the problem.

## Next Decision

Split the next anchor into two parts:

1. Selector: can a denoised full-LM gradient score find a cleaner feature-state pool?
2. Preservation: can routing-time centering, margin regularization, or router-row freezing preserve clean centers under long full-LM training?
