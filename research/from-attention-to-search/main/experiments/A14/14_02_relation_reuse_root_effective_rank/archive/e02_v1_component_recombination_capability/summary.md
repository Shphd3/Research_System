---
experiment_id: A14_02_E02_component_recombination_capability
status: completed_fail
verdict: fail
run_id: a14_02_e02_component_recombination_capability_4gpu_20260723_full_v1
job_id: pt-zecsxjd8
companion_cn: summary_cn.md
---

# Summary: A14_02_E02 Component-Recombination Capability

Primary subanchor:
[historical A14_02_01 component-recombination anchor](/Projects/from-attention-to-search/main/problem_anchors/14_tree_low_rank_language_structure/14_02_relation_reuse_root_effective_rank/archive/e02_v1_component_recombination_capability/14_02_01_component_recombination_capability_anchor.md)

Protocol: [protocol.md](protocol.md) · [中文协议](protocol_cn.md)

## Direct Result

**The preregistered verdict is `fail`.** The generator audit passed and all
10 condition-seed jobs completed. Both conditions learned their seen
component pairs in new nuisance contexts:

- shared components: 5/5 capability passes, mean accuracy 0.9990;
- independent lookup: 5/5 capability passes, mean accuracy 0.9949.

The decisive shared unseen-pair test nevertheless passed in 0/5 seeds. Mean
accuracy was 0.2125, versus the registered 0.80 gate, and mean semantic
consistency was 0.9485, versus the 0.95 gate. Every held-out pair also failed
the registered 0.70 pair-mean guard.

The lookup control averaged 0.0640 on unseen pairs, close to answer chance
$1/17=0.0588$, and triggered no leakage guard.

## What This Establishes

This run separates base-task learning from recombination. The model can solve
seen mappings under disjoint test contexts, so the negative result is not
explained by failure to learn the seen task or by nuisance-context shift.
However, the registered shared task did not produce reliable reuse of
individually observed components in a new pairing.

Shared accuracy was descriptively above lookup in every paired seed, but it
ranged from 0.088 to 0.515 and never reached the capability threshold. This is
compatible with weak partial structure use; it is not evidence that the model
learned the intended compositional algorithm.

## Central Figure

![Capability before representation-rank interpretation](capability_before_rank.png)

The left panel confirms the matched seen-pair capability guard. The right
panel shows that no shared seed reached the unseen-pair capability gate.

## Aggregate Results

| Condition | Seen-pair passes | Mean seen accuracy | Recombination passes | Mean recombination accuracy |
| --- | ---: | ---: | ---: | ---: |
| Shared components | 5/5 | 0.9990 | 0/5 | 0.2125 |
| Independent lookup | 5/5 | 0.9949 | 0/5 expected | 0.0640 |

Shared held-out-pair mean accuracies were 0.1382, 0.2147, 0.2647, and 0.2324;
all were below the frozen 0.70 guard.

## Claim Boundary

Allowed:

> On this controlled NTP surface, diverse-context training was sufficient for
> seen-pair context invariance but insufficient for reliable recombination of
> held-out component pairs.

Not allowed: NTP cannot learn composition in general; the model used only
lookup memorization; shared rules lower or raise ROOT functional rank; the
conditional-rank theorem is false; natural language lacks hierarchy; or a
Router design follows from this result.

No representation rank was measured or interpreted in E02.

## Exactly One Next Decision

Decide whether to park the current A14_02 synthetic shared-versus-lookup
surface instead of authorizing a ROOT functional-rank comparison on a task
that failed its composition-capability gate.
