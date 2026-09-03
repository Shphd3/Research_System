# Detailed Record: A15_13_E12 M2D2 Coarse-Removal And Parent-Freeze Ablation

## Provenance

- Canonical ACP job: `pt-l9txxpze`
- Resource: one reserved `n6ls.iu.i40.4` worker with four H100 GPUs
- Canonical run root: `/data/250010109/MoE_Router/experiments/20260902_a15_13_e12_m2d2_decommon_parent_freeze/runs/full-20260902T185330Z`
- Tests: `5/5` passed.
- Completion: two stage-one checkpoints, eight stage-two checkpoints, and `32/32` confirmation evaluations; all arrays finite.
- Aggregate SHA-256: `21e9547a4c4c598f1a8c1eabbb5285f9848f847583efeaca89ad0a1431476eb9`
- Completion-audit SHA-256: `f94047f30e101a2b8b307500311b5c4342a611160439d7fb067efbeb449891da`

An earlier full run under stamp `20260902T180855Z` completed all scientific training and confirmation evaluations, but its learning-curve evaluator selected the first 576 domain-ordered development examples rather than 64 examples from each of nine domains. Its final full-confirmation results agree with the canonical rerun, but its curves are ineligible. The canonical run above uses an explicitly tested equal-domain development index.

## Model And Factors

Qwen3-0.6B-Base and the language head were frozen. Block 14 contained one shared rank-eight LoRA, three coarse rank-eight experts, nine fine rank-eight experts, one coarse Router, and parent-conditional fine Routers.

The stage-two factorial design was:

| Code | Fine Router input | Coarse Router | Coarse experts |
| --- | --- | --- | --- |
| `SEM_R0_F1` | native causal block-14 state | frozen | frozen |
| `SEM_R1_F1` | state minus centered coarse-Router row space | frozen | frozen |
| `SEM_R0_F0` | native causal block-14 state | frozen | trainable |
| `SEM_R1_F0` | state minus centered coarse-Router row space | frozen | trainable |

The removal operator computes the SVD basis of `parent_router.weight - row_mean` and subtracts the state's projection onto the non-zero right-singular directions. With three coarse classes, this removes at most two linear directions. It does not remove all information statistically associated with coarse labels.

## Factorial Effects

Positive means lower confirmation NLL.

| Factor | Seed 17 | Seed 29 | Direction audit |
| --- | ---: | ---: | --- |
| Remove coarse row space | `+0.0000126` | `-0.0000619` | inconsistent; unsupported |
| Keep coarse experts trainable | `+0.0004616` | `+0.0002693` | positive in both seeds |
| Interaction | `-0.0000095` | `+0.0001075` | inconsistent |

No bootstrap interval was registered for E12. With only two seeds, the parent-update result is evidence of a small repeatable effect, not a precise population effect size.

## Functional Interventions

Changed-minus-intact confirmation NLL was tiny. For the original branch, deletion averaged `+0.0000588`, wrong-one averaged `+0.0000257`, and wrong-two averaged `+0.0000803`. In the remove-coarse plus trainable-parent branch, wrong-one and wrong-two averaged `-0.0000538` and `-0.0000551`. These sign reversals rule out a stable claim that the ablations improved fine-expert non-interchangeability.

## Loss-Oscillation Audit

For every ablation and both seeds, the correlation of update-to-update raw-loss changes with the original branch was `0.999994--0.999995`. Architecture changes this small cannot independently generate almost identical spikes at the same update. The spikes therefore track the shared sequence of easy and hard M2D2 minibatches. The equal-domain fixed-development checkpoints provide the eligible learning curve.

## Artifact Map

- Aggregate: `/data/250010109/MoE_Router/experiments/20260902_a15_13_e12_m2d2_decommon_parent_freeze/runs/full-20260902T185330Z/analysis/aggregate.json`
- Completion audit: `/data/250010109/MoE_Router/experiments/20260902_a15_13_e12_m2d2_decommon_parent_freeze/runs/full-20260902T185330Z/completion_audit.json`
- Histories and checkpoints: `.../stage1/` and `.../conditions/`
- Confirmation arrays: `.../evaluations/*.npz`
- Curated figures: [final effect](figures/m2d2_ablation_final_nll.png), [fixed-development curves](figures/m2d2_fixed_dev_learning_curves.png), [oscillation audit](figures/m2d2_loss_oscillation_diagnostic.png)

## Bounded Interpretation

The parent-update effect says that preserving plasticity in the already learned coarse computation helps slightly during fine-stage language fitting. It does not say the coarse semantic partition improved: the coarse Router stayed frozen, route NMI did not rise, and fine-expert interventions were not stable. The tested subtraction also fails to improve either task NLL or route NMI, so it should be dropped as a default rather than generalized into a claim about all common-information removal methods.
