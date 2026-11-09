# Summary: A06_01_05_E01 Warmup Spectral Router Reinitialization

Primary anchor:
`../../../../problem_anchors/06_geometry_proxy_preservation/06_01_geometry_and_state_discovery/06_01_geometry_and_state_discovery_anchor.md`

Protocol:
`protocol.md`

## Result Snapshot

Verdict: Partially supported, with a tightened method boundary.

What was established: On the uniform no-position slot dataset, short warmup
does make all-position hidden clustering and expert spectral directions more
feature-aware. However, neither source closes the gap to route-position
centers. Route-relevant state selection remains the strongest bottleneck.

What the experiment shows: Immediate feature NMI for all-position clustering
improves from `0.774` at warmup 0 to `0.876` at warmup 40, while route-position
clustering reaches `0.996` at warmup 40. Raw expert SVD also improves after
warmup, and common-projected expert SVD is the best spectral variant
(`0.943` immediate feature NMI at warmup 40). Orthogonalizing expert SVD rows
does not help.

What to do next: Treat delayed warmup geometry as a candidate source audit, not
as a finished method. The next anchor should test whether nested-learning style
future supervision can make route-relevant hidden states feature-aware earlier
and with thicker routing margins.

Execution: Full local two-GPU run completed successfully.

- run name: `a06_25_full_local2gpu_20260703`
- completed cells: `32` seed/slot cells
- training rows: `3360`
- seeds: `0--7`
- slot lengths: `1,2,4,8`
- warmup steps: `0,10,40`
- post-reinit train steps: `160`

## Terminology / Definitions

| Term | Plain meaning | Concrete object / computation | Unit or formula | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- | --- |
| Uniform feature | Four synthetic features sampled equally | Feature ids 0--3, each probability 0.25 | Probability | Keeps the question about geometry, not frequency skew | Real language semantics |
| Route position | Task-relevant audited token | Last token of the repeated feature slot | Sequence index | Correct positive control should route this state | Automatic route discovery |
| All-position pool | Hidden states from every token position | Background, feature-slot, and target-adjacent positions together | Vector set | Tests whether global hidden geometry is enough | Route relevance |
| Warmup | Short training before router reset | 0, 10, or 40 optimizer steps | Steps | Tests whether early learning forms usable geometry | Long-run convergence |
| Expert SVD row | Router row from an expert input-side principal direction | Top right singular vector of the first expert linear layer | Unit vector | Tests whether expert parameter geometry is feature-aware | Expert utility |
| Common-projected SVD | Expert SVD row after removing the route common mean direction | \(v_e-(v_e^\top c)c/\|c\|^2\) | Unit vector after normalization | Tests whether common alignment is a failure source | Best possible common operator |
| Feature NMI | Agreement between feature id and routed expert | NMI(feature id, route) on balanced route-position eval | 0--1 | Primary metric for feature separation | Expert functional value |
| Matched preserve fraction | Survival of the step-0 feature-to-expert identity | Fraction assigned to the matched expert for that feature | 0--1 | Detects identity loss after training | Semantic value |
| Margin p05 | Lower-tail routing safety distance | 5th percentile of matched expert score minus best competitor | Logit difference | Tests whether assignment sits in a stable basin | Loss optimality |
| Slot-start NMI | Agreement between slot start and routed expert | NMI(slot_start, route) | 0--1 | Guards against position shortcut | All context effects absent |

## Exact Setup

Data: Synthetic sequences contain neutral background tokens, one repeated
feature slot, and a feature-specific target token after the slot. Features
0--3 are sampled uniformly for calibration, warmup, training, and evaluation.
The feature tokens are token ids `32--35`; target tokens are `36--39`; neutral
tokens are `0--31`.

No explicit position embeddings are used. Slot starts are balanced over
positions `2,10,18`; slot lengths are `1,2,4,8`. The routed/evaluated position
is the last token of the repeated feature slot. The target is the token
immediately after the slot.

Model: one causal self-attention layer, one weighted top-1 MoE layer with four
experts, hidden size `64`, four attention heads, expert hidden size `128`, and
one language-model head.

Objective: cross-entropy at the route position predicting the feature-specific
target token.

Conditions: no reinitialization, all-position centered k-means,
route-position centered k-means, oracle feature centers, raw expert SVD,
common-projected expert SVD, and orthogonalized expert SVD.

## Primary Metric

Feature NMI is the primary metric because the anchor asks whether uniform
features are separated into different experts. Target accuracy is only a guard:
all methods can learn the synthetic target, so target accuracy cannot decide
whether expert specialization occurred.

## Main Results

### Result 1: Warmup improves all-position clustering, but it does not close the route-position gap.

Immediate feature NMI:

