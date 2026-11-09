# Summary — A12_0_E01 Calibration

## Result Snapshot

**Verdict: insufficient evidence; the capability gate failed.** All 24 calibration runs completed, but no model depth made both NTP and MTP reliably learn the two-step held-out-rule-pair task across the two calibration seeds. Therefore no answer-accuracy threshold should be selected from this run, and the reserved confirmation seeds remain untouched.

The single-step control reached `1.0` final test standard-head answer accuracy in every condition. The two-step task did not: the strongest 4-layer condition was unstable across NTP seeds (`0.2969`, `0.9375`), while both 4-layer MTP seeds remained partial (`0.3008`, `0.2539`). The 1-layer and 2-layer two-step conditions were also partial. This is a capability result, not evidence that composition depth helps or harms MTP.

## Terminology / Definitions

| Term | Concrete meaning | Why it decides this stage | What it cannot prove |
|---|---|---|---|
| Standard-head answer accuracy | Accuracy of the common next-token head \(q_1\) at `SHARED`, predicting `ANSWER_Y`. | It is the shared behavioral surface for NTP and MTP. | Causal use of the intermediate state. |
| Capability gate | Both objectives must learn both task structures reliably at the same model scale. | Without it, steps-to-threshold is not a valid objective comparison. | Perfect equality of task difficulty. |
| Calibration | Two seeds used to expose learnability and choose future decision constants. | It may block or prepare confirmation. | It cannot confirm the mechanism hypothesis. |
| Chance accuracy | \(1/32=0.03125\) for the 32 answer states. | Distinguishes total failure from partial learning. | Accuracy above chance is not task mastery. |

## Exact Comparison

All conditions used fixed nine-token sequences, 32 states, eight fixed bijective rules, the same 48/8/8 ordered-rule-pair split, width 128, four attention heads, feed-forward width 512, batch size 512, AdamW, MTP second-head weight 1, 20,000 steps, and seeds 1201–1202. One layer was diagnostic; two and four layers were the intended decision scales.

## Primary Result

Final test standard-head answer accuracy:

| Layers | Task | NTP seed 1201 | NTP seed 1202 | MTP seed 1201 | MTP seed 1202 | Capability status |
|---:|---|---:|---:|---:|---:|---|
| 1 | single | 1.0000 | 1.0000 | 1.0000 | 1.0000 | control learned |
| 1 | two-step | 0.1797 | 0.1367 | 0.1367 | 0.2148 | failed |
| 2 | single | 1.0000 | 1.0000 | 1.0000 | 1.0000 | control learned |
| 2 | two-step | 0.1016 | 0.0820 | 0.1211 | 0.0781 | failed |
| 4 | single | 1.0000 | 1.0000 | 1.0000 | 1.0000 | control learned |
| 4 | two-step | 0.2969 | 0.9375 | 0.3008 | 0.2539 | failed; seed-unstable |

The chosen primary metric, steps to a common accuracy threshold, is intentionally **not computed**. The threshold was left unset, and no scale passed the prerequisite needed to make threshold crossing interpretable.

## Key Figure

![A12_0 calibration learning curves](figures/a12_0_calibration_learning_curves.png)

The solid line is the mean test standard-head answer accuracy across the two calibration seeds; the band spans the two seeds. The left column shows that every single-step condition learns quickly. The right column shows failure at one and two layers and a large NTP seed split at four layers. The figure has no threshold line because none was selected.

**Take-home:** increasing capacity to four layers makes the two-step workload learnable in one NTP trajectory, but does not produce a reliable shared capability surface for comparing NTP and MTP.

**What the figure does not show:** it does not establish that NTP is better than MTP, that MTP suppresses composition, or that an intermediate state is or is not causally used. The objective weight changes backward gradients, and the held-out rule-pair requirement adds a composition-generalization burden.

## Claim Boundary

Supported now:

- the implementation and four-GPU execution path are valid;
- the single-step control is learnable at all three depths;
- the current two-step carrier does not pass the cross-objective, cross-seed capability gate;
- threshold selection and confirmation must remain blocked.

Not supported:

- any positive or negative MTP advantage;
- a composition-depth interaction in steps to threshold;
- causal formation or use of the intermediate state;
- a conclusion about pretrained models, code, planning, or natural language.

## Exactly One Next Decision

Decide whether to replace the held-out ordered-rule-pair requirement with an in-support capability calibration while preserving the same fixed-length single-step/two-step comparison. This removes composition generalization as an extra burden, but weakens the claim from rule-pair generalization to learning the controlled training distribution.
