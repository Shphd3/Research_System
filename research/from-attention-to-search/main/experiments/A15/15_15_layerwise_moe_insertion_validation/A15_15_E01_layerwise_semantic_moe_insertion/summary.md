# Summary: A15_15_E01 Layerwise Semantic MoE Insertion

Primary Anchor: [A15_15](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_15_layerwise_moe_insertion_validation/15_15_layerwise_moe_insertion_validation_anchor.md)

Frozen Protocol: [protocol.md](protocol.md)

Detailed evidence: [detailed.md](detailed.md)

Result status: `FULL_RUN_COMPLETE`; `AI_DRAFT_AWAITING_HUMAN_CONFIRMATION`

Registered typed verdict: `INSUFFICIENT`

## Result Snapshot

Block 9 makes the supervised causal Router substantially more semantic than block 1, but it does **not** reliably make the MoE more useful. In the main learned-routing arm, the block-1 minus block-9 Oracle-gap interaction is `+0.000625` nat/token for seed 17 and `-0.000911` for seed 29. The signs disagree, so the registered layer-selection hypothesis does not pass. Static readability can currently nominate a layer where labels are easier to route, but cannot select the functionally better MoE insertion point.

The missing Flat Oracle is now complete. It improves mean answer-token NLL from the matched Flat task-only model's `0.831329` to `0.825400`, and the internal eight-task average from `0.136719` to `0.152344`. However, it remains worse than hierarchical task-only (`0.806323` NLL) and hierarchical Oracle (`0.794920` NLL). Correct flat grouping has value, while the hierarchical topology retains the stronger task result in this setup.

## What Actually Ran

- One replacement ACP job, `pt-lxue71oe`, completed on one reserved four-H100 node. The first job `pt-owrlkt10` stopped before training on a false-positive frozen-gradient audit and is excluded.
- The M2D2 experiment is genuinely staged. Stage 1 trains shared LoRA, parent experts, and the parent Router for 144 updates. Stage 2 freezes the parent Router, keeps parent experts trainable in the main arm, and trains shared LoRA plus child experts and child Router for another 144 updates. The frozen-parent-expert arms freeze both parent Router and parent experts.
- All 12 stage-one checkpoints, 24 final layer-study checkpoints, 2 Flat Oracle checkpoints, 96 layer intervention arrays, 6 Flat intervention arrays, and 1,024 Flat benchmark predictions are present. The completion audit returned `FULL_RUN_COMPLETE`.

## Decisive Evidence

| Seed | Learned−Oracle gap, block 1 | Learned−Oracle gap, block 9 | Block 1−block 9 interaction |
|---:|---:|---:|---:|
| 17 | `0.001919` | `0.001294` | `+0.000625` |
| 29 | `0.002510` | `0.003420` | `-0.000911` |
| Mean | `0.002214` | `0.002357` | `-0.000143` |

![Primary layer interaction](figures/01_primary_layer_interaction.png)

How to read: positive interaction favors block 9 and negative interaction favors block 1; the two seeds point in opposite directions.

The frozen static probe recovery rises from `0.599/0.662` at block 1 to `1.000/1.000` at block 9 for coarse/fine labels. The learned online Router follows that ordering: mean coarse/fine route accuracy rises from `0.505/0.393` to `0.687/0.485`, and joint normalized mutual information rises from `0.0677` to `0.2050`.

![Readability and route accessibility](figures/04_readability_and_route_accessibility.png)

How to read: block 9 is clearly better in both frozen label readout and learned route-label agreement; this is a mechanism diagnostic, not task gain.

Expert-function interventions do not show a uniform block-9 advantage. In the learned main arm, deletion is larger at block 9 (`0.000140` versus `0.000100`), but the two wrong-fine substitutions are smaller (`0.000077/0.000109` versus `0.000105/0.000143`). Oracle intervention effects are larger overall and are stronger at block 1.

![Expert function by layer](figures/05_expert_function_by_layer.png)

How to read: with the same vertical scale, learned-path bars remain tiny and block 9 does not dominate all three interventions.

## Ablation Result

Freezing parent experts in stage 2 worsens NLL in both layers and both seeds: the mean penalty is `+0.000924` at block 1 and `+0.000724` at block 9 under native input. Removing the centered parent-Router row space has effects near zero and changes sign across seeds or freeze settings. The supported implementation remains: freeze the parent Router, keep parent experts trainable, and do not subtract the parent-Router row space by default.

![Ablation effects](figures/06_ablation_effects.png)

How to read: bars above zero are worse than native input with trainable parent experts; freezing has a consistent cost, while row-space removal is negligible and unstable.

## Flat Oracle Closure

| Model | Mean answer-token NLL ↓ | Mean internal eight-task score ↑ |
|---|---:|---:|
| Flat task-only | `0.831329` | `0.136719` |
| **Flat Oracle** | **`0.825400`** | **`0.152344`** |
| Hierarchical task-only | `0.806323` | `0.158203` |
| Hierarchical Oracle | `0.794920` | `0.165039` |

![Flat Oracle closure](figures/03_flat_oracle_closure.png)

How to read: lower NLL is better; Flat Oracle improves its matched Flat baseline, but both hierarchical references remain lower.

## Claim Boundary And One Next Decision

The experiment establishes that block 9 exposes labels more accessibly to a supervised causal Router. It does not establish that block 9 is a better functional insertion point, that static readability alone should select MoE layers, or that block 9 is globally optimal. The static E15 nomination also remains formally unqualified because of its `0.000132`-nat shuffled-child guard miss.

The one proposed next decision is to retain static readout only as a cheap candidate generator and require a small functional pilot before choosing a layer. If this rule is to be tested further, the minimal next experiment should add one intermediate-readability block and two additional seeds rather than declare block 9 from the present two-layer contrast.

## Evidence Map

- [Per-model layer NLL](tables/01_layer_nll.csv)
- [Route metrics](tables/02_layer_route_metrics.csv)
- [Expert interventions](tables/03_layer_interventions.csv)
- [Registered interaction](tables/04_layer_interaction.csv)
- [Flat Oracle results](tables/05_flat_oracle.csv)
- [Typed verdict](tables/verdict.json)
- [Completion audit](tables/completion_audit.json)
