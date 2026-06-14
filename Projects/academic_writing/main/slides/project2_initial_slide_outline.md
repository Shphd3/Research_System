# Project 2 Initial Slide Outline

Working title:

```text
Auditing Initialization-Induced Routing Bias in Sparse MoE Routers
```

Presentation constraint:

```text
15 minutes, Week 16 presentation, course focus on core contributions and innovations.
```

Current claim boundary:

```text
This is ongoing research. The deck should present a mechanism audit and current understanding, not a completed MoE specialization method.
```

## Ghost Deck

1. Sparse top-1 MoE routing can look stable without proving useful expert specialization.
2. The current research reframes the problem as an audit of what routing evidence can and cannot prove.
3. Same-feature route consistency is easy to obtain, but it is a weak signal because collapse can satisfy it.
4. In the best non-collapsed early evidence, routing is mostly slot-aligned rather than $B_i$-aligned.
5. A shared hidden component creates an effective expert bias even when the router has no explicit bias term.
6. Fixed routed position and positional embedding are major causal sources of the step-0 common component.
7. Common-logit dominance is early, predictive, and intervention-relevant in the dot-product toy setting.
8. Slot-derived initialization and common-logit cancellation show that slot-level routing is reachable.
9. The updated hypothesis is a common-logit basin followed by sparse top-1 lock-in.
10. The current claim is diagnostic, not a full functional-specialization claim.
11. The next experiments should test label-free anti-common or anti-lock-in routing while preserving sparse top-1 routing.

## Slide-By-Slide Outline

| # | Slide title | Main exhibit placeholder | Speaker purpose | Source / figure need |
|---:|---|---|---|---|
| 1 | Auditing Initialization-Induced Routing Bias in Sparse MoE Routers | Title only | Name the project as an audit of routing bias, not a solved method. | Course requirement + current anchors |
| 2 | Sparse routing needs stronger evidence than route stability. | Minimal MoE routing diagram | Explain why stable expert assignment is not the same as specialization. | `05_04_02_dotproduct_common_logit_causality_anchor.md` |
| 3 | I separate route consistency, feature alignment, non-collapse, and utility. | Diagnostic ladder | Define the evidence ladder used throughout the talk. | `research_source_map.md`; `01_slot_context...anchor.md` |
| 4 | Same-feature consistency can be high even when routing is collapsed. | Feature-key consistency + load guard | Show why consistency alone is a false-positive-prone metric. | H0604a `feature_key_consistency_histogram.png`; `expert_load_distribution.png` |
| 5 | The strongest non-collapsed early structure is slot-aligned, not $B_i$-aligned. | Feature-axis NMI comparison | Explain the feature-axis audit and why NMI decides the route-feature association. | H0604b `feature_axis_nmi_comparison.png` |
| 6 | Ordinary top-1 becomes brittle when feature assumptions are relaxed. | P1/P3 negative-result table | Show that target learning can succeed while route structure remains collapsed or arbitrary. | A05_02 P1/P3 summaries |
| 7 | A shared hidden component acts like an implicit router bias. | Common-offset equation + P1/P2 result | Introduce the mechanism: $h_f=c+r_f$ and $w_e^Tc$ creates an expert-specific offset. | A05_03 common-offset summary |
| 8 | Fixed routed position is a major source of the step-0 common component. | Position-source decision table | Show the causal source audit: routed-position removal sharply reduces common ratio and early max-load. | A05_03 position-source ablation summary |
| 9 | Common-logit dominance predicts collapse and cancellation improves slot routing. | Round-2 evidence table | Present the strongest current mechanism evidence without overclaiming real-LM transfer. | A05_04_02 round-2 summary |
| 10 | The updated hypothesis is a common-logit basin followed by top-1 lock-in. | Mechanism chain | Synthesize the evidence into one mechanistic story. | `05_04_02_dotproduct_common_logit_causality_anchor.md` |
| 11 | The next step is label-free anti-common routing, not a broader benchmark. | Next-experiment decision list | End with a concrete next decision and claim boundary. | `05_04_02_dotproduct_common_logit_causality_anchor.md` |

## Claim Boundary For Slides

Can say:

- Route consistency is not sufficient evidence for feature-level expert specialization.
- In the tested toy setting, common-logit dominance is an early and intervention-relevant contributor to collapse.
- Slot-level routing is reachable under supervised slot initialization or common-logit cancellation.

Cannot say:

- Functional expert specialization is solved.
- Common-logit cancellation is a deployable method.
- The current evidence transfers to real language models, longer contexts, cosine routers, or broad MoE settings.
- Expert computation is causally specialized; the current strongest evidence is about routing assignment.

## Immediate Fill Policy

For the first PPT draft, fill only slide titles and outline-level placeholders. Add figures and full bullets only after the slide sequence is approved.
