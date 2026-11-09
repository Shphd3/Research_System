---
experiment_id: A15_11_E03_counterfactual_utility_residual_tree
status: EVIDENCE_COMPLETE_AI_INTERPRETATION_AWAITING_HUMAN_CONFIRMATION
completed: 2026-08-29
resource: 8xRTX5090_SPOT
primary_job: pt-0aopddjj
---

# Summary: Counterfactual-Utility Residual Tree

Primary Anchor: [A15_11 Anchor](../../../../problem_anchors/15_spectral_representation_and_functional_routing/15_11_gradient_consistent_hierarchical_routing/15_11_gradient_consistent_hierarchical_routing_anchor.md)
Frozen Protocol: [protocol.md](protocol.md)
Detailed record: [detailed.md](detailed.md)

## Result Snapshot

All registered identity, oracle, pairing, numerical, rank, ancestor-projection,
freeze, mask, parameter, candidate-compute, and completion guards pass over
eight paired optimizer seeds. The layered result is:

| Question | Registered verdict | Direct reading |
| --- | --- | --- |
| Does the advisor mechanism distinguish aligned work from permuted fail? | `MECHANISM_SUPPORTED` | yes |
| Does counterfactual-utility supervision improve the tree? | `NO_UTILITY_EFFECT_TREE` | no; it is worse in work |
| Does it improve the flat nonlinear model? | `NO_UTILITY_EFFECT_FLAT` | no established gain |
| Does the tree beat the matched flat model with task loss? | `NO_TREE_ADVANTAGE_TASK_ONLY` | no |
| Does the tree beat it with utility supervision? | `NO_TREE_ADVANTAGE_UNDER_UTILITY` | no; flat is better |
| What happens under the wrong grouping? | `PASS_FAIL_FLAT_ADVANTAGE` | flat avoids the tree's structural floor |
| Overall architecture reading | `GENERIC_NONLINEARITY_OR_UTILITY_SUFFICIENT` | retain the theorem, reject an empirical tree advantage |

The task-only hierarchical model has median endpoint normalized mean-squared
error (NMSE) \(2.30\times10^{-5}\) in work and 0.33698 in fail. Its paired
fail-minus-work learning-curve-area contrast is 0.05406 with 95% interval
[0.05220, 0.05537]. Thus training realizes the exact aligned decomposition and
retains the registered \(1/3\) failure floor under the wrong first split.

Direct per-token utility supervision does not help. In work,
\(S_H=AULC(H_{task})-AULC(H_{util})=-0.03860\) with 95% interval
[-0.06842, -0.00685], and the utility tree's endpoint median is 0.41693.
Seven of eight utility-tree seeds fail to reach the near-zero solution. The
matched flat task-only and utility models both reach near-zero median error,
so neither extra utility labels nor the provided hierarchy are needed for this
four-leaf problem.

![Noise-free NMSE learning curves](figures/nmse_learning_curves.png)

## Bottom-Level Failure Localization

**Direct evidence:** in work, the task-only tree finishes with balanced leaf
load 0.25/0.25/0.25/0.25, utility-target and hidden-probe balanced accuracy
1.0, and positive normalized fifth-percentile margins. The utility tree has
median minimum leaf load 0, native-Gate and frozen-hidden-probe balanced
accuracy 0.625, and normalized fifth-percentile margins -0.478 and -0.586.

**AI inference awaiting human confirmation:** the immediate utility target

\[
\arg\max_e\left(2r_i^\top W_ez_i-\|W_ez_i\|^2\right)
\]

depends on the sampled content vector \(z_i\) and the evolving expert matrices,
while the hierarchical Router observes only \(p\) at level one and \(q\) inside a
deployed parent at level two. Before experts specialize, the best-expert label
therefore need not be a single-valued function of the Router-visible
representation. Stop-gradient hard labels can amplify accidental winners,
starve alternatives, and prevent the utility relation from becoming
separable. The equally poor hidden probe argues against blaming only the
native Gate optimizer. This is a localized explanation, not yet a proven
causal result; the smallest successor would supervise conditional expected
utility rather than instantaneous per-sample utility.

## Claim Boundary

### Can claim

- the advisor's staged common→freeze→functional-residual→1→2→4 mechanism is
  realizable when the supplied grouping matches the rank-one function
  decomposition;
- the same tree keeps its analytic \(1/3\) floor when the first split is wrong;
- generic nonlinear flat routing solves both permutation-equivalent teachers;
- the registered instantaneous hard utility supervision adds no benefit and
  destabilizes the aligned tree under this training contract.

### Cannot claim

- progressive hierarchy has an empirical efficiency advantage over a matched
  flat nonlinear Router;
- counterfactual utility supervision is generally harmful;
- natural-language semantics supply the correct tree;
- the hierarchy can be learned rather than provided;
- a Qwen intervention will improve language-model loss;
- hard ancestor-orthogonal deletion is safe for non-orthogonal real tasks.

## Next Decision

Do not promote the current `H_util` design into Qwen. The bounded next research
question is whether **Router-measurable expected utility**—utility averaged or
softly distilled conditional on the exact Router-visible representation—can
avoid moving-label collapse under the same progressive experts. This proposal
requires human confirmation and a successor Focus/Protocol.
