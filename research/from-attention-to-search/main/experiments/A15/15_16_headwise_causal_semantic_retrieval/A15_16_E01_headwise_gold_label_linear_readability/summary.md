# Summary: A15_16_E01 headwise gold-label linear readability

Primary Anchor: [A15.16](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_16_headwise_causal_semantic_retrieval/15_16_headwise_causal_semantic_retrieval_anchor.md)  
Frozen Protocol: [Protocol](protocol.md)  
Detailed record: [Detailed](detailed.md)  
Result status / eligibility: `FULL_RUN_COMPLETE`; primary evidence `ELIGIBLE`; knowledge wording `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

## Result Snapshot

**Registered verdict:** `NO_REPRODUCIBLE_HEAD_HETEROGENEITY`.

The development selector chose zero-indexed block 20 and query heads `[4,5,13,7]` for both parent and conditional-child labels. On confirmation, those four heads retained large positive gain over the remaining 12: parent `0.300311` nat with 95% bootstrap interval `[0.293544,0.306483]`, and child `0.354685` nat with `[0.347546,0.362285]`; all four probe seeds were positive.

The registered search-corrected permutation gate nevertheless failed for both tasks. Parent spread was `0.401876` versus development null `0.843293` and `0.384120` versus confirmation null `0.836393`. Child spread was `0.460696` versus development null `1.353921` and `0.474199` versus confirmation null `1.326489`. All four one-sided permutation p-values were `1.000`.

Coarse and conditional-fine head rankings were almost identical rather than specialized by granularity: mean layerwise Spearman correlation was `0.971534`; 21/28 layers had complete top-four overlap, and block 20 had overlap `4/4` with correlation `0.988235`.

**What we established:** the same head-quality pattern repeats strongly from development to confirmation, but the registered null does not qualify it as label-specific head heterogeneity. The data do not support assigning different coarse and fine semantic roles to different heads.

**What we do next:** the researcher reviews this four-part result and decides whether Phase 2 should test whether the shared high-readability heads selectively retrieve information beyond a causal-history baseline, or whether the head-resolved route should stop.

## Decision-Bearing Setup

- **Question:** are real parent and within-parent child labels unequally readable from the actual retrieval output of individual attention query heads?
- **Treatment and controls:** true labels versus 2,000 window-label permutations; development-selected top four heads versus the other 12 on untouched confirmation.
- **Changed variable:** query-head identity within a block.
- **Held fixed:** frozen Qwen3-0.6B-Base, M2D2 `3×3`, positions 63--254, 128-dimensional head vector, affine probe capacity, three passes, four seeds, and window-first cell-balanced aggregation.
- **Primary metric:** within-layer 90th-minus-10th percentile spread of \(\log3-\mathrm{CE}\), in nats.
- **Known limitation:** the registered evaluation-time label permutation creates very large wrong-label cross-entropies for confident fitted probes. It is a conservative frozen gate; the top-four confirmation result cannot override it.

## Verdict Basis

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
|---|---:|---|---|---|
| Parent development spread exceeds max-over-layer null | `0.401876 < 0.843293`, `p=1.000` | 2,000 window permutations | fail | [selected tests](tables/selected_head_tests.csv) |
| Parent confirmation spread exceeds fixed-layer null | `0.384120 < 0.836393`, `p=1.000` | frozen block 20 | fail | [selected tests](tables/selected_head_tests.csv) |
| Parent frozen top-four advantage is positive | `0.300311 [0.293544,0.306483]` | all four seeds positive | pass, secondary only | [selected tests](tables/selected_head_tests.csv) |
| Child development spread exceeds max-over-layer null | `0.460696 < 1.353921`, `p=1.000` | 2,000 within-parent permutations | fail | [selected tests](tables/selected_head_tests.csv) |
| Child confirmation spread exceeds fixed-layer null | `0.474199 < 1.326489`, `p=1.000` | frozen block 20 | fail | [selected tests](tables/selected_head_tests.csv) |
| Child frozen top-four advantage is positive | `0.354685 [0.347546,0.362285]` | all four seeds positive | pass, secondary only | [selected tests](tables/selected_head_tests.csv) |

## Key Evidence

![Head heterogeneity and frozen null thresholds](figures/02_head_spread_and_nulls.png)

How to read: the real development and confirmation curves nearly coincide, but the registered cross markers for the permutation thresholds lie far above block 20 for both tasks; therefore the formal heterogeneity gate fails.

![Coarse versus conditional-fine head profiles](figures/04_coarse_fine_head_profiles.png)

How to read: correlations stay above `0.92`, and the two tasks share three or four of their top four heads in 27/28 layers; this is a shared readability ranking, not evidence for separate coarse and fine head roles.

## Claim Boundary

**Can claim:** the fitted per-head linear readouts show a strongly repeated descriptive ranking, with the same block-20 top four heads retained exactly on confirmation; the pre-registered null qualification fails; coarse and fine head rankings are nearly identical.

**Cannot claim:** label-specific attention-head specialization, selective retrieval beyond available history, native causal use, a useful KV-cache selector, an expert insertion location, LoRA/MoE function, or next-token improvement.

## Next Decision

**Decision:** after reviewing the four-part result, decide whether to authorize a complete Phase-2 design that separates causal-history availability from actual attention selection and adds a minimal intervention.

**Completion criterion:** the researcher explicitly accepts either (a) proceed only as a test of the shared high-readability heads, without calling them coarse/fine specialists, or (b) stop the head-resolved route.

**Resume action:** if (a), draft a new frozen Protocol before implementation; if (b), close this Focus without further execution.
