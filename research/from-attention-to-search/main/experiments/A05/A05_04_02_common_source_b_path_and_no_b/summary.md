# A05_04_02 Common Source B-Path And No-B Summary

## Conclusion

The experiment supports a refined source model for common-logit collapse: the direct `B_CONST` residual identity is a major common-source contributor, but it is not the complete mechanism.

Two observations decide the claim:

- Removing only the routed-position B residual in existing B-position checkpoints raises final NMI from `0.080` to `0.797` and drops mean absolute common margin from `2.316` to `0.271`.
- Removing only B's self-value attention contribution does not change the result: final NMI remains `0.080` and common margin remains high at `2.259`.

Deleting `B_CONST` from the task also improves specialization, but does not fully solve it under random initialization. The no-B baseline reaches mean final NMI `0.802`, yet one seed still collapses (`20260523`, NMI `0.083`, max load `0.977`). Early common cancellation on the no-B task is more robust: `NoB_cancel_0_10` reaches mean NMI `0.930` with minimum NMI `0.843`.

## Purpose

Separate three possible common-source explanations:

1. `B_CONST` direct residual identity at the routed position.
2. B self-attention value contribution.
3. A more general top-1 common-stream lock-in that can persist even without B.

## How

P1 uses existing Round-1 B-position checkpoints and applies hidden-state counterfactual patches at the routed `B_CONST` position:

| condition | meaning |
|---|---|
| `original` | standard `h_B = LN(x_B + attention_output_B)` |
| `no_b_residual` | replace the routed-position residual `x_B` with zero, while keeping the attention output |
| `no_b_self_value` | subtract only B's self-value contribution through attention |
| `no_b_full_embedding` | remove the full B embedding path and recompute attention |

P2 changes the data from `SLOT_s B_CONST Y_s` to `SLOT_s Y_s`, routes and computes loss at the slot position, and trains three variants:

| variant | meaning |
|---|---|
| `NoB_baseline` | random initialization, no common cancellation |
| `NoB_cancel_0_10` | common-logit cancellation through step 10 |
| `NoB_cancel_0_final` | common-logit cancellation through the full run |

## Metrics

Primary metric: route-slot NMI, because it measures slot-to-expert specialization rather than load balance alone.

Secondary metrics: max load, active experts, target accuracy, mean absolute common margin, mean absolute slot margin, and route heatmaps.

## P1 B-Path Attribution

| condition | final NMI | max load | common margin | slot margin | interpretation |
|---|---:|---:|---:|---:|---|
| `original` | 0.080 | 0.969 | 2.316 | 0.556 | strong common-dominated collapse |
| `no_b_residual` | 0.797 | 0.550 | 0.271 | 0.434 | direct B residual is a major common source |
| `no_b_self_value` | 0.080 | 0.969 | 2.259 | 0.542 | B self-value attention path is not the main source |
| `no_b_full_embedding` | 0.256 | 0.812 | 0.378 | 0.180 | too destructive; it reduces common but also damages slot signal |

## P2 No-B Training

| variant | mean final NMI | min final NMI | max load | accuracy | common margin | interpretation |
|---|---:|---:|---:|---:|---:|---|
| `NoB_baseline` | 0.802 | 0.083 | 0.497 | 1.000 | 1.396 | deleting B helps, but random init can still collapse |
| `NoB_cancel_0_10` | 0.930 | 0.843 | 0.372 | 1.000 | 0.898 | most robust; early anti-common intervention helps |
| `NoB_cancel_0_final` | 0.918 | 0.613 | 0.372 | 1.000 | 0.905 | helpful but less robust than early-only cancellation |

## Result A Means

If `no_b_residual` improves NMI and reduces common margin while preserving slot signal, then the direct B residual path is a major causal contributor to common-logit dominance.

This is supported.

## Result B Means

If `no_b_self_value` does not improve NMI or reduce common margin, then the common source is not mainly B attending to itself through the value path.

This is supported.

## Interpretation

The best current model is:

`B residual identity + routed-position common stream + sparse top-1 self-reinforcement`

The B residual identity is the strongest identified amplifier in the original B-position task. It explains why the original baseline is so vulnerable to single-expert collapse. However, the no-B baseline still has one collapsed seed, so the common-source problem is not fully explained by B alone.

The no-B cancellation result also sharpens the intervention picture: early common cancellation is better framed as an anti-lock-in intervention than as a permanent architectural requirement.

## Claim Boundary

This experiment identifies a major contributor, not the full common source. It does not prove that expert computation is causally slot-specialized, does not transfer the claim to real language models, and does not show that load balance alone is specialization.

## Next Decision

Audit the residual common source after deleting or weakening the direct B residual path: distinguish attention-output common components from top-1 feedback amplification.

## Source Run

- Result dir: `results/common_source_b_path_and_no_b_4gpu_20260610`
- Figure dir: `figures/common_source_b_path_and_no_b_4gpu_20260610`
- Job id: `pt-8wd06kh3`
- Runtime log: `logs/acp/common_source_b_path_and_no_b_4gpu_20260610_runtime_20260610_053846.log`
