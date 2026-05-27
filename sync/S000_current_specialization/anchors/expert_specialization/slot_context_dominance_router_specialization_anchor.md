---
parent_node: problem.moe_expert_specialization
---

# Slot-Context Dominance for Gating-Induced Expert Specialization

## Question

Can stronger slot context plus slot-centroid router initialization make standard top-1 MoE form slot-aligned routing and slot-specific expert utility?

The sharper subproblem is:

```text
When the same B token has different next-token targets under four different slots,
does increasing the slot context signal in the B hidden state make the gate route by slot rather than by B token identity?
```

This is a child problem of MoE expert specialization. It belongs under the diagnostic line:

```text
why ordinary gating does not produce stable functional specialization
```

It does not solve real-corpus specialization, KV-cache reverse indexing, or new MoE architecture design. It only tests whether the previous failure can be explained by weak slot signal in the gate input.

## Physical Prior

The first physical prior is:

```text
A router can specialize by a feature only if that feature is visible in the router input and useful for the loss.
```

For a B token under slot `s`, the gate input can be decomposed as:

$$
h_{i,s}^{(m)} = c_i + \beta_m u_s + \epsilon
$$

where:

```text
c_i: B token identity component
u_s: slot/context component
m: slot prefix length or context strength
beta_m: strength of slot information at the B position
```

If `beta_m` is small, routing may be dominated by `c_i`. If longer context increases `beta_m`, slot may become a viable routing axis.

Physical meaning: In the real world, long context may strengthen a task-relevant factor in the hidden state, but this alone does not imply that the learned router will use that factor as the expert partition.

The second prior is:

```text
Routing alignment is not enough; the assigned expert must have causal utility for that slot.
```

Therefore the experiment must measure both routing assignment and expert utility.

## Mechanistic Motivation

Previous initialization experiments show that semantic or context initialization can create early routing alignment, but this alignment decays during NTP training. They also show that semantic boundaries can be recoverable in hidden states while the learned router does not use them as stable functional routes.

This leaves one unresolved explanation:

```text
Maybe the slot signal at the B position was too weak or too short, so B token identity dominated the router update.
```

This anchor tests that explanation directly by strengthening the slot context while keeping the same top-1 MoE mechanism.

## Mathematical Modeling

Use four slots and four experts:

$$
s\in\{0,1,2,3\}, \qquad e\in\{0,1,2,3\}
$$

The same token `B_i` appears under every slot:

$$
x_{i,s}=(C_s^{(m)}, B_i)
$$

The target is slot-dependent:

$$
y_{i,s}=\pi_s(B_i)
$$

with:

$$
y_{i,0},y_{i,1},y_{i,2},y_{i,3}\ \text{distinct for the same}\ B_i.
$$

Thus `B_i` alone cannot determine the target. The slot must disambiguate the prediction. So the setting builds a criteria where slots matters more than the B_i identity itself.

The top-1 router is:

$$
p=\operatorname{softmax}(Wh_{i,s}), \qquad r_{i,s}=\arg\max_e p_e
$$

Functional expert utility is:

$$
\Delta CE(s,e)=CE_s(\operatorname{ablate}(e))-CE_s(\operatorname{full})
$$

The primary metric is assignment-utility agreement:

$$
A= P(r_{i,s}=\arg\max_e \Delta CE(s,e)\mid s)
$$

The hypothesis predicts:

```text
in long-slot context data, A and NMI(route, slot) should increase,
and forced expert loss should show a slot-specific diagonal advantage.
```

## Workflow Interface

The workflow is:

```text
four-slot synthetic data
  -> strengthen slot context before B
  -> initialize router rows by B-position slot centroids
  -> train top-1 selected-gate MoE
  -> measure route-slot alignment at B positions
  -> measure slot-conditioned expert utility
  -> decide whether stronger context signal is sufficient for functional specialization
```

The output is not a new model. The output is a mechanism decision:

```text
weak context signal explains the previous failure
```

or:

```text
even visible and predictive slot features are not sufficient for learned top-1 functional specialization
```

## Minimal Computational Test

Use full four slots and four experts.

### Scheme A: repeated slot cue

```text
slot 0: A A A A A  B_i -> Y_{0,i}
slot 1: C C C C C  B_i -> Y_{1,i}
slot 2: G G G G G  B_i -> Y_{2,i}
slot 3: K K K K K  B_i -> Y_{3,i}
```

### Scheme B: distributed slot code

```text
slot 0: p0 q0 r0 t0 u0  B_i -> Y_{0,i}
slot 1: p0 q1 r1 t1 u1  B_i -> Y_{1,i}
slot 2: p1 q0 r1 t0 u1  B_i -> Y_{2,i}
slot 3: p1 q1 r0 t1 u0  B_i -> Y_{3,i}
```

In Scheme B, no single cue token uniquely determines the slot. The full context code is needed.

Router initialization:

$$
\mu_s=\mathbb{E}_i[h(B_i\mid s)], \qquad \bar\mu=\mathbb{E}_s[\mu_s]
$$

$$
w_s \leftarrow \alpha\cdot \operatorname{Normalize}\left((\Sigma+\lambda I)^{-1}(\mu_s-\bar\mu)\right)
$$

Compare:

```text
short one-token slot cue + slot init
long repeated cue + slot init
long distributed code + slot init
oracle slot router upper bound
```

## Falsifiable Conclusion

Supported if:

```text
long-slot conditions make slot decodable from B hidden states;
route-slot matrix becomes diagonal after expert permutation;
assigned expert matches the slot utility-best expert;
forced expert loss and ablation utility show slot-specific diagonal advantage;
this holds across seeds and is stronger than the short-slot condition.
```

Weakened if:

