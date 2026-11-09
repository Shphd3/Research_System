# Summary: A15_13_E03 Qwen3-0.6B CLINC150 One-Layer Backward Hierarchical Router

Primary Anchor: [15_13_01_clinc150_one_layer_backward_hierarchical_router_anchor.md](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_13_semantic_supervision_middle_layer_formation/subanchors/15_13_01_clinc150_one_layer_backward_hierarchical_router_anchor.md)  
Frozen Protocol: [protocol.md](protocol.md)  
Detailed record: [detailed.md](detailed.md)  
Result status / eligibility: machine evidence complete and eligible; registered verdict `INSUFFICIENT`; researcher judgment pending

## Result Snapshot

**Verdict:** The registered learned backward hierarchy did **not** establish a reliable separability advantage over the matched flat 150-expert Router.

**What we established:** Qwen3-0.6B can learn the real CLINC150 task under the registered teacher gate, and all two-seed teacher, Dense, Flat, Oracle, and learned-hierarchy runs completed on 8 RTX 5090 GPUs. The learned hierarchy minus Flat primary effect was -0.0109 percentage points for seed 17 and +0.0440 points for seed 29. The pooled effect was +0.0166 points with a 95% interval of [-0.1618, +0.1922].

**What the experiment shows:** The effects disagree in sign and the interval crosses zero. The functional task guard passed, so the result is not explained by a large loss of final intent accuracy. Oracle was numerically above Flat in both seeds, but this was not the registered primary comparison and has no registered uncertainty test; it is a clue, not a conclusion.

**What we do next:** Proposed, awaiting researcher confirmation: do not scale this exact learned-chain recipe. If the line continues, first redesign the learned teacher-posterior chain so that it can reproduce the Oracle arm's numerical direction under the same one-layer setting.

## Decision-Bearing Setup

**Question:** Does final-layer semantic supervision, applied through the registered coarse-to-fine freeze-and-remove Router at one middle layer, make fine intent information more linearly separable than a matched flat Router?

**Treatment and control:** learned hierarchical backward chain (`HIER_BACKCHAIN`) versus a 150-expert top-2 flat Router (`FLAT150`), paired by teacher seed.

**Changed variable:** hierarchical parent-then-child routing with the parent path frozen and its discriminant row space removed from the child-gate input, versus a single flat fine-intent gate.

**Held fixed:** Qwen3-0.6B teacher, CLINC150 split, block 15 insertion point, residual scale, expert bottleneck, active two-expert fine stage, training passes, checkpoint rule, and seed.

**Primary metric and unit:** equally weighted mean over 10 domains of test macro-F1 from 15-way domain-local frozen linear probes on the post-block-15 representation, in percentage points.

**Known limitation:** two seeds and one dataset/model/layer cannot establish a general property of hierarchical semantic supervision or functional expert specialization.

## Verdict Basis

| Registered rule | Observed value | Guard / eligibility | Verdict | Evidence source |
| --- | --- | --- | --- | --- |
| Both paired seed effects must be positive | seed 17: -0.0109 pp; seed 29: +0.0440 pp | complete paired seeds | Not met | [Detailed evidence](detailed.md) |
| Pooled 95% interval lower bound must exceed zero | +0.0166 pp; 95% interval [-0.1618, +0.1922] | 10,000 intent-stratified paired draws | Not met | [Detailed evidence](detailed.md) |
| Final intent macro-F1 loss must be no worse than -1 pp in either seed | -0.4297 pp; +0.1717 pp | guard passed in both seeds | Passed | [Detailed evidence](detailed.md) |
| Required artifacts and resources must be complete | all required rows present; 8 RTX 5090 GPUs; no H100 | completion audit passed | Eligible | [Detailed evidence](detailed.md) |

## Key Evidence

| Condition | Seed 17 probe F1 (%) | Seed 29 probe F1 (%) | Two-seed mean (%) |
| --- | ---: | ---: | ---: |
| Teacher before stage two | 92.2889 | 91.9919 | 92.1404 |
| Dense continuation | 92.2301 | 91.9927 | 92.1114 |
| Flat-150 | 92.2569 | 92.0364 | 92.1467 |
| Hier-Oracle | 92.3394 | 92.1649 | 92.2521 |
| Hier-Backchain | 92.2461 | 92.0804 | 92.1632 |

## Central Figure

![Paired learned hierarchy versus flat effect](figures/primary_backchain_vs_flat.png)

The dashed line is no difference. The two seed effects fall on opposite sides, and the pooled 95% interval crosses the line. This figure supports only the registered `INSUFFICIENT` verdict; it does not prove that all hierarchical supervision is ineffective.

## Claim Boundary

**Can claim:** under this exact Qwen3-0.6B, CLINC150, block-15, two-seed protocol, the learned backward hierarchical Router did not demonstrate a reliable linear-separability improvement over the matched flat Router.

**Cannot claim:** hierarchy is generally useless; semantic supervision cannot shape representations; Oracle is truly superior; X-MoE representation collapse improved; the Router experts became functionally specialized; or the result transfers to other layers, datasets, or model sizes.

## Next Decision

**Decision:** proposed, awaiting researcher confirmation: stop scaling the unchanged `HIER_BACKCHAIN` recipe and require a learned-supervision repair that first closes the descriptive Oracle-versus-learned gap.

**Completion criterion:** a repaired learned chain must again satisfy both positive paired-seed effects, a pooled interval lower bound above zero, and the -1 pp final-task guard under a newly frozen protocol.

**Resume action:** if confirmed, define one mechanism-changing repair; do not add seeds or model size to the unchanged recipe as a substitute for that repair.
