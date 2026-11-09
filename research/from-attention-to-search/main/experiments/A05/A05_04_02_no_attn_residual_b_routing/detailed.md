# A05_04_02 No-Attention-Residual B-Routing Detailed Record

## 0. Quick Recap

Purpose: test whether direct residual identity at the B-routed position causes common-logit dominance.

Hypothesis: removing `x_B` from the router input should reduce collapse and improve route-slot NMI.

Experiment logic: keep the original B task, but replace `LN(x + attention_output)` with `LN(attention_output)` before the MoE/router.

Conclusion: removing the direct attention-block residual into the router input strongly improves routing compared with the standard residual baseline, but does not produce full one-slot-one-expert specialization.

Evidence: mean final NMI improves from `0.080` to `0.780`, mean max load falls from `0.969` to `0.594`, accuracy remains `1.000`, and final common margin falls from `2.316` to `1.080` while final slot margin rises from `0.556` to `1.863`.

## Source Files

- Protocol: `protocol_for_approval.md`
- Runner: `scripts/run_no_attn_residual_b_routing.py`
- Submit script: `scripts/submit_no_attn_residual_b_routing_4gpu_acp.sh`
- Reference Round-1 run: `../A05_04_01_round1_slot_specialization_protocol_dot_product/results/round1_slot_specialization_dot_product_4gpu_20260609`

## Run Metadata

- Run name: `no_attn_residual_b_routing_4gpu_20260610`
- ACP job id: `pt-pp2rcsg9`
- Job status: `SUCCEEDED`
- Seeds: `20260521` to `20260528`
- Checkpoints: `0, 1, 2, 5, 10, 20, 50, 1600`
- Result dir: `results/no_attn_residual_b_routing_4gpu_20260610`
- Figure dir: `figures/no_attn_residual_b_routing_4gpu_20260610`
- Runtime logs and per-seed raw checkpoint trees are intentionally omitted from git.

## Intervention

- Standard router input: `h = LN(x + attention_output)`.
- Intervened router input: `h = LN(attention_output)`.
- Post-MoE residual is kept: `hidden = LN(h + MoE(h))`.
- Positional embeddings are zeroed and frozen, as in Round 1.
- Router is dot-product sparse top-1.

## Final Aggregate

| condition | mean NMI | mean max load | mean active experts | accuracy |
|---|---:|---:|---:|---:|
| Round1 standard residual reference | 0.080 | 0.969 | 1.125 | 1.000 |
| No attention residual | 0.780 | 0.594 | 2.625 | 1.000 |

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

## Margin Decomposition

Final absolute margin means:

| condition | common margin | slot margin | position margin | residual margin |
|---|---:|---:|---:|---:|
| Round1 standard residual reference | 2.316 | 0.556 | 0.005 | 0.005 |
| No attention residual | 1.080 | 1.863 | 0.032 | 0.020 |

The intervention flips the relative strength of common and slot margins. This is the main evidence that the direct attention-block residual carried a strong common direction into the dot-product router.

## Interpretation

Observation: every final seed has per-slot route purity `1.000`, so each slot is internally route-consistent.

Interpretation: the remaining failure mode is not within-slot instability. It is many-to-one slot merging: some seeds use three experts for four slots, and some use two experts for four slots.

Decision: direct B residual identity is a major collapse amplifier, but removing it alone is not sufficient for full slot-to-expert specialization.

Claim boundary: this experiment does not remove the attention value path, does not remove the post-MoE residual, and does not prove that the residual stream is the only common source.

## Artifact Map

- Final metrics: `results/no_attn_residual_b_routing_4gpu_20260610/final_metrics_by_seed.csv`
- Step metrics: `results/no_attn_residual_b_routing_4gpu_20260610/metrics_by_step.csv`
- Route confusion: `results/no_attn_residual_b_routing_4gpu_20260610/route_confusion_by_step.csv`
- Margin decomposition: `results/no_attn_residual_b_routing_4gpu_20260610/margin_decomposition_by_step.csv`
- Training curve: `results/no_attn_residual_b_routing_4gpu_20260610/training_curve.csv`
- Reference metrics: `results/no_attn_residual_b_routing_4gpu_20260610/reference_round1_p1_clean_baseline_final_metrics.csv`