```text
slot is decodable from B hidden states but routing does not align;
routing aligns with slot but expert utility does not;
only repeated cue works, but distributed code fails;
only assignment metrics improve while target CE or expert utility does not.
```

Redirected if:

```text
oracle slot routing has no utility gap -> the task does not create expert-specific utility;
oracle works but learned routing fails -> top-1 NTP dynamics fail to convert predictive slot factors into expert decomposition.
```

## Current Evidence

Current evidence is negative and boundary-setting:

```text
semantic/context initialization can improve early B-context routing;
final routing alignment decays during training;
final hidden states still contain recoverable B-context boundary;
semantic routing is not automatically a functional expert route.
```

The 2026-05-26 slot-context dominance diagnostic adds a sharper split:

```text
single-B: slot context can control routing and align assignment with utility;
multi-B: slot remains decodable and predictive, but learned routing does not robustly bind assignment to utility under B-identity variation.
```

Key result:

| Mode | Condition | Target Acc | Probe h_B->slot | NMI(route, slot) | Assign-Utility |
|---|---|---:|---:|---:|---:|
| `single_b_sanity` | `A_long_repeated_slot_init` | 1.000 | 1.000 | 1.000 | 1.000 |
| `single_b_sanity` | `B_long_distributed_slot_init` | 1.000 | 1.000 | 0.893 | 1.000 |
| `multi_b_primary` | `A_long_repeated_slot_init` | 1.000 | 1.000 | 0.593 | 0.921 |
| `multi_b_primary` | `B_long_distributed_slot_init` | 1.000 | 1.000 | 0.297 | 0.733 |
| `multi_b_primary` | `Oracle_slot_router` | 1.000 | 0.997 | 1.000 | 1.000 |

The 2026-05-27 trajectory follow-up closes five diagnostic gaps:

```text
initial-vs-final route NMI;
route NMI trajectory;
route-slot and forced-utility heatmaps;
B-position-only Oracle;
random-init controls.
```

Key trajectory result:

| Mode | Condition | NMI 0 -> 1600 | Assign-Utility 0 -> 1600 | Slot-center norm 0 -> 1600 |
|---|---|---:|---:|---:|
| `single_b` | `A_long_repeated_slot_init` | 1.000 -> 1.000 | 0.438 -> 1.000 | 1.089 -> 3.186 |
| `single_b` | `B_long_distributed_slot_init` | 1.000 -> 0.893 | 0.438 -> 1.000 | 0.491 -> 4.185 |
| `multi_b` | `A_long_repeated_slot_init` | 0.243 -> 0.591 | 0.565 -> 0.925 | 1.166 -> 4.903 |
| `multi_b` | `B_long_distributed_slot_init` | 0.078 -> 0.313 | 0.326 -> 0.747 | 0.652 -> 4.298 |
| `multi_b` | `Oracle_b_position_only` | 1.000 -> 1.000 | 0.625 -> 1.000 | 1.166 -> 3.644 |
| `multi_b` | `B_long_random_init` | 0.006 -> 0.010 | 0.420 -> 0.998 | 0.652 -> 5.039 |

Interpretation:

```text
The weak-context explanation is only partially supported.
It explains the fixed-B diagnostic, but not robust multi-B functional specialization.
The stronger failure mode is multi-B initialization geometry plus route-function binding under identity variation.
```

The important correction is:

```text
multi-B slot-centroid init is not initially clean diagonal routing.
Training increases slot-center separation and route NMI, but does not fully convert visible slot geometry into stable top-1 functional routing.
Oracle_b_position_only = 1.0 shows that B-position routing alone is sufficient for the upper bound.
Random-init B_long can show high Assign-Utility with near-zero route NMI, so Assign-Utility must be read with route NMI and utility heatmaps.
Seed-level final routing heatmaps confirm that the multi-B conclusion is not an artifact of averaging: A_long improves but is not stable across seeds, and B_long does not form a reliable slot-to-expert permutation.
```

Result links:

```text
summary: Projects/from-attention-to-search/main/experiments/slot_context_dominance_router_specialization/summary.md
detailed: Projects/from-attention-to-search/main/experiments/slot_context_dominance_router_specialization/detailed.md
sync closure: Projects/from-attention-to-search/XingyuD/sync/0526_slot_context_dominance/report.md
single-B result dir: Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/slot_context_dominance_router_specialization/slot_context_single_b_full_20260526
multi-B result dir: Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/slot_context_dominance_router_specialization/slot_context_multi_b_full_20260526
single-B trajectory result dir: Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/slot_context_dominance_router_specialization/slot_context_single_b_trajectory_full_20260527
multi-B trajectory result dir: Projects/from-attention-to-search/XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/results/slot_context_dominance_router_specialization/slot_context_multi_b_trajectory_full_20260527
```

## Claim Boundary And Next Decision

Supported claim:

```text
Top-1 MoE can form slot-controlled routing in a fixed-B diagnostic when slot is visible and predictive.
```

Weakened claim:

```text
Predictive slot visibility plus slot-centroid init is sufficient for robust multi-B functional specialization.
```

Claim boundary:

```text
This evidence only covers four-slot/four-expert synthetic NTP with no load-balance objective.
It does not rule out auxiliary route-function binding, utility-aware routing regularizers, deeper models, or real-corpus specialization.
It also shows that assignment-utility agreement alone can overstate specialization when utility collapses to a common expert.
```

Next decision:

```text
Do not extend the context-length sweep.
Run the next minimal test on multi_b_primary with an explicit route-function binding signal,
such as a target-position slot-router auxiliary loss or utility-aware routing regularizer.
Judge by route NMI, route heatmap, forced utility heatmap, and assignment-utility together,
especially on the distributed-code condition.
```
