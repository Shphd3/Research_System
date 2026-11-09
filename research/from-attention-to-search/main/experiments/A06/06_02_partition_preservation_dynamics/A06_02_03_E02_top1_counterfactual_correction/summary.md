# Summary: A06_02_03_E02 Top-1 Counterfactual Correction Dynamics

Primary anchor: `../../../../problem_anchors/06_geometry_proxy_preservation/06_02_partition_preservation_dynamics/06_02_partition_preservation_dynamics_anchor.md`

Protocol: `protocol.md`

## Result Snapshot

**Verdict: supported, with an important correction to the prior wording.**

**What we established:** Weighted top-1 does have a correction mechanism, but it does not directly compare the utilities of unselected experts. Recovery therefore behaves like rank-ordered boundary search rather than direct expert identification.

**What the experiment shows:** When the useful expert began at rank 4, soft routing corrected in 30 steps, while weighted top-1 corrected in 153 steps and crossed 142 routing boundaries. All cells eventually corrected by step 200, so the supported claim is weak and rank-mediated correction, not permanent lock-in.

**What we do next:** Model preservation as the interaction between this correction delay and a signed signal/background margin budget.

## Purpose

The run tests whether wrong top-1 assignments are hard to correct because the task path cannot identify the best currently unselected expert.

## Terminology / Definitions

| Term | Meaning | Computation | Why it matters | Cannot prove |
| --- | --- | --- | --- | --- |
| Initial rank | Position of the useful expert in the router score ordering | 1, 2, or 4 | Controls how many alternatives precede it | Natural initialization frequency |
| Correction step | First step where the useful expert becomes top-1 | integer 0-200 | Measures correction latency | Permanent stability |
| Boundary count | Number of selected-expert changes | count | Reveals sequential search | Utility of the final route |
| Unselected utility gap | Update toward useful unselected expert minus other unselected experts | projected row update | Tests counterfactual discrimination | Full optimization efficiency |

## Exact Setup

- Four orthogonal frozen feature centers and four fixed class-specialized experts.
- Exact router score matrices place the useful expert at rank 1, 2, or 4.
- Soft-mixture versus weighted-top-1 output.
- Router-only full-batch SGD, learning rate 0.2, 200 steps.
- 32 seeds, run on two local H100 GPUs.

## Primary Metric And Result

| Router | Rank 1 | Rank 2 | Rank 4 | Rank-4 minus rank-2 penalty |
| --- | ---: | ---: | ---: | ---: |
| Soft | 0 | 7 | 30 | 23 |
| Weighted top-1 | 0 | 12 | 153 | 141 |

Every feature-seed cell corrected by step 200. The top-1 excess rank penalty over soft routing was 118 steps.

At rank 4, the one-step unselected utility gap was `+0.02167` for soft routing and `-0.00736` for weighted top-1. The top-1 path initially favors higher-ranked alternatives rather than the useful rank-4 expert.

## Key Figure

![Correction time grows sharply with initial rank under weighted top-1](figures/correction_time_by_initial_rank.png)

**How to read:** Higher values mean slower identification of the useful expert.

**Observed result:** Both methods slow with rank, but the top-1 rank-4 delay is much larger.

**Take-home:** Top-1's problem is not zero router gradient. It is missing utility-specific comparison among unselected experts.

**What this does not prove:** Permanent lock-in, superiority of soft routing in a trainable MoE, or production top-1 behavior.

## Claim Boundary

**Can claim:** In this weighted-top-1 controlled model, wrong-route correction is rank-mediated and much slower than soft utility-directed correction.

**Cannot claim:** Top-1 can never recover. It recovered every tested cell by step 200.

## Next Decision

Test whether common/background updates consume the finite margin faster than this rank-mediated correction can rebuild it.