| Warmup | All-position centered | Route-position centered | Oracle centered |
| ---: | ---: | ---: | ---: |
| 0 | 0.774 | 0.995 | 1.000 |
| 10 | 0.809 | 0.964 | 1.000 |
| 40 | 0.876 | 0.996 | 1.000 |

Interpretation: early training does make global hidden geometry more
feature-aware, so the step-0-random-hidden-state explanation is partly valid.
But all-position pooling still mixes route and non-route states; route-position
centers remain the positive-control upper bound.

Boundary: This does not prove all-position clustering is useless. It shows that
on this dataset, warmup alone is not enough to promote all-position clustering
as the next method.

### Result 2: Expert spectral directions become useful after warmup, and common projection is the best tested spectral correction.

Immediate feature NMI:

| Warmup | Raw expert SVD | Common-projected expert SVD | Orthogonalized expert SVD |
| ---: | ---: | ---: | ---: |
| 0 | 0.736 | 0.797 | 0.667 |
| 10 | 0.859 | 0.914 | 0.750 |
| 40 | 0.879 | 0.943 | 0.704 |

Interpretation: expert top singular directions are not completely
feature-unaware after warmup. Removing the common mean direction improves
immediate feature separation and gives the only spectral condition with
positive immediate margin p05 at warmup 10/40 (`0.088` and `0.514`).

Boundary: This is a source-quality result, not a deployable spectral-router
claim. The route-position control still has much thicker margins
(`6.407` and `9.456` immediate margin p05 at warmup 10/40).

### Result 3: "Rows are too similar" is not the main failure explanation.

Orthogonalized expert SVD explicitly removes row similarity, but it performs
worse than raw SVD and common-projected SVD. At warmup 40, orthogonalized SVD
has immediate feature NMI `0.704` and immediate margin p05 `-5.311`, while raw
SVD has `0.879` and `-2.809`, and common-projected SVD has `0.943` and `0.514`.

Interpretation: the failure mode is not merely that expert SVD rows are too
close. The stronger explanation is that a source row must be feature-aware and
must avoid common-dominated directions while preserving enough margin.

Boundary: This does not rule out manifold-power or other spectral router
methods. It only rules out naive row orthogonalization as the decisive fix in
this bridge.

### Guards

The data audit passed: every audited split has four feature fractions equal to
`0.25`, and each split uses three slot starts.

The position shortcut guard passed: maximum mean slot-start NMI at immediate
reinit is `0.0166`, and final slot-start NMI remains near zero.

Target learning is not the deciding metric: all final conditions reach target
accuracy `1.000`.

## Key Figures

### Figure: Immediate Feature NMI

![Immediate feature NMI after router reinit](figures/reinit_feature_nmi_by_method_warmup.png)

What this tests: whether warmup makes a candidate geometry usable immediately
after router reinitialization.

Observed result: all-position clustering and expert SVD improve with warmup,
but route-position and oracle controls remain highest.

Take-home: warmup helps representation/source quality, but the route-relevant
state selection problem remains open.

### Figure: Immediate Margin Lower Tail

![Immediate margin p05 after router reinit](figures/reinit_margin_p05_by_method_warmup.png)

What this tests: whether feature separation has a stable positive lower-tail
margin.

Observed result: route-position and oracle conditions have large positive
margins; all-position and raw/orthogonalized SVD stay negative. Common-projected
SVD becomes slightly positive at warmup 10/40.

Take-home: feature NMI alone overstates method readiness. Margin thickness is
still the decisive preservation guard.

### Figure: Common Alignment Diagnostic

![Expert/source row common alignment](figures/diagnostic_common_alignment_by_method_warmup.png)

What this tests: whether candidate rows align with the route common direction.

Observed result: raw expert SVD and orthogonalized SVD show higher common
alignment after warmup; common-projected SVD removes this component by design.

Take-home: common alignment is a plausible spectral failure component, but the
projection used here is only a controlled diagnostic, not a final method.

## Claim Boundary

Can claim:

- Warmup makes all-position hidden states and expert SVD directions more
  feature-aware on the uniform no-position slot dataset.
- Route-position centers remain the strongest tested source for clean
  feature-to-expert routing.
- Common-projected expert SVD is the best tested spectral candidate, while
  simple orthogonalization is not the solution.
- Slot-start leakage is not the visible explanation for the result.

Cannot claim:

- real-DCLM transfer;
- semantic expert formation;
- expert utility;
- a deployable MPI router;
- that all spectral router methods fail;
- that the tested common projection is the optimal common operator.

## Next Decision

Open a nested-learning aligned method anchor. The minimal question should be:

Can a multi-token or long-horizon auxiliary objective make route-relevant hidden
states feature-aware enough that delayed router reinitialization obtains both
high feature NMI and positive margin without needing label-known route-position
selection?

The completion guard should include feature NMI, margin p05, matched preserve
fraction, slot-start NMI, and target loss.
