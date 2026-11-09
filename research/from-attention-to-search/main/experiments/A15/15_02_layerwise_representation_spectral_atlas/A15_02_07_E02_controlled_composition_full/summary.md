---
experiment_id: A15_02_07_E02_controlled_composition_full
record_type: full_result_summary
status: COMPLETE
typed_outcome: insufficient_mixed
scientific_verdict: H1_INSUFFICIENT_H2_INSUFFICIENT
human_closed_book_judgment: confirmed_2026-08-09
---

# Full Result Summary: Controlled Composition 10-Layer Run

## Direct Result

The amended composition task passed its capability and representation guards, but neither H1 nor H2 was precise enough to adjudicate. H1 had a positive confirmation point estimate, \(T_{rank}=0.002114\), but its 95% paired-bootstrap interval was \([-0.002384,0.005226]\) and DEVELOPMENT reversed to \(-0.003608\). H2 had a positive point estimate, \(T_{CIG}=0.018523\) nats/example, but its interval was \([-0.050412,0.081052]\). The registered outcome is `insufficient_mixed`.

The late-layer composition pattern is a candidate signal, not a supported claim: update-only readability rises sharply at layer 25, but the normalized rank-centroid curve is non-monotonic and the conditional-gain uncertainty spans both signs.

## Metric Meaning

- \(R_\ell\) is the complex-minus-simple normalized variance-centroid difference in the layer's own descending parameter-rank order; positive means relatively later local ranks.
- \(T_{rank}\) compares median \(R_\ell\) on layers 25/29/33 against layers 1/5/9.
- Conditional information gain (`CIG`) is the confirmation cross-entropy improvement from adding \(\Delta n\) after freezing an \(n^{old}\) ridge readout. Negative values mean that the fitted increment hurts untouched confirmation performance.
- \(Disc(\Delta n)\) measures update-only linear readability and cannot by itself establish that the update contains information absent from \(n^{old}\).

## Decisive Evidence

| Clause | Registered point estimate | 95% paired-bootstrap interval | Split/guard check | Verdict |
| --- | ---: | ---: | --- | --- |
| H1: later normalized rank allocation | \(+0.002114\) | \([-0.002384,0.005226]\) | DEV \(-0.003608\); all guards pass | Insufficient |
| H2: later conditional novelty | \(+0.018523\) nats/example | \([-0.050412,0.081052]\) | all guards pass | Insufficient |
| Capability gate | simple 0.9902; complex 0.7578 | fixed thresholds 0.80 / 0.60 | confirmation | Pass |

![COMP ten-layer overlays and layer-block trends](figures/comp_10layer_overlay_and_block_trends.png)

The first four panels place all ten sampled layers on shared axes, separately for simple/complex and raw/normalized variance. The lower panels separate common rank relocation, the complex-minus-simple residual, update-only readability, and conditional novelty. Thick horizontal segments are descriptive medians for early 1/5/9, middle 13/17/21, late 25/29/33, and terminal 36. This post-hoc block view does not re-adjudicate the registered H1/H2 verdict.

| Layer block | Median complex/simple raw trace | Simple centroid | Complex centroid | Complex−simple \(R\) | Complex \(Disc(\Delta n)\) | Complex−simple CIG |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Early | 0.8127 | 0.4227 | 0.4312 | -0.0023 | -0.1951 | -0.0156 |
| Middle | 0.6514 | 0.4413 | 0.4293 | -0.0021 | -0.0056 | -0.0028 |
| Late | 0.4258 | 0.6804 | 0.6513 | -0.0002 | +0.6279 | +0.0029 |
| Terminal | 0.5107 | 0.5488 | 0.5509 | +0.0021 | +0.5806 | +0.0003 |

All overlay curves use a centered 129-rank arithmetic mean in the linear variance domain before `log10`; smoothing is display-only. The H2 panel uses a symmetric-log scale so negative early gains, near-zero values, and the positive layer-25 value remain visible together.

## Evidence-Based Knowledge Update

1. A model-capable, paired one-edge versus two-edge construction does not show a stable global movement of normalized variance toward later local parameter ranks. \(R_\ell\) alternates sign, the confirmation early/late contrast is small, and DEVELOPMENT reverses it.
2. The update alone exhibits a clear depth transition in readability: `Disc($\Delta n$)` is negative or near zero through layer 21 and becomes strongly positive at layers 25--36. This supports the limited observation that the terminal composition answer becomes linearly readable from the attention-induced update in late layers.
3. Readability is not yet conditional novelty. The complex CIG peaks at \(0.0801\) nats/example at layer 25, but early-layer corrections hurt confirmation and the eight replicate-level H2 effects are mixed. The wide interval means the data cannot distinguish a genuine late novelty transition from episode/readout variance.
4. Complex examples have lower raw between-class variance than simple examples at every sampled layer. The main treatment effect is therefore not a simple increase in total update variance.

## Claim Boundary

This run supports only late-layer **update readability** for the controlled terminal code. It does not support H1, does not establish conditionally new information, and does not show a gradual layer-by-layer shift. It cannot generalize to natural semantic hierarchy, free generation, nonlinear information, shared eigenvectors, causal MLP use, or training utility.

## Researcher Close-Out

- **Question:** In a capability-passing one-edge versus two-edge composition task, does the complex target move relatively toward later local MLP-parameter ranks with depth and add conditionally new linear information?
- **Direct result:** Not established. \(T_{rank}=+0.002114\) with interval \([-0.002384,0.005226]\) and a DEVELOPMENT sign reversal; conditional information gain is \(+0.018523\) nats/example with interval \([-0.050412,0.081052]\). Both clauses are `insufficient`.
- **Updated judgment:** The late attention-induced update makes the terminal composition code readable, but neither a stable complex-specific rank relocation nor information linearly new beyond the old state is supported. Shared depthwise spectral-shape change remains the object worth explaining.
- **Cannot claim:** COMP does not establish gradual semantic refinement, conditional novelty, nonlinear coding, native MLP use, a functional tail, or Router utility.
- **Next decision:** Close A15_02_07 jointly with TAX and allow only one A15_04 fixed-bank geometry test of whether the shared relocation aligns with the cross-layer parameter tail beyond equal-rank random, head, and middle controls.
