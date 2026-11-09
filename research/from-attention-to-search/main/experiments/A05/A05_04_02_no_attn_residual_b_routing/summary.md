# A05_04_02 No-Attention-Residual B-Routing Summary

## Conclusion

Removing the direct attention-block residual into the router input strongly improves routing specialization on the original B-position task, while preserving target accuracy. Mean final slot-to-expert NMI rises from `0.080` in the Round-1 standard residual baseline to `0.780`; mean max load falls from `0.969` to `0.594`; target accuracy remains `1.000`.

This supports the direct `B_CONST` residual identity as a major causal contributor to common-logit collapse. It does not fully solve specialization: no seed reaches one-slot-one-expert routing, and several seeds merge three slots into one expert. The result is slot-consistent routing with partial expert sharing, not full slot-level specialization.

## Purpose

Test whether `x_B` in `h_B = LN(x_B + attention_output_B)` is a major common source for dot-product top-1 routing collapse.

## How

- Data: original `SLOT_s B_CONST Y_s` task.
- Intervention: use `h = LN(attention_output)` as the MoE/router input.
- Kept fixed: no positional encoding, dot-product router, sparse top-1 routing, B-position loss and routing metrics, post-MoE residual.

## Metrics

- Round1_P1_standard_reference: NMI `0.080`, max_load `0.969`, active_experts `1.125`, accuracy `1.000`.
- NoAttnResidual_B_baseline: NMI `0.780`, max_load `0.594`, active_experts `2.625`, accuracy `1.000`.

## Seed-Level Final Results

| seed | NMI | max load | active experts | accuracy | routing pattern |
|---|---:|---:|---:|---:|---|
| 20260521 | 0.866 | 0.500 | 3 | 1.000 | two slots share one expert |
| 20260522 | 0.866 | 0.500 | 3 | 1.000 | two slots share one expert |
| 20260523 | 0.866 | 0.500 | 3 | 1.000 | two slots share one expert |
| 20260524 | 0.637 | 0.750 | 2 | 1.000 | three slots share one expert |
| 20260525 | 0.637 | 0.750 | 2 | 1.000 | three slots share one expert |
| 20260526 | 0.866 | 0.500 | 3 | 1.000 | two slots share one expert |
| 20260527 | 0.637 | 0.750 | 2 | 1.000 | three slots share one expert |
| 20260528 | 0.866 | 0.500 | 3 | 1.000 | two slots share one expert |

## Figure

![Final routing](figures/no_attn_residual_b_routing_4gpu_20260610/final_routing_standard_vs_no_attn_residual.png)

## Claim Boundary

This removes only the attention-block residual into the router input, not every residual connection. The post-MoE residual is kept. The result supports the direct B residual as a major causal contributor, but it does not identify the full common source and does not prove full expert specialization.

## Source Run

- Result dir: `results/no_attn_residual_b_routing_4gpu_20260610`
- Raw metrics: `results/no_attn_residual_b_routing_4gpu_20260610/final_metrics_by_seed.csv`
- ACP job id: `pt-pp2rcsg9`
- Runtime logs and per-seed raw checkpoint trees are intentionally omitted from git.
